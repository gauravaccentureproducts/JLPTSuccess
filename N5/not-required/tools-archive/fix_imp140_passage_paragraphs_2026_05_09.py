"""IMP-140 (partial): segment each reading passage into paragraphs
and add structural scaffolding for the literal/natural translation
pair the audit asked for.

The audit's full ask was paragraph-level summaries + literal/
natural English translation toggles. We split that into TWO
deliveries:

  THIS PASS (mechanical, scriptable):
    - paragraphs: list of {idx, text_ja, kanji_used, mora}
      derived deterministically by splitting on 。/blank-line.
    - translation_literal / translation_natural: STUB fields with
      `_provenance: 'needs_native_review'` so the schema is in
      place and the UI can light up the toggle UI even before
      content is authored.

  FOLLOW-UP PASS (HUMAN AUTHORING):
    - per-paragraph English summaries
    - the literal + natural translations themselves

This is honest: the structural work is done now; the content
authoring is queued for native-review. The UI gracefully shows
"translation pending native review" until then.
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

SMALL_MERGE = set('ゃゅょぁぃぅぇぉャュョァィゥェォ')


def count_mora_loose(text: str) -> int:
    """Mora count over kana+kanji (kanji counted as 1 mora — coarse)."""
    return sum(
        1 for c in text
        if c not in SMALL_MERGE
        and (
            '぀' <= c <= 'ゟ'
            or '゠' <= c <= 'ヿ'
            or '一' <= c <= '鿿'
        )
    )


def split_paragraphs(ja: str) -> list[str]:
    """Split passage Japanese text into paragraphs.

    Rules (in priority order):
      1. Blank-line separation (\\n\\n) is the strongest signal.
      2. If no blank lines, fall back to line-break (\\n).
      3. Single-paragraph passages stay as one entry.
    """
    if not ja:
        return []
    # Normalise line endings
    text = ja.replace('\r\n', '\n').strip()
    if not text:
        return []
    # Try blank-line split first
    parts = re.split(r'\n\s*\n', text)
    if len(parts) > 1:
        return [p.strip() for p in parts if p.strip()]
    # Fall back: every newline becomes a paragraph (looser)
    parts = [p.strip() for p in text.split('\n') if p.strip()]
    return parts if parts else [text]


def kanji_in(text: str) -> list[str]:
    """Distinct kanji glyphs in order of first appearance."""
    seen = []
    for c in text:
        if '一' <= c <= '鿿' and c not in seen:
            seen.append(c)
    return seen


reading_path = ROOT / 'data' / 'reading.json'
data = json.loads(reading_path.read_text(encoding='utf-8'))
passages = data['passages']

paragraphs_added = 0
stubs_added = 0
multi_para = 0
single_para = 0

for p in passages:
    ja = p.get('ja') or ''
    paras = split_paragraphs(ja)

    paragraphs_array = [
        {
            'idx': i,
            'text_ja': para,
            'kanji_used': kanji_in(para),
            'mora_approx': count_mora_loose(para),
        }
        for i, para in enumerate(paras)
    ]
    if not p.get('paragraphs'):
        p['paragraphs'] = paragraphs_array
        p['paragraphs_provenance'] = 'auto_segmented'
        paragraphs_added += 1
    if len(paras) > 1:
        multi_para += 1
    else:
        single_para += 1

    # Translation stubs (do NOT overwrite if already populated)
    if 'translation_literal' not in p:
        p['translation_literal'] = ''
        p['translation_literal_provenance'] = 'needs_native_review'
        stubs_added += 1
    if 'translation_natural' not in p:
        p['translation_natural'] = ''
        p['translation_natural_provenance'] = 'needs_native_review'

reading_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Total passages:                  {len(passages)}')
print(f'  paragraphs[] populated:        {paragraphs_added}')
print(f'    multi-paragraph:             {multi_para}')
print(f'    single-paragraph:            {single_para}')
print(f'  translation stubs added:       {stubs_added}')
print()
print('Translation content remains pending native review;')
print('the schema + UI affordance are now in place.')
