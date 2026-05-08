"""Cycle-5 Phase 5c: hand-fix the 7 editorial-residual stray English
words found by the final sanity scan after phase 5b.

These are technical-internal terms in paper rationales:
  - Strict-N5 (3 entries) → सख़्त-N5
  - keyed (2 entries) → मुख्य
  - potential (1 entry) → क्षमता-रूप
  - Jukujikun (1 entry) → 熟字訓 (keep as Japanese)
  - moji-corpus / corpus (2 entries) → moji-संग्रह / संग्रह
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

# Hand-fixes by file path + question id
FIXES = {
    ('goi/paper-5.json', 'goi-5.4'): (
        '「じょうずに ひく」 = 「ひくのが じょうず」। समान कौशल, अलग वाक्य-संरचना '
        '(क्रियाविशेषणात्मक → संज्ञीकृत-विशेषण विधेय)। सख़्त-N5: पिछला मुख्य '
        'रूप 「よく ひけます」 (क्षमता-रूप ひける = N4) हटाया गया, उसी नीति से '
        'जो Q4 में लागू हुई।'
    ),
    ('goi/paper-7.json', 'goi-7.6'): (
        '「話すのが じょうず」 = 「上手に 話す」। समान कौशल, अलग वाक्य-संरचना '
        '(संज्ञीकृत विशेषण बनाम क्रियाविशेषण)। सख़्त-N5: पिछले संस्करण में '
        'प्रयुक्त क्षमता-रूप 話せます (N4) भी हटाया गया।'
    ),
    ('goi/paper-7.json', 'goi-7.7'): (
        '「(教師に) しゅくだいを 出す」 ≈ 「先生に しゅくだいを もって いく」। '
        'शिक्षक को गृहकार्य देना भौतिक रूप से उन्हें ले जाने के रूप में '
        'पुनराचित। सख़्त-N5: पिछली मुख्य क्रिया わたす के स्थान पर मोツ + '
        'いく — दोनों मूल N5 क्रियाएँ हैं; わたす अब goi-संग्रह में नहीं '
        'आती। नोट: 持 कान्जी श्वेत-सूची में नहीं है, इसलिए कana में रखा गया।'
    ),
    ('goi/paper-6.json', 'goi-6.11'): (
        'वर्तमान आयु का कथन। मुख्य उत्तर 「いま 二十さいです」 तना के वर्तमान-काल '
        'पहचान-दावे का सीधा पुनःकथन है; अन्य विकल्प समय-संदर्भ बदल देते हैं '
        '(इस साल / कल जन्मदिन / अगले साल)। 二十さい के लिए विशेष पठन はたち अधिक '
        'स्वाभाविक है।'
    ),
    ('goi/paper-6.json', 'goi-6.12'): (
        'वर्तमान आयु का कथन। मुख्य उत्तर 「いま 二十さいです」 तना के वर्तमान-काल '
        'पहचान-दावे का सीधा पुनःकथन है; अन्य विकल्प समय-संदर्भ बदल देते हैं '
        '(इस साल / कल जन्मदिन / अगले साल)। 二十さい के लिए विशेष पठन はたち अधिक '
        'स्वाभाविक है।'
    ),
    ('goi/paper-7.json', 'goi-7.8'): (
        '「(教師に) しゅくだいを 出す」 ≈ 「先生に しゅくだいを もって いく」। '
        'शिक्षक को गृहकार्य देना भौतिक रूप से उन्हें ले जाने के रूप में '
        'पुनराचित। सख़्त-N5: पिछली मुख्य क्रिया わたす के स्थान पर — '
        'vocabulary_n5.md की Ext शाखा से।'
    ),
    ('moji/paper-4.json', 'moji-4.10'): (
        '大人 (おとな — वयस्क)। 熟字訓 (अर्थ-आधारित संयुक्त पठन): कान्जी 大 '
        'और 人 अलग-अलग N5 हैं, पर संयुक्त पठन おとな अनियमित है। संयुक्त '
        'पठन vocabulary_n5.md में N5 शब्दावली प्रविष्टि के रूप में दर्ज है।'
    ),
    ('moji/paper-4.json', 'moji-4.12'): (
        '母 (माँ)। नोट: विकर्षक 妹 कान्जी श्वेत-सूची में नहीं है — यह '
        'मोजी-संग्रह की कान्जी-स्कोप अपवाद-नीति के तहत केवल पहचान-विकर्षक '
        'के रूप में आता है (मोनदाइ 2 के विकर्षक श्वेत-सूची से बाहर के '
        'कान्जी प्रयोग कर सकते हैं जब वे विशिष्ट पारिवारिक-समूह पठन-समानार्थी हों)।'
    ),
    ('moji/paper-5.json', 'moji-5.2'): (
        '子ども यहाँ चयनित है क्योंकि यह इस संग्रह की N5-केवल-कान्जी '
        'नीति का पालन करता है (供 N4 है)। 子供 और 子ども दोनों आधुनिक '
        'जापानी में मानक हैं, और वास्तविक JLPT पर दोनों रूप मिल सकते हैं; '
        'इनमें से चुनाव संग्रह-नीतिगत है।'
    ),
}

flipped = 0
for (file_rel, qid), new_text in FIXES.items():
    path = ROOT / 'data' / 'papers' / file_rel
    if not path.exists():
        print(f'  WARN: {file_rel} not found')
        continue
    pdata = json.loads(path.read_text(encoding='utf-8'))
    found = False
    for q in pdata.get('questions', []):
        if q.get('id') == qid:
            q['rationale_hi'] = new_text
            found = True
            flipped += 1
            print(f'  {file_rel} {qid}: rewritten')
            break
    if found:
        path.write_text(json.dumps(pdata, ensure_ascii=False, indent=2) + '\n',
                        encoding='utf-8')
    else:
        print(f'  WARN: {qid} not found in {file_rel}')

print(f'\nPhase 5c: {flipped} editorial-residual entries fixed')
