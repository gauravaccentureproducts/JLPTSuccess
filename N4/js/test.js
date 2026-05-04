// Chapter 2 - Test. Auto-graded MCQ + dropdown + sentence_order + text_input.
// Per spec §5.3, §5.4, §6.2, §6.6 + Brief §2.10.
import { renderJa } from './furigana.js';
import { matchesAnswer, normalizeAnswer } from './normalize.js';
import * as storage from './storage.js';

let session = null;
let view = 'setup'; // 'setup' | 'attempting' | 'results'
let lastResults = null;

let questionBank = null;
let grammarIndex = null;

async function loadBank() {
  if (questionBank) return questionBank;
  const res = await fetch('data/questions.json');
  if (!res.ok) throw new Error(`Failed to load questions.json: ${res.status}`);
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

export async function renderTest(container, params) {
  // State reset on navigation back to bare #/test from elsewhere. If the
  // user finished a test, navigated away (Learn / Drill / etc.), and then
  // clicks "Test" in the nav, they expect a fresh setup — not the stale
  // results page from earlier. Preserve mid-attempt state (view='attempting')
  // because a user navigating away mid-test probably wants to resume.
  if (!params && view === 'results') {
    view = 'setup';
    session = null;
    lastResults = null;
  }
  if (view === 'attempting' && session) return renderAttempting(container);
  if (view === 'results' && lastResults) return renderResults(container);
  // Deep-link: #/test/<n> starts a test with n questions directly (Brief 2 §14.1).
  if (params) {
    const n = parseInt(decodeURIComponent(params), 10);
    if ([20, 30, 50].includes(n)) {
      await loadBank();
      storage.setSettings({ lastTestLength: n });
      startTest(n, container);
      return;
    }
  }
  return renderSetup(container);
}

// ---------- Setup ----------
async function renderSetup(container) {
  view = 'setup';
  const bank = await loadBank();
  const settings = storage.getSettings();
  const lastLen = settings.lastTestLength || 20;
  const noPriorTests = (storage.getResults() || []).length === 0;

  container.innerHTML = `
    <h2>Chapter 2 - Test</h2>
    ${noPriorTests ? `
      <div class="empty-state-banner">
        <p><strong>Take your first mock test when you've covered at least lessons 1-10.</strong> If you're new, study a few patterns first - missed items will flow into Review and Daily Drill automatically.</p>
        <p><a href="#/learn">Continue learning →</a></p>
      </div>
    ` : ''}
    <p>Configure and start a new auto-graded test. The Submit button stays disabled until every question has an answer.</p>
    <div class="test-setup">
      <label class="length-picker">
        <span>Test length</span>
        <select id="test-length">
          <option value="20" ${lastLen===20?'selected':''}>20 questions</option>
          <option value="30" ${lastLen===30?'selected':''}>30 questions</option>
          <option value="50" ${lastLen===50?'selected':''}>50 questions</option>
        </select>
      </label>
      <button id="start-test" class="btn-primary">Start Test</button>
      <p class="bank-note">Question bank: <strong>${bank.length}</strong> available. Test length is capped at the bank size.</p>
    </div>
    <hr style="border:0; border-top:1px solid var(--c-border); margin:32px 0 24px;">
    <div class="test-papers-cta">
      <h3 style="margin:0 0 8px; font-weight:400;">Mock-test papers</h3>
      <p style="margin:0 0 12px; color:var(--c-muted);">Take a focused 15-question paper from a specific JLPT section (Moji / Goi / Bunpou / Dokkai). 25 papers across 4 sections, drawn from the audited <code>KnowledgeBank</code> question files.</p>
      <a class="btn-secondary" href="#/papers" style="text-decoration:none; padding:10px 18px; display:inline-block; min-height:44px; line-height:24px;">Browse papers →</a>
    </div>
  `;
  document.getElementById('start-test').addEventListener('click', () => {
    const len = parseInt(document.getElementById('test-length').value, 10);
    storage.setSettings({ lastTestLength: len });
    startTest(len, container);
  });
}

// ---------- Sampling ----------
function sampleBalanced(bank, n) {
  // Per FR-T7: max ceil(n/5) per category when n >= 8.
  const cap = n >= 8 ? Math.ceil(n / 5) : Infinity;
  const byPattern = new Map();
  for (const q of bank) {
    if (!byPattern.has(q.grammarPatternId)) byPattern.set(q.grammarPatternId, []);
    byPattern.get(q.grammarPatternId).push(q);
  }
  for (const arr of byPattern.values()) shuffle(arr);

  const out = [];
  const groups = [...byPattern.values()];
  shuffle(groups);

  // Round-robin sample, respecting cap.
  let i = 0;
  while (out.length < n && groups.some(g => g.length > 0)) {
    const grp = groups[i % groups.length];
    if (grp.length > 0 && grp.filter(q => out.includes(q)).length < cap) {
      const next = grp.shift();
      if (next) out.push(next);
    }
    i++;
    if (i > n * 50) break; // safety
  }
  return out.slice(0, Math.min(n, bank.length));
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// ---------- Start ----------
async function startTest(length, container) {
  const bank = await loadBank();
  const sampled = sampleBalanced(bank, length);
  session = {
    questions: sampled,
    answers: {},                   // qid -> answer (string for mcq/dropdown, array for sentence_order)
    tileOrders: {},                // qid -> [] for sentence_order in-progress orders
    currentIdx: 0,
    startedAt: new Date().toISOString(),
  };
  view = 'attempting';
  window.__testInProgress = true;  // Brief 2 §7.3: signals quit-prompt
  renderAttempting(container);
}

// ---------- Attempting ----------
function renderAttempting(container) {
  const total = session.questions.length;
  const q = session.questions[session.currentIdx];
  const remaining = session.questions.filter(qq => !isAnswered(qq)).length;
  const allAnswered = remaining === 0;

  let answerHtml = '';
  if (q.type === 'mcq' || q.type === 'dropdown') {
    answerHtml = renderChoices(q);
  } else if (q.type === 'sentence_order') {
    answerHtml = renderSentenceOrder(q);
  } else if (q.type === 'text_input') {
    answerHtml = renderTextInput(q);
  } else {
    answerHtml = `<p class="placeholder-inline">Unsupported question type: ${esc(q.type)}</p>`;
  }

  container.innerHTML = `
    <div class="test-attempting">
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
        <button id="submit-test" class="btn-primary"
          ${allAnswered ? '' : 'disabled'}
          title="${allAnswered ? 'Submit your test' : `Answer all questions to submit (${remaining} remaining)`}">
          ${allAnswered ? 'Submit' : `Submit (${remaining} remaining)`}
        </button>
      </div>
    </div>
  `;

  // Wire handlers
  document.getElementById('prev-q')?.addEventListener('click', () => goTo(session.currentIdx - 1, container));
  document.getElementById('next-q')?.addEventListener('click', () => goTo(session.currentIdx + 1, container));
  document.getElementById('submit-test')?.addEventListener('click', () => submitTest(container));

  // Choice / tile handlers (delegated)
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

  const textInput = container.querySelector('[data-text-input]');
  if (textInput) {
    textInput.addEventListener('input', () => {
      session.answers[q.id] = textInput.value;
      // Live update the Submit-disabled state
      const remaining = session.questions.filter(qq => !isAnswered(qq)).length;
      const allAnswered = remaining === 0;
      const submit = document.getElementById('submit-test');
      if (submit) {
        submit.disabled = !allAnswered;
        submit.textContent = allAnswered ? 'Submit' : `Submit (${remaining} remaining)`;
        submit.title = allAnswered ? 'Submit your test' : `Answer all questions to submit (${remaining} remaining)`;
      }
    });
    if (typeof session.answers[q.id] === 'string') textInput.value = session.answers[q.id];
  }
}

function isAnswered(q) {
  const a = session.answers[q.id];
  if (q.type === 'sentence_order') {
    return Array.isArray(a) && a.length === (q.tiles?.length || 0);
  }
  if (q.type === 'text_input') {
    return typeof a === 'string' && a.trim() !== '';
  }
  return a !== undefined && a !== null && a !== '';
}

function goTo(idx, container) {
  if (idx < 0 || idx >= session.questions.length) return;
  session.currentIdx = idx;
  renderAttempting(container);
}

// ---------- Question type renderers ----------
function renderChoices(q) {
  const selected = session.answers[q.id];
  const items = (q.choices || []).map(c => `
    <button type="button" data-choice="${esc(c)}" class="choice-button ${selected === c ? 'selected' : ''}">
      ${renderJa(c)}
    </button>
  `).join('');
  return `<div class="choice-grid">${items}</div>`;
}

function renderTextInput(q) {
  const value = typeof session.answers[q.id] === 'string' ? session.answers[q.id] : '';
  return `
    <div class="text-input-wrap">
      <label for="text-input-${esc(q.id)}" class="visually-hidden">Type your answer</label>
      <input
        id="text-input-${esc(q.id)}"
        type="text"
        data-text-input
        class="text-input"
        autocomplete="off"
        autocapitalize="off"
        autocorrect="off"
        spellcheck="false"
        lang="ja"
        placeholder="Type kana or romaji..."
        value="${esc(value)}">
      <p class="muted small">Accepts hiragana, katakana, or Hepburn romaji. Punctuation/whitespace ignored.</p>
    </div>
  `;
}

function renderSentenceOrder(q) {
  const order = session.answers[q.id] || [];
  const remaining = (q.tiles || []).filter(t => !order.includes(t));

  const orderedHtml = order.length
    ? order.map((t, i) => `
        <button type="button" data-tile-remove="${i}" class="tile ordered">${renderJa(t)}</button>
      `).join('')
    : '<span class="tile-placeholder">Click tiles below to build the sentence</span>';

  const remainingHtml = remaining.map(t => `
    <button type="button" data-tile-add="${esc(t)}" class="tile">${renderJa(t)}</button>
  `).join('');

  return `
    <div class="sentence-order">
      <div class="ordered-tray">${orderedHtml}</div>
      <div class="tile-pool">${remainingHtml}</div>
    </div>
  `;
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

// ---------- Submit & Grade ----------
function gradeQuestion(q, answer) {
  if (q.type === 'sentence_order') {
    if (!Array.isArray(answer)) return false;
    const correct = q.correctOrder || [];
    if (answer.length !== correct.length) return false;
    return answer.every((t, i) => t === correct[i]);
  }
  if (q.type === 'text_input') {
    const acceptable = q.acceptedAnswers || [q.correctAnswer];
    return matchesAnswer(answer, acceptable);
  }
  return answer === q.correctAnswer;
}

function submitTest(container) {
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

  const correct = responses.filter(r => r.isCorrect).length;
  const total = responses.length;
  const result = {
    timestamp: new Date().toISOString(),
    type: 'test',
    total,
    correct,
    incorrect: total - correct,
    percent: total > 0 ? Math.round((correct / total) * 100) : 0,
    responses,
  };

  storage.recordTestResponses(responses);
  storage.recordTestResult(result);

  lastResults = { result, questions: session.questions };
  view = 'results';
  window.__testInProgress = false;
  renderResults(container);
}

// ---------- Results ----------
async function renderResults(container) {
  const { result, questions } = lastResults;
  await loadGrammarIndex();

  const reviewItems = result.responses.map(r => {
    const q = questions.find(qq => qq.id === r.questionId);
    return renderReviewItem(q, r);
  }).join('');

  const weakIds = computeGapList(result.responses);
  const gapItems = weakIds.map(id => {
    const p = grammarIndex.get(id);
    const label = p ? p.pattern : id;
    return `<li><a href="#/review">${esc(label)}</a></li>`;
  }).join('');

  container.innerHTML = `
    <div class="test-results">
      <h2>Results</h2>

      <section class="score-summary">
        <div class="score-headline">
          <span class="score-big">${result.correct}/${result.total}</span>
          <span class="score-pct">${result.percent}%</span>
        </div>
        <div class="score-meta">
          <span class="score-correct">${result.correct} correct</span>
          <span class="score-incorrect">${result.incorrect} incorrect</span>
        </div>
      </section>

      <section class="answer-review">
        <h3>Answer Review</h3>
        <ol class="review-list">${reviewItems}</ol>
      </section>

      <section class="gap-list">
        <h3>Grammar Gap List</h3>
        ${gapItems
          ? `<p>Patterns flagged as weak by your rolling history (≥ 50% error AND ≥ 2 attempts):</p><ul>${gapItems}</ul>`
          : `<p>No weak patterns yet. Keep practicing - patterns are flagged after 2+ attempts with ≥ 50% error.</p>`}
      </section>

      <div class="test-nav">
        <button id="new-test" class="btn-primary">New Test</button>
        <button id="back-to-learn">Back to Learn</button>
      </div>
    </div>
  `;

  document.getElementById('new-test')?.addEventListener('click', () => {
    session = null;
    lastResults = null;
    view = 'setup';
    renderSetup(container);
  });
  document.getElementById('back-to-learn')?.addEventListener('click', () => {
    location.hash = '#/learn';
  });
}

function renderReviewItem(q, r) {
  const correctIcon = r.isCorrect ? '✓' : '✗';
  const correctClass = r.isCorrect ? 'correct' : 'incorrect';
  const userAns = formatAnswer(q, r.userAnswer);
  const correctAns = formatAnswer(q, r.correctAnswer);
  const distractor = !r.isCorrect && q.distractor_explanations && typeof r.userAnswer === 'string'
    ? q.distractor_explanations[r.userAnswer]
    : null;
  const pattern = grammarIndex?.get(q.grammarPatternId);
  const patternLabel = pattern ? pattern.pattern : q.grammarPatternId;

  return `
    <li class="review-item ${correctClass}">
      <div class="review-marker" aria-label="${r.isCorrect ? 'correct' : 'incorrect'}">${correctIcon}</div>
      <div class="review-body">
        <div class="review-question">
          ${q.question_ja ? renderJa(q.question_ja) : esc(q.prompt_ja || '')}
        </div>
        <div class="review-answers">
          <span class="answer-label">Your answer:</span>
          <span class="user-answer ${correctClass}">${userAns}</span>
          ${!r.isCorrect ? `<span class="answer-label">Correct:</span><span class="correct-answer">${correctAns}</span>` : ''}
        </div>
        ${q.explanation_en ? `<p class="review-explanation">${esc(q.explanation_en)}</p>` : ''}
        ${distractor ? `<p class="distractor-explanation"><em>Why your choice was wrong:</em> ${esc(distractor)}</p>` : ''}
        <p class="review-pattern">Pattern: <a href="#/learn/${encodeURIComponent(q.grammarPatternId)}">${esc(patternLabel)}</a></p>
      </div>
    </li>
  `;
}

function formatAnswer(q, ans) {
  if (q.type === 'sentence_order' && Array.isArray(ans)) {
    return renderJa(ans.join(' '));
  }
  return renderJa(String(ans ?? '-'));
}

function computeGapList(responses) {
  // Pull current weak list from history (already updated by submitTest).
  return [...new Set(storage.getWeakPatternIds())];
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
