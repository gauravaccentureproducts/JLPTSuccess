# JLPT N5 Goi (語彙) Practice Questions

100 questions covering the Goi (vocabulary) section of the JLPT N5. The Goi section tests the ability to choose the right word for a context, and to recognize paraphrases (synonyms / equivalent expressions).

> **Mondai 1 / Mondai 2 coverage note:** This file covers Mondai 3 + Mondai 4 of the 文字・語彙 (Vocabulary) section. **Mondai 1 (漢字読み, kanji -> reading)** and **Mondai 2 (表記, hiragana -> kanji)** are in `moji_questions_n5.md` - 50 items each, 100 total. An audit walking only this file will see what looks like a coverage gap; the missing Mondai 1+2 are in the sibling moji corpus.

## Subtypes covered

| Mondai | Subtype | Count | File |
|---|---|---|---|
| Mondai 1 | 漢字読み (kanji reading) | 50 | `moji_questions_n5.md` |
| Mondai 2 | 表記 (orthography) | 50 | `moji_questions_n5.md` |
| Mondai 3 | 文脈規定 (contextual) - choose the word that fits the blank | 50 | `goi_questions_n5.md` (this file) |
| Mondai 4 | 言い換え類義 (paraphrase) - choose the sentence with the closest meaning | 50 | `goi_questions_n5.md` (this file) |

## Notation rules

- The blank in Mondai 3 questions is shown as `（  　）`.
- Each question has 4 numbered choices. **Answer**: shows the correct number.
- All stems and correct answers use only N5-syllabus kanji. Distractors may contain non-N5 kanji where authentic JLPT format requires it (see header note in `moji_questions_n5.md` for the full kanji-scope exception).
- No em dashes (U+2014) appear in this file.

## Engine display note

For mock-test mode, the app's test engine MUST hide the `**Answer:**` line and rationale until the student commits an answer. The visible-by-default format here is for self-study reference; runtime test rendering is the engine's responsibility.

## Numeral convention

Numbers are written using both kanji forms (一, 二, 三, 五, 十, 百, 千) and arabic numerals (1, 2, 100, 1000) - mirroring authentic JLPT papers, which use kanji numerals in narrative text and arabic numerals in prices, addresses, schedules, and time tables. This is intentional, not inconsistency.

---

## Mondai 3 - 文脈規定 (Contextual Vocabulary)

50 questions. Choose the word that best fits the blank in the sentence.

## Audit policies (formalized 2026-05-04)

### Paraphrase-tightening pass (2026-05-04, v1.12.13)

Five paraphrase items in Papers 5-7 originally relied on real-world
inference rather than strict semantic equivalence:

  Q70   好き              ->  よく する
  Q76   X より Y すき      ->  Y を よく 飲む
  Q86   電話を かける      ->  電話で 話した
  Q97   じょうず           ->  よく 話せる    (also dropped N4 potential 話せます)
  Q100  ならって いる      ->  れんしゅう

Each stem was tightened in v1.12.13 by adding explicit context that
makes the keyed answer a direct paraphrase rather than an inference:
  - Q70/Q76/Q100 add a frequency clause (「まいにち する」 etc.)
  - Q86 adds the duration of conversation (「一時間 話しました」)
  - Q97 scopes じょうず to "speaking" specifically (「話すのが じょうず」)
    and replaces 話せます (N4 potential) with 上手に 話します (N5 plain).

The rationales no longer carry "by elimination" or "closest among the
four" hedges - these are now true paraphrases.

### Borderline N5 / late-N5 stretch items

Six items in this corpus rely on grammar that is canonically tested
at N4 rather than N5:

  Q47  ～たことがあります  (experience past)
  Q48  ～つもりです        (intent)
  Q62  ～あいだに          (during which)
  Q64  potential form ひけます
  Q91  ～て、N に なります (duration)
  Q97  potential form 話せます

Each is included because the structure is encountered at the strict
N5/N4 boundary and the keyed answer remains correct under the
construction. Per the project's "late_n5" tier convention (also
applied in grammar.json with 25 patterns flagged tier=late_n5), these
items are positioned as **stretch content** for learners on the cusp
of N4. Strict-N5 deployments may filter to questions outside this
list.


