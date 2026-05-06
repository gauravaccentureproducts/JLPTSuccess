"""ISSUE-096 (round-9): vocab examples >=2 missing on 927/1041 entries (89%).

Strategy: auto-derive a second example from grammar.json cross-references.
Each grammar example carries a `vocab_ids` array listing which vocab
entries appear in the sentence. For every vocab entry with <2 examples
that's referenced in some grammar example, pull the first grammar
example whose JA text differs from the existing vocab example and add
it as a second example.

After auto-derive, ~206 vocab entries can reach 2 examples from the
grammar cross-reference pool. The remaining 721 entries without any
grammar cross-reference need authored examples — those are deferred
to a future LLM-curated cycle (logged as IMP/ISSUE in a follow-up).

Idempotent: skips entries that already have >=2 examples; deduplicates
by JA text within each entry.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

VOCAB = Path(__file__).parent.parent / 'data' / 'vocab.json'
GRAMMAR = Path(__file__).parent.parent / 'data' / 'grammar.json'


def main() -> int:
    vdoc = json.loads(VOCAB.read_text(encoding='utf-8'))
    gdoc = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    v_entries = vdoc['entries']
    g_patterns = gdoc['patterns']

    # Build vocab_id -> [grammar_example_dict] cross-reference
    vid_to_examples = {}
    for p in g_patterns:
        for ex in p.get('examples', []):
            for vid in ex.get('vocab_ids', []):
                vid_to_examples.setdefault(vid, []).append(ex)

    n_added = 0
    n_already_ok = 0
    n_no_xref = 0
    n_dup_only = 0

    for w in v_entries:
        existing = w.get('examples', [])
        if len(existing) >= 2:
            n_already_ok += 1
            continue

        vid = w.get('id')
        xrefs = vid_to_examples.get(vid, [])
        if not xrefs:
            n_no_xref += 1
            continue

        existing_ja = {e.get('ja', '').strip() for e in existing}

        # Find grammar examples whose JA differs from existing vocab ones
        added_for_this = 0
        for gex in xrefs:
            ja = gex.get('ja', '').strip()
            if not ja or ja in existing_ja:
                continue
            existing.append({
                'ja': ja,
                'translation_en': gex.get('translation_en', ''),
            })
            existing_ja.add(ja)
            added_for_this += 1
            n_added += 1
            if len(existing) >= 2:
                break

        w['examples'] = existing
        if added_for_this == 0:
            n_dup_only += 1

    VOCAB.write_text(
        json.dumps(vdoc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    # Verify
    vdoc2 = json.loads(VOCAB.read_text(encoding='utf-8'))
    at_2 = sum(1 for w in vdoc2['entries'] if len(w.get('examples', [])) >= 2)
    print(f'Examples added: {n_added}')
    print(f'Already had >=2:           {n_already_ok}')
    print(f'No grammar cross-ref:      {n_no_xref}')
    print(f'Xref existed but JA dup:   {n_dup_only}')
    print(f'\nPost-fix: {at_2}/{len(vdoc2["entries"])} entries have >=2 examples.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
