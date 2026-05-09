"""IMP-125: extend each kanji.json entry's `mnemonic` from a flat
string to a structured 3-mnemonic record (visual + reading +
meaning) per the WaniKani-style mental-imagery convention.

Schema (v2):
  mnemonic: {
    summary:  <original flat string — preserved verbatim>,
    visual:   <visual mnemonic auto-derived from radical_decomposition>,
    reading:  <reading mnemonic auto-derived from on/kun readings>,
    meaning:  <meaning mnemonic — same as summary, since the existing
              flat strings describe meaning>,
    provenance: {
      summary: 'native_reviewed',
      visual:  'auto_derived',     <-- needs native review for quality
      reading: 'auto_derived',     <-- needs native review for quality
      meaning: 'native_reviewed',
    },
  }

The legacy flat string stays the source of truth; the new sub-fields
scaffold the WaniKani 3-mnemonic UX. Native review can refine the
auto_derived fields over follow-up passes; the JA-* invariants stay
green throughout.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

kanji_path = ROOT / 'data' / 'kanji.json'
data = json.loads(kanji_path.read_text(encoding='utf-8'))
entries = data.get('entries', data) if isinstance(data, dict) else data
if isinstance(entries, dict):
    entries_list = list(entries.values())
else:
    entries_list = entries


def derive_visual(entry: dict) -> str:
    """Construct a visual-mnemonic stub from radical decomposition."""
    glyph = entry.get('glyph') or '?'
    radicals = entry.get('radical_decomposition') or []
    radical = entry.get('radical')

    if radicals and isinstance(radicals, list):
        comps = [r.get('glyph') if isinstance(r, dict) else r for r in radicals]
        comps = [c for c in comps if c]
        if comps:
            return (
                f"Picture {glyph} as a combination of "
                + ' + '.join(comps)
                + (' — visualise these components stacked / placed as in the glyph.'
                   if len(comps) >= 2 else '.')
            )
    if radical:
        return f"Picture {glyph} built around the {radical} radical."
    return f"Picture the shape of {glyph} as a memorable scene; rehearse the glyph 5 times by hand."


def derive_reading(entry: dict) -> str:
    """Construct a reading-mnemonic stub from on/kun readings."""
    on = entry.get('on') or []
    kun = entry.get('kun') or []
    primary = entry.get('primary_reading')

    parts = []
    if on:
        parts.append(f"On-reading: {' / '.join(on[:3])}")
    if kun:
        parts.append(f"Kun-reading: {' / '.join(kun[:3])}")
    if primary:
        parts.append(f"Primary in N5 vocab: {primary}")

    if not parts:
        return ''

    return (
        ' · '.join(parts)
        + ' — chain each reading to a familiar word: e.g., on-reading often appears'
          ' in compound nouns, kun-reading in standalone usage. Rehearse 3 vocab examples.'
    )


updated = 0
preserved = 0
for e in entries_list:
    existing = e.get('mnemonic')
    if isinstance(existing, dict) and 'summary' in existing:
        # Already 3-mnemonic shape; leave alone
        preserved += 1
        continue

    summary = existing if isinstance(existing, str) else ''
    visual = derive_visual(e)
    reading = derive_reading(e)
    meaning = summary  # legacy field describes meaning

    e['mnemonic'] = {
        'summary': summary,
        'visual': visual,
        'reading': reading,
        'meaning': meaning,
        'provenance': {
            'summary': 'native_reviewed' if summary else 'auto_derived',
            'visual': 'auto_derived',
            'reading': 'auto_derived',
            'meaning': 'native_reviewed' if summary else 'auto_derived',
        },
    }
    updated += 1

kanji_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Total kanji entries:                {len(entries_list)}')
print(f'  upgraded to 3-mnemonic shape:     {updated}')
print(f'  already 3-mnemonic (preserved):   {preserved}')
print()
print('Schema v2: mnemonic = {summary, visual, reading, meaning, provenance}')
print('summary + meaning preserve the existing flat string verbatim.')
print('visual + reading are auto_derived stubs — flag native review next pass.')
