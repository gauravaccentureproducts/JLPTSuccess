# Legal-vetting F-6 spot-check (2026-05-11)

**Scope:** lightweight manual audit per F-6 of `feedback/legal-vetting-audit-2026-05-10.md`.

**Method:**
- Random sample of 10 questions across `data/papers/*` (402 total questions across 28 papers).
- Seed: `random.seed(0xF6)` (reproducible via `not-required/tools-archive/sample_papers_f6_2026_05_11.py`).
- Each question audited against known competitor-corpus signatures (Genki I/II, Minna no Nihongo, Imabi, Bunpro, WaniKani, Renshuu, JapanesePod101). The learnjapaneseaz.com extract files were already deleted under F-1 / F-12 prior to this audit pass.

**Auditor's note:** this is the *lightweight* track. Heavyweight similarity-detection (quarantined competitor corpus + similarity tool) remains deferred per the audit's F-6 scope statement. The lightweight check is a per-release sanity guard, not an exhaustive screen.

## Sample audit

| # | Question | Type | Verdict | Note |
|---|---|---|---|---|
| 1 | `bunpou-3.1` | i-adj predicate form | ✅ safe | Generic grammar drill (たかい / たかくて / たかいの / たかく). No distinctive scenario or wording. Universal N5 conjugation pattern. |
| 2 | `goi-5.3` | antonym paraphrase | ✅ safe | とおくない ≈ ちかい. Direct antonym pair appearing in every N5 textbook from Genki onward. Generic enough that paraphrasing would be coincidence. |
| 3 | `dokkai-7.9` | schedule comprehension | ✅ safe | Hospital-schedule reading (月、水、金 14:00-19:00 しか). Specific time/day values appear arbitrary; no distinctive idiom or cultural-reference pattern that would trace to a known source. |
| 4 | `moji-5.7` | kanji reading | ✅ safe | 火曜日 from day-of-week distractor set. Standard JLPT format; identical-format drills exist in every public sample. |
| 5 | `dokkai-6.8` | comprehension (relations) | ⚠ borderline — flagged | "おくさんは 私の 学校の 先生でした" — wife-as-teacher narrative is generic but the specific framing (1st-person narrator describing a family member's profession) appears in MNN Lesson 9 and Genki I Ch. 7 reading practice. Likelihood of substantial-similarity claim is **low** since the question only tests profession-vocabulary comprehension; the framing is not the protected element. Recommend leaving as-is but watch this question on future spot-checks. |
| 6 | `bunpou-3.4` | な-adj + あまり + neg | ✅ safe | しずかじゃ ありません is the textbook-canonical polite-negative form. Drill format is universal. |
| 7 | `moji-5.13` | kanji visual distractors | ✅ safe | 午前 vs 牛前 / 午先 (look-alike trap distractors). Distractor pattern is JLPT-standard; the specific look-alike clusters are documented in our `kanji.json` `look_alike_clusters` field (project-original work). |
| 8 | `goi-2.9` | context vocab | ✅ safe | あつい / open window. Generic vocab-in-context drill. |
| 9 | `bunpou-7.1` | particle selection | ✅ safe | Time + に. Single-most-tested N5 grammar point; identical drills across all sources. |
| 10 | `goi-7.3` | paraphrase | ✅ safe | あした やすみです → "tomorrow off work" synonym recognition. Generic vocabulary-equivalence pattern. |

## Findings

- **0 / 10 confirmed paraphrasing risk**
- **1 / 10 borderline** (`dokkai-6.8`) — flagged but verdict is "low likelihood of claim, no remediation required, monitor on next pass"
- **9 / 10 clearly safe** — generic JLPT-standard drill patterns where similarity to public sources is coincidence, not paraphrase

## Recommendation

No remediation actions required from this pass. Maintain F-6 cadence: re-run the sampler with a fresh seed each release. If a future seed surfaces a question that fails this audit, log it as a finding and refactor that specific question.

Next sampler seed reservation: `0xF6_NEXT` (or any value not previously used). Document seed + commit SHA in this file when each future audit pass runs.

---

*Audit conducted 2026-05-11 against repo HEAD post-F-5 (`160b7aa`). Sampler script preserved at `not-required/tools-archive/sample_papers_f6_2026_05_11.py` for reproducibility.*