### Q1

まいあさ コーヒーを （　　）。

1. たべます
2. みます
3. ききます
4. のみます

**Answer: 4** - コーヒー is something one drinks (のむ).

### Q2

ばんごはんを （　　） から、テレビを 見ます。

1. のんで
2. かって
3. かいて
4. たべて

**Answer: 4** - ごはん takes たべる.

### Q3

新しい ノートを （　　）。

1. ききました
2. たべました
3. のみました
4. かいました

**Answer: 4** - ノート is bought (買います).

### Q4

きのう 友だちに （　　）。

1. かいました
2. あいました
3. しました
4. たちました

**Answer: 2** - 友だち + に + あう (to meet).

### Q5

つかれましたから、いえで （　　）。

1. はたらきます
2. やすみます
3. はしります
4. およぎます

**Answer: 2** - つかれた + やすむ. つかれましたから (polite past + から) is the N5-canonical reason -> action chain (replaces ので which leans N4 in major textbooks).

### Q6

あした こうえんへ さんぽに （　　）。

1. きます
2. でます
3. はいります
4. いきます

**Answer: 4** - direction-へ + いく.

### Q7

たなかさんは いま 学校に （　　）。

1. かいます
2. あります
3. もちます
4. います

**Answer: 4** - person + います.

### Q8

つくえの 上に 本が （　　）。

1. でます
2. います
3. たちます
4. あります

**Answer: 4** - inanimate noun + あります.

### Q9

きょうは てんきが （　　）。

1. たかいです
2. ながいです
3. やすいです
4. いいです

**Answer: 4** - てんきが いい (the weather is good).

### Q10

その 本は とても （　　）。

1. おいしいです
2. うるさいです
3. おもしろいです
4. はやいです

**Answer: 3** - 本 + おもしろい (interesting). はやい distractor replaces the prior あつい - あつい is a homophone trap (厚い "thick" is plausible for a book).

### Q11

この りんごは （　　）。

1. おもしろいです
2. たかいです
3. あおいです
4. おいしいです

**Answer: 4** - food + おいしい.

### Q12

すみませんが、もう いちど （　　） ください。

1. たべて
2. かいて
3. はなして
4. のんで

**Answer: 3** - もう いちど + 話す (say again).

### Q13

いえへ かえる まえに、ぎんこうへ （　　）。

1. いきました
2. のみました
3. たべました
4. ききました

**Answer: 1** - place-へ + いく.

### Q14

らいねんから 大学で にほんごを （　　）。

1. あいます
2. はしります
3. べんきょうします
4. やすみます

**Answer: 3** - language + べんきょうする.

### Q15

しゅくだいが おわってから、テレビを （　　）。

1. みます
2. ききます
3. のみます
4. ねます

**Answer: 1** - テレビ + みる.

### Q16

おんがくを （　　） のが すきです。

1. みる
2. かく
3. きく
4. のむ

**Answer: 3** - おんがく + きく.

### Q17

あさごはんに パンを 二まい （　　）。

1. たべました
2. のみました
3. ききました
4. はなしました

**Answer: 1** - パン + たべる.

### Q18

つめたい 水を （　　）。

1. かいました
2. ききました
3. のみました
4. たべました

**Answer: 3** - 水 + のむ.

### Q19

きのうは しごとが とても （　　）。

1. つよいでした
2. いそがしかったです
3. はやいです
4. つかれます

**Answer: 2** - past i-adj + です. しごとが いそがしい (work was busy) is the canonical N5 stem-and-answer pairing for this grammar pattern.

### Q20

子どもが こうえんで （　　） います。

1. あそんで
2. はたらいて
3. あいて
4. しまって

**Answer: 1** - 子ども + あそぶ (play).

### Q21

ほんが つくえの （　　）から おちました。

1. うえ
2. した
3. まえ
4. うしろ

**Answer: 1** - things fall from above; おちる anchors うえ uniquely (a book cannot fall from under, in front of, or behind a desk - only from on top of it).

### Q22

その みせは えきの （　　） に あります。

1. たかい
2. ながい
3. ちかく
4. つよい

**Answer: 3** - 駅の近く (near the station) - natural location phrase.

