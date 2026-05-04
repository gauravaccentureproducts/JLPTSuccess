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

const SUPPORTED = ['en', 'vi', 'id', 'ne', 'zh'];
const DEFAULT_LOCALE = 'en';

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

/**
 * Initialize from saved settings or browser language. Idempotent.
 *
 * ISSUE-029 (audit round-4): when the browser language picks a non-EN
 * locale on first init (no saved setting), surface a one-time toast so
 * the user knows the auto-detection happened and how to override it.
 */
export async function initI18n() {
  const saved = storage.getSettings().uiLocale;
  let initial = saved;
  let auto = false;
  if (!initial) {
    const browserLc = (navigator.language || 'en').split('-')[0].toLowerCase();
    initial = SUPPORTED.includes(browserLc) ? browserLc : DEFAULT_LOCALE;
    auto = (initial !== DEFAULT_LOCALE);
  }
  await setLocale(initial);
  if (auto) {
    // Defer the toast so it lands after first paint, not during init.
    queueMicrotask(() => _flashAutoLocaleToast(initial));
  }
}

const NATIVE_NAMES = {
  en: 'English',
  vi: 'Tiếng Việt',
  id: 'Bahasa Indonesia',
  ne: 'नेपाली',
  zh: '中文',
};

function _flashAutoLocaleToast(lc) {
  if (document.getElementById('locale-auto-toast')) return;
  const t = document.createElement('div');
  t.id = 'locale-auto-toast';
  t.className = 'locale-auto-toast';
  t.setAttribute('role', 'status');
  t.setAttribute('aria-live', 'polite');
  t.innerHTML = `
    App language: <strong lang="${lc}">${NATIVE_NAMES[lc] || lc}</strong>
    <span class="muted small">— change anytime in Settings.</span>
    <button type="button" class="locale-auto-toast-close" aria-label="Dismiss">×</button>
  `;
  document.body.appendChild(t);
  const dismiss = () => { t.classList.add('is-leaving'); setTimeout(() => t.remove(), 200); };
  t.querySelector('.locale-auto-toast-close')?.addEventListener('click', dismiss);
  // Auto-dismiss after 8 seconds.
  setTimeout(dismiss, 8000);
}

/**
 * Lookup with optional placeholder substitution.
 * Keys use dot notation (e.g. 'drill.start'). Missing keys return the key.
 */
export function t(key, vars = {}) {
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
