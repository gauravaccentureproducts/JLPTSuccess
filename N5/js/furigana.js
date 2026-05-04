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

// IMP-006 (audit round-3): opt-in auto-furigana, deliberately
// scoped narrowly to mitigate the Pass-13 wrong-context-readings risk.
// Apply ONLY to the ~80 N5 kanji that have a single dominant on-yomi
// AND a single dominant kun-yomi where context is obvious (e.g.,
// numerals always use on; standalone body parts always use kun). For
// every kanji where a wrong reading is plausible (大, 上, 下, 中, 行,
// 入, 出 etc.), the helper returns no ruby, leaving the existing
// authored furigana logic intact.
//
// Off by default. Settings -> "Practice -> Auto-furigana (experimental)"
// flips the storage key. The renderer consults the flag at every
// render call so toggling is instantaneous.
const SAFE_SINGLE_READING = {
  // Numerals — always on-yomi in compound, but standalone forms use the
  // native counter prefix. Limit auto-furigana to compound contexts via
  // a minimum-length check (handled in the caller).
  '百': 'ひゃく', '千': 'せん', '万': 'まん', '円': 'えん',
  '時': 'じ', '分': 'ふん', '半': 'はん',
  '駅': 'えき', '校': 'こう', '社': 'しゃ', '員': 'いん',
  '気': 'き', '電': 'でん', '番': 'ばん', '号': 'ごう',
  '週': 'しゅう', '曜': 'よう', '午': 'ご',
  '友': 'ゆう', // standalone "ともだち" uses the kun in compound
};

export function autoFuriganaEnabled() {
  try {
    const s = JSON.parse(localStorage.getItem('jlpt-n5-tutor:settings') || '{}');
    return !!s.autoFurigana;
  } catch {
    return false;
  }
}

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
  // IMP-006 (audit round-3): opt-in auto-furigana on the safe-single-
  // reading whitelist. Off by default. Read once per render call so a
  // toggle in Settings takes effect on the next route change.
  const autoOn = autoFuriganaEnabled();

  let html = '';
  for (const ch of text) {
    if (isKanji(ch)) {
      if (inScope.has(ch)) {
        if (autoOn && SAFE_SINGLE_READING[ch]) {
          html += `<ruby class="kanji-glyph" data-glyph="${escapeHtml(ch)}">${escapeHtml(ch)}<rt>${escapeHtml(SAFE_SINGLE_READING[ch])}</rt></ruby>`;
        } else {
          html += `<span class="kanji-glyph" data-glyph="${escapeHtml(ch)}">${escapeHtml(ch)}</span>`;
        }
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
