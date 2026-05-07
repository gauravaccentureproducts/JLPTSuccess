// SVA-NEXT-2.4 (round-9 follow-up, 2026-05-07): print-to-PDF mock-paper.
//
// Why: deadline-driven SSW-applicant + university-applicant learners
// often want a "real paper, real pencil" mock-test ritual — the kind
// of pre-exam practice no other JLPT app provides. The browser already
// knows how to print + save-as-PDF; this module renders any of our
// 29 papers (4 per-section × 7 papers + 1 combined moji+goi × 7 +
// 1 combined bunpou+dokkai × 7 + 1 chokai virtual × 1 + 7 full-mocks)
// in a layout designed for paper consumption rather than the screen.
//
// Routing:
//   #/print/<paperId>           — print view of one paper
//   #/print/<paperId>?key=1     — same, but with answer key page appended
//
// Print etiquette:
//   - A4 size, 2 cm margins, 11 pt body, 13 pt mondai headings.
//   - Page break before each mondai cluster so cuts feel natural.
//   - Absolute zero web chrome on the printed page (CSS @media print
//     hides .primary-nav, .site-footer, .skip-link, anything not
//     inside .print-paper-root).
//   - The on-screen render still shows nav / back-link / buttons;
//     it's only the *printed* version that strips chrome.
//
// Content taxonomy supported (paperId -> handler):
//   moji-N / goi-N / bunpou-N / dokkai-N
//                        — single-category 15Q (or 10Q for Paper 7) paper.
//   genngo-chishiki-moji-goi-N
//                        — combined moji + goi section (two component
//                          papers concatenated under one cover).
//   genngo-chishiki-bunpou-dokkai-N
//                        — combined bunpou + dokkai section.
//   chokai-N             — listening virtual paper (script-only print —
//                          a paper rendition of a listening section makes
//                          sense for the "follow along while audio plays"
//                          ritual; we still include the prompts + choices).
//   full-mock-N          — full 85Q × 105min mock paper (sections
//                          concatenated under one cover, with section
//                          dividers and recommended timing).
//
// Privacy: pure on-device render. No fetch beyond the existing static
// data files. No external print service. The browser's print dialog
// is the only network-adjacent action; that's the OS, not us.

import { renderJa } from './furigana.js';

// ---------- Module-level cache (re-uses lifecycle of papers.js) ----------
let manifest = null;
const paperCache = new Map();

async function loadManifest() {
  if (manifest) return manifest;
  const res = await fetch('data/papers/manifest.json');
  if (!res.ok) throw new Error(`Failed to load papers manifest: ${res.status}`);
  manifest = await res.json();
  return manifest;
}

async function loadPaperByCategoryNumber(category, paperNumber) {
  const cacheKey = `${category}-${paperNumber}`;
  if (paperCache.has(cacheKey)) return paperCache.get(cacheKey);
  const res = await fetch(`data/papers/${category}/paper-${paperNumber}.json`);
  if (!res.ok) throw new Error(`Failed to load paper ${cacheKey}: ${res.status}`);
  const paper = await res.json();
  paperCache.set(cacheKey, paper);
  return paper;
}

// Resolve a flat paperId ("moji-3" / "dokkai-7") into (category, number).
function splitPaperId(paperId) {
  const m = String(paperId).match(/^([a-z]+)-(\d+)$/);
  if (!m) return null;
  return { category: m[1], number: parseInt(m[2], 10) };
}

// Look up a combined section by id in manifest.combined_sections.
function findCombinedSection(m, id) {
  return (m.combined_sections || []).find(s => s.id === id);
}
function findFullMock(m, id) {
  return (m.full_mock_papers || []).find(p => p.id === id);
}
function findVirtualPaper(m, id) {
  return (m.virtual_papers || []).find(p => p.id === id);
}

// ---------- Public API ----------

