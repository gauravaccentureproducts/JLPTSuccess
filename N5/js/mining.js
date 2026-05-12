// IMP-151 (richness audit, 2026-05-12): Migaku-style sentence-mining index.
//
// Single discovery route showing every vocab / kanji / grammar entry's
// authentic-card cross-links in one sortable, filterable table. The
// authentic-content layer already cross-links from cards -> entries
// (vocab_refs / kanji_refs / grammar_refs) and entries -> cards
// (authentic_refs). This view inverts the data into a single index
// for learners who want to "see all the real-world Japanese tied to
// my study items."
//
// Route: #/mining
//
// Design:
//   - Loads authentic.json + vocab.json + kanji.json + grammar.json
//   - Builds a flat entry list across the 3 skill corpora
//   - Filters entries to those with non-empty authentic_refs
//   - Each row: skill chip + entry display + linked card chips
//   - Filter buttons (All / Vocab / Kanji / Grammar) + sort toggle
//
// Implementation is read-only: no localStorage writes, no SRS state.
// Pure discovery surface; clicking a card chip jumps to #/authentic
// and clicking the entry jumps to its detail page.

import { renderJa } from './furigana.js';
import { t, currentLocale } from './i18n.js';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c]));

let _cache = null;

async function loadAll() {
  if (_cache) return _cache;
  const [aR, vR, kR, gR] = await Promise.all([
    fetch('data/authentic.json'),
    fetch('data/vocab.json'),
    fetch('data/kanji.json'),
    fetch('data/grammar.json'),
  ]);
  const [auth, vocab, kanji, grammar] = await Promise.all([
    aR.json(), vR.json(), kR.json(), gR.json(),
  ]);
  const authItems = (auth && auth.items) || [];
  const cardById = new Map();
  for (const c of authItems) cardById.set(c.id, c);

  const vocabEntries = (vocab && vocab.entries) || [];
  const kanjiEntries = (kanji && kanji.entries) || (Array.isArray(kanji) ? kanji : []);
  const grammarPatterns = (grammar && grammar.patterns) || [];

  _cache = { authItems, cardById, vocabEntries, kanjiEntries, grammarPatterns };
  return _cache;
}

// Build a unified flat list of entries with non-empty authentic_refs.
// Each entry has: { skill, id, display_label, display_sub, refs: [card_id...], href }
function buildIndex(data) {
  const out = [];

  for (const v of data.vocabEntries) {
    const refs = v.authentic_refs || [];
    if (!refs.length) continue;
    out.push({
      skill: 'vocab',
      id: v.id,
      display_label: v.form || v.reading || v.id,
      display_sub: v.gloss_en || v.gloss || '',
      reading: v.reading || '',
      refs,
      href: `#/learn/vocab/${encodeURIComponent(v.id)}`,
    });
  }

  for (const k of data.kanjiEntries) {
    const refs = k.authentic_refs || [];
    if (!refs.length) continue;
    out.push({
      skill: 'kanji',
      id: k.id,
      display_label: k.glyph || k.id,
      display_sub: (k.meanings || []).join(', '),
      reading: (k.kun || []).concat(k.on || []).join(' / '),
      refs,
      href: `#/kanji/${encodeURIComponent(k.id)}`,
    });
  }

  for (const p of data.grammarPatterns) {
    // Grammar uses authentic_refs for card-side cross-links.
    const refs = p.authentic_refs || [];
    if (!refs.length) continue;
    out.push({
      skill: 'grammar',
      id: p.id,
      display_label: p.pattern || p.id,
      display_sub: p.meaning_en || '',
      reading: '',
      refs,
      href: `#/learn/${encodeURIComponent(p.id)}`,
    });
  }

  return out;
}

const SKILL_LABEL = {
  vocab:   { en: 'Vocab',    ja: '語彙' },
  kanji:   { en: 'Kanji',    ja: '漢字' },
  grammar: { en: 'Grammar',  ja: '文法' },
};

const CATEGORY_COLOR = {
  hospital:   '#d6604d',
  menu:       '#f4a582',
  notice:     '#92c5de',
  post:       '#fddbc7',
  shop:       '#5aae61',
  signs:      '#4393c3',
  time:       '#b2182b',
  transit:    '#2166ac',
  weather:    '#9970ab',
};

