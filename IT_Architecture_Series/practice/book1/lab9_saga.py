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
