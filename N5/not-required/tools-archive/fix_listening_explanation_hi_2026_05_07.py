"""Q39-narrowed residual: explanation_hi on the 35 listening items
that didn't get translated in earlier rounds. Convention: explanatory
prose in Devanagari Hindi, Japanese quoted examples preserved verbatim
(same approach used for grammar / vocab / kanji / reading hi
translations across the corpus).

Idempotent: skips items that already have explanation_hi.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

LISTENING = Path(__file__).parent.parent / 'data' / 'listening.json'

# id → Hindi translation (mirrors explanation_en semantics; Japanese
# examples preserved verbatim per project convention).
EXPLANATION_HI = {
    'n5.listen.006': "पुष्टि: '上です' (शेल्फ़ के ऊपर)।",
    'n5.listen.007': "'ぼくは あきが いちばん すきです' (मुझे शरद ऋतु सबसे पसंद है)।",
    'n5.listen.008': "'新しい カメラが ほしいです' (मुझे नया कैमरा चाहिए)।",
    'n5.listen.009': "विनम्र शुरुआत के लिए すみません का प्रयोग करें + वर्तमान समय पूछने के लिए いま 何時ですか।",
    'n5.listen.010': "टिकट खरीदने का मानक रूप: गंतव्य + काउंटर + おねがいします।",
    'n5.listen.011': "विनम्र इनकार: माफी माँगें + कहें कि आप भर गए हैं।",
    'n5.listen.012': "सुबह का अभिवादन (शिक्षकों/बड़ों के लिए विनम्र रूप)।",
    'n5.listen.013': "A कहता है 9時はんに しましょう (आइए 9:30 पर मिलते हैं)। B सहमत होता है।",
    'n5.listen.014': "जब महिला स्पष्टीकरण माँगती है, तो पुरुष उत्तर निकास (北口) को निर्दिष्ट करता है।",
    'n5.listen.015': "बच्चा सेब और दूध बताता है, फिर ब्रेड लेने से मना कर देता है।",
    'n5.listen.016': "B का दोस्त व्यस्त है, इसलिए B अपनी माँ के साथ जाता है।",
    'n5.listen.017': "मूल योजना 3:00 बजे की थी; ट्रैफ़िक के कारण वास्तविक आगमन 3:30 बजे होगा।",
    'n5.listen.018': "B उत्तर देता है 電車で 行きます (ट्रेन से जाऊँगा/जाऊँगी)।",
    'n5.listen.019': "छात्र उत्तर देता है あたまが いたかったです (मेरे सिर में दर्द था)।",
    'n5.listen.020': "B कहता है 千五百円でした (यह 1,500 येन था)।",
    'n5.listen.021': "सोमवार सप्ताह के दिनों की सीमा (月-金) में आता है, जो 9-5 है। 1-4 घंटे केवल शनिवार पर लागू होते हैं।",
    'n5.listen.022': "कल बारिश है। परसों मौसम अच्छा है लेकिन प्रश्न कल के बारे में है।",
    'n5.listen.023': "महिला स्पष्ट रूप से मंगलवार और गुरुवार कहती है, और पुष्टि करती है कि बुधवार को नहीं है।",
    'n5.listen.024': "तीन लोग: पिता के शिक्षक, माँ के दोस्त, और स्वयं पिता। माँ नहीं आ रही हैं।",
    'n5.listen.025': "विनम्र सुबह का अभिवादन। おやすみなさい सोते समय का है; こんばんは शाम का; さようなら विदाई का।",
    'n5.listen.026': "ऑर्डर करते समय 〜を ください विनम्र अनुरोध है। अन्य विकल्प कॉफ़ी पीते हैं, स्थान पूछते हैं, या सुनने वाले को आदेश देते हैं।",
    'n5.listen.027': "いいえ、けっこうです किसी प्रस्ताव का मानक विनम्र इनकार है।",
    'n5.listen.028': "किसी और के घर में प्रवेश करते समय しつれいします कहा जाता है। ただいま अपने घर के लिए है।",
    'n5.listen.029': "खाने से पहले いただきます कहा जाता है। ごちそうさま भोजन के बाद कहा जाता है।",
    'n5.listen.030': "どこですか स्थान पूछता है। अन्य विकल्प समय, कीमत पूछते हैं, या सुनने वाले को आदेश देते हैं।",
    'n5.listen.031': "पुरुष पहले एक किताब के बारे में सोचता है लेकिन एक टोपी पर निर्णय लेता है (ぼうしに します)।",
    'n5.listen.032': "शनिवार की योजना दोस्तों के साथ फ़िल्म है (土よう日、えいがを 見に 行きます)।",
    'n5.listen.033': "'レストランは 一かいに あります' (रेस्तरां पहली मंज़िल पर है)।",
    'n5.listen.034': "'はやく かおを あらって' — पहले चेहरा धोएं, फिर नाश्ता।",
    'n5.listen.035': "'中国人は 四人で' (चार चीनी लोग)।",
    'n5.listen.036': "'三日間の りょこうです' (तीन दिन की यात्रा)। (सातवें से नौवें तक = तीन दिन।)",
    'n5.listen.037': "बड़ी किताब 2000 येन है, आज आधी कीमत = 1000 येन।",
    'n5.listen.038': "おじゃまします विनम्र वाक्यांश है जब कोई किसी के घर या स्थान में प्रवेश करता है।",
    'n5.listen.039': "ごちそうさまでした भोजन के बाद रेस्तरां छोड़ते समय कहा जाता है।",
    'n5.listen.040': "शाम का अभिवादन (शाम के लिए こんばんは; सुबह के लिए おはよう, सोने जाते समय おやすみ)।",
}


def main() -> int:
    doc = json.loads(LISTENING.read_text(encoding='utf-8'))
    items = doc['items']
    n_added = 0
    n_skipped = 0
    n_missing = 0
    for it in items:
        if it.get('explanation_hi'):
            n_skipped += 1
            continue
        iid = it['id']
        if iid in EXPLANATION_HI:
            it['explanation_hi'] = EXPLANATION_HI[iid]
            n_added += 1
        else:
            n_missing += 1
    LISTENING.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    have = sum(1 for it in items if it.get('explanation_hi'))
    print(f'Added explanation_hi on {n_added} items.')
    print(f'Skipped (already-set): {n_skipped}')
    print(f'No translation provided: {n_missing}')
    print(f'Coverage: {have}/{len(items)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
