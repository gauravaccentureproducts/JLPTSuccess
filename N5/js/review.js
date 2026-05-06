// Chapter 3 - Review (SM-2 SRS session per Brief §2.11).
// Surfaces grammar patterns due today (SM-2 nextDue ≤ now), plus up to N new
// items each day. Each card presents the pattern + a question; user grades
// 4-button (Again / Hard / Good / Easy); algorithm advances the schedule.
import { renderJa } from './furigana.js';
import * as storage from './storage.js';
import { t } from './i18n.js';

const NEW_PER_DAY_DEFAULT = 10;
const REVIEW_CAP_DEFAULT = 50;

let session = null;
let view = 'setup';

let grammarIndex = null;
let questionIndex = null; // pid -> [questions]
// IMP-092 Phase 2B (audit round-9, 2026-05-07): vocab + kanji indexes
// for the unified review session. Loaded lazily alongside grammar.
let vocabIndex = null;    // form -> entry
let vocabByIdIndex = null; // id   -> entry
let kanjiIndex = null;    // glyph -> entry

async function loadData() {
  if (grammarIndex && questionIndex && vocabIndex && kanjiIndex) return;
  const [g, q, v, k] = await Promise.all([
    fetch('data/grammar.json').then(r => r.json()),
    fetch('data/questions.json').then(r => r.json()),
    fetch('data/vocab.json').then(r => r.json()),
    fetch('data/kanji.json').then(r => r.json()),
  ]);
  grammarIndex = new Map((g.patterns || []).map(p => [p.id, p]));
  questionIndex = new Map();
  for (const qq of q.questions || []) {
    if (!questionIndex.has(qq.grammarPatternId)) questionIndex.set(qq.grammarPatternId, []);
    questionIndex.get(qq.grammarPatternId).push(qq);
  }
  vocabIndex = new Map();
  vocabByIdIndex = new Map();
  for (const e of (v.entries || [])) {
    if (e.form) vocabIndex.set(e.form, e);
    if (e.id) vocabByIdIndex.set(e.id, e);
  }
  kanjiIndex = new Map((k.entries || []).map(e => [e.glyph, e]));
}

function getDueItems(limit) {
  const history = storage.getHistory();
  const now = new Date();
  const due = [];
  for (const [pid, e] of Object.entries(history)) {
    // Skip graduated / manually-known if interval is huge - they won't be due naturally
    if (e.isMastered) continue;
    if (e.nextDue && new Date(e.nextDue) <= now) due.push({ pid, entry: e, isNew: false });
  }
  // Sort: oldest due first (lowest nextDue)
  due.sort((a, b) => new Date(a.entry.nextDue) - new Date(b.entry.nextDue));
  return due.slice(0, limit);
}

function getNewItems(limit, alreadyIncluded) {
  const history = storage.getHistory();
  const seen = new Set([...alreadyIncluded.map(x => x.pid), ...Object.keys(history)]);
  const out = [];
  // Walk all authored grammar patterns in order, take ones never seen
  for (const [pid] of grammarIndex) {
    if (seen.has(pid)) continue;
    if (out.length >= limit) break;
    out.push({ pid, entry: null, isNew: true });
  }
  return out;
}

export async function renderReview(container) {
  await loadData();
  // Stale 'finished' state reset: if the user completed a review session,
  // navigated away, and clicked "Review" again, give them a fresh setup
  // (not last session's score card). Mid-session ('session' state) IS
  // preserved so the user can resume.
  if (view === 'finished') {
    view = 'setup';
    session = null;
  }
  if (view === 'session' && session) return renderCard(container);
  if (view === 'finished' && session) return renderFinished(container);
  return renderSetup(container);
}

