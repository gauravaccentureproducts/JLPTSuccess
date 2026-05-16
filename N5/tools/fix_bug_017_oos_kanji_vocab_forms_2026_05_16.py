"""Fix BUG-017 — 3 kanji used in vocab forms are not in the N5 whitelist
(倍, 籍, 末). Replace the kanji forms with kana per the bug's
recommended path.

Affected entries (form / reading / new form):
  倍   / ばい    → ばい
  国籍 / こくせき → こくせき
  週末 / しゅうまつ → しゅうまつ

Stability: vocab IDs are NOT changed (form-keyed string `n5.vocab.
<section>.<form>` stays as the original). The ID is a stable
identifier referenced from data/drills_auto.json, data/kanji.json,
and possibly other corpora; renaming would cascade. Display `form`
diverges from the ID for these 3 entries, which is acceptable —
form is display, ID is identity.

Within-entry references in `examples[].ja` are scanned and rewritten:
any "二倍" / "国籍" / "週末" substring inside an example's JA text gets
swapped to its kana equivalent. (Other corpora's references to the
vocab ID continue to work unchanged.)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "vocab.json"

# (current_form, new_form, kana_reading, example_substitutions)
# Each subst is (find, replace) applied to every example.ja in the entry.
RENAMES = [
    ("倍",   "ばい",     "ばい",     [("二倍", "二ばい")]),
    ("国籍", "こくせき", "こくせき", [("国籍", "こくせき")]),
    ("週末", "しゅうまつ", "しゅうまつ", [("週末", "しゅうまつ")]),
]


def main() -> int:
    V = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = V.get("entries", [])

    updated = 0
    example_edits = 0
    for old_form, new_form, reading, substs in RENAMES:
        for e in entries:
            if e.get("form") != old_form:
                continue
            # Rename form
            e["form"] = new_form
            # Reading was already kana; confirm
            if e.get("reading") != reading:
                # Reading already matched the kana form per the survey;
                # just normalize.
                e["reading"] = reading
            # Mark provenance
            e["bug_017_fix_2026_05_16"] = True
            # Rewrite any JA examples that still contain the OOS kanji
            for ex in e.get("examples") or []:
                if not isinstance(ex, dict):
                    continue
                ja = ex.get("ja") or ""
                new_ja = ja
                for find, replace in substs:
                    new_ja = new_ja.replace(find, replace)
                if new_ja != ja:
                    ex["ja"] = new_ja
                    example_edits += 1
                    print(f"  {old_form} ({e.get('id','?')}) ex: {ja!r} -> {new_ja!r}")
            # Also rewrite collocations if they contain OOS kanji
            new_cols = []
            for c in (e.get("collocations") or []):
                if isinstance(c, str):
                    new_c = c
                    for find, replace in substs:
                        new_c = new_c.replace(find, replace)
                    new_cols.append(new_c)
                else:
                    new_cols.append(c)
            e["collocations"] = new_cols
            updated += 1
            print(f"  form: {old_form!r} -> {new_form!r} ({e.get('id','?')})")

    VOCAB.write_text(json.dumps(V, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nUpdated {updated} entries, {example_edits} in-entry example substitutions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
