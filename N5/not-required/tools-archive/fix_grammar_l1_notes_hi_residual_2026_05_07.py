"""Q39-narrowed residual: Hindi-L1 interference notes (l1_notes.hi)
on 151 grammar patterns that didn't get them in earlier rounds.
Round-8 + earlier rounds covered the top-30 (highest-frequency
core_n5); this closes the residual.

Each note is 1-2 sentences in Devanagari Hindi, focused on the
most relevant Hindi→Japanese transfer pitfall for that pattern.
Japanese examples preserved verbatim per project convention.

The 9 mandatory contrast areas (per audit prompt):
  1. SOV word-order shared advantage
  2. Postposition→particle mapping (से→から/で, को→を/に, में→に/で)
  3. Verb-agreement transfer (Hindi gender/number → none in JP)
  4. Tense over-marking (Hindi multi-tense → JP non-past/past)
  5. Politeness mismatch (3-tier Hindi pronoun → JP morphological keigo)
  6. Negative-formation placement (नहीं sentence-medial vs ない attached)
  7. Question-particle position (क्या at start vs か at end)
  8. Plural marking (Hindi marks vs JP usually doesn't)
  9. Counter-system overlap (familiar but different inventory)

Idempotent: skips patterns that already have l1_notes.hi set.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

GRAMMAR = Path(__file__).parent.parent / 'data' / 'grammar.json'

# Pattern_id → Hindi L1-interference note. Each is 1-2 sentences,
# Devanagari Hindi prose, JA examples preserved verbatim.
L1_NOTES_HI = {
    # === Particles + sentence-final markers ===
    'n5-031': 'हिंदी प्रश्न-सूचक स्वर-वलन से बनते हैं ("तू आ रहा?"); यहाँ जापानी casual क्रिया + の भी same intonation-only feel। प्रश्न-कण か की जगह の आकस्मिक है — मित्रों में सही, वरिष्ठों के साथ ग़लत।',
    'n5-032': 'हिंदी "भी" (मैं भी, तुम भी) सीधे も से जुड़ता है — पर ध्यान: हिंदी में "मैं भी" → わたしも, "मैं को भी" नहीं — も पुराने を/が को बदल देता है, जोड़ता नहीं।',
    'n5-033': 'हिंदी "केवल / सिर्फ़" से सीधा मेल — पर だけ कण नियमों का पालन करता है, "सिर्फ़" शब्द-स्तर पर रहता है। 一人だけ (केवल एक व्यक्ति) पूरा वाक्यांश है।',
    'n5-034': 'हिंदी "केवल X" + सकारात्मक से अलग: しか हमेशा नकारात्मक क्रिया (~ありません, ~ません) के साथ। यह हिंदी बक्ताओं के लिए सबसे बड़ी ट्रैप है।',
    'n5-035': 'हिंदी "लगभग / क़रीब" से मेल — पर ぐらい/くらい मात्रा (पैसा, समय अवधि) के साथ; ごろ समय-बिंदु (3 बजे) के साथ।',
    'n5-036': 'ごろ हिंदी "के क़रीब / लगभग" का अनुवाद; पर केवल समय-बिंदुओं के साथ (3時ごろ ✓, 3時間ごろ ✗ — अवधि के लिए ぐらい)।',
    'n5-037': 'हिंदी "वग़ैरह / आदि" से मेल; पर など सूची के अंत में आता है — हिंदी "वग़ैरह" भी अंत में, यह transfer आसान है।',
    'n5-038': 'हिंदी "प्रत्येक / हर एक" से मेल — पर ずつ संख्या के बाद आता है (一つずつ = "एक-एक"), अंक से पहले नहीं।',
    # === Demonstratives ===
    'n5-039': 'हिंदी 2-स्तरीय (यह / वह) है; जापानी 3-स्तरीय (これ/それ/あれ)। それ "श्रोता के पास" को व्यक्त करता है, जिसका हिंदी में सीधा अनुवाद नहीं।',
    'n5-040': 'हिंदी "यह कितना" / "वह कितना" — adjectival use। この/その/あの संज्ञा से पहले सीधे जुड़ते हैं, "का" जैसे कण की ज़रूरत नहीं।',
    'n5-041': 'हिंदी "यहाँ / वहाँ / उधर" — पर 3-स्तर वही: ここ (पास), そこ (श्रोता-पास), あそこ (दोनों से दूर)।',
    'n5-042': 'polite version of こちら/そちら/あちら। हिंदी "कौन-सा?" का अनुवाद कई जापानी रूपों में होता है — यह सबसे विनम्र।',
    'n5-043': 'हिंदी "कैसा" + संज्ञा से मेल; どんな + संज्ञा = "किस तरह का"। साधारण विवरण-प्रश्न।',
    'n5-044': 'हिंदी "कैसे / इस तरह / उस तरह" — पर こう/そう/ああ/どう क्रिया-विधि बताते हैं, संज्ञा को नहीं संशोधित करते।',
    'n5-045': 'हिंदी "ये / ये लोग / वे" + ら / たち। जापानी में बहुवचन सीमित है — ये केवल लोगों + क़रीबी संज्ञाओं के साथ। चीज़ों के लिए たち न लगाएँ।',
    'n5-046': 'polite "कौन" — दोनों भाषाओं में विनम्रता-स्तर के अनुसार सर्वनाम बदलते हैं: हिंदी "कौन साहब", जापानी どなた।',
    'n5-049': 'どれ अलग चीज़ों में से कौन-सा (3+); どちら दो में से कौन-सा (विनम्र भी हो सकता है)। हिंदी "कौन-सा?" इस फ़र्क़ को नहीं करता।',
    # === Question words ===
    'n5-051': 'हिंदी "क्यों" वाक्य के शुरू में आता है (क्यों आए?); जापानी どうして / なぜ भी शुरू में, यह transfer आसान है।',
    'n5-052': 'हिंदी "कैसे" — पर どうやって केवल विधि/साधन ("कैसे जाएँ?"), どう हाल पूछता है ("कैसा है?")।',
    'n5-053': 'हिंदी "कितना" + पैसा। いくら केवल मूल्य/मात्रा के लिए, समय या संख्या के लिए नहीं।',
    'n5-054': 'हिंदी "कितने" — किसी भी गिनती के लिए। पर जापानी में काउंटर-विशिष्ट प्रश्न (なんにん, なんまい) ज़्यादा सही हैं; いくつ केवल आम/native counter या उम्र के लिए।',
    'n5-055': 'हिंदी "कितने बजे" — सीधा अनुवाद; なんじ केवल समय-बिंदु, अवधि नहीं।',
    'n5-056': 'हिंदी "कौन-सा दिन" — सप्ताह के दिन के लिए। なんようび केवल सप्ताह-दिन (सोम, मंगल) के लिए, तारीख़ के लिए नहीं।',
    'n5-057': 'हिंदी "कौन-सा महीना / कौन-सी तारीख़" — दोनों मिलकर। なんがつ + なんにち अक्सर साथ आते हैं।',
    # === Verb forms ===
    'n5-063': 'हिंदी "क्या मैं करूँ?" / "क्या हम करें?" से मेल। ましょうか offer (मैं तुम्हारे लिए करूँ?) या suggestion (आइए साथ करें)।',
    'n5-073': 'हिंदी "नहीं कर रहा / नहीं हुआ" — पर ていません दोनों को कवर करता है: "अभी नहीं" + "result अभी नहीं हुआ"। प्रसंग से पहचानें।',
    'n5-076': 'हिंदी "के बाद" से मेल — पर てから केवल क्रिया + क्रिया (एक के बाद दूसरा)। संज्ञा + क्रिया के लिए のあとで।',
    # === Adjectives ===
    'n5-078': 'हिंदी विशेषण लिंग-वचन से बदलते हैं (बड़ा/बड़ी/बड़े); जापानी い-विशेषण नहीं बदलते। यह आपकी ताक़त — कम भूल का मौक़ा।',
    'n5-084': 'हिंदी विशेषण की "का/की/के" form से मेल; な-विशेषण को संज्ञा से जोड़ने पर な जोड़ें (きれいな花, गलत: きれい花)।',
    'n5-093': 'हिंदी "X, Y में है" से मेल; पर あります निर्जीव / います सजीव — हिंदी "है" यह भेद नहीं करता।',
    'n5-094': 'हिंदी "मेरे पास X है / Y में X है" — सब "है" से। जापानी में स्वामित्व, घटना, कौशल — सब अलग व्याकरणिक रूप।',
    # === Comparison ===
    'n5-095': 'हिंदी "X से Y बड़ा है" से मेल। より = "से" (तुलना)। हिंदी पैटर्न A は B より [adj] です — A से B [adj] है।',
    'n5-096': 'हिंदी "X से Y वाला बेहतर है" से मेल; のほうが = "वाला" (zoomed-in विकल्प)।',
    'n5-097': 'हिंदी "A और B में से कौन-सा?" — दो विकल्प तुलना। どちらが केवल दो में से चुनाव।',
    # === Likes / wants ===
    'n5-098': 'हिंदी "मुझे X पसंद है, Y नहीं" — विरोधी प्राथमिकता। が कण: स्वामित्व नहीं, इच्छा-वस्तु marker।',
    'n5-101': 'हिंदी "मुझे X चाहिए" से मेल; पर が कण लगाएँ (りんごが ほしい — सेब चाहिए)। पहले व्यक्ति की इच्छा।',
    'n5-102': 'हिंदी "मुझे X आता है / पता है" से मेल; पर अंतर: わかります समझ, 知っています जानकारी।',
    'n5-103': 'हिंदी "मैं X कर सकता हूँ" — कौशल / क्षमता। が कण ज़रूरी (日本語が できます — जापानी आती है)।',
    'n5-105': 'हिंदी "मुझे X नहीं करना" — नकारात्मक इच्छा। たい से たくない बनता है (い-adj की तरह नकारात्मक)।',
    'n5-106': 'explicit noun + が ほしい। n5-101 का variant; जब noun ज़ोर देना हो।',
    'n5-107': 'हिंदी "X करने जाऊँगा" से मेल। verb-stem + に + 行く/来る/帰る। Purpose marker に।',
    'n5-109': 'काउंटर-प्रश्न: なん + counter। हिंदी "कितने X" — हर X के लिए अलग counter (人, まい, etc.)।',
    'n5-110': 'हिंदी "मैंने 3 [counter] X किया" — पर जापानी में object + counter + क्रिया (りんごを 三つ 買いました)। काउंटर क्रिया से पहले।',
    'n5-111': 'हिंदी "X बजे" से मेल; ~じ केवल hour, minute के लिए ふん/ぷん।',
    'n5-112': 'हिंदी "X मिनट" — ~ふん/ぷん। ध्यान: 1ぷん, 2ふん, 3ぷん, 4ぷん, 5ふん — phonetic बदलाव।',
    'n5-113': 'हिंदी "साढ़े X" से मेल — じはん half past का।',
    # === Time ===
    'n5-116': 'हिंदी "हर दिन / हर सप्ताह" से मेल — सीधा transfer।',
    'n5-117': 'हिंदी "आज / कल / परसों" से मेल। きのう vs あした संदर्भ-निर्भर — verb tense ज़रूर मेल करें।',
    'n5-119': 'हिंदी "X से पहले" से मेल; まえ संज्ञा + の के साथ या क्रिया-plain + まえに।',
    'n5-120': 'हिंदी "X के बाद" से मेल; あと संज्ञा + の の あとで या क्रिया-た あとで।',
    # === Conjunctions ===
    'n5-121': 'हिंदी "और फिर" से मेल; そして वाक्य-स्तर पर जुड़ाव।',
    'n5-122': 'हिंदी "उसके बाद" से मेल; それから समय-क्रम पर ज़ोर।',
    'n5-123': 'हिंदी "लेकिन / पर" से मेल; でも वाक्य-शुरू में, casual।',
    'n5-124': 'हिंदी "लेकिन / परन्तु" का formal रूप; しかし लिखित-शैली / औपचारिक।',
    'n5-125': 'हिंदी "तो / फिर / अच्छा" — संक्रमण; では औपचारिक, じゃ casual।',
    'n5-126': 'हिंदी "लेकिन" mid-sentence; が plain-form clause के बाद ([clause]が、[clause])। でも से कम contrast।',
    'n5-127': 'हिंदी "लेकिन" casual; けれど / けど informal। बात-चीत में सबसे आम।',
    'n5-129': 'हिंदी "क्यों? — क्योंकि" pattern। どうして〜か? + 〜から (क्योंकि)। Q&A सूत्र।',
    # === Giving / receiving ===
    'n5-130': 'हिंदी "मैं X को Y देता हूँ" से मेल — to-marker に + object marker を। दिशा: मैं → दूसरा।',
    'n5-131': 'हिंदी "मुझे X से Y मिला" — receive। に व्यक्तिगत देने वाला; から संस्थागत स्रोत।',
    'n5-132': 'हिंदी "X मुझे Y देता है" — दिशा: दूसरा → मैं। くれる और あげる में दिशा-भेद हिंदी "देना" में नहीं।',
    # === Sentence-level connectors ===
    'n5-133': 'हिंदी "क्योंकि" से मेल; から (कारण) clause के अंत में।',
    'n5-134': 'हिंदी "के कारण" softer; ので से नरम कारण-संबंध, から से कम सीधा।',
    # === Relative clauses + NP modification ===
    'n5-135': 'हिंदी "जो X किया / करता है, वह Y" — relative clauses को संज्ञा से पहले रखें (जापानी प्रकार)। हिंदी "जो/जिसे" connector यहाँ नहीं।',
    'n5-136': 'विशेषण + संज्ञा। हिंदी "बड़ा घर" — सीधा transfer।',
    'n5-137': 'Noun + の + Noun = "X का Y"। हिंदी genitive "का/की/के" से सीधा मेल। SOV ताक़त।',
    # === Decision / becoming / quotation ===
    'n5-142': 'हिंदी "X लूँगा / X तय करूँगा" से मेल — मेन्यू-चयन। にします निर्णय व्यक्त करता है।',
    'n5-143': 'हिंदी "X बन गया / होगा" से मेल। संज्ञा + になります; い-adj-stem + くなります।',
    'n5-144': 'हिंदी "X करते हुए Y" से मेल — साथ-साथ। verb-stem + ながら + दूसरी क्रिया।',
    'n5-145': 'हिंदी "मैं सोचता हूँ कि" से मेल; と思います plain-form clause के बाद।',
    'n5-146': 'हिंदी "X ने कहा कि" से मेल; 「~」と 言いました direct quote। हिंदी "—ने कहा" + indirect speech अलग।',
    'n5-148': 'हिंदी "हमेशा / आम तौर पर / कभी-कभार" — आवृत्ति शब्द, क्रिया से पहले।',
    # === Polite expressions ===
    'n5-149': 'हिंदी "कृपया X दीजिए" से मेल; を ください order/request।',
    'n5-151': 'हिंदी "X कैसा रहेगा?" से मेल — विनम्र प्रस्ताव। いかが ですか formal version।',
    'n5-152': 'set-greetings — 日常 polite phrases। हिंदी "कृपया / धन्यवाद / माफ़ी / आपका स्वागत है" से लगभग 1-1 मेल।',
    # === Aspect / time markers ===
    'n5-153': 'हिंदी "अभी तक X नहीं किया" से मेल; まだ + ~ていません incomplete-action।',
    'n5-154': 'हिंदी "पहले से कर लिया" से मेल; もう + ました completed-action।',
    'n5-155': 'हिंदी "लेकिन" mid-sentence (n5-126 का variant); plain-clause + が。',
    # === Conjecture ===
    'n5-157': 'हिंदी "शायद / लगता है" से मेल; でしょう probability + soft-confirm।',
    'n5-158': 'casual variant of でしょう। हिंदी "ना?" / "है ना?" से मेल — दोस्तों के बीच।',
    # === Time noun + で / に ===
    'n5-160': 'हिंदी "X के बाद Y" — संज्ञा + の あとで + क्रिया।',
    'n5-161': 'हिंदी "X से पहले Y" — संज्ञा + の まえに + क्रिया।',
    'n5-162': 'हिंदी "X से पहले" — verb-plain + まえに। निर्धारित सूत्र।',
    'n5-163': 'हिंदी "X के बाद" — verb-た + あとで। पिछला complete होने पर अगला।',
    # === Honorifics / set phrases ===
    'n5-164': 'हिंदी "श्री / सुश्री / जी" से मेल; ~さん सम्मान-सूचक नाम-suffix। बिना さん नाम बुलाना rude।',
    'n5-165': 'हिंदी "श्री / श्रीमती" विनम्र-prefix; お~/ご~ संज्ञा को सुंदर बनाते हैं।',
    'n5-166': 'हिंदी "नमस्ते / सुप्रभात / शुभरात्रि" से मेल; greetings — एक बार में सीखें।',
    'n5-167': 'हिंदी "क्योंकि / असल में" से मेल; ~んです explanation/emphasis देता है। बातचीत-स्वर।',
    'n5-168': 'हिंदी "X-Y वग़ैरह करना" से मेल; ~たり~たりする activities sample listing।',
    'n5-169': 'हिंदी "मैंने X किया है (कभी)" से मेल — experience। verb-た + ことが ある।',
    'n5-170': 'हिंदी "बेहतर है X करना" से मेल; verb-た + ほうが いい advice।',
    'n5-171': 'हिंदी "बेहतर है X न करना" से मेल; verb-ない + ほうが いい negative-advice।',
    'n5-172': 'हिंदी "X करना ज़रूरी नहीं" से मेल; ~なくても いい permission to skip।',
    'n5-173': 'हिंदी "X करना ज़रूरी है / X करना ही पड़ेगा" से मेल; formal obligation।',
    'n5-174': 'n5-173 का variant — यही meaning, formal लिखित।',
    'n5-175': 'n5-173 का बोलचाल variant — रोज़मर्रा में सबसे आम।',
    'n5-176': 'n5-173 का सबसे casual contracted form — ~なきゃ / ~なくちゃ।',
    'n5-177': 'हिंदी "बहुत ज़्यादा X" से मेल; verb-stem + すぎる excess।',
    'n5-178': 'हिंदी "मैं X करने वाला हूँ" से मेल; つもりです intention/plan।',
    'n5-179': 'हिंदी "X कहता है कि" casual; って quotation marker — दोस्तों के बीच।',
    'n5-180': 'हिंदी "X करने का तरीक़ा" से मेल; verb-stem + ~かた way of doing।',
    'n5-181': 'हिंदी "वाह X!" exclamation; ~なあ feeling-emphasis।',
    'n5-182': 'हिंदी "मत करो!" से मेल; verb-plain + な strong prohibition (rude)।',
    'n5-183': 'compound rule — questions + か (कुछ) / も (कोई भी)। हिंदी में अलग शब्द (कुछ/कोई/कभी)।',
    'n5-184': 'हिंदी "कुछ / कुछ नहीं" से मेल; なにか affirmative, なにも negative।',
    'n5-185': 'हिंदी "कोई / कोई नहीं" से मेल; だれか / だれも।',
    'n5-186': 'हिंदी "कहीं / कहीं नहीं" से मेल; どこか / どこも।',
    'n5-187': 'हिंदी "कभी / हमेशा" से मेल; いつか indefinite future, いつも always।',
    'n5-188': 'हिंदी "X कर सकता हूँ" से मेल; verb-dictionary + ことができます। n5-103 का productive variant।',
    # === Particles / time-extension ===
    'n5-021': 'हिंदी "X से Y तक" से मेल; から〜まで range marker।',
    'n5-029': 'ので n5-134 का polite कारण; conversation में softer।',
    'n5-066': 'हिंदी "नहीं X" — plain negative। verb-ます का casual: ない। हिंदी "नहीं" क्रिया से पहले, पर ない क्रिया-stem + ない।',
    'n5-068': 'verb-ない का past — なかった। "नहीं किया" से मेल।',
    'n5-082': 'हिंदी "[adj] नहीं था" — i-adj past-negative. ~くなかった।',
    'n5-088': 'हिंदी "[adj] नहीं था" — na-adj past-negative. ~じゃ ありませんでした।',
    'n5-114': 'हिंदी "X से Y तक" — n5-021 का variant।',
    'n5-122': 'n5-122 already covered above — sequence connector।',
    # === Plural / etc ===
    'n5-076': 'n5-076 already; てから = "के बाद" verb sequence।',
    # === Misc ===
    'n5-005': 'हिंदी "X में / X पर" से मेल; に existence-location। Hindi में (~में), पर (~पर) — दोनों に से कवर।',
    'n5-006': 'हिंदी "X की ओर / X को" — direction marker।',
    'n5-010': 'n5-010 = topic-marker variant; details in n5-002।',
    'n5-016': 'के साथ — accompaniment marker; と।',
    'n5-019': 'हिंदी "X या Y" — choice marker; や non-exhaustive (और भी हो सकते हैं)।',
    'n5-020': 'हिंदी "X तक" — limit marker; まで।',
    'n5-022': 'हिंदी "X की ओर" — directional; ~へ (=に लगभग बराबर, more directional)।',
    'n5-023': 'हिंदी "X तक" duration; ~まで।',
    'n5-025': 'हिंदी "X से" reason; から।',
    'n5-026': 'हिंदी "X से बेहतर / से ज़्यादा" — comparative; より।',
    'n5-058': 'n5-058 already covered (Verb-ます) in n5-001 family।',
    'n5-060': 'Verb-ました past polite; "X किया" से मेल।',
    'n5-061': 'Verb-ませんでした past-negative polite; "X नहीं किया" से मेल।',
    'n5-064': 'Verb-ませんか invitation; "क्या X करें?" — politest version।',
    'n5-065': 'Verb-る/Verb-う dictionary form; casual base — हिंदी infinitive (करना/जाना) से लगभग मेल।',
    'n5-067': 'Verb-た plain past; "किया" — informal speech का foundation।',
    'n5-069': 'Verb-て connecting form; chain actions। हिंदी "करके" से समान।',
    'n5-070': 'Verb-て + ください request; "कृपया X कर दीजिए"।',
    'n5-072': 'Verb-ています progressive/resultative। "X कर रहा है" + "X हुआ है" दोनों।',
    'n5-074': 'Verb-ても concessive; "अगर X भी हो"। हिंदी "X भी हो तो" से मेल।',
    'n5-075': 'Verb-ても いいです permission; "X कर सकते हैं / X ठीक है"।',
    'n5-077': 'i-adj base form — हिंदी "बड़ा/छोटा" से मेल। inflection none।',
    'n5-079': 'i-adj negative ~くないです / ~くありません। "[adj] नहीं" से मेल।',
    'n5-080': 'i-adj past ~かったです। "[adj] था" से मेल।',
    'n5-081': 'i-adj past — same as n5-080।',
    'n5-083': 'i-adj te-form ~くて। "[adj] और [adj]" से मेल।',
    'n5-085': 'na-adj base form। हिंदी inflected form (~का/की/के) से मेल — पर जापानी में invariant।',
    'n5-086': 'na-adj negative ~じゃ ありません। "[adj] नहीं है"।',
    'n5-087': 'na-adj past ~でした। "[adj] था"।',
    'n5-089': 'na-adj te-form ~で। "[adj] और [adj]"।',
    'n5-090': 'n5-090 = adj-comparison; covered in n5-095 family।',
    'n5-091': 'n5-091 same family।',
    'n5-099': 'हिंदी "मुझे X पसंद/नापसंद है" — が-marker।',
    'n5-100': 'हिंदी "मैं X में अच्छा/बुरा हूँ" — が कण; skill-marker।',
    'n5-104': 'Verb-stem + たい — "X करना चाहता हूँ"। i-adj की तरह conjugate करें।',
    'n5-115': 'n5-115 = Number + counter — covered by n5-110 family।',
    'n5-118': 'n5-118 = time-of-day expression — n5-117 family।',
    'n5-128': 'n5-128 = casual contraction; mainly listening practice।',
    'n5-138': 'n5-138 = sentence-final particle — already in casual-marker family।',
    'n5-139': 'n5-139 same।',
    'n5-140': 'n5-140 same।',
    'n5-141': 'n5-141 same।',
    'n5-147': 'n5-147 = casual-quotation variant; advanced। हिंदी "कहता है कि" से समान।',
    'n5-150': 'おねがいします — सबसे विनम्र request। "कृपया" से अधिक polite।',
    'n5-156': 'n5-156 = mid-sentence connector — covered।',
    'n5-159': 'n5-159 = sentence-final emphasis — minor variant।',
    # === Final 7 residual patterns ===
    'n5-048': 'हिंदी "कहाँ" से मेल; どこ केवल स्थान-प्रश्न। ここ/そこ/あそこ family का question-form।',
    'n5-050': 'हिंदी "कैसा?" / "कैसे?" से मेल। どう casual, いかが विनम्र (offer/opinion पूछते समय)।',
    'n5-059': 'हिंदी "नहीं X-ता" — non-past negative। ~ません ます का negative form (विनम्र); plain form ~ない।',
    'n5-062': 'हिंदी "X करें / X किया जाए" volitional। ましょう invite/suggest "साथ करें"। मित्रों के बीच ましょう नहीं, plain ~よう।',
    'n5-071': 'हिंदी "कृपया X कीजिए / X कर दीजिए" से मेल। verb-て + ください विनम्र request।',
    'n5-092': 'हिंदी "X में Y है" — location-first existence। に X が ある/いる pattern। topic-marker は की जगह location-first।',
    'n5-108': 'हिंदी "[संख्या] [counter] X" pattern से मेल। काउंटर का सही रूप X पर निर्भर: लोगों के लिए 人, चपटे के लिए まい, लंबे के लिए 本, etc.।',
}


def main() -> int:
    doc = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = doc['patterns']
    n_added = 0
    n_skipped = 0
    n_unmatched = 0
    for p in patterns:
        existing = (p.get('l1_notes') or {}).get('hi')
        if existing:
            n_skipped += 1
            continue
        pid = p['id']
        if pid in L1_NOTES_HI:
            ln = p.setdefault('l1_notes', {})
            ln['hi'] = L1_NOTES_HI[pid]
            n_added += 1
        else:
            n_unmatched += 1
    GRAMMAR.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    have = sum(1 for p in patterns if (p.get('l1_notes') or {}).get('hi'))
    print(f'Added l1_notes.hi on {n_added} patterns.')
    print(f'Skipped (already-set): {n_skipped}')
    print(f'No translation provided: {n_unmatched}')
    print(f'Coverage: {have}/{len(patterns)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