### Q23

私の いえは ここから とても （　　） です。

1. あつい
2. とおい
3. ふるい
4. きれい

**Answer: 2** - distance + とおい (far).

### Q24

きょうは あついから、まどを （　　） ください。

1. しめて
2. あけて
3. けして
4. つけて

**Answer: 2** - hot + open the window.

### Q25

ねる まえに でんきを （　　） ください。

1. あけて
2. しめて
3. けして
4. のんで

**Answer: 3** - turn off light.

### Q26

くらいですから、でんきを （　　） ください。

1. けして
2. つけて
3. しめて
4. あけて

**Answer: 2** - dark + turn on light.

### Q27

つぎの （　　） を 右に まがって ください。

1. かど
2. やま
3. はし
4. みち

**Answer: 1** - turn at the corner (かど).

### Q28

毎日 ちかてつで （　　） まで いきます。

1. みず
2. かわ
3. みち
4. かいしゃ

**Answer: 4** - by-subway + to the company.

### Q29

ふゆに なりました。 きょうは （　　） が ふって います。 とても さむいです。

1. かぜ
2. はる
3. はな
4. ゆき

**Answer: 4** - winter + さむい disambiguates to ゆき (snow).

### Q30

きのう 友だちと （　　） を 見に いきました。

1. ほん
2. でんわ
3. しんぶん
4. えいが

**Answer: 4** - 見に行く + えいが (go to see a movie).

### Q31

たんじょうびに 友だちから （　　） を もらいました。

1. しゅくだい
2. プレゼント
3. ニュース
4. しごと

**Answer: 2** - birthday + present.

### Q32

ねこは いすの 下で （　　） います。

1. はしって
2. ねて
3. はたらいて
4. かって

**Answer: 2** - cat + sleeping.

### Q33

つかれましたから、（　　） すわりました。

1. すぐ
2. もう
3. まだ
4. ぜんぜん

**Answer: 1** - immediately. (から: N5-canonical reason conjunction; replaces ので per corpus-wide policy applied alongside the Q5 fix in v1.12.14.)

### Q34

しゅくだいが むずかしくて、 （　　） わかりませんでした。

1. ぜんぜん
2. たくさん
3. すぐ
4. とても

**Answer: 1** - ぜんぜん + negative = "not at all".

### Q35

A: あした パーティーに 来ますか。 B: はい、（　　） 行きます。

1. たくさん
2. すぐ
3. まだ
4. もちろん

**Answer: 4** - もちろん (of course) is natural as confirmation in response to a Y/N question.

### Q36

おかねが ありませんから、何も （　　）。

1. かいません
2. たべました
3. のみました
4. ききました

**Answer: 1** - no money + don't buy.

### Q37

私の おとうとは 大学生では （　　）。 高校生です。

1. ありません
2. ありました
3. あります
4. ありませんでした

**Answer: 1** - present negative.

### Q38

その へやには 子どもが 三（　　） います。

1. まい
2. ほん
3. にん
4. つ

**Answer: 3** - counter for people.

### Q39

きょうしつには ボールが 五（　　） あります。

1. にん
2. つ
3. まい
4. ほん

**Answer: 2** - 〜つ is the generic native counter for small objects (1-9). ボール (ball) takes 〜つ at N5 level. (Furniture like つくえ takes 〜台 (だい) idiomatically - N4-level distinction.)

### Q40

ペンを 二（　　） 買いました。

1. つ
2. ほん
3. にん
4. まい

**Answer: 2** - counter for long thin objects.

### Q41

きってを 三（　　） ください。

1. ほん
2. にん
3. まい
4. つ

**Answer: 3** - counter for flat objects.

### Q42

しごとは いつも （　　） おわります。

1. なんじで
2. たかい
3. ちかい
4. はやく

**Answer: 4** - end early (はやく as adverb, no particle).

### Q43

私の いえから 駅まで （　　） 十分です。

1. はやい
2. ちかい
3. あるいて
4. たかい

**Answer: 3** - on foot (あるいて 十分です = "10 minutes on foot").

### Q44

きょうは あめが ふって いるから、（　　） を もって きました。

1. かばん
2. めがね
3. ぼうし
4. かさ

