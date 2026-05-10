"""Chokai Batch B (2026-05-10):
- L1: deeper aizuchi-tagging scan (was 7/50, target ~20)
- L2: deeper filler-tagging scan (was 6/50, target ~15)
- L3: pitch minimal-pair focus tag (NEW field, on items featuring pitch-distinct words)
- L5: phonological_target tag for sokuon / long-vowel discrimination items
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

# === L1: aizuchi rescan ===
print('=== L1: aizuchi-tagging deeper scan ===')
AIZUCHI_TOKENS = [
    'あー', 'ええ', 'うん', 'はい', 'へえ', 'へぇ', 'あら', 'おお',
    'そうです', 'そうですね', 'そうそう', 'なるほど', 'なるほどね', 'さあ',
    'ふーん', 'ほー', 'ほう', 'いいえ', 'うんうん',
]
aiz_added = 0
for item in items:
    script = item.get('script_ja') or item.get('script') or item.get('ja') or ''
    found = []
    for t in AIZUCHI_TOKENS:
        if t in script:
            found.append(t)
    if found and not item.get('aizuchi_present'):
        item['aizuchi_present'] = True
        item['aizuchi_tokens'] = found
        item['aizuchi_present_provenance'] = 'auto_derived'
        aiz_added += 1
    elif found and item.get('aizuchi_present') and not item.get('aizuchi_tokens'):
        item['aizuchi_tokens'] = found

print(f'  Newly tagged: {aiz_added}')


# === L2: filler rescan ===
print()
print('=== L2: filler-tagging deeper scan ===')
FILLER_TOKENS = [
    'えーと', 'えと', 'あの', 'あのう', 'んー', 'ええと', 'まあ', 'その',
    'ええ、', 'なんて', 'なんていうか', 'ちょっと', 'まーまー',
]
fil_added = 0
for item in items:
    script = item.get('script_ja') or item.get('script') or item.get('ja') or ''
    found = []
    for t in FILLER_TOKENS:
        if t in script:
            found.append(t)
    if found and not item.get('fillers_present'):
        item['fillers_present'] = True
        item['filler_tokens'] = found
        item['fillers_present_provenance'] = 'auto_derived'
        fil_added += 1
    elif found and item.get('fillers_present') and not item.get('filler_tokens'):
        item['filler_tokens'] = found

print(f'  Newly tagged: {fil_added}')


# === L3: pitch_minimal_pair_focus ===
# Scan scripts for words that have known pitch-distinct homographs.
print()
print('=== L3: pitch_minimal_pair_focus tagging ===')
# Pairs: word -> (meaning_a, pitch_a, meaning_b, pitch_b)
# pitch is mora,drop convention (drop=0 means heiban / no drop)
PITCH_PAIRS = {
    'はし': {
        'a': {'meaning': 'bridge', 'kanji': '橋', 'pitch': {'mora': 2, 'drop': 0}},  # heiban LH-H
        'b': {'meaning': 'chopsticks', 'kanji': '箸', 'pitch': {'mora': 2, 'drop': 1}},  # atamadaka HL-L
    },
    'あめ': {
        'a': {'meaning': 'rain', 'kanji': '雨', 'pitch': {'mora': 2, 'drop': 1}},  # HL
        'b': {'meaning': 'candy', 'kanji': '飴', 'pitch': {'mora': 2, 'drop': 0}},  # LH
    },
    'かみ': {
        'a': {'meaning': 'paper', 'kanji': '紙', 'pitch': {'mora': 2, 'drop': 0}},  # heiban
        'b': {'meaning': 'god / spirit', 'kanji': '神', 'pitch': {'mora': 2, 'drop': 1}},  # atamadaka
    },
    'にほん': {
        'a': {'meaning': 'Japan', 'kanji': '日本', 'pitch': {'mora': 3, 'drop': 0}},  # LH-L heiban variant
        'b': {'meaning': 'two long objects', 'kanji': '二本', 'pitch': {'mora': 3, 'drop': 1}},  # nakadaka
    },
    'いま': {
        'a': {'meaning': 'now', 'kanji': '今', 'pitch': {'mora': 2, 'drop': 1}},
        'b': {'meaning': 'living room', 'kanji': '居間', 'pitch': {'mora': 2, 'drop': 0}},
    },
}

pitch_tagged = 0
for item in items:
    script = item.get('script_ja') or item.get('script') or item.get('ja') or ''
    pairs_found = []
    for w, pair in PITCH_PAIRS.items():
        if w in script:
            pairs_found.append({
                'surface': w,
                'pair': pair,
                'note': f"{w}: pitch distinguishes {pair['a']['meaning']} ({pair['a']['kanji']}) from {pair['b']['meaning']} ({pair['b']['kanji']}).",
            })
    if pairs_found:
        item['pitch_minimal_pair_focus'] = pairs_found
        item['pitch_minimal_pair_focus_provenance'] = 'auto_derived'
        pitch_tagged += 1

print(f'  Items with pitch minimal-pair words: {pitch_tagged}')


# === L5: phonological_target — sokuon / long-vowel ===
print()
print('=== L5: phonological_target tagging ===')
# Detect specific forms in scripts
SOKUON_FORMS = {
    'きって': 'sokuon: きって (stamp) vs きて (come) — small っ doubles next consonant',
    'いっぱい': 'sokuon: いっぱい (one cup) vs いぱい (no word) — small っ doubles ぱ',
    'がっこう': 'sokuon: がっこう (school) — small っ before voiceless k',
    'ちょっと': 'sokuon: ちょっと (a little) — small っ before t',
    'ざっし': 'sokuon: ざっし (magazine) — small っ before s',
    'けっこん': 'sokuon: けっこん (marriage) — small っ before k',
}
LONG_VOWEL_FORMS = {
    'ビール': 'long vowel: ビール (3 mora, beer) vs ビル (2 mora, building) — — extends vowel',
    'おばあさん': 'long vowel: おばあさん (grandma) vs おばさん (aunt) — あ extends ば',
    'おじいさん': 'long vowel: おじいさん (grandpa) vs おじさん (uncle) — い extends じ',
    'こうこう': 'long vowel: こうこう (high school) vs ここ (here) — う extends each こ',
    'とおり': 'long vowel: とおり (street) vs とり (bird) — お extends と',
    'ゆうびん': 'long vowel: ゆうびん (mail) — う extends ゆ',
    'おとうさん': 'long vowel: おとうさん (father) — う extends と',
    'おかあさん': 'long vowel: おかあさん (mother) — あ extends か',
    'がっこう': 'long vowel + sokuon: がっこう (school) — both phenomena',
}

ph_tagged = 0
for item in items:
    script = item.get('script_ja') or item.get('script') or item.get('ja') or ''
    targets = []
    for w, note in SOKUON_FORMS.items():
        if w in script:
            targets.append({'category': 'sokuon', 'surface': w, 'note': note})
    for w, note in LONG_VOWEL_FORMS.items():
        if w in script:
            targets.append({'category': 'long_vowel', 'surface': w, 'note': note})
    if targets:
        item['phonological_target'] = targets
        item['phonological_target_provenance'] = 'auto_derived'
        ph_tagged += 1

print(f'  Items with phonological-target words: {ph_tagged}')


# Save
listen_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final
total = len(items)
aiz = sum(1 for i in items if i.get('aizuchi_present'))
fil = sum(1 for i in items if i.get('fillers_present'))
mp = sum(1 for i in items if i.get('pitch_minimal_pair_focus'))
ph = sum(1 for i in items if i.get('phonological_target'))
print()
print('=== FINAL ===')
print(f'  aizuchi_present:           {aiz}/{total}')
print(f'  fillers_present:           {fil}/{total}')
print(f'  pitch_minimal_pair_focus:  {mp}/{total}')
print(f'  phonological_target:       {ph}/{total}')
