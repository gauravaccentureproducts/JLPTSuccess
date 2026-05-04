// Home / landing screen — JLPT N5 syllabus dashboard.
//
// Redesigned 2026-05-02 from the bare "study material." inventory hero into a
// full syllabus control center. Sections, in order:
//   1. Optional resume strip (returning users only).
//   2. Page title: "JLPT N5 Syllabus" + subtitle.
//   3. Syllabus overview: 6 cards (Grammar / Vocab / Kanji / Reading /
//      Listening / Mock Test) with count, description, and action link.
//   4. Recommended study order: 8-step ordered list.
//   5. Progress overview: 6 rows with progress bars (Grammar / Vocab / Kanji /
//      Reading / Listening / Mock Test).
//   6. Placement action block: "Not sure where to start?" + 2 buttons.
//
// Counts in the syllabus cards are read live from data/*.json so the page
// stays accurate as content changes. Progress is computed from localStorage
// (knownKanji + knownVocab + history.isMastered/isManuallyKnown). Reading
// and Listening don't currently track per-passage completion, so they show
// 0/30 until that feature lands.
//
// Copy register: describe contents, no marketing language. No "Master JLPT
// N5" / "Your ultimate study companion" / "Start your journey." Counts are
// bare numerals + nouns. (Spec §5.1.1, mandatory.)
import * as storage from './storage.js';

// Cache the corpus counts and pattern label map at module scope so we
// fetch each data file once per session.
let corpusCounts = null;
let patternLabels = null;  // patternId → friendly label (e.g. "n5-001 — です/だ")
async function loadCorpusCounts() {
  if (corpusCounts) return corpusCounts;
  const files = ['grammar', 'vocab', 'kanji', 'reading', 'listening'];
  const fetches = files.map(name =>
    fetch(`data/${name}.json`)
      .then(r => r.ok ? r.json() : null)
      .catch(() => null)
  );
  const [grammar, vocab, kanji, reading, listening] = await Promise.all(fetches);
  // Each data file uses a different top-level key for its main array.
  const count = (d, ...keys) => {
    if (!d) return 0;
    for (const k of keys) {
      if (Array.isArray(d[k])) return d[k].length;
    }
    return 0;
  };
  corpusCounts = {
    grammar: count(grammar, 'patterns'),
    vocab: count(vocab, 'entries'),
    kanji: count(kanji, 'entries'),
    reading: count(reading, 'passages'),
    listening: count(listening, 'items'),
  };
  // Build the pattern-id → friendly-label map so the resume strip can
  // show "n5-001 — です/だ" instead of the bare ID. Falls back to the
  // bare ID if the pattern lookup fails for any reason.
  if (grammar && Array.isArray(grammar.patterns)) {
    patternLabels = {};
    for (const p of grammar.patterns) {
      if (!p?.id) continue;
      // Prefer the canonical 'pattern' field (the form Japanese learners
      // recognize, e.g. "〜は です"); fall back to 'name' or 'meaning_en'.
      const label = p.pattern || p.name || p.meaning_en || '';
      patternLabels[p.id] = label
        ? `${p.id} — ${label}`
        : p.id;
    }
  }
  return corpusCounts;
}

// Render a number with US-locale thousands separators (1003 → "1,003"). Bare
// digits otherwise. Per spec §5.1 rule 4.
const fmt = (n) => Intl.NumberFormat('en-US').format(n || 0);

// Compute current progress per syllabus section. Reads localStorage —
// completely cold (first-time visitors) returns zeros for every section.
function computeProgress(counts) {
  const history = storage.getHistory();
  const knownKanji = storage.getKnownKanji ? storage.getKnownKanji() : {};
  const knownVocab = storage.getKnownVocab ? storage.getKnownVocab() : {};
  const results = storage.getResults();

  // Grammar: pattern is "studied" when SRS has graduated it OR the user
  // marked it manually known. Mirrors the Mark-as-known affordance on the
  // grammar detail page.
  const grammarStudied = Object.values(history)
    .filter(v => v && (v.isMastered || v.isManuallyKnown))
    .length;

  // Vocab + Kanji: count of explicit "known" flags (set via the
  // Mark-as-known checkbox on the detail pages).
  const vocabKnown = Object.keys(knownVocab).length;
  const kanjiKnown = Object.keys(knownKanji).length;

  // Reading + Listening: per-item completion is recorded in storage by
  // js/reading.js (on first results screen with score>0) and
  // js/listening.js (on first answer submit). The dashboard reflects the
  // count of unique passages / drills the user has engaged with.
  const completedReading = storage.getCompletedReading
    ? storage.getCompletedReading() : {};
  const completedListening = storage.getCompletedListening
    ? storage.getCompletedListening() : {};
  const readingDone = Object.keys(completedReading).length;
  const listeningDone = Object.keys(completedListening).length;

  // Mock Test: most recent result if any.
  const lastTest = results.length ? results[results.length - 1] : null;

  return {
    grammar:   { done: grammarStudied,   total: counts.grammar },
    vocab:     { done: vocabKnown,       total: counts.vocab },
    kanji:     { done: kanjiKnown,       total: counts.kanji },
    reading:   { done: readingDone,      total: counts.reading },
    listening: { done: listeningDone,    total: counts.listening },
    mockTest:  lastTest
      ? { done: lastTest.correct, total: lastTest.total, percent: lastTest.percent }
      : { done: 0, total: 0, percent: null, notAttempted: true },
  };
}

