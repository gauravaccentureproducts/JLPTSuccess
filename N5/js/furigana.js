// Furigana renderer (post-Pass-13 simplification).
//
// Pass-13 native-speaker review found auto-generated ruby was producing
// wrong readings (大学 rendered as 大[おお]+学 instead of だいがく) because
// Japanese kanji readings are context-dependent and a single-primary lookup
// table can't disambiguate. The auto-furigana feature has been removed.
//
// New rule (per user direction 2026-04-30):
//   - In-scope N5 kanji          → render plain kanji, NO ruby.
//   - Out-of-scope kanji         → content authors must write the kana form
//                                  (the renderer flags any leak with `<rt>?</rt>`
//                                  so it's visually obvious during review).
//   - Explicit per-word ruby     → still honoured if the JSON entry carries
//                                  a `furigana: [{word, reading}, ...]` array
//                                  (escape hatch for cases where an author
//                                  deliberately wants to annotate a word).
//
// The kanji popover (click any glyph) reads `data/n5_kanji_readings.json`
// directly at popover-time; that file is still used there.
import * as storage from './storage.js';

let n5KanjiSet = null;

async function loadData() {
  if (n5KanjiSet) return;
  try {
    const wl = await fetch('data/n5_kanji_whitelist.json').then(r => r.json());
    n5KanjiSet = new Set(wl);
  } catch (err) {
    console.warn('Could not load kanji whitelist.', err);
    n5KanjiSet = new Set();
  }
}

// initFuriganaToggle: NAME IS LEGACY. The auto-furigana toggle was removed
// in Pass-13 (2026-04-30). The function is now a thin loader for the kanji
// whitelist used by `renderJa` to mark in-scope vs out-of-scope glyphs;
// kept under its old name so app.js wiring stays untouched. ISSUE-004
// (2026-05-04): dropped the dead `#furigana-toggle` DOM lookup since no
// such element ships in index.html — the comment was confusing future readers.
export async function initFuriganaToggle(_onChange) {
  await loadData();
}

// Legacy compatibility shims (some modules import these).
export function isFuriganaOnForN5() { return false; }
export function getFuriganaMode() { return 'never'; }

const KANJI_RE = /[一-鿿]/;
function isKanji(ch) { return KANJI_RE.test(ch); }

/**
 * Render Japanese text.
 *
 * Per Pass-13 redesign: NO ruby is generated, ever. Explicit-furigana
 * arrays in the JSON are ignored (the user removed the feature altogether).
 *   - In-scope N5 kanji   → plain kanji.
 *   - Out-of-scope kanji  → `<ruby>kanji<rt>?</rt></ruby>` (visible flag for
 *                            content authors; user-facing data should use
 *                            kana for any out-of-scope word).
 *
 * The explicitFurigana parameter is accepted but ignored (kept in the
 * signature for backward compatibility with callers).
 *
 * @param {string} text - Japanese text.
 * @param {Array<{word: string, reading: string}>} _explicitFurigana - ignored.
 * @returns {string} HTML string wrapped in `<span lang="ja">`.
 */
export function renderJa(text, _explicitFurigana = []) {
  if (!text) return '';

  const inScope = n5KanjiSet || new Set();
  let html = '';
  for (const ch of text) {
    if (isKanji(ch)) {
      if (inScope.has(ch)) {
        html += `<span class="kanji-glyph" data-glyph="${escapeHtml(ch)}">${escapeHtml(ch)}</span>`;
      } else {
        // Out-of-scope kanji. Should never appear in clean data; flag visibly.
        html += `<ruby data-glyph="${escapeHtml(ch)}">${escapeHtml(ch)}<rt>?</rt></ruby>`;
      }
    } else {
      html += escapeHtml(ch);
    }
  }
  return `<span lang="ja">${html}</span>`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
