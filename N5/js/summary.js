// Chapter 4 - Summary. Mastered / weak / untested.
import * as storage from './storage.js';

let grammarCache = null;

async function loadGrammar() {
  if (grammarCache) return grammarCache;
  const res = await fetch('data/grammar.json');
  grammarCache = await res.json();
  return grammarCache;
}

export async function renderSummary(container) {
  const data = await loadGrammar();
  const allIds = (data.patterns || []).map(p => p.id);
  const patternMap = new Map((data.patterns || []).map(p => [p.id, p]));
  const masteredIds = storage.getMasteredPatternIds();
  const weakIds = storage.getWeakPatternIds();
  const seenIds = storage.getSeenPatternIds();
  const untestedIds = allIds.filter(id => !seenIds.includes(id));

  const results = storage.getResults();
  const totalTests = results.length;
  const lastTest = results[results.length - 1];

  // Empty state: no progress at all (no tests, no patterns seen). Brief 2 §3.2.
  if (totalTests === 0 && seenIds.length === 0) {
    container.innerHTML = `
      <h2>Chapter 4 - Summary</h2>
      <div class="empty-state">
        <p><strong>Stats appear here once you've studied.</strong></p>
        <p class="muted">Mastered, Need-practice, and Untested counts appear after a Test or completed lessons.</p>
        <p><a href="#/learn" class="btn-primary" style="text-decoration:none">Start a lesson</a></p>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <h2>Chapter 4 - Summary</h2>

    <section class="summary-stats">
      <div class="stat-card mastered">
        <div class="stat-num">${masteredIds.length}</div>
        <div class="stat-label">Mastered</div>
        <div class="stat-hint">≥ 4 consecutive correct</div>
      </div>
      <div class="stat-card weak">
        <div class="stat-num">${weakIds.length}</div>
        <div class="stat-label">Need practice</div>
        <div class="stat-hint">≥ 50% error, ≥ 2 attempts</div>
      </div>
      <div class="stat-card untested">
        <div class="stat-num">${untestedIds.length}</div>
        <div class="stat-label">Untested</div>
        <div class="stat-hint">Not seen in any test</div>
      </div>
      <div class="stat-card neutral">
        <div class="stat-num">${totalTests}</div>
        <div class="stat-label">Tests taken</div>
        ${lastTest ? `<div class="stat-hint">Last: ${formatDate(lastTest.timestamp)}</div>` : '<div class="stat-hint">None yet</div>'}
      </div>
    </section>

    ${renderHeatmap(data.patterns || [], new Set(masteredIds), new Set(weakIds), new Set(seenIds))}

    ${renderErrorPatterns(results, patternMap)}

    ${renderRecommendation(masteredIds, weakIds, untestedIds, patternMap)}

    ${renderSessionLog(results)}

    ${listSection('Mastered', masteredIds, patternMap, 'No mastered patterns yet. 4 consecutive correct in tests/drill graduates a pattern.')}
    ${listSection('Need practice', weakIds, patternMap, 'No weak patterns. Either you have not tested yet, or you are doing well.')}
    ${listSection('Untested', untestedIds, patternMap, 'All authored patterns have been tested at least once.')}

    <section class="next-steps">
      <h3>Suggested next step</h3>
      ${suggestNextStep(masteredIds, weakIds, untestedIds, totalTests)}
    </section>

    <section class="reset">
      <button id="retake-diagnostic">Re-take Diagnostic</button>
      <button id="reset-progress" class="btn-danger">Reset all progress</button>
      <p class="muted small">Reset clears history, results, weak patterns, and settings. Cannot be undone.</p>
    </section>
  `;

  document.getElementById('reset-progress')?.addEventListener('click', () => {
    if (!confirm('Reset all progress? This clears every test result, the rolling history, and weak-pattern flags.')) return;
    if (!confirm('Are you sure? This cannot be undone.')) return;
    storage.reset();
    location.hash = '#/learn';
    location.reload();
  });
  document.getElementById('retake-diagnostic')?.addEventListener('click', () => {
    location.hash = '#/diagnostic';
  });
}

// ----- Error-pattern detection (Brief §2.12) -----

function renderErrorPatterns(results, patternMap) {
  // Aggregate per-pattern accuracy across all results.
  const stats = new Map(); // pid -> {attempts, correct}
  for (const r of results) {
    for (const resp of r.responses || []) {
      if (!resp.grammarPatternId) continue;
      const s = stats.get(resp.grammarPatternId) || { attempts: 0, correct: 0 };
      s.attempts += 1;
      if (resp.isCorrect) s.correct += 1;
      stats.set(resp.grammarPatternId, s);
    }
  }
  if (stats.size === 0) {
    return '';
  }
  // Sort by lowest accuracy, attempts >= 2 only (avoid noise).
  const ranked = [...stats.entries()]
    .map(([pid, s]) => ({
      pid,
      attempts: s.attempts,
      correct: s.correct,
      accuracy: s.correct / s.attempts,
      pattern: patternMap.get(pid),
    }))
    .filter(x => x.attempts >= 2)
    .sort((a, b) => a.accuracy - b.accuracy)
    .slice(0, 6);

  if (ranked.length === 0) return '';

  const items = ranked.map(r => {
    const pct = Math.round(r.accuracy * 100);
    const label = r.pattern?.pattern || r.pid;
    const meaning = r.pattern?.meaning_en || '';
    return `
      <li class="error-row">
        <div class="error-row-head">
          <a href="#/learn/${encodeURIComponent(r.pid)}"><strong>${esc(label)}</strong></a>
          <span class="error-acc">${pct}%</span>
        </div>
        <div class="error-row-meta">${r.correct}/${r.attempts} correct · ${esc(meaning)}</div>
        <div class="error-bar"><div style="width:${pct}%; background: ${pct < 50 ? 'var(--c-error)' : pct < 70 ? 'var(--c-warning)' : 'var(--c-success)'}"></div></div>
      </li>
    `;
  }).join('');

  return `
    <section class="error-patterns">
      <h3>Error patterns</h3>
      <p class="muted small">Patterns with ≥ 2 attempts, sorted by lowest accuracy. Click to revisit the lesson.</p>
      <ol class="error-list">${items}</ol>
    </section>
  `;
}

function renderRecommendation(masteredIds, weakIds, untestedIds, patternMap) {
  const recs = [];
  // 1. Top weak patterns (up to 5)
  for (const pid of weakIds.slice(0, 5)) {
    const p = patternMap.get(pid);
    if (p) recs.push({ pid, label: p.pattern, why: 'Needs practice (≥ 50% errors)' });
  }
  // 2. If room, recommend untested foundational patterns (n5-001 through n5-019)
  if (recs.length < 5) {
    const slots = 5 - recs.length;
    const untestedFoundations = untestedIds.filter(id => /^n5-0(0[1-9]|1[0-9])$/.test(id)).slice(0, slots);
    for (const pid of untestedFoundations) {
      const p = patternMap.get(pid);
      if (p) recs.push({ pid, label: p.pattern, why: 'Foundational - not yet practiced' });
    }
  }
  if (recs.length === 0) return '';
  const items = recs.map(r => `
    <li><a href="#/learn/${encodeURIComponent(r.pid)}"><strong>${esc(r.label)}</strong></a> <span class="muted small">- ${esc(r.why)}</span></li>
  `).join('');
  return `
    <section class="recommendation">
      <h3>Recommended next session</h3>
      <ul class="rec-list">${items}</ul>
    </section>
  `;
}

function renderSessionLog(results) {
  if (!results || results.length === 0) return '';
  const recent = results.slice(-10).reverse(); // newest first, last 10
  const rows = recent.map(r => {
    const pct = r.total > 0 ? Math.round((r.correct / r.total) * 100) : 0;
    const date = new Date(r.timestamp).toLocaleString();
    return `<tr><td>${esc(date)}</td><td>${r.total}</td><td>${r.correct}</td><td>${pct}%</td></tr>`;
  }).join('');
  return `
    <section class="session-log">
      <h3>Session log <span class="muted small">(last ${recent.length})</span></h3>
      <table class="session-table">
        <thead><tr><th>When</th><th>Length</th><th>Correct</th><th>%</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </section>
  `;
}

function renderHeatmap(patterns, mastered, weak, seen) {
  // Group patterns by category, then summarize each.
  const byCat = new Map();
  for (const p of patterns) {
    const cat = p.category || 'Other';
    if (!byCat.has(cat)) byCat.set(cat, { order: p.categoryOrder ?? 99, patterns: [] });
    byCat.get(cat).patterns.push(p);
  }
  const sorted = [...byCat.entries()].sort((a, b) => a[1].order - b[1].order);

  const cells = sorted.map(([cat, { patterns: ps }]) => {
    const total = ps.length;
    const mCount = ps.filter(p => mastered.has(p.id)).length;
    const wCount = ps.filter(p => weak.has(p.id)).length;
    const sCount = ps.filter(p => seen.has(p.id)).length;

    let state = 'untested';
    let title = `${total} pattern${total === 1 ? '' : 's'} - none seen yet`;
    if (wCount > 0) {
      state = 'weak';
      title = `${wCount} weak / ${total} total. Review needed.`;
    } else if (mCount === total && total > 0) {
      state = 'mastered';
      title = `All ${total} mastered.`;
    } else if (sCount > 0) {
      state = 'in-progress';
      title = `${mCount} mastered / ${sCount} seen / ${total} total.`;
    }

    const ratio = total > 0 ? Math.round((mCount / total) * 100) : 0;
    return `
      <div class="heat-cell heat-${state}" title="${esc(title)}" data-cat="${esc(cat)}">
        <div class="heat-cat">${esc(cat)}</div>
        <div class="heat-meta">
          <span class="heat-count">${mCount}/${total}</span>
          ${wCount > 0 ? `<span class="heat-warn">${wCount} weak</span>` : ''}
        </div>
        <div class="heat-bar"><div style="width:${ratio}%"></div></div>
      </div>
    `;
  }).join('');

  return `
    <section class="heatmap-section">
      <h3>Category heatmap</h3>
      <p class="muted small">Each cell shows mastered / total for one of the ${sorted.length} categories. Hover for details.</p>
      <div class="heatmap-grid">${cells}</div>
      <div class="heatmap-legend">
        <span><span class="legend-swatch heat-mastered"></span>All mastered</span>
        <span><span class="legend-swatch heat-in-progress"></span>In progress</span>
        <span><span class="legend-swatch heat-weak"></span>Has weak items</span>
        <span><span class="legend-swatch heat-untested"></span>Untested</span>
      </div>
    </section>
  `;
}

function listSection(title, ids, patternMap, emptyMsg) {
  if (ids.length === 0) {
    return `<section class="pattern-section"><h3>${esc(title)} (0)</h3><p class="muted">${esc(emptyMsg)}</p></section>`;
  }
  const items = ids.map(id => {
    const p = patternMap.get(id);
    const label = p ? `${p.pattern} - ${p.meaning_en}` : id;
    return `<li><a href="#/learn/${encodeURIComponent(id)}">${esc(label)}</a></li>`;
  }).join('');
  return `<section class="pattern-section"><h3>${esc(title)} (${ids.length})</h3><ul>${items}</ul></section>`;
}

function suggestNextStep(mastered, weak, untested, totalTests) {
  if (totalTests === 0) {
    return `<p>Take your first test in <a href="#/test">Chapter 2</a>. The system will identify weak patterns automatically and queue them for re-teaching.</p>`;
  }
  if (weak.length > 0) {
    return `<p><strong>${weak.length}</strong> pattern(s) need practice. Open <a href="#/review">Chapter 3 - Review</a> to study them with form rules, common mistakes, and per-distractor explanations.</p>`;
  }
  if (untested.length > 0) {
    return `<p>You haven't seen <strong>${untested.length}</strong> pattern(s) in any test. Take another test in <a href="#/test">Chapter 2</a> for broader coverage.</p>`;
  }
  return `<p>Strong work - you've covered every authored pattern with no current weaknesses. Keep practicing to graduate them all to mastered.</p>`;
}

function formatDate(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleDateString();
  } catch { return iso; }
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
