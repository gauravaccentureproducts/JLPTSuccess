# N5 Vocabulary — Native-Review Open-Items Findings Report

Generated: 2026-06-04 (batch I).  
Purpose: surface mechanical-heuristic candidates for the 6 OPEN items the human native reviewer needs to close.

This file is **not** a list of confirmed bugs. It is a list of entries the heuristics flagged for human attention. A native reviewer should look at each, decide KEEP / REWRITE / DELETE, and apply the change directly to the corpus.

---

## OPEN-003 / OPEN-004 — particle_examples candidates (589 entries)

Heuristic: entries whose `particle_examples` contain the reviewer's named template shapes (`を しる`, `を する`, `に いく`, `と あう`, `を ならう`) OR have 3+ examples sharing the same 3-character tail (template-generation signal).

### 私 (`n5.vocab.1-people-pronouns-and-se.私`)
reading: `わたし`  
current particle_examples: `['わたしの ともだち', 'わたしの なまえ', 'わたしは がくせい', 'わたしも いく', 'わたしを しる', 'わたしと あう']`

- template-shape hits:
  - shape `を しる` in `わたしを しる`
  - shape `と あう` in `わたしと あう`

### 私たち (`n5.vocab.1-people-pronouns-and-se.私たち`)
reading: `わたしたち`  
current particle_examples: `['わたしたちの ともだち', 'わたしたちの なまえ', 'わたしたちは がくせい', 'わたしたちも いく', 'わたしたちを しる', 'わたしたちと あう']`

- template-shape hits:
  - shape `を しる` in `わたしたちを しる`
  - shape `と あう` in `わたしたちと あう`

### あなた (`n5.vocab.1-people-pronouns-and-se.あなた`)
current particle_examples: `['あなたの ともだち', 'あなたの なまえ', 'あなたは がくせい', 'あなたも いく', 'あなたを しる', 'あなたと あう']`

- template-shape hits:
  - shape `を しる` in `あなたを しる`
  - shape `と あう` in `あなたと あう`

### かれ (`n5.vocab.1-people-pronouns-and-se.かれ`)
current particle_examples: `['かれの ともだち', 'かれの なまえ', 'かれは がくせい', 'かれも いく', 'かれを しる', 'かれと あう']`

- template-shape hits:
  - shape `を しる` in `かれを しる`
  - shape `と あう` in `かれと あう`

### かのじょ (`n5.vocab.1-people-pronouns-and-se.かのじょ`)
current particle_examples: `['かのじょの ともだち', 'かのじょの なまえ', 'かのじょは がくせい', 'かのじょも いく', 'かのじょを しる', 'かのじょと あう']`

- template-shape hits:
  - shape `を しる` in `かのじょを しる`
  - shape `と あう` in `かのじょと あう`

### 人 (`n5.vocab.1-people-pronouns-and-se.人`)
reading: `ひと`  
current particle_examples: `['人と あう', '人と はなす', '人に きく', '人は どこ', '人の なまえ', '人が くる', '人が いる', '人は やさしい']`

- template-shape hits:
  - shape `と あう` in `人と あう`

### だれ (`n5.vocab.1-people-pronouns-and-se.だれ`)
current particle_examples: `['だれですか', 'だれが いい', 'だれを しますか', 'だれに いきますか', 'だれと あいますか', 'だれの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['だれを しますか', 'だれに いきますか', 'だれと あいますか']`

### どなた (`n5.vocab.1-people-pronouns-and-se.どなた`)
current particle_examples: `['どなたですか', 'どなたが いい', 'どなたを しますか', 'どなたに いきますか', 'どなたと あいますか', 'どなたの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['どなたを しますか', 'どなたに いきますか', 'どなたと あいますか']`

### じぶん (`n5.vocab.1-people-pronouns-and-se.じぶん`)
current particle_examples: `['じぶんの ともだち', 'じぶんの なまえ', 'じぶんは がくせい', 'じぶんも いく', 'じぶんを しる', 'じぶんと あう']`

- template-shape hits:
  - shape `を しる` in `じぶんを しる`
  - shape `と あう` in `じぶんと あう`

### かぞく (`n5.vocab.2-people-family.かぞく`)
current particle_examples: `['かぞくと あう', 'かぞくと はなす', 'かぞくに きく', 'かぞくは どこ', 'かぞくの なまえ', 'かぞくが くる', 'かぞくが いる', 'かぞくは やさしい']`

- template-shape hits:
  - shape `と あう` in `かぞくと あう`

### 父 (`n5.vocab.2-people-family.父`)
reading: `ちち`  
current particle_examples: `['父と あう', '父と はなす', '父に きく', '父は どこ', '父の なまえ', '父が くる', '父が いる', '父は やさしい']`

- template-shape hits:
  - shape `と あう` in `父と あう`

### 母 (`n5.vocab.2-people-family.母`)
reading: `はは`  
current particle_examples: `['母と あう', '母と はなす', '母に きく', '母は どこ', '母の なまえ', '母が くる', '母が いる', '母は やさしい']`

- template-shape hits:
  - shape `と あう` in `母と あう`

### あに (`n5.vocab.2-people-family.あに`)
current particle_examples: `['あにと あう', 'あにと はなす', 'あにに きく', 'あには どこ', 'あにの なまえ', 'あにが くる', 'あにが いる', 'あには やさしい']`

- template-shape hits:
  - shape `と あう` in `あにと あう`

### あね (`n5.vocab.2-people-family.あね`)
current particle_examples: `['あねと あう', 'あねと はなす', 'あねに きく', 'あねは どこ', 'あねの なまえ', 'あねが くる', 'あねが いる', 'あねは やさしい']`

- template-shape hits:
  - shape `と あう` in `あねと あう`

### おとうと (`n5.vocab.2-people-family.おとうと`)
current particle_examples: `['おとうとと あう', 'おとうとと はなす', 'おとうとに きく', 'おとうとは どこ', 'おとうとの なまえ', 'おとうとが くる', 'おとうとが いる', 'おとうとは やさしい']`

- template-shape hits:
  - shape `と あう` in `おとうとと あう`

### いもうと (`n5.vocab.2-people-family.いもうと`)
current particle_examples: `['いもうとと あう', 'いもうとと はなす', 'いもうとに きく', 'いもうとは どこ', 'いもうとの なまえ', 'いもうとが くる', 'いもうとが いる', 'いもうとは やさしい']`

- template-shape hits:
  - shape `と あう` in `いもうとと あう`

### おにいさん (`n5.vocab.2-people-family.おにいさん`)
current particle_examples: `['おにいさんと あう', 'おにいさんと はなす', 'おにいさんに きく', 'おにいさんは どこ', 'おにいさんの なまえ', 'おにいさんが くる', 'おにいさんが いる', 'おにいさんは やさしい']`

- template-shape hits:
  - shape `と あう` in `おにいさんと あう`

### おねえさん (`n5.vocab.2-people-family.おねえさん`)
current particle_examples: `['おねえさんと あう', 'おねえさんと はなす', 'おねえさんに きく', 'おねえさんは どこ', 'おねえさんの なまえ', 'おねえさんが くる', 'おねえさんが いる', 'おねえさんは やさしい']`

- template-shape hits:
  - shape `と あう` in `おねえさんと あう`

### きょうだい (`n5.vocab.2-people-family.きょうだい`)
current particle_examples: `['きょうだいと あう', 'きょうだいと はなす', 'きょうだいに きく', 'きょうだいは どこ', 'きょうだいの なまえ', 'きょうだいが くる', 'きょうだいが いる', 'きょうだいは やさしい']`

- template-shape hits:
  - shape `と あう` in `きょうだいと あう`

### りょうしん (`n5.vocab.2-people-family.りょうしん`)
current particle_examples: `['りょうしんと あう', 'りょうしんと はなす', 'りょうしんに きく', 'りょうしんは どこ', 'りょうしんの なまえ', 'りょうしんが くる', 'りょうしんが いる', 'りょうしんは やさしい']`

- template-shape hits:
  - shape `と あう` in `りょうしんと あう`

### そふ (`n5.vocab.2-people-family.そふ`)
current particle_examples: `['そふと あう', 'そふと はなす', 'そふに きく', 'そふは どこ', 'そふの なまえ', 'そふが くる', 'そふが いる', 'そふは やさしい']`

- template-shape hits:
  - shape `と あう` in `そふと あう`

### そぼ (`n5.vocab.2-people-family.そぼ`)
current particle_examples: `['そぼと あう', 'そぼと はなす', 'そぼに きく', 'そぼは どこ', 'そぼの なまえ', 'そぼが くる', 'そぼが いる', 'そぼは やさしい']`

- template-shape hits:
  - shape `と あう` in `そぼと あう`

### おじいさん (`n5.vocab.2-people-family.おじいさん`)
current particle_examples: `['おじいさんと あう', 'おじいさんと はなす', 'おじいさんに きく', 'おじいさんは どこ', 'おじいさんの なまえ', 'おじいさんが くる', 'おじいさんが いる', 'おじいさんは やさしい']`

- template-shape hits:
  - shape `と あう` in `おじいさんと あう`

### おばあさん (`n5.vocab.2-people-family.おばあさん`)
current particle_examples: `['おばあさんと あう', 'おばあさんと はなす', 'おばあさんに きく', 'おばあさんは どこ', 'おばあさんの なまえ', 'おばあさんが くる', 'おばあさんが いる', 'おばあさんは やさしい']`

- template-shape hits:
  - shape `と あう` in `おばあさんと あう`

### 男 (`n5.vocab.2-people-family.男`)
reading: `おとこ`  
current particle_examples: `['男と あう', '男と はなす', '男に きく', '男は どこ', '男の なまえ', '男が くる', '男が いる', '男は やさしい']`

- template-shape hits:
  - shape `と あう` in `男と あう`

### 女 (`n5.vocab.2-people-family.女`)
reading: `おんな`  
current particle_examples: `['女と あう', '女と はなす', '女に きく', '女は どこ', '女の なまえ', '女が くる', '女が いる', '女は やさしい']`

- template-shape hits:
  - shape `と あう` in `女と あう`

### 友だち (`n5.vocab.2-people-family.ともだち`)
reading: `ともだち`  
current particle_examples: `['ともだちと あう', 'ともだちと はなす', 'ともだちに きく', 'ともだちは どこ', 'ともだちの なまえ', 'ともだちが くる', 'ともだちが いる', 'ともだちは やさしい']`

- template-shape hits:
  - shape `と あう` in `ともだちと あう`

### せいと (`n5.vocab.3-people-roles.せいと`)
current particle_examples: `['せいとと あう', 'せいとと はなす', 'せいとに きく', 'せいとは どこ', 'せいとの なまえ', 'せいとが くる', 'せいとが いる', 'せいとは やさしい']`

- template-shape hits:
  - shape `と あう` in `せいとと あう`

### いしゃ (`n5.vocab.3-people-roles.いしゃ`)
current particle_examples: `['いしゃと あう', 'いしゃと はなす', 'いしゃに きく', 'いしゃは どこ', 'いしゃの なまえ', 'いしゃが くる', 'いしゃが いる', 'いしゃは やさしい']`

- template-shape hits:
  - shape `と あう` in `いしゃと あう`

### 会社員 (`n5.vocab.3-people-roles.会社員`)
reading: `かいしゃいん`  
current particle_examples: `['会社員に いく', '会社員で あう', '会社員から くる', '会社員の まえに', '会社員が ある', '会社員は ちかい', '会社員まで あるく', '会社員に つく']`

- template-shape hits:
  - shape `に いく` in `会社員に いく`

### 駅員 (`n5.vocab.3-people-roles.駅員`)
reading: `えきいん`  
current particle_examples: `['駅員と あう', '駅員と はなす', '駅員に きく', '駅員は どこ', '駅員の なまえ', '駅員が くる', '駅員が いる', '駅員は やさしい']`

- template-shape hits:
  - shape `と あう` in `駅員と あう`

### けいかん (`n5.vocab.3-people-roles.けいかん`)
current particle_examples: `['けいかんと あう', 'けいかんと はなす', 'けいかんに きく', 'けいかんは どこ', 'けいかんの なまえ', 'けいかんが くる', 'けいかんが いる', 'けいかんは やさしい']`

- template-shape hits:
  - shape `と あう` in `けいかんと あう`

### おまわりさん (`n5.vocab.3-people-roles.おまわりさん`)
current particle_examples: `['おまわりさんと あう', 'おまわりさんと はなす', 'おまわりさんに きく', 'おまわりさんは どこ', 'おまわりさんの なまえ', 'おまわりさんが くる', 'おまわりさんが いる', 'おまわりさんは やさしい']`

- template-shape hits:
  - shape `と あう` in `おまわりさんと あう`

### りゅうがくせい (`n5.vocab.3-people-roles.りゅうがくせい`)
current particle_examples: `['りゅうがくせいと あう', 'りゅうがくせいと はなす', 'りゅうがくせいに きく', 'りゅうがくせいは どこ', 'りゅうがくせいの なまえ', 'りゅうがくせいが くる', 'りゅうがくせいが いる', 'りゅうがくせいは やさしい']`

- template-shape hits:
  - shape `と あう` in `りゅうがくせいと あう`

### 外国人 (`n5.vocab.3-people-roles.外国人`)
reading: `がいこくじん`  
current particle_examples: `['外国人と あう', '外国人と はなす', '外国人に きく', '外国人は どこ', '外国人の なまえ', '外国人が くる', '外国人が いる', '外国人は やさしい']`

- template-shape hits:
  - shape `と あう` in `外国人と あう`

### 何 (`n5.vocab.6-question-words.何`)
reading: `なに`  
current particle_examples: `['なに / なんですか', 'なに / なんが いい', 'なに / なんを しますか', 'なに / なんに いきますか', 'なに / なんと あいますか', 'なに / なんの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['なに / なんを しますか', 'なに / なんに いきますか', 'なに / なんと あいますか']`

### いつ (`n5.vocab.6-question-words.いつ`)
current particle_examples: `['いつですか', 'いつが いい', 'いつを しますか', 'いつに いきますか', 'いつと あいますか', 'いつの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['いつを しますか', 'いつに いきますか', 'いつと あいますか']`

### いくら (`n5.vocab.6-question-words.いくら`)
current particle_examples: `['いくらですか', 'いくらが いい', 'いくらを しますか', 'いくらに いきますか', 'いくらと あいますか', 'いくらの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['いくらを しますか', 'いくらに いきますか', 'いくらと あいますか']`

### いくつ (`n5.vocab.6-question-words.いくつ`)
current particle_examples: `['いくつですか', 'いくつが いい', 'いくつを しますか', 'いくつに いきますか', 'いくつと あいますか', 'いくつの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['いくつを しますか', 'いくつに いきますか', 'いくつと あいますか']`

### 何時 (`n5.vocab.6-question-words.何時`)
reading: `なんじ`  
current particle_examples: `['なんじですか', 'なんじが いい', 'なんじを しますか', 'なんじに いきますか', 'なんじと あいますか', 'なんじの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['なんじを しますか', 'なんじに いきますか', 'なんじと あいますか']`

### 何曜日 (`n5.vocab.6-question-words.何曜日`)
reading: `なんようび`  
current particle_examples: `['なんようびですか', 'なんようびが いい', 'なんようびを しますか', 'なんようびに いきますか', 'なんようびと あいますか', 'なんようびの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['なんようびを しますか', 'なんようびに いきますか', 'なんようびと あいますか']`

### 何月 (`n5.vocab.6-question-words.何月`)
reading: `なんがつ`  
current particle_examples: `['なんがつですか', 'なんがつが いい', 'なんがつを しますか', 'なんがつに いきますか', 'なんがつと あいますか', 'なんがつの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['なんがつを しますか', 'なんがつに いきますか', 'なんがつと あいますか']`

### 何日 (`n5.vocab.6-question-words.何日`)
reading: `なんにち`  
current particle_examples: `['なんにちですか', 'なんにちが いい', 'なんにちを しますか', 'なんにちに いきますか', 'なんにちと あいますか', 'なんにちの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['なんにちを しますか', 'なんにちに いきますか', 'なんにちと あいますか']`

### なぜ (`n5.vocab.6-question-words.なぜ`)
current particle_examples: `['なぜですか', 'なぜが いい', 'なぜを しますか', 'なぜに いきますか', 'なぜと あいますか', 'なぜの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['なぜを しますか', 'なぜに いきますか', 'なぜと あいますか']`

### どうして (`n5.vocab.6-question-words.どうして`)
current particle_examples: `['どうしてですか', 'どうしてが いい', 'どうしてを しますか', 'どうしてに いきますか', 'どうしてと あいますか', 'どうしての なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['どうしてを しますか', 'どうしてに いきますか', 'どうしてと あいますか']`

### 何で (`n5.vocab.6-question-words.何で`)
reading: `なんで`  
current particle_examples: `['なんでですか', 'なんでが いい', 'なんでを しますか', 'なんでに いきますか', 'なんでと あいますか', 'なんでの なまえ']`

- shared-tail signal (template-generation):
  - tail `ますか`: `['なんでを しますか', 'なんでに いきますか', 'なんでと あいますか']`

### おく (`n5.vocab.7-numbers.おく`)
current particle_examples: `['本を置く', 'かばんを置く', 'テーブルに置く', 'つくえに おく', 'すぐに おく', 'いえに おく', 'たいせつな ものを おく', 'はこに おく', 'もとの ところに おく']`

- shared-tail signal (template-generation):
  - tail ` おく`: `['つくえに おく', 'すぐに おく', 'いえに おく', 'たいせつな ものを おく', 'はこに おく', 'もとの ところに おく']`

### 一つ (`n5.vocab.8-native-counters-series.一つ`)
reading: `ひとつ`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 一つ', 'たくさんの 一つ', 'ひとり 一つ']`

- shared-tail signal (template-generation):
  - tail ` 一つ`: `['ぜんぶで 一つ', 'たくさんの 一つ', 'ひとり 一つ']`

### 二つ (`n5.vocab.8-native-counters-series.二つ`)
reading: `ふたつ`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 二つ', 'たくさんの 二つ', 'ひとり 二つ']`

- shared-tail signal (template-generation):
  - tail ` 二つ`: `['ぜんぶで 二つ', 'たくさんの 二つ', 'ひとり 二つ']`

### 三つ (`n5.vocab.8-native-counters-series.三つ`)
reading: `みっつ`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 三つ', 'たくさんの 三つ', 'ひとり 三つ']`

- shared-tail signal (template-generation):
  - tail ` 三つ`: `['ぜんぶで 三つ', 'たくさんの 三つ', 'ひとり 三つ']`

### 四つ (`n5.vocab.8-native-counters-series.四つ`)
reading: `よっつ`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 四つ', 'たくさんの 四つ', 'ひとり 四つ']`

- shared-tail signal (template-generation):
  - tail ` 四つ`: `['ぜんぶで 四つ', 'たくさんの 四つ', 'ひとり 四つ']`

### 五つ (`n5.vocab.8-native-counters-series.五つ`)
reading: `いつつ`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 五つ', 'たくさんの 五つ', 'ひとり 五つ']`

- shared-tail signal (template-generation):
  - tail ` 五つ`: `['ぜんぶで 五つ', 'たくさんの 五つ', 'ひとり 五つ']`

### 六つ (`n5.vocab.8-native-counters-series.六つ`)
reading: `むっつ`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 六つ', 'たくさんの 六つ', 'ひとり 六つ']`

- shared-tail signal (template-generation):
  - tail ` 六つ`: `['ぜんぶで 六つ', 'たくさんの 六つ', 'ひとり 六つ']`

### 七つ (`n5.vocab.8-native-counters-series.七つ`)
reading: `ななつ`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 七つ', 'たくさんの 七つ', 'ひとり 七つ']`

- shared-tail signal (template-generation):
  - tail ` 七つ`: `['ぜんぶで 七つ', 'たくさんの 七つ', 'ひとり 七つ']`

### 八つ (`n5.vocab.8-native-counters-series.八つ`)
reading: `やっつ`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 八つ', 'たくさんの 八つ', 'ひとり 八つ']`

- shared-tail signal (template-generation):
  - tail ` 八つ`: `['ぜんぶで 八つ', 'たくさんの 八つ', 'ひとり 八つ']`

### 九つ (`n5.vocab.8-native-counters-series.九つ`)
reading: `ここのつ`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 九つ', 'たくさんの 九つ', 'ひとり 九つ']`

- shared-tail signal (template-generation):
  - tail ` 九つ`: `['ぜんぶで 九つ', 'たくさんの 九つ', 'ひとり 九つ']`

### いくつ (`n5.vocab.8-native-counters-series.いくつ`)
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで いくつ', 'たくさんの いくつ', 'ひとり いくつ']`

- shared-tail signal (template-generation):
  - tail `いくつ`: `['いくつ', 'ぜんぶで いくつ', 'たくさんの いくつ', 'ひとり いくつ']`

### 一人 (`n5.vocab.9-counters-common.一人`)
reading: `ひとり`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 一人', 'たくさんの 一人', 'ひとり 一人']`

- shared-tail signal (template-generation):
  - tail ` 一人`: `['ぜんぶで 一人', 'たくさんの 一人', 'ひとり 一人']`

### 二人 (`n5.vocab.9-counters-common.二人`)
reading: `ふたり`  
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで 二人', 'たくさんの 二人', 'ひとり 二人']`

- shared-tail signal (template-generation):
  - tail ` 二人`: `['ぜんぶで 二人', 'たくさんの 二人', 'ひとり 二人']`

### まい (`n5.vocab.9-counters-common.まい`)
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで まい', 'たくさんの まい', 'ひとり まい']`

- shared-tail signal (template-generation):
  - tail ` まい`: `['ぜんぶで まい', 'たくさんの まい', 'ひとり まい']`

### だい (`n5.vocab.9-counters-common.だい`)
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで だい', 'たくさんの だい', 'ひとり だい']`

- shared-tail signal (template-generation):
  - tail ` だい`: `['ぜんぶで だい', 'たくさんの だい', 'ひとり だい']`

### さつ (`n5.vocab.9-counters-common.さつ`)
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで さつ', 'たくさんの さつ', 'ひとり さつ']`

- shared-tail signal (template-generation):
  - tail ` さつ`: `['ぜんぶで さつ', 'たくさんの さつ', 'ひとり さつ']`

### ひき (`n5.vocab.9-counters-common.ひき`)
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで ひき', 'たくさんの ひき', 'ひとり ひき']`

- shared-tail signal (template-generation):
  - tail ` ひき`: `['ぜんぶで ひき', 'たくさんの ひき', 'ひとり ひき']`

### はい (`n5.vocab.9-counters-common.はい`)
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで はい', 'たくさんの はい', 'ひとり はい']`

- shared-tail signal (template-generation):
  - tail ` はい`: `['ぜんぶで はい', 'たくさんの はい', 'ひとり はい']`

### かい (`n5.vocab.9-counters-common.かい`)
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで かい', 'たくさんの かい', 'ひとり かい']`

- shared-tail signal (template-generation):
  - tail ` かい`: `['ぜんぶで かい', 'たくさんの かい', 'ひとり かい']`

### かい (`n5.vocab.9-counters-common.かい.2`)
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで かい', 'たくさんの かい', 'ひとり かい']`

- shared-tail signal (template-generation):
  - tail ` かい`: `['ぜんぶで かい', 'たくさんの かい', 'ひとり かい']`

### とき (`n5.vocab.10-time-general.とき`)
current particle_examples: `['ときどき', 'ねる とき', 'たべる とき', 'こどもの とき', 'おさない とき', 'いる とき', 'はじめての とき']`

- shared-tail signal (template-generation):
  - tail ` とき`: `['ねる とき', 'たべる とき', 'こどもの とき', 'おさない とき', 'いる とき', 'はじめての とき']`

### 時間 (`n5.vocab.10-time-general.時間`)
reading: `じかん`  
current particle_examples: `['時間が ある', '時間に いく', '時間まで まつ', '時間から はじまる', 'いま 時間', '時間は はやい', '時間を まつ', '時間が おわる']`

- template-shape hits:
  - shape `に いく` in `時間に いく`

### とけい (`n5.vocab.10-time-general.とけい`)
current particle_examples: `['とけいを かう', 'とけいを つかう', 'あたらしい とけい', 'たかい とけい', 'とけいを ください', 'とけいは どこ', 'とけいを みる', 'やすい とけい']`

- shared-tail signal (template-generation):
  - tail `とけい`: `['あたらしい とけい', 'たかい とけい', 'やすい とけい']`

### 今 (`n5.vocab.10-time-general.今`)
reading: `いま`  
current particle_examples: `['今が ある', '今に いく', '今まで まつ', '今から はじまる', 'いま 今', '今は はやい', '今を まつ', '今が おわる']`

- template-shape hits:
  - shape `に いく` in `今に いく`

### あした (`n5.vocab.10-time-general.あした`)
current particle_examples: `['あしたが ある', 'あしたに いく', 'あしたまで まつ', 'あしたから はじまる', 'いま あした', 'あしたは はやい', 'あしたを まつ', 'あしたが おわる']`

- template-shape hits:
  - shape `に いく` in `あしたに いく`

### あさって (`n5.vocab.10-time-general.あさって`)
current particle_examples: `['あさってが ある', 'あさってに いく', 'あさってまで まつ', 'あさってから はじまる', 'いま あさって', 'あさっては はやい', 'あさってを まつ', 'あさってが おわる']`

- template-shape hits:
  - shape `に いく` in `あさってに いく`

### おととい (`n5.vocab.10-time-general.おととい`)
current particle_examples: `['おとといが ある', 'おとといに いく', 'おとといまで まつ', 'おとといから はじまる', 'いま おととい', 'おとといは はやい', 'おとといを まつ', 'おとといが おわる']`

- template-shape hits:
  - shape `に いく` in `おとといに いく`

### あさ (`n5.vocab.10-time-general.あさ`)
current particle_examples: `['あさが ある', 'あさに いく', 'あさまで まつ', 'あさから はじまる', 'いま あさ', 'あさは はやい', 'あさを まつ', 'あさが おわる']`

- template-shape hits:
  - shape `に いく` in `あさに いく`

### ひる (`n5.vocab.10-time-general.ひる`)
current particle_examples: `['ひるが ある', 'ひるに いく', 'ひるまで まつ', 'ひるから はじまる', 'いま ひる', 'ひるは はやい', 'ひるを まつ', 'ひるが おわる']`

- template-shape hits:
  - shape `に いく` in `ひるに いく`

### ゆうがた (`n5.vocab.10-time-general.ゆうがた`)
current particle_examples: `['ゆうがたが ある', 'ゆうがたに いく', 'ゆうがたまで まつ', 'ゆうがたから はじまる', 'いま ゆうがた', 'ゆうがたは はやい', 'ゆうがたを まつ', 'ゆうがたが おわる']`

- template-shape hits:
  - shape `に いく` in `ゆうがたに いく`

### ばん (`n5.vocab.10-time-general.ばん`)
current particle_examples: `['ばんが ある', 'ばんに いく', 'ばんまで まつ', 'ばんから はじまる', 'いま ばん', 'ばんは はやい', 'ばんを まつ', 'ばんが おわる']`

- template-shape hits:
  - shape `に いく` in `ばんに いく`

### けさ (`n5.vocab.10-time-general.けさ`)
current particle_examples: `['けさが ある', 'けさに いく', 'けさまで まつ', 'けさから はじまる', 'いま けさ', 'けさは はやい', 'けさを まつ', 'けさが おわる']`

- template-shape hits:
  - shape `に いく` in `けさに いく`

### こんばん (`n5.vocab.10-time-general.こんばん`)
current particle_examples: `['こんばんが ある', 'こんばんに いく', 'こんばんまで まつ', 'こんばんから はじまる', 'いま こんばん', 'こんばんは はやい', 'こんばんを まつ', 'こんばんが おわる']`

- template-shape hits:
  - shape `に いく` in `こんばんに いく`

### こんや (`n5.vocab.10-time-general.こんや`)
current particle_examples: `['こんやが ある', 'こんやに いく', 'こんやまで まつ', 'こんやから はじまる', 'いま こんや', 'こんやは はやい', 'こんやを まつ', 'こんやが おわる']`

- template-shape hits:
  - shape `に いく` in `こんやに いく`

### 午前 (`n5.vocab.10-time-general.午前`)
reading: `ごぜん`  
current particle_examples: `['午前 八時', '午前の じゅぎょう', '午前ちゅう', '午前から ごご まで', '午前に いく', '午前 はやく']`

- template-shape hits:
  - shape `に いく` in `午前に いく`

### 半 (`n5.vocab.10-time-general.半`)
reading: `はん`  
current particle_examples: `['半が ある', '半に いく', '半まで まつ', '半から はじまる', 'いま 半', '半は はやい', '半を まつ', '半が おわる']`

- template-shape hits:
  - shape `に いく` in `半に いく`

### 分 (`n5.vocab.10-time-general.分`)
reading: `ふん`  
current particle_examples: `['分が ある', '分に いく', '分まで まつ', '分から はじまる', 'いま 分', '分は はやい', '分を まつ', '分が おわる']`

- template-shape hits:
  - shape `に いく` in `分に いく`

### びょう (`n5.vocab.10-time-general.びょう`)
current particle_examples: `['びょうが ある', 'びょうに いく', 'びょうまで まつ', 'びょうから はじまる', 'いま びょう', 'びょうは はやい', 'びょうを まつ', 'びょうが おわる']`

- template-shape hits:
  - shape `に いく` in `びょうに いく`

### 日 (`n5.vocab.11-time-days-weeks-month.日`)
reading: `ひ`  
current particle_examples: `['日が ある', '日に いく', '日まで まつ', '日から はじまる', 'いま 日', '日は はやい', '日を まつ', '日が おわる']`

- template-shape hits:
  - shape `に いく` in `日に いく`

### 一日 (`n5.vocab.11-time-days-weeks-month.一日`)
reading: `ついたち`  
current particle_examples: `['一日が ある', '一日に いく', '一日まで まつ', '一日から はじまる', 'いま 一日', '一日は はやい', '一日を まつ', '一日が おわる']`

- template-shape hits:
  - shape `に いく` in `一日に いく`

### 一日 (`n5.vocab.11-time-days-weeks-month.一日.2`)
reading: `いちにち`  
current particle_examples: `['一日が ある', '一日に いく', '一日まで まつ', '一日から はじまる', 'いま 一日', '一日は はやい', '一日を まつ', '一日が おわる']`

- template-shape hits:
  - shape `に いく` in `一日に いく`

### 二日 (`n5.vocab.11-time-days-weeks-month.二日`)
reading: `ふつか`  
current particle_examples: `['二日が ある', '二日に いく', '二日まで まつ', '二日から はじまる', 'いま 二日', '二日は はやい', '二日を まつ', '二日が おわる']`

- template-shape hits:
  - shape `に いく` in `二日に いく`

### 三日 (`n5.vocab.11-time-days-weeks-month.三日`)
reading: `みっか`  
current particle_examples: `['三日が ある', '三日に いく', '三日まで まつ', '三日から はじまる', 'いま 三日', '三日は はやい', '三日を まつ', '三日が おわる']`

- template-shape hits:
  - shape `に いく` in `三日に いく`

### 四日 (`n5.vocab.11-time-days-weeks-month.四日`)
reading: `よっか`  
current particle_examples: `['四日が ある', '四日に いく', '四日まで まつ', '四日から はじまる', 'いま 四日', '四日は はやい', '四日を まつ', '四日が おわる']`

- template-shape hits:
  - shape `に いく` in `四日に いく`

