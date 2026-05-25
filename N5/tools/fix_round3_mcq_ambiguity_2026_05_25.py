#!/usr/bin/env python3
"""
Round 3 MCQ ambiguity fix (user re-flagged my Round 2 fix as still
having 2 valid answers).

Reviewer pointed out that for q-0221 with new choices
[ます, ました, ますか, ませんでした] and stem ending with 。, BOTH
ます and ますか are grammatically valid:
  - のみます。 = "I'll drink." (declarative future)
  - のみますか。 = "Will you drink?" (yes/no question — 。 works for both)

My JA-167 predicate incorrectly excluded ますか from FUTURE compat,
treating 。 as declarative-only. In reality, Japanese 。 marks
sentence-end for BOTH statements and questions.

Round 3 fixes 7 ambiguities caught by the stricter predicate:
  q-0221 FUTURE      ms vs ますか both valid → swap ますか for でした
  q-0224 PAST        ました vs ませんでした polarity ambig → add semantic cue + distractor swap
  q-0226 PAST        same shape → add "おなかが いたくて" cue
  q-0227 PAST        same shape → add "やすみだったから" cue
  q-0228 INVITATION  3 valid (ましょう/ます/ません) → distractor swap to lock ましょう
  q-0229 INVITATION  same shape → distractor swap (Round-2-fixed stem stays)
  q-0230 INVITATION+Q same shape → distractor swap to lock ません(か)

Strategy: when polarity/mood is naturally ambiguous, replace ALL non-
target valid choices with:
  - past-tense forms (when target is future-tense) — clear tense conflict
  - present-tense forms (when target is past-tense) — clear tense conflict
  - でした (V-stem + でした is ungrammatical) — clear conjugation defect
  - ながら (V-stem + ながら needs a main verb) — incomplete sentence
"""
import json
from pathlib import Path

QUESTIONS = Path('data/questions.json')
INDEX = Path('data/index.json')
FIX_LOG = Path('data/grammar.fix_log.json')

FIXES = {
    'q-0221': {
        'question_ja': 'あした コーヒーを のみ（　）。',
        'choices': ['ます', 'ました', 'でした', 'ませんでした'],
        'correctAnswer': 'ます',
        'reason': 'Replaced ますか (still valid as future-question) with でした (V-stem+でした ungrammatical).',
    },
    'q-0224': {
        'question_ja': 'きのう えいがを み（　）。とても おもしろかったです。',
        'choices': ['ました', 'ます', 'でした', 'ながら'],
        'correctAnswer': 'ました',
        'reason': 'Added positive-emotion follow-up. Replaced ません/ませんでした (past-polarity ambig) with present-conflict + ungrammatical.',
    },
    'q-0226': {
        'question_ja': 'きのうは おなかが いたくて、ばんごはんを たべ（　）。',
        'choices': ['ませんでした', 'ました', 'でした', 'ながら'],
        'correctAnswer': 'ませんでした',
        'reason': 'Added "おなかが いたくて、" to lock negative polarity. ました now semantically contradicts.',
    },
    'q-0227': {
        'question_ja': 'せんしゅうは やすみだったから、しごとが あり（　）。',
        'choices': ['ませんでした', 'ました', 'でした', 'ながら'],
        'correctAnswer': 'ませんでした',
        'reason': 'Added "やすみだったから、" to lock negative polarity.',
    },
    'q-0228': {
        'question_ja': 'いっしょに ばんごはんを たべ（　）。',
        'choices': ['ましょう', 'ました', 'でした', 'ながら'],
        'correctAnswer': 'ましょう',
        'reason': 'Replaced ます/ません (also valid in invitation) with past + ungrammatical distractors.',
    },
    'q-0229': {
        'question_ja': '（いっしょに つかれましたね。）ちょっと やすみ（　）。',
        'choices': ['ましょう', 'ました', 'でした', 'ながら'],
        'correctAnswer': 'ましょう',
        'reason': 'Round-2-fixed stem retained. Choices tightened: replaced ます/ません with past + ungrammatical distractors.',
    },
    'q-0230': {
        'question_ja': 'いっしょに えいがを み（　）か。',
        'choices': ['ません', 'ました', 'でした', 'ながら'],
        'correctAnswer': 'ません',
        'reason': 'Replaced ます/ましょう (both valid as ますか/ましょうか) with past-conflict + ungrammatical. ません+か is canonical invitation form.',
    },
}

