"""ISSUE-108: backfill grammarPatternId on paper questions where
the question stem matches a known grammar pattern.

Strategy: for each paper question, look up its kbSourceId in
data/questions.json (which maps Q-IDs to grammarPatternId).
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

# Build kbSourceId → grammarPatternId from questions.json
qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
qmap = {}
for q in qs.get('questions', []):
    kb = q.get('kbSourceId') or q.get('kb_source_id')
    pid = q.get('grammarPatternId') or q.get('grammar_pattern_id')
    if kb and pid:
        qmap[kb] = pid

# Also build by question_ja stem (for paper-bound questions that don't share kbSourceId)
stem_map = {}
for q in qs.get('questions', []):
    stem = q.get('question_ja') or q.get('stem_ja') or ''
    pid = q.get('grammarPatternId') or q.get('grammar_pattern_id')
    if stem and pid:
        stem_map[stem.strip()] = pid

print(f'kbSourceId → grammarPatternId mappings: {len(qmap)}')
print(f'stem → grammarPatternId mappings: {len(stem_map)}')

# Process paper files
paper_dir = ROOT / 'data' / 'papers'
total_q = 0
linked_via_kb = 0
linked_via_stem = 0
already_linked = 0
unlinked = 0
files_changed = 0

for pf in paper_dir.rglob('*.json'):
    if pf.name == 'manifest.json':
        continue
    pdata = json.loads(pf.read_text(encoding='utf-8'))
    changed = False
    for q in pdata.get('questions', []):
        total_q += 1
        if q.get('grammarPatternId') or q.get('grammar_pattern_id'):
            already_linked += 1
            continue
        kb = q.get('kbSourceId') or q.get('kb_source_id')
        if kb and kb in qmap:
            q['grammarPatternId'] = qmap[kb]
            linked_via_kb += 1
            changed = True
            continue
        stem = q.get('question_ja') or q.get('stem_ja') or q.get('stem_html', '')
        # Strip HTML tags for stem match
        import re
        stem_clean = re.sub(r'<[^>]+>', '', stem).strip()
        if stem_clean and stem_clean in stem_map:
            q['grammarPatternId'] = stem_map[stem_clean]
            linked_via_stem += 1
            changed = True
            continue
        unlinked += 1
    if changed:
        pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n',
                      encoding='utf-8')
        files_changed += 1

print(f'\nTotal paper questions:    {total_q}')
print(f'Already linked:            {already_linked}')
print(f'Newly linked via kbSourceId: {linked_via_kb}')
print(f'Newly linked via stem:     {linked_via_stem}')
print(f'Unlinked (no match):       {unlinked}')
print(f'Files modified:            {files_changed}')
print(f'\nFinal coverage: {already_linked + linked_via_kb + linked_via_stem}/{total_q} ({100*(already_linked+linked_via_kb+linked_via_stem)/max(1,total_q):.0f}%)')