**Answer: 4** - rain + umbrella. (から: N5-canonical reason conjunction; replaces ので per corpus-wide policy applied alongside the Q5 fix in v1.12.14.)

### Q45

さむいですから、（　　） を きて ください。

1. ぼうし
2. かばん
3. コート
4. パジャマ

**Answer: 3** - cold + コート (coat). パジャマ replaces the prior シャツ distractor - a shirt is also wearable in cold weather, while pajamas are clearly an indoor / sleep garment.

### Q46

すみません、この みちは よく わかりません。 ちずを （　　） ください。

1. みせて
2. のんで
3. たべて
4. かって

**Answer: 1** - show me the map.

### Q47

私は にほんへ いった ことが （　　）。

1. あります
2. します
3. なります
4. います

**Answer: 1** - こと + ある (experience). Common error: 「〜たことがある」 cannot combine with specific time markers (きょねん, etc.) - it expresses indefinite past experience. Use a plain past tense (きょねん 行きました) for time-specific events instead.

### Q48

来年 大学へ （　　） つもりです。

1. いく
2. でる
3. かえる
4. すむ

**Answer: 1** - 大学へ行く (go to / attend university) - natural form for entering higher education.

### Q49

くつを （　　）から、いえに 入って ください。

1. ぬいで
2. あけて
3. しめて
4. はいて

**Answer: 1** - take off shoes (before entering).

### Q50

たろうさんは おとうさん（　　） せが たかいです。

1. が
2. より
3. の
4. に

**Answer: 2** - taller than father.

---

## Mondai 4 - 言い換え類義 (Paraphrase)

50 questions. Read sentence A. Choose the option whose meaning is closest.

### Q51

A: わたしの ちちは びょういんで はたらいて います。

_My father works at a hospital._

1. わたしの ちちは ははと はたらいて います。
2. わたしの ちちは いしゃです。
3. わたしの ちちは びょうきです。
4. わたしの ちちは 学校の 先生です。

**Answer: 2** - 「病院で はたらく」 ≈ 「いしゃです」. N5 pragmatic substitution (working at a hospital is the standard textbook paraphrase of "is a doctor", though strictly someone could work at a hospital without being a doctor - nurse, admin). Tests the N5 vocab triangle 病院 / はたらく / いしゃ; replaces the prior tautological 「父は医者 = 父の仕事は医者」 which tested no vocabulary.

### Q52

A: この りょうりは おいしくないです。

1. この りょうりは おいしいです。
2. この りょうりは あまいです。
3. この りょうりは まずいです。
4. この りょうりは すきです。

**Answer: 3** - おいしくない ≈ まずい.

### Q53

A: たなかさんは えいごを おしえて います。

1. たなかさんは えいごの 学生です。
2. たなかさんは アメリカ人です。
3. たなかさんは えいごを ならって います。
4. たなかさんは えいごの 先生です。

**Answer: 4** - 「英語を教えている」 → 「英語の先生」: a person who teaches X is the teacher of X. Functional relationship; closest among the four options.

### Q54

A: わたしは まいにち 七時に おきます。

1. わたしは よる 七時に おきます。
2. わたしは あさ 七時に ねます。
3. わたしは あさ 七時に おきます。
4. わたしは よる 七時に ねます。

**Answer: 3** - 起きる + 朝 (morning) is the typical context.

### Q55

A: しゅくだいは ぜんぶ おわりました。

1. しゅくだいが すこし のこって います。
2. しゅくだいは まだ ありません。
3. しゅくだいは ぜんぶ しました。
4. しゅくだいは ぜんぜん しません でした。

**Answer: 3** - ぜんぶ おわった ≈ ぜんぶ した.

### Q56

A: あの レストランは とても 高いです。

1. あの レストランは やすいです。
2. あの レストランは たかい たてものです。
3. あの レストランは たかい りょうりが あります。
4. あの レストランは おかねが たくさん いります。

**Answer: 4** - 高い (expensive) ≈ おかねが たくさん いる.

### Q57

A: わたしは くだものが 大すきです。

1. わたしは くだものが すきじゃ ありません。
2. わたしは くだものが きらいです。
3. わたしは くだものを たべません。
4. わたしは くだものを よく たべます。

