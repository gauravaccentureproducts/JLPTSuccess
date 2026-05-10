"""Vocab Batch B: schema additions
- V2: pragmatic_functions on multi-function words
- V5: devoiced_vowels marker on common cases
- V6: word→pattern reverse map (frequent_patterns) — auto-derive from grammar examples
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

# --- V2: pragmatic_functions on multi-function words ---
print('=== V2: pragmatic_functions ===')
PRAGMA = {
    'すみません': [
        {'function': 'apology', 'gloss': 'sorry / I apologize', 'context': 'minor mistake / interrupting'},
        {'function': 'attention-getter', 'gloss': 'excuse me', 'context': "calling waiter / asking stranger"},
        {'function': 'gratitude-on-receiving', 'gloss': 'thank you (when receiving favor)', 'context': "ceding privilege; mild thanks"},
    ],
    '大丈夫': [
        {'function': 'confirmation', 'gloss': "I'm OK / it's fine", 'context': 'reassuring others'},
        {'function': 'polite-refusal', 'gloss': "no thanks", 'context': "declining offered food/help"},
        {'function': 'asking-after-someone', 'gloss': 'are you OK?', 'context': "checking welfare"},
    ],
    'どうぞ': [
        {'function': 'offering', 'gloss': 'here you go / please take', 'context': 'handing item'},
        {'function': 'please-do', 'gloss': 'please / go ahead', 'context': 'inviting action'},
        {'function': 'by-all-means', 'gloss': 'by all means / certainly', 'context': 'granting permission'},
    ],
    'どうも': [
        {'function': 'thanks-shortened', 'gloss': 'thanks', 'context': 'casual gratitude'},
        {'function': 'sorry-shortened', 'gloss': 'sorry', 'context': 'mild apology'},
        {'function': 'hello-shortened', 'gloss': 'hi / hello', 'context': 'casual greeting'},
        {'function': 'intensifier', 'gloss': 'very / really', 'context': 'before adjective: どうも すみません'},
    ],
    'ちょっと': [
        {'function': 'a-little', 'gloss': 'a little / a bit', 'context': 'small quantity'},
        {'function': 'pragmatic-softener', 'gloss': '...well... / hmm...', 'context': 'declining politely: 「ちょっと…」 trails off'},
        {'function': 'attention-getter', 'gloss': 'excuse me / hey', 'context': 'getting attention casually'},
    ],
    '結構': [
        {'function': 'fine-OK', 'gloss': 'fine / OK / sufficient', 'context': "「結構です」 (acceptable)"},
        {'function': 'polite-refusal', 'gloss': 'no thanks', 'context': "「結構です」 also = no thanks"},
        {'function': 'quite-rather', 'gloss': 'quite / rather', 'context': "「結構いい」 = pretty good"},
    ],
    'はい': [
        {'function': 'affirmative', 'gloss': 'yes', 'context': 'standard yes'},
        {'function': 'aizuchi', 'gloss': 'I see / mhm', 'context': 'back-channel acknowledgment'},
        {'function': 'attention-confirmation', 'gloss': 'present / here', 'context': 'roll-call response'},
        {'function': 'handing-over', 'gloss': 'here you go', 'context': "「はい、これ」 = here, take this"},
    ],
    'いいえ': [
        {'function': 'negative', 'gloss': 'no', 'context': 'standard no'},
        {'function': 'polite-disagreement', 'gloss': "no, that's not so / you're welcome", 'context': "deflecting praise: 「いいえ、そんなことありません」"},
    ],
    'お願いします': [
        {'function': 'request', 'gloss': "please / I'd like", 'context': "ordering / asking favor"},
        {'function': 'closing-greeting', 'gloss': "thanks in advance", 'context': "「よろしく お願いします」 — ritual close"},
    ],
}

prag_added = 0
for e in entries:
    form = e.get('form')
    if form in PRAGMA and not e.get('pragmatic_functions'):
        e['pragmatic_functions'] = PRAGMA[form]
        e['pragmatic_functions_provenance'] = 'llm_curated'
        prag_added += 1
print(f'  Annotated: {prag_added}')

# --- V5: devoiced_vowels marker on common cases ---
print()
print('=== V5: devoiced_vowels marker ===')
# Standard Tokyo speech devoices i/u between voiceless consonants or word-finally
# For common cases: です (des'), きく (kk), した (sht'), すき (sk'), すし (ssh)
DEVOICING = {
    'です':    {'positions': [1], 'note': 'word-final す devoices to "des\'"; standard Tokyo speech'},
    'きく':    {'positions': [1], 'note': 'final く devoices to "kk" between voiceless consonants'},
    'した':    {'positions': [0], 'note': 'first し often devoiced to "sht\'"'},
    'すき':    {'positions': [0], 'note': 'first す often devoiced to "sk\'"'},
    'すし':    {'positions': [0], 'note': 'first す often devoiced before し'},
    'いち':    {'positions': [0], 'note': '初 い often devoiced before voiceless ち'},
    'ふた':    {'positions': [0], 'note': 'ふ devoiced before voiceless た'},
    'はち':    {'positions': [0], 'note': 'は often shortened/devoiced'},
    'した':    {'positions': [0], 'note': 'し devoiced'},
    'くつ':    {'positions': [0], 'note': 'く devoiced before voiceless つ'},
    'して':    {'positions': [0], 'note': 'し devoiced before voiceless て'},
    'ちかく':  {'positions': [0], 'note': 'ち often shortened'},
    'ましょう': {'positions': [0], 'note': 'volitional ましょ — ま before sh'},
    'ました':  {'positions': [1], 'note': 'past ました — し often devoiced'},
    'ません':  {'positions': [0], 'note': 'negative ません — ま often shortened'},
    'まして':  {'positions': [1], 'note': 'connective form'},
    'です':    {'positions': [1], 'note': 'word-final す devoices to "des\'"'},
}

dev_added = 0
for e in entries:
    form = e.get('form')
    if form in DEVOICING and not e.get('devoiced_vowels'):
        e['devoiced_vowels'] = DEVOICING[form]
        e['devoiced_vowels_provenance'] = 'llm_curated'
        dev_added += 1
print(f'  Tagged: {dev_added}')

# --- V6: word→pattern reverse map ---
# Auto-derive: scan grammar.json examples and build vocab_form → set(pattern_id)
print()
print('=== V6: word→pattern reverse map ===')
G = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))['patterns']

vocab_id_to_form = {e.get('id'): e.get('form') for e in entries}
form_to_patterns = defaultdict(set)

for p in G:
    pid = p['id']
    for ex in (p.get('examples') or []):
        if not isinstance(ex, dict):
            continue
        for vid in (ex.get('vocab_ids') or []):
            form = vocab_id_to_form.get(vid)
            if form:
                form_to_patterns[form].add(pid)

# Now annotate vocab entries
rev_added = 0
for e in entries:
    form = e.get('form')
    pats = form_to_patterns.get(form, set())
    # Skip particles/super-common (would be huge); only annotate content words
    if e.get('pos') not in ('noun','verb-1','verb-2','verb-3','i-adj','na-adj','adverb'):
        continue
    if not pats:
        continue
    # Take top 5 patterns (sort by id for stability)
    e['frequent_patterns'] = sorted(pats)[:8]
    e['frequent_patterns_provenance'] = 'auto_derived'
    rev_added += 1

print(f'  Reverse map populated: {rev_added}')

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Summary
total = len(entries)
prag = sum(1 for e in entries if e.get('pragmatic_functions'))
dev = sum(1 for e in entries if e.get('devoiced_vowels'))
rev = sum(1 for e in entries if e.get('frequent_patterns'))
print()
print('=== FINAL ===')
print(f'  pragmatic_functions:  {prag}/{total}')
print(f'  devoiced_vowels:      {dev}/{total}')
print(f'  frequent_patterns:    {rev}/{total}')
