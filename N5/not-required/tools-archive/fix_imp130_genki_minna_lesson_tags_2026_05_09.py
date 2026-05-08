"""IMP-130: surface structured `genki_lesson` and `minna_chapter`
fields on grammar patterns by parsing the existing `sources` array.

The audit complaint was that no pattern carried a structured tag.
In fact, most patterns already encode the lesson in `sources`
(e.g. "genki-1-l3", "minna-1-c8"). The fix is to expose this as a
first-class typed field so the UI can build a path-view ("you
finished Genki I L4? Here is your N5 progress.") without parsing
strings at runtime.

Design:
  - Parse "genki-{B}-l{L}" → {book: B, lesson: L}
  - Parse "minna-{B}-c{C}" → {book: B, chapter: C}
  - Primary intro = lowest (book, lesson) tuple. That's the lesson
    where the pattern is first introduced; subsequent lessons are
    reinforcement.
  - `genki_lessons_all` / `minna_chapters_all` preserve full list
    for cross-reference UIs.
  - Provenance: 'auto_extracted' (extracted from existing curated
    `sources` array; original sources untouched).

Patterns with no genki source: 16 (mostly Genki II coverage).
Patterns with no minna source: 3 (colloquial particles って/なあ/な).
For these, the structured field is omitted entirely (no lossy
default).
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

GENKI_RE = re.compile(r'^genki-(\d+)-l(\d+)$')
MINNA_RE = re.compile(r'^minna-(\d+)-c(\d+)$')


def parse_genki(srcs):
    """Return ([{book,lesson}, ...] sorted, primary={book,lesson} or None)."""
    out = []
    for s in srcs:
        m = GENKI_RE.match(str(s))
        if m:
            out.append({'book': int(m.group(1)), 'lesson': int(m.group(2))})
    out.sort(key=lambda d: (d['book'], d['lesson']))
    return out, (out[0] if out else None)


def parse_minna(srcs):
    """Return ([{book,chapter}, ...] sorted, primary={book,chapter} or None)."""
    out = []
    for s in srcs:
        m = MINNA_RE.match(str(s))
        if m:
            out.append({'book': int(m.group(1)), 'chapter': int(m.group(2))})
    out.sort(key=lambda d: (d['book'], d['chapter']))
    return out, (out[0] if out else None)


grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

genki_added = 0
minna_added = 0
genki_missing = []
minna_missing = []

for p in patterns:
    src = p.get('sources') or []

    g_all, g_primary = parse_genki(src)
    m_all, m_primary = parse_minna(src)

    if g_primary:
        p['genki_lesson'] = g_primary
        if len(g_all) > 1:
            p['genki_lessons_all'] = g_all
        p['genki_lesson_provenance'] = 'auto_extracted'
        genki_added += 1
    else:
        genki_missing.append((p['id'], p.get('pattern', '')))

    if m_primary:
        p['minna_chapter'] = m_primary
        if len(m_all) > 1:
            p['minna_chapters_all'] = m_all
        p['minna_chapter_provenance'] = 'auto_extracted'
        minna_added += 1
    else:
        minna_missing.append((p['id'], p.get('pattern', '')))

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Total patterns:                 {len(patterns)}')
print(f'genki_lesson structured added:  {genki_added}')
print(f'minna_chapter structured added: {minna_added}')
print()
print(f'No Genki source ({len(genki_missing)}):')
for pid, pat in genki_missing:
    print(f'  {pid:8} {pat}')
print()
print(f'No Minna source ({len(minna_missing)}):')
for pid, pat in minna_missing:
    print(f'  {pid:8} {pat}')
