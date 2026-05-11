"""Build bidirectional cross-links between data/authentic.json
cards and data/grammar.json patterns.

Fourth (and last) direction of the authentic-content layer
back-link. Vocab <-> authentic, kanji <-> authentic, and reading
<-> authentic were done in earlier passes. This pass closes the
grammar <-> authentic direction.

Approach: NOT pure-data. The match is SEMANTIC — for each
multi-token authentic card, manually identify which N5 grammar
pattern(s) the card exemplifies. The 100-card corpus has about
35 multi-token cards (with grammar to map) and 65 single-noun
cards (no grammar to map). The mapping below covers the cards
where the pattern is unambiguous and pedagogically valuable.

For each matched pair:
  - On the card:    grammar_refs: ["n5-XXX", ...]
  - On the pattern: authentic_refs: ["auth.X.Y", ...]

Provenance: llm_curated (semantic mapping, not derived).
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Curated mapping: card_id -> list of grammar pattern ids it exemplifies.
# Only includes cards where the pattern is unambiguous and useful.
CARD_TO_PATTERNS = {
    # Hospital
    'auth.hospital.netsu':           ['n5-003', 'n5-090'],     # が + あります
    # Menu
    'auth.menu.gohan-okawari':       ['n5-188'],               # ことができます
    'auth.menu.honjitsu':            ['n5-028'],               # の attribution
    'auth.menu.mizu':                ['n5-071'],               # てください family (noun-form request)
    # Notice
    'auth.notice.shashin-kinshi':    ['n5-077'],               # ないでください
    # Shop
    'auth.shop.cardmoii':            ['n5-079'],               # i-adj + です (いい→いい+です)
    'auth.shop.fukuro':              ['n5-023'],               # か question
    'auth.shop.jikan':               ['n5-021'],               # から〜まで range
    'auth.shop.teikyubi':            ['n5-001', 'n5-002'],     # です + は
    # Transit
    'auth.transit.densha-okurete':   ['n5-072'],               # Verb-ています
    'auth.transit.doa-shimari':      ['n5-003'],               # が subject
    'auth.transit.te-wo-haisaku':    ['n5-071'],               # Verb-てください
    'auth.transit.tsugi':            ['n5-001', 'n5-002'],     # です + は
    'auth.transit.tsugino-eki':      ['n5-028', 'n5-002'],     # の + は
    # Weather
    'auth.weather.ame':              [],                        # single noun, no grammar
    # Signs - many are noun + きんし (no specific pattern)
    'auth.signs.deguchi':            [],                        # 出口 noun
    'auth.signs.iriguchi':           [],                        # 入口 noun
}


def main() -> int:
    auth_fp = ROOT / 'data' / 'authentic.json'
    grammar_fp = ROOT / 'data' / 'grammar.json'

    auth_bak = auth_fp.with_suffix('.json.bak_2026_05_11_authentic_grammar')
    grammar_bak = grammar_fp.with_suffix('.json.bak_2026_05_11_authentic_grammar')
    if not auth_bak.exists():
        shutil.copy2(auth_fp, auth_bak)
        print(f'Backup: {auth_bak.name}')
    if not grammar_bak.exists():
        shutil.copy2(grammar_fp, grammar_bak)
        print(f'Backup: {grammar_bak.name}')

    auth_data = json.loads(auth_fp.read_text(encoding='utf-8'))
    grammar_data = json.loads(grammar_fp.read_text(encoding='utf-8'))

    by_card = {c['id']: c for c in auth_data['items']}
    by_pattern = {p['id']: p for p in grammar_data['patterns']}

    cards_written = 0
    patterns_written = 0

    for cid, pat_ids in CARD_TO_PATTERNS.items():
        if cid not in by_card:
            print(f'  ! card not found: {cid}')
            continue
        if not pat_ids:
            continue
        card = by_card[cid]

        # Write on the card
        existing = card.get('grammar_refs') or []
        new = [p for p in pat_ids if p not in existing and p in by_pattern]
        if new:
            card['grammar_refs'] = existing + new
            card['grammar_refs_provenance'] = 'llm_curated'
            cards_written += 1
            print(f'  + card {cid}: {new}')

        # Write on each pattern
        for pid in pat_ids:
            pat = by_pattern.get(pid)
            if not pat:
                print(f'    ! pattern not found: {pid}')
                continue
            arefs = pat.get('authentic_refs') or []
            if cid not in arefs:
                pat['authentic_refs'] = arefs + [cid]
                pat['authentic_refs_provenance'] = 'llm_curated'
                patterns_written += 1

    auth_fp.write_text(json.dumps(auth_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    grammar_fp.write_text(json.dumps(grammar_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'\nCards updated with grammar_refs:    {cards_written}')
    print(f'Patterns with authentic_refs added: {patterns_written}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
