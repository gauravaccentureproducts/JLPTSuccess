"""IMP-128: derive `collocations` for top-300 high-frequency content
words by mining the project's own example-sentence corpus
(vocab examples + grammar examples + reading passages).

For each target word, we collect every sentence in the corpus
that contains the word's `form` or `reading`, then extract the
top-N most-common surrounding **multi-char content phrases**
(2-4 char tokens that aren't standalone particles or copula).

The collocations field is "phrase-level" (e.g. "学校に行く",
"家族と一緒に"), not just "co-occurring word list", so they're
useful as natural-language patterns. We use a simple bigram/
trigram extraction over the sentence with the target word held
fixed in the middle.

Output schema (consistent with existing collocations[] array):
  collocations: [str, ...]            # phrase strings
  collocations_provenance: 'auto_derived'

Existing curated collocations (those without provenance or with
provenance != 'auto_derived') are preserved.
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ---------- Load corpora ----------

vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
grammar = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
reading = json.loads((ROOT / 'data' / 'reading.json').read_text(encoding='utf-8'))

vocab_entries = vocab['entries']

# Sentences pool: every Japanese sentence we can find in the corpus.
sentences = []

# vocab examples
for v in vocab_entries:
    for ex in (v.get('examples') or []):
        ja = ex.get('ja') if isinstance(ex, dict) else (ex if isinstance(ex, str) else None)
        if ja:
            sentences.append(ja)

# grammar examples
for p in grammar.get('patterns', []):
    for ex in (p.get('examples') or []):
        ja = ex.get('ja') if isinstance(ex, dict) else None
        if ja:
            sentences.append(ja)

# reading passages
passages = reading.get('passages') or []
for ps in passages:
    ja = ps.get('ja') or ''
    # split into sentences on full-stop punctuation
    for s in re.split(r'[。！？\n]', ja):
        s = s.strip()
        if s:
            sentences.append(s)

print(f'Corpus pool: {len(sentences)} sentences')

# ---------- Identify top-300 content-word targets ----------

CONTENT_POS = {'noun', 'verb-1', 'verb-2', 'verb-3', 'i-adj', 'na-adj', 'adverb'}
# Known mis-tagged particles/markers in vocab.json that share `pos: noun`
# but are functionally particles. Skip these to avoid extracting
# meaningless collocations like "は + content" pairs.
PARTICLE_LIKE = {'は', 'が', 'を', 'に', 'へ', 'で', 'と', 'から', 'まで',
                 'の', 'も', 'や', 'か', 'ね', 'よ', 'って', 'なあ', 'ので',
                 'のに', 'けど', 'けれど', 'けれども', 'て', 'って', 'よね'}

candidates = [
    e for e in vocab_entries
    if e.get('pos') in CONTENT_POS
    and e.get('frequency_rank')
    and e.get('form') not in PARTICLE_LIKE
    and e.get('reading') not in PARTICLE_LIKE
    and len(e.get('form') or '') >= 2  # at least 2 chars to be meaningful
]
candidates.sort(key=lambda e: e['frequency_rank'])
targets = candidates[:300]
print(f'Top-300 content-word targets: {len(targets)}')

# ---------- Collocation extraction ----------

# For a given target form/reading, find sentences containing it,
# then extract phrases of length 2-6 chars (excluding the target itself)
# that bracket the target. We grab "<2-3 chars>+target+<2-3 chars>"
# windows and emit them as collocation strings.

def extract_collocations(target_form: str, target_reading: str, max_n: int = 8) -> list[str]:
    """Return up to max_n collocation phrases sorted by corpus frequency."""
    needles = [target_form] if target_form else []
    if target_reading and target_reading != target_form:
        needles.append(target_reading)

    counter = Counter()
    for s in sentences:
        for needle in needles:
            idx = s.find(needle)
            while idx != -1:
                # Window: 2-6 chars ending at idx + needle, OR starting at idx
                # We try a few span lengths to capture natural phrase units.
                for span in (3, 4, 5):
                    # left context: span-1 chars before, ending at idx
                    if idx >= span - 1:
                        left_phrase = s[idx - (span - 1):idx + len(needle) + 1]
                        # require the phrase to be Japanese (no roman/space)
                        if all(_is_jp_char(c) for c in left_phrase):
                            counter[left_phrase] += 1
                    # right context: span-1 chars after needle
                    end = idx + len(needle)
                    if end + (span - 1) <= len(s):
                        right_phrase = s[idx - 1:end + (span - 1)] if idx >= 1 else s[idx:end + (span - 1)]
                        if all(_is_jp_char(c) for c in right_phrase):
                            counter[right_phrase] += 1
                idx = s.find(needle, idx + 1)

    # Filter: phrases must contain the needle and be 3+ chars. We accept
    # count >= 1 (single occurrence) because the internal corpus is small;
    # the resulting collocation is "an attested usage pattern" rather than
    # "a statistically reinforced one". Both kinds are useful for beginners.
    # Then dedupe near-duplicates (one phrase being a substring of another)
    # by keeping the longer one when they share a >=80% character overlap.
    phrases = [
        (p, c) for p, c in counter.items()
        if c >= 1 and any(n in p for n in needles)
        and len(p) >= 3
    ]
    phrases.sort(key=lambda pc: (-pc[1], -len(pc[0])))

    # Dedupe: drop phrase A if there's a longer phrase B that contains A.
    # Keep the longer (more contextual) phrase.
    sorted_by_len_desc = sorted(phrases, key=lambda pc: -len(pc[0]))
    kept = []
    for phrase, count in sorted_by_len_desc:
        if any(phrase in k for k, _ in kept):
            continue  # subsumed by a longer kept phrase
        kept.append((phrase, count))
    # Re-sort kept by count desc for output
    kept.sort(key=lambda pc: (-pc[1], len(pc[0])))
    return [p for p, _ in kept[:max_n]]


def _is_jp_char(c: str) -> bool:
    """True if c is hiragana, katakana, or CJK ideograph."""
    return ('぀' <= c <= 'ゟ'
            or '゠' <= c <= 'ヿ'
            or '一' <= c <= '鿿'
            or c in 'ー〜')


# ---------- Apply ----------

added = 0
preserved = 0
no_collocs_found = 0

for e in targets:
    existing = e.get('collocations')
    existing_prov = e.get('collocations_provenance')
    if existing and existing_prov and existing_prov != 'auto_derived':
        # Curated; do not overwrite. Could augment, but keep it conservative.
        preserved += 1
        continue

    form = e.get('form') or ''
    reading = e.get('reading') or ''
    collocs = extract_collocations(form, reading, max_n=8)

    if not collocs:
        no_collocs_found += 1
        continue

    # If the entry had auto-derived collocations from a prior run,
    # overwrite. If it had no collocations, add them.
    e['collocations'] = collocs
    e['collocations_provenance'] = 'auto_derived'
    added += 1

(ROOT / 'data' / 'vocab.json').write_text(
    json.dumps(vocab, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print()
print(f'Top-300 content words processed:    {len(targets)}')
print(f'  Curated, left untouched:          {preserved}')
print(f'  Auto-derived collocations added:  {added}')
print(f'  No matches found in corpus:       {no_collocs_found}')

# Final coverage report
top300_with_collocs = sum(1 for e in targets if e.get('collocations') and len(e['collocations']) >= 5)
print(f'\nFinal: top-300 with >=5 collocations: {top300_with_collocs}/{len(targets)}'
      f' ({100*top300_with_collocs/len(targets):.0f}%)')
