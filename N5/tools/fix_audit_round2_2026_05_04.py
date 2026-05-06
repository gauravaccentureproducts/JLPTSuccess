"""Audit round 2 (2026-05-04) - apply Fix-marked corpus changes.

Covers ISSUE-009 (backfill missing difficulty), ISSUE-010 (collapse
double-spaces in test stems), and IMP-023 housekeeping confirmation.

Idempotent.
"""
from __future__ import annotations
import io, json, re, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
QJSON = ROOT / 'data' / 'questions.json'

changes: list[str] = []


# ----------------------------------------------------------------------------
# ISSUE-009 - backfill `difficulty` on questions that lack it.
# Heuristic: difficulty = 1 (easiest) if `grammarPatternId` is in the first
# 60 lessons (n5-001 .. n5-060), 2 if 061..120, 3 if 121+ or marked late_n5.
# Fast and stable; subsequent hand-tuning is a separate workstream.
# ----------------------------------------------------------------------------

def backfill_difficulty():
    data = json.loads(QJSON.read_text(encoding='utf-8'))
    qs = data.get('questions', [])
    grammar = json.loads((ROOT / 'data/grammar.json').read_text(encoding='utf-8'))
    late_n5_ids = {p['id'] for p in grammar['patterns'] if p.get('tier') == 'late_n5'}

    n_filled = 0
    for q in qs:
        if 'difficulty' in q and q['difficulty'] is not None:
            continue
        pid = q.get('grammarPatternId') or ''
        m = re.match(r'n5-(\d+)', pid)
        n = int(m.group(1)) if m else 0
        if pid in late_n5_ids:
            d = 3
        elif 1 <= n <= 60:
            d = 1
        elif 61 <= n <= 120:
            d = 2
        elif n > 120:
            d = 3
        else:
            d = 2
        q['difficulty'] = d
        n_filled += 1
    if n_filled:
        QJSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changes.append(f'questions.json: backfilled difficulty on {n_filled} entries (ISSUE-009)')


# ----------------------------------------------------------------------------
# ISSUE-010 - collapse runs of >=2 ASCII spaces to single space in
# `question_ja` / `prompt_ja`. Preserves full-width spaces inside parens
# such as `（  ）` (these are JLPT blank markers and must stay paired).
# ----------------------------------------------------------------------------

def collapse_double_spaces():
    data = json.loads(QJSON.read_text(encoding='utf-8'))
    qs = data.get('questions', [])
    n_fixed = 0
    for q in qs:
        for field in ('question_ja', 'prompt_ja'):
            s = q.get(field)
            if not isinstance(s, str):
                continue
            # Replace runs of 2+ ASCII spaces with one. Full-width spaces
            # (U+3000) untouched - they live inside `（  ）` blank markers
            # and the JLPT convention pairs them.
            new = re.sub(r'(?<! ) {2,}(?! )', ' ', s)  # only inner runs
            new = re.sub(r' {2,}', ' ', new)            # any other run
            if new != s:
                q[field] = new
                n_fixed += 1
    if n_fixed:
        QJSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        changes.append(f'questions.json: collapsed double-spaces in {n_fixed} fields (ISSUE-010)')


def main() -> int:
    backfill_difficulty()
    collapse_double_spaces()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