export async function renderPrint(container, params) {
  // params is the paperId (possibly with ?key=1 appended via the
  // hash router; we accept both ?key=1 and /key suffixes for safety).
  const raw = (params || '').trim();
  if (!raw) return renderIndex(container);
  const [paperIdEncoded, qs] = raw.split('?');
  const paperId = decodeURIComponent(paperIdEncoded);
  const includeKey = (qs && /(?:^|&)key=1\b/.test(qs)) || false;

  let m;
  try {
    m = await loadManifest();
  } catch (e) {
    container.innerHTML = `<article class="print-paper-error"><p>Could not load papers manifest: ${esc(String(e))}</p></article>`;
    return;
  }

  // Dispatch by paperId shape.
  // Order matters: full-mock-N is checked first, then combined-section ids
  // (which contain hyphens), then virtual papers, then per-category.
  if (/^full-mock-\d+$/.test(paperId)) {
    return renderFullMock(container, m, paperId, includeKey);
  }
  if (/^genngo-chishiki-(moji-goi|bunpou-dokkai)-\d+$/.test(paperId)) {
    return renderCombinedSection(container, m, paperId, includeKey);
  }
  if (/^chokai-\d+(?:-virtual)?$/.test(paperId)) {
    return renderChokai(container, m, paperId, includeKey);
  }
  // Per-category single paper (moji-3 / goi-1 / bunpou-7 / dokkai-2).
  const split = splitPaperId(paperId);
  if (split && ['moji', 'goi', 'bunpou', 'dokkai'].includes(split.category)) {
    return renderSingleCategoryPaper(container, m, split, includeKey);
  }
  return renderIndex(container, paperId);
}

// ---------- Index (when paperId is missing or unknown) ----------

async function renderIndex(container, badId) {
  const m = await loadManifest();
  const cards = [];
  // Per-category papers
  (m.categories || []).forEach(cat => {
    cat.papers.forEach(p => {
      cards.push(printCard(p.id, p.name, `${p.questionCount} Q · ${cat.label_ja}`));
    });
  });
  // Combined sections
  (m.combined_sections || []).forEach(s => {
    cards.push(printCard(s.id, s.name_en, `${s.questionCount} Q · ${esc(s.sectionLabel)}`));
  });
  // Full mocks
  (m.full_mock_papers || []).forEach(p => {
    cards.push(printCard(p.id, p.name_en, `${p.totalQuestions} Q · ${p.totalDurationMin} min · full mock`));
  });
  // Virtual chokai
  (m.virtual_papers || []).forEach(p => {
    cards.push(printCard(p.id, p.name, `${p.questionCount} Q · ${p.expectedDurationMin} min · listening`));
  });

  container.innerHTML = `
    <article class="print-paper-index">
      <a class="back-link" href="#/papers">← Mock-test papers</a>
      <h2>Print a paper</h2>
      <p class="page-lede">Pick a paper to render in print-ready layout. Use your browser's <strong>Print → Save as PDF</strong> to keep an offline copy, or print to paper for a real-pencil mock-test ritual. The on-screen layout includes a cover page, mondai-grouped questions, and an optional answer-key page.</p>
      ${badId ? `<p class="print-paper-bad-id">Unknown paper id: <code>${esc(badId)}</code>. Pick from the list below.</p>` : ''}
      <ul class="print-paper-list">${cards.join('')}</ul>
      <p class="print-paper-foot muted small">For the on-screen mock-test flow with auto-grading, use <a href="#/papers">Mock-test papers</a> or <a href="#/test">Test</a>.</p>
    </article>
  `;
}

function printCard(id, name, meta) {
  return `
    <li class="print-paper-card">
      <a class="print-paper-link" href="#/print/${esc(id)}">
        <strong>${esc(name)}</strong>
        <span class="muted small">${esc(meta)}</span>
      </a>
      <span class="print-paper-actions">
        <a href="#/print/${esc(id)}" title="Open print view">View</a>
        <span aria-hidden="true">·</span>
        <a href="#/print/${esc(id)}?key=1" title="Open with answer key">+ Key</a>
      </span>
    </li>
  `;
}

// ---------- Per-category single paper ----------

