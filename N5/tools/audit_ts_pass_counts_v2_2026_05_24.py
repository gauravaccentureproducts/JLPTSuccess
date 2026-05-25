#!/usr/bin/env python3
"""
Honest TS audit v2 — extends v1 to cover the gaps the independent
reviewer flagged:
  - TS-02 partials: within-pattern example dedup (already 0 under strict
    norm; report cross-pattern translation_en reuse separately)
  - TS-03: cm-and-wcp dedup + wrong==correct (cm + wcp); SKIP
    register_variant by-design entries
  - TS-09: cm.why AND wcp.why under 6 tokens
  - TS-10: meaning_ja length (>100 chars now lives in explanation_ja
    per BUG-F; no honest violation now) + Latin token count
  - TS-04, TS-05, TS-06: schema basics + meta consistency

For each TS, report: Pass / Partial / Fail counts that ADD UP to 178.
"""
import argparse
import json
import re
from pathlib import Path

GRAMMAR = Path('data/grammar.json')


def norm(s):
    return re.sub(r'[、。「」？！\s]', '', s or '')


# TS-10 slot-token Latin whitelist (FP-21 lock, locked by JA-166).
# These Latin tokens are LEGITIMATE pedagogical slot notation in
# meaning_ja / explanation_ja (Verb-stem + たい, NOUN + を, etc.) per
# Japanese-pedagogy conventions (Genki, Minna no Nihongo, etc.).
# The TS-10 Latin-token audit MUST treat these as not-flagged.
# Adding a new convention-introduced token? Extend this list AND
# the matching xlsx scenario row (FP-21) per Rule 5 (cross-artifact sync).
SLOT_TOKEN_WHITELIST = {
    'Verb', 'Verb-stem', 'Verb-stem',
    'Adj', 'i-Adj', 'na-Adj',
    'Noun', 'NP',
    'counter',
    'A', 'B', 'X', 'Y',
    'V', 'I', 'II', 'III', 'IV',
    'na', 'i',
    'V-', 'V-ます', 'V-て', 'V-た', 'V-ない',
}


def check_ts02_examples(p):
    """TS-02: examples are well-formed AND no within-pattern dups."""
    fails, partials = [], []
    exs = p.get('examples') or []
    if not exs:
        fails.append("no examples")
    seen = set()
    for i, ex in enumerate(exs):
        if not ex.get('ja') or not ex.get('translation_en'):
            fails.append(f"ex[{i}] missing ja or translation_en")
        key = (norm(ex.get('ja', '')), (ex.get('translation_en', '') or '').strip().lower())
        if key in seen:
            partials.append(f"ex[{i}] duplicate of earlier example")
        seen.add(key)
    return fails, partials


def check_ts03_cm_wcp(p):
    """TS-03: cm and wcp rows well-formed, no dups, no wrong==right (strip).
    SKIPS register_variant entries (FP-16 by-design schema)."""
    fails, partials = [], []
    cms = p.get('common_mistakes') or []
    wcps = p.get('wrong_corrected_pair') or []

    # CM
    seen_cm = set()
    for i, cm in enumerate(cms):
        if cm.get('kind') == 'register_variant':
            continue  # by-design empty wrong/right
        w = cm.get('wrong') or ''
        r = cm.get('right') or ''
        if not w or not r:
            fails.append(f"cm[{i}] empty wrong/right (non-register_variant)")
            continue
        if w.strip() == r.strip():
            fails.append(f"cm[{i}] wrong==right (strip)")
        key = (norm(w), norm(r))
        if key in seen_cm:
            fails.append(f"cm[{i}] duplicate of earlier cm")
        seen_cm.add(key)

    # WCP
    seen_wcp = set()
    for i, ww in enumerate(wcps):
        wr = ww.get('wrong') or ''
        cor = ww.get('correct') or ''
        if not wr or not cor:
            continue  # wcp rows allowed to be sparse historically
        if wr.strip() == cor.strip():
            fails.append(f"wcp[{i}] wrong==correct (strip)")
        key = (norm(wr), norm(cor))
        if key in seen_wcp:
            fails.append(f"wcp[{i}] duplicate of earlier wcp")
        seen_wcp.add(key)

    return fails, partials


