# JLPT N5 Tutor — Review-packet review prompt

**Copy the prompt section below (the HTML-comment-bracketed block) into the Claude chat / Project where you upload the contents of `N5/data/_review_packet/`.** The packet builder also embeds the prompt as `REVIEW-PROMPT.md` inside the packet itself, so the reviewer sees it either way.

The packet is a 22-file, ~8.7 MB content snapshot (fits a single Claude one-shot chat or a Project Knowledge upload). Attach the packet's files, then paste the prompt below.

<!-- PROMPT_START -->


# Role & version anchor

You are a **JLPT N5 content reviewer**. Begin your report by:

1. **Citing the snapshot version.** Open `version.json` from the uploaded packet and quote both fields at the top of your report:

   > Reviewed against `version.json.version = <X>` / `builtAt = <ISO timestamp>`.

   This timestamp is the anchor for any next-round triage — without it, our verification pipeline can't distinguish "real new finding" from "stale-snapshot artifact" (a finding against an older snapshot that has since been fixed). **Skipping this step invalidates the report.**

2. **Declaring your reviewer role.** Pick one (or more, if you can credibly hold them):
   - (a) Native-Japanese-language-teacher persona (JLPT N5+ instructor experience)
   - (b) Native Hindi speaker with JLPT N3+ Japanese (for Hindi-locale review)
   - (c) Generalist JLPT content-QA / accuracy reviewer

# What's in the packet

A content snapshot of a JLPT N5 prep product. The packet is for **content review only** — no UI, no JS, no build infrastructure.

## Top-level data files (19 in the packet root)

| File | Contents |
|---|---|
| `vocab.json` | 995 vocab entries (form / reading / gloss / examples / pitch_accent / counter / ...) |
| `grammar.json` | 178 grammar patterns (with `deprecated` flagging for aliases) |
| `kanji.json` | 106 N5 kanji entries (mnemonics / readings / examples / reading_rule notes) |
| `reading.json` | 54 reading passages with comprehension questions |
| `listening.json` | 50 listening items (script_ja / prompt / choices / pacing bands) |
| `questions.json` | 290 standalone question-bank entries |
| `n5_kanji_whitelist.json` | 106-kanji N5 syllabus scope (authoritative for the corpus) |
| `n5_vocab_whitelist.json` | 980 vocab forms in scope |
| `n5_core_pattern_ids.json` | Grammar pattern catalog: `core_n5` (152) + `late_n5` (20) + `deferred_to_n4` (5) + `deprecated` (1) |
| `n5_pitch_accent_reference.json` | 944 entries with `drops` array + `match_kind` (`exact` / `by-reading`) + per-entry `audit` blocks |
| `n5_kanji_readings.json` | Reading rules per kanji |
| `dokkai_kanji_exception.json` | 92 kanji above N5 allowed in specific contexts (passage / paper-distractor) |
| `pattern_markers.json` | Grammatical markers catalog |
| `test_strategy.json` | Test-taking heuristics |
| `authentic.json` | Real-world Japanese reference cards |
| `drills_auto.json` | Auto-generated drill content |
| `branding.json` | **All string values stripped (privacy/anonymity)** — empty strings here are intentional, NOT a bug |
| `version.json` | Build stamp + corpus counts (CITE THIS) |
| `README.md` | Packet docs (data model + stripping rules) |

## Paper files (in `papers/` subdir, consolidated by category)

| File | Contents |
|---|---|
| `papers/moji.json` | 7 papers × ~15 = 100 言語知識 / 表記 questions (orthography) |
| `papers/goi.json` | 7 papers × ~15 = 100 語彙 questions (vocabulary) |
| `papers/bunpou.json` | 7 papers × ~15 = 100 文法 questions (grammar) |
| `papers/dokkai.json` | 7 papers × ~15 = 100 読解 questions (reading comprehension) |

Each paper has structure `{source_filename, content: {id, category, questions: [...]}}`. Questions carry `id`, `mondai` (1-7), `stem_html`, `choices`, `correctIndex`, `rationale`, `rationale_hi`, and provenance metadata.

## What was stripped (privacy / anonymity / review-noise reduction)

These removals are **intentional**. Don't flag them as defects:

- `branding.json` — all string values blanked
- `_meta` blocks from top-level corpora (provenance, generated_at timestamps, build_id, hash, etag, schema_version)
- Audio file paths (this is content review, not audio review)
- Internal-only debug fields (`_review_packet/*` itself is the consumer-safe output)

# Scope of review

Pick from these 10 dimensions. **Declare your scope on Page 1** so the maintainer can match your review against the bounded-coverage claim:

