"""Build, paginate and export a book: DOCX -> PDF, fill contents page numbers, rebuild, verify.

Usage: python common/release.py 1 [2 3] [--copy]
Requires python-docx, pymupdf and LibreOffice (soffice).
"""
from pathlib import Path
import hashlib, json, re, shutil, subprocess, sys, zipfile
import pymupdf
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_common import index_terms

HERE = Path(__file__).resolve().parent
AUTH = HERE.parent
BOOKS = AUTH.parent / 'books'
SOFFICE = shutil.which('soffice') or '/Applications/LibreOffice.app/Contents/MacOS/soffice'
RELEASE_NAMES = {1: 'Book_1_IT_Architecture_Course_Book', 2: 'Book_2_IT_Architecture_in_Practice', 3: 'Book_3_Enterprise_Architecture'}
OUT_NAMES = {1: 'IT_Architecture_Course_Book', 2: 'IT_Architecture_in_Practice', 3: 'Enterprise_Architecture'}


def run_build(b, pages=None):
    cmd = [sys.executable, str(AUTH / f'book{b}' / 'build_book.py')]
    if pages: cmd += ['--pages', str(pages)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr)
    return r.stdout.strip()


FONTS = sorted((Path.home() / 'Library' / 'Fonts').glob('Nimbus*.otf')) + sorted((Path.home() / 'Library' / 'Fonts').glob('DejaVuSansMono*.ttf'))


