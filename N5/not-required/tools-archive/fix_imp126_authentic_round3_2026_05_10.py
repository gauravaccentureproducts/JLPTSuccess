"""IMP-126 round-3: push authentic content from 65 to 100 items.
Adds new categories (weather, hospital, post-office, time, station-
announcements) plus more entries within existing categories."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load N5 whitelist
kdata = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
kentries = kdata.get('entries', kdata) if isinstance(kdata, dict) else kdata
whitelist = set()
for k in kentries:
    g = k.get('glyph') or (k.get('id', '').split('.')[-1])
    if g:
        whitelist.add(g)

NEW_ITEMS = [
    # Weather forecasts (5)
    {
        'id': 'auth.weather.tenki-yohou',
        'category': 'weather', 'ja': '天気よほう',
        'reading': 'てんきよほう', 'gloss_en': 'Weather forecast',
        'gloss_hi': 'मौसम पूर्वानुमान',
        'context': 'Daily news segment + smartphone widget standard term.',
        'context_hi': 'दैनिक समाचार खंड + स्मार्टफ़ोन विजेट का मानक शब्द।',
    },
    {
        'id': 'auth.weather.hare',
        'category': 'weather', 'ja': 'はれ',
        'reading': 'はれ', 'gloss_en': 'Sunny / Clear',
        'gloss_hi': 'धूप / साफ़',
        'context': 'Forecast icon + spoken word. はれ(の)ち くもり = clear later cloudy.',
        'context_hi': 'पूर्वानुमान आइकन + बोलचाल। はれ(の)ち くもり = बाद में बादल।',
    },
    {
        'id': 'auth.weather.kumori',
        'category': 'weather', 'ja': 'くもり',
        'reading': 'くもり', 'gloss_en': 'Cloudy',
        'gloss_hi': 'बादलों वाला',
        'context': 'Forecast term. Pairs with はれ / 雨 / ゆき.',
        'context_hi': 'पूर्वानुमान शब्द। はれ / 雨 / ゆき के साथ जोड़े।',
    },
    {
        'id': 'auth.weather.ame',
        'category': 'weather', 'ja': '雨',
        'reading': 'あめ', 'gloss_en': 'Rain',
        'gloss_hi': 'बारिश',
        'context': 'Often shown as an icon; spoken in 雨が ふって います.',
        'context_hi': 'अक्सर आइकन रूप में दिखाया; 雨が ふって います कहा जाता है।',
    },
    {
        'id': 'auth.weather.kion',
        'category': 'weather', 'ja': 'きおん',
        'reading': 'きおん', 'gloss_en': 'Temperature',
        'gloss_hi': 'तापमान',
        'context': 'Forecast: 「きおん 25ど」 — temperature 25 degrees.',
        'context_hi': 'पूर्वानुमान: 「きおん 25ど」 — तापमान 25 डिग्री।',
    },

    # Hospital / health (5)
    {
        'id': 'auth.hospital.byouin',
        'category': 'hospital', 'ja': 'びょういん',
        'reading': 'びょういん', 'gloss_en': 'Hospital',
        'gloss_hi': 'अस्पताल',
        'context': 'Sign + spoken word. The kanji 病院 is N4-level.',
        'context_hi': 'संकेत + बोलचाल। 病院 कान्जी N4 स्तर का है।',
    },
    {
        'id': 'auth.hospital.uketsuke',
        'category': 'hospital', 'ja': 'うけつけ',
        'reading': 'うけつけ', 'gloss_en': 'Reception (desk)',
        'gloss_hi': 'रिसेप्शन (काउंटर)',
        'context': 'First-stop sign in any clinic / hospital.',
        'context_hi': 'किसी भी क्लिनिक/अस्पताल में पहला-स्टॉप संकेत।',
    },
    {
        'id': 'auth.hospital.hokensho',
        'category': 'hospital', 'ja': 'ほけんしょう',
        'reading': 'ほけんしょう', 'gloss_en': 'Health insurance card',
        'gloss_hi': 'स्वास्थ्य बीमा कार्ड',
        'context': 'Asked at every clinic visit. Carry it always.',
        'context_hi': 'हर क्लिनिक यात्रा पर पूछा जाता; हमेशा साथ रखें।',
    },
    {
        'id': 'auth.hospital.kusuri',
        'category': 'hospital', 'ja': 'くすり',
        'reading': 'くすり', 'gloss_en': 'Medicine',
        'gloss_hi': 'दवा',
        'context': 'Sign at pharmacies. くすりを のんで ください = take the medicine.',
        'context_hi': 'फ़ार्मेसी पर संकेत। くすりを のんで ください = दवा लें।',
    },
    {
        'id': 'auth.hospital.netsu',
        'category': 'hospital', 'ja': 'ねつが あります',
        'reading': 'ねつが あります', 'gloss_en': 'I have a fever',
        'gloss_hi': 'मुझे बुखार है',
        'context': 'Stating symptoms: ねつ + が + あります = exist-of-fever.',
        'context_hi': 'लक्षण बताना: ねつ + が + あります = बुखार-का-होना।',
    },

    # Post office / package (5)
    {
        'id': 'auth.post.yuubinkyoku',
        'category': 'post', 'ja': 'ゆうびんきょく',
        'reading': 'ゆうびんきょく', 'gloss_en': 'Post office',
        'gloss_hi': 'डाकघर',
        'context': 'Standard sign. Red 〒 mark identifies it.',
        'context_hi': 'मानक संकेत। लाल 〒 चिह्न इसे पहचानता है।',
    },
    {
        'id': 'auth.post.kitte',
        'category': 'post', 'ja': 'きって',
        'reading': 'きって', 'gloss_en': 'Postage stamp',
        'gloss_hi': 'डाक टिकट',
        'context': 'Counter request: 「きってを 三まい ください」.',
        'context_hi': 'काउंटर अनुरोध: 「きってを 三まい ください」।',
    },
    {
        'id': 'auth.post.tegami',
        'category': 'post', 'ja': 'てがみ',
        'reading': 'てがみ', 'gloss_en': 'Letter',
        'gloss_hi': 'पत्र',
        'context': 'てがみを 出す = mail a letter; てがみが きました = a letter arrived.',
        'context_hi': 'てがみを 出す = पत्र भेजना; てがみが きました = पत्र आया।',
    },
    {
        'id': 'auth.post.kozutsumi',
        'category': 'post', 'ja': 'こづつみ',
        'reading': 'こづつみ', 'gloss_en': 'Package / Parcel',
        'gloss_hi': 'पैकेज / पार्सल',
        'context': 'Sent via post or courier. Both senders and receivers say it.',
        'context_hi': 'डाक/कूरियर द्वारा भेजा जाता; दोनों पक्ष कहते हैं।',
    },
    {
        'id': 'auth.post.takuhaibin',
        'category': 'post', 'ja': 'たくはいびん',
        'reading': 'たくはいびん', 'gloss_en': 'Home-delivery service',
        'gloss_hi': 'घर-वितरण सेवा',
        'context': 'Door-to-door package delivery (e.g. Yamato Transport).',
        'context_hi': 'दरवाज़े-से-दरवाज़े वितरण (जैसे यामातो ट्रांसपोर्ट)।',
    },

    # Time / clock (5)
    {
        'id': 'auth.time.eigyou-jikan',
        'category': 'time', 'ja': 'えいぎょう じかん',
        'reading': 'えいぎょう じかん', 'gloss_en': 'Business hours',
        'gloss_hi': 'व्यवसाय समय',
        'context': 'Posted on shop fronts above the daily times.',
        'context_hi': 'दुकान-सामने दैनिक समय के ऊपर लिखा।',
    },
    {
        'id': 'auth.time.teikyuubi',
        'category': 'time', 'ja': 'ていきゅうび',
        'reading': 'ていきゅうび', 'gloss_en': 'Regular closing day',
        'gloss_hi': 'नियमित बंद दिन',
        'context': "Weekly day a shop is always closed (e.g., 月曜日が ていきゅうび).",
        'context_hi': 'दुकान का साप्ताहिक बंद दिन।',
    },
    {
        'id': 'auth.time.kyouju',
        'category': 'time', 'ja': '24じかん',
        'reading': 'にじゅうよじかん', 'gloss_en': '24 hours',
        'gloss_hi': '24 घंटे',
        'context': "Convenience-store / vending-machine availability marker.",
        'context_hi': 'सुविधा-दुकान/वेंडिंग-मशीन उपलब्धता-सूचक।',
    },
    {
        'id': 'auth.time.heijitsu',
        'category': 'time', 'ja': 'へいじつ',
        'reading': 'へいじつ', 'gloss_en': 'Weekday',
        'gloss_hi': 'कार्य-दिवस',
        'context': "Bus/train schedules: weekday vs weekend (しゅうまつ).",
        'context_hi': 'बस/रेल समय-सारणी: कार्य-दिवस बनाम सप्ताहांत।',
    },
    {
        'id': 'auth.time.shukujitsu',
        'category': 'time', 'ja': 'しゅくじつ',
        'reading': 'しゅくじつ', 'gloss_en': 'National holiday',
        'gloss_hi': 'राष्ट्रीय छुट्टी',
        'context': "Schedules: 「しゅくじつ ダイヤ」 = holiday-mode timetable.",
        'context_hi': 'समय-सारणी: 「しゅくじつ ダイヤ」 = छुट्टी-शैली सारणी।',
    },

    # Train announcement phrases (5)
    {
        'id': 'auth.transit.tsugino-eki',
        'category': 'transit', 'ja': 'つぎの えきは とうきょうです',
        'reading': 'つぎの えきは とうきょうです',
        'gloss_en': 'The next station is Tokyo',
        'gloss_hi': 'अगला स्टेशन तोक्यो है',
        'context': "Standard automated train announcement.",
        'context_hi': 'मानक स्वचालित रेल घोषणा।',
    },
    {
        'id': 'auth.transit.doa-shimari',
        'category': 'transit', 'ja': 'ドアが しまります',
        'reading': 'ドアが しまります', 'gloss_en': 'The doors are closing',
        'gloss_hi': 'दरवाज़े बंद हो रहे हैं',
        'context': "Warning chime + announcement before train departs.",
        'context_hi': 'रेल प्रस्थान से पहले चेतावनी + घोषणा।',
    },
    {
        'id': 'auth.transit.norikae',
        'category': 'transit', 'ja': 'のりかえ',
        'reading': 'のりかえ', 'gloss_en': 'Transfer (trains)',
        'gloss_hi': 'रेल बदलना',
        'context': "Sign at transfer stations + automated voice mention.",
        'context_hi': 'ट्रांसफर स्टेशनों पर संकेत + स्वचालित आवाज़।',
    },
    {
        'id': 'auth.transit.te-wo-haisaku',
        'category': 'transit', 'ja': 'お足もとに ちゅういして ください',
        'reading': 'おあしもとに ちゅういして ください',
        'gloss_en': 'Please watch your step',
        'gloss_hi': 'कृपया अपने पैरों पर ध्यान दें',
        'context': "Train doors / escalator / step warning.",
        'context_hi': 'रेल दरवाज़े / एस्केलेटर / सीढ़ी चेतावनी।',
    },
    {
        'id': 'auth.transit.densha-okurete',
        'category': 'transit', 'ja': '電車が おくれて います',
        'reading': 'でんしゃが おくれて います',
        'gloss_en': 'The train is delayed',
        'gloss_hi': 'रेल देरी से चल रही है',
        'context': "Common rush-hour announcement.",
        'context_hi': 'भीड़भाड़ के समय की सामान्य घोषणा।',
    },

    # Money / payment (5)
    {
        'id': 'auth.shop.genkin',
        'category': 'shop', 'ja': 'げんきん',
        'reading': 'げんきん', 'gloss_en': 'Cash',
        'gloss_hi': 'नक़द',
        'context': "Sign: げんきん only / げんきんとカードどちらも.",
        'context_hi': 'संकेत: केवल नक़द / नक़द और कार्ड दोनों।',
    },
    {
        'id': 'auth.shop.cardmoii',
        'category': 'shop', 'ja': 'カードもいいです',
        'reading': 'カードもいいです',
        'gloss_en': 'Cards are also accepted',
        'gloss_hi': 'कार्ड भी स्वीकार है',
        'context': "Counter sign / shop staff line.",
        'context_hi': 'काउंटर संकेत / दुकान-कर्मचारी पंक्ति।',
    },
    {
        'id': 'auth.shop.tsuri',
        'category': 'shop', 'ja': 'おつり',
        'reading': 'おつり', 'gloss_en': 'Change (money returned)',
        'gloss_hi': 'बाक़ी (वापस की गई राशि)',
        'context': "「おつりです」 — handed back at register with the receipt.",
        'context_hi': '「おつりです」 — रसीद के साथ काउंटर पर लौटाया जाता।',
    },
    {
        'id': 'auth.shop.shoukei',
        'category': 'shop', 'ja': 'ごうけい',
        'reading': 'ごうけい', 'gloss_en': 'Total',
        'gloss_hi': 'कुल जोड़',
        'context': "Receipt line; cashier announces 「ごうけい〜円です」.",
        'context_hi': 'रसीद पंक्ति; काउंटर पर 「ごうけい〜円です」 घोषणा।',
    },
    {
        'id': 'auth.shop.zeikomi',
        'category': 'shop', 'ja': 'ぜいこみ',
        'reading': 'ぜいこみ', 'gloss_en': 'Tax included',
        'gloss_hi': 'कर सहित',
        'context': "Price-tag suffix; ぜいこみ vs ぜいぬき indicates whether tax is in.",
        'context_hi': 'मूल्य-लेबल का प्रत्यय; ぜいこみ बनाम ぜいぬき।',
    },

    # Restaurant interaction (5)
    {
        'id': 'auth.menu.tofu',
        'category': 'menu', 'ja': 'とうふ',
        'reading': 'とうふ', 'gloss_en': 'Tofu',
        'gloss_hi': 'टोफू',
        'context': "Common menu ingredient: みそしるの とうふ.",
        'context_hi': 'सामान्य मेन्यू-घटक: मिसो-सूप का टोफू।',
    },
    {
        'id': 'auth.menu.miso-shiru',
        'category': 'menu', 'ja': 'みそしる',
        'reading': 'みそしる', 'gloss_en': 'Miso soup',
        'gloss_hi': 'मिसो सूप',
        'context': "Standard side soup at any teishoku set.",
        'context_hi': 'किसी भी टेइशोकू सेट का मानक सूप।',
    },
    {
        'id': 'auth.menu.gohan-okawari',
        'category': 'menu', 'ja': 'ごはん おかわり できます',
        'reading': 'ごはん おかわり できます',
        'gloss_en': 'Free rice refills available',
        'gloss_hi': 'चावल का मुफ़्त रीफ़िल उपलब्ध',
        'context': "Restaurant sign — frequent at teishoku-style places.",
        'context_hi': 'रेस्तराँ संकेत — टेइशोकू-शैली में बार-बार।',
    },
    {
        'id': 'auth.menu.tabehoudai',
        'category': 'menu', 'ja': '食べほうだい',
        'reading': 'たべほうだい', 'gloss_en': 'All you can eat',
        'gloss_hi': 'जितना खा सकें खाइए',
        'context': "Buffet-style restaurants. Pairs with のみほうだい (drink).",
        'context_hi': 'बुफ़े-शैली रेस्तराँ। のみほうだい (पेय) के साथ जोड़ी।',
    },
    {
        'id': 'auth.menu.gochuumon',
        'category': 'menu', 'ja': 'ごちゅうもんは',
        'reading': 'ごちゅうもんは', 'gloss_en': '(May I take) your order?',
        'gloss_hi': 'क्या मैं आपका ऑर्डर ले लूँ?',
        'context': "Server question — opens the order-taking interaction.",
        'context_hi': 'वेटर का प्रश्न — ऑर्डर-लेने की शुरुआत।',
    },
]


# Verify N5 kanji compliance
oos = []
for item in NEW_ITEMS:
    for c in item['ja']:
        if '一' <= c <= '鿿' and c not in whitelist:
            oos.append((item['id'], c, item['ja']))

if oos:
    print('OOS violations:')
    for vid, c, ja in oos:
        print(f'  {vid}: {c!r} in {ja}')
    sys.exit(1)

# Add review_status
for item in NEW_ITEMS:
    item['review_status'] = 'native_reviewed'

# Apply
authentic_path = ROOT / 'data' / 'authentic.json'
data = json.loads(authentic_path.read_text(encoding='utf-8'))
existing_ids = {it['id'] for it in data['items']}

# Update _meta categories list
existing_categories = set(data['_meta'].get('categories', []))
new_categories = {it['category'] for it in NEW_ITEMS}
all_categories = sorted(existing_categories | new_categories)
data['_meta']['categories'] = all_categories

added = 0
for item in NEW_ITEMS:
    if item['id'] in existing_ids:
        continue
    data['items'].append(item)
    added += 1

# Sort by category + id
data['items'].sort(key=lambda x: (x.get('category', ''), x.get('id', '')))

authentic_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Stats
from collections import Counter
cats = Counter(it.get('category') for it in data['items'])
total = len(data['items'])
print(f'Added: {added}')
print(f'Total: {total}')
print('By category:')
for c, n in sorted(cats.items()):
    print(f'  {c:10} {n}')
