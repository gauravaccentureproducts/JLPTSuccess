"""ISSUE-062 + ISSUE-089 audio render: multi-voice listening MP3s.

Reads listening.json — for each item that has voice_planned populated
(by tools/fix_issue_062_voice_variety_2026_05_07.py), renders the
script_ja using the assigned voice(s) and writes audio/listening/<id>.mp3.

For mondai-1 / mondai-2 dialogues (multi-line scripts), each line is
rendered with the appropriate speaker based on the line's role marker
(男:/女:/narrator) and concatenated with brief inter-line pauses.

For mondai-3 / mondai-4 single-speaker items, the entire script is
rendered with the single primary voice.

Provider: edge-tts (Microsoft Neural TTS, free, runs from Python via
WebSocket to speech.platform.bing.com — no API key required, 7+
Japanese voices available). Build-time only; no runtime network needed.

Optional fallback: VOICEVOX engine on localhost:50021 (if running).

Run:
  pip install edge-tts pydub
  python tools/build_listening_audio_multivoice_2026_05_07.py [--dry-run] [--limit N]

Requires network egress to speech.platform.bing.com (Microsoft TTS
endpoint). If running in a sandboxed environment, run on host instead.

Output:
  audio/listening/<item-id>.mp3
  data/audio_manifest_voice.json (per-item voice metadata)

Idempotent: re-running on already-rendered items skips them unless
--force-rerender. Only re-renders if voice_planned has changed since
last render (hash-tracked in audio_manifest_voice.json).
"""
from __future__ import annotations
import argparse
import asyncio
import hashlib
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / 'data' / 'listening.json'
OUT_DIR = ROOT / 'audio' / 'listening'
MANIFEST = ROOT / 'data' / 'audio_manifest_voice.json'


def voice_plan_hash(vp: dict, script: str) -> str:
    """Stable hash of voice plan + script — used to detect changes."""
    payload = json.dumps(
        {'voice_planned': vp, 'script_ja': script},
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]


def detect_speaker(line_text: str) -> str:
    """Detect speaker role from a line's prefix (男:/女:/narrator)."""
    s = line_text.strip()
    if s.startswith('男'):
        return '男'
    if s.startswith('女'):
        return '女'
    if s.startswith('A'):
        return '男'
    if s.startswith('B'):
        return '女'
    if s.startswith('店員'):
        return '女'  # default for shop-clerk role
    if s.startswith('先生'):
        return '男'  # default for teacher role
    if s.startswith('学生'):
        return '女'
    if s.startswith('母'):
        return '女'
    if s.startswith('父'):
        return '男'
    if s.startswith('子'):
        return '女'
    return 'narrator'


def strip_speaker_prefix(line_text: str) -> str:
    """Strip the speaker prefix from line text for clean TTS rendering."""
    s = line_text.strip()
    for prefix in ('男:', '男：', '女:', '女：', 'A:', 'A：', 'B:', 'B：',
                   '店員:', '店員：', '先生:', '先生：', '学生:', '学生：',
                   '母:', '母：', '父:', '父：', '子:', '子：'):
        if s.startswith(prefix):
            return s[len(prefix):].strip()
    return s


async def render_segment_edge_tts(text: str, voice: str, out_path: Path):
    """Render one text segment with edge-tts to a single MP3."""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(out_path))


async def render_segment_voicevox(text: str, speaker_id: int, out_path: Path):
    """Fallback: render one segment via local VOICEVOX HTTP at :50021.

    Auto-detects whether VOICEVOX is reachable. Maps the 4 edge-tts
    voices to VOICEVOX speaker IDs:
      ja-JP-NanamiNeural   -> speaker 8  (春日部つむぎ female)
      ja-JP-KeitaNeural    -> speaker 11 (玄野武宏 male)
      ja-JP-AoiNeural      -> speaker 0  (四国めたん female-younger)
      ja-JP-DaichiNeural   -> speaker 13 (青山龍星 male-mature)
    """
    import urllib.request
    import urllib.parse
    # 1. audio_query
    qurl = f'http://localhost:50021/audio_query?speaker={speaker_id}&text={urllib.parse.quote(text)}'
    qreq = urllib.request.Request(qurl, method='POST')
    with urllib.request.urlopen(qreq, timeout=15) as r:
        query = r.read()
    # 2. synthesis
    surl = f'http://localhost:50021/synthesis?speaker={speaker_id}'
    sreq = urllib.request.Request(
        surl, data=query, method='POST',
        headers={'Content-Type': 'application/json', 'Accept': 'audio/wav'},
    )
    with urllib.request.urlopen(sreq, timeout=60) as r:
        wav_data = r.read()
    # Write WAV; pydub will transcode to MP3
    wav_path = out_path.with_suffix('.wav')
    wav_path.write_bytes(wav_data)
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_wav(str(wav_path))
        audio.export(str(out_path), format='mp3')
    finally:
        if wav_path.exists():
            wav_path.unlink()


VOICEVOX_SPEAKER_MAP = {
    'ja-JP-NanamiNeural': 8,
    'ja-JP-KeitaNeural': 11,
    'ja-JP-AoiNeural': 0,
    'ja-JP-DaichiNeural': 13,
}


