// Cross-corpus search (Brief 2 §8).
// Searches grammar (id, pattern, meaning_en, explanation_en), vocab (form,
// reading, gloss, section), kanji (glyph, on, kun, meanings).
// Results group by type with a count per group. Click to deep-link.
// `/` keyboard shortcut focuses the input. Works offline once data loads.

let bank = null;
let panel = null;
// Active focus index across the flat result list (-1 = input still focused).
// Maintained by the keyboard-nav handler so ↑/↓/Enter work end-to-end.
let activeIndex = -1;

async function loadBank() {
  if (bank) return bank;
  try {
    const [g, v, k] = await Promise.all([
      fetch('data/grammar.json').then(r => r.json()),
      fetch('data/vocab.json').then(r => r.json()).catch(() => ({ entries: [] })),
      fetch('data/kanji.json').then(r => r.json()).catch(() => ({ entries: [] })),
    ]);
    bank = {
      grammar: (g.patterns || []).map(p => ({
        id: p.id, label: p.pattern, gloss: p.meaning_en || '',
        haystack: ((p.id||'') + ' ' + (p.pattern||'') + ' ' + (p.meaning_en||'') + ' ' + (p.explanation_en||'')).toLowerCase(),
      })),
      // Vocab: keep `form` as the route-id (matches the per-word detail route
      // #/learn/vocab/<form>) but also surface `reading` separately so
      // kanji-form entries show the kana reading inline ("新しい — あたらしい — new").
      vocab: (v.entries || []).slice(0, 1500).map(e => ({
        id: e.form, label: e.form, gloss: e.gloss || '', reading: e.reading || '',
        haystack: ((e.form||'') + ' ' + (e.reading||'') + ' ' + (e.gloss||'')).toLowerCase(),
      })),
      kanji: (k.entries || []).map(e => ({
        id: e.glyph, label: e.glyph, gloss: (e.meanings || []).join(', '),
        haystack: ((e.glyph||'') + ' ' + (e.on||[]).join(' ') + ' ' + (e.kun||[]).join(' ') + ' ' + (e.meanings||[]).join(' ')).toLowerCase(),
      })),
    };
  } catch {
    bank = { grammar: [], vocab: [], kanji: [] };
  }
  return bank;
}

function search(query) {
  const q = (query || '').trim().toLowerCase();
  if (!q) return { grammar: [], vocab: [], kanji: [] };
  const limit = 8;
  const matches = (arr) => arr.filter(x => x.haystack.includes(q)).slice(0, limit);
  // Vocab can have repeated `form` entries when the same word appears in
  // multiple thematic sections (e.g., 名前 in §1 and §15). Dedupe by form
  // so the result list doesn't show the same word twice with the same
  // route — the click would land on the same detail page anyway.
  const dedupeByLabel = (arr) => {
    const seen = new Set();
    return arr.filter(x => {
      if (seen.has(x.label)) return false;
      seen.add(x.label);
      return true;
    });
  };
  return {
    grammar: matches(bank.grammar),
    vocab: dedupeByLabel(matches(bank.vocab)),
    kanji: matches(bank.kanji),
  };
}

// URL builders. Each maps a result item to its canonical route. Vocab
// previously routed everything to #/learn (the Learn hub) — wrong; the
// per-word detail route is #/learn/vocab/<form>. Fixed 2026-05-02.
const HREFS = {
  grammar: it => `#/learn/${encodeURIComponent(it.id)}`,
  kanji:   it => `#/kanji/${encodeURIComponent(it.id)}`,
  vocab:   it => `#/learn/vocab/${encodeURIComponent(it.id)}`,
};

function renderResults(results) {
  const total = results.grammar.length + results.vocab.length + results.kanji.length;
  if (total === 0) return `<p class="search-empty muted" role="status">No matches.</p>`;
  // Render in display order: Grammar → Kanji → Vocab. The flat `idx`
  // counter feeds the keyboard-nav handler so ↑/↓ traverse all groups.
  let idx = 0;
  const renderItem = (it, kind) => {
    const href = HREFS[kind](it);
    const dataIdx = idx++;
    // For vocab: if reading differs from form (i.e., form contains kanji),
    // show "form (reading) — gloss". Otherwise just "form — gloss".
    const labelHTML = (kind === 'vocab' && it.reading && it.reading !== it.label)
      ? `<span lang="ja">${esc(it.label)}</span> <span class="muted small" lang="ja">(${esc(it.reading)})</span>`
      : `<span lang="ja">${esc(it.label)}</span>`;
    return `
      <li><a href="${href}" data-idx="${dataIdx}" role="option">${labelHTML}${it.gloss ? ` <span class="muted small">- ${esc(it.gloss)}</span>` : ''}</a></li>
    `;
  };
  const renderGroup = (title, items, kind) => `
    <section class="search-group">
      <h4>${title} <span class="muted small">(${items.length})</span></h4>
      <ul>${items.map(it => renderItem(it, kind)).join('')}</ul>
    </section>
  `;
  return `
    ${results.grammar.length ? renderGroup('Grammar', results.grammar, 'grammar') : ''}
    ${results.kanji.length   ? renderGroup('Kanji',   results.kanji,   'kanji')   : ''}
    ${results.vocab.length   ? renderGroup('Vocab',   results.vocab,   'vocab')   : ''}
    <p class="search-status visually-hidden" aria-live="polite">${total} ${total === 1 ? 'result' : 'results'}.</p>
  `;
}

