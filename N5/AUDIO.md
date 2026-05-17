# Audio pipeline

JLPT N5 Tutor ships **718 short Japanese audio clips** (~24 MB) that
play inline on grammar examples, reading passages, listening drills,
and the chokai virtual mock paper. **All audio is generated offline at
build time and committed to the repo** — the runtime never makes a
TTS API call.

## Current state (2026-05-17, post-Phase-2 VOICEVOX re-render)

| Module    | Total declared | On disk | Backend (actual) | Voices |
|-----------|----------------|---------|------------------|--------|
| Grammar   | 1782           | 1782 (100%) | **VOICEVOX 0.25.2** | 1 (春日部つむぎ, speaker 8) |
| Reading   | 54             | 54 (100%)   | gTTS                  | 1 |
| Listening | 50             | 50 (100%)   | **VOICEVOX 0.25.2**   | **6** (rotating) |
| Kanji per-yomi | 259       | 259 (100%)  | **VOICEVOX 0.25.2**   | 1 (春日部つむぎ, speaker 8) |
| **Total** | **2145**       | **2145 (100%)** | VOICEVOX-dominant | — |

Round-9 close-out (2026-05-07) brought all three modules to 100%
coverage and replaced single-voice synthetic listening with
**multi-voice VOICEVOX** at JLPT-N5 target pace.

Round-10 (2026-05-12, commit `c28266d`) extended VOICEVOX to grammar
examples (gTTS → VOICEVOX flip, 1782 files re-rendered).

Round-11 (2026-05-14, commit `f21b64e` + post-A47 sweep) patched
the VOICEVOX renderer to strip JLPT-textbook bunsetsu spaces before
passing text to OpenJTalk (otherwise the inter-bunsetsu pause
inserted by OpenJTalk devoices trailing particles, making them
inaudible). All 1782 grammar examples re-rendered. See A47 / F.12 /
AUDIT-COVERAGE-2026-05-15 §Addendum-2026-05-14 for the failure-class
documentation.

## Provider matrix

The N5 build pipeline is **multi-provider with auto-fallback**. Each
module picks the best provider available on the build host:

| Provider | Status | Used for | Why |
|----------|--------|----------|-----|
| **VOICEVOX** (`http://127.0.0.1:50021`) | **Primary for grammar + listening + kanji yomi** (round-10/11 actual) | grammar, listening, kanji yomi | Local engine, MIT-style licence, 30+ Japanese voices, native prosody, no network at build time. **Renderer at `tools/build_audio_voicevox.py` MUST strip bunsetsu spaces** before passing text to VOICEVOX — see A47 / F.12 for the failure class. |
| **edge-tts** (Microsoft Neural via WSS) | Optional / planned | listening, future | 7+ JP voices, free, no API key, but **WSS connection to `wss://speech.platform.bing.com` blocked by some corporate firewalls** — use VOICEVOX where blocked |
| **gTTS** (Google Translate TTS) | **Primary for reading passages only** (post-round-10) | reading | Stable, 1-line install, single voice acceptable for passage narration. Grammar flipped to VOICEVOX 2026-05-12 (commit `c28266d`). |
| piper-tts | Future fallback | none currently | Smaller engine for CI; rougher JP prosody than VOICEVOX |

Builders auto-detect what's available; fall back order on the listening
module is **VOICEVOX → edge-tts → gTTS**. Grammar defaults to VOICEVOX
(post-2026-05-12); reading defaults to gTTS.

## Listening multi-voice plan (round-9 plan + 2026-05-12 actual; counts refreshed 2026-05-17 post-BUG-052/053)

50 listening items use 6 distinct VOICEVOX speakers in rotation, with
speaker-role mapping from `script_ja` line prefixes (男 / 女 / narrator
/ 店員 / 先生 / 学生 / 母 / A / B / F / M).

The original round-9 plan (2026-05-06) targeted 8 speakers across 47
items; the actual 2026-05-12 render landed 6 speakers across 50 items
(IDs 14 冥鳴ひまり + 53 ナースロボ＿タイプＴ from the plan were not
used in the render — see `data/listening.json._meta.voice_variety_plan`
for the corrected speaker catalog and the unmet-target note). Earlier
revisions of this table had wrong character→ID mappings (e.g., ID 11
labeled "Shirakami Kotaro" — incorrect; VOICEVOX 11 is actually 玄野武宏 /
Kurono Takehiro). The table below is derived from
`audio_render_meta.voices_used` on the actual rendered items as of
2026-05-17.

