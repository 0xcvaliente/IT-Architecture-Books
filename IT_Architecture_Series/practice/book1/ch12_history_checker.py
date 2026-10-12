from dataclasses import dataclass
from itertools import permutations

@dataclass(frozen=True)
class Op:
    name: str
    kind: str    # "write" or "read"
    value: int   # the value written, or the value the read returned
    start: int   # time of invocation
    end: int     # time of response

def linearizations(history: list[Op], initial: int = 0) -> list[tuple[str, ...]]:
    """Return every sequential order that explains a completed register history."""
    before = {(a.name, b.name) for a in history for b in history if a.end < b.start}
    valid = []
    for order in permutations(history):
        position = {op.name: i for i, op in enumerate(order)}
        if any(position[a] > position[b] for a, b in before):
            continue  # this order contradicts real-time precedence
        state, legal = initial, True
        for op in order:
            if op.kind == "write":
                state = op.value
            elif op.value != state:
                legal = False
                break
        if legal:
            valid.append(tuple(op.name for op in order))
    return valid

W = Op("W", "write", 1, start=1, end=3)
histories = {
    "read after completed write": [W, Op("R", "read", 0, start=4, end=5)],
    "read overlaps the write": [W, Op("R", "read", 0, start=2, end=5)],
    "later read sees new value": [W, Op("R", "read", 1, start=4, end=5)],
}
for label, history in histories.items():
    print(f"{label}: {linearizations(history)}")
