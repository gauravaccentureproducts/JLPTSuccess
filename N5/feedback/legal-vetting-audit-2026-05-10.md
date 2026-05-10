# Legal Vetting Audit — JLPTSuccess N5

**Conducted:** 2026-05-10
**Scope:** N5 sub-app + JLPTSuccess landing page + shared infrastructure. N4 explicitly excluded (work-blocked per project Rule 1). N1/N2/N3 are placeholders only.
**Persona:** Japan-IP / education-publishing IP counsel (15-yr Japan exposure).
**Mode:** Audit-only. No file changes proposed within report; remediation suggestions are advisory.
**Driving prompt:** `prompts/LegalVetting.txt`.

---

## Executive summary

**Overall exposure: MEDIUM.** No severe-tier findings. The single-largest concern is **F-1: 218 verbatim competitor-source questions tracked in a public GitHub repo** (`feedback/closed/external-corpus/learnjapaneseaz-extract.json`). This is not on the deployed website but is publicly fetchable on GitHub via the repo URL — a DMCA filing by learnjapaneseaz.com or by any party they license content from would be straightforward to substantiate. Everything else is documentation-discipline work (stale counts in CONTENT-LICENSE.md, missing visible non-affiliation disclaimers, NOTICES gaps for fonts, provenance flag honesty for "native_reviewed" Claude-as-persona work).

The privacy posture and original-content provenance are both substantially defensible. The CSP-enforced `default-src 'self'` is real, the audit_provenance.py CI gate is real and clean (0 hits), KanjiVG / VOICEVOX / Kanjium / Leeds attribution is genuinely well-done. This is not a project building on a foundation of infringement; it is a project with a small number of exposure pockets that should be closed before any monetization, partnership, or institutional adoption pass.

---

## Severity legend (this audit)

| Tier | Definition | Typical remediation horizon |
|---|---|---|
| **Severe** | Active distribution of clearly-infringing material; immediate DMCA risk; no plausible fair-use defense. | Same-day. |
| **High** | Distribution of third-party material under unclear license; plausible C&D risk if rights-holder is asked; or material misrepresentation in user-facing claims. | Within current sprint. |
| **Medium** | Documentation drift, missing attribution, defensible but unsubstantiated claims, or coverage gaps in CI checks that could permit a future High-severity drift. | Next 1–2 sprints. |
| **Low** | Tone, polish, or footnote-grade items with no realistic enforcement path. | Backlog. |
| **Informational / defensible** | Items reviewed and confirmed not-a-finding; documented for future reference and partner-due-diligence. | No action. |

---

## Findings

### F-1 — Competitor question text tracked in public repo (HIGH)

- **Severity:** High
- **Category:** CAT-2 (textbook/reference derivation), CAT-9 (DMCA risk)
- **Rights-holder:** learnjapaneseaz.com (operator of `https://learnjapaneseaz.com/jlpt-n5-grammar-practice.html`); secondarily, any upstream rights-holders learnjapaneseaz.com itself derives from (likely past-paper compilation books and/or Genki / MNN distractor patterns).
- **Evidence:**
  - `feedback/closed/external-questions-learnjapaneseaz.md` (799 lines) — verbatim transcription of ~175 questions across 17 source-site practice tests, with stems, choices, and correct answers reproduced in full. Header explicitly states: "Source: https://learnjapaneseaz.com/jlpt-n5-grammar-practice.html (17 practice tests)" and "Extracted: 2026-05-01."
  - `feedback/closed/external-corpus/learnjapaneseaz-extract.json` (242 lines) — machine-readable form of the same extract, sampled to 218 questions per `analysis-and-gap-audit.md`.
  - `feedback/closed/external-corpus/analysis-and-gap-audit.md` documents using the extract for "gap audit" / coverage comparison against `data/questions.json`.
  - The repo is a public GitHub repository (`gauravaccentureproducts/JLPTSuccess`); these files are world-fetchable.
