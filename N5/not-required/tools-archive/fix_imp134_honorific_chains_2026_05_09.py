"""IMP-134: bidirectionally cross-link the 5 canonical N5 honorific
register chains (basic / respectful / humble)."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Each chain: list of (form, reading, gloss_hint, register)
CHAINS = [
    # exist (animate)
    ('exist (animate)', [
        ('いる',          'いる',         'exist',     'neutral'),
        ('いらっしゃる',  'いらっしゃる', 'exist',     'respectful'),
        ('おる',          'おる',         'exist',     'humble'),
    ]),
    # eat
    ('eat', [
        ('食べる',         'たべる',         'eat',     'neutral'),
        ('召し上がる',     'めしあがる',     'eat',     'respectful'),
        ('いただく',       'いただく',       'eat',     'humble'),
    ]),
    # see
    ('see', [
        ('見る',           'みる',           'see',     'neutral'),
        ('ご覧になる',     'ごらんになる',   'see',     'respectful'),
        ('拝見する',       'はいけんする',   'see',     'humble'),
    ]),
    # say
    ('say', [
        ('言う',           'いう',           'say',     'neutral'),
        ('おっしゃる',     'おっしゃる',     'say',     'respectful'),
        ('申す',           'もうす',         'say',     'humble'),
    ]),
    # go / come
    ('go/come', [
        ('行く',           'いく',           'go',      'neutral'),
        ('来る',           'くる',           'come',    'neutral'),
        ('いらっしゃる',   'いらっしゃる',   'go/come', 'respectful'),
        ('参る',           'まいる',         'go/come', 'humble'),
    ]),
]


vpath = ROOT / 'data' / 'vocab.json'
vdata = json.loads(vpath.read_text(encoding='utf-8'))
items = vdata['entries']


def find_entry(lemma_kanji, reading, gloss_hint):
    candidates = []
    for e in items:
        ent_lemma = e.get('lemma') or e.get('form') or ''
        ent_reading = e.get('reading') or ''
        ent_gloss = (e.get('gloss') or '').lower()
        if (ent_lemma == lemma_kanji or ent_lemma == reading) and (ent_reading == reading or not ent_reading):
            score = 0
            if gloss_hint.lower() in ent_gloss:
                score += 5
            candidates.append((score, e))
    if not candidates:
        return None
    candidates.sort(key=lambda x: -x[0])
    return candidates[0][1]


total_linked = 0
for chain_name, members in CHAINS:
    print(f'\nChain: {chain_name}')
    found_entries = []
    for (lemma, reading, gloss_hint, register) in members:
        e = find_entry(lemma, reading, gloss_hint)
        if e:
            found_entries.append((lemma, register, e))
            print(f'  ✓ {register:<10} {lemma} → {e["id"]}')
        else:
            print(f'  ✗ {register:<10} {lemma} NOT FOUND')

    # Cross-link every member to every other member in this chain
    if len(found_entries) >= 2:
        for i, (lemma_i, reg_i, e_i) in enumerate(found_entries):
            chain_links = []
            for j, (lemma_j, reg_j, e_j) in enumerate(found_entries):
                if i == j:
                    continue
                chain_links.append({
                    'id': e_j['id'],
                    'form': lemma_j,
                    'register': reg_j,
                })
            e_i['honorific_chain'] = {
                'name': chain_name,
                'self_register': reg_i,
                'related': chain_links,
            }
            # Also add register tag if missing
            if not e_i.get('register'):
                e_i['register'] = reg_i
            total_linked += 1

vpath.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')
print(f'\nTotal entries with honorific_chain populated: {total_linked}')
