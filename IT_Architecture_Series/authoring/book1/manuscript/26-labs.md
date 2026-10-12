# Practical labs

These twelve labs turn the chapters into observable work. Each lab states its goal, the chapters it builds on, an estimated time that includes writing up the result, the steps, and a reflection question. Nine labs include short Python listings. They use Python 3.10 or newer and the standard library only, and they never contact external services. To run a lab, copy its listings, in the order shown, into one file and run it with `python3` followed by the file name. The expected output printed after each listing is exactly what the code produces.

The listings are deliberately small models of one mechanism each. For example, the SQLite labs show constraints and transactions, but SQLite's locking differs from PostgreSQL's isolation levels. Each lab names what its model leaves out, so that your write-up can state the same limits.

## Lab 1 Requirements and the request journey

**Goal.** Turn the Meridian case into a requirement register, a context view and a request journey that shows where responsibility is accepted.

**Prerequisites.** Chapters 1 to 4. **Estimated time.** Three hours.

### Steps

1. Write the business outcome in two sentences. List at least five stakeholders and one question you would ask each.
2. Separate the facts given in the case brief from the assumptions you add. Mark each assumption with an owner who could confirm it.
3. Fill in a requirement register with at least six rows: a submission behaviour, an access rule, a latency scenario, an availability definition, a recovery expectation and a data lifecycle capability. Leave any unknown policy explicitly open.
4. Draw a context view with customers, service agents, the portal, the CRM, the identity provider, ERP and analytics.
5. Draw a separate request journey for one submission. Label name resolution, the protected connection, API validation, authorisation, durable storage, the receipt and the later CRM handoff. Mark the point where the portal accepts responsibility.
6. Work through the three failures in the second table below on paper.

Use this layout for the register. The first row is a worked example.

| ID | Scenario | Measure | Owner | Test |
| --- | --- | --- | --- | --- |
| R1 | A valid submission arrives at peak load | 95 percent of receipts within 1 s, excluding upload | Product owner | Open-loop load test at 20 per second |
| R2 | … | … | … | … |

For each failure, record what the user sees, what state exists and what support staff need to inspect.

| Failure | What the user sees | State that exists | What support inspects |
| --- | --- | --- | --- |
| The portal's name does not resolve | … | … | … |
| The database rejects the transaction | … | … | … |
| The CRM is unavailable after commit | … | … | … |

**Expected result.** Your views show sign-in and analytics as separate interactions, rather than one chain through every component. The register contains measurable conditions and an open question about the CRM's duplicate behaviour.

### Reflection

Which requirement could change the initial architecture most? What is the smallest investigation that would settle it? Keep this first version and revise it after Lab 4.

## Lab 2 Domain rules and access checks

**Goal.** Separate structural validation from authorisation, and test a staff policy based on a business unit and a set of customer-organisation scopes.

**Prerequisites.** Chapters 5 and 9. **Estimated time.** Two to three hours.

### Steps

1. Read Listing 2.1. Identify the submission value, the validation function and the access function. Explain why `validate` establishes nothing about who may act.
2. Note that a staff member's `scopes` is a set: one agent may serve several tenants, so the policy checks whether the request's tenant is in that set.
3. Save Listings 2.1 and 2.2 in one file and run it.
4. Treat each `Principal` as trusted input from a separate authentication and policy layer. If a client could set `role` or `scopes` itself, the boundary would offer no protection.

Listing 2.1 defines the domain value, the principal and the policy.

~~~python
"""Lab 2: structural validation and resource-level access checks."""
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Submission:
    tenant_id: str
    customer_id: str
    asset_id: str
    description: str

def validate(item: Submission) -> None:
    """Check structure only; who may act is decided by a separate check."""
    if not (item.tenant_id and item.customer_id and item.asset_id):
        raise ValueError("required identifier missing")
    if not 1 <= len(item.description) <= 2000:
        raise ValueError("description must be 1 to 2000 characters")

@dataclass(frozen=True)
class Principal:
    subject: str
    role: str                             # "customer" or "agent"
    tenant_id: str = ""                   # a customer belongs to one tenant
    org_delegation: bool = False          # explicit organisation-wide reading
    business_unit: str = ""               # agents only
    scopes: frozenset[str] = frozenset()  # tenants an agent may serve

@dataclass(frozen=True)
class Request:
    tenant_id: str
    submitted_by: str
    business_unit: str

def may_read(p: Principal, r: Request) -> bool:
    if p.role == "customer":
        same_tenant = p.tenant_id == r.tenant_id
        return same_tenant and (p.subject == r.submitted_by or p.org_delegation)
    if p.role == "agent":
        return p.business_unit == r.business_unit and r.tenant_id in p.scopes
    return False                          # unknown roles are denied
~~~

