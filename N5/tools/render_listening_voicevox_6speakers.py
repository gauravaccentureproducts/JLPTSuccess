"""ISSUE-114 — re-render the 50 listening items via VOICEVOX with 6+
distinct speakers across age bands.

Pipeline:
  1. Read data/listening.json items.
  2. Assign each item a (F-speaker, M-speaker, narrator-speaker) tuple
     cycling through 6 VOICEVOX speakers to achieve age-band variety
     across the 50-item corpus.
  3. For each item, parse script_ja into role-tagged segments
     (男:/女:/narrator), render each segment via VOICEVOX, concatenate
     to a single MP3 with inter-segment silence.
  4. Generate slow version (atempo=0.7).
  5. Update item.audio_render_meta with the new voice metadata
     (voices_used, voice_provider=voicevox, engine version, etc.).

Speaker plan (6 VOICEVOX speakers across age bands):
  speaker  8  →  春日部つむぎ ノーマル (Tsumugi)        adult F
  speaker 11  →  玄野武宏 ノーマル     (Kurono)         adult M
  speaker  2  →  四国めたん ノーマル   (Metan)          young F
  speaker  3  →  ずんだもん ノーマル   (Zundamon)       young M
  speaker 10  →  雨晴はう ノーマル     (Hau)            adolescent F
  speaker 13  →  青山龍星 ノーマル     (Aoyama)         mature-young M

Cycle assignment across 50 items pairs:
  items  1- 9: (Tsumugi, Kurono)      [adult F + adult M]
  items 10-17: (Metan,   Zundamon)    [young F + young M]
  items 18-25: (Tsumugi, Aoyama)      [adult F + mature M]
  items 26-33: (Hau,     Kurono)      [adolescent F + adult M]
  items 34-42: (Metan,   Kurono)      [young F + adult M variant]
  items 43-50: (Tsumugi, Zundamon)    [adult F + young M]

Narrator (the framing 「男の人と女の人が話しています」 segment) uses
the F-speaker of the item.

Engine: VOICEVOX v0.25.2 (CPU) on localhost:50021.
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
import time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
LISTENING_JSON = REPO / "data" / "listening.json"
OUT_DIR = REPO / "audio" / "listening"
ENDPOINT = "http://localhost:50021"

SPEAKERS = {
    "Tsumugi":   {"id":  8, "character": "春日部つむぎ", "style": "ノーマル", "age_band": "adult", "gender": "F"},
    "Kurono":    {"id": 11, "character": "玄野武宏",   "style": "ノーマル", "age_band": "adult", "gender": "M"},
    "Metan":     {"id":  2, "character": "四国めたん", "style": "ノーマル", "age_band": "young", "gender": "F"},
    "Zundamon":  {"id":  3, "character": "ずんだもん", "style": "ノーマル", "age_band": "young", "gender": "M"},
    "Hau":       {"id": 10, "character": "雨晴はう",   "style": "ノーマル", "age_band": "adolescent", "gender": "F"},
    "Aoyama":    {"id": 13, "character": "青山龍星",   "style": "ノーマル", "age_band": "mature", "gender": "M"},
}

# Per-item pair assignment (F_speaker, M_speaker) indexed by item 1-based position
def assign_pair(item_idx_1based: int) -> tuple[str, str]:
    """Returns (F_speaker_key, M_speaker_key) for the item position."""
    i = item_idx_1based
    if   i <=  9:  return ("Tsumugi", "Kurono")
    elif i <= 17:  return ("Metan",   "Zundamon")
    elif i <= 25:  return ("Tsumugi", "Aoyama")
    elif i <= 33:  return ("Hau",     "Kurono")
    elif i <= 42:  return ("Metan",   "Kurono")
    else:          return ("Tsumugi", "Zundamon")


def detect_speaker_role(line: str) -> str:
    """Returns 'F' / 'M' / 'narrator' based on the line's prefix."""
    s = line.strip()
    if not s: return "narrator"
    # Female role prefixes
    if s.startswith("女") or s.startswith("F") or s.startswith("B") or \
       s.startswith("店員") or s.startswith("学生") or s.startswith("母") or s.startswith("子"):
        return "F"
    # Male role prefixes
    if s.startswith("男") or s.startswith("M") or s.startswith("A") or \
       s.startswith("先生") or s.startswith("父"):
        return "M"
    return "narrator"


def strip_role_prefix(line: str) -> str:
    """Strip the role-marker prefix from a script line."""
    s = line.strip()
    for prefix in ("男:", "男:", "男：", "女:", "女:", "女：", "A:", "A：", "B:", "B：",
                   "店員:", "店員：", "先生:", "先生：", "学生:", "学生：",
                   "母:", "母：", "父:", "父：", "子:", "子："):
        if s.startswith(prefix):
            return s[len(prefix):].strip()
    return s


def clean_for_tts(text: str) -> str:
    """Strip learner-spacing before sending to VOICEVOX."""
    if not text: return ""
    return text.replace(" ", "").replace("　", "").replace("\t", "").replace("\n", "")


