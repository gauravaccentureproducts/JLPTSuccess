#!/usr/bin/env python3
"""
Revert BUG-K boilerplate expansions.

Reviewer critique: BUG-K added a "This is a frequent N5 learner error ...
(See pattern detail page for full discussion.)" suffix to 25 wcp.why
rationales that were already crisp and complete. The expansion was
metric-gaming (≥6 tokens) at the cost of pedagogical quality.

This script reads the original why text from data/grammar.fix_log.json
BUG-K_wcp_thin_why section and restores each row's wcp.why to the
pre-expansion text.

Also adds an explicit reviewer_note acknowledging the revert.
"""
import argparse
import json
from pathlib import Path

GRAMMAR = Path('data/grammar.json')
INDEX = Path('data/index.json')
FIX_LOG = Path('data/grammar.fix_log.json')


def lf_size(path: Path) -> int:
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    log = json.loads(FIX_LOG.read_text(encoding='utf-8'))
    bug_k = log.get('BUG-K_wcp_thin_why', {})
    changes = bug_k.get('changes', [])
    if not changes:
        print('No BUG-K changes to revert.')
        return

    g = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns_by_id = {p['id']: p for p in g['patterns']}

    reverted = []
    for ch in changes:
        pid = ch['pattern']
        idx = ch['index']
        before_why = ch['before_why']
        if pid not in patterns_by_id:
            print(f'  WARN: pattern {pid} not found, skipping')
            continue
        p = patterns_by_id[pid]
        wcps = p.get('wrong_corrected_pair') or []
        if idx >= len(wcps):
            print(f'  WARN: {pid} wcp[{idx}] out of range, skipping')
            continue
        cur = wcps[idx].get('why', '')
        wcps[idx]['why'] = before_why
        wcps[idx]['reviewer_note'] = (
            'Reverted from BUG-K boilerplate expansion. Original crisp rationale '
            'restored. Reviewer flagged the expansion as metric-gaming (tautology + '
            'empty generality + broken self-reference); pedagogical quality dropped. '
            'See AUDIT-COVERAGE-2026-05-24.md Part 56.'
        )
        # Clear the audit_wave / review_status tags that were added by the expansion
        # (Keep provenance to preserve forensic chain)
        wcps[idx]['review_status'] = 'ai_native_reviewer_2026_05_24_reverted'
        reverted.append({
            'pattern': pid,
            'index': idx,
            'restored_why': before_why,
            'reverted_why': cur,
        })

    # Bump version
    g['_meta']['version'] = '2026.05.24-revert-bug-k'

    print(f'reverted {len(reverted)} wcp.why fields')

    if args.apply:
        out = json.dumps(g, ensure_ascii=False, indent=2)
        GRAMMAR.write_text(out + '\n', encoding='utf-8')

        idx_json = json.loads(INDEX.read_text(encoding='utf-8'))
        new_size = lf_size(GRAMMAR)
        for entry in idx_json.get('files', []):
            if entry.get('path') == 'data/grammar.json':
                entry['size_bytes'] = new_size
                break
        INDEX.write_text(json.dumps(idx_json, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        # Mark the revert in fix_log
        log['BUG-K_reverted'] = {
            'description': (
                'Reverted BUG-K boilerplate expansions. Reviewer (independent re-audit) '
                'flagged that the ≥6 token floor was metric-gaming and the expansions '
                'were tautological / self-referential / contained empty generality. '
                'Original crisp rationales restored.'
            ),
            'reverts': reverted,
            'lesson': (
                'Heuristic floors (token counts, char lengths) on quality dimensions are '
                'game-able and can DAMAGE quality if a fix-pass optimizes for the metric. '
                'Replace with content checks (presence of the rule and the correction in '
                'the text) or drop the heuristic entirely. See AUDIT-COVERAGE Part 56.'
            ),
        }
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        print(f'\napplied. grammar.json LF size: {new_size}')
    else:
        print('\n--dry-run')


if __name__ == '__main__':
    main()
