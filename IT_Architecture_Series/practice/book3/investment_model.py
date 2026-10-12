"""NPV, IRR and payback for the Helios customer-handoff investment (EUR)."""

def npv(rate: float, investment: float, flows: list[float]) -> float:
    """Investment at time 0; flows[t - 1] arrives at the end of year t."""
    return -investment + sum(cf / (1 + rate) ** t for t, cf in enumerate(flows, 1))

def irr(investment: float, flows: list[float]) -> float:
    lo, hi = 0.0, 1.0                      # bisection: NPV falls as the rate rises
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if npv(mid, investment, flows) > 0 else (lo, mid)
    return mid

def payback(investment: float, flows: list[float], rate: float = 0.0,
            even: bool = False) -> float:
    """Cash arrives at year ends, or accrues evenly through each year if even=True."""
    left = investment
    for t, cf in enumerate(flows, 1):
        pv = cf / (1 + rate) ** t
        if pv >= left:
            return t - 1 + left / pv if even else t
        left -= pv
    return float('inf')

cost, base = 2_500_000, [1_200_000] * 3
scenarios = {  # name: (rate, investment at time 0, flows at the end of years 1, 2, ...)
    'Base case, 8%': (0.08, cost, base),
    'Lower rate, 4%': (0.04, cost, base),
    'Higher rate, 12%': (0.12, cost, base),
    'Benefits 20% lower': (0.08, cost, [960_000] * 3),
    'Benefits one year later': (0.08, cost, [0] + base),
    'Cut: 0.6m deferred': (0.08, cost - 600_000, [-600_000] + base),
    'Cut: 0.6m removed': (0.08, cost - 600_000, [800_000] * 3),
}
for name, (rate, inv, flows) in scenarios.items():
    print(f'{name:<24} NPV EUR {npv(rate, inv, flows):>12,.0f}')
print(f'IRR {irr(cost, base):.2%}')
for even, timing in [(False, 'year-end cash:'), (True, 'even accrual:')]:
    print(f'Payback, {timing:<15} simple {payback(cost, base, 0, even):.2f}, '
          f'discounted {payback(cost, base, 0.08, even):.2f} years')
