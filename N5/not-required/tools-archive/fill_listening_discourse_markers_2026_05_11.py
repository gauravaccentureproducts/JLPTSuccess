"""Auto-derive discourse_markers_used on listening items by
scanning script_ja for known marker patterns.

Audit context: discourse_markers_used = 0/50 across all listening
items. Aizuchi tokens are already tagged on 17/50 — discourse
markers are a SUPERSET (aizuchi + fillers + topic-shifts +
conjunctions + politeness markers).

This pass scans each item's script_ja for tokens in a curated
discourse-marker inventory and writes the hits to
discourse_markers_used.

Marker inventory (categorized):
  fillers:        えーと / あの / あのー / そのー / うーん
  agreement:      そう / そうですね / そうですか / そうなんですか
  aizuchi:        うん / ええ / はい / ヘえ / なるほど / へぇ
  topic-shift:    じゃあ / じゃ / では / それでは / ところで
  emphasis:       やっぱり / やはり / もちろん / ぜひ
  conjunctions:   そして / それから / だから / でも / けど / が
  politeness:     よろしく / どうぞ / すみません

Each item gets:
  discourse_markers_used: [token1, token2, ...]
  discourse_markers_used_provenance: "auto_derived"
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Markers organized as (token, category). Longest first to avoid
# greedy mis-matches (e.g., そうですね before そう).
MARKERS = [
    # Politeness (multi-char first)
    ('どうもありがとうございます', 'politeness'),
    ('ありがとうございます', 'politeness'),
    ('どういたしまして', 'politeness'),
    ('よろしく', 'politeness'),
    ('すみません', 'politeness'),
    ('どうぞ', 'politeness'),
    # Agreement / aizuchi long forms
    ('そうなんですか', 'agreement'),
    ('そうですか', 'agreement'),
    ('そうですね', 'agreement'),
    ('なるほど', 'aizuchi'),
    ('わかりました', 'aizuchi'),
    # Topic shift
    ('それでは', 'topic-shift'),
    ('ところで', 'topic-shift'),
    ('じゃあ', 'topic-shift'),
    ('では', 'topic-shift'),
    ('じゃ、', 'topic-shift'),
    # Fillers
    ('えーと', 'filler'),
    ('えーっと', 'filler'),
    ('うーん', 'filler'),
    ('そのー', 'filler'),
    ('あのー', 'filler'),
    ('えーと、', 'filler'),
    # Conjunctions
    ('そして', 'conjunction'),
    ('それから', 'conjunction'),
    ('だから', 'conjunction'),
    ('でも', 'conjunction'),
    ('けど', 'conjunction'),
    # Short aizuchi (after multi-char so don't shadow)
    ('はい', 'aizuchi'),
    ('うん', 'aizuchi'),
    ('ええ', 'aizuchi'),
    ('そう', 'agreement'),
    ('あの', 'filler'),
    ('へぇ', 'aizuchi'),
    ('ヘえ', 'aizuchi'),
    # Emphasis
    ('やっぱり', 'emphasis'),
    ('やはり', 'emphasis'),
    ('もちろん', 'emphasis'),
    ('ぜひ', 'emphasis'),
]


def scan(script: str) -> list[dict]:
    """Return list of {token, category, count} dicts for hits."""
    if not script:
        return []
    found = {}
    work = script
    # Greedy match longest-first; once a token is consumed, blank it out
    # in the workspace so substring tokens don't double-count.
    for tok, cat in MARKERS:
        cnt = work.count(tok)
        if cnt > 0:
            found[tok] = {'token': tok, 'category': cat, 'count': cnt}
            work = work.replace(tok, ' ' * len(tok))
    return list(found.values())


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_discourse_markers')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    n = 0
    distribution = {}
    for it in data['items']:
        if it.get('discourse_markers_used'):
            continue
        hits = scan(it.get('script_ja') or '')
        if not hits:
            continue
        it['discourse_markers_used'] = hits
        it['discourse_markers_used_provenance'] = 'auto_derived'
        n += 1
        for h in hits:
            distribution[h['token']] = distribution.get(h['token'], 0) + h['count']

    print(f'\nTagged {n} listening items with discourse_markers_used.')
    print('Top markers by frequency:')
    for tok, c in sorted(distribution.items(), key=lambda x: -x[1])[:12]:
        print(f'  {tok}: {c}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
