// Chapter 1 - Learn. Hub > Grammar TOC | Vocab TOC | pattern detail.
import { renderJa } from './furigana.js';
import * as storage from './storage.js';

let grammarCache = null;
let vocabCache = null;
let kanjiCache = null;

async function loadGrammar() {
  if (grammarCache) return grammarCache;
  const res = await fetch('data/grammar.json');
  if (!res.ok) throw new Error(`Failed to load grammar.json: ${res.status}`);
  grammarCache = await res.json();
  return grammarCache;
}

async function loadVocab() {
  if (vocabCache) return vocabCache;
  const res = await fetch('data/vocab.json');
  if (!res.ok) throw new Error(`Failed to load vocab.json: ${res.status}`);
  vocabCache = await res.json();
  return vocabCache;
}

async function loadKanji() {
  if (kanjiCache) return kanjiCache;
  const res = await fetch('data/kanji.json');
  if (!res.ok) throw new Error(`Failed to load kanji.json: ${res.status}`);
  kanjiCache = await res.json();
  return kanjiCache;
}

export async function renderLearn(container, params) {
  const slug = params ? decodeURIComponent(params) : '';
  // Hub: no slug -> 5-card chooser (Brief 2 follow-up).
  if (!slug) {
    // Pre-load corpora so the hub copy reflects live counts (single source of truth = data files).
    await Promise.all([loadGrammar(), loadVocab(), loadKanji()]);
    return renderHub(container);
  }
  // Sub-section: grammar TOC.
  if (slug === 'grammar') {
    const data = await loadGrammar();
    return renderTOC(container, data);
  }
  // Sub-section: vocabulary list or per-word detail.
  if (slug === 'vocab' || slug === 'vocabulary') {
    const data = await loadVocab();
    return renderVocabList(container, data);
  }
  if (slug.startsWith('vocab/')) {
    const data = await loadVocab();
    const grammar = await loadGrammar();
    const form = decodeURIComponent(slug.slice('vocab/'.length));
    return renderVocabDetail(container, data, grammar, form);
  }
  // Otherwise treat as a pattern ID.
  const data = await loadGrammar();
  const pattern = data.patterns.find(p => p.id === slug);
  if (pattern) return renderPatternDetail(container, pattern, data.patterns);
  // Unknown slug - fall back to hub.
  return renderHub(container);
}

