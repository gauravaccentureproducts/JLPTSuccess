// Minimal i18n layer per Brief §3.5.
// Lookup-based; default locale = en. Locales live in /locales/<lang>.json.
// At v1 only en ships; structure ready for vi/id/ne/zh.
//
// Usage:
//   import { t, setLocale, currentLocale } from './i18n.js';
//   t('app.title')       → 'JLPT N5 Grammar Tutor'
//   t('drill.start')     → 'Start drill'
//   t('greeting', {name}) → 'Hello, ${name}'
//
// Falls back to the key itself if missing - never throws.

import * as storage from './storage.js';

// Phase 3 of locale transition (2026-05-06): the 5-locale shell
// (en/vi/id/ne/zh) is narrowed to the 2-locale shell (en/hi). Strategic
// rationale: Hindi is the unique high-demand-low-competition gap (top-5
// JLPT country, ~50K applicants/year, no dedicated Hindi-medium prep
// app); the other four sit in saturated competitive markets where the
// 5-locale shell was diluting depth. Persisted vi/id/ne/zh preferences
// are migrated to en by migrateLocaleSetting() below.
const SUPPORTED = ['en', 'hi'];
const DEFAULT_LOCALE = 'en';

// Phase 2 of locale transition (2026-05-06): locales being removed in
// Phase 3. Persisted preferences in this set get migrated to 'en' on
// first load post-transition. Existing-user safety contract - no error,
// no white screen, no re-prompt.
const DEPRECATED_LOCALES = ['vi', 'id', 'ne', 'zh'];

let _migrationRunThisSession = false;

/**
 * Migrate persisted-locale settings for users who picked vi/id/ne/zh
 * before the en+hi narrowing. Runs at most once per session. Idempotent
 * for users already on en or hi.
 *
 * - vi/id/ne/zh -> en, persisted, console.info exactly once.
 * - any value not in {en, hi, ...DEPRECATED_LOCALES} -> en, persisted.
 * - en or hi -> no-op.
 *
 * Must run BEFORE setLocale() / loadDict() in the bootstrap. Safe to
 * call multiple times (the _migrationRunThisSession guard limits the
 * console output but the migration itself is naturally idempotent).
 */
export function migrateLocaleSetting() {
  let settings;
  try {
    settings = storage.getSettings();
  } catch {
    return; // storage layer broken; nothing to migrate from
  }
  const cur = settings && settings.uiLocale;
  if (cur === 'en' || cur === 'hi') return;
  const wasDeprecated = DEPRECATED_LOCALES.includes(cur);
  const wasJunk = cur != null && !wasDeprecated;
  if (!wasDeprecated && !wasJunk && cur != null) return;
  // Persist 'en' so the next load does not need to re-migrate.
  try {
    storage.setSettings({ uiLocale: 'en' });
  } catch { /* swallow */ }
  if (!_migrationRunThisSession) {
    _migrationRunThisSession = true;
    if (wasDeprecated) {
      // Privacy-safe console signal - no PII, no network call.
      console.info(`locale migrated: ${cur} -> en (Phase 3 of locale transition)`);
    } else if (wasJunk) {
      console.info(`locale migrated: ${cur} -> en (unknown locale)`);
    }
  }
}

let dict = {};
let locale = DEFAULT_LOCALE;
let loadedFor = null;

export function currentLocale() {
  return locale;
}

export async function setLocale(lc) {
  if (!SUPPORTED.includes(lc)) lc = DEFAULT_LOCALE;
  locale = lc;
  storage.setSettings({ uiLocale: lc });
  await loadDict();
}

async function loadDict() {
  if (loadedFor === locale) return;
  try {
    const res = await fetch(`locales/${locale}.json`);
    if (res.ok) {
      dict = await res.json();
      loadedFor = locale;
    } else if (locale !== DEFAULT_LOCALE) {
      // Fallback to default
      const fallback = await fetch(`locales/${DEFAULT_LOCALE}.json`);
      dict = await fallback.json();
      loadedFor = DEFAULT_LOCALE;
    }
  } catch (err) {
    console.warn('i18n: dictionary load failed; falling back to keys', err);
    dict = {};
  }
}

// IMP-074 (audit round-6): privacy-preserving referrer-based locale
// detection. When a user lands from a Vietnamese / Indonesian / Nepali /
// Chinese-domain referrer, weight that locale higher than the bare
// navigator.language signal. The referrer is per-request and never
// stored - same privacy posture as the rest of the app.
// Phase 3 of locale transition (2026-05-06): only India hints survive.
// The four deprecated-locale hints were removed alongside SUPPORTED.
const REFERRER_DOMAIN_HINTS = {
  '.in':       'hi',
  '.co.in':    'hi',
};

function _hintFromReferrer() {
  try {
    const ref = document.referrer || '';
    if (!ref) return null;
    const url = new URL(ref);
    const host = (url.hostname || '').toLowerCase();
    for (const [suffix, lc] of Object.entries(REFERRER_DOMAIN_HINTS)) {
      if (host.endsWith(suffix)) return lc;
    }
  } catch { /* ignore - bad referrer URL */ }
  return null;
}

