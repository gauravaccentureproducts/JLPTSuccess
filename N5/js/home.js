// Home / landing screen - JLPT N5 syllabus dashboard.
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
import { t, currentLocale } from './i18n.js';
// EB-4 (round-9 close-out, 2026-05-07): pedagogy-rule recommender.
// Replaces the v2.0 ML-recommender ask with on-device expert rules.
// See docs/RECOMMENDER-RULES.md for the rule catalogue + privacy
// guarantees. The import is static so esbuild bundles it into
// js/min/home.js; no runtime fetch.
import { gatherSignal, recommend as recommendNext } from './pedagogy-recommender.js';
// SVA-NEXT-3 (round-9 follow-up, 2026-05-08): override-able home
// background glyph (五 by default).
import { getBranding } from './branding.js';

// Cache the corpus counts and pattern label map at module scope so we
// fetch each data file once per session.
let corpusCounts = null;
let patternLabels = null;  // patternId → friendly label (e.g. "n5-001 - です/だ")
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
  // show "n5-001 - です/だ" instead of the bare ID. Falls back to the
  // bare ID if the pattern lookup fails for any reason.
  if (grammar && Array.isArray(grammar.patterns)) {
    patternLabels = {};
    for (const p of grammar.patterns) {
      if (!p?.id) continue;
      // Prefer the canonical 'pattern' field (the form Japanese learners
      // recognize, e.g. "〜は です"); fall back to 'name' or 'meaning_en'.
      const label = p.pattern || p.name || p.meaning_en || '';
      patternLabels[p.id] = label
        ? `${p.id} - ${label}`
        : p.id;
    }
  }
  return corpusCounts;
}

// Render a number using the active locale's grouping convention.
// IMP-110 (round-8 audit, 2026-05-06): when locale=hi, use Indian
// grouping ('hi-IN' → lakh boundary, e.g. 1,00,000); when locale=en,
// use US grouping (1,003 → "1,003"). Falls back to en-US.
const fmt = (n) => {
  const tag = currentLocale() === 'hi' ? 'hi-IN' : 'en-US';
  return Intl.NumberFormat(tag).format(n || 0);
};

// Compute current progress per syllabus section. Reads localStorage -
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

