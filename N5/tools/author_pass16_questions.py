"""
Pass-16 question authoring for the 6 zero-coverage patterns identified in
Pass-15 cross-coverage analysis (TASKS.md F-15.18 .. F-15.23).

Authors 10 new MCQs across 5 patterns:
  - n5-130 あげる (give to others)            : 2 questions
  - n5-131 もらう (receive from)              : 2 questions
  - n5-134 ので (because, softer than から)   : 2 questions
  - n5-144 Verb-stem + ながら (while doing)   : 2 questions
  - n5-148 いつも / たいてい / たまに         : 2 questions

n5-167 (んです / のです) is intentionally skipped per F-15.23 — borderline
N5/N4, needs native-teacher input on N5-appropriate framing.

Each question:
  - Stem with explicit context (no multi-correct trap)
  - Real distractor_explanations (not stub 'see pattern detail')
  - Only N5-allowed kanji; integrity check JA-13 enforces
  - auto: false (manually authored)
  - difficulty: 2 (these patterns are mid-N5)

Idempotent: re-running after IDs are present is a no-op.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_PATH = ROOT / 'data' / 'questions.json'

NEW_QUESTIONS = [
    # ---------------- n5-130 あげる (give to others) ----------------
    {
        'id': 'q-0454',
        'grammarPatternId': 'n5-130',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': '「あげる」と いっしょに つかう、もらう人を しめす ことばを えらんで ください。',
        'question_ja': 'わたしは ともだち（  ）プレゼントを あげました。',
        'choices': ['に', 'を', 'へ', 'から'],
        'correctAnswer': 'に',
        'explanation_en': "あげる takes に for the recipient (the person who receives the gift). Structure: [giver] は [recipient] に [item] を あげる.",
        'distractor_explanations': {
            'を': "を already marks プレゼント (the thing being given). あげる takes one を for the object, not two. The recipient slot uses に.",
            'へ': "へ marks the destination of motion verbs (e.g., がっこうへ いく). For the recipient of giving / receiving verbs, use に.",
            'から': "から marks the SOURCE of an action ('from'). 'Friend から' would mean the friend gave something to me — the opposite direction of あげる. Use に for 'to whom'.",
        },
        'high_confusion': False,
        'difficulty': 2,
        'auto': False,
    },
    {
        'id': 'q-0455',
        'grammarPatternId': 'n5-130',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': '「あげる」の もくてきご（あげる もの）を しめす ことばを えらんで ください。',
        'question_ja': '父は 母に はな（  ）あげました。',
        'choices': ['を', 'が', 'に', 'で'],
        'correctAnswer': 'を',
        'explanation_en': "を marks the direct object — what is being given. Structure: [giver] は [recipient] に [item] を あげる. Here father (父) gives flowers (はな) to mother (母).",
        'distractor_explanations': {
            'が': "が marks the subject. Father is already the topic (父は); flowers are not the doer of the action.",
            'に': "に marks the recipient (母に already takes に). The thing given uses を, not に.",
            'で': "で marks instrument or location of action. It does not mark the object that is given.",
        },
        'high_confusion': False,
        'difficulty': 2,
        'auto': False,
    },
    # ---------------- n5-131 もらう (receive from) ----------------
    {
        'id': 'q-0456',
        'grammarPatternId': 'n5-131',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': '「もらう」と いっしょに つかう、くれた人を しめす ことばを えらんで ください。',
        'question_ja': 'わたしは 父（  ）おかねを もらいました。',
        'choices': ['から', 'へ', 'で', 'と'],
        'correctAnswer': 'から',
        'explanation_en': "から marks the source — the person from whom something is received. Structure: [receiver] は [source] から [item] を もらう. Note: に also works for the source with もらう (e.g., 父に もらいました), but から is the most direct way to signal 'from' and is unambiguous in this MCQ.",
        'distractor_explanations': {
            'へ': "へ marks the destination of motion verbs. The source of もらう (the giver) takes から (or に), never へ.",
            'で': "で marks instrument or location of action. It does not mark the source-person of もらう.",
            'と': "と marks a companion ('with'). 'Father と' would mean 'together with father', not 'from father'. Use から for the source.",
        },
        'high_confusion': False,
        'difficulty': 2,
        'auto': False,
    },
    {
        'id': 'q-0457',
        'grammarPatternId': 'n5-131',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': '「もらう」の もくてきご（もらった もの）を しめす ことばを えらんで ください。',
        'question_ja': 'わたしは 兄から プレゼント（  ）もらいました。',
        'choices': ['を', 'が', 'に', 'へ'],
        'correctAnswer': 'を',
        'explanation_en': "を marks the direct object — what is being received. Structure: [receiver] は [source] から [item] を もらう. Here 'I' receive a present (プレゼント) from 'older brother' (兄).",
        'distractor_explanations': {
            'が': "が marks the subject. The receiver (わたし) is already the topic; the present is not the doer of the action.",
            'に': "に could mark the source (兄に もらいました), but 兄から already fills that role. The thing being received uses を.",
            'へ': "へ marks motion destinations. It cannot mark a direct object.",
        },
        'high_confusion': False,
        'difficulty': 2,
        'auto': False,
    },
    # ---------------- n5-134 ので (because, softer than から) ----------------
    {
        'id': 'q-0458',
        'grammarPatternId': 'n5-134',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': 'りゆうを やわらかく いう ときに つかう ことばを えらんで ください。',
        'question_ja': 'あたまが いたい（  ）、学校を やすみます。',
        'choices': ['ので', 'ながら', 'ても', 'のに'],
        'correctAnswer': 'ので',
        'explanation_en': "ので means 'because' / 'so' and is softer / more polite than から. It attaches to the plain form of verbs and adjectives. Here: 'My head hurts, so I'll be absent from school.'",
        'distractor_explanations': {
            'ながら': "ながら means 'while doing'. It expresses simultaneous actions, not cause-and-effect.",
            'ても': "ても means 'even if'. 'Even if my head hurts, I'll be absent' contradicts the natural causal reading.",
            'のに': "のに means 'although' / 'despite'. 'Although my head hurts, I'll be absent' is the opposite of the intended 'because' relationship.",
        },
        'high_confusion': True,
        'difficulty': 2,
        'auto': False,
    },
    {
        'id': 'q-0459',
        'grammarPatternId': 'n5-134',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': 'なまえ（めいし）に 「ので」を つける ときに ひつような 文字を えらんで ください。',
        'question_ja': '今日は 雨（  ）ので、行きません。',
        'choices': ['な', 'の', 'だ', 'で'],
        'correctAnswer': 'な',
        'explanation_en': "When ので follows a noun or な-adjective, you must insert な between them: 雨 → 雨なので. The plain copula だ does not appear before ので; it becomes な.",
        'distractor_explanations': {
            'の': "雨のので is ungrammatical. The connector for noun + ので is な, not の. (の is the genitive / possessive particle, used differently.)",
            'だ': "雨だので is incorrect. The plain-form copula だ does not survive in front of ので — it shifts to な instead.",
            'で': "雨でので doubles up the で / な-form connectors and is ungrammatical. The fixed pattern is noun + な + ので.",
        },
        'high_confusion': True,
        'difficulty': 2,
        'auto': False,
    },
    # ---------------- n5-144 Verb-stem + ながら ----------------
    {
        'id': 'q-0460',
        'grammarPatternId': 'n5-144',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': '「べんきょうしながら」「ラジオを ―」のように、ふたつの ことを どうじに する ことを あらわす かたちを えらんで ください。',
        'question_ja': 'ラジオを （  ）べんきょうします。',
        'choices': ['ききながら', 'きいて', 'ききました', 'きかない'],
        'correctAnswer': 'ききながら',
        'explanation_en': "Verb-stem + ながら expresses two actions performed simultaneously by the same subject. きく (to listen) → stem きき + ながら = ききながら ('while listening'). Note: both actions must share the same subject.",
        'distractor_explanations': {
            'きいて': "きいて (te-form) connects sequential actions: 'listen, then study'. It does not express simultaneous action.",
            'ききました': "ききました is past polite — a complete sentence ending. It cannot connect two actions in the middle of one sentence.",
            'きかない': "きかない is the negative ('don't listen'), and gives the wrong meaning. It also doesn't form the simultaneous-action structure.",
        },
        'high_confusion': False,
        'difficulty': 2,
        'auto': False,
    },
    {
        'id': 'q-0461',
        'grammarPatternId': 'n5-144',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': 'どうしの 「のみ」と いっしょに つかって、「どうじに」を あらわす ことばを えらんで ください。',
        'question_ja': 'コーヒーを のみ（  ）、本を 読みます。',
        'choices': ['ながら', 'ので', 'から', 'でも'],
        'correctAnswer': 'ながら',
        'explanation_en': "ながら attaches directly to a verb stem (のみ + ながら = のみながら) and means 'while [doing]'. Here: 'I read a book while drinking coffee.' Same subject for both verbs is required.",
        'distractor_explanations': {
            'ので': "ので attaches to the plain form (e.g., のむので), not to the verb stem. のみので is ungrammatical.",
            'から': "から (because / from) does not attach to a bare verb stem. のみから is ungrammatical in this context.",
            'でも': "でも means 'even / but'. It does not attach to a bare verb stem here, and it does not express simultaneous action.",
        },
        'high_confusion': True,
        'difficulty': 2,
        'auto': False,
    },
    # ---------------- n5-148 いつも / たいてい / たまに ----------------
    {
        'id': 'q-0462',
        'grammarPatternId': 'n5-148',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': '「毎日」と おなじ いみで、「100%」を あらわす ことばを えらんで ください。',
        'question_ja': 'わたしは 毎日 7時に おきます。（  ）7時に おきます。',
        'choices': ['いつも', 'たまに', 'あまり', 'ぜんぜん'],
        'correctAnswer': 'いつも',
        'explanation_en': "いつも means 'always' (100% of the time). It naturally pairs with 毎日 ('every day') to emphasize total consistency.",
        'distractor_explanations': {
            'たまに': "たまに means 'occasionally' (low frequency). It contradicts 毎日 ('every day').",
            'あまり': "あまり ('not much') only works with negative verbs (e.g., あまり 行きません). With the positive 'おきます', it is ungrammatical.",
            'ぜんぜん': "ぜんぜん ('not at all') only works with negative verbs and means complete absence. It contradicts the positive 毎日.",
        },
        'high_confusion': False,
        'difficulty': 2,
        'auto': False,
    },
    {
        'id': 'q-0463',
        'grammarPatternId': 'n5-148',
        'type': 'mcq',
        'direction': 'j_to_e',
        'prompt_ja': '「月に 1回」のような ひくい ひんどを あらわす ことばを えらんで ください。',
        'question_ja': 'わたしは 月に 1回 えいがを 見ます。（  ）えいがを 見ます。',
        'choices': ['たまに', 'いつも', 'とても', 'よく'],
        'correctAnswer': 'たまに',
        'explanation_en': "たまに means 'occasionally / once in a while' (low frequency). It naturally pairs with '月に 1回' ('once a month'), which describes infrequent activity.",
        'distractor_explanations': {
            'いつも': "いつも ('always') describes 100% frequency. It contradicts '月に 1回' (only once a month).",
            'とても': "とても means 'very' — it modifies degree, not frequency. *とても 見ます is ungrammatical for an action verb.",
            'よく': "よく ('often / frequently') describes high-medium frequency. It contradicts the explicit '月に 1回' which is low frequency.",
        },
        'high_confusion': True,
        'difficulty': 2,
        'auto': False,
    },
]


def main():
    with QUESTIONS_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)

    existing_ids = {q['id'] for q in data['questions']}
    added = []
    skipped = []
    for nq in NEW_QUESTIONS:
        if nq['id'] in existing_ids:
            skipped.append(nq['id'])
            continue
        data['questions'].append(nq)
        added.append(nq['id'])

    if added:
        with QUESTIONS_PATH.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Added: {added}')
    print(f'Skipped (already present): {skipped}')


if __name__ == '__main__':
    main()
