"""ISSUE-016 (audit round-3): tag every listening item with mondai (1-4)
and a closed format_type enum so the UI can surface the official JLPT
N5 listening sections (もんだい1 課題理解 / もんだい2 ポイント理解 /
もんだい3 発話表現 / もんだい4 即時応答).

Mapping derived from the existing free-form `format` field + choice
count. The official spec is:
  もんだい1 課題理解        → 4-choice
  もんだい2 ポイント理解    → 4-choice
  もんだい3 発話表現        → 3-choice
  もんだい4 即時応答        → 3-choice

The current corpus uses three free-form values: task / point / utterance.
- task      → mondai 1, format_type "task_understanding"
- point     → mondai 2, format_type "point_understanding"
- utterance → mondai 3, format_type "utterance_expression"
              (irrespective of choice count - the 4-choice variants in
              this corpus are non-canonical but utterance-style; no
              mondai 4 items exist as of v1.12.29)

Idempotent: items already carrying mondai + format_type are skipped.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
LIS = ROOT / 'data' / 'listening.json'

FORMAT_MAP = {
    'task':      (1, 'task_understanding'),
    'point':     (2, 'point_understanding'),
    'utterance': (3, 'utterance_expression'),
    # 'response': (4, 'immediate_response'),  # reserved if/when added
}


def main() -> int:
    d = json.loads(LIS.read_text(encoding='utf-8'))
    items = d.get('items', [])
    n_added = 0
    n_skipped = 0
    for it in items:
        if 'mondai' in it and 'format_type' in it:
            n_skipped += 1
            continue
        fmt = it.get('format', '')
        if fmt not in FORMAT_MAP:
            print(f'WARN: unknown format {fmt!r} on {it.get("id")}; leaving untagged')
            continue
        mondai, ftype = FORMAT_MAP[fmt]
        # Insert ordered: mondai right after id, format_type right after format,
        # so the JSON diff is minimal and the schema reads naturally.
        new = {}
        for k, v in it.items():
            new[k] = v
            if k == 'id' and 'mondai' not in new:
                new['mondai'] = mondai
            if k == 'format' and 'format_type' not in new:
                new['format_type'] = ftype
        # Replace in-place so .clear() preserves dict identity inside list.
        it.clear()
        it.update(new)
        n_added += 1

    LIS.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Tagged {n_added} item(s); {n_skipped} already tagged.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
