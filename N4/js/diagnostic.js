// First-run diagnostic placement test per spec §5.7.
// Samples ~10 questions across high-frequency categories.
// Results SEED the weak list / Drill queue but do NOT enter the test results log
// (so the user's "Tests taken" stat stays accurate).
import { renderJa } from './furigana.js';
import * as storage from './storage.js';

let questionBank = null;
let grammarIndex = null;
let session = null;
let view = 'setup'; // 'setup' | 'attempting' | 'results'

const DEFAULT_LENGTH = 10;

async function loadBank() {
  if (questionBank) return questionBank;
  const res = await fetch('data/questions.json');
  const data = await res.json();
  questionBank = data.questions || [];
  return questionBank;
}

async function loadGrammarIndex() {
  if (grammarIndex) return grammarIndex;
  const res = await fetch('data/grammar.json');
  const data = await res.json();
  grammarIndex = new Map((data.patterns || []).map(p => [p.id, p]));
  return grammarIndex;
}

export async function renderDiagnostic(container) {
  await Promise.all([loadBank(), loadGrammarIndex()]);
  if (view === 'attempting' && session) return renderAttempting(container);
  if (view === 'results' && session) return renderResults(container);
  return renderSetup(container);
}

// ---------- Setup ----------
function renderSetup(container) {
  view = 'setup';
  const settings = storage.getSettings();
  const completed = settings.diagnosticCompleted;

  container.innerHTML = `
    <h2>Diagnostic Test</h2>
    <div class="diagnostic-setup">
      <p><strong>${DEFAULT_LENGTH} questions</strong> sampled across the highest-frequency N5 categories. The diagnostic gives you a quick map of which patterns to practice - without affecting your test score history.</p>
      <ul>
        <li>Results don't count toward "Tests taken".</li>
        <li>Missed patterns enter the Drill queue immediately.</li>
        <li>Skippable any time - you can re-take it later from the Summary tab.</li>
      </ul>
      ${completed ? `<p class="muted">You already took the diagnostic on ${formatDate(settings.lastDiagnosticDate)}. Re-taking it will replace any current SRS state for sampled patterns.</p>` : ''}
      <div class="diagnostic-actions">
        <button id="start-diagnostic" class="btn-primary">${completed ? 'Re-take Diagnostic' : 'Start Diagnostic'}</button>
        <button id="skip-diagnostic">Skip for now</button>
      </div>
    </div>
  `;

  document.getElementById('start-diagnostic').addEventListener('click', () => startDiagnostic(container));
  document.getElementById('skip-diagnostic').addEventListener('click', () => {
    storage.setSettings({ diagnosticCompleted: true });
    location.hash = '#/learn';
  });
}

function startDiagnostic(container) {
  const sampled = sampleAcrossCategories(questionBank, DEFAULT_LENGTH);
  if (sampled.length === 0) {
    container.innerHTML = `
      <h2>Diagnostic Test</h2>
      <div class="placeholder"><p>No questions available. Add to <code>data/questions.json</code> first.</p></div>
    `;
    return;
  }
  session = {
    questions: sampled,
    answers: {},
    currentIdx: 0,
    startedAt: new Date().toISOString(),
  };
  view = 'attempting';
  renderAttempting(container);
}