def detect_provider() -> str:
    """Auto-detect which TTS provider is reachable.
    Returns 'voicevox', 'edge-tts', or 'none'."""
    import socket
    # Try VOICEVOX first (fully local, no privacy concern)
    try:
        with socket.create_connection(('localhost', 50021), timeout=2):
            return 'voicevox'
    except OSError:
        pass
    # Try edge-tts (build-time network call)
    try:
        with socket.create_connection(('speech.platform.bing.com', 443), timeout=5):
            return 'edge-tts'
    except OSError:
        pass
    return 'none'


async def render_segment(text: str, voice_name: str, out_path: Path, provider: str):
    """Dispatch to the auto-detected provider."""
    if provider == 'voicevox':
        speaker_id = VOICEVOX_SPEAKER_MAP.get(voice_name, 8)
        await render_segment_voicevox(text, speaker_id, out_path)
    elif provider == 'edge-tts':
        await render_segment_edge_tts(text, voice_name, out_path)
    else:
        raise RuntimeError(
            f'No TTS provider reachable. Either:\n'
            f'  1. Install VOICEVOX engine and start it on :50021, OR\n'
            f'  2. Run from a machine with network egress to '
            f'speech.platform.bing.com:443 (edge-tts)'
        )


async def render_item(item: dict, args, manifest: dict, provider: str) -> tuple[str, str]:
    """Render one listening item. Returns (id, status)."""
    iid = item['id']
    vp = item.get('voice_planned')
    if not vp:
        return iid, 'skipped (no voice_planned)'

    script = item.get('script_ja') or ''
    if not script:
        return iid, 'skipped (no script_ja)'

    # Hash check for idempotency
    h = voice_plan_hash(vp, script)
    if not args.force_rerender and manifest.get(iid, {}).get('hash') == h:
        out_path = OUT_DIR / f'{iid}.mp3'
        if out_path.exists():
            return iid, 'skipped (up-to-date)'

    if args.dry_run:
        return iid, f'would render via {provider} with primary={vp.get("primary")}, secondary={vp.get("secondary")}'

    # Render. For multi-line scripts (dialogue), render each line then
    # concatenate via pydub. For single-line, render directly.
    out_path = OUT_DIR / f'{iid}.mp3'
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = item.get('lines') or []
    primary = vp.get('primary')
    secondary = vp.get('secondary') or primary
    role_map = vp.get('speaker_role_map') or {}

    if not lines or len(lines) <= 1:
        # Single-segment render
        await render_segment(script.strip(), primary, out_path, provider)
    else:
        # Multi-line render — each line as a separate segment, then concat
        try:
            from pydub import AudioSegment
        except ImportError:
            print('  pydub not installed — falling back to single-voice render')
            await render_segment(script.strip(), primary, out_path, provider)
            return iid, f'rendered (single voice fallback): {primary}'

        seg_paths = []
        try:
            for i, line in enumerate(lines):
                text = strip_speaker_prefix(line.get('text_ja', ''))
                if not text:
                    continue
                speaker = detect_speaker(line.get('text_ja', ''))
                voice = role_map.get(speaker, primary if speaker == 'narrator' else secondary)
                seg_path = OUT_DIR / f'.{iid}.seg{i}.mp3'
                await render_segment(text, voice, seg_path, provider)
                seg_paths.append(seg_path)

            # Concatenate with 500ms silence between
            silence = AudioSegment.silent(duration=500)
            combined = AudioSegment.empty()
            for sp in seg_paths:
                combined += AudioSegment.from_mp3(str(sp))
                combined += silence
            combined.export(str(out_path), format='mp3')
        finally:
            for sp in seg_paths:
                if sp.exists():
                    sp.unlink()

    # Update manifest
    manifest[iid] = {
        'hash': h,
        'voice_planned': vp,
        'rendered_at': '2026-05-07',
    }
    return iid, f'rendered: {primary}{" + " + secondary if secondary != primary else ""}'


async def main_async(args):
    listening = json.loads(LISTENING.read_text(encoding='utf-8'))
    items = listening['items']

    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    else:
        manifest = {}

    todo = [it for it in items if it.get('voice_planned')]
    if args.limit:
        todo = todo[:args.limit]

    # Auto-detect provider once. In --dry-run mode, prefer reporting the
    # detected provider but tolerate 'none' (no actual rendering happens).
    provider = detect_provider()
    print(f'TTS provider detected: {provider}')
    if provider == 'none' and not args.dry_run:
        raise RuntimeError(
            'No TTS provider reachable. Either:\n'
            '  1. Install VOICEVOX engine and start it on :50021 (recommended,\n'
            '     fully local, no privacy concern), OR\n'
            '  2. Run from a machine with network egress to '
            'speech.platform.bing.com:443 (edge-tts).\n'
            'Re-run with --dry-run to preview the plan without rendering.'
        )

    print(f'Items to process: {len(todo)} / {len(items)}')
    if args.dry_run:
        print('--dry-run: no files will be written')

    rendered = 0
    for it in todo:
        iid, status = await render_item(it, args, manifest, provider)
        print(f'  {iid}: {status}')
        if 'rendered' in status:
            rendered += 1

    if not args.dry_run:
        MANIFEST.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        print(f'\nManifest written: {MANIFEST}')

    print(f'\nRendered: {rendered}, Skipped: {len(todo) - rendered}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Show plan without writing')
    parser.add_argument('--force-rerender', action='store_true', help='Re-render even if up-to-date')
    parser.add_argument('--limit', type=int, default=None, help='Process only first N items')
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == '__main__':
    main()