function renderSetup(container) {
  view = 'setup';
  const settings = storage.getSettings();
  const newPerDay = settings.dailyNewLimit ?? NEW_PER_DAY_DEFAULT;
  const cap = settings.dailyReviewCap ?? REVIEW_CAP_DEFAULT;
  const dueItems = getDueItems(cap);
  const newItems = getNewItems(newPerDay, dueItems);

  // IMP-092 Phase 2A (audit round-9, 2026-05-07): surface the unified
  // due-counts across grammar+vocab+kanji on the review setup page,
  // matching the design brief's "47 reviews due today (12 grammar ·
  // 23 vocab · 12 kanji)" pattern. Phase 2B (full unified card-render
  // routing by skill) is queued separately; the current session stays
  // grammar-only until the card-render rewrite ships.
  const dueBySkill = storage.getDueCountsBySkill();
  const unifiedDueTotal = dueBySkill.grammar + dueBySkill.vocab + dueBySkill.kanji;

  container.innerHTML = `
    <h2>${t('page.review')}</h2>
    <p>Spaced-repetition session using the SM-2 algorithm. Items reappear at intervals that grow as you grade them correctly and shrink when you miss.</p>

    ${unifiedDueTotal > 0 ? `
      <!-- IMP-092 Phase 2A: unified daily review aggregate -->
      <section class="srs-unified-summary" aria-label="Today's reviews across all skills">
        <h3 style="margin:0 0 8px; font-weight:500;">Today: <strong>${unifiedDueTotal}</strong> review${unifiedDueTotal === 1 ? '' : 's'} due across all skills</h3>
        <p class="muted small" style="margin:0 0 12px;">
          ${dueBySkill.grammar} grammar · ${dueBySkill.vocab} vocab · ${dueBySkill.kanji} kanji
          <span style="margin-left:8px;">(see <a href="#/summary">Progress dashboard</a> for forecast)</span>
        </p>
        <p class="muted small" style="margin:0;">
          The session below covers <strong>grammar reviews only</strong> for now. Vocab and kanji reviews surface on their respective Learn pages until the unified card render ships (IMP-092 Phase 2B).
        </p>
      </section>
    ` : ''}

    <section class="srs-stats">
      <div class="stat-card weak">
        <div class="stat-num">${dueItems.length}</div>
        <div class="stat-label">Grammar due</div>
        <div class="stat-hint">SRS scheduled</div>
      </div>
      <div class="stat-card neutral">
        <div class="stat-num">${newItems.length}</div>
        <div class="stat-label">New grammar</div>
        <div class="stat-hint">never reviewed</div>
      </div>
      <div class="stat-card mastered">
        <div class="stat-num">${dueItems.length + newItems.length}</div>
        <div class="stat-label">Session size</div>
      </div>
    </section>

    <p class="muted small">Configure daily new-card limit and review cap in Settings.</p>

    ${dueItems.length + newItems.length > 0 ? `
      <button id="srs-start" class="btn-primary">Start review session</button>
    ` : (Object.keys(storage.getHistory()).length === 0 ? `
      <div class="empty-state">
        <p><strong>Reviews appear here after you finish your first lesson.</strong></p>
        <p class="muted small">SM-2 spaced repetition starts as soon as you've grade-rated a few patterns.</p>
        <p><a href="#/learn" class="btn-primary" style="text-decoration:none">Go to Learn</a></p>
      </div>
    ` : `
      <div class="empty-state">
        <p><strong>No reviews due right now.</strong> Come back later, or start a new lesson.</p>
        <p><a href="#/learn" class="btn-primary" style="text-decoration:none">Go to Learn</a></p>
      </div>
    `)}
  `;

  document.getElementById('srs-start')?.addEventListener('click', () => {
    // IMP-092 Phase 2B: build the unified queue. Grammar new items still
    // come from getNewItems (since vocab/kanji new-card admission is
    // configured separately and is currently 0/day by default — they
    // enter the SRS via Mark-as-known). The unified queue function
    // covers due-only across all three skills.
    const grammarItemsAsUnified = [...dueItems, ...newItems].map(it => ({
      skill: 'grammar',
      id: it.pid,
      entry: it.entry,
      isNew: it.isNew,
    }));
    // Pull due vocab + kanji from the unified queue and merge round-robin
    const allUnified = storage.getUnifiedDueQueue ? storage.getUnifiedDueQueue() : [];
    const nonGrammarUnified = allUnified.filter(it => it.skill !== 'grammar');
    // Round-robin interleave grammar-with-news + non-grammar
    const queue = [];
    const buckets = [grammarItemsAsUnified, nonGrammarUnified];
    while (buckets.some(b => b.length > 0)) {
      for (const b of buckets) {
        if (b.length > 0) queue.push(b.shift());
      }
    }
    session = {
      queue,
      idx: 0,
      grades: [],
      startedAt: new Date().toISOString(),
    };
    view = 'session';
    renderCard(container);
  });
}

