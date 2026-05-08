"""Scan questions.json for placeholder Hindi text (admits review-pending)."""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent

# Patterns that flag a Hindi value as placeholder (admits the review is incomplete)
PLACEHOLDER_PATTERNS = [
    re.compile(r'अस्थायी'),                                  # "temporary"
    re.compile(r'समीक्षा\s*(प्रतीक्षित|लंबित)'),              # "review pending"
    re.compile(r'मूल\s*समीक्षा'),                              # "original review (pending)"
    re.compile(r'अंग्रे[ज़ज]ी\s*संस्करण'),                     # "see English version"
    re.compile(r'विवरण\s*के\s*लिए.*पृष्ठ'),                    # "see related page for details"
    re.compile(r'यह\s*विकल्प\s*यहाँ\s*अनुपयुक्त\s*है'),       # generic "this distractor is inappropriate"
]

def is_placeholder(s: str) -> tuple[bool, list[str]]:
    if not isinstance(s, str):
        return (False, [])
    matched = [p.pattern for p in PLACEHOLDER_PATTERNS if p.search(s)]
    return (bool(matched), matched)

# Code-mixing detector: Devanagari text containing English letters as words (not just allowed tokens)
ALLOWED_LATIN = {'JLPT', 'N5', 'N4', 'N3', 'N2', 'N1', 'FSRS', 'SRS', 'UI', 'OK', 'RESET',
                 'L', 'M', 'S', 'XL', 'PWA', 'CSV', 'JSON', 'HTML', 'CSS'}
LATIN_WORD = re.compile(r'\b[a-z]{4,}\b', re.IGNORECASE)

def has_code_mix(s: str) -> tuple[bool, list[str]]:
    if not isinstance(s, str):
        return (False, [])
    # Must have Devanagari for it to be code-mix (not pure-Latin)
    has_dev = any('ऀ' <= ch <= 'ॿ' for ch in s)
    if not has_dev:
        return (False, [])
    words = LATIN_WORD.findall(s)
    bad = [w for w in words if w.upper() not in ALLOWED_LATIN]
    return (bool(bad), bad)

def scan_file(path: Path, fields: list[str], list_fields: list[str] = []):
    print(f'\n=== {path.relative_to(ROOT)} ===')
    data = json.loads(path.read_text(encoding='utf-8'))
    items = data.get('questions', data.get('items', data.get('entries', data.get('patterns', []))))
    placeholder_total = 0
    code_mix_total = 0
    code_mix_examples = []
    placeholder_ids = []
    for it in items:
        iid = it.get('id', '?')
        for f in fields:
            v = it.get(f)
            ph, _ = is_placeholder(v)
            cm, badwords = has_code_mix(v)
            if ph:
                placeholder_total += 1
                placeholder_ids.append((iid, f, str(v)[:80]))
            if cm:
                code_mix_total += 1
                if len(code_mix_examples) < 8:
                    code_mix_examples.append((iid, f, badwords[:5], str(v)[:120]))
        for lf in list_fields:
            v = it.get(lf, [])
            if isinstance(v, list):
                for i, elem in enumerate(v):
                    ph, _ = is_placeholder(elem)
                    cm, badwords = has_code_mix(elem)
                    if ph:
                        placeholder_total += 1
                        placeholder_ids.append((iid, f'{lf}[{i}]', str(elem)[:80]))
                    if cm:
                        code_mix_total += 1
                        if len(code_mix_examples) < 8:
                            code_mix_examples.append((iid, f'{lf}[{i}]', badwords[:5], str(elem)[:120]))
            elif isinstance(v, dict):
                for k, elem in v.items():
                    ph, _ = is_placeholder(elem)
                    cm, badwords = has_code_mix(elem)
                    if ph:
                        placeholder_total += 1
                        placeholder_ids.append((iid, f'{lf}[{k}]', str(elem)[:80]))
                    if cm:
                        code_mix_total += 1
                        if len(code_mix_examples) < 8:
                            code_mix_examples.append((iid, f'{lf}[{k}]', badwords[:5], str(elem)[:120]))
    print(f'  Placeholder (review-pending) Hindi values: {placeholder_total}')
    print(f'  Code-mixed (Devanagari + English words) values: {code_mix_total}')
    print(f'  First 5 placeholder examples:')
    for iid, f, sample in placeholder_ids[:5]:
        print(f'    {iid}.{f}: {sample}')
    print(f'  First 5 code-mix examples:')
    for iid, f, words, sample in code_mix_examples[:5]:
        print(f'    {iid}.{f} ({words}): {sample}')
    return placeholder_total, code_mix_total

