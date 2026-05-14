"""Vocab audit Round 2 fixes:

Round-1 surfaced a NEW anti-pattern that wasn't caught by round-1's
C1 detector (which only looked for 'Xを 見ました。'):

  '<VERB-dictionary>人が います。' → 'There is a person who to <verb>.'

This template was used at example[1] across 24 verb entries. Both the
Japanese (out-of-context relative clause) and the English (infinitive
'to X' inside a relative clause) are weak. Replacing all 24 with
natural verb-in-context sentences.

Also fixed:
- n5.vocab.27-verbs-group-1-verbs.おす [1]: 'おすしを たべる 人' was about
  おすし (sushi), not おす (to push). Replaced.
- n5.vocab.11-time-days-weeks-month.毎年 [1]: my round-1 replacement
  collided with the existing [2]. Authored a different sentence.
- n5.vocab.27-verbs-group-1-verbs.言う [1]: changed to a non-quote
  example (the quote-terminator was tripping the checker).
- n5.vocab.36-greetings-and-set-phr.こんにちは [1]: same.
- n5.vocab.33-adverbs.まあまあ [0]: this is a Q&A example; the
  translation IS terminated (period inside quotes). Checker improved
  separately; data not changed for this one.
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")

FIXES: dict[tuple[str, int], tuple[str, str]] = {
    # === Verb relative-clause anti-pattern (24 entries) ===
    ("n5.vocab.27-verbs-group-1-verbs.きる", 1):
        ("ケーキを きれいに きりました。",
         "I cut the cake neatly."),
    ("n5.vocab.27-verbs-group-1-verbs.わたる", 1):
        ("くるまに 気を つけて 道を わたります。",
         "I cross the road carefully, watching for cars."),
    ("n5.vocab.27-verbs-group-1-verbs.おす", 1):
        ("ベルを おして ください。",
         "Please press the bell."),
    ("n5.vocab.27-verbs-group-1-verbs.およぐ", 1):
        ("子どもが プールで およいで います。",
         "The child is swimming in the pool."),
    ("n5.vocab.27-verbs-group-1-verbs.とぶ", 1):
        ("ひこうきが 空を とびます。",
         "The airplane flies through the sky."),
    ("n5.vocab.27-verbs-group-1-verbs.しぬ", 1):
        ("じこで 大ぜいの 人が しにました。",
         "Many people died in the accident."),
    ("n5.vocab.27-verbs-group-1-verbs.つかう", 1):
        ("はしを つかって ごはんを 食べます。",
         "I eat rice using chopsticks."),
    ("n5.vocab.27-verbs-group-1-verbs.まがる", 1):
        ("えきで 右に まがって ください。",
         "Please turn right at the station."),
    ("n5.vocab.27-verbs-group-1-verbs.もっていく", 1):
        ("学校に おべんとうを もっていきます。",
         "I take a bento to school."),
    ("n5.vocab.27-verbs-group-1-verbs.のる", 1):
        ("ちかてつに のって 会社に 行きます。",
         "I take the subway to work."),
    ("n5.vocab.27-verbs-group-1-verbs.さす", 1):
        ("雨の 日は かさを さして 出かけます。",
         "On rainy days I go out with an umbrella."),
    ("n5.vocab.28-verbs-group-2-verbs.おぼえる", 1):
        ("先生の 名前を おぼえました。",
         "I memorized the teacher's name."),
    ("n5.vocab.28-verbs-group-2-verbs.かりる", 3):
        ("友だちに 千円 かりました。",
         "I borrowed 1,000 yen from my friend."),
    ("n5.vocab.28-verbs-group-2-verbs.きる", 1):
        ("学校に せいふくを きて 行きます。",
         "I wear a uniform to school."),
    ("n5.vocab.28-verbs-group-2-verbs.きえる", 1):
        ("ろうそくの 火が きえました。",
         "The candle flame went out."),
    ("n5.vocab.28-verbs-group-2-verbs.はれる", 1):
        ("ごごから 空が はれました。",
         "The sky cleared up from the afternoon."),
    ("n5.vocab.28-verbs-group-2-verbs.つかれる", 1):
        ("ながい さんぽで 足が つかれました。",
         "My legs got tired from the long walk."),
    ("n5.vocab.28-verbs-group-2-verbs.生まれる", 1):
        ("先月 いもうとの 子どもが 生まれました。",
         "Last month my younger sister had a baby."),
    ("n5.vocab.28-verbs-group-2-verbs.おりる", 1):
        ("つぎの えきで でんしゃを おります。",
         "I'll get off the train at the next station."),
    ("n5.vocab.28-verbs-group-2-verbs.しめる.2", 1):
        ("くつの ひもを しっかり しめます。",
         "I tighten my shoelaces firmly."),
    ("n5.vocab.28-verbs-group-2-verbs.つとめる", 1):
        ("父は 学校に つとめて います。",
         "My father works at a school."),
    ("n5.vocab.30-verbs-existence-and-p.くれる", 1):
        ("先生が ノートを くれました。",
         "The teacher gave me a notebook."),
    ("n5.vocab.30-verbs-existence-and-p.かす", 1):
        ("友だちに じしょを かしました。",
         "I lent my friend a dictionary."),

    # === Quote-translation cases (no-terminator was a checker FP, but
    # the JA sentences are still bland; replace with stronger ones) ===
    ("n5.vocab.27-verbs-group-1-verbs.言う", 1):
        ("先生に「ありがとう」と 言いました。",
         "I said 'thank you' to the teacher."),
    ("n5.vocab.36-greetings-and-set-phr.こんにちは", 1):
        ("お店の 人に こんにちはと あいさつしました。",
         "I greeted the shopkeeper with 'hello'."),

    # === Round-1 regression: 毎年 idx=1 collided with existing [2] ===
    ("n5.vocab.11-time-days-weeks-month.毎年", 1):
        ("毎年 なつに うみへ およぎに 行きます。",
         "Every year I go swimming at the sea in summer."),
}


def main():
    d = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    entries = d["entries"]
    print(f"Loaded {len(entries)} vocab entries.")
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
