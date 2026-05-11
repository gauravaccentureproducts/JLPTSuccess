// T5 weak-area dashboard (UI audit P4 feature, 2026-05-11).
//
// Cross-references the user's actual answer history with the
// diagnostic_drills paths in data/test_strategy.json. For each diagnostic
// area, computes a real accuracy score against patterns/vocab/kanji that
// match that area's `module_pointers`, then surfaces actionable
// drill recommendations.
//
// Route: #/weak-areas
//
// Data flow:
//   1. Load test_strategy.json once (cached) → 9 diagnostic_areas.
//   2. Pull storage.getHistory() (per-pattern correct/incorrect counts) +
//      storage.getWrongHistory() (recent miss log).
//   3. For each diagnostic_area, identify the patterns that fall in its scope
//      (parsed from `module_pointers`, e.g., "data/grammar.json:n5-066..070").
//   4. Compute attempts + correct counts → accuracy %.
//   5. Display areas sorted by accuracy ascending (worst first).

import * as storage from './storage.js';
import { t } from './i18n.js';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c]));

let _strategyCache = null;
async function loadStrategy() {
  if (_strategyCache) return _strategyCache;
  try {
    const r = await fetch('data/test_strategy.json');
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    _strategyCache = await r.json();
    return _strategyCache;
  } catch (e) {
    console.error('[weak-areas] load failed:', e);
    return null;
  }
}

let _grammarCache = null;
async function loadGrammar() {
  if (_grammarCache) return _grammarCache;
  try {
    const r = await fetch('data/grammar.json');
    if (!r.ok) return null;
    const d = await r.json();
    _grammarCache = d.patterns || [];
    return _grammarCache;
  } catch { return null; }
}

// Parse a module_pointer like "data/grammar.json:n5-066..070" into a
// predicate that decides whether a given pattern id falls in scope.
function parsePointer(ptr) {
  if (typeof ptr !== 'string') return null;
  const grammarMatch = ptr.match(/grammar\.json:(n5-\d+)(?:\.\.(n5-)?(\d+))?/);
  if (grammarMatch) {
    const startId = grammarMatch[1];
    const endNumStr = grammarMatch[3];
    const startNum = parseInt(startId.split('-')[1], 10);
    const endNum = endNumStr ? parseInt(endNumStr, 10) : startNum;
    return {
      kind: 'grammar',
      matches: (pid) => {
        if (typeof pid !== 'string' || !pid.startsWith('n5-')) return false;
        const n = parseInt(pid.split('-')[1], 10);
        return Number.isFinite(n) && n >= startNum && n <= endNum;
      },
    };
  }
  if (ptr.includes('kanji.json')) {
    return { kind: 'kanji', matches: () => false }; // not used yet
  }
  if (ptr.includes('vocab.json')) {
    return { kind: 'vocab', matches: () => false }; // not used yet
  }
  if (ptr.includes('listening.json')) {
    return { kind: 'listening', matches: () => false };
  }
  if (ptr.includes('reading.json')) {
    return { kind: 'reading', matches: () => false };
  }
  return null;
}

function computeAreaStats(area, history, grammarPatterns) {
  // Build the set of patterns in scope for this diagnostic area.
  const predicates = (area.module_pointers || []).map(parsePointer).filter(Boolean);
  if (!predicates.length) return null;

  const inScope = new Set();
  for (const p of grammarPatterns) {
    for (const pred of predicates) {
      if (pred.kind === 'grammar' && pred.matches(p.id)) {
        inScope.add(p.id);
        break;
      }
    }
  }

  // Aggregate correct/wrong counts from history.
  let attempts = 0;
  let correct = 0;
  for (const pid of inScope) {
    const h = history[pid];
    if (!h) continue;
    const a = (h.correct || 0) + (h.wrong || 0);
    if (!a) continue;
    attempts += a;
    correct += (h.correct || 0);
  }

  const accuracy = attempts > 0 ? Math.round(100 * correct / attempts) : null;
  return {
    area_name: area.area,
    n_in_scope: inScope.size,
    attempts,
    correct,
    accuracy,
    drill_recommendation: area.drill_recommendation || '',
    module_pointers: area.module_pointers || [],
    diagnostic_questions: area.diagnostic_questions || [],
  };
}

