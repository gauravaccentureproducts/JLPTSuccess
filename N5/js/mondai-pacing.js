// IMP-WAVE-P4-T1 (UI audit fix, 2026-05-11): per-mondai pacing helper.
//
// Cross-references each sitting question's (category, mondai) tuple
// with section_timing.json so we can show the user the recommended
// seconds-per-question budget plus the strategy hint for that mondai
// type. The official JLPT timing matters for time-discipline; we
// surface it as a non-blocking chip so users build pacing instinct.
//
// Public API:
//   await loadPacing()                   - prime cache (one fetch)
//   getPacing(category, mondaiNum)       - {seconds, label_ja, type, strategy} | null
//
// Category mapping (matches data/papers/<cat>/paper-N.json):
//   moji, goi              -> section_timing.moji_goi.mondai_breakdown
//   bunpou, dokkai         -> section_timing.bunpou_dokkai.mondai_breakdown
//   listening              -> section_timing.chokai.mondai_breakdown
//
// Mondai numbers come from the question.mondai field on each paper.
// `null` is returned when (a) test_strategy.json hasn't loaded yet
// or (b) the (category, mondai) combination isn't in the breakdown
// table. Callers should render nothing in either case rather than a
// placeholder; the chip is meant to be invisible when data is absent.

let _pacingCache = null;
let _pendingLoad = null;

const CATEGORY_TO_SECTION = {
  moji: 'moji_goi',
  goi: 'moji_goi',
  bunpou: 'bunpou_dokkai',
  dokkai: 'bunpou_dokkai',
  listening: 'chokai',
};

export async function loadPacing() {
  if (_pacingCache) return _pacingCache;
  if (_pendingLoad) return _pendingLoad;
  _pendingLoad = (async () => {
    try {
      const r = await fetch('data/test_strategy.json');
      if (!r.ok) return null;
      const d = await r.json();
      _pacingCache = d.section_timing || null;
      return _pacingCache;
    } catch (e) {
      console.warn('[mondai-pacing] load failed:', e);
      return null;
    } finally {
      _pendingLoad = null;
    }
  })();
  return _pendingLoad;
}

export function getPacing(category, mondaiNum) {
  if (!_pacingCache) return null;
  const sectionKey = CATEGORY_TO_SECTION[category];
  if (!sectionKey) return null;
  const section = _pacingCache[sectionKey];
  if (!section || !Array.isArray(section.mondai_breakdown)) return null;
  const num = parseInt(mondaiNum, 10);
  if (!Number.isFinite(num)) return null;
  const entry = section.mondai_breakdown.find(m => m.number === num);
  if (!entry) return null;
  return {
    seconds: entry.seconds_per_q,
    label_ja: entry.label_ja,
    type: entry.type,
    strategy: entry.strategy,
    mondai_number: entry.number,
  };
}

// Convenience: render a small chip for a question, e.g.
//   <span class="mondai-pace-chip" title="<strategy>">≈30s</span>
// Returns the HTML string (caller is responsible for embedding it).
export function renderPacingChip(category, mondaiNum) {
  const p = getPacing(category, mondaiNum);
  if (!p) return '';
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
  // Strategy hint shown as tooltip (title attr) so the chip stays
  // unobtrusive but the technique is one hover/focus away.
  return `<span class="mondai-pace-chip" title="${esc(p.strategy || '')}" aria-label="Recommended time: ${p.seconds} seconds per question. ${esc(p.strategy || '')}">≈${p.seconds}s</span>`;
}
