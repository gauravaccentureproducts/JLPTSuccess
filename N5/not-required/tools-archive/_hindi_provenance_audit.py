"""HI-16: audit provenance vs content reality across Hindi fields.

Checks: is any *_hi field marked 'native_reviewed' yet contains text
that looks like a placeholder, low-quality machine translation, or
code-mix that wouldn't pass native review?
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PLACEHOLDER_RE = re.compile(
    r'अस्थायी|समीक्षा\s*(प्रतीक्षित|लंबित)|यह\s*विकल्प\s*यहाँ\s*अनुपयुक्त'
    r'|अंग्रे[ज़ज]ी\s*संस्करण|पूर्ण\s*Hindi\s*विवरण'
)
ALLOWED_LATIN = {'JLPT', 'N5', 'N4', 'N3', 'N2', 'N1', 'FSRS', 'SRS', 'UI', 'OK', 'RESET',
                 'L', 'M', 'S', 'XL', 'PWA', 'CSV', 'JSON', 'HTML', 'CSS', 'true', 'false'}
LATIN_WORD = re.compile(r'\b[a-zA-Z]{4,}\b')


def has_devanagari(s):
    return any('ऀ' <= ch <= 'ॿ' for ch in s)

def is_placeholder(s):
    return isinstance(s, str) and bool(PLACEHOLDER_RE.search(s))

def has_codemix(s):
    if not isinstance(s, str) or not has_devanagari(s):
        return False
    # Strip parens content (intentional teaching glosses)
    s2 = re.sub(r'\([^()]*\)', '', s)
    # Strip Japanese tokens
    s2 = re.sub(r'[ぁ-ゖァ-ヺ一-龯]+', '', s2)
    words = LATIN_WORD.findall(s2)
    bad = [w for w in words if w.upper() not in ALLOWED_LATIN]
    return len(bad) >= 2  # 2+ stray English words to flag


issues = defaultdict(list)


def check(value, provenance, label):
    if not isinstance(value, str):
        return
    if is_placeholder(value):
        issues['placeholder'].append((label, provenance, value[:80]))
    elif provenance == 'native_reviewed' and has_codemix(value):
        issues['codemix-but-native_reviewed'].append((label, provenance, value[:120]))


# Walk questions.json
qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
for q in qs.get('questions', []):
    qid = q.get('id', '?')
    eh = q.get('explanation_hi')
    eh_p = q.get('explanation_hi_provenance', '')
    if eh:
        check(eh, eh_p, f"{qid}.explanation_hi")
    de_hi = q.get('distractor_explanations_hi') or {}
    de_p = q.get('distractor_explanations_hi_provenance', '')
    if isinstance(de_hi, dict):
        for k, v in de_hi.items():
            check(v, de_p, f"{qid}.distractor[{k}]")

# Walk grammar.json
gram = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
for p in gram.get('patterns', []):
    pid = p.get('id', '?')
    if p.get('explanation_hi'):
        check(p['explanation_hi'], p.get('explanation_provenance', ''), f"{pid}.explanation_hi")
    if p.get('meaning_hi'):
        check(p['meaning_hi'], p.get('meaning_provenance', ''), f"{pid}.meaning_hi")
    l1n = p.get('l1_notes', {})
    if isinstance(l1n, dict) and l1n.get('hi'):
        check(l1n['hi'], 'native_reviewed', f"{pid}.l1_notes.hi")  # default to NR

# Walk reading.json
read = json.loads((ROOT / 'data' / 'reading.json').read_text(encoding='utf-8'))
for pas in read.get('passages', []):
    pid = pas.get('id', '?')
    if pas.get('summary_hi'):
        check(pas['summary_hi'], pas.get('summary_hi_provenance', ''), f"{pid}.summary_hi")

# Walk listening.json
listen = json.loads((ROOT / 'data' / 'listening.json').read_text(encoding='utf-8'))
for it in listen.get('items', []):
    iid = it.get('id', '?')
    if it.get('explanation_hi'):
        check(it['explanation_hi'], it.get('explanation_hi_provenance', ''), f"{iid}.explanation_hi")

print('## Provenance honesty audit')
print(f'\nPlaceholder Hindi values still on disk: {len(issues["placeholder"])}')
for label, prov, sample in issues['placeholder'][:10]:
    print(f'  {label} (prov: {prov})')
    print(f'    {sample}')

print(f'\nValues marked native_reviewed but with code-mix (>=2 stray EN words): {len(issues["codemix-but-native_reviewed"])}')
for label, prov, sample in issues['codemix-but-native_reviewed'][:15]:
    print(f'  {label}')
    print(f'    {sample}')
