"""Apply 4th-pass goi review fixes (Q64 content + position rebalance).

Reviewer flagged two issues on the v1.12.16 state:

1. Q64 violates the same N4-potential-form policy applied at Q97.
   Stem 「じょうずに ひきます」 with keyed 「よく ひけます」 (N4 potential
   ひける). Same fix pattern as Q97: replace the keyed answer with a
   syntactic frame swap that uses じょうずです in nominalized predicate
   form, dropping the potential. Concretely Q64's keyed becomes
   「ピアノを ひくのが じょうずです」 - the inverse direction of Q97's
   frame swap (Q97: nominalized -> adverbial; Q64: adverbial ->
   nominalized).

2. Answer-position distribution is heavily skewed (current 19/46/26/9
   for positions A/B/C/D vs target ~25/25/25/25). Reviewer noted this
   gives a position-heuristic freebie to test-wise students. Fix is
   mechanical: permute the choice ORDER within each item to move the
   keyed answer into a position-balanced distribution. Choice CONTENT
   is unchanged; only the order changes.

   Skip semantically-constrained items where choice order has natural
   structure: Q38-41 (counter cluster), Q73 (kasu perspective), Q83
   (kariru perspective), Q92 (giving-receiving), Q64 (gets handled
   in #1). After the rebalance lands at exactly 25/25/25/25.

The 21 permutations were computed by tools/compute_rebalance_plan.py
(deterministic: walks unconstrained items in Q-number order, takes the
first N at each surplus position, distributes to deficit positions).

Implementation: per-Q target correctIndex. For each Q, if the current
correctIndex matches the target, skip; otherwise swap choices[current]
and choices[target] to move the keyed answer. Idempotent. Lock-step
MD <-> paper-JSON updates so JA-32 stays green.
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
# Q64 content fix - executed BEFORE the position rebalance because the
# rebalance plan assumes Q64 has already moved to position D.
# ---------------------------------------------------------------------------

Q64_FIXED_CHOICES = [
    'たなかさんは ピアノが へたです。',
    'たなかさんは ピアノを はじめて ひきます。',
    'たなかさんは ピアノが きらいです。',
    'たなかさんは ピアノを ひくのが じょうずです。',
]
Q64_FIXED_CORRECT_INDEX = 3
Q64_FIXED_RATIONALE = (
    '「じょうずに ひく」 = 「ひくのが じょうず」. Same skill, different '
    'syntactic frame (adverbial -> nominalized adjective predicate). '
    'Strict-N5: drops the previous keyed form 「よく ひけます」 (potential '
    'ひける = N4) per the same policy applied at Q97 in v1.12.13. This '
    'is the inverse direction of Q97\'s frame swap (Q97: nominalized -> '
    'adverbial; Q64: adverbial -> nominalized).'
)


def fix_q64_content() -> None:
    """Replace Q64's content (paper-5.json + MD block)."""
    p_path = PAPERS / 'paper-5.json'
    paper = json.loads(p_path.read_text(encoding='utf-8'))
    modified = False
    for q in paper.get('questions', []):
        if q.get('id') != 'goi-5.4':
            continue
        if (q.get('choices') == Q64_FIXED_CHOICES
                and q.get('correctIndex') == Q64_FIXED_CORRECT_INDEX
                and q.get('rationale') == Q64_FIXED_RATIONALE):
            return
        q['choices'] = Q64_FIXED_CHOICES
        q['correctIndex'] = Q64_FIXED_CORRECT_INDEX
        q['rationale'] = Q64_FIXED_RATIONALE
        modified = True
    if modified:
        p_path.write_text(
            json.dumps(paper, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        changes.append('paper-5.json goi-5.4: Q64 content fix (drop N4 ひけます, frame swap to ひくのが じょうず)')

    # MD block
    text = KB.read_text(encoding='utf-8')
    new_block = '''### Q64

A: たなかさんは じょうずに ピアノを ひきます。

1. たなかさんは ピアノが へたです。
2. たなかさんは ピアノを はじめて ひきます。
3. たなかさんは ピアノが きらいです。
4. たなかさんは ピアノを ひくのが じょうずです。

**Answer: 4** - 「じょうずに ひく」 = 「ひくのが じょうず」. Same skill, different syntactic frame (adverbial -> nominalized adjective predicate). Strict-N5: drops the previous keyed form 「よく ひけます」 (potential ひける = N4) per the same policy applied at Q97 in v1.12.13. This is the inverse direction of Q97\'s frame swap (Q97: nominalized -> adverbial; Q64: adverbial -> nominalized).'''
    block_re = re.compile(r'### Q64\b[\s\S]+?(?=\n### Q\d|\n## )')
    m = block_re.search(text)
    if m and m.group(0).strip() != new_block.strip():
        text = text[:m.start()] + new_block + '\n' + text[m.end():]
        KB.write_text(text, encoding='utf-8')
        changes.append('goi_questions_n5.md Q64: replaced block (content fix)')


# ---------------------------------------------------------------------------
# Position rebalance - 21 permutations computed deterministically by
# tools/compute_rebalance_plan.py. Each entry maps kbSourceId -> target
# correctIndex. Items not listed keep their current correctIndex.
# Q64 is included so the script is fully idempotent for the rebalance.
# ---------------------------------------------------------------------------

# After Q64 content fix, Q64 sits at index 3 (already fixed above).
# These 21 are the rebalance permutations on top.
TARGET_INDEX = {
    # B -> A (6 items)
    'Q1': 0, 'Q5': 0, 'Q7': 0, 'Q8': 0, 'Q13': 0, 'Q17': 0,
    # B -> D (14 items)
    'Q23': 3, 'Q24': 3, 'Q26': 3, 'Q27': 3, 'Q29': 3, 'Q30': 3,
    'Q32': 3, 'Q42': 3, 'Q44': 3, 'Q47': 3, 'Q49': 3, 'Q51': 3,
    'Q53': 3, 'Q57': 3,
    # C -> D (1 item)
    'Q3': 3,
}


def swap_choices(choices: list, idx_a: int, idx_b: int) -> list:
    """Return a new choices list with positions idx_a and idx_b swapped."""
    out = list(choices)
    out[idx_a], out[idx_b] = out[idx_b], out[idx_a]
    return out


def apply_position_swap_in_md(text: str, qnum: str, new_choices: list,
                              new_correct_index: int) -> tuple[str, bool]:
    """Rewrite the MD block for `qnum` with the new ordered choices and
    answer line. Return (new_text, modified)."""
    block_re = re.compile(rf'### {re.escape(qnum)}\b([\s\S]+?)(?=\n### Q\d|\n## )')
    m = block_re.search(text)
    if not m:
        changes.append(f'goi_questions_n5.md {qnum}: NOT FOUND (skipped)')
        return text, False
    block = m.group(0)

    # Build the new numbered list lines
    new_choice_lines = '\n'.join(f'{i+1}. {c}' for i, c in enumerate(new_choices))

    # Replace the existing 4-line numbered list (lines starting with 1./2./3./4.)
    list_re = re.compile(r'(?m)^1\. .+\n2\. .+\n3\. .+\n4\. .+')
    new_block, n = list_re.subn(new_choice_lines, block, count=1)
    if n != 1:
        changes.append(f'goi_questions_n5.md {qnum}: choice list pattern not found (skipped)')
        return text, False

    # Replace the **Answer: N** line. Preserve trailing rationale text.
    answer_re = re.compile(r'\*\*Answer: \d+\*\*')
    new_block, n2 = answer_re.subn(f'**Answer: {new_correct_index+1}**', new_block, count=1)
    if n2 != 1:
        changes.append(f'goi_questions_n5.md {qnum}: Answer line not found (skipped)')
        return text, False

    if new_block == block:
        return text, False
    return text[:m.start()] + new_block + text[m.end():], True


def rebalance_positions() -> None:
    """For each Q in TARGET_INDEX, swap choices[current] and choices[target]
    if current != target. Idempotent.
    """
    md_text = KB.read_text(encoding='utf-8')
    md_modified = False

    for paper_n in range(1, 8):
        p_path = PAPERS / f'paper-{paper_n}.json'
        paper = json.loads(p_path.read_text(encoding='utf-8'))
        json_modified = False
        for q in paper.get('questions', []):
            kbid = q.get('kbSourceId')
            if kbid not in TARGET_INDEX:
                continue
            target = TARGET_INDEX[kbid]
            current = q.get('correctIndex')
            if current == target:
                continue  # already at target

            # Apply pure swap: choices[current] <-> choices[target]
            new_choices = swap_choices(q['choices'], current, target)
            q['choices'] = new_choices
            q['correctIndex'] = target
            json_modified = True
            changes.append(f'paper-{paper_n}.json {q["id"]} ({kbid}): pos {current+1} -> {target+1}')

            # Apply same swap to MD block
            md_text, md_changed = apply_position_swap_in_md(
                md_text, kbid, new_choices, target,
            )
            if md_changed:
                md_modified = True
                changes.append(f'goi_questions_n5.md {kbid}: rewrote choice order to match (pos {target+1})')

        if json_modified:
            p_path.write_text(
                json.dumps(paper, ensure_ascii=False, indent=2),
                encoding='utf-8',
            )

    if md_modified:
        KB.write_text(md_text, encoding='utf-8')


def main() -> int:
    fix_q64_content()
    rebalance_positions()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
