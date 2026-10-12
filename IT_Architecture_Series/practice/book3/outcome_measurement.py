"""Pooled, stratified and standardised error rates, and a difference-in-differences."""
from fractions import Fraction

BEFORE = {'A': (10, 100), 'B': (45, 900)}      # unit: (errors, requests)
AFTER = {'A': (72, 900), 'B': (4, 100)}

def pct(x: Fraction) -> str:
    return f'{float(x) * 100:.1f}%'

def rates(data: dict[str, tuple[int, int]]) -> dict[str, Fraction]:
    return {unit: Fraction(errors, n) for unit, (errors, n) in data.items()}

def pooled(data: dict[str, tuple[int, int]]) -> Fraction:
    return Fraction(sum(e for e, _ in data.values()), sum(n for _, n in data.values()))

for label, data in [('Before', BEFORE), ('After', AFTER)]:
    by_unit = ', '.join(f'{unit} {pct(r)}' for unit, r in rates(data).items())
    print(f'{label}: {by_unit}; pooled {pct(pooled(data))}')

total = sum(n for _, n in BEFORE.values())
mix = {unit: Fraction(n, total) for unit, (_, n) in BEFORE.items()}  # earlier mix
standardised = sum(mix[unit] * r for unit, r in rates(AFTER).items())
print('After, standardised to the earlier mix:', pct(standardised))

pilot, comparison = (10, 6), (8, 7)            # error rate (%) before and after
change_p, change_c = pilot[1] - pilot[0], comparison[1] - comparison[0]
print(f'Pilot {change_p} pp, comparison {change_c} pp, '
      f'difference-in-differences {change_p - change_c} pp')
