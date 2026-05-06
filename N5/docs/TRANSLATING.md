# Translating JLPTSuccess

> **2026-05-06 update — strategic narrowing to EN + HI.**
> The app previously shipped 5 locales (en + vi + id + ne + zh).
> Market research found that Vietnamese / Indonesian / Nepali /
> Chinese all sit in saturated competitive markets with established
> JLPT prep apps in their native language. **Hindi is the unique
> high-demand-low-competition gap** (India is the 5th-largest JLPT
> country worldwide; ~50K applicants/year; 73% at N5 or N4; no
> dedicated Hindi-medium prep app exists). The app now ships
> exactly two locales: `en` and `hi`. This doc was rewritten on
> the transition date.

Native Hindi speakers / Japanese-language teachers in India / serious
JLPT learners willing to contribute Hindi translations are the
unblocker for the project's strategic niche. This doc is the on-ramp.

## What needs translating

The app ships two parallel translation surfaces:

### Surface A — UI chrome (`N5/locales/hi.json`)

113 keys covering navigation labels, button text, settings labels,
footer, trust band, page titles, etc. The initial seed was
LLM-curated on 2026-05-06 (Phase 1 of the locale transition); a
native-review pass is the unblocker for promoting the bulk
`_meta.review_status` from `llm_curated` to `native_reviewed`.

### Surface B — content body (`N5/data/*.json`)

The actual lessons. Per-locale fields in each item:

| File | Field | Item count | Hindi seeded so far |
|---|---|---|---|
| `data/grammar.json`   | `meaning_hi` + `explanation_hi`     | 178 patterns | 0 |
| `data/grammar.json`   | `l1_notes.hi` (Hindi-specific gotchas) | 10 priority patterns | 0 |
| `data/vocab.json`     | `gloss_hi`                          | 1041 entries | 116 (top-frequency) |
| `data/kanji.json`     | `meanings_hi`                       | 106 entries  | 106 (all) |
| `data/reading.json`   | `explanation_hi` per question       | 45 passages  | 0 |
| `data/listening.json` | `explanation_hi` per item           | 47 items     | 0 |

Hindi seed-content guidance (script: `Devanagari`; register:
formal-but-friendly; preserve Japanese loan-words for technical JLPT
terminology like `कान्जी` for kanji where Hindi has no settled
equivalent) is in `prompts/LocaleTransitionEnHi.txt` §"HINDI SEED
CONTENT GUIDANCE". Read that section before contributing.

## Workflow

1. **Pick a surface** — vocab gloss, kanji meanings, grammar
   meaning + explanation, listening / reading explanations, or UI
   strings. Vocab gloss and grammar meaning_hi are the highest-
   leverage. Don't try to translate everything in one PR.
2. **Translate in batches** of 30-100 entries per PR. Keep each PR
   reviewable in <60 minutes.
3. **Mark provenance** — when a Hindi field is freshly authored or
   refined, update the entry's `gloss_provenance` /
   `meanings_provenance` / `explanation_provenance` from
   `machine_translated` to `native_reviewed` ONLY if you are a
   native Hindi speaker reviewing the translation in context.
4. **PR title format**: `i18n(hi): <surface> NN entries — native review`
   or `i18n(hi): <surface> NN entries — bulk authoring`.
5. **CI must pass** — `python tools/check_content_integrity.py` must
   exit 0. The `JA-13` invariant skips locale-suffixed translation
   fields automatically; the new Hindi text is fine to contain
   non-N5 kanji or other-script characters.
6. **No external services** — translations land in the repo as
   plain JSON. No Crowdin / Weblate / Lokalise integration (would
   break the privacy-first / no-third-party posture).

## L1-interference notes (Hindi-specific)

The audit prompt `prompts/LocaleTransitionEnHi.txt` enumerates the
8 mandatory L1-interference notes for Hindi-medium pedagogy:

1. **SOV word order** — shared advantage; confidence-builder.
2. **Postposition vs particle mapping** — Hindi से splits into
   Japanese から (source) + で (instrument); Hindi को splits into
   Japanese を (direct object) + に (indirect object); Hindi में
   maps to either に or で context-dependently.
3. **Verb agreement (gender + number)** — Hindi conjugates for
   gender; Japanese does not.
4. **Tense over-marking** — Hindi has more tense forms than
   Japanese; 〜ている covers both progressive AND perfect contexts.
5. **Politeness mismatch** — Hindi has 3-tier pronoun politeness
   (तू / तुम / आप); Japanese has 2-tier basic + full keigo
   morphology.
6. **Negative formation placement** — Hindi नहीं sits before the
   verb; Japanese ない attaches to the verb stem.
7. **Question particle placement** — Hindi क्या at sentence start
   vs Japanese か at sentence end.
8. **Plural marking** — Hindi marks plurals; Japanese mostly
   doesn't (人 = "person" or "people").

These notes go into `data/grammar.json` per-pattern `l1_notes.hi`
field; each pattern that involves any of the above contrasts should
carry the relevant note.

## Quality bar

- **Functional clarity over literary elegance** for the seed cycle
  (current state). A native-review pass follows.
- **Devanagari script throughout** the UI. No Romanized Hindi.
- **English loan-words** allowed for technical JLPT terminology
  where Hindi has no settled equivalent (JLPT itself, pat-test
  patterns, mondai numbers, etc.).
- **Respectful register** — match the existing English UI ("Choose
  language" not "Pick a language!").
- **Tight character budget** for vocab gloss (≤ 30 chars) and
  kanji meanings (≤ 25 chars per entry) so the UI density holds.
- **Cite source** in PR description if you used a published
  Hindi-Japanese dictionary or a specific reference pedagogy text.

## Getting started

1. Fork the repo.
2. Branch off `master` (e.g. `i18n-hi-vocab-batch-001`).
3. Edit `N5/data/vocab.json` (or other surface) to add `gloss_hi`
   on a batch of entries.
4. Run `python N5/tools/check_content_integrity.py` from the N5
   directory — must exit 0.
5. Commit, push, open PR with the title format above.
6. CI runs Playwright + integrity checks. After human review +
   CI green, the maintainer squash-merges.

## Recognition

Contributors are listed in the changelog entry that ships their
work, and (with their permission) in `CONTRIBUTORS.md` once it
exists. Privacy-first project — no email logging, no telemetry on
contributor activity beyond what GitHub itself surfaces.

## Why Hindi (and only Hindi) for non-EN locales

- **Top-5 JLPT country** — India sends ~50K applicants per year
  to JLPT, putting it 5th globally after Japan, China, South
  Korea, and Vietnam.
- **N5+N4 dominance** — 73% of Indian JLPT applicants are at
  N5 or N4 level, perfect product-market fit.
- **No dedicated Hindi-medium prep app** — App-store searches
  and curated lists in 2026-05 turned up zero results. The
  closest competitor is Yoisho Academy, which delivers in
  English with optional Hindi tutoring (and is not an app).
- **5-locale shell was diluting depth** — the previous strategy
  spread thin across vi/id/ne/zh with shallow LLM-curated
  translations; concentrating on en+hi lets us ship native-
  quality depth in the locales that matter most.

The historical 5-locale work is preserved in commit history
(`pre-locale-transition` tag at the parent of the transition
chain). It is not lost; it just no longer ships.
