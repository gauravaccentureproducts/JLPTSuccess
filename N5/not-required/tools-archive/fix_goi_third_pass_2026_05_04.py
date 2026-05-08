"""Apply 4 follow-up fixes from the goi third-pass review (2026-05-04).

After v1.12.14 closed the second-pass items, the same auditor flagged
five remaining observations on a third-pass walk-through. Four are
addressed here; the fifth (Q73/Q74 mirror-pair scatter) is deferred
because the reviewer themselves flagged it as "pedagogically not wrong
as is, just an exam-realism nudge", and a content swap shuffles the
Q-number<->content mapping which has audit-traceability cost.

Applied:
  - Q33: つかれたので -> つかれましたから (corpus-wide ので -> から policy
         consistency, matching the Q5 fix from v1.12.14).
  - Q44: あめが ふって いるので -> あめが ふって いるから (same policy).
  - Q47: rationale reframed - the orphaned きょねん note becomes an
         explicit "Common error" call-out that anticipates a typical
         student error.
  - Q87: off-topic はたち reading note removed; rationale now focuses on
         time-reference (which is what the question actually tests).
         はたち remains documented at vocabulary_n5.md line 1118 so
         no information is lost.

Idempotent. Lock-step MD <-> paper-JSON updates so JA-32 stays green.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / 'KnowledgeBank' / 'goi_questions_n5.md'
PAPERS = ROOT / 'data' / 'papers' / 'goi'

changes: list[str] = []


# ---------------------------------------------------------------------------
# JSON-side updates (paper-3 has Q33+Q44; paper-4 has Q47; paper-6 has Q87)
# ---------------------------------------------------------------------------

JSON_FIXES = {
    # Q33 / goi-3.3: ので -> から (policy consistency)
    (3, 'goi-3.3'): {
        'stem_html': 'つかれましたから、（　　） すわりました。',
        'rationale': 'immediately. (から: N5-canonical reason conjunction; replaces ので per corpus-wide policy applied alongside the Q5 fix in v1.12.14.)',
    },

    # Q44 / goi-3.14: ので -> から (policy consistency)
    (3, 'goi-3.14'): {
        'stem_html': 'きょうは あめが ふって いるから、（　　） を もって きました。',
        'rationale': 'rain + umbrella. (から: N5-canonical reason conjunction; replaces ので per corpus-wide policy applied alongside the Q5 fix in v1.12.14.)',
    },

    # Q47 / goi-4.2: reframe orphaned note as anticipating student error
    (4, 'goi-4.2'): {
        'rationale': 'こと + ある (experience). Common error: 「〜たことがある」 cannot combine with specific time markers (きょねん, etc.) - it expresses indefinite past experience. Use a plain past tense (きょねん 行きました) for time-specific events instead.',
    },

    # Q87 / goi-6.12: drop off-topic はたち reading trivia, focus on
    # time-reference (which is what the question actually tests).
    (6, 'goi-6.12'): {
        'rationale': 'statement of present age. The keyed answer 「いま 二十さいです」 is a direct restatement of the stem\'s present-tense identity claim; the other options shift the time reference (this year / birthday tomorrow / next year). The special reading はたち for 二十さい is documented at vocabulary_n5.md but does not bear on the time-reference test point this question targets.',
    },
}


def update_paper_jsons() -> None:
    for (paper_n, qid), updates in JSON_FIXES.items():
        p_path = PAPERS / f'paper-{paper_n}.json'
        paper = json.loads(p_path.read_text(encoding='utf-8'))
        modified = False
        for q in paper.get('questions', []):
            if q.get('id') != qid:
                continue
            for k, v in updates.items():
                if q.get(k) != v:
                    q[k] = v
                    modified = True
                    changes.append(f'paper-{paper_n}.json {qid}: updated {k}')
        if modified:
            p_path.write_text(json.dumps(paper, ensure_ascii=False, indent=2),
                              encoding='utf-8')


# ---------------------------------------------------------------------------
# MD-side updates
# ---------------------------------------------------------------------------

MD_REPLACEMENTS = {
    'Q33': '''### Q33

つかれましたから、（　　） すわりました。

1. すぐ
2. もう
3. まだ
4. ぜんぜん

**Answer: 1** - immediately. (から: N5-canonical reason conjunction; replaces ので per corpus-wide policy applied alongside the Q5 fix in v1.12.14.)''',

    'Q44': '''### Q44

きょうは あめが ふって いるから、（　　） を もって きました。

1. かばん
2. かさ
3. ぼうし
4. めがね

**Answer: 2** - rain + umbrella. (から: N5-canonical reason conjunction; replaces ので per corpus-wide policy applied alongside the Q5 fix in v1.12.14.)''',

    'Q47': '''### Q47

私は にほんへ いった ことが （　　）。

1. います
2. あります
3. なります
4. します

**Answer: 2** - こと + ある (experience). Common error: 「〜たことがある」 cannot combine with specific time markers (きょねん, etc.) - it expresses indefinite past experience. Use a plain past tense (きょねん 行きました) for time-specific events instead.''',

    'Q87': '''### Q87

A: わたしは 二十さいです。

1. わたしは ことし 二十さいに なります。
2. わたしの たんじょうびは あした です。
3. わたしは いま 二十さいです。
4. わたしは らいねん 二十さいに なります。

**Answer: 3** - statement of present age. The keyed answer 「いま 二十さいです」 is a direct restatement of the stem\'s present-tense identity claim; the other options shift the time reference (this year / birthday tomorrow / next year). The special reading はたち for 二十さい is documented at vocabulary_n5.md but does not bear on the time-reference test point this question targets.''',
}


def update_md_source() -> None:
    text = KB.read_text(encoding='utf-8')
    original_text = text
    for qnum, replacement in MD_REPLACEMENTS.items():
        block_re = re.compile(
            rf'### {re.escape(qnum)}\b[\s\S]+?(?=\n### Q\d|\n## )'
        )
        m = block_re.search(text)
        if m is None:
            changes.append(f'goi_questions_n5.md {qnum}: NOT FOUND (skipped)')
            continue
        if m.group(0).strip() == replacement.strip():
            continue
        text = text[:m.start()] + replacement + '\n' + text[m.end():]
        changes.append(f'goi_questions_n5.md {qnum}: replaced block (third-pass fix)')
    if text != original_text:
        KB.write_text(text, encoding='utf-8')


def main() -> int:
    update_md_source()
    update_paper_jsons()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
