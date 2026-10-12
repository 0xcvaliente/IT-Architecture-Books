import math

def drain_seconds(backlog: int, arrivals: float, successes: float) -> float:
    """Time to clear a backlog when work arrives and completes at constant rates."""
    if successes <= arrivals:
        return math.inf                  # the backlog never shrinks
    return backlog / (successes - arrivals)

def zero_failure_bound(trials: int, confidence: float = 0.95) -> float:
    """Upper bound on the failure probability after `trials` runs with no failure."""
    return 1 - (1 - confidence) ** (1 / trials)

def trials_needed(target: float, confidence: float = 0.95) -> int:
    """Smallest number of failure-free trials whose bound falls below `target`."""
    return math.ceil(math.log(1 - confidence) / math.log(1 - target))

for backlog, arrivals, successes in [(9000, 5, 10), (9000, 5, 15), (9000, 5, 5)]:
    seconds = drain_seconds(backlog, arrivals, successes)
    shown = 'never' if math.isinf(seconds) else f'{seconds:,.0f} s'
    print(f'backlog {backlog:,}, arrivals {arrivals}/s, '
          f'successes {successes}/s: {shown}')
print(f'bound after 400 clean crash trials: {zero_failure_bound(400):.2%}')
print(f'bound if they behave as 8 independent batches: {zero_failure_bound(8):.1%}')
print(f'clean trials needed for a bound below 0.5%: {trials_needed(0.005):,}')