### 六日 (`n5.vocab.11-time-days-weeks-month.六日`)
reading: `むいか`  
current particle_examples: `['六日が ある', '六日に いく', '六日まで まつ', '六日から はじまる', 'いま 六日', '六日は はやい', '六日を まつ', '六日が おわる']`

- template-shape hits:
  - shape `に いく` in `六日に いく`

### 七日 (`n5.vocab.11-time-days-weeks-month.七日`)
reading: `なのか`  
current particle_examples: `['七日が ある', '七日に いく', '七日まで まつ', '七日から はじまる', 'いま 七日', '七日は はやい', '七日を まつ', '七日が おわる']`

- template-shape hits:
  - shape `に いく` in `七日に いく`

### 八日 (`n5.vocab.11-time-days-weeks-month.八日`)
reading: `ようか`  
current particle_examples: `['八日が ある', '八日に いく', '八日まで まつ', '八日から はじまる', 'いま 八日', '八日は はやい', '八日を まつ', '八日が おわる']`

- template-shape hits:
  - shape `に いく` in `八日に いく`

### 九日 (`n5.vocab.11-time-days-weeks-month.九日`)
reading: `ここのか`  
current particle_examples: `['九日が ある', '九日に いく', '九日まで まつ', '九日から はじまる', 'いま 九日', '九日は はやい', '九日を まつ', '九日が おわる']`

- template-shape hits:
  - shape `に いく` in `九日に いく`

### 十日 (`n5.vocab.11-time-days-weeks-month.十日`)
reading: `とおか`  
current particle_examples: `['十日が ある', '十日に いく', '十日まで まつ', '十日から はじまる', 'いま 十日', '十日は はやい', '十日を まつ', '十日が おわる']`

- template-shape hits:
  - shape `に いく` in `十日に いく`

### 二十日 (`n5.vocab.11-time-days-weeks-month.二十日`)
reading: `はつか`  
current particle_examples: `['二十日が ある', '二十日に いく', '二十日まで まつ', '二十日から はじまる', 'いま 二十日', '二十日は はやい', '二十日を まつ', '二十日が おわる']`

- template-shape hits:
  - shape `に いく` in `二十日に いく`

### 週 (`n5.vocab.11-time-days-weeks-month.週`)
reading: `しゅう`  
current particle_examples: `['週が ある', '週に いく', '週まで まつ', '週から はじまる', 'いま 週', '週は はやい', '週を まつ', '週が おわる']`

- template-shape hits:
  - shape `に いく` in `週に いく`

### 月曜日 (`n5.vocab.11-time-days-weeks-month.月曜日`)
reading: `げつようび`  
current particle_examples: `['げつようびから', '月曜日の あさ', '月曜日に いく', '月曜日まで', '月曜日に あう', '月曜日は しごと', '月曜日に はじまる']`

- template-shape hits:
  - shape `に いく` in `月曜日に いく`

### 火曜日 (`n5.vocab.11-time-days-weeks-month.火曜日`)
reading: `かようび`  
current particle_examples: `['火曜日の あさ', '火曜日に いく', '火曜日まで', '火曜日は しごと', '火曜日に あう', '火曜日の よる']`

- template-shape hits:
  - shape `に いく` in `火曜日に いく`

### 水曜日 (`n5.vocab.11-time-days-weeks-month.水曜日`)
reading: `すいようび`  
current particle_examples: `['水曜日の あさ', '水曜日に いく', '水曜日まで', '水曜日に あう', '水曜日の よる', '水曜日の しごと']`

- template-shape hits:
  - shape `に いく` in `水曜日に いく`

### 木曜日 (`n5.vocab.11-time-days-weeks-month.木曜日`)
reading: `もくようび`  
current particle_examples: `['木曜日の あさ', '木曜日に いく', '木曜日まで', '木曜日に あう', '木曜日の よる', '木曜日の しごと']`

- template-shape hits:
  - shape `に いく` in `木曜日に いく`

### 金曜日 (`n5.vocab.11-time-days-weeks-month.金曜日`)
reading: `きんようび`  
current particle_examples: `['金曜日に いく', '金曜日の よる', '金曜日まで', '金曜日に あう', '金曜日は やすみ', '金曜日の しごと']`

- template-shape hits:
  - shape `に いく` in `金曜日に いく`

### 土曜日 (`n5.vocab.11-time-days-weeks-month.土曜日`)
reading: `どようび`  
current particle_examples: `['土曜日に いく', '土曜日の あさ', '土曜日は やすみ', '土曜日に あう', '土曜日の よる', '土曜日まで']`

- template-shape hits:
  - shape `に いく` in `土曜日に いく`

### 日曜日 (`n5.vocab.11-time-days-weeks-month.日曜日`)
reading: `にちようび`  
current particle_examples: `['日曜日に いく', '日曜日の あさ', '日曜日は やすみ', '日曜日 まで', '日曜日に あそぶ', '日曜日の ばん']`

- template-shape hits:
  - shape `に いく` in `日曜日に いく`

### しゅうまつ (`n5.vocab.11-time-days-weeks-month.しゅうまつ`)
current particle_examples: `['しゅうまつが ある', 'しゅうまつに いく', 'しゅうまつまで まつ', 'しゅうまつから はじまる', 'いま しゅうまつ', 'しゅうまつは はやい', 'しゅうまつを まつ', 'しゅうまつが おわる']`

- template-shape hits:
  - shape `に いく` in `しゅうまつに いく`

### 月 (`n5.vocab.11-time-days-weeks-month.月`)
reading: `つき`  
current particle_examples: `['月が ある', '月に いく', '月まで まつ', '月から はじまる', 'いま 月', '月は はやい', '月を まつ', '月が おわる']`

- template-shape hits:
  - shape `に いく` in `月に いく`

### 十一月 (`n5.vocab.11-time-days-weeks-month.十一月`)
reading: `じゅういちがつ`  
current particle_examples: `['十一月を かう', '十一月を つかう', 'あたらしい 十一月', 'たかい 十一月', '十一月を ください', '十一月は どこ', '十一月を みる', 'やすい 十一月']`

- shared-tail signal (template-generation):
  - tail `十一月`: `['あたらしい 十一月', 'たかい 十一月', 'やすい 十一月']`

### 年 (`n5.vocab.11-time-days-weeks-month.年`)
reading: `とし`  
current particle_examples: `['年が ある', '年に いく', '年まで まつ', '年から はじまる', 'いま 年', '年は はやい', '年を まつ', '年が おわる']`

- template-shape hits:
  - shape `に いく` in `年に いく`

### きょねん (`n5.vocab.11-time-days-weeks-month.きょねん`)
current particle_examples: `['きょねんが ある', 'きょねんに いく', 'きょねんまで まつ', 'きょねんから はじまる', 'いま きょねん', 'きょねんは はやい', 'きょねんを まつ', 'きょねんが おわる']`

- template-shape hits:
  - shape `に いく` in `きょねんに いく`

### おととし (`n5.vocab.11-time-days-weeks-month.おととし`)
current particle_examples: `['おととしが ある', 'おととしに いく', 'おととしまで まつ', 'おととしから はじまる', 'いま おととし', 'おととしは はやい', 'おととしを まつ', 'おととしが おわる']`

- template-shape hits:
  - shape `に いく` in `おととしに いく`

### さらいねん (`n5.vocab.11-time-days-weeks-month.さらいねん`)
current particle_examples: `['さらいねんが ある', 'さらいねんに いく', 'さらいねんまで まつ', 'さらいねんから はじまる', 'いま さらいねん', 'さらいねんは はやい', 'さらいねんを まつ', 'さらいねんが おわる']`

- template-shape hits:
  - shape `に いく` in `さらいねんに いく`

### たんじょうび (`n5.vocab.11-time-days-weeks-month.たんじょうび`)
current particle_examples: `['たんじょうびが ある', 'たんじょうびに いく', 'たんじょうびまで まつ', 'たんじょうびから はじまる', 'いま たんじょうび', 'たんじょうびは はやい', 'たんじょうびを まつ', 'たんじょうびが おわる']`

- template-shape hits:
  - shape `に いく` in `たんじょうびに いく`

### まいあさ (`n5.vocab.12-time-frequency-sequen.まいあさ`)
current particle_examples: `['まいあさが ある', 'まいあさに いく', 'まいあさまで まつ', 'まいあさから はじまる', 'いま まいあさ', 'まいあさは はやい', 'まいあさを まつ', 'まいあさが おわる']`

- template-shape hits:
  - shape `に いく` in `まいあさに いく`

### まいばん (`n5.vocab.12-time-frequency-sequen.まいばん`)
current particle_examples: `['まいばんが ある', 'まいばんに いく', 'まいばんまで まつ', 'まいばんから はじまる', 'いま まいばん', 'まいばんは はやい', 'まいばんを まつ', 'まいばんが おわる']`

- template-shape hits:
  - shape `に いく` in `まいばんに いく`

### たまに (`n5.vocab.12-time-frequency-sequen.たまに`)
current particle_examples: `['たまに いく', 'たまに あう', 'たまに たべる', 'たまに みる', 'たまに あそぶ', 'たまに 来る']`

- template-shape hits:
  - shape `に いく` in `たまに いく`

### さいしょ (`n5.vocab.12-time-frequency-sequen.さいしょ`)
current particle_examples: `['さいしょを かう', 'さいしょを つかう', 'あたらしい さいしょ', 'たかい さいしょ', 'さいしょを ください', 'さいしょは どこ', 'さいしょを みる', 'やすい さいしょ']`

- shared-tail signal (template-generation):
  - tail `いしょ`: `['あたらしい さいしょ', 'たかい さいしょ', 'やすい さいしょ']`

### さいご (`n5.vocab.12-time-frequency-sequen.さいご`)
current particle_examples: `['さいごを かう', 'さいごを つかう', 'あたらしい さいご', 'たかい さいご', 'さいごを ください', 'さいごは どこ', 'さいごを みる', 'やすい さいご']`

- shared-tail signal (template-generation):
  - tail `さいご`: `['あたらしい さいご', 'たかい さいご', 'やすい さいご']`

### つぎ (`n5.vocab.12-time-frequency-sequen.つぎ`)
current particle_examples: `['つぎを かう', 'つぎを つかう', 'あたらしい つぎ', 'たかい つぎ', 'つぎを ください', 'つぎは どこ', 'つぎを みる', 'やすい つぎ']`

- shared-tail signal (template-generation):
  - tail ` つぎ`: `['あたらしい つぎ', 'たかい つぎ', 'やすい つぎ']`

### 前 (`n5.vocab.12-time-frequency-sequen.前`)
reading: `まえ`  
current particle_examples: `['前に いく', '前で あう', '前から くる', '前の まえに', '前が ある', '前は ちかい', '前まで あるく', '前に つく']`

- template-shape hits:
  - shape `に いく` in `前に いく`

### ところ (`n5.vocab.13-locations-and-places-.ところ`)
current particle_examples: `['いまの ところ', 'ところで', 'ねる ところ', 'すんでいる ところ', 'はたらく ところ', 'たかい ところ']`

- shared-tail signal (template-generation):
  - tail `ところ`: `['いまの ところ', 'ねる ところ', 'すんでいる ところ', 'はたらく ところ', 'たかい ところ']`

### へや (`n5.vocab.13-locations-and-places-.へや`)
current particle_examples: `['へやに いく', 'へやで あう', 'へやから くる', 'へやの まえに', 'へやが ある', 'へやは ちかい', 'へやまで あるく', 'へやに つく']`

- template-shape hits:
  - shape `に いく` in `へやに いく`

### だいどころ (`n5.vocab.13-locations-and-places-.だいどころ`)
current particle_examples: `['だいどころに いく', 'だいどころで あう', 'だいどころから くる', 'だいどころの まえに', 'だいどころが ある', 'だいどころは ちかい', 'だいどころまで あるく', 'だいどころに つく']`

- template-shape hits:
  - shape `に いく` in `だいどころに いく`

### おてあらい (`n5.vocab.13-locations-and-places-.おてあらい`)
current particle_examples: `['おてあらいに いく', 'おてあらいで あう', 'おてあらいから くる', 'おてあらいの まえに', 'おてあらいが ある', 'おてあらいは ちかい', 'おてあらいまで あるく', 'おてあらいに つく']`

- template-shape hits:
  - shape `に いく` in `おてあらいに いく`

### トイレ (`n5.vocab.13-locations-and-places-.トイレ`)
current particle_examples: `['トイレに いく', 'トイレの ばしょ', 'きれいな トイレ', 'トイレの ドア', 'トイレを そうじする', 'トイレの かぎ']`

- template-shape hits:
  - shape `に いく` in `トイレに いく`

### おふろ (`n5.vocab.13-locations-and-places-.おふろ`)
current particle_examples: `['おふろに いく', 'おふろで あう', 'おふろから くる', 'おふろの まえに', 'おふろが ある', 'おふろは ちかい', 'おふろまで あるく', 'おふろに つく']`

- template-shape hits:
  - shape `に いく` in `おふろに いく`

### げんかん (`n5.vocab.13-locations-and-places-.げんかん`)
current particle_examples: `['げんかんに いく', 'げんかんで あう', 'げんかんから くる', 'げんかんの まえに', 'げんかんが ある', 'げんかんは ちかい', 'げんかんまで あるく', 'げんかんに つく']`

- template-shape hits:
  - shape `に いく` in `げんかんに いく`

### にわ (`n5.vocab.13-locations-and-places-.にわ`)
current particle_examples: `['にわに いく', 'にわで あう', 'にわから くる', 'にわの まえに', 'にわが ある', 'にわは ちかい', 'にわまで あるく', 'にわに つく']`

- template-shape hits:
  - shape `に いく` in `にわに いく`

### 高校 (`n5.vocab.13-locations-and-places-.高校`)
reading: `こうこう`  
current particle_examples: `['高校生を', '高校せい', '高校に いく', '高校の せんせい', '高校の ともだち', '高校を 出る', '高校の しけん']`

- template-shape hits:
  - shape `に いく` in `高校に いく`

### きょうしつ (`n5.vocab.13-locations-and-places-.きょうしつ`)
current particle_examples: `['きょうしつに いく', 'きょうしつで あう', 'きょうしつから くる', 'きょうしつの まえに', 'きょうしつが ある', 'きょうしつは ちかい', 'きょうしつまで あるく', 'きょうしつに つく']`

- template-shape hits:
  - shape `に いく` in `きょうしつに いく`

### としょかん (`n5.vocab.13-locations-and-places-.としょかん`)
current particle_examples: `['としょかんに いく', 'としょかんで あう', 'としょかんから くる', 'としょかんの まえに', 'としょかんが ある', 'としょかんは ちかい', 'としょかんまで あるく', 'としょかんに つく']`

- template-shape hits:
  - shape `に いく` in `としょかんに いく`

### びょういん (`n5.vocab.13-locations-and-places-.びょういん`)
current particle_examples: `['びょういんに いく', 'びょういんで あう', 'びょういんから くる', 'びょういんの まえに', 'びょういんが ある', 'びょういんは ちかい', 'びょういんまで あるく', 'びょういんに つく']`

- template-shape hits:
  - shape `に いく` in `びょういんに いく`

### ぎんこう (`n5.vocab.13-locations-and-places-.ぎんこう`)
current particle_examples: `['ぎんこうに いく', 'ぎんこうで あう', 'ぎんこうから くる', 'ぎんこうの まえに', 'ぎんこうが ある', 'ぎんこうは ちかい', 'ぎんこうまで あるく', 'ぎんこうに つく']`

- template-shape hits:
  - shape `に いく` in `ぎんこうに いく`

### ゆうびんきょく (`n5.vocab.13-locations-and-places-.ゆうびんきょく`)
current particle_examples: `['ゆうびんきょくに いく', 'ゆうびんきょくで あう', 'ゆうびんきょくから くる', 'ゆうびんきょくの まえに', 'ゆうびんきょくが ある', 'ゆうびんきょくは ちかい', 'ゆうびんきょくまで あるく', 'ゆうびんきょくに つく']`

- template-shape hits:
  - shape `に いく` in `ゆうびんきょくに いく`

### 会社 (`n5.vocab.13-locations-and-places-.会社`)
reading: `かいしゃ`  
current particle_examples: `['会社に いく', '会社で あう', '会社から くる', '会社の まえに', '会社が ある', '会社は ちかい', '会社まで あるく', '会社に つく']`

- template-shape hits:
  - shape `に いく` in `会社に いく`

### じむしょ (`n5.vocab.13-locations-and-places-.じむしょ`)
current particle_examples: `['じむしょに いく', 'じむしょで あう', 'じむしょから くる', 'じむしょの まえに', 'じむしょが ある', 'じむしょは ちかい', 'じむしょまで あるく', 'じむしょに つく']`

- template-shape hits:
  - shape `に いく` in `じむしょに いく`

### お店 (`n5.vocab.13-locations-and-places-.お店`)
reading: `おみせ`  
current particle_examples: `['お店に いく', 'お店で あう', 'お店から くる', 'お店の まえに', 'お店が ある', 'お店は ちかい', 'お店まで あるく', 'お店に つく']`

- template-shape hits:
  - shape `に いく` in `お店に いく`

### スーパー (`n5.vocab.13-locations-and-places-.スーパー`)
current particle_examples: `['スーパーに いく', 'スーパーで あう', 'スーパーから くる', 'スーパーの まえに', 'スーパーが ある', 'スーパーは ちかい', 'スーパーまで あるく', 'スーパーに つく']`

- template-shape hits:
  - shape `に いく` in `スーパーに いく`

### デパート (`n5.vocab.13-locations-and-places-.デパート`)
current particle_examples: `['デパートに いく', 'デパートで かう', '大きな デパート', 'デパートの レストラン', 'デパートの セール', 'デパートの 店員']`

- template-shape hits:
  - shape `に いく` in `デパートに いく`

### きっさてん (`n5.vocab.13-locations-and-places-.きっさてん`)
current particle_examples: `['きっさてんに いく', 'きっさてんで あう', 'きっさてんから くる', 'きっさてんの まえに', 'きっさてんが ある', 'きっさてんは ちかい', 'きっさてんまで あるく', 'きっさてんに つく']`

- template-shape hits:
  - shape `に いく` in `きっさてんに いく`

### レストラン (`n5.vocab.13-locations-and-places-.レストラン`)
current particle_examples: `['レストランへ いく', 'レストランで たべる', '日本の レストラン', 'たかい レストラン', 'やすい レストラン', 'レストランの メニュー']`

- shared-tail signal (template-generation):
  - tail `トラン`: `['日本の レストラン', 'たかい レストラン', 'やすい レストラン']`

### やおや (`n5.vocab.13-locations-and-places-.やおや`)
current particle_examples: `['やおやを かう', 'やおやを つかう', 'あたらしい やおや', 'たかい やおや', 'やおやを ください', 'やおやは どこ', 'やおやを みる', 'やすい やおや']`

- shared-tail signal (template-generation):
  - tail `やおや`: `['あたらしい やおや', 'たかい やおや', 'やすい やおや']`

### ほんや (`n5.vocab.13-locations-and-places-.ほんや`)
current particle_examples: `['ほんやに いく', 'ほんやで あう', 'ほんやから くる', 'ほんやの まえに', 'ほんやが ある', 'ほんやは ちかい', 'ほんやまで あるく', 'ほんやに つく']`

- template-shape hits:
  - shape `に いく` in `ほんやに いく`

### はなや (`n5.vocab.13-locations-and-places-.はなや`)
current particle_examples: `['はなやに いく', 'はなやで あう', 'はなやから くる', 'はなやの まえに', 'はなやが ある', 'はなやは ちかい', 'はなやまで あるく', 'はなやに つく']`

- template-shape hits:
  - shape `に いく` in `はなやに いく`

### にくや (`n5.vocab.13-locations-and-places-.にくや`)
current particle_examples: `['にくやを かう', 'にくやを つかう', 'あたらしい にくや', 'たかい にくや', 'にくやを ください', 'にくやは どこ', 'にくやを みる', 'やすい にくや']`

- shared-tail signal (template-generation):
  - tail `にくや`: `['あたらしい にくや', 'たかい にくや', 'やすい にくや']`

### パンや (`n5.vocab.13-locations-and-places-.パンや`)
current particle_examples: `['パンやを かう', 'パンやを つかう', 'あたらしい パンや', 'たかい パンや', 'パンやを ください', 'パンやは どこ', 'パンやを みる', 'やすい パンや']`

- shared-tail signal (template-generation):
  - tail `パンや`: `['あたらしい パンや', 'たかい パンや', 'やすい パンや']`

### 駅 (`n5.vocab.13-locations-and-places-.駅`)
reading: `えき`  
current particle_examples: `['駅に いく', '駅で あう', '駅から くる', '駅の まえに', '駅が ある', '駅は ちかい', '駅まで あるく', '駅に つく']`

- template-shape hits:
  - shape `に いく` in `駅に いく`

### くうこう (`n5.vocab.13-locations-and-places-.くうこう`)
current particle_examples: `['くうこうに いく', 'くうこうで あう', 'くうこうから くる', 'くうこうの まえに', 'くうこうが ある', 'くうこうは ちかい', 'くうこうまで あるく', 'くうこうに つく']`

- template-shape hits:
  - shape `に いく` in `くうこうに いく`

### こうえん (`n5.vocab.13-locations-and-places-.こうえん`)
current particle_examples: `['こうえんに いく', 'こうえんで あう', 'こうえんから くる', 'こうえんの まえに', 'こうえんが ある', 'こうえんは ちかい', 'こうえんまで あるく', 'こうえんに つく']`

- template-shape hits:
  - shape `に いく` in `こうえんに いく`

### どうぶつえん (`n5.vocab.13-locations-and-places-.どうぶつえん`)
current particle_examples: `['どうぶつえんに いく', 'どうぶつえんで あう', 'どうぶつえんから くる', 'どうぶつえんの まえに', 'どうぶつえんが ある', 'どうぶつえんは ちかい', 'どうぶつえんまで あるく', 'どうぶつえんに つく']`

- template-shape hits:
  - shape `に いく` in `どうぶつえんに いく`

### びじゅつかん (`n5.vocab.13-locations-and-places-.びじゅつかん`)
current particle_examples: `['びじゅつかんに いく', 'びじゅつかんで あう', 'びじゅつかんから くる', 'びじゅつかんの まえに', 'びじゅつかんが ある', 'びじゅつかんは ちかい', 'びじゅつかんまで あるく', 'びじゅつかんに つく']`

- template-shape hits:
  - shape `に いく` in `びじゅつかんに いく`

### えいがかん (`n5.vocab.13-locations-and-places-.えいがかん`)
current particle_examples: `['えいがかんに いく', 'えいがかんで あう', 'えいがかんから くる', 'えいがかんの まえに', 'えいがかんが ある', 'えいがかんは ちかい', 'えいがかんまで あるく', 'えいがかんに つく']`

- template-shape hits:
  - shape `に いく` in `えいがかんに いく`

### ホテル (`n5.vocab.13-locations-and-places-.ホテル`)
current particle_examples: `['ホテルに とまる', 'ホテルの へや', 'いい ホテル', '高い ホテル', 'やすい ホテル', 'ホテルから 出る']`

- shared-tail signal (template-generation):
  - tail `ホテル`: `['いい ホテル', '高い ホテル', 'やすい ホテル']`

### りょかん (`n5.vocab.13-locations-and-places-.りょかん`)
current particle_examples: `['りょかんに いく', 'りょかんで あう', 'りょかんから くる', 'りょかんの まえに', 'りょかんが ある', 'りょかんは ちかい', 'りょかんまで あるく', 'りょかんに つく']`

- template-shape hits:
  - shape `に いく` in `りょかんに いく`

### たいしかん (`n5.vocab.13-locations-and-places-.たいしかん`)
current particle_examples: `['たいしかんに いく', 'たいしかんで あう', 'たいしかんから くる', 'たいしかんの まえに', 'たいしかんが ある', 'たいしかんは ちかい', 'たいしかんまで あるく', 'たいしかんに つく']`

- template-shape hits:
  - shape `に いく` in `たいしかんに いく`

### こうばん (`n5.vocab.13-locations-and-places-.こうばん`)
current particle_examples: `['こうばんと あう', 'こうばんと はなす', 'こうばんに きく', 'こうばんは どこ', 'こうばんの なまえ', 'こうばんが くる', 'こうばんが いる', 'こうばんは やさしい']`

- template-shape hits:
  - shape `と あう` in `こうばんと あう`

### こうじょう (`n5.vocab.13-locations-and-places-.こうじょう`)
current particle_examples: `['こうじょうと あう', 'こうじょうと はなす', 'こうじょうに きく', 'こうじょうは どこ', 'こうじょうの なまえ', 'こうじょうが くる', 'こうじょうが いる', 'こうじょうは やさしい']`

- template-shape hits:
  - shape `と あう` in `こうじょうと あう`

### こうさてん (`n5.vocab.13-locations-and-places-.こうさてん`)
current particle_examples: `['こうさてんに いく', 'こうさてんで あう', 'こうさてんから くる', 'こうさてんの まえに', 'こうさてんが ある', 'こうさてんは ちかい', 'こうさてんまで あるく', 'こうさてんに つく']`

- template-shape hits:
  - shape `に いく` in `こうさてんに いく`

### いりぐち (`n5.vocab.13-locations-and-places-.いりぐち`)
current particle_examples: `['いりぐちに いく', 'いりぐちで あう', 'いりぐちから くる', 'いりぐちの まえに', 'いりぐちが ある', 'いりぐちは ちかい', 'いりぐちまで あるく', 'いりぐちに つく']`

- template-shape hits:
  - shape `に いく` in `いりぐちに いく`

### しょくどう (`n5.vocab.13-locations-and-places-.しょくどう`)
current particle_examples: `['しょくどうに いく', 'しょくどうで あう', 'しょくどうから くる', 'しょくどうの まえに', 'しょくどうが ある', 'しょくどうは ちかい', 'しょくどうまで あるく', 'しょくどうに つく']`

- template-shape hits:
  - shape `に いく` in `しょくどうに いく`

### たてもの (`n5.vocab.13-locations-and-places-.たてもの`)
current particle_examples: `['たてものに いく', 'たてもので あう', 'たてものから くる', 'たてものの まえに', 'たてものが ある', 'たてものは ちかい', 'たてものまで あるく', 'たてものに つく']`

- template-shape hits:
  - shape `に いく` in `たてものに いく`

### ろうか (`n5.vocab.13-locations-and-places-.ろうか`)
current particle_examples: `['ろうかに いく', 'ろうかで あう', 'ろうかから くる', 'ろうかの まえに', 'ろうかが ある', 'ろうかは ちかい', 'ろうかまで あるく', 'ろうかに つく']`

- template-shape hits:
  - shape `に いく` in `ろうかに いく`

### プール (`n5.vocab.13-locations-and-places-.プール`)
current particle_examples: `['プールに いく', 'プールで あう', 'プールから くる', 'プールの まえに', 'プールが ある', 'プールは ちかい', 'プールまで あるく', 'プールに つく']`

- template-shape hits:
  - shape `に いく` in `プールに いく`

### ポスト (`n5.vocab.13-locations-and-places-.ポスト`)
current particle_examples: `['ポストを かう', 'ポストを つかう', 'あたらしい ポスト', 'たかい ポスト', 'ポストを ください', 'ポストは どこ', 'ポストを みる', 'やすい ポスト']`

- shared-tail signal (template-generation):
  - tail `ポスト`: `['あたらしい ポスト', 'たかい ポスト', 'やすい ポスト']`

### とおり (`n5.vocab.13-locations-and-places-.とおり`)
current particle_examples: `['この とおり', 'おなじ とおり', 'すきな とおり', 'とおりに する', 'いう とおり', 'たくさんの とおり']`

- shared-tail signal (template-generation):
  - tail `とおり`: `['この とおり', 'おなじ とおり', 'すきな とおり', 'いう とおり', 'たくさんの とおり']`

### かど (`n5.vocab.13-locations-and-places-.かど`)
current particle_examples: `['かどを かう', 'かどを つかう', 'あたらしい かど', 'たかい かど', 'かどを ください', 'かどは どこ', 'かどを みる', 'やすい かど']`

- shared-tail signal (template-generation):
  - tail ` かど`: `['あたらしい かど', 'たかい かど', 'やすい かど']`

### はし (`n5.vocab.13-locations-and-places-.はし`)
current particle_examples: `['はしに いく', 'はしで あう', 'はしから くる', 'はしの まえに', 'はしが ある', 'はしは ちかい', 'はしまで あるく', 'はしに つく']`

- template-shape hits:
  - shape `に いく` in `はしに いく`

### まち (`n5.vocab.13-locations-and-places-.まち`)
current particle_examples: `['まちで かう', '小さい まち', '大きい まち', 'まちを あるく', 'まちの まんなか', 'にぎやかな まち']`

- shared-tail signal (template-generation):
  - tail ` まち`: `['小さい まち', '大きい まち', 'にぎやかな まち']`

### むら (`n5.vocab.13-locations-and-places-.むら`)
current particle_examples: `['むらに いく', 'むらで あう', 'むらから くる', 'むらの まえに', 'むらが ある', 'むらは ちかい', 'むらまで あるく', 'むらに つく']`

- template-shape hits:
  - shape `に いく` in `むらに いく`

### 国 (`n5.vocab.13-locations-and-places-.国`)
reading: `くに`  
current particle_examples: `['国に いく', '国で あう', '国から くる', '国の まえに', '国が ある', '国は ちかい', '国まで あるく', '国に つく']`

- template-shape hits:
  - shape `に いく` in `国に いく`

### 外 (`n5.vocab.13-locations-and-places-.外`)
reading: `そと`  
current particle_examples: `['外に いく', '外で あう', '外から くる', '外の まえに', '外が ある', '外は ちかい', '外まで あるく', '外に つく']`

- template-shape hits:
  - shape `に いく` in `外に いく`

### 中 (`n5.vocab.13-locations-and-places-.中`)
reading: `なか`  
current particle_examples: `['中に いく', '中で あう', '中から くる', '中の まえに', '中が ある', '中は ちかい', '中まで あるく', '中に つく']`

- template-shape hits:
  - shape `に いく` in `中に いく`

### 上 (`n5.vocab.13-locations-and-places-.上`)
reading: `うえ`  
current particle_examples: `['上に いく', '上で あう', '上から くる', '上の まえに', '上が ある', '上は ちかい', '上まで あるく', '上に つく']`

- template-shape hits:
  - shape `に いく` in `上に いく`

### 下 (`n5.vocab.13-locations-and-places-.下`)
reading: `した`  
current particle_examples: `['下に いく', '下で あう', '下から くる', '下の まえに', '下が ある', '下は ちかい', '下まで あるく', '下に つく']`

- template-shape hits:
  - shape `に いく` in `下に いく`

### 左 (`n5.vocab.13-locations-and-places-.左`)
reading: `ひだり`  
current particle_examples: `['左を かう', '左を つかう', 'あたらしい 左', 'たかい 左', '左を ください', '左は どこ', '左を みる', 'やすい 左']`

- shared-tail signal (template-generation):
  - tail `い 左`: `['あたらしい 左', 'たかい 左', 'やすい 左']`

### 右 (`n5.vocab.13-locations-and-places-.右`)
reading: `みぎ`  
current particle_examples: `['右を かう', '右を つかう', 'あたらしい 右', 'たかい 右', '右を ください', '右は どこ', '右を みる', 'やすい 右']`

- shared-tail signal (template-generation):
  - tail `い 右`: `['あたらしい 右', 'たかい 右', 'やすい 右']`

