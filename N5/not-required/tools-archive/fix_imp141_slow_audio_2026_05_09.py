"""IMP-141: render a 0.7x slow-version variant for every listening
MP3 in audio/listening/, and add `audio_slow` reference on each
data/listening.json item.

ffmpeg's `atempo=0.7` audio filter slows playback to 70% speed
without pitch shift (it uses Phase-Vocoder + WSOLA), which is the
correct beginner-aid behavior. The renders preserve VOICEVOX voice
character, just at lower tempo.

Files written:
  audio/listening/<id>.slow.mp3   (47 new files)

JSON updates:
  items[i].audio_slow = "audio/listening/<id>.slow.mp3"
  items[i].audio_render_meta.slow_render_filter = "atempo=0.7"
  items[i].audio_render_meta.slow_render_date  = "2026-05-09"

Idempotent: re-running rewrites the slow MP3s; JSON updates are
no-op if already present.

CC-BY / VOICEVOX licence: the slow variant is a derivative of the
existing per-item VOICEVOX render. Same speaker credit applies
(already captured in NOTICES.md and in
audio_render_meta.voices_used). No new attribution required.
"""
from __future__ import annotations
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUDIO_DIR = ROOT / 'audio' / 'listening'
LISTEN_JSON = ROOT / 'data' / 'listening.json'
SLOW_FACTOR = 0.7

data = json.loads(LISTEN_JSON.read_text(encoding='utf-8'))
items = data['items']

rendered = 0
already = 0
missing_src = []
ffmpeg_failures = []

for it in items:
    src_rel = it.get('audio') or ''
    if not src_rel:
        continue
    src = ROOT / src_rel
    if not src.exists():
        missing_src.append(src_rel)
        continue

    slow_rel = src_rel.replace('.mp3', '.slow.mp3')
    slow = ROOT / slow_rel

    cmd = [
        'ffmpeg',
        '-y',                  # overwrite
        '-loglevel', 'error',
        '-i', str(src),
        '-af', f'atempo={SLOW_FACTOR}',
        '-codec:a', 'libmp3lame',
        '-q:a', '2',           # ~190 kbps VBR — same band as VOICEVOX renders
        str(slow),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
    except subprocess.CalledProcessError as e:
        ffmpeg_failures.append((it.get('id'), e.stderr.decode('utf-8', errors='replace')[:200]))
        continue
    except subprocess.TimeoutExpired:
        ffmpeg_failures.append((it.get('id'), 'TIMEOUT'))
        continue

    if it.get('audio_slow') == slow_rel:
        already += 1
    else:
        rendered += 1
    it['audio_slow'] = slow_rel
    meta = it.setdefault('audio_render_meta', {})
    meta['slow_render_filter'] = f'atempo={SLOW_FACTOR}'
    meta['slow_render_date'] = '2026-05-09'

LISTEN_JSON.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Items processed:        {len(items)}')
print(f'Newly rendered:         {rendered}')
print(f'Already had reference:  {already}')
print(f'Missing source MP3:     {len(missing_src)}')
print(f'ffmpeg failures:        {len(ffmpeg_failures)}')
if missing_src:
    print('  Missing sources:')
    for s in missing_src:
        print(f'    {s}')
if ffmpeg_failures:
    print('  ffmpeg failures:')
    for fid, msg in ffmpeg_failures:
        print(f'    {fid}: {msg}')
