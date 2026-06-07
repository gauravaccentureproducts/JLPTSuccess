// Router + chapter coordinator.
import { initStorage, getDueCount, recordStudyToday, getHistory, getResults, getStreak } from './storage.js';
import { parseRoute, navigateTo, urlForRoute, getBasePath } from './router.js';
import { initFuriganaToggle } from './furigana.js';
import { renderLearn } from './learn.js';
import { renderTest } from './test.js';
import { renderReview } from './review.js';
import { renderSummary } from './summary.js';
import { renderDrill } from './drill.js';
import { renderDiagnostic } from './diagnostic.js';
import { renderSettings, applyTheme, applyFontSize, applyAudioRate, applyReduceMotion } from './settings.js';
import { initKanjiPopover } from './kanji-popover.js';
import { initShortcuts } from './shortcuts.js';
import { initSearch } from './search.js';
import { initPwa } from './pwa.js';
import { renderKosoado } from './kosoado.js';
import { renderWaGa } from './wa-vs-ga.js';
import { renderVerbClass } from './verb-class.js';
import { renderTeForm } from './te-form.js';
import { renderParticlePairs } from './particle-pairs.js';
import { renderCounters } from './counters.js';
import { renderReading } from './reading.js';
import { renderListening } from './listening.js';
import { renderKanji } from './kanji.js';
import { renderHome } from './home.js';
import { initI18n, setLocale, currentLocale, supportedLocales, enabledLocales, t } from './i18n.js';
import { renderPapers } from './papers.js';
import { renderChangelog } from './changelog.js';
import { renderFeedback } from './feedback.js';
import { renderPrivacy, renderNotices } from './md-viewer.js';
import { renderLevels, renderLevelPlaceholder } from './levels.js';
import { initContentProtection } from './content-protect.js';
import { renderMissed } from './missed.js';
import { renderSitting } from './sitting.js';
// SVA-NEXT-2.4 (round-9 follow-up, 2026-05-07): print-to-PDF mock paper.
// Routes #/print and #/print/<paperId>; renders a paper layout
// designed for paper-and-pencil consumption. See js/print-paper.js.
import { renderPrint } from './print-paper.js';
// IMP-126 (richness audit, 2026-05-09): authentic-content layer.
// Renders #/authentic — real-world JP signs / menus / transit / shop
// / notice cards. The audit's "0% authentic content across every
// surface" gap; this is the starter corpus.
import { renderAuthentic } from './authentic.js';
// IMP-WAVE1 (UI audit fix, 2026-05-11): test-strategy page that
// consumes data/test_strategy.json (T1-T6 fully authored). Route /strategy.
import { renderStrategy } from './strategy.js';
// IMP-WAVE-P4-T5 (UI audit fix, 2026-05-11): weak-area diagnostic
// dashboard that cross-references test history with the 9 diagnostic
// areas in test_strategy.json. Route #/weakareas. See js/weak-areas.js.
import { renderWeakAreas } from './weak-areas.js';
// IMP-WAVE-P4-T6 (UI audit fix, 2026-05-11): exam-day prep page
// extracted from test_strategy.json's meta_strategy block.
// Route #/examday. See js/exam-day.js.
import { renderExamDay } from './exam-day.js';
// IMP-WAVE-P4-27 (UI audit fix, 2026-05-12): JP101-parity story-mode
// listening — groups listening items by ambient_context into chained
// auto-play stories. Route #/listeningstory. See js/listening-story.js.
import { renderListeningStory } from './listening-story.js';
// IMP-151 (richness audit, 2026-05-12): Migaku-style sentence-mining
// index — unified discovery view of every vocab/kanji/grammar entry's
// authentic-card cross-links. Route #/mining. See js/mining.js.
import { renderMining } from './mining.js';
// SVA-NEXT-3 (round-9 follow-up, 2026-05-08): branding-override layer.
// Reads data/branding.json (or legacy data/theme-overrides.json) at
// boot and applies CSS tokens, brand strings, meta tags, footer
// attribution, watermark text, etc. Missing file = upstream defaults.
// See docs/SELF-HOST.md § Branding override layer.
import { loadBranding } from './branding.js';

