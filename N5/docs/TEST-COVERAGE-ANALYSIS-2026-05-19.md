# Test-Scenarios Coverage Analysis — 2026-05-19

Source workbook: `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`

**Writing-discipline note.** Every claim below is bounded by what this script scanned. "0 coverage" means "no scenario string in the workbook contains the artifact identifier exactly as scanned"; false negatives are possible when a scenario references an artifact by synonym (e.g. "vocab module" vs `learn-vocab.js`). Numbers reflect counts at the workbook snapshot named above; future additions may change them.


# 1. Per-tab scenario counts

| Tab | Scenarios | P1/High | P2/Medium | P3/Low | Auto | Manual | Hybrid |
|-----|-----------|---------|-----------|--------|------|--------|--------|
| A. Japanese language | 124 | 4 | 15 | 84 | 10 | 101 | 12 |
| B. JLPT format | 19 | 0 | 2 | 9 | 8 | 11 | 0 |
| C. Hindi locale | 21 | 1 | 3 | 10 | 1 | 19 | 1 |
| D. UX design | 27 | 0 | 0 | 14 | 2 | 25 | 0 |
| E. Accessibility | 18 | 0 | 0 | 14 | 4 | 14 | 0 |
| F. Security | 23 | 6 | 0 | 10 | 13 | 10 | 0 |
| G. Privacy and legal | 16 | 0 | 0 | 11 | 2 | 14 | 0 |
| H. Performance | 24 | 0 | 0 | 15 | 9 | 15 | 0 |
| I. Data engineering | 26 | 1 | 3 | 11 | 10 | 15 | 1 |
| J. Pedagogy | 20 | 0 | 0 | 8 | 14 | 5 | 1 |
| K. QA testing | 57 | 1 | 25 | 12 | 32 | 25 | 0 |
| L. Cultural ethical | 11 | 0 | 0 | 7 | 0 | 11 | 0 |
| M. Operations | 14 | 0 | 0 | 1 | 1 | 13 | 0 |
| N. End-user POV | 17 | 0 | 0 | 7 | 1 | 16 | 0 |
| UI Tests | 55 | 0 | 26 | 29 | 55 | 0 | 0 |
| O. Mobile UI testing | 134 | 77 | 54 | 3 | 118 | 16 | 0 |
| **TOTAL** | **606** | | | | | | |

**Total scenarios across all tabs:** 606


# 2. Codebase artifact inventory (denominators)

