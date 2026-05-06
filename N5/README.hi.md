# JLPT N5 ट्यूटर

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![Content: CC BY-SA 4.0](https://img.shields.io/badge/Content-CC%20BY--SA%204.0-lightgrey.svg)](CONTENT-LICENSE.md)
[![JLPT Level: N5](https://img.shields.io/badge/JLPT-N5-14452a.svg)](https://gauravaccentureproducts.github.io/JLPTSuccess/N5/)
[![PWA](https://img.shields.io/badge/PWA-installable-brightgreen.svg)](https://gauravaccentureproducts.github.io/JLPTSuccess/N5/)
[![Locales: EN · HI](https://img.shields.io/badge/locales-EN%20%C2%B7%20HI-blueviolet.svg)](docs/TRANSLATING.md)
[![Privacy: no telemetry](https://img.shields.io/badge/privacy-no%20telemetry-success.svg)](PRIVACY.md)

JLPT N5 की तैयारी के लिए ब्राउज़र-आधारित स्थैतिक वेब ऐप — व्याकरण, शब्दावली, कान्जी, पठन और श्रवण। **कोई सर्वर नहीं। कोई खाता नहीं। कोई तृतीय-पक्ष स्क्रिप्ट नहीं।** बिल्ड टूल (Python) `/tools/` में रहते हैं; सीखने वाला केवल ब्राउज़र चलाता है।

> **2026-05-06 अद्यतन — रणनीतिक ध्यान-केंद्रित: हिंदी।** ऐप पहले 5 भाषाएँ (en/vi/id/ne/zh) समर्थन करता था। बाज़ार अनुसंधान में पाया गया कि **हिंदी एक अनोखा "उच्च माँग, कम प्रतिस्पर्धा" अंतराल है**: भारत JLPT में 5वाँ सबसे बड़ा देश है (~50,000 आवेदक/वर्ष; 73% N5 या N4 स्तर पर); पर समर्पित हिंदी-माध्यम तैयारी ऐप मौजूद नहीं है। 2026-05-06 को ऐप ने en + hi पर ध्यान-केंद्रित किया।

## विशेषताएँ

- **178 N5 व्याकरण पैटर्न** — हर पैटर्न पर ≥3 उदाहरण, ≥1 सामान्य-गलती, हिंदी-वक्ता-विशिष्ट L1 नोट्स (सही पैटर्नों पर — 27/178 अभी)।
- **1,041 N5 शब्दावली प्रविष्टियाँ** — हिंदी अनुवाद, साथ में सहयोगी-शब्द (collocations) उच्च-आवृत्ति प्रविष्टियों पर।
- **106 N5 कान्जी** — मूलाधार (radical) विघटन, स्मृति-संकेत (mnemonic), समान-दिखने वाले समूह, स्ट्रोक-क्रम जाल।
- **45 पठन अनुच्छेद + 47 श्रवण अभ्यास** — मोंदाइ-ट्यागिंग, प्रश्न तर्कसहित, प्रामाणिक JLPT N5 स्वरूप।
- **402 मॉक-परीक्षा प्रश्न (28 पेपर)** — मोजी / गोई / बुनपोऊ / दोक्काइ श्रेणियों में।
- **पूरी तरह से ऑफ़लाइन काम करता है** — सेवा कर्मचारी (service worker) पूरा शेल कैश करता है। पहली ऑनलाइन यात्रा के बाद बिना नेटवर्क काम करता है।

## स्थानीय रूप से चलाएँ

```bash
git clone https://github.com/gauravaccentureproducts/JLPTSuccess.git
cd JLPTSuccess
python -m http.server 8000
# ब्राउज़र में: http://localhost:8000/N5/
```

## हिंदी अनुवाद में योगदान

देखें [`docs/TRANSLATING.md`](docs/TRANSLATING.md) — हिंदी UI / सामग्री समीक्षा कार्यप्रवाह।

## निजता (Privacy)

- कोई लॉगिन नहीं • कोई ट्रैकिंग नहीं • कोई विज्ञापन नहीं • कोई पेवॉल नहीं
- सारी प्रगति आपके ब्राउज़र के localStorage में रहती है (नामस्थान `jlpt-n5-tutor:*`)
- कोई दूरस्थ API कॉल सामान्य उपयोग में नहीं

देखें [`PRIVACY.md`](PRIVACY.md) (अंग्रेज़ी)।

## लाइसेंस

- **कोड**: MIT — देखें `../LICENSE`।
- **शैक्षिक सामग्री**: CC BY-SA 4.0 — देखें `CONTENT-LICENSE.md`।
- **तृतीय-पक्ष**: KanjiVG (CC BY-SA 3.0), Inter, Noto Sans JP — देखें `NOTICES.md`।

## निर्माता-नोट

यह दस्तावेज़ अंग्रेज़ी [`README.md`](README.md) का हिंदी संस्करण है — संक्षिप्त रूप में। पूरी विकास / स्व-होस्टिंग गाइड के लिए मूल README देखें।

---

*अनुप्रयोग 2026-05-06 (v1.12.40+) से EN + HI दो भाषाएँ समर्थन करता है। पुरानी 5-भाषा शाखा (en/vi/id/ne/zh) कमिट इतिहास में `pre-locale-transition` टैग पर सुरक्षित है।*
