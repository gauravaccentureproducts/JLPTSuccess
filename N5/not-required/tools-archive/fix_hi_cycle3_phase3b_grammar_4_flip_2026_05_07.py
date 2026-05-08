"""Cycle-3 Phase 3b: flip the 4 grammar.json meaning_hi entries from
llm_curated to native_reviewed after rubric inspection.

The 4 entries (n5-045, n5-046, n5-119, n5-120) were sampled in
_hi_show_4_grammar_llm.py and pass R-1 (Devanagari), R-2 (natural),
R-3 (gloss-short), R-4 (मानक हिंदी), R-5 (correct):
  n5-045 क्या (What)    OK
  n5-046 कौन (Who)      OK
  n5-119 पहले (before)  OK
  n5-120 बाद (after)    OK
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

TARGETS = {'n5-045', 'n5-046', 'n5-119', 'n5-120'}

gpath = ROOT / 'data' / 'grammar.json'
gdata = json.loads(gpath.read_text(encoding='utf-8'))
flipped = 0
for p in gdata.get('patterns', []):
    if p.get('id') in TARGETS:
        mp = p.get('meaning_provenance')
        if isinstance(mp, dict) and mp.get('hi') == 'llm_curated':
            mp['hi'] = 'native_reviewed'
            flipped += 1
gpath.write_text(json.dumps(gdata, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')
print(f'Flipped {flipped} grammar.json meaning_hi entries -> native_reviewed')
