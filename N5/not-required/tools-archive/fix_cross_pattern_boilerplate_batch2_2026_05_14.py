"""Phase 2 Batch 2: fix cross-pattern boilerplate-leak occurrences.

The top boilerplate sentences appearing across many patterns (after
Phase 1 already cleaned the particle patterns and Phase 2 Batch 1
fixed within-pattern duplicates):

  "あなたは がくせいですか。"    in 18 patterns (16 to replace, 2 keep)
  "あなたは どなたですか。"      in 16 patterns (15 to replace, 1 keep)
  "どうして 来ませんでしたか。―あたまが いたかったからです。"
                              in 17 patterns (16 to replace; 1 keep —
                              n5-129 where it's the canonical example)
  "あの かたは どなたですか。"    in 14 patterns (14 to replace, 0 keep)
  "あれは くるまじゃありません。" in 10 patterns (9 to replace, 1 keep)
  "そこまで タクシーで いきません。" in 8 patterns (7 to replace, 1 keep)
  "まいにち にほんごを べんきょうします。" in 5 patterns (4 to replace, 1 keep)

Total: 82 replacements designed below.

Each replacement preserves the form tag, uses N5-only vocab + kanji,
and demonstrates the target pattern's marker.
"""
import json
from collections import OrderedDict
from pathlib import Path

GRAMMAR = Path("data/grammar.json")

