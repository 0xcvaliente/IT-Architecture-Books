#!/bin/sh
# Render figures/src/NAME.scene.json -> figures/NAME.svg and figures/NAME.png
# using the diagram-craft scene renderer, DejaVu Sans text and the series palette.
# Usage: sh common/make_figure.sh book3 capability_map
set -e
BOOK="$1"; NAME="$2"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
DC="$HOME/.claude/skills/diagram-craft/scripts/diagram.py"
SRC="$HERE/$BOOK/figures/src/$NAME.scene.json"
TMP="$(mktemp -d)"
python3 -I "$DC" check "$SRC"
python3 -I "$DC" render "$SRC" --output "$TMP/$NAME.html" --force
python3 -I "$DC" extract "$TMP/$NAME.html" --output "$TMP/$NAME.svg" --force
sed 's/font-family="[^"]*"/font-family="DejaVu Sans"/g' "$TMP/$NAME.svg" > "$HERE/$BOOK/figures/$NAME.svg"
rsvg-convert -w 5268 -b white "$HERE/$BOOK/figures/$NAME.svg" -o "$HERE/$BOOK/figures/$NAME.png"
rsvg-convert -w 1300 -b white "$HERE/$BOOK/figures/$NAME.svg" -o "$TMP/$NAME.preview.png"
echo "preview: $TMP/$NAME.preview.png"
