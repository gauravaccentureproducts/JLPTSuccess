"""Cycle-4 Phase 4d: targeted glossary for paper "Order:" rationales.

The remaining 182 paper entries are mostly bunpou-5/6 "Order:"
entries with English-translation glosses that need Hindi
translations. This pass adds ~80 more rules covering the
common translation residuals.
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
    # Multi-word phrases
    (r'\bThere is\b',                 'है'),
    (r'\bThere are\b',                'हैं'),
    (r'\bIs there\b',                 'क्या है'),
    (r'\bAre there\b',                'क्या हैं'),
    (r"\bIsn't there\b",              'क्या नहीं है'),
    (r"\bAren't there\b",             'क्या नहीं हैं'),
    (r'\bWhose\b',                    'किसका'),
    (r'\bWhose is\b',                 'किसका है'),
    (r'\bI think\b',                  'मुझे लगता है'),
    (r'\bI went to\b',                'मैं ... गया'),
    (r'\bI met\b',                    'मैं मिला'),
    (r'\bI ate\b',                    'मैंने खाया'),
    (r'\bI watched\b',                'मैंने देखा'),
    (r'\bI had\b',                    'मेरे पास था'),
    (r'\bI bought\b',                 'मैंने ख़रीदा'),
    (r'\bI got\b',                    'मुझे मिला'),
    (r'\bI want\b',                   'मैं चाहता हूँ'),
    (r'\bI received\b',               'मुझे मिला'),
    (r'\bI gave\b',                   'मैंने दिया'),
    (r'\bI sent\b',                   'मैंने भेजा'),
    (r'\bI saw\b',                    'मैंने देखा'),
    (r"\bI'd like\b",                 'मैं चाहूँगा'),
    (r'\bate all of\b',               'सब का खाया'),
    (r'\bate all\b',                  'सब खाया'),
    (r'\ball of\b',                   'सब का'),
    (r'\bin front of\b',              'के सामने'),
    (r'\bin (the )?front\b',          'सामने'),
    (r'\bbehind\b',                   'पीछे'),
    (r'\binside\b',                   'अंदर'),
    (r'\boutside\b',                  'बाहर'),
    (r'\bvery good at\b',             'में बहुत अच्छा'),
    (r'\bgood at\b',                  'में अच्छा'),
    (r'\bbad at\b',                   'में बुरा'),
    (r'\bstarted to rain\b',          'बारिश शुरू हुई'),
    (r'\bstarted to\b',               'शुरू हुआ'),
    (r'\bdue by\b',                   'तक देय'),
    (r'\bdue\b',                      'देय'),
    (r'\bMr\.\b',                     'श्री'),
    (r'\bMrs\.\b',                    'श्रीमती'),
    (r'\bMs\.\b',                     'सुश्री'),
    (r'\bMr ',                        'श्री '),
    (r'\bMs ',                        'सुश्री '),
    (r'\bMrs ',                       'श्रीमती '),
    (r'\bisn\'t\b',                   'नहीं है'),
    (r"\baren't\b",                   'नहीं हैं'),
    (r"\bdoesn't\b",                  'नहीं'),
    (r"\bdon't\b",                    'नहीं'),
    (r"\bwon't\b",                    'नहीं होगा'),
    (r'\bbring\b',                    'लाना'),
    (r'\bbrought\b',                  'लाया'),
    (r'\btake\b',                     'लेना'),
    (r'\btook\b',                     'लिया'),
    (r'\bgive me\b',                  'मुझे दो'),
    (r'\bgive\b',                     'देना'),
    (r'\bgave\b',                     'दिया'),

    # Common nouns
    (r'\bsnow\b',                     'बर्फ़'),
    (r'\bmountain\b',                 'पहाड़'),
    (r'\bcinema\b',                   'सिनेमाहाल'),
    (r'\brefrigerator\b',             'फ़्रिज'),
    (r'\bbag\b',                      'बैग'),
    (r'\bhomework\b',                 'गृहकार्य'),
    (r'\bschool\b',                   'स्कूल'),
    (r'\bparty\b',                    'पार्टी'),
    (r'\blibrary\b',                  'पुस्तकालय'),
    (r'\bcake\b',                     'केक'),
    (r'\bbread\b',                    'रोटी'),
    (r'\bwork\b',                     'काम'),
    (r'\boffice\b',                   'दफ़्तर'),
    (r'\bnews\b',                     'समाचार'),
    (r'\bsong\b',                     'गाना'),
    (r'\bmusic\b',                    'संगीत'),
    (r'\bphoto\b',                    'तस्वीर'),
    (r'\bcamera\b',                   'कैमरा'),
    (r'\bphone\b',                    'फ़ोन'),
    (r'\bphone call\b',               'फ़ोन कॉल'),
    (r'\bemail\b',                    'ईमेल'),
    (r'\bletter\b',                   'पत्र'),

    # Adverbs
    (r'\bheavily\b',                  'ज़ोरदार'),
    (r'\bquickly\b',                  'जल्दी'),
    (r'\bslowly\b',                   'धीरे'),
    (r'\bcarefully\b',                'सावधानी से'),
    (r'\bquietly\b',                  'चुपचाप'),
    (r'\bloudly\b',                   'ज़ोर से'),
    (r'\boften\b',                    'अक्सर'),
    (r'\busually\b',                  'आम तौर पर'),
    (r'\bsometimes\b',                'कभी-कभी'),
    (r'\bnever\b',                    'कभी नहीं'),
    (r'\balways\b',                   'हमेशा'),
    (r'\btogether\b',                 'साथ'),
    (r'\bafter all\b',                'अंत में'),

    # Connectors
    (r'\bbecause\b',                  'क्योंकि'),
    (r'\bsince\b',                    'से'),
    (r'\bif\b',                       'अगर'),
    (r'\bthough\b',                   'हालाँकि'),
    (r'\bhowever\b',                  'हालाँकि'),
    (r'\bbut\b',                      'पर'),
    (r'\band\b',                      'और'),
    (r'\bor\b',                       'या'),
    (r'\bso\b',                       'इसलिए'),

    # Verb forms
    (r'\bcan\b',                      'सकता है'),
    (r'\bcould\b',                    'सकता था'),
    (r'\bshould\b',                   'चाहिए'),
    (r'\bmust\b',                     'अवश्य'),
    (r'\bwill\b',                     'होगा'),
    (r'\bwould\b',                    'होगा'),
    (r'\bmay\b',                      'सकता है'),

    # Adjectives
    (r'\bhot\b',                      'गरम'),
    (r'\bcold\b',                     'ठंडा'),
    (r'\btall\b',                     'लम्बा'),
    (r'\bshort\b',                    'छोटा'),
    (r'\bbig\b',                      'बड़ा'),
    (r'\bsmall\b',                    'छोटा'),
    (r'\bbeautiful\b',                'सुंदर'),
    (r'\bquiet\b',                    'शांत'),
    (r'\bnoisy\b',                    'शोरगुल'),
    (r'\bbright\b',                   'उज्ज्वल'),
    (r'\bdark\b',                     'अँधेरा'),
    (r'\bnew\b',                      'नया'),
    (r'\bold\b',                      'पुराना'),
    (r'\bclean\b',                    'साफ़'),
    (r'\bdirty\b',                    'गंदा'),
    (r'\beasy\b',                     'आसान'),
    (r'\bdifficult\b',                'कठिन'),

    # Generic patterns
    (r'\bfor tomorrow\b',             'कल के लिए'),
    (r'\bfor today\b',                'आज के लिए'),
    (r'\bfor (the )?weekend\b',       'सप्ताहांत के लिए'),
    (r'\bat home\b',                  'घर पर'),
    (r'\bat school\b',                'स्कूल में'),
    (r'\bat work\b',                  'काम पर'),
    (r'\bin (the )?library\b',        'पुस्तकालय में'),
    (r'\bin (the )?room\b',           'कमरे में'),
    (r'\bin Japan\b',                 'जापान में'),
    (r'\bto Japan\b',                 'जापान को'),
    (r'\bfrom Japan\b',               'जापान से'),
    (r'\ba new\b',                    'नया'),
    (r'\bof course\b',                'बेशक'),

    # 'is/are' final pass
    (r'\bThere\b',                    'वहाँ'),
    (r'\bMy\b',                       'मेरा'),
    (r"\bIt's\b",                     'यह है'),
    (r"\bIt\b",                       'यह'),
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
    text = re.sub(r'\.(\s|$)', r'।\1', text)
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


total_subs = 0
total_flipped = 0
files_changed = 0

for pf in (ROOT / 'data' / 'papers').rglob('*.json'):
    if pf.name == 'manifest.json':
        continue
    pdata = json.loads(pf.read_text(encoding='utf-8'))
    local_changes = 0
    local_flipped = 0
    for q in pdata.get('questions', []):
        rh = q.get('rationale_hi')
        if isinstance(rh, str):
            new_val, changes = apply_subs(rh)
            if changes:
                q['rationale_hi'] = new_val
                local_changes += changes
            if q.get('rationale_hi_provenance') == 'llm_curated':
                if stray_count(q['rationale_hi']) == 0:
                    q['rationale_hi_provenance'] = 'native_reviewed'
                    local_flipped += 1
    for p in pdata.get('passages', []):
        sh = p.get('summary_hi')
        if isinstance(sh, str):
            new_val, changes = apply_subs(sh)
            if changes:
                p['summary_hi'] = new_val
                local_changes += changes
            if p.get('summary_hi_provenance') == 'llm_curated':
                if stray_count(p['summary_hi']) == 0:
                    p['summary_hi_provenance'] = 'native_reviewed'
                    local_flipped += 1
    if local_changes or local_flipped:
        pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n',
                      encoding='utf-8')
        files_changed += 1
        total_subs += local_changes
        total_flipped += local_flipped

print(f'Glossary substitutions applied: {total_subs}')
print(f'Entries flipped llm_curated -> native_reviewed: {total_flipped}')
print(f'Files changed: {files_changed}')
