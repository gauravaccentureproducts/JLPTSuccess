# Legal Vetting Audit — JLPTSuccess N5 (run 2)

**Conducted:** 2026-05-13
**Scope:** N5 sub-app + JLPTSuccess landing page + shared infrastructure since the 2026-05-10 baseline audit.
**Persona:** Japan-IP / education-publishing IP counsel (15-yr Japan exposure).
**Mode:** Audit-only. No file changes proposed within this report; remediation suggestions are advisory.
**Driving prompt:** `prompts/LegalVetting.txt`.
**Prior audit:** `feedback/legal-vetting-audit-2026-05-10.md` (13 findings filed, status verified below).

---

## Executive summary

**Overall exposure: HIGH (driven by one specific item).** The 2026-05-10 audit's 13 findings (F-1 through F-13) are substantially closed, partially remediated, or moot per the v1.15.x cycle work. The corpus's overall posture is **stronger than at the prior audit** in every dimension *except one*: the v1.15.0 public-domain references expansion (`data/grammar.json#public_domain_refs`) shipped **four entries that explicitly cite copyrighted works** (Kawabata Yasunari, Nakamura Ukou ×2, Nishijō Yaso). The data file itself discloses the copyright status in the `pd_status` field — strings like `"川端 d.1972; PD pending until 2043"` and `"PD pending until 2043; lyrics protected"`. These are live in master at commit `6af5fac` and trivially fixable (same class as the n5-062 三木露風 fix shipped earlier this session, commit `d228afd`).

The maintainer has explicitly stated zero tolerance for IP risk in this exact class ("regarding animation, skip using the names. lets play safe, cant take even 1% risk." — directive logged 2026-05-12). Four in-copyright literary/musical citations sitting in the shipped data file are precisely that risk.

Everything else this run is either previously-closed, a low-severity documentation cleanup, or genuinely defensible.

---

## Severity legend (this audit)

| Tier | Definition | Typical remediation horizon |
|---|---|---|
| **Severe** | Active distribution of clearly-infringing material; the data file itself admits the work is in copyright. | Same-day. |
| **High** | Distribution of third-party material under unclear license; plausible C&D risk if rights-holder is asked; or material misrepresentation in user-facing claims. | Within current sprint. |
| **Medium** | Documentation drift, mis-dated PD claims, missing attribution, or coverage gaps in CI checks that could permit a future High drift. | Next 1-2 sprints. |
| **Low** | Tone, polish, or footnote-grade items with no realistic enforcement path. | Backlog. |

---

## Findings

### F-1 (2026-05-13) — Four PD references cite works STILL IN COPYRIGHT (SEVERE)

