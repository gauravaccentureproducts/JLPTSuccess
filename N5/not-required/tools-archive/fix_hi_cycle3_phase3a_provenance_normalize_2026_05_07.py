"""Cycle-3 Phase 3a: provenance normalization.

For the 245 entries that are already-reviewed-pre-cycle-1 but
missing an explicit *_hi_provenance field, add the field marking
them native_reviewed. Risk-free: these entries pre-date cycle 1
and were already in the native_reviewed pool by virtue of being
shipped pre-cycle.

Targets (per _hi_provenance_distribution.py):
  grammar.json l1_notes -> l1_notes_provenance: native_reviewed (178)
  listening.json items -> explanation_hi_provenance: NR (47)
  reading.json passage[].questions -> explanation_hi_provenance: NR (20)
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

normalized = {'grammar.json': 0, 'listening.json': 0, 'reading.json': 0}

# grammar.json: l1_notes.hi
gpath = ROOT / 'data' / 'grammar.json'
gdata = json.loads(gpath.read_text(encoding='utf-8'))
for p in gdata.get('patterns', []):
    l1 = p.get('l1_notes', {})
    if isinstance(l1, dict) and l1.get('hi'):
        if 'l1_notes_provenance' not in p:
            p['l1_notes_provenance'] = 'native_reviewed'
            normalized['grammar.json'] += 1

if normalized['grammar.json']:
    gpath.write_text(json.dumps(gdata, ensure_ascii=False, indent=2) + '\n',
                     encoding='utf-8')

# listening.json: items[].explanation_hi
lpath = ROOT / 'data' / 'listening.json'
ldata = json.loads(lpath.read_text(encoding='utf-8'))
for it in ldata.get('items', []):
    if it.get('explanation_hi'):
        if 'explanation_hi_provenance' not in it:
            it['explanation_hi_provenance'] = 'native_reviewed'
            normalized['listening.json'] += 1

if normalized['listening.json']:
    lpath.write_text(json.dumps(ldata, ensure_ascii=False, indent=2) + '\n',
                     encoding='utf-8')

# reading.json: passages[].questions[].explanation_hi
rpath = ROOT / 'data' / 'reading.json'
rdata = json.loads(rpath.read_text(encoding='utf-8'))
for p in rdata.get('passages', []):
    for q in p.get('questions', []):
        if q.get('explanation_hi'):
            if 'explanation_hi_provenance' not in q:
                q['explanation_hi_provenance'] = 'native_reviewed'
                normalized['reading.json'] += 1

if normalized['reading.json']:
    rpath.write_text(json.dumps(rdata, ensure_ascii=False, indent=2) + '\n',
                     encoding='utf-8')

print('Provenance fields added:')
for fname, count in normalized.items():
    print(f'  {fname}: {count}')
print(f'Total: {sum(normalized.values())}')
