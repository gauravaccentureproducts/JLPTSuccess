"""IMP-127: backfill `pitch_accent` on vocab.json entries by
matching against the Kanjium pitch-accent dictionary
(CC BY-SA 4.0, ~124k entries derived from EDICT family).

Source: https://github.com/mifunetoshiro/kanjium
  data/source_files/raw/accents.txt — TSV: form\\treading\\tdrop
  drop is mora-position (0 = heiban, N = drop after Nth mora).
  Multiple drops separated by comma — we keep the first
  (statistically most common in Tokyo standard).

License: CC BY-SA 4.0 — derived from EDRDG EDICT family.
Compatible with this project's content license.

Mora count rules:
  - small kana (ゃゅょぁぃぅぇぉっャュョァィゥェォッ) merge with
    the preceding char and DO NOT count as separate mora
  - ー (long mark) counts as 1 mora
  - everything else = 1 mora per char

Lookup strategy:
  1. (form, reading) exact match
  2. (form, reading) reading-only match (kana entries)

Each newly-imported entry tagged with:
  pitch_accent: {mora: N, drop: D}
  pitch_accent_provenance: 'kanjium_lookup'

Existing entries with pitch_accent already populated are
preserved (respect llm_curated reviews from earlier passes).
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
socket.setdefaulttimeout(60)

CACHE = ROOT / 'not-required' / 'tools-archive' / '_cache_kanjium_accents.txt'
URL = 'https://raw.githubusercontent.com/mifunetoshiro/kanjium/master/data/source_files/raw/accents.txt'

if not CACHE.exists():
    print(f'Fetching {URL} ... (~3 MB)')
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=45).read().decode('utf-8', errors='replace')
    CACHE.write_text(data, encoding='utf-8')
    print(f'  cached to {CACHE.name}')
else:
    print(f'Using cached {CACHE.name}')
    data = CACHE.read_text(encoding='utf-8')

# Build lookup tables.
# Mora-count convention (Tokyo standard, per NHK/OJAD):
#   - small ya/yu/yo + small a/i/u/e/o MERGE with the preceding
#     char (they're palatalised + foreign-loan variants like ティ).
#   - small tsu (っ/ッ — the sokuon/geminate) IS its own mora.
#   - long mark (ー) IS its own mora.
# Earlier draft incorrectly grouped sokuon with the merging set,
# producing drop>mora for words like こっち / みっつ.
SMALL_MERGE = set('ゃゅょぁぃぅぇぉャュョァィゥェォ')

# (form, reading) -> first drop value
by_form_reading = {}
# reading-only -> first drop value (for kana entries)
by_reading = {}

for line in data.splitlines():
    parts = line.rstrip('\n').split('\t')
    if len(parts) != 3:
        continue
    form, reading, drops = parts
    if not drops:
        continue
    drop = drops.split(',')[0].strip()
    if not drop or not drop.lstrip('-').isdigit():
        continue
    drop_int = int(drop)
    # Use form as primary key; reading-only fallback prefers the
    # earliest entry (more common reading-context).
    if form:
        by_form_reading.setdefault((form, reading), drop_int)
    if reading:
        by_reading.setdefault(reading, drop_int)

print(f'Kanjium entries indexed: {len(by_form_reading)} by (form,reading), {len(by_reading)} by reading')


def count_mora(reading: str) -> int:
    """Count mora in a kana string per Tokyo-standard convention.

    Small ya/yu/yo + small a/i/u/e/o merge with the preceding char
    (do NOT count). Sokuon っ/ッ and long mark ー DO count.
    """
    return sum(1 for c in reading if c not in SMALL_MERGE)


vocab_path = ROOT / 'data' / 'vocab.json'
vdata = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = vdata['entries']

assigned = 0
form_match = 0
reading_match = 0
unmatched = 0
unmatched_samples = []
preserved = 0

for e in entries:
    # Preserve human-curated pitch (llm_curated / native_reviewed) but
    # ALLOW re-computation of prior `kanjium_lookup` rows so we can fix
    # the mora-count bug that mistakenly merged sokuon with the small
    # kana set in an earlier draft of this script.
    prov = e.get('pitch_accent_provenance')
    if e.get('pitch_accent') and prov and prov != 'kanjium_lookup':
        preserved += 1
        continue

    form = (e.get('form') or '').strip()
    reading = (e.get('reading') or '').strip()
    if not reading:
        continue

    drop = by_form_reading.get((form, reading))
    if drop is not None:
        form_match += 1
    else:
        drop = by_reading.get(reading)
        if drop is not None:
            reading_match += 1

    if drop is None:
        unmatched += 1
        if len(unmatched_samples) < 12:
            unmatched_samples.append(f"{form} / {reading}")
        continue

    mora = count_mora(reading)
    # Sanity: drop must be in [0, mora]
    if drop < 0 or drop > mora:
        # Inconsistent — skip rather than ship bad data
        unmatched += 1
        if len(unmatched_samples) < 12:
            unmatched_samples.append(f"{form} / {reading} (drop={drop} > mora={mora})")
        continue

    e['pitch_accent'] = {'mora': mora, 'drop': drop}
    e['pitch_accent_provenance'] = 'kanjium_lookup'
    assigned += 1

vocab_path.write_text(
    json.dumps(vdata, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

total = len(entries)
final_with_pitch = preserved + assigned
print()
print(f'Total vocab entries:               {total}')
print(f'Already had pitch_accent:          {preserved}')
print(f'Newly assigned via Kanjium:        {assigned}')
print(f'  via (form,reading) match:        {form_match}')
print(f'  via reading-only fallback:       {reading_match}')
print(f'Still unmatched:                   {unmatched}')
print(f'\nFinal coverage: {final_with_pitch}/{total} ({100*final_with_pitch/total:.0f}%)')
print(f'\nUnmatched samples:')
for s in unmatched_samples:
    print(f'  {s}')
