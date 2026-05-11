// Chapter 2 - Test. Auto-graded MCQ + dropdown + sentence_order + text_input.
// ISSUE-048 (audit round-6): page title now flows through t().
// eslint-disable-next-line no-unused-vars
import { t } from './i18n.js';
// Per spec §5.3, §5.4, §6.2, §6.6 + Brief §2.10.
import { renderJa } from './furigana.js';
import { matchesAnswer, normalizeAnswer } from './normalize.js';
import * as storage from './storage.js';

let session = null;
let view = 'setup'; // 'setup' | 'attempting' | 'results'
let lastResults = null;

let questionBank = null;
let grammarIndex = null;

// IMP-001: exam-mode timer state. The timer is only created when the user
// opts in via the Setup screen (`exam-mode` checkbox). Stored on session so
// renderAttempting can read it after re-renders, and torn down in submitTest.
let timerInterval = null;
let timerEndsAt = null;

// JLPT N5 official timing per the published exam structure:
//   文字・語彙 (Vocabulary):        25 min
//   文法・読解 (Grammar + Reading): 50 min
//   聴解     (Listening):         30 min
//   total paper-based:           105 min
// Test mode here is grammar-only (questions.json is bunpou-flavored), so a
// 60-second-per-question budget is a fair proxy for "JLPT pace" - 20 Qs
// budgets 20 min, 30 Qs budgets 30 min, 50 Qs budgets 50 min, all close to
// the official pacing. Adjustable per-Q rate stored in seconds.
const EXAM_MODE_SEC_PER_Q = 60;