function renderCard(container) {
  const item = session.queue[session.idx];
  if (!item) return renderFinished(container);

  // IMP-092 Phase 2B: legacy items use `pid`; unified items use
  // `{skill, id}`. Default to grammar for backward compatibility.
  const skill = item.skill || 'grammar';
  const itemId = item.id || item.pid;
  const total = session.queue.length;

  // Card-type indicator badge — shows in the progress row
  const SKILL_BADGES = {
    grammar: { label: '文', cls: 'srs-skill-grammar', name: 'Grammar' },
    vocab:   { label: '語', cls: 'srs-skill-vocab',   name: 'Vocab'   },
    kanji:   { label: '漢', cls: 'srs-skill-kanji',   name: 'Kanji'   },
  };
  const badge = SKILL_BADGES[skill] || SKILL_BADGES.grammar;

  // Skill-specific card body
  let cardBody = '';
  let detailHref = `#/learn/${encodeURIComponent(itemId)}`;
  if (skill === 'grammar') {
    const pattern = grammarIndex.get(itemId);
    if (!pattern) { advance(container, 3); return; }
    const examples = (pattern.examples || []).filter(ex => ex.ja && !ex.ja.includes('(see '));
    const example = examples[0];
    const meaning = pattern.meaning_en || '';
    cardBody = `
      <h3 class="pattern-name">${renderJa(pattern.pattern)}</h3>
      <p class="meaning-en">${esc(meaning)}</p>
      ${example ? `
        <div class="srs-example">
          <p>${renderJa(example.ja, example.furigana || [])}</p>
          ${example.translation_en ? `<p class="muted small">${esc(example.translation_en)}</p>` : ''}
        </div>
      ` : ''}
      ${pattern.explanation_en ? `<p class="srs-explanation">${esc(pattern.explanation_en)}</p>` : ''}
    `;
  } else if (skill === 'vocab') {
    // Look up by id first (unified queue), fall back to form.
    const entry = (vocabByIdIndex && vocabByIdIndex.get(itemId))
      || (vocabIndex && vocabIndex.get(itemId));
    if (!entry) { advance(container, 3); return; }
    const exampleSentence = (entry.examples && entry.examples[0]) || null;
    cardBody = `
      <h3 class="pattern-name" lang="ja">${esc(entry.form || '')}</h3>
      <p class="meaning-en"><span lang="ja" class="vocab-reading">${esc(entry.reading || '')}</span>
        ${entry.pos ? `<span class="muted small" style="margin-left:8px;">${esc(entry.pos)}</span>` : ''}</p>
      <p class="meaning-en"><strong>${esc(entry.gloss || '')}</strong></p>
      ${entry.gloss_hi ? `<p class="muted small" lang="hi">${esc(entry.gloss_hi)}</p>` : ''}
      ${exampleSentence ? `
        <div class="srs-example">
          <p lang="ja">${esc(exampleSentence.ja || exampleSentence)}</p>
          ${exampleSentence.translation_en ? `<p class="muted small">${esc(exampleSentence.translation_en)}</p>` : ''}
        </div>
      ` : ''}
      ${entry.collocations && entry.collocations.length ? `
        <p class="muted small">Collocations: <span lang="ja">${entry.collocations.slice(0, 3).map(esc).join(' · ')}</span></p>
      ` : ''}
    `;
    detailHref = entry.form ? `#/learn/vocab/${encodeURIComponent(entry.form)}` : '#/learn/vocab';
  } else if (skill === 'kanji') {
    const entry = kanjiIndex && kanjiIndex.get(itemId);
    if (!entry) { advance(container, 3); return; }
    cardBody = `
      <h3 class="pattern-name kanji-glyph-big" lang="ja" style="font-size:5em; line-height:1;">${esc(entry.glyph)}</h3>
      ${entry.on?.length ? `<p class="meaning-en"><strong>On:</strong> <span lang="ja">${entry.on.map(esc).join(' / ')}</span></p>` : ''}
      ${entry.kun?.length ? `<p class="meaning-en"><strong>Kun:</strong> <span lang="ja">${entry.kun.map(esc).join(' / ')}</span></p>` : ''}
      ${entry.meanings?.length ? `<p class="meaning-en"><strong>Meaning:</strong> ${entry.meanings.map(esc).join(', ')}</p>` : ''}
      ${entry.meanings_hi?.length ? `<p class="muted small" lang="hi">${entry.meanings_hi.map(esc).join(', ')}</p>` : ''}
      ${entry.mnemonic ? `<p class="srs-explanation">${esc(entry.mnemonic)}</p>` : ''}
    `;
    detailHref = `#/kanji/${encodeURIComponent(entry.glyph)}`;
  }

  container.innerHTML = `
    <div class="srs-card">
      <div class="srs-progress">
        <span>Review · Card <strong>${session.idx + 1}</strong> of <strong>${total}</strong></span>
        <span class="srs-skill-badge ${badge.cls}" title="${badge.name}" lang="ja">${badge.label}</span>
        ${item.isNew ? '<span class="srs-tag new">NEW</span>' : ''}
      </div>
      <article class="srs-content">
        ${cardBody}
      </article>

      <div class="srs-grade-row">
        <p class="muted small">Grade your recall:</p>
        <div class="srs-grade-buttons">
          <button class="grade-btn grade-again" data-grade="1">
            <span class="grade-label">Again</span>
            <span class="grade-hint">Forgot it</span>
          </button>
          <button class="grade-btn grade-hard" data-grade="3">
            <span class="grade-label">Hard</span>
            <span class="grade-hint">Correct but difficult</span>
          </button>
          <button class="grade-btn grade-good" data-grade="4">
            <span class="grade-label">Good</span>
            <span class="grade-hint">Correct, normal</span>
          </button>
          <button class="grade-btn grade-easy" data-grade="5">
            <span class="grade-label">Easy</span>
            <span class="grade-hint">Trivially correct</span>
          </button>
        </div>
      </div>

      <div class="test-nav">
        <button id="srs-end">End session</button>
        <a href="${detailHref}" class="srs-link">View full lesson →</a>
      </div>
    </div>
  `;

  container.querySelectorAll('[data-grade]').forEach(btn => {
    btn.addEventListener('click', () => {
      const grade = parseInt(btn.dataset.grade, 10);
      // IMP-092 Phase 2B: skill-aware grade recording. Routes to
      // recordUnifiedSrsResponse which writes to the right history map
      // (grammar / vocab / kanji). Falls back to grammar-only behavior
      // for legacy items missing item.skill.
      const useUnified = item.skill && storage.recordUnifiedSrsResponse;
      const snapshot = useUnified
        ? storage.recordUnifiedSrsResponse(skill, itemId, grade)
        : storage.recordSrsResponse(itemId, grade);
      session.grades.push({ skill, pid: itemId, grade, snapshot });
      advance(container, grade, { lastGraded: { skill, pid: itemId, grade, snapshot, isUnified: useUnified } });
    });
  });

  document.getElementById('srs-end')?.addEventListener('click', () => {
    view = 'finished';
    renderFinished(container);
  });
}