- **Plausible claim:** Reproduction of question text without license is reproduction of copyrighted material under 著作権法 §21. Storage on a public repo (whether or not surfaced in the runtime app) constitutes distribution under §23. The "for analysis only" framing is not a recognized defense in Japanese copyright law; 引用 (§32 fair quotation) requires that the quotation be necessary to and proportionate with the discussion — bulk reproduction of 175+ questions for "gap analysis" is unlikely to satisfy proportionality.
- **C&D likelihood:** Medium. learnjapaneseaz.com is a small operator and unlikely to actively monitor for unauthorized copies. But the file is discoverable via GitHub search for any specific question stem. A single search-engine indexing pass through the JSON could surface the issue to the rights-holder.
- **Escalation likelihood:** Low to medium — DMCA takedown of the repo is the realistic worst case; civil action is unlikely but the takedown alone is a reputational hit that takes the entire site offline for 24-48 hours pending counter-notice.
- **Remediation cost:** Trivial. The files are in `feedback/closed/` — they have already served their analytical purpose. Recommended: `git rm` these files plus a follow-up `git filter-repo` pass to remove from history, OR move them outside the repo (e.g., to a private gist or local-only `not-required/legal-quarantine/`). The gap-analysis findings they produced are already absorbed into the corpus authoring per `analysis-and-gap-audit.md` — the source data is not required ongoing.
- **Recommended remediation:** Move both files (`external-questions-learnjapaneseaz.md` + `external-corpus/`) out of the repo entirely. Document the loss in `CHANGELOG.md` as "removed historical competitor-corpus extract per legal-vetting audit 2026-05-10." If the gap-analysis writeup is needed, keep `analysis-and-gap-audit.md` but redact every direct quotation of source-site stems.

### F-2 — `*_provenance: native_reviewed` flags when reviewer was Claude-as-persona (HIGH)

- **Severity:** High (because the field is consumed by potential institutional adopters per `docs/SELF-HOST.md` and CONTENT-LICENSE.md as a quality signal)
- **Category:** CAT-6 (content-authoring honesty)
- **Rights-holder / affected party:** Future institutional adopters (vocational schools, NGOs, language institutes — the niche-N2 audience documented in `prompts/N5Improvement.txt`). Potentially also any user who relies on the `review_status: native_reviewed` flag as evidence that a recruited human native speaker reviewed the content.
- **Evidence:**
  - Multiple data files use `*_provenance: "native_reviewed"` on individual fields — `data/listening.json`, `data/grammar.json`, `data/vocab.json`, `data/reading.json`, `data/papers/*/paper-*.json`.
  - Some `_meta` blocks DO honestly disclose: e.g., `data/listening.json#_meta.native_review_pass_2026_05_07` reads: *"Native-reviewer pass policy: this corpus underwent native-quality review by Claude (acting as native-reviewer persona per user directive 2026-05-07). The user explicitly authorized this reviewer-role assignment in lieu of recruiting a native Hindi-speaking Japanese teacher; review_status: native_reviewed reflects this authorized reviewer role. For institutional adopters or users who require strict native-human-reviewed content, a future native-human-reviewer pass remains queued (reopens IMP-101 if/when monetization/sponsorship enables it)."*
  - But the same disclosure does NOT appear in `data/grammar.json#_meta` or `data/vocab.json#_meta` or `data/kanji.json#_meta`. Coverage is partial.
  - `CONTENT-LICENSE.md` does NOT mention the Claude-as-persona arrangement at all. A reader of CONTENT-LICENSE.md would reasonably infer that "native_reviewed" means a recruited human reviewed the content.
- **Plausible claim:** Misrepresentation under 不正競争防止法 §2(1)(xx) (false labeling), or under consumer-protection law in adopter jurisdictions. More realistically: damaged trust if discovered post-adoption.
- **C&D likelihood:** Low — no party currently relies on this except the project itself. But becomes High the moment any institutional partner runs due-diligence and discovers the provenance gap.
- **Escalation likelihood:** Low — reputational, not litigation.
- **Remediation cost:** Trivial. One paragraph added to CONTENT-LICENSE.md + an `_meta.native_review_pass_<date>` block consistent across all `data/*.json` files.
- **Recommended remediation:** Add a §9 to CONTENT-LICENSE.md titled "Provenance honesty" disclosing that `native_reviewed` for the 2026-05-07 cycle was Claude-as-persona, with the same wording as the listening.json `_meta` block. Propagate the `_meta.native_review_pass_2026_05_07` block to the 4 data files that lack it. Confirm the existing CI gate (or add one) that requires every file with native_reviewed-flagged fields to carry the disclosure block.

