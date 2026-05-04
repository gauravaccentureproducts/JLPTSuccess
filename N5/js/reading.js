// Reading passages module (Brief §3.2)
// Each session: pick a passage, show it, then run comprehension questions.
import { renderJa } from './furigana.js';
import * as storage from './storage.js';

// Display labels for level / topic taxonomy. Data values stay English
// (stable code keys for lookup); we localize at render time so the
// learner-facing surface is Japanese (per 2026-05-02 user direction).
const LEVEL_JA = {
  'easy':        'やさしい',
  'medium':      'ふつう',
  'info-search': 'じょうほうけんさく',
};
const TOPIC_JA = {
  'self-introduction': 'じこしょうかい',
  'daily routine':     'まいにちの せいかつ',
  'weekend plan':      'しゅうまつの よてい',
  'weekend':           'しゅうまつ',
  'shopping':          'かいもの',
  'family':            'かぞく',
  'weather':           'てんき',
  'schedule':          'よてい',
  'transport':         'こうつう',
  'hobby':             'しゅみ',
  'school':            '学校',
  'food':              'たべもの',
  'travel':            'りょこう',
  'health':            'けんこう',
  'study':             'べんきょう',
  'people':            'ひと',
  'request':           'おねがい',
  'room':              'へや',
  'directions':        'みちあんない',
};

let bank = null;
let session = null;

async function loadBank() {
  if (bank) return bank;
  const res = await fetch('data/reading.json');
  bank = await res.json();
  return bank;
}

export async function renderReading(container) {
  await loadBank();
  if (session) return renderSession(container);
  return renderIndex(container);
}

function renderIndex(container) {
  const passages = bank.passages || [];
  // Mock-test mode (DEFER-12): when on, filters each passage's questions
  // down to those tagged `format_role: "primary"` so the per-passage
  // question count matches the official JLPT-N5 distribution. Persists
  // across navigation via the same settings store as everything else.
  const settings = (typeof storage !== 'undefined' && storage.getSettings)
    ? storage.getSettings() : {};
  const mockTestMode = !!settings.readingMockTestMode;

  const items = passages.map(p => {
    const totalQ = (p.questions || []).length;
    const primaryQ = (p.questions || []).filter(
      q => q.format_role === 'primary' || !q.format_role).length;
    const shownCount = mockTestMode ? primaryQ : totalQ;
    return `
      <li>
        <button class="reading-pick" data-id="${esc(p.id)}">
          <span class="reading-title"><strong>${renderJa(p.title_ja)}</strong> <span class="muted small">(${renderJa(LEVEL_JA[p.level] || p.level)})</span></span>
          <span class="muted small">${renderJa(TOPIC_JA[p.topic] || p.topic)} ・ ${shownCount} ${renderJa('もん')}</span>
        </button>
      </li>
    `;
  }).join('');
  container.innerHTML = `
    <h2>${renderJa('どっかい れんしゅう')}</h2>
    <p>${renderJa('みじかい JLPT けいしきの ぶんしょうと しつもんです。')} ${passages.length} ${renderJa('ぶんしょうが あります。やさしい → ふつう → じょうほうけんさく の じゅんに ならんで います。')}</p>
    <label class="reading-mode-toggle">
      <input type="checkbox" id="reading-mock-mode" ${mockTestMode ? 'checked' : ''}>
      <span>${renderJa('もぎテストモード')} (primary questions only — matches official JLPT N5 distribution)</span>
    </label>
    <ul class="reading-list">${items}</ul>
  `;
  document.getElementById('reading-mock-mode').addEventListener('change', (e) => {
    storage.setSettings({ readingMockTestMode: e.target.checked });
    renderIndex(container);
  });
  container.querySelectorAll('[data-id]').forEach(btn => {
    btn.addEventListener('click', () => {
      const p = passages.find(x => x.id === btn.dataset.id);
      // When mock-test mode is on, narrow the question list to primaries.
      const filtered = mockTestMode
        ? { ...p, questions: (p.questions || []).filter(
              q => q.format_role === 'primary' || !q.format_role) }
        : p;
      session = { passage: filtered, phase: 'read', answers: {}, idx: 0 };
      renderSession(container);
    });
  });
}

function renderSession(container) {
  const p = session.passage;
  if (session.phase === 'read') return renderRead(container, p);
  if (session.phase === 'questions') return renderQuestions(container, p);
  return renderResults(container, p);
}