// Flatten patterns into the same order the TOC presents them: super-category
// declaration order, sorted by patternOrder within each group. Used by the
// detail-page prev/next nav so navigation matches the user's mental model
// (the order they see when browsing the grammar list).
function buildOrderedPatternList(allPatterns) {
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

function renderHub(container) {
  // Zen Modern hub: two semantic groups (Reference + Practice) with
  // hairline-rule section labels and Muji-signature numbered card
  // indices (01-05). Reading-frequency order, not grid-symmetry order.
  const grammarCount = (grammarCache?.patterns || []).length || 187;
  const vocabCount = (vocabCache?.entries || []).length || 1003;
  const kanjiCount = (kanjiCache?.entries || []).length || 106;
  container.innerHTML = `
    <h2>Learn</h2>

    <div class="section-label">
      <span class="section-label-text">Reference</span>
      <span class="section-label-rule" aria-hidden="true"></span>
    </div>
    <div class="learn-hub learn-hub-3">
      <a class="hub-card" href="#/learn/grammar">
        <p class="card-index" aria-hidden="true">01</p>
        <h3>Grammar</h3>
        <p>${grammarCount} patterns across 5 sections. Form, examples, common mistakes.</p>
        <span class="hub-cta">Browse</span>
      </a>
      <a class="hub-card" href="#/learn/vocab">
        <p class="card-index" aria-hidden="true">02</p>
        <h3>Vocabulary</h3>
        <p>${vocabCount} words grouped by topic — people, time, places, verbs, adjectives.</p>
        <span class="hub-cta">Browse</span>
      </a>
      <a class="hub-card" href="#/kanji">
        <p class="card-index" aria-hidden="true">03</p>
        <h3>Kanji</h3>
        <p>${kanjiCount} kanji with on / kun-yomi, meanings, stroke order. Tap any glyph.</p>
        <span class="hub-cta">Browse</span>
      </a>
    </div>

    <div class="section-label">
      <span class="section-label-text">Practice</span>
      <span class="section-label-rule" aria-hidden="true"></span>
    </div>
    <div class="learn-hub learn-hub-2">
      <a class="hub-card" href="#/reading">
        <p class="card-index" aria-hidden="true">04</p>
        <h3>Dokkai (Reading)</h3>
        <p>30 graded passages with comprehension questions. Audio for every passage.</p>
        <span class="hub-cta">Practice</span>
      </a>
      <a class="hub-card" href="#/listening">
        <p class="card-index" aria-hidden="true">05</p>
        <h3>Listening</h3>
        <p>12 items across the three JLPT N5 listening formats. Audio for every script.</p>
        <span class="hub-cta">Practice</span>
      </a>
    </div>
  `;
}

// Render-time mapping: 40 fine-grained vocab sections -> 6 super-sections.
// Same pattern as GRAMMAR_SUPERCATS in renderTOC. Data file unchanged.
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
// Used by BOTH renderVocabList (to render) and renderVocabDetail (to
// compute prev/next) so the detail-page ←/→ navigation matches the
// order the user sees on the list page. Without this shared source of
// truth the two pages disagree at section boundaries — reported
// 2026-05-02 (毎日 list-next is いりぐち; detail-next was まいあさ).
function buildOrderedVocabList(entries) {
  const bySuper = new Map();
  for (const [s] of VOCAB_SUPERSECTS) bySuper.set(s, []);
  for (const e of entries) {
    const sup = vocabSuperSectionFor(e.section || 'Other');
    bySuper.get(sup).push(e);
  }
  const flat = [];
  for (const [sup, items] of bySuper.entries()) {
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

function renderVocabList(container, data) {
  const entries = data.entries || [];
  // Use the shared ordering helper so the list and the detail-page
  // prev/next chain agree byte-for-byte.
  const ordered = buildOrderedVocabList(entries);
  const bySuper = new Map();
  for (const [s] of VOCAB_SUPERSECTS) bySuper.set(s, []);
  for (const e of ordered) {
    const sup = vocabSuperSectionFor(e.section || 'Other');
    bySuper.get(sup).push(e);
  }
  const slugify = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  const sections = [...bySuper.entries()].map(([sup, items]) => {
    // No re-sort: items are already in canonical order from buildOrderedVocabList.
    const cards = items.map(v => `
      <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(v.form || '')}">
        <span class="vocab-form" lang="ja">${esc(v.form || '')}</span>
        ${v.reading ? `<span class="vocab-reading" lang="ja">${esc(v.reading)}</span>` : ''}
        <span class="vocab-gloss">${esc(v.gloss || '')}</span>
      </a>
    `).join('');
    return `
      <details class="vocab-section" id="vocab-${slugify(sup)}">
        <summary><strong>${esc(sup)}</strong> <span class="muted small">(${items.length})</span></summary>
        <div class="vocab-grid">${cards}</div>
      </details>
    `;
  }).join('');

  container.innerHTML = `
    <article class="vocab-toc">
      <a class="back-link" href="#/learn">← Back to Learn</a>
      <h2>Vocabulary</h2>
      <p class="page-lede">${entries.length} N5 words in ${VOCAB_SUPERSECTS.length} sections.</p>
      <div class="toc-controls">
        <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
        <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      </div>
      ${sections}
    </article>
  `;
  wireExpandCollapseControls(container, 'details.vocab-section');
}

function renderVocabDetail(container, vocabData, grammarData, form) {
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
  // data, or auto-tagger hasn't run), fall back to substring match. Future
  // CI run will catch and fix.
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
        // Legacy substring fallback (kanji form OR kana reading)
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
  // Reported 2026-05-02 (毎日 → list-next いりぐち vs detail-next まいあさ).
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
          <p class="vocab-gloss-big">${esc(entry.gloss || '')}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${isVocabKnown ? 'checked' : ''}>
          <span>Mark as known</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">Meaning</h3>
        <p><strong>English:</strong> ${esc(entry.gloss || '-')}</p>
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

  // Wire Mark-as-known toggle (parity with renderPatternDetail). OPEN-10.
  document.getElementById('mark-known-vocab')?.addEventListener('change', (ev) => {
    storage.setVocabKnown(entry.form, ev.target.checked);
  });
}

// Render-time mapping: 32 fine-grained categories in data/grammar.json
// to 5 pedagogically-coherent super-categories.
//
// Revised 2026-05-01 to fix two issues from the prior mapping:
// (a) "Functional and Upper-N5" was a catchall that swept up 7 sub-
//     categories which are actually verb-modal patterns (Permission and
//     Obligation, Experience and Advice, Compound and Listed Actions,
//     Excess, Intention, Way of Doing, Prohibitive). Those duplicated
//     the "Verbs" bucket — moved them in.
// (b) The catchall name described its origin ("the leftovers from N5")
//     rather than its current contents. Renamed "Set Phrases and
//     Discourse" — what's now actually inside is set phrases and
//     idioms, nominalisation markers, polite/honorific vocabulary,
//     sentence-final particles, quotation, and explanatory んです.
//
// Every fine category is now explicitly mapped (no fallback needed).
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
    // Verb-modal patterns moved here from the old catchall bucket
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
  'n5-135': 'Verbs',  // Verb (plain) + Noun — relative clauses
  'n5-144': 'Verbs',  // Verb-stem + ながら — while doing
  'n5-153': 'Verbs',  // まだ + Verb-ていません — not yet
  'n5-154': 'Verbs',  // もう + Verb-ました — already
  'n5-162': 'Verbs',  // Verb-plain ましょう (see 〜ます)
  'n5-163': 'Verbs',  // Verb-た あとで (see 〜あと)
};

function superCategoryFor(pattern) {
  // Allow per-pattern override when the category-level rule misroutes.
  // Caller passes the full pattern object so we can read both `id` and
  // `category`; legacy callers passing just a string still work.
  if (typeof pattern === 'object' && pattern && pattern.id in PATTERN_SUPERCAT_OVERRIDES) {
    return PATTERN_SUPERCAT_OVERRIDES[pattern.id];
  }
  const category = (typeof pattern === 'string') ? pattern : (pattern?.category || '');
  for (const [supercat, members] of GRAMMAR_SUPERCATS) {
    if (members.includes(category)) return supercat;
  }
  // Should never fire on the current 32 categories (all explicitly
  // mapped). Fallback for any future category not in the explicit map.
  return 'Set Phrases and Discourse';
}

function renderTOC(container, data) {
  // Group by super-category instead of fine-grained category.
  const bySuperCat = new Map();
  for (const [supercat] of GRAMMAR_SUPERCATS) bySuperCat.set(supercat, []);
  for (const p of data.patterns) {
    // Pass full pattern so per-id overrides apply (verb-pattern leakers
    // that live inside non-verb subcategories — see PATTERN_SUPERCAT_OVERRIDES).
    const sc = superCategoryFor(p);
    bySuperCat.get(sc).push(p);
  }

  const slugify = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  let html = `
    <a class="back-link" href="#/learn">← Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${data.patterns.length} patterns in ${bySuperCat.size} sections.</p>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
      <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
    </div>
  `;
  // Each super-category renders as a collapsible <details>. First paint:
  // 5 short heading rows (one per super-category). Click to expand a
  // section to see its cards.
  for (const [supercat, items] of bySuperCat) {
    items.sort((a, b) => (a.patternOrder ?? 0) - (b.patternOrder ?? 0));
    html += `<details class="toc-category" id="cat-${slugify(supercat)}">`;
    html += `<summary><h3>${esc(supercat)} <span class="cat-count muted small">(${items.length})</span></h3></summary>`;
    html += `<div class="grammar-grid">`;
    for (const p of items) {
      html += `
        <a class="grammar-card" href="#/learn/${encodeURIComponent(p.id)}">
          <span class="grammar-pattern" lang="ja">${esc(p.pattern)}</span>
          <span class="grammar-gloss">${esc(p.meaning_en)}</span>
        </a>
      `;
    }
    html += `</div></details>`;
  }
  if (data.patterns.length === 0) {
    html += `<div class="placeholder"><p>No patterns yet. Add entries to <code>data/grammar.json</code>.</p></div>`;
  } else if (data.patterns.length === 1) {
    html += `<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>`;
  }
  container.innerHTML = html;
  wireExpandCollapseControls(container, 'details.toc-category');
}

// Wire Expand-all / Collapse-all buttons to the matching details elements.
// Used by Grammar TOC, Vocab list, and Listening index.
function wireExpandCollapseControls(container, detailsSelector) {
  const expand = container.querySelector('.toc-expand-all');
  const collapse = container.querySelector('.toc-collapse-all');
  if (!expand || !collapse) return;
  expand.addEventListener('click', () => {
    container.querySelectorAll(detailsSelector).forEach(d => d.open = true);
  });
  collapse.addEventListener('click', () => {
    container.querySelectorAll(detailsSelector).forEach(d => d.open = false);
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
  // Humanize unknown snake_case keys defensively.
  return String(key)
    .replace(/_/g, ' ')
    .replace(/^./, c => c.toUpperCase());
}

// Build the "How to use / 使い方" table. Two layouts depending on the
// pattern's form-shape:
//
//   (A) Uniform pattern — same surface form attaches to every entry in
//       `attaches_to` (typical: ～だろう, ～ながら, etc.). Render rows of
//       attach-points on the left and one merged cell on the right
//       carrying the literal pattern. Mirrors the layout in the
//       reference image.
//
//   (B) Conjugating pattern — `conjugations` lists multiple forms with
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

  // Top table: attach-points → pattern. Single merged right-column cell
  // shows the pattern itself in JA. If attaches is empty we skip this
  // table and render only the conjugation breakdown.
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

  // Bottom table: conjugation breakdown. Only render if there are 2+
  // distinct conjugation entries (a single conjugation is redundant
  // with the top table).
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

function renderPatternDetail(container, p, allPatterns) {
  const conj = p.form_rules?.conjugations ?? [];
  const examples = p.examples ?? [];
  const mistakes = p.common_mistakes ?? [];
  const attaches = p.form_rules?.attaches_to ?? [];
  const entry = storage.getPatternEntry(p.id);
  const isKnown = !!entry?.isManuallyKnown;
  const isMastered = !!entry?.isMastered;
  const isWeak = !!entry?.isWeak && !isMastered;

  // Prev / next pattern in TOC order. allPatterns may be undefined if a future
  // caller forgets to thread it through — degrade gracefully (no nav row).
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

  const conjRows = conj.map(c => `
    <tr><td>${esc(c.label || c.form)}</td><td>${renderJa(c.example)}</td></tr>
  `).join('');

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

  const html = `
    <article class="pattern-detail">
      ${navHtml}
      <a class="back-link" href="#/learn/grammar">← Back to grammar list</a>
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${esc(p.pattern)}</h2>
          <p class="meaning-en">${esc(p.meaning_en)}</p>
        </div>
        <label class="known-toggle" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${isKnown ? 'checked' : ''}>
          <span>Mark as known</span>
          ${statusBadge}
        </label>
      </div>

      ${renderHowToUseTable(p)}

      <section>
        <h3 class="section-title">Explanation</h3>
        <p>${esc(p.explanation_en)}</p>
      </section>

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
    // Re-render so the badge updates without a full route() call.
    renderPatternDetail(container, p, allPatterns);
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
