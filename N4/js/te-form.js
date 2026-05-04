// て-form gym (Brief §2.2)
// Drills te-form transformation with rule-aware feedback. Tracks per-ending
// accuracy and surfaces it. Accepts kana or romaji.
import { matchesAnswer } from './normalize.js';
import * as storage from './storage.js';

// Source verbs grouped by their te-form RULE (the transformation pattern).
const RULES = {
  'う/つ/る → って': [
    { v: 'かう', te: 'かって', en: 'buy' },
    { v: 'まつ', te: 'まって', en: 'wait' },
    { v: 'とる', te: 'とって', en: 'take' },
    { v: 'のる', te: 'のって', en: 'ride' },
    { v: 'あう', te: 'あって', en: 'meet' },
    { v: 'すわる', te: 'すわって', en: 'sit' },
    { v: 'はしる', te: 'はしって', en: 'run (Group 1 exception)' },
    { v: 'きる', te: 'きって', en: 'cut (Group 1 exception)' },
  ],
  'ぬ/ぶ/む → んで': [
    { v: 'のむ', te: 'のんで', en: 'drink' },
    { v: 'よむ', te: 'よんで', en: 'read' },
    { v: 'あそぶ', te: 'あそんで', en: 'play' },
    { v: 'よぶ', te: 'よんで', en: 'call' },
    { v: 'しぬ', te: 'しんで', en: 'die' },
  ],
  'く → いて (exception: いく → いって)': [
    { v: 'かく', te: 'かいて', en: 'write' },
    { v: 'きく', te: 'きいて', en: 'listen / ask' },
    { v: 'はたらく', te: 'はたらいて', en: 'work' },
    { v: 'いく', te: 'いって', en: 'go (the famous exception!)' },
  ],
  'ぐ → いで': [
    { v: 'およぐ', te: 'およいで', en: 'swim' },
    { v: 'いそぐ', te: 'いそいで', en: 'hurry' },
  ],
  'す → して': [
    { v: 'はなす', te: 'はなして', en: 'speak' },
    { v: 'けす', te: 'けして', en: 'turn off' },
    { v: 'おす', te: 'おして', en: 'push' },
  ],
  'Group 2 (drop る + て)': [
    { v: 'たべる', te: 'たべて', en: 'eat' },
    { v: 'みる', te: 'みて', en: 'see' },
    { v: 'おきる', te: 'おきて', en: 'wake up' },
    { v: 'ねる', te: 'ねて', en: 'sleep' },
    { v: 'おしえる', te: 'おしえて', en: 'teach' },
  ],
  'Irregular (する → して, 来る → きて)': [
    { v: 'する', te: 'して', en: 'do' },
    { v: 'くる', te: 'きて', en: 'come' },
    { v: 'べんきょうする', te: 'べんきょうして', en: 'study' },
  ],
};

let view = 'teach';
let session = null;

export async function renderTeForm(container) {
  if (view === 'drill' && session) return renderDrill(container);
  if (view === 'finished' && session) return renderFinished(container);
  return renderTeach(container);
}

function renderTeach(container) {
  view = 'teach';
  const accuracy = storage.get('te-form-accuracy', {});
  container.innerHTML = `
    <h2>て-form gym</h2>
    <p>The て-form is the gateway to almost every later N5 grammar pattern (てください, ています, てもいいです, etc.). Master the seven transformation rules first; the rest follows.</p>

    <section class="te-rules">
      <h3>Transformation rules</h3>
      <table class="te-rules-table">
        <thead><tr><th>Rule</th><th>Example</th><th>Your accuracy</th></tr></thead>
        <tbody>
          ${Object.entries(RULES).map(([rule, verbs]) => {
            const acc = accuracy[rule];
            const accStr = acc ? `${acc.correct}/${acc.attempts} (${Math.round(acc.correct/acc.attempts*100)}%)` : '-';
            const ex = verbs[0];
            return `<tr><td>${esc(rule)}</td><td lang="ja">${esc(ex.v)} → ${esc(ex.te)}</td><td>${accStr}</td></tr>`;
          }).join('')}
        </tbody>
      </table>
    </section>

    <section class="drill-cta">
      <h3>Drill</h3>
      <p>Type the て-form for each dictionary-form verb. Kana or romaji is fine. After a miss, the rule you violated is shown.</p>
      <button id="te-start" class="btn-primary">Start drill (20 verbs)</button>
    </section>
  `;
  document.getElementById('te-start').addEventListener('click', () => {
    session = {
      queue: buildQueue(20),
      idx: 0,
      score: 0,
      grades: [],
    };
    view = 'drill';
    renderDrill(container);
  });
}