Listing 2.2 runs the validation checks and a table of access cases.

~~~python
def check_validation() -> None:
    validate(Submission("t1", "c1", "a1", "Pump vibrates at start-up"))
    for size in (0, 2001):
        try:
            validate(Submission("t1", "c1", "a1", "x" * size))
        except ValueError:
            continue
        raise AssertionError(f"description of length {size} accepted")
    print("validation: 3 checks passed")

REQUEST = Request(tenant_id="t1", submitted_by="c1", business_unit="north")
CUSTOMER = Principal("c1", "customer", tenant_id="t1")
COLLEAGUE = Principal("c2", "customer", tenant_id="t1")
AGENT = Principal("s1", "agent", business_unit="north",
                  scopes=frozenset({"t1", "t7"}))

CASES = [
    ("customer reads own request", CUSTOMER, True),
    ("colleague without delegation", COLLEAGUE, False),
    ("colleague with delegation", replace(COLLEAGUE, org_delegation=True), True),
    ("customer in another tenant", replace(CUSTOMER, tenant_id="t2"), False),
    ("agent with unit and scope", AGENT, True),
    ("agent in another unit", replace(AGENT, business_unit="south"), False),
    ("agent without tenant scope", replace(AGENT, scopes=frozenset({"t7"})), False),
    ("unknown role", Principal("x1", "auditor"), False),
]

check_validation()
for name, principal, expected in CASES:
    allowed = may_read(principal, REQUEST)
    assert allowed == expected, name
    print(f"{'allow' if allowed else 'deny':5}  {name}")
print(f"access: {len(CASES)} cases passed")
~~~

Expected output:

~~~text
validation: 3 checks passed
allow  customer reads own request
deny   colleague without delegation
allow  colleague with delegation
deny   customer in another tenant
allow  agent with unit and scope
deny   agent in another unit
deny   agent without tenant scope
deny   unknown role
access: 8 cases passed
~~~

### Change and extend

- Add a case for an agent whose `business_unit` is empty, and one for a customer whose delegation has been revoked. Both should be denied.
- Add a `reviewer` role that may read only requests explicitly assigned to that reviewer. Add the cases first, watch them fail, then change `may_read`.
- In your own copy, remove the check `r.tenant_id in p.scopes`. Run the listing and note which case detects the defect, then restore the check.

### Reflection

Which rule would be hard to express with a broad "service agent" role alone? Which system should supply the trusted business-unit assignment and scope set?

## Lab 3 Constraints and transaction rollback

**Goal.** See which invariants the database enforces, and show that one transaction keeps a request and its handoff record together.

**Prerequisites.** Chapter 6. **Estimated time.** Three hours.

### Steps

1. Read the schema in Listing 3.1. The composite foreign key ties a request to an asset in the same tenant. The unique constraint allows each submitting user one request per submission key in each tenant, as in Chapter 6. The check constraint allows only the five handoff states.
2. Save Listings 3.1 and 3.2 in one file and run it.
3. For each rejected insert, name the invariant it protects.
4. The last experiment inserts a request and its handoff record in one transaction, then fails before commit. Both rows disappear together.

Listing 3.1 creates an in-memory database with foreign keys switched on.

~~~python
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
~~~

Listing 3.2 tries three invalid inserts, one valid reuse of a key by another user and one interrupted transaction.

~~~python
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
~~~

Expected output:

~~~text
cross-tenant asset: rejected by a constraint
same user, same key: rejected by a constraint
unknown handoff state: rejected by a constraint
another user, same key: stored as a separate request
after rollback: request s4 = 0, handoff h4 = 0
~~~

SQLite enforces foreign keys only when the `PRAGMA` is set, and its locking model differs from PostgreSQL's isolation levels. Record your results as SQLite behaviour.

### Change and extend

- Commit the request in its own transaction before inserting the handoff, inject the same failure, and compare the counts.
- Add a `customer` table with a composite tenant and customer key, and make each request refer to a customer in its own tenant.
- Optionally, open two connections to a temporary database file and observe SQLite's locking during concurrent writes. If you repeat the experiment in PostgreSQL, record its isolation level and compare.

### Reflection

A foreign key keeps relationships consistent. Which part of the system decides whether an authenticated user may read a given customer's records? What happens to locks and connections if a remote API call is placed between the two inserts?

## Lab 4 The uncertain outcome problem

**Goal.** Show that a durable outbox prevents lost work but leaves duplicate remote effects to the remote contract.

**Prerequisites.** Chapters 8 to 10. **Estimated time.** Four hours.

### Steps

