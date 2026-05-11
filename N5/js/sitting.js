// ISSUE-020 / IMP-032 (audit round-3): full mock-paper sitting flow.
//
// Chains 4 paper-1 papers + 1 listening segment into the official JLPT N5
// rhythm:
//   Section 1: 文字・語彙 (Moji + Goi)        25 min  (15 + 10 questions, ~1 min/Q)
//   Section 2: 文法・読解 (Bunpou + Dokkai)   50 min  (15 + 16 questions, ~1.5 min/Q)
//   Section 3: 聴解        (Listening)       30 min  (12 items, audio-paced)
//
// On entry, the user picks a paper number (1..7) and we run section 1
// (moji-N + goi-N), then prompt to start section 2 (bunpou-N + dokkai-N),
// then section 3 (listening). Each section runs its own countdown timer
// at the official budget; auto-submit at zero. Between sections the
// user gets a 1-minute break screen with a "Skip break" button.
//
// At the end, the per-section results aggregate into one score
// (matching the 0-180 official conversion is out of scope; we report
// raw correct/total per section + an overall percentage).
import * as storage from './storage.js';
import { t } from './i18n.js';
// IMP-WAVE-P4-T1 (UI audit fix, 2026-05-11): per-mondai pacing chip
// using section_timing data from data/test_strategy.json. The chip
// surfaces the JLPT-official recommended seconds/q + technique hint
// next to each question, so users build time discipline without the
// section timer changing.
import { loadPacing, renderPacingChip } from './mondai-pacing.js';

const SECTIONS = [
  // [section-id, label, ja-label, [paper-categories], duration-minutes]
  ['mojigoi',   'Moji + Goi',         '文字・語彙', ['moji', 'goi'],     25],
  ['bunpoudok', 'Bunpou + Dokkai',    '文法・読解', ['bunpou', 'dokkai'], 50],
  ['choukai',   'Listening',          '聴解',       ['listening'],       30],
];
const BREAK_SECONDS = 60;

let session = null;     // { paperNumber, currentSection, startedAt, sectionResults: [], answers: {} }
let timerHandle = null;
let timerEndsAt = null;

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

async function loadPaper(category, n) {
  const r = await fetch(`data/papers/${category}/paper-${n}.json`);
  if (!r.ok) return null;
  return r.json();
}

async function loadListening() {
  const r = await fetch('data/listening.json');
  if (!r.ok) return { items: [] };
  return r.json();
}

function fmtTime(sec) {
  const m = Math.floor(sec / 60);
  const s = String(sec % 60).padStart(2, '0');
  return `${String(m).padStart(2, '0')}:${s}`;
}

function startTimer(seconds, onTick, onExpire) {
  timerEndsAt = Date.now() + seconds * 1000;
  if (timerHandle) clearInterval(timerHandle);
  timerHandle = setInterval(() => {
    const remain = Math.max(0, Math.ceil((timerEndsAt - Date.now()) / 1000));
    onTick(remain);
    if (remain <= 0) {
      clearInterval(timerHandle);
      timerHandle = null;
      onExpire();
    }
  }, 1000);
  // Fire one immediate tick so the chip renders the right value before
  // the first interval lap.
  onTick(seconds);
}

export async function renderSitting(container, params) {
  // Routes:
  //   #/sitting             - paper-number picker
  //   #/sitting/<n>         - start section 1 of paper n
  //   #/sitting/<n>/<i>     - section i (0..2) of paper n
  //   #/sitting/<n>/result  - final aggregate result
  const parts = (params || '').split('/').filter(Boolean);
  if (parts.length === 0) return renderPicker(container);
  const paperNumber = parseInt(parts[0], 10);
  if (!Number.isFinite(paperNumber) || paperNumber < 1 || paperNumber > 7) {
    container.innerHTML = `<p>${esc(t('meta.bad_paper'))} <a href="#/sitting">${esc(t('meta.pick_again'))}</a></p>`;
    return;
  }
  if (parts[1] === 'result') return renderResult(container, paperNumber);
  const sectionIdx = parts[1] ? parseInt(parts[1], 10) : 0;
  if (!Number.isFinite(sectionIdx) || sectionIdx < 0 || sectionIdx >= SECTIONS.length) {
    container.innerHTML = `<p>${esc(t('meta.bad_section'))} <a href="#/sitting">${esc(t('meta.pick_again'))}</a></p>`;
    return;
  }
  return renderSection(container, paperNumber, sectionIdx);
}