function buildQueue(n) {
  // Pick from each rule, weighted toward the high-error ones if any.
  const acc = storage.get('te-form-accuracy', {});
  const weighted = [];
  for (const [rule, verbs] of Object.entries(RULES)) {
    const a = acc[rule];
    const errorRate = a && a.attempts > 0 ? 1 - (a.correct / a.attempts) : 0.5;
    const weight = Math.max(1, Math.round(errorRate * 10));
    for (const verb of verbs) {
      for (let w = 0; w < weight; w++) weighted.push({ ...verb, rule });
    }
  }
  // Shuffle and slice
  for (let i = weighted.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [weighted[i], weighted[j]] = [weighted[j], weighted[i]];
  }
  // Dedup
  const seen = new Set();
  const out = [];
  for (const x of weighted) {
    if (seen.has(x.v)) continue;
    seen.add(x.v);
    out.push(x);
    if (out.length >= n) break;
  }
  return out;
}

function renderDrill(container) {
  const total = session.queue.length;
  const item = session.queue[session.idx];
  const feedback = session.feedback;
  container.innerHTML = `
    <div class="te-drill">
      <div class="srs-progress">
        <span>て-form drill · <strong>${session.idx + 1}</strong> / <strong>${total}</strong></span>
        <span class="muted small">${session.score}/${session.idx + (feedback ? 0 : 0)}</span>
      </div>
      <article class="vc-card">
        <p class="vc-prompt">Type the て-form for:</p>
        <p class="vc-verb" lang="ja">${esc(item.v)}</p>
        <p class="muted small">${esc(item.en)}</p>
        <div style="margin: 16px 0">
          <input id="te-input" type="text" class="text-input" lang="ja"
                 autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"
                 placeholder="Type kana or romaji..." ${feedback ? 'disabled' : ''}>
        </div>
        ${feedback ? `
          <div class="drill-feedback ${feedback.correct ? 'correct' : 'incorrect'}">
            <div class="feedback-headline">${feedback.correct ? 'Correct' : 'Wrong'}</div>
            <p>Answer: <strong lang="ja">${esc(item.te)}</strong></p>
            <p class="muted small">Rule: <strong>${esc(item.rule)}</strong></p>
            <button id="te-next" class="btn-primary">${session.idx === total - 1 ? 'Finish' : 'Next'}</button>
          </div>
        ` : `<button id="te-check" class="btn-primary">Check</button>`}
      </article>
    </div>
  `;

  document.getElementById('te-check')?.addEventListener('click', () => {
    const value = document.getElementById('te-input').value;
    const correct = matchesAnswer(value, [item.te]);
    session.feedback = { correct, value };
    if (correct) session.score += 1;
    session.grades.push({ rule: item.rule, correct });
    // Update per-rule accuracy
    const acc = storage.get('te-form-accuracy', {});
    if (!acc[item.rule]) acc[item.rule] = { attempts: 0, correct: 0 };
    acc[item.rule].attempts += 1;
    if (correct) acc[item.rule].correct += 1;
    storage.set('te-form-accuracy', acc);
    renderDrill(container);
  });
  document.getElementById('te-input')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') document.getElementById('te-check')?.click();
  });
  document.getElementById('te-input')?.focus();
  document.getElementById('te-next')?.addEventListener('click', () => {
    session.feedback = null;
    session.idx += 1;
    if (session.idx >= total) {
      view = 'finished';
      renderFinished(container);
    } else {
      renderDrill(container);
    }
  });
}

function renderFinished(container) {
  const total = session.queue.length;
  const pct = Math.round((session.score / total) * 100);
  // Per-rule breakdown
  const ruleStats = {};
  for (const g of session.grades) {
    if (!ruleStats[g.rule]) ruleStats[g.rule] = { attempts: 0, correct: 0 };
    ruleStats[g.rule].attempts += 1;
    if (g.correct) ruleStats[g.rule].correct += 1;
  }
  const ruleRows = Object.entries(ruleStats).map(([rule, s]) => {
    const ratio = Math.round((s.correct / s.attempts) * 100);
    return `<li><span>${esc(rule)}</span> <span class="muted">${s.correct}/${s.attempts} (${ratio}%)</span></li>`;
  }).join('');

  container.innerHTML = `
    <div class="te-finished">
      <h2>て-form drill complete</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${session.score}/${total}</div><div class="stat-label">Score</div></div>
        <div class="stat-card ${pct >= 80 ? 'mastered' : 'weak'}"><div class="stat-num">${pct}%</div><div class="stat-label">Accuracy</div></div>
      </section>
      <h3>Per-rule accuracy</h3>
      <ul class="te-rule-list">${ruleRows}</ul>
      <p class="muted small">All-time per-rule accuracy is also shown in the rule table at the top of this page. Lower-accuracy rules are over-sampled in the next drill.</p>
      <div class="test-nav">
        <button id="te-restart" class="btn-primary">Drill again</button>
        <button id="te-back">Back</button>
      </div>
    </div>
  `;
  document.getElementById('te-restart').addEventListener('click', () => {
    session = null;
    view = 'teach';
    renderTeach(container);
  });
  document.getElementById('te-back').addEventListener('click', () => {
    location.hash = '#/learn';
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
