// IMP-008 / IMP-031 (audit round-3): wrong-answer history view.
//
// Renders the most-recent 200 wrong answers from storage.getWrongHistory()
// at #/missed. Each row shows: timestamp · pattern label · user's wrong
// answer · the correct answer · link back to the pattern detail page.
//
// "Clear history" button wipes the rolling log (it does NOT touch
// FSRS-4 schedule or test results - only the browsable trail). Same
// interaction model as Anki's Browser view filtered by "again".
import * as storage from './storage.js';
import { t } from './i18n.js';

let grammarIndex = null;

async function loadGrammar() {
  if (grammarIndex) return;
  const r = await fetch('data/grammar.json');
  if (!r.ok) return;
  const d = await r.json();
  grammarIndex = new Map((d.patterns || []).map(p => [p.id, p]));
}

function fmtDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (isNaN(d.getTime())) return '';
  const today = new Date();
  const sameDay = d.toDateString() === today.toDateString();
  if (sameDay) {
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  const yest = new Date();
  yest.setDate(yest.getDate() - 1);
  if (d.toDateString() === yest.toDateString()) {
    return t('meta.yesterday') + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  return d.toLocaleDateString();
}

function fmtAnswer(v) {
  if (v == null) return '<em class="muted">(no answer)</em>';
  if (Array.isArray(v)) return esc(v.join(' / '));
  return esc(String(v));
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

export async function renderMissed(container) {
  await loadGrammar();
  const items = storage.getWrongHistory ? storage.getWrongHistory() : [];

  if (!items.length) {
    container.innerHTML = `
      <article class="missed-page">
        <a class="back-link" href="#/review">← ${esc(t('meta.back_to_review'))}</a>
        <h2>${esc(t('meta.wrong_answer_history'))}</h2>
        <div class="placeholder">
          <p>${esc(t('meta.no_misses'))}</p>
        </div>
      </article>
    `;
    return;
  }

  // Group by date for skim-ability.
  const byDate = new Map();
  for (const r of items) {
    const day = (new Date(r.ts)).toDateString();
    if (!byDate.has(day)) byDate.set(day, []);
    byDate.get(day).push(r);
  }

  let groupsHtml = '';
  for (const [day, rows] of byDate) {
    const rowsHtml = rows.map(r => {
      const p = grammarIndex?.get(r.patternId);
      const label = p ? p.pattern : (r.patternId || '(unknown pattern)');
      return `
        <li class="missed-row">
          <div class="missed-row-meta">
            <span class="missed-row-time muted small">${esc(fmtDate(r.ts))}</span>
            <span class="missed-row-source muted small">${esc(r.source || 'test')}</span>
          </div>
          <div class="missed-row-pattern">
            <a href="#/learn/${encodeURIComponent(r.patternId || '')}" lang="ja">${esc(label)}</a>
          </div>
          <div class="missed-row-answers">
            <p><strong class="muted small">${esc(t('meta.you_label'))}:</strong> <span class="missed-wrong" lang="ja">${fmtAnswer(r.wrongAnswer)}</span></p>
            <p><strong class="muted small">${esc(t('meta.correct_label'))}:</strong> <span class="missed-right" lang="ja">${fmtAnswer(r.correctAnswer)}</span></p>
          </div>
        </li>
      `;
    }).join('');
    groupsHtml += `
      <section class="missed-day-group">
        <header class="section-label">
          <span class="section-label-text">${esc(day)}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ul class="missed-list">${rowsHtml}</ul>
      </section>
    `;
  }

  container.innerHTML = `
    <article class="missed-page">
      <a class="back-link" href="#/review">← ${esc(t('meta.back_to_review'))}</a>
      <h2>${esc(t('meta.wrong_answer_history'))}</h2>
      <p class="page-lede">
        ${esc(t('meta.most_recent_misses').replace('${n}', items.length))}
      </p>
      ${groupsHtml}
      <div class="missed-actions">
        <button id="missed-clear" class="btn-danger">${esc(t('meta.clear_history'))}</button>
      </div>
    </article>
  `;
  document.getElementById('missed-clear')?.addEventListener('click', () => {
    if (!confirm(t('meta.clear_confirm'))) return;
    storage.clearWrongHistory();
    renderMissed(container);
  });
}
