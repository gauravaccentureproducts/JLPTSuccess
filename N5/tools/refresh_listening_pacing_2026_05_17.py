"""Close BUG-048 + BUG-049 — refresh listening.json pacing measurements
   and speed up too_slow items via ffmpeg atempo where feasible.

User request 2026-05-17: "fix these open items as well".

PROBLEM (BUG-048 + BUG-049):
  - Items 041-050 have pacing_morae_per_min=null (never measured).
  - Items 001-040 have stored mpm values from the 2026-05-06 round-9
    edge-tts pacing audit (tools-archive/fix_issue_074_pacing_audit_
    2026_05_06.py); after the 2026-05-12 VOICEVOX re-render those
    values became stale (different audio durations).
  - 26 items reported too_slow at the old measurement (mean 160 mpm
    vs JLPT N5 target 180-240).

APPROACH:
  Pass 1 — re-measure all 50 items against CURRENT audio files using
           the canonical algorithm (kana=1, small kana=0, ー=1,
           kanji=0; matches the round-9 method).
  Pass 2 — for any item still too_slow after re-measurement, apply
           ffmpeg atempo speedup IN PLACE to pull the item into the
           180-240 target band, provided the required speedup factor
           is ≤ 1.5× (preserves audio quality / intelligibility).
           Items needing > 1.5× speedup are left flagged as too_slow
           with a "fix_method_required" annotation (VOICEVOX re-render
           or script rewrite needed; outside this batch's reach).
  Pass 3 — re-measure post-speedup items and finalize fields.
  Pass 4 — refresh _meta.pacing_audit.summary counts.

CANONICAL count_morae() algorithm (preserved from round-9 baseline):
  - Hiragana 3041-3096: +1 (unless small kana ゃゅょぁぃぅぇぉっゎ)
  - Katakana 30A1-30FA: +1 (unless small kana)
  - ー (long-vowel mark): +1
  - Halfwidth katakana FF66-FF9D: +1
  - Kanji: 0 (approximation; per round-9 method note)

Run: python tools/refresh_listening_pacing_2026_05_17.py [--apply-speedup]
"""
from __future__ import annotations

import argparse
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from mutagen.mp3 import MP3

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / "data" / "listening.json"
AUDIO_DIR = ROOT / "audio" / "listening"

PACING_TARGET_MIN = 180
PACING_TARGET_MAX = 240
PACING_TARGET_MID = (PACING_TARGET_MIN + PACING_TARGET_MAX) / 2  # 210

MAX_FFMPEG_SPEEDUP = 1.50  # quality threshold; above this → defer to re-render
MIN_FFMPEG_TEMPO = 0.50    # ffmpeg atempo single-pass minimum (chained for lower)

SMALL_KANA = set("ゃゅょぁぃぅぇぉっゎャュョァィゥェォッヮ")


def count_morae(text: str) -> int:
    """Canonical mora count (round-9 algorithm, kanji = 0)."""
    morae = 0
    for ch in text or "":
        cp = ord(ch)
        if 0x3041 <= cp <= 0x3096:        # Hiragana
            if ch not in SMALL_KANA:
                morae += 1
        elif 0x30A1 <= cp <= 0x30FA:      # Katakana
            if ch not in SMALL_KANA:
                morae += 1
        elif ch == "ー":                  # Long-vowel mark
            morae += 1
        elif 0xFF66 <= cp <= 0xFF9D:      # Halfwidth katakana
            morae += 1
        # else: kanji / punctuation / English / space → 0
    return morae


def get_audio_duration(audio_filename: str) -> float | None:
    path = AUDIO_DIR / audio_filename
    if not path.exists():
        return None
    try:
        return float(MP3(path).info.length)
    except Exception as e:
        print(f"  WARN: cannot read {audio_filename}: {e}")
        return None


def pacing_status_for(mpm: float | None) -> str:
    if mpm is None or mpm <= 0:
        return "unmeasured"
    if mpm < PACING_TARGET_MIN:
        return "too_slow"
    if mpm > PACING_TARGET_MAX:
        return "too_fast"
    return "in_range"


