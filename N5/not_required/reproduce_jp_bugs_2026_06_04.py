"""Reproduce the 12 specific JP-content bugs from the 2026-06-04 audit.
For each cited headword, dump every field that could hold the bug string
(particle_examples, examples[].ja, frequent_patterns, collocations) so we
can confirm what's actually in the corpus before fixing. Read-only."""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('data/vocab.json', encoding='utf-8') as f:
    v = json.load(f)
entries = v['entries']

CITED = ['べんきょうする', 'かす', 'ある', 'しごとする', 'すむ',
         'カタカナ', 'ぬるい', 'うるさい', 'まずい', 'まるい']

def dump(e):
    print(f'  id: {e["id"]}')
    print(f'  form: {e.get("form")!r}  reading: {e.get("reading")!r}  pos: {e.get("pos")!r}')
    pe = e.get('particle_examples') or []
    if pe:
        print(f'  particle_examples ({len(pe)}): {pe}')
    coll = e.get('collocations') or []
    if coll:
        print(f'  collocations ({len(coll)}): {coll}')
    fp = e.get('frequent_patterns') or []
    if fp:
        print(f'  frequent_patterns ({len(fp)}): {fp}')
    ex = e.get('examples') or []
    for i, x in enumerate(ex):
        print(f'  examples[{i}].ja: {x.get("ja")!r}  -> {x.get("translation_en","")[:50]!r}')

for cited in CITED:
    matches = [e for e in entries if e.get('form') == cited]
    print(f'\n=== {cited} ({len(matches)} match) ===')
    if not matches:
        # try reading match
        matches = [e for e in entries if e.get('reading') == cited]
        if matches:
            print(f'  (matched by reading)')
    for e in matches:
        dump(e)
