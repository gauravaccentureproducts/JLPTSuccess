"""Phase 2 Batch 3: fix the remaining high-frequency boilerplate.

Targets the top 5 most-leaking sentences with per-pattern authored
replacements. After Batch 3, max occurrences per sentence drops below
the threshold for JA-81 (boilerplate-leak CI gate).
"""
import json
from collections import OrderedDict
from pathlib import Path

GRAMMAR = Path("data/grammar.json")

REPLACEMENTS = {
    # ===== Evict "だれが きましたか。" from non-だれ/non-が patterns =====
    # Keep n5-003[0] (が), n5-018[0] (だれ), n5-060[4] (V-ました), n5-046[0] (だれ)
    ("n5-090", 4): ("あそこに なにが ありますか。", "What is over there?"),
    ("n5-091", 5): ("きょうしつに だれが いますか。", "Who is in the classroom?"),
    ("n5-110", 4): ("りんごを いくつ かいましたか。", "How many apples did you buy?"),
    ("n5-118", 4): ("もう しゅくだいを しましたか。", "Have you done your homework yet?"),
    ("n5-146", 4): ("せんせいは なんと 言いましたか。", "What did the teacher say?"),
    ("n5-154", 4): ("もう テストは おわりましたか。", "Is the test already over?"),

    # ===== Evict "じぶんで しゅくだいを します。" =====
    # Keep n5-004[5] (を), n5-007[5] (で)
    ("n5-058", 4): ("あした えいがを 見ます。", "I will watch a movie tomorrow."),
    ("n5-092", 4): ("つくえの 上に ほんが あります。", "There is a book on the desk."),
    ("n5-093", 4): ("ぎんこうは えきの となりに あります。", "The bank is next to the station."),
    ("n5-094", 4): ("ここに ペンが あります。", "There is a pen here."),
    ("n5-142", 4): ("コーヒーに します。", "I'll have coffee."),
    ("n5-150", 5): ("メニューを おねがいします。", "Menu, please."),
    ("n5-152", 4): ("どうぞ よろしく おねがいします。", "Pleased to meet you."),
    ("n5-168", 4): ("やすみの 日は 本を よんだり、おんがくを きいたり します。",
                    "On holidays, I read books, listen to music, and so on."),

    # ===== Evict "あにより わたしのほうが はやく おきます。" =====
    # Keep n5-096[2] (より-comparison, this is canonical)
    ("n5-076", 4): ("しゅくだいを して から、ねます。", "After doing homework, I sleep."),
    ("n5-092", 5): ("こうえんに こどもが います。", "There are children in the park."),
    ("n5-093", 5): ("えきは あそこに あります。", "The station is over there."),
    ("n5-094", 5): ("ここに たまごが あります。", "There are eggs here."),
    ("n5-103", 4): ("日本語を 話す ことが できます。", "I can speak Japanese."),
    ("n5-107", 4): ("デパートへ かいものに 行きます。", "I go to the department store to shop."),
    ("n5-147", 4): ("よく カフェへ 行きます。", "I often go to cafés."),
    ("n5-148", 4): ("いつも バスで 行きます。", "I always go by bus."),
    ("n5-188", 4): ("いもうとは ピアノを ひく ことが できます。",
                    "My younger sister can play the piano."),

    # ===== Evict "父に とけいを もらいました。" =====
    # Keep n5-060[5] (V-ました), n5-131[2] (〜にもらいます — canonical)
    ("n5-090", 5): ("きのう ここに ペンが ありました。", "There was a pen here yesterday."),
    ("n5-091", 6): ("きょうしつに せんせいが いました。", "There was a teacher in the classroom."),
    ("n5-110", 5): ("ほんを 二さつ かいました。", "I bought two books."),
    ("n5-118", 5): ("いま テストが おわりました。", "The test just ended."),
    ("n5-125", 4): ("これは わたしの ペンじゃ ありません。", "This isn't my pen."),
    ("n5-146", 5): ("やまださんは 「おはよう」と 言いました。", "Yamada-san said 'Good morning.'"),
    ("n5-154", 5): ("もう ばんごはんを たべました。", "I already ate dinner."),

    # ===== Evict "いもうとは 学校に 行きます。" =====
    # Keep n5-107[5] (V-stem + に 行きます)
    ("n5-076", 5): ("ごはんを たべて から、コーヒーを のみます。",
                    "After eating, I drink coffee."),
    ("n5-092", 6): ("いえに ねこが います。", "There is a cat in the house."),
    ("n5-093", 6): ("としょかんは 学校の 中に あります。", "The library is inside the school."),
    ("n5-094", 6): ("つくえの 上に ノートが あります。", "There is a notebook on the desk."),
    ("n5-103", 5): ("ピアノを ひく ことが できます。", "I can play the piano."),
    ("n5-147", 5): ("ときどき えいがを 見ます。", "Sometimes I watch movies."),
    ("n5-148", 5): ("いつも あさ 7時に おきます。", "I always wake up at 7 AM."),
    ("n5-188", 5): ("わたしは およぐ ことが できます。", "I can swim."),
}


def main() -> None:
    d = json.loads(GRAMMAR.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    applied = []
    missing = []
    for (pid, idx), (new_ja, new_en) in REPLACEMENTS.items():
        target = None
        for p in d["patterns"]:
            if p["id"] == pid:
                target = p
                break
        if not target:
            missing.append((pid, idx, "pattern-not-found"))
            continue
        if idx >= len(target["examples"]):
            missing.append((pid, idx, "index-out-of-range"))
            continue
        ex = target["examples"][idx]
        old = ex.get("ja", "")
        ex["ja"] = new_ja
        ex["translation_en"] = new_en
        if "vocab_ids" in ex:
            ex["vocab_ids"] = []
        if "pitch_marks" in ex:
            ex["pitch_marks"] = []
        applied.append((pid, idx, old, new_ja))
    GRAMMAR.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Batch 3 boilerplate fixes applied: {len(applied)}/{len(REPLACEMENTS)}")
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  {m}")


if __name__ == "__main__":
    main()
