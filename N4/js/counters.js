// Counters module (Brief §2.4)
// Reference table for the major N5 counters with rendaku/irregular readings,
// plus a "how many?" drill that uses a neutral geometric dot (●) repeated
// to visualise the count (no images, no emoji).
import { matchesAnswer } from './normalize.js';
import * as storage from './storage.js';

// Visual marker for "1 thing" in the count drill — Unicode geometric
// shape (Black Circle, U+25CF), renders as plain typography on every
// platform. Repeat this N times to show "this many objects".
const COUNT_DOT = '●';

// Each counter: name, suffix, full reading table 1..10 + "how many",
// with notes on irregularities.
const COUNTERS = {
  'tsu': {
    label: '〜つ',
    desc: 'Native Japanese counter (general things, ages 1-9)',
    readings: {
      1: 'ひとつ', 2: 'ふたつ', 3: 'みっつ', 4: 'よっつ', 5: 'いつつ',
      6: 'むっつ', 7: 'ななつ', 8: 'やっつ', 9: 'ここのつ', 10: 'とお',
      'q': 'いくつ',
    },
    notes: '10 is just とお (not じゅっつ). After 10 switch to 11 = じゅういち + general counter.',
  },
  'nin': {
    label: '〜人 (にん)',
    desc: 'People',
    readings: {
      1: 'ひとり', 2: 'ふたり', 3: 'さんにん', 4: 'よにん', 5: 'ごにん',
      6: 'ろくにん', 7: 'しちにん / ななにん', 8: 'はちにん', 9: 'きゅうにん',
      10: 'じゅうにん', 'q': 'なんにん',
    },
    notes: '1人 ひとり and 2人 ふたり are irregular (special readings).',
  },
  'mai': {
    label: '〜枚 (まい)',
    desc: 'Flat thin objects (paper, plates, tickets, t-shirts)',
    readings: {
      1: 'いちまい', 2: 'にまい', 3: 'さんまい', 4: 'よんまい', 5: 'ごまい',
      6: 'ろくまい', 7: 'ななまい / しちまい', 8: 'はちまい', 9: 'きゅうまい',
      10: 'じゅうまい', 'q': 'なんまい',
    },
    notes: 'No sound changes. Easy counter.',
  },
  'hon': {
    label: '〜本 (ほん / ぼん / ぽん)',
    desc: 'Long thin objects (bottles, pens, umbrellas, trees)',
    readings: {
      1: 'いっぽん', 2: 'にほん', 3: 'さんぼん', 4: 'よんほん', 5: 'ごほん',
      6: 'ろっぽん', 7: 'ななほん', 8: 'はっぽん', 9: 'きゅうほん',
      10: 'じゅっぽん', 'q': 'なんぼん',
    },
    notes: '1, 6, 8, 10 take ぽん; 3 takes ぼん; rest take ほん.',
  },
  'satsu': {
    label: '〜冊 (さつ)',
    desc: 'Books, magazines, bound volumes',
    readings: {
      1: 'いっさつ', 2: 'にさつ', 3: 'さんさつ', 4: 'よんさつ', 5: 'ごさつ',
      6: 'ろくさつ', 7: 'ななさつ', 8: 'はっさつ', 9: 'きゅうさつ',
      10: 'じゅっさつ', 'q': 'なんさつ',
    },
    notes: '1, 8, 10 take small っ.',
  },
  'kai': {
    label: '〜階 (かい / がい)',
    desc: 'Floor of a building',
    readings: {
      1: 'いっかい', 2: 'にかい', 3: 'さんがい / さんかい', 4: 'よんかい',
      5: 'ごかい', 6: 'ろっかい', 7: 'ななかい', 8: 'はっかい / はちかい',
      9: 'きゅうかい', 10: 'じゅっかい', 'q': 'なんがい / なんかい',
    },
    notes: '3階 さんがい is the famous rendaku (sometimes さんかい).',
  },
  'sai': {
    label: '〜歳 / 〜才 (さい)',
    desc: 'Age',
    readings: {
      1: 'いっさい', 2: 'にさい', 3: 'さんさい', 4: 'よんさい', 5: 'ごさい',
      6: 'ろくさい', 7: 'ななさい', 8: 'はっさい', 9: 'きゅうさい',
      10: 'じゅっさい', 'q': 'なんさい',
    },
    notes: '20歳 (twenty) is special: はたち (not にじゅっさい).',
  },
  'hai': {
    label: '〜杯 (はい / ばい / ぱい)',
    desc: 'Cups / glasses (drinks)',
    readings: {
      1: 'いっぱい', 2: 'にはい', 3: 'さんばい', 4: 'よんはい', 5: 'ごはい',
      6: 'ろっぱい', 7: 'ななはい', 8: 'はっぱい', 9: 'きゅうはい',
      10: 'じゅっぱい', 'q': 'なんばい',
    },
    notes: 'Same pattern as 本: 1/6/8/10 → ぱい; 3 → ばい.',
  },
  'fun': {
    label: '〜分 (ふん / ぷん)',
    desc: 'Minutes',
    readings: {
      1: 'いっぷん', 2: 'にふん', 3: 'さんぷん', 4: 'よんぷん', 5: 'ごふん',
      6: 'ろっぷん', 7: 'ななふん', 8: 'はっぷん', 9: 'きゅうふん',
      10: 'じゅっぷん', 'q': 'なんぷん',
    },
    notes: '1, 3, 4, 6, 8, 10 take ぷん; 2, 5, 7, 9 take ふん.',
  },
  'ji': {
    label: '〜時 (じ)',
    desc: 'O\'clock',
    readings: {
      1: 'いちじ', 2: 'にじ', 3: 'さんじ', 4: 'よじ', 5: 'ごじ',
      6: 'ろくじ', 7: 'しちじ', 8: 'はちじ', 9: 'くじ', 10: 'じゅうじ',
      'q': 'なんじ',
    },
    notes: '4時 = よじ (NOT しじ). 7時 = しちじ. 9時 = くじ (NOT きゅうじ).',
  },
  'en': {
    label: '〜円 (えん)',
    desc: 'Yen (currency)',
    readings: {
      1: 'いちえん', 2: 'にえん', 3: 'さんえん', 4: 'よえん', 5: 'ごえん',
      6: 'ろくえん', 7: 'ななえん', 8: 'はちえん', 9: 'きゅうえん',
      10: 'じゅうえん', 'q': 'いくら / なんえん',
    },
    notes: 'For "how much?" use いくら, not なんえん.',
  },
};

