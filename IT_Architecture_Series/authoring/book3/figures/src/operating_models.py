"""Ross, Weill and Robertson's four operating models, with Helios's intended move."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from svgkit import ACCENT, ACCENT_SURFACE, MUTED, SURFACE, Svg

W, H = 880, 600
L, T, S = 125, 20, 500          # plot left, top, side length of each half is S/2... full square S
s = Svg(W, H, 'Four operating models',
        'A two-by-two grid with business process standardisation on the horizontal axis and '
        'business process integration on the vertical axis. Coordination is high integration '
        'and low standardisation; Unification is high on both; Diversification is low on '
        'both; Replication is low integration and high standardisation. An arrow shows '
        'Helios moving from Diversification towards Coordination.')
QW, QH = 350, 240
quads = [  # x, y, name, text
    (L, T, 'Coordination', 'Units share customer, product or\nsupplier data; each keeps its\nown processes'),
    (L + QW, T, 'Unification', 'One business with standard\nprocesses and shared data'),
    (L, T + QH, 'Diversification', 'Independent units with few\nshared customers or data'),
    (L + QW, T + QH, 'Replication', 'Similar units run the same\nstandard processes; little\ndata is shared'),
]
for x, y, name, text in quads:
    focal = name == 'Coordination'
    s.rect(x, y, QW, QH, fill=ACCENT_SURFACE if focal else SURFACE,
           stroke=ACCENT if focal else MUTED, sw=3 if focal else 2, rx=0)
    s.text(x + QW / 2, y + 48, name, size=21, weight='bold', anchor='middle')
    s.text(x + QW / 2, y + 82, text, size=14, anchor='middle', fill=MUTED, lead=19)
# axes
s.arrow(L, T + 2 * QH + 40, L + 2 * QW + 10, T + 2 * QH + 40, sw=2)
s.text(L + QW, T + 2 * QH + 72, 'Business process standardisation', size=16,
       anchor='middle')
s.text(L, T + 2 * QH + 62, 'Low', size=14, fill=MUTED)
s.text(L + 2 * QW - 40, T + 2 * QH + 62, 'High', size=14, fill=MUTED)
s.arrow(L - 40, T + 2 * QH, L - 40, T - 10, sw=2)
s.text(L - 62, T + QH, 'Business process integration', size=16, anchor='middle', rotate=-90)
s.text(L - 88, T + 2 * QH - 4, 'Low', size=14, fill=MUTED)
s.text(L - 92, T + 16, 'High', size=14, fill=MUTED)
# Helios today -> year-one direction, kept left of the quadrant text
hx, hy = L + 45, T + QH + 200
tx, ty = L + 45, T + QH - 50
s.circle(hx, hy, 9, fill=MUTED)
s.text(hx + 20, hy + 6, 'Helios today', size=15, weight='bold')
s.arrow(hx, hy - 12, tx, ty + 12, stroke=ACCENT, sw=3)
s.circle(tx, ty, 9, fill=ACCENT)
s.text(tx + 20, ty + 6, 'Helios year-one target', size=15, weight='bold')
s.save('operating_models')
