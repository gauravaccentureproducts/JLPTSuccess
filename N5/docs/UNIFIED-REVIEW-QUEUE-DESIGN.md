# Unified Daily Review Queue — design brief

> **Closes:** IMP-092 (architectural decision authored 2026-05-07).
> **Status:** Design accepted; Phase 1 implementation incremental;
> Phase 2/3 follow as SRS schema for vocab + kanji ship.

## Problem

Today the review queue is per-skill silos. The learner gets three numbers
(grammar reviews due, vocab reviews due, kanji reviews due) — instead of
one. Anki / RemNote / Renshuu present a single unified daily queue.
Three numbers is a friction tax: the learner has to mentally aggregate
"how much do I owe today", and the silos discourage cross-skill mixing
which is pedagogically optimal (interleaving > blocking for retention).

## Constraints (from the project's existing decisions)

1. **No accounts, no cloud sync.** All SRS state lives in `localStorage`.
   Whatever queue infrastructure ships must work fully offline.
2. **No gamification.** Don't add streaks / XP / leaderboards even in the
   review surface. The unified queue is about reducing friction, not
   adding stickiness.
3. **Per-level isolation.** N5 SRS state lives under
   `jlpt-n5-tutor:*` localStorage namespace; N4/N3/etc. get their own
   namespace when those levels ship. The unified queue is per-level.
4. **SM-2 today, FSRS-4.5 target.** SVA-Q1 in the strategic-value-adds
   queue is "FSRS upgrade." Whatever schema ships must accommodate the
   FSRS migration without a localStorage rewrite (i.e., FSRS state can
   live alongside SM-2 state via a versioned envelope).

## Current state

### Grammar (existing)

`storage.getHistory()` returns a `pid -> entry` map with SM-2 fields:
```
{
  pid: 'n5-001',
  reps: <int>,
  efactor: <float>,
  interval: <days>,
  nextDue: <ISO8601>,
  isMastered: <bool>
}
```

`#/review` page surfaces `nextDue ≤ now` items + N new items/day.

### Vocab (today)

No SRS state. Only a binary `knownVocab[form]: true` flag in localStorage.

### Kanji (today)

No SRS state. Only `knownKanji[glyph]: true` flag.

## Proposed unified architecture

### 1. Versioned multi-skill SRS envelope (Phase 1 storage migration)

Replace the existing flat `history` localStorage key with:

```js
{
  schemaVersion: 2,
  algorithm: 'sm-2',  // 'fsrs-4.5' on Phase 3 upgrade
  grammar: {
    'n5-001': { reps, efactor, interval, nextDue, isMastered },
    ...
  },
  vocab: {
    'n5.vocab.1-...': { reps, efactor, interval, nextDue, isMastered },
    ...
  },
  kanji: {
    '日': { reps, efactor, interval, nextDue, isMastered },
    ...
  }
}
```

**Migration**: on first load post-Phase-1 deploy, wrap the existing
flat `history` map under `.grammar`, set `schemaVersion: 2`, leave the
other skill maps empty. Backward-compatible: storage helpers that
read `getHistory()` for grammar continue to work.

### 2. Unified queue computation (Phase 2)

A new `getDueItems()` function aggregates across all three skill maps:

```js
function getDueAcrossSkills() {
  const state = storage.getMultiSkillState();
  const now = Date.now();
  const out = [];
  for (const [skill, items] of Object.entries(state)) {
    if (skill === 'schemaVersion' || skill === 'algorithm') continue;
    for (const [id, entry] of Object.entries(items)) {
      if (entry.nextDue && new Date(entry.nextDue).getTime() <= now) {
        out.push({ skill, id, entry });
      }
    }
  }
  // Interleave: round-robin per skill so the learner sees mix
  return interleaveByMod(out, 'skill');
}
```

**Interleaving** is the key UX choice — present cards round-robin
across grammar/vocab/kanji, not blocked by skill. Improves retention
per cognitive-science research on interleaved practice.