### となり (`n5.vocab.13-locations-and-places-.となり`)
current particle_examples: `['となりを かう', 'となりを つかう', 'あたらしい となり', 'たかい となり', 'となりを ください', 'となりは どこ', 'となりを みる', 'やすい となり']`

- shared-tail signal (template-generation):
  - tail `となり`: `['あたらしい となり', 'たかい となり', 'やすい となり']`

### よこ (`n5.vocab.13-locations-and-places-.よこ`)
current particle_examples: `['よこを かう', 'よこを つかう', 'あたらしい よこ', 'たかい よこ', 'よこを ください', 'よこは どこ', 'よこを みる', 'やすい よこ']`

- shared-tail signal (template-generation):
  - tail ` よこ`: `['あたらしい よこ', 'たかい よこ', 'やすい よこ']`

### とおく (`n5.vocab.13-locations-and-places-.とおく`)
current particle_examples: `['とおくを かう', 'とおくを つかう', 'あたらしい とおく', 'たかい とおく', 'とおくを ください', 'とおくは どこ', 'とおくを みる', 'やすい とおく']`

- shared-tail signal (template-generation):
  - tail `とおく`: `['あたらしい とおく', 'たかい とおく', 'やすい とおく']`

### むこう (`n5.vocab.13-locations-and-places-.むこう`)
current particle_examples: `['むこうを かう', 'むこうを つかう', 'あたらしい むこう', 'たかい むこう', 'むこうを ください', 'むこうは どこ', 'むこうを みる', 'やすい むこう']`

- shared-tail signal (template-generation):
  - tail `むこう`: `['あたらしい むこう', 'たかい むこう', 'やすい むこう']`

### 北 (`n5.vocab.13-locations-and-places-.北`)
reading: `きた`  
current particle_examples: `['北を かう', '北を つかう', 'あたらしい 北', 'たかい 北', '北を ください', '北は どこ', '北を みる', 'やすい 北']`

- shared-tail signal (template-generation):
  - tail `い 北`: `['あたらしい 北', 'たかい 北', 'やすい 北']`

### 南 (`n5.vocab.13-locations-and-places-.南`)
reading: `みなみ`  
current particle_examples: `['南を かう', '南を つかう', 'あたらしい 南', 'たかい 南', '南を ください', '南は どこ', '南を みる', 'やすい 南']`

- shared-tail signal (template-generation):
  - tail `い 南`: `['あたらしい 南', 'たかい 南', 'やすい 南']`

### 東 (`n5.vocab.13-locations-and-places-.東`)
reading: `ひがし`  
current particle_examples: `['東を かう', '東を つかう', 'あたらしい 東', 'たかい 東', '東を ください', '東は どこ', '東を みる', 'やすい 東']`

- shared-tail signal (template-generation):
  - tail `い 東`: `['あたらしい 東', 'たかい 東', 'やすい 東']`

### 西 (`n5.vocab.13-locations-and-places-.西`)
reading: `にし`  
current particle_examples: `['西を かう', '西を つかう', 'あたらしい 西', 'たかい 西', '西を ください', '西は どこ', '西を みる', 'やすい 西']`

- shared-tail signal (template-generation):
  - tail `い 西`: `['あたらしい 西', 'たかい 西', 'やすい 西']`

### 山 (`n5.vocab.14-nature-and-weather.山`)
reading: `やま`  
current particle_examples: `['山に いく', '山で あう', '山から くる', '山の まえに', '山が ある', '山は ちかい', '山まで あるく', '山に つく']`

- template-shape hits:
  - shape `に いく` in `山に いく`

### 川 (`n5.vocab.14-nature-and-weather.川`)
reading: `かわ`  
current particle_examples: `['川に いく', '川で あう', '川から くる', '川の まえに', '川が ある', '川は ちかい', '川まで あるく', '川に つく']`

- template-shape hits:
  - shape `に いく` in `川に いく`

### うみ (`n5.vocab.14-nature-and-weather.うみ`)
current particle_examples: `['うみに いく', 'うみで あう', 'うみから くる', 'うみの まえに', 'うみが ある', 'うみは ちかい', 'うみまで あるく', 'うみに つく']`

- template-shape hits:
  - shape `に いく` in `うみに いく`

### いけ (`n5.vocab.14-nature-and-weather.いけ`)
current particle_examples: `['ねてはいけま', 'すってはいけま', '話してはいけま', 'はいけませんよ', 'しいけれど', 'やすいけど', '行きたいけど', 'たのしいけど']`

- shared-tail signal (template-generation):
  - tail `いけま`: `['ねてはいけま', 'すってはいけま', '話してはいけま']`
  - tail `いけど`: `['やすいけど', '行きたいけど', 'たのしいけど']`

### みずうみ (`n5.vocab.14-nature-and-weather.みずうみ`)
current particle_examples: `['みずうみを かう', 'みずうみを つかう', 'あたらしい みずうみ', 'たかい みずうみ', 'みずうみを ください', 'みずうみは どこ', 'みずうみを みる', 'やすい みずうみ']`

- shared-tail signal (template-generation):
  - tail `ずうみ`: `['あたらしい みずうみ', 'たかい みずうみ', 'やすい みずうみ']`

### もり (`n5.vocab.14-nature-and-weather.もり`)
current particle_examples: `['もりに いく', 'もりで あう', 'もりから くる', 'もりの まえに', 'もりが ある', 'もりは ちかい', 'もりまで あるく', 'もりに つく']`

- template-shape hits:
  - shape `に いく` in `もりに いく`

### 木 (`n5.vocab.14-nature-and-weather.木`)
reading: `き`  
current particle_examples: `['木が ある', '木に いく', '木まで まつ', '木から はじまる', 'いま 木', '木は はやい', '木を まつ', '木が おわる']`

- template-shape hits:
  - shape `に いく` in `木に いく`

### はる (`n5.vocab.14-nature-and-weather.はる`)
current particle_examples: `['はるが ある', 'はるに いく', 'はるまで まつ', 'はるから はじまる', 'いま はる', 'はるは はやい', 'はるを まつ', 'はるが おわる']`

- template-shape hits:
  - shape `に いく` in `はるに いく`

### なつ (`n5.vocab.14-nature-and-weather.なつ`)
current particle_examples: `['なつが ある', 'なつに いく', 'なつまで まつ', 'なつから はじまる', 'いま なつ', 'なつは はやい', 'なつを まつ', 'なつが おわる']`

- template-shape hits:
  - shape `に いく` in `なつに いく`

### ふゆ (`n5.vocab.14-nature-and-weather.ふゆ`)
current particle_examples: `['ふゆが ある', 'ふゆに いく', 'ふゆまで まつ', 'ふゆから はじまる', 'いま ふゆ', 'ふゆは はやい', 'ふゆを まつ', 'ふゆが おわる']`

- template-shape hits:
  - shape `に いく` in `ふゆに いく`

### 火 (`n5.vocab.14-nature-and-weather.火`)
reading: `ひ`  
current particle_examples: `['火が ある', '火に いく', '火まで まつ', '火から はじまる', 'いま 火', '火は はやい', '火を まつ', '火が おわる']`

- template-shape hits:
  - shape `に いく` in `火に いく`

### どうぶつ (`n5.vocab.15-animals.どうぶつ`)
current particle_examples: `['どうぶつを かう', 'どうぶつを つかう', 'あたらしい どうぶつ', 'たかい どうぶつ', 'どうぶつを ください', 'どうぶつは どこ', 'どうぶつを みる', 'やすい どうぶつ']`

- shared-tail signal (template-generation):
  - tail `うぶつ`: `['あたらしい どうぶつ', 'たかい どうぶつ', 'やすい どうぶつ']`

### いぬ (`n5.vocab.15-animals.いぬ`)
current particle_examples: `['いぬを かう', 'いぬを つかう', 'あたらしい いぬ', 'たかい いぬ', 'いぬを ください', 'いぬは どこ', 'いぬを みる', 'やすい いぬ']`

- shared-tail signal (template-generation):
  - tail ` いぬ`: `['あたらしい いぬ', 'たかい いぬ', 'やすい いぬ']`

### ねこ (`n5.vocab.15-animals.ねこ`)
current particle_examples: `['ねこを かう', 'かわいい ねこ', '小さい ねこ', 'しろい ねこ', 'ねこの えさ', 'ねこと あそぶ']`

- shared-tail signal (template-generation):
  - tail ` ねこ`: `['かわいい ねこ', '小さい ねこ', 'しろい ねこ']`

### さかな (`n5.vocab.15-animals.さかな`)
current particle_examples: `['さかなを たべる', 'さかなを つくる', 'おいしい さかな', 'さかなが すき', 'さかなを かう', 'からい さかな', 'さかなを ちゅうもんする', 'にほんの さかな']`

- shared-tail signal (template-generation):
  - tail `さかな`: `['おいしい さかな', 'からい さかな', 'にほんの さかな']`

### ぶた (`n5.vocab.15-animals.ぶた`)
current particle_examples: `['ぶたを かう', 'ぶたを つかう', 'あたらしい ぶた', 'たかい ぶた', 'ぶたを ください', 'ぶたは どこ', 'ぶたを みる', 'やすい ぶた']`

- shared-tail signal (template-generation):
  - tail ` ぶた`: `['あたらしい ぶた', 'たかい ぶた', 'やすい ぶた']`

### にわとり (`n5.vocab.15-animals.にわとり`)
current particle_examples: `['にわとりを かう', 'にわとりを つかう', 'あたらしい にわとり', 'たかい にわとり', 'にわとりを ください', 'にわとりは どこ', 'にわとりを みる', 'やすい にわとり']`

- shared-tail signal (template-generation):
  - tail `わとり`: `['あたらしい にわとり', 'たかい にわとり', 'やすい にわとり']`

### ぞう (`n5.vocab.15-animals.ぞう`)
current particle_examples: `['ぞうを かう', 'ぞうを つかう', 'あたらしい ぞう', 'たかい ぞう', 'ぞうを ください', 'ぞうは どこ', 'ぞうを みる', 'やすい ぞう']`

- shared-tail signal (template-generation):
  - tail ` ぞう`: `['あたらしい ぞう', 'たかい ぞう', 'やすい ぞう']`

### むし (`n5.vocab.15-animals.むし`)
current particle_examples: `['むしを かう', 'むしを つかう', 'あたらしい むし', 'たかい むし', 'むしを ください', 'むしは どこ', 'むしを みる', 'やすい むし']`

- shared-tail signal (template-generation):
  - tail ` むし`: `['あたらしい むし', 'たかい むし', 'やすい むし']`

### たべもの (`n5.vocab.16-food-and-drink-genera.たべもの`)
current particle_examples: `['たべものを たべる', 'たべものを つくる', 'おいしい たべもの', 'たべものが すき', 'たべものを かう', 'からい たべもの', 'たべものを ちゅうもんする', 'にほんの たべもの']`

- shared-tail signal (template-generation):
  - tail `べもの`: `['おいしい たべもの', 'からい たべもの', 'にほんの たべもの']`

### あさごはん (`n5.vocab.16-food-and-drink-genera.あさごはん`)
current particle_examples: `['あさごはんを たべる', 'あさごはんを つくる', 'おいしい あさごはん', 'あさごはんが すき', 'あさごはんを かう', 'からい あさごはん', 'あさごはんを ちゅうもんする', 'にほんの あさごはん']`

- shared-tail signal (template-generation):
  - tail `ごはん`: `['おいしい あさごはん', 'からい あさごはん', 'にほんの あさごはん']`

### ひるごはん (`n5.vocab.16-food-and-drink-genera.ひるごはん`)
current particle_examples: `['ひるごはんを たべる', 'ひるごはんを つくる', 'おいしい ひるごはん', 'ひるごはんが すき', 'ひるごはんを かう', 'からい ひるごはん', 'ひるごはんを ちゅうもんする', 'にほんの ひるごはん']`

- shared-tail signal (template-generation):
  - tail `ごはん`: `['おいしい ひるごはん', 'からい ひるごはん', 'にほんの ひるごはん']`

### ばんごはん (`n5.vocab.16-food-and-drink-genera.ばんごはん`)
current particle_examples: `['ばんごはんを たべる', 'ばんごはんを つくる', 'おいしい ばんごはん', 'ばんごはんが すき', 'ばんごはんを かう', 'からい ばんごはん', 'ばんごはんを ちゅうもんする', 'にほんの ばんごはん']`

- shared-tail signal (template-generation):
  - tail `ごはん`: `['おいしい ばんごはん', 'からい ばんごはん', 'にほんの ばんごはん']`

### ゆうはん (`n5.vocab.16-food-and-drink-genera.ゆうはん`)
current particle_examples: `['ゆうはんを たべる', 'ゆうはんを つくる', 'おいしい ゆうはん', 'ゆうはんが すき', 'ゆうはんを かう', 'からい ゆうはん', 'ゆうはんを ちゅうもんする', 'にほんの ゆうはん']`

- shared-tail signal (template-generation):
  - tail `うはん`: `['おいしい ゆうはん', 'からい ゆうはん', 'にほんの ゆうはん']`

### ごはん (`n5.vocab.16-food-and-drink-genera.ごはん`)
current particle_examples: `['あさごはんを', 'ばんごはんを', 'ばんごはんは', 'ひるごはんを', 'ばんごはんの', 'あさごはんは', 'ひるごはんが', 'ばんごはんが']`

- shared-tail signal (template-generation):
  - tail `はんを`: `['あさごはんを', 'ばんごはんを', 'ひるごはんを']`

### しょくじ (`n5.vocab.16-food-and-drink-genera.しょくじ`)
current particle_examples: `['しょくじを たべる', 'しょくじを つくる', 'おいしい しょくじ', 'しょくじが すき', 'しょくじを かう', 'からい しょくじ', 'しょくじを ちゅうもんする', 'にほんの しょくじ']`

- shared-tail signal (template-generation):
  - tail `ょくじ`: `['おいしい しょくじ', 'からい しょくじ', 'にほんの しょくじ']`

### おべんとう (`n5.vocab.16-food-and-drink-genera.おべんとう`)
current particle_examples: `['おべんとうを たべる', 'おべんとうを つくる', 'おいしい おべんとう', 'おべんとうが すき', 'おべんとうを かう', 'からい おべんとう', 'おべんとうを ちゅうもんする', 'にほんの おべんとう']`

- shared-tail signal (template-generation):
  - tail `んとう`: `['おいしい おべんとう', 'からい おべんとう', 'にほんの おべんとう']`

### おかし (`n5.vocab.16-food-and-drink-genera.おかし`)
current particle_examples: `['おかしを たべる', 'おかしを つくる', 'おいしい おかし', 'おかしが すき', 'おかしを かう', 'からい おかし', 'おかしを ちゅうもんする', 'にほんの おかし']`

- shared-tail signal (template-generation):
  - tail `おかし`: `['おいしい おかし', 'からい おかし', 'にほんの おかし']`

### たまご (`n5.vocab.17-food-items.たまご`)
current particle_examples: `['たまごを たべる', 'たまごを つくる', 'おいしい たまご', 'たまごが すき', 'たまごを かう', 'からい たまご', 'たまごを ちゅうもんする', 'にほんの たまご']`

- shared-tail signal (template-generation):
  - tail `たまご`: `['おいしい たまご', 'からい たまご', 'にほんの たまご']`

### にく (`n5.vocab.17-food-items.にく`)
current particle_examples: `['にくを たべる', 'にくを つくる', 'おいしい にく', 'にくが すき', 'にくを かう', 'からい にく', 'にくを ちゅうもんする', 'にほんの にく']`

- shared-tail signal (template-generation):
  - tail ` にく`: `['おいしい にく', 'からい にく', 'にほんの にく']`

### ぎゅうにく (`n5.vocab.17-food-items.ぎゅうにく`)
current particle_examples: `['ぎゅうにくを たべる', 'ぎゅうにくを つくる', 'おいしい ぎゅうにく', 'ぎゅうにくが すき', 'ぎゅうにくを かう', 'からい ぎゅうにく', 'ぎゅうにくを ちゅうもんする', 'にほんの ぎゅうにく']`

- shared-tail signal (template-generation):
  - tail `うにく`: `['おいしい ぎゅうにく', 'からい ぎゅうにく', 'にほんの ぎゅうにく']`

### ぶたにく (`n5.vocab.17-food-items.ぶたにく`)
current particle_examples: `['ぶたにくを たべる', 'ぶたにくを つくる', 'おいしい ぶたにく', 'ぶたにくが すき', 'ぶたにくを かう', 'からい ぶたにく', 'ぶたにくを ちゅうもんする', 'にほんの ぶたにく']`

- shared-tail signal (template-generation):
  - tail `たにく`: `['おいしい ぶたにく', 'からい ぶたにく', 'にほんの ぶたにく']`

### とりにく (`n5.vocab.17-food-items.とりにく`)
current particle_examples: `['とりにくを たべる', 'とりにくを つくる', 'おいしい とりにく', 'とりにくが すき', 'とりにくを かう', 'からい とりにく', 'とりにくを ちゅうもんする', 'にほんの とりにく']`

- shared-tail signal (template-generation):
  - tail `りにく`: `['おいしい とりにく', 'からい とりにく', 'にほんの とりにく']`

### やさい (`n5.vocab.17-food-items.やさい`)
current particle_examples: `['やさいを たべる', 'やさいを つくる', 'おいしい やさい', 'やさいが すき', 'やさいを かう', 'からい やさい', 'やさいを ちゅうもんする', 'にほんの やさい']`

- shared-tail signal (template-generation):
  - tail `やさい`: `['おいしい やさい', 'からい やさい', 'にほんの やさい']`

### くだもの (`n5.vocab.17-food-items.くだもの`)
current particle_examples: `['くだものを たべる', 'くだものを つくる', 'おいしい くだもの', 'くだものが すき', 'くだものを かう', 'からい くだもの', 'くだものを ちゅうもんする', 'にほんの くだもの']`

- shared-tail signal (template-generation):
  - tail `だもの`: `['おいしい くだもの', 'からい くだもの', 'にほんの くだもの']`

### りんご (`n5.vocab.17-food-items.りんご`)
current particle_examples: `['りんごを たべる', 'りんごを つくる', 'おいしい りんご', 'りんごが すき', 'りんごを かう', 'からい りんご', 'りんごを ちゅうもんする', 'にほんの りんご']`

- shared-tail signal (template-generation):
  - tail `りんご`: `['おいしい りんご', 'からい りんご', 'にほんの りんご']`

### みかん (`n5.vocab.17-food-items.みかん`)
current particle_examples: `['みかんを たべる', 'みかんを つくる', 'おいしい みかん', 'みかんが すき', 'みかんを かう', 'からい みかん', 'みかんを ちゅうもんする', 'にほんの みかん']`

- shared-tail signal (template-generation):
  - tail `みかん`: `['おいしい みかん', 'からい みかん', 'にほんの みかん']`

### バナナ (`n5.vocab.17-food-items.バナナ`)
current particle_examples: `['バナナを たべる', 'きいろい バナナ', 'おいしい バナナ', 'バナナを かう', 'たくさんの バナナ', 'バナナの あじ']`

- shared-tail signal (template-generation):
  - tail `バナナ`: `['きいろい バナナ', 'おいしい バナナ', 'たくさんの バナナ']`

### いちご (`n5.vocab.17-food-items.いちご`)
current particle_examples: `['いちごを かう', 'いちごを つかう', 'あたらしい いちご', 'たかい いちご', 'いちごを ください', 'いちごは どこ', 'いちごを みる', 'やすい いちご']`

- shared-tail signal (template-generation):
  - tail `いちご`: `['あたらしい いちご', 'たかい いちご', 'やすい いちご']`

### ぶどう (`n5.vocab.17-food-items.ぶどう`)
current particle_examples: `['ぶどうを かう', 'ぶどうを つかう', 'あたらしい ぶどう', 'たかい ぶどう', 'ぶどうを ください', 'ぶどうは どこ', 'ぶどうを みる', 'やすい ぶどう']`

- shared-tail signal (template-generation):
  - tail `ぶどう`: `['あたらしい ぶどう', 'たかい ぶどう', 'やすい ぶどう']`

### レモン (`n5.vocab.17-food-items.レモン`)
current particle_examples: `['レモンを かう', 'レモンを つかう', 'あたらしい レモン', 'たかい レモン', 'レモンを ください', 'レモンは どこ', 'レモンを みる', 'やすい レモン']`

- shared-tail signal (template-generation):
  - tail `レモン`: `['あたらしい レモン', 'たかい レモン', 'やすい レモン']`

### だいこん (`n5.vocab.17-food-items.だいこん`)
current particle_examples: `['だいこんを かう', 'だいこんを つかう', 'あたらしい だいこん', 'たかい だいこん', 'だいこんを ください', 'だいこんは どこ', 'だいこんを みる', 'やすい だいこん']`

- shared-tail signal (template-generation):
  - tail `いこん`: `['あたらしい だいこん', 'たかい だいこん', 'やすい だいこん']`

### にんじん (`n5.vocab.17-food-items.にんじん`)
current particle_examples: `['にんじんを かう', 'にんじんを つかう', 'あたらしい にんじん', 'たかい にんじん', 'にんじんを ください', 'にんじんは どこ', 'にんじんを みる', 'やすい にんじん']`

- shared-tail signal (template-generation):
  - tail `んじん`: `['あたらしい にんじん', 'たかい にんじん', 'やすい にんじん']`

### たまねぎ (`n5.vocab.17-food-items.たまねぎ`)
current particle_examples: `['たまねぎを かう', 'たまねぎを つかう', 'あたらしい たまねぎ', 'たかい たまねぎ', 'たまねぎを ください', 'たまねぎは どこ', 'たまねぎを みる', 'やすい たまねぎ']`

- shared-tail signal (template-generation):
  - tail `まねぎ`: `['あたらしい たまねぎ', 'たかい たまねぎ', 'やすい たまねぎ']`

### じゃがいも (`n5.vocab.17-food-items.じゃがいも`)
current particle_examples: `['じゃがいもを かう', 'じゃがいもを つかう', 'あたらしい じゃがいも', 'たかい じゃがいも', 'じゃがいもを ください', 'じゃがいもは どこ', 'じゃがいもを みる', 'やすい じゃがいも']`

- shared-tail signal (template-generation):
  - tail `がいも`: `['あたらしい じゃがいも', 'たかい じゃがいも', 'やすい じゃがいも']`

### トマト (`n5.vocab.17-food-items.トマト`)
current particle_examples: `['トマトを かう', 'あかい トマト', 'おいしい トマト', 'トマトの サラダ', 'トマトを たべる', '小さい トマト']`

- shared-tail signal (template-generation):
  - tail `トマト`: `['あかい トマト', 'おいしい トマト', '小さい トマト']`

### きゅうり (`n5.vocab.17-food-items.きゅうり`)
current particle_examples: `['きゅうりを かう', 'きゅうりを つかう', 'あたらしい きゅうり', 'たかい きゅうり', 'きゅうりを ください', 'きゅうりは どこ', 'きゅうりを みる', 'やすい きゅうり']`

- shared-tail signal (template-generation):
  - tail `ゅうり`: `['あたらしい きゅうり', 'たかい きゅうり', 'やすい きゅうり']`

### キャベツ (`n5.vocab.17-food-items.キャベツ`)
current particle_examples: `['キャベツを かう', 'キャベツを つかう', 'あたらしい キャベツ', 'たかい キャベツ', 'キャベツを ください', 'キャベツは どこ', 'キャベツを みる', 'やすい キャベツ']`

- shared-tail signal (template-generation):
  - tail `ャベツ`: `['あたらしい キャベツ', 'たかい キャベツ', 'やすい キャベツ']`

### しお (`n5.vocab.17-food-items.しお`)
current particle_examples: `['しおを かう', 'しおを つかう', 'あたらしい しお', 'たかい しお', 'しおを ください', 'しおは どこ', 'しおを みる', 'やすい しお']`

- shared-tail signal (template-generation):
  - tail ` しお`: `['あたらしい しお', 'たかい しお', 'やすい しお']`

### さとう (`n5.vocab.17-food-items.さとう`)
current particle_examples: `['さとうを かう', 'さとうを つかう', 'あたらしい さとう', 'たかい さとう', 'さとうを ください', 'さとうは どこ', 'さとうを みる', 'やすい さとう']`

- shared-tail signal (template-generation):
  - tail `さとう`: `['あたらしい さとう', 'たかい さとう', 'やすい さとう']`

### しょうゆ (`n5.vocab.17-food-items.しょうゆ`)
current particle_examples: `['しょうゆを かう', 'しょうゆを つかう', 'あたらしい しょうゆ', 'たかい しょうゆ', 'しょうゆを ください', 'しょうゆは どこ', 'しょうゆを みる', 'やすい しょうゆ']`

- shared-tail signal (template-generation):
  - tail `ょうゆ`: `['あたらしい しょうゆ', 'たかい しょうゆ', 'やすい しょうゆ']`

### みそ (`n5.vocab.17-food-items.みそ`)
current particle_examples: `['みそを かう', 'みそを つかう', 'あたらしい みそ', 'たかい みそ', 'みそを ください', 'みそは どこ', 'みそを みる', 'やすい みそ']`

- shared-tail signal (template-generation):
  - tail ` みそ`: `['あたらしい みそ', 'たかい みそ', 'やすい みそ']`

### バター (`n5.vocab.17-food-items.バター`)
current particle_examples: `['バターを かう', 'バターを つかう', 'あたらしい バター', 'たかい バター', 'バターを ください', 'バターは どこ', 'バターを みる', 'やすい バター']`

- shared-tail signal (template-generation):
  - tail `バター`: `['あたらしい バター', 'たかい バター', 'やすい バター']`

### すし (`n5.vocab.17-food-items.すし`)
current particle_examples: `['すしを たべる', 'すしを つくる', 'おいしい すし', 'すしが すき', 'すしを かう', 'からい すし', 'すしを ちゅうもんする', 'にほんの すし']`

- shared-tail signal (template-generation):
  - tail ` すし`: `['おいしい すし', 'からい すし', 'にほんの すし']`

### 天ぷら (`n5.vocab.17-food-items.天ぷら`)
reading: `てんぷら`  
current particle_examples: `['天ぷらを たべる', '天ぷらを つくる', 'おいしい 天ぷら', '天ぷらが すき', '天ぷらを かう', 'からい 天ぷら', '天ぷらを ちゅうもんする', 'にほんの 天ぷら']`

- shared-tail signal (template-generation):
  - tail `天ぷら`: `['おいしい 天ぷら', 'からい 天ぷら', 'にほんの 天ぷら']`

### カレー (`n5.vocab.17-food-items.カレー`)
current particle_examples: `['カレーを たべる', 'カレーを つくる', 'おいしい カレー', 'カレーが すき', 'カレーを かう', 'からい カレー', 'カレーを ちゅうもんする', 'にほんの カレー']`

- shared-tail signal (template-generation):
  - tail `カレー`: `['おいしい カレー', 'からい カレー', 'にほんの カレー']`

### ラーメン (`n5.vocab.17-food-items.ラーメン`)
current particle_examples: `['ラーメンを たべる', 'おいしい ラーメン', 'ラーメンの みせ', 'あつい ラーメン', 'ラーメンの あじ', '日本の ラーメン']`

- shared-tail signal (template-generation):
  - tail `ーメン`: `['おいしい ラーメン', 'あつい ラーメン', '日本の ラーメン']`

### うどん (`n5.vocab.17-food-items.うどん`)
current particle_examples: `['うどんを たべる', 'うどんを つくる', 'おいしい うどん', 'うどんが すき', 'うどんを かう', 'からい うどん', 'うどんを ちゅうもんする', 'にほんの うどん']`

- shared-tail signal (template-generation):
  - tail `うどん`: `['おいしい うどん', 'からい うどん', 'にほんの うどん']`

### そば (`n5.vocab.17-food-items.そば`)
current particle_examples: `['いえの そば', 'えきの そば', 'そばを たべる', 'そばに いる', 'おいしい そば', 'そばの みせ']`

- shared-tail signal (template-generation):
  - tail ` そば`: `['いえの そば', 'えきの そば', 'おいしい そば']`

### ハンバーガー (`n5.vocab.17-food-items.ハンバーガー`)
current particle_examples: `['ハンバーガーを かう', 'ハンバーガーを つかう', 'あたらしい ハンバーガー', 'たかい ハンバーガー', 'ハンバーガーを ください', 'ハンバーガーは どこ', 'ハンバーガーを みる', 'やすい ハンバーガー']`

- shared-tail signal (template-generation):
  - tail `ーガー`: `['あたらしい ハンバーガー', 'たかい ハンバーガー', 'やすい ハンバーガー']`

### サンドイッチ (`n5.vocab.17-food-items.サンドイッチ`)
current particle_examples: `['サンドイッチを かう', 'サンドイッチを つかう', 'あたらしい サンドイッチ', 'たかい サンドイッチ', 'サンドイッチを ください', 'サンドイッチは どこ', 'サンドイッチを みる', 'やすい サンドイッチ']`

- shared-tail signal (template-generation):
  - tail `イッチ`: `['あたらしい サンドイッチ', 'たかい サンドイッチ', 'やすい サンドイッチ']`

### サラダ (`n5.vocab.17-food-items.サラダ`)
current particle_examples: `['サラダを かう', 'サラダを つかう', 'あたらしい サラダ', 'たかい サラダ', 'サラダを ください', 'サラダは どこ', 'サラダを みる', 'やすい サラダ']`

- shared-tail signal (template-generation):
  - tail `サラダ`: `['あたらしい サラダ', 'たかい サラダ', 'やすい サラダ']`

### スープ (`n5.vocab.17-food-items.スープ`)
current particle_examples: `['スープを のむ', 'あつい スープ', 'おいしい スープ', 'やさいの スープ', 'スープの あじ', 'やわらかい スープ']`

- shared-tail signal (template-generation):
  - tail `スープ`: `['あつい スープ', 'おいしい スープ', 'やさいの スープ', 'やわらかい スープ']`

### ケーキ (`n5.vocab.17-food-items.ケーキ`)
current particle_examples: `['ケーキを たべる', 'ケーキを つくる', 'おいしい ケーキ', 'ケーキが すき', 'ケーキを かう', 'からい ケーキ', 'ケーキを ちゅうもんする', 'にほんの ケーキ']`

- shared-tail signal (template-generation):
  - tail `ケーキ`: `['おいしい ケーキ', 'からい ケーキ', 'にほんの ケーキ']`

### アイスクリーム (`n5.vocab.17-food-items.アイスクリーム`)
current particle_examples: `['アイスクリームを たべる', 'アイスクリームを つくる', 'おいしい アイスクリーム', 'アイスクリームが すき', 'アイスクリームを かう', 'からい アイスクリーム', 'アイスクリームを ちゅうもんする', 'にほんの アイスクリーム']`

- shared-tail signal (template-generation):
  - tail `リーム`: `['おいしい アイスクリーム', 'からい アイスクリーム', 'にほんの アイスクリーム']`

### ぎゅうにゅう (`n5.vocab.18-drinks.ぎゅうにゅう`)
current particle_examples: `['ぎゅうにゅうを たべる', 'ぎゅうにゅうを つくる', 'おいしい ぎゅうにゅう', 'ぎゅうにゅうが すき', 'ぎゅうにゅうを かう', 'からい ぎゅうにゅう', 'ぎゅうにゅうを ちゅうもんする', 'にほんの ぎゅうにゅう']`

