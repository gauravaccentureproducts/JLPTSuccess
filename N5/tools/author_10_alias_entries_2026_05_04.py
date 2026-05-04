"""Author 9 multi-form vocab.json entries to close the remaining 10 alias tokens.

The 10 multi-form aliases (いい / いえ / ぐらい / けれど / ござる / じゃあ /
では / みんな / やはり / ゼロ) are present in vocabulary_n5.md as multi-
form lines (e.g., 「- いい / よい - [i-adj] good」) but absent from
vocab.json. Their canonical pair-form is also absent from vocab.json
(except くらい-i-adj-dark and れい-noun-courtesy, which are
homograph entries with different meanings).

Resolution: add 9 NEW vocab.json entries — one per multi-form line —
using the precedent established by 8 existing entries (何, 四, 七, 九,
分, etc.) where the `reading` field carries multi-form notation while
`form` stays single. The drift checker splits both `form` and `reading`
on '/' so all 10 alias tokens get matched after this commit.

Entry table:

  form (primary)  reading (multi-form)        section                pos
  いい           いい / よい                  31. い-Adjectives        i-adj
  いえ           いえ / うち                  26. House and Furniture noun
  ぐらい         ぐらい / くらい              35. Particles            particle
  けれど         けれど / けれども / けど      34. Conjunctions         conjunction
  ござる         ござる / ございます          30. Verbs - Existence    verb-1
  じゃあ         じゃあ / では / じゃ          39. Function/Filler       expression
  みんな         みんな / みな                 1. People - Pronouns    noun
  やはり         やはり / やっぱり            33. Adverbs              adverb
  ゼロ           ゼロ / れい                  7. Numbers               numeral

POS values match the multi-form MD lines' tags (verified via JA-31
abbreviation map: noun→n., i-adj→i-adj, particle→part., etc.).

Idempotent: skips entries already present.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent


SECTIONS = {
    1:  ('1-people-pronouns-and-se',     '1. People - Pronouns and Self'),
    7:  ('7-numbers',                    '7. Numbers'),
    26: ('26-house-and-furniture',       '26. House and Furniture'),
    30: ('30-verbs-existence-and-p',     '30. Verbs - Existence and Possession'),
    31: ('31-adjectives',                '31. い-Adjectives'),
    33: ('33-adverbs',                   '33. Adverbs'),
    34: ('34-conjunctions',              '34. Conjunctions'),
    35: ('35-particles-functional-',     '35. Particles (functional vocabulary)'),
    39: ('39-function-filler-expre',     '39. Function / Filler Expressions'),
}


def E(form, reading, gloss, sect, pos, ja, en):
    slug, sect_name = SECTIONS[sect]
    return {
        'id': f'n5.vocab.{slug}.{form}',
        'form': form,
        'reading': reading,
        'gloss': gloss,
        'section': sect_name,
        'pos': pos,
        'examples': [{'ja': ja, 'translation_en': en}],
    }


NEW_ENTRIES = [
    # 1: いい / よい (i-adj "good") — いい more colloquial; よい formal
    E('いい', 'いい / よい', 'good (いい more colloquial; よい more formal/literary — same meaning)',
      31, 'i-adj',
      'きょうは いい てんきです。',
      "It's nice weather today."),
    # 2: いえ / うち (noun "house, home")
    E('いえ', 'いえ / うち', 'house / home (いえ emphasizes the building; うち emphasizes "my place / my household")',
      26, 'noun',
      'いえに かえります。',
      "I'll go home."),
    # 3: ぐらい / くらい (particle "about, approximately")
    E('ぐらい', 'ぐらい / くらい', 'about, approximately (ぐらい more common after voiced sounds; くらい elsewhere — particle of estimate)',
      35, 'particle',
      '一時間 ぐらい かかります。',
      'It takes about an hour.'),
    # 4: けれど / けれども / けど (conj "but, however")
    E('けれど', 'けれど / けれども / けど', 'but / however (けど most casual; けれど middle; けれども most formal — same meaning)',
      34, 'conjunction',
      'いそがしいけれど、行きます。',
      "I'm busy but I'll go."),
    # 5: ござる / ございます (v1 "to be, very polite")
    E('ござる', 'ござる / ございます', 'to be / there is (very polite; ございます is the masu-form, used in shop/hotel speech)',
      30, 'verb-1',
      'おはよう ございます。',
      'Good morning. (formal)'),
    # 6: じゃあ / では / じゃ (exp "well then")
    E('じゃあ', 'じゃあ / では / じゃ', 'well then / so (じゃあ casual; では formal; じゃ very casual — discourse marker for transitioning)',
      39, 'expression',
      'じゃあ、また あした。',
      'Well then, see you tomorrow.'),
    # 7: みんな / みな (noun "everyone")
    E('みんな', 'みんな / みな', 'everyone / all (みんな more colloquial; みな more formal — both function as inclusive "everyone")',
      1, 'noun',
      'みんなで がんばりましょう。',
      "Let's all do our best together."),
    # 8: やはり / やっぱり (adv "as expected")
    E('やはり', 'やはり / やっぱり', 'as expected / after all (やはり more formal; やっぱり colloquial — confirms an expectation or returns to a prior view)',
      33, 'adverb',
      'やはり 日本料理が 好きです。',
      'As expected, I like Japanese food.'),
    # 9: ゼロ / れい (numeral "zero")
    E('ゼロ', 'ゼロ / れい', 'zero (ゼロ for "0" digit reading; れい for formal/numeric "zero" especially in counts)',
      7, 'numeral',
      'てんすうは ゼロでした。',
      'The score was zero.'),
]


def main() -> int:
    p = ROOT / 'data' / 'vocab.json'
    vocab = json.loads(p.read_text(encoding='utf-8'))
    entries = vocab['entries']
    existing_ids = {e['id'] for e in entries}

    added = 0
    for new in NEW_ENTRIES:
        if new['id'] in existing_ids:
            continue
        entries.append(new)
        added += 1

    if added == 0:
        print('No changes (all 9 alias entries already authored).')
        return 0

    p.write_text(json.dumps(vocab, ensure_ascii=False, indent=2),
                 encoding='utf-8')
    print(f'Added {added} new alias entries:')
    for new in NEW_ENTRIES:
        print(f'  + {new["id"]}  [{new["pos"]}]  {new["form"]} ({new["reading"]})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
