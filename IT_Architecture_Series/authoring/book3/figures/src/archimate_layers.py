"""Helios service-fulfilment view in ArchiMate 4, every relationship labelled."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from svgkit import ACCENT, ACCENT_SURFACE, INK, MUTED, SURFACE, PAPER, Svg

W, H = 880, 672
BW, BH = 140, 90
XS = [20, 255, 490, 725]
ROWS = {'b': 50, 'a': 285, 't': 525}
s = Svg(W, H, 'Helios service fulfilment in ArchiMate 4',
        'Business domain: the service coordinator role is assigned to the process Handle service '
        'request, which realises the service Field maintenance, which serves the customer. '
        'Application domain: CRM North realises the case management service and the customer '
        'link hub realises the customer lookup service; both services serve the process. '
        'Technology domain: the shared cloud platform node realises the container hosting '
        'service, which serves both application components.')
for label, y in [('BUSINESS DOMAIN', 12), ('APPLICATION DOMAIN', 247), ('TECHNOLOGY DOMAIN', 487)]:
    s.rect(8, y, W - 16, 140, fill='none', stroke=MUTED, sw=1.2, dash='4 4')
    s.text(18, y + 20, label, size=13, weight='bold', fill=MUTED)

def node(col, row, name, kind, focal=False):
    x, y = XS[col], ROWS[row]
    s.rect(x, y, BW, BH, fill=ACCENT_SURFACE if focal else SURFACE,
           stroke=ACCENT if focal else MUTED, sw=2.5 if focal else 1.5, rx=6)
    lines = name.split('\n')
    s.text(x + 10, y + 24, name, size=15, weight='bold', lead=18)
    s.text(x + 10, y + 24 + 18 * len(lines) + 4, kind, size=13, fill=MUTED, lead=15)

def chip(x, y, text, anchor='middle'):
    w = 8 + 7.6 * len(text)
    x0 = x - w / 2 if anchor == 'middle' else x
    s.rect(x0, y - 14, w, 19, fill=PAPER, stroke='none', sw=0, rx=3)
    s.text(x0 + 4, y, text, size=13, fill=INK)

from math import atan2, cos, sin

def head(x1, y1, x2, y2, kind):
    """Draw the ArchiMate end marker at (x2, y2) for a segment arriving from (x1, y1)."""
    a = atan2(y2 - y1, x2 - x1)
    L, Wd = 12, 6
    bx, by = x2 - L * cos(a), y2 - L * sin(a)
    p2 = (bx + Wd * sin(a), by - Wd * cos(a))
    p3 = (bx - Wd * sin(a), by + Wd * cos(a))
    if kind == 'realises':      # hollow triangle
        s.parts.append(f'<polygon points="{x2:.1f},{y2:.1f} {p2[0]:.1f},{p2[1]:.1f} '
                       f'{p3[0]:.1f},{p3[1]:.1f}" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>')
    elif kind == 'serves':      # open arrowhead
        s.line(x2, y2, *p2, stroke=INK, sw=2); s.line(x2, y2, *p3, stroke=INK, sw=2)
    else:                       # assignment: filled arrowhead
        s.parts.append(f'<polygon points="{x2:.1f},{y2:.1f} {p2[0]:.1f},{p2[1]:.1f} '
                       f'{p3[0]:.1f},{p3[1]:.1f}" fill="{INK}"/>')
    return bx, by

def rel(points, kind):
    dash = '2 4' if kind == 'realises' else None
    (x1, y1), (x2, y2) = points[-2], points[-1]
    ex, ey = head(x1, y1, x2, y2, kind) if kind == 'realises' else (x2, y2)
    pts = points[:-1] + [(ex, ey)]
    for (a1, b1), (a2, b2) in zip(pts, pts[1:]):
        s.line(a1, b1, a2, b2, stroke=INK, sw=2, dash=dash)
    if kind != 'realises':
        head(x1, y1, x2, y2, kind)
    if kind == 'assigned to':
        s.circle(points[0][0] + 4, points[0][1], 4, fill=INK)

def hedge(row, c1, c2, text):
    y = ROWS[row] + BH / 2
    if c2 > c1:
        x1, x2 = XS[c1] + BW, XS[c2]
    else:
        x1, x2 = XS[c1], XS[c2] + BW
    rel([(x1, y), (x2, y)], text)
    chip((x1 + x2) / 2, y - 8, text)

def path(points, text, at):
    rel(points, 'serves')
    chip(at[0], at[1], text, anchor='start')

node(0, 'b', 'Service\ncoordinator', 'Role')
node(1, 'b', 'Handle\nservice\nrequest', 'Process', focal=True)
node(2, 'b', 'Field\nmaintenance', 'Service')
node(3, 'b', 'Customer', 'Business actor')
node(0, 'a', 'CRM North', 'Application\ncomponent')
node(1, 'a', 'Case\nmanagement', 'Service')
node(2, 'a', 'Customer\nlookup', 'Service')
node(3, 'a', 'Customer\nlink hub', 'Application\ncomponent')
node(1, 't', 'Shared cloud\nplatform', 'Node')
node(2, 't', 'Container\nhosting', 'Service')
hedge('b', 0, 1, 'assigned to')
hedge('b', 1, 2, 'realises')
hedge('b', 2, 3, 'serves')
hedge('a', 0, 1, 'realises')
hedge('a', 3, 2, 'realises')
hedge('t', 1, 2, 'realises')
yb, ya, yt = ROWS['b'] + BH, ROWS['a'], ROWS['t']
path([(300, ya), (300, yb)], 'serves', (308, 205))
path([(560, ya), (560, 225), (370, 225), (370, yb)], 'serves', (450, 218))
path([(530, yt), (530, 470), (90, 470), (90, ya + BH)], 'serves', (98, 420))
path([(600, yt), (600, 470), (795, 470), (795, ya + BH)], 'serves', (720, 420))
LY = 656
s.text(18, LY, 'Notation:', size=13, weight='bold', fill=MUTED)
rel([(100, LY - 4), (150, LY - 4)], 'assigned to'); s.text(158, LY, 'assignment', size=13, fill=MUTED)
rel([(260, LY - 4), (310, LY - 4)], 'realises'); s.text(318, LY, 'realisation', size=13, fill=MUTED)
rel([(420, LY - 4), (470, LY - 4)], 'serves'); s.text(478, LY, 'serving', size=13, fill=MUTED)
s.save('archimate_layers')
