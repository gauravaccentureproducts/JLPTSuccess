"""Verify Batch G target entries exist."""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('data/vocab.json', encoding='utf-8') as f:
    v = json.load(f)
entries = v['entries']

TARGETS = {
    'G1 — student scope': ['学生', 'がくせい', 'せいと'],
    'G2 — police tone': ['けいかん', '警官', 'おまわりさん'],
    'G3 — foreigner caution': ['がいこくじん', '外国人'],
    'G4 — date readings': ['一日', 'ついたち', 'いちにち'],
    'G5 — tonight': ['こんや', '今夜', 'こんばん', '今晩'],
    'G6 — part-time': ['アルバイト'],
    'G7 — full/a lot': ['いっぱい'],
    'G8 — just/only': ['ただ'],
    'G9 — only+neg': ['しか'],
    'G10 — gurai/kurai': ['ぐらい', 'くらい'],
    'G11 — yahari': ['やはり', 'やっぱり'],
    'G12 — word/vocab': ['ことば', 'たんご'],
    'G13 — what-means': ['何で', 'なんで'],
    'G14 — want (adj)': ['ほしい'],
    'G15 — gozaru': ['ござる'],
    'G16 — early/fast': ['はやい'],
    'G17 — easy/kind': ['やさしい'],
    'G18 — toilet polite': ['おてあらい', 'トイレ'],
    'G19 — bath/shower': ['おふろ', 'シャワー'],
    'G20 — body dual': ['せ', '足', 'あし'],
    'G21 — kanji/kana': ['じ', 'もじ', 'かんじ', 'かな', 'ひらがな', 'カタカナ'],
    'G22 — spicy': ['からい'],
    'G23 — toilet exclamation': ['いっぱい', 'たくさん', 'ちょっと', 'すこし'],
    'G24 — color noun vs adj': ['白', '白い', 'くろ', 'くろい', 'あか', 'あかい', 'あお', 'あおい'],
    'G25 — old (not people)': ['ふるい'],
    'G26 — house policy': ['はブラシ'],
}
for group, forms in TARGETS.items():
    found = []
    missing = []
    for f in forms:
        m = [e for e in entries if e.get('form') == f]
        if m:
            for e in m:
                found.append(f"{f} (id={e['id'][:55]}, has_pragmatic={bool(e.get('pragmatic_functions'))})")
        else:
            missing.append(f)
    print(f'{group}')
    for s in found:
        print(f'  ✓ {s}')
    if missing:
        print(f'  ✗ MISSING: {missing}')
