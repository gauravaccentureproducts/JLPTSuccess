"""Phase B native-teacher review fixes.

Sweep across all 12 corpora caught:
  1. 74 vocab.json entries with 「Xが あります。」 → "There is X." bare-
     article templated examples (mostly at idx=1).
  2. 5 grammar.json entries with 「あの Xは どこですか。」 leak (same
     pattern that vocab Round 4 cleaned up, but I'd never extended
     the scan to grammar.json).
  3. 4 unnatural verb-pairings in vocab adverb/keigo entries (ぜひ ご
     はんを 食べます, ただ ごはんを 食べます, ためる人が います, あした
     聞こえるつもりです, あした ござるつもりです).
  4. 4 translation_en entries with " / " (multi-translation): pick one.

All replacements:
  - Use the entry's headword in a natural N5-level context
  - Stay within the 106-char N5 kanji whitelist
  - Differ from sibling examples in the same entry
  - Have natural English translations (no bare-article 'There is hat')
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")
GRAMMAR = Path("data/grammar.json")
KANJI = Path("data/kanji.json")

# === Vocab fixes (74 bare-article + others) ===
VOCAB_FIXES = {
    # Family / people (with animacy fixes: animate → います)
    ("n5.vocab.2-people-family.そぼ", 1):
        ("そぼは げんきで さんぽに 行きます。",
         "My grandmother is well and goes for walks."),
    ("n5.vocab.2-people-family.おばさん", 1):
        ("おばさんは アメリカに すんで います。",
         "My aunt lives in America."),
    ("n5.vocab.2-people-family.男の子", 1):
        ("男の子が 道で あそんで います。",
         "A boy is playing on the road."),
    # Time words — 'Xが あります' is grammatically nonsense for time
    ("n5.vocab.10-time-general.こんや", 1):
        ("こんや 友だちと 食じを します。",
         "I'll eat with a friend tonight."),
    ("n5.vocab.11-time-days-weeks-month.年", 1):
        ("来年で 二十さいに なります。",
         "I'll turn 20 next year."),
    ("n5.vocab.12-time-frequency-sequen.後で", 1):
        ("じゅぎょうが おわった 後で 電話します。",
         "I'll call after class ends."),
    # Locations
    ("n5.vocab.13-locations-and-places-.だいどころ", 1):
        ("だいどころで 母が りょうりを して います。",
         "Mother is cooking in the kitchen."),
    ("n5.vocab.13-locations-and-places-.にわ", 1):
        ("にわに 花が さいて います。",
         "Flowers are blooming in the garden."),
    ("n5.vocab.13-locations-and-places-.大学", 1):
        ("大学で にほんごを べんきょうして います。",
         "I'm studying Japanese at university."),
    ("n5.vocab.13-locations-and-places-.パンや", 1):
        ("パンやで あさパンを 買いました。",
         "I bought breakfast bread at the bakery."),
    ("n5.vocab.13-locations-and-places-.どうぶつえん", 1):
        ("どうぶつえんで ぞうを 見ました。",
         "I saw an elephant at the zoo."),
    ("n5.vocab.13-locations-and-places-.道", 1):
        ("この 道は とても せまいです。",
         "This road is very narrow."),
    ("n5.vocab.13-locations-and-places-.かど", 1):
        ("つぎの かどを 右に まがって ください。",
         "Please turn right at the next corner."),
    ("n5.vocab.13-locations-and-places-.むら", 1):
        ("この むらは とても 古いです。",
         "This village is very old."),
    ("n5.vocab.13-locations-and-places-.出口", 1):
        ("出口は あちらです。",
         "The exit is over there."),
    # Nature / weather
    ("n5.vocab.14-nature-and-weather.山", 1):
        ("この 山は とても 高いです。",
         "This mountain is very high."),
    ("n5.vocab.14-nature-and-weather.かぜ", 1):
        ("つよい かぜが ふいて います。",
         "A strong wind is blowing."),
    ("n5.vocab.14-nature-and-weather.くもり", 1):
        ("今日は あさから くもりです。",
         "It has been cloudy since the morning."),
    # Animal
    ("n5.vocab.15-animals.むし", 1):
        ("にわで 小さい むしを 見ました。",
         "I saw a small insect in the garden."),
    # Food
    ("n5.vocab.16-food-and-drink-genera.ひるごはん", 1):
        ("ひるごはんは 十二時に 食べます。",
         "I eat lunch at twelve."),
    ("n5.vocab.16-food-and-drink-genera.おかし", 0):
        ("おかしを 子どもに あげました。",
         "I gave sweets to the child."),
    ("n5.vocab.17-food-items.ぶたにく", 0):
        ("ばんごはんに ぶたにくを 食べました。",
         "I had pork for dinner."),
    ("n5.vocab.17-food-items.くだもの", 1):
        ("やおやで くだものを 買いました。",
         "I bought fruit at the greengrocer."),
    ("n5.vocab.17-food-items.じゃがいも", 1):
        ("じゃがいもを 切って カレーに 入れます。",
         "I cut potatoes and put them in the curry."),
    ("n5.vocab.17-food-items.バター", 1):
        ("パンに バターを ぬります。",
         "I spread butter on bread."),
    ("n5.vocab.17-food-items.チーズ", 1):
        ("チーズを 食べる ことが できますか。",
         "Can you eat cheese?"),
    ("n5.vocab.17-food-items.うどん", 0):
        ("お昼に うどんを 食べました。",
         "I had udon for lunch."),
    ("n5.vocab.17-food-items.サラダ", 1):
        ("やさいの サラダを つくりました。",
         "I made a vegetable salad."),
    ("n5.vocab.17-food-items.スープ", 0):
        ("あつい スープを 飲みました。",
         "I drank hot soup."),
    ("n5.vocab.17-food-items.チョコレート", 1):
        ("子どもに チョコレートを あげました。",
         "I gave the child chocolate."),
    # Tableware
    ("n5.vocab.19-tableware-and-cooking.さら", 1):
        ("白い さらに ケーキを のせました。",
         "I placed cake on a white plate."),
    ("n5.vocab.19-tableware-and-cooking.おわん", 1):
        ("おわんに みそしるを 入れます。",
         "I put miso soup in the bowl."),
    ("n5.vocab.19-tableware-and-cooking.フォーク", 1):
        ("フォークで サラダを 食べます。",
         "I eat salad with a fork."),
    ("n5.vocab.19-tableware-and-cooking.ナイフ", 1):
        ("ナイフで パンを 切ります。",
         "I cut bread with a knife."),
    ("n5.vocab.19-tableware-and-cooking.コップ", 1):
        ("コップに 水を 入れて ください。",
         "Please put water in the cup."),
    ("n5.vocab.19-tableware-and-cooking.なべ", 1):
        ("大きい なべで スープを つくります。",
         "I make soup in a big pot."),
    # Colors
    ("n5.vocab.20-colors.くろ", 1):
        ("くろの ペンで 名前を 書いて ください。",
         "Please write your name with a black pen."),
    ("n5.vocab.20-colors.あお", 1):
        ("空の 色は あおです。",
         "The sky's color is blue."),
    # Clothing
    ("n5.vocab.21-clothing-and-accessor.うわぎ", 1):
        ("ふゆは あつい うわぎを きます。",
         "I wear a thick jacket in winter."),
    ("n5.vocab.21-clothing-and-accessor.コート", 1):
        ("さむいので、コートを きて 出かけます。",
         "It's cold, so I'll wear a coat to go out."),
    ("n5.vocab.21-clothing-and-accessor.シャツ", 1):
        ("白い シャツに ネクタイを します。",
         "I wear a tie with my white shirt."),
    ("n5.vocab.21-clothing-and-accessor.ぼうし", 1):
        ("あつい 日は ぼうしを かぶります。",
         "On hot days I wear a hat."),
    ("n5.vocab.21-clothing-and-accessor.ハンカチ", 1):
        ("ポケットから ハンカチを 出します。",
         "I take a handkerchief out of my pocket."),
    # Money/shopping
    ("n5.vocab.22-money-and-shopping.ねだん", 1):
        ("この くだものの ねだんは 高いです。",
         "The price of this fruit is high."),
    ("n5.vocab.22-money-and-shopping.きっぷ", 3):
        ("えきで きっぷを 二まい 買いました。",
         "I bought two tickets at the station."),
    ("n5.vocab.22-money-and-shopping.てがみ", 3):
        ("母から てがみが とどきました。",
         "A letter arrived from my mother."),
    ("n5.vocab.22-money-and-shopping.にもつ", 1):
        ("じてんしゃの 後ろに にもつを のせました。",
         "I placed the luggage on the back of the bicycle."),
    # School/study
    ("n5.vocab.24-school-and-study.もじ", 1):
        ("ノートに きれいな もじを 書きます。",
         "I write neat characters in my notebook."),
    ("n5.vocab.24-school-and-study.れい", 1):
        ("先生が れいを 三つ 出しました。",
         "The teacher gave three examples."),
    ("n5.vocab.24-school-and-study.新聞", 1):
        ("毎朝 新聞を 読みます。",
         "I read the newspaper every morning."),
    ("n5.vocab.24-school-and-study.いす", 3):
        ("きょうしつに いすが 三十 あります。",
         "There are thirty chairs in the classroom."),
    ("n5.vocab.24-school-and-study.え", 1):
        ("子どもが きれいな えを かきました。",
         "The child drew a beautiful picture."),
    # House
    ("n5.vocab.26-house-and-furniture.アパート", 1):
        ("駅の ちかくに 新しい アパートが できました。",
         "A new apartment building was built near the station."),
    ("n5.vocab.26-house-and-furniture.マンション", 1):
        ("私の マンションは 五かいに あります。",
         "My condo is on the fifth floor."),
    ("n5.vocab.26-house-and-furniture.もん", 1):
        ("学校の もんは 八時に 開きます。",
         "The school gate opens at 8."),
    ("n5.vocab.26-house-and-furniture.せっけん", 1):
        ("せっけんで 手を あらいます。",
         "I wash my hands with soap."),
    ("n5.vocab.26-house-and-furniture.タオル", 1):
        ("白い タオルで かおを ふきます。",
         "I wipe my face with a white towel."),
    ("n5.vocab.26-house-and-furniture.テープ", 3):
        ("テープを はさみで 切ります。",
         "I cut the tape with scissors."),
    # Verbs (fix the ためる/聞こえる/ござる template-leak)
    ("n5.vocab.27-verbs-group-1-verbs.つかう", 0):
        ("はしを つかって ごはんを 食べます。",
         "I use chopsticks to eat rice."),
    ("n5.vocab.28-verbs-group-2-verbs.ためる", 1):
        ("毎日 すこしずつ お金を ためて います。",
         "I'm saving money little by little every day."),
    ("n5.vocab.28-verbs-group-2-verbs.聞こえる", 1):
        ("外から こどもたちの こえが 聞こえます。",
         "I can hear children's voices from outside."),
    ("n5.vocab.30-verbs-existence-and-p.ござる", 1):
        ("こちらに じしょが ございます。",
         "Here is a dictionary (very polite)."),
    # Adverbs (fix unnatural ぜひ/ただ usage)
    ("n5.vocab.33-adverbs.ぜひ", 1):
        ("ぜひ 一どは 日本に 行って みて ください。",
         "Please visit Japan at least once."),
    ("n5.vocab.33-adverbs.ただ", 1):
        ("ただの 水ですが、つめたくて おいしいです。",
         "It's just water, but it's cold and tasty."),
    ("n5.vocab.33-adverbs.やはり", 1):
        ("やはり 学校へ 行きます。",
         "After all, I'll go to school."),
    # Conjunctions (fix multi-translation)
    ("n5.vocab.34-conjunctions.けれど", 1):
        ("えいがは おもしろかったです。けれど、ながかったです。",
         "The movie was interesting, but it was long."),
    # Greetings (multi-translation in en)
    ("n5.vocab.36-greetings-and-set-phr.いってらっしゃい", 1):
        ("先生に「いってらっしゃい」と 言いました。",
         "I said 'have a good day' to the teacher."),
    # Common-nouns-miscella
    ("n5.vocab.37-common-nouns-miscella.話", 1):
        ("おもしろい 話を 聞きました。",
         "I heard an interesting story."),
    ("n5.vocab.37-common-nouns-miscella.うんどう", 1):
        ("まいあさ こうえんで うんどうを します。",
         "I exercise in the park every morning."),
    ("n5.vocab.37-common-nouns-miscella.びょうき", 1):
        ("びょうきで 学校を 休みました。",
         "I missed school because of illness."),
    ("n5.vocab.37-common-nouns-miscella.マッチ", 1):
        ("マッチで ろうそくに 火を つけました。",
         "I lit the candle with a match."),
    ("n5.vocab.37-common-nouns-miscella.はいざら", 1):
        ("テーブルの 上に はいざらを おきました。",
         "I placed an ashtray on the table."),
    ("n5.vocab.37-common-nouns-miscella.じかんわり", 1):
        ("新しい じかんわりを かべに はりました。",
         "I put the new timetable on the wall."),
    ("n5.vocab.37-common-nouns-miscella.はこ", 1):
        ("大きい はこに 本を 入れました。",
         "I put books in a large box."),
    ("n5.vocab.37-common-nouns-miscella.かてい", 1):
        ("私の かていは 五人ぐらしです。",
         "My household has five people."),
    ("n5.vocab.37-common-nouns-miscella.じびき", 1):
        ("古い じびきが ほんだなに あります。",
         "There's an old dictionary on the bookshelf."),
    ("n5.vocab.37-common-nouns-miscella.メートル", 1):
        ("プールの 長さは 二十五メートルです。",
         "The pool is 25 meters long."),
    # Misc
    ("n5.vocab.40-misc-useful-items.ばしょ", 1):
        ("しずかな ばしょで 本を 読みたいです。",
         "I want to read a book in a quiet place."),
    ("n5.vocab.40-misc-useful-items.ほう", 1):
        ("北の ほうへ あるいて ください。",
         "Please walk toward the north."),
    ("n5.vocab.24-school-and-study.おしらせ", 1):
        ("学校から だいじな おしらせが あります。",
         "There is an important announcement from the school."),
    ("n5.vocab.40-misc-useful-items.コンサート", 1):
        ("らい週の どようびに コンサートが あります。",
         "There is a concert next Saturday."),
    # Animacy fixes for 日本人/スペイン人
    ("n5.vocab.25-languages-and-countri.日本人", 1):
        ("わたしの クラスには 日本人が 二十人 います。",
         "There are twenty Japanese students in my class."),
    ("n5.vocab.25-languages-and-countri.スペイン人", 1):
        ("となりの 友だちは スペイン人です。",
         "My neighbor is Spanish."),
    # さかな animal-sense improvement
    ("n5.vocab.15-animals.さかな", 2):
        ("うみに 小さい さかなが たくさん います。",
         "There are many small fish in the sea."),
    # はし-chopsticks (already plural in EN, but improve the JA)
    ("n5.vocab.20-tableware-and-cooking.はし-chopsticks", 0):
        ("毎日 はしで ごはんを 食べます。",
         "I eat rice with chopsticks every day."),
}


# === Grammar fixes (5 doko-template + 1 multi-translation) ===
GRAMMAR_FIXES = {
    ("n5-041", 5):
        ("そこは わたしの きょうしつです。",
         "That is my classroom."),
    ("n5-041", 6):
        ("あそこは こうえんです。",
         "That over there is a park."),
    ("n5-048", 5):
        ("どこへ 行きましたか。",
         "Where did you go?"),
    ("n5-048", 6):
        ("だれが きましたか。",
         "Who came?"),
    ("n5-164", 6):
        ("ホテルは どこに ありますか。",
         "Where is the hotel?"),
    # multi-translation fix for n5-103
    ("n5-103", 0):
        ("日本語が できます。",
         "I can speak Japanese."),
}


# === Kanji fixes (1 multi-translation) ===
KANJI_FIXES = {
    # The sentence is the same Japanese as grammar n5-103[0]
    ("本", 0):
        ("日本語が できます。",
         "I can speak Japanese."),
}


def apply_vocab():
    d = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    n = missing = 0
    for (vid, idx), (new_ja, new_en) in VOCAB_FIXES.items():
        for e in d["entries"]:
            if e["id"] == vid:
                if idx < len(e.get("examples", [])):
                    e["examples"][idx]["ja"] = new_ja
                    e["examples"][idx]["translation_en"] = new_en
                    n += 1
                else:
                    missing += 1
                    print(f"  MISSING idx: {vid}[{idx}]")
                break
        else:
            missing += 1
            print(f"  MISSING id: {vid}")
    VOCAB.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"vocab.json: {n}/{len(VOCAB_FIXES)} fixes applied (missing: {missing})")


def apply_grammar():
    d = json.loads(GRAMMAR.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    n = 0
    for (pid, idx), (new_ja, new_en) in GRAMMAR_FIXES.items():
        for p in d["patterns"]:
            if p["id"] == pid:
                if idx < len(p.get("examples", [])):
                    p["examples"][idx]["ja"] = new_ja
                    p["examples"][idx]["translation_en"] = new_en
                    n += 1
                break
    GRAMMAR.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"grammar.json: {n}/{len(GRAMMAR_FIXES)} fixes applied")


def apply_kanji():
    d = json.loads(KANJI.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    n = 0
    for (glyph, idx), (new_ja, new_en) in KANJI_FIXES.items():
        for e in d["entries"]:
            if e["glyph"] == glyph:
                if idx < len(e.get("sentences", [])):
                    e["sentences"][idx]["ja"] = new_ja
                    e["sentences"][idx]["translation_en"] = new_en
                    n += 1
                break
    KANJI.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"kanji.json: {n}/{len(KANJI_FIXES)} fixes applied")


if __name__ == "__main__":
    apply_vocab()
    apply_grammar()
    apply_kanji()
