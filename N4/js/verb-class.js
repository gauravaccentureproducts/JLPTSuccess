// Verb classification module (Brief §2.1)
// Teaches the three Japanese verb groups (1=五段/u-verbs, 2=一段/ru-verbs,
// 3=irregular する/くる) and drills classification with deliberate
// over-sampling of the high-frequency Group-1 exceptions that look like
// Group 2 (帰る・入る・走る・知る・切る・要る・しゃべる・すべる).
import { matchesAnswer } from './normalize.js';
import * as storage from './storage.js';

// Each verb: dictionary form (kana for safety), group (1/2/3), meaning, isException flag.
const VERBS = [
  // Clear Group 1 (godan / u-verbs)
  { v: 'のむ', g: 1, en: 'drink' },
  { v: 'かう', g: 1, en: 'buy' },
  { v: 'いく', g: 1, en: 'go (irregular た-form)' },
  { v: 'よむ', g: 1, en: 'read' },
  { v: 'はなす', g: 1, en: 'speak' },
  { v: 'かく', g: 1, en: 'write' },
  { v: 'あう', g: 1, en: 'meet' },
  { v: 'まつ', g: 1, en: 'wait' },
  { v: 'とる', g: 1, en: 'take' },
  { v: 'のる', g: 1, en: 'ride' },
  { v: 'うる', g: 1, en: 'sell' },
  { v: 'おわる', g: 1, en: 'finish (intransitive)' },
  { v: 'すわる', g: 1, en: 'sit' },
  { v: 'ある', g: 1, en: 'exist (inanimate)' },
  { v: 'わかる', g: 1, en: 'understand' },
  { v: 'あらう', g: 1, en: 'wash' },
  { v: 'およぐ', g: 1, en: 'swim' },
  { v: 'いそぐ', g: 1, en: 'hurry' },

  // Clear Group 2 (一段 / ru-verbs ending in -iる or -eる)
  { v: 'たべる', g: 2, en: 'eat' },
  { v: 'みる', g: 2, en: 'see' },
  { v: 'おきる', g: 2, en: 'wake up / get up' },
  { v: 'ねる', g: 2, en: 'sleep' },
  { v: 'おしえる', g: 2, en: 'teach' },
  { v: 'あける', g: 2, en: 'open (transitive)' },
  { v: 'しめる', g: 2, en: 'close (transitive)' },
  { v: 'おりる', g: 2, en: 'get off' },
  { v: 'できる', g: 2, en: 'can do' },
  { v: 'わすれる', g: 2, en: 'forget' },
  { v: 'おぼえる', g: 2, en: 'remember' },
  { v: 'かりる', g: 2, en: 'borrow' },

  // The famous Group 1 exceptions (look like Group 2 but aren't)
  { v: 'かえる', g: 1, en: 'return / go home', except: true },
  { v: 'はいる', g: 1, en: 'enter', except: true },
  { v: 'はしる', g: 1, en: 'run', except: true },
  { v: 'しる', g: 1, en: 'know', except: true },
  { v: 'きる', g: 1, en: 'cut', except: true },
  { v: 'いる', g: 1, en: 'need (要る)', except: true },
  { v: 'しゃべる', g: 1, en: 'chatter / speak', except: true },
  { v: 'すべる', g: 1, en: 'slip / slide', except: true },

  // Group 3 - only two
  { v: 'する', g: 3, en: 'do' },
  { v: 'くる', g: 3, en: 'come' },
  { v: 'べんきょうする', g: 3, en: 'study' },
  { v: 'りょこうする', g: 3, en: 'travel' },
];

let drillState = null;
let view = 'teach'; // 'teach' | 'drill' | 'finished'

const PASS_THRESHOLD = 0.9; // 90% required to "pass"
const DRILL_LENGTH = 25;

export async function renderVerbClass(container) {
  if (view === 'drill' && drillState) return renderDrill(container);
  if (view === 'finished' && drillState) return renderFinished(container);
  return renderTeach(container);
}

