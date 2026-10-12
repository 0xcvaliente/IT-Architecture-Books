"""Lab 4: durable local acceptance, then a handoff that may crash."""
import hashlib
import json
import sqlite3
import uuid

class Conflict(Exception):
    """The same submitter reused a key with a different payload."""

def open_db() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:", isolation_level=None)  # explicit BEGIN
    db.executescript("""
    CREATE TABLE request (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL,
      submitted_by TEXT NOT NULL, submission_key TEXT NOT NULL,
      digest TEXT NOT NULL, UNIQUE (tenant, submitted_by, submission_key));
    CREATE TABLE handoff (submission_id TEXT PRIMARY KEY, state TEXT NOT NULL);
    """)
    return db

def submit(db: sqlite3.Connection, tenant: str, user: str, key: str,
           payload: dict) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(body.encode()).hexdigest()
    db.execute("BEGIN IMMEDIATE")
    try:
        old = db.execute("SELECT submission_id, digest FROM request WHERE tenant = ?"
                         " AND submitted_by = ? AND submission_key = ?",
                         (tenant, user, key)).fetchone()
        if old and old[1] != digest:
            raise Conflict(key)
        if old is None:
            submission_id = str(uuid.uuid4())   # assigned by the portal
            db.execute("INSERT INTO request VALUES (?, ?, ?, ?, ?)",
                       (submission_id, tenant, user, key, digest))
            db.execute("INSERT INTO handoff VALUES (?, 'pending')", (submission_id,))
        else:
            submission_id = old[0]
        db.execute("COMMIT")
        return submission_id
    except Exception:
        db.execute("ROLLBACK")
        raise

class FakeCRM:
    def __init__(self, idempotent: bool) -> None:
        self.idempotent = idempotent
        self.cases: dict[str, str] = {}          # case ID -> idempotency key

    def create_case(self, idempotency_key: str) -> str:
        if self.idempotent:
            for case_id, key in self.cases.items():
                if key == idempotency_key:
                    return case_id               # repeat returns the same case
        case_id = f"case-{len(self.cases) + 1}"
        self.cases[case_id] = idempotency_key
        return case_id

CLAIM = ("UPDATE handoff SET state = 'in_flight' WHERE submission_id = ?"
         " AND state IN ('pending', 'retry_due')")

def deliver_one(db: sqlite3.Connection, crm: FakeCRM, crash: bool = False) -> bool:
    row = db.execute("SELECT submission_id FROM handoff WHERE state IN"
                     " ('pending', 'retry_due') LIMIT 1").fetchone()
    if row is None or db.execute(CLAIM, row).rowcount != 1:
        return False                             # nothing due, or claimed elsewhere
    crm.create_case(idempotency_key=row[0])      # the submission ID
    if crash:
        raise RuntimeError("worker stopped before recording the CRM result")
    db.execute("UPDATE handoff SET state = 'confirmed' WHERE submission_id = ?"
               " AND state = 'in_flight'", row)
    return True

def expire_leases(db: sqlite3.Connection) -> None:
    """Simulate lease expiry after a crash: every in_flight claim becomes retryable."""
    db.execute("UPDATE handoff SET state = 'retry_due' WHERE state = 'in_flight'")

db = open_db()
payload = {"asset": "v1", "description": "Pump vibrates at start-up"}
first = submit(db, "t1", "c1", "key-1", payload)
assert submit(db, "t1", "c1", "key-1", payload) == first
print("same user, key and payload: original submission ID returned")
try:
    submit(db, "t1", "c1", "key-1", {"asset": "v2"})
except Conflict:
    print("same user and key, changed payload: rejected as a conflict")
else:
    raise AssertionError("changed payload accepted")
assert submit(db, "t1", "c2", "key-1", payload) != first
print("another user, same key: a separate submission")

db = open_db()
sid = submit(db, "t1", "c1", "key-1", payload)
first_claim = db.execute(CLAIM, (sid,)).rowcount     # worker A
second_claim = db.execute(CLAIM, (sid,)).rowcount    # worker B, a moment later
print(f"two claims on one handoff change {first_claim} and {second_claim} rows")

for idempotent in (False, True):
    db = open_db()
    submit(db, "t1", "c1", "key-1", payload)
    crm = FakeCRM(idempotent)
    try:
        deliver_one(db, crm, crash=True)
    except RuntimeError:
        expire_leases(db)
    deliver_one(db, crm)
    state = db.execute("SELECT state FROM handoff").fetchone()[0]
    print(f"idempotent CRM={idempotent}: handoff {state}, CRM cases={len(crm.cases)}")
