"""Fix item §1.1 from feedback/jlpt-n5-data-files-audit-2026-05-02.md.

Problem: vocab entries cross-listed in thematic sections inherit a
section-default POS rather than the word's actual linguistic POS.
Most pedagogically dangerous: section 30 stamps `verb-1` over `verb-2`
verbs (いる/あげる/くれる/かりる), so a learner conjugating from that
copy would produce *あげります instead of あげます.

Strategy: targeted fix on the 23 entries the audit names explicitly,
plus vocabulary_n5.md sync (JA-31 invariant enforces parity). Naive
"find canonical and propagate" was tried first and overshoots into
homograph territory (人 in section 1 = "person" / pronoun vs section 9
= counter for people; 本 in section 24 = "book" vs section 9 = counter
for long thin objects; おく numeral 億 vs verb 置く; etc). The audit's
explicit list avoids those homograph traps.

Idempotent: re-running is a no-op once fixes are applied.

Audit total: "24+ entries" — this script applies 23 explicit + leaves 1
for a follow-up scan after the runtime test passes (covered separately
in tools/find_remaining_pos_drift.py).
"""
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# (section_slug, form, target_pos)
FIXES = [
    # §1.1 Section 14 Nature/Weather — i-adjectives mis-stamped as noun
    ('14-nature-and-weather', 'あつい',   'i-adj'),
    ('14-nature-and-weather', 'さむい',   'i-adj'),
    ('14-nature-and-weather', 'すずしい', 'i-adj'),
    ('14-nature-and-weather', 'あたたかい','i-adj'),
    # §1.1 Section 20 Colors — i-adjectives mis-stamped as noun
    # Glosses say "(adj)" explicitly; gloss directly contradicted POS.
    ('20-colors', '白い',   'i-adj'),
    ('20-colors', 'くろい', 'i-adj'),
    ('20-colors', 'あかい', 'i-adj'),
    ('20-colors', 'あおい', 'i-adj'),
    ('20-colors', 'きいろい','i-adj'),
    # §1.1 Section 12 Time/Frequency — adverbs mis-stamped as noun
    ('12-time-frequency-sequen', 'いつも',  'adverb'),
    ('12-time-frequency-sequen', 'よく',    'adverb'),
    ('12-time-frequency-sequen', '時々',    'adverb'),
    ('12-time-frequency-sequen', 'たまに',  'adverb'),
    ('12-time-frequency-sequen', 'あまり',  'adverb'),
    ('12-time-frequency-sequen', 'ぜんぜん','adverb'),
    ('12-time-frequency-sequen', 'すぐ',    'adverb'),
    ('12-time-frequency-sequen', 'もう',    'adverb'),
    ('12-time-frequency-sequen', 'まだ',    'adverb'),
    ('12-time-frequency-sequen', 'はじめて','adverb'),
    # §1.1 Section 30 Verbs Existence/Possession — Group-2 mis-stamped Group-1
    # CRITICAL pedagogically: wrong group → wrong conjugation.
    ('30-verbs-existence-and-p', 'いる',   'verb-2'),  # iru = exist (ichidan)
    ('30-verbs-existence-and-p', 'あげる', 'verb-2'),
    ('30-verbs-existence-and-p', 'くれる', 'verb-2'),
    ('30-verbs-existence-and-p', 'かりる', 'verb-2'),
]

# vocabulary_n5.md PoS-tag short forms (matches existing tooling)
POS_TAG_SHORT = {
    'noun':         'n.',
    'verb-1':       'v1',
    'verb-2':       'v2',
    'verb-3':       'v3',
    'i-adj':        'i-adj',
    'na-adj':       'na-adj',
    'adverb':       'adv.',
    'pronoun':      'pron.',
    'particle':     'part.',
    'conjunction':  'conj.',
    'expression':   'expr.',
    'counter':      'counter',
    'demonstrative':'dem.',
    'numeral':      'num.',
    'question-word':'q-word',
    'interjection': 'interj.',
}

def fix_vocab_json(vocab):
    fixed = []
    skipped = []
    for sec, form, target in FIXES:
        eid = f'n5.vocab.{sec}.{form}'
        e = next((x for x in vocab['entries'] if x['id'] == eid), None)
        if not e:
            skipped.append((eid, 'NOT_FOUND'))
            continue
        if e.get('pos') == target:
            skipped.append((eid, 'ALREADY_CORRECT'))
            continue
        before = e.get('pos')
        e['pos'] = target
        fixed.append((eid, before, target))
    return fixed, skipped