- **SPA routes** (unique, normalized): 29  (grepped from index.html + js/*.js)
- **Route family roots**: 26 (e.g., `home`, `learn`, `kanji`, `reading`, ...)
- **JS modules** (js/*.js feature owners): 53
- **Data files** (data/*.json): 25
- **CI invariants** (JA-NN codes in tools/check_content_integrity.py): 125  *(may include duplicate mentions; count is of distinct codes)*

**Caveat:** these counts are what the regex picked up at scan time. The route count includes dynamic-route shapes (e.g., `learn/${id}`); after deduplication of dynamic params, the family-root count (~37) is the more meaningful denominator for screen-coverage.


# 3. SPA route coverage (mobile UI + UI Tests tabs)

Route-family coverage by mobile-UI / desktop-UI / QA tabs combined:

| Route family | Scenarios mentioning `#/family` |
|--------------|--------------------------------:|
| `#/authentic` | 1 |
| `#/changelog` | 1 |
| `#/diagnostic` | 1 |
| `#/drill` | 3 |
| `#/examday` | 1 |
| `#/feedback` | 1 |
| `#/home` | 9 |
| `#/kanji` | 3 |
| `#/learn` | 16 |
| `#/levels` | 1 |
| `#/listening` | 5 |
| `#/listeningstory` | 0 |
| `#/mining` | 1 |
| `#/missed` | 3 |
| `#/notices` | 1 |
| `#/papers` | 3 |
| `#/print` | 3 |
| `#/privacy` | 1 |
| `#/reading` | 4 |
| `#/review` | 4 |
| `#/settings` | 4 |
| `#/sitting` | 2 |
| `#/strategy` | 1 |
| `#/summary` | 3 |
| `#/test` | 5 |
| `#/weakareas` | 1 |

**Coverage**: 25/26 route families have ≥1 scenario (96%).

**Routes with 0 scenarios** (in the tabs scanned — UI/QA/UX/A11y/Mobile):
- `#/listeningstory`


# 4. JS module coverage (any tab)

**Coverage**: 25/53 JS modules referenced by name (47%).

**JS modules with 0 explicit mention** (may still be exercised indirectly via route scenarios):
- `js/app.js`
- `js/branding.js`
- `js/changelog.js`
- `js/content-protect.js`
- `js/corpus-export.js`
- `js/counters.js`
- `js/furigana.js`
- `js/home.js`
- `js/kosoado.js`
- `js/learn.js`
- `js/learn-grammar.js`
- `js/learn-vocab.js`
- `js/missed.js`
- `js/mondai-pacing.js`
- `js/normalize.js`
- `js/particle-pairs.js`
- `js/pedagogy-recommender.js`
- `js/provenance-badge.js`
- `js/romaji-kana.js`
- `js/score-estimator.js`
- `js/settings.js`
- `js/shortcuts.js`
- `js/sitting.js`
- `js/summary.js`
- `js/te-form.js`
- `js/test.js`
- `js/verb-class.js`
- `js/wa-vs-ga.js`


# 5. Data-file coverage (any tab)

| Data file | Scenarios mentioning it |
|-----------|------------------------:|
| `data/_ja91_baseline.json` | 0 |
| `data/_ja94_baseline.json` | 0 |
| `data/audio_manifest.json` | 1 |
| `data/audio_manifest_voice.json` | 0 |
| `data/authentic.json` | 3 |
| `data/branding.json` | 0 |
| `data/build_metadata.json` | 0 |
| `data/dokkai_kanji_exception.json` | 0 |
| `data/drills_auto.json` | 2 |
| `data/grammar.json` | 13 |
| `data/index.json` | 1 |
| `data/kanji.json` | 7 |
| `data/listening.json` | 4 |
| `data/n5_core_pattern_ids.json` | 0 |
| `data/n5_kanji_readings.json` | 0 |
| `data/n5_kanji_whitelist.json` | 0 |
| `data/n5_pitch_accent_reference.json` | 0 |
| `data/n5_vocab_whitelist.json` | 0 |
| `data/pattern_markers.json` | 1 |
| `data/questions.json` | 9 |
| `data/reading.json` | 3 |
| `data/recording_directions.json` | 0 |
| `data/test_strategy.json` | 0 |
| `data/version.json` | 3 |
| `data/vocab.json` | 17 |


# 6. CI invariant coverage (any tab)

**Coverage**: 81/125 CI invariants referenced by name in scenarios (64%).

**Invariants with ≥1 scenario reference:**
- JA-1: 30 scenario(s)
- JA-10: 15 scenario(s)
- JA-100: 3 scenario(s)
- JA-101: 2 scenario(s)
- JA-102: 1 scenario(s)
- JA-103: 2 scenario(s)
- JA-104: 2 scenario(s)
- JA-107: 1 scenario(s)
- JA-108: 3 scenario(s)
- JA-109: 1 scenario(s)
- JA-11: 7 scenario(s)
- JA-110: 1 scenario(s)
- JA-113: 2 scenario(s)
- JA-115: 1 scenario(s)
- JA-116: 1 scenario(s)
- JA-118: 1 scenario(s)
- JA-119: 1 scenario(s)
- JA-12: 5 scenario(s)
- JA-120: 1 scenario(s)
- JA-121: 1 scenario(s)
- JA-122: 1 scenario(s)
- JA-123: 1 scenario(s)
- JA-127: 1 scenario(s)
- JA-13: 2 scenario(s)
- JA-18: 1 scenario(s)
- JA-19: 1 scenario(s)
- JA-2: 3 scenario(s)
- JA-22: 1 scenario(s)
- JA-24: 1 scenario(s)
- JA-29: 1 scenario(s)
- JA-3: 14 scenario(s)
- JA-30: 2 scenario(s)
- JA-31: 2 scenario(s)
- JA-32: 2 scenario(s)
- JA-33: 2 scenario(s)
- JA-35: 3 scenario(s)
- JA-37: 3 scenario(s)
- JA-39: 2 scenario(s)
- JA-4: 5 scenario(s)
- JA-41: 1 scenario(s)
- JA-47: 3 scenario(s)
- JA-48: 2 scenario(s)
- JA-5: 3 scenario(s)
- JA-53: 1 scenario(s)
- JA-59: 2 scenario(s)
- JA-6: 9 scenario(s)
- JA-60: 1 scenario(s)
- JA-61: 1 scenario(s)
- JA-62: 1 scenario(s)
- JA-64: 1 scenario(s)
- JA-67: 1 scenario(s)
- JA-68: 3 scenario(s)
- JA-69: 2 scenario(s)
- JA-7: 5 scenario(s)
- JA-70: 1 scenario(s)
- JA-71: 2 scenario(s)
- JA-72: 1 scenario(s)
- JA-75: 1 scenario(s)
- JA-77: 1 scenario(s)
- JA-8: 26 scenario(s)
- JA-80: 1 scenario(s)
- JA-81: 2 scenario(s)
- JA-82: 1 scenario(s)
- JA-83: 7 scenario(s)
- JA-84: 2 scenario(s)
- JA-85: 2 scenario(s)
- JA-86: 4 scenario(s)
- JA-87: 1 scenario(s)
- JA-88: 2 scenario(s)
- JA-89: 5 scenario(s)
- JA-9: 22 scenario(s)
- JA-90: 3 scenario(s)
- JA-91: 4 scenario(s)
- JA-92: 1 scenario(s)
- JA-93: 3 scenario(s)
- JA-94: 3 scenario(s)
- JA-95: 3 scenario(s)
- JA-96: 2 scenario(s)
- JA-97: 2 scenario(s)
- JA-98: 2 scenario(s)
- JA-99: 2 scenario(s)

**Invariants with 0 explicit scenario reference** (44):
JA-105, JA-106, JA-111, JA-112, JA-114, JA-117, JA-124, JA-125, JA-126, JA-128, JA-129, JA-130, JA-14, JA-15, JA-16, JA-17, JA-20, JA-21, JA-23, JA-25, JA-26, JA-27, JA-28, JA-34, JA-36, JA-38, JA-40, JA-49, JA-50, JA-51, JA-52, JA-54, JA-55, JA-56, JA-57, JA-58, JA-63, JA-65, JA-66, JA-73, JA-74, JA-76, JA-78, JA-79


# 7. Priority + severity distribution (workbook-wide)

**Priority distribution:**

- P3: 245
- P2: 128
- P1: 90
- P4: 84
- P5: 59

**Severity distribution:**

- Major: 391
- Minor: 202
- Critical: 13

**Test type distribution:**

- Manual: 310
- Automated (Selenium): 113
- Auto: 106
- Automated (Selenium 4): 55
- Auto+Manual: 10
- Hybrid: 5
- Automated (Selenium + visual-diff): 2
- Blocked — depends on Hindi audio: 1
- Automated (Playwright): 1
- Automated (Lighthouse): 1
- Automated (Selenium + axe-core): 1
- Automated (Selenium + CDP): 1


# 8. Identified gaps + recommendations

These are derived from sections 3-6 above. Each gap is named explicitly so a follow-up tab/scenario addition can close it.

### 8.1 Routes with 0 mobile-UI/QA scenarios
- `#/listeningstory` — add scenarios to `O. Mobile UI testing` (or `UI Tests`) covering: initial load, primary CTA, navigation in/out, locale-switch.

### 8.2 JS modules with no scenario reference
- 28 of 53 JS modules have 0 explicit name reference in any scenario.
- Many may be exercised indirectly via route-level scenarios (e.g., `storage.js` is touched by every progress-bearing scenario).
- Cross-check needed: for each, decide whether it's a leaf utility (no UX surface) or a feature that lacks scenario coverage.

### 8.3 CI invariants with no scenario reference
- 44 of 125 invariants have 0 explicit reference in scenarios.
- CI invariants are gated structural checks, not user-facing UI behavior — so 0-mention is expected for many. However, scenarios in tab `I. Data engineering` should ideally explicitly name each invariant they validate.

### 8.4 Manual-test backlog (cannot be Selenium-automated)
- Manual scenarios total: 310.
- These need a human runner — track as a separate execution calendar, not via CI.
- Common classes flagged Manual: VoiceOver/NVDA navigation, iOS audio-gesture, soft-keyboard occlusion, IME input, safe-area, pull-to-refresh, real-device PWA install.

### 8.5 Underrepresented dimensions (qualitative)
- **Error-injection / chaos**: very few scenarios cover network-mid-flow, storage-quota-full, SW-update-collision, concurrent-tab-state-conflict.
- **Internationalization stress**: HI is covered (tab C); other RTL/CJK-only locales are out of scope by project decision.
- **Telemetry / observability**: the project claims zero telemetry — there are 1-2 scenarios verifying "network tab is silent." Could be expanded to assert all network requests are first-party + cacheable.
- **Long-session memory pressure**: 1 scenario in O. tab; could expand to test 6-hour session leak detection.
- **Service-worker lifecycle**: 2 scenarios; SW is a complex subsystem deserving 8-10 scenarios (install/activate/skipWaiting/client claim/update flow/precache strategies/runtime caching/Background Sync if used).
- **Content-integrity at runtime**: data/*.json is validated at build by CI invariants, but no scenario verifies the RUNTIME renderer correctly displays the validated data (orphan-data trap documented in procedure-manual D.9.27).

### 8.6 Test-type balance
- Auto-only: ~46%  |  Manual-only: ~51%
- Healthy mix; investment in Appium would convert ~20 Manual soft-keyboard/IME scenarios to Automated.


# 9. Per-tab depth assessment (qualitative)

### A. Japanese language (124 scenarios)
Largest tab. Sub-categories thorough (Naturalness, Particles, Conjugation, Honorifics, Counters, Kanji, Pitch, Translation, Romaji, scope). Manual-heavy by necessity — most claims require native ear.

### B. JLPT format (19 scenarios)
Mondai structure + stem format + difficulty calibration well-named. Item-validity (p-value, biserial) scenarios deferred until learner-cohort data exists — flagged appropriately.

### C. Hindi locale (21 scenarios)
Naturalness + terminology + Devanagari typography + register + cross-language drift covered. Pan-Indian neutrality scenario is a strong addition.

### D. UX design (27 scenarios)
Visual hierarchy + color + typography + IA + onboarding + cognitive load + microinteractions + form input + dark mode + gamification — all named. Heuristic-evaluation-style; would benefit from time-on-task data once collected.

### E. Accessibility (18 scenarios)
WCAG-AA + screen-reader + motor + cognitive + hearing-impaired covered. Should add: WCAG-AAA spot-checks for 2.4.7 focus visible + 2.5.5 target size if claims include AAA.

### F. Security (23 scenarios)
XSS / CSP / supply-chain / secrets / pen-test / GitHub Actions covered. Static-site nature means surface is small; adequate for current threat model. Could add: subresource integrity, side-channel timing, fingerprinting resistance.

### G. Privacy and legal (16 scenarios)
Privacy / GDPR / DPDP / COPPA / license / trademark / advertising-claims covered. Adequate for the legal review completed 2026-05-11.

### H. Performance (24 scenarios)
Core Web Vitals + bundle + audio cache + PWA + cross-browser + mobile-responsive + font + i18n + SEO. Comprehensive for a PWA of this scope.

### I. Data engineering (26 scenarios)
Schema validation + versioning + CACHE_VERSION + backup + CI. GAP: scenarios should explicitly cite each JA-NN invariant they validate.

### J. Pedagogy (20 scenarios)
SLA + SRS + curriculum + assessment-validity + comparative + HI-L1 error anticipation. Some scenarios require learner-cohort data not yet collected; flagged Low priority.

### K. QA testing (57 scenarios)
Exploratory + automation + visual-regression + localization + audio playback. Includes Selenium-suite references. Now overlaps with O. Mobile UI testing; cross-link both tabs.

### L. Cultural ethical (11 scenarios)
JA + HI cultural sensitivity + AI ethics/disclosure + trust-safety. Adequate; depends on native reviewer for execution.

### M. Operations (14 scenarios)
DevOps + analytics + customer-support + documentation. Lightweight for the current solo-maintainer setup; would expand with team.

### N. End-user POV (17 scenarios)
Primary persona + self-study + classroom + returning + bilingual + emerging-market + visually/cognitively-diverse. Persona coverage is broad.

### UI Tests (55 scenarios)
59 Selenium scenarios from prior work. Now subset of mobile-UI coverage; consolidate or explicitly desktop-focus this tab to complement O. Mobile UI testing.

### O. Mobile UI testing (134 scenarios)
134 scenarios: 39 cross-cutting + 95 per-screen. Newest tab; names every SPA route family. Some scenarios marked Manual/Appium for what Selenium cannot reproduce.


# 10. Concrete coverage-expansion recommendations

Ranked by gap-size × user-impact:

1. **Add per-invariant scenario rows in `I. Data engineering`** — 44 of 125 CI invariants currently lack an explicit scenario citation. Each should have a single-row scenario stating: "JA-NN locks <named pattern>; regression test = run tools/check_content_integrity.py against a corpus seeded with the anti-pattern; expect failure."

2. **Service-worker lifecycle expansion in `O. Mobile UI testing`** — add 6-8 scenarios covering: install→activate transition, skipWaiting + clientsClaim, multiple-tab claim race, precache manifest hash mismatch recovery, runtime-cache eviction policy, Background Sync queue (if implemented), update-prompt UX, and stale-while-revalidate verification on key routes.

3. **Runtime renderer correctness** — add scenarios in `K. QA` or new tab `P. Renderer integrity` asserting: for each data field validated by CI invariants, the runtime DOM actually displays it. This closes the orphan-data trap (procedure-manual D.9.27) that lets `collocations` etc. ship without being rendered.

4. **JS module → scenario map** — annotate `js/*.js` files with a JSDoc `@coveredBy ID-list` comment so the link is bidirectional. 28 modules currently have no scenario name-cite.

5. **Long-session + chaos scenarios** — expand from current ~3 in `O.` and `K.` to a dedicated sub-category: 6h memory leak, storage-quota-full, IndexedDB corruption, sw-update mid-flow, tab-eviction recovery, system-time-jump (DST / NTP correction).

6. **Native-human review scenarios** — currently 0 specific scenarios for the native-Hindi review and the 43 pitch-accent `low`/`unverified` entries flagged in AUDIT-COVERAGE. Add as row entries (with realistic priority Low — pending funding).

7. **Visual-regression baseline establishment** — `O.` lists Per-route screenshot diff baseline as 2 scenarios; expand to per-route × per-locale × per-viewport matrix (37 × 2 × 5 = 370 screenshots). Treat as one master scenario with a checklist rather than 370 rows.

8. **Cross-link `UI Tests` and `O. Mobile UI testing`** — `UI Tests` (59 rows) is now ambiguous in scope after `O.` was added. Either retitle `UI Tests` → `UI Tests (Desktop)` or merge appropriately so a future executor knows which to run for which device class.


# 11. Coverage scorecard (point-in-time, bounded)

| Dimension | Coverage | Method | Confidence |
|-----------|----------|--------|------------|
| SPA routes (family roots) | 25/26 (96%) | Substring scan of `#/<family>` in scenario text | High *for the routes named in index.html/js as of commit cb97df1* |
| JS modules (named) | 25/53 (47%) | Substring scan of `<module>.js` | Medium *— indirect coverage via route scenarios is not counted* |
| CI invariants (cited) | 81/125 (64%) | Substring scan of `JA-NN` | Medium *— most invariants are structural and don't require user-facing scenarios* |
| Data files (cited) | 12/25 | Substring scan of filename | Medium |

Each percentage is bounded by what this script's substring matcher found; a scenario can exercise an artifact without literally naming it. The `medium` confidence labels acknowledge this.

---
*Analysis generated by `tools/analyze_test_coverage.py` against workbook snapshot `test-scenarios-by-specialist-perspective.xlsx` at the most recent commit.*
