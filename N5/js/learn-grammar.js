// Grammar half of Chapter 1 - Learn (split out from learn.js per IMP-022,
// audit 2026-05-04 round 2). Owns the grammar TOC, the per-pattern detail
// page, and the supporting category map / per-pattern overrides. Loaded
// lazily by `renderLearn` in learn.js when the user navigates to a grammar
// route, so the hub doesn't pull this code on first paint.
import { renderJa } from './furigana.js';
import * as storage from './storage.js';
import { esc, wireExpandCollapseControls } from './learn.js';
import { currentLocale } from './i18n.js';

// IMP-045 (audit round-5): pick locale-aware grammar explanation when
// present (native_reviewed only - see data/grammar.json
// `_translation_status` policy), else fall back to English. The active
// per-locale field is `explanation_hi` (post-2026-05-06 IMP-096
// narrowing — earlier en/vi/id/ne/zh shell collapsed to en+hi); absence
// is the default state until reviewers fill it via docs/TRANSLATING.md.
function localizedExplanation(p) {
  const lc = currentLocale();
  if (lc && lc !== 'en') {
    const localized = p[`explanation_${lc}`];
    if (typeof localized === 'string' && localized.trim()) return localized;
  }
  return p.explanation_en || '';
}

// ISSUE-056 (audit round-7): pick locale-aware grammar meaning when
// present, else fall back to English meaning. Same pattern as
// localizedExplanation() but for the shorter `meaning_*` field.
function localizedMeaning(p) {
  const lc = currentLocale();
  if (lc && lc !== 'en') {
    const localized = p[`meaning_${lc}`];
    if (typeof localized === 'string' && localized.trim()) return localized;
  }
  return p.meaning_en || '';
}

// IMP-080 (audit round-7): L1-interference notes per locale.
// When the current locale matches an l1_notes key, return the note;
// else return null (renderer hides the section).
function localizedL1Note(p) {
  const lc = currentLocale();
  if (lc && lc !== 'en' && p.l1_notes && typeof p.l1_notes === 'object') {
    const note = p.l1_notes[lc];
    if (typeof note === 'string' && note.trim()) return note;
  }
  return null;
}

// Render-time mapping: 32 fine-grained categories in data/grammar.json
// to 5 pedagogically-coherent super-categories. Every fine category is
// explicitly mapped (no fallback needed).
const GRAMMAR_SUPERCATS = [
  ['Sentence Basics', [
    'Copula and Basic Sentence Structure',
    'Particles',
    'Demonstratives',
    'Question Words',
  ]],
  ['Verbs', [
    'Verbs - Tense and Politeness (ます-form)',
    'Verbs - Plain (Dictionary) Form and Negation',
    'Te-form and Related Patterns',
    'Existence and Possession',
    'Desiderative and Volitional',
    'Giving and Receiving (basic)',
    // Verb-modal patterns moved here from the old catchall bucket.
    'Additional Upper N5 / Borderline Patterns - Permission and Obligation',
    'Additional Upper N5 / Borderline Patterns - Experience and Advice',
    'Additional Upper N5 / Borderline Patterns - Compound and Listed Actions',
    'Additional Upper N5 / Borderline Patterns - Excess',
    'Additional Upper N5 / Borderline Patterns - Intention',
    'Additional Upper N5 / Borderline Patterns - Way of Doing',
    'Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)',
  ]],
  ['Adjectives and Comparison', [
    'Adjectives',
    'Comparison and Preference',
  ]],
  ['Time, Counters, Connectives', [
    'Counters and Quantity',
    'Time Expressions',
    'Conjunctions and Connectives',
    'Asking and Stating with から / ので (basic causation)',
    'Existence-of-Plans and Frequency',
  ]],
  ['Set Phrases and Discourse', [
    'Nominalization and Modification',
    'Common Set Patterns',
    'Functional Expressions (Non-Grammar, Common Usage)',
    'Other Core Patterns',
    'Honorific / Polite Vocabulary at N5 (functional)',
    'Additional Upper N5 / Borderline Patterns - Explanation and Emphasis',
    'Additional Upper N5 / Borderline Patterns - Quotation (Casual)',
    'Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation',
  ]],
];

