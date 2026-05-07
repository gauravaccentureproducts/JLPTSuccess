"""Tally voice + engine usage across listening.json."""
from __future__ import annotations
import io
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / 'data' / 'listening.json'

d = json.loads(LISTENING.read_text(encoding='utf-8'))
voices = Counter()
engines = Counter()
unique_voices = set()
items_per_voice_count = Counter()

for it in d['items']:
    vp = it.get('voice_planned') or {}
    engines[vp.get('engine', 'none')] += 1
    item_voices = set()
    if vp.get('primary'):
        voices[vp['primary']] += 1
        unique_voices.add(vp['primary'])
        item_voices.add(vp['primary'])
    if vp.get('secondary'):
        voices[vp['secondary']] += 1
        unique_voices.add(vp['secondary'])
        item_voices.add(vp['secondary'])
    for v in (vp.get('speaker_role_map') or {}).values():
        voices[v] += 1
        unique_voices.add(v)
        item_voices.add(v)
    items_per_voice_count[len(item_voices)] += 1

print('Engines:')
for k, v in engines.most_common():
    print(f'  {k!r}: {v}')

print(f'\nUnique voices used across corpus: {len(unique_voices)}')
for k, v in voices.most_common():
    print(f'  {k!r}: {v}')

print('\nItems by voice-count distribution:')
for k, v in sorted(items_per_voice_count.items()):
    print(f'  {k} unique voices: {v} items')

# Cross-check: are these all in our VOICEVOX_SPEAKER_MAP?
KNOWN = {'ja-JP-NanamiNeural', 'ja-JP-KeitaNeural', 'ja-JP-AoiNeural', 'ja-JP-DaichiNeural'}
unknown = unique_voices - KNOWN
if unknown:
    print(f'\nWARNING: voices not in VOICEVOX_SPEAKER_MAP: {unknown}')
else:
    print('\nAll voices map cleanly to VOICEVOX_SPEAKER_MAP entries.')
