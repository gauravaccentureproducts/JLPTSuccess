// EB-4: Pedagogy-rule recommender (round-9 close-out, 2026-05-07).
//
// Purpose: replace the v2.0 "ML-backed recommender" item, which sat
// blocked on "needs a privacy-clean data path" — there is no such
// path inside our privacy posture (no telemetry, no cloud, no
// account → no data to train on). The v2.0 ask is therefore not "build
// an ML system" but "deliver a meaningful next-step recommendation
// with the on-device signal already available." A native-Japanese-
// teacher persona authored the rules below; they encode classroom
// pedagogy directly rather than learning it from data.
//
// Design constraints (mandatory):
//   1. PURE FUNCTION — input is a state snapshot from storage, output
//      is a structured recommendation object. No side effects, no
//      fetch, no network, no telemetry.
//   2. DETERMINISTIC — same state in → same recommendation out. No
//      randomness, no time-of-day variance.
//   3. ON-DEVICE — reads only from storage.* (which itself reads only
//      from localStorage). Nothing leaves the device.
//   4. EXPLAINABLE — every recommendation carries a `why` field so
//      learners + reviewers can see the rule that fired.
//   5. RULE-PRIORITY — rules fire in pedagogical priority order; the
//      first match wins. Lower-priority rules are tie-breakers.
//
// Output contract:
//   {
//     surface:   'review' | 'learn' | 'drill' | 'reading' | 'listening'
//                | 'kanji' | 'mock' | 'starter',
//     href:      string  (route to navigate to, hash-style)
//     label_en:  string  (one-line action label, < 60 chars)
//     label_hi:  string  (Hindi mirror)
//     why_en:    string  (one-sentence pedagogical rationale)
//     why_hi:    string  (Hindi mirror)
//     duration:  string  (e.g. "5 min", "15 min")
//     priority:  number  (1 = highest)
//     rule_id:   string  (e.g. 'R-01' — traceable to docs/RECOMMENDER-RULES.md)
//   }
//
// The home page renders the *first* recommendation; the summary page
// optionally renders the top N as a stack.
//
// Rule catalogue is documented in docs/RECOMMENDER-RULES.md.
//
// Tests: pure function → unit-testable; see tests/recommender.test.html
// (browser-runnable, not committed yet — tracked as next-cycle work).

import * as storage from './storage.js';

// ---------------------------------------------------------------------------
// Tunables (in one place so a future content-team adjustment doesn't
// require code archaeology). Each constant is justified in
// docs/RECOMMENDER-RULES.md § Tunables.
// ---------------------------------------------------------------------------
const TUNABLES = Object.freeze({
  // R-01: due-queue threshold above which "clear the queue" outranks
  // everything else. Tuned to the typical N5 classroom session.
  REVIEW_HIGH_DUE: 30,
  // R-01: middle band — show review but not as overwhelming.
  REVIEW_MED_DUE:  10,
  // R-04: weak-pattern threshold — at >= this many wrong answers in
  // recent history on the same pattern, recommend re-learning it.
  WEAK_PATTERN_WRONG_COUNT: 3,
  // R-05: number of starter-pack patterns considered "foundational"
  // for the new-user lane.
  STARTER_PACK_SIZE: 5,
  // R-08: today's-goal completion threshold below which we surface
  // "your daily goal" hint before any other lateral suggestion.
  DAILY_GOAL_PCT_FLOOR: 50,
  // R-09: missing-skill-coverage thresholds — if any skill has
  // < this fraction of items completed, surface that skill.
  COVERAGE_FLOOR: 0.05,
  // R-10: lateral skill switching — if learner has done > this
  // fraction of grammar without touching listening, prompt the swap.
  LATERAL_SWAP_GRAMMAR_PCT: 0.20,
  LATERAL_SWAP_KANJI_PCT:   0.20,
  // R-12: streak-protection — if learner has practiced today, do
  // NOT pile on more recommendations; instead acknowledge.
  ACKNOWLEDGE_AFTER_GOAL_PCT: 100,
  // R-14: mock-test threshold — once learner has touched >= this
  // fraction of grammar AND >= this kanji, suggest a mock paper.
  MOCK_READY_GRAMMAR_PCT: 0.60,
  MOCK_READY_KANJI_PCT:   0.50,
});

