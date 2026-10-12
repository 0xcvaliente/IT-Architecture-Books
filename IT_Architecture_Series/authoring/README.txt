AUTHORING AND REBUILDING

The Markdown files in bookN/manuscript/ are the editorial source of each book. STYLE_GUIDE.md describes the
writing conventions and the markup the build understands.

Layout
  common/build_common.py   shared DOCX builder (cover, contents, styles, tables, figures, callouts, references)
  common/release.py        builds DOCX, exports PDF with LibreOffice, fills contents and index page numbers,
                           repeats until they are stable
  common/make_figure.sh    renders figures/src/NAME.scene.json to figures/NAME.svg and figures/NAME.png
  bookN/build_book.py      per-book settings (title, cover text, output name)
  bookN/references.py      IEEE source list; cite with {REF:key}
  bookN/figures/           editable SVG and rendered PNG figures; src/ holds diagram scene sources
  bookN/pages.json         contents page numbers written by release.py
  bookN/index.json         index terms and page numbers written by release.py
  bookN/index_extra.txt    optional extra index entries; bookN/index_scope.txt limits a term to chapters
  bookN/figure_defer.json  figure placement adjustments written by release.py (with figure_scale.json)

Requirements
  Python 3.10+ with python-docx and pymupdf; LibreOffice; rsvg-convert (librsvg) for figures.
  Fonts: Nimbus Sans (URW base35) for text, DejaVu Sans Mono for code and DejaVu Sans for figure text.
  release.py copies the fonts from ~/Library/Fonts into a private LibreOffice profile so exports use the
  checked typefaces, and disables ligatures in the code font for the PDF.

Rebuild one book (from this folder)
  python bookN/build_book.py              DOCX only; prints counts and warns if exercises and answers differ
  python common/release.py N              DOCX and PDF with verified contents and index page numbers
  python common/release.py 1 2 3 --copy   also copies the results to ../books/

The cover statistics (chapters, exercises, labs, figures) are computed from the manuscript. The index is
generated from the glossary and from multi-word terms set in bold in the chapters; its page numbers come from
the exported PDF, so a DOCX built without release.py has no index. Figure numbers and
{FIG:name} cross-references are assigned automatically in order of appearance.

Word can open and edit the DOCX files directly. Pagination in another word processor or with substituted fonts
can differ from the supplied PDFs.
