"""Dokkai Batch B-2 (2026-05-10): substitute OOS kanji in cultural_callout
fields after batch B authored them with non-N5 kanji.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Substitutions (compounds first, longest-first)
SUBS = [
    ('先輩/後輩', 'senpai (せんぱい) / kouhai (こうはい)'),
    ('お辞儀', 'ojigi (おじぎ)'),
    ('靴を脱ぐ', 'kutsu wo nugu (くつを ぬぐ)'),
    ('本音/建前', 'honne (ほんね) / tatemae (たてまえ)'),
    ('季語', 'kigo (きご)'),
    # singles fallback
    ('輩', 'はい'),
    ('辞', 'じ'),
    ('儀', 'ぎ'),
    ('靴', 'くつ'),
    ('脱', 'ぬ'),
    ('音', 'ね'),
    ('建', 'た'),
    ('季', 'き'),
]

reading_path = ROOT / 'data' / 'reading.json'
data = json.loads(reading_path.read_text(encoding='utf-8'))

def sub(text):
    if not isinstance(text, str):
        return text
    for old, new in SUBS:
        if old in text:
            text = text.replace(old, new)
    return text

fields = 0
for p in data['passages']:
    cc = p.get('cultural_callout')
    if not cc:
        continue
    for entry in cc:
        for k in ('label_en', 'matched_trigger', 'note', 'tag'):
            v = entry.get(k)
            if isinstance(v, str):
                new_v = sub(v)
                if new_v != v:
                    entry[k] = new_v
                    fields += 1

print(f'Fields rewritten: {fields}')

# Verify
K = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
N5 = set()
for e in K.get('entries', []):
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    if g: N5.add(g)
def is_kanji(c): return 0x4E00 <= ord(c) <= 0x9FFF
remaining = {}
for p in data['passages']:
    cc = p.get('cultural_callout')
    if not cc: continue
    for entry in cc:
        for k in ('label_en','matched_trigger','note','tag'):
            v = entry.get(k,'')
            if not isinstance(v, str): continue
            for c in v:
                if is_kanji(c) and c not in N5:
                    remaining.setdefault(c, []).append(p['id'])
print(f'Remaining OOS: {len(remaining)}')
for c, sites in remaining.items():
    print(f'  {c}: {len(sites)} sites')

reading_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)
