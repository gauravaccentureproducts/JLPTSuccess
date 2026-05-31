"""Strip the pattern-echo prefix from `meaning_en` (2026-05-31).

Companion fix script to `audit_meaning_en_pattern_echo_2026_05_31.py`.
For each pattern flagged by the audit (meaning_en starts with the
pattern text + a `-`/`–`/`:`/`=` separator), replace `meaning_en` with
the portion AFTER the separator.

Read backup at:
    data/grammar.json.bak_2026_05_31_ui_polish

Run from N5/:
    python tools/fix_meaning_en_pattern_echo_2026_05_31.py --dry-run
    python tools/fix_meaning_en_pattern_echo_2026_05_31.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "data" / "grammar.json"

SEP_RE = re.compile(r"\s*[-–—:=]\s*")


def _kana_norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("／", "/").replace("、", ",")).strip()


def _strip_echo(meaning: str, pattern: str) -> str | None:
    """Return the trimmed meaning, or None if no echo to strip."""
    if not meaning or not pattern:
        return None
    m_norm = _kana_norm(meaning)
    p_norm = _kana_norm(pattern)
    if not m_norm.startswith(p_norm):
        return None
    rest = m_norm[len(p_norm):]
    sep_m = SEP_RE.match(rest)
    if not sep_m:
        return None
    suggested = rest[sep_m.end():].strip()
    if not suggested:
        return None
    # Drop wrapping quotes if the entire string is quoted.
    if (suggested.startswith("'") and suggested.endswith("'")) or \
       (suggested.startswith('"') and suggested.endswith('"')):
        suggested = suggested[1:-1].strip()
    # Capitalize the first letter if it's lowercase (consistent subtitle style).
    if suggested and suggested[0].islower():
        suggested = suggested[0].upper() + suggested[1:]
    return suggested


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    g = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    patterns = g.get("patterns", [])
    fixed = 0
    samples: list[tuple[str, str, str]] = []
    for p in patterns:
        suggested = _strip_echo(p.get("meaning_en", "") or "", p.get("pattern", "") or "")
        if suggested is None:
            continue
        before = p["meaning_en"]
        if before == suggested:
            continue
        if not args.dry_run:
            p["meaning_en"] = suggested
        fixed += 1
        if len(samples) < 5:
            samples.append((p.get("id", ""), before, suggested))

    # Bump version
    meta = g.get("_meta") or {}
    meta_version = meta.get("version", "")
    if not args.dry_run and fixed:
        meta["version"] = "2026.05.31-meaning-en-dedup"
        g["_meta"] = meta
        GRAMMAR.write_text(
            json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"Patterns scanned: {len(patterns)}")
    print(f"meaning_en fixed: {fixed}{' (dry-run)' if args.dry_run else ''}")
    if samples:
        print("\nSample edits:")
        for pid, before, after in samples:
            print(f"  [{pid}]")
            print(f"    BEFORE: {before!r}")
            print(f"    AFTER:  {after!r}")
    if not args.dry_run and fixed:
        print(f"\n_meta.version: {meta_version!r} -> {meta['version']!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
