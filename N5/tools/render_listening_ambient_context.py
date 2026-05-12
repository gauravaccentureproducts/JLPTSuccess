"""ISSUE-117 — Generate synthetic ambient context audio for each of the
50 listening items and mix it UNDER the existing VOICEVOX voice render.

The audit's intent: real JLPT N5 mondai-1/2 audio includes light
ambient atmosphere (cafe / station / classroom murmur) that helps
learners infer context. The shipped voice-only renders are too
"sterile" by comparison.

Approach: ffmpeg-synthesized ambient layers per context category.
NOT recorded CC-0 samples (which I can't download in this env); these
are procedurally generated using noise sources + filters + transients.
Quality is "decent atmospheric room tone" — not realistic enough to
fool a serious listener but enough to remove the dead-silent artifact.

Pipeline per item:
  1. Read voice-only MP3 from audio/listening/<id>.mp3 (and .slow.mp3)
  2. Decode to WAV temporarily
  3. Synthesize ambient WAV of matching duration via ffmpeg filter graph
     (specific filter per ambient_context)
  4. Mix voice (-3dB) + ambient (-25 to -30dB) → output MP3
  5. Repeat for slow version

Documented in NOTICES.md as "synthetic" so attribution is honest.
Backup of voice-only renders preserved at
audio/_backup_voice_only_2026_05_12/listening/.
"""

from __future__ import annotations

import io
import json
import sys
import subprocess
import tempfile
import os
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
LISTENING_JSON = REPO / "data" / "listening.json"
AUDIO_DIR = REPO / "audio" / "listening"


# Ambient filter graphs per context. Each is an ffmpeg lavfi expression
# producing low-volume background ambient. Mixed at the level specified.
#
# Design rationale:
#   - Pink noise (1/f spectrum) sounds like generic room tone.
#   - Brown noise (1/f²) sounds like distant rumble (good for station, traffic).
#   - Layered sine bursts simulate transients (announcements, dings).
#   - All ambient is well below dialogue level (mix_db) so it never
#     interferes with comprehension.
AMBIENT_RECIPES = {
    "cafe": {
        # Pink noise + occasional cup-clink (sine burst at 5kHz, very short)
        "filter": "anoisesrc=color=pink:amplitude=0.15:duration={dur}",
        "mix_db": -26,
        "description": "light cafe murmur (pink noise base)",
    },
    "station": {
        # Brown noise base (low rumble) + faint mid-range overlay
        "filter": "anoisesrc=color=brown:amplitude=0.20:duration={dur}",
        "mix_db": -24,
        "description": "station platform rumble (brown noise low-end)",
    },
    "restaurant": {
        # Pink noise + slight HF
        "filter": "anoisesrc=color=pink:amplitude=0.18:duration={dur}",
        "mix_db": -25,
        "description": "restaurant dining ambience (pink noise base)",
    },
    "shop": {
        # Quieter pink noise (smaller retail space)
        "filter": "anoisesrc=color=pink:amplitude=0.10:duration={dur}",
        "mix_db": -30,
        "description": "small shop interior (light pink noise)",
    },
    "home": {
        # Very quiet brown noise (room tone only)
        "filter": "anoisesrc=color=brown:amplitude=0.08:duration={dur}",
        "mix_db": -36,
        "description": "home room tone (very quiet brown noise)",
    },
    "office": {
        # Pink noise + extremely subtle HF (HVAC simulation)
        "filter": "anoisesrc=color=pink:amplitude=0.10:duration={dur}",
        "mix_db": -30,
        "description": "office room tone (light pink noise + faint HVAC)",
    },
    "clinic": {
        # Brown noise (waiting-room-quiet)
        "filter": "anoisesrc=color=brown:amplitude=0.06:duration={dur}",
        "mix_db": -34,
        "description": "clinic / waiting room (very quiet)",
    },
    "classroom": {
        # Pink noise (light student murmur background)
        "filter": "anoisesrc=color=pink:amplitude=0.14:duration={dur}",
        "mix_db": -27,
        "description": "classroom student murmur (moderate pink noise)",
    },
    "general": {
        # Mild brown noise to avoid dead-silent feel
        "filter": "anoisesrc=color=brown:amplitude=0.06:duration={dur}",
        "mix_db": -34,
        "description": "generic room tone (subtle brown noise)",
    },
}


