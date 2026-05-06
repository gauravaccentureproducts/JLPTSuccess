"""ISSUE-099 (round-9): vocab verb_class missing on all 134 verbs.

Adds `verb_class` derived from `pos`:
  verb-1 -> "godan"      (Group 1, u-verbs)
  verb-2 -> "ichidan"    (Group 2, ru-verbs)
  verb-3 -> "irregular"  (Group 3, suru/kuru and compound -suru verbs)

Adds `group1_exception: true` on the 6 X-6.6-invariant verbs that look
like Group-2 (ru-ending) but conjugate as Group-1 (godan): 入る (はいる),
帰る (かえる), 走る (はしる), 知る (しる), 切る (きる), 要る (いる).

Identified by (reading, pos="verb-1") since 5 of them are stored in kana form.

Idempotent: skips entries that already have verb_class set.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

VOCAB = Path(__file__).parent.parent / 'data' / 'vocab.json'

POS_TO_CLASS = {
    'verb-1': 'godan',
    'verb-2': 'ichidan',
    'verb-3': 'irregular',
}

# X-6.6 invariant: 6 Group-1 verbs with ru-ending that LOOK like Group-2.
# Identified by (reading, pos="verb-1") to avoid colliding with the homophone
# 切る (verb-2 "to wear") and 要る (verb-1 "to need" — Group-1 exception)
# vs the existence-いる (verb-2).
GROUP1_EXCEPTIONS = {
    ('はいる', 'verb-1'),  # 入る "to enter"
    ('かえる', 'verb-1'),  # 帰る "to return home"
    ('はしる', 'verb-1'),  # 走る "to run"
    ('しる',   'verb-1'),  # 知る "to know"
    ('きる',   'verb-1'),  # 切る "to cut"
    ('いる',   'verb-1'),  # 要る "to need"
}


def main() -> int:
    doc = json.loads(VOCAB.read_text(encoding='utf-8'))
    entries = doc['entries']

    n_verb_class_added = 0
    n_group1_added = 0
    n_skipped = 0

    for w in entries:
        pos = w.get('pos', '')
        if pos not in POS_TO_CLASS:
            continue  # not a verb

        # Set verb_class
        if 'verb_class' not in w:
            w['verb_class'] = POS_TO_CLASS[pos]
            n_verb_class_added += 1
        else:
            n_skipped += 1

        # Set group1_exception
        key = (w.get('reading', ''), pos)
        if key in GROUP1_EXCEPTIONS:
            if not w.get('group1_exception'):
                w['group1_exception'] = True
                n_group1_added += 1

    # Re-serialize preserving key order on existing entries; add new keys at end.
    VOCAB.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print(f'verb_class added on {n_verb_class_added} entries (skipped {n_skipped} already-set).')
    print(f'group1_exception added on {n_group1_added} entries.')

    # Verify
    doc2 = json.loads(VOCAB.read_text(encoding='utf-8'))
    verbs = [w for w in doc2['entries'] if str(w.get('pos', '')).startswith('verb')]
    have_class = sum(1 for w in verbs if w.get('verb_class'))
    have_g1 = sum(1 for w in verbs if w.get('group1_exception'))
    by_class = {}
    for w in verbs:
        c = w.get('verb_class', '?')
        by_class[c] = by_class.get(c, 0) + 1
    print(f'\nPost-fix verification:')
    print(f'  Verbs with verb_class: {have_class}/{len(verbs)}')
    print(f'  Distribution: {by_class}')
    print(f'  Group-1 exceptions tagged: {have_g1}/6')
    return 0


if __name__ == '__main__':
    sys.exit(main())
