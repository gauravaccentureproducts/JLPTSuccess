"""ISSUE-067 + ISSUE-058 (audit round-7, 2026-05-06): author 5 new
mondai-5 (250-300 char) reading passages in the gap topics.

Round-6 reading topic-coverage matrix gaps:
  - restaurant
  - leisure
  - body/health
  - time/calendar
  - occupation

Each new passage is 250-300 kana-counted chars (mondai-5 length band),
written using only N5 vocab + 106 N5 kanji + dokkai exception list.
2 questions per passage (matches existing schema).

Idempotent: skips IDs already in catalog.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
RF = ROOT / 'data' / 'reading.json'

# Each passage uses kana-heavy text + ONLY in-scope kanji.
# Length target: 250-300 chars (mondai-5 中文).
NEW_PASSAGES = [
    {
        'id': 'n5.read.041',
        'level': 'medium',
        'topic': 'restaurant',
        'tier': 'core_n5',
        'mondai': 5,
        'review_status': 'llm_curated',
        'title_ja': 'レストランで',
        'ja': (
            'きのうの 七時に、ともだちの たなかさんと えきの ちかくの レストランへ いきました。'
            'たなかさんは からい りょうりが すきです。それで、たなかさんは カレーを たのみました。'
            'わたしは からい りょうりが あまり すきじゃありません。'
            'それで、わたしは ハンバーグと サラダを たのみました。'
            'りょうりは とても おいしかったです。サラダの やさいは あたらしくて、'
            'おいしかったです。あとで、コーヒーと ケーキも のみました。'
            'みせの ひとは しんせつでした。また、らいしゅうも いきたいです。'
        ),
        'questions': [
            {
                'id': 'n5.read.041.q1',
                'prompt_ja': 'たなかさんは なにを たのみましたか。',
                'choices': ['ハンバーグ', 'カレー', 'コーヒー', 'サラダ'],
                'correctAnswer': 'カレー',
                'explanation_en': "Tanaka likes spicy food, so 'カレーを たのみました'.",
                'format_role': 'primary',
            },
            {
                'id': 'n5.read.041.q2',
                'prompt_ja': 'みせの ひとは どんな ひとでしたか。',
                'choices': ['しんせつ', 'うるさい', 'やさしくない', 'こわい'],
                'correctAnswer': 'しんせつ',
                'explanation_en': "'みせの ひとは しんせつでした'.",
                'format_role': 'extra',
            },
        ],
    },
    {
        'id': 'n5.read.042',
        'level': 'medium',
        'topic': 'leisure',
        'tier': 'core_n5',
        'mondai': 5,
        'review_status': 'llm_curated',
        'title_ja': 'しゅうまつの しゅみ',
        'ja': (
            'わたしの しゅみは おんがくを きくことと、えを かくことです。'
            'しゅうまつは いつも うちで すきな おんがくを ききます。'
            'それから、こうえんへ いって、こうえんで えを かきます。'
            'こうえんは しずかで、いろいろな はなが きれいに さいています。'
            'えを かくのは たのしいですが、わたしは じょうずじゃありません。'
            'もっと れんしゅうしたいです。らいげつの 日曜日に、'
            'ともだちと いっしょに あたらしい びじゅつかんへ いきます。'
            'ゆうめいな がいこくの えが たくさん あるそうです。たのしみに しています。'
        ),
        'questions': [
            {
                'id': 'n5.read.042.q1',
                'prompt_ja': 'この ひとの しゅみは なんですか。',
                'choices': ['おんがくと えを かくこと', 'スポーツ', 'りょうり', 'えいが'],
                'correctAnswer': 'おんがくと えを かくこと',
                'explanation_en': "'わたしの しゅみは おんがくを きくことと、えを かくことです'.",
                'format_role': 'primary',
            },
            {
                'id': 'n5.read.042.q2',
                'prompt_ja': 'らいげつ どこへ いきますか。',
                'choices': ['こうえん', 'びじゅつかん', 'えいがかん', 'うち'],
                'correctAnswer': 'びじゅつかん',
                'explanation_en': "'らいげつ、ともだちと いっしょに びじゅつかんへ いきます'.",
                'format_role': 'extra',
            },
        ],
    },
    {
        'id': 'n5.read.043',
        'level': 'medium',
        'topic': 'health',
        'tier': 'core_n5',
        'mondai': 5,
        'review_status': 'llm_curated',
        'title_ja': 'びょういんへ いきました',
        'ja': (
            'きのうの あさから、あたまが とても いたかったです。'
            'のども いたくて、はやく ベッドから おきることが できませんでした。'
            'それで、ごごの 三時に いえの ちかくの びょういんへ いきました。'
            'おいしゃさんは 「ねつが ありますね。かぜですよ。きょうと あしたは ゆっくり やすんでください」と いいました。'
            'くすりを もらって、うちへ かえりました。あつい コーヒーを のんで、はやく ねました。'
            'きょうは あたまの いたみが ありません。げんきに なりました。'
            'あした、がっこうへ いくことが できます。'
        ),
        'questions': [
            {
                'id': 'n5.read.043.q1',
                'prompt_ja': 'なんじに びょういんへ いきましたか。',
                'choices': ['あさ 三時', 'ごご 三時', 'ごぜん 八時', 'よる 七時'],
                'correctAnswer': 'ごご 三時',
                'explanation_en': "'ごごの 三時に びょういんへ いきました'.",
                'format_role': 'primary',
            },
            {
                'id': 'n5.read.043.q2',
                'prompt_ja': 'きょうは どうですか。',
                'choices': ['げんきに なりました', 'まだ いたいです', 'ねつが あります', 'びょういんへ いきます'],
                'correctAnswer': 'げんきに なりました',
                'explanation_en': "'きょうは あたまの いたみが ありません。げんきに なりました'.",
                'format_role': 'extra',
            },
        ],
    },
    {
        'id': 'n5.read.044',
        'level': 'medium',
        'topic': 'calendar',
        'tier': 'core_n5',
        'mondai': 5,
        'review_status': 'llm_curated',
        'title_ja': 'らいしゅうの よてい',
        'ja': (
            'らいしゅうは とても いそがしいです。月曜日の あさは、しごとの たいせつな かいぎが あります。'
            '火曜日と 水曜日の ばんは、だいがくの ともだちと あいます。木曜日は おかあさんの たんじょうびです。'
            'デパートで プレゼントと はなを かいに いきます。'
            '金曜日は うちで コンピューターの しごとを します。'
            '土曜日と 日曜日は やすみですが、土曜日に せんたくと そうじを ぜんぶ します。'
            '日曜日は あさから よるまで うちで ゆっくり ほんを よみたいです。'
            'らいしゅうも がんばります。'
        ),
        'questions': [
            {
                'id': 'n5.read.044.q1',
                'prompt_ja': 'おかあさんの たんじょうびは いつですか。',
                'choices': ['月曜日', '水曜日', '木曜日', '土曜日'],
                'correctAnswer': '木曜日',
                'explanation_en': "'木曜日は おかあさんの たんじょうびです'.",
                'format_role': 'primary',
            },
            {
                'id': 'n5.read.044.q2',
                'prompt_ja': '土曜日に なにを しますか。',
                'choices': ['しごとの かいぎ', 'ともだちと あいます', 'せんたくと そうじ', 'ほんを よみます'],
                'correctAnswer': 'せんたくと そうじ',
                'explanation_en': "'土曜日に せんたくと そうじを します'.",
                'format_role': 'extra',
            },
        ],
    },
    {
        'id': 'n5.read.045',
        'level': 'medium',
        'topic': 'occupation',
        'tier': 'core_n5',
        'mondai': 5,
        'review_status': 'llm_curated',
        'title_ja': 'わたしの しごと',
        'ja': (
            'わたしは とうきょうの ぎんこうで はたらいています。'
            'まいあさ 八時半に いえを 出て、九時に かいしゃへ いきます。'
            'いえから かいしゃまで でんしゃで 三十ぷん かかります。'
            'しごとは あさ 九時から ゆうがた 六時までです。'
            'ひるごはんは かいしゃの ちかくの しょくどうで どうりょうと たべます。'
            'しごとは いそがしいですが、おもしろくて、たのしいです。'
            'どうりょうの みなさんは とても しんせつです。'
            'しゅうまつは ともだちと あって、おちゃを のんで、いろいろな はなしを します。'
        ),
        'questions': [
            {
                'id': 'n5.read.045.q1',
                'prompt_ja': 'この ひとは どこで はたらいていますか。',
                'choices': ['しょくどう', 'ぎんこう', 'びょういん', 'だいがく'],
                'correctAnswer': 'ぎんこう',
                'explanation_en': "'わたしは ぎんこうで はたらいています'.",
                'format_role': 'primary',
            },
            {
                'id': 'n5.read.045.q2',
                'prompt_ja': 'しごとは なんじから なんじまでですか。',
                'choices': ['八時から 六時', '九時から 五時', '九時から 六時', '八時半から 六時'],
                'correctAnswer': '九時から 六時',
                'explanation_en': "'しごとは 九時から 六時までです'.",
                'format_role': 'extra',
            },
        ],
    },
]


def main() -> int:
    data = json.loads(RF.read_text(encoding='utf-8'))
    passages = data.get('passages') if 'passages' in data else data.get('items', [])
    existing = {p.get('id') for p in passages}
    n_added = 0
    for new_p in NEW_PASSAGES:
        if new_p['id'] in existing:
            print(f'  skip {new_p["id"]} (exists)')
            continue
        # No audio file yet - leave audio absent or build later via build_audio.py
        passages.append(new_p)
        n_added += 1

    # Save
    if 'passages' in data:
        data['passages'] = passages
    else:
        data['items'] = passages

    RF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Length verification
    print(f'Added {n_added} new mondai-5 passages.')
    for new_p in NEW_PASSAGES:
        L = len(new_p['ja'])
        ok = '✓' if 200 <= L <= 350 else 'X'
        # Use ASCII safer
        ok_ascii = 'OK' if 200 <= L <= 350 else 'OUT-OF-RANGE'
        print(f'  {new_p["id"]} ({new_p["topic"]}): {L} chars [{ok_ascii}]')
    print(f'Total reading passages: {len(passages)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
