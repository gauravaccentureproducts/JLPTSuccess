"""Quantify the systematic template-artifact scope across the whole corpus.
Read-only. Counts:
  1. Verbs whose particle_examples contain form+ます or form+ました (malformed
     conjugation — you can't append ます to a dictionary form).
  2. Entries with an い-adjective でした past-form error (<...い>でした).
  3. Example sentences matching the nonsense templates
     「今日は とても <X>です」 and 「この <N>は <X>です」.
"""
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with open('data/vocab.json', encoding='utf-8') as f:
    v = json.load(f)
entries = v['entries']

# ---- 1. Verb conjugation artifacts in particle_examples ----
verb_artifacts = []
for e in entries:
    pos = e.get('pos', '') or ''
    form = e.get('form', '') or ''
    pe = e.get('particle_examples') or []
    if not pe:
        continue
    bad = []
    for p in pe:
        # malformed: dictionary form with ます or ました directly appended
        if p == form + 'ます' or p == form + 'ました':
            bad.append(p)
    if bad:
        verb_artifacts.append((e['id'], form, pos, e.get('verb_class'), bad, pe))

print(f'=== 1. Verb conjugation artifacts (form+ます / form+ました) ===')
print(f'Entries affected: {len(verb_artifacts)}')
# pos distribution
from collections import Counter
posc = Counter(a[2] for a in verb_artifacts)
print(f'pos distribution: {dict(posc)}')
vcc = Counter(a[3] for a in verb_artifacts)
print(f'verb_class distribution: {dict(vcc)}')
print('Sample (first 8):')
for a in verb_artifacts[:8]:
    print(f'  {a[1]} (pos={a[2]}, vc={a[3]}): bad={a[4]}')

# ---- 2. i-adjective でした past-form errors ----
ida_errors = []
DESHITA_RE = re.compile(r'い でした|いでした')
for e in entries:
    fields = []
    for p in (e.get('particle_examples') or []):
        if 'いでした' in p or 'い でした' in p:
            fields.append(('particle_examples', p))
    for i, x in enumerate(e.get('examples') or []):
        ja = x.get('ja', '') or ''
        if 'いでした' in ja or 'い でした' in ja:
            fields.append((f'examples[{i}].ja', ja))
    if fields:
        ida_errors.append((e['id'], e.get('form'), e.get('pos'), fields))

print(f'\n=== 2. i-adjective でした past-form errors ===')
print(f'Entries affected: {len(ida_errors)}')
for a in ida_errors[:15]:
    print(f'  {a[1]} (pos={a[2]}):')
    for fld, val in a[3]:
        print(f'    {fld}: {val!r}')

# ---- 3. Nonsense example-sentence templates ----
TPL_KYOU = re.compile(r'^今日は\s*とても\s*.+です')
TPL_KONO = re.compile(r'^この\s*\S+は\s*.+です')
tpl_examples = []
for e in entries:
    pos = e.get('pos', '') or ''
    for i, x in enumerate(e.get('examples') or []):
        ja = (x.get('ja', '') or '').strip()
        if TPL_KYOU.match(ja):
            tpl_examples.append((e['id'], e.get('form'), pos, f'examples[{i}]', 'KYOU-template', ja, x.get('translation_en', '')))
        elif TPL_KONO.match(ja):
            tpl_examples.append((e['id'], e.get('form'), pos, f'examples[{i}]', 'KONO-template', ja, x.get('translation_en', '')))

print(f'\n=== 3. Template example sentences (今日は とても X / この N は X) ===')
print(f'Total flagged: {len(tpl_examples)}')
kyou = [t for t in tpl_examples if t[4] == 'KYOU-template']
kono = [t for t in tpl_examples if t[4] == 'KONO-template']
print(f'  今日は とても X です: {len(kyou)}')
print(f'  この N は X です: {len(kono)}')
print('Sample KYOU (first 12):')
for t in kyou[:12]:
    print(f'  {t[1]} (pos={t[2]}): {t[5]!r}  -> {t[6][:40]!r}')
print('Sample KONO (first 12):')
for t in kono[:12]:
    print(f'  {t[1]} (pos={t[2]}): {t[5]!r}  -> {t[6][:40]!r}')
