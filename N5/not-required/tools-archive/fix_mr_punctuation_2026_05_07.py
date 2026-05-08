"""Fix the 'Mr।'/'Mrs।'/'Ms।' punctuation bug introduced by Phase 4d
substitution Mr. -> श्री combining with the Devanagari purna-virama
auto-conversion."""
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

count = 0
for pf in (ROOT / 'data' / 'papers').rglob('*.json'):
    if pf.name == 'manifest.json':
        continue
    pdata = json.loads(pf.read_text(encoding='utf-8'))
    changed = False
    for q in pdata.get('questions', []):
        rh = q.get('rationale_hi', '')
        if isinstance(rh, str):
            new = re.sub(r'श्री।\s+', r'श्री ', rh)
            new = re.sub(r'श्रीमती।\s+', r'श्रीमती ', new)
            new = re.sub(r'सुश्री।\s+', r'सुश्री ', new)
            if new != rh:
                q['rationale_hi'] = new
                changed = True
                count += 1
    if changed:
        pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n',
                      encoding='utf-8')

print(f'Fixed {count} Mr। / Mrs। / Ms। punctuation bugs')
