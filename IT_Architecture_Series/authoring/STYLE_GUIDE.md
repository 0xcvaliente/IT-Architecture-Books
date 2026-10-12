# Series style guide

This guide governs the manuscript sources in `book1/`, `book2/` and `book3/`. It is a maintainer document and is not printed in the books.

## 1. The books are self-contained

Each book is an independent textbook. A reader with only the PDF must be able to study every chapter, lab and exercise.

- Do not refer to companion files by name (`lab3_database.py`, `.csv`, `.md` worksheets, "the practice folder", "the lab bundle", "the authoring bundle"). When a lab needs code or data, print it in the book: a short listing in a `~~~` block, or a small table.
- Do not mention how the book was produced or reviewed. Remove: "review edition", "second edition", "academic revision", "abstract-only", "claim-to-source record", "evidence record", "change record", "external-review package", "peer-reviewed" status, "assistant-led", "learner's request", "this revision", named recipients ("Prepared for …"), and source access logistics ("full text was unavailable", "HTTP 403").
- The content is general IT architecture knowledge illustrated with fictional organisations. It does not describe any reader's employer, codebase or project.
- State once, in each book's opening chapter, that the organisations, workloads, budgets and datasets are fictional teaching examples. Do not repeat the disclaimer later ("fictional", "original teaching example", "our own illustration") unless a specific sentence could be mistaken for a real-world fact.

## 2. Voice and sentence style

Write as a clear, confident university textbook in British English.

- **Say what things are and do.** Prefer positive statements. Use the "X is not Y" correction only for a real, common misconception, at most once or twice per section.
  - Before: "A receipt is not a CRM confirmation. It is not a promise of resolution."
  - After: "A receipt confirms that the portal has durably stored the request. CRM confirmation comes later, when the handoff succeeds."
- **One caveat, in the right place.** End paragraphs on the main idea, not on a hedge. Remove stacked caveats ("This does not prove…", "not automatically…", "not a universal…") unless the limit changes what the reader should do.
- **Concrete before abstract.** Introduce a mechanism with a small, specific example (numbers, a request, a table row) and then generalise. Aim for at least two "for example" moments per chapter.
- **Vary the rhythm.** Mix short and longer sentences. Avoid long chains of abstract nouns ("evidence of authority boundary ownership"). Write "who owns the data" rather than "data authority ownership".
- **Use structure.** Use bullet lists for three or more parallel items, numbered lists for procedures, `###` subheadings to break sections longer than about 400 words, and tables for comparisons.
- **Callouts.** Use at most two per chapter, as a line starting with `> ` and a bold label: `> **Common mistake.** …`, `> **In practice.** …`, `> **Check your understanding.** …`.
- **Terminology.** Define a term in bold at first use, then use it consistently. Add new technical terms to the glossary (Book 1) or define them in the text (Books 2 and 3).
- **Punctuation.** Use normal punctuation everywhere, including headings, captions, table cells and reference titles. Write "Operating systems, networking and the request journey", not "Operating systems networking and the request journey". Use the serial comma only where needed for clarity, and be consistent within a book.
- Use British spelling (organisation, authorise, modelling, programme for a portfolio of projects, program for software).

## 3. Chapter shape

```
# N Title

## Learning objectives

After this chapter you should be able to:

- Explain …
- Calculate …
- Design …
- Evaluate …

(content sections, each with a worked example where useful)

## Exercises

N.1 …
N.2 …

## Key points

- …
- …
```

- 3 to 5 learning objectives, each starting with a measurable verb (explain, calculate, compare, design, evaluate, critique, model).
- Key points: 3 to 6 bullets that restate the chapter's main ideas, not new material.
- Integrate material where it belongs logically. Do not leave "advanced" or late-added sections bolted onto the end of a chapter.
- Exercises: at least 4 per chapter, numbered N.1, N.2, … consecutively, mixing levels: one recall or explanation, one calculation or application, one design task, one critique or evaluation. Every exercise has an answer.
- Answers: in the answers chapter, under `## Chapter N`, written as `**N.M** answer text`. Show working for calculations. For open questions, give a model answer and the marking criteria; accept defensible alternatives.

