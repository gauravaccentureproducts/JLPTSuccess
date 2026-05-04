# VOICEVOX integration notes (parked)

**Status:** Closed-by-decision 2026-05-03. The current gTTS audio backend
is accepted as adequate for the JLPT N5 scope. This document is kept as
the activation recipe if a future content tier (N4 listening, dialogue
drills, pitch-accent practice) makes the upgrade worth the install +
render cost.

## Why parked, not done

gTTS produces intelligible Japanese audio for short single-speaker
clips. The N5 corpus is 1,003 vocab + ~15-second listening drills + a
handful of grammar examples — no long-form narration, no pitch-accent
drills, no dialogue practice that requires per-character voice
differentiation. The speaker context in listening drills is set in the
prompt text (`男の人と女の人が話しています ...`), so audio-level
voice differentiation isn't required for the question to be solvable.

The trade-off was:
- VOICEVOX upgrade buys: native pitch accent, multi-character dialogue,
  fully-offline rendering (no Google API).
- VOICEVOX upgrade costs: engine binary install on the build machine,
  a renderer script, ~3,000 clip re-render, license review of which
  character voices the project will use, periodic spot-check of pitch
  accent on rare words.

For the current scope the cost outweighs the benefit. For a future N4
or N3 expansion that adds pitch-accent practice or multi-speaker
dialogues, the calculation flips.

## Activation recipe (when ready)

### 1. Install the engine

The VOICEVOX engine is the headless TTS server. It exposes a REST API
on `http://localhost:50021`. Three install options:

- **Windows / macOS / Linux desktop app** — bundles GUI + engine.
  https://voicevox.hiroshiba.jp/ — download the runtime (~1.5 GB
  with all default voices).
- **Docker** — `docker run -p 50021:50021 voicevox/voicevox_engine:cpu-latest`
  — recommended for CI / build pipelines. CPU-only image is ~700 MB.
- **GPU image** — `voicevox/voicevox_engine:nvidia-latest` if a CUDA
  GPU is available. Roughly 5x faster but unnecessary for batch
  rendering.

Verify install:
```
curl http://localhost:50021/version
# → "0.x.y"
```

### 2. License review

VOICEVOX engine itself is LGPL-3.0. Each character voice model has its
own license. For an educational app most are fine; the project should
deliberately pick voices whose ToS permits the use case.

Recommended starter set (all permit commercial use with attribution):
- ずんだもん (Zundamon) — neutral teen voice, 5 styles
- 四国めたん (Shikoku Metan) — female teen voice, 5 styles
- 春日部つむぎ (Kasukabe Tsumugi) — female young-adult voice
- 玄野武宏 (Kurono Takehiro) — male adult voice (good for "男の人" speakers)

Each voice has an integer `speaker_id` queryable via
`GET /speakers`. Pin the IDs in the renderer script — never use the
default since `speaker_id=0` may shift between releases.

For the attribution requirement: add a `CREDITS.md` listing each
character + voice provider per the per-character ToS template at
https://voicevox.hiroshiba.jp/term/

### 3. Renderer script

The current `tools/build_audio.py` uses gTTS. Add a sibling
`tools/build_audio_voicevox.py` driven by the same content sources
(vocab.json, grammar.json, listening.json, reading.json examples) but
with a different synthesis function:

```python
import requests

def render_voicevox(text: str, speaker_id: int, out_path: Path) -> None:
    # 1. Audio query — VOICEVOX returns a per-text accent dictionary
    #    that you can hand-edit before synthesis.
    q = requests.post(
        "http://localhost:50021/audio_query",
        params={"text": text, "speaker": speaker_id},
    ).json()
    # 2. Synthesis — pass the (possibly hand-tweaked) query back to get WAV.
    wav = requests.post(
        "http://localhost:50021/synthesis",
        params={"speaker": speaker_id},
        json=q,
    ).content
    # 3. Convert to MP3 to keep the manifest schema unchanged.
    out_path.write_bytes(wav)
    # ... ffmpeg WAV → MP3 transcode ...
```

The two-step `audio_query` → `synthesis` is the key VOICEVOX
ergonomics: the query JSON contains a `mora`-by-`mora` accent
description that you can patch when the default reading is wrong
(rare-but-real for vocabulary like 大坂 vs 大阪).

### 4. Multi-voice dialogues

For listening drills with multiple speakers (currently rendered as a
single concatenated gTTS clip), parse the `script` field for speaker
prefixes and route each line to a different `speaker_id`:

```
男の人: コーヒーを ください。
女の人: はい、 すぐに お持ちします。
```

Render each line separately, then concatenate with 200ms silence
between lines (ffmpeg `concat` filter).

### 5. Spot-check pass

Pitch accent occasionally goes wrong on rare words. After the bulk
render, sample ~50 random clips and compare against an authoritative
source (NHK 日本語発音アクセント新辞典 or OJAD). Hand-edit the
audio_query JSON for any mismatches and re-render those clips only.

Budget ~4 hours for the full sweep on the current corpus.

### 6. Cutover

The audio_manifest.json schema doesn't change — same `path`, `id`,
`backend` fields. Bump `backend` from `gtts` to `voicevox` in the
manifest. JA-15 (audio refs resolve to files on disk) keeps catching
broken paths. Replace the gTTS-rendered MP3s in place; the SW cache
will refresh on the next bump of `service-worker.js#CACHE_VERSION`.

## What this means for the master task list

INFRA-2 + INFRA-3 closed-by-decision 2026-05-03. If activated later,
this doc becomes the issue's body for a fresh tracker entry; the
master task list itself doesn't need to be re-opened.
