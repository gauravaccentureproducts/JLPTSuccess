"""Native-teacher audit fix pass — 13 findings from the 2026-05-14
language-accuracy audit on data/grammar.json.

Split into:
- 7 CRITICAL fixes: off-pattern content replacement
- 7 MAJOR fixes:    form-tag-value corrections (content stays)
- 3 MEDIUM/MINOR fixes: duplicate-concept replacement + translation tweaks

(13 unique example slots — one slot got both content AND form-tag fix
counted once.)
"""
import json
from collections import OrderedDict
from pathlib import Path

GRAMMAR = Path("data/grammar.json")

# ===== CRITICAL — off-pattern content replacements (ja + translation_en) =====
CONTENT_FIXES = {
    # n5-125 では/じゃ — [5][6] previously had pure-past sentences unrelated to では/じゃ
    ("n5-125", 5): ("では、しごとは おわりました。", "Well then, work is done."),
    ("n5-125", 6): ("これは わたしの ペンじゃ ありませんでした。", "This wasn't my pen."),

    # n5-129 どうして〜か。〜から。 — [4][5][6] previously had irrelevant copula sentences
    ("n5-129", 4): (
        "どうして 日本語を べんきょうしますか。 すきだからです。",
        "Why do you study Japanese? Because I like it.",
    ),
    ("n5-129", 5): (
        "どうして うちに かえりますか。 つかれたからです。",
        "Why are you going home? Because I'm tired.",
    ),
    ("n5-129", 6): (
        "どうして かいませんでしたか。 たかかったからです。",
        "Why didn't you buy it? Because it was expensive.",
    ),

    # n5-174 〜なくてはならない — [4][6] previously had unrelated content
    ("n5-174", 4): (
        "あした はやく おきなくては なりませんか。",
        "Do I have to wake up early tomorrow?",
    ),
    ("n5-174", 6): (
        "あさごはんを たべなくては なりません。",
        "I have to eat breakfast.",
    ),

    # MEDIUM — n5-097 coffee/tea triple — replace [4] and [7] with diverse pairings
    ("n5-097", 4): (
        "りんごと バナナと、どちらが おいしいですか。",
        "Apple or banana, which is more delicious?",
    ),
    ("n5-097", 7): (
        "あさと よると、どちらが いいですか。",
        "Morning or evening, which is better?",
    ),
}

# ===== MAJOR — form-tag-value corrections (content stays, only the form value changes) =====
FORM_FIXES = {
    ("n5-030", 3): "affirmative",   # was "negative" but content is affirmative
    ("n5-031", 4): "question",      # was "affirmative" but content is informal-question ending in の？
    ("n5-031", 5): "question",      # same
    ("n5-031", 6): "question",      # same
    ("n5-097", 2): "question",      # was "affirmative" but content ends in ですか
    ("n5-125", 4): "negative",      # was "past" but content is present-negative (じゃ ありません)
    ("n5-185", 4): "affirmative",   # was "question" but content is an affirmative statement
    ("n5-001", 4): "habitual",      # to match [9] form="habitual" — both are habitual まいにち sentences
}

# ===== MINOR — translation polish =====
TRANSLATION_FIXES = {
    ("n5-005", 5): "The cat is on/by the chair.",
    ("n5-129", 9): "Why are you hurrying? Because it's getting late.",
}


def main() -> None:
    d = json.loads(GRAMMAR.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)

    applied_content = 0
    applied_form = 0
    applied_trans = 0
    missing = []

    for (pid, idx), (new_ja, new_en) in CONTENT_FIXES.items():
        for p in d["patterns"]:
            if p["id"] == pid:
                if idx >= len(p.get("examples", [])):
                    missing.append((pid, idx, "out-of-range"))
                    break
                ex = p["examples"][idx]
                ex["ja"] = new_ja
                ex["translation_en"] = new_en
                if "vocab_ids" in ex:
                    ex["vocab_ids"] = []
                if "pitch_marks" in ex:
                    ex["pitch_marks"] = []
                applied_content += 1
                break

    for (pid, idx), new_form in FORM_FIXES.items():
        for p in d["patterns"]:
            if p["id"] == pid:
                if idx >= len(p.get("examples", [])):
                    missing.append((pid, idx, "out-of-range"))
                    break
                ex = p["examples"][idx]
                ex["form"] = new_form
                applied_form += 1
                break

    for (pid, idx), new_en in TRANSLATION_FIXES.items():
        for p in d["patterns"]:
            if p["id"] == pid:
                if idx >= len(p.get("examples", [])):
                    missing.append((pid, idx, "out-of-range"))
                    break
                p["examples"][idx]["translation_en"] = new_en
                applied_trans += 1
                break

    GRAMMAR.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Native-audit fixes applied:")
    print(f"  CRITICAL content fixes:    {applied_content}/{len(CONTENT_FIXES)}")
    print(f"  MAJOR form-tag fixes:      {applied_form}/{len(FORM_FIXES)}")
    print(f"  MINOR translation tweaks:  {applied_trans}/{len(TRANSLATION_FIXES)}")
    if missing:
        print(f"\nMISSING: {missing}")


if __name__ == "__main__":
    main()
