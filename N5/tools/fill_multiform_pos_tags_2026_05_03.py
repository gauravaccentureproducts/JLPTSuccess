"""Fill the 12 multi-form entries in vocabulary_n5.md with POS tags.

DEFER-5 closure (final 1.2%). The 1002/1014 entries already carry a
`[<tag>]` in JA-31's canonical position. The remaining 12 are
`form1 / form2[ / form3] - gloss` lines that JA-31's LINE_RE doesn't
match (form pattern stops at the first space). The fix is to insert
`[<tag>]` after the dash separator just like the rest, with the tag
sourced from the corresponding vocab.json entry.

JA-31 will silently skip these lines (no LINE_RE match) and that's
fine — the file format goal is reader-visible PoS, not 100% JA-31
matchability for multi-form variants.

Idempotent: re-running won't double-insert.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / 'KnowledgeBank' / 'vocabulary_n5.md'
JSON_PATH = ROOT / 'data' / 'vocab.json'

POS_ABBREV = {
    'noun': 'n.', 'verb-1': 'v1', 'verb-2': 'v2', 'verb-3': 'v3',
    'i-adj': 'i-adj', 'na-adj': 'na-adj', 'adverb': 'adv.',
    'particle': 'part.', 'conjunction': 'conj.', 'pronoun': 'pron.',
    'counter': 'count.', 'numeral': 'num.', 'demonstrative': 'dem.',
    'question-word': 'Q-word', 'expression': 'exp.',
    'interjection': 'interj.',
}

# Multi-form line pattern: `- form1 / form2 [/ form3] [(reading)] - gloss`
# Capture every Japanese token before the first ` - ` so we can look any of
# them up in vocab.json. The reading-in-parens may attach to ANY of the
# alternates, not just the first one.
MULTIFORM_LINE = re.compile(
    r'^(- )([^\-\n]+?)(\s+-\s+)((?!\[)[^\n]+)$'
)
TAG_PRESENT = re.compile(
    r'\[(n\.|v[123]|i-adj|na-adj|adv\.|part\.|conj\.|pron\.|count\.|num\.|dem\.|Q-word|exp\.|interj\.)\]'
)
SECTION_RE = re.compile(r'^##\s+\d+\.')
IS_JP = re.compile(r'[ぁ-んァ-ヶー一-鿿]')
SLASH_TOKEN_SPLIT = re.compile(r'\s*/\s*')


def build_vocab_index() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Return (by_form, by_reading) mapping form/reading → set of POS tags."""
    vocab = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    by_form: dict[str, set[str]] = {}
    by_reading: dict[str, set[str]] = {}
    for e in vocab.get('entries', []):
        form = e.get('form')
        reading = e.get('reading')
        pos = e.get('pos')
        if not (form and pos):
            continue
        tag = POS_ABBREV.get(pos, pos)
        by_form.setdefault(form, set()).add(tag)
        if reading:
            by_reading.setdefault(reading, set()).add(tag)
    return by_form, by_reading


def extract_form_tokens(form_cluster: str) -> list[str]:
    """Pull form-like tokens out of a slash-separated cluster.

    Strip any '(...)' reading annotation since the parenthesised
    content is a reading, not an alternate form.
    """
    no_parens = re.sub(r'\([^\)]*\)', '', form_cluster).strip()
    return [t.strip() for t in SLASH_TOKEN_SPLIT.split(no_parens) if t.strip()]


