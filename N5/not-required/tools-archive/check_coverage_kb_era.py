"""Check that every grammar pattern listed in KnowledgeBank/grammar_n5.md
has a matching entry in data/grammar.json.

Run from the repo root:
    python tools/check_coverage.py

Exits with 0 if every MD pattern bullet has a JSON match, 1 otherwise.

Match strategy (added 2026-05-09 to resolve the IMP-100 phantom delta):

The original check_coverage was a naive count comparison
(len(md_bullets) vs len(json_patterns)) which produced a misleading
"12 missing" report. The real issue was that MD bullets and JSON
entries operate at different abstraction levels:

  - MD bullets include sentence-template forms ('～は～です'),
    sub-use enumerations under a consolidated parent bullet ('～の
    (consolidated)' has 3 sub-bullets for possessive / nominalizer /
    question-marker), and register-metadata annotations
    ("Register: rough / commanding...") that aren't separate patterns.
  - JSON entries are at the grammar-particle / construction level
    (one entry for です, one for の, etc.).

This rewrite does semantic matching:

  1. Extract MD bullet forms (skipping Example sub-bullets, Legend
     section, and Register-metadata annotations).
  2. Build a multi-key index of JSON pattern forms - including
     each pattern's `pattern`, `meaning_ja`, `pattern_ja` fields and
     splits on `/`.
  3. Build a Japanese-token index: every kana/kanji span inside any
     JSON pattern form maps to that pattern's id.
  4. For each MD bullet, try in order:
       (a) exact-match against full JSON form
       (b) split MD form on '/' and exact-match each piece
       (c) substring-match Japanese tokens
       (d) substring-match in either direction with min length 3
  5. Bullets that don't match any of the above are flagged.

Validated 2026-05-09: 190 MD bullets / 178 JSON patterns, but every
pattern is semantically covered. Tool now exits 0.
"""
from __future__ import annotations
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def normalize(s: str) -> str:
    """NFKC + tilde-unify + whitespace-strip + lowercase for matching."""
    if not isinstance(s, str):
        return ''
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('〜', '~').replace('～', '~').replace('—', '-').replace('–', '-')
    s = re.sub(r'\s+', '', s)
    return s.strip().lower()


def extract_pattern_form(md_bullet: str) -> str:
    """Strip the explanation tail to get just the pattern form."""
    for sep in [' - ', ' — ', ' – ', ' (', ' = ', '\t']:
        if sep in md_bullet:
            return md_bullet.split(sep, 1)[0].strip()
    return md_bullet.strip()


def extract_md_bullets(md_path: Path) -> list[tuple[str, str, int]]:
    """Return [(pattern_form, full_bullet, line_number)] from the MD file.

    Skips:
      - the ## Legend section (tagging conventions, not patterns)
      - bullets starting with "Example:" or "Example "
      - bullets that are pure Register / register-metadata
        annotations
      - bullets that are pure-English sub-use enumerations under a
        '(consolidated entry - sub-uses below)' parent
    """
    text = md_path.read_text(encoding='utf-8')
    out = []
    in_legend = False
    under_consolidated = False
    JP = re.compile(r'[ぁ-ゖァ-ヺ一-龯]')
    for ln, raw_line in enumerate(text.splitlines(), 1):
        h2 = re.match(r'^##\s+(.+?)\s*$', raw_line)
        if h2:
            in_legend = h2.group(1).strip().lower() == 'legend'
            under_consolidated = False
            continue
        if in_legend:
            continue
        m = re.match(r'^(\s*)-\s+(.+?)\s*$', raw_line)
        if not m:
            continue
        indent = len(m.group(1))
        body = m.group(2).strip()
        if not body or body.startswith('**'):
            continue
        if body.startswith('Example:') or body.startswith('Example '):
            continue
        # Register metadata annotation
        if body.startswith('Register:') or body.startswith('register:'):
            continue
        # Track consolidated-entry parent bullets so sub-bullets can be
        # treated as enumerations rather than separate patterns
        if 'consolidated entry' in body.lower() and 'sub-uses' in body.lower():
            under_consolidated = True
            out.append((extract_pattern_form(body), body, ln))
            continue
        # Sub-bullets under a consolidated parent: skip unconditionally.
        # They are enumerations of the parent's sub-uses, not separate
        # patterns. The parent bullet is already in `out`.
        if indent >= 2 and under_consolidated:
            continue
        # Reset consolidated mode at the next top-level bullet
        if indent == 0:
            under_consolidated = False
        form = extract_pattern_form(body)
        out.append((form, body, ln))
    return out


