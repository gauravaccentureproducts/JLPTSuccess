import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('data/vocab.json', encoding='utf-8') as f:
    v = json.load(f)
entries = v['entries']
TARGETS = ['母','父','あに','あね','お母さん','お父さん','お兄さん','お姉さん',
           '祖父','祖母','おじいさん','おばあさん','おじさん','おばさん',
           'おくさん','ご主人']
print('=== Batch-D target presence ===')
for t in TARGETS:
    matches = [e for e in entries if e.get('form') == t]
    print(f'  {t!r}: {len(matches)} match(es) in corpus')

print()
print('=== 家族, 両親 counter state (form OR reading match) ===')
for t in ['家族', '両親', 'かぞく', 'りょうしん']:
    matches = [e for e in entries if e.get('form') == t or e.get('reading') == t]
    for e in matches:
        eid = e['id']
        c = e.get('counter')
        form = e.get('form')
        reading = e.get('reading')
        print(f'  search={t} form={form} reading={reading} (id={eid}): counter = {c!r}')

print()
print('=== お兄さん etc. by reading ===')
for t in ['おにいさん', 'おねえさん', 'そふ', 'そぼ', 'ごしゅじん']:
    matches = [e for e in entries if e.get('reading') == t]
    for e in matches:
        eid = e['id']
        form = e.get('form')
        reading = e.get('reading')
        gloss = e.get('gloss', '')[:50]
        print(f'  search={t} form={form} reading={reading} gloss={gloss}')
