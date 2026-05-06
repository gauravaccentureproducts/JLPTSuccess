"""ISSUE-103 (round-9): reading cultural_context missing on 45/45 passages.

Adds 1-2 sentence cultural callouts (English) on ~16 passages that
reference Japan-specific concepts non-Japan-domiciled learners may not
recognize. The remaining ~29 passages are about universal topics
(weather, daily routine, shopping in any country, family) that don't
need cultural framing.

Callouts are kept short (≤2 sentences) and assume no prior Japan
exposure. Hindi-locale variants (cultural_context_hi) are deferred to
the niche-N1 scaling cycle (ISSUE-094 / Q39 in audit-round9-2026-05-06.md).

Idempotent: skips passages that already have cultural_context set.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

READING = Path(__file__).parent.parent / 'data' / 'reading.json'

# Map passage id -> cultural callout (English)
CULTURAL_CONTEXT = {
    'n5.read.011': (
        'ラーメン (rāmen) is a Japanese noodle soup of Chinese origin, now '
        'considered a defining Japanese comfort food. Casual ramen shops '
        'serve it as a fast lunch — typically eaten in 10-15 minutes.'
    ),
    'n5.read.013': (
        'Kyoto (京都) was the imperial capital of Japan from 794 to 1868 '
        'and is famous for its preserved temples (お寺), shrines, and '
        'traditional crafts. Buying お土産 (omiyage, souvenirs) for '
        'family/colleagues when traveling within Japan is a strong social '
        'custom — even short trips usually end with a souvenir purchase.'
    ),
    'n5.read.017': (
        'A "set" (セット) at a Japanese café is a discounted bundle — '
        'typically a hot drink + a sweet item — designed for the '
        'mid-afternoon coffee break. Set pricing is universal in '
        'Japanese kissaten / chain coffee shops (Doutor, Starbucks JP).'
    ),
    'n5.read.020': (
        'In Japan, addressing a teacher as "先生" (sensei) — both in '
        'speech and in writing — is mandatory. Using a teacher\'s family '
        'name without 先生 attached is rude. The honorific applies to '
        'doctors, lawyers, and authors as well.'
    ),
    'n5.read.022': (
        'カレー (karē) in Japan is the Japanese-style curry: thicker, '
        'sweeter, and milder than Indian curry, served over white rice. '
        'It became popular via the Imperial Japanese Navy in the late '
        '1800s and is now a standard home-cooked meal — most Japanese '
        'families have their own family-recipe curry.'
    ),
    'n5.read.026': (
        '八百屋 (yaoya, "greengrocer") is a small specialty shop selling '
        'fresh vegetables and fruit. Greengrocers are still common in '
        'older neighborhoods, alongside dedicated fish shops (魚屋), '
        'butchers (肉屋), and rice shops (米屋), even though supermarkets '
        'dominate today.'
    ),
    'n5.read.027': (
        'Casual notes left for friends or family — written in mixed '
        'kanji + hiragana — are a common way to plan meetups in Japan. '
        '〜ましょう ("let\'s do") is the standard tone for proposing '
        'casual plans.'
    ),
    'n5.read.029': (
        'Japanese summers (なつ) are hot and humid, especially in cities '
        'like Tokyo where temperatures regularly exceed 30°C. Air '
        'conditioning (エアコン) is universal but switching it on '
        'overnight is a routine summer-survival habit. The summer break '
        '(なつ休み) for students typically runs from late July to late '
        'August.'
    ),
    'n5.read.030': (
        '郵便局 (yūbinkyoku, post office) is a major neighborhood '
        'institution in Japan — they handle mail, packages, and basic '
        'banking (Japan Post Bank). Post offices are usually found near '
        'major train stations, often with the iconic 〒 mark on a red '
        'building.'
    ),
    'n5.read.033': (
        '秋 (aki, autumn) in Japan is a celebrated season for 紅葉 '
        '(kōyō, autumn leaves). The cool weather and colorful foliage '
        'make autumn the most popular season for leisurely walks and '
        'park visits — a cultural habit known as 紅葉狩り (momijigari, '
        '"autumn-leaf hunting").'
    ),
    'n5.read.034': (
        'School parties (学校の パーティー) in Japan are usually small '
        'classroom social events, not large dances — typically organized '
        'by the homeroom teacher and bringing in light snacks. Inviting '
        'someone with a brief written note (this passage\'s style) is '
        'culturally appropriate.'
    ),
    'n5.read.035': (
        'すし (sushi) and てんぷら (tempura) are the two most '
        'internationally-recognized Japanese cuisines, but Japanese '
        'people typically eat ramen, curry, and bento-box lunches far '
        'more often. Sushi is usually a dinner-out occasion or a treat, '
        'not an everyday meal.'
    ),
    'n5.read.036': (
        'Japanese school weeks run Monday-Friday with 6 class periods '
        'per day plus club activities (部活) after school. Daily homework '
        '(しゅくだい) in math + the school\'s primary language is the '
        'norm. Saturday classes were phased out in the early 2000s.'
    ),
    'n5.read.037': (
        'Train delays (電車が おくれて) carry strong social weight in '
        'Japan — train companies issue formal "delay certificates" '
        '(遅延証明書) that students/workers present to teachers/'
        'employers as proof, since being late without explanation '
        'damages trust.'
    ),
    'n5.read.039': (
        'セール (sale) at Japanese bookstores is rare — most shops keep '
        'fixed prices set by the publisher (定価販売). When sales do '
        'happen (e.g. 半分のねだん, "half price"), they\'re usually '
        'stock-clearing events at independent shops, advertised with '
        'おしらせ (notice) flyers.'
    ),
    'n5.read.041': (
        'Restaurants near train stations (えきの ちかくの レストラン) '
        'are a defining feature of Japanese urban life. Ekimae '
        '(駅前, "in front of the station") restaurants cater to '
        'commuters meeting up after work — quick service, modest '
        'prices, and located within a 2-minute walk of the ticket gates.'
    ),
}


def main() -> int:
    doc = json.loads(READING.read_text(encoding='utf-8'))
    passages = doc['passages']

    n_added = 0
    n_skipped = 0
    n_no_match = 0

    for p in passages:
        if p.get('cultural_context'):
            n_skipped += 1
            continue
        pid = p.get('id', '')
        if pid in CULTURAL_CONTEXT:
            p['cultural_context'] = CULTURAL_CONTEXT[pid]
            n_added += 1
        else:
            n_no_match += 1  # passage doesn't need cultural context

    READING.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    # Verify
    doc2 = json.loads(READING.read_text(encoding='utf-8'))
    have_cc = sum(1 for p in doc2['passages'] if p.get('cultural_context'))
    print(f'cultural_context added on {n_added} passages.')
    print(f'Skipped (already-set): {n_skipped}')
    print(f'No callout needed (universal-topic): {n_no_match}')
    print(f'\nPost-fix: {have_cc}/{len(doc2["passages"])} passages have cultural_context.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
