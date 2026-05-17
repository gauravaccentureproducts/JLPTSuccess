"""Audio Phase-2 — VOICEVOX re-render at speed_scale=1.00.

Derived from `render_listening_voicevox_6speakers.py` (which rendered
the corpus at speed_scale=0.95 on 2026-05-12). Phase-2 raises the
speedScale to 1.00 — closer to native conversational pace — and
re-renders every item from source. After this script:

  1. Every audio/listening/n5.listen.NNN.mp3 is regenerated.
  2. Every audio/listening/n5.listen.NNN.slow.mp3 is regenerated
     (atempo=0.7 derived from the new primary).
  3. listening.json item-level audio_render_meta is updated:
     - speed_scale: 0.95 -> 1.00
     - rendered_at: today's date (2026-05-17 phase-2 timestamp)
     - phase2_voicevox_rerender_2026_05_17: True
     - post_render_tempo_change_2026_05_17: removed if present
       (the field captured Phase-1's ffmpeg atempo adjustment;
       Phase-2 re-renders from source so the atempo is gone)
     - post_render_tempo_method: removed if present
     - phase15_method_change_2026_05_17: removed if present
       (the Phase-1.5 rubberband replacement is also superseded
       by the Phase-2 from-source render)
  4. After this script, run `tools/refresh_listening_pacing_2026_05_17.py`
     to re-measure pacing; items outside target band 180-240 mpm
     get atempo or rubberband re-applied (Phase-2 leftover).

Run from N5/ with VOICEVOX engine running at localhost:50021:
    python tools/render_listening_phase2_voicevox_1_00_2026_05_17.py

Estimated wall-clock: ~10-15 min for 50 items × ~5 segments each.
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
LISTENING_JSON = REPO / "data" / "listening.json"
OUT_DIR = REPO / "audio" / "listening"
ENDPOINT = "http://localhost:50021"

SPEED_SCALE = 1.00  # Phase-2 target; was 0.95 in 2026-05-12 render

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
    """Same speaker-pair assignment as the 0.95-render — preserves
    the 6-voice variety distribution authored in the BUG-052 close-out.
    """
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
    query["speedScale"] = SPEED_SCALE
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


def render_item(item: dict, item_idx_1based: int) -> dict:
    iid = item["id"]
    script = item.get("script_ja") or ""
    if not script:
        return {"error": "no script_ja"}

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

    if not segments:
        return {"error": "no segments parsed"}

    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        seg_paths = []
        for i, (spk_id, text) in enumerate(segments):
            wav = synth_segment(text, spk_id)
            p = tmpdir / f"seg-{i:03d}.wav"
            p.write_bytes(wav)
            seg_paths.append(p)

        list_file = tmpdir / "concat.txt"
        silence_path = tmpdir / "silence.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
             "-t", "0.35", str(silence_path)],
            check=True, capture_output=True,
        )
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

        out_mp3 = OUT_DIR / f"{iid}.mp3"
        out_mp3.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(merged_wav), "-acodec", "libmp3lame", "-ab", "128k",
             str(out_mp3)],
            check=True, capture_output=True,
        )

        slow_mp3 = OUT_DIR / f"{iid}.slow.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(merged_wav),
             "-filter:a", "atempo=0.7",
             "-acodec", "libmp3lame", "-ab", "128k",
             str(slow_mp3)],
            check=True, capture_output=True,
        )

    voices_used = []
    seen = set()
    for spk_id, _ in segments:
        if spk_id in seen:
            continue
        seen.add(spk_id)
        for key, spk in SPEAKERS.items():
            if spk["id"] == spk_id:
                voices_used.append(
                    f"voicevox-speaker-{spk_id}-"
                    f"{spk['character']}-{spk['style']}"
                )
                break

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    return {
        "voice_provider": "voicevox",
        "voices_used": voices_used,
        "voicevox_engine_version": "0.25.2",
        "voice_planned_for_engine": {
            "F": {"speaker_id": f_speaker["id"],
                  "character": f_speaker["character"],
                  "style": f_speaker["style"],
                  "age_band": f_speaker["age_band"]},
            "M": {"speaker_id": m_speaker["id"],
                  "character": m_speaker["character"],
                  "style": m_speaker["style"],
                  "age_band": m_speaker["age_band"]},
        },
        "rendered_at": now_iso,
        "speed_scale": SPEED_SCALE,
        "engine": "voicevox-cpu",
        "slow_render_filter": "atempo=0.7",
        "slow_render_date": "2026-05-17",
        "segments_count": len(segments),
        "phase2_voicevox_rerender_2026_05_17": True,
    }


def main() -> int:
    data = json.loads(LISTENING_JSON.read_text(encoding="utf-8"))
    items = data["items"]

    n_ok = 0
    n_fail = 0
    distinct_speakers = set()
    t_start = time.time()
    for idx, item in enumerate(items, start=1):
        iid = item.get("id", f"item-{idx}")
        try:
            t_item = time.time()
            meta = render_item(item, idx)
            if "error" in meta:
                print(f"  [{idx:02d}/{len(items)}] {iid}: ERROR "
                      f"{meta['error']}")
                n_fail += 1
                continue
            # Strip Phase-1 / Phase-1.5 post-processing metadata that is
            # superseded by the Phase-2 from-source render.
            prior_meta = item.get("audio_render_meta") or {}
            for stale_key in ("post_render_tempo_change_2026_05_17",
                              "post_render_tempo_method",
                              "phase15_method_change_2026_05_17"):
                prior_meta.pop(stale_key, None)
            # Merge new meta into prior (preserving any other keys
            # like has_ambient_context_layer, ambient_synth_method,
            # voice_variety_status, etc.)
            prior_meta.update(meta)
            item["audio_render_meta"] = prior_meta
            for v in meta.get("voices_used", []):
                distinct_speakers.add(v)
            elapsed = time.time() - t_item
            n_ok += 1
            print(f"  [{idx:02d}/{len(items)}] {iid}: OK "
                  f"({len(meta['voices_used'])} voices, "
                  f"{meta['segments_count']} segs, {elapsed:.1f}s)")
        except Exception as e:
            print(f"  [{idx:02d}/{len(items)}] {iid}: EXCEPTION {e}")
            n_fail += 1

    # Update _meta-level voicevox stats
    meta_root = data.setdefault("_meta", {})
    meta_root.setdefault("phase2_voicevox_rerender_2026_05_17", {})
    meta_root["phase2_voicevox_rerender_2026_05_17"] = {
        "completed_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S+00:00"
        ),
        "speed_scale": SPEED_SCALE,
        "speed_scale_prior": 0.95,
        "items_rerendered": n_ok,
        "items_failed": n_fail,
        "distinct_voicevox_speakers_used": len(distinct_speakers),
        "engine_version": "0.25.2",
        "note": (
            "From-source VOICEVOX re-render at speed_scale=1.00, "
            "supersedes the 2026-05-12 render at 0.95 + Phase-1 "
            "ffmpeg atempo (commit 47d1edc) + Phase-1.5 librubberband "
            "(commit c79c02e). Item-level audio_render_meta cleared "
            "of post_render_tempo_change_2026_05_17 / "
            "post_render_tempo_method / phase15_method_change_2026_05_17 "
            "since the new primaries no longer carry those adjustments."
        ),
    }

    LISTENING_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    t_total = time.time() - t_start
    print(f"\nDone: {n_ok} OK, {n_fail} FAIL in {t_total:.1f}s.")
    print(f"Distinct voicevox speakers used: {len(distinct_speakers)}")
    print(f"Updated {LISTENING_JSON.name}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
