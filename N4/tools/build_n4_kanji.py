"""Build N4 kanji whitelist + readings + KB markdown from inventory + N5 source.

Reads:
  - <repo>/n4-kanji-inventory.md (167 N4-new kanji)
  - <JLPT-root>/N5/data/n5_kanji_whitelist.json (106 N5 prerequisite kanji)
  - <JLPT-root>/N5/data/n5_kanji_readings.json (N5 kanji on/kun/primary)

Writes:
  - data/n4_kanji_whitelist.json: array of 273 glyphs sorted lesson_order
  - data/n4_kanji_readings.json: per-glyph readings + primary
  - KnowledgeBank/kanji_n4.md: full catalogue (skeleton with N5 + parsed N4)
  - data/kanji.json: runtime data with all 273 entries

Idempotent.
"""
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
N5 = ROOT.parent / 'N5'

# 1. Load N5 prerequisite kanji
n5_whitelist = json.loads((N5 / 'data' / 'n5_kanji_whitelist.json').read_text(encoding='utf-8'))
n5_readings = json.loads((N5 / 'data' / 'n5_kanji_readings.json').read_text(encoding='utf-8'))
print(f'[1] N5 prerequisite kanji loaded: {len(n5_whitelist)} glyphs')

# 2. Parse N4 inventory
inv_text = (ROOT / 'n4-kanji-inventory.md').read_text(encoding='utf-8')
n4_pattern = re.compile(r'^([一-鿿]) \| ([^|]*?) \| ([^|]*?) \| (.+)$', re.MULTILINE)
n4_entries = []
seen = set()
for m in n4_pattern.finditer(inv_text):
    glyph = m.group(1)
    if glyph in seen or glyph in n5_whitelist:
        continue
    seen.add(glyph)
    on_raw = m.group(2).strip()
    kun_raw = m.group(3).strip()
    meaning = m.group(4).strip()
    # Parse on-list (katakana, comma- or 、-separated, can be "—" for none)
    on = []
    if on_raw and on_raw not in ('—', '-'):
        on = [s.strip() for s in re.split(r'[、,]', on_raw) if s.strip()]
    # Parse kun-list (hiragana with okurigana in parens)
    kun = []
    if kun_raw and kun_raw not in ('—', '-'):
        kun = [s.strip() for s in re.split(r'[、,]', kun_raw) if s.strip()]
    n4_entries.append({
        'glyph': glyph, 'on': on, 'kun': kun, 'meanings': [meaning]
    })

print(f'[2] N4 new kanji parsed: {len(n4_entries)} glyphs')

# 3. Build combined whitelist (N5 prerequisite + N4 new)
combined_whitelist = list(n5_whitelist) + [e['glyph'] for e in n4_entries]
print(f'[3] Combined whitelist: {len(combined_whitelist)} glyphs')

# 4. Build readings dict
combined_readings = {}
for g in n5_whitelist:
    if g in n5_readings:
        combined_readings[g] = dict(n5_readings[g])  # shallow copy
        combined_readings[g]['tier'] = 'n5_prerequisite'

for entry in n4_entries:
    g = entry['glyph']
    on, kun = entry['on'], entry['kun']
    # Primary: prefer kun for i-adjective hints (kun ending in (い)), else first on
    primary = on[0] if on else (kun[0] if kun else '')
    primary_kind = 'on' if (on and primary in on) else 'kun'
    # If kun ends in adjective marker (い)/(しい), prefer kun
    if kun and any('(い)' in k or '(しい)' in k for k in kun):
        primary = kun[0]
        primary_kind = 'kun'
    combined_readings[g] = {
        'on': on,
        'kun': kun,
        'primary': primary,
        'primary_kind': primary_kind,
        'tier': 'core_n4',
    }

