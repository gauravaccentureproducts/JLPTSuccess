"""Pass-23 dedup: 10 question IDs (q-0479..q-0488) appear twice in
data/questions.json. The first occurrence per ID is my Pass-16 content
(giving / receiving / ので / ながら / frequency adverbs); the second
occurrence is parallel-session-authored content (まで / possessive の /
nominalizer / question words). Both are valid content; both should stay.

Strategy: keep the FIRST occurrence at its existing ID; renumber the
SECOND occurrence to fresh IDs starting at max-existing+1.

Idempotent: re-running after dedup is a no-op.
"""
import json
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

qpath = ROOT / 'data' / 'questions.json'
data = json.load(qpath.open(encoding='utf-8'))

# Find duplicates
seen: set[str] = set()
duplicates: list[tuple[int, dict]] = []  # (index, question)
for i, q in enumerate(data['questions']):
    qid = q.get('id')
    if qid in seen:
        duplicates.append((i, q))
    else:
        seen.add(qid)

if not duplicates:
    print('No duplicate IDs. No-op.')
    sys.exit(0)

# Find max existing q-NNNN ID
max_n = 0
for q in data['questions']:
    qid = q.get('id', '')
    if qid.startswith('q-') and qid[2:].isdigit():
        n = int(qid[2:])
        if n > max_n:
            max_n = n
print(f'Max existing q-NNNN: q-{max_n:04d}')
print(f'Found {len(duplicates)} duplicate-ID entries to renumber')

# Renumber second occurrences
new_id_start = max_n + 1
renumbered: list[tuple[str, str]] = []
for offset, (idx, q) in enumerate(duplicates):
    new_id = f'q-{new_id_start + offset:04d}'
    old_id = q['id']
    q['id'] = new_id
    renumbered.append((old_id, new_id))
    print(f'  {old_id} -> {new_id} (Q: {(q.get("question_ja","") or "")[:60]})')

# Update _meta block
meta = data.get('_meta', {})
meta['question_count'] = len(data['questions'])
if 'id_range' in meta:
    new_max = 0
    for q in data['questions']:
        qid = q.get('id', '')
        if qid.startswith('q-') and qid[2:].isdigit():
            new_max = max(new_max, int(qid[2:]))
    meta['id_range']['last'] = f'q-{new_max:04d}'
# Append history note
history = meta.get('history', [])
note = (f'Pass-23 dedup (2026-05-02): renumbered {len(renumbered)} '
        f'duplicate-ID question entries (q-0479..q-0488 collision between '
        f'Pass-16 content and parallel-session particle/nominalizer batch). '
        f'Second occurrences moved to {renumbered[0][1]}..{renumbered[-1][1]}.')
if not any('Pass-23 dedup' in (h or '') for h in history):
    history.append(note)
    meta['history'] = history
data['_meta'] = meta

qpath.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding='utf-8',
)
print(f'\nWrote {qpath.relative_to(ROOT)}')
print(f'Total questions: {len(data["questions"])} (no count change; just IDs)')
