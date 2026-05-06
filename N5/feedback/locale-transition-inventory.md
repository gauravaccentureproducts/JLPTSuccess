# Locale-transition pre-flight inventory (Phase 0)

Date: 2026-05-06.
Goal: locate every reference to the four locales being removed (vi, id, ne, zh)
plus any 5-locale claim text. The transition prompt requires this inventory
to be committed before Phase 1 begins.

## N5 sub-app - files to edit

**Total: 175 files.** Grouped by directory:

### `N5/` (8 files)

- `N5/AUDIO.md` - kinds: `quoted_locale` - sample: `"id"`
- `N5/CHANGELOG.md` - kinds: `locale_suffixed_field` - sample: `meanings_vi`
- `N5/README.md` - kinds: `claim_phrase` - sample: `vi/id/ne/zh`
- `N5/TASKS.md` - kinds: `claim_phrase` - sample: `vi/id/ne/zh`
- `N5/index.html` - kinds: `quoted_locale` - sample: `"vi"`
- `N5/sitemap.xml` - kinds: `quoted_locale` - sample: `"vi"`
- `N5/sw.js` - kinds: `locale_json` - sample: `locales/vi.json`
- `N5/verification.md` - kinds: `native_name` - sample: `中文`

### `N5/KnowledgeBank/` (3 files)

- `N5/KnowledgeBank/dokkai_questions_n5.md` - kinds: `english_name` - sample: `Chinese`
- `N5/KnowledgeBank/moji_questions_n5.md` - kinds: `native_name` - sample: `中文`
- `N5/KnowledgeBank/vocabulary_n5.md` - kinds: `english_name` - sample: `Chinese`

### `N5/data/` (7 files)

- `N5/data/audio_manifest.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/grammar.json` - kinds: `locale_suffixed_field` - sample: `meaning_vi`
- `N5/data/kanji.json` - kinds: `locale_suffixed_field` - sample: `meanings_vi`
- `N5/data/listening.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/questions.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/reading.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/vocab.json` - kinds: `locale_suffixed_field` - sample: `gloss_vi`

### `N5/data/papers/` (1 files)

- `N5/data/papers/manifest.json` - kinds: `quoted_locale` - sample: `"id"`

### `N5/data/papers/bunpou/` (7 files)

- `N5/data/papers/bunpou/paper-1.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/bunpou/paper-2.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/bunpou/paper-3.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/bunpou/paper-4.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/bunpou/paper-5.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/bunpou/paper-6.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/bunpou/paper-7.json` - kinds: `quoted_locale` - sample: `"id"`

### `N5/data/papers/dokkai/` (7 files)

- `N5/data/papers/dokkai/paper-1.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/dokkai/paper-2.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/dokkai/paper-3.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/dokkai/paper-4.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/dokkai/paper-5.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/dokkai/paper-6.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/dokkai/paper-7.json` - kinds: `quoted_locale` - sample: `"id"`

### `N5/data/papers/goi/` (7 files)

- `N5/data/papers/goi/paper-1.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/goi/paper-2.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/goi/paper-3.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/goi/paper-4.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/goi/paper-5.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/goi/paper-6.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/goi/paper-7.json` - kinds: `quoted_locale` - sample: `"id"`

### `N5/data/papers/moji/` (7 files)

- `N5/data/papers/moji/paper-1.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/moji/paper-2.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/moji/paper-3.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/moji/paper-4.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/moji/paper-5.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/moji/paper-6.json` - kinds: `quoted_locale` - sample: `"id"`
- `N5/data/papers/moji/paper-7.json` - kinds: `quoted_locale` - sample: `"id"`

### `N5/docs/` (3 files)

- `N5/docs/NATIVE-AUDIO-WORKFLOW.md` - kinds: `quoted_locale` - sample: `"id"`
- `N5/docs/SELF-HOST.md` - kinds: `claim_phrase` - sample: `5 locale`
- `N5/docs/TRANSLATING.md` - kinds: `locale_suffixed_field` - sample: `explanation_vi`

