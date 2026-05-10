"""Chokai Batch B-3 (2026-05-10): rescan all listening item fields (not just
script_ja) for phonological_target and pitch_minimal_pair_focus surfaces.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

listen_path = ROOT / 'data' / 'listening.json'
data = json.loads(listen_path.read_text(encoding='utf-8'))
items = data['items']

# Excludes any field that would be re-derived (the new tag fields themselves)
EXCLUDE_FIELDS = {'pitch_minimal_pair_focus', 'phonological_target',
                  'pitch_minimal_pair_focus_provenance', 'phonological_target_provenance'}

def collect_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in EXCLUDE_FIELDS:
                yield from collect_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from collect_strings(v)

# Pitch pairs (excluding いま — too ambiguous)
PITCH_PAIRS = {
    'はし': {
        'a': {'meaning': 'bridge', 'kanji': '橋', 'pitch': {'mora': 2, 'drop': 0}},
        'b': {'meaning': 'chopsticks', 'kanji': '箸', 'pitch': {'mora': 2, 'drop': 1}},
    },
    'あめ': {
        'a': {'meaning': 'rain', 'kanji': '雨', 'pitch': {'mora': 2, 'drop': 1}},
        'b': {'meaning': 'candy', 'kanji': '飴 (ame, kana)', 'pitch': {'mora': 2, 'drop': 0}},
    },
    'かみ': {
        'a': {'meaning': 'paper', 'kanji': '紙', 'pitch': {'mora': 2, 'drop': 0}},
        'b': {'meaning': 'god / spirit', 'kanji': '神', 'pitch': {'mora': 2, 'drop': 1}},
    },
    'にほん': {
        'a': {'meaning': 'Japan', 'kanji': '日本', 'pitch': {'mora': 3, 'drop': 0}},
        'b': {'meaning': 'two long objects (counter)', 'kanji': '二本', 'pitch': {'mora': 3, 'drop': 1}},
    },
}

SOKUON_FORMS = {
    'きって': "sokuon: kitte (stamp) vs kite (come) — small tsu doubles next consonant",
    'いっぱい': "sokuon: ippai (one cup / full) — small tsu doubles p",
    'がっこう': "sokuon: gakkou (school) — small tsu before voiceless k",
    'ちょっと': "sokuon: chotto (a little) — small tsu before t",
    'ざっし': "sokuon: zasshi (magazine) — small tsu before s",
    'けっこん': "sokuon: kekkon (marriage) — small tsu before k",
}
LONG_VOWEL_FORMS = {
    'ビール': "long vowel: biiru (3 mora, beer) vs biru (2 mora, building)",
    'おばあ': "long vowel: obaasan (grandma) vs obasan (aunt) — extra a",
    'おじい': "long vowel: ojiisan (grandpa) vs ojisan (uncle) — extra i",
    'こうこう': "long vowel: koukou (high school) vs koko (here)",
    'とおり': "long vowel: toori (street) vs tori (bird)",
    'ゆうびん': "long vowel: yuubin (mail) — extra u",
    'おとうさん': "long vowel: otousan (father) — extra u",
    'おかあさん': "long vowel: okaasan (mother) — extra a",
}

pitch_added = 0
ph_added = 0
for item in items:
    text = ' '.join(collect_strings(item))
    # Pitch pairs
    pairs_found = []
    for w, pair in PITCH_PAIRS.items():
        if w in text:
            pairs_found.append({
                'surface': w,
                'pair': pair,
                'note': f"{w}: pitch distinguishes {pair['a']['meaning']} from {pair['b']['meaning']}.",
            })
    if pairs_found:
        item['pitch_minimal_pair_focus'] = pairs_found
        item['pitch_minimal_pair_focus_provenance'] = 'auto_derived'
        pitch_added += 1

    # Phonological target
    targets = []
    for w, note in SOKUON_FORMS.items():
        if w in text:
            targets.append({'category': 'sokuon', 'surface': w, 'note': note})
    for w, note in LONG_VOWEL_FORMS.items():
        if w in text:
            targets.append({'category': 'long_vowel', 'surface': w, 'note': note})
    if targets:
        item['phonological_target'] = targets
        item['phonological_target_provenance'] = 'auto_derived'
        ph_added += 1

print(f'pitch_minimal_pair_focus: {pitch_added}/50')
print(f'phonological_target:      {ph_added}/50')

# Verify no OOS kanji
K = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
N5 = set()
for e in K.get('entries', []):
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    if g: N5.add(g)
def is_kanji(c): return 0x4E00 <= ord(c) <= 0x9FFF
def walk(obj):
    if isinstance(obj, str):
        for c in obj:
            if is_kanji(c) and c not in N5:
                yield c
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)
oos = set()
for item in items:
    for f in ('pitch_minimal_pair_focus','phonological_target'):
        if item.get(f):
            for c in walk(item[f]):
                oos.add(c)
print(f'OOS check: {oos}')

listen_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)
