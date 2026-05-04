# JLPT N5 Moji (文字) Practice Questions

100 questions covering the Moji section of the JLPT N5. The Moji section tests recognition of kanji and their readings, and the ability to write a hiragana word with the correct kanji form. Format follows the official jlpt.jp test paper structure.

## Subtypes covered

| Mondai | Subtype | Count |
|---|---|---|
| Mondai 1 | 漢字読み (kanji reading) - pick the correct hiragana reading for the underlined kanji | 50 |
| Mondai 2 | 表記 (orthography) - pick the correct kanji form for the underlined hiragana word | 50 |

## Notation rules

- Kanji words being tested are surrounded by `<u>...</u>` (HTML underline). This renders as actual underline in browsers and faithful markdown renderers, matching the underline used on the real JLPT paper.
- Hiragana words being tested in Mondai 2 are surrounded by `__...__` (markdown underscore-bold; for legacy compatibility the hiragana underline is shown this way).
- Each question has 4 numbered choices. `**Answer:**` shows the correct number.
- Rationale (optional) is given as a one-line note.
- No em dashes (U+2014) appear in this file.

## Engine display note

For mock-test mode, the app's test engine MUST hide the `**Answer:**` line and rationale until the student commits an answer. The visible-by-default format here is for self-study reference; runtime test rendering is the engine's responsibility.

## Kanji-scope exception for question files

The project's `vocabulary_n5.md` and `kanji_n5.md` rules state that *only N5-syllabus kanji* may appear in catalog content; non-N5 vocabulary is rendered in kana. **Question files (this file, plus `goi_questions_n5.md`, `bunpou_questions_n5.md`, `dokkai_questions_n5.md`) carry a deliberate exception**:

- All **stems** and all **correct answers** use only N5-syllabus kanji.
- **Distractor options** in 表記 (orthography) questions may contain non-N5 kanji because authentic JLPT distractors mimic visually-similar wrong forms - some of which are N4 or higher kanji that look like the N5 target. Forcing N5-only distractors would either require random hiragana (defeats the orthography test) or unrelated N5 kanji (no longer plausible distractors).
- This exception is scoped strictly to question files and does not relax the catalog rule applied to `vocabulary_n5.md` / `kanji_n5.md` / `grammar_n5.md`.

## Distractor verb-form convention (orthography questions)

In Mondai 2 (orthography) and Mondai 1 (kanji-reading), distractors fall into three acceptable types:

1. **Visually-similar N5 kanji** with a different reading (e.g., 多い / 古い / 長い for a 高い target). Most common distractor type at N5; tests whether the learner recognizes the right glyph among lookalikes drawn entirely from the N5 syllabus.

2. **Non-N5 kanji with the same on-yomi** as the target (e.g., a 立ちます distractor of `経ちます` - N3+ kanji, real verb meaning "elapse"). Tests glyph recognition; the non-N5 kanji is acceptable because the question is purely orthographic.

3. **Invented (non-real) verb forms** that combine an N5 kanji with a wrong conjugation pattern (e.g., a 入ります distractor of `出ります` - the real form is 出ます). Tests glyph recognition without requiring the distractor to be a grammatically valid conjugation.

All three types are acceptable because the question asks "which kanji visually belongs in this word", not "is this conjugation pattern grammatical".

---

## Mondai 1 - 漢字読み (Kanji Reading)

50 questions. For the underlined kanji compound, choose the correct hiragana reading.

### Q1

あの 人は <u>学生</u> です。

1. かくせ
2. かくせい
3. がくせ
4. がくせい

**Answer: 4** - 学 (ガク) + 生 (セイ).

### Q2

きのう <u>先生</u> に あいました。

1. せんせえ
2. せんぜい
3. せんせ
4. せんせい

**Answer: 4** - 先 (セン) + 生 (セイ).

### Q3

<u>学校</u> は いえから ちかいです。

1. かっこう
2. がっこ
3. かっこ
4. がっこう

**Answer: 4** - 学 (ガッ) + 校 (コウ), small っ.

### Q4

<u>大学</u> で にほんごを べんきょうします。

1. だいがく
2. だいかく
3. たいがく
4. たいかく

**Answer: 1** - 大 (ダイ) + 学 (ガク).

### Q5

ちちは <u>会社員</u> です。

1. かいしゃいん
2. がいしゃいん
3. かいしゃじん
4. かいさいん

**Answer: 1** - 会社 (かいしゃ) + 員 (イン).

### Q6

<u>日本</u> に すんで います。

1. にっほん
2. にぼん
3. ひほん
4. にほん

