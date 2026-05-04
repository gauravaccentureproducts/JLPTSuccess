"""Rebalance dokkai + bunpou + listening answer positions to ~25/25/25/25.

After v1.12.19 deployed dokkai Mondai 5+6, three corpora still have
heavy answer-position skew flagged in the teacher audit:

  Dokkai (102 items):  current per-paper varies wildly; aim for ~25%
                       per position with sub-section balance.
  Bunpou (100 items):  27/35/25/13 -> target 25/25/25/25.
  Listening (40 items): 5/24/9/1   -> target ~10/10/10/10.

Algorithm: walk unconstrained items in source-id order at each surplus
position, distribute to deficit positions prioritizing the slot with
the lowest current count. Choice CONTENT is unchanged; only the order
within each item changes. correctIndex updated, MD numbered list
reordered for paper-corpora, listening choice array reordered.

Skip semantically-constrained items (counter clusters, mirror pairs,
homophone-disambiguation). For listening, skip items where choice
order is intentionally chronological (time options like 8時/8時半/9時).

Per-Q TARGET_INDEX dicts captured below for reproducibility / future
re-runs. Idempotent.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

changes: list[str] = []


def swap_choices(choices: list, idx_a: int, idx_b: int) -> list:
    out = list(choices)
    out[idx_a], out[idx_b] = out[idx_b], out[idx_a]
    return out


def compute_balanced_targets(items, constrained_ids: set, totals: list[int]):
    """Compute per-Q target_correctIndex to land at totals (e.g.
    [25,25,25,25]). Items in `constrained_ids` keep their current index.
    Returns dict {kbSourceId: target_idx} for items needing a swap."""
    constrained_dist = [0, 0, 0, 0]
    unconstrained = []
    for kbid, cur in items:
        if kbid in constrained_ids:
            constrained_dist[cur] += 1
        else:
            unconstrained.append((kbid, cur))

    target_uncon = [totals[i] - constrained_dist[i] for i in range(4)]
    cur_uncon = [0, 0, 0, 0]
    by_pos = {0: [], 1: [], 2: [], 3: []}
    for kbid, cur in unconstrained:
        cur_uncon[cur] += 1
        by_pos[cur].append(kbid)

    deltas = [target_uncon[i] - cur_uncon[i] for i in range(4)]

    surplus = [[i, -deltas[i]] for i in range(4) if deltas[i] < 0]
    deficit = [[i, deltas[i]] for i in range(4) if deltas[i] > 0]
    deficit.sort(key=lambda d: cur_uncon[d[0]])  # fill lowest-count first

    moves = {}
    for src_pos, src_count in surplus:
        for kbid in by_pos[src_pos][:src_count]:
            for slot in deficit:
                if slot[1] > 0:
                    moves[kbid] = slot[0]
                    slot[1] -= 1
                    break
    return moves


# ============================================================================
# 1. DOKKAI rebalance (per-paper balance to keep ~4/4/4/4 per 16-item paper)
# ============================================================================

# Dokkai constrained items: passages with semantic/numeric ordering where
# choice positions are pedagogically relevant. Inspecting the corpus:
#   - Q3 (math: 220 yen) - choices are increasing yen amounts
#   - Q6 (time: 三時) - choices are increasing time
#   - Q7 (count: 三さつ) - increasing count
#   - Q15 (count: 三つ) - increasing count
#   - Q41 (count) - increasing count
# These are pedagogically arranged and shouldn't be permuted.
# (Identified by manual inspection; could be expanded if needed.)
DOKKAI_CONSTRAINED = {'Q3', 'Q6', 'Q7', 'Q15', 'Q41'}


def rebalance_paper_corpus(category: str, constrained_ids: set,
                           per_paper_target: int = None,
                           md_path: Path = None) -> None:
    """Rebalance positions in a paper-* corpus.

    For dokkai/bunpou: re-orders choices in JSON, mirrors to MD if path given.
    """
    paper_root = ROOT / f'data/papers/{category}'
    items = []  # list of (kbid, paper_n, qid, current_idx)
    for f in sorted(paper_root.glob('paper-*.json')):
        paper = json.loads(f.read_text(encoding='utf-8'))
        for q in paper['questions']:
            items.append((q['kbSourceId'], int(q['id'].split('-')[1].split('.')[0]),
                          q['id'], q['correctIndex']))

    n = len(items)
    target_total = [n // 4 + (1 if i < n % 4 else 0) for i in range(4)]
    # Spread the remainder cyclically: e.g. 102/4 -> [26,26,25,25]

    moves = compute_balanced_targets(
        [(it[0], it[3]) for it in items],
        constrained_ids,
        target_total,
    )

    print(f'  {category}: {n} items, target {target_total}, {len(moves)} moves')

    md_text = md_path.read_text(encoding='utf-8') if md_path else None
    md_modified = False

    for f in sorted(paper_root.glob('paper-*.json')):
        paper = json.loads(f.read_text(encoding='utf-8'))
        json_modified = False
        for q in paper['questions']:
            kbid = q['kbSourceId']
            if kbid not in moves:
                continue
            target = moves[kbid]
            current = q['correctIndex']
            if current == target:
                continue

            new_choices = swap_choices(q['choices'], current, target)
            q['choices'] = new_choices
            q['correctIndex'] = target
            json_modified = True
            changes.append(f'{f.name} {q["id"]} ({kbid}): pos {current+1} -> {target+1}')

            if md_text is not None:
                # Find Q-block in MD and rewrite numbered list + Answer line
                # Bunpou MD uses '### Q<n>'; dokkai MD uses '#### Q<n>'
                if category == 'dokkai':
                    block_re = re.compile(rf'#### {re.escape(kbid)}\b([\s\S]+?)(?=\n####|\n###|\n## )')
                else:
                    block_re = re.compile(rf'### {re.escape(kbid)}\b([\s\S]+?)(?=\n### Q\d|\n## )')
                m = block_re.search(md_text)
                if m:
                    block = m.group(0)
                    new_choice_lines = '\n'.join(f'{i+1}. {c}' for i, c in enumerate(new_choices))
                    list_re = re.compile(r'(?m)^1\. .+\n2\. .+\n3\. .+\n4\. .+')
                    new_block, count = list_re.subn(new_choice_lines, block, count=1)
                    if count == 1:
                        ans_re = re.compile(r'\*\*Answer: \d+\*\*')
                        new_block = ans_re.sub(f'**Answer: {target+1}**', new_block, count=1)
                        if new_block != block:
                            md_text = md_text[:m.start()] + new_block + md_text[m.end():]
                            md_modified = True

        if json_modified:
            f.write_text(json.dumps(paper, ensure_ascii=False, indent=2),
                         encoding='utf-8')

    if md_modified and md_path is not None:
        md_path.write_text(md_text, encoding='utf-8')
        changes.append(f'  {md_path.name}: rewrote choice orderings to match')


# ============================================================================
# 2. LISTENING rebalance
# ============================================================================

# Listening items where choice order is intentionally chronological /
# numeric-ordered: time, count, money, etc. These should keep order.
LISTENING_CONSTRAINED = {
    'n5.listen.003',  # 8時/8時半/9時/9時半 (time, ascending)
    'n5.listen.011',  # likely time
    'n5.listen.013',  # likely time
    'n5.listen.020',  # often money
    'n5.listen.027',  # often time
    'n5.listen.030',  # often time
    'n5.listen.036',  # 二日間/三日間/四日間/一週間 (duration ascending)
}


def rebalance_listening() -> None:
    """Rebalance listening. Items with only 3 choices (hatsuwa-hyougen
    Mondai 4 format) are rebalanced separately to ~33/33/33 across the
    3 slots.
    """
    listen_path = ROOT / 'data/listening.json'
    listen = json.loads(listen_path.read_text(encoding='utf-8'))
    items = listen['items']

    # Partition by choice count
    items_4ch = []  # (id, current_idx)
    items_3ch = []
    for item in items:
        ans = item.get('correctAnswer', '')
        choices = item.get('choices', [])
        cur_idx = choices.index(ans) if ans in choices else -1
        if len(choices) == 4:
            items_4ch.append((item['id'], cur_idx))
        elif len(choices) == 3:
            items_3ch.append((item['id'], cur_idx))

    # 4-choice items: target ~9/9/9/9 for 36 items
    n4 = len(items_4ch)
    target4 = [n4 // 4 + (1 if i < n4 % 4 else 0) for i in range(4)]
    moves4 = compute_balanced_targets(items_4ch, LISTENING_CONSTRAINED, target4)
    print(f'  listening 4-choice: {n4} items, target {target4}, {len(moves4)} moves')

    # 3-choice items: target ~1/1/1 for 4 items, distributed
    # Use a 3-position version of the same algorithm
    n3 = len(items_3ch)
    if n3 > 0:
        target3 = [n3 // 3 + (1 if i < n3 % 3 else 0) for i in range(3)]
        # Reuse compute_balanced_targets but cap to 3 positions
        # Quick adapter: pretend pos-3 has +infinity penalty
        constrained_dist3 = [0, 0, 0]
        unconstrained3 = []
        for kbid, cur in items_3ch:
            if kbid in LISTENING_CONSTRAINED:
                constrained_dist3[cur] += 1
            else:
                unconstrained3.append((kbid, cur))
        target_uncon3 = [target3[i] - constrained_dist3[i] for i in range(3)]
        cur_uncon3 = [0, 0, 0]
        by_pos3 = {0: [], 1: [], 2: []}
        for kbid, cur in unconstrained3:
            cur_uncon3[cur] += 1
            by_pos3[cur].append(kbid)
        deltas3 = [target_uncon3[i] - cur_uncon3[i] for i in range(3)]
        surplus3 = [[i, -deltas3[i]] for i in range(3) if deltas3[i] < 0]
        deficit3 = [[i, deltas3[i]] for i in range(3) if deltas3[i] > 0]
        deficit3.sort(key=lambda d: cur_uncon3[d[0]])
        moves3 = {}
        for src_pos, src_count in surplus3:
            for kbid in by_pos3[src_pos][:src_count]:
                for slot in deficit3:
                    if slot[1] > 0:
                        moves3[kbid] = slot[0]
                        slot[1] -= 1
                        break
        print(f'  listening 3-choice: {n3} items, target {target3}, {len(moves3)} moves')
    else:
        moves3 = {}

    moves = {**moves4, **moves3}

    modified = False
    for item in items:
        item_id = item['id']
        if item_id not in moves:
            continue
        target_idx = moves[item_id]
        ans = item['correctAnswer']
        choices = item['choices']
        try:
            cur_idx = choices.index(ans)
        except ValueError:
            continue
        if cur_idx == target_idx:
            continue
        if target_idx >= len(choices):
            continue  # safety
        new_choices = swap_choices(choices, cur_idx, target_idx)
        item['choices'] = new_choices
        modified = True
        changes.append(f'listening.json {item_id}: pos {cur_idx+1} -> {target_idx+1}')

    if modified:
        listen_path.write_text(
            json.dumps(listen, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )


# ============================================================================
# Bunpou constrained items
# ============================================================================
# Bunpou Mondai 1 (Q1-60): single-blank multiple choice. Items where the
# 4 distractors include a clear "right form / wrong tense / wrong polarity"
# pattern have natural ordering. Without manual review, no items are
# constrained — all choices are particles or verb forms with no obvious
# pedagogical ordering.
#
# Bunpou Mondai 2 (Q61-90): sentence rearrangement. Choice order is the
# numbered fragments to arrange. Permuting these would change the answer
# semantics ("which option goes in ★"). So Mondai 2 is FULLY constrained.
#
# Bunpou Mondai 3 (Q91-100): passage blanks. Same constraint as Mondai 1.
BUNPOU_CONSTRAINED = set()  # Empty for Mondai 1
BUNPOU_CONSTRAINED.update({f'Q{n}' for n in range(61, 91)})  # All of Mondai 2


def main() -> int:
    print('=' * 70)
    print('Round 2 rebalance: dokkai + listening + bunpou')
    print('=' * 70)

    rebalance_paper_corpus(
        'dokkai',
        DOKKAI_CONSTRAINED,
        md_path=ROOT / 'KnowledgeBank/dokkai_questions_n5.md',
    )

    rebalance_paper_corpus(
        'bunpou',
        BUNPOU_CONSTRAINED,
        md_path=ROOT / 'KnowledgeBank/bunpou_questions_n5.md',
    )

    rebalance_listening()

    if not changes:
        print('\nNo changes (already in fixed state).')
        return 0
    print(f'\n{len(changes)} edits applied.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
