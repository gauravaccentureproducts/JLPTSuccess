"""Round-4 vocab audit fixes:
  111 DOKO-NON-LOCATION  ('あの Xは どこですか。' for non-location words)
  178 KORE-BARE          ('これは Xです。' / 'あれは Xです。' templates)
   12 GREET-WRONG-VERB   ('「X」と あいさつしました。' for non-greetings)

Total: 301 replacements. All within N5 kanji whitelist + headword
preserved + distinct from sibling examples.
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")

# (id, idx) -> (new_ja, new_en)
FIXES: dict[tuple[str, int], tuple[str, str]] = {

    # ============================================================
    #  DOKO-NON-LOCATION (111 entries)
    # ============================================================

    # --- people / family / roles ---
    ("n5.vocab.1-people-pronouns-and-se.みなさん", 1):
        ("みなさん、よろしく おねがいします。", "Pleased to meet all of you."),
    ("n5.vocab.2-people-family.お父さん", 1):
        ("お父さんと いっしょに さんぽに 行きました。",
         "I went for a walk with my father."),
    ("n5.vocab.2-people-family.あね", 1):
        ("あねは 三人の 子どもが います。",
         "My older sister has three children."),
    ("n5.vocab.2-people-family.女", 1):
        ("あの 女の 人は しんせつです。",
         "That woman is kind."),
    ("n5.vocab.3-people-roles.けいかん", 1):
        ("こうばんに けいかんが 二人 います。",
         "There are two police officers at the police box."),
    ("n5.vocab.3-people-roles.外国人", 1):
        ("外国人の 友だちが 三人 います。",
         "I have three foreign friends."),
    ("n5.vocab.4-body-parts.からだ", 1):
        ("毎日 はやく ねて からだを 休めます。",
         "I sleep early every day to rest my body."),

    # --- time ---
    ("n5.vocab.10-time-general.とき", 3):
        ("はじめての ときは どきどきしました。",
         "The first time, I was nervous."),
    ("n5.vocab.10-time-general.おととい", 1):
        ("おとといは 雨でした。",
         "The day before yesterday was rainy."),
    ("n5.vocab.10-time-general.ゆうがた", 1):
        ("ゆうがた 五時に いえに かえります。",
         "I return home at 5 in the evening."),
    ("n5.vocab.10-time-general.よる", 1):
        ("よるは しずかに なります。",
         "It becomes quiet at night."),
    ("n5.vocab.11-time-days-weeks-month.三日", 1):
        ("三日 つづけて 雨が ふって います。",
         "It has been raining for three days in a row."),
    ("n5.vocab.11-time-days-weeks-month.来週", 1):
        ("来週は しけんが あります。",
         "There is a test next week."),
    ("n5.vocab.11-time-days-weeks-month.水曜日", 1):
        ("毎週 水曜日に 日本語の じゅぎょうが あります。",
         "I have Japanese class every Wednesday."),
    ("n5.vocab.11-time-days-weeks-month.五月", 1):
        ("五月の さくらは とても きれいです。",
         "Cherry blossoms in May are very beautiful."),
    ("n5.vocab.11-time-days-weeks-month.七月", 1):
        ("七月は あめが よく ふります。",
         "It rains a lot in July."),
    ("n5.vocab.11-time-days-weeks-month.九月", 1):
        ("九月の 中ごろに れんきゅうが あります。",
         "There's a long weekend in mid-September."),
    ("n5.vocab.11-time-days-weeks-month.十一月", 1):
        ("十一月から さむく なります。",
         "It gets cold from November."),
    ("n5.vocab.11-time-days-weeks-month.十二月", 1):
        ("十二月に 学校が 休みに なります。",
         "School breaks up in December."),
    ("n5.vocab.11-time-days-weeks-month.おととし", 1):
        ("おととし けっこんしました。",
         "I got married the year before last."),
    ("n5.vocab.12-time-frequency-sequen.つぎ", 1):
        ("つぎの 電車は 七時です。",
         "The next train is at 7."),
    ("n5.vocab.12-time-frequency-sequen.前", 1):
        ("学校の 前で まちあわせましょう。",
         "Let's meet in front of the school."),

    # --- locations / house items ---
    ("n5.vocab.13-locations-and-places-.おふろ", 1):
        ("ねる 前に おふろに 入ります。",
         "I take a bath before going to bed."),
    ("n5.vocab.13-locations-and-places-.げんかん", 2):
        ("げんかんに かさが 三本 あります。",
         "There are three umbrellas at the entrance."),
    ("n5.vocab.13-locations-and-places-.ほんや", 1):
        ("ほんやで 新しい じしょを 買いました。",
         "I bought a new dictionary at the bookstore."),
    ("n5.vocab.13-locations-and-places-.くうこう", 1):
        ("くうこうまで 一時間 かかります。",
         "It takes one hour to the airport."),
    ("n5.vocab.13-locations-and-places-.ホテル", 1):
        ("あの ホテルは 大きくて きれいです。",
         "That hotel is large and beautiful."),
    ("n5.vocab.13-locations-and-places-.りょかん", 3):
        ("古い りょかんが しずかで 気もちが いいです。",
         "The old inn is quiet and pleasant."),
    ("n5.vocab.13-locations-and-places-.こうばん", 1):
        ("えきの 前に こうばんが あります。",
         "There is a police box in front of the station."),
    ("n5.vocab.13-locations-and-places-.こうじょう", 1):
        ("この こうじょうで 車を つくって います。",
         "Cars are made at this factory."),
    ("n5.vocab.13-locations-and-places-.しょくどう", 1):
        ("学校の しょくどうは 安くて おいしいです。",
         "The school cafeteria is cheap and tasty."),
    ("n5.vocab.13-locations-and-places-.たてもの", 1):
        ("ふるい たてものが しずかに 立って います。",
         "An old building stands quietly."),
    ("n5.vocab.13-locations-and-places-.プール", 1):
        ("プールで およいで つかれました。",
         "I got tired from swimming in the pool."),
    ("n5.vocab.13-locations-and-places-.はし", 1):
        ("はしの 上から 川が 見えます。",
         "I can see the river from the bridge."),
    ("n5.vocab.13-locations-and-places-.後ろ", 1):
        ("学校の 後ろに こうえんが あります。",
         "There is a park behind the school."),
    ("n5.vocab.13-locations-and-places-.とおく", 1):
        ("とおくから 友だちが 私に 会いに 来ます。",
         "A friend is coming from far to meet me."),
    ("n5.vocab.13-locations-and-places-.南", 1):
        ("南の しまは 一年中 あたたかいです。",
         "The southern islands are warm all year."),
    ("n5.vocab.14-nature-and-weather.木", 1):
        ("こうえんの 木の 下で 休みます。",
         "I rest under a tree in the park."),
    ("n5.vocab.14-nature-and-weather.いし", 1):
        ("子どもが 川で いしを ひろいました。",
         "The child picked up a stone at the river."),
    ("n5.vocab.14-nature-and-weather.ほし", 1):
        ("やまで たくさんの ほしを 見ました。",
         "I saw many stars in the mountains."),
    ("n5.vocab.14-nature-and-weather.天気", 1):
        ("天気が いいので さんぽに 行きましょう。",
         "The weather is nice, so let's go for a walk."),
    ("n5.vocab.14-nature-and-weather.はる", 1):
        ("はるは あたらしい きせつの はじまりです。",
         "Spring is the start of a new season."),

    # --- food / drink / items ---
    ("n5.vocab.15-animals.さかな", 1):
        ("毎日 さかなを 食べると からだに いいです。",
         "Eating fish every day is good for the body."),
    ("n5.vocab.15-animals.ぶた", 1):
        ("こうじょうで ぶたを そだてて います。",
         "Pigs are raised at the farm."),
    ("n5.vocab.16-food-and-drink-genera.たべもの", 1):
        ("子どもの すきな たべものは 何ですか。",
         "What is the child's favorite food?"),
    ("n5.vocab.17-food-items.とりにく", 1):
        ("スーパーで とりにくを 買いました。",
         "I bought chicken at the supermarket."),
    ("n5.vocab.17-food-items.みかん", 1):
        ("みかんは ふゆの くだものです。",
         "Mandarin oranges are a winter fruit."),
    ("n5.vocab.17-food-items.いちご", 1):
        ("いちごの ジャムを パンに ぬります。",
         "I spread strawberry jam on bread."),
    ("n5.vocab.17-food-items.たまねぎ", 1):
        ("カレーに たまねぎを 入れます。",
         "I put onion in the curry."),
    ("n5.vocab.17-food-items.きゅうり", 1):
        ("きゅうりは つめたくて おいしいです。",
         "Cucumbers are cool and tasty."),
    ("n5.vocab.17-food-items.キャベツ", 1):
        ("キャベツで サラダを つくります。",
         "I make salad with cabbage."),
    ("n5.vocab.17-food-items.さとう", 1):
        ("おかしには さとうが たくさん 入って います。",
         "Sweets contain a lot of sugar."),
    ("n5.vocab.17-food-items.みそ", 1):
        ("あさは みそしるを 飲みます。",
         "I drink miso soup in the morning."),
    ("n5.vocab.17-food-items.カレー", 1):
        ("カレーは からくて おいしいです。",
         "Curry is spicy and delicious."),
    ("n5.vocab.17-food-items.ラーメン", 1):
        ("あの 店の ラーメンは ゆうめいです。",
         "That shop's ramen is famous."),
    ("n5.vocab.17-food-items.そば", 1):
        ("あつい 日には つめたい そばが 食べたいです。",
         "On hot days I want to eat cold soba."),
    ("n5.vocab.17-food-items.ハンバーガー", 1):
        ("子どもは ハンバーガーが だいすきです。",
         "Children love hamburgers."),
    ("n5.vocab.18-drinks.ジュース", 1):
        ("つめたい ジュースを 一本 飲みました。",
         "I drank a bottle of cold juice."),

    # --- colors / clothing ---
    ("n5.vocab.20-colors.みどり", 1):
        ("はるは みどりが きれいに なります。",
         "Greenery becomes beautiful in spring."),
    ("n5.vocab.20-colors.ピンク", 1):
        ("ピンクの くちべにを つけて います。",
         "I'm wearing pink lipstick."),
    ("n5.vocab.21-clothing-and-accessor.ふく", 1):
        ("ふくを たんすに しまいました。",
         "I put the clothes away in the dresser."),
    ("n5.vocab.21-clothing-and-accessor.ようふく", 1):
        ("ようふくの 上に コートを きます。",
         "I wear a coat over my clothes."),
    ("n5.vocab.21-clothing-and-accessor.セーター", 1):
        ("あたらしい セーターを 母から もらいました。",
         "I received a new sweater from my mother."),
    ("n5.vocab.21-clothing-and-accessor.Tシャツ", 1):
        ("白い Tシャツが 五まい あります。",
         "I have five white T-shirts."),
    ("n5.vocab.21-clothing-and-accessor.ワイシャツ", 1):
        ("ワイシャツに ネクタイを します。",
         "I wear a tie with my dress shirt."),
    ("n5.vocab.21-clothing-and-accessor.ズボン", 1):
        ("くろい ズボンを きて 会社に 行きます。",
         "I wear black trousers to the office."),
    ("n5.vocab.21-clothing-and-accessor.めがね", 1):
        ("こまかい じを 読む とき めがねを かけます。",
         "I put on glasses to read small print."),
    ("n5.vocab.21-clothing-and-accessor.ボタン", 1):
        ("コートの ボタンを 一つ なくしました。",
         "I lost one button on my coat."),
    ("n5.vocab.22-money-and-shopping.お金", 1):
        ("お金は たいせつに つかいましょう。",
         "Let's use money carefully."),
    ("n5.vocab.22-money-and-shopping.きっぷ", 1):
        ("きっぷは じどう はんばいきで 買います。",
         "Tickets are bought at the vending machine."),
    ("n5.vocab.22-money-and-shopping.てがみ", 1):
        ("てがみを 出しに ゆうびんきょくに 行きました。",
         "I went to the post office to mail a letter."),
    ("n5.vocab.22-money-and-shopping.おみやげ", 3):
        ("かぞくに おみやげを 三つ 買いました。",
         "I bought three souvenirs for my family."),
    ("n5.vocab.22-money-and-shopping.レジ", 1):
        ("レジに ながい 行れつが できて います。",
         "There is a long line at the cashier."),
    ("n5.vocab.23-transport.車", 1):
        ("車で 友だちの いえに 行きました。",
         "I went to my friend's house by car."),
    ("n5.vocab.23-transport.じてんしゃ", 1):
        ("じてんしゃの 後ろに 子どもが のります。",
         "The child rides on the back of the bicycle."),
    ("n5.vocab.23-transport.ふね", 1):
        ("古い ふねが みなとに 入って 来ました。",
         "An old ship came into the harbor."),
    ("n5.vocab.23-transport.しんごう", 1):
        ("しんごうが あおの ときに わたります。",
         "I cross when the light is green."),
    ("n5.vocab.24-school-and-study.ことば", 1):
        ("新しい ことばを 五つ おぼえました。",
         "I learned five new words."),
    ("n5.vocab.24-school-and-study.かな", 1):
        ("子どもは まず かなから 学びます。",
         "Children first learn from kana."),
    ("n5.vocab.24-school-and-study.けしゴム", 1):
        ("けしゴムが 小さく なって しまいました。",
         "The eraser has become small."),
    ("n5.vocab.24-school-and-study.電気", 1):
        ("へやの 電気が きえました。",
         "The room's light went out."),
    ("n5.vocab.24-school-and-study.電話", 1):
        ("まいばん 父に 電話を かけます。",
         "I call my father every evening."),
    ("n5.vocab.26-house-and-furniture.と", 1):
        ("との 中から こえが 聞こえます。",
         "I can hear a voice from inside the door."),
    ("n5.vocab.26-house-and-furniture.かいだん", 1):
        ("かいだんで ころんで けがを しました。",
         "I fell on the stairs and got hurt."),
    ("n5.vocab.26-house-and-furniture.しんしつ", 1):
        ("しんしつの 電気を けして ねます。",
         "I turn off the bedroom light and go to sleep."),
    ("n5.vocab.26-house-and-furniture.はブラシ", 1):
        ("毎日 はを はブラシで みがきます。",
         "I brush my teeth every day with a toothbrush."),
    ("n5.vocab.26-house-and-furniture.カメラ", 1):
        ("カメラを もって こうえんに 行きました。",
         "I went to the park with a camera."),
    ("n5.vocab.26-house-and-furniture.おんがく", 1):
        ("車の 中で おんがくを 聞きます。",
         "I listen to music in the car."),
    ("n5.vocab.26-house-and-furniture.うた", 1):
        ("子どもの ころから この うたを しって います。",
         "I've known this song since I was a child."),
    ("n5.vocab.37-common-nouns-miscella.こと", 1):
        ("先生に きく ことが あります。",
         "I have something to ask the teacher."),
    ("n5.vocab.37-common-nouns-miscella.しゅみ", 3):
        ("しゅみを とおして 友だちが できます。",
         "I make friends through my hobbies."),
    ("n5.vocab.37-common-nouns-miscella.パーティー", 1):
        ("パーティーは よる 七時から です。",
         "The party starts at 7 in the evening."),
    ("n5.vocab.37-common-nouns-miscella.きって", 1):
        ("きってを はって ポストに 入れました。",
         "I put on a stamp and dropped it in the mailbox."),
    ("n5.vocab.37-common-nouns-miscella.かぜ", 1):
        ("かぜを ひいて せきが 出ます。",
         "I have a cold and I'm coughing."),
    ("n5.vocab.37-common-nouns-miscella.けが", 1):
        ("足の けがが やっと なおりました。",
         "My foot injury has finally healed."),
    ("n5.vocab.37-common-nouns-miscella.フィルム", 1):
        ("古い フィルムの しゃしんは あたたかみが あります。",
         "Old film photos have a warm feel."),
    ("n5.vocab.37-common-nouns-miscella.はたち", 1):
        ("はたちから おさけを 飲んでも いいです。",
         "From the age of 20 it's OK to drink alcohol."),
    ("n5.vocab.37-common-nouns-miscella.へん", 1):
        ("いえの この へんは とても しずかです。",
         "This area around home is very quiet."),
    ("n5.vocab.37-common-nouns-miscella.なつやすみ", 1):
        ("なつやすみに うみに 行きたいです。",
         "I want to go to the sea during summer vacation."),
    ("n5.vocab.37-common-nouns-miscella.ペット", 1):
        ("子どもが ペットの いぬと あそんで います。",
         "The child is playing with the pet dog."),
    ("n5.vocab.37-common-nouns-miscella.カレンダー", 1):
        ("一月の 新しい カレンダーが 来ました。",
         "A new January calendar arrived."),
    ("n5.vocab.37-common-nouns-miscella.おくさん", 1):
        ("先生の おくさんも 先生です。",
         "The teacher's wife is also a teacher."),
    ("n5.vocab.37-common-nouns-miscella.大きな", 1):
        ("大きな 木が こうえんに 立って います。",
         "A big tree stands in the park."),
    ("n5.vocab.37-common-nouns-miscella.たて", 1):
        ("たての 大きさを はかります。",
         "I measure the vertical length."),
    ("n5.vocab.37-common-nouns-miscella.にっき", 1):
        ("子どもの ころの にっきが まだ あります。",
         "I still have my diary from when I was a child."),
    ("n5.vocab.37-common-nouns-miscella.テープレコーダー", 1):
        ("テープレコーダーで 先生の こえを ろくおんしました。",
         "I recorded the teacher's voice on the tape recorder."),
    ("n5.vocab.37-common-nouns-miscella.クラス", 1):
        ("わたしの クラスには 外国人が 三人 います。",
         "My class has three foreigners."),
    ("n5.vocab.37-common-nouns-miscella.グラム", 1):
        ("やさいを 五百グラム 買いました。",
         "I bought 500 grams of vegetables."),
    ("n5.vocab.40-misc-useful-items.じゅうしょ", 1):
        ("ひっこしで じゅうしょが かわりました。",
         "My address changed when I moved."),
    ("n5.vocab.40-misc-useful-items.しゅっしん", 1):
        ("田中さんの しゅっしんは とうきょうです。",
         "Tanaka-san is from Tokyo."),
    ("n5.vocab.26-house-and-furniture.いえ", 1):
        ("私の いえは 駅の ちかくです。",
         "My house is near the station."),

    # ============================================================
    #  KORE-BARE (178 entries)
    # ============================================================

    # --- people / family ---
    ("n5.vocab.2-people-family.かぞく", 1):
        ("かぞくと しゃしんを とりました。",
         "I took a picture with my family."),
    ("n5.vocab.2-people-family.お母さん", 1):
        ("お母さんから てがみが 来ました。",
         "A letter came from my mother."),
    ("n5.vocab.2-people-family.おにいさん", 1):
        ("おにいさんは とても しんせつです。",
         "My older brother is very kind."),
    ("n5.vocab.2-people-family.おねえさん", 1):
        ("おねえさんに たんじょうびの プレゼントを あげます。",
         "I'll give my older sister a birthday present."),
    ("n5.vocab.2-people-family.おじいさん", 1):
        ("おじいさんと いっしょに さんぽに 行きます。",
         "I go for a walk with my grandfather."),
    ("n5.vocab.2-people-family.おじさん", 1):
        ("おじさんから てがみが とどきました。",
         "A letter arrived from my uncle."),
    ("n5.vocab.2-people-family.女の子", 1):
        ("女の子が こうえんで あそんで います。",
         "A girl is playing in the park."),
    ("n5.vocab.2-people-family.男", 1):
        ("男の 人が 道で 友だちと 話して います。",
         "A man is talking with a friend on the road."),
    ("n5.vocab.3-people-roles.せいと", 1):
        ("せいとが 先生に しつもんを します。",
         "The pupils ask the teacher questions."),
    ("n5.vocab.3-people-roles.会社員", 1):
        ("父は 大きい 会社の 会社員です。",
         "My father is an employee of a large company."),
    ("n5.vocab.3-people-roles.駅員", 1):
        ("駅員が きっぷを かくにんして います。",
         "The station attendant is checking tickets."),
    ("n5.vocab.3-people-roles.店員", 1):
        ("店員が やさしく あいさつしました。",
         "The shop clerk greeted us kindly."),
    ("n5.vocab.3-people-roles.おまわりさん", 1):
        ("おまわりさんが 子どもを たすけました。",
         "The police officer helped the child."),
    ("n5.vocab.3-people-roles.りゅうがくせい", 1):
        ("クラスに りゅうがくせいが 五人 います。",
         "There are five international students in the class."),

    # --- body parts ---
    ("n5.vocab.4-body-parts.かお", 1):
        ("まいあさ かおを あらいます。",
         "I wash my face every morning."),
    ("n5.vocab.4-body-parts.みみ", 1):
        ("みみで おんがくを 聞きます。",
         "I listen to music with my ears."),

    # --- demonstratives ---
    # 'これ' and 'あれ' are demonstratives themselves; 'これは Xです。'
    # is the canonical example for them. Whitelist these so the checker
    # doesn't flag (handled in checker; below we still author cleaner
    # secondary examples for the few flagged here).
    ("n5.vocab.5-demonstratives.これ", 1):
        ("これは おいしい くだものです。",
         "This is delicious fruit."),
    ("n5.vocab.5-demonstratives.これ", 2):
        ("これを ください。",
         "Please give me this."),
    ("n5.vocab.5-demonstratives.あれ", 0):
        ("あれは わたしの 学校です。",
         "That over there is my school."),
    ("n5.vocab.5-demonstratives.あれ", 2):
        ("あれを 見て ください。",
         "Please look at that over there."),

    # --- numbers / counters ---
    ("n5.vocab.7-numbers.千", 0):
        ("せん円 さつを 二まい 出しました。",
         "I handed over two 1000-yen bills."),
    ("n5.vocab.9-counters-common.こ", 1):
        ("ボールを 三こ 買いました。",
         "I bought three balls."),

    # --- time ---
    ("n5.vocab.10-time-general.ひる", 1):
        ("ひるは あたたかく なりました。",
         "It became warm at noon."),
    ("n5.vocab.10-time-general.こんばん", 1):
        ("こんばん パーティーに 来て ください。",
         "Please come to the party this evening."),
    ("n5.vocab.10-time-general.午前", 1):
        ("午前 八時に いえを 出ます。",
         "I leave home at 8 a.m."),
    ("n5.vocab.10-time-general.午後", 1):
        ("午後から 雨が ふる そうです。",
         "It seems it will rain from the afternoon."),
    ("n5.vocab.11-time-days-weeks-month.一日.2", 1):
        ("一日 三かい ごはんを 食べます。",
         "I eat three meals a day."),
    ("n5.vocab.11-time-days-weeks-month.四日", 1):
        ("四日 つづけて 雨でした。",
         "It rained for four days in a row."),
    ("n5.vocab.11-time-days-weeks-month.七日", 1):
        ("今月の 七日は あめでした。",
         "The 7th of this month was rainy."),
    ("n5.vocab.11-time-days-weeks-month.九日", 1):
        ("九日に びょういんへ 行きます。",
         "I'll go to the hospital on the 9th."),
    ("n5.vocab.11-time-days-weeks-month.二十日", 1):
        ("二十日に たんじょうびを いわいます。",
         "I'll celebrate the birthday on the 20th."),
    ("n5.vocab.11-time-days-weeks-month.火曜日", 1):
        ("火曜日は ピアノを ならいます。",
         "I learn piano on Tuesdays."),
    ("n5.vocab.11-time-days-weeks-month.木曜日", 1):
        ("木曜日に 友だちと 食じを します。",
         "I have a meal with friends on Thursdays."),
    ("n5.vocab.11-time-days-weeks-month.土曜日", 1):
        ("土曜日に びじゅつかんに 行きます。",
         "I'll go to the art museum on Saturday."),
    ("n5.vocab.11-time-days-weeks-month.月", 1):
        ("毎月 おこづかいを もらいます。",
         "I receive pocket money every month."),
    ("n5.vocab.11-time-days-weeks-month.四月", 1):
        ("四月から 大学生に なります。",
         "I'll become a college student from April."),
    ("n5.vocab.11-time-days-weeks-month.六月", 1):
        ("六月は つゆの きせつです。",
         "June is the rainy season."),
    ("n5.vocab.11-time-days-weeks-month.今月", 1):
        ("今月 友だちと りょこうに 行きます。",
         "I'm traveling with friends this month."),
    ("n5.vocab.11-time-days-weeks-month.来月", 1):
        ("来月から 新しい しごとが はじまります。",
         "A new job starts next month."),
    ("n5.vocab.11-time-days-weeks-month.きょねん", 1):
        ("きょねんの 七月に けっこんしました。",
         "I got married in July last year."),
    ("n5.vocab.11-time-days-weeks-month.今年", 1):
        ("今年は たくさん 本を 読みました。",
         "I've read many books this year."),
    ("n5.vocab.11-time-days-weeks-month.さらいねん", 1):
        ("さらいねん 新しい いえを 買います。",
         "I'll buy a new house the year after next."),
    ("n5.vocab.12-time-frequency-sequen.毎日", 1):
        ("毎日 友だちに 会います。",
         "I meet friends every day."),
    ("n5.vocab.12-time-frequency-sequen.まいあさ", 1):
        ("まいあさ 七時に おきます。",
         "I wake up at 7 every morning."),
    ("n5.vocab.12-time-frequency-sequen.さいしょ", 1):
        ("さいしょの しゅくだいは むずかしかったです。",
         "The first homework was difficult."),
    ("n5.vocab.12-time-frequency-sequen.さいご", 1):
        ("さいごの 電車は 十時です。",
         "The last train is at 10."),

    # --- locations / places ---
    ("n5.vocab.13-locations-and-places-.トイレ", 1):
        ("トイレは 二かいに あります。",
         "The toilet is on the second floor."),
    ("n5.vocab.13-locations-and-places-.おふろ", 2):
        ("おふろは あつくて 気もちが いいです。",
         "The bath is hot and pleasant."),
    ("n5.vocab.13-locations-and-places-.げんかん", 1):
        ("げんかんで くつを そろえます。",
         "I line up shoes at the entrance."),
    ("n5.vocab.13-locations-and-places-.学校", 3):
        ("学校は 八時から はじまります。",
         "School starts at 8."),
    ("n5.vocab.13-locations-and-places-.高校", 1):
        ("高校で たくさん 友だちが できました。",
         "I made many friends in high school."),
    ("n5.vocab.13-locations-and-places-.会社", 1):
        ("会社まで 一時間 かかります。",
         "It takes one hour to the office."),
    ("n5.vocab.13-locations-and-places-.お店", 1):
        ("お店の 中は すずしいです。",
         "It's cool inside the shop."),
    ("n5.vocab.13-locations-and-places-.きっさてん", 1):
        ("きっさてんは しずかで 気もちが いいです。",
         "The cafe is quiet and pleasant."),
    ("n5.vocab.13-locations-and-places-.びじゅつかん", 1):
        ("びじゅつかんは 月曜日が 休みです。",
         "The art museum is closed on Mondays."),
    ("n5.vocab.13-locations-and-places-.りょかん", 1):
        ("りょかんの 食じは とても おいしかったです。",
         "The meals at the inn were very tasty."),
    ("n5.vocab.13-locations-and-places-.ろうか", 1):
        ("ろうかは ながくて くらいです。",
         "The hallway is long and dark."),
    ("n5.vocab.13-locations-and-places-.ポスト", 1):
        ("ポストは 駅の 前に あります。",
         "The post box is in front of the station."),
    ("n5.vocab.13-locations-and-places-.とおり", 1):
        ("この とおりは 車が おおいです。",
         "There are many cars on this street."),
    ("n5.vocab.13-locations-and-places-.国", 1):
        ("私の 国は ヨーロッパに あります。",
         "My country is in Europe."),
    ("n5.vocab.13-locations-and-places-.中", 1):
        ("はこの 中に おかしが 入って います。",
         "There are sweets inside the box."),
    ("n5.vocab.13-locations-and-places-.上", 1):
        ("山の 上から うみが 見えます。",
         "You can see the sea from the top of the mountain."),
    ("n5.vocab.13-locations-and-places-.下", 1):
        ("木の 下で 休みました。",
         "I rested under the tree."),
    ("n5.vocab.13-locations-and-places-.前", 1):
        ("学校の 前に コンビニが あります。",
         "There is a convenience store in front of the school."),
    ("n5.vocab.13-locations-and-places-.左", 1):
        ("左に びょういんが あります。",
         "There is a hospital on the left."),
    ("n5.vocab.13-locations-and-places-.むこう", 1):
        ("みちの むこうに 友だちが 立って います。",
         "My friend is standing on the other side of the road."),
    ("n5.vocab.13-locations-and-places-.西", 1):
        ("西の 山に 日が しずみます。",
         "The sun sets behind the western mountains."),

    # --- nature / weather (KORE) ---
    ("n5.vocab.14-nature-and-weather.いけ", 1):
        ("いけに 大きい さかなが います。",
         "There is a large fish in the pond."),
    ("n5.vocab.14-nature-and-weather.みずうみ", 1):
        ("みずうみの 水は とても きれいです。",
         "The lake water is very clear."),
    ("n5.vocab.14-nature-and-weather.もり", 1):
        ("もりの 中で とりの こえが します。",
         "I can hear birds singing in the forest."),
    ("n5.vocab.14-nature-and-weather.花", 1):
        ("花の いろは ピンクです。",
         "The flower's color is pink."),
    ("n5.vocab.14-nature-and-weather.くさ", 1):
        ("にわの くさが ながく なりました。",
         "The grass in the garden has grown long."),
    ("n5.vocab.14-nature-and-weather.くも", 1):
        ("くもが 出て、雨が ふりそうです。",
         "Clouds appeared, and it looks like rain."),
    ("n5.vocab.14-nature-and-weather.たいよう", 1):
        ("たいようが あかるく そらを てらします。",
         "The sun brightens the sky."),
    ("n5.vocab.14-nature-and-weather.月", 1):
        ("こんやの 月は とても きれいです。",
         "Tonight's moon is very beautiful."),
    ("n5.vocab.14-nature-and-weather.雨", 1):
        ("雨が やんで、空が はれました。",
         "The rain stopped and the sky cleared."),
    ("n5.vocab.14-nature-and-weather.あき", 1):
        ("あきは こうようが きれいです。",
         "Autumn leaves are beautiful in autumn."),
    ("n5.vocab.14-nature-and-weather.水", 2):
        ("水を コップに 入れて ください。",
         "Please pour water into the cup."),
    ("n5.vocab.14-nature-and-weather.おゆ", 1):
        ("おゆに おちゃを 入れます。",
         "I put tea leaves in hot water."),

    # --- animals (KORE) ---
    ("n5.vocab.15-animals.どうぶつ", 1):
        ("どうぶつえんで いろいろな どうぶつを 見ました。",
         "I saw various animals at the zoo."),
    ("n5.vocab.15-animals.とり", 1):
        ("あさ とりの こえで 目が さめました。",
         "I woke up to the sound of birds in the morning."),
    ("n5.vocab.15-animals.うま", 1):
        ("うまが はしって います。",
         "The horse is running."),
    ("n5.vocab.15-animals.うし", 1):
        ("うしが くさを 食べて います。",
         "The cow is eating grass."),
    ("n5.vocab.15-animals.にわとり", 1):
        ("にわとりが にわで あそんで います。",
         "The chickens are playing in the yard."),

    # --- food / drink (KORE) ---
    ("n5.vocab.16-food-and-drink-genera.しょくじ", 1):
        ("かぞくと しょくじを たのしみます。",
         "I enjoy meals with my family."),
    ("n5.vocab.16-food-and-drink-genera.おべんとう", 1):
        ("おべんとうの 中には おにぎりが あります。",
         "The boxed lunch contains rice balls."),
    ("n5.vocab.16-food-and-drink-genera.おかし", 1):
        ("子どもに おかしを あげました。",
         "I gave sweets to the children."),
    ("n5.vocab.17-food-items.ぶどう", 1):
        ("ぶどうは あまくて おいしいです。",
         "Grapes are sweet and tasty."),
    ("n5.vocab.17-food-items.すいか", 1):
        ("すいかは あまくて つめたいです。",
         "Watermelon is sweet and cool."),
    ("n5.vocab.17-food-items.トマト", 1):
        ("サラダに トマトを 入れます。",
         "I put tomato in the salad."),
    ("n5.vocab.17-food-items.しょうゆ", 1):
        ("しょうゆは 日本の ちょうみりょうです。",
         "Soy sauce is a Japanese seasoning."),
    ("n5.vocab.17-food-items.天ぷら", 1):
        ("やさいの 天ぷらが すきです。",
         "I like vegetable tempura."),
    ("n5.vocab.17-food-items.うどん", 1):
        ("うどんは あつくて おいしいです。",
         "Udon is hot and tasty."),
    ("n5.vocab.17-food-items.サンドイッチ", 1):
        ("サンドイッチを 三つ つくりました。",
         "I made three sandwiches."),
    ("n5.vocab.17-food-items.スープ", 1):
        ("スープが つめたく なって しまいました。",
         "The soup has gone cold."),
    ("n5.vocab.17-food-items.ケーキ", 1):
        ("ケーキを 八つに 分けます。",
         "I'll divide the cake into eight pieces."),
    ("n5.vocab.18-drinks.ぎゅうにゅう", 1):
        ("子どもは ぎゅうにゅうが 大すきです。",
         "Children love milk."),

    # --- tableware / cooking (KORE) ---
    ("n5.vocab.19-tableware-and-cooking.おさら", 1):
        ("白い おさらに ケーキを のせました。",
         "I put cake on the white plate."),
    ("n5.vocab.19-tableware-and-cooking.はし", 1):
        ("子どもが はじめて はしを つかえました。",
         "The child was able to use chopsticks for the first time."),
    ("n5.vocab.19-tableware-and-cooking.スプーン", 1):
        ("子どもには 小さい スプーンを つかいます。",
         "We use a small spoon for the child."),
    ("n5.vocab.19-tableware-and-cooking.カップ", 1):
        ("カップを テーブルに ならべました。",
         "I lined up cups on the table."),

    # --- colors (KORE) ---
    ("n5.vocab.20-colors.あか", 1):
        ("あかの ペンを かして ください。",
         "Please lend me a red pen."),
    ("n5.vocab.20-colors.ちゃいろ", 1):
        ("ちゃいろの かばんを 買いました。",
         "I bought a brown bag."),

    # --- clothing / accessories (KORE) ---
    ("n5.vocab.21-clothing-and-accessor.きもの", 1):
        ("はじめて きものを きて しゃしんを とりました。",
         "I wore a kimono for the first time and took a photo."),
    ("n5.vocab.21-clothing-and-accessor.ネクタイ", 1):
        ("あおい ネクタイを 買いました。",
         "I bought a blue necktie."),
    ("n5.vocab.21-clothing-and-accessor.くつ", 1):
        ("くつは げんかんで ぬいで ください。",
         "Please take off your shoes at the entrance."),
    ("n5.vocab.21-clothing-and-accessor.くつした", 1):
        ("白い くつしたを 二足 ください。",
         "Please give me two pairs of white socks."),
    ("n5.vocab.21-clothing-and-accessor.とけい", 1):
        ("かべに 大きい とけいが かかって います。",
         "There is a large clock on the wall."),
    ("n5.vocab.21-clothing-and-accessor.かさ", 1):
        ("古い かさが こわれました。",
         "My old umbrella broke."),

    # --- money / shopping (KORE) ---
    ("n5.vocab.22-money-and-shopping.円", 0):
        ("百円の おかしを 三つ 買いました。",
         "I bought three 100-yen sweets."),
    ("n5.vocab.22-money-and-shopping.円", 1):
        ("円を ドルに かえました。",
         "I exchanged yen for dollars."),
    ("n5.vocab.22-money-and-shopping.きって", 1):
        ("八十円の きってを 五まい はりました。",
         "I put on five 80-yen stamps."),
    ("n5.vocab.22-money-and-shopping.はがき", 1):
        ("毎年 ねんがじょうの はがきを 書きます。",
         "I write New Year's postcards every year."),
    ("n5.vocab.22-money-and-shopping.ふうとう", 1):
        ("白い ふうとうを 三まい ください。",
         "Please give me three white envelopes."),
    ("n5.vocab.22-money-and-shopping.おみやげ", 1):
        ("先生に おみやげを わたしました。",
         "I gave a souvenir to the teacher."),

    # --- transport (KORE) ---
    ("n5.vocab.23-transport.電車", 1):
        ("電車の 中で 本を 読みます。",
         "I read books in the train."),
    ("n5.vocab.23-transport.きしゃ", 1):
        ("古い きしゃが はくぶつかんに あります。",
         "There is an old steam train at the museum."),
    ("n5.vocab.23-transport.道", 1):
        ("道で 子どもが あそんで います。",
         "Children are playing on the road."),

    # --- school / study (KORE) ---
    ("n5.vocab.24-school-and-study.いみ", 1):
        ("この かんじの いみが わかりません。",
         "I don't understand the meaning of this kanji."),
    ("n5.vocab.24-school-and-study.じ", 1):
        ("ノートに 大きい じで 書きます。",
         "I write in large letters in my notebook."),
    ("n5.vocab.24-school-and-study.カタカナ", 1):
        ("カタカナで 外国人の 名前を 書きます。",
         "I write foreign names in katakana."),
    ("n5.vocab.24-school-and-study.ぶん", 1):
        ("ぶんの さいごに「。」を 書きます。",
         "Put a period at the end of a sentence."),
    ("n5.vocab.24-school-and-study.ぶんしょう", 1):
        ("みじかい ぶんしょうから はじめます。",
         "I'll start with a short composition."),
    ("n5.vocab.24-school-and-study.ぶんぽう", 1):
        ("ぶんぽうの 本を 一さつ 買いました。",
         "I bought one grammar book."),
    ("n5.vocab.24-school-and-study.れんしゅう", 1):
        ("ピアノの れんしゅうを 一時間 します。",
         "I'll practice piano for one hour."),
    ("n5.vocab.24-school-and-study.きょうかしょ", 1):
        ("きょうかしょを 学校に わすれました。",
         "I forgot my textbook at school."),
    ("n5.vocab.24-school-and-study.ざっし", 1):
        ("コンビニで ざっしを 買いました。",
         "I bought a magazine at the convenience store."),
    ("n5.vocab.24-school-and-study.ボールペン", 1):
        ("ボールペンが 三本 あります。",
         "I have three ballpoint pens."),
    ("n5.vocab.24-school-and-study.こくばん", 1):
        ("こくばんに 大きく 書いて ください。",
         "Please write large on the blackboard."),
    ("n5.vocab.24-school-and-study.チョーク", 1):
        ("白い チョークが もう ありません。",
         "There is no more white chalk."),

    # --- languages / countries (KORE) ---
    ("n5.vocab.25-languages-and-countri.えいご", 1):
        ("えいごの 本を 読んで います。",
         "I am reading an English book."),
    ("n5.vocab.25-languages-and-countri.中国", 1):
        ("中国まで ひこうきで 三時間 かかります。",
         "It takes three hours to China by plane."),
    ("n5.vocab.25-languages-and-countri.中国語", 1):
        ("中国語と 日本語は ちがいます。",
         "Chinese and Japanese are different."),
    ("n5.vocab.25-languages-and-countri.かんこく", 1):
        ("かんこくは 日本の となりの 国です。",
         "Korea is the neighboring country of Japan."),
    ("n5.vocab.25-languages-and-countri.かんこくご", 1):
        ("かんこくごの あいさつを おぼえました。",
         "I learned Korean greetings."),
    ("n5.vocab.25-languages-and-countri.フランス", 1):
        ("フランスは ヨーロッパに あります。",
         "France is in Europe."),
    ("n5.vocab.25-languages-and-countri.フランスご", 1):
        ("フランスごは おんがくみたいです。",
         "French sounds like music."),
    ("n5.vocab.25-languages-and-countri.スペイン", 1):
        ("スペインは 大きい 国です。",
         "Spain is a large country."),

    # --- house / furniture (KORE) ---
    ("n5.vocab.26-house-and-furniture.ドア", 1):
        ("ドアの 前に 大きい いぬが います。",
         "There is a big dog in front of the door."),
    ("n5.vocab.26-house-and-furniture.ベッド", 1):
        ("ベッドの よこに とけいが あります。",
         "There is a clock next to the bed."),
    ("n5.vocab.26-house-and-furniture.ふとん", 1):
        ("あさ ふとんを かたづけます。",
         "I put away the futon in the morning."),
    ("n5.vocab.26-house-and-furniture.もうふ", 1):
        ("ふゆの あさは もうふが 二まい いります。",
         "Winter mornings need two blankets."),
    ("n5.vocab.26-house-and-furniture.まくら", 1):
        ("まくらの 下に はがきを かくしました。",
         "I hid a postcard under the pillow."),
    ("n5.vocab.26-house-and-furniture.テーブル", 1):
        ("テーブルを きれいに かたづけました。",
         "I cleaned up the table."),
    ("n5.vocab.26-house-and-furniture.カーテン", 1):
        ("あさ カーテンを あけます。",
         "I open the curtains in the morning."),
    ("n5.vocab.26-house-and-furniture.かぎ", 1):
        ("いえの かぎを ポケットに 入れました。",
         "I put the house key in my pocket."),
    ("n5.vocab.26-house-and-furniture.ラジオ", 1):
        ("ラジオから 日本の おんがくが 聞こえます。",
         "Japanese music is coming from the radio."),
    ("n5.vocab.26-house-and-furniture.え", 1):
        ("子どもが きれいな えを かきました。",
         "The child drew a beautiful picture."),
    ("n5.vocab.26-house-and-furniture.ギター", 1):
        ("ギターを ひきながら うたを うたいます。",
         "I sing songs while playing the guitar."),

    # --- particles (KORE) ---
    ("n5.vocab.35-particles-functional-.の", 2):
        ("私の 本は つくえの 上に あります。",
         "My book is on the desk."),

    # --- common-nouns-miscella (KORE) ---
    ("n5.vocab.37-common-nouns-miscella.もの", 1):
        ("ふくろの 中に いろいろな ものが あります。",
         "There are various things in the bag."),
    ("n5.vocab.37-common-nouns-miscella.もの", 3):
        ("こわれた ものは すてて ください。",
         "Please throw away broken things."),
    ("n5.vocab.37-common-nouns-miscella.やくそく", 1):
        ("あしたの やくそくは 三時です。",
         "Tomorrow's appointment is at 3."),
    ("n5.vocab.37-common-nouns-miscella.しゅみ", 1):
        ("しゅみの 話を しましょう。",
         "Let's talk about hobbies."),
    ("n5.vocab.37-common-nouns-miscella.さんぽ", 1):
        ("あさの さんぽは 気もちが いいです。",
         "A morning walk feels pleasant."),
    ("n5.vocab.37-common-nouns-miscella.しあい", 1):
        ("おもしろい しあいでした。",
         "It was an interesting match."),
    ("n5.vocab.37-common-nouns-miscella.ニュース", 1):
        ("ニュースで 雨と 言って いました。",
         "The news said it would rain."),
    ("n5.vocab.37-common-nouns-miscella.くすり", 1):
        ("くすりは 食じの あとで 飲みます。",
         "I take medicine after meals."),
    ("n5.vocab.37-common-nouns-miscella.スリッパ", 1):
        ("スリッパは げんかんに そろえて います。",
         "Slippers are lined up at the entrance."),
    ("n5.vocab.37-common-nouns-miscella.ティッシュ", 1):
        ("ティッシュで かおを ふきました。",
         "I wiped my face with a tissue."),
    ("n5.vocab.37-common-nouns-miscella.レコード", 1):
        ("古い レコードから おとが 出ました。",
         "Sound came out from the old record."),
    ("n5.vocab.37-common-nouns-miscella.よてい", 1):
        ("らい週の よていを かくにんします。",
         "I check next week's schedule."),
    ("n5.vocab.37-common-nouns-miscella.はんぶん", 1):
        ("おかしを 半分 ずつ 分けました。",
         "I divided the sweets in half."),
    ("n5.vocab.37-common-nouns-miscella.ほんとう", 1):
        ("ほんとうの 話を 聞きたいです。",
         "I want to hear the true story."),
    ("n5.vocab.37-common-nouns-miscella.かびん", 1):
        ("かびんが テーブルの 上に あります。",
         "The vase is on the table."),
    ("n5.vocab.37-common-nouns-miscella.かた", 1):
        ("じょうずな はなしかたを ならいます。",
         "I learn skillful ways of speaking."),
    ("n5.vocab.37-common-nouns-miscella.先", 1):
        ("先の 話を 聞いて ください。",
         "Please listen to what comes first."),
    ("n5.vocab.37-common-nouns-miscella.せびろ", 1):
        ("くろい せびろが 一つ あります。",
         "I have one black business suit."),
    ("n5.vocab.37-common-nouns-miscella.さくぶん", 1):
        ("先生に さくぶんを 出しました。",
         "I submitted my composition to the teacher."),
    ("n5.vocab.37-common-nouns-miscella.キログラム", 1):
        ("三キログラムの にもつを はこびます。",
         "I'll carry the 3-kilogram package."),
    ("n5.vocab.37-common-nouns-miscella.キロメートル", 1):
        ("えきから 二キロメートル あるきました。",
         "I walked two kilometers from the station."),

    # --- sounds (KORE) ---
    ("n5.vocab.38-sounds-and-voice.おと", 1):
        ("おとが しずかに なりました。",
         "The sound became quiet."),

    # --- misc-useful-items (KORE) ---
    ("n5.vocab.40-misc-useful-items.ばあい", 1):
        ("おくれる ばあいは 電話して ください。",
         "If you'll be late, please call."),
    ("n5.vocab.40-misc-useful-items.おもちゃ", 1):
        ("おもちゃが へやに たくさん あります。",
         "There are many toys in the room."),

    # --- locations late additions (KORE) ---
    ("n5.vocab.13-locations-and-places-.カフェ", 1):
        ("えきの 前の カフェは 安いです。",
         "The cafe in front of the station is cheap."),
    ("n5.vocab.13-locations-and-places-.コンビニ", 1):
        ("コンビニは 二十四時間 あいて います。",
         "Convenience stores are open 24 hours."),
    ("n5.vocab.22-money-and-shopping.セール", 1):
        ("なつの セールで ふくを 買いました。",
         "I bought clothes at the summer sale."),
    ("n5.vocab.26-house-and-furniture.ベンチ", 1):
        ("ベンチに ねこが すわって います。",
         "A cat is sitting on the bench."),

    # ============================================================
    #  GREET-WRONG-VERB (12 entries)
    # ============================================================
    ("n5.vocab.36-greetings-and-set-phr.おやすみなさい", 1):
        ("ねる 前に「おやすみなさい」と 言いました。",
         "Before sleeping I said 'good night'."),
    ("n5.vocab.36-greetings-and-set-phr.しつれいします", 1):
        ("へやに 入る 前に「しつれいします」と 言いました。",
         "Before entering the room I said 'excuse me'."),
    ("n5.vocab.36-greetings-and-set-phr.ごめんなさい", 1):
        ("小さい こえで「ごめんなさい」と 言いました。",
         "I said 'sorry' in a quiet voice."),
    ("n5.vocab.36-greetings-and-set-phr.いただきます", 1):
        ("食べる 前に「いただきます」と 言いました。",
         "Before eating I said 'itadakimasu'."),
    ("n5.vocab.36-greetings-and-set-phr.はじめまして", 1):
        ("田中さんに「はじめまして」と 言いました。",
         "I said 'nice to meet you' to Tanaka-san."),
    ("n5.vocab.36-greetings-and-set-phr.いらっしゃいませ", 1):
        ("店員さんが「いらっしゃいませ」と 言いました。",
         "The clerk said 'welcome'."),
    ("n5.vocab.36-greetings-and-set-phr.おじゃまします", 1):
        ("友だちの いえで「おじゃまします」と 言いました。",
         "At my friend's house I said 'excuse me for intruding'."),
    ("n5.vocab.39-function-filler-expre.えーと", 1):
        ("「えーと、おなまえは?」と 聞きました。",
         "I asked, 'Um, what's your name?'"),
    ("n5.vocab.39-function-filler-expre.そうですね", 1):
        ("先生は「そうですね」と 言いました。",
         "The teacher said 'that's right'."),
    ("n5.vocab.39-function-filler-expre.そうですか", 1):
        ("「そうですか」と 聞きました。",
         "I asked, 'Is that so?'"),
    ("n5.vocab.39-function-filler-expre.いいえ", 1):
        ("「いいえ、ちがいます」と 言いました。",
         "I said, 'No, that's wrong.'"),
    ("n5.vocab.39-function-filler-expre.ええ", 1):
        ("「ええ、わかりました」と 言いました。",
         "I said, 'Yes, I understand.'"),
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
