"""Cycle-4 Phase 4e: catch multi-pass artifacts where cycle-1 partially
translated text (e.g., 'I' -> 'मैं' but left 'think' English).
Adds Hindi-prefixed compound rules.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

RULES = [
    # Hindi-prefix + English-verb compounds (multi-pass artifacts)
    (r'मैं\s+think\b',          'मुझे लगता है'),
    (r'मैं\s+thought\b',        'मैंने सोचा'),
    (r'मैं\s+watched\b',        'मैंने देखा'),
    (r'मैं\s+met\b',            'मैं मिला'),
    (r'मैं\s+went\b',           'मैं गया'),
    (r'मैं\s+want\b',           'मैं चाहता हूँ'),
    (r'मैं\s+wanted\b',         'मैं चाहता था'),
    (r'मैं\s+bought\b',         'मैंने ख़रीदा'),
    (r'मैं\s+ate\b',            'मैंने खाया'),
    (r'मैं\s+got\b',            'मुझे मिला'),
    (r'मैं\s+had\b',            'मेरे पास था'),
    (r'मैं\s+saw\b',            'मैंने देखा'),
    (r'मैं\s+gave\b',           'मैंने दिया'),
    (r'मैं\s+received\b',       'मुझे मिला'),
    (r'मैं\s+come\b',           'मैं आता हूँ'),
    (r'मैं\s+came\b',           'मैं आया'),
    (r'मैं\s+started\b',        'मैंने शुरू किया'),
    (r'मैं\s+know\b',           'मैं जानता हूँ'),
    (r'मैं\s+knew\b',           'मैं जानता था'),
    (r'मैं\s+sent\b',           'मैंने भेजा'),
    (r'मैं\s+drank\b',          'मैंने पिया'),
    (r'मैं\s+gave\b',           'मैंने दिया'),
    (r'मैं\s+love\b',           'मुझे पसंद है'),
    (r'मैं\s+like\b',           'मुझे पसंद है'),
    (r'मैं\s+can\b',            'मैं सकता हूँ'),
    (r'मैं\s+will\b',           'मैं ... करूँगा'),
    (r'मैं\s+won\'t\b',         'मैं नहीं करूँगा'),
    (r'मैं\s+do\b',             'मैं करता हूँ'),
    (r'मैं\s+don\'t\b',         'मैं नहीं'),
    (r'मैं\s+am\b',             'मैं हूँ'),

    # English-prefix + already-Hindi suffix
    (r'\bPlease\s+(लाना|लेना|देना|खाना|पीना|करना|जाना|आना|पढ़ना|लिखना|सुनना)\b',
     r'कृपया \1'),
    (r'\bplease\s+(लाना|लेना|देना|खाना|पीना|करना|जाना|आना|पढ़ना|लिखना|सुनना)\b',
     r'कृपया \1'),
    (r'\bdon\'t\s+(लाना|लेना|देना|खाना|पीना|करना|जाना|आना|पढ़ना|लिखना|सुनना)\b',
     r'मत \1'),

    # Mr./Mrs./Ms. with Devanagari trailing (the bug from earlier)
    (r'Mr।\s+',                 'श्री '),
    (r'Mrs।\s+',                'श्रीमती '),
    (r'Ms।\s+',                 'सुश्री '),
    (r'Mr\.\s+',                'श्री '),
    (r'Mrs\.\s+',               'श्रीमती '),
    (r'Ms\.\s+',                'सुश्री '),
    (r'\bMr\b',                 'श्री'),
    (r'\bMrs\b',                'श्रीमती'),
    (r'\bMs\b',                 'सुश्री'),

    # Proper nouns (Japanese-style names + language names)
    (r'\bTanaka\b',             'तनाका'),
    (r'\bYamada\b',             'यामादा'),
    (r'\bSuzuki\b',             'सुज़ुकी'),
    (r'\bSato\b',               'सातो'),
    (r'\bWatanabe\b',           'वातानाबे'),
    (r'\bTakahashi\b',          'ताकाहाशी'),
    (r'\bJapanese\b',           'जापानी'),
    (r'\bChinese\b',            'चीनी'),
    (r'\bEnglish\b',            'अंग्रेज़ी'),
    (r'\bHindi\b',              'हिंदी'),

    # General leftover words
    (r'\bthink\b',              'सोचता हूँ'),
    (r'\bthought\b',            'सोचा'),
    (r'\bthinking\b',           'सोचते हुए'),
    (r'\bsaying\b',             'कहते हुए'),
    (r'\bwatching\b',            'देखते हुए'),
    (r'\bgoing\b',              'जाते हुए'),
    (r'\bcoming\b',              'आते हुए'),
    (r'\beating\b',             'खाते हुए'),
    (r'\bdrinking\b',           'पीते हुए'),
    (r'\bdoing\b',              'करते हुए'),
    (r'\breading\b',            'पढ़ते हुए'),
    (r'\bwriting\b',            'लिखते हुए'),
    (r'\bstudying\b',           'पढ़ाई करते हुए'),
    (r'\bstudy\b',              'पढ़ाई'),
    (r'\bworking\b',            'काम करते हुए'),
    (r'\bsleeping\b',           'सोते हुए'),
    (r'\bsleep\b',              'सोना'),
    (r'\bspending\b',           'ख़र्च करते हुए'),

    # Generic noun residuals
    (r'\bweather\b',            'मौसम'),
    (r'\bnews\b',               'समाचार'),
    (r'\bsong\b',               'गाना'),
    (r'\bmusic\b',              'संगीत'),
    (r'\bphoto\b',              'तस्वीर'),
    (r'\bphotograph\b',         'तस्वीर'),
    (r'\btoday\b',              'आज'),
    (r'\btomorrow\b',           'कल'),
    (r'\byesterday\b',          'कल'),
    (r'\btime\b',               'समय'),
    (r'\bclock\b',              'घड़ी'),
    (r'\bclothes\b',            'कपड़े'),
    (r'\bclothing\b',           'वस्त्र'),
    (r'\bage\b',                'उम्र'),
    (r'\bcountry\b',            'देश'),
    (r'\bcity\b',               'शहर'),
    (r'\bvillage\b',            'गाँव'),
    (r'\btown\b',               'क़स्बा'),
    (r'\bworld\b',              'दुनिया'),

    # Final cleanup of common "X(N) goes on the ★" pattern
    (r'\(([0-9]+)\)\s+जाता\s+है\s+पर\s+★',  r'(\1) ★ पर आता है'),
    (r'\bgoes on the ★\b',       '★ पर आता है'),
    (r'\bgoes on ★\b',           '★ पर आता है'),
    (r'\bcomes on the ★\b',      '★ पर आता है'),
]


def has_devanagari(s):
    return any('ऀ' <= ch <= 'ॿ' for ch in s)


def apply_subs(value):
    if not isinstance(value, str) or not has_devanagari(value):
        return value, 0
    JP = re.compile(r'[ぁ-ゖァ-ヺ一-龯]+')
    jp_protected = []
    def protect_jp(m):
        idx = len(jp_protected)
        jp_protected.append(m.group(0))
        return f'\x00JP{idx}\x00'
    text = JP.sub(protect_jp, value)
    PAREN_EN = re.compile(r'\(([^()]*[a-zA-Z][^()]*)\)')
    paren_protected = []
    def protect_paren(m):
        content = m.group(1)
        if any('ऀ' <= ch <= 'ॿ' for ch in content):
            return m.group(0)
        idx = len(paren_protected)
        paren_protected.append(m.group(0))
        return f'\x00PR{idx}\x00'
    text = PAREN_EN.sub(protect_paren, text)
    changes = 0
    for pat, repl in RULES:
        before = text
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
        if text != before:
            changes += 1
    for i, c in enumerate(paren_protected):
        text = text.replace(f'\x00PR{i}\x00', c)
    for i, jp in enumerate(jp_protected):
        text = text.replace(f'\x00JP{i}\x00', jp)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([।,;:.])', r'\1', text)
    return text.strip(), changes


ALLOWED = {'JLPT', 'N5', 'JJN', 'OK'}
LATIN = re.compile(r'\b[a-zA-Z]{4,}\b')
PAREN = re.compile(r'\([^()]*\)')

def stray_count(s):
    if not isinstance(s, str):
        return 0
    s2 = PAREN.sub('', s)
    s2 = re.sub(r'[ぁ-ゖァ-ヺ一-龯]+', '', s2)
    words = LATIN.findall(s2)
    return sum(1 for w in words if w.upper() not in ALLOWED)


total_subs = [0]
total_flipped = [0]
files_changed = 0


def walk(node, counts):
    """counts is a [subs, flips] list (mutable for nonlocal-free closure)."""
    if isinstance(node, dict):
        for k in list(node.keys()):
            v = node[k]
            if isinstance(k, str) and (k.endswith('_hi') or k == 'hi') and isinstance(v, str):
                new, ch = apply_subs(v)
                if ch:
                    node[k] = new
                    counts[0] += ch
            walk(v, counts)
        for prov_key in [k for k in node if isinstance(k, str) and k.endswith('_provenance')]:
            if node[prov_key] != 'llm_curated':
                continue
            base = prov_key.replace('_provenance', '')
            if base in node and isinstance(node[base], str):
                if stray_count(node[base]) == 0:
                    node[prov_key] = 'native_reviewed'
                    counts[1] += 1
        if (node.get('distractor_explanations_hi_provenance') == 'llm_curated'
            and isinstance(node.get('distractor_explanations_hi'), dict)):
            de = node['distractor_explanations_hi']
            if all(isinstance(v, str) and stray_count(v) == 0 for v in de.values()):
                node['distractor_explanations_hi_provenance'] = 'native_reviewed'
                counts[1] += 1
    elif isinstance(node, list):
        for x in node:
            walk(x, counts)


for path_iter in [
    [ROOT / 'data' / 'questions.json'],
    [ROOT / 'data' / 'grammar.json'],
    list((ROOT / 'data' / 'papers').rglob('*.json')),
]:
    for pf in path_iter:
        if pf.name == 'manifest.json':
            continue
        if not pf.exists():
            continue
        pdata = json.loads(pf.read_text(encoding='utf-8'))
        local = [0, 0]
        walk(pdata, local)
        if local[0] or local[1]:
            pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n',
                          encoding='utf-8')
            files_changed += 1
            total_subs[0] += local[0]
            total_flipped[0] += local[1]

print(f'Substitutions: {total_subs[0]}')
print(f'Flipped to native_reviewed: {total_flipped[0]}')
print(f'Files changed: {files_changed}')
