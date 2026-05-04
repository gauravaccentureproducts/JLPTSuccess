// Mock-test "papers" — multi-paper, category-organized practice.
//
// Surfaces the 360 audited KB questions (moji + goi + bunpou + dokkai)
// that previously sat in source-MD form without reaching learners. The
// build pipeline (tools/build_papers.py) carves them into 15-question
// papers per category and writes data/papers/manifest.json + per-paper
// JSONs.
//
// Routing:
//   #/papers                   — 4-card category index (Moji / Goi / Bunpou / Dokkai)
//   #/papers/<category>        — list of papers for that category
//   #/papers/<category>/<n>    — start the n-th paper (mock-test flow)
//
// Score persistence: per-paper localStorage keys via the storage module.

import { renderJa } from './furigana.js';
import * as storage from './storage.js';

let manifest = null;
const paperCache = new Map();   // paperId -> paper JSON (lazy-loaded)
let session = null;             // active mock-test session
let view = 'setup';              // 'setup' | 'attempting' | 'results'
let lastResults = null;

async function loadManifest() {
  if (manifest) return manifest;
  const res = await fetch('data/papers/manifest.json');
  if (!res.ok) throw new Error(`Failed to load papers manifest: ${res.status}`);
  manifest = await res.json();
  return manifest;
}

async function loadPaper(category, paperNumber) {
  const cacheKey = `${category}-${paperNumber}`;
  if (paperCache.has(cacheKey)) return paperCache.get(cacheKey);
  const res = await fetch(`data/papers/${category}/paper-${paperNumber}.json`);
  if (!res.ok) throw new Error(`Failed to load paper ${cacheKey}: ${res.status}`);
  const paper = await res.json();
  paperCache.set(cacheKey, paper);
  return paper;
}

// ---------- Per-paper localStorage helpers ----------

function paperStateKey(paperId) {
  return `jlpt-n5-tutor.paper.${paperId}`;
}

function getPaperState(paperId) {
  try {
    const raw = localStorage.getItem(paperStateKey(paperId));
    if (!raw) return { attempts: 0, bestScore: null, lastScore: null };
    return JSON.parse(raw);
  } catch {
    return { attempts: 0, bestScore: null, lastScore: null };
  }
}

function recordPaperAttempt(paperId, score, total) {
  const state = getPaperState(paperId);
  const newState = {
    attempts: (state.attempts || 0) + 1,
    bestScore: state.bestScore == null
      ? { correct: score, total }
      : (score > state.bestScore.correct ? { correct: score, total } : state.bestScore),
    lastScore: { correct: score, total, dateIso: new Date().toISOString() },
  };
  localStorage.setItem(paperStateKey(paperId), JSON.stringify(newState));
  return newState;
}

// ---------- Router entry ----------

export async function renderPapers(container, params) {
  const parts = (params || '').split('/').filter(Boolean);

  // State reset on navigation AWAY from active view.
  // `view === 'attempting' | 'results'` is meaningful only when the URL
  // points to a specific paper (#/papers/<cat>/<n>, parts.length === 2).
  // If the URL is now the index (#/papers) or a category list
  // (#/papers/<cat>), the user has navigated out of the flow — clear
  // the stale state so the requested page can render. Without this,
  // clicking "Back to <cat> papers" on the results page just re-rendered
  // the results page (the early-return below short-circuited routing).
  // Reported 2026-05-03 with screenshot of the broken back-button.
  if (parts.length < 2 && (view === 'attempting' || view === 'results')) {
    view = 'setup';
    session = null;
    lastResults = null;
  }

  // Deep-link mid-flow handling: if we're still on the active paper URL
  // (parts.length === 2) AND mid-test or mid-results, honor that.
  if (view === 'attempting' && session) return renderAttempting(container);
  if (view === 'results' && lastResults) return renderResults(container);

  if (parts.length === 0) return renderCategoryIndex(container);
  if (parts.length === 1) return renderPaperList(container, parts[0]);
  if (parts.length === 2) {
    const [cat, paperNum] = parts;
    return startPaper(container, cat, parseInt(paperNum, 10));
  }
  return renderCategoryIndex(container);
}

// ---------- View 1: category index ----------

