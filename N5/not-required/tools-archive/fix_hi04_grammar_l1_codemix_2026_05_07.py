"""HI-04: replace English code-mix in grammar.json l1_notes.hi (and
optionally explanation_hi) with Hindi equivalents.

Walks every grammar pattern's l1_notes.hi (and explanation_hi),
applies word-boundary-aware regex substitutions for common English
technical terms that have settled Hindi equivalents.

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

# Walk up until we find the N5 root (where data/ lives)
ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

GRAMMAR = ROOT / 'data' / 'grammar.json'

# English-technical → Hindi map. Order matters: longer compound phrases first.
# Each entry: (pattern, replacement) where pattern is a regex that uses
# word boundaries.
SUBSTITUTIONS = [
    # ---- Multi-word phrases first (longest match wins) ----
    (r'\bsame as above\b',            'जैसे ऊपर'),
    (r'\bsame intonation-only feel\b', 'केवल-स्वरारोह वाला अहसास'),
    (r'\balready covered\b',           'पहले से शामिल'),
    (r'\bsee n5-(\d+)\b',              r'n5-\1 देखें'),

    # ---- Verb / form / pattern names that should stay in their compound shape ----
    # These are caught by Phase A but residuals may exist
    (r'\bnon-past\b',                  'अभूत'),
    (r'\bpast tense\b',                'भूत-काल'),
    (r'\bpresent tense\b',             'वर्तमान-काल'),

    # ---- JLPT pedagogical vocabulary ----
    (r'\bnominalizer\b',               'नामकरण-कण'),
    (r'\bnominalised\b',               'संज्ञीकृत'),
    (r'\bnominalised\b',               'संज्ञीकृत'),
    (r'\bparticle\b',                  'कण'),
    (r'\bparticles\b',                 'कण'),
    (r'\bstem\b',                      'तना'),
    (r'\bsubject\b',                   'कर्ता'),
    (r'\bobject\b',                    'कर्म'),
    (r'\bverb\b',                      'क्रिया'),
    (r'\bVerb\b',                      'क्रिया'),
    (r'\bverbs\b',                     'क्रियाएँ'),
    (r'\badjective\b',                 'विशेषण'),
    (r'\badjectives\b',                'विशेषण'),
    (r'\badjectival\b',                'विशेषणात्मक'),
    (r'\bnoun\b',                      'संज्ञा'),
    (r'\bnouns\b',                     'संज्ञाएँ'),
    (r'\badverb\b',                    'क्रिया-विशेषण'),
    (r'\bcounter\b',                   'काउंटर'),
    (r'\bcounters\b',                  'काउंटर'),
    (r'\bclause\b',                    'उपवाक्य'),
    (r'\bsentence\b',                  'वाक्य'),
    (r'\bquestion\b',                  'प्रश्न'),
    (r'\bquestions\b',                 'प्रश्न'),
    (r'\bquestion-form\b',             'प्रश्न-रूप'),

    # ---- Aspect / register vocabulary ----
    (r'\bcasual\b',                    'अनौपचारिक'),
    (r'\bpolite\b',                    'विनम्र'),
    (r'\bformal\b',                    'औपचारिक'),
    (r'\binformal\b',                  'अनौपचारिक'),
    (r'\bnegative\b',                  'नकारात्मक'),
    (r'\baffirmative\b',               'सकारात्मक'),
    (r'\bplain\b',                     'सादा'),
    (r'\banimate\b',                   'सजीव'),
    (r'\binanimate\b',                 'निर्जीव'),
    (r'\bpast\b',                      'भूत'),

    # ---- Meta-vocabulary ----
    (r'\btransfer\b',                  'मेल'),
    (r'\bsame\b',                      'समान'),
    (r'\bonly\b',                      'केवल'),
    (r'\bversion\b',                   'संस्करण'),
    (r'\bvariant\b',                   'रूपांतर'),
    (r'\bfeel\b',                      'अनुभव'),
    (r'\bfamily\b',                    'समूह'),
    (r'\bcovered\b',                   'शामिल'),
    (r'\balready\b',                   'पहले से'),
    (r'\bnative\b',                    'देसी'),
    (r'\bintonation\b',                'स्वर-आरोह'),
    (r'\boffer\b',                     'प्रस्ताव'),
    (r'\bopinion\b',                   'राय'),
    (r'\bform\b',                      'रूप'),
    (r'\bforms\b',                     'रूप'),

    # ---- Romaji glue words ----
    (r'\bnoun-modifier\b',             'संज्ञा-संशोधक'),
    (r'\bnoun-form\b',                 'संज्ञा-रूप'),

    # ---- Round-2 expansion (words found by Phase E re-scan) ----
    # Compounds first
    (r'\btopic-marker\b',              'विषय-सूचक'),
    (r'\btopic-first\b',               'विषय-प्रथम'),
    (r'\blocation-first\b',            'स्थान-प्रथम'),
    (r'\bskill-marker\b',              'कौशल-सूचक'),
    (r'\bset-greetings\b',             'मानक अभिवादन'),
    (r'\bnon-past\b',                  'अभूत'),
    (r'\bsequence connector\b',        'अनुक्रम-जोड़क'),
    (r'\bchain actions\b',             'क्रमिक क्रियाएँ'),
    (r'\bincomplete-action\b',         'अपूर्ण-क्रिया'),
    (r'\bvolitional\b',                'इच्छासूचक'),
    (r'\bquotation\b',                 'उद्धरण'),
    (r'\bgreetings\b',                 'अभिवादन'),
    (r'\bgenitive\b',                  'सम्बंधसूचक'),
    (r'\binvitation\b',                'आमंत्रण'),
    (r'\binvite\b',                    'आमंत्रित करना'),
    (r'\binvitations\b',               'आमंत्रण'),
    (r'\bsuggestion\b',                'सुझाव'),
    (r'\bsuggest\b',                   'सुझाव देना'),
    (r'\binfinitive\b',                'धातु-रूप'),
    (r'\bfoundation\b',                'आधार'),
    (r'\bconnecting\b',                'जोड़क'),
    (r'\bconnector\b',                 'जोड़क'),
    (r'\bchain\b',                     'श्रृंखला'),
    (r'\bactions\b',                   'क्रियाएँ'),
    (r'\baction\b',                    'क्रिया'),
    (r'\bprogressive\b',               'प्रगतिशील'),
    (r'\bresultative\b',               'परिणाम-सूचक'),
    (r'\bresult\b',                    'परिणाम'),
    (r'\bconcessive\b',                'रियायत-सूचक'),
    (r'\binflection\b',                'रूप-परिवर्तन'),
    (r'\binflected\b',                 'रूप-परिवर्तित'),
    (r'\binvariant\b',                 'अपरिवर्तनीय'),
    (r'\bcomparison\b',                'तुलना'),
    (r'\bexistence\b',                 'अस्तित्व'),
    (r'\btopic\b',                     'विषय'),
    (r'\bskill\b',                     'कौशल'),
    (r'\bconjugate\b',                 'रूपांतरित करना'),
    (r'\bexplicit\b',                  'स्पष्ट'),
    (r'\bpurpose\b',                   'प्रयोजन'),
    (r'\bhour\b',                      'घंटा'),
    (r'\bminute\b',                    'मिनट'),
    (r'\bphonetic\b',                  'ध्वन्यात्मक'),
    (r'\bhalf\b',                      'आधा'),
    (r'\bnumber\b',                    'संख्या'),
    (r'\btense\b',                     'काल'),
    (r'\btime\b',                      'समय'),
    (r'\babove\b',                     'ऊपर'),
    (r'\bpolitest\b',                  'सर्वोच्च-विनम्र'),
    (r'\bmarker\b',                    'सूचक'),
    (r'\brequest\b',                   'अनुरोध'),
    (r'\bbase\b',                      'मूल'),
    (r'\bpattern\b',                   'पैटर्न'),
    (r'\bemphasis\b',                  'ज़ोर'),
    (r'\bdictionary\b',                'शब्दकोश'),
    (r'\bspeech\b',                    'भाषा'),
    (r'\bpermission\b',                'अनुमति'),
    (r'\bsequence\b',                  'क्रम'),
    (r'\blocation\b',                  'स्थान'),
    (r'\bfirst\b',                     'पहले'),
    (r'\badvice\b',                    'सलाह'),
    (r'\badvanced\b',                  'उन्नत'),

    # Connector words (only inside Hindi prose; word boundaries protect English fragments)
    (r'\bin\b',                        'में'),
    (r'\bof\b',                        'का'),
    (r'\bfor\b',                       'के लिए'),

    # ---- Round-3 expansion (final residuals) ----
    # Capital-N variants (case-sensitive regex doesn't match)
    (r'\bNoun\b',                      'संज्ञा'),
    (r'\bNumber\b',                    'संख्या'),
    (r'\bPurpose\b',                   'प्रयोजन'),
    (r'\bAnswer\b',                    'उत्तर'),
    # Final residuals
    (r'\bnone\b',                      'कोई नहीं'),
    (r'\bexpression\b',                'अभिव्यक्ति'),
    (r'\bcontrast\b',                  'विरोध'),
    (r'\breceive\b',                   'प्राप्त'),
    (r'\bsofter\b',                    'नरम'),
    (r'\brelative\b',                  'सम्बंधक'),
    (r'\bclauses\b',                   'उपवाक्य'),
    (r'\bdirect\b',                    'सीधा'),
    (r'\bquote\b',                     'उद्धरण'),
    (r'\bindirect\b',                  'अप्रत्यक्ष'),
    (r'\border\b',                     'आदेश'),
    (r'\bphrases\b',                   'वाक्यांश'),
    (r'\bphrase\b',                    'वाक्यांश'),
]


def has_devanagari(s: str) -> bool:
    return any('ऀ' <= ch <= 'ॿ' for ch in s)


def apply_subs(value: str) -> tuple[str, list[str]]:
    """Apply substitutions only inside Hindi (Devanagari-bearing) text.

    Protects parenthesized English glosses (a teaching device — e.g.,
    "नामकरण-कण (nominalizer)") from being converted to tautologies.
    """
    if not isinstance(value, str) or not has_devanagari(value):
        return value, []

    # Find all parenthesized English-only spans and protect them
    PAREN_EN = re.compile(r'\(([^()]*[a-zA-Z][^()]*)\)')
    protected = []

    def protect(m):
        content = m.group(1)
        # Only protect if it's mostly English (no Devanagari inside)
        if any('ऀ' <= ch <= 'ॿ' for ch in content):
            return m.group(0)  # mixed; don't protect, let subs run
        idx = len(protected)
        protected.append(m.group(0))
        return f'\x00PROT{idx}\x00'

    new = PAREN_EN.sub(protect, value)

    applied = []
    for pat, repl in SUBSTITUTIONS:
        before = new
        new = re.sub(pat, repl, new)
        if new != before:
            applied.append(pat)

    # Restore protected spans
    for i, content in enumerate(protected):
        new = new.replace(f'\x00PROT{i}\x00', content)

    return new, applied


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--limit', type=int, default=None)
    args = parser.parse_args()

    data = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = data.get('patterns', [])

    change_log = defaultdict(int)
    samples = []
    touched_count = 0

    for pat in patterns:
        # l1_notes.hi
        l1n = pat.get('l1_notes')
        if isinstance(l1n, dict) and isinstance(l1n.get('hi'), str):
            new_val, applied = apply_subs(l1n['hi'])
            if applied:
                if not args.dry_run:
                    l1n['hi'] = new_val
                touched_count += 1
                if len(samples) < 20:
                    samples.append(('l1_notes.hi', pat.get('id', '?'), l1n['hi'] if not args.dry_run else None, applied[:5], (l1n['hi'] if args.dry_run else new_val)[:200]))
                for a in applied:
                    change_log[a] += 1
        # explanation_hi (also has code-mix per HI-05)
        eh = pat.get('explanation_hi')
        if isinstance(eh, str):
            new_val, applied = apply_subs(eh)
            if applied:
                if not args.dry_run:
                    pat['explanation_hi'] = new_val
                touched_count += 1
                if len(samples) < 30:
                    samples.append(('explanation_hi', pat.get('id', '?'), None, applied[:5], new_val[:200]))
                for a in applied:
                    change_log[a] += 1
        if args.limit and touched_count >= args.limit:
            break

    if not args.dry_run:
        GRAMMAR.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8'
        )

    print(f"\nTotal entries touched: {touched_count}")
    print(f"\nPer-rule change counts:")
    for rule, count in sorted(change_log.items(), key=lambda x: -x[1]):
        print(f'  {rule:<40} {count}')

    print(f"\nSample replacements (first 12):")
    for field, iid, _, rules, snippet in samples[:12]:
        print(f"  {iid}.{field}")
        print(f"    rules applied: {rules}")
        print(f"    after: {snippet}")


if __name__ == '__main__':
    main()
