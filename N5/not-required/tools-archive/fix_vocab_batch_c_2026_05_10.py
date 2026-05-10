"""Vocab Batch C (2026-05-10):
- V5: devoiced_vowels — expand from 4 to ~50 common Tokyo-standard cases
- V2: pragmatic_functions — add 6 more multi-function N5 words
- V8 (start): counter_register pairs — pilot 6 counter words
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

# --- V5: Standard Tokyo devoicing ---
# Rules: high vowels /i/, /u/ devoice
#   1. Between two voiceless consonants (k/s/t/h/p)
#   2. Word-finally after a voiceless consonant
# Mora positions are 0-indexed.
print('=== V5: devoiced_vowels expansion ===')
DEVOICING = {
    # final-す devoicing (です/ます ecosystem)
    'です':       {'positions': [1], 'note': "word-final す devoices to des'", 'rule': 'final_after_voiceless'},
    'ます':       {'positions': [1], 'note': "word-final す devoices to mas'", 'rule': 'final_after_voiceless'},
    'ません':     {'positions': [], 'note': 'no standard devoicing — m is voiced', 'rule': 'no_devoicing'},
    # しー (し between voiceless)
    'した':       {'positions': [0], 'note': "first し devoices to sht' (s+t voiceless)", 'rule': 'between_voiceless'},
    'して':       {'positions': [0], 'note': "first し devoices (s+t voiceless)", 'rule': 'between_voiceless'},
    'しつもん':   {'positions': [0], 'note': "first し devoices before voiceless つ", 'rule': 'between_voiceless'},
    'しけん':     {'positions': [0], 'note': "first し devoices before voiceless k", 'rule': 'between_voiceless'},
    'しちじ':     {'positions': [0], 'note': "first し devoices before voiceless ち", 'rule': 'between_voiceless'},
    'しちがつ':   {'positions': [0], 'note': "first し devoices before voiceless ち", 'rule': 'between_voiceless'},
    'しゅくだい': {'positions': [0], 'note': "first しゅ devoices before voiceless k", 'rule': 'between_voiceless'},
    'しんぱい':   {'positions': [0], 'note': "first し devoices before voiceless p (ぱ)", 'rule': 'between_voiceless'},
    # きー (き between voiceless)
    'きく':       {'positions': [0], 'note': "き devoices between voiceless k+k", 'rule': 'between_voiceless'},
    'きた':       {'positions': [0], 'note': "き devoices before voiceless t", 'rule': 'between_voiceless'},
    'きって':     {'positions': [0], 'note': "き devoices before voiceless tt", 'rule': 'between_voiceless'},
    'きっぷ':     {'positions': [0], 'note': "き devoices before voiceless pp", 'rule': 'between_voiceless'},
    'きそく':     {'positions': [0], 'note': "き devoices before voiceless s", 'rule': 'between_voiceless'},
    'きかい':     {'positions': [0], 'note': "き devoices before voiceless k", 'rule': 'between_voiceless'},
    # すー (す between voiceless)
    'すし':       {'positions': [0], 'note': "first す devoices before voiceless し", 'rule': 'between_voiceless'},
    'すき':       {'positions': [0], 'note': "first す devoices before voiceless k", 'rule': 'between_voiceless'},
    'すこし':     {'positions': [0], 'note': "first す devoices before voiceless k", 'rule': 'between_voiceless'},
    'すきやき':   {'positions': [0], 'note': "first す devoices before voiceless k", 'rule': 'between_voiceless'},
    'すずしい':   {'positions': [0], 'note': "first す devoices before voiceless す/ず onset", 'rule': 'between_voiceless'},
    # くー
    'くつ':       {'positions': [0], 'note': "く devoices before voiceless つ", 'rule': 'between_voiceless'},
    'くさ':       {'positions': [0], 'note': "く devoices before voiceless s", 'rule': 'between_voiceless'},
    'くすり':     {'positions': [0], 'note': "く devoices before voiceless s", 'rule': 'between_voiceless'},
    # ふー
    'ふたつ':     {'positions': [0], 'note': "ふ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ふたり':     {'positions': [0], 'note': "ふ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ふく':       {'positions': [0], 'note': "ふ devoices before voiceless k", 'rule': 'between_voiceless'},
    'ふつう':     {'positions': [0], 'note': "ふ devoices before voiceless つ", 'rule': 'between_voiceless'},
    # ちー
    'ちかく':     {'positions': [0], 'note': "ち often shortened/devoiced before voiceless k", 'rule': 'between_voiceless'},
    'ちかい':     {'positions': [0], 'note': "ち devoices before voiceless k", 'rule': 'between_voiceless'},
    'ちず':       {'positions': [0], 'note': "ち devoices before voiceless す/ず onset", 'rule': 'between_voiceless'},
    'ちち':       {'positions': [0, 1], 'note': "both ち's may devoice (ch+ch)", 'rule': 'between_voiceless'},
    'ちかてつ':   {'positions': [0], 'note': "ち devoices before voiceless k", 'rule': 'between_voiceless'},
    # ひー
    'ひと':       {'positions': [0], 'note': "ひ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ひとつ':     {'positions': [0], 'note': "ひ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ひとり':     {'positions': [0], 'note': "ひ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ひこうき':   {'positions': [0], 'note': "ひ devoices before voiceless k", 'rule': 'between_voiceless'},
    # つー
    'つくえ':     {'positions': [0], 'note': "つ devoices before voiceless k", 'rule': 'between_voiceless'},
    'つかい':     {'positions': [0], 'note': "つ devoices before voiceless k", 'rule': 'between_voiceless'},
    'つくる':     {'positions': [0], 'note': "つ devoices before voiceless k", 'rule': 'between_voiceless'},
    # number/counter words
    'いち':       {'positions': [0], 'note': "い marginally devoiced before voiceless ch", 'rule': 'between_voiceless'},
    'はち':       {'positions': [0], 'note': "は often shortened/devoiced before voiceless ch", 'rule': 'between_voiceless'},
    'はちじ':     {'positions': [0], 'note': "は devoices before voiceless ch", 'rule': 'between_voiceless'},
    # politeness markers
    'ました':     {'positions': [1], 'note': "past ました — し often devoiced (between voiceless)", 'rule': 'between_voiceless'},
    'まして':     {'positions': [1], 'note': "connective form — し devoices", 'rule': 'between_voiceless'},
    'ましょう':   {'positions': [1], 'note': "volitional ましょ — し often shortened", 'rule': 'between_voiceless'},
    # special: っ (sokuon) words
    'がっこう':   {'positions': [], 'note': 'sokuon-onset; voiceless geminate, no vowel devoicing', 'rule': 'no_devoicing'},
}

dev_added = 0
dev_replaced = 0
for e in entries:
    form = e.get('form')
    reading = e.get('reading')
    target = None
    if form in DEVOICING:
        target = DEVOICING[form]
    elif reading in DEVOICING:
        target = DEVOICING[reading]
    if target is not None:
        if e.get('devoiced_vowels'):
            # Replace with new richer form (rule field)
            e['devoiced_vowels'] = target
            e['devoiced_vowels_provenance'] = 'llm_curated'
            dev_replaced += 1
        else:
            e['devoiced_vowels'] = target
            e['devoiced_vowels_provenance'] = 'llm_curated'
            dev_added += 1

print(f'  Tagged: {dev_added} new + {dev_replaced} re-annotated')

# --- V2: pragmatic_functions ---
print()
print('=== V2: pragmatic_functions expansion ===')
PRAGMA_NEW = {
    'そうです': [
        {'function': 'confirmation', 'gloss': "that's right / yes that's so", 'context': 'confirming a statement'},
        {'function': 'aizuchi', 'gloss': "I see / oh really", 'context': 'back-channel acknowledgment'},
        {'function': 'hearsay-marker', 'gloss': "I hear that / apparently", 'context': "after V/Adj plain: 雨が降る そうです"},
    ],
    'もう': [
        {'function': 'already', 'gloss': "already", 'context': "もう食べました = already ate"},
        {'function': 'no-longer', 'gloss': "no longer (with negative)", 'context': "もう食べません = no longer eat"},
        {'function': 'one-more', 'gloss': "one more / another", 'context': "もう一杯 = one more cup"},
    ],
    'まだ': [
        {'function': 'still', 'gloss': "still (with positive)", 'context': "まだ食べています = still eating"},
        {'function': 'not-yet', 'gloss': "not yet (with ていません)", 'context': "まだ食べていません = haven't eaten yet"},
        {'function': 'only', 'gloss': "only / merely", 'context': "まだ子供だ = (he's) just a child"},
    ],
    'でも': [
        {'function': 'sentence-conjunction', 'gloss': "but / however", 'context': "starts a contrasting sentence"},
        {'function': 'even', 'gloss': "even (X)", 'context': "子供でも わかる = even a child understands"},
        {'function': 'or-something', 'gloss': "or something / how about", 'context': "コーヒーでも飲みませんか = how about coffee?"},
    ],
    'いいです': [
        {'function': 'good-OK', 'gloss': "(it's) good / fine", 'context': 'positive evaluation'},
        {'function': 'polite-refusal', 'gloss': "no thanks", 'context': "(けっこう です) — declining offer"},
        {'function': 'permission-grant', 'gloss': "OK / go ahead", 'context': "use it as you wish"},
    ],
    'ところ': [
        {'function': 'place-noun', 'gloss': "place / spot", 'context': "いいところ = nice place"},
        {'function': 'about-to', 'gloss': "about to V", 'context': "Vる + ところ = about to do"},
        {'function': 'just-did', 'gloss': "just did V", 'context': "Vた + ところ = just finished"},
    ],
}

prag_added = 0
for e in entries:
    form = e.get('form')
    if form in PRAGMA_NEW and not e.get('pragmatic_functions'):
        e['pragmatic_functions'] = PRAGMA_NEW[form]
        e['pragmatic_functions_provenance'] = 'llm_curated'
        prag_added += 1

print(f'  Annotated: {prag_added}')

# --- V8: counter_register pilot ---
print()
print('=== V8: counter_register (pilot) ===')
# For people-counters: ひとり/ふたり/(さんにん) etc., note that 1-2 are
# kun-yomi exceptions, 3+ uses on-yomi pattern. Useful for learners.
COUNTER_REGISTER = {
    'ひとり': {
        'counter': 'にん',
        'irregular': True,
        'note': '1-person uses irregular kun-reading ひとり (NOT いちにん). Standard for politeness.',
        'register_pair': {'casual_alt': '一人 (ひとり)', 'formal_same': '一名 (いちめい — very formal contexts only)'},
    },
    'ふたり': {
        'counter': 'にん',
        'irregular': True,
        'note': '2-person uses irregular kun-reading ふたり (NOT ににん). Standard.',
        'register_pair': {'casual_alt': '二人 (ふたり)', 'formal_same': '二名 (にめい)'},
    },
    'ひとつ': {
        'counter': 'つ',
        'irregular': True,
        'note': 'Generic counter 1-thing uses kun-stem ひと- (1-10: ひと/ふた/みっ/よっ/いつ/むっ/なな/やっ/ここの/とお)',
        'register_pair': {'casual_alt': '一個 (いっこ)', 'formal_same': '一品 (いっぴん — for goods)'},
    },
    'ひとつき': {
        'counter': 'つき/かげつ',
        'irregular': False,
        'note': 'Casual: ひとつき (1 month). Formal: いっかげつ. Both common in N5.',
        'register_pair': {'casual_alt': 'ひとつき', 'formal_same': '一ヶ月 (いっかげつ)'},
    },
    'いっぱい': {
        'counter': 'はい',
        'irregular': False,
        'note': '1-cup. Sound-change: い+ぱい (rendaku-like geminate after い).',
        'register_pair': {'casual_alt': 'いっぱい', 'formal_same': '一杯'},
    },
    'いっぴき': {
        'counter': 'ひき',
        'irregular': False,
        'note': '1-small-animal. Sound change: い+ぴき (geminate).',
        'register_pair': {'casual_alt': 'いっぴき', 'formal_same': '一匹'},
    },
}

cr_added = 0
for e in entries:
    form = e.get('form')
    reading = e.get('reading')
    target_form = form if form in COUNTER_REGISTER else (reading if reading in COUNTER_REGISTER else None)
    if target_form and not e.get('counter_register'):
        e['counter_register'] = COUNTER_REGISTER[target_form]
        e['counter_register_provenance'] = 'llm_curated'
        cr_added += 1

print(f'  Annotated: {cr_added}')

# Save
vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final
total = len(entries)
prag = sum(1 for e in entries if e.get('pragmatic_functions'))
dev = sum(1 for e in entries if e.get('devoiced_vowels'))
cr = sum(1 for e in entries if e.get('counter_register'))
print()
print('=== FINAL ===')
print(f'  pragmatic_functions:  {prag}/{total}')
print(f'  devoiced_vowels:      {dev}/{total}')
print(f'  counter_register:     {cr}/{total}')