# 5. Write whitelist + readings
(ROOT / 'data' / 'n4_kanji_whitelist.json').write_text(
    json.dumps(combined_whitelist, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(ROOT / 'data' / 'n4_kanji_readings.json').write_text(
    json.dumps(combined_readings, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'[4-5] data/n4_kanji_whitelist.json + data/n4_kanji_readings.json written')

# 6. Build data/kanji.json — N4-NEW ONLY (per user directive 2026-05-04:
# "make sure N5 content is not repeated in N4"). Whitelist still includes
# N5 kanji (so N4 content can use N5 kanji in compounds), but the
# CATALOGUE only teaches the 143 N4-new glyphs. N5 review lives in the
# sibling app.
n4_new_glyphs = [e['glyph'] for e in n4_entries]  # only N4-new
kanji_entries = []
for i, g in enumerate(n4_new_glyphs):
    r = combined_readings.get(g, {})
    entry = {
        'id': f'n4.kanji.{g}',
        'glyph': g,
        'tier': 'core_n4',
        'n5_prerequisite': False,
        'lesson_order': i + 1,
        'frequency_rank': i + 1,  # placeholder; refine in Pass-3
        'on': r.get('on', []),
        'kun': r.get('kun', []),
        'primary_reading': r.get('primary', ''),
        'primary_kind': r.get('primary_kind', 'on'),
        'meanings': [],  # filled below for N4
        'stroke_order_svg': f'svg/kanji/{g}.svg',
        'recognition_priority': 1 if i < 30 else (3 if i >= 130 else 2),
        'examples': [],  # Pass-3 authoring
        'notes': '',
    }
    kanji_entries.append(entry)

# Backfill meanings for N4 entries from inventory
n4_meaning_map = {e['glyph']: e['meanings'][0] for e in n4_entries}
for entry in kanji_entries:
    if entry['glyph'] in n4_meaning_map:
        m = n4_meaning_map[entry['glyph']]
        entry['meanings'] = [s.strip() for s in re.split(r'[;,]', m) if s.strip()][:5]

kanji_payload = {
    '_meta': {
        'schema_version': 1,
        'entity_count': len(kanji_entries),
        'id_range': 'n4.kanji.<glyph>',
        'id_gap_policy': 'ID is the literal glyph; never gappy.',
        'history': [
            {'date': '2026-05-04',
             'delta': f'+{len(kanji_entries)} N4-new kanji (N5 prereqs not repeated; whitelist union retained for content scope)'}
        ],
    },
    'entries': kanji_entries,
}
(ROOT / 'data' / 'kanji.json').write_text(
    json.dumps(kanji_payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'[6] data/kanji.json written ({len(kanji_entries)} N4-new entries)')

# 7. Build KnowledgeBank/kanji_n4.md
md = ['# JLPT N4 Kanji', '',
      'Source-of-truth catalogue for N4-new kanji only.',
      f'Whitelist = N5 ∪ N4 = {len(combined_whitelist)} glyphs (kept as a UNION so N4 content can use N5 kanji in compounds).',
      f'Catalogue (this file) = N4 only = {len(n4_entries)} glyphs. N5 review lives in the sibling app.',
      'Build pipeline parses into `data/kanji.json`. Schema per spec §14.',
      '',
      '## N5 prerequisites',
      '',
      'N5 kanji are NOT taught in this app. Review them via the N5 sibling app at',
      'https://gauravaccentureproducts.github.io/jlpt-n5-tutor/.',
      '',
      f'## N4 kanji ({len(n4_entries)})',
      '']
for e in n4_entries:
    g = e['glyph']
    r = combined_readings[g]
    on_str = '、'.join(r.get('on', []))
    kun_str = '、'.join(r.get('kun', []))
    meaning = e['meanings'][0] if e['meanings'] else '(meaning TBD)'
    # JA-12 expects format: `- **{kanji}** ...`
    md.append(f'- **{g}**  (tier: core_n4)')
    md.append(f'  - on: {on_str if on_str else "(none)"}')
    md.append(f'  - kun: {kun_str if kun_str else "(none)"}')
    md.append(f'  - primary: {r.get("primary", "")}  (kind: {r.get("primary_kind", "on")})')
    md.append(f'  - meanings: {meaning}')
    md.append('')

(ROOT / 'KnowledgeBank' / 'kanji_n4.md').write_text(
    '\n'.join(md) + '\n', encoding='utf-8')
print(f'[7] KnowledgeBank/kanji_n4.md written ({len(n4_entries)} N4-new entries; N5 prereqs not included)')

print('\nDone. Run python tools/check_content_integrity.py to verify.')
