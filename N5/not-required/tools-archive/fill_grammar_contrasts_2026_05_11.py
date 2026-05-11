"""Fill bidirectional `contrasts` cross-links on grammar.json for
8 high-confidence textbook contrasts.

Audit context: the 2026-05-09 richness audit flagged 81/178 grammar
patterns without `contrasts`. Most of those 81 are standalone
patterns with no natural N5-corpus contrast partner. This pass
fills the 8 that have unambiguous textbook contrasts where both
endpoints exist in the corpus.

Contrast pairs (all bidirectional, both endpoints in data):
  n5-023 (か question final)   <-> n5-024 (か choice "A か B")
  n5-027 (よね combined)        <-> n5-025 (ね tag-confirmation)
  n5-027 (よね combined)        <-> n5-026 (よ assertion)
  n5-049 (どれ/どの/どちら which) <-> n5-050 (どう / いかが how)
  n5-049 (どれ/どの/どちら which) <-> n5-042 (こちら polite directions)
  n5-060 (polite past -ました)   <-> n5-067 (plain past た-form)
  n5-061 (polite past neg -ませんでした) <-> n5-068 (plain past neg -なかった)
  n5-076 (Verb-てから 'after')   <-> n5-120 (〜あと 'after, separately')

Schema (matches existing entries):
  contrasts: [{with_pattern_id, note}]

If a destination pattern already has a `contrasts` array, the new
entry APPENDS (does not replace). If the new entry would duplicate
an existing with_pattern_id, it is skipped.

Provenance for new entries: `llm_curated`. Existing entries on the
target patterns keep whatever provenance they had — the appended
list is heterogeneous if mixing native + LLM authors. The
schema doesn't carry per-entry provenance today.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Each item is (id_a, id_b, note_for_a_about_b, note_for_b_about_a).
PAIRS = [
    ('n5-023', 'n5-024',
     'Same particle か, different function: n5-023 is the sentence-final question marker (行きますか). n5-024 is the listing/choice marker between alternatives (コーヒーか おちゃ).',
     'Same particle か, different function: n5-024 lists alternatives ("A or B"). n5-023 ends a question sentence. Listening cue: position — final か = question; medial か = choice.'),

    ('n5-027', 'n5-025',
     'n5-025 is ね alone (mild confirmation, "right?"). n5-027 is the よね combination — adds the よ-assertion punch ("I think so, and you agree, right?").',
     'よね is the combined form: よ (assertion) + ね (seeking agreement). n5-025 is the bare ね alone — softer, just inviting confirmation.'),

    ('n5-027', 'n5-026',
     'n5-026 is よ alone (assertion / new info to listener). n5-027 is the よね combination — keeps よ\'s assertive force but seeks agreement instead of just informing.',
     'よね is the combined form: よ (assertion) + ね (seeking agreement). n5-026 is the bare よ alone — purely informing, not soliciting agreement.'),

    ('n5-049', 'n5-050',
     'Both are question words. n5-049 (どれ / どの / どちら) asks which item from a known set. n5-050 (どう / いかが) asks about state, opinion, or makes a polite offer ("how about ~?").',
     'Both are question words. n5-050 (どう / いかが) asks state / opinion. n5-049 (どれ / どの / どちら) asks which item to pick from a list. Often confused: "which one is good?" = どれが いいですか (n5-049), "how is it?" = どうですか (n5-050).'),

    ('n5-049', 'n5-042',
     'n5-042 (こちら / そちら / あちら / どちら) is the polite こそあど directions series. どちら appears in BOTH: n5-042 uses it as "which direction / which one (polite)", n5-049 uses どちら as the polite どれ in 2-way choice questions.',
     'n5-049 (どれ / どの / どちら) covers the which-selection question words across the こそあど grid. n5-042 is the polite parallel series (こちら / そちら / あちら / どちら) — どちら is shared between them as the polite version of どれ.'),

    ('n5-060', 'n5-067',
     'Both express past affirmative. n5-060 is the polite -ました form (友だちに 会いました). n5-067 is the plain た-form (友だちに 会った). Same meaning, different register.',
     'Both express past affirmative. n5-067 is the plain た-form (友だちに 会った, casual). n5-060 is the polite -ました form (友だちに 会いました). Choose by register, not meaning.'),

    ('n5-061', 'n5-068',
     'Both express past negative. n5-061 is the polite -ませんでした (行きませんでした). n5-068 is the plain -なかった (行かなかった). Same meaning, different register.',
     'Both express past negative. n5-068 is the plain -なかった (行かなかった, casual). n5-061 is the polite -ませんでした (行きませんでした). Casual writing / friends use plain; polite speech uses -ませんでした.'),

    ('n5-076', 'n5-120',
     'Both mean "after". n5-076 (Verb-てから) links two clauses in tight temporal sequence ("after eating, watch TV") — the second clause requires the first. n5-120 (〜あと) marks a more independent "after" — often noun-form あとで, less tight coupling.',
     'Both mean "after". n5-120 (〜あと / あとで) is the noun-style "after". n5-076 (Verb-てから) tightly chains two actions where the second depends on the first ("after eating, then watch TV"). Use てから for cause-effect; あと for sequencing.'),
]


def main() -> int:
    fp = ROOT / 'data' / 'grammar.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_contrasts_fill')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['patterns']}

    added = 0
    for a, b, note_a, note_b in PAIRS:
        if a not in by_id or b not in by_id:
            print(f'  ! missing pattern: a={a}({a in by_id}) b={b}({b in by_id})')
            continue
        pa = by_id[a]
        pb = by_id[b]

        # Append to a's contrasts (preserve existing)
        a_list = pa.get('contrasts') or []
        if not any(c.get('with_pattern_id') == b for c in a_list):
            a_list.append({'with_pattern_id': b, 'note': note_a})
            pa['contrasts'] = a_list
            added += 1
            print(f'  + {a} -> {b}')

        # Append to b's contrasts (preserve existing)
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
