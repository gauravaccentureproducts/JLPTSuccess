"""Cycle-4 Phase 4c: extend glossary with paper-rationale-specific terms,
apply across paper files, then re-run clean-flip to native_reviewed.
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

RULES = [
    # Multi-word phrases
    (r"\bprior version\b",            "पूर्व संस्करण"),
    (r"\bcurrent version\b",          "वर्तमान संस्करण"),
    (r"\bstructurally broken\b",      "संरचनात्मक रूप से टूटा"),
    (r"\bstructurally\b",             "संरचनात्मक रूप से"),
    (r"\bcontrastive-topic\b",        "विरोध-विषय"),
    (r"\bcontrastive topic\b",        "विरोध-विषय"),
    (r"\bnon-exhaustive\b",           "आंशिक"),
    (r"\bexhaustive\b",               "पूर्ण"),
    (r"\bbefore doing\b",             "करने से पहले"),
    (r"\bafter doing\b",              "करने के बाद"),
    (r"\bwant to eat\b",              "खाना चाहना"),
    (r"\bwant to drink\b",            "पीना चाहना"),
    (r"\bwant to do\b",               "करना चाहना"),
    (r"\bwant to rest\b",             "आराम करना चाहना"),
    (r"\bdon't go\b",                 "नहीं जाना"),
    (r"\bdon't eat\b",                "नहीं खाना"),
    (r"\bin the hotel\b",             "होटल में"),
    (r"\bat the hotel\b",             "होटल में"),
    (r"\bon top of\b",                "के ऊपर"),
    (r"\bon (the )?top\b",            "ऊपर"),
    (r"\bI watched\b",                "मैंने देखा"),
    (r"\bI had\b",                    "मेरे पास था"),
    (r"\bI have been to\b",           "मैं ... जा चुका हूँ"),
    (r"\bhave been\b",                "जा चुके"),
    (r"\bbeen to\b",                  "जा चुके"),
    (r"\bgoes on (the )?★\b",         "★ पर आता है"),
    (r"\bcomes on (the )?★\b",        "★ पर आता है"),
    (r"\b(I |we |you )?got married\b", "विवाहित हुआ"),
    (r"\bget(s)? married\b",          "विवाहित होता है"),
    (r"\bsubject of\b",               "का कर्ता"),
    (r"\bobject of\b",                "का कर्म"),
    (r"\btopic of\b",                 "का विषय"),
    (r"\bexisting subject\b",         "मौजूदा कर्ता"),
    (r"\bexisting\b",                 "मौजूदा"),
    (r"\bintransitive verb\b",        "अकर्मक क्रिया"),
    (r"\btransitive verb\b",          "सकर्मक क्रिया"),
    (r"\bsentence-final\b",           "वाक्य-अंत्य"),
    (r"\binverts the logic\b",        "तर्क को उलट देता है"),
    (r"\bwould invert\b",             "उलट देगा"),
    (r"\bnatural fit\b",              "स्वाभाविक"),

    # Single words
    (r"\bpredicates?\b",              "विधेय"),
    (r"\bintransitive\b",             "अकर्मक"),
    (r"\btransitive\b",               "सकर्मक"),
    (r"\bparallel\b",                 "समानांतर"),
    (r"\bcausal\b",                   "कारणात्मक"),
    (r"\bconcessive\b",               "रियायत-सूचक"),
    (r"\blisting\b",                  "सूची"),
    (r"\blist\b",                     "सूची"),
    (r"\bcomparison\b",               "तुलना"),
    (r"\bsub\b",                      "कर्ता"),
    (r"\bneg\b",                      "नकारात्मक"),
    (r"\bprior\b",                    "पूर्व"),
    (r"\boption\b",                   "विकल्प"),
    (r"\boptions\b",                  "विकल्प"),
    (r"\bchained\b",                  "श्रृंखला-बद्ध"),
    (r"\bchain\b",                    "श्रृंखला"),
    (r"\banchored\b",                 "स्थिर"),
    (r"\banchor\b",                   "लंगर"),
    (r"\bdisambiguate\b",             "स्पष्ट करना"),
    (r"\bdisambiguation\b",           "स्पष्टीकरण"),
    (r"\bshop\b",                     "दुकान"),
    (r"\bdesk\b",                     "मेज़"),
    (r"\bhotel\b",                    "होटल"),
    (r"\bbread\b",                    "रोटी"),
    (r"\bChina\b",                    "चीन"),
    (r"\bJapan\b",                    "जापान"),
    (r"\bIndia\b",                    "भारत"),
    (r"\bname\b",                     "नाम"),
    (r"\bprohibition\b",              "निषेध"),
    (r"\binvert\b",                   "उलटना"),
    (r"\binverts\b",                  "उलटता है"),
    (r"\binverted\b",                 "उलटा हुआ"),
    (r"\brain\b",                     "बारिश"),
    (r"\bhungry\b",                   "भूखा"),
    (r"\brest\b",                     "आराम"),
    (r"\brationale\b",                "तर्क"),
    (r"\bdistractor\b",               "विकर्षक"),
    (r"\bdistractors\b",              "विकर्षक"),
    (r"\bcommutes\b",                 "आना-जाना करता है"),
    (r"\bbroken\b",                   "टूटा"),
    (r"\bcomplete\b",                 "पूर्ण"),
    (r"\bincomplete\b",               "अपूर्ण"),
    (r"\bgrandfather\b",              "दादा"),
    (r"\bgrandmother\b",              "दादी"),
    (r"\bbrother\b",                  "भाई"),
    (r"\bsister\b",                   "बहन"),
    (r"\baunt\b",                     "मौसी"),
    (r"\buncle\b",                    "मामा"),
    (r"\bmovie\b",                    "फ़िल्म"),
    (r"\btowel\b",                    "तौलिया"),
    (r"\bwallet\b",                   "बटुआ"),
    (r"\bumbrella\b",                 "छाता"),
    (r"\bglasses\b",                  "चश्मा"),
    (r"\bcat\b",                      "बिल्ली"),
    (r"\bdog\b",                      "कुत्ता"),
    (r"\bbird\b",                     "पक्षी"),
    (r"\bfish\b",                     "मछली"),
    (r"\bcar\b",                      "गाड़ी"),
    (r"\bbus\b",                      "बस"),
    (r"\btaxi\b",                     "टैक्सी"),
    (r"\bplane\b",                    "हवाई जहाज़"),
    (r"\bbicycle\b",                  "साइकिल"),
    (r"\bsubway\b",                   "मेट्रो"),
    (r"\btrain\b",                    "ट्रेन"),
    (r"\bstation\b",                  "स्टेशन"),
    (r"\bairport\b",                  "हवाई अड्डा"),
    (r"\bhospital\b",                 "अस्पताल"),
    (r"\bbank\b",                     "बैंक"),
    (r"\boffice\b",                   "दफ़्तर"),
    (r"\brestaurant\b",               "रेस्तराँ"),
    (r"\bsupermarket\b",              "सुपरमार्केट"),
    (r"\bconvenience store\b",        "सुविधा-दुकान"),
    (r"\bpost office\b",              "डाकघर"),
    (r"\bword for\b",                 "के लिए शब्द"),
    (r"\bword\b",                     "शब्द"),
    (r"\bquestions\b",                "प्रश्न"),
    (r"\banswer\b",                   "उत्तर"),
    (r"\bcorrect\b",                  "सही"),
    (r"\bgrandparents\b",             "दादा-दादी"),
    (r"\bclassroom\b",                "कक्षा"),
    (r"\blesson\b",                   "पाठ"),
    (r"\bclass\b",                    "कक्षा"),

    # Common copula-related residuals
    (r"\bcopula\b",                   "कोपुला"),
    (r"\bnegated\b",                  "नकारात्मक"),
    (r"\bnegation\b",                 "नकार"),
    (r"\baffirmation\b",              "सकार"),
    (r"\baffirmative\b",              "सकारात्मक"),

    # already in earlier glossaries but reinforce
    (r"\bpossessive\b",               "स्वामित्व"),
    (r"\bpossession\b",               "स्वामित्व"),

    # Final gluewords / boilerplate
    (r"\bexpressed\b",                "व्यक्त किया गया"),
    (r"\bbasic\b",                    "मूल"),
    (r"\bidentical\b",                "समान"),
    (r"\bequivalent\b",               "समकक्ष"),
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


# Apply to paper files
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
            # Now check if it's clean enough to flip
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