async function renderCategoryIndex(container) {
  const m = await loadManifest();
  const cards = m.categories.map(cat => {
    const completed = cat.papers.filter(p => {
      const st = getPaperState(p.id);
      return (st.attempts || 0) > 0;
    }).length;
    return `
      <a class="paper-cat-card" href="#/papers/${esc(cat.id)}">
        <div class="paper-cat-icon" aria-hidden="true">${categoryIcon(cat.id)}</div>
        <div class="paper-cat-meta">
          <h3>${esc(cat.label)} <span class="paper-cat-ja" lang="ja">${esc(cat.label_ja)}</span></h3>
          <p class="paper-cat-desc">${esc(cat.description)}</p>
          <p class="paper-cat-stats">
            <span class="paper-stat">${cat.paperCount} papers</span>
            <span class="paper-stat-sep">·</span>
            <span class="paper-stat">${cat.questionCount} questions</span>
            <span class="paper-stat-sep">·</span>
            <span class="paper-stat">${completed} of ${cat.paperCount} attempted</span>
          </p>
        </div>
      </a>
    `;
  }).join('');

  container.innerHTML = `
    <article class="papers-index">
      <a class="back-link" href="#/test">← Back to Test</a>
      <h2>Mock-test Papers</h2>
      <p class="page-lede">${m.totalQuestions} audited JLPT N5 questions across ${m.totalPapers} papers in 4 sections. Each paper is sized to a study-session (15 questions, ~10 minutes). Scores persist locally so you can track which papers you've completed.</p>
      <div class="paper-cat-grid">${cards}</div>
      <p class="papers-foot-note">Source: <code>KnowledgeBank/{moji,goi,bunpou,dokkai}_questions_n5.md</code> — curated and native-teacher-reviewed across Pass-9 through Pass-19.</p>
    </article>
  `;
}

function categoryIcon(catId) {
  // Hairline-style icons (Zen Modern aesthetic): single letter in a circle.
  const letters = { moji: '字', goi: '語', bunpou: '法', dokkai: '読' };
  return `<span class="paper-cat-letter" lang="ja">${letters[catId] || '?'}</span>`;
}

// ---------- View 2: paper list for a category ----------

async function renderPaperList(container, categoryId) {
  const m = await loadManifest();
  const cat = m.categories.find(c => c.id === categoryId);
  if (!cat) {
    container.innerHTML = `
      <article class="papers-index">
        <a class="back-link" href="#/papers">← Back to Mock-test Papers</a>
        <h2>Unknown category</h2>
        <p>The category <code>${esc(categoryId)}</code> doesn't exist. <a href="#/papers">Return to the index.</a></p>
      </article>
    `;
    return;
  }

  const cards = cat.papers.map(p => {
    const st = getPaperState(p.id);
    const attempted = (st.attempts || 0) > 0;
    const best = st.bestScore;
    const badge = attempted
      ? `<span class="paper-badge paper-badge-done">${best ? `${best.correct}/${best.total}` : 'Done'}</span>`
      : `<span class="paper-badge paper-badge-new">New</span>`;
    return `
      <a class="paper-card" href="#/papers/${esc(cat.id)}/${p.paperNumber}">
        <div class="paper-card-num">Paper ${p.paperNumber}</div>
        <div class="paper-card-meta">
          <span class="paper-q-count">${p.questionCount} questions</span>
          <span class="paper-source-range muted">${esc(p.source_question_range)}</span>
        </div>
        ${badge}
      </a>
    `;
  }).join('');

  container.innerHTML = `
    <article class="papers-index">
      <a class="back-link" href="#/papers">← All sections</a>
      <h2>${esc(cat.label)} <span class="paper-cat-ja" lang="ja">${esc(cat.label_ja)}</span></h2>
      <p class="page-lede">${esc(cat.description)} · ${cat.paperCount} papers · ${cat.questionCount} questions total.</p>
      <div class="paper-list-grid">${cards}</div>
    </article>
  `;
}

// ---------- View 3: starting a paper (loads + transitions to attempting) ----------

