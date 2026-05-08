"""Dump the 206 paper-rationale_hi entries still llm_curated."""
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
    file_label = pf.relative_to(ROOT).as_posix()
    for q in pdata.get('questions', []):
        if q.get('rationale_hi_provenance') == 'llm_curated':
            count += 1
            print(f'\n{file_label} {q.get("id")}')
            print(f'  EN: {q.get("rationale", "")[:160]}')
            print(f'  HI: {q.get("rationale_hi", "")[:200]}')

print(f'\nTotal llm_curated paper rationales: {count}')
