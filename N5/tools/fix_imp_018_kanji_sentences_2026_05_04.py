"""IMP-018: add example sentences to each of the 106 N5 kanji entries.

Strategy: scan data/grammar.json examples (each is a short, N5-whitelisted
sentence with ja + translation_en). For each kanji glyph, pick up to 2
distinct sentences whose `ja` field contains the glyph. The shortest
matching examples are preferred (most beginner-friendly).

If no grammar example contains a kanji, fall back to scanning
data/reading.json passages and synthesise a 1-clause excerpt around the
glyph (clean cut at sentence punctuation 。/、 boundaries).

If still no match, leave the entry's `sentences` field absent — a separate
audit invariant can flag the gap. (Empirically all 106 N5 kanji appear in
the grammar/reading corpora; the fallback is defensive.)

Idempotent: skips entries that already have a `sentences` field.
"""
from __future__ import annotations
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KANJI_JSON = ROOT / 'data' / 'kanji.json'
GRAMMAR_JSON = ROOT / 'data' / 'grammar.json'
READING_JSON = ROOT / 'data' / 'reading.json'
LISTENING_JSON = ROOT / 'data' / 'listening.json'
PAPERS_DIR = ROOT / 'data' / 'papers'

# Hand-authored sentences for the 8 kanji that don't naturally appear in
# any of the corpus sources (typically isolated body-parts, large numerals,
# or directional kanji that aren't woven into N5 passages). Each uses only
# N5-whitelist kanji + the target glyph.
HAND_AUTHORED = {
    '万': [{'ja': '五万円 あります。', 'translation_en': 'I have 50,000 yen.'}],
    '足': [{'ja': '足が いたいです。', 'translation_en': 'My foot hurts.'}],
    '目': [{'ja': '目が きれいです。', 'translation_en': 'Her eyes are beautiful.'}],
    '力': [{'ja': '力を かして ください。', 'translation_en': 'Please lend me your strength.'}],
    '西': [{'ja': '学校は 西に あります。', 'translation_en': 'The school is to the west.'}],
    '南': [{'ja': '南の くにに 行きました。', 'translation_en': 'I went to a southern country.'}],
    '空': [{'ja': '空が 青いです。', 'translation_en': 'The sky is blue.'}],
    '号': [{'ja': '一号せんに のります。', 'translation_en': 'I take line 1.'}],
}

MAX_SENTENCES_PER_KANJI = 2
SENTENCE_MIN_LEN = 5      # too-short matches are useless
SENTENCE_MAX_LEN = 80     # widened from 60 — some passages have a single
                          # 70-char sentence containing the kanji


def find_grammar_sentences(glyph: str, examples: list, taken: set) -> list:
    """Return up to MAX matching {ja, translation_en} from grammar examples,
    sorted shortest-first, deduplicated against `taken`."""
    candidates = []
    for ex in examples:
        ja = ex.get('ja', '') or ''
        en = ex.get('translation_en', '') or ex.get('en', '') or ''
        if glyph not in ja:
            continue
        if not (SENTENCE_MIN_LEN <= len(ja) <= SENTENCE_MAX_LEN):
            continue
        if ja in taken:
            continue
        candidates.append({'ja': ja, 'translation_en': en})
    candidates.sort(key=lambda c: len(c['ja']))
    return candidates[:MAX_SENTENCES_PER_KANJI]


def _split_sentences(ja: str) -> list[str]:
    """Split Japanese text on 。！？ keeping the ender as part of each piece."""
    chunks = re.split(r'([。！？])', ja)
    merged = []
    for i in range(0, len(chunks) - 1, 2):
        piece = chunks[i].strip() + chunks[i + 1]
        if piece:
            merged.append(piece)
    if len(chunks) % 2 == 1 and chunks[-1].strip():
        merged.append(chunks[-1].strip())
    return merged


