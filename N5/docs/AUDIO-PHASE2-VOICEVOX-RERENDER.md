# Audio Phase-2 — VOICEVOX re-render at speed_scale=1.00

**Status as of 2026-05-17: COMPLETED.** Phase-2 shipped in the
JA-91+JA-94 follow-on batch (commit pending) on 2026-05-17. All
50 listening items were re-rendered from source via VOICEVOX at
`speed_scale=1.00`, replacing the prior 2026-05-12 render at
`speed_scale=0.95` plus the Phase-1 (ffmpeg atempo) and Phase-1.5
(librubberband on 3 items) post-processing layers. Pacing
distribution post-Phase-2:

- in_range: 50 / 50 (target band 180–240 mpm)
- mean: 214.5 mpm; min 190.4; max 237.3
- 16 items needed no post-processing (rendered direct from VOICEVOX)
- 29 items needed single-pass `ffmpeg-atempo` adjustment (factor in
  [0.5, 2.0] range) to land in band
- 5 items needed single-pass `ffmpeg-rubberband` (factor < 0.5,
  outside atempo's single-pass range) — n5.listen.010, 041, 044,
  045, 047. Authoring follows the Phase-1.5 quality-upgrade pattern.

CI invariants: 122/122 green. Bug tracker: 53 / 53 Fixed / 0 Open.

## What Phase-2 delivered

A from-source VOICEVOX re-render at speed_scale=1.00 — closer to
native conversational pace than the 0.95 baseline — replacing all
50 listening primaries plus their `.slow.mp3` companions
(regenerated at single-pass `atempo=0.7` from the new primaries).
The chained-atempo artifact class (3 items at Phase-1, then 5 items
at Phase-2's post-render pacing pass) was retired both times via
the Phase-1.5 / Phase-2-follow-on librubberband substitute.

Per-item provenance: every item with `audio_render_meta.
phase2_voicevox_rerender_2026_05_17 = True` was re-rendered at
speed_scale=1.00 in this Phase-2 batch. The audio_render_meta also
captures `voices_used`, `voice_planned_for_engine`, and the
post-render tempo method (`null` / `ffmpeg-atempo` /
`ffmpeg-rubberband` per item).

## How Phase-2 was run

Procedure (one-time; preserved for future reference):

```bash
# 1. Confirm VOICEVOX is running:
curl http://127.0.0.1:50021/version    # → "0.25.2"

# 2. From N5/, run the Phase-2 renderer:
python tools/render_listening_phase2_voicevox_1_00_2026_05_17.py
# Reads data/listening.json, re-renders each item.script_ja at
# speed_scale=1.00, writes audio/listening/n5.listen.NNN.mp3 +
# .slow.mp3 (atempo=0.7), updates audio_render_meta per item.
# ~12 min wall-clock for 50 items on CPU engine.

# 3. Re-measure pacing + auto-apply atempo to items outside band:
python tools/refresh_listening_pacing_2026_05_17.py --apply-speedup
# Pass 1: re-measure all 50 against new audio.
# Pass 2: apply ffmpeg atempo to too_slow OR too_fast items
#         (factor < 0.5 chains 2 passes; will be replaced in step 4).
# Pass 3: re-measure post-tempo-change items.
# Pass 4: update _meta.pacing_audit.summary.

# 4. Replace chained-atempo (factor < 0.5) with librubberband
#    single-pass:
python tools/apply_phase2_rubberband_chained_items_2026_05_17.py
# For each item with factor < 0.5: re-render from VOICEVOX again,
# apply rubberband single-pass instead of atempo chain, regenerate
# the .slow.mp3 from the new primary, update meta.

# 5. Re-measure pacing (no --apply this time):
python tools/refresh_listening_pacing_2026_05_17.py

# 6. Verify CI green:
python tools/check_content_integrity.py
# Expect: PASS all 122 invariants.

# 7. Commit + push (file-based commit per CLAUDE.md commit rule):
python -c "open('.commit_msg.tmp','w',encoding='utf-8').write('...')"
git add N5/audio/listening/*.mp3 N5/data/listening.json N5/tools/...
git commit -F N5/.commit_msg.tmp
rm -f N5/.commit_msg.tmp
git push origin master
```

## What Phase-2 did NOT change

- The pacing CI invariant (JA-114). Still passes.
- The voice-speaker catalog (6 distinct speakers). Same 6 as before:
  speaker 8 春日部つむぎ / 11 玄野武宏 / 2 四国めたん / 3 ずんだもん /
  10 雨晴はう / 13 青山龍星. Per-item assignment unchanged.
- The script text (`script_ja` on every item).
- The bug tracker. BUG-048 / 049 stay Fixed; this was a quality
  upgrade, not a bug close.
- CI invariant count. Still 122/122.

## Provenance / records preserved in audio_render_meta

Each item's `audio_render_meta` carries:

```json
{
  "voice_provider": "voicevox",
  "voices_used": ["voicevox-speaker-8-春日部つむぎ-ノーマル", ...],
  "voicevox_engine_version": "0.25.2",
  "voice_planned_for_engine": {"F": {...}, "M": {...}},
  "rendered_at": "2026-05-17T18:xx:xx+00:00",
  "speed_scale": 1.00,
  "engine": "voicevox-cpu",
  "slow_render_filter": "atempo=0.7",
  "slow_render_date": "2026-05-17",
  "segments_count": <N>,
  "phase2_voicevox_rerender_2026_05_17": true,
  "post_render_tempo_change_2026_05_17": <factor>,  // present if atempo/rubberband applied
  "post_render_tempo_method": "ffmpeg-atempo" | "ffmpeg-rubberband",
  "phase15_method_change_2026_05_17": {...}  // present if rubberband replaced chained atempo
}
```

The Phase-1 / Phase-1.5 metadata fields (`post_render_tempo_change_
2026_05_17` / `post_render_tempo_method` / `phase15_method_change_
2026_05_17`) are CLEARED at the start of Phase-2 (since the audio
is re-rendered from source) and only re-applied if Phase-2's
post-render pacing pass actually needed them. After Phase-2:

- 16 items have no post-processing fields (rendered direct).
- 29 items have `post_render_tempo_method: ffmpeg-atempo`
  (single-pass atempo).
- 5 items have `post_render_tempo_method: ffmpeg-rubberband` +
  `phase15_method_change_2026_05_17` recording the swap rationale.

## Phase historical timeline

1. **2026-05-12**: Initial VOICEVOX render at `speed_scale=0.95`
   via `tools/render_listening_voicevox_6speakers.py`. 6-speaker
   variety established (BUG-052 close-out).
2. **2026-05-17 Phase-1** (commit `47d1edc`, BUG-048/049 close-out):
   pacing re-measurement + ffmpeg atempo applied to 39 items to
   land them in the JLPT N5 target band. 3 items needed chained
   atempo (factor < 0.5).
3. **2026-05-17 Phase-1.5** (commit `c79c02e`): librubberband
   replaced chained atempo on the 3 items (n5.listen.041 / 044 /
   045). The chained-atempo artifact class was retired at this
   point for those specific items.
4. **2026-05-17 Phase-2** (commit pending — THIS batch):
   from-source VOICEVOX re-render at `speed_scale=1.00`; post-
   render pacing pass produced 34 atempo adjustments (29
   single-pass + 5 chained); chained items replaced with
   librubberband single-pass.

Post-Phase-2 state is the definitive shipping state.