**Answer: 4** - 大すき + よく食べる.

### Q58

A: きのうの よる、はやく ねました。

1. きのう おそく ねました。
2. きのう はやく ねました。
3. きのうの あさ、おそく おきました。
4. きのうの あさ、はやく おきました。

**Answer: 2** - paraphrase identical with kanji.

### Q59

A: にちようびは ひまです。

1. にちようびは いそがしいです。
2. にちようびは しごとが あります。
3. にちようびは じかんが あります。
4. にちようびは つかれて います。

**Answer: 3** - ひま ≈ じかんが ある.

### Q60

A: きょうしつに 学生が おおぜい います。

1. きょうしつには 学生が ぜんぜん いません。
2. きょうしつには 学生が たくさん います。
3. きょうしつには 学生が 一人 います。
4. きょうしつには 学生が 二人 います。

**Answer: 2** - おおぜい (many people) is the closest match among the choices. Strictly, おおぜい is restricted to people while たくさん is general (people, things, abstract); the substitution works here because the noun is 学生 (people).

### Q61

A: わたしは いま おなかが すいて います。

1. わたしは いま 何か たべたいです。
2. わたしは いま 何か のみたいです。
3. わたしは いま ねたいです。
4. わたしは いま やすみたいです。

**Answer: 1** - hungry → want to eat.

### Q62

A: でんしゃの 中で 本を 読みました。

1. でんしゃで 本を かいました。
2. でんしゃに のる まえに 本を 読みました。
3. でんしゃに のって いる あいだに 本を 読みました。
4. でんしゃの まえで 本を 読みました。

**Answer: 3** - inside the train while riding.

### Q63

A: わたしの いえは 駅から とおく ありません。

1. わたしの いえは 駅から とても とおいです。
2. わたしの いえは 駅の 中に あります。
3. わたしの いえは 駅の 上に あります。
4. わたしの いえは 駅から ちかいです。

**Answer: 4** - とおくない ≈ ちかい (direct antonym pair).

### Q64

A: たなかさんは じょうずに ピアノを ひきます。

1. たなかさんは ピアノが へたです。
2. たなかさんは ピアノを はじめて ひきます。
3. たなかさんは ピアノが きらいです。
4. たなかさんは ピアノを ひくのが じょうずです。

**Answer: 4** - 「じょうずに ひく」 = 「ひくのが じょうず」. Same skill, different syntactic frame (adverbial -> nominalized adjective predicate). Strict-N5: drops the previous keyed form 「よく ひけます」 (potential ひける = N4) per the same policy applied at Q97 in v1.12.13. This is the inverse direction of Q97's frame swap (Q97: nominalized -> adverbial; Q64: adverbial -> nominalized).

### Q65

A: もう おそいから、いえに かえりましょう。

1. もう はやいから、もう少し いましょう。
2. しごとが はやく おわったから、かえりましょう。
3. じかんが おそく なったから、いえに かえりましょう。
4. もう おそいから、ねましょう。

**Answer: 3** - もう おそい ≈ じかんが おそい.

### Q66

A: その みせは くだものを うって います。

1. その みせは くだものを かいます。
2. その みせは くだものが すきです。
3. その みせは くだものの みせです。
4. その みせは くだものを たべます。

**Answer: 3** - shop selling fruit = fruit shop.

### Q67

A: きのう びょうきで 学校を やすみました。

1. きのうは げんきでした。
2. きのうは 学校に いきませんでした。
3. きのうは 学校で べんきょうしました。
4. きのうは よる おそくまで 学校に いました。

**Answer: 2** - missed school = didn't go.

### Q68

A: だれも きょうしつに いません。

_There is no one in the classroom._

1. きょうしつに 人が いません。
2. きょうしつに 一人 います。
3. きょうしつに 二人 います。
4. きょうしつに 学生が おおぜい います。

**Answer: 1** - だれも (no one - universal over people) = 人が いません (no people). Both negate the existence of any person, so the scope matches exactly.

### Q69

A: しゅくだいは まだ おわって いません。

1. しゅくだいは ぜんぶ おわりました。
2. しゅくだいは すこし のこって います。
3. しゅくだいは あしたから します。
4. しゅくだいは ありません。

