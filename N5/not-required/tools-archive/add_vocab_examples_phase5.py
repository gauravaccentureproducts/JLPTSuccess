"""Phase 5 of the example-coverage authoring pass (2026-05-03).

Combines:
  (a) 23 Phase-4 stragglers re-keyed to their actual ID
  (b) ~200 NEW examples across remaining-uncovered sections:
      locations, nature/weather, animals, food, drinks, tableware,
      clothing, money/shopping, transport, school/study, countries,
      house/furniture, i-adj tail, na-adj tail, adverbs tail,
      common-nouns misc.

Lookup strategy:
  - ADDITIONS keyed by exact entry ID (verified against data).
  - Idempotent: re-running skips entries that already have the example.

Constraints: N5 kanji + kana only (JA-13 enforced post-run).
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
P = 'n5.vocab.'

def E(ja, en):
    return {'ja': ja, 'translation_en': en}

ADDITIONS = {
    # ===== Phase 4 stragglers (re-keyed to actual IDs) =====
    P+'10-time-general.今':                       E('今、何時ですか。', 'What time is it now?'),
    P+'10-time-general.今日':                     E('今日は 月曜日です。', 'Today is Monday.'),
    P+'12-time-frequency-sequen.毎日':            E('毎日 日本語を べんきょうします。', 'I study Japanese every day.'),
    P+'12-time-frequency-sequen.時々':            E('時々 えいがを 見ます。', 'I sometimes watch movies.'),
    P+'12-time-frequency-sequen.前':              E('ねる 前に 本を 読みます。', 'I read a book before sleeping.'),
    P+'20-colors.白':                             E('白は ゆきの 色です。', 'White is the color of snow.'),
    P+'20-colors.白い':                           E('白い シャツを きました。', 'I wore a white shirt.'),
    P+'27-verbs-group-1-verbs.会う':              E('友だちに 会います。', 'I meet a friend.'),
    P+'27-verbs-group-1-verbs.言う':              E('「こんにちは」と 言います。', 'I say "hello".'),
    P+'27-verbs-group-1-verbs.聞く':              E('おんがくを 聞きます。', 'I listen to music.'),
    P+'27-verbs-group-1-verbs.かえる':            E('家に かえります。', 'I return home. (Group 1 exception!)'),
    P+'28-verbs-group-2-verbs.出る':              E('家を 出ます。', 'I leave the house.'),
    P+'31-adjectives.新しい':                     E('新しい 本を 買いました。', 'I bought a new book.'),
    P+'31-adjectives.高い':                       E('この とけいは 高いです。', 'This watch is expensive.'),
    P+'31-adjectives.小さい':                     E('小さい ねこが います。', "There's a small cat."),
    P+'31-adjectives.古い':                       E('この 古い 本を 読みました。', 'I read this old book.'),
    P+'31-adjectives.安い':                       E('安い くつを 買いました。', 'I bought cheap shoes.'),
    P+'33-adverbs.まず':                          E('まず、てを あらいましょう。', "First, let's wash our hands."),
    P+'37-common-nouns-miscella.先':              E('お先に しつれいします。', 'Excuse me for leaving first.'),
    P+'37-common-nouns-miscella.りょうり':        E('日本の りょうりが 大すきです。', 'I love Japanese cuisine.'),
    P+'39-function-filler-expre.いいえ':          E('いいえ、ちがいます。', "No, that's not right."),
    P+'39-function-filler-expre.はい':            E('はい、わかりました。', 'Yes, I understand.'),
    P+'9-counters-common.はい':                   E('コーヒーを 一ぱい 飲みました。', 'I drank one cup of coffee.'),

    # ===== NEW Phase 5 entries =====

    # 13. Locations and Places (general) - top 30
    P+'13-locations-and-places-ge.学校':          E('学校に 行きます。', 'I go to school.'),
    P+'13-locations-and-places-ge.家':            E('家に かえります。', 'I go home.'),
    P+'13-locations-and-places-ge.いえ':          E('いえに かえります。', 'I go home.'),
    P+'13-locations-and-places-ge.へや':          E('へやに 入ります。', 'I enter the room.'),
    P+'13-locations-and-places-ge.お手洗い':      E('お手洗いは どこですか。', 'Where is the bathroom?'),
    P+'13-locations-and-places-ge.えき':          E('えきで 友だちに 会います。', "I meet my friend at the station."),
    P+'13-locations-and-places-ge.駅':            E('駅まで あるいて 行きます。', 'I walk to the station.'),
    P+'13-locations-and-places-ge.バスてい':      E('バスていで まちます。', 'I wait at the bus stop.'),
    P+'13-locations-and-places-ge.びょういん':    E('びょういんに 行きます。', 'I go to the hospital.'),
    P+'13-locations-and-places-ge.こうえん':      E('こうえんで あそびます。', 'I play in the park.'),
    P+'13-locations-and-places-ge.としょかん':    E('としょかんで 本を 読みます。', 'I read books at the library.'),
    P+'13-locations-and-places-ge.デパート':      E('デパートで かいものを します。', 'I shop at the department store.'),
    P+'13-locations-and-places-ge.スーパー':      E('スーパーで パンを 買います。', 'I buy bread at the supermarket.'),
    P+'13-locations-and-places-ge.コンビニ':      E('コンビニで おにぎりを 買いました。', 'I bought a rice ball at the convenience store.'),
    P+'13-locations-and-places-ge.レストラン':    E('レストランで ばんごはんを 食べました。', 'I ate dinner at a restaurant.'),
    P+'13-locations-and-places-ge.カフェ':        E('カフェで コーヒーを 飲みます。', 'I drink coffee at a cafe.'),
    P+'13-locations-and-places-ge.きっさてん':    E('きっさてんで おちゃを 飲みました。', 'I drank tea at the cafe.'),
    P+'13-locations-and-places-ge.ぎんこう':      E('ぎんこうで お金を ひきだします。', 'I withdraw money at the bank.'),
    P+'13-locations-and-places-ge.ゆうびんきょく': E('ゆうびんきょくで きってを 買います。', 'I buy stamps at the post office.'),
    P+'13-locations-and-places-ge.大学':          E('大学に 行きたいです。', 'I want to go to university.'),
    P+'13-locations-and-places-ge.まち':          E('まちは にぎやかです。', 'The town is lively.'),
    P+'13-locations-and-places-ge.中':            E('かばんの 中に 本が あります。', 'There is a book in the bag.'),
    P+'13-locations-and-places-ge.外':            E('外は さむいです。', "It's cold outside."),
    P+'13-locations-and-places-ge.上':            E('つくえの 上に 本が あります。', 'A book is on the desk.'),
    P+'13-locations-and-places-ge.下':            E('いすの 下に ねこが います。', 'A cat is under the chair.'),

    # 14. Nature and Weather - top 20
    P+'14-nature-and-weather.雨':                 E('今日は 雨です。', "It's raining today."),
    P+'14-nature-and-weather.ゆき':               E('冬は ゆきが ふります。', 'It snows in winter.'),
    P+'14-nature-and-weather.風':                 E('今日は 風が つよいです。', 'The wind is strong today.'),
    P+'14-nature-and-weather.そら':               E('そらが あおいです。', 'The sky is blue.'),
    P+'14-nature-and-weather.つき':               E('よる、つきが きれいです。', 'The moon is pretty at night.'),
    P+'14-nature-and-weather.太陽':               E('太陽が 出ました。', 'The sun came out.'),
    P+'14-nature-and-weather.ほし':               E('よる、ほしを 見ます。', 'I look at stars at night.'),
    P+'14-nature-and-weather.山':                 E('山に のぼります。', 'I climb the mountain.'),
    P+'14-nature-and-weather.川':                 E('川で およぎます。', 'I swim in the river.'),
    P+'14-nature-and-weather.うみ':               E('夏に うみで およぎます。', 'I swim in the sea in summer.'),
    P+'14-nature-and-weather.木':                 E('こうえんに 大きい 木が あります。', "There's a big tree in the park."),
    P+'14-nature-and-weather.花':                 E('花が きれいに さきました。', 'The flowers bloomed beautifully.'),
    P+'14-nature-and-weather.てんき':             E('今日の てんきは いいです。', "Today's weather is good."),
    P+'14-nature-and-weather.あつい':             E('夏は とても あついです。', 'Summer is very hot.'),
    P+'14-nature-and-weather.さむい':             E('冬は さむいです。', 'Winter is cold.'),
    P+'14-nature-and-weather.夏':                 E('夏が すきです。', 'I like summer.'),
    P+'14-nature-and-weather.冬':                 E('冬は ゆきが ふります。', 'It snows in winter.'),
    P+'14-nature-and-weather.はる':               E('はるは あたたかいです。', 'Spring is warm.'),
    P+'14-nature-and-weather.あき':               E('あきは すずしいです。', 'Autumn is cool.'),

    # 15. Animals - all
    P+'15-animals.いぬ':                          E('いぬが すきです。', 'I like dogs.'),
    P+'15-animals.ねこ':                          E('ねこが いえに います。', "There's a cat at home."),
    P+'15-animals.とり':                          E('そらに とりが とんで います。', 'A bird is flying in the sky.'),
    P+'15-animals.さかな':                        E('さかなを 食べます。', 'I eat fish.'),
    P+'15-animals.うま':                          E('うまは 大きい どうぶつです。', 'A horse is a big animal.'),
    P+'15-animals.うし':                          E('うしの にくを 食べました。', 'I ate beef.'),
    P+'15-animals.ぶた':                          E('ぶたは かわいいです。', 'Pigs are cute.'),
    P+'15-animals.どうぶつ':                      E('どうぶつが 大すきです。', 'I love animals.'),

    # 16. Food and Drink - General
    P+'16-food-and-drink-general.ごはん':         E('あさごはんを 食べました。', 'I ate breakfast.'),
    P+'16-food-and-drink-general.あさごはん':     E('あさごはんは パンでした。', 'Breakfast was bread.'),
    P+'16-food-and-drink-general.ひるごはん':     E('ひるごはんを 食べましょう。', "Let's eat lunch."),
    P+'16-food-and-drink-general.ばんごはん':     E('ばんごはんは 七時です。', 'Dinner is at seven.'),
    P+'16-food-and-drink-general.おかし':         E('おかしを 食べます。', 'I eat sweets.'),
    P+'16-food-and-drink-general.りょうり':       E('日本りょうりが すきです。', 'I like Japanese cuisine.'),

    # 17. Food - Items - top 20
    P+'17-food-items.パン':                       E('あさ、パンを 食べます。', 'I eat bread in the morning.'),
    P+'17-food-items.たまご':                     E('たまごを 二つ ください。', 'Two eggs please.'),
    P+'17-food-items.りんご':                     E('りんごは あかいです。', 'Apples are red.'),
    P+'17-food-items.みかん':                     E('みかんを 食べます。', 'I eat mandarin oranges.'),
    P+'17-food-items.バナナ':                     E('バナナは きいろいです。', 'Bananas are yellow.'),
    P+'17-food-items.やさい':                     E('やさいを たくさん 食べます。', 'I eat lots of vegetables.'),
    P+'17-food-items.くだもの':                   E('くだものが すきです。', 'I like fruit.'),
    P+'17-food-items.にく':                       E('にくを 食べます。', 'I eat meat.'),
    P+'17-food-items.おにぎり':                   E('コンビニで おにぎりを 買いました。', 'I bought a rice ball at the convenience store.'),
    P+'17-food-items.おべんとう':                 E('おべんとうを もって 行きます。', "I bring a packed lunch."),
    P+'17-food-items.ケーキ':                     E('たんじょうびに ケーキを 食べます。', 'I eat cake on my birthday.'),
    P+'17-food-items.アイスクリーム':             E('夏は アイスクリームが おいしいです。', 'Ice cream is delicious in summer.'),
    P+'17-food-items.チーズ':                     E('チーズが すきです。', 'I like cheese.'),
    P+'17-food-items.バター':                     E('パンに バターを ぬります。', 'I spread butter on bread.'),
    P+'17-food-items.ラーメン':                   E('ラーメンを 食べました。', 'I ate ramen.'),
    P+'17-food-items.すし':                       E('日曜日に すしを 食べます。', 'I eat sushi on Sunday.'),
    P+'17-food-items.てんぷら':                   E('てんぷらは おいしいです。', 'Tempura is delicious.'),

    # 18. Drinks - all
    P+'18-drinks.水':                             E('水を 飲みます。', 'I drink water.'),
    P+'18-drinks.おちゃ':                         E('おちゃを 飲みましょう。', "Let's drink tea."),
    P+'18-drinks.コーヒー':                       E('あさ、コーヒーを 飲みます。', 'I drink coffee in the morning.'),
    P+'18-drinks.ぎゅうにゅう':                   E('ぎゅうにゅうを 飲みます。', 'I drink milk.'),
    P+'18-drinks.ジュース':                       E('ジュースを 三本 ください。', 'Three juices please.'),
    P+'18-drinks.ビール':                         E('ばんに ビールを 飲みます。', 'I drink beer in the evening.'),
    P+'18-drinks.ワイン':                         E('ワインは おいしいです。', 'Wine is delicious.'),
    P+'18-drinks.おさけ':                         E('おさけを 飲みません。', "I don't drink alcohol."),

    # 21. Clothing - top 15
    P+'21-clothing-and-accessorie.シャツ':        E('白い シャツを きます。', 'I wear a white shirt.'),
    P+'21-clothing-and-accessorie.ズボン':        E('あたらしい ズボンを 買いました。', 'I bought new pants.'),
    P+'21-clothing-and-accessorie.スカート':      E('しろい スカートを はいて います。', "I'm wearing a white skirt."),
    P+'21-clothing-and-accessorie.くつ':          E('くつを ぬいで ください。', 'Please take off your shoes.'),
    P+'21-clothing-and-accessorie.くつした':      E('くつしたを はきます。', 'I put on socks.'),
    P+'21-clothing-and-accessorie.ぼうし':        E('ぼうしを かぶります。', 'I put on a hat.'),
    P+'21-clothing-and-accessorie.ふく':          E('あたらしい ふくを 買いました。', 'I bought new clothes.'),
    P+'21-clothing-and-accessorie.めがね':        E('めがねを かけて います。', 'I wear glasses.'),
    P+'21-clothing-and-accessorie.とけい':        E('とけいを 見ます。', 'I look at my watch.'),
    P+'21-clothing-and-accessorie.かばん':        E('かばんに 本を 入れます。', 'I put the book in the bag.'),

    # 22. Money and Shopping - all
    P+'22-money-and-shopping.お金':               E('お金が ありません。', "I have no money."),
    P+'22-money-and-shopping.いくら':             E('これは いくらですか。', 'How much is this?'),
    P+'22-money-and-shopping.ねだん':             E('この かばんの ねだんは 高いです。', "This bag's price is expensive."),
    P+'22-money-and-shopping.きって':             E('きってを 二まい 買います。', "I buy two stamps."),
    P+'22-money-and-shopping.はがき':             E('はがきを 書きます。', 'I write a postcard.'),

    # 23. Transport - top 10
    P+'23-transport.でんしゃ':                    E('でんしゃで 学校に 行きます。', 'I go to school by train.'),
    P+'23-transport.バス':                        E('バスで えきに 行きます。', 'I go to the station by bus.'),
    P+'23-transport.くるま':                      E('くるまで ドライブします。', 'I go for a drive by car.'),
    P+'23-transport.じてんしゃ':                  E('じてんしゃで かいものに 行きます。', 'I go shopping by bicycle.'),
    P+'23-transport.ちかてつ':                    E('ちかてつで 行きます。', 'I go by subway.'),
    P+'23-transport.タクシー':                    E('タクシーに のります。', 'I take a taxi.'),
    P+'23-transport.ひこうき':                    E('ひこうきで にほんに 行きます。', 'I go to Japan by plane.'),
    P+'23-transport.ふね':                        E('ふねで しまに 行きます。', 'I go to the island by boat.'),

    # 24. School and Study - top 20
    P+'24-school-and-study.学生':                 E('わたしは 学生です。', 'I am a student.'),
    P+'24-school-and-study.先生':                 E('先生は しんせつです。', 'The teacher is kind.'),
    P+'24-school-and-study.大学生':               E('あには 大学生です。', 'My older brother is a university student.'),
    P+'24-school-and-study.高校生':               E('わたしは 高校生です。', 'I am a high school student.'),
    P+'24-school-and-study.じゅぎょう':           E('じゅぎょうは 九時から です。', 'Class starts at 9.'),
    P+'24-school-and-study.しゅくだい':           E('しゅくだいを します。', 'I do my homework.'),
    P+'24-school-and-study.テスト':               E('あした テストが あります。', "There's a test tomorrow."),
    P+'24-school-and-study.しけん':               E('しけんは むずかしかったです。', 'The exam was difficult.'),
    P+'24-school-and-study.きょうしつ':           E('きょうしつに 入ります。', 'I enter the classroom.'),
    P+'24-school-and-study.本':                   E('本を 読みます。', 'I read a book.'),
    P+'24-school-and-study.じしょ':               E('じしょで しらべます。', 'I look it up in the dictionary.'),
    P+'24-school-and-study.ノート':               E('ノートに 書きます。', 'I write in the notebook.'),
    P+'24-school-and-study.えんぴつ':             E('えんぴつで 書きます。', 'I write with a pencil.'),
    P+'24-school-and-study.ペン':                 E('ペンを かして ください。', 'Please lend me a pen.'),
    P+'24-school-and-study.かみ':                 E('かみを 一まい ください。', 'One sheet of paper please.'),
    P+'24-school-and-study.つくえ':               E('つくえの 上に 本が あります。', 'A book is on the desk.'),
    P+'24-school-and-study.いす':                 E('いすに すわります。', 'I sit on the chair.'),

    # 25. Languages and Countries
    P+'25-languages-and-countries.日本':          E('日本に 行きたいです。', 'I want to go to Japan.'),
    P+'25-languages-and-countries.日本語':        E('日本語を べんきょうします。', 'I study Japanese.'),
    P+'25-languages-and-countries.アメリカ':      E('アメリカから 来ました。', 'I came from America.'),
    P+'25-languages-and-countries.えいご':        E('えいごを 話します。', 'I speak English.'),
    P+'25-languages-and-countries.中国':          E('中国は 大きい 国です。', 'China is a big country.'),
    P+'25-languages-and-countries.中国語':        E('中国語が わかりません。', "I don't understand Chinese."),
    P+'25-languages-and-countries.かんこく':      E('かんこくの りょうりが すきです。', 'I like Korean food.'),
    P+'25-languages-and-countries.国':            E('わたしの 国は 大きいです。', 'My country is big.'),

    # 26. House and Furniture - top 15
    P+'26-house-and-furniture.まど':              E('まどを あけて ください。', 'Please open the window.'),
    P+'26-house-and-furniture.ドア':              E('ドアを しめます。', 'I close the door.'),
    P+'26-house-and-furniture.テーブル':          E('テーブルの 上に 花が あります。', 'Flowers are on the table.'),
    P+'26-house-and-furniture.ベッド':            E('ベッドで ねます。', 'I sleep in bed.'),
    P+'26-house-and-furniture.しょくどう':        E('しょくどうで ごはんを 食べます。', 'I eat in the dining room.'),
    P+'26-house-and-furniture.だいどころ':        E('だいどころで りょうりを します。', 'I cook in the kitchen.'),
    P+'26-house-and-furniture.お風呂':            E('お風呂に 入ります。', 'I take a bath.'),
    P+'26-house-and-furniture.シャワー':          E('あさ シャワーを あびます。', 'I shower in the morning.'),
    P+'26-house-and-furniture.テレビ':            E('テレビを 見ます。', 'I watch TV.'),
    P+'26-house-and-furniture.でんわ':            E('でんわを かけます。', 'I make a phone call.'),
    P+'26-house-and-furniture.れいぞうこ':        E('れいぞうこに 入れます。', 'I put it in the refrigerator.'),
    P+'26-house-and-furniture.でんき':            E('でんきを つけます。', 'I turn on the light.'),

    # 27. More Group-1 verbs
    P+'27-verbs-group-1-verbs.あらう':            E('てを あらいます。', 'I wash my hands.'),
    P+'27-verbs-group-1-verbs.おわる':            E('じゅぎょうが おわりました。', 'Class ended.'),
    P+'27-verbs-group-1-verbs.のる':              E('バスに のります。', 'I get on the bus.'),
    P+'27-verbs-group-1-verbs.のぼる':            E('山に のぼります。', 'I climb the mountain.'),
    P+'27-verbs-group-1-verbs.はたらく':          E('ぎんこうで はたらきます。', 'I work at a bank.'),
    P+'27-verbs-group-1-verbs.はじまる':          E('じゅぎょうが はじまります。', 'Class begins.'),
    P+'27-verbs-group-1-verbs.まつ':              E('えきで まちます。', 'I wait at the station.'),
    P+'27-verbs-group-1-verbs.もつ':              E('かばんを もって います。', "I'm holding a bag."),
    P+'27-verbs-group-1-verbs.つくる':            E('ばんごはんを つくります。', 'I make dinner.'),
    P+'27-verbs-group-1-verbs.つかう':            E('はしを つかいます。', 'I use chopsticks.'),
    P+'27-verbs-group-1-verbs.あるく':            E('えきまで あるきます。', 'I walk to the station.'),

    # 28. More Group-2 verbs
    P+'28-verbs-group-2-verbs.おしえる':          E('日本語を おしえます。', 'I teach Japanese.'),
    P+'28-verbs-group-2-verbs.おぼえる':          E('かんじを おぼえます。', 'I memorize kanji.'),
    P+'28-verbs-group-2-verbs.あける':            E('まどを あけます。', 'I open the window.'),
    P+'28-verbs-group-2-verbs.しめる':            E('ドアを しめます。', 'I close the door.'),
    P+'28-verbs-group-2-verbs.おりる':            E('バスを おります。', 'I get off the bus.'),
    P+'28-verbs-group-2-verbs.かりる':            E('としょかんで 本を かります。', 'I borrow a book at the library.'),

    # 31. More i-adjectives
    P+'31-adjectives.おもしろい':                 E('この 本は おもしろいです。', 'This book is interesting.'),
    P+'31-adjectives.おいしい':                   E('この りょうりは おいしいです。', 'This food is delicious.'),
    P+'31-adjectives.いそがしい':                 E('今日は いそがしいです。', 'Today is busy.'),
    P+'31-adjectives.あたたかい':                 E('はるは あたたかいです。', 'Spring is warm.'),
    P+'31-adjectives.すずしい':                   E('あきは すずしいです。', 'Autumn is cool.'),
    P+'31-adjectives.あまい':                     E('この ケーキは あまいです。', 'This cake is sweet.'),
    P+'31-adjectives.からい':                     E('この りょうりは からいです。', 'This food is spicy.'),
    P+'31-adjectives.いい':                       E('今日は いい てんきです。', "Today's weather is good."),
    P+'31-adjectives.わるい':                     E('わるい ニュースが あります。', "There's bad news."),
    P+'31-adjectives.いたい':                     E('あたまが いたいです。', 'My head hurts.'),
    P+'31-adjectives.ながい':                     E('ながい かみが すきです。', 'I like long hair.'),
    P+'31-adjectives.みじかい':                   E('みじかい てがみを 書きました。', 'I wrote a short letter.'),
    P+'31-adjectives.ひろい':                     E('この へやは ひろいです。', 'This room is spacious.'),
    P+'31-adjectives.せまい':                     E('わたしの へやは せまいです。', 'My room is small.'),
    P+'31-adjectives.おもい':                     E('この かばんは おもいです。', 'This bag is heavy.'),
    P+'31-adjectives.かるい':                     E('この かばんは かるいです。', 'This bag is light.'),
    P+'31-adjectives.つよい':                     E('かれは つよいです。', 'He is strong.'),
    P+'31-adjectives.よわい':                     E('わたしは よわいです。', 'I am weak.'),
    P+'31-adjectives.はやい':                     E('しんかんせんは はやいです。', 'The bullet train is fast.'),
    P+'31-adjectives.おそい':                     E('バスは おそいです。', 'The bus is slow.'),
    P+'31-adjectives.とおい':                     E('家は とおいです。', 'My house is far.'),
    P+'31-adjectives.ちかい':                     E('えきは ちかいです。', 'The station is close.'),

    # 32. na-adj tail (only ~12 left)
    P+'32-na-adjectives.だいすき':                E('日本語が だいすきです。', 'I really love Japanese.'),
    P+'32-na-adjectives.だいきらい':              E('やさいが だいきらいです。', 'I really hate vegetables.'),
    P+'32-na-adjectives.げんき':                  E('わたしは げんきです。', 'I am healthy/fine.'),
    P+'32-na-adjectives.ゆうめい':                E('この レストランは ゆうめいです。', 'This restaurant is famous.'),

    # 33. Adverbs
    P+'33-adverbs.とても':                        E('とても おいしいです。', "It's very delicious."),
    P+'33-adverbs.すこし':                        E('すこし つかれました。', "I'm a little tired."),
    P+'33-adverbs.たくさん':                      E('たくさん 食べました。', 'I ate a lot.'),
    P+'33-adverbs.ちょっと':                      E('ちょっと まって ください。', 'Please wait a moment.'),
    P+'33-adverbs.いっしょに':                    E('いっしょに 行きましょう。', "Let's go together."),
    P+'33-adverbs.はやく':                        E('はやく 来て ください。', 'Please come quickly.'),
    P+'33-adverbs.ゆっくり':                      E('ゆっくり 話して ください。', 'Please speak slowly.'),
    P+'33-adverbs.もっと':                        E('もっと べんきょうします。', "I'll study more."),
    P+'33-adverbs.だんだん':                      E('だんだん あつくなります。', "It's gradually getting hot."),
    P+'33-adverbs.きっと':                        E('きっと 来ます。', "He'll definitely come."),
    P+'33-adverbs.たぶん':                        E('たぶん あした 雨です。', "Maybe it'll rain tomorrow."),
}


def main() -> int:
    vpath = ROOT / 'data' / 'vocab.json'
    data = json.loads(vpath.read_text(encoding='utf-8'))
    by_id = {v['id']: v for v in data['entries']}
    # Fallback: by (section_token, form-or-reading-token)
    by_section_token: dict[tuple[str, str], dict] = {}
    for v in data['entries']:
        vid = v.get('id', '')
        if not vid.startswith(P): continue
        rest = vid[len(P):]
        if '-' not in rest: continue
        section_token = rest.split('-', 1)[0]  # '13', '14', etc.
        for key in (v.get('form'), v.get('reading')):
            if key:
                by_section_token.setdefault((section_token, key), v)

    added, skipped, not_found = [], [], []
    for vid, new_ex in ADDITIONS.items():
        v = by_id.get(vid)
        if v is None:
            # Fallback: parse my key for section + last token, then look up
            rest = vid[len(P):]
            if '-' in rest and '.' in rest:
                section_token = rest.split('-', 1)[0]
                last_token = rest.rsplit('.', 1)[-1]
                v = by_section_token.get((section_token, last_token))
        if v is None:
            not_found.append(vid); continue
        existing = v.get('examples') or []
        if any(e.get('ja') == new_ex['ja'] for e in existing):
            skipped.append(vid); continue
        existing.append(new_ex)
        v['examples'] = existing
        added.append(vid)
    if added:
        vpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Added inline example to {len(added)} vocab entries.')
    if skipped: print(f'Skipped (already had it): {len(skipped)}')
    if not_found:
        print(f'NOT FOUND ({len(not_found)}):')
        for v in sorted(not_found):
            print(f'  {v}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
