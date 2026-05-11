"""Second wave of grammar contrast fills.

The first wave (fill_grammar_contrasts_2026_05_11.py) authored 8
high-confidence textbook contrast pairs. This second wave adds 5
more pairs that were missing because the partner already had
contrasts pointing elsewhere — adding the back-reference is now
the missing direction.

Pairs (note direction):
  n5-073 -> n5-072  (Verb-ていません <-> Verb-ています progressive)
  n5-129 -> n5-134  (どうして〜から Q-A reason <-> ので softer because)
  n5-170 <-> n5-171 (V-た + ほうが いい should <-> V-ない + ほうが いい
                     shouldn't — bidirectional)
  n5-021 -> n5-010  (から〜まで range <-> まで until)
  n5-129 -> n5-009  (どうして〜から <-> から (causal))

Schema: same as wave 1. Provenance: llm_curated.
Notes follow the same disambiguation-cue pattern as wave 1.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# (id_a, id_b, note_for_a_about_b, note_for_b_about_a or None for unidirectional)
PAIRS = [
    ('n5-073', 'n5-072',
     'Negative pair: n5-072 (Verb-ています) is the affirmative continuous / state. n5-073 (Verb-ていません) is the negative — "currently NOT in state, NOT doing." Same form, opposite polarity.',
     None),  # n5-072 already contrasts with n5-073 explicitly

    ('n5-129', 'n5-134',
     'Both are reason patterns. n5-129 is the explicit Q-and-A frame (どうして〜か → 〜から). n5-134 (〜ので) is the softer / more polite "because" — preferred when the speaker wants to sound less direct.',
     None),  # n5-134 already contrasts with から-related patterns

    ('n5-170', 'n5-171',
     'Affirmative recommendation. n5-170 (Verb-た + ほうが いい) is "you should do X" using the た-form. n5-171 is the negative counterpart (Verb-ない + ほうが いい) — "you shouldn\'t do X". Mind the た vs ない form distinction.',
     'Negative recommendation. n5-171 (Verb-ない + ほうが いい) is "you shouldn\'t do X" using the ない-form. n5-170 is the affirmative counterpart (Verb-た + ほうが いい) — "you should do X". The form distinguishes polarity.'),

    ('n5-021', 'n5-010',
     'Paired range. n5-021 is the "から ～ まで" both-endpoints range marker (9:00 から 5:00 まで). n5-010 is the bare まで, marking just the endpoint ("until X") without the explicit start.',
     None),  # n5-010 already contrasts with n5-009 (から)

    ('n5-129', 'n5-009',
     'Both involve から as causal. n5-009 is the bare から marker on a clause ("because-X"). n5-129 is the explicit Q-and-A frame (どうしてですか / 〜から) — a discourse template, not just a particle.',
     None),  # n5-009 already contrasts with n5-010
]


def main() -> int:
    fp = ROOT / 'data' / 'grammar.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_contrasts_wave2')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['patterns']}

    added = 0
    for a, b, note_a, note_b in PAIRS:
        if a not in by_id or b not in by_id:
            print(f'  ! missing pattern: a={a in by_id} b={b in by_id}')
            continue
        pa = by_id[a]
        a_list = pa.get('contrasts') or []
        if not any(c.get('with_pattern_id') == b for c in a_list):
            a_list.append({'with_pattern_id': b, 'note': note_a})
            pa['contrasts'] = a_list
            added += 1
            print(f'  + {a} -> {b}')

        if note_b:
            pb = by_id[b]
            b_list = pb.get('contrasts') or []
            if not any(c.get('with_pattern_id') == a for c in b_list):
                b_list.append({'with_pattern_id': a, 'note': note_b})
                pb['contrasts'] = b_list
                added += 1
                print(f'  + {b} -> {a}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nAdded {added} contrast cross-link entries.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
