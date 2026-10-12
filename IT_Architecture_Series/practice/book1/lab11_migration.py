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
