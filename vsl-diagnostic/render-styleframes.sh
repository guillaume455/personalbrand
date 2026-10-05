#!/bin/bash
# Renders styleframes with the Chromium preinstalled in this environment (the pip Playwright expects another build).
# Usage: bash vsl-diagnostic/render-styleframes.sh [A1 B2 ...]
cd "$(dirname "$0")/.."
python3 - "$@" <<'PY'
import runpy, sys
from playwright.sync_api import BrowserType
_launch = BrowserType.launch
BrowserType.launch = lambda self, **kw: _launch(self, executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", **kw)
sys.argv = [".claude/skills/motion-design/scripts/render-styleframes.py", "vsl-diagnostic", *sys.argv[1:]]
runpy.run_path(sys.argv[0], run_name="__main__")
PY
