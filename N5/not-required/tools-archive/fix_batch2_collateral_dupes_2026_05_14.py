"""Phase 2 Batch 2 cleanup — 13 within-pattern duplicates introduced
by Batch 2 (my replacement sentences collided with sentences already
present at other indices in the same pattern).

Replace the higher-index duplicate with a distinct sentence that
demonstrates the same pattern + form.
"""
import json
from collections import OrderedDict
from pathlib import Path

GRAMMAR = Path("data/grammar.json")

REPLACEMENTS = {
    ("n5-050", 5): ("あの ホテルは どうですか。", "How is that hotel?"),
    ("n5-052", 5): ("どうやって この えきへ 来ましたか。", "How did you come to this station?"),
    ("n5-056", 8): ("あなたの たんじょうびは なんようびですか。", "What day is your birthday?"),
    ("n5-073", 8): ("おかあさんは まだ おきて いません。", "Mother hasn't woken up yet."),
    ("n5-082", 8): ("あの えいがは おもしろくなかったです。", "That movie wasn't interesting."),
    ("n5-086", 7): ("わたしの へやは きれいじゃありません。", "My room isn't clean."),
    ("n5-089", 6): ("せんせいは しんせつで、まじめです。", "The teacher is kind and serious."),
    ("n5-097", 9): ("あかいのと あおいのと、どちらが いいですか。", "Red or blue, which is good?"),
    ("n5-151", 5): ("デザートは いかがですか。", "How about dessert?"),
    ("n5-153", 7): ("まだ ほんを よんで いません。", "I haven't read the book yet."),
    ("n5-154", 8): ("もう テストは おわりました。", "The test is already over."),
    ("n5-176", 8): ("もう かえらなきゃ。", "Gotta go home now."),
    ("n5-185", 4): ("だれかに きいて みます。", "I'll ask someone."),
}


def main() -> None:
    d = json.loads(GRAMMAR.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    applied = []
    for (pid, idx), (new_ja, new_en) in REPLACEMENTS.items():
        for p in d["patterns"]:
            if p["id"] == pid:
                ex = p["examples"][idx]
                old = ex.get("ja", "")
                ex["ja"] = new_ja
                ex["translation_en"] = new_en
                if "vocab_ids" in ex:
                    ex["vocab_ids"] = []
                if "pitch_marks" in ex:
                    ex["pitch_marks"] = []
                applied.append((pid, idx, old, new_ja))
                break
    GRAMMAR.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Within-pattern duplicate cleanup: {len(applied)}/{len(REPLACEMENTS)}")


if __name__ == "__main__":
    main()
