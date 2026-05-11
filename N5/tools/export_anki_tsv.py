"""Export vocab / grammar / kanji corpora to Anki-compatible TSV.

P4 #30 (audit competitor-feature parity): Migaku / Anki users want
to seed their personal decks with the N5 corpus. This script
produces three TSV files (tab-separated values, no surrounding
quotes) that Anki imports directly via File > Import.

Output files (written to dist/anki/):
  n5_vocab.tsv    — N5 vocabulary deck
  n5_grammar.tsv  — N5 grammar pattern deck
  n5_kanji.tsv    — N5 kanji deck

Field layouts (all stable for Anki note-type binding):

  vocab.tsv columns:
    form  reading  gloss_en  gloss_hi  pos  section  example_ja
    example_en  audio_path  vocab_id

  grammar.tsv columns:
    pattern_id  pattern_ja  meaning_en  example_ja  example_en
    common_mistake_ja  common_mistake_en  cultural_callout

  kanji.tsv columns:
    glyph  on_yomi  kun_yomi  meaning_en  meaning_hi  stroke_count
    radical  mnemonic_summary  mnemonic_visual  mnemonic_reading
    etymology_origin  etymology_story

Idempotent. Re-running rewrites the TSVs. Output is plain UTF-8
without BOM (Anki's preferred encoding).

Run:  python tools/export_anki_tsv.py
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def tsv_clean(s) -> str:
    """Strip tab + newline characters; collapse whitespace."""
    if s is None:
        return ''
    if not isinstance(s, str):
        s = str(s)
    return s.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ').strip()


def export_vocab(out_dir: Path) -> int:
    fp = ROOT / 'data' / 'vocab.json'
    data = json.loads(fp.read_text(encoding='utf-8'))['entries']
    cols = ['form', 'reading', 'gloss_en', 'gloss_hi', 'pos', 'section',
            'example_ja', 'example_en', 'audio_path', 'vocab_id']
    lines = ['\t'.join(cols)]
    for e in data:
        exs = e.get('examples') or []
        first_ex = exs[0] if exs else {}
        row = [
            tsv_clean(e.get('form')),
            tsv_clean(e.get('reading')),
            tsv_clean(e.get('gloss')),
            tsv_clean(e.get('gloss_hi')),
            tsv_clean(e.get('pos')),
            tsv_clean(e.get('section')),
            tsv_clean(first_ex.get('ja')),
            tsv_clean(first_ex.get('translation_en')),
            '',  # audio_path placeholder (vocab audio is currently TTS-on-demand, no static file path)
            tsv_clean(e.get('id')),
        ]
        lines.append('\t'.join(row))
    (out_dir / 'n5_vocab.tsv').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return len(data)


def export_grammar(out_dir: Path) -> int:
    fp = ROOT / 'data' / 'grammar.json'
    data = json.loads(fp.read_text(encoding='utf-8'))['patterns']
    cols = ['pattern_id', 'pattern_ja', 'meaning_en', 'example_ja',
            'example_en', 'common_mistake_ja', 'common_mistake_en',
            'cultural_callout']
    lines = ['\t'.join(cols)]
    for p in data:
        exs = p.get('examples') or []
        first_ex = exs[0] if exs else {}
        mistakes = p.get('common_mistakes') or []
        first_m = mistakes[0] if mistakes else {}
        callout = (p.get('cultural_callout') or {}).get('note', '')
        row = [
            tsv_clean(p.get('id')),
            tsv_clean(p.get('pattern_ja') or p.get('title_ja')),
            tsv_clean(p.get('meaning_en') or p.get('summary')),
            tsv_clean(first_ex.get('ja')),
            tsv_clean(first_ex.get('translation_en') or first_ex.get('translation')),
            tsv_clean(first_m.get('wrong') or first_m.get('ja') if isinstance(first_m, dict) else first_m),
            tsv_clean(first_m.get('why') or first_m.get('en') if isinstance(first_m, dict) else ''),
            tsv_clean(callout),
        ]
        lines.append('\t'.join(row))
    (out_dir / 'n5_grammar.tsv').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return len(data)


def export_kanji(out_dir: Path) -> int:
    fp = ROOT / 'data' / 'kanji.json'
    raw = json.loads(fp.read_text(encoding='utf-8'))
    entries = raw.get('entries', raw) if isinstance(raw, dict) else raw
    if isinstance(entries, dict):
        entries = list(entries.values())
    cols = ['glyph', 'on_yomi', 'kun_yomi', 'meaning_en', 'meaning_hi',
            'stroke_count', 'radical', 'mnemonic_summary', 'mnemonic_visual',
            'mnemonic_reading', 'etymology_origin', 'etymology_story']
    lines = ['\t'.join(cols)]
    for e in entries:
        mn = e.get('mnemonic') or {}
        etym = e.get('etymology') or {}
        rad = e.get('radical') or {}
        rad_str = rad.get('glyph', '') if isinstance(rad, dict) else str(rad)
        row = [
            tsv_clean(e.get('glyph')),
            tsv_clean(', '.join(e.get('on') or [])),
            tsv_clean(', '.join(e.get('kun') or [])),
            tsv_clean(', '.join(e.get('meanings') or [])),
            tsv_clean(', '.join(e.get('meanings_hi') or [])),
            tsv_clean(e.get('stroke_count')),
            tsv_clean(rad_str),
            tsv_clean(mn.get('summary')),
            tsv_clean(mn.get('visual')),
            tsv_clean(mn.get('reading')),
            tsv_clean(etym.get('origin_type')),
            tsv_clean(etym.get('story')),
        ]
        lines.append('\t'.join(row))
    (out_dir / 'n5_kanji.tsv').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return len(entries)


def main() -> int:
    out_dir = ROOT / 'dist' / 'anki'
    out_dir.mkdir(parents=True, exist_ok=True)

    n_vocab = export_vocab(out_dir)
    n_grammar = export_grammar(out_dir)
    n_kanji = export_kanji(out_dir)

    print(f'Exported to {out_dir.relative_to(ROOT)}:')
    print(f'  n5_vocab.tsv   ({n_vocab} entries)')
    print(f'  n5_grammar.tsv ({n_grammar} patterns)')
    print(f'  n5_kanji.tsv   ({n_kanji} kanji)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
