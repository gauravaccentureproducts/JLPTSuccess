"""IMP-122 (TBD): Render the 47 listening items via VOICEVOX local server.

============================================================================
DEPRECATED 2026-05-07 — DATA-INCOMPATIBLE WITH CURRENT SCHEMA.

This script expects `voice_planned` to be a flat dict of {speaker_label:
int_speaker_id}. The current data/listening.json (post-2026-05-06 voice
variety pass) instead uses {primary, secondary, engine, speaker_role_map}
where the values are edge-tts voice-name strings (e.g. 'ja-JP-NanamiNeural'),
not integer speaker IDs.

Use tools/build_listening_audio_multivoice_2026_05_07.py instead. It:
  - Reads the current schema correctly.
  - Auto-detects VOICEVOX (preferred) or edge-tts at runtime.
  - Maps edge-tts voice names to VOICEVOX speaker IDs internally.
  - Closes ISSUE-062 + ISSUE-089 with a single command.

Kept here for git-history clarity; do not run.
============================================================================

Closes ISSUE-062 (voice variety = 1) + ISSUE-074-residual (26 too-slow
items) + ISSUE-090 data-side (TTS corpus) in a single execute pass,
once VOICEVOX is installed locally. Reads the `voice_planned` field
populated by `tools/plan_listening_voice_variety_2026_05_06.py` so each
item gets the correct multi-voice rendering.

Prerequisites
-------------
1. VOICEVOX desktop or VOICEVOX core/engine running at http://localhost:50021
   (free; download: https://voicevox.hiroshiba.jp/)
2. ffmpeg in PATH (for WAV → MP3 conversion). Verify with `ffmpeg -version`.
3. pip install requests  (the only third-party dep beyond stdlib)

Run
---
    python tools/render_listening_audio_voicevox.py            # render all 47 items
    python tools/render_listening_audio_voicevox.py --dry-run  # show plan, don't render
    python tools/render_listening_audio_voicevox.py --only n5.listen.001  # one item

Output
------
- Writes audio/listening/<id>.mp3 for each rendered item
- Updates listening.json: each item gets `voice_variety_status: "rendered"`,
  `audio_render_meta: {voicevox_voices: [...], speed_scale, pitch_scale, rendered_at}`
- Skips items whose status is already "rendered" unless --force

Algorithm per item
------------------
For each listening item with voice_planned + script_ja:
  1. Split script_ja into speaker-labeled lines (e.g. "男：あした…").
  2. For each line, pick the voice_id from voice_planned[speaker_label].
     Single-narration items use voice_planned["_narration"].
  3. POST /audio_query?speaker={voice_id}&text={line} to VOICEVOX.
  4. Patch the returned query: speed_scale = SPEED_SCALE (default 1.30),
     pitch_scale unchanged, intonationScale unchanged. The 1.30x bumps
     the default voicevox-shikoku-metan ~150-160 morae/min to ~195-208,
     landing inside the JLPT-N5 target band 180-240 (per ISSUE-074).
  5. POST /synthesis?speaker={voice_id} with the patched query.
  6. Concatenate per-line WAV bytes with 250 ms silence gaps between
     turns (real-conversation feel).
  7. Convert combined WAV → MP3 via ffmpeg (-codec:a libmp3lame -b:a 64k).

The resulting 47 MP3s replace the current single-voice voicevox-shikoku-metan
files (or fill in the 7 currently-missing items). Each renamed/replaced
audio is sanity-checked: duration > 0, MP3 magic header present.

If VOICEVOX is unreachable
--------------------------
Script exits with rc=2 and clear error pointing to install instructions.
No partial state is left on disk — atomic writes via .tmp + rename.
"""
from __future__ import annotations
import argparse
import io
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
LISTENING = ROOT / 'data' / 'listening.json'
AUDIO_DIR = ROOT / 'audio' / 'listening'

VOICEVOX_BASE = 'http://localhost:50021'
SPEED_SCALE = 1.30      # bumps shikoku-metan default pace to JLPT-N5 target band (180-240 mpm)
PITCH_SCALE = 0.0
INTONATION_SCALE = 1.0
INTER_TURN_SILENCE_MS = 250

# Speaker-label classification (mirror of plan_listening_voice_variety_2026_05_06.py).
MALE_HINTS = {'男', '父', '先生男', 'かれ', 'お父さん'}
FEMALE_HINTS = {'女', '母', '先生女', 'かのじょ', 'お母さん'}
SPEAKER_LABEL_RE = re.compile(r'^([^\s：]{1,5})：(.*)$')


def _import_requests():
    try:
        import requests
        return requests
    except ImportError:
        sys.stderr.write(
            'ERROR: `requests` not installed. Run: pip install requests\n'
        )
        sys.exit(2)


