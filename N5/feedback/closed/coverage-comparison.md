# Cross-coverage comparison: our 163 vs learnjapaneseaz.com 175

- Our questions:  163 total (138 mcq)
- External:       175 questions across 17 tests

## Most-tested correct-answer tokens

| Token | Ours | External | Δ (ours−ext) |
|-------|-----:|---------:|------------:|
| に | 3 | 14 | -11 |
| で | 5 | 11 | -6 |
| を | 3 | 5 | -2 |
| が | 4 | 4 | +0 |
| と | 2 | 6 | -4 |
| も | 3 | 4 | -1 |
| から | 3 | 3 | +0 |
| いつ | 4 | 1 | +3 |
| か | 4 | 1 | +3 |
| ません | 4 | 0 | +4 |
| は | 2 | 2 | +0 |
| の | 0 | 4 | -4 |
| でした | 3 | 0 | +3 |
| や | 3 | 0 | +3 |
| へ | 2 | 1 | +1 |
| なに | 2 | 1 | +1 |
| 行く | 0 | 3 | -3 |
| たべて | 2 | 1 | +1 |
| います | 1 | 1 | +0 |
| ここ | 2 | 0 | +2 |
| どう | 1 | 1 | +0 |
| まで | 2 | 0 | +2 |
| ぐらい | 1 | 1 | +0 |
| ませんでした | 2 | 0 | +2 |
| のんで | 1 | 1 | +0 |

## Tokens tested by external corpus but absent from our correct-answer set

- `の` × 4
- `行く` × 3
- `もらいました` × 2
- `ので` × 2
- `起きた` × 2
- `いたくて` × 1
- `うって` × 1
- `しめて` × 1
- `見に` × 1
- `食べていません。` × 1
- `かりた` × 1
- `ききながら` × 1
- `見た` × 1
- `しずかに` × 1
- `ひろくない` × 1
- `さむく` × 1
- `あつかった。` × 1
- `すわないで` × 1
- `スーパー` × 1
- `まっすぐ` × 1
- `もって` × 1
- `あとで` × 1
- `ゆっくり` × 1
- `かりに` × 1
- `きれいに` × 1
- `聞きながら` × 1
- `ありません` × 1
- `したり` × 1
- `あいて` × 1
- `らいしゅう` × 1

## Tokens we test that external doesn't

- `ません` × 4
- `でした` × 3
- `や` × 3
- `です` × 2
- `まで` × 2
- `これ` × 2
- `どれ` × 2
- `ここ` × 2
- `なん` × 2
- `だれ` × 2
- `ます` × 2
- `ました` × 2
- `ませんでした` × 2
- `ましょう` × 2
- `い` × 2
- `くなかった` × 2
- `この` × 1
- `あの` × 1
- `どこ` × 1
- `は ... は` × 1
- `にも` × 1
- `それ` × 1
- `のむ` × 1
- `たべる` × 1
- `のまない` × 1
- `こない` × 1
- `よんだ` × 1
- `いった` × 1
- `くない` × 1
- `おもしろくない` × 1

## Pattern coverage in our bank

- Unique pattern IDs covered: 84
- Most over-represented (top 10):
  - `n5-001` × 5
  - `n5-002` × 5
  - `n5-007` × 5
  - `n5-004` × 4
  - `n5-005` × 4
  - `n5-003` × 3
  - `n5-008` × 3
  - `n5-010` × 3
  - `n5-013` × 3
  - `n5-014` × 3
- Singletons (patterns with 1 question): 35

## Notes for downstream review

- The external corpus does not tag questions to grammar-pattern IDs, so this comparison is at the *correct-answer token* level only. A finer-grained mapping would require manually tagging each external question.
- Tokens absent from our correct-answer set may either be (a) genuine coverage gaps OR (b) variants we test under a different surface form (e.g., we test `見て` and they test `見せて`).
- Use this as a triage signal, not as a definitive gap report. Items in "external but not ours" with count ≥ 3 are the strongest candidates for new question authoring.
