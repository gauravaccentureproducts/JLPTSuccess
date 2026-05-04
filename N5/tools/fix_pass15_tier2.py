"""
Pass-15 Tier-2 Japanese-accuracy fixes.

Three categories addressed:

1. F-15.12: q-0421 was a duplicate of q-0420 (both tested sentence-final か,
   but q-0421 was tagged to n5-024 = OR-between-alternatives か). Fix:
   rewrite q-0421's stem to test the OR sense.

2. F-15.13: n5-024 grammar pattern's first two examples were copy-pasted
   from n5-023 (sentence-final か), so they don't illustrate the OR sense
   the pattern is supposed to teach. Replace with real OR-か examples.

3. F-15.14 / F-15.15: q-0007 and q-0008 are early N5 questions teaching
   が-with-すき and direct-object を respectively. Without context, は is
   grammatically valid (contrastive topic) for both. Add minimal context
   that forces the canonical N5 reading and replace stub
   distractor_explanations with real reasons.

Idempotent.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = ROOT / 'data' / 'questions.json'
GRAMMAR_PATH = ROOT / 'data' / 'grammar.json'

QUESTION_FIXES = {
    'q-0421': {
        'question_ja': 'コーヒー（  ） おちゃが いいです。',
        'prompt_ja': 'ふたつの えらびかたを ならべる ことばを えらんで ください。',
        'choices': ['か', 'は', 'が', 'を'],
        'correctAnswer': 'か',
        'explanation_en': "か between two nouns means 'or' — it joins alternatives, e.g., コーヒーか おちゃ ('coffee or tea'). This is the use covered by pattern n5-024 (distinct from sentence-final か / question marker, which is n5-023).",
        'distractor_explanations': {
            'は': "は marks the topic. Between two nouns it does not mean 'or'; it would split the sentence into a topic-comment relation that does not fit here.",
            'が': "が marks the subject. It does not connect two alternative nouns. The OR-particle is か.",
            'を': "を marks a direct object. It does not connect two alternative nouns. The OR-particle is か.",
        },
    },
    # F-15.14: q-0007 ねこ___すきです (correct=が)
    'q-0007': {
        'question_ja': 'A：「どんな どうぶつが すきですか。」　B：「ねこ（  ）すきです。」',
        'prompt_ja': '「すきな もの」を こたえる ときに つかう ことばを えらんで ください。',
        'choices': ['は', 'が', 'を', 'に'],
        'correctAnswer': 'が',
        'explanation_en': "The pattern X が すき expresses 'I like X'. When answering 'What do you like?', the liked-thing always takes が. (は can sound contrastive — 'as for cats, [I] like [them], but...' — which is N3+ nuance and doesn't match this direct answer.)",
        'distractor_explanations': {
            'は': "は would topicalize 'cats' and add a contrastive nuance ('as for cats... [implying contrast with another animal]'). When directly answering 'what do you like', the natural particle is が.",
            'を': "を marks the direct object of a transitive verb. すき (好き) is a な-adjective ('liked'), not a verb, so its target is marked with が, not を.",
            'に': "に marks destination, recipient, or specific time. It does not mark the target of すき / きらい / じょうず etc. — those use が.",
        },
    },
    # F-15.15: q-0008 ほん___よみます (correct=を)
    'q-0008': {
        'question_ja': '（としょかんで）　わたしは ほん（  ）よみます。',
        'prompt_ja': '「よみます」の もくてきごを しめす ことばを えらんで ください。',
        'choices': ['は', 'が', 'を', 'に'],
        'correctAnswer': 'を',
        'explanation_en': "を marks the direct object of a transitive verb. ほんを よみます = 'I read books'. (は can topicalize 'books' for contrastive nuance — 'as for books, [I] read [them], but...' — which is N3+ pragmatics and doesn't fit a plain statement of what one does at the library.)",
        'distractor_explanations': {
            'は': "は would topicalize 'books' with contrastive nuance ('as for books...'). For a simple statement 'I read books', the direct-object particle is を.",
            'が': "が marks the subject (the doer). 'Books' is what is read, not who is reading — so it cannot take が.",
            'に': "に marks destination, recipient, or specific time. It does not mark the direct object of an action verb.",
        },
    },
}

# Replace the wrong examples in n5-024 (currently copied from n5-023).
# Keep only the one example that does illustrate OR-か and add two more.
GRAMMAR_FIX_N5_024_EXAMPLES = [
    {
        'form': 'noun か noun',
        'ja': 'コーヒーか おちゃが いいです。',
        'translation_en': 'Coffee or tea would be good.',
    },
    {
        'form': 'noun か noun',
        'ja': 'ペンか えんぴつで かいてください。',
        'translation_en': 'Please write with a pen or pencil.',
    },
    {
        'form': 'time-noun か time-noun',
        'ja': 'あしたか あさってに いきます。',
        'translation_en': "I'll go tomorrow or the day after.",
    },
]


def fix_questions():
    with QUESTIONS_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)

    fixed, skipped = [], []
    for q in data['questions']:
        qid = q.get('id')
        if qid not in QUESTION_FIXES:
            continue
        patch = QUESTION_FIXES[qid]
        if q.get('question_ja') == patch['question_ja']:
            skipped.append(qid)
            continue
        for k, v in patch.items():
            q[k] = v
        q['auto'] = False
        fixed.append(qid)

    if fixed:
        with QUESTIONS_PATH.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return fixed, skipped


def fix_grammar():
    with GRAMMAR_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)

    target_idx = None
    for i, p in enumerate(data['patterns']):
        if p.get('id') == 'n5-024':
            target_idx = i
            break
    if target_idx is None:
        return False, 'n5-024 not found'

    pattern = data['patterns'][target_idx]
    current_examples = pattern.get('examples', [])
    # Idempotency: if the OR examples are already in place (i.e., the second
    # example is the pen-pencil one), skip.
    if (len(current_examples) >= 2
            and 'ペン' in (current_examples[1].get('ja') or '')):
        return False, 'already-fixed'

    # Preserve any non-example fields. Replace examples wholesale.
    pattern['examples'] = GRAMMAR_FIX_N5_024_EXAMPLES

    with GRAMMAR_PATH.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True, 'fixed'


if __name__ == '__main__':
    qf, qs = fix_questions()
    print(f'Questions fixed: {qf}')
    print(f'Questions skipped: {qs}')
    gf, msg = fix_grammar()
    print(f'Grammar n5-024: {msg} (changed={gf})')
