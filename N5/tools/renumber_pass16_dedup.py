"""
Repair: 10 IDs (q-0454 .. q-0463) currently appear TWICE in
data/questions.json — once from my Pass-16 commit (2f90e61) using
patterns n5-130 / n5-131 / n5-134 / n5-144 / n5-148, and again from a
parallel Pass-15 P0 commit (12629d5) using paraphrase subtype with
patterns n5-117 / n5-079 / etc. Both branches landed independently and
the parallel commit didn't see my prior IDs.

This script keeps the parallel session's q-0454..q-0463 (paraphrase set,
which is also the broader Pass-15 P0 cluster q-0454..q-0472) and
renumbers my Pass-16 questions to q-0479..q-0488 (after the highest
existing ID q-0478 from Pass-15 P1 kanji_writing).

Identification: my Pass-16 entries are uniquely identifiable by their
grammarPatternId being one of {n5-130, n5-131, n5-134, n5-144, n5-148}
AND their auto field being False AND the q-id in q-0454..q-0463. The
parallel set has subtype='paraphrase' and uses other patterns.

Idempotent: re-running after renumber is a no-op.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QPATH = ROOT / 'data' / 'questions.json'

# Pattern membership identifies my Pass-16 set unambiguously.
MY_PATTERNS = {'n5-130', 'n5-131', 'n5-134', 'n5-144', 'n5-148'}
COLLIDING_RANGE = {f'q-04{n:02d}' for n in range(54, 64)}
NEW_RANGE = {f'q-04{n:02d}' for n in range(79, 89)}

with QPATH.open('r', encoding='utf-8') as f:
    data = json.load(f)

# Find the duplicates
mine = []
others = []
non_colliding = []
for q in data['questions']:
    qid = q.get('id')
    if qid in COLLIDING_RANGE:
        if q.get('grammarPatternId') in MY_PATTERNS and q.get('auto') is False:
            mine.append(q)
        else:
            others.append(q)
    else:
        non_colliding.append(q)

print(f'Mine (Pass-16): {len(mine)} entries — IDs: {sorted(q["id"] for q in mine)}')
print(f'Others (parallel Pass-15 P0 paraphrase): {len(others)} entries — IDs: {sorted(q["id"] for q in others)}')
print(f'Non-colliding: {len(non_colliding)}')

if not mine:
    print('No-op: my Pass-16 entries not found at colliding IDs. Already renumbered or never landed.')
elif len(mine) != 10 or len(others) != 10:
    print('UNEXPECTED count. Aborting without writing.')
else:
    # Renumber: my entries get the new IDs in order. mine is already in
    # order if it was iterated from the file in insertion order.
    # Sort by current id to be safe.
    mine.sort(key=lambda q: q['id'])
    new_ids_sorted = sorted(NEW_RANGE)
    for q, new_id in zip(mine, new_ids_sorted):
        old_id = q['id']
        q['id'] = new_id
        print(f'  {old_id} -> {new_id}')

    # Rebuild questions list
    new_list = non_colliding + others + mine

    # Update _meta block
    meta = data.get('_meta', {})
    meta['question_count'] = len(new_list)
    if 'id_range' in meta:
        # find max id
        max_n = 0
        for qq in new_list:
            qid = qq.get('id', '')
            if qid.startswith('q-') and qid[2:].isdigit():
                max_n = max(max_n, int(qid[2:]))
        meta['id_range']['last'] = f'q-{max_n:04d}'
    if 'type_distribution' in meta:
        from collections import Counter
        tc = Counter(qq.get('type', '?') for qq in new_list)
        meta['type_distribution'] = dict(tc)
    # Append history note
    history = meta.get('history', [])
    note = ('Pass-17 dedup (2026-05-01): repaired duplicate-ID collision between '
            'Pass-16 (giving/receiving + ので + ながら + frequency adverbs) and a '
            'parallel Pass-15 P0 (paraphrase) that both claimed q-0454..q-0463. '
            'The Pass-15 P0 set kept those IDs; Pass-16 questions were renumbered '
            'to q-0479..q-0488 (after Pass-15 P1 kanji_writing q-0478).')
    if not any('Pass-17 dedup' in (h or '') for h in history):
        history.append(note)
        meta['history'] = history

    data['questions'] = new_list
    data['_meta'] = meta
    with QPATH.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Total questions after dedup: {len(new_list)}')