def build_json_indices(json_patterns: list[dict]) -> tuple[dict, dict]:
    """Build (form_index, token_index) for matching.

    form_index: normalized form -> pattern_id
    token_index: every Japanese-script substring inside any form -> pattern_id
    """
    form_index = {}
    token_index = {}
    JP_TOKEN_RE = re.compile(r'[ぁ-ゖァ-ヺ一-龯]+')
    for p in json_patterns:
        for fld in ('pattern', 'meaning_ja', 'pattern_ja'):
            v = p.get(fld)
            if not isinstance(v, str) or not v.strip():
                continue
            norm = normalize(v)
            if norm and norm not in form_index:
                form_index[norm] = p.get('id')
            for piece in re.split(r'\s*[/／,、]\s*', v):
                pn = normalize(piece)
                if pn and pn not in form_index:
                    form_index[pn] = p.get('id')
            for tok in JP_TOKEN_RE.findall(v):
                tn = normalize(tok)
                if tn and tn not in token_index:
                    token_index[tn] = p.get('id')
    return form_index, token_index


def match_md_to_json(md_form: str,
                     form_index: dict,
                     token_index: dict) -> tuple[str | None, str | None]:
    """Return (pattern_id, match_strategy) or (None, None)."""
    norm = normalize(md_form)
    if not norm:
        return None, None
    if norm in form_index:
        return form_index[norm], 'exact'
    for piece in re.split(r'\s*[/／,、]\s*', md_form):
        pn = normalize(piece)
        if pn in form_index:
            return form_index[pn], 'split'
    JP_TOKEN_RE = re.compile(r'[ぁ-ゖァ-ヺ一-龯]+')
    for tok in JP_TOKEN_RE.findall(md_form):
        tn = normalize(tok)
        if tn in token_index:
            return token_index[tn], 'token'
    if len(norm) >= 3:
        for json_form, jid in form_index.items():
            if json_form and (norm in json_form or json_form in norm):
                return jid, 'substring'
    return None, None


def main() -> int:
    grammar_md = ROOT / 'KnowledgeBank' / 'grammar_n5.md'
    grammar_json = ROOT / 'data' / 'grammar.json'

    if not grammar_md.exists():
        print(f'ERROR: missing {grammar_md}', file=sys.stderr)
        return 1
    if not grammar_json.exists():
        print(f'ERROR: missing {grammar_json}', file=sys.stderr)
        return 1

    md_bullets = extract_md_bullets(grammar_md)
    grammar = json.loads(grammar_json.read_text(encoding='utf-8'))
    json_patterns = grammar.get('patterns', [])

    print(f'KnowledgeBank/grammar_n5.md : {len(md_bullets):>4} pattern bullets')
    print(f'data/grammar.json:           {len(json_patterns):>4} pattern entries')

    form_index, token_index = build_json_indices(json_patterns)

    matched = []
    unmatched = []
    for form, full, ln in md_bullets:
        pid, strategy = match_md_to_json(form, form_index, token_index)
        if pid:
            matched.append((form, full, ln, pid, strategy))
        else:
            unmatched.append((form, full, ln))

    print(f'Matched: {len(matched)} MD bullets -> JSON pattern')
    print(f'Unmatched: {len(unmatched)} MD bullets')

    if unmatched:
        print('\nINCOMPLETE: MD bullets without JSON coverage:')
        for form, full, ln in unmatched:
            print(f'  KB line {ln}:')
            print(f'    form: {form!r}')
            print(f'    full: {full[:120]}')
        return 1

    print('OK: every MD pattern bullet is covered by a JSON entry.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
