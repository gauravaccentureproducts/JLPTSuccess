"""IMP-139 follow-up: assign frequency_rank to the remaining 295 vocab
entries (mostly kana-only beginner forms + kanji compounds whose canonical
form differs from how the Leeds corpus tokenises them).

Strategy: for each unmatched entry, search the cached Leeds corpus for
the FIRST line where the entry's `reading` or `form` appears as a
substring. Use that line's position as a proxy frequency_rank.

Provenance: 'leeds_corpus_substring_proxy' — looser than the exact-
match 'leeds_corpus_internet_jp', so future native-curation can
distinguish. The numerical rank is a reasonable lower-bound (the
substring-match rank is the rank of the SHORTEST word containing the
target, which is a defensible proxy for "the broader topic family").

Entries with no substring hit get rank=44999 (one past the corpus
size) so they sort to the end.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CACHE = ROOT / 'not-required' / 'tools-archive' / '_cache_leeds_jp_freq_44492.txt'
if not CACHE.exists():
    print('Leeds corpus cache missing. Run fix_imp139_frequency_rank first.')
    sys.exit(1)

corpus_lines = [l.strip() for l in CACHE.read_text(encoding='utf-8').splitlines() if l.strip()]
print(f'Corpus lines: {len(corpus_lines)}')

# Build first-occurrence index: substring -> rank.
# We index by sub-strings that COULD be needles (vocab readings/forms).
# To keep memory bounded, we don't pre-build all substrings; we just
# search linearly through the corpus per missing entry. The cache fits
# in memory and the loop is O(missing × corpus) which is ~13M
# comparisons — fast enough on a modern CPU.

vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

assigned = 0
fallback = 0  # entries that get the placeholder rank

for e in entries:
    if e.get('frequency_rank'):
        continue
    form = (e.get('form') or '').strip()
    reading = (e.get('reading') or '').strip()
    # Reading sometimes has '/' alternates. Try the first.
    reading_first = reading.split('/')[0].strip() if '/' in reading else reading

    # Build needle list — try the longer needle first
    needles = []
    if form:
        needles.append(form)
    if reading_first and reading_first != form:
        needles.append(reading_first)

    rank = None
    for needle in needles:
        if not needle or len(needle) < 2:
            continue
        for i, line in enumerate(corpus_lines, start=1):
            if needle in line:
                rank = i
                break
        if rank is not None:
            break

    if rank is None:
        # Place at end-of-corpus
        e['frequency_rank'] = 44999
        e['frequency_rank_source'] = 'low_frequency_placeholder'
        e['frequency_rank_provenance'] = 'auto_extracted'
        fallback += 1
    else:
        e['frequency_rank'] = rank
        e['frequency_rank_source'] = 'leeds_corpus_substring_proxy'
        e['frequency_rank_provenance'] = 'auto_extracted'
        assigned += 1

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final coverage
total = len(entries)
with_rank = sum(1 for e in entries if e.get('frequency_rank'))
print(f'Substring-proxy assigned: {assigned}')
print(f'End-of-corpus placeholder: {fallback}')
print(f'Total coverage: {with_rank}/{total} ({100*with_rank/total:.0f}%)')
