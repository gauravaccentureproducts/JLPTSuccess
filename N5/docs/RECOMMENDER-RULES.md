# Pedagogy-rule recommender (EB-4)

> **Status:** Shipped 2026-05-07 (round-9 close-out, v1.12.50). Closes
> EB-4 (was: "v2.0 ML-backed recommender, blocked on privacy-clean
> data path"). Implementation: `js/pedagogy-recommender.js`.
> **Author:** project's resident 日本語教師 persona.

---

## 1. Why rules, not ML

The original EB-4 ask was a v2.0 ML recommender. It sat blocked under
[`TASKS.md` § External-blocked backlog](../TASKS.md) for a year because
**we don't have a data path that respects our privacy posture**. The
options were:

1. **Train on cloud-aggregated learner data** — would require accounts,
   telemetry, and a cloud backend. Breaks every claim in
   [`PRIVACY.md`](../PRIVACY.md). Non-starter.
2. **On-device learning** — viable in principle (e.g. WebLLM /
   Transformers.js), but:
   - Adds 200–500 MB to the bundle.
   - Each user trains a fresh model on a tiny dataset (their own
     history) — converges to noise.
   - Most users would turn it off the moment it touches CPU.
3. **Federated learning** — needs a coordination server. We don't
   have one.

The native-JA-teacher persona pointed out that **for a curriculum
this constrained (178 grammar patterns, fixed JLPT N5 syllabus, well-
known progression order)** the optimal recommender is not ML at all;
it's **rules a teacher would tell you**. Encode the pedagogy
directly. The data signal you actually need (today's due count,
last-viewed pattern, weak patterns over the last 30 days) is already
on-device in `localStorage`.

This is the well-known design pattern: **expert rules > ML when you
have the expertise and not the data**. We have the expertise.

---

## 2. Rule catalogue

The 14 rules in `js/pedagogy-recommender.js`, in **priority order**
(first to fire wins).

| ID | Name | Triggers when | Recommends | Pedagogical rationale |
|---|---|---|---|---|
| **R-01** | clear large review queue | `dueTotal ≥ 30` | `#/review` | Backlogs that big mean the SRS schedule has already slipped. Reviewing now preserves the spacing curve. |
| **R-02** | clear medium review queue | `10 ≤ dueTotal < 30` | `#/review` | Steady daily review at this size keeps retention curves healthy. |
| **R-03** | clear small review queue | `0 < dueTotal < 10` | `#/review` | Small queue = clean schedule. Don't let it grow. |
| **R-04** | revisit weakest pattern | a single pattern has `≥3` recent (≤30d) wrong answers | `#/learn/<id>` | Repeated misses mean the explanation didn't stick the first time. Re-reading the pattern (not just drilling) breaks the wrong-answer loop. |
| **R-05** | starter pack for new user | learner is brand new (no history) | `#/learn/n5-001` (first of 5) | Foundational machinery (です・は・ます・い-adj・か) is the bones every other N5 pattern hangs on. |
| **R-06** | resume last session | last-viewed pattern exists | `#/learn/<lastId>` | Working memory of an open pattern fades within hours; finishing it consolidates. |
| **R-07** | diagnose first | barely-touched grammar (<5 %) and no due queue | `#/diagnostic` | Placement check finds the real starting line in 10 minutes. Avoids learners restudying material they already know. |
| **R-08** | daily-goal nudge | today's progress <50 % AND no due queue | `#/drill` | Daily mixed practice keeps recall sharp on days when SRS happens to be empty. |
| **R-09** | minority-coverage surface | one skill (listening / reading / kanji) is <5 % done | the under-served skill | Single-skill silos are fragile; even one item from the under-served lane keeps progress balanced. |
| **R-10** | lateral swap | grammar >20 % done AND listening / kanji <5 % | the under-served skill | Grammar without sound is half a language; kanji recognition becomes blocking by mid-N5. Swap before either gap calcifies. |
| **R-11** | re-read just-explored | returning user, no other rule fired | `#/learn/<lastId>` | Second-pass reading is when long-term encoding happens. |
| **R-12** | acknowledge goal met | learner has practiced today AND queue is clear | `#/summary` (not a study action) | **Streak protection:** never pile on more recommendations after the goal is met. Acknowledge and step back; tomorrow is a fresh slot. |
| **R-13** | continue explore (catch-all) | returning user, nothing else fires | `#/learn` | Open Learn hub; let the learner pick the next thread. |
| **R-14** | mock paper ready | grammar ≥60 % AND kanji ≥50 % | `#/test` | Coverage is broad enough that a timed mock now reveals real exam-shape gaps. Do one before piling on more content. |

---

## 3. Tunables

All thresholds in one place, in `js/pedagogy-recommender.js`
`TUNABLES` constant. Each is justified below; **don't change without
updating both the rule above and this section**.

| Constant | Value | Why this number |
|---|---|---|
| `REVIEW_HIGH_DUE` | 30 | Above ~30 cards, a typical learner can't clear the queue in one sitting; we surface "clear now" before any other rule because the SRS schedule is at risk. 30 is the typical N5 daily-target ceiling × 1.5. |
| `REVIEW_MED_DUE` | 10 | Below 30 but above 10, the queue is **doable in one sitting** without exhausting the learner. Surface as a second-tier action. |
| `WEAK_PATTERN_WRONG_COUNT` | 3 | Two misses can be noise; three is a pattern. Threshold borrowed from typical N5 classroom error-tracking practice. |
| `STARTER_PACK_SIZE` | 5 | The 5 patterns picked are the absolute floor (です, は, Verb-ます, い-adj, か). Any new learner needs all 5 within their first hour. |
| `DAILY_GOAL_PCT_FLOOR` | 50 | Below 50 % of today's goal, gentle nudge. Above 50 % we trust the learner to finish. |
| `COVERAGE_FLOOR` | 0.05 (5 %) | If any skill has been touched <5 %, that's a silo risk. 5 % = ~1 listening drill or ~5 kanji or ~2 reading passages — ridiculously low bar so the rule fires for genuinely-untouched lanes only. |
| `LATERAL_SWAP_GRAMMAR_PCT` | 0.20 (20 %) | At ~36 grammar patterns done (20 % of 178), the learner has enough machinery that swap to listening / kanji yields more growth than another grammar. |
| `LATERAL_SWAP_KANJI_PCT` | 0.20 (20 %) | Symmetric. |
| `MOCK_READY_GRAMMAR_PCT` | 0.60 (60 %) | At ~107 patterns, the typical N5 mock paper hits ≥80 % of the grammar shown. Below this, mock papers are demoralising rather than diagnostic. |
| `MOCK_READY_KANJI_PCT` | 0.50 (50 %) | At ~53 kanji, reading sections become navigable; below this, the mock-test reading section is a kanji-recognition test, not a comprehension test. |

---

## 4. Privacy guarantees

The recommender is bound by these constraints:

- **No fetch / no XHR / no WebSocket / no `sendBeacon`.** The module
  imports only `./storage.js`. Grep for these in
  `js/pedagogy-recommender.js`:
  ```
  fetch(    sendBeacon(    new XMLHttpRequest    new WebSocket
  ```
  All zero matches.
- **No telemetry.** Recommendations are computed and rendered locally;
  no record is kept of what was recommended.
- **No cloud model load.** No dynamic imports outside the existing
  bundle.
- **No `Math.random`.** Recommender is deterministic — same state in,
  same recommendation out. Tests can pin behaviour.
- **No time-of-day variance.** A learner doesn't get different advice
  at 2 AM vs 2 PM unless their state changed.

**Independently verifiable:** open DevTools → Network tab on
`#/home`. The recommender's invocation triggers zero network
requests.

---

## 5. Testing

Each rule is a pure function returning either a recommendation
object or `null`. Unit-testing is straightforward:

```js
import { gatherSignal, recommend } from './js/pedagogy-recommender.js';

// Test R-04: weak-pattern surfacing
const signal = {
  isReturning: true,
  dueTotal: 0,
  goalMet: false,
  goalPct: 0,
  reviewsToday: 0,
  dailyGoal: 20,
  dueBySkill: { grammar: 0, vocab: 0, kanji: 0 },
  completionPct: { grammar: 0.5, vocab: 0.3, kanji: 0.4, reading: 0.3, listening: 0.3 },
  seenPatterns: new Array(89).fill().map((_, i) => `n5-${String(i+1).padStart(3, '0')}`),
  masteredPatterns: [],
  weakPatterns: ['n5-115'],
  wrongByPattern: new Map([['n5-115', 4]]),
  lastLearnId: 'n5-001',
  counts: { grammar: 178, vocab: 1041, kanji: 106, reading: 45, listening: 47 },
};
const rec = recommend(signal);
console.assert(rec.rule_id === 'R-04', 'expected R-04 to fire');
console.assert(rec.surface === 'learn');
```

A browser-runnable test page is tracked as next-cycle work
(`tests/recommender.test.html`).

---

## 6. How to add a rule

Two moves, both small:

1. Author the rule function in `js/pedagogy-recommender.js`. Keep it
   pure: input is `signal`, output is a recommendation or `null`.
   Assign a new `rule_id` like `R-15`.
2. Insert it into the `RULES` array at the correct **priority**
   position. Priority is encoded by array index — earlier = higher
   priority.
3. Document it in § 2 above. Without § 2 documentation the rule is
   considered un-reviewed and will be reverted at the next round.

That's the contract.

---

## 7. How to disable the recommender entirely

Edge case: a learner who finds the recommendation noisy can disable
it via Settings → "Show study suggestions" toggle (TODO — currently
hard-on; toggle work tracked as a follow-up under `IMP-NEXT-1`).
Until that ships, the workaround is removing the `<aside
class="home-recommend">` from `js/home.js#renderHome` in your fork.

The privacy story is unaffected either way — no recommendation = no
recommendation computed; computing one = no data leaving the device.

---

## 8. Future work (out of scope for round-9)

- **Per-locale `why_*` strings** — currently `why_en` + `why_hi`
  hand-authored; a future round can add per-locale variants without
  changing the rule logic.
- **Settings-toggleable recommender** — see § 7.
- **Recommender debug overlay** — DevTools-only "show me the signal"
  panel for advanced learners who want to understand why a particular
  rule fired. Tracked as next-cycle.
- **R-15+** — additional rules from the JA-teacher persona. Common
  candidates:
  - "It's been > 7 days since you opened a kanji card; try one." (decay)
  - "Your accuracy on counter-questions is < 60 %; revisit the
    counters module." (skill-targeted)
  - "Your last 3 mock papers all stalled on dokkai mondai 4; try
    re-reading passages first." (mondai-specific)

These rules require fielding signal we don't yet aggregate. Adding
them is straightforward once the signal accessors exist in
`js/storage.js`.

---

*Authored by the project's resident 日本語教師 persona. Reviewed
2026-05-07.*