const ROUTES = {
  home:       renderHome,
  learn:      renderLearn,
  test:       renderTest,
  drill:      renderDrill,
  review:     renderReview,
  summary:    renderSummary,
  diagnostic: renderDiagnostic,
  settings:   renderSettings,
  kosoado:    renderKosoado,
  waga:       renderWaGa,
  verbclass:  renderVerbClass,
  teform:     renderTeForm,
  particles:  renderParticlePairs,
  counters:   renderCounters,
  reading:    renderReading,
  listening:  renderListening,
  kanji:      renderKanji,
  papers:     renderPapers,
  changelog:  renderChangelog,
  feedback:   renderFeedback,
  // ISSUE-055 (round-7 deferred → fixed 2026-05-06): in-app markdown
  // viewer for PRIVACY.md + NOTICES.md (replaces raw .md links that
  // triggered downloads on mobile Safari).
  privacy:    renderPrivacy,
  notices:    renderNotices,
  missed:     renderMissed,    // IMP-008/031: wrong-answer history
  sitting:    renderSitting,   // ISSUE-020/IMP-032: full mock-paper sitting
  print:      renderPrint,     // SVA-NEXT-2.4: print-to-PDF mock paper
  authentic:  renderAuthentic, // IMP-126: authentic real-world JP signs/menus/etc.
  strategy:   renderStrategy,  // IMP-WAVE1: T1-T6 test-strategy page (data/test_strategy.json)
  weakareas:  renderWeakAreas, // IMP-WAVE-P4-T5: cross-history weak-area diagnostic dashboard
  examday:    renderExamDay,   // IMP-WAVE-P4-T6: exam-day prep page (printable checklist)
  listeningstory: renderListeningStory, // IMP-WAVE-P4-27: JP101-parity story-mode listening
  mining:     renderMining,    // IMP-151: Migaku-style sentence-mining cross-link index
  // Level-1 hierarchy: picker + 4 placeholder pages for N4-N1.
  // The actual N5 content stays at all the routes above (home, learn,
  // test, etc.) - clicking N5 on the picker navigates to #/home.
  levels:     renderLevels,
  n4:         renderLevelPlaceholder,
  n3:         renderLevelPlaceholder,
  n2:         renderLevelPlaceholder,
  n1:         renderLevelPlaceholder,
};

// parseRoute() moved to js/router.js to make it importable by every
// module that navigates (no circular-import worries). Same shape:
// returns { name, params }. Handles base-path detection AND legacy
// #/... URL rewriting via replaceState for backward compatibility.

function setActiveNav(name) {
  document.querySelectorAll('.primary-nav a').forEach(a => {
    const isActive = a.dataset.route === name;
    a.classList.toggle('active', isActive);
    // IMP-012 (audit round-3): a11y - expose the active nav link to
    // assistive tech. aria-current="page" is the canonical signal.
    if (isActive) a.setAttribute('aria-current', 'page');
    else a.removeAttribute('aria-current');
  });
  // Also publish the active route as a body data attribute so the CSS
  // can hide the primary nav + search on the level picker and on the
  // N4-N1 placeholder pages (no point showing nav into N5 content
  // when the user explicitly chose a different / unbuilt level).
  document.body.dataset.route = name;
}


function refreshDrillBadge() {
  const badge = document.getElementById('drill-badge');
  if (!badge) return;
  const due = getDueCount();
  if (due > 0) {
    badge.textContent = String(due);
    badge.hidden = false;
  } else {
    badge.hidden = true;
  }
}

function renderSkeleton(container, name) {
  // Skeleton placeholder shapes matching the destination route.
  // Replaces the legacy "Loading..." text per Brief 2 §3.1.
  // Each shape kind maps to a specific HTML block that approximates the
  // dimensions of the rendered content, so the layout doesn't shift when
  // the real content swaps in.
  const shapes = {
    home:       ['title', 'tagline', 'cta', 'pillars'],
    learn:      ['title', 'rows', 'rows', 'rows'],
    test:       ['title', 'card', 'card'],
    drill:      ['title', 'card'],
    review:     ['title', 'card'],
    summary:    ['title', 'rows', 'rows'],
    diagnostic: ['title', 'card', 'rows'],
    settings:   ['title', 'rows', 'rows'],
    reading:    ['title', 'rows', 'rows'],
    listening:  ['title', 'rows'],
    kanji:      ['title', 'grid'],
  };
  const blocks = (shapes[name] || ['title', 'card', 'rows']).map(kind => {
    if (kind === 'title')   return '<div class="skeleton skeleton-title" aria-hidden="true"></div>';
    if (kind === 'tagline') return '<div class="skeleton skeleton-tagline" aria-hidden="true"></div>';
    if (kind === 'cta')     return '<div class="skeleton-ctas" aria-hidden="true"><div class="skeleton skeleton-btn"></div><div class="skeleton skeleton-btn"></div></div>';
    if (kind === 'pillars') return '<div class="skeleton-pillars" aria-hidden="true"><div class="skeleton skeleton-pillar"></div><div class="skeleton skeleton-pillar"></div></div>';
    if (kind === 'grid')    return '<div class="skeleton-grid" aria-hidden="true">' + '<div class="skeleton skeleton-grid-cell"></div>'.repeat(18) + '</div>';
    if (kind === 'card')    return '<div class="skeleton skeleton-card" aria-hidden="true"></div>';
    return '<div class="skeleton skeleton-row" aria-hidden="true"></div>'.repeat(3);
  }).join('');
  container.innerHTML = `<div class="skeleton-wrap" role="status" aria-live="polite" aria-label="Loading">${blocks}</div>`;
}

