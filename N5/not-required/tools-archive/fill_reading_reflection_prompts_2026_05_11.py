"""Author `reflection_prompts` on the first 20 reading passages.

Audit context: reflection_prompts = 0/54 — post-passage critical-
thinking questions are entirely absent. This pass authors 2-3
reflection questions per passage for the first 20 passages
(by id order), as a starter pass.

Schema:
  reflection_prompts: [
    {
      prompt_en: "<question in English>",
      prompt_ja: "<optional, simpler Japanese version>",
      type: "comprehension" | "application" | "inference" | "personal",
    },
    ...
  ]

Type taxonomy:
  comprehension: directly checks what the passage said
  application:   how would you use this content
  inference:     read-between-the-lines deduction
  personal:      relate to learner's own experience

Provenance: llm_curated.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROMPTS = {
    'n5.read.001': [
        {'prompt_en': 'What does Anna study in Tokyo?', 'type': 'comprehension'},
        {'prompt_en': 'Where is Anna from, and how does the passage tell us that?', 'type': 'comprehension'},
        {'prompt_en': 'What is Anna\'s hobby, and how might she practice it?', 'type': 'inference'},
    ],
    'n5.read.002': [
        {'prompt_en': 'List the speaker\'s daily activities in order from morning to night.', 'type': 'comprehension'},
        {'prompt_en': 'Which activity is the most time-consuming based on the passage?', 'type': 'inference'},
        {'prompt_en': 'How does your own daily routine compare to the one described?', 'type': 'personal'},
    ],
    'n5.read.003': [
        {'prompt_en': 'How many people are in the family described?', 'type': 'comprehension'},
        {'prompt_en': 'What does each family member do?', 'type': 'comprehension'},
        {'prompt_en': 'Why might the speaker mention occupations specifically?', 'type': 'inference'},
    ],
    'n5.read.004': [
        {'prompt_en': 'What did the person buy, and how much was the total?', 'type': 'comprehension'},
        {'prompt_en': 'Where did the shopping take place?', 'type': 'comprehension'},
        {'prompt_en': 'Was the shopping considered a good value? How can you tell?', 'type': 'inference'},
    ],
    'n5.read.005': [
        {'prompt_en': 'What sport does the writer play, and when?', 'type': 'comprehension'},
        {'prompt_en': 'Why might they have chosen that particular day of the week?', 'type': 'inference'},
        {'prompt_en': 'Do you have a similar weekly habit? Describe it briefly.', 'type': 'personal'},
    ],
    'n5.read.006': [
        {'prompt_en': 'What is the weather like in the passage?', 'type': 'comprehension'},
        {'prompt_en': 'How does the weather affect the speaker\'s plans?', 'type': 'inference'},
    ],
    'n5.read.007': [
        {'prompt_en': 'What hours is the library open on weekends?', 'type': 'comprehension'},
        {'prompt_en': 'How long can books be borrowed for?', 'type': 'comprehension'},
        {'prompt_en': 'If you needed to return a book on Sunday, when could you do it?', 'type': 'application'},
    ],
    'n5.read.008': [
        {'prompt_en': 'What mode of transport is described, and how long does the trip take?', 'type': 'comprehension'},
        {'prompt_en': 'When does the speaker arrive?', 'type': 'comprehension'},
    ],
    'n5.read.009': [
        {'prompt_en': 'What food does the speaker like, and what doesn\'t they like?', 'type': 'comprehension'},
        {'prompt_en': 'Where does the speaker usually eat?', 'type': 'inference'},
        {'prompt_en': 'What is your favorite food, and how often do you eat it?', 'type': 'personal'},
    ],
    'n5.read.010': [
        {'prompt_en': 'Who does the speaker live with?', 'type': 'comprehension'},
        {'prompt_en': 'What does each member do for work or study?', 'type': 'comprehension'},
    ],
    'n5.read.011': [
        {'prompt_en': 'What is the speaker eating, and at what time?', 'type': 'comprehension'},
        {'prompt_en': 'Is this a typical meal time in Japan?', 'type': 'application'},
    ],
    'n5.read.012': [
        {'prompt_en': 'What items did the shopper buy, and at what prices?', 'type': 'comprehension'},
        {'prompt_en': 'What is the total bill?', 'type': 'application'},
    ],
    'n5.read.013': [
        {'prompt_en': 'Where is the speaker traveling to, and how?', 'type': 'comprehension'},
        {'prompt_en': 'What time of year is implied by the travel context?', 'type': 'inference'},
    ],
    'n5.read.014': [
        {'prompt_en': 'What was the shopping outcome (success / failure / partial)?', 'type': 'inference'},
        {'prompt_en': 'Where did the trip take place?', 'type': 'comprehension'},
    ],
    'n5.read.015': [
        {'prompt_en': 'What is the weather forecast for tomorrow?', 'type': 'comprehension'},
        {'prompt_en': 'What activity is the speaker planning, and how does weather affect it?', 'type': 'application'},
    ],
    'n5.read.016': [
        {'prompt_en': 'What health issue is described?', 'type': 'comprehension'},
        {'prompt_en': 'What advice is given or implied?', 'type': 'inference'},
        {'prompt_en': 'When was the last time you experienced a similar symptom?', 'type': 'personal'},
    ],
    'n5.read.017': [
        {'prompt_en': 'How much does a coffee-and-cake set cost?', 'type': 'comprehension'},
        {'prompt_en': 'Is the set deal cheaper than buying the items separately?', 'type': 'application'},
        {'prompt_en': 'Which item would you order, and why?', 'type': 'personal'},
    ],
    'n5.read.018': [
        {'prompt_en': 'What is the speaker\'s daily morning routine?', 'type': 'comprehension'},
        {'prompt_en': 'How might this routine differ on weekends?', 'type': 'inference'},
    ],
    'n5.read.019': [
        {'prompt_en': 'What is the appointment time, and where?', 'type': 'comprehension'},
        {'prompt_en': 'Why might the speaker be sharing this information?', 'type': 'inference'},
    ],
    'n5.read.020': [
        {'prompt_en': 'What is the speaker\'s morning schedule?', 'type': 'comprehension'},
        {'prompt_en': 'What does the speaker do on weekends?', 'type': 'comprehension'},
        {'prompt_en': 'Compare this schedule to your own typical day.', 'type': 'personal'},
    ],
}


def main() -> int:
    fp = ROOT / 'data' / 'reading.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_reflection_prompts_starter')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['passages']}

    n = 0
    for pid, prompts in PROMPTS.items():
        p = by_id.get(pid)
        if not p:
            print(f'  ! missing passage: {pid}')
            continue
        if p.get('reflection_prompts'):
            print(f'  - skip (already filled): {pid}')
            continue
        p['reflection_prompts'] = prompts
        p['reflection_prompts_provenance'] = 'llm_curated'
        n += 1

    print(f'\nAuthored reflection_prompts on {n} passages.')
    print(f'Coverage: 0/54 -> {n}/54 ({100 * n // 54}%)')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
