"""Wave 3 — finish reflection_prompts (passages 41-54).

After this, coverage 40/54 -> 54/54 (100%).
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROMPTS = {
    'n5.read.041': [
        {'prompt_en': 'What kind of restaurant is described?', 'type': 'comprehension'},
        {'prompt_en': 'What menu items does the writer mention?', 'type': 'comprehension'},
        {'prompt_en': 'Would you order the same items, and why?', 'type': 'personal'},
    ],
    'n5.read.042': [
        {'prompt_en': 'Where is the writer planning to go this weekend?', 'type': 'comprehension'},
        {'prompt_en': 'Who is the writer going with?', 'type': 'comprehension'},
        {'prompt_en': 'What might they do once they arrive?', 'type': 'inference'},
    ],
    'n5.read.043': [
        {'prompt_en': 'What symptoms does the writer have?', 'type': 'comprehension'},
        {'prompt_en': 'How long have the symptoms lasted?', 'type': 'comprehension'},
        {'prompt_en': 'What action does the writer plan to take?', 'type': 'application'},
    ],
    'n5.read.044': [
        {'prompt_en': 'What event is on the calendar?', 'type': 'comprehension'},
        {'prompt_en': 'What date and time is it scheduled for?', 'type': 'comprehension'},
        {'prompt_en': 'If you had to RSVP, what would you say?', 'type': 'application'},
    ],
    'n5.read.045': [
        {'prompt_en': 'What hobby or daily ritual is the writer describing?', 'type': 'comprehension'},
        {'prompt_en': 'How important is this ritual to the writer?', 'type': 'inference'},
    ],
    'n5.read.046': [
        {'prompt_en': 'Where is America in relation to Japan, geographically?', 'type': 'comprehension'},
        {'prompt_en': 'Why does the writer want to climb Mt. Fuji next year?', 'type': 'inference'},
        {'prompt_en': 'Is there a similarly iconic landmark in your country?', 'type': 'personal'},
    ],
    'n5.read.047': [
        {'prompt_en': 'How do you reach the cheap shop from the station exit?', 'type': 'application'},
        {'prompt_en': 'How is the shop owner described?', 'type': 'comprehension'},
        {'prompt_en': 'Why might the writer prefer the smaller shop over the bigger one?', 'type': 'inference'},
    ],
    'n5.read.048': [
        {'prompt_en': 'What is Tanaka asking Yamada to do?', 'type': 'comprehension'},
        {'prompt_en': 'How does the writer convey friendliness in the letter?', 'type': 'inference'},
        {'prompt_en': 'How would you politely respond to this letter in Japanese?', 'type': 'application'},
    ],
    'n5.read.049': [
        {'prompt_en': 'What did the writer do during the morning rain?', 'type': 'comprehension'},
        {'prompt_en': 'What changes after lunch?', 'type': 'comprehension'},
        {'prompt_en': 'How does this passage reflect Japanese springtime culture?', 'type': 'inference'},
    ],
    'n5.read.050': [
        {'prompt_en': 'How many men and women work at this company?', 'type': 'comprehension'},
        {'prompt_en': 'What contrasts are drawn between Nakayama and Ogawa?', 'type': 'comprehension'},
        {'prompt_en': 'What atmosphere does the workplace seem to have?', 'type': 'inference'},
    ],
    'n5.read.051': [
        {'prompt_en': 'How many apples did the writer buy and at what price?', 'type': 'comprehension'},
        {'prompt_en': 'Was the total under or over 1,000 yen?', 'type': 'application'},
        {'prompt_en': 'What does the writer\'s reaction tell us about their shopping mood?', 'type': 'inference'},
    ],
    'n5.read.052': [
        {'prompt_en': 'What subjects do the two students study together?', 'type': 'comprehension'},
        {'prompt_en': 'When and where does each class meet?', 'type': 'comprehension'},
        {'prompt_en': 'Do you have a study buddy or partner? Describe how you study together.', 'type': 'personal'},
    ],
    'n5.read.053': [
        {'prompt_en': 'What body parts ache from running?', 'type': 'comprehension'},
        {'prompt_en': 'What is the writer\'s plan for tomorrow?', 'type': 'comprehension'},
        {'prompt_en': 'When was the last time you over-exercised? What did you do to recover?', 'type': 'personal'},
    ],
    'n5.read.054': [
        {'prompt_en': 'Where is the writer traveling, and how long is the trip?', 'type': 'comprehension'},
        {'prompt_en': 'What is the approximate cost?', 'type': 'comprehension'},
        {'prompt_en': 'What do you think the writer is looking forward to most?', 'type': 'inference'},
    ],
}


def main() -> int:
    fp = ROOT / 'data' / 'reading.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_reflection_wave3')
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
    print(f'\nWave 3 added reflection_prompts on {n} more passages.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