print('## Placeholder + code-mix scan')
total_ph, total_cm = 0, 0
for path, fields, list_fields in [
    (ROOT / 'data' / 'questions.json', ['explanation_hi'], ['distractor_explanations_hi']),
    (ROOT / 'data' / 'grammar.json', ['meaning_hi', 'explanation_hi'], []),
    (ROOT / 'data' / 'listening.json', ['explanation_hi'], []),
    (ROOT / 'data' / 'reading.json', ['summary_hi'], []),
    (ROOT / 'data' / 'vocab.json', ['gloss_hi'], []),
    (ROOT / 'data' / 'kanji.json', [], ['meanings_hi']),
]:
    if path.exists():
        ph, cm = scan_file(path, fields, list_fields)
        total_ph += ph
        total_cm += cm

# Special: grammar.json l1_notes.hi (nested)
print('\n=== grammar.json l1_notes.hi (nested scan) ===')
gram = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
l1n_ph = 0
l1n_cm = 0
l1n_examples = []
for p in gram.get('patterns', []):
    l1n = p.get('l1_notes', {})
    if isinstance(l1n, dict) and l1n.get('hi'):
        ph, _ = is_placeholder(l1n['hi'])
        cm, badwords = has_code_mix(l1n['hi'])
        if ph: l1n_ph += 1
        if cm:
            l1n_cm += 1
            if len(l1n_examples) < 12:
                l1n_examples.append((p.get('id', '?'), badwords[:6], l1n['hi'][:140]))
print(f'  Placeholder l1_notes.hi: {l1n_ph}')
print(f'  Code-mixed l1_notes.hi: {l1n_cm}')
print(f'  First 12 code-mix examples:')
for iid, words, sample in l1n_examples:
    print(f'    {iid} ({words}): {sample}')

# Reading questions explanation_hi (nested)
print('\n=== reading.json passages[].questions[].explanation_hi (nested) ===')
read = json.loads((ROOT / 'data' / 'reading.json').read_text(encoding='utf-8'))
rq_ph = 0
rq_cm = 0
rq_total = 0
for pas in read.get('passages', []):
    for q in pas.get('questions', []):
        v = q.get('explanation_hi')
        if v:
            rq_total += 1
            ph, _ = is_placeholder(v)
            cm, badwords = has_code_mix(v)
            if ph: rq_ph += 1
            if cm: rq_cm += 1
print(f'  Total reading-question explanation_hi: {rq_total}')
print(f'  Placeholder: {rq_ph}')
print(f'  Code-mixed: {rq_cm}')

print(f'\n## Grand totals')
print(f'  Placeholder Hindi values: {total_ph + l1n_ph + rq_ph}')
print(f'  Code-mixed Hindi values:  {total_cm + l1n_cm + rq_cm}')

# Kanji list-arity check
print('\n## Kanji meaning-list arity mismatch')
kanji = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
mismatches = []
for e in kanji.get('entries', []):
    en = e.get('meanings') or []
    hi = e.get('meanings_hi') or []
    if isinstance(en, list) and isinstance(hi, list) and len(en) != len(hi):
        mismatches.append((e.get('id', '?'), len(en), len(hi), en, hi))
print(f'  Kanji entries with mismatched English/Hindi meaning-list lengths: {len(mismatches)}/{len(kanji.get("entries", []))}')
print(f'  First 10 examples:')
for iid, en_n, hi_n, en, hi in mismatches[:10]:
    print(f'    {iid}: {en_n} EN [{", ".join(en)}] vs {hi_n} HI [{", ".join(hi)}]')
