// Vocabulary half of Chapter 1 - Learn (split out from learn.js per IMP-022,
// audit 2026-05-04 round 2). Owns the vocab list page and the per-word
// detail page. Loaded lazily by `renderLearn` in learn.js when the user
// navigates to a vocab route.
import { renderJa } from './furigana.js';
import * as storage from './storage.js';
import { esc, wireExpandCollapseControls } from './learn.js';
import { currentLocale } from './i18n.js';
import { renderItemBadge } from './provenance-badge.js';

// IMP-046 (audit round-5): pick locale-aware vocab gloss when present,
// else fall back to English. The translated subset (~120 entries) carries
// `gloss_vi/_id/_ne/_zh`; remaining entries fall through to `gloss`.
function localizedGloss(entry) {
  const lc = currentLocale();
  if (lc && lc !== 'en') {
    const localized = entry[`gloss_${lc}`];
    if (typeof localized === 'string' && localized.trim()) return localized;
  }
  return entry.gloss || '';
}

// Render-time mapping: 40 fine-grained vocab sections -> 6 super-sections.
// Same pattern as GRAMMAR_SUPERCATS in learn-grammar.js. Data file unchanged.
const VOCAB_SUPERSECTS = [
  ['People and Body', [
    '1. People - Pronouns and Self', '2. People - Family',
    '3. People - Roles', '4. Body Parts',
  ]],
  ['Demonstratives, Questions, Numbers, Time', [
    '5. Demonstratives', '6. Question Words', '7. Numbers',
    '8. Native Counters (つ-series)', '9. Counters (Common)',
    '10. Time - General', '11. Time - Days, Weeks, Months, Years',
    '12. Time - Frequency / Sequence',
  ]],
  ['Places and Things', [
    '13. Locations and Places (general)', '14. Nature and Weather',
    '15. Animals', '16. Food and Drink - General', '17. Food - Items',
    '18. Drinks', '19. Tableware and Cooking', '20. Colors',
    '21. Clothing and Accessories', '22. Money and Shopping',
    '23. Transport', '24. School and Study',
    '25. Languages and Countries', '26. House and Furniture',
  ]],
  ['Verbs', [
    '27. Verbs - Group 1 (う-verbs)', '28. Verbs - Group 2 (る-verbs)',
    '29. Verbs - Irregular and する-verbs', '30. Verbs - Existence and Possession',
  ]],
  ['Adjectives and Function Words', [
    '31. い-Adjectives', '32. な-Adjectives', '33. Adverbs',
    '34. Conjunctions', '35. Particles (functional vocabulary)',
    '36. Greetings and Set Phrases',
  ]],
  ['Misc', [
    '37. Common Nouns - Miscellaneous', '38. Sounds and Voice',
    '39. Function / Filler Expressions', '40. Misc Useful Items',
  ]],
];

function vocabSuperSectionFor(section) {
  for (const [supersect, members] of VOCAB_SUPERSECTS) {
    if (members.includes(section)) return supersect;
  }
  return 'Misc';  // safe fallback
}

// Flatten the vocab corpus into the same order the list page presents it:
//   super-section declaration order, then ascending section-number,
//   then form-alphabetical within each section.
// Used by BOTH renderVocabularyList (to render) and renderVocabularyDetail
// (to compute prev/next) so the detail-page ←/→ navigation matches the
// order the user sees on the list page. Without this shared source of
// truth the two pages disagree at section boundaries.
function buildOrderedVocabList(entries) {
  const bySuper = new Map();
  for (const [s] of VOCAB_SUPERSECTS) bySuper.set(s, []);
  for (const e of entries) {
    const sup = vocabSuperSectionFor(e.section || 'Other');
    bySuper.get(sup).push(e);
  }
  const flat = [];
  for (const [, items] of bySuper.entries()) {
    items.sort((a, b) => {
      const na = parseInt(a.section || '', 10);
      const nb = parseInt(b.section || '', 10);
      if (!isNaN(na) && !isNaN(nb) && na !== nb) return na - nb;
      return (a.form || '').localeCompare(b.form || '');
    });
    flat.push(...items);
  }
  return flat;
}

// IMP-029 (audit round 2): vocab list filter state.
let _vocabFilterText = '';

function _matchVocab(v, q) {
  if (!q) return true;
  const hay = [
    v.form || '', v.reading || '', v.gloss || '', v.section || '',
  ].join(' ').toLowerCase();
  return hay.includes(q);
}

