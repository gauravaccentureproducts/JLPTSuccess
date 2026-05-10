"""IMP-139 final pass: replace the rank=44999 placeholder on 267
entries with realistic section-based ranks.

Many of these are common N5 words (pronouns, family terms, body
parts, basic verbs in kana) that incorrectly sort last. The real
frequency for a kana-only beginner form is similar to the kanji
form's frequency, which IS in the Leeds corpus.

Strategy: each section has a base rank-band (informed by Leeds
corpus where the section's anchor words DID match). Within a
section we spread placeholders across the band based on their
position in the entries array.

Provenance: 'section_band_estimate' — distinguishes from exact
matches and substring proxies. Native curation can refine later.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Section-name prefix -> (start_rank, end_rank) — frequency band.
# Based on observed Leeds rank for each section's anchor word
# (e.g. "1. People - Pronouns" → わたし=rank-1, so band 1000-1800).
SECTION_BANDS = {
    '1.':  (1000, 1800),    # Pronouns
    '2.':  (1500, 2800),    # Family
    '3.':  (2000, 3500),    # Roles
    '4.':  (1800, 3000),    # Body parts
    '5.':  (2500, 4000),    # Body parts cont.
    '6.':  (800, 2200),     # Question words (very common)
    '7.':  (1500, 3500),    # Numbers
    '8.':  (2500, 4000),    # Counters
    '9.':  (2500, 4000),    # Time-Hours
    '10.': (1500, 3500),    # Time-General
    '11.': (1800, 3500),    # Time-Days/Weeks/Months
    '12.': (3000, 5000),    # Time-Past/Future markers
    '13.': (2000, 4500),    # Locations
    '14.': (3000, 5000),    # Directions
    '15.': (3500, 5500),    # Weather
    '16.': (3000, 5500),    # Food/Drink
    '17.': (3500, 5500),    # Food cont.
    '18.': (3500, 5500),    # Drinks
    '19.': (3500, 5500),    # Restaurants
    '20.': (3500, 5500),    # Tableware
    '21.': (4000, 6000),    # Cooking
    '22.': (3000, 5000),    # Daily life
    '23.': (3500, 5500),    # Transport
    '24.': (2500, 4500),    # School and Study
    '25.': (3000, 5000),    # Work
    '26.': (3000, 4500),    # House and Furniture
    '27.': (1500, 4000),    # Verbs Group 1
    '28.': (2000, 4000),    # Verbs Group 2
    '29.': (1800, 4000),    # Verbs Irregular/する
    '30.': (2500, 4500),    # Adjective antonyms
    '31.': (2000, 4000),    # い-Adjectives
    '32.': (2500, 4000),    # な-Adjectives
    '33.': (2500, 4500),    # Adverbs
    '34.': (3500, 5500),    # Conjunctions
    '35.': (1500, 3500),    # Particles
    '36.': (2500, 5000),    # Greetings/Set Phrases
    '37.': (3500, 6000),    # Common Nouns - Misc
    '38.': (4000, 7000),    # Loanwords misc
    '39.': (3000, 5000),    # Function/filler
    '40.': (3500, 6500),    # Other
}


def section_band(section: str) -> tuple[int, int]:
    """Return (lo, hi) rank band for the section. Default mid-range."""
    if not section:
        return (5000, 8000)
    prefix = section.split()[0]
    return SECTION_BANDS.get(prefix, (5000, 8000))


vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

# Group placeholder entries by section, preserving array order
by_section = defaultdict(list)
for i, e in enumerate(entries):
    if e.get('frequency_rank_source') == 'low_frequency_placeholder':
        by_section[e.get('section', '')].append((i, e))

updated = 0
for section, items in by_section.items():
    lo, hi = section_band(section)
    n = len(items)
    if n == 0:
        continue
    if n == 1:
        # Single entry: place at midpoint
        items[0][1]['frequency_rank'] = (lo + hi) // 2
        items[0][1]['frequency_rank_source'] = 'section_band_estimate'
        items[0][1]['frequency_rank_provenance'] = 'auto_extracted'
        updated += 1
        continue
    # Spread evenly across band based on position-in-section
    span = hi - lo
    for j, (i, e) in enumerate(items):
        rank = lo + int(j * span / max(1, n - 1))
        e['frequency_rank'] = rank
        e['frequency_rank_source'] = 'section_band_estimate'
        e['frequency_rank_provenance'] = 'auto_extracted'
        updated += 1

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Verify no entry still at the placeholder rank
still_placeholder = sum(1 for e in entries
                        if e.get('frequency_rank_source') == 'low_frequency_placeholder')
print(f'Re-ranked: {updated} entries')
print(f'Still placeholder: {still_placeholder}')
print()
# Show new rank distribution
from collections import Counter
by_band = Counter()
for e in entries:
    r = e.get('frequency_rank', 99999)
    if r < 1000: by_band['<1k'] += 1
    elif r < 2000: by_band['1-2k'] += 1
    elif r < 3000: by_band['2-3k'] += 1
    elif r < 5000: by_band['3-5k'] += 1
    elif r < 10000: by_band['5-10k'] += 1
    elif r < 20000: by_band['10-20k'] += 1
    else: by_band['>20k'] += 1
print('Rank distribution across all 1000 entries:')
for band, n in [('<1k',by_band['<1k']),('1-2k',by_band['1-2k']),('2-3k',by_band['2-3k']),
                ('3-5k',by_band['3-5k']),('5-10k',by_band['5-10k']),
                ('10-20k',by_band['10-20k']),('>20k',by_band['>20k'])]:
    print(f'  {band:7} {n}')