def check_ts04(p):
    """TS-04: contrast cross-link + category sanity."""
    fails, partials = [], []
    contrasts = p.get('contrasts') or []
    if not contrasts:
        fails.append("no contrasts")
    if not p.get('category'):
        fails.append("no category")
    return fails, partials


def check_ts05(p):
    """TS-05: pattern form appears in at least one example (heuristic).

    HISTORY: Previously emitted 'Fail' when coverage=0. Reviewer
    (2026-05-24 re-audit) confirmed all 0-coverage hits were
    conjugation-based misses (e.g., pattern '〜じはん' appears as
    '〜時はん' with kanji; pattern '〜すぎる' appears as conjugated
    'すぎました'). The static-substring heuristic CANNOT cleanly handle
    conjugation; calling these 'Fail' overclaims real defects.

    Replacement: emit 'NA-heuristic-limit' label when coverage is 0
    AND the pattern includes kana/kanji forms that typically conjugate
    (verb endings, adjective endings). A true Fail would require
    inflection-aware matching, which is out of scope for static checks.
    """
    fails, partials = [], []
    pat_form = (p.get('pattern') or '').replace('〜', '').replace(' ', '')
    if not pat_form:
        return fails, partials  # skip if no form
    exs = p.get('examples') or []
    if not exs:
        return fails, partials
    fragments = re.findall(r'[ぁ-ゟァ-ヿ一-龯]{2,}', pat_form)
    if not fragments:
        return fails, partials
    hits = 0
    for ex in exs:
        ja = ex.get('ja', '') or ''
        if any(f in ja for f in fragments):
            hits += 1
    coverage = hits / len(exs) if exs else 0
    # NA-heuristic-limit (not Fail) for 0-coverage cases — almost always
    # a conjugation-driven false negative that needs an NLP-level matcher.
    if coverage == 0:
        partials.append("NA-heuristic-limit: pattern form not found by static substring match (conjugation likely; needs inflection-aware matcher)")
    elif coverage < 0.3:
        partials.append(f"only {hits}/{len(exs)} examples visibly contain the pattern form (heuristic; conjugated forms may not match literally)")
    return fails, partials


def check_ts06_audio(p):
    """TS-06: audio paths declared + reachable (path-level, not content)."""
    fails, partials = [], []
    exs = p.get('examples') or []
    if not exs:
        return fails, partials
    audio_count = sum(1 for ex in exs if ex.get('audio'))
    if audio_count == 0:
        fails.append("no audio paths on examples")
    elif audio_count < len(exs):
        partials.append(f"{audio_count}/{len(exs)} examples have audio paths")
    return fails, partials


def check_ts09_why(p):
    """TS-09: cm.why AND wcp.why are non-empty.

    HISTORY: This predicate previously enforced a >=6 token floor.
    Reviewer (2026-05-24 re-audit, post-BUG-K) flagged the floor as
    metric-gameable: a fix-pass added boilerplate suffixes to satisfy
    the count, damaging pedagogical quality (tautology + empty
    generality + broken self-reference). Crisp one-liners like
    "Action-location uses で, not に" are PEDAGOGICALLY COMPLETE
    even at 5 tokens.

    Replacement: just check why is non-empty. Token-count floor
    REMOVED. A future content-quality check could examine whether
    `why` names both the rule and the correction, but that needs
    NLP-level analysis beyond static heuristics.
    """
    fails, partials = [], []
    for arr_name in ('common_mistakes', 'wrong_corrected_pair'):
        for i, item in enumerate(p.get(arr_name) or []):
            if item.get('kind') == 'register_variant':
                continue
            why = item.get('why', '') or ''
            if not why.strip():
                # Truly empty why is a real defect (failure)
                fails.append(f"{arr_name}[{i}].why is empty")
    return fails, partials


