# Changelog archive (v1.0.0 - v1.9.0)

These entries pre-date the v1.10.0 syllabus-dashboard milestone (2026-05-02).
They are kept verbatim for historical reference only — see `../CHANGELOG.md`
for the active backlog.

---

## v1.9.0 - 2026-05-02 (Japanese-first language sweep)

User direction: the learner-facing surface should be in Japanese, not English. Closes a series of parallel cleanups across reading, listening, and shared UI chrome.

### Changed (user-visible)
- **Dokkai (reading) passage titles → Japanese.** All 30 passage titles in `data/reading.json` rewritten from English (e.g. "My family") to N5-scope Japanese (e.g. わたしの かぞく). Title kanji verified against the 111-entry N5 catalog.
- **English passage translation panel removed from dokkai.** The "Show English translation" `<details>` block is gone from `js/reading.js`; the corresponding `translation_en` field has been deleted from all 30 passages in `data/reading.json`.
- **Reading-list metadata Japanified.** Level (`easy`/`medium`/`info-search` → やさしい/ふつう/じょうほうけんさく) and topic (19 distinct values, e.g. `family` → かぞく) now render in Japanese via lookup maps. Data values remain English keys for code stability.
- **Listening item titles → Japanese.** All 30 `title_en` fields in `data/listening.json` migrated to `title_ja` (e.g. "Where to meet" → どこで 会いますか, "Buying a ticket" → きっぷを 買う). Renderer uses the existing furigana pipeline; kanji-glyph popovers still work.
- **Listening format taxonomy in kana.** `課題理解 / ポイント理解 / 発話表現` (which contain non-N5 kanji) now render as `かだいりかい (タスクりかい) / ポイントりかい / はつわひょうげん` so the format names stay readable for an N5 learner.
- **UI page chrome Japanified** across reading + listening modules: page titles ("Reading practice" → どっかい れんしゅう, "Listening practice" → ちょうかい れんしゅう), intro paragraphs, back/start buttons, feedback labels (Correct/Wrong → せいかい/ざんねん), result stats (Score/Accuracy → スコア/せいかいりつ), section toggles (Show passage → ぶんしょうを 見る), expand/collapse-all controls.
- **Mock-test paper bunpou paper-7 restored.** New `parse_mondai3_passages()` in `tools/build_papers.py` correctly handles passage-grouped Mondai-3 grammar questions (Q91-Q100 from `KnowledgeBank/bunpou_questions_n5.md`); the rationale-leak bug that swallowed the next passage header into Q95's rationale is also fixed (tightened section-break regex to `^#{2,3}\s+(?!Q\d)`).
- **Bunpou stem N5-kanji cleanup.** Replaced 朝→あさ, 東京→とうきょう, 大阪→おおさか, 公園→こうえん, 牛乳→ぎゅうにゅう, 思います→おもいます, 楽しい→たのしい across 10 occurrences in bunpou paper stems and Mondai-3 passages. Also fixed one goi stem (Q17). Dokkai retains these kanji per its formalized naturalness exception (see JA-28 below).

### Added (invariants - locks the work in)
- **JA-26** - no duplicate question IDs in `data/questions.json` (closes a parallel-session collision class that hit twice across Pass-15 / Pass-16).
- **JA-27** - `data/reading.json` and `data/listening.json` may not carry `title_en` or `translation_en` fields. Prevents regression of the EN-removal direction.
- **JA-28** - `data/papers/dokkai/*.json` content is bounded by N5 catalog ∪ documented exception list (`data/dokkai_kanji_exception.json`, 25 kanji). Any new non-N5 kanji must be either kana-ized or explicitly added to the exception JSON. Bunpou / moji / goi stay strictly N5 via JA-13.

### Removed (cleanup)
- 16 dead `translation_en` fields in `data/questions.json` that no runtime path read (verified zero `q.translation_en` / `question.translation_en` / `item.translation_en` references). Grammar.json `translation_en` is intentionally retained - `js/learn.js` and `js/review.js` actively render those for grammar-pattern teaching.
- Redundant `lang="ja"` attributes on wrapper elements in `js/reading.js`. `renderJa()` already wraps output in `<span lang="ja">` so the parent attributes were producing nested duplicates in the DOM; the parent-level attribute is dropped.

