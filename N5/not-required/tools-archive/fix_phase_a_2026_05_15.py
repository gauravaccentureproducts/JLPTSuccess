"""Phase A fixes — counter-noun pedagogy issues.

The native-counter-series entries 三つ through 九つ each had
「本が Xつ あります。」 at example[1]. Pedagogically suboptimal:
books canonically take the dedicated counter 冊 (一冊、二冊…),
not the general native counter つ. While the sentence is technically
grammatical, a native Japanese teacher would replace 本 with a noun
that's CANONICALLY in the つ-counter set (round / general 3D objects)
so the example demonstrates the right pairing.

Replacement nouns chosen to:
  1. Pair canonically with つ
  2. Not duplicate other examples in the same entry
  3. Use only N5 kanji or kana (N5 whitelist safe)
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")

FIXES = {
    ("n5.vocab.8-native-counters-series.三つ", 1):
        ("ボールが 三つ あります。", "There are three balls."),
    ("n5.vocab.8-native-counters-series.四つ", 1):
        ("コップが 四つ あります。", "There are four cups."),
    ("n5.vocab.8-native-counters-series.六つ", 1):
        ("はこが 六つ あります。", "There are six boxes."),
    ("n5.vocab.8-native-counters-series.七つ", 1):
        ("いえの まえに 木が 七つ あります。",
         "There are seven trees in front of the house."),
    ("n5.vocab.8-native-counters-series.八つ", 1):
        ("ふくろが 八つ あります。", "There are eight bags."),
    ("n5.vocab.8-native-counters-series.九つ", 1):
        ("いすが 九つ あります。", "There are nine chairs."),
}

# Separate dict for grammar.json fixes
GRAMMAR_FIXES = {
    # n5-110 teaches CANONICAL counter usage. Example [3] used さかな
    # + 二つ — but fish canonically takes 匹/ひき. Eggs (たまご)
    # naturally take つ, fitting the pattern's canonical-counter lesson.
    ("n5-110", 3):
        ("ばんごはんに たまごを 二つ 食べました。",
         "I ate two eggs for dinner."),
}


def main():
    d = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    n = 0
    for (vid, idx), (new_ja, new_en) in FIXES.items():
        for e in d["entries"]:
            if e["id"] == vid:
                e["examples"][idx]["ja"] = new_ja
                e["examples"][idx]["translation_en"] = new_en
                n += 1
                print(f"  vocab {vid}[{idx}]: {new_ja}")
                break
    VOCAB.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nApplied {n}/{len(FIXES)} vocab counter-pedagogy fixes")
    # Grammar fixes
    GRAMMAR = Path("data/grammar.json")
    g = json.loads(GRAMMAR.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    gn = 0
    for (pid, idx), (new_ja, new_en) in GRAMMAR_FIXES.items():
        for p in g["patterns"]:
            if p["id"] == pid:
                p["examples"][idx]["ja"] = new_ja
                p["examples"][idx]["translation_en"] = new_en
                gn += 1
                print(f"  grammar {pid}[{idx}]: {new_ja}")
                break
    GRAMMAR.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Applied {gn}/{len(GRAMMAR_FIXES)} grammar counter-pedagogy fixes")


if __name__ == "__main__":
    main()
