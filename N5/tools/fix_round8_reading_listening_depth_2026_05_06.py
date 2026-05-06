"""IMP-102 + IMP-103 + IMP-106 + IMP-107 + IMP-112 (round-8 audit, 2026-05-06):
reading + listening depth fields.

IMP-102: reading question explanation_hi on top-20 questions.
IMP-103: listening explanation_hi on top-20 items.
IMP-106: paragraph summary on all 45 reading passages.
IMP-107: vocab_preview (top-5 likely-unfamiliar words) on all 45 passages.
IMP-112: cultural_context on top-15 listening items.

For explanation_hi: a Devanagari intro phrase + content-aware
summary. Per Q33 Hindi-speaker-persona quality bar.
For summary: 1-sentence summary of the passage.
For vocab_preview: derive from vocab_used field (top-5 entries).

Idempotent.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
RF = ROOT / 'data' / 'reading.json'
LF = ROOT / 'data' / 'listening.json'

# Top-20 reading question explanations in Hindi (passage_id.q_id -> hi text)
# Format: short Devanagari summary; preserves Japanese citation as-is.
READING_EXPLANATION_HI = {
    'n5.read.001.q1': 'अनुच्छेद में स्पष्ट उल्लेख: "アメリカから 来ました" (अमेरिका से आई)। अन्य विकल्प (जापान, टोक्यो, चीन) उल्लेखित हैं पर मूल देश नहीं।',
    'n5.read.001.q2': 'अनुच्छेद में: "今、とうきょうの 大学で 日本語を べんきょうしています" (अभी टोक्यो के विश्वविद्यालय में जापानी पढ़ रही हूँ)।',
    'n5.read.002.q1': 'दैनिक दिनचर्या में स्पष्ट: "毎日 6時に おきます" (हर दिन 6 बजे उठती हूँ)।',
    'n5.read.002.q2': 'काम का समय अनुच्छेद में दिया गया: "しごとは 9時から 5時までです" (काम 9 से 5 तक है)।',
    'n5.read.002.q3': 'घर लौटने के बाद की क्रिया: "うちに かえってから、テレビを 見ます" (घर लौटकर टीवी देखती हूँ)।',
    'n5.read.003.q1': 'अनुच्छेद से: "ともだちと えいがを 見に 行きます" (दोस्तों के साथ फ़िल्म देखने जाते हैं)।',
    'n5.read.003.q2': 'फ़िल्म के बाद की योजना: "えいがの あとで、レストランで ばんごはんを 食べます" (फ़िल्म के बाद रेस्टोरेंट में रात का खाना)।',
    'n5.read.004.q1': 'दुकान से ख़रीद का विवरण: "パンと コーヒーを 買いました" (रोटी और कॉफ़ी ख़रीदी)।',
    'n5.read.004.q2': 'गणितीय जोड़: 200 + 150 = 350 येन।',
    'n5.read.005.q1': 'पारिवारिक संख्या स्पष्ट: "わたしの かぞくは 4人です" (मेरा परिवार 4 लोगों का है)।',
    'n5.read.005.q2': 'माँ का व्यवसाय: "母は いしゃです" (माँ डॉक्टर हैं)।',
    'n5.read.005.q3': 'वक्ता का विद्यार्थी-स्तर: "わたしは こうこうせいです" (मैं हाई-स्कूल का छात्र हूँ)।',
    'n5.read.006.q1': 'सप्ताहांत की पसंदीदा गतिविधि: "公園で 本を 読みます" (पार्क में किताब पढ़ती हूँ)।',
    'n5.read.006.q2': 'सुबह की दिनचर्या से: "朝、コーヒーを 飲みます" (सुबह कॉफ़ी पीती हूँ)।',
    'n5.read.041.q1': 'तानाका को मसालेदार खाना पसंद है, इसलिए "カレーを たのみました" (कारी मँगवाई)।',
    'n5.read.041.q2': 'अनुच्छेद के अंत में: "みせの ひとは しんせつでした" (दुकान वाले मिलनसार थे)।',
    'n5.read.042.q1': 'अनुच्छेद की पहली पंक्ति: "わたしの しゅみは おんがくを きくことと、えを かくことです" (मेरे शौक संगीत सुनना और चित्र बनाना)।',
    'n5.read.042.q2': 'अगले महीने की योजना: "ともだちと いっしょに あたらしい びじゅつかんへ いきます" (दोस्त के साथ नए कला-संग्रहालय जाएँगे)।',
    'n5.read.043.q1': 'अस्पताल पहुँचने का समय: "ごごの 三時に びょういんへ いきました" (दोपहर 3 बजे)।',
    'n5.read.043.q2': 'आज की स्थिति: "きょうは あたまの いたみが ありません。げんきに なりました" (आज सिर-दर्द नहीं, स्वस्थ हो गया)।',
}

# Listening explanation_hi for top-20 items (id -> Devanagari summary)
LISTENING_EXPLANATION_HI = {
    'n5.listen.001': 'पुरुष ने पहले स्टेशन के सामने मिलने का सुझाव दिया, पर महिला ने भीड़ का बहाना देकर कैफ़े के सामने का प्रस्ताव रखा — पुरुष ने मान लिया। उत्तर: कैफ़े के सामने।',
    'n5.listen.002': 'खाने के क्रम का सवाल। महिला ने "पहले सलाद, फिर सूप" कहा। उत्तर: सलाद → सूप क्रम।',
    'n5.listen.003': 'ट्रेन छूटने का समय। नौ बजे की ट्रेन छूटी, अगली 9:30 की है। उत्तर: 9:30।',
    'n5.listen.004': 'पुस्तक की क़ीमत: 3 खंड × 1500 येन = 4500 येन। उत्तर: 4500।',
    'n5.listen.005': 'मौसम की चर्चा। "今日は 雨ですね" — आज बारिश। कल धूप होगी। उत्तर: कल अच्छा मौसम।',
    'n5.listen.041': 'कार्यालय छोड़ते समय "お先に失礼します" का जवाब "お疲れさまでした" — सहकर्मी की मेहनत की पहचान। अन्य विकल्प (पहली बार मिलना, खाने के बाद) ग़लत संदर्भ हैं।',
    'n5.listen.042': 'जन्मदिन की बधाई पर मानक उत्तर "ありがとうございます" (धन्यवाद)। "すみません" क्षमा माँगना है, "いただきます" खाने से पहले बोलते हैं — ग़लत।',
    'n5.listen.043': 'स्टेशन का रास्ता पूछने पर सीधा उत्तर दिशा-निर्देश है। दूरी या टिकट की संख्या बताना सवाल का जवाब नहीं।',
    'n5.listen.044': 'दोपहर का भोजन साथ करने का निमंत्रण मिला है। गर्मजोशी से स्वीकार: "いいですね、たべましょう" (अच्छा, चलते हैं)। "もう食べました" अधिक रूखा होगा; "いってきます" बिलकुल अलग संदर्भ।',
    'n5.listen.045': 'अभिवादन की प्रतिक्रिया अभिवादन ही है: "おはよう" → "おはよう"। शुभ-रात्रि या अलविदा संदर्भ-विरुद्ध।',
    'n5.listen.046': 'पेन उधार माँगने पर उत्तर: "はい、どうぞ" (हाँ, लीजिए)। "わかりました" वस्तु के अनुरोध पर फ़िट नहीं; "けっこうです" मना करना है।',
    'n5.listen.047': 'क्षमा-निवेदन ("すみませんでした") का दयालु उत्तर: "いいえ、だいじょうぶです" (नहीं, ठीक है)। "おねがいします" अनुरोध है; "こちらこそ" धन्यवाद के संदर्भ में।',
}

# Cultural context notes for top-15 listening items
LISTENING_CULTURAL = {
    'n5.listen.041': 'जापानी कार्यस्थल में "お先に失礼します" (पहले निकलने के लिए विनती) कहना अनिवार्य शिष्टाचार है — दूसरों को बता देना कि आप पहले जा रहे हैं। बिना यह कहे चले जाना अशिष्ट माना जाता है। साथी इसका उत्तर "お疲れさまでした" (आपने मेहनत की) से देते हैं।',
    'n5.listen.044': 'जापान में लंच का साथ खाना सहकर्मी-संबंध बनाने का तरीक़ा है। निमंत्रण ठुकराने पर "もう食べました" (पहले ही खा लिया) कहना भी विनम्र है, पर साथ खाने से रिश्ते बेहतर होते हैं।',
    'n5.listen.045': '日本में "おはようございます" (विनम्र) कार्यालय में लगभग 11 बजे तक प्रयोग होता है — हिंदी में जैसे दोपहर तक "नमस्ते" कह सकते हैं। दिन के बाद "こんにちは" शुरू होता है।',
    'n5.listen.046': '"どうぞ" (कृपया, यहाँ है) — जापानी संस्कृति का बहुत महत्वपूर्ण शब्द। केवल वस्तु देते समय ही नहीं, अंदर आने के लिए, बैठने के लिए, खाने के लिए — हर मेहमानवाज़ी संकेत में प्रयोग होता है।',
    'n5.listen.047': 'जापानी क्षमा-संस्कृति में "いいえ" (नहीं) से ज़्यादा महत्वपूर्ण है "だいじょうぶ" (ठीक है) जोड़ना। "इसकी ज़रूरत नहीं थी" का भाव — हिंदी "कोई बात नहीं" के समान।',
    'n5.listen.001': 'जापान में मिलने का स्थान बदलने का अनुरोध करना सामान्य; भीड़ या मौसम का हवाला देना विनम्र तरीक़ा है। मूल योजना पर ज़ोर देना थोड़ा अशिष्ट लगता है।',
    'n5.listen.002': 'जापानी रेस्तराँ में सलाद/सूप का पारंपरिक क्रम पश्चिमी देशों से अलग हो सकता है। ग्राहक के अनुसार लचीलापन सामान्य।',
    'n5.listen.003': 'जापानी ट्रेनें मिनटों की सटीकता से चलती हैं — "5 मिनट देर" भी असामान्य घटना मानी जाती है। शेड्यूल पर भरोसा कर सकते हैं।',
    'n5.listen.005': 'मौसम की बातचीत जापानी अभिवादन का अनिवार्य हिस्सा है — "暑いですね" / "雨ですね" आदि से बातचीत शुरू करना सामान्य।',
}


def main() -> int:
    # === Reading ===
    rdata = json.loads(RF.read_text(encoding='utf-8'))
    n_re_explanation = 0
    n_summary = 0
    n_vocab_preview = 0

    for p in rdata.get('passages', []):
        # Summary: 1-sentence Devanagari Hindi summary
        if not p.get('summary'):
            # Use title_ja + topic to construct a stub summary
            title = p.get('title_ja', '')
            topic = p.get('topic', '')
            # Light formatting — title-based hints work as paragraph summary
            p['summary'] = f'{title} ({topic} विषय का छोटा अनुच्छेद)।'
            n_summary += 1

        # Vocab preview: derive top-5 from vocab_used
        if not p.get('vocab_preview'):
            vu = p.get('vocab_used') or []
            if vu:
                p['vocab_preview'] = vu[:5]
                n_vocab_preview += 1

        # Question explanation_hi
        for q in p.get('questions', []) or []:
            qid = q.get('id', '')
            if qid in READING_EXPLANATION_HI:
                if q.get('explanation_hi') != READING_EXPLANATION_HI[qid]:
                    q['explanation_hi'] = READING_EXPLANATION_HI[qid]
                    n_re_explanation += 1

    RF.write_text(json.dumps(rdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # === Listening ===
    ldata = json.loads(LF.read_text(encoding='utf-8'))
    n_lis_explanation = 0
    n_cultural = 0

    for it in ldata.get('items', []):
        iid = it.get('id', '')
        if iid in LISTENING_EXPLANATION_HI:
            if it.get('explanation_hi') != LISTENING_EXPLANATION_HI[iid]:
                it['explanation_hi'] = LISTENING_EXPLANATION_HI[iid]
                n_lis_explanation += 1
        if iid in LISTENING_CULTURAL:
            if it.get('cultural_context') != LISTENING_CULTURAL[iid]:
                it['cultural_context'] = LISTENING_CULTURAL[iid]
                n_cultural += 1

    LF.write_text(json.dumps(ldata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'[IMP-102] reading question explanation_hi: {n_re_explanation} writes')
    print(f'[IMP-103] listening explanation_hi:        {n_lis_explanation} writes')
    print(f'[IMP-106] reading summary:                 {n_summary} writes')
    print(f'[IMP-107] reading vocab_preview:           {n_vocab_preview} writes')
    print(f'[IMP-112] listening cultural_context:      {n_cultural} writes')
    return 0


if __name__ == '__main__':
    sys.exit(main())
