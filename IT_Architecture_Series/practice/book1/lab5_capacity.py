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
