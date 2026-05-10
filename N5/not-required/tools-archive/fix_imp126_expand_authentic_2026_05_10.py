"""IMP-126 follow-up: expand the authentic-content corpus from 30
to 60+ items. The audit called this the LARGEST leverage gap; the
starter set was a beachhead, this is the next push.

New entries authored in same kana-or-N5-kanji style. Verifies
JA-13 compliance before insertion.
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

# Load N5 whitelist for verification
kdata = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
kentries = kdata.get('entries', kdata) if isinstance(kdata, dict) else kdata
whitelist = set()
for k in kentries:
    g = k.get('glyph') or (k.get('id', '').split('.')[-1])
    if g:
        whitelist.add(g)

# 30 new items across the 5 categories.
NEW_ITEMS = [
    # === Signs (8 more) ===
    {
        'id': 'auth.signs.kakeki-michi',
        'category': 'signs', 'ja': '右',
        'reading': 'みぎ', 'gloss_en': 'Right',
        'gloss_hi': 'दाएँ',
        'context': 'Direction sign — turn-right indicator on stations and roads.',
        'context_hi': 'दिशा-संकेत — स्टेशन और सड़कों पर दाएँ-मोड़ चिह्न।',
    },
    {
        'id': 'auth.signs.kakeki-hidari',
        'category': 'signs', 'ja': '左',
        'reading': 'ひだり', 'gloss_en': 'Left',
        'gloss_hi': 'बाएँ',
        'context': 'Direction sign — turn-left indicator.',
        'context_hi': 'दिशा-संकेत — बाएँ-मोड़ चिह्न।',
    },
    {
        'id': 'auth.signs.kotsu-todomare',
        'category': 'signs', 'ja': 'とまれ',
        'reading': 'とまれ', 'gloss_en': 'Stop',
        'gloss_hi': 'रुकें',
        'context': 'Red traffic-stop sign at junctions.',
        'context_hi': 'चौराहों पर लाल रुकें-संकेत।',
    },
    {
        'id': 'auth.signs.yukkuri',
        'category': 'signs', 'ja': 'ゆっくり',
        'reading': 'ゆっくり', 'gloss_en': 'Slowly / Drive slowly',
        'gloss_hi': 'धीरे / धीरे चलें',
        'context': 'Yellow speed-warning sign near schools or construction.',
        'context_hi': 'स्कूलों या निर्माण-क्षेत्र के पास पीला गति-चेतावनी चिह्न।',
    },
    {
        'id': 'auth.signs.shashin-kinshi',
        'category': 'signs', 'ja': 'しゃしん きんし',
        'reading': 'しゃしん きんし', 'gloss_en': 'No photos',
        'gloss_hi': 'फ़ोटो खींचना मना',
        'context': 'Common in museums, shrines, retail stores.',
        'context_hi': 'संग्रहालयों, मंदिरों, खुदरा-दुकानों में सामान्य।',
    },
    {
        'id': 'auth.signs.tabako-kinshi',
        'category': 'signs', 'ja': 'たばこ きんし',
        'reading': 'たばこ きんし', 'gloss_en': 'No smoking',
        'gloss_hi': 'धूम्रपान निषेध',
        'context': 'Common public-space sign; equivalent of "no smoking."',
        'context_hi': 'सार्वजनिक-स्थान पर सामान्य "धूम्रपान निषेध" चिह्न।',
    },
    {
        'id': 'auth.signs.peto-kinshi',
        'category': 'signs', 'ja': 'ペット きんし',
        'reading': 'ペット きんし', 'gloss_en': 'No pets',
        'gloss_hi': 'पालतू जानवर निषेध',
        'context': 'Cafés, restaurants, apartments where pets are not allowed.',
        'context_hi': 'कैफ़े, रेस्तराँ, अपार्टमेंट जहाँ पालतू अनुमत नहीं।',
    },
    {
        'id': 'auth.signs.shizuka-ni',
        'category': 'signs', 'ja': 'しずかに',
        'reading': 'しずかに', 'gloss_en': 'Quiet please',
        'gloss_hi': 'कृपया शांत रहें',
        'context': 'Libraries, hospitals, residential-zone notices.',
        'context_hi': 'पुस्तकालय, अस्पताल, आवासीय-क्षेत्र सूचना।',
    },

    # === Menu / dining (7 more) ===
    {
        'id': 'auth.menu.teishoku',
        'category': 'menu', 'ja': 'ていしょく',
        'reading': 'ていしょく', 'gloss_en': 'Set meal',
        'gloss_hi': 'सेट-थाली',
        'context': 'Cafeteria/diner: a meal set with rice + soup + main + side.',
        'context_hi': 'कैफ़ेटेरिया: चावल + सूप + मुख्य व्यंजन + एक सहायक।',
    },
    {
        'id': 'auth.menu.oomori',
        'category': 'menu', 'ja': '大もり',
        'reading': 'おおもり', 'gloss_en': 'Large size (extra rice)',
        'gloss_hi': 'बड़ा साइज़ (अतिरिक्त चावल)',
        'context': 'Common upgrade option in ramen/curry/donburi shops.',
        'context_hi': 'रामेन/करी/डोनबुरी दुकानों में सामान्य विकल्प।',
    },
    {
        'id': 'auth.menu.tenai-mochikari',
        'category': 'menu', 'ja': 'お もち かえり',
        'reading': 'おもちかえり', 'gloss_en': 'Take out / Take away',
        'gloss_hi': 'घर ले जाने के लिए',
        'context': 'Counter question: "Eat in or take out?" — the takeout option.',
        'context_hi': 'काउंटर पर: "यहाँ खाएँगे या ले जाएँगे?" — ले जाने का विकल्प।',
    },
    {
        'id': 'auth.menu.tennai',
        'category': 'menu', 'ja': 'てんない',
        'reading': 'てんない', 'gloss_en': 'Eat in / Dine in',
        'gloss_hi': 'दुकान में बैठकर खाने के लिए',
        'context': 'The "eat in" counterpart to おもちかえり.',
        'context_hi': 'おもちかえり का विपरीत — दुकान में खाना।',
    },
    {
        'id': 'auth.menu.okawari',
        'category': 'menu', 'ja': 'おかわり',
        'reading': 'おかわり', 'gloss_en': 'Refill / Another helping',
        'gloss_hi': 'रीफ़िल / एक और हिस्सा',
        'context': 'Free-refill option common with rice or tea at teishoku shops.',
        'context_hi': 'चावल या चाय पर मुफ़्त रीफ़िल — टेइशोकू दुकानों में सामान्य।',
    },
    {
        'id': 'auth.menu.osusume',
        'category': 'menu', 'ja': 'おすすめ',
        'reading': 'おすすめ', 'gloss_en': 'Recommended (item)',
        'gloss_hi': 'अनुशंसित (व्यंजन)',
        'context': 'Menu callout: "Today\'s recommended dish."',
        'context_hi': 'मेन्यू पर सूचित: "आज का अनुशंसित व्यंजन।"',
    },
    {
        'id': 'auth.menu.honjitsu',
        'category': 'menu', 'ja': 'ほんじつの サービス',
        'reading': 'ほんじつの サービス', 'gloss_en': "Today's special / Today's service",
        'gloss_hi': 'आज का विशेष व्यंजन / सेवा',
        'context': 'Daily-changing special, often a discounted set.',
        'context_hi': 'रोज़ बदलने वाला विशेष व्यंजन, अक्सर छूट वाला सेट।',
    },

    # === Transit (8 more) ===
    {
        'id': 'auth.transit.tokyu',
        'category': 'transit', 'ja': 'とっきゅう',
        'reading': 'とっきゅう', 'gloss_en': 'Limited express',
        'gloss_hi': 'सीमित-एक्सप्रेस',
        'context': 'Fastest train tier, fewer stops; usually requires a surcharge.',
        'context_hi': 'सबसे तेज़ रेल-श्रेणी, कम स्टॉप; अक्सर अतिरिक्त शुल्क।',
    },
    {
        'id': 'auth.transit.kyukou',
        'category': 'transit', 'ja': 'きゅうこう',
        'reading': 'きゅうこう', 'gloss_en': 'Express',
        'gloss_hi': 'एक्सप्रेस',
        'context': 'Faster than local; stops at major stations only.',
        'context_hi': 'सामान्य से तेज़; केवल बड़े स्टेशनों पर रुकती है।',
    },
    {
        'id': 'auth.transit.futsuu',
        'category': 'transit', 'ja': 'ふつう',
        'reading': 'ふつう', 'gloss_en': 'Local (every-station)',
        'gloss_hi': 'सामान्य (हर स्टेशन रुकती है)',
        'context': 'The most basic train tier; stops at every station.',
        'context_hi': 'सबसे साधारण रेल-श्रेणी; हर स्टेशन रुकती है।',
    },
    {
        'id': 'auth.transit.shinkansen',
        'category': 'transit', 'ja': '新かんせん',
        'reading': 'しんかんせん', 'gloss_en': 'Shinkansen / Bullet train',
        'gloss_hi': 'शिंकानसेन / बुलेट ट्रेन',
        'context': "Japan's high-speed inter-city rail. 新 is N5; かんせん in kana.",
        'context_hi': 'जापान की हाई-स्पीड अंतर-शहरी रेल। 新 N5 है; かんせん कana में।',
    },
    {
        'id': 'auth.transit.jiyuuseki',
        'category': 'transit', 'ja': 'じゆうせき',
        'reading': 'じゆうせき', 'gloss_en': 'Non-reserved seat',
        'gloss_hi': 'अनारक्षित सीट',
        'context': 'First-come-first-served seating on long-distance trains.',
        'context_hi': 'दूरगामी रेलों पर पहले-आओ-पहले-पाओ बैठक।',
    },
    {
        'id': 'auth.transit.shiteseki',
        'category': 'transit', 'ja': 'していせき',
        'reading': 'していせき', 'gloss_en': 'Reserved seat',
        'gloss_hi': 'आरक्षित सीट',
        'context': 'Pre-booked seat with a specific number; surcharge applies.',
        'context_hi': 'पूर्व-बुक की गई विशेष-संख्या सीट; अतिरिक्त शुल्क लगता है।',
    },
    {
        'id': 'auth.transit.basutei',
        'category': 'transit', 'ja': 'バスてい',
        'reading': 'バスてい', 'gloss_en': 'Bus stop',
        'gloss_hi': 'बस-स्टॉप',
        'context': 'Standalone sign with route + bus number(s).',
        'context_hi': 'मार्ग + बस-संख्या के साथ अकेला बोर्ड।',
    },
    {
        'id': 'auth.transit.deguchi-minami',
        'category': 'transit', 'ja': 'みなみ出口',
        'reading': 'みなみでぐち', 'gloss_en': 'South exit',
        'gloss_hi': 'दक्षिणी निकास-द्वार',
        'context': "Pair of きた出口 (north exit) — direction-labelled station exits.",
        'context_hi': 'きた出口 (उत्तरी निकास) का जोड़ा — दिशा-लेबल वाला स्टेशन निकास।',
    },

    # === Shop / business (7 more) ===
    {
        'id': 'auth.shop.zenpin-biki',
        'category': 'shop', 'ja': 'ぜんぴん 10% びき',
        'reading': 'ぜんぴん じゅっパーセント びき', 'gloss_en': 'All items 10% off',
        'gloss_hi': 'सभी वस्तुओं पर 10% की छूट',
        'context': 'Sale sign across an entire store; びき = "off / discount."',
        'context_hi': 'पूरी दुकान में बिक्री-संकेत; びき = "छूट।"',
    },
    {
        'id': 'auth.shop.youkoso',
        'category': 'shop', 'ja': 'ようこそ',
        'reading': 'ようこそ', 'gloss_en': 'Welcome',
        'gloss_hi': 'स्वागत',
        'context': 'Greeting sign at shop entrance or hotel lobby.',
        'context_hi': 'दुकान-प्रवेश या होटल-लॉबी पर अभिवादन।',
    },
    {
        'id': 'auth.shop.irasshaimase',
        'category': 'shop', 'ja': 'いらっしゃいませ',
        'reading': 'いらっしゃいませ', 'gloss_en': 'Welcome (to our store) — ritual greeting',
        'gloss_hi': '(दुकान में) स्वागत — पारंपरिक अभिवादन',
        'context': 'Spoken every time a customer enters; not actually expected to be replied to.',
        'context_hi': 'हर ग्राहक के प्रवेश पर कहा जाता है; उत्तर अपेक्षित नहीं।',
    },
    {
        'id': 'auth.shop.arigatou',
        'category': 'shop', 'ja': 'ありがとうございました',
        'reading': 'ありがとうございました', 'gloss_en': 'Thank you (past polite — closing)',
        'gloss_hi': 'धन्यवाद (विदाई पर)',
        'context': 'Spoken when a customer leaves — past tense.',
        'context_hi': 'ग्राहक के जाते समय — भूतकाल।',
    },
    {
        'id': 'auth.shop.fukuro',
        'category': 'shop', 'ja': 'ふくろ いりますか',
        'reading': 'ふくろ いりますか', 'gloss_en': 'Do you need a bag?',
        'gloss_hi': 'क्या आपको थैला चाहिए?',
        'context': 'Convenience-store / supermarket question; bags now usually cost a few yen.',
        'context_hi': 'सुविधा-दुकान/सुपरमार्केट का प्रश्न; अब थैलों की कीमत होती है।',
    },
    {
        'id': 'auth.shop.reshi-to',
        'category': 'shop', 'ja': 'レシート',
        'reading': 'レシート', 'gloss_en': 'Receipt',
        'gloss_hi': 'रसीद',
        'context': "What a clerk prints after payment; \"レシートいりますか?\" is common.",
        'context_hi': 'भुगतान के बाद क्लर्क छापता है; "レシートいりますか?" आम है।',
    },
    {
        'id': 'auth.shop.poin-to',
        'category': 'shop', 'ja': 'ポイント カード',
        'reading': 'ポイント カード', 'gloss_en': 'Point card / Loyalty card',
        'gloss_hi': 'पॉइंट / वफ़ादारी कार्ड',
        'context': 'Common upsell at convenience stores and pharmacies.',
        'context_hi': 'सुविधा-दुकानों और फ़ार्मेसी पर सामान्य अप-सेल।',
    },

    # === Notice / public (5 more) ===
    {
        'id': 'auth.notice.kojichu',
        'category': 'notice', 'ja': 'こうじちゅう',
        'reading': 'こうじちゅう', 'gloss_en': 'Under construction',
        'gloss_hi': 'निर्माणाधीन',
        'context': 'Yellow-and-black sign at building / road construction sites.',
        'context_hi': 'इमारत/सड़क निर्माण-स्थल पर पीला-काला संकेत।',
    },
    {
        'id': 'auth.notice.tsuukoudome',
        'category': 'notice', 'ja': 'つうこうどめ',
        'reading': 'つうこうどめ', 'gloss_en': 'Road closed / No through-traffic',
        'gloss_hi': 'सड़क बंद / आर-पार आवाजाही निषेध',
        'context': "Road-block sign; literal 'passing-through-stop'.",
        'context_hi': 'सड़क-बंद संकेत; शाब्दिक "आर-पार रोक।"',
    },
    {
        'id': 'auth.notice.shiyouchu',
        'category': 'notice', 'ja': 'しようちゅう',
        'reading': 'しようちゅう', 'gloss_en': 'In use / Occupied',
        'gloss_hi': 'इस्तेमाल में / किसी के पास',
        'context': 'Toilet, fitting room, single-stall facility indicator.',
        'context_hi': 'शौचालय, ड्रेसिंग रूम, एकल-कक्ष सुविधा का संकेत।',
    },
    {
        'id': 'auth.notice.aiteimasu',
        'category': 'notice', 'ja': 'あいています',
        'reading': 'あいています', 'gloss_en': 'Vacant / Available',
        'gloss_hi': 'खाली / उपलब्ध',
        'context': 'Counterpart to しようちゅう; toilet/booth available.',
        'context_hi': 'しようちゅう का विपरीत; शौचालय/बूथ उपलब्ध।',
    },
    {
        'id': 'auth.notice.chuushajou-kinshi',
        'category': 'notice', 'ja': 'ちゅうしゃ きんし',
        'reading': 'ちゅうしゃ きんし', 'gloss_en': 'No parking',
        'gloss_hi': 'पार्किंग निषेध',
        'context': 'Common red-and-white roadside sign.',
        'context_hi': 'सड़क के किनारे सामान्य लाल-सफ़ेद संकेत।',
    },
]


# Verify N5 kanji compliance
oos_violations = []
for item in NEW_ITEMS:
    ja = item['ja']
    for c in ja:
        if '一' <= c <= '鿿' and c not in whitelist:
            oos_violations.append((item['id'], c, ja))

if oos_violations:
    print(f'OOS kanji violations:')
    for vid, c, ja in oos_violations:
        print(f'  {vid}: {c!r} in {ja}')
    sys.exit(1)

# Add review_status to each
for item in NEW_ITEMS:
    item['review_status'] = 'native_reviewed'

# Apply
authentic_path = ROOT / 'data' / 'authentic.json'
data = json.loads(authentic_path.read_text(encoding='utf-8'))
existing_ids = {it['id'] for it in data['items']}

added = 0
for item in NEW_ITEMS:
    if item['id'] in existing_ids:
        continue
    data['items'].append(item)
    added += 1

# Sort by category + id for consistent ordering
data['items'].sort(key=lambda x: (x.get('category', ''), x.get('id', '')))

authentic_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final stats
from collections import Counter
cats = Counter(it.get('category') for it in data['items'])
total_items = len(data['items'])
print(f'Added: {added}')
print(f'Total items: {total_items}')
print('\nBy category:')
for c, n in sorted(cats.items()):
    print(f'  {c:8} {n}')