function sampleAcrossCategories(bank, n) {
  // Bucket questions by the pattern's category (look up via grammarIndex).
  const buckets = new Map();
  for (const q of bank) {
    const p = grammarIndex.get(q.grammarPatternId);
    const cat = p?.category || '?';
    if (!buckets.has(cat)) buckets.set(cat, []);
    buckets.get(cat).push(q);
  }
  // Shuffle within each bucket.
  for (const arr of buckets.values()) shuffle(arr);
  // Round-robin pull one per category until we hit n.
  const order = [...buckets.entries()];
  shuffle(order);
  const out = [];
  let i = 0;
  while (out.length < n && order.some(([, arr]) => arr.length > 0)) {
    const [, arr] = order[i % order.length];
    if (arr.length > 0) out.push(arr.shift());
    i++;
    if (i > n * 50) break;
  }
  return out;
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// ---------- Attempting ---------- (mirrors test.js but without record/results-log writes)
function renderAttempting(container) {
  const total = session.questions.length;
  const q = session.questions[session.currentIdx];
  const remaining = session.questions.filter(qq => !isAnswered(qq)).length;
  const allAnswered = remaining === 0;

  let answerHtml = '';
  if (q.type === 'mcq' || q.type === 'dropdown') answerHtml = renderChoices(q);
  else if (q.type === 'sentence_order') answerHtml = renderSentenceOrder(q);

  container.innerHTML = `
    <div class="test-attempting">
      <div class="diagnostic-banner">Diagnostic - results seed your weak list but don't count toward score history</div>
      <div class="test-progress">
        <div class="progress-meta">
          <span>Question <strong>${session.currentIdx + 1}</strong> of <strong>${total}</strong></span>
          <span class="answered-count">${total - remaining} / ${total} answered</span>
        </div>
        <div class="progress-bar"><div style="width:${((session.currentIdx + 1) / total) * 100}%"></div></div>
      </div>

      <article class="question-card">
        <p class="prompt">${esc(q.prompt_ja || '')}</p>
        ${q.question_ja ? `<p class="question">${renderJa(q.question_ja)}</p>` : ''}
        ${answerHtml}
      </article>

      <div class="test-nav">
        <button id="prev-q" ${session.currentIdx === 0 ? 'disabled' : ''}>← Previous</button>
        <button id="next-q" ${session.currentIdx === total - 1 ? 'disabled' : ''}>Next →</button>
        <button id="finish-diagnostic" class="btn-primary"
          ${allAnswered ? '' : 'disabled'}
          title="${allAnswered ? 'Finish diagnostic' : `${remaining} unanswered`}">
          ${allAnswered ? 'Finish Diagnostic' : `Finish (${remaining} remaining)`}
        </button>
      </div>
    </div>
  `;

  document.getElementById('prev-q')?.addEventListener('click', () => goTo(session.currentIdx - 1, container));
  document.getElementById('next-q')?.addEventListener('click', () => goTo(session.currentIdx + 1, container));
  document.getElementById('finish-diagnostic')?.addEventListener('click', () => finish(container));

  container.querySelectorAll('[data-choice]').forEach(el => {
    el.addEventListener('click', () => {
      session.answers[q.id] = el.dataset.choice;
      renderAttempting(container);
    });
  });
  container.querySelectorAll('[data-tile-add]').forEach(el => {
    el.addEventListener('click', () => addTile(q, el.dataset.tileAdd, container));
  });
  container.querySelectorAll('[data-tile-remove]').forEach(el => {
    el.addEventListener('click', () => removeTile(q, parseInt(el.dataset.tileRemove, 10), container));
  });
}

function renderChoices(q) {
  const sel = session.answers[q.id];
  return `<div class="choice-grid">${
    (q.choices || []).map(c =>
      `<button type="button" data-choice="${esc(c)}" class="choice-button ${sel === c ? 'selected' : ''}">${renderJa(c)}</button>`
    ).join('')
  }</div>`;
}

function renderSentenceOrder(q) {
  const order = session.answers[q.id] || [];
  const remaining = (q.tiles || []).filter(t => !order.includes(t));
  const orderedHtml = order.length
    ? order.map((t, i) => `<button type="button" data-tile-remove="${i}" class="tile ordered">${renderJa(t)}</button>`).join('')
    : '<span class="tile-placeholder">Click tiles below to build the sentence</span>';
  const remainingHtml = remaining.map(t => `<button type="button" data-tile-add="${esc(t)}" class="tile">${renderJa(t)}</button>`).join('');
  return `<div class="sentence-order"><div class="ordered-tray">${orderedHtml}</div><div class="tile-pool">${remainingHtml}</div></div>`;
}

function isAnswered(q) {
  const a = session.answers[q.id];
  if (q.type === 'sentence_order') return Array.isArray(a) && a.length === (q.tiles?.length || 0);
  return a !== undefined && a !== null && a !== '';
}

function goTo(idx, container) {
  if (idx < 0 || idx >= session.questions.length) return;
  session.currentIdx = idx;
  renderAttempting(container);
}

function addTile(q, tile, container) {
  if (!session.answers[q.id]) session.answers[q.id] = [];
  if (session.answers[q.id].includes(tile)) return;
  session.answers[q.id].push(tile);
  renderAttempting(container);
}
function removeTile(q, idx, container) {
  if (!Array.isArray(session.answers[q.id])) return;
  session.answers[q.id].splice(idx, 1);
  if (session.answers[q.id].length === 0) delete session.answers[q.id];
  renderAttempting(container);
}

function gradeQuestion(q, answer) {
  if (q.type === 'sentence_order') {
    if (!Array.isArray(answer)) return false;
    const correct = q.correctOrder || [];
    return answer.length === correct.length && answer.every((t, i) => t === correct[i]);
  }
  return answer === q.correctAnswer;
}

// ---------- Finish ----------
function finish(container) {
  const responses = session.questions.map(q => {
    const a = session.answers[q.id];
    return {
      questionId: q.id,
      grammarPatternId: q.grammarPatternId,
      type: q.type,
      userAnswer: a,
      correctAnswer: q.correctAnswer ?? q.correctOrder,
      isCorrect: gradeQuestion(q, a),
    };
  });

  // Diagnostic responses go through the same SRS / weak-detection pipeline as
  // tests (so missed patterns enter Drill), but do NOT add to the test results
  // log. Per spec §5.7 - "results don't count toward score history".
  storage.recordTestResponses(responses);
  // Mark settings
  storage.setSettings({
    diagnosticCompleted: true,
    lastDiagnosticDate: new Date().toISOString(),
  });

  session.responses = responses;
  view = 'results';
  renderResults(container);
}

// ---------- Results ----------
function renderResults(container) {
  const responses = session.responses;
  const total = responses.length;
  const correct = responses.filter(r => r.isCorrect).length;
  const incorrect = total - correct;
  const weakIds = [...new Set(responses.filter(r => !r.isCorrect).map(r => r.grammarPatternId))];

  const weakItems = weakIds.map(id => {
    const p = grammarIndex.get(id);
    return `<li><a href="#/learn/${encodeURIComponent(id)}">${esc(p?.pattern || id)}</a> - ${esc(p?.meaning_en || '')}</li>`;
  }).join('');

  const categoriesCovered = new Set();
  for (const q of session.questions) {
    const p = grammarIndex.get(q.grammarPatternId);
    if (p?.category) categoriesCovered.add(p.category);
  }

  container.innerHTML = `
    <h2>Diagnostic - Results</h2>
    <div class="diagnostic-banner">These results don't count toward "Tests taken". Missed patterns are queued in Drill.</div>

    <section class="score-summary">
      <div class="score-headline"><span class="score-big">${correct}/${total}</span></div>
      <div class="score-meta">
        <span class="score-correct">${correct} correct</span>
        <span class="score-incorrect">${incorrect} incorrect</span>
      </div>
      <p class="muted">Sampled ${categoriesCovered.size} categor${categoriesCovered.size === 1 ? 'y' : 'ies'} across the N5 catalog.</p>
    </section>

    ${weakIds.length > 0 ? `
      <section class="gap-list">
        <h3>Patterns to review (${weakIds.length})</h3>
        <p>These patterns missed at least once. They've entered your Drill queue at the 1-day box.</p>
        <ul>${weakItems}</ul>
        <div class="test-nav" style="justify-content:flex-start; margin-top:12px">
          <a href="#/drill" class="btn-primary" style="text-decoration:none; padding:10px 20px">Drill them now</a>
          <a href="#/review" style="padding:10px 16px">Review the lessons</a>
        </div>
      </section>
    ` : `
      <section class="gap-list"><p>No misses - strong baseline. Take the full Test in Chapter 2 to dig deeper.</p></section>
    `}

    <div class="test-nav">
      <button id="diag-back" class="btn-primary">Back to Learn</button>
    </div>
  `;

  document.getElementById('diag-back')?.addEventListener('click', () => { location.hash = '#/learn'; });
}

function formatDate(iso) {
  if (!iso) return '';
  try { return new Date(iso).toLocaleDateString(); } catch { return iso; }
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
