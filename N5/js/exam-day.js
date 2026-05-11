// IMP-WAVE-P4-T6 (UI audit fix, 2026-05-11): exam-day prep page.
//
// Surfaces the meta_strategy block from data/test_strategy.json
// (five-minute_summary + exam_day_checklist + two_week_drill_schedule
// + study_distribution_recommendation) as an actionable pre-exam
// prep checklist. Route: #/examday.
//
// The data was already in test_strategy.json but only reachable
// via the static /strategy page that lists everything in one
// scroll. This page extracts the exam-day-specific subset into a
// focused, printable view so users can use it as a literal
// pre-exam checklist on the day of the test.
//
// Public API:
//   await renderExamDay(container)

import { t } from './i18n.js';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c]));

let _strategyCache = null;
async function loadStrategy() {
  if (_strategyCache) return _strategyCache;
  try {
    const r = await fetch('data/test_strategy.json');
    if (!r.ok) return null;
    _strategyCache = await r.json();
    return _strategyCache;
  } catch (e) {
    console.warn('[exam-day] load failed:', e);
    return null;
  }
}

export async function renderExamDay(container) {
  container.innerHTML = `<p class="muted small">Loading exam-day prep…</p>`;
  const d = await loadStrategy();
  if (!d || !d.meta_strategy) {
    container.innerHTML = `<article class="exam-day-page"><p>Couldn't load exam-day data. Please retry.</p></article>`;
    return;
  }
  const ms = d.meta_strategy;
  const summary    = ms.five_minute_summary || [];
  const checklist  = ms.exam_day_checklist || [];
  const schedule   = ms.two_week_drill_schedule || [];
  const studyDist  = ms.study_distribution_recommendation || {};
  const exam = (d.section_timing && d.section_timing.exam_structure) || {};

  container.innerHTML = `
    <article class="exam-day-page">
      <a class="back-link" href="#/strategy">← Back to Strategy</a>
      <h2>JLPT N5 — Exam-Day Prep</h2>
      <p class="page-lede">
        Print this page, or pull it up on your phone the morning of the test.
        Compact, actionable, sourced from <code>data/test_strategy.json</code>.
      </p>

      <section class="exam-day-callout">
        <h3>5-minute pre-exam summary</h3>
        <ul class="exam-day-list">
          ${summary.map(s => `<li>${esc(s)}</li>`).join('')}
        </ul>
      </section>

      <section class="exam-day-callout exam-day-checklist-section">
        <h3>📋 Day-of-exam checklist</h3>
        <ul class="exam-day-checklist">
          ${checklist.map(c => `<li><label><input type="checkbox" class="exam-check"> ${esc(c)}</label></li>`).join('')}
        </ul>
        <p class="muted small">Your checks are saved locally so they survive page reloads.</p>
      </section>

      ${exam.section_1 ? `
        <section class="exam-day-callout">
          <h3>Exam structure at a glance</h3>
          <table class="category-table">
            <thead>
              <tr><th>Section</th><th>Duration</th><th>Questions</th><th>Score min</th><th>Score max</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>${esc(exam.section_1.name || 'Section 1')}</td>
                <td>${esc(String(exam.section_1.total_minutes || ''))} min</td>
                <td>${esc(String(exam.section_1.total_questions || ''))}</td>
                <td>${esc(String(exam.section_1.score_min_required || ''))}</td>
                <td>${esc(String(exam.section_1.score_max || ''))}</td>
              </tr>
              <tr>
                <td>${esc(exam.section_2?.name || 'Section 2')}</td>
                <td>${esc(String(exam.section_2?.total_minutes || ''))} min</td>
                <td>${esc(String(exam.section_2?.total_questions || ''))}</td>
                <td>${esc(String(exam.section_2?.score_min_required || ''))}</td>
                <td>${esc(String(exam.section_2?.score_max || ''))}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr><th>Total to pass</th><th colspan="3"></th><th>≥ ${esc(String(exam.pass_threshold_total || 80))} / ${esc(String(exam.pass_threshold_total_max || 180))}</th></tr>
            </tfoot>
          </table>
          ${exam.section_minimums_rule ? `<p class="muted small">${esc(exam.section_minimums_rule)}</p>` : ''}
        </section>
      ` : ''}

      ${Object.keys(studyDist).length ? `
        <section class="exam-day-callout">
          <h3>Recommended study-time distribution</h3>
          <ul class="exam-day-list">
            ${Object.entries(studyDist).map(([k, v]) => `<li><strong>${esc(k)}</strong>: ${esc(v)}</li>`).join('')}
          </ul>
        </section>
      ` : ''}

      ${schedule.length ? `
        <section class="exam-day-callout">
          <h3>14-day drill schedule</h3>
          <p class="muted small">Use the 14 days before exam day to cycle through these focused sessions:</p>
          <table class="category-table">
            <thead>
              <tr><th>Day</th><th>Focus</th><th>Minutes</th></tr>
            </thead>
            <tbody>
              ${schedule.map(s => `<tr><td>Day ${esc(String(s.day))}</td><td>${esc(s.focus)}</td><td>${esc(String(s.minutes || ''))}</td></tr>`).join('')}
            </tbody>
          </table>
        </section>
      ` : ''}

      <p class="muted small" style="margin-top:24px">
        <a href="#/strategy">See full strategy bank →</a>
        ·
        <a href="#/weakareas">View your weak-area diagnostic →</a>
      </p>
    </article>
  `;

  // Persist the day-of-exam checkbox state so the page is usable as
  // a live checklist on exam morning.
  const STORAGE_KEY = 'jlpt-n5-tutor:examDayChecks';
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch { saved = {}; }
  container.querySelectorAll('.exam-check').forEach((cb, idx) => {
    cb.checked = !!saved[idx];
    cb.addEventListener('change', () => {
      saved[idx] = cb.checked;
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(saved)); } catch {}
    });
  });
}
