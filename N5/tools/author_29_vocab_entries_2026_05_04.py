"""Author 29 new vocab.json entries to eliminate whitelist↔vocab.json drift.

Each of the 30 "missing-from-vocab.json" tokens (excluding 10 multi-form
aliases that are already documented as design) gets promoted to a full
structured catalog entry with form, reading, gloss, section, pos, and
1 example sentence.

Note: 30 → 29 unique entries because こうこうせい AND 高校生 (kana
+ kanji forms of "high school student") merge into a single entry
with form=高校生, reading=こうこうせい. build_data.py extracts both
form and reading into the whitelist, so one vocab entry covers both
whitelist tokens.

Section assignments matched against the 40 existing sections in
vocab.json. Section ID slugs verified by probing existing entries.
JA-31 POS parity respected: each MD entry's POS tag (already present
since the words appear in vocabulary_n5.md) is mirrored in the JSON
pos field. JA-13 only scans grammar/questions/reading/listening JSONs,
so non-N5 kanji forms (倍, 国籍, 週末) are permitted in vocab.json.

Idempotent: skips items already present in vocab.json by ID match.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

# Section slug map (from probe).
SECTIONS = {
    3:  ('3-people-roles',          '3. People - Roles'),
    9:  ('9-counters-common',       '9. Counters (Common)'),
    10: ('10-time-general',         '10. Time - General'),
    11: ('11-time-days-weeks-month', '11. Time - Days, Weeks, Months, Years'),
    13: ('13-locations-and-places-', '13. Locations and Places (general)'),
    14: ('14-nature-and-weather',   '14. Nature and Weather'),
    22: ('22-money-and-shopping',   '22. Money and Shopping'),
    24: ('24-school-and-study',     '24. School and Study'),
    25: ('25-languages-and-countri', '25. Languages and Countries'),
    26: ('26-house-and-furniture',  '26. House and Furniture'),
    27: ('27-verbs-group-1-verbs',  '27. Verbs - Group 1 (う-verbs)'),
    28: ('28-verbs-group-2-verbs',  '28. Verbs - Group 2 (る-verbs)'),
    33: ('33-adverbs',              '33. Adverbs'),
    36: ('36-greetings-and-set-phr', '36. Greetings and Set Phrases'),
    37: ('37-common-nouns-miscella', '37. Common Nouns - Miscellaneous'),
    40: ('40-misc-useful-items',    '40. Misc Useful Items'),
}


def E(form, reading, gloss, sect, pos, example_ja, example_en):
    """Construct a vocab.json entry."""
    slug, sect_name = SECTIONS[sect]
    return {
        'id': f'n5.vocab.{slug}.{form}',
        'form': form,
        'reading': reading,
        'gloss': gloss,
        'section': sect_name,
        'pos': pos,
        'examples': [{'ja': example_ja, 'translation_en': example_en}],
    }


# 29 entries (high school student is a single entry covering kana + kanji).
NEW_ENTRIES = [
    E('いっぱい', 'いっぱい', 'full / a lot',
      33, 'adverb',
      'コップに 水が いっぱい あります。',
      "There's a lot of water in the cup."),
    E('おくれる', 'おくれる', 'be late',
      28, 'verb-2',
      'バスが 来なかったので、学校に おくれました。',
      "The bus didn't come, so I was late to school."),
    E('おしらせ', 'おしらせ', 'announcement, notice',
      24, 'noun',
      '学校から おしらせが きました。',
      'An announcement came from school.'),
    E('おじゃまします', 'おじゃまします', "excuse me / I'm coming in (set phrase used when entering someone's home)",
      36, 'expression',
      '「おじゃまします」と 言って、友だちの うちに 入りました。',
      "I said 'excuse me' and entered my friend's house."),
    E('おてら', 'おてら', 'temple (Buddhist)',
      13, 'noun',
      'おてらは とても しずかです。',
      'The temple is very quiet.'),
    E('おもちゃ', 'おもちゃ', 'toy',
      40, 'noun',
      '子どもは おもちゃで あそびます。',
      'Children play with toys.'),
    E('高校生', 'こうこうせい', 'high school student',
      3, 'noun',
      'あには 高校生です。',
      'My older brother is a high school student.'),
    E('さくら', 'さくら', 'cherry blossom',
      14, 'noun',
      '四月に さくらが さきます。',
      'Cherry blossoms bloom in April.'),
    E('じゅんび', 'じゅんび', 'preparation',
      24, 'noun',
      'テストの じゅんびを します。',
      'I prepare for the test.'),
    E('ぜひ', 'ぜひ', 'by all means / definitely',
      33, 'adverb',
      'ぜひ あそびに 来て ください。',
      'Please come to visit by all means.'),
    E('ただ', 'ただ', 'just / only / simply',
      33, 'adverb',
      'ただの 友だちです。',
      "It's just a friend."),
    E('ためる', 'ためる', 'save / accumulate (e.g., money, points)',
      28, 'verb-2',
      'りょこうの ために お金を ためて います。',
      'I am saving money for a trip.'),
    E('たんご', 'たんご', 'vocabulary word',
      24, 'noun',
      '日本語の たんごを おぼえます。',
      'I memorize Japanese vocabulary.'),
    E('はらう', 'はらう', 'pay',
      27, 'verb-1',
      'コンビニで お金を はらいました。',
      'I paid the money at the convenience store.'),
    E('べつべつ', 'べつべつ', 'separately',
      33, 'adverb',
      'べつべつに はらいましょう。',
      "Let's pay separately."),
    E('アルバイト', 'アルバイト', 'part-time job (often shortened to バイト)',
      22, 'noun',
      'カフェで アルバイトを して います。',
      'I work part-time at a cafe.'),
    E('カフェ', 'カフェ', 'cafe',
      13, 'noun',
      'カフェで コーヒーを 飲みました。',
      'I drank coffee at the cafe.'),
    E('コンサート', 'コンサート', 'concert',
      40, 'noun',
      '土曜日に コンサートに 行きます。',
      "I'll go to the concert on Saturday."),
    E('コンビニ', 'コンビニ', 'convenience store',
      13, 'noun',
      'コンビニで パンを 買いました。',
      'I bought bread at the convenience store.'),
    E('スペイン人', 'スペインじん', 'Spanish person',
      25, 'noun',
      'あの 人は スペイン人です。',
      'That person is Spanish.'),
    E('セール', 'セール', 'sale (price reduction)',
      22, 'noun',
      'デパートで セールを して います。',
      "There's a sale at the department store."),
    E('フロント', 'フロント', 'reception desk / front desk',
      13, 'noun',
      'ホテルの フロントで かぎを もらいました。',
      'I got the key at the hotel reception desk.'),
    E('ベンチ', 'ベンチ', 'bench',
      26, 'noun',
      'こうえんの ベンチに すわりました。',
      'I sat on the park bench.'),
    E('倍', 'ばい', 'times / -fold (counter for multiplicative)',
      9, 'counter',
      'これは あれの 二ばい おおきいです。',
      'This is twice as big as that.'),
    E('出口', 'でぐち', 'exit',
      13, 'noun',
      'えきの 出口で あいましょう。',
      "Let's meet at the station exit."),
    E('国籍', 'こくせき', 'nationality',
      25, 'noun',
      'あなたの こくせきは 何ですか。',
      "What's your nationality?"),
    E('後', 'あと', 'after / later (時間的に後で)',
      10, 'noun',
      'ごはんの 後で べんきょうします。',
      "I'll study after dinner."),
    E('聞こえる', 'きこえる', 'be audible / can be heard (intransitive of 聞く)',
      28, 'verb-2',
      'となりの へやから 音楽が 聞こえます。',
      'I can hear music from the next room.'),
    E('週末', 'しゅうまつ', 'weekend',
      11, 'noun',
      'しゅうまつに りょこうに 行きます。',
      'I go on a trip on the weekend.'),
]


def main() -> int:
    p = ROOT / 'data' / 'vocab.json'
    vocab = json.loads(p.read_text(encoding='utf-8'))
    entries = vocab['entries']
    existing_ids = {e['id'] for e in entries}

    added = 0
    for new in NEW_ENTRIES:
        if new['id'] in existing_ids:
            continue
        entries.append(new)
        added += 1

    if added == 0:
        print('No changes (all 29 entries already authored).')
        return 0

    p.write_text(json.dumps(vocab, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Added {added} new vocab entries:')
    for new in NEW_ENTRIES:
        print(f'  + {new["id"]}  [{new["pos"]}]  {new["form"]} ({new["reading"]}) — {new["gloss"][:50]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
