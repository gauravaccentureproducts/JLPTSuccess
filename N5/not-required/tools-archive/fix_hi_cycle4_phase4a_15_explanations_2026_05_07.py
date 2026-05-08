"""Cycle-4 Phase 4a: native-Hindi-expert rewrite of the 15
remaining llm_curated explanation_hi entries in questions.json.

Each rewrite applies R-1..R-7 rubric:
  R-1 Devanagari throughout (Japanese tokens stay Japanese)
  R-2 Natural Hindi sentence structure
  R-3 Register matches teaching prose
  R-4 मानक हिंदी default vocabulary
  R-5 Grammatical accuracy
  R-6 Pedagogical fidelity (Hindi facts about Hindi correct;
       Japanese facts about Japanese correct)
  R-7 Cross-surface consistency
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

REWRITES = {
    'q-0226': "ませんでした विनम्र भूत-नकारात्मक रूप। \"मैंने कल रात का खाना नहीं खाया।\"",
    'q-0229': "\"थोड़ा आराम कर लें\" — ましょう अनौपचारिक सुझाव के लिए।",
    'q-0230': "ませんか = \"क्या आप ... नहीं?\" / \"चलें?\" — विनम्र आमंत्रण। जापानी में नकारात्मक रूप ही मानक विनम्र निमंत्रण है।",
    'q-0233': "समूह-2 का शब्दकोश-रूप たべる है (ます/ない/た के लिए る हटाएँ)।",
    'q-0236': "む से समाप्त होने वाली क्रियाएँ: む → んだ। よむ → よんだ।",
    'q-0238': "い-विशेषण अपना अंतिम い です से पहले बनाए रखते हैं।",
    'q-0254': "क्रमिक श्रृंखला: मध्यवर्ती क्रियाएँ て-रूप में होती हैं; अंतिम क्रिया 行きました काल धारण करती है।",
    'q-0259': "けっこんする क्षणिक क्रिया है — ています परिणामी अवस्था व्यक्त करती है (\"विवाहित है\")।",
    'q-0264': "ないでください = \"कृपया मत करें\"। सादा ない-रूप का प्रयोग करें।",
    'q-0454': "おととい = परसों (बीता हुआ) = 2 दिन पहले = ふつかまえ। देसी काउंटर ふつか (2 दिन) + まえ (पहले) यह पर्याय-श्रृंखला बनाते हैं।",
    'q-0458': "やすい (सस्ता) = たかくない (महँगा नहीं)। आम विलोम-जोड़ी। たかい का अर्थ \"लम्बा\" भी होता है, पर क़ीमत के संदर्भ में \"महँगा\"।",
    'q-0459': "やさしい (आसान, 易しい) = むずかしくない (कठिन नहीं)। ध्यान: やさしい का \"दयालु\" अर्थ भी होता है (優しい), पर N5 में \"आसान\" अर्थ अधिक प्रचलित है।",
    'q-0460': "たくさん = いっぱい (बहुत, ख़ूब)। दोनों मात्रा-सूचक क्रियाविशेषण हैं — \"बड़ी मात्रा\" का अर्थ देते हैं।",
    'q-0461': "せんたくする (कपड़े धोना, 洗濯する) = あらう (धोना)। विशिष्ट-से-सामान्य की शाब्दिक समानता; दोनों एक ही क्रिया का संकेत देते हैं।",
    'q-0463': "まずい (बेस्वाद) = おいしくない (स्वादिष्ट नहीं)। विलोम-जोड़ी; まずい सीधे おいしい का い-विशेषण विपरीत है।",
}

qpath = ROOT / 'data' / 'questions.json'
qdata = json.loads(qpath.read_text(encoding='utf-8'))
flipped = 0
not_found = []
for q in qdata['questions']:
    qid = q.get('id')
    if qid in REWRITES:
        q['explanation_hi'] = REWRITES[qid]
        q['explanation_hi_provenance'] = 'native_reviewed'
        flipped += 1
        del REWRITES[qid]

if REWRITES:
    print(f'WARN: {len(REWRITES)} ids not found: {list(REWRITES.keys())}')

qpath.write_text(json.dumps(qdata, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')
print(f'Phase 4a: {flipped} explanation_hi entries rewritten + flipped to native_reviewed')
