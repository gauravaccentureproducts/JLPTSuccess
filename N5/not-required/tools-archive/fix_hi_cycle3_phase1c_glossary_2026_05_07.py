"""Cycle-3 Phase 1c: third-tier glossary expansion targeting the
residual English words found in cycle-3's questions.json llm_curated
batch.

Targets words I noticed during the 58-entry rubric review.
"""
from __future__ import annotations
import argparse
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
    # Multi-word phrases first
    (r"\bday after tomorrow\b",       "परसों"),
    (r"\bday before yesterday\b",     "परसों"),
    (r"\bthis morning\b",             "आज सुबह"),
    (r"\bthis evening\b",             "आज शाम"),
    (r"\bthis afternoon\b",           "आज दोपहर"),
    (r"\b2 days ago\b",               "2 दिन पहले"),
    (r"\b3 days ago\b",               "3 दिन पहले"),
    (r"\bdiary-entry\b",              "डायरी-प्रविष्टि"),
    (r"\bdiary entry\b",              "डायरी प्रविष्टि"),
    (r"\bdictionary form\b",          "शब्दकोश रूप"),
    (r"\bSpecific-to-general\b",      "विशिष्ट-से-सामान्य"),
    (r"\bspecific-to-general\b",      "विशिष्ट-से-सामान्य"),
    (r"\bantonym-via-negation\b",     "नकार-द्वारा-विलोम"),
    (r"\bantonym via negation\b",     "नकार के द्वारा विलोम"),
    (r"\bAntonym pair\b",             "विलोम जोड़ी"),
    (r"\bantonym pair\b",             "विलोम जोड़ी"),
    (r"\bopposite-meaning\b",         "विपरीत-अर्थ"),
    (r"\bbad-tasting\b",              "बेस्वाद"),
    (r"\bgood-tasting\b",              "स्वादिष्ट"),
    (r"\ba lot\b",                    "बहुत"),
    (r"\ba bit\b",                    "थोड़ा"),
    (r"\bin price context\b",         "क़ीमत के संदर्भ में"),
    (r"\bin terms of\b",              "के संदर्भ में"),
    (r"\bDirect lexical equivalence\b", "सीधी शाब्दिक समानता"),
    (r"\bdirect lexical equivalence\b", "सीधी शाब्दिक समानता"),
    (r"\blexical equivalence\b",      "शाब्दिक समानता"),
    (r"\bnative counter\b",           "देसी काउंटर"),
    (r"\bsynonym chain\b",            "पर्याय श्रृंखला"),
    (r"\bsynonym pair\b",             "पर्याय जोड़ी"),
    (r"\bI didn't\b",                 "मैंने नहीं"),
    (r"\bI don't\b",                  "मैं नहीं"),
    (r"\bI'll\b",                     "मैं"),
    (r"\bwe'll\b",                    "हम"),
    (r"\byou're\b",                   "आप हैं"),
    (r"\bI'm\b",                      "मैं हूँ"),

    # Single words - new additions
    (r"\byesterday\b",                "कल"),
    (r"\btomorrow\b",                 "कल"),
    (r"\btoday\b",                    "आज"),
    (r"\bnow\b",                      "अभी"),
    (r"\bmorning\b",                  "सुबह"),
    (r"\bevening\b",                  "शाम"),
    (r"\bafternoon\b",                "दोपहर"),
    (r"\bnight\b",                    "रात"),
    (r"\bfamous\b",                   "प्रसिद्ध"),
    (r"\bexception\b",                "अपवाद"),
    (r"\bexceptions\b",               "अपवाद"),
    (r"\bexceptional\b",              "अपवादी"),
    (r"\bfinal\b",                    "अंतिम"),
    (r"\bmiddle\b",                   "मध्य"),
    (r"\bongoing\b",                  "जारी"),
    (r"\bmarried\b",                  "विवाहित"),
    (r"\bpunctual\b",                 "क्षणिक"),
    (r"\bresulting\b",                "परिणामस्वरूप"),
    (r"\bbit\b",                      "थोड़ा"),
    (r"\boffer\b",                    "प्रस्ताव"),
    (r"\boffers\b",                   "प्रस्ताव"),
    (r"\boffered\b",                  "प्रस्तुत किया"),
    (r"\bpredicatively\b",            "विधेयात्मक रूप से"),
    (r"\bpredicative\b",              "विधेयात्मक"),
    (r"\binanimate\b",                "निर्जीव"),
    (r"\banimate\b",                  "सजीव"),
    (r"\binanimate\b",                "निर्जीव"),
    (r"\bevents\b",                   "घटनाएँ"),
    (r"\bevent\b",                    "घटना"),
    (r"\bMultiple\b",                 "कई"),
    (r"\bmultiple\b",                 "कई"),
    (r"\bexcept\b",                   "के सिवाय"),
    (r"\bcarries\b",                  "धारण करता है"),
    (r"\bcarry\b",                    "धारण करना"),
    (r"\bcarried\b",                  "धारण किया"),
    (r"\bsignals\b",                  "संकेत देता है"),
    (r"\bsignal\b",                   "संकेत"),
    (r"\bforces\b",                   "मजबूर करता है"),
    (r"\bforce\b",                    "बल"),
    (r"\bforced\b",                   "मजबूर"),
    (r"\badverbs\b",                  "क्रियाविशेषण"),
    (r"\badverb\b",                   "क्रियाविशेषण"),
    (r"\bamount\b",                   "मात्रा"),
    (r"\btarget\b",                   "लक्ष्य"),
    (r"\btargets\b",                  "लक्ष्य"),
    (r"\btargeted\b",                 "लक्षित"),
    (r"\bquantity\b",                 "मात्रा"),
    (r"\blends\b",                    "उधार देता है"),
    (r"\blend\b",                     "उधार देना"),
    (r"\blent\b",                     "उधार दिया"),
    (r"\bborrows\b",                  "उधार लेता है"),
    (r"\bborrow\b",                   "उधार लेना"),
    (r"\bborrowed\b",                 "उधार लिया"),
    (r"\bchange\b",                   "बदलाव"),
    (r"\bchanges\b",                  "बदलाव"),
    (r"\bchanged\b",                  "बदला"),
    (r"\bperspective\b",              "दृष्टिकोण"),
    (r"\bbright\b",                   "उज्ज्वल"),
    (r"\bdark\b",                     "अँधेरा"),
    (r"\bdifficult\b",                "कठिन"),
    (r"\beasy\b",                     "आसान"),
    (r"\bkind\b",                     "दयालु"),
    (r"\bsense\b",                    "अर्थ"),
    (r"\bmeaning\b",                  "अर्थ"),
    (r"\bmeat\b",                     "मांस"),
    (r"\bdinner\b",                   "रात का खाना"),
    (r"\bbreakfast\b",                "नाश्ता"),
    (r"\blunch\b",                    "दोपहर का खाना"),
    (r"\bdelicious\b",                "स्वादिष्ट"),
    (r"\btests\b",                    "परखता है"),
    (r"\btest\b",                     "परीक्षण"),
    (r"\btested\b",                   "परीक्षण किया"),
    (r"\bkeep\b",                     "रखना"),
    (r"\bkeeps\b",                    "रखता है"),
    (r"\bkept\b",                     "रखा"),
    (r"\boldest\b",                   "सबसे पुराना"),
    (r"\byoungest\b",                 "सबसे छोटा"),
    (r"\bsequential\b",               "क्रमिक"),
    (r"\bnumeric\b",                  "संख्यात्मक"),
    (r"\bnumeral\b",                  "अंक"),

    # JLPT-pedagogical terms
    (r"\binvite\b",                   "आमंत्रित करना"),
    (r"\binvited\b",                  "आमंत्रित"),
    (r"\binvitation\b",               "आमंत्रण"),
    (r"\binviting\b",                  "आमंत्रित करते हुए"),
    (r"\bplus\b",                     "के साथ"),
    (r"\bminus\b",                    "के बिना"),
    (r"\bsubject's\b",                "कर्ता का"),
    (r"\bspeaker's\b",                "वक्ता का"),
    (r"\blistener's\b",               "श्रोता का"),
    (r"\bobject's\b",                 "वस्तु का"),
    (r"\bowner's\b",                  "स्वामी का"),
    (r"\bmaintain\b",                 "बनाए रखना"),
    (r"\bmaintains\b",                "बनाए रखता है"),
    (r"\bmaintained\b",               "बनाए रखा गया"),
    (r"\breinforces\b",               "पुष्ट करता है"),
    (r"\breinforce\b",                "पुष्ट करना"),
    (r"\bcovers\b",                   "शामिल करता है"),
    (r"\bcover\b",                    "शामिल करना"),
    (r"\bcovered\b",                  "शामिल किया गया"),
    (r"\bdrop\b",                     "हटाना"),
    (r"\bdrops\b",                    "हटाता है"),
    (r"\bdropped\b",                  "हटाया"),
    (r"\bdropping\b",                 "हटाते हुए"),
    (r"\badd\b",                      "जोड़ना"),
    (r"\badds\b",                     "जोड़ता है"),
    (r"\badded\b",                    "जोड़ा गया"),
    (r"\battaches\b",                 "जुड़ता है"),
    (r"\battach\b",                   "जोड़ना"),
    (r"\battached\b",                 "जुड़ा हुआ"),
    (r"\bbefore\b",                   "पहले"),
    (r"\bafter\b",                    "बाद"),
    (r"\bcommon\b",                   "सामान्य"),
    (r"\bmost common\b",              "सबसे आम"),
    (r"\bcommon mistake\b",           "सामान्य ग़लती"),
    (r"\brule\b",                     "नियम"),
    (r"\brules\b",                    "नियम"),
    (r"\bregular rule\b",             "नियमित नियम"),

    # 'of' contexts (avoid double substitution from earlier)
    (r"\bonset of\b",                 "आरंभ"),
    (r"\bend of\b",                   "अंत"),
    (r"\btype of\b",                  "का प्रकार"),
    (r"\bkind of\b",                  "का प्रकार"),

    # Fillers
    (r"\bnote\b",                     "नोट"),
    (r"\bnotes\b",                    "नोट"),
    (r"\bnoted\b",                    "नोट किया"),
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


