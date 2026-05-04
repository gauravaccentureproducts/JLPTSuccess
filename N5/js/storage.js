// LocalStorage adapter - namespaced per spec FR-P4.
const NS = 'jlpt-n5-tutor:';

export function get(key, fallback = null) {
  const raw = localStorage.getItem(NS + key);
  if (raw === null) return fallback;
  try { return JSON.parse(raw); } catch { return fallback; }
}

export function set(key, value) {
  localStorage.setItem(NS + key, JSON.stringify(value));
}

export function remove(key) {
  localStorage.removeItem(NS + key);
}

export function reset() {
  Object.keys(localStorage)
    .filter(k => k.startsWith(NS))
    .forEach(k => localStorage.removeItem(k));
}

const DEFAULT_SETTINGS = {
  furiganaOnN5Kanji: false,         // legacy binary toggle (kept for migration)
  furiganaMode: 'hide-known',       // 'always' | 'hide-known' | 'never' (Brief 2 §4.1)
  lastTestLength: 20,
  diagnosticCompleted: false,
  lastDiagnosticDate: null,
  audioPlaybackRate: 1.0,           // Brief 2 §5: 0.75 / 1.0 / 1.25
  reduceMotion: null,               // null = follow prefers-reduced-motion; true/false override
};

export function getSettings() {
  return { ...DEFAULT_SETTINGS, ...(get('settings') || {}) };
}

export function setSettings(patch) {
  const next = { ...getSettings(), ...patch };
  set('settings', next);
  return next;
}

export function getHistory() {
  return get('history', {});
}

export function setHistory(h) {
  set('history', h);
}

export function getResults() {
  return get('results', []);
}

export function initStorage() {
  if (get('settings') === null) set('settings', DEFAULT_SETTINGS);
  if (get('history') === null) set('history', {});
  if (get('results') === null) set('results', []);
  if (get('knownKanji') === null) set('knownKanji', {});  // Brief 2 §4.2
  if (get('streak') === null) set('streak', { current: 0, longest: 0, lastStudyDate: null, days: [] });
}

// Streak tracking (Brief 2 §6.1).
// `days` is a sliding window of YYYY-MM-DD strings (last 30 days) for the heatmap.
function todayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}
export function getStreak() { return get('streak', { current: 0, longest: 0, lastStudyDate: null, days: [] }); }
export function recordStudyToday() {
  const s = getStreak();
  const today = todayKey();
  if (s.lastStudyDate === today) return s;
  // If lastStudyDate is yesterday, increment streak. Otherwise reset to 1.
  if (s.lastStudyDate) {
    const last = new Date(s.lastStudyDate);
    const diff = Math.round((new Date(today) - last) / 86400000);
    s.current = diff === 1 ? s.current + 1 : 1;
  } else {
    s.current = 1;
  }
  s.longest = Math.max(s.longest || 0, s.current);
  s.lastStudyDate = today;
  s.days = [...new Set([...(s.days || []), today])].slice(-30);
  set('streak', s);
  return s;
}

// Per-kanji "I know this" flags (Brief 2 §4.2).
export function getKnownKanji() { return get('knownKanji', {}); }
export function isKanjiKnown(glyph) { return !!getKnownKanji()[glyph]; }
export function setKanjiKnown(glyph, known) {
  const m = getKnownKanji();
  if (known) m[glyph] = true; else delete m[glyph];
  set('knownKanji', m);
}

// Per-vocab "I know this word" flags (added 2026-05-01 per OPEN-10:
// the Mark-as-known control needs parity across grammar / vocab / kanji
// detail surfaces). Keyed by vocab `form` (the surface kana/kanji word)
// rather than by id, so the user-visible identity matches what they see
// on the detail page.
export function getKnownVocab() { return get('knownVocab', {}); }
export function isVocabKnown(form) { return !!getKnownVocab()[form]; }
export function setVocabKnown(form, known) {
  const m = getKnownVocab();
  if (known) m[form] = true; else delete m[form];
  set('knownVocab', m);
}