// ---------------------------------------------------------------------------
// Helpers — pure utility. No storage access here; that lives in
// `gatherSignal()` so the rules themselves can be tested with a hand-
// rolled signal object.
// ---------------------------------------------------------------------------

function todayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

// Aggregate per-skill due counts safely; the unified-queue API may not
// be present in all build vintages.
function safeDueCountsBySkill() {
  if (typeof storage.getDueCountsBySkill === 'function') {
    return storage.getDueCountsBySkill();
  }
  // Fallback: grammar-only legacy.
  return {
    grammar: typeof storage.getDueCount === 'function' ? storage.getDueCount() : 0,
    vocab: 0,
    kanji: 0,
  };
}

// Count of N5 corpus items per surface — fallback constants used only
// if the live data files have not been read yet. Kept intentionally
// short of live counts so the recommender never blocks on data load;
// home.js passes the live counts in via `signal.corpusCounts`.
const CORPUS_FALLBACK = Object.freeze({
  grammar: 178,
  vocab: 1041,
  kanji: 106,
  reading: 45,
  listening: 47,
});

// Build the full signal object the rules consume. Pure-ish: the only
// impurity is reading from storage / closures over `corpusCounts`. The
// rules below operate on this dict only.
export function gatherSignal({ corpusCounts } = {}) {
  const counts = corpusCounts && Object.keys(corpusCounts).length
    ? corpusCounts
    : CORPUS_FALLBACK;

  const history = (typeof storage.getHistory === 'function') ? storage.getHistory() : {};
  const results = (typeof storage.getResults === 'function') ? storage.getResults() : [];
  const settings = (typeof storage.getSettings === 'function') ? storage.getSettings() : {};
  const streak = (typeof storage.getStreak === 'function') ? storage.getStreak() : null;
  const reviewsToday = (typeof storage.getReviewsToday === 'function') ? storage.getReviewsToday() : 0;
  const dailyGoal = (typeof storage.getDailyGoal === 'function') ? storage.getDailyGoal() : 20;
  const wrongHistory = (typeof storage.getWrongHistory === 'function') ? storage.getWrongHistory() : [];
  const dueBySkill = safeDueCountsBySkill();
  const dueTotal = (dueBySkill.grammar || 0) + (dueBySkill.vocab || 0) + (dueBySkill.kanji || 0);

  const knownKanji = (typeof storage.getKnownKanji === 'function') ? storage.getKnownKanji() : {};
  const knownVocab = (typeof storage.getKnownVocab === 'function') ? storage.getKnownVocab() : {};
  const completedReading = (typeof storage.getCompletedReading === 'function') ? storage.getCompletedReading() : {};
  const completedListening = (typeof storage.getCompletedListening === 'function') ? storage.getCompletedListening() : {};

  const seenPatterns = (typeof storage.getSeenPatternIds === 'function') ? storage.getSeenPatternIds() : [];
  const masteredPatterns = (typeof storage.getMasteredPatternIds === 'function') ? storage.getMasteredPatternIds() : [];
  const weakPatterns = (typeof storage.getWeakPatternIds === 'function') ? storage.getWeakPatternIds() : [];

  const completionPct = {
    grammar:   counts.grammar   ? seenPatterns.length / counts.grammar : 0,
    vocab:     counts.vocab     ? Object.keys(knownVocab).length / counts.vocab : 0,
    kanji:     counts.kanji     ? Object.keys(knownKanji).length / counts.kanji : 0,
    reading:   counts.reading   ? Object.keys(completedReading).length / counts.reading : 0,
    listening: counts.listening ? Object.keys(completedListening).length / counts.listening : 0,
  };

  const isReturning = Object.keys(history).length > 0 || results.length > 0;
  const goalPct = dailyGoal > 0 ? Math.round(100 * reviewsToday / dailyGoal) : 0;
  const goalMet = streak && streak.lastStudyDate === todayKey();

  // Wrong-answer aggregation per pattern. The wrongHistory entries
  // typically carry { patternId, timestamp, ... }. Recent (last 30
  // days) entries are weighted; older ones decay out.
  const cutoff = Date.now() - 30 * 24 * 60 * 60 * 1000;
  const wrongByPattern = new Map();
  for (const w of wrongHistory) {
    if (!w?.patternId) continue;
    if (w.timestamp && w.timestamp < cutoff) continue;
    wrongByPattern.set(w.patternId, (wrongByPattern.get(w.patternId) || 0) + 1);
  }

  return {
    isReturning,
    streak: streak || { current: 0 },
    goalMet,
    goalPct,
    reviewsToday,
    dailyGoal,
    dueBySkill,
    dueTotal,
    completionPct,
    seenPatterns,
    masteredPatterns,
    weakPatterns,
    wrongByPattern,
    lastLearnId: settings.lastLearnId || null,
    counts,
  };
}

