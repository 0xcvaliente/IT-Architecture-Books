from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'common'))
from build_common import build

build(Path(__file__).resolve().parent, {
    'number': 1,
    'header': 'IT Architecture Course Book',
    'title': 'IT Architecture\nCourse Book',
    'subtitle': 'Book 1  ·  Foundations, reasoning and worked architectures',
    'cover_lines': lambda s: [
        'Vendor-neutral concepts with Azure and AWS examples',
        f"{s['chapters']} chapters   ·   {s['exercises']} exercises   ·   {s['labs']} practical labs",
        f"A twelve-week study route, four cases and {s['figures']} figures",
    ],
    'edition': 'Revised edition\nOctober 2026',
    'output': 'IT_Architecture_Course_Book.docx',
})
