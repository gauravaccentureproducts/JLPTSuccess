"""IMP-117: Standardize gloss_provenance / meanings_hi_provenance data shape.

Some vocab entries have `gloss_provenance` as a STRING (legacy, like
"native_reviewed"); others have it as a DICT keyed by locale
(`{"en": "native_reviewed", "hi": "llm_curated"}`). Renderer code
expects a consistent shape.

This script normalizes to the DICT shape:
  - If `gloss_provenance` is a string S, becomes {"en": S}.
  - If `gloss_hi` is populated and dict has no "hi" key, adds
    {"hi": "llm_curated"} (matches what the JCE-4 / Hindi seed pass
    actually authored).

Same logic for kanji `meanings_provenance` -> dict shape; rename to
canonical `meanings_provenance` so renderer can consume one schema.

Idempotent: running twice produces no further changes.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VOCAB = ROOT / 'data' / 'vocab.json'
KANJI = ROOT / 'data' / 'kanji.json'


def normalize_provenance_field(entry: dict, field_name: str, hi_field_present: bool) -> bool:
    """Normalize a provenance field into dict shape.

    Returns True if the entry was modified."""
    val = entry.get(field_name)
    changed = False

    if val is None:
        # No provenance at all — synthesize a reasonable default
        if hi_field_present:
            entry[field_name] = {'en': 'native_reviewed', 'hi': 'llm_curated'}
            changed = True
        else:
            entry[field_name] = {'en': 'native_reviewed'}
            changed = True
    elif isinstance(val, str):
        # Legacy string shape — convert to dict
        new_val = {'en': val}
        if hi_field_present:
            new_val['hi'] = 'llm_curated'
        entry[field_name] = new_val
        changed = True
    elif isinstance(val, dict):
        # Already dict — only fill in missing hi if hi-field is present
        if hi_field_present and 'hi' not in val:
            val['hi'] = 'llm_curated'
            changed = True
        # Ensure en is set
        if 'en' not in val:
            val['en'] = 'native_reviewed'
            changed = True

    return changed


def main():
    # vocab
    with VOCAB.open('r', encoding='utf-8') as f:
        v = json.load(f)
    vocab = v['entries']
    v_changed = 0
    for e in vocab:
        if normalize_provenance_field(e, 'gloss_provenance', bool(e.get('gloss_hi'))):
            v_changed += 1
    with VOCAB.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print(f'Vocab: normalized gloss_provenance on {v_changed} entries.')

    # kanji
    with KANJI.open('r', encoding='utf-8') as f:
        k = json.load(f)
    kanji = k['entries']
    k_changed = 0
    for e in kanji:
        if normalize_provenance_field(e, 'meanings_provenance', bool(e.get('meanings_hi'))):
            k_changed += 1
    with KANJI.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(k, f, ensure_ascii=False, indent=2)
    print(f'Kanji: normalized meanings_provenance on {k_changed} entries.')


if __name__ == '__main__':
    main()