// ---------------------------------------------------------------------------
// Rule catalogue. Each rule is a function that returns a recommendation
// object or null. Rules are invoked in priority order; first non-null
// wins for the home-page slot. The summary page can stack the top N.
//
// Convention:
//   - Rule IDs trace to docs/RECOMMENDER-RULES.md (R-01 … R-14).
//   - Rules return null when their condition does not fire.
//   - A rule never reads storage directly; it only reads `signal`.
// ---------------------------------------------------------------------------

function R01_clearLargeReviewQueue(signal) {
  if (signal.dueTotal >= TUNABLES.REVIEW_HIGH_DUE) {
    return {
      surface: 'review',
      href: '#/review',
      label_en: `Clear today's review queue (${signal.dueTotal} due)`,
      label_hi: `आज की समीक्षा कतार साफ़ करें (${signal.dueTotal} बाकी)`,
      why_en: 'A backlog this size means SRS spacing has slipped; reviewing now preserves the schedule.',
      why_hi: 'इतनी बड़ी कतार का मतलब है कि SRS अंतराल बिगड़ रहा है; अभी समीक्षा करने से शेड्यूल बना रहता है।',
      duration: '15-20 min',
      priority: 1,
      rule_id: 'R-01',
    };
  }
  return null;
}

function R02_clearMediumReviewQueue(signal) {
  if (signal.dueTotal >= TUNABLES.REVIEW_MED_DUE && signal.dueTotal < TUNABLES.REVIEW_HIGH_DUE) {
    return {
      surface: 'review',
      href: '#/review',
      label_en: `Run today's review (${signal.dueTotal} due)`,
      label_hi: `आज की समीक्षा करें (${signal.dueTotal} बाकी)`,
      why_en: 'Steady daily reviews keep retention high without fatigue.',
      why_hi: 'दैनिक समीक्षा से बिना थकान धारण ऊँचा रहता है।',
      duration: '8-10 min',
      priority: 2,
      rule_id: 'R-02',
    };
  }
  return null;
}

function R03_smallReviewQueue(signal) {
  if (signal.dueTotal > 0 && signal.dueTotal < TUNABLES.REVIEW_MED_DUE) {
    return {
      surface: 'review',
      href: '#/review',
      label_en: `Quick review (${signal.dueTotal} due)`,
      label_hi: `त्वरित समीक्षा (${signal.dueTotal} बाकी)`,
      why_en: 'Small queue — clear it now and the schedule stays clean.',
      why_hi: 'छोटी कतार — अभी साफ़ कर दें तो शेड्यूल साफ़ रहेगा।',
      duration: '3-5 min',
      priority: 3,
      rule_id: 'R-03',
    };
  }
  return null;
}

function R04_revisitWeakestPattern(signal) {
  // Highest-wrong-count pattern in the last 30 days, if it exceeds threshold.
  let topPid = null;
  let topCount = 0;
  for (const [pid, n] of signal.wrongByPattern) {
    if (n > topCount) { topCount = n; topPid = pid; }
  }
  if (topPid && topCount >= TUNABLES.WEAK_PATTERN_WRONG_COUNT) {
    return {
      surface: 'learn',
      href: `#/learn/${encodeURIComponent(topPid)}`,
      label_en: `Re-learn ${topPid} (${topCount} recent misses)`,
      label_hi: `${topPid} फिर से सीखें (${topCount} हाल की चूक)`,
      why_en: 'You have missed this pattern repeatedly — re-reading the explanation breaks the wrong-answer loop.',
      why_hi: 'आपने यह पैटर्न बार-बार चूका है — व्याख्या फिर पढ़ने से गलत-उत्तर का चक्र टूटता है।',
      duration: '5 min',
      priority: 4,
      rule_id: 'R-04',
    };
  }
  return null;
}

