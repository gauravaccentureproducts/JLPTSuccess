"""ISSUE-105: populate lookalikes array on every kanji that's part
of a confusable cluster, with all OTHER cluster members."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CLUSTERS = [
    ('the dot moves', ['大', '犬', '太']),
    ('line position', ['木', '本', '末', '未']),
    ('radical similarity', ['人', '入', '八']),
    ('rectangle variations', ['日', '目', '白']),
    ('vertical bar', ['千', '干', '王', '玉']),
    ('cross-bar position', ['上', '止', '正']),
    ('stroke count', ['古', '占']),
    ('top stroke direction', ['千', '午']),
]

kpath = ROOT / 'data' / 'kanji.json'
kdata = json.loads(kpath.read_text(encoding='utf-8'))
entries = kdata['entries']

# Build kanji glyph → entry map (use 'glyph' field, fallback to id)
by_glyph = {}
for e in entries:
    glyph = e.get('glyph') or e.get('char') or e.get('id', '').split('.')[-1]
    by_glyph[glyph] = e

# Multi-cluster aware: a kanji can be in multiple clusters (千 is in two)
# Record ALL cluster members even if some are out of N5 scope - that's
# pedagogically valuable (the UI can warn about N4-confusables).
lookalikes_in_scope = {}    # glyph -> set of N5-corpus look-alikes
lookalike_clusters = {}     # glyph -> list of {note, members (full), in_scope_members}

for note, members in CLUSTERS:
    in_scope = [m for m in members if m in by_glyph]
    for m in members:
        if m not in by_glyph:
            continue  # out-of-scope members can't be edited
        # Cluster members other than self
        siblings_in_scope = [x for x in in_scope if x != m]
        siblings_all = [x for x in members if x != m]
        lookalikes_in_scope.setdefault(m, set()).update(siblings_in_scope)
        lookalike_clusters.setdefault(m, []).append({
            'note': note,
            'members': siblings_all,
            'in_corpus': siblings_in_scope,
            'out_of_corpus': [x for x in siblings_all if x not in by_glyph],
        })

linked = 0
for glyph, look_set in lookalikes_in_scope.items():
    e = by_glyph[glyph]
    e['lookalikes'] = sorted(look_set)
    e['lookalike_clusters'] = lookalike_clusters[glyph]
    linked += 1
    inscope = sorted(look_set)
    all_targets = sum((c['members'] for c in lookalike_clusters[glyph]), [])
    out = [x for x in all_targets if x not in by_glyph]
    print(f'  ✓ {glyph}: in-scope={inscope}  also-warn={out}')

kpath.write_text(json.dumps(kdata, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')
print(f'\nLinked {linked} kanji across {len(CLUSTERS)} confusable clusters')
