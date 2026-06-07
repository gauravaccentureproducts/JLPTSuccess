// Single-kanji detail page (Brief 2 §14.1).
// Routed via #/kanji/<glyph> - shows glyph, on/kun-yomi, meanings,
// stroke-order SVG slot, and a "back to list" link.
// The stroke-order SVG path lives in data/kanji.json under stroke_order_svg;
// the SVG file itself ships separately (KanjiVG drop-in target).
import * as storage from './storage.js';
import { currentLocale, t } from './i18n.js';
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
  // Search / stroke-lesson filters / sort card removed (user request
  // 2026-06-08): the index now shows every N5 kanji in lesson order as a
  // simple grid. List tiles show only the glyph for active-recall practice;
  // readings + meanings appear on the detail page after click-through.
  const sorted = entries.slice()
    .sort((a, b) => (a.lesson_order ?? 999) - (b.lesson_order ?? 999));
  const cards = sorted.map(e => `
    <a class="kanji-card" href="#/kanji/${encodeURIComponent(e.glyph)}">
      <span class="kanji-card-glyph" lang="ja">${esc(e.glyph)}</span>
    </a>
  `).join('');

  container.innerHTML = `
    <a class="back-link" href="#/learn">← Back to Learn</a>
    <h2>Kanji</h2>
    <p>${entries.length} kanji at JLPT N5 level. Tap any card for readings, meanings, and stroke order.</p>
    <div class="kanji-card-grid">${cards}</div>
  `;
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
        <a href="#/kanji">← ${esc(t('kanji_detail.all_kanji'))}</a>
        <span class="muted small">${idx + 1} ${esc(t('kanji_detail.of_total'))} ${entries.length}</span>
      </div>
      <div class="kanji-glyph-row pattern-header">
        <div class="kanji-glyph-cluster">
          <div class="kanji-glyph-big" lang="ja">${esc(entry.glyph)}</div>
          <div class="kanji-readings">
            ${entry.on?.length
                ? `<p><strong>${esc(t('kanji_detail.on'))}:</strong> <span lang="ja">${entry.on.map(esc).join(' / ')}</span></p>`
                : (Array.isArray(entry.on) ? `<p><strong>${esc(t('kanji_detail.on'))}:</strong> <span class="muted small">${esc(t('kanji_detail.none_at_n5'))}</span></p>` : '')}
            ${entry.kun?.length
                ? `<p><strong>${esc(t('kanji_detail.kun'))}:</strong> <span lang="ja">${entry.kun.map(esc).join(' / ')}</span></p>`
                : (Array.isArray(entry.kun) ? `<p><strong>${esc(t('kanji_detail.kun'))}:</strong> <span class="muted small">${esc(t('kanji_detail.none_at_n5'))}</span></p>` : '')}
            ${(() => { const m = localizedMeanings(entry); return m.length ? `<p><strong>${esc(t('kanji_detail.meaning'))}:</strong> ${m.map(esc).join(', ')} ${renderItemBadge(entry, true)}</p>` : ''; })()}
          </div>
        </div>
        <label class="known-toggle" title="Manually mark this kanji as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-kanji" ${isKnown ? 'checked' : ''}>
          <span>${esc(t('kanji_detail.mark_as_known'))}</span>
        </label>
      </div>
      ${(entry.radical || entry.radical_decomposition || entry.mnemonic) ? `
        <section class="kanji-mnemonic-block">
          <h3>${esc(t('kanji_detail.radical_and_mnemonic'))}</h3>
          ${entry.radical ? `
            <p><strong>${esc(t('kanji_detail.radical'))}:</strong>
              <span class="kanji-radical-glyph" lang="ja">${esc(entry.radical.glyph || '')}</span>
              <span class="muted small">${esc(entry.radical.name || '')}</span>
            </p>
          ` : ''}
          ${entry.radical_decomposition?.length ? `
            <p><strong>${esc(t('kanji_detail.components'))}:</strong>
              <span class="kanji-decomposition" lang="ja">${entry.radical_decomposition.map(esc).join(' + ')}</span>
            </p>
          ` : ''}
          ${renderMnemonicBlock(entry.mnemonic)}
          ${entry.mnemonic_image ? `
            <!-- Mnemonic illustration (decorative memory-aid card). The
                 authoritative readings/meaning stay as the live HTML above;
                 the image is supplementary. alt text + lazy-load required. -->
            <figure class="kanji-mnemonic-figure">
              <img class="kanji-mnemonic-img" src="${esc(entry.mnemonic_image)}"
                   loading="lazy" decoding="async"
                   alt="${esc(entry.mnemonic_image_alt || ('Memory-aid illustration for the kanji ' + (entry.glyph || '')))}">
            </figure>
          ` : ''}
          ${entry.etymology ? `
            <!-- IMP-WAVE-P2-13 (UI audit fix, 2026-05-11): historical /
                 pictographic origin of the kanji. Schema:
                 {origin_type, story, related_modern}. -->
            <div class="kanji-etymology">
              <p><strong>Etymology:</strong>
                <span class="kanji-etymology-type muted small">(${esc(entry.etymology.origin_type || 'origin')})</span>
                ${esc(entry.etymology.story || '')}
              </p>
              ${entry.etymology.related_modern ? `
                <p class="muted small">${esc(entry.etymology.related_modern)}</p>
              ` : ''}
            </div>
          ` : ''}
        </section>
      ` : ''}
      ${entry.confusable_with?.length ? `
        <section class="kanji-confusable-block">
          <h3>${esc(t('kanji_detail.dont_confuse'))}</h3>
          <div class="kanji-confusable-grid">
            ${entry.confusable_with.map(g => `
              <a class="kanji-confusable-card" href="#/kanji/${encodeURIComponent(g)}">
                <span lang="ja">${esc(g)}</span>
              </a>
            `).join('')}
          </div>
        </section>
      ` : ''}
      ${(() => {
        // Merged "Example usage" + "Words containing this kanji" (user request
        // 2026-06-08): the two overlapped, so they are now ONE section listing
        // the N5 words that use this kanji, clickable through to the vocab entry
        // when one exists. Built from examples[] (richer compounds, pedagogical
        // order) unioned with n5_compounds[] (vocab-linked), deduped by form, and
        // EXCLUDING kana-only homophones (e.g. あめ "candy" does not contain 雨)
        // so the heading stays truthful.
        const glyph = entry.glyph || '';
        const compounds = entry.n5_compounds || [];
        const linkForms = new Set(compounds.filter(c => c.form).map(c => c.form));
        const seen = new Set();
        const rows = [];
        for (const it of [...(entry.examples || []), ...compounds]) {
          const form = it.form || '';
          if (!form || !form.includes(glyph)) continue;   // drop kana homophones
          if (seen.has(form)) continue;
          seen.add(form);
          rows.push({ form, reading: it.reading || '', gloss: it.gloss || '', link: linkForms.has(form) });
        }
        if (!rows.length) return '';
        const body = rows.map(r => {
          const formCell = r.link
            ? `<a href="#/learn/vocab/${encodeURIComponent(r.form)}" lang="ja">${esc(r.form)}</a>`
            : `<span lang="ja">${esc(r.form)}</span>`;
          return `
                <tr>
                  <td class="ex-form">${formCell}</td>
                  <td class="ex-reading" lang="ja">${esc(r.reading)}</td>
                  <td class="ex-gloss">${esc(r.gloss)}</td>
                </tr>`;
        }).join('');
        return `
        <section class="kanji-examples">
          <h3>${esc(t('kanji_detail.example_usage'))}</h3>
          <p class="muted small">N5 words that use this kanji. Click a linked row to open its vocab entry.</p>
          <table class="kanji-examples-table">
            <tbody>${body}</tbody>
          </table>
        </section>`;
      })()}
      ${entry.sentences?.length ? `
        <section class="kanji-sentences">
          <h3>${esc(t('kanji_detail.in_a_sentence'))}</h3>
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
      ${entry.authentic_refs?.length ? `
        <!-- IMP-WAVE-AUTHENTIC-XLINK (2026-05-11): real-world
             cards where this kanji appears on actual JP signs,
             menus, transit boards, etc. The /authentic page
             hosts the source cards. -->
        <section class="kanji-authentic-refs">
          <h3>Seen in the real world</h3>
          <p class="muted small">
            This kanji appears on these authentic Japanese cards. Click to see the original sign / menu / notice in context.
          </p>
          <ul class="authentic-ref-list">
            ${entry.authentic_refs.map(cid => {
              const cat = (cid.split('.')[1] || 'authentic');
              return `<li><a href="#/authentic">${esc(cid)}</a> <span class="muted small">(${esc(cat)})</span></li>`;
            }).join('')}
          </ul>
        </section>
      ` : ''}
      ${entry.stroke_order_svg ? `
        <section class="kanji-stroke">
          <h3>${esc(t('kanji_detail.stroke_order'))}</h3>
          <object class="stroke-svg" data="${esc(entry.stroke_order_svg)}" type="image/svg+xml" aria-label="Stroke order for ${esc(entry.glyph)}">
            <p class="muted small">${esc(t('kanji_detail.stroke_diagram_fail'))}</p>
          </object>
          <p class="muted small kanji-stroke-credit">${esc(t('kanji_detail.stroke_order_credit'))}: <a href="https://kanjivg.tagaini.net/" rel="noopener noreferrer" target="_blank">KanjiVG</a> (CC BY-SA 3.0).</p>
        </section>
      ` : ''}
      ${entry.stroke_order_mistakes ? `
        <!-- JCE-7 (round-9 follow-up, 2026-05-08): classroom-trap notes
             on stroke order, authored by the resident JA-teacher
             persona. Surfaces below the SVG so a learner reading the
             diagram has the trap context inline. -->
        <section class="kanji-stroke-mistakes">
          <h3>${esc(t('kanji_detail.stroke_order_traps'))}</h3>
          <p class="kanji-stroke-mistake-note" lang="ja">${esc(entry.stroke_order_mistakes)}</p>
        </section>
      ` : ''}
      ${(() => {
        const trap = entry.stroke_order_trap;
        if (!trap || typeof trap !== 'object') return '';
        return `
          <section class="kanji-stroke-trap">
            <h3>${esc(t('kanji_detail.stroke_order_trap_section'))}</h3>
            ${trap.trap ? `<p><strong>${esc(t('kanji_detail.what_learners_get_wrong'))}:</strong> ${esc(trap.trap)}</p>` : ''}
            ${trap.correct_order_summary ? `<p><strong>${esc(t('kanji_detail.correct_order'))}:</strong> ${esc(trap.correct_order_summary)}</p>` : ''}
            ${trap.why_it_matters ? `<p><strong>${esc(t('kanji_detail.why_it_matters'))}:</strong> ${esc(trap.why_it_matters)}</p>` : ''}
          </section>
        `;
      })()}
      ${(() => {
        const drill = entry.on_kun_pair_drill;
        if (!drill || typeof drill !== 'object') return '';
        const sa = drill.standalone || {};
        const cp = drill.compound || {};
        return `
          <section class="kanji-on-kun-drill">
            <h3>${esc(t('kanji_detail.on_kun_pair_drill'))}</h3>
            <table class="on-kun-drill-table">
              <thead>
                <tr><th>${esc(t('kanji_detail.standalone_typically_kun'))}</th><th>${esc(t('kanji_detail.compound_typically_on'))}</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <span class="form" lang="ja">${esc(sa.form || '')}</span>
                    <span class="reading muted small" lang="ja">${esc(sa.reading || '')}</span>
                    <span class="gloss">${esc(sa.gloss || '')}</span>
                  </td>
                  <td>
                    <span class="form" lang="ja">${esc(cp.form || '')}</span>
                    <span class="reading muted small" lang="ja">${esc(cp.reading || '')}</span>
                    <span class="gloss">${esc(cp.gloss || '')}</span>
                  </td>
                </tr>
              </tbody>
            </table>
            ${drill.contrast_note ? `<p class="contrast-note">${esc(drill.contrast_note)}</p>` : ''}
          </section>
        `;
      })()}
      ${entry.reading_rule ? `
        <section class="kanji-reading-rule">
          <h3>${esc(t('kanji_detail.reading_rule_of_thumb'))}</h3>
          <p class="muted small">${esc(entry.reading_rule)}</p>
        </section>
      ` : ''}
      ${(() => {
        const oc = Array.isArray(entry.okurigana_cuts) ? entry.okurigana_cuts : [];
        if (!oc.length) return '';
        return `
          <section class="kanji-okurigana-cuts">
            <h3>${esc(t('kanji_detail.okurigana_boundary'))}</h3>
            <p class="muted small">${esc(t('kanji_detail.okurigana_intro'))}</p>
            <ul class="okurigana-cuts-list">
              ${oc.map(cut => {
                // cut format: "<kanji>:<okurigana>" e.g. "食:べる"
                const parts = String(cut).split(':');
                if (parts.length !== 2) {
                  return `<li><span lang="ja">${esc(cut)}</span></li>`;
                }
                return `<li>
                  <span class="okurigana-kanji" lang="ja">${esc(parts[0])}</span><span class="okurigana-cut" aria-hidden="true">︱</span><span class="okurigana-suffix" lang="ja">${esc(parts[1])}</span>
                </li>`;
              }).join('')}
            </ul>
          </section>
        `;
      })()}
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

  // Owner decision (2026-06-08): review/provenance status (e.g. an "auto /
  // pending native review" tag) is internal and must never surface to the
  // learner. Badge suppressed; the mnemonic text itself is shown as-is.
  const provBadge = (_key) => '';

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
