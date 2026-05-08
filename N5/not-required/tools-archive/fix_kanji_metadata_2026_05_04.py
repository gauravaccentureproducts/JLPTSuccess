"""IMP-003 / IMP-015: enrich data/kanji.json with stroke_count + additional_readings.

Stroke counts derive from the bundled KanjiVG SVGs by counting per-stroke
<path id="kvg:XXXXX-sN" ...> entries. Idempotent.

For IMP-015, only 私 (taught only as わたし at N5; on-yomi シ exists in real
exposure) gets a populated `additional_readings` field. The other 14
"missing kun-yomi" kanji legitimately have no common kun-yomi in modern
Japanese; pruning is correct, no enrichment needed.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KANJI_JSON = ROOT / 'data' / 'kanji.json'
SVG_DIR = ROOT / 'svg' / 'kanji'

# Per IMP-015: kanji where adding ON-yomi to additional_readings is
# pedagogically defensible (i.e., the reading is in real-world N5 exposure
# but the project chose to teach the kun-yomi only).
ADDITIONAL_READINGS = {
    '私': {'on': ['シ']},
    # 'X': {'on': [...], 'kun': [...]}  -- add more here if future audits identify them
}


PATH_RE = re.compile(r'<path\s+id="kvg:[^"]+-s(\d+)"')


def stroke_count_for(glyph: str) -> int | None:
    f = SVG_DIR / f'{glyph}.svg'
    if not f.exists():
        return None
    text = f.read_text(encoding='utf-8')
    nums = [int(m.group(1)) for m in PATH_RE.finditer(text)]
    return max(nums) if nums else None


def main() -> int:
    data = json.loads(KANJI_JSON.read_text(encoding='utf-8'))
    entries = data['entries']
    changes = []
    for e in entries:
        glyph = e.get('glyph')
        if not glyph:
            continue
        # IMP-003: stroke_count
        sc = stroke_count_for(glyph)
        if sc is not None and e.get('stroke_count') != sc:
            e['stroke_count'] = sc
            changes.append(f'  {glyph}: stroke_count={sc}')
        # IMP-015: additional_readings
        if glyph in ADDITIONAL_READINGS:
            target = ADDITIONAL_READINGS[glyph]
            if e.get('additional_readings') != target:
                e['additional_readings'] = target
                changes.append(f'  {glyph}: additional_readings={target}')

    if not changes:
        print('No changes (already enriched).')
        return 0

    KANJI_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'{len(changes)} fields set:')
    for c in changes[:20]:
        print(c)
    if len(changes) > 20:
        print(f'  ... +{len(changes) - 20} more')
    return 0


if __name__ == '__main__':
    sys.exit(main())
