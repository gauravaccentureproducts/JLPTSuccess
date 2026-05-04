# Audio pipeline

JLPT N5 Tutor ships ~600 short Japanese audio clips (~19 MB) that play
inline on grammar examples, reading passages, and listening drills. All
audio is generated **offline at build time** and committed to the repo —
the runtime never makes a TTS API call.

## Current state (2026-05-02)

| Module    | Total declared | On disk | Backend |
|-----------|----------------|---------|---------|
| Grammar   | 551            | 550     | gTTS    |
| Reading   | 30             | 30      | gTTS    |
| Listening | 30             | 12      | gTTS    |
| **Total** | **611**        | **592 (96.9%)** | mixed |

19 clips are missing — primarily listening 013–030 (INFRA-1) and one
grammar example (`n5-167.2`). These will be regenerated on the next
build cycle.

The current backend is gTTS (Google Translate TTS via the `gtts` Python
library). It works but has known limitations for Japanese:

- Robotic prosody on katakana words ("コーヒー" sounds halting)
- Single voice — every speaker sounds identical, which is wrong for
  listening dialogues with multiple turns
- Network call required at build time (not at runtime — but it does
  mean the build is non-reproducible without internet)

## Target backend: VOICEVOX

[VOICEVOX](https://voicevox.hiroshiba.jp/) is a free, MIT-style,
local-only Japanese TTS engine with 30+ trained voices. It gives us:

- **Native Japanese prosody** — designed for Japanese, not English-with-Japanese-words
- **Multi-voice dialogue** — different speakers per turn in listening drills
- **Offline build** — no network at build time once the engine is downloaded
- **Higher audio quality** — neural TTS, sounds natural

## How to run a full re-render with VOICEVOX

One-time setup (per machine):

1. Download the VOICEVOX engine for your OS:
   https://voicevox.hiroshiba.jp/ (~200 MB, free, MIT-style license)
2. Launch the app — it auto-starts an HTTP engine on
   `http://127.0.0.1:50021`
3. Install ffmpeg (used to transcode WAV → MP3):
   - Windows: `winget install ffmpeg` or grab a static build from
     https://www.gyan.dev/ffmpeg/builds/
   - macOS: `brew install ffmpeg`
   - Linux: `apt install ffmpeg`
4. Confirm both work:
   ```
   curl http://127.0.0.1:50021/version    # → "0.16.0" or similar
   ffmpeg -version                         # → ffmpeg version 6.x
   ```

Then run the builders:

```sh
# Render the missing listening drills (18 of 30)
python tools/build_audio_voicevox.py \
    --target listening \
    --missing-only \
    --workers 4

# Render the missing grammar example
python tools/build_audio_voicevox.py \
    --target grammar \
    --missing-only

# Full re-render of everything (overwrites existing files):
python tools/build_audio_voicevox.py --target listening --resume
python tools/build_audio_voicevox.py --target reading   --resume
python tools/build_audio_voicevox.py --target grammar   --resume
```

`--resume` skips files where the input text hash hasn't changed since
the last render (idempotent re-runs).

## Two builder scripts (different use cases)

| Script | Best for | Backends |
|--------|----------|----------|
| `tools/build_audio.py`          | One-tool batch, single voice, hybrid backend selection | VOICEVOX → piper → gTTS → pyttsx3 |
| `tools/build_audio_voicevox.py` | Multi-voice listening dialogues, parallel batch rendering, retry-on-network-flake | VOICEVOX only |

Use `build_audio.py` when you want any-backend-that's-installed-wins
(useful for quick fills without VOICEVOX setup).

Use `build_audio_voicevox.py` when you have VOICEVOX running and want:
- Multi-voice support via `[F1]` / `[M1]` / `[F2]` / `[M2]` script tags
- Parallel rendering (`--workers 4` is the default, raise if you have a
  beefy GPU)
- Better progress reporting + retry-on-transient-error logic

## Multi-voice dialogue format (VOICEVOX-only)

In `data/listening.json`, prefix each speaker turn with a tag:

```json
{
  "id": "n5.listen.013",
  "script_ja": "[F1] こんにちは。\n[M1] こんにちは。げんきですか。\n[F1] はい、げんきです。"
}
```

The builder parses tags and routes each segment to the right speaker:

| Tag | Speaker | VOICEVOX ID | Description |
|-----|---------|-------------|-------------|
| `[F1]` | 春日部つむぎ ノーマル | 8  | Default female (warm, casual) |
| `[F2]` | 四国めたん ノーマル    | 2  | Alternate female (upbeat)     |
| `[M1]` | ずんだもん ノーマル    | 3  | Default male (younger)        |
| `[M2]` | 玄野武宏 ノーマル      | 11 | Alternate male (deeper)       |

Lines without a tag inherit the previous speaker; the very first line
defaults to `[F1]`. Segments are synthesized individually then
concatenated via ffmpeg. Single-line scripts (no tags) skip the
concatenation step.

## Auditing audio coverage

```sh
python tools/audit_audio_coverage.py
```

Output: per-module `present / declared` counts, list of missing IDs,
and a JSON dump of the gap list to `feedback/audio-coverage-gaps.json`.
Run before/after a build to confirm what changed. Exit code 0 if 100%,
non-zero otherwise — wire into a pre-commit hook if you want to
hard-block missing-audio commits.

## Troubleshooting

**`VOICEVOX engine not reachable at http://127.0.0.1:50021`**

The desktop app isn't running, or it's running on a non-default port.
Launch it; if you've changed the port, pass `--endpoint
http://127.0.0.1:<port>`.

**`subprocess.CalledProcessError: ffmpeg ... returned non-zero exit status`**

Either ffmpeg isn't on `PATH`, or your input WAV has corrupt headers.
Run `ffmpeg -i path/to/seg-000.wav` to inspect; if the file is empty,
the VOICEVOX synth call returned 0 bytes (engine bug — restart the app).

**`HTTP Error 422` from VOICEVOX**

The text contains characters the engine can't handle (very rare, mostly
exotic kanji). Check `data/listening.json` for the offending entry; if
it's a real N5 character, file a bug to the VOICEVOX repo. Workaround:
re-write the line in hiragana for that one entry.

