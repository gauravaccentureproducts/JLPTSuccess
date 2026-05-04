// Drill mode (SRS-light) per spec §5.8.
// Reads patterns due today (nextDue <= now), pulls questions from those patterns,
// and runs a session with IMMEDIATE feedback per question (not batched).
import { renderJa } from './furigana.js';
import * as storage from './storage.js';

let questionBank = null;
let grammarIndex = null;

let session = null;
let view = 'setup'; // 'setup' | 'drilling' | 'finished'

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

export async function renderDrill(container) {
  // Stale 'finished' state reset: if the user completed a drill session,
  // navigated away, and clicked "Drill" again, give them fresh setup.
  // Mid-session ('drilling' state) is preserved so the user can resume.
  if (view === 'finished') {
    view = 'setup';
    session = null;
  }
  if (view === 'drilling' && session) return renderDrilling(container);
  if (view === 'finished' && session) return renderFinished(container);
  return renderSetup(container);
}

// ---------- Setup ----------
async function renderSetup(container) {
  view = 'setup';
  await Promise.all([loadBank(), loadGrammarIndex()]);
  const dueIds = storage.getDuePatternIds();
  const allEntries = Object.entries(storage.getHistory());
  const totalInQueue = allEntries.filter(([, v]) => v.srsBox && v.srsBox !== 'graduated').length;
  const graduatedCount = allEntries.filter(([, v]) => v.srsBox === 'graduated').length;

  if (dueIds.length === 0) {
    container.innerHTML = `
      <h2>Drill</h2>
      <div class="placeholder">
        <p><strong>No patterns due right now.</strong></p>
        <p>Patterns enter Drill the moment you miss them in a Test or Diagnostic. Once in Drill, they reappear at <strong>1d / 3d / 7d / 14d</strong> intervals - graduate after 4 consecutive correct answers.</p>
        <p class="muted">Queue: <strong>${totalInQueue}</strong> pending · <strong>${graduatedCount}</strong> graduated</p>
        <p style="margin-top:24px"><a href="#/test" class="btn-primary" style="text-decoration:none">Take a Test →</a></p>
      </div>
    `;
    return;
  }

  // Sample 5-10 questions from due patterns. Prefer questions for missed patterns.
  const sampled = sampleDrillQuestions(dueIds, questionBank, 10);

  if (sampled.length === 0) {
    container.innerHTML = `
      <h2>Drill</h2>
      <div class="placeholder">
        <p><strong>${dueIds.length}</strong> pattern(s) due, but no questions exist for them yet.</p>
        <p class="muted">Add questions for these patterns to <code>data/questions.json</code>.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <h2>Drill</h2>
    <div class="drill-setup">
      <div class="drill-stats">
        <div class="stat-card weak"><div class="stat-num">${dueIds.length}</div><div class="stat-label">Due today</div></div>
        <div class="stat-card neutral"><div class="stat-num">${totalInQueue}</div><div class="stat-label">In queue</div></div>
        <div class="stat-card mastered"><div class="stat-num">${graduatedCount}</div><div class="stat-label">Graduated</div></div>
      </div>
      <p>Drill session: <strong>${sampled.length}</strong> question(s) from due patterns. You'll get feedback after each question. Correct answers advance the SRS box (1d → 3d → 7d → 14d → graduated). A wrong answer resets the pattern to the 1-day box.</p>
      <button id="start-drill" class="btn-primary">Start Drill</button>
    </div>
  `;

  document.getElementById('start-drill').addEventListener('click', () => {
    session = {
      questions: sampled,
      currentIdx: 0,
      answers: {},        // qid -> {answer, isCorrect, recorded}
      startedAt: new Date().toISOString(),
    };
    view = 'drilling';
    renderDrilling(container);
  });
}

function sampleDrillQuestions(dueIds, bank, max) {
  const dueSet = new Set(dueIds);
  const candidates = bank.filter(q => dueSet.has(q.grammarPatternId));
  shuffle(candidates);
  // Sample at most one question per pattern in the first pass, then top up.
  const seen = new Set();
  const first = [];
  for (const q of candidates) {
    if (!seen.has(q.grammarPatternId)) {
      first.push(q);
      seen.add(q.grammarPatternId);
    }
  }
  const rest = candidates.filter(q => !first.includes(q));
  return [...first, ...rest].slice(0, max);
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// ---------- Drilling ----------
function renderDrilling(container) {
  const total = session.questions.length;
  const idx = session.currentIdx;
  const q = session.questions[idx];
  const answer = session.answers[q.id];
  const showingFeedback = !!answer;

  const pattern = grammarIndex.get(q.grammarPatternId);
  const patternLabel = pattern ? pattern.pattern : q.grammarPatternId;

  let answerHtml = '';
  if (q.type === 'mcq' || q.type === 'dropdown') {
    answerHtml = renderChoices(q, answer);
  } else if (q.type === 'sentence_order') {
    answerHtml = renderSentenceOrder(q, answer);
  }

  const feedbackHtml = showingFeedback ? renderFeedback(q, answer) : '';
  const ready = isAnswered(q, answer);
  const checkHint = !showingFeedback && !ready
    ? (() => {
        const hint = q.type === 'sentence_order'
          ? 'Tap the tiles in order to build the sentence, then click Check Answer.'
          : q.type === 'text_input'
            ? 'Type your answer in the box, then click Check Answer.'
            : 'Pick a choice, then click Check Answer.';
        return `<p class="check-answer-hint">${hint}</p>`;
      })()
    : '';
  const buttonHtml = showingFeedback
    ? `<button id="next-drill" class="btn-primary">${idx === total - 1 ? 'Finish Drill' : 'Next Question →'}</button>`
    : `${checkHint}<button id="check-answer" class="btn-primary" ${ready ? '' : 'disabled'} title="${ready ? 'Check your answer' : 'Answer the question first'}">Check Answer</button>`;

  container.innerHTML = `
    <div class="drill-session">
      <div class="drill-header">
        <span>Drill · Question <strong>${idx + 1}</strong> of <strong>${total}</strong></span>
        <span class="pattern-tag">Pattern: ${esc(patternLabel)}</span>
      </div>
      <div class="progress-bar"><div style="width:${((idx + (showingFeedback ? 1 : 0.5)) / total) * 100}%"></div></div>

      <article class="question-card">
        <p class="prompt">${esc(q.prompt_ja || '')}</p>
        ${q.question_ja ? `<p class="question">${renderJa(q.question_ja)}</p>` : ''}
        ${answerHtml}
        ${feedbackHtml}
      </article>

      <div class="test-nav">${buttonHtml}</div>
    </div>
  `;

  // Wire handlers
  if (!showingFeedback) {
    container.querySelectorAll('[data-choice]').forEach(el => {
      el.addEventListener('click', () => {
        if (session.answers[q.id]) return; // locked after feedback
        session.draftAnswer = el.dataset.choice;
        session.questions[idx]._draft = el.dataset.choice;
        renderDrilling(container);
      });
    });
    container.querySelectorAll('[data-tile-add]').forEach(el => {
      el.addEventListener('click', () => addTile(q, el.dataset.tileAdd, container));
    });
    container.querySelectorAll('[data-tile-remove]').forEach(el => {
      el.addEventListener('click', () => removeTile(q, parseInt(el.dataset.tileRemove, 10), container));
    });
    document.getElementById('check-answer')?.addEventListener('click', () => checkAnswer(q, container));
  } else {
    document.getElementById('next-drill')?.addEventListener('click', () => advance(container));
  }
}

function renderChoices(q, answer) {
  const draft = answer ? answer.answer : q._draft;
  const items = (q.choices || []).map(c => {
    let cls = 'choice-button';
    if (answer) {
      // Locked feedback view
      if (c === q.correctAnswer) cls += ' correct-choice';
      if (answer.answer === c && c !== q.correctAnswer) cls += ' wrong-choice';
    } else if (draft === c) {
      cls += ' selected';
    }
    return `<button type="button" data-choice="${esc(c)}" class="${cls}" ${answer ? 'disabled' : ''}>${renderJa(c)}</button>`;
  }).join('');
  return `<div class="choice-grid">${items}</div>`;
}

function renderSentenceOrder(q, answer) {
  const order = (answer ? answer.answer : (q._draft || []));
  const remaining = (q.tiles || []).filter(t => !order.includes(t));
  const orderedHtml = order.length
    ? order.map((t, i) => {
        let cls = 'tile ordered';
        if (answer) {
          const correctAt = q.correctOrder?.[i] === t;
          cls = `tile ordered ${correctAt ? 'correct-tile' : 'wrong-tile'}`;
        }
        return `<button type="button" ${answer ? 'disabled' : `data-tile-remove="${i}"`} class="${cls}">${renderJa(t)}</button>`;
      }).join('')
    : '<span class="tile-placeholder">Click tiles below to build the sentence</span>';
  const remainingHtml = remaining.map(t =>
    `<button type="button" ${answer ? 'disabled' : `data-tile-add="${esc(t)}"`} class="tile">${renderJa(t)}</button>`
  ).join('');
  return `
    <div class="sentence-order">
      <div class="ordered-tray">${orderedHtml}</div>
      <div class="tile-pool">${remainingHtml}</div>
    </div>
  `;
}

function isAnswered(q, answer) {
  if (answer) return true;
  if (q.type === 'sentence_order') {
    return Array.isArray(q._draft) && q._draft.length === (q.tiles?.length || 0);
  }
  return q._draft !== undefined && q._draft !== null && q._draft !== '';
}

function addTile(q, tile, container) {
  if (!q._draft) q._draft = [];
  if (q._draft.includes(tile)) return;
  q._draft.push(tile);
  renderDrilling(container);
}

function removeTile(q, idx, container) {
  if (!Array.isArray(q._draft)) return;
  q._draft.splice(idx, 1);
  renderDrilling(container);
}

function gradeQuestion(q, draft) {
  if (q.type === 'sentence_order') {
    if (!Array.isArray(draft)) return false;
    const correct = q.correctOrder || [];
    if (draft.length !== correct.length) return false;
    return draft.every((t, i) => t === correct[i]);
  }
  return draft === q.correctAnswer;
}

function checkAnswer(q, container) {
  const draft = q._draft;
  const isCorrect = gradeQuestion(q, draft);
  session.answers[q.id] = { answer: draft, isCorrect, recorded: false };

  // Persist to SRS state
  storage.recordDrillResponse(q.grammarPatternId, isCorrect);
  session.answers[q.id].recorded = true;

  renderDrilling(container);
}

function renderFeedback(q, answer) {
  const isCorrect = answer.isCorrect;
  const pattern = grammarIndex.get(q.grammarPatternId);
  const distractor = !isCorrect && q.distractor_explanations && typeof answer.answer === 'string'
    ? q.distractor_explanations[answer.answer]
    : null;
  const updatedEntry = storage.getPatternEntry(q.grammarPatternId);
  const newBox = updatedEntry?.srsBox || '?';
  const consec = updatedEntry?.consecutiveCorrect ?? 0;

  let advanceMsg = '';
  if (isCorrect) {
    if (newBox === 'graduated') {
      advanceMsg = `<strong class="graduated">Graduated.</strong> Pattern mastered.`;
    } else {
      advanceMsg = `Advanced to <strong>${newBox}</strong> box. ${consec}/4 consecutive correct.`;
    }
  } else {
    advanceMsg = `Reset to the <strong>1d</strong> box. This pattern returns tomorrow.`;
  }

  return `
    <div class="drill-feedback ${isCorrect ? 'correct' : 'incorrect'}">
      <div class="feedback-headline">${isCorrect ? 'Correct' : 'Wrong'}</div>
      ${q.explanation_en ? `<p class="feedback-explanation">${esc(q.explanation_en)}</p>` : ''}
      ${distractor ? `<p class="feedback-distractor"><em>Why your choice was off:</em> ${esc(distractor)}</p>` : ''}
      <p class="feedback-srs">${advanceMsg}</p>
      ${pattern ? `<p class="feedback-pattern">Pattern: <a href="#/learn/${encodeURIComponent(pattern.id)}">${esc(pattern.pattern)}</a></p>` : ''}
    </div>
  `;
}

function advance(container) {
  if (session.currentIdx === session.questions.length - 1) {
    view = 'finished';
    renderFinished(container);
    return;
  }
  session.currentIdx += 1;
  renderDrilling(container);
}

// ---------- Finished ----------
function renderFinished(container) {
  const total = session.questions.length;
  const correct = Object.values(session.answers).filter(a => a.isCorrect).length;
  const incorrect = total - correct;

  // Per-pattern summary: which advanced, which reset
  const byPattern = new Map();
  for (const q of session.questions) {
    const ans = session.answers[q.id];
    if (!byPattern.has(q.grammarPatternId)) byPattern.set(q.grammarPatternId, { right: 0, wrong: 0 });
    const p = byPattern.get(q.grammarPatternId);
    if (ans?.isCorrect) p.right++; else p.wrong++;
  }

  const patternRows = [...byPattern.entries()].map(([pid, counts]) => {
    const p = grammarIndex.get(pid);
    const entry = storage.getPatternEntry(pid);
    const box = entry?.srsBox === 'graduated' ? '★ graduated' : (entry?.srsBox || '-');
    return `
      <li>
        <span class="pat-name">${esc(p?.pattern || pid)}</span>
        <span class="pat-stats">${counts.right} right · ${counts.wrong} wrong</span>
        <span class="pat-box">${esc(box)}</span>
      </li>
    `;
  }).join('');

  container.innerHTML = `
    <div class="drill-finished">
      <h2>Drill complete</h2>
      <div class="score-summary">
        <div class="score-headline">
          <span class="score-big">${correct}/${total}</span>
        </div>
        <div class="score-meta">
          <span class="score-correct">${correct} correct</span>
          <span class="score-incorrect">${incorrect} incorrect</span>
        </div>
      </div>

      <h3>Pattern updates</h3>
      <ul class="pattern-summary-list">${patternRows}</ul>

      <div class="test-nav">
        <button id="drill-again" class="btn-primary">Drill again</button>
        <button id="drill-back">Back to Learn</button>
      </div>
    </div>
  `;

  document.getElementById('drill-again')?.addEventListener('click', () => {
    session = null;
    view = 'setup';
    renderSetup(container);
  });
  document.getElementById('drill-back')?.addEventListener('click', () => {
    location.hash = '#/learn';
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
