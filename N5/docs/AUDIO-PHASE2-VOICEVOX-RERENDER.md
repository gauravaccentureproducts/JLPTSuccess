# Audio Phase-2 — VOICEVOX re-render at speed_scale=1.00

**Status as of 2026-05-17:** Phase-1 (ffmpeg atempo post-processing
on the 2026-05-12 VOICEVOX render at speed_scale=1.30) shipped in
commit `47d1edc`. All 50 listening items are now in the JLPT N5
target band 180–240 mpm; mean 213.6. BUG-048 and BUG-049 are
closed. CI passes.

**Phase-2 is a quality upgrade, not a correctness fix.** Phase-1
is shippable. Phase-2 cleans up the audio-processing artifacts
introduced by the chained ffmpeg atempo applied to 7 items with
slowdown factors below 0.5 (a 2-pass `atempo=0.5,atempo=...`
chain).

## Why Phase-2 exists

The 2026-05-12 VOICEVOX render used `speed_scale=1.30`. After
re-measurement (commit `47d1edc`, BUG-048 close-out) the actual
pacing was wildly above the target band — mean ~295 mpm vs target
180–240. The remedy was to slow the audio DOWN, not up.

ffmpeg's `atempo` filter handles tempo change with pitch
preservation (PSOLA-style algorithms). At factors in [0.5, 2.0]
single-pass, quality is near-transparent for speech. The 7 items
that needed factor < 0.5 were chained `atempo=0.5,atempo=X` to
reach effective factors of 0.476–0.499 — quality is still
intelligible but has slightly more processing artifacts than
single-pass.

A from-source VOICEVOX re-render at `speed_scale=1.00` would
produce cleaner audio for those 7 items (and arguably for the
other 32 slowed-down items too — VOICEVOX's native pace control
is higher fidelity than post-hoc atempo on the rendered MP3).

## Why this is deferred

Phase-2 requires VOICEVOX running locally:

1. Install VOICEVOX (Windows: `winget install
   HiroshibaKazuyuki.VOICEVOX.CPU`; macOS / Linux: manual
   download from <https://voicevox.hiroshiba.jp/>). ~1.9 GB
   download, MIT-style licence, runs entirely offline.
2. Launch the app — auto-starts an HTTP engine on
   `http://127.0.0.1:50021`.
3. The maintainer machine needs ffmpeg (already required for
   Phase-1; should already be installed).

This is a one-time per-machine setup. The agent-side tooling can't
do step 1 because VOICEVOX needs interactive install + binary
execution.

## How to run Phase-2 (when ready)

```bash
# 1. Confirm VOICEVOX is running:
curl http://127.0.0.1:50021/version    # → "0.25.2" or similar

# 2. From the repo root, run the re-render at speed_scale=1.00:
cd N5/
python tools/build_audio_voicevox.py --target listening --resume \
       --speed-scale 1.00 --force-re-render-all

# 3. The script re-renders every item at the new speed_scale,
#    overwriting audio/listening/n5.listen.{NNN}.mp3 +
#    audio/listening/n5.listen.{NNN}.slow.mp3 (the 0.7× variant
#    is auto-derived from the primary track).
#
# 4. Re-measure pacing + update _meta:
python tools/refresh_listening_pacing_2026_05_17.py
# (Without --apply-speedup; just refresh measurements.
# The new VOICEVOX render at 1.00× will likely land closer to
# 200-240 mpm without any atempo post-processing needed.)

# 5. Verify CI:
python tools/check_content_integrity.py
# Expect: PASS all 119 invariants.

# 6. Update audio_render_meta.post_render_tempo_change_2026_05_17
#    — remove the field on every item (no longer applicable; the
#    audio was rendered at the correct speed_scale from source).

# 7. Commit + push the audio-only batch:
git add N5/audio/listening/*.mp3 N5/data/listening.json
git commit -m "audio: Phase-2 — VOICEVOX re-render at speed_scale=1.00

Replaces the 2026-05-12 render at 1.30 + ffmpeg atempo
post-processing (47d1edc) with a from-source VOICEVOX render at
1.00. Cleaner audio quality, especially on the 7 items that
previously needed chained atempo (factor < 0.5).

Pacing distribution unchanged: 50/50 in target band 180-240 mpm
(re-measured post-render). audio_render_meta.post_render_tempo_
change_2026_05_17 cleared on all items (no longer applies)."
git push origin master
```

## What Phase-2 does NOT change

- The pacing CI invariant (JA-114) — already passes; will continue to.
- The voice-speaker catalog (`_meta.voice_variety_plan` —
  BUG-052/053 close-out). Same 6 speakers, same role assignments.
- The script text. Re-render uses the existing `script_ja` field
  on every item.
- The bug tracker. BUG-048 and BUG-049 stay Fixed (this is a
  quality upgrade, not a bug close).

## Estimated effort

- Setup (one-time): ~10 min (install + verify).
- Re-render run: ~25 min (50 items × 0.5 min average).
- Re-measure + verify: ~2 min.
- Commit + push: ~3 min.

**Total ~40 min once VOICEVOX is installed.** This is the only
remaining audio-side task surfaced by the 2026-05-17 audit.

## Provenance / records preserved

Even after Phase-2 lands, the audit trail of the Phase-1 post-
processing is preserved in git history (commit `47d1edc`'s log
message + the AUDIT-COVERAGE Part 16 addendum). Future native-
listener review can compare the Phase-1 audio against the Phase-2
audio if quality differences need to be characterized.
