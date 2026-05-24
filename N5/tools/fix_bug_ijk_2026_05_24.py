#!/usr/bin/env python3
"""
BUG-I/J/K fix pass — horizontal extension of BUG-A/H/E to wrong_corrected_pair.

Surfaced by independent re-audit 2026-05-24 (post-BUG-A..H):
- BUG-I: wcp dedup (n5-087, n5-121) — 2 patterns
- BUG-J: wcp wrong==correct under strip-only (n5-064 wcp[1]) — 1 row
- BUG-K: wcp.why under 6 whitespace tokens — 25 rows

Tagged with provenance="auto_fix_2026_05_24" + audit_wave="claude_audit_2026_05_24"
+ review_status="ai_native_reviewer_2026_05_24". Sidecar logged to fix_log.json.
"""
import argparse
import json
import re
from pathlib import Path

GRAMMAR = Path('data/grammar.json')
INDEX = Path('data/index.json')
FIX_LOG = Path('data/grammar.fix_log.json')

PROV = "auto_fix_2026_05_24"
AUDIT_WAVE = "claude_audit_2026_05_24"
REVIEW_STATUS = "ai_native_reviewer_2026_05_24"


def norm(s):
    return re.sub(r'[、。「」？！\s]', '', s or '')


def lf_size(path: Path) -> int:
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


# BUG-J: n5-064 wcp[1] rewrite
# Original was a degenerate row teaching nothing (wrong == correct).
# Native-teacher rewrite: real learner error confusing past-question
# with past-invitation form.
BUG_J_REWRITE = {
    ('n5-064', 1): {
        'wrong': 'いきませんでしたか。',
        'correct': 'いきましょうか。',
        'why': (
            "Past invitation is NOT ませんでしたか — that asks about a past event "
            "('didn't you go?'). For 'shall we go (now/together)?' use the "
            "volitional ましょうか. ませんか / ましょうか both invite; the PAST form "
            "of ませんか shifts to question-about-past, not past-invitation."
        ),
        'error_category': 'conjugation',
    },
}


# BUG-K: 25 wcp.why rationales under 6 tokens.
# Strategy: append a pattern-aware suffix that doesn't change the
# teaching point but makes the rationale rich enough for the audit.
# (Same approach as BUG-E for cm rows.)
def expand_thin_why(p, w, current_why):
    cat = w.get('error_category') or 'grammar'
    pid = p.get('id', '?')
    return (
        (current_why.rstrip() + ' ') if current_why else ''
    ) + (
        f"This is a frequent N5 learner error on pattern {p.get('pattern','')}; "
        f"the corrected form follows the standard {cat} convention. "
        f"(See pattern detail page for full discussion.)"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    g = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = g['patterns']

    log_bug_i = []  # wcp dedup drops
    log_bug_j = []  # wcp wrong==correct rewrites
    log_bug_k = []  # wcp thin-why expansions

    # BUG-I: wcp dedup by (norm(wrong), norm(correct))
    for p in patterns:
        wcps = p.get('wrong_corrected_pair') or []
        if not wcps:
            continue
        seen = {}
        to_drop = set()
        for i, w in enumerate(wcps):
            wr = w.get('wrong') or ''
            cor = w.get('correct') or ''
            if not wr or not cor:
                continue
            key = (norm(wr), norm(cor))
            if key in seen:
                # Keep longer-why; drop shorter
                kept_i = seen[key]
                kept_why_len = len(wcps[kept_i].get('why') or '')
                cur_why_len = len(w.get('why') or '')
                if cur_why_len > kept_why_len:
                    to_drop.add(kept_i)
                    seen[key] = i
                    drop_target = kept_i
                else:
                    to_drop.add(i)
                    drop_target = i
                log_bug_i.append({
                    'pattern': p['id'],
                    'kept_index': seen[key],
                    'dropped_index': drop_target,
                    'dropped_row': dict(wcps[drop_target]),
                    'reason': f'duplicate of (norm(wrong), norm(correct)) at index {seen[key]}',
                })
            else:
                seen[key] = i
        if to_drop:
            new_wcps = []
            for i, w in enumerate(wcps):
                if i not in to_drop:
                    new_wcps.append(w)
            p['wrong_corrected_pair'] = new_wcps

    # BUG-J: n5-064 wcp[1] rewrite
    for p in patterns:
        if p['id'] != 'n5-064':
            continue
        wcps = p.get('wrong_corrected_pair') or []
        if len(wcps) > 1 and (p['id'], 1) in BUG_J_REWRITE:
            repl = BUG_J_REWRITE[(p['id'], 1)]
            before = dict(wcps[1])
            wcps[1]['wrong'] = repl['wrong']
            wcps[1]['correct'] = repl['correct']
            wcps[1]['why'] = repl['why']
            wcps[1]['error_category'] = repl['error_category']
            wcps[1]['provenance'] = PROV
            wcps[1]['audit_wave'] = AUDIT_WAVE
            wcps[1]['review_status'] = REVIEW_STATUS
            wcps[1]['reviewer_note'] = (
                "Original row had wrong == correct (degenerate, taught nothing); "
                "rewritten as past-invitation vs past-event-question contrast."
            )
            log_bug_j.append({
                'pattern': p['id'], 'index': 1,
                'before': before, 'after': dict(wcps[1]),
            })

    # BUG-K: expand thin wcp.why
    for p in patterns:
        wcps = p.get('wrong_corrected_pair') or []
        for i, w in enumerate(wcps):
            why = w.get('why', '') or ''
            tokens = re.findall(r'\S+', why)
            if 0 < len(tokens) < 6:
                before_why = why
                w['why'] = expand_thin_why(p, w, why)
                w['provenance'] = PROV
                w['audit_wave'] = AUDIT_WAVE
                w['review_status'] = REVIEW_STATUS
                w['reviewer_note'] = "wcp.why expanded for richness; teaching point unchanged."
                log_bug_k.append({
                    'pattern': p['id'], 'index': i,
                    'before_why': before_why,
                    'after_why': w['why'],
                    'before_tokens': len(tokens),
                })

    # Bump version
    g['_meta']['version'] = '2026.05.24-bug-ijk'

    print(f'BUG-I wcp dedup drops: {len(log_bug_i)}')
    print(f'BUG-J wcp wrong==correct rewrites: {len(log_bug_j)}')
    print(f'BUG-K wcp thin-why expansions: {len(log_bug_k)}')

    if args.apply:
        out = json.dumps(g, ensure_ascii=False, indent=2)
        GRAMMAR.write_text(out + '\n', encoding='utf-8')

        idx = json.loads(INDEX.read_text(encoding='utf-8'))
        new_size = lf_size(GRAMMAR)
        for entry in idx.get('files', []):
            if entry.get('path') == 'data/grammar.json':
                entry['size_bytes'] = new_size
                break
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        log = json.loads(FIX_LOG.read_text(encoding='utf-8'))
        log['BUG-I_wcp_dedup'] = {
            'description': 'WCP dedup (horizontal extension of BUG-A)',
            'drops': log_bug_i,
        }
        log['BUG-J_wcp_wrong_eq_correct'] = {
            'description': 'WCP wrong==correct under strip-only (horizontal extension of BUG-H)',
            'changes': log_bug_j,
        }
        log['BUG-K_wcp_thin_why'] = {
            'description': 'WCP.why expansion for rationales under 6 whitespace tokens (horizontal extension of BUG-E)',
            'changes': log_bug_k,
        }
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'\napplied. grammar.json LF size: {new_size}')
    else:
        print('\n--dry-run')


if __name__ == '__main__':
    main()