async function renderSingleCategoryPaper(container, m, split, includeKey) {
  const { category, number } = split;
  let paper;
  try {
    paper = await loadPaperByCategoryNumber(category, number);
  } catch (e) {
    container.innerHTML = `<article class="print-paper-error"><p>Could not load <code>${esc(category)}-${number}</code>: ${esc(String(e))}</p><p><a href="#/print">Back to print index.</a></p></article>`;
    return;
  }
  const cat = (m.categories || []).find(c => c.id === category) || { label: category, label_ja: '' };
  const meta = (cat.papers || []).find(p => p.id === paper.id) || {};
  const sections = [{
    label_ja: cat.label_ja || cat.label || category,
    label_en: cat.label || category,
    questions: paper.questions,
    duration_min: meta.expectedDurationMin || null,
  }];
  const cover = {
    name_en: paper.name || `${cat.label} Paper ${number}`,
    name_ja: `${cat.label_ja || ''} Paper ${number}`,
    total_q: paper.questions.length,
    duration_min: meta.expectedDurationMin || null,
    instructions: defaultInstructions(category),
  };
  return renderPrintShell(container, paper.id, cover, sections, includeKey);
}

// ---------- Combined section (genngo-chishiki-...) ----------

async function renderCombinedSection(container, m, sectionId, includeKey) {
  const sec = findCombinedSection(m, sectionId);
  if (!sec) return renderIndex(container, sectionId);
  // componentPapers like ["moji-1", "goi-1"]
  const components = await Promise.all(sec.componentPapers.map(async id => {
    const sp = splitPaperId(id);
    if (!sp) return null;
    const paper = await loadPaperByCategoryNumber(sp.category, sp.number);
    const cat = (m.categories || []).find(c => c.id === sp.category) || { label: sp.category, label_ja: '' };
    const pmeta = (cat.papers || []).find(p => p.id === id) || {};
    return {
      label_ja: cat.label_ja,
      label_en: cat.label,
      questions: paper.questions,
      duration_min: pmeta.expectedDurationMin || null,
    };
  }));
  const sections = components.filter(Boolean);
  const cover = {
    name_en: sec.name_en,
    name_ja: sec.name_ja,
    total_q: sec.questionCount,
    duration_min: sec.expectedDurationMin,
    instructions: defaultInstructions('combined'),
  };
  return renderPrintShell(container, sec.id, cover, sections, includeKey);
}

// ---------- Full mock paper ----------

async function renderFullMock(container, m, mockId, includeKey) {
  const fm = findFullMock(m, mockId);
  if (!fm) return renderIndex(container, mockId);
  const sections = [];
  for (const sectionId of fm.sections) {
    if (/^genngo-chishiki/.test(sectionId)) {
      const sec = findCombinedSection(m, sectionId);
      if (!sec) continue;
      for (const compId of sec.componentPapers) {
        const sp = splitPaperId(compId);
        if (!sp) continue;
        const paper = await loadPaperByCategoryNumber(sp.category, sp.number);
        const cat = (m.categories || []).find(c => c.id === sp.category) || { label: sp.category, label_ja: '' };
        sections.push({
          label_ja: cat.label_ja,
          label_en: cat.label,
          questions: paper.questions,
          duration_min: null,
        });
      }
    } else if (/^chokai-\d+/.test(sectionId)) {
      const vp = findVirtualPaper(m, sectionId.replace(/-virtual$/, ''));
      if (vp) {
        sections.push({
          label_ja: '聴解',
          label_en: 'Listening',
          questions: chokaiQuestionsFromVirtual(vp),
          duration_min: vp.expectedDurationMin || null,
          is_chokai: true,
          source_listening_ids: vp.source_listening_ids || [],
        });
      }
    }
  }
  const cover = {
    name_en: fm.name_en,
    name_ja: fm.name_ja,
    total_q: fm.totalQuestions,
    duration_min: fm.totalDurationMin,
    instructions: defaultInstructions('full-mock'),
  };
  return renderPrintShell(container, fm.id, cover, sections, includeKey);
}

// ---------- Chokai virtual paper (listening) ----------

