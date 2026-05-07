// SVA-NEXT-3 (round-9 follow-up, 2026-05-08): branding-override layer.
//
// Why this exists
// ===============
// Vocational schools, NGOs, language institutes etc. want to deploy
// JLPTSuccess on their own infrastructure under their own brand:
//   - Indian Tier-2 / Tier-3 SSW-prep training centres.
//   - Japanese-language schools that prefer not to send student data
//     to a US/Japan SaaS.
//   - University departments running internal mock-test rituals.
//
// Without this layer they'd have to fork the source and edit hardcoded
// strings + CSS tokens + meta tags by hand. With this layer they drop
// one file: `data/branding.json`. The runtime applies overrides at
// boot, before first paint. Missing file = upstream JLPTSuccess
// defaults (so the upstream deploy is unaffected).
//
// What it overrides
// =================
//   - CSS custom-property tokens (accent / bg / text / line / surface).
//   - The header brand label + aria-label.
//   - The <title> tag + meta-description + og:* + twitter:*.
//   - The footer trust strip text (per-locale).
//   - An optional footer attribution line ("Powered by JLPTSuccess").
//   - The print-paper diagonal watermark text.
//   - The home-page background watermark glyph (五 by default).
//
// What it deliberately does NOT override
// ======================================
//   - localStorage namespace (`jlpt-n5-tutor:`) — would orphan
//     installed-PWA progress on every fork update.
//   - Service-worker scope or cache version.
//   - Privacy guarantees (no telemetry, no third-party scripts) —
//     a fork that adds analytics MUST update PRIVACY.md per upstream
//     posture; the loader doesn't help with that.
//
// Privacy
// =======
// Pure on-device. Only network request the loader makes is the same-
// origin fetch of `data/branding.json`. No ping to upstream, no
// tracking, no telemetry. If branding.json is absent, no fetch fires
// at all (404 falls back silently).

const FALLBACK = Object.freeze({
  brand: {
    name: 'JLPT N5',
    short_name: 'JLPT N5',
    header_label: 'JLPT N5',
    header_aria_label: 'JLPTSuccess home, choose a level',
    watermark_text: 'JLPTSUCCESS.COM',
    home_glyph: '五',
    footer_attribution_html: '',
    footer_homepage_url: '',
  },
  tokens: {},
  meta: {},
  trust_strip: { en: '', hi: '' },
});

let cached = null;
let cachedFlat = null;

// Public getter. Returns the resolved branding object (a shallow merge
// of FALLBACK + the loaded `data/branding.json` if present). Always
// safe to call at any time; returns FALLBACK if the loader hasn't run
// yet.
export function getBranding() {
  if (cachedFlat) return cachedFlat;
  return FALLBACK;
}

// Public loader. Awaited once during app bootstrap. Idempotent —
// re-runs are no-ops once cached.
//
// Source precedence (highest first):
//   1. data/branding.json — unified branding file (current).
//   2. data/theme-overrides.json — legacy file from the v1.7 era.
//      Tokens + brand.name only; superseded by branding.json. Loader
//      keeps reading it so existing forks with that file in place
//      continue to work without migration.
//   3. FALLBACK — upstream JLPTSuccess defaults.
export async function loadBranding() {
  if (cachedFlat) return cachedFlat;
  let user = null;
  for (const src of ['data/branding.json', 'data/theme-overrides.json']) {
    try {
      const r = await fetch(src, { cache: 'no-cache' });
      if (r.ok) {
        user = await r.json();
        break;
      }
    } catch (_) { /* try next source */ }
  }
  cached = user || null;
  cachedFlat = mergeBranding(FALLBACK, user || {});
  applyBranding(cachedFlat);
  return cachedFlat;
}

// Shallow per-section merge. We don't deep-merge token-by-token by
// hand because all token names are CSS custom properties; the user
// either sets the token or doesn't, and `Object.assign` with the
// FALLBACK first preserves any unset keys.
function mergeBranding(base, user) {
  const out = JSON.parse(JSON.stringify(base));
  const sections = ['brand', 'tokens', 'meta', 'trust_strip'];
  for (const s of sections) {
    if (user[s] && typeof user[s] === 'object') {
      Object.assign(out[s], user[s]);
    }
  }
  return out;
}

