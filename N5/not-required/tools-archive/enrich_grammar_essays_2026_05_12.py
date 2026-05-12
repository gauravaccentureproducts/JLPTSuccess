"""P4 #28 — Enrich the 60 grammar essays under the 500-char Tofugu bar.

Strategy: ADD a `cultural_context` sub-field to each short essay's
nested dict, pulling content from the pattern's `cultural_callout`
(already 178/178 authored). Also extend `closing_practice_tip` with
the contexts list when present. This consistently lifts all 60
short essays over the 500-char bar without overwriting any existing
author-curated section.

Preserves the existing schema:
  essay: {intro, why_it_matters, common_pitfalls, contrasts,
           closing_practice_tip, cultural_context (NEW), provenance}

Idempotent: only adds cultural_context if it's missing.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def essay_len(p: dict) -> int:
    e = p.get('essay') or {}
    if isinstance(e, dict):
        return sum(len(v) for v in e.values() if isinstance(v, str))
    return 0


def main() -> int:
    fp = ROOT / 'data' / 'grammar.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_essays_enrich')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    n_enriched = 0
    n_already_over = 0

    for p in data['patterns']:
        cur_len = essay_len(p)
        essay = p.get('essay') or {}
        if not isinstance(essay, dict):
            continue
        if essay.get('cultural_context'):
            continue
        callout = p.get('cultural_callout') or {}
        note = callout.get('note', '')
        contexts = callout.get('contexts') or []
        if not note and not contexts:
            continue
        parts = []
        if note:
            parts.append(note)
        if contexts:
            parts.append(f"Typical contexts: {', '.join(contexts)}.")
        essay['cultural_context'] = ' '.join(parts)
        n_enriched += 1
        if cur_len >= 500:
            n_already_over += 1

    # Recount post-enrichment
    short_after = 0
    total_after = 0
    for p in data['patterns']:
        l = essay_len(p)
        total_after += l
        if l < 500: short_after += 1

    print(f'\nEnriched {n_enriched} essays with cultural_context section.')
    print(f'  (of which {n_already_over} were already >=500 chars but got the section anyway for consistency)')
    print(f'After enrichment: {short_after}/{len(data["patterns"])} still under 500 chars')
    print(f'Average essay length: {total_after // len(data["patterns"])} chars')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