### `N5/feedback/` (2 files)

- `N5/feedback/MASTER-TASK-LIST.md` - kinds: `claim_phrase` - sample: `5 locales`
- `N5/feedback/ui-testing-plan.md` - kinds: `english_name` - sample: `Vietnamese`

### `N5/feedback/closed/` (7 files)

- `N5/feedback/closed/jlpt-n5-data-correction-brief.md` - kinds: `quoted_locale` - sample: `"id"`
- `N5/feedback/closed/jlpt-n5-data-files-audit-2026-05-02.md` - kinds: `quoted_locale` - sample: `"id"`
- `N5/feedback/closed/jlpt-n5-infrastructure-audit-2026-05-03.md` - kinds: `quoted_locale` - sample: `"id"`
- `N5/feedback/closed/jlpt-n5-reading-feedback.md` - kinds: `quoted_locale` - sample: `"id"`
- `N5/feedback/closed/jlpt-n5-tutor-developer-brief.md` - kinds: `quoted_locale` - sample: `"id"`
- `N5/feedback/closed/jlpt-n5-tutor-ux-developer-brief2.md` - kinds: `english_name` - sample: `Vietnamese`
- `N5/feedback/closed/native-teacher-review-request.md` - kinds: `native_name` - sample: `中文`

### `N5/js/` (6 files)

- `N5/js/i18n.js` - kinds: `quoted_locale` - sample: `'vi'`
- `N5/js/kanji.js` - kinds: `locale_suffixed_field` - sample: `meanings_vi`
- `N5/js/learn-grammar.js` - kinds: `locale_suffixed_field` - sample: `explanation_vi`
- `N5/js/learn-vocab.js` - kinds: `locale_suffixed_field` - sample: `gloss_vi`
- `N5/js/normalize.js` - kinds: `quoted_locale` - sample: `'ne'`
- `N5/js/settings.js` - kinds: `native_name` - sample: `Tiếng Việt`

### `N5/locales/` (4 files)

- `N5/locales/id.json` - kinds: `english_name` - sample: `Indonesian`
- `N5/locales/ne.json` - kinds: `english_name` - sample: `Nepali`
- `N5/locales/vi.json` - kinds: `english_name` - sample: `Vietnamese`
- `N5/locales/zh.json` - kinds: `english_name` - sample: `Chinese`

### `N5/prompts/` (2 files)

- `N5/prompts/LocaleTransitionEnHi.txt` - kinds: `locale_suffixed_field` - sample: `gloss_vi`
- `N5/prompts/N5Improvement.txt` - kinds: `english_name` - sample: `Vietnamese`

### `N5/specifications/` (3 files)

- `N5/specifications/JLPT-N5-Current-Implementation-Spec.md` - kinds: `quoted_locale` - sample: `'vi'`
- `N5/specifications/JLPT-N5-Functional-Spec-v3.1-supplement.md` - kinds: `claim_phrase` - sample: `5 locales`
- `N5/specifications/README.md` - kinds: `claim_phrase` - sample: `vi/id/ne/zh`

### `N5/tests/` (1 files)

- `N5/tests/round3-features.spec.js` - kinds: `quoted_locale` - sample: `"vi"`

### `N5/tools/` (100 files)