// Per-passage / per-drill completion tracking (added 2026-05-02 for the
// homepage syllabus-dashboard Progress section; previously reading and
// listening had no per-item completion state, so the dashboard's Reading
// and Listening rows were stuck at 0/30). A passage is "completed" the
// first time a user finishes its question set with at least one correct
// answer; a listening drill is "completed" the first time the user
// submits an answer (right or wrong, since listening is graded
// auto-submit).
export function getCompletedReading() { return get('completedReading', {}); }
export function isReadingCompleted(id) { return !!getCompletedReading()[id]; }
export function setReadingCompleted(id) {
  const m = getCompletedReading();
  if (m[id]) return; // idempotent — first-completion only
  m[id] = { at: new Date().toISOString() };
  set('completedReading', m);
}

export function getCompletedListening() { return get('completedListening', {}); }
export function isListeningCompleted(id) { return !!getCompletedListening()[id]; }
export function setListeningCompleted(id) {
  const m = getCompletedListening();
  if (m[id]) return;
  m[id] = { at: new Date().toISOString() };
  set('completedListening', m);
}

// ---- Pattern history per spec §7.4 + §6.6 ----

const FRESH_PATTERN_ENTRY = {
  attempts: 0,
  correct: 0,
  incorrect: 0,
  errorRate: 0,
  consecutiveCorrect: 0,
  isWeak: false,
  isMastered: false,
  isManuallyKnown: false,
  lastSeen: null,
  // Legacy Leitner-light state (kept for migration / existing UI badges)
  srsBox: null,         // null | '1d' | '3d' | '7d' | '14d' | 'graduated'
  nextDue: null,        // ISO date string when this pattern next appears in Drill
  // FSRS-4 state (replaced SM-2 2026-05-01; see EB-4 Tier-1)
  stability: null,      // S - days the memory holds at 90% recall
  difficulty: null,     // D - clamped [1..10]
  lastReview: null,     // ISO timestamp of most recent review
  // Legacy SM-2 fields kept for backward compat / migration. Not used at
  // runtime since 2026-05-01; FSRS-4 is the active scheduler.
  easeFactor: 2.5,      // EF - SM-2 ease factor
  interval: 0,          // days until next review (also kept by FSRS)
  reps: 0,              // consecutive correct streak (resets on lapse)
  lapses: 0,            // total times the user has forgotten this item
};

// SRS box graduation order. Per spec §5.8.
const NEXT_BOX = { '1d': '3d', '3d': '7d', '7d': '14d', '14d': 'graduated' };
const BOX_DAYS = { '1d': 1, '3d': 3, '7d': 7, '14d': 14 };

function isoNowPlusDays(days) {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString();
}

function updatePatternEntry(entry, isCorrect, nowIso, source = 'test') {
  const e = { ...FRESH_PATTERN_ENTRY, ...entry };
  e.attempts += 1;
  if (isCorrect) {
    e.correct += 1;
    e.consecutiveCorrect += 1;
  } else {
    e.incorrect += 1;
    e.consecutiveCorrect = 0;
  }
  e.errorRate = e.incorrect / e.attempts;
  // FR-W1: weak if errorRate >= 0.5 AND attempts >= 2
  e.isWeak = e.errorRate >= 0.5 && e.attempts >= 2;
  // FR-W3 / FR-W4: mastered after 4 consecutive correct OR manual override
  e.isMastered = e.isManuallyKnown || e.consecutiveCorrect >= 4;
  e.lastSeen = nowIso;

  // SRS state transitions per §5.8
  if (!isCorrect) {
    // Any wrong answer (test or drill) puts/keeps the pattern in the 1d box,
    // immediately drillable so the learner can recover the pattern while it's
    // fresh. Only on the NEXT correct in drill does it space out.
    e.srsBox = '1d';
    e.nextDue = nowIso;
    // FR-W4: a miss clears the manual-mastery override.
    e.isManuallyKnown = false;
    // Recompute isMastered now that isManuallyKnown is false.
    e.isMastered = e.consecutiveCorrect >= 4;
  } else if (source === 'drill' && e.srsBox && e.srsBox !== 'graduated') {
    // Correct answer in DRILL only - advance the box.
    if (e.consecutiveCorrect >= 4 || e.srsBox === '14d') {
      e.srsBox = 'graduated';
      e.nextDue = null;
    } else {
      e.srsBox = NEXT_BOX[e.srsBox] || e.srsBox;
      e.nextDue = e.srsBox === 'graduated' ? null : isoNowPlusDays(BOX_DAYS[e.srsBox]);
    }
  }
  // Note: correct answer in TEST does NOT advance the SRS box. Test is for
  // assessment; only Drill earns graduation (FR-S3 spirit).

  return e;
}

