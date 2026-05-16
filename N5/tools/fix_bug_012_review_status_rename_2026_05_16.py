"""Fix BUG-012 — rename review_status from `native_reviewed` to
`ai_quality_reviewed` and add `review_status_provenance` field.

Background:
  All ~1846 content items across 7 corpora carry
  `review_status: "native_reviewed"`. The _meta block discloses that
  the label was assigned by Claude acting as a native-reviewer
  persona — not by an actual native human Japanese teacher. But the
  per-item label, read in isolation by downstream tooling / UI badge
  surfaces / third-party adopters, implies human-native review.

  BUG-003 (n5-098 with 10/10 wrong translations) proved the label
  was unreliable on at least one pattern that carried it. Until a
  real native-human review pass happens, the label needs to
  disambiguate at the point of use, not just in _meta.

Per BUG-012's preferred fix (Option B):
  - Rename the field value: native_reviewed → ai_quality_reviewed
  - Add `review_status_provenance: "claude_native_reviewer_persona"`
    alongside (machine-readable signal of who/what did the review)
  - Update JA-35 CI invariant's closed enum
  - Update js/provenance-badge.js label text + check

Scope:
  - data/grammar.json (178), data/vocab.json (1009),
    data/kanji.json (106), data/reading.json (54),
    data/listening.json (50), data/authentic.json (100 of 188),
    data/questions.json (261). Total ~1758 entries to rename.
  - Other values (llm_curated, auto_generated) are unchanged.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# (file path, top-level key holding the items list)
TARGETS = [
    ("data/grammar.json", "patterns"),
    ("data/vocab.json", "entries"),
    ("data/kanji.json", "entries"),
    ("data/reading.json", "passages"),
    ("data/listening.json", "items"),
    ("data/authentic.json", "items"),
    ("data/questions.json", "questions"),
]

OLD_VALUE = "native_reviewed"
NEW_VALUE = "ai_quality_reviewed"
PROVENANCE_FIELD = "review_status_provenance"
PROVENANCE_VALUE = "claude_native_reviewer_persona"


def detect_items_key(d: dict) -> str | None:
    """Find the top-level key holding the items list. Used when the
    expected key (per TARGETS) isn't present."""
    for k in ("patterns", "entries", "passages", "items", "questions"):
        if isinstance(d.get(k), list):
            return k
    return None


def main() -> int:
    total_renamed = 0
    total_skipped = 0
    errors: list[str] = []

    for rel_path, expected_key in TARGETS:
        fpath = ROOT / rel_path
        if not fpath.exists():
            errors.append(f"{rel_path}: file not found")
            continue
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{rel_path}: JSON decode error — {e}")
            continue

        # Use expected_key if present; else auto-detect.
        key = expected_key if expected_key in data else detect_items_key(data)
        if not key:
            errors.append(f"{rel_path}: no items list found (tried {expected_key!r})")
            continue

        items = data[key]
        renamed = 0
        skipped = 0
        for item in items:
            if not isinstance(item, dict):
                continue
            rs = item.get("review_status")
            if rs == OLD_VALUE:
                item["review_status"] = NEW_VALUE
                if PROVENANCE_FIELD not in item:
                    item[PROVENANCE_FIELD] = PROVENANCE_VALUE
                renamed += 1
            elif rs == NEW_VALUE:
                # Already migrated; ensure provenance is set.
                if PROVENANCE_FIELD not in item:
                    item[PROVENANCE_FIELD] = PROVENANCE_VALUE
                    renamed += 1
                else:
                    skipped += 1
            # else: rs is llm_curated / auto_generated / missing — leave alone

        # Also update _meta disclosure if present
        if isinstance(data.get("_meta"), dict):
            meta = data["_meta"]
            if "review_status_note" not in meta:
                meta["review_status_note"] = (
                    "review_status='ai_quality_reviewed' means: Claude (LLM) "
                    "applied a native-reviewer persona during corpus authoring. "
                    "Not equivalent to review by a human native Japanese teacher. "
                    "See review_status_provenance for the specific signal. A "
                    "future human-native review pass is queued; BUG-012 fix "
                    "renames the field from 'native_reviewed' to make the AI "
                    "origin visible at the point of use."
                )

        fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        total_renamed += renamed
        total_skipped += skipped
        print(f"  {rel_path}: renamed {renamed}, skipped {skipped} (already migrated)")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e}")
        return 1

    print(
        f"\nSummary: {total_renamed} entries renamed to {NEW_VALUE!r} + provenance added; "
        f"{total_skipped} skipped (already complete)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
