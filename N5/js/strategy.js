// IMP-WAVE1 (UI audit fix, 2026-05-11): Test-strategy page renderer.
// Consumes data/test_strategy.json (T1-T6 fully authored) and surfaces:
//   T1 section_timing  — per-mondai time budgets
//   T2 trap_patterns   — 30 catalogued JLPT N5 traps
//   T3 techniques      — 15 actionable test-taking techniques
//   T4 score_breakdown — JEES scoring + diagnostic bands
//   T5 diagnostic_drills — 9 weak-area drill paths
//   T6 meta_strategy   — 5-min summary + study split + 14-day schedule + exam-day checklist
//
// Route: #/strategy
//
// Until now this rich 36 KB data file was reachable at /data/test_strategy.json
// but not consumed by any UI surface. This module wires it up.

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c]));

let _strategy = null;
async function loadStrategy() {
  if (_strategy) return _strategy;
  try {
    const r = await fetch('data/test_strategy.json');
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    _strategy = await r.json();
    return _strategy;
  } catch (e) {
    console.error('[strategy] load failed:', e);
    return null;
  }
}

function renderSectionTiming(timing) {
  if (!timing) return '';
  const sections = ['moji_goi', 'bunpou_dokkai', 'chokai'];
  const html = sections.map(key => {
    const s = timing[key];
    if (!s) return '';
    const rows = (s.mondai_breakdown || []).map(m => `
      <tr>
        <td>${esc(m.number)}</td>
        <td>${esc(m.type)} ${m.label_ja ? `<span class="muted small" lang="ja">${esc(m.label_ja)}</span>` : ''}</td>
        <td>${esc(m.n_questions)}</td>
        <td>${esc(m.seconds_per_q)}s</td>
        <td class="muted small">${esc(m.strategy || '')}</td>
      </tr>
    `).join('');
    return `
      <section class="timing-section">
        <h4>${esc(s.section_part || key)} — ${esc(s.module || '')}</h4>
        <p class="muted small">${esc(s.total_minutes)} min · ${esc(s.total_questions)} questions · avg ${esc(s.average_seconds_per_question)}s/q</p>
        <table class="timing-table">
          <thead><tr><th>Mondai</th><th>Type</th><th>Q</th><th>Time/Q</th><th>Strategy</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
        ${s.time_budget_warning ? `<p class="muted small warning">⚠ ${esc(s.time_budget_warning)}</p>` : ''}
        ${s.rest_break ? `<p class="muted small">${esc(s.rest_break)}</p>` : ''}
        ${s.format_note ? `<p class="muted small">${esc(s.format_note)}</p>` : ''}
      </section>
    `;
  }).join('');
  return `
    <section class="strategy-block">
      <h3>T1 · Section &amp; mondai timing</h3>
      ${html}
    </section>
  `;
}

function renderTrapPatterns(traps) {
  if (!Array.isArray(traps) || !traps.length) return '';
  // Group by module
  const byModule = {};
  traps.forEach(t => { (byModule[t.module || 'other'] ||= []).push(t); });
  const html = Object.entries(byModule).map(([mod, list]) => `
    <details class="trap-group">
      <summary><strong>${esc(mod)}</strong> (${list.length})</summary>
      <ul class="trap-list">
        ${list.map(t => `
          <li>
            <p><strong>${esc(t.name || '')}</strong> — ${esc(t.description || '')}</p>
            ${t.wrong_example ? `<p class="wrong" lang="ja">✗ ${esc(t.wrong_example)}</p>` : ''}
            ${t.correct_example ? `<p class="right" lang="ja">✓ ${esc(t.correct_example)}</p>` : ''}
            ${t.defense ? `<p class="muted small"><em>Defense:</em> ${esc(t.defense)}</p>` : ''}
          </li>
        `).join('')}
      </ul>
    </details>
  `).join('');
  return `
    <section class="strategy-block">
      <h3>T2 · Trap-pattern catalog (${traps.length} traps)</h3>
      ${html}
    </section>
  `;
}

function renderTechniques(techs) {
  if (!Array.isArray(techs) || !techs.length) return '';
  return `
    <section class="strategy-block">
      <h3>T3 · Test-taking techniques (${techs.length})</h3>
      <ul class="techniques-list">
        ${techs.map(t => `
          <li>
            <p><strong>${esc(t.title_en || t.name || '')}</strong>${t.title_ja ? ` <span class="muted small" lang="ja">${esc(t.title_ja)}</span>` : ''}</p>
            <p>${esc(t.description || '')}</p>
            ${t.applies_to?.length ? `<p class="muted small">Applies to: ${t.applies_to.map(esc).join(', ')}</p>` : ''}
            ${t.rationale ? `<p class="muted small"><em>Why:</em> ${esc(t.rationale)}</p>` : ''}
            ${t.warning ? `<p class="warning"><em>⚠ Warning:</em> ${esc(t.warning)}</p>` : ''}
          </li>
        `).join('')}
      </ul>
    </section>
  `;
}

