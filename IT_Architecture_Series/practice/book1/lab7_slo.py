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
