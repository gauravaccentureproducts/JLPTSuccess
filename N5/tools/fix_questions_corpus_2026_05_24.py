#!/usr/bin/env python3
"""
Audit + fix data/questions.json (290 items).

Native-teacher audit results (schema-aware):
  - MCQ (260): 260/260 well-formed
  - sentence_order (16): 16/16 well-formed
  - text_input (14): 14/14 well-formed

Real defects:
  - 6 schema-aware duplicate questions (same content, full-width vs
    half-width whitespace inside parens):
    q-0358 → dup of q-0019
    q-0421 → dup of q-0025
    q-0428 → dup of q-0034
    q-0429 → dup of q-0036
    q-0430 → dup of q-0038
    q-0530 → dup of q-0506

  - 3 questions with stale distractor_explanations keys (old choices
    no longer in current choices list):
    q-0022: de key 'と' not in [へ,は,や,で]
    q-0293: de key 'など' not in [か,だけ,に,や]
    q-0433: de keys 'こう','そう','ああ' not in [だれ,どう,いつ,どこ]

This script drops 6 dup questions and removes 5 stale distractor keys.
"""
import argparse
import json
import re
from pathlib import Path

QUESTIONS = Path('data/questions.json')
INDEX = Path('data/index.json')
FIX_LOG = Path('data/grammar.fix_log.json')

PROV = "auto_fix_2026_05_24"
AUDIT_WAVE = "claude_audit_2026_05_24"
REVIEW_STATUS = "ai_native_reviewer_2026_05_24"


def lf_size(path: Path) -> int:
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


DUP_DROP_IDS = ['q-0358', 'q-0421', 'q-0428', 'q-0429', 'q-0430', 'q-0530']

STALE_DISTRACTOR_KEYS = {
    'q-0022': ['と'],
    'q-0293': ['など'],
    'q-0433': ['こう', 'そう', 'ああ'],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    q = json.loads(QUESTIONS.read_text(encoding='utf-8'))
    items = q['questions']

    drop_log = []
    distractor_log = []

    # 1. Drop dup questions
    new_items = []
    for it in items:
        if it['id'] in DUP_DROP_IDS:
            drop_log.append({
                'dropped_id': it['id'],
                'question_ja': it.get('question_ja', '')[:80],
                'correctAnswer': it.get('correctAnswer'),
                'reason': 'schema-aware duplicate of earlier question (whitespace-only variant)',
            })
        else:
            new_items.append(it)
    q['questions'] = new_items

    # 2. Strip stale distractor_explanations keys
    for it in new_items:
        if it['id'] in STALE_DISTRACTOR_KEYS:
            stale_keys = STALE_DISTRACTOR_KEYS[it['id']]
            de = it.get('distractor_explanations') or {}
            removed = {}
            for k in stale_keys:
                if k in de:
                    removed[k] = de.pop(k)
            # Also strip from distractor_explanations_hi if present
            de_hi = it.get('distractor_explanations_hi') or {}
            removed_hi = {}
            for k in stale_keys:
                if k in de_hi:
                    removed_hi[k] = de_hi.pop(k)
            it['provenance'] = PROV
            it['audit_wave'] = AUDIT_WAVE
            it['review_status'] = REVIEW_STATUS
            it['reviewer_note'] = f'Stripped {len(removed)} stale distractor_explanations keys (no longer in choices).'
            distractor_log.append({
                'id': it['id'],
                'removed_keys': list(removed.keys()),
                'removed_keys_hi': list(removed_hi.keys()),
                'current_choices': it.get('choices'),
            })

    if '_meta' in q:
        q['_meta']['native_review_pass_2026_05_24'] = (
            f'Native-teacher audit + schema-aware dedup. '
            f'{len(drop_log)} duplicate questions dropped + '
            f'{len(distractor_log)} questions stripped of stale distractor_explanations keys.'
        )

    print(f'dup question drops: {len(drop_log)}')
    print(f'distractor stale-key strips: {len(distractor_log)} questions ({sum(len(d["removed_keys"]) for d in distractor_log)} keys)')

    if args.apply:
        QUESTIONS.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        idx = json.loads(INDEX.read_text(encoding='utf-8'))
        for entry in idx.get('files', []):
            if entry.get('path') == 'data/questions.json':
                entry['size_bytes'] = lf_size(QUESTIONS)
                break
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        log = json.loads(FIX_LOG.read_text(encoding='utf-8'))
        log['questions_corpus_audit_2026_05_24'] = {
            'description': (
                'Schema-aware audit of data/questions.json (290 items). 3 question types '
                'with distinct schemas: mcq (260), sentence_order (16), text_input (14). '
                'All 290 are well-formed for their respective schema. 6 schema-aware '
                'duplicates dropped + 5 stale distractor_explanations keys stripped.'
            ),
            'dup_drops': drop_log,
            'distractor_strips': distractor_log,
            'total_remaining': len(new_items),
        }
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'\napplied. questions.json LF size: {lf_size(QUESTIONS)}')
        print(f'remaining questions: {len(new_items)}')
    else:
        print('\n--dry-run')


if __name__ == '__main__':
    main()