function renderRead(container, p) {
  container.innerHTML = `
    <article class="reading-passage">
      <div class="srs-progress">
        <span><a href="#/reading" id="reading-back">← ${renderJa('もどる')}</a> ・ ${renderJa('ぶんしょうを 読んで、しつもんを はじめて ください。')}</span>
      </div>
      <h2>${renderJa(p.title_ja)}</h2>
      <p class="muted small">レベル: ${renderJa(LEVEL_JA[p.level] || p.level)} ・ トピック: ${renderJa(TOPIC_JA[p.topic] || p.topic)}</p>
      <div class="passage-text">${renderJa(p.ja)}</div>
      ${p.audio ? `
        <div class="reading-audio">
          <p class="muted small">${renderJa('おんせい (ある とき):')}</p>
          <audio controls preload="none" src="${esc(p.audio)}">Your browser does not support audio.</audio>
        </div>
      ` : ''}
      <button id="reading-start-q" class="btn-primary">${renderJa('しつもんを はじめる')} (${p.questions.length})</button>
    </article>
  `;
  document.getElementById('reading-back').addEventListener('click', (e) => {
    e.preventDefault();
    session = null;
    location.hash = '#/reading';
  });
  document.getElementById('reading-start-q').addEventListener('click', () => {
    session.phase = 'questions';
    renderQuestions(container, p);
  });
}

function renderQuestions(container, p) {
  const total = p.questions.length;
  const idx = session.idx;
  const q = p.questions[idx];
  const picked = session.answers[q.id];
  const feedback = picked != null;
  const correct = picked === q.correctAnswer;

  container.innerHTML = `
    <article class="reading-passage">
      <div class="srs-progress">
        <span>${renderJa(p.title_ja)} ・ ${renderJa('もんだい')} ${idx + 1} / ${total}</span>
      </div>
      <details class="passage-recap">
        <summary>${renderJa('ぶんしょうを 見る')}</summary>
        <div class="passage-text">${renderJa(p.ja)}</div>
      </details>
      <div class="question-card">
        <p class="question">${renderJa(q.prompt_ja)}</p>
        <div class="choice-grid">
          ${q.choices.map(c => {
            let cls = 'choice-button';
            if (feedback) {
              if (c === q.correctAnswer) cls += ' correct-choice';
              else if (c === picked) cls += ' wrong-choice';
            } else if (picked === c) {
              cls += ' selected';
            }
            return `<button data-pick="${esc(c)}" class="${cls}" ${feedback ? 'disabled' : ''}>${renderJa(c)}</button>`;
          }).join('')}
        </div>
        ${feedback ? `
          <div class="drill-feedback ${correct ? 'correct' : 'incorrect'}">
            <div class="feedback-headline">${correct ? renderJa('せいかい') : renderJa('ざんねん')}</div>
            ${q.explanation_en ? `<p class="muted small">${esc(q.explanation_en)}</p>` : ''}
            <button id="reading-next" class="btn-primary">${idx === total - 1 ? renderJa('おわり') : renderJa('つぎの しつもん')}</button>
          </div>
        ` : ''}
      </div>
    </article>
  `;
  container.querySelectorAll('[data-pick]').forEach(btn => {
    btn.addEventListener('click', () => {
      session.answers[q.id] = btn.dataset.pick;
      renderQuestions(container, p);
    });
  });
  document.getElementById('reading-next')?.addEventListener('click', () => {
    if (idx === total - 1) {
      session.phase = 'results';
      renderResults(container, p);
    } else {
      session.idx += 1;
      renderQuestions(container, p);
    }
  });
}

function renderResults(container, p) {
  const total = p.questions.length;
  const score = p.questions.filter(q => session.answers[q.id] === q.correctAnswer).length;
  const pct = Math.round((score / total) * 100);
  // Mark this passage as completed the first time the user reaches the
  // results screen with at least one correct answer. Powers the homepage
  // Progress section's Reading row.
  if (score > 0) {
    storage.setReadingCompleted(p.id);
  }
  container.innerHTML = `
    <div class="reading-results">
      <h2>${renderJa(p.title_ja)} ・ ${renderJa('けっか')}</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${score}/${total}</div><div class="stat-label">${renderJa('スコア')}</div></div>
        <div class="stat-card ${pct >= 70 ? 'mastered' : 'weak'}"><div class="stat-num">${pct}%</div><div class="stat-label">${renderJa('せいかいりつ')}</div></div>
      </section>
      <div class="test-nav">
        <button id="reading-back-list" class="btn-primary">${renderJa('ほかの ぶんしょうを えらぶ')}</button>
      </div>
    </div>
  `;
  document.getElementById('reading-back-list').addEventListener('click', () => {
    session = null;
    renderIndex(container);
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