function advance(container, _grade, opts = {}) {
  session.idx += 1;
  if (session.idx >= session.queue.length) {
    view = 'finished';
    renderFinished(container);
  } else {
    renderCard(container);
    // After the next card has rendered, mount a transient 2s-undo toast
    // referring to the GRADE WE JUST RECORDED. Clicking it rolls the
    // last grade back via storage.undoSrsResponse, removes it from
    // session.grades, and dismisses the toast. Auto-dismisses at 2s.
    if (opts.lastGraded) {
      mountUndoToast(container, opts.lastGraded);
    }
  }
}

// 2-second undo toast for DEFER-14. Single-instance: any prior toast is
// torn down before a new one mounts. The toast button is a real focus
// target for keyboard users; auto-dismiss timer is cleared on hover.
let undoTimer = null;
function mountUndoToast(container, lastGraded) {
  const existing = document.getElementById('undo-grade-toast');
  if (existing) existing.remove();
  if (undoTimer) { clearTimeout(undoTimer); undoTimer = null; }

  const GRADE_LABELS = { 1: 'Again', 3: 'Hard', 4: 'Good', 5: 'Easy' };
  const label = GRADE_LABELS[lastGraded.grade] || `Grade ${lastGraded.grade}`;

  const toast = document.createElement('div');
  toast.id = 'undo-grade-toast';
  toast.className = 'undo-toast';
  toast.setAttribute('role', 'status');
  toast.setAttribute('aria-live', 'polite');
  toast.innerHTML = `
    <span class="undo-toast-text">Recorded: <strong>${label}</strong></span>
    <button type="button" class="undo-toast-btn" id="undo-grade-btn">↶ Undo</button>
  `;
  document.body.appendChild(toast);

  // Roll back on click. Removes the just-recorded grade from the
  // session log AND restores storage to the pre-grade snapshot.
  document.getElementById('undo-grade-btn').addEventListener('click', () => {
    // IMP-092 Phase 2B: skill-aware undo. Falls back to grammar-only
    // for legacy items.
    const ok = lastGraded.isUnified && storage.undoUnifiedSrsResponse
      ? storage.undoUnifiedSrsResponse(lastGraded.skill, lastGraded.pid, lastGraded.snapshot)
      : storage.undoSrsResponse(lastGraded.pid, lastGraded.snapshot);
    if (ok) {
      // Pop the last grade entry from the session log so the finished
      // screen + summary stats stay in sync with storage.
      const idx = session.grades.findIndex(g =>
        g.pid === lastGraded.pid && g.grade === lastGraded.grade);
      if (idx >= 0) session.grades.splice(idx, 1);
    }
    teardownUndoToast();
  });

  // Pause the auto-dismiss while the user hovers over the toast - gives
  // people on slow reading speed a chance to react.
  toast.addEventListener('mouseenter', () => {
    if (undoTimer) { clearTimeout(undoTimer); undoTimer = null; }
  });
  toast.addEventListener('mouseleave', () => {
    if (!undoTimer) undoTimer = setTimeout(teardownUndoToast, 2000);
  });

  undoTimer = setTimeout(teardownUndoToast, 2000);
}

