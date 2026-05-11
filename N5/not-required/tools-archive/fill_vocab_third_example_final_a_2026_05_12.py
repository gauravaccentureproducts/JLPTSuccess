"""Final wave A — function words (particles / conjunctions /
demonstratives / numerals / counters / pronouns / expressions /
irregular verbs / question words). These were filtered out of
waves 1-14; now finishing P3 #15 to 100%.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    # Particles
    'n5.vocab.35-particles-functional-.の':     {'ja': 'これは 私の 本です。',                   'translation_en': 'This is my book.'},
    'n5.vocab.35-particles-functional-.に':     {'ja': '七時に 家を 出ます。',                  'translation_en': 'I leave home at 7.'},
    'n5.vocab.35-particles-functional-.は':     {'ja': 'きょうは いい てんきですね。',           'translation_en': 'Today is nice weather.'},
    'n5.vocab.35-particles-functional-.を':     {'ja': 'パンを 食べます。',                     'translation_en': 'I eat bread.'},
    'n5.vocab.34-conjunctions.が':              {'ja': '高いですが、おいしいです。',             'translation_en': 'It\'s expensive, but tasty.'},
    'n5.vocab.35-particles-functional-.が':    {'ja': '子どもが あそんで います。',             'translation_en': 'A child is playing.'},
    'n5.vocab.35-particles-functional-.で':    {'ja': 'バスで 行きます。',                     'translation_en': 'I go by bus.'},
    'n5.vocab.35-particles-functional-.と':    {'ja': '友だちと 出かけます。',                 'translation_en': 'I go out with a friend.'},
    'n5.vocab.35-particles-functional-.も':    {'ja': '私も 行きます。',                       'translation_en': 'I\'ll go too.'},
    'n5.vocab.35-particles-functional-.か':    {'ja': '行きますか、行きませんか。',             'translation_en': 'Will you go or not?'},
    'n5.vocab.34-conjunctions.から':            {'ja': 'さむいから、コートを きました。',        'translation_en': 'Because it\'s cold, I wore a coat.'},
    'n5.vocab.35-particles-functional-.から':  {'ja': '九時から しごとです。',                 'translation_en': 'Work starts at 9.'},
    'n5.vocab.35-particles-functional-.や':    {'ja': 'りんごや みかんを 買いました。',         'translation_en': 'I bought apples and mandarins (among other things).'},
    'n5.vocab.35-particles-functional-.ね':    {'ja': '今日は あついですね。',                'translation_en': 'It\'s hot today, isn\'t it?'},
    'n5.vocab.35-particles-functional-.まで':  {'ja': '五時まで しごとを します。',             'translation_en': 'I work until 5.'},
    'n5.vocab.35-particles-functional-.など':  {'ja': '本や ノートなどを 買いました。',         'translation_en': 'I bought books, notebooks, etc.'},
    'n5.vocab.35-particles-functional-.へ':    {'ja': '日本へ 行きたいです。',                'translation_en': 'I want to go to Japan.'},
    'n5.vocab.35-particles-functional-.だけ':  {'ja': '一人だけ 来ました。',                  'translation_en': 'Only one person came.'},
    'n5.vocab.35-particles-functional-.よ':    {'ja': 'もう おわりましたよ。',                'translation_en': 'It\'s already finished, FYI.'},
    'n5.vocab.35-particles-functional-.しか':  {'ja': '一人しか いません。',                  'translation_en': 'There\'s only one person.'},
    'n5.vocab.35-particles-functional-.ぐらい':{'ja': '駅まで 十分ぐらい かかります。',         'translation_en': 'It takes about 10 minutes to the station.'},
    'n5.vocab.35-particles-functional-.ずつ':  {'ja': '一つずつ 取って ください。',             'translation_en': 'Please take one each.'},
    'n5.vocab.35-particles-functional-.ごろ':  {'ja': '三時ごろ 来て ください。',              'translation_en': 'Please come around 3.'},

    # Conjunctions
    'n5.vocab.34-conjunctions.でも':            {'ja': 'あめでした。でも、出かけました。',        'translation_en': 'It rained. But I went out anyway.'},
    'n5.vocab.34-conjunctions.そして':           {'ja': '朝ごはんを 食べました。そして、学校へ 行きました。','translation_en': 'I ate breakfast. And then I went to school.'},
    'n5.vocab.34-conjunctions.しかし':           {'ja': 'むずかしいです。しかし、おもしろいです。','translation_en': 'It\'s difficult. However, it\'s interesting.'},
    'n5.vocab.34-conjunctions.だから':           {'ja': 'あめだから、家に いました。',             'translation_en': 'It was raining, so I stayed home.'},
    'n5.vocab.34-conjunctions.けれど':           {'ja': '高いけれど、買いました。',               'translation_en': 'It was expensive but I bought it.'},
    'n5.vocab.34-conjunctions.それから':          {'ja': '本を 読みました。それから、ねました。',  'translation_en': 'I read a book. After that, I slept.'},
    'n5.vocab.34-conjunctions.または':           {'ja': 'コーヒー または おちゃに します。',       'translation_en': 'I\'ll have coffee or tea.'},
    'n5.vocab.34-conjunctions.ですから':          {'ja': '雨です。ですから、出かけません。',        'translation_en': 'It\'s raining. Therefore, I won\'t go out.'},
    'n5.vocab.34-conjunctions.ところで':          {'ja': 'ところで、しゅくだいは おわりましたか。','translation_en': 'By the way, did you finish the homework?'},
    'n5.vocab.34-conjunctions.それで':           {'ja': 'あめでした。それで、出かけませんでした。','translation_en': 'It was raining. And so, I didn\'t go out.'},
    'n5.vocab.34-conjunctions.それに':           {'ja': '安いです。それに、おいしいです。',        'translation_en': 'It\'s cheap. Moreover, it\'s tasty.'},

    # Verb-3 (irregular)
    'n5.vocab.29-verbs-irregular-and-v.する':    {'ja': '毎日 べんきょうを します。',             'translation_en': 'I study every day.'},
    'n5.vocab.29-verbs-irregular-and-v.来る':   {'ja': '友だちが 来ました。',                  'translation_en': 'My friend came.'},
    'n5.vocab.29-verbs-irregular-and-v.べんきょうする':{'ja': '日本語を べんきょうしています。', 'translation_en': 'I\'m studying Japanese.'},
    'n5.vocab.29-verbs-irregular-and-v.けっこんする':{'ja': '来年 けっこんします。',             'translation_en': 'I\'m getting married next year.'},
    'n5.vocab.29-verbs-irregular-and-v.さんぽする':{'ja': 'こうえんで さんぽします。',           'translation_en': 'I take a walk in the park.'},
    'n5.vocab.29-verbs-irregular-and-v.りょこうする':{'ja': 'らいねん 日本へ りょこうします。',  'translation_en': 'I\'ll travel to Japan next year.'},
    'n5.vocab.29-verbs-irregular-and-v.れんしゅうする':{'ja': '毎日 ピアノを れんしゅうします。','translation_en': 'I practice piano every day.'},
    'n5.vocab.29-verbs-irregular-and-v.しつもんする':{'ja': '先生に しつもんしました。',          'translation_en': 'I asked the teacher a question.'},
    'n5.vocab.29-verbs-irregular-and-v.しごとする':{'ja': '父は 大きい 会社で しごとします。', 'translation_en': 'My father works at a big company.'},
    'n5.vocab.29-verbs-irregular-and-v.電話する':{'ja': 'あした 母に 電話します。',             'translation_en': 'I\'ll call my mother tomorrow.'},
    'n5.vocab.29-verbs-irregular-and-v.コピーする':{'ja': 'この 紙を コピーして ください。',  'translation_en': 'Please copy this paper.'},
    'n5.vocab.29-verbs-irregular-and-v.そうじする':{'ja': '土曜日に へやを そうじします。',     'translation_en': 'I clean my room on Saturday.'},
    'n5.vocab.29-verbs-irregular-and-v.せんたくする':{'ja': '日曜日に せんたくします。',          'translation_en': 'I do laundry on Sunday.'},
    'n5.vocab.29-verbs-irregular-and-v.かいものする':{'ja': 'スーパーで かいものします。',       'translation_en': 'I go shopping at the supermarket.'},

    # Counters
    'n5.vocab.9-counters-common.人':             {'ja': '家族は 四人です。',                     'translation_en': 'My family has four members.'},
    'n5.vocab.9-counters-common.本':             {'ja': 'ペンを 三本 ください。',                'translation_en': 'Please give me three pens.'},
    'n5.vocab.9-counters-common.こ':             {'ja': 'りんごを 五こ 買いました。',             'translation_en': 'I bought five apples.'},
    'n5.vocab.9-counters-common.倍':             {'ja': 'その 二倍 ください。',                  'translation_en': 'Please give me twice that.'},
    'n5.vocab.9-counters-common.ど':             {'ja': 'にほんに 三ど 行きました。',             'translation_en': 'I\'ve been to Japan three times.'},
    'n5.vocab.9-counters-common.番':             {'ja': '一番 すきな いろは あおです。',         'translation_en': 'My most-favorite color is blue.'},
    'n5.vocab.9-counters-common.はい':            {'ja': 'コーヒーを 一ぱい ください。',           'translation_en': 'Please give me one cup of coffee.'},
    'n5.vocab.9-counters-common.まい':            {'ja': '紙を 五まい ください。',                'translation_en': 'Please give me five sheets of paper.'},
    'n5.vocab.9-counters-common.かい':            {'ja': '私は 三かいに すんで います。',         'translation_en': 'I live on the third floor.'},
    'n5.vocab.9-counters-common.かい.2':          {'ja': 'にほんに 二かい 行きました。',           'translation_en': 'I\'ve been to Japan twice.'},
    'n5.vocab.9-counters-common.だい':            {'ja': '車を 三だい もって います。',            'translation_en': 'I own three cars.'},
    'n5.vocab.9-counters-common.さつ':            {'ja': '本を 二さつ 買いました。',              'translation_en': 'I bought two books.'},
    'n5.vocab.9-counters-common.ひき':            {'ja': 'うちには ねこが 三びき います。',        'translation_en': 'We have three cats at home.'},
    'n5.vocab.9-counters-common.一人':            {'ja': '一人で 行きました。',                   'translation_en': 'I went alone.'},
    'n5.vocab.9-counters-common.二人':            {'ja': '二人で 食事に 行きました。',             'translation_en': 'The two of us went to eat.'},

    # Native counters series
    'n5.vocab.8-native-counters-series.十':      {'ja': '十さい いじょうの 人が 入れます。',     'translation_en': 'People 10 years old and over can enter.'},
    'n5.vocab.8-native-counters-series.一つ':     {'ja': 'おにぎりを 一つ 買いました。',           'translation_en': 'I bought one rice ball.'},
    'n5.vocab.8-native-counters-series.二つ':     {'ja': 'りんごを 二つ ください。',              'translation_en': 'Please give me two apples.'},
    'n5.vocab.8-native-counters-series.三つ':     {'ja': 'たまごを 三つ 食べました。',             'translation_en': 'I ate three eggs.'},
    'n5.vocab.8-native-counters-series.四つ':     {'ja': 'みかんを 四つ 買いました。',             'translation_en': 'I bought four mandarins.'},
    'n5.vocab.8-native-counters-series.五つ':     {'ja': 'かばんを 五つ 見ました。',              'translation_en': 'I looked at five bags.'},
    'n5.vocab.8-native-counters-series.六つ':     {'ja': 'おかしを 六つ 食べました。',             'translation_en': 'I ate six sweets.'},
    'n5.vocab.8-native-counters-series.七つ':     {'ja': 'いちごを 七つ もらいました。',           'translation_en': 'I received seven strawberries.'},
    'n5.vocab.8-native-counters-series.八つ':     {'ja': 'おもちを 八つ 食べました。',             'translation_en': 'I ate eight rice cakes.'},
    'n5.vocab.8-native-counters-series.九つ':     {'ja': 'きょうの しつもんは 九つです。',         'translation_en': 'Today\'s questions number nine.'},
    'n5.vocab.8-native-counters-series.いくつ':   {'ja': 'いくつ ありますか。',                 'translation_en': 'How many are there?'},

    # Numerals
    'n5.vocab.7-numbers.一':                     {'ja': 'コーヒーを 一杯 ください。',             'translation_en': 'Please give me one coffee.'},
    'n5.vocab.7-numbers.二':                     {'ja': '二時に かいぎが あります。',             'translation_en': 'There\'s a meeting at 2.'},
    'n5.vocab.7-numbers.三':                     {'ja': '三人で 行きます。',                     'translation_en': 'Three of us will go.'},
    'n5.vocab.7-numbers.四':                     {'ja': '家族は 四人です。',                     'translation_en': 'My family has four members.'},
    'n5.vocab.7-numbers.五':                     {'ja': '五時に おきます。',                    'translation_en': 'I get up at 5.'},
    'n5.vocab.7-numbers.六':                     {'ja': '六月から なつです。',                  'translation_en': 'Summer starts from June.'},
    'n5.vocab.7-numbers.七':                     {'ja': '七時に かえります。',                  'translation_en': 'I return at 7.'},
    'n5.vocab.7-numbers.八':                     {'ja': '八月は とても あついです。',            'translation_en': 'August is very hot.'},
    'n5.vocab.7-numbers.九':                     {'ja': '九時から しごとです。',                'translation_en': 'Work starts at 9.'},
    'n5.vocab.7-numbers.十':                     {'ja': '十時に ねます。',                      'translation_en': 'I go to bed at 10.'},
    'n5.vocab.7-numbers.十一':                   {'ja': '十一月は さむく なります。',            'translation_en': 'November gets cold.'},
    'n5.vocab.7-numbers.百':                     {'ja': 'りんごは 百円です。',                  'translation_en': 'An apple is 100 yen.'},
    'n5.vocab.7-numbers.千':                     {'ja': '本は 千円でした。',                    'translation_en': 'The book was 1000 yen.'},
    'n5.vocab.7-numbers.万':                     {'ja': '一万円 借りました。',                  'translation_en': 'I borrowed 10,000 yen.'},
    'n5.vocab.7-numbers.おく':                   {'ja': '一おく円は とても 大きい かずです。',  'translation_en': '100 million yen is a very big number.'},
    'n5.vocab.7-numbers.ゼロ':                   {'ja': '答えは ゼロです。',                    'translation_en': 'The answer is zero.'},
    'n5.vocab.7-numbers.一万':                   {'ja': '一万円 もって います。',                'translation_en': 'I have 10,000 yen.'},
    'n5.vocab.7-numbers.二十':                   {'ja': '今年で 二十さいに なります。',          'translation_en': 'I\'ll be 20 this year.'},

    # Demonstratives
    'n5.vocab.5-demonstratives.この':            {'ja': 'この 本は おもしろいです。',           'translation_en': 'This book is interesting.'},
    'n5.vocab.5-demonstratives.その':            {'ja': 'その くつは いくらですか。',           'translation_en': 'How much are those shoes?'},
    'n5.vocab.5-demonstratives.それ':            {'ja': 'それは 何ですか。',                   'translation_en': 'What is that?'},
    'n5.vocab.5-demonstratives.これ':            {'ja': 'これは 母からの プレゼントです。',     'translation_en': 'This is a present from my mother.'},
    'n5.vocab.5-demonstratives.そう':            {'ja': 'そう おもいます。',                   'translation_en': 'I think so.'},
    'n5.vocab.5-demonstratives.そんな':           {'ja': 'そんな ことは ありません。',           'translation_en': 'That sort of thing doesn\'t happen.'},
    'n5.vocab.5-demonstratives.ここ':            {'ja': 'ここで まちましょう。',                'translation_en': 'Let\'s wait here.'},
    'n5.vocab.5-demonstratives.そこ':            {'ja': 'そこに 本が あります。',               'translation_en': 'There\'s a book there.'},
    'n5.vocab.5-demonstratives.あれ':            {'ja': 'あれは ふじ山です。',                  'translation_en': 'That over there is Mt. Fuji.'},
    'n5.vocab.5-demonstratives.どの':            {'ja': 'どの 本が すきですか。',               'translation_en': 'Which book do you like?'},
    'n5.vocab.5-demonstratives.どこ':            {'ja': 'えきは どこですか。',                 'translation_en': 'Where is the station?'},
    'n5.vocab.5-demonstratives.こんな':           {'ja': 'こんな まちが すきです。',             'translation_en': 'I like this kind of town.'},
    'n5.vocab.5-demonstratives.あの':            {'ja': 'あの 人は 先生です。',                'translation_en': 'That person is the teacher.'},
    'n5.vocab.5-demonstratives.こちら':          {'ja': 'こちらへ どうぞ。',                    'translation_en': 'This way, please.'},
    'n5.vocab.5-demonstratives.こう':            {'ja': 'こう やって ください。',               'translation_en': 'Please do it like this.'},
    'n5.vocab.5-demonstratives.どんな':           {'ja': 'どんな 人ですか。',                   'translation_en': 'What kind of person is it?'},
    'n5.vocab.5-demonstratives.ああ':            {'ja': 'ああ いう ことを 言わないで ください。','translation_en': 'Please don\'t say that kind of thing.'},
    'n5.vocab.5-demonstratives.どちら':           {'ja': 'どちらに しますか。',                 'translation_en': 'Which one will you choose?'},
    'n5.vocab.5-demonstratives.どれ':            {'ja': 'どれが いちばん いいですか。',         'translation_en': 'Which is the best?'},
    'n5.vocab.5-demonstratives.こっち':           {'ja': 'こっちに 来て。',                     'translation_en': 'Come here (casual).'},
    'n5.vocab.5-demonstratives.そちら':           {'ja': 'そちらの ほうが いいですね。',          'translation_en': 'That way is better, isn\'t it?'},
    'n5.vocab.5-demonstratives.どっち':           {'ja': 'どっちが すきですか。',                'translation_en': 'Which one do you like?'},
    'n5.vocab.5-demonstratives.あそこ':           {'ja': 'あそこに ぎんこうが あります。',        'translation_en': 'There\'s a bank over there.'},
    'n5.vocab.5-demonstratives.あちら':           {'ja': 'あちらが 出口です。',                  'translation_en': 'The exit is that way.'},
    'n5.vocab.5-demonstratives.あっち':           {'ja': 'あっちに ホテルが あります。',          'translation_en': 'There\'s a hotel that way (casual).'},
    'n5.vocab.5-demonstratives.そっち':           {'ja': 'そっちは 何がありますか。',            'translation_en': 'What\'s over there (casual)?'},
    'n5.vocab.5-demonstratives.あんな':           {'ja': 'あんな きれいな いえに すみたいです。', 'translation_en': 'I want to live in such a beautiful house.'},

    # Pronouns
    'n5.vocab.1-people-pronouns-and-se.私':      {'ja': '私は 学生です。',                       'translation_en': 'I am a student.'},
    'n5.vocab.1-people-pronouns-and-se.あなた':  {'ja': 'あなたは 何さいですか。',                'translation_en': 'How old are you?'},
    'n5.vocab.1-people-pronouns-and-se.私たち':  {'ja': '私たちは クラスメートです。',             'translation_en': 'We are classmates.'},
    'n5.vocab.1-people-pronouns-and-se.じぶん':  {'ja': 'じぶんで しゅくだいを します。',         'translation_en': 'I do my homework by myself.'},
    'n5.vocab.1-people-pronouns-and-se.かれ':    {'ja': 'かれは 大学生です。',                   'translation_en': 'He is a university student.'},
    'n5.vocab.1-people-pronouns-and-se.かのじょ':{'ja': 'かのじょは 先生です。',                   'translation_en': 'She is a teacher.'},

    # Question words
    'n5.vocab.6-question-words.何':              {'ja': 'これは 何ですか。',                   'translation_en': 'What is this?'},
    'n5.vocab.6-question-words.いつ':            {'ja': 'いつ 帰りますか。',                   'translation_en': 'When will you return?'},
    'n5.vocab.6-question-words.何曜日':          {'ja': 'きょうは 何曜日ですか。',              'translation_en': 'What day of the week is it today?'},
    'n5.vocab.6-question-words.何月':            {'ja': 'たんじょうびは 何月ですか。',           'translation_en': 'What month is your birthday?'},
    'n5.vocab.6-question-words.何日':            {'ja': 'きょうは 何日ですか。',                'translation_en': 'What day of the month is it today?'},
    'n5.vocab.6-question-words.いくら':          {'ja': 'これは いくらですか。',                'translation_en': 'How much is this?'},
    'n5.vocab.6-question-words.いくつ':          {'ja': 'いくつ ありますか。',                 'translation_en': 'How many are there?'},
    'n5.vocab.6-question-words.何で':            {'ja': '何で 行きますか。',                   'translation_en': 'By what (means) will you go?'},
    'n5.vocab.6-question-words.何時':            {'ja': 'いま 何時ですか。',                   'translation_en': 'What time is it now?'},
    'n5.vocab.1-people-pronouns-and-se.だれ':    {'ja': 'あの 人は だれですか。',                'translation_en': 'Who is that person?'},
    'n5.vocab.1-people-pronouns-and-se.どなた':  {'ja': 'どなた様ですか。',                     'translation_en': 'Who is it (polite)?'},

    # Expressions (greetings + fillers)
    'n5.vocab.36-greetings-and-set-phr.ありがとう':{'ja': '本を かして くれて、ありがとう。',     'translation_en': 'Thanks for lending me the book.'},
    'n5.vocab.33-adverbs.どうも':                 {'ja': 'どうも ありがとうございます。',           'translation_en': 'Thank you very much.'},
    'n5.vocab.36-greetings-and-set-phr.どうも':   {'ja': 'どうも すみません。',                   'translation_en': 'I\'m really sorry.'},
    'n5.vocab.36-greetings-and-set-phr.ありがとうございます':{'ja': 'プレゼント、ありがとうございます。','translation_en': 'Thank you for the gift.'},
    'n5.vocab.36-greetings-and-set-phr.おはようございます':{'ja': 'おはようございます、先生。',     'translation_en': 'Good morning, teacher.'},
    'n5.vocab.36-greetings-and-set-phr.こんにちは':{'ja': 'こんにちは、田中さん。',                 'translation_en': 'Hello, Mr. Tanaka.'},
    'n5.vocab.36-greetings-and-set-phr.こんばんは':{'ja': 'こんばんは。よる おそく すみません。',   'translation_en': 'Good evening. Sorry it\'s late.'},
    'n5.vocab.36-greetings-and-set-phr.おやすみなさい':{'ja': 'もう ねます。おやすみなさい。',       'translation_en': 'I\'m going to bed. Good night.'},
    'n5.vocab.36-greetings-and-set-phr.さようなら':{'ja': 'では、さようなら。',                    'translation_en': 'Well then, goodbye.'},
    'n5.vocab.36-greetings-and-set-phr.しつれいします':{'ja': 'しつれいします、先に かえります。',  'translation_en': 'Excuse me, I\'m heading home first.'},
    'n5.vocab.36-greetings-and-set-phr.しつれいしました':{'ja': 'おそく なって しつれいしました。', 'translation_en': 'Excuse me for being late.'},
    'n5.vocab.36-greetings-and-set-phr.どういたしまして':{'ja': 'ありがとうございました。— どういたしまして。','translation_en': 'Thank you. — You\'re welcome.'},
    'n5.vocab.36-greetings-and-set-phr.ごめんなさい':{'ja': 'おそくなって、ごめんなさい。',         'translation_en': 'Sorry I\'m late.'},
    'n5.vocab.36-greetings-and-set-phr.いただきます':{'ja': 'いただきます。',                       'translation_en': '(Said before eating.)'},
    'n5.vocab.36-greetings-and-set-phr.ごちそうさまでした':{'ja': 'おいしかったです。ごちそうさまでした。','translation_en': 'It was delicious. Thank you for the meal.'},
    'n5.vocab.36-greetings-and-set-phr.いってきます':{'ja': 'では、いってきます。',                'translation_en': 'OK, I\'m off.'},
    'n5.vocab.36-greetings-and-set-phr.いってらっしゃい':{'ja': 'き気をつけて、いってらっしゃい。', 'translation_en': 'Be careful, see you later.'},
    'n5.vocab.36-greetings-and-set-phr.ただいま':  {'ja': 'ただいま。— おかえりなさい。',           'translation_en': 'I\'m home. — Welcome back.'},
    'n5.vocab.36-greetings-and-set-phr.おかえりなさい':{'ja': 'おかえりなさい。今日は どうでしたか。','translation_en': 'Welcome back. How was today?'},
    'n5.vocab.36-greetings-and-set-phr.はじめまして':{'ja': 'はじめまして、よろしく おねがいします。','translation_en': 'Nice to meet you, please treat me well.'},
    'n5.vocab.33-adverbs.どうぞよろしく':            {'ja': 'これから どうぞよろしく。',             'translation_en': 'Please treat me well from now on.'},
    'n5.vocab.36-greetings-and-set-phr.どうぞよろしく':{'ja': '本日は どうぞよろしく お願いします。','translation_en': 'Pleased to meet you today.'},
    'n5.vocab.36-greetings-and-set-phr.おげんきですか':{'ja': 'おげんきですか。— はい、げんきです。','translation_en': 'How are you? — I\'m fine, thank you.'},
    'n5.vocab.36-greetings-and-set-phr.おかげさまで': {'ja': 'おかげさまで、げんきです。',           'translation_en': 'Thanks to you, I\'m well.'},
    'n5.vocab.36-greetings-and-set-phr.いらっしゃいませ':{'ja': 'いらっしゃいませ、何名様ですか。','translation_en': 'Welcome, how many people?'},
    'n5.vocab.36-greetings-and-set-phr.おじゃまします':{'ja': 'おじゃまします。',                  'translation_en': '(Said when entering someone\'s home.)'},
    'n5.vocab.36-greetings-and-set-phr.おねがいします':{'ja': 'コーヒー、おねがいします。',        'translation_en': 'Coffee, please.'},
    'n5.vocab.36-greetings-and-set-phr.すみません':{'ja': 'すみません、みちが わかりません。',    'translation_en': 'Excuse me, I don\'t know the way.'},
    'n5.vocab.39-function-filler-expre.いかが':   {'ja': 'おちゃは いかがですか。',                'translation_en': 'How about some tea?'},
    'n5.vocab.39-function-filler-expre.じゃあ':   {'ja': 'じゃあ、また あした。',                'translation_en': 'Well then, see you tomorrow.'},
    'n5.vocab.39-function-filler-expre.それでは': {'ja': 'それでは、はじめましょう。',            'translation_en': 'Well then, let\'s begin.'},
    'n5.vocab.39-function-filler-expre.そうですか':{'ja': 'そうですか。それは すごいですね。',    'translation_en': 'Is that so? That\'s amazing.'},
    'n5.vocab.39-function-filler-expre.そうですね':{'ja': 'そうですね。考えて みます。',          'translation_en': 'Hmm, let me think about it.'},
    'n5.vocab.39-function-filler-expre.はい':     {'ja': 'はい、わかりました。',                 'translation_en': 'Yes, I understand.'},
    'n5.vocab.39-function-filler-expre.いいえ':   {'ja': 'いいえ、行きません。',                'translation_en': 'No, I won\'t go.'},
    'n5.vocab.39-function-filler-expre.うん':    {'ja': 'うん、いいよ。',                       'translation_en': 'Yeah, OK (casual).'},
    'n5.vocab.39-function-filler-expre.ええ':    {'ja': 'ええ、そうです。',                     'translation_en': 'Yes, that\'s right.'},
    'n5.vocab.39-function-filler-expre.ううん':  {'ja': 'ううん、ちがう。',                     'translation_en': 'No, that\'s wrong (casual).'},
    'n5.vocab.39-function-filler-expre.さあ':    {'ja': 'さあ、わかりません。',                 'translation_en': 'Hmm, I don\'t know.'},
    'n5.vocab.39-function-filler-expre.えーと':  {'ja': 'えーと、なまえは…',                    'translation_en': 'Um, my name is...'},
    'n5.vocab.39-function-filler-expre.あの':    {'ja': 'あの、すみません。',                   'translation_en': 'Um, excuse me.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_final_a')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {e['id']: e for e in data['entries']}
    n = 0
    not_found = 0
    for vid, ex in THIRD.items():
        e = by_id.get(vid)
        if not e:
            not_found += 1
            continue
        exs = e.get('examples') or []
        if len(exs) >= 3:
            continue
        exs.append({'ja': ex['ja'], 'translation_en': ex['translation_en'], 'provenance': 'llm_curated'})
        e['examples'] = exs
        n += 1
    print(f'\nFinal wave A added 3rd example on {n} entries. Not found: {not_found}.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
