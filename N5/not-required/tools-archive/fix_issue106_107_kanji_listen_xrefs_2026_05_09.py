"""ISSUE-106 + ISSUE-107: bidirectional cross-references.

ISSUE-106 — kanji.json: each kanji gains a `reading_passages` array
listing the passages that use it. The forward direction
(`reading.passages[*].kanji_used`) was already curated; this is
the reverse-index for "click a kanji → see passages that use it".

  reading_passages: [
    {passage_id, title_ja, level}
  ]

ISSUE-107 — listening.json: each item gains an inline
`vocab_glossary` array of N5 vocab forms detected in `script_ja`,
each with reading + gloss. Lets the listening UI surface a quick
glossary panel without making the user search vocab separately.

  vocab_glossary: [
    {form, reading, gloss, gloss_hi, vocab_id}
  ]

Both tasks are pure auto-derivation — no native review needed. Each
stamped with `*_provenance: 'auto_derived'`.
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

# ============================================================================
# ISSUE-106: kanji → reading_passages (reverse of passages.kanji_used)
# ============================================================================

reading_path = ROOT / 'data' / 'reading.json'
kanji_path = ROOT / 'data' / 'kanji.json'

rdata = json.loads(reading_path.read_text(encoding='utf-8'))
kdata = json.loads(kanji_path.read_text(encoding='utf-8'))

passages = rdata.get('passages') or rdata
kanji_entries = kdata.get('entries') or kdata
if isinstance(kanji_entries, dict):
    kanji_entries = list(kanji_entries.values())

# index kanji glyph → entry (handle either 'glyph' or first id-segment)
glyph_to_kanji = {}
for k in kanji_entries:
    g = k.get('glyph') or (k.get('id', '').split('.')[-1])
    if g:
        glyph_to_kanji[g] = k

# Build reverse index: glyph → list of {passage_id, title_ja, level}
glyph_to_passages: dict = {}
for p in passages:
    pid = p.get('id')
    title = p.get('title_ja', '')
    level = p.get('level', '')
    used = p.get('kanji_used') or []
    for g in used:
        if g in glyph_to_kanji:
            glyph_to_passages.setdefault(g, []).append({
                'passage_id': pid,
                'title_ja': title,
                'level': level,
            })

# Stamp on kanji entries
linked = 0
not_in_passages = []
for k in kanji_entries:
    g = k.get('glyph') or (k.get('id', '').split('.')[-1])
    refs = glyph_to_passages.get(g, [])
    if refs:
        k['reading_passages'] = refs
        k['reading_passages_provenance'] = 'auto_derived'
        linked += 1
    else:
        not_in_passages.append(g)

kanji_path.write_text(
    json.dumps(kdata, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print('===== ISSUE-106: kanji → reading_passages =====')
print(f'Total kanji:                       {len(kanji_entries)}')
print(f'  linked to >=1 passage:           {linked}')
print(f'  not used in any reading passage: {len(not_in_passages)}')
print(f'Coverage: {linked}/{len(kanji_entries)} ({100*linked/len(kanji_entries):.0f}%)')
print()

# ============================================================================
# ISSUE-107: listening.script_ja → vocab_glossary
# ============================================================================

vocab_path = ROOT / 'data' / 'vocab.json'
listen_path = ROOT / 'data' / 'listening.json'

vdata = json.loads(vocab_path.read_text(encoding='utf-8'))
ldata = json.loads(listen_path.read_text(encoding='utf-8'))

vocab_entries = vdata.get('entries') or vdata
listen_items = ldata.get('items') or ldata

# Build vocab index: form/reading/lemma -> entry, prioritizing kanji forms
# (longest first so we match 学生 before 学).
vocab_lookup = {}  # form_or_reading -> entry
all_forms = []
for v in vocab_entries:
    form = (v.get('form') or '').strip()
    reading = (v.get('reading') or '').strip()
    if form:
        vocab_lookup.setdefault(form, v)
        all_forms.append(form)
    if reading and reading != form:
        # only register reading-only when no kanji form has the same string
        vocab_lookup.setdefault(reading, v)
        all_forms.append(reading)

# Sort by length descending — longest match wins so we don't extract
# 何時 (4 chars combined) by stopping at 何 (1 char).
all_forms = sorted(set(all_forms), key=lambda s: -len(s))

# Match anywhere in script_ja: for a given script, scan and collect
# distinct vocab forms that appear. Skip 1-char particles and very
# common pronoun/copula glue (は, が, を, etc.) to keep glossary focused
# on content words.
SKIP_FORMS = {
    'は', 'が', 'を', 'に', 'へ', 'で', 'と', 'から', 'まで',
    'の', 'も', 'や', 'か', 'ね', 'よ', 'よね', 'ので', 'のに',
    'です', 'ます', 'でした', 'ました', 'ません', 'でしょう',
    'これ', 'それ', 'あれ', 'どれ', 'この', 'その', 'あの', 'どの',
    'ここ', 'そこ', 'あそこ', 'どこ',
    '私', 'わたし', '私たち', 'わたしたち', '僕', 'ぼく',
    'はい', 'いいえ', 'はじめまして',
}

linked = 0
total_ref = 0
for it in listen_items:
    script = it.get('script_ja') or ''
    if not script:
        continue
    seen = set()
    glossary = []
    for f in all_forms:
        if f in SKIP_FORMS:
            continue
        if len(f) < 2:  # skip 1-char particles / particles
            continue
        if f in script and f not in seen:
            seen.add(f)
            v = vocab_lookup[f]
            glossary.append({
                'form': v.get('form'),
                'reading': v.get('reading'),
                'gloss': v.get('gloss'),
                'gloss_hi': v.get('gloss_hi'),
                'vocab_id': v.get('id'),
            })
    if glossary:
        # Sort by first appearance in the script for natural reading order
        def first_pos(g):
            return script.find(g['form']) if g['form'] in script else (
                script.find(g['reading']) if g['reading'] else 999_999
            )
        glossary.sort(key=first_pos)
        it['vocab_glossary'] = glossary
        it['vocab_glossary_provenance'] = 'auto_derived'
        linked += 1
        total_ref += len(glossary)

listen_path.write_text(
    json.dumps(ldata, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print('===== ISSUE-107: listening → vocab_glossary =====')
print(f'Total listening items:             {len(listen_items)}')
print(f'  with vocab_glossary populated:   {linked}')
print(f'Total vocab refs added:            {total_ref}')
print(f'Avg glossary size:                 {total_ref/max(1,linked):.1f} entries/item')