// JLPT N5 pass threshold: 80/180 overall = 44.4% (and 19/60 per section).
// For test mode (variable length, grammar-only) we use a more conservative
// 60% study-target pass mark - matches Bunpro / Try! N5 study guidance.
const PASS_PERCENT = 60;

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
  // clicks "Test" in the nav, they expect a fresh setup - not the stale
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
  const lastExamMode = !!settings.examMode;

  // ISSUE-019 (audit round 3): pull live paper-manifest counts so the CTA
  // string stays in sync with reality (was hard-coded "25 papers"; actual
  // is 28). Defensive fallback for the rare case the manifest fetch fails
  // (e.g., file:// load): omit the count rather than render a stale number.
  // IMP-115 (audit round-9): also pull full_mock_papers + combined_sections
  // metadata for the Full Mock Test CTA so it accurately advertises the
  // real JLPT shape (85Q / 105min) and exposes paper-1..paper-7 selectable.
  let paperCountStr = t('meta.mock_papers');
  let fullMockPapers = null;
  try {
    const m = await fetch('data/papers/manifest.json').then(r => r.ok ? r.json() : null);
    if (m && m.totalPapers && m.totalQuestions) {
      paperCountStr = `${m.totalPapers} papers (${m.totalQuestions} questions)`;
    }
    if (m && Array.isArray(m.full_mock_papers) && m.full_mock_papers.length) {
      fullMockPapers = m.full_mock_papers;
    }
  } catch { /* keep fallback string */ }

  container.innerHTML = `
    <h2>${t('page.test')}</h2>
    ${noPriorTests ? `
      <div class="empty-state-banner">
        <p><strong>${esc(t('meta.first_mock_hint'))}</strong></p>
        <p><a href="#/learn">${esc(t('meta.continue_learning'))} →</a></p>
      </div>
    ` : ''}
    <!-- Promotional trust callout (round-9 follow-up 2026-05-07): the
         "your scores stay on this device" message is the strongest
         niche-N2 reassurance precisely at the moment a learner is
         about to submit results. Bunpro / Renshuu push results to
         their server; the callout makes the privacy claim concrete
         right where it matters most. -->
    <aside class="trust-callout" aria-label="Privacy reassurance">
      <strong>${t('trust.no_login')} · ${t('trust.no_tracking')} · ${t('trust.on_device')}</strong>
      <p>${t('trust.test_callout')}</p>
    </aside>
    <p>${esc(t('meta.test_setup_intro'))}</p>
    <div class="test-setup">
      <label class="length-picker">
        <span>${esc(t('meta.test_length'))}</span>
        <select id="test-length">
          <option value="20" ${lastLen===20?'selected':''}>20 ${esc(t('meta.questions_unit'))}</option>
          <option value="30" ${lastLen===30?'selected':''}>30 ${esc(t('meta.questions_unit'))}</option>
          <option value="50" ${lastLen===50?'selected':''}>50 ${esc(t('meta.questions_unit'))}</option>
        </select>
      </label>
      <label class="exam-mode-toggle" title="Adds a countdown timer at JLPT pace (~60 seconds per question). Auto-submits at zero.">
        <input type="checkbox" id="exam-mode" ${lastExamMode ? 'checked' : ''}>
        <span>${esc(t('test.exam_mode'))}</span>
      </label>
      <button id="start-test" class="btn-primary">${esc(t('meta.start_test'))}</button>
      <p class="bank-note">Question bank: <strong>${bank.length}</strong> available. Test length is capped at the bank size.</p>
      <p class="bank-note muted small">${esc(t('test.pass_mark'))}: <strong>${PASS_PERCENT}%</strong> (JLPT N5 study target).</p>
    </div>
    <hr style="border:0; border-top:1px solid var(--c-border); margin:32px 0 24px;">
    <div class="test-papers-cta">
      <h3 style="margin:0 0 8px; font-weight:400;">${esc(t('meta.mock_papers'))}</h3>
      <p style="margin:0 0 12px; color:var(--c-muted);">Take a focused paper from a specific JLPT section (Moji / Goi / Bunpou / Dokkai). ${paperCountStr} across 4 sections, drawn from the audited <code>KnowledgeBank</code> question files.</p>
      <a class="btn-secondary" href="#/papers" style="text-decoration:none; padding:10px 18px; display:inline-block; min-height:44px; line-height:24px;">Browse papers →</a>
    </div>
    <hr style="border:0; border-top:1px solid var(--c-border); margin:32px 0 24px;">
    <div class="test-sitting-cta">
      <h3 style="margin:0 0 8px; font-weight:400;">Full Mock Test (real JLPT N5 shape)</h3>
      <p style="margin:0 0 12px; color:var(--c-muted);">Take the entire JLPT N5 in one sitting: <strong>言語知識（文字・語彙） 30Q / 25 min</strong> → <strong>言語知識（文法）・読解 31Q / 50 min</strong> → <strong>聴解 24Q / 30 min</strong>. Total <strong>85Q / 105 min</strong> (close to the official 91Q / 105min). Each section runs at the official time budget and auto-submits at zero.${fullMockPapers ? ` ${fullMockPapers.length} papers available.` : ''}</p>
      <a class="btn-secondary" href="#/sitting" style="text-decoration:none; padding:10px 18px; display:inline-block; min-height:44px; line-height:24px;">Start full mock test →</a>
    </div>
  `;
  document.getElementById('start-test').addEventListener('click', () => {
    const len = parseInt(document.getElementById('test-length').value, 10);
    const examMode = !!document.getElementById('exam-mode')?.checked;
    storage.setSettings({ lastTestLength: len, examMode });
    startTest(len, container, { examMode });
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
async function startTest(length, container, opts = {}) {
  const bank = await loadBank();
  const sampled = sampleBalanced(bank, length);
  const examMode = !!opts.examMode;
  session = {
    questions: sampled,
    answers: {},                   // qid -> answer (string for mcq/dropdown, array for sentence_order)
    tileOrders: {},                // qid -> [] for sentence_order in-progress orders
    currentIdx: 0,
    startedAt: new Date().toISOString(),
    examMode,                       // IMP-001
    durationSec: examMode ? length * EXAM_MODE_SEC_PER_Q : null,
  };
  // IMP-001: schedule the countdown clock if exam mode is on.
  if (examMode) {
    timerEndsAt = Date.now() + session.durationSec * 1000;
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => onTimerTick(container), 1000);
  } else {
    timerEndsAt = null;
  }
  view = 'attempting';
  window.__testInProgress = true;  // Brief 2 §7.3: signals quit-prompt
  renderAttempting(container);
}

// IMP-001: timer-tick handler. Updates the visible chip; on zero, auto-submits
// without confirmation (JLPT real exams also stop dead at the bell).
function onTimerTick(container) {
  if (!timerEndsAt || view !== 'attempting') return;
  const remainingMs = timerEndsAt - Date.now();
  const chip = document.getElementById('test-timer');
  if (chip) {
    const totalSec = Math.max(0, Math.ceil(remainingMs / 1000));
    const mm = String(Math.floor(totalSec / 60)).padStart(2, '0');
    const ss = String(totalSec % 60).padStart(2, '0');
    chip.textContent = `${mm}:${ss}`;
    chip.classList.toggle('danger', totalSec <= 60);
    chip.classList.toggle('warning', totalSec > 60 && totalSec <= 300);
  }
  if (remainingMs <= 0) {
    clearInterval(timerInterval);
    timerInterval = null;
    timerEndsAt = null;
    submitTest(container);
  }
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

  // IMP-001: timer chip text - pre-render to current remaining if exam mode.
  let timerChipHtml = '';
  if (session.examMode && timerEndsAt) {
    const totalSec = Math.max(0, Math.ceil((timerEndsAt - Date.now()) / 1000));
    const mm = String(Math.floor(totalSec / 60)).padStart(2, '0');
    const ss = String(totalSec % 60).padStart(2, '0');
    const cls = totalSec <= 60 ? ' danger' : (totalSec <= 300 ? ' warning' : '');
    timerChipHtml = `<span id="test-timer" class="test-timer-chip${cls}" aria-live="polite" title="Time remaining">${mm}:${ss}</span>`;
  }

  container.innerHTML = `
    <div class="test-attempting">
      <div class="test-progress">
        <div class="progress-meta">
          <span>Question <strong>${session.currentIdx + 1}</strong> of <strong>${total}</strong></span>
          ${timerChipHtml}
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
  // IMP-001: stop the countdown if it was running.
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  const elapsedSec = session.startedAt
    ? Math.round((Date.now() - new Date(session.startedAt).getTime()) / 1000)
    : null;
  const timedOut = !!(session.examMode && timerEndsAt && Date.now() >= timerEndsAt);
  timerEndsAt = null;

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
    examMode: session.examMode || false,
    elapsedSec,
    timedOut,
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

  // IMP-002: pass / fail badge against the JLPT N5 study target.
  const passed = result.percent >= PASS_PERCENT;
  const passBadge = `
    <div class="pass-badge ${passed ? 'pass' : 'fail'}" role="status">
      ${passed
        ? `<strong>Pass</strong> · ≥ ${PASS_PERCENT}% study target`
        : `<strong>Below pass</strong> · target ${PASS_PERCENT}% (you got ${result.percent}%)`}
    </div>
  `;
  // Optional elapsed-time / timed-out indicator (IMP-001 follow-through).
  let timeChip = '';
  if (typeof result.elapsedSec === 'number') {
    const mm = Math.floor(result.elapsedSec / 60);
    const ss = String(result.elapsedSec % 60).padStart(2, '0');
    const tag = result.timedOut ? ' (auto-submitted at zero)' : '';
    timeChip = `<span class="score-time muted small">Time: ${mm}m ${ss}s${tag}</span>`;
  }

  // IMP-004: per-grammar-category breakdown. questions.json items reference
  // grammarPatternId; the grammar.json pattern carries `category` (e.g.,
  // "Particles", "Copula", "Verbs - て-form"). Aggregate correct/total per
  // category so the learner sees concretely where to focus next.
  const byCategory = new Map();  // category -> { correct, total }
  for (const r of result.responses) {
    const p = grammarIndex.get(r.grammarPatternId);
    const cat = (p && p.category) || 'Other';
    if (!byCategory.has(cat)) byCategory.set(cat, { correct: 0, total: 0 });
    const e = byCategory.get(cat);
    e.total += 1;
    if (r.isCorrect) e.correct += 1;
  }
  // Sort by lowest accuracy first (most actionable for "where to study next").
  const breakdownRows = [...byCategory.entries()]
    .sort((a, b) => (a[1].correct / a[1].total) - (b[1].correct / b[1].total))
    .map(([cat, { correct, total }]) => {
      const pct = total > 0 ? Math.round((correct / total) * 100) : 0;
      const cls = pct >= PASS_PERCENT ? 'pass' : 'fail';
      return `
        <tr class="${cls}">
          <td class="cat-name">${esc(cat)}</td>
          <td class="cat-score">${correct} / ${total}</td>
          <td class="cat-pct">${pct}%</td>
          <td class="cat-bar"><div class="cat-bar-track"><div class="cat-bar-fill" style="width:${pct}%"></div></div></td>
        </tr>
      `;
    })
    .join('');

  // IMP-026 (audit round-3): per-question-type breakdown alongside the
  // per-category one. Tells the learner whether they're tripping over
  // sentence_order vs MCQ vs text_input - useful when choosing which
  // drill mode to spend the next session on.
  const TYPE_LABELS = {
    'mcq':            'Multiple choice',
    'sentence_order': 'Sentence ordering',
    'text_input':     'Text input',
    'dropdown':       'Dropdown',
  };
  const byType = new Map();
  for (const r of result.responses) {
    const t = r.type || 'mcq';
    if (!byType.has(t)) byType.set(t, { correct: 0, total: 0 });
    const e = byType.get(t);
    e.total += 1;
    if (r.isCorrect) e.correct += 1;
  }
  const typeRows = [...byType.entries()]
    .sort((a, b) => (a[1].correct / a[1].total) - (b[1].correct / b[1].total))
    .map(([t, { correct, total }]) => {
      const pct = total > 0 ? Math.round((correct / total) * 100) : 0;
      const cls = pct >= PASS_PERCENT ? 'pass' : 'fail';
      const label = TYPE_LABELS[t] || t;
      return `
        <tr class="${cls}">
          <td class="cat-name">${esc(label)}</td>
          <td class="cat-score">${correct} / ${total}</td>
          <td class="cat-pct">${pct}%</td>
          <td class="cat-bar"><div class="cat-bar-track"><div class="cat-bar-fill" style="width:${pct}%"></div></div></td>
        </tr>
      `;
    })
    .join('');

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
          ${timeChip}
        </div>
        ${passBadge}
      </section>

      <section class="category-breakdown">
        <h3>By grammar category</h3>
        ${byCategory.size > 0 ? `
          <table class="category-table">
            <thead>
              <tr><th>Category</th><th>Score</th><th>%</th><th>Distribution</th></tr>
            </thead>
            <tbody>${breakdownRows}</tbody>
          </table>
          <p class="muted small">Categories sorted by accuracy (weakest first). Pass target ${PASS_PERCENT}%.</p>
        ` : '<p class="muted">No category metadata available for this test.</p>'}
      </section>

      <section class="category-breakdown">
        <h3>By question type</h3>
        ${byType.size > 1 ? `
          <table class="category-table">
            <thead>
              <tr><th>Type</th><th>Score</th><th>%</th><th>Distribution</th></tr>
            </thead>
            <tbody>${typeRows}</tbody>
          </table>
          <p class="muted small">Types sorted by accuracy (weakest first). Useful for picking your next drill mode.</p>
        ` : '<p class="muted small">All questions in this test were the same type - type breakdown is only meaningful when the test mixes question formats.</p>'}
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