**The build silently produces 0-byte mp3s**

Check that ffmpeg is finding `libmp3lame`. Run `ffmpeg -encoders | grep
mp3` — should list `libmp3lame`. If missing, your ffmpeg was built
without the codec; install a full build (most distributions package
this; Windows static builds from gyan.dev include it).

## Future: piper-tts as a third option

[Piper](https://github.com/rhasspy/piper) is a smaller, faster,
neural-but-not-as-natural alternative to VOICEVOX. Pre-trained Japanese
voices exist but have rougher prosody than VOICEVOX. Useful when
VOICEVOX's 200 MB engine is too heavy (e.g. CI sandbox); not the
default. Install: `pip install piper-tts`, then
`python tools/build_audio.py --backend piper --voice <path-to-onnx>`.

## File layout

```
audio/
├── grammar/
│   ├── n5-001.0.mp3      # pattern n5-001, example index 0
│   ├── n5-001.1.mp3
│   └── ...
├── reading/
│   ├── n5.read.001.mp3   # passage id verbatim
│   └── ...
└── listening/
    ├── n5.listen.001.mp3 # listening item id verbatim
    └── ...

data/audio_manifest.json   # build state — which IDs were rendered
                            # by which backend, with content hashes
```

## Reproducibility

Every render writes:
- The audio file in its target location
- A manifest entry with: `path`, `voice`, `hash` (SHA256 of input text)

A re-run with `--resume` reads the hash and skips items where the
input text hasn't changed. So a fresh checkout + `--resume` regenerates
only items added/edited since the last run.
