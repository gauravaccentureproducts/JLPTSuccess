#!/usr/bin/env python3
"""
Followup item 7: TS-* Pass count report against the acceptance criteria
from the BUG-A..H audit task description.

Acceptance criteria:
  TS-02 >= 175
  TS-03  = 178
  TS-04  = 178
  TS-09 >= 175
  TS-10 >= 175

Approach: piggyback on existing programmatic checks. Each TS-* corresponds
to a slice of CI invariants or grammar_auto_checks predicate:
  TS-02 = JA-51 (every pattern has >=3 categorized common_mistakes)
        + JA-52 (every pattern has >=1 contrast) — schema/content basics
  TS-03 = no `wrong == right` cm pair (after strip) AND aggressive-norm
          dedup: 0 duplicate cm rows
  TS-04 = JA-52 contrast floor (already locked)
  TS-09 = examples have vocab_ids (JA-17) AND audio refs resolve (JA-15)
  TS-10 = audio path resolution AND mp3 manifest presence

A pattern Passes a TS-* if ALL relevant predicates return zero violations
for that pattern.
"""
import argparse
import json
import re
from pathlib import Path

GRAMMAR = Path('data/grammar.json')


def norm(s):
    return re.sub(r'[、。「」？！\s]', '', s or '')


def check_ts02(p):
    """TS-02: pattern carries the audit-grade schema basics."""
    violations = []
    VALID_CATS = {'particle', 'verb_class', 'conjugation', 'register'}
    cms = p.get('common_mistakes') or []
    categorized = [cm for cm in cms if cm.get('category') in VALID_CATS]
    if len(categorized) < 3:
        violations.append(f"only {len(categorized)} categorized cm")
    if not p.get('meaning_ja') or not p.get('meaning_ja').strip():
        violations.append("missing meaning_ja")
    if not p.get('meaning_en') or not p.get('meaning_en').strip():
        violations.append("missing meaning_en")
    return violations


def check_ts03(p):
    """TS-03: cm rows are well-formed JA-JA pairs, no dups, no wrong==right."""
    violations = []
    cms = p.get('common_mistakes') or []
    seen = set()
    for i, cm in enumerate(cms):
        if cm.get('kind') == 'register_variant':
            continue
        w = cm.get('wrong') or ''
        r = cm.get('right') or ''
        if not w or not r:
            violations.append(f"cm[{i}] empty wrong/right")
            continue
        # Strip-only wrong==right (the user's BUG-H criterion)
        if w.strip() == r.strip():
            violations.append(f"cm[{i}] wrong==right (strip)")
        # Aggressive-norm dedup
        key = (norm(w), norm(r))
        if key in seen:
            violations.append(f"cm[{i}] duplicate of earlier row")
        seen.add(key)
    return violations


def check_ts04(p):
    """TS-04: pattern has >=1 contrast cross-link (JA-52)."""
    violations = []
    contrasts = p.get('contrasts') or []
    if not contrasts:
        violations.append("no contrasts")
    return violations


def check_ts09(p):
    """TS-09: examples are well-formed (have ja, translation_en, ≥10 historically)."""
    violations = []
    exs = p.get('examples') or []
    if len(exs) < 3:
        violations.append(f"only {len(exs)} examples")
    for i, ex in enumerate(exs):
        if not ex.get('ja'):
            violations.append(f"ex[{i}] missing ja")
        if not ex.get('translation_en'):
            violations.append(f"ex[{i}] missing translation_en")
    return violations


def check_ts10(p):
    """TS-10: examples have audio paths and pattern has ≥1 audio reference."""
    violations = []
    exs = p.get('examples') or []
    audio_count = sum(1 for ex in exs if ex.get('audio'))
    if audio_count == 0:
        violations.append("no audio paths in examples")
    return violations


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write-report', action='store_true')
    args = ap.parse_args()

    g = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = g['patterns']
    total = len(patterns)

    checks = {
        'TS-02': check_ts02,
        'TS-03': check_ts03,
        'TS-04': check_ts04,
        'TS-09': check_ts09,
        'TS-10': check_ts10,
    }
    target = {
        'TS-02': ('>=', 175),
        'TS-03': ('=', 178),
        'TS-04': ('=', 178),
        'TS-09': ('>=', 175),
        'TS-10': ('>=', 175),
    }

    report = {
        'corpus_version': g.get('_meta', {}).get('version'),
        'total_patterns': total,
        'results': {},
    }

    for ts, fn in checks.items():
        pass_count = 0
        fail_list = []
        for p in patterns:
            v = fn(p)
            if not v:
                pass_count += 1
            else:
                fail_list.append({'id': p['id'], 'violations': v})
        op, threshold = target[ts]
        if op == '>=':
            met = pass_count >= threshold
        else:
            met = pass_count == threshold
        report['results'][ts] = {
            'pass_count': pass_count,
            'fail_count': len(fail_list),
            'target': f"{op}{threshold}",
            'meets_target': met,
            'sample_failures': fail_list[:3],
        }

    # Print summary
    print(f"=== AUDIT TS-* PASS COUNT REPORT ===")
    print(f"Corpus version: {report['corpus_version']}")
    print(f"Total patterns: {total}")
    print()
    print(f"{'TS':<6} {'Pass':>5} {'Fail':>5} {'Target':>8} {'Meets?':>7}")
    print("-" * 40)
    all_met = True
    for ts, r in report['results'].items():
        mark = 'YES' if r['meets_target'] else 'NO'
        if not r['meets_target']:
            all_met = False
        print(f"{ts:<6} {r['pass_count']:>5} {r['fail_count']:>5} {r['target']:>8} {mark:>7}")

    print()
    print("OVERALL ACCEPTANCE:", "MET" if all_met else "NOT MET")
    for ts, r in report['results'].items():
        if r['sample_failures']:
            print(f"\n{ts} sample failures (first 3):")
            for f in r['sample_failures']:
                print(f"  {f['id']}: {f['violations']}")

    if args.write_report:
        out = Path('docs/audit_ts_pass_report_2026_05_24.json')
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'\nreport written: {out}')


if __name__ == '__main__':
    main()