| Speaker | VOICEVOX ID | Items rendered | Role bucket | Use |
|---------|-------------|---:|-------------|-----|
| 春日部つむぎ ノーマル (Kasukabe Tsumugi)  |  8 | 25 | Female (upbeat) | Default 女 / F / 学生 / 店員 |
| 四国めたん ノーマル (Shikoku Metan)        |  2 | 17 | Female (warm)   | Alt 女 / 母 / narrator |
| 玄野武宏 ノーマル (Kurono Takehiro)        | 11 | 12 | Male (warm)     | Default 男 / M / A / 学生 |
| 雨晴はう ノーマル (Amehare Hau)            | 10 |  8 | Female (calm)   | Alt 女 / narrator |
| ずんだもん ノーマル (Zundamon)              |  3 |  6 | Other (cute)    | Cameo / 学生 / narrator |
| 青山龍星 ノーマル (Aoyama Ryusei)          | 13 |  6 | Male (deeper)   | Alt 男 / 先生 / B / narrator |

Voice rotation is deterministic per item (seeded by `id`) so re-renders
are reproducible. **Current speed_scale (Phase-2, 2026-05-17): 1.00**
— close to native conversational pace; out-of-band items get
per-item ffmpeg post-processing (single-pass `atempo` for factor in
[0.5, 2.0]; single-pass `rubberband` for factor < 0.5) to land them
in the JLPT-N5 target band of **180–240 morae/min**. See
`docs/AUDIO-PHASE2-VOICEVOX-RERENDER.md` for the full phase history
(2026-05-12 render at 0.95 → Phase-1 atempo `47d1edc` → Phase-1.5
rubberband `c79c02e` → Phase-2 from-source re-render `cdd0e6d`).

Each rendered file's metadata is captured in
`data/audio_manifest_voice.json` and inlined into the per-item
`audio_render_meta` block in `data/listening.json`:

```json
"audio_render_meta": {
  "voice_provider": "voicevox",
  "voicevox_engine_version": "0.25.2",
  "voices_used": [
    "voicevox-speaker-8-春日部つむぎ-ノーマル",
    "voicevox-speaker-11-玄野武宏-ノーマル"
  ],
  "speed_scale": 1.00,
  "rendered_at": "2026-05-17T18:30:00+00:00",
  "phase2_voicevox_rerender_2026_05_17": true,
  "post_render_tempo_change_2026_05_17": 0.95,
  "post_render_tempo_method": "ffmpeg-atempo"
}
```

Post-render tempo fields are only present on the 34 items where the
fresh VOICEVOX render landed outside target band; 16 items have no
post-processing fields.

## Builder scripts