function renderPicker(container) {
  container.innerHTML = `
    <article class="sitting-picker">
      <a class="back-link" href="#/test">← ${esc(t('meta.back_to_test'))}</a>
      <h2>${esc(t('meta.sitting_title'))}</h2>
      <p class="page-lede">${esc(t('meta.sitting_intro'))}</p>
      <p class="muted">${esc(t('meta.pick_paper_intro'))}</p>
      <div class="sitting-paper-grid">
        ${[1, 2, 3, 4, 5, 6, 7].map(n => `
          <a class="sitting-paper-card" href="#/sitting/${n}/0">
            <span class="card-index" aria-hidden="true">${String(n).padStart(2, '0')}</span>
            <h3>${esc(t('meta.paper_n').replace('${n}', n))}</h3>
            <p class="muted small">moji-${n} · goi-${n} · bunpou-${n} · dokkai-${n} · listening</p>
          </a>
        `).join('')}
      </div>
    </article>
  `;
}

async function renderSection(container, paperNumber, sectionIdx) {
  const [, label, jaLabel, categories, durationMin] = SECTIONS[sectionIdx];
  if (!session || session.paperNumber !== paperNumber) {
    session = {
      paperNumber,
      currentSection: sectionIdx,
      startedAt: new Date().toISOString(),
      sectionResults: [],
      answers: {},
    };
  }

  // Load all questions for this section.
  let questions = [];
  if (categories[0] === 'listening') {
    const d = await loadListening();
    // Pull the first 12 listening items for the section (round-3 corpus
    // doesn't have per-paper listening; share the same 12 across all
    // paper numbers for now).
    questions = (d.items || []).slice(0, 12).map(it => ({
      id: it.id,
      stem_html: it.title_ja || it.id,
      audio: it.audio,
      script_ja: it.script_ja,
      prompt_ja: it.prompt_ja,
      choices: it.choices || [],
      correctIndex: (it.choices || []).findIndex(c => c === it.correctAnswer),
      kind: 'listening',
      // IMP-WAVE-P4-T1: carry mondai (1..4 = task / point / utterance
      // / immediate_response) so renderPacingChip can look up the
      // chokai section_timing entry for this item.
      mondai: it.mondai,
    }));
  } else {
    for (const cat of categories) {
      const p = await loadPaper(cat, paperNumber);
      if (p) {
        questions.push(...p.questions.map(q => ({ ...q, kind: cat })));
      }
    }
  }

  if (questions.length === 0) {
    container.innerHTML = `<p>No questions for section ${sectionIdx}. <a href="#/sitting">Restart.</a></p>`;
    return;
  }

  // IMP-WAVE-P4-T1: prime the pacing cache so renderPacingChip()
  // returns chips synchronously inside the template literal below.
  // Best-effort — if the fetch fails, chips simply render as ''.
  await loadPacing();

  const submit = () => {
    // Grade.
    let correct = 0;
    for (const q of questions) {
      const a = session.answers[q.id];
      if (typeof a === 'number' && a === q.correctIndex) correct += 1;
    }
    session.sectionResults[sectionIdx] = {
      label, jaLabel, total: questions.length, correct,
      durationSec: durationMin * 60,
    };
    if (sectionIdx + 1 < SECTIONS.length) {
      // Break screen, then advance.
      renderBreak(container, paperNumber, sectionIdx + 1);
    } else {
      location.hash = `#/sitting/${paperNumber}/result`;
    }
  };

  // Render the form.
  const total = questions.length;
  container.innerHTML = `
    <article class="sitting-section">
      <header class="sitting-section-header">
        <span class="sitting-section-label" lang="ja">${esc(jaLabel)}</span>
        <h2>${esc(label)} <span class="muted small">(Paper ${paperNumber}, ${total} questions)</span></h2>
        <p class="sitting-timer-chip" id="sitting-timer" aria-live="polite">${fmtTime(durationMin * 60)}</p>
      </header>
      <form id="sitting-form" class="sitting-form">
        ${questions.map((q, i) => `
          <fieldset class="sitting-question" id="sq-${esc(q.id)}">
            <legend>Q${i + 1} ${renderPacingChip(q.kind, q.mondai)}</legend>
            ${q.audio ? `<audio class="example-audio" controls preload="metadata" src="${esc(q.audio)}"></audio>` : ''}
            ${q.stem_html ? `<p class="sitting-stem" lang="ja">${q.stem_html}</p>` : ''}
            ${q.prompt_ja ? `<p class="sitting-prompt" lang="ja">${esc(q.prompt_ja)}</p>` : ''}
            ${q.script_ja && !q.audio ? `<p class="sitting-script" lang="ja">${esc(q.script_ja)}</p>` : ''}
            <div class="sitting-choices">
              ${(q.choices || []).map((ch, ci) => `
                <label>
                  <input type="radio" name="${esc(q.id)}" value="${ci}">
                  <span lang="ja">${esc(ch)}</span>
                </label>
              `).join('')}
            </div>
          </fieldset>
        `).join('')}
        <div class="sitting-actions">
          <button type="submit" class="btn-primary">Submit section ${sectionIdx + 1} of ${SECTIONS.length}</button>
        </div>
      </form>
    </article>
  `;

  document.getElementById('sitting-form').addEventListener('submit', (ev) => {
    ev.preventDefault();
    if (timerHandle) clearInterval(timerHandle);
    timerHandle = null;
    // Capture current selections.
    for (const q of questions) {
      const sel = document.querySelector(`input[name="${q.id}"]:checked`);
      if (sel) session.answers[q.id] = parseInt(sel.value, 10);
    }
    submit();
  });
  document.getElementById('sitting-form').addEventListener('change', (ev) => {
    if (ev.target.tagName === 'INPUT') {
      const q = questions.find(qq => qq.id === ev.target.name);
      if (q) session.answers[q.id] = parseInt(ev.target.value, 10);
    }
  });

  startTimer(
    durationMin * 60,
    (remain) => {
      const chip = document.getElementById('sitting-timer');
      if (chip) chip.textContent = fmtTime(remain);
      if (remain <= 60 && chip) chip.classList.add('danger');
    },
    () => {
      // Auto-submit on zero.
      for (const q of questions) {
        const sel = document.querySelector(`input[name="${q.id}"]:checked`);
        if (sel) session.answers[q.id] = parseInt(sel.value, 10);
      }
      submit();
    },
  );
}