/**
 * Record a test's responses into rolling history.
 * @param {Array<{questionId, grammarPatternId, isCorrect}>} responses
 */
export function recordTestResponses(responses) {
  const history = getHistory();
  const now = new Date().toISOString();
  for (const r of responses) {
    if (!r.grammarPatternId) continue;
    history[r.grammarPatternId] = updatePatternEntry(
      history[r.grammarPatternId] || FRESH_PATTERN_ENTRY,
      r.isCorrect,
      now,
      'test',
    );
  }
  setHistory(history);
}

/**
 * Record a single drill response into rolling history.
 * Drill responses ADVANCE the SRS box on correct, RESET to 1d on wrong.
 */
export function recordDrillResponse(grammarPatternId, isCorrect) {
  if (!grammarPatternId) return;
  const history = getHistory();
  const now = new Date().toISOString();
  history[grammarPatternId] = updatePatternEntry(
    history[grammarPatternId] || FRESH_PATTERN_ENTRY,
    isCorrect,
    now,
    'drill',
  );
  setHistory(history);
}

/**
 * Return pattern IDs that are due for Drill now (nextDue <= now and not graduated).
 */
export function getDuePatternIds() {
  const history = getHistory();
  const now = new Date().toISOString();
  return Object.entries(history)
    .filter(([, v]) => v.srsBox && v.srsBox !== 'graduated' && v.nextDue && v.nextDue <= now)
    .map(([id]) => id);
}

export function getDueCount() {
  return getDuePatternIds().length;
}

/**
 * Append a test result summary to the results log.
 */
export function recordTestResult(result) {
  const all = getResults();
  all.push(result);
  setResults(all);
}

export function setResults(arr) {
  set('results', arr);
}

export function getWeakPatternIds() {
  const h = getHistory();
  return Object.entries(h)
    .filter(([, v]) => v.isWeak && !v.isMastered)
    .map(([id]) => id);
}

export function getMasteredPatternIds() {
  const h = getHistory();
  return Object.entries(h).filter(([, v]) => v.isMastered).map(([id]) => id);
}

export function getSeenPatternIds() {
  const h = getHistory();
  return Object.entries(h).filter(([, v]) => v.attempts > 0).map(([id]) => id);
}

export function getPatternEntry(id) {
  const h = getHistory();
  return h[id] || null;
}

// =============== SRS algorithm: FSRS-4 (EB-4 Tier-1, 2026-05-01) ===============
//
// Replaces SM-2 with FSRS-4 (Free Spaced Repetition Scheduler v4) — the
// algorithm Anki 23.10+ uses by default. Better recall prediction than SM-2,
// no new data collection required, fully on-device.
//
// FSRS-4 reference: https://github.com/open-spaced-repetition/fsrs4anki/wiki
//
// Per-item state:
//   stability (S): days the memory holds at 90% recall probability
//   difficulty (D): clamped [1..10], how "hard" this card is
//   last_review: ISO timestamp of the most recent review
// 4-button grading. The UI buttons emit 1/3/4/5 (SM-2 legacy) which we
// translate internally to FSRS's 1/2/3/4 scale.
//
// SM-2 fields (easeFactor / interval / reps) are preserved on each entry
// for compatibility with the existing Drill SRS-box UI badges and for
// migration. New reviews update FSRS state; legacy SM-2 fields decay.

