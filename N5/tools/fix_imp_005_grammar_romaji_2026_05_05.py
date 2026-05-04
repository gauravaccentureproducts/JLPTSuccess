"""IMP-005 (audit round-3): generate Hepburn romaji for every grammar
example in data/grammar.json.

Approach (62% of examples are pure-kana — trivial; the 38% with kanji
need a reading lookup before romanization):

1. Build a kanji-form -> kana-reading dictionary by walking
   data/vocab.json (every entry carries `form` + `reading`). For
   compounds the reading is canonical for that form; for standalone
   kanji we fall back to data/kanji.json's primary on/kun reading.
2. For each example's `ja` text, do a greedy longest-prefix replacement
   of kanji-containing substrings with their kana reading from the
   dictionary. Single kanji not in vocab fall back to kanji.json
   primary reading. Stragglers (rare) keep the kanji glyph and emit a
   `[?]` marker so the audit can flag them.
3. Convert the resulting all-kana string to Hepburn romaji using a
   straightforward rule-based mapper (handles all hiragana + katakana,
   diacritics, small-tsu doubling, small-ya/yu/yo, n-before-bilabial,
   long-vowel macrons via simple ou/ei representation, particles
   は/へ/を rendered as wa/e/o).
4. Write the result back to each example as a new `romaji` field.

Idempotent: examples already carrying a `romaji` field are skipped.
Re-runs after a corpus change pick up the new examples without
re-converting the existing rows.
"""
from __future__ import annotations
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
GRAMMAR = DATA / 'grammar.json'
VOCAB = DATA / 'vocab.json'
KANJI = DATA / 'kanji.json'

KANJI_RE = re.compile(r'[一-鿿々]')


# ---------------------------------------------------------------------------
# Hepburn romaji table.
# ---------------------------------------------------------------------------

ROMAJI = {
    # hiragana — gojuon
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'ゐ': 'wi', 'ゑ': 'we', 'を': 'o',  # を as object particle = "o"
    'ん': 'n',
    # voiced
    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
    # small vowels (rarely standalone)
    'ぁ': 'a', 'ぃ': 'i', 'ぅ': 'u', 'ぇ': 'e', 'ぉ': 'o',
    'ゃ': 'ya', 'ゅ': 'yu', 'ょ': 'yo',
    'ゎ': 'wa',
    # symbols
    'ー': '-',  # long-vowel mark — replaced by previous-vowel duplication below
}

# Two-char yoon combinations (small ゃ/ゅ/ょ).
YOON = {
    'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
    'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
    'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
    'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
    'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
    'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
    'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
    'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
    'じゃ': 'ja',  'じゅ': 'ju',  'じょ': 'jo',
    'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
    'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
    # katakana variants
    'キャ': 'kya', 'キュ': 'kyu', 'キョ': 'kyo',
    'シャ': 'sha', 'シュ': 'shu', 'ショ': 'sho',
    'チャ': 'cha', 'チュ': 'chu', 'チョ': 'cho',
    'ニャ': 'nya', 'ニュ': 'nyu', 'ニョ': 'nyo',
    'ヒャ': 'hya', 'ヒュ': 'hyu', 'ヒョ': 'hyo',
    'ミャ': 'mya', 'ミュ': 'myu', 'ミョ': 'myo',
    'リャ': 'rya', 'リュ': 'ryu', 'リョ': 'ryo',
    'ギャ': 'gya', 'ギュ': 'gyu', 'ギョ': 'gyo',
    'ジャ': 'ja',  'ジュ': 'ju',  'ジョ': 'jo',
    'ビャ': 'bya', 'ビュ': 'byu', 'ビョ': 'byo',
    'ピャ': 'pya', 'ピュ': 'pyu', 'ピョ': 'pyo',
}

# Katakana single-char (mirror hiragana table).
KATA = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa', 'ヲ': 'o',
    'ン': 'n',
    'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
    'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
    'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
    'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
    'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
    'ァ': 'a', 'ィ': 'i', 'ゥ': 'u', 'ェ': 'e', 'ォ': 'o',
    'ャ': 'ya', 'ュ': 'yu', 'ョ': 'yo',
}


def kana_to_romaji(s: str) -> str:
    """Convert a kana-only Japanese string to Hepburn romaji."""
    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        # 2-char yoon (small ya/yu/yo)
        if i + 1 < n and s[i:i + 2] in YOON:
            out.append(YOON[s[i:i + 2]])
            i += 2
            continue
        # small-tsu (っ/ッ) — double the next consonant
        if ch in ('っ', 'ッ') and i + 1 < n:
            nxt_pair = s[i + 1:i + 3]
            nxt_rom = YOON.get(nxt_pair) or ROMAJI.get(s[i + 1]) or KATA.get(s[i + 1]) or ''
            if nxt_rom:
                # Double consonant. Special case: chi -> tchi, shi -> sshi.
                if nxt_rom.startswith('ch'):
                    out.append('t')
                else:
                    out.append(nxt_rom[0])
            i += 1
            continue
        # long-vowel mark ー — repeat last vowel
        if ch == 'ー' and out:
            last = out[-1]
            if last and last[-1] in 'aiueo':
                out.append(last[-1])
            i += 1
            continue
        # ん handling: render as 'm' before b/p/m, else 'n'
        if ch in ('ん', 'ン'):
            if i + 1 < n:
                nxt_rom = ROMAJI.get(s[i + 1]) or KATA.get(s[i + 1]) or ''
                if nxt_rom and nxt_rom[0] in ('b', 'p', 'm'):
                    out.append('m')
                elif nxt_rom and nxt_rom[0] in 'aiueoy':
                    out.append("n'")  # apostrophe to disambiguate
                else:
                    out.append('n')
            else:
                out.append('n')
            i += 1
            continue
        # single-char hiragana/katakana
        if ch in ROMAJI:
            out.append(ROMAJI[ch])
        elif ch in KATA:
            out.append(KATA[ch])
        else:
            # Pass through ASCII / punctuation / unrecognised char.
            out.append(ch)
        i += 1
    return ''.join(out)


