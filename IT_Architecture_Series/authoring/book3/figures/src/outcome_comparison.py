"""Difference-in-differences: pilot 10% to 6%, comparison 8% to 7%, assumed path 10% to 9%."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from svgkit import ACCENT, INK, MUTED, Svg

W, H = 940, 510
L, R, T, B = 130, 640, 40, 460            # plot box; y axis 5% (bottom) to 11% (top)
def y(v): return B - (v - 5) / 6 * (B - T)
XB, XA = L + 70, R - 70                   # x of Before and After
s = Svg(W, H, 'Difference-in-differences for the reconciliation pilot',
        'Error rate in percent before and after the pilot. The participating division falls '
        'from 10 to 6, the comparison division from 8 to 7. A dashed line shows the assumed '
        'path of the participating division without the pilot, from 10 to 9. The 3 point '
        'gap at the end is the difference-in-differences.')
for v in range(5, 12):
    s.line(L, y(v), R, y(v), stroke='#d9d9d9', sw=1)
    s.text(L - 14, y(v) + 5, f'{v}%', size=14, anchor='end', fill=MUTED)
s.line(L, T, L, B, stroke=INK, sw=1.5)
s.line(L, B, R, B, stroke=INK, sw=1.5)
s.text(XB, B + 30, 'Before', size=16, anchor='middle')
s.text(XA, B + 30, 'After', size=16, anchor='middle')
s.text(L - 70, (T + B) / 2, 'Error rate', size=16, anchor='middle', rotate=-90)
# assumed untreated path, comparison, pilot
s.line(XB, y(10), XA, y(9), stroke=MUTED, sw=2.5, dash='9 7')
s.line(XB, y(8), XA, y(7), stroke=INK, sw=3)
for x, v in [(XB, 8), (XA, 7)]:
    s.rect(x - 7, y(v) - 7, 14, 14, fill=INK, stroke=INK, sw=1, rx=1)
s.line(XB, y(10), XA, y(6), stroke=ACCENT, sw=3.5)
for x, v in [(XB, 10), (XA, 6)]:
    s.circle(x, y(v), 8, fill=ACCENT)
# 3 pp bracket
bx = XA + 28
s.line(bx, y(9), bx, y(6), stroke=INK, sw=2)
s.line(bx - 8, y(9), bx, y(9), stroke=INK, sw=2)
s.line(bx - 8, y(6), bx, y(6), stroke=INK, sw=2)
s.text(bx + 12, (y(9) + y(6)) / 2 + 5, '3 points', size=15, weight='bold')
# legend
LX, LY = 680, 90
s.line(LX, LY, LX + 46, LY, stroke=ACCENT, sw=3.5); s.circle(LX + 23, LY, 7, fill=ACCENT)
s.text(LX + 60, LY + 5, 'Participating division:\n10% to 6%', size=15, lead=19)
s.line(LX, LY + 70, LX + 46, LY + 70, stroke=INK, sw=3)
s.rect(LX + 16, LY + 63, 14, 14, fill=INK, stroke=INK, sw=1, rx=1)
s.text(LX + 60, LY + 75, 'Comparison division:\n8% to 7%', size=15, lead=19)
s.line(LX, LY + 140, LX + 46, LY + 140, stroke=MUTED, sw=2.5, dash='9 7')
s.text(LX + 60, LY + 145, 'Assumed path without\nthe pilot: 10% to 9%', size=15, lead=19)
s.save('outcome_comparison')
