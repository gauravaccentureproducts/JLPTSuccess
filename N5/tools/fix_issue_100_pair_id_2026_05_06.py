"""ISSUE-100 (round-9): vocab pair_id (transitivity) integrity.

The audit reported 22/1041 entries paired — that count was correct but
hid 3 data bugs: pair_id wrongly assigned to homonym entries that share
form+reading but are NOT part of the transitivity pair semantically:

  1. しめる (id=...しめる.2, "to tie / fasten") had pair_id=close, but
     "tie / fasten" is not part of the 開ける/閉める transitive-pair
     cluster. Only the "close" sense should be paired with 閉まる.
  2. いれる (id=...いれる, "to make (tea / coffee)") had pair_id=enter,
     but "make (a drink)" is not part of the 入れる/入る pair. Only the
     "put in" sense should be paired with 入る.
  3. きる (id=...28-verbs-group-2-verbs.きる, "to wear (upper body)",
     verb-2) had pair_id=cut, but "wear" is not part of the 切る/切れる
     pair. Only the "cut" sense (verb-1, Group-1 exception) should be
     paired (with 切れる, which is absent from the corpus — see _meta
     gap note below).

After this fix:
  - 9 complete pairs (open, close, enter, exit, begin, drop,
    switch_on, switch_off) — both transitive + intransitive present
  - 3 single-sided pairs (stop, wake, cut) — partner absent from
    corpus; these are flagged in _meta for future width-exception scope

The X-6.6 invariant (Group-1 exception verbs that look like Group-2)
is unrelated to pair_id; that's covered by ISSUE-099.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

VOCAB = Path(__file__).parent.parent / 'data' / 'vocab.json'

# Identify entries to strip pair_id from (the 3 homonym data bugs)
# Use (id) as the unique key — reading-only is ambiguous because that
# IS exactly the homonym situation we're disambiguating.
WRONG_PAIRINGS = {
    'n5.vocab.28-verbs-group-2-verbs.しめる.2',  # tie/fasten, not "close"
    'n5.vocab.28-verbs-group-2-verbs.いれる',     # make tea, not "put in"
    'n5.vocab.28-verbs-group-2-verbs.きる',        # to wear, not "cut"
}

# Asymmetric pairs whose transitive partner is absent from the corpus.
# These are documented in vocab._meta so future audits know it's intentional
# (corpus coverage gap) not pair_id authoring drift.
ASYMMETRIC_PAIRS = {
    'stop': {'present': '止まる (とまる, intransitive)', 'absent': '止める (とめる, transitive)'},
    'wake': {'present': '起きる (おきる, intransitive)', 'absent': '起こす (おこす, transitive)'},
    'cut':  {'present': '切る (きる, transitive, Group-1 exception)', 'absent': '切れる (きれる, intransitive)'},
}


def main() -> int:
    doc = json.loads(VOCAB.read_text(encoding='utf-8'))
    entries = doc['entries']

    n_stripped = 0
    for w in entries:
        if w.get('id') in WRONG_PAIRINGS and 'pair_id' in w:
            del w['pair_id']
            n_stripped += 1

    # Document asymmetric-pair gaps in _meta.
    if '_meta' not in doc:
        doc['_meta'] = {}
    doc['_meta']['transitivity_pair_gaps'] = {
        'note': (
            'Pair_id integrity: 9 complete pairs (open/close/enter/exit/'
            'begin/drop/switch_on/switch_off) + 3 single-sided pairs '
            'where the partner verb is absent from the N5 vocab corpus. '
            'Documented per ISSUE-100 (round-9 audit, 2026-05-06). '
            'Adding the missing partners (止める, 起こす, 切れる) is a '
            'width-add deferred to a future cycle (cf. anti-items list '
            'in audit-round9-2026-05-06.md §7).'
        ),
        'asymmetric_pairs': ASYMMETRIC_PAIRS,
    }

    VOCAB.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )
    print(f'Stripped pair_id from {n_stripped} homonym entries.')

    # Verify
    doc2 = json.loads(VOCAB.read_text(encoding='utf-8'))
    paired = [w for w in doc2['entries'] if w.get('pair_id')]
    by_pair = {}
    for w in paired:
        by_pair.setdefault(w['pair_id'], []).append(w)
    print(f'\nPost-fix pair_id state: {len(paired)} entries across {len(by_pair)} pairs.')
    complete = sum(1 for ws in by_pair.values() if len(ws) == 2 and len({w.get("transitivity") for w in ws}) == 2)
    asymmetric = len(by_pair) - complete
    print(f'  Complete pairs (both transitive + intransitive): {complete}')
    print(f'  Asymmetric pairs (partner absent from corpus): {asymmetric}')
    for pid, ws in sorted(by_pair.items()):
        bits = [(w['form'], w.get('transitivity', '-')) for w in ws]
        marker = '✓' if len(ws) == 2 and len({w.get("transitivity") for w in ws}) == 2 else '⚠'
        print(f'  {marker} {pid}: {bits}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
