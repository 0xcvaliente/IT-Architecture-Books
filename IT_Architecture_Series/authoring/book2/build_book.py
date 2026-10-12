from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'common'))
from build_common import build

build(Path(__file__).resolve().parent, {
    'number': 2,
    'header': 'IT Architecture in Practice',
    'title': 'IT Architecture\nin Practice',
    'subtitle': 'Book 2  ·  Design evaluation and decision-making',
    'cover_lines': lambda s: [
        'Four design studios with worked dossiers and Azure and AWS mappings',
        f"{s['chapters']} chapters   ·   {s['exercises']} exercises   ·   {s['figures']} figures",
        'An eight-week route with experiments and architecture dossiers',
    ],
    'edition': 'Revised edition\nOctober 2026',
    'output': 'IT_Architecture_in_Practice.docx',
})