1. Read Listing 4.1. `submit` opens a transaction and looks up the key for this tenant and submitting user. A repeat with the same payload digest returns the original submission ID; a changed payload raises `Conflict`. A new key gets a fresh submission ID, a UUID, stored together with a `pending` handoff record.
2. Read Listing 4.2. The fake CRM is outside the database transaction. The worker claims a record with a conditional update (`CLAIM`) and checks that exactly one row changed, so two workers can never both own the same handoff. It then calls the CRM with the submission ID as the idempotency key and records `confirmed`. A simulated crash stops it after the CRM call. The listing does not store lease times: `expire_leases` stands in for the moment a real lease runs out, by returning every `in_flight` record to `retry_due`. A production claim stores a lease expiry and resets only claims whose lease has passed.
3. Save Listings 4.1 to 4.3 in one file and run it.
4. Draw the failure sequence. Mark the local transaction, the remote side effect, the crash point and the retry.

Listing 4.1 accepts submissions durably and idempotently.

~~~python
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
~~~

Listing 4.2 provides the fake CRM, the worker and a simulated lease expiry.

~~~python
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
~~~

Listing 4.3 runs the local checks and two delivery scenarios.

~~~python
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
~~~

Expected output:

~~~text
same user, key and payload: original submission ID returned
same user and key, changed payload: rejected as a conflict
another user, same key: a separate submission
two claims on one handoff change 1 and 0 rows
idempotent CRM=False: handoff confirmed, CRM cases=2
idempotent CRM=True: handoff confirmed, CRM cases=1
~~~

The local guarantees hold in both scenarios. The duplicate CRM case appears only when the CRM ignores the idempotency key. The simulation is single-threaded, and a fake CRM cannot show how a real vendor behaves under concurrency; for Meridian, that remains a release condition.

### Change and extend

- Add a scenario in which the CRM call fails before creating anything. Describe the expected states before you change the code.
- Move the database to a temporary file, open two connections and call `submit` with the same user and key from two threads at once. Which statement decides the race, and what does the losing caller receive?
- Before retrying, look up the external key in the CRM and record `confirmed` if a case exists. Move the record to `manual_review` if the lookup finds more than one case.
- Write an ADR that states the exact guarantee you can make today, the residual risk and the reconciliation process.

### Reflection

Would writing `confirmed` before the CRM call solve the problem? Show the failure that would then become possible.

## Lab 5 Capacity, backlog and recovery

**Goal.** Derive arrival rates from the case, model a CRM outage and its recovery, and connect the results to recovery objectives.

**Prerequisites.** Chapters 12 and 13. **Estimated time.** Three hours.

### Steps

1. Read Listing 5.1. Rates are constant, so the model is a fluid approximation, without random arrivals or variable task durations.
2. Note the two stated assumptions: the busiest hour carries ten times the annual average, and the CRM quota allows five handoffs per second.
3. Run the listing and compare the results with the worked example in Chapter 21.
4. Add a scenario of your own for normal demand, and state the units of every input.

Listing 5.1 computes backlogs, drain times and the work at risk in a recovery-point window.

~~~python
"""Lab 5: a deterministic fluid model of backlog growth and recovery."""
ANNUAL_REQUESTS = 100_000
SECONDS_PER_YEAR = 365 * 24 * 3600

def backlog(arrivals: float, service: float, seconds: float,
            start: float = 0.0) -> float:
    """Queue length after `seconds` at constant rates; never below zero."""
    return max(0.0, start + (arrivals - service) * seconds)

def drain_seconds(queue: float, arrivals: float, service: float) -> float:
    """Time to empty the queue; infinite if service cannot exceed arrivals."""
    if service <= arrivals:
        return float("inf")
    return queue / (service - arrivals)

average = ANNUAL_REQUESTS / SECONDS_PER_YEAR    # submissions per second
busy = 10 * average                             # stated busy-hour assumption
quota = 5.0                                     # CRM handoffs per second, assumed

print(f"annual average {average:.4f}/s; busy hour {busy:.4f}/s")
outage = backlog(busy, 0, 30 * 60)
print(f"30-minute CRM outage in the busy hour: {outage:.0f} queued, "
      f"drained in {drain_seconds(outage, busy, quota):.1f} s")
stress = backlog(20, 0, 10 * 60) + backlog(busy, 0, 20 * 60)
print(f"outage overlapping the 10-minute peak: {stress:,.0f} queued, "
      f"drained in {drain_seconds(stress, busy, quota) / 60:.1f} min")
print(f"queue at 30/s in and 24/s out for 15 minutes: "
      f"{backlog(30, 24, 15 * 60):,.0f}")
print(f"submissions inside a 15-minute RPO window in the busy hour: "
      f"{busy * 15 * 60:.1f}")
~~~

Expected output:

