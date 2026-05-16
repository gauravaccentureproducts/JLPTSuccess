"""Fix BUG-021 — primary_reading set to on-yomi for 6 kanji whose
N5 standalone usage is the kun-yomi.

For these kanji, the on-yomi appears only as a suffix/prefix in
compounds, while the standalone-in-sentence form a learner first
encounters uses the kun-yomi. Flip primary_reading to the kun-yomi.

  人: にん → ひと   (にん = counter suffix; standalone 人 = ひと)
  中: ちゅう → なか (ちゅう = prefix/suffix; standalone 中 = なか)
  外: がい → そと   (がい = prefix; standalone 外 = そと)
  東: とう → ひがし (とう = prefix; standalone 東 = ひがし)
  車: しゃ → くるま (しゃ = suffix; standalone 車 = くるま)
  国: こく → くに   (こく = prefix; standalone 国 = くに)

The on-yomi remains in the `on` array and audio_yomi map; this
change only affects which reading is presented as the canonical
association on the kanji card.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / "data" / "kanji.json"

REASSIGNMENTS = {
    "人": ("にん", "ひと"),
    "中": ("ちゅう", "なか"),
    "外": ("がい", "そと"),
    "東": ("とう", "ひがし"),
    "車": ("しゃ", "くるま"),
    "国": ("こく", "くに"),
}


def main() -> int:
    K = json.loads(KANJI.read_text(encoding="utf-8"))
    entries = K.get("entries", [])
    updated = 0
    for glyph, (old_pr, new_pr) in REASSIGNMENTS.items():
        entry = next((e for e in entries if e.get("glyph") == glyph), None)
        if not entry:
            print(f"  ERROR: kanji {glyph} not found")
            return 1
        current = entry.get("primary_reading")
        if current != old_pr:
            print(f"  WARN: {glyph} primary_reading is {current!r}, expected {old_pr!r}; skipping")
            continue
        # Verify the new reading exists in the kun list
        kun = entry.get("kun") or []
        # Kun-yomi entries may have ".suffix" markers (e.g., "ひと.り") — match prefix
        matched = any(k.split(".")[0] == new_pr or k == new_pr for k in kun)
        if not matched:
            print(f"  WARN: {glyph} new reading {new_pr!r} not in kun list {kun!r}; will set anyway")
        entry["primary_reading"] = new_pr
        entry["primary_reading_provenance"] = "bug_021_fix_2026_05_17_kun_standalone_use"
        entry["primary_reading_was_on_yomi_pre_bug_021"] = old_pr
        updated += 1
        print(f"  {glyph}: primary_reading {old_pr!r} → {new_pr!r}")

    KANJI.write_text(json.dumps(K, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nUpdated {updated} entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
