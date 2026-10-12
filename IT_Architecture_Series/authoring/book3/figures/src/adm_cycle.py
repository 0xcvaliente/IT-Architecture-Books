"""Generate figures/adm_cycle.svg: the TOGAF ADM phases around requirements management.

Run: python3 -I adm_cycle.py  (writes ../adm_cycle.svg), then
rsvg-convert -w 5268 -b white ../adm_cycle.svg -o ../adm_cycle.png
"""
from math import cos, sin, radians, atan2, degrees
from pathlib import Path

W, H = 880, 640
CX, CY, RX, RY = 448, 338, 300, 222
BW, BH = 206, 58
INK, MUTED, EDGE, SURF, ACC, ACC_S = '#000000', '#323232', '#323232', '#f3f3f3', '#276ef1', '#e8f0fe'
PHASES = [  # (angle in degrees, clockwise from top), label lines
    (-90, ['A. Architecture vision']),
    (-45, ['B. Business', 'architecture']),
    (0, ['C. Information systems', 'architectures']),
    (45, ['D. Technology', 'architecture']),
    (90, ['E. Opportunities', 'and solutions']),
    (135, ['F. Migration planning']),
    (180, ['G. Implementation', 'governance']),
    (225, ['H. Architecture', 'change management']),
]

def pt(a):
    return CX + RX * cos(radians(a)), CY + RY * sin(radians(a))

def box(x, y, w, h, lines, fill=SURF, stroke=MUTED, bold_first=False, size=15):
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="8" '
           f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>']
    n = len(lines)
    for i, s in enumerate(lines):
        ty = y + h / 2 + (i - (n - 1) / 2) * (size + 4) + size * 0.35
        weight = ' font-weight="bold"' if (bold_first and i == 0) else ''
        out.append(f'<text x="{x + w / 2:.1f}" y="{ty:.1f}" font-size="{size}"{weight} '
                   f'text-anchor="middle" fill="{INK}">{s}</text>')
    return out

def arrowhead(x, y, ang, size=13):
    a = radians(ang)
    p1 = (x, y)
    p2 = (x - size * cos(a) + size * 0.5 * sin(a), y - size * sin(a) - size * 0.5 * cos(a))
    p3 = (x - size * cos(a) - size * 0.5 * sin(a), y - size * sin(a) + size * 0.5 * cos(a))
    return (f'<polygon points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} '
            f'{p3[0]:.1f},{p3[1]:.1f}" fill="{EDGE}"/>')

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d" font-family="DejaVu Sans">',
       '<title id="t">The TOGAF Architecture Development Method cycle</title>',
       '<desc id="d">Phases A to H run clockwise around requirements management. '
       'A preliminary phase precedes the cycle. Every phase exchanges requirements with '
       'the centre.</desc>',
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
# cycle path
svg.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" '
           f'stroke="{EDGE}" stroke-width="2.5"/>')
# arrowheads midway between phases, pointing clockwise
def inside_box(px_, py_, pad=6):
    for b, _ in PHASES:
        bx, by = pt(b)
        if abs(px_ - bx) <= BW / 2 + pad and abs(py_ - by) <= BH / 2 + pad:
            return True
    return False
for k in range(8):
    a0 = -90 + 45 * k
    vis = [a0 + i * 0.25 for i in range(181) if not inside_box(*pt(a0 + i * 0.25))]
    a = (min(vis) + max(vis)) / 2 + 2      # middle of the visible arc, nudged clockwise
    x, y = pt(a)
    tx, ty = -RX * sin(radians(a)), RY * cos(radians(a))
    svg.append(arrowhead(x, y, degrees(atan2(ty, tx))))
# dashed links from centre box to each phase box
RW, RH = 200, 80
for a, _ in PHASES:
    x, y = pt(a)
    # start at the centre-box edge, end at the phase-box edge
    dx, dy = x - CX, y - CY
    def clip(cx, cy, hw, hh, dx, dy):
        t = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
        return cx + dx * t, cy + dy * t
    sx, sy = clip(CX, CY, RW / 2 + 4, RH / 2 + 4, dx, dy)
    ex, ey = clip(x, y, BW / 2 + 4, BH / 2 + 4, -dx, -dy)
    svg.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
               f'stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="6 5"/>')
# phase boxes
for a, lines in PHASES:
    x, y = pt(a)
    svg += box(x - BW / 2, y - BH / 2, BW, BH, lines)
# centre: requirements management (focal)
svg += box(CX - RW / 2, CY - RH / 2, RW, RH, ['Requirements', 'management'],
           fill=ACC_S, stroke=ACC, bold_first=False, size=16)
# preliminary phase, top left, feeding phase A
PX, PY, PW, PH = 20, 10, 170, 52
svg += box(PX, PY, PW, PH, ['Preliminary'])
ax, ay = pt(-90)
top = ay - BH / 2
svg.append(f'<polyline points="{PX + PW},{PY + PH / 2} {ax - 50},{PY + PH / 2} '
           f'{ax - 50},{top - 12}" fill="none" stroke="{EDGE}" stroke-width="2.5"/>')
svg.append(arrowhead(ax - 50, top - 1, 90))
# legend
LY = H - 28
svg.append(f'<line x1="40" y1="{LY}" x2="90" y2="{LY}" stroke="{EDGE}" stroke-width="2.5"/>')
svg.append(arrowhead(92, LY, 0))
svg.append(f'<text x="104" y="{LY + 6}" font-size="13" fill="{MUTED}">Usual order of phases</text>')
svg.append(f'<line x1="290" y1="{LY}" x2="340" y2="{LY}" stroke="{MUTED}" stroke-width="1.6" '
           f'stroke-dasharray="6 5"/>')
svg.append(f'<text x="352" y="{LY + 6}" font-size="13" fill="{MUTED}">'
           'Each phase reads and updates the managed requirements</text>')
svg.append('</svg>')
Path(__file__).resolve().parent.parent.joinpath('adm_cycle.svg').write_text('\n'.join(svg) + '\n')
print('wrote adm_cycle.svg')