DISTRACTORS_EN = {
    'ました': 'Past tense — conflicts with the future/invitation context.',
    'ます': 'Present/future tense — conflicts with the past-tense context.',
    'ません': 'Present negative — conflicts with past-tense context (past negative is ませんでした).',
    'ませんでした': 'Past negative — would change the polarity of the statement.',
    'でした': 'V-stem + でした is ungrammatical (でした only follows nouns or na-adjectives).',
    'ながら': 'V-stem + ながら means "while V-ing" and needs a following main verb. Cannot end a sentence.',
    'ましょう': 'Volitional — doesn\'t fit the declarative context.',
    'ますか': 'Question form — would change the sentence type.',
}

DISTRACTORS_HI = {
    'ました': 'भूतकाल; भविष्य/निमंत्रण-संदर्भ से टकराता है।',
    'ます': 'वर्तमान/भविष्य; भूत-संदर्भ से टकराता है।',
    'ません': 'वर्तमान नकारात्मक; भूतकाल में ませんでした चाहिए।',
    'ませんでした': 'भूत नकारात्मक; कथन की ध्रुवता बदल देता है।',
    'でした': 'V-stem + でした व्याकरण-सम्मत नहीं (でした संज्ञा/na-विशेषण के बाद आता है)।',
    'ながら': 'V-stem + ながら = "V करते हुए"; इसके बाद दूसरा क्रिया चाहिए।',
    'ましょう': 'इच्छा-रूप; घोषणात्मक संदर्भ से मेल नहीं खाता।',
    'ますか': 'प्रश्न रूप; वाक्य प्रकार बदल देता है।',
}


def lf_size(path):
    return len(Path(path).read_bytes().replace(b'\r\n', b'\n'))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    q = json.loads(QUESTIONS.read_text(encoding='utf-8'))
    changes = []
    for it in q['questions']:
        if it['id'] in FIXES:
            f = FIXES[it['id']]
            before = {'q': it.get('question_ja'), 'ch': list(it.get('choices') or []), 'ca': it.get('correctAnswer')}
            it['question_ja'] = f['question_ja']
            it['choices'] = list(f['choices'])
            it['correctAnswer'] = f['correctAnswer']
            it['distractor_explanations'] = {c: DISTRACTORS_EN[c] for c in f['choices'] if c != f['correctAnswer']}
            it['distractor_explanations_hi'] = {c: DISTRACTORS_HI[c] for c in f['choices'] if c != f['correctAnswer']}
            it['distractor_explanations_hi_provenance'] = 'auto_fix_2026_05_25'
            it['provenance'] = 'auto_fix_2026_05_25'
            it['audit_wave'] = 'claude_audit_2026_05_25'
            it['review_status'] = 'ai_native_reviewer_2026_05_25'
            it['reviewer_note'] = f['reason']
            it['explanation_en'] = f'Only {f["correctAnswer"]} is grammatically valid here. {f["reason"]}'
            assert it['correctAnswer'] in it['choices']
            changes.append({'id': it['id'], 'before': before, 'after': {'q': f['question_ja'], 'ch': f['choices'], 'ca': f['correctAnswer']}})
            print(f"  {it['id']}: choices={f['choices']}")

    print(f'\nfixed: {len(changes)} questions')

    if args.apply:
        QUESTIONS.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        idx = json.loads(INDEX.read_text(encoding='utf-8'))
        for entry in idx.get('files', []):
            path = entry.get('path')
            if path and Path(path).exists():
                entry['size_bytes'] = lf_size(path)
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        log = json.loads(FIX_LOG.read_text(encoding='utf-8'))
        log['mcq_ambiguity_round3_2026_05_25'] = {
            'description': 'Round 3 — user re-flagged q-0221 ますか ambiguity. Stricter predicate caught 7 more ambiguities including 3 past-polarity-ambiguous + 3 invitation-multi-valid + q-0221. All fixed with past-tense / ungrammatical / incomplete-ender distractors.',
            'changes': changes,
        }
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