let view = 'browse';
let drillState = null;

export async function renderCounters(container) {
  if (view === 'drill' && drillState) return renderDrill(container);
  return renderBrowse(container);
}

function renderBrowse(container) {
  view = 'browse';
  const sections = Object.entries(COUNTERS).map(([key, c]) => `
    <section class="counter-row">
      <header class="counter-row-head">
        <h3>${esc(c.label)} <span class="muted small">${esc(c.desc)}</span></h3>
      </header>
      <table class="counter-table">
        <thead><tr>${[1,2,3,4,5,6,7,8,9,10,'q'].map(n => `<th>${n === 'q' ? '?' : n}</th>`).join('')}</tr></thead>
        <tbody><tr>${[1,2,3,4,5,6,7,8,9,10,'q'].map(n => `<td lang="ja">${esc(c.readings[n] || '')}</td>`).join('')}</tr></tbody>
      </table>
      <p class="muted small">${esc(c.notes)}</p>
    </section>
  `).join('');

  container.innerHTML = `
    <h2>Counters</h2>
    <p>Japanese needs a counter when you state a quantity. The set below covers the most-tested N5 counters with their rendaku/irregular readings called out.</p>

    ${sections}

    <section class="drill-cta">
      <h3>How many? drill</h3>
      <p>Drill randomly picks a counter and a count, shows that many neutral dots, and asks you to type the counter phrase. Kana or romaji is accepted.</p>
      <button id="ct-start" class="btn-primary">Start drill (15 questions)</button>
    </section>
  `;

  document.getElementById('ct-start').addEventListener('click', () => {
    drillState = {
      queue: buildQueue(15),
      idx: 0,
      score: 0,
      grades: [],
    };
    view = 'drill';
    renderDrill(container);
  });
}

