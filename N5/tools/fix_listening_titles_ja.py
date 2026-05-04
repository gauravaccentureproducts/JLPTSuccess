"""Convert listening item titles from English to N5-scope Japanese,
parallel to the dokkai migration of 2026-05-01.

Same rationale: the learner-facing surface should be in Japanese.
Vocabulary in titles is restricted to N5-syllabus kanji (catalog at
KnowledgeBank/kanji_n5.md, 111 entries) plus kana.

Idempotent: re-running after the migration is a no-op.
"""
import json
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# English title -> Japanese title (N5 kanji + kana only).
# Kanji used are all confirmed in kanji_n5.md catalog:
#   会 (240), 何 (150), 出 (420), 時 (117), 間 (313), 聞 (396),
#   買 (440), 本 (75), 行 (416), 来 (412), 先 (...), 生 (...),
#   日 (81), 食 (384), 入 (424), 友 (178), 店 (371).
TITLE_MAP: dict[str, str] = {
    # Format: task (situational dialogue, pick action/place/etc.)
    "Where to meet":                       "どこで 会いますか",
    "What to buy":                         "何を 買いますか",
    "What time to leave":                  "何時に 出ますか",
    "Choosing a drink":                    "のみものを えらぶ",
    # Format: point (information lookup)
    "Reason for being late":               "おくれた りゆう",
    "Where the book is":                   "本は どこですか",
    "Favorite season":                     "すきな きせつ",
    "What he wants for his birthday":      "たんじょうびに ほしい もの",
    # Format: utterance (politeness / greeting)
    "Asking for the time":                 "時間を 聞く",
    "Buying a ticket":                     "きっぷを 買う",
    "Refusing politely":                   "ていねいに ことわる",
    "Greeting in the morning":             "あさの あいさつ",
    # Pass-N additions
    "What time to meet":                   "何時に 会いますか",
    "Where to wait":                       "どこで まちますか",
    "What to buy at the shop":             "店で 何を 買いますか",
    "Going with whom":                     "だれと 行きますか",
    "When the teacher will arrive":        "先生は いつ 来ますか",
    "How to travel":                       "どうやって 行きますか",
    "Why no homework":                     "しゅくだいが ない りゆう",
    "How much was the book":               "本は いくらでしたか",
    "Library hours":                       "としょかんの 時間",
    "Tomorrow's weather":                  "あしたの てんき",
    "Which days for homework":             "しゅくだいは 何よう日",
    "Who is coming today":                 "きょう だれが 来ますか",
    "Greeting the teacher in the morning": "あさの 先生への あいさつ",
    "Asking for coffee at a shop":         "店で コーヒーを たのむ",
    "Politely declining a drink":          "のみものを ていねいに ことわる",
    "Entering a friend's home":            "友だちの いえに 入る",
    "Before eating":                       "食べる まえ",
    "Asking the way":                      "みちを 聞く",
}


def main() -> int:
    lpath = ROOT / 'data' / 'listening.json'
    data = json.load(lpath.open(encoding='utf-8'))
    items = data.get('items', [])
    converted: list[str] = []
    skipped_already_ja: list[str] = []
    missing: list[str] = []

    new_items = []
    for it in items:
        title_en = it.get('title_en')
        title_ja = it.get('title_ja')
        if title_ja and not title_en:
            skipped_already_ja.append(title_ja)
            ja = title_ja
        elif title_en:
            ja = TITLE_MAP.get(title_en)
            if ja is None:
                missing.append(title_en)
                new_items.append(it)
                continue
            converted.append(f'{title_en} -> {ja}')
        else:
            ja = None
        # Reorder: title_ja sits where title_en used to be (right after
        # `format`), drop title_en. (No translation_en in listening.json
        # by construction; explanation_en stays.)
        rebuilt = {}
        for k, v in it.items():
            if k in ('title_en', 'title_ja'):
                continue
            rebuilt[k] = v
            if k == 'format' and ja is not None:
                rebuilt['title_ja'] = ja
        new_items.append(rebuilt)
    data['items'] = new_items

    if missing:
        print(f'ERROR: titles not in TITLE_MAP: {missing}', file=sys.stderr)
        return 1

    lpath.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(f'Converted titles: {len(converted)}')
    for c in converted:
        print(f'  {c}')
    print(f'Skipped (already JA): {len(skipped_already_ja)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
