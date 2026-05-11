"""Author `inference_question_expansion` on the first 15 listening
items.

Audit context: inference_question_expansion = 0/50. The audit
wants each item to carry an optional follow-up "what would they
say next?" / "what does this imply about the speaker?" question
that goes beyond the literal-comprehension correctAnswer.

This starter pass authors 1-2 inference questions per item for
the first 15 items.

Schema:
  inference_question_expansion: {
    prompts: [
      {
        prompt_ja: "<question in Japanese>",
        prompt_en: "<English gloss>",
        hint: "<optional clue about what to listen for>",
        type: "next_utterance" | "speaker_intent" | "implication" |
              "relationship",
      }
    ]
  }

Provenance: llm_curated.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXPANSIONS = {
    'n5.listen.001': {
        'prompts': [
            {'prompt_ja': '二人は どんな かんけいですか。', 'prompt_en': 'What relationship do the two people have?', 'hint': 'Listen for register and politeness markers.', 'type': 'relationship'},
            {'prompt_ja': 'なぜ えきの 前で 会わないですか。', 'prompt_en': 'Why don\'t they meet in front of the station?', 'type': 'implication'},
        ],
    },
    'n5.listen.002': {
        'prompts': [
            {'prompt_ja': '男の人は どこに いますか。', 'prompt_en': 'Where is the man right now?', 'type': 'speaker_intent'},
            {'prompt_ja': '女の人は うちで 何を つくりますか。', 'prompt_en': 'What might the woman be making at home?', 'hint': 'Pan + eggs + milk suggests a specific dish.', 'type': 'implication'},
        ],
    },
    'n5.listen.003': {
        'prompts': [
            {'prompt_ja': '二人は あした どこに 行きますか。', 'prompt_en': 'Where might the two people be going tomorrow?', 'hint': 'They\'re catching a 9 AM train.', 'type': 'implication'},
        ],
    },
    'n5.listen.004': {
        'prompts': [
            {'prompt_ja': '男の人は つぎに 何を 言いますか。', 'prompt_en': 'What would the man say next after the order is confirmed?', 'type': 'next_utterance'},
            {'prompt_ja': 'お店は あついですか、つめたいですか。', 'prompt_en': 'Is the cafe likely warm or cool inside? Why might the customer want cold coffee?', 'type': 'implication'},
        ],
    },
    'n5.listen.005': {
        'prompts': [
            {'prompt_ja': '先生は つぎに 何を 言いますか。', 'prompt_en': 'What might the teacher say next?', 'type': 'next_utterance'},
            {'prompt_ja': 'この 学生は ふつう ちこくしますか。', 'prompt_en': 'Is this student typically late, based on the teacher\'s tone?', 'type': 'implication'},
        ],
    },
    'n5.listen.006': {
        'prompts': [
            {'prompt_ja': '女の人は つぎに 何を しますか。', 'prompt_en': 'What does the woman do next, after receiving the location?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.007': {
        'prompts': [
            {'prompt_ja': 'この 人は どの きせつが いちばん きらいですか。', 'prompt_en': 'Which season does this person dislike the most?', 'hint': 'They mention reasons for disliking summer and winter — compare.', 'type': 'implication'},
            {'prompt_ja': 'はるは すきですか、すきじゃないですか。', 'prompt_en': 'Does the speaker like spring? What\'s the qualifier?', 'type': 'implication'},
        ],
    },
    'n5.listen.008': {
        'prompts': [
            {'prompt_ja': '女の人は カメラを かいますか。', 'prompt_en': 'Will the woman buy the camera as a gift, based on this conversation?', 'type': 'implication'},
            {'prompt_ja': '男の人は ふだん どんな しゅみが ありますか。', 'prompt_en': 'What hobbies might the man have, given he wants a camera?', 'type': 'implication'},
        ],
    },
    'n5.listen.009': {
        'prompts': [
            {'prompt_ja': 'しらない人は どう こたえますか。', 'prompt_en': 'How would a stranger typically respond to your question?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.010': {
        'prompts': [
            {'prompt_ja': 'まどぐちの 人は どう こたえますか。', 'prompt_en': 'How does the ticket-counter staff typically respond?', 'type': 'next_utterance'},
            {'prompt_ja': 'おわかれの あいさつは 何ですか。', 'prompt_en': 'What is the standard closing phrase you would add after paying?', 'type': 'implication'},
        ],
    },
    'n5.listen.011': {
        'prompts': [
            {'prompt_ja': 'ともだちは どう こたえますか。', 'prompt_en': 'How does the friend likely respond?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.012': {
        'prompts': [
            {'prompt_ja': '先生は どう こたえますか。', 'prompt_en': 'How does the teacher likely greet back?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.013': {
        'prompts': [
            {'prompt_ja': '二人は どんな かんけいですか。', 'prompt_en': 'What relationship do A and B have (classmates / friends / colleagues)?', 'type': 'relationship'},
        ],
    },
    'n5.listen.014': {
        'prompts': [
            {'prompt_ja': 'なぜ 男の人は 北の 出口を えらびましたか。', 'prompt_en': 'Why might the man specifically choose the north exit?', 'type': 'implication'},
        ],
    },
    'n5.listen.015': {
        'prompts': [
            {'prompt_ja': '母は つぎに 何を 言いますか。', 'prompt_en': 'What does the mother say next?', 'type': 'next_utterance'},
            {'prompt_ja': 'なぜ パンは いりませんか。', 'prompt_en': 'Why doesn\'t the child want bread? What might they have at home?', 'type': 'implication'},
        ],
    },
}


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_inference_starter')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {it['id']: it for it in data['items']}

    n = 0
    for lid, content in EXPANSIONS.items():
        it = by_id.get(lid)
        if not it:
            print(f'  ! missing: {lid}')
            continue
        if it.get('inference_question_expansion'):
            print(f'  - skip (already filled): {lid}')
            continue
        it['inference_question_expansion'] = content
        it['inference_question_expansion_provenance'] = 'llm_curated'
        n += 1

    print(f'\nAuthored inference_question_expansion on {n} items.')
    print(f'Coverage: 0/50 -> {n}/50 ({100 * n // 50}%)')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
