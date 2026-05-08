"""List the remaining English words in grammar.json l1_notes.hi after Phase E."""
from __future__ import annotations
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

ALLOWED_LATIN = {'JLPT', 'N5', 'N4', 'N3', 'N2', 'N1', 'FSRS', 'SRS', 'UI', 'OK', 'RESET',
                 'L', 'M', 'S', 'XL', 'PWA', 'CSV', 'JSON', 'HTML', 'CSS'}
LATIN_WORD = re.compile(r'\b[a-zA-Z]{4,}\b')

# Track if a Latin word is INSIDE parens (intentional teaching gloss)
PAREN_RE = re.compile(r'\([^()]*\)')

def has_devanagari(s: str) -> bool:
    return any('ऀ' <= ch <= 'ॿ' for ch in s)

word_counts = Counter()
in_paren_counts = Counter()
not_in_paren_counts = Counter()
samples = {}

gram = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
for p in gram.get('patterns', []):
    l1n = p.get('l1_notes')
    if isinstance(l1n, dict) and isinstance(l1n.get('hi'), str):
        v = l1n['hi']
        if not has_devanagari(v):
            continue
        # Find paren spans
        paren_spans = [(m.start(), m.end()) for m in PAREN_RE.finditer(v)]
        for m in LATIN_WORD.finditer(v):
            w = m.group(0)
            if w.upper() in ALLOWED_LATIN:
                continue
            in_paren = any(s <= m.start() and m.end() <= e for s, e in paren_spans)
            word_counts[w.lower()] += 1
            if in_paren:
                in_paren_counts[w.lower()] += 1
            else:
                not_in_paren_counts[w.lower()] += 1
                if w.lower() not in samples:
                    samples[w.lower()] = (p.get('id', '?'), v[:200])

# Same for explanation_hi
for p in gram.get('patterns', []):
    eh = p.get('explanation_hi')
    if isinstance(eh, str) and has_devanagari(eh):
        paren_spans = [(m.start(), m.end()) for m in PAREN_RE.finditer(eh)]
        for m in LATIN_WORD.finditer(eh):
            w = m.group(0)
            if w.upper() in ALLOWED_LATIN:
                continue
            in_paren = any(s <= m.start() and m.end() <= e for s, e in paren_spans)
            word_counts[w.lower()] += 1
            if in_paren:
                in_paren_counts[w.lower()] += 1
            else:
                not_in_paren_counts[w.lower()] += 1
                if w.lower() not in samples:
                    samples[w.lower()] = (p.get('id', '?') + '/expl', eh[:200])

print('Remaining English words by frequency (those NOT in parens):')
for w, c in not_in_paren_counts.most_common(50):
    in_p = in_paren_counts.get(w, 0)
    iid, sample = samples.get(w, ('?', ''))
    print(f'  {w:<25} not-in-paren={c:<4} in-paren={in_p:<4}')
    print(f'    e.g., {iid}: {sample}')

total_no_paren = sum(not_in_paren_counts.values())
print(f'\nTotal Latin-word occurrences NOT inside parens: {total_no_paren}')
print(f'Total Latin-word occurrences INSIDE parens (teaching glosses, OK): {sum(in_paren_counts.values())}')
