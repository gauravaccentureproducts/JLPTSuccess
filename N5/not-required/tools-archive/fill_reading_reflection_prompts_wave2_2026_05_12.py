"""Wave 2 — extend reflection_prompts to passages 21-40.

Wave 1 (2026-05-11) covered the first 20 passages. This wave covers
the next 20 (passages 21-40). Same schema + 4-type taxonomy
(comprehension / application / inference / personal).
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROMPTS = {
    'n5.read.021': [
        {'prompt_en': 'What time options are available for the Tokyo–Osaka flight?', 'type': 'comprehension'},
        {'prompt_en': 'If you wanted to arrive in Osaka by 2 PM, which flight would you take?', 'type': 'application'},
        {'prompt_en': 'Why might morning flights be more popular than evening ones?', 'type': 'inference'},
    ],
    'n5.read.022': [
        {'prompt_en': 'What activity does the writer do on weekends?', 'type': 'comprehension'},
        {'prompt_en': 'Who joins the writer for this activity?', 'type': 'comprehension'},
        {'prompt_en': 'What does this say about the writer\'s social life?', 'type': 'inference'},
    ],
    'n5.read.023': [
        {'prompt_en': 'On which days does the bus not run?', 'type': 'comprehension'},
        {'prompt_en': 'What is the adult-vs-child fare difference?', 'type': 'comprehension'},
        {'prompt_en': 'If your shift ended at 7 PM on a Friday, would you catch the bus home?', 'type': 'application'},
    ],
    'n5.read.024': [
        {'prompt_en': 'What part-time job does the writer have?', 'type': 'comprehension'},
        {'prompt_en': 'How does it interact with their studies?', 'type': 'inference'},
    ],
    'n5.read.025': [
        {'prompt_en': 'Describe the writer\'s daily routine in 3 bullets.', 'type': 'comprehension'},
        {'prompt_en': 'How does this routine compare to your own?', 'type': 'personal'},
    ],
    'n5.read.026': [
        {'prompt_en': 'What did the writer buy on this shopping trip?', 'type': 'comprehension'},
        {'prompt_en': 'Was the trip described as successful or disappointing?', 'type': 'inference'},
    ],
    'n5.read.027': [
        {'prompt_en': 'What is the plan being proposed?', 'type': 'comprehension'},
        {'prompt_en': 'Who is the sender, who is the recipient?', 'type': 'comprehension'},
        {'prompt_en': 'How would you politely accept or decline this invitation in Japanese?', 'type': 'application'},
    ],
    'n5.read.028': [
        {'prompt_en': 'What hobby is described?', 'type': 'comprehension'},
        {'prompt_en': 'How often does the writer practice it?', 'type': 'comprehension'},
    ],
    'n5.read.029': [
        {'prompt_en': 'What is the weather forecast?', 'type': 'comprehension'},
        {'prompt_en': 'What clothing or item should one carry given the forecast?', 'type': 'application'},
    ],
    'n5.read.030': [
        {'prompt_en': 'How do you get from the station to the writer\'s house?', 'type': 'comprehension'},
        {'prompt_en': 'If you missed the directions, what landmarks would help you find the way?', 'type': 'inference'},
    ],
    'n5.read.031': [
        {'prompt_en': 'What pet does the writer have?', 'type': 'comprehension'},
        {'prompt_en': 'How does the writer feel about it?', 'type': 'inference'},
        {'prompt_en': 'Do you have a pet, and how would you describe its routine?', 'type': 'personal'},
    ],
    'n5.read.032': [
        {'prompt_en': 'What is the writer\'s job?', 'type': 'comprehension'},
        {'prompt_en': 'What is the work schedule?', 'type': 'comprehension'},
    ],
    'n5.read.033': [
        {'prompt_en': 'What is the weather like in the passage?', 'type': 'comprehension'},
        {'prompt_en': 'How does the weather affect the writer\'s mood or plans?', 'type': 'inference'},
    ],
    'n5.read.034': [
        {'prompt_en': 'What is being invited and when?', 'type': 'comprehension'},
        {'prompt_en': 'Who is the sender, who is the recipient?', 'type': 'comprehension'},
        {'prompt_en': 'How would you accept this invitation in polite Japanese?', 'type': 'application'},
    ],
    'n5.read.035': [
        {'prompt_en': 'What food is the writer describing or recommending?', 'type': 'comprehension'},
        {'prompt_en': 'What does the writer like about it?', 'type': 'inference'},
    ],
    'n5.read.036': [
        {'prompt_en': 'What is the writer\'s travel plan?', 'type': 'comprehension'},
        {'prompt_en': 'Why might they have chosen that destination?', 'type': 'inference'},
    ],
    'n5.read.037': [
        {'prompt_en': 'What transport mode is described?', 'type': 'comprehension'},
        {'prompt_en': 'What was the travel duration and cost?', 'type': 'comprehension'},
    ],
    'n5.read.038': [
        {'prompt_en': 'What study habit is the writer describing?', 'type': 'comprehension'},
        {'prompt_en': 'What is the writer\'s motivation for studying?', 'type': 'inference'},
        {'prompt_en': 'How does your own study approach compare?', 'type': 'personal'},
    ],
    'n5.read.039': [
        {'prompt_en': 'When is the sale, and what discount is offered?', 'type': 'comprehension'},
        {'prompt_en': 'What categories of books are on sale?', 'type': 'comprehension'},
        {'prompt_en': 'If you wanted to attend, which day/time would you go?', 'type': 'application'},
    ],
    'n5.read.040': [
        {'prompt_en': 'What flower / plant / natural feature is described?', 'type': 'comprehension'},
        {'prompt_en': 'In which season does it bloom?', 'type': 'comprehension'},
        {'prompt_en': 'Is there a similar seasonal landmark in your culture?', 'type': 'personal'},
    ],
}


def main() -> int:
    fp = ROOT / 'data' / 'reading.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_reflection_prompts_wave2')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['passages']}
    n = 0
    for pid, prompts in PROMPTS.items():
        p = by_id.get(pid)
        if not p:
            print(f'  ! missing: {pid}'); continue
        if p.get('reflection_prompts'):
            print(f'  - skip: {pid}'); continue
        p['reflection_prompts'] = prompts
        p['reflection_prompts_provenance'] = 'llm_curated'
        n += 1
    print(f'\nWave 2 added reflection_prompts on {n} more passages.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
