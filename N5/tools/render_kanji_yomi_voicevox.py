"""ISSUE-123 — render per-yomi audio for each N5 kanji via VOICEVOX.

Each kanji entry has `on` and `kun` reading arrays (typically 1-3
readings each). This script renders one short MP3 per reading and
wires the paths into a new `audio_yomi` field on each kanji entry:

    {
      "audio_yomi": {
        "on":  [{"reading": "いち", "audio": "audio/kanji/一-on-いち.mp3"}, ...],
        "kun": [{"reading": "ひと", "audio": "audio/kanji/一-kun-ひと.mp3"}, ...]
      }
    }

Engine: VOICEVOX v0.25.2, speaker 8 (春日部つむぎ) — same character as
the grammar audio for consistency.

Single-mora utterances are tricky for TTS engines (most are trained on
longer phrases). To get a clean pronunciation, the input text is
padded slightly: the engine reads the reading with natural pacing
rather than abruptly cut. The resulting MP3s are short (typically
0.4-0.8 seconds).

Output:
  audio/kanji/<glyph>-on-<reading>.mp3       (on-yomi pronunciations)
  audio/kanji/<glyph>-kun-<reading>.mp3      (kun-yomi pronunciations)

Idempotent: re-running skips files that already exist on disk unless
the file size is suspicious (<2 KB suggests a failed render).
"""

from __future__ import annotations

import io
import json
import sys
import urllib.request
import urllib.parse
import tempfile
import subprocess
import os
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
KANJI_JSON = REPO / "data" / "kanji.json"
OUT_DIR = REPO / "audio" / "kanji"
ENDPOINT = "http://localhost:50021"
SPEAKER = 8  # 春日部つむぎ ノーマル


def synth_yomi(reading: str) -> bytes:
    """Render a single kanji reading via VOICEVOX. Returns WAV bytes."""
    # Tiny pre-padding helps short utterances get clean prosody
    # Sanitize: drop suffix markers like ".1" from kun readings (e.g. "あ.う" → "あう")
    clean = reading.replace(".", "").replace("-", "")
    qurl = f"{ENDPOINT}/audio_query?speaker={SPEAKER}&text={urllib.parse.quote(clean)}"
    qreq = urllib.request.Request(qurl, method="POST")
    with urllib.request.urlopen(qreq, timeout=30) as r:
        query = json.loads(r.read())
    query["speedScale"] = 0.95
    query["prePhonemeLength"] = 0.1   # tiny pre-pad helps clarity
    query["postPhonemeLength"] = 0.15
    query["pauseLengthScale"] = 0.7

    surl = f"{ENDPOINT}/synthesis?speaker={SPEAKER}"
    sreq = urllib.request.Request(
        surl, data=json.dumps(query).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
    )
    with urllib.request.urlopen(sreq, timeout=60) as r:
        return r.read()


def render_and_save(glyph: str, kind: str, reading: str) -> str:
    """Render one reading + save as MP3. Returns relative path."""
    # Use the original reading (with .) as filename for clarity
    safe_reading = reading.replace("/", "-").replace("\\", "-")
    rel_path = f"audio/kanji/{glyph}-{kind}-{safe_reading}.mp3"
    out_path = REPO / rel_path
    if out_path.exists() and out_path.stat().st_size > 2000:
        return rel_path  # cached
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wav = synth_yomi(reading)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir=str(OUT_DIR)) as tf:
        tf.write(wav)
        wav_path = tf.name
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", wav_path, "-acodec", "libmp3lame", "-ab", "96k",
             str(out_path)],
            check=True, capture_output=True,
        )
    finally:
        os.unlink(wav_path)
    return rel_path


def main() -> int:
    data = json.loads(KANJI_JSON.read_text(encoding="utf-8"))
    entries = data.get("entries", data)
    if isinstance(entries, dict):
        entries = list(entries.values())

    n_rendered = 0
    n_failed = 0
    for k in entries:
        glyph = k.get("glyph")
        if not glyph:
            continue
        ons = k.get("on") or []
        kuns = k.get("kun") or []

        on_audio = []
        for r in ons:
            try:
                rel = render_and_save(glyph, "on", r)
                on_audio.append({"reading": r, "audio": rel})
                n_rendered += 1
            except Exception as e:
                print(f"  {glyph} on:{r} ERROR {type(e).__name__}: {e}")
                n_failed += 1

        kun_audio = []
        for r in kuns:
            try:
                rel = render_and_save(glyph, "kun", r)
                kun_audio.append({"reading": r, "audio": rel})
                n_rendered += 1
            except Exception as e:
                print(f"  {glyph} kun:{r} ERROR {type(e).__name__}: {e}")
                n_failed += 1

        if on_audio or kun_audio:
            k["audio_yomi"] = {"on": on_audio, "kun": kun_audio}
            k["audio_yomi_provenance"] = "voicevox-speaker-8-tsumugi"

        if (n_rendered % 50) == 0 and n_rendered > 0:
            print(f"  {glyph}: progress {n_rendered} renders")

    KANJI_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    coverage = sum(1 for k in entries if k.get("audio_yomi"))
    print(f"\n=== Summary ===")
    print(f"Renders:   {n_rendered}")
    print(f"Failed:    {n_failed}")
    print(f"Kanji with audio_yomi: {coverage}/{len(entries)}")
    return 0 if n_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