function renderTimeout(container, name) {
  container.innerHTML = `
    <div class="placeholder">
      <h2>Couldn't load this view</h2>
      <p>The <strong>${name}</strong> tab is taking longer than expected.</p>
      <p class="muted small">If you're offline, the cached version may still appear in a moment. Otherwise the data file may be missing or unreachable.</p>
      <button class="btn-primary" onclick="window.location.reload()">Retry</button>
    </div>
  `;
}

// 2026-05-05 (locale-chip fix): the primary-nav links in index.html ship
// with hardcoded English labels. After a locale switch, they need to
// be re-translated. Called at the start of every route() so the labels
// always match the active locale. Resolves the user-reported bug where
// clicking a locale chip didn't visibly change anything.
// IMP-069 (audit round-6): generic data-i18n-key attribute walker.
// Any element with `data-i18n-key="..."` gets its textContent set to
// `t(key)` on route change. Primary use: footer "Help translate" link
// + future static labels in index.html. Avoids per-element wiring.
function applyDataI18nKeys() {
  document.querySelectorAll('[data-i18n-key]').forEach(el => {
    const key = el.dataset.i18nKey;
    const translated = t(key);
    if (translated && translated !== key) el.textContent = translated;
  });
}

function applyNavTranslations() {
  const NAV_KEYS = {
    'learn/grammar': 'nav.learn',     // → "Grammar" / "Học" / etc. - locale "Learn" is closest
    'learn/vocab':   'nav.learn',     // → "Vocabulary" - share Learn-bucket label here too
    'kanji':         'nav.kanji',
    'reading':       'nav.reading',
    'listening':     'nav.listening',
    'test':          'nav.test',
    'sitting':       'nav.mock',
    'missed':        'nav.missed',
    'summary':       'nav.progress',
  };
  // Per-route override: Grammar + Vocabulary deserve their own locale keys
  // (currently nav.learn collides). Use ad-hoc strings sourced from
  // home/learn-hub keys when available; fall back to the existing label.
  // Phase 3 of locale transition (2026-05-06): narrowed from 5 locales
  // (en/vi/id/ne/zh) to 2 (en/hi). Existing-user safety: any visitor
  // whose persisted locale is one of the four removed locales gets
  // migrated to en by migrateLocaleSetting() before render.
  const PER_ROUTE = {
    'learn/grammar': { en: 'Grammar', hi: 'व्याकरण' },
    'learn/vocab':   { en: 'Vocabulary', hi: 'शब्दावली' },
    'kanji':         { en: 'Kanji', hi: 'कान्जी' },
    'reading':       { en: 'Reading', hi: 'पठन' },
    'listening':     { en: 'Listening', hi: 'श्रवण' },
    'test':          { en: 'Test', hi: 'परीक्षा' },
    'sitting':       { en: 'Mock', hi: 'मॉक' },
    'missed':        { en: 'Missed', hi: 'छूटे प्रश्न' },
    'summary':       { en: 'Progress', hi: 'प्रगति' },
  };
  const lc = currentLocale();
  document.querySelectorAll('.primary-nav a[data-route]').forEach(a => {
    const route = a.dataset.route;
    const map = PER_ROUTE[route];
    if (map && map[lc]) a.textContent = map[lc];
  });
}

