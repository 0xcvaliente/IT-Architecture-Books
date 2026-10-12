"""Supplier comparison: apply the mandatory condition first, then weighted scores."""

SUPPLIERS = {  # name: (passes the export test, scores for fit, operability, cost)
    'A': (True, (4, 3, 4)),
    'B': (True, (3, 5, 3)),
    'C': (False, (5, 4, 5)),
}

def ranking(weights: tuple[float, float, float]) -> list[tuple[str, float]]:
    assert abs(sum(weights) - 1) < 1e-9, 'weights must sum to 1'
    totals = {name: sum(w * s for w, s in zip(weights, scores))
              for name, (eligible, scores) in SUPPLIERS.items() if eligible}
    return sorted(totals.items(), key=lambda item: -item[1])

for weights in [(0.40, 0.35, 0.25), (0.50, 0.25, 0.25)]:
    print(weights, [(name, round(total, 2)) for name, total in ranking(weights)])

for w in [0.30, 1 / 3, 0.36]:          # vary the operability weight
    rest = 1 - w
    result = ranking((rest * 0.6, w, rest * 0.4))
    print(f'operability {w:.3f}:', [(name, round(total, 3)) for name, total in result])
