"""IMP-182: bump the cache version across all 3 places in one command.

Usage: python tools/bump_cache_version.py <new-version>
  e.g.  python tools/bump_cache_version.py 1.15.4

Updates:
  1. index.html      `<link href="css/main.min.css?v=X.Y.Z">`
  2. index.html      `<script src="js/min/app.js?v=X.Y.Z">`
  3. sw.js           `const CACHE_VERSION = 'jlptsuccess-n5-vX.Y.Z'`

Verifies all three matched before saving. CI invariant JA-68 enforces
that the three remain in sync on every commit.
"""
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")


def main():
    if len(sys.argv) != 2:
        print("usage: python tools/bump_cache_version.py <new-version>")
        print("       e.g.  python tools/bump_cache_version.py 1.15.4")
        sys.exit(1)
    new = sys.argv[1].strip()
    if not VERSION_RE.match(new):
        print(f"error: '{new}' does not look like a semver X.Y.Z")
        sys.exit(1)

    index_path = Path("index.html")
    sw_path = Path("sw.js")

    index = index_path.read_text(encoding="utf-8")
    sw = sw_path.read_text(encoding="utf-8")

    # Extract current versions to validate before/after
    css_re = re.compile(r'(css/main\.min\.css\?v=)(\d+\.\d+\.\d+)')
    js_re = re.compile(r'(js/min/app\.js\?v=)(\d+\.\d+\.\d+)')
    sw_re = re.compile(r"(CACHE_VERSION\s*=\s*'jlptsuccess-n5-v)(\d+\.\d+\.\d+)(')")

    css_m = css_re.search(index)
    js_m = js_re.search(index)
    sw_m = sw_re.search(sw)

    if not (css_m and js_m and sw_m):
        print("error: could not locate version strings:")
        print(f"  css_match={bool(css_m)}, js_match={bool(js_m)}, sw_match={bool(sw_m)}")
        sys.exit(1)

    old_css = css_m.group(2)
    old_js = js_m.group(2)
    old_sw = sw_m.group(2)

    print(f"Current:  css={old_css}  js={old_js}  sw={old_sw}")
    print(f"Bumping to: {new}")

    if old_css != old_js or old_js != old_sw:
        print(f"warning: pre-bump versions differ — will normalize all 3 to {new}")

    new_index = css_re.sub(rf"\g<1>{new}", index)
    new_index = js_re.sub(rf"\g<1>{new}", new_index)
    new_sw = sw_re.sub(rf"\g<1>{new}\g<3>", sw)

    index_path.write_text(new_index, encoding="utf-8")
    sw_path.write_text(new_sw, encoding="utf-8")

    print("Done. Verify with: grep -E '?v=|CACHE_VERSION' index.html sw.js")


if __name__ == "__main__":
    main()