// Per-pattern overrides for cases where the fine-grained `category` value
// doesn't match the pattern's true type. These are individual patterns
// that live inside a non-verb subcategory but are actually verb patterns
// (verb relative clauses, verb-stem constructions, ています/ました with
// time markers, etc.). Moved to "Verbs" to remove the cross-bucket
// duplication the user flagged 2026-05-01.
const PATTERN_SUPERCAT_OVERRIDES = {
  'n5-135': 'Verbs',  // Verb (plain) + Noun - relative clauses
  'n5-144': 'Verbs',  // Verb-stem + ながら - while doing
  'n5-153': 'Verbs',  // まだ + Verb-ていません - not yet
  'n5-154': 'Verbs',  // もう + Verb-ました - already
  'n5-162': 'Verbs',  // Verb-plain ましょう (see 〜ます)
  'n5-163': 'Verbs',  // Verb-た あとで (see 〜あと)
};

function superCategoryFor(pattern) {
  if (typeof pattern === 'object' && pattern && pattern.id in PATTERN_SUPERCAT_OVERRIDES) {
    return PATTERN_SUPERCAT_OVERRIDES[pattern.id];
  }
  const category = (typeof pattern === 'string') ? pattern : (pattern?.category || '');
  for (const [supercat, members] of GRAMMAR_SUPERCATS) {
    if (members.includes(category)) return supercat;
  }
  // Should never fire on the current 32 categories (all explicitly mapped).
  return 'Set Phrases and Discourse';
}

// Flatten patterns into the same order the TOC presents them: super-category
// declaration order, sorted by patternOrder within each group. Used by the
// detail-page prev/next nav so navigation matches the user's mental model
// (the order they see when browsing the grammar list).
export function buildOrderedPatternList(allPatterns) {
  const bySuperCat = new Map();
  for (const [supercat] of GRAMMAR_SUPERCATS) bySuperCat.set(supercat, []);
  for (const pat of allPatterns) {
    const sc = superCategoryFor(pat);
    if (bySuperCat.has(sc)) bySuperCat.get(sc).push(pat);
  }
  const flat = [];
  for (const [, items] of bySuperCat) {
    items.sort((a, b) => (a.patternOrder ?? 0) - (b.patternOrder ?? 0));
    flat.push(...items);
  }
  return flat;
}

// IMP-029 (audit round 2): grammar list filter state. Module-local so the
// search query and tier persist while the user navigates within the index
// but reset on a fresh page load.
let _grammarFilterText = '';
let _grammarFilterTier = 'all';   // 'all' | 'core_n5' | 'late_n5'

function _matchGrammar(p, q, tier) {
  if (tier !== 'all' && (p.tier || 'core_n5') !== tier) return false;
  if (!q) return true;
  const hay = [
    p.pattern, p.meaning_en, p.meaning_ja || '',
    p.notes || '', (p.examples || []).map(e => e.ja).join(' '),
  ].join(' ').toLowerCase();
  return hay.includes(q);
}

