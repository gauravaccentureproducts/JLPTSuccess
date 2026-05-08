"""HI-02 round 2: sweep code-mix in questions.json after the placeholder
translations introduced new Hindi text with residual English words.

Reuses the HI-04 grammar glossary + adds a few more terms specific to
questions.json prose (emphasize, specifically, natural, etc.).
"""
from __future__ import annotations
import argparse
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

QUESTIONS = ROOT / 'data' / 'questions.json'

# Comprehensive glossary - from HI-04 + question-specific additions
SUBSTITUTIONS = [
    # Multi-word phrases first
    (r"\bcommon mistake\b", "सामान्य ग़लती"),
    (r"\bless natural\b", "कम स्वाभाविक"),
    (r"\bmore natural\b", "अधिक स्वाभाविक"),
    (r"\bvery polite\b", "बहुत विनम्र"),
    (r"\bnot natural\b", "स्वाभाविक नहीं"),
    (r"\bstarting point\b", "प्रारंभ-बिंदु"),
    (r"\bend point\b", "अंत-बिंदु"),
    (r"\bdirect object\b", "सीधा कर्म"),
    (r"\bindirect object\b", "अप्रत्यक्ष कर्म"),
    (r"\bnew info\b", "नई जानकारी"),
    (r"\bknown info\b", "ज्ञात जानकारी"),
    (r"\bquestion word\b", "प्रश्न-शब्द"),
    (r"\btopic-marker\b", "विषय-सूचक"),
    (r"\btopic\b", "विषय"),
    (r"\bin the room\b", "कमरे में"),
    (r"\bat the park\b", "पार्क में"),
    (r"\bthrough the park\b", "पार्क से"),
    (r"\bvisible to\b", "दिखता है"),
    (r"\bclassifier\b", "वर्गीकारक"),

    # Connectors and structure
    (r"\bemphasize\b", "ज़ोर देता है"),
    (r"\bemphasizes\b", "ज़ोर देता है"),
    (r"\bemphasized\b", "ज़ोर दिया गया"),
    (r"\bspecifically\b", "विशेष रूप से"),
    (r"\bnatural\b", "स्वाभाविक"),
    (r"\bunnatural\b", "अस्वाभाविक"),
    (r"\bnatural-ish\b", "स्वाभाविक-सा"),
    (r"\bpassive-ish\b", "कर्मवाच्य-सा"),
    (r"\bpassive\b", "कर्मवाच्य"),
    (r"\bactive\b", "कर्तृवाच्य"),
    (r"\bstative\b", "स्थिर"),
    (r"\bdynamic\b", "गतिशील"),
    (r"\bnegation\b", "नकार"),
    (r"\bnegated\b", "नकारात्मक"),
    (r"\binformation\b", "जानकारी"),
    (r"\binfo\b", "जानकारी"),
    (r"\bappear\b", "आ सकता है"),
    (r"\bappears\b", "आता है"),
    (r"\btakes\b", "लेता है"),
    (r"\bgives\b", "देता है"),
    (r"\boften\b", "अक्सर"),
    (r"\busually\b", "आम तौर पर"),
    (r"\bsometimes\b", "कभी-कभी"),
    (r"\bnever\b", "कभी नहीं"),
    (r"\balways\b", "हमेशा"),
    (r"\boriginally\b", "मूल रूप से"),
    (r"\boriginal\b", "मूल"),
    (r"\borigin\b", "मूल"),
    (r"\bsource\b", "स्रोत"),

    # Comparatives
    (r"\bless\b", "कम"),
    (r"\bmore\b", "अधिक"),
    (r"\bvery\b", "बहुत"),
    (r"\btoo\b", "बहुत ज़्यादा"),
    (r"\benough\b", "पर्याप्त"),

    # Verb forms
    (r"\buse\b", "प्रयोग"),
    (r"\buses\b", "प्रयोग करता है"),
    (r"\bused\b", "प्रयोग किया गया"),
    (r"\bgoing\b", "जा रहा है"),
    (r"\bgo\b", "जाना"),
    (r"\bgone\b", "गया"),
    (r"\bcame\b", "आया"),
    (r"\bcomes\b", "आता है"),
    (r"\bcome\b", "आना"),
    (r"\bsays\b", "कहता है"),
    (r"\bsay\b", "कहना"),
    (r"\bsaid\b", "कहा"),
    (r"\bdoes\b", "करता है"),
    (r"\bdo\b", "करना"),
    (r"\bdid\b", "किया"),
    (r"\bdone\b", "किया गया"),
    (r"\bbe\b", "होना"),
    (r"\bbeing\b", "होते हुए"),
    (r"\bbeen\b", "रहा"),
    (r"\bhas\b", "के पास है"),
    (r"\bhave\b", "के पास है"),
    (r"\bhad\b", "के पास था"),
    (r"\bbuy\b", "ख़रीदना"),
    (r"\bbought\b", "ख़रीदा"),
    (r"\beat\b", "खाना"),
    (r"\bate\b", "खाया"),
    (r"\bplay\b", "खेलना"),
    (r"\bplayed\b", "खेला"),
    (r"\bwalk\b", "टहलना"),
    (r"\bwalked\b", "टहला"),
    (r"\bsee\b", "देखना"),
    (r"\bsaw\b", "देखा"),
    (r"\bdrink\b", "पीना"),
    (r"\bdrank\b", "पिया"),

    # Common nouns
    (r"\bword\b", "शब्द"),
    (r"\bwords\b", "शब्द"),
    (r"\bsentence\b", "वाक्य"),
    (r"\bquestion\b", "प्रश्न"),
    (r"\banswer\b", "उत्तर"),
    (r"\bspeaker\b", "वक्ता"),
    (r"\blistener\b", "श्रोता"),
    (r"\bmarker\b", "सूचक"),
    (r"\bmark\b", "चिह्न"),
    (r"\bmarks\b", "सूचित करता है"),
    (r"\bplace\b", "जगह"),
    (r"\bperson\b", "व्यक्ति"),
    (r"\bpeople\b", "लोग"),
    (r"\bthing\b", "वस्तु"),
    (r"\bthings\b", "वस्तुएँ"),
    (r"\bevent\b", "घटना"),
    (r"\bnumber\b", "संख्या"),
    (r"\bform\b", "रूप"),
    (r"\btime\b", "समय"),
    (r"\bmoney\b", "पैसा"),

    # Pronouns
    (r"\bI\b", "मैं"),
    (r"\bmy\b", "मेरा"),
    (r"\bme\b", "मुझे"),
    (r"\byou\b", "आप"),
    (r"\byour\b", "आपका"),
    (r"\bone\b", "एक"),
    (r"\bsomething\b", "कुछ"),
    (r"\beverything\b", "सब कुछ"),
    (r"\bnothing\b", "कुछ नहीं"),
    (r"\bsomeone\b", "कोई"),
    (r"\beveryone\b", "हर कोई"),
    (r"\bno one\b", "कोई नहीं"),
    (r"\bwhere\b", "जहाँ"),
    (r"\bwhen\b", "जब"),
    (r"\bwhy\b", "क्यों"),
    (r"\bhow\b", "कैसे"),
    (r"\bwhat\b", "क्या"),
    (r"\bwho\b", "कौन"),
    (r"\bwhich\b", "जो"),

    # Logic / structure
    (r"\bbut\b", "पर"),
    (r"\band\b", "और"),
    (r"\bor\b", "या"),
    (r"\bso\b", "इसलिए"),
    (r"\bbecause\b", "क्योंकि"),
    (r"\bif\b", "अगर"),
    (r"\bthough\b", "हालाँकि"),
    (r"\bhowever\b", "हालाँकि"),
    (r"\balthough\b", "यद्यपि"),
    (r"\bwhile\b", "जबकि"),
    (r"\bunless\b", "जब तक नहीं"),
    (r"\binstead\b", "इसके बजाय"),
    (r"\binstead of\b", "के बजाय"),
    (r"\bnot\b", "नहीं"),
    (r"\bonly\b", "केवल"),
    (r"\balso\b", "भी"),
    (r"\beven\b", "भी"),

    # Demonstratives / determiners
    (r"\bthis\b", "यह"),
    (r"\bthat\b", "वह"),
    (r"\bthese\b", "ये"),
    (r"\bthose\b", "वे"),

    # Prepositions
    (r"\bin\b", "में"),
    (r"\bof\b", "का"),
    (r"\bfor\b", "के लिए"),
    (r"\bfrom\b", "से"),
    (r"\bto\b", "को"),
    (r"\bwith\b", "के साथ"),
    (r"\bat\b", "में"),
    (r"\bon\b", "पर"),
    (r"\babout\b", "के बारे में"),
    (r"\bbefore\b", "पहले"),
    (r"\bafter\b", "बाद"),
    (r"\bduring\b", "के दौरान"),

    # Forms
    (r"\bnon-past\b", "अभूत"),
    (r"\baffirmative\b", "सकारात्मक"),
    (r"\bnegative\b", "नकारात्मक"),
    (r"\bpolite\b", "विनम्र"),
    (r"\bcasual\b", "अनौपचारिक"),
    (r"\bformal\b", "औपचारिक"),
    (r"\bplain\b", "सादा"),
    (r"\bpresent\b", "वर्तमान"),
    (r"\bpast\b", "भूत"),
    (r"\bfuture\b", "भविष्य"),
    (r"\bhabitual\b", "अभ्यासगत"),
    (r"\bprogressive\b", "प्रगतिशील"),
    (r"\bperfect\b", "पूर्ण"),

    # JLPT pedagogical
    (r"\bstem\b", "तना"),
    (r"\bsubject\b", "कर्ता"),
    (r"\bobject\b", "कर्म"),
    (r"\bverb\b", "क्रिया"),
    (r"\bverbs\b", "क्रियाएँ"),
    (r"\badjective\b", "विशेषण"),
    (r"\bnoun\b", "संज्ञा"),
    (r"\bparticle\b", "कण"),
    (r"\bparticles\b", "कण"),
    (r"\bcounter\b", "काउंटर"),
    (r"\bcounters\b", "काउंटर"),
    (r"\bclause\b", "उपवाक्य"),
    (r"\blocation\b", "स्थान"),
    (r"\baction\b", "क्रिया-कर्म"),
    (r"\bdestination\b", "गंतव्य"),
    (r"\bdestinations\b", "गंतव्य"),
    (r"\bdirection\b", "दिशा"),
    (r"\bmovement\b", "गति"),
    (r"\bmotion\b", "गति"),
    (r"\bpath\b", "रास्ता"),
    (r"\bmeans\b", "साधन"),
    (r"\binstrument\b", "उपकरण"),
    (r"\bcompanion\b", "साथी"),
    (r"\bexistence\b", "अस्तित्व"),
    (r"\bgenitive\b", "सम्बंधसूचक"),

    # Articles to remove
    (r"\bthe\b", ""),
    (r"\ba\b", ""),
    (r"\ban\b", ""),
    (r"\bis\b", "है"),
    (r"\bare\b", "हैं"),
    (r"\bwas\b", "था"),
    (r"\bwere\b", "थे"),
    (r"\bwill\b", "होगा"),
    (r"\bwill be\b", "होगा"),
    (r"\bbeen\b", "रहा"),

    # Yes/No
    (r"\byes\b", "हाँ"),
    (r"\bno\b", "नहीं"),

    # Round-3 residuals (after questions.json sweep)
    (r"\bneither\b", "कोई भी नहीं"),
    (r"\bfits\b", "फ़िट होता है"),
    (r"\bfit\b", "फ़िट"),
    (r"\bfitted\b", "फ़िट हुआ"),
    (r"\basking\b", "पूछने"),
    (r"\bask\b", "पूछना"),
    (r"\basked\b", "पूछा"),
    (r"\btake\b", "लेना"),
    (r"\btook\b", "लिया"),
    (r"\btaking\b", "लेते हुए"),
    (r"\bknown\b", "ज्ञात"),
    (r"\btopics\b", "विषय"),
    (r"\bwon't\b", "नहीं होगा"),
    (r"\bwill not\b", "नहीं होगा"),
    (r"\bisn't\b", "नहीं है"),
    (r"\baren't\b", "नहीं हैं"),
    (r"\bwasn't\b", "नहीं था"),
    (r"\bweren't\b", "नहीं थे"),
    (r"\broom\b", "कमरा"),
    (r"\bhouse\b", "घर"),
    (r"\bschool\b", "स्कूल"),
    (r"\bpark\b", "पार्क"),
    (r"\bcity\b", "शहर"),
    (r"\bcountry\b", "देश"),
    (r"\bbecome\b", "बनना"),
    (r"\bbecomes\b", "बनता है"),
    (r"\bbecame\b", "बना"),
    (r"\bbring\b", "लाना"),
    (r"\bbrought\b", "लाया"),
    (r"\btalk\b", "बात करना"),
    (r"\btalked\b", "बात की"),
    (r"\bspeak\b", "बोलना"),
    (r"\bspoke\b", "बोला"),
    (r"\bwork\b", "काम"),
    (r"\bworks\b", "काम करता है"),
    (r"\bworked\b", "काम किया"),
    (r"\blive\b", "रहना"),
    (r"\blives\b", "रहता है"),
    (r"\blived\b", "रहा"),
    (r"\bmake\b", "बनाना"),
    (r"\bmade\b", "बनाया"),
    (r"\bmakes\b", "बनाता है"),
    (r"\bgive\b", "देना"),
    (r"\bgave\b", "दिया"),
    (r"\bgiven\b", "दिया गया"),
    (r"\bget\b", "पाना"),
    (r"\bgot\b", "पाया"),
    (r"\breceived\b", "प्राप्त हुआ"),
    (r"\breceive\b", "प्राप्त करना"),
    (r"\breceiver\b", "प्राप्तकर्ता"),
    (r"\bgiver\b", "दाता"),

    # More common words
    (r"\bgood\b", "अच्छा"),
    (r"\bbad\b", "बुरा"),
    (r"\bnice\b", "अच्छा"),
    (r"\bnew\b", "नया"),
    (r"\bold\b", "पुराना"),
    (r"\bbig\b", "बड़ा"),
    (r"\bsmall\b", "छोटा"),
    (r"\blong\b", "लम्बा"),
    (r"\bshort\b", "छोटा"),
    (r"\bhigh\b", "ऊँचा"),
    (r"\blow\b", "नीचा"),
    (r"\bhot\b", "गरम"),
    (r"\bcold\b", "ठंडा"),
    (r"\bfast\b", "तेज़"),
    (r"\bslow\b", "धीमा"),
    (r"\bnow\b", "अभी"),
    (r"\btoday\b", "आज"),
    (r"\byesterday\b", "कल"),
    (r"\btomorrow\b", "कल"),
    (r"\bevery\b", "हर"),
    (r"\beach\b", "हर"),

    # English question words (residuals)
    (r"\bphysical\b", "भौतिक"),
    (r"\bemotional\b", "भावनात्मक"),
    (r"\bspecific\b", "विशिष्ट"),
    (r"\bgeneral\b", "सामान्य"),
    (r"\bcorrect\b", "सही"),
    (r"\bincorrect\b", "ग़लत"),
    (r"\bwrong\b", "ग़लत"),
    (r"\bright\b", "सही"),
    (r"\btrue\b", "सच"),
    (r"\bfalse\b", "झूठ"),
    (r"\bvalid\b", "मान्य"),
    (r"\binvalid\b", "अमान्य"),

    # Articles, structure, glue
    (r"\bof course\b", "बेशक"),
    (r"\bof the\b", "का"),
    (r"\bbecause of\b", "की वजह से"),
    (r"\bas\b", "के रूप में"),
    (r"\blike\b", "के समान"),
    (r"\bsuch as\b", "जैसे"),
    (r"\beach other\b", "एक-दूसरे को"),

    # Final cleanup
    (r"\bUse\b", "प्रयोग करें"),
    (r"\bAll\b", "सब"),
    (r"\ball\b", "सब"),
    (r"\bany\b", "कोई"),
    (r"\bsome\b", "कुछ"),
    (r"\bmany\b", "कई"),
    (r"\bfew\b", "कुछ"),
]


