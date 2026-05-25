#!/usr/bin/env python3
"""
Fix ambiguous MCQ questions where 2+ choices are grammatically valid
completions for an N5 learner.

User-flagged example (q-0221):
  あした コーヒーを のみ（　）。  choices=[ません, ます, ました, ましょう]
  - のみます  = "will drink"           ✓ valid
  - のみましょう = "let's drink"        ✓ also valid
  - のみません = "won't drink"          also valid
  - のみました = past — wrong with あした

An N5 learner can't reliably pick between ます/ましょう/ません without
disambiguating context. Native-teacher fix: either add disambiguating
context to the stem OR replace the ambiguous wrong choices with
clearly-grammatically-wrong distractors.

Native-teacher pass (5 in questions.json + 2 in mock papers):

  q-0220 まいにち よみ (habit, +): replace ません/たい distractors so only ます fits.
  q-0221 あした のみ (future, +): replace ましょう/ません with ますか/ませんでした (clear tense conflicts).
  q-0222 わたしは にくを たべ (- intent): add negative-cue context to stem.
  q-0223 あした 学校へ いき (- intent): add "明日はやすみ" context to stem.
  q-0229 ちょっと やすみ (volitional): add fatigue-cue + 一緒に to stem.
  bunpou-2.12 毎日 友だちに あい (habit, +): add positive-emotion sentence.
  bunpou-3.9 つかれました すこし やすみ (たい): expand to ...たいです slot.
"""
import argparse
import json
from pathlib import Path

QUESTIONS = Path('data/questions.json')
INDEX = Path('data/index.json')
FIX_LOG = Path('data/grammar.fix_log.json')

PROV = "auto_fix_2026_05_25"
AUDIT_WAVE = "claude_audit_2026_05_25"
REVIEW_STATUS = "ai_native_reviewer_2026_05_25"

# Per-question rewrites
QUESTION_FIXES = {
    'q-0220': {
        'question_ja': 'わたしは まいにち ほんを よみ（　）。',
        'choices': ['ます', 'ました', 'ませんでした', 'ながら'],
        'correctAnswer': 'ます',
        'explanation_en': 'Habitual present positive: まいにち (every day) + ほんを よみます (I read books). ました/ませんでした are past tense and conflict with the まいにち habitual frame. ながら needs another verb to follow (V-stem + ながら = "while V-ing") so it cannot end the sentence.',
        'note': 'Replaced ません (polarity-ambiguous) and たい (register-ambiguous) with clear-wrong distractors.',
    },
    'q-0221': {
        'question_ja': 'あした コーヒーを のみ（　）。',
        'choices': ['ます', 'ました', 'ますか', 'ませんでした'],
        'correctAnswer': 'ます',
        'explanation_en': 'Future declarative: あした (tomorrow) + のみます (will drink). ました/ませんでした are past tense and conflict with あした. ますか is a question form that requires the sentence to end with か。 (the stem ends with 。 only, so ますか creates a punctuation mismatch).',
        'note': 'Replaced ましょう (volitional, also-valid) and ません (polarity-ambiguous) with clear-wrong distractors.',
    },
    'q-0222': {
        'question_ja': 'わたしは ベジタリアンです。にくを たべ（　）。',
        'choices': ['ません', 'ます', 'ました', 'ましょう'],
        'correctAnswer': 'ません',
        'explanation_en': 'Negative declarative locked by the preceding sentence "わたしは ベジタリアンです" (I am vegetarian). The ベジタリアン context makes "I don\'t eat meat" the only natural completion. たべます (contradicts vegetarianism), たべました (past doesn\'t match "I am vegetarian" present-tense framing), たべましょう ("let\'s eat meat" contradicts the stated identity).',
        'note': 'Added "わたしは ベジタリアンです。" context to lock negative polarity (was: stem was contextless).',
    },
    'q-0223': {
        'question_ja': 'あしたは やすみです。がっこうへ いき（　）。',
        'choices': ['ません', 'ます', 'ました', 'ましょうか'],
        'correctAnswer': 'ません',
        'explanation_en': 'Negative future locked by the preceding sentence "あしたは やすみです" (tomorrow is a day off). With "tomorrow is a holiday", "won\'t go to school" is the only natural completion. いきます (contradicts day-off), いきました (past + あした conflict), いきましょうか ("shall we go to school" contradicts day-off).',
        'note': 'Added "あしたは やすみです。" context to lock negative polarity.',
    },
    'q-0229': {
        'question_ja': '（一緒に つかれましたね。）ちょっと やすみ（　）。',
        'choices': ['ましょう', 'ます', 'ました', 'ません'],
        'correctAnswer': 'ましょう',
        'explanation_en': 'Volitional/invitation locked by the preceding "(一緒に つかれましたね)" — "(we\'re tired together, aren\'t we)". With this fatigue + inclusive frame, "let\'s rest a bit" (やすみましょう) is the only natural completion. やすみます (declarative; doesn\'t respond to the invitation cue), やすみました (past conflict), やすみません (contradicts the fatigue cue).',
        'note': 'Added "(一緒に つかれましたね。)" inclusive-fatigue context to lock volitional.',
    },
}

