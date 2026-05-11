"""Author estimated timestamped_transcript on listening items.

Audit context: timestamped_transcript = 0/50. Real audio waveform
analysis isn't in scope (no offline align tooling). This pass
produces ESTIMATED line-level timings by:

  1. Split script_ja on speaker tags (男:/女:/A:/B:/先生:/etc.).
  2. Count morae per line (kana + small-tsu + long-vowels).
  3. Distribute the item's audio_seconds_estimated across lines
     proportionally by mora count.

Schema:
  timestamped_transcript: {
    estimated: true,
    pacing_morae_per_min: <number>,
    total_seconds: <number>,
    lines: [
      {
        speaker: "男" | "女" | "A" | ...,
        text: "<line text>",
        mora_count: <int>,
        start_s: <float>,
        end_s: <float>,
      },
      ...
    ]
  }

Provenance: auto_derived. The `estimated: true` flag is the
renderer's signal that timing is NOT from audio analysis.
"""
from __future__ import annotations
import io, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


SPEAKER_RE = re.compile(r'^(?P<speaker>[A-Z]|男(?:の人)?|女(?:の人)?|男1|女1|男2|女2|先生|学生|店員|いしゃ|かんじゃ|母|父|子(?:ども)?|友|たけし|お?きゃくさん)[:：]\s*(?P<text>.*)$')


def split_lines(script: str) -> list[tuple[str, str]]:
    """Split script into (speaker, text) pairs. Lines without a
    speaker tag get '?' as speaker."""
    out = []
    for raw in script.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = SPEAKER_RE.match(line)
        if m:
            out.append((m.group('speaker'), m.group('text').strip()))
        else:
            out.append(('-', line))
    return out


def count_morae(text: str) -> int:
    """Approximate mora count: count hiragana/katakana except small
    tsu and small vowels (which extend the preceding mora). Small
    counters like ゃ/ゅ/ょ also belong to the preceding mora.
    Skip kanji (each counts as ~2 mora on average — but we have
    readings in kana for most listening scripts)."""
    small = set('ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶー')
    n = 0
    for ch in text:
        if ch in small:
            continue  # extends preceding mora; not counted separately
        # Hiragana/katakana range
        cp = ord(ch)
        if 0x3041 <= cp <= 0x3096 or 0x30A1 <= cp <= 0x30FA:
            n += 1
        elif 0x4E00 <= cp <= 0x9FFF:
            n += 2  # kanji ~2 mora on average
    return n


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_timestamps')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    n = 0
    n_skip_no_script = 0
    n_skip_short = 0

    for it in data['items']:
        if it.get('timestamped_transcript'):
            continue
        script = it.get('script_ja') or ''
        if not script:
            n_skip_no_script += 1
            continue
        lines = split_lines(script)
        if len(lines) < 2:
            n_skip_short += 1
            continue

        total_s = (it.get('time_target_seconds') or {}).get('audio_seconds_estimated')
        if not total_s:
            # Fallback: use pacing
            pacing = it.get('pacing_morae_per_min') or 180.0
            total_morae = sum(count_morae(t) for _, t in lines)
            total_s = (total_morae / pacing) * 60.0

        # Mora-proportional distribution
        mora_counts = [count_morae(t) for _, t in lines]
        total_mora = sum(mora_counts) or 1
        cur = 0.0
        out_lines = []
        for (speaker, text), mc in zip(lines, mora_counts):
            dur = (mc / total_mora) * total_s
            out_lines.append({
                'speaker': speaker,
                'text': text,
                'mora_count': mc,
                'start_s': round(cur, 2),
                'end_s': round(cur + dur, 2),
            })
            cur += dur

        it['timestamped_transcript'] = {
            'estimated': True,
            'pacing_morae_per_min': it.get('pacing_morae_per_min') or 180,
            'total_seconds': round(total_s, 1),
            'lines': out_lines,
        }
        it['timestamped_transcript_provenance'] = 'auto_derived'
        n += 1

    print(f'Filled timestamped_transcript on {n}/{len(data["items"])} items.')
    print(f'  Skipped (no script_ja): {n_skip_no_script}')
    print(f'  Skipped (no line breakdown): {n_skip_short}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