- shared-tail signal (template-generation):
  - tail `にゅう`: `['おいしい ぎゅうにゅう', 'からい ぎゅうにゅう', 'にほんの ぎゅうにゅう']`

### ジュース (`n5.vocab.18-drinks.ジュース`)
current particle_examples: `['ジュースを のむ', 'おいしい ジュース', 'りんごの ジュース', 'ジュースを かう', 'つめたい ジュース', 'ジュースの あじ']`

- shared-tail signal (template-generation):
  - tail `ュース`: `['おいしい ジュース', 'りんごの ジュース', 'つめたい ジュース']`

### ワイン (`n5.vocab.18-drinks.ワイン`)
current particle_examples: `['ワインを のむ', 'あかい ワイン', 'しろい ワイン', 'ワインの あじ', 'ワインを かう', 'おいしい ワイン']`

- shared-tail signal (template-generation):
  - tail `ワイン`: `['あかい ワイン', 'しろい ワイン', 'おいしい ワイン']`

### さら (`n5.vocab.19-tableware-and-cooking.さら`)
current particle_examples: `['さらを かう', 'さらを つかう', 'あたらしい さら', 'たかい さら', 'さらを ください', 'さらは どこ', 'さらを みる', 'やすい さら']`

- shared-tail signal (template-generation):
  - tail ` さら`: `['あたらしい さら', 'たかい さら', 'やすい さら']`

### おさら (`n5.vocab.19-tableware-and-cooking.おさら`)
current particle_examples: `['おさらを かう', 'おさらを つかう', 'あたらしい おさら', 'たかい おさら', 'おさらを ください', 'おさらは どこ', 'おさらを みる', 'やすい おさら']`

- shared-tail signal (template-generation):
  - tail `おさら`: `['あたらしい おさら', 'たかい おさら', 'やすい おさら']`

### ちゃわん (`n5.vocab.19-tableware-and-cooking.ちゃわん`)
current particle_examples: `['ちゃわんを たべる', 'ちゃわんを つくる', 'おいしい ちゃわん', 'ちゃわんが すき', 'ちゃわんを かう', 'からい ちゃわん', 'ちゃわんを ちゅうもんする', 'にほんの ちゃわん']`

- shared-tail signal (template-generation):
  - tail `ゃわん`: `['おいしい ちゃわん', 'からい ちゃわん', 'にほんの ちゃわん']`

### おわん (`n5.vocab.19-tableware-and-cooking.おわん`)
current particle_examples: `['おわんを かう', 'おわんを つかう', 'あたらしい おわん', 'たかい おわん', 'おわんを ください', 'おわんは どこ', 'おわんを みる', 'やすい おわん']`

- shared-tail signal (template-generation):
  - tail `おわん`: `['あたらしい おわん', 'たかい おわん', 'やすい おわん']`

### はし (`n5.vocab.19-tableware-and-cooking.はし`)
current particle_examples: `['はしに いく', 'はしで あう', 'はしから くる', 'はしの まえに', 'はしが ある', 'はしは ちかい', 'はしまで あるく', 'はしに つく']`

- template-shape hits:
  - shape `に いく` in `はしに いく`

### スプーン (`n5.vocab.19-tableware-and-cooking.スプーン`)
current particle_examples: `['スプーンを かう', 'スプーンを つかう', 'あたらしい スプーン', 'たかい スプーン', 'スプーンを ください', 'スプーンは どこ', 'スプーンを みる', 'やすい スプーン']`

- shared-tail signal (template-generation):
  - tail `プーン`: `['あたらしい スプーン', 'たかい スプーン', 'やすい スプーン']`

### フォーク (`n5.vocab.19-tableware-and-cooking.フォーク`)
current particle_examples: `['フォークを かう', 'フォークを つかう', 'あたらしい フォーク', 'たかい フォーク', 'フォークを ください', 'フォークは どこ', 'フォークを みる', 'やすい フォーク']`

- shared-tail signal (template-generation):
  - tail `ォーク`: `['あたらしい フォーク', 'たかい フォーク', 'やすい フォーク']`

### ナイフ (`n5.vocab.19-tableware-and-cooking.ナイフ`)
current particle_examples: `['ナイフを つかう', 'ちいさい ナイフ', 'ナイフで きる', 'あたらしい ナイフ', 'ナイフの は', 'パンの ナイフ']`

- shared-tail signal (template-generation):
  - tail `ナイフ`: `['ちいさい ナイフ', 'あたらしい ナイフ', 'パンの ナイフ']`

### コップ (`n5.vocab.19-tableware-and-cooking.コップ`)
current particle_examples: `['コップを かう', 'コップを つかう', 'あたらしい コップ', 'たかい コップ', 'コップを ください', 'コップは どこ', 'コップを みる', 'やすい コップ']`

- shared-tail signal (template-generation):
  - tail `コップ`: `['あたらしい コップ', 'たかい コップ', 'やすい コップ']`

### カップ (`n5.vocab.19-tableware-and-cooking.カップ`)
current particle_examples: `['カップを かう', 'コーヒーの カップ', '大きい カップ', 'おちゃの カップ', 'カップに いれる', 'おしゃれな カップ']`

- shared-tail signal (template-generation):
  - tail `カップ`: `['コーヒーの カップ', '大きい カップ', 'おちゃの カップ', 'おしゃれな カップ']`

### れいぞうこ (`n5.vocab.19-tableware-and-cooking.れいぞうこ`)
current particle_examples: `['れいぞうこを かう', 'れいぞうこを つかう', 'あたらしい れいぞうこ', 'たかい れいぞうこ', 'れいぞうこを ください', 'れいぞうこは どこ', 'れいぞうこを みる', 'やすい れいぞうこ']`

- shared-tail signal (template-generation):
  - tail `ぞうこ`: `['あたらしい れいぞうこ', 'たかい れいぞうこ', 'やすい れいぞうこ']`

### なべ (`n5.vocab.19-tableware-and-cooking.なべ`)
current particle_examples: `['なべを かう', 'なべを つかう', 'あたらしい なべ', 'たかい なべ', 'なべを ください', 'なべは どこ', 'なべを みる', 'やすい なべ']`

- shared-tail signal (template-generation):
  - tail ` なべ`: `['あたらしい なべ', 'たかい なべ', 'やすい なべ']`

### いろ (`n5.vocab.20-colors.いろ`)
current particle_examples: `['いろを かう', 'いろを つかう', 'あたらしい いろ', 'たかい いろ', 'いろを ください', 'いろは どこ', 'いろを みる', 'やすい いろ']`

- shared-tail signal (template-generation):
  - tail ` いろ`: `['あたらしい いろ', 'たかい いろ', 'やすい いろ']`

### 白 (`n5.vocab.20-colors.白`)
reading: `しろ`  
current particle_examples: `['白を かう', '白を つかう', 'あたらしい 白', 'たかい 白', '白を ください', '白は どこ', '白を みる', 'やすい 白']`

- shared-tail signal (template-generation):
  - tail `い 白`: `['あたらしい 白', 'たかい 白', 'やすい 白']`

### くろ (`n5.vocab.20-colors.くろ`)
current particle_examples: `['くろを かう', 'くろを つかう', 'あたらしい くろ', 'たかい くろ', 'くろを ください', 'くろは どこ', 'くろを みる', 'やすい くろ']`

- shared-tail signal (template-generation):
  - tail ` くろ`: `['あたらしい くろ', 'たかい くろ', 'やすい くろ']`

### あか (`n5.vocab.20-colors.あか`)
current particle_examples: `['あかを かう', 'あかを つかう', 'あたらしい あか', 'たかい あか', 'あかを ください', 'あかは どこ', 'あかを みる', 'やすい あか']`

- shared-tail signal (template-generation):
  - tail ` あか`: `['あたらしい あか', 'たかい あか', 'やすい あか']`

### あお (`n5.vocab.20-colors.あお`)
current particle_examples: `['あおを かう', 'あおを つかう', 'あたらしい あお', 'たかい あお', 'あおを ください', 'あおは どこ', 'あおを みる', 'やすい あお']`

- shared-tail signal (template-generation):
  - tail ` あお`: `['あたらしい あお', 'たかい あお', 'やすい あお']`

### きいろ (`n5.vocab.20-colors.きいろ`)
current particle_examples: `['きいろを かう', 'きいろを つかう', 'あたらしい きいろ', 'たかい きいろ', 'きいろを ください', 'きいろは どこ', 'きいろを みる', 'やすい きいろ']`

- shared-tail signal (template-generation):
  - tail `きいろ`: `['あたらしい きいろ', 'たかい きいろ', 'やすい きいろ']`

### ちゃいろ (`n5.vocab.20-colors.ちゃいろ`)
current particle_examples: `['ちゃいろを かう', 'ちゃいろを つかう', 'あたらしい ちゃいろ', 'たかい ちゃいろ', 'ちゃいろを ください', 'ちゃいろは どこ', 'ちゃいろを みる', 'やすい ちゃいろ']`

- shared-tail signal (template-generation):
  - tail `ゃいろ`: `['あたらしい ちゃいろ', 'たかい ちゃいろ', 'やすい ちゃいろ']`

### みどり (`n5.vocab.20-colors.みどり`)
current particle_examples: `['みどりを かう', 'みどりを つかう', 'あたらしい みどり', 'たかい みどり', 'みどりを ください', 'みどりは どこ', 'みどりを みる', 'やすい みどり']`

- shared-tail signal (template-generation):
  - tail `みどり`: `['あたらしい みどり', 'たかい みどり', 'やすい みどり']`

### ふく (`n5.vocab.21-clothing-and-accessor.ふく`)
current particle_examples: `['ふくを かう', 'ふくを つかう', 'あたらしい ふく', 'たかい ふく', 'ふくを ください', 'ふくは どこ', 'ふくを みる', 'やすい ふく']`

- shared-tail signal (template-generation):
  - tail ` ふく`: `['あたらしい ふく', 'たかい ふく', 'やすい ふく']`

### ようふく (`n5.vocab.21-clothing-and-accessor.ようふく`)
current particle_examples: `['ようふくを かう', 'ようふくを つかう', 'あたらしい ようふく', 'たかい ようふく', 'ようふくを ください', 'ようふくは どこ', 'ようふくを みる', 'やすい ようふく']`

- shared-tail signal (template-generation):
  - tail `うふく`: `['あたらしい ようふく', 'たかい ようふく', 'やすい ようふく']`

### きもの (`n5.vocab.21-clothing-and-accessor.きもの`)
current particle_examples: `['きものを かう', 'きものを つかう', 'あたらしい きもの', 'たかい きもの', 'きものを ください', 'きものは どこ', 'きものを みる', 'やすい きもの']`

- shared-tail signal (template-generation):
  - tail `きもの`: `['あたらしい きもの', 'たかい きもの', 'やすい きもの']`

### うわぎ (`n5.vocab.21-clothing-and-accessor.うわぎ`)
current particle_examples: `['うわぎを かう', 'うわぎを つかう', 'あたらしい うわぎ', 'たかい うわぎ', 'うわぎを ください', 'うわぎは どこ', 'うわぎを みる', 'やすい うわぎ']`

- shared-tail signal (template-generation):
  - tail `うわぎ`: `['あたらしい うわぎ', 'たかい うわぎ', 'やすい うわぎ']`

### コート (`n5.vocab.21-clothing-and-accessor.コート`)
current particle_examples: `['コートに いく', 'コートで あう', 'コートから くる', 'コートの まえに', 'コートが ある', 'コートは ちかい', 'コートまで あるく', 'コートに つく']`

- template-shape hits:
  - shape `に いく` in `コートに いく`

### セーター (`n5.vocab.21-clothing-and-accessor.セーター`)
current particle_examples: `['セーターを かう', 'セーターを つかう', 'あたらしい セーター', 'たかい セーター', 'セーターを ください', 'セーターは どこ', 'セーターを みる', 'やすい セーター']`

- shared-tail signal (template-generation):
  - tail `ーター`: `['あたらしい セーター', 'たかい セーター', 'やすい セーター']`

### シャツ (`n5.vocab.21-clothing-and-accessor.シャツ`)
current particle_examples: `['ワイシャツを', 'ワイシャツは', 'シャツを きる', '新しい シャツ', 'しろい シャツ', 'シャツを かう', 'あおい シャツ', 'Tシャツ']`

- shared-tail signal (template-generation):
  - tail `シャツ`: `['新しい シャツ', 'しろい シャツ', 'あおい シャツ', 'Tシャツ']`

### Tシャツ (`n5.vocab.21-clothing-and-accessor.Tシャツ`)
reading: `ティーシャツ`  
current particle_examples: `['Tシャツを きる', '新しい Tシャツ', 'Tシャツを かう', 'しろい Tシャツ', 'あかい Tシャツ', 'Tシャツの デザイン']`

- shared-tail signal (template-generation):
  - tail `シャツ`: `['新しい Tシャツ', 'しろい Tシャツ', 'あかい Tシャツ']`

### ワイシャツ (`n5.vocab.21-clothing-and-accessor.ワイシャツ`)
current particle_examples: `['ワイシャツを かう', 'ワイシャツを つかう', 'あたらしい ワイシャツ', 'たかい ワイシャツ', 'ワイシャツを ください', 'ワイシャツは どこ', 'ワイシャツを みる', 'やすい ワイシャツ']`

- shared-tail signal (template-generation):
  - tail `シャツ`: `['あたらしい ワイシャツ', 'たかい ワイシャツ', 'やすい ワイシャツ']`

### ズボン (`n5.vocab.21-clothing-and-accessor.ズボン`)
current particle_examples: `['ズボンを かう', 'ズボンを つかう', 'あたらしい ズボン', 'たかい ズボン', 'ズボンを ください', 'ズボンは どこ', 'ズボンを みる', 'やすい ズボン']`

- shared-tail signal (template-generation):
  - tail `ズボン`: `['あたらしい ズボン', 'たかい ズボン', 'やすい ズボン']`

### スカート (`n5.vocab.21-clothing-and-accessor.スカート`)
current particle_examples: `['スカートを はく', '新しい スカート', 'みじかい スカート', 'ながい スカート', 'スカートを かう', 'あおい スカート']`

- shared-tail signal (template-generation):
  - tail `カート`: `['新しい スカート', 'みじかい スカート', 'ながい スカート', 'あおい スカート']`

### ネクタイ (`n5.vocab.21-clothing-and-accessor.ネクタイ`)
current particle_examples: `['ネクタイを かう', 'ネクタイを つかう', 'あたらしい ネクタイ', 'たかい ネクタイ', 'ネクタイを ください', 'ネクタイは どこ', 'ネクタイを みる', 'やすい ネクタイ']`

- shared-tail signal (template-generation):
  - tail `クタイ`: `['あたらしい ネクタイ', 'たかい ネクタイ', 'やすい ネクタイ']`

### ぼうし (`n5.vocab.21-clothing-and-accessor.ぼうし`)
current particle_examples: `['ぼうしを かう', 'ぼうしを つかう', 'あたらしい ぼうし', 'たかい ぼうし', 'ぼうしを ください', 'ぼうしは どこ', 'ぼうしを みる', 'やすい ぼうし']`

- shared-tail signal (template-generation):
  - tail `ぼうし`: `['あたらしい ぼうし', 'たかい ぼうし', 'やすい ぼうし']`

### くつ (`n5.vocab.21-clothing-and-accessor.くつ`)
current particle_examples: `['くつを かう', 'くつを つかう', 'あたらしい くつ', 'たかい くつ', 'くつを ください', 'くつは どこ', 'くつを みる', 'やすい くつ']`

- shared-tail signal (template-generation):
  - tail ` くつ`: `['あたらしい くつ', 'たかい くつ', 'やすい くつ']`

### くつした (`n5.vocab.21-clothing-and-accessor.くつした`)
current particle_examples: `['くつしたを かう', 'くつしたを つかう', 'あたらしい くつした', 'たかい くつした', 'くつしたを ください', 'くつしたは どこ', 'くつしたを みる', 'やすい くつした']`

- shared-tail signal (template-generation):
  - tail `つした`: `['あたらしい くつした', 'たかい くつした', 'やすい くつした']`

### かばん (`n5.vocab.21-clothing-and-accessor.かばん`)
current particle_examples: `['かばんを かう', 'かばんを つかう', 'あたらしい かばん', 'たかい かばん', 'かばんを ください', 'かばんは どこ', 'かばんを みる', 'やすい かばん']`

- shared-tail signal (template-generation):
  - tail `かばん`: `['あたらしい かばん', 'たかい かばん', 'やすい かばん']`

### さいふ (`n5.vocab.21-clothing-and-accessor.さいふ`)
current particle_examples: `['さいふを かう', 'さいふを つかう', 'あたらしい さいふ', 'たかい さいふ', 'さいふを ください', 'さいふは どこ', 'さいふを みる', 'やすい さいふ']`

- shared-tail signal (template-generation):
  - tail `さいふ`: `['あたらしい さいふ', 'たかい さいふ', 'やすい さいふ']`

### めがね (`n5.vocab.21-clothing-and-accessor.めがね`)
current particle_examples: `['めがねを かう', 'めがねを つかう', 'あたらしい めがね', 'たかい めがね', 'めがねを ください', 'めがねは どこ', 'めがねを みる', 'やすい めがね']`

- shared-tail signal (template-generation):
  - tail `めがね`: `['あたらしい めがね', 'たかい めがね', 'やすい めがね']`

### かさ (`n5.vocab.21-clothing-and-accessor.かさ`)
current particle_examples: `['かさを かう', 'かさを つかう', 'あたらしい かさ', 'たかい かさ', 'かさを ください', 'かさは どこ', 'かさを みる', 'やすい かさ']`

- shared-tail signal (template-generation):
  - tail ` かさ`: `['あたらしい かさ', 'たかい かさ', 'やすい かさ']`

### お金 (`n5.vocab.22-money-and-shopping.お金`)
reading: `おかね`  
current particle_examples: `['お金を かう', 'お金を つかう', 'あたらしい お金', 'たかい お金', 'お金を ください', 'お金は どこ', 'お金を みる', 'やすい お金']`

- shared-tail signal (template-generation):
  - tail ` お金`: `['あたらしい お金', 'たかい お金', 'やすい お金']`

### 円 (`n5.vocab.22-money-and-shopping.円`)
reading: `えん`  
current particle_examples: `['円を かう', '円を つかう', 'あたらしい 円', 'たかい 円', '円を ください', '円は どこ', '円を みる', 'やすい 円']`

- shared-tail signal (template-generation):
  - tail `い 円`: `['あたらしい 円', 'たかい 円', 'やすい 円']`

### ねだん (`n5.vocab.22-money-and-shopping.ねだん`)
current particle_examples: `['ねだんを たべる', 'ねだんを つくる', 'おいしい ねだん', 'ねだんが すき', 'ねだんを かう', 'からい ねだん', 'ねだんを ちゅうもんする', 'にほんの ねだん']`

- shared-tail signal (template-generation):
  - tail `ねだん`: `['おいしい ねだん', 'からい ねだん', 'にほんの ねだん']`

### きっぷ (`n5.vocab.22-money-and-shopping.きっぷ`)
current particle_examples: `['きっぷを かう', 'きっぷを つかう', 'あたらしい きっぷ', 'たかい きっぷ', 'きっぷを ください', 'きっぷは どこ', 'きっぷを みる', 'やすい きっぷ']`

- shared-tail signal (template-generation):
  - tail `きっぷ`: `['あたらしい きっぷ', 'たかい きっぷ', 'やすい きっぷ']`

### きって (`n5.vocab.22-money-and-shopping.きって`)
current particle_examples: `['きってに いく', 'きってで あう', 'きってから くる', 'きっての まえに', 'きってが ある', 'きっては ちかい', 'きってまで あるく', 'きってに つく', 'きってを かう', 'きってを つかう', 'あたらしい きって', 'たかい きって', 'きってを ください', 'きっては どこ', 'きってを みる', 'やすい きって']`

- template-shape hits:
  - shape `に いく` in `きってに いく`
- shared-tail signal (template-generation):
  - tail `きって`: `['あたらしい きって', 'たかい きって', 'やすい きって']`

### はがき (`n5.vocab.22-money-and-shopping.はがき`)
current particle_examples: `['はがきを かう', 'はがきを つかう', 'あたらしい はがき', 'たかい はがき', 'はがきを ください', 'はがきは どこ', 'はがきを みる', 'やすい はがき']`

- shared-tail signal (template-generation):
  - tail `はがき`: `['あたらしい はがき', 'たかい はがき', 'やすい はがき']`

### ふうとう (`n5.vocab.22-money-and-shopping.ふうとう`)
current particle_examples: `['ふうとうを かう', 'ふうとうを つかう', 'あたらしい ふうとう', 'たかい ふうとう', 'ふうとうを ください', 'ふうとうは どこ', 'ふうとうを みる', 'やすい ふうとう']`

- shared-tail signal (template-generation):
  - tail `うとう`: `['あたらしい ふうとう', 'たかい ふうとう', 'やすい ふうとう']`

### てがみ (`n5.vocab.22-money-and-shopping.てがみ`)
current particle_examples: `['てがみを かう', 'てがみを つかう', 'あたらしい てがみ', 'たかい てがみ', 'てがみを ください', 'てがみは どこ', 'てがみを みる', 'やすい てがみ']`

- shared-tail signal (template-generation):
  - tail `てがみ`: `['あたらしい てがみ', 'たかい てがみ', 'やすい てがみ']`

### にもつ (`n5.vocab.22-money-and-shopping.にもつ`)
current particle_examples: `['にもつを かう', 'にもつを つかう', 'あたらしい にもつ', 'たかい にもつ', 'にもつを ください', 'にもつは どこ', 'にもつを みる', 'やすい にもつ']`

- shared-tail signal (template-generation):
  - tail `にもつ`: `['あたらしい にもつ', 'たかい にもつ', 'やすい にもつ']`

### おみやげ (`n5.vocab.22-money-and-shopping.おみやげ`)
current particle_examples: `['おみやげを かう', 'おみやげを つかう', 'あたらしい おみやげ', 'たかい おみやげ', 'おみやげを ください', 'おみやげは どこ', 'おみやげを みる', 'やすい おみやげ']`

- shared-tail signal (template-generation):
  - tail `みやげ`: `['あたらしい おみやげ', 'たかい おみやげ', 'やすい おみやげ']`

### じどうしゃ (`n5.vocab.23-transport.じどうしゃ`)
current particle_examples: `['じどうしゃを かう', 'じどうしゃを つかう', 'あたらしい じどうしゃ', 'たかい じどうしゃ', 'じどうしゃを ください', 'じどうしゃは どこ', 'じどうしゃを みる', 'やすい じどうしゃ']`

- shared-tail signal (template-generation):
  - tail `うしゃ`: `['あたらしい じどうしゃ', 'たかい じどうしゃ', 'やすい じどうしゃ']`

### じてんしゃ (`n5.vocab.23-transport.じてんしゃ`)
current particle_examples: `['じてんしゃを かう', 'じてんしゃを つかう', 'あたらしい じてんしゃ', 'たかい じてんしゃ', 'じてんしゃを ください', 'じてんしゃは どこ', 'じてんしゃを みる', 'やすい じてんしゃ']`

- shared-tail signal (template-generation):
  - tail `んしゃ`: `['あたらしい じてんしゃ', 'たかい じてんしゃ', 'やすい じてんしゃ']`

### バス (`n5.vocab.23-transport.バス`)
current particle_examples: `['バスを かう', 'バスを つかう', 'あたらしい バス', 'たかい バス', 'バスを ください', 'バスは どこ', 'バスを みる', 'やすい バス']`

- shared-tail signal (template-generation):
  - tail ` バス`: `['あたらしい バス', 'たかい バス', 'やすい バス']`

### タクシー (`n5.vocab.23-transport.タクシー`)
current particle_examples: `['タクシーを かう', 'タクシーを つかう', 'あたらしい タクシー', 'たかい タクシー', 'タクシーを ください', 'タクシーは どこ', 'タクシーを みる', 'やすい タクシー']`

- shared-tail signal (template-generation):
  - tail `クシー`: `['あたらしい タクシー', 'たかい タクシー', 'やすい タクシー']`

### ちかてつ (`n5.vocab.23-transport.ちかてつ`)
current particle_examples: `['ちかてつを かう', 'ちかてつを つかう', 'あたらしい ちかてつ', 'たかい ちかてつ', 'ちかてつを ください', 'ちかてつは どこ', 'ちかてつを みる', 'やすい ちかてつ']`

- shared-tail signal (template-generation):
  - tail `かてつ`: `['あたらしい ちかてつ', 'たかい ちかてつ', 'やすい ちかてつ']`

### ひこうき (`n5.vocab.23-transport.ひこうき`)
current particle_examples: `['ひこうきを かう', 'ひこうきを つかう', 'あたらしい ひこうき', 'たかい ひこうき', 'ひこうきを ください', 'ひこうきは どこ', 'ひこうきを みる', 'やすい ひこうき']`

- shared-tail signal (template-generation):
  - tail `こうき`: `['あたらしい ひこうき', 'たかい ひこうき', 'やすい ひこうき']`

### ふね (`n5.vocab.23-transport.ふね`)
current particle_examples: `['ふねを かう', 'ふねを つかう', 'あたらしい ふね', 'たかい ふね', 'ふねを ください', 'ふねは どこ', 'ふねを みる', 'やすい ふね']`

- shared-tail signal (template-generation):
  - tail ` ふね`: `['あたらしい ふね', 'たかい ふね', 'やすい ふね']`

### しんごう (`n5.vocab.23-transport.しんごう`)
current particle_examples: `['しんごうに いく', 'しんごうで あう', 'しんごうから くる', 'しんごうの まえに', 'しんごうが ある', 'しんごうは ちかい', 'しんごうまで あるく', 'しんごうに つく']`

- template-shape hits:
  - shape `に いく` in `しんごうに いく`

### べんきょう (`n5.vocab.24-school-and-study.べんきょう`)
current particle_examples: `['べんきょうが ある', 'べんきょうが ない', 'べんきょうを いう', 'べんきょうを きく', 'いい べんきょう', 'べんきょうの とき', 'べんきょうを おもう', 'べんきょうを しる']`

- template-shape hits:
  - shape `を しる` in `べんきょうを しる`

### じゅぎょう (`n5.vocab.24-school-and-study.じゅぎょう`)
current particle_examples: `['じゅぎょうを かう', 'じゅぎょうを つかう', 'あたらしい じゅぎょう', 'たかい じゅぎょう', 'じゅぎょうを ください', 'じゅぎょうは どこ', 'じゅぎょうを みる', 'やすい じゅぎょう']`

- shared-tail signal (template-generation):
  - tail `ぎょう`: `['あたらしい じゅぎょう', 'たかい じゅぎょう', 'やすい じゅぎょう']`

### しゅくだい (`n5.vocab.24-school-and-study.しゅくだい`)
current particle_examples: `['しゅくだいに いく', 'しゅくだいで あう', 'しゅくだいから くる', 'しゅくだいの まえに', 'しゅくだいが ある', 'しゅくだいは ちかい', 'しゅくだいまで あるく', 'しゅくだいに つく']`

- template-shape hits:
  - shape `に いく` in `しゅくだいに いく`

### しけん (`n5.vocab.24-school-and-study.しけん`)
current particle_examples: `['しけんを かう', 'しけんを つかう', 'あたらしい しけん', 'たかい しけん', 'しけんを ください', 'しけんは どこ', 'しけんを みる', 'やすい しけん']`

- shared-tail signal (template-generation):
  - tail `しけん`: `['あたらしい しけん', 'たかい しけん', 'やすい しけん']`

### しつもん (`n5.vocab.24-school-and-study.しつもん`)
current particle_examples: `['しつもんが ある', 'しつもんが ない', 'しつもんを いう', 'しつもんを きく', 'いい しつもん', 'しつもんの とき', 'しつもんを おもう', 'しつもんを しる']`

- template-shape hits:
  - shape `を しる` in `しつもんを しる`

### こたえ (`n5.vocab.24-school-and-study.こたえ`)
current particle_examples: `['こたえが ある', 'こたえが ない', 'こたえを いう', 'こたえを きく', 'いい こたえ', 'こたえの とき', 'こたえを おもう', 'こたえを しる']`

- template-shape hits:
  - shape `を しる` in `こたえを しる`

### いみ (`n5.vocab.24-school-and-study.いみ`)
current particle_examples: `['いみが ある', 'いみが ない', 'いみを いう', 'いみを きく', 'いい いみ', 'いみの とき', 'いみを おもう', 'いみを しる']`

- template-shape hits:
  - shape `を しる` in `いみを しる`

### ことば (`n5.vocab.24-school-and-study.ことば`)
current particle_examples: `['日本ごの ことば', 'むずかしい ことば', 'きれいな ことば', 'ことばの いみ', 'ことばを ならう', 'やさしい ことば']`

- template-shape hits:
  - shape `を ならう` in `ことばを ならう`
- shared-tail signal (template-generation):
  - tail `ことば`: `['日本ごの ことば', 'むずかしい ことば', 'きれいな ことば', 'やさしい ことば']`

### じ (`n5.vocab.24-school-and-study.じ`)
current particle_examples: `['じが ある', 'じに いく', 'じまで まつ', 'じから はじまる', 'いま じ', 'じは はやい', 'じを まつ', 'じが おわる']`

- template-shape hits:
  - shape `に いく` in `じに いく`

### かんじ (`n5.vocab.24-school-and-study.かんじ`)
current particle_examples: `['かんじを かう', 'かんじを つかう', 'あたらしい かんじ', 'たかい かんじ', 'かんじを ください', 'かんじは どこ', 'かんじを みる', 'やすい かんじ']`

- shared-tail signal (template-generation):
  - tail `かんじ`: `['あたらしい かんじ', 'たかい かんじ', 'やすい かんじ']`

### ひらがな (`n5.vocab.24-school-and-study.ひらがな`)
current particle_examples: `['ひらがなを かう', 'ひらがなを つかう', 'あたらしい ひらがな', 'たかい ひらがな', 'ひらがなを ください', 'ひらがなは どこ', 'ひらがなを みる', 'やすい ひらがな']`

- shared-tail signal (template-generation):
  - tail `らがな`: `['あたらしい ひらがな', 'たかい ひらがな', 'やすい ひらがな']`

### カタカナ (`n5.vocab.24-school-and-study.カタカナ`)
current particle_examples: `['カタカナを かう', 'カタカナを つかう', 'あたらしい カタカナ', 'たかい カタカナ', 'カタカナを ください', 'カタカナは どこ', 'カタカナを みる', 'やすい カタカナ']`

- shared-tail signal (template-generation):
  - tail `タカナ`: `['あたらしい カタカナ', 'たかい カタカナ', 'やすい カタカナ']`

### もじ (`n5.vocab.24-school-and-study.もじ`)
current particle_examples: `['もじを かう', 'もじを つかう', 'あたらしい もじ', 'たかい もじ', 'もじを ください', 'もじは どこ', 'もじを みる', 'やすい もじ']`

- shared-tail signal (template-generation):
  - tail ` もじ`: `['あたらしい もじ', 'たかい もじ', 'やすい もじ']`

### ぶんしょう (`n5.vocab.24-school-and-study.ぶんしょう`)
current particle_examples: `['ぶんしょうを かう', 'ぶんしょうを つかう', 'あたらしい ぶんしょう', 'たかい ぶんしょう', 'ぶんしょうを ください', 'ぶんしょうは どこ', 'ぶんしょうを みる', 'やすい ぶんしょう']`

