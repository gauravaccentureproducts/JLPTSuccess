# feedback/closed — archived feedback

These documents are kept for traceability but are no longer actionable.
Each one is either:

- a **decision document** that records a closed decision,
- an **audit report** whose findings have been applied to the live data
  bundle / KnowledgeBank, or
- a **brief** whose features are shipped in the live app.

The single live tracker is [`../MASTER-TASK-LIST.md`](../MASTER-TASK-LIST.md);
it consolidates and supersedes every audit and brief in this folder.

If you are looking for *what work is currently open*, do not read here —
read `../MASTER-TASK-LIST.md` and the project-root `TASKS.md`.

---

## Why each file is closed

### Decision documents
| File | Decision |
|---|---|
| `f15-23-n5-167-nodesu-native-teacher-decision.md` | Keep n5-167 at `tier=late_n5`, do not author a question (pattern is N4 territory; recognition-only at N5). |
| `f17-9-vocab-pos-tags-decision.md` | No KB markdown annotation needed — runtime already has 100% PoS coverage in `data/vocab.json`. |

### Audit reports — findings applied
| File | Closure note |
|---|---|
| `jlpt-n5-consolidated-audit-2026-05-01.md` | Self-states "All 10 OPEN items closed today; 0 actionable code-doable items remain." Successor to all individual audit/brief docs. |
| `jlpt-n5-content-correction-brief.md` | KnowledgeBank corrections (kanji/vocab catalog) verified resolved by the consolidated 2026-05-01 audit. |
| `jlpt-n5-data-correction-brief.md` | Data-bundle corrections (会/番 readings, missing kanji, etc.) verified resolved by the consolidated 2026-05-01 audit. |
| `jlpt-n5-reading-feedback.md` | reading.json kanji-whitelist enforcement now clean across all 30 passages. |
| `jlpt-n5-knowledgebank-md-audit-2026-05-01.md` | KB markdown audit — findings absorbed into MASTER-TASK-LIST. |
| `jlpt-n5-dossier-followup-audit-2026-05-02.md` | Self-states "Every issue flagged in the previous audit is now resolved. Dossier is ready to ship." |
| `teacher-audit-2026-05-02.md` | T-1..T-5 categories all 0 findings; T-6 fixed; T-7..T-9 categorised as gap-not-bug. |
| `llm-audit-validation-report.md` | n5-115 + n5-008 fixes shipped (closed via consolidated audit's OPEN-1/2/3). |

### Briefs — shipped features
| File | Closure note |
|---|---|
| `jlpt-n5-tutor-developer-brief.md` | Original developer brief (curriculum + offline + privacy + cross-browser). All hard constraints + Phase 4/5 deliverables shipped. |
| `jlpt-n5-tutor-developer-brief.ja.md` | Japanese translation of the same brief; same closure scope. |
| `jlpt-n5-tutor-ux-developer-brief2.md` | UX Brief 2 — landing rebuild, Learn hub, per-vocab detail, Phases 1-4 all shipped (referenced by `ui-testing-plan.md`). |
| `jlpt-n5-ui-design-brief.md` | Zen Modern design system locked; CI design-system rules D-3/D-4/D-8 enforce ongoing compliance. |
| `jlpt-n5-homepage-update.md` | Syllabus dashboard with neutral inventorial copy + design-system rule 11 in `specifications/jlpt-n5-design-system-zen-modern.md` shipped. |

### External corpus — gap audit consumed
| File | Closure note |
|---|---|
| `external-questions-learnjapaneseaz.md` | Reference extract from learnjapaneseaz.com; gaps closed via Pass-15 (paraphrase + kanji_writing subtypes shipped per JA-29). |
| `external-corpus/learnjapaneseaz-extract.json` | Extraction artefact; consumed. |
| `external-corpus/analysis-and-gap-audit.md` | Gap audit; closure via Pass-15 P0 + P1 batches. |
| `coverage-comparison.md` | "163 vs 175" comparison superseded by current 198+ question count + JA-29 closed-taxonomy. |

### Native-reviewer dossier — replaced by internal-audit pair
| File | Closure note |
|---|---|
| `native-teacher-review-request.md` | Pass-11 native review request; the user's directive on 2026-05-02 was to treat the **internal pre-review-audit + follow-up-audit pair as "the reviewer"**, so an external native pass is not on the path. |
| `native-review-dossier/cover.md` | Dossier cover page (reviewer instructions). |
| `native-review-dossier/01_grammar_patterns.md` | 177 grammar patterns dossier. |
| `native-review-dossier/02_vocab_borderline.md` | 122 borderline vocab dossier. |
| `native-review-dossier/03_kanji_readings.md` | 106 kanji dossier. |
| `native-review-dossier/04_reading_passages.md` | 30 dokkai passages dossier. |
| `native-review-dossier/05_listening_scripts.md` | 30 listening dialogues dossier. |
| `native-review-dossier/review_log.csv` | Empty findings template — consumed by internal audits. |
| `native-review-dossier/jlpt-n5-dossier-pre-review-audit-2026-05-02.md` | First internal pass; all 14 findings closed (3 critical / 4 high / 5 medium / 2 low). The follow-up audit one folder up confirms closure. |

---

## What's still open / live (kept at `feedback/` top level)

- `MASTER-TASK-LIST.md` — single live tracker.
- `ui-testing-plan.md` — active testing-plan reference.
- `procedure-manual-review-issues.md` — issues with the next-level procedure manual; relevant for any future N4/N3/N2/N1 build.
- `jees-inquiry-template.md` — drafted but explicitly not sent; kept for the day a past-paper licence question arises.
- `audio-coverage-gaps.json` — auto-generated by `tools/audit_audio_coverage.py`; regenerated each run.
- `n4-{kanji,grammar,vocab-sample}-inventory.md` + `n4-inventory-manifest.md` — bootstrap inventories for a future N4 build (Pass-21 closure deliverables).
- `Prompts/Japanese language Accuracy check.txt` — reusable audit prompt template.
