"""Scan Hindi text for kana-transliterated-to-Devanagari anti-pattern.

The convention should be: Japanese tokens stay in Japanese script;
Devanagari is reserved for Hindi words. e.g., 'な-adjective' translates
to 'な-विशेषण' (kana + Devanagari), NOT 'ना-विशेषण' (Devanagari
syllable + Devanagari word).

Detects common patterns:
  ना-X        (should be な-X)        na-adjective
  ते-X        (should be て-X)        te-form
  ता-X        (should be た-X)        ta-form (past)
  नाई-X       (should be ない-X)      nai-form (negative)
  मासू-X      (should be ます-X)      masu-form
  देसू-X      (should be です-X)
  देस्-X      (should be です-X)
  सूरू-X      (should be する-X)
  क्ता-X      (should be いた-X / etc)

Plus reverse: Hindi syllables that legitimately appear in non-JLPT
contexts (e.g., कुता "dog" doesn't apply). We only flag when the
syllable is followed by a hyphen + a Hindi grammatical term.
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent

# Devanagari syllable + hyphen + Devanagari grammatical term = transliteration
# We list specific syllables that overlap with common Japanese kana romaji
# transliterated to Devanagari.
SUSPECTS = [
    # (devanagari_form, expected_kana, gloss)
    ('ना', 'な', 'na-adjective particle'),
    ('ते', 'て', 'te-form'),
    ('ता', 'た', 'ta-form (past)'),
    ('नाई', 'ない', 'nai-form (negative)'),
    ('मासू', 'ます', 'masu-form'),
    ('मास', 'ます', 'masu-form (variant)'),
    ('देसू', 'です', 'desu copula'),
    ('देस', 'です', 'desu (variant)'),
    ('सूरू', 'する', 'suru verb'),
    ('कूरू', 'くる', 'kuru verb'),
    ('इकू', 'いく', 'iku verb'),
    ('आरू', 'ある', 'aru existence'),
    ('इरू', 'いる', 'iru existence'),
    ('रू', 'る', 'ru-ending'),
    ('केई', 'けい', 'kei (form name)'),
    ('काता', 'かた', 'kata (way of)'),
    ('मासेन', 'ません', 'masen negative'),
]

# Hindi grammatical terms that signal a JLPT context
HINDI_GRAMMAR_TERMS = [
    'विशेषण', 'क्रिया', 'रूप', 'संज्ञा', 'कण', 'वाक्य', 'पैटर्न',
    'भूत', 'नकार', 'प्रश्न', 'आदेश', 'अनुरोध', 'अनुमति', 'इच्छा',
    'काल', 'पुरुष', 'वचन', 'समाप्ति', 'जोड़', 'विरोध',
]

def make_regex():
    """Build one regex per suspect: \\bSUSPECT-(?:HINDI_TERM)\\b"""
    patterns = []
    terms_alt = '|'.join(HINDI_GRAMMAR_TERMS)
    for dev, kana, gloss in SUSPECTS:
        # Match the suspect at a word boundary, followed by hyphen, followed by a Hindi grammar term
        pat = re.compile(rf'(?<![ऀ-ॿ]){re.escape(dev)}-(?:{terms_alt})\b')
        patterns.append((pat, dev, kana, gloss))
    return patterns

PATTERNS = make_regex()

def scan_value(s):
    """Returns list of (matched_text, suspect_devanagari, expected_kana, gloss)."""
    if not isinstance(s, str):
        return []
    hits = []
    for pat, dev, kana, gloss in PATTERNS:
        for m in pat.finditer(s):
            hits.append((m.group(0), dev, kana, gloss))
    return hits

def walk(node, path, all_hits):
    if isinstance(node, dict):
        for k, v in node.items():
            new_path = f'{path}.{k}' if path else k
            if isinstance(k, str) and (k == 'hi' or k.endswith('_hi') or k == 'l1_notes'):
                # Walk inside, looking for string values
                pass
            walk(v, new_path, all_hits)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk(item, f'{path}[{i}]', all_hits)
    elif isinstance(node, str):
        # Only check if it's likely Hindi (contains Devanagari)
        if any('ऀ' <= ch <= 'ॿ' for ch in node):
            hits = scan_value(node)
            if hits:
                all_hits.append((path, node, hits))

print('## Kana-transliteration anti-pattern scan')
print('## Looking for Devanagari syllables that should be Japanese kana')
print('=' * 72)

total_hits = 0
by_suspect = defaultdict(int)
all_examples = []

for fname in ['vocab.json', 'kanji.json', 'grammar.json', 'reading.json',
              'listening.json', 'questions.json']:
    path = ROOT / 'data' / fname
    if not path.exists():
        continue
    data = json.loads(path.read_text(encoding='utf-8'))
    file_hits = []
    walk(data, '', file_hits)
    if file_hits:
        print(f'\n=== data/{fname}: {len(file_hits)} entries with kana-transliteration ===')
        for fpath, fval, hits in file_hits[:6]:
            unique_dev = sorted(set(h[1] for h in hits))
            print(f'  @ {fpath[:80]}')
            print(f'    found: {unique_dev}')
            print(f'    text:  {fval[:140]}')
        total_hits += len(file_hits)
        for fpath, fval, hits in file_hits:
            for h in hits:
                by_suspect[h[1]] += 1
            all_examples.extend([(fname, fpath, fval, hits)])

# Locales hi.json
hi_ui = json.loads((ROOT / 'locales' / 'hi.json').read_text(encoding='utf-8'))
ui_hits = []
walk(hi_ui, '', ui_hits)
if ui_hits:
    print(f'\n=== locales/hi.json: {len(ui_hits)} UI entries with kana-transliteration ===')
    for fpath, fval, hits in ui_hits:
        unique_dev = sorted(set(h[1] for h in hits))
        print(f'  @ {fpath}')
        print(f'    found: {unique_dev}')
        print(f'    text:  {fval[:140]}')
    total_hits += len(ui_hits)
    for fpath, fval, hits in ui_hits:
        for h in hits:
            by_suspect[h[1]] += 1

print('\n' + '=' * 72)
print(f'Total entries with Devanagari kana-transliteration anti-pattern: {total_hits}')
print('\nBy suspect syllable (occurrences, not entries):')
for dev, count in sorted(by_suspect.items(), key=lambda x: -x[1]):
    expected = next((kana for d, kana, _ in SUSPECTS if d == dev), '?')
    print(f"  {dev!r} (should be {expected!r}): {count}")

# ============================================================================
# Pass 2: Latin romaji + Devanagari grammatical term (e.g., "na-विशेषण")
# ============================================================================
print('\n' + '=' * 72)
print('## Pass 2: Latin romaji + Devanagari grammatical term')
print('## (e.g., "na-विशेषण" — should be "な-विशेषण")')
print('=' * 72)

LATIN_SUSPECTS = ['na', 'i', 'te', 'ta', 'nai', 'masu', 'desu', 'su', 'ru',
                  'ku', 'kute', 'sou', 'tara', 'tari', 'tai', 'kute',
                  'ba', 'eba', 'reba']

# Pattern: optional preceding char that's not a letter, then a Latin word, hyphen, Devanagari grammar term
hindi_terms_alt = '|'.join(HINDI_GRAMMAR_TERMS)
latin_pattern = re.compile(
    rf'\b({"|".join(LATIN_SUSPECTS)})-({hindi_terms_alt})\b',
    re.IGNORECASE
)

latin_hits = defaultdict(list)

def walk_latin(node, path):
    if isinstance(node, dict):
        for k, v in node.items():
            new_path = f'{path}.{k}' if path else k
            walk_latin(v, new_path)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk_latin(item, f'{path}[{i}]')
    elif isinstance(node, str):
        if any('ऀ' <= ch <= 'ॿ' for ch in node):
            for m in latin_pattern.finditer(node):
                latin_hits[m.group(1).lower()].append((path, m.group(0), node[:140]))

for fname in ['vocab.json', 'kanji.json', 'grammar.json', 'reading.json',
              'listening.json', 'questions.json']:
    path = ROOT / 'data' / fname
    if path.exists():
        data = json.loads(path.read_text(encoding='utf-8'))
        walk_latin(data, fname)

hi_ui = json.loads((ROOT / 'locales' / 'hi.json').read_text(encoding='utf-8'))
walk_latin(hi_ui, 'locales/hi.json')

print('\nLatin-romaji + Devanagari occurrences:')
total_latin = 0
for syll, occurrences in sorted(latin_hits.items(), key=lambda x: -len(x[1])):
    total_latin += len(occurrences)
    print(f"\n  '{syll}-X' pattern: {len(occurrences)} hits")
    for path, match, sample in occurrences[:3]:
        print(f"    @ {path[:80]}")
        print(f"      matched: {match!r}")
        print(f"      text: {sample}")

print(f'\nTotal Latin-romaji-mix occurrences: {total_latin}')

# ============================================================================
# Pass 3: Confirm the "correct" form is actually used elsewhere (sanity)
# ============================================================================
print('\n' + '=' * 72)
print('## Pass 3: confirm correct form (Japanese kana + Devanagari) IS used')
print('=' * 72)

correct_pattern = re.compile(rf'[ぁ-んァ-ヶ]+-({hindi_terms_alt})')
correct_hits = 0
correct_examples = []

def walk_correct(node, path):
    global correct_hits
    if isinstance(node, dict):
        for k, v in node.items():
            new_path = f'{path}.{k}' if path else k
            walk_correct(v, new_path)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk_correct(item, f'{path}[{i}]')
    elif isinstance(node, str):
        if any('ऀ' <= ch <= 'ॿ' for ch in node):
            for m in correct_pattern.finditer(node):
                correct_hits += 1
                if len(correct_examples) < 8:
                    correct_examples.append((path, m.group(0), node[:120]))

for fname in ['vocab.json', 'kanji.json', 'grammar.json', 'reading.json',
              'listening.json', 'questions.json']:
    path = ROOT / 'data' / fname
    if path.exists():
        data = json.loads(path.read_text(encoding='utf-8'))
        walk_correct(data, fname)

walk_correct(hi_ui, 'locales/hi.json')

print(f'\nCorrect-form (Japanese kana + Devanagari grammatical term): {correct_hits} hits')
print('First 8 correct-form examples:')
for path, match, sample in correct_examples:
    print(f"  @ {path[:80]}")
    print(f"    matched: {match!r}")
    print(f"    text: {sample}")
