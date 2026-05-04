"""Comprehensive multi-correct-answer audit across the question bank.

Triggered by Pass-15 retrospective + 2026-05-02 user finding that some
paper questions still ship multi-correct (e.g., コーヒー（ ）飲みます with
both など and だけ valid). The Pass-15 scanner only handled a narrow
particle-pair set; this audit extends to:

  A. Interchangeable particle pairs (Pass-15 baseline).
  B. Scope / restriction particles attaching to noun-before-verb:
     {など, だけ, しか, ばかり, も} — multiple of these can be valid
     simultaneously when the stem doesn't disambiguate.
  C. List-conjunction particles between nouns: {と, や, とか, など}.
  D. Frequency adverbs: {いつも, よく, たまに, あまり, ぜんぜん}.
  E. Demonstrative quartets without scene context (Pass-15 baseline).
  F. Manner-vs-degree confusables: (とても, よく, あまり) overlap in
     some affirmative contexts.

For each MCQ, the scanner reports a finding if 2+ choices fall into the
same "interchangeable category" AND the question_ja stem doesn't carry a
disambiguator (scene parenthetical, anchor phrase, or context sentence).

Output: stdout report grouped by source-file + category. Findings include
question id, stem, choices, marked-correct, and which other choices are
mutually valid.

Usage:
  python tools/audit_multi_correct.py
  python tools/audit_multi_correct.py --json > findings.json
"""
import json
import io
import sys
import re
import argparse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------
# Multi-correct pattern catalog
# --------------------------------------------------------------------

KOSOADO_QUARTETS = [
    {'これ', 'それ', 'あれ', 'どれ'},
    {'この', 'その', 'あの', 'どの'},
    {'ここ', 'そこ', 'あそこ', 'どこ'},
    {'こちら', 'そちら', 'あちら', 'どちら'},
    {'こう', 'そう', 'ああ', 'どう'},
]

# (a, b): both valid in many contexts; flag if both present in choices.
INTERCHANGEABLE_PAIRS = [
    ('に', 'へ'),         # motion destination
    ('から', 'ので'),     # reason connector
    ('に', 'と'),         # recipient / companion (with でんわをする, あう, etc.)
    ('まで', 'から'),     # time-range endpoints (when the stem doesn't fix one)
    ('も', 'は'),         # topic vs additive (Pass-15 q-0026 / 0422 family)
    ('や', 'と'),         # non-exhaustive vs exhaustive list
    ('だけ', 'しか'),     # only (scope; しか requires negative verb but learners
                          #   often have positive-context confusion)
]

# Restriction / scope particles that attach to a noun before a verb.
# In a stem "<noun>（ ）<verb-ます>" with no other disambiguator, multiple
# of these can read as legitimate completions.
SCOPE_RESTRICTION_PARTICLES = {'など', 'だけ', 'しか', 'ばかり', 'も', 'は'}

# Frequency adverbs (calibration grey-zone candidates).
# Note: とても is intentionally excluded — it's a degree adverb (very), not
# frequency. Including it caused E-category false positives in Pass-23 r2.
FREQ_ADVERBS = {'いつも', 'よく', 'たまに', 'あまり', 'ぜんぜん',
                'たいてい', 'ときどき'}

# Subset of FREQ_ADVERBS where the boundaries are subjective: a learner
# could defensibly pick either depending on personal threshold.
# Pass-23 r4 (2026-05-02) — added after q-0488 (月に 1かい → たまに OR よく
# both defensible) demonstrated that calibration questions need their own
# stricter audit even when only 2 of these are in the choice set.
FREQ_GREYZONE_PAIRS = [
    {'よく', 'たまに'},      # "often" vs "occasionally" — fuzzy mid-low band
    {'よく', 'ときどき'},    # "often" vs "sometimes" — fuzzy mid band
    {'たまに', 'ときどき'},  # "occasionally" vs "sometimes" — near synonyms
    {'いつも', 'たいてい'},  # "always" vs "usually" — near synonyms
]

# Sentence-final speech-act particles. With a bare statement stem
# "<S> です（ ）" three of {か, ね, よ} all produce grammatical Japanese
# with different speech acts (question / confirmation / assertion). The
# question is single-correct only when the stem fixes the speech act
# (e.g. via a follow-up "はい/いいえ" answer or an explicit question word).
SPEECH_ACT_PARTICLES = {'か', 'ね', 'よ'}