def to_pdf(docx, b):
    # A private LibreOffice profile per book allows parallel exports; the checked
    # layout needs Nimbus Sans and Nimbus Mono PS inside that profile's font folder.
    profile = Path(f'/tmp/lo_profile_{hashlib.md5(str(AUTH).encode()).hexdigest()[:6]}_book{b}')
    fontdir = profile / 'user' / 'fonts'
    fontdir.mkdir(parents=True, exist_ok=True)
    for f in FONTS: shutil.copy(f, fontdir / f.name)
    # LibreOffice applies the monospace font's fi/fl ligatures (in_flight -> in_ﬂight); Word does
    # not. Export from a copy whose code font name disables ligatures with LibreOffice's ':-liga'.
    work = profile.parent / f'{profile.name}_export'; work.mkdir(exist_ok=True)
    src = work / docx.name
    with zipfile.ZipFile(docx) as zin, zipfile.ZipFile(src, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in ('word/styles.xml', 'word/document.xml'):
                for mono in (b'"Nimbus Mono PS"', b'"DejaVu Sans Mono"'):
                    data = data.replace(mono, mono[:-1] + b':-liga"')
            zout.writestr(item, data)
    subprocess.run([SOFFICE, f'-env:UserInstallation=file://{profile}', '--headless', '--convert-to', 'pdf',
                    '--outdir', str(work), str(src)], check=True, capture_output=True)
    pdf = docx.with_suffix('.pdf')
    shutil.move(str(src.with_suffix('.pdf')), pdf)
    return pdf


def norm(s):
    s = s.translate(str.maketrans('\u2018\u2019\u201c\u201d', "''\"\""))
    return re.sub(r'\s+', ' ', s).strip()


def heading_pages(pdf, headings):
    """Page of each H1: the first page after the contents where a 22 pt line equals the title."""
    doc = pymupdf.open(pdf)
    found = {}
    for pno in range(2, len(doc)):
        for b in doc[pno].get_text('dict')['blocks']:
            for l in b.get('lines', []):
                txt = norm(''.join(s['text'] for s in l['spans']))
                size = max((s['size'] for s in l['spans']), default=0)
                if size > 20 and txt not in found:
                    found[txt] = pno + 1
    pages = {}
    for h in headings:
        t = norm(h['title'])
        hit = found.get(t) or next((v for k, v in found.items() if t.startswith(k) or k.startswith(t[:40])), None)
        if hit is None: raise SystemExit(f'Heading not found in PDF: {t}')
        pages[h['title']] = hit
    return pages, len(doc)


def read_scope(root):
    """index_scope.txt: 'term | 9-11' limits a term to those chapters (for words with several senses)."""
    f = root / 'index_scope.txt'; scope = {}
    if f.exists():
        for line in f.read_text().splitlines():
            if '|' in line and not line.startswith('#'):
                term, rng = (x.strip() for x in line.split('|', 1))
                lo, _, hi = rng.partition('-'); scope[term] = (int(lo), int(hi or lo))
    return scope


def index_pages(pdf, headings, pages, terms, scope=None):
    """Pages for each index term within the chapters and labs, preferring pages where the term is defined
    (set in bold) and pages where it occurs most often. At most six pages per term."""
    order = [h for h in headings]
    first = min(pages[h['title']] for h in order if h['chapter'])
    last_ch = max(i for i, h in enumerate(order) if h['chapter'])
    after = [h for h in order[last_ch + 1:] if h['title'] not in ('Practical labs', 'Index')]
    end = pages[after[0]['title']] - 1 if after else None
    doc = pymupdf.open(pdf)
    end = end or len(doc)
    texts = {}
    for pno in range(first - 1, end):
        page = doc[pno]; r = page.rect
        normal, bold = [], []
        for b in page.get_text('dict', clip=pymupdf.Rect(0, 45, r.width, r.height - 45))['blocks']:
            for l in b.get('lines', []):
                for sp in l['spans']:
                    normal.append(sp['text'])
                    if 'Bold' in sp['font']: bold.append(sp['text'])
        texts[pno + 1] = (norm(' '.join(normal)).lower(), norm(' '.join(bold)).lower())
    # Page range of each chapter, for scoped terms.
    starts = [(h['chapter'], pages[h['title']]) for h in order if h['title'] in pages]
    span = {}
    for i, (ch, pg) in enumerate(starts):
        if ch: span[ch] = (pg, starts[i + 1][1] - 1 if i + 1 < len(starts) else len(doc))
    out = {}
    for term in terms:
        lim = (scope or {}).get(term)
        lo, hi = (span[lim[0]][0], span[lim[1]][1]) if lim else (0, 10 ** 6)
        base = term.split(' (')[0].lower()
        rx = re.compile(r'(?<![a-z0-9])' + re.escape(base) + r'(s|es)?(?![a-z0-9])')
        scored = []
        for pg, (txt, bold) in texts.items():
            if not lo <= pg <= hi: continue
            n = len(rx.findall(txt))
            if n: scored.append((n + (5 if rx.search(bold) else 0), pg))
        if scored:
            out[term] = sorted(pg for _, pg in sorted(scored, reverse=True)[:6])
    return out


def figure_gaps(pdf, root, defer, scale):
    """Figures that start a page while the previous page of the same chapter ends with a large gap.
    Returns an updated deferral map (name -> body paragraphs to move the figure past)."""
    raw = '\n'.join(f.read_text() for f in sorted((root / 'manuscript').glob('*.md')))
    raw = re.sub(r'^~~~.*?^~~~[^\n]*$', '', raw, flags=re.M | re.S)
    names = [m.group(1).strip() for m in re.finditer(r'^FIGURE ([^|]+)\|', raw, re.M)]
    doc = pymupdf.open(pdf); new, new_scale = dict(defer), dict(scale)
    for pno in range(3, len(doc)):
        page = doc[pno]; H = page.rect.height
        caps = [b for b in page.get_text('blocks') if re.match(r'Figure (\d+)\s', b[4])]
        imgs = page.get_image_info()
        if not caps or not imgs or min(i['bbox'][1] for i in imgs) > 110: continue
        n = int(re.match(r'Figure (\d+)', caps[0][4]).group(1))
        prev = doc[pno - 1]
        body = [b for b in prev.get_text('blocks') if 45 < b[1] < H - 45]
        if not body: continue
        gap = (H - 50 - max(b[3] for b in body)) / (H - 100)
        if gap > 0.22 and n <= len(names):
            name = names[n - 1]
            # Prefer a modest reduction that lets the figure and caption fit the gap; else move it later.
            room = H - 50 - max(b[3] for b in body) - (caps[0][3] - caps[0][1]) - 26
            fig_h = max(i['bbox'][3] - i['bbox'][1] for i in imgs)
            factor = room / fig_h
            if factor * scale.get(name, 1) >= 0.72 and factor < 1:
                new_scale[name] = round(scale.get(name, 1) * factor, 3)
            elif new.get(name, 0) < 4: new[name] = new.get(name, 0) + 1
    return new, new_scale


def release(b, copy):
    root = AUTH / f'book{b}'
    (root / 'index.json').unlink(missing_ok=True)
    (root / 'figure_defer.json').unlink(missing_ok=True)
    (root / 'figure_scale.json').unlink(missing_ok=True)
    defer, scale = {}, {}
    run_build(b)
    docx = root / 'output' / f'{OUT_NAMES[b]}.docx'
    terms = index_terms(root)
    pdf = to_pdf(docx, b)
    headings = json.loads((root / 'heading_index.json').read_text())
    pages, _ = heading_pages(pdf, headings)
    scope = read_scope(root)
    index = index_pages(pdf, headings, pages, terms, scope)
    for _ in range(9):
        (root / 'pages.json').write_text(json.dumps(pages, indent=1))
        (root / 'index.json').write_text(json.dumps(index, indent=1, ensure_ascii=False))
        info = run_build(b, root / 'pages.json')
        headings = json.loads((root / 'heading_index.json').read_text())
        pdf = to_pdf(docx, b)
        new, n = heading_pages(pdf, headings)
        new_index = index_pages(pdf, headings, new, terms, scope)
        new_defer, new_scale = figure_gaps(pdf, root, defer, scale)
        if new == pages and new_index == index and new_defer == defer and new_scale == scale: break
        pages, index, defer, scale = new, new_index, new_defer, new_scale
        (root / 'figure_defer.json').write_text(json.dumps(defer, indent=1))
        (root / 'figure_scale.json').write_text(json.dumps(scale, indent=1))
    else:
        raise SystemExit('Pagination did not converge')
    print(info)
    print(json.dumps({'book': b, 'pdf_pages': n, 'contents_verified': True, 'index_terms': len(index),
                      'figures_moved': len([k for k, v in defer.items() if v]), 'figures_scaled': len(scale)}))
    if copy:
        BOOKS.mkdir(exist_ok=True)
        shutil.copy(docx, BOOKS / f'{RELEASE_NAMES[b]}.docx')
        shutil.copy(pdf, BOOKS / f'{RELEASE_NAMES[b]}.pdf')


if __name__ == '__main__':
    copy = '--copy' in sys.argv
    for a in sys.argv[1:]:
        if a.isdigit(): release(int(a), copy)