export function renderGrammarTOC(container, data) {
  // Group by super-category instead of fine-grained category.
  const bySuperCat = new Map();
  for (const [supercat] of GRAMMAR_SUPERCATS) bySuperCat.set(supercat, []);

  const q = _grammarFilterText.trim().toLowerCase();
  const filtered = data.patterns.filter(p => _matchGrammar(p, q, _grammarFilterTier));
  for (const p of filtered) {
    const sc = superCategoryFor(p);
    bySuperCat.get(sc).push(p);
  }

  const slugify = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const chip = (group, value, label, active) =>
    `<button type="button" class="kanji-chip ${active ? 'active' : ''}"
       data-grammar-filter-group="${group}" data-grammar-filter-value="${value}">${esc(label)}</button>`;

  let html = `
    <a class="back-link" href="#/learn">← Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${data.patterns.length} patterns in ${bySuperCat.size} sections.</p>
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. て-form / wants to / です)"
        value="${esc(_grammarFilterText)}" autocomplete="off"
        aria-label="Search grammar patterns">
      <div class="kanji-filter-row" aria-label="Tier filter">
        <span class="kanji-filter-label">Tier:</span>
        ${chip('tier', 'all', 'All', _grammarFilterTier === 'all')}
        ${chip('tier', 'core_n5', 'Core N5', _grammarFilterTier === 'core_n5')}
        ${chip('tier', 'late_n5', 'Late N5', _grammarFilterTier === 'late_n5')}
      </div>
      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${filtered.length}</strong> of ${data.patterns.length}.
      </p>
    </div>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
      <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      <!-- IMP-143 (richness audit, 2026-05-09): print-as-PDF cheat
           sheet for the entire grammar list. Auto-expands all sections,
           triggers window.print(), then restores prior state. The print
           stylesheet reveals .grammar-card-print-* spans for a dense
           one-row-per-pattern reference layout. -->
      <button type="button" class="btn-secondary toc-print-cheatsheet">
        🖨 Print cheat sheet
      </button>
    </div>
  `;
  for (const [supercat, items] of bySuperCat) {
    if (items.length === 0) continue;
    items.sort((a, b) => (a.patternOrder ?? 0) - (b.patternOrder ?? 0));
    const isFiltered = q || _grammarFilterTier !== 'all';
    html += `<details class="toc-category" id="cat-${slugify(supercat)}"${isFiltered ? ' open' : ''}>`;
    html += `<summary><h3>${esc(supercat)} <span class="cat-count muted small">(${items.length})</span></h3></summary>`;
    html += `<div class="grammar-grid">`;
    for (const p of items) {
      // IMP-143 (richness audit, 2026-05-09): inline meaning_en +
      // first-example + Genki lesson tag in hidden print-only spans.
      // The print stylesheet reveals them so the rendered list view
      // becomes a printable cheat sheet (one row per pattern).
      const firstExample = (() => {
        const exs = (p.examples || []).filter(e => e && e.ja);
        return exs[0] ? exs[0].ja : '';
      })();
      const lessonTag = p.genki_lesson
        ? `G${p.genki_lesson.book}·L${p.genki_lesson.lesson}`
        : '';
      html += `
        <a class="grammar-card" href="#/learn/${encodeURIComponent(p.id)}">
          <span class="grammar-pattern" lang="ja">${esc(p.pattern)}</span>
          <span class="grammar-card-print-meaning">${esc(p.meaning_en || '')}</span>
          <span class="grammar-card-print-example" lang="ja">${esc(firstExample)}</span>
          ${lessonTag ? `<span class="grammar-card-print-lesson">${esc(lessonTag)}</span>` : ''}
        </a>
      `;
    }
    html += `</div></details>`;
  }
  if (filtered.length === 0) {
    html += `<div class="placeholder"><p>No patterns match the current filter.</p></div>`;
  } else if (data.patterns.length === 1) {
    html += `<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>`;
  }
  container.innerHTML = html;
  wireExpandCollapseControls(container, 'details.toc-category');

  // IMP-143: wire the cheat-sheet print button. Force-expand every
  // <details> so the printed output shows all categories, then trigger
  // window.print() and restore the prior open/closed state on
  // afterprint so the on-screen TOC isn't disrupted.
  container.querySelector('.toc-print-cheatsheet')?.addEventListener('click', () => {
    const detailsEls = Array.from(container.querySelectorAll('details.toc-category'));
    const priorOpen = detailsEls.map(d => d.open);
    detailsEls.forEach(d => { d.open = true; });
    document.body.classList.add('is-printing-cheatsheet');
    const restore = () => {
      detailsEls.forEach((d, i) => { d.open = priorOpen[i]; });
      document.body.classList.remove('is-printing-cheatsheet');
      window.removeEventListener('afterprint', restore);
    };
    window.addEventListener('afterprint', restore);
    window.print();
  });

  const inp = document.getElementById('grammar-filter-q');
  if (inp) {
    inp.addEventListener('input', () => {
      _grammarFilterText = inp.value;
      renderGrammarTOC(container, data);
      const re = document.getElementById('grammar-filter-q');
      if (re) {
        re.focus();
        const v = re.value;
        re.setSelectionRange(v.length, v.length);
      }
    });
  }
  container.querySelectorAll('[data-grammar-filter-group]').forEach(btn => {
    btn.addEventListener('click', () => {
      const g = btn.dataset.grammarFilterGroup;
      const v = btn.dataset.grammarFilterValue;
      if (g === 'tier') _grammarFilterTier = v;
      renderGrammarTOC(container, data);
    });
  });
}