def build_atempo_chain(factor: float) -> str | None:
    """Build a chained atempo filter string for tempo `factor`.

    atempo single-pass range is [0.5, 2.0]. For factors outside that,
    chain two filters: e.g. factor=0.4 → atempo=0.5,atempo=0.8 (0.5×0.8=0.4).

    Returns None if factor is unsafe (< 0.25 or > 4.0 — would degrade
    audio quality unacceptably even with chaining).
    """
    if factor <= 0 or factor < 0.25 or factor > 4.0:
        return None
    if 0.5 <= factor <= 2.0:
        return f"atempo={factor:.4f}"
    # Chain two atempo filters
    if factor < 0.5:
        # e.g. 0.4 → 0.5 * 0.8
        return f"atempo=0.5,atempo={factor / 0.5:.4f}"
    else:  # factor > 2.0
        return f"atempo=2.0,atempo={factor / 2.0:.4f}"


def apply_ffmpeg_atempo(audio_path: Path, factor: float) -> bool:
    """In-place tempo change via ffmpeg atempo. factor>1 speeds up,
    factor<1 slows down. Returns True on success.

    Refuses extreme factors that would degrade audio quality
    unacceptably (< 0.25× or > 4.0×); refuses speedups that exceed
    MAX_FFMPEG_SPEEDUP (1.5×) per the BUG-049 quality threshold.
    """
    if abs(factor - 1.0) < 0.001:
        return False  # no-op
    if factor > MAX_FFMPEG_SPEEDUP:
        return False  # defer to re-render
    # For slowdowns, allow chained atempo down to 0.25 (factor=0.5 single-
    # pass + factor=0.5 chained = 0.25). Below 0.25 → defer.
    chain = build_atempo_chain(factor)
    if chain is None:
        return False
    tmp = Path(tempfile.gettempdir()) / f"_atempo_{audio_path.name}"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(audio_path),
        "-filter:a", chain,
        "-vn",
        str(tmp),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"  ffmpeg FAIL ({audio_path.name}): {result.stderr.strip()[:200]}")
            return False
        if not tmp.exists() or tmp.stat().st_size < 256:
            print(f"  ffmpeg produced empty/missing output for {audio_path.name}")
            return False
        shutil.copy2(tmp, audio_path)
        tmp.unlink()
        return True
    except subprocess.TimeoutExpired:
        print(f"  ffmpeg TIMEOUT on {audio_path.name}")
        return False
    except FileNotFoundError:
        print("  ERROR: ffmpeg not found on PATH")
        return False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply-speedup", action="store_true",
                   help="Pass 2: apply ffmpeg atempo to too_slow items "
                        "where speedup ≤ 1.5x. Without this flag, only "
                        "re-measurement runs (Pass 1).")
    p.add_argument("--dry-run", action="store_true",
                   help="Report what would change; do not modify files.")
    args = p.parse_args(argv)

    doc = json.loads(LISTENING.read_text(encoding="utf-8"))
    items = doc.get("items", [])
    print(f"Loaded listening.json — {len(items)} items")

    # =================================================================
    # PASS 1 — re-measure all items against current audio
    # =================================================================
    print("\n=== PASS 1: re-measure all items against current audio ===")
    pre_mpm_by_id: dict[str, float | None] = {}
    pre_status_by_id: dict[str, str | None] = {}
    measured = []
    for it in items:
        iid = it["id"]
        script = it.get("script_ja") or ""
        audio = it.get("audio") or ""
        pre_mpm_by_id[iid] = it.get("pacing_morae_per_min")
        pre_status_by_id[iid] = it.get("pacing_status")
        if not script or not audio:
            it["pacing_status"] = "no_audio"
            it["pacing_morae_per_min"] = None
            continue
        audio_filename = Path(audio).name
        dur = get_audio_duration(audio_filename)
        if dur is None or dur <= 0:
            it["pacing_status"] = "no_audio"
            it["pacing_morae_per_min"] = None
            continue
        morae = count_morae(script)
        if morae <= 0:
            # Empty / kanji-only script; can't measure
            it["pacing_status"] = "unmeasured"
            it["pacing_morae_per_min"] = None
            continue
        mpm = round(morae * 60.0 / dur, 1)
        it["pacing_morae_per_min"] = mpm
        it["pacing_status"] = pacing_status_for(mpm)
        measured.append((iid, dur, morae, mpm, it["pacing_status"]))

    # Report Pass 1 diff
    print(f"  Re-measured {len(measured)} items.")
    drifted = [m for m in measured
               if pre_mpm_by_id.get(m[0]) is not None
               and abs((pre_mpm_by_id[m[0]] or 0) - m[3]) > 1.0]
    print(f"  Items with measurement drift vs prior stored value: {len(drifted)}")
    for iid, dur, morae, mpm, status in drifted[:10]:
        pre = pre_mpm_by_id[iid]
        print(f"    {iid}: stored={pre} → measured={mpm} (Δ={mpm - pre:+.1f})")
    if len(drifted) > 10:
        print(f"    ... and {len(drifted) - 10} more")

    # =================================================================
    # PASS 2 — apply ffmpeg atempo speedup to too_slow items
    # =================================================================
    if args.apply_speedup and not args.dry_run:
        print("\n=== PASS 2: ffmpeg atempo tempo-change on out-of-band items ===")
        changed = []
        deferred = []
        for it in items:
            status = it.get("pacing_status")
            if status not in ("too_slow", "too_fast"):
                continue
            iid = it["id"]
            mpm = it.get("pacing_morae_per_min")
            if not mpm or mpm <= 0:
                continue
            # Compute tempo factor to land at target mid-band (210 mpm).
            #   speedup=1.x for too_slow items (mpm < 180 → factor > 1)
            #   slowdown=0.x for too_fast items (mpm > 240 → factor < 1)
            factor = PACING_TARGET_MID / mpm
            if factor > MAX_FFMPEG_SPEEDUP:
                # Speedup beyond quality threshold
                it["pacing_fix_method_required"] = (
                    f"requires re-render (speedup {factor:.2f}x > "
                    f"ffmpeg-safe threshold {MAX_FFMPEG_SPEEDUP}x); "
                    f"current {mpm} mpm vs target {PACING_TARGET_MIN}-"
                    f"{PACING_TARGET_MAX} mpm"
                )
                deferred.append((iid, mpm, factor, "speedup_too_aggressive"))
                continue
            if factor < 0.25:
                # Slowdown beyond quality threshold even chained
                it["pacing_fix_method_required"] = (
                    f"requires re-render (slowdown {factor:.2f}x < "
                    f"safe threshold 0.25x); current {mpm} mpm well "
                    f"above target {PACING_TARGET_MIN}-{PACING_TARGET_MAX}"
                )
                deferred.append((iid, mpm, factor, "slowdown_too_extreme"))
                continue
            audio_filename = Path(it["audio"]).name
            audio_path = AUDIO_DIR / audio_filename
            if not audio_path.exists():
                continue
            direction = "slowdown" if factor < 1.0 else "speedup"
            print(f"  {iid}: {direction} {factor:.3f}x (mpm {mpm} → ~{PACING_TARGET_MID})")
            if apply_ffmpeg_atempo(audio_path, factor):
                changed.append((iid, mpm, factor))
                # Also apply matching tempo change to the slow variant (preserves 0.7× character)
                slow_audio_filename = audio_filename.replace(".mp3", ".slow.mp3")
                slow_path = AUDIO_DIR / slow_audio_filename
                if slow_path.exists():
                    apply_ffmpeg_atempo(slow_path, factor)
                # Record the tempo change applied
                arm = it.setdefault("audio_render_meta", {})
                arm["post_render_tempo_change_2026_05_17"] = round(factor, 4)
                arm["post_render_tempo_method"] = "ffmpeg-atempo"
            else:
                deferred.append((iid, mpm, factor, "ffmpeg_failed"))

        print(f"  Applied tempo change on {len(changed)} items.")
        print(f"  Deferred {len(deferred)} items.")
        for iid, mpm, factor, reason in deferred:
            print(f"    DEFERRED {iid}: mpm={mpm}, factor={factor:.3f}x, reason={reason}")

        # =================================================================
        # PASS 3 — re-measure post-tempo-change items
        # =================================================================
        print("\n=== PASS 3: re-measure post-tempo-change ===")
        for iid, _, _ in changed:
            it = next((x for x in items if x["id"] == iid), None)
            if not it:
                continue
            audio_filename = Path(it["audio"]).name
            dur = get_audio_duration(audio_filename)
            if dur is None or dur <= 0:
                continue
            morae = count_morae(it.get("script_ja") or "")
            mpm = round(morae * 60.0 / dur, 1)
            it["pacing_morae_per_min"] = mpm
            it["pacing_status"] = pacing_status_for(mpm)
        print(f"  Re-measured {len(changed)} post-tempo-change items.")

    # =================================================================
    # PASS 4 — refresh _meta.pacing_audit.summary
    # =================================================================
    print("\n=== PASS 4: refresh _meta.pacing_audit.summary ===")
    counts = {"in_range": 0, "too_slow": 0, "too_fast": 0,
              "no_audio": 0, "unmeasured": 0}
    paces = []
    for it in items:
        st = it.get("pacing_status", "unmeasured")
        counts[st] = counts.get(st, 0) + 1
        v = it.get("pacing_morae_per_min")
        if isinstance(v, (int, float)):
            paces.append(v)

    summary_block = doc.setdefault("_meta", {}).setdefault("pacing_audit", {})
    summary_block["summary"] = {
        **counts,
        "min_observed": round(min(paces), 1) if paces else None,
        "max_observed": round(max(paces), 1) if paces else None,
        "mean_observed": round(sum(paces) / len(paces), 1) if paces else None,
    }
    summary_block.setdefault("note",
        "Refreshed 2026-05-17 against current VOICEVOX-rendered audio. "
        "See _meta.pacing_fix_status for BUG-049 disposition.")
    summary_block["target_range_morae_per_min"] = [PACING_TARGET_MIN, PACING_TARGET_MAX]
    summary_block["last_refresh"] = "2026-05-17"
    summary_block["method"] = (
        "Programmatic: mutagen MP3.info.length for duration; "
        "count_morae() kana-based (kanji=0 approximation) per "
        "tools-archive/fix_issue_074_pacing_audit_2026_05_06.py. "
        "Refreshed in this 2026-05-17 pass to match current audio "
        "(post-2026-05-12 VOICEVOX render + post-ffmpeg-atempo "
        "speedup where applicable)."
    )

    print(f"  Post-refresh summary: {counts}")
    if paces:
        print(f"  mpm: min={min(paces):.1f}, max={max(paces):.1f}, "
              f"mean={sum(paces)/len(paces):.1f}")

    # Update _meta.pacing_fix_status to reflect BUG-049 progress
    fix_status = doc["_meta"].setdefault("pacing_fix_status", {})
    fix_status["last_action"] = "2026-05-17 — re-measured all 50 items + applied ffmpeg atempo speedup"
    fix_status["current_distribution"] = counts
    if args.apply_speedup:
        in_range_n = counts.get("in_range", 0)
        too_slow_n = counts.get("too_slow", 0)
        if too_slow_n == 0:
            fix_status["status"] = "fixed_2026_05_17"
            fix_status["resolution"] = (
                "All items in JLPT N5 target band 180-240 mpm after re-measure + ffmpeg atempo."
            )
        else:
            fix_status["status"] = f"partial_2026_05_17_{too_slow_n}_remaining"
            fix_status["resolution"] = (
                f"{in_range_n}/{len(items)} items in target band; {too_slow_n} items "
                f"still too_slow — flagged with `pacing_fix_method_required` "
                f"indicating VOICEVOX re-render or script rewrite needed."
            )

    if not args.dry_run:
        LISTENING.write_text(
            json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"\nSaved {LISTENING}")
    else:
        print("\n(--dry-run; no files saved)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
