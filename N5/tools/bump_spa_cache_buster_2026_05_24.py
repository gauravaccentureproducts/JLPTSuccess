"""Bump the ?v=N.N.N cache-buster on the <script type=module src=...app.js>
tag across index.html + all 178 mirror HTMLs. Without bumping it,
browsers that have the old app.js cached will keep serving the old
JS even though server has the fix.

Idempotent — replaces `?v=<anything>` with `?v=NEW_VERSION` only on
lines referencing app.js.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEW_VERSION = "1.17.0"

# Match `src="...app.js?v=<old>"` (any version)
RE_APP_JS = re.compile(r'(src="[^"]*app\.js\?v=)[^"]+(")')


def patch_file(path: Path, new_version: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, n = RE_APP_JS.subn(rf"\g<1>{new_version}\g<2>", text)
    if n == 0 or new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    targets = [ROOT / "index.html"]
    learn_dir = ROOT / "learn"
    for child in sorted(learn_dir.iterdir()):
        if child.is_dir() and child.name.startswith("n5-"):
            idx = child / "index.html"
            if idx.exists():
                targets.append(idx)
    changed = 0
    for t in targets:
        if patch_file(t, NEW_VERSION):
            changed += 1
    print(f"Bumped app.js cache-buster to ?v={NEW_VERSION} in {changed} files ({len(targets)} scanned)")


if __name__ == "__main__":
    main()
