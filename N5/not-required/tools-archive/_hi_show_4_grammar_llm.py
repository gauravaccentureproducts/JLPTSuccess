"""Show the 4 grammar.json patterns whose meaning_hi is llm_curated."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

g = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
for p in g.get('patterns', []):
    mhp = p.get('meaning_hi_provenance')
    mp = p.get('meaning_provenance')
    is_llm = False
    if isinstance(mhp, str) and mhp == 'llm_curated':
        is_llm = True
    elif isinstance(mp, dict) and mp.get('hi') == 'llm_curated':
        is_llm = True
    elif isinstance(mp, str) and mp == 'llm_curated':
        is_llm = True
    if is_llm:
        print(f"--- {p.get('id')} ---")
        print(f"  pattern: {p.get('pattern')}")
        print(f"  meaning_en: {p.get('meaning_en', '')[:120]}")
        print(f"  meaning_hi: {p.get('meaning_hi', '')[:200]}")
