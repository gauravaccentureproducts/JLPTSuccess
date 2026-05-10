"""Grammar Batch C-2 (2026-05-10):
Follow-up substitution: replace OOS (out-of-scope) kanji introduced by Batch C
in wrong_corrected_pair entries with kana equivalents.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Substitution map: OOS kanji compound (or single) -> kana
SUBS = [
    # Compounds first (longer matches)
    ('不自然', 'ふしぜん'),
    ('持って', 'もって'),
    ('公園', 'こうえん'),
    ('通り', 'とおり'),
    ('通る', 'とおる'),
    ('通ります', 'とおります'),
    ('時点', 'じてん'),
    ('住む', 'すむ'),
    ('住んで', 'すんで'),
    ('結婚', 'けっこん'),
    ('結婚する', 'けっこんする'),
    ('吸う', 'すう'),
    ('吸って', 'すって'),
    ('吸い', 'すい'),
    ('遠慮', 'えんりょ'),
    ('良い', 'よい'),
    ('静か', 'しずか'),
    ('明日', 'あした'),
    ('昨日', 'きのう'),
    ('違う', 'ちがう'),
    ('違い', 'ちがい'),
    ('違いま', 'ちがいま'),
    ('運転', 'うんてん'),
    ('運転する', 'うんてんする'),
    # Single chars (catch any remaining)
    ('不', 'ふ'),
    ('自', 'じ'),
    ('然', 'ぜん'),
    ('持', 'も'),
    ('公', 'こう'),
    ('園', 'えん'),
    ('通', 'とお'),
    ('点', 'てん'),
    ('住', 'す'),
    ('結', 'けつ'),
    ('婚', 'こん'),
    ('吸', 'す'),
    ('遠', 'えん'),
    ('慮', 'りょ'),
    ('良', 'よ'),
    ('静', 'しず'),
    ('明', 'あき'),
    ('昨', 'さく'),
    ('違', 'ちが'),
    ('運', 'うん'),
    ('転', 'てん'),
]

grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

def substitute(text: str) -> str:
    if not text:
        return text
    for old, new in SUBS:
        if old in text:
            text = text.replace(old, new)
    return text

# Apply only to wrong_corrected_pair entries (where Batch C OOS originated)
fixed = 0
fields_changed = 0
for p in patterns:
    wcp = p.get('wrong_corrected_pair')
    if not isinstance(wcp, list):
        continue
    for entry in wcp:
        for k in ('wrong', 'correct', 'why'):
            v = entry.get(k, '')
            new_v = substitute(v)
            if new_v != v:
                entry[k] = new_v
                fields_changed += 1
                fixed = 1
        if fixed:
            fixed = 0

# Verify: scan for remaining OOS kanji in user-facing fields
with open(ROOT / 'data' / 'kanji.json', encoding='utf-8') as f:
    kdata = json.load(f)
N5_KANJI = set()
for e in kdata.get('entries', []):
    g = e.get('glyph') or (e.get('id', '').split('.')[-1])
    if g:
        N5_KANJI.add(g)

def is_kanji(c):
    return 0x4E00 <= ord(c) <= 0x9FFF

remaining = {}
for p in patterns:
    wcp = p.get('wrong_corrected_pair')
    if not isinstance(wcp, list):
        continue
    for entry in wcp:
        for k in ('wrong','correct','why'):
            v = entry.get(k, '')
            for c in v:
                if is_kanji(c) and c not in N5_KANJI:
                    remaining.setdefault(c, []).append(p['id'])

print(f'Fields rewritten: {fields_changed}')
print(f'Remaining OOS kanji: {len(remaining)}')
for c, sites in remaining.items():
    print(f'  {c} -> {len(sites)} sites: {sites[:3]}')

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)
