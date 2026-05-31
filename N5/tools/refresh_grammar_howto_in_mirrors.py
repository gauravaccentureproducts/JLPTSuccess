"""Surgically refresh the body of each grammar static mirror so the HOW
TO USE / 使い方 section matches the SPA's rendering.

Why this script exists (BUG-203, 2026-05-31):
    The static mirror at learn/<pid>/index.html previously emitted only
    ``<h2>Attaches to</h2><p>{tokens}</p>`` — a single technical token
    under the section header. Users hitting the mirror with JS-disabled
    or before SPA boot saw what looked like an empty HOW TO USE region.
    The SPA renders a much richer view (top table + conjugation table).
    build_static_mirrors.py was updated to emit the richer markup, but
    running the wholesale rebuild would re-migrate ~1372 hand-patched
    content mirrors. This script does a surgical edit: only the body
    region between ``<h1>...</h1>`` and the trailing ``<footer>...
    </footer>`` is regenerated. Header (app-header + nav + meta tags),
    footer (breadcrumb + license + pattern-id), SPA boot script, and
    canonical URLs are untouched.

What the script does:
    1. Reads data/grammar.json
    2. For each grammar pattern (id starts with "n5-")
    3. Opens learn/<id>/index.html if it exists
    4. Locates the <h1>...</h1> close tag and the next <footer> open tag
    5. Generates the new body via _render_grammar_pattern_body
    6. Substitutes the body region in place
    7. Writes back (preserving line endings and existing surrounding markup)

Run from N5/:
    python tools/refresh_grammar_howto_in_mirrors.py
    python tools/refresh_grammar_howto_in_mirrors.py --dry-run

After running:
    python tools/check_content_integrity.py
    (JA-172 verifies static-mirror parity for HOW TO USE).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Import the shared renderer from build_static_mirrors so the surgical
# edit emits exactly the same markup as a wholesale rebuild.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_static_mirrors import _render_grammar_pattern_body  # type: ignore  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "data" / "grammar.json"
LEARN_DIR = ROOT / "learn"


# Boundary markers used to identify the body region in an existing mirror.
# We match the <h1>...</h1> close (end of header) and the <footer ...>
# open (start of footer). The body is everything between, exclusive.
_H1_CLOSE_RE = re.compile(r"</h1>\s*", re.MULTILINE)
_FOOTER_OPEN_RE = re.compile(r"<footer[^>]*>", re.MULTILINE)


def _refresh_one(p: dict, dry_run: bool = False) -> str:
    """Return one of: 'rewrote', 'unchanged', 'missing', 'unparseable'."""
    pid = p.get("id")
    if not pid:
        return "missing"
    fp = LEARN_DIR / pid / "index.html"
    if not fp.exists():
        return "missing"
    src = fp.read_text(encoding="utf-8")
    h1m = _H1_CLOSE_RE.search(src)
    if not h1m:
        return "unparseable"
    footm = _FOOTER_OPEN_RE.search(src, h1m.end())
    if not footm:
        return "unparseable"
    new_body, _desc = _render_grammar_pattern_body(p)
    # Preserve the newline after </h1> that the original template uses
    # (line-break separates header from body), and a newline before
    # <footer> for cleanliness.
    new_section = src[: h1m.end()] + "\n" + new_body + "\n" + src[footm.start():]
    if new_section == src:
        return "unchanged"
    if not dry_run:
        fp.write_text(new_section, encoding="utf-8")
    return "rewrote"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Report what would change, don't write.")
    ap.add_argument("--ids", default="",
                    help="Comma-separated pattern IDs to refresh (default: all).")
    args = ap.parse_args()

    g = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    patterns = g.get("patterns", [])
    if args.ids:
        wanted = set(s.strip() for s in args.ids.split(",") if s.strip())
        patterns = [p for p in patterns if p.get("id") in wanted]
        if not patterns:
            print(f"No patterns matched --ids={args.ids!r}")
            return 1

    counts = {"rewrote": 0, "unchanged": 0, "missing": 0, "unparseable": 0}
    unparseable_ids: list[str] = []
    missing_ids: list[str] = []
    for p in patterns:
        status = _refresh_one(p, dry_run=args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        if status == "unparseable":
            unparseable_ids.append(p.get("id") or "?")
        elif status == "missing":
            missing_ids.append(p.get("id") or "?")

    print("=" * 60)
    print(f"Grammar mirrors HOW TO USE refresh{' (DRY RUN)' if args.dry_run else ''}")
    print("=" * 60)
    print(f"  Rewrote:      {counts['rewrote']}")
    print(f"  Unchanged:    {counts['unchanged']}")
    print(f"  Missing:      {counts['missing']} {missing_ids[:5]}{'...' if len(missing_ids)>5 else ''}")
    print(f"  Unparseable:  {counts['unparseable']} {unparseable_ids[:5]}{'...' if len(unparseable_ids)>5 else ''}")
    if counts["unparseable"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
