"""Audit `meaning_en` strings for the pattern-echo anti-pattern (2026-05-31).

User-caught on n5-040 detail page: the subtitle rendered as
    'こんな / そんな / あんな / どんな + Noun - this/that kind of'
because `meaning_en` for that pattern literally started with the pattern
text. The renderer pairs the pattern title (h2) with the meaning
subtitle; when meaning_en echoes the pattern, the subtitle is
"<pattern> - <real meaning>", visually wasting the line on a repeat
of what's already in the title.

This script:
  1. Scans every grammar pattern.
  2. Reports rows where `meaning_en` starts with the pattern (or a
     normalized form), followed by a separator (-, –, :, =).
  3. Suggests a trimmed `meaning_en`.

Read-only. Writes a report file; does not mutate data.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAMMAR = ROOT / "data" / "grammar.json"

# Separators that, when found between the echoed pattern and the real
# meaning, qualify the prefix as a redundant echo.
SEP_RE = re.compile(r"\s*[-–—:=]\s*")


def _kana_norm(s: str) -> str:
    """Compare ignoring spaces around slashes + variant separators that
    can differ between p.pattern and the prefix in meaning_en."""
    return re.sub(r"\s+", " ", s.replace("／", "/").replace("、", ",")).strip()


def _starts_with_pattern(meaning: str, pattern: str) -> tuple[bool, str | None]:
    """Returns (echoes, suggested_meaning).
    Echoes = True iff meaning starts with the pattern (normalized), then
    a separator. suggested_meaning is the portion after the separator,
    or None if no echo.
    """
    if not meaning or not pattern:
        return False, None
    m_norm = _kana_norm(meaning)
    p_norm = _kana_norm(pattern)
    if not m_norm.startswith(p_norm):
        return False, None
    rest = m_norm[len(p_norm):]
    sep_m = SEP_RE.match(rest)
    if not sep_m:
        return False, None
    suggested = rest[sep_m.end():].strip()
    if not suggested:
        return False, None
    # Strip wrapping quotes if the entire suggestion is a single quoted phrase.
    if (suggested.startswith("'") and suggested.endswith("'")) or \
       (suggested.startswith('"') and suggested.endswith('"')):
        suggested = suggested[1:-1].strip()
    return True, suggested


def main() -> int:
    g = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    patterns = g.get("patterns", [])
    hits: list[dict] = []
    for p in patterns:
        echoes, suggested = _starts_with_pattern(
            p.get("meaning_en", "") or "", p.get("pattern", "") or ""
        )
        if echoes:
            hits.append({
                "id": p.get("id"),
                "pattern": p.get("pattern"),
                "current_meaning_en": p.get("meaning_en"),
                "suggested_meaning_en": suggested,
            })
    print(f"Total patterns: {len(patterns)}")
    print(f"Pattern-echo hits: {len(hits)}")
    if hits:
        out = ROOT / ".tmp_meaning_en_echo_report.json"
        out.write_text(json.dumps(hits, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Report: {out}")
        print()
        print("Sample (first 10):")
        for h in hits[:10]:
            print(f"  [{h['id']}] {h['pattern']!r}")
            print(f"    current:   {h['current_meaning_en']!r}")
            print(f"    suggested: {h['suggested_meaning_en']!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
