# Translating JLPTSuccess (IMP-056)

Native speakers / language teachers / serious learners willing to
contribute translations are the unblocker for the project's primary
strategic niche (multilingual non-English-native JLPT N5 candidates —
see audit-tracker `Q13`). This doc is the on-ramp.

## What needs translating

The app ships two parallel translation surfaces:

### Surface A — UI chrome (locales/<lc>.json)

75 keys per locale covering navigation labels, button text, settings
labels, etc. Currently:

| Locale | UI keys translated |
|---|---|
| en (source) | 75 / 75 |
| vi | 33 / 75 |
| id | 33 / 75 |
| ne | 33 / 75 |
| zh | 33 / 75 |

Filling vi/id/ne/zh from 33 to 75 closes the round-4 audit's
**ISSUE-026** UI-coverage gap.

### Surface B — content body (data/*.json)

The actual lessons. Per-locale fields in each item:

- `data/grammar.json` — `explanation_en`, `meaning_en`, `notes`,
  `common_mistakes[*].why` × 178 patterns.
- `data/vocab.json` — `gloss` × 1041 entries.
- `data/kanji.json` — `meanings[]` × 106 kanji.
- `data/reading.json` — `explanation_en` × ~84 reading questions
  (most are quoted-JA passage pointers — see audit-tracker IMP-019).
- `data/listening.json` — `explanation_en` × 40 items.

Total: ~1325 unique strings × 4 locales = ~5300 strings to fill the
content body across vi/id/ne/zh.

This is the **IMP-045 / IMP-046 / IMP-047** workload.

## How to contribute

### Quick translation (UI chrome only)

1. Fork the repo.
2. Open `N5/locales/<lc>.json` for your locale (pick from
   vi / id / ne / zh, or add a new one — see `SELF-HOST.md`).
3. Each key in `en.json` should appear in your locale file. Copy the
   English value, replace with the native translation.
4. PR titled `i18n(<lc>): translate <surface> keys (NN/75 -> MM/75)`.

### Content translation (lesson body)

The schema does NOT yet have `explanation_vi`, `gloss_vi`,
`meanings_vi` etc. fields — adding those is the IMP-045/046/047
infrastructure work.

When that infrastructure lands (tracked by audit IDs above),
translation flow will be:

1. Pick a single corpus surface to start with (recommend `vocab.json`
   glosses — easiest, shortest strings, biggest learner impact).
2. For each entry, add the per-locale field alongside the English
   field:
   ```json
   { "form": "学校", "reading": "がっこう",
     "gloss":    "school",
     "gloss_vi": "trường học",
     "gloss_id": "sekolah" }
   ```
3. PR titled `content(<lc>): translate <surface> (NN/total -> MM/total)`.

## Quality bar

- **Native review preferred.** Machine-translated drafts are useful
  but should be reviewed by a native speaker before merging.
- **JLPT-context appropriate.** "School" in `gloss_vi` should be the
  word a Vietnamese learner would actually use for 学校 in a Japanese
  textbook — not a regional dialect form.
- **Kept short.** Keep glosses to ≤ 30 characters where possible to
  not overflow the existing UI rows.
- **No machine-translation marker drift.** If a string is auto-
  generated, mark it `_provenance: "machine-translated"` so the
  reviewer pass can find it. Native-reviewed strings drop the marker.

## Provenance tagging (ISSUE-030)

Once the round-4 ISSUE-030 provenance schema lands, every translated
string ships with a `review_status` tag:

- `native_reviewed` — reviewed by a native speaker, with attribution.
- `llm_curated` — AI-drafted, sanity-checked by a contributor.
- `machine_translated` — auto-translated, no human review yet.

Honest labeling is critical for trust — the audit is explicit that
items shouldn't all "look the same to the learner" when quality
varies.

## ⭐ Reviewers wanted (Q20: actively recruiting, 2026-05-05)

The 4 non-English locales currently ship as **machine-translated** —
the round-4 close-out got UI strings from 44% to 100%+ coverage but
no native speaker has signed off yet. Round-5 audit Q20 resolved as
"actively recruit per-locale reviewers."

**The fastest way to upgrade a single locale from machine-translated
to native-reviewed:**

1. Read your locale's JSON file (`locales/vi.json` / `id.json` /
   `ne.json` / `zh.json`).
2. The `_meta.provenance` field at the top says `machine_translated`
   today.
3. Skim the 75 UI strings; fix anything that reads unnaturally or
   mistranslates JLPT terminology.
4. Open a PR titled `i18n(<lc>): native review pass — N keys
   touched`.
5. In the PR, set `_meta.provenance: "native_reviewed"` and add a
   `_meta.reviewer: "<your-name>"` line with your name or GitHub
   handle so the credit lands in `N5/NOTICES.md`.

| Locale | Native speaker review status |
|---|---|
| Vietnamese (vi) | ❌ machine-translated · reviewer needed |
| Indonesian (id) | ❌ machine-translated · reviewer needed |
| Nepali (ne) | ❌ machine-translated · reviewer needed |
| Chinese (zh) | ❌ machine-translated · reviewer needed |

**If you can review one of the 4 locales above:**

- Open a GitHub issue titled `[i18n] Available to review <locale>
  translations` — we will tag your PR for fast-track review.
- Or just submit the PR directly using the workflow above.

This recruitment is a niche-N1 unblocker: Vietnamese / Indonesian /
Nepali / Chinese JLPT-N5 candidates are millions of learners
currently under-served by EN-only apps (Bunpou / WaniKani /
Renshuu / JLPT Sensei). Native review of even the 75-key UI moves
the multilingual claim from "infrastructure exists" to "credibly
reviewed" without translating the full 5000-string content body.

## Alternative: machine-translation seed pass

If a native reviewer is not available for a locale, a community
contributor can do an initial machine-translation pass via DeepL /
Google Translate / Claude / etc., land it as a PR with EVERY string
tagged `review_status: "machine_translated"`, and explicitly mark the
PR as "needs native review before merge".

This is a viable starting point if waiting for native reviewers is
blocking the multilingual niche claim — see audit-tracker `Q14`.

## Acknowledgements

Translators and reviewers are credited in `N5/NOTICES.md` per locale.
Contributions are licensed CC BY-SA 4.0 (matching the rest of the
content corpus).
