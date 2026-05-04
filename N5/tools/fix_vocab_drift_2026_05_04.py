"""Resolve vocab drift: add 28 missing JSON-only entries to vocabulary_n5.md.

Audit found that vocab.json had 28 entries with no representation in
vocabulary_n5.md. Each is appended to its appropriate thematic section
in the MD source. PoS tag mapped from JSON `pos` field per the
'## Part-of-Speech Tags' legend.

Idempotent: skips entries already present.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / 'KnowledgeBank' / 'vocabulary_n5.md'

POS_TO_MD = {
    'noun': '[n.]',
    'verb-1': '[v1]',
    'verb-2': '[v2]',
    'verb-3': '[v3]',
    'i-adjective': '[i-adj]',
    'na-adjective': '[na-adj]',
    'adverb': '[adv.]',
    'particle': '[part.]',
    'conjunction': '[conj.]',
    'pronoun': '[pron.]',
    'counter': '[count.]',
    'numeral': '[num.]',
    'demonstrative': '[dem.]',
    'expression': '[exp.]',
    'interjection': '[interj.]',
}

# Per-entry: (form, target_section_heading, optional_reading_in_paren)
# Mapped by hand based on thematic fit. The target_section is the H2
# heading; the entry is appended before the next H2 (or end-of-file).
ADDITIONS = [
    # form, JSON-form, target_section_heading, reading_paren (None if same as form)
    ('いっぱい',  '## 33. Adverbs',                       None),
    ('おくれる', '## 28. Verbs - Group 2 (る-verbs)',     None),
    ('おしらせ', '## 37. Common Nouns - Miscellaneous',   None),
    ('おじゃまします', '## 36. Greetings and Set Phrases', None),
    ('おてら',   '## 13. Locations and Places (general)', None),
    ('おもちゃ', '## 37. Common Nouns - Miscellaneous',   None),
    ('さくら',   '## 14. Nature and Weather',             None),
    ('じゅんび', '## 29. Verbs - Irregular and する-verbs', None),
    ('ぜひ',     '## 33. Adverbs',                       None),
    ('ただ',     '## 33. Adverbs',                       None),
    ('ためる',   '## 28. Verbs - Group 2 (る-verbs)',     None),
    ('たんご',   '## 24. School and Study',              None),
    ('はらう',   '## 27. Verbs - Group 1 (う-verbs)',     None),
    ('べつべつ', '## 33. Adverbs',                       None),
    ('アルバイト', '## 24. School and Study',            None),
    ('カフェ',   '## 13. Locations and Places (general)', None),
    ('コンサート', '## 37. Common Nouns - Miscellaneous', None),
    ('コンビニ', '## 13. Locations and Places (general)', None),
    ('スペイン人', '## 25. Languages and Countries',     'スペインじん'),
    ('セール',   '## 22. Money and Shopping',            None),
    ('フロント', '## 13. Locations and Places (general)', None),
    ('ベンチ',   '## 26. House and Furniture',           None),
    ('倍',       '## 9. Counters (Common)',              'ばい'),
    ('出口',     '## 13. Locations and Places (general)', 'でぐち'),
    ('国籍',     '## 25. Languages and Countries',       'こくせき'),
    ('聞こえる', '## 28. Verbs - Group 2 (る-verbs)',    'きこえる'),
    ('週末',     '## 11. Time - Days, Weeks, Months, Years', 'しゅうまつ'),
    ('高校生',   '## 24. School and Study',              'こうこうせい'),
]


def main() -> int:
    vocab = json.loads((ROOT / 'data/vocab.json').read_text(encoding='utf-8'))['entries']
    by_form = {e['form'].split('/')[0].strip(): e for e in vocab}

    text = KB.read_text(encoding='utf-8')

    changes = []

    for form, section_heading, reading_paren in ADDITIONS:
        # Already in MD?
        line_re = re.compile(rf'^- {re.escape(form)}\b', re.MULTILINE)
        if line_re.search(text):
            continue

        entry = by_form.get(form)
        if entry is None:
            print(f'  WARN: {form} not in JSON, skipping')
            continue

        pos_md = POS_TO_MD.get(entry.get('pos', ''), '[n.]')
        gloss = entry.get('gloss', '?').strip()

        # Build the MD line
        if reading_paren and reading_paren != form:
            line = f'- {form} ({reading_paren}) - {pos_md} {gloss}'
        else:
            line = f'- {form} - {pos_md} {gloss}'

        # Find section heading + insert before next ## heading (or end)
        section_match = re.search(rf'^{re.escape(section_heading)}.*?$', text, re.MULTILINE)
        if not section_match:
            print(f'  WARN: section "{section_heading}" not found for {form}')
            continue

        # Find the position to insert: end of this section (just before next ##)
        next_h2 = re.search(r'^## ', text[section_match.end():], re.MULTILINE)
        if next_h2:
            insert_pos = section_match.end() + next_h2.start()
        else:
            insert_pos = len(text)

        # Insert. Make sure there's a newline before our line and the section ends cleanly.
        # Find the last non-empty line of the section (strip trailing blank lines)
        section_text = text[section_match.end():insert_pos]
        # Find last content line
        section_text_stripped = section_text.rstrip('\n')
        new_section_end = section_match.end() + len(section_text_stripped)

        text = (text[:new_section_end] + '\n' + line +
                text[new_section_end:])

        changes.append(f'  + {form} -> {section_heading.strip("# ")}')

    if not changes:
        print('No changes (all 28 already present).')
        return 0

    KB.write_text(text, encoding='utf-8')
    print(f'{len(changes)} entries added to vocabulary_n5.md:')
    for c in changes:
        print(c)
    return 0


if __name__ == '__main__':
    sys.exit(main())
