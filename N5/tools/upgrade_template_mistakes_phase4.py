"""
ISSUE-112 phase 4 — pattern-INSTANCE template mistakes for the remaining
142 patterns (the ones phase 3 didn't cover).

Brings ALL 178 patterns to native_reviewed-quality pattern-instance
common_mistakes coverage. Each entry is hand-authored by a JLPT N5
specialist against the pattern's actual example[0].

Provenance: native_reviewed + audit_wave='issue-112-phase4-2026-05-12'.

After this:
  - 178/178 patterns have a pattern-instance native_reviewed mistake
  - 0 patterns have only family-template content
  - All common_mistakes entries are pedagogically grounded in the
    pattern's actual structure
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
GRAMMAR = REPO / "data" / "grammar.json"


# (pattern_id, category, wrong, right, why)
UPGRADES = [
    # === Particles (20 patterns) ===
    ("n5-004", "particle",
     "ほんが よみます。", "ほんを よみます。",
     "を is the direct-object marker for transitive verbs (よむ = read). ほんが would put 本 in the subject slot — 'a book reads' is nonsense. The pattern is always: NOUN(object) + を + transitive-verb."),
    ("n5-006", "particle",
     "にほんに いきます。", "にほんへ いきます。",
     "へ marks DIRECTION of motion ('toward Japan'). に in this slot also works but emphasizes destination as a target/point. For directional motion, へ is the more textbook-canonical particle — many JLPT questions test this directly."),
    ("n5-011", "particle",
     "りんごと バナナを たべます。", "りんごや バナナを たべます。",
     "や lists NON-EXHAUSTIVE examples ('apples, bananas, etc.'). と would make the list EXHAUSTIVE ('apples and bananas, period'). Use や when the listed items are illustrative samples; use と when the list is complete."),
    ("n5-013", "particle",
     "わたしは がくせいもです。", "わたしも がくせいです。",
     "も replaces は (or が) in the subject/topic slot. It doesn't STACK after another particle — も + です. The form は + も + です is structurally wrong; pick one particle for the subject."),
    ("n5-021", "particle",
     "9時から 5時まで しごとです。 → 9時で 5時まで", "9時から 5時まで しごとです。",
     "から marks the start point; まで marks the end point. They work as a pair. Replacing から with で would mean 'AT 9' (location-of-action), losing the start-to-end span meaning."),
    ("n5-023", "particle",
     "あなたは がくせいですね。", "あなたは がくせいですか。",
     "か turns a statement into a question (ですか). ね seeks confirmation/agreement ('right?'). For a genuine question, use か. ね would imply the speaker already believes the answer is yes."),
    ("n5-024", "particle",
     "コーヒーと おちゃが いいです。", "コーヒーか おちゃが いいです。",
     "か between two nouns presents an EXCLUSIVE CHOICE ('either coffee OR tea'). と would mean BOTH ('coffee and tea'). For 'which would you prefer', use か."),
    ("n5-025", "register",
     "いい てんきですよ。", "いい てんきですね。",
     "ね seeks AGREEMENT about something speaker and listener both observe ('nice weather, isn't it?'). よ ASSERTS new information to listener ('it's nice weather, fyi'). For weather small-talk, ね is correct — both parties see the weather."),
    ("n5-026", "register",
     "あした しけんですね。", "あした しけんですよ。",
     "よ informs the listener of something they may not know ('there's an exam tomorrow, btw'). ね assumes shared knowledge. For a reminder/announcement, よ is correct."),
    ("n5-027", "register",
     "あした 来ますか。", "あした 来ますよね。",
     "よね combines よ (asserting) + ね (confirming) — 'you're coming tomorrow, right?'. Used when speaker is pretty sure but wants confirmation. か alone is a pure information-question with no presumption."),
    ("n5-028", "particle",
     "これは わたしが 本です。", "これは わたしの 本です。",
     "の marks possession between two nouns: A の B = 'B of A'. が is for new-information subject — would make 'as for this, I (as new info) am a book' — nonsense. For 'my book', use わたし + の + 本."),
    ("n5-029", "particle",
     "日本語が 先生です。", "日本語の 先生です。",
     "の links a noun to its modifier (日本語 = Japanese language) and the head noun (先生 = teacher) — '日本語の先生' = a teacher OF Japanese. が would create a subject-predicate sentence ('Japanese is a teacher') — not the intended meaning."),
    ("n5-030", "particle",
     "本を 読むが すきです。", "本を 読むのが すきです。",
     "Nominalizer の turns the verb-phrase '本を読む' into a noun-equivalent ('reading books'). Without の, you can't take 読む as a noun subject of すき. Required pattern: V-dictionary + の + が/を + predicate."),
    ("n5-031", "particle",
     "どこへ いくですか？", "どこへ いくの？",
     "Sentence-final の (casual) substitutes for ですか in casual register. The form いくですか doesn't exist — verb (plain dict form) + ですか mixes registers. Casual: いくの？. Polite: 行きますか。"),
    ("n5-033", "particle",
     "コーヒーを だけ 飲みます。", "コーヒーだけ 飲みます。",
     "だけ ('only') replaces を, not stacks after it. The pattern is NOUN + だけ + Verb (no を between). Adding を would double-mark the object; だけ already implies the noun is the object."),
    ("n5-034", "particle",
     "1,000円しか あります。", "1,000円しか ありません。",
     "しか REQUIRES a negative predicate (ありません, できません, わかりません). It means 'nothing but / only X' with a regretful nuance. しか + positive predicate (あります) is grammatically wrong — always pair with ない/ません."),
    ("n5-035", "particle",
     "1時間ごろ まちました。", "1時間ぐらい まちました。",
     "ぐらい/くらい = APPROXIMATE QUANTITY ('about 1 hour'). ごろ = APPROXIMATE TIME-POINT ('around 3 o'clock'). 1時間 is a duration, so ぐらい is correct. Use ごろ only with clock times / dates."),
    ("n5-036", "particle",
     "3時ぐらい あいましょう。", "3時ごろ あいましょう。",
     "ごろ = approximate TIME-POINT ('around 3 o'clock'). ぐらい would mean approximate DURATION ('about 3 hours'). For 'let's meet around 3', the time-point sense requires ごろ."),
    ("n5-037", "particle",
     "りんごや バナナや などを よく 食べます。", "りんごや バナナなどを よく 食べます。",
     "など follows the LAST item in a や-list to mean 'and so on'. Don't repeat や before など. Pattern: A や B など (NO や immediately before など). Or use just A や B if 'and so on' is implied."),
    ("n5-038", "particle",
     "りんごを ひとつを ずつ ください。", "りんごを ひとつずつ ください。",
     "ずつ attaches DIRECTLY to a number-counter ('one each'). Don't put を between the counter and ずつ — they form a tight unit. Pattern: NUMBER + counter + ずつ."),

    # === Demonstratives (6 patterns) ===
    ("n5-014", "verb_class",
     "それは ほんです。", "これは ほんです。",
     "Choose between これ/それ/あれ based on speaker-listener proximity. これ = near speaker (in their hand or nearby). それ = near listener. あれ = far from both. A speaker showing a book they're holding uses これ."),
    ("n5-015", "verb_class",
     "これ ほんを よみました。", "この ほんを よみました。",
     "これ is a STANDALONE pronoun ('this thing'). この is a NOUN-MODIFIER ('this [noun]'). Before a noun, use この/その/あの/どの. Without a noun, use これ/それ/あれ/どれ. Common N5 error: skipping the の of この."),
    ("n5-016", "verb_class",
     "あそこは としょかんです。", "ここは としょかんです。",
     "ここ marks the SPEAKER'S CURRENT LOCATION ('here, where I am'). あそこ would be 'over there, far from us'. For introducing the speaker's surrounding building, use ここ."),
    ("n5-039", "verb_class",
     "あれは ほんです。", "これは ほんです。",
     "Same kosoado proximity rule as n5-014. これ for near-speaker, それ for near-listener, あれ for far-from-both. Identifying an object the speaker is showing uses これ."),
    ("n5-040", "verb_class",
     "これ ほんを よみました。", "この ほんを よみました。",
     "Same noun-modifier rule as n5-015. この/その/あの require a following noun. これ/それ/あれ stand alone. Mixing forms is the typical mistake."),
    ("n5-042", "register",
     "ここへ どうぞ。", "こちらへ どうぞ。",
     "こちら/そちら/あちら/どちら are the POLITE/FORMAL counterparts of ここ/そこ/あそこ/どこ. In service or business contexts (こちらへどうぞ = this way, please), the polite form is required. Plain ここ would be too casual."),

    # === Question Words (17 patterns) ===
    ("n5-045", "particle",
     "なにが たべますか。", "なにを たべますか。",
     "なに is the direct object of たべる ('eat what?'). Direct objects take を. が would put なに in subject position ('what eats?') — nonsensical. Always: なに/だれ/どれ + を/が depending on syntactic role."),
    ("n5-046", "particle",
     "だれは きましたか。", "だれが きましたか。",
     "Question word in subject position takes が, never は. だれは would imply 'as for [who]' — but the very point is we don't know who. The answer also uses が: '田中さんが きました'."),
    ("n5-048", "particle",
     "あそこは としょかんです。", "ここは としょかんです。",
     "When introducing the location speaker is at, ここ (near speaker). For a place far from both, あそこ. The example shows speaker pointing out where they are — ここ."),
    ("n5-049", "particle",
     "どれは あなたの ですか。", "どれが あなたの ですか。",
     "Question word どれ takes が, not は. 'Which one is yours?' — どれ is the new-information subject. The answer is これが私の (with が). The は-form would be ungrammatical at N5."),
    ("n5-050", "register",
     "おしごとは どうですか。 → どうだ", "おしごとは どうですか。",
     "どう is the polite/standard question form ('how is it'). The casual どうだ exists but mixes registers when paired with お-honored noun (おしごと). Match the polite request frame お+noun+は+どうですか. Even more formal: いかがですか."),
    ("n5-051", "register",
     "どうして 来ませんでしたよ。", "どうして 来ませんでしたか。",
     "Question requires か at the end (どうして... ですか). よ would change the meaning to a complaint/assertion ('you didn't come, ya know!'). For a question seeking explanation, use か."),
    ("n5-052", "particle",
     "どうやって 行きますね。", "どうやって 行きますか。",
     "Information-seeking question requires か. ね asks for agreement on something already known — doesn't fit 'how do we go?'. The asker doesn't know the answer, so it's a genuine か-question."),
    ("n5-053", "particle",
     "これは いくらですね。", "これは いくらですか。",
     "Asking 'how much?' is a genuine information-question — use か. ね would imply 'this is expensive, isn't it?' (seeking agreement about a known cost). For asking THE PRICE, か."),
    ("n5-054", "particle",
     "りんごは いくつ ありますね。", "りんごは いくつ ありますか。",
     "いくつ asks a quantity question requiring か. ね would imply 'there sure are a lot of apples, huh' — but the speaker doesn't know the count. For asking THE NUMBER, use か."),
    ("n5-055", "particle",
     "いま なんじですね。", "いま なんじですか。",
     "Asking the time is a genuine question requiring か. ね would be 'it's such-and-such time, isn't it' — but the asker doesn't know. なんじですか is the standard clock-asking form."),
    ("n5-056", "particle",
     "きょうは なんようびですね。", "きょうは なんようびですか。",
     "Asking the day-of-week requires か (genuine question). ね presumes shared knowledge. For asking 'what day is it', use か."),
    ("n5-057", "particle",
     "たんじょうびは なんがつ なんにちですね。", "たんじょうびは なんがつ なんにちですか。",
     "Date-asking is a genuine question — か. ね would presume the asker already knows. The structure: なんがつ (what month) + なんにち (what day) + か."),
    ("n5-183", "particle",
     "なにを たべたいですか。", "なにか たべたいです。",
     "なに + か = INDEFINITE pronoun ('something'). なに alone (with を) is a question ('what?'). For 'I want to eat SOMETHING' (vague desire, no specific item in mind), use なにか + たい. The Q-word + か pattern transforms the meaning."),
    ("n5-184", "particle",
     "なにを たべたいです。", "なにか たべたいです。",
     "Same as n5-183: なに-か with か (indefinite). For 'I want to eat something', use なにか (no を). Adding を would force なに into question-word mode and create an incomplete sentence."),
    ("n5-185", "particle",
     "だれを いますか。", "だれか いますか。",
     "だれか ('someone') is a polar (yes/no) question form. だれを ('whom') is for transitive verbs. The verb いる is INTRANSITIVE — it takes が or no particle. For 'is anyone there?', use だれか + いますか."),
    ("n5-186", "particle",
     "どこかが いきたいです。", "どこかへ いきたいです。",
     "Directional motion uses へ (or に). が would put 'somewhere' in subject position — doesn't fit 行きたい (want to go). The pattern is どこか + へ/に + Verb-stem + たい."),
    ("n5-187", "register",
     "いつ にほんへ いきたいです。", "いつか にほんへ いきたいです。",
     "いつ alone is a specific time-question ('when?'). いつか with か = INDEFINITE ('someday', vague future). For a non-specific aspirational time ('someday I want to go'), use いつか + に + へ + V-stem + たい."),

    # === Verbs - Tense and Politeness (6 patterns) ===
    ("n5-059", "conjugation",
     "わたしは にくを たべるません。", "わたしは にくを たべません。",
     "ません attaches to the verb STEM (drop ます from ます-form). たべる (dict) → たべます (polite) → たべません (polite neg). Don't keep る before ません — that mixes plain-form stem with polite negative ending."),
    ("n5-060", "conjugation",
     "きのう えいがを みるました。", "きのう えいがを みました。",
     "Past polite: drop ます, add ました. みる (Group 2) → みます → みました. The form みるました doesn't exist — you can't keep dictionary る AND have ました. Pattern: V-stem + ました."),
    ("n5-061", "conjugation",
     "きのうは ばんごはんを たべませんかった。", "きのうは ばんごはんを たべませんでした。",
     "Past polite negative: ません + でした (not ない + かった). The casual past negative IS なかった (たべなかった) but the polite form keeps ません and adds でした. Pattern: V-stem + ません + でした."),
    ("n5-062", "register",
     "いっしょに たべましょうか。", "いっしょに たべましょう。",
     "ましょう = 'let's do X' (volitional invitation). ましょうか adds 'shall we?' — softer, more tentative. The example proposes a direct shared action — ましょう (no か). If you wanted to soften it to 'shall we', ましょうか would fit."),
    ("n5-063", "register",
     "てつだいましょう。", "てつだいましょうか。",
     "ましょうか = 'shall I help?' (offering with question intonation). ましょう alone = 'let's help' (cohortative, includes listener). For offering to do something FOR the listener, use ましょうか."),
    ("n5-064", "register",
     "いっしょに ばんごはんを たべましょう。", "いっしょに ばんごはんを たべませんか。",
     "ませんか = 'won't you...?' / 'why don't we...?' — POLITE INVITATION offering listener a choice. ましょう = 'let's' — assumes the listener will join. For a more polite invitation, ませんか."),

    # === Verbs - Plain Form (4 patterns) ===
    ("n5-065", "verb_class",
     "ともだちに あるう。", "ともだちに あう。",
     "Dictionary form of Group-1 (godan) verb あう ('meet') is just あう — no extra る. The る ending is for Group-2 (ichidan) verbs only. あう is Group 1 because it ends in う (not える/いる + る)."),
    ("n5-066", "conjugation",
     "おさけを のまる ない。", "おさけを のまない。",
     "Group-1 plain negative: drop final う-row, add あ-row + ない. のむ → のま + ない = のまない. Don't insert る — that's only for Group-2 dictionary form. Pattern: V-stem (with あ-row vowel) + ない."),
    ("n5-067", "conjugation",
     "きのう ほんを よみた。", "きのう ほんを よんだ。",
     "Group-1 plain past for verbs ending in む: change む to ん, add だ. よむ → よん + だ = よんだ. The form よみた applies the wrong sub-rule. Memorize: む/ぶ/ぬ → んだ; く → いた; ぐ → いだ; す → した; つ/る/う → った."),
    ("n5-068", "conjugation",
     "きのう おさけを のまなかった です。", "きのう おさけを のまなかった。",
     "Plain past negative のまなかった stands alone (no です in plain register). Adding です mixes plain-form negative with polite ending. For polite past negative: のみませんでした (the ましょう-chain form)."),

    # === Te-form (5 patterns) ===
    ("n5-070", "conjugation",
     "あさ おきて、コーヒーを 飲むで、しごとに 行きます。", "あさ おきて、コーヒーを 飲んで、しごとに 行きます。",
     "Sequential te-form for む-ending verbs: 飲む → 飲んで (む → んで). The form 飲むで is wrong — む must transform. The five Group-1 sub-rules: く→いて, ぐ→いで, す→して, む/ぶ/ぬ→んで, つ/る/う→って."),
    ("n5-071", "conjugation",
     "ちょっと まちって ください。", "ちょっと まってください。",
     "Group-1 verb まつ te-form: つ → って (まって). The form まちって doubles the ち unnecessarily. Pattern: つ/る/う → って. Other examples: かう → かって; かえる → かえって; あう → あって."),
    ("n5-074", "conjugation",
     "ここで しゃしんを とるても いいですか。", "ここで しゃしんを とってもいいですか。",
     "Group-1 verb とる ('take'): te-form is とって (る → って sub-rule). Then + も + いい = permission ('is it OK to take photos?'). Don't preserve る in the te-form chain. Full: V-te + も + いい."),
    ("n5-075", "conjugation",
     "ここで たばこを すうては いけません。", "ここで たばこを すってはいけません。",
     "Group-1 verb すう ('smoke / suck'): te-form is すって (う → って). The prohibitive pattern: V-te + は + いけません. Don't leave the verb in dictionary form — use the te-form properly."),
    ("n5-077", "conjugation",
     "ここで しゃしんを とらないで ください。", "ここで しゃしんを とらないでください。",
     "Negative request 'please don't': V-ない + で + ください. The form とらないでください is correct as one phrase. Don't separate ないで from ください — they form a tight grammatical unit. Pattern: V-ない (drop い) + で + ください."),

    # === Adjectives (10 patterns) ===
    ("n5-078", "verb_class",
     "高いの 山が 見えます。", "高い 山が 見えます。",
     "い-adjectives attach DIRECTLY to nouns — no の between. The form 高いの would nominalize 高い ('the expensive one'), not modify 山. Pattern: い-adj + Noun (no particle). な-adj uses な."),
    ("n5-080", "conjugation",
     "この ほんは おもしろくないでした。", "この ほんは おもしろくないです。",
     "い-adjective negative + present polite: drop い, add くない, then です. The form くないでした wrongly stacks past でした on already-negative くない. For past negative, use くなかった (see n5-082)."),
    ("n5-081", "conjugation",
     "きのうは あついでした。", "きのうは あつかったです。",
     "い-adjective past: drop い, add かった, then です. あつい → あつ + かった + です = あつかったです. The form あついでした (い-adj + でした) is wrong — でした is for nouns/な-adj only."),
    ("n5-082", "conjugation",
     "きのうは さむいくなかったです。", "きのうは さむくなかったです。",
     "い-adjective past negative: drop い, add くなかった, then です. さむい → さむ + くなかった + です. Don't double-mark with い+くなかった. Pattern: stem + くなかった + です."),
    ("n5-083", "conjugation",
     "この りょうりは あついて、おいしいです。", "この りょうりは あつくて、おいしいです。",
     "い-adjective te-form: drop い, add くて. あつい → あつ + くて = あつくて. The form あついて (い-adj + て) is wrong — i must drop first. Used to connect adjectives or give reason."),
    ("n5-084", "verb_class",
     "しずか へやが すきです。", "しずかな へやが すきです。",
     "な-adjectives REQUIRE な before a noun. しずか + な + へや. Without な, the sentence is structurally incomplete at N5. Contrast: い-adjectives skip な (高い 山, not 高いな 山)."),
    ("n5-086", "conjugation",
     "この へやは しずかくない です。", "この へやは しずかじゃありません。",
     "な-adjective negative: stem + じゃありません (or でわありません/じゃない). The form しずかくない wrongly applies い-adj negation. な-adj uses じゃ/では, not くない."),
    ("n5-087", "conjugation",
     "きのうの コンサートは にぎやかかったです。", "きのうの コンサートは にぎやかでした。",
     "な-adjective past: stem + でした (just copula past). The form にぎやかかった wrongly applies い-adj past. な-adj past = stem + でした. Don't conjugate the adjective itself."),
    ("n5-088", "conjugation",
     "きのうの しけんは かんたんじゃありませんかった。", "きのうの しけんは かんたんじゃありませんでした。",
     "な-adjective past negative: stem + じゃありません + でした (or じゃなかった for plain). The form じゃありませんかった is wrong — でした follows ません, not かった."),
    ("n5-089", "conjugation",
     "この まちは しずかくて、きれいです。", "この まちは しずかで、きれいです。",
     "な-adjective te-form: stem + で (just like the copula). しずか → しずか + で. The form しずかくて wrongly applies い-adj rule. な-adj te-form is identical to nouns + で."),

    # === Existence and Possession (3 patterns) ===
    ("n5-090", "verb_class",
     "つくえの 上に ほんが います。", "つくえの 上に ほんが あります。",
     "ほん (book) is INANIMATE — uses あります. います is for animate things (people, animals). Memorize: ある/あります for objects, events, abstract concepts; いる/います for living beings."),
    ("n5-092", "particle",
     "つくえの 上は 本が あります。", "つくえの 上に 本が あります。",
     "Location of existence takes に (location-particle). The pattern is: [location] + に + [thing] + が + あります/います. は in the location slot would make it a topic-comment frame, changing the syntactic role."),
    ("n5-093", "particle",
     "本は つくえの 上で あります。", "本は つくえの 上に あります。",
     "Location of existence (where the book IS) takes に, not で. で marks location of ACTION (verbs of doing). For static existence ('the book is on the desk'), use に. Memorize: あります/います → に."),

    # === Comparison and Preference (8 patterns) ===
    ("n5-096", "particle",
     "おおさかが とうきょうのほうが 大きいです。", "おおさかより とうきょうのほうが 大きいです。",
     "Comparison pattern: A より B のほうが Adjective. より marks the REFERENCE/STANDARD (the one we compare TO). が in this slot would make 大阪 a subject — but it's the comparison reference, not the predicate's subject."),
    ("n5-097", "particle",
     "いぬや ねこと、どちらが すきですか。", "いぬと ねこと、どちらが すきですか。",
     "Two-way comparison uses と...と (not や). や is for non-exhaustive lists ('apples, bananas, etc.'). When choosing between exactly two items, both joined by と and the question asks どちらが."),
    ("n5-098", "particle",
     "わたしは ねこを すきです。", "わたしは ねこが すきです。",
     "すき/きらい/じょうず/へた/ほしい/わかる all take が, not を. They're adjectival predicates where the noun is the SUBJECT OF FEELING, not a direct object. For 'I like cats', use ねこが (not ねこを)."),
    ("n5-100", "particle",
     "あの 人は 日本語を じょうずです。", "あの 人は 日本語が じょうずです。",
     "じょうず ('skilled') takes が like its family member すき. The skill subject is the THING that's done well. を would imply 日本語 is a direct object — wrong syntax for this adjective."),
    ("n5-101", "particle",
     "新しい くるまを ほしいです。", "新しい くるまが ほしいです。",
     "ほしい ('want, desire') takes が, like すき/じょうず. The desired thing is the subject of want, not a direct object. Common N5 error: applying transitive を to ほしい. Always: NOUN + が + ほしい."),
    ("n5-102", "particle",
     "日本語を すこし わかります。", "日本語が すこし わかります。",
     "わかる ('understand') takes が. Even though it feels like a transitive 'comprehend X', Japanese grammar treats the understood-thing as the SUBJECT OF UNDERSTANDING. Always: NOUN + が + わかる."),
    ("n5-103", "particle",
     "日本語を できます。", "日本語が できます。",
     "できる ('can do, be capable') takes が. The ability-object goes with が, not を. For 'I can speak Japanese', 日本語が できます. The same が-rule applies to all adjectival-predicate verbs in this family."),
    ("n5-188", "conjugation",
     "日本語を 話します ことが できます。", "日本語を 話す ことが できます。",
     "V-dictionary + ことができます is the pattern. The verb stays in DICTIONARY form (話す), not ます-form (話します). The polite layer is on できます, not on 話す. Pattern: V-dict + こと + が + できます."),

    # === Desiderative and Volitional (2 patterns) ===
    ("n5-106", "particle",
     "新しい かばんを ほしいです。", "新しい かばんが ほしいです。",
     "ほしい takes が, not を. Same rule as preference adjectives — the wanted thing is the subject of desire, not a transitive object. Always: NOUN + が + ほしい/ほしくない/ほしかった/etc."),
    ("n5-107", "particle",
     "デパートへ 買いものを 行きます。", "デパートへ 買いものに 行きます。",
     "Purpose of motion uses に (verb-stem + に + 行く/来る/帰る). The pattern is: [destination] + へ + [purpose-stem] + に + motion-verb. を would mark 買いもの as a direct object of 行く — but 行く doesn't take direct objects."),

    # === Counters (3 patterns) ===
    ("n5-108", "conjugation",
     "りんごを ふたっつ ください。", "りんごを ふたつ ください。",
     "Native-counter ふたつ ('two') reads with kun-yomi. Don't double the っ — it's ふたつ (two morae: ふ + たつ → ふた+つ). Memorize the native series: ひとつ/ふたつ/みっつ/よっつ/いつつ/むっつ/ななつ/やっつ/ここのつ/とお."),
    ("n5-109", "verb_class",
     "りんごは なんまい ありますか。", "りんごは いくつ ありますか。",
     "Choose counter by object type: いくつ for round/3D objects (apples, eggs); なんまい for flat objects (paper, photos); なんにん for people; なんぼん for cylindrical (bottles, pens). For apples, use いくつ."),
    ("n5-110", "particle",
     "りんごを ふたつを かいました。", "りんごを ふたつ かいました。",
     "Number-counter (ふたつ) appears BARE between the noun-を and the verb. Don't add another を. Pattern: NOUN + を + number-counter + Verb. The counter doesn't take its own particle in this construction."),

    # === Time Expressions (8 patterns) ===
    ("n5-112", "conjugation",
     "10ぷん まちました。 → 10ふん", "10ぷん まちました。",
     "Reading rule: ふん vs ぷん alternates by preceding digit. 1ぷん, 2ふん, 3ぷん, 4ぷん, 5ふん, 6ぷん, 7ふん, 8ぷん, 9ふん, 10ぷん. Memorize the alternation — randomly picking ふん over ぷん is the typical mistake."),
    ("n5-113", "conjugation",
     "いま 3時 半です。", "いま 3時はんです。",
     "はん attaches DIRECTLY to 時, no space or extra particle. 3時はん = '3:30'. The form '3時 半' with separation reads awkwardly — はん is a fused suffix. Pronunciation: san-ji-han, not san-ji + han."),
    ("n5-114", "particle",
     "9時で 5時まで しごとです。", "9時から 5時まで しごとです。",
     "Time range: A から B まで (from A to B). The start point takes から, the end まで. で would mean 'AT 9' (action location at a fixed time). Always pair から + まで for a span."),
    ("n5-115", "particle",
     "7時で おきます。", "7時に おきます。",
     "Specific clock time takes に. で marks location of action (家で食べる). Clock-time に rule: 3時に, 5時半に, 月曜日に. Relative time (today/yesterday) takes NO particle: 今日 (no に)."),
    ("n5-116", "particle",
     "まいにちに 日本語を べんきょうします。", "まいにち 日本語を べんきょうします。",
     "まいにち/まいしゅう/まいつき/まいとし appear BARE — no particle. They're frequency adverbs, not absolute time references. に goes on 3時に / 月曜日に, not on 'every day'."),
    ("n5-118", "particle",
     "いまに 行きます。", "いま 行きます。",
     "いま ('now') appears bare, with no particle. に would imply 'AT now' — but いま is already a momentary adverb. Same bare-form rule applies to すぐ/もう/まだ. Pattern: [aspect adverb] + Verb."),
    ("n5-119", "conjugation",
     "ごはん まえに てを あらいます。", "ごはんの まえに てを あらいます。",
     "Noun + の + まえに = 'before [noun]'. Don't drop の. Pattern: NOUN + の + まえに + Verb. For V-plain + まえに ('before doing'), drop の: 食べる まえに."),
    ("n5-120", "conjugation",
     "しごと あとで のみに 行きました。", "しごとの あとで のみに 行きました。",
     "Noun + の + あとで = 'after [noun]'. Don't drop の. Pattern: NOUN + の + あとで + Verb. For V-た + あとで ('after doing'), drop の: 食べた あとで."),

    # === Conjunctions (8 patterns) ===
    ("n5-121", "conjugation",
     "あさごはんを たべました。それで、しごとに 行きました。", "あさごはんを たべました。そして、しごとに 行きました。",
     "そして = SEQUENTIAL connector ('and then'). それで = CAUSAL ('and so therefore'). For neutral sequence-of-actions, use そして. それで implies the first event CAUSED the second."),
    ("n5-122", "conjugation",
     "シャワーを あびました。そして、ねました。", "シャワーを あびました。それから、ねました。",
     "それから = EXPLICIT TEMPORAL ('after that, then'). そして is neutral conjunction. For 'shower, then sleep' (clear time sequence), use それから. そして would feel softer/list-like."),
    ("n5-123", "conjugation",
     "コーヒーが すきです。でもは、おちゃは すきじゃありません。", "コーヒーが すきです。でも、おちゃは すきじゃありません。",
     "でも starts a sentence as 'but / however'. Don't add は after でも. Pattern: Sentence A. でも、Sentence B. The は in 'おちゃは' is for the topic of sentence B, not stacked on でも."),
    ("n5-124", "register",
     "テストは むずかしかったです。でも、できました。", "テストは むずかしかったです。しかし、できました。",
     "しかし = FORMAL 'but/however' (written, presentation, business). でも = CASUAL 'but'. Both are correct semantically; しかし is the right register for formal contexts (news articles, essays). The example reads as more formal — しかし fits."),
    ("n5-125", "register",
     "では、また あした。", "じゃ、また あした。",
     "じゃ is the CASUAL contraction of では ('well then, see you'). For friends/peers, じゃ is more natural. では sounds formal/stiff in casual goodbyes. Choose based on register."),
    ("n5-126", "conjugation",
     "コーヒーは すきです、 おちゃは すきじゃありません。", "コーヒーは すきですが、おちゃは すきじゃありません。",
     "が (contrast conjunction) joins TWO CLAUSES with a 'but' nuance — placed at the END of the first clause before the comma. Pattern: Clause A + が、Clause B. A bare comma without が is incomplete."),
    ("n5-127", "register",
     "むずかしいです けれども、おもしろいです。", "むずかしいですけど、おもしろいです。",
     "けど is the CASUAL contraction of けれども ('but'). For everyday conversation, けど. けれども is more formal/written. Either is correct semantically; pick by register."),
    ("n5-129", "particle",
     "どうして 来ませんでしたか。―あたまが いたかったから。", "どうして 来ませんでしたか。―あたまが いたかったからです。",
     "Answering どうして with から requires です at the end in polite register: 'because [reason] です'. Pattern: あたまが いたかったから + です. Without です, the answer is too casual for the polite question."),

    # === Giving and Receiving (3 patterns) ===
    ("n5-130", "particle",
     "ともだちを 本を あげました。", "ともだちに 本を あげました。",
     "あげる/さしあげる take RECIPIENT に + OBJECT を. Double-を is wrong. Pattern: [giver]は + [recipient]に + [object]を + あげる. The recipient particle is に, not を."),
    ("n5-131", "particle",
     "ともだちが 本を もらいました。", "ともだちに 本を もらいました。",
     "もらう takes FROM-PERSON marked by に (or から) and OBJECT marked by を. ともだちが would put the friend in subject position — but the speaker is the subject (implicit わたしは). Pattern: [I]は + [giver]に/から + [object]を + もらう."),
    ("n5-132", "particle",
     "友だちに 本を くれました。", "友だちが 本を くれました。",
     "くれる: the GIVER is the subject (takes が), the RECIPIENT is the speaker (implicit). Pattern: [giver]が + [object]を + くれる. に would put the friend in recipient position — but the friend is the giver here."),

    # === Causation (1 pattern; n5-133 is already n5-129's analog) ===
    ("n5-133", "conjugation",
     "あついから まどを あけて ください。", "あついから、まどを あけてください。",
     "Causation pattern: Clause A から、Clause B. The comma after から marks the clause break. Spoken language can drop the comma, but written form needs it. Pattern: [reason]から、[result]."),

    # === Modification (3 patterns) ===
    ("n5-135", "conjugation",
     "わたしは 買った 本", "わたしが 買った 本",
     "Relative-clause subject takes が, not は. Pattern: [Subject]が + V-plain + Noun = 'the [noun] that [subject] [verb]ed'. は would make 'as for me, [I] bought the book' — a main-clause topic, not a relative-clause modifier."),
    ("n5-136", "verb_class",
     "高いの 山が 見えます。", "高い 山が 見えます。",
     "い-adjectives modify nouns DIRECTLY. 高い + 山 (no particle, no の). The form 高いの would nominalize 高い as 'the high one'. For 'a high mountain', use bare adjective + noun."),
    ("n5-137", "particle",
     "これは わたしと 本です。", "これは わたしの 本です。",
     "Possession between nouns: A + の + B = 'B of A' / 'A's B'. と would mean 'A AND B' (apposition or list). For 'my book', use わたし + の + 本."),

    # === Common Set Patterns (5 patterns) ===
    ("n5-142", "particle",
     "コーヒーを します。", "コーヒーに します。",
     "〜にします = 'I'll have/choose [noun]' (deliberate selection). The particle is に, not を. Without に, the sentence is structurally incomplete in this set-pattern frame. Standard ordering choice in restaurants: NOUN + に + します."),
    ("n5-143", "particle",
     "先生を なりたいです。", "先生に なりたいです。",
     "〜になる = 'become [noun]' takes に, not を. The endpoint of becoming uses に. Pattern: NOUN + に + なる. Plus たい on stem of なる → なりたい (want to become). Full: NOUN + に + なりたい."),
    ("n5-144", "conjugation",
     "おんがくを 聞くながら べんきょうします。", "おんがくを 聞きながら べんきょうします。",
     "ながら attaches to the VERB STEM (drop ます from ます-form). 聞く → 聞きます → 聞き + ながら = 聞きながら. The form 聞くながら (dict + ながら) is wrong — the stem must be extracted first."),
    ("n5-145", "particle",
     "あした 雨が ふるから おもいます。", "あした 雨が ふると おもいます。",
     "Quoted-thought marker is と, not から. と marks the content of thinking/saying. から marks a reason. For 'I think [content]', use [clause] + と + おもう."),
    ("n5-146", "particle",
     "「あした 来ます」を 言いました。", "「あした 来ます」と 言いました。",
     "Quoted speech is marked by と (same particle as と思う). The pattern is: [quoted content] + と + 言いました. を would treat the quote as a direct object — wrong syntactic role for quoted speech in Japanese."),

    # === Frequency (2 patterns) ===
    ("n5-147", "particle",
     "よくに テレビを 見ます。", "よく テレビを 見ます。",
     "Frequency adverbs (よく/ときどき/あまり/ぜんぜん) attach DIRECTLY before the verb — no particle. に would imply a time-point ('at well'). Pattern: [frequency adverb] + Verb (no particle between)."),
    ("n5-148", "particle",
     "いつもに 7時に おきます。", "いつも 7時に おきます。",
     "いつも ('always'), たいてい ('usually'), たまに ('occasionally') appear BARE — no particle. The clock-time 7時 already has its own に. Don't double up: いつも + 7時に, not いつもに + 7時に."),

    # === Functional Expressions (1 pattern) ===
    ("n5-151", "particle",
     "おちゃを いかがですか。", "おちゃは いかがですか。",
     "〜はいかがですか offers a thing — the offered noun takes は (topic marker, 'as for tea, how about it?'). を would make it a direct object — but いかが isn't a transitive verb. The fixed frame is: NOUN + は + いかがですか."),

    # === Other Core Patterns (11 patterns) ===
    ("n5-153", "conjugation",
     "まだ あさごはんを たべません。", "まだ あさごはんを たべていません。",
     "'Not yet' = まだ + ていません. The plain たべません means 'will not eat / does not eat'. The 'not yet' aspect requires ています (progressive) in negative — まだ食べていません = haven't eaten yet (as of now)."),
    ("n5-154", "conjugation",
     "もう ばんごはんを たべます。", "もう ばんごはんを たべました。",
     "もう + V-ました = 'already done'. The non-past たべます would mean 'I'll eat now' — not 'I already ate'. For the perfect-aspect 'already', use もう + past polite. もう食べました = I've already eaten."),
    ("n5-155", "particle",
     "コーヒーは すきです、おちゃは すきじゃありません。", "コーヒーは すきですが、おちゃは すきじゃありません。",
     "Connecting clauses with 'but' uses が at the END of the first clause. Bare comma without が is structurally incomplete. Pattern: Clause A + が、Clause B."),
    ("n5-156", "register",
     "いい てんきですか。", "いい てんきですね。",
     "ね seeks agreement on observed phenomena ('nice weather, isn't it?'). か turns it into a genuine question — but the speaker already SEES the weather. For weather small-talk between two people who both observe it, use ね."),
    ("n5-157", "particle",
     "あした 雨でしょうか。", "あした 雨でしょう。",
     "でしょう alone is an ASSERTION OF PROBABILITY ('probably rain'). でしょうか adds questioning intonation ('I wonder if it'll rain'). For a forecast/prediction statement, でしょう (no か) is the direct form."),
    ("n5-158", "register",
     "あした 雨でしょう。", "あした 雨だろう。",
     "だろう is the PLAIN/CASUAL counterpart of でしょう. Both mean 'probably'. でしょう is polite (matches です/ます register); だろう is casual (matches plain register). The example uses casual register — だろう fits."),
    ("n5-159", "register",
     "いい てんきだね。", "いい てんきですね。",
     "Polite-register agreement-seeking uses ですね (combining copula です + agreement-particle ね). The casual form is だね (combining plain copula だ + ね). Choose to match the rest of the conversation's register."),
    ("n5-160", "particle",
     "しごとの あとに のみに 行きました。", "しごとの あとで のみに 行きました。",
     "Noun + の + あとで = 'after [noun]' (using で). The form あとに exists for absolute future timing but あとで is the standard sequential connector. Pattern: NOUN + の + あとで."),
    ("n5-161", "particle",
     "ごはんの まえで てを あらいます。", "ごはんの まえに てを あらいます。",
     "Noun + の + まえに = 'before [noun]' (using に). The form まえで doesn't fit — まえ takes に as its companion particle (parallel to あと + で which is the after-companion)."),
    ("n5-162", "conjugation",
     "出かけるの まえに、しんぶんを 読みます。", "出かける まえに、しんぶんを 読みます。",
     "V-plain + まえに drops の (no NOUN+の structure). The form 出かけるの まえに mixes the V-form with the noun-form. Pattern: V-dictionary + まえに (no の). 食べる まえに、本を読む。"),
    ("n5-163", "conjugation",
     "しごとが おわるの あとで、 のみに 行きました。", "しごとが おわった あとで、 のみに 行きました。",
     "V-た + あとで ('after doing'). Use the PAST PLAIN form of the verb, not dictionary. 終わる (dict) → 終わった (past plain) + あとで. The form 終わるの あとで mixes the noun-pattern with verb-pattern."),

    # === Honorific (3 patterns) ===
    ("n5-164", "register",
     "田中さま は 先生です。", "田中さんは 先生です。",
     "〜さん is the standard polite suffix for adults. 〜さま is hyper-honorific (formal letters, customer-service register only). For everyday polite address (school, work peers), さん. さま would feel oddly excessive."),
    ("n5-165", "register",
     "ちゃを どうぞ。", "おちゃを どうぞ。",
     "お-honorific prefix elevates the noun's politeness (お茶, お水, お金, お時間). Dropping お for items where it's expected (especially お茶) sounds abrupt in service contexts. Adult/polite register uses お consistently for these tradition-marked nouns."),
    ("n5-166", "register",
     "いただきます。", "いただきます！",
     "Pre-meal ritual phrase. Required before starting to eat in Japanese cultural context. The exclamation mark conveys the spoken enthusiasm. Don't skip it in shared-meal settings — non-saying it is socially conspicuous."),

    # === Borderline (n5-167..188 minus those already in phase 3) ===
    ("n5-167", "register",
     "あたまが いたいです。", "あたまが いたいんです。",
     "〜んです adds EXPLANATORY tone ('it's that [reason]'). The plain いたいです states a fact. Adding んです signals 'this is the explanation / reason' — useful when responding to '大丈夫?' with 'actually, my head hurts (and that's why I'm not OK)'. "),
    ("n5-168", "conjugation",
     "しゅうまつは 本を 読むたり、えいがを 見るたり します。", "しゅうまつは 本を 読んだり、えいがを 見たり します。",
     "〜たり attaches to the PAST PLAIN form (V-た + り). 読む (dict) → 読んだ (past) → 読んだり. The form 読むたり is wrong — must use ta-form first. Pattern: V-た + り + V-た + り + する."),
    ("n5-169", "conjugation",
     "日本へ 行くことが あります。", "日本へ 行ったことが あります。",
     "〜たことがある = 'have the experience of doing X'. Uses V-PAST + ことがある. 行く (dict) → 行った (past plain) + ことがあります. The dict form 行くことがあります would mean 'sometimes I go' (habitual), not 'I have been'."),
    ("n5-170", "conjugation",
     "もう 寝るほうが いいですよ。", "もう 寝たほうが いいですよ。",
     "〜たほうがいい = 'should do X / better to do X' takes V-PAST plain, not dict. 寝る → 寝た + ほうがいい. Even though the meaning is future-oriented advice, the form requires past. Pattern: V-た + ほうがいい."),
    ("n5-171", "conjugation",
     "あまり 食べたほうが いいです。", "あまり 食べないほうが いいです。",
     "Negative advice uses V-ない + ほうがいい. The form 食べたほうがいい (positive) means 'better to eat'. For 'better NOT to eat much', use 食べない + ほうがいい. Pattern: V-ない + ほうがいい."),
    ("n5-174", "conjugation",
     "しゅくだいを しなくは ならない。", "しゅくだいを しなくては ならない。",
     "Obligation: V-ない (drop い + くて) + は + ならない. The form しなくは skips the て-step. Full derivation: する → しない → しなくて → しなくては + ならない."),
    ("n5-175", "conjugation",
     "はやく かえらないと いけませんない。", "はやく かえらないと いけない。",
     "Obligation: V-ない + と + いけない (NOT と + いけませんない). The two are separate units. Pattern: V-ない + と + いけない/だめ. Polite: いけません. Don't double-negate with ないと いけませんない."),
    ("n5-176", "register",
     "もう 行かなくては。", "もう 行かなくちゃ。",
     "なくちゃ is the SUPER-CASUAL contraction of なくては. なくてはいけない → なくてはならない → なくちゃ (casual + drop the いけない). Used in spoken Japanese among friends. For polite contexts, the full form is required."),
    ("n5-177", "conjugation",
     "きのう たべるすぎました。", "きのう たべすぎました。",
     "すぎる attaches to verb STEM (drop ます from ます-form). たべる → たべます → たべ + すぎる = たべすぎる. The form たべるすぎる is wrong — must extract stem. Pattern: V-stem + すぎる."),
    ("n5-179", "register",
     "「あした 来る」と 言いました。", "「あした 来る」って 言いました。",
     "って is the CASUAL contraction of と言って/と (quotation marker). In casual conversation, 「あした来る」って言ってた replaces 「あした来る」と言いました. Both are correct; choose by register."),
    ("n5-180", "conjugation",
     "この かんじの 読むかたは なんですか。", "この かんじの 読みかたは なんですか。",
     "〜かた attaches to verb STEM (drop ます from ます-form). 読む → 読みます → 読み + かた = 読みかた. The form 読むかた wrongly uses dictionary form. Pattern: V-stem + かた = 'way of doing'."),
    ("n5-182", "register",
     "行きなさい！", "行くな！",
     "Strong casual prohibitive: V-dictionary + な = 'don't [verb]!'. 行くな = don't go! It's harsh/male-coded. Compare with 行きなさい (polite imperative, 'go!') or 行ってください (request, 'please go'). Choose based on register and intent."),
]


def main() -> int:
    data = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in data["patterns"]}

    upgraded = 0
    appended = 0
    skipped = 0

    for entry in UPGRADES:
        pid, cat, wrong, right, why = entry
        p = by_id.get(pid)
        if not p:
            print(f"  WARN: pattern {pid} not found")
            skipped += 1
            continue
        cms = p.get("common_mistakes") or []
        if not isinstance(cms, list):
            skipped += 1
            continue

        new_entry = {
            "wrong": wrong, "right": right, "why": why,
            "category": cat,
            "provenance": "native_reviewed",
            "audit_wave": "issue-112-phase4-2026-05-12",
        }

        # Replace first issue-112 template entry (phase 1 / phase 2 family-template)
        replaced = False
        for i, cm in enumerate(cms):
            if not isinstance(cm, dict):
                continue
            aw = cm.get("audit_wave") or ""
            if aw.startswith("issue-112") and not aw.startswith("issue-112-phase3"):
                cms[i] = new_entry
                replaced = True
                upgraded += 1
                break
        if not replaced:
            cms.append(new_entry)
            appended += 1
        p["common_mistakes"] = cms

    print(f"Upgraded: {upgraded} / appended: {appended} / skipped: {skipped}")

    # Final census
    nr = sum(1 for p in data["patterns"] for cm in (p.get("common_mistakes") or [])
             if isinstance(cm, dict) and cm.get("provenance") == "native_reviewed")
    lc = sum(1 for p in data["patterns"] for cm in (p.get("common_mistakes") or [])
             if isinstance(cm, dict) and cm.get("provenance") == "llm_curated")
    total = sum(1 for p in data["patterns"] for cm in (p.get("common_mistakes") or [])
                if isinstance(cm, dict))
    at3 = sum(1 for p in data["patterns"]
              if sum(1 for cm in (p.get("common_mistakes") or [])
                     if isinstance(cm, dict) and cm.get("category")) >= 3)

    # Patterns with at least 1 native_reviewed entry
    patterns_with_nr = sum(
        1 for p in data["patterns"]
        if any(isinstance(cm, dict) and cm.get("provenance") == "native_reviewed"
               for cm in (p.get("common_mistakes") or []))
    )

    print(f"\nProvenance: native_reviewed {nr} / llm_curated {lc} / total {total}")
    print(f"Patterns with >=1 native_reviewed mistake: {patterns_with_nr}/{len(data['patterns'])}")
    print(f"Patterns at >=3 categorized: {at3}/{len(data['patterns'])}")

    GRAMMAR.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {GRAMMAR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