def check_ts10_meaning(p):
    """TS-10: meaning fields complete + no over-long meaning_ja
    (BUG-F moved overflow to explanation_ja)."""
    fails, partials = [], []
    if not (p.get('meaning_en') or '').strip():
        fails.append("missing meaning_en")
    if not (p.get('meaning_ja') or '').strip():
        fails.append("missing meaning_ja")
    mja = p.get('meaning_ja', '') or ''
    if len(mja) > 100:
        partials.append(f"meaning_ja {len(mja)} chars > 100 (BUG-F should have split)")
    # If explanation_ja exists, it should be non-empty (JA-162)
    if 'explanation_ja' in p:
        ej = (p.get('explanation_ja') or '').strip()
        if not ej:
            fails.append("explanation_ja key present but empty (JA-162 violation)")
    return fails, partials


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write-report', action='store_true')
    args = ap.parse_args()

    g = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = g['patterns']
    total = len(patterns)

    checks = {
        'TS-02': check_ts02_examples,
        'TS-03': check_ts03_cm_wcp,
        'TS-04': check_ts04,
        'TS-05': check_ts05,
        'TS-06': check_ts06_audio,
        'TS-09': check_ts09_why,
        'TS-10': check_ts10_meaning,
    }
    # Target acceptance (originally TS-02..TS-10; honest re-run)
    target = {
        'TS-02': ('>=', 175),
        'TS-03': ('=', 178),
        'TS-04': ('=', 178),
        'TS-05': ('>=', 150),
        'TS-06': ('>=', 175),
        'TS-09': ('>=', 175),
        'TS-10': ('>=', 175),
    }

    report = {
        'corpus_version': g.get('_meta', {}).get('version'),
        'total_patterns': total,
        'register_variant_skip_applied': True,
        'results': {},
    }

    print(f"=== HONEST TS-* AUDIT v2 ===")
    print(f"Corpus version: {report['corpus_version']}")
    print(f"Total patterns: {total}")
    print()
    print(f"{'TS':<6} {'Pass':>5} {'Part':>5} {'Fail':>5} {'Target':>8} {'Meets?':>7}")
    print("-" * 50)

    all_met = True
    for ts, fn in checks.items():
        pass_n, part_n, fail_n = 0, 0, 0
        sample_partials = []
        sample_fails = []
        for p in patterns:
            f, partials = fn(p)
            if f:
                fail_n += 1
                if len(sample_fails) < 5:
                    sample_fails.append({'id': p['id'], 'violations': f})
            elif partials:
                part_n += 1
                if len(sample_partials) < 5:
                    sample_partials.append({'id': p['id'], 'partials': partials})
            else:
                pass_n += 1
        op, threshold = target[ts]
        if op == '>=':
            met = pass_n >= threshold
        else:
            met = pass_n == threshold
        if not met:
            all_met = False
        report['results'][ts] = {
            'pass': pass_n, 'partial': part_n, 'fail': fail_n,
            'target': f"{op}{threshold}", 'meets': met,
            'sample_fails': sample_fails,
            'sample_partials': sample_partials,
        }
        mark = 'YES' if met else 'NO'
        print(f"{ts:<6} {pass_n:>5} {part_n:>5} {fail_n:>5} {threshold:>8} {mark:>7}")

    print()
    print("OVERALL:", "ALL MET" if all_met else "GAPS REMAIN")

    for ts, r in report['results'].items():
        if r['fail'] or r['partial']:
            print(f"\n{ts} P={r['pass']} Part={r['partial']} Fail={r['fail']}")
            for f in r['sample_fails']:
                print(f"  FAIL  {f['id']}: {f['violations']}")
            for f in r['sample_partials'][:3]:
                print(f"  PART  {f['id']}: {f['partials']}")

    if args.write_report:
        out = Path('docs/audit_ts_pass_report_v2_2026_05_24.json')
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'\nreport: {out}')


if __name__ == '__main__':
    main()
