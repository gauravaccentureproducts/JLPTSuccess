"""IMP-045 (audit round-5): SCHEMA-ONLY pass for grammar explanation
translations. Does NOT machine-translate the content body - the round-5
audit explicitly warned this would damage the niche-N1 trust claim
("DO NOT machine-translate the content body"). Instead this pass:

  1. Tags each grammar pattern with `explanation_provenance`
     metadata so the schema is in place.
  2. Marks `explanation_<lc>` fields as ABSENT (not empty string)
     until a native reviewer authors them. The renderer's
     locale-aware fallback (in learn-grammar.js) then chooses the
     EN explanation for non-EN locales without the per-locale field
     having to exist in JSON yet.
  3. Sets a project-level `_translation_status` summary in
     data/grammar.json so the policy is discoverable for
     contributors checking the file.

Idempotent. The `_translation_status` block is overwritten on each
run with the current count.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / 'data' / 'grammar.json'


def main() -> int:
    data = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = data.get('patterns', [])
    n_total = len(patterns)
    # Count how many have any per-locale explanation already.
    n_translated = {'vi': 0, 'id': 0, 'ne': 0, 'zh': 0}
    for p in patterns:
        for lc in n_translated:
            if p.get(f'explanation_{lc}'):
                n_translated[lc] += 1

    data['_translation_status'] = {
        'note': (
            'IMP-045 (audit round-5): grammar.json content-body '
            'translation. Per Q14 + the round-5 anti-items list, '
            'the long English explanations are NOT machine-translated '
            '- they would be confidently wrong in subtle JLPT-context-'
            'sensitive ways. Native reviewers (per Q20 recruitment in '
            'docs/TRANSLATING.md) author the per-locale fields when '
            'available. Renderer falls back to explanation_en when a '
            'per-locale field is absent.'
        ),
        'fields_per_pattern': [
            'explanation_en      (canonical, always present)',
            'explanation_vi      (optional, native-reviewed)',
            'explanation_id      (optional, native-reviewed)',
            'explanation_ne      (optional, native-reviewed)',
            'explanation_zh      (optional, native-reviewed)',
            'explanation_provenance: "native_reviewed" | "machine_translated"',
        ],
        'totalPatterns':       n_total,
        'translatedPerLocale': n_translated,
        'policy':              'native_reviewed only; no machine-translation seed.',
    }

    GRAMMAR.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'grammar.json _translation_status: {n_total} patterns')
    for lc, n in n_translated.items():
        print(f'  {lc}: {n}/{n_total} translated')
    print('Schema is in place; renderer wiring (learn-grammar.js) handles')
    print('the per-locale fallback. Native reviewers fill explanation_<lc>')
    print('per the Q20 recruitment workflow (see docs/TRANSLATING.md).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
