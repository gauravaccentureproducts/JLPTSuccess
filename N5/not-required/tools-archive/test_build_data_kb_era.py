"""Regression tests for tools/build_data.py.

These tests guard against the Pass-13 build-pipeline corruption class:
- Bug A (line 107): a kanji-header regex required `\\s*$` end-anchor, so
  `[Ext]`-tagged headers (e.g. `**手** [Ext]`) were silently dropped - 9
  N5 kanji vanished from data/kanji.json before the fix.
- Bug B (line 142): meanings were split on `[/,;]` without first stripping
  parentheticals, so glosses like "birth (primary N5 use: in compounds
  like 学生, 先生)" fragmented into 3 broken pieces.

The tests synthesise a small KB-like markdown fixture, run the parsers on
it, and assert the parsed result matches a known-good shape. They do NOT
touch the real data/ files - pure unit tests against the parser.

Run standalone:
    python tools/test_build_data.py

Or via pytest if the project ever adopts it:
    pytest tools/test_build_data.py -v

Exit code 0 on pass, 1 on any failure.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

# Add the project root to the path so we can import tools.build_data as a
# module without relying on cwd.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import build_data  # noqa: E402


# ---------------------------------------------------------------------------
# Fixture: a small markdown file shaped like KnowledgeBank/kanji_n5.md.
# Includes plain headers, [Ext]-tagged headers, and a meaning containing
# parentheticals + commas - the exact combinations that broke pre-Pass-13.
# ---------------------------------------------------------------------------

KB_FIXTURE = """
# N5 Kanji

## Body

- **一**
  - On: イチ / イツ
  - Kun: ひと
  - Meanings: one

- **手** [Ext]
  - On: シュ
  - Kun: て
  - Meanings: hand

- **生**
  - On: セイ / ショウ
  - Kun: い
  - Meanings: life, birth (primary N5 use: in compounds like 学生, 先生)

- **円** [Ext]
  - On: エン
  - Kun:
  - Meanings: yen
"""


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def make_fixture() -> Path:
    fd = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".md", delete=False
    )
    fd.write(KB_FIXTURE)
    fd.close()
    return Path(fd.name)


def test_ext_tagged_kanji_are_parsed() -> list[str]:
    """Bug A regression: `**手** [Ext]` must produce a 手 entry.

    Before Pass-13 fix, the regex required the line to end with `**` (or
    only whitespace), so `[Ext]` after the bold marker caused the parser
    to skip the line entirely. 9 kanji disappeared from data/kanji.json
    in production.
    """
    fixture = make_fixture()
    failures = []
    try:
        readings = build_data.extract_kanji_readings(fixture)
        if "手" not in readings:
            failures.append(
                "Bug A regression: `**手** [Ext]` was not parsed. "
                f"Got entries for: {list(readings.keys())}"
            )
        if "円" not in readings:
            failures.append(
                "Bug A regression: `**円** [Ext]` was not parsed. "
                f"Got entries for: {list(readings.keys())}"
            )
    finally:
        fixture.unlink()
    return failures


def test_meanings_with_parenthetical_not_fragmented() -> list[str]:
    """Bug B regression: meanings with `(... ,)` parentheticals must not
    fragment on internal commas. Pre-fix, `生`'s meaning string fragmented
    into three pieces because the comma inside the parenthetical was a
    split point.
    """
    fixture = make_fixture()
    failures = []
    try:
        corpus = build_data.extract_kanji_corpus(fixture)
        sei = next((e for e in corpus if e.get("glyph") == "生"), None)
        if sei is None:
            failures.append("Bug B regression: 生 entry missing entirely")
            return failures
        meanings = sei.get("meanings", [])
        # Expected: ["life", "birth"] (or similar clean tokens). Bug-B output
        # was ["life", "birth (primary N5 use: in compounds like 学生", "先生)"]
        # - three fragments with broken parens.
        if any("primary N5 use" in m for m in meanings):
            failures.append(
                "Bug B regression: parenthetical leaked into a meanings entry. "
                f"Got: {meanings}"
            )
        if any(m.endswith(")") and not m.startswith("(") for m in meanings):
            failures.append(
                "Bug B regression: a meanings entry ends with `)` (orphaned "
                f"parenthetical fragment). Got: {meanings}"
            )
        if len(meanings) > 4:
            failures.append(
                f"Bug B regression: 生 meanings exploded into {len(meanings)} "
                f"pieces (expected ≤2). Got: {meanings}"
            )
    finally:
        fixture.unlink()
    return failures


def test_headers_without_ext_still_work() -> list[str]:
    """Smoke test: plain `**一**` header still parses (we didn't break the
    happy path while widening the regex)."""
    fixture = make_fixture()
    failures = []
    try:
        readings = build_data.extract_kanji_readings(fixture)
        if "一" not in readings:
            failures.append(
                "Smoke regression: plain `**一**` header was not parsed."
            )
    finally:
        fixture.unlink()
    return failures


def test_real_data_invariants() -> list[str]:
    """End-to-end: the real KnowledgeBank/kanji_n5.md must produce 106
    entries (matches data/n5_kanji_whitelist.json), all kanji glyphs are
    BMP characters, and no entry has the parenthetical-fragment shape.
    """
    failures = []
    kb = ROOT / "KnowledgeBank" / "kanji_n5.md"
    if not kb.exists():
        return [f"Smoke: KB file missing: {kb}"]
    readings = build_data.extract_kanji_readings(kb)
    if len(readings) != 106:
        failures.append(
            f"E2E regression: expected 106 kanji from KnowledgeBank/kanji_n5.md, "
            f"got {len(readings)}. The Pass-13 corpus size is the canonical "
            f"truth (see verification.md Pass 13)."
        )
    for kanji in readings:
        if not (0x4E00 <= ord(kanji[0]) <= 0x9FFF):
            failures.append(
                f"E2E regression: parsed entry '{kanji}' is not a CJK Unified "
                f"Ideographs glyph - parser leaked junk."
            )

    corpus = build_data.extract_kanji_corpus(kb)
    if len(corpus) != 106:
        failures.append(
            f"E2E regression: extract_kanji_corpus returned {len(corpus)} "
            f"entries, expected 106."
        )
    for entry in corpus:
        for m in entry.get("meanings", []):
            if "primary N5 use" in m or "compounds like" in m:
                failures.append(
                    f"E2E regression: parenthetical leaked into meanings of "
                    f"{entry.get('glyph')!r}: {m!r}"
                )
    return failures


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

TESTS = [
    ("Bug A - [Ext]-tagged headers parse", test_ext_tagged_kanji_are_parsed),
    ("Bug B - parenthetical doesn't fragment meanings", test_meanings_with_parenthetical_not_fragmented),
    ("Smoke - plain headers still parse", test_headers_without_ext_still_work),
    ("E2E - real KB produces 106 clean entries", test_real_data_invariants),
]


def main() -> int:
    print(f"build_data.py regression tests - {len(TESTS)} cases")
    print("=" * 60)
    overall: list[str] = []
    for label, fn in TESTS:
        try:
            failures = fn()
        except Exception as e:  # noqa: BLE001
            failures = [f"raised {type(e).__name__}: {e}"]
        status = "PASS" if not failures else f"FAIL ({len(failures)})"
        print(f"  {status:<8} {label}")
        if failures:
            for f in failures:
                print(f"           - {f}")
        overall.extend(failures)
    print("=" * 60)
    if overall:
        print(f"FAIL: {len(overall)} regression(s)")
        return 1
    print(f"PASS: all {len(TESTS)} tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
