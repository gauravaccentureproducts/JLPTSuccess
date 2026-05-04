"""N4 corpus coverage report.

Compares our authored corpora against the source-of-truth inventories:
- Kanji:   data/n4_kanji_whitelist.json vs n4-kanji-inventory.md
- Vocab:   data/vocab.json vs n4-vocab-inventory-full.md (or sample)
- Grammar: data/grammar.json vs n4-grammar-inventory.md

For each layer, reports:
  - inventory_total: entries in source inventory
  - our_total: entries we have
  - inventory_missing: in source but not in ours (gap to close)
  - extra_in_ours: in ours but not in source (likely N5-prereq inheritance)

Output: feedback/coverage-report-n4.md
"""
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

# ---------- Kanji ----------
print('[1/3] Kanji coverage...')
inv_text = (ROOT / 'n4-kanji-inventory.md').read_text(encoding='utf-8')
KANJI_RE = re.compile(r'^([一-鿿]) \| ', re.MULTILINE)
inv_kanji = set(KANJI_RE.findall(inv_text))
our_kanji_whitelist = set(json.loads(
    (ROOT / 'data' / 'n4_kanji_whitelist.json').read_text(encoding='utf-8')))
n5_whitelist = set(json.loads(
    (ROOT.parent / 'N5' / 'data' / 'n5_kanji_whitelist.json').read_text(encoding='utf-8')))

kanji_inventory_only = inv_kanji - our_kanji_whitelist
kanji_extras = our_kanji_whitelist - inv_kanji  # mostly N5 prereqs
kanji_extras_n5 = kanji_extras & n5_whitelist
kanji_extras_other = kanji_extras - n5_whitelist

print(f'  Inventory: {len(inv_kanji)} kanji')
print(f'  Whitelist: {len(our_kanji_whitelist)} kanji')
print(f'  Missing from whitelist: {len(kanji_inventory_only)}')
print(f'  N5-prereq inherited: {len(kanji_extras_n5)}')
print(f'  Other extras: {len(kanji_extras_other)}')

# ---------- Vocab ----------
print('\n[2/3] Vocab coverage...')
vocab_inv_path = ROOT / 'n4-vocab-inventory-full.md'
if not vocab_inv_path.exists():
    vocab_inv_path = ROOT / 'n4-vocab-inventory-sample.md'
vocab_inv_text = vocab_inv_path.read_text(encoding='utf-8')
# Format: `FORM | READING | MEANING | POS`
ENTRY_RE = re.compile(r'^([^|#\s\n][^|\n]*?) \| ([^|\n]+?) \| ([^|\n]+?) \| ([^\n]+)$', re.MULTILINE)
inv_vocab = set()
for m in ENTRY_RE.finditer(vocab_inv_text):
    form = m.group(1).strip()
    if form.startswith(('**', '|', '---', 'KANJI', 'FORM', 'Form')):
        continue
    inv_vocab.add(form)

our_vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
our_vocab_forms = set(v['form'] for v in our_vocab['entries'])
our_n4_forms = set(v['form'] for v in our_vocab['entries'] if v.get('tier') == 'core_n4')

vocab_missing = inv_vocab - our_vocab_forms
vocab_n5_inherited = our_vocab_forms - our_n4_forms

print(f'  Inventory: {len(inv_vocab)} forms')
print(f'  Total in our vocab.json: {len(our_vocab_forms)}')
print(f'  N4-tier in ours: {len(our_n4_forms)}')
print(f'  N5-prereq inherited: {len(vocab_n5_inherited)}')
print(f'  Missing from ours: {len(vocab_missing)}')

# ---------- Grammar ----------
print('\n[3/3] Grammar coverage...')
gram_inv_text = (ROOT / 'n4-grammar-inventory.md').read_text(encoding='utf-8')
GRAM_RE = re.compile(r'^([^|#\s\n][^|\n]*?) \| ([^\n]+)$', re.MULTILINE)
inv_grammar = set()
for m in GRAM_RE.finditer(gram_inv_text):
    pat = m.group(1).strip()
    if pat.startswith(('**', '|', '---')) or pat in ('PATTERN', 'Format', 'Source', 'Cross-reference'):
        continue
    inv_grammar.add(pat)

our_grammar = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
our_grammar_patterns = set(p['pattern'] for p in our_grammar['patterns'])
our_n4_patterns = set(p['pattern'] for p in our_grammar['patterns'] if p.get('tier') == 'core_n4')