# Paper fixes (different file path)
PAPER_FIXES = {
    'bunpou-2.12': {
        'paper': 'bunpou/paper-2.json',
        'stem_html': '毎日 学校で ともだちに あい（　　）。とても たのしいです。',
        'choices': ['ます', 'ません', 'ました', 'ませんでした'],
        'correctIndex': 0,
        'rationale': 'Habitual present positive: 毎日 (every day) + あいます (I meet). The follow-up "とても たのしいです" (very fun) locks positive polarity — you wouldn\'t describe NOT meeting friends as "very fun". ました/ませんでした are past tense and conflict with 毎日.',
        'note': 'Added "とても たのしいです。" to lock positive polarity (was: contextless).',
    },
    'bunpou-3.9': {
        'paper': 'bunpou/paper-3.json',
        'stem_html': 'つかれましたから、すこし やすみ（　　）です。',
        'choices': ['ます', 'たい', 'ました', 'ません'],
        'correctIndex': 1,
        'rationale': 'Desiderative + polite copula: V-stem + たい + です = "want to V" in polite form. The trailing です in the stem locks the slot to a い-form word (V-stem+たい). ますです / ましたです / ませんです are not grammatical (です doesn\'t attach to these).',
        'note': 'Added trailing です to lock the slot to V-stem+たい (was: open slot ambiguous between ます/たい).',
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    # Questions.json fixes
    q = json.loads(QUESTIONS.read_text(encoding='utf-8'))
    q_changes = []
    for it in q['questions']:
        if it['id'] in QUESTION_FIXES:
            fix = QUESTION_FIXES[it['id']]
            before = {
                'question_ja': it.get('question_ja'),
                'choices': list(it.get('choices') or []),
                'correctAnswer': it.get('correctAnswer'),
            }
            it['question_ja'] = fix['question_ja']
            it['choices'] = list(fix['choices'])
            it['correctAnswer'] = fix['correctAnswer']
            it['explanation_en'] = fix['explanation_en']
            it['provenance'] = PROV
            it['audit_wave'] = AUDIT_WAVE
            it['review_status'] = REVIEW_STATUS
            it['reviewer_note'] = fix['note']
            # Sanity: correctAnswer must be in choices
            assert it['correctAnswer'] in it['choices'], f"{it['id']}: correctAnswer not in choices"
            q_changes.append({'id': it['id'], 'before': before, 'after': fix})
            print(f"  {it['id']}: {fix['question_ja'][:50]}")
            print(f"    choices: {fix['choices']}, correct: {fix['correctAnswer']}")

    # Papers fixes
    paper_changes = []
    for qid, fix in PAPER_FIXES.items():
        path = Path('data/papers') / fix['paper']
        d = json.loads(path.read_text(encoding='utf-8'))
        for q_ in d.get('questions') or []:
            if q_.get('id') == qid:
                before = {
                    'stem_html': q_.get('stem_html'),
                    'choices': list(q_.get('choices') or []),
                    'correctIndex': q_.get('correctIndex'),
                }
                q_['stem_html'] = fix['stem_html']
                q_['choices'] = list(fix['choices'])
                q_['correctIndex'] = fix['correctIndex']
                q_['rationale'] = fix['rationale']
                # Sanity
                assert 0 <= q_['correctIndex'] < len(q_['choices']), f"{qid}: bad correctIndex"
                paper_changes.append({'id': qid, 'paper': fix['paper'], 'before': before, 'after': {k:v for k,v in fix.items() if k != 'paper'}})
                print(f"  {qid} ({fix['paper']}): {fix['stem_html'][:50]}")
                print(f"    choices: {fix['choices']}, correct: {fix['choices'][fix['correctIndex']]}")
        if args.apply:
            path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f"\nquestions.json fixes: {len(q_changes)}")
    print(f"paper fixes: {len(paper_changes)}")

    if args.apply:
        QUESTIONS.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        # Resync index
        idx = json.loads(INDEX.read_text(encoding='utf-8'))
        def lf(p): return len(Path(p).read_bytes().replace(b'\r\n', b'\n'))
        for entry in idx.get('files', []):
            if entry.get('path') == 'data/questions.json':
                entry['size_bytes'] = lf(QUESTIONS)
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        # Fix log
        log = json.loads(FIX_LOG.read_text(encoding='utf-8'))
        log['ambiguous_mcq_fix_2026_05_25'] = {
            'description': (
                '7 MCQ questions surfaced where 2+ choices are grammatically valid '
                'for an N5 learner without context disambiguation. Native-teacher pass '
                'added disambiguating context to stems OR replaced ambiguous distractors '
                'with clearly-grammatically-wrong ones (e.g., ますか where stem ends with '
                '。 not か。; V-stem + ながら without a following verb).'
            ),
            'questions_json_fixes': q_changes,
            'paper_fixes': paper_changes,
        }
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'\napplied.')
    else:
        print('\n--dry-run')


if __name__ == '__main__':
    main()