## 4. Markup the build understands

- `# N Title` chapter; `# Title` front or back matter; `##`, `###` headings.
- `- ` bullet; `1. ` numbered step; `> ` callout.
- `| a | b |` tables. The first row is the header. Cells may contain `**bold**` and `` `code` ``. Keep cells short.
- `~~~` code blocks. Lines must not exceed 88 characters. Listings should usually be under 40 lines.
- `FIGURE name | Caption sentence` inserts `figures/name.png`. Captions are full sentences with normal punctuation.
- `{FIG:name}` in text becomes "Figure N". Use it instead of "the figure below".
- `{REF:key}` or `{REF:key1,key2}` cites sources defined in `references.py`.
- `` `inline code` `` for identifiers, SQL keywords, HTTP headers and field names.
- `*italic*` for titles of books, standards and papers mentioned in running text, and for rare emphasis.
- Glossary entries (`**Term.** definition`) and multi-word terms set in bold in the chapters feed the generated index.

## 5. References

Each entry in `references.py` is `key: (authors, title, url, detail)`, formatted in IEEE style.

- Cite primary or canonical sources for ideas (the paper or book that introduced or defined the idea), standards for protocol claims, and official documentation for product behaviour.
- Books and papers without a free URL are allowed: use the DOI URL or the publisher's page. If there is no stable URL, use `''`.
- Every new source must be verified with a web search before it is added: authors, title, year, venue, and that it supports the claim. Never invent a reference, a page number or a DOI. If you cannot verify a source, do not cite it.
- Every defined source in a book must be cited, and every citation must support the sentence it follows.

## 6. Figures

- Prefer few, meaningful figures. Each figure needs a caption, a `{FIG:}` reference in the text, and a legend when line styles or colours carry meaning.
- To create a figure, invoke the `diagram-craft` skill for guidance. Write a positioned scene in `bookN/figures/src/NAME.scene.json` and run `sh common/make_figure.sh bookN NAME` from `authoring/`. Then open the printed preview PNG with the Read tool and fix any overlaps or unclear routes before using it.
- Use these palette tokens in every scene: `{"paper":"#ffffff","surface":"#f3f3f3","ink":"#000000","muted":"#323232","rule":"#323232","edge":"#323232","accent":"#276ef1","accent_surface":"#e8f0fe"}`. Use `emphasis` for at most one focal node. Keep labels short, use sentence case, and size the canvas at about 1000–1200 wide by 400–650 high.
- For diagrams the scene format cannot express (quadrants, timelines, cycles), write a clean standalone SVG by hand in the same palette with `font-family="DejaVu Sans"`, save it as `bookN/figures/NAME.svg`, and render it with `rsvg-convert -w 5268 -b white NAME.svg -o NAME.png`.
- To change an existing matplotlib figure, redraw it as a scene with the same name. Do not hand-edit the old path data.

## 7. Code listings

- Use Python 3.10+ with the standard library only (SQLite is fine), short and readable, with type hints where they help.
- Every listing must run as printed. Copy it to a scratch directory outside the repository, run it with `python3 -I`, and check that the output shown in the book matches exactly.
- Listings are generic teaching code. They model one mechanism clearly and state their limits in one sentence of prose, not in repeated disclaimers.
- If a book's `practice/` folder has a file with the same purpose, update that file to match the printed listing exactly, so the optional companion code never disagrees with the book.

## 8. Building and checking

From `authoring/`:

```
/tmp/itab/venv/bin/python bookN/build_book.py          # DOCX; prints counts, unused sources, warnings
/tmp/itab/venv/bin/python common/release.py N          # DOCX -> PDF with contents page numbers (needs LibreOffice)
python3 -I /tmp/itab/metrics.py .                       # style metrics for all books
```

Run `release.py` with the sandbox disabled. It writes `bookN/output/*.pdf`. Inspect changed pages by rendering them to PNG with pymupdf (`/tmp/itab/venv/bin/python`) and reading the images.
