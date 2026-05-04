"""Phase 4 of the example-coverage authoring pass (2026-05-03).

Continues vocab-example coverage from Phase 3 (51 entries shipped).
This batch targets ~180 highest-leverage uncovered entries:
  - Numbers + counters (mechanical "X-counter" demonstrations)
  - Time / calendar / frequency (days, months, time-of-day)
  - Colors (simple "Xは Y-color です")
  - Greetings + set phrases (actual dialogue use)
  - Particles (typical-use sentences)
  - Demonstrative tail (こんな / そんな / あんな / ああ / こう)
  - Top common verbs (Group 1, Group 2, irregular, existence)
  - Top common adjectives (i + na)

Constraints: N5 kanji + kana only. JA-13 + JA-16 enforced post-run.

Idempotent.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# Helper to keep this file readable: a one-liner per entry.
def E(ja, en):
    return {'ja': ja, 'translation_en': en}

PREFIX = 'n5.vocab.'

ADDITIONS = {
    # Numbers
    PREFIX + '7-numbers.一':       E('りんごを 一つ ください。', 'One apple please.'),
    PREFIX + '7-numbers.二':       E('二人で 行きます。', 'We are going together (two people).'),
    PREFIX + '7-numbers.三':       E('三月は はるです。', 'March is spring.'),
    PREFIX + '7-numbers.四':       E('四時に あいましょう。', "Let's meet at four o'clock."),
    PREFIX + '7-numbers.五':       E('五分 まってください。', 'Please wait five minutes.'),
    PREFIX + '7-numbers.六':       E('六時に おきます。', 'I get up at six.'),
    PREFIX + '7-numbers.七':       E('七時に ばんごはんを 食べます。', 'I eat dinner at seven.'),
    PREFIX + '7-numbers.八':       E('八月は あついです。', 'August is hot.'),
    PREFIX + '7-numbers.九':       E('九時に 学校が はじまります。', 'School starts at nine.'),
    PREFIX + '7-numbers.十':       E('十分 かかります。', 'It takes ten minutes.'),
    PREFIX + '7-numbers.十一':     E('十一月は さむいです。', 'November is cold.'),
    PREFIX + '7-numbers.二十':     E('わたしは 二十さいです。', 'I am twenty years old.'),
    PREFIX + '7-numbers.百':       E('百円 ください。', 'One hundred yen please.'),
    PREFIX + '7-numbers.千':       E('これは 千円です。', 'This is 1000 yen.'),
    PREFIX + '7-numbers.万':       E('一万円 はらいました。', 'I paid 10,000 yen.'),
    PREFIX + '7-numbers.一万':     E('くつは 一万円でした。', 'The shoes were 10,000 yen.'),
    PREFIX + '7-numbers.おく':     E('日本の 人口は 一おく人ぐらいです。', "Japan's population is about 100 million."),

    # Native counters (つ-series)
    PREFIX + '8-native-counters-series.一つ':   E('みかんを 一つ かいました。', 'I bought one mandarin orange.'),
    PREFIX + '8-native-counters-series.二つ':   E('かばんを 二つ もって います。', 'I have two bags.'),
    PREFIX + '8-native-counters-series.三つ':   E('いすが 三つ あります。', 'There are three chairs.'),
    PREFIX + '8-native-counters-series.四つ':   E('たまごを 四つ ください。', 'Four eggs please.'),
    PREFIX + '8-native-counters-series.五つ':   E('りんごを 五つ かいました。', 'I bought five apples.'),
    PREFIX + '8-native-counters-series.六つ':   E('ケーキを 六つ つくりました。', 'I made six cakes.'),
    PREFIX + '8-native-counters-series.七つ':   E('七つの くにを たびしました。', 'I traveled to seven countries.'),
    PREFIX + '8-native-counters-series.八つ':   E('八つの りんごが テーブルに あります。', 'There are eight apples on the table.'),
    PREFIX + '8-native-counters-series.九つ':   E('九つの しつもんが あります。', 'I have nine questions.'),
    PREFIX + '8-native-counters-series.十':     E('十の おかしを ください。', 'Ten sweets please.'),
    PREFIX + '8-native-counters-series.いくつ': E('みかんは いくつ ありますか。', 'How many oranges are there?'),

    # Counters (common)
    PREFIX + '9-counters-common.人':        E('クラスに 三十人 います。', 'There are thirty people in the class.'),
    PREFIX + '9-counters-common.一人':      E('一人で 行きます。', 'I will go alone.'),
    PREFIX + '9-counters-common.二人':      E('二人で カフェに 行きました。', 'The two of us went to a cafe.'),
    PREFIX + '9-counters-common.まい':      E('かみを 三まい ください。', 'Three sheets of paper please.'),

    # Time - General (subset)
    PREFIX + '10-time-general.いま':        E('いま、何時ですか。', 'What time is it now?'),
    PREFIX + '10-time-general.きょう':      E('きょうは 月曜日です。', 'Today is Monday.'),
    PREFIX + '10-time-general.あした':      E('あした 学校に 行きます。', 'I will go to school tomorrow.'),
    PREFIX + '10-time-general.きのう':      E('きのう 友だちに あいました。', 'I met a friend yesterday.'),
    PREFIX + '10-time-general.あさ':        E('あさ コーヒーを 飲みます。', 'I drink coffee in the morning.'),
    PREFIX + '10-time-general.ひる':        E('ひるごはんを 食べました。', 'I ate lunch.'),
    PREFIX + '10-time-general.よる':        E('よるは 本を 読みます。', 'At night I read books.'),
    PREFIX + '10-time-general.ばん':        E('ばんごはんは 七時です。', 'Dinner is at seven.'),
    PREFIX + '10-time-general.ゆうがた':    E('ゆうがた さんぽを します。', 'I take a walk in the evening.'),

    # Time - Days/Weeks/Months/Years (subset)
    PREFIX + '11-time-days-weeks-months-y.月曜日':   E('月曜日に 学校が はじまります。', 'School starts on Monday.'),
    PREFIX + '11-time-days-weeks-months-y.火曜日':   E('火曜日は いそがしいです。', 'Tuesday is busy.'),
    PREFIX + '11-time-days-weeks-months-y.水曜日':   E('水曜日に かいぎが あります。', "There's a meeting on Wednesday."),
    PREFIX + '11-time-days-weeks-months-y.木曜日':   E('木曜日は ピアノの 日です。', "Thursday is piano day."),
    PREFIX + '11-time-days-weeks-months-y.金曜日':   E('金曜日は 友だちと 出かけます。', 'On Friday I go out with friends.'),
    PREFIX + '11-time-days-weeks-months-y.土曜日':   E('土曜日は 休みです。', 'Saturday is a day off.'),
    PREFIX + '11-time-days-weeks-months-y.日曜日':   E('日曜日に 家ぞくと あいます。', 'On Sunday I see my family.'),
    PREFIX + '11-time-days-weeks-months-y.今日':     E('今日は 雨です。', "Today it's raining."),
    PREFIX + '11-time-days-weeks-months-y.毎日':     E('毎日 日本語を べんきょうします。', 'I study Japanese every day.'),
    PREFIX + '11-time-days-weeks-months-y.毎週':     E('毎週 友だちに あいます。', 'I see a friend every week.'),
    PREFIX + '11-time-days-weeks-months-y.今週':     E('今週は しけんが あります。', 'There is an exam this week.'),
    PREFIX + '11-time-days-weeks-months-y.来週':     E('来週 京都に 行きます。', 'Next week I go to Kyoto.'),
    PREFIX + '11-time-days-weeks-months-y.今月':     E('今月は 五月です。', 'This month is May.'),
    PREFIX + '11-time-days-weeks-months-y.来月':     E('来月 たんじょうびです。', 'My birthday is next month.'),
    PREFIX + '11-time-days-weeks-months-y.今年':     E('今年は あたらしい 学校に 行きます。', 'This year I go to a new school.'),
    PREFIX + '11-time-days-weeks-months-y.来年':     E('来年 大学生に なります。', 'Next year I will become a university student.'),

    # Time - Frequency / Sequence
    PREFIX + '12-time-frequency-sequence.いつも':    E('いつも 七時に おきます。', 'I always wake up at seven.'),
    PREFIX + '12-time-frequency-sequence.よく':      E('よく カフェに 行きます。', 'I often go to cafes.'),
    PREFIX + '12-time-frequency-sequence.ときどき':  E('ときどき えいがを 見ます。', 'I sometimes watch movies.'),
    PREFIX + '12-time-frequency-sequence.たまに':    E('たまに りょうりを します。', 'I occasionally cook.'),
    PREFIX + '12-time-frequency-sequence.あまり':    E('あまり 食べません。', "I don't eat much."),
    PREFIX + '12-time-frequency-sequence.ぜんぜん':  E('ぜんぜん わかりません。', "I don't understand at all."),
    PREFIX + '12-time-frequency-sequence.まず':      E('まず、てを あらいましょう。', "First, let's wash our hands."),
    PREFIX + '12-time-frequency-sequence.つぎに':    E('つぎに、コーヒーを 飲みます。', 'Next, I drink coffee.'),
    PREFIX + '12-time-frequency-sequence.さいご':    E('さいごに、はを みがきます。', 'Lastly, I brush my teeth.'),
    PREFIX + '12-time-frequency-sequence.さき':      E('さきに 行きます。', "I'll go ahead."),
    PREFIX + '12-time-frequency-sequence.あと':      E('あとで でんわします。', "I'll call you later."),
    PREFIX + '12-time-frequency-sequence.まえ':      E('ねる まえに 本を 読みます。', 'I read a book before sleeping.'),
    PREFIX + '12-time-frequency-sequence.まだ':      E('まだ ばんごはんを 食べていません。', "I haven't eaten dinner yet."),
    PREFIX + '12-time-frequency-sequence.もう':      E('もう しゅくだいは おわりました。', "I've already finished my homework."),

    # Colors
    PREFIX + '20-colors.あかい':     E('あかい 花が きれいです。', 'The red flower is pretty.'),
    PREFIX + '20-colors.あおい':     E('あおい そらが すきです。', 'I like the blue sky.'),
    PREFIX + '20-colors.しろい':     E('しろい くつを かいました。', 'I bought white shoes.'),
    PREFIX + '20-colors.くろい':     E('くろい かばんを もって います。', 'I have a black bag.'),
    PREFIX + '20-colors.きいろい':   E('きいろい バナナです。', "It's a yellow banana."),
    PREFIX + '20-colors.ちゃいろ':   E('ちゃいろの くつを はきます。', 'I wear brown shoes.'),
    PREFIX + '20-colors.みどり':     E('みどりの 木が たくさん あります。', 'There are many green trees.'),
    PREFIX + '20-colors.あか':       E('あかは 花の 色です。', 'Red is the color of flowers.'),
    PREFIX + '20-colors.あお':       E('あおは そらの 色です。', 'Blue is the color of the sky.'),
    PREFIX + '20-colors.しろ':       E('しろは ゆきの 色です。', 'White is the color of snow.'),
    PREFIX + '20-colors.くろ':       E('くろは よるの 色です。', 'Black is the color of night.'),
    PREFIX + '20-colors.きいろ':     E('きいろは レモンの 色です。', 'Yellow is the color of lemons.'),

    # Particles (functional vocabulary)
    PREFIX + '35-particles-functional-.は':       E('わたしは 学生です。', 'I am a student. (topic は)'),
    PREFIX + '35-particles-functional-.が':       E('ねこが すきです。', 'I like cats. (subject が)'),
    PREFIX + '35-particles-functional-.を':       E('本を 読みます。', 'I read a book. (object を)'),
    PREFIX + '35-particles-functional-.に':       E('七時に おきます。', 'I get up at seven. (time に)'),
    PREFIX + '35-particles-functional-.で':       E('カフェで コーヒーを 飲みます。', 'I drink coffee at a cafe. (location で)'),
    PREFIX + '35-particles-functional-.へ':       E('学校へ 行きます。', 'I go to school. (direction へ)'),
    PREFIX + '35-particles-functional-.と':       E('友だちと えいがを 見ます。', 'I watch a movie with a friend. (with と)'),
    PREFIX + '35-particles-functional-.から':     E('九時から はじまります。', 'It starts at nine. (from から)'),
    PREFIX + '35-particles-functional-.まで':     E('五時まで しごとを します。', 'I work until five. (until まで)'),
    PREFIX + '35-particles-functional-.の':       E('わたしの 本です。', "It is my book. (possessive の)"),
    PREFIX + '35-particles-functional-.も':       E('わたしも 行きます。', 'I will go too. (also も)'),
    PREFIX + '35-particles-functional-.や':       E('りんごや みかんを かいました。', 'I bought apples and oranges (among other things). (や)'),
    PREFIX + '35-particles-functional-.か':       E('元気ですか。', 'How are you? (question か)'),
    PREFIX + '35-particles-functional-.ね':       E('いい てんきですね。', "It's nice weather, isn't it? (ね)"),
    PREFIX + '35-particles-functional-.よ':       E('あぶないですよ。', "It's dangerous, you know! (よ)"),
    PREFIX + '35-particles-functional-.より':     E('夏は 冬より あついです。', 'Summer is hotter than winter. (より)'),

    # Greetings and set phrases
    PREFIX + '36-greetings-set-phrases.おはようございます':     E('おはようございます！', 'Good morning! (polite)'),
    PREFIX + '36-greetings-set-phrases.こんにちは':           E('こんにちは。元気ですか。', 'Hello. How are you?'),
    PREFIX + '36-greetings-set-phrases.こんばんは':           E('こんばんは。', 'Good evening.'),
    PREFIX + '36-greetings-set-phrases.おやすみなさい':       E('おやすみなさい。', 'Good night.'),
    PREFIX + '36-greetings-set-phrases.さようなら':           E('さようなら、また あした。', 'Goodbye, see you tomorrow.'),
    PREFIX + '36-greetings-set-phrases.ありがとうございます': E('ありがとうございます！', 'Thank you very much!'),
    PREFIX + '36-greetings-set-phrases.すみません':           E('すみません、メニューを ください。', 'Excuse me, the menu please.'),
    PREFIX + '36-greetings-set-phrases.ごめんなさい':         E('ごめんなさい。おそく なりました。', "I'm sorry. I'm late."),
    PREFIX + '36-greetings-set-phrases.いただきます':         E('いただきます！', 'Thank you for the food! (before eating)'),
    PREFIX + '36-greetings-set-phrases.ごちそうさま':         E('ごちそうさまでした。', 'Thank you for the meal. (after eating)'),
    PREFIX + '36-greetings-set-phrases.おねがいします':       E('コーヒーを おねがいします。', 'Coffee please.'),
    PREFIX + '36-greetings-set-phrases.どうぞ':               E('どうぞ、おかけください。', 'Please, have a seat.'),
    PREFIX + '36-greetings-set-phrases.どうも':               E('どうも、ありがとう。', 'Thank you very much.'),
    PREFIX + '36-greetings-set-phrases.はい':                 E('はい、わかりました。', "Yes, I understand."),
    PREFIX + '36-greetings-set-phrases.いいえ':               E('いいえ、ちがいます。', "No, that's not right."),

    # Demonstratives tail
    PREFIX + '5-demonstratives.そんな':   E('そんな ことは 言わないで ください。', "Please don't say such things."),
    PREFIX + '5-demonstratives.ああ':     E('ああ、そうですか。', 'Oh, I see.'),

    # Common verbs (Group 1)
    PREFIX + '27-verbs-group-1-verbs.行く':       E('学校に 行きます。', 'I go to school.'),
    PREFIX + '27-verbs-group-1-verbs.書く':       E('手紙を 書きます。', 'I write a letter.'),
    PREFIX + '27-verbs-group-1-verbs.聞く':       E('おんがくを 聞きます。', 'I listen to music.'),
    PREFIX + '27-verbs-group-1-verbs.読む':       E('本を 読みます。', 'I read a book.'),
    PREFIX + '27-verbs-group-1-verbs.飲む':       E('水を 飲みます。', 'I drink water.'),
    PREFIX + '27-verbs-group-1-verbs.話す':       E('日本語を 話します。', 'I speak Japanese.'),
    PREFIX + '27-verbs-group-1-verbs.買う':       E('くだものを 買います。', 'I buy fruit.'),
    PREFIX + '27-verbs-group-1-verbs.あう':       E('友だちに あいます。', 'I meet a friend.'),
    PREFIX + '27-verbs-group-1-verbs.あらう':     E('てを あらいます。', 'I wash my hands.'),
    PREFIX + '27-verbs-group-1-verbs.あそぶ':     E('こうえんで あそびます。', 'I play in the park.'),
    PREFIX + '27-verbs-group-1-verbs.いう':       E('「こんにちは」と いいます。', 'I say "hello".'),
    PREFIX + '27-verbs-group-1-verbs.およぐ':     E('うみで およぎます。', 'I swim in the sea.'),
    PREFIX + '27-verbs-group-1-verbs.おわる':     E('しごとが おわります。', 'Work ends.'),
    PREFIX + '27-verbs-group-1-verbs.かかる':     E('一時間 かかります。', 'It takes one hour.'),
    PREFIX + '27-verbs-group-1-verbs.きく':       E('みちを ききました。', 'I asked for directions.'),
    PREFIX + '27-verbs-group-1-verbs.のる':       E('バスに のります。', 'I get on the bus.'),
    PREFIX + '27-verbs-group-1-verbs.のぼる':     E('山に のぼります。', 'I climb the mountain.'),
    PREFIX + '27-verbs-group-1-verbs.はたらく':   E('会社で はたらきます。', 'I work at a company.'),
    PREFIX + '27-verbs-group-1-verbs.はじまる':   E('じゅぎょうが はじまります。', 'The class begins.'),

    # Common verbs (Group 2)
    PREFIX + '28-verbs-group-2-verbs.見る':       E('テレビを 見ます。', 'I watch TV.'),
    PREFIX + '28-verbs-group-2-verbs.食べる':     E('ごはんを 食べます。', 'I eat rice/a meal.'),
    PREFIX + '28-verbs-group-2-verbs.おきる':     E('七時に おきます。', 'I get up at seven.'),
    PREFIX + '28-verbs-group-2-verbs.ねる':       E('十一時に ねます。', 'I go to bed at eleven.'),
    PREFIX + '28-verbs-group-2-verbs.あける':     E('まどを あけて ください。', 'Please open the window.'),
    PREFIX + '28-verbs-group-2-verbs.しめる':     E('ドアを しめます。', 'I close the door.'),
    PREFIX + '28-verbs-group-2-verbs.おしえる':   E('日本語を おしえます。', 'I teach Japanese.'),
    PREFIX + '28-verbs-group-2-verbs.おぼえる':   E('かんじを おぼえます。', 'I memorize kanji.'),
    PREFIX + '28-verbs-group-2-verbs.かえる':     E('うちに かえります。', 'I return home. (Group 1 exception!)'),
    PREFIX + '28-verbs-group-2-verbs.でる':       E('家を でます。', 'I leave the house.'),

    # Verbs - irregular
    PREFIX + '29-verbs-irregular-and-suru.する':           E('しゅくだいを します。', 'I do my homework.'),
    PREFIX + '29-verbs-irregular-and-suru.来る':           E('友だちが 来ます。', 'A friend is coming.'),
    PREFIX + '29-verbs-irregular-and-suru.べんきょうする': E('日本語を べんきょうします。', 'I study Japanese.'),
    PREFIX + '29-verbs-irregular-and-suru.りょうりする':   E('ばんごはんを りょうりします。', 'I cook dinner.'),

    # Existence verbs
    PREFIX + '30-verbs-existence-and-poss.ある':       E('テーブルに 本が あります。', 'There is a book on the table.'),
    PREFIX + '30-verbs-existence-and-poss.いる':       E('へやに ねこが います。', "There's a cat in the room."),

    # i-adjectives (top common)
    PREFIX + '31-i-adjectives.大きい':     E('この かばんは 大きいです。', 'This bag is big.'),
    PREFIX + '31-i-adjectives.小さい':     E('ねこは 小さいです。', 'The cat is small.'),
    PREFIX + '31-i-adjectives.あたらしい': E('あたらしい 本を 買いました。', 'I bought a new book.'),
    PREFIX + '31-i-adjectives.古い':       E('この 古い 家は 百年です。', 'This old house is 100 years old.'),
    PREFIX + '31-i-adjectives.高い':       E('この とけいは 高いです。', 'This watch is expensive.'),
    PREFIX + '31-i-adjectives.安い':       E('この 安い かばんを 買います。', "I'll buy this cheap bag."),
    PREFIX + '31-i-adjectives.あつい':     E('夏は あついです。', 'Summer is hot.'),
    PREFIX + '31-i-adjectives.さむい':     E('冬は さむいです。', 'Winter is cold.'),
    PREFIX + '31-i-adjectives.おもしろい': E('この えいがは おもしろいです。', 'This movie is interesting.'),
    PREFIX + '31-i-adjectives.おいしい':   E('この りんごは おいしいです。', 'This apple is delicious.'),
    PREFIX + '31-i-adjectives.いそがしい': E('今週は いそがしいです。', 'This week is busy.'),
    PREFIX + '31-i-adjectives.ちいさい':   E('ちいさい 子どもが います。', "There's a small child."),
    PREFIX + '31-i-adjectives.ふるい':     E('ふるい 本を 読みました。', 'I read an old book.'),
    PREFIX + '31-i-adjectives.たかい':     E('たかい ビルが あります。', "There's a tall building."),
    PREFIX + '31-i-adjectives.やすい':     E('やすい くつを 買いました。', 'I bought cheap shoes.'),

    # na-adjectives (top common)
    PREFIX + '32-na-adjectives.きれい':     E('この 花は きれいです。', 'This flower is pretty.'),
    PREFIX + '32-na-adjectives.げんき':     E('わたしは げんきです。', 'I am fine/healthy.'),
    PREFIX + '32-na-adjectives.しずか':     E('としょかんは しずかです。', 'The library is quiet.'),
    PREFIX + '32-na-adjectives.にぎやか':   E('まちは にぎやかです。', 'The town is lively.'),
    PREFIX + '32-na-adjectives.ひま':       E('きょうは ひまです。', "I'm free today."),
    PREFIX + '32-na-adjectives.すき':       E('コーヒーが すきです。', 'I like coffee.'),
    PREFIX + '32-na-adjectives.きらい':     E('やさいが きらいです。', "I dislike vegetables."),
    PREFIX + '32-na-adjectives.じょうず':   E('かのじょは ピアノが じょうずです。', 'She is good at piano.'),
    PREFIX + '32-na-adjectives.へた':       E('わたしは うたが へたです。', "I'm bad at singing."),
    PREFIX + '32-na-adjectives.ゆうめい':   E('この レストランは ゆうめいです。', 'This restaurant is famous.'),
    PREFIX + '32-na-adjectives.しんせつ':   E('先生は しんせつです。', 'The teacher is kind.'),
    PREFIX + '32-na-adjectives.だいじょうぶ': E('だいじょうぶですか。', 'Are you okay?'),
    PREFIX + '32-na-adjectives.たいせつ':   E('家ぞくは たいせつです。', 'Family is important.'),
    PREFIX + '32-na-adjectives.べんり':     E('この アプリは べんりです。', 'This app is convenient.'),
    PREFIX + '32-na-adjectives.いろいろ':   E('いろいろな 国に 行きました。', "I've been to various countries."),

    # Question words tail
    PREFIX + '6-question-words.何':         E('これは 何ですか。', 'What is this?'),
    PREFIX + '6-question-words.何曜日':     E('きょうは 何曜日ですか。', 'What day of the week is it today?'),
    PREFIX + '6-question-words.何月':       E('たんじょうびは 何月ですか。', 'What month is your birthday?'),
    PREFIX + '6-question-words.何日':       E('きょうは 何日ですか。', 'What day of the month is it today?'),
    PREFIX + '6-question-words.何で':       E('何で 学校に 行きますか。', 'How do you go to school?'),
}


def main() -> int:
    """Match my additions by FORM rather than full ID — the section
    portion of the ID is hard to reconstruct from outside the data
    (e.g. '11-time-days-weeks-month' vs my guessed '11-time-days-
    weeks-months-y'). For each additions key, derive the form (the
    last dot-separated segment) and match against any vocab entry
    whose form == that token AND whose ID starts with the section
    prefix from the additions key.

    Falls back gracefully — if no entry matches, the addition is
    listed as not-found. False matches across sections are blocked
    by the section-prefix anchor.
    """
    vpath = ROOT / 'data' / 'vocab.json'
    data = json.loads(vpath.read_text(encoding='utf-8'))
    # Build: (section_prefix_token, form) -> entry
    # The section prefix token is the integer section number, e.g.
    # '11' for any '11-time-...' variant.
    by_section_form: dict[tuple[str, str], dict] = {}
    for v in data['entries']:
        vid = v.get('id', '')
        if not vid.startswith(PREFIX): continue
        rest = vid[len(PREFIX):]  # e.g. '11-time-days-weeks-month.今'
        if '.' not in rest: continue
        section_token = rest.split('-', 1)[0]  # '11'
        form = v.get('form', '')
        by_section_form[(section_token, form)] = v
    added, skipped, not_found = [], [], []
    for key, new_ex in ADDITIONS.items():
        if not key.startswith(PREFIX):
            not_found.append(key); continue
        rest = key[len(PREFIX):]
        if '.' not in rest:
            not_found.append(key); continue
        section_part, form_part = rest.split('.', 1)
        section_token = section_part.split('-', 1)[0]
        v = by_section_form.get((section_token, form_part))
        if v is None:
            not_found.append(key); continue
        existing = v.get('examples') or []
        if any(e.get('ja') == new_ex['ja'] for e in existing):
            skipped.append(key); continue
        existing.append(new_ex)
        v['examples'] = existing
        added.append(key)
    if added:
        vpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Added inline example to {len(added)} vocab entries.')
    if skipped: print(f'Skipped (already had it): {len(skipped)}')
    if not_found:
        print(f'NOT FOUND ({len(not_found)}):')
        for k in sorted(not_found):
            print(f'  {k}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