- shared-tail signal (template-generation):
  - tail `しょう`: `['あたらしい ぶんしょう', 'たかい ぶんしょう', 'やすい ぶんしょう']`

### ぶんぽう (`n5.vocab.24-school-and-study.ぶんぽう`)
current particle_examples: `['ぶんぽうを かう', 'ぶんぽうを つかう', 'あたらしい ぶんぽう', 'たかい ぶんぽう', 'ぶんぽうを ください', 'ぶんぽうは どこ', 'ぶんぽうを みる', 'やすい ぶんぽう']`

- shared-tail signal (template-generation):
  - tail `んぽう`: `['あたらしい ぶんぽう', 'たかい ぶんぽう', 'やすい ぶんぽう']`

### れい (`n5.vocab.24-school-and-study.れい`)
current particle_examples: `['れいを かう', 'れいを つかう', 'あたらしい れい', 'たかい れい', 'れいを ください', 'れいは どこ', 'れいを みる', 'やすい れい']`

- shared-tail signal (template-generation):
  - tail ` れい`: `['あたらしい れい', 'たかい れい', 'やすい れい']`

### れんしゅう (`n5.vocab.24-school-and-study.れんしゅう`)
current particle_examples: `['れんしゅうを かう', 'れんしゅうを つかう', 'あたらしい れんしゅう', 'たかい れんしゅう', 'れんしゅうを ください', 'れんしゅうは どこ', 'れんしゅうを みる', 'やすい れんしゅう']`

- shared-tail signal (template-generation):
  - tail `しゅう`: `['あたらしい れんしゅう', 'たかい れんしゅう', 'やすい れんしゅう']`

### きょうかしょ (`n5.vocab.24-school-and-study.きょうかしょ`)
current particle_examples: `['きょうかしょを かう', 'きょうかしょを つかう', 'あたらしい きょうかしょ', 'たかい きょうかしょ', 'きょうかしょを ください', 'きょうかしょは どこ', 'きょうかしょを みる', 'やすい きょうかしょ']`

- shared-tail signal (template-generation):
  - tail `かしょ`: `['あたらしい きょうかしょ', 'たかい きょうかしょ', 'やすい きょうかしょ']`

### じしょ (`n5.vocab.24-school-and-study.じしょ`)
current particle_examples: `['じしょを かう', 'じしょを つかう', 'あたらしい じしょ', 'たかい じしょ', 'じしょを ください', 'じしょは どこ', 'じしょを みる', 'やすい じしょ']`

- shared-tail signal (template-generation):
  - tail `じしょ`: `['あたらしい じしょ', 'たかい じしょ', 'やすい じしょ']`

### ざっし (`n5.vocab.24-school-and-study.ざっし`)
current particle_examples: `['ざっしを かう', 'ざっしを つかう', 'あたらしい ざっし', 'たかい ざっし', 'ざっしを ください', 'ざっしは どこ', 'ざっしを みる', 'やすい ざっし']`

- shared-tail signal (template-generation):
  - tail `ざっし`: `['あたらしい ざっし', 'たかい ざっし', 'やすい ざっし']`

### えんぴつ (`n5.vocab.24-school-and-study.えんぴつ`)
current particle_examples: `['えんぴつを かう', 'えんぴつを つかう', 'あたらしい えんぴつ', 'たかい えんぴつ', 'えんぴつを ください', 'えんぴつは どこ', 'えんぴつを みる', 'やすい えんぴつ']`

- shared-tail signal (template-generation):
  - tail `んぴつ`: `['あたらしい えんぴつ', 'たかい えんぴつ', 'やすい えんぴつ']`

### ボールペン (`n5.vocab.24-school-and-study.ボールペン`)
current particle_examples: `['ボールペンを かう', 'ボールペンを つかう', 'あたらしい ボールペン', 'たかい ボールペン', 'ボールペンを ください', 'ボールペンは どこ', 'ボールペンを みる', 'やすい ボールペン']`

- shared-tail signal (template-generation):
  - tail `ルペン`: `['あたらしい ボールペン', 'たかい ボールペン', 'やすい ボールペン']`

### まんねんひつ (`n5.vocab.24-school-and-study.まんねんひつ`)
current particle_examples: `['まんねんひつを かう', 'まんねんひつを つかう', 'あたらしい まんねんひつ', 'たかい まんねんひつ', 'まんねんひつを ください', 'まんねんひつは どこ', 'まんねんひつを みる', 'やすい まんねんひつ']`

- shared-tail signal (template-generation):
  - tail `んひつ`: `['あたらしい まんねんひつ', 'たかい まんねんひつ', 'やすい まんねんひつ']`

### ペン (`n5.vocab.24-school-and-study.ペン`)
current particle_examples: `['ペンを かう', 'ペンを つかう', 'あたらしい ペン', 'たかい ペン', 'ペンを ください', 'ペンは どこ', 'ペンを みる', 'やすい ペン']`

- shared-tail signal (template-generation):
  - tail ` ペン`: `['あたらしい ペン', 'たかい ペン', 'やすい ペン']`

### こくばん (`n5.vocab.24-school-and-study.こくばん`)
current particle_examples: `['こくばんを かう', 'こくばんを つかう', 'あたらしい こくばん', 'たかい こくばん', 'こくばんを ください', 'こくばんは どこ', 'こくばんを みる', 'やすい こくばん']`

- shared-tail signal (template-generation):
  - tail `くばん`: `['あたらしい こくばん', 'たかい こくばん', 'やすい こくばん']`

### チョーク (`n5.vocab.24-school-and-study.チョーク`)
current particle_examples: `['チョークを かう', 'チョークを つかう', 'あたらしい チョーク', 'たかい チョーク', 'チョークを ください', 'チョークは どこ', 'チョークを みる', 'やすい チョーク']`

- shared-tail signal (template-generation):
  - tail `ョーク`: `['あたらしい チョーク', 'たかい チョーク', 'やすい チョーク']`

### つくえ (`n5.vocab.24-school-and-study.つくえ`)
current particle_examples: `['つくえを かう', 'つくえを つかう', 'あたらしい つくえ', 'たかい つくえ', 'つくえを ください', 'つくえは どこ', 'つくえを みる', 'やすい つくえ']`

- shared-tail signal (template-generation):
  - tail `つくえ`: `['あたらしい つくえ', 'たかい つくえ', 'やすい つくえ']`

### けしゴム (`n5.vocab.24-school-and-study.けしゴム`)
current particle_examples: `['けしゴムを かう', 'けしゴムを つかう', 'あたらしい けしゴム', 'たかい けしゴム', 'けしゴムを ください', 'けしゴムは どこ', 'けしゴムを みる', 'やすい けしゴム']`

- shared-tail signal (template-generation):
  - tail `しゴム`: `['あたらしい けしゴム', 'たかい けしゴム', 'やすい けしゴム']`

### ちず (`n5.vocab.24-school-and-study.ちず`)
current particle_examples: `['ちずを かう', 'ちずを つかう', 'あたらしい ちず', 'たかい ちず', 'ちずを ください', 'ちずは どこ', 'ちずを みる', 'やすい ちず']`

- shared-tail signal (template-generation):
  - tail ` ちず`: `['あたらしい ちず', 'たかい ちず', 'やすい ちず']`

### しゃしん (`n5.vocab.24-school-and-study.しゃしん`)
current particle_examples: `['しゃしんが ある', 'しゃしんが ない', 'しゃしんを いう', 'しゃしんを きく', 'いい しゃしん', 'しゃしんの とき', 'しゃしんを おもう', 'しゃしんを しる']`

- template-shape hits:
  - shape `を しる` in `しゃしんを しる`

### 電話番号 (`n5.vocab.24-school-and-study.電話番号`)
reading: `でんわばんごう`  
current particle_examples: `['電話番号を かう', '電話番号を つかう', 'あたらしい 電話番号', 'たかい 電話番号', '電話番号を ください', '電話番号は どこ', '電話番号を みる', 'やすい 電話番号']`

- shared-tail signal (template-generation):
  - tail `話番号`: `['あたらしい 電話番号', 'たかい 電話番号', 'やすい 電話番号']`

### 日本 (`n5.vocab.25-languages-and-countri.日本`)
reading: `にほん`  
current particle_examples: `['日本を かう', '日本を つかう', 'あたらしい 日本', 'たかい 日本', '日本を ください', '日本は どこ', '日本を みる', 'やすい 日本']`

- shared-tail signal (template-generation):
  - tail ` 日本`: `['あたらしい 日本', 'たかい 日本', 'やすい 日本']`

### 日本語 (`n5.vocab.25-languages-and-countri.日本語`)
reading: `にほんご`  
current particle_examples: `['日本語を かう', '日本語を つかう', 'あたらしい 日本語', 'たかい 日本語', '日本語を ください', '日本語は どこ', '日本語を みる', 'やすい 日本語']`

- shared-tail signal (template-generation):
  - tail `日本語`: `['あたらしい 日本語', 'たかい 日本語', 'やすい 日本語']`

### えいご (`n5.vocab.25-languages-and-countri.えいご`)
current particle_examples: `['えいごを かう', 'えいごを つかう', 'あたらしい えいご', 'たかい えいご', 'えいごを ください', 'えいごは どこ', 'えいごを みる', 'やすい えいご']`

- shared-tail signal (template-generation):
  - tail `えいご`: `['あたらしい えいご', 'たかい えいご', 'やすい えいご']`

### 中国語 (`n5.vocab.25-languages-and-countri.中国語`)
reading: `ちゅうごくご`  
current particle_examples: `['中国語を ならう', '中国語が じょうず', '中国語の せんせい', '中国語で はなす', '中国語の 本', '中国語の しけん']`

- template-shape hits:
  - shape `を ならう` in `中国語を ならう`

### かんこく (`n5.vocab.25-languages-and-countri.かんこく`)
current particle_examples: `['かんこくに いく', 'かんこくで あう', 'かんこくから くる', 'かんこくの まえに', 'かんこくが ある', 'かんこくは ちかい', 'かんこくまで あるく', 'かんこくに つく']`

- template-shape hits:
  - shape `に いく` in `かんこくに いく`

### かんこくご (`n5.vocab.25-languages-and-countri.かんこくご`)
current particle_examples: `['かんこくごを かう', 'かんこくごを つかう', 'あたらしい かんこくご', 'たかい かんこくご', 'かんこくごを ください', 'かんこくごは どこ', 'かんこくごを みる', 'やすい かんこくご']`

- shared-tail signal (template-generation):
  - tail `こくご`: `['あたらしい かんこくご', 'たかい かんこくご', 'やすい かんこくご']`

### フランスご (`n5.vocab.25-languages-and-countri.フランスご`)
current particle_examples: `['フランスごを かう', 'フランスごを つかう', 'あたらしい フランスご', 'たかい フランスご', 'フランスごを ください', 'フランスごは どこ', 'フランスごを みる', 'やすい フランスご']`

- shared-tail signal (template-generation):
  - tail `ンスご`: `['あたらしい フランスご', 'たかい フランスご', 'やすい フランスご']`

### 外国語 (`n5.vocab.25-languages-and-countri.外国語`)
reading: `がいこくご`  
current particle_examples: `['外国語を かう', '外国語を つかう', 'あたらしい 外国語', 'たかい 外国語', '外国語を ください', '外国語は どこ', '外国語を みる', 'やすい 外国語']`

- shared-tail signal (template-generation):
  - tail `外国語`: `['あたらしい 外国語', 'たかい 外国語', 'やすい 外国語']`

### と (`n5.vocab.26-house-and-furniture.と`)
current particle_examples: `['とに いく', 'とで あう', 'とから くる', 'との まえに', 'とが ある', 'とは ちかい', 'とまで あるく', 'とに つく']`

- template-shape hits:
  - shape `に いく` in `とに いく`

### まど (`n5.vocab.26-house-and-furniture.まど`)
current particle_examples: `['まどに いく', 'まどで あう', 'まどから くる', 'まどの まえに', 'まどが ある', 'まどは ちかい', 'まどまで あるく', 'まどに つく']`

- template-shape hits:
  - shape `に いく` in `まどに いく`

### かべ (`n5.vocab.26-house-and-furniture.かべ`)
current particle_examples: `['かべが ある', 'かべが ない', 'かべを いう', 'かべを きく', 'いい かべ', 'かべの とき', 'かべを おもう', 'かべを しる']`

- template-shape hits:
  - shape `を しる` in `かべを しる`

### かいだん (`n5.vocab.26-house-and-furniture.かいだん`)
current particle_examples: `['かいだんに いく', 'かいだんで あう', 'かいだんから くる', 'かいだんの まえに', 'かいだんが ある', 'かいだんは ちかい', 'かいだんまで あるく', 'かいだんに つく']`

- template-shape hits:
  - shape `に いく` in `かいだんに いく`

### いま (`n5.vocab.26-house-and-furniture.いま`)
current particle_examples: `['言いました', 'おもいます', 'らいました', 'かいましたか', 'あらいます', 'もらいまし', 'あいました', 'とうございます']`

- shared-tail signal (template-generation):
  - tail `ました`: `['言いました', 'らいました', 'あいました']`
  - tail `います`: `['おもいます', 'あらいます', 'とうございます']`

### しんしつ (`n5.vocab.26-house-and-furniture.しんしつ`)
current particle_examples: `['しんしつに いく', 'しんしつで あう', 'しんしつから くる', 'しんしつの まえに', 'しんしつが ある', 'しんしつは ちかい', 'しんしつまで あるく', 'しんしつに つく']`

- template-shape hits:
  - shape `に いく` in `しんしつに いく`

### ふとん (`n5.vocab.26-house-and-furniture.ふとん`)
current particle_examples: `['ふとんを かう', 'ふとんを つかう', 'あたらしい ふとん', 'たかい ふとん', 'ふとんを ください', 'ふとんは どこ', 'ふとんを みる', 'やすい ふとん']`

- shared-tail signal (template-generation):
  - tail `ふとん`: `['あたらしい ふとん', 'たかい ふとん', 'やすい ふとん']`

### もうふ (`n5.vocab.26-house-and-furniture.もうふ`)
current particle_examples: `['もうふを かう', 'もうふを つかう', 'あたらしい もうふ', 'たかい もうふ', 'もうふを ください', 'もうふは どこ', 'もうふを みる', 'やすい もうふ']`

- shared-tail signal (template-generation):
  - tail `もうふ`: `['あたらしい もうふ', 'たかい もうふ', 'やすい もうふ']`

### まくら (`n5.vocab.26-house-and-furniture.まくら`)
current particle_examples: `['まくらを かう', 'まくらを つかう', 'あたらしい まくら', 'たかい まくら', 'まくらを ください', 'まくらは どこ', 'まくらを みる', 'やすい まくら']`

- shared-tail signal (template-generation):
  - tail `まくら`: `['あたらしい まくら', 'たかい まくら', 'やすい まくら']`

### たな (`n5.vocab.26-house-and-furniture.たな`)
current particle_examples: `['たなを かう', 'たなを つかう', 'あたらしい たな', 'たかい たな', 'たなを ください', 'たなは どこ', 'たなを みる', 'やすい たな']`

- shared-tail signal (template-generation):
  - tail ` たな`: `['あたらしい たな', 'たかい たな', 'やすい たな']`

### ほんだな (`n5.vocab.26-house-and-furniture.ほんだな`)
current particle_examples: `['ほんだなを かう', 'ほんだなを つかう', 'あたらしい ほんだな', 'たかい ほんだな', 'ほんだなを ください', 'ほんだなは どこ', 'ほんだなを みる', 'やすい ほんだな']`

- shared-tail signal (template-generation):
  - tail `んだな`: `['あたらしい ほんだな', 'たかい ほんだな', 'やすい ほんだな']`

### カーテン (`n5.vocab.26-house-and-furniture.カーテン`)
current particle_examples: `['カーテンを あける', 'カーテンを しめる', 'あつい カーテン', 'うすい カーテン', '新しい カーテン', 'カーテンの いろ']`

- shared-tail signal (template-generation):
  - tail `ーテン`: `['あつい カーテン', 'うすい カーテン', '新しい カーテン']`

### かぎ (`n5.vocab.26-house-and-furniture.かぎ`)
current particle_examples: `['かぎを かう', 'かぎを つかう', 'あたらしい かぎ', 'たかい かぎ', 'かぎを ください', 'かぎは どこ', 'かぎを みる', 'やすい かぎ']`

- shared-tail signal (template-generation):
  - tail ` かぎ`: `['あたらしい かぎ', 'たかい かぎ', 'やすい かぎ']`

### せっけん (`n5.vocab.26-house-and-furniture.せっけん`)
current particle_examples: `['せっけんを かう', 'せっけんを つかう', 'あたらしい せっけん', 'たかい せっけん', 'せっけんを ください', 'せっけんは どこ', 'せっけんを みる', 'やすい せっけん']`

- shared-tail signal (template-generation):
  - tail `っけん`: `['あたらしい せっけん', 'たかい せっけん', 'やすい せっけん']`

### タオル (`n5.vocab.26-house-and-furniture.タオル`)
current particle_examples: `['タオルを かう', 'タオルを つかう', 'あたらしい タオル', 'たかい タオル', 'タオルを ください', 'タオルは どこ', 'タオルを みる', 'やすい タオル']`

- shared-tail signal (template-generation):
  - tail `タオル`: `['あたらしい タオル', 'たかい タオル', 'やすい タオル']`

### えいが (`n5.vocab.26-house-and-furniture.えいが`)
current particle_examples: `['えいがが ある', 'えいがが ない', 'えいがを いう', 'えいがを きく', 'いい えいが', 'えいがの とき', 'えいがを おもう', 'えいがを しる']`

- template-shape hits:
  - shape `を しる` in `えいがを しる`

### おんがく (`n5.vocab.26-house-and-furniture.おんがく`)
current particle_examples: `['おんがくが ある', 'おんがくが ない', 'おんがくを いう', 'おんがくを きく', 'いい おんがく', 'おんがくの とき', 'おんがくを おもう', 'おんがくを しる']`

- template-shape hits:
  - shape `を しる` in `おんがくを しる`

### うた (`n5.vocab.26-house-and-furniture.うた`)
current particle_examples: `['うたを うたう', 'すきな うた', 'おもしろい うた', 'うたの 名前', 'にほんごの うた', 'うたを ならう']`

- template-shape hits:
  - shape `を ならう` in `うたを ならう`
- shared-tail signal (template-generation):
  - tail ` うた`: `['すきな うた', 'おもしろい うた', 'にほんごの うた']`

### え (`n5.vocab.26-house-and-furniture.え`)
current particle_examples: `['えを かう', 'えを つかう', 'あたらしい え', 'たかい え', 'えを ください', 'えは どこ', 'えを みる', 'やすい え']`

- shared-tail signal (template-generation):
  - tail `い え`: `['あたらしい え', 'たかい え', 'やすい え']`

### ピアノ (`n5.vocab.26-house-and-furniture.ピアノ`)
current particle_examples: `['ピアノを ひく', 'ピアノを ならう', 'ピアノの せんせい', 'ピアノの レッスン', 'ピアノの コンサート', 'ピアノが すき']`

- template-shape hits:
  - shape `を ならう` in `ピアノを ならう`

### ギター (`n5.vocab.26-house-and-furniture.ギター`)
current particle_examples: `['ギターを ひく', 'ギターを ならう', '新しい ギター', 'ギターの レッスン', 'ギターの コンサート', 'ギターを かう']`

- template-shape hits:
  - shape `を ならう` in `ギターを ならう`

### 会う (`n5.vocab.27-verbs-group-1-verbs.会う`)
reading: `あう`  
current particle_examples: `['会う', '会うます', '会うました', 'よく 会う', 'まいにち 会う', 'いま 会う']`

- shared-tail signal (template-generation):
  - tail ` 会う`: `['よく 会う', 'まいにち 会う', 'いま 会う']`

### 言う (`n5.vocab.27-verbs-group-1-verbs.言う`)
reading: `いう`  
current particle_examples: `['言う', '言うます', '言うました', 'よく 言う', 'まいにち 言う', 'いま 言う']`

- shared-tail signal (template-generation):
  - tail ` 言う`: `['よく 言う', 'まいにち 言う', 'いま 言う']`

### 行く (`n5.vocab.27-verbs-group-1-verbs.行く`)
reading: `いく`  
current particle_examples: `['おいくつですか', 'ていく人が', 'もっていく人', '学校へ 行く', '日本へ 行く', '行ってきます', 'いっしょに 行く', 'うみに 行く', 'ともだちと 行く']`

- shared-tail signal (template-generation):
  - tail ` 行く`: `['学校へ 行く', '日本へ 行く', 'いっしょに 行く', 'うみに 行く', 'ともだちと 行く']`

### うたう (`n5.vocab.27-verbs-group-1-verbs.うたう`)
current particle_examples: `['うたう', 'うたうます', 'うたうました', 'よく うたう', 'まいにち うたう', 'いま うたう']`

- shared-tail signal (template-generation):
  - tail `うたう`: `['うたう', 'よく うたう', 'まいにち うたう', 'いま うたう']`

### おもう (`n5.vocab.27-verbs-group-1-verbs.おもう`)
current particle_examples: `['おもう', 'おもうます', 'おもうました', 'よく おもう', 'まいにち おもう', 'いま おもう']`

- shared-tail signal (template-generation):
  - tail `おもう`: `['おもう', 'よく おもう', 'まいにち おもう', 'いま おもう']`

### 買う (`n5.vocab.27-verbs-group-1-verbs.買う`)
reading: `かう`  
current particle_examples: `['つかう人が', 'ほんを 買う', 'プレゼントを 買う', 'やすく 買う', 'たかく 買う', 'まいにち 買う', 'ともだちに 買って あげる']`

- shared-tail signal (template-generation):
  - tail ` 買う`: `['ほんを 買う', 'プレゼントを 買う', 'やすく 買う', 'たかく 買う', 'まいにち 買う']`

### 書く (`n5.vocab.27-verbs-group-1-verbs.書く`)
reading: `かく`  
current particle_examples: `['たかくないです', 'しかくいでした', 'えを 書く', 'てがみを 書く', 'なまえを 書く', 'にっきを 書く', 'すうじを 書く', 'べんきょうを 書く']`

- shared-tail signal (template-generation):
  - tail ` 書く`: `['えを 書く', 'てがみを 書く', 'なまえを 書く', 'にっきを 書く', 'すうじを 書く', 'べんきょうを 書く']`

### 聞く (`n5.vocab.27-verbs-group-1-verbs.聞く`)
reading: `きく`  
current particle_examples: `['大きくないです', 'おんがくを 聞く', '先生に 聞く', 'はなしを 聞く', 'ニュースを 聞く', 'よく 聞く', 'こたえを 聞く']`

- shared-tail signal (template-generation):
  - tail ` 聞く`: `['おんがくを 聞く', '先生に 聞く', 'はなしを 聞く', 'ニュースを 聞く', 'よく 聞く', 'こたえを 聞く']`

### きる (`n5.vocab.27-verbs-group-1-verbs.きる`)
current particle_examples: `['きる', 'きるます', 'きるました', 'よく きる', 'まいにち きる', 'いま きる']`

- shared-tail signal (template-generation):
  - tail ` きる`: `['よく きる', 'まいにち きる', 'いま きる']`

### つくる (`n5.vocab.27-verbs-group-1-verbs.つくる`)
current particle_examples: `['つくる', 'つくるます', 'つくるました', 'よく つくる', 'まいにち つくる', 'いま つくる']`

- shared-tail signal (template-generation):
  - tail `つくる`: `['つくる', 'よく つくる', 'まいにち つくる', 'いま つくる']`

### しる (`n5.vocab.27-verbs-group-1-verbs.しる`)
current particle_examples: `['しる', 'しるます', 'しるました', 'よく しる', 'まいにち しる', 'いま しる']`

- shared-tail signal (template-generation):
  - tail ` しる`: `['よく しる', 'まいにち しる', 'いま しる']`

### すむ (`n5.vocab.27-verbs-group-1-verbs.すむ`)
current particle_examples: `['すむ', 'すむます', 'すむました', 'よく すむ', 'まいにち すむ', 'いま すむ']`

- shared-tail signal (template-generation):
  - tail ` すむ`: `['よく すむ', 'まいにち すむ', 'いま すむ']`

### 立つ (`n5.vocab.27-verbs-group-1-verbs.立つ`)
reading: `たつ`  
current particle_examples: `['駅に立つ', 'いすから立つ', 'まどの まえに 立つ', 'はやく 立つ', 'いすから 立つ', 'まっすぐ 立つ', '一じかん 立つ', '時間が 立つ']`

- shared-tail signal (template-generation):
  - tail ` 立つ`: `['まどの まえに 立つ', 'はやく 立つ', 'いすから 立つ', 'まっすぐ 立つ', '一じかん 立つ', '時間が 立つ']`

### とる (`n5.vocab.27-verbs-group-1-verbs.とる`)
current particle_examples: `['とる', 'とるます', 'とるました', 'よく とる', 'まいにち とる', 'いま とる']`

- shared-tail signal (template-generation):
  - tail ` とる`: `['よく とる', 'まいにち とる', 'いま とる']`

### とる (`n5.vocab.27-verbs-group-1-verbs.とる.2`)
current particle_examples: `['しゃしんを とる', 'メモを とる', 'ノートを とる', '手に とる', '休みを とる', 'お金を とる']`

- shared-tail signal (template-generation):
  - tail ` とる`: `['しゃしんを とる', 'メモを とる', 'ノートを とる', '手に とる', '休みを とる', 'お金を とる']`

### なく (`n5.vocab.27-verbs-group-1-verbs.なく`)
current particle_examples: `['なく', 'なくます', 'なくました', 'よく なく', 'まいにち なく', 'いま なく']`

- shared-tail signal (template-generation):
  - tail ` なく`: `['よく なく', 'まいにち なく', 'いま なく']`

### 飲む (`n5.vocab.27-verbs-group-1-verbs.飲む`)
reading: `のむ`  
current particle_examples: `['たのむことが', 'コーヒーを 飲む', 'お水を 飲む', 'おさけを 飲む', 'たくさん 飲む', '一日に 飲む', 'おちゃを 飲む']`

- shared-tail signal (template-generation):
  - tail ` 飲む`: `['コーヒーを 飲む', 'お水を 飲む', 'おさけを 飲む', 'たくさん 飲む', '一日に 飲む', 'おちゃを 飲む']`

### 入る (`n5.vocab.27-verbs-group-1-verbs.入る`)
reading: `はいる`  
current particle_examples: `['入る', '入るます', '入るました', 'よく 入る', 'まいにち 入る', 'いま 入る']`

- shared-tail signal (template-generation):
  - tail ` 入る`: `['よく 入る', 'まいにち 入る', 'いま 入る']`

### はく (`n5.vocab.27-verbs-group-1-verbs.はく`)
current particle_examples: `['くつをはく', 'ズボンをはく', 'スカートをはく']`

- shared-tail signal (template-generation):
  - tail `をはく`: `['くつをはく', 'ズボンをはく', 'スカートをはく']`

### 話す (`n5.vocab.27-verbs-group-1-verbs.話す`)
reading: `はなす`  
current particle_examples: `['電話するつもり', '日本語で 話す', 'ともだちと 話す', 'ゆっくり 話す', '大きな こえで 話す', 'もんだいに ついて 話す', 'たくさん 話す']`

- shared-tail signal (template-generation):
  - tail ` 話す`: `['日本語で 話す', 'ともだちと 話す', 'ゆっくり 話す', '大きな こえで 話す', 'もんだいに ついて 話す', 'たくさん 話す']`

### はしる (`n5.vocab.27-verbs-group-1-verbs.はしる`)
current particle_examples: `['はしる', 'はしるます', 'はしるました', 'よく はしる', 'まいにち はしる', 'いま はしる']`

- shared-tail signal (template-generation):
  - tail `はしる`: `['はしる', 'よく はしる', 'まいにち はしる', 'いま はしる']`

### はたらく (`n5.vocab.27-verbs-group-1-verbs.はたらく`)
current particle_examples: `['はたらく', 'はたらくます', 'はたらくました', 'よく はたらく', 'まいにち はたらく', 'いま はたらく']`

- shared-tail signal (template-generation):
  - tail `たらく`: `['はたらく', 'よく はたらく', 'まいにち はたらく', 'いま はたらく']`

### まつ (`n5.vocab.27-verbs-group-1-verbs.まつ`)
current particle_examples: `['まつ', 'まつます', 'まつました', 'よく まつ', 'まいにち まつ', 'いま まつ']`

- shared-tail signal (template-generation):
  - tail ` まつ`: `['よく まつ', 'まいにち まつ', 'いま まつ']`

### もつ (`n5.vocab.27-verbs-group-1-verbs.もつ`)
current particle_examples: `['もつ', 'もつます', 'もつました', 'よく もつ', 'まいにち もつ', 'いま もつ']`

- shared-tail signal (template-generation):
  - tail ` もつ`: `['よく もつ', 'まいにち もつ', 'いま もつ']`

### 読む (`n5.vocab.27-verbs-group-1-verbs.読む`)
reading: `よむ`  
current particle_examples: `['読む', '読むます', '読むました', 'よく 読む', 'まいにち 読む', 'いま 読む']`

- shared-tail signal (template-generation):
  - tail ` 読む`: `['よく 読む', 'まいにち 読む', 'いま 読む']`

### わたる (`n5.vocab.27-verbs-group-1-verbs.わたる`)
current particle_examples: `['わたる', 'わたるます', 'わたるました', 'よく わたる', 'まいにち わたる', 'いま わたる']`

- shared-tail signal (template-generation):
  - tail `わたる`: `['わたる', 'よく わたる', 'まいにち わたる', 'いま わたる']`

### 分かる (`n5.vocab.27-verbs-group-1-verbs.分かる`)
reading: `わかる`  
current particle_examples: `['分かる', '分かるます', '分かるました', 'よく 分かる', 'まいにち 分かる', 'いま 分かる']`

- shared-tail signal (template-generation):
  - tail `分かる`: `['分かる', 'よく 分かる', 'まいにち 分かる', 'いま 分かる']`

### おわる (`n5.vocab.27-verbs-group-1-verbs.おわる`)
current particle_examples: `['おわる', 'おわるます', 'おわるました', 'よく おわる', 'まいにち おわる', 'いま おわる']`

- shared-tail signal (template-generation):
  - tail `おわる`: `['おわる', 'よく おわる', 'まいにち おわる', 'いま おわる']`

### はじまる (`n5.vocab.27-verbs-group-1-verbs.はじまる`)
current particle_examples: `['はじまる', 'はじまるます', 'はじまるました', 'よく はじまる', 'まいにち はじまる', 'いま はじまる']`

- shared-tail signal (template-generation):
  - tail `じまる`: `['はじまる', 'よく はじまる', 'まいにち はじまる', 'いま はじまる']`

### かえる (`n5.vocab.27-verbs-group-1-verbs.かえる`)
current particle_examples: `['かえる', 'かえるます', 'かえるました', 'よく かえる', 'まいにち かえる', 'いま かえる']`

- shared-tail signal (template-generation):
  - tail `かえる`: `['かえる', 'よく かえる', 'まいにち かえる', 'いま かえる']`

### うる (`n5.vocab.27-verbs-group-1-verbs.うる`)
current particle_examples: `['うる', 'うるます', 'うるました', 'よく うる', 'まいにち うる', 'いま うる']`

- shared-tail signal (template-generation):
  - tail ` うる`: `['よく うる', 'まいにち うる', 'いま うる']`

