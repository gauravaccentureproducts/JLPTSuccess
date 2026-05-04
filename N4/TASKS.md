# JLPT N4 Tutor — Tasks

**Last updated:** 2026-05-04 (Pass-3 priority items complete; v0.2.0 — ALL 41 invariants PASS)

## Live site

- Repo: `https://github.com/<org>/jlpt-n4-tutor` (configure on first deploy)
- Live URL: `https://<org>.github.io/jlpt-n4-tutor/` (configure)
- Engine tests: 0/0 (`tests.html` ported; needs N4-specific test data)
- CI invariants: **41/41 PASS** (all green)

## Status snapshot

- **Version:** v0.2.0 (Pass-3 priority items complete)
- **SW version:** `jlpt-n4-tutor-v1`
- **Grammar:** 307 patterns (178 N5 prerequisite + 129 N4) with explanation/form_rules/examples seeded
- **Vocab:** 1672 entries (1041 N5 prerequisite + 631 N4 from full JLPT Sensei fetch)
- **Kanji:** 249 glyphs + 249 stroke-order SVGs in svg/kanji/. 183 KB entries have examples lines.
- **Reading:** 30 short passages embedded in dokkai_questions_n4.md
- **Listening:** 30 chokai items + 30 synthetic MP3s
- **Questions:** 591 total (100 moji + 100 goi + 100 bunpou + 102 dokkai + 189 ext)
- **Mock-test papers:** 28 papers across 4 categories (402 questions in data/papers/)
- **Audio:** 80 MP3s rendered (50 grammar + 30 listening; remaining grammar can render in subsequent passes)
- **Locales:** 5 (en/vi/id/ne/zh) — shell ported, N4 strings TBD
- **Routes:** 21 routes wired in router; all primary content routes have data

## External-blocked backlog

- **EB-1:** Native-recorded listening audio. Ship synthetic gtts in v1; native re-record per item in v2.
- **EB-2:** Native-teacher review. Ship LLM-only audit in v1; native sign-off in v2.
- **EB-3:** Translation of brief to Japanese. v2.
- **EB-4:** FSRS-4 SRS migration. SM-2 in v1.
- **EB-5:** Stroke-order SVGs for 280 kanji (KanjiVG fetch). Pass-2.

## Pass-1 (initial skeleton, 2026-05-04)

### Done

- [x] Repo skeleton at `<JLPT-root>/N4/`, git init.
- [x] Directory structure per spec §29.
- [x] Copied 7 directories from N5: `.claude`, `.github`, `css`, `fonts`, `js`, `locales`, `tools`.
- [x] Copied 6 root files from N5: `index.html`, `manifest.webmanifest`, `sw.js`, `tests.html`, `playwright.config.js`, `package.json`.
- [x] Token substitution `n5` → `n4`: `jlpt-n5-tutor`, `JLPT N5`, `n5_kanji_*`, `n5_vocab_*`, `grammar_n5`, `vocabulary_n5`, `kanji_n5`, `*_questions_n5`.
- [x] Brand kanji `五` → `四` in `css/main.css`.
- [x] Favicon SVG embedded data URI: `N5` → `N4` in `index.html`, `manifest.webmanifest`.
- [x] SW cache version reset: `jlpt-n4-tutor-v1`.
- [x] `data/*.json` skeleton: 6 entity files + 3 whitelist files + audio_manifest + papers/manifest, all empty arrays + populated `_meta`.
- [x] `KnowledgeBank/*.md` skeleton: 9 files (3 catalogues + 5 question files + sources).
- [x] N4-specific top-level files: `README.md`, `CHANGELOG.md`, `TASKS.md` (this file), `MEMORY.md`, `PRIVACY.md`, `CONTENT-LICENSE.md`, `NOTICES.md`.
- [x] N4 spec lives at repo root: `procedure-manual-build-next-jlpt-level.N4.md`.
- [x] Bootstrap inventories present: `n4-grammar-inventory.md`, `n4-kanji-inventory.md`, `n4-vocab-inventory-sample.md`, `n4-inventory-manifest.md`, `N4-PLANNING.md`.

### Deferred (defaults applied per N4 spec §39.2 / §0.A.2)

- **Native voice budget** → synthetic TTS via gtts. Mark all listening items `voice: "synthetic"`. v2 native re-record per item.
- **Native teacher review** → LLM-only via `tools/llm_audit.py`. Mark all hand-authored entries `review_status: "llm_only"`.
- **Translation of brief to Japanese** → English-only ship. EB-3.
- **Subscription / monetisation** → free, no monetisation.
- **SRS algorithm** → SM-2 (FSRS-4 deferred to v2).
- **Handwriting kanji practice** → defer to v2.
- **IME-typing input mode** → defer to v2 (kana-strict in v1).
- **Reading-comprehension speed test** → defer to v2.
- **Mock test mode timing** → use JLPT.jp official N4 timing (125 min total: 30/60/35).

## Pass-2 (seed corpus complete, 2026-05-04)

### Layer 0 — verify CI (DONE)

- [x] Run `python tools/check_content_integrity.py`: 35/41 invariants PASS.
- [x] 6 FAIL all in JA-8 (Q-count, expected for empty question banks).

