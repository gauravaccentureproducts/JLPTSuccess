"""Migration: replace every `location.hash = '#/...'` (or template
literal variant) with `navigateTo('...')` across the source JS files.
Adds the `import { navigateTo } from './router.js';` line after the
existing imports if not already present.

Skips the minified files (js/min/*). They are rebuilt by build_min_js.py.

Skips js/app.js because app.js already imports navigateTo + uses other
router helpers; navigation inside app.js's DOMContentLoaded routing
uses replaceState directly, not navigateTo.

Run: python tools/migrate_hash_to_pathname_2026_05_24.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS_DIR = ROOT / "js"

# Files known to contain `location.hash = ...` (from grep output)
TARGETS = [
    "diagnostic.js", "drill.js", "listening.js", "particle-pairs.js",
    "reading.js", "review.js", "settings.js", "sitting.js",
    "summary.js", "te-form.js", "test.js", "verb-class.js",
]

# Match patterns:
#   location.hash = '#/route';
#   location.hash = "#/route";
#   location.hash = `#/route`;
#   location.hash = `#/listening/${id}`;
RE_SINGLE = re.compile(r"location\.hash\s*=\s*'#/([^']*)'\s*;")
RE_DOUBLE = re.compile(r'location\.hash\s*=\s*"#/([^"]*)"\s*;')
RE_TEMPLATE = re.compile(r"location\.hash\s*=\s*`#/([^`]*)`\s*;")

IMPORT_LINE = "import { navigateTo } from './router.js';"


def patch_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    original = text
    counts = {"single": 0, "double": 0, "template": 0}

    def sub_single(m):
        counts["single"] += 1
        return f"navigateTo('{m.group(1)}');"
    def sub_double(m):
        counts["double"] += 1
        return f'navigateTo("{m.group(1)}");'
    def sub_template(m):
        counts["template"] += 1
        return f"navigateTo(`{m.group(1)}`);"

    text = RE_SINGLE.sub(sub_single, text)
    text = RE_DOUBLE.sub(sub_double, text)
    text = RE_TEMPLATE.sub(sub_template, text)

    if text == original:
        return {"file": path.name, "changed": False, **counts}

    # Add the import if not already present
    if IMPORT_LINE not in text:
        # Find the last import line and insert after it
        lines = text.split("\n")
        last_import_idx = -1
        for i, line in enumerate(lines):
            if line.startswith("import ") and " from " in line:
                last_import_idx = i
        if last_import_idx >= 0:
            lines.insert(last_import_idx + 1, IMPORT_LINE)
            text = "\n".join(lines)
        else:
            # No imports at all - prepend
            text = IMPORT_LINE + "\n" + text

    path.write_text(text, encoding="utf-8")
    return {"file": path.name, "changed": True, **counts}


def main():
    print(f"Scanning {len(TARGETS)} files in {JS_DIR}")
    total_replacements = 0
    for name in TARGETS:
        path = JS_DIR / name
        if not path.exists():
            print(f"  SKIP (not found): {name}")
            continue
        result = patch_file(path)
        replacements = result["single"] + result["double"] + result["template"]
        total_replacements += replacements
        mark = "OK" if result["changed"] else "noop"
        print(f"  {mark}  {result['file']}: {replacements} replacement(s) (single={result['single']} double={result['double']} template={result['template']})")
    print(f"Total replacements: {total_replacements}")


if __name__ == "__main__":
    main()