**Answer: 2** - not finished yet ≈ some remaining.

### Q70

A: たろうさんは スポーツが すきで、 まいにち します。

_Taro likes sports and does them every day._

1. たろうさんは スポーツを よく します。
2. たろうさんは スポーツを 見ません。
3. たろうさんは スポーツを ぜんぜん しません。
4. たろうさんは スポーツが きらいです。

**Answer: 1** - 「すき + まいにち する」 = 「よく する」. The frequency context makes this a direct paraphrase rather than an inference from liking alone.

### Q71

A: きょうしつは しずかです。

1. きょうしつは うるさいです。
2. きょうしつには だれも いません。
3. きょうしつでは 学生が ねて います。
4. きょうしつには おとが ありません。

**Answer: 4** - quiet = no sound.

### Q72

A: あした しけんが あります。

1. あした テストが あります。
2. あした やすみです。
3. あした パーティーが あります。
4. あした しごとが ありません。

**Answer: 1** - 試験 ≈ テスト.

### Q73

A: 友だちに 本を かしました。

1. 友だちは 私に 本を かしました。
2. 友だちは 私から 本を かりました。
3. 友だちが 私に 本を あげました。
4. 私は 友だちから 本を もらいました。

**Answer: 2** - 「私が友だちに貸す」 = 「友だちが私から借りる」 (perspective inversion of かす ⇄ かりる).

### Q74

A: わたしは バスに のって 学校へ いきます。

1. わたしは あるいて 学校へ いきます。
2. わたしは でんしゃで 学校へ いきます。
3. わたしは バスで 学校へ いきます。
4. わたしは じてんしゃで 学校へ いきます。

**Answer: 3** - のって ≈ で.

### Q75

A: ことしの 一月に 日本へ きました。

1. らいねん 日本へ いきます。
2. ことしの はじめに 日本へ きました。
3. 一年 まえに 日本へ きました。
4. きょねんの 一月に 日本へ きました。

**Answer: 2** - 一月 (January) is the beginning of the year. The other options describe a different time (next year, last year, one year ago).

### Q76

A: わたしは おちゃより コーヒーの ほうが すきで、 まいにち 飲みます。

_I prefer coffee to tea, and drink it every day._

1. わたしは コーヒーより おちゃの ほうが すきです。
2. わたしは おちゃと コーヒーが すきです。
3. わたしは おちゃが きらいで、コーヒーが すきです。
4. わたしは コーヒーを よく のみます。

**Answer: 4** - 「コーヒーの ほうが すき + まいにち 飲む」 = 「コーヒーを よく 飲む」. The frequency clause makes the preference paraphrase direct.

### Q77

A: しゅくだいは むずかしくないです。

1. しゅくだいは やさしいです。
2. しゅくだいは むずかしいです。
3. しゅくだいは おもしろいです。
4. しゅくだいは ながいです。

**Answer: 1** - not difficult ≈ easy.

### Q78

A: あの レストランは いつも おきゃくさんが おおいです。

1. あの レストランは おきゃくさんが すくないです。
2. あの レストランは いつも すいて います。
3. あの レストランは いつも こんで います。
4. あの レストランは とおいです。

**Answer: 3** - お客さんが多い ≈ こんで いる (crowded). At N5 level these are paraphrasable; strictly, "many customers" describes count and "crowded" describes density.

### Q79

A: たなかさんの いえは 大きくないです。

_Tanaka-san's house is not big._

1. たなかさんの いえは ちいさいです。
2. たなかさんの いえは 大きいです。
3. たなかさんの いえは あたらしいです。
4. たなかさんの いえは ふるいです。

**Answer: 1** - by elimination among the four options. Strictly, 大きくない (not big) is broader than ちいさい (small) - 中ぐらい (medium-sized) also fits 大きくない. Among the four options, ちいさい is the closest single-word match.

### Q80

A: きょうは あつくないです。

1. きょうは すずしいです。
2. きょうは あついです。
3. きょうは あたたかいです。
4. きょうは ねむいです。