async function startPaper(container, categoryId, paperNumber) {
  if (!Number.isInteger(paperNumber) || paperNumber < 1) {
    container.innerHTML = `<p>Invalid paper number.</p>`;
    return;
  }
  const paper = await loadPaper(categoryId, paperNumber);
  session = {
    paper,
    paperId: paper.id,
    categoryId,
    paperNumber,
    questions: paper.questions,
    answers: new Array(paper.questions.length).fill(null), // 0-based choice index per question, or null
    currentIdx: 0,
    submitted: false,
  };
  view = 'attempting';
  return renderAttempting(container);
}

// ---------- View 4: attempting (one question at a time) ----------

function renderAttempting(container) {
  const s = session;
  if (!s) {
    container.innerHTML = `<p>No active session. <a href="#/papers">Pick a paper.</a></p>`;
    return;
  }
  const q = s.questions[s.currentIdx];
  const total = s.questions.length;
  const answered = s.answers.filter(a => a !== null).length;

  // Passage rendering for dokkai (passage_text on the question entry)
  const passageBlock = q.passage_text
    ? `<div class="paper-passage" lang="ja">${renderJaSafe(q.passage_text)}</div>`
    : '';

  const choicesHtml = q.choices.map((choice, i) => `
    <label class="paper-choice ${s.answers[s.currentIdx] === i ? 'selected' : ''}">
      <input type="radio" name="choice" value="${i}" ${s.answers[s.currentIdx] === i ? 'checked' : ''}>
      <span class="paper-choice-letter">${i + 1}</span>
      <span class="paper-choice-text" lang="ja">${renderJaSafe(choice)}</span>
    </label>
  `).join('');

  container.innerHTML = `
    <article class="paper-attempting">
      <header class="paper-progress-bar">
        <a class="paper-quit" href="#/papers/${esc(s.categoryId)}" title="Quit and return to paper list">✕ Quit</a>
        <div class="paper-progress-info">
          <span class="paper-progress-current">Q${s.currentIdx + 1}</span>
          <span class="paper-progress-of">of ${total}</span>
          <span class="paper-progress-answered">· ${answered} answered</span>
        </div>
      </header>
      ${passageBlock}
      <div class="paper-question-stem" lang="ja">${renderJaSafe(q.stem_html)}</div>
      <form class="paper-choices" id="paper-choices-form">${choicesHtml}</form>
      <footer class="paper-controls">
        <button type="button" class="btn-secondary" id="paper-prev" ${s.currentIdx === 0 ? 'disabled' : ''}>← Previous</button>
        ${s.currentIdx === total - 1
          ? (() => {
              const remaining = total - answered;
              const allAnswered = remaining === 0;
              return `
                <div class="paper-submit-cluster">
                  ${allAnswered ? '' : `<p class="paper-submit-hint">Answer all ${total} questions to submit · <strong>${remaining}</strong> ${remaining === 1 ? 'question' : 'questions'} unanswered</p>`}
                  <button type="button" class="btn-primary" id="paper-submit" ${allAnswered ? '' : 'disabled'} title="${allAnswered ? 'Submit your paper' : `Answer all questions to submit (${remaining} remaining)`}">${allAnswered ? 'Submit paper' : `Submit paper (${remaining} remaining)`}</button>
                </div>`;
            })()
          : `<button type="button" class="btn-primary" id="paper-next">Next →</button>`}
      </footer>
    </article>
  `;

  // Wire interactions
  const form = document.getElementById('paper-choices-form');
  form.addEventListener('change', (e) => {
    if (e.target && e.target.name === 'choice') {
      s.answers[s.currentIdx] = parseInt(e.target.value, 10);
      renderAttempting(container); // re-render to update selected highlight + counts
    }
  });
  document.getElementById('paper-prev')?.addEventListener('click', () => {
    if (s.currentIdx > 0) { s.currentIdx -= 1; renderAttempting(container); }
  });
  document.getElementById('paper-next')?.addEventListener('click', () => {
    if (s.currentIdx < total - 1) { s.currentIdx += 1; renderAttempting(container); }
  });
  document.getElementById('paper-submit')?.addEventListener('click', () => {
    submitPaper(container);
  });
}

