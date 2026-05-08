"""Convert dokkai/reading passage titles from English to N5-scope
Japanese, and remove the English-translation field so the runtime no
longer renders the "Show English translation" UI panel.

Per user request 2026-05-01: titles should be in Japanese, and the
N5 reading practice should not surface English translations of the
passage. Vocabulary in titles is restricted to N5-syllabus kanji
(catalog at KnowledgeBank/kanji_n5.md) plus kana.

Idempotent: re-running after the migration is a no-op.
"""
import json
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# English title -> Japanese title (N5-scope vocab + kana + N5 kanji only).
# Where the English title was already topical (Self-introduction, My family),
# the Japanese form mirrors the same topic; where the English title named
# a place (At the convenience store), Japanese uses で / へ markers natural
# to N5 learners.
TITLE_MAP: dict[str, str] = {
    "Self-introduction":              "じこしょうかい",
    "Daily routine":                  "まいにちの せいかつ",
    "Weekend plan":                   "しゅうまつの よてい",
    "At the convenience store":       "コンビニで",
    "My family":                      "わたしの かぞく",
    "Today's weather":                "きょうの てんき",
    "Library notice":                 "としょかんの おしらせ",
    "Going to school":                "学校へ",
    "My hobby":                       "わたしの しゅみ",
    "My classroom":                   "わたしの きょうしつ",
    "Lunch today":                    "きょうの ひるごはん",
    "At the bookstore":               "本やで",
    "Trip to Kyoto":                  "きょうとへの りょこう",
    "New clothes":                    "あたらしい ふく",
    "Spring":                         "はる",
    "I'm sick":                       "びょうきです",
    "Cafe menu":                      "カフェの メニュー",
    "Studying Japanese":              "日本語の べんきょう",
    "Last Sunday":                    "せんしゅうの 日よう日",
    "My teacher":                     "わたしの 先生",
    "Flight schedule":                "ひこうきの じかん",
    "Yesterday's evening":            "きのうの ばん",
    "Bus stop notice":                "バスていの おしらせ",
    "My friend":                      "わたしの 友だち",
    "Saturday morning":               "土よう日の あさ",
    "Buying fruit":                   "くだものを かいに",
    "A note from a friend":           "友だちからの メモ",
    "My room":                        "わたしの へや",
    "Summer":                         "なつ",
    "How to get to the post office":  "ゆうびんきょくへの 行きかた",
}


def main() -> int:
    rpath = ROOT / 'data' / 'reading.json'
    data = json.load(rpath.open(encoding='utf-8'))
    passages = data.get('passages', [])
    converted: list[str] = []
    skipped_already_ja: list[str] = []
    missing: list[str] = []
    removed_translation = 0
    new_passages = []
    for p in passages:
        # If already migrated (has title_ja, no title_en), still pass
        # through reorder/translation-removal logic
        title_en = p.get('title_en')
        title_ja = p.get('title_ja')
        if title_ja and not title_en:
            skipped_already_ja.append(title_ja)
            ja = title_ja
        elif title_en:
            ja = TITLE_MAP.get(title_en)
            if ja is None:
                missing.append(title_en)
                new_passages.append(p)
                continue
            converted.append(f'{title_en} -> {ja}')
        else:
            ja = None
        # Reorder: title_ja immediately after id+level+topic (where
        # title_en used to live), drop title_en + translation_en.
        rebuilt = {}
        for k, v in p.items():
            if k in ('title_en', 'title_ja', 'translation_en'):
                continue
            rebuilt[k] = v
            if k == 'topic' and ja is not None:
                rebuilt['title_ja'] = ja
        if 'translation_en' in p:
            removed_translation += 1
        new_passages.append(rebuilt)
    data['passages'] = new_passages

    if missing:
        print(f'ERROR: titles not in TITLE_MAP: {missing}', file=sys.stderr)
        return 1

    rpath.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(f'Converted titles: {len(converted)}')
    for c in converted:
        print(f'  {c}')
    print(f'Skipped (already JA): {len(skipped_already_ja)}')
    print(f'Removed translation_en: {removed_translation}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
