// Forgiving answer-matcher for type-the-answer drills. Per Brief §2.10.
// Accepts kana, romaji (Hepburn-ish), or mixed input, normalizes punctuation,
// half/full-width, and trailing whitespace, then compares against a list of
// acceptable answers.

// Hepburn → hiragana table. Sorted longest-first so e.g. "kya" matches before "ka".
const ROMAJI_TABLE = (() => {
  const base = {
    // Digraphs (3-letter)
    'kya':'きゃ','kyu':'きゅ','kyo':'きょ',
    'sha':'しゃ','shu':'しゅ','sho':'しょ','shi':'し',
    'cha':'ちゃ','chu':'ちゅ','cho':'ちょ','chi':'ち',
    'nya':'にゃ','nyu':'にゅ','nyo':'にょ',
    'hya':'ひゃ','hyu':'ひゅ','hyo':'ひょ',
    'mya':'みゃ','myu':'みゅ','myo':'みょ',
    'rya':'りゃ','ryu':'りゅ','ryo':'りょ',
    'gya':'ぎゃ','gyu':'ぎゅ','gyo':'ぎょ',
    'ja':'じゃ','ju':'じゅ','jo':'じょ','ji':'じ',
    'bya':'びゃ','byu':'びゅ','byo':'びょ',
    'pya':'ぴゃ','pyu':'ぴゅ','pyo':'ぴょ',
    'tsu':'つ','tsa':'つぁ','tse':'つぇ','tso':'つぉ',
    'fa':'ふぁ','fi':'ふぃ','fe':'ふぇ','fo':'ふぉ','fu':'ふ',
    // Vowels
    'a':'あ','i':'い','u':'う','e':'え','o':'お',
    // K-row
    'ka':'か','ki':'き','ku':'く','ke':'け','ko':'こ',
    'ga':'が','gi':'ぎ','gu':'ぐ','ge':'げ','go':'ご',
    // S-row
    'sa':'さ','su':'す','se':'せ','so':'そ',
    'za':'ざ','zu':'ず','ze':'ぜ','zo':'ぞ',
    // T-row
    'ta':'た','te':'て','to':'と',
    'da':'だ','de':'で','do':'ど','dzu':'づ',
    // N-row
    'na':'な','ni':'に','nu':'ぬ','ne':'ね','no':'の',
    // H-row
    'ha':'は','hi':'ひ','he':'へ','ho':'ほ',
    'ba':'ば','bi':'び','bu':'ぶ','be':'べ','bo':'ぼ',
    'pa':'ぱ','pi':'ぴ','pu':'ぷ','pe':'ぺ','po':'ぽ',
    // M-row
    'ma':'ま','mi':'み','mu':'む','me':'め','mo':'も',
    // Y-row
    'ya':'や','yu':'ゆ','yo':'よ',
    // R-row
    'ra':'ら','ri':'り','ru':'る','re':'れ','ro':'ろ',
    // W-row + を
    'wa':'わ','wo':'を',
    // ん handled below via lookahead
  };
  // Sort keys by descending length so longest-match wins.
  const keys = Object.keys(base).sort((a, b) => b.length - a.length);
  return { keys, map: base };
})();

/**
 * Convert a romaji string (lowercase Hepburn) to hiragana. Best-effort.
 * - 'tt' / 'kk' / etc → small っ + corresponding kana
 * - 'n' followed by a non-vowel-non-y → ん
 * - Trailing 'n' / 'n'' → ん
 */
