"""Fill `register` tag on the 38 N5 vocab expressions still missing
it.

Audit context: the 2026-05-09 richness audit flagged register-tag
coverage at 2% on vocab. Most missing entries are concrete nouns
where register doesn't add much information. The cleanest tractable
slice is `pos == "expression"`: 43 set-phrase/greeting/filler items
where register IS meaningful (polite vs neutral vs casual matters
for "I'm sorry" / "thanks" choice). 5 are already filled; this
script does the remaining 38.

Tagging rules (heuristic):
  - Contains 'ございます' or 'ございました'        -> polite (formal)
  - Ends with 'ます' / 'ました' / 'です' / 'でした' -> polite
  - Contains 'なさい' (gentle command)           -> polite
  - Casual-marker pronouns (うん, ええ, ううん)     -> casual
  - Filler/hesitation (えーと, あの, さあ)         -> neutral
  - All other set greetings/responses            -> neutral

Manual override (for cases the heuristic gets wrong):
  ありがとう       -> casual (cf. ありがとうございます polite)
  どうも           -> casual (cf. どうもありがとうございます polite)
  はい / いいえ    -> neutral (formal-register independent)
  またあした / じゃあ -> casual
  いただきます / ごちそうさまでした -> neutral (set table phrases — register-independent)
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Manual override map (specific cases the heuristic mis-classifies)
OVERRIDES = {
    'ありがとう': 'casual',
    'どうも': 'casual',
    'はい': 'neutral',
    'いいえ': 'neutral',
    'ええ': 'casual',
    'うん': 'casual',
    'ううん': 'casual',
    'じゃあ': 'casual',
    'えーと': 'neutral',
    'あの': 'neutral',
    'さあ': 'neutral',
    'いただきます': 'neutral',  # set table phrase — register-independent
    'ごちそうさまでした': 'neutral',  # set table phrase
    'いってきます': 'neutral',  # set departure phrase
    'いってらっしゃい': 'neutral',  # set departure phrase
    'ただいま': 'neutral',  # set return phrase
    'おかえりなさい': 'neutral',  # set return phrase
    'こんにちは': 'neutral',  # standard greeting
    'こんばんは': 'neutral',
    'もしもし': 'neutral',  # telephone-specific, register-independent
    'さようなら': 'neutral',
    'どうぞ': 'neutral',
    'どうぞよろしく': 'neutral',
    'なるほど': 'neutral',
    'いいえ': 'neutral',
    'それでは': 'polite',
    'おじゃまします': 'polite',
    'いかが': 'polite',  # explicitly polite form of どう
}


def classify(form: str) -> str:
    if form in OVERRIDES:
        return OVERRIDES[form]
    if 'ございます' in form or 'ございました' in form:
        return 'polite'
    if form.endswith('ます') or form.endswith('ました') or form.endswith('です') or form.endswith('でした'):
        return 'polite'
    if 'なさい' in form:
        return 'polite'
    return 'neutral'


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_register_expressions')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    n = 0
    by_register = {'polite': [], 'neutral': [], 'casual': []}
    for e in data['entries']:
        if e.get('pos') != 'expression':
            continue
        if e.get('register'):
            continue
        form = e.get('form') or ''
        reg = classify(form)
        e['register'] = reg
        e['register_provenance'] = 'auto_derived'
        by_register[reg].append(form)
        n += 1

    for r, items in by_register.items():
        print(f'  {r} ({len(items)}): {items[:6]}{"..." if len(items)>6 else ""}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nTagged {n} expression-pos entries with register.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
