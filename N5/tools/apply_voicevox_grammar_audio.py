"""Post-render: wire the now-existing VOICEVOX audio files into the
data layer and refresh manifests.

Runs AFTER `tools/build_audio_voicevox.py --target grammar` completes.

Three side-effects:

  1. data/grammar.json — populate every patterns[].examples[].audio
     with the relative path `audio/grammar/<id>.<i>.mp3` (the file
     that VOICEVOX just rendered). The renderer in
     js/learn-grammar.js reads this field at runtime; when null the
     <audio> element is suppressed.

  2. data/audio_manifest.json — bump backend metadata to reflect the
     VOICEVOX render. Preserves the existing `items` list (legacy
     gtts metadata) and adds a `grammar` block describing the new
     state.

  3. Reports counts only — CONTENT-LICENSE.md attribution is done
     separately by hand (each VOICEVOX character has a specific
     name + UUID that needs proper attribution).

Idempotent: re-running produces no diff once applied.
"""
from __future__ import annotations

import io
import json
import sys
import os
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
GRAMMAR = REPO / "data" / "grammar.json"
MANIFEST = REPO / "data" / "audio_manifest.json"
AUDIO_DIR = REPO / "audio" / "grammar"


def main() -> int:
    if not GRAMMAR.exists():
        print(f"ERROR: {GRAMMAR} not found")
        return 1
    if not AUDIO_DIR.exists():
        print(f"ERROR: {AUDIO_DIR} not found")
        return 1

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    wired = 0
    missing = 0
    already = 0
    for p in grammar.get("patterns", []):
        pid = p.get("id")
        for i, ex in enumerate(p.get("examples") or []):
            if not isinstance(ex, dict):
                continue
            expected = f"audio/grammar/{pid}.{i}.mp3"
            disk_path = REPO / expected
            if not disk_path.exists():
                missing += 1
                continue
            current = ex.get("audio")
            if current == expected:
                already += 1
                continue
            ex["audio"] = expected
            wired += 1

    print(f"Wired {wired} audio fields (newly populated)")
    print(f"Already correct: {already}")
    print(f"Missing on disk: {missing}")

    GRAMMAR.write_text(
        json.dumps(grammar, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {GRAMMAR}")

    # Update audio_manifest.json — preserve existing items list,
    # update backend + add per-target metadata
    manifest = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    # Update backend signal
    manifest["backend"] = "voicevox"
    manifest["voice_default"] = "voicevox-speaker-8-tsumugi"
    manifest["voicevox_engine_version"] = "0.25.2"
    manifest["voicevox_render_date"] = "2026-05-12"
    manifest["voicevox_character_attribution"] = {
        "speaker_id": 8,
        "character": "Kasukabe Tsumugi (春日部つむぎ)",
        "style": "Normal (ノーマル)",
        "speaker_uuid": "35b2c544-660e-401e-b503-0e14c635303a",
        "license": "VOICEVOX:春日部つむぎ — usable for commercial + non-commercial work with attribution per https://voicevox.hiroshiba.jp/",
    }

    # Add grammar render summary
    manifest_grammar = manifest.setdefault("grammar_voicevox", {})
    rendered_count = 0
    for p in grammar.get("patterns", []):
        pid = p.get("id")
        for i, ex in enumerate(p.get("examples") or []):
            disk = REPO / f"audio/grammar/{pid}.{i}.mp3"
            if disk.exists():
                manifest_grammar[f"{pid}.{i}"] = {
                    "path": f"audio/grammar/{pid}.{i}.mp3",
                    "voice": "voicevox-speaker-8-tsumugi",
                    "size_bytes": disk.stat().st_size,
                }
                rendered_count += 1

    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nUpdated {MANIFEST}: backend=voicevox; {rendered_count} grammar items tracked")

    return 0 if missing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