// Render Japanese without crashing on the <u> tags or other inline HTML
// the KB question stems contain. The KB intentionally uses <u>kanji</u>
// underlines for Mondai-1 reading questions; we let those through.
function renderJaSafe(html) {
  if (!html) return '';
  // Light pass: trust the KB content (already audited). renderJa() expects
  // plain text, so we emit the html directly with class="ja" wrapping.
  return `<span class="ja-text" lang="ja">${html}</span>`;
}

// ---------- Submit + results ----------

function submitPaper(container) {
  const s = session;
  let correct = 0;
  const detail = s.questions.map((q, i) => {
    const chosen = s.answers[i];
    const isRight = chosen === q.correctIndex;
    if (isRight) correct += 1;
    return {
      idx: i,
      kbSourceId: q.kbSourceId,
      stem_html: q.stem_html,
      choices: q.choices,
      correctIndex: q.correctIndex,
      chosen,
      isRight,
      rationale: q.rationale || '',
    };
  });

  const total = s.questions.length;
  recordPaperAttempt(s.paperId, correct, total);
  // Also feed into the global SRS / weak-list system for future drill targeting.
  // We synthesize a result entry per question so the existing summary tab can pick them up.
  try {
    s.questions.forEach((q, i) => {
      const passed = s.answers[i] === q.correctIndex;
      // Store under a synthetic patternId so paper-only attempts don't pollute
      // grammar-pattern stats. Use category-level bucketing.
      storage.recordAttempt?.(`paper:${s.categoryId}:${q.kbSourceId}`, passed, 'paper');
    });
  } catch {}

  lastResults = {
    paperId: s.paperId,
    paperName: s.paper.name,
    categoryId: s.categoryId,
    correct,
    total,
    detail,
  };
  view = 'results';
  session = null;
  return renderResults(container);
}

function renderResults(container) {
  const r = lastResults;
  if (!r) {
    container.innerHTML = `<p>No results to display. <a href="#/papers">Pick a paper.</a></p>`;
    return;
  }
  const pct = Math.round((r.correct / r.total) * 100);
  const verdict = pct >= 80 ? 'Great work' : pct >= 60 ? 'Solid' : pct >= 40 ? 'Keep going' : 'Review and retry';
  const reviewHtml = r.detail.map(d => `
    <li class="paper-review-item ${d.isRight ? 'review-right' : 'review-wrong'}">
      <div class="paper-review-head">
        <span class="paper-review-num">Q${d.idx + 1}</span>
        <span class="paper-review-status">${d.isRight ? '✓' : '✗'}</span>
        <span class="paper-review-source muted">${esc(d.kbSourceId)}</span>
      </div>
      <div class="paper-review-stem ja-text" lang="ja">${d.stem_html}</div>
      <ol class="paper-review-choices">
        ${d.choices.map((c, i) => {
          const cls = i === d.correctIndex ? 'choice-correct' : (i === d.chosen ? 'choice-chosen-wrong' : '');
          return `<li class="${cls}" lang="ja">${esc(c)}</li>`;
        }).join('')}
      </ol>
      ${d.rationale ? `<p class="paper-review-rationale">${esc(d.rationale)}</p>` : ''}
    </li>
  `).join('');

  container.innerHTML = `
    <article class="paper-results">
      <header class="paper-results-summary">
        <h2>${esc(r.paperName)} · Results</h2>
        <div class="paper-score-display">
          <div class="paper-score-big">${r.correct}<span class="paper-score-of">/${r.total}</span></div>
          <div class="paper-score-pct">${pct}%</div>
          <div class="paper-score-verdict">${verdict}</div>
        </div>
      </header>
      <nav class="paper-results-actions">
        <a class="btn-primary" href="#/papers/${esc(r.categoryId)}">Back to ${esc(r.categoryId)} papers</a>
        <a class="btn-secondary" href="#/papers/${esc(r.categoryId)}/${parseInt(r.paperId.split('-')[1], 10)}" id="paper-retry">Retry this paper</a>
      </nav>
      <section class="paper-review">
        <h3>Question review</h3>
        <ol class="paper-review-list">${reviewHtml}</ol>
      </section>
    </article>
  `;
  // Reset state on retry click so the next start fires cleanly.
  document.getElementById('paper-retry')?.addEventListener('click', () => {
    view = 'setup';
    lastResults = null;
  });
}

// ---------- Utility ----------

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}
