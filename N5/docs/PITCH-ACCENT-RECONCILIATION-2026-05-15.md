# Pitch-Accent Reconciliation — 2026-05-15

## Methodology

Cross-referenced every vocab.json `pitch_accent.drop` value against
the kanjium pitch-accent dataset (commit `8a0cdaa16d64a281a2048de2eee2ec5e3a440fa6`,
CC-BY-SA 4.0). For each vocab entry:

- **MATCH:** current drop ∈ reference drops → `confidence: high`
- **DISAGREE:** current drop not in reference → fix to reference[0] →
  `confidence: high`, source pinned
- **NOT_FOUND:** not in reference (gairaigo, function words, compounds
  kanjium doesn't enumerate) → `confidence: unverified`, value kept as-is

## Statistics (Round 1 + Round 2)

### Round 1 — initial reconciliation
- **MATCH (no change):** 916
- **DISAGREE → fixed:** 28
- **NOT_FOUND (unverified):** 65
- **Total processed:** 1009

### Round 2 — morphological-rule promotions + `alternates` field
- **A1 (suru compounds → noun-accent rule):**   11 promoted to `medium`
- **A2 (お-prefix forms → base-noun lookup):**    6 promoted to `medium`
- **A3 (country names → katakana-toponym):**     5 promoted to `medium`
- **A4 (greeting phrases → not-in-lexicon):**   16 tagged `low`
- **B (kanjium alternates field added):**       226 entries with multi-
  drop attestation now expose `pitch_accent.alternates: [list]`

### Final confidence distribution
- **`high`:**        944 (94%) — kanjium MATCH or auto-fixed to kanjium
- **`medium`:**       22 (2%)  — morphological-rule (suru/お/country)
- **`low`:**          16 (2%)  — lexicalized greeting phrases (need
                                   native review)
- **`unverified`:**   27 (3%)  — compound expressions and particles
                                   that genuinely lack a reference

## Diff list — DISAGREE entries fixed to reference

| Vocab ID | Form | Reading | Old | New | All reference drops | Match kind |
|----------|------|---------|-----|-----|---------------------|------------|
| `n5.vocab.5-demonstratives.ああ` | ああ | ああ | 1 | **0** | 0 | exact |
| `n5.vocab.36-greetings-and-set-phr.いらっしゃいませ` | いらっしゃいませ | いらっしゃいませ | 0 | **6** | 6 | exact |
| `n5.vocab.27-verbs-group-1-verbs.おす` | おす | おす | 0 | **1** | 1 | exact |
| `n5.vocab.34-conjunctions.から` | から | から | 2 | **1** | 1 | exact |
| `n5.vocab.35-particles-functional-.から` | から | から | 2 | **1** | 1 | exact |
| `n5.vocab.34-conjunctions.けれど` | けれど | けれど | 0 | **1** | 1 | exact |
| `n5.vocab.5-demonstratives.これ` | これ | これ | 0 | **1** | 1 | exact |
| `n5.vocab.27-verbs-group-1-verbs.さす` | さす | さす | 1 | **0** | 0 | exact |
| `n5.vocab.5-demonstratives.それ` | それ | それ | 0 | **1** | 1 | exact |
| `n5.vocab.1-people-pronouns-and-se.だれ` | だれ | だれ | 1 | **2** | 2 | exact |
| `n5.vocab.35-particles-functional-.で` | で | で | 0 | **1** | 1 | exact |
| `n5.vocab.34-conjunctions.ですから` | ですから | ですから | 0 | **1** | 1 | exact |
| `n5.vocab.35-particles-functional-.ね` | ね | ね | 0 | **1** | 1 | exact |
| `n5.vocab.9-counters-common.はい` | はい | はい | 0 | **1** | 1 | exact |
| `n5.vocab.39-function-filler-expre.はい` | はい | はい | 0 | **1** | 1 | exact |
| `n5.vocab.35-particles-functional-.も` | も | も | 0 | **1** | 1 | exact |
| `n5.vocab.26-house-and-furniture.エレベーター` | エレベーター | エレベーター | 4 | **3** | 3 | exact |
| `n5.vocab.17-food-items.キャベツ` | キャベツ | キャベツ | 0 | **1** | 1 | exact |
| `n5.vocab.17-food-items.サラダ` | サラダ | サラダ | 0 | **1** | 1 | exact |
| `n5.vocab.37-common-nouns-miscella.ストーブ` | ストーブ | ストーブ | 0 | **2** | 2 | exact |
| `n5.vocab.19-tableware-and-cooking.スプーン` | スプーン | スプーン | 1 | **2** | 2 | exact |
| `n5.vocab.37-common-nouns-miscella.スリッパ` | スリッパ | スリッパ | 0 | **1** | 1,2 | exact |
| `n5.vocab.7-numbers.ゼロ` | ゼロ | ゼロ | 0 | **1** | 1 | exact |
| `n5.vocab.17-food-items.トマト` | トマト | トマト | 0 | **1** | 1 | exact |
| `n5.vocab.17-food-items.バター` | バター | バター | 0 | **1** | 1 | exact |
| `n5.vocab.13-locations-and-places-.フロント` | フロント | フロント | 1 | **0** | 0 | exact |
| `n5.vocab.26-house-and-furniture.ラジオ` | ラジオ | ラジオ | 0 | **1** | 1 | exact |
| `n5.vocab.37-common-nouns-miscella.レコード` | レコード | レコード | 0 | **2** | 2 | exact |

## Sample of NOT_FOUND (`confidence: unverified`) entries

These are predominantly gairaigo (loanwords), compound expressions,
and function-word entries not in the kanjium upstream. Their
`pitch_accent.drop` values are kept as-is from LLM authoring and
should be flagged for future native-human review.

| Vocab ID | Form | Reading | Drop (kept) |
|----------|------|---------|-------------|
| `n5.vocab.7-numbers.一万` | 一万 | いちまん | 3 |
| `n5.vocab.12-time-frequency-sequen.もうすぐ` | もうすぐ | もうすぐ | 0 |
| `n5.vocab.12-time-frequency-sequen.後で` | 後で | あとで | 1 |
| `n5.vocab.13-locations-and-places-.お店` | お店 | おみせ | 0 |
| `n5.vocab.17-food-items.じゃがいも` | じゃがいも | じゃがいも | 0 |
| `n5.vocab.18-drinks.おさけ` | おさけ | おさけ | 0 |
| `n5.vocab.19-tableware-and-cooking.おさら` | おさら | おさら | 0 |
| `n5.vocab.19-tableware-and-cooking.おわん` | おわん | おわん | 0 |
| `n5.vocab.21-clothing-and-accessor.ワイシャツ` | ワイシャツ | ワイシャツ | 0 |
| `n5.vocab.24-school-and-study.カタカナ` | カタカナ | カタカナ | 3 |
| `n5.vocab.25-languages-and-countri.アメリカ` | アメリカ | アメリカ | 0 |
| `n5.vocab.25-languages-and-countri.フランス` | フランス | フランス | 0 |
| `n5.vocab.25-languages-and-countri.ドイツ` | ドイツ | ドイツ | 1 |
| `n5.vocab.25-languages-and-countri.スペイン` | スペイン | スペイン | 2 |
| `n5.vocab.25-languages-and-countri.イギリス` | イギリス | イギリス | 0 |
| `n5.vocab.27-verbs-group-1-verbs.もっていく` | もっていく | もっていく | 4 |
| `n5.vocab.29-verbs-irregular-and-v.べんきょうする` | べんきょうする | べんきょうする | 0 |
| `n5.vocab.29-verbs-irregular-and-v.けっこんする` | けっこんする | けっこんする | 0 |
| `n5.vocab.29-verbs-irregular-and-v.さんぽする` | さんぽする | さんぽする | 0 |
| `n5.vocab.29-verbs-irregular-and-v.りょこうする` | りょこうする | りょこうする | 0 |
| `n5.vocab.29-verbs-irregular-and-v.れんしゅうする` | れんしゅうする | れんしゅうする | 0 |
| `n5.vocab.29-verbs-irregular-and-v.しつもんする` | しつもんする | しつもんする | 0 |
| `n5.vocab.29-verbs-irregular-and-v.しごとする` | しごとする | しごとする | 1 |
| `n5.vocab.29-verbs-irregular-and-v.電話する` | 電話する | でんわする | 0 |
| `n5.vocab.29-verbs-irregular-and-v.コピーする` | コピーする | コピーする | 1 |
| `n5.vocab.29-verbs-irregular-and-v.そうじする` | そうじする | そうじする | 0 |
| `n5.vocab.29-verbs-irregular-and-v.せんたくする` | せんたくする | せんたくする | 0 |
| `n5.vocab.29-verbs-irregular-and-v.かいものする` | かいものする | かいものする | 0 |
| `n5.vocab.33-adverbs.いっしょに` | いっしょに | いっしょに | 0 |
| `n5.vocab.33-adverbs.一人で` | 一人で | ひとりで | 2 |
| ... | ... | ... | (+35 more) |

## Caveats

- **Source authority:** kanjium aggregates from EDICT/EDRDG and NHK
  日本語発音アクセント新辞典. Some words have multiple attested drops
  (e.g., 0 OR 2); the reference's `drops` array lists all and we
  accept any as MATCH.
- **Tokyo dialect bias:** kanjium reflects standard Tokyo pronunciation;
  Kansai/Kyushu accent patterns differ entirely.
- **Reading-only matches (`match_kind: by-reading`):** these used the
  reading-only fallback because our vocab uses kana-only forms for
  many words where kanjium has the kanji form. The drop set is the
  UNION of all kanjium entries with that reading — wider but less
  precise. JA-90 treats both `exact` and `by-reading` as valid
  high-confidence sources.
- **NOT_FOUND entries:** ~18% of vocab — kept as `unverified`. Future
  native-human review pass should prioritize these.

## Locked by

CI invariant **JA-90** validates that every vocab `pitch_accent.drop`
agrees with the reference (or has `confidence: unverified` set).

