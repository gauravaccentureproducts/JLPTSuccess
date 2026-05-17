"""Fix BUG-041 through BUG-046 — reading.json data-quality bugs.

5 of these (BUG-041, 042, 044, 045, 046) are batch-drift in the
9 most-recently-added passages (n5.read.046–054), which used a
different authoring convention from the first 45 passages.
BUG-043 is independent — _meta.schema_additions update.

BUG-041: level field mixes semantics (easy/medium/info-search/N5).
         Migration: add `difficulty` field; drop `level`.
            easy/medium → difficulty=easy/medium
            N5 → difficulty=medium (the 9 newest passages)
            info-search → drop (info-search is in format_role)

BUG-042: summary field is mixed JA+EN+HI on 45 passages, JA-only
         on 9. Normalize to JA-only across all 54.
            For mixed entries: extract the JA portion before "("
            For JA-only entries: keep as-is

BUG-043: format_type enum missing "notice" in _meta.schema_additions.
         Add it; remove "comprehension" reference (resolved by BUG-044).

BUG-044: format_type AND format_role both set to "comprehension" on
         9 passages. Remove the duplicate format_type="comprehension"
         field. passage.format_role stays as the canonical passage-
         type field.

BUG-045: vocab_preview has two shapes (list of strings vs list of
         dicts). Normalize all 54 to Shape A (list of vocab IDs only).
         For the 9 Shape B passages: extract `vocab_id` from each
         dict.

BUG-046: 45 passages use わたし; 9 use 私. Standardize on 私 (kanji
         in N5 whitelist). String-replace わたし → 私 in JA text on
         the 45 passages; ensure kanji_used includes 私.
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
READING = ROOT / "data" / "reading.json"


def fix_bug_041_difficulty(passages: list[dict]) -> int:
    """Replace `level` with `difficulty`. Migration rules per the bug."""
    n = 0
    for p in passages:
        level = p.get("level")
        if level is None:
            continue
        # Map per bug description
        if level == "easy":
            difficulty = "easy"
        elif level == "medium":
            difficulty = "medium"
        elif level == "N5":
            difficulty = "medium"  # The 9 newest passages
        elif level == "info-search":
            difficulty = None  # info-search is in format_role; drop difficulty
        else:
            print(f"  WARN: {p.get('id')} has unknown level={level!r}; skipping")
            continue
        if difficulty:
            p["difficulty"] = difficulty
        # Drop level
        del p["level"]
        p["bug_041_fix_2026_05_17"] = True
        n += 1
    return n


def fix_bug_042_summary(passages: list[dict]) -> int:
    """Normalize summary to JA-only.

    For mixed entries (Shape A pattern "じこしょうかい (self-introduction विषय...)。"),
    extract the JA portion before the opening parenthesis. Move the
    parenthetical to a new `summary_en` field if it contains English.
    For JA-only entries, keep as-is.
    """
    n = 0
    # Allow Japanese full-stop 。 (U+3002), Devanagari danda । (U+0964),
    # ASCII period, or no terminator at all.
    paren_pattern = re.compile(r"^([^(]+?)\s*\(([^)]+)\)\s*[。।.]?\s*$")
    for p in passages:
        summary = p.get("summary")
        if not summary:
            continue
        # Check if the summary matches the mixed shape
        m = paren_pattern.match(summary.strip())
        if m:
            ja_title = m.group(1).strip()
            paren_content = m.group(2).strip()
            # Preserve EN portion in a new field; HI is already in summary_hi
            p["summary"] = ja_title
            if paren_content:
                p["summary_en_extracted"] = paren_content
            n += 1
        # else: already JA-only or unrecognized shape; leave alone
    return n


def fix_bug_043_meta_schema(reading_data: dict) -> int:
    """Update _meta.schema_additions text to reflect post-fix state."""
    meta = reading_data.setdefault("_meta", {})
    old = meta.get("schema_additions", "")
    new = (
        "passages[].tier (core_n5|late_n5|info_search), "
        "passages[].difficulty (easy|medium|hard — BUG-041 fix replaced legacy `level` field), "
        "passages[].format_type (info-search only: schedule_table|menu_list|notice), "
        "passages[].format_role (passage type: self_intro|narrative|info_search|comprehension|primary), "
        "passages[].questions[].format_role (primary|extra) — per-question priority. "
        "passages[].summary is JA-only (per BUG-042); summary_en for English (if extracted from legacy mixed-language entries); summary_hi for Hindi. "
        "passages[].vocab_preview is a list of vocab_id strings (per BUG-045 normalization)."
    )
    if old != new:
        meta["schema_additions"] = new
        return 1
    return 0


def fix_bug_044_format_type_comprehension(passages: list[dict]) -> int:
    """Remove format_type='comprehension' from passages where it duplicates
    format_role. format_role at passage level is the canonical type field.
    """
    n = 0
    for p in passages:
        if p.get("format_type") == "comprehension":
            del p["format_type"]
            p["bug_044_fix_2026_05_17"] = True
            n += 1
    return n


def fix_bug_045_vocab_preview(passages: list[dict]) -> int:
    """Normalize vocab_preview to list of vocab_id strings.

    For passages where vocab_preview is a list of dicts (Shape B),
    extract just the vocab_id from each dict.
    """
    n = 0
    for p in passages:
        vp = p.get("vocab_preview")
        if not isinstance(vp, list) or not vp:
            continue
        if all(isinstance(x, str) for x in vp):
            continue  # already Shape A
        # Shape B: list of dicts → extract vocab_id
        if all(isinstance(x, dict) for x in vp):
            new_vp = [x.get("vocab_id") for x in vp if x.get("vocab_id")]
            p["vocab_preview"] = new_vp
            p["bug_045_fix_2026_05_17"] = True
            n += 1
        else:
            print(f"  WARN: {p.get('id')} has mixed-shape vocab_preview; skipping")
    return n


def fix_bug_046_pronoun(passages: list[dict]) -> int:
    """Replace わたし → 私 in JA text. Update kanji_used to include 私."""
    n_passages_changed = 0
    n_replacements = 0
    for p in passages:
        ja = p.get("ja", "")
        if "わたし" not in ja:
            continue
        # Count and replace
        replacements_here = ja.count("わたし")
        new_ja = ja.replace("わたし", "私")
        p["ja"] = new_ja
        # Update kanji_used to include 私 if not already
        kanji_used = p.get("kanji_used") or []
        if "私" not in kanji_used:
            kanji_used.append("私")
            p["kanji_used"] = kanji_used
        p["bug_046_fix_2026_05_17"] = True
        n_passages_changed += 1
        n_replacements += replacements_here
    return n_passages_changed, n_replacements


def main() -> int:
    R = json.loads(READING.read_text(encoding="utf-8"))
    passages = R.get("passages", [])

    print(f"Loaded reading.json — {len(passages)} passages")

    print("\n--- BUG-041: level → difficulty ---")
    n = fix_bug_041_difficulty(passages)
    print(f"  Migrated {n} passages")

    print("\n--- BUG-042: summary → JA-only ---")
    n = fix_bug_042_summary(passages)
    print(f"  Normalized {n} passages (extracted JA title from mixed-lang summaries)")

    print("\n--- BUG-043: _meta.schema_additions update ---")
    n = fix_bug_043_meta_schema(R)
    print(f"  Updated schema_additions: {n}")

    print("\n--- BUG-044: remove format_type='comprehension' ---")
    n = fix_bug_044_format_type_comprehension(passages)
    print(f"  Removed format_type field from {n} passages")

    print("\n--- BUG-045: vocab_preview Shape B → Shape A ---")
    n = fix_bug_045_vocab_preview(passages)
    print(f"  Normalized {n} passages to Shape A (list of vocab_ids)")

    print("\n--- BUG-046: わたし → 私 ---")
    n_pass, n_repl = fix_bug_046_pronoun(passages)
    print(f"  Changed {n_pass} passages, {n_repl} total replacements")

    READING.write_text(json.dumps(R, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved {READING}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
