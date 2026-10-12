"""Decision tree: expand now or run a pilot first (EUR millions, one valuation date)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from svgkit import ACCENT, ACCENT_SURFACE, INK, MUTED, SURFACE, Svg

W, H = 880, 600
s = Svg(W, H, 'Expand now or run a pilot first',
        'A decision square chooses between expanding now and running a pilot costing 0.05. '
        'Expanding now leads to a chance node: high adoption with probability 0.5 gives +1.0, '
        'low adoption gives -0.6, an expected value of 0.20. The pilot leads to a chance node: '
        'a favourable result with probability 0.5 is followed by a decision to expand, worth '
        '0.68; an unfavourable result is followed by a decision not to expand, worth 0. The '
        'pilot policy is worth 0.29 after its cost.')

def square(cx, cy, label=None):
    s.rect(cx - 16, cy - 16, 32, 32, fill=SURFACE, stroke=INK, sw=2, rx=2)

def circle(cx, cy):
    s.circle(cx, cy, 16, fill=SURFACE, stroke=INK, sw=2)

def branch(pts, dashed=False, label=None, lx=None, ly=None):
    d = '7 5' if dashed else None
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        s.line(x1, y1, x2, y2, sw=2, dash=d)
    if label:
        s.text(lx, ly, label, size=14)

def leaf(x, y, text, value, chosen=False):
    s.text(x, y + 5, text, size=14, weight='bold' if chosen else 'normal',
           fill=INK if chosen else MUTED)
    s.text(840, y + 5, value, size=14, weight='bold' if chosen else 'normal', anchor='end',
           fill=INK if chosen else MUTED)

# root decision
square(40, 290)
branch([(56, 290), (90, 290), (90, 110), (284, 110)], label='Expand now', lx=104, ly=100)
branch([(56, 290), (90, 290), (90, 420), (284, 420)], label='Run pilot (cost 0.05)', lx=104, ly=410)
s.text(48, 336, 'Decide', size=14, weight='bold', anchor='middle')
# expand now: chance node
circle(300, 110)
s.text(250, 148, 'EV 0.20', size=14, anchor='middle')
branch([(316, 110), (340, 110), (340, 60), (560, 60)], True, 'High adoption, p = 0.5', 354, 50)
branch([(316, 110), (340, 110), (340, 170), (560, 170)], True, 'Low adoption, p = 0.5', 354, 160)
leaf(580, 60, 'Expansion succeeds', '+1.0'); leaf(580, 170, 'Expansion struggles', '−0.6')
# pilot: chance node then decisions
circle(300, 420)
s.text(230, 458, 'EV 0.34 − 0.05 = 0.29', size=14, anchor='middle')
branch([(316, 420), (340, 420), (340, 330), (524, 330)], True, 'Favourable, p = 0.5', 350, 320)
branch([(316, 420), (340, 420), (340, 510), (524, 510)], True, 'Unfavourable, p = 0.5', 350, 500)
square(540, 330); square(540, 510)
branch([(556, 330), (580, 330), (580, 295), (610, 295)])
branch([(556, 330), (580, 330), (580, 365), (610, 365)])
leaf(620, 295, 'Expand, EV 0.68', '0.68', True); leaf(620, 365, 'Do not expand', '0')
branch([(556, 510), (580, 510), (580, 475), (610, 475)])
branch([(556, 510), (580, 510), (580, 545), (610, 545)])
leaf(620, 475, 'Expand, EV −0.28', '−0.28'); leaf(620, 545, 'Do not expand', '0', True)
# legend
LY = 585
s.rect(20, LY - 12, 16, 16, fill=SURFACE, stroke=INK, sw=2, rx=2)
s.text(44, LY + 1, 'Decision', size=13, fill=MUTED)
s.circle(132, LY - 4, 8, fill=SURFACE, stroke=INK, sw=2)
s.text(146, LY + 1, 'Chance', size=13, fill=MUTED)
s.line(220, LY - 4, 260, LY - 4, sw=2); s.text(268, LY + 1, 'Choice', size=13, fill=MUTED)
s.line(340, LY - 4, 380, LY - 4, sw=2, dash='7 5'); s.text(388, LY + 1, 'Chance outcome', size=13, fill=MUTED)
s.text(520, LY + 1, 'Bold: the branch chosen at each decision', size=13, fill=MUTED)
s.save('pilot_decision')
