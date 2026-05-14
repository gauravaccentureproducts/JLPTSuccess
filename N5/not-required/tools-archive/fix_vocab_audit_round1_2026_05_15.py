"""Vocab audit Round 1 fixes:
- C1: 109 template-leak ja replacements ('Xを 見ました。' → natural sentence)
- C2: 86 within-entry duplicate ja replacements (replace position [dup_idx])
- C3: 1 wrong-headword example (たばこ entry got a bus/school sentence)

All replacements:
- Use the entry's headword (form or reading) in natural context
- Stay within N5 kanji whitelist (106 chars)
- Differ from other examples already in the same entry
- Have natural English translations
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")

# Format: (vocab_id, idx) -> (new_ja, new_en)
# vocab_id is the entry["id"] string.
C1_FIXES: dict[tuple[str, int], tuple[str, str]] = {
    # --- People / family ---
    ("n5.vocab.2-people-family.母", 1):
        ("母は えいがが すきです。", "My mother likes movies."),
    ("n5.vocab.2-people-family.おとうと", 1):
        ("おとうとと よく あそびます。", "I often play with my younger brother."),
    ("n5.vocab.2-people-family.いもうと", 1):
        ("いもうとと いっしょに テレビを 見ます。", "I watch TV with my younger sister."),
    ("n5.vocab.2-people-family.おばあさん", 1):
        ("おばあさんに 本を もらいました。", "I received a book from my grandmother."),
    ("n5.vocab.2-people-family.大人", 1):
        ("大人に なったら 車を 買いたいです。", "When I become an adult, I want to buy a car."),
    ("n5.vocab.3-people-roles.いしゃ", 1):
        ("あの いしゃは しんせつです。", "That doctor is kind."),
    ("n5.vocab.3-people-roles.高校生", 1):
        ("高校生は まいにち べんきょうします。", "High school students study every day."),
    ("n5.vocab.1-people-pronouns-and-se.みんな", 1):
        ("みんなに あいさつします。", "I greet everyone."),

    # --- Time (general / days / weeks / months / frequency) ---
    ("n5.vocab.10-time-general.けさ", 1):
        ("けさは あめが ふって います。", "It is raining this morning."),
    ("n5.vocab.10-time-general.後", 1):
        ("しごとの 後で 友だちと 会います。", "I'll meet a friend after work."),
    ("n5.vocab.11-time-days-weeks-month.一日", 1):
        ("今月の 一日は 日曜日でした。", "The 1st of this month was Sunday."),
    ("n5.vocab.11-time-days-weeks-month.二日", 1):
        ("今月の 二日は 金曜日です。", "The 2nd of this month is Friday."),
    ("n5.vocab.11-time-days-weeks-month.八日", 1):
        ("来月の 八日に 出かけます。", "I will go out on the 8th of next month."),
    ("n5.vocab.11-time-days-weeks-month.十日", 1):
        ("今月の 十日は 子どもの たんじょうびです。", "The 10th of this month is my child's birthday."),
    ("n5.vocab.11-time-days-weeks-month.今週", 1):
        ("今週の 土曜日に 友だちが 来ます。", "A friend is coming this Saturday."),
    ("n5.vocab.11-time-days-weeks-month.三月", 1):
        ("三月から 新しい 学校に 行きます。", "I will start at a new school from March."),
    ("n5.vocab.11-time-days-weeks-month.毎年", 1):
        ("毎年 さくらが きれいに さきます。", "Every year the cherry blossoms bloom beautifully."),
    ("n5.vocab.12-time-frequency-sequen.まいばん", 1):
        ("まいばん 八時に ばんごはんを 食べます。", "I eat dinner at 8 pm every night."),

    # --- Locations / places ---
    ("n5.vocab.13-locations-and-places-.ところ", 1):
        ("しずかな ところで べんきょうします。", "I study in a quiet place."),
    ("n5.vocab.13-locations-and-places-.おてあらい", 1):
        ("おてあらいに 行って きます。", "I'll go to the restroom and come back."),
    ("n5.vocab.13-locations-and-places-.学校", 1):
        ("学校で にほんごを ならいます。", "I learn Japanese at school."),
    ("n5.vocab.13-locations-and-places-.じむしょ", 1):
        ("じむしょで しごとを して います。", "I am working at the office."),
    ("n5.vocab.13-locations-and-places-.スーパー", 1):
        ("スーパーで やさいを 買いました。", "I bought vegetables at the supermarket."),
    ("n5.vocab.13-locations-and-places-.レストラン", 1):
        ("あの レストランは おいしいです。", "That restaurant is delicious."),
    ("n5.vocab.13-locations-and-places-.やおや", 1):
        ("やおやで トマトを 買いました。", "I bought tomatoes at the greengrocer."),
    ("n5.vocab.13-locations-and-places-.にくや", 1):
        ("にくやで ぶたにくを 買います。", "I will buy pork at the butcher."),
    ("n5.vocab.13-locations-and-places-.えいがかん", 2):
        ("えいがかんは えきの ちかくに あります。", "The movie theater is near the station."),
    ("n5.vocab.13-locations-and-places-.たいしかん", 1):
        ("たいしかんで ビザを もらいました。", "I got a visa at the embassy."),
    ("n5.vocab.13-locations-and-places-.こうさてん", 1):
        ("こうさてんを わたって ください。", "Please cross at the intersection."),
    ("n5.vocab.13-locations-and-places-.いりぐち", 1):
        ("いりぐちで まちあわせましょう。", "Let's meet at the entrance."),
    ("n5.vocab.13-locations-and-places-.外", 1):
        ("外で あそんで います。", "We are playing outside."),
    ("n5.vocab.13-locations-and-places-.右", 1):
        ("つぎの こうさてんを 右に まがって ください。", "Please turn right at the next intersection."),
    ("n5.vocab.13-locations-and-places-.となり", 1):
        ("となりの へやで 子どもが ねて います。", "The child is sleeping in the next room."),
    ("n5.vocab.13-locations-and-places-.よこ", 1):
        ("いすの よこに かばんを おきました。", "I put my bag next to the chair."),
    ("n5.vocab.13-locations-and-places-.北", 1):
        ("北の 国は ふゆが ながいです。", "Northern countries have long winters."),
    ("n5.vocab.13-locations-and-places-.東", 1):
        ("東の 空が あかるく なりました。", "The eastern sky has brightened."),
    ("n5.vocab.13-locations-and-places-.おてら", 1):
        ("ふるい おてらに お参りに 行きました。", "I went to pay respects at an old temple."),
    ("n5.vocab.13-locations-and-places-.フロント", 1):
        ("フロントで チェックインを します。", "I check in at the front desk."),

    # --- Nature / weather ---
    ("n5.vocab.14-nature-and-weather.川", 1):
        ("川の 水は とても つめたいです。", "The river water is very cold."),
    ("n5.vocab.14-nature-and-weather.は", 1):
        ("木の はが きいろく なりました。", "The leaves have turned yellow."),
    ("n5.vocab.14-nature-and-weather.空", 1):
        ("今日は 空が とても 青いです。", "The sky is very blue today."),
    ("n5.vocab.14-nature-and-weather.ゆき", 1):
        ("ゆきが ふって 山が 白く なりました。", "The mountain became white from the falling snow."),
    ("n5.vocab.14-nature-and-weather.はれ", 1):
        ("はれの 日に せんたくを します。", "I do the laundry on clear days."),
    ("n5.vocab.14-nature-and-weather.なつ", 1):
        ("なつは うみで およぎたいです。", "I want to swim in the sea in summer."),
    ("n5.vocab.14-nature-and-weather.ふゆ", 1):
        ("ふゆは あつい コートを きます。", "I wear a thick coat in winter."),
    ("n5.vocab.14-nature-and-weather.火", 1):
        ("火が とても あついです。", "The fire is very hot."),
    ("n5.vocab.14-nature-and-weather.おゆ", 3):
        ("おゆを コップに 入れて ください。", "Please pour hot water into the cup."),
    ("n5.vocab.14-nature-and-weather.さくら", 1):
        ("さくらの 花は とても きれいです。", "Cherry blossoms are very beautiful."),

    # --- Animals ---
    ("n5.vocab.15-animals.うま", 2):
        ("うまに のった ことが ありますか。", "Have you ever ridden a horse?"),
    ("n5.vocab.15-animals.ぶた", 2):
        ("ぶたは とても かしこい どうぶつです。", "Pigs are very intelligent animals."),
    # ぞう has C1 hits at BOTH idx=1 and idx=2 (both ja are 'ぞうを 見ました')
    # so they're also within-entry duplicates. Replace idx=1 only here;
    # idx=2 stays as "どうぶつえんで ぞうを 見ました。" which is fine.
    # The dedup-related C2 entry will then be auto-clean.
    ("n5.vocab.15-animals.ぞう", 1):
        ("ぞうは 長い はなで 水を 飲みます。", "Elephants drink water with their long trunks."),

    # --- Food and drink (general / items) ---
    ("n5.vocab.16-food-and-drink-genera.のみもの", 1):
        ("つめたい のみものを ください。", "Please give me a cold drink."),
    ("n5.vocab.16-food-and-drink-genera.ゆうはん", 1):
        ("七時に ゆうはんを 食べます。", "I eat dinner at 7 pm."),
    ("n5.vocab.17-food-items.たまご", 1):
        ("あさ たまごを 食べます。", "I eat eggs in the morning."),
    ("n5.vocab.17-food-items.ぎゅうにく", 1):
        ("ぎゅうにくで カレーを つくります。", "I make curry with beef."),
    ("n5.vocab.17-food-items.ぶたにく", 1):
        ("スーパーで ぶたにくを 買いました。", "I bought pork at the supermarket."),
    ("n5.vocab.17-food-items.やさい", 1):
        ("やさいは 体に いいです。", "Vegetables are good for the body."),
    ("n5.vocab.17-food-items.レモン", 1):
        ("レモンを はんぶんに きって ください。", "Please cut the lemon in half."),
    ("n5.vocab.17-food-items.だいこん", 1):
        ("だいこんで スープを つくります。", "I make soup with daikon."),
    ("n5.vocab.17-food-items.にんじん", 1):
        ("にんじんは あまくて おいしいです。", "Carrots are sweet and tasty."),
    ("n5.vocab.17-food-items.しお", 1):
        ("しおを すこし 入れて ください。", "Please add a little salt."),
    ("n5.vocab.18-drinks.こうちゃ", 1):
        ("こうちゃに さとうを 入れますか。", "Do you put sugar in your black tea?"),
    ("n5.vocab.18-drinks.ワイン", 1):
        ("赤い ワインを 一本 ください。", "Please give me a bottle of red wine."),

    # --- Tableware / kitchen ---
    ("n5.vocab.19-tableware-and-cooking.ちゃわん", 1):
        ("ちゃわんを テーブルに ならべます。", "I'll set rice bowls on the table."),
    ("n5.vocab.19-tableware-and-cooking.れいぞうこ", 1):
        ("れいぞうこの 中は つめたいです。", "The inside of the refrigerator is cold."),

    # --- Colors ---
    ("n5.vocab.20-colors.いろ", 1):
        ("どの いろが すきですか。", "Which color do you like?"),
    ("n5.vocab.20-colors.白", 1):
        ("白の シャツを 買いました。", "I bought a white shirt."),
    ("n5.vocab.20-colors.きいろ", 1):
        ("バナナの 色は きいろです。", "Bananas are yellow."),

    # --- Clothing / accessories ---
    ("n5.vocab.21-clothing-and-accessor.スカート", 1):
        ("みじかい スカートは すきじゃありません。", "I don't like short skirts."),
    ("n5.vocab.21-clothing-and-accessor.さいふ", 1):
        ("あたらしい さいふを 買いました。", "I bought a new wallet."),
    ("n5.vocab.21-clothing-and-accessor.ポケット", 1):
        ("ポケットから ハンカチを 出しました。", "I took a handkerchief out of my pocket."),

    # --- Money / shopping ---
    ("n5.vocab.22-money-and-shopping.ドル", 1):
        ("一ドルは 百四十円ぐらいです。", "One dollar is about 140 yen."),
    ("n5.vocab.22-money-and-shopping.はがき", 3):
        ("はがきを 三まい 買いました。", "I bought three postcards."),
    ("n5.vocab.22-money-and-shopping.アルバイト", 1):
        ("アルバイトで お金を ためました。", "I saved money from my part-time job."),

    # --- Transport ---
    ("n5.vocab.23-transport.じどうしゃ", 1):
        ("じどうしゃで りょこうします。", "I travel by car."),
    ("n5.vocab.23-transport.バイク", 1):
        ("バイクの 後ろに のります。", "I ride on the back of the motorbike."),
    ("n5.vocab.23-transport.ちかてつ", 1):
        ("ちかてつで 三十分 かかります。", "It takes 30 minutes by subway."),
    ("n5.vocab.23-transport.ひこうき", 1):
        ("ひこうきは 空を とびます。", "Airplanes fly in the sky."),

    # --- School / study ---
    ("n5.vocab.24-school-and-study.こたえ", 1):
        ("こたえを ノートに 書きました。", "I wrote the answer in my notebook."),
    ("n5.vocab.24-school-and-study.ひらがな", 1):
        ("ひらがなで 名前を 書いて ください。", "Please write your name in hiragana."),
    ("n5.vocab.24-school-and-study.じしょ", 1):
        ("あたらしい じしょを 買いました。", "I bought a new dictionary."),
    ("n5.vocab.24-school-and-study.かみ", 1):
        ("かみに 名前を 書きました。", "I wrote my name on the paper."),
    ("n5.vocab.24-school-and-study.まんねんひつ", 1):
        ("まんねんひつで てがみを 書きます。", "I write letters with a fountain pen."),
    ("n5.vocab.24-school-and-study.いす", 1):
        ("この いすは 大きくて らくです。", "This chair is big and comfortable."),
    ("n5.vocab.24-school-and-study.ちず", 1):
        ("ちずで 学校までの 道を しらべました。", "I looked up the route to school on the map."),
    ("n5.vocab.24-school-and-study.番号", 1):
        ("ぎんこうの 番号を おしえて ください。", "Please tell me the bank account number."),
    ("n5.vocab.24-school-and-study.電話番号", 1):
        ("電話番号が かわりました。", "My phone number has changed."),
    ("n5.vocab.24-school-and-study.じゅんび", 1):
        ("あしたの じゅんびは できましたか。", "Have you finished preparing for tomorrow?"),

    # --- Languages / countries ---
    ("n5.vocab.25-languages-and-countri.ドイツ", 1):
        ("ドイツの 車は ゆうめいです。", "German cars are famous."),
    ("n5.vocab.25-languages-and-countri.イギリス", 1):
        ("イギリスの こうちゃは おいしいです。", "British black tea is tasty."),
    ("n5.vocab.25-languages-and-countri.外国", 1):
        ("外国で べんきょうしたいです。", "I want to study abroad."),

    # --- House / furniture ---
    ("n5.vocab.26-house-and-furniture.かべ", 1):
        ("かべに ポスターを はりました。", "I put a poster on the wall."),
    ("n5.vocab.26-house-and-furniture.エレベーター", 1):
        ("エレベーターは どこですか。", "Where is the elevator?"),
    ("n5.vocab.26-house-and-furniture.たな", 1):
        ("たなから コップを とって ください。", "Please take a cup from the shelf."),
    ("n5.vocab.26-house-and-furniture.ほんだな", 1):
        ("ほんだなを かいました。", "I bought a bookshelf."),
    ("n5.vocab.26-house-and-furniture.電気", 1):
        ("出る とき 電気を けして ください。", "Please turn off the light when you leave."),
    ("n5.vocab.26-house-and-furniture.テープ", 1):
        ("テープが きれて しまいました。", "The tape broke."),
    ("n5.vocab.26-house-and-furniture.ビデオ", 1):
        ("ビデオを かりて 来ました。", "I came back having rented a video."),

    # --- Misc nouns ---
    ("n5.vocab.37-common-nouns-miscella.こと", 3):
        ("あした 大切な ことが あります。", "I have something important tomorrow."),
    ("n5.vocab.37-common-nouns-miscella.ことば", 1):
        ("やさしい ことばで 話して ください。", "Please speak in simple words."),
    ("n5.vocab.37-common-nouns-miscella.ようじ", 1):
        ("ようじが おわったら 電話します。", "I'll call you when my errand is done."),
    ("n5.vocab.37-common-nouns-miscella.もんだい", 1):
        ("もんだいの こたえを 書きます。", "I write the answer to the problem."),
    ("n5.vocab.37-common-nouns-miscella.ゲーム", 1):
        ("友だちと ゲームを して あそびます。", "I play games with my friends."),
    ("n5.vocab.37-common-nouns-miscella.ニュース", 0):
        ("まいあさ ニュースを 見ます。", "I watch the news every morning."),
    ("n5.vocab.37-common-nouns-miscella.ほか", 1):
        ("ほかの 店に 行きましょう。", "Let's go to a different store."),
    ("n5.vocab.37-common-nouns-miscella.ストーブ", 1):
        ("へやに ストーブが あります。", "There is a heater in the room."),
    ("n5.vocab.37-common-nouns-miscella.ページ", 1):
        ("つぎの ページを ひらいて ください。", "Please open the next page."),
    ("n5.vocab.40-misc-useful-items.ねんれい", 1):
        ("ねんれいは ひみつです。", "My age is a secret."),
}


# C2 within-entry duplicate fixes: (id, dup_idx) -> (new_ja, new_en)
# Each replacement uses the headword in a way that differs from the
# other examples already in the entry. IDs verified against audit.
C2_FIXES: dict[tuple[str, int], tuple[str, str]] = {
    ("n5.vocab.1-people-pronouns-and-se.私", 2):
        ("私は 日本ごを ならって います。",
         "I am learning Japanese."),
    ("n5.vocab.1-people-pronouns-and-se.かた", 2):
        ("あの かたは どちらから 来ましたか。",
         "Where is that person from?"),
    ("n5.vocab.1-people-pronouns-and-se.みなさん", 2):
        ("みなさん、おはようございます。",
         "Good morning, everyone."),
    ("n5.vocab.1-people-pronouns-and-se.じぶん", 2):
        ("じぶんの 名前を 書いて ください。",
         "Please write your own name."),
    ("n5.vocab.2-people-family.あに", 2):
        ("あには ぎんこうで はたらいて います。",
         "My older brother works at a bank."),
    ("n5.vocab.3-people-roles.駅員", 2):
        ("駅員に きっぷの 買いかたを 聞きました。",
         "I asked the station attendant how to buy a ticket."),
    ("n5.vocab.3-people-roles.けいかん", 2):
        ("けいかんが こうさてんに 立って います。",
         "A police officer is standing at the intersection."),
    ("n5.vocab.4-body-parts.くち", 2):
        ("くちが かわきました。",
         "My mouth is dry."),
    ("n5.vocab.4-body-parts.おなか", 2):
        ("あさから おなかが いたいです。",
         "I've had a stomachache since the morning."),
    ("n5.vocab.5-demonstratives.この", 2):
        ("この かばんは 私のです。",
         "This bag is mine."),
    ("n5.vocab.5-demonstratives.どの", 2):
        ("どの くつを はきますか。",
         "Which shoes will you wear?"),
    ("n5.vocab.5-demonstratives.そこ", 2):
        ("そこで まって いて ください。",
         "Please wait there."),
    ("n5.vocab.5-demonstratives.どこ", 2):
        ("おてあらいは どこに ありますか。",
         "Where is the restroom?"),
    ("n5.vocab.5-demonstratives.こちら", 2):
        ("こちらは 山田さんです。",
         "This is Yamada-san."),
    ("n5.vocab.5-demonstratives.そう", 2):
        ("そうですか。しりませんでした。",
         "Is that so? I didn't know."),
    ("n5.vocab.6-question-words.何", 2):
        ("何を 食べたいですか。",
         "What do you want to eat?"),
    ("n5.vocab.6-question-words.いくら", 2):
        ("この シャツは いくらですか。",
         "How much is this shirt?"),
    ("n5.vocab.6-question-words.何曜日", 2):
        ("あしたは 何曜日ですか。",
         "What day of the week is tomorrow?"),
    ("n5.vocab.6-question-words.何月", 2):
        ("らい月は 何月ですか。",
         "What month is next month?"),
    ("n5.vocab.6-question-words.何日", 2):
        ("らい週は 何日からですか。",
         "From what date is next week?"),
    ("n5.vocab.9-counters-common.こ", 2):
        ("たまごを 十こ ください。",
         "Please give me ten eggs."),
    ("n5.vocab.10-time-general.とき", 2):
        ("学生の とき よく 本を 読みました。",
         "When I was a student, I often read books."),
    ("n5.vocab.10-time-general.分", 2):
        ("じゅぎょうは 五十分です。",
         "The class is 50 minutes."),
    ("n5.vocab.11-time-days-weeks-month.九月", 2):
        ("九月は すずしく なります。",
         "September becomes cool."),
    ("n5.vocab.12-time-frequency-sequen.毎日", 2):
        ("毎日 はやく おきます。",
         "I wake up early every day."),
    ("n5.vocab.12-time-frequency-sequen.まいばん", 2):
        ("まいばん おふろに 入ります。",
         "I take a bath every night."),
    ("n5.vocab.13-locations-and-places-.おてあらい", 2):
        ("おてあらいで 手を あらいます。",
         "I wash my hands in the restroom."),
    ("n5.vocab.13-locations-and-places-.たいしかん", 2):
        ("たいしかんは 大きい たてものです。",
         "The embassy is a large building."),
    ("n5.vocab.13-locations-and-places-.ろうか", 2):
        ("ろうかは しずかに あるいて ください。",
         "Please walk quietly in the hallway."),
    ("n5.vocab.13-locations-and-places-.とおく", 2):
        ("とおくから 友だちが 来ました。",
         "A friend came from far away."),
    ("n5.vocab.14-nature-and-weather.はる", 2):
        ("はるに さくらが さきます。",
         "Cherry blossoms bloom in spring."),
    ("n5.vocab.14-nature-and-weather.すずしい", 2):
        ("うみの ちかくは すずしくて 気もちが いいです。",
         "The seaside is cool and pleasant."),
    ("n5.vocab.16-food-and-drink-genera.のみもの", 2):
        ("つめたい のみものを 一つ ください。",
         "Please give me one cold drink."),
    ("n5.vocab.17-food-items.しょうゆ", 2):
        ("しょうゆを すこし 入れて ください。",
         "Please add a little soy sauce."),
    ("n5.vocab.19-tableware-and-cooking.フォーク", 2):
        ("フォークを とって ください。",
         "Please pass me a fork."),
    ("n5.vocab.19-tableware-and-cooking.ナイフ", 2):
        ("ナイフは つくえの ひだりに あります。",
         "The knife is to the left on the table."),
    ("n5.vocab.21-clothing-and-accessor.ボタン", 2):
        ("ボタンを おして ください。",
         "Please press the button."),
    ("n5.vocab.22-money-and-shopping.お金", 2):
        ("ぎんこうで お金を おろしました。",
         "I withdrew money at the bank."),
    ("n5.vocab.23-transport.しんごう", 2):
        ("しんごうが あおに なりました。",
         "The traffic light turned green."),
    ("n5.vocab.24-school-and-study.れい", 2):
        ("先生が れいを 三つ 出しました。",
         "The teacher gave three examples."),
    ("n5.vocab.24-school-and-study.つくえ", 2):
        ("つくえを きれいに かたづけました。",
         "I tidied up the desk."),
    ("n5.vocab.24-school-and-study.けしゴム", 2):
        ("けしゴムで まちがいを けしました。",
         "I erased the mistake with an eraser."),
    ("n5.vocab.24-school-and-study.おしらせ", 2):
        ("おしらせを よく 読んで ください。",
         "Please read the notice carefully."),
    ("n5.vocab.25-languages-and-countri.中国", 2):
        ("中国は 人が とても 多いです。",
         "China has very many people."),
    ("n5.vocab.26-house-and-furniture.いま", 2):
        ("いまに 大きい ソファが あります。",
         "There is a large sofa in the living room."),
    ("n5.vocab.26-house-and-furniture.ほんだな", 2):
        ("ほんだなを 新しく 買いました。",
         "I bought a new bookshelf."),
    ("n5.vocab.27-verbs-group-1-verbs.すわる", 2):
        ("ここに すわっても いいですか。",
         "May I sit here?"),
    ("n5.vocab.28-verbs-group-2-verbs.はじめる", 2):
        ("これから かいぎを はじめます。",
         "I'll start the meeting now."),
    ("n5.vocab.28-verbs-group-2-verbs.きえる", 2):
        ("そとの 雨で 火が きえました。",
         "The fire went out from the outside rain."),
    ("n5.vocab.29-verbs-irregular-and-v.かいものする", 2):
        ("土曜日に デパートで かいものします。",
         "I go shopping at the department store on Saturday."),
    ("n5.vocab.30-verbs-existence-and-p.くれる", 2):
        ("友だちが プレゼントを くれました。",
         "My friend gave me a present."),
    ("n5.vocab.31-adjectives.みじかい", 2):
        ("この みじかい えんぴつで 書けません。",
         "I can't write with this short pencil."),
    ("n5.vocab.31-adjectives.かるい", 2):
        ("この にもつは かるくて はこびやすいです。",
         "This luggage is light and easy to carry."),
    ("n5.vocab.31-adjectives.いたい", 2):
        ("足が いたくて はやく あるけません。",
         "My foot hurts so I can't walk fast."),
    ("n5.vocab.31-adjectives.つまらない", 2):
        ("つまらない 話でしたね。",
         "That was a boring talk, wasn't it."),
    ("n5.vocab.33-adverbs.ぜんぶ", 2):
        ("しゅくだいを ぜんぶ おわりました。",
         "I finished all the homework."),
    ("n5.vocab.33-adverbs.どうも", 2):
        ("どうも すみませんでした。",
         "I'm really sorry."),
    ("n5.vocab.33-adverbs.まっすぐ", 2):
        ("この 道を まっすぐ あるいて ください。",
         "Please walk straight down this road."),
    ("n5.vocab.33-adverbs.もういちど", 2):
        ("もういちど 聞いても いいですか。",
         "May I ask once more?"),
    ("n5.vocab.34-conjunctions.ですから", 2):
        ("ねつが あります。ですから、休みます。",
         "I have a fever. Therefore, I'll take the day off."),
    ("n5.vocab.34-conjunctions.ところで", 2):
        ("ところで、今 何時ですか。",
         "By the way, what time is it now?"),
    ("n5.vocab.35-particles-functional-.まで", 2):
        ("えきまで あるいて 行きます。",
         "I'll walk to the station."),
    ("n5.vocab.36-greetings-and-set-phr.しつれいしました", 2):
        ("おくれて しつれいしました。",
         "Sorry for being late."),
    ("n5.vocab.36-greetings-and-set-phr.おかげさまで", 2):
        ("おかげさまで しごとが うまく いきました。",
         "Thanks to you, the work went well."),
    ("n5.vocab.36-greetings-and-set-phr.ぺこぺこ", 2):
        ("お昼まえで おなかが ぺこぺこです。",
         "It's before noon and my stomach is rumbling."),
    ("n5.vocab.37-common-nouns-miscella.話", 2):
        ("先生の 話を ノートに 書きました。",
         "I wrote the teacher's talk in my notebook."),
    ("n5.vocab.37-common-nouns-miscella.プレゼント", 2):
        ("たんじょうびに 何の プレゼントが ほしいですか。",
         "What present do you want for your birthday?"),
    ("n5.vocab.37-common-nouns-miscella.かぜ", 2):
        ("かぜで 学校を 休みました。",
         "I was absent from school because of a cold."),
    ("n5.vocab.37-common-nouns-miscella.はんぶん", 2):
        ("りんごを はんぶんに 切って ください。",
         "Please cut the apple in half."),
    ("n5.vocab.37-common-nouns-miscella.カレンダー", 2):
        ("カレンダーで 月曜日を かくにんしました。",
         "I checked Monday on the calendar."),
    ("n5.vocab.37-common-nouns-miscella.おくさん", 2):
        ("おくさんも コンサートに 行きますか。",
         "Will your wife also go to the concert?"),
    ("n5.vocab.37-common-nouns-miscella.先", 2):
        ("どうぞ お先に お入り ください。",
         "Please go in first."),
    ("n5.vocab.38-sounds-and-voice.こえ", 2):
        ("こえが 大きくて よく 聞こえます。",
         "Your voice is loud and easy to hear."),
    ("n5.vocab.39-function-filler-expre.あの", 2):
        ("あの、すみません。みちを 教えて ください。",
         "Um, excuse me. Please tell me the way."),
    ("n5.vocab.39-function-filler-expre.はい", 2):
        ("はい、私が 田中です。",
         "Yes, I am Tanaka."),
    ("n5.vocab.39-function-filler-expre.ええ", 2):
        ("ええ、いっしょに 行きましょう。",
         "Yes, let's go together."),
    ("n5.vocab.39-function-filler-expre.うん", 2):
        ("うん、それで いいよ。",
         "Yeah, that's fine."),
    ("n5.vocab.39-function-filler-expre.ううん", 2):
        ("ううん、私じゃないよ。",
         "No, it's not me."),
    ("n5.vocab.39-function-filler-expre.さあ", 2):
        ("さあ、しゅっぱつしましょう。",
         "Well then, let's get going."),
    ("n5.vocab.39-function-filler-expre.それでは", 2):
        ("それでは、また あとで。",
         "Well then, see you later."),
    ("n5.vocab.39-function-filler-expre.じゃあ", 2):
        ("じゃあ、また らい週ね。",
         "OK, see you next week."),
    ("n5.vocab.40-misc-useful-items.じゅうしょ", 2):
        ("ここに じゅうしょを 書いて ください。",
         "Please write your address here."),
    ("n5.vocab.40-misc-useful-items.しゅっしん", 2):
        ("私の しゅっしんは 大さかです。",
         "I'm from Osaka."),
    ("n5.vocab.40-misc-useful-items.コンサート", 2):
        ("コンサートの きっぷを 二まい 買いました。",
         "I bought two concert tickets."),
    ("n5.vocab.33-adverbs.どきどき", 2):
        ("はじめての はっぴょうで どきどきしました。",
         "I was nervous at my first presentation."),
    ("n5.vocab.33-adverbs.わくわく", 2):
        ("あしたの たびを 考えて わくわくします。",
         "I'm excited thinking about tomorrow's trip."),
}


# C3: real headword-missing example fix
C3_FIXES: dict[tuple[str, int], tuple[str, str]] = {
    # 'バスで 学校へ 行きます。' has nothing to do with たばこ. Replace.
    ("n5.vocab.37-common-nouns-miscella.たばこ", 1):
        ("ここで たばこを すって いいですか。",
         "May I smoke a cigarette here?"),
}


def apply_fixes(fixes: dict, entries: list, label: str) -> int:
    applied = 0
    missing = []
    for (eid, idx), (new_ja, new_en) in fixes.items():
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
            missing.append((eid, idx, f"idx-out-of-range (only {len(exs)})"))
            continue
        exs[idx]["ja"] = new_ja
        exs[idx]["translation_en"] = new_en
        applied += 1
    print(f"{label}: applied {applied}/{len(fixes)}; missing={len(missing)}")
    for m in missing[:10]:
        print(f"  MISSING: {m}")
    return applied


def main():
    d = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    entries = d["entries"]
    print(f"Loaded {len(entries)} vocab entries.")
    n1 = apply_fixes(C1_FIXES, entries, "C1 template-leak")
    n2 = apply_fixes(C2_FIXES, entries, "C2 within-entry dup")
    n3 = apply_fixes(C3_FIXES, entries, "C3 wrong-headword example")
    VOCAB.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nTotal applied: {n1 + n2 + n3}")


if __name__ == "__main__":
    main()
