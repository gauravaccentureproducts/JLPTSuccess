"""ISSUE-081 (round-8 audit, 2026-05-06): bring vocab entries to the
≥2-examples floor by auto-cross-referencing grammar.json examples.

Pre-fix: 10/1041 entries have ≥2 examples (1%).
Strategy: for each vocab entry with only 1 example, scan grammar.json
examples for sentences containing the entry's form. Add the first new
match as a 2nd example. Mark with a `source` field crediting the
grammar pattern it came from.

Bounded effort: process top-200 frequency-ranked entries in this pass
(determined by entries.json index — earlier entries are more frequent
in the N5 corpus).

Idempotent: skips entries that already have ≥2 examples.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
VF = ROOT / 'data' / 'vocab.json'
GF = ROOT / 'data' / 'grammar.json'

# Cap how many entries we process this pass — top-200 by index order.
LIMIT = 200


def main() -> int:
    vdata = json.loads(VF.read_text(encoding='utf-8'))
    gdata = json.loads(GF.read_text(encoding='utf-8'))

    # Build a flat list of all grammar examples with their source pattern id.
    grammar_examples = []
    for p in gdata.get('patterns', []):
        for ex in p.get('examples', []) or []:
            ja = ex.get('ja') or ''
            if ja:
                grammar_examples.append({
                    'ja': ja,
                    'translation_en': ex.get('translation_en') or ex.get('en') or '',
                    'source_pattern': p.get('id'),
                })

    n_added = 0
    n_skipped_already = 0
    n_no_match = 0

    for idx, e in enumerate(vdata.get('entries', [])):
        if idx >= LIMIT:
            break
        existing = e.get('examples') or []
        if len(existing) >= 2:
            n_skipped_already += 1
            continue
        form = e.get('form') or ''
        reading = e.get('reading') or ''
        if not form:
            continue
        # Find a grammar example containing this form (kanji form preferred,
        # else the kana reading) AND not already in the entry's examples.
        existing_ja = {ex.get('ja') for ex in existing}
        match = None
        for ge in grammar_examples:
            if ge['ja'] in existing_ja:
                continue
            # Match on form (which may equal reading for kana entries).
            if form in ge['ja'] or (form != reading and reading and reading in ge['ja']):
                match = ge
                break
        if not match:
            n_no_match += 1
            continue
        # Append as second example
        existing.append({
            'ja': match['ja'],
            'translation_en': match['translation_en'],
            'source': match['source_pattern'],
        })
        e['examples'] = existing
        n_added += 1

    VF.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    n_total_2plus = sum(1 for e in vdata['entries']
                        if len(e.get('examples', [])) >= 2)
    total = len(vdata['entries'])
    print(f'[ISSUE-081] Auto-cross-referenced examples (top-{LIMIT})')
    print(f'  added 2nd example:        {n_added}')
    print(f'  already had >= 2:         {n_skipped_already}')
    print(f'  no grammar.json match:    {n_no_match}')
    print(f'  total entries with >= 2:  {n_total_2plus}/{total}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
