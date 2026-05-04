"""Apply 1st-pass moji review fixes (5 item-level + 37 permutation rebalance).

Reviewer flagged the moji corpus on first pass:

(1) One major must-fix: answer-position distribution 56/31/12/1 ->
    target ~25/25/25/25, with sub-section balance so neither Mondai
    has an anomaly (Mondai 1 was 27/15/7/1, Mondai 2 was 29/16/5/0
    with zero D answers).

(2) Five polish-grade item fixes:
    Q19   stem 「今年は さむいです」 reads slightly oddly (さむい is a
          moment, not a year-long state). Rewrite stem to anchor
          to ふゆ: 「今年の ふゆは さむいです」.
    Q55   Add jukujikun acknowledgement to rationale - 大人/おとな
          is a semantic compound reading; the kanji are N5 but the
          compound is irregular.
    Q57   Add note that distractor 妹 is not in the kanji whitelist
          (recognition-only distractor per moji-corpus kanji-scope
          exception).
    Q78   Add semantic-distractor explanation - the 通/路/行
          alternatives are family-of-meaning N4+ kanji.
    Q92   Strengthen rationale wording on the 起/経/建 trap - those
          are real verbs also read たちます but N3+ in scope.

Skip semantic-constrained items in the rebalance:
    Q54 力, Q55 大人, Q59 人, Q73 午前, Q79 駅, Q89 行きます/生きます,
    Q92 立ちます, Q93 休, Q95 買います/飼います, Q99 白
    These have carefully-arranged choice orders (visual-confusion
    2x2 grids, homophone-disambiguation pairs) that would lose
    pedagogical value if shuffled.

Per-section targets after rebalance:
    Mondai 1 (Q1-50):   13/13/12/12 = 50
    Mondai 2 (Q51-100): 12/12/13/13 = 50
    Global total:        25/25/25/25

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
KB = ROOT / 'KnowledgeBank' / 'moji_questions_n5.md'
PAPERS = ROOT / 'data' / 'papers' / 'moji'

changes: list[str] = []


# ---------------------------------------------------------------------------
# Item-level fixes (rationale tweaks + Q19 stem rewrite)
# ---------------------------------------------------------------------------

ITEM_FIXES = {
    # Q19 / moji-2.4: stem rewrite (anchor さむい to ふゆ for naturalness)
    (2, 'moji-2.4'): {
        'stem_html': '<u>今年</u>の ふゆは さむいです。',
        'rationale': '今年 is read ことし (irregular jukujikun reading).',
    },

    # Q55 / moji-4.10: jukujikun acknowledgement
    (4, 'moji-4.10'): {
        'rationale': '大人 (おとな - adult). Jukujikun (semantic compound reading): the kanji 大 and 人 are individually N5, but the compound reading おとな is irregular. The compound is documented as an N5 vocab entry in vocabulary_n5.md; the irregular-reading pattern is standard for N5 family/age vocabulary.',
    },

    # Q57 / moji-4.12: distractor 妹 not in whitelist note
    (4, 'moji-4.12'): {
        'rationale': '母 (mother). Note: distractor 妹 is not in the kanji whitelist - it appears as a recognition-only distractor per the moji-corpus kanji-scope exception (Mondai 2 distractors may use non-whitelist kanji where authentic JLPT format requires it). Students do not need to read 妹 to reject it; family-relation kanji shape suffices.',
    },

    # Q78 / moji-6.3: semantic-distractor explanation
    (6, 'moji-6.3'): {
        'rationale': '道 (みち - road, way). 道 is whitelisted N5 (kanji whitelist line 98) and listed at vocabulary_n5.md. The distractors 通 / 路 / 行 are family-of-meaning alternatives commonly seen in N4+ vocabulary (通る / 通り pass through, 道路 / 路上 road, 行く go). The semantic-distractor design tests whether the student knows 道 specifically rather than just recognizing the "road / way" semantic field.',
    },

    # Q92 / moji-7.2: strengthen trap wording
    (7, 'moji-7.2'): {
        'rationale': '立ちます (stand up - the everyday N5 sense of たつ). The other forms 起ちます / 経ちます / 建ちます are real Japanese verbs also read たちます (rise up / time passes / a building stands) but are N3+ in scope. Broader-exposure students should not be misled by the polysemy; for N5 the 立 form is the only correct match for "students stand up when the teacher enters".',
    },
}


def update_paper_jsons() -> None:
    for (paper_n, qid), updates in ITEM_FIXES.items():
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


# MD blocks for the item-level fixes (rationale tweaks + Q19 stem rewrite)
MD_REPLACEMENTS = {
    'Q19': '''### Q19

<u>今年</u>の ふゆは さむいです。

1. こんねん
2. ことし
3. いまとし
4. きんねん

**Answer: 2** - 今年 is read ことし (irregular jukujikun reading).''',

    'Q55': '''### Q55

この えいがは __おとな__ から 子どもまで みんな たのしめます。

1. 大人
2. 太人
3. 大入
4. 太入

**Answer: 1** - 大人 (おとな - adult). Jukujikun (semantic compound reading): the kanji 大 and 人 are individually N5, but the compound reading おとな is irregular. The compound is documented as an N5 vocab entry in vocabulary_n5.md; the irregular-reading pattern is standard for N5 family/age vocabulary.''',

    'Q57': '''### Q57

__はは__ は 学校の 先生です。

1. 父
2. 妹
3. 母
4. 友

**Answer: 3** - 母 (mother). Note: distractor 妹 is not in the kanji whitelist - it appears as a recognition-only distractor per the moji-corpus kanji-scope exception (Mondai 2 distractors may use non-whitelist kanji where authentic JLPT format requires it). Students do not need to read 妹 to reject it; family-relation kanji shape suffices.''',

    'Q92': '''### Q92

先生が きょうしつに 来たので、学生が __たちます__。

1. 立ちます
2. 起ちます
3. 経ちます
4. 建ちます

**Answer: 1** - 立ちます (stand up - the everyday N5 sense of たつ). The other forms 起ちます / 経ちます / 建ちます are real Japanese verbs also read たちます (rise up / time passes / a building stands) but are N3+ in scope. Broader-exposure students should not be misled by the polysemy; for N5 the 立 form is the only correct match for "students stand up when the teacher enters".''',

    # Q78 written here with the POST-permutation choice order (rebalance
    # moves keyed A -> C, so 道 lands at position 3). Both item-fix and
    # rebalance produce the same final state -> idempotent.
    'Q78': '''### Q78

がっこうへ いく __みち__ で 友だちに あいました。

1. 路
2. 通
3. 道
4. 行

**Answer: 3** - 道 (みち - road, way). 道 is whitelisted N5 (kanji whitelist line 98) and listed at vocabulary_n5.md. The distractors 通 / 路 / 行 are family-of-meaning alternatives commonly seen in N4+ vocabulary (通る / 通り pass through, 道路 / 路上 road, 行く go). The semantic-distractor design tests whether the student knows 道 specifically rather than just recognizing the "road / way" semantic field.''',
}


def update_md_item_fixes() -> None:
    text = KB.read_text(encoding='utf-8')
    original_text = text
    for qnum, replacement in MD_REPLACEMENTS.items():
        block_re = re.compile(
            rf'### {re.escape(qnum)}\b[\s\S]+?(?=\n### Q\d|\n## )'
        )
        m = block_re.search(text)
        if m is None:
            changes.append(f'moji_questions_n5.md {qnum}: NOT FOUND (skipped)')
            continue
        if m.group(0).strip() == replacement.strip():
            continue
        text = text[:m.start()] + replacement + '\n' + text[m.end():]
        changes.append(f'moji_questions_n5.md {qnum}: replaced block (item fix)')
    if text != original_text:
        KB.write_text(text, encoding='utf-8')


# ---------------------------------------------------------------------------
# Position rebalance (37 permutations; per-section balanced)
# Computed by tools/compute_moji_rebalance_plan.py
# ---------------------------------------------------------------------------

TARGET_INDEX = {
    # Mondai 1 (Q1-50): A->D (11), A->C (3), B->C (2)
    'Q5': 3, 'Q6': 3, 'Q9': 3, 'Q11': 3, 'Q13': 3, 'Q15': 3,
    'Q18': 3, 'Q21': 3, 'Q23': 3, 'Q26': 3, 'Q28': 3,
    'Q33': 2, 'Q36': 2, 'Q37': 2,
    'Q1': 2, 'Q2': 2,

    # Mondai 2 (Q51-100): A->D (13), A->C (4), B->C (4)
    'Q52': 3, 'Q53': 3, 'Q58': 3, 'Q60': 3,
    'Q62': 3, 'Q63': 3, 'Q65': 3, 'Q66': 3, 'Q67': 3,
    'Q70': 3, 'Q71': 3, 'Q75': 3, 'Q77': 3,
    'Q78': 2, 'Q81': 2, 'Q83': 2, 'Q85': 2,
    'Q51': 2, 'Q56': 2, 'Q61': 2, 'Q64': 2,
}


def swap_choices(choices: list, idx_a: int, idx_b: int) -> list:
    out = list(choices)
    out[idx_a], out[idx_b] = out[idx_b], out[idx_a]
    return out


def apply_position_swap_in_md(text: str, qnum: str, new_choices: list,
                              new_correct_index: int) -> tuple[str, bool]:
    """Rewrite the MD block for `qnum` with the new ordered choices and
    answer line. Preserves stem and rationale text."""
    block_re = re.compile(rf'### {re.escape(qnum)}\b([\s\S]+?)(?=\n### Q\d|\n## )')
    m = block_re.search(text)
    if not m:
        changes.append(f'moji_questions_n5.md {qnum}: NOT FOUND (skipped)')
        return text, False
    block = m.group(0)

    new_choice_lines = '\n'.join(f'{i+1}. {c}' for i, c in enumerate(new_choices))

    list_re = re.compile(r'(?m)^1\. .+\n2\. .+\n3\. .+\n4\. .+')
    new_block, n = list_re.subn(new_choice_lines, block, count=1)
    if n != 1:
        changes.append(f'moji_questions_n5.md {qnum}: choice list pattern not found (skipped)')
        return text, False

    answer_re = re.compile(r'\*\*Answer: \d+\*\*')
    new_block, n2 = answer_re.subn(f'**Answer: {new_correct_index+1}**', new_block, count=1)
    if n2 != 1:
        changes.append(f'moji_questions_n5.md {qnum}: Answer line not found (skipped)')
        return text, False

    if new_block == block:
        return text, False
    return text[:m.start()] + new_block + text[m.end():], True


def rebalance_positions() -> None:
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
                continue

            new_choices = swap_choices(q['choices'], current, target)
            q['choices'] = new_choices
            q['correctIndex'] = target
            json_modified = True
            changes.append(f'paper-{paper_n}.json {q["id"]} ({kbid}): pos {current+1} -> {target+1}')

            md_text, md_changed = apply_position_swap_in_md(
                md_text, kbid, new_choices, target,
            )
            if md_changed:
                md_modified = True
                changes.append(f'moji_questions_n5.md {kbid}: rewrote choice order to match (pos {target+1})')

        if json_modified:
            p_path.write_text(
                json.dumps(paper, ensure_ascii=False, indent=2),
                encoding='utf-8',
            )

    if md_modified:
        KB.write_text(md_text, encoding='utf-8')


def main() -> int:
    update_md_item_fixes()
    update_paper_jsons()
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
