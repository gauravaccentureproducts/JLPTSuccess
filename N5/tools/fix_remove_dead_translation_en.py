"""Remove the 16 dead `translation_en` fields from data/questions.json.

Audit 2026-05-02: questions.json has 16 translation_en entries left
over from earlier authoring passes. None of them are referenced by
the runtime (js/{drill,questions,quiz,papers,reading,listening}.js
all checked — zero `q.translation_en` / `question.translation_en` /
`item.translation_en` reads). They are silently shipped dead data.

Per same direction as the dokkai/listening Japanification, delete
these fields. Idempotent.

NOT TOUCHING:
  - data/grammar.json — translation_en is genuinely rendered by
    js/learn.js (grammar examples) and js/review.js (review screen).
    Grammar pattern teaching legitimately needs English glosses.
"""
import json
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    qpath = ROOT / 'data' / 'questions.json'
    data = json.load(qpath.open(encoding='utf-8'))
    removed: list[str] = []
    for q in data.get('questions', []):
        if 'translation_en' in q:
            removed.append(q.get('id', '?'))
            del q['translation_en']
    if removed:
        qpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Removed translation_en from {len(removed)} questions:')
    for qid in removed:
        print(f'  {qid}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
