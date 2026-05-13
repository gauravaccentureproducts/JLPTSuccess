"""Phase 2 Batch 1: fix within-pattern duplicate examples.

68 cases where the same sentence appears at TWO different indices in
ONE grammar pattern (e.g. n5-003 had "だれが きましたか。" at [0] and
[8]). For each, we keep the first occurrence and replace the second
with a newly-authored sentence that demonstrates the same pattern,
preserves the existing form tag, and uses N5-vocab + N5-kanji only.

vocab_ids and pitch_marks are cleared on each replaced example;
they tagged words from the OLD sentence and would point at wrong
vocab in the new sentence. A future content-enrichment pass can
re-tag.

Run:
  python -X utf8 not-required/tools-archive/fix_within_pattern_duplicates_2026_05_14.py
"""
import json
from collections import OrderedDict
from pathlib import Path

GRAMMAR = Path("data/grammar.json")

# Map of (pattern_id, dup_index_to_replace) -> (new_ja, new_translation_en).
# The form tag is preserved from the existing example.
REPLACEMENTS = {
    ("n5-003", 8): ("なにが おいしいですか。", "What is delicious?"),
    ("n5-004", 7): ("おちゃを のみます。", "I drink tea."),
    ("n5-007", 8): ("うちで えいがを みます。", "I watch movies at home."),
    ("n5-013", 7): ("たなかさんも きます。", "Mr./Ms. Tanaka also comes."),
    ("n5-014", 7): ("これは ペンです。", "This is a pen."),
    ("n5-014", 8): ("それは くるまですか。", "Is that a car?"),
    ("n5-017", 8): ("なにを かいますか。", "What will you buy?"),
    ("n5-018", 9): ("それは だれの ペンですか。", "Whose pen is that?"),
    ("n5-025", 7): ("あついですね。", "It's hot, isn't it?"),
    ("n5-025", 9): ("おもしろいですね。", "It's interesting, isn't it?"),
    ("n5-037", 5): ("りんごや バナナなどを たべました。", "I ate apples, bananas, and so on."),
    ("n5-041", 8): ("そこに ぎんこうが あります。", "There is a bank there."),
    ("n5-042", 7): ("こちらは わたしの きょうしつです。", "This is my classroom."),
    ("n5-042", 8): ("りんごと バナナと、どちらが すきですか。", "Apple or banana, which do you like?"),
    ("n5-044", 9): ("わたしも そう おもいます。", "I think so too."),
    ("n5-048", 8): ("どこで まちましたか。", "Where did you wait?"),
    ("n5-050", 7): ("てんきは どうですか。", "How is the weather?"),
    ("n5-050", 8): ("ケーキは いかがですか。", "How about cake?"),
    ("n5-051", 8): ("なぜ おそく きましたか。", "Why did you come late?"),
    ("n5-052", 8): ("どうやって たべますか。", "How do you eat it?"),
    ("n5-053", 7): ("その ほんは いくらですか。", "How much is that book?"),
    ("n5-053", 8): ("ふたつで いくらですか。", "How much for two?"),
    ("n5-054", 7): ("みかんは いくつ ありますか。", "How many oranges are there?"),
    ("n5-056", 7): ("あしたは なんようびですか。", "What day is tomorrow?"),
    ("n5-056", 8): ("テストは なんようびですか。", "What day is the test?"),
    ("n5-057", 7): ("クリスマスは なんがつ なんにちですか。", "When is Christmas?"),
    ("n5-057", 8): ("やすみは なんがつですか。", "What month is the holiday?"),
    ("n5-059", 7): ("あさごはんは たべません。", "I don't eat breakfast."),
    ("n5-062", 7): ("いっしょに あるきましょう。", "Let's walk together."),
    ("n5-063", 5): ("いっしょに かえりましょうか。", "Shall we go home together?"),
    ("n5-063", 7): ("でんきを つけましょうか。", "Shall I turn on the light?"),
    ("n5-063", 8): ("おちゃを つくりましょうか。", "Shall I make tea?"),
    ("n5-079", 7): ("この りょうりは おいしいです。", "This dish is delicious."),
    ("n5-080", 7): ("この えいがは おもしろくないです。", "This movie isn't interesting."),
    ("n5-081", 7): ("テストは むずかしかったです。", "The test was difficult."),
    ("n5-083", 4): ("あの ほんは ながくて おもしろいです。", "That book is long and interesting."),
    ("n5-089", 6): ("この まちは しずかで、きれいです。", "This town is quiet and clean."),
    ("n5-092", 9): ("がっこうに せんせいが います。", "There is a teacher at school."),
    ("n5-093", 9): ("ねこは いすの したに います。", "The cat is under the chair."),
    ("n5-097", 8): ("やまと うみと、どちらが すきですか。", "Mountain or sea, which do you like?"),
    ("n5-105", 6): ("きょうは いきたくないです。", "I don't want to go today."),
    ("n5-106", 6): ("おおきい いえが ほしいです。", "I want a big house."),
    ("n5-106", 9): ("じてんしゃが ほしいです。", "I want a bicycle."),
    ("n5-109", 4): ("がくせいは なんにん いますか。", "How many students are there?"),
    ("n5-109", 7): ("かみは なんまい ありますか。", "How many sheets of paper are there?"),
    ("n5-112", 5): ("30分 まちました。", "I waited 30 minutes."),
    ("n5-116", 6): ("まいしゅう えいがを みます。", "I watch movies every week."),
    ("n5-117", 7): ("あしたは やすみです。", "Tomorrow is a holiday."),
    ("n5-130", 7): ("母に かばんを あげました。", "I gave my mother a bag."),
    ("n5-142", 7): ("おちゃに します。", "I'll have tea."),
    ("n5-142", 8): ("のみものは なにに しますか。", "What will you have to drink?"),
    ("n5-143", 8): ("せんせいに なりたいです。", "I want to become a teacher."),
    ("n5-148", 8): ("たいてい バスで 学校へ いきます。", "I usually go to school by bus."),
    ("n5-149", 7): ("ペンを ください。", "Please give me a pen."),
    ("n5-150", 7): ("おちゃを おねがいします。", "Tea, please."),
    ("n5-150", 8): ("おみずを おねがいします。", "Water, please."),
    ("n5-151", 7): ("おかしは いかがですか。", "How about some sweets?"),
    ("n5-154", 7): ("もう ごはんを たべました。", "I already ate."),
    ("n5-155", 5): ("やすいですが、おいしくないです。", "It's cheap, but it isn't delicious."),
    ("n5-155", 6): ("ねこは すきですが、いぬは すきじゃありません。", "I like cats, but I don't like dogs."),
    ("n5-156", 7): ("この りょうりは おいしいですよ。", "This dish is delicious, you know."),
    ("n5-165", 8): ("ごはんを どうぞ。", "Please have some rice."),
    ("n5-170", 7): ("やさいを たべた ほうが いいですよ。", "You should eat vegetables."),
    ("n5-174", 7): ("あさ はやく おきなくては なりません。", "I must wake up early in the morning."),
    ("n5-176", 8): ("もう いかなくちゃ。", "Gotta go now."),
    ("n5-181", 8): ("そらが きれいだなあ。", "The sky is beautiful!"),
    ("n5-184", 7): ("なにか のみたいです。", "I want to drink something."),
    ("n5-185", 4): ("だれか いますか。", "Is someone there?"),
}


def main() -> None:
    d = json.loads(GRAMMAR.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)

    applied = []
    missing = []
    for (pid, idx), (new_ja, new_en) in REPLACEMENTS.items():
        target = None
        for p in d.get("patterns", []):
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
        if "vocab_ids" in ex:
            ex["vocab_ids"] = []
        if "pitch_marks" in ex:
            ex["pitch_marks"] = []
        applied.append((pid, idx, old_ja, new_ja))

    GRAMMAR.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Within-pattern duplicate fixes applied: {len(applied)}/{len(REPLACEMENTS)}")
    if missing:
        print(f"\nMISSING (not applied):")
        for pid, idx, reason in missing:
            print(f"  {pid}[{idx}]: {reason}")


if __name__ == "__main__":
    main()