export function renderVocabularyList(container, data) {
  const entries = data.entries || [];
  const q = _vocabFilterText.trim().toLowerCase();
  const ordered = buildOrderedVocabList(entries);
  const filtered = ordered.filter(e => _matchVocab(e, q));
  const bySuper = new Map();
  for (const [s] of VOCAB_SUPERSECTS) bySuper.set(s, []);
  for (const e of filtered) {
    const sup = vocabSuperSectionFor(e.section || 'Other');
    bySuper.get(sup).push(e);
  }
  const slugify = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  const isFiltered = q.length > 0;
  // IMP-071 (audit round-6): per-section translation-coverage badge
  // when on a non-EN locale. Counts how many of the section's items
  // have a populated `gloss_<lc>` field. Helps reviewers focus their
  // translation effort + signals to learners which sections are
  // covered. Hidden on EN (no translation concept).
  const lc = currentLocale();
  const showCoverage = (lc && lc !== 'en');
  const coverageOf = (items) => {
    if (!showCoverage) return '';
    const total = items.length;
    if (total === 0) return '';
    const covered = items.filter(v =>
      typeof v[`gloss_${lc}`] === 'string' && v[`gloss_${lc}`].trim()
    ).length;
    const pct = Math.round(100 * covered / total);
    const tone = pct >= 50 ? 'good' : pct > 0 ? 'partial' : 'none';
    return `<span class="vocab-coverage-badge tone-${tone}" title="${covered}/${total} translated">${pct}%</span>`;
  };
  const sections = [...bySuper.entries()]
    .filter(([, items]) => items.length > 0)
    .map(([sup, items]) => {
      const cards = items.map(v => `
        <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(v.form || '')}">
          <span class="vocab-form" lang="ja">${esc(v.form || '')}</span>
          ${v.reading ? `<span class="vocab-reading" lang="ja">${esc(v.reading)}</span>` : ''}
          <span class="vocab-gloss">${esc(localizedGloss(v))}</span>
        </a>
      `).join('');
      return `
        <details class="vocab-section" id="vocab-${slugify(sup)}"${isFiltered ? ' open' : ''}>
          <summary><strong>${esc(sup)}</strong> <span class="muted small">(${items.length})</span> ${coverageOf(items)}</summary>
          <div class="vocab-grid">${cards}</div>
        </details>
      `;
    }).join('');

  container.innerHTML = `
    <article class="vocab-toc">
      <a class="back-link" href="#/learn">← Back to Learn</a>
      <h2>Vocabulary</h2>
      <p class="page-lede">${entries.length} N5 words in ${VOCAB_SUPERSECTS.length} sections.</p>
      <div class="kanji-filters" role="search" aria-label="Filter vocabulary">
        <input type="search" id="vocab-filter-q" class="kanji-filter-input"
          placeholder="Search form, reading, or English (e.g. たべる / eat / 飲む)"
          value="${esc(_vocabFilterText)}" autocomplete="off" lang="ja"
          aria-label="Search vocabulary">
        <p class="kanji-filter-count muted small" aria-live="polite">
          Showing <strong>${filtered.length}</strong> of ${entries.length}.
        </p>
      </div>
      <div class="toc-controls">
        <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
        <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      </div>
      ${sections || '<div class="placeholder"><p>No words match the current filter.</p></div>'}
    </article>
  `;
  wireExpandCollapseControls(container, 'details.vocab-section');

  const inp = document.getElementById('vocab-filter-q');
  if (inp) {
    inp.addEventListener('input', () => {
      _vocabFilterText = inp.value;
      renderVocabularyList(container, data);
      const re = document.getElementById('vocab-filter-q');
      if (re) {
        re.focus();
        const v = re.value;
        re.setSelectionRange(v.length, v.length);
      }
    });
  }
}