### おす (`n5.vocab.27-verbs-group-1-verbs.おす`)
current particle_examples: `['おす', 'おすます', 'おすました', 'よく おす', 'まいにち おす', 'いま おす']`

- shared-tail signal (template-generation):
  - tail ` おす`: `['よく おす', 'まいにち おす', 'いま おす']`

### およぐ (`n5.vocab.27-verbs-group-1-verbs.およぐ`)
current particle_examples: `['およぐ', 'およぐます', 'およぐました', 'よく およぐ', 'まいにち およぐ', 'いま およぐ']`

- shared-tail signal (template-generation):
  - tail `およぐ`: `['およぐ', 'よく およぐ', 'まいにち およぐ', 'いま およぐ']`

### ひく (`n5.vocab.27-verbs-group-1-verbs.ひく`)
current particle_examples: `['ひく', 'ひくます', 'ひくました', 'よく ひく', 'まいにち ひく', 'いま ひく']`

- shared-tail signal (template-generation):
  - tail ` ひく`: `['よく ひく', 'まいにち ひく', 'いま ひく']`

### ひく (`n5.vocab.27-verbs-group-1-verbs.ひく.2`)
current particle_examples: `['ひく', 'ひくます', 'ひくました', 'よく ひく', 'まいにち ひく', 'いま ひく']`

- shared-tail signal (template-generation):
  - tail ` ひく`: `['よく ひく', 'まいにち ひく', 'いま ひく']`

### よぶ (`n5.vocab.27-verbs-group-1-verbs.よぶ`)
current particle_examples: `['よぶ', 'よぶます', 'よぶました', 'よく よぶ', 'まいにち よぶ', 'いま よぶ']`

- shared-tail signal (template-generation):
  - tail ` よぶ`: `['よく よぶ', 'まいにち よぶ', 'いま よぶ']`

### とぶ (`n5.vocab.27-verbs-group-1-verbs.とぶ`)
current particle_examples: `['とぶ', 'とぶます', 'とぶました', 'よく とぶ', 'まいにち とぶ', 'いま とぶ']`

- shared-tail signal (template-generation):
  - tail ` とぶ`: `['よく とぶ', 'まいにち とぶ', 'いま とぶ']`

### こまる (`n5.vocab.27-verbs-group-1-verbs.こまる`)
current particle_examples: `['こまる', 'こまるます', 'こまるました', 'よく こまる', 'まいにち こまる', 'いま こまる']`

- shared-tail signal (template-generation):
  - tail `こまる`: `['こまる', 'よく こまる', 'まいにち こまる', 'いま こまる']`

### ならぶ (`n5.vocab.27-verbs-group-1-verbs.ならぶ`)
current particle_examples: `['ならぶ', 'ならぶます', 'ならぶました', 'よく ならぶ', 'まいにち ならぶ', 'いま ならぶ']`

- shared-tail signal (template-generation):
  - tail `ならぶ`: `['ならぶ', 'よく ならぶ', 'まいにち ならぶ', 'いま ならぶ']`

### のぼる (`n5.vocab.27-verbs-group-1-verbs.のぼる`)
current particle_examples: `['のぼる', 'のぼるます', 'のぼるました', 'よく のぼる', 'まいにち のぼる', 'いま のぼる']`

- shared-tail signal (template-generation):
  - tail `のぼる`: `['のぼる', 'よく のぼる', 'まいにち のぼる', 'いま のぼる']`

### わたす (`n5.vocab.27-verbs-group-1-verbs.わたす`)
current particle_examples: `['わたす', 'わたすます', 'わたすました', 'よく わたす', 'まいにち わたす', 'いま わたす']`

- shared-tail signal (template-generation):
  - tail `わたす`: `['わたす', 'よく わたす', 'まいにち わたす', 'いま わたす']`

### ぬぐ (`n5.vocab.27-verbs-group-1-verbs.ぬぐ`)
current particle_examples: `['ぬぐ', 'ぬぐます', 'ぬぐました', 'よく ぬぐ', 'まいにち ぬぐ', 'いま ぬぐ']`

- shared-tail signal (template-generation):
  - tail ` ぬぐ`: `['よく ぬぐ', 'まいにち ぬぐ', 'いま ぬぐ']`

### あらう (`n5.vocab.27-verbs-group-1-verbs.あらう`)
current particle_examples: `['あらう', 'あらうます', 'あらうました', 'よく あらう', 'まいにち あらう', 'いま あらう']`

- shared-tail signal (template-generation):
  - tail `あらう`: `['あらう', 'よく あらう', 'まいにち あらう', 'いま あらう']`

### いそぐ (`n5.vocab.27-verbs-group-1-verbs.いそぐ`)
current particle_examples: `['いそぐ', 'いそぐます', 'いそぐました', 'よく いそぐ', 'まいにち いそぐ', 'いま いそぐ']`

- shared-tail signal (template-generation):
  - tail `いそぐ`: `['いそぐ', 'よく いそぐ', 'まいにち いそぐ', 'いま いそぐ']`

### しぬ (`n5.vocab.27-verbs-group-1-verbs.しぬ`)
current particle_examples: `['しぬ', 'しぬます', 'しぬました', 'よく しぬ', 'まいにち しぬ', 'いま しぬ']`

- shared-tail signal (template-generation):
  - tail ` しぬ`: `['よく しぬ', 'まいにち しぬ', 'いま しぬ']`

### すう (`n5.vocab.27-verbs-group-1-verbs.すう`)
current particle_examples: `['すう', 'すうます', 'すうました', 'よく すう', 'まいにち すう', 'いま すう']`

- shared-tail signal (template-generation):
  - tail ` すう`: `['よく すう', 'まいにち すう', 'いま すう']`

### ちがう (`n5.vocab.27-verbs-group-1-verbs.ちがう`)
current particle_examples: `['ちがう', 'ちがうます', 'ちがうました', 'よく ちがう', 'まいにち ちがう', 'いま ちがう']`

- shared-tail signal (template-generation):
  - tail `ちがう`: `['ちがう', 'よく ちがう', 'まいにち ちがう', 'いま ちがう']`

### つかう (`n5.vocab.27-verbs-group-1-verbs.つかう`)
current particle_examples: `['つかう', 'つかうます', 'つかうました', 'よく つかう', 'まいにち つかう', 'いま つかう']`

- shared-tail signal (template-generation):
  - tail `つかう`: `['つかう', 'よく つかう', 'まいにち つかう', 'いま つかう']`

### つく (`n5.vocab.27-verbs-group-1-verbs.つく`)
current particle_examples: `['つく', 'つくます', 'つくました', 'よく つく', 'まいにち つく', 'いま つく']`

- shared-tail signal (template-generation):
  - tail ` つく`: `['よく つく', 'まいにち つく', 'いま つく']`

### ならう (`n5.vocab.27-verbs-group-1-verbs.ならう`)
current particle_examples: `['ならう', 'ならうます', 'ならうました', 'よく ならう', 'まいにち ならう', 'いま ならう']`

- shared-tail signal (template-generation):
  - tail `ならう`: `['ならう', 'よく ならう', 'まいにち ならう', 'いま ならう']`

### はる (`n5.vocab.27-verbs-group-1-verbs.はる`)
current particle_examples: `['はる', 'はるます', 'はるました', 'よく はる', 'まいにち はる', 'いま はる']`

- shared-tail signal (template-generation):
  - tail ` はる`: `['よく はる', 'まいにち はる', 'いま はる']`

### まがる (`n5.vocab.27-verbs-group-1-verbs.まがる`)
current particle_examples: `['まがる', 'まがるます', 'まがるました', 'よく まがる', 'まいにち まがる', 'いま まがる']`

- shared-tail signal (template-generation):
  - tail `まがる`: `['まがる', 'よく まがる', 'まいにち まがる', 'いま まがる']`

### みがく (`n5.vocab.27-verbs-group-1-verbs.みがく`)
current particle_examples: `['みがく', 'みがくます', 'みがくました', 'よく みがく', 'まいにち みがく', 'いま みがく']`

- shared-tail signal (template-generation):
  - tail `みがく`: `['みがく', 'よく みがく', 'まいにち みがく', 'いま みがく']`

### もっていく (`n5.vocab.27-verbs-group-1-verbs.もっていく`)
current particle_examples: `['もっていく', 'もっていくます', 'もっていくました', 'よく もっていく', 'まいにち もっていく', 'いま もっていく']`

- shared-tail signal (template-generation):
  - tail `ていく`: `['もっていく', 'よく もっていく', 'まいにち もっていく', 'いま もっていく']`

### もってくる (`n5.vocab.27-verbs-group-1-verbs.もってくる`)
current particle_examples: `['もってくる', 'もってくるます', 'もってくるました', 'よく もってくる', 'まいにち もってくる', 'いま もってくる']`

- shared-tail signal (template-generation):
  - tail `てくる`: `['もってくる', 'よく もってくる', 'まいにち もってくる', 'いま もってくる']`

### あく (`n5.vocab.27-verbs-group-1-verbs.あく`)
current particle_examples: `['あく', 'あくます', 'あくました', 'よく あく', 'まいにち あく', 'いま あく']`

- shared-tail signal (template-generation):
  - tail ` あく`: `['よく あく', 'まいにち あく', 'いま あく']`

### しまる (`n5.vocab.27-verbs-group-1-verbs.しまる`)
current particle_examples: `['しまる', 'しまるます', 'しまるました', 'よく しまる', 'まいにち しまる', 'いま しまる']`

- shared-tail signal (template-generation):
  - tail `しまる`: `['しまる', 'よく しまる', 'まいにち しまる', 'いま しまる']`

### だす (`n5.vocab.27-verbs-group-1-verbs.だす`)
current particle_examples: `['だす', 'だすます', 'だすました', 'よく だす', 'まいにち だす', 'いま だす']`

- shared-tail signal (template-generation):
  - tail ` だす`: `['よく だす', 'まいにち だす', 'いま だす']`

### おとす (`n5.vocab.27-verbs-group-1-verbs.おとす`)
current particle_examples: `['おとす', 'おとすます', 'おとすました', 'よく おとす', 'まいにち おとす', 'いま おとす']`

- shared-tail signal (template-generation):
  - tail `おとす`: `['おとす', 'よく おとす', 'まいにち おとす', 'いま おとす']`

### ふく (`n5.vocab.27-verbs-group-1-verbs.ふく`)
current particle_examples: `['ふく', 'ふくます', 'ふくました', 'よく ふく', 'まいにち ふく', 'いま ふく']`

- shared-tail signal (template-generation):
  - tail ` ふく`: `['よく ふく', 'まいにち ふく', 'いま ふく']`

### ふる (`n5.vocab.27-verbs-group-1-verbs.ふる`)
current particle_examples: `['ふる', 'ふるます', 'ふるました', 'よく ふる', 'まいにち ふる', 'いま ふる']`

- shared-tail signal (template-generation):
  - tail ` ふる`: `['よく ふる', 'まいにち ふる', 'いま ふる']`

### くもる (`n5.vocab.27-verbs-group-1-verbs.くもる`)
current particle_examples: `['くもる', 'くもるます', 'くもるました', 'よく くもる', 'まいにち くもる', 'いま くもる']`

- shared-tail signal (template-generation):
  - tail `くもる`: `['くもる', 'よく くもる', 'まいにち くもる', 'いま くもる']`

### なくす (`n5.vocab.27-verbs-group-1-verbs.なくす`)
current particle_examples: `['なくす', 'なくすます', 'なくすました', 'よく なくす', 'まいにち なくす', 'いま なくす']`

- shared-tail signal (template-generation):
  - tail `なくす`: `['なくす', 'よく なくす', 'まいにち なくす', 'いま なくす']`

### のる (`n5.vocab.27-verbs-group-1-verbs.のる`)
current particle_examples: `['のる', 'のるます', 'のるました', 'よく のる', 'まいにち のる', 'いま のる']`

- shared-tail signal (template-generation):
  - tail ` のる`: `['よく のる', 'まいにち のる', 'いま のる']`

### すわる (`n5.vocab.27-verbs-group-1-verbs.すわる`)
current particle_examples: `['すわる', 'すわるます', 'すわるました', 'よく すわる', 'まいにち すわる', 'いま すわる']`

- shared-tail signal (template-generation):
  - tail `すわる`: `['すわる', 'よく すわる', 'まいにち すわる', 'いま すわる']`

### たのむ (`n5.vocab.27-verbs-group-1-verbs.たのむ`)
current particle_examples: `['たのむ', 'たのむます', 'たのむました', 'よく たのむ', 'まいにち たのむ', 'いま たのむ']`

- shared-tail signal (template-generation):
  - tail `たのむ`: `['たのむ', 'よく たのむ', 'まいにち たのむ', 'いま たのむ']`

### とまる (`n5.vocab.27-verbs-group-1-verbs.とまる`)
current particle_examples: `['とまる', 'とまるます', 'とまるました', 'よく とまる', 'まいにち とまる', 'いま とまる']`

- shared-tail signal (template-generation):
  - tail `とまる`: `['とまる', 'よく とまる', 'まいにち とまる', 'いま とまる']`

### おく (`n5.vocab.27-verbs-group-1-verbs.おく`)
current particle_examples: `['おくまい', '一おく人ぐらい', 'つくえに おく', 'すぐに おく', 'いえに おく', 'たいせつな ものを おく', 'はこに おく', 'もとの ところに おく']`

- shared-tail signal (template-generation):
  - tail ` おく`: `['つくえに おく', 'すぐに おく', 'いえに おく', 'たいせつな ものを おく', 'はこに おく', 'もとの ところに おく']`

### さく (`n5.vocab.27-verbs-group-1-verbs.さく`)
current particle_examples: `['さく', 'さくます', 'さくました', 'よく さく', 'まいにち さく', 'いま さく']`

- shared-tail signal (template-generation):
  - tail ` さく`: `['よく さく', 'まいにち さく', 'いま さく']`

### かかる (`n5.vocab.27-verbs-group-1-verbs.かかる`)
current particle_examples: `['時間がかかる', 'お金がかかる', '一時間かかる', 'じかんが かかる', 'お金が かかる', 'いちじかん かかる', 'たくさん かかる', 'すこし かかる', 'おもいきり かかる']`

- shared-tail signal (template-generation):
  - tail `かかる`: `['時間がかかる', 'お金がかかる', '一時間かかる', 'じかんが かかる', 'お金が かかる', 'いちじかん かかる', 'たくさん かかる', 'すこし かかる', 'おもいきり かかる']`

### さす (`n5.vocab.27-verbs-group-1-verbs.さす`)
current particle_examples: `['さす', 'さすます', 'さすました', 'よく さす', 'まいにち さす', 'いま さす']`

- shared-tail signal (template-generation):
  - tail ` さす`: `['よく さす', 'まいにち さす', 'いま さす']`

### けす (`n5.vocab.27-verbs-group-1-verbs.けす`)
current particle_examples: `['けす', 'けすます', 'けすました', 'よく けす', 'まいにち けす', 'いま けす']`

- shared-tail signal (template-generation):
  - tail ` けす`: `['よく けす', 'まいにち けす', 'いま けす']`

### いる (`n5.vocab.28-verbs-group-2-verbs.いる`)
current particle_examples: `['お金がいる', '時間がいる', 'そこに いる', 'いっしょに いる', 'うちに いる', 'まだ いる', 'かいしゃに いる', 'ともだちが いる']`

- shared-tail signal (template-generation):
  - tail ` いる`: `['そこに いる', 'いっしょに いる', 'うちに いる', 'まだ いる', 'かいしゃに いる', 'ともだちが いる']`

### 食べる (`n5.vocab.28-verbs-group-2-verbs.食べる`)
reading: `たべる`  
current particle_examples: `['食べる', '食べるます', '食べるました', 'よく 食べる', 'まいにち 食べる', 'いま 食べる']`

- shared-tail signal (template-generation):
  - tail `食べる`: `['食べる', 'よく 食べる', 'まいにち 食べる', 'いま 食べる']`

### 見る (`n5.vocab.28-verbs-group-2-verbs.見る`)
reading: `みる`  
current particle_examples: `['見るだけです', 'えいがを 見る', 'テレビを 見る', 'ゆめを 見る', 'よく 見る', 'おもしろい ものを 見る', 'はじめて 見る']`

- shared-tail signal (template-generation):
  - tail ` 見る`: `['えいがを 見る', 'テレビを 見る', 'ゆめを 見る', 'よく 見る', 'おもしろい ものを 見る', 'はじめて 見る']`

### ねる (`n5.vocab.28-verbs-group-2-verbs.ねる`)
current particle_examples: `['ねる', 'ねるます', 'ねるました', 'よく ねる', 'まいにち ねる', 'いま ねる']`

- shared-tail signal (template-generation):
  - tail ` ねる`: `['よく ねる', 'まいにち ねる', 'いま ねる']`

### おきる (`n5.vocab.28-verbs-group-2-verbs.おきる`)
current particle_examples: `['おきる', 'おきるます', 'おきるました', 'よく おきる', 'まいにち おきる', 'いま おきる']`

- shared-tail signal (template-generation):
  - tail `おきる`: `['おきる', 'よく おきる', 'まいにち おきる', 'いま おきる']`

### 出る (`n5.vocab.28-verbs-group-2-verbs.出る`)
reading: `でる`  
current particle_examples: `['出る', '出るます', '出るました', 'よく 出る', 'まいにち 出る', 'いま 出る']`

- shared-tail signal (template-generation):
  - tail ` 出る`: `['よく 出る', 'まいにち 出る', 'いま 出る']`

### 入れる (`n5.vocab.28-verbs-group-2-verbs.入れる`)
reading: `いれる`  
current particle_examples: `['入れる', '入れるます', '入れるました', 'よく 入れる', 'まいにち 入れる', 'いま 入れる']`

- shared-tail signal (template-generation):
  - tail `入れる`: `['入れる', 'よく 入れる', 'まいにち 入れる', 'いま 入れる']`

### あける (`n5.vocab.28-verbs-group-2-verbs.あける`)
current particle_examples: `['あける', 'あけるます', 'あけるました', 'よく あける', 'まいにち あける', 'いま あける']`

- shared-tail signal (template-generation):
  - tail `あける`: `['あける', 'よく あける', 'まいにち あける', 'いま あける']`

### しめる (`n5.vocab.28-verbs-group-2-verbs.しめる`)
current particle_examples: `['しめる', 'しめるます', 'しめるました', 'よく しめる', 'まいにち しめる', 'いま しめる']`

- shared-tail signal (template-generation):
  - tail `しめる`: `['しめる', 'よく しめる', 'まいにち しめる', 'いま しめる']`

### おしえる (`n5.vocab.28-verbs-group-2-verbs.おしえる`)
current particle_examples: `['おしえる', 'おしえるます', 'おしえるました', 'よく おしえる', 'まいにち おしえる', 'いま おしえる']`

- shared-tail signal (template-generation):
  - tail `しえる`: `['おしえる', 'よく おしえる', 'まいにち おしえる', 'いま おしえる']`

### おぼえる (`n5.vocab.28-verbs-group-2-verbs.おぼえる`)
current particle_examples: `['おぼえる', 'おぼえるます', 'おぼえるました', 'よく おぼえる', 'まいにち おぼえる', 'いま おぼえる']`

- shared-tail signal (template-generation):
  - tail `ぼえる`: `['おぼえる', 'よく おぼえる', 'まいにち おぼえる', 'いま おぼえる']`

### わすれる (`n5.vocab.28-verbs-group-2-verbs.わすれる`)
current particle_examples: `['わすれる', 'わすれるます', 'わすれるました', 'よく わすれる', 'まいにち わすれる', 'いま わすれる']`

- shared-tail signal (template-generation):
  - tail `すれる`: `['わすれる', 'よく わすれる', 'まいにち わすれる', 'いま わすれる']`

### かりる (`n5.vocab.28-verbs-group-2-verbs.かりる`)
current particle_examples: `['かりる', 'かりるます', 'かりるました', 'よく かりる', 'まいにち かりる', 'いま かりる']`

- shared-tail signal (template-generation):
  - tail `かりる`: `['かりる', 'よく かりる', 'まいにち かりる', 'いま かりる']`

### こたえる (`n5.vocab.28-verbs-group-2-verbs.こたえる`)
current particle_examples: `['こたえる', 'こたえるます', 'こたえるました', 'よく こたえる', 'まいにち こたえる', 'いま こたえる']`

- shared-tail signal (template-generation):
  - tail `たえる`: `['こたえる', 'よく こたえる', 'まいにち こたえる', 'いま こたえる']`

### 出かける (`n5.vocab.28-verbs-group-2-verbs.出かける`)
reading: `でかける`  
current particle_examples: `['出かける', '出かけるます', '出かけるました', 'よく 出かける', 'まいにち 出かける', 'いま 出かける']`

- shared-tail signal (template-generation):
  - tail `かける`: `['出かける', 'よく 出かける', 'まいにち 出かける', 'いま 出かける']`

### かける (`n5.vocab.28-verbs-group-2-verbs.かける`)
current particle_examples: `['かける', 'かけるます', 'かけるました', 'よく かける', 'まいにち かける', 'いま かける']`

- shared-tail signal (template-generation):
  - tail `かける`: `['かける', 'よく かける', 'まいにち かける', 'いま かける']`

### きる (`n5.vocab.28-verbs-group-2-verbs.きる`)
current particle_examples: `['きる', 'きるます', 'きるました', 'よく きる', 'まいにち きる', 'いま きる']`

- shared-tail signal (template-generation):
  - tail ` きる`: `['よく きる', 'まいにち きる', 'いま きる']`

### つける (`n5.vocab.28-verbs-group-2-verbs.つける`)
current particle_examples: `['電気をつける', 'テレビをつける', '気をつける', '電気を つける', 'テレビを つける', '名前を つける', 'きを つける', 'スイッチを つける', 'マークを つける']`

- shared-tail signal (template-generation):
  - tail `つける`: `['電気をつける', 'テレビをつける', '気をつける', '電気を つける', 'テレビを つける', '名前を つける', 'きを つける', 'スイッチを つける', 'マークを つける']`

### ならべる (`n5.vocab.28-verbs-group-2-verbs.ならべる`)
current particle_examples: `['ならべる', 'ならべるます', 'ならべるました', 'よく ならべる', 'まいにち ならべる', 'いま ならべる']`

- shared-tail signal (template-generation):
  - tail `らべる`: `['ならべる', 'よく ならべる', 'まいにち ならべる', 'いま ならべる']`

### はじめる (`n5.vocab.28-verbs-group-2-verbs.はじめる`)
current particle_examples: `['はじめる', 'はじめるます', 'はじめるました', 'よく はじめる', 'まいにち はじめる', 'いま はじめる']`

- shared-tail signal (template-generation):
  - tail `じめる`: `['はじめる', 'よく はじめる', 'まいにち はじめる', 'いま はじめる']`

### 見せる (`n5.vocab.28-verbs-group-2-verbs.見せる`)
reading: `みせる`  
current particle_examples: `['見せる', '見せるます', '見せるました', 'よく 見せる', 'まいにち 見せる', 'いま 見せる']`

- shared-tail signal (template-generation):
  - tail `見せる`: `['見せる', 'よく 見せる', 'まいにち 見せる', 'いま 見せる']`

### あびる (`n5.vocab.28-verbs-group-2-verbs.あびる`)
current particle_examples: `['あびる', 'あびるます', 'あびるました', 'よく あびる', 'まいにち あびる', 'いま あびる']`

- shared-tail signal (template-generation):
  - tail `あびる`: `['あびる', 'よく あびる', 'まいにち あびる', 'いま あびる']`

### いれる (`n5.vocab.28-verbs-group-2-verbs.いれる`)
current particle_examples: `['いれる', 'いれるます', 'いれるました', 'よく いれる', 'まいにち いれる', 'いま いれる']`

- shared-tail signal (template-generation):
  - tail `いれる`: `['いれる', 'よく いれる', 'まいにち いれる', 'いま いれる']`

### あつめる (`n5.vocab.28-verbs-group-2-verbs.あつめる`)
current particle_examples: `['あつめる', 'あつめるます', 'あつめるました', 'よく あつめる', 'まいにち あつめる', 'いま あつめる']`

- shared-tail signal (template-generation):
  - tail `つめる`: `['あつめる', 'よく あつめる', 'まいにち あつめる', 'いま あつめる']`

### きえる (`n5.vocab.28-verbs-group-2-verbs.きえる`)
current particle_examples: `['きえる', 'きえるます', 'きえるました', 'よく きえる', 'まいにち きえる', 'いま きえる']`

- shared-tail signal (template-generation):
  - tail `きえる`: `['きえる', 'よく きえる', 'まいにち きえる', 'いま きえる']`

### おちる (`n5.vocab.28-verbs-group-2-verbs.おちる`)
current particle_examples: `['おちる', 'おちるます', 'おちるました', 'よく おちる', 'まいにち おちる', 'いま おちる']`

- shared-tail signal (template-generation):
  - tail `おちる`: `['おちる', 'よく おちる', 'まいにち おちる', 'いま おちる']`

### はれる (`n5.vocab.28-verbs-group-2-verbs.はれる`)
current particle_examples: `['はれる', 'はれるます', 'はれるました', 'よく はれる', 'まいにち はれる', 'いま はれる']`

- shared-tail signal (template-generation):
  - tail `はれる`: `['はれる', 'よく はれる', 'まいにち はれる', 'いま はれる']`

### つかれる (`n5.vocab.28-verbs-group-2-verbs.つかれる`)
current particle_examples: `['つかれる', 'つかれるます', 'つかれるました', 'よく つかれる', 'まいにち つかれる', 'いま つかれる']`

- shared-tail signal (template-generation):
  - tail `かれる`: `['つかれる', 'よく つかれる', 'まいにち つかれる', 'いま つかれる']`

### 生まれる (`n5.vocab.28-verbs-group-2-verbs.生まれる`)
reading: `うまれる`  
current particle_examples: `['生まれる', '生まれるます', '生まれるました', 'よく 生まれる', 'まいにち 生まれる', 'いま 生まれる']`

- shared-tail signal (template-generation):
  - tail `まれる`: `['生まれる', 'よく 生まれる', 'まいにち 生まれる', 'いま 生まれる']`

### おりる (`n5.vocab.28-verbs-group-2-verbs.おりる`)
current particle_examples: `['おりる', 'おりるます', 'おりるました', 'よく おりる', 'まいにち おりる', 'いま おりる']`

- shared-tail signal (template-generation):
  - tail `おりる`: `['おりる', 'よく おりる', 'まいにち おりる', 'いま おりる']`

### しめる (`n5.vocab.28-verbs-group-2-verbs.しめる.2`)
current particle_examples: `['しめる', 'しめるます', 'しめるました', 'よく しめる', 'まいにち しめる', 'いま しめる']`

- shared-tail signal (template-generation):
  - tail `しめる`: `['しめる', 'よく しめる', 'まいにち しめる', 'いま しめる']`

### つとめる (`n5.vocab.28-verbs-group-2-verbs.つとめる`)
current particle_examples: `['つとめる', 'つとめるます', 'つとめるました', 'よく つとめる', 'まいにち つとめる', 'いま つとめる']`

- shared-tail signal (template-generation):
  - tail `とめる`: `['つとめる', 'よく つとめる', 'まいにち つとめる', 'いま つとめる']`

### する (`n5.vocab.29-verbs-irregular-and-v.する`)
current particle_examples: `['んするつもりで', '電話するつ', 'さんぽするこ', 'ぽすることが', 'うすることが', 'しごとするこ', 'とすることが', 'コピーするこ']`

- shared-tail signal (template-generation):
  - tail `するこ`: `['さんぽするこ', 'しごとするこ', 'コピーするこ']`
  - tail `ことが`: `['ぽすることが', 'うすることが', 'とすることが']`

### 来る (`n5.vocab.29-verbs-irregular-and-v.来る`)
reading: `くる`  
current particle_examples: `['くるまが', 'くるまで', 'もってくるつ', 'てくるつもりで', 'ともだちが 来る', 'まいにち 来る', 'はやく 来てください', 'いっしょに 来る', '日本に 来る', '電車が 来る']`

- shared-tail signal (template-generation):
  - tail ` 来る`: `['ともだちが 来る', 'まいにち 来る', 'いっしょに 来る', '日本に 来る', '電車が 来る']`

### べんきょうする (`n5.vocab.29-verbs-irregular-and-v.べんきょうする`)
current particle_examples: `['べんきょうする', 'べんきょうするます', 'べんきょうするました', 'よく べんきょうする', 'まいにち べんきょうする', 'いま べんきょうする']`

- shared-tail signal (template-generation):
  - tail `うする`: `['べんきょうする', 'よく べんきょうする', 'まいにち べんきょうする', 'いま べんきょうする']`

### けっこんする (`n5.vocab.29-verbs-irregular-and-v.けっこんする`)
current particle_examples: `['けっこんする', 'けっこんするます', 'けっこんするました', 'よく けっこんする', 'まいにち けっこんする', 'いま けっこんする']`

- shared-tail signal (template-generation):
  - tail `んする`: `['けっこんする', 'よく けっこんする', 'まいにち けっこんする', 'いま けっこんする']`

### さんぽする (`n5.vocab.29-verbs-irregular-and-v.さんぽする`)
current particle_examples: `['さんぽする', 'さんぽするます', 'さんぽするました', 'よく さんぽする', 'まいにち さんぽする', 'いま さんぽする']`

- shared-tail signal (template-generation):
  - tail `ぽする`: `['さんぽする', 'よく さんぽする', 'まいにち さんぽする', 'いま さんぽする']`

### りょこうする (`n5.vocab.29-verbs-irregular-and-v.りょこうする`)
current particle_examples: `['りょこうする', 'りょこうするます', 'りょこうするました', 'よく りょこうする', 'まいにち りょこうする', 'いま りょこうする']`

- shared-tail signal (template-generation):
  - tail `うする`: `['りょこうする', 'よく りょこうする', 'まいにち りょこうする', 'いま りょこうする']`

### しつもんする (`n5.vocab.29-verbs-irregular-and-v.しつもんする`)
current particle_examples: `['しつもんする', 'しつもんするます', 'しつもんするました', 'よく しつもんする', 'まいにち しつもんする', 'いま しつもんする']`

- shared-tail signal (template-generation):
  - tail `んする`: `['しつもんする', 'よく しつもんする', 'まいにち しつもんする', 'いま しつもんする']`

### しごとする (`n5.vocab.29-verbs-irregular-and-v.しごとする`)
current particle_examples: `['しごとする', 'しごとするます', 'しごとするました', 'よく しごとする', 'まいにち しごとする', 'いま しごとする']`

- shared-tail signal (template-generation):
  - tail `とする`: `['しごとする', 'よく しごとする', 'まいにち しごとする', 'いま しごとする']`

### 電話する (`n5.vocab.29-verbs-irregular-and-v.電話する`)
reading: `でんわする`  
current particle_examples: `['電話する', '電話するます', '電話するました', 'よく 電話する', 'まいにち 電話する', 'いま 電話する']`

- shared-tail signal (template-generation):
  - tail `話する`: `['電話する', 'よく 電話する', 'まいにち 電話する', 'いま 電話する']`

### コピーする (`n5.vocab.29-verbs-irregular-and-v.コピーする`)
current particle_examples: `['コピーする', 'コピーするます', 'コピーするました', 'よく コピーする', 'まいにち コピーする', 'いま コピーする']`

- shared-tail signal (template-generation):
  - tail `ーする`: `['コピーする', 'よく コピーする', 'まいにち コピーする', 'いま コピーする']`

