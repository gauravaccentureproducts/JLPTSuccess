"""ISSUE-017 (audit round-3): rebalance answer-position on goi/paper-1
and moji/paper-1.

Both papers had distribution {0:2, 1:2, 2:3, 3:8} (spread 6) — almost
half the answers landed on choice D, defeating the face-validity of
"audited paper". Target: {0:4, 1:4, 2:3, 3:4} (spread 1, mirroring the
global 25.1/25.1/24.9/24.9% the rest of the corpus achieves).

Method: pick 4 items per paper currently at correctIndex=3 and rotate
their choice arrays so the right answer moves to a different slot.
This preserves question semantics — only the visual ordering changes —
and the correctIndex updates in lock-step.

Per-paper plan:
  goi/paper-1:
    goi-1.1 : swap choices[0] ↔ [3] → correctIndex 3 → 0
    goi-1.2 : swap choices[0] ↔ [3] → correctIndex 3 → 0
    goi-1.3 : swap choices[1] ↔ [3] → correctIndex 3 → 1
    goi-1.6 : swap choices[1] ↔ [3] → correctIndex 3 → 1
  moji/paper-1:
    moji-1.1: swap choices[0] ↔ [3] → correctIndex 3 → 0
    moji-1.2: swap choices[0] ↔ [3] → correctIndex 3 → 0
    moji-1.3: swap choices[1] ↔ [3] → correctIndex 3 → 1
    moji-1.6: swap choices[1] ↔ [3] → correctIndex 3 → 1

Each rotation: distribution moves 2 items 3→0 and 2 items 3→1, net
delta {0: +2, 1: +2, 3: -4}, landing {0:4, 1:4, 2:3, 3:4}.

Idempotent: if the target distribution is already in place, nothing
changes.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / 'data' / 'papers'

# (paper-relpath, [(question-id, swap-with-index), ...])
PLAN = [
    ('goi/paper-1.json', [
        ('goi-1.1', 0),
        ('goi-1.2', 0),
        ('goi-1.3', 1),
        ('goi-1.6', 1),
    ]),
    ('moji/paper-1.json', [
        ('moji-1.1', 0),
        ('moji-1.2', 0),
        ('moji-1.3', 1),
        ('moji-1.6', 1),
    ]),
]


def rotate(q: dict, swap_with: int) -> bool:
    """Swap choices[correctIndex] with choices[swap_with] in-place. Return
    True if the rotation was applied (False if already aligned)."""
    ci = q.get('correctIndex')
    if ci == swap_with:
        return False
    choices = q['choices']
    choices[ci], choices[swap_with] = choices[swap_with], choices[ci]
    q['correctIndex'] = swap_with
    return True


def main() -> int:
    rotated = 0
    for relpath, items in PLAN:
        p = PAPERS / relpath
        d = json.loads(p.read_text(encoding='utf-8'))
        questions_by_id = {q['id']: q for q in d['questions']}
        for qid, target_idx in items:
            q = questions_by_id.get(qid)
            if not q:
                print(f'WARN: {relpath} has no question {qid}; skipping')
                continue
            if rotate(q, target_idx):
                rotated += 1
                print(f'  {relpath} {qid}: correctIndex 3 -> {target_idx}')
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nRotated {rotated} question(s).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
