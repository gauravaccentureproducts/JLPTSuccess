"""Phase-2 follow-on: replace chained ffmpeg-atempo with single-pass
librubberband on the 5 items needing factor < 0.5 slowdown.

After the Phase-2 VOICEVOX re-render at speed_scale=1.00 (commit pending)
plus the post-render pacing refresh (which applied ffmpeg atempo to 34
items to pull them into the JLPT N5 target band 180-240 mpm), 5 items
needed atempo factor < 0.5 — outside the single-pass atempo range and
therefore implemented as `atempo=0.5,atempo=X` chains. This script
replaces the chained-atempo output with a single-pass rubberband
output, same as the Phase-1.5 quality-upgrade pattern from commit
c79c02e.

Procedure per item:
  1. Re-render the item from VOICEVOX at speed_scale=1.00 to a fresh
     temp WAV (the post-Phase-1.5-style "source" we need).
  2. Apply ffmpeg `rubberband=tempo=<factor>` single-pass to the WAV.
  3. Replace the in-corpus n5.listen.NNN.mp3.
  4. Regenerate n5.listen.NNN.slow.mp3 (atempo=0.7 single-pass) from
     the new primary.
  5. Update audio_render_meta.post_render_tempo_method "ffmpeg-atempo"
     -> "ffmpeg-rubberband" + add phase15_method_change_2026_05_17.

Run from N5/ with VOICEVOX engine running at localhost:50021:
    python tools/apply_phase2_rubberband_chained_items_2026_05_17.py

Re-run `tools/refresh_listening_pacing_2026_05_17.py` afterward to
update pacing measurements.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
LISTENING_JSON = REPO / "data" / "listening.json"
OUT_DIR = REPO / "audio" / "listening"
ENDPOINT = "http://localhost:50021"

# Speakers map (mirrors the Phase-2 render script).
SPEAKERS = {
    "Tsumugi":  {"id":  8, "character": "春日部つむぎ", "style": "ノーマル",
                 "age_band": "adult",      "gender": "F"},
    "Kurono":   {"id": 11, "character": "玄野武宏",     "style": "ノーマル",
                 "age_band": "adult",      "gender": "M"},
    "Metan":    {"id":  2, "character": "四国めたん",   "style": "ノーマル",
                 "age_band": "young",      "gender": "F"},
    "Zundamon": {"id":  3, "character": "ずんだもん",   "style": "ノーマル",
                 "age_band": "young",      "gender": "M"},
    "Hau":      {"id": 10, "character": "雨晴はう",     "style": "ノーマル",
                 "age_band": "adolescent", "gender": "F"},
    "Aoyama":   {"id": 13, "character": "青山龍星",     "style": "ノーマル",
                 "age_band": "mature",     "gender": "M"},
}


def assign_pair(item_idx_1based: int) -> tuple[str, str]:
    i = item_idx_1based
    if i <= 9:
        return ("Tsumugi", "Kurono")
    if i <= 17:
        return ("Metan", "Zundamon")
    if i <= 25:
        return ("Tsumugi", "Aoyama")
    if i <= 33:
        return ("Hau", "Kurono")
    if i <= 42:
        return ("Metan", "Kurono")
    return ("Tsumugi", "Zundamon")


def detect_speaker_role(line: str) -> str:
    s = line.strip()
    if not s:
        return "narrator"
    if (s.startswith("女") or s.startswith("F") or s.startswith("B")
            or s.startswith("店員") or s.startswith("学生")
            or s.startswith("母") or s.startswith("子")):
        return "F"
    if (s.startswith("男") or s.startswith("M") or s.startswith("A")
            or s.startswith("先生") or s.startswith("父")):
        return "M"
    return "narrator"


def strip_role_prefix(line: str) -> str:
    s = line.strip()
    for prefix in ("男:", "男:", "男:", "女:", "女:", "女:",
                   "A:", "A:", "B:", "B:",
                   "店員:", "店員:", "先生:", "先生:",
                   "学生:", "学生:", "母:", "母:",
                   "父:", "父:", "子:", "子:"):
        if s.startswith(prefix):
            return s[len(prefix):].strip()
    return s


def clean_for_tts(text: str) -> str:
    if not text:
        return ""
    return (text.replace(" ", "").replace("　", "")
                .replace("\t", "").replace("\n", ""))


def synth_segment(text: str, speaker_id: int) -> bytes:
    qurl = (f"{ENDPOINT}/audio_query?speaker={speaker_id}"
            f"&text={urllib.parse.quote(text)}")
    qreq = urllib.request.Request(qurl, method="POST")
    with urllib.request.urlopen(qreq, timeout=30) as r:
        query = json.loads(r.read())
    query["speedScale"] = 1.00
    query["prePhonemeLength"] = 0.0
    query["postPhonemeLength"] = 0.0
    query["pauseLengthScale"] = 0.9
    surl = f"{ENDPOINT}/synthesis?speaker={speaker_id}"
    sreq = urllib.request.Request(
        surl, data=json.dumps(query).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
    )
    with urllib.request.urlopen(sreq, timeout=120) as r:
        return r.read()


def rerender_then_rubberband(item: dict, item_idx_1based: int,
                             factor: float) -> None:
    """Re-render the item from VOICEVOX, then apply rubberband at factor."""
    iid = item["id"]
    script = item.get("script_ja") or ""
    if not script:
        raise RuntimeError(f"{iid}: no script_ja")

    f_key, m_key = assign_pair(item_idx_1based)
    f_speaker = SPEAKERS[f_key]
    m_speaker = SPEAKERS[m_key]

    lines = [ln for ln in script.split("\n") if ln.strip()]
    segments: list[tuple[int, str]] = []
    for ln in lines:
        role = detect_speaker_role(ln)
        clean = clean_for_tts(strip_role_prefix(ln))
        if not clean:
            continue
        if role == "F":
            segments.append((f_speaker["id"], clean))
        elif role == "M":
            segments.append((m_speaker["id"], clean))
        else:
            segments.append((f_speaker["id"], clean))

    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        seg_paths = []
        for i, (spk_id, text) in enumerate(segments):
            wav = synth_segment(text, spk_id)
            p = tmpdir / f"seg-{i:03d}.wav"
            p.write_bytes(wav)
            seg_paths.append(p)

        # Silence + concat
        silence_path = tmpdir / "silence.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
             "-t", "0.35", str(silence_path)],
            check=True, capture_output=True,
        )
        list_file = tmpdir / "concat.txt"
        lines_out = []
        for i, p in enumerate(seg_paths):
            lines_out.append(f"file '{p.name}'")
            if i < len(seg_paths) - 1:
                lines_out.append(f"file '{silence_path.name}'")
        list_file.write_text("\n".join(lines_out), encoding="utf-8")

        merged_wav = tmpdir / "merged.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "concat", "-safe", "0",
             "-i", str(list_file), "-c", "copy", str(merged_wav)],
            check=True, capture_output=True, cwd=str(tmpdir),
        )

        # Apply rubberband at the target factor
        rb_wav = tmpdir / "rb.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(merged_wav),
             "-filter:a", f"rubberband=tempo={factor:.4f}",
             str(rb_wav)],
            check=True, capture_output=True,
        )

        # Transcode to primary MP3 + .slow.mp3
        out_mp3 = OUT_DIR / f"{iid}.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(rb_wav), "-acodec", "libmp3lame", "-ab", "128k",
             str(out_mp3)],
            check=True, capture_output=True,
        )

        slow_mp3 = OUT_DIR / f"{iid}.slow.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(rb_wav),
             "-filter:a", "atempo=0.7",
             "-acodec", "libmp3lame", "-ab", "128k",
             str(slow_mp3)],
            check=True, capture_output=True,
        )


def main() -> int:
    data = json.loads(LISTENING_JSON.read_text(encoding="utf-8"))
    items = data["items"]
    targets = []
    for idx, it in enumerate(items, start=1):
        arm = it.get("audio_render_meta") or {}
        factor = arm.get("post_render_tempo_change_2026_05_17")
        if factor is None:
            continue
        if float(factor) < 0.5:
            targets.append((idx, it, float(factor)))

    print(f"Phase-2 follow-on targets (chained-atempo, factor<0.5): "
          f"{len(targets)}")
    for idx, it, f in targets:
        print(f"  [{idx}] {it['id']}: factor={f:.4f}")
    print()

    for idx, item, factor in targets:
        iid = item["id"]
        print(f"  Re-rendering {iid} + rubberband(tempo={factor:.4f})...",
              end="", flush=True)
        rerender_then_rubberband(item, idx, factor)
        arm = item.setdefault("audio_render_meta", {})
        arm["post_render_tempo_method"] = "ffmpeg-rubberband"
        arm["phase15_method_change_2026_05_17"] = {
            "from": "ffmpeg-atempo (chained 0.5 + factor/0.5)",
            "to": "ffmpeg-rubberband (single-pass)",
            "factor": factor,
            "phase": "Phase-2 follow-on",
            "rationale": (
                "Replaces 2-pass atempo chain (applied during the "
                "Phase-2 pacing refresh on the speed_scale=1.00 fresh "
                "VOICEVOX render) with single-pass librubberband. "
                "Same quality rationale as Phase-1.5 (commit c79c02e): "
                "rubberband preserves transients better at sub-0.5 "
                "slowdown factors."
            ),
        }
        print(" OK")

    LISTENING_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nUpdated {len(targets)} items in {LISTENING_JSON.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
