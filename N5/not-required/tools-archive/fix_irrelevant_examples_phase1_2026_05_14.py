"""Phase 1 fix for irrelevant grammar examples flagged in
audit_grammar_example_relevance_2026_05_14.py.

Replaces 28 boilerplate / off-pattern examples across 15 particle and
ko-so-a-do patterns with newly-authored examples that demonstrate the
target marker. Each replacement preserves the `form` tag; vocab_ids
and pitch_marks are cleared (the renderer handles their absence —
they can be re-tagged in a future content-enrichment pass).

The 14 boilerplate sentences this fix evicts:
  "わたしは がくせいです。"  (was repeated across 14 patterns)
  "私は 学生です。"            (9 patterns)
  "じぶんで しゅくだいを します。" (14 patterns)
  "あにより わたしのほうが はやく おきます。" (14 patterns)
  "父に とけいを もらいました。" (11 patterns)
  "母と えいがを 見ました。"   (9 patterns)
  "いもうとは 学校に 行きます。" (10 patterns)
  "あなたは どなたですか。"   (18 patterns)
  "あなたは がくせいですか。" (21 patterns)
(plus a few more that survive in OTHER patterns where they are
relevant; this fix only removes the irrelevant occurrences.)

Phase 2 (deferred — surface to user): the broader sweep across the
remaining ~157 boilerplate-leak entries, requiring per-pattern
authoring decisions.

Run:
  python -X utf8 not-required/tools-archive/fix_irrelevant_examples_phase1_2026_05_14.py
"""
import json
from collections import OrderedDict
from pathlib import Path

GRAMMAR = Path("data/grammar.json")

# Map of (pattern_id, example_index) -> (new_ja, new_translation_en).
# Form tags are preserved from the existing example (not overwritten).
REPLACEMENTS = {
    # n5-003 — が (subject / want / preference / existence)
    ("n5-003", 5): ("いぬが ほしいです。", "I want a dog."),

    # n5-004 — を (direct-object marker)
    ("n5-004", 6): ("日本語を べんきょうします。", "I study Japanese."),

    # n5-005 — に (location of existence / time / recipient)
    ("n5-005", 5): ("ねこは いすに います。", "The cat is on the chair."),
    ("n5-005", 6): ("父に てがみを かきます。", "I write a letter to my father."),

    # n5-006 — へ (direction)
    ("n5-006", 4): ("こうえんへ あるきます。", "I walk to the park."),
    ("n5-006", 5): ("ともだちは アメリカへ いきます。", "My friend goes to America."),
    ("n5-006", 6): ("ぎんこうへ いきます。", "I go to the bank."),

    # n5-007 — で (means / location-of-action / instrument)
    ("n5-007", 6): ("日本語で 話します。", "I speak in Japanese."),

    # n5-008 — と (with / and / quotation)
    ("n5-008", 5): ("ねこと あそびます。", "I play with the cat."),
    ("n5-008", 6): ("あにと すしを たべました。", "I ate sushi with my older brother."),

    # n5-009 — から (from / since)
    ("n5-009", 5): ("あさ 7時から はたらきます。", "I work from 7 AM in the morning."),
    ("n5-009", 6): ("あさから あめです。", "It has been rainy since morning."),

    # n5-010 — まで (until / as far as)
    ("n5-010", 5): ("あしたまで まちます。", "I will wait until tomorrow."),
    ("n5-010", 6): ("土曜日まで 学校が あります。", "I have school until Saturday."),

    # n5-011 — や (non-exhaustive listing)
    ("n5-011", 4): ("あさ パンや たまごを たべます。", "In the morning I eat bread, eggs, etc."),
    ("n5-011", 5): ("アメリカや 日本へ いきました。", "I went to America, Japan, and other places."),
    ("n5-011", 6): ("きのう ぎゅうにくや さかなを たべました。", "Yesterday I ate beef, fish, and so on."),

    # n5-013 — も (also / too)
    ("n5-013", 5): ("これも わたしの ほんです。", "This is also my book."),
    ("n5-013", 6): ("父も 母も げんきです。", "Both my father and mother are well."),

    # n5-014 — これ／それ／あれ／どれ (this/that/that-over-there/which)
    ("n5-014", 5): ("それは わたしの かさです。", "That is my umbrella."),
    ("n5-014", 6): ("これは 父の しゃしんです。", "This is my father's photograph."),

    # n5-015 — この／その／あの／どの + N (modifier demonstratives)
    ("n5-015", 5): ("あの ねこは どこから 来ましたか。", "Where did that cat come from?"),
    ("n5-015", 6): ("どの えいがを 見ますか。", "Which movie will you watch?"),

    # n5-016 — ここ／そこ／あそこ／どこ (here/there/over-there/where)
    ("n5-016", 5): ("ここで まちます。", "I will wait here."),
    ("n5-016", 6): ("ホテルは あそこです。", "The hotel is over there."),

    # n5-018 — だれ／どなた (who / who-polite)
    ("n5-018", 6): ("あの 女の人は どなたですか。", "Who is that woman?"),

    # n5-019 — いつ (when)
    ("n5-019", 5): ("テストは いつですか。", "When is the test?"),
    ("n5-019", 6): ("いつ ひるごはんを たべますか。", "When do you eat lunch?"),
}


def main() -> None:
    d = json.loads(GRAMMAR.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    patterns = d.get("patterns", [])

    applied = []
    missing = []
    for (pid, idx), (new_ja, new_en) in REPLACEMENTS.items():
        target = None
        for p in patterns:
            if p.get("id") == pid:
                target = p
                break
        if target is None:
            missing.append((pid, idx, "pattern-not-found"))
            continue
        examples = target.get("examples", [])
        if idx >= len(examples):
            missing.append((pid, idx, f"index-out-of-range (have {len(examples)})"))
            continue
        ex = examples[idx]
        old_ja = ex.get("ja", "")
        ex["ja"] = new_ja
        ex["translation_en"] = new_en
        # Clear vocab_ids and pitch_marks — they were tagged for the OLD
        # sentence and would point at the wrong words now. A future content-
        # enrichment pass will re-tag from the new ja.
        if "vocab_ids" in ex:
            ex["vocab_ids"] = []
        if "pitch_marks" in ex:
            ex["pitch_marks"] = []
        applied.append((pid, idx, old_ja, new_ja))

    GRAMMAR.write_text(
        json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Replacements applied: {len(applied)}/{len(REPLACEMENTS)}")
    print()
    for pid, idx, old_ja, new_ja in applied:
        print(f"  {pid}[{idx}]")
        print(f"    BEFORE: {old_ja}")
        print(f"    AFTER:  {new_ja}")
    if missing:
        print()
        print(f"MISSING (not applied):")
        for pid, idx, reason in missing:
            print(f"  {pid}[{idx}]: {reason}")


if __name__ == "__main__":
    main()
