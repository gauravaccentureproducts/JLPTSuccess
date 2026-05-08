"""Cycle-2 Phase 1b: extend glossary further to catch the residuals
that Phase 1 missed.

Targets the second-tier residual words found by re-running the
diagnostic after Phase 1. ~30 additional rules.
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

# Phase-1b additions: words found in residuals but missed by Phase 1's glossary
RULES = [
    # Multi-word first
    (r"\bDictionary \(सादा\) रूप\b", "शब्दकोश (सादा) रूप"),
    (r"\bantonym pair\b",         "विलोम जोड़ी"),
    (r"\bsynonym pair\b",         "पर्याय जोड़ी"),
    (r"\bword for\b",             "के लिए शब्द"),
    (r"\bin (the )?hospital\b",   "अस्पताल में"),
    (r"\bcommon mistake\b",       "सामान्य ग़लती"),
    (r"\bof course\b",            "बेशक"),
    (r"\bend point\b",            "अंत-बिंदु"),

    # Words missed by Phase 1
    (r"\btense\b",                "काल"),
    (r"\bopposite\b",             "विपरीत"),
    (r"\bstandard\b",             "मानक"),
    (r"\bDictionary\b",           "शब्दकोश"),
    (r"\bdictionary\b",           "शब्दकोश"),
    (r"\bthan\b",                 "से"),
    (r"\bexpensive\b",            "महँगा"),
    (r"\bcheap\b",                "सस्ता"),
    (r"\bper\b",                  "के अनुसार"),
    (r"\btrain\b",                "ट्रेन"),
    (r"\bparaphrase\b",           "पुनराचना"),
    (r"\bstrictly\b",             "कड़ाई से"),
    (r"\bthrough\b",              "के माध्यम से"),
    (r"\bpair\b",                 "जोड़ी"),
    (r"\bway\b",                  "तरीक़ा"),
    (r"\betc\b",                  "आदि"),
    (r"\bhand\b",                 "हाथ"),
    (r"\bpronoun\b",              "सर्वनाम"),
    (r"\bsequential\b",           "क्रमिक"),
    (r"\bactions\b",              "क्रियाएँ"),
    (r"\baction\b",               "क्रिया-कर्म"),
    (r"\babsent\b",               "अनुपस्थित"),
    (r"\bantonym\b",              "विलोम"),
    (r"\bsynonym\b",              "पर्याय"),
    (r"\bsubstitution\b",         "प्रतिस्थापन"),
    (r"\bsubstitute\b",           "प्रतिस्थापित"),
    (r"\bpragmatic\b",            "व्यावहारिक"),
    (r"\bcommutes\b",             "आना-जाना"),
    (r"\bcommute\b",              "आना-जाना"),
    (r"\btextbook\b",             "पाठ्यपुस्तक"),
    (r"\bworking\b",              "काम करते हुए"),
    (r"\bhurts\b",                "दर्द होता है"),
    (r"\bhurt\b",                 "दर्द"),
    (r"\bcausal\b",               "कारणात्मक"),
    (r"\billustrates\b",          "दिखाता है"),
    (r"\billustrate\b",           "दिखाना"),
    (r"\bexhaustive\b",           "संपूर्ण"),
    (r"\bcontradictory\b",        "विरोधाभासी"),
    (r"\bemphasizing\b",          "ज़ोर देते हुए"),
    (r"\bspecifically\b",         "विशेष रूप से"),
    (r"\bexplicit\b",             "स्पष्ट"),
    (r"\binvite\b",               "आमंत्रित करना"),
    (r"\binvited\b",              "आमंत्रित"),
    (r"\binviting\b",              "आमंत्रित करते हुए"),
    (r"\bjuice\b",                "जूस"),
    (r"\btea\b",                  "चाय"),
    (r"\bcoffee\b",               "कॉफ़ी"),
    (r"\bwater\b",                "पानी"),
    (r"\bdoctor\b",               "डॉक्टर"),
    (r"\bnurse\b",                "नर्स"),
    (r"\bteacher\b",              "शिक्षक"),
    (r"\bnoun-modifier\b",        "संज्ञा-संशोधक"),
    (r"\bmodifier\b",             "संशोधक"),
    (r"\bquantity\b",             "मात्रा"),
    (r"\bdistractor\b",           "विकर्षक"),
    (r"\bdistractors\b",          "विकर्षक"),
    (r"\bcanonical\b",            "मानक"),
    (r"\bproperty\b",             "गुण"),
    (r"\binformation\b",          "जानकारी"),
    (r"\bidentifies\b",           "पहचानता है"),
    (r"\bidentify\b",             "पहचानना"),
    (r"\bidentified\b",           "पहचाना गया"),
    (r"\bidentical\b",            "समान"),
    (r"\binterval\b",             "अंतराल"),
    (r"\binstance\b",             "उदाहरण"),
    (r"\binstances\b",            "उदाहरण"),
    (r"\bcase\b",                 "मामला"),
    (r"\bsense\b",                "अर्थ"),
    (r"\bspecify\b",              "निर्दिष्ट करना"),
    (r"\bspecified\b",            "निर्दिष्ट"),
    (r"\bnominalised\b",          "संज्ञीकृत"),
    (r"\bnominalized\b",          "संज्ञीकृत"),
    (r"\brequires\b",             "की आवश्यकता है"),
    (r"\brequire\b",              "आवश्यकता"),
    (r"\brequest\b",              "अनुरोध"),
    (r"\brequests\b",             "अनुरोध"),
    (r"\bfinite\b",               "सीमित"),
    (r"\bswitches\b",             "बदलता है"),
    (r"\bswitch\b",               "बदलाव"),
    (r"\baddition\b",             "जोड़"),
    (r"\bspoken\b",               "बोला गया"),
    (r"\bspeak\b",                "बोलना"),
    (r"\bspeaks\b",               "बोलता है"),
    (r"\bcasual\b",               "अनौपचारिक"),
    (r"\bclass\b",                "वर्ग"),
    (r"\bdrink\b",                "पीना"),
    (r"\bdrinks\b",               "पेय"),
    (r"\beat\b",                  "खाना"),
    (r"\bate\b",                  "खाया"),
    (r"\bnote\b",                 "नोट"),

    # Already in P1 but case-sensitivity might have missed; reinforce
    (r"\bDictionary\b",           "शब्दकोश"),
    (r"\bDirect\b",               "सीधा"),
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

    total_changes = 0
    files_changed = 0
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
    for f, c in sorted(by_file.items(), key=lambda x: -x[1])[:10]:
        print(f'  {f}: {c}')


if __name__ == '__main__':
    main()