# Spatial-position vocabulary cluster. With a stem "<noun>の（ ）に <noun>が
# あります" all four positions are syntactically valid; only context can
# pin one. Flag when 2+ are in choices and the stem has no directional
# verb / map / movement-cue anchor.
SPATIAL_POSITIONS = {'うえ', 'した', 'まえ', 'うしろ',
                     'なか', 'そと', 'みぎ', 'ひだり',
                     'となり', 'よこ', 'ちかく',
                     '上', '下', '前', '後ろ', '中', '外',
                     '右', '左', '隣', '横', '近く'}

# --------------------------------------------------------------------
# Heuristics: scene context detection
# --------------------------------------------------------------------

def has_scene_context(stem: str) -> bool:
    """True if the stem contains a scene-setting parenthetical preceding
    the blank, OR contains an explicit anchor phrase that disambiguates,
    OR carries an explicit destination/recipient/source that pins one
    role of an interchangeable particle pair.

    Refined 2026-05-02 (Pass-23 round 2) to reduce false-positive rate:
    the previous version flagged questions where one of the OTHER choices
    was a clearly-distinguishing distractor. The audit shouldn't trip on
    those — they're not actually multi-correct."""
    if not stem:
        return False
    # Pattern: (scene)　stem-with-blank — full-width parens before blank
    if re.search(r'^[（(][^）)]+[）)][\s　]', stem):
        return True
    # Pattern: prior-sentence ending in 。 followed by stem
    if '。' in stem and stem.index('。') < stem.find('（'):
        if re.search(r'。[\s　]*[^（]*（', stem):
            return True
    # Anchor-phrase heuristic: stem mentions a frequency / time / numeric
    # anchor that pins one answer
    anchors = ['毎日', '毎週', '毎年', '毎朝', 'いつも', '一日', '月に',
               '年に', '週に', '一回', '1回', '1かい', '一度', 'しか',
               'ぜんぜん', 'あまり', '前', 'まえ', 'あとで', 'すこし',
               # Destination/recipient/source anchors — if a separate
               # destination is given (e.g., へ, に at another position
               # in the stem), the blank can't ALSO be a destination
               # particle, so に/へ are not multi-correct.
               'こうえんへ', 'がっこうへ', 'いえへ', 'えきへ', 'みせへ',
               'にちようびに', 'げつようびに', 'かようびに',
               # Verb-specific disambiguators — these verbs only pair
               # with one of an interchangeable pair, not both.
               'はじまります', 'はじまる', 'おわります', 'おわる',
               'かけました', 'かけます', 'いいました', 'いう',
               # Quote-marker anchor (forces と uniquely)
               'いいました', 'と いいました',
               # Bracket-quoted strings (force と as quote-marker)
               '「', '」',
               # Existence verbs: only に for location-of-existence
               # (excludes へ as direction, excludes と as "and")
               'います', 'あります', 'いません', 'ありません',
               'いる', 'ある', 'いない', 'ない です',
               # Recipient/source verbs: only に, not へ/と
               'もらいました', 'もらう', 'もらって',
               'あげました', 'あげる', 'あげて',
               'くれました', 'くれる', 'くれて',
               'おしえました', 'ならいました',
               # Comparison anchor: どちら / どっち forces と uniquely
               'どちら', 'どっち', 'くらべ', '比べ',
               # Companion anchor: と "with X" structure (verb of joint
               # activity with two-person stem)
               'いっしょに', '一緒に',
               # Purpose anchor: かいもの / べんきょう + に + 行く/来る
               'かいもの', '勉強', 'べんきょう', 'しょくじ', '食事',
               # Time anchor: numeric時 / 分 → に, never へ
               '時', '分', '半', 'ごろ',
               # Range complement: if まで appears the other endpoint is から
               'まで',
               ]
    if any(a in stem for a in anchors):
        return True
    # Question-word + ( ) + negative-verb pattern: tests the n5-013
    # "question word + も + negative" pattern. は can't attach to question
    # words (だれは, なには are ungrammatical), so even though は and も
    # are both scope-restriction particles, the question is single-correct.
    qword_pattern = re.search(
        r'(だれ|なに|なん|どこ|いつ|どう|どれ|どの|いくら|いくつ)[\s　]*[（(]',
        stem,
    )
    if qword_pattern:
        # Confirm a negative verb form follows the blank
        if re.search(r'(ません|ない|なかった)', stem):
            return True
    # Joint-activity-verb pattern: "<person>（ ）<obj>を <verb>" where
    # the verb is one that doesn't take a に-recipient (見る, 食べる, 飲む,
    # あそぶ). The person-noun + blank takes と (companion), not に — so
    # に/と aren't actually interchangeable here.
    joint_verbs = ['見ました', '見ます', '見る',
                   '食べました', '食べます', '食べる',
                   '飲みました', '飲みます', '飲む',
                   'あそびました', 'あそびます', 'あそぶ',
                   'べんきょうしました', 'べんきょうします',
                   '勉強しました', '勉強します']
    if re.search(r'を[\s　]*\S*(' + '|'.join(map(re.escape, joint_verbs)) + r')', stem):
        # Confirm there's a person noun (proper noun, さん-suffix, kinship)
        # before the blank.
        if re.search(r'(ともだち|友だち|友達|さん|せんせい|先生|'
                     r'おかあさん|おとうさん|あに|あね|いもうと|おとうと|'
                     r'かれ|かのじょ|ひと|人|きょうだい|兄弟)[\s　]*[（(]', stem):
            return True
    return False


