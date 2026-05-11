"""Author a 3rd example sentence on the most-frequent vocab entries
currently stuck at 2 examples.

Audit context: 971/1009 vocab entries have exactly 2 examples
(audit's "Examples ≥3" bar = 4%). This pass authors a 3rd example
for the top ~40 most-frequent nouns / verbs / adjectives (filtered
by frequency_rank ascending).

For each entry, the new example:
  - Uses different grammatical context than the existing 2
  - Stays within N5 grammar
  - Reuses N5-set kanji only (kana for kanji above N5)
  - Carries a natural English translation

Schema (matches existing examples):
  {ja, translation_en, provenance: "llm_curated"}

Coverage target: 40/971 of the gap = small but representative
starter pass on the top-frequency vocabulary slice.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD_EXAMPLES = {
    'n5.vocab.4-body-parts.は': {
        'ja': 'はを みがいてから ねます。',
        'translation_en': 'I brush my teeth before going to bed.',
    },
    'n5.vocab.14-nature-and-weather.は': {
        'ja': 'あきには きの はが あかく なります。',
        'translation_en': 'In autumn, the leaves on the trees turn red.',
    },
    'n5.vocab.4-body-parts.て': {
        'ja': 'ごはんの まえに てを あらいましょう。',
        'translation_en': 'Let\'s wash our hands before the meal.',
    },
    'n5.vocab.26-house-and-furniture.と': {
        'ja': 'いえの まえの とを しめて ください。',
        'translation_en': 'Please close the door in front of the house.',
    },
    'n5.vocab.30-verbs-existence-and-p.いる.2': {
        'ja': 'これは いりますか。いいえ、いりません。',
        'translation_en': 'Do you need this? — No, I don\'t need it.',
    },
    'n5.vocab.30-verbs-existence-and-p.ある': {
        'ja': 'つくえの 上に 本が あります。',
        'translation_en': 'There is a book on the desk.',
    },
    'n5.vocab.1-people-pronouns-and-se.人': {
        'ja': 'あの 人は とても しんせつです。',
        'translation_en': 'That person is very kind.',
    },
    'n5.vocab.11-time-days-weeks-month.年': {
        'ja': '来年 日本へ いきたいです。',
        'translation_en': 'I want to go to Japan next year.',
    },
    'n5.vocab.11-time-days-weeks-month.日': {
        'ja': 'きょうは いい 日ですね。',
        'translation_en': 'Today is a nice day, isn\'t it?',
    },
    'n5.vocab.11-time-days-weeks-month.月': {
        'ja': '一月から 四月まで さむいです。',
        'translation_en': 'From January to April it is cold.',
    },
    'n5.vocab.14-nature-and-weather.月': {
        'ja': 'こん夜の 月は とても きれいです。',
        'translation_en': 'Tonight\'s moon is very beautiful.',
    },
    'n5.vocab.13-locations-and-places-.中': {
        'ja': 'かばんの 中に 何が ありますか。',
        'translation_en': 'What\'s inside the bag?',
    },
    'n5.vocab.27-verbs-group-1-verbs.なく': {
        'ja': 'いえの ねこが ないて います。',
        'translation_en': 'The cat at home is crying.',
    },
    'n5.vocab.25-languages-and-countri.日本': {
        'ja': '日本は アジアの 国です。',
        'translation_en': 'Japan is a country in Asia.',
    },
    'n5.vocab.31-adjectives.いい': {
        'ja': 'この えいがは とても いいです。',
        'translation_en': 'This movie is very good.',
    },
    'n5.vocab.10-time-general.今': {
        'ja': '今 何時ですか。',
        'translation_en': 'What time is it now?',
    },
    'n5.vocab.13-locations-and-places-.ところ': {
        'ja': 'この ところは とても しずかです。',
        'translation_en': 'This place is very quiet.',
    },
    'n5.vocab.12-time-frequency-sequen.前': {
        'ja': '食べる 前に 手を あらいます。',
        'translation_en': 'Before eating, I wash my hands.',
    },
    'n5.vocab.13-locations-and-places-.前': {
        'ja': '駅の 前で 会いましょう。',
        'translation_en': 'Let\'s meet in front of the station.',
    },
    'n5.vocab.4-body-parts.せ': {
        'ja': 'あの 人は せが 高いですね。',
        'translation_en': 'That person is tall, isn\'t he?',
    },
    'n5.vocab.10-time-general.時間': {
        'ja': '時間が ありません。いそぎましょう。',
        'translation_en': 'There\'s no time. Let\'s hurry.',
    },
    'n5.vocab.22-money-and-shopping.円': {
        'ja': 'この 本は 二千円です。',
        'translation_en': 'This book costs 2,000 yen.',
    },
    'n5.vocab.13-locations-and-places-.上': {
        'ja': 'つくえの 上に かばんが あります。',
        'translation_en': 'There is a bag on top of the desk.',
    },
    'n5.vocab.37-common-nouns-miscella.話': {
        'ja': 'おもしろい 話を 聞きました。',
        'translation_en': 'I heard an interesting story.',
    },
    'n5.vocab.24-school-and-study.本': {
        'ja': 'まいばん 本を 読みます。',
        'translation_en': 'I read a book every night.',
    },
    'n5.vocab.10-time-general.分': {
        'ja': '十分 まって ください。',
        'translation_en': 'Please wait for ten minutes.',
    },
    'n5.vocab.10-time-general.今日': {
        'ja': '今日は どようびです。',
        'translation_en': 'Today is Saturday.',
    },
    'n5.vocab.10-time-general.後': {
        'ja': '後で 電話します。',
        'translation_en': 'I\'ll call you later.',
    },
    'n5.vocab.27-verbs-group-1-verbs.言う': {
        'ja': '先生は 何と 言いましたか。',
        'translation_en': 'What did the teacher say?',
    },
    'n5.vocab.13-locations-and-places-.国': {
        'ja': 'あなたの 国は どこですか。',
        'translation_en': 'What country are you from?',
    },
    'n5.vocab.13-locations-and-places-.会社': {
        'ja': '父は 大きい 会社で はたらいて います。',
        'translation_en': 'My father works at a big company.',
    },
    'n5.vocab.25-languages-and-countri.アメリカ': {
        'ja': '兄は アメリカに すんで います。',
        'translation_en': 'My older brother lives in America.',
    },
    'n5.vocab.31-adjectives.くらい': {
        'ja': 'よるは みちが くらいです。',
        'translation_en': 'At night, the road is dark.',
    },
    'n5.vocab.3-people-roles.先生': {
        'ja': '日本語の 先生は しんせつです。',
        'translation_en': 'The Japanese teacher is kind.',
    },
    'n5.vocab.28-verbs-group-2-verbs.見る': {
        'ja': 'まいあさ ニュースを 見ます。',
        'translation_en': 'I watch the news every morning.',
    },
    'n5.vocab.32-adjectives.いろいろ': {
        'ja': 'いろいろな 国の 食べものが あります。',
        'translation_en': 'There are foods from various countries.',
    },
    'n5.vocab.37-common-nouns-miscella.大きな': {
        'ja': '大きな いえに すみたいです。',
        'translation_en': 'I want to live in a big house.',
    },
    'n5.vocab.37-common-nouns-miscella.ページ': {
        'ja': '十ページから 読みましょう。',
        'translation_en': 'Let\'s read from page 10.',
    },
    'n5.vocab.25-languages-and-countri.中国': {
        'ja': '中国は 大きい 国です。',
        'translation_en': 'China is a big country.',
    },
    'n5.vocab.37-common-nouns-miscella.先': {
        'ja': 'お先に しつれいします。',
        'translation_en': 'Excuse me for leaving first.',
    },
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_third_example_starter')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {e['id']: e for e in data['entries']}

    n = 0
    for vid, ex in THIRD_EXAMPLES.items():
        e = by_id.get(vid)
        if not e:
            print(f'  ! vocab not found: {vid}')
            continue
        exs = e.get('examples') or []
        if len(exs) >= 3:
            print(f'  - skip (already has 3+): {vid}')
            continue
        new_ex = {
            'ja': ex['ja'],
            'translation_en': ex['translation_en'],
            'provenance': 'llm_curated',
        }
        exs.append(new_ex)
        e['examples'] = exs
        n += 1

    print(f'\nAdded 3rd example on {n} vocab entries.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
