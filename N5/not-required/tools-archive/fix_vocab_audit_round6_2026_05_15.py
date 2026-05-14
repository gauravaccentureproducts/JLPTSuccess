"""Round-6: diversify C4 cross-entry boilerplate.

For each of the 5 over-reused sentences (used ≥5× across vocab entries),
keep the use(s) where the entry's headword is genuinely demonstrated,
replace the use(s) where the sentence is just templated filler.

Net effect: each of the 5 sentences ends up used <5 times. 14 fixes.
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")

FIXES = {
    # === "わたしは がくせいです。" (5→3) ===
    # KEEP: 私 (pronoun), 学生 (student), particle は (topic marker)
    # REPLACE: tooth は, height せ (wrong content)
    ("n5.vocab.4-body-parts.は", 1):
        ("毎日 はを みがいて います。",
         "I brush my teeth every day."),
    ("n5.vocab.4-body-parts.せ", 1):
        ("あには 私より せが 高いです。",
         "My older brother is taller than me."),

    # === "あの 人は だれですか。" (5→3) ===
    # KEEP: 人 (person), だれ (who), demonstrative あの
    # REPLACE: counter 人, filler あの
    ("n5.vocab.9-counters-common.人", 1):
        ("クラスは 二十人 います。",
         "There are 20 people in the class."),
    ("n5.vocab.39-function-filler-expre.あの", 1):
        ("あの…ちょっと いいですか。",
         "Um... do you have a moment?"),

    # === "あついから、まどを あけてください。" (8→4) ===
    # KEEP: 14-nature あつい (hot weather), まど, conj から, 31-adj あつい (hot weather)
    # REPLACE: て (hand — wrong), あく (intransitive — wrong),
    #          あつい.2 (hot-touch), あつい.3 (thick)
    ("n5.vocab.4-body-parts.て", 1):
        ("ごはんの 前に てを あらいます。",
         "I wash my hands before meals."),
    ("n5.vocab.27-verbs-group-1-verbs.あく", 1):
        ("かぜで まどが ひとりでに あきました。",
         "The window opened by itself in the wind."),
    ("n5.vocab.31-adjectives.あつい.2", 1):
        ("おちゃが あつくて 飲めません。",
         "The tea is too hot to drink."),
    ("n5.vocab.31-adjectives.あつい.3", 1):
        ("この 本は あつくて おもいです。",
         "This book is thick and heavy."),

    # === "まいにち にほんごを べんきょうします。" (7→2) ===
    # KEEP: べんきょう (study), particle を (object marker)
    # REPLACE: 二, 五, まい counter, 本 counter, 今日
    ("n5.vocab.7-numbers.二", 1):
        ("にもつが 二つ あります。",
         "There are two pieces of luggage."),
    ("n5.vocab.7-numbers.五", 1):
        ("くだものを 五つ ください。",
         "Please give me five pieces of fruit."),
    ("n5.vocab.9-counters-common.まい", 1):
        ("白い かみを 三まい ください。",
         "Please give me three sheets of white paper."),
    ("n5.vocab.9-counters-common.本", 1):
        ("ペンを 二本 買いました。",
         "I bought two pens."),
    ("n5.vocab.10-time-general.今日", 1):
        ("今日は 友だちに 会います。",
         "I'll meet a friend today."),

    # === "コーヒーは 飲みますが、にくは たべません。" (5→4) ===
    # KEEP: にく, コーヒー, 飲む, 食べる
    # REPLACE: particle が (contrastive use, not subject)
    ("n5.vocab.35-particles-functional-.が", 1):
        ("つくえの 上に 本が あります。",
         "There is a book on the desk."),
}


def main():
    d = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    entries = d["entries"]
    applied = 0
    missing = []
    for (eid, idx), (new_ja, new_en) in FIXES.items():
        target = None
        for e in entries:
            if e.get("id") == eid:
                target = e
                break
        if target is None:
            missing.append((eid, idx, "entry-not-found"))
            continue
        exs = target.get("examples", [])
        if idx >= len(exs):
            missing.append((eid, idx, f"idx-out-of-range ({len(exs)})"))
            continue
        exs[idx]["ja"] = new_ja
        exs[idx]["translation_en"] = new_en
        applied += 1
    print(f"Applied: {applied}/{len(FIXES)}")
    for m in missing:
        print(f"  MISSING: {m}")
    VOCAB.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