### 3. UI surfaces (Phase 2)

- `#/review` becomes the unified daily queue:
  - Header: "Today: 47 reviews due (12 grammar · 23 vocab · 12 kanji) · 8 new"
  - Single 4-button grading surface
  - Card-type indicator badge (small, top-right): 文 (grammar) / 語 (vocab) / 漢 (kanji)
  - 4-button grades route through skill-specific SRS update functions
- Per-skill review (legacy `#/learn/grammar`, `#/learn/vocab`,
  `#/learn/kanji`) stays available for skill-specific drill sessions
- Home page card replaces "12 grammar reviews / 23 vocab / 12 kanji"
  with "47 reviews due today" + small per-skill breakdown subtitle

### 4. New-card admission (Phase 2)

Currently grammar review admits N new patterns/day from the corpus.
The unified queue applies the same logic per skill:
- N grammar new/day (default 10)
- M vocab new/day (default 10)
- K kanji new/day (default 5)

Total daily new cards: ~25 by default. User-configurable per skill in
Settings (already exists for grammar; add vocab+kanji controls in
Phase 2).

### 5. Vocab-card / kanji-card rendering (Phase 2)

Vocab card: form + reading (furigana) + example sentence; user
self-grades on whether they recalled the gloss before flipping.
Kanji card: glyph + on/kun + example compound; user self-grades on
recognition.

Both reuse the existing 4-button grading surface (Again / Hard /
Good / Easy). SM-2 state updates per skill independently (different
ef-factor curves are OK; future FSRS-4.5 will normalize).

### 6. FSRS-4.5 migration path (Phase 3)

When SVA-Q1 ships, the multi-skill envelope's `algorithm` field
flips to `fsrs-4.5`. Per-skill states preserve existing reps but
recompute intervals via FSRS's stability/difficulty formula. Interval
crossover: `fsrs-4.5` reviews start being scheduled; existing SM-2
intervals carried forward for items not yet re-rated.

## Implementation phases

| Phase | Scope | Effort | Status |
|---|---|---|---|
| **0 (this brief)** | Architectural decision documented | 2 hrs | ✅ Done |
| **1 — Storage migration** | localStorage schema bump v1→v2; backward-compatible read helpers | 1 day | 🚧 Pending |
| **2 — Unified queue UI** | `#/review` round-robin + vocab/kanji card render + home aggregate | 3-5 days | 🚧 Pending |
| **3 — FSRS-4.5 upgrade** | (also closes SVA-Q1) | 2-3 days | 🚧 Pending |

## Acceptance criteria

- [ ] localStorage envelope has `schemaVersion: 2` with grammar+vocab+kanji maps
- [ ] `#/review` shows a single daily queue interleaved across skills
- [ ] Home page card shows "X reviews due today" (single number, with per-skill subtitle)
- [ ] Vocab cards + kanji cards render with the same 4-button grading
- [ ] No accounts / no cloud / no gamification added
- [ ] Migration from v1 envelope is idempotent + backward-compatible
- [ ] Existing grammar SRS behavior preserved (regression test)

## What this brief is NOT

- Not an implementation pull-request. The phases above each ship as
  separate commits with their own review.
- Not a commitment to FSRS-4.5 timing. Phase 3 ships when SVA-Q1 is
  prioritized; Phase 2 doesn't depend on it.
- Not a UI mockup. Layout decisions (single-column vs split-pane) are
  left to the Phase 2 implementor.

## Cross-references

- Registry item: IMP-092 (this brief closes the architectural-decision
  side; implementation phases ship as separate items)
- Strategic value-add: SVA-Q1 (FSRS-4.5 upgrade — Phase 3 dependency)
- Anti-item: ANTI-2 (no streaks / XP / leaderboards) — re-read before
  any review-surface UI choice
- Related: existing `js/review.js` (grammar SRS today)