### Tooling
- `tools/fix_dokkai_titles_remove_en.py` - idempotent EN→JA migration for reading.json
- `tools/fix_listening_titles_ja.py` - idempotent EN→JA migration for listening.json
- `tools/audit_dokkai_kanji_scope.py` - read-only inventory of non-N5 kanji in dokkai papers (used to seed JA-28's exception list)
- `tools/fix_remove_dead_translation_en.py` - idempotent removal of dead questions.json fields
- `tools/fix_pass23_round2.py` and `tools/fix_dedup_q0479_q0488.py` - Pass-23 round 2 audit fixes (multi-correct prompts, scope-leak prompts, q-0479..q-0488 ID dedup)

v1.9.0 / SW v82. **37/37 invariants green** (was 35; added JA-26 + JA-27 + JA-28 across this milestone).

---

## v1.8.2 - 2026-05-01 (Pass-14 Phase A: delete 38 stub questions)

### Fixed
- **Question bank quality** - applied F-14.1 from the Pass-14 audit. Deleted 38 "pattern-meta" questions (q-0280 through q-0416 family) that taught nothing. All matched the stub format `「つぎの いみに あう パターン: ～X～ れい:...」`. The flaws:
 - Answer was literally quoted in the stem (e.g., stem said "パターン: ～たり～たりする" and "～たり～たりする" was one of the choices).
 - Distractors mixed wildly different types in the same option set (a particle alongside a pattern label alongside an adverb chain), so a learner could rule out 3 of 4 options just from format.
 - Prompt said "fill the blank" but the stem had no blank.
 - One question (q-0382) had a rendering corruption - double colon from a Pass-12 cleanup leftover.
- **Bank size**: 181 → 143 real questions. Every remaining question has valid pedagogical structure (no answer-in-stem, no distractor-type mismatch, no prompt-stem mismatch).

### Cascade-resolved
Deleting F-14.1 also closed F-14.2 (answer-in-stem, 4 questions), F-14.3 (q-0382 corruption), F-14.4 (prompt-stem mismatch in 37 questions), F-14.7 (distractor-length asymmetry), and F-14.8 (incompatible-type mixing). 6 audit findings closed in one mechanical pass.

### Still open from Pass-14
- F-14.5: q-0418 dual-mode schema (text_input + stale `choices` array). Decision needed.
- F-14.6: 33 ID gaps (q-0051 → q-0220 jumps 168). Decision needed: keep / renumber / document.
- F-14.9: inconsistent slash convention in `choices` (~40 entries).
- F-14.10: type distribution skew (138 mcq / 4 sentence_order / 1 text_input). Author more non-mcq.

v1.8.2 / SW v61. 26/26 invariants green.

---

## v1.8.1 - 2026-05-01 (Settings danger zone)

### Added
- **Danger-zone visual treatment** for the existing Reset Progress flow (`js/settings.js`). The destructive action now sits below the regular settings, separated by `--space-8` of whitespace and a thin red top border. A red "DANGER ZONE" label in `--tracking-label` ALL-CAPS calls extra attention. The pre-existing typed-phrase confirmation gate ("Type `RESET` to confirm") still gates the actual destruction - belt + suspenders.
- New `.reset-confirm-box` styling: red-tinted bg, hairline incorrect border, monospace `RESET` input, secondary Cancel button.

### Why
The Reset action wipes 11 categories of state (FSRS schedule, study history, test results, streak, known-kanji flags, drill stats, manual overrides, diagnostic results, settings preferences, last-viewed lesson, weak-pattern tracking). For users who've used the app for weeks, that's a lot of personalized state. The danger zone adds visual quarantine to match the action's actual consequence.

v1.8.1 / SW v60. 26/26 invariants green.

---

## v1.8.0 - 2026-05-01 (Zen Modern design overhaul)

A comprehensive visual refresh per `specifications/jlpt-n5-design-system-zen-modern.md` (Muji-inspired). Hierarchy through typography and whitespace, hairlines instead of borders, no shadows / no gradients / no decorative icons. Total work shipped across 4 commits.

### Phase 1 - Foundation (commit `af38e11`)
- New `:root` token system: surfaces (bg/surface/surface-alt), hairlines (line/line-strong), text (text/text-muted/text-faint), brand accent (`#1F4D2E` deep forest, replaces warmer `#14452a`), semantic state (correct/incorrect/due each with tint).
- Type scale: `--text-2xs` (11px) through `--text-2xl` (32px). Body 15px (down from 16px) - tighter, content-heavy correct.
- Weights: 300 / 400 / 500 only. Audited and replaced 41 occurrences of weight 600/700 in `css/main.css`.
- Spacing scale 4px - 128px; Muji aesthetic favours the BIG end (96px between major sections).
- Container widths narrow/base/wide (640/880/1120).
- Border radius: 2/4/6 only - geometric, hard-edged, no SaaS 12-16px curves.
- Motion tokens: 120ms / 180ms / 300ms with iOS ease-out.
- **Dark mode: full parity** - every light token has a dark twin. Triggers via `prefers-color-scheme: dark` OR `data-theme="dark"`.
- Body has `font-variant-numeric: tabular-nums` globally (stats, counters, timers, SRS intervals align vertically).
- Smooth color transition on theme toggle.

### Phase 2 - Components (commit `4703202`)
- **Header**: 56px sticky, 0.5px hairline bottom; container-wide max; brand-link gets a `五` mark in a 24px hairline-bordered square (cultural anchor per spec §4.1).
- **Primary nav**: tabs with 1.5px accent underline on `.active` (replaces filled-pill background).
- **Section labels**: new component - ALL-CAPS text-2xs label + flex-1 hairline rule, used between major page sections.
- **Buttons**: unified `.btn-primary` / `.btn-secondary` / `.btn-ghost` / `.btn-danger` at h-36 base, h-28 sm, h-44 lg. Focus ring 2px accent + 2px offset.
- **Cards**: 0.5px hairline, 6px radius, hover lightens to surface-alt (no transform, no shadow).
- **`.card-index`** numbered indicator (Muji signature 01/02/03).
- **Pills**: status-only, 4 tinted variants.
- **Progress bar**: 2px height (was 6px) - present but barely there.
- **Table**: hairlines only, no vertical borders, no striping.
- **Form controls**: h-40, focus border-accent.
- **Footer**: hairline-top, muted single row.
- **Furigana ruby**: `.furigana-off rt {display:none}` + `.furigana-known rt {visibility:hidden}` toggle classes.
- **Dropped**: 8 `box-shadow` declarations + 5 `transform: translateY` hover lifts (spec §8 forbids both).

### Phase 3 - Page treatments (commit `70f5ad2`)
- **Learn hub**: 5 numbered cards (`01 Grammar` / `02 Vocabulary` / `03 Kanji` / `04 Dokkai` / `05 Listening`). Section labels "Reference" / "Practice" with hairline rule. Copy: "32 categories" → "5 sections" (matches v1.7.5 supercategories); "~1003" → "1003".
- **Home**: "Sections" section label above the 2 pillar cards, which now show `01 Learn` / `02 Test` numbered indices. Hyphens upgraded to em-dashes in body copy.
- **Header**: gear glyph `⚙` (rendering as colored emoji on some platforms) → "Settings" text link.
- **Drill choice grid**: 2-col fixed, max-width 560px, centered. 56px tall buttons, hairline border, accent-tint on `.selected` (was filled green).
- **Test setup card**: 1.5px top border in `--color-text` (formality cue per spec §5.8).
- **Settings**: single-column max-width 640px, transparent bg, hairline rows. New `.settings-danger-zone` scaffold with red top border + "DANGER ZONE" label.

### Phase 4 - Self-hosted fonts (this commit)
- **Inter** (300 / 400 / 500) shipped as woff2 in `fonts/`. Total Inter footprint: ~338 KB. Critical because the Muji aesthetic requires Inter Light (300) for hero headlines - system fonts have no true Light.
- **Noto Sans JP** (weight 400, per spec §2.3 Japanese is always 400) subset to N5 + N4 character coverage (hiragana + katakana + 106 N5 kanji + ~85 N4 kanji + ASCII + JP punctuation = ~740 chars). Built via `python -m fontTools.subset` with `brotli` compression. Output: 165 KB woff2 (down from 4.5 MB unsubsetted).
- **Total font footprint: ~503 KB**, all CSP `'self'` (no third-party network).
- **`<link rel=preload>`** on the two most-used (Inter 400 + Noto Sans JP 400) so first paint isn't a system-font flash.
- **`@font-face`** with `font-display: swap` so latin renders immediately with system fallback while the woff2 streams in.
- **`unicode-range`** on the Noto Sans JP face so the browser doesn't try this font for latin characters (Inter is preferred there).
- **SW precache** updated: 4 new woff2 entries, cache `v59`.

### Stats
- 4 commits / 4 phases.
- ~600 lines of CSS replaced or added.
- 41 weight-600/700 → 500 replacements.
- 8 box-shadows + 5 hover-lifts purged.
- 4 woff2 fonts, ~503 KB total install footprint addition.
- 26/26 content-integrity invariants green throughout.

---

## v1.7.11 - 2026-05-01 (UI cleanup: remove decorative emojis)

### Removed
- **All decorative pictograph emojis** from the UI per user direction. Specifically:
 - **Learn hub** (`renderHub` in `js/learn.js`): the 5 hub-card icons (📖 Grammar, 📚 Vocabulary, ✍️ Kanji, 📰 Dokkai, 🎧 Listening) and the lede sentence "Pick what you want to study. Each section is self-contained."
 - **Home streak** (`js/home.js`): 🔥 streak-flame icon. Streak count + label remain.
 - **Empty states**: 🌱 in `js/review.js` (2 places - no-due and no-history empty states); 📊 in `js/summary.js`.
 - **Offline indicator** (`js/pwa.js`): leading ⚠ removed; banner now reads plain "Offline - cached content only".
 - **Verb-class warning section** (`js/verb-class.js`): leading ⚠ removed from the "famous Group-1 exceptions" heading.
 - **Counter drill** (`js/counters.js`): the 11 per-counter pictograph icons (🍎 つ, 👤 人, 📄 枚, 🍶 本, 📕 冊, 🏢 階, 🎂 歳, 🍵 杯, ⏱ 分, 🕒 時, 💴 円). Replaced with the neutral geometric Black-Circle dot (`●`, U+25CF) for the count visualisation so the "show N objects" drill still works without using emoji.
- **Dead CSS**: `.hub-icon`, `.streak-flame`, `.empty-state .empty-icon` rules - orphaned after the markup removal above.

### Kept (intentional)
- **Typographic correctness markers** (✓/✗ in `js/test.js`'s review screen): Unicode Dingbats (U+2713 / U+2717), classified as text-presentation glyphs by default; these are the standard correct/incorrect indicators every testing UI uses, with color-coded CSS (green/red). Not pictograph emojis.
- **★ Mastered badge** and **★ graduated** labels: Black Star (U+2605), pure typographic geometric symbol, never renders as pictograph.

---

## v1.7.10 - 2026-05-01 (homograph disambiguation: vocab_ids per example)

### Fixed
- **Wrong example sentences on homograph vocab pages.** The かた "person (polite)" detail page was showing the example 「この かんじの 読みかたは なんですか」 - but 読みかた "way of reading" is a different かた (n5.vocab.37 "way of doing", not n5.vocab.1 "person"). Same class of bug existed for 75 other homograph clusters: は (tooth / leaf / topic-marker), ひと (person / one), ある (to be / a certain), いる (to need / to be), おく (to put / 100 million), ほん (book / counter for cylindrical), はい (yes / counter for cupfuls), かい (counter for floors / counter for times / shellfish), きる (to wear / to cut), から (from / because), が (subject-marker / but), と (with / when / and), どうも (somehow / thanks), and 60 more. Every example now carries an explicit `vocab_ids: [...]` list naming exactly which vocab entries it demonstrates; the renderer matches by ID, never by substring.

### Changed
- **`data/grammar.json`**: every example sentence (589 total) gained a `vocab_ids` field. Auto-tagged via `tools/link_grammar_examples_to_vocab.py` with 13 hand-coded disambiguation rules + POS-aware substring matching + verb / i-adj conjugation matching (handles ます-form, te-form, た-form, ない-form, potential, and i-adj くて / かった forms).
- **`js/learn.js#renderVocabDetail`**: filters examples by `ex.vocab_ids.includes(entry.id)` instead of substring on the form field. Backward-compat fallback to substring kept for any legacy data.

### Added (CI)
- **JA-17 invariant** "Grammar examples have vocab_ids (homograph guard)" - every grammar example with non-empty `ja` text must declare a `vocab_ids` list. Blocks any future regression. Now 26/26 invariants green.

### Tooling
- **`tools/link_grammar_examples_to_vocab.py`** (idempotent re-runnable): scans every grammar example, finds POS-aware substring matches against `data/vocab.json`, applies homograph disambiguation rules, and writes `vocab_ids` back. Falls back to over-linking for ambiguous homograph forms without explicit rules (safe per "over-link beats under-link" direction). Conjugation-fallback covers verbs and i-adjectives in inflected form (e.g. 行けません → 行く, いそがしくて → いそがしい, わかります → 分かる via reading).
- **Conjugation-collision post-filters**: 来る/きる kana ms-stem き collision (drops きる "to wear / cut" unless clothing/cutting context); 入る/はい kana stem collision (drops "yes" expression and "cupful" counter unless example starts with greeting); 行く/いけ collision in the Verb-て+はいけません idiom (drops "lake" noun).
- **Counter numeral-prefix guard**: 2-char counter forms (かい / ほん / はい) require an immediately-preceding numeral (0-9, fullwidth digits, 一二三…) so that かい inside かいました (買う conjugated) doesn't false-match the counter "1階".
- **Standalone-word boundary guard**: 2-char `expression`/`interjection` POS forms require a left word-boundary so that はい (yes) doesn't false-match inside すってはいけません.

### Stats
- 75 homograph clusters fully covered. 589/589 (100%) examples linked to ≥1 vocab entry. 473 homograph-disambiguation decisions made by the auto-tagger across the corpus.

---

## v1.7.0 - 2026-05-01 (FSRS-4 replaces SM-2)

### Changed
- **SRS scheduler upgraded from SM-2 to FSRS-4** (Free Spaced Repetition Scheduler v4 - the algorithm Anki ≥23.10 uses by default). FSRS-4 has empirically better recall prediction than SM-2 in published comparisons; for our use case it's a drop-in replacement that requires no new data collection and runs entirely in the browser.
- **Per-item state schema** gained `stability` (S, days the memory holds at 90% recall), `difficulty` (D, clamped 1-10), and `lastReview` (ISO timestamp). Legacy SM-2 fields (`easeFactor`, `interval`, `reps`, `lapses`) are preserved for migration and legacy badge UI but are no longer used at runtime.
- **Migration is automatic and lossless.** On the first FSRS-graded review of any pre-existing entry that has SM-2 state but no FSRS state, the scheduler seeds `stability` from the SM-2 `interval` and `difficulty` from the inverted ease-factor curve (EF 1.3 → D 10, EF 2.5+ → D ~2). Subsequent reviews update via FSRS-4. No user action needed; no progress lost.
- **Grading UI unchanged.** Drill review buttons still emit grades on the SM-2 1/3/4/5 scale (Again/Hard/Good/Easy); the scheduler translates internally to FSRS's 1/2/3/4 scale.

### Why it matters
- Better recall predictions → fewer items re-shown when not needed, fewer items missed when they are needed.
- Closes EB-4 Tier-1 from the 2026-05-01 external-blocked-items reframing (the v2.0 recommender was originally deferred indefinitely on the assumption that "richer recommender = needs telemetry"; FSRS-4 demonstrates a richer scheduler with zero new data).

### Note
- This is a code-only change. No grammar/vocab/listening/reading/kanji content was modified. All 25 content-integrity invariants remain green.

---

## v1.6.4 - 2026-05-01 (K-1 kanji example usage + Pass 14c/15a corrections)

### Added
- **Example-usage section on every kanji card.** Each of the 106 kanji detail pages now shows 1-3 N5-syllabus example words in a three-column table (form / reading / English gloss). Added between the readings strip and the Stroke order block. Form, reading, and gloss come from `data/kanji.json#examples`. The K-1 substitution rule is applied at data-time: if a useful word like 手紙 (letter) contains an out-of-scope kanji (紙), the form is authored as 手がみ - the target kanji stays kanji, the OOS kanji becomes its contextual reading. New JA-16 invariant guards this rule.
- **`tools/populate_kanji_examples.py`** (idempotent): auto-picks examples for 100 kanji from `data/vocab.json`; hand-curated `MANUAL_EXAMPLES` for 6 kanji (口/目/力/手/友/足) that had no vocab references in the corpus (recovered in Pass-13 but vocab corpus didn't catch up).

### Changed (Pass 14c - low-effort backlog batch, 2026-04-30 → 2026-05-01)
- **`audio_manifest.json` voice metadata.** Top-level `voice_default: "synthetic-gtts"`; per-item `voice` field stamped on all 631 entries. `tools/build_audio.py` now skips items marked `voice: "native"` so externally-recorded items (when EB-1 lands) aren't synthesized over.
- **何 primary reading**: なに → なん. Across N5 vocab compounds (何時/何曜日/何月/何日/何人), なん dominates; なに is correct only for the standalone 何ですか. Source (`tools/build_data.py` PASS10_PRIMARY_OVERRIDES) and generated JSON now agree. Note: the `primary` field is unused at runtime since Pass 13 auto-furigana removal - this is data correctness, not behaviour.
- **`questions.json` half-width parens** in 4 stage-direction wrappers (q-0028, q-0029, q-0032, q-0049): ASCII `(...)` → fullwidth `（...）` per Japanese typography norms.
- **Listening curriculum-prerequisite metadata.** `data/listening.json#n5.listen.005` got `requires_patterns: ["n5-030"]` + `_curriculum_note` documenting the nominalising-の dependency.
- **Dead CSS removed.** `.hero-stats`, `.trust-strip` and their nested rules were orphaned after v1.6.1's copy audit removed those DOM elements. ~28 lines.
- **meaning_ja consistency.** 7 patterns (n5-013, 019, 032, 047, 069, 111, 123) had placeholder meaning_ja (just the form quoted, or wrong concept); rewritten as proper short-noun-phrase definitions. n5-069 specifically had `「てある」` which is a different N4 grammar - replaced with `ことばを つなぐ どうしの かたち`.
- **vocab.json POS tagging.** Every one of 1003 entries now has a `pos` field (noun / verb-1 / verb-2 / verb-3 / i-adj / na-adj / adverb / particle / conjunction / interjection / pronoun / counter / numeral / demonstrative / question-word / expression). Section-name heuristic + gloss-pattern fallback.
- **こそあど → "Demonstratives" in user-facing UI.** Page heading, Learn-hub deep-dive link, grammar.json category labels, and vocab.json section labels all renamed. Code-internal use of こそあど (file names, route slugs, CSS classes, function names) retained - backend-only term.

### Added (CI tooling)
- **JA-15 invariant** "Audio refs resolve to files on disk" - walks `data/audio_manifest.json`, normalises Windows-style backslashes, asserts every entry's `path` exists. 631/631 verified at landing.
- **JA-16 invariant** "Kanji examples use only target-or-whitelist kanji" - guards the K-1 substitution rule.
- **`tools/test_build_data.py`** (4 regression tests): Bug A `[Ext]`-tagged headers parse, Bug B parenthetical doesn't fragment meanings, smoke test for plain headers, E2E real KB produces 106 clean entries. Wired into `content-integrity.yml` workflow.
- **`tools/llm_audit.py`** - Anthropic-API-driven content audit script as Pass-15 substitute (per the EB-2 automation analysis). Validated on a 5-pattern sample; full report at `feedback/llm-audit-validation-report.md`.
- **`tools/heuristic_audit.py`** - free $0 alternative to llm_audit.py: deterministic Python scans for the same issue classes the LLM caught. Run on full corpus in ~50ms.

### Changed (Pass 15a - heuristic audit, 2026-05-01)
- **45 fixes from a free heuristic audit of all 187 patterns.** Surfaced 60 findings (75% precision); fixed 45.
 - 38 patterns had auto-gen `Duplicate-cleanup redirect. See n5-XXX...` text reaching learners as `notes`. All cleaned.
 - n5-158 (〜だろう casual): examples were teaching the *polite* でしょう, not the casual だろう. Pedagogical inversion fixed.
 - n5-112 (〜ふん/ぷん counter): examples used 分 kanji, bypassing the kana counter readings the pattern teaches. Converted to ふん/ぷん.
 - n5-173/174/175 (must-do variants): 3 patterns shared a single example that demonstrated only n5-176. Each now has a distinct example.
 - n5-105 / n5-106: plain-form examples in patterns explicitly teaching the polite form. Standardised to polite.
- **Cumulative:** ~635 findings raised across Pass 1-15a, ~620 fixed, 2 deferred.

### Note
- v1.6.3 was an internal-only asset-version bump for the Demonstratives UI rename + skeleton polish; no separate user-facing changes beyond what's listed under v1.6.4.
- All changes verified: 25/25 content-integrity invariants green; all 4 CI workflows (`pages-build-deployment`, `content-integrity`, `lighthouse-ci`, `playwright-p0-smoke`) green on every commit since the playwright workflow was unblocked.

---

## v1.6.2 - 2026-04-30 (Stroke-order SVGs)

### Added
- **Stroke-order diagrams on every kanji card.** Drop-in of all 106 KanjiVG SVGs (CC BY-SA 3.0) at `svg/kanji/<glyph>.svg`. The placeholder text "Stroke-order SVG not yet shipped." that was visible on every one of the 106 kanji detail cards is gone. Each kanji card now shows the actual stroke-by-stroke diagram with stroke numbers.
- **`NOTICES.md`** at the repo root: third-party content attributions. KanjiVG entry includes source, license, copyright, and a note on the only modification made (codepoint-hex filenames renamed to literal-glyph filenames to keep on-disk names learner-readable; SVG payload byte-for-byte preserved).
- **`tools/fetch_kanjivg.py`** build script: fetches the 106 SVGs from KanjiVG's GitHub raw URLs. Idempotent (skips files already present). Used at build time only.

### Changed
- **Service worker precache** now derives the 106 SVG URLs at install time from `data/n5_kanji_whitelist.json` rather than hand-listing them. Avoids drift between data and precache.
- **Kanji card fallback message** rewritten: `Stroke-order SVG not yet shipped. Drop-in target: ...` → `Stroke-order diagram could not load.` (only visible when an SVG is missing or `<object>` fails to render).
- **CC BY-SA 3.0 attribution line** added under the stroke-order diagram on every kanji card, linking to <https://kanjivg.tagaini.net/>.

### Note
- This is a content-only addition. Zero changes to grammar/vocab/listening/reading data. All 23 content-integrity invariants remain green.
- SVG payload size: ~496 KB total across 106 files (avg ~4.7 KB each).

---

## v1.6.1 - 2026-04-30 (Copy audit: voice consistency)

### Changed
- **Hero copy rewritten** to remove sales-promo voice. Headline `Pass JLPT N5 with 15 minutes a day` → `JLPT N5 study material`; first-time CTA `Start your first lesson` → `Start a lesson`; returning-visitor h2 `Continue your N5 study` → `Continue`. No factual changes; voice now matches an institutional reference site (think MIT OpenCourseWare) rather than a SaaS landing page.
- **Hero trust strip removed** from the page body. The same facts (offline, no account, local storage) are now reachable via the `Privacy` link in the footer; on-page repetition was the marker of marketing voice.
- **Hero stats** reverted from pill badges to a flat dot-separated list - pills read as a stat-card scoreboard; flat reads as a table of contents.
- **Recommender widget** copy rewritten: `What should I study next?` → `Suggested next`; `Keep your 5-day streak alive` → `Continue (5-day streak)`; `Clear today's review queue` / `Run today's review` → `N reviews due today`; `Try a quick mixed drill` → `Mixed drill`; `Pick up the next lesson` → `Next lesson`. Numbers are the motivator; imperatives removed.
- **Returning resume cards** copy rewritten: `Continue where you left off` → `Resume`; `Today's review queue` → `Reviews due today`; `All caught up - come back tomorrow.` → `No reviews due.`; `Learn something new` → `Open Learn`.
- **Streak label** simplified: `5 day streak` → `5 days`; the heading-style "streak" word removed.
- **Site title** `JLPT N5 Grammar Tutor` → `JLPT N5 - study material`. Per UI brief §1.1 #1: "Grammar Tutor" undersells (vocab, kanji, reading, listening are also part of the corpus).
- **Meta description** rewritten in plain English (`Free JLPT N5 study material covering grammar, vocabulary, kanji, reading and listening. Works offline; no account.`) - replaces developer jargon (`Static, on-device, privacy-preserving tutor for JLPT N5 grammar.`) which a non-developer searcher couldn't parse.
- **Drill answer feedback** glyphs dropped: `✓ Correct` / `✗ Not quite` → `Correct` / `Wrong`. Color + label is enough; the glyphs rendered inconsistently across platforms (Windows plain text vs mobile emoji).
- **Drill graduation message** `★ Graduated! This pattern is mastered.` → `Graduated. Pattern mastered.`
- **Counter-drill feedback** glyphs dropped (same rationale as above).
- **Summary empty state** copy rewritten: `Your dashboard fills in as you study.` → `Stats appear here once you've studied.`; `Start your first lesson` → `Start a lesson`.

### Note
- These are voice-only changes. No grammar/vocab/kanji content was modified. All 23 content-integrity invariants remain green.
- Voice contract recorded in `TASKS.md` under "Copy audit" so future copy doesn't drift back into marketing register.

---

## v1.5.0 - 2026-04-30 (UX Brief 2 - Phase 1-4)

### Added
- **Home screen** (#/home) is now the default landing page. First-time visitors see a CTA "Start your first lesson" + placement check link + 3-card pillars (Learn / Practice / Test). Returning visitors see a Continue card, Today's review queue, and a 7-day streak heatmap.
- **Search** across grammar / vocab / kanji from the header. Press `/` to focus. Works offline.
- **Three-mode furigana** (Always / Hide on known kanji / Never) in Settings, with a live preview.
- **Per-kanji popover**: click any kanji glyph to see on/kun-yomi + meanings + an "I know this" toggle that persists.
- **Single-kanji pages** (#/kanji/<glyph>) and the kanji index (#/kanji) showing all 97 N5 entries.
- **Keyboard shortcuts** (1-4 / Space / Enter / ? / Esc / /) with a `?` cheatsheet overlay.
- **Settings additions**: audio playback speed (0.75 / 1.0 / 1.25x), reduce-motion toggle, typed-phrase reset confirm ("Type RESET").
- **Skeleton placeholders** replace the legacy "Loading..." text on every route. 5-second timeout shows a real "Couldn't load this view" UI with Retry.
- **Empty states** for Review (no progress / no due), Summary (no progress), and Test (no completed tests).
- **Trust strip** on the landing screen ("Works offline / No login required / Your progress stays on this device") above the fold.
- **PWA install prompt** (one-time, dismissible).
- **Offline indicator** in the corner when the network drops.
- **"Update available" toast** when a new shell version is detected (stale-while-revalidate).
- **Streak tracking**: current + longest day-streak in localStorage, 7-day heatmap on home.
- **Mobile bottom-nav** at viewports ≤ 480px with iOS safe-area insets honored.
- **Print stylesheet** (`@media print`) for clean handouts of any Learn lesson.
- **Persistent location indicator** chip below the header showing the active route.
- **Deep links**: #/test/<n> for n ∈ {20, 30, 50} starts a test directly. #/kanji/<glyph> jumps to a kanji page.

### Changed
- **Tagline** updated to "Pass JLPT N5 with 15 minutes a day. No login, no ads, no data shared."
- **Footer** updated to "Works offline. No login. Your progress stays on this device."
- **Primary nav** restructured: Home / Learn / Practice (renamed from Daily Drill) / Review / Test. Summary + Settings moved to a secondary nav row.
- **Service worker** now uses stale-while-revalidate for the shell (HTML/CSS/JS) and cache-first for content (data/audio/locales). Posts an update message to clients when new shell bytes are detected.

## v1.4.0 - 2026-04-29 (Brief 1 - final assets)

### Added
- **491 audio files** for all grammar examples, reading passages, and listening scripts (gTTS Japanese voice, ~19 MB).
- **30 reading passages** (expanded from 8) with 2-3 comprehension questions each.
- **12 listening items** across the three JLPT N5 formats (4 task / 4 point / 4 utterance) with audio.
- Grammar example audio player in the Learn UI.

### Fixed
- `tools/build_audio.py`: `Path.with_suffix` was stripping the example index for IDs like `n5-001.0`. Switched to manual string concat so all 449 grammar example files render uniquely.

## v1.3.0 - 2026-04-30 (native-speaker audit Pass 8)

52 findings raised, 52 fixed. Severity: 16 HIGH, 27 MED, 9 LOW. Touched `moji_questions_n5.md`, `bunpou_questions_n5.md`, `goi_questions_n5.md`, `dokkai_questions_n5.md`, `externally_sourced_n5.md`. See `verification.md` §7.

## v1.2.0 - 2026-04 (UX Brief 1 / Phase 4 + 5)

- 187 patterns enriched, 250 questions written (no stubs).
- 1002 vocab entries + 97 kanji entries.
- Verb classification, て-form gym, counters, こそあど, は vs が, particle pairs modules.
- Reading + Listening shells.
- Settings panel + 5-locale i18n + PWA manifest + export/import progress.
- SM-2 SRS in Review with Again/Hard/Good/Easy grading.
- 37 browser-runnable tests.

## v1.0.0 - 2026 initial release

- Vanilla HTML/CSS/JS scaffold, hash router, LocalStorage adapter.
- 4 chapters + Drill + Diagnostic.
- Threshold-based weak detection.
- Service worker, offline-capable.
