// こそあど systems page (Brief §2.5)
// Single-page reference: 4-row × 4-column grid + speaker/listener proximity
// diagram + a quick drill that asks for the right form given a row+column.
import { renderJa } from './furigana.js';

const ROWS = [
  { key: 'this', label_en: 'this (near speaker)', kana: 'こ-' },
  { key: 'that_l', label_en: "that (near listener)", kana: 'そ-' },
  { key: 'that_far', label_en: 'that (far from both)', kana: 'あ-' },
  { key: 'which', label_en: 'which / what', kana: 'ど-' },
];

const COLS = [
  { key: 'pronoun', label_en: 'Pronoun (object)', cell_en: 'this one', forms: ['これ', 'それ', 'あれ', 'どれ'] },
  { key: 'adjective', label_en: 'Adjective + Noun', cell_en: 'this + N', forms: ['この', 'その', 'あの', 'どの'] },
  { key: 'place', label_en: 'Location', cell_en: 'here / there / where', forms: ['ここ', 'そこ', 'あそこ', 'どこ'] },
  { key: 'polite', label_en: 'Polite (direction / option)', cell_en: 'this way / which way', forms: ['こちら', 'そちら', 'あちら', 'どちら'] },
];

let drillState = null;

export async function renderKosoado(container) {
  container.innerHTML = `
    <h2>Demonstratives (this / that / which)</h2>
    <p>Japanese demonstratives form a regular 4×4 grid. The first column lists pronouns (standalone), the second adjectives (always followed by a noun), the third locations, and the fourth the polite directions/options.</p>

    ${renderProximity()}
    ${renderGrid()}
    ${renderDrill()}
  `;

  wireDrill(container);
}

function renderProximity() {
  return `
    <section class="kosoado-proximity">
      <h3>Proximity</h3>
      <div class="proximity-diagram">
        <div class="prox-row">
          <div class="prox-bubble speaker">SPEAKER<br><small>こ-</small></div>
          <div class="prox-arrow">↔</div>
          <div class="prox-bubble listener">LISTENER<br><small>そ-</small></div>
          <div class="prox-arrow long">────────</div>
          <div class="prox-bubble far">FAR FROM BOTH<br><small>あ-</small></div>
        </div>
        <div class="prox-question">QUESTION (anywhere) <strong>ど-</strong></div>
      </div>
      <p class="muted small">こ- = near speaker, そ- = near listener, あ- = far from both, ど- = question.</p>
    </section>
  `;
}

function renderGrid() {
  let html = `
    <section class="kosoado-grid-section">
      <h3>Grid</h3>
      <table class="kosoado-grid">
        <thead>
          <tr>
            <th>Row →<br>↓ Column</th>
            ${COLS.map(c => `<th>${esc(c.label_en)}<br><small>${esc(c.cell_en)}</small></th>`).join('')}
          </tr>
        </thead>
        <tbody>
  `;
  ROWS.forEach((row, ri) => {
    html += `<tr><th>${esc(row.label_en)}<br><small>${esc(row.kana)}</small></th>`;
    COLS.forEach((col) => {
      html += `<td>${renderJa(col.forms[ri])}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table></section>`;
  return html;
}

function renderDrill() {
  if (!drillState) {
    return `
      <section class="kosoado-drill">
        <h3>Quick drill</h3>
        <p>Click "Start" to be asked random row+column combinations. Type the form (kana).</p>
        <button id="kosoado-start" class="btn-primary">Start drill</button>
      </section>
    `;
  }
  const { question, userAnswer, feedback, score, total } = drillState;
  return `
    <section class="kosoado-drill">
      <h3>Quick drill <span class="muted small">(${score} / ${total})</span></h3>
      <div class="drill-question">
        <p>Give the form for <strong>${esc(question.row.label_en)}</strong> × <strong>${esc(question.col.label_en)}</strong>:</p>
        <input type="text" id="kosoado-input" class="text-input" lang="ja"
               autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"
               placeholder="Type kana or romaji..." value="${esc(userAnswer || '')}"
               ${feedback ? 'disabled' : ''}>
      </div>
      ${feedback ? `
        <div class="drill-feedback ${feedback.correct ? 'correct' : 'incorrect'}">
          <div class="feedback-headline">${feedback.correct ? 'Correct' : 'Wrong'}</div>
          <p>Answer: <strong lang="ja">${esc(question.expected)}</strong></p>
        </div>
        <button id="kosoado-next" class="btn-primary">Next</button>
      ` : `
        <button id="kosoado-check" class="btn-primary">Check</button>
      `}
      <button id="kosoado-stop" style="margin-left: 8px">End drill</button>
    </section>
  `;
}

function wireDrill(container) {
  const startBtn = document.getElementById('kosoado-start');
  if (startBtn) {
    startBtn.addEventListener('click', () => {
      drillState = { score: 0, total: 0 };
      pickQuestion();
      renderInPlace(container);
    });
    return;
  }
  const stop = document.getElementById('kosoado-stop');
  if (stop) {
    stop.addEventListener('click', () => {
      drillState = null;
      renderInPlace(container);
    });
  }
  const check = document.getElementById('kosoado-check');
  if (check) {
    check.addEventListener('click', () => {
      const input = document.getElementById('kosoado-input');
      check_answer(input.value);
      renderInPlace(container);
    });
    document.getElementById('kosoado-input')?.focus();
  }
  const next = document.getElementById('kosoado-next');
  if (next) {
    next.addEventListener('click', () => {
      pickQuestion();
      drillState.feedback = null;
      drillState.userAnswer = '';
      renderInPlace(container);
    });
  }
}

function renderInPlace(container) {
  // Re-render only the drill section to keep grid/proximity stable.
  const section = container.querySelector('.kosoado-drill');
  if (!section) {
    container.innerHTML = '';
    renderKosoado(container);
    return;
  }
  section.outerHTML = renderDrill();
  wireDrill(container);
}

function pickQuestion() {
  const ri = Math.floor(Math.random() * ROWS.length);
  const ci = Math.floor(Math.random() * COLS.length);
  drillState.question = {
    row: ROWS[ri],
    col: COLS[ci],
    expected: COLS[ci].forms[ri],
  };
  drillState.feedback = null;
  drillState.userAnswer = '';
}

async function check_answer(value) {
  const { matchesAnswer } = await import('./normalize.js');
  const correct = matchesAnswer(value, [drillState.question.expected]);
  drillState.feedback = { correct };
  drillState.total += 1;
  if (correct) drillState.score += 1;
  drillState.userAnswer = value;
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
