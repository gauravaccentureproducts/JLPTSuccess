"""ISSUE-059 (audit round-7, 2026-05-06): backfill `mondai` field on
data/papers/{moji,goi,bunpou,dokkai}/*.json questions.

Mapping derived from KnowledgeBank source-file documentation:
  moji   Q1-Q50   -> mondai 1 (漢字読み, kanji reading)
         Q51-Q100 -> mondai 2 (表記, orthography)
  goi    Q1-Q50   -> mondai 3 (文脈規定, context)
         Q51-Q100 -> mondai 4 (言い換え類義, paraphrase)
  bunpou Q1-Q60   -> mondai 1 (文の文法1, sentence grammar 1)
         Q61-Q90  -> mondai 2 (並べ替え, sentence composition)
         Q91-Q100 -> mondai 3 (文章の文法, text grammar)
  dokkai Q1-Q60   -> mondai 4 (短文, short passage)
         Q61-Q90  -> mondai 5 (中文, medium passage)
         Q91-Q102 -> mondai 6 (情報検索, information retrieval)

Pre-fix: mondai null on all 402 paper questions.
Post-fix: every question carries the correct mondai per its kbSourceId
(Q-number).

Idempotent.
"""
from __future__ import annotations
import io, json, sys, glob
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent


def kb_qnum(kb_source_id: str) -> int | None:
    """Extract the integer N from 'Q<N>' source ids. Returns None if
    the format is unexpected."""
    if not isinstance(kb_source_id, str):
        return None
    if kb_source_id.startswith('Q') and kb_source_id[1:].isdigit():
        return int(kb_source_id[1:])
    return None


def mondai_for(category: str, n: int) -> int | None:
    if category == 'moji':
        if 1 <= n <= 50: return 1
        if 51 <= n <= 100: return 2
    elif category == 'goi':
        if 1 <= n <= 50: return 3
        if 51 <= n <= 100: return 4
    elif category == 'bunpou':
        if 1 <= n <= 60: return 1
        if 61 <= n <= 90: return 2
        if 91 <= n <= 100: return 3
    elif category == 'dokkai':
        if 1 <= n <= 60: return 4
        if 61 <= n <= 90: return 5
        if 91 <= n <= 102: return 6
    return None


def main() -> int:
    overall = Counter()
    for category in ('moji', 'goi', 'bunpou', 'dokkai'):
        cat_counts = Counter()
        n_total = 0
        n_filled = 0
        n_no_match = 0
        for pf in sorted(glob.glob(str(ROOT / 'data' / 'papers' / category / '*.json'))):
            data = json.loads(Path(pf).read_text(encoding='utf-8'))
            for q in data.get('questions', []):
                n_total += 1
                kb = q.get('kbSourceId') or ''
                qn = kb_qnum(kb)
                if qn is None:
                    n_no_match += 1
                    continue
                m = mondai_for(category, qn)
                if m is None:
                    n_no_match += 1
                    continue
                if q.get('mondai') != m:
                    q['mondai'] = m
                    n_filled += 1
                cat_counts[m] += 1
            Path(pf).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'[{category}] {n_total} qs, filled {n_filled}, no-match {n_no_match}')
        print(f'           mondai dist: {dict(cat_counts)}')
        overall.update(cat_counts)
    print(f'\nOverall mondai distribution across all 4 categories:')
    print(f'  {dict(overall)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
