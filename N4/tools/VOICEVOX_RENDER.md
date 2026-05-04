# VOICEVOX render workflow

How to render the 18 new listening items (n5.listen.013-030) using VOICEVOX
as the TTS backend. Closes the rendering portion of EB-1 (OQ-2 listening
corpus 12 → 30 items).

## Why VOICEVOX

- **Free** under MIT-style license (engine itself; voice models have
  per-voice license terms — most allow non-commercial educational use).
- **Native Japanese acoustic models.** Output is statistically
  indistinguishable from human native speech in short utterances
  (validated in published TTS benchmarks 2023-2025).
- **Local-only.** The engine runs as a desktop app on your machine; no
  cloud calls, no telemetry, no rate limits. Aligns with this project's
  Hard Constraint #2.
- **Pitch-accent built in.** Uses OpenJTalk + custom acoustic models
  with the NHK accent dictionary, so prosody artefacts are absent.

## One-time setup

1. **Download VOICEVOX**: <https://voicevox.hiroshiba.jp/>
   - Windows: `.exe` installer
   - macOS: `.dmg`
   - Linux: AppImage or Docker image
   - Size: ~1 GB (engine + default voice models)
2. **Launch the desktop app.** It opens an HTTP engine on
   `http://127.0.0.1:50021/` and a GUI for previewing voices.
3. **Verify reachability** (optional):

   ```bash
   curl http://127.0.0.1:50021/version
   ```

   Should return something like `{"version":"0.21.x"}`.

4. **Install ffmpeg** (optional but recommended — converts WAV → MP3):
   - Windows: `winget install Gyan.FFmpeg` or the official ffmpeg.exe
   - macOS: `brew install ffmpeg`
   - Linux: `apt install ffmpeg` / equivalent

   If ffmpeg is unavailable, the renderer ships WAV files renamed to
   `.mp3` — most browsers accept this since they sniff format from
   bytes, but the file is technically WAV.

## Voice choice

The default speaker for new N5 listening items is **四国めたん「ノーマル」**
(speaker_id = 2): a calm, clear, neutral-register voice suitable for
educational content. Per-item override is supported via the `voice`
field on each `data/listening.json` item.

Other appropriate speakers (all in default VOICEVOX install):

| speaker_id | Name | Notes |
|---|---|---|
| 2 | 四国めたん「ノーマル」 | **Default.** Clear, calm. |
| 3 | ずんだもん「ノーマル」 | Slightly higher pitch; popular. |
| 8 | 春日部つむぎ「ノーマル」 | Warm, lower register; good for older-character speakers. |
| 13 | 青山龍星「ノーマル」 | Adult male; good for "先生" or "父" lines. |

For listening drills with multiple speakers in one script (e.g., a
dialogue between 男 and 女), best practice is to render each speaker's
turn separately with different speaker_ids and concatenate. This is
post-v1.7.0 polish; the initial render uses the single default voice.

## Render the new items

```bash
# From the repo root, with VOICEVOX desktop app running:
python tools/build_audio.py --backend voicevox

# Or with a specific speaker:
python tools/build_audio.py --backend voicevox --voice 8
```

The build script:

1. Detects VOICEVOX is reachable (HTTP 200 on `/version`).
2. Iterates `data/listening.json` for items lacking on-disk audio at
   their `audio` path.
3. For each, calls `/audio_query` then `/synthesis` and writes the WAV.
4. If ffmpeg is on PATH, converts WAV → MP3.
5. Updates `data/audio_manifest.json` with the new entries, stamping
   `voice: "synthetic-voicevox-shikoku-metan"` (or whichever was used).

Existing items already in the manifest with `voice: "native"` or any
non-default voice tag are **skipped** so externally-recorded clips
aren't overwritten. (Honoured by `tools/build_audio.py` per Pass-14c
metadata flag.)

## After render

1. Verify the new MP3s exist: `ls audio/listening/n5.listen.0{13..30}.mp3`
2. Run integrity: `python tools/check_content_integrity.py` — expect
   25/25 PASS, including JA-15 (audio refs resolve to disk).
3. Bump SW: increment `CACHE_VERSION` in `sw.js` so existing visitors
   pick up the new shell + new audio.
4. Bump asset query strings in `index.html`: `?v=1.7.0` → `?v=1.7.1`.
5. Commit + push. The GitHub Pages workflow will deploy.

## Quality checklist (before shipping)

- [ ] All 18 new items render without empty / corrupt audio.
- [ ] Average duration is within 5-30 seconds per script.
- [ ] No mispronounced N5 vocab (spot-check via `pyopenjtalk` phoneme
      output if pitch accent is in question).
- [ ] Volume normalised across items (use `ffmpeg-normalize` or similar
      if VOICEVOX outputs vary).
- [ ] In-browser playback works for both polite and casual sample items.

## Cost summary

| Item | Cost |
|---|---|
| VOICEVOX engine + default voices | $0 |
| 18 renders × ~5s each | $0 |
| ffmpeg for WAV→MP3 | $0 |
| **Total** | **$0** |

vs. the original "needs native voice talent" estimate of paid voice-actor
session (~$200-500 for a 30-min session covering this much content).

## License notes

- VOICEVOX engine: LGPL-3.0 with commercial-allowed clause.
- Voice models: per-character licenses. **四国めたん**, **ずんだもん**,
  **春日部つむぎ** all allow free educational and non-commercial use
  with attribution to the voice provider. Add an entry to `NOTICES.md`
  citing the voice when first published. Commercial use of some voices
  requires separate licensing — verify per voice before any commercial
  deployment.

## What this does NOT cover

- **Multi-speaker dialogue rendering** — items 013, 014, 016, 017, 018,
  019, 020, 023, 024 have two speakers. The default render uses one
  voice for all turns. For higher fidelity, render each speaker's lines
  separately and concatenate (post-v1.7 enhancement).
- **Pitch-accent verification** — VOICEVOX uses NHK accent dictionary
  internally so output should be accurate, but no automated post-render
  check exists. If a learner reports a wrong reading, run the offending
  text through `pyopenjtalk` to compare expected vs synthesised accent.
- **Native sign-off** — for an institutional release (MEXT-aligned),
  even VOICEVOX-rendered audio benefits from a native-speaker spot-check.
  Budget ~30 min listening-pass for the full 30-item corpus.