// 8 study-order steps per spec §5.1 - ordered, beginner-friendly, no
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

  // IMP-024 + IMP-027 (audit round-3): surface (a) reviews completed
  // today vs the user's goal and (b) the FSRS-due queue size,
  // prominently on the home dashboard. Both link straight to #/review.
  const reviewsToday = storage.getReviewsToday ? storage.getReviewsToday() : 0;
  const dailyGoal    = storage.getDailyGoal ? storage.getDailyGoal() : 20;
  const goalPct      = Math.min(100, Math.round(100 * reviewsToday / dailyGoal));
  // IMP-092 Phase 2A (audit round-9, 2026-05-07): home page now shows
  // the unified due-count across grammar + vocab + kanji (was grammar-
  // only). The previous getDueCount() lookup is preserved for any other
  // call sites; the home aggregate uses the per-skill breakdown sum.
  const _dueBySkill  = storage.getDueCountsBySkill
    ? storage.getDueCountsBySkill()
    : { grammar: storage.getDueCount ? storage.getDueCount() : 0, vocab: 0, kanji: 0 };
  const dueCount     = _dueBySkill.grammar + _dueBySkill.vocab + _dueBySkill.kanji;
  const dueBreakdown = (_dueBySkill.vocab > 0 || _dueBySkill.kanji > 0)
    ? `<span class="muted small" style="margin-left:6px;">(${_dueBySkill.grammar} grammar · ${_dueBySkill.vocab} vocab · ${_dueBySkill.kanji} kanji)</span>`
    : '';
  // IMP-036 (audit round-3): 7-day review forecast bar chart.
  const forecast = storage.getReviewForecast ? storage.getReviewForecast(7) : [];
  const forecastMax = Math.max(1, ...forecast.map(f => f.count));

  // Resume strip - single-line link above the syllabus title for returning
  // users. First-time visitors see no strip at all. Show the friendly
  // pattern label ("n5-001 - です/だ") instead of just the ID when the
  // grammar lookup map is loaded.
  const resumeLabel = (patternLabels && patternLabels[lastViewed])
    || lastViewed;
  const resumeStrip = (isReturning && lastViewed)
    ? `<a class="resume-strip" href="#/learn/${encodeURIComponent(lastViewed)}">Last session: ${esc(resumeLabel)}.</a>`
    : '';

  // Q44 onboarding "first 60 seconds" path (lowest-effort lane: starter-set).
  // For brand-new users who skipped or finished the diagnostic, surface a
  // curated 5-pattern starter pack — the foundational grammatical machinery
  // every N5 learner needs first. The 5 are chosen by frequency × didactic
  // weight, not by lesson order: です (sentences), は (topic marker), Verb-ます
  // (polite verbs), い-adjectives (sentence with [adj]), か (questions).
  // Once the user opens any of them, they appear in `history` and this strip
  // disappears (becomes the "Last session" resume strip instead).
  const STARTER_PATTERNS = [
    { id: 'n5-001', label: 'です／〜ます', why: 'How sentences end politely' },
    { id: 'n5-002', label: 'は',            why: 'The topic marker' },
    { id: 'n5-058', label: 'Verb-ます',    why: 'Polite verb form' },
    { id: 'n5-077', label: 'い-Adjectives', why: 'Describing things' },
    { id: 'n5-024', label: 'か',            why: 'Asking questions' },
  ];
  // EB-4: pedagogy recommender. The recommender returns a structured
  // suggestion (highest-priority rule that fires for current state).
  // For new users this typically lands as R-05 starter-pack (already
  // surfaced separately below as `starterStrip`), so we suppress the
  // duplicate by gating recCard to returning users only. Pure +
  // deterministic + on-device — see docs/RECOMMENDER-RULES.md.
  // IMP-NEXT-1 (round-9 follow-up, 2026-05-08): Settings toggle to
  // disable the card. Default-on; only suppressed when the user
  // explicitly toggles it off. Setting lives at storage.settings
  // .showRecommender; home.js reads it on every render.
  const showRecommender = settings.showRecommender !== false;
  let recCard = '';
  try {
    if (isReturning && showRecommender) {
      const rec = recommendNext(gatherSignal({ corpusCounts: counts }));
      if (rec) {
        const loc = currentLocale();
        const label = loc === 'hi' ? rec.label_hi : rec.label_en;
        const why   = loc === 'hi' ? rec.why_hi   : rec.why_en;
        recCard = `
          <aside class="home-recommend" aria-labelledby="home-recommend-h">
            <h3 id="home-recommend-h" class="home-recommend-title">${esc(t('home.recommend_title') || 'Recommended next')}</h3>
            <a class="home-recommend-action" href="${esc(rec.href)}">
              <span class="home-recommend-label"><strong>${esc(label)}</strong></span>
              <span class="home-recommend-meta muted small">${esc(rec.duration)} · ${esc(rec.rule_id)}</span>
            </a>
            <p class="home-recommend-why muted small">${esc(why)}</p>
          </aside>
        `;
      }
    }
  } catch (e) {
    // Non-fatal: recommender is decorative. Surface in console for
    // dev diagnosis, never break the home render.
    if (typeof console !== 'undefined') console.warn('[recommender] suppressed:', e);
  }

  const starterStrip = (!isReturning) ? `
    <aside class="starter-pack" aria-labelledby="starter-pack-h">
      <h3 id="starter-pack-h" class="starter-pack-title">New to JLPT N5? Start here.</h3>
      <p class="starter-pack-lede muted small">These 5 patterns are the foundation — every other N5 grammar pattern builds on these. Tap any one to read the explanation, examples, and common mistakes. Roughly <strong>5 minutes per pattern</strong>.</p>
      <ol class="starter-pack-list">
        ${STARTER_PATTERNS.map((p, i) => `
          <li>
            <a href="#/learn/${encodeURIComponent(p.id)}" class="starter-pack-card">
              <span class="starter-pack-num">${i + 1}</span>
              <span class="starter-pack-meta">
                <strong lang="ja">${esc(p.label)}</strong>
                <small>${esc(p.why)}</small>
              </span>
            </a>
          </li>
        `).join('')}
      </ol>
      <p class="starter-pack-foot muted small">Or take the <a href="#/diagnostic">10-question diagnostic</a> to see what you already know.</p>
    </aside>
  ` : '';

  container.innerHTML = `
    <section class="home-syllabus">
      <p class="home-up-link">
        <a href="#/levels">← All JLPT levels</a>
      </p>
      ${resumeStrip}
      ${starterStrip}

      <header class="syllabus-header">
        <span class="syllabus-watermark" aria-hidden="true">${esc((getBranding()?.brand?.home_glyph) || '五')}</span>
        <h1 class="syllabus-title">${t('home.syllabus_title')}</h1>
        <p class="syllabus-subtitle">${t('home.syllabus_subtitle')}</p>
        <!-- ISSUE-027 / IMP-048 (audit round-4): privacy / niche-N2
             trust band. Surfaces the most-defensible competitive claim
             on first paint. 2026-05-05: trust pills now use t() so
             they translate when the locale chip switches. -->
        <p class="syllabus-trust-band" aria-label="Trust signals">
          <span class="trust-pill"><span aria-hidden="true">●</span> ${t('trust.no_login')}</span>
          <span class="trust-pill"><span aria-hidden="true">●</span> ${t('trust.no_tracking')}</span>
          <a class="trust-pill" href="${'./' /* placeholder for install hook */}" data-trust-install title="Install for offline use"><span aria-hidden="true">●</span> ${t('trust.works_offline')}</a>
          <a class="trust-pill" href="https://github.com/gauravaccentureproducts/JLPTSuccess/blob/master/LICENSE" target="_blank" rel="noopener" title="MIT licensed source · CC BY-SA content"><span aria-hidden="true">●</span> ${t('trust.open_source')}</a>
          <a class="trust-pill" href="PRIVACY.md" target="_blank" rel="noopener" title="No data leaves your device"><span aria-hidden="true">●</span> ${t('trust.on_device')}</a>
          <span class="trust-pill" title="Free, forever. No ads, no paywall, no upsell."><span aria-hidden="true">●</span> ${t('trust.free_no_paywall')}</span>
        </p>
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
            <a class="syllabus-daily-progress" href="#/review" title="Open today's review queue">
              <span class="syllabus-daily-progress-label">${t('home.today_label')}: <strong>${reviewsToday}</strong> / ${dailyGoal}</span>
              <span class="syllabus-daily-progress-bar" aria-hidden="true">
                <span class="syllabus-daily-progress-fill" style="width:${goalPct}%"></span>
              </span>
            </a>
            ${dueCount > 0 ? `
              <a class="syllabus-daily-due" href="#/review">
                ${t('home.reviews_due', { n: `<strong>${dueCount}</strong>` })}${dueBreakdown}
              </a>
            ` : `
              <span class="syllabus-daily-due is-empty">${t('home.no_reviews_due')}</span>
            `}
            <span class="syllabus-daily-today ${dailyGoalMet ? 'is-met' : 'is-pending'}">
              <span class="syllabus-daily-mark" aria-hidden="true">${dailyGoalMet ? '✓' : '○'}</span>
              <span class="syllabus-daily-text">${dailyGoalMet ? t('home.practiced_today') : t('home.not_yet_practiced')}</span>
            </span>
          </div>
        ` : ''}
      </header>

      ${recCard}

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

      ${isReturning && forecast.length ? `
        <!-- IMP-036 (audit round-3): 7-day review forecast.
             Aggregates FSRS-4 nextDue dates from grammar + vocab + kanji
             histories so the learner sees "tomorrow I'll have 8 reviews;
             Wednesday I'll have 25 - better stay on top of it". -->
        <section class="syllabus-forecast" aria-label="Review forecast">
          <header class="section-label">
            <span class="section-label-text">${t('home.forecast_label')}</span>
            <span class="section-label-rule" aria-hidden="true"></span>
          </header>
          <ol class="forecast-bar-chart">
            ${forecast.map(b => {
              const h = b.count === 0 ? 4 : Math.max(8, Math.round(56 * b.count / forecastMax));
              return `
                <li class="forecast-bar">
                  <span class="forecast-bar-count">${b.count}</span>
                  <span class="forecast-bar-track" aria-hidden="true">
                    <span class="forecast-bar-fill" style="height:${h}px"></span>
                  </span>
                  <span class="forecast-bar-label muted small">${esc(b.label)}</span>
                </li>
              `;
            }).join('')}
          </ol>
          <p class="muted small" style="margin-top:6px;">
            <a href="#/missed">Browse wrong-answer history →</a>
          </p>
        </section>
      ` : ''}

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
