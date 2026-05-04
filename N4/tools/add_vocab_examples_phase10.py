"""Phase 10 (2026-05-03): close the inline-example gap. 132 vocab
entries previously had no inline `examples` array — they were only
cited via grammar.json's `vocab_ids`. This batch authors a dedicated
example sentence for each so vocab detail pages don't fall back on
the grammar-pattern citation.

All N5 scope (kanji + kana). Idempotent — skips entries that already
have at least one inline example.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
P = 'n5.vocab.'

def E(ja, en):
    return {'ja': ja, 'translation_en': en}

ADDITIONS = {
    # 1. Pronouns/Self
    P+'1-people-pronouns-and-se.あなた': E('あなたは どなたですか。', 'Who are you?'),
    P+'1-people-pronouns-and-se.かた': E('あの かたは 先生です。', 'That person is a teacher. (polite)'),
    P+'1-people-pronouns-and-se.人': E('あの 人は 田中さんです。', 'That person is Tanaka.'),
    P+'1-people-pronouns-and-se.だれ': E('それは だれの かばんですか。', 'Whose bag is that?'),
    P+'1-people-pronouns-and-se.どなた': E('どなたですか。', 'Who is it? (polite)'),

    # 2. Family
    P+'2-people-family.きょうだい': E('きょうだいは 二人 います。', 'I have two siblings.'),
    P+'2-people-family.りょうしん': E('りょうしんと 一いっしょに すんで います。', 'I live with my parents.'),
    P+'2-people-family.子ども': E('こうえんで 子どもが あそんで います。', 'A child is playing in the park.'),
    P+'2-people-family.ともだち': E('ともだちと えいがに 行きました。', 'I went to a movie with a friend.'),

    # 3. Roles
    P+'3-people-roles.学生': E('わたしは 大学の 学生です。', 'I am a university student.'),
    P+'3-people-roles.先生': E('先生に しつもんしました。', 'I asked the teacher a question.'),

    # 4. Body parts
    P+'4-body-parts.あたま': E('あたまが いたいです。', 'My head hurts.'),
    P+'4-body-parts.はな': E('はなが たかいです。', 'I have a high nose.'),
    P+'4-body-parts.おなか': E('おなかが すきました。', "I'm hungry. (lit. stomach is empty)"),

    # 5. Demonstratives
    P+'5-demonstratives.これ': E('これは 何ですか。', 'What is this?'),
    P+'5-demonstratives.それ': E('それを ください。', 'Please give me that.'),
    P+'5-demonstratives.あれ': E('あれは 学校です。', 'That is the school.'),
    P+'5-demonstratives.どれ': E('どれが いいですか。', 'Which one is good?'),
    P+'5-demonstratives.この': E('この 本は おもしろいです。', 'This book is interesting.'),
    P+'5-demonstratives.その': E('その かばんは わたしのです。', 'That bag is mine.'),
    P+'5-demonstratives.あの': E('あの 人は 田中さんです。', 'That person is Tanaka.'),
    P+'5-demonstratives.どの': E('どの 本が すきですか。', 'Which book do you like?'),
    P+'5-demonstratives.ここ': E('ここで まちます。', "I'll wait here."),
    P+'5-demonstratives.そこ': E('そこに 本が あります。', "There's a book there."),
    P+'5-demonstratives.あそこ': E('あそこに えきが あります。', "The station is over there."),
    P+'5-demonstratives.どこ': E('えきは どこですか。', 'Where is the station?'),
    P+'5-demonstratives.こちら': E('こちらは 田中さんです。', 'This is Tanaka. (introducing)'),
    P+'5-demonstratives.そちら': E('そちらは どうですか。', 'How about your side?'),
    P+'5-demonstratives.どちら': E('どちらが すきですか。', 'Which (of the two) do you like?'),
    P+'5-demonstratives.こんな': E('こんな 本を よみたいです。', 'I want to read this kind of book.'),
    P+'5-demonstratives.あんな': E('あんな 大きい 家に すみたいです。', 'I want to live in a house like that.'),
    P+'5-demonstratives.どんな': E('どんな りょうりが すきですか。', 'What kind of food do you like?'),
    P+'5-demonstratives.こう': E('こう 書いて ください。', 'Please write it like this.'),
    P+'5-demonstratives.そう': E('そうですね。', "That's right / That's so."),
    P+'5-demonstratives.どう': E('日本語は どうですか。', 'How is Japanese (going)?'),

    # 6. Question words
    P+'6-question-words.いつ': E('たんじょうびは いつですか。', 'When is your birthday?'),
    P+'6-question-words.いくら': E('これは いくらですか。', 'How much is this?'),
    P+'6-question-words.いくつ': E('りんごは いくつ ありますか。', 'How many apples are there?'),
    P+'6-question-words.何時': E('今 何時ですか。', 'What time is it now?'),
    P+'6-question-words.なぜ': E('なぜ 来ませんでしたか。', 'Why did you not come?'),
    P+'6-question-words.どうして': E('どうして おそく なりましたか。', 'Why are you late?'),

    # 9. Counters
    P+'9-counters-common.さつ': E('本を 三さつ 買いました。', 'I bought three books.'),
    P+'9-counters-common.ひき': E('ねこが 二ひき います。', 'There are two cats.'),

    # 10. Time-general
    P+'10-time-general.時間': E('時間が ありません。', "I don't have time."),
    P+'10-time-general.あさって': E('あさっては 土よう日です。', 'The day after tomorrow is Saturday.'),
    P+'10-time-general.びょう': E('十びょう まって ください。', 'Please wait ten seconds.'),

    # 11. Days/weeks/months
    P+'11-time-days-weeks-month.日': E('日が みじかく なりました。', 'The days have become shorter.'),
    P+'11-time-days-weeks-month.しゅうまつ': E('しゅうまつに 友だちと あいます。', "On the weekend I'll meet friends."),
    P+'11-time-days-weeks-month.たんじょうび': E('たんじょうびは 五月です。', 'My birthday is in May.'),

    # 12. Frequency/sequence
    P+'12-time-frequency-sequen.はじめて': E('はじめて 日本に 行きました。', "I went to Japan for the first time."),

    # 13. Locations
    P+'13-locations-and-places-.きょうしつ': E('きょうしつで べんきょうします。', 'I study in the classroom.'),
    P+'13-locations-and-places-.ちかく': E('家の ちかくに スーパーが あります。', "There's a supermarket near my house."),

    # 17. Food items
    P+'17-food-items.あめ': E('あめを 一つ 買いました。', 'I bought one piece of candy.'),

    # 24. School/study
    P+'24-school-and-study.べんきょう': E('まいにち べんきょうします。', 'I study every day.'),
    P+'24-school-and-study.しつもん': E('先生に しつもんを しました。', 'I asked the teacher a question.'),
    P+'24-school-and-study.かんじ': E('かんじを 書く れんしゅうを します。', 'I practice writing kanji.'),
    P+'24-school-and-study.しゃしん': E('家ぞくの しゃしんを 見せます。', "I'll show you a family photo."),

    # 26. House and furniture
    P+'26-house-and-furniture.へや': E('わたしの へやは 大きいです。', 'My room is big.'),
    P+'26-house-and-furniture.いま': E('いまで テレビを 見ます。', 'I watch TV in the living room.'),
    P+'26-house-and-furniture.つくえ': E('つくえの 上に 本が あります。', "There's a book on the desk."),
    P+'26-house-and-furniture.えいが': E('日よう日に えいがを 見ます。', 'I watch movies on Sundays.'),
    P+'26-house-and-furniture.おんがく': E('おんがくを 聞きながら べんきょうします。', 'I study while listening to music.'),

    # 27. Group-1 verbs
    P+'27-verbs-group-1-verbs.おもう': E('おもしろいと おもいます。', 'I think it is interesting.'),
    P+'27-verbs-group-1-verbs.すむ': E('東京に すんで います。', "I'm living in Tokyo."),
    P+'27-verbs-group-1-verbs.とる': E('かばんを とって ください。', 'Please take/pick up the bag.'),
    P+'27-verbs-group-1-verbs.とる.2': E('しゃしんを とります。', 'I take a photo.'),
    P+'27-verbs-group-1-verbs.なく': E('赤ちゃんが ないて います。', "The baby is crying."),
    P+'27-verbs-group-1-verbs.入る': E('へやに 入って ください。', 'Please enter the room.'),
    P+'27-verbs-group-1-verbs.休む': E('土よう日と 日よう日は 休みます。', 'I rest on Saturdays and Sundays.'),
    P+'27-verbs-group-1-verbs.分かる': E('日本語が 分かります。', 'I understand Japanese.'),
    P+'27-verbs-group-1-verbs.おす': E('ボタンを おします。', 'I push the button.'),
    P+'27-verbs-group-1-verbs.すう': E('たばこは すいません。', "I don't smoke."),
    P+'27-verbs-group-1-verbs.ちがう': E('それは ちがいます。', "That is different / wrong."),
    P+'27-verbs-group-1-verbs.つく': E('えきに 七時に つきました。', 'I arrived at the station at seven.'),
    P+'27-verbs-group-1-verbs.みがく': E('まいにち はを みがきます。', 'I brush my teeth every day.'),
    P+'27-verbs-group-1-verbs.あく': E('まどが あいて います。', 'The window is open.'),
    P+'27-verbs-group-1-verbs.ふる': E('雨が ふって います。', 'It is raining.'),
    P+'27-verbs-group-1-verbs.おく': E('かばんを いすに おきます。', 'I place my bag on the chair.'),
    P+'27-verbs-group-1-verbs.さく': E('はるに 花が さきます。', 'Flowers bloom in spring.'),

    # 28. Group-2 verbs
    P+'28-verbs-group-2-verbs.いる': E('へやに ねこが います。', "There's a cat in the room."),
    P+'28-verbs-group-2-verbs.わすれる': E('かさを わすれました。', 'I forgot my umbrella.'),
    P+'28-verbs-group-2-verbs.出かける': E('しゅうまつに 出かけます。', "I go out on the weekend."),
    P+'28-verbs-group-2-verbs.はじめる': E('日本語の べんきょうを はじめました。', "I started studying Japanese."),
    P+'28-verbs-group-2-verbs.あびる': E('あさ シャワーを あびます。', "I shower in the morning."),

    # 30. Existence/possession
    P+'30-verbs-existence-and-p.いる': E('家に いぬが います。', "There's a dog at home."),
    P+'30-verbs-existence-and-p.もらう': E('父に プレゼントを もらいました。', 'I received a present from my father.'),

    # 31. i-adjectives
    P+'31-adjectives.あつい': E('今日は あついです。', "It is hot today."),
    P+'31-adjectives.あつい.2': E('お茶が あついです。気を つけて ください。', 'The tea is hot. Please be careful.'),
    P+'31-adjectives.たのしい': E('パーティーは たのしかったです。', 'The party was fun.'),
    P+'31-adjectives.むずかしい': E('かんじは むずかしいです。', 'Kanji is difficult.'),
    P+'31-adjectives.あかるい': E('この へやは あかるいです。', "This room is bright."),
    P+'31-adjectives.くらい': E('そとは くらいです。', "It's dark outside."),
    P+'31-adjectives.あぶない': E('あぶないですから、気を つけて ください。', "It's dangerous, so please be careful."),
    P+'31-adjectives.ほしい': E('あたらしい かばんが ほしいです。', "I want a new bag."),

    # 32. na-adjectives
    P+'32-adjectives.かんたん': E('この もんだいは かんたんです。', "This problem is simple."),

    # 33. Adverbs
    P+'33-adverbs.ぜんぶ': E('ぜんぶ 食べました。', 'I ate everything.'),
    P+'33-adverbs.もう': E('もう ばんごはんを 食べました。', "I've already eaten dinner."),
    P+'33-adverbs.まだ': E('まだ しゅくだいを して いません。', "I haven't done my homework yet."),
    P+'33-adverbs.どうぞ': E('どうぞ、おかけ ください。', "Please, have a seat."),
    P+'33-adverbs.どうも': E('どうも ありがとう。', "Thank you very much."),
    P+'33-adverbs.どう': E('日本の せいかつは どうですか。', "How is life in Japan?"),
    P+'33-adverbs.なぜ': E('なぜ 来なかったのですか。', "Why did you not come?"),
    P+'33-adverbs.どうして': E('どうして 学校を 休みましたか。', "Why did you skip school?"),

    # 34. Conjunctions
    P+'34-conjunctions.そして': E('えきに 行きました。そして、電車に のりました。', "I went to the station. And then I got on the train."),
    P+'34-conjunctions.それから': E('しゅくだいを しました。それから、ねました。', "I did my homework. After that, I went to bed."),
    P+'34-conjunctions.でも': E('あついです。でも、まどは あけません。', "It's hot. But I won't open the window."),
    P+'34-conjunctions.しかし': E('むずかしかったです。しかし、おもしろかったです。', "It was difficult. However, it was interesting."),
    P+'34-conjunctions.から': E('あついから、まどを あけます。', "It's hot, so I'll open the window."),
    P+'34-conjunctions.ですから': E('雨です。ですから、出かけません。', "It's raining. Therefore, I won't go out."),

    # 35. Particles
    P+'35-particles-functional-.だけ': E('わたしだけ 行きます。', "Only I will go."),
    P+'35-particles-functional-.しか': E('百円しか ありません。', "I only have 100 yen."),
    P+'35-particles-functional-.ごろ': E('七時ごろ 家に かえります。', "I'll return home around seven."),
    P+'35-particles-functional-.ずつ': E('一つずつ 食べて ください。', "Please eat one at a time."),
    P+'35-particles-functional-.など': E('りんごや みかんなどを 買いました。', "I bought apples, oranges, and so on."),

    # 36. Greetings
    P+'36-greetings-and-set-phr.ありがとう': E('ありがとう、田中さん。', "Thanks, Tanaka."),
    P+'36-greetings-and-set-phr.ごちそうさまでした': E('ごちそうさまでした。とても おいしかったです。', "Thank you for the meal. It was delicious."),
    P+'36-greetings-and-set-phr.おげんきですか': E('おげんきですか。', "How are you?"),

    # 37. Common nouns misc
    P+'37-common-nouns-miscella.名前': E('名前を 教えて ください。', "Please tell me your name."),
    P+'37-common-nouns-miscella.しごと': E('しごとは いそがしいです。', "Work is busy."),
    P+'37-common-nouns-miscella.りょこう': E('夏に りょこうします。', "I'll travel in the summer."),
    P+'37-common-nouns-miscella.スポーツ': E('スポーツが すきです。', "I like sports."),
    P+'37-common-nouns-miscella.プレゼント': E('友だちに プレゼントを あげました。', "I gave a present to my friend."),
    P+'37-common-nouns-miscella.けっこん': E('来年 けっこんします。', "I will get married next year."),
    P+'37-common-nouns-miscella.しゃしん': E('しゃしんを とりましょう。', "Let's take a photo."),
    P+'37-common-nouns-miscella.シャワー': E('あさ シャワーを あびます。', "I shower in the morning."),
    P+'37-common-nouns-miscella.たばこ': E('ここで たばこは すえません。', "You can't smoke here."),
    P+'37-common-nouns-miscella.やすみ': E('あしたは やすみです。', "Tomorrow is a day off."),

    # 38. Sounds
    P+'38-sounds-and-voice.こえ': E('大きい こえで 話して ください。', "Please speak in a loud voice."),

    # 39. Function fillers
    P+'39-function-filler-expre.あの': E('あの、すみません。', "Um, excuse me."),
    P+'39-function-filler-expre.いかが': E('コーヒーは いかがですか。', "How about some coffee? (polite)"),

    # 40. Misc useful
    P+'40-misc-useful-items.名前': E('お名前を おねがいします。', "Your name please."),
    P+'40-misc-useful-items.しごと': E('父の しごとは 先生です。', "My father's job is teacher."),
}


def main() -> int:
    vpath = ROOT / 'data' / 'vocab.json'
    data = json.loads(vpath.read_text(encoding='utf-8'))
    by_id = {v['id']: v for v in data['entries']}
    added, skipped, not_found = [], [], []
    for vid, new_ex in ADDITIONS.items():
        v = by_id.get(vid)
        if v is None:
            not_found.append(vid); continue
        existing = v.get('examples') or []
        if any(e.get('ja') == new_ex['ja'] for e in existing):
            skipped.append(vid); continue
        existing.append(new_ex)
        v['examples'] = existing
        added.append(vid)
    if added:
        vpath.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                         encoding='utf-8')
    print(f'Added inline example to {len(added)} vocab entries.')
    if skipped: print(f'Skipped (already had it): {len(skipped)}')
    if not_found:
        print(f'NOT FOUND ({len(not_found)}):')
        for v in sorted(not_found):
            print(f'  {v}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