// Single source of truth for the 6 syllabus cards. Description + action copy
// stays in sync with what the linked page actually contains. Update the
// description whenever a section's scope changes.
function syllabusCards(counts) {
  return [
    {
      idx: '01', id: 'grammar',
      title: 'Grammar',
      count: `${fmt(counts.grammar)} patterns`,
      desc: 'Basic sentence structure, particles, verb forms, adjectives, comparison, requests, and common N5 expressions.',
      href: '#/learn/grammar',
      action: 'Open Grammar Syllabus',
    },
    {
      idx: '02', id: 'vocab',
      title: 'Vocabulary',
      count: `${fmt(counts.vocab)} words`,
      desc: 'Daily life words, time expressions, family, food, school, travel, verbs, adjectives, and common expressions.',
      href: '#/learn/vocab',
      action: 'Open Vocabulary List',
    },
    {
      idx: '03', id: 'kanji',
      title: 'Kanji',
      count: `${fmt(counts.kanji)} characters`,
      desc: 'Numbers, time, people, school, directions, nature, common verbs, and basic recognition kanji.',
      href: '#/kanji',
      action: 'Open Kanji List',
    },
    {
      idx: '04', id: 'reading',
      title: 'Reading',
      count: `${fmt(counts.reading)} passages`,
      desc: 'Short notices, simple messages, daily-life paragraphs, and basic comprehension practice.',
      href: '#/reading',
      action: 'Start Reading Practice',
    },
    {
      idx: '05', id: 'listening',
      title: 'Listening',
      count: `${fmt(counts.listening)} drills`,
      desc: 'Greetings, classroom phrases, daily conversations, time, shopping, directions, and simple Q&A.',
      href: '#/listening',
      action: 'Start Listening Practice',
    },
    {
      idx: '06', id: 'test',
      title: 'Mock Test',
      count: '15 questions',
      desc: 'Auto-scored mock test with correct answers, explanations, and weak-area review.',
      href: '#/test',
      action: 'Take Mock Test',
    },
  ];
}

// 8 study-order steps per spec §5.1 — ordered, beginner-friendly, no
// promotional framing. Each step is a sentence, no period (matches list
// register elsewhere on the site). Each step links to the most directly-
// actionable surface (per user request 2026-05-02): grammar/vocab/kanji
// land on the canonical learn TOCs; "Practice grammar questions" routes
// to the daily Drill (the grammar-question practice loop, distinct from
// the mock test); "Review weak areas" routes to the SRS Review queue.
const STUDY_ORDER = [
  { text: 'Learn basic sentence structure and particles', href: '#/learn/grammar' },
  { text: 'Study core vocabulary',                         href: '#/learn/vocab' },
  { text: 'Learn basic kanji recognition',                 href: '#/kanji' },
  { text: 'Practice grammar questions',                    href: '#/drill' },
  { text: 'Practice short reading passages',               href: '#/reading' },
  { text: 'Practice listening drills',                     href: '#/listening' },
  { text: 'Take the mock test',                            href: '#/test' },
  { text: 'Review weak areas',                             href: '#/review' },
];

function renderSyllabusCard(card) {
  return `
    <a class="syllabus-card" href="${card.href}" data-section="${card.id}">
      <p class="syllabus-card-index" aria-hidden="true">${card.idx}</p>
      <h3 class="syllabus-card-title">${card.title}</h3>
      <p class="syllabus-card-count">${esc(card.count)}</p>
      <p class="syllabus-card-desc">${esc(card.desc)}</p>
      <span class="syllabus-card-action">${esc(card.action)} <span aria-hidden="true">→</span></span>
    </a>
  `;
}

function renderProgressRow(label, p) {
  if (p.notAttempted) {
    return `
      <li class="progress-row">
        <span class="progress-label">${esc(label)}</span>
        <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:0%"></span></span>
        <span class="progress-value">Not attempted</span>
      </li>
    `;
  }
  const pct = p.total > 0 ? Math.min(100, Math.round((p.done / p.total) * 100)) : 0;
  const valueText = label === 'Mock Test'
    ? `${p.done} / ${p.total} (${p.percent ?? pct}%)`
    : `${fmt(p.done)} / ${fmt(p.total)}`;
  return `
    <li class="progress-row">
      <span class="progress-label">${esc(label)}</span>
      <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:${pct}%"></span></span>
      <span class="progress-value">${valueText}</span>
    </li>
  `;
}