const GRADE_AGAIN = 1;
const GRADE_HARD = 3;
const GRADE_GOOD = 4;
const GRADE_EASY = 5;

export const SM2 = { GRADE_AGAIN, GRADE_HARD, GRADE_GOOD, GRADE_EASY };
export const FSRS_GRADE = { AGAIN: 1, HARD: 2, GOOD: 3, EASY: 4 };

// FSRS-4 default weights from the Anki/Open-SR community calibration set.
// These are general-purpose defaults; per-user optimization (which would
// need cross-user data we don't have) could improve them but isn't worth
// the complexity for an N5 study tool.
const FSRS_W = [0.4, 0.6, 2.4, 5.8, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14,
                0.94, 2.18, 0.05, 0.34, 1.26, 0.29, 2.61];
const FSRS_DESIRED_RETENTION = 0.9;
const FSRS_LN_TARGET = Math.log(FSRS_DESIRED_RETENTION);  // -0.1054
const FSRS_LN_09 = Math.log(0.9);  // identical to LN_TARGET when retention = 0.9

// Translate the legacy SM-2 1/3/4/5 grade scale to FSRS's 1/2/3/4 scale.
// We do this internally so review.js can keep its existing data-grade
// attributes (1/3/4/5) without UI changes.
function toFsrsGrade(g) {
  if (g <= 1) return 1;       // Again
  if (g === 3) return 2;      // Hard
  if (g === 4) return 3;      // Good
  return 4;                   // 5 → Easy
}

function clampDifficulty(d) {
  return Math.max(1, Math.min(10, d));
}

function initialFsrsState(grade) {
  // First-ever review of an item — no prior memory state.
  const fg = toFsrsGrade(grade);
  const stability = Math.max(0.1, FSRS_W[fg - 1]);  // w[0..3] index by grade-1
  const difficulty = clampDifficulty(FSRS_W[4] - (fg - 3) * FSRS_W[5]);
  return { stability, difficulty };
}

function nextStability(S_old, D_old, R_actual, fg) {
  if (fg === 1) {
    // Lapse. Stability drops toward post-lapse formula.
    return FSRS_W[11]
      * Math.pow(D_old, -FSRS_W[12])
      * (Math.pow(S_old + 1, FSRS_W[13]) - 1)
      * Math.exp(FSRS_W[14] * (1 - R_actual));
  }
  // Recall. Stability grows.
  const factor = Math.exp(FSRS_W[8])
    * (11 - D_old)
    * Math.pow(S_old, -FSRS_W[9])
    * (Math.exp(FSRS_W[10] * (1 - R_actual)) - 1);
  const hardPenalty = fg === 2 ? FSRS_W[15] : 1;
  const easyBonus = fg === 4 ? FSRS_W[16] : 1;
  return S_old * (1 + factor * hardPenalty * easyBonus);
}

function nextDifficulty(D_old, fg) {
  // Update step
  const D_step = D_old - FSRS_W[6] * (fg - 3);
  // Mean reversion toward the difficulty for an Easy first review (D_init_4)
  const D_init_4 = FSRS_W[4] - (4 - 3) * FSRS_W[5];
  const D_reverted = FSRS_W[7] * D_init_4 + (1 - FSRS_W[7]) * D_step;
  return clampDifficulty(D_reverted);
}

