"""One-shot authoring script: add 18 new listening items (n5.listen.013-030)
to data/listening.json. Closes EB-1 (OQ-2 listening corpus 12 -> 30+).

All Japanese text uses N5-whitelist kanji + kana only (verified against
data/n5_kanji_whitelist.json). Scripts are short conversational
exchanges suitable for VOICEVOX rendering. Each item carries the
voice metadata `synthetic-voicevox-shikoku-metan` so the build pipeline
knows how to render it (when VOICEVOX is wired up).

Run once:
    python tools/add_listening_items.py
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "data" / "listening.json"
VOICE = "synthetic-voicevox-shikoku-metan"

NEW_ITEMS = [
    # TASK FORMAT (6 items) - choose what action / where / which option
    {
        "id": "n5.listen.013",
        "format": "task",
        "title_en": "What time to meet",
        "audio": "audio/listening/n5.listen.013.mp3",
        "script_ja": "A: あした 学校で 会いましょう。\nB: はい。何時に 会いますか。\nA: 9時はんに しましょう。\nB: わかりました。",
        "prompt_ja": "あした 何時に 会いますか。",
        "choices": ["8時", "8時はん", "9時", "9時はん"],
        "correctAnswer": "9時はん",
        "explanation_en": "A says 9時はんに しましょう (let's meet at 9:30). B agrees.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.014",
        "format": "task",
        "title_en": "Where to wait",
        "audio": "audio/listening/n5.listen.014.mp3",
        "script_ja": "男: 来週の 土ようび、駅の 前で まってください。\n女: 駅の どこですか。\n男: 北の 出口です。\n女: わかりました。",
        "prompt_ja": "女の人は どこで まちますか。",
        "choices": ["駅の 中", "駅の 北の 出口", "駅の 南の 出口", "駅の 前"],
        "correctAnswer": "駅の 北の 出口",
        "explanation_en": "When the woman asks for clarification, the man specifies the north exit.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.015",
        "format": "task",
        "title_en": "What to buy at the shop",
        "audio": "audio/listening/n5.listen.015.mp3",
        "script_ja": "母: 店で 何を 買いますか。\n子: りんごを 三つと、ぎゅうにゅうを 一本 買います。\n母: パンも 買いますか。\n子: いいえ、パンは いりません。",
        "prompt_ja": "子どもは 何を 買いますか。",
        "choices": ["りんごと ぎゅうにゅうと パン", "りんごと ぎゅうにゅう", "ぎゅうにゅうと パン", "りんごだけ"],
        "correctAnswer": "りんごと ぎゅうにゅう",
        "explanation_en": "The child names apples and milk, then declines bread.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.016",
        "format": "task",
        "title_en": "Going with whom",
        "audio": "audio/listening/n5.listen.016.mp3",
        "script_ja": "A: あしたの えいがは だれと 行きますか。\nB: はじめは 友だちと 行きました。 でも、友だちは いそがしいです。\nA: そうですか。\nB: ですから、母と 行きます。",
        "prompt_ja": "B さんは あした だれと 行きますか。",
        "choices": ["友だち", "父", "母", "ひとりで"],
        "correctAnswer": "母",
        "explanation_en": "B's friend is busy, so B goes with their mother.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.017",
        "format": "task",
        "title_en": "When the teacher will arrive",
        "audio": "audio/listening/n5.listen.017.mp3",
        "script_ja": "男: 先生は 何時に 来ますか。\n女: 三時に 来ます。 でも、道が こんで います。\n男: では、何時に なりますか。\n女: たぶん 三時はんです。",
        "prompt_ja": "先生は 何時に 来ますか。",
        "choices": ["二時", "三時", "三時はん", "四時"],
        "correctAnswer": "三時はん",
        "explanation_en": "Original plan was 3:00; due to traffic the actual arrival will be 3:30.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.018",
        "format": "task",
        "title_en": "How to travel",
        "audio": "audio/listening/n5.listen.018.mp3",
        "script_ja": "A: あした どこへ 行きますか。\nB: 父の 友だちの いえへ 行きます。\nA: 何で 行きますか。\nB: 電車で 行きます。",
        "prompt_ja": "あした B さんは 何で 行きますか。",
        "choices": ["車", "電車", "バス", "あるいて"],
        "correctAnswer": "電車",
        "explanation_en": "B answers 電車で 行きます (by train).",
        "voice": VOICE,
    },

    # POINT FORMAT (6 items) - extract a specific detail
    {
        "id": "n5.listen.019",
        "format": "point",
        "title_en": "Why no homework",
        "audio": "audio/listening/n5.listen.019.mp3",
        "script_ja": "先生: しゅくだいは しましたか。\n生徒: すみません。 きのう しゅくだいを しませんでした。\n先生: どうしてですか。\n生徒: あたまが いたかったです。",
        "prompt_ja": "生徒は どうして しゅくだいを しませんでしたか。",
        "choices": ["いそがしかったから", "あたまが いたかったから", "わすれたから", "本が なかったから"],
        "correctAnswer": "あたまが いたかったから",
        "explanation_en": "The student answers あたまが いたかったです (I had a headache).",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.020",
        "format": "point",
        "title_en": "How much was the book",
        "audio": "audio/listening/n5.listen.020.mp3",
        "script_ja": "A: その 本は いくらでしたか。\nB: 千五百円でした。\nA: 高いですね。\nB: でも、おもしろい 本ですよ。",
        "prompt_ja": "本は いくらでしたか。",
        "choices": ["五百円", "千円", "千五百円", "二千円"],
        "correctAnswer": "千五百円",
        "explanation_en": "B says 千五百円でした (it was 1,500 yen).",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.021",
        "format": "point",
        "title_en": "Library hours",
        "audio": "audio/listening/n5.listen.021.mp3",
        "script_ja": "学生: としょかんは 何時から 何時までですか。\n先生: 月よう日から 金よう日までは 9時から 5時までです。 土ようびは 1時から 4時までです。",
        "prompt_ja": "月よう日の としょかんは 何時から 何時までですか。",
        "choices": ["8時から 4時まで", "9時から 5時まで", "1時から 4時まで", "9時から 4時まで"],
        "correctAnswer": "9時から 5時まで",
        "explanation_en": "Monday is in the weekday range (月-金), which is 9-5. The 1-4 hours apply only to Saturday.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.022",
        "format": "point",
        "title_en": "Tomorrow's weather",
        "audio": "audio/listening/n5.listen.022.mp3",
        "script_ja": "女: あしたの 天気は どうですか。\n男: あしたは 雨です。 でも、あさっては 天気が いいです。\n女: そうですか。",
        "prompt_ja": "あしたの 天気は どうですか。",
        "choices": ["天気が いい", "雨", "ゆき", "つめたい"],
        "correctAnswer": "雨",
        "explanation_en": "Tomorrow is rainy. Day-after-tomorrow is nice but the question is about tomorrow.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.023",
        "format": "point",
        "title_en": "Which days for homework",
        "audio": "audio/listening/n5.listen.023.mp3",
        "script_ja": "男: しゅくだいは いつですか。\n女: 火よう日と 木よう日です。\n男: 水よう日は ありませんか。\n女: ありません。",
        "prompt_ja": "しゅくだいは 何よう日に ありますか。",
        "choices": ["月よう日と 水よう日", "火よう日と 木よう日", "水よう日と 金よう日", "月よう日と 金よう日"],
        "correctAnswer": "火よう日と 木よう日",
        "explanation_en": "The woman explicitly says Tuesday and Thursday, and confirms there is none on Wednesday.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.024",
        "format": "point",
        "title_en": "Who is coming today",
        "audio": "audio/listening/n5.listen.024.mp3",
        "script_ja": "母: 今日は だれが 来ますか。\n子: 父の 先生と、母の 友だちが 来ます。 父も 6時に 来ます。\n母: わかりました。",
        "prompt_ja": "今日は だれが 来ますか。",
        "choices": ["父・母・先生", "父の 先生・母・先生", "父の 先生・母の 友だち・父", "先生と 友だちだけ"],
        "correctAnswer": "父の 先生・母の 友だち・父",
        "explanation_en": "Three people: father's teacher, mother's friend, and father himself. The mother is asking, not coming.",
        "voice": VOICE,
    },

    # UTTERANCE FORMAT (6 items) - what to say in a situation
    {
        "id": "n5.listen.025",
        "format": "utterance",
        "title_en": "Greeting the teacher in the morning",
        "audio": "audio/listening/n5.listen.025.mp3",
        "script_ja": "あさ 学校で 先生に 会いました。",
        "prompt_ja": "あさ 学校で 先生に 会いました。何と 言いますか。",
        "choices": ["おはよう ございます", "おやすみ なさい", "こんばんは", "さようなら"],
        "correctAnswer": "おはよう ございます",
        "explanation_en": "Polite morning greeting. おやすみなさい is bedtime; こんばんは is evening; さようなら is goodbye.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.026",
        "format": "utterance",
        "title_en": "Asking for coffee at a shop",
        "audio": "audio/listening/n5.listen.026.mp3",
        "script_ja": "店で コーヒーを 買いたいです。",
        "prompt_ja": "店で コーヒーを 買いたいです。何と 言いますか。",
        "choices": ["コーヒーを ください", "コーヒーを 食べます", "コーヒーは どこですか", "コーヒーが すきです"],
        "correctAnswer": "コーヒーを ください",
        "explanation_en": "〜を ください is the polite request when ordering. The other options eat coffee, ask location, or state preference.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.027",
        "format": "utterance",
        "title_en": "Politely declining a drink",
        "audio": "audio/listening/n5.listen.027.mp3",
        "script_ja": "友だちが おちゃを すすめました。 飲みたく ないです。",
        "prompt_ja": "友だちが おちゃを すすめました。 飲みたく ないです。何と 言いますか。",
        "choices": ["ありがとう ございます", "すみません", "いいえ、けっこうです", "おねがいします"],
        "correctAnswer": "いいえ、けっこうです",
        "explanation_en": "いいえ、けっこうです is the standard polite refusal of an offer.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.028",
        "format": "utterance",
        "title_en": "Entering a friend's home",
        "audio": "audio/listening/n5.listen.028.mp3",
        "script_ja": "友だちの いえへ 入ります。",
        "prompt_ja": "友だちの いえへ 入ります。何と 言いますか。",
        "choices": ["ただいま", "いただきます", "しつれいします", "どうも ありがとう"],
        "correctAnswer": "しつれいします",
        "explanation_en": "しつれいします is said when entering someone else's home. ただいま is for your own home.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.029",
        "format": "utterance",
        "title_en": "Before eating",
        "audio": "audio/listening/n5.listen.029.mp3",
        "script_ja": "ごはんを 食べる 前です。",
        "prompt_ja": "ごはんを 食べる 前です。何と 言いますか。",
        "choices": ["ごちそうさま", "いただきます", "しつれいします", "すみません"],
        "correctAnswer": "いただきます",
        "explanation_en": "いただきます is said before eating. ごちそうさま is after the meal.",
        "voice": VOICE,
    },
    {
        "id": "n5.listen.030",
        "format": "utterance",
        "title_en": "Asking the way",
        "audio": "audio/listening/n5.listen.030.mp3",
        "script_ja": "駅へ 行きたいです。 道が わかりません。",
        "prompt_ja": "駅へ 行きたいです。 道が わかりません。 しらない 人に 何と 聞きますか。",
        "choices": ["駅は どこですか", "駅は 何時ですか", "駅は いくらですか", "駅へ 行って ください"],
        "correctAnswer": "駅は どこですか",
        "explanation_en": "どこですか asks for location. The other options ask time, price, or command the listener to go.",
        "voice": VOICE,
    },
]


def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    existing_ids = {it["id"] for it in data["items"]}
    new_count = 0
    skipped = 0
    for item in NEW_ITEMS:
        if item["id"] in existing_ids:
            skipped += 1
            continue
        data["items"].append(item)
        new_count += 1
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"added {new_count} new items; skipped {skipped}; total now {len(data['items'])}")
    return 0


if __name__ == "__main__":
    main()
