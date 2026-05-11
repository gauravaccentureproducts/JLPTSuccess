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
// IMP-WAVE3 (UI audit fix, 2026-05-11): syllabus cards now localized via i18n.
// Keys live under `home.card_<id>_*` in locales/{en,hi}.json. fmt() preserves
// per-locale Indian/US number grouping.
function syllabusCards(counts) {
  const localCount = (key, n) => {
    const tpl = t(`home.${key}`);
    if (typeof tpl === 'string' && tpl.includes('${n}')) return tpl.replace('${n}', fmt(n));
    return tpl;
  };
  return [
    {
      idx: '01', id: 'grammar',
      title: t('home.card_grammar_title'),
      count: localCount('card_grammar_count', counts.grammar),
      desc: t('home.card_grammar_desc'),
      href: '#/learn/grammar',
      action: t('home.card_grammar_action'),
    },
    {
      idx: '02', id: 'vocab',
      title: t('home.card_vocab_title'),
      count: localCount('card_vocab_count', counts.vocab),
      desc: t('home.card_vocab_desc'),
      href: '#/learn/vocab',
      action: t('home.card_vocab_action'),
    },
    {
      idx: '03', id: 'kanji',
      title: t('home.card_kanji_title'),
      count: localCount('card_kanji_count', counts.kanji),
      desc: t('home.card_kanji_desc'),
      href: '#/kanji',
      action: t('home.card_kanji_action'),
    },
    {
      idx: '04', id: 'reading',
      title: t('home.card_reading_title'),
      count: localCount('card_reading_count', counts.reading),
      desc: t('home.card_reading_desc'),
      href: '#/reading',
      action: t('home.card_reading_action'),
    },
    {
      idx: '05', id: 'listening',
      title: t('home.card_listening_title'),
      count: localCount('card_listening_count', counts.listening),
      desc: t('home.card_listening_desc'),
      href: '#/listening',
      action: t('home.card_listening_action'),
    },
    {
      idx: '06', id: 'test',
      title: t('home.card_test_title'),
      count: t('home.card_test_count'),
      desc: t('home.card_test_desc'),
      href: '#/test',
      action: t('home.card_test_action'),
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
// IMP-144 (richness audit, 2026-05-09): the "Review" CTA points at the
// SRS queue, which already round-robins grammar + vocab + kanji per
// IMP-092 Phase 2B. Renaming it "Mixed drill (SRS)" surfaces that
// multi-skill nature on the home study path so learners understand
// they're getting one mixed 15-min session, not three separate review
// loops.
// IMP-WAVE3 (UI audit fix, 2026-05-11): study-order steps now localized via i18n.
// Localized at render time so the locale swap is live.
function studyOrder() {
  return [
    { text: t('home.study_step_grammar'),   href: '#/learn/grammar' },
    { text: t('home.study_step_vocab'),     href: '#/learn/vocab' },
    { text: t('home.study_step_kanji'),     href: '#/kanji' },
    { text: t('home.study_step_drill'),     href: '#/drill' },
    { text: t('home.study_step_reading'),   href: '#/reading' },
    { text: t('home.study_step_listening'), href: '#/listening' },
    { text: t('home.study_step_test'),      href: '#/test' },
    { text: t('home.study_step_review'),    href: '#/review' },
    // IMP-126 (richness audit, 2026-05-09): authentic real-world JP
    // (signs / menus / transit / shop / notice).
    { text: t('home.study_step_authentic'), href: '#/authentic' },
  ];
}

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
        <span class="progress-value">${esc(t('home.progress_not_attempted'))}</span>
      </li>
    `;
  }
  const pct = p.total > 0 ? Math.min(100, Math.round((p.done / p.total) * 100)) : 0;
  // IMP-WAVE3: compare against canonical test label for mock-percentage format.
  const valueText = (label === t('home.progress_label_test') || label === 'Mock Test')
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

  // EB-4: pedagogy recommender. The recommender returns a structured
  // suggestion (highest-priority rule that fires for current state).
  // Gated to returning users only — pure + deterministic + on-device.
  // See docs/RECOMMENDER-RULES.md.
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

  container.innerHTML = `
    <section class="home-syllabus">
      <p class="home-up-link">
        <a href="#/levels">← All JLPT levels</a>
      </p>
      ${resumeStrip}

      ${isReturning ? `
        <div class="syllabus-daily-status">
          <span class="syllabus-daily-streak">Streak: ${streak?.current ?? 0} ${(streak?.current ?? 0) === 1 ? 'day' : 'days'}</span>
          <a class="syllabus-daily-progress" href="#/review" title="Open today's mixed-skill review queue (grammar + vocab + kanji SRS)">
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

      ${recCard}

      <section class="syllabus-overview" aria-label="Syllabus overview">
        <header class="section-label">
          <span class="section-label-text">${esc(t('home.syllabus_section_label'))}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <div class="syllabus-grid">
          ${cards.map(renderSyllabusCard).join('')}
        </div>
      </section>

      <section class="syllabus-study-order" aria-label="Recommended study order">
        <header class="section-label">
          <span class="section-label-text">${esc(t('home.study_order_section_label'))}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ol class="study-order-list">
          ${studyOrder().map((step, i) => `
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
          <span class="section-label-text">${esc(t('home.progress_section_label'))}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ul class="progress-list">
          ${renderProgressRow(t('home.progress_label_grammar'), progress.grammar)}
          ${renderProgressRow(t('home.progress_label_vocab'), progress.vocab)}
          ${renderProgressRow(t('home.progress_label_kanji'), progress.kanji)}
          ${renderProgressRow(t('home.progress_label_reading'), progress.reading)}
          ${renderProgressRow(t('home.progress_label_listening'), progress.listening)}
          ${renderProgressRow(t('home.progress_label_test'), progress.mockTest)}
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
        <p class="syllabus-action-prompt">${esc(t('home.action_prompt'))}</p>
        <div class="syllabus-action-buttons">
          <a class="btn-action btn-action-primary" href="#/diagnostic">${esc(t('home.action_placement'))}</a>
          <a class="btn-action btn-action-secondary" href="#/learn/grammar">${esc(t('home.action_start_grammar'))}</a>
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
