"""ISSUE-109: add pair_id cross-link on the 12 canonical N5
transitivity-pair verbs. Uses lemma OR reading lookup with gloss
hint to disambiguate.
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

# (transitive_lemma, transitive_reading, t_gloss_hint,
#  intransitive_lemma, intransitive_reading, i_gloss_hint, sense_label)
PAIRS = [
    ('開ける', 'あける', 'open', '開く', 'あく', 'open', 'open'),
    ('閉める', 'しめる', 'close', '閉まる', 'しまる', 'close', 'close'),
    ('入れる', 'いれる', 'put in', '入る', 'はいる', 'enter', 'enter/put-in'),
    ('出す', 'だす', 'put out', '出る', 'でる', 'go out', 'exit/put-out'),
    ('始める', 'はじめる', 'begin', '始まる', 'はじまる', 'begin', 'begin'),
    ('止める', 'とめる', 'stop', '止まる', 'とまる', 'stop', 'stop'),
    ('つける', 'つける', 'turn on', 'つく', 'つく', 'turn on', 'turn-on'),
    ('消す', 'けす', 'turn off', '消える', 'きえる', 'disappear', 'turn-off/disappear'),
    ('起こす', 'おこす', 'wake', '起きる', 'おきる', 'wake', 'wake'),
    ('落とす', 'おとす', 'drop', '落ちる', 'おちる', 'fall', 'drop/fall'),
    ('直す', 'なおす', 'fix', '直る', 'なおる', 'be fixed', 'fix'),
    ('切る', 'きる', 'cut', '切れる', 'きれる', 'cut', 'cut'),
]


vpath = ROOT / 'data' / 'vocab.json'
vdata = json.loads(vpath.read_text(encoding='utf-8'))
items = vdata['entries']

def find_entry(lemma_kanji, reading, gloss_hint, want_transitivity):
    """Find vocab entry matching by lemma (kanji or kana) + reading + transitivity."""
    candidates = []
    for e in items:
        ent_lemma = e.get('lemma') or e.get('form') or ''
        ent_reading = e.get('reading') or ''
        ent_trans = e.get('transitivity') or ''
        ent_gloss = (e.get('gloss') or '').lower()
        # match by either kanji lemma or kana lemma
        if (ent_lemma == lemma_kanji or ent_lemma == reading) and ent_reading == reading:
            score = 0
            if want_transitivity == ent_trans:
                score += 10
            if gloss_hint.lower() in ent_gloss:
                score += 5
            candidates.append((score, e))
    if not candidates:
        return None
    candidates.sort(key=lambda x: -x[0])
    return candidates[0][1]


linked = 0
unlinked_pairs = []
for (t_lemma, t_reading, t_hint,
     i_lemma, i_reading, i_hint, label) in PAIRS:
    t_entry = find_entry(t_lemma, t_reading, t_hint, 'transitive')
    i_entry = find_entry(i_lemma, i_reading, i_hint, 'intransitive')
    if not t_entry or not i_entry:
        unlinked_pairs.append((label, t_entry is not None, i_entry is not None))
        continue
    t_id = t_entry['id']
    i_id = i_entry['id']
    t_entry['pair_id'] = i_id
    i_entry['pair_id'] = t_id
    if not t_entry.get('transitivity'):
        t_entry['transitivity'] = 'transitive'
    if not i_entry.get('transitivity'):
        i_entry['transitivity'] = 'intransitive'
    linked += 1
    print(f'  ✓ {label}: {t_lemma} ({t_id}) <-> {i_lemma} ({i_id})')

vpath.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')

print(f'\nLinked {linked}/{len(PAIRS)} canonical pairs')
if unlinked_pairs:
    print('Unlinked (one or both halves missing):')
    for label, t_ok, i_ok in unlinked_pairs:
        print(f'  - {label}: transitive_found={t_ok} intransitive_found={i_ok}')
