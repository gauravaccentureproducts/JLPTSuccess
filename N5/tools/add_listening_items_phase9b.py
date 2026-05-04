"""Phase 9b (2026-05-03): expand listening corpus from 30 to 40 items.
10 new items, 4 task / 3 point / 3 utterance.

Schema mirrors existing entries: format / title_ja / audio / script_ja
/ prompt_ja / choices / correctAnswer / explanation_en.

JA-13 + JA-23 enforced post-run. All N5 scope.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

ITEMS = [
    # ===== TASK comprehension (4) =====
    {
        "id": "n5.listen.031",
        "format": "task",
        "title_ja": "プレゼントを えらぶ",
        "script_ja": (
            "男の人と 女の人が 話して います。男の人は 何を 買いますか。\n"
            "女：たんじょうびに 何を あげますか。\n"
            "男：本が いいかな。\n"
            "女：ぼうしも きれいですよ。\n"
            "男：そうですね。じゃ、ぼうしに します。"
        ),
        "prompt_ja": "男の人は 何を 買いますか。",
        "choices": ["本", "ぼうし", "とけい", "シャツ"],
        "correctAnswer": "ぼうし",
        "explanation_en": "The man initially considered a book but decided on a hat (ぼうしに します).",
    },
    {
        "id": "n5.listen.032",
        "format": "task",
        "title_ja": "週まつの よてい",
        "script_ja": (
            "二人が 話して います。男の人は 土よう日に 何を しますか。\n"
            "女：土よう日、何を しますか。\n"
            "男：友だちと えいがを 見に 行きます。\n"
            "女：日よう日も 出かけますか。\n"
            "男：日よう日は 家で 休みます。"
        ),
        "prompt_ja": "男の人は 土よう日に 何を しますか。",
        "choices": [
            "家で 休みます",
            "友だちと えいがを 見ます",
            "しごとを します",
            "学校に 行きます",
        ],
        "correctAnswer": "友だちと えいがを 見ます",
        "explanation_en": "Saturday plan is movies with friends (土よう日、えいがを 見に 行きます).",
    },
    {
        "id": "n5.listen.033",
        "format": "task",
        "title_ja": "ホテルの へや",
        "script_ja": (
            "じょうけい：ホテルの フロントで。\n"
            "女：すみません、いま 何かい いますか。\n"
            "男：今、五かいに います。\n"
            "女：レストランは どこですか。\n"
            "男：レストランは 一かいに あります。"
        ),
        "prompt_ja": "レストランは 何かいに ありますか。",
        "choices": ["一かい", "二かい", "五かい", "十かい"],
        "correctAnswer": "一かい",
        "explanation_en": "'レストランは 一かいに あります'.",
    },
    {
        "id": "n5.listen.034",
        "format": "task",
        "title_ja": "あさの じゅんび",
        "script_ja": (
            "母と 子どもが 話して います。子どもは あさ、まず 何を しますか。\n"
            "母：はやく かおを あらって。\n"
            "子：はい。あさごはんは。\n"
            "母：かおを あらってから 食べます。"
        ),
        "prompt_ja": "子どもは あさ、まず 何を しますか。",
        "choices": [
            "あさごはんを 食べる",
            "かおを あらう",
            "がっこうに 行く",
            "ねる",
        ],
        "correctAnswer": "かおを あらう",
        "explanation_en": "'はやく かおを あらって' — wash face first, then breakfast.",
    },

    # ===== POINT comprehension (3) =====
    {
        "id": "n5.listen.035",
        "format": "point",
        "title_ja": "学生の こくせき",
        "script_ja": (
            "女の学生が 話して います。\n"
            "わたしの クラスには 二十人 います。日本人は 五人です。中国人は 四人で、かんこく人も 四人 います。アメリカ人は 二人です。"
        ),
        "prompt_ja": "クラスに 中国人は 何人 いますか。",
        "choices": ["二人", "三人", "四人", "五人"],
        "correctAnswer": "四人",
        "explanation_en": "'中国人は 四人で'.",
    },
    {
        "id": "n5.listen.036",
        "format": "point",
        "title_ja": "りょこうの 日にち",
        "script_ja": (
            "男の人が しごとの あとで 話して います。\n"
            "来月の 七日から 九日まで、おおさかに 行きます。三日かんの りょこうです。新かんせんで 行きます。"
        ),
        "prompt_ja": "りょこうは 何日かんですか。",
        "choices": ["二日かん", "三日かん", "四日かん", "一週間"],
        "correctAnswer": "三日かん",
        "explanation_en": "'三日かんの りょこうです'. (Seventh through ninth = three days.)",
    },
    {
        "id": "n5.listen.037",
        "format": "point",
        "title_ja": "本の ねだん",
        "script_ja": (
            "店員が 話して います。\n"
            "この 本は 千五百円です。あの 大きい 本は 二千円です。きょうは セールで、ぜんぶ 半分の ねだんです。"
        ),
        "prompt_ja": "大きい 本は きょう いくらですか。",
        "choices": ["五百円", "千円", "千五百円", "二千円"],
        "correctAnswer": "千円",
        "explanation_en": "Big book is 2000 yen, half-price today = 1000 yen.",
    },

    # ===== UTTERANCE expression (3) =====
    {
        "id": "n5.listen.038",
        "format": "utterance",
        "title_ja": "りょかんに 入る とき",
        "script_ja": (
            "じょうけい：りょかんに 入る とき、ていねいに 言います。何と 言いますか。"
        ),
        "prompt_ja": "何と 言いますか。",
        "choices": [
            "ただいま",
            "おじゃまします",
            "おかえりなさい",
            "いただきます",
        ],
        "correctAnswer": "おじゃまします",
        "explanation_en": "おじゃまします is the polite phrase when entering someone’s home or place.",
    },
    {
        "id": "n5.listen.039",
        "format": "utterance",
        "title_ja": "店を 出る とき",
        "script_ja": (
            "じょうけい：ごはんを 食べた あとで、お金を はらいました。店を 出る とき、何と 言いますか。"
        ),
        "prompt_ja": "何と 言いますか。",
        "choices": [
            "いただきます",
            "ごちそうさまでした",
            "おはようございます",
            "おやすみなさい",
        ],
        "correctAnswer": "ごちそうさまでした",
        "explanation_en": "ごちそうさまでした is said after a meal when leaving the restaurant.",
    },
    {
        "id": "n5.listen.040",
        "format": "utterance",
        "title_ja": "先生に あった とき",
        "script_ja": (
            "じょうけい：あさ、学校で 先生に あいました。何と 言いますか。"
        ),
        "prompt_ja": "何と 言いますか。",
        "choices": [
            "おはようございます",
            "こんばんは",
            "さようなら",
            "おやすみなさい",
        ],
        "correctAnswer": "おはようございます",
        "explanation_en": "おはようございます = good morning (formal greeting in the morning).",
    },
]


def main() -> int:
    lpath = ROOT / 'data' / 'listening.json'
    data = json.loads(lpath.read_text(encoding='utf-8'))
    existing_ids = {it['id'] for it in data['items']}
    added = []
    skipped = []
    for it in ITEMS:
        if it['id'] in existing_ids:
            skipped.append(it['id'])
            continue
        it['audio'] = f"audio/listening/{it['id']}.mp3"
        data['items'].append(it)
        added.append(it['id'])
    if added:
        lpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Added {len(added)} listening items: {added}')
    if skipped: print(f'Skipped: {skipped}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