export function renderVocabularyDetail(container, vocabData, grammarData, form) {
  const entries = vocabData.entries || [];
  const entry = entries.find(e => e.form === form);
  if (!entry) {
    container.innerHTML = `
      <article class="vocab-detail">
        <a class="back-link" href="#/learn/vocab">← Back to Vocabulary</a>
        <h2>Word not found</h2>
        <p>No vocab entry matches <strong lang="ja">${esc(form)}</strong>. The word may live under a different form.</p>
      </article>
    `;
    return;
  }
  // Pull example sentences from grammar.json. Each example carries a
  // `vocab_ids: [...]` field (populated by tools/link_grammar_examples_to_vocab.py)
  // listing exactly which vocab entries it demonstrates. We filter by ID
  // — not by substring on the form field — so homographs (e.g., かた "person"
  // vs かた "way of doing") never cross-contaminate. See JA-17 invariant.
  //
  // Backward-compat fallback: if an example has no vocab_ids field (older
  // data, or auto-tagger hasn't run), fall back to substring match.
  const seen = new Set();
  const examples = [];
  for (const p of (grammarData.patterns || [])) {
    for (const ex of (p.examples || [])) {
      if (!ex.ja || ex.ja.includes('(see ')) continue;
      if (seen.has(ex.ja)) continue;
      let matches = false;
      if (Array.isArray(ex.vocab_ids)) {
        matches = ex.vocab_ids.includes(entry.id);
      } else {
        const needles = [form];
        if (entry.reading && entry.reading !== form) needles.push(entry.reading);
        matches = needles.some(n => ex.ja.includes(n));
      }
      if (matches) {
        seen.add(ex.ja);
        examples.push({ ja: ex.ja, en: ex.translation_en, source: p.pattern });
        if (examples.length >= 24) break;
      }
    }
    if (examples.length >= 24) break;
  }
  examples.sort((a, b) => (a.ja?.length || 0) - (b.ja?.length || 0));
  const top = examples.slice(0, 5);

  // prev / next: walk the SAME canonical order the list page uses
  // (super-section → section-number → form-alpha) via the shared
  // buildOrderedVocabList helper. This guarantees the list page and
  // the detail page agree on what comes after each entry. Match by
  // `id` (unique per entry) so homographs like きる v1/v2 or はい
  // counter/expression don't collide.
  const ordered = buildOrderedVocabList(entries);
  const idx = ordered.findIndex(e => e.id === entry.id);
  const prev = idx > 0 ? ordered[idx - 1] : null;
  const next = idx >= 0 && idx < ordered.length - 1 ? ordered[idx + 1] : null;

  // Mark-as-known parity (OPEN-10): vocab detail gets the same toggle
  // affordance as grammar pattern detail, in the same header-right position.
  const isVocabKnown = storage.isVocabKnown(entry.form);
  container.innerHTML = `
    <article class="vocab-detail">
      <a class="back-link" href="#/learn/vocab">← Back to Vocabulary</a>
      <header class="vocab-header pattern-header">
        <div>
          <p class="muted small">${esc(entry.section || '')}</p>
          <h2 class="vocab-form-big" lang="ja">${esc(entry.form)}</h2>
          ${entry.reading ? `<p class="vocab-reading-big" lang="ja">${esc(entry.reading)}</p>` : ''}
          <p class="vocab-gloss-big">${esc(localizedGloss(entry))} ${renderItemBadge(entry, true)}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${isVocabKnown ? 'checked' : ''}>
          <span>Mark as known</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">Meaning</h3>
        <p><strong>${currentLocale() === 'en' ? 'English' : 'Meaning'}:</strong> ${esc(localizedGloss(entry) || '-')}</p>
        ${currentLocale() !== 'en' && entry.gloss && localizedGloss(entry) !== entry.gloss
            ? `<p><strong>English:</strong> ${esc(entry.gloss)}</p>`
            : ''}
        ${entry.reading ? `<p><strong>Japanese reading:</strong> <span lang="ja">${esc(entry.reading)}</span></p>` : ''}
      </section>

      <section>
        <h3 class="section-title">Example sentences ${top.length ? `(${top.length})` : ''}</h3>
        ${top.length ? `
          <ol class="example-list">
            ${top.map(ex => `
              <li>
                <p lang="ja" class="example-ja">${renderJa(ex.ja)}</p>
                ${ex.en ? `<p class="translation">${esc(ex.en)}</p>` : ''}
                ${ex.source ? `<p class="muted small">From pattern: <span lang="ja">${esc(ex.source)}</span></p>` : ''}
              </li>
            `).join('')}
          </ol>
        ` : `
          <p class="muted">No example sentences in the corpus yet for this word. Try the search bar to find phrases that include it.</p>
        `}
      </section>

      <nav class="vocab-nav">
        ${prev ? `<a href="#/learn/vocab/${encodeURIComponent(prev.form)}">← <span lang="ja">${esc(prev.form)}</span></a>` : '<span></span>'}
        ${next ? `<a href="#/learn/vocab/${encodeURIComponent(next.form)}"><span lang="ja">${esc(next.form)}</span> →</a>` : '<span></span>'}
      </nav>
    </article>
  `;

  document.getElementById('mark-known-vocab')?.addEventListener('change', (ev) => {
    storage.setVocabKnown(entry.form, ev.target.checked);
  });
}
