"""Iteration 4: global-aware rebalance for moji and goi.

Iter 1 used per-paper target [4,4,4,3] uniformly, which produces total
distribution skew when constrained items concentrate at certain positions
(moji + goi have constrained-item clusters at A/B, leaving D=20 globally).

This pass:
- Measures constrained-position distribution per corpus
- Computes unconstrained-only target to compensate
- Re-rebalances unconstrained items globally to achieve corpus-wide
  25/25/25/25 (within ±1)

Idempotent.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

CONSTRAINED_BY_CAT = {
    'moji': {'Q54','Q55','Q59','Q73','Q79','Q89','Q92','Q93','Q95','Q99'},
    'goi': {'Q38','Q39','Q40','Q41','Q64','Q73','Q83','Q92'},
    'bunpou': set(f'Q{n}' for n in range(61, 91)),  # Mondai 2 fully constrained
    'dokkai': {'Q3','Q6','Q7','Q15','Q41'},
}

changes: list[str] = []


def rebalance_corpus_globally(cat: str) -> None:
    """For a corpus, re-permute unconstrained items so global distribution
    is uniform (25/25/25/25 for 100 items)."""
    constrained = CONSTRAINED_BY_CAT[cat]

    # Read all questions across all papers
    paper_files = sorted((ROOT / f'data/papers/{cat}').glob('paper-*.json'))
    all_papers = {f.name: json.loads(f.read_text(encoding='utf-8')) for f in paper_files}

    # Catalog
    items = []  # (paper_name, q_index_in_paper, q_obj)
    for pname, paper in all_papers.items():
        for i, q in enumerate(paper['questions']):
            items.append((pname, i, q))

    n = len(items)
    target_total = [n // 4 + (1 if i < n % 4 else 0) for i in range(4)]  # 25/25/25/25 for 100

    # Constrained items keep position
    constrained_dist = [0,0,0,0]
    unconstrained = []
    for pname, qi, q in items:
        if q['kbSourceId'] in constrained:
            constrained_dist[q['correctIndex']] += 1
        else:
            unconstrained.append((pname, qi, q))

    target_uncon = [target_total[i] - constrained_dist[i] for i in range(4)]
    cur_uncon = [0,0,0,0]
    for _, _, q in unconstrained:
        cur_uncon[q['correctIndex']] += 1

    deltas = [target_uncon[i] - cur_uncon[i] for i in range(4)]
    surplus = [[i, -d] for i, d in enumerate(deltas) if d < 0]
    deficit = [[i, d] for i, d in enumerate(deltas) if d > 0]
    deficit.sort(key=lambda d: cur_uncon[d[0]])

    if not surplus or not deficit:
        print(f'  {cat}: already balanced (constrained={constrained_dist}, current uncon={cur_uncon}, target uncon={target_uncon})')
        return

    print(f'  {cat}: rebalancing — constrained={constrained_dist}, cur_uncon={cur_uncon}, target_uncon={target_uncon}, deltas={deltas}')

    # Group unconstrained by current pos
    by_pos = {0:[], 1:[], 2:[], 3:[]}
    for entry in unconstrained:
        by_pos[entry[2]['correctIndex']].append(entry)

    # Pick items to move
    moves = []  # (entry, target_idx)
    for src_pos, src_count in surplus:
        # Sort items at src_pos by Q-number for determinism
        sorted_items = sorted(by_pos[src_pos], key=lambda e: int(e[2]['kbSourceId'][1:]))
        for entry in sorted_items[:src_count]:
            for slot in deficit:
                if slot[1] > 0:
                    moves.append((entry, slot[0]))
                    slot[1] -= 1
                    break

    # Apply moves
    md_path = ROOT / f'KnowledgeBank/{cat}_questions_n5.md'
    md_text = md_path.read_text(encoding='utf-8')

    for entry, target_idx in moves:
        pname, qi, q = entry
        cur_idx = q['correctIndex']
        if cur_idx == target_idx:
            continue
        new_choices = list(q['choices'])
        new_choices[cur_idx], new_choices[target_idx] = new_choices[target_idx], new_choices[cur_idx]
        q['choices'] = new_choices
        q['correctIndex'] = target_idx
        changes.append(f'{cat}/{pname} {q["id"]} ({q["kbSourceId"]}): {cur_idx+1} -> {target_idx+1}')

        # Mirror to MD
        kbid = q['kbSourceId']
        for prefix in ['#### ', '### ']:
            block_re = re.compile(rf'{re.escape(prefix)}{re.escape(kbid)}\b([\s\S]+?)(?=\n#{{3,4}} Q\d|\n## )')
            m = block_re.search(md_text)
            if m:
                block = m.group(0)
                new_lines = '\n'.join(f'{i+1}. {c}' for i, c in enumerate(new_choices))
                list_re = re.compile(r'(?m)^1\. .+\n2\. .+\n3\. .+\n4\. .+')
                new_block, count = list_re.subn(new_lines, block, count=1)
                if count == 1:
                    new_block = re.sub(r'\*\*Answer: \d+\*\*', f'**Answer: {target_idx+1}**', new_block, count=1)
                    if new_block != block:
                        md_text = md_text[:m.start()] + new_block + md_text[m.end():]
                break

    # Save papers
    for pname, paper in all_papers.items():
        p_path = ROOT / f'data/papers/{cat}/{pname}'
        p_path.write_text(json.dumps(paper, ensure_ascii=False, indent=2), encoding='utf-8')

    md_path.write_text(md_text, encoding='utf-8')


def main() -> int:
    for cat in ['moji', 'goi', 'bunpou', 'dokkai']:
        rebalance_corpus_globally(cat)
    if not changes:
        print('No changes (already balanced).')
        return 0
    print(f'\n{len(changes)} edits applied.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