// Friendly labels for the raw `form_rules.attaches_to` category strings.
// When a key isn't in this map, we humanize it on the fly (snake_case →
// "Snake case"). The mapping covers all 35 keys present in grammar.json
// as of 2026-05-02.
const ATTACHES_TO_LABEL = {
  'noun':                    'Noun',
  'noun_subject':            'Noun (subject)',
  'noun_location':           'Noun (location)',
  'noun_time':               'Noun (time)',
  'noun_quantity':           'Noun (quantity)',
  'noun_or_adj':             'Noun or adjective',
  'na_adjective':            'な-adjective',
  'i_adjective':             'い-adjective',
  'verb':                    'Verb',
  'verb_stem':               'Verb stem (ます-base)',
  'verb_stem_i':             'Verb i-stem',
  'verb_root':               'Verb root',
  'verb_dictionary':         'Verb (dictionary form)',
  'verb_plain':              'Verb (plain form)',
  'verb_te':                 'Verb (て-form)',
  'verb_ta':                 'Verb (た-form)',
  'verb_nai':                'Verb (ない-form)',
  'verb_mashita':            'Verb (ました form)',
  'verb_te_imasu_neg':       'Verb (て-いません)',
  'verb_or_adj_stem':        'Verb or adjective stem',
  'pronoun':                 'Pronoun',
  'question_word':           'Question word',
  'before_noun':             'Before a noun',
  'adverbial':               'Adverbial position',
  'sentence_end':            'Sentence end',
  'sentence_pattern':        'Full sentence',
  'clause':                  'Clause',
  'clause_start':            'Clause-initial',
  'clause_end':              'Clause-final',
  'plain_clause':            'Plain-form clause',
  'plain_or_polite_clause':  'Plain or polite clause',
  'quoted_clause':           'Quoted clause',
  'quantity':                'Quantity expression',
  'number':                  'Number',
  'set_phrase':              'Set phrase',
  'standalone':              'Standalone',
  'dialogue':                'Dialogue line',
  'after_name':              'After a name',
};

function attachesLabel(key) {
  if (ATTACHES_TO_LABEL[key]) return ATTACHES_TO_LABEL[key];
  return String(key)
    .replace(/_/g, ' ')
    .replace(/^./, c => c.toUpperCase());
}

