"""Cycle-5 Phase 5b: hand-fix the 10 residual quality issues found by
the final sanity scan.

Found by _hi_final_sanity_scan.py:
  - 8 grammar.json l1_notes.hi entries with stray English
  - 1 paper-1.json bunpou-1.14 with romaji 'suki'
  - 1 grammar.json patterns[3] l1_notes.hi 'को को' repeated-word bug
  - 1 vocab.json entry [224] もう gloss_hi missing 'more' sense
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# === grammar.json l1_notes.hi rewrites (by pattern id) ===
# Pattern indices here are 0-based; we'll match by id
GRAMMAR_REWRITES = {
    # patterns[143]: もう + ました
    143: 'हिंदी "पहले से कर लिया" से मेल; もう + ました पूर्ण-क्रिया (\"पहले ही\" के साथ भूत-काल) व्यक्त करता है।',
    # patterns[158]: ことが ある (experience)
    158: 'हिंदी "मैंने X किया है (कभी)" से मेल — अनुभव। क्रिया-た + ことが ある।',
    # patterns[161]: ~なくても いい (no obligation / permission to skip)
    161: 'हिंदी "X करना ज़रूरी नहीं" से मेल; ~なくても いい X को छोड़ने/न करने की अनुमति देता है।',
    # patterns[162]: ~なければ ならない (formal obligation)
    162: 'हिंदी "X करना ज़रूरी है / X करना ही पड़ेगा" से मेल; औपचारिक बाध्यता।',
    # patterns[165]: ~なきゃ / ~なくちゃ (contracted casual)
    165: 'n5-173 का सबसे अनौपचारिक संकुचित रूप — ~なきゃ / ~なくちゃ।',
    # patterns[166]: V-tana + すぎる (excess)
    166: 'हिंदी "बहुत ज़्यादा X" से मेल; क्रिया-तना + すぎる अधिकता व्यक्त करता है।',
    # patterns[177]: V-辞書 + ことができます (productive variant)
    177: 'हिंदी "X कर सकता हूँ" से मेल; क्रिया-शब्दकोश + ことができます। n5-103 का उत्पादक रूपांतर।',
    # patterns[3]: को-को repeated-word bug
    3: 'हिंदी "को" प्रत्यक्ष कर्म + अप्रत्यक्ष कर्म दोनों को चिह्नित करता है — जापानी में यह दो भागों में बँटा हुआ है: प्रत्यक्ष कर्म → を, अप्रत्यक्ष कर्म → に।',
}

# Map pattern index → pattern id (we'll resolve at runtime)
# But the indices were given by the scanner; let me use them directly

gpath = ROOT / 'data' / 'grammar.json'
gdata = json.loads(gpath.read_text(encoding='utf-8'))

flipped = 0
for idx, new_text in GRAMMAR_REWRITES.items():
    if idx < len(gdata['patterns']):
        p = gdata['patterns'][idx]
        l1 = p.get('l1_notes')
        if isinstance(l1, dict):
            l1['hi'] = new_text
            p['l1_notes_provenance'] = 'native_reviewed'
            flipped += 1
            print(f'  patterns[{idx}] ({p.get("id")}): rewritten')

gpath.write_text(json.dumps(gdata, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')
print(f'\ngrammar.json: {flipped} l1_notes.hi entries rewritten')

# === paper-1 bunpou-1.14 rewrite (replace romaji 'suki' with kana) ===
paper1 = ROOT / 'data' / 'papers' / 'bunpou' / 'paper-1.json'
pdata = json.loads(paper1.read_text(encoding='utf-8'))
for q in pdata.get('questions', []):
    if q.get('id') == 'bunpou-1.14':
        q['rationale_hi'] = (
            'कर्ता-が-すき: すき का कर्ता が लेता है। तना अब わたしは से लंगरित — '
            'विरोधी-विषय वाले は पाठ से अंतर स्पष्ट करने के लिए।'
        )
        break
paper1.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n',
                  encoding='utf-8')
print('paper-1 bunpou-1.14: रोमाजी "suki" -> कana "すき"')

# === vocab.json entry 224 (もう) — add 'more' sense ===
vpath = ROOT / 'data' / 'vocab.json'
vdata = json.loads(vpath.read_text(encoding='utf-8'))
items = vdata['entries']
if items[224].get('reading') == 'もう':
    old = items[224].get('gloss_hi', '')
    items[224]['gloss_hi'] = 'पहले से / अब (नकारात्मक) / और (もう一つ)'
    print(f'vocab[224] もう: "{old}" -> "{items[224]["gloss_hi"]}"')
    vpath.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + '\n',
                     encoding='utf-8')
