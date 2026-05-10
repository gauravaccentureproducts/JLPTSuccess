"""Chokai Batch B-2 (2026-05-10): substitute 居 (N4) with kana-only form
in pitch_minimal_pair_focus → pair → b → kanji field.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

listen_path = ROOT / 'data' / 'listening.json'
data = json.loads(listen_path.read_text(encoding='utf-8'))

fixed = 0
removed = 0
for item in data['items']:
    pmpf = item.get('pitch_minimal_pair_focus')
    if not pmpf:
        continue
    new_pmpf = []
    for entry in pmpf:
        # If pair has 居間, drop the entire いま entry (N4)
        if entry.get('surface') == 'いま':
            removed += 1
            continue
        # Otherwise substitute any 居 with kana
        if entry.get('note', '').find('居間') != -1:
            entry['note'] = entry['note'].replace('居間', 'ima (いま, kana-only N5 form)')
            fixed += 1
        new_pmpf.append(entry)
    if new_pmpf:
        item['pitch_minimal_pair_focus'] = new_pmpf
    else:
        del item['pitch_minimal_pair_focus']
        if 'pitch_minimal_pair_focus_provenance' in item:
            del item['pitch_minimal_pair_focus_provenance']

print(f'Entries dropped (いま/居間): {removed}')
print(f'Entries with substituted note: {fixed}')

# Verify
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
for item in data['items']:
    for field in ('pitch_minimal_pair_focus', 'phonological_target'):
        v = item.get(field)
        if v:
            for c in walk(v):
                oos.add(c)
print(f'Remaining OOS in batch B fields: {len(oos)}: {oos}')

listen_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final state
items = data['items']
mp = sum(1 for i in items if i.get('pitch_minimal_pair_focus'))
print(f'pitch_minimal_pair_focus (after cleanup): {mp}/{len(items)}')
