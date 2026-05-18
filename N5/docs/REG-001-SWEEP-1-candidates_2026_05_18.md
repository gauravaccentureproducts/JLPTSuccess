# REG-001 SWEEP-1 candidates (run 2026-05-18)

Per REG-001 (BUG-106) sweep protocol, this report lists every
`wrong_corrected_pair` entry across `data/grammar.json` whose
`error_category` is `register` OR whose `why` field references
register/elevation/politeness terms.

Each candidate needs per-entry native-speaker classification:

- **A** — genuine register-variant → migrate to `register_variant`
- **B** — genuine ungrammatical → keep as `wrong_corrected_pair`
- **C** — pragmatic-mismatch (different from register; e.g. ね-seeking-agreement-when-listener-cannot-evaluate) → keep but re-categorize

Total candidates: **89**.

The n5-046 entry was already migrated by this commit (REG-001
close-out). Remaining candidates surface as follow-up bug
filings (REG-002..NN) for batched fix cycles.

## Triage table

| Pattern | index | wrong (truncated) | correct (truncated) | why (truncated) | category |
|---|---|---|---|---|---|
| n5-001 | 0 | わたし がくせい。 | わたしは がくせいです。 | Polite predicate requires です; bare nouns are casual incomplete sentences. | register |
| n5-004 | 2 | みずを のみたい。 | みずが のみたい。 | With Vたい (desiderative), the desired object usually takes が in plain N5 register | particle |
| n5-016 | 2 | こちらは どこ ですか。 (asking your own location) | ここは どこ ですか。 | こちら is polite/direction ("this way / over here"); ここ is the spatial pronoun ("he | lexicon |
| n5-017 | 1 | なにを たべます？ (in writing, end with ?) | なにを たべますか。 | Formal Japanese ends questions with か。, not ?. The question particle is the mark | word_order |
| n5-018 | 0 | せんせい、だれですか。 (asking the teacher politely) | せんせい、どなたですか。 | どなた is the polite form of だれ; use it when speaking to/about superiors. | register |
| n5-023 | 0 | たべます か? | たべますか。 | Formal Japanese ends questions with か。. Combining か + ? is non-standard. | word_order |
| n5-023 | 1 | なにを たべます。 (intent: question) | なにを たべますか。 | Wh-questions still need か at the end in formal Japanese. | word_order |
| n5-025 | 0 | いい てんきです ね。 (about your own observation, no agreement sought | いい てんきです。 | ね seeks agreement / shared perception. If listener cannot evaluate, ね sounds odd | register |
| n5-026 | 1 | がくせいですよ。 (in formal context to teacher) | がくせいです。 | よ has assertive tone; can sound presumptuous to seniors. In formal context omit  | register |
| n5-027 | 1 | がくせい です よね。 (about your own status) | がくせい です。 | よね assumes shared knowledge; for facts only you know, drop it. | register |
| n5-030 | 2 | はしりますの は たのしいです。 | はしるのは たのしいです。 | Nominalizer の attaches to PLAIN form, not polite ます-form. | conjugation |
| n5-041 | 1 | こちらは どこ。 (asking own location) | ここは どこ ですか。 | こちら is polite/direction; for spatial pronoun "here" use ここ. | lexicon |
| n5-042 | 0 | こちらは どこ ですか。 (asking where you are, casually) | ここは どこ ですか。 | こちら is polite/direction; for plain spatial use ここ. | register |
| n5-045 | 2 | なんで にほんへ きましたか。 (asked formally) | どうやって にほんへ きましたか。 | なんで is casual/multifunction (why? / by what means?); use どうやって for clear "by wha | register |
| n5-048 | 1 | どこから きましたか。 (asking origin politely) | どちらから いらっしゃいましたか。 | In formal contexts use どちら + irassyaru; どこ is neutral. | register |
| n5-050 | 0 | コーヒー どう ですか。 (in formal context to client) | コーヒー、いかがですか。 | いかが is the polite form of どう; use it with seniors/clients. | register |
| n5-054 | 2 | おとうさんは いくつ ですか。 (asking parent's age in formal context) | おとうさんは おいくつですか。 | For polite age-asking add お (oikutsu). | register |
| n5-058 | 1 | わたしは まいにち がっこうへ いきますね。 | わたしは まいにち がっこうへ いきます。 | Habitual statement of fact does not need ね; ね seeks agreement and softens declar | register |
| n5-060 | 1 | いきました でした。 | いきました。 | ました already encodes past + polite. Do not add でした (which is past of です/copula). | conjugation |
| n5-061 | 0 | たべませんかった。 | たべませんでした。 | Polite past-negative is ませんでした (not ませんかった). The past tense sits in でした. | conjugation |
| n5-061 | 1 | たべなかったでした。 | たべませんでした。 / たべなかった。 | Plain なかった + でした is double-marking. Use polite ませんでした OR plain なかった. | conjugation |
| n5-061 | 2 | きのう たべませんでした か。 (rising) | きのう たべましたか。 (with なに or asking confirmation) | Negative-question form often implies "did you not eat?" expecting yes; use caref | register |
| n5-062 | 1 | あした たべましょう。 (to a stranger) | あした たべませんか。 | ましょう is "let's" (assumes agreement); 〜ませんか is more polite invitation to a strang | register |
| n5-064 | 0 | いきます か。 (intent: would you like to go) | いきませんか。 | Polite invitation uses negative form ませんか ("won't you...?"); positive ますか is a y | lexicon |
| n5-064 | 1 | いきませんでしたか。 (intent: invitation in past) | いきませんでしたか。 | ませんでしたか is a question about a past event ("did you not go?"), NOT a past invitat | register |
| n5-064 | 2 | いっしょに たべませんか? | いっしょに たべませんか。 | Use 。 not ?; question-mark is not standard in formal Japanese (though acceptable | word_order |
| n5-065 | 0 | たべる ます。 | たべます。 | Polite form drops る from Group-2 stem and adds ます. Do not keep both. | conjugation |
| n5-066 | 0 | 行きないです。 | 行きません。 / 行かないです。 | Polite negative is ません; plain negative of 行く is 行かない (NOT 行きない). | conjugation |
| n5-068 | 0 | たべなかったでした。 | たべなかった。 / たべませんでした。 | なかった is plain past-negative; do not add でした. Use one register or the other. | conjugation |
| n5-070 | 2 | いって たべます。 | いって、たべます。 | In wakachi-gaki / formal text, comma after て is conventional for clarity. | word_order |
| n5-071 | 1 | おきてください。 (in commanding tone to a senior) | おきていただけませんか。 | 〜てください is request, but to seniors use higher-respect 〜ていただけませんか. | register |
| n5-074 | 0 | たべてもいいか。 (to teacher) | たべてもいいですか。 | Permission-asking to a senior must keep です; dropping です is too casual. | register |
| n5-075 | 1 | たべて は いけない。 (to a customer) | おたべに ならないでください。 / ごえんりょください。 | てはいけない is direct prohibition, too blunt for customers; use polite ごえんりょください. | register |
| n5-076 | 1 | おきましてから、シャワーを あびます。 | おきてから、シャワーを あびます。 | てから takes plain te-form, not ましてから (overly formal/incorrect for N5). | register |
| n5-077 | 2 | いかないでください。 (to a friend casually) | いかないで。 | Plain casual register drops ください: ないで alone is fine with intimates. | register |
| n5-079 | 1 | いいです。 (about an offer, intent: no thanks) | けっこうです。 / だいじょうぶです。 | いいです can mean "good" OR "no thanks" depending on context — risky in offers. Use  | register |
| n5-082 | 2 | たかくありませんかった。 | たかくありませんでした。 | Polite past-negative is くありませんでした (not くありませんかった); the past tense lives in でした. | conjugation |
| n5-087 | 2 | げんきだったです。 | げんきでした。 | Plain past だった + です is double-marking. Use polite past でした directly. | register |
| n5-094 | 1 | ほんが あった。 (about future possession) | ほんが あります。 | あった is plain past; non-past plain is ある, polite is あります. | conjugation |
| n5-097 | 1 | A と B と、どっちが すきですか。 (in formal context) | A と B と、どちらが すきですか。 | どっち is casual; どちら is polite. Match register. | register |
| n5-100 | 2 | わたしは じょうずです。 (about myself) | わたしは あまり じょうずじゃありません。 | Calling oneself 上手 is culturally arrogant; use modest じょうずじゃありません or まだまだ. | register |
| n5-101 | 2 | せんせいは くるまが ほしいです。 | せんせいは くるまを ほしがっています。 | ほしい with 1st-person OK; 3rd-person requires ほしがっている (observable wanting-behavior | register |
| n5-102 | 2 | わかってる。 (in formal context) | わかります。 / わかっています。 | わかってる is plain spoken contraction; in polite contexts use わかります. | register |
| n5-104 | 2 | せんせいは すしを たべたいです。 | せんせいは すしを たべたがっています。 | 〜たい reports 1st-person desire only; 3rd-person uses 〜たがっている (observable behavior | register |
| n5-106 | 1 | ともだちは くるまが ほしいです。 | ともだちは くるまを ほしがっています。 | ほしい works for 1st person; 3rd-person needs ほしがる (observable wanting). | register |
| n5-113 | 1 | にじはん ぐらい です ね。 | にじはん ぐらい です。 | Confirming time to listener can use ね; depends on shared context. | register |
| n5-119 | 0 | たべますまえに、 てを あらいます。 | たべるまえに、 てを あらいます。 | まえに takes plain dictionary form, not polite ます. | conjugation |
| n5-123 | 1 | でも、それは ちがうです。 | でも、それは ちがいます。 | ちがう is a Group-1 verb, not adjective: polite is ちがいます (not ちがうです). | conjugation |
| n5-125 | 0 | では、たべる。 (in formal context to teacher) | では、いただきます。 / それでは、はじめます。 | では is formal "well then"; pair with formal continuation. | register |
| n5-125 | 1 | じゃ、せんせい。 (to a teacher) | では、せんせい。 | じゃ is the casual contraction of では; use では in formal contexts. | register |
| n5-125 | 2 | では、また あした。 (to a friend) | じゃ、また あした。 | では is formal; among friends じゃ is more natural. | register |
| n5-127 | 0 | たかい けど、おいしい。 (in formal context) | たかい けれど、おいしい。 / たかい です が、おいしい です。 | けど is the casual form of けれど; use けれど (or が) in formal context. | register |
| n5-129 | 0 | どうして いきますか。 おそい から です。 | どうして いかないんですか。 おそいからです。 | For "why" + reason explanation often use 〜んです (explanatory). Plain Vます is too ne | lexicon |
| n5-129 | 2 | なぜから、いきます。 | なぜなら、いきます。 | Reason connector is なぜなら (formal/written), not なぜから. | lexicon |
| n5-131 | 1 | せんせいに プレゼントを もらいました。 (about teacher → student) | せんせいから プレゼントを いただきました。 | Receiving from a senior uses humble いただく. | register |
| n5-132 | 1 | せんせい が ほんを くれました。 | せんせい が ほんを くださいました。 | Senior (先生) giving to me = honorific くださる (くださいました). | register |
| n5-134 | 2 | おそいですので、 いきません。 | おそいので、 いきません。 | ので takes plain form on the left in standard usage. ですので exists but is heavier. | register |
| n5-135 | 0 | よみますほん。 | よむ ほん。 | V-plain modifies noun; do NOT use polite ます-form before noun. | conjugation |
| n5-145 | 0 | あめが ふりますと おもいます。 | あめが ふると おもいます。 | 〜とおもう takes plain form (Vる/Vない/Vた); polite ます-form before と is non-standard. | conjugation |
| n5-145 | 2 | がくせいだと おもう です。 | がくせいだと おもいます。 | おもう can be plain; if attaching to something stack-able, use polite おもいます (consis | register |
| n5-150 | 1 | みずを おねがい ください。 | みずを おねがいします。 | Standard polite request is おねがいします (one phrase). おねがいください is non-standard. | lexicon |
| n5-151 | 1 | コーヒーは どう ですか。 (in formal context to senior) | コーヒーは いかがですか。 | いかが is polite version of どう; use with seniors. | register |
| n5-152 | 0 | どうもありがとう。 (intent: a casual thanks to friend) | ありがとう。 / どうも。 | どうもありがとう is mid-formality; pure casual is どうも or ありがとう. | register |
| n5-152 | 1 | すみません どうも おねがいします どうぞ。 | すみません、おねがいします。 | Stacking polite phrases is unnecessary; one fits the context. | lexicon |
| n5-152 | 2 | どうも、いいです。 (declining offer politely) | いいえ、けっこうです。 | For polite refusal use いいえ + けっこう/だいじょうぶ; どうも is too short. | register |
| n5-159 | 2 | たかいですね、いいです。 | たかいですね。 | Stand-alone ね is a complete utterance (rising tone seeks agreement). | register |
| n5-162 | 0 | たべますまえに。 | たべるまえに。 | まえに takes plain dictionary form, not polite ます. | conjugation |
| n5-163 | 2 | たべました あとで。 | たべたあとで。 | Polite ました cannot precede あとで; use plain past Vた. | conjugation |
| n5-164 | 0 | わたしさんは がくせいです。 (about yourself) | わたしは がくせいです。 | Never add さん to your own name. さん is for OTHERS. | register |
| n5-164 | 1 | やまださまさん。 | やまださま。 / やまださん。 | Do not stack honorifics さま + さん; choose one (さま is more formal). | word_order |
| n5-166 | 1 | ごちそうさまだ。 | ごちそうさま。 / ごちそうさまでした。 | Set phrase; standard polite form is ごちそうさまでした (after meal). | register |
| n5-166 | 2 | おはよう ございます。 (between intimates, casual time) | おはよう。 | おはようございます is polite; おはよう alone for casual. | register |
| n5-167 | 1 | たべましたんです。 | たべたんです。 | 〜んです attaches to PLAIN form (Vた/Vる/Vない), not polite ます-form. Drop ました → たべた + んで | conjugation |
| n5-167 | 2 | がくせいなんです。 (intent: I am a student — neutral) | がくせいです。 | 〜んです adds explanatory nuance; use plain です for neutral statement. Overusing んです  | register |
| n5-168 | 2 | たべたり よんだり します ます。 | たべたり よんだり します。 | する becomes polite します at end; do not double ます. | conjugation |
| n5-169 | 1 | いったことが ありますね。 (about your own experience) | いったことが あります。 | ね about your own experience implies seeking listener confirmation, which is odd. | register |
| n5-170 | 1 | たべない ほうがいい です ね。 (commanding) | たべない ほうがいいですよ。 | Advisory uses よ (informing) more than ね (seeking agreement). | register |
| n5-170 | 2 | たべた ほうが いい だ。 | たべた ほうが いい。 | いい is an adjective; do not append だ. Use plain いい or polite いいです. | conjugation |
| n5-171 | 0 | たべない ほうが いいですね。 (commanding tone) | たべない ほうが いいですよ。 | Advice typically uses よ (informing); ね (agreement-seeking) sounds odd here. | register |
| n5-173 | 1 | たべなくちゃ いけない。 (in formal context) | たべなくては いけません。 | なくちゃ is casual contraction of なくては; in formal use full form + ません. | register |
| n5-173 | 2 | たべないと いけない。 (intent: in formal context) | たべなくては いけません。 | ないと-いけない and なくては-いけない overlap; なくては is more formal. | register |
| n5-174 | 0 | たべなくては だめです。 | たべなくては なりません。 | Standard formal closer is なりません. だめ is more casual. | register |
| n5-176 | 0 | たべなくちゃ いけません。 (in formal speech) | たべなくては いけません。 | なくちゃ is casual contraction; in formal use なくては. | register |
| n5-178 | 0 | たべますつもりです。 | たべるつもりです。 | つもり attaches to PLAIN form (Vる/Vない), not polite ます. | conjugation |
| n5-179 | 0 | たなかさんは くるって いいました。 | たなかさんは くるって。 / たなかさんが くると いいました。 | って is casual quotative ("said"); often standalone. Stacking with といいました mixes re | register |
| n5-179 | 1 | たなかさんですって? (in formal context) | たなかさんですか。 | 〜って? as a question is casual; in formal context use か. | register |
| n5-179 | 2 | がくせいだって、しかし わかりません。 (intent: I hear he's a student but I don | がくせいだそうですが、よくわかりません。 | Hearsay in N5 written form is そうです; って is conversational. | register |
| n5-181 | 2 | たかいなあ ですね。 | たかいなあ。 / たかいですね。 | なあ and ですね are alternative emphatic endings; do not stack. | register |
| n5-188 | 2 | たべますことが できます。 | たべることが できます。 | こと attaches to PLAIN form (Vる), not polite ます. | conjugation |

## Notes

- The n5-046 entry that triggered REG-001 was migrated in the
  same commit (now in `common_mistakes` as `kind: register_variant`).
- Many `wrong_corrected_pair` entries flagged here are NOT
  register-variants — e.g. `n5-001 わたし がくせい。 → わたしは
  がくせいです。` is a genuine incomplete-sentence error, not a
  register choice. The sweep flag is a candidate, not a verdict.
- The triage requires reading the FULL context of each entry
  (what the surrounding pattern teaches, what level the
  surrounding examples assume, etc.) and a native-speaker
  judgment on each case. That work is scoped as a separate
  REG-002..NN bug batch.

- Bounded-coverage phrasing: this sweep catches candidates
  where the trigger-markers fire (register-keyword in `why`
  or `error_category=register`). A more subtle register-
  conflation that uses no flagged keyword would slip past.
  The new CI invariants (INV-REG-1..5, wired as JA-123..127
  in this commit) catch the structural symptoms of the
  defect, not the keyword presence — they are the durable
  guard regardless of which review surface catches the entry.
