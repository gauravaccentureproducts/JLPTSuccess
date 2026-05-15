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

## Statistics

- **MATCH (no change):** 810
- **DISAGREE → fixed:** 22
- **NOT_FOUND (unverified):** 177
- **Total processed:** 1009

Reference coverage: 82% of vocab entries
have a kanjium-derived high-confidence value. Remaining
17% are mostly loanwords (gairaigo) and function-word
phrases not in the kanjium upstream.

## Diff list — DISAGREE entries fixed to reference

| Vocab ID | Form | Reading | Old | New | All reference drops | Match kind |
|----------|------|---------|-----|-----|---------------------|------------|
| `n5.vocab.10-time-general.あした` | あした | あした | 0 | **3** | 3 | by-reading |
| `n5.vocab.1-people-pronouns-and-se.あなた` | あなた | あなた | 0 | **2** | 2,1 | by-reading |
| `n5.vocab.30-verbs-existence-and-p.ある` | ある | ある | 2 | **1** | 1 | by-reading |
| `n5.vocab.15-animals.うし` | うし | うし | 2 | **0** | 0,1 | by-reading |
| `n5.vocab.10-time-general.おととい` | おととい | おととい | 0 | **3** | 3 | by-reading |
| `n5.vocab.35-particles-functional-.ぐらい` | ぐらい | ぐらい | 1 | **0** | 0 | by-reading |
| `n5.vocab.36-greetings-and-set-phr.こんばんは` | こんばんは | こんばんは | 0 | **5** | 5 | by-reading |
| `n5.vocab.30-verbs-existence-and-p.ござる` | ござる | ござる | 1 | **2** | 2 | by-reading |
| `n5.vocab.39-function-filler-expre.じゃあ` | じゃあ | じゃあ | 1 | **2** | 2 | by-reading |
| `n5.vocab.13-locations-and-places-.とおく` | とおく | とおく | 1 | **3** | 3,0 | by-reading |
| `n5.vocab.27-verbs-group-1-verbs.はじまる` | はじまる | はじまる | 4 | **0** | 0 | by-reading |
| `n5.vocab.15-animals.ぶた` | ぶた | ぶた | 2 | **0** | 0 | by-reading |
| `n5.vocab.13-locations-and-places-.へや` | へや | へや | 0 | **2** | 2 | by-reading |
| `n5.vocab.2-people-family.りょうしん` | りょうしん | りょうしん | 3 | **1** | 1 | by-reading |
| `n5.vocab.11-time-days-weeks-month.二月` | 二月 | にがつ | 0 | **3** | 3 | exact |
| `n5.vocab.11-time-days-weeks-month.五月` | 五月 | ごがつ | 0 | **1** | 1 | exact |
| `n5.vocab.11-time-days-weeks-month.四月` | 四月 | しがつ | 0 | **3** | 3 | exact |
| `n5.vocab.11-time-days-weeks-month.年` | 年 | とし | 1 | **2** | 2 | exact |
| `n5.vocab.11-time-days-weeks-month.日` | 日 | ひ | 1 | **0** | 0 | exact |
| `n5.vocab.12-time-frequency-sequen.時々` | 時々 | ときどき | 4 | **0** | 0,2 | exact |
| `n5.vocab.11-time-days-weeks-month.毎年` | 毎年 | まいとし | 1 | **0** | 0 | exact |
| `n5.vocab.28-verbs-group-2-verbs.見せる` | 見せる | みせる | 0 | **2** | 2 | exact |

## Sample of NOT_FOUND (`confidence: unverified`) entries

These are predominantly gairaigo (loanwords), compound expressions,
and function-word entries not in the kanjium upstream. Their
`pitch_accent.drop` values are kept as-is from LLM authoring and
should be flagged for future native-human review.

| Vocab ID | Form | Reading | Drop (kept) |
|----------|------|---------|-------------|
| `n5.vocab.5-demonstratives.こんな` | こんな | こんな | 0 |
| `n5.vocab.5-demonstratives.そんな` | そんな | そんな | 0 |
| `n5.vocab.5-demonstratives.あんな` | あんな | あんな | 0 |
| `n5.vocab.5-demonstratives.どんな` | どんな | どんな | 1 |
| `n5.vocab.7-numbers.一万` | 一万 | いちまん | 3 |
| `n5.vocab.12-time-frequency-sequen.もうすぐ` | もうすぐ | もうすぐ | 0 |
| `n5.vocab.12-time-frequency-sequen.後で` | 後で | あとで | 1 |
| `n5.vocab.13-locations-and-places-.トイレ` | トイレ | トイレ | 1 |
| `n5.vocab.13-locations-and-places-.お店` | お店 | おみせ | 0 |
| `n5.vocab.13-locations-and-places-.スーパー` | スーパー | スーパー | 1 |
| `n5.vocab.13-locations-and-places-.デパート` | デパート | デパート | 2 |
| `n5.vocab.13-locations-and-places-.レストラン` | レストラン | レストラン | 1 |
| `n5.vocab.13-locations-and-places-.ホテル` | ホテル | ホテル | 1 |
| `n5.vocab.13-locations-and-places-.プール` | プール | プール | 1 |
| `n5.vocab.13-locations-and-places-.ポスト` | ポスト | ポスト | 1 |
| `n5.vocab.17-food-items.パン` | パン | パン | 1 |
| `n5.vocab.17-food-items.バナナ` | バナナ | バナナ | 1 |
| `n5.vocab.17-food-items.レモン` | レモン | レモン | 0 |
| `n5.vocab.17-food-items.じゃがいも` | じゃがいも | じゃがいも | 0 |
| `n5.vocab.17-food-items.トマト` | トマト | トマト | 0 |
| `n5.vocab.17-food-items.キャベツ` | キャベツ | キャベツ | 0 |
| `n5.vocab.17-food-items.バター` | バター | バター | 0 |
| `n5.vocab.17-food-items.チーズ` | チーズ | チーズ | 1 |
| `n5.vocab.17-food-items.カレー` | カレー | カレー | 0 |
| `n5.vocab.17-food-items.ハンバーガー` | ハンバーガー | ハンバーガー | 3 |
| `n5.vocab.17-food-items.サンドイッチ` | サンドイッチ | サンドイッチ | 4 |
| `n5.vocab.17-food-items.サラダ` | サラダ | サラダ | 0 |
| `n5.vocab.17-food-items.スープ` | スープ | スープ | 1 |
| `n5.vocab.17-food-items.ケーキ` | ケーキ | ケーキ | 1 |
| `n5.vocab.17-food-items.アイスクリーム` | アイスクリーム | アイスクリーム | 5 |
| ... | ... | ... | (+147 more) |

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

