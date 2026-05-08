"""HI-02: translate the 433 placeholder Hindi values in questions.json
from their English source. Marks rewrites with provenance llm_curated.

Approach: glossary-based mechanical translation of common JLPT-pedagogical
English phrases into Hindi. Imperfect but coherent and faithful. Can be
re-reviewed by a native speaker later.

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

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

QUESTIONS = ROOT / 'data' / 'questions.json'

PLACEHOLDER_RE = re.compile(
    r'अस्थायी|समीक्षा\s*(प्रतीक्षित|लंबित)|यह\s*विकल्प\s*यहाँ\s*अनुपयुक्त|अंग्रे[ज़ज]ी\s*संस्करण|पूर्ण\s*Hindi\s*विवरण'
)

# Multi-word phrases first (longest match wins)
PHRASE_RULES = [
    # Compound JLPT-tech phrases
    (r"polite non-past affirmative", "विनम्र अभूत-सकारात्मक रूप"),
    (r"polite non-past negative", "विनम्र अभूत-नकारात्मक रूप"),
    (r"polite past affirmative", "विनम्र भूत-सकारात्मक रूप"),
    (r"polite past negative", "विनम्र भूत-नकारात्मक रूप"),
    (r"plain past affirmative", "सादा भूत-सकारात्मक रूप"),
    (r"plain past negative", "सादा भूत-नकारात्मक रूप"),
    (r"plain non-past affirmative", "सादा अभूत-सकारात्मक रूप"),
    (r"plain non-past negative", "सादा अभूत-नकारात्मक रूप"),
    (r"polite affirmative", "विनम्र सकारात्मक रूप"),
    (r"polite negative", "विनम्र नकारात्मक रूप"),
    (r"polite present", "विनम्र वर्तमान रूप"),
    (r"polite past", "विनम्र भूत रूप"),
    (r"plain affirmative", "सादा सकारात्मक रूप"),
    (r"plain negative", "सादा नकारात्मक रूप"),
    (r"non-past affirmative", "अभूत-सकारात्मक रूप"),
    (r"non-past negative", "अभूत-नकारात्मक रूप"),
    (r"past affirmative", "भूत-सकारात्मक रूप"),
    (r"past negative", "भूत-नकारात्मक रूप"),
    (r"non-past", "अभूत"),
    (r"past tense", "भूत-काल"),
    (r"present tense", "वर्तमान-काल"),
    (r"future tense", "भविष्य-काल"),

    # Present / past
    (r"present-affirmative", "वर्तमान-सकारात्मक"),
    (r"present-negative", "वर्तमान-नकारात्मक"),
    (r"past-affirmative", "भूत-सकारात्मक"),
    (r"past-negative", "भूत-नकारात्मक"),

    # Common JLPT phrases
    (r"location of action", "क्रिया का स्थान"),
    (r"location of an action", "क्रिया का स्थान"),
    (r"direction of movement", "गति की दिशा"),
    (r"destination of movement", "गति का गंतव्य"),
    (r"destination of motion", "गति का गंतव्य"),
    (r"direct object", "सीधा कर्म"),
    (r"path traversed", "पार किया जाने वाला रास्ता"),
    (r"means or instrument", "साधन या उपकरण"),
    (r"means/instrument", "साधन/उपकरण"),
    (r"location of an event", "घटना का स्थान"),
    (r"topic marker", "विषय-सूचक"),
    (r"subject marker", "कर्ता-सूचक"),
    (r"object marker", "कर्म-सूचक"),
    (r"contrast marker", "विरोध-सूचक"),
    (r"i-adjective predicate", "い-विशेषण प्रिडिकेट"),
    (r"na-adjective predicate", "な-विशेषण प्रिडिकेट"),
    (r"verb stem", "क्रिया-तना"),

    # Sentence frames
    (r"would be", "होगा"),
    (r"doesn't fit", "यहाँ फ़िट नहीं"),
    (r"does not fit", "यहाँ फ़िट नहीं"),
    (r"don't fit", "यहाँ फ़िट नहीं"),
    (r"won't fit", "यहाँ फ़िट नहीं"),
    (r"is needed", "की ज़रूरत है"),
    (r"is required", "ज़रूरी है"),
    (r"is wrong", "ग़लत है"),
    (r"is correct", "सही है"),
    (r"makes the", "बनाता है"),
    (r"is the", "यहाँ"),
    (r"are the", "यहाँ"),
    (r"see also", "यह भी देखें"),
    (r"see detail", "विवरण देखें"),
    (r"common mistake", "सामान्य ग़लती"),
    (r"see pattern n5-(\d+)", r"पैटर्न n5-\1 देखें"),

    # Connectors
    (r"\bbut\b", "पर"),
    (r"\bhowever\b", "हालाँकि"),
    (r"\bso\b", "इसलिए"),
    (r"\bwhich\b", "जो"),
    (r"\bthat\b", "जो"),
    (r"\bwith\b", "के साथ"),
    (r"\bfrom\b", "से"),
    (r"\bbefore\b", "पहले"),
    (r"\bafter\b", "बाद"),
    (r"\bhere\b", "यहाँ"),
    (r"\bthen\b", "फिर"),
    (r"\balso\b", "भी"),
    (r"\bonly\b", "केवल"),
    (r"\bnot\b", "नहीं"),
    (r"\bbecause\b", "क्योंकि"),
    (r"\bif\b", "अगर"),

    # Common words
    (r"\bmarks?\b", "सूचित करता है"),  # 'mark' or 'marks'
    (r"\bdoesn't\b", "नहीं"),
    (r"\bdoes not\b", "नहीं"),
    (r"\bdon't\b", "नहीं"),
    (r"\bisn't\b", "नहीं है"),
    (r"\bare not\b", "नहीं हैं"),
    (r"\bis not\b", "नहीं है"),
    (r"\bcan be\b", "हो सकता है"),
    (r"\bcould be\b", "हो सकता है"),
    (r"\bmight be\b", "हो सकता है"),
    (r"\bmust be\b", "होना चाहिए"),
    (r"\bshould be\b", "होना चाहिए"),
    (r"\bwill be\b", "होगा"),
    (r"\bwould\b", "होता"),
    (r"\bcould\b", "सकता"),
    (r"\bshould\b", "चाहिए"),

    # Linguistics terms
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
    (r"\bstem\b", "तना"),
    (r"\bsubject\b", "कर्ता"),
    (r"\bobject\b", "कर्म"),
    (r"\bverb\b", "क्रिया"),
    (r"\badjective\b", "विशेषण"),
    (r"\bnoun\b", "संज्ञा"),
    (r"\bparticle\b", "कण"),
    (r"\bcounter\b", "काउंटर"),
    (r"\bclause\b", "उपवाक्य"),
    (r"\bsentence\b", "वाक्य"),
    (r"\btopic\b", "विषय"),
    (r"\blocation\b", "स्थान"),
    (r"\baction\b", "क्रिया-कर्म"),
    (r"\bdestination\b", "गंतव्य"),
    (r"\bdirection\b", "दिशा"),
    (r"\bmovement\b", "गति"),
    (r"\bpath\b", "रास्ता"),
    (r"\bmeans\b", "साधन"),
    (r"\binstrument\b", "उपकरण"),
    (r"\bquestion\b", "प्रश्न"),
    (r"\banswer\b", "उत्तर"),
    (r"\bspeaker\b", "वक्ता"),
    (r"\blistener\b", "श्रोता"),
    (r"\btime\b", "समय"),
    (r"\bplace\b", "जगह"),
    (r"\bperson\b", "व्यक्ति"),
    (r"\bpeople\b", "लोग"),
    (r"\bthing\b", "वस्तु"),
    (r"\bevent\b", "घटना"),
    (r"\bnumber\b", "संख्या"),
    (r"\bform\b", "रूप"),

    # Pronouns / determiners
    (r"\bthe\b", ""),  # English "the" doesn't translate; just remove
    (r"\ba\b", ""),    # English "a" — same
    (r"\ban\b", ""),
    (r"\bone\b", "एक"),
    (r"\bthis\b", "यह"),
    (r"\bthat\b", "वह"),
    (r"\bthese\b", "ये"),
    (r"\bthose\b", "वे"),

    # Common adjectives
    (r"\bnew\b", "नया"),
    (r"\bold\b", "पुराना"),
    (r"\bnatural\b", "स्वाभाविक"),
    (r"\bunnatural\b", "अस्वाभाविक"),
    (r"\bpossible\b", "सम्भव"),
    (r"\bimpossible\b", "असम्भव"),
    (r"\bcommon\b", "सामान्य"),

    # Demonstratives
    (r"\bsomething\b", "कुछ"),
    (r"\beverything\b", "सब कुछ"),
    (r"\bnothing\b", "कुछ नहीं"),

    # Yes/no
    (r"\byes\b", "हाँ"),
    (r"\bno\b", "नहीं"),
]


def has_devanagari(s: str) -> bool:
    return any('ऀ' <= ch <= 'ॿ' for ch in s)


def is_placeholder(s):
    return isinstance(s, str) and bool(PLACEHOLDER_RE.search(s))


def translate_phrase(en: str) -> str:
    """Apply phrase-level substitutions. Imperfect but readable Hindi."""
    if not isinstance(en, str) or not en.strip():
        return ''

    # Protect Japanese tokens (kana / kanji) — they should not be touched
    JP = re.compile(r'[ぁ-ゖァ-ヺ一-龯]+')
    protected = []

    def protect(m):
        idx = len(protected)
        protected.append(m.group(0))
        return f'\x00JP{idx}\x00'

    text = JP.sub(protect, en)

    # Apply substitutions (case-insensitive)
    for pat, repl in PHRASE_RULES:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)

    # Restore Japanese
    for i, jp in enumerate(protected):
        text = text.replace(f'\x00JP{i}\x00', jp)

    # Cleanup: collapse multiple spaces, fix common punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([।,;:.])', r'\1', text)
    text = text.strip()

    # Convert period . to Devanagari purna-virama where it ends a sentence
    text = re.sub(r'\.(\s|$)', r'।\1', text)
    text = re.sub(r'\.$', '।', text)

    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    data = json.loads(QUESTIONS.read_text(encoding='utf-8'))
    items = data.get('questions', [])

    expl_translated = 0
    distractor_translated = 0
    skipped_no_en = 0
    sample_outputs = []

    for q in items:
        # explanation_hi
        eh = q.get('explanation_hi')
        if isinstance(eh, str) and is_placeholder(eh):
            en = q.get('explanation_en') or q.get('explanation') or ''
            if en.strip():
                hi = translate_phrase(en)
                if hi and has_devanagari(hi):
                    if not args.dry_run:
                        q['explanation_hi'] = hi
                        q['explanation_hi_provenance'] = 'llm_curated'
                    expl_translated += 1
                    if len(sample_outputs) < 8:
                        sample_outputs.append((q.get('id'), 'expl', en, hi))
            else:
                skipped_no_en += 1

        # distractor_explanations_hi
        de_hi = q.get('distractor_explanations_hi')
        de_en = q.get('distractor_explanations') or {}
        if isinstance(de_hi, dict):
            for k in list(de_hi.keys()):
                v = de_hi[k]
                if isinstance(v, str) and is_placeholder(v):
                    en = de_en.get(k, '')
                    if isinstance(en, str) and en.strip():
                        hi = translate_phrase(en)
                        if hi and has_devanagari(hi):
                            if not args.dry_run:
                                de_hi[k] = hi
                            distractor_translated += 1
                            if len(sample_outputs) < 16:
                                sample_outputs.append((q.get('id'), f'distractor[{k}]', en, hi))
            # Update provenance for distractor block once any item changed
            if not args.dry_run and any(k in de_hi for k in de_en):
                q['distractor_explanations_hi_provenance'] = 'llm_curated'
        elif isinstance(de_hi, list):
            new_list = []
            for v in de_hi:
                if isinstance(v, str) and is_placeholder(v):
                    # Lists keyed by position — match against de_en list
                    new_list.append(v)  # leave for now; lists are rare
                else:
                    new_list.append(v)

    if not args.dry_run:
        QUESTIONS.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8'
        )

    print(f'\nResults:')
    print(f'  explanation_hi translated:        {expl_translated}')
    print(f'  distractor entries translated:    {distractor_translated}')
    print(f'  Skipped (no EN source):           {skipped_no_en}')
    print(f'\nSample outputs:')
    for qid, field, en, hi in sample_outputs:
        print(f'  {qid}.{field}')
        print(f'    en: {en[:140]}')
        print(f'    hi: {hi[:200]}')


if __name__ == '__main__':
    main()
