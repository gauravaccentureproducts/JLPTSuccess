"""Merge data/n5_deferred_to_n4.json into data/n5_core_pattern_ids.json.

Eliminates three-file drift risk on the deferred-to-N4 patterns. After
the merge:
- grammar.json carries tier='deferred_to_n4' per pattern (canonical)
- n5_core_pattern_ids.json#deferred_to_n4 carries the full attribution
  objects (rationale + sources_n5 + sources_n4)
- n5_deferred_to_n4.json is DELETED

JA-34 already accepts late_n5 as objects; needs a parallel update to
accept deferred_to_n4 as objects (currently expects flat strings).
"""
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CORE = ROOT / "data" / "n5_core_pattern_ids.json"
DEFER = ROOT / "data" / "n5_deferred_to_n4.json"


def main() -> None:
    core = json.loads(CORE.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    defer = json.loads(DEFER.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)

    # Promote the standalone file's pattern objects into the index file
    core["deferred_to_n4"] = defer["patterns"]

    # Update _meta doc to reflect schema parity with late_n5
    core["_meta"]["doc"] = (
        "ISSUE-033 (audit round-4) + ISSUE-005 + 2026-05-14 merge: explicit "
        "list of pattern IDs that are strictly within JLPT N5 scope (core_n5 "
        "— flat strings), borderline N5/N4 (late_n5 — array of objects with "
        "rationale + sources_n5 + sources_n4 per pattern), and deliberately-"
        "deferred-to-N4 (deferred_to_n4 — array of objects, SAME SHAPE as "
        "late_n5). The deferred patterns ship in grammar.json with "
        "tier='deferred_to_n4' — they remain accessible to learners but are "
        "flagged as N4-equivalent in the tier classification. "
        "Schema-merge 2026-05-14: standalone data/n5_deferred_to_n4.json was "
        "merged into this file to eliminate three-file drift risk; the index "
        "now carries the rationale + source attribution that previously lived "
        "in the standalone file."
    )

    CORE.write_text(json.dumps(core, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("merged: deferred_to_n4 field now carries object array")
    print(f"  count: {len(core['deferred_to_n4'])}")
    print(f"  shape: {type(core['deferred_to_n4'][0]).__name__} with keys {list(core['deferred_to_n4'][0].keys())}")

    DEFER.unlink()
    print(f"deleted: {DEFER}")


if __name__ == "__main__":
    main()
