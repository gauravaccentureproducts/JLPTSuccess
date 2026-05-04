"""Phase 1 of the example-coverage authoring pass (2026-05-03).

35 kanji entries in data/kanji.json have only one example word.
Add a second N5-scope example word to each. Constraints:
  - Each form must contain only target-kanji + kanji in the N5
    whitelist (JA-16 invariant). Non-N5 kanji is replaced with kana.
  - Each form must differ from the existing example.
  - Reading must be accurate; gloss must be a real translation.
  - All readings + glosses chosen to be common N5 vocabulary
    (numbers, daily verbs, body parts, basic compounds).

Idempotent: re-running after the migration is a no-op.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# Map: kanji glyph -> example to ADD as the second example.
# The form is shown to learners on the kanji detail page; non-N5 kanji
# in compounds are replaced with kana to satisfy JA-16.
ADDITIONS = {
    '百': {'form': '三百',     'reading': 'さんびゃく', 'gloss': 'three hundred'},
    '千': {'form': '千円',     'reading': 'せんえん',   'gloss': '1000 yen'},
    '円': {'form': '百円',     'reading': 'ひゃくえん', 'gloss': '100 yen'},
    '土': {'form': '土',       'reading': 'つち',       'gloss': 'soil, earth (kun)'},
    '半': {'form': '半分',     'reading': 'はんぶん',   'gloss': 'half'},
    '友': {'form': '友',       'reading': 'とも',       'gloss': 'friend (kun)'},
    '力': {'form': '力もち',   'reading': 'ちからもち', 'gloss': 'strong person'},
    '小': {'form': '小学校',   'reading': 'しょうがっこう', 'gloss': 'elementary school'},
    '上': {'form': '上手',     'reading': 'じょうず',   'gloss': 'skillful, good at'},
    '下': {'form': '下手',     'reading': 'へた',       'gloss': 'unskillful, bad at'},
    '左': {'form': '左手',     'reading': 'ひだりて',   'gloss': 'left hand'},
    '右': {'form': '右手',     'reading': 'みぎて',     'gloss': 'right hand'},
    '東': {'form': '東口',     'reading': 'ひがしぐち', 'gloss': 'east exit'},
    '西': {'form': '西口',     'reading': 'にしぐち',   'gloss': 'west exit'},
    '南': {'form': '南口',     'reading': 'みなみぐち', 'gloss': 'south exit'},
    '北': {'form': '北口',     'reading': 'きたぐち',   'gloss': 'north exit'},
    '間': {'form': '一時間',   'reading': 'いちじかん', 'gloss': 'one hour'},
    '山': {'form': '火山',     'reading': 'かざん',     'gloss': 'volcano'},
    '川': {'form': '小川',     'reading': 'おがわ',     'gloss': 'small stream / Ogawa (surname)'},
    '田': {'form': '田中',     'reading': 'たなか',     'gloss': 'Tanaka (surname)'},
    '雨': {'form': '大雨',     'reading': 'おおあめ',   'gloss': 'heavy rain'},
    '花': {'form': '花見',     'reading': 'はなみ',     'gloss': 'flower viewing (cherry blossom)'},
    '空': {'form': '空気',     'reading': 'くうき',     'gloss': 'air'},
    '食': {'form': '食べもの', 'reading': 'たべもの',   'gloss': 'food'},
    '飲': {'form': '飲みもの', 'reading': 'のみもの',   'gloss': 'drink, beverage'},
    '読': {'form': '読みかた', 'reading': 'よみかた',   'gloss': 'way of reading; reading (of a kanji)'},
    '書': {'form': '書きかた', 'reading': 'かきかた',   'gloss': 'way of writing'},
    '行': {'form': '行きかた', 'reading': 'いきかた',   'gloss': 'way of going / how to get there'},
    '立': {'form': '立ち上がる','reading': 'たちあがる', 'gloss': 'to stand up'},
    '休': {'form': '休み',     'reading': 'やすみ',     'gloss': 'holiday, rest, day off'},
    '言': {'form': '言いかた', 'reading': 'いいかた',   'gloss': 'way of saying, expression'},
    '買': {'form': '買いもの', 'reading': 'かいもの',   'gloss': 'shopping'},
    '安': {'form': '安く',     'reading': 'やすく',     'gloss': 'cheaply (adverb)'},
    '古': {'form': '古本',     'reading': 'ふるほん',   'gloss': 'second-hand book'},
    '長': {'form': '長さ',     'reading': 'ながさ',     'gloss': 'length'},
}


def main() -> int:
    kpath = ROOT / 'data' / 'kanji.json'
    data = json.loads(kpath.read_text(encoding='utf-8'))
    added: list[str] = []
    skipped: list[str] = []
    not_found = set(ADDITIONS.keys())
    for k in data['entries']:
        glyph = k.get('glyph')
        if glyph not in ADDITIONS:
            continue
        not_found.discard(glyph)
        new_ex = ADDITIONS[glyph]
        existing = k.get('examples') or []
        # Idempotency: skip if the new form already exists
        if any(e.get('form') == new_ex['form'] for e in existing):
            skipped.append(glyph)
            continue
        existing.append(new_ex)
        k['examples'] = existing
        added.append(glyph)
    if added:
        kpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Added 2nd example for {len(added)} kanji:')
    for g in added:
        print(f'  {g} -> {ADDITIONS[g]["form"]} ({ADDITIONS[g]["reading"]}) - {ADDITIONS[g]["gloss"]}')
    if skipped:
        print(f'Skipped (already had it): {skipped}')
    if not_found:
        print(f'WARNING - kanji not in data: {sorted(not_found)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
