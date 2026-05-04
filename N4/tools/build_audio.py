"""Build audio assets for grammar examples and reading passages.

Why a build-time pipeline (Brief §1.1, §5):
    The app must run with no remote API at runtime. So all audio is generated
    OFFLINE during a build step and committed (or shipped to a separate assets
    repo and pre-cached by the service worker on first online visit).

Backends supported (auto-detected, first-available wins):
    1. piper-tts (https://github.com/rhasspy/piper) - high-quality neural,
       offline. Recommended.
       Install:  pip install piper-tts
       Voice:    download a Japanese voice ONNX, e.g.
                   wget https://huggingface.co/rhasspy/piper-voices/resolve/main/ja/ja_JP/jp-takaha-medium/ja_JP-takaha-medium.onnx
                   wget https://huggingface.co/rhasspy/piper-voices/resolve/main/ja/ja_JP/jp-takaha-medium/ja_JP-takaha-medium.onnx.json
                 and pass --voice <path-to-onnx>.
    2. pyttsx3 (offline, OS-native) - works without network. Voice quality
       depends on what's installed on the OS. On Windows, SAPI5 'Haruka' or
       'Ayumi' may be present if the Japanese language pack is installed.

Output:
    audio/grammar/<pattern_id>.<example_idx>.mp3      (or .wav from pyttsx3)
    audio/reading/<passage_id>.mp3
    audio/listening/<item_id>.mp3
    data/audio_manifest.json                          - which IDs were rendered

Run from the repo root:
    python tools/build_audio.py [--backend piper|pyttsx3] [--voice path] [--limit N]

The script is IDEMPOTENT: it skips outputs that already exist unless --force.

This pipeline is OPT-IN. The app degrades gracefully when audio files are
missing - players show no clip, and the listening module shows a notice.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
READING_JSON = ROOT / "data" / "reading.json"
LISTENING_JSON = ROOT / "data" / "listening.json"
MANIFEST = ROOT / "data" / "audio_manifest.json"
OUT_GRAMMAR = ROOT / "audio" / "grammar"
OUT_READING = ROOT / "audio" / "reading"
OUT_LISTENING = ROOT / "audio" / "listening"


def detect_backend(prefer: str | None = None):
    """Pick the first backend that imports successfully or is reachable."""
    candidates = []
    if prefer:
        candidates.append(prefer)
    # voicevox first (free, native Japanese acoustic models, MIT-style)
    if "voicevox" not in candidates:
        candidates.append("voicevox")
    # piper second (offline neural)
    if "piper" not in candidates:
        candidates.append("piper")
    # gtts third (network at build-time, OK quality)
    if "gtts" not in candidates:
        candidates.append("gtts")
    # pyttsx3 last (OS-native fallback)
    if "pyttsx3" not in candidates:
        candidates.append("pyttsx3")

    for name in candidates:
        try:
            if name == "voicevox":
                # VOICEVOX is reached over HTTP; check if the engine
                # is running on its default port. The user must launch
                # the engine separately (it's a desktop app).
                import urllib.request
                try:
                    urllib.request.urlopen("http://127.0.0.1:50021/version", timeout=1)
                    return "voicevox"
                except Exception:
                    continue
            if name == "piper":
                import piper  # noqa: F401
                return "piper"
            if name == "gtts":
                import gtts  # noqa: F401
                return "gtts"
            if name == "pyttsx3":
                import pyttsx3  # noqa: F401
                return "pyttsx3"
        except ImportError:
            continue
    return None


class VoicevoxBackend:
    """VOICEVOX engine over HTTP. Free, JA-native, runs locally.

    Setup (one-time):
        1. Install VOICEVOX from https://voicevox.hiroshiba.jp/
           (Windows / macOS / Linux desktop app, free, MIT-style)
        2. Launch the app — it starts an HTTP engine on
           http://127.0.0.1:50021/
        3. Run this builder: `python tools/build_audio.py --backend voicevox`

    Voice IDs (speaker_id). Pick a calm reading-suitable voice for N5
    listening drills. Defaults to 四国めたん「ノーマル」 (id=2) which has
    a neutral, clear prosody appropriate for educational content.

    Per-item override: if a `voice` field on the source listening item
    encodes a specific speaker_id (e.g., "synthetic-voicevox-shikoku-metan"
    -> 2, "synthetic-voicevox-zundamon" -> 3), the backend can route
    accordingly. For now we use a single fixed voice; refine if needed.
    """
    DEFAULT_SPEAKER_ID = 2  # 四国めたん「ノーマル」

    def __init__(self, voice: str | None = None):
        import urllib.request
        self.suffix = ".mp3"
        self.endpoint = "http://127.0.0.1:50021"
        # voice argument is the speaker id as a string, or a name we map
        if voice and voice.isdigit():
            self.speaker_id = int(voice)
        else:
            self.speaker_id = self.DEFAULT_SPEAKER_ID
        # Verify reachability
        try:
            urllib.request.urlopen(f"{self.endpoint}/version", timeout=2)
        except Exception as e:
            raise RuntimeError(
                f"VOICEVOX engine not reachable at {self.endpoint}. "
                "Launch the VOICEVOX desktop app first. "
                f"Underlying error: {e}"
            )

    def render(self, text: str, out_path: Path):
        import json as _json
        import urllib.parse
        import urllib.request
        # Step 1: get audio_query (analysis result)
        q_url = (
            f"{self.endpoint}/audio_query"
            f"?text={urllib.parse.quote(text)}"
            f"&speaker={self.speaker_id}"
        )
        q_req = urllib.request.Request(q_url, method="POST")
        with urllib.request.urlopen(q_req, timeout=30) as r:
            audio_query = r.read()
        # Step 2: synthesise WAV
        s_url = f"{self.endpoint}/synthesis?speaker={self.speaker_id}"
        s_req = urllib.request.Request(
            s_url,
            data=audio_query,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(s_req, timeout=120) as r:
            wav_bytes = r.read()
        # Step 3: write as WAV first, then convert to MP3 if ffmpeg is around.
        # If conversion fails (no ffmpeg), keep the WAV - the player handles
        # both via <audio> element.
        wav_path = out_path.with_suffix(".wav")
        wav_path.write_bytes(wav_bytes)
        try:
            import subprocess
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(wav_path), "-codec:a", "libmp3lame",
                 "-qscale:a", "2", str(out_path)],
                check=True, capture_output=True,
            )
            wav_path.unlink()
        except (FileNotFoundError, subprocess.CalledProcessError):
            # No ffmpeg / conversion failed. Leave WAV; manifest will still
            # carry .mp3 path but the file on disk is the WAV. Practical
            # workaround: rename .wav to .mp3 (browsers don't enforce the
            # extension; the audio element sniffs the actual format).
            wav_path.rename(out_path)


class GttsBackend:
    """Google Translate TTS - network at BUILD TIME ONLY (not runtime)."""
    def __init__(self, _voice: str | None = None):
        from gtts import gTTS  # noqa: F401
        self.suffix = ".mp3"

    def render(self, text: str, out_path: Path):
        from gtts import gTTS
        tts = gTTS(text=text, lang="ja", slow=False)
        tts.save(str(out_path))


class PiperBackend:
    def __init__(self, voice_path: str):
        from piper.voice import PiperVoice
        if not voice_path or not Path(voice_path).exists():
            raise RuntimeError(
                "Piper requires --voice <path-to-.onnx>. Download from "
                "https://github.com/rhasspy/piper-voices and pass the file path."
            )
        self.voice = PiperVoice.load(voice_path)
        self.suffix = ".wav"

    def render(self, text: str, out_path: Path):
        with open(out_path, "wb") as f:
            self.voice.synthesize(text, f)


class Pyttsx3Backend:
    def __init__(self, voice_id: str | None = None):
        import pyttsx3
        self.engine = pyttsx3.init()
        # Try to find a Japanese voice
        if voice_id:
            self.engine.setProperty("voice", voice_id)
        else:
            for v in self.engine.getProperty("voices"):
                if "japan" in v.name.lower() or "ja" in (v.languages and v.languages[0] or "").lower():
                    self.engine.setProperty("voice", v.id)
                    break
        self.suffix = ".wav"

    def render(self, text: str, out_path: Path):
        self.engine.save_to_file(text, str(out_path))
        self.engine.runAndWait()


_DIGIT_KANJI = {'0': '〇', '1': '一', '2': '二', '3': '三', '4': '四',
                '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}

def _num_to_kanji(num: int) -> str:
    """Convert an int 0-9999 to its Japanese kanji form for TTS.

    Examples: 1 -> 一, 10 -> 十, 30 -> 三十, 100 -> 百, 1500 -> 千五百.
    Beyond 9999 we fall back to digit-by-digit which gTTS still reads
    in Japanese context if surrounded by Japanese text.
    """
    if num == 0:
        return '〇'
    if num >= 10000:
        return ''.join(_DIGIT_KANJI[d] for d in str(num))
    parts = []
    thousands = num // 1000
    if thousands:
        parts.append(('' if thousands == 1 else _DIGIT_KANJI[str(thousands)]) + '千')
    rem = num % 1000
    hundreds = rem // 100
    if hundreds:
        parts.append(('' if hundreds == 1 else _DIGIT_KANJI[str(hundreds)]) + '百')
    rem = rem % 100
    tens = rem // 10
    if tens:
        parts.append(('' if tens == 1 else _DIGIT_KANJI[str(tens)]) + '十')
    ones = rem % 10
    if ones:
        parts.append(_DIGIT_KANJI[str(ones)])
    return ''.join(parts)


_DIGIT_RUN = re.compile(r'\d+')

def normalize_for_tts(text: str) -> str:
    """Pre-process Japanese text for TTS so digits read in Japanese, not English.

    gTTS pronounces ASCII digits in English when surrounded by Japanese
    ('3' -> 'three' instead of 'sa-n'). This converts ASCII digit runs to
    their kanji equivalents BEFORE rendering. The display text in the
    JSON is unchanged - this only affects the TTS input.
    """
    def _sub(m):
        try:
            return _num_to_kanji(int(m.group()))
        except (ValueError, KeyError):
            return m.group()
    return _DIGIT_RUN.sub(_sub, text)


def collect_jobs(force: bool, limit: int | None):
    """Return list of (text, out_path, source_id).

    Each text is run through normalize_for_tts() so digits hit the TTS
    engine as kanji (read in Japanese) instead of ASCII (read in English).
    """
    jobs = []

    # Grammar examples
    if GRAMMAR_JSON.exists():
        g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
        for p in g.get("patterns", []):
            for i, ex in enumerate(p.get("examples", []) or []):
                ja = ex.get("ja")
                if not ja or "(see " in ja:
                    continue
                out = OUT_GRAMMAR / f"{p['id']}.{i}"
                jobs.append((normalize_for_tts(ja), out, f"grammar.{p['id']}.{i}"))

    # Reading passages
    if READING_JSON.exists():
        r = json.loads(READING_JSON.read_text(encoding="utf-8"))
        for p in r.get("passages", []):
            ja = p.get("ja")
            if not ja:
                continue
            out = OUT_READING / p["id"]
            jobs.append((normalize_for_tts(ja), out, f"reading.{p['id']}"))

    # Listening items
    if LISTENING_JSON.exists():
        l = json.loads(LISTENING_JSON.read_text(encoding="utf-8"))
        for it in l.get("items", []):
            ja = it.get("script_ja") or it.get("prompt_ja")
            if not ja:
                continue
            out = OUT_LISTENING / it["id"]
            jobs.append((normalize_for_tts(ja), out, f"listening.{it['id']}"))

    if limit:
        jobs = jobs[:limit]
    return jobs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--backend", choices=["piper", "gtts", "pyttsx3", "auto"], default="auto")
    ap.add_argument("--voice", help="Voice file (piper) or voice id (pyttsx3)")
    ap.add_argument("--limit", type=int, help="Limit jobs (for testing)")
    ap.add_argument("--force", action="store_true", help="Re-render existing files")
    args = ap.parse_args()

    backend_name = args.backend if args.backend != "auto" else detect_backend()
    if not backend_name:
        print("ERROR: no TTS backend installed.", file=sys.stderr)
        print("Install one:", file=sys.stderr)
        print("  pip install piper-tts     # recommended (offline neural)", file=sys.stderr)
        print("  pip install pyttsx3       # OS-native voices", file=sys.stderr)
        return 2

    if backend_name == "voicevox":
        backend = VoicevoxBackend(args.voice)
    elif backend_name == "piper":
        backend = PiperBackend(args.voice)
    elif backend_name == "gtts":
        backend = GttsBackend(args.voice)
    else:
        backend = Pyttsx3Backend(args.voice)

    OUT_GRAMMAR.mkdir(parents=True, exist_ok=True)
    OUT_READING.mkdir(parents=True, exist_ok=True)
    OUT_LISTENING.mkdir(parents=True, exist_ok=True)

    # Read prior manifest (if any) so per-item `voice: "native"` overrides
    # are preserved across rebuilds. Per OQ-2 backlog (TASKS.md): items
    # marked "native" are recorded externally — the builder must NOT try to
    # synthesise them. This keeps the corpus mixed-voice safe.
    prior_voice: dict[str, str] = {}
    if MANIFEST.exists():
        try:
            prior = json.loads(MANIFEST.read_text(encoding="utf-8"))
            for it in prior.get("items", []):
                if it.get("voice"):
                    prior_voice[it["id"]] = it["voice"]
        except Exception:
            pass  # fall through; treat as no prior voice info

    voice_default = f"synthetic-{backend_name}"  # e.g. synthetic-gtts, synthetic-piper
    jobs = collect_jobs(args.force, args.limit)
    print(f"Backend: {backend_name}. Jobs: {len(jobs)}.")
    rendered = 0
    skipped = 0
    skipped_native = 0
    failed = 0
    manifest = {
        "backend": backend_name,
        # `voice_default` is the voice used for items lacking a per-item
        # `voice` field. Per-item `voice: "native"` overrides this and tells
        # consumers (and this builder) that the audio is externally recorded
        # by a human voice talent rather than synthesised.
        "voice_default": voice_default,
        "items": [],
    }

    for text, out_base, src_id in jobs:
        # Append suffix manually rather than using with_suffix, because IDs
        # like 'n5-001.0' contain a dot that with_suffix would treat as the
        # existing suffix (causing all examples for one pattern to collide).
        out = Path(str(out_base) + backend.suffix)
        # Always serialize manifest paths with forward slashes (POSIX
        # convention) regardless of build-host OS. Audio files are fetched
        # by the runtime via fetch() / <audio src=...> which both expect
        # URL-style forward slashes. Backslash-on-Windows broke PWA
        # deployment (infra audit 2026-05-03 §2.1).
        item: dict = {
            "id": src_id,
            "path": out.relative_to(ROOT).as_posix(),
        }
        # Preserve any prior per-item voice metadata, then decide rendering.
        prior_v = prior_voice.get(src_id)
        if prior_v == "native":
            # Externally recorded; don't synthesise. Just record presence.
            item["voice"] = "native"
            skipped_native += 1
            manifest["items"].append(item)
            continue
        if prior_v:
            item["voice"] = prior_v
        if out.exists() and not args.force:
            skipped += 1
            item["skipped"] = True
            manifest["items"].append(item)
            continue
        try:
            backend.render(text, out)
            rendered += 1
            # Newly rendered items: stamp with the active backend's voice
            # unless they already inherited a prior voice.
            if "voice" not in item:
                item["voice"] = voice_default
            manifest["items"].append(item)
            if rendered % 25 == 0:
                print(f"  ... {rendered} rendered")
        except Exception as e:
            failed += 1
            print(f"FAIL {src_id}: {e}", file=sys.stderr)

    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Done. rendered={rendered} skipped={skipped} skipped_native={skipped_native} failed={failed}.")
    print(f"Manifest: {MANIFEST.relative_to(ROOT)}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