function ensurePanel() {
  if (panel) return panel;
  panel = document.createElement('div');
  panel.className = 'search-panel';
  panel.hidden = true;
  panel.setAttribute('role', 'listbox');
  panel.setAttribute('aria-label', 'Search results');
  document.body.appendChild(panel);
  // Outside-click: hide. Inside-click: let the link's own navigation
  // handle it; we don't need to hide here since hash-route navigation
  // re-renders main and unmounts the search input naturally.
  document.addEventListener('click', (ev) => {
    if (panel.hidden) return;
    if (panel.contains(ev.target)) return;
    if (ev.target.id === 'search-input') return;
    panel.hidden = true;
    activeIndex = -1;
  });
  return panel;
}

function positionPanel(input) {
  const r = input.getBoundingClientRect();
  // Clamp width so the panel never overflows the viewport on narrow
  // screens. On mobile (<480px) the panel goes near-full-width with a
  // small side margin; on desktop the natural width is preserved.
  const vw = document.documentElement.clientWidth;
  const minW = Math.min(320, vw - 24);
  const naturalW = Math.max(r.width, minW);
  const maxW = vw - 24;
  const w = Math.min(naturalW, maxW);
  let left = r.left + window.scrollX;
  // If the panel would extend past the right edge, shift it left so it fits.
  if (left + w > window.scrollX + vw - 12) {
    left = Math.max(window.scrollX + 12, window.scrollX + vw - w - 12);
  }
  panel.style.top = `${r.bottom + 4 + window.scrollY}px`;
  panel.style.left = `${left}px`;
  panel.style.width = `${w}px`;
}

// Keyboard nav: ↓/↑ moves through results, Enter follows the highlighted
// link, Escape clears + closes. Wraps top→bottom and bottom→top.
function highlightItem(items, idx) {
  items.forEach(a => a.classList.remove('is-active'));
  if (idx >= 0 && idx < items.length) {
    items[idx].classList.add('is-active');
    items[idx].scrollIntoView({ block: 'nearest' });
  }
}

export async function initSearch() {
  const input = document.getElementById('search-input');
  if (!input) return;
  ensurePanel();
  input.setAttribute('role', 'combobox');
  input.setAttribute('aria-autocomplete', 'list');
  input.setAttribute('aria-expanded', 'false');
  // Lazy-load bank on first focus
  let loaded = false;
  const ensureLoaded = async () => { if (!loaded) { await loadBank(); loaded = true; } };
  input.addEventListener('focus', ensureLoaded);
  input.addEventListener('input', async () => {
    await ensureLoaded();
    const q = input.value;
    if (!q.trim()) {
      panel.hidden = true;
      input.setAttribute('aria-expanded', 'false');
      activeIndex = -1;
      return;
    }
    const results = search(q);
    panel.innerHTML = renderResults(results);
    positionPanel(input);
    panel.hidden = false;
    input.setAttribute('aria-expanded', 'true');
    activeIndex = -1;
  });
  input.addEventListener('blur', () => {
    // Defer hide so click on a result still works
    setTimeout(() => {
      if (!panel.matches(':hover')) {
        panel.hidden = true;
        input.setAttribute('aria-expanded', 'false');
        activeIndex = -1;
      }
    }, 150);
  });
  input.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape') {
      input.value = '';
      panel.hidden = true;
      input.setAttribute('aria-expanded', 'false');
      activeIndex = -1;
      input.blur();
      return;
    }
    if (panel.hidden) return;
    const items = [...panel.querySelectorAll('a[data-idx]')];
    if (items.length === 0) return;
    if (ev.key === 'ArrowDown') {
      ev.preventDefault();
      activeIndex = (activeIndex + 1) % items.length;
      highlightItem(items, activeIndex);
    } else if (ev.key === 'ArrowUp') {
      ev.preventDefault();
      activeIndex = activeIndex <= 0 ? items.length - 1 : activeIndex - 1;
      highlightItem(items, activeIndex);
    } else if (ev.key === 'Enter') {
      // Only intercept Enter when a result is highlighted; otherwise
      // let the form / default behavior (no-op) handle it.
      if (activeIndex >= 0 && items[activeIndex]) {
        ev.preventDefault();
        items[activeIndex].click();
      }
    }
  });
  // '/' keyboard shortcut to focus search (Brief 2 §8).
  document.addEventListener('keydown', (ev) => {
    const t = ev.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    if (ev.key === '/' && !ev.metaKey && !ev.ctrlKey && !ev.altKey) {
      ev.preventDefault();
      input.focus();
      input.select();
    }
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