~~~text
annual average 0.0032/s; busy hour 0.0317/s
30-minute CRM outage in the busy hour: 57 queued, drained in 11.5 s
outage overlapping the 10-minute peak: 12,038 queued, drained in 40.4 min
queue at 30/s in and 24/s out for 15 minutes: 5,400
submissions inside a 15-minute RPO window in the busy hour: 28.5
~~~

At normal volume a thirty-minute outage leaves a few dozen handoffs, cleared in seconds. Only the rare overlap with the exceptional peak creates a backlog that takes most of an hour to drain.

### Change and extend

- Lower the quota to one handoff per second and find the stress-case drain time. Then set the quota below the busy-hour arrival rate and explain the result.
- Add Chapter 10's retry schedule (2 seconds, doubling, capped at 15 minutes) for handoffs that failed during the outage. Find the longest a handoff can wait after the CRM returns, and compare it with the drain time.
- Estimate storage separately for queued handoff metadata (about 1 KB each) and for attachments (up to 10 MB each) in the stress case, in decimal units.

### Reflection

Which measurements from a real workload would you collect before sizing production? How would skewed task durations change the risk?

## Lab 6 Threats, privacy and evidence

**Goal.** Build a threat model and a data lifecycle register for the Meridian portal.

**Prerequisites.** Chapter 15. **Estimated time.** Four hours.

### Steps

1. On your latest diagrams, mark the public entry points, trust boundaries, administrative access, external vendors and the analytics route.
2. Walk each element and data flow with the STRIDE questions: can someone spoof an identity, tamper with data, repudiate an action, disclose information, deny service or elevate privilege?
3. Record at least six credible threats, including cross-tenant access, credential compromise, malicious attachments, replayed events, resource exhaustion and disclosure through logs.
4. Choose one threat and trace its controls across layers. For cross-tenant access, these might be trusted principal scope, resource-level checks, composite keys, restricted exports and negative tests. State which controls are independent and which share an assumption.
5. Fill in the lifecycle register for every store and processor. Write "policy required before release" where the retention rule is still unknown.

Use this threat register. The first row is a worked example.

| Threat | Asset | Conditions | Impact | Control | Verification | Owner | Residual risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Agent reads a request outside their scopes | Request content | Valid staff login; guessable request IDs | Disclosure to another tenant's competitor | Check unit and scope on every route | Cross-scope denial tests on API, export and search | Portal team | Wrong scope data in the directory |
| … | … | … | … | … | … | … | … |

Use this lifecycle register.

| Store or processor | Purpose | Retention rule | Deletion or correction mechanism | Evidence that it ran |
| --- | --- | --- | --- | --- |
| Operational database | … | … | … | … |
| Object storage | … | … | … | … |
| Analytics tables | … | … | … | … |
| Search index | … | … | … | … |
| Logs | … | … | … | … |
| Backups | … | … | … | … |

As an optional extension, review an AI summarisation feature: treat document content as untrusted input, enforce retrieval permissions, define quality measures and require a human review before consequential use.

**Expected result.** The model connects every control to a concrete threat and a test, and it separates an implemented technical capability from an approved legal or business policy.

### Reflection

Which residual risk needs explicit business acceptance? Which of your verification results would become invalid if the identity provider or the attachment scanner changed?

## Lab 7 SLOs, telemetry and incident response

**Goal.** Calculate an availability SLI, an error budget, a burn rate and a latency SLI from one sample, and see why failed requests must stay in latency percentiles.

**Prerequisites.** Chapter 17. **Estimated time.** Three hours.

### Steps

1. Read Listing 7.1. A small table of buckets generates 1,020 observations: 1,000 eligible requests and 20 ineligible ones rejected for invalid input.
2. Note the measurement rule. Failed requests stay in the latency data at 2,500 ms, the moment the client stopped waiting. The latency SLI counts a request as good only if it received a durable receipt within 1,000 ms.
3. Run the listing.
4. Compare the two percentile lines. Dropping the eight failures hides the slowest outcomes and moves the 99th percentile from 2,400 ms to 1,600 ms.

Listing 7.1 builds the sample and computes the indicators. Percentiles use the nearest-rank method.

~~~python
"""Lab 7: SLIs, error budget, burn rate and latency percentiles."""
import math

TIMEOUT_MS = 2500  # the client stops waiting here; a failure is never "fast"
BUCKETS = [  # (count, eligible, durable receipt, latency in ms)
    (955, True, True, 400), (30, True, True, 1600),
    (7, True, True, 2400), (8, True, False, TIMEOUT_MS),
    (20, False, False, 120),  # ineligible: invalid input, rejected
]
rows = [(e, ok, ms) for n, e, ok, ms in BUCKETS for _ in range(n)]

def nearest_rank(values: list[int], p: float) -> int:
    ordered = sorted(values)
    return ordered[math.ceil(p * len(ordered)) - 1]