def main():
    total_changes = 0
    files_changed = 0
    by_file = defaultdict(int)

    qpath = ROOT / 'data' / 'questions.json'
    qdata = json.loads(qpath.read_text(encoding='utf-8'))
    for q in qdata.get('questions', []):
        eh = q.get('explanation_hi')
        if eh:
            new_val, changes = apply_subs(eh)
            if changes:
                q['explanation_hi'] = new_val
                total_changes += 1
                by_file['questions.json'] += 1
        de_hi = q.get('distractor_explanations_hi') or {}
        if isinstance(de_hi, dict):
            for k in list(de_hi.keys()):
                v = de_hi[k]
                if isinstance(v, str):
                    new_val, changes = apply_subs(v)
                    if changes:
                        de_hi[k] = new_val
                        total_changes += 1
                        by_file['questions.json'] += 1
    if by_file['questions.json']:
        qpath.write_text(json.dumps(qdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        files_changed += 1

    gpath = ROOT / 'data' / 'grammar.json'
    gdata = json.loads(gpath.read_text(encoding='utf-8'))
    for p in gdata.get('patterns', []):
        for fld in ('meaning_hi', 'explanation_hi'):
            v = p.get(fld)
            if isinstance(v, str):
                new_val, changes = apply_subs(v)
                if changes:
                    p[fld] = new_val
                    total_changes += 1
                    by_file['grammar.json'] += 1
        l1n = p.get('l1_notes')
        if isinstance(l1n, dict) and isinstance(l1n.get('hi'), str):
            new_val, changes = apply_subs(l1n['hi'])
            if changes:
                l1n['hi'] = new_val
                total_changes += 1
                by_file['grammar.json'] += 1
    if by_file['grammar.json']:
        gpath.write_text(json.dumps(gdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        files_changed += 1

    for pf in (ROOT / 'data' / 'papers').rglob('*.json'):
        if pf.name == 'manifest.json':
            continue
        pdata = json.loads(pf.read_text(encoding='utf-8'))
        local_changes = 0
        for q in pdata.get('questions', []):
            v = q.get('rationale_hi')
            if isinstance(v, str):
                new_val, changes = apply_subs(v)
                if changes:
                    q['rationale_hi'] = new_val
                    local_changes += 1
        for p in pdata.get('passages', []):
            v = p.get('summary_hi')
            if isinstance(v, str):
                new_val, changes = apply_subs(v)
                if changes:
                    p['summary_hi'] = new_val
                    local_changes += 1
        if local_changes:
            pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            files_changed += 1
            total_changes += local_changes
            by_file[f'papers/{pf.parent.name}/{pf.name}'] += local_changes

    print(f"\nTotal entries changed: {total_changes}")
    print(f"Files changed: {files_changed}")


if __name__ == '__main__':
    main()