export async function renderHome(container) {
  const history = storage.getHistory();
  const results = storage.getResults();
  const isReturning = Object.keys(history).length > 0 || results.length > 0;
  const settings = storage.getSettings();
  const lastViewed = settings.lastLearnId || null;
  const counts = await loadCorpusCounts();
  const progress = computeProgress(counts);
  const cards = syllabusCards(counts);

  // Daily-goal-met badge: shows ✓ when the user has practiced at least
  // once today (any action that records a study day in the streak
  // tracker). Decoupled from the streak count so a returning user sees
  // separately "current streak: 5" + "today: ✓ done" / "today: not yet."
  const streak = storage.getStreak ? storage.getStreak() : null;
  const todayKey = (() => {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  })();
  const dailyGoalMet = isReturning && streak && streak.lastStudyDate === todayKey;

  // Resume strip — single-line link above the syllabus title for returning
  // users. First-time visitors see no strip at all. Show the friendly
  // pattern label ("n5-001 — です/だ") instead of just the ID when the
  // grammar lookup map is loaded.
  const resumeLabel = (patternLabels && patternLabels[lastViewed])
    || lastViewed;
  const resumeStrip = (isReturning && lastViewed)
    ? `<a class="resume-strip" href="#/learn/${encodeURIComponent(lastViewed)}">Last session: ${esc(resumeLabel)}.</a>`
    : '';

  container.innerHTML = `
    <section class="home-syllabus">
      <p class="home-up-link">
        <a href="#/levels">← All JLPT levels</a>
      </p>
      ${resumeStrip}

      <header class="syllabus-header">
        <span class="syllabus-watermark" aria-hidden="true">五</span>
        <h1 class="syllabus-title">JLPT N5 Syllabus</h1>
        <p class="syllabus-subtitle">Study grammar, vocabulary, kanji, reading, and listening in a structured order.</p>
        <ul class="syllabus-stat-pills" aria-label="Corpus size">
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${fmt(counts.grammar)}</span><span class="syllabus-stat-lbl">grammar patterns</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${fmt(counts.vocab)}</span><span class="syllabus-stat-lbl">vocab words</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${fmt(counts.kanji)}</span><span class="syllabus-stat-lbl">kanji</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${fmt(counts.reading)}</span><span class="syllabus-stat-lbl">reading passages</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${fmt(counts.listening)}</span><span class="syllabus-stat-lbl">listening drills</span></li>
        </ul>
        ${isReturning ? `
          <div class="syllabus-daily-status">
            <span class="syllabus-daily-streak">Streak: ${streak?.current ?? 0} ${(streak?.current ?? 0) === 1 ? 'day' : 'days'}</span>
            <span class="syllabus-daily-today ${dailyGoalMet ? 'is-met' : 'is-pending'}">
              <span class="syllabus-daily-mark" aria-hidden="true">${dailyGoalMet ? '✓' : '○'}</span>
              <span class="syllabus-daily-text">${dailyGoalMet ? 'Practiced today' : 'Not yet practiced today'}</span>
            </span>
          </div>
        ` : ''}
      </header>

      <section class="syllabus-overview" aria-label="Syllabus overview">
        <header class="section-label">
          <span class="section-label-text">Syllabus</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <div class="syllabus-grid">
          ${cards.map(renderSyllabusCard).join('')}
        </div>
      </section>

      <section class="syllabus-study-order" aria-label="Recommended study order">
        <header class="section-label">
          <span class="section-label-text">Recommended Study Order</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ol class="study-order-list">
          ${STUDY_ORDER.map((step, i) => `
            <li class="study-order-item">
              <a class="study-order-link" href="${step.href}">
                <span class="study-order-num" aria-hidden="true">${String(i + 1).padStart(2, '0')}</span>
                <span class="study-order-text">${esc(step.text)}</span>
              </a>
            </li>
          `).join('')}
        </ol>
      </section>

      <section class="syllabus-progress" aria-label="Progress overview">
        <header class="section-label">
          <span class="section-label-text">Progress</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ul class="progress-list">
          ${renderProgressRow('Grammar', progress.grammar)}
          ${renderProgressRow('Vocabulary', progress.vocab)}
          ${renderProgressRow('Kanji', progress.kanji)}
          ${renderProgressRow('Reading', progress.reading)}
          ${renderProgressRow('Listening', progress.listening)}
          ${renderProgressRow('Mock Test', progress.mockTest)}
        </ul>
      </section>

      <section class="syllabus-action" aria-label="Where to start">
        <p class="syllabus-action-prompt">Not sure where to start?</p>
        <div class="syllabus-action-buttons">
          <a class="btn-action btn-action-primary" href="#/diagnostic">Take Placement Check</a>
          <a class="btn-action btn-action-secondary" href="#/learn/grammar">Start with Grammar</a>
        </div>
      </section>
    </section>
  `;
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
