"""Tiny helpers for the hand-built Book 3 figures (series palette, DejaVu Sans).

Each generator imports this module, writes ../NAME.svg, and is rendered with
rsvg-convert -w 5268 -b white NAME.svg -o NAME.png
"""
from math import atan2, cos, radians, sin
from pathlib import Path
from xml.sax.saxutils import escape

PAPER, SURFACE, INK, MUTED = '#ffffff', '#f3f3f3', '#000000', '#323232'
EDGE, ACCENT, ACCENT_SURFACE = '#323232', '#276ef1', '#e8f0fe'
OUT = Path(__file__).resolve().parent.parent


class Svg:
    def __init__(self, w: int, h: int, title: str, desc: str):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" '
            f'font-family="DejaVu Sans">',
            f'<title id="t">{escape(title)}</title>', f'<desc id="d">{escape(desc)}</desc>',
            f'<rect width="{w}" height="{h}" fill="{PAPER}"/>']

    def rect(self, x, y, w, h, fill=SURFACE, stroke=MUTED, sw=2, dash=None, rx=8):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=16, weight='normal', anchor='start', fill=INK,
             lead=None, rotate=None):
        """Draw one or more lines; y is the first baseline."""
        lead = lead or round(size * 1.25)
        tr = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ''
        for i, line in enumerate(s.split('\n')):
            self.parts.append(
                f'<text x="{x}" y="{y + i * lead}" font-size="{size}" font-weight="{weight}" '
                f'text-anchor="{anchor}" fill="{fill}"{tr}>{escape(line)}</text>')

    def line(self, x1, y1, x2, y2, stroke=EDGE, sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                          f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def arrow(self, x1, y1, x2, y2, stroke=EDGE, sw=2.5, dash=None, head=14):
        a = atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * 0.8 * cos(a), y2 - head * 0.8 * sin(a)
        self.line(x1, y1, bx, by, stroke, sw, dash)
        p2 = (x2 - head * cos(a) + head * 0.5 * sin(a), y2 - head * sin(a) - head * 0.5 * cos(a))
        p3 = (x2 - head * cos(a) - head * 0.5 * sin(a), y2 - head * sin(a) + head * 0.5 * cos(a))
        self.parts.append(f'<polygon points="{x2:.1f},{y2:.1f} {p2[0]:.1f},{p2[1]:.1f} '
                          f'{p3[0]:.1f},{p3[1]:.1f}" fill="{stroke}"/>')

    def circle(self, cx, cy, r, fill=INK, stroke=None, sw=2):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{s}/>')

    def save(self, name: str):
        (OUT / f'{name}.svg').write_text('\n'.join(self.parts + ['</svg>']) + '\n')
        print('wrote', name + '.svg')
