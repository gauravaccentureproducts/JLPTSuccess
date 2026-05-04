"""Refresh `skipped` flag on every audio_manifest.json entry to reflect
whether the MP3 actually exists on disk now.

Closes infra-audit §2.2 (HIGH) — at audit time 688/708 items were
flagged `skipped: true` because their MP3s weren't rendered yet. Since
then the gTTS render pass produced all 708 MP3s (verified by the
orphan-audio cleanup tool: 708 files on disk == 708 manifest entries,
0 missing). The `skipped` flags were never refreshed.

The runtime doesn't consume `skipped` (grep'd `js/`: zero readers), so
this is metadata hygiene rather than a UX fix. But §2.2 was filed at
HIGH severity precisely because the metadata was misleading; clearing
it closes the audit item cleanly and prevents future tooling that
might consume the flag from being misled.

Idempotent: re-derives existence-on-disk every run.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'data' / 'audio_manifest.json'


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    items = data['items'] if isinstance(data, dict) and 'items' in data else data
    flipped_to_false = 0
    flipped_to_true = 0
    unchanged = 0
    for it in items:
        path = it.get('path') or it.get('audio') or ''
        if not path:
            continue
        full = ROOT / path.lstrip('/').replace('\\', '/')
        exists = full.is_file()
        prev = it.get('skipped')
        new = not exists
        if prev != new:
            it['skipped'] = new
            if new:
                flipped_to_true += 1
            else:
                flipped_to_false += 1
        else:
            unchanged += 1
    if flipped_to_false or flipped_to_true:
        MANIFEST.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Manifest entries: {len(items)}')
    print(f'  flipped skipped: true → false (file now exists): {flipped_to_false}')
    print(f'  flipped skipped: false → true (file now missing): {flipped_to_true}')
    print(f'  unchanged:                                       {unchanged}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
