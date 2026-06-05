/*
 * error-monitor.js - IMP-5: production runtime-error capture.
 *
 * WHY THIS EXISTS
 * On the live static site a JavaScript error otherwise vanishes into the
 * visitor's console and the maintainer never sees it. Production-only bugs
 * (specific Safari versions, odd input data, race conditions, network/SW cache
 * misses) are invisible without telemetry. This installs global `error` +
 * `unhandledrejection` handlers and keeps a capped ring buffer of recent errors
 * in localStorage + window.__errorLog so:
 *   (a) errors are inspectable on-device (window.__errorLog), and
 *   (b) the IMP-2 "Report a problem" flow can attach the recent error(s) to a
 *       GitHub issue - closing the production-feedback loop without a backend.
 *
 * CSP / privacy
 * This file is same-origin (script-src 'self'), captures LOCALLY only, and
 * makes NO external request by default - fully compatible with the strict CSP
 * (connect-src 'self') and the site's no-tracking promise. The buffer holds
 * only error text + URL + UA, in the user's own browser.
 *
 * TO ENABLE EXTERNAL REPORTING (Sentry or any collector) - TWO steps required:
 *   1. Paste the collector's ingest URL into DSN below (a client-side Sentry
 *      DSN is non-sensitive / public by design).
 *   2. Add that origin to the CSP connect-src directive in index.html, e.g.
 *      connect-src 'self' https://oXXXXXX.ingest.sentry.io
 * Until BOTH are done the monitor stays in local-capture mode and any send is
 * silently blocked by CSP (the local buffer still holds the error).
 */
(function () {
  "use strict";

  // IMP-5 user step: paste a Sentry (or custom collector) ingest URL here AND
  // add its origin to CSP connect-src in index.html. Empty = local-capture only.
  var DSN = "";

  var MAX = 25;                  // ring-buffer cap
  var KEY = "n5_error_log_v1";

  var log = [];
  try { log = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { log = []; }
  if (!Array.isArray(log)) log = [];
  window.__errorLog = log;

  function persist() {
    try { localStorage.setItem(KEY, JSON.stringify(log.slice(-MAX))); }
    catch (e) { /* quota / private mode: keep in-memory only */ }
  }

  function forward(entry) {
    if (!DSN) return;            // local-capture mode
    try {
      // Minimal dependency-free beacon. Requires connect-src to allow the DSN
      // origin (see header); otherwise the browser blocks it and we stay local.
      if (navigator.sendBeacon) navigator.sendBeacon(DSN, JSON.stringify(entry));
    } catch (e) { /* blocked by CSP or offline: local buffer already holds it */ }
  }

  function record(kind, message, detail) {
    var entry = {
      t: new Date().toISOString(),
      kind: kind,
      message: String(message == null ? "" : message).slice(0, 500),
      url: location.href,
      detail: String(detail == null ? "" : detail).slice(0, 1000),
      ua: navigator.userAgent
    };
    log.push(entry);
    if (log.length > MAX) log.splice(0, log.length - MAX);
    persist();
    if (window.console && console.warn) console.warn("[error-monitor]", kind, entry.message);
    forward(entry);
  }

  window.addEventListener("error", function (e) {
    var where = e && e.filename ? (e.filename + ":" + e.lineno + ":" + e.colno) : "";
    record("error", e && e.message, where);
  });
  window.addEventListener("unhandledrejection", function (e) {
    var r = e && e.reason;
    record("unhandledrejection", r && r.message ? r.message : r, r && r.stack ? r.stack : "");
  });

  // Helper the IMP-2 Report-a-problem flow uses to attach recent errors.
  window.__recentErrors = function (n) { return log.slice(-(n || 3)); };
})();