function badgeForAccuracy(acc) {
  if (acc == null) return `<span class="weak-area-badge weak-area-untested">Not tested</span>`;
  if (acc < 60) return `<span class="weak-area-badge weak-area-low">${acc}% — needs review</span>`;
  if (acc < 80) return `<span class="weak-area-badge weak-area-mid">${acc}% — improving</span>`;
  return `<span class="weak-area-badge weak-area-high">${acc}% — solid</span>`;
}

export async function renderWeakAreas(container) {
  container.innerHTML = `<p class="muted small">Computing your weak areas…</p>`;
  const [strategy, grammarPatterns] = await Promise.all([loadStrategy(), loadGrammar()]);
  if (!strategy || !grammarPatterns) {
    container.innerHTML = `<article class="weak-areas-page"><p>Couldn't load required data. Please try again.</p></article>`;
    return;
  }

  const history = storage.getHistory() || {};
  const areas = (strategy.diagnostic_drills && strategy.diagnostic_drills.diagnostic_areas) || [];

  const stats = areas
    .map(a => computeAreaStats(a, history, grammarPatterns))
    .filter(Boolean);

  // Sort: areas with attempts and lowest accuracy first; untested last.
  stats.sort((a, b) => {
    if (a.accuracy == null && b.accuracy == null) return 0;
    if (a.accuracy == null) return 1;
    if (b.accuracy == null) return -1;
    return a.accuracy - b.accuracy;
  });

  const anyAttempts = stats.some(s => s.attempts > 0);

  container.innerHTML = `
    <article class="weak-areas-page">
      <a class="back-link" href="#/summary">← Back to Progress</a>
      <h2>Weak-area diagnostic</h2>
      <p class="muted">
        Cross-references your actual test &amp; drill history against the
        9 diagnostic areas in <code>test_strategy.json</code>. Areas with
        accuracy &lt; 60% are flagged for review; each links to the
        specific drill resources for that gap.
      </p>
      ${!anyAttempts ? `
        <div class="empty-state">
          <p>No test history yet. Take a few tests or drill some questions, then come back to see your diagnostic.</p>
          <p><a href="#/test" class="btn-primary" style="text-decoration:none">Start a test</a></p>
        </div>
      ` : ''}
      <section class="weak-areas-list">
        ${stats.map(s => `
          <article class="weak-area-card">
            <header class="weak-area-header">
              <h3>${esc(s.area_name)}</h3>
              ${badgeForAccuracy(s.accuracy)}
            </header>
            <p class="muted small">
              ${s.n_in_scope} pattern(s) in scope ·
              ${s.attempts} attempt(s)${s.accuracy != null ? ` · ${s.correct}/${s.attempts} correct` : ''}
            </p>
            ${s.drill_recommendation ? `<p class="weak-area-recommendation">${esc(s.drill_recommendation)}</p>` : ''}
            ${s.diagnostic_questions?.length ? `
              <details class="weak-area-diagnostic">
                <summary class="muted small">Diagnostic questions</summary>
                <ul>${s.diagnostic_questions.map(q => `<li class="muted small">${esc(q)}</li>`).join('')}</ul>
              </details>
            ` : ''}
            ${s.module_pointers?.length ? `
              <p class="muted small">References: ${s.module_pointers.map(esc).join(', ')}</p>
            ` : ''}
          </article>
        `).join('')}
      </section>
      <p class="muted small" style="margin-top:24px">
        <a href="#/strategy">See full test-strategy bank →</a>
      </p>
    </article>
  `;
}
