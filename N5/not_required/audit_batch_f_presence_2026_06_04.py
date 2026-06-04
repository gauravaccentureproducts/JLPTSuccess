"""Verify Batch F target entries exist in vocab.json before writing fixes.
Read-only.
"""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('data/vocab.json', encoding='utf-8') as f:
    v = json.load(f)
entries = v['entries']

TARGETS = {
    'F1 — legacy markers': ['きしゃ', 'じびき', 'せびろ'],
    'F2 — naku (cry, animals)': ['なく'],
    'F3 — pronouns': ['かのじょ', 'かれ', 'じぶん', 'あなた'],
    'F4 — sensei title': ['先生', 'せんせい'],
    'F5 — greetings': ['しつれいします', 'しつれいしました',
                       'さようなら', 'おかえりなさい',
                       'おかげさまで', 'ごちそうさまでした'],
    'F6a — sea / lake': ['うみ', 'みずうみ'],
    'F6b — house / home': ['いえ', 'うち'],
    'F6c — rice': ['ごはん', 'こめ'],
    'F6d — alcohol': ['おさけ', 'さけ'],
    'F6e — cup': ['カップ', 'コップ'],
    'F7 — na-adj predicates': ['すき', 'だいすき', 'きらい', 'だいきらい'],
    'F8 — kirei': ['きれい'],
}
for group, forms in TARGETS.items():
    print(f'  {group}')
    for f in forms:
        # match by form OR reading
        m = [e for e in entries if e.get('form') == f or e.get('reading') == f]
        for e in m:
            existing_pf = bool(e.get('pragmatic_functions'))
            print(f'    {f!r} (form={e.get("form")!r}, id={e["id"]}) '
                  f'gloss={(e.get("gloss") or "-")[:50]!r} '
                  f'pragmatic_functions={existing_pf}')
        if not m:
            print(f'    {f!r} -- NOT IN CORPUS')
