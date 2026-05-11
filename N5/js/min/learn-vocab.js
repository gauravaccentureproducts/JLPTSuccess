// Vocabulary half of Chapter 1 - Learn (split out from learn.js per IMP-022,
// audit 2026-05-04 round 2). Owns the vocab list page and the per-word
// detail page. Loaded lazily by `renderLearn` in learn.js when the user
// navigates to a vocab route.
import { renderJa } from './furigana.js';
import * as storage from './storage.js';
import { esc, wireExpandCollapseControls } from './learn.js';
import { currentLocale, t } from './i18n.js';
import { renderItemBadge } from './provenance-badge.js';

// ISSUE-063 + IMP-087 (audit round-7): render NHK pitch-accent {mora,
// drop} as a compact Tokyo-dialect HL pattern over the reading.
// drop = 0 -> 平板 (flat-rising LHHHH); drop = 1 -> 頭高 (HLLLL);
// drop = N -> 中高 (LHHH...drop position then L). N5-suitable concise
// view; an SVG visualizer can replace this later.
function _pitchPattern(pa, reading) {
  if (!pa || !Number.isFinite(pa.mora)) return '';
  const m = pa.mora;
  const drop = pa.drop;
  let pattern = '';
  for (let i = 1; i <= m; i++) {
    if (drop === 0) {
      pattern += i === 1 ? 'L' : 'H';
    } else if (drop === 1) {
      pattern += i === 1 ? 'H' : 'L';
    } else {
      pattern += i === 1 ? 'L' : (i <= drop ? 'H' : 'L');
    }
  }
  return pattern;
}

// IMP-088 (audit round-7): map counter codes to their canonical kana
// readings for display (e.g. 'satsu' -> さつ).
function _counterKana(code) {
  const map = {
    'satsu': 'さつ',
    'dai': 'だい',
    'hiki': 'ひき',
    'wa': 'わ',
    'mai': 'まい',
    'ken': 'けん',
    'hon': 'ほん',
    'soku': 'そく',
    'ko': 'こ',
    'nin': 'にん',
    'tsu': 'つ',
    'kai': 'かい',
    'do': 'ど',
    'fun': 'ふん',
    'ji': 'じ',
  };
  return map[code] || code;
}

// IMP-119 (round-9, 2026-05-06): keigo-chain trio data.
// 9 N5 vocab entries carry `register_chain_id` linking to a humble/plain/
// respectful trio. The humble (謙譲語) and respectful (尊敬語) forms are
// N3+ scope and not present in data/vocab.json, but surfacing them as a
// "for-awareness" callout on the plain entry's detail page closes the
// niche-N4 (all-in-one) gap of "I had to look this up in another app."
//
// Format: chain_id -> {humble, respectful, note_en}
const _KEIGO_CHAINS = {
  'be': {
    humble:     { ja: 'おる',         reading: 'おる',         gloss: 'to exist (humble; said about self / in-group)' },
    respectful: { ja: 'いらっしゃる', reading: 'いらっしゃる', gloss: 'to exist (respectful; said about social superiors)' },
    note_en: 'いる has both humble (謙譲語: おる) and respectful (尊敬語: いらっしゃる) keigo forms. The respectful いらっしゃる also covers "go" and "come" (see chains go / come).',
  },
  'go': {
    humble:     { ja: '参る',         reading: 'まいる',       gloss: 'to go / come (humble)' },
    respectful: { ja: 'いらっしゃる', reading: 'いらっしゃる', gloss: 'to go / come / be (respectful)' },
    note_en: '行く maps to humble 参る and respectful いらっしゃる. The respectful いらっしゃる is shared with "come" and "be" (one form, three meanings).',
  },
  'eat': {
    humble:     { ja: 'いただく',     reading: 'いただく',     gloss: 'to eat / receive (humble; also said before meals as いただきます)' },
    respectful: { ja: '召し上がる',   reading: 'めしあがる',   gloss: 'to eat (respectful; offered to the listener)' },
    note_en: '食べる has the humble form いただく (also a courtesy expression before meals) and the respectful 召し上がる (used when offering food: お召し上がりください = "please eat").',
  },
  'see': {
    humble:     { ja: '拝見する',     reading: 'はいけんする', gloss: 'to see / look at (humble)' },
    respectful: { ja: 'ご覧になる',   reading: 'ごらんになる', gloss: 'to see / look at (respectful)' },
    note_en: '見る\'s humble 拝見する is used when viewing something a superior gave/showed you (e.g. 写真を拝見しました). 御覧になる is offered to a superior (お写真を御覧になりますか).',
  },
  'say': {
    humble:     { ja: '申す',         reading: 'もうす',       gloss: 'to say (humble; common in self-introductions)' },
    respectful: { ja: 'おっしゃる',   reading: 'おっしゃる',   gloss: 'to say (respectful)' },
    note_en: '言う\'s humble 申す appears in self-intros (鈴木と申します = "I am called Suzuki"). Respectful おっしゃる is used when quoting a superior\'s words (先生がおっしゃった).',
  },
  'do': {
    humble:     { ja: 'いたす',       reading: 'いたす',       gloss: 'to do (humble)' },
    respectful: { ja: 'なさる',       reading: 'なさる',       gloss: 'to do (respectful)' },
    note_en: 'する maps to humble いたす and respectful なさる. Common in customer-service speech: お電話いたします (I will call) / 何になさいますか (what would you like).',
  },
};