function renderTeach(container) {
  view = 'teach';
  const lastAttempt = storage.get('verb-class-last-attempt', null);

  container.innerHTML = `
    <h2>Verb groups - classification</h2>
    <p>Japanese verbs split into three groups. Knowing which group a verb belongs to is the prerequisite for every conjugation (ます-form, て-form, plain-past, ない-form, etc.). Classification first, conjugation second.</p>

    <section class="verb-group-section">
      <h3>Group 1 - 五段 (u-verbs)</h3>
      <p>Dictionary form ends in any of <code>-う -つ -る -く -ぐ -す -ぬ -ぶ -む</code>. Conjugation shifts the final vowel: のむ → のみます → のんで → のんだ.</p>
      <p class="verb-list" lang="ja">のむ・かう・いく・よむ・はなす・かく・あう・まつ・とる・のる</p>
    </section>

    <section class="verb-group-section">
      <h3>Group 2 - 一段 (ru-verbs)</h3>
      <p>Dictionary form ends in <code>-iる</code> or <code>-eる</code>. Conjugation simply drops る: たべる → たべます → たべて → たべた.</p>
      <p class="verb-list" lang="ja">たべる・みる・おきる・ねる・おしえる・あける・しめる・できる・わすれる</p>
    </section>

    <section class="verb-group-section">
      <h3>Group 3 - Irregulars</h3>
      <p>Just two: する (do) and くる (come). Anything ending in <code>～する</code> like べんきょうする conjugates like する.</p>
      <p class="verb-list" lang="ja">する・くる・べんきょうする・りょこうする</p>
    </section>

    <section class="verb-group-section warning-section">
      <h3>The famous Group-1 exceptions</h3>
      <p>These verbs end in <code>-iる</code> or <code>-eる</code> and LOOK like Group 2, but they are actually <strong>Group 1</strong>. Memorize them - the drill below over-samples them deliberately.</p>
      <p class="verb-list" lang="ja">かえる (return)・はいる (enter)・はしる (run)・しる (know)・きる (cut)・いる (need)・しゃべる (chatter)・すべる (slip)</p>
    </section>

    <section class="drill-cta">
      <h3>Drill: classify on sight</h3>
      <p>${DRILL_LENGTH} verbs, mixed groups, with deliberate over-sampling of the exceptions. Pass threshold: ${Math.round(PASS_THRESHOLD * 100)}%.</p>
      ${lastAttempt ? `<p class="muted small">Last attempt: ${lastAttempt.score}/${lastAttempt.total} (${Math.round(lastAttempt.score / lastAttempt.total * 100)}%) on ${new Date(lastAttempt.ts).toLocaleDateString()}.</p>` : ''}
      <button id="vc-start" class="btn-primary">Start drill</button>
    </section>
  `;

  document.getElementById('vc-start').addEventListener('click', () => {
    drillState = {
      queue: buildQueue(),
      idx: 0,
      score: 0,
      misses: [],
    };
    view = 'drill';
    renderDrill(container);
  });
}

