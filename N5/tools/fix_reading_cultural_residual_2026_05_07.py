"""Q39-narrowed residual: add cultural_context to the 11 reading
passages that ISSUE-103 left blank because their topics looked
"universal." Subsequent UI test (BUG-2 fix) wired the renderer to
display the field, so even subtle Japan-specific framing on universal
topics adds learner value (commute culture, conbini norms, school
classroom setup, etc.).

Idempotent: skips passages that already have cultural_context.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

READING = Path(__file__).parent.parent / 'data' / 'reading.json'

# Passage id → cultural callout. Each is 1-2 sentences, English,
# explaining the Japan-specific framing on a topic that may look
# universal but has implicit Japanese norms (work hours, conbini,
# school classroom layout, commute patterns, etc.).
CULTURAL_RESIDUAL = {
    'n5.read.002': (
        'A 9-to-5 workday in Japan often stretches longer in practice '
        '(残業, zangyō, "overtime" is common in white-collar roles), '
        'but the polite default written form remains "9 to 5" because '
        'overtime is socially expected, not contractually scheduled. '
        'Reading "wakes at 6, works 9-5" maps to a typical urban '
        'commuting routine.'
    ),
    'n5.read.003': (
        'えいが (movie) + ばんごはん (dinner) is the canonical Japanese '
        'casual outing pairing — equivalent to "dinner and a movie" '
        'in English-speaking countries. Movie tickets in Japan are '
        '¥1,800-2,000 standard, with 1,200 yen "Lady\'s Day" '
        'discounts on Wednesdays still common at major chains.'
    ),
    'n5.read.004': (
        'コンビニ (konbini, "convenience store" — 7-Eleven, FamilyMart, '
        'Lawson) are central to Japanese daily life: fresh bento, '
        'package pickup, ATM, copying, and bill payment, 24/7. '
        'A ¥350 breakfast (pan + coffee) is the standard '
        'pre-commute price point.'
    ),
    'n5.read.006': (
        'Japan\'s climate varies sharply by latitude — Hokkaido and '
        'the Sea-of-Japan side get heavy snow (豪雪, gōsetsu), while '
        'Tokyo sees light snow only a few times a winter. The '
        '「雪が ふる」 in this passage suggests the speaker lives in '
        'a snow-prone region or expects an unusual Tokyo flurry.'
    ),
    'n5.read.008': (
        'Japanese commutes are dominated by trains: a typical '
        'urban worker walks ~10 min to the station, takes the train '
        '20-30 min, walks again at the destination. Cars are rare '
        'for daily commutes in Tokyo / Osaka due to expensive '
        'parking and dense rail coverage. The 30-minute total in '
        'the passage is on the short side of normal.'
    ),
    'n5.read.009': (
        'Public 公園 (parks) in Japan are heavily used at dawn for '
        'jogging and ラジオ体操 (radio calisthenics — a national '
        'morning fitness ritual broadcast since 1928). Saturday '
        'soccer with friends is a common adult amateur pattern, '
        'often arranged via casual community 草サッカー (kusa-sakkā, '
        '"grass-roots soccer") groups.'
    ),
    'n5.read.010': (
        'Japanese classrooms are typically arranged in 5-row × 5-column '
        'grids (≈25-40 students per class). The teacher\'s desk at '
        'the front + students facing forward is universal — group-work '
        'rearrangements happen but the default layout is rows. The '
        '25-desk count in the passage is a small class by Japanese '
        'urban-school standards (40 is more common).'
    ),
    'n5.read.012': (
        '本屋 (honya, bookstores) remain culturally important in Japan '
        'despite e-commerce — major chains like Kinokuniya and Maruzen '
        'serve as community spaces. Books in Japan are typically priced '
        '¥600-1,500 (the ¥1,500 in the passage is a mid-range '
        'reference book or N5 study material). 立ち読み (tachiyomi, '
        'standing-and-reading) is socially tolerated as long as the '
        'shrink-wrap stays on.'
    ),
    'n5.read.018': (
        'Foreign learners studying Japanese in Japan typically attend '
        'a 日本語学校 (Nihongo gakkō, language school) for 1-2 years '
        'before transitioning to university. A "1-year-of-study, '
        'plans-to-go-to-Japan-next-year" arc is the canonical N5 '
        'self-introduction story. Kanji difficulty + hiragana ease '
        'mirrors the JLPT level progression itself.'
    ),
    'n5.read.023': (
        'Japanese bus services typically run different schedules on '
        'weekdays / Saturdays / Sundays-and-holidays — the three-tier '
        'split in this passage is universal. Service density is high '
        'on weekdays (every 1-2 hours in semi-rural areas) and thin '
        'on Sundays. Major holidays (お正月, お盆, GW) often suspend '
        'service entirely.'
    ),
    'n5.read.042': (
        'Public 公園 (parks) double as informal art and music spaces — '
        'people sketching, playing instruments, or practicing voice '
        'are common, especially at larger parks like 上野公園 (Ueno) '
        'or 代々木公園 (Yoyogi). The combination of indoor music + '
        'outdoor sketching in this passage maps to a typical '
        '日曜日 (Sunday) leisure rhythm.'
    ),
}


def main() -> int:
    doc = json.loads(READING.read_text(encoding='utf-8'))
    passages = doc['passages']
    n_added = 0
    n_skipped = 0
    for p in passages:
        if p.get('cultural_context'):
            n_skipped += 1
            continue
        pid = p.get('id')
        if pid in CULTURAL_RESIDUAL:
            p['cultural_context'] = CULTURAL_RESIDUAL[pid]
            n_added += 1
    READING.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    have = sum(1 for p in passages if p.get('cultural_context'))
    print(f'Added {n_added} cultural_context callouts.')
    print(f'Skipped (already-set): {n_skipped}')
    print(f'Coverage: {have}/{len(passages)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