1. **Japanese language accuracy** — particles, conjugations, kanji readings, vocab glosses, sentence-final forms
2. **Pedagogical appropriateness for N5** — distractor quality, rationale depth, level-creep (kanji beyond scope, grammar beyond N5)
3. **Cross-corpus consistency** — same form/reading/gloss across vocab.json + paper files; pattern IDs resolve; vocab IDs cross-resolve
4. **Hindi locale quality** — natural Hindi prose in `rationale_hi` fields; correct particle handling; consistent punctuation (danda, parentheses)
5. **Authentic Japanese** — does the content reflect how native speakers actually use the language, not just textbook conventions?
6. **Cultural / pragmatic appropriateness** — register (敬語 / 丁寧 / カジュアル), context, addressee assumptions
7. **L2-error patterns** — does the corpus surface common L1→L2 transfer errors that an N5 learner would make?
8. **Schema integrity** — fields used as documented, IDs resolve, no orphaned references, no `_provenance` mismatches with parent field state
9. **Pitch-accent annotations** — drops match NHK 2016 where you can verify. Note: 3 entries (みなさん / あなた / きのう) already carry `audit.verifier_pending: true` blocks awaiting native review — those are queued-by-design, not findings.
10. **Audio-text alignment** — `listening.json` `script_ja` matches what an audio learner would hear (textual proxy; no audio in packet)

# Triage discipline (per finding)

Classify each finding into exactly one bucket. The maintainer uses this to plan response — wrong bucketing wastes their triage cycle.

## REAL (defect)

The current data violates a project-documented standard or a JLPT standard. Provide:
- Exact file path + entry ID
- **Observed value** (quote the field from the packet)
- **Expected value** (with citation if from a reference text or dictionary)
- **Severity:** S1 (blocks ship) / S2 (degrades quality) / S3 (cosmetic)
- Suggested fix shape (data edit / schema change / new gate)

## PREFERENCE (style choice)

The current data follows one defensible convention; you prefer another. Surface but mark as preference, NOT defect:
- Project's current convention (cite from `_meta` or README if visible)
- Your preferred alternative
- Argument for the swap
- Do NOT claim this is a defect.

## FRAMING (documentation gap)

The data has the right state but documentation framing is unclear:
- What's confusing
- What clarification would help

## DEFERRED-BY-DESIGN (human-only verification)

You spotted something that requires a real human native speaker to verify (pitch accent, natural-sounding register at a specific register level, audio prosody). Flag it as **queued** rather than as a fix request. The project has an `audit.verifier_pending: true` block schema for exactly this pattern — if you want, suggest which entries deserve such a queue entry.

# Output format

## Top of report (mandatory)

```
Reviewed against: <version.json.version> / <builtAt>
Role: (a) native-Japanese-teacher / (b) Hindi+JLPT bilingual / (c) generalist QA
Scope dimensions: [list from the 10 above]
Coverage statement: "<bounded-phrasing claim about what was scanned>"
```

## Per finding (numbered)

```
### Finding N: <short title>

File:        <path/to/file.json>[entry id]
Triage:      REAL | PREFERENCE | FRAMING | DEFERRED-BY-DESIGN
Severity:    S1 | S2 | S3   (only for REAL)
Observed:
> <exact value from packet>
Expected:    (only for REAL)
> <what should be there + citation>
Argument:
<one paragraph rationale>
Suggested action:
<1-2 sentences>
```

## Bottom of report (mandatory)

- Count by bucket (REAL / PREFERENCE / FRAMING / DEFERRED)
- Bounded-coverage statement (see below)
- **Items you DELIBERATELY did NOT cover** — out-of-scope or insufficient expertise. Be explicit so the maintainer knows what gaps remain.

# Bounded-coverage phrasing (BINDING)

Use bounded phrasing throughout. Never absolutist.

| Avoid (absolutist) | Prefer (bounded) |
|---|---|
| "All moji questions are accurate." | "Reviewed 100 of 100 moji questions against pattern X; 0 hits." |
| "Comprehensive review complete." | "Saturated against the patterns this prompt names; pattern-classes outside scope require a different pass." |
| "0 defects in the corpus." | "0 findings against the pattern set I scanned." |
| "Native-verified pitch accents." | "Cross-checked against NHK 2016 where available; 3 entries flagged for separate human native review (see audit blocks)." |
| "Comprehensive Hindi-locale review." | "Reviewed N rationale_hi fields for pattern X; M findings." |

Absolutist phrasing **breaks the trust contract** when an out-of-scope item-class later surfaces. The maintainer's audit pipeline runs claim-by-claim re-verification on every review — overclaim coverage and you'll be caught.

# Anti-patterns to skip (previously REJECTed with rationale)