function applyFsrs(entry, grade, nowIso) {
  const e = { ...FRESH_PATTERN_ENTRY, ...entry };
  const fg = toFsrsGrade(grade);
  let S_old = e.stability;
  let D_old = e.difficulty;

  // Migration: if no FSRS state but legacy SM-2 state exists, seed FSRS from it.
  // Otherwise, this is a first-ever review.
  if (S_old === undefined || S_old === null) {
    if (e.easeFactor && e.interval) {
      // Translate SM-2 → FSRS:
      // - SM-2 interval is roughly stability when targeting 90% retention
      // - SM-2 easeFactor (1.3..2.5+) maps inversely to difficulty (1..10)
      S_old = Math.max(0.1, e.interval || 1);
      D_old = clampDifficulty(10 - 8 * (((e.easeFactor || 2.5) - 1.3) / (2.5 - 1.3)));
    } else {
      // First review of this item.
      const init = initialFsrsState(grade);
      e.stability = init.stability;
      e.difficulty = init.difficulty;
      e.lastReview = nowIso;
      // Schedule next due
      const intervalDays = Math.max(1, Math.round(init.stability));
      e.interval = intervalDays;  // keep for legacy badge UI
      const next = new Date();
      next.setDate(next.getDate() + intervalDays);
      e.nextDue = next.toISOString();
      e.lastSeen = nowIso;
      if (fg === 1) e.lapses = (e.lapses || 0) + 1;
      return e;
    }
  }

  // Subsequent review: update S and D.
  const lastReview = e.lastReview ? new Date(e.lastReview) : new Date(nowIso);
  const elapsedDays = Math.max(0, (Date.parse(nowIso) - lastReview.getTime()) / 86400000);
  const R_actual = Math.exp(FSRS_LN_09 * elapsedDays / Math.max(0.1, S_old));

  e.stability = Math.max(0.1, nextStability(S_old, D_old, R_actual, fg));
  e.difficulty = nextDifficulty(D_old, fg);
  e.lastReview = nowIso;
  if (fg === 1) e.lapses = (e.lapses || 0) + 1;

  // Schedule next due
  const intervalDays = Math.max(1,
    Math.round(e.stability * (FSRS_LN_TARGET / FSRS_LN_09))
  );
  e.interval = intervalDays;  // keep for legacy badge UI
  const next = new Date();
  next.setDate(next.getDate() + intervalDays);
  e.nextDue = next.toISOString();
  e.lastSeen = nowIso;
  return e;
}

// SM-2 implementation kept as a fallback / migration reference. Not called
// at runtime since 2026-05-01; FSRS-4 (above) is the active scheduler.
// Removing this would lose the ability to interpret old entries that have
// only easeFactor/interval and no stability/difficulty.
function applySm2(entry, grade, nowIso) {
  const e = { ...FRESH_PATTERN_ENTRY, ...entry };
  if (grade < 3) {
    e.lapses = (e.lapses || 0) + 1;
    e.reps = 0;
    e.interval = 1;
  } else {
    e.reps = (e.reps || 0) + 1;
    if (e.reps === 1) e.interval = 1;
    else if (e.reps === 2) e.interval = 6;
    else e.interval = Math.round((e.interval || 1) * (e.easeFactor || 2.5));
  }
  const newEf = (e.easeFactor || 2.5) + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02));
  e.easeFactor = Math.max(1.3, newEf);
  const next = new Date();
  next.setDate(next.getDate() + e.interval);
  e.nextDue = next.toISOString();
  e.lastSeen = nowIso;
  return e;
}

/**
 * Record an SRS graded response. The drill UI sends grades on the legacy
 * SM-2 1/3/4/5 scale (Again/Hard/Good/Easy); the FSRS scheduler translates
 * internally to FSRS's 1/2/3/4 scale.
 */
export function recordSrsResponse(grammarPatternId, grade) {
  if (!grammarPatternId) return;
  const history = getHistory();
  const now = new Date().toISOString();
  const existing = history[grammarPatternId] || FRESH_PATTERN_ENTRY;
  // Snapshot the pre-update entry so the 2s-undo flow in Review can
  // restore it byte-for-byte (DEFER-14, shipped 2026-05-02). The clone
  // is JSON-safe because every field on a history entry is a primitive.
  const preUpdateSnapshot = JSON.parse(JSON.stringify(existing));
  const updated = applyFsrs(existing, grade, now);
  // Keep rolling-history fields in sync for the existing weak-detection code.
  updated.attempts = (updated.attempts || 0) + 1;
  if (grade < 3) {
    updated.incorrect = (updated.incorrect || 0) + 1;
    updated.consecutiveCorrect = 0;
  } else {
    updated.correct = (updated.correct || 0) + 1;
    updated.consecutiveCorrect = (updated.consecutiveCorrect || 0) + 1;
  }
  updated.errorRate = updated.incorrect / Math.max(1, updated.attempts);
  updated.isWeak = updated.errorRate >= 0.5 && updated.attempts >= 2;
  updated.isMastered = updated.isManuallyKnown || updated.consecutiveCorrect >= 4;
  history[grammarPatternId] = updated;
  setHistory(history);
  return preUpdateSnapshot;
}

