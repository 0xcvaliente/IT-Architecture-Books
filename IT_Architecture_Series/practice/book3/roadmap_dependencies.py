"""Critical-path schedule for the Helios customer identity pilot (weeks)."""

TASKS = {  # name: (duration, predecessors), listed in dependency order
    'A': (4, []),          # agree identity semantics
    'B': (6, ['A']),       # implement shared identifiers
    'C': (3, ['A']),       # define integration contracts
    'D': (4, ['B', 'C']),  # pilot a customer handoff
    'E': (2, ['D']),       # assess results and decide rollout
}

def schedule(tasks: dict[str, tuple[int, list[str]]]) -> tuple[dict, dict, int]:
    early: dict[str, int] = {}                 # earliest finish (forward pass)
    for name, (dur, preds) in tasks.items():
        early[name] = max((early[p] for p in preds), default=0) + dur
    end = max(early.values())
    late: dict[str, int] = {}                  # latest finish (backward pass)
    for name in reversed(list(tasks)):
        succs = [s for s, (_, preds) in tasks.items() if name in preds]
        late[name] = min((late[s] - tasks[s][0] for s in succs), default=end)
    return early, late, end

early, late, end = schedule(TASKS)
for name, (dur, _) in TASKS.items():
    start, slack = early[name] - dur, late[name] - early[name]
    print(f'{name}: start {start:>2}  finish {early[name]:>2}  slack {slack}')
critical = [n for n in TASKS if late[n] == early[n]]
print('Completion:', end, 'weeks; critical path:', '-'.join(critical))

shared = dict(TASKS, C=(3, ['B']))             # one team must do B, then C
print('With one shared team for B and C:', schedule(shared)[2], 'weeks')