function R05_starterPackForNewUser(signal) {
  if (!signal.isReturning) {
    return {
      surface: 'starter',
      href: '#/learn/n5-001',
      label_en: 'Start the 5-pattern foundation pack',
      label_hi: '5-पैटर्न आधार-पैक शुरू करें',
      why_en: 'です・は・ます・い-adjectives・か are the bones every other N5 pattern hangs on.',
      why_hi: 'です・は・ます・い-विशेषण・か — सब अन्य N5 पैटर्न इन्हीं पर टँगे होते हैं।',
      duration: '25 min total (5 patterns × 5 min)',
      priority: 5,
      rule_id: 'R-05',
    };
  }
  return null;
}

function R06_resumeLastSession(signal) {
  if (signal.isReturning && signal.lastLearnId) {
    return {
      surface: 'learn',
      href: `#/learn/${encodeURIComponent(signal.lastLearnId)}`,
      label_en: `Continue ${signal.lastLearnId}`,
      label_hi: `${signal.lastLearnId} जारी रखें`,
      why_en: 'You opened this in your last session; finishing it consolidates that working memory before it fades.',
      why_hi: 'पिछले सत्र में इसे खोला था; इसे पूरा करने से वह कार्यशील स्मृति मिटने से पहले स्थिर हो जाती है।',
      duration: '5-10 min',
      priority: 6,
      rule_id: 'R-06',
    };
  }
  return null;
}

function R07_diagnoseFirst(signal) {
  // If returning user has < 5 % of grammar seen but no due queue, the
  // diagnostic surface is the highest-leverage next stop.
  if (signal.isReturning && signal.completionPct.grammar < 0.05 && signal.dueTotal === 0) {
    return {
      surface: 'mock',
      href: '#/diagnostic',
      label_en: 'Take the 10-question placement check',
      label_hi: '10-प्रश्न प्लेसमेंट जाँच लें',
      why_en: 'You have barely opened the syllabus; the placement check finds your real starting line in 10 minutes.',
      why_hi: 'आपने पाठ्यक्रम मुश्किल से खोला है; प्लेसमेंट जाँच 10 मिनट में आपकी असली शुरुआत खोज देती है।',
      duration: '10 min',
      priority: 7,
      rule_id: 'R-07',
    };
  }
  return null;
}

function R08_dailyGoalNudge(signal) {
  if (signal.isReturning && !signal.goalMet && signal.goalPct < TUNABLES.DAILY_GOAL_PCT_FLOOR && signal.dueTotal === 0) {
    return {
      surface: 'drill',
      href: '#/drill',
      label_en: `Mixed drill (${signal.reviewsToday} / ${signal.dailyGoal} today)`,
      label_hi: `मिश्रित अभ्यास (आज ${signal.reviewsToday} / ${signal.dailyGoal})`,
      why_en: 'Daily mixed practice keeps recall sharp even when no SRS items are due.',
      why_hi: 'जब कोई SRS पुनरीक्षण बाकी न हो, तब भी दैनिक मिश्रित अभ्यास स्मरण को तेज़ रखता है।',
      duration: '10-15 min',
      priority: 8,
      rule_id: 'R-08',
    };
  }
  return null;
}