eligible = [(ok, ms) for e, ok, ms in rows if e]
good = sum(ok for ok, _ in eligible)
bad = len(eligible) - good
target = 0.999
budget = len(eligible) * (1 - target)
print(f"eligible={len(eligible)} good={good} success={good / len(eligible):.2%}")
print(f"error budget at {target:.1%}: {budget:.1f} bad requests; observed {bad}; "
      f"burn rate {(bad / len(eligible)) / (1 - target):.1f}")
fast = sum(ok and ms <= 1000 for ok, ms in eligible)
print(f"latency SLI (durable receipt within 1000 ms): {fast / len(eligible):.2%}")
all_ms = [ms for _, ms in eligible]
ok_ms = [ms for ok, ms in eligible if ok]
print(f"failures included: p95={nearest_rank(all_ms, 0.95)} ms "
      f"p99={nearest_rank(all_ms, 0.99)} ms")
print(f"failures excluded: p95={nearest_rank(ok_ms, 0.95)} ms "
      f"p99={nearest_rank(ok_ms, 0.99)} ms")
~~~

Expected output:

~~~text
eligible=1000 good=992 success=99.20%
error budget at 99.9%: 1.0 bad requests; observed 8; burn rate 8.0
latency SLI (durable receipt within 1000 ms): 95.50%
failures included: p95=400 ms p99=2400 ms
failures excluded: p95=400 ms p99=1600 ms
~~~

The sample fails the 99.9 percent success objective, with a burn rate of 8, while it meets the latency target of 95 percent within one second. One thousand requests are a short sample, far from a monthly report, so treat the result as a signal to investigate.

### Change and extend

- Add fields for the CRM outcome, the acceptance time and the first time the case was visible in the CRM. Choose an observation cut-off. For confirmed handoffs, compute propagation delay; for those still `pending` or `retry_due`, report their current age and whether the target is already breached.
- Write two alerts: one for a sustained fall in submission success and one for old handoff work. Include the first diagnostic step, the responsible role and the escalation condition.

### Reflection

What happens to the report if monitoring misses an hour? How should a service report communicate that gap?

## Lab 8 Cost sensitivity and a decision review

**Goal.** Reproduce the three-year cost comparison, test its sensitivity and check when a pricing commitment pays off.

**Prerequisites.** Chapters 18 and 19. **Estimated time.** Three hours.

### Steps

1. Read Listing 8.1. All amounts are illustrative euros without discounting, tax or inflation.
2. Run it and check the baselines and the first two scenarios against Chapter 18. The third scenario, a higher support effort for the purchased portal, is new: explain why it changes the ranking.
3. Note the break-even result: a 30 percent discount pays off only when more than 70 percent of the committed hours are used.

Listing 8.1 computes the two baseline totals, three sensitivity scenarios and a commitment comparison.

~~~python
"""Lab 8: three-year cost comparison, sensitivity and commitment break-even."""

def three_year_total(initial: float, integration: float, platform: float,
                     operations: float, exit_cost: float, years: int = 3) -> float:
    """Undiscounted total: one-time costs plus yearly costs plus exit."""
    return initial + integration + years * (platform + operations) + exit_cost

CUSTOM = dict(initial=120_000, integration=35_000, platform=24_000,
              operations=60_000, exit_cost=20_000)
PURCHASED = dict(initial=45_000, integration=55_000, platform=54_000,
                 operations=30_000, exit_cost=35_000)

scenarios = [
    ("custom baseline", CUSTOM),
    ("purchased baseline", PURCHASED),
    ("purchased, subscription +20%", {**PURCHASED, "platform": 54_000 * 1.2}),
    ("custom, operations +25%", {**CUSTOM, "operations": 60_000 * 1.25}),
    ("purchased, support 45,000", {**PURCHASED, "operations": 45_000}),
]
for name, inputs in scenarios:
    print(f"{name:30} EUR {three_year_total(**inputs):>9,.0f}")

def commitment_saving(on_demand: float, discount: float, committed_hours: float,
                      used_hours: float) -> float:
    """Positive when the commitment beats paying on demand for the hours used."""
    committed_cost = committed_hours * on_demand * (1 - discount)
    return used_hours * on_demand - committed_cost

hours = 5 * 730 * 12  # the five steady instances for a year
for used in (1.0, 0.7, 0.5):
    saving = commitment_saving(0.10, 0.30, hours, used * hours)
    print(f"commitment used {used:.0%}: saving EUR {saving:,.2f} a year")
~~~

Expected output:

~~~text
custom baseline                EUR   427,000
purchased baseline             EUR   387,000
purchased, subscription +20%   EUR   419,400
custom, operations +25%        EUR   472,000
purchased, support 45,000      EUR   432,000
commitment used 100%: saving EUR 1,314.00 a year
commitment used 70%: saving EUR 0.00 a year
commitment used 50%: saving EUR -876.00 a year
~~~

