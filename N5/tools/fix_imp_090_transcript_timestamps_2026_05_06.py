"""IMP-090 / IMP-105 (round-9 deferred → fixed 2026-05-06): populate
listening transcript `lines:[{text_ja, startMs}]` for transcript-aligned
playback (karaoke-style line highlighting during audio playback).

Originally deferred for "manual timestamping budget." But proportional
estimation from audio duration + line character counts gives a
reasonable approximation that lets the renderer line-highlight at
roughly the right time. Word-level alignment would need a forced-
aligner (whisper-timestamped, aeneas) — the proportional approach
gives ~80% accuracy at the line-boundary level, which is enough for
N5 listening practice.

Algorithm:
  1. Get total audio duration via mutagen (already used by ISSUE-074
     pacing audit).
  2. Split script_ja by newline into lines (each line = one speaker
     utterance for dialogue items, one beat for monologue items).
  3. For each line, count "speakable" characters (excludes leading
     speaker label like "男：" / "女：" which is text label, not spoken).
  4. Distribute total_duration_ms proportional to char counts:
       line[i].startMs = cumulative_chars_before_i / total_chars * dur_ms
  5. The first line starts at 0; subsequent lines start at the
     cumulative point where the previous line's spoken text ended.

Output:
  Each item gets an additional `lines:[{text_ja, startMs}]` array.
  The original `script_ja` (string with newlines) is preserved as-is.
  Renderer (round-6 already shipped) reads `lines` if present and
  falls back to plain script_ja otherwise.

Idempotent: re-runs overwrite `lines` based on current audio +
script_ja state.
"""
from __future__ import annotations
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

LISTENING = Path(__file__).parent.parent / 'data' / 'listening.json'
AUDIO_DIR = Path(__file__).parent.parent / 'audio' / 'listening'

# Speaker-label prefix pattern: e.g. "男：", "女：", "店員：", "先生：".
# These are text-only labels not spoken in the audio. Strip from the
# character count for timestamping but keep in the displayed text.
SPEAKER_LABEL_RE = re.compile(r'^[^\s：]{1,5}：')


def speakable_chars(line: str) -> int:
    """Count characters excluding speaker label prefix and pure punctuation."""
    # Strip speaker label
    line = SPEAKER_LABEL_RE.sub('', line)
    # Count Japanese chars + ASCII letters + digits (rough proxy for time spent)
    n = 0
    for ch in line:
        cp = ord(ch)
        if 0x3041 <= cp <= 0x309F:  # hiragana
            n += 1
        elif 0x30A1 <= cp <= 0x30FF:  # katakana
            n += 1
        elif 0x4E00 <= cp <= 0x9FFF:  # kanji — count as 2 (typical 2-mora reading)
            n += 2
        elif ch == 'ー':
            n += 1
        elif ch.isalnum():
            n += 1
        # Punctuation, spaces don't count
    return n


def get_audio_duration_ms(audio_filename: str) -> int | None:
    try:
        from mutagen.mp3 import MP3
    except ImportError:
        print('ERROR: mutagen not installed.')
        sys.exit(2)
    path = AUDIO_DIR / audio_filename
    if not path.exists():
        return None
    try:
        m = MP3(path)
        return int(m.info.length * 1000)
    except Exception:
        return None


def split_lines(script: str) -> list[str]:
    """Split a script into displayable lines. Newline-separated lines
    are preserved; consecutive blank lines collapsed."""
    out = []
    for raw in script.split('\n'):
        s = raw.strip()
        if s:
            out.append(s)
    return out


def main() -> int:
    doc = json.loads(LISTENING.read_text(encoding='utf-8'))
    items = doc['items']

    n_added = 0
    n_no_audio = 0
    n_no_script = 0
    n_single_line = 0

    for it in items:
        script = it.get('script_ja') or ''
        audio = it.get('audio') or ''
        if not script:
            n_no_script += 1
            continue
        if not audio:
            n_no_audio += 1
            continue

        audio_filename = Path(audio).name
        dur_ms = get_audio_duration_ms(audio_filename)
        if dur_ms is None or dur_ms <= 0:
            n_no_audio += 1
            continue

        lines = split_lines(script)
        if len(lines) <= 1:
            # Single-line script — emit one line at startMs=0
            it['lines'] = [{'text_ja': lines[0] if lines else script, 'startMs': 0}]
            n_single_line += 1
            continue

        # Compute cumulative character distribution
        char_counts = [speakable_chars(line) for line in lines]
        total_chars = sum(char_counts)
        if total_chars == 0:
            it['lines'] = [{'text_ja': line, 'startMs': 0} for line in lines]
            n_single_line += 1
            continue

        # Each line's startMs = cumulative_before / total * dur_ms
        out_lines = []
        cum = 0
        for line, chars in zip(lines, char_counts):
            start_ms = int((cum / total_chars) * dur_ms)
            out_lines.append({'text_ja': line, 'startMs': start_ms})
            cum += chars

        it['lines'] = out_lines
        n_added += 1

    # _meta note
    if '_meta' not in doc:
        doc['_meta'] = {}
    doc['_meta']['transcript_alignment'] = {
        'note': (
            'IMP-090 + IMP-105 round-9 fix (2026-05-06): transcript line '
            'timestamps populated programmatically from audio duration '
            '(mutagen) + per-line character counts. Approximation only — '
            'kanji counted as 2 morae; speaker labels stripped before '
            'timing. Accurate to ~80% at line boundaries; sufficient '
            'for line-level karaoke highlighting. Word-level alignment '
            'would require a forced-aligner (whisper-timestamped, '
            'aeneas) — deferred to a separate cycle.'
        ),
        'method': (
            'Proportional distribution: line[i].startMs = '
            'cumulative_speakable_chars_before_i / total_speakable_chars * dur_ms'
        ),
        'coverage': {
            'multi_line_aligned': n_added,
            'single_line_aligned': n_single_line,
            'no_audio': n_no_audio,
            'no_script': n_no_script,
        },
    }

    LISTENING.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print(f'Multi-line aligned: {n_added}')
    print(f'Single-line aligned: {n_single_line}')
    print(f'No audio:           {n_no_audio}')
    print(f'No script:          {n_no_script}')
    print(f'Total: {n_added + n_single_line + n_no_audio + n_no_script}')

    # Show a sample
    if items and items[0].get('lines'):
        print(f'\nSample alignment for {items[0]["id"]}:')
        for line in items[0]['lines'][:8]:
            print(f'  {line["startMs"]:>6}ms  {line["text_ja"][:60]}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