export async function renderMining(container) {
  container.innerHTML = '<div class="placeholder"><p>Loading mining index…</p></div>';

  const data = await loadAll();
  const index = buildIndex(data);

  // Default state: show all, sort by skill then label.
  let filter = 'all';
  let sortMode = 'skill'; // 'skill' | 'label' | 'count'

  const cardChip = (cardId) => {
    const card = data.cardById.get(cardId);
    if (!card) return `<span class="mining-card-chip mining-card-missing" title="Missing card: ${esc(cardId)}">?</span>`;
    const color = CATEGORY_COLOR[card.category] || '#888';
    const ja = card.ja || cardId;
    const en = card.gloss_en || '';
    const title = `${ja} — ${en} (${card.category || '?'})`;
    return `<a class="mining-card-chip" href="#/authentic" data-card-id="${esc(cardId)}" title="${esc(title)}" style="border-left:3px solid ${color}">
      <span class="mining-card-ja" lang="ja">${esc(ja)}</span>
      ${en ? `<span class="mining-card-en muted small">${esc(en)}</span>` : ''}
    </a>`;
  };

  const rowHtml = (e) => `
    <li class="mining-row" data-skill="${esc(e.skill)}">
      <a class="mining-entry" href="${e.href}">
        <span class="mining-skill-badge mining-skill-${esc(e.skill)}" aria-label="${esc(SKILL_LABEL[e.skill]?.en || e.skill)}">${esc(SKILL_LABEL[e.skill]?.en?.[0] || '?')}</span>
        <span class="mining-entry-label" lang="ja">${esc(e.display_label)}</span>
        ${e.reading ? `<span class="mining-entry-reading muted small" lang="ja">${esc(e.reading)}</span>` : ''}
        ${e.display_sub ? `<span class="mining-entry-sub muted small">${esc(e.display_sub)}</span>` : ''}
      </a>
      <div class="mining-cards">
        ${e.refs.map(cardChip).join('')}
      </div>
      <span class="mining-count muted small" aria-label="linked cards">×${e.refs.length}</span>
    </li>
  `;

  const sortIndex = (arr) => {
    const copy = [...arr];
    if (sortMode === 'count') {
      copy.sort((a, b) => (b.refs.length - a.refs.length) || a.display_label.localeCompare(b.display_label));
    } else if (sortMode === 'label') {
      copy.sort((a, b) => a.display_label.localeCompare(b.display_label, 'ja'));
    } else {
      const skillOrder = { vocab: 0, kanji: 1, grammar: 2 };
      copy.sort((a, b) => (skillOrder[a.skill] - skillOrder[b.skill]) || a.display_label.localeCompare(b.display_label, 'ja'));
    }
    return copy;
  };

  const filtered = () => {
    const sorted = sortIndex(index);
    return filter === 'all' ? sorted : sorted.filter(e => e.skill === filter);
  };

  const counts = {
    all:     index.length,
    vocab:   index.filter(e => e.skill === 'vocab').length,
    kanji:   index.filter(e => e.skill === 'kanji').length,
    grammar: index.filter(e => e.skill === 'grammar').length,
  };

  const totalRefs = index.reduce((s, e) => s + e.refs.length, 0);

  const render = () => {
    const rows = filtered().map(rowHtml).join('');
    container.innerHTML = `
      <article class="mining-page">
        <header class="mining-header">
          <h2>${esc(t('mining.title') || 'Real-world cross-links')}</h2>
          <p class="muted small">${esc(t('mining.tagline') || 'Every vocab / kanji / grammar entry that links to one or more authentic real-Japan cards. Click an entry to jump to its detail page; click a card chip to browse the full authentic library.')}</p>
          <p class="muted small">${counts.all} entries linked across ${data.authItems.length} authentic cards (${totalRefs} cross-links total).</p>
        </header>

        <div class="mining-toolbar" role="toolbar" aria-label="Filters and sort">
          <div class="mining-filters" role="group" aria-label="Filter by skill">
            <button type="button" class="mining-filter ${filter==='all'?'active':''}"     data-filter="all">All <span class="muted small">(${counts.all})</span></button>
            <button type="button" class="mining-filter ${filter==='vocab'?'active':''}"   data-filter="vocab">Vocab <span class="muted small">(${counts.vocab})</span></button>
            <button type="button" class="mining-filter ${filter==='kanji'?'active':''}"   data-filter="kanji">Kanji <span class="muted small">(${counts.kanji})</span></button>
            <button type="button" class="mining-filter ${filter==='grammar'?'active':''}" data-filter="grammar">Grammar <span class="muted small">(${counts.grammar})</span></button>
          </div>
          <div class="mining-sort" role="group" aria-label="Sort order">
            <label for="mining-sort-select" class="muted small">Sort:</label>
            <select id="mining-sort-select" class="mining-sort-select">
              <option value="skill" ${sortMode==='skill'?'selected':''}>By skill, then label</option>
              <option value="label" ${sortMode==='label'?'selected':''}>Alphabetical (label)</option>
              <option value="count" ${sortMode==='count'?'selected':''}>By cross-link count (desc)</option>
            </select>
          </div>
        </div>

        <ol class="mining-list">
          ${rows || '<li class="placeholder">No cross-links match the current filter.</li>'}
        </ol>

        <p class="muted small" style="margin-top:24px;">
          <a href="#/authentic">← Browse the full authentic card library</a>
        </p>
      </article>
    `;
    wireEvents();
  };

  const wireEvents = () => {
    container.querySelectorAll('.mining-filter').forEach(btn => {
      btn.addEventListener('click', () => {
        filter = btn.dataset.filter;
        render();
      });
    });
    const sortSel = container.querySelector('#mining-sort-select');
    if (sortSel) {
      sortSel.addEventListener('change', () => {
        sortMode = sortSel.value;
        render();
      });
    }
  };

  render();
}