// IMP-WAVE-P4-29 (UI audit fix, 2026-05-12): per-route SEO meta
// updater. SPAs ship a single index.html; server-side meta tags
// can't change per route. Client-side updates still help screen
// readers, dynamic-rendering crawlers (Googlebot since 2019 runs
// JS), and browser tab titles / share previews.
//
// Maps each route to a (title, description) tuple. The hash-deep
// param (e.g., #/learn/n5-001) gets appended to title when present
// for deep-link previews. Falls back to the static meta when no
// route-specific tuple exists.
const ROUTE_META = {
  home:       { title: 'JLPT N5 study material — free, offline, English + Hindi',
                desc:  'Grammar / vocab / kanji / reading / listening. No login. No tracking. Works offline.' },
  learn:      { title: 'Learn JLPT N5 — grammar + vocabulary',
                desc:  '178 N5 grammar patterns and 1009 vocab entries, with native examples and provenance.' },
  test:       { title: 'JLPT N5 test mode',
                desc:  'Timed multiple-choice tests over the N5 corpus. Per-question rationale, per-pattern history.' },
  drill:      { title: 'JLPT N5 spaced-repetition drill',
                desc:  'SRS-graded review of patterns and vocab you have studied. SM-2 / FSRS scheduling.' },
  review:     { title: 'JLPT N5 review queue',
                desc:  'Items due for review today. Anki-style grading.' },
  summary:    { title: 'JLPT N5 progress dashboard',
                desc:  'Mastered patterns, weak areas, error patterns, study streak.' },
  diagnostic: { title: 'JLPT N5 placement diagnostic',
                desc:  '15-question placement test to establish where to start.' },
  settings:   { title: 'JLPT N5 settings',
                desc:  'Locale, theme, font size, audio rate, daily caps, data export.' },
  reading:    { title: 'JLPT N5 reading practice',
                desc:  '54 reading passages with grammar footnotes, vocabulary preview, time targets.' },
  listening:  { title: 'JLPT N5 listening practice',
                desc:  '50 chokai items with VOICEVOX audio, transcripts, distractor-pattern hints.' },
  kanji:      { title: 'JLPT N5 kanji — 106 characters',
                desc:  '106 N5 kanji with stroke-order SVGs, mnemonics, etymology, real-world cards.' },
  sitting:    { title: 'JLPT N5 mock paper sitting',
                desc:  'Full timed mock exam with section breaks, per-mondai pacing, scaled-score estimate.' },
  papers:     { title: 'JLPT N5 papers',
                desc:  '29 papers across moji, goi, bunpou, dokkai, listening, plus full-mock sets.' },
  missed:     { title: 'JLPT N5 wrong-answer history',
                desc:  'Every question you got wrong, ordered for review.' },
  print:      { title: 'Print JLPT N5 paper to PDF',
                desc:  'Save any mock paper as a printable PDF for paper-and-pencil practice.' },
  authentic:  { title: 'Authentic Japanese — real-world signs, menus, transit',
                desc:  '100 cards of actual JP signage, menu prices, station notices, weather forecasts.' },
  strategy:   { title: 'JLPT N5 test-taking strategy',
                desc:  'Section timing, trap patterns, 15 techniques, score breakdown, diagnostic drills.' },
  weakareas:  { title: 'JLPT N5 weak-area diagnostic',
                desc:  'Cross-references your history against 9 diagnostic areas; surfaces drill recommendations.' },
  examday:    { title: 'JLPT N5 exam-day prep checklist',
                desc:  '5-min summary, day-of checklist, 14-day drill schedule. Printable.' },
  changelog:  { title: 'JLPT N5 changelog',
                desc:  'Version history of the JLPTSuccess N5 release stream.' },
  privacy:    { title: 'JLPT N5 privacy policy',
                desc:  'No login. No telemetry. No third-party scripts. Everything stays in your browser.' },
  notices:    { title: 'JLPT N5 legal notices + licenses',
                desc:  'MIT (code) + CC BY-SA 4.0 (content). Third-party attribution.' },
  feedback:   { title: 'JLPT N5 feedback',
                desc:  'How to report a content error, suggest improvements, or request a feature.' },
};

