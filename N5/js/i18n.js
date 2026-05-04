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
 */
export async function initI18n() {
  const saved = storage.getSettings().uiLocale;
  let initial = saved;
  if (!initial) {
    const browserLc = (navigator.language || 'en').split('-')[0].toLowerCase();
    initial = SUPPORTED.includes(browserLc) ? browserLc : DEFAULT_LOCALE;
  }
  await setLocale(initial);
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
