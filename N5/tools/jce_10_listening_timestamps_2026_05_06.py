"""JCE-10: Add timestamped `lines` to remaining 7 listening items
(mondai-4 immediate-response items).

Coverage before: 40/47 listening items had timestamped lines (built by
prior round-7 batch-H). The 7 remaining are mondai-4 (即時応答 /
immediate response) — single-line stimuli where the script is one short
utterance played once. For those, a single line entry at startMs=0
is the natural answer.

Schema: lines is a list of {text_ja, startMs} dicts.

Idempotent: skips items that already have lines populated.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / 'data' / 'listening.json'


def main():
    with LISTENING.open('r', encoding='utf-8') as f:
        data = json.load(f)

    items = data['items']
    matched = 0
    skipped = 0
    for it in items:
        if it.get('lines'):
            skipped += 1
            continue
        script = it.get('script_ja') or it.get('script') or ''
        if not script:
            print(f'  WARN: {it.get("id")} has no script_ja; skipping')
            continue
        # mondai-4 items are single-line; for safety, split on newlines
        # in case any non-mondai-4 item gets here without lines
        lines_text = [s for s in script.split('\n') if s.strip()]
        # Estimate timing: assume 200 morae/min = 3.33 morae/sec
        # so one mora = 300 ms. Approximate kana-count -> ms duration.
        cumulative_ms = 0
        lines = []
        for line in lines_text:
            kana_count = len(line)  # rough proxy for morae
            line_dur_ms = max(1500, int(kana_count * 300))
            lines.append({'text_ja': line, 'startMs': cumulative_ms})
            cumulative_ms += line_dur_ms + 500  # 500ms inter-line pause
        it['lines'] = lines
        matched += 1

    print(f'Authored timestamped lines on {matched} items.')
    print(f'Skipped (already had lines): {skipped}')

    with LISTENING.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote: {LISTENING}')


if __name__ == '__main__':
    main()