function _renderKeigoChain(entry) {
  const chain = _KEIGO_CHAINS[entry.register_chain_id];
  if (!chain) return '';
  const plain = entry.form;
  const plainReading = entry.reading || '';
  const plainGloss = entry.gloss || '';
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
  return `
    <div class="keigo-chain">
      <p><strong>Keigo chain (${esc(entry.register_chain_id)}):</strong> this verb has humble (謙譲語) and respectful (尊敬語) forms used in formal Japanese.</p>
      <table class="keigo-chain-table" aria-label="Politeness register trio">
        <thead>
          <tr>
            <th>Humble (謙譲語)</th>
            <th>Plain (you are here)</th>
            <th>Respectful (尊敬語)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td data-label="Humble (謙譲語)">
              <span lang="ja" class="keigo-form">${esc(chain.humble.ja)}</span>
              <span lang="ja" class="keigo-reading muted small">${esc(chain.humble.reading)}</span>
              <span class="keigo-gloss">${esc(chain.humble.gloss)}</span>
            </td>
            <td data-label="Plain (you are here)" class="keigo-cell-current">
              <span lang="ja" class="keigo-form">${esc(plain)}</span>
              <span lang="ja" class="keigo-reading muted small">${esc(plainReading)}</span>
              <span class="keigo-gloss">${esc(plainGloss)}</span>
            </td>
            <td data-label="Respectful (尊敬語)">
              <span lang="ja" class="keigo-form">${esc(chain.respectful.ja)}</span>
              <span lang="ja" class="keigo-reading muted small">${esc(chain.respectful.reading)}</span>
              <span class="keigo-gloss">${esc(chain.respectful.gloss)}</span>
            </td>
          </tr>
        </tbody>
      </table>
      <p class="muted small">${esc(chain.note_en)}</p>
      <p class="muted small">Humble + respectful forms are N3+ scope; shown here for awareness only — they are not yet drilled at N5.</p>
    </div>
  `;
}