async function renderChokai(container, m, paperId, includeKey) {
  const id = paperId.replace(/-virtual$/, '');
  const vp = findVirtualPaper(m, id);
  if (!vp) return renderIndex(container, paperId);
  const cover = {
    name_en: `${vp.name} (script)`,
    name_ja: vp.label_ja,
    total_q: vp.questionCount,
    duration_min: vp.expectedDurationMin || null,
    instructions: defaultInstructions('chokai'),
  };
  const sections = [{
    label_ja: '聴解',
    label_en: 'Listening',
    questions: chokaiQuestionsFromVirtual(vp),
    duration_min: vp.expectedDurationMin || null,
    is_chokai: true,
    source_listening_ids: vp.source_listening_ids || [],
  }];
  return renderPrintShell(container, vp.id, cover, sections, includeKey);
}

// Lazy-load listening.json on first chokai render so the printed paper
// can include the script + question text. Listening is the only place
// where the question stem is prerecorded audio rather than written;
// for printing, we substitute the script_ja text. The audio itself is
// of course not in print — but the printed paper includes a "play
// online" hint.
let _listeningCache = null;
async function loadListening() {
  if (_listeningCache) return _listeningCache;
  const r = await fetch('data/listening.json');
  _listeningCache = r.ok ? await r.json() : { items: [] };
  return _listeningCache;
}

// Build a shaped questions[] array from a chokai virtual-paper id list.
// Each question has stem_html (from script_ja), choices, correctIndex,
// rationale (from explanation_*), id, mondai. Async wrapper not needed
// since we eagerly resolve listening before calling.
function chokaiQuestionsFromVirtual(vp) {
  // Note: vp doesn't have the question text inline; we look them up
  // from listening.json. Returns a *promise-like* placeholder — the
  // actual fill happens in renderPrintShell (which is async-aware
  // via the listening cache).
  return vp.source_listening_ids.map((lid, i) => ({
    _chokai_listen_id: lid,
    id: `${vp.id}-${i + 1}`,
    mondai: null,  // resolved via listening.json item
    type: 'mcq',
    stem_html: '',        // filled at render time
    choices: [],          // filled at render time
    correctIndex: 0,
    rationale: '',
  }));
}

// ---------- Render shell (the actual page layout) ----------

async function renderPrintShell(container, paperId, cover, sections, includeKey) {
  // Resolve any chokai placeholders.
  const hasChokai = sections.some(s => s.is_chokai);
  if (hasChokai) {
    const listening = await loadListening();
    const itemMap = new Map((listening.items || []).map(it => [it.id, it]));
    sections.forEach(s => {
      if (!s.is_chokai) return;
      s.questions = s.questions.map(q => {
        const it = itemMap.get(q._chokai_listen_id);
        if (!it) return { ...q, stem_html: '(listening item not found: ' + esc(q._chokai_listen_id) + ')' };
        const correctIdx = (it.choices || []).findIndex(c => c === it.correctAnswer);
        return {
          ...q,
          mondai: it.mondai || null,
          stem_html: chokaiStemHtml(it),
          choices: it.choices || [],
          correctIndex: correctIdx >= 0 ? correctIdx : 0,
          rationale: it.explanation_ja || it.explanation_en || '',
        };
      });
    });
  }

  // Group questions per-section by mondai for clean cuts.
  const renderedSections = sections.map(s => {
    const groups = groupByMondai(s.questions);
    const groupHtml = groups.map(g => `
      <section class="print-mondai">
        <header class="print-mondai-header">
          <h3>${mondaiLabel(s, g.mondai)}</h3>
          ${mondaiInstructions(s, g.mondai)}
        </header>
        <ol class="print-q-list">
          ${g.questions.map(q => renderQuestion(q, s.is_chokai)).join('')}
        </ol>
      </section>
    `).join('');
    return `
      <section class="print-section">
        <header class="print-section-header">
          <h2 lang="ja">${esc(s.label_ja || '')}</h2>
          <p class="print-section-meta">${esc(s.label_en || '')}${s.duration_min ? ` · ${s.duration_min} min` : ''} · ${s.questions.length} questions</p>
        </header>
        ${groupHtml}
      </section>
    `;
  }).join('');

  const keyHtml = includeKey ? renderAnswerKey(sections) : '';

  container.innerHTML = `
    <article class="print-paper-screen">
      <header class="print-paper-toolbar">
        <a class="back-link" href="#/print">← Print index</a>
        <span class="print-paper-toolbar-actions">
          <a class="btn-secondary" href="#/print/${esc(paperId)}${includeKey ? '' : '?key=1'}">${includeKey ? 'Hide answer key' : '+ Answer key'}</a>
          <button class="btn-primary" id="print-paper-now-btn" type="button">Print / Save PDF</button>
        </span>
      </header>

      <article class="print-paper-root" lang="ja">
        ${renderWatermark()}
        ${renderCover(cover)}
        ${renderedSections}
        ${keyHtml}
        <footer class="print-paper-footer">
          <p class="print-paper-source">${esc(cover.name_en)} · JLPTSuccess · gauravaccentureproducts.github.io/JLPTSuccess</p>
        </footer>
      </article>

      <p class="muted small print-paper-hint">Tip: Browser <strong>Print</strong> dialog has a "Save as PDF" destination. Use that to keep an offline copy without using paper. Each printed page carries a faint <strong>JLPTSUCCESS.COM</strong> watermark — readability of the questions is unaffected; the watermark deters resale of printed copies.</p>
    </article>
  `;

  // Render Japanese text with furigana overlay where applicable.
  // (renderJa walks text nodes; safe to skip for now if it's not
  // available — print is still legible.)
  try { if (typeof renderJa === 'function') renderJa(container); } catch (_) {}

  const btn = container.querySelector('#print-paper-now-btn');
  if (btn) {
    btn.addEventListener('click', () => window.print());
  }
}