// Build the "How to use / 使い方" table. Two layouts depending on the
// pattern's form-shape:
//   (A) Uniform pattern - same surface form attaches to every entry in
//       `attaches_to` (typical: ～だろう, ～ながら, etc.). Render rows of
//       attach-points on the left and one merged cell on the right
//       carrying the literal pattern.
//   (B) Conjugating pattern - `conjugations` lists multiple forms with
//       distinct examples (typical: 〜です／〜ます, ーは, etc.). The
//       attach-point table at top still shows the rowspan layout for
//       quick scanning; a secondary "Forms" table underneath shows the
//       conjugation labels + examples.
function renderHowToUseTable(p) {
  const attaches = p.form_rules?.attaches_to ?? [];
  const conjugations = p.form_rules?.conjugations ?? [];
  if (!attaches.length && !conjugations.length) return '';

  const usageHeader = `
    <div class="pattern-usage-header">
      <h3 class="section-title">How to use</h3>
      <span class="pattern-usage-chip" lang="ja">使い方</span>
    </div>
  `;

  const topTable = attaches.length ? `
    <table class="pattern-usage-table" aria-label="Attach points for ${esc(p.pattern)}">
      <tbody>
        ${attaches.map((a, i) => `
          <tr>
            <td class="pattern-usage-pos">${esc(attachesLabel(a))}</td>
            ${i === 0
              ? `<td class="pattern-usage-form" rowspan="${attaches.length}" lang="ja">${renderJa(p.pattern)}</td>`
              : ''}
          </tr>
        `).join('')}
      </tbody>
    </table>
  ` : '';

  const conjTable = conjugations.length >= 2 ? `
    <table class="pattern-conjugation-table" aria-label="Conjugation forms">
      <thead>
        <tr><th scope="col">Form</th><th scope="col">Example</th></tr>
      </thead>
      <tbody>
        ${conjugations.map(c => `
          <tr>
            <td>${esc(c.label || c.form)}</td>
            <td lang="ja">${renderJa(c.example)}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  ` : '';

  return `<section class="pattern-usage">${usageHeader}${topTable}${conjTable}</section>`;
}

export function renderGrammarPatternDetail(container, p, allPatterns) {
  const conj = p.form_rules?.conjugations ?? [];
  const examples = p.examples ?? [];
  const mistakes = p.common_mistakes ?? [];
  const entry = storage.getPatternEntry(p.id);
  const isKnown = !!entry?.isManuallyKnown;
  const isMastered = !!entry?.isMastered;
  const isWeak = !!entry?.isWeak && !isMastered;

  // Prev / next pattern in TOC order. allPatterns may be undefined if a future
  // caller forgets to thread it through - degrade gracefully (no nav row).
  const ordered = Array.isArray(allPatterns) ? buildOrderedPatternList(allPatterns) : [];
  const idx = ordered.findIndex(x => x.id === p.id);
  const prev = idx > 0 ? ordered[idx - 1] : null;
  const next = idx >= 0 && idx < ordered.length - 1 ? ordered[idx + 1] : null;
  const navHtml = (prev || next) ? `
    <div class="pattern-nav">
      ${prev
        ? `<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(prev.id)}" title="Previous: ${esc(prev.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${esc(prev.pattern)}</span></a>`
        : `<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>`}
      ${next
        ? `<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(next.id)}" title="Next: ${esc(next.pattern)}"><span class="pattern-nav-name" lang="ja">${esc(next.pattern)}</span> &rarr;</a>`
        : `<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>`}
    </div>
  ` : '';

  const exampleItems = examples.map((ex, i) => {
    const skipAudio = !ex.ja || ex.ja.includes('(see ');
    const audioPath = skipAudio ? null : `audio/grammar/${p.id}.${i}.mp3`;
    return `
    <li>
      <span class="form-tag">${esc(ex.form || '')}</span>
      ${renderJa(ex.ja, ex.furigana)}
      ${ex.translation_en ? `<span class="translation">${esc(ex.translation_en)}</span>` : ''}
      ${audioPath ? `<audio class="example-audio" controls preload="none" src="${esc(audioPath)}">Audio not available.</audio>` : ''}
    </li>
  `;
  }).join('');

  const mistakeItems = mistakes.map(m => `
    <li>
      <div><span class="wrong">${renderJa(m.wrong)}</span></div>
      <div><span class="right">${renderJa(m.right)}</span></div>
      <span class="why">${esc(m.why)}</span>
    </li>
  `).join('');

  const statusBadge = isMastered
    ? `<span class="status-badge mastered">★ Mastered</span>`
    : isWeak
      ? `<span class="status-badge weak">Needs practice</span>`
      : '';

  // IMP-146 (richness audit, 2026-05-09): "Print / Save as PDF" button.
  // Browser-native print → save-as-PDF flow. The companion @media print
  // rules in css/main.css hide nav/chrome and format pattern-detail for
  // paper. No PDF library, no network round-trip, no extra dependency.
  // Effective lesson-notes export per the Genki lesson tag also added
  // in IMP-130.
  const lessonTag = (() => {
    const g = p.genki_lesson;
    if (!g) return '';
    return `<span class="pattern-lesson-tag" title="Genki ${g.book} Lesson ${g.lesson}">G${g.book}·L${g.lesson}</span>`;
  })();

  const html = `
    <article class="pattern-detail">
      ${navHtml}
      <a class="back-link no-print" href="#/learn/grammar">← Back to grammar list</a>
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${esc(p.pattern)} ${lessonTag}</h2>
          <p class="meaning-en">${esc(localizedMeaning(p))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${isKnown ? 'checked' : ''}>
          <span>Mark as known</span>
          ${statusBadge}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          🖨 Print / Save as PDF
        </button>
      </div>

      ${renderHowToUseTable(p)}

      <section>
        <h3 class="section-title">Explanation</h3>
        <p>${esc(localizedExplanation(p))}</p>
      </section>

      ${(() => {
        // IMP-137 (richness audit, 2026-05-10): Tofugu-style pedagogical
        // essay for the top-30 trickiest patterns. Renders when an essay
        // object is present. Each section is a short pedagogical
        // commentary block (intro, why_it_matters, common_pitfalls,
        // contrasts, closing_practice_tip). Stubs (provenance =
        // needs_native_review) render the intro + auto-extracted bits
        // and show a "essay pending native review" hint for the
        // empty fields.
        const essay = p.essay;
        if (!essay || typeof essay !== 'object') return '';
        const stub = essay.provenance === 'needs_native_review';
        const item = (label, text, fallback) => {
          if (!text && !fallback) return '';
          if (!text) return `<p><strong>${esc(label)}:</strong> <span class="muted small">${esc(fallback)}</span></p>`;
          return `<p><strong>${esc(label)}:</strong> ${esc(text)}</p>`;
        };
        return `
          <section class="pattern-essay">
            <h3 class="section-title">Deep dive ${stub ? '<span class="essay-stub-badge muted small">stub</span>' : ''}</h3>
            ${item('At a glance', essay.intro)}
            ${item('Why it matters', essay.why_it_matters, stub ? 'Pending native author.' : '')}
            ${item('Common pitfalls', essay.common_pitfalls)}
            ${item('Contrasts', essay.contrasts)}
            ${item('Practice tip', essay.closing_practice_tip, stub ? 'Pending native author.' : '')}
          </section>
        `;
      })()}

      ${(() => {
        // IMP-080 (audit round-7): L1-interference note for the active
        // locale, when authored. Niche-N1 unique-claim lever.
        const note = localizedL1Note(p);
        if (!note) return '';
        return `
          <section class="l1-note">
            <h3 class="section-title">L1 note</h3>
            <p>${esc(note)}</p>
          </section>
        `;
      })()}

      <section>
        <h3 class="section-title">Examples (${examples.length})</h3>
        <ul class="example-list">${exampleItems}</ul>
      </section>

      ${mistakes.length ? `
        <section>
          <h3 class="section-title">Common Mistakes / Contrasts</h3>
          <ul class="mistakes-list">${mistakeItems}</ul>
        </section>
      ` : ''}

      <section>
        <h3 class="section-title">意味（やさしい にほんご）</h3>
        <p>${renderJa(p.meaning_ja)}</p>
      </section>

      ${p.notes ? `<section><h3 class="section-title">Notes</h3><p>${esc(p.notes)}</p></section>` : ''}
    </article>
  `;
  container.innerHTML = html;

  document.getElementById('mark-known')?.addEventListener('change', (ev) => {
    storage.setManuallyKnown(p.id, ev.target.checked);
    renderGrammarPatternDetail(container, p, allPatterns);
  });
  // IMP-146: print → save-as-PDF. window.print() opens the browser
  // print dialog where the user picks "Save as PDF" as the destination.
  // No new dependency; @media print CSS hides the chrome.
  document.getElementById('pattern-print-btn')?.addEventListener('click', () => {
    window.print();
  });
}
