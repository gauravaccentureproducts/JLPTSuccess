"""ISSUE-013 (audit round-3): populate `additional_readings` (non-N5
on/kun-yomi) on every entry in data/kanji.json so the round-2 popover
disclosure (ISSUE-008 wiring in js/kanji-popover.js) renders meaningful
content for all 106 kanji rather than just 1.

Each entry gets:
  additional_readings: {
    on:  [...],   // on-yomi readings beyond what N5 teaches
    kun: [...],   // kun-yomi readings beyond what N5 teaches
  }

Coverage: this pass authors readings for every kanji from the
well-established Joyo / KanjiDic2-style readings catalogue. Entries
already carrying additional_readings keep their existing values
(idempotent). Empty arrays are valid and explicit - meaning "no
non-N5 reading worth surfacing" - and are distinct from a missing
field (which would imply "not yet authored").

Note: this is a one-shot authoring pass; future cycles can refine
specific entries based on user feedback or curriculum updates.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / 'data' / 'kanji.json'

# Hand-authored additional readings for each of the 106 N5 kanji.
# Format: glyph -> {'on': [...], 'kun': [...]}.
# Empty arrays are explicit: "no further reading taught at higher levels
# that's worth surfacing on the N5 popover".
#
# Source: Joyo kanji readings catalogue. Conservative - only common
# alternate readings are included; archaic / extremely rare readings
# are omitted to keep the popover useful for an N5 learner.
ADDITIONAL = {
    # Numerals
    '一': {'on': [],          'kun': []},
    '二': {'on': [],          'kun': []},
    '三': {'on': [],          'kun': []},
    '四': {'on': [],          'kun': []},
    '五': {'on': [],          'kun': []},
    '六': {'on': [],          'kun': []},
    '七': {'on': [],          'kun': []},
    '八': {'on': [],          'kun': []},
    '九': {'on': [],          'kun': []},
    '十': {'on': [],          'kun': []},
    '百': {'on': [],          'kun': ['もも']},
    '千': {'on': ['せん'],    'kun': []},
    '万': {'on': ['ばん'],    'kun': []},
    '円': {'on': [],          'kun': ['まる(い)']},
    # Days / time
    '日': {'on': [],          'kun': []},
    '月': {'on': [],          'kun': []},
    '火': {'on': [],          'kun': ['ほ']},
    '水': {'on': [],          'kun': []},
    '木': {'on': ['もく'],    'kun': ['こ']},
    '金': {'on': ['こん'],    'kun': []},
    '土': {'on': [],          'kun': []},
    '曜': {'on': [],          'kun': []},
    '年': {'on': [],          'kun': []},
    '時': {'on': [],          'kun': []},
    '分': {'on': ['ぶん',  'ぶ'], 'kun': ['わ(ける)', 'わ(かれる)', 'わ(かる)', 'わ(かつ)']},
    '半': {'on': [],          'kun': ['なか(ば)']},
    '今': {'on': ['きん'],    'kun': []},
    '何': {'on': ['か'],      'kun': []},
    '毎': {'on': [],          'kun': ['ごと(に)']},
    '週': {'on': [],          'kun': []},
    '午': {'on': [],          'kun': []},
    # People
    '人': {'on': ['ニン'],    'kun': []},
    '男': {'on': ['なん'],    'kun': []},
    '女': {'on': ['にょ',  'にょう'], 'kun': ['め']},
    '子': {'on': ['す'],      'kun': []},
    '友': {'on': [],          'kun': []},
    '父': {'on': [],          'kun': []},
    '母': {'on': [],          'kun': []},
    '先': {'on': [],          'kun': []},
    '生': {'on': ['しょう'],  'kun': ['い(きる)', 'い(かす)', 'い(ける)', 'う(まれる)', 'は(える)', 'き', 'なま']},
    '名': {'on': ['みょう'],  'kun': []},
    # Body parts
    '手': {'on': [],          'kun': ['た']},
    '足': {'on': ['そく'],    'kun': ['た(す)', 'た(りる)', 'た(る)']},
    '目': {'on': ['もく',  'ぼく'], 'kun': ['ま']},
    '口': {'on': ['く'],      'kun': []},
    '耳': {'on': ['じ'],      'kun': []},
    '力': {'on': ['りき'],    'kun': []},
    # Places / nature
    '山': {'on': [],          'kun': []},
    '川': {'on': ['せん'],    'kun': []},
    '田': {'on': ['でん'],    'kun': []},
    '空': {'on': [],          'kun': ['あ(く)', 'あ(ける)', 'から', 'むな(しい)']},
    '天': {'on': [],          'kun': ['あめ', 'あま']},
    '雨': {'on': ['う'],      'kun': ['あま']},
    '気': {'on': [],          'kun': []},
    '電': {'on': [],          'kun': []},
    # Directions
    '上': {'on': ['しょう'],  'kun': ['あ(げる)', 'あ(がる)', 'のぼ(る)', 'のぼ(せる)', 'のぼ(す)', 'かみ']},
    '下': {'on': ['げ'],      'kun': ['くだ(る)', 'くだ(さる)', 'くだ(さい)', 'お(りる)', 'お(ろす)', 'さ(げる)', 'さ(がる)', 'もと']},
    '左': {'on': ['さ'],      'kun': []},
    '右': {'on': ['ゆう'],    'kun': []},
    '中': {'on': ['じゅう'],  'kun': []},
    '外': {'on': ['げ'],      'kun': ['ほか', 'はず(す)', 'はず(れる)']},
    '前': {'on': [],          'kun': []},
    '後': {'on': ['こう'],    'kun': ['のち', 'うし(ろ)', 'おく(れる)']},
    '東': {'on': [],          'kun': []},
    '西': {'on': ['さい'],    'kun': []},
    '南': {'on': ['な'],      'kun': []},
    '北': {'on': [],          'kun': ['そむ(く)', 'にげる']},
    # School / objects
    '学': {'on': [],          'kun': ['まな(ぶ)']},
    '校': {'on': [],          'kun': []},
    '本': {'on': [],          'kun': ['もと']},
    '会': {'on': ['え'],      'kun': []},
    '社': {'on': ['じゃ'],    'kun': ['やしろ']},
    '員': {'on': [],          'kun': []},
    '駅': {'on': [],          'kun': []},
    '店': {'on': [],          'kun': ['たな']},
    '車': {'on': [],          'kun': []},
    '道': {'on': ['とう'],    'kun': []},
    '国': {'on': [],          'kun': []},
    '入': {'on': ['じゅ'],    'kun': ['い(る)', 'い(れる)', 'はい(る)']},
    '出': {'on': ['すい'],    'kun': ['だ(す)', 'で(る)']},
    '行': {'on': ['ぎょう',  'あん'], 'kun': ['ゆ(く)', 'おこな(う)']},
    '来': {'on': [],          'kun': ['きた(る)', 'きた(す)']},
    '見': {'on': [],          'kun': ['み(える)', 'み(せる)']},
    '聞': {'on': ['もん'],    'kun': ['き(こえる)']},
    '読': {'on': ['とう',  'とく'], 'kun': []},
    '書': {'on': [],          'kun': []},
    '話': {'on': [],          'kun': ['はなし']},
    '言': {'on': ['ごん'],    'kun': ['こと']},
    '食': {'on': ['じき'],    'kun': ['く(う)', 'く(らう)']},
    '飲': {'on': [],          'kun': []},
    '買': {'on': [],          'kun': []},
    '立': {'on': ['りゅう'],  'kun': ['た(てる)']},
    '休': {'on': [],          'kun': ['やす(まる)', 'やす(める)']},
    '長': {'on': [],          'kun': []},
    '高': {'on': [],          'kun': ['たか', 'たか(まる)', 'たか(める)']},
    '安': {'on': [],          'kun': []},
    '新': {'on': [],          'kun': ['あら(た)', 'にい']},
    '古': {'on': [],          'kun': ['ふる(す)']},
    '大': {'on': ['たい'],    'kun': ['おお(きい)', 'おお(いに)']},
    '小': {'on': [],          'kun': ['お', 'こ']},
    '多': {'on': [],          'kun': []},
    '少': {'on': [],          'kun': ['すこ(し)']},
    '白': {'on': ['びゃく'],  'kun': ['しら', 'しろ(い)']},
    '青': {'on': ['しょう'],  'kun': ['あお(い)']},
    '赤': {'on': ['しゃく'],  'kun': ['あか(い)', 'あか(らむ)', 'あか(らめる)']},
    '魚': {'on': ['ぎょ'],    'kun': ['うお']},
    '犬': {'on': ['けん'],    'kun': []},
    '花': {'on': [],          'kun': []},
    '茶': {'on': ['さ'],      'kun': []},
    '半': {'on': [],          'kun': ['なか(ば)']},
    '号': {'on': [],          'kun': []},
}


def main() -> int:
    data = json.loads(KANJI.read_text(encoding='utf-8'))
    added = 0
    populated = 0
    skipped = 0
    for e in data.get('entries', []):
        glyph = e.get('glyph')
        if not glyph:
            continue
        # Has existing additional_readings? Skip - keep curator's edits.
        if 'additional_readings' in e and e['additional_readings']:
            existing = e['additional_readings']
            if existing.get('on') or existing.get('kun'):
                skipped += 1
                continue
        ar = ADDITIONAL.get(glyph, {'on': [], 'kun': []})
        e['additional_readings'] = ar
        added += 1
        if ar['on'] or ar['kun']:
            populated += 1

    KANJI.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Added/refreshed additional_readings on {added} entries.')
    print(f'  populated (non-empty): {populated}')
    print(f'  empty scaffold:         {added - populated}')
    print(f'  skipped (already populated): {skipped}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