export function romajiToHiragana(input) {
  if (!input) return '';
  let s = String(input).toLowerCase();
  // Strip apostrophes (common for n')
  s = s.replace(/'/g, '');
  let out = '';
  let i = 0;
  while (i < s.length) {
    // Sokuon: double consonant (except n)
    if (i + 1 < s.length && s[i] === s[i + 1] && /[bcdfghjkmpqrstvwxyz]/.test(s[i])) {
      out += 'っ';
      i += 1;
      continue;
    }
    // ん: standalone 'n' before non-vowel-non-y, or end of string
    if (s[i] === 'n' && (i === s.length - 1 || /[^aiueoy]/.test(s[i + 1]))) {
      out += 'ん';
      i += 1;
      continue;
    }
    // Try longest match
    let matched = false;
    for (const k of ROMAJI_TABLE.keys) {
      if (s.startsWith(k, i)) {
        out += ROMAJI_TABLE.map[k];
        i += k.length;
        matched = true;
        break;
      }
    }
    if (!matched) {
      // Pass through unknown char (likely punctuation / space)
      out += s[i];
      i += 1;
    }
  }
  return out;
}

/**
 * Convert katakana to hiragana for matching purposes.
 */
function katakanaToHiragana(s) {
  let out = '';
  for (const ch of s) {
    const code = ch.charCodeAt(0);
    if (code >= 0x30A1 && code <= 0x30F6) out += String.fromCharCode(code - 0x60);
    else out += ch;
  }
  return out;
}

/**
 * Normalize an answer string for comparison:
 * - lowercase
 * - half-width katakana → full-width
 * - katakana → hiragana
 * - romaji → hiragana
 * - strip whitespace, punctuation, common particles around edges
 */
export function normalizeAnswer(s) {
  if (s == null) return '';
  let t = String(s).trim();
  // Half-width to full-width for ASCII (uppercase letters etc.)
  t = t.normalize('NFKC');
  // Remove common trailing/leading punctuation
  t = t.replace(/^[\s「『（(『]+|[\s。、，,．.！!？?」』）)］]+$/g, '');
  // If contains any romaji letter, convert romaji to hiragana
  if (/[a-z]/i.test(t)) {
    t = romajiToHiragana(t.toLowerCase());
  }
  // Katakana → hiragana for matching
  t = katakanaToHiragana(t);
  // Strip remaining whitespace
  t = t.replace(/\s+/g, '');
  return t;
}

/**
 * Generate alternate forms of a normalized string by enumerating per-position
 * swaps for the homophone-particle pairs that romaji input collapses:
 *   wa ↔ は, e ↔ へ, o ↔ を.
 *
 * Romaji 'wa' converts to わ but Japanese topic-particle は is also pronounced
 * 'wa'. Mass-replacing every わ with は would corrupt content words like わたし.
 * Instead we enumerate every subset of swap positions (cap at 16 swappable
 * positions = 65536 candidates worst case; trims runaway by capping at 8).
 */
const SWAP_PAIRS = [['わ', 'は'], ['お', 'を'], ['え', 'へ']];
const SWAP_FROMS = SWAP_PAIRS.map(([from]) => from);
const SWAP_MAP = Object.fromEntries(SWAP_PAIRS);

function withParticleAlternates(base) {
  if (!base) return [''];
  // Find positions whose char is a swap source (わ / お / え)
  const positions = [];
  for (let i = 0; i < base.length; i++) {
    if (SWAP_FROMS.includes(base[i])) positions.push(i);
  }
  // Cap to avoid combinatorial blow-up on long inputs.
  const capped = positions.slice(-8);
  const N = capped.length;
  const variants = new Set([base]);
  for (let mask = 1; mask < (1 << N); mask++) {
    const arr = base.split('');
    for (let bit = 0; bit < N; bit++) {
      if (mask & (1 << bit)) {
        const idx = capped[bit];
        arr[idx] = SWAP_MAP[arr[idx]];
      }
    }
    variants.add(arr.join(''));
  }
  return [...variants];
}

/**
 * Match user input against a list of acceptable answers.
 * Returns true if any normalized acceptable answer equals the normalized input
 * (or its homophone-particle alternate).
 */
export function matchesAnswer(userInput, acceptable) {
  const a = normalizeAnswer(userInput);
  if (!a) return false;
  const userVariants = new Set(withParticleAlternates(a));
  const list = Array.isArray(acceptable) ? acceptable : [acceptable];
  for (const x of list) {
    const target = normalizeAnswer(x);
    for (const variant of userVariants) {
      if (variant === target) return true;
    }
  }
  return false;
}
