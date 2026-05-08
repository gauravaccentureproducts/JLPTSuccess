"""Swap Q74 <-> Q83 content (paper-5.14 <-> paper-6.8) per third-pass review.

Reviewer flagged Q73 (kasu perspective) and Q74 (kariru perspective)
as a conceptually-mirror pair appearing in immediate sequence in
paper-5 (positions 5.13 + 5.14). Their suggestion: scatter them so
the mirror perspective doesn't give an exam-realism freebie via
pattern recognition.

Implementation: swap Q74's content with Q83 (transportation: のる -> で,
which is unrelated to giving/receiving). After swap:

  Q73 (paper-5.13)  - kasu perspective (UNCHANGED)
  Q74 (paper-5.14)  - transportation (was Q83's content)
  Q83 (paper-6.8)   - kariru perspective (was Q74's content)

Distance between Q73 (kasu) and Q83-now-with-kariru: 10 questions in
different papers. Clean separation.

kbSourceId mapping is preserved (paper-5.14 -> "Q74", paper-6.8 ->
"Q83") because kbSourceId tracks MD position, not semantic content.
JA-32 stays green via lock-step MD <-> JSON updates.

Audit-traceability note: pre-v1.12.16 audit reports referencing "Q74"
mean kariru; post-v1.12.16 they mean transportation. The swap is
fully documented in CHANGELOG v1.12.16. Q73 is unchanged.

Idempotent: detects current content state and only swaps if needed.
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


# Target content for each Q-position after the swap.
# Q74 receives the transportation content; Q83 receives the kariru
# (borrow) content. Q73 is unchanged.
Q74_NEW_CONTENT = {
    'stem_html': 'A: わたしは バスに のって 学校へ いきます。',
    'choices': [
        'わたしは あるいて 学校へ いきます。',
        'わたしは でんしゃで 学校へ いきます。',
        'わたしは バスで 学校へ いきます。',
        'わたしは じてんしゃで 学校へ いきます。',
    ],
    'correctIndex': 2,
    'rationale': 'のって ≈ で.',
}

Q83_NEW_CONTENT = {
    'stem_html': 'A: 友だちから 本を かりました。',
    'choices': [
        '友だちが 私に 本を かしました。',
        '友だちが 私から 本を かりました。',
        '私が 友だちに 本を あげました。',
        '友だちは 本を かいました。',
    ],
    'correctIndex': 0,
    'rationale': 'borrowed = friend lent.',
}

# Map (paper_n, qid) -> target content (kbSourceId is preserved).
JSON_FIXES = {
    (5, 'goi-5.14'): Q74_NEW_CONTENT,
    (6, 'goi-6.8'): Q83_NEW_CONTENT,
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


# MD blocks for the two swapped positions
MD_REPLACEMENTS = {
    'Q74': '''### Q74

A: わたしは バスに のって 学校へ いきます。

1. わたしは あるいて 学校へ いきます。
2. わたしは でんしゃで 学校へ いきます。
3. わたしは バスで 学校へ いきます。
4. わたしは じてんしゃで 学校へ いきます。

**Answer: 3** - のって ≈ で.''',

    'Q83': '''### Q83

A: 友だちから 本を かりました。

1. 友だちが 私に 本を かしました。
2. 友だちが 私から 本を かりました。
3. 私が 友だちに 本を あげました。
4. 友だちは 本を かいました。

**Answer: 1** - borrowed = friend lent.''',
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
        changes.append(f'goi_questions_n5.md {qnum}: replaced block (Q74<->Q83 swap)')
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
