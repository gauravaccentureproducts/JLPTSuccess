"""ISSUE-104: Add `format_role` field on all 45 N5 reading passages.

Per the N5Improvement.txt audit prompt's reading section (JA-29
adjacent), each passage carries a closed-enum `format_role` that
distinguishes the question-purpose variant within the mondai:

  - "primary"        — main reading content (tested for comprehension)
  - "supplementary"  — supports a primary item (e.g., a poster
                       referenced in a question; not tested directly)
  - "info_search"    — mondai-6 information-search format (timetable,
                       schedule, menu, notice)
  - "self_intro"     — self-introduction style passages (mondai-4 only)
  - "narrative"      — first-person narrative

Default mapping (per mondai + format_type):
  mondai-6                      -> info_search
  mondai-5                      -> narrative
  mondai-4 + format_type=schedule_table / menu_list / notice
                                -> info_search (data-style)
  mondai-4 + topic=self-introduction
                                -> self_intro
  mondai-4 + everything else    -> primary

Idempotent.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READING = ROOT / 'data' / 'reading.json'


def assign_format_role(p: dict) -> str:
    mondai = p.get('mondai')
    format_type = p.get('format_type')
    topic = (p.get('topic') or '').lower()

    if mondai == 6:
        return 'info_search'
    if mondai == 5:
        return 'narrative'
    # mondai-4 disambiguation
    if format_type in ('schedule_table', 'menu_list', 'notice'):
        return 'info_search'
    if 'self-introduction' in topic or 'self_intro' in topic:
        return 'self_intro'
    return 'primary'


def main():
    with READING.open('r', encoding='utf-8') as f:
        data = json.load(f)
    passages = data['passages']
    matched = 0
    skipped = 0
    distribution: dict[str, int] = {}
    for p in passages:
        if p.get('format_role'):
            skipped += 1
            distribution[p['format_role']] = distribution.get(p['format_role'], 0) + 1
            continue
        role = assign_format_role(p)
        p['format_role'] = role
        matched += 1
        distribution[role] = distribution.get(role, 0) + 1
    print(f'Set format_role on {matched} passages.')
    print(f'Skipped (already had value): {skipped}')
    print(f'Final distribution: {distribution}')
    with READING.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
