"""One-shot audit to verify the 2026-06-04 native-reviewer findings
against the live vocab corpus. Read-only.
Confirms scope of: kata sense mixing, counter on collective nouns,
homonym pairs needing 'don't confuse' notes, particle-example template
shapes, family-term gloss/register fields.
"""
import json
import sys
import io
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('data/vocab.json', encoding='utf-8') as f:
    d = json.load(f)
entries = d.get('entries', [])
print('Total entries:', len(entries))
print()

# 1. かた / 方 entries — is the sense really mixed?
print('--- (1) kata / 方 entries ---')
for e in entries:
    if e.get('form') in ('かた', '方', '〜かた', '〜方'):
        pe = e.get('particle_examples') or []
        ex = e.get('examples') or []
        print('  id={0}  form={1}  reading={2}'.format(e['id'], e['form'], e.get('reading') or '-'))
        print('    gloss      : {0}'.format(e.get('gloss', '-')))
        if pe:
            print('    particle_ex: {0}'.format(pe[:4]))
        if ex:
            for x in ex[:3]:
                print('    example    : {0}  -- {1}'.format(x.get('ja', ''), (x.get('translation_en') or '')[:50]))
print()

# 2. Counter on collective / abstract nouns
print('--- (2) counter on collective / abstract entries ---')
TARGETS = ['家族', '両親', '勉強', '旅行', '天気', '色', '味', 'みんな',
           'みんなさん', '皆さん', '会社', '学校', '人']
for target in TARGETS:
    for e in entries:
        if e.get('form') == target:
            c = e.get('counter')
            print('  {0:8s}  counter = {1!r}'.format(target, c))
print()

# 3. Homonym scan — readings shared by 2+ entries
print('--- (3) homonym readings (>= 2 entries) ---')
by_reading = defaultdict(list)
for e in entries:
    r = e.get('reading') or e.get('form') or ''
    if r:
        by_reading[r].append((e.get('form', ''), e.get('gloss', '')[:40]))
dups = {r: v for r, v in by_reading.items() if len(v) >= 2}
print('Total readings with >=2 entries: {0}'.format(len(dups)))
# Show the highlighted ones from the report
HIGHLIGHT = ['は', 'はな', 'あめ', 'はし', 'かみ', 'きる', 'いる',
             'あつい', 'とる', 'ひく', 'しめる', 'かぜ', 'はやい',
             'やさしい', 'なく', 'いま', 'かた']
for r in HIGHLIGHT:
    if r in dups:
        print('  ', r)
        for form, gloss in dups[r]:
            print('     form={0:10s}  gloss={1}'.format(form, gloss))
print()
# Other duplicates beyond the highlighted ones
extras = sorted([r for r in dups if r not in HIGHLIGHT])
print('Other duplicate readings:', len(extras))
for r in extras[:30]:
    forms = [f for f, _ in dups[r]]
    print('  {0:8s}  forms: {1}'.format(r, forms))
print()

# 4. Particle-example template detection
print('--- (4) suspect particle-example patterns ---')
# Reviewer flagged shapes:
SUSPECT_PATTERNS = [
    'をしますか', 'をしる', 'にいきますか', 'とあう',
]
suspect_count = 0
suspect_samples = []
for e in entries:
    pe = e.get('particle_examples') or []
    for p in pe:
        if any(sp in p for sp in SUSPECT_PATTERNS):
            suspect_count += 1
            if len(suspect_samples) < 20:
                suspect_samples.append('  {0:8s} (id={1}) :: {2}'.format(e.get('form', ''), e.get('id', ''), p))
print('Suspect particle examples found:', suspect_count)
for s in suspect_samples[:20]:
    print(s)
print()

# 5. Family entries — what's the current gloss / pragmatic note shape?
print('--- (5) family entries current gloss/register state ---')
FAMILY = ['母', '父', 'あに', 'あね', 'お母さん', 'お父さん',
          'お兄さん', 'お姉さん', '祖父', '祖母',
          'おじいさん', 'おばあさん', 'おじさん', 'おばさん',
          '家族', '両親', '兄', '姉', '弟', '妹']
for target in FAMILY:
    for e in entries:
        if e.get('form') == target:
            print('  {0}'.format(target))
            print('    gloss: {0}'.format(e.get('gloss', '-')))
            if e.get('register'):
                print('    register: {0}'.format(e['register']))
            if e.get('register_origin'):
                print('    register_origin: {0}'.format(e['register_origin']))
            if e.get('pragmatic_functions'):
                print('    pragmatic_functions: present ({0})'.format(len(e['pragmatic_functions'])))
            break

# 6. Verb pairs flagged: transitive/intransitive + homophones
print()
print('--- (6) verb pairs / homophones in corpus ---')
VERB_PAIRS = [
    ('あく', 'あける'),
    ('しまる', 'しめる'),
    ('おちる', 'おとす'),
    ('でる', 'だす'),
    ('きえる', 'けす'),
    ('はじまる', 'はじめる'),
]
for a, b in VERB_PAIRS:
    ea = next((e for e in entries if e.get('form') == a), None)
    eb = next((e for e in entries if e.get('form') == b), None)
    if ea and eb:
        print('  {0} <-> {1}'.format(a, b))
        print('    {0}: transitivity={1} pair_id={2}'.format(a, ea.get('transitivity'), ea.get('pair_id')))
        print('    {0}: transitivity={1} pair_id={2}'.format(b, eb.get('transitivity'), eb.get('pair_id')))
