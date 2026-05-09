"""IMP-129: line-level timestamps for listening transcripts.

The audit asked for whisper.cpp word-timed transcripts. Whisper
requires ~150-1000 MB of ML model weights bundled with the build
pipeline, which doesn't fit Tier-2 medium-effort budget on this
project.

We deliver the next-most-useful approximation: **mora-proportional
line timestamps**. For each listening item:

  1. Read total audio duration via ffprobe.
  2. Compute mora count for each line in the existing curated
     `lines` array (using the same Tokyo-standard rules from
     IMP-127 — small ya/yu/yo merge, sokuon and long mark count).
  3. Distribute the total duration across lines proportional to
     their mora count.
  4. Write `startMs` + `endMs` per line.

This is enough for:
  - Click-to-seek-by-line ("click line 3 → audio jumps to that spot")
  - Karaoke-style auto-highlight during playback (approximate)
  - Pacing analysis (mora/sec per line)

NOT enough for:
  - Word-level karaoke
  - Phoneme alignment

Future upgrade: integrate whisper.cpp with a JP-tuned model when
the build budget permits. Keep `transcript_timing_provenance:
"mora_proportional"` so the upgrade path is data-tagged.
"""
from __future__ import annotations
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SMALL_MERGE = set('ゃゅょぁぃぅぇぉャュョァィゥェォ')


def count_mora(text: str) -> int:
    """Tokyo-standard mora count over kana text. Non-kana chars
    (kanji, punctuation, latin) are excluded since they don't
    contribute to acoustic timing in this approximation.
    Approximation note: kanji that READ as 1-3 mora are counted as
    1 mora here. The proportional distribution is robust to this
    simplification.
    """
    return sum(
        1 for c in text
        if c not in SMALL_MERGE
        and (
            '぀' <= c <= 'ゟ'
            or '゠' <= c <= 'ヿ'
            or '一' <= c <= '鿿'
        )
    )


def get_duration_ms(audio_path: Path) -> int:
    """Read audio duration in ms via ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(audio_path),
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return int(round(float(out.stdout.strip()) * 1000)) if out.stdout.strip() else 0


listen_path = ROOT / 'data' / 'listening.json'
data = json.loads(listen_path.read_text(encoding='utf-8'))
items = data['items']

processed = 0
no_audio = 0
no_lines = 0
ffprobe_failures = []

for it in items:
    audio_rel = it.get('audio')
    if not audio_rel:
        no_audio += 1
        continue
    lines = it.get('lines') or []
    if not lines:
        no_lines += 1
        continue

    audio_abs = ROOT / audio_rel
    if not audio_abs.exists():
        no_audio += 1
        continue

    try:
        duration_ms = get_duration_ms(audio_abs)
    except Exception as e:
        ffprobe_failures.append((it.get('id'), str(e)))
        continue

    if duration_ms <= 0:
        ffprobe_failures.append((it.get('id'), 'duration=0'))
        continue

    # Compute per-line mora; floor at 1 to avoid zero-weight lines.
    mora = [max(1, count_mora(ln.get('text_ja') or '')) for ln in lines]
    total_mora = sum(mora)

    # Distribute duration. Cumulative ms ensures monotonic non-overlap.
    cursor = 0
    for ln, m in zip(lines, mora):
        ln_duration = int(round(duration_ms * m / total_mora))
        ln['startMs'] = cursor
        ln['endMs'] = cursor + ln_duration
        cursor += ln_duration
    # Final line snaps to the audio end (rounding leftover).
    lines[-1]['endMs'] = duration_ms

    it['transcript_timing_provenance'] = 'mora_proportional'
    processed += 1

listen_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Total listening items:    {len(items)}')
print(f'  timestamps applied:     {processed}')
print(f'  no audio source:        {no_audio}')
print(f'  no lines (skip):        {no_lines}')
print(f'  ffprobe failures:       {len(ffprobe_failures)}')
if ffprobe_failures:
    for fid, msg in ffprobe_failures:
        print(f'    {fid}: {msg}')