function renderScoreBreakdown(sb) {
  if (!sb || typeof sb !== 'object') return '';
  const sec = sb.sections || {};
  const total = sb.total_score || {};
  const bands = sb.diagnostic_band || {};
  return `
    <section class="strategy-block">
      <h3>T4 · Score breakdown</h3>
      <p class="muted small">${esc(sb.scoring_system || '')}</p>
      <table class="score-table">
        <thead><tr><th>Section</th><th>Max</th><th>Pass min</th></tr></thead>
        <tbody>
          ${Object.entries(sec).map(([k, s]) => `
            <tr>
              <td>${esc(s.label || k)}</td>
              <td>${esc(s.max_score)}</td>
              <td>${esc(s.pass_min)}</td>
            </tr>
          `).join('')}
          <tr><td><strong>Total</strong></td><td><strong>${esc(total.max_score)}</strong></td><td><strong>${esc(total.pass_min)}</strong></td></tr>
        </tbody>
      </table>
      ${total.rule ? `<p class="muted small"><strong>Rule:</strong> ${esc(total.rule)}</p>` : ''}
      ${sb.scaling_explanation ? `<p class="muted small"><strong>Scaling:</strong> ${esc(sb.scaling_explanation)}</p>` : ''}
      <h4>Diagnostic bands</h4>
      <ul class="diag-bands">
        ${Object.entries(bands).map(([band, desc]) => `
          <li><strong>${esc(band)}:</strong> ${esc(desc)}</li>
        `).join('')}
      </ul>
    </section>
  `;
}

function renderDiagnostic(diag) {
  if (!diag || !Array.isArray(diag.diagnostic_areas)) return '';
  return `
    <section class="strategy-block">
      <h3>T5 · Diagnostic + drill recommendations</h3>
      <ul class="diagnostic-list">
        ${diag.diagnostic_areas.map(a => `
          <li>
            <p><strong>${esc(a.area)}</strong></p>
            ${a.diagnostic_questions?.length ? `<p class="muted small">Diagnostic: ${a.diagnostic_questions.map(esc).join('; ')}</p>` : ''}
            ${a.drill_recommendation ? `<p>${esc(a.drill_recommendation)}</p>` : ''}
            ${a.module_pointers?.length ? `<p class="muted small">References: ${a.module_pointers.map(esc).join(', ')}</p>` : ''}
          </li>
        `).join('')}
      </ul>
      ${diag.drill_methodology?.length ? `
        <h4>Drill methodology</h4>
        <ol>${diag.drill_methodology.map(s => `<li>${esc(s)}</li>`).join('')}</ol>
      ` : ''}
    </section>
  `;
}

function renderMetaStrategy(meta) {
  if (!meta || typeof meta !== 'object') return '';
  return `
    <section class="strategy-block">
      <h3>T6 · Meta-strategy</h3>
      ${meta.five_minute_summary?.length ? `
        <h4>Five-minute summary</h4>
        <ol>${meta.five_minute_summary.map(s => `<li>${esc(s)}</li>`).join('')}</ol>
      ` : ''}
      ${meta.study_distribution_recommendation ? `
        <h4>Study distribution</h4>
        <ul>${Object.entries(meta.study_distribution_recommendation).map(([k,v]) => `<li><strong>${esc(k)}:</strong> ${esc(v)}</li>`).join('')}</ul>
      ` : ''}
      ${meta.two_week_drill_schedule?.length ? `
        <details>
          <summary><strong>Fourteen-day drill schedule</strong></summary>
          <ol>${meta.two_week_drill_schedule.map(d => `<li><strong>Day ${esc(d.day)}:</strong> ${esc(d.focus)} <span class="muted small">(${esc(d.minutes)} min)</span></li>`).join('')}</ol>
        </details>
      ` : ''}
      ${meta.exam_day_checklist?.length ? `
        <h4>Exam-day checklist</h4>
        <ul>${meta.exam_day_checklist.map(s => `<li>${esc(s)}</li>`).join('')}</ul>
      ` : ''}
    </section>
  `;
}

export async function renderStrategy(container /*, params */) {
  container.innerHTML = `<p class="muted small">Loading test strategy…</p>`;
  const s = await loadStrategy();
  if (!s) {
    container.innerHTML = `<article class="strategy-page"><p>Could not load test-strategy data. Please try again.</p></article>`;
    return;
  }
  container.innerHTML = `
    <article class="strategy-page">
      <a class="back-link" href="#/home">← Back home</a>
      <h2>JLPT N5 · Test-taking strategy</h2>
      <p class="muted small">${esc(s.source_notes || '')}</p>
      <!-- IMP-WAVE-P4-T6 (2026-05-11): focused entry-point into the
           printable exam-day prep page (extracts meta_strategy into
           an actionable checklist). -->
      <p>
        <a href="#/examday" class="btn-secondary" style="text-decoration:none">📋 Open exam-day prep checklist →</a>
        ·
        <a href="#/weakareas" style="margin-left:8px">Weak-area diagnostic →</a>
      </p>
      ${renderSectionTiming(s.section_timing)}
      ${renderTrapPatterns(s.trap_patterns)}
      ${renderTechniques(s.techniques)}
      ${renderScoreBreakdown(s.score_breakdown)}
      ${renderDiagnostic(s.diagnostic_drills)}
      ${renderMetaStrategy(s.meta_strategy)}
      <p class="muted small">Schema version ${esc(s.schema_version)} · last updated ${esc(s.last_updated)}</p>
    </article>
  `;
}