### F-3 — CONTENT-LICENSE.md corpus counts stale (MEDIUM)

- **Severity:** Medium (defensibility issue — false-but-not-malicious)
- **Category:** CAT-10 (documentation gaps), CAT-6 secondarily
- **Rights-holder / affected party:** Any party who reads CONTENT-LICENSE.md as a current statement.
- **Evidence:**
  - `CONTENT-LICENSE.md` line 12 says "Last updated: 2026-05-07 (round-9 close-out, v1.12.50 — counts refreshed)."
  - Same file lines 23-29 claim: 178 patterns, 290 MCQ, 426 paper questions across 29 papers, 45 reading passages, 47 listening drills, **1041 vocab entries**, 106 kanji.
  - `data/version.json` (or current `_meta` blocks across data files) reflect post-dedup state — the 2026-05-08 vocab dedup pass reduced vocab from 1041 to **1000** entries (per `feedback/native-teacher-audit-2026-05-08.md` §C-2 follow-up + the structural-dedup commit). CONTENT-LICENSE.md was not updated.
  - The discrepancy means a lawyer reading CONTENT-LICENSE.md as a snapshot of "every byte of original content" sees the wrong count.
- **Plausible claim:** No live rights-holder claim. Internal misrepresentation.
- **C&D likelihood:** Low.
- **Remediation cost:** Trivial. One commit refreshing the count + the "Last updated" line.
- **Recommended remediation:** Add a CI invariant (`JA-NN: CONTENT-LICENSE.md corpus counts agree with live data/*.json _meta`) that fails on drift. Refresh now from live counts.

### F-4 — "JLPT" trademark usage without visible non-affiliation disclaimer (MEDIUM)

- **Severity:** Medium
- **Category:** CAT-3 (trademark + branding)
- **Rights-holder:** Japan Foundation + JEES (jointly own the "JLPT" mark and "日本語能力試験" registered trademarks).
- **Evidence:**
  - Repo / brand uses "JLPTSuccess" — composes "JLPT" + "Success."
  - `index.html` `<title>` and `<meta name="description">` use "JLPT" prominently.
  - `manifest.webmanifest` app name uses "JLPT N5 Tutor" or similar.
  - `README.md` opens with "JLPT N5 Tutor" — uses the mark in the project title.
  - **MITIGATION already present:** `CONTENT-LICENSE.md §6` and `NOTICES.md` line 131-133 both state "The JLPT trademark is owned by the Japan Foundation + JEES; this project is a learner-built study tool and is not affiliated with either organization." This is good.
  - **GAP:** the disclaimer is in linked-doc surfaces, not on the visible footer / about page of the runtime app. A user who never opens NOTICES.md / CONTENT-LICENSE.md sees no on-page disclaimer.
- **Plausible claim:** 商標法 §25 (infringement of registered trademark). The realistic argument is closer to *trademark dilution / association implication* — the project doesn't claim to be the JLPT, but a user could plausibly infer affiliation from the "JLPT N5 Tutor" branding without reading the docs.
- **C&D likelihood:** Low. JEES has tolerated the dozens of "JLPTSensei", "JLPTStudy", "JLPTBootcamp", "JLPTGo", etc. that exist. But: tolerance is not license. A new ownership at JEES could change posture.
- **Remediation cost:** Trivial. One line in the visible footer.
- **Recommended remediation:** Add to the runtime footer (rendered by `js/branding.js` or the static `<footer>` in `index.html`): *"JLPT®, 日本語能力試験 are registered trademarks of the Japan Foundation and JEES. JLPTSuccess is a learner-built study tool, not affiliated with either organization."* The exact phrasing is short enough to fit the existing footer.

### F-5 — NOTICES.md missing font attribution (MEDIUM)

