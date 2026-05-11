"""Third wave of grammar contrast fills.

Wave 1 (8 pairs / 14 entries) and Wave 2 (5 pairs / 6 entries) closed
the most obvious textbook contrasts. Wave 3 adds 10 more pairs across
adjective forms, want-expressions, list-chaining, transitional
particles, and Q-and-A counter usage. Each pair has both endpoints
in the corpus and a textbook-canonical contrast relationship.

Pairs (bidirectional unless noted; "set" = partner already has
contrasts pointing elsewhere — only the missing direction is added):

  n5-070 (te-chain) <-> n5-168 (たり sample-listing)
  n5-070 (te-chain) <-> n5-144 (ながら simultaneous)
  n5-097 (どちらが which-of-two) <-> n5-098 (likes/dislikes compare)
  n5-080 (i-adj neg present) <-> n5-082 (i-adj neg past)
  n5-080 (i-adj neg present) -> n5-079 (i-adj affirm present)  [unidir]
  n5-082 (i-adj neg past)    -> n5-081 (i-adj past affirm)     [unidir]
  n5-088 (na-adj past neg)   -> n5-087 (na-adj past affirm)    [unidir]
  n5-110 (counter+verb quantity) -> n5-109 (how-many counter Q) [unidir]
  n5-125 (では/じゃ well-then) <-> n5-126 (が clause but)
  n5-101 (が ほしい want object) -> n5-104 (V-stem たい want action) [unidir]

Schema: same as waves 1 + 2. Provenance: llm_curated on the
appended entries; the destination patterns keep prior provenance.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# (a, b, note_a_about_b, note_b_about_a or None for unidirectional)
PAIRS = [
    ('n5-070', 'n5-168',
     'Both chain actions. n5-070 (Verb-て、Verb-て…) lists actions IN ORDER ("did X, then Y, then Z"). n5-168 (〜たり〜たりする) lists actions AS SAMPLES from a larger set, in no particular order ("we did things like X and Y").',
     'Both list multiple actions. n5-168 (〜たり〜たり) presents the actions as REPRESENTATIVE SAMPLES, order-irrelevant. n5-070 (Verb-て、Verb-て) chains them in TEMPORAL SEQUENCE ("first X, then Y").'),

    ('n5-070', 'n5-144',
     'Both link two actions. n5-070 (Verb-て、Verb-て) is sequential: "did X, THEN Y". n5-144 (Verb-stem + ながら) is simultaneous: "X WHILE Y" (both happen at the same time).',
     'Both link two actions. n5-144 (Verb-stem + ながら) is simultaneous ("X while Y, both at once"). n5-070 (Verb-て chain) is sequential ("X, then Y"). Mind the form: stem+ながら vs te-form chain.'),

    ('n5-097', 'n5-098',
     'Both compare two items. n5-097 (AとBと、どちらが ～ですか) asks the comparison question. n5-098 (likes/dislikes) is the standard answer template using より.',
     'Both involve comparison between two items. n5-098 (likes/dislikes contrast) is the assertion frame; n5-097 (AとBと、どちらが) is the question frame that elicits this kind of answer.'),

    ('n5-080', 'n5-082',
     'Same negative form, different tense. n5-080 is i-adj NEGATIVE PRESENT (たかくないです / たかくありません). n5-082 is i-adj NEGATIVE PAST (たかくなかったです / たかくありませんでした). Both derive from くない + tense marker.',
     'Same negative form, different tense. n5-082 is i-adj NEGATIVE PAST. n5-080 is i-adj NEGATIVE PRESENT. Mind the suffix: なかった (past) vs ない (non-past).'),

    ('n5-080', 'n5-079',
     'Opposite polarity. n5-079 is i-adj AFFIRMATIVE PRESENT (たかいです). n5-080 is i-adj NEGATIVE PRESENT (たかくないです). The negative form drops final い and adds くない.',
     None),  # n5-079 already has contrasts pointing elsewhere

    ('n5-082', 'n5-081',
     'Opposite polarity. n5-081 is i-adj AFFIRMATIVE PAST (たかかったです). n5-082 is i-adj NEGATIVE PAST (たかくなかったです). Both share the i-adj い→かった transformation; the negative inserts く+ない before the past marker.',
     None),  # n5-081 already has contrasts

    ('n5-088', 'n5-087',
     'Opposite polarity. n5-087 is na-adj PAST AFFIRMATIVE (きれいでした). n5-088 is na-adj PAST NEGATIVE (きれいじゃありませんでした / きれいではありませんでした). Mind the でした vs じゃ/ではありませんでした.',
     None),  # n5-087 already has contrasts

    ('n5-110', 'n5-109',
     'Q-and-A counter pair. n5-109 is the question (なんまい / いくつ / 何人 etc.). n5-110 is the answer pattern: Object + counter-with-number + Verb ("I bought three books"). Same counter inventory, opposite speech acts.',
     None),  # n5-109 already has contrasts

    ('n5-125', 'n5-126',
     'Both are transitional connectives. n5-125 (では / じゃ) is a topic-shift adverb at sentence start ("Well then, …"). n5-126 (が clause-but) is an adversative clause-connector inside a sentence ("X, but Y"). Different syntactic position; different function.',
     'Both are transitional. n5-126 (が clause-but) is adversative ("X, but Y"). n5-125 (では / じゃ) is a topic-shift adverb sentence-initially ("well then…"). Position determines function.'),

    ('n5-101', 'n5-104',
     'Both express wanting. n5-101 (〜が ほしいです) wants an OBJECT (noun-marked want). n5-104 (Verb-stem + たい) wants an ACTION (verb-stem desire). Different POS: noun-marked ほしい vs verb-stem たい.',
     None),  # n5-104 already has contrasts
]


def main() -> int:
    fp = ROOT / 'data' / 'grammar.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_contrasts_wave3')
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