// ---------- Render helpers ----------

// Tiled "JLPTSUCCESS.COM" watermark behind every printed page.
//
// Why an inline SVG with <pattern>+<rect>:
//   - Foreground SVG content prints reliably regardless of the user's
//     "Background graphics" toggle in the print dialog. A CSS
//     background-image would not — many browsers strip those by default.
//   - The <pattern> repeats deterministically, so the same logo grid
//     appears on every page when the wrapper is fixed-positioned in
//     @media print.
//   - rotate(-28) on the text plus letter-spacing gives the classic
//     diagonal watermark look without needing a logo image asset.
//
// Readability protection:
//   - fill-opacity 0.06 sits well below the contrast threshold for
//     interfering with body text (which is full-black at 11pt).
//   - The wrapper has pointer-events:none + user-select:none so the
//     watermark can never block clicks or text selection on screen.
//   - z-index management (CSS) puts every content child on z-index 1
//     so the watermark stays strictly behind cover / questions / key.
//
// Tile geometry:
//   280 x 160 px tile, one logo per tile, rotated -28deg from horizontal.
//   At a typical A4 print canvas (~794x1123px @ 96dpi minus 2cm margins
//   ≈ 670x973), that yields ~3 columns x ~6 rows = ~18 watermarks per
//   page. Dense enough to be unmistakable, sparse enough that any 2cm
//   patch of paper has only one watermark visible.
function renderWatermark() {
  return `
    <div class="print-paper-watermark" aria-hidden="true">
      <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
        <defs>
          <pattern id="jlpts-watermark" x="0" y="0" width="280" height="160" patternUnits="userSpaceOnUse">
            <text x="140" y="86"
                  font-family="Helvetica, Arial, sans-serif"
                  font-size="16"
                  font-weight="700"
                  fill="#000"
                  fill-opacity="0.06"
                  letter-spacing="2"
                  text-anchor="middle"
                  transform="rotate(-28 140 86)">JLPTSUCCESS.COM</text>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#jlpts-watermark)" />
      </svg>
    </div>
  `;
}

function renderCover(c) {
  return `
    <header class="print-paper-cover">
      <p class="print-paper-brand">JLPTSuccess · JLPT N5</p>
      <h1 class="print-paper-title" lang="ja">${esc(c.name_ja || c.name_en || '')}</h1>
      ${c.name_en && c.name_en !== c.name_ja ? `<p class="print-paper-title-en">${esc(c.name_en)}</p>` : ''}
      <dl class="print-paper-cover-meta">
        <dt>Questions</dt><dd>${c.total_q}</dd>
        ${c.duration_min ? `<dt>Time allowed</dt><dd>${c.duration_min} min</dd>` : ''}
        <dt>Date</dt><dd class="print-paper-fillable">________________</dd>
        <dt>Name</dt><dd class="print-paper-fillable">________________________________</dd>
      </dl>
      <section class="print-paper-instructions">
        <h2>Instructions</h2>
        ${c.instructions}
      </section>
    </header>
  `;
}