### Change and extend

- Add a third option that keeps the current portal and improves only the integration. Estimate its one-time and recurring costs, label every invented value and name the evidence that would replace it.
- List the non-financial requirements: access control, data export, support, integration behaviour and user experience. Separate mandatory requirements from weighted preferences, and exclude any option that fails a mandatory one.
- Write a one-page decision memo with the recommendation, the assumptions that drive it, two alternatives, the main risks, a review trigger and a phased plan.

### Reflection

Which uncertainty is worth paying to investigate? Which decision can wait without harming the first release?

## Lab 9 Order saga and uncertain payment

**Goal.** Test an order state machine in which an unknown payment is never treated as a rejection, compensation failures stay visible, and terminal states ignore late callbacks.

**Prerequisites.** Chapter 22. **Estimated time.** Four hours.

### Steps

1. Read Listing 9.1. `confirmed`, `rejected` and `cancelled` are terminal: once an order reaches one, a provider report is recorded and changes nothing.
2. Save Listings 9.1 and 9.2 in one file and run it.
3. Follow scenario C closely. The reservation expires, the authorisation arrives late, the first void fails and the second succeeds. A delayed duplicate "authorised" callback then arrives and is ignored, so the cancelled order stays cancelled and its stock stays available.
4. In your own copy, remove the terminal check at the start of `payment_report` and run it again. The duplicate callback in scenario A now pushes a confirmed order into compensation, and the assertion fails. Restore the check.

Listing 9.1 defines the order and its transitions.

~~~python
"""Lab 9: an order saga with explicit compensation (in memory only)."""
from dataclasses import dataclass, field

TERMINAL = {"confirmed", "rejected", "cancelled"}

@dataclass
class Order:
    stock: int = 1
    reservation: str = "none"   # none, active, committed, released
    payment: str = "none"       # none, unknown, authorised, rejected, voided
    state: str = "received"
    notes: list[str] = field(default_factory=list)

    def reserve(self) -> None:
        if self.reservation == "active":
            return                                   # repeated request
        if self.reservation != "none" or self.stock < 1:
            raise ValueError("cannot reserve")
        self.stock -= 1
        self.reservation, self.state = "active", "payment_pending"

    def release(self) -> None:
        if self.reservation == "active":             # stock returns only once
            self.stock, self.reservation = self.stock + 1, "released"

    def payment_report(self, outcome: str) -> None:
        if self.state in TERMINAL:                   # late or repeated report
            self.notes.append(f"ignored '{outcome}' in {self.state}")
            return
        if self.payment in {"authorised", "rejected"} and outcome != self.payment:
            raise ValueError("conflicting provider outcomes")
        self.payment = outcome
        if outcome == "authorised" and self.reservation == "active":
            self.reservation, self.state = "committed", "confirmed"
        elif outcome == "authorised":                # stock no longer held
            self.state = "compensation_pending"
        elif outcome == "rejected":
            self.release()
            self.state = "rejected"

    def void(self, provider_ok: bool) -> None:
        if self.state != "compensation_pending":
            raise ValueError("nothing to compensate")
        if provider_ok:                              # otherwise retry later
            self.payment, self.state = "voided", "cancelled"
~~~

Listing 9.2 runs three scenarios.

~~~python
a = Order()
a.reserve()
a.payment_report("unknown")
assert a.state == "payment_pending"           # unknown is never a rejection
a.payment_report("authorised")
a.payment_report("authorised")                # the provider repeats its callback
assert (a.state, a.stock) == ("confirmed", 0)
print(f"A: unknown, then authorised twice -> {a.state}, stock={a.stock}")

b = Order()
b.reserve()
b.payment_report("rejected")
b.payment_report("rejected")
assert (b.state, b.stock) == ("rejected", 1)  # stock released exactly once
print(f"B: rejected twice -> {b.state}, stock={b.stock}")

c = Order()
c.reserve()
c.release()                                   # the reservation expires first
c.payment_report("authorised")                # money held, stock already freed
c.void(provider_ok=False)
assert c.state == "compensation_pending"      # failure stays visible
c.void(provider_ok=True)
c.payment_report("authorised")                # late duplicate after the void
assert (c.state, c.payment, c.stock) == ("cancelled", "voided", 1)
print(f"C: expired, void failed then succeeded -> {c.state}, stock={c.stock}")
print(f"C: {c.notes[-1]}")
~~~

Expected output:

~~~text
A: unknown, then authorised twice -> confirmed, stock=0
B: rejected twice -> rejected, stock=1
C: expired, void failed then succeeded -> cancelled, stock=1
C: ignored 'authorised' in cancelled
~~~