**Answer: 1** - by elimination among the four options. Strictly, あつくない (not hot) is broader than すずしい (cool) - "warm" (あたたかい) also qualifies as "not hot" - but the other three options are clearly wrong (あつい = opposite meaning; あたたかい = different temperature property; ねむい = irrelevant property), so すずしい is the closest fit.

### Q81

A: その しごとを する 人は いません。

1. みんなが その しごとを します。
2. その しごとは おもしろいです。
3. その しごとは おわりました。
4. だれも その しごとを しません。

**Answer: 4** - 人がいない = だれもしない.

### Q82

A: きょうは あめが ふって います。

1. きょうは てんきが いいです。
2. きょうは そらが くもって います。
3. きょうは てんきが よくないです。
4. きょうは ゆきが ふって います。

**Answer: 3** - 雨が降っている = 天気がよくない (direct weather-state paraphrase).

### Q83

A: 友だちから 本を かりました。

1. 友だちが 私に 本を かしました。
2. 友だちが 私から 本を かりました。
3. 私が 友だちに 本を あげました。
4. 友だちは 本を かいました。

**Answer: 1** - borrowed = friend lent.

### Q84

A: きょうは 時間が ありません。

1. きょうは ひまです。
2. きょうは げんきです。
3. きょうは つかれて います。
4. きょうは いそがしいです。

**Answer: 4** - no time ≈ busy.

### Q85

A: こうえんで さんぽしました。

1. こうえんで あそびました。
2. こうえんを あるきました。
3. こうえんで すわりました。
4. こうえんに いきました。

**Answer: 2** - 散歩 ≈ 歩く.

### Q86

A: 友だちに でんわを かけて、 一時間 話しました。

_I called my friend and we talked for an hour._

1. 友だちが でんわを くれました。
2. 友だちと でんわで 話しました。
3. でんわを 買いました。
4. 友だちに 手紙を 書きました。

**Answer: 2** - 「電話を かけて + 一時間 話した」 = 「電話で 話した」. The "talked for one hour" context confirms a successful conversation, removing the inference gap.

### Q87

A: わたしは 二十さいです。

1. わたしは ことし 二十さいに なります。
2. わたしの たんじょうびは あした です。
3. わたしは いま 二十さいです。
4. わたしは らいねん 二十さいに なります。

**Answer: 3** - statement of present age. The keyed answer 「いま 二十さいです」 is a direct restatement of the stem's present-tense identity claim; the other options shift the time reference (this year / birthday tomorrow / next year). The special reading はたち for 二十さい is documented at vocabulary_n5.md but does not bear on the time-reference test point this question targets.

### Q88

A: きょうしつには つくえが いっぱい あります。

1. きょうしつには つくえが すこし あります。
2. きょうしつには つくえが たくさん あります。
3. きょうしつには つくえが ありません。
4. きょうしつには つくえが ひとつ あります。

**Answer: 2** - いっぱい ≈ たくさん.

### Q89

A: その くつは 高かったです。

_Those shoes were expensive._

1. その くつは とても やすいです。
2. その くつに とても たくさん お金を はらいました。
3. その くつは ながかったです。
4. その くつは よかったです。

**Answer: 2** - 高かった (was expensive) = たくさん お金を 払った (paid a lot of money). Note: 「高い お金」 is unnatural Japanese - money is not 高い/安い; ねだん (price) is. Hence the rewording from a prior version.

### Q90

A: たろうさんは げんきです。

1. たろうさんは びょうきです。
2. たろうさんは つかれて います。
3. たろうさんは びょうきでは ありません。
4. たろうさんは いそがしいです。

**Answer: 3** - 元気 (well, lively) and 病気ではない (not sick) overlap in everyday usage. Closest among the four options; strictly, 元気 implies vigor, not just absence of illness.

### Q91

A: わたしは 日本に きて 一年に なります。

1. わたしは 来年 日本へ きます。
2. わたしは 一年 まえに 日本を 出ました。
3. わたしは 一年 まえから 日本に います。
4. わたしは 一年 だけ 日本に いました。

**Answer: 3** - here for 1 year = came 1 year ago.

### Q92

A: 友だちに たんじょうびの プレゼントを あげました。