function applyRouteMeta(name, params) {
  const meta = ROUTE_META[name];
  if (!meta) return;
  let title = meta.title;
  if (params && typeof params === 'string' && params.length) {
    title += ` — ${params.split('/')[0]}`;
  }
  document.title = title;
  // Update or create per-route meta description
  let desc = document.querySelector('meta[name="description"]');
  if (desc) desc.setAttribute('content', meta.desc);
  // Mirror to OG
  for (const sel of ['meta[property="og:title"]', 'meta[name="twitter:title"]']) {
    const m = document.querySelector(sel);
    if (m) m.setAttribute('content', title);
  }
  for (const sel of ['meta[property="og:description"]', 'meta[name="twitter:description"]']) {
    const m = document.querySelector(sel);
    if (m) m.setAttribute('content', meta.desc);
  }
  // og:url - the canonical pathname URL (history mode, no hash). Each
  // pattern has its own server-resolvable URL, so social-card previews
  // and crawlers can fetch the page directly. Normalised: strip
  // /index.html from the tail so /learn/n5-001/index.html and
  // /learn/n5-001/ produce the same canonical URL.
  const ogUrl = document.querySelector('meta[property="og:url"]');
  if (ogUrl) {
    const canonical = location.origin + location.pathname.replace(/\/index\.html$/, '/');
    ogUrl.setAttribute('content', canonical);
  }
}

async function route() {
  const container = document.getElementById('app');
  const { name, params } = parseRoute();
  // Unknown-route fallback: parseRoute() now redirects unknown names to
  // 'home' via replaceState (KNOWN_ROUTES guard in router.js, BUG-202).
  // But keep a defensive fallback here too in case ROUTES drifts out of
  // sync with KNOWN_ROUTES — fall back to renderHome (NOT renderLearn,
  // which previously hung on unresolvable sub-params like
  // /#/learn/grammar → renderLearn('grammar')).
  const handler = ROUTES[name] || ROUTES.home;
  setActiveNav(handler === renderLearn ? 'learn' : name);
  applyNavTranslations();
  applyDataI18nKeys();
  applyRouteMeta(name, params);
  renderSkeleton(container, name);
  let timedOut = false;
  const timeoutId = setTimeout(() => {
    timedOut = true;
    renderTimeout(container, name);
  }, 5000);
  try {
    await handler(container, params);
  } catch (err) {
    console.error('Route handler failed:', err);
    if (!timedOut) {
      container.innerHTML = `<div class="placeholder"><h2>Error</h2><p>${err.message}</p><button class="btn-primary" onclick="window.location.reload()">Reload</button></div>`;
    }
  } finally {
    clearTimeout(timeoutId);
  }
  // Scroll to the top on every route change (user request 2026-06-08): when a
  // kanji card (or any list item) is opened, the detail page must start at its
  // header — the big glyph — not retain the previous page's scroll position
  // mid-page. Hash routing carries no in-page anchors, so this is always safe.
  window.scrollTo(0, 0);
  refreshDrillBadge();
}

// Brief 2 §7.3: prompt before discarding in-progress Test state.
function shouldPromptOnLeave() {
  // The test module sets a window-global flag when it enters/exits
  // attempting; we can't peek into its state cleanly from here.
  return !!window.__testInProgress;
}

window.addEventListener('beforeunload', (ev) => {
  if (shouldPromptOnLeave()) {
    ev.preventDefault();
    ev.returnValue = '';
    return '';
  }
});

// Track the last "confirmed" pathname so we can revert browser
// back/forward navigation when an in-progress test is interrupted.
let lastConfirmedPath = location.pathname;
window.addEventListener('popstate', (ev) => {
  if (shouldPromptOnLeave()) {
    const ok = confirm('Quit this test? Progress so far will be saved to history.');
    if (!ok) {
      // Revert without re-firing the handler
      history.replaceState(null, '', lastConfirmedPath || getBasePath());
      return;
    }
    window.__testInProgress = false;
  }
  lastConfirmedPath = location.pathname;
  route();
});