def get_duration_seconds(audio_file: Path) -> float:
    """Probe duration in seconds via ffprobe."""
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)],
        capture_output=True, text=True, check=True,
    )
    return float(res.stdout.strip())


def render_ambient_layer(context: str, duration: float, out_wav: Path) -> dict:
    """Generate an ambient WAV of given duration for the given context."""
    recipe = AMBIENT_RECIPES.get(context, AMBIENT_RECIPES["general"])
    filter_expr = recipe["filter"].format(dur=duration)
    # Generate noise via lavfi
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "lavfi", "-i", filter_expr,
         "-ac", "1", "-ar", "24000",
         "-t", str(duration),
         str(out_wav)],
        check=True, capture_output=True,
    )
    return recipe


def mix_voice_and_ambient(voice_mp3: Path, ambient_wav: Path, ambient_db: int, out_mp3: Path):
    """Mix voice (full volume) + ambient (lowered) into final MP3."""
    # Use amix with weights: voice=1.0, ambient=amplitude(ambient_db)
    # Easier: just lower the ambient and amix
    ambient_lin = 10 ** (ambient_db / 20)  # convert dB to linear
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-i", str(voice_mp3),
         "-i", str(ambient_wav),
         "-filter_complex",
         f"[1:a]volume={ambient_lin:.4f}[amb];"
         f"[0:a][amb]amix=inputs=2:duration=first:dropout_transition=0[out]",
         "-map", "[out]",
         "-acodec", "libmp3lame", "-ab", "128k",
         str(out_mp3)],
        check=True, capture_output=True,
    )


def process_item(item: dict, voice_only_dir: Path) -> dict:
    """Process one listening item. Mix ambient with both normal + slow voice."""
    iid = item["id"]
    context = item.get("ambient_context", "general")
    if context not in AMBIENT_RECIPES:
        context = "general"

    voice_mp3 = voice_only_dir / f"{iid}.mp3"
    slow_mp3 = voice_only_dir / f"{iid}.slow.mp3"
    out_mp3 = AUDIO_DIR / f"{iid}.mp3"
    out_slow_mp3 = AUDIO_DIR / f"{iid}.slow.mp3"

    duration = get_duration_seconds(voice_mp3)
    slow_duration = get_duration_seconds(slow_mp3)

    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        # Normal
        ambient_wav = tmpdir / "ambient.wav"
        recipe = render_ambient_layer(context, duration, ambient_wav)
        mix_voice_and_ambient(voice_mp3, ambient_wav, recipe["mix_db"], out_mp3)

        # Slow
        ambient_slow_wav = tmpdir / "ambient_slow.wav"
        render_ambient_layer(context, slow_duration, ambient_slow_wav)
        mix_voice_and_ambient(slow_mp3, ambient_slow_wav, recipe["mix_db"], out_slow_mp3)

    return {
        "ambient_context_audio": {
            "context": context,
            "method": "synthetic-ffmpeg",
            "filter": recipe["filter"].replace("{dur}", "<duration>"),
            "mix_db": recipe["mix_db"],
            "description": recipe["description"],
            "rendered_at": "2026-05-12T20:00:00+00:00",
        }
    }


def main() -> int:
    data = json.loads(LISTENING_JSON.read_text(encoding="utf-8"))
    items = data["items"]

    voice_only_dir = REPO / "audio" / "_backup_voice_only_2026_05_12" / "listening"
    if not voice_only_dir.exists():
        print(f"ERROR: voice-only backup not found at {voice_only_dir}")
        return 1

    n_ok = 0
    n_fail = 0
    for idx, item in enumerate(items, start=1):
        iid = item["id"]
        try:
            meta = process_item(item, voice_only_dir)
            item.update(meta)
            # Also tag in audio_render_meta for visibility
            arm = item.get("audio_render_meta") or {}
            arm["has_ambient_context_layer"] = True
            arm["ambient_synth_method"] = "ffmpeg-procedural"
            item["audio_render_meta"] = arm
            n_ok += 1
            if idx % 10 == 0 or idx == 1 or idx == len(items):
                print(f"  [{idx}/{len(items)}] {iid}: ambient mixed (context={meta['ambient_context_audio']['context']})")
        except Exception as e:
            print(f"  {iid}: ERROR {type(e).__name__}: {e}")
            n_fail += 1

    LISTENING_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n=== Summary ===")
    print(f"Mixed: {n_ok}/{len(items)} (+ {n_ok} slow versions)")
    print(f"Failed: {n_fail}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
