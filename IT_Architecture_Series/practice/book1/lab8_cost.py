"""Lab 8: three-year cost comparison, sensitivity and commitment break-even."""

def three_year_total(initial: float, integration: float, platform: float,
                     operations: float, exit_cost: float, years: int = 3) -> float:
    """Undiscounted total: one-time costs plus yearly costs plus exit."""
    return initial + integration + years * (platform + operations) + exit_cost

CUSTOM = dict(initial=120_000, integration=35_000, platform=24_000,
              operations=60_000, exit_cost=20_000)
PURCHASED = dict(initial=45_000, integration=55_000, platform=54_000,
                 operations=30_000, exit_cost=35_000)

scenarios = [
    ("custom baseline", CUSTOM),
    ("purchased baseline", PURCHASED),
    ("purchased, subscription +20%", {**PURCHASED, "platform": 54_000 * 1.2}),
    ("custom, operations +25%", {**CUSTOM, "operations": 60_000 * 1.25}),
    ("purchased, support 45,000", {**PURCHASED, "operations": 45_000}),
]
for name, inputs in scenarios:
    print(f"{name:30} EUR {three_year_total(**inputs):>9,.0f}")

def commitment_saving(on_demand: float, discount: float, committed_hours: float,
                      used_hours: float) -> float:
    """Positive when the commitment beats paying on demand for the hours used."""
    committed_cost = committed_hours * on_demand * (1 - discount)
    return used_hours * on_demand - committed_cost

hours = 5 * 730 * 12  # the five steady instances for a year
for used in (1.0, 0.7, 0.5):
    saving = commitment_saving(0.10, 0.30, hours, used * hours)
    print(f"commitment used {used:.0%}: saving EUR {saving:,.2f} a year")