- `N5/tools/_locale_transition_inventory.py` - kinds: `english_name` - sample: `Vietnamese`
- `N5/tools/_read_decisions_round2.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/add_common_mistakes_phase8.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/add_dokkai_passages_phase9a.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/add_grammar_examples.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/add_listening_items.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/add_listening_items_phase9b.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/add_uncovered_questions.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/add_uncovered_questions_batch2.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/add_uncovered_questions_batch3.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/add_vocab_examples.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/add_vocab_examples_phase10.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/add_vocab_examples_phase4.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/add_vocab_examples_phase5.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/add_vocab_examples_phase6.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/add_vocab_examples_phase7.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/audit_audio_coverage.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/audit_example_coverage.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/audit_multi_correct.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/audit_provenance.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/audit_teacher_review.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/author_10_alias_entries_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/author_29_vocab_entries_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/author_45_dokkai_rationales_2026_05_04.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/author_pass16_questions.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/build_audio.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/build_audio_voicevox.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/build_data.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/build_papers.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/build_spec.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/check_content_integrity.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/deploy_dokkai_mondai_5_6_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/export_native_review_dossier.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fill_question_coverage.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/fix_audit_2026_05_03_batch.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_audit_round2_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_audit_round2_xlsx_done_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_audit_round3_final_xlsx_done_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_audit_round3_questions_done_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_audit_round3_xlsx_done_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_audit_round4_done_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_audit_round5_done_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_audit_round5_followup_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_data_audit_2026_05_02_batch1.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_data_bugs_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_dedup_q0479_q0488.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_goi_audit_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_goi_fourth_pass_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_goi_inference_cluster_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_goi_re_review_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_goi_third_pass_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_imp_005_grammar_romaji_2026_05_05.py` - kinds: `quoted_locale` - sample: `'ne'`
- `N5/tools/fix_imp_045_grammar_explanations_schema_2026_05_05.py` - kinds: `locale_suffixed_field` - sample: `explanation_vi`
- `N5/tools/fix_imp_046_vocab_extend_2026_05_05.py` - kinds: `locale_suffixed_field` - sample: `gloss_vi`
- `N5/tools/fix_imp_046_vocab_glosses_translate_2026_05_05.py` - kinds: `locale_suffixed_field` - sample: `gloss_vi`
- `N5/tools/fix_imp_047_kanji_meanings_translate_2026_05_05.py` - kinds: `locale_suffixed_field` - sample: `meanings_vi`
- `N5/tools/fix_infra_audit_2026_05_03.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_issue_016_listening_mondai_2026_05_05.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/fix_issue_017_paper1_rebalance_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_issue_056_grammar_localization_2026_05_06.py` - kinds: `locale_suffixed_field` - sample: `meaning_vi`
- `N5/tools/fix_issue_057_listening_mondai4_2026_05_06.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_issue_058_reading_mondai_backfill_2026_05_06.py` - kinds: `native_name` - sample: `中文`
- `N5/tools/fix_issue_059_paper_mondai_backfill_2026_05_06.py` - kinds: `native_name` - sample: `中文`
- `N5/tools/fix_issue_061_balance_question_choices_2026_05_06.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_issue_067_reading_topic_gaps_2026_05_06.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_issue_068_common_mistakes_floor_2026_05_06.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_iter1_2026_05_04.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/fix_iter2_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_iter3_2026_05_04.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/fix_iter4_global_rebalance_2026_05_04.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/fix_kosoado_basic.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_moji_first_pass_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_moji_source_audit_2026_05_03.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_paper_audit_2026_05_03.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_particle_basic.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_pass15_tier2.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_pass23_multi_correct.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_pass23_round2.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_pos_thematic_sections.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_remove_dead_translation_en.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_round4_content_audit_2026_05_04.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/fix_round5_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/fix_round7_quick_content_wins_2026_05_06.py` - kinds: `quoted_locale` - sample: `'zh'`
- `N5/tools/generate_stub_questions.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/heuristic_audit.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/inspect_candidates.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/link_grammar_examples_to_vocab.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/llm_audit.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/propagate_ref_md_audit_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/rebalance_round2_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/register_audit_round3_2026_05_05.py` - kinds: `claim_phrase` - sample: `5 locale`
- `N5/tools/register_audit_round4_2026_05_05.py` - kinds: `locale_suffixed_field` - sample: `explanation_vi`
- `N5/tools/register_audit_round5_2026_05_05.py` - kinds: `english_name` - sample: `Vietnamese`
- `N5/tools/register_audit_round6_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/register_dev_issue_list_deferrals_2026_05_05.py` - kinds: `claim_phrase` - sample: `EN/VI`
- `N5/tools/renumber_pass16_dedup.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/restructure_audit_xlsx_2026_05_05.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/sample_questions_for_review.py` - kinds: `quoted_locale` - sample: `"id"`
- `N5/tools/scan_multi_correct.py` - kinds: `quoted_locale` - sample: `'id'`
- `N5/tools/swap_q74_q83_2026_05_04.py` - kinds: `quoted_locale` - sample: `'id'`

