"""Wave 3 — finish listening inference_question_expansion (items 31-50).

After this, coverage 30/50 -> 50/50 (100%).
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EXPANSIONS = {
    'n5.listen.031': {
        'prompts': [
            {'prompt_ja': '女の人は 男の人に 何を おすすめしましたか。', 'prompt_en': 'Which gift did the woman recommend?', 'type': 'speaker_intent'},
            {'prompt_ja': '男の人は どうして 本に しませんでしたか。', 'prompt_en': 'Why did the man change his mind from book to hat?', 'type': 'inference'},
        ],
    },
    'n5.listen.032': {
        'prompts': [
            {'prompt_ja': '男の人は しゅうまつ どのくらい いそがしいですか。', 'prompt_en': 'How busy will the man\'s weekend be?', 'type': 'implication'},
        ],
    },
    'n5.listen.033': {
        'prompts': [
            {'prompt_ja': 'お きゃくは つぎに 何を しますか。', 'prompt_en': 'What does the guest probably do next?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.034': {
        'prompts': [
            {'prompt_ja': '子どもは つぎに 何を しますか。', 'prompt_en': 'What will the child do right after washing their face?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.035': {
        'prompts': [
            {'prompt_ja': 'クラスで 一ばん おおい こくせきは どこですか。', 'prompt_en': 'Which nationality has the largest count?', 'type': 'implication'},
            {'prompt_ja': 'のこりの 五人は どんな 人ですか。', 'prompt_en': 'How many students are unaccounted for in the breakdown?', 'type': 'application'},
        ],
    },
    'n5.listen.036': {
        'prompts': [
            {'prompt_ja': 'なぜ しんかんせんを えらびましたか。', 'prompt_en': 'Why might they choose Shinkansen over flight or bus?', 'type': 'inference'},
        ],
    },
    'n5.listen.037': {
        'prompts': [
            {'prompt_ja': 'きょう 大きい 本は いくらに なりますか。', 'prompt_en': 'Calculate today\'s price for the big book.', 'type': 'application'},
            {'prompt_ja': 'なぜ お きゃくは セールを えらびますか。', 'prompt_en': 'Why might customers wait for sale days?', 'type': 'inference'},
        ],
    },
    'n5.listen.038': {
        'prompts': [
            {'prompt_ja': 'いえの 人は どう こたえますか。', 'prompt_en': 'How does the host typically respond?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.039': {
        'prompts': [
            {'prompt_ja': '店員は どう こたえますか。', 'prompt_en': 'How does the restaurant staff typically respond?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.040': {
        'prompts': [
            {'prompt_ja': 'ともだちは どう こたえますか。', 'prompt_en': 'How does the friend typically respond to an evening greeting?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.041': {
        'prompts': [
            {'prompt_ja': 'のこって いる 人は 何と こたえますか。', 'prompt_en': 'How does the remaining person typically respond?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.042': {
        'prompts': [
            {'prompt_ja': 'たんじょうびの 人は つぎに 何を 言いますか。', 'prompt_en': 'How does the birthday person typically reply?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.043': {
        'prompts': [
            {'prompt_ja': 'みちを きかれた 人は つぎに 何を 言いますか。', 'prompt_en': 'How does the asked-for-directions person typically respond?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.044': {
        'prompts': [
            {'prompt_ja': 'さそわれた 人は どう こたえますか。', 'prompt_en': 'How does the invited person typically reply?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.045': {
        'prompts': [
            {'prompt_ja': 'あいさつされた 人は つぎに 何を 言いますか。', 'prompt_en': 'How does the greeted person reply?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.046': {
        'prompts': [
            {'prompt_ja': 'ペンを かりられた 人は どう こたえますか。', 'prompt_en': 'How does the asked person typically respond?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.047': {
        'prompts': [
            {'prompt_ja': 'あやまられた 人は どう こたえますか。', 'prompt_en': 'How does the apologized-to person typically respond?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.048': {
        'prompts': [
            {'prompt_ja': '女の人は つぎに 何を しますか。', 'prompt_en': 'What does the woman do next after agreeing to the walk?', 'type': 'next_utterance'},
        ],
    },
    'n5.listen.049': {
        'prompts': [
            {'prompt_ja': 'みちを きかれた 人の こたえに、どんな ことばが ふくまれて いますか。', 'prompt_en': 'What kind of language markers (fillers / hesitations) appear in the response?', 'type': 'implication'},
        ],
    },
    'n5.listen.050': {
        'prompts': [
            {'prompt_ja': 'いしゃは つぎに 何を しますか。', 'prompt_en': 'What does the doctor do next after deciding to give medicine?', 'type': 'next_utterance'},
            {'prompt_ja': 'かんじゃは どんな びょうきだと おもいますか。', 'prompt_en': 'What illness does the patient likely have?', 'type': 'inference'},
        ],
    },
}


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_inference_wave3')
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
    print(f'\nWave 3 added inference on {n} more items.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
