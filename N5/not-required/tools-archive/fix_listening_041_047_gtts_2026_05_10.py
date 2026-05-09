"""Render audio for the 7 listening items (041-047) that lack `audio`
source — gTTS fallback (VOICEVOX engine not running locally).

After this:
  1. Sets `audio` field on each item.
  2. Calls gTTS to render each script_ja → MP3.
  3. fix_imp141_slow_audio renders 0.7x slow variants for these 7.
  4. fix_imp129_line_timestamps applies mora-proportional line timing.

Provenance: tagged 'gtts' in audio_render_meta to distinguish from
the VOICEVOX-rendered 040 set."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUDIO_DIR = ROOT / 'audio' / 'listening'
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

import gtts

listen_path = ROOT / 'data' / 'listening.json'
data = json.loads(listen_path.read_text(encoding='utf-8'))
items = data['items']

rendered = 0
failures = []

for it in items:
    if it.get('audio'):
        continue
    script = it.get('script_ja') or ''
    if not script:
        continue
    audio_rel = f"audio/listening/{it['id']}.mp3"
    audio_abs = ROOT / audio_rel

    if not audio_abs.exists():
        try:
            tts = gtts.gTTS(text=script, lang='ja', slow=False)
            tts.save(str(audio_abs))
            iid = it['id']
            print(f'  rendered: {iid} ({len(script)} chars)')
        except Exception as e:
            failures.append((it['id'], str(e)))
            continue

    it['audio'] = audio_rel
    meta = it.setdefault('audio_render_meta', {})
    meta['render_engine'] = 'gtts'
    meta['render_date'] = '2026-05-10'
    meta['voices_used'] = []  # gTTS = single synthetic voice; no per-line speaker ids
    rendered += 1

listen_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print()
print(f'Rendered: {rendered}')
print(f'Failures: {len(failures)}')
for fid, msg in failures:
    print(f'  {fid}: {msg}')
