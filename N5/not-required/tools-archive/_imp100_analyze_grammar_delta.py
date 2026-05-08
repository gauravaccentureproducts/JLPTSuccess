"""IMP-100 deep analysis: actually identify which 12 MD bullets don't
have a JSON pattern entry. Goes beyond the count-based check_coverage.py.

Approach:
1. Extract MD bullet lines (the same as check_coverage.py does).
2. For each MD bullet, extract the leading Japanese-token (the pattern
   form, before any " - " or " — " separator with English explanation).
3. Normalize tilde/whitespace variants.
4. For each JSON pattern, normalize its `pattern` field the same way
   plus all `meaning_ja` / `pattern_ja` if present.
5. Match each MD pattern to the closest JSON pattern.
6. Report MD patterns with no JSON match.
"""
from __future__ import annotations
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def normalize(s: str) -> str:
    """Normalize tilde + whitespace + NFKC for comparison."""
    if not isinstance(s, str):
        return ''
    s = unicodedata.normalize('NFKC', s)
    # Unify tilde variants
    s = s.replace('〜', '~').replace('～', '~').replace('—', '-').replace('–', '-')
    # Strip whitespace
    s = re.sub(r'\s+', '', s)
    return s.strip().lower()


def extract_pattern_form(md_bullet: str) -> str:
    """From an MD bullet like 'です - polite copula', return 'です'."""
    # Split on common explanation separators
    for sep in [' - ', ' — ', ' – ', ' (', ' = ', '\t']:
        if sep in md_bullet:
            return md_bullet.split(sep, 1)[0].strip()
    return md_bullet.strip()


def main():
    md_path = ROOT / 'KnowledgeBank' / 'grammar_n5.md'
    json_path = ROOT / 'data' / 'grammar.json'

    # ---- Extract MD bullets (mirror of check_coverage.py logic) ----
    text = md_path.read_text(encoding='utf-8')
    md_patterns = []  # list of (bullet_form, full_bullet, line_num)
    in_legend = False
    for ln, line in enumerate(text.splitlines(), 1):
        h2 = re.match(r'^##\s+(.+?)\s*$', line)
        if h2:
            in_legend = h2.group(1).strip().lower() == 'legend'
            continue
        if in_legend:
            continue
        m = re.match(r'^\s*-\s+(.+?)\s*$', line)
        if not m:
            continue
        body = m.group(1).strip()
        if not body or body.startswith('**'):
            continue
        if body.startswith('Example:') or body.startswith('Example '):
            continue
        form = extract_pattern_form(body)
        md_patterns.append((form, body, ln))

    print(f'MD bullets: {len(md_patterns)}')

    # ---- Extract JSON patterns (with all forms / aliases) ----
    grammar = json.loads(json_path.read_text(encoding='utf-8'))
    json_pats = grammar.get('patterns', [])
    print(f'JSON patterns: {len(json_pats)}')

    # Build a normalized index of JSON patterns
    json_index = {}  # normalized_form -> pattern_id
    for p in json_pats:
        for fld in ('pattern', 'meaning_ja', 'pattern_ja'):
            v = p.get(fld)
            if isinstance(v, str) and v.strip():
                norm = normalize(v)
                if norm and norm not in json_index:
                    json_index[norm] = p.get('id')
                # Also try splitting on common separators (e.g. "なん / なに")
                for piece in re.split(r'\s*[/／,、]\s*', v):
                    piece_norm = normalize(piece)
                    if piece_norm and piece_norm not in json_index:
                        json_index[piece_norm] = p.get('id')

    # ---- For each MD pattern, look it up ----
    # Build extra index: every Japanese token (kana/kanji span) inside any
    # JSON pattern's form, so MD sentence-templates like '～は～です' can
    # match the JSON 'です' entry by substring.
    JP_TOKEN_RE = re.compile(r'[ぁ-ゖァ-ヺ一-龯]+')
    json_token_index = {}  # token -> pattern_id
    for p in json_pats:
        for fld in ('pattern', 'meaning_ja', 'pattern_ja'):
            v = p.get(fld) or ''
            for tok in JP_TOKEN_RE.findall(v):
                tok_norm = normalize(tok)
                if tok_norm and tok_norm not in json_token_index:
                    json_token_index[tok_norm] = p.get('id')

    matched = []
    unmatched = []
    for form, full_bullet, ln in md_patterns:
        norm = normalize(form)
        if not norm:
            continue
        # 1. Exact match in normalized form index
        if norm in json_index:
            matched.append((form, json_index[norm], 'exact'))
            continue
        # 2. Try splitting on common alternation separators
        found = None
        for piece in re.split(r'\s*[/／,、]\s*', form):
            pn = normalize(piece)
            if pn in json_index:
                found = json_index[pn]
                break
        if found:
            matched.append((form, found, 'split'))
            continue
        # 3. Substring match: every Japanese token in MD form is in some
        #    JSON pattern. If the MD form has at least one Japanese token
        #    that exactly matches a JSON token-form, treat as matched.
        md_tokens = JP_TOKEN_RE.findall(form)
        substring_match = None
        for tok in md_tokens:
            tn = normalize(tok)
            if tn in json_token_index:
                substring_match = json_token_index[tn]
                break
        if substring_match:
            matched.append((form, substring_match, 'token'))
            continue
        # 4. Fuzzy: MD form is a substring of any JSON form, or vice versa
        for json_form, jid in json_index.items():
            if (norm and json_form and len(norm) >= 3
                and (norm in json_form or json_form in norm)):
                matched.append((form, jid, 'substring'))
                substring_match = jid
                break
        if not substring_match:
            unmatched.append((form, full_bullet, ln))

    print(f'\nMatched: {len(matched)} MD bullets -> JSON pattern')
    print(f'Unmatched: {len(unmatched)} MD bullets WITHOUT a JSON pattern')

    print(f'\n--- Unmatched (the "12 missing") ---')
    for form, full_bullet, ln in unmatched:
        print(f'\n  KB line {ln}:')
        print(f'    form: {form!r}')
        print(f'    full: {full_bullet[:160]}')

    # Also surface JSON patterns with no MD match (the inverse)
    print(f'\n--- JSON patterns with no MD match (sanity check) ---')
    md_norms = set(normalize(form) for form, _, _ in md_patterns)
    md_norms.update(normalize(piece)
                    for form, _, _ in md_patterns
                    for piece in re.split(r'\s*[/／,、]\s*', form))
    json_no_md = []
    for p in json_pats:
        v = p.get('pattern', '')
        if normalize(v) in md_norms:
            continue
        # Try aliases / split
        ok = False
        for fld in ('pattern', 'meaning_ja', 'pattern_ja'):
            val = p.get(fld) or ''
            for piece in re.split(r'\s*[/／,、]\s*', val):
                if normalize(piece) in md_norms:
                    ok = True
                    break
            if ok: break
        if not ok:
            json_no_md.append((p.get('id'), v))
    print(f'  Count: {len(json_no_md)}')
    for iid, pat in json_no_md[:8]:
        print(f'    {iid}: {pat[:80]}')


if __name__ == '__main__':
    main()