function defaultInstructions(kind) {
  const common = `
    <ol>
      <li>Write your name and the date in the spaces above.</li>
      <li>Read each question carefully and circle <strong>one</strong> answer per question.</li>
      <li>Do not write outside the answer area; erasers are permitted.</li>
      <li>If you change your mind, cross out the wrong answer cleanly and circle your new choice.</li>
    </ol>
  `;
  switch (kind) {
    case 'full-mock':
      return `
        <p>This is a 105-minute, three-section mock paper modelled on the real JLPT N5 sitting.</p>
        ${common}
        <p><strong>Section timing:</strong> 25 min for 言語知識（文字・語彙）, 50 min for 言語知識（文法）・読解, 30 min for 聴解. Take a brief stretch between sections; do <strong>not</strong> exceed total 105 min.</p>
      `;
    case 'chokai':
      return `
        <p>This is a printed transcript of a listening section. The audio is not on paper — play it from your phone or computer while marking answers here.</p>
        ${common}
        <p><strong>Audio source:</strong> on the JLPTSuccess web app, open the Listening tab and play the items in order. Each item is read once at JLPT-N5 pace.</p>
      `;
    case 'combined':
      return `
        <p>This is a combined-section paper. Time yourself for the full section; do <strong>not</strong> pause between sub-sections.</p>
        ${common}
      `;
    default:
      return common;
  }
}

function groupByMondai(qs) {
  const buckets = new Map();
  qs.forEach(q => {
    const k = q.mondai == null ? 0 : q.mondai;
    if (!buckets.has(k)) buckets.set(k, []);
    buckets.get(k).push(q);
  });
  return [...buckets.entries()].sort((a, b) => a[0] - b[0]).map(([mondai, questions]) => ({ mondai, questions }));
}

function mondaiLabel(s, m) {
  if (!m) return s.label_ja || s.label_en || 'Questions';
  // JLPT-canonical mondai labels per section.
  const cat = (s.label_en || '').toLowerCase();
  const labels = {
    moji:  ['', '問題1 漢字読み', '問題2 表記', '問題3 文脈規定', '問題4 言い換え', '問題5 用法'],
    goi:   ['', '問題1 文脈規定', '問題2 言い換え類義', '問題3 用法', '問題4', '問題5'],
    bunpou:['', '問題1 文の文法 (1)', '問題2 文の文法 (2) (並べ替え)', '問題3 文章の文法'],
    dokkai:['', '問題4 内容理解 (短文)', '問題5 内容理解 (中文)', '問題6 情報検索'],
    listening:['', '問題1 課題理解', '問題2 ポイント理解', '問題3 発話表現', '問題4 即時応答'],
  };
  const arr = labels[cat] || labels[s.label_en && s.label_en.toLowerCase()] || null;
  if (arr && arr[m]) return `<span lang="ja">${esc(arr[m])}</span>`;
  return `<span lang="ja">問題${m}</span>`;
}