function buildQueue(n) {
  const keys = Object.keys(COUNTERS);
  const out = [];
  for (let i = 0; i < n; i++) {
    const key = keys[Math.floor(Math.random() * keys.length)];
    const c = COUNTERS[key];
    // Pick 1..10 (skip q)
    const num = Math.floor(Math.random() * 10) + 1;
    out.push({ key, counter: c, num });
  }
  return out;
}

function renderDrill(container) {
  const total = drillState.queue.length;
  const item = drillState.queue[drillState.idx];
  const feedback = drillState.feedback;
  const expected = item.counter.readings[item.num];

  // For object-based counters, render N geometric dots. For abstract
  // counters (time, age, currency, floor), show the unit + a number.
  const isObject = ['tsu', 'nin', 'mai', 'hon', 'satsu', 'hai'].includes(item.key);
  const visual = isObject
    ? `<div class="counter-visual" aria-label="${item.num} ${item.counter.label}">${COUNT_DOT.repeat(item.num)}</div>`
    : `<div class="counter-abstract"><span style="font-size: 32px">${item.num}</span> <span class="muted">${esc(item.counter.label)}</span></div>`;

  container.innerHTML = `
    <div class="counter-drill">
      <div class="srs-progress">
        <span>Counter drill · <strong>${drillState.idx + 1}</strong> / <strong>${total}</strong></span>
        <span class="muted small">${drillState.score}/${drillState.idx + (feedback ? 0 : 0)}</span>
      </div>
      <article class="vc-card">
        <p class="vc-prompt">How many? Type the full counter phrase.</p>
        ${visual}
        <p class="muted small">Counter: <strong>${esc(item.counter.label)}</strong></p>
        <input id="ct-input" type="text" class="text-input" lang="ja"
               autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"
               placeholder="Type kana or romaji..." ${feedback ? 'disabled' : ''}>
        ${feedback ? `
          <div class="drill-feedback ${feedback.correct ? 'correct' : 'incorrect'}">
            <div class="feedback-headline">${feedback.correct ? 'Correct' : 'Wrong'}</div>
            <p>Expected: <strong lang="ja">${esc(expected)}</strong></p>
            <p class="muted small">${esc(item.counter.notes)}</p>
            <button id="ct-next" class="btn-primary">${drillState.idx === total - 1 ? 'Finish' : 'Next'}</button>
          </div>
        ` : `<button id="ct-check" class="btn-primary">Check</button>`}
      </article>
    </div>
  `;

  document.getElementById('ct-check')?.addEventListener('click', () => {
    const value = document.getElementById('ct-input').value;
    // Accept any of the slash-separated readings
    const acceptable = String(expected).split(/\s*\/\s*/).map(s => s.trim()).filter(Boolean);
    const correct = acceptable.some(a => matchesAnswer(value, [a]));
    drillState.feedback = { correct };
    if (correct) drillState.score += 1;
    drillState.grades.push({ key: item.key, correct });
    renderDrill(container);
  });
  document.getElementById('ct-input')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') document.getElementById('ct-check')?.click();
  });
  document.getElementById('ct-input')?.focus();
  document.getElementById('ct-next')?.addEventListener('click', () => {
    drillState.feedback = null;
    drillState.idx += 1;
    if (drillState.idx >= total) {
      view = 'browse';
      drillState = null;
      renderBrowse(container);
    } else {
      renderDrill(container);
    }
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
