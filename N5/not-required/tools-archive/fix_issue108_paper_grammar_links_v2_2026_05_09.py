"""ISSUE-108 v2: backfill grammarPatternId on paper questions by
matching the rationale text against grammar.json pattern fingerprints.

Approach:
  1. Build pattern fingerprints: each grammar pattern → set of search
     tokens (pattern field + meaning_en + meaning_ja + form_rules
     conjugation labels).
  2. For each paper question, score every pattern against the
     rationale + correctAnswer + choices.
  3. Take the best-scoring pattern if score ≥ threshold.
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


def japanese_tokens(text):
    """Return all Japanese-script tokens in text (kana/kanji spans)."""
    if not isinstance(text, str):
        return []
    return re.findall(r'[ぁ-ゖァ-ヺ一-龯]+', text)


def english_keywords(text):
    """Return all English content words ≥3 chars (lowercased)."""
    if not isinstance(text, str):
        return set()
    return {w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', text)}


# ============================================================================
# Build grammar.json fingerprints
# ============================================================================

gram = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
patterns = gram.get('patterns', [])

# pattern fingerprint: (id, ja_tokens, en_keywords, primary_form)
fingerprints = []
for p in patterns:
    pid = p.get('id')
    if not pid:
        continue
    ja_tokens = set()
    en_kw = set()

    for fld in ('pattern', 'meaning_ja', 'pattern_ja'):
        v = p.get(fld) or ''
        ja_tokens.update(japanese_tokens(v))

    for fld in ('meaning_en', 'explanation_en'):
        v = p.get(fld) or ''
        en_kw.update(english_keywords(v))

    # form_rules conjugations carry verb-form names
    fr = p.get('form_rules') or {}
    for c in fr.get('conjugations', []) or []:
        for fld in ('label', 'form', 'example'):
            v = c.get(fld) or ''
            ja_tokens.update(japanese_tokens(v))
            en_kw.update(english_keywords(v))

    fingerprints.append({
        'id': pid,
        'pattern': p.get('pattern', ''),
        'ja': ja_tokens,
        'en': en_kw,
    })


def best_match(rationale, choices, correct_answer):
    """Score every pattern; return best id + score, or (None, 0)."""
    rj = set(japanese_tokens(rationale or ''))
    re_kw = english_keywords(rationale or '')

    # Add correctAnswer Japanese tokens
    if correct_answer:
        rj.update(japanese_tokens(correct_answer))
    # Choices Japanese tokens
    for ch in choices or []:
        rj.update(japanese_tokens(ch))

    if not (rj or re_kw):
        return None, 0

    best = (None, 0)
    for fp in fingerprints:
        score = 0
        # Exact-match on pattern field is highest signal
        for t in fp['ja']:
            if t and len(t) <= 4 and t in rj:
                score += 5  # short patterns like は/が/を/に worth a lot
            elif t and len(t) > 4 and t in (rationale or ''):
                score += 3
        # English keyword overlap
        for kw in re_kw & fp['en']:
            score += 1
        # Bonus: pattern field exact-string match in rationale
        if fp['pattern'] and fp['pattern'] in (rationale or ''):
            score += 4

        if score > best[1]:
            best = (fp['id'], score)

    return best


# ============================================================================
# Walk paper files
# ============================================================================

paper_dir = ROOT / 'data' / 'papers'
total = 0
matched = 0
unmatched = 0
unmatched_samples = []
files_changed = 0

# Threshold: minimum score to commit a match
THRESHOLD = 5

for pf in paper_dir.rglob('*.json'):
    if pf.name == 'manifest.json':
        continue
    pdata = json.loads(pf.read_text(encoding='utf-8'))
    changed = False
    for q in pdata.get('questions', []):
        total += 1
        if q.get('grammarPatternId'):
            continue
        rationale = q.get('rationale', '')
        choices = q.get('choices', [])
        ca = q.get('correctAnswer')
        if ca is None:
            ci = q.get('correctIndex')
            if isinstance(ci, int) and choices and 0 <= ci < len(choices):
                ca = choices[ci]
        pid, score = best_match(rationale, choices, ca)
        if pid and score >= THRESHOLD:
            q['grammarPatternId'] = pid
            q['grammarPatternId_provenance'] = 'auto_inferred'
            matched += 1
            changed = True
        else:
            unmatched += 1
            if len(unmatched_samples) < 8:
                unmatched_samples.append({
                    'id': q.get('id'),
                    'rationale': rationale[:80],
                    'best': pid, 'score': score,
                })
    if changed:
        pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n',
                      encoding='utf-8')
        files_changed += 1

print(f'Total paper questions:    {total}')
print(f'Newly matched:            {matched}')
print(f'Unmatched:                {unmatched}')
print(f'Files modified:           {files_changed}')
print(f'\nFinal coverage: {matched}/{total} ({100*matched/max(1,total):.0f}%)')
print('\nUnmatched samples (low-score / no rationale):')
for s in unmatched_samples:
    print(f'  {s["id"]} (best={s["best"]}, score={s["score"]}): {s["rationale"]}')