# --------------------------------------------------------------------
# Per-question check
# --------------------------------------------------------------------

def check_question(q: dict) -> list[dict]:
    """Return list of finding dicts for this question. Empty if clean."""
    if q.get('type') != 'mcq':
        # paper format uses correctIndex; runtime format uses correctAnswer
        if q.get('type') is not None and q.get('type') != 'mcq':
            return []
    choices = q.get('choices', [])
    if not isinstance(choices, list) or len(choices) < 2:
        return []
    choice_set = set(choices)
    correct = q.get('correctAnswer')
    # paper format: correctIndex (0-based) + choices
    if correct is None and 'correctIndex' in q and isinstance(q['correctIndex'], int):
        ci = q['correctIndex']
        if 0 <= ci < len(choices):
            correct = choices[ci]
    if correct is None:
        return []

    stem = q.get('question_ja') or q.get('stem_html') or ''
    # Strip <u>...</u> and other simple HTML for analysis
    stem_clean = re.sub(r'<[^>]+>', '', stem)
    has_scene = has_scene_context(stem_clean)

    findings = []

    # A. Demonstrative quartets without scene context
    for quartet in KOSOADO_QUARTETS:
        if quartet <= choice_set and not has_scene:
            findings.append({
                'category': 'A_kosoado_no_context',
                'severity': 'CRITICAL',
                'reason': f'ko-so-a-do quartet {sorted(quartet)} in choices without scene context',
                'multi_correct_with': sorted(quartet - {correct}),
            })
            break

    # B. Interchangeable particle pairs both present + correct is one of them
    for a, b in INTERCHANGEABLE_PAIRS:
        if a in choice_set and b in choice_set and correct in (a, b) and not has_scene:
            other = b if correct == a else a
            findings.append({
                'category': 'B_interchangeable_pair',
                'severity': 'HIGH',
                'reason': f'interchangeable pair ({a}, {b}) both in choices, correct={correct}',
                'multi_correct_with': [other],
            })
            break  # only flag once per question

    # C. Scope/restriction particles cluster
    scope_in_choices = choice_set & SCOPE_RESTRICTION_PARTICLES
    if len(scope_in_choices) >= 2 and correct in scope_in_choices:
        # Stem pattern: noun（ ）verb-ます with no anchor
        if not has_scene:
            findings.append({
                'category': 'C_scope_restriction',
                'severity': 'HIGH',
                'reason': f'multiple scope-restriction particles in choices: {sorted(scope_in_choices)}',
                'multi_correct_with': sorted(scope_in_choices - {correct}),
            })

    # D. List-conjunction cluster (between nouns)
    list_particles = {'と', 'や', 'とか', 'など'} & choice_set
    if len(list_particles) >= 2 and correct in list_particles and not has_scene:
        # Stem must look like "<noun>（ ）<noun>" pattern to actually be a list
        # context. Heuristic: the blank is between two katakana/kanji words.
        if re.search(r'[ぁ-んァ-ヶ一-鿿]+[（(]\s*[）)][ぁ-んァ-ヶ一-鿿]+', stem_clean):
            findings.append({
                'category': 'D_list_conjunction',
                'severity': 'MEDIUM',
                'reason': f'multiple list-conjunction particles {sorted(list_particles)} between nouns',
                'multi_correct_with': sorted(list_particles - {correct}),
            })

    # E. Frequency adverbs cluster (most stems have ONE that fits cleanly,
    # but if 3+ frequency adverbs are in choices and there's no anchor,
    # the question is borderline)
    freq_in_choices = choice_set & FREQ_ADVERBS
    if len(freq_in_choices) >= 3 and correct in freq_in_choices and not has_scene:
        findings.append({
            'category': 'E_frequency_adverbs',
            'severity': 'LOW',
            'reason': f'three+ frequency adverbs without disambiguator: {sorted(freq_in_choices)}',
            'multi_correct_with': sorted(freq_in_choices - {correct}),
        })

    # F. Frequency calibration grey-zone — stricter than E. A numeric
    # frequency in the stem (月に Xかい / 週に Xかい / etc.) maps to a
    # range of frequency adverbs that depend on speaker subjectivity.
    # Pass-23 r4: q-0488 (月に 1かい → たまに OR よく) demonstrated that
    # specific 2-element pairs of FREQ_GREYZONE_PAIRS are multi-correct
    # even with only 2 choices in the set. The numeric anchor is the
    # disambiguator for *particle* questions but the grey-zone trigger
    # for adverb questions, so this rule fires regardless of has_scene.
    has_numeric_frequency = bool(re.search(
        r'(月|週|年|毎日|毎週|毎月|毎年)に[\s　]*[1-9一二三四五六七八九十]', stem_clean))
    if has_numeric_frequency:
        for pair in FREQ_GREYZONE_PAIRS:
            if pair <= choice_set and correct in pair:
                other = (pair - {correct}).pop()
                findings.append({
                    'category': 'F_frequency_calibration',
                    'severity': 'HIGH',
                    'reason': f'numeric frequency in stem + adverb pair {sorted(pair)} '
                              f'is calibration-grey-zone (subjective threshold)',
                    'multi_correct_with': [other],
                })
                break

    # G. Sentence-final speech-act particles. Stem ends in "<S>です（ ）"
    # or "<S>ます（ ）" without any context that fixes the speech act
    # (no follow-up answer pinning question/confirmation/assertion, no
    # explicit question word). か / ね / よ all produce grammatical
    # Japanese with different speech acts.
    sap_in_choices = choice_set & SPEECH_ACT_PARTICLES
    sentence_final_blank = bool(re.search(
        r'(です|ます|でした|ました|ません|ませんでした)[\s　]*[（(]\s*[）)][。\s　]*$', stem_clean))
    if sentence_final_blank and len(sap_in_choices) >= 2 and correct in sap_in_choices:
        # Disambiguators that fix the speech act:
        #   - explicit question word in stem (どこ / だれ / いつ / なに / etc.)
        #   - follow-up "はい / いいえ" turn pinning か
        #   - explicit context cue (asking / telling / confirming)
        has_qword = bool(re.search(r'(だれ|どこ|いつ|なに|なん|どう|どれ|どの|いくら|いくつ)', stem_clean))
        has_yesno_followup = 'はい' in stem_clean or 'いいえ' in stem_clean
        if not (has_qword or has_yesno_followup):
            findings.append({
                'category': 'G_speech_act_particle',
                'severity': 'HIGH',
                'reason': f'sentence-final particle pair {sorted(sap_in_choices)} '
                          f'with no speech-act anchor (no question word, no はい/いいえ follow-up)',
                'multi_correct_with': sorted(sap_in_choices - {correct}),
            })

    # H. Spatial-position vocabulary without directional anchor. Stem
    # "<X>の（ ）に <Y>が あります" is multi-correct when 2+ positions are
    # in the choices and the stem doesn't pin a direction (no map, no
    # movement verb, no canonical "X on Y" object pair like book/desk).
    pos_in_choices = choice_set & SPATIAL_POSITIONS
    spatial_blank = bool(re.search(r'の[\s　]*[（(]\s*[）)][\s　]*に', stem_clean))
    if spatial_blank and len(pos_in_choices) >= 2 and correct in pos_in_choices:
        # Anchors that pin a single position:
        #   - canonical object/place pair where one position is overwhelming
        #     (本+つくえ → うえ, ねこ+いえ → なか, etc.)
        #   - movement verb that fixes direction (出る → そと, 入る → なか)
        #   - explicit map / coordinate hint
        canonical_anchors = ['つくえ', '机', 'テーブル', 'ベッド',
                             'いす', '椅子', 'はこ', '箱',
                             '出', '入', 'すわ', '座']
        if not any(a in stem_clean for a in canonical_anchors):
            findings.append({
                'category': 'H_spatial_no_anchor',
                'severity': 'HIGH',
                'reason': f'multiple spatial positions {sorted(pos_in_choices)} '
                          f'with no directional anchor in stem',
                'multi_correct_with': sorted(pos_in_choices - {correct}),
            })

    return findings


