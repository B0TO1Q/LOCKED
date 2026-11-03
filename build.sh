#!/usr/bin/env bash
# Rebuilds LOCKED.pdf, the per-sheet SVGs and index.html.
# Needs: python3, reportlab (pip install reportlab), poppler-utils (pdftocairo).
set -euo pipefail
cd "$(dirname "$0")"

python3 src/build_locked.py

rm -rf svg && mkdir svg
python3 - <<'EOF'
import json, subprocess
pages = json.load(open("src/pages.json"))
subprocess.run(["pdftocairo", "-svg", "-f", "1", "-l", "1", "LOCKED.pdf", "svg/cover.svg"], check=True)
for p in pages:
    n = str(p["page"])
    subprocess.run(["pdftocairo", "-svg", "-f", n, "-l", n, "LOCKED.pdf", f"svg/{p['code']}.svg"], check=True)
EOF
# Give every sheet a real 8.5 x 11 in. size so it opens and prints at true scale.
sed -i.bak '2s/width="612" height="792"/width="8.5in" height="11in"/' svg/*.svg && rm -f svg/*.bak

python3 src/build_html.py
