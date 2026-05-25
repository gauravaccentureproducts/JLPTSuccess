#!/usr/bin/env python3
"""
Horizontal MCQ ambiguity fix — across non-verb-ending classes.

After horizontal sweep beyond JA-167, found 6 additional ambiguous MCQs:

  q-0027  だれ（）きませんでした  PARTICLE  だれも (nobody) vs だれが (who-not) both valid
  q-0034  （）を たべますか        QWORD     なに vs なん vs どれ all grammatically valid
  q-0036  （）が きましたか        QWORD     だれ vs なに both valid (person vs thing subject)
  q-0051  （）から ...勉強しています QWORD  いつ/だれ/どこ/なに all valid (from-X)
  q-0433  おしごとは（）ですか     QWORD     どう/いつ/どこ all valid (different info-types)
  bunpou-1.13 おかね（）ありませんから  PARTICLE  が vs は both grammatical

Strategy:
  - QWORD ambiguities: add semantic-disambiguating context (answer-hint
    or constraining adverb) OR replace distractors with semantically-
    impossible Q-words.
  - PARTICLE ambiguities: replace ambiguous-grammatical-distractor with
    clearly-wrong particle (へ for non-direction context, etc.).

Bunpou-1.5 (きょう が/は) NOT fixed — both technically valid but は is
strongly dominant in canonical teaching; reviewer-tier polish only.
"""
import json
from pathlib import Path

QUESTIONS = Path('data/questions.json')
PAPER_113 = Path('data/papers/bunpou/paper-1.json')
INDEX = Path('data/index.json')
FIX_LOG = Path('data/grammar.fix_log.json')

QUESTION_FIXES = {
    'q-0027': {
        'question_ja': 'だれ（　）きませんでした。',
        'choices': ['も', 'を', 'に', 'へ'],
        'correctAnswer': 'も',
        'distractors_en': {
            'を': '来る is intransitive; だれを来る is ungrammatical.',
            'に': 'に would mark a direction/target; だれに 来る is unusual.',
            'へ': 'へ is direction marker; doesn\'t fit subject-of-arrival.',
        },
        'distractors_hi': {
            'を': '来る अकर्मक क्रिया है; だれを来る व्याकरण-सम्मत नहीं।',
            'に': 'に दिशा/लक्ष्य चिह्न; だれに 来る असामान्य।',
            'へ': 'へ दिशा चिह्न; आगमन के विषय के साथ नहीं।',
        },
        'reason': 'Replaced が (would yield "Who didn\'t come?" — also grammatically valid) with へ (direction particle, semantically wrong for subject-of-arrival).',
    },
    'q-0034': {
        'question_ja': '（　）を たべますか。',
        'choices': ['なに', 'どこ', 'いつ', 'だれ'],
        'correctAnswer': 'なに',
        'distractors_en': {
            'どこ': 'どこ asks for location, not for an object to eat.',
            'いつ': 'いつ asks for time, not for an object to eat.',
            'だれ': 'だれ asks for a person; semantically impossible as direct object of 食べる.',
        },
        'distractors_hi': {
            'どこ': 'どこ स्थान पूछता है; खाने की वस्तु नहीं।',
            'いつ': 'いつ समय पूछता है; खाने की वस्तु नहीं।',
            'だれ': 'だれ व्यक्ति पूछता है; 食べる का प्रत्यक्ष कर्म असंभव।',
        },
        'reason': 'Replaced なん/どれ (both grammatically valid for "what to eat") with semantically-impossible Q-words for direct object of 食べる.',
    },
    'q-0036': {
        'question_ja': '（　）が きましたか。',
        'choices': ['だれ', 'どこ', 'いつ', 'どう'],
        'correctAnswer': 'だれ',
        'distractors_en': {
            'どこ': '"Which place came" — semantically odd.',
            'いつ': 'いつ takes no particle; いつが is ungrammatical.',
            'どう': 'どう asks for manner; doesn\'t fit subject slot before が.',
        },
        'distractors_hi': {
            'どこ': '"कौन-सी जगह आई" — अर्थहीन।',
            'いつ': 'いつ के साथ कण नहीं आता; いつが व्याकरण-सम्मत नहीं।',
            'どう': 'どう "कैसे" पूछता है; が से पहले विषय-स्लॉट में नहीं आता।',
        },
        'reason': 'Replaced なに (also valid for non-person subject "what came") with semantically-impossible Q-words.',
    },
    'q-0051': {
        'question_ja': '「3ねん前です。」と こたえました。（　）から にほんごを べんきょうしていますか。',
        'choices': ['いつ', 'どう', 'なぜ', 'どんな'],
        'correctAnswer': 'いつ',
        'distractors_en': {
            'どう': 'どう+から is ungrammatical (どう doesn\'t take から).',
            'なぜ': 'なぜ+から is ungrammatical (なぜ stands alone; cause-of-cause is awkward).',
            'どんな': 'どんな needs a following noun; どんなから is ungrammatical.',
        },
        'distractors_hi': {
            'どう': 'どう+から व्याकरण-सम्मत नहीं।',
            'なぜ': 'なぜ+から व्याकरण-सम्मत नहीं।',
            'どんな': 'どんな के बाद संज्ञा चाहिए; どんなから व्याकरण-सम्मत नहीं।',
        },
        'reason': 'Added "「3ねん前です。」と こたえました。" answer-hint to lock "since when" → いつ. Replaced だれ/どこ/なに (all valid as from-X) with Q-words that don\'t attach to から.',
    },
    'q-0433': {
        'question_ja': 'おしごとは（　）ですか。 — たのしいです。',
        'choices': ['どう', 'だれ', 'どんな', 'なぜ'],
        'correctAnswer': 'どう',
        'distractors_en': {
            'だれ': 'だれ asks for a person; work isn\'t a person.',
            'どんな': 'どんな needs a following noun; どんなですか is incomplete.',
            'なぜ': 'なぜ asks "why"; doesn\'t fit asking about a state/quality.',
        },
        'distractors_hi': {
            'だれ': 'だれ व्यक्ति पूछता है; काम व्यक्ति नहीं।',
            'どんな': 'どんな के बाद संज्ञा चाहिए; どんなですか अधूरा।',
            'なぜ': 'なぜ "क्यों" पूछता है; स्थिति/गुण के बारे में नहीं।',
        },
        'reason': 'Added "— たのしいです。" reply-hint to lock "how" (asking about quality). Replaced いつ/どこ (also valid info-type questions) with semantically-impossible Q-words.',
    },
}

