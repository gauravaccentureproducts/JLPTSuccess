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

// Parse the current location.pathname into a route { name, params }.
// Backward-compat: if a legacy #/... URL is present, rewrite it to
// the clean path form via replaceState before parsing.
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
  if (!m) return { name: 'home', params: '' };
  return { name: m[1], params: m[2] || '' };
}