### Layer 3 — Kanji whitelist + catalogue (DONE)

- [x] Built `data/n4_kanji_whitelist.json` from `n4-kanji-inventory.md` + N5 prerequisites = 249 glyphs (24 inventory entries overlapped with N5).
- [x] Built `data/n4_kanji_readings.json` per glyph: on/kun/primary.
- [x] Authored `KnowledgeBank/kanji_n4.md`: structured catalogue (JA-12 PASS, all 249 entries).
- [x] X-6.9 PASS (primary-reading sanity).
- [ ] Fetch KanjiVG SVGs into `svg/kanji/` — Pass-3.
- [ ] Per-glyph examples from full vocab corpus — Pass-3.

### Layer 4 — Vocabulary corpus (SEED done; full corpus deferred to Pass-3)

- [x] Authored `KnowledgeBank/vocabulary_n4.md` SEED: 1159 entries (1041 N5 prerequisite + 118 N4 from a-h sample).
- [x] Per-WORD PoS rule applied (suru-nouns generate two entries: [n.] + [v3]).
- [x] `tools/build_n4_vocab.py` derives `data/vocab.json`.
- [x] JA-31 PASS (vocab PoS parity, homograph-aware).
- [ ] Extend to full ~600 N4 entries from Tanos N4 CSV — Pass-3.

### Layer 5 — Grammar catalogue (SEED done; examples + form_rules deferred to Pass-3)

- [x] Authored `KnowledgeBank/grammar_n4.md`: 307 patterns (178 N5 prerequisite + 129 N4 from inventory).
- [x] 18-category structure per spec.
- [x] Out-of-scope kanji kana-folded (場合は -> ばあいは, 必要 -> ひつよう, 頃 -> ころ).
- [x] Meta-topics dropped (意向形, 受身形, 他動詞 & 自動詞).
- [x] `tools/build_n4_grammar.py` derives `data/grammar.json`.
- [ ] form_rules + examples + common_mistakes per pattern — Pass-3.
- [ ] Cross-reference Bunpro N4 / Genki II / Minna II — Pass-3.

## Pass-3 (post-seed content authoring, target 2026-08-04)

### Layer 6 — Reading + Listening (~6-10 hr)

- [ ] Author `KnowledgeBank/dokkai_questions_n4.md`: ~30 passages per spec §15.
- [ ] Author `KnowledgeBank/chokai_questions_n4.md`: ~30 listening items per §16.
- [ ] `tools/build_audio.py` synthetic TTS pass.

### Layer 7 — Question banks (~12-24 hr) — JA-8 RELEASE BLOCKER

- [ ] `moji_questions_n4.md` 100 questions per Mondai 1/2/3.
- [ ] `goi_questions_n4.md` 100 questions per Mondai 4/5/6.
- [ ] `bunpou_questions_n4.md` 100 questions per Mondai 1/2/3.
- [ ] `dokkai_questions_n4.md` 102 questions linked to ~30 passages.
- [ ] `externally_sourced_n5.md` 189 third-party-sourced questions (filename per integrity check).
- [ ] Total target: 591 questions.
- [ ] `tools/scan_multi_correct.py` — fix every flag.
- [ ] `tools/heuristic_audit.py` — apply auto-fixes.
- [ ] `tools/build_papers.py` — slice into 15-question papers.

### Layer 8 — Audit + tests + deploy

- [ ] `tools/llm_audit.py` over question banks (~$10-15 API).
- [ ] `tools/coverage_compare.py` vs jlptsensei.com / tanos.co.uk.
- [ ] Browser smoke test via `tests-e2e/p0-smoke.spec.js`.
- [ ] Lighthouse CI green: PWA=100, Perf≥90 mobile, A11y≥95.
- [ ] axe-core scan: zero serious / critical violations.
- [ ] First deploy to `<org>.github.io/jlpt-n4-tutor/`.
- [ ] Tag `v1.0.0`.

## Pass-4 (post-launch, target 2026-09-04)

- [ ] Native-teacher review of grammar patterns (commission reviewer).
- [ ] Native-recorded listening audio for top-priority items.
- [ ] Coverage gap fixes from Pass-3 §coverage_compare.
- [ ] FSRS-4 SRS migration.

## Known limitations (v0.1.0-alpha)

- Question banks empty (591 expected) — JA-8 release blocker; Pass-3 deliverable.
- Reading / Listening corpora empty — Pass-3 deliverable.
- Vocab corpus is SEED (118 N4 entries) — full Tanos fetch in Pass-3.
- Grammar form_rules / examples / common_mistakes are placeholders — Pass-3 enrichment.
- No audio MP3s — synthetic gtts runs in Pass-3 against authored content.
- No N4-specific Playwright tests yet.

## Recommended next action

Pass-3 Layer 7 (question banks) is the JA-8 release-blocker. Authoring 591 questions across moji/goi/bunpou/dokkai/externally_sourced is ~12-24 hr of focused content work. Recommend doing it after the full Tanos N4 vocab fetch (Pass-3 Layer 4) so questions can use the full vocab pool for distractor generation.
