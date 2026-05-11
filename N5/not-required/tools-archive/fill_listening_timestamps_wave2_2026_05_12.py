"""Wave 2 — single-utterance timestamps for the 20 utterance_expression
+ immediate_response items.

Wave 1 (2026-05-11) timestamped 30/50 multi-line dialog items. The
20 remaining have script_ja that's just context-in-parentheses or
a brief situation; the actual SPEECH is the correctAnswer (and for
immediate_response, the prompt-script line + correctAnswer pair).

This wave authors a minimal timestamp:
  - utterance_expression: 1 line wrapping correctAnswer
  - immediate_response:   2 lines (script setup + correctAnswer)

Same mora-proportional distribution as wave 1.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def count_morae(text: str) -> int:
    small = set('ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶー')
    n = 0
    for ch in text:
        if ch in small:
            continue
        cp = ord(ch)
        if 0x3041 <= cp <= 0x3096 or 0x30A1 <= cp <= 0x30FA:
            n += 1
        elif 0x4E00 <= cp <= 0x9FFF:
            n += 2
    return n


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_timestamps_wave2')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    n = 0
    for it in data['items']:
        if it.get('timestamped_transcript'):
            continue
        ftype = it.get('format_type', '')
        correct = it.get('correctAnswer') or ''
        script = it.get('script_ja') or ''
        # Build line list
        lines_raw = []
        if ftype == 'immediate_response':
            # script_ja is the cue / prompt-utterance from a partner; correctAnswer is the response
            if script.strip():
                lines_raw.append(('partner', script.strip()))
            if correct.strip():
                lines_raw.append(('response', correct.strip()))
        else:
            # utterance_expression — script is context (in parens); correctAnswer is what the learner should say
            if correct.strip():
                lines_raw.append(('speaker', correct.strip()))
            else:
                # fallback: use the script body
                if script.strip():
                    lines_raw.append(('speaker', script.strip()))

        if not lines_raw:
            continue

        pacing = it.get('pacing_morae_per_min') or 180
        total_morae = sum(count_morae(t) for _, t in lines_raw) or 1
        total_s = (total_morae / pacing) * 60.0

        cur = 0.0
        out_lines = []
        for spk, txt in lines_raw:
            mc = count_morae(txt)
            dur = (mc / total_morae) * total_s
            out_lines.append({
                'speaker': spk,
                'text': txt,
                'mora_count': mc,
                'start_s': round(cur, 2),
                'end_s': round(cur + dur, 2),
            })
            cur += dur

        it['timestamped_transcript'] = {
            'estimated': True,
            'single_utterance': len(lines_raw) <= 1,
            'pacing_morae_per_min': pacing,
            'total_seconds': round(total_s, 1),
            'lines': out_lines,
        }
        it['timestamped_transcript_provenance'] = 'auto_derived'
        n += 1

    print(f'\nWave 2 added timestamped_transcript on {n} more items.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
