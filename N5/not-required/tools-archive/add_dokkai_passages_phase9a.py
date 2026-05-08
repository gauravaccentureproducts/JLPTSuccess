"""Phase 9a (2026-05-03): expand dokkai (reading) corpus from 30 to 40
passages. 10 new passages with 2-3 comprehension questions each.

Topics chosen to fill gaps in the existing 30:
  - animals (わたしの いぬ)
  - work / part-time (アルバイト)
  - season (秋の とうきょう)
  - personal letter to friend
  - food preferences (すきな たべもの)
  - school event (学校の パーティー)
  - transport delay (電車の おくれ)
  - hobby (ピアノ)
  - shopping / sale (本やの セール) - info-search format
  - park walk (こうえんの さんぽ)

All N5 scope: kanji from kanji_n5.md catalog, vocab from N5 list.
Idempotent. JA-13 enforced.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

PASSAGES = [
    {
        "id": "n5.read.031",
        "level": "easy",
        "topic": "animals",
        "title_ja": "わたしの いぬ",
        "ja": "わたしの 家には 大きい 白い いぬが います。名前は シロです。シロは 五さいです。まいにち、あさと よる、こうえんで シロと さんぽします。シロは ボールが だいすきです。よく いっしょに あそびます。",
        "questions": [
            {
                "prompt_ja": "シロは 何さいですか。",
                "choices": ["三さい", "四さい", "五さい", "六さい"],
                "correctAnswer": "五さい",
                "explanation_en": "'シロは 五さいです'.",
                "format_role": "primary",
            },
            {
                "prompt_ja": "シロと どこで さんぽしますか。",
                "choices": ["家", "こうえん", "学校", "店"],
                "correctAnswer": "こうえん",
                "explanation_en": "'こうえんで シロと さんぽします'.",
                "format_role": "extra",
            },
        ],
        "tier": "core_n5",
    },
    {
        "id": "n5.read.032",
        "level": "medium",
        "topic": "work",
        "title_ja": "アルバイト",
        "ja": "わたしは 大学生です。月よう日と 水よう日と 金よう日に カフェで アルバイトを して います。じかんは 五時から 九時までです。しごとは たのしいですが、ときどき つかれます。お金を ためて、来年 日本に 行きたいです。",
        "questions": [
            {
                "prompt_ja": "アルバイトは いつですか。",
                "choices": [
                    "毎日",
                    "月よう日と 水よう日と 金よう日",
                    "土よう日と 日よう日",
                    "火よう日と 木よう日",
                ],
                "correctAnswer": "月よう日と 水よう日と 金よう日",
                "explanation_en": "'月よう日と 水よう日と 金よう日に カフェで アルバイト'.",
                "format_role": "primary",
            },
            {
                "prompt_ja": "どうして お金を ためますか。",
                "choices": [
                    "カフェを 買いたいから",
                    "日本に 行きたいから",
                    "車を 買いたいから",
                    "学校を やめたいから",
                ],
                "correctAnswer": "日本に 行きたいから",
                "explanation_en": "'お金を ためて、来年 日本に 行きたいです'.",
                "format_role": "extra",
            },
        ],
        "tier": "core_n5",
    },
    {
        "id": "n5.read.033",
        "level": "easy",
        "topic": "weather",
        "title_ja": "とうきょうの あき",
        "ja": "とうきょうの あきは とても きれいです。木の はが あかや きいろに なります。すずしくて、さんぽが たのしいです。あさは 七時ごろ、そらが あかいです。とりの こえも 聞こえます。あきは わたしの すきな きせつです。",
        "questions": [
            {
                "prompt_ja": "あきの あさは どんな てんきですか。",
                "choices": ["雨です", "そらが あかいです", "ゆきが ふります", "あついです"],
                "correctAnswer": "そらが あかいです",
                "explanation_en": "'あさは 七時ごろ、そらが あかいです'.",
                "format_role": "primary",
            },
            {
                "prompt_ja": "この 人の すきな きせつは いつですか。",
                "choices": ["はる", "なつ", "あき", "ふゆ"],
                "correctAnswer": "あき",
                "explanation_en": "'あきは わたしの すきな きせつです'.",
                "format_role": "extra",
            },
        ],
        "tier": "core_n5",
    },
    {
        "id": "n5.read.034",
        "level": "easy",
        "topic": "family",
        "title_ja": "友だちからの 手紙",
        "ja": "やまださんへ\nお元気ですか。わたしは 元気です。あした 学校で パーティーが あります。三時から 五時までです。先生も 来ます。たのしい ですから、来て ください。\nたなか",
        "questions": [
            {
                "prompt_ja": "パーティーは いつ ありますか。",
                "choices": ["きのう", "きょう", "あした", "来週"],
                "correctAnswer": "あした",
                "explanation_en": "'あした 学校で パーティーが あります'.",
                "format_role": "primary",
            },
            {
                "prompt_ja": "パーティーは どこで ありますか。",
                "choices": ["家", "学校", "こうえん", "店"],
                "correctAnswer": "学校",
                "explanation_en": "'あした 学校で パーティーが あります'.",
                "format_role": "extra",
            },
        ],
        "tier": "core_n5",
    },
    {
        "id": "n5.read.035",
        "level": "easy",
        "topic": "food",
        "title_ja": "すきな たべもの",
        "ja": "わたしは 日本の りょうりが だいすきです。とくに、すしと てんぷらが すきです。日よう日に よく レストランへ 行きます。きのうは 母と いっしょに ラーメンを 食べました。とても おいしかったです。",
        "questions": [
            {
                "prompt_ja": "とくに すきな りょうりは 何ですか。",
                "choices": ["カレー", "すしと てんぷら", "ラーメン", "パン"],
                "correctAnswer": "すしと てんぷら",
                "explanation_en": "'とくに、すしと てんぷらが すきです'.",
                "format_role": "primary",
            },
            {
                "prompt_ja": "きのうは 何を 食べましたか。",
                "choices": ["すし", "てんぷら", "ラーメン", "カレー"],
                "correctAnswer": "ラーメン",
                "explanation_en": "'きのうは 母と いっしょに ラーメンを 食べました'.",
                "format_role": "extra",
            },
            {
                "prompt_ja": "きのう だれと 食べましたか。",
                "choices": ["父", "母", "友だち", "一人で"],
                "correctAnswer": "母",
                "explanation_en": "'きのうは 母と いっしょに ラーメンを 食べました'.",
                "format_role": "extra",
            },
        ],
        "tier": "core_n5",
    },
    {
        "id": "n5.read.036",
        "level": "medium",
        "topic": "school",
        "title_ja": "学校の しゅくだい",
        "ja": "わたしの 学校は 月よう日から 金よう日までです。まいにち しゅくだいが あります。しゅくだいは 日本語と すうがくです。日本語の しゅくだいは ながいですが、おもしろいです。すうがくは むずかしいです。土よう日と 日よう日は 学校が 休みですから、しゅくだいも すこしです。",
        "questions": [
            {
                "prompt_ja": "学校は いつまでですか。",
                "choices": [
                    "月よう日から 金よう日まで",
                    "月よう日から 土よう日まで",
                    "毎日",
                    "火よう日から 木よう日まで",
                ],
                "correctAnswer": "月よう日から 金よう日まで",
                "explanation_en": "'月よう日から 金よう日までです'.",
                "format_role": "primary",
            },
            {
                "prompt_ja": "むずかしい しゅくだいは 何ですか。",
                "choices": ["日本語", "えいご", "すうがく", "りか"],
                "correctAnswer": "すうがく",
                "explanation_en": "'すうがくは むずかしいです'.",
                "format_role": "extra",
            },
        ],
        "tier": "core_n5",
    },
    {
        "id": "n5.read.037",
        "level": "medium",
        "topic": "transport",
        "title_ja": "電車の おくれ",
        "ja": "今日 わたしは 七時に 家を 出ました。でも、電車が おくれて、八時十分に 学校に つきました。先生に「すみません」と 言いました。先生は「だいじょうぶです」と 言いました。あしたは 早く 出ます。",
        "questions": [
            {
                "prompt_ja": "今日 何時に 家を 出ましたか。",
                "choices": ["六時", "七時", "八時", "九時"],
                "correctAnswer": "七時",
                "explanation_en": "'七時に 家を 出ました'.",
                "format_role": "primary",
            },
            {
                "prompt_ja": "学校に 何時に つきましたか。",
                "choices": ["七時十分", "八時", "八時十分", "九時"],
                "correctAnswer": "八時十分",
                "explanation_en": "'八時十分に 学校に つきました'.",
                "format_role": "extra",
            },
        ],
        "tier": "core_n5",
    },
    {
        "id": "n5.read.038",
        "level": "easy",
        "topic": "hobby",
        "title_ja": "わたしの しゅみ",
        "ja": "わたしの しゅみは ピアノです。五さいから ピアノを ならって います。今は 一週間に 二かい、ピアノきょうしつに 行きます。先生は とても しんせつです。来月、コンサートで ピアノを ひきます。たのしみです。",
        "questions": [
            {
                "prompt_ja": "いつから ピアノを ならって いますか。",
                "choices": ["三さい", "五さい", "七さい", "十さい"],
                "correctAnswer": "五さい",
                "explanation_en": "'五さいから ピアノを ならって います'.",
                "format_role": "primary",
            },
            {
                "prompt_ja": "一週間に 何かい きょうしつに 行きますか。",
                "choices": ["一かい", "二かい", "三かい", "毎日"],
                "correctAnswer": "二かい",
                "explanation_en": "'一週間に 二かい、ピアノきょうしつに 行きます'.",
                "format_role": "extra",
            },
        ],
        "tier": "core_n5",
    },
    {
        "id": "n5.read.039",
        "level": "info-search",
        "topic": "shopping",
        "title_ja": "本やの セール",
        "ja": "本やの おしらせ\n大セール！\n日にち：八月一日から 八月七日まで\n時間：あさ 十時から よる 八時まで\n本は ぜんぶ 半分の ねだんです。\n日本語の 本も えいごの 本も あります。\nぜひ 来て ください！",
        "questions": [
            {
                "prompt_ja": "セールは いつ おわりますか。",
                "choices": ["八月一日", "八月七日", "八月十日", "九月一日"],
                "correctAnswer": "八月七日",
                "explanation_en": "'八月一日から 八月七日まで'.",
                "format_role": "primary",
                "format_type": "info-search",
            },
            {
                "prompt_ja": "本は いくらに なりますか。",
                "choices": [
                    "ぜんぶ 千円",
                    "ぜんぶ 半分の ねだん",
                    "ぜんぶ ただ",
                    "ぜんぶ 二ばいの ねだん",
                ],
                "correctAnswer": "ぜんぶ 半分の ねだん",
                "explanation_en": "'本は ぜんぶ 半分の ねだんです'.",
                "format_role": "extra",
                "format_type": "info-search",
            },
        ],
        "tier": "core_n5",
    },
    {
        "id": "n5.read.040",
        "level": "easy",
        "topic": "nature",
        "title_ja": "こうえんの さんぽ",
        "ja": "土よう日の あさ、わたしは こうえんに 行きました。こうえんには 大きい 木が たくさん あります。子どもたちが ボールで あそんで いました。おじいさんは ベンチで 本を 読んで いました。とりの こえも 聞こえました。きれいな あさでした。",
        "questions": [
            {
                "prompt_ja": "土よう日の あさ、どこに 行きましたか。",
                "choices": ["学校", "こうえん", "店", "うみ"],
                "correctAnswer": "こうえん",
                "explanation_en": "'こうえんに 行きました'.",
                "format_role": "primary",
            },
            {
                "prompt_ja": "おじいさんは 何を して いましたか。",
                "choices": [
                    "ボールで あそんで いました",
                    "本を 読んで いました",
                    "うたを うたって いました",
                    "ねて いました",
                ],
                "correctAnswer": "本を 読んで いました",
                "explanation_en": "'おじいさんは ベンチで 本を 読んで いました'.",
                "format_role": "extra",
            },
        ],
        "tier": "core_n5",
    },
]


def main() -> int:
    rpath = ROOT / 'data' / 'reading.json'
    data = json.loads(rpath.read_text(encoding='utf-8'))
    existing_ids = {p['id'] for p in data['passages']}
    added = []
    skipped = []
    for p in PASSAGES:
        if p['id'] in existing_ids:
            skipped.append(p['id'])
            continue
        # Stamp question IDs and audio path
        for i, q in enumerate(p['questions'], 1):
            q.setdefault('id', f"{p['id']}.q{i}")
        p['audio'] = f"audio/reading/{p['id']}.mp3"
        data['passages'].append(p)
        added.append(p['id'])
    if added:
        rpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Added {len(added)} passages: {added}')
    if skipped: print(f'Skipped (already present): {skipped}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