**Answer: 4** - 日本 = にほん. (The reading にっぽん also exists for formal/political contexts but is not in the answer choices.)

### Q7

<u>日本語</u> が すこし わかります。

1. にほんごう
2. にぼんご
3. にっぽんご
4. にほんご

**Answer: 4** - 日本 (にほん) + 語 (ゴ).

### Q8

<u>中国</u> へ いった ことが あります。

1. ちゅごく
2. ちゅうこく
3. ちゅうごく
4. ちゅごこく

**Answer: 3** - 中 (チュウ) + 国 (コク → ごく with rendaku).

### Q9

きょうは <u>月曜日</u> です。

1. げっつようび
2. げつようび
3. もくようび
4. かようび

**Answer: 2** - 月 (ゲツ) + 曜日 (ヨウビ).

### Q10

<u>水曜日</u> に プールへ いきます。

1. かようび
2. すいようび
3. もくようび
4. みずようび

**Answer: 2** - 水 (スイ) + 曜日 (ヨウビ).

### Q11

<u>金曜日</u> の よる、ともだちと あいます。

1. どようび
2. かようび
3. げつようび
4. きんようび

**Answer: 4** - 金 (キン) + 曜日.

### Q12

<u>土曜日</u> は やすみです。

1. つちようび
2. とようび
3. どようび
4. どっようび

**Answer: 3** - 土 (ド) + 曜日.

### Q13

<u>日曜日</u> に かぞくと こうえんへ いきました。

1. にっようび
2. げつようび
3. ひようび
4. にちようび

**Answer: 4** - 日 (ニチ) + 曜日.

### Q14

きょうは <u>十月</u> ついたちです。

1. しがつ
2. はちがつ
3. じゅうがつ
4. じゅういちがつ

**Answer: 3** - 十 (ジュウ) + 月 (ガツ).

### Q15

<u>九月</u> に がっこうが はじまります。

1. くつき
2. きゅうがつ
3. ここのがつ
4. くがつ

**Answer: 4** - 九 has reading ク in 九月; 月 reads ガツ for months.

### Q16

<u>七月</u> は あついです。

1. なながつ
2. なのがつ
3. しちがつ
4. ななつき

**Answer: 3** - 七 has reading シチ in 七月.

### Q17

<u>四月</u> から 大学に いきます。

1. しがつ
2. よがつ
3. よんがつ
4. よっがつ

**Answer: 1** - 四 has reading シ in 四月.

### Q18

<u>今日</u> は とても いい てんきです。

1. きょう
2. こんにち
3. こんじつ
4. きょうび

**Answer: 1** - 今日 is read きょう (irregular jukujikun).

### Q19

<u>今年</u>の ふゆは さむいです。

1. ことし
2. こんねん
3. いまとし
4. きんねん

**Answer: 1** - 今年 is read ことし (irregular jukujikun reading).

### Q20

<u>先月</u> たんじょうびでした。

1. せんがつ
2. ぜんげつ
3. せんげつ
4. ぜんがつ

**Answer: 3** - 先 (セン) + 月 (ゲツ).

### Q21

<u>来週</u> りょこうに いきます。

1. らいしゅ
2. こんしゅう
3. らいしゅう
4. せんしゅう

**Answer: 3** - 来 (ライ) + 週 (シュウ).

### Q22

<u>毎日</u> にほんごを べんきょうします。

1. まいにち
2. まいひ
3. まいじつ
4. まいか

**Answer: 1** - 毎 (マイ) + 日 (ニチ).

### Q23

<u>午前</u> くじに がっこうへ いきます。

1. くぜん
2. ごご
3. しょうご
4. ごぜん

**Answer: 4** - 午 (ゴ) + 前 (ゼン).

### Q24

<u>午後</u> さんじに あいましょう。

1. ごぜん
2. ごこ
3. ごご
4. ごう

**Answer: 3** - 午 (ゴ) + 後 (ゴ).

### Q25

ごじ<u>半</u> に いえに かえります。

1. ばん
2. はん
3. なか
4. ぱん

**Answer: 2** - 半 (ハン).

### Q26

きょうは <u>何曜日</u> ですか。

1. どようび
2. なにようび
3. かようび
4. なんようび

**Answer: 4** - 何 (なん) + 曜日.

### Q27

<u>何時</u> に きますか。

1. なじ
2. なんじ
3. いつじ
4. なにじ

**Answer: 2** - 何 (なん) + 時 (ジ).

### Q28

つくえの <u>上</u> に ほんが あります。

1. うる
2. うへ
3. うい
4. うえ

**Answer: 4** - 上 (うえ).

### Q29

ねこは いすの <u>下</u> に います。

