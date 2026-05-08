"""IMP-139: backfill `frequency_rank` on vocab.json entries by
matching `form` (and falling back to `reading`) against the
University of Leeds Japanese Internet Corpus frequency list
(CC-BY, distributed via hingston/japanese).

Source: https://github.com/hingston/japanese
  - 44492-japanese-words-latin-lines-removed.txt
  - rank = position in the file (1-based)
  - License: CC-BY 2.5 (University of Leeds Corpus)

Lookup strategy:
  1. Try `form` exact match (kanji/kana surface form).
  2. Fall back to `reading` exact match (kana-only form).
  3. If neither hits in top-44492, leave field absent.

Provenance: 'leeds_corpus_lookup' to make clear this is a coarse
internet-text proxy, not BCCWJ. The audit asked for BCCWJ; this
ships a freely-redistributable proxy now and tags provenance for
future swap.
"""
from __future__ import annotations
import io
import json
import socket
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
socket.setdefaulttimeout(30)

CACHE = ROOT / 'not-required' / 'tools-archive' / '_cache_leeds_jp_freq_44492.txt'
URL = 'https://raw.githubusercontent.com/hingston/japanese/master/44492-japanese-words-latin-lines-removed.txt'

if not CACHE.exists():
    print(f'Fetching {URL} ...')
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='replace')
    CACHE.write_text(data, encoding='utf-8')
    print(f'  cached to {CACHE.name}')
else:
    print(f'Using cached {CACHE.name}')
    data = CACHE.read_text(encoding='utf-8')

words = [l.strip() for l in data.splitlines() if l.strip()]
print(f'Corpus entries: {len(words)}')

# Build rank index: word -> 1-based rank (first occurrence wins)
rank = {}
for i, w in enumerate(words, start=1):
    if w not in rank:
        rank[w] = i

vocab_path = ROOT / 'data' / 'vocab.json'
vdata = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = vdata['entries']

assigned = 0
fallback_reading = 0
unmatched = 0
unmatched_samples = []

for e in entries:
    if 'frequency_rank' in e:
        continue  # respect any pre-existing curated rank

    form = (e.get('form') or '').strip()
    reading = (e.get('reading') or '').strip()

    r = rank.get(form)
    if r is None and reading and reading != form:
        r = rank.get(reading)
        if r is not None:
            fallback_reading += 1

    if r is not None:
        e['frequency_rank'] = r
        e['frequency_rank_source'] = 'leeds_corpus_internet_jp'
        e['frequency_rank_provenance'] = 'auto_extracted'
        assigned += 1
    else:
        unmatched += 1
        if len(unmatched_samples) < 12:
            unmatched_samples.append(f"{form} / {reading}")

vocab_path.write_text(
    json.dumps(vdata, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print()
print(f'Total vocab entries:        {len(entries)}')
print(f'Assigned frequency_rank:    {assigned}')
print(f'  via form match:           {assigned - fallback_reading}')
print(f'  via reading fallback:     {fallback_reading}')
print(f'Unmatched (no rank):        {unmatched}')
print(f'\nCoverage: {assigned}/{len(entries)} ({100*assigned/len(entries):.0f}%)')
print(f'\nUnmatched samples:')
for s in unmatched_samples:
    print(f'  {s}')