### そうじする (`n5.vocab.29-verbs-irregular-and-v.そうじする`)
current particle_examples: `['そうじする', 'そうじするます', 'そうじするました', 'よく そうじする', 'まいにち そうじする', 'いま そうじする']`

- shared-tail signal (template-generation):
  - tail `じする`: `['そうじする', 'よく そうじする', 'まいにち そうじする', 'いま そうじする']`

### せんたくする (`n5.vocab.29-verbs-irregular-and-v.せんたくする`)
current particle_examples: `['せんたくする', 'せんたくするます', 'せんたくするました', 'よく せんたくする', 'まいにち せんたくする', 'いま せんたくする']`

- shared-tail signal (template-generation):
  - tail `くする`: `['せんたくする', 'よく せんたくする', 'まいにち せんたくする', 'いま せんたくする']`

### かいものする (`n5.vocab.29-verbs-irregular-and-v.かいものする`)
current particle_examples: `['かいものする', 'かいものするます', 'かいものするました', 'よく かいものする', 'まいにち かいものする', 'いま かいものする']`

- shared-tail signal (template-generation):
  - tail `のする`: `['かいものする', 'よく かいものする', 'まいにち かいものする', 'いま かいものする']`

### ある (`n5.vocab.30-verbs-existence-and-p.ある`)
current particle_examples: `['ある', 'あるます', 'あるました', 'よく ある', 'まいにち ある', 'いま ある']`

- shared-tail signal (template-generation):
  - tail ` ある`: `['よく ある', 'まいにち ある', 'いま ある']`

### いる (`n5.vocab.30-verbs-existence-and-p.いる.2`)
current particle_examples: `['そこに いる', 'いっしょに いる', 'うちに いる', 'まだ いる', 'かいしゃに いる', 'ともだちが いる']`

- shared-tail signal (template-generation):
  - tail ` いる`: `['そこに いる', 'いっしょに いる', 'うちに いる', 'まだ いる', 'かいしゃに いる', 'ともだちが いる']`

### やる (`n5.vocab.30-verbs-existence-and-p.やる`)
current particle_examples: `['やる', 'やるます', 'やるました', 'よく やる', 'まいにち やる', 'いま やる']`

- shared-tail signal (template-generation):
  - tail ` やる`: `['よく やる', 'まいにち やる', 'いま やる']`

### あげる (`n5.vocab.30-verbs-existence-and-p.あげる`)
current particle_examples: `['プレゼントを あげる', 'おかしを あげる', 'ともだちに あげる', '本を あげる', 'お金を あげる', 'はなを あげる']`

- shared-tail signal (template-generation):
  - tail `あげる`: `['プレゼントを あげる', 'おかしを あげる', 'ともだちに あげる', '本を あげる', 'お金を あげる', 'はなを あげる']`

### もらう (`n5.vocab.30-verbs-existence-and-p.もらう`)
current particle_examples: `['もらう', 'もらうます', 'もらうました', 'よく もらう', 'まいにち もらう', 'いま もらう']`

- shared-tail signal (template-generation):
  - tail `もらう`: `['もらう', 'よく もらう', 'まいにち もらう', 'いま もらう']`

### くれる (`n5.vocab.30-verbs-existence-and-p.くれる`)
current particle_examples: `['くれる人が', 'おくれるつもりで', 'ともだちが くれる', 'プレゼントを くれる', '本を くれる', '時間を くれる', 'おかしを くれる', 'おしえて くれる']`

- shared-tail signal (template-generation):
  - tail `くれる`: `['ともだちが くれる', 'プレゼントを くれる', '本を くれる', '時間を くれる', 'おかしを くれる', 'おしえて くれる']`

### かす (`n5.vocab.30-verbs-existence-and-p.かす`)
current particle_examples: `['かす', 'かすます', 'かすました', 'よく かす', 'まいにち かす', 'いま かす']`

- shared-tail signal (template-generation):
  - tail ` かす`: `['よく かす', 'まいにち かす', 'いま かす']`

### かえす (`n5.vocab.30-verbs-existence-and-p.かえす`)
current particle_examples: `['かえす', 'かえすます', 'かえすました', 'よく かえす', 'まいにち かえす', 'いま かえす']`

- shared-tail signal (template-generation):
  - tail `かえす`: `['かえす', 'よく かえす', 'まいにち かえす', 'いま かえす']`

### うれしい (`n5.vocab.31-adjectives.うれしい`)
current particle_examples: `['とてもうれしい', '会えてうれしい', 'うれしい きもち', 'うれしくて なく', 'とても うれしい', 'うれしい ニュース', 'うれしい ひ', 'うれしい こと']`

- shared-tail signal (template-generation):
  - tail `れしい`: `['とてもうれしい', '会えてうれしい', 'とても うれしい']`

### くらい (`n5.vocab.31-adjectives.くらい`)
current particle_examples: `['円くらいです', '分くらいです', '五ふん くらい', 'いちじかん くらい', 'これ くらい', 'にじゅっぷん くらい', 'いっしゅうかん くらい', 'どれ くらい']`

- shared-tail signal (template-generation):
  - tail `くらい`: `['五ふん くらい', 'いちじかん くらい', 'これ くらい', 'にじゅっぷん くらい', 'いっしゅうかん くらい', 'どれ くらい']`

### ほしい (`n5.vocab.31-adjectives.ほしい`)
current particle_examples: `['くるまが ほしい', '時間が ほしい', '本が ほしい', 'お金が ほしい', '休みが ほしい', '新しい ものが ほしい']`

- shared-tail signal (template-generation):
  - tail `ほしい`: `['くるまが ほしい', '時間が ほしい', '本が ほしい', 'お金が ほしい', '休みが ほしい', '新しい ものが ほしい']`

### まず (`n5.vocab.33-adverbs.まず`)
current particle_examples: `['まず 食べる', 'まず こたえる', 'まず やってみる', 'まず しゅくだいを する', 'まず きく', 'まず よむ']`

- template-shape hits:
  - shape `を する` in `まず しゅくだいを する`

### そして (`n5.vocab.34-conjunctions.そして`)
current particle_examples: `['AはBです。そして、CはDです。', 'おいしい。そして、 たかい。', 'たべました。そして、 ねます。', 'そして、 いきましょう。', 'そして、 おわります。', 'いきます。そして、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。そして、 ねます。', 'そして、 おわります。', 'いきます。そして、 かえります。']`

### それから (`n5.vocab.34-conjunctions.それから`)
current particle_examples: `['AはBです。それから、CはDです。', 'おいしい。それから、 たかい。', 'たべました。それから、 ねます。', 'それから、 いきましょう。', 'それから、 おわります。', 'いきます。それから、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。それから、 ねます。', 'それから、 おわります。', 'いきます。それから、 かえります。']`

### それで (`n5.vocab.34-conjunctions.それで`)
current particle_examples: `['AはBです。それで、CはDです。', 'おいしい。それで、 たかい。', 'たべました。それで、 ねます。', 'それで、 いきましょう。', 'それで、 おわります。', 'いきます。それで、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。それで、 ねます。', 'それで、 おわります。', 'いきます。それで、 かえります。']`

### でも (`n5.vocab.34-conjunctions.でも`)
current particle_examples: `['AはBです。でも、CはDです。', 'おいしい。でも、 たかい。', 'たべました。でも、 ねます。', 'でも、 いきましょう。', 'でも、 おわります。', 'いきます。でも、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。でも、 ねます。', 'でも、 おわります。', 'いきます。でも、 かえります。']`

### しかし (`n5.vocab.34-conjunctions.しかし`)
current particle_examples: `['AはBです。しかし、CはDです。', 'おいしい。しかし、 たかい。', 'たべました。しかし、 ねます。', 'しかし、 いきましょう。', 'しかし、 おわります。', 'いきます。しかし、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。しかし、 ねます。', 'しかし、 おわります。', 'いきます。しかし、 かえります。']`

### が (`n5.vocab.34-conjunctions.が`)
current particle_examples: `['AはBです。が、CはDです。', 'おいしい。が、 たかい。', 'たべました。が、 ねます。', 'が、 いきましょう。', 'が、 おわります。', 'いきます。が、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。が、 ねます。', 'が、 おわります。', 'いきます。が、 かえります。']`

### から (`n5.vocab.34-conjunctions.から`)
current particle_examples: `['AはBです。から、CはDです。', 'おいしい。から、 たかい。', 'たべました。から、 ねます。', 'から、 いきましょう。', 'から、 おわります。', 'いきます。から、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。から、 ねます。', 'から、 おわります。', 'いきます。から、 かえります。']`

### だから (`n5.vocab.34-conjunctions.だから`)
current particle_examples: `['AはBです。だから、CはDです。', 'おいしい。だから、 たかい。', 'たべました。だから、 ねます。', 'だから、 いきましょう。', 'だから、 おわります。', 'いきます。だから、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。だから、 ねます。', 'だから、 おわります。', 'いきます。だから、 かえります。']`

### ですから (`n5.vocab.34-conjunctions.ですから`)
current particle_examples: `['AはBです。ですから、CはDです。', 'おいしい。ですから、 たかい。', 'たべました。ですから、 ねます。', 'ですから、 いきましょう。', 'ですから、 おわります。', 'いきます。ですから、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。ですから、 ねます。', 'ですから、 おわります。', 'いきます。ですから、 かえります。']`

### それに (`n5.vocab.34-conjunctions.それに`)
current particle_examples: `['AはBです。それに、CはDです。', 'おいしい。それに、 たかい。', 'たべました。それに、 ねます。', 'それに、 いきましょう。', 'それに、 おわります。', 'いきます。それに、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。それに、 ねます。', 'それに、 おわります。', 'いきます。それに、 かえります。']`

### ところで (`n5.vocab.34-conjunctions.ところで`)
current particle_examples: `['AはBです。ところで、CはDです。', 'おいしい。ところで、 たかい。', 'たべました。ところで、 ねます。', 'ところで、 いきましょう。', 'ところで、 おわります。', 'いきます。ところで、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。ところで、 ねます。', 'ところで、 おわります。', 'いきます。ところで、 かえります。']`

### または (`n5.vocab.34-conjunctions.または`)
current particle_examples: `['AはBです。または、CはDです。', 'おいしい。または、 たかい。', 'たべました。または、 ねます。', 'または、 いきましょう。', 'または、 おわります。', 'いきます。または、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。または、 ねます。', 'または、 おわります。', 'いきます。または、 かえります。']`

### もの (`n5.vocab.37-common-nouns-miscella.もの`)
current particle_examples: `['かいものを', 'たてものは', 'のみものは', 'くだものが', 'くだものを', '買いものを', 'たべものが', 'たべものは']`

- shared-tail signal (template-generation):
  - tail `ものを`: `['かいものを', 'くだものを', '買いものを']`
  - tail `ものは`: `['たてものは', 'のみものは', 'たべものは']`

### こと (`n5.vocab.37-common-nouns-miscella.こと`)
current particle_examples: `['行ったことが', '食べたことが', 'ことばを', '聞くことが', 'しることが', 'はくことが', 'ひくことが', 'はることが']`

- shared-tail signal (template-generation):
  - tail `ことが`: `['行ったことが', '食べたことが', '聞くことが', 'しることが', 'はくことが', 'ひくことが', 'はることが']`

### 名前 (`n5.vocab.37-common-nouns-miscella.名前`)
reading: `なまえ`  
current particle_examples: `['名前を おしえてください', 'すきな 名前', 'こどもの 名前', 'みせの 名前', '名前を よぶ', '名前を おぼえる']`

- shared-tail signal (template-generation):
  - tail ` 名前`: `['すきな 名前', 'こどもの 名前', 'みせの 名前']`

### 話 (`n5.vocab.37-common-nouns-miscella.話`)
reading: `はなし`  
current particle_examples: `['話を かう', '話を つかう', 'あたらしい 話', 'たかい 話', '話を ください', '話は どこ', '話を みる', 'やすい 話']`

- shared-tail signal (template-generation):
  - tail `い 話`: `['あたらしい 話', 'たかい 話', 'やすい 話']`

### しごと (`n5.vocab.37-common-nouns-miscella.しごと`)
current particle_examples: `['しごとが ある', 'しごとが ない', 'しごとを いう', 'しごとを きく', 'いい しごと', 'しごとの とき', 'しごとを おもう', 'しごとを しる']`

- template-shape hits:
  - shape `を しる` in `しごとを しる`

### やくそく (`n5.vocab.37-common-nouns-miscella.やくそく`)
current particle_examples: `['やくそくを かう', 'やくそくを つかう', 'あたらしい やくそく', 'たかい やくそく', 'やくそくを ください', 'やくそくは どこ', 'やくそくを みる', 'やすい やくそく']`

- shared-tail signal (template-generation):
  - tail `くそく`: `['あたらしい やくそく', 'たかい やくそく', 'やすい やくそく']`

### ようじ (`n5.vocab.37-common-nouns-miscella.ようじ`)
current particle_examples: `['ようじを かう', 'ようじを つかう', 'あたらしい ようじ', 'たかい ようじ', 'ようじを ください', 'ようじは どこ', 'ようじを みる', 'やすい ようじ']`

- shared-tail signal (template-generation):
  - tail `ようじ`: `['あたらしい ようじ', 'たかい ようじ', 'やすい ようじ']`

### もんだい (`n5.vocab.37-common-nouns-miscella.もんだい`)
current particle_examples: `['もんだいが ある', 'もんだいが ない', 'もんだいを いう', 'もんだいを きく', 'いい もんだい', 'もんだいの とき', 'もんだいを おもう', 'もんだいを しる']`

- template-shape hits:
  - shape `を しる` in `もんだいを しる`

### しゅみ (`n5.vocab.37-common-nouns-miscella.しゅみ`)
current particle_examples: `['しゅみを かう', 'しゅみを つかう', 'あたらしい しゅみ', 'たかい しゅみ', 'しゅみを ください', 'しゅみは どこ', 'しゅみを みる', 'やすい しゅみ']`

- shared-tail signal (template-generation):
  - tail `しゅみ`: `['あたらしい しゅみ', 'たかい しゅみ', 'やすい しゅみ']`

### りょこう (`n5.vocab.37-common-nouns-miscella.りょこう`)
current particle_examples: `['りょこうが ある', 'りょこうが ない', 'りょこうを いう', 'りょこうを きく', 'いい りょこう', 'りょこうの とき', 'りょこうを おもう', 'りょこうを しる']`

- template-shape hits:
  - shape `を しる` in `りょこうを しる`

### さんぽ (`n5.vocab.37-common-nouns-miscella.さんぽ`)
current particle_examples: `['さんぽを かう', 'さんぽを つかう', 'あたらしい さんぽ', 'たかい さんぽ', 'さんぽを ください', 'さんぽは どこ', 'さんぽを みる', 'やすい さんぽ']`

- shared-tail signal (template-generation):
  - tail `さんぽ`: `['あたらしい さんぽ', 'たかい さんぽ', 'やすい さんぽ']`

### うんどう (`n5.vocab.37-common-nouns-miscella.うんどう`)
current particle_examples: `['うんどうが ある', 'うんどうが ない', 'うんどうを いう', 'うんどうを きく', 'いい うんどう', 'うんどうの とき', 'うんどうを おもう', 'うんどうを しる']`

- template-shape hits:
  - shape `を しる` in `うんどうを しる`

### ゲーム (`n5.vocab.37-common-nouns-miscella.ゲーム`)
current particle_examples: `['ゲームを する', 'ビデオ ゲーム', 'おもしろい ゲーム', 'ゲームに かつ', 'ゲームの じかん', '新しい ゲーム']`

- template-shape hits:
  - shape `を する` in `ゲームを する`
- shared-tail signal (template-generation):
  - tail `ゲーム`: `['ビデオ ゲーム', 'おもしろい ゲーム', '新しい ゲーム']`

### スポーツ (`n5.vocab.37-common-nouns-miscella.スポーツ`)
current particle_examples: `['スポーツが ある', 'スポーツが ない', 'スポーツを いう', 'スポーツを きく', 'いい スポーツ', 'スポーツの とき', 'スポーツを おもう', 'スポーツを しる']`

- template-shape hits:
  - shape `を しる` in `スポーツを しる`

### しあい (`n5.vocab.37-common-nouns-miscella.しあい`)
current particle_examples: `['しあいが ある', 'しあいが ない', 'しあいを いう', 'しあいを きく', 'いい しあい', 'しあいの とき', 'しあいを おもう', 'しあいを しる']`

- template-shape hits:
  - shape `を しる` in `しあいを しる`

### ニュース (`n5.vocab.37-common-nouns-miscella.ニュース`)
current particle_examples: `['ニュースを みる', 'いい ニュース', 'わるい ニュース', 'あさの ニュース', 'ニュースの じかん', 'おもしろい ニュース']`

- shared-tail signal (template-generation):
  - tail `ュース`: `['いい ニュース', 'わるい ニュース', 'あさの ニュース', 'おもしろい ニュース']`

### パーティー (`n5.vocab.37-common-nouns-miscella.パーティー`)
current particle_examples: `['パーティーには', 'パーティーに いく', 'パーティーを する', 'たんじょうびの パーティー', 'たのしい パーティー', 'パーティーの ばしょ', '大きな パーティー']`

- template-shape hits:
  - shape `を する` in `パーティーを する`
  - shape `に いく` in `パーティーに いく`
- shared-tail signal (template-generation):
  - tail `ティー`: `['たんじょうびの パーティー', 'たのしい パーティー', '大きな パーティー']`

### りゅうがく (`n5.vocab.37-common-nouns-miscella.りゅうがく`)
current particle_examples: `['りゅうがくが ある', 'りゅうがくが ない', 'りゅうがくを いう', 'りゅうがくを きく', 'いい りゅうがく', 'りゅうがくの とき', 'りゅうがくを おもう', 'りゅうがくを しる']`

- template-shape hits:
  - shape `を しる` in `りゅうがくを しる`

### けっこん (`n5.vocab.37-common-nouns-miscella.けっこん`)
current particle_examples: `['けっこんが ある', 'けっこんが ない', 'けっこんを いう', 'けっこんを きく', 'いい けっこん', 'けっこんの とき', 'けっこんを おもう', 'けっこんを しる']`

- template-shape hits:
  - shape `を しる` in `けっこんを しる`

### びょうき (`n5.vocab.37-common-nouns-miscella.びょうき`)
current particle_examples: `['びょうきを かう', 'びょうきを つかう', 'あたらしい びょうき', 'たかい びょうき', 'びょうきを ください', 'びょうきは どこ', 'びょうきを みる', 'やすい びょうき']`

- shared-tail signal (template-generation):
  - tail `ょうき`: `['あたらしい びょうき', 'たかい びょうき', 'やすい びょうき']`

### くすり (`n5.vocab.37-common-nouns-miscella.くすり`)
current particle_examples: `['くすりを かう', 'くすりを つかう', 'あたらしい くすり', 'たかい くすり', 'くすりを ください', 'くすりは どこ', 'くすりを みる', 'やすい くすり']`

- shared-tail signal (template-generation):
  - tail `くすり`: `['あたらしい くすり', 'たかい くすり', 'やすい くすり']`

### けが (`n5.vocab.37-common-nouns-miscella.けが`)
current particle_examples: `['けがを かう', 'けがを つかう', 'あたらしい けが', 'たかい けが', 'けがを ください', 'けがは どこ', 'けがを みる', 'やすい けが']`

- shared-tail signal (template-generation):
  - tail ` けが`: `['あたらしい けが', 'たかい けが', 'やすい けが']`

### はいざら (`n5.vocab.37-common-nouns-miscella.はいざら`)
current particle_examples: `['はいざらを かう', 'はいざらを つかう', 'あたらしい はいざら', 'たかい はいざら', 'はいざらを ください', 'はいざらは どこ', 'はいざらを みる', 'やすい はいざら']`

- shared-tail signal (template-generation):
  - tail `いざら`: `['あたらしい はいざら', 'たかい はいざら', 'やすい はいざら']`

### スリッパ (`n5.vocab.37-common-nouns-miscella.スリッパ`)
current particle_examples: `['スリッパを かう', 'スリッパを つかう', 'あたらしい スリッパ', 'たかい スリッパ', 'スリッパを ください', 'スリッパは どこ', 'スリッパを みる', 'やすい スリッパ']`

- shared-tail signal (template-generation):
  - tail `リッパ`: `['あたらしい スリッパ', 'たかい スリッパ', 'やすい スリッパ']`

### ティッシュ (`n5.vocab.37-common-nouns-miscella.ティッシュ`)
current particle_examples: `['ティッシュを かう', 'ティッシュを つかう', 'あたらしい ティッシュ', 'たかい ティッシュ', 'ティッシュを ください', 'ティッシュは どこ', 'ティッシュを みる', 'やすい ティッシュ']`

- shared-tail signal (template-generation):
  - tail `ッシュ`: `['あたらしい ティッシュ', 'たかい ティッシュ', 'やすい ティッシュ']`

### よてい (`n5.vocab.37-common-nouns-miscella.よてい`)
current particle_examples: `['よていを かう', 'よていを つかう', 'あたらしい よてい', 'たかい よてい', 'よていを ください', 'よていは どこ', 'よていを みる', 'やすい よてい']`

- shared-tail signal (template-generation):
  - tail `よてい`: `['あたらしい よてい', 'たかい よてい', 'やすい よてい']`

### じかんわり (`n5.vocab.37-common-nouns-miscella.じかんわり`)
current particle_examples: `['じかんわりが ある', 'じかんわりに いく', 'じかんわりまで まつ', 'じかんわりから はじまる', 'いま じかんわり', 'じかんわりは はやい', 'じかんわりを まつ', 'じかんわりが おわる']`

- template-shape hits:
  - shape `に いく` in `じかんわりに いく`

### はこ (`n5.vocab.37-common-nouns-miscella.はこ`)
current particle_examples: `['はこを かう', 'はこを つかう', 'あたらしい はこ', 'たかい はこ', 'はこを ください', 'はこは どこ', 'はこを みる', 'やすい はこ']`

- shared-tail signal (template-generation):
  - tail ` はこ`: `['あたらしい はこ', 'たかい はこ', 'やすい はこ']`

### はたち (`n5.vocab.37-common-nouns-miscella.はたち`)
current particle_examples: `['はたちが ある', 'はたちに いく', 'はたちまで まつ', 'はたちから はじまる', 'いま はたち', 'はたちは はやい', 'はたちを まつ', 'はたちが おわる']`

- template-shape hits:
  - shape `に いく` in `はたちに いく`

### なつやすみ (`n5.vocab.37-common-nouns-miscella.なつやすみ`)
current particle_examples: `['なつやすみが ある', 'なつやすみに いく', 'なつやすみまで まつ', 'なつやすみから はじまる', 'いま なつやすみ', 'なつやすみは はやい', 'なつやすみを まつ', 'なつやすみが おわる']`

- template-shape hits:
  - shape `に いく` in `なつやすみに いく`

### やすみ (`n5.vocab.37-common-nouns-miscella.やすみ`)
current particle_examples: `['やすみが ある', 'やすみに いく', 'やすみまで まつ', 'やすみから はじまる', 'いま やすみ', 'やすみは はやい', 'やすみを まつ', 'やすみが おわる']`

- template-shape hits:
  - shape `に いく` in `やすみに いく`

### りょうり (`n5.vocab.37-common-nouns-miscella.りょうり`)
current particle_examples: `['りょうりを かう', 'りょうりを つかう', 'あたらしい りょうり', 'たかい りょうり', 'りょうりを ください', 'りょうりは どこ', 'りょうりを みる', 'やすい りょうり']`

- shared-tail signal (template-generation):
  - tail `ょうり`: `['あたらしい りょうり', 'たかい りょうり', 'やすい りょうり']`

### かてい (`n5.vocab.37-common-nouns-miscella.かてい`)
current particle_examples: `['かていに いく', 'かていで あう', 'かていから くる', 'かていの まえに', 'かていが ある', 'かていは ちかい', 'かていまで あるく', 'かていに つく']`

- template-shape hits:
  - shape `に いく` in `かていに いく`

### かびん (`n5.vocab.37-common-nouns-miscella.かびん`)
current particle_examples: `['かびんを かう', 'かびんを つかう', 'あたらしい かびん', 'たかい かびん', 'かびんを ください', 'かびんは どこ', 'かびんを みる', 'やすい かびん']`

- shared-tail signal (template-generation):
  - tail `かびん`: `['あたらしい かびん', 'たかい かびん', 'やすい かびん']`

### おくさん (`n5.vocab.37-common-nouns-miscella.おくさん`)
current particle_examples: `['おくさんと あう', 'おくさんと はなす', 'おくさんに きく', 'おくさんは どこ', 'おくさんの なまえ', 'おくさんが くる', 'おくさんが いる', 'おくさんは やさしい']`

- template-shape hits:
  - shape `と あう` in `おくさんと あう`

### せびろ (`n5.vocab.37-common-nouns-miscella.せびろ`)
current particle_examples: `['せびろに いく', 'せびろで あう', 'せびろから くる', 'せびろの まえに', 'せびろが ある', 'せびろは ちかい', 'せびろまで あるく', 'せびろに つく']`

- template-shape hits:
  - shape `に いく` in `せびろに いく`

### ゆうべ (`n5.vocab.37-common-nouns-miscella.ゆうべ`)
current particle_examples: `['ゆうべが ある', 'ゆうべに いく', 'ゆうべまで まつ', 'ゆうべから はじまる', 'いま ゆうべ', 'ゆうべは はやい', 'ゆうべを まつ', 'ゆうべが おわる']`

- template-shape hits:
  - shape `に いく` in `ゆうべに いく`

### にっき (`n5.vocab.37-common-nouns-miscella.にっき`)
current particle_examples: `['にっきを かう', 'にっきを つかう', 'あたらしい にっき', 'たかい にっき', 'にっきを ください', 'にっきは どこ', 'にっきを みる', 'やすい にっき']`

- shared-tail signal (template-generation):
  - tail `にっき`: `['あたらしい にっき', 'たかい にっき', 'やすい にっき']`

### さくぶん (`n5.vocab.37-common-nouns-miscella.さくぶん`)
current particle_examples: `['さくぶんを かう', 'さくぶんを つかう', 'あたらしい さくぶん', 'たかい さくぶん', 'さくぶんを ください', 'さくぶんは どこ', 'さくぶんを みる', 'やすい さくぶん']`

- shared-tail signal (template-generation):
  - tail `くぶん`: `['あたらしい さくぶん', 'たかい さくぶん', 'やすい さくぶん']`

### じびき (`n5.vocab.37-common-nouns-miscella.じびき`)
current particle_examples: `['じびきを かう', 'じびきを つかう', 'あたらしい じびき', 'たかい じびき', 'じびきを ください', 'じびきは どこ', 'じびきを みる', 'やすい じびき']`

- shared-tail signal (template-generation):
  - tail `じびき`: `['あたらしい じびき', 'たかい じびき', 'やすい じびき']`

### テープレコーダー (`n5.vocab.37-common-nouns-miscella.テープレコーダー`)
current particle_examples: `['テープレコーダーを かう', 'テープレコーダーを つかう', 'あたらしい テープレコーダー', 'たかい テープレコーダー', 'テープレコーダーを ください', 'テープレコーダーは どこ', 'テープレコーダーを みる', 'やすい テープレコーダー']`

- shared-tail signal (template-generation):
  - tail `ーダー`: `['あたらしい テープレコーダー', 'たかい テープレコーダー', 'やすい テープレコーダー']`

### ストーブ (`n5.vocab.37-common-nouns-miscella.ストーブ`)
current particle_examples: `['ストーブを かう', 'ストーブを つかう', 'あたらしい ストーブ', 'たかい ストーブ', 'ストーブを ください', 'ストーブは どこ', 'ストーブを みる', 'やすい ストーブ']`

- shared-tail signal (template-generation):
  - tail `トーブ`: `['あたらしい ストーブ', 'たかい ストーブ', 'やすい ストーブ']`

### ページ (`n5.vocab.37-common-nouns-miscella.ページ`)
current particle_examples: `['二十ページを', 'ページを ひらく', 'つぎの ページ', 'いちページ', 'ページが ない', 'ページの すうじ', 'はじめの ページ']`

- shared-tail signal (template-generation):
  - tail `ページ`: `['つぎの ページ', 'いちページ', 'はじめの ページ']`

### グラム (`n5.vocab.37-common-nouns-miscella.グラム`)
current particle_examples: `['キログラムで', 'ログラムです', '五キログラムの', 'いちグラム', 'ひゃくグラム', 'グラムで はかる', 'グラムの けいさん', 'たくさんの グラム', 'グラムを みる']`

- shared-tail signal (template-generation):
  - tail `グラム`: `['いちグラム', 'ひゃくグラム', 'たくさんの グラム']`

### メートル (`n5.vocab.37-common-nouns-miscella.メートル`)
current particle_examples: `['ロメートルです', '三キロメートルで', 'いちメートル', 'ひゃくメートル', 'メートルで はかる', 'メートルの たかさ', 'メートルの ながさ', '十メートル']`

- shared-tail signal (template-generation):
  - tail `ートル`: `['いちメートル', 'ひゃくメートル', '十メートル']`

### キログラム (`n5.vocab.37-common-nouns-miscella.キログラム`)
current particle_examples: `['キログラムを かう', 'キログラムを つかう', 'あたらしい キログラム', 'たかい キログラム', 'キログラムを ください', 'キログラムは どこ', 'キログラムを みる', 'やすい キログラム']`

- shared-tail signal (template-generation):
  - tail `グラム`: `['あたらしい キログラム', 'たかい キログラム', 'やすい キログラム']`

### キロメートル (`n5.vocab.37-common-nouns-miscella.キロメートル`)
current particle_examples: `['キロメートルを かう', 'キロメートルを つかう', 'あたらしい キロメートル', 'たかい キロメートル', 'キロメートルを ください', 'キロメートルは どこ', 'キロメートルを みる', 'やすい キロメートル']`

- shared-tail signal (template-generation):
  - tail `ートル`: `['あたらしい キロメートル', 'たかい キロメートル', 'やすい キロメートル']`

### こえ (`n5.vocab.38-sounds-and-voice.こえ`)
current particle_examples: `['こえが ある', 'こえが ない', 'こえを いう', 'こえを きく', 'いい こえ', 'こえの とき', 'こえを おもう', 'こえを しる']`

- template-shape hits:
  - shape `を しる` in `こえを しる`

### おと (`n5.vocab.38-sounds-and-voice.おと`)
current particle_examples: `['おとが ある', 'おとが ない', 'おとを いう', 'おとを きく', 'いい おと', 'おとの とき', 'おとを おもう', 'おとを しる']`

- template-shape hits:
  - shape `を しる` in `おとを しる`

### ばしょ (`n5.vocab.40-misc-useful-items.ばしょ`)
current particle_examples: `['ばしょに いく', 'ばしょで あう', 'ばしょから くる', 'ばしょの まえに', 'ばしょが ある', 'ばしょは ちかい', 'ばしょまで あるく', 'ばしょに つく']`

- template-shape hits:
  - shape `に いく` in `ばしょに いく`

### ばあい (`n5.vocab.40-misc-useful-items.ばあい`)
current particle_examples: `['ばあいを かう', 'ばあいを つかう', 'あたらしい ばあい', 'たかい ばあい', 'ばあいを ください', 'ばあいは どこ', 'ばあいを みる', 'やすい ばあい']`

- shared-tail signal (template-generation):
  - tail `ばあい`: `['あたらしい ばあい', 'たかい ばあい', 'やすい ばあい']`

