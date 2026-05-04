"""Enrich kanji_n4.md and data/kanji.json with per-glyph examples.

For each N4-tier kanji entry without examples, finds 2-5 vocab entries
whose form contains that kanji and uses them as examples.

Vocab pool: N4 vocab + N5 sibling vocab. Many N4 kanji appear primarily
in N5 compounds (e.g., 京 → 東京). Drawing from the N5 sibling vocab
gives meaningful coverage for the 66 N4 kanji not present in N4-only vocab.

Idempotent: skips entries that already have examples.
"""
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
N5 = ROOT.parent / 'N5'

# Load
kanji = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']
# Also load N5 sibling vocab so we can pull example words for N4 kanji
# whose primary use is in N5 compounds (e.g., 京 → 東京).
n5_vocab = []
n5_vocab_path = N5 / 'data' / 'vocab.json'
if n5_vocab_path.exists():
    n5_vocab = json.loads(n5_vocab_path.read_text(encoding='utf-8')).get('entries', [])
    # Tag for downstream prioritisation
    for e in n5_vocab:
        e['_source'] = 'n5_sibling'
whitelist = set(json.loads((ROOT / 'data' / 'n4_kanji_whitelist.json').read_text(encoding='utf-8')))

KANJI_RE = re.compile(r'[一-鿿]')

def all_kanji_in_scope(s):
    return all((not KANJI_RE.match(c)) or c in whitelist for c in s)

# Filter vocab to in-scope entries (forms whose all kanji are in N4 whitelist).
# Combine N4 vocab + N5 sibling vocab — both pools contribute candidate
# example words. The whitelist (N5 ∪ N4 = 249 kanji) bounds what's allowed.
combined_vocab = list(vocab) + list(n5_vocab)
in_scope_vocab = [v for v in combined_vocab if all_kanji_in_scope(v.get('form', ''))]
print(f'In-scope vocab pool: {len(in_scope_vocab)} (N4: {len(vocab)} + N5 sibling: {len(n5_vocab)})')

# Build: kanji -> list of vocab entries containing it
kanji_to_vocab = {}
for v in in_scope_vocab:
    form = v.get('form', '')
    if not form:
        continue
    # Skip kana-only forms
    if not any(KANJI_RE.match(c) for c in form):
        continue
    for c in form:
        if KANJI_RE.match(c) and c in whitelist:
            kanji_to_vocab.setdefault(c, []).append(v)

# Load curated kanji examples (glyph -> [{form, reading, gloss}, ...])
CURATED_PATH = ROOT / 'KnowledgeBank' / 'kanji_examples_n4.md'
curated = {}
if CURATED_PATH.exists():
    text = CURATED_PATH.read_text(encoding='utf-8')
    # Format: `{glyph} | form1(reading1,gloss1) | form2(reading2,gloss2) | ...`
    line_re = re.compile(r'^([一-鿿])\s*\|\s*(.+)$', re.MULTILINE)
    field_re = re.compile(r'([^(|]+?)\s*\(\s*([^,]+?)\s*,\s*([^)]+?)\s*\)')
    for m in line_re.finditer(text):
        g = m.group(1)
        rest = m.group(2)
        examples = []
        for fm in field_re.finditer(rest):
            examples.append({
                'form': fm.group(1).strip(),
                'reading': fm.group(2).strip(),
                'gloss': fm.group(3).strip(),
            })
        if examples:
            curated[g] = examples
    print(f'Loaded {len(curated)} curated kanji example sets from {CURATED_PATH.name}')

# Enrich each kanji entry. ALWAYS overwrite if any current example uses
# out-of-scope kanji — otherwise prior bad runs of this enricher
# would persist.
enriched = 0
KANJI_RE_LOCAL = re.compile(r'[一-鿿]')
def has_oos(s):
    return any(KANJI_RE_LOCAL.match(c) and c not in whitelist for c in s)

for entry in kanji['entries']:
    g = entry.get('glyph')
    if not g:
        continue
    # If existing examples are clean, keep them. If any contain OOS kanji,
    # wipe and rebuild.
    cur = entry.get('examples') or []
    if cur and not any(has_oos(e.get('form', '')) for e in cur):
        continue
    if cur:
        entry['examples'] = []
    examples = []
    # First try the auto-discovered candidates (in-scope vocab forms)
    candidates = kanji_to_vocab.get(g, [])
    if candidates:
        n4_first = sorted(candidates, key=lambda v: 0 if v.get('tier') == 'core_n4' else 1)
        seen_forms = set()
        for v in n4_first:
            form = v.get('form', '')
            if form in seen_forms:
                continue
            seen_forms.add(form)
            examples.append({
                'form': form,
                'reading': v.get('reading', ''),
                'gloss': (v.get('gloss', '') or '').split(';')[0].strip(),
            })
            if len(examples) >= 5:
                break
    # Fallback: use the curated kanji-examples file. Auto-filter any
    # example whose form uses out-of-scope kanji (JA-16 satisfies if all
    # surviving examples have all-in-scope kanji).
    if not examples and g in curated:
        for cex in curated[g]:
            if all_kanji_in_scope(cex.get('form', '')):
                examples.append(cex)
    if examples:
        entry['examples'] = examples
        enriched += 1

print(f'Enriched {enriched} kanji with examples')

# Write back data/kanji.json
(ROOT / 'data' / 'kanji.json').write_text(
    json.dumps(kanji, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'data/kanji.json updated')

# Update KnowledgeBank/kanji_n4.md to include examples per glyph
kb_path = ROOT / 'KnowledgeBank' / 'kanji_n4.md'
text = kb_path.read_text(encoding='utf-8')
# For each kanji entry block, find the closing line and append examples
# Block format: `- **{kanji}**  (tier: ...)` followed by sub-bullets

def replace_block(text, glyph, examples):
    """Add an `examples` sub-bullet to the block starting at `- **{glyph}**`."""
    pattern = re.compile(
        r'(- \*\*' + re.escape(glyph) + r'\*\*\s+\(tier:[^\n]*\n'
        r'(?:  - [^\n]*\n)+)',
        re.MULTILINE
    )
    m = pattern.search(text)
    if not m:
        return text
    block = m.group(1)
    if '  - examples:' in block:
        return text  # already has examples
    ex_strs = [f'{e["form"]}({e["reading"]}, {e["gloss"]})' for e in examples[:5]]
    new_line = '  - examples: ' + '; '.join(ex_strs) + '\n'
    return text[:m.end()] + new_line + text[m.end():]

updated = 0
for entry in kanji['entries']:
    if not entry.get('examples'):
        continue
    g = entry['glyph']
    new_text = replace_block(text, g, entry['examples'])
    if new_text != text:
        text = new_text
        updated += 1

kb_path.write_text(text, encoding='utf-8')
print(f'kanji_n4.md updated: {updated} entries got examples line')
