"""ISSUE-030 (audit round-4): scaffold review_status / provenance tags
on every content item across the 5 corpora.

Default tag for the whole corpus today is `llm_curated` — most content
was authored by Claude/GPT-style assistants with author review, then
audited by the 41/43 content-integrity invariants. Any item that has
explicitly been native-reviewed (by a Japanese speaker) can be
upgraded to `native_reviewed` in a follow-up pass.

Schema:
  review_status: "native_reviewed" | "llm_curated" | "auto_generated"
  reviewed_by:   string (optional — name / handle of native reviewer)
  reviewed_at:   ISO timestamp (optional)

This pass writes `review_status: "llm_curated"` on every item that
doesn't already carry the field. Idempotent.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'

DEFAULT_STATUS = 'llm_curated'

# (file, top-level-key, item-shape — describes how to walk)
TARGETS = [
    ('grammar.json',   'patterns'),
    ('vocab.json',     'entries'),
    ('kanji.json',     'entries'),
    ('reading.json',   'passages'),
    ('listening.json', 'items'),
]


def main() -> int:
    total_items = 0
    total_added = 0
    for fname, key in TARGETS:
        p = DATA / fname
        d = json.loads(p.read_text(encoding='utf-8'))
        items = d.get(key, [])
        added = 0
        for it in items:
            total_items += 1
            if 'review_status' in it:
                continue
            it['review_status'] = DEFAULT_STATUS
            added += 1
            total_added += 1
        if added:
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'  {fname:<20} {len(items):>4} items, {added:>4} tagged')

    print(f'\nTotal: {total_added}/{total_items} items got review_status="{DEFAULT_STATUS}".')
    print('Upgrade individual items to "native_reviewed" via a follow-up pass once a native')
    print('reviewer signs off. The schema also supports `reviewed_by` and `reviewed_at`.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