## Top-level (JLPTSuccess root) files to edit

- `CONTRIBUTING.md` - kind `claim_phrase` - sample `vi/id/ne/zh`

## /N4/ contamination (FLAGGED - must NOT be edited)

Per `.claude/CLAUDE.md` Rule 1, `/N4/` is work-blocked. The grep below
shows N4 files that reference vi/id/ne/zh - they MUST remain unchanged.
Phase 10 verifies `git diff pre-locale-transition..HEAD --stat` shows zero
N4 deltas.

**N4 hits: 106 files.**
- `N4/CHANGELOG.md` (`claim_phrase`)
- `N4/KnowledgeBank/dokkai_questions_n4.md` (`native_name`)
- `N4/KnowledgeBank/kanji_examples_n4.md` (`english_name`)
- `N4/TASKS.md` (`claim_phrase`)
- `N4/data/audio_manifest.json` (`quoted_locale`)
- `N4/data/grammar.json` (`quoted_locale`)
- `N4/data/kanji.json` (`quoted_locale`)
- `N4/data/listening.json` (`quoted_locale`)
- `N4/data/papers/bunpou/paper-1.json` (`quoted_locale`)
- `N4/data/papers/bunpou/paper-2.json` (`quoted_locale`)
- `N4/data/papers/bunpou/paper-3.json` (`quoted_locale`)
- `N4/data/papers/bunpou/paper-4.json` (`quoted_locale`)
- `N4/data/papers/bunpou/paper-5.json` (`quoted_locale`)
- `N4/data/papers/bunpou/paper-6.json` (`quoted_locale`)
- `N4/data/papers/bunpou/paper-7.json` (`quoted_locale`)
- `N4/data/papers/dokkai/paper-1.json` (`quoted_locale`)
- `N4/data/papers/dokkai/paper-2.json` (`quoted_locale`)
- `N4/data/papers/dokkai/paper-3.json` (`quoted_locale`)
- `N4/data/papers/dokkai/paper-4.json` (`quoted_locale`)
- `N4/data/papers/dokkai/paper-5.json` (`quoted_locale`)
- ... and 86 more

## Pattern-frequency summary (N5 only)

- `quoted_locale`: 134 hits
- `locale_suffixed_field`: 15 hits
- `english_name`: 11 hits
- `claim_phrase`: 8 hits
- `native_name`: 6 hits
- `locale_json`: 1 hits

## Phase mapping

Per `prompts/LocaleTransitionEnHi.txt`:

- **Phase 1 (additive)**: create `locales/hi.json`, add `hi` to
  `js/i18n.js` SUPPORTED_LOCALES + chip group + sw.js precache.
- **Phase 2 (migration)**: add `migrateLocaleSetting()` to bootstrap.
- **Phase 3 (remove)**: delete the four locale files; remove the four chips;
  prune SUPPORTED_LOCALES; bump CACHE_VERSION.
- **Phase 4 (data prune)**: tooling script removes `gloss_<lc>` /
  `meaning_<lc>` / `explanation_<lc>` / `meanings_<lc>` keys for
  lc ∈ {vi,id,ne,zh}; seeds `_hi` placeholders.
- **Phase 5 (docs)**: rewrite multilingual claim text in README, PRIVACY,
  CHANGELOG, specs, audit prompt, top-level brand surfaces.
- **Phase 6 (CI)**: update `tools/check_content_integrity.py` locale list.
- **Phase 7 (tests)**: update Playwright specs that assert chip count.
- **Phase 8 (smoke)**: live preview walkthrough.
- **Phase 9 (registry)**: append IMP-NNN row to xlsx.
- **Phase 10 (push)**: `git push origin master`; `pre-locale-transition`
  tag already exists at the parent commit.

---

_Generated by `tools/_locale_transition_inventory.py`._
