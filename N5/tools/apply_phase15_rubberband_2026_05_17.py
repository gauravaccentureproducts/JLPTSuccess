"""Apply Phase-1.5 — replace ffmpeg-atempo with rubberband on the 3
listening items that needed chained atempo (factor < 0.5).

What this script DOES (one-shot, idempotent on metadata update):
  1. For each of n5.listen.041 / 044 / 045 (the items with
     audio_render_meta.post_render_tempo_change_2026_05_17 < 0.5):
     - Updates `audio_render_meta.post_render_tempo_method` from
       'ffmpeg-atempo' to 'ffmpeg-rubberband' (Phase-1.5).
     - Adds `audio_render_meta.phase15_method_change_2026_05_17`
       = {"from": "ffmpeg-atempo (chained 0.5 + factor/0.5)",
          "to": "ffmpeg-rubberband (single-pass)",
          "rationale": "higher-quality time-stretching for
                        sub-0.5 slowdown factors"}.

What this script ASSUMES:
  - The audio MP3 files have already been replaced with rubberband
    output (done outside this script, ahead of running it).
  - `tools/refresh_listening_pacing_2026_05_17.py` has already
    re-measured pacing (so listening.json `pacing_morae_per_min`
    reflects the new audio).

Run from N5/:
    python tools/apply_phase15_rubberband_2026_05_17.py
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
LISTENING_JSON = ROOT / "data" / "listening.json"

# IDs whose audio_render_meta needs the method swap.
TARGET_IDS = {"n5.listen.041", "n5.listen.044", "n5.listen.045"}


def main() -> int:
    data = json.loads(LISTENING_JSON.read_text(encoding="utf-8"))
    items = data.get("items", [])
    n_updated = 0
    for it in items:
        if it.get("id") not in TARGET_IDS:
            continue
        arm = it.get("audio_render_meta")
        if not isinstance(arm, dict):
            continue
        prior_method = arm.get("post_render_tempo_method")
        if prior_method != "ffmpeg-atempo":
            print(f"  {it['id']}: skip (current method "
                  f"{prior_method!r}; expected 'ffmpeg-atempo')")
            continue
        factor = arm.get("post_render_tempo_change_2026_05_17")
        arm["post_render_tempo_method"] = "ffmpeg-rubberband"
        arm["phase15_method_change_2026_05_17"] = {
            "from": "ffmpeg-atempo (chained 0.5 + factor/0.5)",
            "to": "ffmpeg-rubberband (single-pass)",
            "factor": factor,
            "rationale": (
                "Replaces 2-pass atempo chain (Phase-1, commit 47d1edc) "
                "with single-pass librubberband for sub-0.5 slowdown "
                "factors. Higher-quality PSOLA/phase-vocoder time-"
                "stretching preserves transients better at extreme "
                "factors. Audio length preserved within ~1% of "
                "Phase-1 output; pacing re-measured post-replacement."
            ),
        }
        n_updated += 1
        print(f"  {it['id']}: method ffmpeg-atempo → ffmpeg-rubberband "
              f"(factor {factor})")
    LISTENING_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nUpdated {n_updated} items in {LISTENING_JSON.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
