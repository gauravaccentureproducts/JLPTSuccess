#!/usr/bin/env python3
"""
Unified cross-corpus audit (W3.2).

Single tool that runs all TS-* scenarios across all corpora and
the auxiliary question + paper corpora. Replaces the scattered
per-corpus fix scripts as the canonical point-of-truth invocation.

Usage:
  python tools/audit_all.py            # all corpora, human summary
  python tools/audit_all.py --json     # JSON output
  python tools/audit_all.py --corpus grammar  # single-corpus mode

Exit 0 if clean; 1 if any defects.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from audit_ts_pass_counts_v2_2026_05_24 import (
    check_ts02_examples, check_ts03_cm_wcp, check_ts04, check_ts05,
    check_ts06_audio, check_ts09_why, check_ts10_meaning, norm,
)


def audit_grammar(data):
    patterns = data['patterns']
    results = defaultdict(lambda: {'pass': 0, 'partial': 0, 'fail': 0, 'samples': []})
    checks = {
        'TS-02': check_ts02_examples, 'TS-03': check_ts03_cm_wcp, 'TS-04': check_ts04,
        'TS-05': check_ts05, 'TS-06': check_ts06_audio, 'TS-09': check_ts09_why,
        'TS-10': check_ts10_meaning,
    }
    for ts, fn in checks.items():
        for p in patterns:
            f, partials = fn(p)
            if f:
                results[ts]['fail'] += 1
                if len(results[ts]['samples']) < 3:
                    results[ts]['samples'].append({'id': p['id'], 'violations': f})
            elif partials:
                results[ts]['partial'] += 1
            else:
                results[ts]['pass'] += 1
    return dict(results)


def audit_vocab(data):
    entries = data.get('entries', [])
    r = {'pass': 0, 'within_entry_ex_dups': 0, 'missing_gloss': 0, 'missing_examples': 0}
    for e in entries:
        ok = True
        if not (e.get('gloss') or '').strip(): r['missing_gloss'] += 1; ok = False
        if not (e.get('examples') or []): r['missing_examples'] += 1; ok = False
        seen = set()
        for ex in (e.get('examples') or []):
            if isinstance(ex, dict):
                key = (norm(ex.get('ja','')), (ex.get('translation_en','') or '').strip().lower())
                if key in seen and ex.get('ja'): r['within_entry_ex_dups'] += 1; ok = False
                seen.add(key)
        if ok: r['pass'] += 1
    r['total'] = len(entries)
    return r


def audit_kanji(data):
    entries = data.get('entries', [])
    r = {'pass': 0, 'within_entry_ex_dups': 0, 'empty_meanings': 0}
    for e in entries:
        ok = True
        if not (e.get('meanings') or []): r['empty_meanings'] += 1; ok = False
        seen = set()
        for ex in (e.get('examples') or []):
            if isinstance(ex, dict) and ex.get('form'):
                key = norm(ex.get('form'))
                if key in seen: r['within_entry_ex_dups'] += 1; ok = False
                seen.add(key)
        if ok: r['pass'] += 1
    r['total'] = len(entries)
    return r


def audit_reading(data):
    passages = data.get('passages', [])
    r = {'pass': 0, 'empty_ja': 0, 'no_questions': 0, 'bad_question': 0}
    for p in passages:
        ok = True
        if not (p.get('ja') or '').strip(): r['empty_ja'] += 1; ok = False
        qs = p.get('questions') or []
        if not qs: r['no_questions'] += 1; ok = False
        for q in qs:
            if q.get('correctAnswer') is None or not (q.get('choices') or []):
                r['bad_question'] += 1; ok = False
        if ok: r['pass'] += 1
    r['total'] = len(passages)
    return r


def audit_listening(data):
    items = data.get('items', [])
    r = {'pass': 0, 'empty_script': 0, 'no_answer': 0, 'bad_choices': 0}
    for it in items:
        ok = True
        if not (it.get('script_ja') or '').strip(): r['empty_script'] += 1; ok = False
        if it.get('correctAnswer') is None: r['no_answer'] += 1; ok = False
        if len(it.get('choices') or []) < 2: r['bad_choices'] += 1; ok = False
        if ok: r['pass'] += 1
    r['total'] = len(items)
    return r


def audit_questions(data):
    items = data['questions']
    r = {'pass': 0, 'malformed_mcq': 0, 'malformed_sentence_order': 0, 'malformed_text_input': 0, 'dups': 0}
    seen = {}
    for it in items:
        ok = True
        t = it.get('type')
        if t == 'mcq':
            ch = it.get('choices') or []; ca = it.get('correctAnswer')
            if not (it.get('question_ja') or '').strip() or not ch or ca is None or ca not in ch:
                r['malformed_mcq'] += 1; ok = False
            k = ('mcq', norm(it.get('question_ja','')), str(it.get('correctAnswer','')))
        elif t == 'sentence_order':
            tiles = it.get('tiles') or []; co = it.get('correctOrder') or []
            if not tiles or not co or sorted(tiles) != sorted(co):
                r['malformed_sentence_order'] += 1; ok = False
            k = ('so', tuple(sorted(tiles)), tuple(co))
        elif t == 'text_input':
            aa = it.get('acceptedAnswers') or []; ca = it.get('correctAnswer')
            if not aa or ca is None: r['malformed_text_input'] += 1; ok = False
            k = ('ti', norm(it.get('question_ja','')), str(it.get('correctAnswer','')))
        else:
            k = None
        if k:
            if k in seen: r['dups'] += 1; ok = False
            seen[k] = it['id']
        if ok: r['pass'] += 1
    r['total'] = len(items)
    return r


def audit_papers():
    papers = sorted(Path('data/papers').rglob('paper-*.json'))
    all_q = []
    for p in papers:
        d = json.loads(p.read_text(encoding='utf-8'))
        for q in d.get('questions') or []:
            all_q.append((str(p.relative_to('data/papers')), q))
    r = {'pass': 0, 'malformed': 0, 'dups': 0, 'kbsourceid_unresolved': 0}
    seen = {}
    qc = json.loads(Path('data/questions.json').read_text(encoding='utf-8'))
    q_ids = {qq['id'] for qq in qc['questions']}
    for path, q in all_q:
        ok = True
        if not isinstance(q, dict): r['malformed'] += 1; continue
        ci = q.get('correctIndex'); ch = q.get('choices') or []
        stem = q.get('stem_html') or q.get('stem') or q.get('passage') or ''
        if not isinstance(stem, str): stem = str(stem)
        if not ch or ci is None or not isinstance(ci, int) or ci < 0 or ci >= len(ch):
            r['malformed'] += 1; ok = False
        if not stem.strip(): r['malformed'] += 1; ok = False
        key = (norm(stem), tuple(sorted(ch)), ci) if stem and ch else None
        if key:
            if key in seen: r['dups'] += 1; ok = False
            seen[key] = q.get('id')
        kb = q.get('kbSourceId')
        if kb and isinstance(kb, str) and kb.startswith('q-') and kb not in q_ids:
            r['kbsourceid_unresolved'] += 1; ok = False
        if ok: r['pass'] += 1
    r['total'] = len(all_q); r['paper_count'] = len(papers)
    return r


CORPORA = {
    'grammar': ('data/grammar.json', audit_grammar),
    'vocab': ('data/vocab.json', audit_vocab),
    'kanji': ('data/kanji.json', audit_kanji),
    'reading': ('data/reading.json', audit_reading),
    'listening': ('data/listening.json', audit_listening),
    'questions': ('data/questions.json', audit_questions),
    'papers': (None, audit_papers),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--corpus', choices=list(CORPORA) + ['all'], default='all')
    args = ap.parse_args()

    report = {}
    for name, (path, fn) in CORPORA.items():
        if args.corpus != 'all' and args.corpus != name: continue
        if path:
            data = json.loads(Path(path).read_text(encoding='utf-8'))
            report[name] = fn(data)
        else:
            report[name] = fn()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print("=" * 60)
    print("UNIFIED CROSS-CORPUS AUDIT")
    print("=" * 60)
    any_fail = False
    for corpus, data in report.items():
        print(f"\n[{corpus.upper()}]")
        if corpus == 'grammar':
            for ts, counts in data.items():
                if counts['fail'] > 0: any_fail = True
                print(f"  {ts}: pass={counts['pass']:3} partial={counts['partial']:3} fail={counts['fail']:3}")
        else:
            for k, v in data.items():
                if isinstance(v, int): print(f"  {k}: {v}")
            defect_keys = [k for k in data if k.startswith('malformed') or 'dup' in k or 'empty' in k or 'missing' in k or 'bad' in k or 'unresolved' in k]
            if any(data.get(k, 0) > 0 for k in defect_keys):
                any_fail = True

    print("\n" + "=" * 60)
    print(f"OVERALL: {'CLEAN' if not any_fail else 'DEFECTS FOUND'}")
    return 1 if any_fail else 0


if __name__ == '__main__':
    sys.exit(main())