The model keeps state in memory and has no crash durability. A real design stores each transition in a transaction, with provider idempotency and reconciliation.

### Change and extend

- Add an explicit `expire` method that refuses to release a reservation that is already `committed`. Test both orders of "expire" and "authorised".
- Add a `rejected` report that arrives after a confirmed order and decide how it should be raised for investigation.
- Draw a sequence that shows where a real process could crash between the provider's success and the local record, and explain how reconciliation recovers.

### Reflection

What should the customer see in each state of scenario C, and who owns an order stuck in `compensation_pending`?

## Lab 10 Late events and corrected analytical totals

**Goal.** Deduplicate events by identity and version, assign them by event day, and publish corrected totals.

**Prerequisites.** Chapter 23. **Estimated time.** Three hours.

### Steps

1. Read Listing 10.1. Amounts are integer cents, and each event has an explicit source version. The function uses only rows ingested up to a cut-off day, which simulates what was known at each publication. Every row arrives at most two days after its event day, so all of them fall within Chapter 23's allowed lateness.
2. Save Listings 10.1 and 10.2 in one file and run it.
3. Compare the naive sum with the published totals, and follow how day 1 changes when the late event arrives.

Listing 10.1 materialises totals per event day.

~~~python
"""Lab 10: deduplicate by event and version, assign by event day.

Amounts are integer cents. Ingest day is when the platform received the row.
"""
from collections import defaultdict

EVENTS = [
    dict(id="e1", version=1, event_day=1, ingest_day=1, cents=10_000),
    dict(id="e1", version=1, event_day=1, ingest_day=1, cents=10_000),  # repeat
    dict(id="e3", version=1, event_day=2, ingest_day=2, cents=7_500),
    dict(id="e2", version=1, event_day=1, ingest_day=3, cents=5_000),   # late
    dict(id="e3", version=2, event_day=2, ingest_day=4, cents=7_000),   # correction
]

def materialise(events: list[dict], cutoff: int) -> dict[int, int]:
    """Totals per event day using rows ingested up to the cutoff day."""
    latest: dict[str, dict] = {}
    seen: dict[tuple, tuple] = {}
    for e in events:
        if e["ingest_day"] > cutoff:
            continue
        identity, content = (e["id"], e["version"]), (e["event_day"], e["cents"])
        if seen.setdefault(identity, content) != content:
            raise ValueError(f"conflicting content for {identity}")
        if e["id"] not in latest or e["version"] > latest[e["id"]]["version"]:
            latest[e["id"]] = e
    totals: dict[int, int] = defaultdict(int)
    for e in latest.values():
        totals[e["event_day"]] += e["cents"]
    return dict(totals)
~~~

Listing 10.2 prints three publications and tests a conflicting duplicate.

~~~python
def euros(cents: int) -> str:
    return f"{cents / 100:.2f}"

naive = sum(e["cents"] for e in EVENTS[:4])
print(f"naive sum of arriving rows before the correction: {euros(naive)}")
for cutoff in (1, 3, 4):
    totals = materialise(EVENTS, cutoff)
    days = ", ".join(f"day {d}: {euros(c)}" for d, c in sorted(totals.items()))
    print(f"published after ingest day {cutoff}: {days}; "
          f"total {euros(sum(totals.values()))}")

conflict = {**EVENTS[0], "cents": 9_999}      # same id and version, new content
try:
    materialise(EVENTS + [conflict], cutoff=4)
except ValueError as error:
    print(f"rejected: {error}")
assert materialise(EVENTS[::-1], 4) == materialise(EVENTS, 4)  # order-independent
~~~

Expected output:

~~~text
naive sum of arriving rows before the correction: 325.00
published after ingest day 1: day 1: 100.00; total 100.00
published after ingest day 3: day 1: 150.00, day 2: 75.00; total 225.00
published after ingest day 4: day 1: 150.00, day 2: 70.00; total 220.00
rejected: conflicting content for ('e1', 1)
~~~

The source contract here guarantees a version number per event. Explain what rule you would need for a source without one.

### Change and extend

- Add a deletion marker with an explicit business meaning. Decide whether it removes a fact, reverses a measure or triggers a privacy action, and update the function and checks.
- Add a publication record with a revision number and a correction reason for each run.
- Enforce the allowed-lateness rule: route any row with ingest day − event day > 2 to an exceptions list instead of the totals, and add a row that tests it.

### Reflection

How would you explain the change in the day-1 total to an operations manager who saw the first figure?

## Lab 11 Migration reconciliation and the false comfort of counts

**Goal.** Build a cutover gate that checks keys, values, relationships and change position, rather than row counts alone.

**Prerequisites.** Chapter 24. **Estimated time.** Three hours.

### Steps

