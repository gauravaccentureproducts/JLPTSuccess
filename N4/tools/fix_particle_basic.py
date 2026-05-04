"""
Pass-15 Basic-issue fix #2: particle questions with multi-correct distractors.

Native-teacher review identified six MCQs where the stem accepts two of the
four particle options as grammatically valid. Fixes either:
  (a) replace one of the multi-correct distractors with a clearly-wrong
      particle, OR
  (b) add scene-setting that makes only the marked-correct answer natural,
      OR
  (c) tighten the verb / object so semantic ambiguity collapses.

Affected:
  q-0013  どこ___いきますか — へ/に ambiguous → replace に with から in choices
  q-0026  わたし___がくせいです (も) — は/も ambiguous → add prior-sentence
  q-0422  わたし___がくせいです (も) — same bug, different scene to avoid dup
  q-0016  ともだち___いきました (と) — と/に ambiguous → add destination
  q-0020  5時___しごとです (まで) — まで/から ambiguous → add 9時から prefix
  q-0044  ともだち___でんわをしました (に) — に/と ambiguous → use かけました

Idempotent: re-running after a fix is a no-op.
"""
import json
from pathlib import Path

QUESTIONS_PATH = Path(__file__).resolve().parent.parent / 'data' / 'questions.json'

FIXES = {
    'q-0013': {
        # Replace に in distractors with から (which is wrong here — どこから
        # changes the meaning to "where from"). へ is now uniquely correct
        # for motion destination.
        'question_ja': 'どこ（　）いきますか。',
        'choices': ['で', 'へ', 'を', 'から'],
        'correctAnswer': 'へ',
        'explanation_en': "へ marks the direction of motion verbs (いく / 行く). At N5 level, へ is the canonical direction marker; に also works for arrival points but a JLPT MCQ should not present both as choices, so this question uses から (the wrong direction) as the contrast distractor.",
        'distractor_explanations': {
            'で': "で marks the location of an action (e.g., こうえんで あそびます = play at the park). For the destination of motion, use へ.",
            'を': "を marks the path being traversed (e.g., こうえんを さんぽします = walk through the park), or a direct object. For the destination of いきます, use へ.",
            'から': "から means 'from'. どこから いきますか would ask the starting point, not the destination. Use へ for where one is going.",
        },
    },
    'q-0026': {
        'question_ja': '（田中さんは がくせいです。）　わたし（　）がくせいです。',
        'prompt_ja': '前の 文と おなじ ことを 言う ときの ことばを えらんで ください。',
        'choices': ['は', 'も', 'が', 'を'],
        'correctAnswer': 'も',
        'explanation_en': "も means 'also/too'. After a previous sentence already states X is a student, わたしも がくせいです adds the speaker to that group. Without the additive context, わたしは and わたしも are both grammatical (with different meanings); the prior sentence here forces the additive reading.",
        'distractor_explanations': {
            'は': "は would topicalize 'I' but lose the 'also' meaning. Since 田中さん has already been said to be a student, the natural connector is も ('me too').",
            'が': "が would mark the speaker as the focused / selected subject ('it is I who am the student'), which contradicts the additive context.",
            'を': "を marks a direct object of a transitive verb. がくせい is a noun predicate, not an object — を doesn't fit.",
        },
    },
    'q-0422': {
        'question_ja': '（さとうさんも たなかさんも がくせいです。）　わたし（　）がくせいです。',
        'prompt_ja': 'ほかにも がくせいが いる ことを ふまえて、じぶんも おなじだと 言う ことばを えらんで ください。',
        'choices': ['も', 'は', 'が', 'を'],
        'correctAnswer': 'も',
        'explanation_en': "When prior context lists multiple people who share the same status, the additive particle も extends that status to include the speaker. わたしも がくせいです = 'I am also a student.'",
        'distractor_explanations': {
            'は': "は would just topicalize 'I' without the 'also' nuance. The context lists multiple students, so the additive も is what natively connects the speaker to the group.",
            'が': "が would single out the speaker as the focused subject, which clashes with the inclusive context (the prior sentence already names other students).",
            'を': "を marks a direct object of a transitive verb. がくせい is the noun predicate of a copula sentence — を is grammatically impossible here.",
        },
    },
    'q-0016': {
        'question_ja': 'ともだち（　）こうえんへ いきました。',
        'choices': ['に', 'で', 'と', 'を'],
        'correctAnswer': 'と',
        'explanation_en': "と marks the companion / co-actor of the action. With an explicit destination (こうえんへ), the only natural reading for ともだち___ is 'with my friend'. Without the destination, ともだちに いきました 'went to my friend's place' is also valid — that's why the destination clause is required to disambiguate.",
        'distractor_explanations': {
            'に': "に would mark a destination ('went to my friend'), but the destination slot is already filled by こうえんへ. So ともだち__ here must mark the companion, which uses と.",
            'で': "で marks location of action or means/instrument. It does not fit a person performing the action together with the speaker.",
            'を': "を marks a direct object (or path with motion verbs). A person who joins the action is not a direct object — use と.",
        },
    },
    'q-0020': {
        'question_ja': '（あさは 9時から はじまります。）　5時（　）しごとです。',
        'prompt_ja': '前の 文の 「9時から」と セットで 「いつまで」を あらわす ことばを えらんで ください。',
        'choices': ['から', 'まで', 'に', 'で'],
        'correctAnswer': 'まで',
        'explanation_en': "まで marks the end-point of a range (time or place). Paired with から ('from'), the structure 〜から 〜まで expresses 'from X until Y'. The prior sentence already supplies 9時から ('from 9'); the blank requires the matching まで for 'until 5'.",
        'distractor_explanations': {
            'から': "から means 'from'. The prior sentence already established 9時から, so the missing piece is the end-point — まで.",
            'に': "に marks a single point in time (e.g., 5時に おきます = 'wake up at 5'). It does not pair with から to express a range.",
            'で': "で marks location of action or means. It does not mark a time end-point.",
        },
    },
    'q-0044': {
        'question_ja': 'ともだち（　）でんわを かけました。',
        'choices': ['を', 'に', 'で', 'と'],
        'correctAnswer': 'に',
        'explanation_en': "でんわを かける ('to make / place a phone call') takes に for the recipient — the person being called. Note: でんわを する (a more general verb) can take と for 'phone-talk with', so the verb was changed to かけました to lock the answer to に.",
        'distractor_explanations': {
            'を': "を marks the direct object — but でんわを is already filling that slot. The recipient of かける takes a separate particle (に).",
            'で': "で marks location of action or means/instrument. It cannot mark the recipient of a phone call.",
            'と': "と would mean 'phoned WITH (i.e., talked together)' — that nuance pairs with でんわを する, not かける. Since the verb is かけました ('made a call'), the recipient takes に.",
        },
    },
}


def main():
    with QUESTIONS_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)

    fixed = []
    skipped = []
    for q in data['questions']:
        qid = q.get('id')
        if qid not in FIXES:
            continue
        patch = FIXES[qid]
        if q.get('question_ja') == patch['question_ja'] and q.get('choices') == patch['choices']:
            skipped.append(qid)
            continue
        for k, v in patch.items():
            q[k] = v
        q['auto'] = False
        fixed.append(qid)

    if fixed:
        with QUESTIONS_PATH.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Fixed: {fixed}')
    print(f'Skipped (already fixed): {skipped}')
    missing = set(FIXES) - set(fixed) - set(skipped)
    if missing:
        print(f'WARNING - not found: {sorted(missing)}')


if __name__ == '__main__':
    main()
