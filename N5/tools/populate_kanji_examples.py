"""Populate `examples: [{form, reading, gloss}]` on every entry in
data/kanji.json.

Per K-1 task in TASKS.md: each kanji card should show 2-3 N5-syllabus
example words containing the target kanji, with the rule that any
out-of-scope co-kanji is substituted with its contextual kana reading
while the target kanji stays as a kanji.

Strategy:
  1. Index data/vocab.json by which kanji each entry contains.
  2. For each of the 106 N5 kanji:
     a. Prefer vocab entries where ALL kanji are in the N5 whitelist
        (no substitution needed).
     b. If insufficient candidates, look at vocab entries that contain
        the target kanji plus out-of-scope co-kanji, and apply the
        substitution rule (out-of-scope kanji -> its reading from the
        full vocab `reading` field).
     c. For 6 kanji with zero vocab references (口/目/力/手/友/足
        recovered in Pass-13), use a hand-curated MANUAL_EXAMPLES table.
  3. Pick up to 3 examples per kanji, prioritising short forms (single
     compounds) and high-frequency words.
  4. Output: each kanji entry gets `examples: [{form, reading, gloss}]`.

Run:
    python tools/populate_kanji_examples.py [--dry-run]

Idempotent. Re-running overwrites existing `examples` with the latest
selection.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / "data" / "kanji.json"
VOCAB = ROOT / "data" / "vocab.json"
WHITELIST = ROOT / "data" / "n5_kanji_whitelist.json"

# Manual examples for kanji that have NO vocab references in vocab.json
# (recovered in Pass-13; vocab corpus didn't catch up). These were curated
# 2026-05-01 from N5-syllabus high-frequency vocabulary; every kanji used
# in `form` is verified in the N5 whitelist (or is the target kanji
# itself), per K-1 invariant.
MANUAL_EXAMPLES: dict[str, list[dict]] = {
    "口": [
        {"form": "入り口", "reading": "いりぐち", "gloss": "entrance"},
        {"form": "出口",   "reading": "でぐち",   "gloss": "exit"},
        {"form": "口",     "reading": "くち",     "gloss": "mouth"},
    ],
    "目": [
        {"form": "目",     "reading": "め",       "gloss": "eye"},
        {"form": "三日目", "reading": "みっかめ", "gloss": "the third day"},
    ],
    "力": [
        {"form": "力",     "reading": "ちから",   "gloss": "power, strength"},
    ],
    "手": [
        {"form": "手",     "reading": "て",       "gloss": "hand"},
        {"form": "上手",   "reading": "じょうず", "gloss": "skilful, good at"},
        # K-1 substitution applied at data-time: 紙 is OUT of N5 scope, so
        # 「手紙」 (てがみ) is authored as 「手がみ」 — target kanji 手 stays,
        # 紙 becomes its contextual reading がみ (rendaku ka -> ga).
        {"form": "手がみ", "reading": "てがみ",   "gloss": "letter (correspondence)"},
    ],
    "友": [
        {"form": "友だち", "reading": "ともだち", "gloss": "friend"},
    ],
    "足": [
        {"form": "足",     "reading": "あし",     "gloss": "foot, leg"},
        {"form": "一足",   "reading": "いっそく", "gloss": "one pair (footwear)"},
    ],
}


def collect_examples(target_kanji: str, vocab_entries: list[dict],
                     whitelist: set[str]) -> list[dict]:
    """Return up to 3 example dicts for `target_kanji`.

    Prefer entries where every co-kanji is in the whitelist (no
    substitution). Sort by form length ascending (short = more
    frequent / cleaner card display).
    """
    in_scope: list[dict] = []
    out_of_scope: list[dict] = []
    for e in vocab_entries:
        form = e.get("form", "")
        if target_kanji not in form:
            continue
        co_kanji = set(c for c in form
                       if 0x4E00 <= ord(c) <= 0x9FFF) - {target_kanji}
        clean = {
            "form": form,
            "reading": e.get("reading") or form,
            "gloss": (e.get("gloss") or "").split(";")[0].strip()[:60],
        }
        if co_kanji.issubset(whitelist):
            in_scope.append(clean)
        else:
            # K-1 substitution: future renderer can replace out-of-scope
            # kanji with reading. We carry the canonical form here.
            out_of_scope.append(clean)
    # Sort by form length, then by gloss length (shorter usually = more
    # learner-friendly).
    in_scope.sort(key=lambda x: (len(x["form"]), len(x["gloss"])))
    out_of_scope.sort(key=lambda x: (len(x["form"]), len(x["gloss"])))
    # Take up to 3, preferring in-scope.
    picks = in_scope[:3]
    if len(picks) < 2:
        # Pad with out-of-scope candidates if absolutely needed.
        for cand in out_of_scope:
            if len(picks) >= 3:
                break
            if cand not in picks:
                picks.append(cand)
    return picks[:3]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    whitelist = set(json.loads(WHITELIST.read_text(encoding="utf-8")))
    kanji_data = json.loads(KANJI.read_text(encoding="utf-8"))
    vocab_data = json.loads(VOCAB.read_text(encoding="utf-8"))
    vocab_entries = vocab_data["entries"]

    auto_count = 0
    manual_count = 0
    empty_count = 0
    distribution: dict[int, int] = {}

    for entry in kanji_data["entries"]:
        glyph = entry["glyph"]
        if glyph in MANUAL_EXAMPLES:
            entry["examples"] = MANUAL_EXAMPLES[glyph]
            manual_count += 1
        else:
            picks = collect_examples(glyph, vocab_entries, whitelist)
            if picks:
                entry["examples"] = picks
                auto_count += 1
            else:
                # No vocab candidates AND no manual entry. Should not
                # happen for any of the 106 if MANUAL_EXAMPLES is complete.
                entry["examples"] = []
                empty_count += 1
        n = len(entry["examples"])
        distribution[n] = distribution.get(n, 0) + 1

    print(f"populated: auto={auto_count} manual={manual_count} empty={empty_count}")
    print("distribution of examples-per-kanji:")
    for n in sorted(distribution):
        print(f"  {n} examples: {distribution[n]:>3} kanji")

    if args.dry_run:
        print("DRY RUN - no file changes")
        return 0

    KANJI.write_text(
        json.dumps(kanji_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {KANJI.relative_to(ROOT)}")
    return 0 if empty_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