// Restore a single pattern's history entry to a prior snapshot. Used by
// the Review undo-2s flow (DEFER-14): the caller stashes the return
// value of recordSrsResponse, and if the user clicks Undo within the
// window, calls undoSrsResponse(pid, snapshot) to roll back.
export function undoSrsResponse(grammarPatternId, snapshot) {
  if (!grammarPatternId || !snapshot) return false;
  const history = getHistory();
  // Defensive: only restore if the entry still exists (user might have
  // hit Reset progress in the meantime).
  if (!history[grammarPatternId]) return false;
  history[grammarPatternId] = snapshot;
  setHistory(history);
  return true;
}

export function getSrsState(grammarPatternId) {
  const e = getHistory()[grammarPatternId];
  if (!e) return null;
  return {
    // FSRS-4 state (the active scheduler since 2026-05-01)
    stability: e.stability ?? null,
    difficulty: e.difficulty ?? null,
    lastReview: e.lastReview ?? null,
    // Legacy SM-2 state (informational; not used at runtime)
    easeFactor: e.easeFactor ?? 2.5,
    interval: e.interval ?? 0,
    reps: e.reps ?? 0,
    lapses: e.lapses ?? 0,
    nextDue: e.nextDue,
  };
}

/**
 * Toggle the manual-mastery override for a pattern (FR-W4).
 * When true, isMastered becomes true regardless of attempt count. The flag
 * is cleared automatically on the next miss.
 */
export function setManuallyKnown(grammarPatternId, known) {
  const history = getHistory();
  const e = { ...FRESH_PATTERN_ENTRY, ...(history[grammarPatternId] || {}) };
  e.isManuallyKnown = !!known;
  e.isMastered = e.isManuallyKnown || e.consecutiveCorrect >= 4;
  history[grammarPatternId] = e;
  setHistory(history);
}

/**
 * Export all progress (settings + history + results) as a JSON-serializable
 * object suitable for download as `progress.json`.
 */
export function exportProgress() {
  return {
    schemaVersion: 2,
    exportedAt: new Date().toISOString(),
    appVersion: 'jlpt-n5-tutor',
    settings: getSettings(),
    history: getHistory(),
    results: getResults(),
    knownKanji: getKnownKanji(),
    streak: getStreak(),
  };
}

/**
 * Import a progress payload, replacing all existing state. Validates the
 * schema and refuses to import if it doesn't match.
 * Schema v1 is accepted (knownKanji + streak just default to empty).
 * Schema v2 includes knownKanji + streak.
 * @returns {{ok: boolean, message: string}}
 */
export function importProgress(payload) {
  if (!payload || typeof payload !== 'object') {
    return { ok: false, message: 'Invalid payload (not an object).' };
  }
  if (![1, 2].includes(payload.schemaVersion)) {
    return { ok: false, message: `Unsupported schema version: ${payload.schemaVersion}` };
  }
  if (!payload.settings || !payload.history || !Array.isArray(payload.results)) {
    return { ok: false, message: 'Missing required fields (settings/history/results).' };
  }
  set('settings', payload.settings);
  set('history', payload.history);
  set('results', payload.results);
  // v2 keys (Brief 2 §4.2 + §6.1): tolerate missing on v1 imports.
  if (payload.knownKanji && typeof payload.knownKanji === 'object') {
    set('knownKanji', payload.knownKanji);
  }
  if (payload.streak && typeof payload.streak === 'object') {
    set('streak', payload.streak);
  }
  return { ok: true, message: `Imported. ${Object.keys(payload.history).length} pattern entries, ${payload.results.length} test results.` };
}