### ほう (`n5.vocab.40-misc-useful-items.ほう`)
current particle_examples: `['ねたほうが', '行ったほうが', 'わたしのほうが', 'ねないほうが', 'きょうのほうが', 'ーヒーのほうが', '食べないほうが', '飲まないほうが']`

- shared-tail signal (template-generation):
  - tail `ほうが`: `['ねたほうが', '行ったほうが', 'わたしのほうが', 'ねないほうが', 'きょうのほうが', 'ーヒーのほうが', '食べないほうが', '飲まないほうが']`

### じゅうしょ (`n5.vocab.40-misc-useful-items.じゅうしょ`)
current particle_examples: `['じゅうしょを かう', 'じゅうしょを つかう', 'あたらしい じゅうしょ', 'たかい じゅうしょ', 'じゅうしょを ください', 'じゅうしょは どこ', 'じゅうしょを みる', 'やすい じゅうしょ']`

- shared-tail signal (template-generation):
  - tail `うしょ`: `['あたらしい じゅうしょ', 'たかい じゅうしょ', 'やすい じゅうしょ']`

### ねんれい (`n5.vocab.40-misc-useful-items.ねんれい`)
current particle_examples: `['ねんれいを かう', 'ねんれいを つかう', 'あたらしい ねんれい', 'たかい ねんれい', 'ねんれいを ください', 'ねんれいは どこ', 'ねんれいを みる', 'やすい ねんれい']`

- shared-tail signal (template-generation):
  - tail `んれい`: `['あたらしい ねんれい', 'たかい ねんれい', 'やすい ねんれい']`

### しゅっしん (`n5.vocab.40-misc-useful-items.しゅっしん`)
current particle_examples: `['しゅっしんに いく', 'しゅっしんで あう', 'しゅっしんから くる', 'しゅっしんの まえに', 'しゅっしんが ある', 'しゅっしんは ちかい', 'しゅっしんまで あるく', 'しゅっしんに つく']`

- template-shape hits:
  - shape `に いく` in `しゅっしんに いく`

### いっぱい (`n5.vocab.33-adverbs.いっぱい`)
current particle_examples: `['たくさん いっぱい', 'お金が いっぱい', 'いっぱい たべる', 'いっぱい のむ', 'おなか いっぱい', 'ひとが いっぱい']`

- shared-tail signal (template-generation):
  - tail `っぱい`: `['たくさん いっぱい', 'お金が いっぱい', 'おなか いっぱい', 'ひとが いっぱい']`

### おくれる (`n5.vocab.28-verbs-group-2-verbs.おくれる`)
current particle_examples: `['おくれる', 'おくれるます', 'おくれるました', 'よく おくれる', 'まいにち おくれる', 'いま おくれる']`

- shared-tail signal (template-generation):
  - tail `くれる`: `['おくれる', 'よく おくれる', 'まいにち おくれる', 'いま おくれる']`

### おしらせ (`n5.vocab.24-school-and-study.おしらせ`)
current particle_examples: `['おしらせを かう', 'おしらせを つかう', 'あたらしい おしらせ', 'たかい おしらせ', 'おしらせを ください', 'おしらせは どこ', 'おしらせを みる', 'やすい おしらせ']`

- shared-tail signal (template-generation):
  - tail `しらせ`: `['あたらしい おしらせ', 'たかい おしらせ', 'やすい おしらせ']`

### おてら (`n5.vocab.13-locations-and-places-.おてら`)
current particle_examples: `['おてらに いく', 'おてらで あう', 'おてらから くる', 'おてらの まえに', 'おてらが ある', 'おてらは ちかい', 'おてらまで あるく', 'おてらに つく']`

- template-shape hits:
  - shape `に いく` in `おてらに いく`

### さくら (`n5.vocab.14-nature-and-weather.さくら`)
current particle_examples: `['さくらを かう', 'さくらを つかう', 'あたらしい さくら', 'たかい さくら', 'さくらを ください', 'さくらは どこ', 'さくらを みる', 'やすい さくら']`

- shared-tail signal (template-generation):
  - tail `さくら`: `['あたらしい さくら', 'たかい さくら', 'やすい さくら']`

### じゅんび (`n5.vocab.24-school-and-study.じゅんび`)
current particle_examples: `['じゅんびを かう', 'じゅんびを つかう', 'あたらしい じゅんび', 'たかい じゅんび', 'じゅんびを ください', 'じゅんびは どこ', 'じゅんびを みる', 'やすい じゅんび']`

- shared-tail signal (template-generation):
  - tail `ゅんび`: `['あたらしい じゅんび', 'たかい じゅんび', 'やすい じゅんび']`

### たんご (`n5.vocab.24-school-and-study.たんご`)
current particle_examples: `['たんごを かう', 'たんごを つかう', 'あたらしい たんご', 'たかい たんご', 'たんごを ください', 'たんごは どこ', 'たんごを みる', 'やすい たんご']`

- shared-tail signal (template-generation):
  - tail `たんご`: `['あたらしい たんご', 'たかい たんご', 'やすい たんご']`

### はらう (`n5.vocab.27-verbs-group-1-verbs.はらう`)
current particle_examples: `['はらう', 'はらうます', 'はらうました', 'よく はらう', 'まいにち はらう', 'いま はらう']`

- shared-tail signal (template-generation):
  - tail `はらう`: `['はらう', 'よく はらう', 'まいにち はらう', 'いま はらう']`

### アルバイト (`n5.vocab.22-money-and-shopping.アルバイト`)
current particle_examples: `['アルバイトを する', 'アルバイトの じかん', 'アルバイトの きゅうりょう', 'アルバイトを さがす', 'アルバイトの しごと', 'アルバイトに 行く']`

- template-shape hits:
  - shape `を する` in `アルバイトを する`

### コンサート (`n5.vocab.40-misc-useful-items.コンサート`)
current particle_examples: `['コンサートに いく', 'コンサートを みる', 'コンサートの チケット', 'コンサートが ある', 'コンサートの じかん', 'いい コンサート']`

- template-shape hits:
  - shape `に いく` in `コンサートに いく`

### コンビニ (`n5.vocab.13-locations-and-places-.コンビニ`)
current particle_examples: `['コンビニに いく', 'コンビニで かう', 'コンビニの ちかく', 'コンビニで はらう', 'コンビニの コーヒー', '24じかんの コンビニ']`

- template-shape hits:
  - shape `に いく` in `コンビニに いく`

### スペイン人 (`n5.vocab.25-languages-and-countri.スペイン人`)
reading: `スペインじん`  
current particle_examples: `['スペイン人と あう', 'スペイン人と はなす', 'スペイン人に きく', 'スペイン人は どこ', 'スペイン人の なまえ', 'スペイン人が くる', 'スペイン人が いる', 'スペイン人は やさしい']`

- template-shape hits:
  - shape `と あう` in `スペイン人と あう`

### セール (`n5.vocab.22-money-and-shopping.セール`)
current particle_examples: `['セールに いく', '大きな セール', 'セールの ふく', 'セールが ある', 'セールで かう', 'セールの じかん']`

- template-shape hits:
  - shape `に いく` in `セールに いく`

### ベンチ (`n5.vocab.26-house-and-furniture.ベンチ`)
current particle_examples: `['ベンチに すわる', 'こうえんの ベンチ', '大きな ベンチ', '木の ベンチ', 'ベンチで まつ', 'ベンチが あいている']`

- shared-tail signal (template-generation):
  - tail `ベンチ`: `['こうえんの ベンチ', '大きな ベンチ', '木の ベンチ']`

### ばい (`n5.vocab.9-counters-common.倍`)
current particle_examples: `['ひとつ', 'ふたつ', 'みっつ', 'いくつ', 'なんこ', 'ぜんぶで ばい', 'たくさんの ばい', 'ひとり ばい']`

- shared-tail signal (template-generation):
  - tail ` ばい`: `['ぜんぶで ばい', 'たくさんの ばい', 'ひとり ばい']`

### 出口 (`n5.vocab.13-locations-and-places-.出口`)
reading: `でぐち`  
current particle_examples: `['出口を 出る', 'みなみの 出口', 'きたの 出口', '出口の まえ', '出口を さがす', 'えきの 出口']`

- shared-tail signal (template-generation):
  - tail ` 出口`: `['みなみの 出口', 'きたの 出口', 'えきの 出口']`

### こくせき (`n5.vocab.25-languages-and-countri.国籍`)
current particle_examples: `['こくせきを かう', 'こくせきを つかう', 'あたらしい こくせき', 'たかい こくせき', 'こくせきを ください', 'こくせきは どこ', 'こくせきを みる', 'やすい こくせき']`

- shared-tail signal (template-generation):
  - tail `くせき`: `['あたらしい こくせき', 'たかい こくせき', 'やすい こくせき']`

### 後 (`n5.vocab.10-time-general.後`)
reading: `あと`  
current particle_examples: `['後に いく', '後で あう', '後から くる', '後の まえに', '後が ある', '後は ちかい', '後まで あるく', '後に つく']`

- template-shape hits:
  - shape `に いく` in `後に いく`

### 聞こえる (`n5.vocab.28-verbs-group-2-verbs.聞こえる`)
reading: `きこえる`  
current particle_examples: `['聞こえる', '聞こえるます', '聞こえるました', 'よく 聞こえる', 'まいにち 聞こえる', 'いま 聞こえる']`

- shared-tail signal (template-generation):
  - tail `こえる`: `['聞こえる', 'よく 聞こえる', 'まいにち 聞こえる', 'いま 聞こえる']`

### いえ (`n5.vocab.26-house-and-furniture.いえ`)
current particle_examples: `['いえに いく', 'いえで あう', 'いえから くる', 'いえの まえに', 'いえが ある', 'いえは ちかい', 'いえまで あるく', 'いえに つく']`

- template-shape hits:
  - shape `に いく` in `いえに いく`

### ぐらい (`n5.vocab.35-particles-functional-.ぐらい`)
current particle_examples: `['ぐらい / くらい がくせいです', 'ぐらい / くらい すきです', 'ぐらい / くらい ありません', 'これぐらい / くらい', 'なんぐらい / くらい', 'いつぐらい / くらい']`

- shared-tail signal (template-generation):
  - tail `くらい`: `['これぐらい / くらい', 'なんぐらい / くらい', 'いつぐらい / くらい']`

### けれど (`n5.vocab.34-conjunctions.けれど`)
current particle_examples: `['AはBです。けれど / けれども / けど、CはDです。', 'おいしい。けれど / けれども / けど、 たかい。', 'たべました。けれど / けれども / けど、 ねます。', 'けれど / けれども / けど、 いきましょう。', 'けれど / けれども / けど、 おわります。', 'いきます。けれど / けれども / けど、 かえります。']`

- shared-tail signal (template-generation):
  - tail `ます。`: `['たべました。けれど / けれども / けど、 ねます。', 'けれど / けれども / けど、 おわります。', 'いきます。けれど / けれども / けど、 かえります。']`

### ござる (`n5.vocab.30-verbs-existence-and-p.ござる`)
current particle_examples: `['ござる', 'ござるます', 'ござるました', 'よく ござる', 'まいにち ござる', 'いま ござる']`

- shared-tail signal (template-generation):
  - tail `ござる`: `['ござる', 'よく ござる', 'まいにち ござる', 'いま ござる']`

### どきどき (`n5.vocab.33-adverbs.どきどき`)
current particle_examples: `['どきどき する', 'むねが どきどき', 'しんぞうが どきどき', 'どきどきの しゅんかん', 'まだ どきどき', 'どきどき とまらない']`

- shared-tail signal (template-generation):
  - tail `きどき`: `['むねが どきどき', 'しんぞうが どきどき', 'まだ どきどき']`

### ビル (`n5.vocab.13-locations-and-places-.ビル`)
current particle_examples: `['たかい ビル', 'おおきい ビル', 'ビルの 中', 'ビルの 上', '会社の ビル', 'あたらしい ビル']`

- shared-tail signal (template-generation):
  - tail ` ビル`: `['たかい ビル', 'おおきい ビル', '会社の ビル', 'あたらしい ビル']`

---

## OPEN-005 — gloss audit (205 entries)

Heuristic: glosses that are very short (< 4 chars), very long (> 90 chars), multi-sense without disambiguation in `pragmatic_functions`, or sentence-shaped (containing 'is/am/are' — usually a sign that the gloss is a usage example, not a definition).

### Flag: `multi-sense-no-disambig` (136 entries)

- **おなか** (`n5.vocab.4-body-parts.おなか`): 'stomach, belly'
- **こちら** (`n5.vocab.5-demonstratives.こちら`): 'this way / this person (polite)'
- **いくつ** (`n5.vocab.6-question-words.いくつ`): 'how many, how old'
- **だい** (`n5.vocab.9-counters-common.だい`): 'counter for machines / vehicles'
- **かい** (`n5.vocab.9-counters-common.かい`): 'floor of a building (e.g., 3-かい = 3rd floor)'
- **かい** (`n5.vocab.9-counters-common.かい.2`): 'number of times / occurrences (e.g., 3-かい = three times). Same kana, different counter (different kanji); context disambiguates.'
- **番** (`n5.vocab.9-counters-common.番`): 'number, ordinal'
- **ど** (`n5.vocab.9-counters-common.ど`): 'degrees, occurrences'
- **とき** (`n5.vocab.10-time-general.とき`): 'time, when'
- **時間** (`n5.vocab.10-time-general.時間`): 'time, hour'
- **とけい** (`n5.vocab.10-time-general.とけい`): 'clock, watch'
- **ひる** (`n5.vocab.10-time-general.ひる`): 'noon, daytime'
- **ばん** (`n5.vocab.10-time-general.ばん`): 'evening, night'
- **二日** (`n5.vocab.11-time-days-weeks-month.二日`): '2nd / two days'
- **三日** (`n5.vocab.11-time-days-weeks-month.三日`): '3rd / three days'
- **四日** (`n5.vocab.11-time-days-weeks-month.四日`): '4th / four days'
- **六日** (`n5.vocab.11-time-days-weeks-month.六日`): '6th / six days'
- **七日** (`n5.vocab.11-time-days-weeks-month.七日`): '7th / seven days'
- **八日** (`n5.vocab.11-time-days-weeks-month.八日`): '8th / eight days'
- **九日** (`n5.vocab.11-time-days-weeks-month.九日`): '9th / nine days'
- **十日** (`n5.vocab.11-time-days-weeks-month.十日`): '10th / ten days'
- **二十日** (`n5.vocab.11-time-days-weeks-month.二十日`): '20th / twenty days'
- **月** (`n5.vocab.11-time-days-weeks-month.月`): 'month, moon'
- **すぐ** (`n5.vocab.12-time-frequency-sequen.すぐ`): 'soon, immediately'
- **もうすぐ** (`n5.vocab.12-time-frequency-sequen.もうすぐ`): 'soon, before long'
- **さいしょ** (`n5.vocab.12-time-frequency-sequen.さいしょ`): 'first, beginning'
- **さいご** (`n5.vocab.12-time-frequency-sequen.さいご`): 'last, end'
- **前** (`n5.vocab.12-time-frequency-sequen.前`): 'before, in front'
- **いりぐち** (`n5.vocab.13-locations-and-places-.いりぐち`): 'entrance, entry'
- **しょくどう** (`n5.vocab.13-locations-and-places-.しょくどう`): 'cafeteria, dining room'
  - …and 106 more (see raw data)

### Flag: `sentence-shaped` (6 entries)

- **毎年** (`n5.vocab.11-time-days-weeks-month.毎年`): 'every year (まいとし is more common in conversation; まいねん in formal/written contexts)'
- **ひく** (`n5.vocab.27-verbs-group-1-verbs.ひく.2`): 'to pull (homophone of the above; separate verb, separate kanji - both are common N5 readings of ひく)'
- **いる** (`n5.vocab.30-verbs-existence-and-p.いる.2`): 'to need (Group 1 exception - looks like Group 2; homophone of existence-いる which is Group 2)'
- **おげんきですか** (`n5.vocab.36-greetings-and-set-phr.おげんきですか`): 'how are you?'
- **そうですか** (`n5.vocab.39-function-filler-expre.そうですか`): 'is that so?'
- **ござる** (`n5.vocab.30-verbs-existence-and-p.ござる`): 'to be / there is (very polite; ございます is the ます-form, used in shop/hotel speech)'

### Flag: `very-long` (16 entries)

- **あなた** (`n5.vocab.1-people-pronouns-and-se.あなた`): "you (use with caution — Japanese typically uses the person's name + さん or drops the subject entirely)"
- **かれ** (`n5.vocab.1-people-pronouns-and-se.かれ`): 'boyfriend (primary in modern conversational Japanese); he, him (third-person pronoun, more formal/literary)'
- **かのじょ** (`n5.vocab.1-people-pronouns-and-se.かのじょ`): 'girlfriend (primary in modern conversational Japanese); she, her (third-person pronoun, more formal/literary)'
- **かい** (`n5.vocab.9-counters-common.かい.2`): 'number of times / occurrences (e.g., 3-かい = three times). Same kana, different counter (different kanji); context disambiguates.'
- **一日** (`n5.vocab.11-time-days-weeks-month.一日.2`): 'one day, a whole day (note: same kanji 一日 with a different reading, distinct from ついたち; context disambiguates)'
- **とる** (`n5.vocab.27-verbs-group-1-verbs.とる.2`): 'to take (a photo or video) - homophone of the above; uses a different kanji (not in N5 syllabus); semantically a specialization of "take"'
- **ひく** (`n5.vocab.27-verbs-group-1-verbs.ひく.2`): 'to pull (homophone of the above; separate verb, separate kanji - both are common N5 readings of ひく)'
- **いる** (`n5.vocab.30-verbs-existence-and-p.いる.2`): 'to need (Group 1 exception - looks like Group 2; homophone of existence-いる which is Group 2)'
- **あつい** (`n5.vocab.31-adjectives.あつい.2`): 'hot (to the touch; separate adjective and separate kanji - homophone of the hot-weather one)'
- **あつい** (`n5.vocab.31-adjectives.あつい.3`): 'thick (e.g., a thick book; separate adjective and separate kanji - third homophone of the あつい readings above)'
- **はやい** (`n5.vocab.31-adjectives.はやい`): 'early (time-related) - and separately, はやい - fast (speed-related). Two separate adjectives sharing the kana reading; the kanji disambiguates.'
- **やさしい** (`n5.vocab.31-adjectives.やさしい`): 'easy (of a task) - and separately, やさしい - kind / gentle (of a person). Two separate adjectives sharing the kana reading; different kanji distinguish them.'
- **ぐらい** (`n5.vocab.35-particles-functional-.ぐらい`): 'about, approximately (ぐらい more common after voiced sounds; くらい elsewhere - particle of estimate)'
- **じゃあ** (`n5.vocab.39-function-filler-expre.じゃあ`): 'well then / so (じゃあ casual; では formal; じゃ very casual - discourse marker for transitioning)'
- **みんな** (`n5.vocab.1-people-pronouns-and-se.みんな`): 'everyone / all (みんな more colloquial; みな more formal - both function as inclusive "everyone")'
- **やはり** (`n5.vocab.33-adverbs.やはり`): 'as expected / after all (やはり more formal; やっぱり colloquial - confirms an expectation or returns to a prior view)'

### Flag: `very-short` (51 entries)

- **私たち** (`n5.vocab.1-people-pronouns-and-se.私たち`): 'we'
- **だれ** (`n5.vocab.1-people-pronouns-and-se.だれ`): 'who'
- **男の子** (`n5.vocab.2-people-family.男の子`): 'boy'
- **男** (`n5.vocab.2-people-family.男`): 'man'
- **目** (`n5.vocab.4-body-parts.め`): 'eye'
- **みみ** (`n5.vocab.4-body-parts.みみ`): 'ear'
- **どう** (`n5.vocab.5-demonstratives.どう`): 'how'
- **なぜ** (`n5.vocab.6-question-words.なぜ`): 'why'
- **どうして** (`n5.vocab.6-question-words.どうして`): 'why'
- **一** (`n5.vocab.7-numbers.一`): 'one'
- **二** (`n5.vocab.7-numbers.二`): 'two'
- **六** (`n5.vocab.7-numbers.六`): 'six'
- **十** (`n5.vocab.7-numbers.十`): 'ten'
- **二つ** (`n5.vocab.8-native-counters-series.二つ`): 'two'
- **六つ** (`n5.vocab.8-native-counters-series.六つ`): 'six'
- **十** (`n5.vocab.8-native-counters-series.十`): 'ten'
- **今** (`n5.vocab.10-time-general.今`): 'now'
- **日** (`n5.vocab.11-time-days-weeks-month.日`): 'day'
- **五月** (`n5.vocab.11-time-days-weeks-month.五月`): 'May'
- **どうぶつえん** (`n5.vocab.13-locations-and-places-.どうぶつえん`): 'zoo'
- **とおく** (`n5.vocab.13-locations-and-places-.とおく`): 'far'
- **空** (`n5.vocab.14-nature-and-weather.空`): 'sky'
- **たいよう** (`n5.vocab.14-nature-and-weather.たいよう`): 'sun'
- **いぬ** (`n5.vocab.15-animals.いぬ`): 'dog'
- **ねこ** (`n5.vocab.15-animals.ねこ`): 'cat'
- **うし** (`n5.vocab.15-animals.うし`): 'cow'
- **ぶた** (`n5.vocab.15-animals.ぶた`): 'pig'
- **たまご** (`n5.vocab.17-food-items.たまご`): 'egg'
- **かばん** (`n5.vocab.21-clothing-and-accessor.かばん`): 'bag'
- **円** (`n5.vocab.22-money-and-shopping.円`): 'yen'
  - …and 21 more (see raw data)

---

## OPEN-013 — example sentences audit (81 entries)

Heuristic: example sentences that are longer than 35 characters, contain kanji not in the N5 whitelist, or have a run of 4+ consecutive kanji (likely off-N5 vocabulary block).

### おじいさん (`n5.vocab.2-people-family.おじいさん`)
- example[2]: `おじいさんは 元気です。` → flags: ['off-N5-kanji(元)']

### 学生 (`n5.vocab.3-people-roles.学生`)
- example[2]: `兄は 大学の 学生です。` → flags: ['off-N5-kanji(兄)']

### かお (`n5.vocab.4-body-parts.かお`)
- example[0]: `朝、かおを あらいます。` → flags: ['off-N5-kanji(朝)']

### あんな (`n5.vocab.5-demonstratives.あんな`)
- example[0]: `あんな 大きい 家に すみたいです。` → flags: ['off-N5-kanji(家)']

### いつ (`n5.vocab.6-question-words.いつ`)
- example[2]: `いつ 帰りますか。` → flags: ['off-N5-kanji(帰)']

### まい (`n5.vocab.9-counters-common.まい`)
- example[2]: `紙を 五まい ください。` → flags: ['off-N5-kanji(紙)']

### こんや (`n5.vocab.10-time-general.こんや`)
- example[0]: `こんや 家に います。` → flags: ['off-N5-kanji(家)']

### 日曜日 (`n5.vocab.11-time-days-weeks-month.日曜日`)
- example[0]: `日曜日に 家ぞくと あいます。` → flags: ['off-N5-kanji(家)']

### 毎月 (`n5.vocab.11-time-days-weeks-month.毎月`)
- example[0]: `毎月 一回 あいます。` → flags: ['off-N5-kanji(回)']

### いつも (`n5.vocab.12-time-frequency-sequen.いつも`)
- example[2]: `いつも 朝 七時に おきます。` → flags: ['off-N5-kanji(朝)']

### ちかく (`n5.vocab.13-locations-and-places-.ちかく`)
- example[0]: `家の ちかくに スーパーが あります。` → flags: ['off-N5-kanji(家)']

### くさ (`n5.vocab.14-nature-and-weather.くさ`)
- example[2]: `にわの くさを 切りました。` → flags: ['off-N5-kanji(切)']

### 空 (`n5.vocab.14-nature-and-weather.空`)
- example[1]: `今日は 空が とても 青いです。` → flags: ['off-N5-kanji(青)']

### にわとり (`n5.vocab.15-animals.にわとり`)
- example[2]: `にわとりが 朝 はやく なきます。` → flags: ['off-N5-kanji(朝)']

### やさい (`n5.vocab.17-food-items.やさい`)
- example[1]: `やさいは 体に いいです。` → flags: ['off-N5-kanji(体)']

### たまねぎ (`n5.vocab.17-food-items.たまねぎ`)
- example[0]: `たまねぎを 切ります。` → flags: ['off-N5-kanji(切)']
- example[2]: `たまねぎを 半分 切りました。` → flags: ['off-N5-kanji(切)']

### じゃがいも (`n5.vocab.17-food-items.じゃがいも`)
- example[1]: `じゃがいもを 切って カレーに 入れます。` → flags: ['off-N5-kanji(切)']

### キャベツ (`n5.vocab.17-food-items.キャベツ`)
- example[0]: `キャベツを 切ります。` → flags: ['off-N5-kanji(切)']
- example[2]: `キャベツを 半分 切りました。` → flags: ['off-N5-kanji(切)']

### おちゃ (`n5.vocab.18-drinks.おちゃ`)
- example[2]: `朝は おちゃを 飲みます。` → flags: ['off-N5-kanji(朝)']

### こうちゃ (`n5.vocab.18-drinks.こうちゃ`)
- example[2]: `朝は こうちゃを 飲みます。` → flags: ['off-N5-kanji(朝)']

### コーヒー (`n5.vocab.18-drinks.コーヒー`)
- example[2]: `朝 コーヒーを 一ぱい 飲みます。` → flags: ['off-N5-kanji(朝)']

### ナイフ (`n5.vocab.19-tableware-and-cooking.ナイフ`)
- example[0]: `ナイフで パンを 切ります。` → flags: ['off-N5-kanji(切)']

### ちゃいろ (`n5.vocab.20-colors.ちゃいろ`)
- example[2]: `ちゃいろの くつが 好きです。` → flags: ['off-N5-kanji(好)']

### きもの (`n5.vocab.21-clothing-and-accessor.きもの`)
- example[0]: `お正月に きものを きます。` → flags: ['off-N5-kanji(正)']

### ズボン (`n5.vocab.21-clothing-and-accessor.ズボン`)
- example[2]: `青い ズボンを きました。` → flags: ['off-N5-kanji(青)']

### さいふ (`n5.vocab.21-clothing-and-accessor.さいふ`)
- example[2]: `さいふを 家に わすれました。` → flags: ['off-N5-kanji(家)']

### ドル (`n5.vocab.22-money-and-shopping.ドル`)
- example[1]: `一ドルは 百四十円ぐらいです。` → flags: ['kanji-run(百四十円)']

### バイク (`n5.vocab.23-transport.バイク`)
- example[2]: `兄は バイクで かよって います。` → flags: ['off-N5-kanji(兄)']

### れんしゅう (`n5.vocab.24-school-and-study.れんしゅう`)
- example[0]: `れんしゅうが 大切です。` → flags: ['off-N5-kanji(切)']

### 新聞 (`n5.vocab.24-school-and-study.新聞`)
- example[1]: `毎朝 新聞を 読みます。` → flags: ['off-N5-kanji(朝)']
- example[2]: `父は 毎朝 新聞を 読みます。` → flags: ['off-N5-kanji(朝)']

### ボールペン (`n5.vocab.24-school-and-study.ボールペン`)
- example[2]: `青い ボールペンで しけんを 書きます。` → flags: ['off-N5-kanji(青)']

### ペン (`n5.vocab.24-school-and-study.ペン`)
- example[2]: `青い ペンを かして ください。` → flags: ['off-N5-kanji(青)']

### こくばん (`n5.vocab.24-school-and-study.こくばん`)
- example[0]: `先生は こくばんに 字を 書きます。` → flags: ['off-N5-kanji(字)']
- example[2]: `先生が こくばんに 字を 書きました。` → flags: ['off-N5-kanji(字)']

### しゃしん (`n5.vocab.24-school-and-study.しゃしん`)
- example[0]: `家ぞくの しゃしんを 見せます。` → flags: ['off-N5-kanji(家)']

### 番号 (`n5.vocab.24-school-and-study.番号`)
- example[2]: `電話番号を 教えて ください。` → flags: ['off-N5-kanji(教)', 'kanji-run(電話番号)']

### 電話番号 (`n5.vocab.24-school-and-study.電話番号`)
- example[0]: `電話番号を 教えて ください。` → flags: ['off-N5-kanji(教)', 'kanji-run(電話番号)']
- example[1]: `電話番号が かわりました。` → flags: ['kanji-run(電話番号)']
- example[2]: `電話番号を おしえて ください。` → flags: ['kanji-run(電話番号)']

### 日本人 (`n5.vocab.25-languages-and-countri.日本人`)
- example[2]: `兄の 友だちは 日本人です。` → flags: ['off-N5-kanji(兄)']

### アメリカ (`n5.vocab.25-languages-and-countri.アメリカ`)
- example[2]: `兄は アメリカに すんで います。` → flags: ['off-N5-kanji(兄)']

### 中国 (`n5.vocab.25-languages-and-countri.中国`)
- example[2]: `中国は 人が とても 多いです。` → flags: ['off-N5-kanji(多)']

### かんこくご (`n5.vocab.25-languages-and-countri.かんこくご`)
- example[2]: `かんこくごを 少し はなせます。` → flags: ['off-N5-kanji(少)']

### フランスご (`n5.vocab.25-languages-and-countri.フランスご`)
- example[2]: `フランスごを 少し はなせます。` → flags: ['off-N5-kanji(少)']

### テープ (`n5.vocab.26-house-and-furniture.テープ`)
- example[3]: `テープを はさみで 切ります。` → flags: ['off-N5-kanji(切)']

### ギター (`n5.vocab.26-house-and-furniture.ギター`)
- example[2]: `兄は ギターを ひきます。` → flags: ['off-N5-kanji(兄)']

### 書く (`n5.vocab.27-verbs-group-1-verbs.書く`)
- example[0]: `手紙を 書きます。` → flags: ['off-N5-kanji(紙)']

### すむ (`n5.vocab.27-verbs-group-1-verbs.すむ`)
- example[0]: `東京に すんで います。` → flags: ['off-N5-kanji(京)']
- example[2]: `兄は とうきょうに すんで います。` → flags: ['off-N5-kanji(兄)']

### はしる (`n5.vocab.27-verbs-group-1-verbs.はしる`)
- example[1]: `毎朝 こうえんで はしります。` → flags: ['off-N5-kanji(朝)']

### かえる (`n5.vocab.27-verbs-group-1-verbs.かえる`)
- example[0]: `家に かえります。` → flags: ['off-N5-kanji(家)']

### ひく (`n5.vocab.27-verbs-group-1-verbs.ひく.2`)
- example[1]: `妹は 毎日 ピアノを ひきます。` → flags: ['off-N5-kanji(妹)']

### よぶ (`n5.vocab.27-verbs-group-1-verbs.よぶ`)
- example[0]: `友だちを 家に よびました。` → flags: ['off-N5-kanji(家)']

### のぼる (`n5.vocab.27-verbs-group-1-verbs.のぼる`)
- example[1]: `ふじ山に のぼる 人が 多いです。` → flags: ['off-N5-kanji(多)']

_…and 31 more entries with flagged examples (see raw data)._

---

## Summary

- OPEN-003 / OPEN-004 particle-examples candidates: **589 entries**
- OPEN-005 gloss-audit candidates: **205 entries**
- OPEN-013 example-sentence candidates: **81 entries**

All numbers are heuristic flags, not confirmed bugs. The human native reviewer should walk each list and decide per entry.
