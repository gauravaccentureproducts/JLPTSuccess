"""ISSUE-058 (audit round-7, 2026-05-06): backfill mondai field on
data/reading.json passages.

Pre-fix: mondai=null on all 40/40 passages.
Post-fix: mondai∈{4,5,6} based on length + format_type.

Heuristic:
  - format_type ∈ {schedule_table, menu_list, notice, poster} -> mondai 6
    (情報検索 = info-search; question tests locate-the-fact)
  - body length < 200 chars (kana-counted) -> mondai 4 (短文)
  - body length >= 200 -> mondai 5 (中文)

Idempotent: re-running detects existing mondai and skips.
"""
from __future__ import annotations
import io, json, sys
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
RF = ROOT / 'data' / 'reading.json'

INFO_SEARCH_FORMATS = {'schedule_table', 'menu_list', 'notice', 'poster', 'timetable', 'flyer'}


def assign_mondai(passage: dict) -> int:
    body = passage.get('ja') or passage.get('passage_ja') or passage.get('passage') or ''
    fmt = passage.get('format_type') or ''
    if fmt in INFO_SEARCH_FORMATS:
        return 6
    L = len(body)
    if L < 200:
        return 4
    return 5


def main() -> int:
    data = json.loads(RF.read_text(encoding='utf-8'))
    passages = data.get('passages', data.get('items', []))
    n_filled = 0
    n_unchanged = 0
    counts = Counter()
    for p in passages:
        proposed = assign_mondai(p)
        current = p.get('mondai')
        if current == proposed:
            n_unchanged += 1
        else:
            p['mondai'] = proposed
            n_filled += 1
        counts[proposed] += 1

    RF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Filled mondai on {n_filled} passages; {n_unchanged} unchanged.')
    print(f'Distribution: {dict(counts)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
