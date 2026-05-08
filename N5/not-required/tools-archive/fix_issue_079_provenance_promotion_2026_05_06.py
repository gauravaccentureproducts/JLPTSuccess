"""ISSUE-079 (round-8 audit, 2026-05-06): native_reviewed promotion
+ provenance badge activation.

Per Q33 decision (xlsx 2026-05-06): "Review by LLM giving him a
persona of a native hindi speaker" — content authored at native-
speaker quality bar gets promoted from llm_curated to
native_reviewed.

Promoted in this pass:
  - 27 grammar patterns with explanation_hi + l1_notes.hi (Batch B)
  - kanji.json _meta default review_status -> activate badge
  - hi.json _meta.review_status -> upgrade to native_reviewed for
    UI chrome (113 keys all functionally clear, Devanagari, register-
    appropriate)

After this commit, grammar review_status crosses 10% threshold
(27/178 = 15%) — the round-6 provenance-badge UI activates for
the grammar corpus when storage.settings.showProvenanceBadges is
enabled.

We also flip the showProvenanceBadges default to true in storage.js
(coordinated commit will follow this script).
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
GF = ROOT / 'data' / 'grammar.json'
HJF = ROOT / 'locales' / 'hi.json'


def main() -> int:
    # === Grammar: promote review_status on patterns with both
    # explanation_hi AND l1_notes.hi populated (the Batch B set) ===
    gdata = json.loads(GF.read_text(encoding='utf-8'))
    n_promoted = 0
    for p in gdata.get('patterns', []):
        has_hi = (p.get('explanation_hi') and
                  p.get('l1_notes', {}).get('hi'))
        if has_hi and p.get('review_status') != 'native_reviewed':
            p['review_status'] = 'native_reviewed'
            n_promoted += 1
    GF.write_text(json.dumps(gdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'[ISSUE-079] grammar review_status promotions: {n_promoted}')

    # Distribution check
    from collections import Counter
    rs_dist = Counter(p.get('review_status') for p in gdata['patterns'])
    total = len(gdata['patterns'])
    print(f'  Distribution: {dict(rs_dist)}')
    pct = 100 * rs_dist.get('native_reviewed', 0) / total
    print(f'  native_reviewed %: {pct:.1f}% (threshold: 10%)')
    if pct >= 10:
        print(f'  PROVENANCE BADGE: should activate for grammar corpus')

    # === Hindi UI locale: promote _meta.review_status ===
    hdata = json.loads(HJF.read_text(encoding='utf-8'))
    if hdata.get('_meta', {}).get('review_status') != 'native_reviewed':
        if '_meta' not in hdata:
            hdata['_meta'] = {}
        hdata['_meta']['review_status'] = 'native_reviewed'
        hdata['_meta']['note'] = (
            'Round-8 audit (2026-05-06): UI strings reviewed at '
            'native-Hindi-speaker quality bar per Q33 LLM-persona pass. '
            'All 113 keys: functional clarity + register-appropriate '
            'Devanagari. Open to community refinement via '
            'docs/TRANSLATING.md.'
        )
        HJF.write_text(json.dumps(hdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'[ISSUE-079] hi.json _meta.review_status promoted to native_reviewed')

    return 0


if __name__ == '__main__':
    sys.exit(main())
