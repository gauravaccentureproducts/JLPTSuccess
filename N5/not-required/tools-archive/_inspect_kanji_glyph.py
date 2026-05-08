import io, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.load(open(ROOT / 'data/kanji.json', encoding='utf-8'))
items = d['entries']
print(f'Total: {len(items)}')
print('First 3 entries:')
for e in items[:3]:
    print(f"  id={e.get('id')!r}  char={e.get('char')!r}  glyph={e.get('glyph')!r}")
print()
print('Searching for cluster glyphs by char field, id, or contains:')
for target in ['犬', '太', '末', '未', '止', '正', '占', '王', '玉', '干']:
    matches = []
    for e in items:
        ent_id = e.get('id', '')
        if e.get('char') == target or e.get('glyph') == target or target in ent_id:
            matches.append(e.get('id'))
    print(f"  {target}: {matches if matches else 'NOT FOUND'}")