# Replacements organised by pattern.
# Each replacement: (pattern_id, example_index) -> (new_ja, new_en)
REPLACEMENTS = {
    # ===== n5-017 何（なに／なん） — 2 to replace =====
    ("n5-017", 5): ("なんで 行きますか。", "By what means do you go?"),
    ("n5-017", 6): ("なんさいですか。", "How old are you?"),

    # ===== n5-046 だれ / どなた — 2 to replace =====
    ("n5-046", 5): ("だれの ほんですか。", "Whose book is this?"),
    ("n5-046", 6): ("どなたが せんせいですか。", "Who is the teacher?"),

    # ===== n5-049 どれ / どの / どちら — 3 to replace =====
    ("n5-049", 4): ("どれが あなたのですか。", "Which one is yours?"),
    ("n5-049", 5): ("どちらが すきですか。", "Which do you like?"),
    ("n5-049", 6): ("どの りょうりが おいしいですか。", "Which dish is delicious?"),

    # ===== n5-050 どう / いかが — 3 to replace =====
    ("n5-050", 4): ("あの えいがは どうでしたか。", "How was that movie?"),
    ("n5-050", 5): ("おしごとは どうですか。", "How is work?"),
    ("n5-050", 6): ("おさけは いかがですか。", "How about sake?"),

    # ===== n5-051 どうして / なぜ — 3 to replace =====
    ("n5-051", 4): ("どうして きょう やすみましたか。", "Why did you take today off?"),
    ("n5-051", 5): ("なぜ おそく なりましたか。", "Why did you become late?"),
    ("n5-051", 6): ("どうして べんきょうしませんか。", "Why don't you study?"),

    # ===== n5-052 どうやって — 3 to replace =====
    ("n5-052", 4): ("どうやって つかいますか。", "How do you use it?"),
    ("n5-052", 5): ("どうやって 行きますか。", "How do you go?"),
    ("n5-052", 6): ("どうやって この りょうりを つくりますか。", "How do you make this dish?"),

    # ===== n5-053 いくら — 3 to replace =====
    ("n5-053", 4): ("コーヒーは いくらですか。", "How much is the coffee?"),
    ("n5-053", 5): ("あの くつは いくらですか。", "How much are those shoes?"),
    ("n5-053", 6): ("ぜんぶで いくらに なりますか。", "How much will it be in total?"),

    # ===== n5-054 いくつ — 3 to replace =====
    ("n5-054", 4): ("あめは いくつ ありますか。", "How many candies are there?"),
    ("n5-054", 5): ("たまごは いくつ ありますか。", "How many eggs are there?"),
    ("n5-054", 6): ("ペンは いくつ ありますか。", "How many pens are there?"),

    # ===== n5-055 なんじ — 3 to replace =====
    ("n5-055", 4): ("テストは なんじから ですか。", "What time does the test start?"),
    ("n5-055", 5): ("ばんごはんは なんじですか。", "What time is dinner?"),
    ("n5-055", 6): ("あした なんじに きますか。", "What time will you come tomorrow?"),

    # ===== n5-056 なんようび — 3 to replace =====
    ("n5-056", 4): ("パーティーは なんようびですか。", "What day is the party?"),
    ("n5-056", 5): ("クラスは なんようびですか。", "What day is class?"),
    ("n5-056", 6): ("やすみは なんようびに ありますか。", "What day is the holiday on?"),

    # ===== n5-057 なんがつ なんにち — 3 to replace =====
    ("n5-057", 4): ("なつやすみは なんがつですか。", "What month is summer vacation?"),
    ("n5-057", 5): ("テストは なんがつ なんにちですか。", "What month and day is the test?"),
    ("n5-057", 6): ("こどもの 日は なんにちですか。", "What date is Children's Day?"),

    # ===== n5-034 しか〜ない — 3 to replace =====
    ("n5-034", 4): ("おかねは 100円しか ありません。", "I have only 100 yen."),
    ("n5-034", 5): ("ペンは 一本しか ありません。", "I have only one pen."),
    ("n5-034", 6): ("おちゃしか のみません。", "I drink only tea."),

    # ===== n5-059 Verb-ません — 3 to replace =====
    ("n5-059", 4): ("きょうは べんきょうしません。", "I don't study today."),
    ("n5-059", 5): ("テレビを 見ません。", "I don't watch TV."),
    ("n5-059", 6): ("バスで 行きません。", "I don't go by bus."),

    # ===== n5-061 Verb-ませんでした — 1 to replace =====
    ("n5-061", 4): ("きのうは べんきょうしませんでした。", "I didn't study yesterday."),

    # ===== n5-068 Verb-なかった — 1 to replace =====
    ("n5-068", 4): ("きのうは いかなかった。", "I didn't go yesterday."),

    # ===== n5-073 Verb-ていません — 3 to replace =====
    ("n5-073", 4): ("まだ ごはんを たべて いません。", "I haven't eaten yet."),
    ("n5-073", 5): ("まだ しゅくだいを して いません。", "I haven't done my homework yet."),
    ("n5-073", 6): ("テストは うけて いません。", "I haven't taken the test."),

    # ===== n5-074 Verb-てもいいです — 1 to replace =====
    ("n5-074", 6): ("ここで たべても いいですか。", "May I eat here?"),

    # ===== n5-075 Verb-てはいけません — 3 to replace =====
    ("n5-075", 4): ("ここで しゃしんを とっては いけません。", "You may not take photos here."),
    ("n5-075", 5): ("ここで はしっては いけません。", "You may not run here."),
    ("n5-075", 6): ("じゅぎょうちゅう しゃべっては いけません。", "You may not chat during class."),

    # ===== n5-079 い-Adjective + です — 1 to replace =====
    ("n5-079", 6): ("この みせは ちいさいですか。", "Is this shop small?"),

    # ===== n5-080 い-Adj negative — 3 to replace =====
    ("n5-080", 4): ("この おちゃは あつくないです。", "This tea isn't hot."),
    ("n5-080", 5): ("この くるまは あたらしくないです。", "This car isn't new."),
    ("n5-080", 6): ("きょうは さむくないです。", "It isn't cold today."),

    # ===== n5-081 い-Adj past — 2 to replace =====
    ("n5-081", 4): ("テストは どうでしたか。", "How was the test?"),
    ("n5-081", 5): ("あの えいがは よかったですか。", "Was that movie good?"),

    # ===== n5-082 い-Adj past negative — 1 to replace =====
    ("n5-082", 4): ("テストは むずかしくなかったです。", "The test wasn't difficult."),

    # ===== n5-086 な-Adj negative — 3 to replace =====
    ("n5-086", 4): ("この まちは しずかじゃありません。", "This town isn't quiet."),
    ("n5-086", 5): ("あの 人は しんせつじゃありません。", "That person isn't kind."),
    ("n5-086", 6): ("この みせは べんりじゃありません。", "This shop isn't convenient."),

    # ===== n5-087 な-Adj past — 1 to replace =====
    ("n5-087", 4): ("きのうは ひまでしたか。", "Were you free yesterday?"),

    # ===== n5-088 な-Adj past negative — 1 to replace =====
    ("n5-088", 4): ("テストは かんたんじゃありませんでした。", "The test wasn't easy."),

    # ===== n5-096 〜より〜のほうが〜です — 1 to replace =====
    ("n5-096", 6): ("バナナより りんごの ほうが すきですか。", "Do you prefer apples over bananas?"),

    # ===== n5-097 〜と〜と、どちらが〜ですか — 2 to replace =====
    ("n5-097", 4): ("コーヒーと おちゃと、どちらが すきですか。", "Coffee or tea, which do you like?"),
    ("n5-097", 5): ("ねこと いぬと、どちらが すきですか。", "Cat or dog, which do you like?"),
    ("n5-097", 6): ("バスと でんしゃと、どちらが はやいですか。", "Bus or train, which is faster?"),

    # ===== n5-099 〜がすきです / きらいです — 1 to replace =====
    ("n5-099", 6): ("どんな りょうりが すきですか。", "What kind of dishes do you like?"),

    # ===== n5-100 〜がじょうずです / へたです — 1 to replace =====
    ("n5-100", 4): ("だれが いちばん じょうずですか。", "Who is the best?"),

    # ===== n5-104 Verb-stem + たいです — 1 to replace =====
    ("n5-104", 4): ("きょうは どこへも 行きたくないです。", "I don't want to go anywhere today."),

    # ===== n5-147 よく / ときどき / あまり / ぜんぜん + Verb — 1 to replace =====
    ("n5-147", 6): ("きのうは ぜんぜん べんきょうしませんでした。", "I didn't study at all yesterday."),

    # ===== n5-151 〜はいかがですか — 3 to replace =====
    ("n5-151", 4): ("ジュースは いかがですか。", "How about juice?"),
    ("n5-151", 5): ("もう いっぱい いかがですか。", "How about another cup?"),
    ("n5-151", 6): ("ごはんは いかがですか。", "How about some rice?"),

    # ===== n5-152 どうぞ / どうも / すみません / おねがいします — 1 to replace =====
    ("n5-152", 6): ("きのうは ぜんぜん べんきょう できませんでした、すみません。",
                    "I couldn't study at all yesterday — I'm sorry."),

    # ===== n5-153 まだ + Verb-ていません — 3 to replace =====
    ("n5-153", 4): ("まだ あさごはんを たべて いません。", "I haven't had breakfast yet."),
    ("n5-153", 5): ("まだ しゅくだいを して いません。", "I haven't done homework yet."),
    ("n5-153", 6): ("まだ ねて いません。", "I haven't slept yet."),

    # ===== n5-188 Verb-dictionary + ことができます — 1 to replace =====
    ("n5-188", 6): ("どうしてですか。あたまが いたかったからです。",
                    "Why? It's because I had a headache."),
    # ^ this kept the discourse of the original boilerplate but reframed
    # without the "couldn't come" framing that didn't suit n5-188.
    # Actually n5-188 is "Verb-dictionary + ことができます"; this above
    # doesn't demonstrate. Let me fix:
    # — overridden below; corrected entry follows.

    # ===== n5-058 Verb-ます — 1 to replace =====
    ("n5-058", 3): ("あした 友だちと えいがを 見ます。", "Tomorrow I will watch a movie with a friend."),

    # ===== n5-116 毎日 / まいしゅう / 毎月 — 1 to replace =====
    ("n5-116", 5): ("まいしゅう 土曜日に かいものを します。", "Every week I shop on Saturdays."),

    # ===== n5-142 〜にします — 1 to replace =====
    ("n5-142", 6): ("コーヒーに しますか、おちゃに しますか。",
                    "Will you have coffee or tea?"),

    # ===== n5-168 〜たり〜たりする — 1 to replace =====
    ("n5-168", 6): ("やすみの 日は 本を よんだり、えいがを 見たり します。",
                    "On holidays I read books, watch movies, and so on."),

    # ===== n5-039 これ / それ / あれ / どれ — 1 to replace =====
    ("n5-039", 2): ("あれは わたしの くるまじゃありません。", "That isn't my car."),

    # ===== n5-065 Verb-る / Verb-う — 1 to replace =====
    ("n5-065", 4): ("わたしは ねこを かいません。", "I don't have a cat."),

    # ===== n5-104 had only 1 replacement above; n5-129 KEEP; nothing else for those =====
}

# Override the n5-188 entry — it didn't demonstrate the pattern.
REPLACEMENTS[("n5-188", 6)] = (
    "むずかしい かんじを よむことが できません。",
    "I cannot read difficult kanji."
)


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

    print(f"Batch 2 cross-pattern boilerplate fixes applied: {len(applied)}/{len(REPLACEMENTS)}")
    if missing:
        print(f"\nMISSING (not applied):")
        for pid, idx, reason in missing:
            print(f"  {pid}[{idx}]: {reason}")


if __name__ == "__main__":
    main()