function renderBreak(container, paperNumber, nextSectionIdx) {
  const [, label, jaLabel] = SECTIONS[nextSectionIdx];
  let remain = BREAK_SECONDS;
  container.innerHTML = `
    <article class="sitting-break">
      <h2>Break</h2>
      <p class="page-lede">Stretch. Get water. Section <strong>${nextSectionIdx + 1}</strong> (${esc(label)} / <span lang="ja">${esc(jaLabel)}</span>) starts in <strong id="break-countdown">${remain}</strong>s.</p>
      <div class="sitting-break-actions">
        <a class="btn-primary" href="#/sitting/${paperNumber}/${nextSectionIdx}" id="skip-break">Skip break, start now</a>
      </div>
    </article>
  `;
  if (timerHandle) clearInterval(timerHandle);
  timerHandle = setInterval(() => {
    remain -= 1;
    const el = document.getElementById('break-countdown');
    if (el) el.textContent = String(remain);
    if (remain <= 0) {
      clearInterval(timerHandle);
      timerHandle = null;
      location.hash = `#/sitting/${paperNumber}/${nextSectionIdx}`;
    }
  }, 1000);
}

function renderResult(container, paperNumber) {
  if (!session || !session.sectionResults || session.sectionResults.length < SECTIONS.length) {
    container.innerHTML = `<p>No completed sitting in memory. <a href="#/sitting">Start again.</a></p>`;
    return;
  }
  let totalCorrect = 0, totalQs = 0;
  for (const r of session.sectionResults) {
    totalCorrect += r.correct;
    totalQs += r.total;
  }
  const pct = totalQs > 0 ? Math.round(100 * totalCorrect / totalQs) : 0;
  // IMP-121 (audit round-9): real JLPT N5 pass thresholds.
  // - Per-section raw minimum (approximated to app's 30Q/31Q/24Q
  //   structure): ~63% Section 1, ~61% Section 2, ~79% Section 3.
  //   Real JLPT is 19/60 raw per section (after scaling).
  // - Overall: 80/180 scaled = 44.4%, but as a raw-question approximation
  //   on the 85Q app, that's ~38/85 (~45%). The 60% study target is the
  //   conservative pedagogical bar (matches Bunpro / Try! N5 guidance).
  const PASS = 60;                  // study target (conservative)
  const SECTION_MIN_PCT = [63, 61, 79];  // per-section raw minimums
  const SECTION_MIN_LABEL = '~19 / section';
  // Per-section pass test against the section-specific minimum
  const sectionPasses = session.sectionResults.map((r, i) => {
    const p = r.total ? (100 * r.correct / r.total) : 0;
    return p >= SECTION_MIN_PCT[i];
  });
  const allSectionMinsMet = sectionPasses.every(Boolean);
  container.innerHTML = `
    <article class="sitting-result">
      <h2>JLPT N5 Mock - Paper ${paperNumber} - Result</h2>
      <p class="page-lede">
        Total: <strong>${totalCorrect} / ${totalQs}</strong> (${pct}%) ·
        ${pct >= PASS && allSectionMinsMet
          ? `<span class="pass-badge pass">Pass · all section minimums met</span>`
          : pct >= PASS
            ? `<span class="pass-badge fail">Overall ${pct}% (≥${PASS}%) but a section is below its minimum</span>`
            : `<span class="pass-badge fail">Below ${PASS}% study-target</span>`}
      </p>
      <p class="muted small" style="margin-top:-4px;">
        Real JLPT N5 official pass mark = 80 / 180 (44.4%) with section minimums of 19 / 60 (~32% per section after scoring scale). Study target ≥ ${PASS}% is the conservative bar matching Bunpro / Try! N5 guidance.
      </p>
      <table class="category-table">
        <thead>
          <tr>
            <th>Section</th>
            <th>Score</th>
            <th>%</th>
            <th>Section minimum</th>
          </tr>
        </thead>
        <tbody>
          ${session.sectionResults.map((r, i) => {
            const p = r.total ? Math.round(100 * r.correct / r.total) : 0;
            const cls = sectionPasses[i] ? 'pass' : 'fail';
            const minStatus = sectionPasses[i] ? '✓ met' : `✗ ${SECTION_MIN_PCT[i]}%`;
            return `<tr class="${cls}"><td>${esc(r.label)} <span class="muted small" lang="ja">(${esc(r.jaLabel)})</span></td><td>${r.correct} / ${r.total}</td><td>${p}%</td><td class="muted small">${minStatus}</td></tr>`;
          }).join('')}
        </tbody>
        <tfoot>
          <tr><th>Total</th><th>${totalCorrect} / ${totalQs}</th><th>${pct}%</th><th class="muted small">≥ ${PASS}% target</th></tr>
        </tfoot>
      </table>
      <p class="muted small">
        ※ The app ships 85Q across the 3 sections (close to the official 91Q). Per-section minimums above are raw-question approximations. The official JLPT N5 score report uses a scaled-equating method that this app does not replicate — only raw-correct percentages are shown.
      </p>
      <div class="test-nav">
        <a class="btn-primary" href="#/sitting">Try another paper</a>
        <a class="btn-secondary" href="#/home">Home</a>
      </div>
    </article>
  `;
  // Reset session so a future click on a paper starts fresh.
  session = null;
}