def fix_vocab_md(md_text, fixed_entries):
    """For each fixed entry, find the line in vocabulary_n5.md and update its
    [POS] tag. The MD format is:  - <form> (<reading>) - [<pos>] <gloss>
    OR:                           - <form> - [<pos>] <gloss>   (when reading == form)

    We search by form within the same section header (## n. <Section Name>).
    """
    lines = md_text.split('\n')
    fixes_applied = []
    skipped_md = []

    # Build a section-aware index: find lines per (section_slug, form)
    # Section header like:  ### 14. Nature and Weather  (or  ## 14. Nature ...)
    sec_map = {}  # line_number → section_slug (loose match)
    current_sec_slug = None
    sec_re = re.compile(r'^#+\s+(\d+)\.\s+(.+?)\s*$')
    for i, line in enumerate(lines):
        m = sec_re.match(line)
        if m:
            num = m.group(1)
            name = m.group(2)
            # Build slug: e.g. "14. Nature and Weather" → "14-nature-and-weather"
            slug = f"{num}-" + re.sub(r'[^a-zA-Z0-9]+', '-', name.lower()).strip('-')
            # The vocab.json IDs use truncated slugs (e.g. "12-time-frequency-sequen"
            # for "Time - Frequency / Sequence"); match by prefix.
            current_sec_slug = slug
        sec_map[i] = current_sec_slug

    for eid, before, target in fixed_entries:
        # eid like "n5.vocab.14-nature-and-weather.あつい"
        parts = eid.split('.')
        sec_slug_short = parts[2]  # "14-nature-and-weather"
        form = parts[3]
        target_short = POS_TAG_SHORT.get(target, target)
        before_short = POS_TAG_SHORT.get(before, before)

        # Find lines matching this form within sections that share the prefix
        # (handle MD section names being longer than the JSON slug truncation)
        candidates = []
        for i, line in enumerate(lines):
            md_sec = sec_map.get(i) or ''
            if not md_sec.startswith(sec_slug_short.split('-')[0] + '-'):
                continue
            # Match line like "- <form> (<reading>) - [<pos>] <gloss>" or "- <form> - [<pos>] <gloss>"
            stripped = line.strip()
            if not stripped.startswith('- '):
                continue
            # Form must appear at start of bullet; followed by space, "(", or " -"
            content = stripped[2:]  # drop "- "
            if content.startswith(form + ' ') or content.startswith(form + '\t'):
                candidates.append(i)

        if not candidates:
            skipped_md.append((eid, 'MD_LINE_NOT_FOUND'))
            continue

        # Update first match (forms are unique within their section)
        idx = candidates[0]
        old_line = lines[idx]
        new_line = re.sub(r'\[' + re.escape(before_short) + r'\]',
                          f'[{target_short}]', old_line, count=1)
        if new_line == old_line:
            # Try replacing whatever bracket value is there with the target
            new_line = re.sub(r'\[[^\]]+\]', f'[{target_short}]', old_line, count=1)
        if new_line != old_line:
            lines[idx] = new_line
            fixes_applied.append((eid, idx + 1))
        else:
            skipped_md.append((eid, f'NO_CHANGE_AT_LINE_{idx+1}'))

    return '\n'.join(lines), fixes_applied, skipped_md

def main():
    vp = ROOT / 'data' / 'vocab.json'
    mdp = ROOT / 'KnowledgeBank' / 'vocabulary_n5.md'

    vocab = json.loads(vp.read_text(encoding='utf-8'))
    md_text = mdp.read_text(encoding='utf-8')

    fixed, skipped = fix_vocab_json(vocab)
    new_md, md_fixes, md_skipped = fix_vocab_md(md_text, fixed)

    vp.write_text(json.dumps(vocab, ensure_ascii=False, indent=2) + '\n',
                  encoding='utf-8')
    mdp.write_text(new_md, encoding='utf-8')

    print('=== fix_pos_thematic_sections.py ===')
    print(f'\ndata/vocab.json: {len(fixed)} fixed, {len(skipped)} skipped')
    for eid, before, target in fixed:
        print(f'  {eid}  {before} → {target}')
    for eid, reason in skipped:
        print(f'  SKIP {eid}  ({reason})')

    print(f'\nKnowledgeBank/vocabulary_n5.md: {len(md_fixes)} fixed, {len(md_skipped)} skipped')
    for eid, line in md_fixes:
        print(f'  line {line}: {eid}')
    for eid, reason in md_skipped:
        print(f'  SKIP {eid}  ({reason})')

if __name__ == '__main__':
    main()