1. Read Listing 11.1. Source and target each hold three orders, but the target has one missing order, one extra order and one changed amount. One order line points to an order that does not exist, and the target has applied two fewer changes than the source.
2. Run the listing. The counts match and the gate still stops the cutover for five reasons.
3. Note that the repaired data passes.

Listing 11.1 defines the data and the gate.

~~~python
"""Lab 11: a cutover gate that checks keys, values, links and position."""
SOURCE = {"o1": 10_000, "o2": 20_000, "o3": 30_000}   # order ID -> cents
TARGET = {"o1": 10_000, "o2": 21_000, "o4": 30_000}
TARGET_LINES = {"l1": "o1", "l2": "o2", "l3": "o9"}   # line ID -> order ID
SOURCE_POSITION, TARGET_APPLIED = 1_042, 1_040        # change-log positions

def compare(source: dict, target: dict) -> dict[str, list[str]]:
    shared = source.keys() & target.keys()
    return {"missing": sorted(source.keys() - target.keys()),
            "extra": sorted(target.keys() - source.keys()),
            "changed": sorted(k for k in shared if source[k] != target[k])}

def gate(source: dict, target: dict, lines: dict, source_position: int,
         applied_position: int) -> list[str]:
    """Return the reasons to stop; an empty list means the gate passes."""
    problems = [f"{kind} orders: {keys}"
                for kind, keys in compare(source, target).items() if keys]
    orphans = sorted(line for line, order in lines.items() if order not in target)
    if orphans:
        problems.append(f"lines without an order: {orphans}")
    if applied_position < source_position:
        lag = source_position - applied_position
        problems.append(f"target is {lag} changes behind the source")
    return problems

print(f"row counts: source={len(SOURCE)} target={len(TARGET)}")
for problem in gate(SOURCE, TARGET, TARGET_LINES, SOURCE_POSITION, TARGET_APPLIED):
    print("stop:", problem)
repaired_lines = {"l1": "o1", "l2": "o2", "l3": "o3"}
after = gate(SOURCE, dict(SOURCE), repaired_lines, SOURCE_POSITION, SOURCE_POSITION)
assert after == []
print("after repair: gate passes")
~~~

Expected output:

~~~text
row counts: source=3 target=3
stop: missing orders: ['o3']
stop: extra orders: ['o4']
stop: changed orders: ['o2']
stop: lines without an order: ['l3']
stop: target is 2 changes behind the source
after repair: gate passes
~~~

The listing compares small in-memory dictionaries. A real gate also needs a consistent snapshot, evidence of production completeness and business acceptance.

### Change and extend

- Add a legitimately transformed field, such as amounts converted from cents to a decimal type, and write the approved comparison rule.
- Write a full cutover rule that combines this gate with the write fence, access tests and a timed rollback rehearsal, and set the latest safe decision point.

### Reflection

Which discrepancies would you allow the business owner to accept, and which must always stop the cutover?

## Lab 12 Architecture evaluation workshop

**Goal.** Evaluate one case architecture with a utility tree, a trace of each high-priority scenario and a bounded conclusion.

**Prerequisites.** Chapters 20 to 24. **Estimated time.** Five hours.

### Steps

1. Choose one case and freeze a version of its proposed architecture.
2. Identify three stakeholder concerns, two credible options and the mandatory constraints. Exclude any option that fails a mandatory constraint.
3. Build a utility tree with at least five leaf scenarios, rated by importance and difficulty.
4. For each high-priority scenario, trace the responsible components and failure paths, name a sensitivity point and propose the smallest useful experiment.
5. Review the design in two passes, or ask a peer to challenge it. In the second pass, introduce one change: a lower vendor quota, an unavailable region, a late source correction or a failed compensation. Keep the first-pass findings rather than rewriting them.
6. Conclude with proceed, proceed with conditions, investigate further, or reject. Tie each condition to an owner and to observable closure evidence, and check the argument against the Chapter 25 rubric.

Record the case, architecture version, date and reviewer at the top of the worksheet, then use this table. The first row is a worked example.

| Scenario | Importance, difficulty | Components on the path | Claim | Evidence | Finding, owner and closure |
| --- | --- | --- | --- | --- | --- |
| CRM down for 30 minutes | H, M | API, outbox, worker, CRM adapter | No accepted request lost | Outage rehearsal with reconciliation report | Open until rehearsal passes; integration lead |
| … | … | … | … | … | … |

For each option, also list its strengths, costs, sensitivity points, trade-offs, untested assumptions and the observations that would change the choice.

**Expected result.** A reviewer can tell apart checked facts, untested assumptions, contextual judgement and unresolved risks in your conclusion. The workshop follows the structure of the ATAM in miniature; a full evaluation involves more stakeholders and more time.

### Reflection

Which finding changed between the two passes, and what does that tell you about the sensitivity of the design?
