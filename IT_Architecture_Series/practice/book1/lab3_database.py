"""Lab 3: constraints, and one transaction for a request and its handoff."""
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript("""
CREATE TABLE asset (
  tenant_id TEXT NOT NULL, asset_id TEXT NOT NULL, name TEXT NOT NULL,
  PRIMARY KEY (tenant_id, asset_id));
CREATE TABLE request (
  tenant_id TEXT NOT NULL, submission_id TEXT NOT NULL,
  asset_id TEXT NOT NULL, submitted_by TEXT NOT NULL,
  submission_key TEXT NOT NULL,
  PRIMARY KEY (tenant_id, submission_id),
  UNIQUE (tenant_id, submitted_by, submission_key),
  FOREIGN KEY (tenant_id, asset_id) REFERENCES asset (tenant_id, asset_id));
CREATE TABLE handoff (
  handoff_id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL, submission_id TEXT NOT NULL,
  state TEXT NOT NULL CHECK (state IN
    ('pending', 'in_flight', 'confirmed', 'retry_due', 'manual_review')),
  FOREIGN KEY (tenant_id, submission_id)
    REFERENCES request (tenant_id, submission_id));
INSERT INTO asset VALUES ('t1', 'v1', 'Pump A'), ('t2', 'v2', 'Compressor B');
INSERT INTO request VALUES ('t1', 's1', 'v1', 'c1', 'key-1');
""")

NEW_REQUEST = "INSERT INTO request VALUES (?, ?, ?, ?, ?)"
NEW_HANDOFF = "INSERT INTO handoff VALUES (?, ?, ?, ?)"

def expect_rejection(label: str, sql: str, row: tuple) -> None:
    try:
        with db:
            db.execute(sql, row)
    except sqlite3.IntegrityError:
        print(f"{label}: rejected by a constraint")
    else:
        raise AssertionError(f"{label}: unexpectedly accepted")

expect_rejection("cross-tenant asset", NEW_REQUEST, ("t1", "s2", "v2", "c1", "k2"))
expect_rejection("same user, same key", NEW_REQUEST, ("t1", "s3", "v1", "c1", "key-1"))
expect_rejection("unknown handoff state", NEW_HANDOFF, ("h1", "t1", "s1", "done"))
with db:  # user c2 has its own key space, so this is a new request
    db.execute(NEW_REQUEST, ("t1", "s5", "v1", "c2", "key-1"))
print("another user, same key: stored as a separate request")

try:
    with db:  # commits on success, rolls back if the block raises
        db.execute(NEW_REQUEST, ("t1", "s4", "v1", "c1", "key-4"))
        db.execute(NEW_HANDOFF, ("h4", "t1", "s4", "pending"))
        raise RuntimeError("simulated crash before commit")
except RuntimeError:
    pass

def count(sql: str) -> int:
    return db.execute(sql).fetchone()[0]

requests = count("SELECT count(*) FROM request WHERE submission_id = 's4'")
handoffs = count("SELECT count(*) FROM handoff WHERE handoff_id = 'h4'")
assert (requests, handoffs) == (0, 0)
print(f"after rollback: request s4 = {requests}, handoff h4 = {handoffs}")