# Inventory may have parenthesized readings; we kana-folded out-of-scope kanji.
# So a pattern like "場合は（ばあいは）" in inventory might be "ばあいは" in ours.
# Match by stripping parenthetical readings for fairness.
def normalize_pattern(p):
    # Strip parenthesized reading like （xxx）
    return re.sub(r'（[ぁ-んー〜]+）', '', p).strip()

our_grammar_normalized = {normalize_pattern(p): p for p in our_grammar_patterns}
inv_grammar_normalized = {normalize_pattern(p): p for p in inv_grammar}

grammar_missing = []
for nkey, original in inv_grammar_normalized.items():
    # Skip meta-topics that we deliberately dropped
    if original in ('意向形（いこうけい）', '受身形（うけみけい）',
                    '他動詞 & 自動詞', '他動詞', '自動詞'):
        continue
    if nkey in our_grammar_normalized:
        continue
    # Try fuzzy: pattern present anywhere
    if any(nkey in p or p in nkey for p in our_grammar_normalized.keys()):
        continue
    grammar_missing.append(original)

print(f'  Inventory: {len(inv_grammar)} patterns')
print(f'  Total in our grammar.json: {len(our_grammar_patterns)}')
print(f'  N4-tier in ours: {len(our_n4_patterns)}')
print(f'  Missing from ours: {len(grammar_missing)}')

# ---------- Write report ----------
report_path = ROOT / 'feedback' / 'coverage-report-n4.md'
report_path.parent.mkdir(parents=True, exist_ok=True)

lines = ['# N4 Corpus Coverage Report', '',
         f'Generated: {Path(__file__).name}', '',
         '## Summary', '',
         '| Layer | Inventory | Our total | N4-tier | N5-inherited | Missing |',
         '|---|---|---|---|---|---|',
         f'| Kanji   | {len(inv_kanji)} | {len(our_kanji_whitelist)} | {len(our_kanji_whitelist - n5_whitelist)} | {len(kanji_extras_n5)} | {len(kanji_inventory_only)} |',
         f'| Vocab   | {len(inv_vocab)} | {len(our_vocab_forms)} | {len(our_n4_forms)} | {len(vocab_n5_inherited)} | {len(vocab_missing)} |',
         f'| Grammar | {len(inv_grammar)} | {len(our_grammar_patterns)} | {len(our_n4_patterns)} | {len(our_grammar_patterns) - len(our_n4_patterns)} | {len(grammar_missing)} |',
         '',
         '## Kanji gaps',
         '',
         f'{len(kanji_inventory_only)} kanji in inventory but not in our whitelist:',
         '']
if kanji_inventory_only:
    lines.append('  ' + ''.join(sorted(kanji_inventory_only)))
else:
    lines.append('  (none — full inventory captured)')

lines.extend(['', '## Vocab gaps', '',
              f'{len(vocab_missing)} forms in inventory but not in our vocab.json:', ''])
if vocab_missing:
    for form in sorted(vocab_missing)[:50]:
        lines.append(f'- {form}')
    if len(vocab_missing) > 50:
        lines.append(f'- ... and {len(vocab_missing) - 50} more')
else:
    lines.append('(none — full inventory captured)')

lines.extend(['', '## Grammar gaps', '',
              f'{len(grammar_missing)} patterns in inventory but not in our grammar.json:', ''])
if grammar_missing:
    for pat in sorted(grammar_missing)[:50]:
        lines.append(f'- {pat}')
    if len(grammar_missing) > 50:
        lines.append(f'- ... and {len(grammar_missing) - 50} more')
else:
    lines.append('(none — full inventory captured)')

lines.extend(['', '## Recommendations', ''])
if kanji_inventory_only:
    lines.append(f'- Add {len(kanji_inventory_only)} missing kanji to whitelist + KB catalogue.')
if vocab_missing:
    lines.append(f'- Add {len(vocab_missing)} missing vocab forms (or document why excluded).')
if grammar_missing:
    lines.append(f'- Add {len(grammar_missing)} missing grammar patterns.')
if not (kanji_inventory_only or vocab_missing or grammar_missing):
    lines.append('- Coverage is complete vs source inventories. Next gap: vs Tanos N4 / Bunpro N4.')

report_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'\nReport: {report_path.relative_to(ROOT)}')