/**
 * Initialize from saved settings or browser language. Idempotent.
 *
 * ISSUE-029 (audit round-4): when the browser language picks a non-EN
 * locale on first init (no saved setting), surface a one-time toast so
 * the user knows the auto-detection happened and how to override it.
 *
 * IMP-074 (audit round-6): referrer-domain hint takes precedence over
 * bare navigator.language IF the user hasn't yet picked a locale. A
 * Vietnamese visitor arriving from a .vn blog gets VI even if their
 * device locale is EN.
 */
export async function initI18n() {
  // Phase 2 of locale transition (2026-05-06): migrate persisted vi/id/
  // ne/zh -> en BEFORE any locale-dependent rendering. After Phase 3
  // ships these locales become un-supported; this hook makes the
  // existing-user journey through the transition silent.
  migrateLocaleSetting();
  const saved = storage.getSettings().uiLocale;
  let initial = saved;
  let auto = false;
  if (!initial) {
    const refHint = _hintFromReferrer();
    if (refHint && SUPPORTED.includes(refHint)) {
      initial = refHint;
      auto = (initial !== DEFAULT_LOCALE);
    } else {
      // ISSUE-066 (audit round-7): consult navigator.languages[] (plural -
      // the priority-ordered array of all browser-language preferences)
      // before falling back to navigator.language alone. For users whose
      // device is en-US but Accept-Language is "vi-VN, en-US", the hint
      // to default to vi is found in navigator.languages[0]. Pick the
      // FIRST entry whose primary subtag is in SUPPORTED.
      let pickedFromList = null;
      const langs = Array.isArray(navigator.languages) ? navigator.languages : [];
      for (const tag of langs) {
        const lc = (tag || '').split('-')[0].toLowerCase();
        if (SUPPORTED.includes(lc)) { pickedFromList = lc; break; }
      }
      if (pickedFromList) {
        initial = pickedFromList;
      } else {
        const browserLc = (navigator.language || 'en').split('-')[0].toLowerCase();
        initial = SUPPORTED.includes(browserLc) ? browserLc : DEFAULT_LOCALE;
      }
      auto = (initial !== DEFAULT_LOCALE);
    }
  }
  await setLocale(initial);
  if (auto) {
    queueMicrotask(() => _flashAutoLocaleToast(initial));
  }
}

const NATIVE_NAMES = {
  en: 'English',
  hi: 'हिन्दी',
};

function _flashAutoLocaleToast(lc) {
  if (document.getElementById('locale-auto-toast')) return;
  // ISSUE-046 (audit round-5): render the toast in the user's
  // detected locale rather than English. The toast is the very first
  // string a non-EN learner sees; English-framed copy around a native
  // language label is confusing. Falls back to EN if the keys are
  // missing in the locale (which they shouldn't be - round-4 ISSUE-026
  // added home.locale_auto_prefix + home.locale_auto_suffix to all 5).
  const prefix = t('home.locale_auto_prefix');
  const suffix = t('home.locale_auto_suffix');
  // Defensive: if t() returned the bare key (lookup miss), fall back.
  const safePrefix = prefix === 'home.locale_auto_prefix' ? 'App language:' : prefix;
  const safeSuffix = suffix === 'home.locale_auto_suffix' ? '- change anytime in Settings.' : suffix;
  const toast = document.createElement('div');
  toast.id = 'locale-auto-toast';
  toast.className = 'locale-auto-toast';
  toast.setAttribute('role', 'status');
  toast.setAttribute('aria-live', 'polite');
  toast.setAttribute('lang', lc);
  toast.innerHTML = `
    ${safePrefix} <strong lang="${lc}">${NATIVE_NAMES[lc] || lc}</strong>
    <span class="muted small">${safeSuffix}</span>
    <button type="button" class="locale-auto-toast-close" aria-label="Dismiss">×</button>
  `;
  document.body.appendChild(toast);
  const dismiss = () => { toast.classList.add('is-leaving'); setTimeout(() => toast.remove(), 200); };
  toast.querySelector('.locale-auto-toast-close')?.addEventListener('click', dismiss);
  // Auto-dismiss after 8 seconds.
  setTimeout(dismiss, 8000);
}

/**
 * Lookup with optional placeholder substitution.
 * Keys use dot notation (e.g. 'drill.start'). Missing keys return the key.
 *
 * ISSUE-041 / IMP-059 (audit round-5): underscore-prefixed top-level
 * keys are reserved for schema metadata (e.g., `_meta.provenance`,
 * `_meta.note`) and are NOT addressable by t(). Caller asking for
 * `_meta.something` always gets the key back as a fallback. This keeps
 * the i18n keyspace clean of metadata leaks.
 */
export function t(key, vars = {}) {
  if (typeof key !== 'string' || !key) return key;
  if (key.startsWith('_')) return key;  // schema metadata, not user-facing
  const parts = key.split('.');
  let cur = dict;
  for (const p of parts) {
    if (cur && typeof cur === 'object' && p in cur) cur = cur[p];
    else return key; // missing - return key as fallback
  }
  if (typeof cur !== 'string') return key;
  return cur.replace(/\$\{(\w+)\}/g, (_, name) => vars[name] ?? `\${${name}}`);
}

export const supportedLocales = SUPPORTED.slice();
