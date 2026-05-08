"""JCE-9: Author cultural-context callouts on N5 reading passages.

Adds `cultural_context` field to passages where Japan-specific cultural
references appear and would benefit from inline scaffolding for non-
Japan-resident learners. Authored 2026-05-06 by Claude.

Schema: cultural_context is a string. Renderer is expected to display
this as an inline aside / pop-over after the passage on the reading
page.

Idempotent: skips passages that already have a populated
cultural_context. Marks `cultural_context_provenance: llm_curated` on
each authored entry.

The 16 passages that already have cultural_context (authored by an
earlier round) are not touched. This script adds 18 more.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READING = ROOT / 'data' / 'reading.json'

CALLOUTS = {
    'n5.read.001': (
        'どうぞよろしくおねがいします (douzo yoroshiku onegai shimasu, "please treat me well") '
        'is the standard self-introduction closer in Japan. Used after stating your name, '
        'origin, and what you do. The expected response is こちらこそ、よろしくおねがいします '
        '(kochira koso, yoroshiku onegai shimasu — "same here, pleased to meet you"). Mandatory '
        'in formal first meetings: business, school, neighbours, parents-in-law. Skipping it '
        'reads as cold or rude.'
    ),
    'n5.read.005': (
        'Japanese family terms split between humble (own family) and respectful (someone else\'s). '
        '父 (chichi) / 母 (haha) refer to ONE\'S OWN parents in humble speech to outsiders. '
        'お父さん (otousan) / お母さん (okaasan) refer to someone else\'s parents — or to your own '
        'parents when you are addressing them directly at home. Same pattern: あに / あね '
        '(own older brother / sister) vs お兄さん / お姉さん. This own-vs-others split is core '
        'to Japanese in-group / out-group politeness (うち / そと).'
    ),
    'n5.read.007': (
        'Public and university libraries (図書館) in Japan typically loan books for 2 weeks '
        '(二週間まで), free of charge, with one automatic renewal. Sundays closed (日曜日：休み) '
        'is common at school libraries; public libraries usually close on Mondays instead. '
        'Online catalogs and reservation systems are universal even at small branches. '
        'Quiet-study seating is heavily used.'
    ),
    'n5.read.014': (
        'デパート (depaato) — Japanese department stores like Mitsukoshi, Takashimaya, Isetan, '
        'Daimaru — are upscale with formal customer service (gift-wrapping, doormen on opening). '
        'Each floor has a theme: B1F / basement = food hall (デパ地下), middle floors = '
        'fashion / cosmetics, top floors = restaurants. Sales (バーゲン) run twice a year — '
        'New Year and mid-summer. Prices are fixed; haggling is not a thing.'
    ),
    'n5.read.015': (
        '桜 (sakura, cherry blossom) blooms in late March to early April depending on latitude — '
        'Tokyo around the start of the new fiscal year and the school entrance ceremony (入学式). '
        'さくらを見に行く ("going to see sakura") is 花見 (hanami) — picnicking under the trees, '
        'often with food and beer. Weather services publish a cherry-blossom front (桜前線) '
        'tracking the bloom from Okinawa northward. Sakura is central to Japanese aesthetic '
        'identity.'
    ),
    'n5.read.016': (
        '病院 (byouin) in Japanese means both "hospital" and "doctor\'s clinic" — the same word '
        'covers a small neighbourhood clinic and a large hospital. For a cold or headache, you '
        'visit a small 内科 (naika, internal medicine clinic) and pay a 30% out-of-pocket fee '
        'under the National Health Insurance system; the rest is covered. Same-day walk-ins are '
        'standard at clinics. Pharmacies (薬局, yakkyoku) dispense prescriptions next door.'
    ),
    'n5.read.019': (
        'うみに行く (going to the sea / beach) is a summer staple. Japan is an island nation, '
        'so most major cities are within 1-2 hours of a beach. Popular destinations from Tokyo: '
        'Enoshima, Zushi, Kamakura. From Osaka: Suma. Beach activities are swimming, sunbathing, '
        'and BBQ. Beach huts (海の家, umi-no-ie) operate seasonally July-August serving food and '
        'shaved ice (かき氷, kakigoori).'
    ),
    'n5.read.021': (
        'Tokyo - Osaka is the most-trafficked corridor in Japan. The 新幹線 (shinkansen, '
        'bullet train) is the default choice — about 2.5 hours, runs every 10 minutes, no airport-'
        'security overhead. Flights (ひこうき) compete on cost via low-cost carriers (Peach, '
        'Jetstar Japan). Tokyo airports: Haneda (HND, closer in) and Narita (NRT, farther). '
        'Osaka airports: Itami (ITM, closer in) and Kansai (KIX, on artificial island).'
    ),
    'n5.read.024': (
        'International students (留学生, ryuugakusei) at Japanese universities are '
        'predominantly from China, Korea, Vietnam, Indonesia, Malaysia, Thailand, and Taiwan, '
        'with smaller European / American cohorts. Spanish speakers are a small demographic. '
        'Programs split into short-term exchange (1 year) and full degree (4 years for '
        'undergraduate, 2-3 for graduate). Most universities offer Japanese-language preparatory '
        'years for students who arrive without N1.'
    ),
    'n5.read.025': (
        '土曜日 (Saturday) weekend culture: most Japanese workers have Saturday off (週休二日制, '
        'two-day weekend) but many shops, schools, and small businesses still operate Saturday '
        'mornings. Saturday morning is often used for personal hobbies — reading, gardening, '
        'morning walks (さんぽ), gym. Sundays are typically family time. The Friday-night '
        '"weekend start" greeting is はなきん (hana-kin, from 花金 = "flower Friday").'
    ),
    'n5.read.028': (
        'Japanese bedrooms (寝室, しんしつ) are typically small — 4 to 6 jou (about 7-10 m²). '
        'Western-style beds (ベッド) are common in apartments; traditional ふとん (futon) on '
        'tatami floors is still common in rural homes and ryokan inns. The futon is rolled out '
        'at night and stored in a closet (押入れ, oshiire) by day, freeing the room for daytime use.'
    ),
    'n5.read.031': (
        'Pet culture in Japan: small breeds dominate — toy poodles, dachshunds, Chihuahuas, and '
        'native Shiba Inu. Pets are walked daily, often in stroller carriers in summer to avoid '
        'hot pavement. シロ (Shiro = "white") is a classic Japanese pet name pattern, alongside '
        'タロー / ハナ / モモ. Pet ownership in apartments requires landlord approval; many '
        'older buildings prohibit pets entirely.'
    ),
    'n5.read.032': (
        'アルバイト (arubaito, from German "Arbeit"; often shortened バイト, baito) — part-time '
        'jobs are nearly universal among Japanese university students. Café / convenience store / '
        'restaurant / cram school are most common. 5-9 PM after classes is the standard shift. '
        'Hourly wages start around ¥1,000-1,200; tips do not exist. Many students save for travel '
        '(旅行) or technology purchases.'
    ),
    'n5.read.038': (
        'Piano (ピアノ) is among Japan\'s most popular childhood arts (alongside swimming, '
        'English conversation, and abacus). Yamaha and Kawai dominate the instrument market '
        'globally and are Japanese brands. Piano teachers operate small home studios (ピアノ教室) '
        'in residential neighbourhoods. Year-end recitals (発表会, happyoukai) are a major ritual; '
        'parents film the performance.'
    ),
    'n5.read.040': (
        'Japanese parks (公園, kouen) function as community hubs. Even small neighbourhood parks '
        '(within 5-min walk of most homes in cities) typically have a children\'s play area '
        '(子供の遊び場), benches for elderly residents, and a baseball / soccer-friendly open space. '
        'Public morning radio-exercise (ラジオ体操) sessions still run at some parks in summer for '
        'children and seniors.'
    ),
    'n5.read.043': (
        'Visiting the doctor (病院 / clinic) for a cold (かぜ) or fever (ねつ) is normal '
        'preventive care in Japan, not just for emergencies. The doctor will likely prescribe '
        'medication, recommend rest at home, and issue a 診断書 (medical certificate) if you '
        'need to skip work. National Health Insurance covers 70% of costs; you pay 30% on the '
        'spot. Pharmacies (薬局) are next door to the clinic.'
    ),
    'n5.read.044': (
        'Mother\'s birthday gift culture: in Japan, flowers (花) — typically carnations or roses '
        '— and a department-store-wrapped item (デパートでプレゼント) are the formal pattern. '
        'Mother\'s Day (母の日) is the second Sunday of May; carnations are the traditional Mother\'s '
        'Day flower (the colour signals different meanings: red for living mothers, white for '
        'remembrance). Birthday gifts overlap with this convention.'
    ),
    'n5.read.045': (
        'Japanese banking (銀行) employees follow a traditional salaryman routine: leave home '
        '~8:30 AM, commute by train (~30 minutes), arrive at the office by 9 AM, paper-based '
        'work, lunch at 12-1, work until 6-7 PM. Major banks (メガバンク): Mitsubishi UFJ '
        '(三菱UFJ), Sumitomo Mitsui (三井住友), Mizuho (みずほ). Bank teller (窓口担当) is a '
        'typical entry-level role; rotation across branches is standard for early-career staff.'
    ),
}


def main():
    with READING.open('r', encoding='utf-8') as f:
        data = json.load(f)

    passages = data['passages']
    by_id = {p['id']: p for p in passages}

    matched = 0
    skipped_have = 0
    not_found = []
    for pid, callout in CALLOUTS.items():
        p = by_id.get(pid)
        if p is None:
            not_found.append(pid)
            continue
        if p.get('cultural_context'):
            skipped_have += 1
            continue
        p['cultural_context'] = callout
        p['cultural_context_provenance'] = 'llm_curated'
        matched += 1

    print(f'Authored cultural_context on {matched} passages.')
    print(f'Skipped (already had cultural_context): {skipped_have}.')
    if not_found:
        print(f'IDs not found in reading.json: {not_found}')

    with READING.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote: {READING}')


if __name__ == '__main__':
    main()