def has_devanagari(s: str) -> bool:
    return any('ऀ' <= ch <= 'ॿ' for ch in s)


def apply_subs(value: str) -> tuple[str, int]:
    """Apply substitutions, protecting Japanese tokens + parens-English."""
    if not isinstance(value, str) or not has_devanagari(value):
        return value, 0

    # Protect Japanese
    JP = re.compile(r'[ぁ-ゖァ-ヺ一-龯]+')
    jp_protected = []

    def protect_jp(m):
        idx = len(jp_protected)
        jp_protected.append(m.group(0))
        return f'\x00JP{idx}\x00'

    text = JP.sub(protect_jp, value)

    # Protect parenthesized English
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

    # Apply substitutions
    changes = 0
    for pat, repl in SUBSTITUTIONS:
        before = text
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
        if text != before:
            changes += 1

    # Restore parens
    for i, c in enumerate(paren_protected):
        text = text.replace(f'\x00PR{i}\x00', c)
    # Restore Japanese
    for i, jp in enumerate(jp_protected):
        text = text.replace(f'\x00JP{i}\x00', jp)

    # Cleanup
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([।,;:.])', r'\1', text)
    text = re.sub(r'\.(\s|$)', r'।\1', text)
    text = text.strip()

    return text, changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    data = json.loads(QUESTIONS.read_text(encoding='utf-8'))
    items = data.get('questions', [])

    expl_changed = 0
    distractor_changed = 0

    for q in items:
        eh = q.get('explanation_hi')
        if isinstance(eh, str):
            new_val, changes = apply_subs(eh)
            if changes:
                if not args.dry_run:
                    q['explanation_hi'] = new_val
                expl_changed += 1

        de_hi = q.get('distractor_explanations_hi')
        if isinstance(de_hi, dict):
            for k in list(de_hi.keys()):
                v = de_hi[k]
                if isinstance(v, str):
                    new_val, changes = apply_subs(v)
                    if changes:
                        if not args.dry_run:
                            de_hi[k] = new_val
                        distractor_changed += 1

    if not args.dry_run:
        QUESTIONS.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8'
        )

    print(f'\nResults:')
    print(f'  explanation_hi entries changed:        {expl_changed}')
    print(f'  distractor_explanations_hi changed:    {distractor_changed}')


if __name__ == '__main__':
    main()
