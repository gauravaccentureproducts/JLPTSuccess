"""ISSUE-061 (audit round-7, 2026-05-06): rebalance questions.json so the
correct-answer position is not heavily skewed toward position 0.

Pre-fix distribution: pos0=56.9%, pos1=30.8%, pos2=8.5%, pos3=3.8%.
Post-fix target:      pos0=25%,   pos1=25%,   pos2=25%,   pos3=25% (+/-)

Method: deterministic per-item position assignment derived from the
question's own id. Choices are rotated so the correct answer lands on
the assigned position. For questions with <4 choices (e.g. text_input or
sentence_order), the rotation is a no-op.

Idempotent: re-running computes the same position for each id and
re-rotates choices (no drift). Distribution is verified after the pass.

Authoring drift safeguard: round-7 added JA-36 invariant; this script
brings questions.json into compliance once at fix-time. Future
authoring waves should write balanced ratios; the invariant catches
drift in CI.
"""
from __future__ import annotations
import io, json, sys
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
QF = ROOT / 'data' / 'questions.json'


def position_for_id(qid: str) -> int:
    """Deterministic 0..3 position derived from the question id.

    Uses the trailing digits of the id (e.g. q-0042 -> 42) modulo 4 so the
    distribution is exactly balanced for sequential-id corpora.
    """
    digits = ''.join(ch for ch in qid if ch.isdigit())
    if not digits:
        return abs(hash(qid)) % 4
    return int(digits) % 4


def main() -> int:
    data = json.loads(QF.read_text(encoding='utf-8'))
    questions = data.get('questions', [])
    n_rotated = 0
    n_skipped = 0
    for q in questions:
        cs = q.get('choices')
        ca = q.get('correctAnswer')
        if not isinstance(cs, list) or len(cs) != 4 or ca not in cs:
            n_skipped += 1
            continue
        target_pos = position_for_id(q.get('id', ''))
        cur_pos = cs.index(ca)
        if cur_pos == target_pos:
            continue
        # Swap the choices at cur_pos and target_pos so the correct answer
        # ends up at target_pos. Distractor explanations (if keyed by string
        # value of the choice) stay valid because we don't mutate strings.
        cs[cur_pos], cs[target_pos] = cs[target_pos], cs[cur_pos]
        n_rotated += 1

    QF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Verify post-distribution
    counts = Counter()
    total = 0
    for q in questions:
        cs = q.get('choices', [])
        ca = q.get('correctAnswer')
        if isinstance(cs, list) and len(cs) == 4 and ca in cs:
            counts[cs.index(ca)] += 1
            total += 1

    print(f'Rotated: {n_rotated}, skipped (non-4-choice): {n_skipped}, total 4-choice: {total}')
    print('Post-fix distribution:')
    for pos in (0, 1, 2, 3):
        n = counts.get(pos, 0)
        pct = 100 * n / total if total else 0
        print(f'  pos{pos}: {n:4d} ({pct:.1f}%)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
