"""Cycle-2 Phase 0: list the most-frequent English words still
appearing in Hindi prose across questions.json + grammar.json +
paper files. Output drives the Phase-1 glossary expansion.
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ALLOWED_LATIN = {'JLPT', 'N5', 'N4', 'N3', 'N2', 'N1', 'FSRS', 'SRS', 'UI', 'OK',
                 'RESET', 'L', 'M', 'S', 'XL', 'PWA', 'CSV', 'JSON', 'HTML', 'CSS'}
LATIN_WORD = re.compile(r'\b[a-zA-Z]{3,}\b')
PAREN_RE = re.compile(r'\([^()]*\)')

def has_devanagari(s):
    return any('ऀ' <= ch <= 'ॿ' for ch in s)

word_count = Counter()
in_paren_count = Counter()
samples = {}

def scan_value(value, ctx):
    if not isinstance(value, str) or not has_devanagari(value):
        return
    paren_spans = [(m.start(), m.end()) for m in PAREN_RE.finditer(value)]
    for m in LATIN_WORD.finditer(value):
        w = m.group(0)
        if w.upper() in ALLOWED_LATIN:
            continue
        in_paren = any(s <= m.start() and m.end() <= e for s, e in paren_spans)
        word_count[w.lower()] += 1
        if in_paren:
            in_paren_count[w.lower()] += 1
        if w.lower() not in samples:
            samples[w.lower()] = (ctx, value[:140])

# Walk questions.json
qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
for q in qs.get('questions', []):
    qid = q.get('id', '?')
    scan_value(q.get('explanation_hi', ''), f'q.json {qid}.expl')
    de_hi = q.get('distractor_explanations_hi') or {}
    if isinstance(de_hi, dict):
        for k, v in de_hi.items():
            scan_value(v, f'q.json {qid}.dist[{k}]')

# Walk grammar.json
gram = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
for p in gram.get('patterns', []):
    pid = p.get('id', '?')
    scan_value(p.get('meaning_hi', ''), f'gram {pid}.meaning')
    scan_value(p.get('explanation_hi', ''), f'gram {pid}.expl')
    l1n = p.get('l1_notes') or {}
    if isinstance(l1n, dict):
        scan_value(l1n.get('hi', ''), f'gram {pid}.l1')

# Walk paper files
for pf in (ROOT / 'data' / 'papers').rglob('*.json'):
    if pf.name == 'manifest.json':
        continue
    pdata = json.loads(pf.read_text(encoding='utf-8'))
    for q in pdata.get('questions', []):
        scan_value(q.get('rationale_hi', ''), f'paper {pf.name} {q.get("id", "?")}')
    for p in pdata.get('passages', []):
        scan_value(p.get('summary_hi', ''), f'paper {pf.name} pas')

# Report
total = sum(word_count.values())
total_no_paren = total - sum(in_paren_count.values())
print(f'Total English-word occurrences in Hindi prose: {total}')
print(f'  Inside parens (intentional teaching glosses): {sum(in_paren_count.values())}')
print(f'  Outside parens (audit targets): {total_no_paren}')
print(f'\nTop 60 words (sorted by out-of-paren count):')
for w, c in word_count.most_common(60):
    out_paren = c - in_paren_count.get(w, 0)
    if out_paren == 0:
        continue
    ctx, sample = samples.get(w, ('?', ''))
    print(f"  {w:<20} {out_paren:>4}  e.g., {ctx}")
    print(f"    {sample}")