function buildQueue() {
  const exceptions = VERBS.filter(v => v.except);
  const others = VERBS.filter(v => !v.except);
  shuffle(exceptions);
  shuffle(others);
  // Over-sample exceptions: 40% of queue is exceptions
  const exTarget = Math.floor(DRILL_LENGTH * 0.4);
  const out = [];
  while (out.length < DRILL_LENGTH) {
    const fromExceptions = out.filter(v => v.except).length < exTarget && exceptions.length;
    if (fromExceptions) {
      out.push({ ...exceptions[Math.floor(Math.random() * exceptions.length)] });
    } else {
      out.push({ ...others[Math.floor(Math.random() * others.length)] });
    }
  }
  shuffle(out);
  return out;
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function renderDrill(container) {
  const item = drillState.queue[drillState.idx];
  const total = drillState.queue.length;
  const feedback = drillState.feedback;

  container.innerHTML = `
    <div class="vc-drill">
      <div class="srs-progress">
        <span>Verb classification · <strong>${drillState.idx + 1}</strong> / <strong>${total}</strong></span>
        <span class="muted small">Score: ${drillState.score}/${drillState.idx + (feedback ? 0 : 0)}</span>
      </div>
      <article class="vc-card">
        <p class="vc-prompt">Which group is this verb?</p>
        <p class="vc-verb" lang="ja">${esc(item.v)}</p>
        <p class="muted small">${esc(item.en)}</p>
        <div class="vc-buttons">
          <button class="vc-btn" data-grp="1" ${feedback ? 'disabled' : ''}>Group 1<br><small>五段 (u-verbs)</small></button>
          <button class="vc-btn" data-grp="2" ${feedback ? 'disabled' : ''}>Group 2<br><small>一段 (ru-verbs)</small></button>
          <button class="vc-btn" data-grp="3" ${feedback ? 'disabled' : ''}>Group 3<br><small>Irregular</small></button>
        </div>
        ${feedback ? `
          <div class="drill-feedback ${feedback.correct ? 'correct' : 'incorrect'}">
            <div class="feedback-headline">${feedback.correct ? 'Correct' : 'Wrong'}</div>
            <p>${esc(item.v)} is <strong>Group ${item.g}</strong>${item.except ? ' (a famous Group-1 exception - looks like Group 2 but isn\'t)' : ''}.</p>
            <button id="vc-next" class="btn-primary">${drillState.idx === total - 1 ? 'Finish' : 'Next'}</button>
          </div>
        ` : ''}
      </article>
    </div>
  `;

  container.querySelectorAll('.vc-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const g = parseInt(btn.dataset.grp, 10);
      const correct = g === item.g;
      if (correct) drillState.score += 1;
      else drillState.misses.push(item);
      drillState.feedback = { correct };
      renderDrill(container);
    });
  });

  document.getElementById('vc-next')?.addEventListener('click', () => {
    drillState.feedback = null;
    drillState.idx += 1;
    if (drillState.idx >= total) {
      view = 'finished';
      renderFinished(container);
    } else {
      renderDrill(container);
    }
  });
}

function renderFinished(container) {
  const total = drillState.queue.length;
  const score = drillState.score;
  const pct = Math.round((score / total) * 100);
  const passed = pct >= Math.round(PASS_THRESHOLD * 100);

  storage.set('verb-class-last-attempt', { score, total, ts: new Date().toISOString(), passed });

  const missByGroup = { 1: [], 2: [], 3: [] };
  for (const m of drillState.misses) missByGroup[m.g].push(m);

  container.innerHTML = `
    <div class="vc-finished">
      <h2>Drill complete</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${score}/${total}</div><div class="stat-label">Score</div></div>
        <div class="stat-card ${passed ? 'mastered' : 'weak'}"><div class="stat-num">${pct}%</div><div class="stat-label">${passed ? 'PASSED' : 'Try again'}</div></div>
      </section>
      ${passed ? '<p>You can confidently classify N5 verbs. Time to drill conjugation (te-form, ます-form, etc.).</p>' : `<p>Aim for ${Math.round(PASS_THRESHOLD*100)}%. The Group-1 exceptions are usually the trip-up - re-read the warning section above.</p>`}
      ${drillState.misses.length > 0 ? `
        <h3>Missed</h3>
        <ul class="vc-misses">
          ${drillState.misses.map(m => `<li><span lang="ja">${esc(m.v)}</span> <span class="muted small">(${esc(m.en)}) - Group ${m.g}${m.except ? ' [exception]' : ''}</span></li>`).join('')}
        </ul>
      ` : ''}
      <div class="test-nav">
        <button id="vc-restart" class="btn-primary">Try again</button>
        <button id="vc-back">Back</button>
      </div>
    </div>
  `;

  document.getElementById('vc-restart').addEventListener('click', () => {
    drillState = null;
    view = 'teach';
    renderTeach(container);
  });
  document.getElementById('vc-back').addEventListener('click', () => {
    location.hash = '#/learn';
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