// IMP-046 (audit round-5): pick locale-aware vocab gloss when present,
// else fall back to English. The translated subset (~120 entries) carries
// `gloss_hi`; remaining entries fall through to `gloss`. Phase 3 of
// locale transition (2026-05-06) narrowed the set from {vi,id,ne,zh}
// to {hi} only.
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
      // 2026-05-06 (user request): list-tile pages show only the entry's
      // primary form for active-recall practice. Reading + gloss appear
      // on the detail page after click-through. This lets learners
      // self-assess "do I remember what this means?" before revealing.
      const cards = items.map(v => `
        <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(v.form || '')}">
          <span class="vocab-form" lang="ja">${esc(v.form || '')}</span>
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
    // IME composition guard — see learn-grammar.js for the rationale.
    // tl;dr: re-rendering on every `input` event destroys the input
    // mid-IME-composition; partial latin chars (ｔ etc.) leak into
    // the value. Skip until compositionend fires.
    let isComposing = false;
    const reapply = () => {
      _vocabFilterText = inp.value;
      renderVocabularyList(container, data);
      const re = document.getElementById('vocab-filter-q');
      if (re) {
        re.focus();
        const v = re.value;
        re.setSelectionRange(v.length, v.length);
      }
    };
    inp.addEventListener('compositionstart', () => { isComposing = true; });
    inp.addEventListener('compositionend',   () => { isComposing = false; reapply(); });
    inp.addEventListener('input', () => {
      if (isComposing) return;
      reapply();
    });
  }
}

export function renderVocabularyDetail(container, vocabData, grammarData, form) {
  const entries = vocabData.entries || [];
  const entry = entries.find(e => e.form === form);
  if (!entry) {
    container.innerHTML = `
      <article class="vocab-detail">
        <a class="back-link" href="#/learn/vocab">← ${esc(t('vocab_detail.back_to_vocabulary'))}</a>
        <h2>Word not found</h2>
        <p>No vocab entry matches <strong lang="ja">${esc(form)}</strong>. The word may live under a different form.</p>
      </article>
    `;
    return;
  }
  // Pull example sentences from grammar.json. Each example carries a
  // `vocab_ids: [...]` field (populated by tools/link_grammar_examples_to_vocab.py)
  // listing exactly which vocab entries it demonstrates. We filter by ID
  // - not by substring on the form field - so homographs (e.g., かた "person"
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
  // BUG-4 fix (UI test 2026-05-07): fall back to vocab.json's own
  // `examples` array for entries that have no grammar cross-reference.
  // 724 entries got templated 2nd examples in v1.12.44 (ISSUE-096 + Phase-3
  // residual) but were invisible until this fallback was wired up.
  // Source-tagged "Vocab catalog" so the learner can distinguish.
  for (const ex of (entry.examples || [])) {
    if (!ex.ja) continue;
    if (seen.has(ex.ja)) continue;
    seen.add(ex.ja);
    examples.push({ ja: ex.ja, en: ex.translation_en, source: 'Vocab catalog' });
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
      <a class="back-link" href="#/learn/vocab">← ${esc(t('vocab_detail.back_to_vocabulary'))}</a>
      <header class="vocab-header pattern-header">
        <div>
          <p class="muted small">${esc(entry.section || '')}</p>
          <h2 class="vocab-form-big" lang="ja">${esc(entry.form)}</h2>
          ${entry.reading ? `<p class="vocab-reading-big" lang="ja">${esc(entry.reading)}</p>` : ''}
          <p class="vocab-gloss-big">${esc(localizedGloss(entry))} ${renderItemBadge(entry, true)}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${isVocabKnown ? 'checked' : ''}>
          <span>${esc(t('vocab_detail.mark_as_known'))}</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">${esc(t('vocab_detail.meaning'))}</h3>
        <p><strong>${currentLocale() === 'en' ? esc(t('vocab_detail.english')) : esc(t('vocab_detail.meaning'))}:</strong> ${esc(localizedGloss(entry) || '-')}</p>
        ${currentLocale() !== 'en' && entry.gloss && localizedGloss(entry) !== entry.gloss
            ? `<p><strong>${esc(t('vocab_detail.english'))}:</strong> ${esc(entry.gloss)}</p>`
            : ''}
        ${entry.reading ? `<p><strong>${esc(t('vocab_detail.japanese_reading'))}:</strong> <span lang="ja">${esc(entry.reading)}</span></p>` : ''}
        ${(() => {
          // ISSUE-063 + IMP-087 + IMP-088 (audit round-7): surface vocab
          // depth fields when present. Pitch shown as Tokyo-dialect HL
          // pattern derived from {mora, drop}; counter shown as the
          // canonical reading; register chain badge for keigo entries.
          const out = [];
          if (entry.pitch_accent && Number.isFinite(entry.pitch_accent.mora)) {
            out.push(`<p><strong>${esc(t('vocab_detail.pitch_accent'))}:</strong> <span class="vocab-pitch" lang="ja">${esc(_pitchPattern(entry.pitch_accent, entry.reading))}</span> <span class="muted small">(drop: ${entry.pitch_accent.drop})</span></p>`);
          }
          if (entry.counter) {
            out.push(`<p><strong>${esc(t('vocab_detail.counter'))}:</strong> <span lang="ja">〜${esc(_counterKana(entry.counter))}</span></p>`);
          }
          if (entry.register) {
            out.push(`<p><strong>${esc(t('vocab_detail.register'))}:</strong> <span class="vocab-register-tag">${esc(entry.register)}</span></p>`);
          }
          if (entry.transitivity) {
            out.push(`<p><strong>${esc(t('vocab_detail.transitivity'))}:</strong> ${esc(entry.transitivity)}${entry.pair_id ? ` <span class="muted small">(${esc(t('vocab_detail.pair'))}: ${esc(entry.pair_id)})</span>` : ''}</p>`);
          }
          // BUG-3 fix (UI test 2026-05-07): surface verb_class +
          // group1_exception. Populated on all 134 verbs in v1.12.43
          // (ISSUE-099) but invisible until this render hook.
          if (entry.verb_class) {
            const classLabels = {
              godan: 'Godan (Group 1, u-verb)',
              ichidan: 'Ichidan (Group 2, ru-verb)',
              irregular: 'Irregular (Group 3 — する / 来る)',
            };
            const label = classLabels[entry.verb_class] || entry.verb_class;
            const g1exc = entry.group1_exception
              ? ` <span class="vocab-g1-exception" title="Looks like Group 2 but conjugates as Group 1 (X-6.6)">Group-1 exception</span>`
              : '';
            out.push(`<p><strong>${esc(t('vocab_detail.verb_class'))}:</strong> ${esc(label)}${g1exc}</p>`);
          }
          // IMP-119 (round-9, 2026-05-06): keigo-chain visualizer.
          // When the entry is part of a register chain (humble / plain /
          // respectful trio), render an awareness panel showing all three
          // forms side-by-side. Most humble/respectful forms (おる, いただく,
          // 召し上がる, 申す, おっしゃる, etc.) are N3+ scope and absent
          // from the N5 vocab corpus, so we hold the trio data in this
          // module rather than data/vocab.json. The N5 learner sees it as
          // "FYI: here is the keigo equivalent", not "drill this now".
          if (entry.register_chain_id && _KEIGO_CHAINS[entry.register_chain_id]) {
            out.push(_renderKeigoChain(entry));
          }
          // Phase 3 of locale transition (2026-05-06): the false_friends.zh
          // hook is removed alongside the zh locale - currentLocale() can
          // no longer return 'zh'. The underlying data is stripped in
          // Phase 4. If/when a Hindi false-friends list is authored, a
          // false_friends.hi hook can replace this with the same shape.
          return out.join('');
        })()}
      </section>

      <section>
        <h3 class="section-title">${esc(t('vocab_detail.example_sentences'))} ${top.length ? `(${top.length})` : ''}</h3>
        ${top.length ? `
          <ol class="example-list">
            ${top.map(ex => `
              <li>
                <p lang="ja" class="example-ja">${renderJa(ex.ja)}</p>
                ${ex.en ? `<p class="translation">${esc(ex.en)}</p>` : ''}
                ${ex.source ? `<p class="muted small">${esc(t('vocab_detail.from_pattern'))}: <span lang="ja">${esc(ex.source)}</span></p>` : ''}
              </li>
            `).join('')}
          </ol>
        ` : `
          <p class="muted">${esc(t('vocab_detail.no_examples'))}</p>
        `}
      </section>

      ${(() => {
        // IMP-WAVE4 (UI audit fix, 2026-05-11): collocations.
        // 988/1009 entries have curated collocations. Render as a flex-list of
        // chips. Format: array of strings, each one a real Japanese phrase
        // (e.g., "コーヒーを のむ", "あつい コーヒー").
        const colls = Array.isArray(entry.collocations) ? entry.collocations.filter(c => typeof c === 'string' && c.trim()) : [];
        if (!colls.length) return '';
        return `
          <section class="vocab-collocations">
            <h3 class="section-title">${esc(t('vocab_detail.collocations'))} (${colls.length})</h3>
            <ul class="collocation-list">
              ${colls.map(c => `<li class="collocation-chip" lang="ja">${esc(c)}</li>`).join('')}
            </ul>
          </section>
        `;
      })()}

      ${(() => {
        // IMP-WAVE4: false_friends — easily confused words.
        // Field is an array of forms (strings) that learners commonly confuse
        // with this entry. Render as inline cross-references to those vocab pages.
        const ff = Array.isArray(entry.false_friends) ? entry.false_friends : [];
        if (!ff.length) return '';
        return `
          <section class="vocab-false-friends">
            <h3 class="section-title">${esc(t('vocab_detail.false_friends'))}</h3>
            <div class="false-friend-grid">
              ${ff.map(form => `
                <a class="false-friend-card" href="#/learn/vocab/${encodeURIComponent(form)}">
                  <span lang="ja">${esc(form)}</span>
                </a>
              `).join('')}
            </div>
          </section>
        `;
      })()}

      ${(() => {
        // IMP-WAVE4: pragmatic_functions — multi-function word disambiguation.
        // Schema: array of {function, gloss, context} objects.
        const pf = Array.isArray(entry.pragmatic_functions) ? entry.pragmatic_functions : [];
        if (!pf.length) return '';
        return `
          <section class="vocab-pragmatic">
            <h3 class="section-title">${esc(t('vocab_detail.pragmatic'))}</h3>
            <ul class="pragmatic-list">
              ${pf.map(p => `
                <li>
                  <strong class="pragmatic-function">${esc(p.function || '')}</strong>
                  ${p.gloss ? ` — <span class="pragmatic-gloss">${esc(p.gloss)}</span>` : ''}
                  ${p.context ? `<p class="muted small pragmatic-context">${esc(p.context)}</p>` : ''}
                </li>
              `).join('')}
            </ul>
          </section>
        `;
      })()}

      ${(() => {
        // IMP-WAVE4: devoiced_vowels — Tokyo-standard phonological marker.
        // Schema: {positions: int[], note: string, rule: string}.
        const dv = entry.devoiced_vowels;
        if (!dv || typeof dv !== 'object') return '';
        return `
          <section class="vocab-devoicing">
            <h3 class="section-title">${esc(t('vocab_detail.devoiced_vowels'))}</h3>
            ${Array.isArray(dv.positions) && dv.positions.length
              ? `<p><strong>${esc(t('vocab_detail.devoiced_position'))}:</strong> mora ${dv.positions.join(', ')} (0-indexed)</p>`
              : `<p class="muted small">${esc(t('vocab_detail.devoiced_no_dev'))}</p>`}
            ${dv.note ? `<p class="muted small">${esc(dv.note)}</p>` : ''}
            ${dv.rule ? `<p class="muted small"><em>${esc(t('vocab_detail.devoiced_rule'))}:</em> ${esc(dv.rule)}</p>` : ''}
          </section>
        `;
      })()}

      ${(() => {
        // IMP-WAVE4: counter_register — casual/formal counter pair.
        // Schema: {counter, irregular, note, register_pair: {casual_alt, formal_same}}.
        const cr = entry.counter_register;
        if (!cr || typeof cr !== 'object') return '';
        return `
          <section class="vocab-counter-register">
            <h3 class="section-title">${esc(t('vocab_detail.counter_register'))}</h3>
            ${cr.counter ? `<p><strong>${esc(t('vocab_detail.counter_root'))}:</strong> <span lang="ja">〜${esc(cr.counter)}</span> ${cr.irregular ? `<span class="vocab-g1-exception" title="Irregular kun-yomi form">${esc(t('vocab_detail.irregular'))}</span>` : ''}</p>` : ''}
            ${cr.note ? `<p>${esc(cr.note)}</p>` : ''}
            ${cr.register_pair ? `
              <div class="register-pair-grid">
                ${cr.register_pair.casual_alt ? `<div><span class="muted small">${esc(t('vocab_detail.casual'))}:</span> <span lang="ja">${esc(cr.register_pair.casual_alt)}</span></div>` : ''}
                ${cr.register_pair.formal_same ? `<div><span class="muted small">${esc(t('vocab_detail.formal'))}:</span> <span lang="ja">${esc(cr.register_pair.formal_same)}</span></div>` : ''}
              </div>
            ` : ''}
          </section>
        `;
      })()}

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
