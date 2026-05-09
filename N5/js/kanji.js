// Single-kanji detail page (Brief 2 §14.1).
// Routed via #/kanji/<glyph> - shows glyph, on/kun-yomi, meanings,
// stroke-order SVG slot, and a "back to list" link.
// The stroke-order SVG path lives in data/kanji.json under stroke_order_svg;
// the SVG file itself ships separately (KanjiVG drop-in target).
import * as storage from './storage.js';
import { currentLocale } from './i18n.js';
import { renderItemBadge } from './provenance-badge.js';

// IMP-047 (audit round-5): pick locale-aware meanings if available, else
// fall back to English. Per-locale field is `meanings_hi` (post-2026-05-06
// IMP-096 narrowing — earlier en/vi/id/ne/zh shell collapsed to en+hi);
// `meanings` is the canonical English source-of-truth.
function localizedMeanings(entry) {
  const lc = currentLocale();
  if (lc && lc !== 'en') {
    const localized = entry[`meanings_${lc}`];
    if (Array.isArray(localized) && localized.length) return localized;
  }
  return entry.meanings || [];
}

let bank = null;

async function loadBank() {
  if (bank) return bank;
  const res = await fetch('data/kanji.json');
  bank = await res.json();
  return bank;
}

export async function renderKanji(container, params) {
  await loadBank();
  const entries = bank.entries || [];
  const glyph = params ? decodeURIComponent(params) : '';
  if (!glyph) return renderIndex(container, entries);
  const entry = entries.find(e => e.glyph === glyph);
  if (!entry) {
    container.innerHTML = `
      <div class="placeholder">
        <h2>Kanji not found</h2>
        <p>No N5 entry for <strong lang="ja">${esc(glyph)}</strong>.</p>
        <p><a href="#/kanji" class="btn-primary" style="text-decoration:none">Back to kanji list</a></p>
      </div>
    `;
    return;
  }
  return renderDetail(container, entry, entries);
}

// IMP-003: kanji index now ships with a search/filter row.
// Filters are AND-composed: text query matches glyph / on / kun / meaning;
// stroke chip selects a stroke-count bracket; lesson chip selects a
// lesson_order range. IMP-025 (2026-05-04 round 2): added a "Sort by"
// dropdown so the user can re-order the result set by lesson, frequency,
// stroke count, or glyph (Unicode codepoint). State is module-local so
// the filters persist while the user navigates within the index but reset
// on a fresh page load.
let _filterText = '';
let _filterStroke = 'all';   // 'all' | '1-5' | '6-10' | '11-15' | '16+'
let _filterLesson = 'all';   // 'all' | '1-30' | '31-60' | '61-90' | '91-106'
let _sortBy = 'lesson';      // 'lesson' | 'frequency' | 'strokes' | 'glyph'

function _strokeBracket(n) {
  if (n == null) return '';
  if (n <= 5) return '1-5';
  if (n <= 10) return '6-10';
  if (n <= 15) return '11-15';
  return '16+';
}
function _lessonBracket(n) {
  if (n == null) return '';
  if (n <= 30) return '1-30';
  if (n <= 60) return '31-60';
  if (n <= 90) return '61-90';
  return '91-106';
}

function _matchesFilter(e, q, strokeBr, lessonBr) {
  if (q) {
    const additional = e.additional_readings || {};
    const hay = [
      e.glyph || '',
      ...(e.on || []),
      ...(e.kun || []),
      ...(additional.on || []),
      ...(additional.kun || []),
      ...(e.meanings || []),
    ].join(' ').toLowerCase();
    if (!hay.includes(q)) return false;
  }
  if (strokeBr !== 'all' && _strokeBracket(e.stroke_count) !== strokeBr) return false;
  if (lessonBr !== 'all' && _lessonBracket(e.lesson_order) !== lessonBr) return false;
  return true;
}

function _sortKey(e) {
  switch (_sortBy) {
    case 'frequency': return e.frequency_rank ?? 999;
    case 'strokes':   return e.stroke_count ?? 999;
    case 'glyph':     return e.glyph || '';
    case 'lesson':
    default:          return e.lesson_order ?? 999;
  }
}

