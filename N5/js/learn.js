// Chapter 1 - Learn. Hub > Grammar TOC | Vocab TOC | pattern detail.
//
// IMP-022 (audit 2026-05-04 round 2): the grammar half (~18 KB) and the
// vocab half (~10 KB) of this module live in `learn-grammar.js` and
// `learn-vocab.js` respectively. The dispatcher in this file dynamic-
// imports the right chunk on demand, so the hub renders without paying
// for code paths the user hasn't asked for. The two chunks reuse `esc`
// and `wireExpandCollapseControls` exported below — keeping these here
// avoids duplication and a third "shared" module.

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
  // Hub: no slug -> 5-card chooser.
  if (!slug) {
    // Pre-load corpora so the hub copy reflects live counts (single source
    // of truth = data files).
    await Promise.all([loadGrammar(), loadVocab(), loadKanji()]);
    return renderHub(container);
  }
  // Grammar TOC.
  if (slug === 'grammar') {
    const [{ renderGrammarTOC }, data] = await Promise.all([
      import('./learn-grammar.js'),
      loadGrammar(),
    ]);
    return renderGrammarTOC(container, data);
  }
  // Vocabulary list.
  if (slug === 'vocab' || slug === 'vocabulary') {
    const [{ renderVocabularyList }, data] = await Promise.all([
      import('./learn-vocab.js'),
      loadVocab(),
    ]);
    return renderVocabularyList(container, data);
  }
  // Per-word vocab detail.
  if (slug.startsWith('vocab/')) {
    const [{ renderVocabularyDetail }, data, grammar] = await Promise.all([
      import('./learn-vocab.js'),
      loadVocab(),
      loadGrammar(),
    ]);
    const form = decodeURIComponent(slug.slice('vocab/'.length));
    return renderVocabularyDetail(container, data, grammar, form);
  }
  // Otherwise treat as a grammar pattern ID.
  const [{ renderGrammarPatternDetail }, data] = await Promise.all([
    import('./learn-grammar.js'),
    loadGrammar(),
  ]);
  const pattern = data.patterns.find(p => p.id === slug);
  if (pattern) return renderGrammarPatternDetail(container, pattern, data.patterns);
  // Unknown slug - fall back to hub.
  return renderHub(container);
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

// Shared helpers — exported so the lazy-loaded `learn-grammar.js` and
// `learn-vocab.js` can reuse them without a third "shared" module. Both
// are tiny pure functions; co-locating them with the dispatcher keeps the
// dependency graph flat (chunks → dispatcher; dispatcher → chunks at
// runtime via dynamic import).

// HTML-escape an arbitrary value. Used wherever we splice user-/data-
// derived strings into innerHTML templates.
export function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

// Wire Expand-all / Collapse-all buttons to the matching `<details>`
// elements in the rendered container. Used by Grammar TOC, Vocab list,
// and Listening index — anywhere the page presents a stack of accordion
// sections with global expand/collapse controls.
export function wireExpandCollapseControls(container, detailsSelector) {
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
