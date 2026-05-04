"""Phase 2 of the example-coverage authoring pass (2026-05-03).

63 grammar patterns in data/grammar.json have fewer than 3 examples.
Author 1-2 additional natural N5-scope examples per pattern to reach
the 3+ baseline.

Each addition is:
  - ja:             a natural N5 sentence using the pattern
  - form:           tag matching the pattern's form_rules.conjugations
                    (affirmative / negative / past / etc., or a generic
                    `affirmative` when no specific form applies)
  - translation_en: faithful English translation
  - vocab_ids:      empty list — the link_grammar_examples_to_vocab.py
                    tool can auto-populate later. JA-17 only requires
                    the field exist.

Constraints:
  - JA-13: no out-of-scope kanji in stems / examples
  - JA-17: vocab_ids field present (list)

Idempotent: re-running after the migration is a no-op (skips additions
already present by ja-string match).
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# Map: pattern_id -> list of new examples to append.
ADDITIONS = {
    'n5-030': [
        {'ja': 'にほんごを 話すのは むずかしいです。', 'form': 'affirmative',
         'translation_en': 'Speaking Japanese is difficult.'},
    ],
    'n5-034': [
        {'ja': 'りんごは 一つしか ありません。', 'form': 'affirmative',
         'translation_en': 'There is only one apple.'},
    ],
    'n5-038': [
        {'ja': '子どもたちに あめを 二つずつ あげました。', 'form': 'affirmative',
         'translation_en': 'I gave each child two candies.'},
    ],
    'n5-052': [
        {'ja': 'この かんじは どうやって 書きますか。', 'form': 'affirmative',
         'translation_en': 'How do you write this kanji?'},
    ],
    'n5-054': [
        {'ja': 'かばんの 中に 本が いくつ ありますか。', 'form': 'affirmative',
         'translation_en': 'How many books are in your bag?'},
    ],
    'n5-056': [
        {'ja': 'やすみは なんようびですか。', 'form': 'affirmative',
         'translation_en': 'What day of the week is your day off?'},
    ],
    'n5-057': [
        {'ja': 'なつ休みは なんがつからですか。', 'form': 'affirmative',
         'translation_en': 'When (what month) does summer vacation start?'},
    ],
    'n5-073': [
        {'ja': 'しゅくだいを まだ していません。', 'form': 'negative',
         'translation_en': "I haven't done my homework yet."},
    ],
    'n5-096': [
        {'ja': 'あにより わたしのほうが 早く おきます。', 'form': 'affirmative',
         'translation_en': 'I get up earlier than my older brother.'},
    ],
    'n5-097': [
        {'ja': 'なつと ふゆと、どちらが すきですか。', 'form': 'affirmative',
         'translation_en': 'Which do you like better, summer or winter?'},
    ],
    'n5-100': [
        {'ja': '母は 字を 書くのが じょうずです。', 'form': 'affirmative',
         'translation_en': 'My mother is good at writing.'},
    ],
    'n5-105': [
        {'ja': 'びょういんに 行きたくないです。', 'form': 'negative',
         'translation_en': "I don't want to go to the hospital."},
    ],
    'n5-106': [
        {'ja': '休みが ほしいです。', 'form': 'affirmative',
         'translation_en': 'I want a day off.'},
    ],
    'n5-109': [
        {'ja': 'クラスに 学生は なんにん いますか。', 'form': 'affirmative',
         'translation_en': 'How many students are in the class?'},
    ],
    'n5-110': [
        {'ja': '本を 三さつ 読みました。', 'form': 'affirmative',
         'translation_en': 'I read three books.'},
    ],
    'n5-112': [
        {'ja': 'バスで 二十ぷん かかります。', 'form': 'affirmative',
         'translation_en': 'It takes 20 minutes by bus.'},
    ],
    'n5-113': [
        {'ja': 'えいがは 七時はんに はじまります。', 'form': 'affirmative',
         'translation_en': 'The movie starts at 7:30.'},
    ],
    'n5-116': [
        {'ja': 'まいとし 友だちと たんじょうびを いわいます。', 'form': 'affirmative',
         'translation_en': 'Every year I celebrate my birthday with friends.'},
    ],
    'n5-119': [
        {'ja': 'テストの まえに よく べんきょうしました。', 'form': 'affirmative',
         'translation_en': 'I studied well before the test.'},
    ],
    'n5-120': [
        {'ja': 'えいがを 見た あとで コーヒーを 飲みました。', 'form': 'affirmative',
         'translation_en': 'After watching the movie, I drank coffee.'},
    ],
    'n5-121': [
        {'ja': 'スーパーに 行きました。そして、パンを かいました。', 'form': 'affirmative',
         'translation_en': 'I went to the supermarket. And then I bought bread.'},
    ],
    'n5-122': [
        {'ja': '本を 読みました。それから、休みました。', 'form': 'affirmative',
         'translation_en': 'I read a book. After that, I rested.'},
    ],
    'n5-123': [
        {'ja': 'ねむかったです。でも、ねませんでした。', 'form': 'affirmative',
         'translation_en': 'I was sleepy. But I did not sleep.'},
    ],
    'n5-124': [
        {'ja': '雨が ふっていました。しかし、出かけました。', 'form': 'affirmative',
         'translation_en': 'It was raining. However, I went out.'},
        {'ja': '日本語は むずかしいです。しかし、たのしいです。', 'form': 'affirmative',
         'translation_en': 'Japanese is difficult. However, it is fun.'},
    ],
    'n5-125': [
        {'ja': 'では、しつもんは ありませんか。', 'form': 'affirmative',
         'translation_en': 'Well then, are there any questions?'},
    ],
    'n5-127': [
        {'ja': '日本語は たのしいけど、かんじが むずかしい。', 'form': 'affirmative',
         'translation_en': 'Japanese is fun, but kanji is hard.'},
    ],
    'n5-129': [
        {'ja': 'どうして 行きませんでしたか。―ねつが あったからです。', 'form': 'affirmative',
         'translation_en': 'Why didn\'t you go? — Because I had a fever.'},
        {'ja': 'どうして 学校を 休みましたか。―あたまが いたかったからです。', 'form': 'affirmative',
         'translation_en': 'Why did you skip school? — Because I had a headache.'},
    ],
    'n5-130': [
        {'ja': '先生に 花を あげました。', 'form': 'affirmative',
         'translation_en': 'I gave flowers to the teacher.'},
    ],
    'n5-131': [
        {'ja': '父に 時計を もらいました。', 'form': 'affirmative',
         'translation_en': 'I received a watch from my father.'},
    ],
    'n5-132': [
        {'ja': '先生が 本を くれました。', 'form': 'affirmative',
         'translation_en': 'The teacher gave me a book.'},
    ],
    'n5-133': [
        {'ja': 'さむいから、まどを しめてください。', 'form': 'affirmative',
         'translation_en': "It's cold, so please close the window."},
    ],
    'n5-134': [
        {'ja': 'お金が ないので、買えません。', 'form': 'negative',
         'translation_en': "I have no money, so I can't buy it."},
    ],
    'n5-142': [
        {'ja': 'のみものは おちゃに します。', 'form': 'affirmative',
         'translation_en': "I'll have tea for the drink."},
    ],
    'n5-144': [
        {'ja': 'テレビを 見ながら ごはんを 食べます。', 'form': 'affirmative',
         'translation_en': 'I eat while watching TV.'},
    ],
    'n5-145': [
        {'ja': 'この えいがは おもしろいと 思います。', 'form': 'affirmative',
         'translation_en': 'I think this movie is interesting.'},
    ],
    'n5-146': [
        {'ja': '田中さんは 「行きません」と 言いました。', 'form': 'negative',
         'translation_en': 'Tanaka-san said, "I will not go."'},
    ],
    'n5-149': [
        {'ja': 'すみません、メニューを ください。', 'form': 'affirmative',
         'translation_en': 'Excuse me, please give me the menu.'},
    ],
    'n5-151': [
        {'ja': 'コーヒーは いかがですか。', 'form': 'affirmative',
         'translation_en': 'How about some coffee?'},
    ],
    'n5-153': [
        {'ja': 'まだ ばんごはんを 食べていません。', 'form': 'negative',
         'translation_en': "I haven't eaten dinner yet."},
    ],
    'n5-154': [
        {'ja': 'もう 学校に 行きました。', 'form': 'affirmative',
         'translation_en': 'I already went to school.'},
    ],
    'n5-157': [
        {'ja': 'あした 友だちが 来るでしょう。', 'form': 'affirmative',
         'translation_en': 'My friend will probably come tomorrow.'},
    ],
    'n5-158': [
        {'ja': 'たぶん 田中さんは 学生だろう。', 'form': 'affirmative',
         'translation_en': 'Tanaka-san is probably a student.'},
    ],
    'n5-160': [
        {'ja': '学校の あとで としょかんに 行きます。', 'form': 'affirmative',
         'translation_en': 'After school I go to the library.'},
    ],
    'n5-161': [
        {'ja': 'ばんごはんの まえに 休みました。', 'form': 'affirmative',
         'translation_en': 'I rested before dinner.'},
    ],
    'n5-162': [
        {'ja': '出かける まえに かさを もちます。', 'form': 'affirmative',
         'translation_en': 'I take an umbrella before going out.'},
    ],
    'n5-163': [
        {'ja': 'ごはんを 食べた あとで お皿を あらいます。', 'form': 'affirmative',
         'translation_en': 'After eating, I wash the dishes.'},
    ],
    'n5-164': [
        {'ja': 'すずきさんは わたしの 友だちです。', 'form': 'affirmative',
         'translation_en': 'Suzuki-san is my friend.'},
    ],
    'n5-168': [
        {'ja': '日曜日は そうじしたり、せんたくしたり します。', 'form': 'affirmative',
         'translation_en': 'On Sundays I clean, do laundry, and so on.'},
        {'ja': 'パーティーで 食べたり 飲んだり しました。', 'form': 'past',
         'translation_en': 'At the party we ate, drank, and so on.'},
    ],
    'n5-169': [
        {'ja': '京都に 行ったことが あります。', 'form': 'affirmative',
         'translation_en': 'I have been to Kyoto.'},
    ],
    'n5-170': [
        {'ja': 'はやく ねたほうが いいです。', 'form': 'affirmative',
         'translation_en': "It's better to go to bed early."},
    ],
    'n5-171': [
        {'ja': 'おそく ねないほうが いいです。', 'form': 'negative',
         'translation_en': "It's better not to go to bed late."},
        {'ja': 'たくさん 飲まないほうが いいですよ。', 'form': 'negative',
         'translation_en': "You shouldn't drink too much."},
    ],
    'n5-172': [
        {'ja': '日曜日は 学校に 行かなくても いいです。', 'form': 'negative',
         'translation_en': "You don't have to go to school on Sundays."},
        {'ja': 'いそがなくても いいですよ。', 'form': 'negative',
         'translation_en': "You don't have to hurry."},
    ],
    'n5-173': [
        {'ja': 'はやく かえらなくては いけません。', 'form': 'affirmative',
         'translation_en': 'I have to go home early.'},
        {'ja': 'くすりを 飲まなくては いけない。', 'form': 'affirmative',
         'translation_en': 'I must take the medicine.'},
    ],
    'n5-174': [
        {'ja': 'あした 早く おきなくては なりません。', 'form': 'affirmative',
         'translation_en': 'I have to get up early tomorrow.'},
        {'ja': 'まいにち べんきょうしなくては ならない。', 'form': 'affirmative',
         'translation_en': 'I have to study every day.'},
    ],
    'n5-175': [
        {'ja': 'もう 行かないと いけません。', 'form': 'affirmative',
         'translation_en': 'I have to go now.'},
        {'ja': 'しゅくだいを しないと いけない。', 'form': 'affirmative',
         'translation_en': 'I have to do my homework.'},
    ],
    'n5-176': [
        {'ja': 'もう 行かなきゃ。', 'form': 'affirmative',
         'translation_en': 'I gotta go now. (casual)'},
        {'ja': 'はやく ねなくちゃ。', 'form': 'affirmative',
         'translation_en': 'I gotta go to bed early. (casual)'},
    ],
    'n5-177': [
        {'ja': 'この くつは 大きすぎます。', 'form': 'affirmative',
         'translation_en': 'These shoes are too big.'},
    ],
    'n5-178': [
        {'ja': 'なつ休みに 国へ かえるつもりです。', 'form': 'affirmative',
         'translation_en': 'I intend to go back home for summer break.'},
        {'ja': 'たばこを やめるつもりです。', 'form': 'affirmative',
         'translation_en': 'I intend to quit smoking.'},
    ],
    'n5-179': [
        {'ja': '田中さんは 「行かない」って 言ってた。', 'form': 'negative',
         'translation_en': 'Tanaka-san said he\'s not going. (casual)'},
        {'ja': 'えいがは おもしろかったって。', 'form': 'past',
         'translation_en': '(They said) the movie was fun. (casual)'},
    ],
    'n5-180': [
        {'ja': '日本語の 書きかたを 教えてください。', 'form': 'affirmative',
         'translation_en': 'Please teach me how to write Japanese.'},
        {'ja': 'えきまでの 行きかたが わかりません。', 'form': 'affirmative',
         'translation_en': "I don't know how to get to the station."},
    ],
    'n5-181': [
        {'ja': 'きょうは いい 天気だなあ。', 'form': 'affirmative',
         'translation_en': 'What nice weather today!'},
        {'ja': 'この ケーキは おいしいなあ。', 'form': 'affirmative',
         'translation_en': 'This cake is really delicious!'},
    ],
    'n5-182': [
        {'ja': 'うるさい！しゃべるな！', 'form': 'affirmative',
         'translation_en': 'Quiet! Stop talking! (rough)'},
        {'ja': 'ここに 入るな。', 'form': 'affirmative',
         'translation_en': 'Do not enter here. (sign)'},
    ],
    'n5-183': [
        {'ja': 'だれか 手つだってください。', 'form': 'affirmative',
         'translation_en': 'Someone please help me.'},
    ],
}


def main() -> int:
    gpath = ROOT / 'data' / 'grammar.json'
    data = json.loads(gpath.read_text(encoding='utf-8'))
    added: dict[str, int] = {}
    skipped: dict[str, int] = {}
    not_found = set(ADDITIONS.keys())
    total_added = 0

    for p in data['patterns']:
        pid = p.get('id')
        if pid not in ADDITIONS:
            continue
        not_found.discard(pid)
        existing = p.get('examples') or []
        existing_ja = {e.get('ja','') for e in existing}
        new_count = 0
        skip_count = 0
        for new_ex in ADDITIONS[pid]:
            if new_ex['ja'] in existing_ja:
                skip_count += 1
                continue
            # Ensure JA-17 contract: vocab_ids field exists as a list
            new_ex.setdefault('vocab_ids', [])
            existing.append(new_ex)
            new_count += 1
        if new_count:
            p['examples'] = existing
            added[pid] = new_count
            total_added += new_count
        if skip_count:
            skipped[pid] = skip_count

    if total_added:
        gpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Added {total_added} new grammar examples across {len(added)} patterns:')
    for pid in sorted(added.keys()):
        print(f'  {pid}: +{added[pid]}')
    if skipped:
        print(f'Skipped (already present): {sum(skipped.values())} across {len(skipped)} patterns')
    if not_found:
        print(f'WARNING - patterns not in data: {sorted(not_found)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
