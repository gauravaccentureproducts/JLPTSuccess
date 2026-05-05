// Router + chapter coordinator.
import { initStorage, getDueCount, recordStudyToday, getHistory, getResults, getStreak } from './storage.js';
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
import { initI18n, setLocale, currentLocale, supportedLocales, t } from './i18n.js';
import { renderPapers } from './papers.js';
import { renderChangelog } from './changelog.js';
import { renderFeedback } from './feedback.js';
import { renderLevels, renderLevelPlaceholder } from './levels.js';
import { initContentProtection } from './content-protect.js';
import { renderMissed } from './missed.js';
import { renderSitting } from './sitting.js';

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
  missed:     renderMissed,    // IMP-008/031: wrong-answer history
  sitting:    renderSitting,   // ISSUE-020/IMP-032: full mock-paper sitting
  // Level-1 hierarchy: picker + 4 placeholder pages for N4-N1.
  // The actual N5 content stays at all the routes above (home, learn,
  // test, etc.) — clicking N5 on the picker navigates to #/home.
  levels:     renderLevels,
  n4:         renderLevelPlaceholder,
  n3:         renderLevelPlaceholder,
  n2:         renderLevelPlaceholder,
  n1:         renderLevelPlaceholder,
};

function parseRoute() {
  // Default landing is the N5 syllabus dashboard.
  // The level picker now lives at the parent path (../) — handled by
  // JLPTSuccess/index.html, NOT by this app. Any bookmark to #/levels
  // bounces out via the location.replace below.
  const hash = location.hash;
  if (hash === '#/levels' || hash === '#/n5' || hash === '#/n4'
      || hash === '#/n3' || hash === '#/n2' || hash === '#/n1') {
    location.replace('../');
    return { name: 'home', params: '' };
  }
  const safe = hash || '#/home';
  const m = safe.match(/^#\/(\w+)(?:\/(.*))?$/);
  if (!m) return { name: 'home', params: '' };
  return { name: m[1], params: m[2] || '' };
}

function setActiveNav(name) {
  document.querySelectorAll('.primary-nav a').forEach(a => {
    const isActive = a.dataset.route === name;
    a.classList.toggle('active', isActive);
    // IMP-012 (audit round-3): a11y — expose the active nav link to
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
function applyNavTranslations() {
  const NAV_KEYS = {
    'learn/grammar': 'nav.learn',     // → "Grammar" / "Học" / etc. — locale "Learn" is closest
    'learn/vocab':   'nav.learn',     // → "Vocabulary" — share Learn-bucket label here too
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
  const PER_ROUTE = {
    'learn/grammar': { en: 'Grammar', vi: 'Ngữ pháp', id: 'Tata bahasa', ne: 'व्याकरण', zh: '语法' },
    'learn/vocab':   { en: 'Vocabulary', vi: 'Từ vựng', id: 'Kosakata',  ne: 'शब्दावली', zh: '词汇' },
    'kanji':         { en: 'Kanji', vi: 'Kanji', id: 'Kanji', ne: 'कान्जी', zh: '汉字' },
    'reading':       { en: 'Reading', vi: 'Đọc', id: 'Membaca', ne: 'पढाइ', zh: '阅读' },
    'listening':     { en: 'Listening', vi: 'Nghe', id: 'Mendengar', ne: 'सुनाइ', zh: '听力' },
    'test':          { en: 'Test', vi: 'Kiểm tra', id: 'Tes', ne: 'परीक्षण', zh: '测试' },
    'sitting':       { en: 'Mock', vi: 'Thi thử', id: 'Simulasi', ne: 'मॉक', zh: '模拟' },
    'missed':        { en: 'Missed', vi: 'Câu sai', id: 'Salah', ne: 'गल्ती', zh: '错题' },
    'summary':       { en: 'Progress', vi: 'Tiến độ', id: 'Progres', ne: 'प्रगति', zh: '进度' },
  };
  const lc = currentLocale();
  document.querySelectorAll('.primary-nav a[data-route]').forEach(a => {
    const route = a.dataset.route;
    const map = PER_ROUTE[route];
    if (map && map[lc]) a.textContent = map[lc];
  });
}

async function route() {
  const container = document.getElementById('app');
  const { name, params } = parseRoute();
  const handler = ROUTES[name] || renderLearn;
  setActiveNav(handler === renderLearn ? 'learn' : name);
  applyNavTranslations();
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
  refreshDrillBadge();
}

// Brief 2 §7.3: prompt before discarding in-progress Test state.
function shouldPromptOnLeave() {
  const hash = location.hash || '';
  // The test module sets view='attempting' on its own state. We can't peek
  // into it cleanly here, but we can detect via a global flag the module
  // sets when it enters/exits attempting.
  return !!window.__testInProgress;
}

window.addEventListener('beforeunload', (ev) => {
  if (shouldPromptOnLeave()) {
    ev.preventDefault();
    ev.returnValue = '';
    return '';
  }
});

let lastConfirmedHash = location.hash;
window.addEventListener('hashchange', (ev) => {
  // Skip-link a11y: clicking "Skip to main content" sets the hash to
  // #app (or any non-route fragment). parseRoute only recognises
  // hashes that start with `#/`, so without this guard, every
  // skip-link click silently re-routes the user back to #/home,
  // losing their place. Detect non-route hashes and short-circuit —
  // the browser still scrolls to / focuses the target anchor (which
  // now has tabindex="-1" on <main id="app"> for programmatic focus).
  // Closes #14 from the developer-issue-list audit.
  const hash = location.hash;
  if (hash && !hash.startsWith('#/')) {
    return;
  }
  if (shouldPromptOnLeave()) {
    const ok = confirm('Quit this test? Progress so far will be saved to history.');
    if (!ok) {
      // Revert hash without re-firing the handler (silent)
      history.replaceState(null, '', lastConfirmedHash || '#/home');
      return;
    }
    window.__testInProgress = false;
  }
  lastConfirmedHash = location.hash;
  route();
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
  initThemeOverrides();
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
  // IMP-044 (audit round-3): first-run onboarding. Fresh installs (no
  // prior history, no test results, no streak) get routed to the
  // diagnostic at first touch. Returning users keep their normal hash.
  // Once seen, the onboardingSeen sentinel keeps subsequent landings on
  // home — diagnostic stays reachable from #/diagnostic.
  if (!location.hash) {
    try {
      const noHistory = Object.keys(getHistory()).length === 0;
      const noResults = (getResults() || []).length === 0;
      const noStreak  = !getStreak()?.lastStudyDate;
      const isFirstRun = noHistory && noResults && noStreak;
      const seenOnboard = localStorage.getItem('jlpt-n5-tutor:onboardingSeen');
      if (isFirstRun && !seenOnboard) {
        localStorage.setItem('jlpt-n5-tutor:onboardingSeen', '1');
        location.hash = '#/diagnostic';
      } else {
        location.hash = '#/home';
      }
    } catch {
      location.hash = '#/home';
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
      history.replaceState(null, '', location.pathname + location.hash);
      location.hash = '#/home';
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
// idempotent — already-enhanced nodes are no-ops.
document.addEventListener('DOMContentLoaded', () => {
  import('./audio-player.js').then(({ enhanceAudioPlayers }) => {
    const root = document.getElementById('app') || document.body;
    const obs = new MutationObserver(() => {
      applyAudioRate();
      enhanceAudioPlayers(root);
    });
    obs.observe(root, { childList: true, subtree: true });
    enhanceAudioPlayers(root);
  });
});

// Fullscreen toggle (top-right header). Clicking the button toggles between
// document fullscreen and windowed mode. We swap the SVG icon between the
// "maximize" (4 corners) and "minimize" (inward arrows) shapes via CSS state.
// The browser's own Esc key exits fullscreen too — we listen for the
// fullscreenchange event so the button label reflects current state.
// IMP-052 (audit round-4): runtime theme overrides for institutional
// forks. Loads data/theme-overrides.json if present; missing file =
// use the design tokens defined in css/main.css :root. Maps tokens
// onto :root CSS custom properties; brand-name swap updates document
// title + the brand-link aria-label.
async function initThemeOverrides() {
  try {
    const r = await fetch('data/theme-overrides.json');
    if (!r.ok) return;
    const cfg = await r.json();
    if (cfg && typeof cfg === 'object') {
      const root = document.documentElement;
      for (const [k, v] of Object.entries(cfg.tokens || {})) {
        if (typeof k === 'string' && k.startsWith('--')) {
          root.style.setProperty(k, String(v));
        }
      }
      if (cfg.brand && typeof cfg.brand.name === 'string') {
        const brand = document.querySelector('.brand-link');
        if (brand) brand.textContent = cfg.brand.name;
      }
    }
  } catch { /* missing file is the default — silently use repo tokens */ }
}

// ISSUE-028 (audit round-4): wire the header locale-chip group.
// 5 chips swap the i18n locale on click + reload the active route.
// `aria-pressed` reflects the current locale.
function initLocaleChips() {
  const group = document.getElementById('locale-chip-group');
  if (!group) return;
  const sync = () => {
    const cur = currentLocale();
    group.querySelectorAll('.locale-chip').forEach(b => {
      const isActive = b.dataset.lc === cur;
      b.classList.toggle('is-active', isActive);
      b.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
  };
  group.querySelectorAll('.locale-chip').forEach(b => {
    if (!supportedLocales.includes(b.dataset.lc)) {
      b.disabled = true;
      return;
    }
    b.addEventListener('click', async () => {
      await setLocale(b.dataset.lc);
      sync();
      route();   // re-render the active route in the new locale
    });
  });
  sync();
  // Sync on locale-change event from Settings panel.
  document.addEventListener('locale-changed', sync);
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
      // Permissions-Policy or user gesture issues — fail silently; the button
      // is opportunistic and shouldn't block the rest of the UI.
      console.warn('Fullscreen toggle failed:', err);
    }
  });
  document.addEventListener('fullscreenchange', updateLabel);
  document.addEventListener('webkitfullscreenchange', updateLabel);
  updateLabel();
}
