"""Author per-paragraph summaries on the 7 multi-paragraph reading
passages.

Audit context: paragraph_summary = 0/54. The audit metric assumes
every passage has multiple body paragraphs needing inline gist
anchors. The N5 corpus reality: 47/54 passages are single-paragraph
(the existing passage.summary serves as the paragraph summary).
Only 7 passages have multiple paragraphs:

  n5.read.007 - library notice (5 paragraphs)
  n5.read.017 - cafe menu (6 paragraphs)
  n5.read.021 - airplane schedule (7 paragraphs)
  n5.read.023 - bus-stop notice (5 paragraphs)
  n5.read.027 - friend memo (3 paragraphs)
  n5.read.034 - friend letter (3 paragraphs)
  n5.read.039 - bookstore sale notice (7 paragraphs)

For each, author a short English gloss on each paragraph,
attached as paragraph.summary_en (preserving the existing
paragraph schema). Provenance recorded at the passage level.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SUMMARIES = {
    'n5.read.007': [
        'Heading: Library hours',
        'Weekday hours (Mon–Fri): 9:00–21:00',
        'Saturday hours: 10:00–18:00',
        'Sunday: closed',
        'Lending rule: books can be borrowed for up to 2 weeks',
    ],
    'n5.read.017': [
        'Heading: Menu',
        'Coffee: 300 yen',
        'Tea (green): 250 yen',
        'Cake: 500 yen',
        'Sandwich: 600 yen',
        'Set deal (coffee + cake): 700 yen',
    ],
    'n5.read.021': [
        'Flight info: Tokyo to Osaka',
        'Morning departures: 6, 7, 8 AM',
        'Midday departures: 12 noon, 1 PM',
        'Evening departures: 6, 7, 8 PM',
        'Flight duration: 1 hour',
        'Adult fare: 25,000 yen',
        'Child fare: 12,500 yen',
    ],
    'n5.read.023': [
        'Heading: Bus schedule',
        'Weekday service (Mon–Fri): hourly, 8:00–18:00 even hours',
        'Saturday service: 9:00 / 12:00 / 15:00',
        'Sunday: no service',
        'Fares: 300 yen adult / 150 yen child',
    ],
    'n5.read.027': [
        'Salutation: To Yamada',
        'Plan: meet at the station 1 PM tomorrow, have tea at a cafe, then shop at the department store',
        'Sign-off: From Suzuki',
    ],
    'n5.read.034': [
        'Salutation: To Yamada-san',
        'Body: invitation to a school party tomorrow, 3–5 PM, with the teacher attending',
        'Sign-off: Tanaka',
    ],
    'n5.read.039': [
        'Heading: Bookstore notice',
        'Tagline: BIG SALE!',
        'Sale dates: 1–7 August',
        'Sale hours: 10 AM – 8 PM daily',
        'Discount: 50% off all books',
        'Inventory: Japanese books AND English books',
        'Call to action: come visit!',
    ],
}


def main() -> int:
    fp = ROOT / 'data' / 'reading.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_paragraph_summaries')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['passages']}

    n = 0
    for pid, summaries in SUMMARIES.items():
        p = by_id.get(pid)
        if not p:
            print(f'  ! missing passage: {pid}')
            continue
        paragraphs = p.get('paragraphs') or []
        if len(paragraphs) != len(summaries):
            print(f'  ! {pid}: paragraph count mismatch ({len(paragraphs)} actual vs {len(summaries)} drafted)')
            continue
        for i, para in enumerate(paragraphs):
            para['summary_en'] = summaries[i]
        p['paragraph_summary_provenance'] = 'llm_curated'
        n += 1
        print(f'  + {pid}: {len(summaries)} per-paragraph summaries')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nAuthored paragraph-level summaries on {n} passages.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
