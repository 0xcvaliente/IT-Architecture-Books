Record = tuple[str, int, int, float]      # (request, version, day, hours to close)

def latest(records: list[Record]) -> dict[str, Record]:
    """Highest version of each request; a replayed copy changes nothing."""
    best: dict[str, Record] = {}
    for r in records:
        if r[0] not in best or r[1] > best[r[0]][1]:
            best[r[0]] = r
    return best

ledger: list[dict] = []                   # publications are appended, never edited

def publish(records: list[Record], day: int, reason: str) -> None:
    rows = [r for r in latest(records).values() if r[2] == day]
    inputs = sorted((r[0], r[1]) for r in rows)
    before = next((p for p in reversed(ledger) if p['day'] == day), None)
    if before and before['inputs'] == inputs:
        print(f'{reason}: inputs unchanged, no new publication')
        return
    mean = sum(r[3] for r in rows) / len(rows)
    entry = {'id': f'P{len(ledger) + 1}', 'day': day, 'mean': mean,
             'inputs': inputs, 'supersedes': before['id'] if before else None}
    ledger.append(entry)
    note = f", supersedes {entry['supersedes']}" if before else ''
    print(f"{entry['id']} day {day}: mean {mean:.1f} h over {len(rows)} "
          f"requests{note} ({reason})")

feed = [('r1', 1, 1, 4.0), ('r2', 1, 1, 10.0)]
publish(feed, 1, 'first run')
feed.append(('r3', 1, 1, 1.0))            # a day-1 closure that arrives late
publish(feed, 1, 'late arrival of r3')
feed.append(('r1', 1, 1, 4.0))            # the source replays r1
publish(feed, 1, 'replay of r1')
feed.append(('r2', 2, 1, 16.0))           # the source corrects r2's start time
publish(feed, 1, 'correction of r2')
first, last = ledger[0], ledger[-1]
print(f"{first['id']} and {last['id']} both show {first['mean']:.1f} h:")
print(f"  {first['id']} used {first['inputs']}")
print(f"  {last['id']} used {last['inputs']}")