| Script | Purpose | Backend(s) |
|--------|---------|------------|
| `tools/build_audio.py`                                        | Single-voice batch (grammar/reading), hybrid backend selection | VOICEVOX → piper → gTTS → pyttsx3 |
| `tools/build_audio_voicevox.py`                               | Multi-voice listening dialogues, parallel batch render, retry-on-network-flake | VOICEVOX only |
| `tools/render_listening_audio_voicevox.py`                    | Earlier single-pass VOICEVOX listening render (kept for reference) | VOICEVOX only |
| **`tools/build_listening_audio_multivoice_2026_05_07.py`**    | **Round-9 actual: 4-voice rotation, role-aware speaker mapping, hash-tracked re-render** | edge-tts → VOICEVOX (auto-fallback) |
| `tools/audit_audio_coverage.py`                               | Coverage gap report (used / declared per module) | n/a |
| **`tools/fix_truncated_audio_2026_05_07.py`**                 | **Truncation guard: scans all 718 files, re-renders any clipped at sentence-internal punctuation** | gTTS (re-render only) |
| `tools/cleanup_orphan_audio_2026_05_03.py`                    | Removes audio files no longer referenced by any data/*.json | n/a |
| `tools/refresh_audio_manifest_skipped_2026_05_03.py`          | Reconciles `data/audio_manifest.json` with on-disk state | n/a |

## How to run a full re-render with VOICEVOX

One-time setup (per machine):

1. Install VOICEVOX — Windows shortcut:
   ```
   winget install HiroshibaKazuyuki.VOICEVOX.CPU
   ```
   Or download manually: https://voicevox.hiroshiba.jp/ (~1.9 GB,
   MIT-style licence, runs entirely offline).
2. Launch the app — auto-starts an HTTP engine on
   `http://127.0.0.1:50021`.
3. Install ffmpeg (for WAV → MP3 transcode and listening segment
   concat):
   ```
   winget install Gyan.FFmpeg          # Windows
   brew install ffmpeg                  # macOS
   apt install ffmpeg                   # Linux
   ```
4. Confirm both work:
   ```
   curl http://127.0.0.1:50021/version  # → "0.25.2" or similar
   ffmpeg -version                       # → ffmpeg 6.x / 8.x
   ```
5. Install the Python deps used by the round-9 multivoice script:
   ```
   pip install edge-tts pydub mutagen gtts
   ```

Then run the builders:

```sh
# Multi-voice listening render via VOICEVOX (2026-05-12 production run
# covers all 50 items at the corrected 6-speaker catalog; the round-9
# 47-item / 4-speaker numbers in earlier docs are obsolete):
python tools/build_listening_audio_multivoice_2026_05_07.py

# Or the older one-tool-fits-all batch (any-backend wins):
python tools/build_audio.py --target grammar   --resume
python tools/build_audio.py --target reading   --resume
python tools/build_audio_voicevox.py --target listening --resume

# After render: audit coverage
python tools/audit_audio_coverage.py

# Sanity check: catch any truncated clips
python tools/fix_truncated_audio_2026_05_07.py
```

`--resume` skips files whose input text hash hasn't changed since the
last render (idempotent re-runs).

## Truncation guard (round-9, 2026-05-07)

A user-reported regression (`コーヒーは 飲みますが、にくは たべません。`
played only the first clause) traced to gTTS occasionally clipping at
sentence-internal punctuation. The guard at
`tools/fix_truncated_audio_2026_05_07.py`:

1. Scans all 718 audio files, computes
   `morae_per_second = morae(text) / duration(mp3)`.
2. Flags any file with rate > 5.5 morae/sec (well above gTTS's natural
   ~4 morae/sec pace — a sure sign of mid-sentence truncation).
3. Re-renders flagged files via fresh gTTS calls.
4. **Only replaces** the cached file if the fresh render is ≥ 20 %
   longer (avoids touching naturally-fast short emphatic sentences).

Round-9 found and re-rendered 9 truncated files
(`n5-002.2`, `n5-007.3`, `n5-024.1`, `n5-091.3`, `n5-104.3`,
`n5-162.0`, `n5-163.0`, `n5-173.0`, `n5-187.0`).

The guard is idempotent — re-runs are no-ops once flagged files have
been replaced. Wire it into a release pre-commit hook to catch future
regressions.

## Multi-voice dialogue format

Two formats coexist in `data/listening.json`:

**A. Bracket-tag style (legacy, used by `build_audio_voicevox.py`)**

```json
{ "id": "n5.listen.013",
  "script_ja": "[F1] こんにちは。\n[M1] こんにちは。げんきですか。\n[F1] はい、げんきです。" }
```

**B. Role-prefix style (round-9 actual, used by
`build_listening_audio_multivoice_2026_05_07.py`)**

```json
{ "id": "n5.listen.013",
  "lines": [
    { "speaker": "女", "ja": "こんにちは。" },
    { "speaker": "男", "ja": "こんにちは。げんきですか。" },
    { "speaker": "女", "ja": "はい、げんきです。" }
  ] }
```

Both formats coexist; the round-9 builder reads `lines[]` first and
falls back to parsing `script_ja` if absent. Lines without an explicit
speaker inherit the previous speaker; the very first line defaults to
`narrator` → mapped per the table above.

## Auditing audio coverage

```sh
python tools/audit_audio_coverage.py
```

Output: per-module `present / declared` counts, list of missing IDs,
JSON dump to `feedback/audio-coverage-gaps.json`. Exit code 0 if 100 %
(current state), non-zero otherwise — wire into pre-commit if you want
hard-block on missing audio.

## Troubleshooting

**`VOICEVOX engine not reachable at http://127.0.0.1:50021`**

The desktop app isn't running, or it's on a non-default port. Launch
it; if you've changed the port, pass
`--endpoint http://127.0.0.1:<port>`.

**`aiohttp.ConnectionTimeoutError: wss://speech.platform.bing.com`
(edge-tts)**

Corporate firewall is blocking the WebSocket endpoint. **Pivot to
VOICEVOX** — that's exactly why round-9 chose it as primary. The
multivoice script auto-falls-back if `VOICEVOX_ENGINE_URL` is set or
if it detects a running local engine.

**`subprocess.CalledProcessError: ffmpeg ... non-zero exit`**

Either ffmpeg isn't on `PATH`, or your input WAV has corrupt headers.
Run `ffmpeg -i path/to/seg-000.wav` to inspect; if the file is empty,
the VOICEVOX synth call returned 0 bytes (engine bug — restart the
app).

**`HTTP 422` from VOICEVOX**

Text contains characters the engine can't handle (rare; mostly exotic
kanji). Workaround: re-write the line in hiragana for that one entry.

**Build silently produces 0-byte mp3s**

Check ffmpeg has `libmp3lame`: `ffmpeg -encoders | grep mp3`. Missing
codec → install a full ffmpeg build (Windows static from gyan.dev,
Linux `ffmpeg-extra-codecs` package).

**Audio plays but cuts off mid-sentence**

Run the truncation guard:
`python tools/fix_truncated_audio_2026_05_07.py`. If the issue persists
after re-render, check that the source text in `data/<module>.json`
doesn't contain literal `\n` or zero-width characters that confuse the
TTS engine.

## File layout

```
audio/
├── grammar/
│   ├── n5-001.0.mp3                # pattern n5-001, example index 0
│   ├── n5-001.1.mp3
│   └── …  (631 files)
├── reading/
│   ├── n5.read.001.mp3             # passage id verbatim
│   └── …  (40 files)
└── listening/
    ├── n5.listen.001.mp3           # listening item id verbatim
    └── …  (47 files)

data/
├── audio_manifest.json             # legacy build state — voice / hash per id
└── audio_manifest_voice.json       # round-9: per-item voice plan + render meta
```

## Reproducibility

Every render writes:

- The audio file in its target location.
- A manifest entry with: `path`, `voice`, `hash` (SHA256 of input text),
  `engine`, `rendered_at`.

A re-run with `--resume` reads the hash and skips items where the
input text hasn't changed. So a fresh checkout + `--resume` regenerates
only items added/edited since the last run.

The `audio_render_meta` block on each `data/listening.json` item also
captures the engine version (`voicevox_engine_version: "0.25.2"`) and
`speed_scale`, so the exact render conditions for any item are
recoverable from data alone.

## Native-speaker swap path (IMP-094, future)

The pipeline supports per-item replacement of synthetic audio with
native-speaker recordings without code changes — see
[`docs/NATIVE-AUDIO-WORKFLOW.md`](docs/NATIVE-AUDIO-WORKFLOW.md). The
`voice` field on each manifest item flags which provider rendered it
(`synthetic-gtts` / `synthetic-voicevox-<speaker>` / `native`); the
build pipeline skips items marked `native` so a hand-recorded file
isn't clobbered by a re-run.

This pathway is **content-team only** (recruitment + studio time);
no developer work is required to land a batch.

## Future: piper-tts as a third option

[Piper](https://github.com/rhasspy/piper) is a smaller, faster,
neural-but-not-as-natural alternative to VOICEVOX. Pre-trained Japanese
voices exist but have rougher prosody than VOICEVOX. Useful when
VOICEVOX's ~1.9 GB engine is too heavy (e.g. CI sandbox); not the
default. Install: `pip install piper-tts`, then
`python tools/build_audio.py --backend piper --voice <path-to-onnx>`.

Note: as of round-9 the `voices.json` registry has **no native
Japanese voice** — Piper is therefore not currently usable for N5 and
is documented only as a future option once a JP voice is published.