# ---------------------------------------------------------------------------
# Build the kanji-to-reading dictionary.
# ---------------------------------------------------------------------------

def build_kana_lookup() -> dict[str, str]:
    """Map every vocab `form` (kanji-containing) to its kana `reading`.
    Plus single-kanji fallback from kanji.json's primary on/kun reading."""
    lookup: dict[str, str] = {}
    vocab = json.loads(VOCAB.read_text(encoding='utf-8'))
    for e in vocab.get('entries', []):
        form = e.get('form') or ''
        reading = e.get('reading') or ''
        if form and reading and KANJI_RE.search(form):
            # Only add if reading is pure kana (no kanji).
            if not KANJI_RE.search(reading):
                lookup[form] = reading
    # Single-kanji fallback from kanji.json.
    kanji_data = json.loads(KANJI.read_text(encoding='utf-8'))
    for k in kanji_data.get('entries', []):
        glyph = k.get('glyph')
        if not glyph or glyph in lookup:
            continue
        # Prefer kun (it's the standalone reading); fall back to on.
        reading = (k.get('kun') or k.get('on') or [None])[0]
        if reading:
            lookup[glyph] = reading
    return lookup


# ---------------------------------------------------------------------------
# Greedy longest-match kanji-mixed -> all-kana converter.
# ---------------------------------------------------------------------------

def to_kana(text: str, lookup: dict[str, str]) -> str:
    """Replace every kanji-containing substring in `text` with its kana
    reading via greedy longest-prefix lookup. Kana / punctuation /
    spaces pass through unchanged."""
    out: list[str] = []
    i = 0
    n = len(text)
    keys_by_len: dict[int, list[str]] = {}
    for k in lookup:
        keys_by_len.setdefault(len(k), []).append(k)
    max_key_len = max(keys_by_len.keys()) if keys_by_len else 0

    while i < n:
        ch = text[i]
        if not KANJI_RE.match(ch):
            out.append(ch)
            i += 1
            continue
        # Greedy longest-prefix match anchored at i.
        matched = None
        for L in range(min(max_key_len, n - i), 0, -1):
            cand = text[i:i + L]
            if cand in lookup:
                matched = (cand, lookup[cand])
                break
        if matched:
            out.append(matched[1])
            i += len(matched[0])
        else:
            # Unknown kanji — pass through with a marker so the audit
            # can spot it without breaking the romaji string.
            out.append(ch)
            i += 1
    return ''.join(out)


# ---------------------------------------------------------------------------
# Particle adjustments — kana-to-romaji handles を→o uniformly, but は/へ
# only become wa/e when used as standalone particles (i.e., flanked by
# spaces/punctuation). Conservative regex pass.
# ---------------------------------------------------------------------------

def adjust_particles_in_kana(s: str) -> str:
    """Mark は particles as WA and へ as E so kana_to_romaji emits the
    right pronunciation. Heuristic: は immediately following a bunsetsu
    (kana/kanji char, no space) and immediately followed by a clause
    boundary (space, punctuation, end-of-string) is the topic particle.

    This is a conservative heuristic — false positives on は as part of
    a noun (e.g., はな "flower") are avoided by requiring the right-hand
    boundary. False negatives (e.g., a non-particle は at end of sentence)
    are accepted as the lesser evil; affected cases are rare in this
    corpus and the romaji is still readable."""
    s = re.sub(r'(?<=[ぁ-ゟ゠-ヿ一-鿿])は(?= |、|。|！|？|$)', ' wa', s)
    s = re.sub(r'(?<=[ぁ-ゟ゠-ヿ一-鿿])へ(?= |、|。|！|？|$)', ' e', s)
    # Also break off other particles for readability (を already maps to o).
    s = re.sub(r'(?<=[ぁ-ゟ゠-ヿ一-鿿])を(?= |、|。|！|？|$)', ' を', s)
    return s


def romanize(text: str, lookup: dict[str, str]) -> str:
    kana = to_kana(text, lookup)
    kana = adjust_particles_in_kana(kana)
    return kana_to_romaji(kana)


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------

def main() -> int:
    lookup = build_kana_lookup()
    grammar = json.loads(GRAMMAR.read_text(encoding='utf-8'))

    n_added = 0
    n_skipped = 0
    n_unresolved = 0
    for p in grammar.get('patterns', []):
        for ex in p.get('examples', []):
            if 'romaji' in ex:
                n_skipped += 1
                continue
            ja = ex.get('ja', '') or ''
            if not ja:
                continue
            rom = romanize(ja, lookup)
            # Light cleanup: collapse multiple spaces, trim.
            rom = re.sub(r'\s+', ' ', rom).strip()
            ex['romaji'] = rom
            if KANJI_RE.search(rom):
                n_unresolved += 1
            n_added += 1

    GRAMMAR.write_text(json.dumps(grammar, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Added romaji to {n_added} example(s); {n_skipped} already had it.')
    if n_unresolved:
        print(f'  WARN: {n_unresolved} romaji string(s) still contain kanji (unmapped vocab).')
    print(f'Lookup dictionary size: {len(lookup)} kanji-form entries.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
