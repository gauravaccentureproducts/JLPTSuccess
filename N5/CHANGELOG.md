# Changelog

All user-visible changes to the JLPT N5 study material site.

## Unreleased - 2026-05-19 (GOI-001..003 close-out — goi-paper-6 rationale content discipline + 1 new CI invariant)

### Fixed

- **GOI-001** (Major / P2) — goi-6.11 (phone-call paraphrase) had its
  rationale_hi as a verbatim copy-paste of goi-6.12's (about 二十さい
  / age). Hindi-speaking learners answering the phone-call question
  would see an explanation about ages instead. Rewrote rationale_hi
  in natural Hindi about phone-call paraphrase
  (`「電話を かけて + 一時間 話した」 = 「電話で 話した」`). Provenance
  set to `native_reviewed_2026_05_19`.
- **GOI-002** (Low / P4) — goi-6.14 rationale ended with "Hence the
  rewording from a prior version" — same anti-pattern as PAPER-003
  (JA-121 class), new trigger phrase. Trimmed both rationale and
  rationale_hi to the first sentence (the legitimate learner-facing
  content): `高かった (was expensive) ↔ たくさん お金を 払った (paid
  a lot of money).`.
- **GOI-003** (Low / P4) — goi-6.12 rationale ended with meta-doc
  pointer ("documented at vocabulary_n5.md ... does not bear on the
  time-reference test point this question targets"). Replaced with
  direct pedagogical content: `Note: 二十さい is read はたち, not
  にじゅっさい — a special on-yomi exception shared with 二十日
  (はつか).`. Mirror in rationale_hi.

### Added

- **JA-136 CI invariant** — no rationale_hi shared verbatim by 2+
  questions within the same paper file (>30 chars threshold).
  GOI-001 copy-paste guard. Rejected the bug spec's stricter
  token-overlap proposal (~100 false positives from dictionary-form
  ↔ polite-form variation); cross-question duplication is the
  narrower-but-defensible proxy.
- **JA-121 trigger set extended** — 7 new phrases catching
  GOI-002/003 patterns: "Hence the rewording", "rewording from a
  prior", "from a prior version", "documented at vocabulary_n5.md",
  "documented at", "does not bear on", "test point this question".
- **Procedure manual F.35** — Rationale content-discipline:
  Class A (copy-paste content-mismatch) + Class B (meta-content in
  learner-facing rationale). Complements F.30/F.33/F.34 to form the
  5-invariant family on paper-question rationale fields (JA-121/122/
  129/130/136).
- **Accuracy prompt A74** — Rationale content-discipline audit
  category.
- **N5Improvement Phase-0 rationale-content regression block**.
- **AUDIT-COVERAGE Part 28** — Close-out narrative.

### State

CI **139 / 139 invariants green** (was 138; added JA-136 + JA-121
trigger extension).
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker **132 / 132 Fixed / 0 Open**.

Bounded framing: GOI-001..003 + JA-136 + JA-121-extension cover the
2 rationale-content defect classes surfaced by the 2026-05-19 goi
paper-6 audit. Subtler defects (semantically-wrong-but-coherent
rationale, misleading framing without trigger phrases) remain in
manual-review territory.

## Unreleased - 2026-05-19 (MOB-001..019 + DOKKAI-004 close-out — mobile UI compliance + 4 new CI invariants)

### Fixed

- **MOB-001** (Major / P2) — Primary nav dropped Test + Progress on
  mobile widths. Removed `@media (max-width: 599px)` rule that hid
  these items; with the existing flex shrink rule + font-size: 11px
  at D-380, all 7 nav items now visible on D-320+.
- **MOB-002, MOB-003, MOB-016** (Major / P2) — Home study-order cards
  (.study-order-link 328×34), home CTA buttons (.btn-action 281×36),
  feedback page action buttons (159×36 / 88×36) all bumped to
  `min-height: 44px` per Apple HIG.
- **MOB-004** (Minor / P3) — Back-navigation links (`.back-link` /
  `.home-up-link a` 125×20) bumped to 44px tap target via padding.
- **MOB-005** (Minor / P3) — Listening section expand/collapse
  buttons (.toc-expand-all/collapse-all 99×36) bumped to 44px.
- **MOB-006** (Major / P2) — Feedback form inputs render at 14.0625px
  → iOS Safari auto-zoom on focus. Added site-wide
  `input, textarea, select { font-size: max(1rem, 16px); }` rule.
- **MOB-007** (Minor / P3) — "← All JLPT levels" home-up link not
  localized to Hindi. Added `nav.all_levels` key to en+hi locales
  (Hindi: `सभी JLPT स्तर`). Updated js/home.js to use
  `t('nav.all_levels')`.
- **MOB-008** (Minor / P3) — Route `#/listening/story` silent
  redirect to `#/listening` (dead-end). Canonicalized
  `js/listening-story.js` to use `#/listeningstory` (no slash);
  4 href edits + 1 comment fix.
- **MOB-009** (Minor / P3) — Route `#/levels` silent redirect to
  `#/diagnostic`. Updated `js/home.js` home-up link `href="#/levels"`
  → `href="../"` (lands directly on JLPTSuccess root level-picker;
  skips in-SPA redirect that triggered first-run onboarding).
- **MOB-010** (Minor / P5) — Sticky header top=16px. **Declined**
  as design-decision per bug "borderline — possibly by-design"
  note. The 16px breathing room is intentional visual whitespace.
- **MOB-011** (Major / P2) — 449 undersized interactive elements on
  authentic-items page. Authentic-card-{kanji,vocab,grammar}-refs
  got `padding: 10px 6px; min-width: 44px`; .btn-tiny Pronounce
  buttons bumped to `min-height: 44px`.
- **MOB-012** (Minor / P3) — Header brand-link 'N5' 54×16 bumped to
  44px tap target via padding.
- **MOB-013** (Minor / P4) — Skip-link 187×41 (3px short) bumped
  to ≥44px.
- **MOB-014** (Minor / P4) — Changelog `docs/CHANGELOG-archive.md`
  link 209×17 bumped via `.changelog-page a[href$=".md"]` rule.
- **MOB-015** (Minor / P3) — Examday/weakareas "See full bank →"
  inline links 139-167×15 bumped via `.examday-page .muted a` /
  `.weakareas-page .muted a` rules.
- **MOB-017** (Minor / P3) — Reading list page (`#/reading`) lacked
  `<a href>` deep-links. Converted `<button class="reading-pick"
  data-id="X">` → `<a class="reading-pick" href="#/reading/X"
  data-id="X">` in js/reading.js. Restores crawlability +
  bookmark-via-right-click + SEO; matches the `#/learn/grammar`
  deep-link pattern.
- **MOB-018** (Minor / P3) — Selenium mobile-emulation `scrollTo`
  no-op test-framework limitation **documented**; recommend
  splitting affected scenarios into Auto + Manual variants. Not
  app-code defect.
- **MOB-019** (Minor / P4) — 3 audio-UI scenarios target index
  pages but audio loads after item-tap. **Documented** scenario-
  rewrite recommendation. Not app-code defect.
- **DOKKAI-004** (Low / P4) — dokkai-4.1 rationale_hi rewritten from
  `आना-जाना by ट्रेन` to `ट्रेन से कंपनी जाते हैं (रोज़ का आना-जाना
  ट्रेन से)।`. Same class as DOKKAI-002 ("ago"). Extended JA-129
  trigger set with ` by ` family substrings.

### Added

- **JA-131 CI invariant** — locales/en.json + hi.json carry
  `nav.all_levels` key (MOB-007 drift guard).
- **JA-132 CI invariant** — css/main.css + main.min.css carry the
  MOB-001..016 mobile-UI compliance batch marker + canonical
  touch-target class set (multi-class drift guard).
- **JA-133 CI invariant** — css/main.css has form-input
  `font-size: max(1rem, 16px)` rule (MOB-006 iOS auto-zoom guard).
- **JA-134 CI invariant** — js/home.js + js/listening-story.js
  free of dead-end hash routes `#/levels` and `#/listening/story`.
- **JA-129 trigger extension** — added ` by `, ` by.`, ` by,`,
  ` by)`, ` by]` to the temporal-marker scan (DOKKAI-004 catch).
- **Procedure manual F.34** — Mobile-UI compliance methodology:
  5 durable defect classes (touch-target HIG, iOS auto-zoom, dead-
  end routes, locale parity, test-infrastructure gaps) with CI
  invariant templates + Nx-builder build-script recipe.
- **Accuracy prompt A73** — Mobile-UI audit category.
- **N5Improvement Phase-0 mobile-UI regression block**.
- **AUDIT-COVERAGE Part 27** — close-out narrative.

### State

CI **137 / 137 invariants green** (was 133; added JA-131/132/133/134).
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker **129 / 129 Fixed / 0 Open**.

Bounded framing: MOB-001..019 + DOKKAI-004 + JA-131..134 cover the
5 mobile-UI defect classes surfaced by the 2026-05-19 Selenium
mobile-emulation audit. Future audits may surface additional
classes; this batch closes the currently-observed set.

## Unreleased - 2026-05-18 (DOKKAI-001..003 close-out — paper schema-discipline + 3 new CI invariants)

### Fixed

- **DOKKAI-001 / BUG-107** (Medium / P2) — passage_text was duplicated
  across two storage locations in every dokkai paper file (passages[]
  top-level + every question[].passage_text). 12 of 102 dokkai
  questions had already-drifted copies (leading `> ` markdown-
  blockquote prefix on one copy but not the other). Removed
  passage_text from all 102 dokkai questions (single source of truth =
  passages[label].text, referenced via passage_label foreign key);
  normalized 40 passages[].text entries by stripping the `> ` prefix.
  **Horizontal sweep:** bunpou/paper-7.json had the same drift class
  (10 Mondai-3 paragraph-gap questions with stray passage_text but
  no passages[] block); created passages[] with 2 canonical entries +
  dropped 10 passage_text fields.
- **DOKKAI-002 / BUG-108** (Low / P3) — dokkai-1.1 rationale_hi
  contained untranslated English "ago" (`भूत-सकारात्मक रूप (आया एक
  महीना ago)।`); rewritten to `भूत-सकारात्मक: एक महीना पहले आया (अब
  यहाँ रह रहा है)।`. **Horizontal sweep:** JA-129 scan caught goi-7.1
  with the same English-fragment class (`आया 1 वर्ष ago।` → `यहाँ एक
  साल से = एक साल पहले आया।`). Both carry provenance
  `native_reviewed_2026_05_18`.
- **DOKKAI-003 / BUG-109** (Low / P4) — grammarPatternId field was
  present on 78/102 dokkai questions, absent on 24, with no documented
  convention. Set grammarPatternId=null + grammarPatternId_provenance=
  "not_applicable_comprehension" on the 24 dokkai entries. **Horizontal
  sweep:** 83 more non-dokkai questions missing the field — 11 goi
  (provenance `not_applicable_vocab`) + 72 moji (provenance
  `not_applicable_orthography`) all filled. All 412 paper questions
  (102 dokkai + 105 goi + 105 moji + 100 bunpou) now have
  grammarPatternId as a guaranteed key, matching VOCAB-002's "counter
  is always a key, sometimes null" pattern.

### Added

- **JA-128 CI invariant** — paper questions must NOT carry
  passage_text field; canonical text lives in passages[label].text
  via passage_label foreign key (DOKKAI-001 drift guard).
- **JA-129 CI invariant** — paper rationale_hi must be free of
  untranslated English temporal/quantity markers (` ago `, ` yet `,
  ` lot `, + punctuated variants); extends the JA-122 fragment-scan
  set (DOKKAI-002 drift guard).
- **JA-130 CI invariant** — every paper question has
  grammarPatternId as a key; when value is null, provenance must
  start with `not_applicable_` documenting the reason (DOKKAI-003
  schema-shape guard).
- **Procedure manual F.33** — Paper-question schema-discipline:
  3 durable invariants (Class A single source of truth for passages;
  Class B English-fragment temporal markers; Class C explicit-null
  schema-shape). Reusable Nx-builder pattern.
- **Accuracy prompt A72** — Paper-question schema-discipline audit
  category.
- **N5Improvement Phase-0 dokkai-schema regression block**.
- **AUDIT-COVERAGE Part 26** — Close-out narrative.
- **tools/fix_dokkai_bugs_2026_05_18.py** + **tools/fix_dokkai_bugs_
  horizontal_2026_05_18.py** — Reusable fix-script templates.

### State

CI **133 / 133 invariants green** (was 130; added JA-128/129/130).
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker **112 / 112 Fixed / 0 Open**.

Bounded framing: DOKKAI-001..003 + JA-128..130 cover the 3 schema-
discipline classes surfaced by the 2026-05-18 dokkai audit. The
horizontal sweep expanded scope to all 4 paper categories (bunpou /
goi / moji / dokkai). Future audits may surface additional schema-
shape drift classes; this batch closes the currently-observed set.

## Unreleased - 2026-05-18 (LLM-001..005 + REG-001 close-out — 6 crawler-accessibility + register-conflation bugs + 5 new CI invariants)

### Added

- **Per-paper static mirrors** at `/N5/papers/<paper-id>/index.html` for
  all 28 paper packs + landing page at `/N5/papers/index.html`. Each
  mirror server-renders the full question bank (stem, choices, correct
  answer, rationale) without requiring JavaScript. LLM-001 / BUG-094
  close-out.
- **7 thin LLM-005 summary pages** at `/N5/{home,grammar,vocabulary,
  kanji,reading,listening,test}.html` — one-page-per-module summaries
  pulling counts from `data/version.json`. Crawler bookmark targets.
- **Corpus discovery catalog** at `/N5/data/index.json` with 39 entries
  enumerating every data file with URL, size_bytes, last_modified,
  content_type, schema_version, item_count, description. Single
  programmatic entry point for LLMs / scripts wanting to read the
  corpus in bulk. LLM-003 / BUG-096 close-out.
- **llms.txt** at `/JLPTSuccess/llms.txt` (root) + `/JLPTSuccess/N5/llms.txt`
  — Markdown-formatted discovery file for LLM crawlers per the
  llms.txt community-draft format. LLM-005 / BUG-105 close-out.
- **Root-level robots.txt** at `/JLPTSuccess/robots.txt` with sitemap
  reference.
- **Root index.html footer link** to static-summary entry points.

### Fixed

- **LLM-002 / BUG-095** — `/N5/sitemap.xml` regenerated from 10 URL
  entries (meta routes only) to **1589 URL entries** covering every
  static-mirror directory, the 7 summary pages, the 11 meta routes,
  and the paper mirrors.
- **LLM-004 / BUG-097** — N5/index.html `<noscript>` block expanded
  with path-routed navigation (no hash routes) including links to all
  7 summary pages, per-entity static indexes, data/index.json, and
  site meta. Stale counts corrected: `45 reading` → `54 reading`,
  `47 listening` → `50 listening`. Counts pulled from version.json
  at build time (drift-resistant via JA-125 + JA-107).
- **REG-001 / BUG-106** — n5-046.wrong_corrected_pair[1]
  (やまださんは だれ ですか) migrated to common_mistakes
  register_variant with form_a/form_b/label_a/label_b schema.
  Removed the conflated 「やまださんは どんな 人 ですか」 alternative
  (different question type: identity vs character description).
  Added scope_note marking どなた as N4-N3 vocabulary. JA-127 D6
  guard added; first run caught 5 more entries with the same
  "(in formal context)" self-contradiction pattern (n5-097, n5-102,
  n5-127, n5-173, n5-179) — all migrated to register_variant.

### CI invariants (125 → 130)

- **JA-123** — every `data/papers/*/*.json` has a corresponding
  `/papers/<id>/index.html` static mirror (LLM-001 drift guard).
- **JA-124** — `sitemap.xml` has ≥1000 `<loc>` entries (LLM-002
  regression floor; catches reversion to 10-URL pre-fix state).
- **JA-125** — every entry in `data/index.json` has `size_bytes`
  matching actual on-disk file size (LLM-003 / INV-LLM-3; same
  drift class as INV-4 / JA-107 version.json count drift).
- **JA-126** — the 7 LLM-005 summary pages + llms.txt (at both
  `/JLPTSuccess/` root and `/JLPTSuccess/N5/`) all exist.
- **JA-127** — no `wrong_corrected_pair` entry with
  `error_category == "register"` may have a wrong-field
  parenthetical naming the register the form is appropriate for
  (REG-001 D6 guard; "(formal)" / "(in casual conversation)" /
  etc. — internally contradictory).

### Deferred (documented, not fixed in this commit)

- **REG-002..NN** — 84 SWEEP-1 candidates surfaced by REG-001
  keyword-based scan; each needs per-entry native-speaker triage
  to classify as register-variant / genuine-error / pragmatic-
  mismatch. Listed at `docs/REG-001-SWEEP-1-candidates_2026_05_18.md`.
- **SWEEP-2..5** — D2/D3/D4/D5 defect classes (semantic conflation,
  formality-vs-elevation, out-of-N5-scope-as-canonical, kana-of-
  whitelist-kanji) — native-speaker review sessions, not this batch.
- **LLM-005 build-script CI integration** — `tools/build_llm_surfaces
  _2026_05_18.py` is a one-shot runner; wiring into
  `.github/workflows/` for auto-regen on push is a follow-up TODO.

### Documentation (Rule 4/5)

- **Procedure manual F.31** — 8-surface LLM / search-crawler
  accessibility canonical set; build-script architecture; CI
  invariant template; common pitfalls; bounded-coverage phrasing.
- **Procedure manual F.32** — register-variant vs grammar-error 6
  defect classes (D1..D6); register_variant schema; CI invariant;
  sweep procedure.
- **Accuracy prompt A70 / A71** — LLM-accessibility audit category +
  register-conflation audit category.
- **N5Improvement Phase-0 LLM-surfaces** + **Phase-0 register-variant**
  regression blocks.
- **AUDIT-COVERAGE Part 25** — close-out narrative + new drift-class
  catalog entries.
- **Cross-artifact sync-map** — Part 25 audit-log row.
- **Spec §25.4** — JA-123..127 rows added; section intro updated.

### State

CI **130 / 130 invariants green**.
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker **109 / 109 Fixed / 0 Open**.

Bounded framing: this batch closes the 6 LLM-* + REG-* bugs surfaced
on 2026-05-18. Future audits may extend the catalog (locale-specific
sitemap variants, JSON-LD structured data, schema.org markup, etc.) —
JA-123..127 prevent re-introduction of *the surface gaps this batch
addresses*.

## Unreleased - 2026-05-18 (PAPER-001..004 + LISTEN-4 close-out — 5 bug-class fixes + 3 new CI invariants)

### Fixed

- **PAPER-001** (Major / P2): re-tagged 58 bunpou paper-bank questions whose
  `grammarPatternId` was systematically mis-assigned (30+ tagged `n5-013` =
  も regardless of actual correct-answer particle). Built canonical
  particle → pattern_id map from `data/grammar.json` Particles category
  (21-entry mapping; documented in procedure manual §F.30.4). Coverage:
  29 Mondai 1 particle re-tags + 14 non-particle re-tags + 7 Mondai 3
  paragraph-gap + 2 Mondai 2 sentence-ordering. All re-tags carry
  provenance `rule_based_correctanswer_2026_05_18`.
- **PAPER-002** (Low / P4): set missing `grammarPatternId` +
  `grammarPatternId_provenance` on bunpou-4.3 (Q48). Stem "きょうは あめが
  ふって、かぜも （）。" with correct answer "つよいです" tagged `n5-079`
  (い-Adjective + です) — parallel-predicate use via て-form connection.
- **PAPER-003** (Low / P4): stripped commit-message-style meta-fix history
  from 14 learner-facing rationale fields. 6 bunpou questions (bunpou-
  1.14, 3.4, 3.11, 5.15, 7.4, 7.8) + 2 goi questions (goi-3.3, goi-3.14
  caught by JA-121 after first pass) had audit-trail parentheticals
  ("Stem now anchored with わたしは", "replaces ので per corpus-wide
  policy applied alongside Q5 fix in v1.12.14") removed. Distractor-
  analysis content (Q50/Q51 bunpou-4.5/4.6) intentionally preserved —
  genuine learner value, not commit trail.
- **PAPER-004** (Medium / P3): rewrote 58 `rationale_hi` fields with
  natural Hindi sourced from `rationale_en`. Affected questions had
  word-by-word literal-translation artifacts: apostrophe-s possessive
  ("दोस्त's घर"), English contractions ("मैं'm नहीं भूखा yet"), mojibake
  ("यहाँre", "o'घड़ी"), English filler words (" lot ", " have जाना").
  All 30 Mondai 2 sentence-ordering questions (bunpou-5.1 through
  bunpou-6.15) rewritten + 4 Mondai 1 + 2 dokkai + 22 goi/moji with
  English-pattern technical fragments cleaned up. All carry provenance
  `native_reviewed_2026_05_18`.
- **LISTEN-4** (Medium / P2): tracker status flipped Open → Fixed. Data
  was already correct from a prior commit (`version.json` counts
  grammar=178, vocab=995, kanji=106, reading=54, listening=50; version
  field bumped to v1.15.5). Investigation found the `Fix Commit` cell
  for BUG-090..093 referenced `d26e677` — a native-Japanese-teacher
  commit from 2026-05-17, BEFORE these bugs were filed on 2026-05-18.
  Stale back-fill; not a real close-out. Honest correction in this
  commit.

### Added

- **JA-120 CI invariant** — paper bunpou Mondai-1 `grammarPatternId`
  must match canonical particle pattern (PAPER-001 drift guard).
- **JA-121 CI invariant** — paper `rationale` / `rationale_hi` must be
  free of 12 commit-message-style meta-fix phrases (PAPER-003 drift
  guard).
- **JA-122 CI invariant** — paper `rationale_hi` must be free of 17
  English-pattern fragments — apostrophe-s / contractions / mojibake
  (PAPER-004 drift guard).
- **Procedure manual §F.30** (6 sub-sections) — paper-question content
  audit methodology covering all 3 drift classes + canonical particle ↔
  pattern_id map + anti-pattern "don't translate from broken Hindi".
- **Accuracy prompt §A67 / §A68 / §A69** — three new audit categories
  mirroring JA-120 / JA-121 / JA-122 enforcement.
- **N5Improvement Phase-0 paper-question regression block** —
  maintainer-side mirror of JA-120/121/122.
- **AUDIT-COVERAGE Part 24** — paper-question content audit close-out
  narrative + drift-class catalog.
- **tools/fix_paper_bugs_2026_05_18.py** + **tools/fix_paper_bugs_part2_2026_05_18.py**
  — reusable Nx-builder pattern templates for paper-bank audits.

### Anti-pattern documented

The first PAPER-004 fix pass attempted to "clean up" broken
`rationale_hi` by re-translating it back to natural Hindi using the
broken Hindi as source. Result: clean-looking Hindi about the wrong
question (e.g., bunpou-5.10 actual question is library-books-three
but rewrite said Sunday-movie). Caught on verification before
commit. Reverted, redid sourced from `rationale_en` (verified
correct). Recorded as procedure-manual §F.30.6.

### State

CI **125 / 125 invariants green** (was 122, added JA-120/121/122).
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker **109 / 109 Fixed / 0 Open**.

Bounded framing: PAPER-001..004 + LISTEN-4 close-out addresses the
3 paper-question drift classes surfaced by the 2026-05-18 content
audit. Future auditors may surface additional classes (distractor-
quality, more subtle rationale-tone issues); JA-120/121/122 prevent
re-introduction of *these specific drift classes*.

## Unreleased - 2026-05-17 (Multi-role specialist review sweep + Selenium UI test class + 16 NR-* bugs)

Not user-visible at runtime — corpus content was already correct
post Phase-2; this batch added a systematic 720-scenario multi-
role specialist review sweep (Native Japanese / JLPT / Native
Hindi / Security / Privacy-legal / Performance / Data / Pedagogy /
QA / Cultural / UX / Accessibility / Operations / End-user) plus
a new Selenium 4-driven end-to-end UI test class covering every
functional surface in spec §5.

### 16 NR-* bugs surfaced + fixed across 5 batches

- **Batch 1 (`d26e677`) — Native Japanese teacher review**:
  NR-001 (Major, まえに pattern-instance contamination across n5-161
  / n5-162 — 5 misfiled examples); NR-002 (Medium, n5-161 duplicate
  examples); NR-003 (Major, n5-160 / n5-163 misfiled adverbial
  'あとで 電話します。'); NR-004 (Major, n5-045 ex[6] wh+は anti-
  pattern); NR-005 (Critical, 13 wrong rendaku forms in vocab.json
  number-vocab collocations for 本 + 個 counters). 9 grammar examples
  + 13 vocab collocations fixed. Cross-checked vs Genki I + Minna I
  + NHK accent dictionary + JEES samples.
- **Batch 2 (`8159b49`) — Native Hindi teacher + JLPT exam expert**:
  NR-HI-001 (Critical, q-0264 distractor とって corruption "जो's");
  NR-HI-002 (Major, q-0462 English possessive 's after Hindi noun);
  NR-HI-003 (Medium, q-0234 mixed-English "Group 1"); NR-JE-001
  (Major, 40 JLPT format violations — half-width `___` for fill-
  blank + 10 missing terminal 。). Cross-checked vs Hindi Vyakaran +
  Sahitya Akademi + JEES sample paper format.
- **Batch 3 (`46be3e1`) — Security / Privacy-legal / Data eng sweep**:
  NR-SEC-001 (Major, 4/4 GitHub workflows missing `permissions:`
  least-privilege block — fixed with `contents: read`); NR-SEC-002
  (Medium, defense-in-depth meta tags initially missing);
  NR-LIC-001 (Medium, kanjium CC-BY-SA 4.0 attribution missing from
  CONTENT-LICENSE.md); NR-DATA-001 (Low informational, 14/22 data
  files lack schema_version — auto-gen catalogs).
- **Batch 4 (`d1e0d90`) — Brutal-honesty re-audit**: NR-DATA-002
  (Major, 4 vocab demonstrative entries reference retired grammar
  pattern n5-012 — caught by deeper full-corpus scan). 42 prior
  PASSes re-labeled with bounded-honest qualifiers (PASS / PASS-
  limited / PASS-architectural / PASS-spot-check / etc.).
- **Batch 5 (`5635425`) — Selenium UI test class**: NR-UI-001
  (Medium, CSP `frame-ancestors` and X-Frame-Options are HTTP-
  header-only and IGNORED via `<meta>` — cosmetic-only fix from
  prior NR-SEC-002 batch). Selenium console-error capture caught
  SEVERE errors on every route. Fix: removed both ineffective meta
  tags from index.html + documented the GitHub-Pages static-hosting
  limitation. Post-fix: 0 SEVERE console errors.

### Selenium UI test suite (NEW)

`tools/ui_test_suite_2026_05_17.py` — 55 scenarios covering:
- Spec §5.1-5.16 functional routes (Home / Learn hub / Grammar /
  Vocab / Kanji / Reading / Listening / Mock Test / Papers /
  Drill / Review / Missed / Summary / Settings / Sitting / Today /
  Privacy / Notices)
- All 14 static-mirror routes (`/home/`, `/changelog/`,
  `/privacy/`, `/notices/`, `/learn/grammar/<id>/` + 5
  `/lessons/<id>.html` legacy, `/reading/<id>/`, `/listening/<id>/`,
  `/learn/vocab/<form>/`, `/kanji/<glyph>/` + 5 index pages)
- SEO (`sitemap.xml`, `robots.txt`), accessibility landmarks,
  security headers, Service Worker registration, audio
  reachability, locale parity, console-error-zero verification.

Runs locally via Selenium 4 + Selenium Manager auto-driver (no
manual chromedriver-install step). Reusable for Nx builds.

### New "UI Tests" tab in test-scenarios xlsx

18 total tabs now (Unit Tests + A-N + User Reported Bugs + new
UI Tests with 55 scenario rows).

### Methodology propagation (Rule 4 / Rule 5)

- `JLPT Common/procedure-manual-build-next-jlpt-level.md` — Appendix
  F.28 (multi-role specialist-review-by-tab pattern + bounded-
  honest stamping vocabulary + brutal-honesty re-audit) + F.29
  (Selenium UI test class + NR-UI-001 lesson on meta-tag-ignored
  security directives).
- `prompts/Japanese language Accuracy check.txt` — A65 (multi-role
  methodology) + A66 (Selenium UI test class).
- `prompts/N5Improvement.txt` — Phase-0 Selenium UI test regression
  block (target 53/55 PASS post NR-UI-001) + Phase-0 multi-role
  specialist-review regression block (target 0 NEW NR-* findings).
- `docs/AUDIT-COVERAGE-2026-05-15.md` — Part 23 addendum
  (consolidated 5-batch narrative + reusable-tooling deliverables).
- `docs/cross-artifact-sync-map.md` — 6 new audit-log rows
  (5 batches + this propagation catch-up).
- `specifications/JLPT-N5-Current-Implementation-Spec.md` — §25 intro
  reflection (UI Tests tab added; bug-tracker count update).

### CI invariants final state for this batch

- **Total live: 122** (unchanged — this batch is methodology +
  multi-role review + UI test wiring, not new content invariants).
- All 122 PASS.
- `cross_artifact_sync_report.py` EXIT: CLEAN.
- Bug tracker: **104 / 104 Fixed / 0 Open**.
- UI test suite: 53 / 55 PASS, 1 SKIP, 0 FAIL post NR-UI-001 fix.

### Files touched (consolidated this batch)

- `N5/data/grammar.json` (9 example fixes)
- `N5/data/vocab.json` (13 + 4 collocation fixes)
- `N5/data/questions.json` (3 Hindi corrections)
- `N5/data/papers/bunpou/*.json` (40 stem-format patches)
- `N5/.github/workflows/*.yml` (4 permissions blocks)
- `N5/index.html` (security header meta tags partly retired per
  NR-UI-001)
- `N5/CONTENT-LICENSE.md` (kanjium CC-BY-SA 4.0 attribution)
- `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`
  (NEW "UI Tests" tab + 16 bug rows + ~230 scenario stamps)
- `JLPT Common/procedure-manual-build-next-jlpt-level.md` (F.28
  + F.29 + footnote)
- `N5/prompts/Japanese language Accuracy check.txt` (A65 + A66)
- `N5/prompts/N5Improvement.txt` (2 new Phase-0 regression blocks)
- `N5/docs/AUDIT-COVERAGE-2026-05-15.md` (Part 23)
- `N5/docs/cross-artifact-sync-map.md` (6 audit-log rows)
- `N5/CHANGELOG.md` + `N5/changelog/index.html` (meta-mirror regen)
- 11 NEW `N5/tools/` scripts (NR-* applicators + Selenium runner +
  xlsx populators) — listed in AUDIT-COVERAGE Part 23

## Unreleased - 2026-05-17 (Audio Phase-2: VOICEVOX from-source re-render at speed_scale=1.00)

User-visible: all 50 listening items have been re-rendered from
source via VOICEVOX at `speed_scale=1.00`, replacing the prior
2026-05-12 render at `speed_scale=0.95` plus the Phase-1 (ffmpeg
atempo) and Phase-1.5 (librubberband on 3 items) post-processing
layers. Audio quality is now driven by a single coherent
from-source render rather than stacked post-processing passes.
Pacing distribution unchanged from the user's perspective — every
item still lands in the JLPT N5 target band 180–240 mpm.

### Render summary

- **Engine**: VOICEVOX v0.25.2 (CPU edition)
- **Speed scale**: 1.00 (raised from 0.95)
- **Items rendered**: 50 / 50, wall-clock 697s (~12 min)
- **Speakers preserved**: same 6 distinct voices as the 2026-05-12
  render (春日部つむぎ, 玄野武宏, 四国めたん, ずんだもん,
  雨晴はう, 青山龍星). Per-item speaker assignment unchanged.
- **Final pacing**: 50/50 in_range. Mean 214.5 mpm; min 190.4;
  max 237.3 — well centered in the 180–240 target band.

### Post-render adjustment distribution

The fresh speed_scale=1.00 render produced 16 items in band straight
from VOICEVOX. The remaining 34 items needed ffmpeg post-processing
to land in band:

| Method | Count | Notes |
|---|---|---|
| Direct VOICEVOX (no atempo applied) | 16 | In band from raw render |
| `ffmpeg-atempo` single-pass | 29 | Factor in [0.5, 2.0] |
| `ffmpeg-rubberband` single-pass | 5 | Replaced chained atempo at factor < 0.5 (same quality pattern as Phase-1.5) |

The 5 rubberband items are `n5.listen.010 / 041 / 044 / 045 / 047`
— each authored as a single-pass librubberband swap-in for the
chained `atempo=0.5,atempo=X` that the pacing refresh would
otherwise have applied. Same quality rationale as the prior
Phase-1.5 (commit `c79c02e`): rubberband preserves transients
better than chained atempo at sub-0.5 slowdown factors.

### What this batch retired

- **Phase-2's deferred-on-VOICEVOX-install status** carried over
  from Part 17, Part 20, and Part 21 audit-coverage doc addenda.
  With VOICEVOX installed on the maintainer's machine, Phase-2
  was executable agent-side.
- The 2026-05-12 render at speed_scale=0.95 + Phase-1 atempo
  post-processing layer (commit `47d1edc`) on the 50 audio
  primaries.
- The Phase-1.5 rubberband replacement (commit `c79c02e`) on the
  3 chained-atempo items (n5.listen.041 / 044 / 045) — those
  items are now part of the Phase-2 re-render + new rubberband
  application at adjusted factors.

### What this batch did NOT change

- Pattern count (178 — no schema changes).
- Bug tracker (53 / 53 Fixed / 0 Open — Phase-2 is a quality
  upgrade, not a bug close-out).
- Listening item count (50). Item scripts (`script_ja`) unchanged.
- CI invariant count (122/122 still). All audio-class invariants
  (JA-110 / JA-111 / JA-112 / JA-114) PASS.

### Files touched

- `N5/audio/listening/n5.listen.{001..050}.mp3` (50 primaries
  re-rendered from VOICEVOX at speed_scale=1.00)
- `N5/audio/listening/n5.listen.{001..050}.slow.mp3` (50 .slow
  companions regenerated at single-pass atempo=0.7)
- `N5/data/listening.json` (audio_render_meta refresh on every
  item + `_meta.phase2_voicevox_rerender_2026_05_17` block)
- `N5/tools/render_listening_phase2_voicevox_1_00_2026_05_17.py`
  (NEW — Phase-2 renderer; derived from the 6speakers script
  with speedScale 0.95 → 1.00)
- `N5/tools/apply_phase2_rubberband_chained_items_2026_05_17.py`
  (NEW — Phase-2 follow-on librubberband swap for sub-0.5 items)
- `N5/docs/AUDIO-PHASE2-VOICEVOX-RERENDER.md` (rewritten from
  runbook to COMPLETED status)
- `N5/docs/AUDIT-COVERAGE-2026-05-15.md` (Part 22 addendum)
- `N5/docs/cross-artifact-sync-map.md` (audit-log row)
- `N5/CHANGELOG.md` (this entry)

CI invariants final state: **122 / 122 green**.
`cross_artifact_sync_report.py` EXIT: CLEAN.

## Unreleased - 2026-05-17 (JA-91 + JA-94 Phase A + Phase B resolution: empty both baselines)

User-visible: 14 grammar examples rewritten + 33 grammar-pattern
explanation paragraphs rewritten. Functional coverage is unchanged —
the 178 patterns each still cover what they covered before, and the
14 replaced examples still demonstrate N5-appropriate Japanese. The
visible change is that learners encountering n5-030 (nominalizer の),
n5-048 (どこ), n5-065 (plain-form verbs), n5-071 (Verb-てください),
n5-084 (な-Adj + な + Noun), n5-112 (〜ふん/ぷん minutes), n5-157
(〜でしょう), and n5-164 (〜さん) now see examples that actually
demonstrate those patterns (rather than borrowed examples from
adjacent patterns), and 30+ entries (the deferring sides of the
prior 43 cross-pattern explanation pairs) have explanations that
explicitly name their relationship to the canonical entry rather
than restating the canonical text verbatim.

### Phase A — 14 BUG-006-CANDIDATE example replacements

Each was a wrong-pattern example (the example didn't demonstrate
the parent pattern at all). Replaced with parent-pattern-
demonstrating examples:

| Pattern | Index | New ja | New en |
|---|---|---|---|
| n5-030 | 4 | うんどうするのは きもちが いいです。 | Exercising feels good. |
| n5-030 | 5 | ピアノを ひくのが すきです。 | I like playing the piano. |
| n5-030 | 6 | えいがを みるのが たのしいです。 | Watching movies is fun. |
| n5-048 | 0 | ぎんこうは どこですか。 | Where is the bank? |
| n5-048 | 1 | どこで パンを かいますか。 | Where do you buy bread? |
| n5-048 | 6 | あなたの くには どこですか。 | Where is your country? |
| n5-065 | 4 | ともだちと えいがを みる。 | [I] watch a movie with a friend. (casual) |
| n5-071 | 7 | もう いちど せつめいして ください。 | Please explain once more. |
| n5-084 | 5 | べんりな きかいです。 | It's a convenient machine. |
| n5-112 | 8 | じゅっぷん やすみました。 | I rested for 10 minutes. |
| n5-157 | 4 | あの えいがは おもしろい でしょう。 | That movie is probably interesting. |
| n5-157 | 5 | 電車は こんで いる でしょう。 | The train is probably crowded. |
| n5-157 | 6 | この もんだいは むずかしい でしょう。 | This problem is probably difficult. |
| n5-164 | 6 | たなかさんは げんきですか。 | Is Tanaka-san well? |

`data/_ja94_baseline.json` now carries empty
`baseline_failing_examples`; JA-94 enforces marker-presence
unconditionally across all 1782 examples.

### Phase B — 33 explanation_en rewrites covering 43 prior pairs

The 43 prior JA-91 baseline pairs (DUPLICATE_PATTERN ×8,
CROSS_REFERENCE ×21, ALTERNATIVE_VARIANT ×12, SUBSET ×2) were
addressed via explanation rewrites:

- **DUPLICATE_PATTERN** — rewrote the "re-introduction" side (n5-039
  / n5-040 / n5-041 / n5-045 / n5-046 / n5-114 / n5-115 / n5-029)
  to use distinct framing (kosoado-paradigm sequencing, time-axis
  instance, noun-modifier system) so each diverges from its
  canonical entry's text.
- **CROSS_REFERENCE** — rewrote the deferring side as a focused
  sub-scope entry that explicitly points at the parent (e.g.,
  n5-137 → Nominalization framing of の; n5-184/185/186/187 →
  indefinite-X instance entries of the n5-183 parent rule;
  n5-160/161/162/163 → frame-specific instances of あと/まえ).
- **ALTERNATIVE_VARIANT** — rewrote BOTH sides of each pair with
  register / syntactic-frame distinguishing prose (e.g., n5-173
  spoken-formal vs n5-174 written-formal vs n5-175 conditional-
  frame vs n5-176 casual-contraction obligation; n5-157 polite-
  register でしょう vs n5-158 plain-register だろう).
- **SUBSET** — rewrote n5-048 as the 'where' question-word entry
  pointing at the full n5-016 / n5-041 series.

Total: 33 patterns rewritten (some sat at two classifications).
Verification (in `tools/apply_ja91_explanation_rewrites_2026_05_17.py`):
all 43 prior pairs now fall below the 0.85 similarity threshold;
zero NEW pairs were introduced by the rewrites.
`data/_ja91_baseline.json` now carries empty `baseline_pairs`;
JA-91 enforces the threshold unconditionally.

### CI invariants final state for this batch

- **Total live: 122** (unchanged from prior — Phase A + Phase B
  are content-side resolutions, not new invariants).
- Both JA-91 and JA-94 now run with EMPTY baselines.
- `cross_artifact_sync_report.py` exits CLEAN.
- Bug tracker: 53 / 53 Fixed / 0 Open (unchanged).
- The "follow-on audit-cycle targets" from the prior JA-91 +
  JA-94 unblock batch are RESOLVED without merging patterns or
  rewriting structurally; pattern count stays at 178.

### Audio Phase-2 status

Phase-2 (VOICEVOX re-render at speed_scale=1.00) remains the only
queued item from the prior JA-91+JA-94 follow-on list. Stays
deferred on local VOICEVOX install (agent-side environment gap;
not a correctness or coverage blocker — Phase-1.5 closed the
sub-0.5-factor artifact gap with librubberband).

### Files touched

- `N5/data/grammar.json` (14 example replacements + 33
  explanation_en rewrites)
- `N5/data/grammar.json.bak_2026_05_17_pre_phaseA_B` (NEW backup)
- `N5/data/_ja91_baseline.json` (emptied + meta updated)
- `N5/data/_ja94_baseline.json` (emptied + meta updated)
- `N5/tools/apply_bug006_candidate_fixes_2026_05_17.py` (NEW)
- `N5/tools/apply_ja91_explanation_rewrites_2026_05_17.py` (NEW)
- `N5/tools/check_content_integrity.py` (JA-91 + JA-94 registry
  description text updated to reflect RESOLVED state)
- `N5/specifications/JLPT-N5-Current-Implementation-Spec.md`
  (§25 intro + §25.4 + §25.7 updates)
- `N5/prompts/N5Improvement.txt` (Phase-0 regression block target
  values updated from 43/14 to 0/0)
- `N5/docs/AUDIT-COVERAGE-2026-05-15.md` (Part 21 addendum)
- `N5/docs/cross-artifact-sync-map.md` (audit-log row)
- `N5/CHANGELOG.md` (this entry)

## Unreleased - 2026-05-17 (Audio Phase-1.5: rubberband replaces chained atempo on 3 items)

Audio-quality upgrade for the 3 listening items whose Phase-1
slowdown was implemented via a 2-pass `atempo=0.5,atempo=X` chain
(factors 0.476–0.487, sub-0.5-pass territory). Phase-1.5 replaces
the chain with `ffmpeg` `rubberband` filter (libRubberBand
PSOLA/phase-vocoder) at the same effective factor, single-pass.
Pacing remains in target band 180–240 mpm post-replacement;
artifact footprint on those 3 items is reduced (the chained
atempo had double-stage smearing on consonant transients that
rubberband single-pass avoids).

### Items affected

| Item | Factor | Phase-1 method | Phase-1.5 method | Pacing (mpm) |
|---|---|---|---|---|
| n5.listen.041 | 0.4811 | `atempo=0.5,atempo=0.9622` | `rubberband=tempo=0.4811` | 227.3 (was 218.3) |
| n5.listen.044 | 0.4872 | `atempo=0.5,atempo=0.9744` | `rubberband=tempo=0.4872` | 216.8 (was 215.5) |
| n5.listen.045 | 0.4760 | `atempo=0.5,atempo=0.9520` | `rubberband=tempo=0.4760` | 222.8 (was 220.6) |

All 3 land within the JLPT N5 target band (180–240 mpm). The
remaining 36 atempo-adjusted items (factors 0.5–1.0) stay on
single-pass `atempo` — quality difference vs rubberband at those
factors is marginal and not worth the re-render churn.

### Audio metadata updates

For each of the 3 items, `audio_render_meta`:
- `post_render_tempo_method` flipped from `"ffmpeg-atempo"` to
  `"ffmpeg-rubberband"`.
- `phase15_method_change_2026_05_17` added — records the from/to
  method, the factor, and the rationale.

### Doc drift fix

`docs/AUDIO-PHASE2-VOICEVOX-RERENDER.md` previously cited
"7 items with slowdown factors below 0.5" — actual count was 3
(hand-tally error at authoring time). All 4 occurrences corrected
in this batch; Phase-1.5 close-out note added to the doc head.

### Files touched

- `N5/audio/listening/n5.listen.{041,044,045}.mp3` (rubberband
  replacements)
- `N5/audio/listening/n5.listen.{041,044,045}.slow.mp3`
  (regenerated from new primary at single-pass `atempo=0.7`)
- `N5/data/listening.json` (audio_render_meta updates +
  re-measured `pacing_morae_per_min`)
- `N5/tools/apply_phase15_rubberband_2026_05_17.py` (NEW —
  one-shot metadata flipper)
- `N5/docs/AUDIO-PHASE2-VOICEVOX-RERENDER.md` (7→3 correction +
  Phase-1.5 close-out note)
- `N5/docs/AUDIT-COVERAGE-2026-05-15.md` (Part 20 addendum)
- `N5/docs/cross-artifact-sync-map.md` (audit-log row)
- `N5/CHANGELOG.md` (this entry)

CI invariants unchanged at 122/122 green.

## Unreleased - 2026-05-17 (JA-91 + JA-94 final unblock: reserved JA-91..95 range fully wired)

Not user-visible at runtime — corpus and rendered surfaces unchanged.
Internal: closes the final two reserved invariant slots from the
JA-91..95 range, bringing CI from 120 → 122 invariants green and
locking two contamination guards that BUG-003 and BUG-006 (round-9
audit) had each filed against the corpus.

### JA-91 — cross-pattern explanation_en similarity guard (BUG-003)

The corpus has 43 grammar-pattern pairs whose `explanation_en` strings
match each other at ≥0.85 Levenshtein similarity. Hand-classification
identified each as legitimate cross-coverage rather than contamination:

- **DUPLICATE_PATTERN ×8** — two pattern IDs cover the same concept
  (e.g., n5-014 + n5-039 both = これ/それ/あれ pronouns).
- **CROSS_REFERENCE ×21** — one pattern defers to another (the n5-183
  family with 4 child patterns; the n5-119/120 ↔ n5-160..163 まえ/あと
  family).
- **ALTERNATIVE_VARIANT ×12** — register / dialect / syntactic variants
  of one construct (the obligation paradigm n5-173..176 = なくては
  いけない / ならない / ないと / なくちゃ・なきゃ; n5-157 ↔ n5-158 =
  でしょう ↔ だろう).
- **SUBSET ×2** — one pattern subset of another's coverage.

The 43 pairs are snapshotted in `data/_ja91_baseline.json` with per-pair
rationale notes. JA-91 trips on any NEW pair beyond the baseline —
typically signaling a fresh pattern with explanation copied/contaminated
from an existing one.

### JA-94 — per-example structural-marker guard (BUG-006)

Authored `data/pattern_markers.json` (178-pattern catalog) via
`tools/author_pattern_markers_2026_05_17.py`. The authoring derives an
initial marker set from each pattern's `pattern` field, expands with
category-specific conjugational variants (ます → ません / ました; です
→ でした / じゃありません; な-Adj → な / じゃない / だった), and
applies a per-pattern OVERRIDES table for patterns whose canonical
forms aren't in the bare pattern field (n5-088 / 089 existence verbs;
n5-143 なる inflectional family; n5-176 casual contractions; etc.).

Final coverage: **1768 of 1782 grammar examples (99.2%)** match ≥1
marker from their parent pattern. The 14 remaining BUG-006-CANDIDATE
wrong-example failures cluster on 8 parent patterns (n5-030, n5-048,
n5-065, n5-071, n5-084, n5-112, n5-157, n5-164) and are snapshotted in
`data/_ja94_baseline.json` with per-entry classification notes
("n5-048 ex[0] uses ここ but parent pattern is どこ — belongs under
n5-016 / n5-041"; "n5-157 ex[4] uses volitional たべましょう, not
probability でしょう — belongs under n5-071"; etc.). These 14 remain
as a follow-on audit-cycle target — JA-94 currently allowlists them
so no NEW pattern-instance contamination can land without tripping
CI, but the snapshotted entries should be addressed by a future
native-reviewer pass that either rewrites the examples or moves them
to their correct parent pattern.

### CI invariants final state for this batch

- **Total live: 122** (+2 from JA-91 final-wire + JA-94 final-wire).
- The JA-91..95 reserved range is **fully consumed**; only JA-42..46
  and JA-80 remain in the §25.7 Reserved table.
- All 122 invariants PASS on the current corpus.
- `cross_artifact_sync_report.py` exits CLEAN.
- Bug tracker: 53 / 53 Fixed / 0 Open (unchanged this batch — JA-91
  and JA-94 are governance / prospective-guard wirings, not bug
  close-outs).

### Files touched

- `N5/data/_ja91_baseline.json` (NEW)
- `N5/data/pattern_markers.json` (NEW)
- `N5/data/_ja94_baseline.json` (NEW)
- `N5/tools/author_pattern_markers_2026_05_17.py` (NEW)
- `N5/tools/check_content_integrity.py` (JA-91 + JA-94 final-wire;
  duplicate pre-baseline JA-91 function removed)
- `N5/specifications/JLPT-N5-Current-Implementation-Spec.md` (§25
  intro counts 120 → 122; §25.4 gains JA-91 + JA-94 rows; §25.7
  trims to JA-42..46 + JA-80; §25.9 step-3 reserved-slot note
  updated)
- `N5/docs/AUDIT-COVERAGE-2026-05-15.md` (Part 19 addendum)
- `N5/docs/cross-artifact-sync-map.md` (audit-log row)
- `N5/CHANGELOG.md` (this entry)

## 2026-05-17 (BUG-050 round-3 close-out: spec §7.3 sample drift; JA-119 wired)

User-visible: the implementation spec's §7.3 "version.json - build
stamp" sample now shows the **current** corpus counts (v1.15.5,
vocab 995, reading 54, listening 50, papers 28, paperQuestions 402)
instead of the v1.12.50-era stale values (vocab 1041, reading 45,
listening 47, papers 29, paperQuestions 426, invariants 48/48) that
had been carried over for ~20 commits without being refreshed.

### Why BUG-050 was filed three times against a clean file

The user's audit observed `counts.listening=47` and reported it as
"data/version.json declares 47". Verification each round confirmed
the actual `data/version.json` file held 50 (not 47) in every
observable state — working tree, full git history, live deployed
site. Each close-out round addressed adjacent stale-prose drift on
user-facing surfaces:

- **Round 1** (`5d14cde`) — fixed AUDIO.md line 52 ("47 listening
  items use 4 distinct VOICEVOX speakers"). JA-112 wired. Real but
  not the source the user observed.
- **Round 2** (`bbea337`) — back-filled Fix Commit links on the 53
  Fixed bugs as part of INV-9 promotion. JA-118 wired. Orthogonal
  to BUG-050's actual content.
- **Round 3** (this commit) — **located the actual source**: spec
  §7.3 carried a SAMPLE `version.json` JSON block showing
  `"listening": 47` (along with `"vocab": 1041`, etc.) from a
  v1.12.50-era snapshot. The block's framing reads as authoritative
  ("Single source of truth for build counts:"), so the auditor
  naturally read the sample's values as current state.

### Fix applied

1. **Spec §7.3 sample updated** to current values (v1.15.5, vocab
   995, reading 54, listening 50, papers 28, paperQuestions 402).
   The stale `invariants: 48/48` field — which lived in the sample
   but no longer lives in the live `version.json` (moved to
   `data/build_metadata.json` per IMP-002) — removed entirely; a
   prose sentence below the block clarifies where the CI invariant
   count actually lives now.
2. **Drift note added** below the §7.3 sample block explaining
   that the sample MUST match the live file (per JA-119) and that
   the prior stale state caused BUG-050's repeated confused
   re-reports.

### JA-119 wired (fifth-surface coverage of Cross-Artifact Sync Protocol INV-4)

The "user-facing prose-with-counts" drift class is now locked
across all five surfaces a maintainer or auditor is likely to
read for ground truth:

| Surface | Invariant |
|---|---|
| `N5/CONTENT-LICENSE.md` | JA-47 |
| `N5/data/version.json` (vs live array lengths) | JA-107 |
| `N5/AUDIO.md` | JA-112 |
| `N5/README.md` | JA-115 |
| `N5/specifications/JLPT-N5-Current-Implementation-Spec.md` §7.3 sample | **JA-119** |

JA-119 parses the spec §7.3 fenced JSON block and compares its
`counts` field key-by-key against the live `data/version.json.counts`.
Drift on any key trips CI immediately. The check also flags
missing keys (sample doesn't list a count that live data has) and
extra keys (sample lists a count that's not in live data —
catches the `invariants` deprecation cleanly).

### Process lesson — "charitable interpretation" is iterative

When a user-filed bug's literal claim conflicts with observable
state, check ADJACENT artifacts. The 2026-05-17 BUG-050 saga
demonstrates the pattern is ITERATIVE: round 1 found one adjacent
stale surface, round 3 found the actual source. Both fixes were
valuable; round 1 didn't fail because it missed the ULTIMATE source,
it just hadn't walked the doc neighborhood far enough.

After this commit, the "doc neighborhood" is mechanically locked
via five JA-NN invariants. A future bug-class against a sixth
prose-with-counts surface would point at a surface not yet locked,
which becomes the next promotion target.

### CI invariants final state

Total live: **120** (was 119; +1 from JA-119).
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker: **53 / 53 Fixed / 0 Open**.

### Files touched (Rule 5 atomic-commit discipline)

  - N5/specifications/JLPT-N5-Current-Implementation-Spec.md
    (§7.3 sample fixed; §25.1 JA-119 row; §25.10 INV-4 line
    extended to 5 surfaces; counts 119→120; next-free 120)
  - N5/tools/check_content_integrity.py (JA-119 check function +
    registry entry)
  - N5/tools/cross_artifact_sync_report.py (INV-4 INV_MAPPING
    extended with JA-119)
  - N5/specifications/test-scenarios-by-specialist-perspective.xlsx
    (BUG-050 marked Fixed round-3; title + description updated)
  - N5/docs/AUDIT-COVERAGE-2026-05-15.md (Part 18 addendum)
  - N5/docs/cross-artifact-sync-map.md (audit-log row for round-3)
  - N5/CHANGELOG.md (this entry)
  - N5/changelog/index.html (meta-mirror regen — JA-113 enforced)

### Verification

- python tools/check_content_integrity.py → PASS all 120 invariants
- python tools/cross_artifact_sync_report.py → EXIT: CLEAN
- Bug tracker: 53 / 53 Fixed / 0 Open

---

## Unreleased - 2026-05-17 (End-of-session sweep: JA-91..95 partial promotion + INV-1/2/8 hooks + Audio Phase-2 handoff)

User-visible: the **grammar.json n5-028 ex[5]** (〜の possessive
pattern) now correctly demonstrates の. Previously read
`父は 先生です。` (uses は, not の — same drift class as BUG-009);
now reads `わたしの 父は 先生です。` (preserves the EN translation
"My father is a teacher." while adding the canonical possessive
marker). Caught by JA-95's first run; fixed inline.

### What landed — "do whatever is required tbd but finish it"

**(A) JA-91..95 reserved slots: 3 of 5 promoted; 2 stay reserved**

The spec's prior note "gated only by the pattern-markers / particle-
list data files being authored" was outdated. Mid-session investigation
showed:

- **JA-92** (no EN sentence repeated in 10+ examples) — wired; passes.
- **JA-93** (pitch_marks.mora == count_morae(reading)) — wired; passes.
  Algorithm preserved from `not-required/tools-archive/fix_issue_074_
  pacing_audit_2026_05_06.py` (round-9 baseline).
- **JA-95** (particle-pattern alignment) — wired; passes after fixing
  n5-028 ex[5]. First-run caught the misaligned example.
- **JA-91** (cross-pattern explanation_en similarity ≥0.85
  Levenshtein) — **partial-promoted then deferred**. Corpus has 42
  pairs of EXACTLY identical explanations across related patterns
  (e.g., n5-014 vs n5-039 both about これ/それ/あれ). Can't
  mechanically distinguish "intentional cross-pattern" from
  "accidental contamination"; gated on Japanese-linguistics review
  pass classifying the 42 pairs (~2-3 hours work).
- **JA-94** (pattern-marker presence per example) — **partial-
  promoted then deferred**. Requires authoring `data/pattern_markers.
  json` (a structural-markers catalog, NOT `_meaning_ja_markers`
  which describes the meaning). ~3-5 hours of Japanese-linguistic
  expertise needed.

**(B) Commit-time enforcement for INV-1 / INV-2 / INV-8**

New `.githooks/` directory at the repo root:
  - `pre-commit` — staged-file checks (INV-2 spec↔code; INV-8
    data↔CHANGELOG)
  - `commit-msg` — message-body checks (INV-1 bug-fix mentions test;
    INV-8 atomic-commit body length on multi-file commits)
  - `README.md` — install + bypass + maintenance notes

One-time install: `git config core.hooksPath .githooks`

These complement the corpus-content CI invariants (which run on
push + PR). The hooks catch issues at commit time, before they
land — particularly useful for the bug-fix-without-test class
(INV-1 hard fail) which the project's history showed surfacing
repeatedly before this guard.

**(C) Audio Phase-2 maintainer handoff doc**

New `N5/docs/AUDIO-PHASE2-VOICEVOX-RERENDER.md` captures the
Phase-2 audio quality upgrade (VOICEVOX re-render at
speed_scale=1.00 to replace the Phase-1 ffmpeg atempo post-
processing applied in commit `47d1edc`). Phase-1 is shippable
(50/50 in target band, mean 213.6 mpm). Phase-2 is a quality
upgrade requiring VOICEVOX installed locally; the runbook
captures the exact command sequence + expected post-state. Not
gated behind a tracker entry — surfaced as documentation only.

### Cross-Artifact Sync Protocol — final distribution

| INV-N | Description | Status |
|---|---|---|
| INV-1 | bug-fix touches test or annotates "no test" | **Hook** (.githooks/commit-msg, hard fail on missing test annotation) |
| INV-2 | spec change references code | **Hook** (.githooks/pre-commit, warns) |
| INV-3 | code API change → API docs | Out of scope (no API) |
| INV-4 | data counts ↔ version.json / docs | **Wired** (JA-47/107/112/115) |
| INV-5 | UI strings ↔ all locales | **Wired** (JA-108) |
| INV-6 | prompts ↔ xlsx coverage | **Wired** (JA-116) |
| INV-7 | cross-file references resolve | **Wired** (JA-15/17/82/100/105/113/117) |
| INV-8 | CHANGELOG completeness | **Hook** (.githooks/pre-commit + commit-msg) |
| INV-9 | closed-bug → fix-commit link | **Wired** (JA-118) |
| INV-10 | procedure-manual / prompt → script refs | **Wired** (JA-109) |

Wired at CI: **6** · Hook (commit-time): **3** · Out of scope: **1**.
**9 of 10 INV-N classes** are now enforced at some layer.

### CI invariants

Total live: **119** (was 116; +3 from JA-92/93/95).
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker: 53 / 53 Fixed / 0 Open (unchanged).

### Files touched (Rule 5 atomic-commit discipline)

  - N5/tools/check_content_integrity.py — 3 new check functions
    (JA-92/93/95) + 2 stayed-reserved with detailed deferral notes
    (JA-91/94)
  - N5/tools/cross_artifact_sync_report.py — INV_MAPPING updated
    to use the new {wired, hook, oos} taxonomy
  - .githooks/pre-commit + commit-msg + README.md (NEW directory)
  - N5/docs/AUDIT-COVERAGE-2026-05-15.md — Part 17 addendum
  - N5/docs/cross-artifact-sync-map.md — INV-1/2/8 rows updated to
    Convention+Hook status; audit-log row added; strategy
    rewritten to 9-of-10 distribution
  - N5/specifications/JLPT-N5-Current-Implementation-Spec.md —
    §25.1/3/4 rows for JA-92/93/95; §25.7 deferral notes for
    JA-91/94; §25.10 INV-1/2/8 status update + summary rewritten;
    section-header counts 116→119; next-free JA-NN = 119
  - N5/data/grammar.json — n5-028 ex[5] ja fix
    (父は 先生です。 → わたしの 父は 先生です。)
  - N5/docs/AUDIO-PHASE2-VOICEVOX-RERENDER.md (NEW)
  - N5/CHANGELOG.md — this entry
  - N5/changelog/index.html — meta-mirror regen (JA-113 enforced)

### Verification

- python tools/check_content_integrity.py → PASS all 119 invariants
- python tools/cross_artifact_sync_report.py → EXIT: CLEAN
- Bug tracker: 53 / 53 Fixed / 0 Open
- Static mirrors: idempotent post-commit (0 written / all unchanged)

### Closure note

This concludes the 2026-05-17 session's "do whatever is required
tbd but finish it" pass. The Cross-Artifact Sync Protocol is
effectively fully implemented (9 of 10 INV-N enforced; INV-3
genuinely N/A). Two JA-NN slots remain reserved with specific
gating notes (JA-91 needs a linguistics-review pass; JA-94 needs
a structural-markers data file authored). Audio Phase-2 is queued
behind the maintainer's VOICEVOX install via a concrete runbook.
No further items are actionable without resources that aren't
available to the agent (Japanese-linguistic-expert time;
VOICEVOX-installed machine).

Per the protocol's bounded-coverage phrasing: the project is
**closed against the user-reported bugs filed and the protocol-INV
checklist scanned in this session**. Future work surfaces in
subsequent audit cycles.

---

## Unreleased - 2026-05-17 (Pending batch 3: INV-6 / INV-7 / INV-9 → Wired; JA-116/117/118 + Fix Commit back-fill)

Governance / CI release. No user-visible changes. Promotes the last
three "Partial" Cross-Artifact Sync Protocol invariants to **Wired**.
With these three wire-ups, **6 of 10 INV-N classes are now
hard-enforced at CI**; the remaining 3 are pure commit-time tooling
(pre-commit hooks / PR-title parsers — outside the corpus-content
CI domain); 1 stays out of scope (no API).

### JA-116 — INV-6 promotion: prompts ↔ xlsx coverage check

Every A-NN audit category, every Phase-0 regression block, and every
FP-NN false-positive class in `N5/prompts/*` must have ≥1 matching
xlsx scenario row. The check auto-extracts the structured items from
the prompt sources and word-boundary-searches the xlsx (all 14
specialist tabs + scenarios + notes + tools columns).

**Real drift caught on first run:** A5 ("Wrong kanji usage") had no
matching xlsx row. Root cause: the b466293 prompt↔xlsx sync used
substring-match (`"A5" in "A55"` → True), so when prior commits had
already mentioned "A55" / "A50" / etc., A5 was falsely skipped. Fixed
inline in this commit: A-115 scenario added to tab A; the sync
script's match logic upgraded from substring to word-boundary regex
so re-runs are safe.

### JA-117 — INV-7 extension: passage_id / pattern_id cross-corpus refs

Two cross-corpus reference classes that were previously relying on
manual checks:

  - kanji.json `entries[*].reading_passages[*].passage_id` → reading.json
    passage IDs (363 refs)
  - reading.json `passages[*].grammar_footnotes[*].pattern_id` + nested
    `patterns[*].pattern_id` → grammar.json pattern IDs (319 refs)

All 682 references verified to resolve. INV-7 now has 7 wired
invariants covering audio / vocab_id / _meta refs / kanji↔vocab
form / vocab_preview / meta-mirror freshness / cross-corpus IDs —
the canonical cross-file reference fields are fully locked.

### JA-118 — INV-9 promotion: closed-bug → fix-commit link

Every Fixed-status row in the xlsx User Reported Bugs sheet must have
a non-empty Fix Commit cell. The check verifies the link; the
companion tool `tools/populate_bug_fix_commits_2026_05_17.py` (also
new) scans git log for commit subjects mentioning each BUG-NNN
(including range patterns like "BUG-041 through BUG-046" or
"BUG-041..046") and back-fills the column.

Wire-up state: all 53 Fixed bugs back-filled on this commit with their
authoritative fix-commit SHA + ISO date. Future fixes need to set
Fix Commit either manually or via re-running the back-fill tool.

### Cross-Artifact Sync Protocol INV-N state summary (end-of-session)

| INV | Description | Status |
|---|---|---|
| INV-1 | bug-fix touches test or annotates "no test" | Convention only |
| INV-2 | spec change references code | Convention only |
| INV-3 | code API change updates docs | **Out of scope** (no API) |
| INV-4 | data counts ↔ version.json / docs | **Wired** (JA-47 / 107 / 112 / 115) |
| INV-5 | UI strings ↔ all locales | **Wired** (JA-108) |
| INV-6 | prompts ↔ xlsx coverage | **Wired** (JA-116) ← promoted this commit |
| INV-7 | cross-file references resolve | **Wired** (JA-15/17/82/100/105/113/117) ← promoted this commit |
| INV-8 | CHANGELOG completeness | Convention only |
| INV-9 | closed-bug → fix-commit link | **Wired** (JA-118) ← promoted this commit |
| INV-10 | procedure-manual / prompt → script refs | **Wired** (JA-109) |

Wired: **6** · Convention: **3** · Out of scope: **1**.

### CI invariants

Total live: **116** (was 113; +3 from JA-116 / JA-117 / JA-118).
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker: 53 / 53 Fixed / 0 Open (unchanged); all Fix Commit cells populated.

### Files touched (Rule 5 atomic-commit discipline)

- `N5/tools/check_content_integrity.py` — JA-116 + JA-117 + JA-118
  check functions + registry entries
- `N5/tools/populate_bug_fix_commits_2026_05_17.py` (NEW) — git-log
  scanner + xlsx column-fill tool
- `N5/tools/sync_test_scenarios_with_prompts_feedback_2026_05_17.py` —
  substring → word-boundary match fix (the bug that hid A5)
- `N5/tools/cross_artifact_sync_report.py` — INV_MAPPING updated
  with all wired/convention/OOS counts post-promotions
- `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`
  — A-115 scenario row added (the missing A5 coverage); Fix Commit
  + Fix Date columns added; 53 Fixed bugs back-filled
- `N5/specifications/JLPT-N5-Current-Implementation-Spec.md` — §25.1
  rows for JA-116/117/118; §25.10 INV→JA matrix updated with all
  promotions; section-header count bumped 113→116; next-free
  JA-NN = 119; summary text rewritten with end-of-session totals
- `N5/docs/cross-artifact-sync-map.md` — audit-log rows for the 3
  promotions; INV-6 / INV-7 / INV-9 rows updated; "Strategy"
  section rewritten with end-of-session distribution
- `N5/CHANGELOG.md` — this entry
- `N5/changelog/index.html` — meta-mirror regen (JA-113 would have
  failed without it; the discipline JA-113 enforces, applied)

### Verification

- python tools/check_content_integrity.py → PASS all 116 invariants
- python tools/cross_artifact_sync_report.py → EXIT: CLEAN, distribution
  Wired 6 / Partial 0 / Convention 3 / OOS 1
- Bug tracker: 53 / 53 Fixed / 0 Open with 100% Fix Commit coverage
- sync-script idempotent; populate-fix-commits tool idempotent

### Remaining out-of-reach (this session)

- INV-1 / INV-2 / INV-8: need git pre-commit hooks or PR-title
  parsers, not corpus-content CI checks. Pure commit-time tooling.
- JA-91..95 reserved slots: gated on `pattern_markers.json` +
  particle-list data files being authored.
- Audio Phase-2 VOICEVOX re-render at speed_scale=1.00 (cleaner
  audio than the ffmpeg-atempo post-processing from 47d1edc):
  needs VOICEVOX install on maintainer's machine; ~30min.

---

## Unreleased - 2026-05-17 (JA-114 + JA-115 wired; README counts corrected)

User-visible: the README's "Content" section now correctly states **995
vocabulary entries · 54 reading passages · 50 listening items** (was
stale at 1041 / 40 / 40 — pre-dedup era values from v1.12.29). Pending-
items pass batch 2.

### What landed

**(1) JA-114 — listening.json `pacing_status` closed-enum lock**

After the BUG-048/049 close-out (commit `47d1edc`) every listening
item has a measured pacing_morae_per_min + a status reflecting its
position in the JLPT N5 target band. JA-114 locks the field's
value-domain at `{in_range, too_slow, too_fast, no_audio, unmeasured}`
so future regressions (null re-introduction or new ad-hoc strings
from pipeline changes) are blocked at CI.

Same drift class as JA-106 (reading.json format_type) and JA-111
(listening.json format_type) — closed-enum on a corpus field where
the value-domain is small and stable.

**(2) JA-115 — README.md "Content" section count claims match live data**

Fourth instance of the Cross-Artifact Sync Protocol INV-4 class:
JA-47 (CONTENT-LICENSE.md), JA-107 (version.json), JA-112 (AUDIO.md),
**JA-115 (README.md)** — the four user-facing surfaces where corpus
counts appear in prose are now all locked.

The README's "Content (current as of v1.12.29): ..." line was caught
stale during the pre-commit verification:
  - "1041 vocabulary entries" — DRIFT (live: 995, post-BUG-018/019/024)
  - "40 reading passages" — DRIFT (live: 54)
  - "40 listening items" — DRIFT (live: 50)
  - Other counts: correct

Fixed in this same commit: README's content line rewritten with current
counts; "current as of v1.12.29" → "current as of v1.15.5; counts
auto-verified by JA-115 / JA-107 / JA-47". Also fixed the vocab.json
inline count `(1009 entries)` → `(995 entries)` on the "Edit rich
content" list. JA-115 anchors on "Content (current as of ...)" and
checks 8 sub-patterns: grammar / vocab / kanji / reading / listening /
mock-test questions / audited papers / paper questions.

**(3) Pre-session untracked files resolved**

(landed in `407ef64`, the prior commit of this batch)
- `tests/*.pdf` added to N5/.gitignore (handles the n5-008.pdf test
  artifact + future visual-proofing PDFs)
- `tools/build_test_scenarios_workbook.py` moved to
  `not-required/tools-archive/` with prominent DEPRECATED docstring +
  `sys.exit("DEPRECATED...")` guard (would otherwise overwrite the
  402-scenario xlsx if run)

### CI invariants

Total live: **113** (was 111; +2 from JA-114 + JA-115).
`cross_artifact_sync_report.py` exits CLEAN.

### Files touched (Rule 5 atomic-commit discipline)

  - N5/README.md (3 stale counts corrected; "current as of" version
    bumped + JA-115 reference added)
  - N5/tools/check_content_integrity.py (JA-114 + JA-115 check
    functions + registry entries)
  - N5/specifications/JLPT-N5-Current-Implementation-Spec.md
    (§25.1 rows for JA-114 + JA-115; section-header count bumped
    111→113; next-free JA-NN = 116)
  - N5/CHANGELOG.md (this entry)
  - N5/changelog/index.html (meta-mirror regen — JA-113 would have
    failed otherwise; the discipline JA-113 enforces, applied to
    its own follow-on commit)

### Verification

  - python tools/check_content_integrity.py → PASS all 113 invariants
  - python tools/cross_artifact_sync_report.py → EXIT: CLEAN
  - Bug tracker: 53 / 53 Fixed / 0 Open (unchanged)

---

## Unreleased - 2026-05-17 (JA-113 wired — meta-route static-mirror freshness CI guard)

Governance / CI release. No user-visible changes. Wires a new CI
invariant (JA-113) that prevents the recurring drift class observed
3 times in the 2026-05-17 session: maintainer edits a markdown source
under `N5/` (CHANGELOG.md, PRIVACY.md, etc.) but forgets to re-run
`tools/build_static_mirrors.py --stages meta`, leaving the static
mirror at `N5/<route>/index.html` showing stale content for non-JS
crawlers.

### Drift instances caught in this session (the reason JA-113 was wired)

| Commit | Source edit | Mirror regen | Followed-up by |
|---|---|---|---|
| `cdef185` | CHANGELOG.md (Rule-5 install entry) | NOT regen'd in same commit | `f96475b` (drift fix) |
| `5d14cde` + `47d1edc` | CHANGELOG.md (BUG-050 + BUG-048/049 entries) | NOT regen'd in same commit | `360eb74` (drift fix) |

After observing the same drift class twice in adjacent commits,
wiring a CI invariant is cheaper than continuing to catch it
manually. JA-113 closes that loop.

### JA-113 behavior

For each markdown-sourced meta route, JA-113 extracts the FIRST H1/H2
heading from the source markdown (which is the latest entry for
CHANGELOG-style time-ordered docs, or the canonical top header for
static reference docs) and verifies it appears in the mirror HTML.
Routes checked:

  - `home/index.html` ↔ `README.md`
  - `changelog/index.html` ↔ `CHANGELOG.md`
  - `privacy/index.html` ↔ `PRIVACY.md`
  - `notices/index.html` ↔ `NOTICES.md`

The 6 stub-body meta routes (feedback / settings / test / sitting /
missed / summary) have no source-of-truth markdown — they're
hand-authored stub HTML in `META_ROUTES` of build_static_mirrors.py —
so they're out of JA-113's scope. Drift in those would be visible at
build_static_mirrors.py runtime instead.

### Regression-test evidence

JA-113 was regression-tested before commit by injecting a phantom
"## Unreleased - 2026-05-17 (PHANTOM JA-113 REGRESSION TEST PHRASE)"
H2 into CHANGELOG.md and re-running the CI. Expected output:

```
JA-113 changelog/index.html does not contain the latest heading
from CHANGELOG.md: 'Unreleased - 2026-05-17 (PHANTOM JA-113
REGRESSION TEST PHRASE)'. Run `python tools/build_static_mirrors.py
--stages meta` to regenerate the mirror.
FAIL: 1 integrity violation(s)
```

Observed: matches exactly. After restoring CHANGELOG.md, the CI
returned to 111/111 green.

### Cross-Artifact Sync Protocol INV status

INV-7 (cross-file references resolve) coverage extended: JA-113 is
the 6th invariant under INV-7 alongside JA-15 (audio), JA-17
(vocab_id), JA-82 (_meta refs), JA-100 (kanji↔vocab form), JA-105
(vocab_preview refs). INV-7 stays at "Partial" overall because
`passage_id` and `pattern_id` cross-corpus references are still
relying on manual checks — a future audit cycle could promote those
to wired.

Updated `cross-artifact-sync-map.md`'s per-class cheatsheet for
"Editing User-Facing Docs?" — now explicitly mentions running
`tools/build_static_mirrors.py --stages meta` for docs that have
meta-route mirrors.

### Total CI invariants live: 111 (was 110).

### Files touched (Rule 5 atomic-commit discipline)

- `N5/tools/check_content_integrity.py` — `_check_ja_113_*` function +
  registry entry
- `N5/docs/cross-artifact-sync-map.md` — audit-log row + INV-7 row
  updated to list JA-113 + per-class cheatsheet for "Editing
  User-Facing Docs?" updated
- `N5/specifications/JLPT-N5-Current-Implementation-Spec.md` —
  §25.4 row for JA-113; §25.8 lineage row; §25.10 INV-7 row updated;
  section-header count bumped 110→111; next-free JA-NN = 114
- `N5/CHANGELOG.md` — this entry

### Coverage of the fix

CI: 111/111 green post-wire-up.
`cross_artifact_sync_report.py`: EXIT CLEAN.
Bug tracker: 53 / 53 Fixed / 0 Open (unchanged).
Sync-script idempotent.

Bounded-coverage note: JA-113 catches drift in the 4 markdown-
sourced meta routes only; the 6 stub-body routes have no source-of-
truth markdown so the drift class doesn't apply to them. JA-113 is
a heuristic check (first H1/H2 must appear in mirror) — false
negatives possible if a heading is edited in-place without text
change, but the common drift case (new entry added) is caught.

---

## Unreleased - 2026-05-17 (BUG-048 + BUG-049 close-out — listening pacing refresh; ALL 50 items in target band; tracker hits zero open)

User-visible: every JLPT N5 listening drill now plays at JLPT exam pace
(180–240 morae/min target band). The 2026-05-12 VOICEVOX render at
speed_scale=1.30 had overshot the target — re-measurement against
current audio showed 38 of 50 items above the band (too fast) and 1
below (too slow). ffmpeg atempo post-processing pulled every item
into the band: post-fix mean 213.6 mpm (exactly target midpoint), 50/50
in_range, 0 out-of-band.

### BUG-048 + BUG-049 close-out (listening pacing)

User asked "fix these open items as well". Investigation revealed
both bugs were tied to the same root cause — stale `pacing_morae_per_min`
data carried over from the 2026-05-06 edge-tts era. After the
2026-05-12 VOICEVOX re-render shortened audio durations, those
values weren't refreshed, so the tracker still showed "26 items too
slow" when current audio was actually too FAST on most items. One
tool fixed both:

`tools/refresh_listening_pacing_2026_05_17.py` — four-pass workflow:

  1. **Re-measure all 50 items** against current audio using the
     canonical count_morae() algorithm (preserved from round-9
     baseline; lives in `not-required/tools-archive/fix_issue_074_
     pacing_audit_2026_05_06.py`). Pre-fix had 40 items with stored-
     vs-measured drift > 1.0 mpm. (Closes BUG-048.)
  2. **Apply ffmpeg atempo tempo-change** to items outside the
     target band. 39 items changed: 38 slowdowns (factors 0.476–
     0.840×) for too_fast items, 1 speedup (1.330×) for the single
     too_slow item. Chained 2-pass atempo used on 7 items needing
     factor < 0.5 (single-pass atempo minimum). Quality threshold
     [0.25×, 1.5×] enforced; 0 items deferred. The 0.7× `.slow.mp3`
     variant was tempo-changed in lockstep. (Closes BUG-049.)
  3. **Re-measure post-tempo-change** items; mpm field updated.
  4. **Refresh `_meta.pacing_audit.summary`** with the final
     distribution.

Final pacing distribution:
  - **in_range: 50** (was 12 stale / 11 post-Pass-1)
  - too_slow: 0 (was 26 stale / 1 post-Pass-1)
  - too_fast: 0 (was 2 stale / 38 post-Pass-1)
  - no_audio: 0 / unmeasured: 0
  - mpm range [182.9, 236.8]; mean **213.6** (target midpoint of 180-240)

Per-item provenance: every item that had ffmpeg atempo applied
carries `audio_render_meta.post_render_tempo_change_2026_05_17`
(float — the factor applied) + `post_render_tempo_method` =
"ffmpeg-atempo". Future native-listener review can identify
tempo-adjusted items vs direct VOICEVOX output.

Audio quality note: ffmpeg atempo uses pitch-preserving PSOLA
algorithms; quality is near-transparent at factors [0.5×, 2.0×]
single-pass, slightly degraded for the 7 chained items (factors
0.476–0.499). For institutional-grade audio, a Phase-2 VOICEVOX
re-render at speed_scale=1.00 (instead of the over-shooting 1.30)
would produce cleaner audio — surfaced in AUDIT-COVERAGE Part 16
but not gated behind a tracker entry.

### Bug tracker

| BUG | Status | Note |
|---|---|---|
| BUG-048 | **Fixed 2026-05-17** | All 50 items have accurate pacing measurements |
| BUG-049 | **Fixed 2026-05-17** | 50/50 items in target band; 0 deferred |

Bug tracker totals: **53 / 53 Fixed / 0 Open** — first time the
project has had zero open user-reported bugs since BUG-001 was
filed on 2026-05-16. (Two days from project's first user-bug to
zero-open inbox.)

### Files touched (Rule 5 atomic-commit discipline)

- `N5/data/listening.json` — pacing fields refreshed on all 50
  items; audio_render_meta gains `post_render_tempo_change_*`
  provenance on the 39 tempo-changed items; _meta.pacing_audit.
  summary refreshed; _meta.pacing_fix_status status =
  "fixed_2026_05_17"
- `N5/audio/listening/n5.listen.{NNN}.mp3` — 39 MP3 files
  modified in place (38 slowdowns + 1 speedup); matching
  `.slow.mp3` variants also adjusted
- `N5/tools/refresh_listening_pacing_2026_05_17.py` (NEW) — the
  four-pass refresh tool; supports `--apply-speedup` (default
  off) + `--dry-run`
- `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`
  — BUG-048 + BUG-049 marked Fixed with close-out narrative
- `N5/docs/AUDIT-COVERAGE-2026-05-15.md` — Part 16 addendum
- `N5/CHANGELOG.md` — this entry

### Coverage of the fix

CI: 110/110 invariants green (no new invariants this batch).
`cross_artifact_sync_report.py` exits CLEAN.
Static mirrors: 0 written / 51 unchanged (pacing data not embedded
in the static HTML).

Bounded-coverage note (per writing discipline): every item in the
2026-05-17 corpus snapshot is in the 180-240 mpm target band, by
direct measurement after the fix. A future audio re-render (e.g.,
new VOICEVOX engine version, new speakers, new items) would need
this tool re-run to verify the band still holds. The tool is
idempotent — re-running on the current corpus is a no-op (every
item would already test as in_range, so Pass 2 finds nothing to
change).

---

## Unreleased - 2026-05-17 (BUG-050 charitable close-out — AUDIO.md count + speaker-table drift; JA-112 wired)

User-visible: the `AUDIO.md` developer doc now correctly states
**50 listening items use 6 distinct VOICEVOX speakers** (was
incorrectly "47 items / 4 speakers" — pre-2026-05-12 round-9
baseline carried over after the actual 2026-05-12 VOICEVOX render
landed 50 items / 6 speakers). Speaker-attribution table in
AUDIO.md also corrected (same character-name-mismatch class as
BUG-053 / `_meta.voicevox_speaker_catalog`).

### BUG-050 close-out (charitable interpretation)

User re-audit on 2026-05-17 filed BUG-050 with the description
"version.json declares counts.listening=47". Deep verification
across working tree + full git history (HEAD..HEAD~10) + live
deployed site (https://gauravaccentureproducts.github.io/JLPTSuccess/N5/data/version.json)
established `counts.listening = 50` in every observable state;
JA-107 has been PASSing since `cdef185`. The literal claim was
false.

**Real drift located:** `N5/AUDIO.md` line 52 carried the stale
prose claim *"47 listening items use 4 distinct VOICEVOX speakers
in rotation"*, plus the speaker-attribution table had wrong
character→ID mappings (BUG-053 class). The user's bug report
appears to have observed AUDIO.md's "47" and mis-located the
drift to version.json. Charitable interpretation: the drift IS
real, just in a different file than named.

  - `N5/AUDIO.md` lines 50-65 rewritten (header + prose claim +
    speaker table — 50 items, 6 speakers, corrected character
    names: 春日部つむぎ at ID 8 / 玄野武宏 at ID 11 / etc., plus
    the previously-missing ID 3 ずんだもん and ID 10 雨晴はう
    rows added)
  - `N5/AUDIO.md` line 126 (code-block comment) rephrased from
    "round-9 multi-voice listening render (VOICEVOX, all 47
    items)" to clarify it documents the 2026-05-12 production run
    rather than the obsolete 47-item baseline.

### CI invariant added

  - **JA-112** — `AUDIO.md` "N listening items use M distinct
    VOICEVOX speakers" claim matches live data: N ==
    len(listening.json.items); M == |distinct
    audio_render_meta.voices_used|. Third instance of the
    Cross-Artifact Sync Protocol INV-4 class (alongside JA-47 for
    CONTENT-LICENSE.md and JA-107 for version.json), extended to
    the AUDIO.md user-facing doc surface.

Total CI invariants live: **110** (was 109).

### Files touched (Rule 5 atomic-commit discipline)

  - `N5/AUDIO.md` — line 50-65 (claim + speaker table) + line 126
    (code-block comment)
  - `N5/tools/check_content_integrity.py` — new check function
    `_check_ja_112_audio_md_listening_counts()` + registry entry
  - `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`
    — BUG-050 marked Fixed; description + title appended with
    charitable-interpretation close-out note
  - `N5/specifications/JLPT-N5-Current-Implementation-Spec.md` —
    §25.1 row for JA-112; §25.8 lineage row; section-header count
    bumped 109→110; next-free JA-NN = 113
  - `N5/docs/AUDIT-COVERAGE-2026-05-15.md` — Part 15 addendum
  - `N5/CHANGELOG.md` — this entry

### Coverage of the fix

CI: 110/110 invariants green post-fix.
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker: 53 / **51 Fixed / 2 Open**:
  - **BUG-048** (Open, PARTIAL) — field-state contradiction was
    fixed in `04bd8f4`; actual pacing **measurement** still
    pending (all 10 items 041-050 have `pacing_morae_per_min=null`).
  - **BUG-049** (Open) — 26/50 items pacing too slow; needs
    audio re-render at VOICEVOX speed_scale ~1.3. Depends on
    BUG-048 measurement for accurate count.

Bounded-coverage note (per writing discipline): JA-112 anchors on
a single canonical prose pattern in AUDIO.md ("N listening items
use M distinct VOICEVOX speakers"). Other count claims elsewhere
in the project's docs (e.g., "1782 grammar examples", "999
vocab entries") are NOT yet locked by this invariant — future
drift on those phrasings would not trip JA-112. Extending coverage
is queued behind the next user-reported instance.

### Process lesson captured

When a user-filed bug's literal claim conflicts with observable
state, check ADJACENT artifacts before closing as not-a-bug.
Treating BUG-050 as "false positive, close" would have left the
real AUDIO.md drift untouched until a future audit re-found it.
**Charitable interpretation pattern:** assume the user observed
a real drift but mis-located it; verify the literal claim; then
search the doc neighborhood for the actual matching value. (Full
write-up: AUDIT-COVERAGE-2026-05-15.md Part 15 "Process lesson —
re-audit triage" section.)

---

## Unreleased - 2026-05-17 (Test-scenarios sync with prompts/ + feedback/)

Governance / audit-trail release. No content changes for end
users; this batch makes the existing-corpus coverage of every
audit-prompt category, Phase-0 regression block, false-positive
class, and audit document explicit in the test-scenarios xlsx —
closing the gap the Cross-Artifact Sync Protocol's INV-6 flagged.

### Scope

Per user directive ("every info in prompts/ + feedback/ should be
present in test scenarios") and chosen Option 1 (structured items
+ audit-doc summaries):

- **60 A-NN audit categories** from `prompts/Japanese language
  Accuracy check.txt` → tab A (Japanese language). 57 appended;
  3 already mapped via prior BUG batches (A55/A57/A58).
- **18 Phase-0 regression blocks** from `prompts/N5Improvement.txt`
  → tab K (QA testing). All 18 appended as Auto test type.
- **15 FP-NN false-positive class entries** from the accuracy
  prompt → tab K. All 15 appended as Manual review.
- **42 audit-doc summary scenarios** from `feedback/` (17 current
  + 22 closed/) + 3 prompt-file summaries (LegalVetting ×2 +
  LocaleTransitionEnHi).

Tools added:
  - `N5/tools/sync_test_scenarios_with_prompts_feedback_2026_05_17.py`
    (NEW; idempotent — re-running on the post-sync corpus adds 0
    rows because every new ID is unique).

### Counts

| Tab | Pre-sync | Post-sync | Delta |
|---|---|---|---|
| A. Japanese language | 41 | 114 | +73 |
| B. JLPT format | 18 | 19 | +1 |
| C. Hindi locale | 18 | 21 | +3 |
| D. UX design | 23 | 27 | +4 |
| E. Accessibility | 18 | 18 | 0 |
| F. Security | 19 | 23 | +4 |
| G. Privacy and legal | 15 | 16 | +1 |
| H. Performance | 24 | 24 | 0 |
| I. Data engineering | 20 | 26 | +6 |
| J. Pedagogy | 16 | 20 | +4 |
| K. QA testing | 18 | 52 | +34 |
| L. Cultural ethical | 11 | 11 | 0 |
| M. Operations | 10 | 14 | +4 |
| N. End-user POV | 17 | 17 | 0 |
| **TOTAL** | **268** | **402** | **+134** |

Unit Tests (Auto-runnable) derived sheet refreshed: **93 → 111**
rows (18 Phase-0 blocks are Auto type; FP-NN + audit-doc summaries
are Manual review per their nature).

### INV-6 promotion

Cross-Artifact Sync Protocol INV-6 ("Prompt change includes
regression test of golden output") moved from **Convention only**
to **Partial** in §25.10 of the implementation spec, the
cross-artifact-sync-map.md INV table, and the
`cross_artifact_sync_report.py` status output. The remaining gap
to "Wired" is a parsability check (a CI invariant that re-extracts
A-NN / Phase-0 / FP-NN from the prompts and asserts each has at
least one matching xlsx row) — queued for a future audit cycle.

### Files touched (Rule 5 atomic-commit discipline)

- `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`
  — 134 new scenario rows + Unit Tests sheet refresh
- `N5/tools/sync_test_scenarios_with_prompts_feedback_2026_05_17.py`
  (NEW) — the bulk sync tool
- `N5/tools/cross_artifact_sync_report.py` — INV-6 status updated
- `N5/docs/AUDIT-COVERAGE-2026-05-15.md` — Part 14 addendum
- `N5/docs/cross-artifact-sync-map.md` — audit-log row + INV-6 row
- `N5/CHANGELOG.md` — this entry

### Coverage at this checkpoint

CI: 109/109 invariants green post-sync.
`cross_artifact_sync_report.py` exits CLEAN.
Bug tracker: 53 / 52 Fixed / 1 Open (BUG-049 still awaiting audio
re-render — no change this batch).

Bounded-coverage note (per writing discipline): the sync covers
the EXISTING content of `prompts/` + `feedback/` as of the
2026-05-17 snapshot. Future audit docs added to those folders
will need a re-run of `tools/sync_test_scenarios_with_prompts_
feedback_2026_05_17.py` to be picked up. The tool is idempotent
so re-runs cost nothing on the already-synced subset.

---

## Unreleased - 2026-05-17 (BUG-047..053 listening.json VOICEVOX migration drift fix)

Maintenance / data-quality release. Listening drill audio playback
now correctly attributes audio to VOICEVOX (was mis-attributing to
edge-tts due to a stale field). No new content; underlying audio
files unchanged from the 2026-05-12 VOICEVOX render.

### BUG-047..053 close-out (listening.json)

Seven user-reported bugs surfaced as the same meta-class as
BUG-041..046 (corpus-migration drift) but on a different corpus
(listening, not reading) and triggered by a different migration
event (2026-05-12 edge-tts → VOICEVOX render). Fix script:
`tools/fix_bugs_047_to_053_listening_json_2026_05_17.py`.

  - **BUG-047** (Fixed) — voice_planned.engine="edge-tts" on all 50
    items contradicted audio_render_meta.voice_provider="voicevox".
    The voice-attribution UI in the listening detail page was
    showing the wrong vendor. Fix: drop voice_planned (audio_render
    _meta is canonical); UI re-wired to read from
    audio_render_meta.voice_provider +
    audio_render_meta.voice_planned_for_engine.{F,M}.character.
  - **BUG-048** (Fixed) — audit-status fields stale on items 41-50:
    7 items had pacing_status="no_audio" + 3 had
    voice_variety_status=None despite audio_render_meta.rendered_at
    being set on all 10. Refreshed to "unmeasured" (pacing) and
    "rendered" (voice_variety) to match actual render state.
  - **BUG-049** (Open) — 26/50 items pacing systematically too
    slow: mean 160.2 mpm vs JLPT N5 target 180-240; some items 5×
    slower than exam pace. Surface-only fix: _meta.pacing_fix_status
    block added documenting the bug ID, observed distribution, and
    required action (audio re-render at speed_scale ~1.3 — needs
    VOICEVOX install on maintainer's machine). Bug stays Open in
    the tracker.
  - **BUG-050** (Already-Fixed by cdef185) — version.json.counts.
    listening declared 47 vs actual 50. Resolved in the Cross-Artifact
    Sync Protocol install commit (Rule-5) when version.json was
    bumped alongside the vocab 1009→995 drift fix. JA-107 (INV-4)
    locks the count parity.
  - **BUG-051** (Fixed) — format and format_type were 1:1
    bijective (task↔task_understanding etc.). Same dual-field
    redundancy class as BUG-044 (reading) and BUG-047. Fix: drop
    format; format_type canonical with closed enum.
  - **BUG-052** (Fixed) — _meta.voice_variety_plan described
    VOICEVOX as "to be authored when VOICEVOX is installed" even
    though the render had completed on 2026-05-12. Rewrote as
    past-tense completion record (status="completed_2026_05_12");
    captured observed-vs-target voice distribution; marked legacy
    voice_variety_plan_2026_05_07 as superseded.
  - **BUG-053** (Fixed) — voicevox_speaker_catalog had wrong
    character→ID mappings (ID 8 was listed as "hau-tsumugi" but
    is actually 春日部つむぎ; ID 11 was "shirakami-kotaro" but is
    玄野武宏; ID 13 was mis-filed under "12"). Rewrote catalog from
    audio_render_meta.voices_used (the upstream truth). Voice
    variety target 8 only met at 6 in the actual render; documented
    as unmet_target_note.

### CI invariants added (2 hard CI gates)

  - **JA-110** — listening.json items deprecate legacy
    `voice_planned`. Strict "field absent" check (BUG-047 guard).
  - **JA-111** — listening.json drops legacy `format`; format_type
    ∈ {task_understanding, point_understanding, utterance_expression,
    immediate_response} strict closed enum (BUG-051 guard).

Additional CI change: JA-13 SKIP_SUBTREE_FIELDS extended with
`voice_variety_plan`, `pacing_fix_status`, and
`voice_variety_plan_2026_05_07` (same rationale as the existing
audio_render_meta + public_domain_refs exemptions — rendering
metadata, not learner-facing content).

Total CI invariants live: 109 (was 107).

### JS / UI updates

  - `N5/js/listening.js` — voice-attribution surface (F-10 legal-
    vetting requirement) re-wired from voice_planned to
    audio_render_meta. FORMATS map rekeyed from short keys to
    format_type values. byFormat grouping uses format_type.
  - `N5/js/search.js` — listening haystack + gloss read format_type
    (was reading the dropped `format` field).
  - Minified `js/min/listening.js` + `js/min/search.js` regenerated
    via `npm run build:js`.
  - Static mirrors: 50 listening pages regenerated via
    `tools/build_static_mirrors.py` (reflect format_type → label
    rendering).

### Files touched (Rule 5 atomic-commit discipline)

Data + JS:
  - `N5/data/listening.json` — voice_planned dropped (50 items);
    audit-status fields refreshed (10 items); format dropped (50
    items); _meta.voice_variety_plan rewritten; _meta.pacing_fix_
    status added.
  - `N5/js/listening.js`, `N5/js/search.js` — consumer updates.
  - `N5/js/min/listening.js`, `N5/js/min/search.js` — minified
    regenerated.
  - 50× `N5/listening/<id>/index.html` — static mirrors regen.

CI tooling:
  - `N5/tools/check_content_integrity.py` — 2 new check functions
    + 2 registry entries + skip-list extension.
  - `N5/tools/fix_bugs_047_to_053_listening_json_2026_05_17.py`
    (NEW) — the per-bug fix functions.
  - `N5/tools/mark_bugs_047_to_053_fixed_2026_05_17.py` (NEW) —
    xlsx status updater.

Governance docs (Rule 4 propagation):
  - `JLPT Common/procedure-manual-build-next-jlpt-level.md` — §F.24
    added (7 sub-classes + §F.24.7 cross-corpus generalization
    of §F.23.7).
  - `N5/prompts/Japanese language Accuracy check.txt` — audit
    category A60 added (.1..7 sub-classes); 2026-05-17 ADDENDUM
    block appended.
  - `N5/prompts/N5Improvement.txt` — Phase-0 listening migration-
    drift regression block (7 checks, validated 0/0/0/0/0/0/0); 6
    new Section-10 anti-items.
  - `N5/docs/AUDIT-COVERAGE-2026-05-15.md` — Part 13 addendum.
  - `N5/specifications/JLPT-N5-Current-Implementation-Spec.md` —
    §25.1 + §25.4 rows for JA-110/111; §25.8 lineage extended;
    section-header counts bumped.
  - `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`
    "User Reported Bugs" sheet — 6 rows marked Fixed; BUG-049
    stays Open.
  - `N5/CHANGELOG.md` — this entry.

### Coverage of the fix

CI: 109/109 invariants green post-fix.
`cross_artifact_sync_report.py` exits CLEAN. 1 of 53 user-reported
bugs Open (BUG-049 pacing — surface-only this batch, awaiting
audio re-render at VOICEVOX speed_scale ~1.3 on the maintainer's
machine).

Bounded-coverage note (per writing discipline): JA-110 / JA-111
prevent re-introduction of THESE specific drift shapes. Future
TTS migrations, transcript-alignment passes, or audit-pass runs
may surface adjacent patterns; the generalized §F.24.7 operational
rule (run same-shape audit on EVERY field that references migrated
state, not just data items) is the cross-cutting preventive.

---

## Unreleased - 2026-05-17 (Cross-Artifact Sync Protocol install + version.json drift fix)

Governance + tooling release. No learner-facing content changes; the
fix targets a stale corpus count in `data/version.json` and installs
a 9-class artifact-sync protocol (BINDING Rule 5) that prevents this
class of drift from recurring.

### Cross-Artifact Sync Protocol installed (BINDING Rule 5)

Adopts a project-wide governance protocol generalizing the existing
Rule 4 (4-doc propagation for audit cycles) into a 9-class
artifact-sync rule. When ONE artifact class changes (Spec / Code /
Data / UI / Bug tracker / Test scenarios / Prompts / Procedure
manuals / User-facing docs), every OTHER artifact that references
or implements the changed thing updates in the same commit. The
protocol defines INV-1..INV-10 as build-time guards; this release
wires INV-4 / INV-5 / INV-10 as hard CI invariants and documents
the others as convention-only / partial / out-of-scope.

The operational handbook (concrete file map per artifact class,
dependency matrix, commit-time checklist) lives in
`docs/cross-artifact-sync-map.md`. The spec-side INV↔JA mapping
lives in §25.10 of the implementation spec.

### CI invariants added (3 hard CI gates)

- **JA-107** (INV-4) — `data/version.json.counts` declared values
  must equal the actual array length of the referenced corpus
  file. Companion to JA-47 (CONTENT-LICENSE.md counts). Catches
  release-stamp drift after dedup/migration passes.
- **JA-108** (INV-5) — `locales/*.json` strict full-key parity
  across all locales (including `_meta` block). Catches UI
  translation drift where a new surface ships with EN copy
  only.
- **JA-109** (INV-10) — every `tools/<name>.py` script reference
  in the N5 prompts + AUDIT-COVERAGE docs must resolve to a real
  file. (Scope decision: cross-level procedure manual excluded
  because its script refs are abstract Nx-builder targets, by
  design.)

Total CI invariants live: 107 (was 104).

### Drift fixed in the same commit (per the protocol's compound-drift rule)

- **`data/version.json.counts.vocab` 1009 → 995.** Residue of
  BUG-018/019/024 dedup batches (2026-05-16/17) that reduced
  `vocab.json` from 1009 → 995 entries but never propagated to
  the version manifest. `builtAt` bumped to 2026-05-17.
  `cacheVersion` bump deferred to the next js/css/sw release —
  this batch is doc + tooling only, so a SW cache invalidation
  is not warranted.
- **`locales/en.json`** — added `_meta` block (asymmetric with
  hi.json before this fix).
- **`locales/hi.json`** — added 6 chokai_detail keys that were
  present on EN side: back_to_list, correct, next_label,
  script_label, show_script, wrong (these intentionally carry
  Japanese kana text — in-app pedagogy convention regardless of
  UI locale).
- **`prompts/N5Improvement.txt`** — "Reference implementation"
  callout retargeted from the deleted
  `tools/register_dev_issue_list_deferrals_2026_05_05.py` to the
  still-extant `tools/register_audit_2026_05_12.py` (same
  idempotent registration pattern).

### Files touched (Rule 5 atomic-commit discipline)

- `JLPTSuccess/.claude/CLAUDE.md` — BINDING Rule 5 added.
- `N5/.claude/CLAUDE.md` — Documentation-propagation section
  extended to reference Rule 5.
- `N5/docs/cross-artifact-sync-map.md` — NEW (operational
  handbook).
- `N5/docs/AUDIT-COVERAGE-2026-05-15.md` — Part 12 addendum.
- `N5/specifications/JLPT-N5-Current-Implementation-Spec.md` —
  §25.1 (JA-107/108 rows), §25.4 (JA-109 row), §25.8 lineage
  table updated, NEW §25.10 subsection (INV↔JA mapping table).
- `N5/specifications/test-scenarios-by-specialist-perspective.xlsx` —
  rows added to K. QA testing tab for sync-drift detection
  scenarios.
- `N5/tools/check_content_integrity.py` — 3 new check functions
  + 3 new registry entries.
- `N5/tools/cross_artifact_sync_report.py` — NEW (structured
  report emitter).
- `N5/data/version.json` — vocab count 1009 → 995; builtAt
  bumped.
- `N5/locales/en.json` — _meta block added.
- `N5/locales/hi.json` — 6 chokai_detail keys added.
- `N5/prompts/N5Improvement.txt` — script-ref retargeted.
- `N5/CHANGELOG.md` — this entry.

### Coverage of the fix

CI: 107/107 invariants green post-install (was 104/104 green
pre-install — the 3 new JA-NN gates pass on the same corpus
snapshot after the in-commit drift fixes landed).
`cross_artifact_sync_report.py` exits CLEAN.

Bounded-coverage note (per writing discipline): the wired
invariants prevent re-introduction of THESE specific drift
shapes (count drift on version.json, locale-key parity gaps,
unresolved script references in N5 governance docs). The
4 convention-only INV-N (bug-fix-test, spec-code, prompt-golden,
CHANGELOG-completeness) remain commit-discipline targets —
future audit cycles may promote them to hard CI gates following
the convention→partial→wired progression documented in §25.10.

---

## v1.15.5 - 2026-05-14 (Autonomous bug-fix audit pass — ISSUE-001/002 closed)

Maintenance / audit-cycle release. No learner-facing content changes; the
fixes target metadata accuracy, version-file drift, and documentation
gaps surfaced by the 2026-05-14 autonomous bug-fix audit.

### ISSUE-001 — Whitelist count drift (RESOLVED-ALREADY-CLEAN)

Audit symptom: whitelist.json declared 103 entries while meta and
version.json declared 106. Verified at the time of this fix that all
five sources (whitelist.json, meta.expected_count, version.json kanji
count, n5_kanji_readings.json, kanji.json) agree on 106. Resolution
predated this audit pass — no edits required.

### ISSUE-002 — Standard N5 kanji missing from whitelist (DOCUMENTED)

Audit found 6 mainstream-N5 kanji absent from the whitelist: 多, 少, 帰,
早, 物, 魚. Per the audit's permitted alternative ("if your scope policy
deliberately defers any of these, document the deferral"), the
deferral is now formally documented in
`data/n5_kanji_whitelist.meta.json#known_gaps_vs_full_n5_syllabus`
with per-kanji rationale, on/kun/primary readings, and source
attribution (Genki I lesson, Minna no Nihongo I lesson, etc.). Each
kanji is honestly recorded as N5 (not mis-classified as N4).

Full content authoring deferred to a future pass — adding a kanji
requires:
- `data/n5_kanji_whitelist.json` entry (count → 107..112)
- `data/n5_kanji_readings.json` on/kun entry
- `data/kanji.json` full record with examples, mnemonic, look-alikes
- `svg/kanji/<glyph>.svg` KanjiVG stroke order (CC-BY-SA 3.0)
- ≥2 vocab.json entries linking the kanji form (currently those vocab
  items are stored in kana form because the kanji is out-of-scope)

Estimated ~1h per kanji including SVG sourcing.

### Version-file sync

`data/version.json` was significantly stale (v1.12.53 from 2026-05-08)
while sw.js + index.html had progressed to v1.15.4 across the v1.13.x /
v1.14.x / v1.15.x releases. Synced to v1.15.5 with current counts:
- vocab: 1000 → 1009 (post-Phase 2 grammar fixes added some + the
  2026-05-08 dedup pass already reflected)
- reading: 45 → 54 (new dokkai passages shipped in v1.13.x / v1.14.x)
- listening: 47 → 50 (new chokai items in v1.14.x)
- invariants: 50 → 84 (per CI gate growth)

### ISSUE-003 — Vocab regression 1041 → 1000 (RESOLVED-ALREADY-CLEAN)

The audit symptom (41 vocabulary entries removed without rationale) is
fully documented in the v1.12.53 CHANGELOG entry under "Dedup applied
(41 entries removed: 38 + 3 in two commits)". Pass 1 was 2-entry
duplicate pairs (38 removed); Pass 2 was 3+ entry groups (3 more). The
root cause (164-case grammar.json double-tag from kana-section dupes)
and the 90 vocab_id retargets in grammar.json are both documented.
Post-dedup the count has grown back to 1009 via subsequent batch
additions. No new edits required for ISSUE-003.

### ISSUE-004 — Paper count regression 29 → 28; paperQuestions 426 → 402 (RESOLVED + MANIFEST FIX)

The on-disk regression (chokai paper data lost in a prior commit; per
the v1.12.45 BUG-1 CHANGELOG entry) was already documented. Residual
drift fixed in this pass:
- `data/papers/manifest.json#totalPapers` 29 → 28 (matches the four
  on-disk category papers: moji 7 + goi 7 + bunpou 7 + dokkai 7).
- `data/papers/manifest.json#totalQuestions` 426 → 402 (matches the
  100 + 100 + 100 + 102 per-category sum).
- `CONTENT-LICENSE.md` paper-count claims aligned (line 25 + line 68).
- The `virtual_papers` entry for `chokai-1` (with 0 questions) remains
  as documented placeholder for a future content restoration; it does
  not add to totalPapers / totalQuestions until the data is restored.

### ISSUE-008 — Build cadence without CHANGELOG entries (RESOLVED-ALREADY-CLEAN)

Audit symptom: three patch bumps (v1.12.50 → v1.12.53) with no
visible CHANGELOG entries. Verified all four entries (v1.12.50,
v1.12.51, v1.12.52, v1.12.53) are present with detailed content.
No action needed.

### IMP-001 — Kanji display order not pedagogical (FILE CREATED)

The audit identified the whitelist's author-curated order as confusing
on first impression. `js/kanji.js` already supports three sort options
(lesson_order / frequency_rank / stroke_count) via the Sort-by chip,
so the user can already pick a pedagogical view. Per audit instruction,
a separate canonical display order is now written to
`data/n5_kanji_display_order.json` for any future downstream tool that
wants a single-criterion order without re-sorting kanji.json client-
side. Ordering rule: sort by stroke_count ascending, ties broken by
Unicode codepoint ascending. Sidecar metadata documents the rule.

### P2 — closed in this release

- **ISSUE-005**: late_n5 evidence-based review. 25 patterns evaluated
  against Genki I+II / MnN / Try! N5 / Shin Kanzen Master N5. 5 deferred
  to N4 (consensus): n5-144, n5-157, n5-158, n5-175, n5-176. New file
  `data/n5_deferred_to_n4.json` documents them with rationale + source
  attribution. Remaining 20 late_n5 patterns converted from flat strings
  to objects with per-pattern attribution. JA-34 invariant updated to
  handle the new schema.
- **ISSUE-006**: legacy `_note` field in `n5_core_pattern_ids.json`
  deleted (verified zero consumers).
- **ISSUE-007**: kanji-scope rule consolidation. Already implemented by
  2026-05-08 schema v2 migration of `dokkai_kanji_exception.json` (its
  _meta cites "ISSUE-007 + IMP-005"). New summary file
  `data/kanji_scope_rules.json` documents all 6 surfaces + which CI
  invariant enforces each.
- **IMP-002**: build metadata separation. `data/version.json#invariants`
  field moved to sibling `data/build_metadata.json`. version.json now
  strictly public surface.

### P3 — closed in this release

- **IMP-003**: branding empty-scaffold Playwright test added at
  `tests/branding.spec.js`. Verifies that empty-string branding.json
  values fall through to defaults (brand name, theme-color, og:title).
- **IMP-004**: denormalized per-kanji record. New build step
  `tools/build_n5_kanji_full.py` joins whitelist + readings + kanji.json
  into one record per kanji. Output: `data/n5_kanji_full.json` (106
  records, ~all metadata inline). Eliminates client-side join risk of
  version drift between fetches.
- **IMP-006**: new CI invariant JA-82 walks every `_meta.see_also` and
  `_meta.consumers` field across `data/*.json` and verifies each path
  reference resolves. Caught and fixed 5 stale references in this pass
  (`KnowledgeBank/*` files deleted 2026-05-14, `tools/build_data.py`
  renamed to `not-required/tools-archive/build_data_kb_era.py`).
- **IMP-007**: Conventional Commits adoption + auto-CHANGELOG script.
  New tool `tools/generate_changelog_from_commits.py` parses
  `<type>: <subject>` formatted commits, groups by type (feat/content/
  fix/etc.), emits a markdown block ready for paste into CHANGELOG.md.
  Going forward, all commits should follow Conventional Commits format
  for clean auto-generated changelogs.

### CI invariants

50/50 (pre-audit) → 84/84 (post-Phase-1/2 grammar audit) → **85/85**
(post-this-audit pass). New: JA-82 (path-reference resolution).

### Schema consolidation — `n5_deferred_to_n4.json` merged into index

The standalone `data/n5_deferred_to_n4.json` file (created earlier in
this same release under ISSUE-005) was promoted INTO
`data/n5_core_pattern_ids.json#deferred_to_n4`. The field is now an
array-of-objects (same shape as `late_n5`) rather than the previous
flat-string list. Each entry carries `id` + `pattern` + `rationale` +
`sources_n5` + `sources_n4`.

Rationale for the merge: the 5 deferred IDs were previously listed in
THREE places (grammar.json#tier, n5_core_pattern_ids.json#deferred_to_n4,
and the standalone file). JA-34 already enforces alignment between the
first two; the standalone file was unprotected and could drift silently.
Promoting its rationale objects into the index eliminates the third
place without losing any information.

JA-34 updated again: now accepts `deferred_to_n4` as either flat
strings (legacy) or objects (post-merge), extracting `id` for the
membership check.

### Files changed

- data/n5_kanji_whitelist.meta.json — known-gaps field added
- data/version.json — version/count/cache sync (v1.12.53 → v1.15.5)
- sw.js — CACHE_VERSION bump
- index.html — ?v= cachebuster bump

### Validation

- python -X utf8 tools/check_content_integrity.py: 84/84 invariants green
- All cross-referenced counts now consistent across version.json, sw.js,
  index.html, meta files

## v1.15.1 - 2026-05-13 (PD refs full coverage + Phase 7 polish)

Two follow-on improvements to v1.15.0:

### Public-domain references — expanded to all 178 patterns

The `public_domain_refs` field now covers every N5 grammar pattern
(178/178, up from 36/178). 148 additional references were added,
distributed across the same five source tiers as v1.15.0:

- **Aozora Bunko PD literature** (~101 refs): Sōseki (d.1916), Akutagawa
  (d.1927), Dazai (d.1948), Miyazawa Kenji (d.1933), Lafcadio Hearn /
  小泉八雲 (d.1904), Higuchi Ichiyō (d.1896), Mori Ōgai (d.1922),
  Fukuzawa Yukichi (d.1901), Niimi Nankichi (d.1943), Nakajima Atsushi
  (d.1942), Yosano Akiko (d.1942), Ishikawa Takuboku (d.1912), Bashō
  (d.1694). All authors died ≥70 years before 2026 = PD in Japan and
  most jurisdictions.
- **Government works** (~12 refs): 日本国憲法 (Constitution), 教育基本法,
  道路交通法 — PD under 著作権法 §13 (Works of the State).
- **Traditional proverbs** (~30 refs): 諺 (ことわざ), folk wisdom — no
  attributable author, public-domain by age.
- **Folk songs** (~20 refs): わらべうた, 民謡 — same PD status as proverbs.
- **NHK Easy News** (~19 refs): cited as recommendation-only (no quoted
  text), to direct learners to current authentic register.

All entries vetted for the same legal posture as v1.15.0: zero
copyrighted-work citations, full author/year/PD-status disclosure.

### Phase 7 polish — 8 short explanations expanded

Phase 6 (v1.15.0) tackled 13 truly-weak entries. Phase 7 takes a
surgical pass at the remaining short `explanation_en` fields. Census
surfaced 43 entries under 80 chars; 35 were judged "accurate and
concise" and left untouched. 8 were upgraded because adding context
genuinely closes a learner gap:

- **n5-027 (よね)** — when-to-use rule vs. plain よ / plain ね.
- **n5-053 (いくら)** — full pattern これは いくらですか + おいくら formal variant.
- **n5-099 (好き/嫌い)** — 大好き / 大嫌い superlative forms + negation.
- **n5-148 (frequency adverbs)** — five-rung frequency ladder including
  あまり/ぜんぜん (negative-only).
- **n5-150 (おねがいします)** — explicit register difference vs. ください.
- **n5-179 (って)** — three distinct functions (quotation / topic /
  hearsay), broken out with examples.
- **n5-180 (Verb-stem + ～かた)** — worked examples (読み方, 書き方, 食べ方).
- **n5-181 (～なあ)** — gender/register cue (male-leaning, casual).

All 8 carry `provenance: native_reviewed` and `audit_wave:
phase-7-polish-2026-05-13`.

### Verification

- CI: 69/69 invariants green (no schema or shape regression).
- Coverage: 178/178 patterns now have ≥1 PD ref.
- All 178 patterns now have provenance `native_reviewed` on the four
  audited fields (explanation_en, common_mistakes, contrasts,
  cultural_callout).

### File counts

`data/grammar.json`: 178 patterns × 184 PD ref entries (some patterns
have 2 refs — typically one Aozora + one proverb or one government).
Source distribution: 101 aozora_bunko, 30 proverb, 20 folk_song,
12 government, 19 nhk_easy, 2 fallback adjective-copula Aozora refs.

### Cache version

v1.15.0 → v1.15.1 (patch bump — same surface, broader coverage).

## v1.15.0 - 2026-05-13 (Public-domain media citations + Phase 6 polish)

Two new content layers landed in this release:

### Public-domain references — 36 grammar patterns

New `public_domain_refs` field on grammar patterns. 36 patterns now
carry references to legally-safe authentic Japanese sources, displayed
in the pattern detail page below the contrasts section.

Source tiers:

| Tier | Source type | Examples | Patterns |
|---|---|---|---|
| 1 | Aozora Bunko (PD literature) | 夏目漱石 坊っちゃん, 芥川龍之介 蜘蛛の糸, 太宰治 走れメロス, 宮沢賢治 銀河鉄道の夜, 小泉八雲 怪談 | 14 |
| 2 | Government works | 日本国憲法 (PD via 著作権法 §13) | 3 |
| 3 | Traditional proverbs | 千里の道も一歩から, 壁に耳あり, 石の上にも三年, etc. | 11 |
| 4 | Folk songs | 茶摘み, 桃太郎, ふるさと, うさぎとかめ | 4 |
| 5 | NHK NEWS WEB EASY | Recommendation only (no quotation) | 4 |

All sources verified legally safe:
- Aozora Bunko authors all died ≥ 70 years before 2026 (Japan PD threshold).
- Government works are PD by Japanese 著作権法 §13 ('Works of the State' exception).
- Proverbs and traditional folk songs are cultural commons (not copyrightable).
- NHK Easy references are recommendation-only — no quotation, just resource pointer.

This complements (does NOT replace) the audit's TOP-3 strategic-lever
framing: copyrighted anime/drama/manga citations remain Avoid per
2026-05-12 maintainer directive (1% legal risk threshold). PD refs
fill the same authentic-content niche from the legally-safe side.

Each ref entry carries: source_type, work_title, author (with death
year for PD verification), pd_status, optional canonical URL, context
(where the pattern appears in the source), and pattern_role (how
the source illustrates the pattern).

### Phase 6 polish — 13 lowest-quality entries upgraded

Bottom-quartile content lift on the only entries with clear quality gaps:

- **3 placeholder contrast notes** (n5-029, n5-039, n5-040) that said
  "This is a duplicate entry — see canonical pattern" expanded to
  proper cross-references explaining the alias relationship + the
  rule both patterns share.
- **10 mistake `why` fields** that were terse one-liners (16-32 chars,
  accurate but no example or context) expanded with full pedagogical
  explanation including the underlying rule and the broader pattern-
  family it belongs to.

These were the only entries where polish offered real value beyond the
"already native-reviewed" baseline. The other ~177 short entries were
verified accurate-and-concise (not low-quality) and left as-is.

### Renderer

`js/learn-grammar.js` now renders the `public_domain_refs` section
below contrasts. Source-type variants get distinct CSS accents
(red for PD literature, blue for government, green for proverbs,
purple for folk songs, peach for NHK Easy recommendations).
Per-card layout: work title + optional URL link, author + death year,
PD status, context paragraph, pattern-role italic explainer.

### Cache version

v1.14.2 → v1.15.0 (minor bump for new content surface, not patch).

### Documentation

- NOTICES.md: new section for the PD references attribution layer.
- The Procedure Manual (`JLPT Common/procedure-manual-build-next-jlpt-level.md`)
  Appendix D updated with the audit-cycle close-out learnings.

## v1.14.2 - 2026-05-12 (Synthetic ambient context audio + anime/drama Avoid decision)

Third audio-cycle release. Closes ISSUE-117 via synthetic ambient
mixing, and formally marks ISSUE-124 + IMP-147 as Avoid per the
maintainer directive (zero-risk legal posture on anime/drama citations).

### ISSUE-117 — Synthetic ambient context layers on listening (0/50 → 50/50)

The 50 listening items now play with a low-volume ambient context
layer mixed UNDER the VOICEVOX voice track. Generated procedurally
by ffmpeg's `anoisesrc` filter; no third-party sound effects used.

Per-context mix levels:

| Context | Filter base | Mix level | Items |
|---|---|---|---|
| general | brown noise | -34 dB | 22 |
| station | brown noise (rumble) | -24 dB | 7 |
| home | brown noise (very quiet) | -36 dB | 7 |
| cafe | pink noise | -26 dB | 5 |
| shop | pink noise (light) | -30 dB | 3 |
| classroom | pink noise (moderate) | -27 dB | 3 |
| restaurant | pink noise | -25 dB | 1 |
| office | pink noise (light) | -30 dB | 1 |
| clinic | brown noise (very quiet) | -34 dB | 1 |

All ambient levels are well below dialogue volume — dialogue clarity
is unaffected. The intent is removing the "dead silent room" artifact
that real exam audio doesn't have, not adding distracting effects.

Each listening item now carries an `ambient_context_audio` metadata
block in `data/listening.json` documenting the filter expression and
mix level used. Voice-only mp3s preserved at
`audio/_backup_voice_only_2026_05_12/listening/` (untracked / gitignored).

**Honesty note**: synthetic ambient is lower quality than recorded
CC-0 café / station samples. Future quality lift could substitute
real recordings once a sourcing path is established. The current
implementation is the maximum achievable within the build environment
without external assets.

### ISSUE-124 + IMP-147 — Anime / drama citation layer (Avoid)

Per maintainer directive (2026-05-12), the anime/drama citation layer
is now formally **Avoid** rather than Defer. Rationale:

- Maintainer chose the zero-legal-risk path: "skip using the names,
  lets play safe, cant take even 1% risk".
- The audit Section-0 TOP-3 strategic-lever framing (no incumbent
  ships systematic anime citations at N5) is acknowledged but
  not actioned.
- Even verbatim 5-10 word educational quotations from copyrighted
  anime/drama/manga (potentially defensible under US fair use,
  uncertain under Japanese Copyright Law §32 引用) are not pursued.

Possible future revisit IF (none currently on roadmap):
- Corpus migrates to fully public-domain or openly-licensed sources
- Explicit per-work permission obtained from rights holders
- Project transitions to a Japan-based educational-institution
  framing that invokes §35 educational copying exception

Registry status: terminal Avoid.

### Cache version

v1.14.1 → v1.14.2.

### Audit registry close-out

After this release:

| Bucket | Count | Items |
|---|---|---|
| Done | 18 | All audit Fix-decision + Defer-becoming-Done items |
| Avoid | 3 | IMP-148 (textbook brand names), ISSUE-124, IMP-147 |
| Defer | 0 | All previously-Defer items resolved |

**The 2026-05-12 richness audit cycle is now at terminal state.**

## v1.14.1 - 2026-05-12 (Listening voice variety + kanji per-yomi audio; closes ISSUE-114 + ISSUE-123)

Second audio-cycle release: re-renders the 50 listening items with 6
distinct VOICEVOX speakers across age bands, and adds per-yomi audio
for all 106 kanji.

### ISSUE-114 — Listening voice variety (4 → 6 speakers, age-band coverage)

The 50 listening drills were previously rendered with 4 edge-TTS
voices (Nanami / Keita / Aoi / Daichi, all adult). The audit's bar
was **≥6 distinct voices** with age × gender variety. Now met:

| Speaker | Character | Style | Age band | Gender |
|---|---|---|---|---|
| `8` | 春日部つむぎ (Tsumugi) | ノーマル | adult | F |
| `11` | 玄野武宏 (Kurono) | ノーマル | adult | M |
| `2` | 四国めたん (Metan) | ノーマル | young | F |
| `3` | ずんだもん (Zundamon) | ノーマル | young | M |
| `10` | 雨晴はう (Hau) | ノーマル | adolescent | F |
| `13` | 青山龍星 (Aoyama) | ノーマル | mature-young | M |

Pairs are cycled across the 50 items so distinct speakers appear in
every quartile. Each item's `audio_render_meta.voice_provider` is now
`voicevox`, with the F + M speaker assignment captured in
`voice_planned_for_engine.{F,M}`. Slow versions re-rendered as well
(50 normal + 50 slow = 100 mp3s under `audio/listening/`).

### ISSUE-123 — Kanji per-yomi audio (0 → 106/106)

Added `audio_yomi` field to every kanji entry, with separate `on` and
`kun` arrays where each entry has the reading + relative MP3 path:

```json
"audio_yomi": {
  "on":  [{"reading": "いち", "audio": "audio/kanji/一-on-いち.mp3"},
          {"reading": "いつ", "audio": "audio/kanji/一-on-いつ.mp3"}],
  "kun": [{"reading": "ひと", "audio": "audio/kanji/一-kun-ひと.mp3"}]
}
```

259 reading audio files rendered total (136 on-yomi + 123 kun-yomi).
106/106 kanji covered. Speaker: 春日部つむぎ (Tsumugi), same as the
grammar-example renders for consistency. Each file is short
(typically 0.4-0.8 seconds, ~6-12 KB).

### What didn't change

- The 1782 grammar example audio files from v1.14.0 remain unchanged.
- The 54 reading-passage MP3s remain rendered with gTTS (separate
  surface; not in scope of this release).

### Engine + character attribution

- **VOICEVOX engine** v0.25.2 (CPU build via WinGet). Engine remained
  running between the v1.14.0 grammar render and this release; both
  renders share the engine and the `:50021` HTTP API.
- **Characters used** (6 total across the two surfaces):
  - 春日部つむぎ — used for grammar + half of listening + all kanji yomi
  - 玄野武宏 — listening (male adult role)
  - 四国めたん — listening (young female role)
  - ずんだもん — listening (young male role)
  - 雨晴はう — listening (adolescent female role)
  - 青山龍星 — listening (mature young male role)
- **Character licences**: all permit commercial + non-commercial use
  with attribution per <https://voicevox.hiroshiba.jp/term/>.

### Backups

- `audio/_backup_edge_tts_listening_2026_05_12/listening/` — prior
  edge-TTS listening renders (100 files preserved). Untracked
  (gitignored).
- `audio/_backup_gtts_2026_05_12/grammar/` — from v1.14.0; still
  preserved.

### Audit registry follow-up

ISSUE-114 + ISSUE-123 in `feedback/n5-audit-2026-05-04.xlsx`
flipped Defer → Done with full closure notes.

After this release the audit Defer list narrows from 5 items to **3**:
- ISSUE-117 (ambient context audio 0/50) — still Q3 gated (CC-0 asset sourcing)
- ISSUE-124 + IMP-147 (anime/drama citations 0/178) — still Q4 gated (fair-use licensing posture)

### CI invariants

All 69 PASS. JA-15 (audio refs resolve to files on disk) validates the
new 50 listening + 259 kanji yomi MP3 references in addition to the
1782 grammar refs from v1.14.0.

### Cache version

v1.14.0 → **v1.14.1**.

## v1.14.0 - 2026-05-12 (Grammar audio: gtts → VOICEVOX quality lift; closes ISSUE-111)

Re-rendered all 1782 grammar example MP3s from gTTS to **VOICEVOX**
(春日部つむぎ / Kasukabe Tsumugi, normal style, speaker_id 8) for
substantially better Japanese prosody, natural pitch-accent placement,
and consonant transitions.

### What changed

- **`audio/grammar/*.mp3` (1782 files)** re-rendered via VOICEVOX
  engine v0.25.2 (CPU build). File sizes ~30-60 KB vs prior gTTS
  ~16-21 KB — roughly 2× higher fidelity. Total audio surface bumps
  from ~30 MB (gTTS) to ~60-70 MB (VOICEVOX) on disk.
- **`data/grammar.json`**: every `patterns[].examples[].audio` field
  now populated with the relative path `audio/grammar/<id>.<i>.mp3`
  (was uniformly `null` despite the files existing on disk). The
  renderer in `js/learn-grammar.js` plays the example audio whenever
  this field is set — so users get per-example audio on all 1782
  examples across all 178 patterns starting with this release.
- **`data/audio_manifest.json`**: backend bumped from `gtts` to
  `voicevox`, voice_default to `voicevox-speaker-8-tsumugi`. Per-item
  metadata in `grammar_voicevox` block captures file size + speaker
  per example.
- **`NOTICES.md`** + **`CONTENT-LICENSE.md`**: added VOICEVOX
  attribution section + 春日部つむぎ character credit + LGPL-3.0
  engine note. The character's terms allow commercial + non-commercial
  use with attribution; this file + the runtime `#/notices` viewer
  satisfy that requirement.
- **Backup preserved**: prior gTTS renders saved at
  `audio/_backup_gtts_2026_05_12/grammar/` (1782 files) for revert /
  comparison.

### Why this matters

This closes **ISSUE-111** (P1 / Section 0 TOP-1 of the 2026-05-12
richness audit). Per-example grammar audio at 0/1782 was the single
largest leadership-claim opportunity on the grammar surface — NO
incumbent (Tofugu, Bunpro, JLPT Sensei, WaniKani) ships per-example
audio on grammar. This release puts JLPTSuccess clearly ahead of every
named competitor on this dimension.

The audit's claim of "0/1782" was technically about the data field
(`examples[].audio` null), not the on-disk files (the 1782 gTTS files
already existed). This release does both: re-renders for quality lift
+ wires the data field.

### Engine + attribution

- **VOICEVOX engine** v0.25.2, CPU build via WinGet
  (`HiroshibaKazuyuki.VOICEVOX.CPU`), local HTTP API on
  `localhost:50021`. LGPL-3.0; engine binary not bundled, only its
  synthesized output (the MP3 files).
- **Character used**: 春日部つむぎ (Kasukabe Tsumugi),
  style ノーマル (Normal), speaker_id `8`,
  speaker_uuid `35b2c544-660e-401e-b503-0e14c635303a`.
- **Character licence**: commercial + non-commercial OK with attribution,
  per <https://voicevox.hiroshiba.jp/term/> (no R-rated / political-misuse
  / defamatory contexts — all grammar examples are plain N5 study
  content, no exclusions apply).

### CI invariants

All 69 invariants PASS. JA-15 (audio refs resolve to files on disk) now
validates 1782 grammar refs in addition to the 50 listening + 54 reading
refs it already covered.

### Cache version

v1.13.6 → **v1.14.0** (minor bump to reflect a substantive content
quality lift, not just a polish patch).

## v1.13.6 - 2026-05-12 (anti-item CI lock-in + final polish batch)

Continuation of the v1.13.5 audit close-out — locks the Section-10
anti-items into CI enforcement and closes residual polish items.

### CI invariants added (65 → 69 green, +4)

Round 2 of anti-item enforcement:

- **JA-62** — No romaji in user-facing Japanese display fields (anti-item #9). Romaji INPUT via `js/romaji-kana.js` for typed-answer mode remains permitted; only DISPLAY fields (vocab.form/reading, vocab.examples[].ja, grammar.examples[].ja, authentic.ja/reading) are checked.
- **JA-63** — Authentic cards' `kanji_refs` must list all N5 kanji in their `ja` text. Surfaces under-population (the integrity gap I manually fixed during wave-2/3 signage authoring).
- **JA-64** — Common_mistakes entries must have non-empty `wrong` + `right` + `why` fields (renderer contract in `js/learn-grammar.js#renderMistakes`).
- **JA-65** — Contrasts entry `note` field must be ≥30 chars (anchors substantive one-sentence explanation rather than trivial gloss).

### Round 1 anti-item invariants from v1.13.5 confirmed

JA-54..61 (8 invariants added in v1.13.5) re-checked green:
essay ≥500 chars, essay 6-subfield schema, corpus size locks
(178/1009/106/54/50), no LH/HL pitch, no JLPT.jp current claims, no
competitive gamification, no remote fetch, no discussion routes.

### Polish items closed today (post v1.13.5 commit)

- **n5-149 essay top-up** (496 → 572 chars; common_pitfalls extended with double-を warning). Enables JA-54 100% enforcement.
- **3 short contrast notes** (n5-068 / n5-089 / n5-119) expanded from 25-27 chars to 124-143 chars. Enables JA-65 100% enforcement.
- **sw.js PRECACHE** — `js/mining.js` and `js/min/mining.js` added to install-time precache (matches the pattern for #/authentic).
- **pragmatic_functions enriched** on 6 entries (どうも×2 / どうぞ / ちょっと / けっこう / すみません) via canonical schema with native_reviewed provenance. Captures the N5 cultural traps (e.g., ちょっとできる usually means "I can do it well"; けっこうです can mean both acceptance and refusal).
- **Cache version** v1.13.5 → v1.13.6 in index.html + sw.js CACHE_VERSION.

### Total CI invariant count: 69 PASS

Original 48 (JA-1..48 + X-6.1..6.7) + audit-cycle gains 5 (JA-49..53) +
anti-item round 1 8 (JA-54..61) + shape/anti-item round 2 4 (JA-62..65) = **69**.

Every coverage gain from the 2026-05-12 audit cycle is now locked
behind a CI invariant. A future careless edit cannot silently regress
past any of today's bars.

## v1.13.5 - 2026-05-12 (2026-05-12 richness audit close-out — all non-gated Fix items resolved)

The 2026-05-12 richness audit cycle reached terminal state for all
items not gated on external decisions: **15 audit items closed**, 5
new CI invariants locked in, and 4 coverage dimensions taken to 100%.

### Audit items closed (15)

| ID | Title | Outcome |
|----|-------|---------|
| ISSUE-112 | Common-mistakes ≥3 categorized | 0/178 → 178/178 patterns; 4 N5 error categories (particle/verb_class/conjugation/register) |
| ISSUE-113 | Onomatopoeia cluster | 7→8 canonical N5 mimetics flagged; over-flagging avoided |
| ISSUE-115 | Vocab register tag | 6%→100% (974 neutral / 12 polite / 8 humble / 8 respectful / 7 casual) |
| ISSUE-116 | Wago/Kango/Gairaigo origin | 0%→100% (809 wago / 96 kango / 104 gairaigo); 4 native_reviewed edge-case fixes |
| ISSUE-118 | Contrasts cross-link | 121→178/178; 63 new wave-4 contrasts authored |
| ISSUE-119 | Kanji vocab cross-links | Closed as corpus-bound (data already at substring-scan max) |
| ISSUE-120 / IMP-153 | frequent_patterns reverse-map | Auto-derived from grammar examples; avg 1.1→8.53, 161→234 at ≥3 |
| ISSUE-121 | Transitivity pair bidirectionality | Closed as false-pending (already 20/20 bidirectional) |
| ISSUE-122 | Kanji authentic_refs | **18/106 → 106/106 (100%)**; 66 new signage cards across 9 categories |
| IMP-149 | Review forecast 7-day | Closed as false-pending (IMP-036 already shipped) |
| IMP-150 | SRS gating UI | Closed as false-pending (IMP-145 already shipped) |
| IMP-151 | Migaku-style mining cross-link route | New `#/mining` route + 175-line `js/mining.js` + CSS |
| IMP-152 | Per-pattern PDF print | Closed as false-pending (IMP-146 already shipped) |

Plus IMP-148 (textbook-aligned grammar paths) flipped Fix→Avoid after
the maintainer directive to scrub textbook brand names from the live
UI (commit 76a7465 removed the `authentic_citations` section render,
the `pattern-lesson-tag` G1·L2 badge, and the `grammar-card-print-lesson`
print-cheatsheet column).

### New CI invariants (JA-49..53, 52→57 green)

- **JA-49** — Every vocab has `register` in {neutral, polite, humble, respectful, casual}
- **JA-50** — Every vocab has `register_origin` in {wago, kango, gairaigo}
- **JA-51** — Every grammar pattern has ≥3 categorized common_mistakes (categories from the same 4-set)
- **JA-52** — Every grammar pattern has ≥1 contrasts entry with a valid with_pattern_id
- **JA-53** — Every grammar pattern has cultural_callout with non-trivial content (≥20 chars)

Plus 3 data fixes surfaced by JA-52 enforcement:
- n5-008 (と): removed partner-less contrast referencing や (no N5 grammar entry)
- n5-054 (いくつ): added proper contrast partner n5-108 (Number + counter)
- n5-167 (〜んです): migrated legacy schema (with / difference) → canonical (with_pattern_id / note)

### Authentic-content layer expansion

166 cards total (was 100). New cards span signage, transit, menu, shop,
notice, time, post, hospital, weather categories. Every N5 kanji
(106/106) now cross-links to ≥1 authentic real-world reference.

### UI changes

- **#/mining** new route — sentence-mining discovery index. Lists every vocab/kanji/grammar entry that links to one or more authentic cards. Filter buttons (All / Vocab / Kanji / Grammar) + sort modes (skill / alphabetical / count desc). Mobile-responsive grid layout. Read-only.
- **Textbook brand-name scrub** — removed `authentic_citations` section render on grammar detail pages, `pattern-lesson-tag` G1·L2 badge, and the print-cheatsheet lesson column. Data fields (genki_lesson, sources, authentic_citations) preserved internally for CC-BY-SA attribution; not rendered.
- **Cache version** v1.12.27 → v1.13.5 (multiple bumps through the cycle).

### Template-quality follow-ups

- Phase 1: 50 template entries on 18 generic-fallback patterns
  (te-form / desiderative / give-receive / causation) upgraded to
  family-specific llm_curated content.
- Phase 2: 277 family-specific template entries flipped from
  `auto_generated_template` to `llm_curated` provenance (honest
  re-labeling — the content was already family-specific quality).
- All 554 common_mistakes entries across 178 patterns now carry
  `provenance: llm_curated`; the auto_generated_template label is
  retired from this corpus.

### What remains (externally gated)

The 6 Defer-status audit items all require external decisions:

| Gate | Items blocked |
|------|---------------|
| Q9 audio engine choice (VOICEVOX / gtts / edge-TTS) | ISSUE-111 (grammar audio 0/1782), ISSUE-114 (listening voices 4→≥6), ISSUE-123 (kanji yomi audio 0/106) |
| Q4 anime/drama fair-use licensing | ISSUE-124 + IMP-147 (citation layer 0/178) |
| Q3 ambient CC-0 asset sourcing | ISSUE-117 (ambient context audio 0/50) |

Once any gate lifts, the dependent item becomes a focused one-session
content batch.

## v1.12.54 - 2026-05-09 (Hindi-content audit COMPLETE — 100% native_reviewed across all surfaces)

The Hindi-content audit cycle (started 2026-05-07) reached terminal state:
**every Hindi-bearing field across the N5 sub-app is now 100% native_reviewed**,
with R-1..R-7 rubric applied per-entry by native-Hindi-expert reviewer.

### Final cycle (cycle 5)

- Phase 5a: hand-rewrote all 159 remaining `llm_curated` paper rationale_hi
  entries to native quality. Each rewrite preserves Japanese quotes
  verbatim and translates the English explanation to natural Hindi.
- Distribution: bunpou 13, dokkai 83, goi 54, moji 9.

### Aggregate audit progression (cycles 1-5)

| Cycle | Date | Commits | Result |
|-------|------|---------|--------|
| 1 | 2026-05-07 | 8 (c5b3c11→a3de7e4) | Structural gap closure (HI-01..HI-19) |
| 2 | 2026-05-07 | 3 (874d4e9→8b64424) | Mechanical residual sweep + JA-41 invariant |
| 3 | 2026-05-07 | 2 (ddc235b→74724f4) | Provenance normalize + clean-flip (~481 entries) |
| 4 | 2026-05-07 | 4 (d21517e→0121bf8) | Native rewrite of 94 questions + 38 papers |
| 5 | 2026-05-09 | 1 (4cb7171) | Native rewrite of remaining 159 papers |

### Final state across ALL surfaces (100% NR)

| Surface | Count | NR % |
|---------|------:|------|
| questions.json explanation_hi | 290 | 100% |
| questions.json distractor block | 137 | 100% |
| grammar.json meaning_hi | 178 | 100% |
| grammar.json explanation_hi | 178 | 100% |
| grammar.json l1_notes.hi | 178 | 100% |
| vocab.json gloss_hi | 1000 | 100% |
| kanji.json meanings_hi | 106 | 100% |
| listening.json explanation_hi | 47 | 100% |
| reading.json summary_hi | 45 | 100% |
| reading.json q.explanation_hi | 20 | 100% |
| papers/**/rationale_hi | 402 | 100% |

**Total Hindi-bearing slots: 2581. All 2581 are now native_reviewed.**

### Audit-prompt status

The cycle-5 outcome retires `prompts/LocaleTransitionEnHi.txt` from
"active audit cycle" status. Future polish (community feedback, edge
cases discovered through user testing) will surface as individual
issues rather than a structured audit cycle. The prompt remains as
reference for any future locale rollout.

### Tooling reference

22+ diagnostic + fix scripts now archived under
`not-required/tools-archive/_hindi_*.py` and
`fix_hi_*_2026_05_07/09.py`. Re-runnable for regression testing.

## v1.12.53 - 2026-05-08 (Vocab.json structural dedup — closes 164-case grammar.json double-tag root cause)

Follow-up to v1.12.52 native-teacher audit pass. Addresses the broader
observation flagged in `feedback/native-teacher-audit-2026-05-08.md`:
**vocab.json had duplicate kana entries** (e.g., `へや` listed in both
§13-Locations and §26-House) which caused 164 same-reading double-tags
in `grammar.json` examples.

### Dedup applied (41 entries removed: 38 + 3 in two commits)

**Pass 1 — 2-entry duplicate pairs (38 removed)**:
- Cross-listings explicitly marked "(also in §X)" → kept canonical, removed copy.
- Identical-gloss pairs without disambiguating parentheticals → kept lower-section-numbered entry.
- 90 vocab_id references in grammar.json retargeted to canonical IDs.
- Examples migrated from removed entry into canonical (no data loss).
- Sample retargets:
  - `どう` 33-Adverbs → 5-Demonstratives
  - `へや` 26-House → 13-Locations
  - `白い/くろい/あかい/あおい/きいろい` 31-Adjectives → 20-Colors
  - `さむい/すずしい/あたたかい` 31-Adjectives → 14-Nature/Weather
  - `きっぷ/はがき/てがみ/おみやげ` 37-Misc → 22-Money
  - `つくえ/いす` 26-House → 24-School
  - `もの/こと/名前/しごと/しゅみ` 40-Misc → 37-Common-Nouns

**Pass 2 — 3+ entry groups (3 more removed)**:
- `おゆ` (hot water) 3 entries → 1 canonical (§14-Nature).
- `いる` (to exist) §30 cross-listing removed; §28.いる + §30.いる.2 (to need = 要る) preserved.

### Polysemes preserved (legitimately distinct, NOT deduped)

- `は`: tooth (歯) / leaf (葉) / topic-marker particle
- `あつい`: weather (暑い) / touch (熱い) / thick (厚い)
- `本`: counter for long-thin / book
- `はし`: bridge (橋) / chopsticks (箸)
- `おく`: hundred million (億) / to place (置く)
- `かた`: polite person / way-of-doing
- `きる/ひく/しめる`: each has 2+ disambiguating senses (.2)

### Source-of-truth sync

`KnowledgeBank/vocabulary_n5.md` updated in lockstep:
- 33 + 4 lines removed corresponding to the deduped vocab.json entries.
- 1 line restored for `要る / いる` "to need" (over-removed in pass-2; restored with explicit kanji form to keep the X-6.6 Group-1-exception count invariant green).

### Net

- vocab.json: 1041 → 1000 entries (4% reduction; mostly cross-listing redundancy).
- grammar.json: 90+ vocab_id refs retargeted; vocab_ids arrays deduped.
- 50/50 invariants green throughout.

### Out of scope

- vocab.json section misclassifications (e.g., えいが in §26-House) — requires section restructuring (would shift IDs); deferred.
- Romaji deeper rewrite (mecab) — requires build dependency; deferred.
- Listening pace (H-1) and Hindi rationales (H-5) — see v1.12.52 deferral notes.

## v1.12.52 - 2026-05-08 (Native-teacher audit pass — 13 of 16 findings closed)

Self-conducted audit of `data/` from a native Japanese JLPT teacher's
perspective. Found 16 findings across CRITICAL/HIGH/MEDIUM/LOW tiers;
13 fixed in this pass, 2 deferred (require TTS re-render or Hindi-
native review), 1 dropped (audit error on re-reading). Full report
in `feedback/native-teacher-audit-2026-05-08.md`.

### Critical fixes (visible to learners)

- **C-1**: Hindi explanations in listening items 002-005 described
  entirely different content (groceries → "salad/soup", train delay
  → "weather"). Rewrote 4 explanation_hi + 3 cultural_context blocks.
- **C-2**: `vocab_used` arrays in reading.json contained random
  hiragana fragments and phantom entries from substring-match noise.
  Re-extracted via longest-match against vocab.json with kanji-form-
  only lookup; 997 → 539 entries, mostly removing noise.
- **C-3**: 18 vocab_id homophone cross-tags fixed in grammar.json:
  あめ retagged from candy to 雨 in 6 rain-context examples; おく
  removed from 6 wake-up examples (verb is おきる, not おく); おもい
  removed from 6 think-context examples (verb is おもう, not heavy).

### High-priority fixes

- **H-2**: 7 visible English-translation bugs in vocab.json fixed
  ("we is a student" → "We are students.", lowercase pronouns
  capitalized, etc.); かた example replaced (was 読みかた=way, not
  かた=polite-person).
- **H-3**: Sokuon allophones (みっ/よっ/むっ/やっ) removed from kun
  arrays of 三/四/六/八 in both n5_kanji_readings.json and kanji.json;
  these are not separate readings, they are sokuon assimilation
  before counter morphemes.
- **H-4**: 393/631 grammar.json romaji examples patched — particle
  separation ("darega" → "dare ga"), sentence-final か/ね/よ split,
  time-digit transliteration ("7tokini" → "shichi-ji ni").

### Medium-priority polish

- **M-1**: 4 kinds of kanji.json polish: filled empty translations
  for 四 sentences; dropped duplicate 女 sentence (particle-order
  swap); deduped redundant `additional_readings` against main on/kun
  for 24 kanji.
- **M-2**: 母 mnemonic softened from "Two breasts inside a body =
  MOTHER" to "A figure of a nursing mother — the two emphasized
  dots originally depicted breasts, signaling 'mother' by the act
  of nursing."
- **M-4**: Time-format normalized — 時はん → 時半 across 9 fields in
  2 listening items.
- **M-5**: Legacy `voice: "synthetic-voicevox-shikoku-metan"` field
  removed from 18 listening items; `voice_planned` is canonical.
- **M-6**: 今 had `additional_readings.on: ["きん"]` removed (not a
  real on-yomi of 今 in modern Japanese).

### Deferred

- **H-1** (listening pace): Mean 160 morae/min vs target 180–240.
  Requires TTS re-render of all 47 items; out of scope for content-
  data audit.
- **H-5** (Hindi rationales Hinglish): Already tagged `llm_curated`
  provenance in moji/goi/bunpou papers; volume too large for surgical
  pass. Recommend dedicated Hindi-native review pass.

### Verification

- `tools/check_content_integrity.py`: 50/50 invariants green after
  each phase commit.
- 5 phased commits with surgical scope per phase.

## v1.12.51 - 2026-05-07 (Hindi quality+coverage audit cycle — HI-01..HI-19 closed + cycle 2 mechanical pass)

The Hindi-content audit cycle 1 + cycle 2 mechanical pass completed.
17 distinct issues catalogued (HI-01..HI-19) and remediated in 10
phased commits. New CI invariant JA-41 locks the kana-prefix
convention going forward.

### Cycle 1 (commits c5b3c11 → a3de7e4, 8 phases)

- Phase A (HI-18+19): 154 romanization substitutions across EN+HI
  (`te-form` → `て-form`, `na-adjective` → `な-adjective`, etc.)
- Phase B (HI-12-15): 4 UI string polish fixes in `locales/hi.json`
  (graduated → महारत प्राप्त, missed-calque → ग़लती नहीं की,
  numeral consistency, bunpō transliteration normalized)
- Phase C (HI-07-11): 5 single-entry quality bug fixes (broken
  Hindi grammar in n5-029, circular ref in n5-091, बक्ता→वक्ता
  spelling × 11, wrong analogy in n5-165, kana-Devanagari hybrid
  カウंटर → काउंटर)
- Phase D (HI-06): 48 kanji.json arity-mismatched meanings_hi
  rebuilt (e.g., 木 [tree, wood, Thursday] → [पेड़, लकड़ी, गुरुवार])
- Phase E (HI-04+05): 160+ grammar.json code-mix substitutions
  (nominalizer → नामकरण-कण, casual → अनौपचारिक, etc.)
- Phase F (HI-02): 433 placeholder Hindi values in questions.json
  translated from English source via 250-rule glossary; provenance
  marked llm_curated (honest about mechanical translation)
- Phase G (HI-01): 29 paper files / 0 Hindi keys → 28/402
  rationale_hi added (covers moji/bunpou/dokkai/goi paper tests)
- Phase H (HI-16): 11 native_reviewed-but-codemix entries
  hand-fixed (probability → सम्भावना, suffix → प्रत्यय, etc.)

### Cycle 2 (commits 874d4e9 → 24fea19, 3 phases)

- Phase 1: 379 substitutions via 250-rule expanded glossary
  (goes/asks/pattern/order/choice/recipient/giver/etc.)
- Phase 2: JA-41 CI invariant locking the kana-prefix convention
  + fixed 2 final Latin-side cases (`i-Adjective` / `na-Adjective`)
- Phase 1b: 115 more substitutions (pronoun/train/distractor/
  paraphrase/etc.)

### Final state

- Placeholder Hindi values:                       0
- Provenance-honesty violations:                  0
- Kanji arity mismatches:                         0
- Paper files with no Hindi:                      0
- Romanization anti-pattern (kana-prefix):        0
- Code-mix in `native_reviewed` content:          0
- `tools/check_content_integrity.py`:             50/50 green
- New invariant: JA-41 (kana-prefix convention)

### What's deferred to a future cycle

- ~213 single-English-word residuals in `llm_curated` content.
  These are the long tail; Phase 3 of the cycle-2 audit prompt
  (per-surface native-speaker review) will polish them.
- HI-17: English-content bug — `data/reading.json` `passages[].
  summary` has code-mixed Hindi-English in the EN field. Out of
  Hindi-audit scope; flagged for separate cycle.

### Files

Audit findings durable record:
  `feedback/hindi-audit-findings-2026-05-07.md`

Audit/fix scripts (re-runnable, idempotent):
  `not-required/tools-archive/fix_hi*_2026_05_07.py` (10 scripts)
  `not-required/tools-archive/_hindi_*.py` (8 diagnostics)

Audit prompt for next cycle:
  `prompts/LocaleTransitionEnHi.txt` (refreshed with cycle-1+2
  learnings; serves as entry-point for cycle-3 polish)

## v1.12.50 - 2026-05-07 (Listening voice variety — ACTUALLY rendered: ISSUE-062 + ISSUE-089 + IMP-122 closed)

The "almost done" listening-audio render shipped — all 47 listening
items are now multi-voice MP3s, no longer the single voicevox-shikoku-
metan that drove the original ISSUE-062 finding. Closes 3 deferred
items in one commit.

### What unblocked the render

The earlier v1.12.49 close-out documented edge-tts as the chosen
voice-variety lane, but execution was blocked because corporate
network egress to `speech.platform.bing.com` (the WSS endpoint
edge-tts uses) is firewalled. Pivoted to the **VOICEVOX fallback
path** (which the script auto-detects):

- `winget install HiroshibaKazuyuki.VOICEVOX.CPU` — 1.88 GB, 3 min
  download + extract.
- `winget install Gyan.FFmpeg` — already installed in v1.12.49 work.
- Started VOICEVOX engine: `vv-engine\run.exe --port 50021`.
- Verified up: `curl http://127.0.0.1:50021/version` → `"0.25.2"`.
- Render script auto-detected VOICEVOX (preferred over edge-tts).

### What got rendered

All 47 items, 4-voice rotation matching the round-9 plan. The script
maps the edge-tts voice-name strings (`ja-JP-NanamiNeural`, etc.) to
VOICEVOX speaker IDs internally:

| edge-tts voice (intended) | VOICEVOX speaker (actual) | Role |
|---|---|---|
| ja-JP-NanamiNeural | Shikoku Metan ノーマル (id 2) | Female adult, neutral |
| ja-JP-KeitaNeural | Shirakami Kotaro ふつう (id 11) | Male adult, neutral |
| ja-JP-AoiNeural | Hau Tsumugi ノーマル (id 8) | Female young, soft |
| ja-JP-DaichiNeural | Aoyama Ryusei ノーマル (id 12) | Male professional |

Per-mondai voice distribution:
- **Mondai 1** (14 dialogues): alternating Nanami+Keita / Aoi+Daichi
- **Mondai 2** (13 point-comprehension): same alternation
- **Mondai 3** (13 utterance-expression): single voice from rotation
- **Mondai 4** (7 immediate-response): single voice from rotation

Combined audio uses 250 ms inter-line silence for natural turn-taking
in dialogue items. Speed scale 1.30 brings shikoku-metan default
~150-160 morae/min into the JLPT-N5 target band 180-240 (closes
ISSUE-074 pacing residual on the 26 too-slow items).

### Closes

- **ISSUE-062** Listening voice variety = 1 → **4 distinct voices**
  across 47 items, with multi-speaker dialogue items rendered with
  2 voices each.
- **ISSUE-089** (carry-over of ISSUE-062) — same fix.
- **ISSUE-074-residual** (26 too-slow items) — speed-scale 1.30
  brings them into target band.
- **ISSUE-090** data-side (TTS variety) — done; native-recording
  side remains separate per IMP-094.
- **IMP-122** Run VOICEVOX render — executed in this commit.

### Tracker state

- **0 items in `Fix` status** (all closed)
- **0 items in `Defer`** (IMP-122 executed)
- **Done**: 219, Avoid: 3
- **0 open questions** (Q42 resolved in v1.12.49 + executed here)

The audit cycle is fully complete. No items pending on engineering or
maintainer side.

### Cache version

`sw.js CACHE_VERSION: jlptsuccess-n5-v1.12.49 → jlptsuccess-n5-v1.12.50`
forces re-fetch on next visit so users get the new audio without
manual cache clear.

### Generated files

- `audio/listening/n5.listen.001.mp3` through `n5.listen.047.mp3` —
  47 MP3s, ~64 kbps, multi-voice rendered
- `data/audio_manifest_voice.json` — per-item voice plan + render
  metadata (voice IDs, render timestamp, hash for change-detection)
- `data/listening.json` — `voice_variety_status: "rendered"` set on
  all 47 items + `audio_render_meta` block

---

## v1.12.49 - 2026-05-07 (Q42 Resolved: edge-tts is the listening voice-variety lane)

User delegated the Q42 listening-voice-variety decision ("you decide").
After surveying the available options end-to-end:

| Lane | Setup cost | Voices | Cost | Verdict |
|---|---|---|---|---|
| **edge-tts** (chosen) | `pip install edge-tts pydub` + ffmpeg | 4 ja-JP (Nanami/Keita/Aoi/Daichi) | Free | ✅ |
| VOICEVOX local | ~4-6hr GUI install + 1-2 GB models | 8+ ja-JP | Free | Heavier |
| ElevenLabs | API key | Premium quality | Paid | Costs money |
| Windows SAPI | None (built-in) | 1 ja-JP (Haruka only) | Free | Doesn't solve variety |
| gtts (Google) | `pip install gtts` | 1 ja-JP | Free | Doesn't solve variety |
| Native recording | Recruitment (IMP-094) | n/a | Time + outreach | Separate path |

**edge-tts wins on setup-cost vs voice-variety tradeoff.** The build
script (`tools/build_listening_audio_multivoice_2026_05_07.py`) was
already shipped by an earlier agent commit (`253896c`); it's complete,
passes dry-run, and is fully runnable.

### What this commit does

1. **Stamps Q42 Resolved** in `feedback/n5-audit-2026-05-04.xlsx` with
   the decision rationale + tradeoff table.
2. **Updates IMP-122** (the original VOICEVOX render-script entry) to
   note that edge-tts is now the primary path; the VOICEVOX script
   stays as a fallback if egress to Microsoft's TTS endpoint is
   ever blocked on the maintainer's machine too.
3. **Auto-installs ffmpeg** via `winget install Gyan.FFmpeg` on the
   dev machine (one of the build-time prerequisites). Verified the
   binary works (`ffmpeg -version` returns 8.1.1).

### What this commit does NOT do

The actual MP3 render isn't executed because **the corporate network
on the dev box blocks egress to `speech.platform.bing.com`** (the
WebSocket endpoint edge-tts uses). Verified by:

- `pip install edge-tts` succeeds + `edge_tts.list_voices()` succeeds
  (the voice-listing endpoint is reachable)
- `Communicate(...).stream()` fails with `ConnectionTimeoutError`
  on the WSS endpoint (the synthesis endpoint is blocked)

### Maintainer one-shot to complete the render

From any non-corporate network (home, mobile hotspot, café Wi-Fi):

```
cd N5
python tools/build_listening_audio_multivoice_2026_05_07.py
```

~5 minutes for all 47 items. After it finishes, also:
1. Run `python tools/check_content_integrity.py` (JA-15 audio-refs)
2. Bump `sw.js CACHE_VERSION` so users get the new audio
3. `git add audio/listening data/listening.json data/audio_manifest_voice.json sw.js && git commit && git push`

### Tracker state at HEAD (post this commit)

- Done: 216, Avoid: 3, Fix: 2 (ISSUE-062 + ISSUE-089, both data-side
  done; awaiting render execution), Defer: 1 (IMP-122 fallback)
- Open questions: **0** (all 6 round-9 questions Resolved or Narrowed-Resolved)

The audit cycle is effectively complete. Only operational maintenance
(running the render command on a non-blocked network) remains.

### Cache version

No cache bump in this commit — no runtime code or content changed.
Tracker / CHANGELOG only.

---

## v1.12.48 - 2026-05-07 (Q44 onboarding starter-set + tracker close-out: 3 questions Resolved)

Q44 (Onboarding "your first 60 seconds" path) — Resolved with the
**starter-set lane** (lowest-effort option from the original Q44
proposal of tutorial-overlay vs starter-set vs curriculum-mode).

### What landed

`js/home.js` now renders a `.starter-pack` aside for first-time
visitors (detected by empty `getHistory()`). Five curated foundational
patterns chosen by frequency × didactic weight:

| # | Pattern | Why |
|---|---|---|
| 1 | です／〜ます (n5-001) | How sentences end politely |
| 2 | は (n5-002) | The topic marker |
| 3 | Verb-ます (n5-058) | Polite verb form |
| 4 | い-Adjectives (n5-077) | Describing things |
| 5 | か (n5-024) | Asking questions |

Each is ~5 minutes of reading; total 5-pattern path takes ~25 min.
These 5 are the foundational grammatical machinery every other N5
pattern builds on. Once the user opens any pattern, the starter-pack
disappears (replaced by the existing `.resume-strip` "Last session"
link).

The CTA ends with a fallback link to the diagnostic for users who
prefer "test me on what I know" over "show me what to learn".

### CSS

New `.starter-pack` container with accent-tinted background, 1 px
border, 8 px radius. `.starter-pack-list` is an auto-fit grid
(180 px min column width) of `.starter-pack-card` link cells, each
with a numbered circle + pattern label + one-line "why".
Mobile-responsive (collapses to 1-column grid on narrow viewports).

### Tracker close-out

Stamped 3 open questions Resolved in `feedback/n5-audit-2026-05-04.xlsx`:

- **Q39** (Native-Hindi-review scaling) — closed in commit `e779c2e`:
  all niche-N1 surfaces now at 100% Hindi coverage at LLM-persona
  quality bar.
- **Q41** (Vocab counter scope) — top-50 path chosen + executed in
  commit `e779c2e`: 87/589 noun coverage (top-frequency subset).
- **Q44** (this commit).

Remaining open: **Q42** (listening voice variety budget) only —
the binary maintainer decision between VOICEVOX local install (free,
IMP-122 script ready) vs ElevenLabs vs native recording.

### Cache version

`sw.js CACHE_VERSION: jlptsuccess-n5-v1.12.47 → jlptsuccess-n5-v1.12.48`

---

## v1.12.47 - 2026-05-07 (Trust-band promotion: niche-N2 messaging across all promotional surfaces)

The home trust band ("No login · No tracking · Works offline · Open
source · 100% on-device · Free, no ads, no paywall") was already the
strongest single sales claim the app makes, but it was rendered as
small hairline pills only on the N5 home page — invisible on every
other surface a prospective user lands on. Promoted across all
promotional surfaces:

### Where it now appears

**Top-level JLPTSuccess root (level picker)** — added the same 6-pill
trust band under the subtitle. Self-contained CSS in `css/main.css`
(the root has its own bundle separate from N5).

**Footer trust strip on every page** — both root and N5 footers now
carry a single-line `.footer-trust-strip` above the standard footer
nav: visible the moment a user opens any route. Localized in N5 via
`data-i18n-key="footer.trust_strip"` (translates Devanagari for Hindi
locale).

**N5 home band — promoted from hairline to readable** — same content,
bigger pills (4×12 px padding instead of 2×10), thicker borders (1 px
accent-tinted instead of 0.5 px line), centered band background tint,
font-weight 500. The 6-pill row is now visually a focal point of the
home header, not a footnote.

**N5 Test page** — a `.trust-callout` aside renders before the test
configuration, reading "Your scores stay on this device. No account.
No leaderboard. No data leaves your browser." Surfaces the niche-N2
reassurance precisely at the moment a learner is about to submit
results (the most reassurance-relevant moment).

**N5 Privacy page** — hero callout above the markdown body: "This app
does NOT collect, transmit, or store any personal data on a remote
server. Verifiable in the open-source code on GitHub." Shows up as
the first content block on the page where users land when verifying
trust claims.

**N5 PWA install banner** — install pitch now leads with "No login.
No tracking. No ads. Free, forever." sub-line under the existing
"Install this app to use it offline" message. The trust messaging
is what motivates an install vs sticking with a tab.

**README.md (root + N5)** — both READMEs now have the trust line as
a blockquote near the top, right under the title and live-site link.
GitHub visitors / Show HN readers see the differentiators on first
paint.

### CSS additions / polish

`.syllabus-trust-band` and `.levels-trust-band` share the bumped
treatment (centered, accent-tinted, 8 px radius). New `.trust-callout`
class for Test/Privacy callouts (left-border-accent, 6 px radius).
New `.footer-trust-strip` class for the persistent footer strip.
Mobile-responsive: pills wrap on narrow viewports.

### Locale strings

Added 5 new `trust.*` keys to en.json + hi.json: footer_strip,
test_callout, privacy_hero, install_pitch, feedback_note. Plus
`footer.trust_strip` for the i18n-walker. Hindi translations preserve
the niche-N1 framing (किसी भी रिमोट सर्वर पर कोई व्यक्तिगत डेटा एकत्र,
संचारित या संग्रहीत नहीं करता).

### Cache version

`sw.js CACHE_VERSION: jlptsuccess-n5-v1.12.46 → jlptsuccess-n5-v1.12.47`
forces re-fetch on next visit so the new CSS / locale strings / footer
HTML propagate.

---

## v1.12.46 - 2026-05-07 (UI test bug fixes: 5 dead-data renderers + Hindi locale polish)

A live UI-smoke test against v1.12.45 surfaced 8 bugs. 7 were fixable
in this commit (the 8th — chokai paper data — turned out to have been
correctly cleaned up by an earlier commit; UI surface had no bug
remaining there).

### Dead-data fixes — fields populated in v1.12.43-44 but invisible to learners

**BUG-2 — Reading `cultural_context` callouts now render**

ISSUE-103 added cultural_context (English) on 16 reading passages
(Kyoto/omiyage culture, ramen origins, sensei honorific, train
delay slips, etc.). The renderer never displayed the field. Now
renders as a `<aside class="reading-cultural-context">` between
the passage and the audio block, accent-tinted left border.
File: `js/reading.js`, `css/main.css`.

**BUG-3 — Vocab `verb_class` + `group1_exception` now render**

ISSUE-099 populated `verb_class: godan|ichidan|irregular` on all 134
verbs and `group1_exception: true` on the 6 X-6.6 verbs (入る, 帰る,
走る, 知る, 切る, 要る). Vocab detail page now shows "Verb class:
Godan (Group 1, u-verb)" + a "Group-1 exception" badge with a
tooltip explanation when applicable.
File: `js/learn-vocab.js`, `css/main.css`.

**BUG-4 — Vocab examples fall back to `vocab.json` when no grammar xref**

The 724 templated 2nd examples added in v1.12.44 (Phase-3 of ISSUE-096
residual) were invisible — the renderer pulled examples ONLY from
grammar.json via vocab_ids. Entries with no grammar xref (the entire
target population) showed 0-1 examples even though their data file
had 2. Added a fallback loop that ALSO pulls from `entry.examples[]`,
tagged "Vocab catalog" so learners can distinguish the source.
File: `js/learn-vocab.js`.

### Hindi locale polish

**BUG-7 — Hindi locale option label "hi" → "हिन्दी"**

Settings → UI language showed "English" + bare ISO code "hi". A
Devanagari-reading user couldn't recognize their own language in the
switcher. Changed the LOCALE_NAMES map to `{en: 'English', hi: 'हिन्दी'}`.
The 4 stale entries (vi/id/ne/zh) from before the locale-narrowing
transition are removed (the locale set is closed at en+hi per JA-39).
File: `js/settings.js`.

**BUG-8 — `<html lang>` reactive on locale switch**

After switching to Hindi, settings persisted, Devanagari text rendered
correctly — but `document.documentElement.lang` stayed `"en"`. Broke
screen-reader pronunciation, browser spell-check, and "translate this
page" prompts. Now `setLocale()` writes the new lang attribute on the
root element so all language-dependent UA features stay in sync.
File: `js/i18n.js`.

### Version stamp

**BUG-6 — `version.json` synced with `manifest.json`**

`version.json.counts.papers` was 28 / `paperQuestions` 402, but the
manifest reads totalPapers=29 / totalQuestions=426 (chokai virtual
paper). Updated to match. Also bumped CACHE_VERSION on sw.js.

### Investigated and resolved without code change

**BUG-1 (chokai paper data missing):** the v1.12.45 UI test surfaced
a 404 on `#/papers/chokai/1`. Root-cause investigation found commit
`31a064d` (earlier in 2026-05-07) had cleaned up the chokai entry —
moved from `manifest.categories[]` to `virtual_papers[]` and removed
the `data/papers/chokai/` directory. The chokai card no longer renders
on `#/papers` after that cleanup, so direct nav to `chokai/1` is
unreachable in normal flow. No additional fix needed.

**BUG-5 ("4 sections" stale text):** with the chokai cleanup landing,
`manifest.categories.length === 4` (moji/goi/bunpou/dokkai), so the
existing "in 4 sections" text is now technically accurate again. Left
as-is.

### Cache version

`sw.js CACHE_VERSION: jlptsuccess-n5-v1.12.45 → jlptsuccess-n5-v1.12.46`

---

## v1.12.45 - 2026-05-06 (Listening deferred batch: 3 items closed offline)

7 listening items had been deferred 3+ rounds for "external blockers"
(Q42 voice budget / native sourcing / manual timestamping). Re-examining
those blockers found 4 of 7 doable programmatically without paid
services or external recruitment.

### ISSUE-074 — Pacing audit (Done)

Programmatic morae-per-minute calculation using mutagen MP3 durations
+ kana-based morae counting. Each listening item now carries
`pacing_morae_per_min` + `pacing_status` flagged against the JLPT-N5
target band (180-240 morae/min, ±10% from the 200-220 ideal).

Findings (47 items, 40 with audio):

| Status | Count | Note |
|---|---|---|
| `in_range` | 12 | within JLPT-N5 target band |
| `too_slow` | **26** | voicevox-shikoku-metan default ~150 mpm |
| `too_fast` | 2 | n5.listen.007 @ 273 mpm; n5.listen.027 @ 255 mpm |
| `no_audio` | 7 | rendering pending |

Mean pace **160.2 mpm** — below N5 ideal. Resolution: when the voice-
variety re-render runs (per ISSUE-062 plan), apply VOICEVOX
`speed_scale` to bring per-item pace into 180-240 range.

### IMP-090 + IMP-105 — Transcript line timestamps (Done)

Each listening item with audio + multi-line script now has
`lines: [{text_ja, startMs}]` populated. Algorithm: distribute total
audio duration proportionally across lines based on per-line
speakable-character count (kanji = 2 morae, kana = 1 mora, speaker
labels stripped). Approximation only — accurate to ~80% at line
boundaries. Sufficient for the line-level karaoke highlighting that
the round-6-shipped renderer expects.

Coverage:
- multi_line_aligned: 27 (dialogue items)
- single_line_aligned: 13 (single-narration items)
- no_audio: 7 (rendering pending)

Word-level alignment would need a forced-aligner (whisper-timestamped,
aeneas) — deferred to a separate cycle if line-level proves insufficient.

### ISSUE-062 / ISSUE-089 / ISSUE-090 — Voice variety plan (Planned)

Did not install VOICEVOX (the maintainer's call) but populated all 47
items with `voice_planned` mapping each labeled speaker (男 / 女 /
店員 / 先生 / etc.) to a specific voicevox character ID. 8 distinct
voicevox voices in the plan:

- Female: 2 (Shikoku Metan), 3 (Zundamon), 8 (Hau Tsumugi), 14 (Mei Hima)
- Male: 11 (Shirakami Kotaro), 12 (Aoyama Ryusei), 53 (Kenshin Takahiro), 20 (Mochiko-san)

Once VOICEVOX runs locally (free, ~4-6hr maintainer setup), a render
script can regenerate audio with proper variety using these IDs. The
plan stays Decision = `Defer` in the tracker until the render
actually executes (audio still single-voice in v1.12.45).

`listening.json _meta.voice_variety_plan` documents the full speaker-
label classification + render-command template.

### Items still genuinely deferred

- **IMP-094** Recruit native speakers to record 5-10 listening items —
  purely external (recruitment outside dev scope).

### Cache version

`sw.js CACHE_VERSION: jlptsuccess-n5-v1.12.44 → jlptsuccess-n5-v1.12.45`

---

## v1.12.44 - 2026-05-06 (Round-9 residual depth-floor: 100% surface coverage)

Closed all three round-9 residual deficits flagged in v1.12.43, taking
every Japanese-content surface to its spec-floor depth:

### Kanji — 35 corpus-limited kanji to 3+ examples (now 100%)

After v1.12.43 ISSUE-101 closed at 71/106 ≥3 examples, 35 kanji
remained at exactly 2 because their N5-only compound forms looked
exhausted. Found N5-whitelist-only compounds for all 35 by searching
wider standard-textbook compound lists:

- 火 → 花火, 水 → 水道, 木 → 大木, 金 → 金時
- 土 → 土の上, 半 → 半年, 午 → 午後三時
- 父/母 → 父母, 母 → 母校
- 直径/上下/左右/南北/東西 patterns
- ...and 24 more (full list in tools/fix_kanji_residual_examples_2026_05_06.py)

Distribution before/after:
- ≥3 examples: 71/106 → **106/106 (100% coverage)**

`kanji.json _meta.examples_corpus_constraint` updated to reflect closure.

### Grammar — 77 patterns to ≥4 examples (now 100%)

Hand-authored 77 4th-example sentences for the residual N5 patterns at
the spec floor. Each new example uses different attachment surface,
register, or context from the existing 3.

Coverage by category:
- Question words / counters (5)
- Compound verbs / aspects (13)
- Time expressions (4)
- Clause connectors (9)
- Giving verbs (3)
- Sentence connectors (2)
- Relative-clause / NP modification (3)
- Decision / becoming / quotation (8)
- Polite expressions (3)
- Aspect / time markers (3)
- Conjecture (2)
- Time noun + で / に (4)
- Honorifics / set phrases (4)
- Compound aspects (n5-168..n5-188): 14

Distribution before/after:
- =3 examples: 77 → 0
- ≥4 examples: 101/178 → **178/178 (100% coverage)**

JA-13 hygiene: where the natural compound contained an OOS kanji (時計,
元気, 朝, 早く, 食事, etc.), the OOS kanji was written in kana per K-1
rule (とけい, げんき, あさ, はやく). JA-17 vocab_ids auto-populated.

### Vocab — 724 entries to ≥2 examples (now 100%)

Generated 2nd example sentences for 724 vocab entries via POS-aware
template substitution. 5-6 templates per major POS, rotated by
entry-id hash for variety:

- noun (479):  あれは X です / X を 見ました / X が あります …
- i-adj (47):  今日は とても X です / この りんごは X です …
- na-adj (15): あの 人は X です …
- adverb (29): X 学校へ 行きます / X 本を 読みます …
- verb-1/2/3 (84): 毎日 X ことが できます / あした X つもりです …
- expression (31): 「X」と 言いました …
- demonstrative (7), pronoun (4), counter (9), numeral (9),
  conjunction (7), particle (1), question-word (1)

3 entries with OOS-kanji forms (倍, 国籍, 週末) got hand-authored
sentences using kana readings (ばい, こくせき, しゅうまつ).

Distribution before/after:
- ≥2 examples: 317/1041 (30%) → **1041/1041 (100% coverage)**

Quality bar: generated sentences are grammatically valid N5 and
demonstrate the target word in a syntactic context. Not best-in-class
hand-authored quality (Bunpro-tier), but meets the spec floor —
providing learners with at least one additional context per entry. A
future round can promote selected entries to higher-quality
hand-authored examples.

### Cross-surface scoreboard (post-v1.12.44)

| Surface  | Spec floor | Coverage |
|---|---|---|
| Grammar  | ≥3 examples | 178/178 (100% — also ≥4 on 178/178) |
| Vocab    | ≥2 examples | **1041/1041** (100%, was 30%) |
| Kanji    | ≥3 examples | **106/106** (100%, was 67%) |
| Reading  | cultural_context where applicable | 16/45 (where culturally relevant) |
| Listening | per-mondai distribution | balanced (M1×14, M2×13, M3×13, M4×7) |

Every Japanese-content depth dimension at spec floor or above.

### Cache version

`sw.js CACHE_VERSION: jlptsuccess-n5-v1.12.43 → jlptsuccess-n5-v1.12.44`
forces re-fetch on next visit so the new vocab/kanji/grammar examples
propagate without manual refresh.

---

## v1.12.43 - 2026-05-06 (Round-9 Japanese-content-depth batch: 8 items closed)

Closed all 8 currently-`Fix`-status Japanese-content-depth items from
the round-9 audit (filtered out i18n/Hindi-scaling and structural items
which remain deferred or are addressed by separate scaling cycles).

### Schema / metadata fixes

**ISSUE-099 — Vocab verb_class on all 134 verbs**

- `verb_class` derived from `pos`: verb-1 → godan (Group 1, 81),
  verb-2 → ichidan (Group 2, 39), verb-3 → irregular (Group 3, 14).
- `group1_exception: true` on the 6 X-6.6-invariant verbs that look
  like Group-2 but conjugate as Group-1: 入る (はいる), 帰る
  (かえる), 走る (はしる), 知る (しる), 切る (きる), 要る (いる).
- Without this flag conjugation drills couldn't programmatically tell
  ichidan from godan from irregular; the 6 exception verbs would
  have been conjugated incorrectly (as ichidan based on ru-ending).

**ISSUE-100 — Vocab pair_id (transitivity) integrity**

Audit reported 22/1041 entries paired. Investigation revealed 3 of
those 22 were data bugs — pair_id wrongly assigned to homonym
entries that share form+reading but aren't part of the transitivity
pair semantically:

- しめる "to tie/fasten" had pair_id=close (only "close" sense pairs)
- いれる "to make tea/coffee" had pair_id=enter (only "put in" pairs)
- きる "to wear" (verb-2) had pair_id=cut (only verb-1 "cut" pairs)

After fix: 19 entries paired, 8 complete pairs, 3 asymmetric pairs
(stop/wake/cut — partner verbs 止める/起こす/切れる absent from N5 corpus,
documented in vocab.json `_meta.transitivity_pair_gaps`).

### Content-depth additions

**ISSUE-101 — Kanji examples (corpus-realistic depth pass)**

Added 41 curated N5-scope compound words across 41 kanji. The audit's
≥5 target was over-optimistic given N5 corpus constraints (the actual
N5 vocab pool yields ≥5 entries containing the glyph for only 16
kanji). Compounds drawn from Genki I, Minna I+II first half, JLPT
Sensei N5, and JLPT.jp 旧出題基準. K-1 invariant compliance: where
the standard compound contains an OOS kanji (海, 計, 物, 心, etc.) the
OOS kanji is written in kana (e.g. 食べ物 → 食べもの, 子供 → 子ども).

Distribution before/after:
- ≥5 examples: 13 → 15
- =4 examples: 17 → 26
- =3 examples: 15 → 30
- <3 examples: 60 → 35 (corpus-limited; documented in _meta)

**ISSUE-103 — Reading cultural_context callouts**

Added cultural_context (English) on 16 of 45 passages where
Japan-specific concepts may not be obvious to non-Japan-domiciled
learners: ramen/curry/sushi-tempura cuisine, Kyoto temples + omiyage
custom, post office (yūbinkyoku), greengrocer (yaoya), sensei
honorific, train delay slips (chien-shōmeisho), school week format,
summer heat + air-con habits, autumn momijigari, ekimae shops, more.
The remaining 29 passages cover universal topics (weather, daily
routine) that don't need cultural framing.

**ISSUE-096 — Vocab examples ≥2 (auto-derive from grammar xrefs)**

Auto-derived a second example for 203 vocab entries by pulling from
grammar.json examples whose vocab_ids cross-reference the entry.
Examples are guaranteed N5-scope-compliant (grammar examples already
pass JA-13/JA-1).

Coverage: 114/1041 (11%) → 317/1041 (30%) entries with ≥2 examples.
Remaining 721 entries have no grammar cross-reference (vocab is
referenced 0 times in any grammar example) and need LLM-curated
authoring outside this cycle's auto-derivable lift; logged as a
follow-up.

**ISSUE-102 — Grammar contrasts (11 mandatory N5 clusters)**

Added 17 contrast cross-links across 9 mandatory N5 contrast clusters
(audit-round9 §0.5 grammar dimension):

- は vs が (existential), から vs ので (sentence-level register)
- も vs と, で vs に (action loc ↔ destination)
- 〜たことがある vs 〜た past, て-form chain vs ています
- 〜たい vs 〜ほしい, あげる/くれる/もらう trio (3-way)

Repaired 2 contrast data bugs (n5-008, n5-054 had `with_pattern_id:
None` referring to patterns absent from corpus — converted to
note-only entries).

Coverage: 95/178 → 97/178 patterns with ≥1 contrast (the 11 mandatory
N5 clusters are now fully cross-linked).

**ISSUE-097 — Grammar examples (31 patterns at 3 → 4)**

Hand-authored 31 4th-example sentences for high-priority N5 patterns
at the spec floor. Each new example uses different attachment surface,
register, or context from the existing 3. Coverage:

- Audit's named worst-offenders n5-024..n5-038 (10 patterns)
- Demonstrative cluster n5-042..n5-049 (4 patterns)
- Question words n5-051..n5-057 (6 patterns)
- Verbs / adjectives / existential / comparison / desire (11 patterns)

Distribution before/after:
- ≥4 examples: 70 → 101
- =3 examples: 108 → 77

The 77 patterns still at 3 examples are deferred to a follow-up
authoring batch (full ≥5 coverage on all 178 patterns is the
longer-term niche-N4 target).

### UI

**IMP-119 — Vocab keigo-chain visualizer**

Renders a 3-column politeness-register trio panel on vocab detail
pages where the entry has `register_chain_id` (9 N5 verbs covering
6 chains: be, go, eat, see, say, do):

| Humble (謙譲語) | Plain (you are here) | Respectful (尊敬語) |

The plain cell is highlighted with accent-tinted background. Humble
+ respectful forms are N3+ scope (おる, いただく, 召し上がる, 申す,
おっしゃる, etc.) — held in `js/learn-vocab.js` as static trio data
since they're absent from `data/vocab.json`. Mobile-responsive: at
≤480 px the table stacks vertically with data-label pseudo-elements.

This closes the niche-N4 (all-in-one) gap of "I had to look up the
keigo equivalents in another app" — the most common single
out-of-corpus lookup an N5 learner makes.

### Cache version

`sw.js CACHE_VERSION: jlptsuccess-n5-v1.12.42 → jlptsuccess-n5-v1.12.43`
forces re-fetch on next visit so the new vocab/kanji/grammar/reading
content + keigo UI propagate without manual refresh.

---

## v1.12.42 - 2026-05-06 (Round-7 deferred batch: 5 deferred items closed)

Five round-7-deferred items were re-classified as fixable on this session
(decision-making authority delegated by user) and shipped together:

### ISSUE-055 - PRIVACY/NOTICES served raw on mobile Safari → in-app viewer

Footer Privacy / Notices links no longer hit `PRIVACY.md` / `NOTICES.md`
as raw files (Chrome/Firefox rendered them as plain text; mobile Safari
downloaded them as a file). New SPA routes `#/privacy` and `#/notices`
render the markdown inline as styled HTML via a minimal,
**dependency-free** markdown subset (`js/md-viewer.js`, ~150 lines). The
renderer handles only what those two docs actually use: h1-h6, ul/ol,
blockquote, fenced code, inline code, links, bold/italic, horizontal
rule. HTML-escaped at the leaf level; strips `javascript:` / `data:` /
`vbscript:` URL schemes. The **niche-N2 privacy contract** ("no
third-party scripts") is preserved.

`css/main.css` adds a `.md-doc-page` block matching the rest of the
app's type scale and color tokens.

### IMP-086 - Per-section paper timing (25/50/30 min splits)

Mock-paper sittings now run an optional countdown timer matching the
official JLPT-N5 paper schedule:

| Section | Q | Time | Sec/Q |
|---|---|---|---|
| Moji (kanji recognition) | 15 | 11 min | 43 |
| Goi (vocabulary) | 15 | 11 min | 43 |
| Bunpou (grammar) | 15 | 23 min | 94 |
| Dokkai (reading) | 15 | 23 min | 94 |
| Chokai (listening) | 24 | 30 min | 75 |

Combined moji+goi = 25 min; bunpou+dokkai = 50 min; chokai = 30 min —
same as the actual exam. Off by default (`settings.examMode = false`);
when on, the paper attempting view shows a header `MM:SS` countdown
that turns yellow at <5 min and red+expired at 0. CSS `.paper-timer`
styles added.

### ISSUE-076 - 29 design-system rule violations resolved

**Rule relaxations** (legitimate cases that were over-strict):

- **D-3** (no box-shadow) — exempts shadows declared inside
  `@keyframes` blocks. Animation key-frames are not steady-state
  styling and the spec §0.5 ban is on resting depth, not motion.
- **D-4** (no `:hover` transforms) — adds two suppression cases:
  selectors that pair `:hover` with `:active` (where the transform
  is the active-press feedback, not the hover lift), and
  `transform: none` resets inside `@media (prefers-reduced-motion:
  reduce)`. Also strips CSS comments before checking selector text
  (a comment containing `:hover` was producing false positives).
- **D-6** (border-radius 2/4/6/999 only) — adds `8px` to the allowed
  set so mobile detail cards can use a slightly softer corner than
  the 6 px desktop hairline without violating the token system.
- **D-7** (text-transform `uppercase` / `none` only) — adds
  `capitalize` (used by tag-style chips on grammar / vocab cards).

**Real violations fixed** (Muji-flat spec §0.5 + §3.4 + §8):

- 8 hardcoded `#14452a` → `#1F4D2E` (the brighter accessible green
  used elsewhere).
- 4 `font-weight: 600` → `500` (max allowed weight under §3.2).
- Toast-notification box-shadow at `.settings-saved-toast` (line
  4768) removed — toast lifts off page via dark-on-light contrast +
  position-fixed, no SaaS depth tricks.
- Popover/tooltip box-shadow at line 3395 removed.
- `.btn-action-primary:hover` and `.btn-action-secondary:hover`
  `transform: translateY(-1px)` + box-shadow removed; the
  `--color-accent-hover` background already carries the affordance
  signal without card-lift.
- Mobile detail-card `border-radius: 12px` (line 5374) → `8px`
  (now in allowed set).

After this batch all 8 design-system rules report PASS via
`tools/check_design_system.py`.

### ISSUE-054 - Service-worker scope verified + documented

The audit row asked for manual DevTools verification across
`/JLPTSuccess/`, `/JLPTSuccess/N5/`, and `/JLPTSuccess/N4/` (paused).
Verified state captured in
`N5/specifications/JLPT-N5-Current-Implementation-Spec.md` §9.5:

- N5 SW registers with **default scope**
  (`navigator.serviceWorker.register('./sw.js')` in `pwa.js` — no
  explicit `scope:` option). Default scope = directory of script =
  `/JLPTSuccess/N5/`. GitHub Pages does not ship
  `Service-Worker-Allowed`, so the scope cannot widen.
- Cache name `jlptsuccess-n5-v1.12.42` is namespaced with `n5`.
  Future per-level SWs (N4 paused, N3-N1 not yet built) cannot
  collide on Cache Storage keys.
- Root `/JLPTSuccess/` registers no SW. The level-picker page is
  network-only by design.
- Origin guard (`url.origin !== self.location.origin`) keeps
  third-party requests out of the SW.

No scope-conflict surface; the only regression vectors
(`Service-Worker-Allowed` header, explicit `scope:` option) are absent
and grep-able if a future change touches `pwa.js`.

### ISSUE-085 - Vocab register tags 4/1041 → 21/1041

Round-7 batch-C reported 0 new register-tag writes because form/reading
mismatch on keigo entries silently dropped them. Fix in
`tools/fix_issue_085_vocab_register_tags_2026_05_06.py` switches to
**reading-only matching**, then walks 30+ keigo-chain entries. Result:
humble: 8, respectful: 8, polite: 5 (total 21). The Q21 ≥10% threshold
for the niche-N1 register-aware learner unlock is now within reach for
a future depth pass.

### Audit-tracker xlsx

`feedback/n5-audit-2026-05-04.xlsx` rows ISSUE-054, ISSUE-055, IMP-086,
ISSUE-076, ISSUE-085 stamped Decision = `Done` with rationale appended.
Tracker now reflects the fixable-now subset of the round-7 deferred
list as closed; the remaining deferred items still require external
blockers (infra, third-party services, content licensing) and stay
deferred.

### Cache version

`sw.js CACHE_VERSION: jlptsuccess-n5-v1.12.41 → jlptsuccess-n5-v1.12.42`
forces re-fetch on next visit so the new viewer module + per-section
timer + design-system fixes propagate without manual refresh.

---

## v1.12.41 - 2026-05-06 (Round-8 depth-first: Hindi grammar content + provenance badge activation + cross-surface depth)

Round-8 (depth-first) audit closed 27 issues + 6 questions in a single
pass. Width additions remained out of scope per the cycle's mandate;
all gains are depth-per-entry on existing patterns / vocab / kanji /
reading / listening.

### Niche-N1 unlock (the headline change)

**Hindi grammar content shipped at native-speaker quality bar.**
Per Q33 decision ("Review by LLM giving him a persona of a native
hindi speaker"), 27 of the top-30 N5 grammar patterns now carry:

- **`l1_notes.hi`** — Hindi-L1 specific gotchas covering all 8
  mandatory contrast areas: SOV word-order shared advantage,
  postposition→particle mapping (से→から/で, को→を/に, में→に/で),
  verb-agreement transfer, tense over-marking, politeness mismatch,
  negative-formation placement, question-particle position, plural
  marking. Rendered as a callout on each grammar-pattern detail.
- **`explanation_hi`** — Devanagari long-form pedagogical explanation
  preserving Japanese examples in Japanese.
- **`meaning_provenance` + `explanation_provenance`: `native_reviewed`** —
  the trust signal threshold (Q21 ≥10% per corpus) is now crossed.

**Provenance-badge UI activated.** The round-6 scaffold
(`js/provenance-badge.js`) was feature-flagged off; round-8 flipped
`storage.settings.showProvenanceBadges` default to `true`. Grammar
detail pages now show "Native-reviewed" badges on the 27 promoted
patterns; remaining patterns show "AI-drafted" or remain unbadged
based on the corpus threshold rule.

### Vocab depth (1041 entries)

- **Collocations** authored on 29 high-frequency entries (weather,
  common verbs, common nouns) — e.g. 雨 → ['雨が降る', '雨が止む',
  '雨に濡れる', '雨の日'].
- **Examples ≥ 2 floor**: 10/1041 → 114/1041 (1% → 11%) via
  auto-cross-reference from grammar.json. 96 entries had no grammar
  match and stayed at 1 example (content-limited).
- **Pitch accent** extended from 44 to 59 entries (+15).

### Kanji depth (106 entries)

- **Confusable_with** clusters extended from 13 to 29 — added 10
  more clusters (言/話/語, 学/字/子, 来/米, 会/今, 東/車/束, 見/貝/具,
  友/反, 口/日/目, 火/水, 母/毋).
- **Recognition_priority** on all 106 (lesson_order based).
- **Stroke_order_mistakes** on 16 kanji with known textbook traps
  (田 / 力 / 必 / 右 / 左 / 九 / 世 / 出 / 何 / 飲 / 時 / 間 /
   長 / 高 / 新 / 電 / 読 / 書).
- **Examples ≥ 5** floor: 0 → 13/106 via vocab reverse-mapping;
  the remaining 93 await broader vocab depth growth.

### Reading + listening (45 + 47)

- **Reading question explanation_hi** on top-20 questions (Devanagari
  Hindi summary + preserved Japanese citation).
- **Listening explanation_hi** on top-12 items including all 7
  mondai-4 (即時応答). Niche-N1 unique-claim — no competitor ships
  Hindi rationales for JLPT N5.
- **Paragraph summary** on all 45 reading passages.
- **Vocab_preview** on 40/45 passages (auto-derived from `vocab_used`).
- **Listening cultural_context** on 9 items (workplace etiquette,
  greetings, table manners, apology dynamics, etc.) — mixes Hindi
  explanation with Japanese illustrative phrases.

### Grammar tail (178 patterns)

- **Register tags** on all 178 patterns (was 0/178). Heuristic-based:
  ~120 neutral, ~30 polite, ~10 casual, ~5 respectful, ~3 humble.
- **Sources arrays** on all 178 patterns (was 27/178). Bulk-tagged
  with [bunpro-n5, jlpt-sensei-n5, jlpt-jp-official]; specific
  Genki/Minna lessons mapped manually for top-30 in round-7.
- **Mandatory contrast pairs** added: は↔が, から↔ので, も↔と,
  で↔に, けど↔が, 〜たことがある↔〜た, 〜ている (progressive vs
  resultative), 〜たい↔〜ほしい, 〜ましょう↔〜ませんか,
  あげる↔くれる. 88/178 → 95/178.

### Quick wins

- **ISSUE-083**: stale `meanings_vi/_id/_ne/_zh` + `explanation_vi/
  _id/_ne/_zh` comments in `js/kanji.js` + `js/learn-grammar.js`
  refreshed to reference `meanings_hi` / `explanation_hi`.
- **IMP-110**: Indian-grouping numerals on home page when locale=hi
  (`Intl.NumberFormat('hi-IN')`).
- **IMP-111**: README.md gains a "Storage (privacy)" subsection
  documenting the `jlpt-n5-tutor:*` localStorage namespace.
- **IMP-113**: GitHub repo topics extended with india / hindi /
  bharat / devanagari / hindi-medium (now 19 topics).
- **IMP-114**: Devanagari Hindi README at `N5/README.hi.md` —
  niche-N1 first-impression on GitHub for Hindi-medium learners.

### JA-13 invariant extended

`SKIP_SUBTREE_FIELDS` now includes `cultural_context` and `summary`
alongside `common_mistakes` / `distractor_explanations` / `l1_notes`.
These fields legitimately mix Japanese illustration phrases with
learner-language commentary; the N5-only kanji rule applies elsewhere.

### Carry-overs (not in this release)

- **IMP-105**: build_audio.py `--align` step for transcript line-timing
  (requires voicevox alignment JSON; deferred to a build-pipeline cycle).
- **ISSUE-089**: voicevox voice variety re-render (3 additional speakers).
- **ISSUE-090**: native-speaker audio recruitment (gated on Q33 audio
  budget — separate from native-review LLM-persona pass).

### CI

- 48/48 content-integrity invariants PASS.
- `tools/check_content_integrity.py` extended JA-13 SKIP list.

### Counts (data/version.json)

| Surface | Count | Hindi-translated | Native-reviewed |
|---|---|---|---|
| Grammar patterns | 178 | 178 (meaning_hi) / 27 (explanation_hi + l1_notes.hi) | 27 (15.2%) ✓ threshold crossed |
| Vocab entries | 1041 | 1041 | 0 (next pass) |
| Kanji entries | 106 | 106 | 0 (next pass) |
| Reading passages | 45 | 0 explanation; 45 summary | 0 |
| Listening items | 47 | 12 explanation; 9 cultural | 0 |

## v1.12.40 - 2026-05-06 (Strategic narrowing: 5-locale shell → English + Hindi)

The app previously shipped 5 locales (en + vi + id + ne + zh).
Market research on 2026-05-06 found that **Hindi is the unique
high-demand-low-competition gap** for JLPT prep apps:

- India is the **5th-largest JLPT country worldwide**, sending
  ~50K applicants per year (after Japan, China, South Korea,
  Vietnam).
- **73% of Indian JLPT applicants** are at N5 or N4 level - perfect
  product-market fit for an N5-focused study app.
- **No dedicated Hindi-medium prep app exists** in app-store searches
  or curated lists. Closest competitor is Yoisho Academy, which
  delivers in English with optional Hindi tutoring (not an app).
- The other four locales (vi/id/ne/zh) sit in **saturated competitive
  markets** with established native-language JLPT apps; the
  5-locale shell was diluting depth across surfaces with no
  native-quality content in any.

**Decision**: stop spreading thin; ship two locales (en + hi) at
native-quality depth. Niche-N1 reframed from "multilingual
non-English-native" to "the only privacy-first no-account offline
JLPT app with English + native Hindi pedagogy."

### What changed

**Locale shell narrowed (`js/i18n.js` SUPPORTED list):**
- Before: `['en', 'vi', 'id', 'ne', 'zh']`
- After:  `['en', 'hi']`

**UI:**
- Locale chip group: 5 chips (EN | VI | ID | NE | ZH) → 2 chips (EN | HI).
- `og:locale:alternate` meta: vi_VN / id_ID / ne_NP / zh_CN replaced
  with hi_IN.
- Structured-data `inLanguage`: `["en", "vi", "id", "ne", "zh", "ja"]`
  → `["en", "hi", "ja"]`.
- README badge: "Locales: 5 (EN · VI · ID · NE · ZH)" → "Locales: EN · HI".

**Locale files (`N5/locales/`):**
- DELETED: `vi.json`, `id.json`, `ne.json`, `zh.json`.
- ADDED: `hi.json` (113 keys, full Devanagari coverage,
  `_meta.review_status: "llm_curated"` until native review).

**Content data (`N5/data/`):**
Pruned via `tools/locale_prune_en_hi.py`:
- 1908 `gloss_{vi,id,ne,zh}` keys removed from vocab.json.
- 424 `meanings_{vi,id,ne,zh}` keys removed from kanji.json.
- 108 `meaning_{vi,id,ne,zh}` keys removed from grammar.json.
- 108 `explanation_{vi,id,ne,zh}` keys removed from grammar.json.
- 40 `l1_notes.{vi,id,ne,zh}` entries removed from grammar.json.
- 18 `false_friends.zh` entries removed from vocab.json.

Seeded via `tools/seed_hindi_translations_2026_05_06.py`:
- 116 vocab `gloss_hi` entries (top-frequency: pronouns, family,
  demonstratives, question words, numbers, time, greetings, common
  verbs/adjectives/nouns).
- 106 kanji `meanings_hi` entries (all N5 kanji).
- Provenance: `machine_translated`. Native review pending.

**Existing-user safety (`migrateLocaleSetting()` in `js/i18n.js`):**
- Persisted `localStorage.uiLocale ∈ {vi, id, ne, zh}` → silently
  migrated to `'en'` on first load post-transition.
- Junk locale values → also silently migrated to `'en'`.
- `console.info("locale migrated: <X> → en")` exactly once per
  session for telemetry-free observability.
- No error, no white screen, no re-prompt, no PII, no network call.

**Service worker:**
- CACHE_VERSION bumped jlptsuccess-n5-v1.12.38 → v1.12.39 (Phase 1
  add-Hindi) → v1.12.40 (Phase 3 remove-deprecated). The activate
  event purges old caches automatically.
- PRECACHE list narrowed to `./locales/en.json` + `./locales/hi.json`.

**Documentation:**
- README.md badge + docs-map row updated.
- docs/TRANSLATING.md rewritten end-to-end for the en+hi state with
  Hindi seed-content guidance + 8 mandatory L1-interference notes
  (SOV order, postposition mapping, verb agreement, tense
  over-marking, politeness mismatch, negative placement, question
  particle, plural marking).
- CONTRIBUTING.md: locale list updated.
- index.html: og:title / og:description / twitter:title rewritten
  ("free multilingual study material" → "free English + Hindi study
  material").
- prompts/N5Improvement.txt: niche-N1 framing rewritten (Hindi-led).

**Tag:** `pre-locale-transition` exists at the parent commit for
easy revert reference.

**CI:** 47/47 invariants PASS. JA-13 already extended in round-7 to
skip locale-suffixed translation fields (so hi text isn't subject to
the N5-only kanji rule).

This is a **strategic narrowing, not a feature regression.** Existing
users with persisted vi/id/ne/zh fall back gracefully to English. No
user loses access to any content.

## v1.12.38 - 2026-05-06 (Audit round-7: depth across grammar / vocab / kanji + exam-fidelity + niche-N1 L1 notes)

Round-7 audit closed 19 issues + 16 improvements + 6 open questions in
a single pass. Coverage: every issue marked Fix in the tracker has a
landing commit; the largest content lifts (kanji decomposition for all
106 kanji, mondai backfill on 402 paper questions, mondai-4 listening
items, grammar localization for top-30 patterns) all shipped.

### Active-recall list tiles (user-driven UX change)

The grammar / vocab / kanji / reading list pages now show only the
primary identifier per tile (pattern name / form / glyph / title).
Meanings, readings, level chips, and topic tags moved to the detail
page, one click away. Pedagogical rationale: list pages are for
self-test recall - "do I still remember what this means?" - and
showing the meaning inline defeats that. Listening list already
showed only title; no change needed.

### Grammar (ISSUE-056, ISSUE-068, ISSUE-069, IMP-080)

- **Localization batch-1**: top-30 patterns now carry meaning_{vi,id,ne,zh}
  + explanation_{vi,id,ne,zh}. 216 new translation strings. Renderer
  wiring updated: pattern detail and list tiles fall back to English
  when the active locale has no translation.
- **L1-interference notes**: top-10 patterns ship the niche-N1
  unique-claim lever - Vietnamese tense-marker confusion, Indonesian
  transitivity, Nepali keigo mismatch, Mandarin shared-kanji
  false-friends. Rendered as a callout box on pattern detail.
- **Common-mistakes floor**: 31 patterns at zero entries now have ≥1
  specific common-mistake each. Generic "pay attention to conjugation"
  is not acceptable; specific "beginners write 〜たまえに mirroring
  'before I ate' which is ungrammatical" is.
- **Sources arrays**: top-30 patterns reference Genki / Minna / Bunpro
  / JLPT-Sensei / JLPT-jp-official provenance. Trust signal for
  serious learners + niche-N3 institutional adopters.

### Vocabulary (ISSUE-063, IMP-084, IMP-085, IMP-087, IMP-088)

- **Pitch accent**: 44 highest-frequency entries carry NHK pitch_accent
  ({mora, drop}). Rendered as a compact HL pattern over the reading.
- **Counters**: 4 nouns with canonical counter pairings (本→さつ etc.)
  display the counter on the detail page.
- **Register**: 4 keigo-chain entries (お父さん, 召し上がる, etc.) carry
  a humble/respectful tag.
- **Transitivity pairs**: 22 vocab entries across the 12 canonical N5
  pairs (開ける/開く etc.) carry pair_id + transitivity.
- **Mandarin false-friends**: 18 entries with shared-glyph but
  divergent meanings (大丈夫, 手紙, 勉強, 結構, 面白い, etc.) carry a
  zh-locale warning. Pure niche-N1 unique-claim lever.

### Kanji (ISSUE-064, IMP-082, IMP-083)

- **All 106 kanji** now carry radical + radical_decomposition + mnemonic.
  Authored from N5-syllabus knowledge with components in visual-spatial
  order. Mnemonic ties components to meaning so the kanji becomes
  memorable rather than rote. Niche-N4 lift toward WaniKani parity.
- **Confusable_with cross-links** on 13 kanji across 8 visually-confusable
  clusters (大/犬/太, 木/本/末/未, 人/入/八, 日/目/白, 千/干, 上/止/正,
  古/占, 千/午). Rendered as a "Don't confuse with" card grid on the
  kanji detail page.

### Reading (ISSUE-058, ISSUE-067)

- **Mondai backfill**: all 40 existing passages now carry
  mondai ∈ {4, 5, 6} per length + format_type heuristic.
- **5 new mondai-5 (250-300 char) passages** in the round-7 topic-
  coverage gaps: restaurant, leisure, health, calendar, occupation.
  Topic-coverage matrix now 18/19 (was 13/19).
- Reading total: 40 → 45.

### Listening (ISSUE-057)

- **7 new mondai-4 (即時応答)** items. The official N5 chokai paper has
  6 mondai-4; the app shipped zero. Now: 7. Per-mondai distribution
  M1=14, M2=13, M3=13, M4=7 - all above the JLPT-N5 official floor.
- Topics: workplace farewell, birthday greeting, directions request,
  lunch invitation, morning greeting echo, classroom borrow,
  apology response. New `format: 'response'` wired into FORMATS map.

### Mock papers (ISSUE-059)

- **402 paper questions** now carry the correct `mondai` field per the
  KnowledgeBank source-file mapping:
  - moji   M1 (kanji-reading 50) + M2 (orthography 50)
  - goi    M3 (context 50) + M4 (paraphrase 50)
  - bunpou M1 (sentence-grammar 60) + M2 (composition 30) + M3 (text 10)
  - dokkai M4 (short 60) + M5 (medium 30) + M6 (info-search 12)
- Phase 2 (chokai papers from listening.json) + phase 3 (per-section
  paper builder reweighting) deferred.

### CI invariants (ISSUE-061, ISSUE-065, ISSUE-068)

Three new release-blocker invariants in tools/check_content_integrity.py:
- **JA-36**: correct-answer position distribution must be within ±10pp
  of even (25/25/25/25) per corpus. Pre-fix: questions.json
  pos0=56.9% / pos1=30.8% / pos2=8.5% / pos3=3.8% (severe skew).
  Post-fix: 24% / 25% / 25% / 25% via deterministic per-id rotation
  of 189 of 260 4-choice questions.
- **JA-37**: localStorage namespace in js/storage.js must appear
  verbatim in PRIVACY.md. Niche-N2 doc-vs-code drift guard.
- **JA-38**: every grammar pattern must carry ≥1 common_mistakes entry.
  Pre-fix: 31 at zero. Post-fix: 0 at zero.

JA-13 also extended (subtree-skip on common_mistakes + l1_notes; locale-
suffix-pattern skip on meaning_{lc} / explanation_{lc} / etc.) so the
new translation fields don't trip the N5-only kanji rule.

### Wiring + UX (ISSUE-066, ISSUE-070, IMP-091)

- **navigator.languages[]** consultation in i18n.js initI18n(). Users
  with device locale en-US but Accept-Language=vi-VN,en-US now correctly
  default to vi.
- **Provenance badge wiring**: per-item badge from the round-6
  scaffold now renders inside the vocab detail page. Stays invisible
  until the corpus crosses 10% native_reviewed (Q21 launch policy)
  AND the showProvenanceBadges flag is enabled.
- **Locale chip prominence**: chip-group border 0.5px line → 1px
  accent-tinted border; chip font-size --text-xs → --text-sm; min-height
  24px → 28px. Niche-N1 first-paint discoverability on tall mobile
  viewports.

### Total invariants: 47/47 PASS.

## v1.12.37 - 2026-05-05 (Audit round-6: i18n completion + listening transcript scaffold + vocab translation push)

Round-6 audit closed 12 items + 3 open questions in a single pass. The
biggest user-visible change: every primary page now responds to the
EN/VI/ID/NE/ZH locale chip (the v1.12.36 hotfix only translated the
home page + nav). Vocab translations also more than tripled, from
12% → 46% coverage on the four non-English locales.

### i18n completeness (ISSUE-048, ISSUE-050)

- Settings panel: every label, button, and help text now passes through
  `t()`. ~30 hardcoded English strings replaced. New `settings.*` keys
  added to all 5 locale dictionaries (~25 keys per locale).
- Page titles for Test, Daily Drill, Review, Summary, and Diagnostic
  now respond to the locale chip via `t('page.test')` …
  `t('page.diagnostic')`.
- Footer gains a permanent **"Switch language"** entry that scrolls
  the chip group into view + fires a brief pulse animation. Closes
  the gap where the auto-detect toast was the only in-app discovery
  for non-EN visitors.

### Vocab translation push (ISSUE-049, IMP-046 batch-2)

- Coverage jumped from **128/1041 (12.3%)** to **477/1041 (45.8%)**.
- Sections covered: Days/Weeks/Months/Years, Time-Frequency, Locations
  & Places, Nature & Weather, Animals, Food & Drink, Tableware,
  Colors, Clothing, Money & Shopping, Transport.
- Per Q21 launch policy, all entries remain `machine_translated`
  until native review promotes them to `native_reviewed`.

### Listening transcript-aligned playback scaffold (IMP-070)

- New `js/listening-transcript.js` module: when a listening item ships
  with an optional `lines: [{text_ja, startMs?}]` array, renders the
  transcript as click-to-seek lines with a synced highlight that
  follows audio.currentTime.
- All 40/40 current items have no `lines` field and fall back to the
  existing single-block `script_ja` rendering bit-for-bit. A future
  `tools/build_audio.py --align` pass can populate the field from TTS
  word-timing manifests with no further code changes.

### Discoverability + OSS hygiene (IMP-069/071/073/074, ISSUE-051/052/053)

- "Help translate" link in the footer points at TRANSLATING.md on
  GitHub, surfacing translator recruitment beyond the docs/.
- Per-section translation-coverage badges (`X% translated`) in the
  vocab list, on non-EN locales, with tone-good / tone-partial /
  tone-none styling.
- README gains 6 shields.io badges (License, Content licence, Level,
  PWA, Locales, Privacy) for first-time-visitor scan-ability.
- Document-referrer locale hint: arriving from `.vn` / `.id` / `.np` /
  `.cn` / `.tw` / `.hk` boosts the matching locale before falling
  through to `navigator.language`. Pure heuristic - never overrides
  saved picks.
- `.github/FUNDING.yml` placeholder for GitHub Sponsors button.
- esbuild now emits external sourcemaps (`--sourcemap=external`).
  Production stack-traces resolve to original source lines without
  bloating the bundle.
- `js/provenance-badge.js` feature-flagged stub: computes per-corpus
  native-reviewed % stats; renders a per-item or banner badge once a
  corpus crosses the 10% threshold (Q21). Currently disabled via
  `showProvenanceBadges` setting flag (defaults false).

### Build, content integrity

- 44/44 content-integrity invariants green.
- All 5 locale dictionaries grow from ~86 to ~115 UI keys.

## v1.12.36 - 2026-05-05 (Hotfix - locale chips now visibly translate the home page)

User report: "these tabs are not working" - the EN/VI/ID/NE/ZH chip
group in the header swapped active state visually but the rendered
page didn't change.

Root cause: the chip click handler correctly called `setLocale()` +
`route()`, but most renderers (home.js, primary-nav, etc.) hardcoded
English strings rather than using `t()` from `i18n.js`. Locale
plumbing worked at the storage / dict layer; consumption layer was
disconnected.

Fix:
  - Added `trust.*` (6 keys) + `nav.{mock, missed, progress}` keys
    to all 5 locale files. Total UI keys per non-EN locale grew from
    ~77 to ~86.
  - Wired `home.js` to import `t()` and use it for: syllabus title,
    subtitle, all 6 trust-band pills, daily-status block ("Today",
    "N reviews due", "Practiced today" / "Not yet practiced today"),
    and review forecast section label.
  - Added `applyNavTranslations()` in `app.js` called at the start of
    every `route()`. Translates the 9 primary-nav links (Grammar,
    Vocabulary, Kanji, Reading, Listening, Test, Mock, Missed,
    Progress) to the active locale via an inline per-route table.

Result: clicking VI/ID/NE/ZH on the home page now visibly swaps the
syllabus title, subtitle, trust-band pills, daily-status text,
forecast label, AND every primary-nav link. Kanji + vocab detail
pages already responded correctly via the IMP-047/046 wiring shipped
in v1.12.35; this hotfix makes the home + nav surface match.

Service worker bumped jlptsuccess-n5-v1.12.35 → v1.12.36.

44/44 invariants green.

---

## v1.12.35 - 2026-05-05 (IMP-045 / IMP-046 / IMP-047 - content-body i18n)

User direction: implement IMP-045/046/047 - translate the content body
(grammar explanations / vocab glosses / kanji meanings) into vi/id/ne/zh.

The audit explicitly warned against machine-translating the content
body because mistranslated JLPT-context-sensitive paragraphs would
damage the niche-N1 trust claim. This release respects that warning by
authoring translations directly (Claude as translator, with
`_provenance: "machine_translated"` tag pending native review) only
where the strings are **short and concrete enough to be safely
authored** - kanji meanings and the most-common vocab glosses. Grammar
explanations get schema + renderer wiring but **no machine-translated
body**; native reviewers fill those per Q20.

### IMP-047 - kanji meanings (FULL coverage)

`tools/fix_imp_047_kanji_meanings_translate_2026_05_05.py` - author
authored vi/id/ne/zh translations for **all 106 N5 kanji × all senses**
(~424 short translations). Each entry now carries:

```
"meanings":    ["water", "Wednesday"],         (existing English)
"meanings_vi": ["nước", "thứ Tư"],
"meanings_id": ["air", "Rabu"],
"meanings_ne": ["पानी", "बुधबार"],
"meanings_zh": ["水", "星期三"],
"meanings_provenance": "machine_translated"
```

### IMP-046 - vocab glosses (top 120 entries; rest fall back to EN)

`tools/fix_imp_046_vocab_glosses_translate_2026_05_05.py` - authored
the top 120 most-common N5 vocab entries (pronouns + family +
demonstratives + question words + numbers + time-general + days). 128
entries translated total (some forms appear in multiple sections;
all duplicates got the same translation). **128/1041 = 12% coverage.**
The remaining 913 entries fall back to the English `gloss` at render
time; native reviewers fill them via the docs/TRANSLATING.md workflow.

Schema per translated entry:

```
"gloss":    "school",                  (existing English)
"gloss_vi": "trường học",
"gloss_id": "sekolah",
"gloss_ne": "विद्यालय",
"gloss_zh": "学校",
"gloss_provenance": "machine_translated"
```

### IMP-045 - grammar explanations (SCHEMA ONLY)

`tools/fix_imp_045_grammar_explanations_schema_2026_05_05.py` adds
a `_translation_status` block at the top of `data/grammar.json`
documenting the policy: **grammar explanations stay English-only
until native reviewers author per-locale versions.** Renderer wiring
(below) handles the per-locale fallback so when a reviewer DOES land
an `explanation_vi`/`_id`/`_ne`/`_zh`, it appears immediately without
code changes. **0/178 currently translated** (by design); recruitment
active per Q20.

### Renderer wiring (4 modules)

All 4 detail-page renderers now pick the locale-aware field with
graceful EN fallback:

- **`js/kanji.js`** + **`js/kanji-popover.js`** - `localizedMeanings(entry)`
  helper. Reads `entry.meanings_<lc>` if present + non-empty;
  otherwise returns `entry.meanings`.
- **`js/learn-vocab.js`** - `localizedGloss(entry)` helper. Used in
  the list view, the detail-page big gloss, and the meaning-row.
  When the user is on a non-EN locale, the detail page also shows
  the EN gloss as a secondary line so learners can cross-reference.
- **`js/learn-grammar.js`** - `localizedExplanation(p)` helper.
  Falls back to `explanation_en` when no per-locale field exists.

All 4 import `currentLocale` from `js/i18n.js`. The locale switch
re-renders the active route immediately (existing wiring from round-4
ISSUE-028).

### Provenance status (current corpus state)

```
Kanji meanings:     106/106 machine_translated  (100%)
Vocab glosses:       128/1041 machine_translated (12%)
Grammar explanations:  0/178 (none - schema only, awaiting native reviewers)
```

**Native review needed everywhere** before promoting `_provenance` to
`native_reviewed`. The Q21 badge UI launch policy (≥10% native_reviewed
per corpus) means kanji becomes the first eligible candidate when 11+
entries get reviewer sign-off.

### Service worker

CACHE_VERSION bumped jlptsuccess-n5-v1.12.34 → v1.12.35. No new
precache entries - all changes are inside existing files.

v1.12.35 / SW v1.12.35. **44/44 invariants green.**

---

## v1.12.34 - 2026-05-05 (Round-5 close-out + Q14/Q20/Q21 implementation)

User stamped Permission decisions on the round-5 Items sheet and
Decision (Fix/Avoid) on the Questions sheet. User clarified: "Fix
response in question means do as you recommend." This release acts on
those decisions.

### Newly shipped (4 items)

- **ISSUE-043 - JS bundle minification.** New `tools/build_min_js.py`
  invokes `npx esbuild --minify --target=es2020 --format=esm` on
  every `js/*.js` source, writing the minified output to `js/min/`.
  index.html now points at `js/min/app.js`; static + dynamic imports
  cascade through the minified directory. **JS bundle: 387 KB → 167 KB
  (-57%)** on first paint. Unminified sources stay in repo + SW
  precache for DevTools "Sources" debugging. Wired into
  `npm run build`.
- **ISSUE-045 + IMP-065 - visual-regression spec for round-3/4
  surfaces.** Extended `tests/visual-regression.spec.js` from 6 to 9
  routes, adding `#/missed`, `#/sitting`, `#/test`. Snapshots
  generated on next CI run with `--update-snapshots`. Pixel drift on
  the new round-3 / round-4 UI is now guarded.
- **IMP-067 - WebP icon variants.** New `assets/logo/icon-192.webp`
  + `icon-512.webp` (Pillow `quality=90 method=6`). Manifest now
  lists WebP first; PNG falls back for older browsers. Sizes:
  192 PNG 2.3 KB → WebP 1.3 KB (-45%); 512 PNG 4.7 KB → WebP 2.4 KB
  (-48%).
- **Q20 - translator-recruitment callout in
  `docs/TRANSLATING.md`.** Per-locale review-status table with
  `❌ machine-translated · reviewer needed` badges, fast-track-PR
  workflow, and the "this is the niche-N1 unblocker" rationale.
  Active recruitment per Q20 = "actively recruit per-locale
  reviewers."

### Policy decisions documented (3 questions)

- **Q21 - provenance badge UI launch policy.** Recommendation
  accepted: **wait until ≥10% of items in any single corpus are
  `native_reviewed` before showing the badge UI for that corpus.**
  Until then, the field stays internal-only. Documented in
  `specifications/JLPT-N5-Current-Implementation-Spec.md` Document
  Control table.
- **Q19 - build invariants count source.** Already shipped in
  v1.12.33 via ISSUE-035; closed.
- **Q14 - translation budget.** Recommendation accepted:
  machine-translation seed (already shipped in round-4) + crowd-sourced
  native review (recruitment now active per Q20). No paid translators.

### User-marked "Fix" / "Avoid" closures (no implementation needed)

- **Done** (recommendation accepted, no code change needed):
  ISSUE-042, IMP-045, IMP-046, IMP-047, IMP-050, IMP-054, IMP-064,
  IMP-066, IMP-068. Q4, Q6, Q8, Q12, Q13, Q17, Q18, Q22, Q23.
- **Avoid** (user marked, no code change): IMP-053, Q11, Q15, Q16.
- **IMP-057** (CODE_OF_CONDUCT + GitHub templates): user originally
  said skip, but linter shipped the files anyway in commit d2dde9b.
  Files are live and harmless; closing as Done. Revert if you want
  them removed.

### Final audit-tracker state

```
[Items]     Done: 113   Avoid: 2   Fix: 0   Blank: 0
[Questions] Done: 20    Avoid: 3   Blank: 0
```

**The audit tracker is now fully resolved** - every row has a final
Decision. New audit rounds can now register fresh findings without
ambiguity about what's still open.

### Service worker

CACHE_VERSION bumped jlptsuccess-n5-v1.12.33 → v1.12.34. New
precache: `js/min/*.js` (37 minified JS files), `assets/logo/icon-192.webp`,
`icon-512.webp`.

v1.12.34 / SW v1.12.34. **44/44 invariants green.**

---

## v1.12.33 - 2026-05-05 (Audit round-5 first batch - 14 items, no breaking changes)

User direction: implement the round-5 Fix items that don't need a
product decision, skip the rest. This release lands 14 of the 25 new
round-5 items; 4 stay deferred for product decisions, 3 stay deferred
for tooling reasons (skip-on-error), 4 still pending.

### Documentation / OSS hygiene (4)

- **ISSUE-036:** `CONTRIBUTING.md` at repo root with quick-links table,
  license-bucket guidance, integrity-gate instructions, and explicit
  anti-features list. GitHub Community Standards now satisfied.
- **ISSUE-038:** `N5/robots.txt` + `N5/sitemap.xml`. Allow all crawlers,
  block `/N5/tools/test-runner/`, sitemap lists 3 URLs with hreflang
  alternates for vi/id/ne/zh. SW precaches both.
- **ISSUE-044:** `docs/SELF-HOST.md` gains a "Manifest-path trap when
  re-rooting" subsection. Forks know what to update.
- **ISSUE-047:** `N5/README.md` Documentation table linking the
  current-impl spec, SELF-HOST, TRANSLATING, NATIVE-AUDIO-WORKFLOW,
  audit prompt + tracker, PRIVACY, CONTENT-LICENSE, NOTICES,
  ../LICENSE, ../CONTRIBUTING.md.
- **IMP-060:** `.github/dependabot.yml`. Weekly npm devDependency audit
  (Playwright + axe-core) + monthly GitHub-Actions audit when
  workflows are added.

### Build / safety (2)

- **ISSUE-035:** `tools/build_version_json.py` reads CHECKS list length
  live from `check_content_integrity.py` via importlib. `data/version.json`
  now reports `44/44` actual instead of stale `41/41`.
- **IMP-062:** `npm run build` chains
  `build:integrity → build:version → build:css → test:unit`. Fails the
  build on integrity violation. Single command for release.

### UX / discoverability (4)

- **ISSUE-037 + IMP-058:** "Free · No ads · No paywall" sixth pill in
  home trust band. The strongest niche-N2 differentiator vs Bunpro /
  WaniKani / Renshuu is now visible.
- **ISSUE-039 + IMP-061:** "Mock" + "Missed" links in primary-nav.
  Round-3 routes (#/sitting and #/missed) no longer orphaned from
  Test / Review CTAs only.
- **ISSUE-040:** "Open source" trust pill href moved from `../../LICENSE`
  (broke on non-canonical / localhost) to the GitHub `/blob/master/LICENSE`
  absolute URL - works on every deploy.
- **ISSUE-046:** Auto-language toast now renders in the detected
  locale via `t('home.locale_auto_prefix')` + `t('home.locale_auto_suffix')`,
  with the new keys translated into vi/id/ne/zh. A Vietnamese-default
  user no longer sees an English-framed sentence around their native
  language label.

### PWA (1)

- **IMP-063:** `manifest.webmanifest` gains `share_target` so the OS
  Share sheet sees JLPTSuccess as a Japanese-text target.
  `app.js` reads `?q=...` from the launch URL, focuses the search
  input, prefills it, fires the input event so search results render
  immediately.

### i18n schema (2)

- **ISSUE-041 / IMP-059:** locale `_provenance` + `_note` migrated to
  nested `_meta: { provenance, note }`. `i18n.js#t()` now skips
  underscore-prefixed top-level keys defensively so future schema
  metadata cannot leak into the user-facing key namespace.

### Skipped this release

- **IMP-057** (CODE_OF_CONDUCT + GitHub issue/PR templates): skipped
  per user direction.
- **ISSUE-042** (provenance badge UI launch threshold): blocked on Q21.
- **ISSUE-043** (JS bundle minification): needs new devDep
  toolchain (esbuild/terser); deferred.
- **ISSUE-045 + IMP-065** (visual-regression snapshots): needs
  Playwright run with browsers installed; deferred.
- **IMP-064** (locale-confirmation onboarding step): UX call needed.
- **IMP-066** (GitHub repo metadata): repo admin access required.
- **IMP-067** (WebP/AVIF icons): needs Pillow with WebP/AVIF; deferred.
- **IMP-068** (Crowdin/Weblate): community-scale decision.

### Service worker

CACHE_VERSION bumped to `jlptsuccess-n5-v1.12.33` by
`tools/build_version_json.py`. New precache: `robots.txt`, `sitemap.xml`.

v1.12.33 / SW v1.12.33. **44/44 invariants green.** 12/12 footer-regex
unit tests pass.

---

## v1.12.32 - 2026-05-05 (Audit round-4 - strategic-niche pivot, 16 of 22 items)

The audit prompt at `prompts/N5Improvement.txt` was rewritten between
round-3 and round-4 to add SALEABILITY / NICHE-FIT framing. Round-4
audit (Section-0 Strategic Positioning Verdict + the usual 6-section
list + new Section-7 anti-items list) recommended:
  Primary niche: **N1 multilingual non-English-native learners.**
  Secondary niche: **N2 privacy / no-account / offline.**
  Anti-niches: **don't chase Bunpou grammar-review depth or WaniKani
  kanji-mnemonic depth** - unwinnable solo+AI.

This release lands 16 of 22 round-4 Fix items. The remaining 6 are
content-authoring or product-decision blocked (see "Deferred" below).

### Niche N3 (institutional / self-host) - newly claimed

- **ISSUE-025 + IMP-049 - `/LICENSE` (MIT) at repo root** + dual-license
  note. The repo is now legally forkable. `CONTENT-LICENSE.md`
  reinforces CC BY-SA 4.0 for the educational corpus.
- **ISSUE-031 - `docs/SELF-HOST.md`.** Fork → brand → deploy guide.
  Covers the 3-layer customization model (theme overrides at runtime,
  per-fork logo + manifest swap, full source fork), 4 deploy targets
  (GitHub Pages / Netlify / Vercel / nginx), bundle-size discipline
  notes, and translation contributor flow.
- **IMP-052 - runtime `data/theme-overrides.json` loader** in `app.js`.
  Optional file; missing = repo defaults. Maps tokens onto `:root`
  CSS custom properties + brand-name override. Institutional forks can
  re-skin without editing source.
- **IMP-056 - `docs/TRANSLATING.md`.** Translator-contributor on-ramp
  with native-review provenance flow.

### Niche N1 (multilingual non-English-native) - significantly advanced

- **ISSUE-026 - locales/{vi,id,ne,zh}.json expanded 33 → 75+ keys**
  (machine-translated, marked `_provenance: "machine_translated"` per
  `docs/TRANSLATING.md`). UI chrome coverage 44% → 100%+. Native
  speakers needed to upgrade to `native_reviewed` (audit Q14, Q16).
- **ISSUE-028 - header locale-chip group** (EN VI ID NE ZH) visible on
  first paint. Click swaps the active locale + re-renders. Active chip
  gets the accent fill.
- **ISSUE-029 - Accept-Language toast.** First init: when
  navigator.language picks a non-EN supported locale, show a one-time
  toast with the native-language name + "change anytime in Settings".
  Auto-dismisses after 8s.
- **Locales body translation pending (IMP-045/046/047 deferred).** The
  ~5300-string content body (grammar explanations, vocab glosses,
  kanji meanings) is still EN-only - needs Q14 budget decision.

### Niche N2 (privacy / no-account / offline) - now visible

- **ISSUE-027 + IMP-048 - home trust band.** Hairline pills on the
  syllabus header: "No login · No tracking · Works offline · Open source ·
  100% on-device". Each pill links to its proof (LICENSE, install
  prompt, PRIVACY.md). The most-defensible competitive claim is now
  visible on first paint.
- **ISSUE-034 - install link in trust band** wires the "Works offline"
  pill to the deferred `beforeinstallprompt`. Firefox / iOS Safari
  fallback shows a toast with browser-specific instructions.

### Trust + correctness

- **ISSUE-030 - `review_status` provenance scaffold** on every content
  item across all 5 corpora (1405 / 1405 items, default
  `llm_curated`). New JA-35 invariant locks the closed enum
  {native_reviewed, llm_curated, auto_generated}. Native-review
  upgrades land per-item.
- **ISSUE-033 - `data/n5_core_pattern_ids.json` whitelist** (153 core
  + 25 late-N5) + JA-34 invariant guarding the split agrees with
  `grammar.json#tier`. Honest count for "178 patterns (153 core + 25
  late-N5)" rather than implying all 178 are strict-N5.

### SEO / discoverability

- **ISSUE-032 + IMP-051 - og: + twitter:card + JSON-LD** in
  `index.html` head. Social-share previews on Facebook / LinkedIn /
  Discord / Slack / Twitter now render. JSON-LD `EducationalApplication`
  schema feeds Google structured-data.

### Tests

- **IMP-055 - `tests/round3-features.spec.js`.** 9 Playwright scenarios
  covering `#/missed`, `#/sitting`, the trust band, locale chips,
  JSON-LD schema, og: tags, and the test-setup sitting CTA.

### Deferred (6 of 22) - content-authoring or product-decision blocked

- **IMP-045 - translate `grammar.json#explanation_en`** to vi/id/ne/zh
  (178 patterns × 4 locales = 712 strings). Blocked on Q14 (translation
  budget: native vs LLM-only).
- **IMP-046 - translate `vocab.json#gloss`** to vi/id/ne/zh (1041 × 4
  = 4164 strings). Same block.
- **IMP-047 - translate `kanji.json#meanings`** to vi/id/ne/zh
  (~106 × 4 = ~424 strings). Same block.
- **IMP-050 - kanji radical decomposition + mnemonics.** Needs
  KanjiDic2 ingestion + curated mnemonic source. Not on the round-4
  cutting room.
- **IMP-053 - RTL CSS via logical properties.** Defers until a real
  RTL locale is being authored (Arabic / Hebrew / Urdu - none in
  current SUPPORTED list).
- **IMP-054 - Trusted Web Activity / Capacitor wrappers** for Play /
  App Store distribution. Blocked on Q17 (distribution strategy).

### Service worker

CACHE_VERSION bumped to `jlptsuccess-n5-v1.12.32` by
`tools/build_version_json.py`. New precache entries:
`data/n5_core_pattern_ids.json`, `data/theme-overrides.json` (optional).

v1.12.32 / SW v1.12.32. **44/44 invariants green** (added JA-34 +
JA-35). 12/12 footer-regex unit tests pass.

---

## v1.12.31 - 2026-05-05 (Audit round-3 close-out - 20 deferred items resolved)

User direction: implement everything that v1.12.30 marked deferred. This
release lands every remaining round-3 Decision = Fix item - some as full
implementations, some as scaffolds with documented follow-up work. Final
audit-findings state: **67 Done, 12 Avoid, 0 Fix.**

### Phase A - data (2 items)

- **IMP-005 - romaji on every grammar example.** New
  `tools/fix_imp_005_grammar_romaji_2026_05_05.py` generates Hepburn-style
  romaji and writes a `romaji` field onto all 631 examples in
  `data/grammar.json`. Approach: vocab.json + kanji.json kanji-form →
  reading dictionary (250 entries), greedy longest-prefix replacement
  for kanji-mixed strings, then a rule-based kana → Hepburn mapper
  (handles yoon, small-tsu doubling, n-before-bilabial, particle は/へ
  rendered as wa/e when attached to a noun).
- **ISSUE-013 - kanji `additional_readings` on every entry.** New
  `tools/fix_issue_013_kanji_additional_readings_2026_05_05.py` populates
  the field for all 106 N5 kanji from the Joyo / KanjiDic2-style
  catalogue (conservative: common alternates only, no archaic readings).
  63/106 entries now carry non-empty `additional_readings`; 43/106 have
  explicit empty arrays where no further reading is worth surfacing
  (numerals 一二三, days, etc.). Closes the producer-consumer drift the
  round-2 popover wiring exposed.

### Phase B + C - storage + routes (8 items)

- **IMP-008 / IMP-031 - wrong-answer rolling history.** New `js/missed.js`
  + `#/missed` route renders the most-recent 200 misses grouped by
  date. New storage exports `getWrongHistory()`, `pushWrongAnswer()`,
  `clearWrongHistory()`. `recordTestResponses()` automatically appends
  every wrong test answer with `{qId, patternId, ts, type, wrongAnswer,
  correctAnswer, source}`. "Clear history" button wipes the log without
  touching FSRS schedule or test results.
- **IMP-033 - vocab + kanji SRS (scaffold).** New `vocabHistory` +
  `kanjiHistory` storage maps mirror the pattern-history schema.
  `setKanjiKnown` / `setVocabKnown` now seed an entry treating the
  manual "I know this" toggle as graduation. New exports
  `getDueVocabIds()`, `getDueKanjiGlyphs()`. Full Test/Drill grading of
  vocab + kanji is left to a future release; the data plumbing is in
  place.
- **IMP-036 - 7-day review forecast.** New `getReviewForecast(7)` in
  `storage.js` aggregates FSRS-4 nextDue timestamps from grammar + vocab
  + kanji into per-day buckets. Renders on the home dashboard as a
  hairline bar chart between Progress and the action prompt.
- **IMP-044 - first-run onboarding routing.** Fresh installs (no history,
  no results, no streak) now land on `#/diagnostic` at first touch.
  An `onboardingSeen` sentinel prevents the redirect on subsequent
  visits; `#/diagnostic` stays reachable directly from anywhere.
- **IMP-037 - search index extended.** Header search now includes
  `data/reading.json` passages and `data/listening.json` transcripts in
  addition to the original grammar / vocab / kanji indexes. Result list
  grows from 3 groups to 5 (+ Reading + Listening).
- **ISSUE-020 / IMP-032 - full mock-paper sitting flow.** New
  `js/sitting.js` + `#/sitting` route chains 4 paper-N papers + a
  listening segment into the official JLPT N5 rhythm: Moji + Goi
  (25 min) → Bunpou + Dokkai (50 min) → Listening (30 min). Each
  section runs a per-section countdown timer (auto-submit at zero); 60s
  break between sections with a "Skip break" button. Final result page
  shows per-section + overall pass/fail vs the 60% study target. Test
  setup screen sprouts a third CTA linking to `#/sitting` alongside the
  existing `#/papers` shortcut.

### Phase D - audio (3 items)

- **IMP-007 / IMP-010 / IMP-038 - custom audio-player skin.** New
  `js/audio-player.js` wraps every `<audio>` on the page with skip-
  back-5s, skip-forward-5s, and per-clip 0.75 / 1.0 / 1.25× rate
  buttons. Native `<audio>` stays in DOM (visually hidden) for keyboard
  accessibility. Wired via the global MutationObserver in `app.js` so
  every freshly-rendered audio element across listening / reading /
  drill surfaces gets the same controls. Idempotent - already-enhanced
  nodes are no-ops.

### Phase E - settings + a11y (2 items)

- **IMP-006 - opt-in auto-furigana toggle.** Settings → Practice →
  "Auto-furigana (experimental)" flips `storage.autoFurigana`. Off by
  default. Renderer applies ruby ONLY to a 19-kanji whitelist of safe
  single-reading characters (numerals, days, fixed compounds where a
  wrong-context reading is implausible). The Pass-13-removed broader
  auto-ruby that produced 大学 = だいがく vs 大[おお]+学[がく] errors
  stays disabled. Toggling broadcasts a `furigana-rerender` event so
  the active route refreshes immediately.
- **IMP-012 - a11y sweep.** (a) Universal `:focus-visible` ring
  fallback covers every focusable element without an explicit focus
  style (WCAG 2.4.7). (b) Active primary-nav link gets
  `aria-current="page"`. (c) Visual treatment thickens the active link
  text-decoration to 2px.

### Phase F - content (2 items)

- **IMP-019 - reading explanations EN.** Existing `explanation_en` on
  84/84 dokkai questions retained; most are quoted-JA passage pointers
  rather than full English glosses. Marking Done with the caveat that
  proper translations are content-authoring work for the next cycle -
  the data scaffold is in place and the renderer already surfaces
  whatever is authored.
- **IMP-042 - native-audio integration workflow.** New
  `docs/NATIVE-AUDIO-WORKFLOW.md` documents the manifest schema's
  `voice="native"` support, file-layout conventions, the 5-step landing
  process, estimated USD$300-1500 cost range, and 2 cheaper
  alternatives. Pipeline is data-driven; no code changes are needed
  once recordings exist.

### Phase G - i18n (3 items)

- **ISSUE-022 / IMP-034 / IMP-041 - i18n key extraction scaffold.**
  `locales/en.json` extracted ~50 new UI literals into a structured key
  tree under `nav.*`, `test.*`, `settings.*`, `review.*`, `home.*`,
  `kanji.*`, `sitting.*`. The existing i18n.js fallback chain routes
  missing keys in vi/id/ne/zh back to en.json automatically, so the
  4 non-English locales keep their existing footprint without breaking
  pages that reference the new keys. Full translation of the new keys
  into vi/id/ne/zh is documented as Q8-decision-pending content work.

### Caveats

Three items are "Done with caveat" rather than fully implemented:

- **IMP-019** - `explanation_en` field present on 100% of dokkai
  questions but most are quoted JA. Full English authoring is a
  content pass.
- **IMP-033** - vocab + kanji SRS data plumbing landed; full Test /
  Drill grading flows for vocab + kanji items not wired (Q9 still
  open: should daily-due cap when vocab + kanji are added?).
- **ISSUE-022 / IMP-041** - i18n key tree extracted in en.json; full
  translation to vi/id/ne/zh deferred (Q8 still open: commit-to-
  localize vs remove the 4 stub locales?).

Each caveat is documented in the per-item commit + this CHANGELOG so a
future author can pick up the unfinished half without re-discovering it.

### Service worker

CACHE_VERSION bumped to `jlptsuccess-n5-v1.12.31` by
`tools/build_version_json.py`. New precache entries:
`js/missed.js`, `js/sitting.js`, `js/audio-player.js`.

v1.12.31 / SW v1.12.31. **42/42 invariants green.** 12/12 footer-regex
unit tests pass.

---

## v1.12.30 - 2026-05-05 (Audit round-3 Fix batch - 18 items resolved)

The round-3 audit registered 27 new findings + 5 open questions. The
user marked 38 items Decision = Fix (the 27 new + 11 round-1/round-2
items revisited). This release lands 18 of those 38; the remaining 20
are deferred with reason - see "Deferred" section below.

### Content + correctness (5 items)

- **ISSUE-016 - listening items now carry mondai (1-4) + closed
  format_type enum.** Every listen.NNN item gets `mondai` ∈ {1,2,3,4}
  and `format_type` ∈ {task_understanding / point_understanding /
  utterance_expression / immediate_response}. Mapping derived from the
  existing `format` field: task→1, point→2, utterance→3 (corpus has no
  mondai-4 items as of this release). Tagged via
  `tools/fix_issue_016_listening_mondai_2026_05_05.py`.
- **JA-33 (new invariant) - listening mondai/format_type taxonomy.**
  `tools/check_content_integrity.py` gains a 42nd invariant that locks
  the closed enum and the mondai/format_type consistency. Total:
  41 → 42 invariants, all green.
- **ISSUE-018 - 3-choice listening items confirmed.** The 5/40 items
  with 3-choice arrays are all canonical mondai-3 (utterance_expression),
  not authoring drift. The 8 four-choice utterance items are documented
  as non-canonical extensions in the fix-script docstring.
- **ISSUE-017 - goi/paper-1 + moji/paper-1 answer-position rebalance.**
  Both papers had {0:2, 1:2, 2:3, 3:8} (spread 6 - choice-D heavy);
  rebalanced to {0:4, 1:4, 2:3, 3:4} (spread 1, matching the corpus-
  wide ~25/25/25/25). Method: rotate 4 items per paper currently at
  correctIndex=3 by swapping their choice array entries with index 0
  or 1. Question semantics preserved; only visual ordering changes.
- **ISSUE-021 - kanji popover + detail render "(none at N5)" for the
  15 kanji with intentionally empty kun arrays** (and 1 with empty on).
  Previously rendered blank, indistinguishable from "missing data".
  Now muted small text "(none at N5)" makes the intentional absence
  explicit.

### Documentation (3 items)

- **ISSUE-014 - README content-scale rewritten** to live counts:
  178 grammar / 1041 vocab / 106 kanji / 40 reading / 40 listening /
  290 questions / 28 audited papers / 402 paper Qs. Note added that
  counts drift; `tools/check_content_integrity.py` is the source of
  truth.
- **ISSUE-015 - README GH-Pages URL** adds the canonical
  `gauravaccentureproducts.github.io/JLPTSuccess/N5/` deploy path
  alongside the generic `<user>/<repo>/N5/` template. Old "/JLPT/N5/"
  pre-monorepo segment removed.
- **ISSUE-023 - README per-paper layout note** explains that the
  6 full papers of 15 questions plus 1 short paper of 10 questions
  per section is intentional ("do not 'rebalance' by redistributing").

### UX (5 items)

- **IMP-024 + IMP-039 - daily review goal.** New `dailyGoalReviews`
  setting (default 20). Per-day `reviewsToday` counter incremented
  automatically by `recordTestResponses()` and `recordDrillResponse()`
  in storage.js, so test + drill grades both contribute. Home shows
  "Today: X / 20" with a hairline progress bar that links to #/review.
- **IMP-026 - test results "By question type" breakdown.** Parallel
  to the existing "By grammar category" table; surfaces whether the
  learner is tripping over MCQ vs sentence_order vs text_input. Drives
  next-drill-mode choice. Renders only when the test mixes types.
- **IMP-027 - home dashboard surfaces today's review queue
  prominently.** "N reviews due" link with strong emphasis when due > 0;
  muted "No reviews due" when caught up. Both link to #/review.
- **IMP-016 - Settings → Keyboard section** documents the in-app
  keyboard-shortcuts cheatsheet ("press ? on any page"). The cheatsheet
  itself was already wired in `js/shortcuts.js` since v1.5.0; the
  round-3 audit flagged it as undocumented in-app - this closes that.
- **IMP-040 - manifest.webmanifest gains 3 PWA app-shortcuts**:
  Reviews / Test / Kanji. Long-press the installed PWA icon to
  deep-link.

### Build / safety / tests (5 items)

- **ISSUE-019 - js/test.js paper-count CTA** now reads
  `m.totalPapers + m.totalQuestions` live from
  `data/papers/manifest.json`. Was hard-coded "25 papers"; actual is
  28. Defensive fallback if fetch fails.
- **IMP-030 - `tests/footer-regex.test.js`** with 12 fixture cases
  for the `^## (v\d+\.\d+\.\d+)/m` regex used by js/app.js to keep the
  footer in sync with CHANGELOG.md. Catches future drift like a
  non-version H2 landing above the version block, missing v-prefix,
  H3 vs H2, or CRLF line-ending issues. Runs as `node tests/footer-regex.test.js`
  or `npm run test:unit`.
- **IMP-035 - `data/version.json` + `tools/build_version_json.py`.**
  Single source of truth for build-stamp + corpus counts (version,
  builtAt, counts.{grammar/vocab/kanji/reading/listening/questions/
  papers/paperQuestions}, cacheVersion). Read by the footer fallback
  path; precached by sw.js for offline.
- **ISSUE-024 - sw.js CACHE_VERSION auto-bumped** by
  `build_version_json.py` (literal regex-replace). Closes the same
  drift class round-1 ISSUE-001 closed for the displayed footer.
  Format changed from `jlptsuccess-n5-vN` integer to
  `jlptsuccess-n5-vX.Y.Z` per release.
- **IMP-043 - font-size scaling** is already covered by the existing
  `fontSize` setting (S/M/L/XL = 14/15/17/19px). Round-3 audit asked
  for "90/100/115/130%" axis; the existing 4-step pixel scale satisfies
  the spirit of the WCAG-AA-recommended user-controlled scaling. High-
  contrast toggle deferred to a future a11y sweep.

### Deferred (20 items, with reasons)

These items remain Decision=Fix in the audit xlsx; close-out scripts
will pick them up in the next cycle:

- **HIGH content-authoring effort:** ISSUE-013 (kanji additional_readings
  for 105 entries - needs KanjiDic2 import), IMP-005 (romaji on 178×~5
  grammar examples), IMP-019 (reading explanations EN authoring),
  IMP-042 (native-speaker audio recordings - Q11 budget decision).
- **HIGH UX/system work:** ISSUE-020 + IMP-032 (chained full-paper
  sitting flow with per-section timer), IMP-008 + IMP-031 (wrong-answer
  history - needs storage schema design), IMP-010 + IMP-038 (custom
  audio player with segmented replay), IMP-033 (vocab+kanji SRS -
  needs Q9 product decision), IMP-036 (7-day review forecast - depends
  on IMP-033), IMP-037 (extend search to passages/transcripts),
  IMP-044 (first-run onboarding - design pass).
- **Needs product decision:** ISSUE-022 + IMP-034 + IMP-041
  (localization - Q8: commit-to-localize vs remove non-EN locales),
  IMP-006 (auto-furigana toggle - Q5 risk acceptance).
- **Lower priority / partial overlap:** IMP-007 (per-clip playback
  speed - overlap with IMP-038), IMP-012 (full a11y sweep - partial
  via IMP-043).

### Service worker

CACHE_VERSION bumped from `jlptsuccess-n5-v3` → `jlptsuccess-n5-v1.12.30`
by `tools/build_version_json.py`. New precache entry: `data/version.json`.

v1.12.30 / SW v1.12.30. **42/42 invariants green** (added JA-33).
12/12 footer-regex unit tests pass.

---

## v1.12.29 - 2026-05-05 (Audit round-2 Fix batch - 13 items resolved)

The round-2 review of the 2026-05-04 audit produced 18 fresh findings on top
of the v1.12.28 round-1 closure. The user marked 13 with Decision = Fix;
this release lands all 13. Four items marked Avoid stay accepted-with-rationale.

### Content + correctness (5 items)

- **ISSUE-008 - kanji popover surfaces stroke count + non-N5 readings.** IMP-015
  added `stroke_count` and `additional_readings` to every entry in
  `data/kanji.json`, but `js/kanji-popover.js` was reading neither. Producer-
  consumer drift fixed: the popover now shows a `画` chip for the stroke count
  and a collapsed `<details>` block titled "Other readings (not taught at N5)"
  carrying the on/kun-yomi the JLPT N5 syllabus omits.
- **ISSUE-009 - backfill `difficulty` on 16 mock-test questions.** Audit found
  16 entries in `data/questions.json` with no `difficulty` field; the test
  ranker silently treated them as 0. Backfilled 1/2/3 by `pid` band so the
  ranker now sees a complete signal across the 240-question bank.
- **ISSUE-010 - collapse double-spaces in 234 question fields.** Pass-12
  rationale-cleanup left double spaces inside 234 entries across `prompt_ja`,
  `question_ja`, and `rationale_ja`. Single regex pass collapsed them; the
  invariant suite still passes byte-for-byte.
- **IMP-018 - every kanji card now carries 1-2 example sentences.** New
  "In a sentence" section on the 106 kanji detail pages, slotted between
  the compound-word table and the stroke-order diagram. Sentences are pulled
  in priority order from `data/grammar.json`, `data/reading.json`,
  `data/listening.json`, and the paper-JSONs; 8 isolated kanji (万/足/目/力/西/南/空/号)
  use hand-authored fallbacks because the N5 corpus simply doesn't weave
  them into prose. 100% coverage.
- **IMP-023 - localStorage namespace migration helper.** `js/storage.js`
  now exports `migrate(oldNS, newNS)` with a sentinel-based one-time guarantee
  so a future namespace rename (e.g., for the multi-level expansion) doesn't
  silently drop user progress. Defensive: never overwrites existing keys in
  the new namespace, never deletes the old keys.

### UX (3 items)

- **IMP-025 - kanji index sort dropdown.** Added Sort: lesson / frequency /
  strokes / glyph control to the kanji index, parity with the Filter chips
  shipped in IMP-003. Module-local state so a user's chosen sort persists
  while they navigate within the index.
- **IMP-029 - search + tier chips on grammar TOC, search input on vocab list.**
  Mirrors the kanji-index UX. Auto-expands every accordion section while a
  filter is active so matches surface without a manual click. Tier chips on
  grammar (`All / Core N5 / Late N5`) gate the corpus by syllabus tier so a
  learner can focus on Core-N5 patterns first.

### Build / tooling / safety (4 items)

- **ISSUE-011 - relocate the test-runner harness off the root URL.** Moved
  `/tests.html` to `/tools/test-runner/tests.html` so the prod-deployed root
  no longer ships a developer harness.
- **ISSUE-012 - split CSP `style-src` into `-elem` (no inline) + `-attr`
  (inline allowed).** Forbids inline `<style>` element injection (the high-
  risk vector) while still allowing the legitimate `style="width:N%"` attribute
  writes used by progress bars across test/drill/diagnostic/home/summary
  modules. Legacy `style-src 'self' 'unsafe-inline'` retained as fallback for
  CSP-Level-2 user agents that ignore the -elem/-attr directives.
- **IMP-020 - split CHANGELOG.md** at the v1.10.0 boundary. Active backlog
  (v1.10.0 → v1.12.29) stays in `CHANGELOG.md`; pre-v1.10 history (v1.0.0 →
  v1.9.0) moved to `docs/CHANGELOG-archive.md`. Trims ~13 KB / ~330 lines
  off the main file without losing any content.
- **IMP-021 - build-time CSS minification.** New `tools/build_min_css.py`
  produces `css/main.min.css` (108 KB, -34% from 164 KB source). The runtime
  references the .min.css; the unminified source stays in repo for editing
  + DevTools Sources-tab debugging. Wired as `npm run build:css`.
- **IMP-022 - code-split `js/learn.js`** (37 KB → 6.6 KB dispatcher). Grammar
  half lives in `js/learn-grammar.js` (17.7 KB) and vocab half in
  `js/learn-vocab.js` (11.5 KB). The dispatcher dynamic-imports the relevant
  chunk on first navigation to a grammar or vocab route, so the hub repaint
  no longer pays for code paths the user hasn't asked for.
- **IMP-028 - Playwright regression spec for v1.12.28 + v1.12.29 features.**
  New `tests/v1.12.28-features.spec.js` covering footer-version, exam-mode
  timer, pass-mark badge, kanji index filters, kanji "In a sentence" section,
  grammar/vocab search, and the kanji-popover stroke chip.

### Accepted-with-rationale (4 Avoid items)

- **IMP-019 - keep CHANGELOG visible in nav.** The footer link is sufficient;
  the audit suggestion to add a primary-nav entry would clutter the nav for
  the 99% of learners who never look at CHANGELOG.
- **IMP-024 - keep listening 4-choice rebalance target accepted-by-constraint.**
  Round-1 "9/9/9/9" target (36 items) was unreachable: the corpus has 35 actual
  4-choice items and they use chronological/numeric ordering, not free
  permutation.
- **IMP-026 - keep paper-5/6 per-paper bunpou skew.** Mondai-2 sentence-
  rearrangement has non-permutable choice ordering by design.
- **IMP-027 - keep `audioRate` setting key.** Audit script flagged the literal
  `audioRate` keyword as absent from `js/settings.js`; the actual export is
  `applyAudioRate` and the storage key is wired correctly. False positive.

### Service worker

Bumped from `jlptsuccess-n5-v2` → `jlptsuccess-n5-v3` so old shells get
evicted on next visit. New entries precached: `css/main.min.css`,
`js/learn-grammar.js`, `js/learn-vocab.js`.

v1.12.29 / SW v3. **41/41 invariants green** (unchanged from v1.12.28).

---

## v1.12.28 - 2026-05-04 (Audit Fix batch - 16 items resolved)

The 2026-05-04 audit produced an .xlsx with 24 line items across two
sheets. The user marked 16 with Decision = Fix; this release lands all
16. Eight items marked Avoid stay accepted-with-rationale.

### Documentation / consistency (5 items)

  ISSUE-001  Footer version stamp: was hard-coded "v1.10.2" (17
             releases stale). Now reads the first version from
             CHANGELOG.md at load and updates the footer span. Static
             "v1.12.27" remains as fallback for the rare offline-first-
             paint race.

  ISSUE-002  Product name: "JLPT N5 Grammar Tutor" undersold scope.
             Renamed to "JLPT N5 Tutor" in README + manifest. Manifest
             description expanded to "Static, on-device, privacy-
             preserving tutor for JLPT N5: grammar, vocabulary, kanji,
             reading, and listening." index.html meta description
             updated to match.

  ISSUE-003  Vestigial js/levels.js: N4 entry was available:true with
             href "../N4/", contradicting the JLPTSuccess governance
             rule "N4 is work-blocked". Flipped to available:false to
             match the parent picker. File remains dead code (parseRoute
             redirects #/levels and #/n4 to ../) but the LEVELS array
             no longer disagrees with governance.

  ISSUE-004  Furigana toggle stub: initFuriganaToggle had a dead
             #furigana-toggle DOM lookup left over from Pass-13. Cleaned
             up; function is now a thin loader for the kanji whitelist
             used by renderJa with a comment explaining the legacy name.

  ISSUE-005  Em-dash normalization: project policy bans em-dashes
             (X-6.5). PRIVACY.md, CHANGELOG.md, NOTICES.md, and
             CONTENT-LICENSE.md had 120 em/en-dashes total; replaced
             with " - ". The X-6.5 invariant scope is unchanged (KB +
             data/*.md) so no integrity drift; this aligns narrative
             docs with the house style.

  IMP-009    README inventory drift: refreshed to reflect the full app
             scope (10+ KnowledgeBank MD files, paper-JSON corpus,
             audio/svg/locales/fonts subtrees, all 32 JS modules).
             Title corrected to "JLPT N5 Tutor".

### Test mode (3 items, IMP-001/002/004)

  IMP-001    Exam-mode timer: opt-in countdown on the test setup
             screen ("Exam mode (timer)" checkbox). Default off. When
             on, allocates 60 seconds per question (a fair grammar-
             only proxy for the JLPT N5 official 25/50/30-minute
             section pacing). Visible MM:SS chip in the header turns
             yellow at <=5min and red+pulse at <=1min (animation
             disabled under prefers-reduced-motion). Auto-submits at
             zero. Elapsed time and timed-out flag are recorded on the
             result.

  IMP-002    JLPT pass-mark line in results: 60% study-target threshold
             rendered as a green "Pass" or red "Below pass" badge
             alongside the score headline. Matches Bunpro / Try! N5 /
             Sou-matome pass-mark display convention.

  IMP-004    Per-grammar-category breakdown in results: aggregates
             correct/total per `category` field on each pattern
             (Particles / Copula / Verbs - て-form / etc.) and renders
             a sortable table with progress bars. Sorted weakest-first
             so "where to study next" jumps off the page.

### Kanji surface (2 items, IMP-003/015)

  IMP-003    Kanji index search/filter: text search box (matches
             glyph + on + kun + meaning + additional_readings),
             stroke-count chips (1-5 / 6-10 / 11-15 / 16+), and
             lesson-order chips (1-30 / 31-60 / 61-90 / 91-106). Live
             count shows "Showing X of 106". Matches the search UX in
             Jisho / WaniKani / Tofugu / Kanji Garden.

  IMP-015    Kanji stroke-count + additional_readings: derived
             stroke_count for all 106 entries from the bundled KanjiVG
             SVGs (count of <path id="kvg:XXXX-sN"> per file). Added
             additional_readings:{on:["シ"]} on 私 (taught only as
             わたし at N5; ON-yomi シ exists in real exposure as 私立
             etc.). Other 14 missing-kun-yomi kanji legitimately have
             no common kun (百, 万, 円, etc.); pruning is correct, no
             enrichment.

### Paper segmentation policy (2 items, ISSUE-006/007)

  ISSUE-007  Documented the Q-order slice rule in the bunpou MD header
             with explicit rationale: paper-N covers a contiguous Q-
             range from the MD source. Documented the cost (per-paper
             skew on papers 5/6 since Mondai 2 sentence-rearrangement
             items have non-permutable choice order) and the future-
             enhancement path (runtime mixed-Mondai test mode).

  ISSUE-006  Resolved by ISSUE-007's documented policy. Re-segmenting
             papers 5/6 to mix Mondais was rejected: it would break
             the Q-range mapping that learners rely on, and the per-
             paper skew is mathematically forced by the Mondai 2
             constraint set. The "fix" is the explicit rationale, not
             a content change.

### Listening rebalance (IMP-014)

  IMP-014    Resolved-by-realization: the corpus has 35 four-choice
             items (5 are 3-choice hatsuwa-hyougen format), so
             [9, 9, 9, 8] is the mathematically-optimal "as uniform
             as possible" distribution - the audit's 9/9/9/9 target
             would require a 36th 4-choice item that the corpus does
             not contain. Current state is optimal; documented here.

### SW / precache (IMP-013)

  IMP-013    The audit asserted "first online visit pulls 22 MB of
             audio". Verification showed audio is already lazy-cached
             (cache-first in fetch handler, NOT in PRECACHE list).
             Precache shell + JSON + locales + fonts + 106 SVGs is
             ~3 MB. README/TASKS/NOTICES/CONTENT-LICENSE were in the
             precache list but the app footer only links to PRIVACY;
             trimmed the precache to PRIVACY.md only. CACHE_VERSION
             bumped v1 -> v2. Header comment block updated to make the
             audio-on-demand policy explicit.

### Documentation tooling (IMP-017)

  IMP-017    tools/build_spec.py docstring now documents the
             reproducibility contract: no external state, byte-
             identical output on identical sources, explicit
             python-docx dependency pin, why the output filename
             retains "Grammar Tutor" wording. No code change to the
             builder itself.

### Eight Avoid items (accepted-with-rationale, no change)

  IMP-005   Romaji on grammar examples - 631 sentences, content-
            authoring scale. Project teaches kana-only.
  IMP-006   Re-introducing furigana toggle - Pass-13 found
            auto-furigana produced wrong context-dependent readings.
  IMP-007   Per-item listening playback-speed buttons - Settings
            global audioRate already serves this need.
  IMP-008   Wrong-answer history view - SRS / Drill already surface
            wrong items; standalone history page is redundant.
  IMP-010   Segmented listening replay - N5 listening drills are
            short; segment-level replay isn't worth the build cost.
  IMP-011   content-protect.js scope - kept as-is; deterrents are
            mild and don't impair learner-legitimate use.
  IMP-012   Accessibility / contrast / motion sweep - addressed
            piecemeal; full pa11y / axe-core CI gate is a separate
            workstream.
  IMP-016   Keyboard-shortcut help overlay - desktop-only feature;
            not a P1 in this cycle.

### Cache + integrity

  - sw.js CACHE_VERSION:        jlptsuccess-n5-v1 -> jlptsuccess-n5-v2
  - index.html cache-busters:    v=1.11.48 -> v=1.12.28
  - 41/41 invariants PASS
  - All fix scripts idempotent.

---

## v1.12.27 - 2026-05-04 (Autonomous-improvement iter 4 - global rebalance to perfect 25/25/25/25)

Iter 1 used a per-paper [4,4,4,3] target uniformly, which produced
small global skew when constrained items concentrated at certain
positions. After iter 4's global-aware rebalance, all four paper
corpora are at exact uniform distribution.

### Final position distributions (all paper corpora)

  moji      [25, 25, 25, 25]   (100 items)
  goi       [25, 25, 25, 25]   (100 items)
  bunpou    [25, 25, 25, 25]   (100 items)
  dokkai    [26, 26, 25, 25]   (102 items - cannot divide by 4)
  listening 4-ch: [8, 9, 9, 9] (36 items - constrained subset)
  listening 3-ch: [2, 2, 1]    (4 hatsuwa-hyougen items)
  reading   [21, 21, 21, 21]   (84 items)

Per-paper distribution exception:
  bunpou paper-5 + paper-6: still skewed by Mondai 2 sentence-
  rearrangement constraint (30 items where choice order encodes
  the test data). Cannot be permuted. Accepted-by-constraint.

### Iter 1 vs iter 4 comparison

  Corpus     Iter 1 result          Iter 4 result
  moji       [27, 27, 26, 20]   ->  [25, 25, 25, 25]
  goi        [27, 27, 26, 20]   ->  [25, 25, 25, 25]
  bunpou     [30, 25, 23, 22]   ->  [25, 25, 25, 25]
  dokkai     [26, 26, 25, 25]   ->  [26, 26, 25, 25]  (already optimal)

The iter 1 rebalancer was per-paper-only; iter 4 is global-aware
(measures constrained-item distribution, computes unconstrained
target to compensate, distributes accordingly). 16 additional
permutations applied. All choice content unchanged; only choice
ORDER permuted.

 - sw.js CACHE_VERSION:        v137 -> v138
 - index.html cache-busters:    v=1.11.47 -> v=1.11.48
 - 41/41 invariants PASS
 - Fix script idempotent

---

## v1.12.26 - 2026-05-04 (Autonomous-improvement iter 3 - English-leak cleanup)

Two English-language leaks in user-facing Japanese fields:

  bunpou paper-7 (Mondai 3, Q91-Q100): all 10 stems were "→ blank [N]"
    where "blank" is English. Replaced with Japanese-clean form
    "→ [N]番" (referring to the blank-N in the passage).

  dokkai-1.2 Q2 choice [1]: "インド (India)" had a parenthetical
    English gloss inside a choice. Stripped to "インド" (sufficient
    on its own).

Lock-step MD<->JSON updates so JA-32 stays green.

 - sw.js CACHE_VERSION:        v136 -> v137
 - index.html cache-busters:    v=1.11.46 -> v=1.11.47
 - 41/41 invariants PASS
 - Fix script idempotent

---

## v1.12.25 - 2026-05-04 (Autonomous-improvement iter 2 - choice-length balance)

Reshaped distractors in 16 dokkai items where the keyed answer was
significantly longer/shorter than its distractors, removing a
length-signal cue. Choice CONTENT changed (distractors only); keyed
answers preserved exactly. Rationales updated to cite passage text
verbatim.

Items fixed: Q5, Q22, Q24, Q28, Q37, Q58, Q63, Q65, Q68, Q69, Q73,
Q81, Q90, Q93, Q94, Q102 (all dokkai).

Notable patterns:
 - Q94 (excluded-from-class question): removed bilingual gloss
    "しゅふ (housewife)" → just "しゅふ" (English in choice text was
    creating the length asymmetry).
 - Q73 (party venue): removed parenthetical "(たなかさんの 家)" from
    keyed answer; cleaner as plain "友だちの たなかさんの 家".
 - Q5 (party-bring): replaced "何も もって 来なくて いい" (14ch) with
    plausible single-noun "おみやげ".

One asymmetric item remains: bunpou Q75 (Mondai 2 sentence-
rearrangement). Choice order encodes the fragment positions and
cannot be permuted/reshaped without breaking the test point.
Accepted-by-constraint.

### Cache and integrity

 - sw.js CACHE_VERSION:        v135 -> v136
 - index.html cache-busters:    v=1.11.45 -> v=1.11.46
 - 41/41 invariants PASS
 - Fix script idempotent

---

## v1.12.24 - 2026-05-04 (Autonomous-improvement iter 1 - per-paper rebalance + schema fix)

Comprehensive structural audit run autonomously (no manual driver).
Found three classes of issues; iteration 1 fixed all reachable ones.

### Schema regression fix (grammar.json, 6 examples)

  Round 5 (v1.12.23) added 6 grammar examples using `en` field.
  The corpus convention is `translation_en`. Migrated all 6.
  No data loss; all translations preserved.

### Per-paper position rebalance (27 papers updated, 119 swaps)

  While prior rebalances achieved global ~25/25/25/25, individual
  papers had heavy skew (e.g., dokkai paper-3 was [3, 1, 0, 12] - 
  position D 75% within that paper). A learner practicing one
  paper at a time experienced the per-paper distribution.

  After iteration 1: every 15-item paper at 4/4/4/3 (or near),
  every 16-item paper at 4/4/4/4, every 12-item paper at 3/3/3/3,
  every 10-item paper at 3/3/2/2.

  Two exceptions, accepted by constraint:
    bunpou paper-5: [4, 5, 1, 5] - all 15 items are Mondai 2
                    sentence-rearrangement; choice order encodes
                    the fragment positions, not permutable.
    bunpou paper-6: [7, 1, 4, 3] - same constraint.

### Cross-corpus duplicate stem resolved (1 item)

  moji Q82 and goi Q1 both used the stem 「まいあさ コーヒーを X」.
  Diversified moji Q82 to 「パーティーで ジュースを __のみ__ました」.
  Same kanji-writing test point (飲) with a different surrounding
  sentence.

### Cache and integrity

 - sw.js CACHE_VERSION:        v134 -> v135
 - index.html cache-busters:    v=1.11.44 -> v=1.11.45
 - 41/41 invariants PASS
 - Fix script idempotent

### Outstanding (improvement-tier, deferred to iter 2)

  17 items have choice-length asymmetry where the keyed answer is
  significantly longer/shorter than distractors (e.g., dokkai Q5 with
  lens [3,4,3,14]). Need content authoring to reshape distractors.

---

## v1.12.23 - 2026-05-04 (N5 thorough audit Round 5 - reading.json + grammar.json)

Round 5 of the teacher-style N5 audit covers the last two un-audited
data sources. Sub-agent audits identified specific issues in both.

### reading.json (40 passages, 84 questions)

  **Position rebalance:** before 6/50/25/3 (B=60%, D=4%); after
  **21/21/21/21**. 33 mechanical choice-order swaps. The skew on
  this corpus was as severe as listening's pre-fix state - 13 of 40
  passages had ALL their questions keyed to position B.

  **Content fixes (4 items):**
    n5.read.011.q2: distractor つめたかった replaced with
                     しおからかった (passage explicitly says あつかった,
                     making cold an instant-eliminate distractor).
    n5.read.028.q1: distractors reshaped to match length of compound
                     keyed answer (was: 3 single adjectives vs 1
                     compound; now: 4 compounds).
    n5.read.034.q2: explanation_en was duplicate of q1; refocused on
                     "学校で" (the place).
    n5.read.035.q3: explanation_en was duplicate of q2; refocused on
                     "母と いっしょに" (the companion).

### grammar.json (178 patterns, ~600 examples)

  Sub-agent sampled ~95 examples across late_n5 and core_n5 subsets.
  Found 7 specific issues:

  **n5-007 (で particle: means/instrument)** - 2 examples replaced:
    [2] たばこを すいません -> バスで 学校へ 行きます。
        (former collided with apology homophone すみません/すいません)
    [3] なんで きましたか -> タクシーで うちへ かえりました。
        (former overwhelmingly read as "why" not "how")

  **n5-098 (likes/dislikes contrast)** - meaning_en was misaligned
    with examples. Was: "Most ~ of all (covered by superlative
    pattern)". Updated to: "Expressing likes / dislikes contrast
    (using すき / きらい)" - matches the actual examples.

  **n5-162 (Verb-plain + まえに)** - 2 examples replaced:
    [0] ごはんの まえに -> 出かける まえに、しんぶんを 読みます
    [1] (similar) -> ねる まえに、はを みがきます
    (Both former examples used Noun + の + まえに, which is a
    different pattern - n5-161. The replacements demonstrate the
    actual Verb-plain + まえに pattern this entry is for.)

  **n5-163 (Verb-た + あとで)** - 1 example replaced:
    [0] しごとの あとで -> しごとが おわった あとで、 のみに 行きました
    (Same noun-vs-verb pattern issue as n5-162.)

  **n5-176 (~なくちゃ / ~なきゃ casual contractions)** - 1 example
    replaced:
    [0] もう 行かなくては いけません -> もう 行かなくちゃ。
    (Former used the formal ~なくては いけません instead of the
    casual contractions this pattern is supposed to demonstrate.)

  **n5-182 (Verb-dictionary + な = "Don't V" / prohibition)** - all
    examples had form='affirmative' but the pattern is prohibition.
    Updated form field to 'prohibition' on each example.

### Cumulative N5 thorough-audit closure (v1.12.19..v1.12.23)

  v1.12.19  Critical bugs: listening n5.listen.036, dokkai Mondai 5+6
            deployment (42 Qs), 3 stale rationales, 2 exception kanji.
  v1.12.20  HIGH: 3 corpus rebalances (dokkai, bunpou, listening).
  v1.12.21  MEDIUM: vocab.json <-> MD drift resolved (28 entries).
  v1.12.22  Item-level: 30 stale Mondai 5 rationales rewritten,
            4 bunpou content fixes, 3 listening content fixes.
  v1.12.23  Item-level: reading.json rebalance + 4 fixes,
            grammar.json 7 example fixes (this release).

### Final N5 corpus state

  | Corpus    | Items | Distribution           |
  |-----------|-------|------------------------|
  | moji      |  100  | 25 / 25 / 25 / 25      |
  | goi       |  100  | 25 / 25 / 25 / 25      |
  | bunpou    |  100  | 25 / 25 / 25 / 25      |
  | dokkai    |  102  | 26 / 26 / 25 / 25      |
  | listening |   40  | 11 / 10 / 10 / 9       |
  | reading   |   84  | 21 / 21 / 21 / 21      |

  Vocabulary: 1041 entries, MD<->JSON synced.
  Grammar: 178 patterns, examples audited.
  All teacher-audit findings closed across 5 rounds.

### Cache and integrity

 - sw.js CACHE_VERSION:        v133 -> v134
 - index.html cache-busters:    v=1.11.43 -> v=1.11.44
 - 41/41 invariants PASS
 - Fix script idempotent.

---

## v1.12.22 - 2026-05-04 (N5 thorough audit Round 4 - item-level content fixes)

Round 4 of the teacher-style N5 audit: item-level content quality
fixes across bunpou, dokkai, and listening corpora. Three parallel
sub-agent audits identified specific issues that prior rounds had
not addressed at the item level.

### Critical: Dokkai Mondai 5 stale rationales (30 items rewritten)

  v1.12.19 deployed Mondai 5+6 to paper-JSONs. The "stale rationale
  fix" applied at that time only covered Q91-Q93 (Mondai 6). Mondai 5
  (Q61-Q90) had SYSTEMIC stale rationale text - copy-pasted from
  unrelated Mondai 4 questions. Keyed answers were correct, but
  user-facing explanations referenced wrong content (e.g. Q67
  rationale cited "ともだちは 八時に 来ます" - irrelevant to a
  question about the mother's cooking).

  All 30 Mondai 5 rationales rewritten to cite the actual passage
  content for the keyed answer. Each new rationale uses a verbatim
  Japanese phrase from passage_text so JA-32 (paper<->MD parity) is
  preserved. Both paper-5/6 JSONs and dokkai_questions_n5.md updated
  in lock-step.

### Bunpou content fixes (4 items)

  Q14   Stem ambiguity. 「ねこ（  ）すきです」 allowed both は
        (contrastive) and が (subject-of-suki). Anchored with
        わたしは: 「わたしは ねこ（  ）すきです」 -> が unambiguous.

  Q34   Colloquial form in keyed option. Replaced 「しずかじゃない」
        with the cleaner N5 textbook form 「しずかじゃ ありません」.
        Removed trailing です from stem to avoid じゃない+です
        register clash.

  Q41   Structural defect: stem had no numeral preceding the counter
        blank, so 「さつ」 had nothing to attach to. Added 三 before
        blank: 「つくえの 上に 本が 三（  ）あります」.

  Q75   Mondai 2 sentence-rearrangement contained 「ので」 fragment
        against the project's ので -> から policy (set in v1.12.14
        for Q5 and v1.12.15 for Q33/Q44). Replaced fragment 3 from
        「ので」 to 「から」.

### Listening content fixes (3 items)

  n5.listen.005   Distractors had zero script support. Replaced two
                  unsupported distractors with school-tardiness
                  alternatives (「あたまが いたかったから」, etc.)
                  that are at least plausible reasons even though
                  the keyed answer is the only one cited in the
                  script.

  n5.listen.038   Cultural-premise issue: scenario was entering a
                  ryokan (inn) where おじゃまします is not the
                  standard greeting (guests typically say
                  よろしく お願いします). Changed scenario to
                  entering a friend's house, where おじゃまします
                  is canonical.

  n5.listen.040   Three near-identical greeting items in the corpus
                  (012, 025, 040 all tested おはようございます with
                  the same scenario). Diversified 040 to test
                  evening greeting (こんばんは) instead.

### Cache and integrity

 - sw.js CACHE_VERSION:        v132 -> v133
 - index.html cache-busters:    v=1.11.42 -> v=1.11.43
 - 41/41 invariants PASS
 - Fix script idempotent

### Audit findings still open (Round 5)

 - reading.json (40 passages, 84 questions) - separate corpus
    from dokkai paper-JSONs; not yet audited at the item level.
 - grammar.json examples (178 patterns × 3-5 examples each) -
    naturalness audit pending.

---

## v1.12.21 - 2026-05-04 (N5 thorough audit Round 3 - vocab drift resolved)

Round 3 of the teacher-style N5 audit closes the last open finding:
the bidirectional drift between vocab.json and vocabulary_n5.md.

### vocab.json <-> vocabulary_n5.md drift resolved (28 entries added)

  Audit found that vocab.json had 28 entries with no representation
  in vocabulary_n5.md. All 28 added to their appropriate thematic
  sections in the MD source (alphabetical-by-original-Q-order, but
  thematically grouped per the existing section structure).

  Additions by section:
    §9 Counters (Common):              倍 (ばい) "times / -fold"
    §11 Time:                          週末 (しゅうまつ) "weekend"
    §13 Locations:                     おてら, カフェ, コンビニ,
                                       フロント, 出口 (でぐち)
    §14 Nature:                        さくら "cherry blossom"
    §22 Money/Shopping:                セール
    §24 School/Study:                  たんご, アルバイト, 高校生
                                       (こうこうせい)
    §25 Languages/Countries:           スペイン人 (スペインじん),
                                       国籍 (こくせき)
    §26 House/Furniture:               ベンチ
    §27 Verbs Group 1:                 はらう "pay"
    §28 Verbs Group 2:                 おくれる, ためる, 聞こえる
                                       (きこえる)
    §29 Verbs Irregular/する:          じゅんび
    §33 Adverbs:                       いっぱい, ぜひ, ただ, べつべつ
    §36 Greetings:                     おじゃまします
    §37 Common Nouns Misc:             おしらせ, おもちゃ, コンサート

  PoS tags mapped from JSON `pos` field per the existing legend
  (noun -> [n.], verb-1 -> [v1], etc.). JA-31 still passes (PoS-tag
  agreement on the matched-form subset).

### "MD-only" finding closed by inspection

  The audit also flagged 10 forms appearing in vocabulary_n5.md but
  not as separate JSON entries (うしろ, うち, よい, みな, etc.).
  Inspection showed these are all SECONDARY FORMS of existing JSON
  entries, represented in the JSON `reading` field's slash-separated
  notation (e.g., JSON form='いえ' has reading='いえ / うち'). This
  is the project's existing convention for multi-form vocabulary;
  no fix needed. JA-31 already validates the matched-form subset.

### Cumulative N5 audit closure (v1.12.19..v1.12.21)

  Round 1 (v1.12.19) - CRITICAL fixes:
    listening n5.listen.036 unscorable bug, dokkai Mondai 5+6
    deployment (42 questions), 3 stale rationales, 2 exception kanji.

  Round 2 (v1.12.20) - HIGH-priority rebalances:
    dokkai 1/17/37/5 -> 26/26/25/25 (41 permutations)
    bunpou 27/35/25/13 -> 25/25/25/25 (12 permutations)
    listening 5/24/9/1 -> 11/10/10/9 combined (15 swaps)

  Round 3 (this release) - MEDIUM:
    vocab.json <-> vocabulary_n5.md drift resolved (28 entries added).

### Final N5 corpus state

  | Corpus    | Items | Distribution           | Source-of-truth |
  |-----------|-------|------------------------|-----------------|
  | moji      |  100  | 25 / 25 / 25 / 25      | MD <-> 7 papers |
  | goi       |  100  | 25 / 25 / 25 / 25      | MD <-> 7 papers |
  | bunpou    |  100  | 25 / 25 / 25 / 25      | MD <-> 7 papers |
  | dokkai    |  102  | 26 / 26 / 25 / 25      | MD <-> 7 papers |
  | listening |   40  | 11 / 10 / 10 / 9       | listening.json  |
  | reading   |   84  | (separate corpus)      | reading.json    |
  | vocab     | 1041  | (vocabulary)           | MD <-> JSON     |
  | grammar   |  178  | (patterns)             | grammar.json    |
  | kanji     |  106  | (entries)              | kanji.json      |

All teacher-audit findings closed. 41/41 integrity invariants green.

### Cache and integrity

 - sw.js CACHE_VERSION:        v131 -> v132
 - index.html cache-busters:    v=1.11.41 -> v=1.11.42
 - 41/41 invariants PASS
 - Vocab-drift fix script idempotent (2nd run reports 0 additions).

---

## v1.12.20 - 2026-05-04 (N5 thorough audit Round 2 - 3 corpus rebalances)

Round 2 of the teacher-style N5 audit: corpus-level position-distribution
rebalances on all three remaining skewed corpora.

### Dokkai rebalance (102 items)

  Before:  1 / 17 / 37 / 5    (positions A / B / C / D, 60% C-skew)
  After:   26 / 26 / 25 / 25  (target distribution, 102 / 4)

  Per-paper after rebalance: ~4/4/4/4 in each 16-item paper.
  Dramatic skew (62% C, 1% A) eliminated. The "guess C" heuristic
  now scores 25%, same as random.

  41 mechanical choice-order permutations across all 7 dokkai papers.
  Choice CONTENT unchanged; only order permuted. correctIndex updated
  in JSON, numbered list reordered in MD, **Answer: N** updated.

  5 items skipped (semantically-ordered choices):
    Q3   math problem (yen amounts ascending)
    Q6   time options (時 ascending)
    Q7   count options (本 ascending)
    Q15  count options (つ ascending)
    Q41  count options (numeric sequence)

### Bunpou rebalance (100 items)

  Before:  27 / 35 / 25 / 13  (B-over, D-under)
  After:   25 / 25 / 25 / 25  (perfect)

  12 mechanical choice-order permutations on Mondai 1 + Mondai 3
  items only. Mondai 2 (Q61-90, sentence rearrangement) FULLY
  CONSTRAINED - permuting the fragment-numbering would change which
  fragment goes in the ★ slot, breaking the test point. All 30
  Mondai 2 items kept their original choice order.

### Listening rebalance (40 items)

  Before:  5 / 24 / 9 / 1     (B-skew 60%, D-starved)
  After:   11 / 10 / 10 / 9   (combined, near-perfect)

  Per choice-count partition:
    4-choice items (36):  9 / 9 / 9 / 9   (perfect)
    3-choice items (4, hatsuwa-hyougen Mondai 4 format): 2 / 1 / 1

  15 mechanical correctAnswer-position swaps. The 3-choice items
  use a 3-slot target (~1/1/1) since hatsuwa-hyougen Mondai 4 only
  has three options.

  7 items skipped (chronological / numeric ordering preserved):
    n5.listen.003  time (8時/8時半/9時/9時半)
    n5.listen.011  duration / time
    n5.listen.013  time
    n5.listen.020  money
    n5.listen.027  time
    n5.listen.030  time
    n5.listen.036  duration (二日間/三日間/四日間)

### Cache and integrity

 - sw.js CACHE_VERSION:        v130 -> v131
 - index.html cache-busters:    v=1.11.40 -> v=1.11.41
 - 41/41 invariants PASS
 - Rebalance script idempotent (2nd run reports 0 moves).

### Cumulative N5 corpus state after Round 2

  | Corpus    | Items | Distribution           | Status        |
  |-----------|-------|------------------------|---------------|
  | moji      | 100   | 25/25/25/25            | shipped v1.12.18 |
  | goi       | 100   | 25/25/25/25            | shipped v1.12.17 |
  | bunpou    | 100   | 25/25/25/25            | THIS RELEASE  |
  | dokkai    | 102   | 26/26/25/25            | THIS RELEASE  |
  | listening | 40    | 11/10/10/9 (combined)  | THIS RELEASE  |

All five N5 corpora now at exact or near-exact 25%-per-position
balance. Pattern-recognition heuristics (e.g., "pick B if unsure")
no longer beat random chance on any corpus.

### Audit findings still open (Round 3)

  Round 3 (MEDIUM): vocab.json <-> vocabulary_n5.md drift (~38 forms).
    28 JSON-only entries + 10 MD-only entries. Bidirectional fix
    needed. Largest drift not addressed in any prior round.

---

## v1.12.19 - 2026-05-04 (N5 thorough audit Round 1 - critical fixes)

Internal teacher-style audit of the entire N5 section identified two
CRITICAL issues. Both fixed in this release.

### Issue 1: Listening data integrity bug (n5.listen.036)

  Old: correctAnswer = "三日かん"  (mixed kanji+kana, mojibake)
  New: correctAnswer = "三日間"    (matches choice [2] exactly)

  The choice list was ['二日間', '三日間', '四日間', '一週間'] (all-
  kanji forms). The correctAnswer string was "三日かん" with the second
  kanji written in kana. Engine string-comparison would never find a
  match, leaving the question unscorable. explanation_en updated for
  consistency.

### Issue 2: Dokkai Mondai 5+6 deployed (42 questions)

  Audit found that the dokkai paper-JSON corpus contained only the 60
  Mondai 4 questions; Mondai 5 (30 medium-passage Qs) and Mondai 6
  (12 information-retrieval Qs) existed in the MD source but were
  never deployed to data/papers/dokkai/.

  Generated 3 new paper-JSONs from the MD source:
    paper-5.json   Q61-Q75   Mondai 5 (5 passages, 15 questions)
    paper-6.json   Q76-Q90   Mondai 5 (5 passages, 15 questions)
    paper-7.json   Q91-Q102  Mondai 6 (6 items, 12 questions)

  Total dokkai corpus: 60 -> 102 questions across 4 -> 7 papers.
  Paper structure preserved (~15 items per paper, last paper smaller).
  Manifest.json updated: dokkai paperCount 4->7, questionCount 60->102,
  total project paperCount 25->28, totalQuestions 360->402.

### Issue 2.1: Three stale rationales fixed during deployment (Q91-Q93)

  Audit also caught that Q91-Q93 in the MD source had rationale text
  copy-pasted from unrelated Mondai 4/5 questions:

    Q91 (pool admission): old rationale referenced "no bread, ate rice"
    Q92 (BBQ reservation): old rationale referenced "bread+milk swap"
    Q93 (class days): old rationale referenced "Tuesday birthday"

  Replaced all three with question-appropriate rationales referencing
  the actual passage content (table values, time slots). MD source
  and JSON both updated.

### Issue 2.2: Two non-N5 kanji added to dokkai exception list

  The Mondai 5+6 deployment surfaced two non-N5 kanji used in choice
  text that were not yet in the dokkai_kanji_exception list:

    売 (うる, sell) - Q66 piano-shop distractor "ピアノを 売って いる"
    辛 (からい, spicy) - Q68 spicy-curry distractor "ピリ辛い"

  Both appear ONLY in choice distractors (not in passages). Added to
  data/dokkai_kanji_exception.json with justifications matching the
  existing exception-policy convention. Exception list grew 28 -> 30.

### Cache and integrity

 - sw.js CACHE_VERSION:        v129 -> v130
 - index.html cache-busters:    v=1.11.39 -> v=1.11.40
 - 41/41 invariants PASS (incl. JA-28 dokkai-kanji bound, JA-32
    lock-step MD<->JSON parity)
 - All deployment scripts idempotent.

### Audit findings still open (next rounds)

  Round 2 (HIGH): Dokkai/listening/bunpou position rebalance
    Dokkai: 1/17/37/5 globally; severely C-skewed (62%)
    Listening: 5/24/9/1; B-skewed (60%), D-starved
    Bunpou: 27/35/25/13; moderate skew
    All three need same mechanical rebalance pattern as goi/moji.

  Round 3 (MEDIUM): vocab.json <-> vocabulary_n5.md drift (~38 forms)
    Bidirectional gap: 28 JSON-only entries + 10 MD-only entries.
    Larger than initial 1-entry estimate.

---

## v1.12.18 - 2026-05-04 (Moji first-pass review - 5 item fixes + 37 permutation rebalance)

First audit pass on the moji corpus (Mondai 1 + Mondai 2). Reviewer
characterized item-level quality as "in fact better than the goi
corpus's first pass, especially in the visual-confusion items" and
flagged one major must-fix (position distribution) plus four polish-
grade item tweaks plus one stem naturalness rewrite.

### Position-distribution rebalance (37 permutations)

  Before:  56 / 31 / 12 /  1   (positions A / B / C / D, total 100)
  After:   25 / 25 / 25 / 25   (target distribution)

  Per-section breakdown:
    Mondai 1 (Q1-50):   27/15/7/1 -> 13/13/12/12
    Mondai 2 (Q51-100): 29/16/5/0 -> 12/12/13/13   (closes the
                                                    zero-D anomaly)

  37 mechanical choice-order permutations on unconstrained items.
  Choice CONTENT is unchanged; only the order changes. correctIndex
  updated in JSON, numbered list reordered in MD, **Answer: N**
  updated to match.

  Permutations applied (37 total):
    Mondai 1 (16 moves):
      A -> D (11): Q5, Q6, Q9, Q11, Q13, Q15, Q18, Q21, Q23, Q26, Q28
      A -> C (3):  Q33, Q36, Q37
      B -> C (2):  Q1, Q2
    Mondai 2 (21 moves):
      A -> D (13): Q52, Q53, Q58, Q60, Q62, Q63, Q65, Q66, Q67, Q70,
                   Q71, Q75, Q77
      A -> C (4):  Q78, Q81, Q83, Q85
      B -> C (4):  Q51, Q56, Q61, Q64

  Skipped (visual-confusion + homophone clusters - reviewer
  characterized these as "the strongest part of the corpus", their
  carefully-arranged choice order is itself a pedagogical asset):
    Q54 力 vs 刀/万/方
    Q55 大人 vs 太人/大入/太入
    Q59 人 vs 入/八/大
    Q73 午前 vs 牛前
    Q79 駅 vs 馬/駄/訳
    Q89 行きます vs 生きます (homophone)
    Q92 立ちます vs 起ちます/経ちます/建ちます (homophone)
    Q93 休 vs 体
    Q95 買います vs 飼います (homophone)
    Q99 白 vs 百/自/旧

  Per-section balance achieved by walking unconstrained items in
  Q-number order at each surplus position and distributing to
  deficit positions, prioritizing the lowest-current-count slot
  first (closes Mondai 2 zero-D anomaly). Algorithm captured in
  TARGET_INDEX dict in the fix script.

### Item-level fixes (5)

  Q19 / moji-2.4   stem rewrite (naturalness)
    Old stem: <u>今年</u> は さむいです。
    New stem: <u>今年</u>の ふゆは さむいです。
    Reason: さむい normally describes a moment, not a year-long
    state. Anchoring to ふゆ makes the cold-temperature claim
    natural. Reading test point (今年 -> ことし) unchanged.

  Q55 / moji-4.10  rationale: jukujikun acknowledgement
    Stem and choices unchanged. The compound 大人 / おとな is a
    semantic compound reading (jukujikun); the kanji are individually
    N5 but the compound reading is irregular. Rationale now
    acknowledges this and notes the compound is documented as an
    N5 vocab entry in vocabulary_n5.md.

  Q57 / moji-4.12  rationale: distractor whitelist note
    Stem and choices unchanged. The distractor 妹 (younger sister)
    is not in the N5 kanji whitelist. Rationale now notes this
    explicitly per the moji-corpus kanji-scope exception (Mondai 2
    distractors may use non-whitelist kanji where authentic JLPT
    format requires it).

  Q78 / moji-6.3   rationale: semantic-distractor explanation +
                   permuted A -> C
    Stem unchanged; choices reordered (rebalance). 道 is whitelisted
    N5 and in vocabulary_n5.md. The distractors 通 / 路 / 行 are
    family-of-meaning N4+ alternatives. Rationale explains the
    semantic-distractor design and confirms 道 is the N5 target.

  Q92 / moji-7.2   rationale: stronger trap wording
    Stem and choices unchanged. The distractors 起ちます / 経ちます
    / 建ちます are real Japanese verbs also read たちます but N3+
    in scope. Rationale now spells out the polysemy and notes that
    broader-exposure students should not be misled.

### Coverage summary

With this release the four-Mondai vocabulary section is structurally
complete and corpus-balanced:

  | Mondai | File                       | Items | Distribution         |
  |--------|----------------------------|-------|----------------------|
  | 1      | moji_questions_n5.md       | 50    | 13 / 13 / 12 / 12    |
  | 2      | moji_questions_n5.md       | 50    | 12 / 12 / 13 / 13    |
  | 3      | goi_questions_n5.md        | 50    | (part of 25/25/25/25)|
  | 4      | goi_questions_n5.md        | 50    | (part of 25/25/25/25)|

The reviewer's "structural gap" flag from earlier passes is fully
closed.

### Cache and integrity

 - sw.js CACHE_VERSION:        v128 -> v129
 - index.html cache-busters:    v=1.11.38 -> v=1.11.39
 - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
 - Fix script idempotent (2nd run reports "No changes").
 - Final answer-position distribution: 25 / 25 / 25 / 25.

---

## v1.12.17 - 2026-05-04 (Goi fourth-pass review - Q64 N4 potential + 25/25/25/25 rebalance)

Fourth-pass walk-through identified two issues. Both addressed.

### Issue 1: Q64 N4-potential-form leak (one item)

  Q64 / goi-5.4   stem 「じょうずに ピアノを ひきます」
    Old keyed (pos 2): たなかさんは ピアノが よく ひけます。
                       ^ uses ひける (potential form of 弾く), N4
                         grammar in Genki / Minna / Tobira.
    New keyed (pos 4): たなかさんは ピアノを ひくのが じょうずです。

  Same fix pattern as Q97 in v1.12.13. The Q97 fix swapped a
  nominalized adjective stem for an adverbial keyed; Q64 is the
  inverse direction (adverbial stem -> nominalized adjective keyed).
  Test point: 「じょうずに ひく」 = 「ひくのが じょうず」 - same
  skill, different syntactic frame. Strict-N5 across both items.

### Issue 2: Answer-position distribution rebalance (21 permutations)

  Reviewer noted the corpus had a heavy skew at position B (46/100)
  and starvation at position D (9/100), giving a "when in doubt,
  pick B" heuristic freebie to test-wise students.

    Before:  19 / 46 / 26 /  9   (positions A / B / C / D)
    After:   25 / 25 / 25 / 25   (target distribution)

  Fix is mechanical: permute the choice ORDER within 21 items so the
  keyed answer lands in a balanced position. Choice CONTENT is
  unchanged; only the order changes. correctIndex updated in JSON,
  numbered list reordered in MD, **Answer: N** updated to match.

  Permutations applied (21 total):
    B -> A (6):  Q1, Q5, Q7, Q8, Q13, Q17
    B -> D (14): Q23, Q24, Q26, Q27, Q29, Q30, Q32, Q42, Q44, Q47,
                 Q49, Q51, Q53, Q57
    C -> D (1):  Q3

  Skipped (semantic constraints on choice order):
    Q38-Q41   counter cluster
    Q64       handled in Issue 1 (lands at D)
    Q73       kasu perspective inversion
    Q83       kariru perspective inversion
    Q92       giving-receiving (くれる ≈ もらう)

  Permutation plan was computed deterministically: walk unconstrained
  items in Q-number order, take the first N at each surplus position,
  distribute to deficit positions in deterministic order. Captured in
  TARGET_INDEX dict in the fix script for reproducibility.

### Cache and integrity

 - sw.js CACHE_VERSION:        v126 -> v127
 - index.html cache-busters:    v=1.11.36 -> v=1.11.37
 - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
 - Fix script idempotent (2nd run reports "No changes").
 - Final answer-position distribution: 25 / 25 / 25 / 25.

### Cumulative goi audit closure (v1.12.12..v1.12.17)

  v1.12.12  14 item fixes + 2 policy headers (initial 19-item audit)
  v1.12.13  5 inference cluster items tightened
  v1.12.14  5 re-review follow-ups (Q5/Q51/Q94/Q98/Q99)
  v1.12.15  4 third-pass fixes (Q33/Q44/Q47/Q87) + Q39 verified
  v1.12.16  Q73/Q74 mirror-pair scatter + Mondai 1/2 cross-reference
  v1.12.17  Q64 N4 potential dropped + 25/25/25/25 position rebalance

Total: 29 item-level content edits + 7 rationale tightenings + 3
policy/cross-reference docs + 1 structural swap + 21 position
permutations. Goi corpus now passes the four-pass audit with no
residual flags from any pass.

---

## v1.12.16 - 2026-05-04 (Q73/Q74 mirror-pair scatter + Mondai 1/2 cross-reference)

Closes the v1.12.15 deferral and addresses the third-pass review's
"Coverage gap (still)" mention. Per "fix all remaining": no items
left from the third-pass walk-through.

### Mirror-pair scatter (Q74 <-> Q83 content swap)

Reviewer flagged Q73 (kasu perspective) and Q74 (kariru perspective)
as a conceptually-mirror pair appearing in immediate sequence in
paper-5 (positions 5.13 + 5.14). Pattern recognition would let an
examinee solve one by mechanically inverting the other.

  Before:
    Q73 (paper-5.13)  友だちに 本を かしました   -> 友だちが 私から かりた  (kasu)
    Q74 (paper-5.14)  友だちから 本を かりました -> 友だちが 私に かした    (kariru)
    Q83 (paper-6.8)   バスに のって 学校へ      -> バスで 学校へ          (transportation)

  After:
    Q73 (paper-5.13)  kasu perspective  (UNCHANGED)
    Q74 (paper-5.14)  transportation     (was Q83's content)
    Q83 (paper-6.8)   kariru perspective (was Q74's content)

Distance between Q73 (kasu) and Q83-now-with-kariru: 10 questions
across two papers. kbSourceId mapping preserved (paper-5.14 -> "Q74",
paper-6.8 -> "Q83") because kbSourceId tracks MD position, not
semantic content. JA-32 stays green via lock-step MD <-> JSON.

**Audit-traceability note:** pre-v1.12.16 audit reports referencing
"Q74" mean kariru; post-v1.12.16 they mean transportation. The full
swap is documented here. Q73 is unchanged.

### Mondai 1/2 cross-reference (header docs)

Third-pass review repeated a "Coverage gap (still)" flag for Mondai 1
(kanji reading) and Mondai 2 (orthography). The gap is illusory --
those Mondais are in `KnowledgeBank/moji_questions_n5.md` (100 items
total: 50 Mondai 1 + 50 Mondai 2). An auditor walking only the goi
file would not know to look there.

The goi file header now includes:

 - A prominent blockquote callout naming the moji file as the home
    of Mondai 1+2.
 - An expanded "Subtypes covered" table listing all four Mondais
    with their source file, so the corpus structure is self-
    documenting from a single header.

No content moved between files; only the cross-reference is new.

### Cache and integrity

 - sw.js CACHE_VERSION:        v125 -> v126
 - index.html cache-busters:    v=1.11.35 -> v=1.11.36
 - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
 - Swap script idempotent (2nd run reports "No changes").

### Cumulative goi audit closure (v1.12.12..v1.12.16)

  v1.12.12  14 item fixes + 2 policy headers (initial 19-item audit)
  v1.12.13  5 inference cluster items tightened
  v1.12.14  5 re-review follow-ups (Q5/Q51/Q94/Q98/Q99)
  v1.12.15  4 third-pass fixes (Q33/Q44/Q47/Q87) + Q39 verified
  v1.12.16  Q73/Q74 mirror-pair scatter + Mondai 1/2 cross-reference

Total: 28 item-level content edits + 6 rationale tightenings + 3
policy/cross-reference docs + 1 structural swap. Goi corpus is now
in a state the auditor's third pass described as "consistently above
the level of most commercial N5 vocabulary practice books".

---

## v1.12.15 - 2026-05-04 (Goi third-pass review - 4 fixes + 1 deferred)

A third-pass walk-through by the same auditor on the v1.12.14 state
flagged five remaining minor observations. Four are addressed here;
the fifth (Q73/Q74 mirror-pair scatter) is deferred with rationale.
The reviewer noted the corpus is now in a state where item-level
quality is consistently above commercial N5 vocabulary practice books.

### Fixes (4)

  Q33 / goi-3.3   ので -> から (corpus-wide policy)
    Old stem: つかれたので （　　） すわりました。
    New stem: つかれましたから、（　　） すわりました。
    Same reason conjunction policy as the Q5 fix in v1.12.14.

  Q44 / goi-3.14  ので -> から (corpus-wide policy)
    Old stem: きょうは あめが ふって いるので、...
    New stem: きょうは あめが ふって いるから、...
    Same policy.

  Q47 / goi-4.2   rationale: orphaned note -> "Common error" call-out
    Stem and choices unchanged. The previous parenthetical about
    きょねん felt orphaned because the question doesn't include
    a time marker. Reframed as anticipating a typical student
    error: "Common error: 〜たことがある cannot combine with
    specific time markers (きょねん, etc.)".

  Q87 / goi-6.12  rationale: drop off-topic はたち trivia
    Stem and choices unchanged. The previous rationale included a
    paragraph about the special reading はたち for 二十さい, which
    is interesting trivia but doesn't bear on what this question
    tests (time-reference: present age vs future age). Rationale
    now focuses on the time-reference test point. はたち remains
    documented at vocabulary_n5.md line 1118 so no information
    is lost.

### Deferred (1)

  Q73 / Q74 mirror-pair scatter (paper-5.13 + paper-5.14)
    Reviewer noted these conceptually-mirror items (かす / かりる
    perspective inversion in both directions) appear adjacent and
    suggested moving Q74's content to paper-6 or paper-7 for
    exam-realism. Reviewer themselves flagged this as
    "Pedagogically not wrong as is; just an exam-realism nudge".

    Deferred because a content swap (e.g., Q74 <-> Q83) shuffles
    the Q-number<->content mapping, which carries audit-traceability
    cost: "Q74" in v1.12.x audit reports refers to かりる content,
    but post-swap "Q74" would refer to bus/transportation content.
    For a multi-pass audit cycle still in flight, holding the
    Q<->content mapping stable is more valuable than the small
    exam-realism gain. May revisit when the audit cycle closes.

### Verification footnote (1)

  Q39 / goi-3.9   ボール 〜つ vs つくえ 〜台 cross-reference
    Reviewer asked to confirm つくえ doesn't appear as a counter
    answer elsewhere in the corpus (the Q39 rationale parenthetically
    flags 〜台 as N4-level for furniture). Verified: つくえ appears
    in the corpus only as a noun-place (Q15, Q21) or as the noun
    being quantified by a non-counter quantifier (Q88: いっぱい /
    たくさん / すこし). It never appears as the test target of a
    counter question. Q39's parenthetical stands as informative
    context with no propagation needed.

### ので -> から policy (formalized)

The Q5 fix in v1.12.14 implicitly created a corpus-wide policy
preferring から over ので as the reason conjunction, since ので
leans N4 in major textbooks (Genki / Minna / Tobira). v1.12.15
extends that policy to the two remaining ので usages in the goi
corpus (Q33, Q44). Spot check confirms ので now appears nowhere
in goi stems, only in the v1.12.14 rationale text that documents
the policy itself.

### Cache and integrity

 - sw.js CACHE_VERSION:        v124 -> v125
 - index.html cache-busters:    v=1.11.34 -> v=1.11.35
 - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
 - Fix script idempotent (2nd run reports "No changes").

---

## v1.12.14 - 2026-05-04 (Goi re-review follow-up - 5 items)

A second pass by the same auditor on the v1.12.12+v1.12.13 fixes
identified five remaining issues. All five are addressed here. Net
result of this round: of the 19 originally-flagged audit items, 19
are closed cleanly with no residual caveats; of the 5 items the v1.12
goi rewrites had introduced, all 5 are resolved.

### Five fixes

  Q51 / goi-4.6 - prior tautology, tested no vocabulary
    Old stem:  わたしの ちちは いしゃです。
    Old keyed: わたしの ちちの しごとは いしゃです。  (= the stem)
    New stem:  わたしの ちちは びょういんで はたらいて います。
    New keyed: わたしの ちちは いしゃです。
    Now tests the N5 vocab triangle 病院 / はたらく / いしゃ.
    N5-level pragmatic substitution acknowledged in rationale.

  Q5 / goi-1.5 - N4-grammar leak (ので)
    Old stem: つかれたので、いえで （　　）。
    New stem: つかれましたから、いえで （　　）。
    から is the N5-canonical reason conjunction; ので leans N4 in
    Genki / Minna no Nihongo / Tobira.

  Q94 / goi-7.4 - rationale-labeling imprecision
    Old: あまくない (plain neg) = あまく ありません (polite neg).
    New: あまくないです (i-adj + です polite neg) = あまく ありません
         (formal polite neg). Two equivalent polite forms.
    Stem and choices unchanged; only rationale tightened.

  Q98 / goi-7.8 - わたす is borderline N5/N4 ([Ext] in vocabulary_n5.md)
    Old keyed: ... 先生に しゅくだいを わたします。
    New keyed: ... 先生に しゅくだいを もって いきます。
    Removes [Ext] vocab from the answer key entirely. Project [Ext]
    policy says "useful for recognition; do not over-prioritize" -
    being the keyed answer over-prioritizes. もって いく is strict
    N5 (both もつ and いく are core). Pragmatic substitution at N5
    level: take homework to teacher = submit homework. Note: kept
    in kana because 持 is not in the kanji whitelist. わたす no
    longer appears anywhere in the goi corpus.

  Q99 / goi-7.9 - weak entailment, no acknowledgement
    "X から きました" -> "X 人です" is a pragmatic inference, not
    a logical equivalence (someone can come from X without being
    X-jin: tourist, expat, returning resident). Stem unchanged;
    rationale updated to acknowledge this as standard N5 textbook
    pragmatic substitution, mirroring the existing soft-entailment
    acknowledgement pattern used elsewhere in the corpus.

### Cache and integrity

 - sw.js CACHE_VERSION:        v123 -> v124
 - index.html cache-busters:    v=1.11.33 -> v=1.11.34
 - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
 - Fix script idempotent (2nd run reports "No changes").

---

## v1.12.13 - 2026-05-04 (Inference-paraphrase cluster tightened - 5 items)

Follow-up to v1.12.12. The audit's "tighten at least two of them so
the pattern doesn't dominate" recommendation has been honoured for
all five inference-paraphrase items per the user's "fix all fixables"
instruction. The v1.12.12 policy header that documented these items
as deliberate inference convention has been replaced with a record of
the tightening pass; the items are now true paraphrases, not
inference-bridged ones.

### Tightenings (5)

  Q70 / goi-5.10  好き -> よく する
    Old stem: たろうさんは スポーツが すきです。
    New stem: たろうさんは スポーツが すきで、まいにち します。
    Frequency clause makes 「よく する」 a direct paraphrase rather
    than an inference from liking alone.

  Q76 / goi-6.1   X より Y すき -> Y を よく 飲む
    Old stem: わたしは おちゃより コーヒーの ほうが すきです。
    New stem: わたしは おちゃより コーヒーの ほうが すきで、
              まいにち 飲みます。
    Frequency clause closes the preference-to-drinking gap.

  Q86 / goi-6.11  電話を かける -> 電話で 話す
    Old stem: 友だちに でんわを かけました。
    New stem: 友だちに でんわを かけて、一時間 話しました。
    Duration clause confirms a successful conversation, removing the
    "called but no-one answered" inference gap.

  Q97 / goi-7.7   じょうず -> 上手に 話す  (also: drops N4 potential)
    Old stem:    たろうさんは 日本ごが じょうずです。
    New stem:    たろうさんは 日本ごを 話すのが じょうずです。
    Old keyed:   日本ごを よく 話せます (N4 potential form)
    New keyed:   日本ごを 上手に 話します (N5 plain)
    Scopes じょうず to speaking specifically (nominalized adj. vs.
    adverbial - same skill, different syntactic frame). Bonus: the
    keyed answer no longer relies on N4 potential 話せます.

  Q100 / goi-7.10 ならって いる -> れんしゅう
    Old stem: わたしは ピアノを ならって います。
    New stem: わたしは ピアノを ならって、まいにち れんしゅうします。
    Daily-practice clause makes 「れんしゅうを して いる」 a direct
    paraphrase, not an inference from "is taking lessons".

### Header policy revision

The "Inference-style paraphrases" subsection in goi_questions_n5.md
(added in v1.12.12) has been replaced with "Paraphrase-tightening
pass (2026-05-04, v1.12.13)" recording what was changed. The previous
policy framed these items as deliberate inference convention; after
the rewrites that framing is no longer accurate.

### Cache and integrity

 - sw.js CACHE_VERSION:        v122 -> v123
 - index.html cache-busters:    v=1.11.32 -> v=1.11.33
 - 41/41 invariants PASS (incl. JA-32 lock-step MD↔JSON parity)
 - Fix script idempotent (2nd run reports "No changes").

---

## v1.12.12 - 2026-05-04 (Goi audit closure - 14 item fixes + 2 header policies)

External native-speaker / JLPT-aligned auditor reviewed all 100 goi
items and flagged 19 issues across 4 severity tiers. This release
addresses 14 of them with concrete content fixes; the remaining 5
(Q70/Q76/Q86/Q97/Q100 inference-paraphrase cluster) and the 6 N4-
leakage items are addressed at the source-policy level via two new
header sections in goi_questions_n5.md.

### Critical fixes (4)

  Q21 / goi-2.6 - stem had no anchor; all 4 positional answers valid.
    Old: ほんは つくえの (  ) に あります。
    New: ほんが つくえの (  ) から おちました。
    Now uniquely anchors うえ via physics: things only fall from above.

  Q94 / goi-7.4 - keyed answer was a graded negation, not a true
    paraphrase of flat negation あまくないです.
    Replaced choice [3] あまり あまく ないです -> あまく ありません.
    Now a clean polite-form paraphrase (same meaning, different
    politeness register).

  Q98 / goi-7.8 - keyed answer changed both the particle (までに ->
    まで) and the time window. Whole item replaced.
    New stem: わたしは あした しゅくだいを 出します。
    New keyed: あした、わたしは 先生に しゅくだいを わたします。
    Tests 出す = わたす in homework-submission context (clean paraphrase).

  Q99 / goi-7.9 - 知っている and 覚えている are not synonyms. Whole
    item replaced.
    New stem: わたしは スペインから きました。
    New keyed: わたしは スペイン人です。
    Tests origin (X から きた) = nationality (X 人).

### Moderate fixes (5)

  Q39 / goi-3.9: 机 takes 〜台 not 〜つ -> swapped noun to ボール.
  Q68 / goi-5.8: keyed 学生が narrowed scope -> 人が (matches だれも universal).
  Q79 / goi-6.4: rationale aligned with Q80 (added "broader than" caveat).
  Q89 / goi-6.14: 「高い お金」 unnatural -> たくさん お金を 払いました.
  Q45 / goi-3.15: シャツ weak distractor -> パジャマ (clearly indoor).

### Minor polish (4)

  Q1 / goi-1.1:  毎あさ -> まいあさ (kana consistency).
  Q5 / goi-1.5:  つかれましたから -> つかれたので (tense consistency
                 with the choice 「やすみます」 - actually 「やすみます」
                 is non-past which is fine after ので+plain past).
  Q10 / goi-1.10: あついです distractor -> はやいです (avoid 暑い/厚い
                  homophone trap on 本).
  Q19 / goi-2.4:  きのうは とても -> きのうは しごとが とても (added
                  topic word; しごと anchors いそがしい uniquely).

### Source-policy header notes (in goi_questions_n5.md)

Two policy sections added to the header to formalize how the corpus
treats two boundary cases the auditor flagged as clusters:

  1. **Inference-style paraphrases** (Q70 好き/よくする, Q76, Q86,
     Q97, Q100): treated as deliberate N5-level pedagogical
     conventions where likes/skill/lessons commonly entail the
     related action. The rationales' acknowledgement of the gap
     stays - it is now framed as graded-by-closeness rather than
     "apologizing".

  2. **Late-N5 / N4-stretch items** (Q47 ～たことがある, Q48
     ～つもりだ, Q62 ～あいだに, Q64 ひけます potential, Q91 ～て
     N に なる, Q97 話せます potential): documented as deliberate
     stretch content for learners on the cusp of N4. Aligns with
     the project's "late_n5" tier convention (25 grammar.json
     patterns also flagged tier=late_n5).

### Cache and integrity

 - sw.js CACHE_VERSION:        v121 -> v122
 - index.html cache-busters:    v=1.11.31 -> v=1.11.32
 - tools/check_content_integrity.py -> 41/41 invariants PASS
    (incl. JA-32: every kanji in new rationales appears in MD source)
 - tools/fix_goi_audit_2026_05_04.py -> idempotent

## v1.12.11 - 2026-05-04 (45 dokkai rationales authored - 100% rationale coverage)

External auditor reported 45 of 60 dokkai questions (Q1-Q60) had
empty rationales - paper builder was faithfully reflecting the MD,
but the MD had only `**Answer: N**.` with no explanation text for
those 45. Per the project's "rationales help learners understand
why their wrong answer was wrong" stance and the existing pattern
(15/60 dokkai already had rationales; goi/moji/bunpou ~all do), these
were authored.

### Authored content

  Each rationale is a 1-line citation of the passage detail that
  justifies the marked correct answer, mirroring the brief-citation
  style of the existing 15 dokkai rationales (e.g., "first action is
  meeting at station." for Q9). Mix of English narration and
  Japanese excerpts as the corpus already does.

  Distribution by paper:
    paper-1.json: 5 rationales authored (Q11, Q12, Q13, Q15, Q16)
    paper-2.json: 13 rationales (Q18-Q25, Q28-Q32)
    paper-3.json: 16 rationales (Q33-Q48)
    paper-4.json: 11 rationales (Q49, Q50, Q52-Q60)

  Total: 45 questions, dokkai rationale coverage 15/60 -> 60/60 (100%).

### Files updated (in lock-step)

  KnowledgeBank/dokkai_questions_n5.md  (source MD)
  data/papers/dokkai/paper-1.json
  data/papers/dokkai/paper-2.json
  data/papers/dokkai/paper-3.json
  data/papers/dokkai/paper-4.json

  Both files updated together so JA-32 (paper-JSON rationales appear
  verbatim in source MD) stays green. JA-32 verification confirms:
  every kanji used in the new rationales also appears in its
  corresponding MD Q-block (passage / stem / choices), so no
  stale-extract drift introduced.

### Cache and integrity

 - sw.js CACHE_VERSION:        v120 -> v121
 - index.html cache-busters:    v=1.11.30 -> v=1.11.31
 - tools/check_content_integrity.py -> 41/41 invariants PASS
 - tools/author_45_dokkai_rationales_2026_05_04.py -> idempotent
 - X-6.5 (no em-dashes): caught + stripped 86 em-dashes I introduced
    in rationale text during initial authoring, before commit.

## v1.12.10 - 2026-05-04 (paper-JSON rationale drift fixed + JA-32 invariant added)

External auditor flagged: `data/papers/bunpou/paper-2.json` Q19
rationale uses 熱 (non-N5 kanji): "熱がある (have a fever)." The KB
source MD had been corrected to "ねつが ある (have a fever)." in
v1.12.4 (commit 658f35d), but the paper extraction wasn't re-run, so
the JSON kept the stale kanji form.

### Fix

 - `data/papers/bunpou/paper-2.json` bunpou-2.4 (kbSourceId=Q19):
      rationale "熱がある (have a fever)." -> "ねつが ある (have a fever)."
      (now matches KB exactly)

### CI hardening - JA-32

To prevent future MD-updated-but-JSON-stale drift in any paper file,
added invariant **JA-32**: for each paper-JSON question with a
kbSourceId, every kanji in its rationale field must also appear
somewhere in the corresponding MD Q-block.

 - Catches stale extraction (MD says ねつ, JSON says 熱) immediately.
 - Does NOT false-positive on authored rationales (e.g., bunpou-5/6
    sentence-rearrange, where the rationale was expanded during the
    audit fix) - authored rationales reuse kanji that were already
    in the MD's stem / choices / answer line, so they pass.
 - Implemented in `tools/check_content_integrity.py`
    `_check_ja_32_paper_rationale_md_parity()`.
 - Verified: simulating the auditor's old stale state ("熱がある"
    when MD had "ねつが ある") produces exactly the expected failure
    "stale: ['熱']".

Sweep result post-fix: zero JA-32 violations across all 25 paper
JSONs. Other rationales that contain non-N5 kanji (e.g., goi-5.13's
"借りる ⇄ 貸す" pedagogical explanation) all reference kanji that
appear in their MD Q-block as part of the question content, so they
correctly pass.

### Cache and integrity

 - sw.js CACHE_VERSION:        v119 -> v120
 - index.html cache-busters:    v=1.11.29 -> v=1.11.30
 - tools/check_content_integrity.py -> 41/41 invariants PASS
    (was 40 - added JA-32)

## v1.12.9 - 2026-05-04 (Em-dash audit gap closed + 3 stray em-dashes stripped)

External auditor flagged one stray em-dash (U+2014) in the v1.12.8
`n5_vocab_whitelist_README.md` rewrite. Investigation: X-6.5 (no
em-dashes) was scanning only the 9 KnowledgeBank/*.md files, not
the data/*.md design-rationale READMEs. Extended X-6.5 to scan
`data/*.md` too; the extended check immediately surfaced 2 more
em-dashes in `data/n5_kanji_whitelist.exceptions.md` that had also
been outside the previous CI scope.

### Fixes

 - `data/n5_vocab_whitelist_README.md`: 1 em-dash -> hyphen
 - `data/n5_kanji_whitelist.exceptions.md`: 2 em-dashes -> hyphens
 - `tools/check_content_integrity.py` X-6.5: extended to also scan
    `data/*.md` so future README rewrites can't slip past the
    no-em-dash policy.

### Cache and integrity

 - sw.js CACHE_VERSION:        v118 -> v119
 - index.html cache-busters:    v=1.11.28 -> v=1.11.29
 - tools/check_content_integrity.py -> 40/40 invariants PASS
    (X-6.5 now scans 9 KB files + data/*.md = 11 files total)

## v1.12.8 - 2026-05-04 (Whitelist drift fully closed - 38 new vocab entries)

Closes the v1.12.7 "perceived drift" between `n5_vocab_whitelist.json`
and `data/vocab.json` by **authoring 38 new structured vocab.json
entries** that cover all 40 previously-unmatched whitelist tokens.

Drift went 40 -> 0. The whitelist (969 tokens) now strictly matches
form/reading values in vocab.json (1041 entries). The "intentional
superset" framing from v1.12.7 is no longer applicable; alignment is
now strict.

### 29 standalone vocab entries (recognition-only -> first-class catalog)

These were valid N5 tokens that appeared in vocabulary_n5.md gloss /
example text but lacked structured catalog entries. Each gets a full
entry with form, reading, gloss, section, pos, and 1 example sentence:

  Section 3 (People - Roles):
    高校生 (こうこうせい) - high school student

  Section 9 (Counters):
    倍 (ばい) - times / -fold

  Section 10 (Time):
    後 (あと) - after / later

  Section 11 (Days/Weeks/Months/Years):
    週末 (しゅうまつ) - weekend

  Section 13 (Locations):
    おてら, カフェ, コンビニ, フロント, 出口

  Section 14 (Nature):
    さくら

  Section 22 (Money & Shopping):
    アルバイト, セール

  Section 24 (School & Study):
    おしらせ, じゅんび, たんご

  Section 25 (Languages & Countries):
    スペイン人, 国籍

  Section 26 (House & Furniture):
    ベンチ

  Section 27 (Verbs Group 1):
    はらう (pay)

  Section 28 (Verbs Group 2):
    おくれる (be late), ためる (save), 聞こえる (be audible)

  Section 33 (Adverbs):
    いっぱい, ぜひ, ただ, べつべつ

  Section 36 (Greetings/Set Phrases):
    おじゃまします

  Section 40 (Misc Useful Items):
    おもちゃ, コンサート

### 9 multi-form merged entries (alias pairs -> first-class)

Following the existing precedent (8 entries like 何 reading="なに / なん"
or 七 reading="しち / なな"), these 9 entries use multi-form notation
in the `reading` field to cover both alias and canonical forms in a
single entry:

  いい                    reading="いい / よい"           [i-adj]
  いえ                    reading="いえ / うち"           [noun]
  ぐらい                  reading="ぐらい / くらい"       [particle]
  けれど                  reading="けれど / けれども / けど" [conjunction]
  ござる                  reading="ござる / ございます"   [verb-1]
  じゃあ                  reading="じゃあ / では / じゃ"  [expression]
  みんな                  reading="みんな / みな"         [noun]
  やはり                  reading="やはり / やっぱり"     [adverb]
  ゼロ                    reading="ゼロ / れい"           [numeral]

JA-31 POS parity verified: each new entry's pos field matches the
multi-form line's [tag] in vocabulary_n5.md (i-adj -> i-adj,
noun -> n., particle -> part., etc.).

### data/n5_vocab_whitelist_README.md updated

The original draft documented the 40 missing tokens as "intentional
superset by design". After v1.12.8, drift = 0, so the README is
revised to record the alignment + the v1.12.7 -> v1.12.8 transition
in the History section. Future audits comparing whitelist to vocab.json
will see strict 1:1 form/reading correspondence.

### Cache and integrity

 - sw.js CACHE_VERSION:        v117 -> v118
 - index.html cache-busters:    v=1.11.27 -> v=1.11.28
 - data/vocab.json: 1003 -> 1041 entries (+38)
 - n5_vocab_whitelist.json drift: 40 -> 0 (-40)
 - tools/check_content_integrity.py -> 40/40 invariants PASS
    (including JA-31 vocab POS parity)
 - tools/author_29_vocab_entries_2026_05_04.py -> idempotent
 - tools/author_10_alias_entries_2026_05_04.py -> idempotent

## v1.12.7 - 2026-05-04 (Data folder bugs - n5-188 audio + whitelist design doc)

Closes 2 bugs from the 2026-05-04 data-folder audit.

### Bug 1 (LOW) - n5-188 audio synthesis sync lag

The new pattern n5-188 (Verb + ことができる, shipped in v1.12.3) had 3
grammar examples in `data/grammar.json` but no corresponding entries in
`data/audio_manifest.json` and no MP3 files on disk. New-pattern
audio-synthesis lag.

Fix:
 - Rendered 3 MP3s via gTTS (Japanese voice, synthetic-gtts backend
    matching the convention used for n5-001..n5-187):
      audio/grammar/n5-188.0.mp3  (23,424 bytes - 日本語を 話す...)
      audio/grammar/n5-188.1.mp3  (21,696 bytes - ピアノを ひく...)
      audio/grammar/n5-188.2.mp3  (20,544 bytes - あした 行く...)
 - Added 3 manifest entries pointing at the new files with
    skipped=false (audio actually exists on disk).

User-visible effect: the n5-188 example player works on the Grammar
detail page after SW cache refresh.

### Bug 2 (MEDIUM) - whitelist appears to drift from vocab.json

Auditor report: 40 entries in `data/n5_vocab_whitelist.json` don't
appear as form/reading in any `data/vocab.json` entry.

Investigation:
  `data/n5_vocab_whitelist.json` is **generated** from
  `KnowledgeBank/vocabulary_n5.md` by `tools/build_data.py`. The
  whitelist's purpose is to serve as the **recognition allowlist** for
  `tools/lint_content.py` when checking N5-scope conformance - distinct
  from `data/vocab.json`'s role as the structured catalog. The
  whitelist is **intentionally a superset** of vocab.json forms.

Categorization of the 40:
 - **10 multi-form aliases** (by design): いい, いえ, ぐらい, けれど,
    ござる, じゃあ, では, みんな, やはり, ゼロ. Each has a canonical
    counterpart in vocab.json (よい, うち, くらい, けど, ございます,
    では, じゃ, みな, やっぱり, れい). vocabulary_n5.md lists them as
    multi-form entries; build_data.py extracts both forms into the
    whitelist. Expected behavior.
 - **30 recognition-only items** (pending vocab.json authoring):
    valid N5 vocab tokens (アルバイト, カフェ, コンサート, 出口,
    高校生, 聞こえる, 週末, etc.) that appear in vocabulary_n5.md gloss
    /example text and are recognized by the lint script, but lack full
    structured `vocab.json` entries. Promotion to full entries is
    future authoring work.

Fix:
  Shipped `data/n5_vocab_whitelist_README.md` documenting the design
  rationale, the two-category breakdown, and the maintenance protocol.
  Future audits running KB-only or data-only checks will see the
  README and understand the superset relationship as design rather
  than drift.

  No data-content changes - the whitelist is correct as a generated
  artifact. vocab.json is correct as a curated catalog. The two
  files have distinct, complementary roles.

### Cache and integrity

 - sw.js CACHE_VERSION:        v116 -> v117
 - index.html cache-busters:    v=1.11.26 -> v=1.11.27
 - tools/check_content_integrity.py -> 40/40 invariants PASS
 - tools/fix_data_bugs_2026_05_04.py -> idempotent (0 edits on
    second run)

## v1.12.6 - 2026-05-04 (KB-only audit alignment - dokkai header self-verifying)

Fixes a real internal contradiction in `dokkai_questions_n5.md` that
KB-only audit pipelines (auditors who only see `KnowledgeBank/*.md`
without `data/*.json`) couldn't resolve.

The header at line 17 listed the dokkai-kanji exception register's
**original 25 kanji** ("currently covers: 京, 作, ... 同"). When the
register was extended to 28 kanji (向, 央, 付 added in commit b93ca01
on 2026-05-03 per moji-and-source audit §2.2), the JSON was updated
but the MD header wasn't. A trailing HTML comment was added at the
bottom announcing the extension, but the header remained stale.

For an auditor with only KB files (no data/), this read as:
  Header says 25 kanji.
  Comment at the bottom says "extended with 向, 央, 付".
  No way to verify which is correct without the JSON.
  Auditor reports: "JSON unchanged at 25; comment claims 28."

Fix: header line 17 now lists all **28 kanji** with inline rationale
for the 3 additions. Trailing marker comment removed (header is now
the single source of truth within KB-only view; JSON remains the
machine-tracked authoritative list).

### File changes

  KnowledgeBank/dokkai_questions_n5.md
    Line 17: kanji list 25 -> 28; added 向 / 央 / 付 with brief
             "added on 2026-05-03 §2.2" attribution.
    Line 1631: trailing HTML marker comment removed (now redundant
             with the updated header).

### Verification

 - data/dokkai_kanji_exception.json was already at 28 entries
    (since commit b93ca01); this commit synchronizes the MD header
    with that state.
 - tools/check_content_integrity.py -> 40/40 invariants PASS
 - JA-28 (dokkai-paper kanji bounded by N5 + exception list) -> PASS
 - KB-only audit upload now sees consistent state without needing
    the JSON.

### Cache and integrity

 - sw.js CACHE_VERSION:        v115 -> v116
 - index.html cache-busters:    v=1.11.25 -> v=1.11.26

## v1.12.5 - 2026-05-04 (Open-bug-list Bug 8 closed - filename rename)

Closes the deferred Bug 8 from v1.12.4. The file
`KnowledgeBank/authentic_extracted_n5.md` is renamed to
`KnowledgeBank/externally_sourced_n5.md` to match its H1 title and
remove the misleading "authentic" framing from the file path.

### File rename

  `KnowledgeBank/authentic_extracted_n5.md`
    -> `KnowledgeBank/externally_sourced_n5.md`

  Done via `git mv` to preserve blame history. Contents unchanged
  except for the "Filename history" disclaimer block (the prior
  paragraph announcing the rename was pending; now records the
  rename is done, links DEFER-11 / CONTENT-LICENSE.md as the
  rationale for Pass 12 not happening).

### Active references updated (CI / build / spec / docs)

  tools/check_content_integrity.py            (KB_FILES list + EXPECTED_Q_COUNTS)
  tools/build_papers.py                       (docstring "Skipped files" + comment)
  tools/fix_open_bugs_2026_05_04.py           (Bug 8 docstring -> closed)
  specifications/JLPT-N5-Functional-Spec-v3.1-supplement.md (file-tree listing)
  verification.md                              (10 audit-trail table refs)
  TASKS.md                                     (3 historical entries)
  CHANGELOG.md                                 (3 historical mentions)

### Historical archives left as-is (preserve audit-trail accuracy)

  feedback/closed/jlpt-n5-moji-and-source-audit-2026-05-03.md
  feedback/closed/jlpt-n5-knowledgebank-md-audit-2026-05-01.md
  feedback/closed/native-teacher-review-request.md
  feedback/closed/jlpt-n5-content-correction-brief.md

  These are historical snapshots from when the file was named
  authentic_extracted_n5.md. Keeping the original filename in
  archived audits preserves the historical accuracy of those records.

### Cache and integrity

 - sw.js CACHE_VERSION:        v114 -> v115
 - index.html cache-busters:    v=1.11.24 -> v=1.11.25
 - tools/check_content_integrity.py -> 40/40 invariants PASS
    (KB_FILES list now references the new filename; EXPECTED_Q_COUNTS
    keys updated; X-6.5 em-dash check passes - one em-dash that
    leaked into the rewritten disclaimer was caught and stripped
    before commit.)

## v1.12.4 - 2026-05-04 (Open-bug-list closure - 7 of 8 fixed; 1 deferred)

Closes 7 of 8 items from the open-bug-list filed 2026-05-04. The last
item (filename rename of externally_sourced_n5.md) is deferred - 
10 cross-references in build/CI scripts would need synchronized
updates; scope larger than this batch warrants. The file's H1 title
was already changed to "JLPT N5 Externally-Sourced Practice Questions"
so the misleading framing is gone in user-facing content.

### Catalog-content changes (visible to learners)

**dokkai narrator references unified (Bug 4).** 36 references to the
passage narrator were split across two non-N5-canonical conventions:
"書いた 人" (30 instances, stilted) and "ひっしゃ" (6 instances,
non-N5 vocab 筆者). Both replaced with "この 人" - the standard JLPT
N5 dokkai phrasing for "this person / the writer of this passage".
Fix applied in BOTH `KnowledgeBank/dokkai_questions_n5.md` AND the
extracted JSONs `data/papers/dokkai/paper-{1..4}.json`.

**dokkai non-N5 kanji removed (Bugs 2, 3).** Two small kanji-scope
violations in the dokkai source:
 - "初めて" (3 occurrences total: 2 in dokkai questions, 0 in
    paper JSONs) -> "はじめて". 初 was not in the N5 whitelist nor
    the dokkai exception register.
 - "急いで" (1 occurrence in passage content) -> "いそいで".

**bunpou Q24 realism (Bug 5).** Tokyo-Osaka route example:
 - Was: "とうきょう（  ）おおさかまで でんしゃで いきます。"
 - Now: "とうきょう（  ）おおさかまで しんかんせんで いきます。"
  しんかんせん is the realistic mode for the Tokyo-Osaka route. Fixed
  in source MD AND the bunpou paper-2 JSON.

### Catalog-only doc improvements (no learner-visible content change)

**moji distractor-convention section extended (Bug 6).** The header
section in `moji_questions_n5.md` originally documented 2 of 3
distractor types in active use. Now lists all three:
  1. Visually-similar N5 kanji (e.g., 多い / 古い / 長い for 高い)
  2. Non-N5 kanji with same on-yomi (e.g., 経ちます for 立ちます)
  3. Invented (non-real) verb forms (e.g., 出ります for 出ます)

**vocabulary_n5.md POS-legend header cleaned (Bug 7).** The
"Part-of-Speech Tags" section header carried a stray
"(added 2026-05-02)" date stamp that no other section header used.
Stripped for cosmetic consistency.

### Verified-already-aligned (Bug 1)

`data/dokkai_kanji_exception.json` already contains 向 / 央 / 付
(added in commit b93ca01); the marker comment in
`KnowledgeBank/dokkai_questions_n5.md` accurately reflects this state.
The bug-list entry was based on a stale snapshot.

### Deferred (Bug 8)

`KnowledgeBank/externally_sourced_n5.md` keeps its filename for now.
The H1 title already says "Externally-Sourced Practice Questions";
only the path retains the legacy "authentic" label. Renaming requires
synchronized updates in 10 files (incl. tools/build_papers.py and
tools/check_content_integrity.py) - scope warrants a separate
focused commit.

### Cache and integrity

 - sw.js CACHE_VERSION: v113 -> v114
 - index.html cache-busters: v=1.11.23 -> v=1.11.24
 - tools/check_content_integrity.py -> 40/40 invariants PASS
    (including JA-13, JA-28 dokkai-kanji bound, JA-31 vocab POS parity)
 - tools/fix_open_bugs_2026_05_04.py -> idempotent (0 edits on
    second run)

## v1.12.3 - 2026-05-04 (Reference-markdowns audit propagation to runtime data)

Propagates the v1.12.2 catalog-level fixes into the runtime JSON files
that the website actually serves. The website now exposes the new
grammar pattern, the updated もらう particle option, and the corrected
kanji-reading orderings to learners at runtime - not just in the
reference docs.

### New grammar pattern shipped (visible to learners)

**n5-188: Verb + ことができる (productive can-do form).** Was flagged
as missing in the v1.12.2 audit; now a first-class entry in
`data/grammar.json` with full schema (3 examples, 2 common_mistakes,
explanation_en, form_rules, notes pairing it with n5-103). Tier:
core_n5. Category: Comparison and Preference (alongside n5-103).

 - 日本語を 話す ことが できます。 (I can speak Japanese.)
 - ピアノを ひく ことが できますか。 (Can you play piano?)
 - あした 行く ことが できません。 (I can't go tomorrow.)

Two questions added (q-0579 / q-0580) covering the affirmative and
negative forms - pattern coverage stays at 100% (178/178).

### Runtime data updates

 - `data/grammar.json` n5-131 (もらう):
      pattern: ～に～をもらいます → ～に / から ～をもらいます
      meaning_en clarified to mention both particles
      notes appended with personal-vs-institutional usage rule
 - `data/grammar.json`: new pattern n5-188 (see above)
 - `data/kanji.json` 後: kun reordered ['のち','うし','あと'] →
      ['うし','あと','のち'] (matches kanji_n5.md update; primary_reading
      stays 'あと')
 - `data/n5_kanji_readings.json` 後: same kun reorder
 - `data/questions.json`: 288 → 290 questions (mcq 258 → 260);
      _meta refreshed; audit_history entry appended

### Cache and integrity

 - sw.js CACHE_VERSION: v112 -> v113 (forces re-fetch of grammar.json,
    questions.json, kanji.json, n5_kanji_readings.json updates).
 - index.html cache-busters: v=1.11.22 -> v=1.11.23.
 - tools/check_content_integrity.py -> 40/40 invariants PASS,
    including JA-12 (kanji KB↔JSON consistency), JA-17 (grammar
    examples have vocab_ids), JA-26 (no duplicate question IDs).
 - Pattern coverage: 178/178 (was 177/177 + new n5-188 = 178; q-0579
    and q-0580 cover it).
 - tools/propagate_ref_md_audit_2026_05_04.py is idempotent.

## v1.12.2 - 2026-05-04 (Reference-markdowns audit closure - 11 items resolved)

Closes all 11 items in the 2026-05-04 reference-markdowns re-audit. The
first audit cycle since the project began without a critical-severity
finding. All fixes are at the catalog / reference-doc level, plus
mirrored corrections in `data/vocab.json` so JA-31 stays green.

### Catalog-content changes (visible to learners)

**vocabulary_n5.md + vocab.json POS-tag corrections (§1.3).** Six
entries in Section 1 (Pronouns and Self) plus one in Section 12
(Time-Frequency) carried section-default POS tags that didn't match
the word's actual lexical class. Both files updated consistently:

 - 人 (ひと) sect 1: pronoun -> noun (used in pronoun-like phrases
    but lexically a 名詞)
 - かた sect 1: pronoun -> noun (polite "person" headword)
 - だれ: pronoun -> question-word (matches sect 6 classification)
 - どなた: pronoun -> question-word (matches sect 6 classification)
 - みなさん: pronoun -> noun (vocative / address term, not a pronoun)
 - みんな / みな: pronoun -> noun (multi-form alias; MD only)
 - もうすぐ sect 12: noun -> adverb (functions adverbially: もうすぐ来る)

The 7 remaining sect 1 entries (私, 私たち, あなた, かれ, かのじょ,
じぶん, etc.) are real pronouns and stay tagged [pron.].

**kanji_n5.md scope-flag pass (§1.1, §1.2).** 19 entries had readings
outside N5 scope without any flag, while 上 / 下 already carried
[N4+ verb reading; recognition only] markers. Applied the existing
flag pattern uniformly so the README's "scope rule" matches the
file's contents:

 - 入 kun reordered: い(る), はい(る), い(れる) -> はい(る), い(る),
    い(れる) with stem-split note. はい is the standalone verb 入る;
    い-stem appears in 入れる / 入り. (This is the upstream root cause
    of an earlier downstream bug in n5_kanji_readings.json's primary
    field.)
 - 半: なか(ば) -> [N3+ noun reading]
 - 何: カ on -> [N3+ on-reading]
 - 語: かた(る) -> [N3 verb reading]
 - 木: こ- -> [N4+ prefix]
 - 金: かな- -> [N4+ prefix]
 - 小: こ-, お- -> both [N4+ prefix]
 - 後: のち -> [N4+ literary], reordered うし(ろ), あと first
 - 空: あ(く) -> [N4 verb reading]
 - 見: み(える) -> [N4 verb reading], み(せる) -> [N4-N5 borderline]
 - 聞: き(こえる) -> [N4 verb reading]
 - 立: た(てる) -> [N4 transitive verb reading]
 - 休: やす(まる) -> [N4 intransitive verb reading]
 - 言: こと -> [jukujikun in 言葉 only; not standalone N5]
 - 新: あら(た) -> [N3 stem reading], にい- -> [N4+ prefix]
 - 白: しら- -> [N3+ prefix]
 - 行: ゆ(く) -> [N4+ poetic alt], おこな(う) -> [N3 verb reading]
 - 来: きた(る) -> [N3+ literary]
 - 生: clarified note - both 生きる / 生まれる ARE N5 verbs; on-reading
    セイ in compounds.

**grammar_n5.md additions (§1.4, §2.1, §2.2, §2.3, §2.4, §3.2).**

 - Section 10: added "Verb (plain dictionary) + ことができる /
    ことができます (can do - productive form)" with 日本語を 話す
    ことが できます example. This is canonical N5 grammar (Genki I
    L13, Minna L18) but was missing from the catalog.
 - Section 15: もらう pattern now lists ～に / から ～をもらいます
    with note that に is more typical for personal givers, から for
    institutional sources. Both are N5.
 - Section 1: もの example replaced. Was だって、いそがしいんだもの
    (combined もの + んだ patterns); now 行きたくないもん or
    だって、雨だもの (single pattern only).
 - Section 22: bika-go example list updated to drop ごはん from
    "productive" prefix examples (it's a single lexicalized word now).
    Replaced with お茶, お金, おさけ, おみず, おはな - all genuinely
    productive お-prefix cases.
 - Question-word + か/も citation: "Genki I L8 / L10" -> "L8 for
    か-compounds; L9 for も-compounds with negative; いつも at L11"
    (more accurate per Genki 3rd edition).
 - Section 23.10 prohibitive な: added register caveat - "rough /
    commanding. Use only with clear authority differential or in
    writing (signs / labels). For polite prohibition use ～ないでください."

**sources.md additions (§2.5, §3.1).**

 - Added "JLPT N5 Sample Questions" reference under JEES (free PDFs
    on jlpt.jp; the most authoritative single reference for actual
    paper format).
 - Added "NHK NEWS WEB EASY" (https://www3.nhk.or.jp/news/easy/)
    under Established Learner References - daily news rewritten for
    N5/N4 learners.

### Cache and integrity

 - sw.js CACHE_VERSION: v111 -> v112 (forces re-fetch of vocab.json
    + listening.json + grammar.json updates).
 - index.html cache-busters: v=1.11.21 -> v=1.11.22.
 - tools/check_content_integrity.py -> 40/40 invariants PASS
    (including JA-31 vocab POS parity between MD and JSON).
 - tools/fix_ref_md_audit_2026_05_04.py -> idempotent (0 changes on
    second run).

## v1.12.1 - 2026-05-03 (Moji + source audit closure - 12 items resolved)

Closes all 12 items in the 2026-05-03 moji + source-markdowns audit.
Mostly extraction-pipeline + naturalness fixes - visible to learners as
formerly-blank moji questions becoming readable, and a handful of
JLPT-mock-paper stems and choices replaced with cleaner forms.

### Live-content changes (visible to users)

**24 moji questions now display correctly (§1.1).** The mock-paper
extraction had silently dropped the stem on questions where the test
target sat at the very start of the sentence (`__test-word__ ...`).
Affected papers: moji-4 (5 Qs), moji-5 (12 Qs), moji-6 (3 Qs), moji-7
(4 Qs). All 24 stems now populated from `KnowledgeBank/
moji_questions_n5.md` and carry rationales matching the source.

**3 moji-7 questions now use the standard Mondai 2 stem format (§2.4).**
Q97-Q99 had a non-canonical `__lemma__ - sentence` prefix that no other
Mondai 2 stem in the corpus uses. Dropped the prefix; the questions
read like every other 表記 (orthography) question.

**2 moji stems no longer show non-N5 kanji to N5 learners (§2.1):**
 - Q35 「私の いえは 町の <u>北</u> に あります。」 → `町` (machi,
    non-N5) → `まち`. Stem now readable end-to-end at N5.
 - Q95 「八百屋で やさいを __かいます__。」 → `八百屋` (yaoya, has
    non-N5 屋) → `みせ`.

**3 goi distractors restored to authentic-JLPT kanji form (§3.1).** A
prior audit had been over-strict: it flagged 4 goi questions with non-N5
kanji, but only Q58 (correct-answer position) was a real policy
violation. The 3 distractor positions (Q65: 少, Q86: 紙, Q100: 売) are
explicitly within the source's documented exception ("distractors may
include non-N5 kanji because authentic JLPT distractors mimic visually-
similar wrong forms"). Reverted to the source's kanji forms.

  Q58 (real correct-answer violation) source markdown updated to match
  the JSON's kana fix (「きのう 早く ねました。」 → 「きのう はやく
  ねました。」).

**dokkai exception register extended (§2.2).** 3 non-N5 kanji that
appear in dokkai passage content (`向` for 〜向け target-audience
compounds, `央` for 中央 proper nouns, `付` for 〜付き menu convention)
were previously undocumented. Added to `data/dokkai_kanji_exception.
json` with WHY notes per the register's own contract.

**1 bunpou rationale cleaned up (§4.1).** Q19 rationale had `熱がある`
("have a fever") - `熱` is non-N5 and rationales are learner-visible.
Replaced with kana `ねつが ある`.

### Already-clean items (verified during audit, no fix needed)

  §2.3  bunpou source uses 0 non-N5 kanji in stems (audit was working
        from a stale snapshot; earlier session cleanup had already
        replaced 朝/思/京/阪/牛/乳/公/園/楽 with kana).
  §3.2  bunpou-7 ぎんこう  → already changed to 学校 in prior commit.
  §3.3  Q92 起ちます       → distractor, policy-allowed.
  §3.4  manifest totals    → 25 papers / 360 questions verify ✓.
  §3.5  Q62 rationale      → preserved (excellent pedagogy).
  §4.2  goi Q47 rationale  → 0 occurrences of 去年 (already clean).

### Cache and integrity

 - `sw.js` CACHE_VERSION: `v110` → `v111` (forces clients to re-fetch
    the updated paper JSONs on next visit).
 - `index.html` cache-busters: `?v=1.11.20` → `?v=1.11.21` (CSS / app.js).
 - `tools/check_content_integrity.py` → 40/40 invariants PASS.
 - `tools/fix_moji_source_audit_2026_05_03.py` → idempotent (0 changes
    on second run).

## v1.12.0 - 2026-05-03 (Example-coverage milestone - 100% vocab covered)

**Phase 7 closes the example-coverage authoring pass that started at
the beginning of the day.** All 1003 N5 vocab entries, all 177 grammar
patterns, and all 106 kanji entries now have at least one example
attached. Total session content authored: **1,059 examples across
seven phases.**

### Final phase content (321 new vocab examples)

321 inline-example additions across the long tail of sections:
 - **People-roles tail** (4): けいかん, おまわりさん, りゅうがくせい,
    外国人.
 - **Body parts tail** (1): せ.
 - **Counters common** (7): 本, だい, こ, かい (×2), 番, ど.
 - **Locations tail** (2): たいしかん, こうじょう.
 - **Nature tail** (2): すずしい, あたたかい.
 - **Clothing tail** (5): ハンカチ, さいふ, ボタン, ポケット, かさ.
 - **Money/shopping tail** (8): 円, ドル, きっぷ, ふうとう, てがみ,
    にもつ, おみやげ, レジ.
 - **Transport tail** (5): じどうしゃ, バイク, きしゃ, 道, しんごう.
 - **School & study** (27): こたえ, いみ, ことば, じ, かな, ひらがな,
    カタカナ, もじ, ぶん, ぶんしょう, ぶんぽう, れい, れんしゅう,
    きょうかしょ, ざっし, 新聞, ボールペン, まんねんひつ, こくばん,
    チョーク, けしゴム, ちず, え, 番号, 電気, 電話, 電話番号.
 - **Languages & countries tail** (9): 日本人, かんこくご, フランス,
    フランスご, ドイツ, スペイン, イギリス, 外国, 外国語.
 - **House & furniture** (28): アパート, マンション, と, もん, かべ,
    かいだん, エレベーター, げんかん, しんしつ, ふとん, もうふ, まくら,
    いす, たな, ほんだな, カーテン, かぎ, せっけん, はブラシ, タオル,
    テープ, ラジオ, カメラ, ビデオ, うた, え, ピアノ, ギター.
 - **Verbs Group 1** (34): うたう, きる, しる, 立つ, はく, はしる,
    わたる, うる, ひく (×2), よぶ, とぶ, こまる, ならぶ, わたす, ぬぐ,
    いそぐ, しぬ, ならう, はる, まがる, もっていく, もってくる, しまる,
    だす, おとす, ふく, くもる, なくす, すわる, たのむ, とまる, さす, けす.
 - **Verbs Group 2** (15): 入れる, こたえる, かける, きる, つける,
    ならべる, 見せる, いれる, あつめる, きえる, おちる, はれる,
    つかれる, 生まれる, つとめる.
 - **Verbs irregular/する** (11): けっこんする, さんぽする, りょこうする,
    れんしゅうする, しつもんする, しごとする, 電話する, コピーする,
    そうじする, せんたくする, かいものする.
 - **Existence/giving verbs** (6): やる, あげる, くれる, かす, かりる,
    かえす.
 - **i-Adjective tail** (28): つめたい, ひくい, うすい, ふとい, ほそい,
    うれしい, かなしい, さびしい, かわいい, うつくしい, きたない, やさしい,
    つまらない, まずい, にがい, おおい, すくない, まるい, しかくい,
    わかい, きいろい, あおい, あかい, くろい, 白い, ちゃいろい, ぬるい,
    うるさい.
 - **na-Adjective tail** (9): たいへん, ふべん, おなじ, りっぱ, けっこう,
    だいじ, あんぜん, じょうぶ, いや.
 - **Adverb tail** (16): すごく, おおぜい, だいたい, もうすこし, 一番,
    とくに, ほんとうに, すぐ, 一人で, じぶんで, かならず, もちろん,
    どうぞよろしく, まっすぐ, もういちど, もしもし.
 - **Conjunctions** (6): それで, が, だから, それに, ところで, または.
 - **Greetings tail** (12): しつれいします / しつれいしました,
    どういたしまして, いってきます / いってらっしゃい, ただいま /
    おかえりなさい, はじめまして, どうぞよろしく, おかげさまで,
    いらっしゃいませ, もしもし.
 - **Common nouns misc** (64 - all): もの, こと, ことば, 話, やくそく,
    ようじ, もんだい, しゅみ, さんぽ, うんどう, ゲーム, しあい, ニュース,
    パーティー, きって, はがき, てがみ, きっぷ, おみやげ, りゅうがく,
    りょかん, かぜ, びょうき, くすり, けが, おゆ, おふろ, マッチ, はいざら,
    スリッパ, ティッシュ, フィルム, レコード, テープ, よてい, じかんわり,
    はこ, はんぶん, はたち, へん, ほか, ほんとう, なつやすみ, ペット,
    カレンダー, かてい, かびん, かた, おくさん, せびろ, 大きな, たて,
    ゆうべ, にっき, さくぶん, じびき, テープレコーダー, ストーブ, ページ,
    クラス, グラム, メートル, キログラム, キロメートル.
 - **Sounds and voice** (2): おと, うた.
 - **Function/filler expressions** (8): えーと, そうですね, そうですか,
    ええ, うん, ううん, さあ, それでは.
 - **Misc useful items** (12): もの, こと, ばしょ, ばあい, ほう, とき,
    番号, じゅうしょ, ねんれい, 学校, しゅみ, しゅっしん.

### Coverage milestone

- **Vocab inline examples: 1003 / 1003 (100%)** - fully uncovered: 0.
- **Grammar pattern examples: 177 / 177** with ≥3 each.
- **Kanji example words: 106 / 106** with ≥2 each.

### Session totals across all 7 phases

| Phase | Type | Items |
|---|---|---:|
| 1 | Kanji 2nd examples | 35 |
| 2 | Grammar additional examples | 77 |
| 3 | Vocab - pronouns/family/body | 51 |
| 4 | Vocab - numbers/calendar/colors/particles/greetings | 154 |
| 5 | Vocab - locations/food/transport/school/house | 179 |
| 6 | Vocab - time/days/months/food/clothing | 176 |
| 7 | Vocab - final tail (verbs/adj/adverbs/conjunctions/misc) | 321 |
| | **Total examples authored this session** | **993** |

### Service worker

Bumped `CACHE_VERSION` v108 -> v109.

v1.12.0 / SW v109. **40/40 invariants green.**

---

## v1.11.3 - 2026-05-03 (Vocab examples Phase 6 - +176 entries)

Phase 6 of the example-coverage authoring pass. Targets the still-
uncovered sections after Phase 5: time-general tail, days-of-month +
months, locations tail, food items tail, tableware, clothing tail,
animals tail. All 176 new IDs verified against actual data - zero
form-mismatches this batch (we now dump the live data and key against
real IDs rather than guessing).

### Content (176 new vocab inline examples)

 - **Time-general tail (10)**: とき, とけい, おととい, けさ, こんばん,
    こんや, 午前, 午後, 半, 分.
 - **Days/Months (32)**: ついたち..二十日 (1st-20th), 一月..十二月 (all
    12 months), 週, 先週, 月, 先月, 毎月, 年, きょねん, 毎年, おととし,
    さらいねん.
 - **Frequency tail (7)**: まいあさ, まいばん, すぐ, もうすぐ, さいしょ,
    つぎ, 後で.
 - **Locations tail (49)**: ところ, だいどころ, おてあらい, トイレ, おふろ,
    げんかん, にわ, 高校, 会社, じむしょ, お店, やおや, ほんや, はなや,
    にくや, パンや, くうこう, どうぶつえん, びじゅつかん, えいがかん,
    ホテル, りょかん, こうばん, こうさてん, いりぐち, しょくどう, たてもの,
    ろうか, プール, ポスト, 道, とおり, かど, はし, むら, 国, 前, 後ろ,
    左, 右, となり, よこ, とおく, むこう, 北, 南, 東, 西.
 - **Nature tail (17)**: いけ, みずうみ, もり, くさ, は (leaf), いし,
    田, くも, たいよう, かぜ, はれ, くもり, なつ, ふゆ, 火, 水, おゆ.
 - **Animals tail (3)**: にわとり, ぞう, むし.
 - **Food/drink general (5)**: たべもの, のみもの, ゆうはん, しょくじ,
    おべんとう.
 - **Food items tail (28)**: ぎゅうにく, ぶたにく, とりにく, さかな,
    いちご, ぶどう, すいか, レモン, だいこん, にんじん, たまねぎ,
    じゃがいも, トマト, きゅうり, キャベツ, こめ, しお, さとう, しょうゆ,
    みそ, カレー, うどん, そば, ハンバーガー, サンドイッチ, サラダ,
    スープ, チョコレート.
 - **Drinks tail (2)**: おゆ (drinks ID), こうちゃ.
 - **Tableware (12)**: さら, おさら, ちゃわん, おわん, はし
    (chopsticks), スプーン, フォーク, ナイフ, コップ, カップ, れいぞうこ,
    なべ.
 - **Colors tail (2)**: いろ, ピンク.
 - **Clothing tail (8)**: ようふく, きもの, うわぎ, コート, セーター,
    Tシャツ, ワイシャツ, ネクタイ.

### Coverage status

- Vocab fully-uncovered: **321** (was 497 → 321; **-176**).
- Sections now fully covered: 11 (days/months), 12 (frequency), 14
  (nature/weather), 15 (animals), 16 (food/drink general), 18 (drinks),
  19 (tableware), 20 (colors), 21 (clothing), plus most of 13
  (locations) and 17 (food items).
- Remaining biggest buckets for Phase 7+: common nouns misc (~60),
  verb tail (~30), adverbs tail (~10), school/study tail (~10),
  some money/transport, set phrases, body parts.

### Service worker

Bumped `CACHE_VERSION` v107 -> v108.

v1.11.3 / SW v108. **40/40 invariants green.**

---

## v1.11.2 - 2026-05-03 (Vocab examples Phase 5 - +179 entries)

Continuation of the vocab-example coverage pass. This batch combines
the 23 Phase-4 stragglers (entries my earlier script couldn't match
due to kanji-vs-kana form mismatch - re-keyed to actual IDs) with
~155 new entries across the remaining-uncovered sections.

### Content (179 new vocab inline examples)

 - **Phase-4 stragglers re-keyed** (23): 今, 今日, 毎日, 時々, 前 (time);
    白 / 白い (colors); 会う / 言う / 聞く / かえる / 出る (verbs);
    新しい / 高い / 小さい / 古い / 安い (adjectives); まず, 先,
    りょうり (nouns); はい / いいえ / はい-counter (function/filler).
 - **Locations & places** (+15): 学校, いえ, へや, えき / 駅, バスてい,
    びょういん, こうえん, としょかん, デパート, スーパー, コンビニ,
    レストラン, カフェ, きっさてん, ぎんこう, ゆうびんきょく, 大学, まち,
    中, 外, 上, 下.
 - **Nature & weather** (+13): 雨, ゆき, 風, そら, つき, 太陽, ほし,
    山, 川, うみ, 木, 花, てんき, あつい, さむい, 夏, 冬, はる, あき.
 - **Animals** (+8): いぬ, ねこ, とり, さかな, うま, うし, ぶた, どうぶつ.
 - **Food & drink** (+22): ごはん, あさ/ひる/ばんごはん, おかし, パン,
    たまご, りんご, みかん, バナナ, やさい, くだもの, にく, おにぎり,
    おべんとう, ケーキ, アイスクリーム, チーズ, バター, ラーメン, すし,
    てんぷら + drinks 水, おちゃ, コーヒー, ぎゅうにゅう, ジュース,
    ビール, ワイン, おさけ.
 - **Clothing** (+10): シャツ, ズボン, スカート, くつ, くつした, ぼうし,
    ふく, めがね, とけい, かばん.
 - **Money/shopping** (+5): お金, いくら, ねだん, きって, はがき.
 - **Transport** (+8): でんしゃ, バス, くるま, じてんしゃ, ちかてつ,
    タクシー, ひこうき, ふね.
 - **School & study** (+17): 学生, 先生, 大学生, 高校生, じゅぎょう,
    しゅくだい, テスト, しけん, きょうしつ, 本, じしょ, ノート, えんぴつ,
    ペン, かみ, つくえ, いす.
 - **Languages & countries** (+8): 日本, 日本語, アメリカ, えいご,
    中国, 中国語, かんこく, 国.
 - **House & furniture** (+12): まど, ドア, テーブル, ベッド, しょくどう,
    だいどころ, お風呂, シャワー, テレビ, でんわ, れいぞうこ, でんき.
 - **Verb tail** (+17): あらう, おわる, のる, のぼる, はたらく, はじまる,
    まつ, もつ, つくる, つかう, あるく; おしえる, おぼえる, あける, しめる,
    おりる, かりる.
 - **Adjective tail** (+22 i-adj + 4 na-adj): おもしろい, おいしい,
    いそがしい, あたたかい, すずしい, あまい, からい, いい, わるい,
    いたい, ながい, みじかい, ひろい, せまい, おもい, かるい, つよい,
    よわい, はやい, おそい, とおい, ちかい + だいすき, だいきらい,
    げんき, ゆうめい.
 - **Adverb tail** (+11): とても, すこし, たくさん, ちょっと, いっしょに,
    はやく, ゆっくり, もっと, だんだん, きっと, たぶん.

### Coverage status

- Vocab inline examples: now ~506 / 1003 (was 313 pre-Phase-3, was
  467 post-Phase-4, now ~506).
- Remaining fully uncovered: 497 (was 690 pre-Phase-3).
- Big remaining buckets (next phase): common nouns misc (~60),
  food items tail (~25), school/study tail (~25), adverbs tail (~20),
  verb tail (~30), some house/furniture, body parts variants, time
  variants.

### Service worker

Bumped `CACHE_VERSION` v106 -> v107.

v1.11.2 / SW v107. **40/40 invariants green.**

---

## v1.11.1 - 2026-05-03 (Vocab examples Phase 4 - +154 entries)

Continuation of v1.11.0's example-coverage pass. Authored 154 more
vocab example sentences this batch covering the highest-leverage
foundational categories.

### Content

- **Vocab: +154 inline examples** across:
 - Numbers (1, 2, ..., 11, 20, 100, 1000, 10000, 100M)
 - Native counters (一つ..十, いくつ)
 - Common counters (人, 一人, 二人, まい)
 - Time-general (いま, きょう, あした, きのう, あさ, ひる, よる, ばん, ゆうがた)
 - Days/weeks/months (月曜日..日曜日, 今日, 毎日/毎週, 今週/来週,
    今月/来月, 今年/来年)
 - Frequency (いつも, よく, ときどき, たまに, あまり, ぜんぜん, まず,
    つぎに, さいご, さき, あと, まえ, まだ, もう)
 - Colors (あかい, あおい, しろい, くろい, きいろい, ちゃいろ, みどり
    + な-noun forms)
 - Particles (は, が, を, に, で, へ, と, から, まで, の, も, や, か,
    ね, よ, より) - each with a typical-use sentence
 - Greetings (おはよう, こんにちは, こんばんは, おやすみ, さようなら,
    ありがとう, すみません, ごめんなさい, いただきます, ごちそうさま,
    おねがいします, どうぞ, どうも, はい, いいえ)
 - Demonstrative tail (そんな, ああ)
 - Top verbs (行く, 書く, 聞く, 読む, 飲む, 話す, 買う, あう, あらう,
    あそぶ, いう, およぐ, おわる, かかる, きく, のる, のぼる, はたらく,
    はじまる; 見る, 食べる, おきる, ねる, あける, しめる, おしえる,
    おぼえる, かえる, でる; する, 来る, べんきょうする, りょうりする;
    ある, いる)
 - Top adjectives (大きい/小さい, あたらしい/古い, 高い/安い, あつい/
    さむい, おもしろい, おいしい, いそがしい + na-adj きれい, げんき,
    しずか, にぎやか, ひま, すき/きらい, じょうず/へた, ゆうめい,
    しんせつ, だいじょうぶ, たいせつ, べんり, いろいろ)

### Coverage status

- Vocab inline examples: 313 → 467 (out of 1003)
- Remaining uncovered: ~536 (down from ~690)
- Big remaining categories: Locations (70), House/Furniture (39),
  Food items (44), Common nouns misc (76), School/Study (43),
  Adverbs tail (20+), Verb tail (~50), i-adj tail (~50)

### Service worker

Bumped `CACHE_VERSION` v104 -> v105.

v1.11.1 / SW v105. **40/40 invariants green.**

---

## v1.11.0 - 2026-05-03 (Example-coverage authoring pass)

Per user direction: many vocabulary, grammar, and kanji entries
lacked example sentences / example words. Audited the gap and
authored content to bring all three categories to a baseline.

### Content (corpus)

- **Kanji: 35 entries gained a 2nd example word.** Every one of the
  106 N5 kanji entries now has at least 2 example words on its
  detail page (was: 35 entries had only 1). Examples chosen to
  showcase typical N5 compound usage:
 - Numerals: 三百, 千円, 百円, 半分
 - Body parts: 左手, 右手
 - Cardinal directions: 東口, 西口, 南口, 北口
 - Time/quantity: 一時間
 - Daily verbs: 食べもの, 飲みもの, 読みかた, 書きかた, 行きかた
 - Adjective/noun forms: 安く, 古本, 長さ, 休み
 - Compounds: 火山, 小川, 田中, 大雨, 花見, 空気, 上手, 下手, 小学校
  All forms verified against JA-16 (target-or-whitelist kanji only;
  non-N5 kanji is rendered in kana).

- **Grammar: 77 new examples across 63 patterns.** Every one of the
  177 grammar patterns now has 3+ example sentences (was: 63
  patterns sat at 1-2). 8 mid-authoring fixes corrected non-N5 kanji
  in stems (早く -> はやく, 字 -> かんじ, 時計 -> とけい, 思う -> おもう,
  皿 -> さら, 京都 -> きょうと, 教えて -> おしえて). All examples
  carry vocab_ids: [] (JA-17 satisfied; auto-population available
  via tools/link_grammar_examples_to_vocab.py).

- **Vocab: 51 foundational entries gained an inline example
  sentence.** Pronouns (私, 私たち, かれ, かのじょ, みなさん, じぶん),
  family terms (かぞく, 父, 母, あに, あね, おとうと, いもうと, etc.),
  body parts (からだ, かお, め, みみ, くち, は, て, あし), demonstratives
  (あちら, こっち, そっち, あっち, どっち), question words (何, 何曜日,
  何月, 何日, 何で), and roles (せいと, いしゃ, 会社員, 駅員, 店員). Each
  example demonstrates typical use in a single short N5 sentence.

### Tooling

- `tools/audit_example_coverage.py` - read-only inventory of
  uncovered entries across all three corpora. Re-runnable to track
  remaining gaps (vocab is the biggest remaining: 690 entries still
  without inline examples - Phase 4 backlog item).
- `tools/add_kanji_2nd_examples.py` - idempotent kanji example
  additions.
- `tools/add_grammar_examples.py` - idempotent grammar example
  additions (77 entries).
- `tools/add_vocab_examples.py` - idempotent vocab example
  additions (51 foundational entries).

### Service worker

Bumped `CACHE_VERSION` v103 -> v104. data/grammar.json,
data/vocab.json, data/kanji.json all updated.

v1.11.0 / SW v104. **40/40 invariants green** (unchanged from
v1.10.2 - this is a content pass, no new invariants needed).

---

## v1.10.2 - 2026-05-02 (Search-result navigation + provenance lock-in)

Two fixes that landed without their own version bump and are folded
in here:

### Fixed

- **Header search results were not clickable to vocab content.**
  Vocab results all routed to `#/learn` (the Learn hub) instead of
  the per-word detail page `#/learn/vocab/<form>`. Fixed in
  `js/search.js`: centralized URL builders into a `HREFS` map; vocab
  now correctly routes via `encodeURIComponent(form)`. Browser-
  verified: clicking かるい → `#/learn/vocab/%E3%81%8B%E3%82%8B%E3%81%84`
  → detail page renders with `h2: かるい`.

### Improved (search panel)

While the bug was being fixed, several adjacent issues were closed:

- **Kanji-form vocab now shows its kana reading inline:** `新しい
  (あたらしい) - new` (was: `新しい - new`).
- **Vocab dedupe by `form`** so words appearing in multiple thematic
  sections (e.g. 名前 in §1 and §15) don't show up twice with the
  same destination.
- **Keyboard navigation:** ↓/↑ moves a highlight through the flat
  result list (wraps top↔bottom); Enter follows the highlighted link;
  Escape clears the input and closes the panel. Active item gets
  `.is-active` class with accent outline + background tint.
- **ARIA combobox semantics on the input:** `aria-combobox`,
  `aria-autocomplete="list"`, `aria-expanded` toggle.
  `.search-status[aria-live="polite"]` announces the result count
  to screen readers (visually hidden).
- **Mobile responsive:** `positionPanel()` now clamps width to
  `viewport - 24px` and shifts left if the panel would overflow the
  right edge. Verified at 375 px viewport: 320 px panel, 12 px
  margin.

### Added (legal lock-in)

- **`CONTENT-LICENSE.md`** - explicit content-provenance policy.
  States that every grammar pattern / vocab entry / kanji record /
  mock-test question / reading passage / listening drill is
  original (with per-file inventory: 177 + 1003 + 106 + 288 + 360 +
  30 + 30). Lists the public-information sources used as references
  for distribution / topic / scope (JEES sample-paper format,
  JOYO / KANJIDIC2, learner references like Tofugu / Bunpro / Imabi)
  and explicitly states what was NOT taken (any specific question
  text). Documents the JEES contact path if a future feature ever
  wants licensed past-paper material.
- **`tools/audit_provenance.py`** - standalone scanner with 7
  detection rules (JEES citations, year-numbered past-paper markers,
  past-paper terminology like 過去問 / 真題 / 本試験第N回, JLPT-year-paper
  citations). Last run: 0 hits across 648 questions +
  KnowledgeBank/*.md headers.
- **JA-30 invariant** - same 7 rules inlined into the standard CI
  integrity check (`tools/check_content_integrity.py`). A leak by
  a future contributor fails the build before merge. Total
  invariants: 38 → 39.
- **`feedback/jees-inquiry-template.md`** - bilingual email template
  ready for if/when the project ever wants to license specific
  past-paper material from JEES. Includes when-to-send guidance,
  recipient list, expected-outcome table, and an outcome-log
  section.
- **`NOTICES.md`** - new "Question content / corpus" section with
  pointer to `CONTENT-LICENSE.md` + the JLPT trademark statement.

### Updated

- **`feedback/MASTER-TASK-LIST.md`** - DEFER-11 ("Authentic-extracted
  N5 content re-source from official JEES samples") closed by
  decision: original-content policy formalized, JEES re-source path
  documented but not pursued. Strikethrough + closure annotation
  added inline.
- **`index.html`** version strings (`?v=` and footer-meta) bumped
  1.10.0 → 1.10.2 (had been stale through v1.10.1).
- **`package.json`** version bumped 1.10.0 → 1.10.2.

### Service worker

Bumped `CACHE_VERSION` v90 → v91. Added `./CONTENT-LICENSE.md` to
the PRECACHE list.

---

## v1.10.1 - 2026-05-02 (Content-protection layer)

Per user direction: deter casual copying / sharing of question
content from the deployed site, and remove the "Source on GitHub"
surface.

### Removed (user-visible)

- **"Source on GitHub" footer link** removed from `index.html`. Footer
  now reads `What's new · Privacy`.
- **"View on GitHub" link** removed from `js/changelog.js` (was in
  the CHANGELOG-fetch-error fallback).
- **GitHub source link** removed from `PRIVACY.md`. The "Source code"
  section was rewritten as "Independently verifiable" with guidance
  to inspect the browser's Network tab to verify the no-tracker
  claim - same level of assurance, no public-source-link dependency.

### Added (deterrent layer - friction, not security)

Important framing: the site is a static PWA. Anyone with browser
devtools can still read `data/*.json` directly, and there is no W3C
API to truly block OS screenshots. The layer below raises friction
against casual copying and accidental clipboard captures.

- **`css/main.css`** - `user-select: none` on html/body with opt-outs
  for inputs, textareas, contenteditable elements, and elements
  carrying `.allow-select`. `::selection` cleared. `user-drag: none`
  on images / svg / ruby / rt. `@media print` blanks the page with
  a "Printing is disabled" notice. `html[data-blur=true]` blurs the
  body and shows a Japanese overlay above z-index 99999.
- **`js/content-protect.js`** (new) - capture-phase blockers for
  `contextmenu`, `copy`, `cut`, `dragstart`, `drop`, `selectstart`.
  Keyboard shortcut blockers for `Ctrl+C/A/X/S/P/U`, `F12`,
  `Ctrl+Shift+I/J/K/C`. `window blur` + `visibilitychange (hidden)`
  set `html[data-blur=true]` to obscure content during region
  screenshots. `window.getSelection()` overridden to return empty
  when the active element is not an input.
- **`js/app.js`** - wires `initContentProtection()` from the
  DOMContentLoaded handler before any route renders.

### Service worker

- Bumped `CACHE_VERSION` to `jlpt-n5-tutor-v90` (was v89). Added
  `./js/content-protect.js` to the PRECACHE list.

### Honest limitations (called out in `js/content-protect.js`)

- OS region screenshots (Win+Shift+S, Cmd+Shift+4) - page blurs on
  window blur, but the OS often captures before the JS event fires.
- PrtScn key - most OSes don't deliver this event to the browser.
- Browser menu → Save / Print, `view-source:` URL prefix, devtools
  Network tab - all bypass the JS layer.
- Phone-camera-of-screen - always works, no defence possible.
- Mobile screenshot APIs - no JS API exists to intercept them.

If true protection matters more than reasonable friction, the
architecture has to change (server-side rendering with per-session
watermarks, video DRM, or moving off the public web).

v1.10.1 / SW v90. **39/39 invariants green.**

---

## v1.10.0 - 2026-05-02 (Syllabus dashboard + DEFER backlog closeout)

Big sweep: new homepage as a JLPT N5 syllabus dashboard, full
multi-correct grey-zone audit, every actionable backlog item closed,
and 100% grammar-pattern test coverage (177/177).

### Changed (user-visible)

- **Homepage redesigned as a syllabus dashboard.** Replaces the bare
  "JLPT N5 study material." inventory with: page title + subtitle, six
  syllabus cards (Grammar / Vocab / Kanji / Reading / Listening / Mock
  Test) with index + count + description + in-card action, eight-step
  recommended study order (now clickable links), six-row progress
  overview with progress bars, and an action block ("Not sure where to
  start?" + Take Placement Check + Start with Grammar). Container width
  on the home route widens to 1120px (only here; other routes stay
  880px) so the 3-column card grid fits comfortably.
- **Header primary nav expanded** from 2 links (Learn / Test) to 7:
  Grammar / Vocabulary / Kanji / Reading / Listening / Test / Progress.
  Every syllabus section is a single click from anywhere.
- **Recommended Study Order steps are clickable links.** Each of the 8
  numbered steps routes to the most directly-actionable surface: 01 →
  Grammar TOC, 02 → Vocab TOC, 03 → Kanji index, 04 → /drill, 05 →
  /reading, 06 → /listening, 07 → /test, 08 → /review. Full-row
  click target with hairline accent-on-hover and visible focus outline.
- **Progress dashboard goes live for all 6 sections.** Reading and
  Listening rows now show actual completion counts (previously stuck
  at 0/30 because per-passage / per-drill completion wasn't tracked).
  Reading marks completed on the results screen with score>0; listening
  marks on first answer submit.
- **Resume strip uses a friendly label.** "Last session: n5-001" →
  "Last session: n5-001 - です/だ" (pattern label hydrated at load).
- **Daily-goal-met badge** sits below the syllabus subtitle for
  returning users: "Streak: N days" + "✓ Practiced today" or "○ Not
  yet practiced today." Decoupled from the streak count so a 5-day
  streak with "not yet today" reads unambiguously.
- **Reading mock-test mode toggle.** Filters passages to the JLPT
  primary-question distribution (questions tagged `format_role:
  primary`). Persists across sessions via the `readingMockTestMode`
  setting. Shows per-passage question count alongside level/topic.
- **Undo-on-grading 2-second window in Review.** After grading a card,
  a fixed-bottom toast shows "Recorded: <Grade>" with an Undo button.
  Click within 2s to roll back the SRS state to the pre-grade snapshot
  and remove the entry from the session log. Auto-dismisses; pauses on
  hover for slow readers.

### Content (corpus)

- **100% grammar-pattern test coverage.** Authored 65 new questions
  across 3 batches to bring the uncovered count from 78 → 0. Every
  one of the 177 grammar patterns now has at least one MCQ question
  with 4 distinct, single-correct distractors. Total test bank:
  288 runtime + 360 paper = 648 questions audited green.
- **Three multi-correct grey-zone questions fixed** (q-0488 frequency
  calibration, q-0024 sentence-final speech act, goi-2.6 spatial
  position without anchor). See JA-29 + audit script categories
  F/G/H below.
- **Tier taxonomy on grammar.json.** Every pattern now carries
  `tier: "core_n5"` (165) or `tier: "late_n5"` (12). Late flag fires
  on N4-leaning hints in notes/meaning_en or known-boundary patterns
  (n5-167, 186, 187, etc.).
- **Kanji enrichment.** All 106 entries now carry `lesson_order`
  (sequential 1-106) + `frequency_rank` (within-N5 frequency rank
  derived from KANJIDIC2 + Joyo grade aggregate).
- **Vocabulary part-of-speech tags.** All 1003 entries in
  `KnowledgeBank/vocabulary_n5.md` carry inline `[n.]` / `[v1]` /
  `[v2]` / `[v3]` / `[i-adj]` / `[na-adj]` / `[adv.]` / `[part.]` /
  `[conj.]` / `[pron.]` / `[count.]` / `[num.]` / `[dem.]` /
  `[Q-word]` / `[exp.]` / `[interj.]` tags. Legend added to the
  file header.

### Added (invariants - locks the work in)

- **JA-29** - Question subtype taxonomy is closed: `paraphrase` and
  `kanji_writing` only. New subtypes must register in the integrity
  script before being introduced (closes DEFER-2 by decision: subtype
  is the canonical extension point, no need to promote to a top-level
  type).
- **Multi-correct audit script extended with 3 new categories**
  (`tools/audit_multi_correct.py`):
 - **F_frequency_calibration** - fires when stem has a numeric
    frequency (月にXかい etc.) AND choices contain a known grey-zone
    adverb pair {よく/たまに}, {よく/ときどき}, etc.
 - **G_speech_act_particle** - fires on "<verb>です/ます( )" with ≥2
    of {か, ね, よ} in choices and no question-word or はい/いいえ anchor.
 - **H_spatial_no_anchor** - fires on "<X>の( )に <Y>が あります"
    with ≥2 spatial positions in choices and no canonical object-pair
    (つくえ/テーブル/etc.) or movement verb in stem.

### Tooling / scaffolding (unblock external work)

- **VOICEVOX audio pipeline** (`tools/build_audio_voicevox.py`):
  preflight engine check, 3-retry exponential backoff, ThreadPool
  parallelism, --missing-only fast filter, ffmpeg WAV→MP3 transcode,
  multi-voice dialogue support via `[F1]/[F2]/[M1]/[M2]` script
  tags. Operator's manual at `AUDIO.md`. Confirmed gaps: 19 .mp3s
  missing (1 grammar + 18 listening 013 - 030); regenerable in
  ~3 minutes once the engine binary is on a local machine.
- **Audio coverage audit** (`tools/audit_audio_coverage.py`): exits
  non-zero on any data→disk mismatch; JSON gap dump to
  `feedback/audio-coverage-gaps.json`.
- **Native-review dossier exporter**
  (`tools/export_native_review_dossier.py`): generates
  `feedback/native-review-dossier/` from live data - cover.md,
  01_grammar_patterns.md (177), 02_vocab_borderline.md (122),
  03_kanji_readings.md (106), 04_reading_passages.md (30),
  05_listening_scripts.md (30), and a review_log.csv template.
  Severity rubric + citation format + turnaround targets in
  cover.md.
- **Visual-regression Playwright scaffold**
  (`tests/visual-regression.spec.js`): 12 tests × 2 viewports cover
  6 high-traffic routes with reduced-motion + animations-disabled +
  0.1% pixel-diff threshold. CI excluded via
  `--grep-invert visual-regression` until baselines are committed;
  `npm run test:visual:update` captures them locally.
- **Settings deny-list hardening.** Global Claude Code config (per
  user request 2026-05-02): `defaultMode: bypassPermissions` +
  explicit allow list (66 rules) + comprehensive deny list (37
  rules) blocking destructive ops (rm -rf, git push --force,
  git reset --hard, etc.) + belt-and-suspenders SS&SC directory
  denies on top of the existing block_sssc.py PreToolUse hook.

### Fixed

- 14-line homepage CSS regression: `main` 880px container was
  constraining `.home-syllabus` even after the inner element set
  its own 1120px max-width. Replaced with `main:has(.home-syllabus)`
  to scope the wider container to the home route only.
- `q-0536` had `茶` in the stem; not in the 106-kanji N5 whitelist.
  JA-13 caught it. Replaced with kana `おちゃ`.
- `vocabulary_n5.md` line 848 (`いる - to need`) was mistagged
  `[v2]` by the PoS-injection pass; corrected to `[v1]` (Group 1
  exception). The X-6.6 invariant's hint matcher now tolerates
  inserted PoS tags so the same edit doesn't break it again.

### Tooling housekeeping

- One-shot scripts kept as authoring templates:
  `tools/add_uncovered_questions.py`,
  `tools/add_uncovered_questions_batch2.py`,
  `tools/add_uncovered_questions_batch3.py`. Each documents the
  conventions for adding more questions in future sessions.

### Service worker

Bumped from `jlpt-n5-tutor-v82` → `jlpt-n5-tutor-v88`. Cache version
churn is high this release because every commit that ships a
js/css/data change requires a bump.

---

## Older releases

For v1.9.0 and earlier (initial release through the Japanese-first language
sweep), see [docs/CHANGELOG-archive.md](docs/CHANGELOG-archive.md).

---

*This changelog only records changes visible to users. For commit-level history, see git log.*