// Global click interception for internal navigation. Any <a> with a
// data-route attribute (e.g. primary-nav links, footer links, in-page
// CTAs) is routed via navigateTo() instead of triggering a full
// page navigation. Works correctly whether the user is on index.html
// or on a static-mirror deep-link, because navigateTo() builds the
// absolute URL from getBasePath().
//
// Also catches anchor tags whose href still uses the legacy `#/...`
// form (until every HTML href is migrated in Phase 3 + every static
// mirror is regenerated). Modifier-clicks (Ctrl/Cmd/Shift/Alt and
// middle-button) are NOT intercepted - the user wants those to open
// in a new tab / window, which requires the real href.
document.addEventListener('click', (ev) => {
  if (ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
  const a = ev.target.closest('a');
  if (!a) return;
  const dataRoute = a.getAttribute('data-route');
  const href = a.getAttribute('href') || '';
  let route = null;
  if (dataRoute) {
    route = dataRoute;
  } else if (href.startsWith('#/')) {
    route = href.slice(2);
  }
  if (route == null) return;
  ev.preventDefault();
  navigateTo(route);
});

// Backward-compat: any legacy `#/...` link click or bookmark still
// triggers a route. parseRoute() inside route() will replaceState the
// URL to the clean path form. Skip-link a11y: ignore non-route hashes
// (e.g. #app for "Skip to main content") - the browser still does the
// anchor scroll / focus, just no route change.
window.addEventListener('hashchange', (ev) => {
  const hash = location.hash;
  if (hash && !hash.startsWith('#/')) return;
  if (shouldPromptOnLeave()) {
    const ok = confirm('Quit this test? Progress so far will be saved to history.');
    if (!ok) {
      history.replaceState(null, '', lastConfirmedPath || getBasePath());
      return;
    }
    window.__testInProgress = false;
  }
  // parseRoute() will rewrite the hash to a clean path; trigger route().
  route().then(() => { lastConfirmedPath = location.pathname; });
});
window.addEventListener('DOMContentLoaded', async () => {
  initStorage();
  applyTheme();
  applyFontSize();
  applyReduceMotion();
  initContentProtection();   // <-- copy / right-click / screenshot deterrents
  await initI18n();
  await initFuriganaToggle(route);
  initKanjiPopover();
  initShortcuts();
  initSearch();
  initPwa();
  initFullscreenToggle();
  initLocaleChips();
  // SVA-NEXT-3: superseded initThemeOverrides() — now reads data/branding.json
  // (a unified file covering CSS tokens + brand strings + meta tags + footer
  // attribution + watermark text). Falls back to data/theme-overrides.json
  // for legacy forks. Awaited so overrides apply BEFORE first route render.
  await loadBranding();
  // ISSUE-001: keep the footer version-stamp in sync with CHANGELOG.md so a
  // forgotten manual bump never re-introduces the v1.10.2 → v1.12.27 drift.
  // Cheap because CHANGELOG.md is precached by the SW; if the fetch fails
  // (e.g., rare offline first-paint race) the static fallback in index.html
  // remains visible.
  fetch('CHANGELOG.md').then(r => r.ok ? r.text() : '').then(text => {
    const m = text.match(/^## (v\d+\.\d+\.\d+)/m);
    const el = document.querySelector('[data-footer-version]');
    if (m && el) el.textContent = m[1];
  }).catch(() => {});
  // Record study activity for streak (Brief 2 §6.1) on any meaningful interaction
  ['click', 'keydown'].forEach(evt => {
    document.addEventListener(evt, () => recordStudyToday(), { once: true });
  });
  // IMP-044 (audit round-3): first-run onboarding. Fresh installs
  // (no prior history, no test results, no streak) get routed to the
  // diagnostic at first touch. Returning users land on home. Once
  // seen, the onboardingSeen sentinel keeps subsequent landings on
  // home; diagnostic stays reachable from /diagnostic/.
  //
  // History-mode rewrite (2026-05-24): the "is the user at the root
  // URL?" check used to test `!location.hash`; now we test whether
  // parseRoute() returns the default home route AND no legacy hash
  // is present.
  {
    const basePath = getBasePath().replace(/\/$/, '');
    const currentPath = location.pathname.replace(/\/index\.html$/, '').replace(/\/$/, '');
    const atRoot = currentPath === basePath;
    const hasLegacyHash = location.hash && location.hash.startsWith('#/');
    if (atRoot && !hasLegacyHash) {
      try {
        const noHistory = Object.keys(getHistory()).length === 0;
        const noResults = (getResults() || []).length === 0;
        const noStreak  = !getStreak()?.lastStudyDate;
        const isFirstRun = noHistory && noResults && noStreak;
        const seenOnboard = localStorage.getItem('jlpt-n5-tutor:onboardingSeen');
        if (isFirstRun && !seenOnboard) {
          localStorage.setItem('jlpt-n5-tutor:onboardingSeen', '1');
          history.replaceState(null, '', urlForRoute('diagnostic'));
        }
        // else: stay at base — home is the default route from parseRoute().
      } catch { /* noop */ }
    }
  }
  // IMP-063 (audit round-5): handle PWA share_target. When the OS Share
  // sheet sends a Japanese phrase to JLPTSuccess, the manifest routes
  // it to /N5/?q=<text>. Pull the q out of the query string, focus the
  // search input, prefill it, and fire the input event so the search
  // panel opens with results.
  try {
    const qs = new URLSearchParams(location.search);
    const sharedQ = qs.get('q') || qs.get('text') || qs.get('title');
    if (sharedQ) {
      // Strip the query string from the URL so a refresh doesn't re-trigger.
      // Also normalise to the home route in pathname mode.
      history.replaceState(null, '', getBasePath());
      // Defer focus until the home route renders.
      queueMicrotask(() => {
        const input = document.getElementById('search-input');
        if (input) {
          input.value = sharedQ;
          input.focus();
          input.dispatchEvent(new Event('input', { bubbles: true }));
        }
      });
    }
  } catch { /* noop */ }
  await route();
  applyAudioRate();
});

// Re-render the active route when furigana mode changes (Brief 2 §4.1, §4.2)
// without losing scroll - listens for the custom event from Settings + popover.
document.addEventListener('furigana-rerender', () => { route(); });
// Apply audio rate + custom skin to every new <audio> on route change.
// IMP-007/IMP-010/IMP-038 (audit round-3): the bare <audio controls> is
// replaced by a skinned wrapper with skip-back-5s, skip-forward-5s,
// and per-clip 0.75/1.0/1.25× rate buttons. enhanceAudioPlayers is
// idempotent - already-enhanced nodes are no-ops.
//
// 2026-05-08 BUG FIX: applyAudioRate() was being called inside the
// MutationObserver, which fired on every textContent update (including
// the audio player's own time-display updates from `timeupdate` /
// `loadedmetadata` / `ratechange`). That created a feedback loop:
//   1. user clicks 1.25× → audio.playbackRate = 1.25
//   2. ratechange event → updateTime() → timeEl.textContent = "..."
//   3. MutationObserver sees textContent change → applyAudioRate()
//      resets every <audio>'s playbackRate to the global Settings
//      value (1.0 by default) → per-clip override is clobbered.
// The per-clip rate buttons appeared to do nothing (highlight changed,
// playback rate didn't). Fix: drop applyAudioRate() from the
// MutationObserver. The initial rate is already applied per-clip in
// enhanceOne() (audio-player.js line 51-56) by reading the Settings
// at the time the <audio> is wrapped — so the global Settings rate
// still works as the *default*, but per-clip overrides stick.
document.addEventListener('DOMContentLoaded', () => {
  import('./audio-player.js').then(({ enhanceAudioPlayers }) => {
    const root = document.getElementById('app') || document.body;
    const obs = new MutationObserver(() => {
      enhanceAudioPlayers(root);
    });
    obs.observe(root, { childList: true, subtree: true });
    enhanceAudioPlayers(root);
  });
});

// Fullscreen toggle (top-right header). Clicking the button toggles between
// document fullscreen and windowed mode. We swap the SVG icon between the
// "maximize" (4 corners) and "minimize" (inward arrows) shapes via CSS state.
// The browser's own Esc key exits fullscreen too - we listen for the
// fullscreenchange event so the button label reflects current state.
// IMP-052 (audit round-4) → SVA-NEXT-3 (round-9 follow-up, 2026-05-08):
// the inline initThemeOverrides() function lived here for ~3 rounds and
// only handled CSS tokens + brand.name. Superseded by js/branding.js,
// which is a strict superset (tokens + brand strings + meta tags +
// footer attribution + watermark text + per-locale trust strip), and
// which reads BOTH `data/branding.json` (current) AND
// `data/theme-overrides.json` (legacy fallback) so existing forks keep
// working without migration. See docs/SELF-HOST.md § Branding override
// layer for the unified schema.

// Header locale toggle: single icon-btn-shaped button that swaps between
// EN and HI on click. The visible text reflects the CURRENT locale; the
// aria-label tells the user what'll happen on click ("Switch to Hindi" /
// "Switch to English"). Replaces the earlier 2-chip pill group per design
// family alignment 2026-05-09.
function initLocaleChips() {
  const btn = document.getElementById('locale-toggle');
  if (!btn) return;
  // Phase-1 launch (2026-05-24): when only one locale is UI-enabled,
  // hide the toggle entirely (and do not register click listeners).
  // The button stays in the DOM so Phase 2 reactivation is a one-line
  // change in js/i18n.js (widen ENABLED_LOCALES) — no HTML edit needed.
  // Note: the `hidden` HTML attribute is overridden by `.icon-btn`'s
  // `display: flex` CSS rule, so we also force `display: none` inline
  // to make the hide actually take effect visually.
  if (!enabledLocales || enabledLocales.length <= 1) {
    btn.hidden = true;
    btn.setAttribute('aria-hidden', 'true');
    btn.style.display = 'none';
    // Also hide the footer "Switch language" link — it would otherwise
    // scroll to and pulse the now-invisible toggle, leaving the user
    // confused about why nothing happened.
    const footerSwitch = document.getElementById('footer-switch-lang');
    if (footerSwitch) {
      footerSwitch.hidden = true;
      footerSwitch.style.display = 'none';
    }
    return;
  }
  const label = btn.querySelector('[data-locale-label]');
  // Multi-locale rotation. Cycles through the ENABLED subset (UI-offered),
  // not the SUPPORTED set (data-shipped). Phase 2 widens ENABLED_LOCALES.
  const cycle = enabledLocales.length ? enabledLocales : ['en'];
  const sync = () => {
    const cur = currentLocale();
    // Visible label is the DESTINATION locale (the one click will
    // switch TO), not the current locale. So when the page is in
    // English, the button shows "HI" — i.e. "click here to go to
    // Hindi." This matches the affordance pattern users expect from
    // single-button language switchers.
    const nextIdx = (cycle.indexOf(cur) + 1) % cycle.length;
    const next = cycle[nextIdx];
    if (label) label.textContent = (next || 'en').toUpperCase();
    const nextNice = ({ en: 'English', hi: 'Hindi' })[next] || next.toUpperCase();
    btn.setAttribute('aria-label', 'Switch to ' + nextNice);
    btn.setAttribute('title', 'Switch to ' + nextNice);
    btn.setAttribute('lang', next || 'en');
  };
  btn.addEventListener('click', async () => {
    const cur = currentLocale();
    const nextIdx = (cycle.indexOf(cur) + 1) % cycle.length;
    const next = cycle[nextIdx];
    if (!supportedLocales.includes(next)) return;
    await setLocale(next);
    sync();
    route();   // re-render the active route in the new locale
  });
  sync();
  // Sync on locale-change event from Settings panel.
  document.addEventListener('locale-changed', sync);

  // Footer "Switch language" link still works — scroll the toggle into
  // view and pulse it so the user finds the picker.
  const switchLink = document.getElementById('footer-switch-lang');
  if (switchLink) {
    switchLink.addEventListener('click', (e) => {
      e.preventDefault();
      btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
      btn.classList.add('locale-toggle-pulse');
      setTimeout(() => btn.classList.remove('locale-toggle-pulse'), 1200);
      btn.focus({ preventScroll: true });
    });
  }
}

function initFullscreenToggle() {
  const btn = document.getElementById('fullscreen-toggle');
  if (!btn) return;
  const targetEl = () => document.documentElement;
  const isFullscreen = () => !!(document.fullscreenElement || document.webkitFullscreenElement);
  const updateLabel = () => {
    const fs = isFullscreen();
    btn.setAttribute('aria-label', fs ? 'Exit fullscreen' : 'Toggle fullscreen');
    btn.setAttribute('title', fs ? 'Exit fullscreen' : 'Toggle fullscreen');
    btn.classList.toggle('is-fullscreen', fs);
  };
  btn.addEventListener('click', async () => {
    try {
      if (isFullscreen()) {
        if (document.exitFullscreen) await document.exitFullscreen();
        else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
      } else {
        const el = targetEl();
        if (el.requestFullscreen) await el.requestFullscreen();
        else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
      }
    } catch (err) {
      // Permissions-Policy or user gesture issues - fail silently; the button
      // is opportunistic and shouldn't block the rest of the UI.
      console.warn('Fullscreen toggle failed:', err);
    }
  });
  document.addEventListener('fullscreenchange', updateLabel);
  document.addEventListener('webkitfullscreenchange', updateLabel);
  updateLabel();
}
