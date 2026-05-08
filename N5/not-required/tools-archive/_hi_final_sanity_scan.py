"""Final sanity scan across all 100%-NR Hindi content. Looks for:
1. Stray English words in NR-marked text (residue from cycle 5)
2. Identical EN==HI passthroughs (no actual translation)
3. Suspiciously short Hindi (< 30% length of English)
4. Hindi values < 3 chars (probably truncated)
5. Repeated words bug ("रूप रूप", "है है")
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ALLOWED_LATIN = {'JLPT', 'N5', 'N4', 'N3', 'N2', 'N1', 'FSRS', 'SRS', 'UI', 'OK',
                 'RESET', 'L', 'M', 'S', 'XL', 'PWA', 'CSV', 'JSON', 'HTML', 'CSS',
                 'AM', 'PM', 'Cha', 'Shiro'}
LATIN_WORD = re.compile(r'\b[a-zA-Z]{4,}\b')
PAREN = re.compile(r'\([^()]*\)')

def has_devanagari(s):
    return any('ऀ' <= ch <= 'ॿ' for ch in s)

def stray_english(s):
    if not isinstance(s, str):
        return []
    s2 = PAREN.sub('', s)
    s2 = re.sub(r'[ぁ-ゖァ-ヺ一-龯]+', '', s2)
    return [w for w in LATIN_WORD.findall(s2) if w.upper() not in ALLOWED_LATIN]

def find_repeated(s):
    """Find consecutive identical words."""
    if not isinstance(s, str):
        return []
    words = s.split()
    return [words[i] for i in range(len(words) - 1) if words[i] == words[i + 1] and len(words[i]) > 1]

issues = defaultdict(list)


def check_pair(en, hi, where):
    if not isinstance(hi, str) or not has_devanagari(hi):
        return
    # 1. Stray English
    stray = stray_english(hi)
    if stray:
        issues['stray_english'].append((where, hi[:120], stray[:5]))
    # 2. Passthrough
    if isinstance(en, str) and en.strip() == hi.strip():
        issues['passthrough'].append((where, hi[:120], None))
    # 3. Short Hindi
    if isinstance(en, str) and len(en) > 50:
        ratio = len(hi) / len(en)
        if ratio < 0.3:
            issues['too_short'].append((where, f'EN={len(en)} HI={len(hi)} ratio={ratio:.2f}', None))
    # 4. Truncated
    if len(hi.strip()) < 3:
        issues['too_short_abs'].append((where, hi, None))
    # 5. Repeated words
    rep = find_repeated(hi)
    if rep:
        issues['repeated_words'].append((where, hi[:120], rep[:3]))


def walk(node, path, file_label, en_context=None):
    if isinstance(node, dict):
        en_text = (node.get('explanation_en') or node.get('meaning_en') or
                   node.get('rationale') or node.get('summary_en') or
                   node.get('explanation') or node.get('gloss') or '')
        for k, v in node.items():
            if isinstance(k, str) and k.endswith('_hi') and isinstance(v, str):
                check_pair(en_text, v, f'{file_label}::{path}.{k}')
            elif isinstance(k, str) and k == 'hi' and isinstance(v, str):
                # for nested l1_notes / etc — find sibling 'en'
                en_sib = node.get('en', '')
                check_pair(en_sib, v, f'{file_label}::{path}.{k}')
            walk(v, f'{path}.{k}' if path else k, file_label, en_text)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk(item, f'{path}[{i}]', file_label, en_context)

# Walk all surfaces
for fname in ['vocab.json', 'kanji.json', 'grammar.json', 'reading.json',
              'listening.json', 'questions.json']:
    p = ROOT / 'data' / fname
    if p.exists():
        walk(json.loads(p.read_text(encoding='utf-8')), '', fname)

papers_dir = ROOT / 'data' / 'papers'
if papers_dir.exists():
    for pf in papers_dir.rglob('*.json'):
        if pf.name == 'manifest.json':
            continue
        walk(json.loads(pf.read_text(encoding='utf-8')),
             '', f'papers/{pf.parent.name}/{pf.name}')

# locales/hi.json
hi_ui = json.loads((ROOT / 'locales' / 'hi.json').read_text(encoding='utf-8'))
en_ui = json.loads((ROOT / 'locales' / 'en.json').read_text(encoding='utf-8'))

def flatten(d, prefix=''):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(flatten(v, f'{prefix}.{k}' if prefix else k))
    else:
        out[prefix] = d
    return out

en_flat = flatten(en_ui)
hi_flat = flatten(hi_ui)
for k in hi_flat:
    if k.startswith('_meta'):
        continue
    en = en_flat.get(k, '')
    check_pair(en, hi_flat[k], f'locales/hi.json::{k}')

# Report
print('## Final sanity scan results')
print()
for category in ['stray_english', 'passthrough', 'too_short', 'too_short_abs', 'repeated_words']:
    cases = issues.get(category, [])
    print(f'{category}: {len(cases)} issues')
    for where, sample, extra in cases[:8]:
        print(f'  {where[:90]}')
        print(f'    sample: {sample}')
        if extra:
            print(f'    extra: {extra}')
    print()
