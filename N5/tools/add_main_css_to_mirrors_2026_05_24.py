"""Each migrated mirror only links its own inline <style> (the original
static-page styling). The SPA-rendered #app content uses different CSS
class names (.audio-skin-*, .example-audio, .pattern-nav-*, etc.) that
live in css/main.min.css. Without that stylesheet linked, the SPA-
rendered view is structurally correct but visually unstyled (the bug
the user reported - audio controls render as a row of plain buttons).

Fix: add <link rel="stylesheet" href="../../css/main.min.css"> to each
mirror's head, immediately after the existing <style> block.

Idempotent: skips files that already link main.min.css.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEARN_DIR = ROOT / "learn"

CSS_LINK = '<link rel="stylesheet" href="../../css/main.min.css">'
RE_STYLE_END = re.compile(r"</style>\s*", re.IGNORECASE)


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if CSS_LINK in text:
        return False
    new_text, n = RE_STYLE_END.subn(f"</style>\n{CSS_LINK}\n", text, count=1)
    if n == 0 or new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    mirrors = []
    for child in sorted(LEARN_DIR.iterdir()):
        if not child.is_dir():
            continue
        if not child.name.startswith("n5-"):
            continue
        idx = child / "index.html"
        if idx.exists():
            mirrors.append(idx)
    print(f"Found {len(mirrors)} mirrors")
    changed = 0
    for m in mirrors:
        if patch(m):
            changed += 1
    print(f"Patched {changed} mirrors (added main.min.css link)")


if __name__ == "__main__":
    main()
