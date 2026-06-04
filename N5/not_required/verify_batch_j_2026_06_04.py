import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('data/vocab.json', encoding='utf-8') as f:
    v = json.load(f)
entries = v['entries']

print('=== Verify cited bug fixes (J1 conjugations) ===')
checks = {
    'べんきょうする': ('べんきょうします', 'べんきょうするます'),
    'かす': ('かします', 'かすました'),
    'ある': ('あります', 'あるます'),
    'しごとする': ('しごとします', 'しごとするます'),
    'すむ': ('すみます', 'すむます'),
}
for form, (should_have, should_not) in checks.items():
    e = next((x for x in entries if x.get('form') == form), None)
    pe = e.get('particle_examples') or []
    print(f'  {form}: has {should_have!r}={should_have in pe} | malformed {should_not!r} present={should_not in pe}')

print('\n=== J4 specifics ===')
e = next(x for x in entries if x.get('form') == 'うるさい')
ringo = [x.get('ja') for x in e.get('examples') or [] if 'りんご' in (x.get('ja', '') or '')]
print(f'  うるさい: りんご examples remaining = {ringo}')
print(f'  うるさい examples now: {[x.get("ja") for x in e.get("examples") or []]}')
e = next(x for x in entries if x.get('form') == 'カタカナ')
print(f'  カタカナ particle_examples now: {e.get("particle_examples")}')

print('\n=== J2/J3 spot-check ===')
for form in ('まずい', 'まるい', 'ぬるい'):
    e = next(x for x in entries if x.get('form') == form)
    print(f'  {form} examples now: {[x.get("ja") for x in e.get("examples") or []]}')

print('\n=== Residual sweep: any form+ます/form+ました left? ===')
left = 0
for e in entries:
    form = e.get('form', '')
    pe = e.get('particle_examples') or []
    for p in pe:
        if p == form + 'ます' or p == form + 'ました':
            left += 1
            print(f'  STILL MALFORMED: {form} -> {p}')
print(f'  malformed remaining: {left}')

print('\n=== Residual: any えいがは <i-adj>でした left? ===')
import re
EIGA = re.compile(r'^えいがは\s*.+でした')
left2 = 0
for e in entries:
    for x in e.get('examples') or []:
        if EIGA.match((x.get('ja', '') or '').strip()):
            left2 += 1
            print(f'  STILL: {e.get("form")} -> {x.get("ja")}')
print(f'  えいがは-deshita remaining: {left2}')