function teardownUndoToast() {
  if (undoTimer) { clearTimeout(undoTimer); undoTimer = null; }
  const t = document.getElementById('undo-grade-toast');
  if (t) t.remove();
}

function renderFinished(container) {
  const counts = { 1: 0, 3: 0, 4: 0, 5: 0 };
  for (const g of session.grades) counts[g.grade] = (counts[g.grade] || 0) + 1;
  const total = session.grades.length;

  // Per-pattern next-due summary
  const summary = session.grades.map(({ pid, grade }) => {
    const p = grammarIndex.get(pid);
    const e = storage.getSrsState(pid);
    return {
      label: p?.pattern || pid,
      grade,
      nextDue: e?.nextDue,
      interval: e?.interval,
    };
  });

  container.innerHTML = `
    <div class="srs-finished">
      <h2>Review complete</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${total}</div><div class="stat-label">Total cards</div></div>
        <div class="stat-card weak"><div class="stat-num">${counts[1]}</div><div class="stat-label">Again</div></div>
        <div class="stat-card neutral"><div class="stat-num">${counts[3] + counts[4]}</div><div class="stat-label">Hard / Good</div></div>
        <div class="stat-card mastered"><div class="stat-num">${counts[5]}</div><div class="stat-label">Easy</div></div>
      </section>

      <h3>Schedule</h3>
      <ul class="srs-schedule">
        ${summary.map(s => `
          <li>
            <span lang="ja"><strong>${esc(s.label)}</strong></span>
            <span class="muted small">grade ${s.grade}, next in ${s.interval}d (${s.nextDue ? new Date(s.nextDue).toLocaleDateString() : '-'})</span>
          </li>
        `).join('')}
      </ul>

      <div class="test-nav">
        <button id="srs-restart" class="btn-primary">Start new session</button>
        <button id="srs-back">Back to Learn</button>
      </div>
    </div>
  `;

  document.getElementById('srs-restart')?.addEventListener('click', () => {
    session = null;
    view = 'setup';
    renderSetup(container);
  });
  document.getElementById('srs-back')?.addEventListener('click', () => {
    location.hash = '#/learn';
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