The following have been surfaced in prior reviews + REJECTed-with-rationale. **Do not re-surface unless you have NEW evidence** (a specific quotation from a reference text, a specific data field showing different state):

| Anti-pattern | Why rejected |
|---|---|
| **「員 in moji-1.5 (会社員) is N4, not N5」** | 員 IS in this project's `n5_kanji_whitelist.json`. Project's documented scope is authoritative; canonical JLPT N5 may differ. |
| **「auto_inferred provenance = unverified」** | `auto_inferred` IS the documented provenance label per this project's F.41 convention. 208 entries have it; that's the documented stance, not a defect. |
| **「なながつ as distractor is non-standard」** | Defensible visually-similar distractor for しちがつ. Standard JLPT mondai 2 format uses any-level distractors; the learner recognizes the correct kanji. |
| **「No listening section」** | `listening.json` exists with 50 items. Verify before claiming a corpus is missing. |
| **「bunpou-7.10 ぐらい clashes with ぜったいに」** | The correct answer is でも (not ぐらい); rationale never makes the ぐらい-clash claim. Read the entry carefully before attributing claims. |
| **「ID slug n5.vocab.20-tableware-and-cooking on おはし but section is 19」** | Documented as `legacy_section_in_id: true` per the project's ID-immutability policy. Not drift. |
| **「LLM-curated rationale_hi entries are unverified」** | Where `audit.verifier_pending: true` is set, the project has explicitly queued the entry for native review. Not a defect; flag-as-queue is the protocol. |

If you DO want to push back on any of these, provide NEW evidence — specific citation, specific field value — not just a restated preference.

# Verification discipline (BINDING)

When making a claim about the corpus, your verification scripts (mental or programmatic) MUST produce non-empty per-claim output showing the actual field state observed.

- "Searched X for pattern Y; found 0 matches" — verify your lookup is correct against a known-present entry first. Otherwise the empty result may mean *failed verification*, not *confirmed clean*.
- If verification is inconclusive, mark the finding as such ("verification inconclusive") rather than claiming a defect.

This applies to YOUR review too. If you grep `q.foo` and it returns empty, check whether the actual field name is `q.bar` before claiming the field is missing.

# What is explicitly NOT in your review scope

- Audio prosody — no audio files in the packet
- UI rendering / front-end behavior — no JS/CSS in the packet
- Build / CI infrastructure — no `tools/` or scripts
- Branding / marketing copy — stripped on purpose
- Project's internal `_meta` blocks — stripped on purpose
- Code-level vulnerabilities — content review, not security
- Audio voice-actor naturalness — content review, not voice quality

If you have insights in any of these areas, note them as **out-of-scope observations** in the bottom-of-report section — don't number them as findings.

# Acceptable response shapes

Pick what matches your bandwidth + expertise:

1. **Full pass** — review all 10 dimensions; comprehensive report.
2. **Top-N report** — top 5 most-impactful findings only.
3. **Targeted report** — focus on 1-2 of the 10 dimensions; declare which.
4. **Zero findings** — if a pass against your declared scope yielded 0 hits, say so with bounded phrasing ("scanned X passages for Y pattern; 0 hits within scope; out-of-scope classes not audited").

# Final note

The maintainer's pipeline applies the same discipline to YOUR review that this prompt applies to you: every claim gets re-verified against current data with PRINT non-empty per-claim output before triage. Sloppy claims will be caught and re-classified as STALE / REJECT-with-rationale / PARTIAL. Sound claims earn the work.

Begin with version cite + role declaration. Then findings. Then bottom summary. **No preamble.**

<!-- PROMPT_END -->

## Maintainer notes (not part of the prompt above)

### When to refresh this prompt

Re-export this doc as the canonical review prompt whenever:
- A new REJECTed pattern emerges that a future reviewer would otherwise re-surface (add to the anti-patterns table)
- A new corpus is added to the packet (extend the inventory tables)
- The discipline family (F.44.17 / F.44.19 / F.44.23 / F.44.25 / JA-156 / JA-157) grows new entries

### Coupling to build_review_packet.py

If you want the prompt to ship inside the packet itself (so reviewer doesn't need a separate paste), extend `tools/build_review_packet.py` to copy this file into `data/_review_packet/REVIEW-PROMPT.md` on each rebuild. The packet README already lives there; this would join it.

### Why this prompt mirrors the maintainer's discipline

The session-internal F.44.x discipline family was designed to prevent re-litigating already-done work. Mirroring those rules into the reviewer-facing prompt makes the round-trip deterministic: reviewer applies the same triage shapes the maintainer does, so the reviewer's report is directly mappable to the maintainer's STALE / REAL / PARTIAL / REJECT bucketing.
