"""Fix BUG-023 — restore kanji forms to 5 vocab.json entries whose
form fields were stored kana-only despite the kanji being in the
N5 whitelist.

This is the inverse of BUG-017 / BUG-020:
  - BUG-017 / BUG-020 case: vocab/kanji.json showed forms with
    OOS kanji (末, 籍) → fix was to switch to kana / remove the
    compound.
  - BUG-023 case: vocab.json showed kana-only forms even though
    all kanji are in N5 whitelist → fix is to restore the kanji
    form (kanji.json had it right; vocab.json was the laggard).

Affected (form changes; reading and id unchanged):
  ともだち → 友だち         (kanji 友 is N5; だち as okurigana kana,
                              avoiding N4 kanji 達 per scope rule)
  て        → 手             (kanji 手 is N5)
  じょうず → 上手             (kanji 上, 手 are N5)
  あし      → 足             (kanji 足 is N5)
  め        → 目             (kanji 目 is N5)

ID stability: vocab IDs already encode the kana suffix
(n5.vocab.<section>.<form-original>) so cross-corpus references
continue to resolve. The kanji.json compounds for these 5 already
use the kanji forms with these vocab_ids — they will now match
exactly after this fix.

CI invariant JA-100 is being tightened in the same commit to a
strict form-match check (catches both directions of drift
automatically going forward).
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "vocab.json"

# (vocab_id, current_kana_form, new_kanji_form)
RENAMES = [
    ("n5.vocab.2-people-family.ともだち",    "ともだち", "友だち"),
    ("n5.vocab.4-body-parts.て",              "て",       "手"),
    ("n5.vocab.32-adjectives.じょうず",       "じょうず", "上手"),
    ("n5.vocab.4-body-parts.あし",            "あし",     "足"),
    ("n5.vocab.4-body-parts.め",              "め",       "目"),
]


def main() -> int:
    V = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = V.get("entries", [])
    by_id = {e.get("id"): e for e in entries if e.get("id")}

    updated = 0
    errors: list[str] = []
    for vid, old_form, new_form in RENAMES:
        entry = by_id.get(vid)
        if not entry:
            errors.append(f"{vid}: not found")
            continue
        cur = entry.get("form")
        if cur != old_form:
            errors.append(f"{vid}: current form {cur!r} != expected {old_form!r}")
            continue
        entry["form"] = new_form
        entry["form_was_kana_pre_bug_023"] = old_form
        entry["bug_023_fix_2026_05_17"] = True
        updated += 1
        print(f"  {vid}: form {old_form!r} → {new_form!r}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e}")
        return 1

    VOCAB.write_text(json.dumps(V, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nUpdated {updated} entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