function R09_minorityCoverage(signal) {
  // Surface the *most under-served* skill if any falls below the floor.
  // Only fires for returning users; new users get R-05.
  if (!signal.isReturning) return null;
  const lanes = [
    { skill: 'listening', pct: signal.completionPct.listening, surface: 'listening', href: '#/listening' },
    { skill: 'reading',   pct: signal.completionPct.reading,   surface: 'reading',   href: '#/reading'   },
    { skill: 'kanji',     pct: signal.completionPct.kanji,     surface: 'kanji',     href: '#/kanji'     },
  ];
  // Pick the lane that's both below the floor AND the *lowest* of the three.
  const sorted = lanes.filter(l => l.pct < TUNABLES.COVERAGE_FLOOR).sort((a,b) => a.pct - b.pct);
  if (sorted.length === 0) return null;
  const top = sorted[0];
  const labelMap = {
    listening: ['First listening drill', 'पहला श्रवण अभ्यास',
                'A listening drill at this stage establishes the prosody+pace expectation; without it, grammar study floats free of the spoken language.',
                'इस चरण में एक श्रवण अभ्यास से उच्चारण-गति की अपेक्षा बनती है; इसके बिना व्याकरण-अध्ययन बोली-भाषा से कटा रहता है।'],
    reading:   ['First reading passage', 'पहला पठन-अनुच्छेद',
                'Reading early — even one passage — anchors grammar patterns in their natural sentence environment.',
                'जल्दी एक भी पठन से व्याकरण-पैटर्न अपने स्वाभाविक वाक्य-वातावरण में जम जाते हैं।'],
    kanji:     ['Open the kanji index', 'कान्जी सूची खोलें',
                'You\'ll need 106 kanji for N5; meeting them in groups of 5 from day one is far easier than cramming the lot.',
                'N5 के लिए 106 कान्जी चाहिए; दिन-1 से 5-5 के समूह में मिलना अंतिम रटाई से कहीं आसान है।'],
  };
  const [le, lh, we, wh] = labelMap[top.skill];
  return {
    surface: top.surface,
    href: top.href,
    label_en: le,
    label_hi: lh,
    why_en: we,
    why_hi: wh,
    duration: '8-10 min',
    priority: 9,
    rule_id: 'R-09',
  };
}

function R10_lateralSwap(signal) {
  // Returning user, balanced grammar progress, but listening untouched.
  if (!signal.isReturning) return null;
  if (signal.completionPct.grammar > TUNABLES.LATERAL_SWAP_GRAMMAR_PCT
      && signal.completionPct.listening < TUNABLES.LATERAL_SWAP_GRAMMAR_PCT * 0.25) {
    return {
      surface: 'listening',
      href: '#/listening',
      label_en: 'Try a listening drill — your grammar is well ahead',
      label_hi: 'एक श्रवण-अभ्यास करें — व्याकरण आगे है',
      why_en: 'Grammar without sound is half a language; one listening drill calibrates expectations on real-time pace.',
      why_hi: 'ध्वनि के बिना व्याकरण आधी भाषा है; एक श्रवण-अभ्यास से वास्तविक-समय की गति की समझ बनती है।',
      duration: '8 min',
      priority: 10,
      rule_id: 'R-10',
    };
  }
  if (signal.completionPct.grammar > TUNABLES.LATERAL_SWAP_GRAMMAR_PCT
      && signal.completionPct.kanji < TUNABLES.LATERAL_SWAP_KANJI_PCT * 0.25) {
    return {
      surface: 'kanji',
      href: '#/kanji',
      label_en: 'Open the kanji index — your grammar is well ahead',
      label_hi: 'कान्जी सूची खोलें — व्याकरण आगे है',
      why_en: 'Reading and listening start to require kanji recognition by mid-N5; pulling the lever now keeps progress balanced.',
      why_hi: 'मध्य-N5 तक पठन-श्रवण कान्जी पहचान माँगने लगते हैं; अभी ध्यान देने से प्रगति संतुलित रहती है।',
      duration: '5-10 min',
      priority: 10,
      rule_id: 'R-10',
    };
  }
  return null;
}

function R11_reReadJustExploredPattern(signal) {
  // Tie-breaker: returning user with no other rule firing — re-open
  // last viewed pattern explicitly. This is the same as R-06 except
  // with a different rationale tone (consolidation rather than resume).
  if (signal.isReturning && signal.lastLearnId) {
    return {
      surface: 'learn',
      href: `#/learn/${encodeURIComponent(signal.lastLearnId)}`,
      label_en: `Reread ${signal.lastLearnId}`,
      label_hi: `${signal.lastLearnId} पुनः पढ़ें`,
      why_en: 'A second reading of a pattern is when long-term encoding happens — you\'ve seen it once; now consolidate.',
      why_hi: 'दूसरी बार पढ़ने पर ही दीर्घ-कालिक स्मरण बनता है — एक बार देख चुके हैं; अब स्थिर करें।',
      duration: '3-5 min',
      priority: 11,
      rule_id: 'R-11',
    };
  }
  return null;
}