function renderIndex(container, entries) {
  const q = _filterText.trim().toLowerCase();
  const filtered = entries
    .filter(e => _matchesFilter(e, q, _filterStroke, _filterLesson))
    .slice()
    .sort((a, b) => {
      const ka = _sortKey(a), kb = _sortKey(b);
      if (typeof ka === 'string') return ka.localeCompare(kb);
      return ka - kb;
    });
  // 2026-05-06 (user request): list-tile pages show only the kanji glyph
  // for active-recall practice. Readings + meanings appear on the detail
  // page after click-through. This lets learners self-assess "do I know
  // this kanji?" before revealing the answer.
  const cards = filtered.map(e => `
    <a class="kanji-card" href="#/kanji/${encodeURIComponent(e.glyph)}">
      <span class="kanji-card-glyph" lang="ja">${esc(e.glyph)}</span>
    </a>
  `).join('');

  const chip = (group, value, label, active) =>
    `<button type="button" class="kanji-chip ${active ? 'active' : ''}"
       data-filter-group="${group}" data-filter-value="${value}">${esc(label)}</button>`;

  container.innerHTML = `
    <a class="back-link" href="#/learn">← Back to Learn</a>
    <h2>Kanji</h2>
    <p>${entries.length} kanji at JLPT N5 level. Tap any card for readings, meanings, and stroke order.</p>

    <div class="kanji-filters" role="search" aria-label="Filter kanji">
      <input type="search" id="kanji-filter-q" class="kanji-filter-input"
        placeholder="Search reading, meaning, or glyph (e.g. みず / water / 水)"
        value="${esc(_filterText)}" autocomplete="off" lang="ja"
        aria-label="Search kanji by reading, meaning, or glyph">

      <div class="kanji-filter-row" aria-label="Stroke count filter">
        <span class="kanji-filter-label">Strokes:</span>
        ${chip('stroke', 'all', 'All', _filterStroke === 'all')}
        ${chip('stroke', '1-5', '1-5', _filterStroke === '1-5')}
        ${chip('stroke', '6-10', '6-10', _filterStroke === '6-10')}
        ${chip('stroke', '11-15', '11-15', _filterStroke === '11-15')}
        ${chip('stroke', '16+', '16+', _filterStroke === '16+')}
      </div>

      <div class="kanji-filter-row" aria-label="Lesson order filter">
        <span class="kanji-filter-label">Lesson:</span>
        ${chip('lesson', 'all', 'All', _filterLesson === 'all')}
        ${chip('lesson', '1-30', '1-30', _filterLesson === '1-30')}
        ${chip('lesson', '31-60', '31-60', _filterLesson === '31-60')}
        ${chip('lesson', '61-90', '61-90', _filterLesson === '61-90')}
        ${chip('lesson', '91-106', '91-106', _filterLesson === '91-106')}
      </div>

      <div class="kanji-filter-row kanji-sort-row" aria-label="Sort kanji">
        <span class="kanji-filter-label">Sort:</span>
        <select id="kanji-sort" class="kanji-sort-select" aria-label="Sort kanji by">
          <option value="lesson"    ${_sortBy === 'lesson'    ? 'selected' : ''}>Lesson order (default)</option>
          <option value="frequency" ${_sortBy === 'frequency' ? 'selected' : ''}>Frequency rank</option>
          <option value="strokes"   ${_sortBy === 'strokes'   ? 'selected' : ''}>Stroke count</option>
          <option value="glyph"     ${_sortBy === 'glyph'     ? 'selected' : ''}>Glyph (Unicode order)</option>
        </select>
      </div>

      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${filtered.length}</strong> of ${entries.length}.
      </p>
    </div>

    <div class="kanji-card-grid">${cards || '<p class="muted">No kanji match the current filters.</p>'}</div>
  `;

  const input = document.getElementById('kanji-filter-q');
  if (input) {
    input.addEventListener('input', () => {
      _filterText = input.value;
      renderIndex(container, entries);
      // Re-focus the input after re-render and restore caret.
      const newInput = document.getElementById('kanji-filter-q');
      if (newInput) {
        newInput.focus();
        const v = newInput.value;
        newInput.setSelectionRange(v.length, v.length);
      }
    });
  }

  container.querySelectorAll('[data-filter-group]').forEach(btn => {
    btn.addEventListener('click', () => {
      const group = btn.dataset.filterGroup;
      const value = btn.dataset.filterValue;
      if (group === 'stroke') _filterStroke = value;
      else if (group === 'lesson') _filterLesson = value;
      renderIndex(container, entries);
    });
  });

  // IMP-025: sort dropdown
  const sortSelect = document.getElementById('kanji-sort');
  if (sortSelect) {
    sortSelect.addEventListener('change', () => {
      _sortBy = sortSelect.value;
      renderIndex(container, entries);
    });
  }
}

