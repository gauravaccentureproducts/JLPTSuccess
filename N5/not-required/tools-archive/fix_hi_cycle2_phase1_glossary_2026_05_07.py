"""Cycle-2 Phase 1: comprehensive glossary expansion.

Walks all Hindi-bearing fields across questions.json, grammar.json,
listening.json, reading.json, and paper files. Applies a much-
expanded glossary covering the ~60 most-frequent residuals from
cycle 1.

Skip-list excludes structural fields (pos, type, label, etc.) -
romaji is intentional in those.

Run with --dry-run first.
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

# ============================================================================
# Glossary (multi-word phrases first, then single words)
# ============================================================================
RULES = [
    # ---- Multi-word phrases (longest match wins) ----
    (r"\bplace of action\b",            "क्रिया का स्थान"),
    (r"\blet's\b",                      "चलिए"),
    (r"\blet us\b",                     "चलिए"),
    (r"\bme too\b",                     "मैं भी"),
    (r"\bto be\b",                      "होना"),
    (r"\bquestion word\b",              "प्रश्न-शब्द"),
    (r"\bquestion words\b",             "प्रश्न-शब्द"),
    (r"\bsingle point\b",               "एकल बिंदु"),
    (r"\bend-point\b",                  "अंत-बिंदु"),
    (r"\bend point\b",                  "अंत-बिंदु"),
    (r"\bstarting point\b",             "प्रारंभ-बिंदु"),
    (r"\bdirect lexical equivalence\b", "सीधी शाब्दिक समानता"),
    (r"\bgrammatical pair\b",           "व्याकरणिक जोड़ी"),
    (r"\bregular rule\b",               "नियमित नियम"),
    (r"\birregular form\b",             "अनियमित रूप"),
    (r"\bover-regularized\b",           "अति-नियमित"),
    (r"\bover-regularised\b",           "अति-नियमित"),
    (r"\bdoesn't follow\b",             "का पालन नहीं करता"),
    (r"\bdoes not follow\b",            "का पालन नहीं करता"),
    (r"\bisn't followed\b",             "के बाद नहीं आता"),
    (r"\bnot followed\b",               "के बाद नहीं आता"),
    (r"\bcalls for\b",                  "की माँग करता है"),
    (r"\bin (the )?speaker's hand\b",   "वक्ता के हाथ में"),
    (r"\bin (the )?listener's hand\b",  "श्रोता के हाथ में"),
    (r"\bcomplete absence\b",           "पूर्ण अनुपस्थिति"),
    (r"\bevery day\b",                  "हर दिन"),
    (r"\beach day\b",                   "हर दिन"),
    (r"\bevery week\b",                 "हर हफ़्ते"),
    (r"\blast week\b",                  "पिछले हफ़्ते"),
    (r"\bnext week\b",                  "अगले हफ़्ते"),
    (r"\blast year\b",                  "पिछले साल"),
    (r"\bnext year\b",                  "अगले साल"),
    (r"\bnext month\b",                 "अगले महीने"),
    (r"\bevery year\b",                 "हर साल"),
    (r"\bevery month\b",                "हर महीने"),

    # ---- Verbs (base) ----
    (r"\bgoes\b",        "जाता है"),
    (r"\bgo\b",          "जाना"),
    (r"\bwent\b",        "गया"),
    (r"\bgone\b",        "गया"),
    (r"\bgoing\b",       "जा रहा"),
    (r"\bcomes\b",       "आता है"),
    (r"\bcome\b",        "आना"),
    (r"\bcame\b",        "आया"),
    (r"\bcoming\b",      "आ रहा"),
    (r"\basks\b",        "पूछता है"),
    (r"\bask\b",         "पूछना"),
    (r"\basked\b",       "पूछा"),
    (r"\basking\b",      "पूछते हुए"),
    (r"\bsays\b",        "कहता है"),
    (r"\bsay\b",         "कहना"),
    (r"\bsaid\b",        "कहा"),
    (r"\btells\b",       "बताता है"),
    (r"\btell\b",        "बताना"),
    (r"\btold\b",        "बताया"),
    (r"\bgives\b",       "देता है"),
    (r"\bgive\b",        "देना"),
    (r"\bgave\b",        "दिया"),
    (r"\bgiven\b",       "दिया गया"),
    (r"\bgets\b",        "पाता है"),
    (r"\bget\b",         "पाना"),
    (r"\bgot\b",         "पाया"),
    (r"\bsees\b",        "देखता है"),
    (r"\bsee\b",         "देखना"),
    (r"\bsaw\b",         "देखा"),
    (r"\bseen\b",        "देखा गया"),
    (r"\breads\b",       "पढ़ता है"),
    (r"\bread\b",        "पढ़ना"),
    (r"\bwrites\b",      "लिखता है"),
    (r"\bwrite\b",       "लिखना"),
    (r"\bwrote\b",       "लिखा"),
    (r"\bwritten\b",     "लिखा गया"),
    (r"\bdrops\b",       "गिराता है"),
    (r"\bdrop\b",        "हटाना"),
    (r"\bdropped\b",     "हटाया"),
    (r"\bdropping\b",    "हटाते हुए"),
    (r"\bstacks\b",      "ढेर लगाता है"),
    (r"\bstack\b",       "ढेर"),
    (r"\bfollows\b",     "का पालन करता है"),
    (r"\bfollow\b",      "का पालन"),
    (r"\bfollowed\b",    "के बाद आया"),
    (r"\breplaces\b",    "की जगह लेता है"),
    (r"\breplace\b",     "की जगह"),
    (r"\bcontradicts\b", "के विपरीत है"),
    (r"\bcontradict\b",  "विरोधाभास"),
    (r"\bcontradicting\b","विरोधाभासी"),
    (r"\btopicalize\b",  "विषय बनाना"),
    (r"\bemphasize\b",   "ज़ोर देता है"),
    (r"\bemphasizes\b",  "ज़ोर देता है"),
    (r"\bestablished\b", "स्थापित"),
    (r"\bestablish\b",   "स्थापित करना"),
    (r"\bexpressed\b",   "व्यक्त किया"),
    (r"\bexpresses\b",   "व्यक्त करता है"),
    (r"\bexpress\b",     "व्यक्त"),
    (r"\bdescribes\b",   "वर्णित"),
    (r"\bdescribe\b",    "वर्णित करना"),
    (r"\bdescribed\b",   "वर्णित"),
    (r"\bintroduce\b",   "प्रस्तुत"),
    (r"\bintroduces\b",  "प्रस्तुत करता है"),
    (r"\bcalled\b",      "कहलाता"),
    (r"\bcalls\b",       "बुलाता है"),
    (r"\bshown\b",       "दिखाया गया"),
    (r"\bshowing\b",     "दिखाते हुए"),
    (r"\bshows\b",       "दिखाता है"),
    (r"\bshow\b",        "दिखाना"),
    (r"\bbought\b",      "ख़रीदा"),
    (r"\bbuy\b",         "ख़रीदना"),
    (r"\beat\b",         "खाना"),
    (r"\bate\b",         "खाया"),
    (r"\bdrank\b",       "पिया"),
    (r"\bdrink\b",       "पीना"),
    (r"\bplay\b",        "खेलना"),
    (r"\bplayed\b",      "खेला"),
    (r"\bsleep\b",       "सोना"),
    (r"\bslept\b",       "सोया"),
    (r"\bbecome\b",      "बनना"),
    (r"\bbecomes\b",     "बनता है"),
    (r"\bbecame\b",      "बना"),
    (r"\bsearch\b",      "खोज"),

    # ---- Common nouns ----
    (r"\bpattern\b",     "पैटर्न"),
    (r"\border\b",       "क्रम"),
    (r"\bchoice\b",      "विकल्प"),
    (r"\bchoices\b",     "विकल्प"),
    (r"\bdetail\b",      "विवरण"),
    (r"\bdetails\b",     "विवरण"),
    (r"\bday\b",         "दिन"),
    (r"\bweek\b",        "हफ़्ता"),
    (r"\bmonth\b",       "महीना"),
    (r"\byear\b",        "वर्ष"),
    (r"\bnoun\b",        "संज्ञा"),
    (r"\bnouns\b",       "संज्ञाएँ"),
    (r"\bbook\b",        "किताब"),
    (r"\bbooks\b",       "किताबें"),
    (r"\bfriend\b",      "दोस्त"),
    (r"\bfriends\b",     "दोस्त"),
    (r"\bfather\b",      "पिता"),
    (r"\bmother\b",      "माता"),
    (r"\bparents\b",     "माता-पिता"),
    (r"\bperson\b",      "व्यक्ति"),
    (r"\bpeople\b",      "लोग"),
    (r"\breason\b",      "कारण"),
    (r"\bresult\b",      "परिणाम"),
    (r"\bcontext\b",     "संदर्भ"),
    (r"\bstatement\b",   "कथन"),
    (r"\bquestion\b",    "प्रश्न"),
    (r"\bquestions\b",   "प्रश्न"),
    (r"\banswer\b",      "उत्तर"),
    (r"\bspeaker\b",     "वक्ता"),
    (r"\blistener\b",    "श्रोता"),
    (r"\bobject\b",      "वस्तु"),
    (r"\bobjects\b",     "वस्तुएँ"),
    (r"\bsubject\b",     "विषय"),
    (r"\boption\b",      "विकल्प"),
    (r"\boptions\b",     "विकल्प"),
    (r"\brange\b",       "श्रेणी"),
    (r"\bpoint\b",       "बिंदु"),
    (r"\bslot\b",        "स्थान"),
    (r"\brecipient\b",   "प्राप्तकर्ता"),
    (r"\bgiver\b",       "दाता"),
    (r"\bcompanion\b",   "साथी"),
    (r"\bhabit\b",       "अभ्यास"),
    (r"\bhead\b",        "सिर"),
    (r"\btime\b",        "समय"),
    (r"\bplace\b",       "जगह"),
    (r"\bevent\b",       "घटना"),
    (r"\bnumber\b",      "संख्या"),
    (r"\bword\b",        "शब्द"),
    (r"\bwords\b",       "शब्द"),
    (r"\bsentence\b",    "वाक्य"),
    (r"\bsentences\b",   "वाक्य"),
    (r"\bclause\b",      "उपवाक्य"),
    (r"\bphrase\b",      "वाक्यांश"),
    (r"\bphrases\b",     "वाक्यांश"),
    (r"\bmovie\b",       "फ़िल्म"),
    (r"\bcollege\b",     "कॉलेज"),
    (r"\bschool\b",      "स्कूल"),
    (r"\bstudent\b",     "छात्र"),
    (r"\bstudents\b",    "छात्र"),
    (r"\bteacher\b",     "शिक्षक"),
    (r"\bhouse\b",       "घर"),
    (r"\bhome\b",        "घर"),
    (r"\broom\b",        "कमरा"),
    (r"\bpark\b",        "पार्क"),
    (r"\bcity\b",        "शहर"),
    (r"\bworld\b",       "दुनिया"),
    (r"\bcountry\b",     "देश"),
    (r"\bmovie\b",       "फ़िल्म"),
    (r"\brecurrence\b",  "पुनरावृत्ति"),
    (r"\bfrequency\b",   "आवृत्ति"),
    (r"\bpredicate\b",   "विधेय"),
    (r"\bnegation\b",    "नकार"),
    (r"\bequivalence\b", "समानता"),
    (r"\bequivalent\b",  "समकक्ष"),
    (r"\bnominalizer\b", "नामकरण-कण"),
    (r"\bdegree adverb\b", "मात्रा-क्रियाविशेषण"),
    (r"\bdegree\b",      "मात्रा"),

    # ---- Adjectives / adverbs ----
    (r"\bsame\b",        "समान"),
    (r"\bdifferent\b",   "अलग"),
    (r"\bsimilar\b",     "समान"),
    (r"\bnew\b",         "नया"),
    (r"\bold\b",         "पुराना"),
    (r"\bbig\b",         "बड़ा"),
    (r"\bsmall\b",       "छोटा"),
    (r"\bgood\b",        "अच्छा"),
    (r"\bbad\b",         "बुरा"),
    (r"\bstrong\b",      "सख़्त"),
    (r"\bweak\b",        "कमज़ोर"),
    (r"\bnatural\b",     "स्वाभाविक"),
    (r"\bunnatural\b",   "अस्वाभाविक"),
    (r"\bcorrect\b",     "सही"),
    (r"\bincorrect\b",   "ग़लत"),
    (r"\bwrong\b",       "ग़लत"),
    (r"\bgrammatical\b", "व्याकरणिक"),
    (r"\bungrammatical\b","अव्याकरणिक"),
    (r"\bregular\b",     "नियमित"),
    (r"\birregular\b",   "अनियमित"),
    (r"\bdirect\b",      "सीधा"),
    (r"\bindirect\b",    "अप्रत्यक्ष"),
    (r"\bspecific\b",    "विशिष्ट"),
    (r"\bgeneral\b",     "सामान्य"),
    (r"\bdefinite\b",    "निश्चित"),
    (r"\bindefinite\b",  "अनिश्चित"),
    (r"\bcomplete\b",    "पूर्ण"),
    (r"\bincomplete\b",  "अपूर्ण"),
    (r"\bcommon\b",      "सामान्य"),
    (r"\brare\b",        "दुर्लभ"),
    (r"\bnear\b",        "नज़दीक"),
    (r"\bfar\b",         "दूर"),
    (r"\bother\b",       "अन्य"),
    (r"\bothers\b",      "अन्य"),
    (r"\bfocused\b",     "केंद्रित"),
    (r"\bselected\b",    "चयनित"),
    (r"\bfilled\b",      "भरा हुआ"),
    (r"\bempty\b",       "ख़ाली"),
    (r"\babsent\b",      "अनुपस्थित"),
    (r"\bpresent\b",     "उपस्थित"),
    (r"\bonce\b",        "एक बार"),
    (r"\btwice\b",       "दो बार"),
    (r"\bagain\b",       "फिर"),
    (r"\bjust\b",        "केवल"),
    (r"\balone\b",       "अकेला"),
    (r"\btogether\b",    "साथ"),
    (r"\bboth\b",        "दोनों"),
    (r"\beither\b",      "या तो"),
    (r"\bany\b",         "कोई"),
    (r"\bevery\b",       "हर"),
    (r"\beach\b",        "हर"),

    # ---- Modal / aspect verbs ----
    (r"\bcannot\b",      "नहीं कर सकता"),
    (r"\bcan't\b",       "नहीं कर सकता"),
    (r"\bcan\b",         "सकता है"),
    (r"\bcould\b",       "सकता था"),
    (r"\bshould\b",      "चाहिए"),
    (r"\bshouldn't\b",   "नहीं चाहिए"),
    (r"\bmust\b",        "अवश्य"),
    (r"\bmustn't\b",     "नहीं करना चाहिए"),
    (r"\bmight\b",       "सकता है"),
    (r"\bmay\b",         "सकता है"),
    (r"\bwon't\b",       "नहीं होगा"),
    (r"\bwill not\b",    "नहीं होगा"),
    (r"\bwill\b",        "होगा"),
    (r"\bwould\b",       "होगा"),
    (r"\bwant\b",        "चाहना"),
    (r"\bwants\b",       "चाहता है"),
    (r"\bwanted\b",      "चाहा"),
    (r"\bdesire\b",      "इच्छा"),
    (r"\bneed\b",        "ज़रूरत"),
    (r"\bneeded\b",      "ज़रूरी"),
    (r"\bneeds\b",       "ज़रूरत है"),

    # ---- Connectors / glue ----
    (r"\bamong\b",       "के बीच"),
    (r"\bbetween\b",     "के बीच"),
    (r"\bagainst\b",     "के विरुद्ध"),
    (r"\bafter\b",       "बाद"),
    (r"\bbefore\b",      "पहले"),
    (r"\bduring\b",      "के दौरान"),
    (r"\bsince\b",       "से"),
    (r"\bwhile\b",       "जबकि"),
    (r"\bunless\b",      "जब तक नहीं"),
    (r"\binstead\b",     "इसके बजाय"),
    (r"\bnext\b",        "अगला"),
    (r"\bprior\b",       "पूर्व"),
    (r"\bprevious\b",    "पिछला"),
    (r"\bcurrent\b",     "वर्तमान"),
    (r"\blet\b",         "करने दें"),
    (r"\bmean\b",        "मतलब"),
    (r"\bmeans\b",       "साधन"),
    (r"\bmeaning\b",     "अर्थ"),
    (r"\bconnect\b",     "जोड़ना"),
    (r"\bconnects\b",    "जोड़ता है"),
    (r"\bconnector\b",   "जोड़क"),
    (r"\bconnecting\b",  "जोड़ने वाला"),
    (r"\bconstruction\b","रचना"),
    (r"\bbuild\b",       "बनाना"),
    (r"\bbuilt\b",       "बना हुआ"),
    (r"\binto\b",        "में"),

    # ---- Numbers ----
    (r"\btwo\b",         "दो"),
    (r"\bthree\b",       "तीन"),
    (r"\bfour\b",        "चार"),
    (r"\bfive\b",        "पाँच"),
    (r"\bsix\b",         "छह"),
    (r"\bseven\b",       "सात"),
    (r"\beight\b",       "आठ"),
    (r"\bnine\b",        "नौ"),
    (r"\bten\b",         "दस"),

    # ---- Pedagogical pivots already in use; reinforce ----
    (r"\bpermission\b",  "अनुमति"),
    (r"\bprobability\b", "सम्भावना"),
    (r"\bpossibility\b", "सम्भावना"),
    (r"\bpossession\b",  "स्वामित्व"),
    (r"\bownership\b",   "स्वामित्व"),
    (r"\bcompanionship\b", "साथ"),
    (r"\bsuggestion\b",  "सुझाव"),
    (r"\binvitation\b",  "आमंत्रण"),
    (r"\brequest\b",     "अनुरोध"),
    (r"\badvice\b",      "सलाह"),
    (r"\binstruction\b", "निर्देश"),
    (r"\bexplanation\b", "व्याख्या"),
    (r"\bvocabulary\b",  "शब्दावली"),
    (r"\bgrammar\b",     "व्याकरण"),
    (r"\bmedium\b",      "माध्यम"),

    # ---- Final residual sweep ----
    (r"\babsence\b",     "अनुपस्थिति"),
    (r"\boccurrence\b",  "घटना"),
    (r"\bunique\b",      "अनोखा"),
    (r"\bvalid\b",       "मान्य"),
    (r"\bvariant\b",     "रूपांतर"),
    (r"\bversion\b",     "संस्करण"),
    (r"\bbase\b",        "मूल"),
    (r"\borigin\b",      "मूल"),
    (r"\boriginal\b",    "मूल"),
    (r"\binner\b",       "आंतरिक"),
    (r"\bouter\b",       "बाहरी"),
    (r"\bsmoothly\b",    "सहजता से"),
    (r"\bsmooth\b",      "सहज"),

    # ---- Pronouns & determiners ----
    (r"\bI\b",           "मैं"),
    (r"\bmy\b",          "मेरा"),
    (r"\bme\b",          "मुझे"),
    (r"\byour\b",        "आपका"),
    (r"\byou\b",         "आप"),
    (r"\bhis\b",         "उसका"),
    (r"\bher\b",         "उसका"),
    (r"\bhim\b",         "उसे"),
    (r"\bher\b",         "उसे"),
    (r"\bone\b",         "एक"),
    (r"\bsomething\b",   "कुछ"),
    (r"\beverything\b",  "सब कुछ"),
    (r"\bnothing\b",     "कुछ नहीं"),
    (r"\beveryone\b",    "हर कोई"),
    (r"\bsomeone\b",     "कोई"),
    (r"\bno one\b",      "कोई नहीं"),

    # ---- Final connector + boilerplate ----
    (r"\bsince\b",       "से"),
    (r"\balthough\b",    "हालाँकि"),
    (r"\bhowever\b",     "हालाँकि"),
    (r"\bmoreover\b",    "इसके अलावा"),
    (r"\bfurthermore\b", "इसके अलावा"),
    (r"\btherefore\b",   "इसलिए"),
    (r"\bthus\b",        "इस तरह"),
    (r"\babout\b",       "के बारे में"),
    (r"\bintroduce\b",   "प्रस्तुत करना"),
    (r"\bregardless\b",  "की परवाह किए बिना"),
    (r"\bdespite\b",     "के बावजूद"),

    # ---- Articles + simple gluewords ----
    (r"\bthe\b",         ""),
    (r"\ba\b",           ""),
    (r"\ban\b",          ""),

    # ---- 'is/are/was/were' (after specific phrases handled above) ----
    (r"\bis\b",          "है"),
    (r"\bare\b",         "हैं"),
    (r"\bwas\b",         "था"),
    (r"\bwere\b",        "थे"),

    # Helpers
    (r"\byes\b",         "हाँ"),
    (r"\bno\b",          "नहीं"),
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    files_changed = 0
    total_changes = 0
    by_file = defaultdict(int)

    # questions.json
    qpath = ROOT / 'data' / 'questions.json'
    qdata = json.loads(qpath.read_text(encoding='utf-8'))
    for q in qdata.get('questions', []):
        eh = q.get('explanation_hi')
        if eh:
            new_val, changes = apply_subs(eh)
            if changes:
                if not args.dry_run:
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
                        if not args.dry_run:
                            de_hi[k] = new_val
                        total_changes += 1
                        by_file['questions.json'] += 1
    if not args.dry_run and by_file['questions.json']:
        qpath.write_text(json.dumps(qdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        files_changed += 1

    # grammar.json
    gpath = ROOT / 'data' / 'grammar.json'
    gdata = json.loads(gpath.read_text(encoding='utf-8'))
    for p in gdata.get('patterns', []):
        for fld in ('meaning_hi', 'explanation_hi'):
            v = p.get(fld)
            if isinstance(v, str):
                new_val, changes = apply_subs(v)
                if changes:
                    if not args.dry_run:
                        p[fld] = new_val
                    total_changes += 1
                    by_file['grammar.json'] += 1
        l1n = p.get('l1_notes')
        if isinstance(l1n, dict) and isinstance(l1n.get('hi'), str):
            new_val, changes = apply_subs(l1n['hi'])
            if changes:
                if not args.dry_run:
                    l1n['hi'] = new_val
                total_changes += 1
                by_file['grammar.json'] += 1
    if not args.dry_run and by_file['grammar.json']:
        gpath.write_text(json.dumps(gdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        files_changed += 1

    # paper files
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
                    if not args.dry_run:
                        q['rationale_hi'] = new_val
                    local_changes += 1
        for p in pdata.get('passages', []):
            v = p.get('summary_hi')
            if isinstance(v, str):
                new_val, changes = apply_subs(v)
                if changes:
                    if not args.dry_run:
                        p['summary_hi'] = new_val
                    local_changes += 1
        if local_changes and not args.dry_run:
            pf.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            files_changed += 1
        total_changes += local_changes
        if local_changes:
            by_file[f'papers/{pf.parent.name}/{pf.name}'] += local_changes

    print(f"\nTotal entries changed: {total_changes}")
    print(f"Files changed: {files_changed}")
    print(f"\nBy file (top 15):")
    for f, c in sorted(by_file.items(), key=lambda x: -x[1])[:15]:
        print(f'  {f}: {c}')


if __name__ == '__main__':
    main()