- **Severity:** Severe
- **Category:** CAT-1 (citation of copyrighted material) + CAT-6 (content-authoring honesty — the data file's own `pd_status` confesses the issue)
- **Rights-holder:** Estates of 川端康成 (Kawabata Yasunari), 中村雨紅 (Nakamura Ukou), 西條八十 (Nishijō Yaso). All represented by mainstream Japanese publishers (新潮社, 講談社) with active enforcement histories.
- **Evidence:** `data/grammar.json` shipped at master `6af5fac`:

  | Pattern | Cited work | Author | Death year | PD-in year (life+70) | `pd_status` text |
  |---|---|---|---|---:|---|
  | **n5-025** | 夕焼け小焼け | 中村雨紅 | 1972 | 2042 | "PD pending (Nakamura d.1972; melody by 草川信 d.1948 PD 2019)" |
  | **n5-080** | 雪国 | 川端康成 | 1972 | 2042 | "川端 d.1972; PD pending until 2043" |
  | **n5-164** | 肩たたき | 西條八十 (lyrics) | 1970 | 2040 | "Japan PD pending (Nishijō died 1970; expires 2041)" |
  | **n5-181** | 夕焼け小焼け | 中村雨紅 | 1972 | 2042 | "PD pending until 2043; lyrics protected" |

  All four entries quote literal text from the cited works in the `context` field (e.g., n5-164: "Classic 童謡 about a child gently tapping their grandmother's shoulders. The lyric..."). The n5-080 entry also embeds a self-incriminating "(Fallback ref:)" prefix in its context, indicating the original author of `tools/author_pd_refs_expand.py` intended this as a placeholder for later replacement.

- **Plausible claim:** Direct reproduction of in-copyright lyrics / prose under 著作権法 §21 (reproduction right) and §23 (public-transmission right) since the repo is publicly fetchable on GitHub. The site itself does not display the `context` field to end-users (it does display `work_title` + `author` + `pd_status` text — which themselves admit copyright status, making the reproduction defense weaker). 引用 §32 (fair quotation) is unlikely to cover this because: (a) the quotation is not subordinated to a critical discussion of the source work, (b) the entries are mass-cataloged alongside genuinely-PD works which weakens the "necessary for legitimate purpose" prong, (c) the `pd_status` self-disclosure shows the project KNEW the works were in copyright.
- **C&D likelihood:** Medium for Kawabata estate (高度に管理されている; 新潮社 is litigation-experienced); Low-Medium for 童謡 lyrics (JASRAC may handle but unlikely to pursue free educational app actively). The HIGH-risk vector is not direct rights-holder enforcement — it's **automated GitHub-scrape DMCA filings** by content-monitoring services that flag the work titles.
- **Escalation likelihood:** Low for civil action; Medium for DMCA takedown of the repo if surfaced via automated scan.
- **Remediation cost:** **Trivial.** Same fix pattern as commit `d228afd` (n5-062 三木露風 → traditional わらべうた とおりゃんせ). For each of the 4 entries: replace the in-copyright reference with a verified pre-1956-death-year work (Aozora Bunko PD authors: 漱石 d.1916, 芥川 d.1927, 鏡花 d.1939, 啄木 d.1912, 賢治 d.1933, 子規 d.1902) or with a traditional わらべうた / 童謡 dated to pre-Meiji or with anonymous attribution.
- **Recommended remediation:** One script + one commit. Replace the four entries with verified-PD substitutes; cross-check author_death_year ≤ 1955 (a conservative buffer over the 1967 mathematical PD threshold). Add JA-69 invariant to CI: `_check_ja_69_pd_refs_actually_pd` that scans `public_domain_refs` and FAILS on any entry whose `pd_status` text contains `"pending"` / `"protected"` / `"in copyright"` / `"PD in 20"` (any 20xx year). This prevents recurrence.

### F-2 (2026-05-13) — Three PD-status text strings claim "pending" but the work IS public-domain (MEDIUM)

- **Severity:** Medium (defensibility — misrepresentation of legal status of OUR OWN materials, though in the conservative direction)
- **Category:** CAT-6 (content-authoring honesty)
- **Rights-holder / affected party:** No live claim. Internal misrepresentation: the entries say "pending" when the cited work is genuinely PD (author Takano Tatsuyuki d.1947, which became PD in 1998 under the pre-2018 life+50 rule; the 2018 law change to life+70 does NOT retroactively re-copyright already-PD works).
- **Evidence:** `data/grammar.json`:
  - n5-016, n5-116, n5-156: each cites 高野辰之 (Takano Tatsuyuki) songs (たけのこ / おぼろづきよ / etc.) with `pd_status: "Japan PD pending (Takano d.1947; expires 2018)"`. Takano IS PD (since 1998; the "expires 2018" note appears to confuse the 2018 LAW CHANGE date with a copyright-expiration date).
  - Same files reference melodies by 岡野貞一 (d.1941) and 草川信 (d.1948) with similarly-confused PD-status strings.
- **Plausible claim:** None — these entries are safer than they claim to be. The risk is reputational if an institutional reviewer reads CONTENT-LICENSE.md alongside the data and concludes "the project doesn't know the difference between PD and non-PD."
- **C&D likelihood:** None.
- **Remediation cost:** Trivial. Fix the `pd_status` string to read "Japan PD since 1998 (Takano d.1947; pre-2018 life+50 rule)" etc.
- **Recommended remediation:** Bundled with F-1 fix — same script, sweep the `pd_status` field for incorrect "pending" claims on pre-1968 author-death-year entries.

### F-3 (2026-05-13) — CONTENT-LICENSE.md has stale section §4 vocab count (LOW)

- **Severity:** Low
- **Category:** CAT-10 (documentation gaps)
- **Evidence:** `CONTENT-LICENSE.md`:
  - Line 28: `"data/vocab.json (1009 entries)"` — correct.
  - Line 80: `"the vocabulary scope (~800 core entries; we expanded to 1003 with related N5 vocabulary)"` — stale (actual: 1009).
  - Line 80: `"the grammar inventory (~150 patterns; we cover 177 with related forms)"` — stale (actual: 178).
- **Plausible claim:** None — pedantic-only.
- **Remediation cost:** Trivial.
- **Recommended remediation:** Update §4 line 80 to read "1009 vocabulary entries" and "178 grammar patterns."

### F-4 (2026-05-13) — `auto_provenance.py` scope does not cover `public_domain_refs.context` field (MEDIUM)

- **Severity:** Medium
- **Category:** CAT-6 (content-authoring honesty) + CAT-9 (CI coverage)
- **Evidence:** The CI provenance scanner `tools/audit_provenance.py` scans for "past-paper signatures" but does NOT check whether `public_domain_refs[*].context` contains in-copyright quoted text. F-1 above slipped past CI for exactly this reason — JA-66 (above-N5 kanji guard) caught Phase 7 drift but no invariant guards the legal-PD status of newly-added PD refs.
- **Plausible claim:** None directly; this is a process gap.
- **Remediation cost:** Trivial — new lambda invariant (estimated one turn including negative-test).
- **Recommended remediation:** JA-69 invariant (as described in F-1): scan every `public_domain_refs` entry; FAIL on any entry whose `pd_status` contains red-flag substrings ("pending" / "protected" / "in copyright" / `PD in 20[3-9]\d`). Bonus: assert `author_death_year is None or author_death_year ≤ 1955` (conservative buffer over Japan's mathematical PD threshold of 1967).

### F-5 (2026-05-13) — `tools/author_pd_refs_expand.py` script committed with "(Fallback ref:)" placeholder text in n5-080 (LOW)

- **Severity:** Low (committed in-repo; not currently rendered to users since `context` is the rendered field but the substring is in `context` itself)
- **Category:** CAT-10 (documentation hygiene)
- **Evidence:** `data/grammar.json#n5-080.public_domain_refs[0].context` starts with `"(Fallback ref:) い-adj negative form has been used since classical Japanese literature. For PD coverage, use 漱石's 草枕 instead."` This is an author's note to themselves that didn't get cleaned up before commit. It also explicitly admits the entry should have been replaced with a Sōseki reference.
- **Plausible claim:** Embarrassment-class only; no live claim.
- **Remediation cost:** Trivial — folded into F-1 fix.
- **Recommended remediation:** When F-1 replaces n5-080's Kawabata reference, the "(Fallback ref:)" prefix goes with it.

### F-6 (2026-05-13) — Prior F-7 (mock-paper format resemblance) reaffirmed (MEDIUM, mostly mitigated)

- **Severity:** Medium (carry-forward, unchanged from 2026-05-10)
- **Category:** CAT-2 (textbook/reference derivation)
- **Evidence:** Same as prior F-7. Mock-paper format mirrors official JLPT N5 (Mondai 1-7 structure, question-count distribution). CONTENT-LICENSE.md §5 explicitly disclaims: "The MCQ paper structure ... follows the standard JLPT N5 format. This is a fact about the test, documented in dozens of learner books and on jlpt.jp. The format itself is not copyrightable - only specific question text is."
- **Plausible claim:** None — format-vs-expression doctrine is well-established.
- **Remediation cost:** N/A — no remediation required; this is defensive documentation.
- **Recommended remediation:** Carry forward unchanged.

### F-7 (2026-05-13) — Prior F-1 (learnjapaneseaz competitor corpus) verified closed (informational)

- **Status:** **Closed.** The verbatim files (`feedback/closed/external-questions-learnjapaneseaz.md` + `feedback/closed/external-corpus/learnjapaneseaz-extract.json`) are no longer in the working tree. The remaining `feedback/closed/external-corpus/analysis-and-gap-audit.md` (204 lines) has been redacted per F-1; every direct source-stem quote replaced with `[source ... redacted per F-1]` markers; the analytical findings + format taxonomy preserved. No further action needed.

### F-8 (2026-05-13) — Prior F-2 (native_reviewed Claude-as-persona disclosure) verified closed (informational)

- **Status:** **Closed.** `CONTENT-LICENSE.md §9 "Provenance honesty"` (lines 134-157) explicitly discloses: *"The `review_status: native_reviewed` flag ... reflects a review pass conducted on 2026-05-07 by Claude (Anthropic's LLM) acting in a native-reviewer persona, per explicit user directive. The user authorized this reviewer-role assignment in lieu of recruiting a native Hindi-speaking Japanese teacher."* The maintainer additionally directed (this session, 2026-05-13): "Everything is machine generated and nothing is native reviewed here. No need to disclose this as long as it is correct" — which means: keep the internal CONTENT-LICENSE.md disclosure (covers institutional due-diligence) but do NOT expose provenance tiers as UI trust signals (IMP-184 set to Avoid this session). The two posture decisions are coherent.

### F-9 (2026-05-13) — Prior F-3..F-12 verified closed (informational)

- **Status:** All remaining prior-audit findings closed:
  - **F-3** CONTENT-LICENSE corpus counts: refreshed 2026-05-11 (carries F-3-close timestamp in the file). Minor stale §4 entries surface as new F-3 above (LOW).
  - **F-4** JLPT trademark non-affiliation disclaimer: shipped — see `index.html` lines 296-298 (`<small class="footer-disclaimer">`).
  - **F-5** NOTICES.md font attribution: verified; current NOTICES.md tracks all third-party content.
  - **F-6** `audit_provenance.py` paraphrase detection: still narrow scope; superseded by F-4 (2026-05-13) above.
  - **F-7** Mock-paper format resemblance: carried forward as new F-6 (2026-05-13).
  - **F-8** KanjiVG SVG header preservation: JA-48 invariant enforces (running green).
  - **F-9** PRIVACY.md GitHub Pages disclosure: shipped — see `PRIVACY.md` lines 27-45 (GDPR Art 13/14 information-obligation section).
  - **F-10** VOICEVOX speaker credit at audio surface: shipped per `audio_render_meta.voices_used` cataloging per item.
  - **F-11** Test suite verification: 72/72 invariants green; CI was 50 at the prior audit, now 70+2 (JA-67 + JA-68 added this session).
  - **F-13** Edge-TTS → VOICEVOX flip: shipped per NOTICES.md update; legacy edge-TTS backup is gitignored at `audio/_backup_edge_tts_listening_2026_05_12/` (verified not in `git ls-files`).

---

## What is provably defensible

The following are explicitly **not findings**; documented for partner / due-diligence reference.

- **Privacy posture:** `PRIVACY.md` accurately describes the runtime; CSP enforced; no fetch to non-local URLs (JA-60 invariant); no analytics endpoints (independently verifiable per the PRIVACY.md "Open the Network tab" instruction).
- **Code license clarity:** MIT (`LICENSE` at repo root). Code/content separation cleanly documented in `CONTENT-LICENSE.md`.
- **Content license (CC BY-NC 4.0):** Documented in `CONTENT-LICENSE.md`; reaffirmed in `SELFHOST.md` (new this session, commit `d228afd`). Operators forking know what they're getting.
- **Third-party attribution:** `NOTICES.md` is comprehensive — KanjiVG (CC BY-SA 3.0), VOICEVOX engine + per-character voice licenses, Kanjium pitch dictionary (CC BY-SA 4.0), gTTS, Microsoft Edge TTS (historical), Aozora Bunko PD literature, Japanese government works (Constitution etc.).
- **Provenance integrity (mostly):** `audit_provenance.py` scans 716 audited questions for past-paper signatures, 0 hits (last run 2026-05-07; surface unchanged). CI keeps it clean.
- **Audit-cycle hygiene:** Two new anti-patterns added to JLPT Common procedure manual this session (`#22` no-day-estimates and `#23` no-calendar-cadence-audits). These are governance discipline, not legal exposure.
- **PD-refs framework (5-tier):** Aozora Bunko PD literature + Japanese government works (§13 著作権法 exception for state works) + traditional proverbs + folk songs + NHK Easy News (recommendation-only). For 211 of 215 refs (98%), this is genuinely PD-clean. Only F-1's 4 entries break the framework.
- **Anti-anime-citation discipline:** ISSUE-124 + IMP-147 set to Avoid per maintainer 2026-05-12 ("1% legal risk is too much"). The corpus has zero anime/drama/manga citations. The 4 F-1 entries are an inconsistency with this same posture — they cite copyrighted SONG LYRICS and PROSE, which is the same legal class.

---

## Monetization blast-radius

If JLPTSuccess monetizes (sponsorship, institutional adoption, ad-supported tier, or commercial license sale):

1. **F-1 in-copyright PD-refs (Severe today): becomes immediately litigation-grade.** Commercial use of in-copyright lyrics + prose dramatically widens the rights-holder's standing. 引用 §32 fair-quotation virtually collapses under commercial use. **Block monetization until F-1 fixed.**
2. **F-2 mis-labeled PD claims (Medium today): becomes Medium-High** under commercial — false-statement-class under 不正競争防止法 §2 (1)(xx) if anyone relies on the project's PD-status claims and gets sued.
3. **F-6 mock-paper format resemblance (Medium today): unchanged** — format-vs-expression doctrine still applies. But JEES is more likely to investigate a commercial JLPT-prep product than a free one.
4. **Native-reviewer disclosure (closed today): unchanged** — already disclosed in CONTENT-LICENSE.md §9. If an institutional partner contractually requires "native-speaker-reviewed content," the project would need to actually recruit a reviewer.
5. **JLPT trademark non-affiliation (closed today): becomes High** under commercial — passing-off (詐称通用 unter 商標法 §25) is rarely actionable for free non-commercial use but actively enforced for commercial competitors.

**Net:** the project is currently 1 commit away (F-1 fix) from being monetization-ready on the legal exposure dimensions. The remaining items are governance / documentation hygiene.

---

## Documentation remediation backlog

Bundled-edits version (one commit, all together):

1. **CONTENT-LICENSE.md §4 line 80:** "1003" → "1009"; "177" → "178".
2. **CONTENT-LICENSE.md §1 first cell label:** verify "1009 entries" appears consistently throughout (currently inconsistent across lines 28 vs 80).
3. **N/A — pd_status text fixes:** rolled into F-1 + F-2 fix commit; not a separate doc edit.

---

## Open factual questions

The audit could not resolve from the repo alone:

- **Q1:** Has anyone external (institutional reviewer, JEES rep, learnjapaneseaz operator, Kawabata estate) actually contacted the project about any of the 13 prior-audit findings, the F-1 4-entry copyright issue, or anything else? If so, the response posture is more involved than a private re-audit run.
- **Q2:** The remediation script for F-1 should substitute in-copyright references with PD-cleared ones. For n5-025 + n5-181 (both cite 夕焼け小焼け), is there a single-author Aozora work covering the same pattern category (童謡 reflective register / sentence-final 〜なあ), or do these need bespoke replacements? **Answerable in one turn during the fix.**

---

## What this audit explicitly did NOT cover

- **N4-N1 corpus:** out of scope; product-paused per project Rule 1.
- **Hindi-locale-specific legal posture:** handled by the separate Hindi prompt; touched here only where it intersects English-locale fields.
- **Similarity-detection pass against Genki / MNN textbooks:** I do not have the source texts in scope. The CONTENT-LICENSE.md §4 explicit non-derivation claim ("Tofugu / WaniKani / Imabi / Bunpro / JLPTsensei / Tae Kim ... Any verbatim text — DID NOT TAKE") remains an unverified self-claim. No automated finding from this audit; recommend running a third-party similarity scan if budget allows (one-time, low cost).
- **GDPR specifics beyond F-9 PRIVACY.md disclosure:** the data-controller layer is correctly assigned to GitHub Pages per PRIVACY.md lines 38-44. Detailed EEA representative + DPIA + ROPA paperwork is out of scope for a free non-commercial product but would become an item if EU institutional adoption happens.

---

## Recommended action sequence

Per anti-pattern #22 (estimate in turns, not days):

1. **One turn:** Fix F-1 (4 in-copyright PD refs) — replace with verified-PD substitutes; same code pattern as the n5-062 三木露風 fix shipped earlier this session in commit `d228afd`. Includes F-2 (mis-labeled PD claims) and F-5 (n5-080 fallback prefix) in the same edit batch.
2. **One turn:** Add JA-69 invariant to CI (F-4) — pd_status red-flag string scanner. Prevents recurrence.
3. **One turn:** F-3 doc cleanup (CONTENT-LICENSE.md §4 stale counts). Can be folded into commit #1.
4. **No action:** F-6 (carry-forward), F-7..F-9 (closed/informational), monetization-blast-radius items (no monetization planned).

**Total to clear all Severe + Medium findings: 2 commits, ~3 turns including verification.**

Human-attention required: confirm the F-1 substitute references before commit lands (~1 AskUserQuestion turn if the substitutes are ambiguous; likely zero turns if I use the same source pool as commit `caa46d1` / `d228afd`).
