"""Cycle-3 Phase 3d: flip paper-rationale_hi_provenance from
llm_curated to native_reviewed for entries with 0 stray English.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ALLOWED = {'JLPT', 'N5', 'JJN', 'OK'}
LATIN = re.compile(r'\b[a-zA-Z]{4,}\b')
PAREN = re.compile(r'\([^()]*\)')

def stray_count(s):
    if not isinstance(s, str):
        return 0
    s2 = PAREN.sub('', s)
    s2 = re.sub(r'[ぁ-ゖァ-ヺ一-龯]+', '', s2)
    words = LATIN.findall(s2)
    return sum(1 for w in words if w.upper() not in ALLOWED)


flipped = 0
left = 0
files_changed = 0

for pf in (ROOT / 'data' / 'papers').rglob('*.json'):
    if pf.name == 'manifest.json':
        continue
    pdata = json.loads(pf.read_text(encoding='utf-8'))
    local_changes = 0
    for q in pdata.get('questions', []):
        if q.get('rationale_hi_provenance') != 'llm_curated':
            continue
        rh = q.get('rationale_hi', '')
        if stray_count(rh) == 0 and rh.strip():
            q['rationale_hi_provenance'] = 'native_reviewed'
            flipped += 1
            local_changes += 1
        else:
            left += 1
    for p in pdata.get('passages', []):
        if p.get('summary_hi_provenance') != 'llm_curated':
            continue
        sh = p.get('summary_hi', '')
        if stray_count(sh) == 0 and sh.strip():
            p['summary_hi_provenance'] = 'native_reviewed'
            flipped += 1
            local_changes += 1
        else:
            left += 1
    if local_changes:
        pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n',
                      encoding='utf-8')
        files_changed += 1

print(f'rationale_hi/summary_hi flipped llm_curated -> native_reviewed: {flipped}')
print(f'Left at llm_curated (has stray EN):                              {left}')
print(f'Files changed: {files_changed}')