1. しだ
2. した
3. しぢ
4. しと

**Answer: 2** - 下 (した).

### Q30

<u>右</u> に まがって ください。

1. みき
2. みぎ
3. みじ
4. みち

**Answer: 2** - 右 (みぎ).

### Q31

<u>左</u> がわに 大きい きが あります。

1. ひがり
2. ひだり
3. ひたり
4. ひだい

**Answer: 2** - 左 (ひだり).

### Q32

ぎんこうの <u>前</u> に コンビニが あります。

1. まい
2. まえ
3. まへ
4. もえ

**Answer: 2** - 前 (まえ).

### Q33

学校の <u>後ろ</u> に こうえんが あります。

1. あしろ
2. うしる
3. うしろ
4. うじろ

**Answer: 3** - 後ろ (うしろ) - kun-yomi reading.

### Q34

きょうは さむいので、<u>外</u> へ でません。

1. そど
2. そと
3. さと
4. のそと

**Answer: 2** - 外 (そと).

### Q35

私の いえは まちの <u>北</u> に あります。

1. ひがし
2. きた
3. みなみ
4. にし

**Answer: 2** - 北 (きた).

### Q36

<u>山</u> の うえに ゆきが あります。

1. やみ
2. やめ
3. やま
4. やも

**Answer: 3** - 山 (やま).

### Q37

<u>川</u> で さかなを みました。

1. かれ
2. かは
3. かわ
4. かや

**Answer: 3** - 川 (かわ).

### Q38

きょうは <u>天気</u> が いいです。

1. でんぎ
2. でんき
3. てんぎ
4. てんき

**Answer: 4** - 天 (テン) + 気 (キ).

### Q39

<u>雨</u> が ふって います。

1. うめ
2. あま
3. あみ
4. あめ

**Answer: 4** - 雨 (あめ) - kun-yomi for the standalone noun.

### Q40

<u>花</u> が きれいに さいて います。

1. ばな
2. はね
3. はま
4. はな

**Answer: 4** - 花 (はな).

### Q41

<u>電車</u> で 駅まで いきます。

1. でんさ
2. てんしゃ
3. でんしゃ
4. てんさ

**Answer: 3** - 電 (デン) + 車 (シャ).

### Q42

<u>電話</u> ばんごうを おしえて ください。

1. でんわ
2. てんわ
3. でんは
4. てんは

**Answer: 1** - 電 (デン) + 話 (ワ).

### Q43

<u>駅</u> の まえで まって います。

1. えき
2. えぎ
3. えく
4. やき

**Answer: 1** - 駅 (エキ).

### Q44

その <u>店</u> で パンを 買いました。

1. みせ
2. みぜ
3. みす
4. みえ

**Answer: 1** - 店 (みせ).

### Q45

<u>新しい</u> ノートを 買いました。

1. あたらしい
2. あらたしい
3. あだらしい
4. あたうしい

**Answer: 1** - 新 (あたら) + しい.

### Q46

この くつは <u>古い</u> です。

1. ふろい
2. ふるい
3. ぶるい
4. ふらい

**Answer: 2** - 古 (ふる) + い.

### Q47

この かばんは <u>高い</u> です。

1. たがい
2. たかい
3. たけい
4. だかい

**Answer: 2** - 高 (たか) + い.

### Q48

<u>安い</u> くつを 買いました。

1. あすい
2. やすい
3. やしい
4. やせい

**Answer: 2** - 安 (やす) + い.

### Q49

<u>白い</u> いぬが います。

1. しろい
2. しらい
3. じろい
4. しろう

**Answer: 1** - 白 (しろ) + い.

### Q50

この みちは <u>長い</u> です。

1. ながい
2. なかい
3. のがい
4. ねがい

**Answer: 1** - 長 (なが) + い.

---

## Mondai 2 - 表記 (Orthography)

50 questions. Choose the correct kanji form of the underlined hiragana word.

### Q51

あの __がくせい__ は とても しんせつです。

1. 学先
2. 字生
3. 学生
4. 字先

**Answer: 3** - 学 (study) + 生 (life / student).

### Q52

__せんせい__ に しつもんを しました。

1. 先成
2. 先正
3. 先生
4. 元生

**Answer: 3** - 先生 (teacher).

### Q53

__がっこう__ で にほんごを べんきょうします。

1. 字交
2. 字校
3. 学交
4. 学校

**Answer: 4** - 学校 (school).

### Q54

うちの 父は とても __ちから__ が つよいです。

1. 力
2. 刀
3. 万
4. 方

**Answer: 1** - 力 (ちから - strength, N5 kanji).

### Q55