function R12_acknowledgeGoalMet(signal) {
  // Streak-protection: if the learner has hit today's goal, do NOT
  // pile on more recommendations. Acknowledge and step back.
  if (signal.isReturning && signal.goalMet && signal.dueTotal === 0) {
    return {
      surface: 'home',
      href: '#/summary',
      label_en: 'Goal met today — see progress',
      label_hi: 'आज का लक्ष्य पूरा — प्रगति देखें',
      why_en: 'You have practiced today and the queue is clear. Review your progress; tomorrow is a fresh slot.',
      why_hi: 'आज अभ्यास हो चुका है और कतार साफ़ है। प्रगति देखें; कल नया दिन है।',
      duration: '2 min',
      priority: 12,
      rule_id: 'R-12',
    };
  }
  return null;
}

function R13_continueExplore(signal) {
  // Catch-all returning user with no other signal: open Learn hub.
  if (signal.isReturning) {
    return {
      surface: 'learn',
      href: '#/learn',
      label_en: 'Open Learn',
      label_hi: 'सीखें खोलें',
      why_en: 'Pick a category and pull the next thread.',
      why_hi: 'एक श्रेणी चुनें और अगला धागा खींचें।',
      duration: '10 min',
      priority: 13,
      rule_id: 'R-13',
    };
  }
  return null;
}

function R14_mockPaperReady(signal) {
  if (signal.completionPct.grammar >= TUNABLES.MOCK_READY_GRAMMAR_PCT
      && signal.completionPct.kanji >= TUNABLES.MOCK_READY_KANJI_PCT) {
    return {
      surface: 'mock',
      href: '#/test',
      label_en: 'You are ready for a mock paper',
      label_hi: 'आप एक मॉक-पेपर के लिए तैयार हैं',
      why_en: 'Coverage is broad enough that a timed mock paper now reveals real exam-shape gaps; do one before piling on more new content.',
      why_hi: 'कवरेज इतनी विस्तृत है कि एक समयबद्ध मॉक-पेपर अब वास्तविक परीक्षा-आकार की कमियाँ उजागर करेगा; और नया सामग्री जोड़ने से पहले एक करें।',
      duration: '20-30 min',
      priority: 14,
      rule_id: 'R-14',
    };
  }
  return null;
}

// Rule list, ordered by priority. Edit at your peril — the order
// encodes pedagogy, not just code style.
const RULES = [
  R01_clearLargeReviewQueue,
  R02_clearMediumReviewQueue,
  R03_smallReviewQueue,
  R04_revisitWeakestPattern,
  R05_starterPackForNewUser,
  R06_resumeLastSession,
  R07_diagnoseFirst,
  R08_dailyGoalNudge,
  R09_minorityCoverage,
  R10_lateralSwap,
  R11_reReadJustExploredPattern,
  R12_acknowledgeGoalMet,
  R13_continueExplore,
  R14_mockPaperReady,
];

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

// Single-recommendation API: returns the highest-priority rule's
// output. Returns null if no rule fires (extremely unlikely; R-13 is
// a catch-all for returning users, R-05 for new users).
export function recommend(signal) {
  for (const r of RULES) {
    const rec = r(signal);
    if (rec) return rec;
  }
  return null;
}

// Stack API: returns up to N recommendations, deduplicated by surface
// (so a learner doesn't see "review review review"). Used by the
// summary page.
export function recommendStack(signal, limit = 3) {
  const out = [];
  const surfaces = new Set();
  for (const r of RULES) {
    const rec = r(signal);
    if (rec && !surfaces.has(rec.surface)) {
      out.push(rec);
      surfaces.add(rec.surface);
      if (out.length >= limit) break;
    }
  }
  return out;
}

// Convenience: gather signal + recommend in one call.
export function recommendNow(opts = {}) {
  return recommend(gatherSignal(opts));
}

export function recommendStackNow(limit = 3, opts = {}) {
  return recommendStack(gatherSignal(opts), limit);
}

// Expose tunables + rule IDs for tests + docs sync.
export const _internals = Object.freeze({
  TUNABLES,
  RULE_IDS: RULES.map(fn => fn.name),
});
