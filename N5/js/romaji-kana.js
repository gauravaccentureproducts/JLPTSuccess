// IMP-WAVE-P4-21 (UI audit fix, 2026-05-12): romaji-to-hiragana
// auto-converter. Attaches to typed-input fields in the drill /
// production-review flow so a learner without a JP IME can type
// answers in romaji and see them convert live to kana.
//
// Coverage: the standard 平假名 syllabary (gojuuon + dakuten +
// handakuten + youon). Special cases: ん (n / nn / n'), small tsu
// for double consonants, long vowels (-).
//
// Usage:
//   import { attachRomajiKana } from './romaji-kana.js';
//   attachRomajiKana(inputElement);
//
// Behavior: on every `input` event, the input's value is rewritten
// from the latest converted form. Cursor position is preserved at
// the end (typical IME behavior). The conversion is RIGHTMOST-
// LONGEST: e.g., "sho" -> しょ before "s" -> "s".

const KANA = {
  // Vowels
  'a':'あ','i':'い','u':'う','e':'え','o':'お',
  // K
  'ka':'か','ki':'き','ku':'く','ke':'け','ko':'こ',
  'kya':'きゃ','kyu':'きゅ','kyo':'きょ',
  // S
  'sa':'さ','shi':'し','si':'し','su':'す','se':'せ','so':'そ',
  'sha':'しゃ','shu':'しゅ','sho':'しょ','sya':'しゃ','syu':'しゅ','syo':'しょ',
  // T
  'ta':'た','chi':'ち','ti':'ち','tsu':'つ','tu':'つ','te':'て','to':'と',
  'cha':'ちゃ','chu':'ちゅ','cho':'ちょ','tya':'ちゃ','tyu':'ちゅ','tyo':'ちょ',
  // N
  'na':'な','ni':'に','nu':'ぬ','ne':'ね','no':'の',
  'nya':'にゃ','nyu':'にゅ','nyo':'にょ',
  // H
  'ha':'は','hi':'ひ','fu':'ふ','hu':'ふ','he':'へ','ho':'ほ',
  'hya':'ひゃ','hyu':'ひゅ','hyo':'ひょ',
  // M
  'ma':'ま','mi':'み','mu':'む','me':'め','mo':'も',
  'mya':'みゃ','myu':'みゅ','myo':'みょ',
  // Y
  'ya':'や','yu':'ゆ','yo':'よ',
  // R
  'ra':'ら','ri':'り','ru':'る','re':'れ','ro':'ろ',
  'rya':'りゃ','ryu':'りゅ','ryo':'りょ',
  // W
  'wa':'わ','wo':'を','wi':'うぃ','we':'うぇ',
  // N (special)
  'n':'ん',  // bare n; converter handles n+vowel ambiguity below
  'nn':'ん',
  // G (dakuten)
  'ga':'が','gi':'ぎ','gu':'ぐ','ge':'げ','go':'ご',
  'gya':'ぎゃ','gyu':'ぎゅ','gyo':'ぎょ',
  // Z (dakuten)
  'za':'ざ','ji':'じ','zi':'じ','zu':'ず','ze':'ぜ','zo':'ぞ',
  'ja':'じゃ','ju':'じゅ','jo':'じょ','jya':'じゃ','jyu':'じゅ','jyo':'じょ',
  // D (dakuten)
  'da':'だ','di':'ぢ','du':'づ','de':'で','do':'ど',
  'dya':'ぢゃ','dyu':'ぢゅ','dyo':'ぢょ',
  // B (dakuten)
  'ba':'ば','bi':'び','bu':'ぶ','be':'べ','bo':'ぼ',
  'bya':'びゃ','byu':'びゅ','byo':'びょ',
  // P (handakuten)
  'pa':'ぱ','pi':'ぴ','pu':'ぷ','pe':'ぺ','po':'ぽ',
  'pya':'ぴゃ','pyu':'ぴゅ','pyo':'ぴょ',
  // Long vowel
  '-':'ー',
};

// Sort keys longest-first for greedy match
const KEYS = Object.keys(KANA).sort((a, b) => b.length - a.length);

const VOWELS = new Set(['a', 'i', 'u', 'e', 'o']);

/**
 * Convert a romaji string to hiragana. Preserves any non-romaji
 * characters (including existing kana / kanji / punctuation) as-is.
 */
export function romajiToKana(input) {
  let out = '';
  let buf = '';
  for (let i = 0; i < input.length; i++) {
    const ch = input[i].toLowerCase();
    // Non-letter: flush buffer and pass through
    if (!/[a-z\-']/.test(ch)) {
      // Flush any pending "n" as ん
      if (buf === 'n') { out += 'ん'; buf = ''; }
      // Apostrophe: 'n + vowel' separator — flush n
      if (ch === "'" && buf === '') { continue; }
      out += input[i];
      continue;
    }
    buf += ch;
    // Double consonant -> small つ (e.g., "kka" -> "っか")
    if (buf.length >= 2 && buf[0] === buf[1] && !VOWELS.has(buf[0]) && buf[0] !== 'n') {
      out += 'っ';
      buf = buf.slice(1);
    }
    // Try longest match
    let matched = false;
    for (const key of KEYS) {
      if (buf.endsWith(key)) {
        const prefix = buf.slice(0, buf.length - key.length);
        // The prefix could be incomplete; only flush if it would
        // independently convert (e.g., should not happen at this
        // point — but emit prefix as-is for safety).
        if (prefix) {
          // Handle case where prefix is a leftover "n" before a vowel-starting kana
          if (prefix === 'n' && /^[aiueo]/.test(key)) {
            out += 'ん';
          } else {
            out += prefix;
          }
        }
        out += KANA[key];
        buf = '';
        matched = true;
        break;
      }
    }
    if (matched) continue;
  }
  // Flush remaining: "n" -> "ん", other leftover romaji stays
  if (buf === 'n') out += 'ん';
  else out += buf;
  return out;
}

/**
 * Attach live romaji→kana conversion to an input element.
 * Idempotent: safe to call multiple times on the same element
 * (only attaches once).
 */
export function attachRomajiKana(inputEl) {
  if (!inputEl || inputEl.dataset.romajiKanaAttached === '1') return;
  inputEl.dataset.romajiKanaAttached = '1';
  inputEl.setAttribute('inputmode', 'text');
  inputEl.setAttribute('lang', 'ja');
  inputEl.addEventListener('input', (ev) => {
    const before = inputEl.value;
    const converted = romajiToKana(before);
    if (converted !== before) {
      inputEl.value = converted;
      // Cursor to end (standard IME behavior)
      try { inputEl.setSelectionRange(converted.length, converted.length); } catch {}
    }
  });
}

/**
 * Attach to all matching inputs on a container. Useful for batch-
 * wiring up answer fields in drill / test pages.
 */
export function attachRomajiKanaAll(container, selector = 'input[data-jp-input]') {
  if (!container) return;
  container.querySelectorAll(selector).forEach(attachRomajiKana);
}