function renderDetail(container, entry, entries) {
  const idx = entries.findIndex(e => e.glyph === entry.glyph);
  const prev = idx > 0 ? entries[idx - 1] : null;
  const next = idx < entries.length - 1 ? entries[idx + 1] : null;
  // Mark-as-known parity (OPEN-10): kanji detail gets the same toggle
  // affordance as grammar pattern detail and vocab detail. Same vertical
  // position relative to the entry header.
  const isKnown = storage.isKanjiKnown(entry.glyph);
  container.innerHTML = `
    <article class="kanji-detail">
      <div class="srs-progress">
        <a href="#/kanji">← All kanji</a>
        <span class="muted small">${idx + 1} of ${entries.length}</span>
      </div>
      <div class="kanji-glyph-row pattern-header">
        <div class="kanji-glyph-cluster">
          <div class="kanji-glyph-big" lang="ja">${esc(entry.glyph)}</div>
          <div class="kanji-readings">
            ${entry.on?.length
                ? `<p><strong>On:</strong> <span lang="ja">${entry.on.map(esc).join(' / ')}</span></p>`
                : (Array.isArray(entry.on) ? `<p><strong>On:</strong> <span class="muted small">(none at N5)</span></p>` : '')}
            ${entry.kun?.length
                ? `<p><strong>Kun:</strong> <span lang="ja">${entry.kun.map(esc).join(' / ')}</span></p>`
                : (Array.isArray(entry.kun) ? `<p><strong>Kun:</strong> <span class="muted small">(none at N5)</span></p>` : '')}
            ${(() => { const m = localizedMeanings(entry); return m.length ? `<p><strong>Meaning:</strong> ${m.map(esc).join(', ')} ${renderItemBadge(entry, true)}</p>` : ''; })()}
          </div>
        </div>
        <label class="known-toggle" title="Manually mark this kanji as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-kanji" ${isKnown ? 'checked' : ''}>
          <span>Mark as known</span>
        </label>
      </div>
      ${(entry.radical || entry.radical_decomposition || entry.mnemonic) ? `
        <section class="kanji-mnemonic-block">
          <h3>Radical &amp; mnemonic</h3>
          ${entry.radical ? `
            <p><strong>Radical:</strong>
              <span class="kanji-radical-glyph" lang="ja">${esc(entry.radical.glyph || '')}</span>
              <span class="muted small">${esc(entry.radical.name || '')}</span>
            </p>
          ` : ''}
          ${entry.radical_decomposition?.length ? `
            <p><strong>Components:</strong>
              <span class="kanji-decomposition" lang="ja">${entry.radical_decomposition.map(esc).join(' + ')}</span>
            </p>
          ` : ''}
          ${renderMnemonicBlock(entry.mnemonic)}
        </section>
      ` : ''}
      ${entry.confusable_with?.length ? `
        <section class="kanji-confusable-block">
          <h3>Don't confuse with</h3>
          <div class="kanji-confusable-grid">
            ${entry.confusable_with.map(g => `
              <a class="kanji-confusable-card" href="#/kanji/${encodeURIComponent(g)}">
                <span lang="ja">${esc(g)}</span>
              </a>
            `).join('')}
          </div>
        </section>
      ` : ''}
      ${entry.examples?.length ? `
        <section class="kanji-examples">
          <h3>Example usage (N5)</h3>
          <table class="kanji-examples-table">
            <tbody>
              ${entry.examples.map(ex => `
                <tr>
                  <td class="ex-form" lang="ja">${esc(ex.form)}</td>
                  <td class="ex-reading" lang="ja">${esc(ex.reading || '')}</td>
                  <td class="ex-gloss">${esc(ex.gloss || '')}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </section>
      ` : ''}
      ${entry.sentences?.length ? `
        <section class="kanji-sentences">
          <h3>In a sentence</h3>
          <ul class="kanji-sentences-list">
            ${entry.sentences.map(s => `
              <li>
                <p class="kanji-sentence-ja" lang="ja">${esc(s.ja)}</p>
                ${s.translation_en ? `<p class="kanji-sentence-en muted small">${esc(s.translation_en)}</p>` : ''}
              </li>
            `).join('')}
          </ul>
        </section>
      ` : ''}
      ${entry.stroke_order_svg ? `
        <section class="kanji-stroke">
          <h3>Stroke order</h3>
          <object class="stroke-svg" data="${esc(entry.stroke_order_svg)}" type="image/svg+xml" aria-label="Stroke order for ${esc(entry.glyph)}">
            <p class="muted small">Stroke-order diagram could not load.</p>
          </object>
          <p class="muted small kanji-stroke-credit">Stroke data: <a href="https://kanjivg.tagaini.net/" rel="noopener noreferrer" target="_blank">KanjiVG</a> (CC BY-SA 3.0).</p>
        </section>
      ` : ''}
      ${entry.stroke_order_mistakes ? `
        <!-- JCE-7 (round-9 follow-up, 2026-05-08): classroom-trap notes
             on stroke order, authored by the resident JA-teacher
             persona. Surfaces below the SVG so a learner reading the
             diagram has the trap context inline. -->
        <section class="kanji-stroke-mistakes">
          <h3>Common stroke-order traps</h3>
          <p class="kanji-stroke-mistake-note" lang="ja">${esc(entry.stroke_order_mistakes)}</p>
        </section>
      ` : ''}
      <nav class="kanji-nav">
        ${prev ? `<a href="#/kanji/${encodeURIComponent(prev.glyph)}">← <span lang="ja">${esc(prev.glyph)}</span></a>` : '<span></span>'}
        ${next ? `<a href="#/kanji/${encodeURIComponent(next.glyph)}"><span lang="ja">${esc(next.glyph)}</span> →</a>` : '<span></span>'}
      </nav>
    </article>
  `;
  // Wire Mark-as-known toggle (parity with renderPatternDetail + vocab). OPEN-10.
  document.getElementById('mark-known-kanji')?.addEventListener('change', (ev) => {
    storage.setKanjiKnown(entry.glyph, ev.target.checked);
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

// IMP-125 (richness audit, 2026-05-10): WaniKani-style 3-mnemonic
// renderer. Backwards-compatible: accepts either the new
// {summary, visual, reading, meaning, provenance} object or the
// legacy flat string and renders accordingly.
function renderMnemonicBlock(mn) {
  if (!mn) return '';
  if (typeof mn === 'string') {
    // Legacy flat-string path; preserve previous render exactly.
    return `<p class="kanji-mnemonic">${esc(mn)}</p>`;
  }
  if (typeof mn !== 'object') return '';

  const summary = mn.summary || mn.meaning || '';
  const visual = mn.visual || '';
  const reading = mn.reading || '';
  const prov = mn.provenance || {};

  const provBadge = (key) => {
    const p = prov[key];
    if (p === 'auto_derived') {
      return ' <span class="kanji-mnemonic-prov muted small" title="Auto-derived stub; pending native review.">auto</span>';
    }
    return '';
  };

  const lines = [];
  if (summary) {
    lines.push(`<p class="kanji-mnemonic kanji-mnemonic-summary"><strong>Meaning:</strong> ${esc(summary)}${provBadge('summary')}</p>`);
  }
  if (visual && visual !== summary) {
    lines.push(`<p class="kanji-mnemonic kanji-mnemonic-visual"><strong>Visual:</strong> ${esc(visual)}${provBadge('visual')}</p>`);
  }
  if (reading) {
    lines.push(`<p class="kanji-mnemonic kanji-mnemonic-reading"><strong>Reading:</strong> ${esc(reading)}${provBadge('reading')}</p>`);
  }
  return lines.join('\n          ');
}
