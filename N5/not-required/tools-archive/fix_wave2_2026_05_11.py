"""Wave 2: Visible content bugs from UI audit.

B1: Fix placeholder grammar pattern titles (4 entries say just "Verb" or
    "Adjective + Noun" instead of descriptive titles).
B2: Fill empty `form` field in kanji examples (34 rows across 10 kanji had
    kanji-form column blank in the rendered table).
B3: Normalize format_type for n5.listen.048-050 so they don't appear under
    a raw "dialogue" free-tag in the listening list.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============================================================
# B1: Fix placeholder grammar pattern titles
# ============================================================
print('=== B1: Fix placeholder pattern titles ===')
g_path = ROOT / 'data' / 'grammar.json'
G = json.loads(g_path.read_text(encoding='utf-8'))

TITLE_FIX = {
    # Each entry: pattern → meaningful descriptive title
    'n5-135': {'pattern': 'V-plain + N (relative clause)',
               'meaning_ja': '動詞ふつう形 ＋ N。「読む 本」のように 動詞が 名詞を しゅうしょくする ばあい。'},
    'n5-136': {'pattern': 'Adj + N (combined)',
               'meaning_ja': '形容詞（い／な）＋ 名詞。い-形容詞は そのまま、な-形容詞は 「な」を つけて 名詞に つける。'},
    'n5-162': {'pattern': 'V-plain + まえに',
               'meaning_ja': '動詞ふつう形（じしょけい）＋ まえに。「ねる まえに 本を よみます」。'},
    'n5-163': {'pattern': 'V-た + あとで',
               'meaning_ja': '動詞ふつう形 (過去) ＋ あとで。「ごはんを たべた あとで さんぽ します」。'},
}

fixed_b1 = 0
for p in G['patterns']:
    fix = TITLE_FIX.get(p.get('id'))
    if fix and p.get('pattern') in ('Verb', 'Adjective + Noun'):
        old = p.get('pattern')
        p['pattern'] = fix['pattern']
        if 'meaning_ja' in fix:
            p['meaning_ja'] = fix['meaning_ja']
        print(f'  {p["id"]}: "{old}" -> "{p["pattern"]}"')
        fixed_b1 += 1

g_path.write_text(json.dumps(G, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'B1 fixed: {fixed_b1}')

# ============================================================
# B2: Fill empty kanji example forms
# ============================================================
print()
print('=== B2: Fill empty kanji example forms ===')
k_path = ROOT / 'data' / 'kanji.json'
K = json.loads(k_path.read_text(encoding='utf-8'))
entries = K['entries']

# For each kanji, hand-curated fill for rows where form is empty.
# Reading-only entries derive their form from common N5 compounds.
FORM_FILL = {
    # Reading -> form mapping (per kanji). Keys are kanji glyph; values are
    # dict[reading -> form].
    '日': {
        'にちようび': '日曜日',
        'にほんじん': '日本人',
        'にほんご':   '日本語',
        'ついたち':   '一日',
        'なのか':     '七日',
        'みっか':     '三日',
        'ここのか':   '九日',
    },
    '月': {
        'いちがつ':   '一月',
        'にがつ':     '二月',
        'さんがつ':   '三月',
        'しがつ':     '四月',
        'ごがつ':     '五月',
    },
    '一': {
        'いちにち':   '一日',
        'ついたち':   '一日',
        'ひとつき':   '一月',
        'いっぽん':   '一本',
    },
    '十': {
        'じゅうがつ': '十月',
        'じっぷん':   '十分',
        'じゅっぷん': '十分',
        'とおか':     '十日',
    },
    '人': {
        'にほんじん': '日本人',
        'ひとり':     '一人',
        'ふたり':     '二人',
        'おとな':     '大人',
    },
    '二': {
        'にがつ':     '二月',
        'ふたり':     '二人',
        'ふつか':     '二日',
    },
    '曜': {
        'にちようび': '日曜日',
        'げつようび': '月曜日',
        'かようび':   '火曜日',
    },
    '国': {
        'にほんこく': '日本国',
        'がいこく':   '外国',
    },
    '週': {
        'こんしゅう': '今週',
    },
    '何': {
        'なんようび': '何曜日',
    },
}

fixed_b2 = 0
for e in entries:
    g = e.get('glyph') or e.get('id', '').split('.')[-1]
    fill_map = FORM_FILL.get(g)
    if not fill_map:
        continue
    for ex in e.get('examples') or []:
        if not ex.get('form'):
            r = ex.get('reading')
            if r in fill_map:
                ex['form'] = fill_map[r]
                fixed_b2 += 1

k_path.write_text(json.dumps(K, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'B2 filled: {fixed_b2}')

# ============================================================
# B3: Normalize listening format_type for n5.listen.048-050
# ============================================================
print()
print('=== B3: Normalize listening format_type ===')
l_path = ROOT / 'data' / 'listening.json'
L = json.loads(l_path.read_text(encoding='utf-8'))

# n5.listen.048 / 049 / 050 currently have format_type that falls through to
# raw "dialogue" tag. Map them to nearest canonical mondai. Looking at their
# content: aizuchi-rich dialogues — these are most naturally task_understanding
# (mondai 1) extensions. But they were authored to drill aizuchi/filler
# recognition, not task. Pragmatic fix: classify them as task_understanding
# (mondai 1) so they group cleanly; preserve their original format_type in a
# new field so the data isn't lost.

fixed_b3 = 0
for it in L['items']:
    if it['id'] in ('n5.listen.048', 'n5.listen.049', 'n5.listen.050'):
        orig_format_type = it.get('format_type')
        if orig_format_type and orig_format_type not in (
            'task_understanding', 'point_understanding',
            'speech_expression', 'immediate_response'):
            # Move original to format_type_original; set canonical
            it['format_type_original'] = orig_format_type
            it['format_type'] = 'task_understanding'
            # Ensure mondai is set
            if it.get('mondai') not in (1, 2, 3, 4):
                it['mondai'] = 1
            print(f'  {it["id"]}: format_type "{orig_format_type}" -> "task_understanding" (orig preserved in format_type_original)')
            fixed_b3 += 1

l_path.write_text(json.dumps(L, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'B3 fixed: {fixed_b3}')

print()
print('=== SUMMARY ===')
print(f'  B1 placeholder titles fixed: {fixed_b1}')
print(f'  B2 empty kanji example forms filled: {fixed_b2}')
print(f'  B3 listening format_type normalized: {fixed_b3}')
