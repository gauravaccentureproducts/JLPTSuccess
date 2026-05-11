// IMP-126 (richness audit, 2026-05-09): authentic-content layer.
// The audit's largest leverage gap was 0% authentic real-world JP
// across every existing surface. This module renders the starter
// corpus from data/authentic.json — signs, menus, transit, shop,
// notice — grouped by category as cards.
import { renderJa } from './furigana.js';
import { t } from './i18n.js';

let dataCache = null;

async function loadData() {
  if (dataCache) return dataCache;
  const res = await fetch('data/authentic.json');
  dataCache = await res.json();
  return dataCache;
}

const CATEGORY_LABEL = {
  signs:    { en: 'Signs',                  ja: 'かんばん' },
  menu:     { en: 'Menu / dining',          ja: 'メニュー' },
  transit:  { en: 'Transit / station',      ja: 'えき' },
  shop:     { en: 'Shop / business hours',  ja: 'みせ' },
  notice:   { en: 'Notices / warnings',     ja: 'おしらせ' },
  // Added in IMP-126 round-3 (2026-05-10):
  weather:  { en: 'Weather forecast',       ja: 'てんき' },
  hospital: { en: 'Hospital / health',      ja: 'びょういん' },
  post:     { en: 'Post office / parcels',  ja: 'ゆうびんきょく' },
  time:     { en: 'Time / business hours',  ja: 'じかん' },
};

const CATEGORY_ORDER = ['signs', 'menu', 'transit', 'shop', 'notice',
                        'weather', 'hospital', 'post', 'time'];

export async function renderAuthentic(container) {
  const data = await loadData();
  const items = data.items || [];

  const byCat = new Map();
  for (const cat of CATEGORY_ORDER) byCat.set(cat, []);
  for (const it of items) {
    if (byCat.has(it.category)) byCat.get(it.category).push(it);
  }

  const sections = CATEGORY_ORDER.map(cat => {
    const list = byCat.get(cat) || [];
    if (!list.length) return '';
    const label = CATEGORY_LABEL[cat] || { en: cat, ja: cat };
    const cards = list.map(renderItemCard).join('');
    return `
      <section class="authentic-section" id="auth-${cat}">
        <h3 class="authentic-cat-title">
          <span lang="ja">${esc(label.ja)}</span>
          <span class="muted small"> · ${esc(label.en)}</span>
        </h3>
        <div class="authentic-grid">${cards}</div>
      </section>
    `;
  }).join('');

  container.innerHTML = `
    <article class="authentic-root">
      <a class="back-link" href="#/home">← Home</a>
      <h2>Authentic Japanese (real-world signs &amp; phrases)</h2>
      <p class="page-lede">
        ${items.length} starter entries you'd actually see in Japan — station signs,
        menu prices, shop hours, public-space notices. Every entry sticks to the
        N5 kanji whitelist (or kana when the kanji is N4+); the goal is real-world
        usage, not vocabulary expansion beyond N5.
      </p>
      <p class="muted small">
        Tap a card to study; click <em>Pronounce</em> to use your device's
        speech engine if available (no audio is bundled — privacy-preserving).
      </p>
      ${sections}
    </article>
  `;

  // Wire pronunciation buttons. Uses the SpeechSynthesis Web API
  // (built-in to every browser; no network call). Falls back gracefully
  // when no JA voice is installed.
  container.querySelectorAll('[data-auth-speak]').forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.dataset.authSpeak || '';
      if (!('speechSynthesis' in window) || !text) return;
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = 'ja-JP';
      utter.rate = 0.9;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utter);
    });
  });
}

function renderItemCard(it) {
  const ja = it.ja || '';
  const reading = it.reading || '';
  return `
    <div class="authentic-card" data-category="${esc(it.category)}">
      <div class="authentic-card-ja" lang="ja">${renderJa(ja)}</div>
      ${reading && reading !== ja ? `
        <div class="authentic-card-reading muted small" lang="ja">${esc(reading)}</div>
      ` : ''}
      <div class="authentic-card-gloss"><strong>${esc(it.gloss_en || '')}</strong></div>
      ${it.gloss_hi ? `<div class="authentic-card-gloss-hi muted small" lang="hi">${esc(it.gloss_hi)}</div>` : ''}
      ${it.context ? `<p class="authentic-card-context muted small">${esc(it.context)}</p>` : ''}
      ${it.vocab_refs?.length ? `
        <p class="authentic-card-vocab-refs muted small">
          Study vocab: ${it.vocab_refs.map(vid => `<a href="#/learn/${encodeURIComponent(vid)}">${esc(vidLabel(vid))}</a>`).join(', ')}
        </p>
      ` : ''}
      ${it.kanji_refs?.length ? `
        <p class="authentic-card-kanji-refs muted small">
          Study kanji: ${it.kanji_refs.map(kid => `<a href="#/kanji/${encodeURIComponent(vidLabel(kid))}" lang="ja">${esc(vidLabel(kid))}</a>`).join(' ')}
        </p>
      ` : ''}
      ${it.grammar_refs?.length ? `
        <p class="authentic-card-grammar-refs muted small">
          Study grammar: ${it.grammar_refs.map(pid => `<a href="#/learn/${encodeURIComponent(pid)}">${esc(pid)}</a>`).join(', ')}
        </p>
      ` : ''}
      <div class="authentic-card-actions">
        <button type="button" class="btn-secondary btn-tiny" data-auth-speak="${esc(ja)}"
                title="Read aloud (uses your device's voice — no network call)">
          🔊 Pronounce
        </button>
      </div>
    </div>
  `;
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

// IMP-WAVE-AUTHENTIC-XLINK (2026-05-11): pull the trailing
// dot-delimited segment out of a vocab id like
// "n5.vocab.13-locations-and-places-.びょういん" — that's the
// human-readable surface form. Falls back to the full id if
// the parse fails.
function vidLabel(vid) {
  if (typeof vid !== 'string') return String(vid);
  const idx = vid.lastIndexOf('.');
  return idx >= 0 ? vid.slice(idx + 1) : vid;
}
