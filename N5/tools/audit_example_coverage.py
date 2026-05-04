"""Audit example-sentence / example-word coverage across vocab.json,
grammar.json, kanji.json.

Read-only. Reports:
  - Vocab entries with no example sentence (no `examples` array, or empty)
  - Grammar patterns with fewer than 3 examples
  - Kanji entries with no `examples` array or empty `kun` when kun
    readings legitimately exist for that kanji

Used to scope a content-authoring batch.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

def load(p):
    return json.loads(p.read_text(encoding='utf-8'))


def audit_vocab():
    """Vocab entries lacking example sentences. The data may store
    examples either inline on the entry, or by reference to grammar
    examples via `vocab_ids`. We treat an entry as 'covered' if either:
      (a) it has its own `examples` array with >=1 entry, OR
      (b) at least one grammar example references its `id` via vocab_ids.
    """
    vj = load(ROOT / 'data' / 'vocab.json')
    gj = load(ROOT / 'data' / 'grammar.json')
    entries = vj.get('entries', [])
    # Build: vocab_id -> count of grammar examples that cite it.
    cited: dict[str, int] = {}
    for p in gj.get('patterns', []):
        for ex in p.get('examples', []):
            for vid in ex.get('vocab_ids', []) or []:
                cited[vid] = cited.get(vid, 0) + 1
    uncovered = []
    no_inline = []
    for v in entries:
        vid = v.get('id', '')
        own = v.get('examples') or []
        cites = cited.get(vid, 0)
        if not own and not cites:
            uncovered.append(v)
        if not own:
            no_inline.append(v)
    return {
        'total': len(entries),
        'no_examples_anywhere': uncovered,
        'no_inline_examples': no_inline,
        'cited_only_count': len(no_inline) - len(uncovered),
    }


def audit_grammar():
    """Grammar patterns and their example counts."""
    gj = load(ROOT / 'data' / 'grammar.json')
    patterns = gj.get('patterns', [])
    zero, lt3, ok = [], [], []
    for p in patterns:
        n = len(p.get('examples') or [])
        if n == 0:
            zero.append(p)
        elif n < 3:
            lt3.append(p)
        else:
            ok.append(p)
    return {'total': len(patterns), 'zero_examples': zero,
            'fewer_than_3_examples': lt3, 'ok': ok}


def audit_kanji():
    """Kanji entries lacking example words and kanji entries with empty
    kun array when kun readings would be expected (heuristic: any kanji
    where the catalog's kun row is non-empty)."""
    kj = load(ROOT / 'data' / 'kanji.json')
    entries = kj.get('entries', [])
    no_examples, lt2_examples, no_kun = [], [], []
    for k in entries:
        ex = k.get('examples') or []
        if not ex:
            no_examples.append(k)
        elif len(ex) < 2:
            lt2_examples.append(k)
        if not (k.get('kun') or []):
            no_kun.append(k)
    return {'total': len(entries), 'no_examples': no_examples,
            'fewer_than_2_examples': lt2_examples, 'no_kun': no_kun}


def main():
    print('='*70)
    print('Example-coverage audit (vocab + grammar + kanji)')
    print('='*70)
    v = audit_vocab()
    print(f'\nVOCAB  ({v["total"]} entries)')
    print(f'  no example sentence anywhere: {len(v["no_examples_anywhere"])}')
    print(f'  no inline examples (covered only via grammar.vocab_ids): {v["cited_only_count"]}')
    print(f'  → entries fully without any example: {len(v["no_examples_anywhere"])}')
    print('  sample (first 8 fully uncovered):')
    for x in v['no_examples_anywhere'][:8]:
        print(f'    {x.get("form","?")}  ({x.get("reading","")})  - {x.get("gloss","")[:40]}')

    g = audit_grammar()
    print(f'\nGRAMMAR  ({g["total"]} patterns)')
    print(f'  zero examples: {len(g["zero_examples"])}')
    print(f'  fewer than 3 examples: {len(g["fewer_than_3_examples"])}')
    print(f'  ok (>=3): {len(g["ok"])}')
    if g['zero_examples']:
        print('  zero-example patterns:')
        for p in g['zero_examples']:
            print(f'    {p["id"]}  {p.get("pattern","")[:30]}')
    if g['fewer_than_3_examples']:
        print('  fewer-than-3 (sample):')
        for p in g['fewer_than_3_examples'][:8]:
            print(f'    {p["id"]}  {p.get("pattern","")[:30]}  ({len(p.get("examples",[]))})')

    k = audit_kanji()
    print(f'\nKANJI  ({k["total"]} entries)')
    print(f'  no examples: {len(k["no_examples"])}')
    print(f'  fewer than 2 examples: {len(k["fewer_than_2_examples"])}')
    print(f'  no kun reading: {len(k["no_kun"])}')
    if k['no_examples']:
        print('  no-example kanji (sample):')
        for x in k['no_examples'][:10]:
            print(f'    {x["glyph"]}  on={x.get("on",[])}  kun={x.get("kun",[])}  meaning={x.get("meanings",[])}')
    if k['fewer_than_2_examples']:
        print('  fewer-than-2-example kanji (sample):')
        for x in k['fewer_than_2_examples'][:10]:
            print(f'    {x["glyph"]}  ({len(x.get("examples",[]))} ex)  on={x.get("on",[])}  kun={x.get("kun",[])}')


if __name__ == '__main__':
    main()