1. 友だちが 私に プレゼントを あげました。
2. 友だちは 私から プレゼントを もらいました。
3. 私が 友だちから プレゼントを もらいました。
4. 友だちは プレゼントを 買いませんでした。

**Answer: 2** - 「私が友だちにあげる」 = 「友だちが私からもらう」 (perspective inversion of あげる ⇄ もらう).

### Q93

A: あした しごとが ありません。

1. あした やすみです。
2. あした しごとが おそく おわります。
3. あした しごとに いきます。
4. あした しごとが はじまります。

**Answer: 1** - no work tomorrow = day off.

### Q94

A: この みせの ケーキは あまくないです。

_The cake at this shop is not sweet._

1. この みせの ケーキは あまいです。
2. この みせの ケーキは からい です。
3. この みせの ケーキは あまく ありません。
4. この みせの ケーキは おいしくないです。

**Answer: 3** - あまくないです (i-adj + です polite neg) = あまく ありません (formal polite neg). Two equivalent polite negative forms of i-adjectives - a true synonymy item rather than a graded approximation. Same meaning, different polite form.

### Q95

A: たなかさんは いつも しずかです。

1. たなかさんは いつも あまり 話しません。
2. たなかさんは いつも たくさん 話します。
3. たなかさんは いつも うるさいです。
4. たなかさんは いつも おこって います。

**Answer: 1** - quiet ≈ doesn't talk much.

### Q96

A: きょうは ゆうがた に かえります。

1. きょうは よる おそく かえります。
2. きょうは あさ はやく かえります。
3. きょうは ひるごろ かえります。
4. きょうは よるの まえに かえります。

**Answer: 4** - 夕方 ≈ 夜の前 (before night).

### Q97

A: たろうさんは 日本ごを 話すのが じょうずです。

_Taro is good at speaking Japanese._

1. たろうさんは 日本ごを 上手に 話します。
2. たろうさんは 日本ごが ぜんぜん わかりません。
3. たろうさんは 日本ごが すきじゃ ありません。
4. たろうさんは 日本ごを ならって います。

**Answer: 1** - 「話すのが じょうず」 = 「上手に 話す」. Same skill, different syntactic frame (nominalized adjective vs. adverbial). Strict-N5: also drops the potential form 話せます (N4) used in a previous version.

### Q98

A: わたしは あした しゅくだいを 出します。

_I will submit my homework tomorrow._

1. あした しゅくだいを はじめます。
2. あした、 わたしは しゅくだいを 先生に もって いきます。
3. あした しゅくだいを かいます。
4. あした しゅくだいを かえします。

**Answer: 2** - 「(教師に) しゅくだいを 出す」 ≈ 「先生に しゅくだいを もって いく」. Submitting homework to a teacher is paraphrased as physically taking it to them. Strict-N5: replaces the previous keyed verb わたす (vocabulary_n5.md [Ext] borderline N5/N4) with もって いく - both もつ and いく are core N5; わたす no longer appears in the goi corpus. Note: kept in kana since 持 is not in the kanji whitelist.

### Q99

A: わたしは スペインから きました。

_I came from Spain._

1. わたしは スペインへ いきます。
2. わたしは スペイン人です。
3. わたしは スペインの 人と ともだちです。
4. わたしは スペインごを 話します。

**Answer: 2** - X から きた ≈ X 人. N5 pragmatic substitution: at this level "came from X" is the standard textbook paraphrase of nationality, even though strictly someone could come from X without being X-jin (tourist, long-term resident, expat returning home). Closest among the four offered options.

### Q100

A: わたしは ピアノを ならって、 まいにち れんしゅうします。

_I'm taking piano lessons and practice every day._

1. わたしは ピアノが よく わかります。
2. わたしは ピアノを 売って います。
3. わたしは ピアノを 買いました。
4. わたしは ピアノの れんしゅうを して います。

**Answer: 4** - 「ならって + まいにち れんしゅうする」 = 「れんしゅうを して いる」. Lessons + daily practice is a direct paraphrase of "doing practice", not an inference from "is taking lessons".

## End of file

100 questions complete: 50 文脈規定 + 50 言い換え類義.

Continues in `bunpou_questions_n5.md` and `dokkai_questions_n5.md`.