この えいがは __おとな__ から 子どもまで みんな たのしめます。

1. 大人
2. 太人
3. 大入
4. 太入

**Answer: 1** - 大人 (おとな - adult). Jukujikun (semantic compound reading): the kanji 大 and 人 are individually N5, but the compound reading おとな is irregular. The compound is documented as an N5 vocab entry in vocabulary_n5.md; the irregular-reading pattern is standard for N5 family/age vocabulary.

### Q56

うちの __ちち__ は かいしゃいんです。

1. 母
2. 兄
3. 父
4. 友

**Answer: 3** - 父 (father).

### Q57

__はは__ は 学校の 先生です。

1. 父
2. 妹
3. 母
4. 友

**Answer: 3** - 母 (mother). Note: distractor 妹 is not in the kanji whitelist - it appears as a recognition-only distractor per the moji-corpus kanji-scope exception (Mondai 2 distractors may use non-whitelist kanji where authentic JLPT format requires it). Students do not need to read 妹 to reject it; family-relation kanji shape suffices.

### Q58

ごはんの まえに __て__ を あらいます。

1. 千
2. 毛
3. 牛
4. 手

**Answer: 4** - 手 (hand, N5).

### Q59

__ひと__ が おおぜい います。

1. 入
2. 人
3. 八
4. 大

**Answer: 2** - 人 (person).

### Q60

__おとこ__ の こが あそんで います。

1. 文
2. 田
3. 力
4. 男

**Answer: 4** - 男 (man / male).

### Q61

__おんな__ の 学生が きました。

1. 母
2. 安
3. 女
4. 好

**Answer: 3** - 女 (woman / female).

### Q62

うちには __こども__ が ふたり います。

1. 子ども
2. 字ども
3. 小ども
4. 子供

**Answer: 1** - 子ども is selected here because it follows this corpus's N5-only-kanji policy (供 is N4). Both 子供 and 子ども are standard in modern Japanese, and on the actual JLPT both forms appear; the choice between them is a corpus-internal scope rule, not a correctness rule.

### Q63

__にほん__ に すんで います。

1. 日本
2. 月本
3. 日木
4. 月木

**Answer: 1** - 日本 (Japan).

### Q64

__にほんご__ で 話します。

1. 日本後
2. 月本語
3. 日本語
4. 日本話

**Answer: 3** - 日本語 (Japanese language).

### Q65

__がいこく__ で しごとを して います。

1. 外国
2. 内国
3. 外校
4. 外区

**Answer: 1** - 外 + 国.

### Q66

きょうは __なんようび__ ですか。

1. 木曜日
2. 何曜日
3. 火曜日
4. 月曜日

**Answer: 2** - 何曜日.

### Q67

きょうは __かようび__ です。

1. 金曜日
2. 火曜日
3. 木曜日
4. 水曜日

**Answer: 2** - 火曜日.

### Q68

__もくようび__ に テストが あります。

1. 火曜日
2. 水曜日
3. 木曜日
4. 金曜日

**Answer: 3** - 木 (Thursday).

### Q69

__きょう__ は とても いい てんきです。

1. 今月
2. 今年
3. 今日
4. 来日

**Answer: 3** - 今日.

### Q70

__らいねん__ に だいがくに いきます。

1. 毎年
2. 今年
3. 先年
4. 来年

**Answer: 4** - 来年.

### Q71

__せんしゅう__ えいがを 見ました。

1. 毎週
2. 来週
3. 今週
4. 先週

**Answer: 4** - 先週.

### Q72

__まいにち__ にほんごを 話します。

1. 来日
2. 毎日
3. 今日
4. 先日

**Answer: 2** - 毎日.

### Q73

__ごぜん__ じゅうじに あいましょう。

1. 午前
2. 午後
3. 牛前
4. 午先

**Answer: 1** - 午前.

### Q74

__ごご__ に 友だちが きます。

1. 午前
2. 午後
3. 午午
4. 牛後

**Answer: 2** - 午後.

### Q75

__でんしゃ__ の なかで 本を 読みます。

1. 田車
2. 雨車
3. 電東
4. 電車

**Answer: 4** - 電車.

### Q76

__でんわ__ で 友だちと 話します。

1. 電語
2. 田話
3. 田語
4. 電話

**Answer: 4** - 電話.

### Q77

きのう __くるま__ を 買いました。

1. 中
2. 東
3. 来
4. 車

**Answer: 4** - 車.

### Q78

がっこうへ いく __みち__ で 友だちに あいました。

1. 道
2. 通
3. 路
4. 行

