"""TIME quadrant (Tolerate, Invest, Migrate, Eliminate) for six Helios applications."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from svgkit import ACCENT, ACCENT_SURFACE, INK, MUTED, SURFACE, Svg

# application: (technical fitness, business value), both on 1-5 scales; label offset
APPS = {
    'ERP Core': (3.9, 4.2, (16, 6)),
    'Identity Platform': (3.4, 3.8, (16, 6)),
    'CRM Central': (3.7, 3.3, (16, 6)),
    'CRM North': (2.0, 3.5, (16, 6)),
    'Legacy Orders': (1.4, 4.0, (16, 6)),
    'Analytics Warehouse': (3.25, 2.5, (16, 6)),
}
W, H = 880, 640
L, T, SIDE = 120, 20, 500          # plot area: x 150-710 (1..5), y 30-590 (5..1)
def px(v): return L + (v - 1) / 4 * SIDE
def py(v): return T + (5 - v) / 4 * SIDE
s = Svg(W, H, 'TIME quadrant for six Helios applications',
        'Technical fitness on the horizontal axis and business value on the vertical axis, '
        'each from 1 to 5, split at 3. Migrate is high value and low fitness, Invest high on '
        'both, Eliminate low on both, Tolerate low value and high fitness. CRM North and '
        'Legacy Orders fall in Migrate; ERP Core, Identity Platform and CRM Central in '
        'Invest; Analytics Warehouse in Tolerate.')
half = SIDE / 2
quads = [(L, T, 'Migrate', 'Valuable but technically weak:\nmove to a better platform'),
         (L + half, T, 'Invest', 'Valuable and sound:\nextend and improve'),
         (L, T + half, 'Eliminate', 'Low value and weak:\nretire when safe'),
         (L + half, T + half, 'Tolerate', 'Sound but low value:\nrun at minimum cost')]
for x, y, name, text in quads:
    s.rect(x, y, half, half, fill=SURFACE, stroke=MUTED, sw=2, rx=0)
    top = y == T
    ny = y + 36 if top else y + half - 62
    s.text(x + half / 2, ny, name, size=20, weight='bold', anchor='middle')
    s.text(x + half / 2, ny + 26, text, size=14, anchor='middle', fill=MUTED, lead=17)
for name, (tf, bv, (dx, dy)) in APPS.items():
    x, y = px(tf), py(bv)
    s.circle(x, y, 8, fill=ACCENT, stroke='#ffffff', sw=2)
    s.text(x + dx, y + dy, name, size=14, weight='bold', fill=INK)
# axes with ticks 1..5
s.arrow(L, T + SIDE + 30, L + SIDE + 15, T + SIDE + 30, sw=2)
s.arrow(L - 30, T + SIDE, L - 30, T - 12, sw=2)
for v in range(1, 6):
    s.line(px(v), T + SIDE + 24, px(v), T + SIDE + 36, sw=2)
    s.text(px(v), T + SIDE + 56, str(v), size=14, anchor='middle', fill=MUTED)
    s.line(L - 36, py(v), L - 24, py(v), sw=2)
    s.text(L - 44, py(v) + 5, str(v), size=14, anchor='end', fill=MUTED)
s.text(L + SIDE / 2, T + SIDE + 82, 'Technical fitness', size=16, anchor='middle')
s.text(L - 70, T + SIDE / 2, 'Business value', size=16, anchor='middle', rotate=-90)
# note on the right
s.text(L + SIDE + 30, T + 30, 'How to read it', size=16, weight='bold')
s.text(L + SIDE + 30, T + 60,
       'Each point is one\napplication, scored by\nits owners and the\narchitecture team.\n\n'
       'The quadrant suggests\na disposition. Cost,\ndependencies and exit\nterms decide it.',
       size=14, fill=MUTED, lead=19)
s.save('time_quadrant')