def find_text_sentences(glyph: str, texts: list[str], taken: set) -> list:
    """Generic: cut sentences containing the glyph from any list of JA strings."""
    found = []
    for txt in texts:
        if not txt or glyph not in txt:
            continue
        for s in _split_sentences(txt):
            # Strip leading dialogue markers like "男：" / "女：" / "店員：".
            s_clean = re.sub(r'^[一-鿿ぁ-んァ-ンA-Za-z]{1,3}：', '', s).strip()
            if (glyph in s_clean
                    and SENTENCE_MIN_LEN <= len(s_clean) <= SENTENCE_MAX_LEN
                    and s_clean not in taken):
                found.append({'ja': s_clean, 'translation_en': ''})
            if len(found) >= MAX_SENTENCES_PER_KANJI:
                return found
    return found


def find_reading_sentences(glyph: str, passages: list, taken: set) -> list:
    return find_text_sentences(
        glyph, [p.get('ja', '') for p in passages], taken,
    )


def find_listening_sentences(glyph: str, items: list, taken: set) -> list:
    return find_text_sentences(
        glyph, [it.get('script_ja', '') for it in items], taken,
    )


def find_paper_sentences(glyph: str, taken: set) -> list:
    """Last-resort: scan paper-JSON stems and passages."""
    texts = []
    for f in PAPERS_DIR.rglob('paper-*.json'):
        d = json.loads(f.read_text(encoding='utf-8'))
        for q in d.get('questions', []):
            for fld in ('stem_html', 'passage_text'):
                v = q.get(fld, '') or ''
                if v:
                    # Strip "A:" / "B:" prefixes used in goi paraphrase items.
                    v = re.sub(r'^A:\s*', '', v)
                    texts.append(v)
    return find_text_sentences(glyph, texts, taken)


def main() -> int:
    kanji_data = json.loads(KANJI_JSON.read_text(encoding='utf-8'))
    grammar = json.loads(GRAMMAR_JSON.read_text(encoding='utf-8'))
    reading = json.loads(READING_JSON.read_text(encoding='utf-8'))
    listening = json.loads(LISTENING_JSON.read_text(encoding='utf-8'))

    all_grammar_examples = [
        ex for p in grammar.get('patterns', []) for ex in p.get('examples', [])
    ]
    all_passages = reading.get('passages', [])
    all_listen = listening.get('items', [])

    # Track sentences already attached to a kanji, so we don't reuse the
    # same example across multiple kanji entries.
    used_sentences: set[str] = set()

    n_added = 0
    n_from_grammar = 0
    n_from_reading = 0
    n_from_listening = 0
    n_from_papers = 0
    n_total_unmatched = 0
    for entry in kanji_data['entries']:
        if 'sentences' in entry:
            # Already populated; skip (idempotent).
            continue
        glyph = entry['glyph']

        # Try sources in priority order: grammar (cleanest, has translations)
        # → reading → listening → paper-JSONs → hand-authored fallback.
        sents = find_grammar_sentences(glyph, all_grammar_examples, used_sentences)
        if sents:
            n_from_grammar += 1
        if not sents:
            sents = find_reading_sentences(glyph, all_passages, used_sentences)
            if sents: n_from_reading += 1
        if not sents:
            sents = find_listening_sentences(glyph, all_listen, used_sentences)
            if sents: n_from_listening += 1
        if not sents:
            sents = find_paper_sentences(glyph, used_sentences)
            if sents: n_from_papers += 1
        if not sents and glyph in HAND_AUTHORED:
            sents = HAND_AUTHORED[glyph]

        if not sents:
            n_total_unmatched += 1
            continue

        entry['sentences'] = sents
        for s in sents:
            used_sentences.add(s['ja'])
        n_added += 1

    if n_added == 0:
        print('No changes (all entries already have sentences).')
        return 0

    KANJI_JSON.write_text(
        json.dumps(kanji_data, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'Sentences added on {n_added}/{len(kanji_data["entries"])} kanji entries.')
    print(f'  by source: grammar={n_from_grammar}, reading={n_from_reading}, '
          f'listening={n_from_listening}, papers={n_from_papers}')
    if n_total_unmatched:
        print(f'  {n_total_unmatched} entries had NO match in any corpus (left unset)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