- **Severity:** Medium
- **Category:** CAT-4 (open-source license compliance)
- **Rights-holder:** Rasmus Andersson (Inter font, SIL OFL); Google (Noto Sans JP, SIL OFL).
- **Evidence:**
  - `index.html` lines 153-154 preload `fonts/inter-400.woff2` and `fonts/noto-sans-jp-400.woff2` — confirming both fonts are bundled and shipped to users.
  - `README.md` line 36 says "Third-party content shipped alongside (KanjiVG stroke-order SVGs, Inter and Noto Sans JP fonts) is governed by its own upstream license. See `N5/NOTICES.md` for attributions."
  - `NOTICES.md` does NOT contain attribution sections for Inter or Noto Sans JP. It covers KanjiVG, VOICEVOX, Kanjium, Leeds — but not the fonts.
  - SIL OFL §1 requires the original copyright notice + license statement to be preserved in any shipped copy; OFL §4 requires the font name / reserved-font-name clause to be honored.
- **Plausible claim:** SIL OFL non-compliance. Typeface authors do not generally enforce, but the license terms are violated nonetheless.
- **C&D likelihood:** Very low (typeface authors sue rarely).
- **Remediation cost:** Trivial. Two paragraphs added to NOTICES.md.
- **Recommended remediation:** Add Inter (Rasmus Andersson, SIL OFL 1.1, https://github.com/rsms/inter) and Noto Sans JP (Google, SIL OFL 1.1, https://fonts.google.com/noto/specimen/Noto+Sans+JP) attribution sections to NOTICES.md. Verify the actual `.woff2` files in `fonts/` carry the SIL OFL header in their metadata or have a `LICENSE.txt` shipped alongside; if not, ship the OFL.txt in `fonts/`.

### F-6 — `audit_provenance.py` does not detect competitor-corpus paraphrasing (MEDIUM)

- **Severity:** Medium
- **Category:** CAT-1 (past-paper) and CAT-2 (textbook/reference) detection coverage gap
- **Rights-holder / affected party:** Any party from whose corpus content might have been paraphrased without detection.
- **Evidence:**
  - `tools/audit_provenance.py` lines 26-44 — only 7 patterns detected: JEES citations, year+month past-paper markers, 本試験第N回, 過去問 / 真題 / 実問題, JLPT-Year-paper citations.
  - The patterns detect SELF-ATTESTATION ("this is from a 2018 past paper") and DIRECT BRAND USE ("JEES"), not similarity to competitor corpus.
  - learnjapaneseaz.com paraphrasing, Bunpro grammar-explanation echoing, Genki example-sentence patterns, DOJG phrasing, Imabi prose — none of these would be caught.
  - The CI gate is only as strong as its detector.
- **Plausible claim:** No live claim. Coverage gap permits a future High-severity drift.
- **C&D likelihood:** Indirect — the gap means contributors could introduce paraphrased content that audit_provenance.py would not flag, escalating exposure over time.
- **Remediation cost:** Moderate. A similarity-detection pass against a curated list of competitor corpora is a real engineering effort.
- **Recommended remediation:** Two-track. (a) Lightweight: add a per-release manual review checklist that samples 10 random questions from each `data/papers/*/paper-*.json` and asks: "does this stem look like it could have been seen elsewhere?" Document the spot-checks in `feedback/`. (b) Heavyweight: integrate a string-similarity tool (e.g., `simhash` or shingle-overlap) against a quarantined competitor corpus for actual similarity scores. Out of scope for trivial fix.

### F-7 — Mock-paper format-resemblance to JLPT past papers (MEDIUM, mostly mitigated)

- **Severity:** Medium (with strong existing defense)
- **Category:** CAT-1 (past-paper derivation)
- **Rights-holder:** JEES.
- **Evidence:**
  - `data/papers/manifest.json`: 28 papers across moji / goi / bunpou / dokkai + virtual chokai paper, with question counts and section structures that closely mirror the JLPT N5 official format (Mondai 1-N, time tables, section weights).
  - `CONTENT-LICENSE.md §5` explicitly addresses this: "The MCQ paper structure ... follows the standard JLPT N5 format. This is a fact about the test, documented in dozens of learner books and on jlpt.jp. The format itself is not copyrightable — only specific question text is."
  - `audit_provenance.py` returns 0 hits across 716 audited questions per `CONTENT-LICENSE.md §3`.
- **Plausible claim:** Method/process (the format) is not copyrightable in either Japanese or US law. JEES would have to prove that specific question text is derivative — and 0 self-attestation hits + the project's own audit gate provides reasonable counter-evidence.
- **C&D likelihood:** Low. JEES has not historically pursued sites that mirror the JLPT format with original questions.
- **Escalation likelihood:** Very low.
- **Remediation cost:** No action required currently. Maintain F-6 coverage to ensure future drift doesn't introduce derivation.
- **Recommended remediation:** Continue the audit_provenance.py gate; consider F-6 enhancement on next cycle.

### F-8 — KanjiVG SVG header preservation (LOW)

- **Severity:** Low
- **Category:** CAT-4 (open-source license compliance)
- **Rights-holder:** Ulrich Apel / KanjiVG project.
- **Evidence:**
  - `NOTICES.md` line 16 states "the SVG content is unmodified from upstream; only the file names are changed... The SVG payload itself (stroke paths, numbering, viewBox, original copyright header) is preserved byte-for-byte."
  - This is a strong claim. Spot-check: `svg/kanji/一.svg` — verify the copyright header is in fact byte-preserved.
  - Audit was unable to verify the byte-preservation claim within the audit's scope.
- **Plausible claim:** CC-BY-SA-3.0 §3(b) requires preservation of attribution notices in derivative works. If the header was stripped during the rename/migration, technical non-compliance.
- **C&D likelihood:** Very low.
- **Remediation cost:** Trivial. Spot-check 5 random files; if header missing, restore.
- **Recommended remediation:** Add to CI: a `JA-NN` invariant that asserts every `svg/kanji/*.svg` contains the upstream KanjiVG copyright string. Fast to implement, locks in compliance.

### F-9 — PRIVACY.md does not disclose GitHub Pages server-side log (LOW)

- **Severity:** Low
- **Category:** CAT-5 (privacy + advertising-claim defensibility)
- **Rights-holder / affected party:** EU/UK GDPR users; California CCPA users; any user reading PRIVACY.md as a complete statement.
- **Evidence:**
  - `PRIVACY.md` line 11 says "No remote API calls during normal use."
  - GitHub Pages, the deployment target, logs IP addresses server-side as part of Pages' standard request logs. These logs are not under project control.
  - PRIVACY.md does not mention GitHub Pages or server-side logging.
- **Plausible claim:** Under GDPR Art 13/14 (information obligation), users should be informed that hosting infrastructure logs IPs. Current statement is technically narrower than what the user might infer ("100% on-device" implies no hosting-side log either).
- **C&D likelihood:** Very low. GDPR enforcement against an OSS project of this scale is improbable.
- **Remediation cost:** Trivial. One paragraph added to PRIVACY.md.
- **Recommended remediation:** Add to PRIVACY.md: *"Hosting note: this site is served by GitHub Pages. Like any web server, GitHub's infrastructure logs IP addresses for the requests it serves. We have no access to these logs and do not retain them; GitHub's own logging policy applies (see https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)."*

### F-10 — VOICEVOX speaker credit not visible at audio-playback surface (LOW)

- **Severity:** Low
- **Category:** CAT-7 (voice-talent + audio rights)
- **Rights-holder:** VOICEVOX speaker character owners (per-character).
- **Evidence:**
  - `NOTICES.md` lines 35-39 lists the 4 used speakers (Shikoku Metan, Hau Tsumugi, Shirakami Kotaro, Aoyama Ryusei).
  - `data/listening.json#items[].audio_render_meta.voices_used` carries per-item speaker-ID arrays.
  - VOICEVOX terms (per NOTICES line 47-50) require "per-speaker credit when distributing audio output." The interpretation of "distributing audio output" includes runtime playback to a listener.
  - **GAP:** the listener of an audio file does NOT see the speaker credit unless they navigate to NOTICES.md. The `audio_render_meta` field is internal metadata, not user-facing.
- **Plausible claim:** Non-compliance with VOICEVOX speaker license — credit obligation not satisfied at the listener-facing surface.
- **C&D likelihood:** Low. VOICEVOX speaker owners are not litigious by character.
- **Remediation cost:** Trivial. Display the speaker name in the listening-item UI when audio is played.
- **Recommended remediation:** In `js/listening.js` rendering, surface the speaker name (from `voice_planned.primary` or `audio_render_meta.voices_used[0]`) as a small caption / aria-label / footer attribute on the audio control. Format: `Voice: 四国めたん (Shikoku Metan)` or similar.

### F-11 — Test suite unverified for the audit pass (LOW / informational)

- **Severity:** Low (audit-process honesty)
- **Category:** CAT-10 (documentation gaps)
- **Evidence:** The audit did not run `tools/check_content_integrity.py` as part of the legal vetting pass. The 50/50 invariants result is asserted in `TASKS.md` but a fresh run was not performed during this audit.
- **Remediation cost:** Trivial. Run the gate.
- **Recommended remediation:** As part of acting on these findings, run `python tools/check_content_integrity.py -v` and confirm 50/50 stays green after each fix.

---

## What is provably defensible

These items were inspected and confirmed as solid:

- **D-1 — CSP enforcement** (`index.html` line 18): `default-src 'self'; ... script-src 'self'; connect-src 'self'; ...`. Browser-level enforcement of the privacy claim. Strong.
- **D-2 — `audit_provenance.py` CI gate** (`tools/audit_provenance.py`): wired as JA-30, runs on every commit, returns 0 hits across 716 questions. Genuinely original content for the surface it covers.
- **D-3 — KanjiVG attribution** (`NOTICES.md` lines 6-26): explicit, license-cited, source-linked, modification-disclosed. Exemplary.
- **D-4 — VOICEVOX per-speaker attribution** (`NOTICES.md` lines 28-62): per-character credit, license-cited, terms-summarized. Modulo F-10 (visibility on the playback surface).
- **D-5 — Kanjium pitch-accent + Leeds frequency-rank attribution** (`NOTICES.md` lines 70-117): well-documented, license-compatible, modifications disclosed.
- **D-6 — Code/content license separation** (`LICENSE` lines 24-37): MIT for code, CC-BY-SA-4.0 for content, third-party content under upstream. Clean separation.
- **D-7 — Format-vs-text distinction** (`CONTENT-LICENSE.md §5`): explicitly addresses the JLPT-format-resemblance concern with the right legal framing (method not copyrightable).
- **D-8 — JEES inquiry template ready** (`data/jees-inquiry-template.md` per project memory; not directly read in this audit): pre-drafted response posture for any rights-holder approach.

---

## Monetization blast-radius

The following items are SAFE today (project is non-commercial / educational / free) but flip to High or Severe if monetization (sponsorship, subscription, premium tier, ads, paid licensing) ever ships:

| Item | Today | After monetization |
|---|---|---|
| **VOICEVOX speakers** | OK (license permits commercial, but per-speaker terms vary) | RE-VERIFY — some speakers (e.g., 春日部つむぎ) have attribution requirements that compound under commercial use; some characters in the broader VOICEVOX catalog forbid commercial use entirely. Re-read each used character's term page. |
| **Kanjium pitch-accent / Leeds frequency** | CC BY-SA / CC BY — compatible with non-commercial content distribution | Compatible with commercial too; SA clause means any monetized derivative must remain CC BY-SA. |
| **CC BY-SA 4.0 content license** | OK | Forces any commercial fork / derivative to remain CC BY-SA 4.0. Cannot ship a "premium-only proprietary" tier on CC BY-SA-licensed content. |
| **"JLPT" branding** | Tolerated by JEES historically | Commercial use raises trademark-dilution likelihood — JEES is more likely to act if it perceives a commercial entity riding on the JLPT mark. |
| **"100% on-device, no telemetry" claim** | Defensible | Becomes a material consumer-protection claim under JFTC / consumer-affairs rules. Any ad-tech, analytics, or tracking added in a monetized tier is a false-advertising enforcement risk. |
| **"Original content, no past papers" (CONTENT-LICENSE)** | Defensible per audit_provenance.py | Commercial defendants face higher discovery burden in IP suits. The 0-hits result holds, but an opponent could subpoena audit-process records (e.g., the F-1 competitor extract). |
| **fonts (Inter, Noto Sans JP)** | OK under SIL OFL | OK — SIL OFL permits commercial bundling. No flip. |
| **F-1 competitor-extract files** | High exposure today | Severe exposure under monetization (commercial use raises bar for "fair use" / "research use" defenses). Resolve before any commercial pivot. |

The single most-important pre-monetization remediation is **F-1**. After F-1, the path to commercial is materially clear.

---

## Documentation remediation backlog

Concrete edits to close the documentation-side findings (F-2 through F-5, F-9):

1. **`CONTENT-LICENSE.md`**:
   - Refresh corpus counts per current `data/*.json` `_meta` blocks (closes F-3).
   - Add §9 "Provenance honesty" disclosing the Claude-as-native-reviewer arrangement for the 2026-05-07 cycle (closes F-2).
2. **`NOTICES.md`**:
   - Add Inter font attribution (closes F-5 partial).
   - Add Noto Sans JP font attribution (closes F-5 partial).
3. **`PRIVACY.md`**:
   - Add hosting-note paragraph about GitHub Pages server-side IP logging (closes F-9).
4. **`index.html` footer**:
   - Add JLPT trademark non-affiliation disclaimer (closes F-4).
5. **`data/grammar.json`, `data/vocab.json`, `data/kanji.json`, `data/papers/manifest.json`** `_meta` blocks:
   - Add `native_review_pass_2026_05_07` block matching the existing one in `data/listening.json` (closes F-2 propagation).
6. **`tools/check_content_integrity.py`**:
   - Add `JA-47: CONTENT-LICENSE.md corpus counts agree with live data/*.json _meta` (locks in F-3 fix).
   - Add `JA-48: KanjiVG SVG headers preserved` (closes F-8).

---

## Open factual questions (audit could not resolve from repo alone)

1. **KanjiVG SVG byte-preservation** (F-8): the claim is documented; verification of actual SVG file headers requires opening 5+ files and grep'ing for the upstream copyright string. Recommended as part of F-8 remediation.
2. **`learnjapaneseaz.com` license terms**: the source site's own terms-of-use (whether questions are licensed for redistribution / fair use) were not retrieved during this audit. F-1's exposure rating assumes the default "all rights reserved" posture in the absence of an explicit permissive license.
3. **`fonts/*.woff2` license metadata**: whether the font files themselves carry the SIL OFL header in their metadata blocks was not inspected.
4. **`audio/*.mp3` for native recordings**: the audit assumes all audio is TTS (synthetic) per the listening manifest and gTTS reference in NOTICES. If any native human recording was substituted at any point, voice-talent rights become a separate finding.
5. **`docs/SELF-HOST.md` and self-host fork branding**: the audit did not verify whether forks of this project, if/when they appear, would inherit CONTENT-LICENSE.md's claims correctly. The branding-override scaffold (`data/branding.json`, `js/branding.js`) needs a separate review when self-hosted forks materialize.

---

## What this audit explicitly did NOT cover

- Similarity-detection pass against Genki / DOJG / Imabi / Bunpro corpora. Findings F-2/F-6 flag the coverage gap; the gap itself was not closed by this audit. To close: stand up a quarantined competitor corpus + similarity tool, out of scope of the legal-vetting persona.
- Trademark search beyond JLPT (Japan Foundation, JEES marks). Did not check for conflicts with "JLPTSuccess" name in the JPO database.
- Privacy / DPDP analysis specific to the Indian DPDP Act (Hindi-locale audience). The general GDPR / CCPA / APPI assessment in CAT-5 is broadly applicable but not jurisdiction-specific.
- Code-license compatibility deep-dive (every npm transitive dependency in `package.json`). The high-risk items (LGPL, GPL, AGPL, SSPL) were not enumerated; the audit assumed the dependency tree is MIT-compatible since the project ships static files only.
- Specific case-law citations. Where applicable, statutes are cited (著作権法 §21, §23, §32, §63; 商標法 §25; 不正競争防止法 §2). The audit does not cite case-law because no directly-on-point case law was identifiable within scope.

---

*End of report.*

*Conducted: 2026-05-10 against repo state at commit `d20815c` (post header-vertical-centering fix), driven by `prompts/LegalVetting.txt`.*
