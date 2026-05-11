"""Wave 2 — extend listening inference_question_expansion to items 16-30.

Wave 1 (2026-05-11) covered the first 15 items. This wave adds
1-2 prompts to each of items 16-30.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXPANSIONS = {
    'n5.listen.016': {
        'prompts': [
            {'prompt_ja': 'なぜ さいしょの 友だちと 行きませんか。', 'prompt_en': 'Why isn\'t B going with their original friend?', 'type': 'implication'},
            {'prompt_ja': 'B さんと 母は どんな かんけいですか。', 'prompt_en': 'What does this tell us about B\'s relationship with their mother?', 'type': 'relationship'},
        ],
    },
    'n5.listen.017': {
        'prompts': [
            {'prompt_ja': '先生は どうして おくれますか。', 'prompt_en': 'Why is the teacher running late?', 'type': 'speaker_intent'},
            {'prompt_ja': '三時半に なったら、つぎに 何が おこりますか。', 'prompt_en': 'What probably happens when the teacher arrives at 3:30?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.018': {
        'prompts': [
            {'prompt_ja': 'B さんは 自分の 父と 行きますか。', 'prompt_en': 'Is B going with their own father, or to their father\'s friend\'s house?', 'type': 'implication'},
            {'prompt_ja': 'なぜ くるまで 行かないですか。', 'prompt_en': 'Why might they choose train over driving?', 'type': 'inference'},
        ],
    },
    'n5.listen.019': {
        'prompts': [
            {'prompt_ja': '先生は 学生を しかりますか、ゆるしますか。', 'prompt_en': 'Will the teacher scold the student or accept the excuse?', 'type': 'implication'},
        ],
    },
    'n5.listen.020': {
        'prompts': [
            {'prompt_ja': 'B さんは その 本を きにいって いますか。', 'prompt_en': 'Does B think the book is worth the price?', 'type': 'implication'},
        ],
    },
    'n5.listen.021': {
        'prompts': [
            {'prompt_ja': 'にちようびに 行きたいです。 行けますか。', 'prompt_en': 'If you wanted to go on Sunday, could you? (Listen for what days are mentioned.)', 'type': 'application'},
        ],
    },
    'n5.listen.022': {
        'prompts': [
            {'prompt_ja': 'あさっての 計画を 立てる ほうが いいですか、あしたの 計画ですか。', 'prompt_en': 'Which day would be better for an outdoor plan based on the forecast?', 'type': 'application'},
        ],
    },
    'n5.listen.023': {
        'prompts': [
            {'prompt_ja': '水よう日は 学校が ありますか。', 'prompt_en': 'Does the speaker have school on Wednesday?', 'type': 'implication'},
        ],
    },
    'n5.listen.024': {
        'prompts': [
            {'prompt_ja': 'こん夜は どんな パーティーに なりますか。', 'prompt_en': 'What kind of gathering does this sound like — formal or casual?', 'type': 'inference'},
            {'prompt_ja': 'なぜ 父は おそく 来ますか。', 'prompt_en': 'Why might the father arrive later than the others?', 'type': 'inference'},
        ],
    },
    'n5.listen.025': {
        'prompts': [
            {'prompt_ja': '先生は どう こたえますか。', 'prompt_en': 'How does the teacher typically greet back?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.026': {
        'prompts': [
            {'prompt_ja': '店員は つぎに 何を 言いますか。', 'prompt_en': 'What does the cafe staff typically say next?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.027': {
        'prompts': [
            {'prompt_ja': '友だちは どう 反応しますか。', 'prompt_en': 'How might the friend respond to a polite refusal?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.028': {
        'prompts': [
            {'prompt_ja': 'いえの 人は つぎに 何を 言いますか。', 'prompt_en': 'What does the host typically say in reply?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.029': {
        'prompts': [
            {'prompt_ja': 'いっしょに 食べる 人は どう こたえますか。', 'prompt_en': 'What is the typical response from the others at the table?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.030': {
        'prompts': [
            {'prompt_ja': 'しらない 人は どう こたえますか。', 'prompt_en': 'How does a stranger typically respond to a polite direction-asking phrase?', 'type': 'next_utterance'},
            {'prompt_ja': 'どんな 答えを よういして おく べきですか。', 'prompt_en': 'What follow-up phrase should you prepare?', 'type': 'application'},
        ],
    },
}


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_inference_wave2')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {it['id']: it for it in data['items']}
    n = 0
    for lid, content in EXPANSIONS.items():
        it = by_id.get(lid)
        if not it:
            print(f'  ! missing: {lid}'); continue
        if it.get('inference_question_expansion'):
            print(f'  - skip: {lid}'); continue
        it['inference_question_expansion'] = content
        it['inference_question_expansion_provenance'] = 'llm_curated'
        n += 1
    print(f'\nWave 2 added inference on {n} more items.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
