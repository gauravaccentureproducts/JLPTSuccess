"""Enrich data/vocab.json with curated example sentences.

Reads KnowledgeBank/vocab_examples_n4.md and attaches each example to
the matching vocab entry by `form`. Idempotent.

Filters out any example with out-of-scope kanji (per JA-13).
"""
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

vocab_data = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
whitelist = set(json.loads((ROOT / 'data' / 'n4_kanji_whitelist.json').read_text(encoding='utf-8')))

KANJI_RE = re.compile(r'[一-鿿]')

def all_kanji_in_scope(s):
    return all((not KANJI_RE.match(c)) or c in whitelist for c in s)

CURATED_PATH = ROOT / 'KnowledgeBank' / 'vocab_examples_n4.md'
curated = {}
if CURATED_PATH.exists():
    text = CURATED_PATH.read_text(encoding='utf-8')
    line_re = re.compile(r'^([^|#\n]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*$', re.MULTILINE)
    for m in line_re.finditer(text):
        form = m.group(1).strip()
        ja = m.group(2).strip()
        en = m.group(3).strip()
        # Skip header / format docs
        if form.startswith(('#', 'Format', '**', 'KANJI', 'FORM')):
            continue
        if form in ('form', 'Format'):
            continue
        if not all_kanji_in_scope(ja):
            print(f'  Skipping out-of-scope sentence for {form}: {ja}')
            continue
        curated.setdefault(form, []).append({
            'ja': ja,
            'translation_en': en,
        })
print(f'Loaded {len(curated)} curated example sets from {CURATED_PATH.name}')

enriched = 0
already = 0
for v in vocab_data['entries']:
    form = v.get('form', '')
    if not form:
        continue
    if form in curated:
        if v.get('examples'):
            already += 1
            continue
        v['examples'] = curated[form]
        enriched += 1

print(f'Enriched {enriched} vocab entries (skipped {already} already populated)')

(ROOT / 'data' / 'vocab.json').write_text(
    json.dumps(vocab_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'data/vocab.json updated')