PAPER_FIXES = {
    'bunpou-1.13': {
        'paper_path': 'data/papers/bunpou/paper-1.json',
        'stem_html': 'おかね（　　）ぜんぜん ありませんから、何も 買いません。',
        'choices': ['を', 'に', 'へ', 'が'],
        'correctIndex': 3,  # が
        'rationale': 'ある/あります takes が as the subject particle: おかねが ありません. The added ぜんぜん (not at all) locks the existential-negation reading, where が is canonical. を/に/へ don\'t fit subject-of-ある.',
        'rationale_hi': 'ある/あります विषय कण के रूप में が लेता है: おかねが ありません। ぜんぜん (बिल्कुल नहीं) जोड़ने से अस्तित्व-नकार पठन तय हो जाता है। を/に/へ ある के विषय के साथ नहीं आते।',
        'reason': 'Replaced は (おかねは ありません also fully grammatical) with へ (direction marker, wrong for subject slot). Added ぜんぜん to strengthen the existential-negation read where が is canonical.',
    },
}


def lf_size(p): return len(Path(p).read_bytes().replace(b'\r\n', b'\n'))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    q = json.loads(QUESTIONS.read_text(encoding='utf-8'))
    q_changes = []
    for it in q['questions']:
        if it['id'] in QUESTION_FIXES:
            f = QUESTION_FIXES[it['id']]
            before = {'q': it.get('question_ja'), 'ch': list(it.get('choices') or []), 'ca': it.get('correctAnswer')}
            it['question_ja'] = f['question_ja']
            it['choices'] = list(f['choices'])
            it['correctAnswer'] = f['correctAnswer']
            it['distractor_explanations'] = f['distractors_en']
            it['distractor_explanations_hi'] = f['distractors_hi']
            it['distractor_explanations_hi_provenance'] = 'auto_fix_2026_05_25'
            it['provenance'] = 'auto_fix_2026_05_25'
            it['audit_wave'] = 'claude_audit_2026_05_25'
            it['review_status'] = 'ai_native_reviewer_2026_05_25'
            it['reviewer_note'] = f['reason']
            it['explanation_en'] = f'Only {f["correctAnswer"]} is the natural answer here. {f["reason"]}'
            assert it['correctAnswer'] in it['choices']
            q_changes.append({'id': it['id'], 'before': before, 'after': {'q': f['question_ja'], 'ch': f['choices'], 'ca': f['correctAnswer']}})
            print(f"  {it['id']}: {f['question_ja'][:60]}")
            print(f"    choices: {f['choices']}, correct: {f['correctAnswer']}")

    p_changes = []
    for qid, fix in PAPER_FIXES.items():
        path = Path(fix['paper_path'])
        d = json.loads(path.read_text(encoding='utf-8'))
        for q_ in d.get('questions') or []:
            if q_.get('id') == qid:
                before = {'stem': q_.get('stem_html'), 'ch': list(q_.get('choices') or []), 'ci': q_.get('correctIndex')}
                q_['stem_html'] = fix['stem_html']
                q_['choices'] = list(fix['choices'])
                q_['correctIndex'] = fix['correctIndex']
                q_['rationale'] = fix['rationale']
                q_['rationale_hi'] = fix['rationale_hi']
                p_changes.append({'id': qid, 'before': before, 'after': {'stem': fix['stem_html'], 'ch': fix['choices'], 'ci': fix['correctIndex']}})
                print(f"  {qid}: {fix['stem_html'][:60]}")
                print(f"    choices: {fix['choices']}, correct: {fix['choices'][fix['correctIndex']]}")
        if args.apply:
            path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'\nquestions.json fixes: {len(q_changes)}')
    print(f'paper fixes: {len(p_changes)}')

    if args.apply:
        QUESTIONS.write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        idx = json.loads(INDEX.read_text(encoding='utf-8'))
        for entry in idx.get('files', []):
            path = entry.get('path')
            if path and Path(path).exists():
                entry['size_bytes'] = lf_size(path)
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        log = json.loads(FIX_LOG.read_text(encoding='utf-8'))
        log['horizontal_mcq_ambiguity_fix_2026_05_25'] = {
            'description': 'Horizontal MCQ ambiguity sweep beyond JA-167 verb-ending class. Surfaced 5 question_word + 1 particle ambiguity across questions.json + 1 in papers. Fixed via context cues (answer-hints, constraining adverbs) + semantically-wrong Q-word distractors. bunpou-1.5 (kyou が/は) deliberately not fixed (は dominant in canonical teaching; reviewer polish only).',
            'questions_json_fixes': q_changes,
            'paper_fixes': p_changes,
        }
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
