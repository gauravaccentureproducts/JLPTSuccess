#!/usr/bin/env python3
"""
Followup fixes after BUG-A..H sweep:

Item 6: 3 cm rows that look like wrong==right under aggressive norm
        — rewrite to substantive learner-error variants that survive
        BOTH the aggressive and strip-only norms.

        - n5-126[2]: register-conjunction rewrite (から vs が)
        - n5-155[0]: register-mismatch rewrite (けど vs が)
        - n5-166[1]: spurious-で rewrite (おはようでございます)

Tagged with provenance="auto_fix_2026_05_24" + audit_wave="claude_audit_2026_05_24"
+ source="BUG-A..H followup item-6".
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


def norm(s):
    return re.sub(r'[、。「」？！\s]', '', s or '')


def lf_size(path: Path) -> int:
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


REWRITES = {
    # (pattern_id, cm_index): {wrong, right, why, category}
    ('n5-126', 2): {
        'wrong': '高いですから、おいしいです。',
        'right': '高いですが、おいしいです。',
        'why': "Use が for CONTRAST ('high BUT delicious'). から means BECAUSE/SO and would imply 'because expensive, therefore delicious' — wrong logic. Pattern: [polite-clause]が、[polite-clause] for contrastive connection.",
        'category': 'register',
    },
    ('n5-155', 0): {
        'wrong': 'むずかしいけど、おもしろいですが。',
        'right': 'むずかしいですが、おもしろいです。',
        'why': "けど is the casual contrastive; pairs with plain forms (むずかしい+けど). With polite-form clauses use が (or けれども). Don't mix plain-form けど + polite-form です. Pattern: [polite-clause]が、[polite-clause].",
        'category': 'register',
    },
    ('n5-166', 1): {
        'wrong': 'おはようでございます。',
        'right': 'おはようございます。',
        'why': "おはようございます is a fixed greeting — one fused word. Don't insert で between おはよう and ございます; the compound is not [おはよう] + [で] + [ございます]. The morning-polite form is morphologically a single unit.",
        'category': 'register',
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    g = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = g['patterns']

    changes = []
    for p in patterns:
        cms = p.get('common_mistakes') or []
        for i, cm in enumerate(cms):
            key = (p.get('id'), i)
            if key in REWRITES:
                repl = REWRITES[key]
                before = dict(cm)
                cm['wrong'] = repl['wrong']
                cm['right'] = repl['right']
                cm['why'] = repl['why']
                cm['category'] = repl['category']
                cm['provenance'] = PROV
                cm['audit_wave'] = AUDIT_WAVE
                cm['source'] = 'BUG-A..H followup item-6 (substantive variant)'
                changes.append({
                    'pattern': p['id'], 'index': i,
                    'before': before, 'after': dict(cm),
                })
                print(f'  {p["id"]} cm[{i}] rewritten')

    # Verify aggressive-norm distinct
    for c in changes:
        w = norm(c['after']['wrong'])
        r = norm(c['after']['right'])
        if w == r:
            print(f"  WARN: {c['pattern']} cm[{c['index']}] still wrong==right under aggressive norm")
        else:
            print(f"  OK: {c['pattern']} cm[{c['index']}] distinct under aggressive norm")

    # Bump _meta.version
    g['_meta']['version'] = '2026.05.24-followups'

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

        # Append to fix_log
        log = json.loads(FIX_LOG.read_text(encoding='utf-8'))
        log['BUG-A_followup_item6'] = {
            'description': 'Substantive-variant rewrites for 3 cm rows that looked like wrong==right under aggressive norm; now distinct under BOTH aggressive and strip-only norms.',
            'changes': changes,
        }
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        print(f'\napplied. grammar.json LF size: {new_size}')
    else:
        print(f'\n--dry-run. would rewrite {len(changes)} rows')


if __name__ == '__main__':
    main()
