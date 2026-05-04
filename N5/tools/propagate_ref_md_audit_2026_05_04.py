"""Propagate the 2026-05-04 reference-markdowns audit fixes from the
catalog markdowns into the runtime data files (and any other places
that mirror the catalog).

What this script does:

  1. data/kanji.json — sync 後 kun ordering with kanji_n5.md.
     入 was already in sync. No JSON-level scope-flag mirror needed
     (the [N4+] notes are MD-only annotations).

  2. data/n5_kanji_readings.json — sync 後 kun ordering same.

  3. data/grammar.json — n5-131 (もらう):
     pattern field "～に～をもらいます" → "～に / から ～をもらいます"
     meaning_en clarified to mention both particles
     form_rules note about source-marker alternation
     (The from-source example already exists; only labeling lags.)

  4. data/grammar.json — add new pattern n5-188:
     Verb (plain dictionary) + ことができる (productive can-do form)
     With 3 examples, common_mistakes, full schema mirroring n5-103.

  5. data/questions.json — add q-0579 covering n5-188 (DEFER-1
     100% coverage maintained: 178 patterns / 178 with questions).
     Also add q-0580 for variety (negative form). Refresh _meta.

Idempotent. JA-12 / JA-13 / JA-17 / JA-21 / JA-26 invariants run via
check_content_integrity.py after.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

changes: list[str] = []


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding='utf-8'))


def save(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                 encoding='utf-8')


# =====================================================================
# 1 + 2. 後 kun ordering in kanji.json + n5_kanji_readings.json
# =====================================================================
def sync_ato_kun() -> None:
    OLD_KUN = ['のち', 'うし', 'あと']
    NEW_KUN = ['うし', 'あと', 'のち']  # mirrors kanji_n5.md update

    # kanji.json
    p = ROOT / 'data' / 'kanji.json'
    k = load(p)
    entries = k['entries'] if isinstance(k, dict) else k
    ato = next((e for e in entries if e.get('glyph') == '後'), None)
    if ato and ato.get('kun') == OLD_KUN:
        ato['kun'] = NEW_KUN
        save(p, k)
        changes.append('kanji.json 後: kun reordered うし/あと/のち')

    # n5_kanji_readings.json
    p2 = ROOT / 'data' / 'n5_kanji_readings.json'
    r = load(p2)
    if isinstance(r.get('後'), dict) and r['後'].get('kun') == OLD_KUN:
        r['後']['kun'] = NEW_KUN
        save(p2, r)
        changes.append('n5_kanji_readings.json 後: kun reordered うし/あと/のち')


# =====================================================================
# 3. n5-131 もらう — update pattern label + meaning_en
# =====================================================================
def update_morau() -> None:
    p = ROOT / 'data' / 'grammar.json'
    g = load(p)
    patterns = g['patterns']
    n131 = next((x for x in patterns if x['id'] == 'n5-131'), None)
    if n131 is None:
        return
    NEW_PATTERN = '～に / から ～をもらいます'
    NEW_MEANING = '～に / から ～を もらいます - receive (from) (に for personal givers, から for institutional sources)'
    if n131.get('pattern') != NEW_PATTERN:
        n131['pattern'] = NEW_PATTERN
        changes.append('grammar.json n5-131: pattern label updated to include から')
    if n131.get('meaning_en') != NEW_MEANING:
        n131['meaning_en'] = NEW_MEANING
        changes.append('grammar.json n5-131: meaning_en clarified')
    # Add a notes line about particle-choice if not already present.
    notes = n131.get('notes') or ''
    note_addition = (
        'Both ～に and ～から are valid at N5: ～に is more typical for '
        'personal givers (友だちに, 母に); ～から for institutional / '
        'non-personal sources (学校から, ぎんこうから).'
    )
    if 'Both ～に and ～から' not in notes:
        n131['notes'] = (notes + ' ' + note_addition).strip() if notes else note_addition
        changes.append('grammar.json n5-131: notes appended (particle-choice)')
    save(p, g)


# =====================================================================
# 4. Add new pattern n5-188 to grammar.json
# =====================================================================
def add_kotogadekiru_pattern() -> None:
    p = ROOT / 'data' / 'grammar.json'
    g = load(p)
    patterns = g['patterns']
    if any(x['id'] == 'n5-188' for x in patterns):
        return  # idempotent
    new_pattern = {
        'id': 'n5-188',
        'tier': 'core_n5',
        'pattern': 'Verb-dictionary + ことができます',
        'category': 'Comparison and Preference',
        'categoryOrder': 11,
        'patternOrder': 10,
        'meaning_en': ('Verb (plain dictionary) + ことができます - '
                       'can do (productive can-do form)'),
        'meaning_ja': '「〜することが できる」',
        'form_rules': {
            'attaches_to': ['verb'],
            'conjugations': [
                {
                    'form': 'verb-dict + こと + が できる',
                    'label': 'Productive can-do',
                    'example': '日本語を 話す ことが できます',
                },
                {
                    'form': 'verb-dict + こと + が できません',
                    'label': 'Negative',
                    'example': 'あした 行く ことが できません',
                },
            ],
        },
        'explanation_en': (
            "Nominalize a plain-form verb with こと, then use the "
            "noun-can-do frame ～ができる. The productive 'can do X' "
            "construction; pairs with noun-only ～ができる (n5-103). "
            "In casual speech the こと is sometimes dropped (Verb-"
            "potential form), but at N5 the こと-form is the standard "
            "introduction (Genki I L13, Minna no Nihongo L18)."
        ),
        'examples': [
            {
                'ja': '日本語を 話す ことが できます。',
                'form': 'affirmative',
                'translation_en': 'I can speak Japanese.',
                'vocab_ids': [
                    'n5.vocab.25-languages-and-countri.日本語',
                    'n5.vocab.27-verbs-group-1-verbs.話す',
                    'n5.vocab.35-particles-functional-.を',
                    'n5.vocab.35-particles-functional-.が',
                ],
            },
            {
                'ja': 'ピアノを ひく ことが できますか。',
                'form': 'question',
                'translation_en': 'Can you play piano?',
                'vocab_ids': [
                    'n5.vocab.26-house-and-furniture.ピアノ',
                    'n5.vocab.27-verbs-group-1-verbs.ひく',
                    'n5.vocab.35-particles-functional-.を',
                    'n5.vocab.35-particles-functional-.が',
                    'n5.vocab.35-particles-functional-.か',
                ],
            },
            {
                'ja': 'あした 行く ことが できません。',
                'form': 'negative',
                'translation_en': "I can't go tomorrow.",
                'vocab_ids': [
                    'n5.vocab.10-time-general.あした',
                    'n5.vocab.27-verbs-group-1-verbs.行く',
                    'n5.vocab.35-particles-functional-.が',
                ],
            },
        ],
        'common_mistakes': [
            {
                'wrong': '日本語が 話す ことが できます。',
                'right': '日本語を 話す ことが できます。',
                'why': ('Within the こと-clause, 話す takes its normal '
                        'object marker を; only the outer こと takes が. '
                        'The が is on こと, not on the verb\'s object.'),
            },
            {
                'wrong': '日本語を 話せます。',
                'right': '日本語を 話す ことが できます。',
                'why': ('At N5 the こと-form is taught; the bare '
                        'potential form 話せる is N4. They mean the '
                        'same thing but stick to the こと-form for the '
                        'N5 exam.'),
            },
        ],
        'contrasts': [],
        'notes': (
            'Pairs with n5-103 (noun + ～ができます): use n5-103 when the '
            'thing-you-can-do is a noun (skill / language / activity); '
            'use this pattern when it\'s a verb (action). Many '
            'textbooks introduce both in the same lesson.'
        ),
    }
    patterns.append(new_pattern)
    save(p, g)
    changes.append('grammar.json: added pattern n5-188 (Verb + ことができる)')


# =====================================================================
# 5. Add questions for n5-188 + refresh _meta
# =====================================================================
def add_questions_for_n188() -> None:
    p = ROOT / 'data' / 'questions.json'
    q = load(p)
    qs = q.get('questions', [])
    existing_ids = {x.get('id') for x in qs}
    if 'q-0579' in existing_ids and 'q-0580' in existing_ids:
        # Already added; just refresh meta.
        refresh_meta(q)
        save(p, q)
        return
    Q1 = {
        'id': 'q-0579',
        'grammarPatternId': 'n5-188',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': '（  ）に 入る ことばを えらんで ください。',
        'question_ja': '日本語を 話す こと（  ）できます。',
        'choices': ['が', 'を', 'に', 'で'],
        'correctAnswer': 'が',
        'explanation_en': ('「ことができる」 takes が on the こと '
                           'nominalizer. Within the こと-clause the '
                           'verb 話す retains its normal object 日本語'
                           'を; only the outer こと takes が.'),
        'distractor_explanations': {
            'を': ('を marks 日本語 (the object of 話す) but not こと; '
                   'こと is the subject of できる, which takes が.'),
            'に': ('に marks recipient/destination, not the subject of '
                   'a できる-frame.'),
            'で': ('で marks means/location; here the structure '
                   'specifies a verb noun-clause that is "doable", '
                   'which takes が.'),
        },
        'high_confusion': False,
        'difficulty': 2,
    }
    Q2 = {
        'id': 'q-0580',
        'grammarPatternId': 'n5-188',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': '（  ）に 入る ことばを えらんで ください。',
        'question_ja': 'あした 友だちに あう ことが （  ）。',
        'choices': ['できません', 'ありません', 'いません', 'しません'],
        'correctAnswer': 'できません',
        'explanation_en': ('Verb-dict + ことが できません = "cannot do". '
                           'The full negative form of the productive '
                           'can-do construction.'),
        'distractor_explanations': {
            'ありません': ('ありません negates existence (ない). '
                           'Pairing it with 「ことが」 yields '
                           '「ことが ありません」 = "have not done", '
                           'a different N5 grammar (experience). '
                           'Here we want capability negation.'),
            'いません': ('いません is the negative existence for '
                         'animate subjects. Doesn\'t fit the こと '
                         'frame.'),
            'しません': ('しません = "do not do" (volition / habit), '
                         'not "cannot do". Loses the ability sense.'),
        },
        'high_confusion': False,
        'difficulty': 2,
    }
    qs.extend([Q1, Q2])
    q['questions'] = qs
    refresh_meta(q)
    save(p, q)
    changes.append('questions.json: added q-0579 + q-0580 for n5-188')


def refresh_meta(q: dict) -> None:
    qs = q.get('questions', [])
    type_dist: dict[str, int] = {}
    for x in qs:
        t = x.get('type', 'mcq')
        type_dist[t] = type_dist.get(t, 0) + 1
    ids = sorted(x.get('id', '') for x in qs)
    meta = q.get('_meta') or {}
    new_count = len(qs)
    new_range = {'first': ids[0] if ids else '?',
                 'last': ids[-1] if ids else '?'}
    history = meta.get('audit_history') or meta.get('history') or []
    note = ('Reference-markdowns audit propagation (2026-05-04): '
            'added q-0579 / q-0580 covering new pattern n5-188 '
            '(Verb + ことができる, productive can-do form). Bank: '
            f'{new_count - 2} → {new_count} (mcq +2). Pattern coverage '
            'remains 100% (178/178).')
    if not any('Reference-markdowns audit propagation' in (h or '') for h in history):
        if isinstance(history, list):
            history.append(note)
            if 'audit_history' in meta:
                meta['audit_history'] = history
            else:
                meta['history'] = history
            changes.append('questions.json _meta: appended audit_history note')
    if meta.get('question_count') != new_count:
        meta['question_count'] = new_count
        changes.append(f'questions.json _meta.question_count: {new_count}')
    if meta.get('type_distribution') != type_dist:
        meta['type_distribution'] = type_dist
        changes.append(f'questions.json _meta.type_distribution: {type_dist}')
    if meta.get('id_range') != new_range:
        meta['id_range'] = new_range
        changes.append(f'questions.json _meta.id_range: {new_range["first"]}..{new_range["last"]}')
    q['_meta'] = meta


def main() -> int:
    sync_ato_kun()
    update_morau()
    add_kotogadekiru_pattern()
    add_questions_for_n188()

    if not changes:
        print('No changes (already propagated).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
