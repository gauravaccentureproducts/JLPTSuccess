// History-mode router helpers, shared across every JS module that
// needs to navigate within the SPA.
//
// Side effect on import: monkey-patches window.fetch so any
// document-relative URL (e.g. `fetch('data/grammar.json')`) is
// resolved against the SPA root (getBasePath()), not the current
// document URL. This lets the SPA boot from a deep path like
// /learn/n5-001/ (static mirror) AND still fetch its data files
// correctly. Absolute URLs (/foo, https://...) and Request objects
// pass through untouched.
(function installBaseAwareFetch() {
  if (typeof window === 'undefined' || !window.fetch) return;
  if (window.__baseAwareFetchInstalled) return;
  window.__baseAwareFetchInstalled = true;
  const _origFetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    if (typeof input === 'string' &&
        !input.startsWith('/') &&
        !input.startsWith('http://') &&
        !input.startsWith('https://') &&
        !input.startsWith('blob:') &&
        !input.startsWith('data:')) {
      // Document-relative URL - rebase to SPA root
      const pn = location.pathname;
      const m = pn.match(/^(.*\/N5\/)/);
      const base = m ? m[1] : '/';
      input = base + input;
    }
    return _origFetch(input, init);
  };
})();
//
// Migration note (2026-05-24): pre-v1.17 the SPA used hash routing
// (location.hash = '#/learn/n5-001'). We migrated to history mode so
// each pattern has a real path-based URL (/learn/n5-001/) that
// crawlers, LLMs, and link previewers can fetch directly. Legacy
// hash URLs are silently rewritten on boot for backward compatibility.
//
// This module has NO imports from other app modules, so it's safe to
// import from anywhere without creating circular dependencies.

// Base-path detection. Production deploys at /JLPTSuccess/N5/; local
// dev `python -m http.server` runs at /. The N5/ segment is the
// reliable marker.
export function getBasePath() {
  const pn = location.pathname;
  const m = pn.match(/^(.*\/N5\/)/);
  if (m) return m[1];
  // No N5/ in the path - assume root (local dev).
  return '/';
}

// Normalize a route string (e.g. 'learn/n5-001' or '/learn/n5-001/')
// into a clean route part: no leading slash, trailing slash present
// for non-empty routes.
function normalizeRoute(routeStr) {
  let r = (routeStr || '').replace(/^[#/]+/, '');  // strip leading # or /
  r = r.replace(/^\//, '');
  if (r && !r.endsWith('/')) r += '/';
  return r;
}

// Build the absolute pathname for a given route (e.g. 'learn/n5-001').
export function urlForRoute(routeStr) {
  const base = getBasePath();
  const r = normalizeRoute(routeStr);
  return base + r;
}

// Build a base-relative URL for a static asset (audio, image, etc.).
// Use this when injecting URLs into HTML attributes like `<audio src>`
// or `<img src>` - browsers resolve those against document.baseURI
// (which is the current page URL, including deep mirror paths), NOT
// against any wrapped fetch logic. Without this helper, `audio/X.mp3`
// from a page at `/learn/n5-001/` resolves to `/learn/n5-001/audio/X.mp3`
// (404). Pass-through for absolute URLs.
export function assetUrl(path) {
  if (!path) return path;
  if (typeof path !== 'string') return path;
  if (path.startsWith('/') || path.startsWith('http://') ||
      path.startsWith('https://') || path.startsWith('blob:') ||
      path.startsWith('data:')) {
    return path;
  }
  return getBasePath() + path;
}

// Navigate to a route. opts.replace: use replaceState instead of
// pushState (no new history entry). Triggers the SPA route handler
// by dispatching a popstate event, which app.js listens for.
export function navigateTo(routeStr, opts) {
  const target = urlForRoute(routeStr);
  if (target === location.pathname) return;
  if (opts && opts.replace) {
    history.replaceState(null, '', target);
  } else {
    history.pushState(null, '', target);
  }
  window.dispatchEvent(new PopStateEvent('popstate'));
}

// Known route names, kept in sync with ROUTES map in js/app.js.
// parseRoute() validates parsed name against this set; unknown
// routes redirect to N5 home (silently, via replaceState) rather
// than rendering an in-app "unknown" state that hangs.
//
// Added 2026-05-26 (BUG-202 user-reported: hash URL
// /N5/#/learn/grammar left the page stuck on skeleton loaders
// because route dispatch fell through to a handler that couldn't
// resolve the sub-params. User rule: any wrong URL → that N
// level's home page; no 404s, no hangs).
export const KNOWN_ROUTES = new Set([
  'home', 'learn', 'test', 'drill', 'review', 'summary', 'diagnostic',
  'settings', 'kosoado', 'waga', 'verbclass', 'teform', 'particles',
  'counters', 'reading', 'listening', 'kanji', 'papers', 'changelog',
  'feedback', 'privacy', 'notices', 'missed', 'sitting', 'print',
  'authentic', 'strategy', 'weakareas', 'examday', 'listeningstory',
  'mining', 'levels',
]);

// Parse the current location.pathname into a route { name, params }.
// Backward-compat: if a legacy #/... URL is present, rewrite it to
// the clean path form via replaceState before parsing.
// Unknown-route guard: if the parsed name isn't in KNOWN_ROUTES,
// redirect to N5 home (BUG-202 fix, 2026-05-26).
export function parseRoute() {
  // Legacy hash URL - convert to clean path
  const hash = location.hash;
  if (hash && hash.startsWith('#/')) {
    const cleanRoute = hash.slice(2);  // strip "#/"
    const target = urlForRoute(cleanRoute);
    history.replaceState(null, '', target);
    // Fall through and parse the new pathname
  }

  const base = getBasePath();
  let route = location.pathname;
  if (route.startsWith(base)) route = route.slice(base.length);
  // Tidy the route string
  route = route.replace(/^\/+/, '').replace(/\/+$/, '').replace(/\/?index\.html$/, '');

  if (!route) return { name: 'home', params: '' };

  // Level picker redirects (legacy parent-level URLs that should bounce
  // out to the level-picker index.html at parent path)
  if (['levels', 'n5', 'n4', 'n3', 'n2', 'n1'].includes(route)) {
    location.replace('../');
    return { name: 'home', params: '' };
  }

  // Match `name/params` where name is a single word (\w+) and params
  // is the remainder (which may contain slashes, e.g. listening/item-id
  // or sitting/1/result).
  const m = route.match(/^(\w[\w-]*)(?:\/(.*))?$/);
  if (!m) {
    // Malformed route → redirect to home (no in-app stuck-loader state)
    history.replaceState(null, '', base);
    return { name: 'home', params: '' };
  }

  const name = m[1];
  // Unknown-route guard: if name isn't a registered route, silently
  // redirect to N5 home. Catches typos in deep links, dead links
  // from old indexes, hash-stripped routes that don't resolve, etc.
  if (!KNOWN_ROUTES.has(name)) {
    if (typeof console !== 'undefined' && console.warn) {
      console.warn(`[router] unknown route "${name}" → redirecting to N5 home`);
    }
    history.replaceState(null, '', base);
    return { name: 'home', params: '' };
  }
  return { name, params: m[2] || '' };
}
