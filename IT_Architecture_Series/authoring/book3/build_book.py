from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'common'))
from build_common import build

build(Path(__file__).resolve().parent, {
    'number': 3,
    'header': 'Enterprise Architecture',
    'title': 'Enterprise\nArchitecture',
    'subtitle': 'Book 3  ·  Strategy, governance and transformation',
    'cover_lines': lambda s: [
        'Frameworks, decisions and evidence for enterprise change',
        f"{s['chapters']} chapters   ·   {s['exercises']} exercises   ·   {s['figures']} figures",
        'A ten-week route from enterprise analysis to a three-year roadmap',
    ],
    'edition': 'Revised edition\nOctober 2026',
    'output': 'Enterprise_Architecture.docx',
})
