"""Phase 3 of the example-coverage authoring pass (2026-05-03).

50 foundational vocab entries get an inline example sentence on their
detail page. The picks are the highest-frequency uncovered entries:
pronouns, family terms, body parts, demonstratives, question words,
and core numerals.

Constraints:
  - JA must be N5-scope kanji + N5 vocab + kana
  - Each example demonstrates typical use of the target word
  - Translation is faithful but natural English

Idempotent.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# Map: vocab id -> example to attach as the FIRST inline example.
ADDITIONS = {
    # Pronouns
    'n5.vocab.1-people-pronouns-and-se.私':
        {'ja': '私は 学生です。', 'translation_en': 'I am a student.'},
    'n5.vocab.1-people-pronouns-and-se.私たち':
        {'ja': '私たちは 友だちです。', 'translation_en': 'We are friends.'},
    'n5.vocab.1-people-pronouns-and-se.かれ':
        {'ja': 'かれは とても しんせつです。', 'translation_en': 'He is very kind.'},
    'n5.vocab.1-people-pronouns-and-se.かのじょ':
        {'ja': 'かのじょは 日本語が じょうずです。', 'translation_en': 'She is good at Japanese.'},
    'n5.vocab.1-people-pronouns-and-se.みなさん':
        {'ja': 'みなさん、こんにちは。', 'translation_en': 'Hello everyone.'},
    'n5.vocab.1-people-pronouns-and-se.じぶん':
        {'ja': 'じぶんで しゅくだいを します。', 'translation_en': 'I do my homework by myself.'},

    # Family
    'n5.vocab.2-people-family.かぞく':
        {'ja': 'わたしの かぞくは 四人です。', 'translation_en': 'My family has four people.'},
    'n5.vocab.2-people-family.父':
        {'ja': '父は 先生です。', 'translation_en': 'My father is a teacher.'},
    'n5.vocab.2-people-family.母':
        {'ja': '母は りょうりが じょうずです。', 'translation_en': 'My mother is good at cooking.'},
    'n5.vocab.2-people-family.お父さん':
        {'ja': '田中さんの お父さんは いしゃです。', 'translation_en': "Tanaka-san's father is a doctor."},
    'n5.vocab.2-people-family.お母さん':
        {'ja': 'やまださんの お母さんは やさしいです。', 'translation_en': "Yamada-san's mother is kind."},
    'n5.vocab.2-people-family.あに':
        {'ja': 'あには 大学生です。', 'translation_en': 'My older brother is a university student.'},
    'n5.vocab.2-people-family.あね':
        {'ja': 'あねは 二十さいです。', 'translation_en': 'My older sister is twenty years old.'},
    'n5.vocab.2-people-family.おとうと':
        {'ja': 'おとうとは 七さいです。', 'translation_en': 'My younger brother is seven years old.'},
    'n5.vocab.2-people-family.いもうと':
        {'ja': 'いもうとは 学校に 行きます。', 'translation_en': 'My younger sister goes to school.'},
    'n5.vocab.2-people-family.おにいさん':
        {'ja': 'おにいさんは どこに いますか。', 'translation_en': 'Where is your older brother?'},
    'n5.vocab.2-people-family.おねえさん':
        {'ja': 'おねえさんは とても きれいです。', 'translation_en': 'Your older sister is very pretty.'},
    'n5.vocab.2-people-family.そふ':
        {'ja': 'そふは げんきです。', 'translation_en': 'My grandfather is healthy.'},
    'n5.vocab.2-people-family.そぼ':
        {'ja': 'そぼは 八十さいです。', 'translation_en': 'My grandmother is eighty years old.'},
    'n5.vocab.2-people-family.おじいさん':
        {'ja': 'おじいさんは 本を 読んで います。', 'translation_en': 'The old man is reading a book.'},
    'n5.vocab.2-people-family.おばあさん':
        {'ja': 'おばあさんが あいさつを しました。', 'translation_en': 'The old woman greeted me.'},
    'n5.vocab.2-people-family.おじさん':
        {'ja': 'おじさんは アメリカに すんで います。', 'translation_en': 'My uncle lives in America.'},
    'n5.vocab.2-people-family.おばさん':
        {'ja': 'おばさんは 花が すきです。', 'translation_en': 'My aunt likes flowers.'},
    'n5.vocab.2-people-family.男の子':
        {'ja': 'こうえんで 男の子が あそんで います。', 'translation_en': 'A boy is playing in the park.'},
    'n5.vocab.2-people-family.女の子':
        {'ja': '女の子が うたを うたって います。', 'translation_en': 'A girl is singing a song.'},
    'n5.vocab.2-people-family.男':
        {'ja': 'あの 男の 人は 先生です。', 'translation_en': 'That man is a teacher.'},
    'n5.vocab.2-people-family.女':
        {'ja': 'あの 女の 人は いしゃです。', 'translation_en': 'That woman is a doctor.'},
    'n5.vocab.2-people-family.大人':
        {'ja': '大人は 千円、子どもは 五百円です。', 'translation_en': 'Adults are 1000 yen, children are 500 yen.'},

    # Roles
    'n5.vocab.3-people-roles.せいと':
        {'ja': 'この 学校の せいとは 百人です。', 'translation_en': "This school has 100 pupils."},
    'n5.vocab.3-people-roles.いしゃ':
        {'ja': 'ちちは いしゃです。', 'translation_en': 'My father is a doctor.'},
    'n5.vocab.3-people-roles.会社員':
        {'ja': 'あには 会社員です。', 'translation_en': 'My older brother is a company employee.'},
    'n5.vocab.3-people-roles.駅員':
        {'ja': '駅員に みちを 聞きました。', 'translation_en': 'I asked the station staff for directions.'},
    'n5.vocab.3-people-roles.店員':
        {'ja': '店員さんに ねだんを 聞きました。', 'translation_en': 'I asked the shop clerk the price.'},

    # Body parts
    'n5.vocab.4-body-parts.からだ':
        {'ja': 'からだが つかれました。', 'translation_en': 'My body is tired.'},
    'n5.vocab.4-body-parts.かお':
        {'ja': '朝、かおを あらいます。', 'translation_en': 'I wash my face in the morning.'},
    'n5.vocab.4-body-parts.め':
        {'ja': 'めが いたいです。', 'translation_en': 'My eyes hurt.'},
    'n5.vocab.4-body-parts.みみ':
        {'ja': 'みみで おんがくを 聞きます。', 'translation_en': 'I listen to music with my ears.'},
    'n5.vocab.4-body-parts.くち':
        {'ja': 'くちを あけて ください。', 'translation_en': 'Please open your mouth.'},
    'n5.vocab.4-body-parts.は':
        {'ja': 'まいにち はを みがきます。', 'translation_en': 'I brush my teeth every day.'},
    'n5.vocab.4-body-parts.て':
        {'ja': 'ごはんの まえに てを あらいます。', 'translation_en': 'I wash my hands before meals.'},
    'n5.vocab.4-body-parts.あし':
        {'ja': 'あしが いたいです。', 'translation_en': 'My feet hurt.'},

    # Demonstratives
    'n5.vocab.5-demonstratives.あちら':
        {'ja': 'あちらが 田中さんです。', 'translation_en': 'That person over there is Tanaka-san.'},
    'n5.vocab.5-demonstratives.こっち':
        {'ja': 'こっちに 来て ください。', 'translation_en': 'Come this way please.'},
    'n5.vocab.5-demonstratives.そっち':
        {'ja': 'そっちは あぶないですよ。', 'translation_en': 'That way is dangerous.'},
    'n5.vocab.5-demonstratives.あっち':
        {'ja': 'あっちに えきが あります。', 'translation_en': 'The station is over that way.'},
    'n5.vocab.5-demonstratives.どっち':
        {'ja': 'どっちが いいですか。', 'translation_en': 'Which one is better?'},

    # Question words
    'n5.vocab.6-question-words.何':
        {'ja': 'これは 何ですか。', 'translation_en': 'What is this?'},
    'n5.vocab.6-question-words.何曜日':
        {'ja': 'きょうは 何曜日ですか。', 'translation_en': 'What day of the week is it today?'},
    'n5.vocab.6-question-words.何月':
        {'ja': 'たんじょうびは 何月ですか。', 'translation_en': 'What month is your birthday?'},
    'n5.vocab.6-question-words.何日':
        {'ja': 'きょうは 何日ですか。', 'translation_en': "What day of the month is it today?"},
    'n5.vocab.6-question-words.何で':
        {'ja': '何で 学校に 行きますか。', 'translation_en': 'How do you go to school?'},
}


def main() -> int:
    vpath = ROOT / 'data' / 'vocab.json'
    data = json.loads(vpath.read_text(encoding='utf-8'))
    added = []
    skipped = []
    not_found = set(ADDITIONS.keys())
    for v in data['entries']:
        vid = v.get('id')
        if vid not in ADDITIONS: continue
        not_found.discard(vid)
        existing = v.get('examples') or []
        new_ex = ADDITIONS[vid]
        if any(e.get('ja') == new_ex['ja'] for e in existing):
            skipped.append(vid)
            continue
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
    if not_found: print(f'WARNING - vocab ids not found: {sorted(not_found)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
