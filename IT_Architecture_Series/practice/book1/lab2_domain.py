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
