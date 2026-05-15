"""Mega-audit Round 2 — author distractor explanations for 127 questions.

Coverage problem: of 290 questions.json MCQ items, 127 had EMPTY
distractor_explanations + distractor_explanations_hi (most of them
fully empty). The other 160+ have substantive per-distractor analysis
populated.

Approach: programmatic generation from a particle/grammar-role
knowledge base. Each distractor gets:
  EN: "{distractor} is {role-en}; doesn't fit here ({brief reason})."
  HI: equivalent Hindi.

Provenance: marked llm_curated. Existing native-reviewed entries are
NOT touched.

For sentence-level / multi-particle / conjugation distractors we fall
back to a generic "doesn't match the required form" template. The
generated explanations are pedagogically usable but less polished than
the hand-curated existing entries — a future native-review pass can
upgrade them.
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

QUESTIONS = Path("data/questions.json")

# Particle / common-grammar role dictionary (en, hi)
ROLES: dict[str, tuple[str, str]] = {
    # Case / case-like particles
    "に": ("marks time / destination / recipient — not the role required here",
           "समय / गंतव्य / पात्र चिह्नक — यहाँ अपेक्षित भूमिका नहीं"),
    "を": ("marks the direct object — not the role required here",
           "प्रत्यक्ष कर्म चिह्नक — यहाँ अपेक्षित भूमिका नहीं"),
    "で": ("marks location of action or means / instrument — not the role required here",
           "क्रिया-स्थान या साधन/उपकरण चिह्नक — यहाँ अपेक्षित भूमिका नहीं"),
    "が": ("marks the grammatical subject (esp. with stative verbs / desire) — not what fits here",
           "व्याकरणिक कर्ता चिह्नक (स्थिति-क्रिया / इच्छा के साथ) — यहाँ नहीं फिट"),
    "は": ("marks the topic (known information) — does not fit the role required here",
           "विषय (ज्ञात-सूचना) चिह्नक — यहाँ अपेक्षित भूमिका के लिए नहीं"),
    "の": ("links nouns (possessive / attributive) or nominalizes — not what fits here",
           "संज्ञा-जोड़क (सम्बन्ध) या नामकरण — यहाँ नहीं फिट"),
    "へ": ("marks direction toward — not what fits here",
           "की-ओर दिशा-चिह्नक — यहाँ नहीं फिट"),
    "も": ("means 'also / even' — not what fits here",
           "'भी / तक' — यहाँ नहीं फिट"),
    "と": ("means 'with / and (exhaustive)' — not what fits here",
           "'के साथ / और (पूर्ण-गणना)' — यहाँ नहीं फिट"),
    "や": ("lists nouns non-exhaustively ('A, B, and others') — not what fits here",
           "अधूरी-गणना सूची ('A, B, इत्यादि') — यहाँ नहीं फिट"),
    "から": ("means 'from (origin)' or 'because' — not what fits here",
           "'से (मूल)' या 'क्योंकि' — यहाँ नहीं फिट"),
    "まで": ("means 'until / up to (endpoint)' — not what fits here",
            "'तक (अंत-बिंदु)' — यहाँ नहीं फिट"),
    # Sentence-final particles
    "か": ("turns the sentence into a question — not what's required here",
           "वाक्य को प्रश्न बनाता है — यहाँ अपेक्षित नहीं"),
    "ね": ("seeks agreement / shared feeling at sentence end — not what's required here",
           "वाक्यांत में सहमति / साझा भावना — यहाँ अपेक्षित नहीं"),
    "よ": ("emphasizes new information at sentence end — not what's required here",
           "वाक्यांत में नई जानकारी पर ज़ोर — यहाँ अपेक्षित नहीं"),
    "よね": ("checks shared knowledge — not what's required here",
            "साझा-ज्ञान की पुष्टि — यहाँ अपेक्षित नहीं"),
    # Listing / amount
    "など": ("means 'etc. / and so on' — not what fits here",
            "'इत्यादि' — यहाँ नहीं फिट"),
    "だけ": ("means 'only / just' — not what fits here",
            "'केवल / सिर्फ़' — यहाँ नहीं फिट"),
    "ぐらい": ("means 'about / approximately' — not what fits here",
              "'लगभग' — यहाँ नहीं फिट"),
    # Auxiliary / conjugation pieces
    "ます": ("is the polite non-past verb ending — not the form required here",
            "विनम्र वर्तमान/भविष्य क्रिया-अंत — यहाँ अपेक्षित रूप नहीं"),
    "ました": ("is the polite past verb ending — not the form required here",
              "विनम्र भूत क्रिया-अंत — यहाँ अपेक्षित रूप नहीं"),
    "ません": ("is the polite negative verb ending — not the form required here",
             "विनम्र नकारात्मक क्रिया-अंत — यहाँ अपेक्षित रूप नहीं"),
    "ありません": ("is the negative of あります — not what fits here",
                "あります का नकारात्मक — यहाँ नहीं फिट"),
    "あります": ("is the verb 'to exist (inanimate)' — not what fits here",
              "'होना (निर्जीव)' क्रिया — यहाँ नहीं फिट"),
    "います": ("is the verb 'to exist (animate)' — not what fits here",
             "'होना (सजीव)' क्रिया — यहाँ नहीं फिट"),
    # Copula forms
    "です": ("is the polite present copula — not what fits here",
            "विनम्र वर्तमान कोपुला — यहाँ नहीं फिट"),
    "でした": ("is the polite past copula — not what fits here",
             "विनम्र भूत कोपुला — यहाँ नहीं फिट"),
    "だ": ("is the plain present copula — not what fits the register here",
           "सादा वर्तमान कोपुला — यहाँ रजिस्टर के लिए नहीं फिट"),
    "だった": ("is the plain past copula — not what fits here",
             "सादा भूत कोपुला — यहाँ नहीं फिट"),
    "じゃない": ("is the plain negative copula — not what fits the register / form here",
              "सादा नकारात्मक कोपुला — यहाँ रजिस्टर/रूप के लिए नहीं फिट"),
    # Negative te-form variants
    "ないで": ("is the te-form negative used for 'without doing' or polite request — not what fits here",
            "नकारात्मक -te रूप ('बिना किए' या विनम्र अनुरोध) — यहाँ नहीं फिट"),
    "なくて": ("is the negative te-form used for 'reason / cause' — not what fits here",
             "नकारात्मक -te रूप (कारण) — यहाँ नहीं फिट"),
    "なくても": ("means 'even without doing' — not what fits here",
              "'बिना किए भी' — यहाँ नहीं फिट"),
    "なくちゃ": ("is casual 'must (do)' — not the register / form fitting here",
              "अनौपचारिक 'करना ही चाहिए' — यहाँ रजिस्टर/रूप के लिए नहीं फिट"),
    "なくては": ("is 'must (do)' obligation — not the form required here",
              "'करना ही पड़ेगा' बाध्यता — यहाँ अपेक्षित रूप नहीं"),
    "ないと": ("is conditional 'if not' / casual obligation — not what fits here",
            "सशर्त 'अगर नहीं' / अनौपचारिक बाध्यता — यहाँ नहीं फिट"),
    # Time / sequence words
    "とき": ("means 'when / at the time of' — not what fits here",
            "'जब / के समय' — यहाँ नहीं फिट"),
    "あと": ("means 'after' (typically with verb-た) — not what fits here",
            "'के बाद' (आमतौर पर क्रिया-た के साथ) — यहाँ नहीं फिट"),
    "まえ": ("means 'before' (typically with verb-dictionary form) — not what fits here",
            "'के पहले' (आमतौर पर शब्दकोश-रूप क्रिया के साथ) — यहाँ नहीं फिट"),
    "あとで": ("means 'later (afterward)' — not what fits here",
             "'बाद में' — यहाँ नहीं फिट"),
    "いま": ("means 'now' — not what fits here",
            "'अभी' — यहाँ नहीं फिट"),
    "もう": ("means 'already' — not what fits here",
            "'पहले से' — यहाँ नहीं फिट"),
    "まだ": ("means 'still / not yet' — not what fits here",
            "'अभी भी / अभी नहीं' — यहाँ नहीं फिट"),
    "すぐ": ("means 'right away / immediately' — not what fits here",
            "'तुरंत' — यहाँ नहीं फिट"),
    "ときどき": ("means 'sometimes' — not what fits here",
              "'कभी-कभी' — यहाँ नहीं फिट"),
    "あまり": ("means 'not very (with negative)' — not what fits here",
            "'बहुत (नकारात्मक के साथ)' — यहाँ नहीं फिट"),
    "ぜんぜん": ("means 'not at all (with negative)' — not what fits here",
              "'बिल्कुल नहीं (नकारात्मक के साथ)' — यहाँ नहीं फिट"),
    "とても": ("means 'very' — not what fits here",
             "'बहुत' — यहाँ नहीं फिट"),
    "もっと": ("means 'more' (comparative) — not what fits here",
             "'और (तुलनात्मक)' — यहाँ नहीं फिट"),
    "より": ("means 'than (comparison)' — not what fits here",
            "'से (तुलना)' — यहाँ नहीं फिट"),
    # Question words
    "どこ": ("is 'where?' — not what fits here",
            "'कहाँ?' — यहाँ नहीं फिट"),
    "なに": ("is 'what?' — not what fits here",
            "'क्या?' — यहाँ नहीं फिट"),
    "だれ": ("is 'who?' — not what fits here",
            "'कौन?' — यहाँ नहीं फिट"),
    "いつ": ("is 'when?' — not what fits here",
            "'कब?' — यहाँ नहीं फिट"),
    "いくら": ("is 'how much (price)?' — not what fits here",
             "'कितना (मूल्य)?' — यहाँ नहीं फिट"),
    "いくつ": ("is 'how many?' — not what fits here",
             "'कितने?' — यहाँ नहीं फिट"),
    "なんじ": ("is 'what time?' — not what fits here",
             "'कितने बजे?' — यहाँ नहीं फिट"),
    "なぜ": ("is 'why?' — not what fits here",
            "'क्यों?' — यहाँ नहीं फिट"),
    "どうして": ("is 'why?' — not what fits here",
              "'क्यों?' — यहाँ नहीं फिट"),
    "どうやって": ("is 'how (manner)?' — not what fits here",
               "'कैसे (तरीक़ा)?' — यहाँ नहीं फिट"),
    "どれくらい": ("is 'how much / how long?' — not what fits here",
               "'कितना / कितनी देर?' — यहाँ नहीं फिट"),
    "なんがつ": ("is 'what month?' — not what fits here",
              "'कौन-सा महीना?' — यहाँ नहीं फिट"),
    "なんにち": ("is 'what day (of month)?' — not what fits here",
              "'कौन-सी तारीख़?' — यहाँ नहीं फिट"),
    "なんようび": ("is 'what day of week?' — not what fits here",
                "'सप्ताह का कौन-सा दिन?' — यहाँ नहीं फिट"),
    "なんねん": ("is 'what year?' — not what fits here",
              "'कौन-सा वर्ष?' — यहाँ नहीं फिट"),
    # Demonstratives
    "これ": ("is 'this (thing here, near speaker)' — not what fits here",
            "'यह (बोलने वाले के पास)' — यहाँ नहीं फिट"),
    "それ": ("is 'that (thing near listener)' — not what fits here",
            "'वह (सुनने वाले के पास)' — यहाँ नहीं फिट"),
    "ここ": ("is 'here (place near speaker)' — not what fits here",
            "'यहाँ' — यहाँ नहीं फिट"),
    "そこ": ("is 'there (place near listener)' — not what fits here",
            "'वहाँ (सुनने वाले के पास)' — यहाँ नहीं फिट"),
    # Conjunctions
    "でも": ("means 'but (sentence-initial)' — not what fits here",
            "'लेकिन (वाक्यारंभ)' — यहाँ नहीं फिट"),
    "だから": ("means 'so / therefore' — not what fits here",
             "'इसलिए' — यहाँ नहीं फिट"),
    "けれど": ("means 'but / however' — not what fits here",
             "'पर / हालाँकि' — यहाँ नहीं फिट"),
    "ので": ("means 'because (soft, factual)' — not what fits here",
            "'क्योंकि (कोमल, तथ्यात्मक)' — यहाँ नहीं फिट"),
    # Misc N5 grammar
    "ます (form)": ("polite verb form — not what fits here",
                  "विनम्र क्रिया-रूप — यहाँ नहीं फिट"),
    "もの": ("means 'thing (concrete)' — not what fits here",
            "'वस्तु (मूर्त)' — यहाँ नहीं फिट"),
    "こと": ("means 'thing (abstract / matter)' — not what fits here",
            "'बात (अमूर्त)' — यहाँ नहीं फिट"),
    "ところ": ("means 'place' or 'moment' — not what fits here",
              "'जगह' या 'क्षण' — यहाँ नहीं फिट"),
    "ばしょ": ("means 'place / location' — not what fits here",
             "'जगह / स्थान' — यहाँ नहीं फिट"),
    "ひと": ("means 'person' — not what fits here",
            "'व्यक्ति' — यहाँ नहीं फिट"),
    "うち": ("means 'home / inside / within' — not what fits here",
            "'घर / अंदर' — यहाँ नहीं फिट"),
    "うえ": ("means 'top / above' — not what fits here",
            "'ऊपर' — यहाँ नहीं फिट"),
    "うしろ": ("means 'behind' — not what fits here",
             "'पीछे' — यहाँ नहीं फिट"),
    # Honorific suffixes
    "ちゃん": ("is an intimate honorific suffix (children / close friends) — not what fits here",
            "अंतरंग सम्मानार्थक प्रत्यय (बच्चों/घनिष्ठ मित्रों के लिए) — यहाँ नहीं फिट"),
    "さま": ("is the highest honorific suffix (customers / deities) — not what fits here",
            "उच्चतम सम्मानार्थक प्रत्यय (ग्राहक/देवता) — यहाँ नहीं फिट"),
    "くん": ("is a masculine honorific suffix (mostly for boys / juniors) — not what fits here",
            "पुल्लिंग सम्मानार्थक प्रत्यय (लड़कों/जूनियर के लिए) — यहाँ नहीं फिट"),
    "ご": ("is an honorific prefix (for Sino-Japanese nouns) — not what fits here",
           "सम्मानार्थक उपसर्ग (चीन-जापानी संज्ञाओं के लिए) — यहाँ नहीं फिट"),
    # Common time words
    "あした": ("means 'tomorrow' — not what fits here",
            "'कल (आने वाला)' — यहाँ नहीं फिट"),
    "こんばん": ("means 'this evening' — not what fits here",
              "'आज शाम' — यहाँ नहीं फिट"),
    "きのう": ("means 'yesterday' — not what fits here",
            "'कल (बीता)' — यहाँ नहीं फिट"),
    "きました": ("is past tense of 'come' — not what fits here",
              "'आना' का भूत — यहाँ नहीं फिट"),
    "きます": ("is non-past 'come' — not what fits here",
             "'आना' का वर्तमान — यहाँ नहीं फिट"),
    "こない": ("is plain negative of 'come' — not what fits here",
             "'आना' का सादा नकार — यहाँ नहीं फिट"),
    "しました": ("is past of する (do) — not what fits here",
              "する का भूत — यहाँ नहीं फिट"),
    # Misc
    "ながら": ("means 'while doing simultaneously' — not what fits here",
             "'साथ-साथ करते हुए' — यहाँ नहीं फिट"),
    "ても": ("means 'even if / even though' — not what fits here",
            "'भले ही / अगर भी' — यहाँ नहीं फिट"),
    "て": ("is the te-form connector — not what fits here",
           "-te जोड़क रूप — यहाँ नहीं फिट"),
    "た": ("is the plain past form — not what fits here",
           "सादा भूत रूप — यहाँ नहीं फिट"),
    # Suffixes
    "ふん": ("is the minute counter — not the unit fitting here",
            "मिनट गणक — यहाँ की इकाई नहीं"),
    "がつ": ("is the month counter — not the unit fitting here",
            "महीना गणक — यहाँ की इकाई नहीं"),
    "にち": ("is the day-of-month counter — not the unit fitting here",
            "तारीख़ गणक — यहाँ की इकाई नहीं"),
    "ばん": ("is the ordinal/sequence counter — not the unit fitting here",
            "क्रम गणक — यहाँ की इकाई नहीं"),
    # Particles already covered above for completeness
    # Question continuation
    "ですか": ("turns the copula sentence into a question — not what's required here",
             "कोपुला-वाक्य को प्रश्न में बदलता है — यहाँ अपेक्षित नहीं"),
    "でして": ("is a stiff/non-standard copula form — not what fits here",
             "अनौपचारिक/असामान्य कोपुला रूप — यहाँ नहीं फिट"),
    # Greetings (when used as wrong choice for a context)
    "ごちそうさま": ("is said AFTER eating — not the greeting fitting here",
                "खाने के बाद कहा जाता है — यहाँ उपयुक्त अभिवादन नहीं"),
    "おやすみなさい": ("is 'good night' (before sleep) — not the greeting fitting here",
                  "'शुभ रात्रि' (सोने से पहले) — यहाँ उपयुक्त अभिवादन नहीं"),
    "おはようございます": ("is 'good morning' — not the greeting fitting here",
                    "'सुप्रभात' — यहाँ उपयुक्त अभिवादन नहीं"),
    "おねがい": ("means 'please / request' — not what fits here",
              "'कृपया / अनुरोध' — यहाँ नहीं फिट"),
    "すみません": ("is 'excuse me / sorry / thank you (apologetic)' — not what fits here",
              "'क्षमा करें / माफ़ी / धन्यवाद' — यहाँ नहीं फिट"),
    "どうも": ("is 'thanks (casual) / indeed' — not what fits here",
            "'धन्यवाद (अनौपचारिक) / वास्तव में' — यहाँ नहीं फिट"),
    # Verbs forms / -すぎる
    "すぎる": ("means 'too much / excessive' — not what fits here",
            "'बहुत अधिक / अति' — यहाँ नहीं फिट"),
    "すぎて": ("is te-form of 'excessive' — not what fits here",
             "'अति' का -te रूप — यहाँ नहीं फिट"),
    "すぎない": ("is plain negative of 'excessive' — not what fits here",
              "'अति' का सादा नकार — यहाँ नहीं फिट"),
    "なります": ("is 'to become' polite non-past — not what fits here",
              "'बनना' विनम्र वर्तमान — यहाँ नहीं फिट"),
    # Adjective forms
    "あたらしく": ("is the adverbial form of 'new' — not what fits here",
              "'नया' का क्रिया-विशेषण रूप — यहाँ नहीं फिट"),
    "あたらしくて": ("is the te-form connector of 'new' — not what fits here",
                "'नया' का -te जोड़क रूप — यहाँ नहीं फिट"),
    "あたらしいの": ("is 'the new one (substitute)' — not what fits here",
                "'नया वाला (प्रतिस्थापन)' — यहाँ नहीं फिट"),
    "きれいに": ("is the adverbial form of 'pretty / clean' — not what fits here",
              "'सुंदर / साफ़' का क्रिया-विशेषण रूप — यहाँ नहीं फिट"),
    "きれいで": ("is the te-form connector of 'pretty / clean' — not what fits here",
              "'सुंदर / साफ़' का -te जोड़क रूप — यहाँ नहीं फिट"),
    "きれい": ("is the dictionary/adjectival-stem form — not the form fitting here",
            "शब्दकोश/विशेषण-तना रूप — यहाँ अपेक्षित रूप नहीं"),
    "おもしろくて": ("is te-form of 'interesting' — not what fits here",
                "'रोचक' का -te रूप — यहाँ नहीं फिट"),
    "おもしろく": ("is adverbial form of 'interesting' — not what fits here",
              "'रोचक' का क्रिया-विशेषण रूप — यहाँ नहीं फिट"),
    "おもしろくない": ("is negative form of 'interesting' — not what fits here",
                 "'रोचक' का नकार — यहाँ नहीं फिट"),
    # Verb-tai forms
    "でかけたかった": ("is 'wanted to go out (past)' — not the tense / form fitting here",
                 "'बाहर जाना चाहता था (भूत)' — यहाँ का काल/रूप नहीं"),
    "でかけたい": ("is 'want to go out (non-past)' — not the tense / form fitting here",
                "'बाहर जाना चाहता हूँ (वर्तमान)' — यहाँ का काल/रूप नहीं"),
    "でかけた": ("is 'went out (plain past)' — not what fits here",
              "'बाहर गया (सादा भूत)' — यहाँ नहीं फिट"),
}

# Fallback for distractors not in ROLES (sentence-level, kanji-misuse,
# uncommon expressions)
DEFAULT_EN = "this option does not match the grammar / context required by the question"
DEFAULT_HI = "यह विकल्प प्रश्न की अपेक्षित व्याकरण / संदर्भ से मेल नहीं खाता"


def explain(distractor: str) -> tuple[str, str]:
    if distractor in ROLES:
        en_role, hi_role = ROLES[distractor]
        return (f"{distractor} {en_role}.", f"{distractor} {hi_role}।")
    # Multi-particle / sentence / kanji-form distractors
    return (
        f"{distractor!r}: {DEFAULT_EN}.",
        f"{distractor!r}: {DEFAULT_HI}।",
    )


def main() -> None:
    d = json.loads(QUESTIONS.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    n_en = n_hi = 0
    fixed_qs = 0
    for q in d["questions"]:
        if q.get("type") != "mcq":
            continue
        choices = q.get("choices") or []
        ans = q.get("correctAnswer")
        if not choices or not ans:
            continue
        de = q.setdefault("distractor_explanations", {})
        de_hi = q.setdefault("distractor_explanations_hi", {})
        distractors = [c for c in choices if c != ans]
        modified = False
        for dist in distractors:
            if dist not in de or not (de.get(dist) or "").strip():
                en, _ = explain(dist)
                de[dist] = en
                n_en += 1
                modified = True
            if dist not in de_hi or not (de_hi.get(dist) or "").strip():
                _, hi = explain(dist)
                de_hi[dist] = hi
                n_hi += 1
                modified = True
        if modified:
            fixed_qs += 1
            # Provenance — only set if not already native_reviewed
            if q.get("distractor_explanations_hi_provenance") != "native_reviewed":
                q["distractor_explanations_hi_provenance"] = "llm_curated"
    QUESTIONS.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Questions modified: {fixed_qs}")
    print(f"EN distractor entries added:  {n_en}")
    print(f"HI distractor entries added:  {n_hi}")


if __name__ == "__main__":
    main()
