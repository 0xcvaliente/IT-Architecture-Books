"""NPV sensitivity of the EUR 2.5m customer-handoff investment (values from the listing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from svgkit import ACCENT, INK, MUTED, Svg

ROWS = [('Lower rate, 4%', 830_109), ('Base case, 8%', 592_516), ('Higher rate, 12%', 382_198),
        ('Benefits one year later', 363_441), ('Benefits 20% lower', -25_987)]
W, H = 880, 440
ZERO, SCALE = 330, 0.55 / 1000
s = Svg(W, H, 'Sensitivity of net present value',
        'Horizontal bars show NPV in thousands of euros for five scenarios: 830 at 4%, 593 at '
        '8%, 382 at 12%, 363 with benefits one year later and minus 26 with 20% lower benefits.')
for i, (name, v) in enumerate(ROWS):
    y = 20 + i * 70
    s.text(245, y + 31, name, size=15, anchor='end')
    w = abs(v) * SCALE
    x = ZERO if v >= 0 else ZERO - w
    s.rect(round(x, 1), y + 8, round(w, 1), 36, fill=ACCENT if v >= 0 else MUTED,
           stroke='none', sw=0, rx=2)
    label = f'{v / 1000:,.0f}'.replace('-', '−')
    if v >= 0:
        s.text(round(ZERO + w + 8, 1), y + 32, label, size=15, weight='bold')
    else:
        s.text(round(ZERO + 8, 1), y + 32, label, size=15, weight='bold')
s.line(ZERO, 15, ZERO, 370, stroke=INK, sw=2)
for t in range(-100, 901, 100):
    x = ZERO + t * 1000 * SCALE
    s.line(x, 370, x, 380, stroke=INK, sw=1.5)
    s.text(x, 400, f'{t:,}'.replace('-', '−'), size=14, anchor='middle', fill=MUTED)
s.line(ZERO - 100 * 1000 * SCALE, 370, ZERO + 900 * 1000 * SCALE, 370, stroke=INK, sw=1.5)
s.text(ZERO + 400 * 1000 * SCALE, 430, 'Net present value, EUR thousands', size=15, anchor='middle')
s.save('investment')
