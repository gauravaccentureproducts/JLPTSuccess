"""Build bidirectional cross-links between data/authentic.json
cards and data/vocab.json entries.

Audit context: the 2026-05-09 richness audit's biggest single gap
was the authentic-content layer (0% cross-linking from grammar /
vocab / kanji / reading / listening to authentic cards). The
/authentic route exists with 100 real-world Japanese cards across
9 categories (hospital / menu / transit / signs / notice /
shop / post / time / weather), but none was reachable from the
corpus entries.

This pass authors:
  - On each matched vocab entry: `authentic_refs: ["auth.X.Y", ...]`
  - On each authentic card: `vocab_refs: ["n5.vocab.X.Y", ...]`

Matching strategy (multi-pass, deterministic):
  1. Exact-match card.ja or card.reading against vocab.form OR
     vocab.reading.
  2. Tokenize card.ja by whitespace + punctuation. For each token:
     a. Direct match.
     b. Strip trailing particle (を/は/が/に/で/と/も/の/へ/や/か/ね/
        よ/まで/から).
     c. Strip leading お- politeness prefix; re-match.
  3. Match all hits; dedupe.

Skip tokens that ARE particles (the bare particle itself).
Multi-word phrases produce multiple links (head noun + secondary
content nouns).
"""
from __future__ import annotations
import io, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PARTICLES = ('を', 'は', 'が', 'に', 'で', 'と', 'も', 'の', 'へ', 'や', 'か', 'ね', 'よ', 'まで', 'から')


def strip_particles(t: str) -> str:
    for p in sorted(PARTICLES, key=lambda x: -len(x)):
        if t.endswith(p) and len(t) > len(p):
            return t[:-len(p)]
    return t


def strip_o_prefix(t: str) -> str | None:
    if t.startswith('お') and len(t) > 1:
        return t[1:]
    return None


def tokenize(s: str) -> list[str]:
    s = re.sub(r'[、。！？]+', ' ', s)
    return [t for t in re.split(r'\s+', s.strip()) if t]


def main() -> int:
    auth_fp = ROOT / 'data' / 'authentic.json'
    vocab_fp = ROOT / 'data' / 'vocab.json'

    auth_bak = auth_fp.with_suffix('.json.bak_2026_05_11_authentic_refs')
    vocab_bak = vocab_fp.with_suffix('.json.bak_2026_05_11_authentic_refs')
    if not auth_bak.exists():
        shutil.copy2(auth_fp, auth_bak)
        print(f'Backup: {auth_bak.name}')
    if not vocab_bak.exists():
        shutil.copy2(vocab_fp, vocab_bak)
        print(f'Backup: {vocab_bak.name}')

    auth_data = json.loads(auth_fp.read_text(encoding='utf-8'))
    vocab_data = json.loads(vocab_fp.read_text(encoding='utf-8'))

    # Build exact-form lookup
    by_exact: dict[str, str] = {}
    for e in vocab_data['entries']:
        for fld in ('form', 'reading'):
            s = e.get(fld) or ''
            if s and s not in by_exact:
                by_exact[s] = e['id']

    # Build vocab-by-id for back-link writes
    vocab_by_id = {e['id']: e for e in vocab_data['entries']}

    card_to_vocab: dict[str, list[str]] = {}
    for card in auth_data['items']:
        mids: list[str] = []
        # Strategy 1 - exact match
        for s in (card.get('ja'), card.get('reading')):
            if s and s in by_exact:
                eid = by_exact[s]
                if eid not in mids:
                    mids.append(eid)
        # Strategy 2 - per-token with particle/prefix stripping
        for tok in tokenize(card.get('ja') or '') + tokenize(card.get('reading') or ''):
            if tok in PARTICLES:
                continue
            for variant in (tok, strip_particles(tok)):
                if variant and variant in by_exact:
                    eid = by_exact[variant]
                    if eid not in mids:
                        mids.append(eid)
            stripped = strip_o_prefix(strip_particles(tok))
            if stripped and stripped in by_exact:
                eid = by_exact[stripped]
                if eid not in mids:
                    mids.append(eid)
        if mids:
            card_to_vocab[card['id']] = mids

    print(f'\nCards with >=1 vocab match: {len(card_to_vocab)}/{len(auth_data["items"])}')

    # Write back-links on cards (vocab_refs) and on vocab entries (authentic_refs).
    n_cards_written = 0
    n_vocab_written = 0
    for card in auth_data['items']:
        cid = card['id']
        if cid not in card_to_vocab:
            continue
        vocab_refs = card.get('vocab_refs') or []
        new = [v for v in card_to_vocab[cid] if v not in vocab_refs]
        if new:
            card['vocab_refs'] = vocab_refs + new
            card['vocab_refs_provenance'] = 'auto_derived'
            n_cards_written += 1
        for vid in card_to_vocab[cid]:
            ve = vocab_by_id.get(vid)
            if not ve:
                continue
            arefs = ve.get('authentic_refs') or []
            if cid not in arefs:
                ve['authentic_refs'] = arefs + [cid]
                ve['authentic_refs_provenance'] = 'auto_derived'
                n_vocab_written += 1

    auth_fp.write_text(json.dumps(auth_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    vocab_fp.write_text(json.dumps(vocab_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'Cards updated with vocab_refs:    {n_cards_written}')
    print(f'Vocab entries with authentic_refs added: {n_vocab_written}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