# --------------------------------------------------------------------
# Loaders
# --------------------------------------------------------------------

def load_runtime_questions():
    qd = json.load((ROOT / 'data' / 'questions.json').open(encoding='utf-8'))
    out = []
    for q in qd['questions']:
        out.append({
            **q,
            '_source': 'data/questions.json',
            '_id': q.get('id'),
        })
    return out


def load_paper_questions():
    out = []
    papers_dir = ROOT / 'data' / 'papers'
    if not papers_dir.exists():
        return out
    manifest = json.load((papers_dir / 'manifest.json').open(encoding='utf-8'))
    for cat in manifest['categories']:
        for paper_meta in cat['papers']:
            paper_path = papers_dir / cat['id'] / f"paper-{paper_meta['paperNumber']}.json"
            if not paper_path.exists():
                continue
            paper = json.load(paper_path.open(encoding='utf-8'))
            for q in paper['questions']:
                # Translate the paper format to a unified shape. For
                # passage-context questions the stem_html is just a pointer
                # ("→ blank [2]") and the disambiguating context lives in
                # passage_text — splice them so the anchor heuristics see
                # the full context.
                stem = q.get('stem_html', '')
                if q.get('passage_text'):
                    stem = q['passage_text'] + '\n' + stem
                out.append({
                    'id': q['id'],
                    'type': 'mcq',
                    'question_ja': stem,
                    'choices': q.get('choices', []),
                    'correctIndex': q.get('correctIndex'),
                    '_source': f'data/papers/{cat["id"]}/paper-{paper_meta["paperNumber"]}.json',
                    '_id': q['id'],
                })
    return out


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', action='store_true', help='Emit JSON instead of human-readable')
    args = parser.parse_args()

    runtime_qs = load_runtime_questions()
    paper_qs = load_paper_questions()
    all_qs = runtime_qs + paper_qs

    findings = []
    for q in all_qs:
        for f in check_question(q):
            f['question_id'] = q['_id']
            f['source'] = q['_source']
            f['stem'] = (q.get('question_ja') or q.get('stem_html') or '')[:120]
            f['choices'] = q.get('choices', [])
            # surface the correct answer
            if 'correctAnswer' in q:
                f['correct'] = q.get('correctAnswer')
            elif 'correctIndex' in q and q.get('choices'):
                ci = q['correctIndex']
                if 0 <= ci < len(q['choices']):
                    f['correct'] = q['choices'][ci]
            findings.append(f)

    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
        return

    # Human-readable grouped report
    by_cat = {}
    for f in findings:
        by_cat.setdefault(f['category'], []).append(f)

    print(f'Total questions audited: {len(all_qs)} ({len(runtime_qs)} runtime + {len(paper_qs)} paper)')
    print(f'Total findings: {len(findings)}')
    print()
    for cat in sorted(by_cat):
        cat_findings = by_cat[cat]
        sev = cat_findings[0]['severity']
        print(f'\n{"="*72}')
        print(f'  Category {cat} ({sev}): {len(cat_findings)} findings')
        print(f'{"="*72}')
        for f in cat_findings:
            print(f'\n  {f["question_id"]} [{f["source"]}]')
            print(f'    stem:    {f["stem"]}')
            print(f'    choices: {f["choices"]}')
            print(f'    correct: {f.get("correct", "?")}')
            print(f'    issue:   {f["reason"]}')
            print(f'    multi-correct with: {f["multi_correct_with"]}')

    # Summary by category
    print(f'\n{"="*72}')
    print('  SUMMARY')
    print(f'{"="*72}')
    for cat in sorted(by_cat):
        sev = by_cat[cat][0]['severity']
        print(f'  {cat:35} {sev:8} {len(by_cat[cat]):4} findings')


if __name__ == '__main__':
    main()
