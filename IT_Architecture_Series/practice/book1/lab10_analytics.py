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