def synth_segment(text: str, speaker_id: int) -> bytes:
    """Render one segment via VOICEVOX; returns WAV bytes."""
    # audio_query
    qurl = f"{ENDPOINT}/audio_query?speaker={speaker_id}&text={urllib.parse.quote(text)}"
    qreq = urllib.request.Request(qurl, method="POST")
    with urllib.request.urlopen(qreq, timeout=30) as r:
        query = json.loads(r.read())
    # Tune for natural Japanese pacing (per the existing edge-tts script's iter-2 tuning)
    query["speedScale"] = 0.95            # natural N5 listening pace
    query["prePhonemeLength"] = 0.0
    query["postPhonemeLength"] = 0.0
    query["pauseLengthScale"] = 0.9       # keep audible inter-sentence breath
    # synthesis
    surl = f"{ENDPOINT}/synthesis?speaker={speaker_id}"
    sreq = urllib.request.Request(
        surl, data=json.dumps(query).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", "Accept": "audio/wav"},
    )
    with urllib.request.urlopen(sreq, timeout=120) as r:
        return r.read()


def render_item(item: dict, item_idx_1based: int) -> dict:
    """Render one listening item. Returns the updated audio_render_meta."""
    iid = item["id"]
    script = item.get("script_ja") or ""
    if not script:
        return {"error": "no script_ja"}

    f_key, m_key = assign_pair(item_idx_1based)
    f_speaker = SPEAKERS[f_key]
    m_speaker = SPEAKERS[m_key]

    # Parse script into lines and assign speaker per line
    lines = [ln for ln in script.split("\n") if ln.strip()]
    segments = []  # list of (speaker_id, text)
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
            # Narrator → use F speaker (per audit convention)
            segments.append((f_speaker["id"], clean))

    if not segments:
        return {"error": "no segments parsed"}

    # Synth each segment, write to temp WAV, concatenate via ffmpeg
    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        seg_paths = []
        for i, (spk_id, text) in enumerate(segments):
            wav = synth_segment(text, spk_id)
            p = tmpdir / f"seg-{i:03d}.wav"
            p.write_bytes(wav)
            seg_paths.append(p)
        # Build concat list with 350ms silence between segments
        # (better than naive byte-concat for inter-speaker pacing)
        list_file = tmpdir / "concat.txt"
        # Generate a silence WAV for 350ms
        silence_path = tmpdir / "silence.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
             "-t", "0.35", str(silence_path)],
            check=True, capture_output=True,
        )
        # Interleave segments with silence
        lines_out = []
        for i, p in enumerate(seg_paths):
            lines_out.append(f"file '{p.name}'")
            if i < len(seg_paths) - 1:
                lines_out.append(f"file '{silence_path.name}'")
        list_file.write_text("\n".join(lines_out), encoding="utf-8")

        merged_wav = tmpdir / "merged.wav"
        # ffmpeg concat demuxer needs files in cwd or with absolute paths
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "concat", "-safe", "0",
             "-i", str(list_file), "-c", "copy", str(merged_wav)],
            check=True, capture_output=True, cwd=str(tmpdir),
        )

        # Transcode merged WAV → MP3 (normal)
        out_mp3 = OUT_DIR / f"{iid}.mp3"
        out_mp3.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(merged_wav), "-acodec", "libmp3lame", "-ab", "128k",
             str(out_mp3)],
            check=True, capture_output=True,
        )

        # Generate slow version (atempo=0.7)
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
        if spk_id not in seen:
            seen.add(spk_id)
            for key, spk in SPEAKERS.items():
                if spk["id"] == spk_id:
                    voices_used.append(f"voicevox-speaker-{spk_id}-{spk['character']}-{spk['style']}")
                    break

    return {
        "voice_provider": "voicevox",
        "voices_used": voices_used,
        "voicevox_engine_version": "0.25.2",
        "voice_planned_for_engine": {
            "F": {"speaker_id": f_speaker["id"], "character": f_speaker["character"],
                  "style": f_speaker["style"], "age_band": f_speaker["age_band"]},
            "M": {"speaker_id": m_speaker["id"], "character": m_speaker["character"],
                  "style": m_speaker["style"], "age_band": m_speaker["age_band"]},
        },
        "rendered_at": "2026-05-12T18:00:00+00:00",
        "speed_scale": 0.95,
        "engine": "voicevox-cpu",
        "slow_render_filter": "atempo=0.7",
        "slow_render_date": "2026-05-12",
        "segments_count": len(segments),
    }


def main() -> int:
    data = json.loads(LISTENING_JSON.read_text(encoding="utf-8"))
    items = data["items"]

    n_ok = 0
    n_fail = 0
    distinct_speakers = set()
    for idx, item in enumerate(items, start=1):
        try:
            meta = render_item(item, idx)
            if meta.get("error"):
                print(f"  {item['id']}: ERROR {meta['error']}")
                n_fail += 1
                continue
            item["audio_render_meta"] = meta
            for v in meta.get("voices_used", []):
                # Extract speaker_id from voicevox-speaker-N-...
                parts = v.split("-")
                if len(parts) >= 3:
                    try:
                        distinct_speakers.add(int(parts[2]))
                    except ValueError:
                        pass
            n_ok += 1
            print(f"  {item['id']} (item {idx}/50): rendered "
                  f"with speakers {meta['voice_planned_for_engine']['F']['character']} + "
                  f"{meta['voice_planned_for_engine']['M']['character']}")
        except Exception as e:
            print(f"  {item['id']}: EXCEPTION {type(e).__name__}: {e}")
            n_fail += 1

    LISTENING_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n=== Summary ===")
    print(f"Rendered:        {n_ok}/{len(items)}")
    print(f"Failed:          {n_fail}")
    print(f"Distinct speakers used: {len(distinct_speakers)} (audit target: >=6)")
    print(f"Speaker IDs:     {sorted(distinct_speakers)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
