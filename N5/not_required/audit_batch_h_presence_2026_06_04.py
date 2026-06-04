"""Audit Batch H targets in the live corpus."""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('data/vocab.json', encoding='utf-8') as f:
    v = json.load(f)
entries = v['entries']

GROUPS = {
    'H1 — counter cleanup extended': [
        'べんきょう', '勉強', 'りょこう', '旅行', 'てんき', '天気',
        'いろ', '色', 'こと', 'もの', 'しごと', '仕事', 'りょうり', '料理',
    ],
    'H2 — legacy markers extended': [
        'レコード', 'フィルム', 'マッチ', 'はいざら', '灰皿',
    ],
    'H3 — verb pairs (transitivity)': [
        'あく', '開く', 'あける', '開ける',
        'しまる', '閉まる', 'しめる', '閉める',
        'おちる', '落ちる', 'おとす', '落とす',
        'でる', '出る', 'だす', '出す',
        'きえる', '消える', 'けす', '消す',
        'はじまる', '始まる', 'はじめる', '始める',
    ],
    'H4 — pronoun cautions': [
        'きみ', '君', '私', 'わたし', '私たち', 'わたしたち',
        'みんな', 'みなさん', 'みな', '皆さん',
    ],
}

for group, targets in GROUPS.items():
    print(f'\n=== {group} ===')
    for t in targets:
        m = [e for e in entries if e.get('form') == t]
        if m:
            for e in m:
                counter = e.get('counter')
                trans = e.get('transitivity')
                pair = e.get('pair_id')
                pf = bool(e.get('pragmatic_functions'))
                print(f'  ✓ {t} (id={e["id"][:55]}) counter={counter!r} trans={trans!r} pair_id={pair!r} pf={pf}')
        else:
            print(f'  ✗ {t} -- not in corpus')