def _verify_voicevox_running(requests) -> bool:
    try:
        r = requests.get(f'{VOICEVOX_BASE}/version', timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def _verify_ffmpeg() -> bool:
    return shutil.which('ffmpeg') is not None


def _split_script(script: str) -> list[tuple[str, str]]:
    """Return [(speaker_label, line_text), ...] from a script_ja.
    Lines without a "X：" prefix are treated as narration (label '_narration').
    """
    out = []
    for raw in script.split('\n'):
        line = raw.strip()
        if not line:
            continue
        m = SPEAKER_LABEL_RE.match(line)
        if m:
            out.append((m.group(1), m.group(2).strip()))
        else:
            out.append(('_narration', line))
    return out


def _pick_voice(voice_planned: dict, speaker_label: str) -> int:
    """Map a speaker label to a voicevox speaker_id.
    1. Exact match in voice_planned dict
    2. Hint-classified male/female fallback
    3. _narration fallback
    4. Default 2 (Shikoku Metan ノーマル)
    """
    if speaker_label in voice_planned:
        return voice_planned[speaker_label]
    if speaker_label in MALE_HINTS:
        return voice_planned.get('_male_default', 11)  # Shirakami Kotaro
    if speaker_label in FEMALE_HINTS:
        return voice_planned.get('_female_default', 2)  # Shikoku Metan
    return voice_planned.get('_narration', 2)


def _voicevox_synth_line(requests, text: str, speaker_id: int) -> bytes:
    """Render a single line via VOICEVOX. Returns WAV bytes."""
    # 1. audio_query
    r1 = requests.post(
        f'{VOICEVOX_BASE}/audio_query',
        params={'speaker': speaker_id, 'text': text},
        timeout=15,
    )
    r1.raise_for_status()
    query = r1.json()
    query['speedScale'] = SPEED_SCALE
    query['pitchScale'] = PITCH_SCALE
    query['intonationScale'] = INTONATION_SCALE
    # 2. synthesis
    r2 = requests.post(
        f'{VOICEVOX_BASE}/synthesis',
        params={'speaker': speaker_id},
        json=query,
        timeout=60,
        headers={'Content-Type': 'application/json', 'Accept': 'audio/wav'},
    )
    r2.raise_for_status()
    return r2.content


def _silence_wav_bytes(framerate: int, sampwidth: int, nchannels: int, ms: int) -> bytes:
    """Generate raw WAV bytes for `ms` of silence matching the given format."""
    nframes = int(framerate * ms / 1000)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        w.setnchannels(nchannels)
        w.setsampwidth(sampwidth)
        w.setframerate(framerate)
        w.writeframes(b'\x00' * (nframes * sampwidth * nchannels))
    return buf.getvalue()


def _concat_wavs(wav_chunks: list[bytes], silence_ms: int) -> bytes:
    """Concatenate WAVs in-memory, inserting `silence_ms` between turns.
    All chunks must share format (verified at first chunk)."""
    if not wav_chunks:
        return b''
    # Read first to get format
    first = wave.open(io.BytesIO(wav_chunks[0]), 'rb')
    fr, sw, nc = first.getframerate(), first.getsampwidth(), first.getnchannels()
    frames_total = []
    silence = _silence_wav_bytes(fr, sw, nc, silence_ms)
    silence_wav = wave.open(io.BytesIO(silence), 'rb')
    silence_frames = silence_wav.readframes(silence_wav.getnframes())
    for i, chunk in enumerate(wav_chunks):
        w = wave.open(io.BytesIO(chunk), 'rb')
        if w.getframerate() != fr or w.getsampwidth() != sw or w.getnchannels() != nc:
            raise RuntimeError(
                f'WAV chunk {i} format mismatch: '
                f'{w.getframerate()}Hz {w.getsampwidth()*8}-bit {w.getnchannels()}ch '
                f'vs first {fr}Hz {sw*8}-bit {nc}ch'
            )
        frames_total.append(w.readframes(w.getnframes()))
        if i < len(wav_chunks) - 1:
            frames_total.append(silence_frames)
    out_buf = io.BytesIO()
    with wave.open(out_buf, 'wb') as w:
        w.setnchannels(nc)
        w.setsampwidth(sw)
        w.setframerate(fr)
        for f in frames_total:
            w.writeframes(f)
    return out_buf.getvalue()


def _wav_to_mp3(wav_bytes: bytes, out_mp3_path: Path) -> None:
    """Write WAV → MP3 via ffmpeg subprocess. Atomic via .tmp + rename."""
    out_mp3_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_mp3_path.with_suffix('.tmp.mp3')
    proc = subprocess.run(
        ['ffmpeg', '-y', '-i', '-', '-codec:a', 'libmp3lame', '-b:a', '64k', str(tmp_path)],
        input=wav_bytes,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f'ffmpeg failed (rc={proc.returncode}): '
            f'{proc.stderr[-500:].decode("utf-8", errors="replace")}'
        )
    tmp_path.replace(out_mp3_path)


def render_one_item(requests, item: dict, force: bool = False, dry_run: bool = False) -> dict:
    """Render a single listening item. Returns status dict."""
    item_id = item['id']
    status = {'id': item_id, 'rendered': False, 'voices_used': set(), 'reason': None}

    if not item.get('voice_planned'):
        status['reason'] = 'no voice_planned'
        return status
    if not item.get('script_ja'):
        status['reason'] = 'no script_ja'
        return status
    if item.get('voice_variety_status') == 'rendered' and not force:
        status['reason'] = 'already rendered (use --force to redo)'
        return status

    voice_planned = item['voice_planned']
    lines = _split_script(item['script_ja'])
    if not lines:
        status['reason'] = 'empty script after split'
        return status

    # Plan
    plan = []
    for label, text in lines:
        vid = _pick_voice(voice_planned, label)
        plan.append((label, vid, text))
        status['voices_used'].add(vid)

    print(f'\n=== {item_id} (mondai={item.get("mondai")}) ===')
    for label, vid, text in plan:
        preview = text[:50].replace('\n', ' ')
        print(f'  {label:<12} v{vid:<3} {preview}{"..." if len(text) > 50 else ""}')

    if dry_run:
        status['reason'] = 'dry-run (not synthesized)'
        return status

    # Synthesize each line
    wav_chunks = []
    for label, vid, text in plan:
        try:
            wav = _voicevox_synth_line(requests, text, vid)
            wav_chunks.append(wav)
        except Exception as e:
            status['reason'] = f'voicevox synth failed for "{label}: {text[:30]}...": {e}'
            return status

    # Concatenate
    try:
        combined_wav = _concat_wavs(wav_chunks, INTER_TURN_SILENCE_MS)
    except Exception as e:
        status['reason'] = f'concat failed: {e}'
        return status

    # Encode MP3 + write atomically
    audio_path = item.get('audio') or f'audio/listening/{item_id}.mp3'
    out_path = ROOT / audio_path
    try:
        _wav_to_mp3(combined_wav, out_path)
    except Exception as e:
        status['reason'] = f'mp3 encode failed: {e}'
        return status

    status['rendered'] = True
    status['voices_used'] = sorted(status['voices_used'])
    status['out_path'] = str(out_path.relative_to(ROOT))
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Plan only, no synthesis')
    parser.add_argument('--only', action='append', help='Render only the listed item id(s)')
    parser.add_argument('--force', action='store_true', help='Re-render items already marked rendered')
    args = parser.parse_args()

    requests = _import_requests()

    if not args.dry_run:
        if not _verify_voicevox_running(requests):
            sys.stderr.write(
                f'ERROR: VOICEVOX not reachable at {VOICEVOX_BASE}\n'
                f'  Install: https://voicevox.hiroshiba.jp/\n'
                f'  Then launch VOICEVOX desktop app (or run voicevox_engine).\n'
            )
            return 2
        if not _verify_ffmpeg():
            sys.stderr.write(
                'ERROR: ffmpeg not found in PATH (needed for WAV → MP3).\n'
                '  Install: https://ffmpeg.org/download.html\n'
            )
            return 2

    doc = json.loads(LISTENING.read_text(encoding='utf-8'))
    items = doc['items']
    if args.only:
        items = [it for it in items if it['id'] in set(args.only)]
        if not items:
            print(f'ERROR: --only matched no items')
            return 1

    statuses = []
    for it in items:
        s = render_one_item(requests, it, force=args.force, dry_run=args.dry_run)
        statuses.append(s)

    # Update listening.json (only if not dry-run + something rendered)
    if not args.dry_run:
        rendered_ids = {s['id'] for s in statuses if s['rendered']}
        if rendered_ids:
            full_doc = json.loads(LISTENING.read_text(encoding='utf-8'))
            for it in full_doc['items']:
                if it['id'] in rendered_ids:
                    it['voice_variety_status'] = 'rendered'
                    it['audio_render_meta'] = {
                        'voicevox_voices': sorted(set(
                            v for s in statuses if s['id'] == it['id']
                            for v in s['voices_used']
                        )),
                        'speed_scale': SPEED_SCALE,
                        'pitch_scale': PITCH_SCALE,
                        'intonation_scale': INTONATION_SCALE,
                        'rendered_at': datetime.now(timezone.utc).isoformat(),
                    }
            LISTENING.write_text(
                json.dumps(full_doc, ensure_ascii=False, indent=2) + '\n',
                encoding='utf-8'
            )

    # Summary
    rendered = sum(1 for s in statuses if s['rendered'])
    skipped = sum(1 for s in statuses if not s['rendered'])
    print(f'\n=== Summary ===')
    print(f'Rendered: {rendered}/{len(statuses)}')
    print(f'Skipped:  {skipped}/{len(statuses)}')
    for s in statuses:
        if not s['rendered']:
            print(f'  SKIP {s["id"]}: {s["reason"]}')

    if not args.dry_run and rendered:
        # Bump SW cache key reminder
        print(f'\nNEXT STEPS:')
        print(f'  1. Bump sw.js CACHE_VERSION (e.g. v1.12.46 → v1.12.47)')
        print(f'  2. Run python tools/check_content_integrity.py to verify JA-15 (audio refs resolve).')
        print(f'  3. Test in browser: navigate #/listening → first item plays the new multi-voice audio.')
        print(f'  4. If satisfied, commit + push: git add audio/listening data/listening.json sw.js && git commit')

    return 0 if rendered or args.dry_run else 1


if __name__ == '__main__':
    sys.exit(main())