**Answer: 1** - 道 (みち - road, way). 道 is whitelisted N5 (kanji whitelist line 98) and listed at vocabulary_n5.md. The distractors 通 / 路 / 行 are family-of-meaning alternatives commonly seen in N4+ vocabulary (通る / 通り pass through, 道路 / 路上 road, 行く go). The semantic-distractor design tests whether the student knows 道 specifically rather than just recognizing the "road / way" semantic field.

### Q79

__えき__ で 友だちと あいました。

1. 駅
2. 馬
3. 駄
4. 訳

**Answer: 1** - 駅.

### Q80

__みせ__ は えきの まえに あります。

1. 占
2. 居
3. 庄
4. 店

**Answer: 4** - 店.

### Q81

ばんごはんを いまから __たべます__。

1. 飯べます
2. 飲べます
3. 食べます
4. 喫べます

**Answer: 3** - 食べます.

### Q82

パーティーで ジュースを __のみ__ました。

1. 食み
2. 飲み
3. 読み
4. 進み

**Answer: 2** - 飲む (のむ - to drink). 飲 is N5; the distractors share visual / phonetic similarity in a different context.

### Q83

ニュースを テレビで __みます__。

1. 視ます
2. 観ます
3. 見ます
4. 看ます

**Answer: 3** - N5 standard 見ます.

### Q84

おんがくを __ききます__。

1. 効きます
2. 聞きます
3. 利きます
4. 訊きます

**Answer: 2** - 聞きます.

### Q85

にほんごで __はなします__。

1. 離します
2. 放します
3. 話します
4. 講します

**Answer: 3** - 話します.

### Q86

まいばん 本を __よみます__。

1. 詠みます
2. 読みます
3. 訳みます
4. 諳みます

**Answer: 2** - 読みます.

### Q87

てがみを __かきます__。

1. 描きます
2. 書きます
3. 画きます
4. 掻きます

**Answer: 2** - 書きます.

### Q88

あした 友だちが いえに __きます__。

1. 来ます
2. 起ます
3. 着ます
4. 切ます

**Answer: 1** - 来ます (to come).

### Q89

まいあさ 八時に がっこうへ __いきます__。

1. 生きます
2. 行きます
3. 帰きます
4. 入きます

**Answer: 2** - 行きます.

### Q90

まいあさ 七時に いえを __でます__。

1. 出ます
2. 入ます
3. 立ます
4. 来ます

**Answer: 1** - 出ます.

### Q91

ねる まえに おふろに __はいります__。

1. 立ります
2. 出ります
3. 入ります
4. 切ります

**Answer: 3** - 入ります.

### Q92

先生が きょうしつに 来たので、学生が __たちます__。

1. 立ちます
2. 起ちます
3. 経ちます
4. 建ちます

**Answer: 1** - 立ちます (stand up - the everyday N5 sense of たつ). The other forms 起ちます / 経ちます / 建ちます are real Japanese verbs also read たちます (rise up / time passes / a building stands) but are N3+ in scope. Broader-exposure students should not be misled by the polysemy; for N5 the 立 form is the only correct match for "students stand up when the teacher enters".

### Q93

つかれたから すこし __やすみます__。

1. 体みます
2. 休みます
3. 安みます
4. 寄みます

**Answer: 2** - 休みます.

### Q94

先生が なまえを __いいます__。

1. 謂います
2. 云います
3. 言います
4. 議います

**Answer: 3** - N5 standard 言います.

### Q95

みせで やさいを __かいます__。

1. 飼います
2. 買います
3. 替います
4. 換います

**Answer: 2** - 買います.

### Q96

この とけいは とても __たかい__ です。

1. 多い
2. 長い
3. 古い
4. 高い

**Answer: 4** - 高い.

### Q97

この レストランは __やすい__ です。

1. 寄い
2. 易い
3. 休い
4. 安い

**Answer: 4** - 安い.

### Q98

この かわは とても __ながい__ です。

1. 永い
2. 長い
3. 強い
4. 高い

**Answer: 2** - 長い.

### Q99

__しろい__ ねこが います。

1. 白い
2. 百い
3. 自い
4. 旧い

**Answer: 1** - 白い.

### Q100

__なまえ__ を ここに かいて ください。

1. 名前
2. 名先
3. 友前
4. 名間

**Answer: 1** - 名前.

---

## End of file

100 questions complete: 50 漢字読み + 50 表記.

Next files in this series (per `TASKS.md` Phase 2.9):

- `goi_questions_n5.md` - 文脈規定 + 言い換え類義
- `bunpou_questions_n5.md` - 文法1 + 文法2 + 文章の文法
- `dokkai_questions_n5.md` - 短文 + 中文 + 情報検索