function mondaiInstructions(s, m) {
  // Light, JLPT-canonical mondai-specific framing where it helps the
  // pencil-and-paper version. Many mondai don't need extra text;
  // return empty for those.
  const cat = (s.label_en || '').toLowerCase();
  const map = {
    'moji-1': '<p class="print-mondai-instr" lang="ja">_____ のことばの よみかたを えらんでください。</p>',
    'moji-2': '<p class="print-mondai-instr" lang="ja">_____ のことばを かんじで かいてあるのは どれですか。</p>',
    'goi-1':  '<p class="print-mondai-instr" lang="ja">(  ) に なにを いれますか。いちばん いいものを えらんでください。</p>',
    'bunpou-1': '<p class="print-mondai-instr" lang="ja">(  ) に なにを いれますか。いちばん いいものを えらんでください。</p>',
    'bunpou-2': '<p class="print-mondai-instr" lang="ja">_★_ に はいる ものは どれですか。1・2・3・4 から いちばん いい ものを えらんでください。</p>',
    'dokkai-4': '<p class="print-mondai-instr" lang="ja">つぎの 文を よんで、しつもんに こたえてください。</p>',
    'dokkai-6': '<p class="print-mondai-instr" lang="ja">つぎの ページを 見て、しつもんに こたえてください。</p>',
    'listening-1': '<p class="print-mondai-instr" lang="ja">問題1: 二人の話を聞いて、男の人 (女の人) は次に何をしますか。1・2・3・4 から、いちばん いいものを えらんでください。</p>',
    'listening-3': '<p class="print-mondai-instr" lang="ja">問題3: 場面を見ながら矢印 (→) の人は何と言いますか。1・2・3 から、いちばん いいものを えらんでください。</p>',
    'listening-4': '<p class="print-mondai-instr" lang="ja">問題4: 文を聞いて、それに対する答えとして、いちばん いいものを えらんでください。</p>',
  };
  return map[`${cat}-${m}`] || '';
}

function renderQuestion(q, isChokai) {
  const stem = String(q.stem_html || q.prompt_html || q.prompt_ja || '').trim();
  const choices = q.choices || [];
  const choiceHtml = choices.map((ch, i) => `
    <li class="print-choice">
      <span class="print-choice-num">${circleNum(i + 1)}</span>
      <span class="print-choice-text" lang="ja">${esc(ch)}</span>
    </li>
  `).join('');
  return `
    <li class="print-q" id="print-q-${esc(q.id || '')}">
      <header class="print-q-header">
        <span class="print-q-id muted small">${esc(q.id || '')}</span>
        ${isChokai ? '<span class="print-q-audio-hint muted small">(audio plays once)</span>' : ''}
      </header>
      <div class="print-q-stem" lang="ja">${stem}</div>
      <ol class="print-q-choices">${choiceHtml}</ol>
    </li>
  `;
}

function chokaiStemHtml(item) {
  // Rendered listening item: prompt_ja + script_ja.
  // For pencil-and-paper, we do print the script (which on the audio
  // version the learner only hears). This is the "follow along while
  // audio plays" use case; advanced learners may choose not to look
  // and only mark answers from audio.
  const prompt = item.prompt_ja || '';
  const script = item.script_ja || '';
  return `
    <p class="print-chokai-prompt"><strong>${esc(item.title_ja || item.id || '')}</strong> &nbsp; ${esc(prompt)}</p>
    <pre class="print-chokai-script">${esc(script)}</pre>
  `;
}

function renderAnswerKey(sections) {
  const groups = sections.map(s => {
    const rows = s.questions.map(q => {
      const correct = circleNum((q.correctIndex || 0) + 1);
      const choice = (q.choices || [])[q.correctIndex || 0] || '';
      const rationale = (q.rationale || '').trim();
      return `
        <li>
          <span class="print-key-id">${esc(q.id || '')}</span>
          <span class="print-key-correct">${correct}</span>
          <span class="print-key-text" lang="ja">${esc(choice)}</span>
          ${rationale ? `<p class="print-key-why muted small" lang="ja">${esc(rationale)}</p>` : ''}
        </li>
      `;
    }).join('');
    return `
      <section class="print-key-section">
        <h3>${esc(s.label_en || s.label_ja || 'Section')}</h3>
        <ol class="print-key-list">${rows}</ol>
      </section>
    `;
  }).join('');
  return `
    <section class="print-key" aria-labelledby="print-key-h">
      <h2 id="print-key-h">Answer key</h2>
      <p class="muted small">Cut along this line before handing the paper to a learner; or print without the answer key by removing <code>?key=1</code> from the URL.</p>
      ${groups}
    </section>
  `;
}

// ---------- Tiny utilities ----------

function circleNum(n) {
  // Render 1..9 as ① ② ③ etc., 10..20 as plain.
  const m = ['', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨'];
  return m[n] || String(n);
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