# Manual override / fallback for multi-form aliases. Two cases:
#
#   (a) The cluster has no match at all in vocab.json (8 below).
#   (b) The cluster has a vocab.json match but it's a homograph and
#       picks the wrong POS via lookup. Two known homograph mis-tags:
#         - くらい: vocab.json has the i-adj "dark"; the multi-form
#           "ぐらい / くらい - about" line is the particle.
#         - れい:   vocab.json has the noun "courtesy"; the multi-form
#           "ゼロ / れい - zero" line is the numeral.
#       For these the override fires regardless of vocab.json match.
#
# Identified by audit on 2026-05-03; N=10 entries.
MANUAL_FALLBACK: dict[frozenset[str], str] = {
    # (a) no vocab.json match
    frozenset(['いえ', 'うち']): 'n.',
    frozenset(['ござる', 'ございます']): 'v1',
    frozenset(['いい', 'よい']): 'i-adj',
    frozenset(['みんな', 'みな']): 'pron.',
    frozenset(['では', 'じゃ']): 'exp.',
    frozenset(['けれど', 'けれども', 'けど']): 'conj.',
    frozenset(['じゃあ', 'では']): 'exp.',
    frozenset(['やはり', 'やっぱり']): 'adv.',
    # (b) homograph override — must beat vocab.json's match
    frozenset(['ぐらい', 'くらい']): 'part.',
    frozenset(['ゼロ', 'れい']): 'num.',
}


def lookup_pos(tokens: list[str], by_form: dict[str, set[str]],
               by_reading: dict[str, set[str]]) -> str | None:
    """Return a POS tag for the multi-form cluster.

    Resolution order:
      1. MANUAL_FALLBACK override (handles both no-match and homograph
         mis-tag cases — must run BEFORE vocab.json lookup).
      2. Single-candidate vocab.json match.
      3. Multi-candidate priority list (rare; only for unambiguous
         word-class chains).
    """
    # 1. Manual override always wins. Handles both:
    #    (a) cluster has no vocab.json match,
    #    (b) cluster has a wrong-POS homograph match.
    manual = MANUAL_FALLBACK.get(frozenset(tokens))
    if manual is not None:
        return manual

    candidates: set[str] = set()
    for tok in tokens:
        candidates |= by_form.get(tok, set())
        candidates |= by_reading.get(tok, set())
    if not candidates:
        return None
    if len(candidates) == 1:
        return next(iter(candidates))
    # Multiple POS tags found; prefer the order matching the broader
    # category most often used in the MD legend (n., v1, etc.).
    PRIORITY = ['n.', 'v1', 'v2', 'v3', 'i-adj', 'na-adj', 'adv.', 'part.',
                'conj.', 'pron.', 'count.', 'num.', 'dem.', 'Q-word', 'exp.',
                'interj.']
    for p in PRIORITY:
        if p in candidates:
            return p
    return next(iter(candidates))


def main() -> int:
    by_form, by_reading = build_vocab_index()
    text = MD_PATH.read_text(encoding='utf-8')
    out_lines: list[str] = []
    in_section = False
    changed = 0
    skipped: list[tuple[int, str]] = []
    for ln, raw in enumerate(text.split('\n'), 1):
        if raw.startswith('## '):
            in_section = bool(SECTION_RE.match(raw))
            out_lines.append(raw)
            continue
        if not in_section or not raw.startswith('- '):
            out_lines.append(raw)
            continue
        rest = raw[2:].lstrip()
        if not IS_JP.search(rest[:1]):
            out_lines.append(raw)
            continue
        # If the line already has a POS tag in any position, leave alone.
        if TAG_PRESENT.search(raw):
            out_lines.append(raw)
            continue
        m = MULTIFORM_LINE.match(raw)
        if not m:
            out_lines.append(raw)
            continue
        form_cluster, dash_sep, gloss = m.group(2), m.group(3), m.group(4)
        tokens = extract_form_tokens(form_cluster)
        tag = lookup_pos(tokens, by_form, by_reading)
        if tag is None:
            skipped.append((ln, raw))
            out_lines.append(raw)
            continue
        new_line = f'{m.group(1)}{form_cluster}{dash_sep}[{tag}] {gloss}'
        out_lines.append(new_line)
        changed += 1

    if changed:
        MD_PATH.write_text('\n'.join(out_lines), encoding='utf-8')
    print(f'POS tags inserted: {changed}')
    if skipped:
        print(f'Could not resolve POS for {len(skipped)} lines:')
        for ln, raw in skipped:
            print(f'  L{ln}: {raw}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
