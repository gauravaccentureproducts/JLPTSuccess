"""Round-9 audit snapshot — read-only.

Computes per-surface depth metrics for the audit report.
Single-use; safe to delete after the audit registration commits.
"""
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

# --- GRAMMAR ---
gd = json.loads(Path('data/grammar.json').read_text(encoding='utf-8'))
g = gd['patterns']
G = len(g)
print(f'GRAMMAR (n={G}):')
gd_rows = [
    ('examples >=5', sum(1 for p in g if len(p.get('examples', [])) >= 5), G),
    ('examples >=4', sum(1 for p in g if len(p.get('examples', [])) >= 4), G),
    ('contrasts >=1', sum(1 for p in g if len(p.get('contrasts', [])) >= 1), G),
    ('l1_notes.hi', sum(1 for p in g if (p.get('l1_notes') or {}).get('hi')), G),
    ('explanation_hi', sum(1 for p in g if p.get('explanation_hi')), G),
    ('native_reviewed (review_status)', sum(1 for p in g if p.get('review_status') == 'native_reviewed'), G),
    ('audio on examples', sum(1 for p in g if any(e.get('audio') for e in p.get('examples', []))), G),
    ('pitch on examples', sum(1 for p in g if any(e.get('pitch_accent') for e in p.get('examples', []))), G),
]
for name, met, tot in gd_rows:
    below = tot - met
    print(f'  {name:42s}: {met:4d}/{tot}  ({below} below, {below/tot*100:.0f}%)')
worst_g_ex = sorted([p for p in g if len(p.get('examples', [])) < 5], key=lambda p: len(p.get('examples', [])))[:10]
print(f'  worst-offender IDs (<5 ex): {[p["id"] for p in worst_g_ex]}')

# --- VOCAB ---
vd = json.loads(Path('data/vocab.json').read_text(encoding='utf-8'))
v = vd['entries']
V = len(v)
print(f'\nVOCAB (n={V}):')
verbs = [w for w in v if str(w.get('pos', '')).startswith('verb')]
nouns = [w for w in v if w.get('pos') == 'noun']
vd_rows = [
    ('examples >=2 (floor)', sum(1 for w in v if len(w.get('examples', [])) >= 2), V),
    ('examples >=3 (target)', sum(1 for w in v if len(w.get('examples', [])) >= 3), V),
    ('pitch_accent', sum(1 for w in v if w.get('pitch_accent') is not None), V),
    ('collocations >=1', sum(1 for w in v if len(w.get('collocations', [])) >= 1), V),
    ('register tag', sum(1 for w in v if w.get('register')), V),
    ('counter (out of nouns)', sum(1 for w in nouns if w.get('counter')), len(nouns)),
    ('verb_class (out of verbs)', sum(1 for w in verbs if w.get('verb_class')), len(verbs)),
    ('pair_id', sum(1 for w in v if w.get('pair_id')), V),
    ('native_reviewed', sum(1 for w in v if w.get('review_status') == 'native_reviewed'), V),
]
for name, met, tot in vd_rows:
    below = tot - met
    print(f'  {name:42s}: {met:4d}/{tot}  ({below} below, {below/tot*100:.0f}%)')

# --- KANJI ---
kd = json.loads(Path('data/kanji.json').read_text(encoding='utf-8'))
k = kd['entries']
K = len(k)
print(f'\nKANJI (n={K}):')
kd_rows = [
    ('examples >=5 (compound vocab)', sum(1 for x in k if len(x.get('examples', [])) >= 5), K),
    ('examples >=3', sum(1 for x in k if len(x.get('examples', [])) >= 3), K),
    ('confusable_with >=1', sum(1 for x in k if len(x.get('confusable_with', [])) >= 1), K),
    ('sentences >=1 (full N5 sentence)', sum(1 for x in k if x.get('sentences')), K),
    ('mnemonic', sum(1 for x in k if x.get('mnemonic')), K),
    ('native_reviewed', sum(1 for x in k if x.get('review_status') == 'native_reviewed'), K),
]
for name, met, tot in kd_rows:
    below = tot - met
    print(f'  {name:42s}: {met:4d}/{tot}  ({below} below, {below/tot*100:.0f}%)')
worst_k = sorted(k, key=lambda x: len(x.get('examples', [])))[:10]
print(f'  worst-offender (fewest cross-links): {[x["glyph"] for x in worst_k]}')

# --- READING ---
rd = json.loads(Path('data/reading.json').read_text(encoding='utf-8'))
r = rd['passages']
R = len(r)
print(f'\nREADING (n={R}):')
rd_rows = [
    ('mondai-5 (medium)', sum(1 for p in r if p.get('mondai') == 5), R),
    ('mondai-6 (info-search)', sum(1 for p in r if p.get('mondai') == 6), R),
    ('summary_hi', sum(1 for p in r if p.get('summary_hi')), R),
    ('cultural_context', sum(1 for p in r if p.get('cultural_context')), R),
    ('format_role', sum(1 for p in r if p.get('format_role')), R),
    ('format_type', sum(1 for p in r if p.get('format_type')), R),
    ('audio', sum(1 for p in r if p.get('audio')), R),
    ('native_reviewed', sum(1 for p in r if p.get('review_status') == 'native_reviewed'), R),
]
for name, met, tot in rd_rows:
    below = tot - met
    print(f'  {name:42s}: {met:4d}/{tot}  ({below} below, {below/tot*100:.0f}%)')

# --- LISTENING ---
ld = json.loads(Path('data/listening.json').read_text(encoding='utf-8'))
li = ld['items']
L = len(li)
print(f'\nLISTENING (n={L}):')
ld_rows = [
    ('audio file present', sum(1 for p in li if p.get('audio')), L),
    ('voice metadata', sum(1 for p in li if p.get('voice')), L),
    ('cultural_context', sum(1 for p in li if p.get('cultural_context')), L),
    ('explanation_hi', sum(1 for p in li if p.get('explanation_hi')), L),
    ('vocab_glossary', sum(1 for p in li if p.get('vocab_glossary') or p.get('glossary')), L),
    ('transcript_lines (timestamped)', sum(1 for p in li if isinstance(p.get('script_ja'), list) and p['script_ja'] and isinstance(p['script_ja'][0], dict)), L),
    ('native_reviewed', sum(1 for p in li if p.get('review_status') == 'native_reviewed'), L),
]
for name, met, tot in ld_rows:
    below = tot - met
    print(f'  {name:42s}: {met:4d}/{tot}  ({below} below, {below/tot*100:.0f}%)')
voices = {}
for p in li:
    voc = p.get('voice', 'no_voice')
    voices[voc] = voices.get(voc, 0) + 1
print(f'  voice variety: {voices}')

# --- QUESTIONS ---
qj = json.loads(Path('data/questions.json').read_text(encoding='utf-8'))
qs = qj['questions']
Q = len(qs)
print(f'\nQUESTIONS (n={Q}):')
print(f'  explanation_en: {sum(1 for q in qs if q.get("explanation_en"))}/{Q}')
print(f'  explanation_hi: {sum(1 for q in qs if q.get("explanation_hi"))}/{Q}')
print(f'  distractor_explanations: {sum(1 for q in qs if q.get("distractor_explanations"))}/{Q}')
