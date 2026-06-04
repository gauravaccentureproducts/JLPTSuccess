import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('data/vocab.json', encoding='utf-8') as f:
    v = json.load(f)
entries = v['entries']

print('=== verb-3 (irregular) forms ===')
for e in entries:
    if e.get('pos') == 'verb-3':
        print(f'  {e.get("form")!r}  vc={e.get("verb_class")}  reading={e.get("reading")!r}')

print('\n=== all 「今日は とても X です」 examples (full list) ===')
import re
TPL = re.compile(r'^今日は\s*とても\s*(.+?)です')
for e in entries:
    for i, x in enumerate(e.get('examples') or []):
        ja = (x.get('ja','') or '').strip()
        m = TPL.match(ja)
        if m:
            print(f'  {e.get("form")!r} (pos={e.get("pos")}): {ja!r}')

print('\n=== verb-1 final-kana distribution (for conjugator coverage) ===')
from collections import Counter
finals = Counter()
for e in entries:
    if e.get('pos') == 'verb-1':
        f = e.get('form','')
        if f:
            finals[f[-1]] += 1
print(f'  {dict(finals)}')
