"""ISSUE-057 (audit round-7, 2026-05-06): author 7 mondai-4 (即時応答)
listening items.

The official JLPT N5 chokai paper has 6 mondai-4 items. The app shipped
zero. This batch adds 7 items (one over the floor for variety).

Mondai 4 (即時応答) format:
  - Single-line stimulus (a question or prompt).
  - 3 short response options (NOT 4 — official format).
  - Pick the most natural reply.
  - Tests pragmatic + register awareness, not vocab.

Each item carries:
  format: 'utterance'    (matches existing FORMATS['utterance'] in listening.js)
  format_type: 'quick_response'  (closed-enum addition for JA-33)
  mondai: 4
  prompt_ja: 'もんだい4: いちばん いい へんじを えらんで ください'
  script_ja: <stimulus line>
  choices: [3 short replies]
  correctAnswer: <the natural one>
  explanation_en: <why this answer fits>
  review_status: 'llm_curated'
  audio: null (audio generated later by build_audio.py)

Idempotent: skips IDs already in catalog.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
LF = ROOT / 'data' / 'listening.json'

NEW_ITEMS = [
    {
        'id': 'n5.listen.041',
        'mondai': 4,
        'format': 'response',
        'format_type': 'immediate_response',
        'review_status': 'llm_curated',
        'title_ja': 'いえに かえります',
        'prompt_ja': 'もんだい4: いちばん いい へんじを えらんで ください。',
        'script_ja': 'おさきに しつれいします。',
        'choices': [
            'おつかれさまでした。',
            'はじめまして。',
            'ごちそうさまでした。',
        ],
        'correctAnswer': 'おつかれさまでした。',
        'explanation_en': "When a colleague says 'お先に失礼します' (leaving work first), the standard reply is 'お疲れさまでした' (you've worked hard). 'はじめまして' is a first-meeting greeting; 'ごちそうさまでした' is for after meals.",
    },
    {
        'id': 'n5.listen.042',
        'mondai': 4,
        'format': 'response',
        'format_type': 'immediate_response',
        'review_status': 'llm_curated',
        'title_ja': 'ありがとう',
        'prompt_ja': 'もんだい4: いちばん いい へんじを えらんで ください。',
        'script_ja': 'たんじょうび、おめでとうございます。',
        'choices': [
            'ありがとうございます。',
            'すみません。',
            'いただきます。',
        ],
        'correctAnswer': 'ありがとうございます。',
        'explanation_en': "Standard reply when someone congratulates you on your birthday: 'thank you'. 'すみません' apologises; 'いただきます' is said before eating.",
    },
    {
        'id': 'n5.listen.043',
        'mondai': 4,
        'format': 'response',
        'format_type': 'immediate_response',
        'review_status': 'llm_curated',
        'title_ja': 'みち を きく',
        'prompt_ja': 'もんだい4: いちばん いい へんじを えらんで ください。',
        'script_ja': 'すみません、えきは どこですか。',
        'choices': [
            'まっすぐ いって、みぎに まがって ください。',
            'えきは とおいです。',
            'きっぷは 二まいです。',
        ],
        'correctAnswer': 'まっすぐ いって、みぎに まがって ください。',
        'explanation_en': "When asked 'where is the station?' the natural reply is directions ('go straight then turn right'). The other options state distance or count tickets but don't answer 'where'.",
    },
    {
        'id': 'n5.listen.044',
        'mondai': 4,
        'format': 'response',
        'format_type': 'immediate_response',
        'review_status': 'llm_curated',
        'title_ja': 'いただきます',
        'prompt_ja': 'もんだい4: いちばん いい へんじを えらんで ください。',
        'script_ja': 'いっしょに ひるごはんを たべませんか。',
        'choices': [
            'いいですね、たべましょう。',
            'もう たべました。',
            'いってきます。',
        ],
        'correctAnswer': 'いいですね、たべましょう。',
        'explanation_en': "When invited 'won't you eat lunch with me?', the warm acceptance is 'sounds good, let's eat'. 'もう食べました' (already ate) is technically a refusal but more abrupt; 'いってきます' (I'm off) is wrong context entirely.",
    },
    {
        'id': 'n5.listen.045',
        'mondai': 4,
        'format': 'response',
        'format_type': 'immediate_response',
        'review_status': 'llm_curated',
        'title_ja': 'おはよう',
        'prompt_ja': 'もんだい4: いちばん いい へんじを えらんで ください。',
        'script_ja': 'おはようございます。',
        'choices': [
            'おはようございます。',
            'おやすみなさい。',
            'さようなら。',
        ],
        'correctAnswer': 'おはようございます。',
        'explanation_en': "Greeting echoes greeting: 'good morning' is met with 'good morning'. 'おやすみなさい' is good-night; 'さようなら' is goodbye.",
    },
    {
        'id': 'n5.listen.046',
        'mondai': 4,
        'format': 'response',
        'format_type': 'immediate_response',
        'review_status': 'llm_curated',
        'title_ja': 'きょうしつで',
        'prompt_ja': 'もんだい4: いちばん いい へんじを えらんで ください。',
        'script_ja': 'すみません、ペンを かして ください。',
        'choices': [
            'はい、どうぞ。',
            'はい、わかりました。',
            'いいえ、けっこうです。',
        ],
        'correctAnswer': 'はい、どうぞ。',
        'explanation_en': "When asked to lend a pen, the natural reply is 'yes, here you go' ('どうぞ' = please take it). 'わかりました' (understood) doesn't fit a request for an object; 'いいえ、けっこうです' (no thank you) refuses.",
    },
    {
        'id': 'n5.listen.047',
        'mondai': 4,
        'format': 'response',
        'format_type': 'immediate_response',
        'review_status': 'llm_curated',
        'title_ja': 'たすけて くれて',
        'prompt_ja': 'もんだい4: いちばん いい へんじを えらんで ください。',
        'script_ja': 'すみませんでした。',
        'choices': [
            'いいえ、だいじょうぶです。',
            'おねがいします。',
            'こちらこそ。',
        ],
        'correctAnswer': 'いいえ、だいじょうぶです。',
        'explanation_en': "When someone apologises 'sorry', the gracious reply is 'no, it's fine'. 'おねがいします' (please) is unrelated; 'こちらこそ' (likewise) fits 'thank you' contexts.",
    },
]


def main() -> int:
    data = json.loads(LF.read_text(encoding='utf-8'))
    items = data.get('items', [])
    existing = {it['id'] for it in items}
    n_added = 0
    for new_it in NEW_ITEMS:
        if new_it['id'] in existing:
            print(f'  skip {new_it["id"]} (exists)')
            continue
        items.append(new_it)
        n_added += 1
    data['items'] = items

    LF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Verify mondai distribution
    from collections import Counter
    md = Counter(it.get('mondai') for it in items)
    print(f'Added {n_added} mondai-4 items. Total listening items: {len(items)}.')
    print(f'mondai distribution: {dict(md)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