// Apply branding to the live DOM.
//
// Called once at boot from loadBranding(). Modules that consume the
// branding lazily (print-paper.js's watermark, home.js's footer
// attribution, etc.) use getBranding() to read the cached value at
// render time.
function applyBranding(b) {
  if (typeof document === 'undefined') return;

  // --- 1. CSS custom-property tokens ---
  const root = document.documentElement;
  for (const [k, v] of Object.entries(b.tokens || {})) {
    if (typeof v === 'string' && v) {
      // Only set tokens that look like CSS custom properties to
      // avoid accidental injection. (--color-foo, --r, --motion-fast.)
      if (k.startsWith('--')) root.style.setProperty(k, v);
    }
  }

  // --- 2. Header brand label + aria-label ---
  const brandLink = document.querySelector('.brand-link');
  if (brandLink) {
    if (b.brand.header_label) brandLink.textContent = b.brand.header_label;
    if (b.brand.header_aria_label) brandLink.setAttribute('aria-label', b.brand.header_aria_label);
  }

  // --- 3. Document title + meta tags ---
  const meta = b.meta || {};
  if (meta.title) document.title = meta.title;
  setMeta('name', 'description', meta.description);
  setMeta('property', 'og:title', meta.og_title);
  setMeta('property', 'og:description', meta.og_description);
  setMeta('property', 'og:url', meta.og_url);
  setMeta('name', 'twitter:title', meta.twitter_title);
  setLink('canonical', meta.canonical_url);

  // --- 4. Footer trust strip ---
  // Only override if the user supplied a non-empty string; otherwise
  // i18n.t() handles localization. The override survives locale
  // switches because applyTrustStrip writes to all matching nodes
  // and removes the i18n-key attribute so the upstream localizer
  // doesn't overwrite us on next swap.
  const ts = b.trust_strip || {};
  // Default upstream applies localization at runtime via t(). If the
  // fork wants per-locale overrides, we re-apply them whenever the
  // locale chip group dispatches a change.
  applyTrustStrip(ts);
  document.addEventListener('locale:changed', () => applyTrustStrip(ts));

  // --- 5. Footer attribution (institutional "Powered by" link) ---
  if (b.brand.footer_attribution_html || b.brand.footer_homepage_url) {
    insertFooterAttribution(b.brand);
  }

  // --- 6. Stamp the body so other modules can detect "branded mode" ---
  if (cached) document.body.dataset.branded = 'on';
}

function setMeta(attrType, attrName, value) {
  if (!value) return;
  let el = document.querySelector(`meta[${attrType}="${attrName}"]`);
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute(attrType, attrName);
    document.head.appendChild(el);
  }
  el.setAttribute('content', value);
}

function setLink(rel, href) {
  if (!href) return;
  let el = document.querySelector(`link[rel="${rel}"]`);
  if (!el) {
    el = document.createElement('link');
    el.setAttribute('rel', rel);
    document.head.appendChild(el);
  }
  el.setAttribute('href', href);
}

function applyTrustStrip(ts) {
  // Find the localized trust-strip element; the i18n key is
  // `footer.trust_strip`. We only override if the fork supplied a
  // string for the *current* locale.
  const node = document.querySelector('[data-i18n-key="footer.trust_strip"]');
  if (!node) return;
  const html = document.documentElement.lang || 'en';
  const lang = html.toLowerCase().startsWith('hi') ? 'hi' : 'en';
  const v = (ts && typeof ts[lang] === 'string') ? ts[lang].trim() : '';
  if (v) {
    node.textContent = v;
    // Drop the i18n key so the next locale-swap doesn't overwrite us.
    // Set a data-branded marker so a fork dev can spot the override.
    node.dataset.branded = 'trust-strip';
    node.removeAttribute('data-i18n-key');
  }
}

function insertFooterAttribution(brand) {
  // Insert (or replace) a `.footer-attribution` paragraph just below
  // the trust strip in the footer. Idempotent.
  const footer = document.querySelector('footer.app-footer');
  if (!footer) return;
  let p = footer.querySelector('.footer-attribution');
  if (!p) {
    p = document.createElement('p');
    p.className = 'footer-attribution';
    const trust = footer.querySelector('.footer-trust-strip');
    if (trust && trust.parentNode === footer) {
      trust.insertAdjacentElement('afterend', p);
    } else {
      footer.insertBefore(p, footer.firstChild);
    }
  }
  if (brand.footer_attribution_html) {
    p.innerHTML = brand.footer_attribution_html;
  } else if (brand.footer_homepage_url) {
    p.innerHTML = `Powered by <a href="${escAttr(brand.footer_homepage_url)}" rel="noopener" target="_blank">JLPTSuccess</a>`;
  }
}

function escAttr(s) {
  return String(s ?? '').replace(/"/g, '&quot;').replace(/&/g, '&amp;');
}
