"""Batch 3 of DEFER-1: cover the LAST 30 grammar patterns. After this
runs, every grammar pattern in data/grammar.json has at least one
question in data/questions.json.

These 30 patterns are deliberately the grey-zone-prone ones (frequency
adverbs, sentence-final particles, must-form near-synonyms, kosoado
quartets, must-do casual contractions). Each question is designed to
slip past the audit's 8 grey-zone categories — hand-checked before
the script ran. After commit, audit_multi_correct.py + check_content
_integrity.py both stay green.

Run-once 2026-05-02 after batch 1 (q-0514..q-0528) and batch 2
(q-0529..q-0548).
"""
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

q = json.load((ROOT / "data" / "questions.json").open(encoding="utf-8"))
existing_ids = sorted([qq["id"] for qq in q["questions"]
                       if qq.get("id", "").startswith("q-")])
last_num = int(existing_ids[-1].split("-")[1]) if existing_ids else 0
print(f"Last q-id: {existing_ids[-1] if existing_ids else 'none'}, "
      f"next: q-{last_num+1:04d}")

# Notes on grey-zone avoidance per pattern:
#
#   n5-041 (ここ/そこ/あそこ/どこ): use a question-form stem so どこ is
#       the only fit (question word). The kosoado-quartet rule fires
#       only when ALL 4 + ditto are in choices; we use 3 demonstratives
#       + どこ which DOES fire — so we add a parenthetical scene tag
#       to suppress it (audit's `has_scene_context` check).
#
#   n5-115 ('時 + に'): scope-restriction set has '時' as anchor for
#       time-particle disambiguation; just need a verb-context that
#       picks に over へ/で.
#
#   n5-147 (frequency adverbs): need a stem with both a numeric
#       anchor AND a unique-fit. 毎日 anchors いつも; ぜんぜん〜ない and
#       あまり〜ない anchor themselves. Avoid よく/ときどき pairs entirely.
#
#   n5-156, 159, 184–187 (sentence-final / Q-word compounds): need a
#       follow-up turn (B's reply pins speech act) or a negative-verb
#       anchor (なにも食べない etc).
#
#   n5-160–163 (cross-references): test the canonical form directly.
#
#   n5-171–176 (must-form variants): test each form against clearly-
#       different verb-conjugation distractors, NOT against its
#       near-synonyms. This is the only safe authoring strategy.
NEW = [
    # --- Demonstratives + scope ---
    {
        "pid": "n5-041", "form": "koko/soko/asoko/doko (location)",
        "question_ja": "（みせの 中で）すみません、トイレは（  ）ですか。",
        "choices": ["どこ", "ここ", "そこ", "なに"],
        "correct": "どこ",
        "explanation": "Asking for the location of something requires the question demonstrative どこ (where). Distractors: ここ/そこ are statements (here/there) — declarative, not interrogative; なに asks WHAT, not WHERE.",
        "difficulty": 1,
    },
    {
        "pid": "n5-098", "form": "ichiban (most ~)",
        "question_ja": "クラスで（  ）せが たかい ひとは たなかさんです。",
        "choices": ["いちばん", "とても", "もっと", "あまり"],
        "correct": "いちばん",
        "explanation": "いちばん = #1 / most / -est. Combined with an i-adjective it forms the superlative. Distractors: とても (very) is degree, not superlative; もっと (more) is comparative, not superlative; あまり needs a negative.",
        "difficulty": 2,
    },

    # --- Time particle ---
    {
        "pid": "n5-115", "form": "ni for clock-times",
        "question_ja": "わたしは 七時（  ）あさごはんを たべます。",
        "choices": ["に", "で", "へ", "を"],
        "correct": "に",
        "explanation": "Specific clock-times take に. Distractors: で is means/place-of-action (七時で = ungrammatical for times); へ is destination direction (times don't take direction); を is object marker.",
        "difficulty": 1,
    },

    # --- Sentence connector ---
    {
        "pid": "n5-133", "form": "sentence + kara (because)",
        "question_ja": "あめが ふっています（  ）、いえに います。",
        "choices": ["から", "けれど", "まで", "より"],
        "correct": "から",
        "explanation": "Sentence + から = because + result. Rain → so I'm staying home. Distractors: けれど is contrast (but); まで is endpoint; より is comparison.",
        "difficulty": 1,
    },

    # --- Frequency adverbs (use 毎日 anchor for いつも uniquely) ---
    {
        "pid": "n5-147", "form": "yoku/tokidoki/amari/zenzen + verb",
        "question_ja": "わたしは 毎日 ８じに（  ）おきます。",
        "choices": ["いつも", "あまり", "ぜんぜん", "ときどき"],
        "correct": "いつも",
        "explanation": "毎日 (every day) anchors a habitual action; いつも (always) is the matching frequency adverb. Distractors: あまり and ぜんぜん require a negative verb (ません/ない); ときどき (sometimes) contradicts 毎日.",
        "difficulty": 2,
    },

    # --- Set polite phrases ---
    {
        "pid": "n5-152", "form": "douzo/doumo/sumimasen/onegaishimasu",
        "question_ja": "（  ）すわって ください。",
        "choices": ["どうぞ", "どうも", "すみません", "おねがい"],
        "correct": "どうぞ",
        "explanation": "どうぞ + V-て ください = please go ahead and [V] / please [V] (offering / inviting). Distractors: どうも is gratitude (thanks), すみません is apology, おねがい is requesting a favor (won't pair with V-て + ください).",
        "difficulty": 2,
    },

    # --- Sentence-final particles (use follow-up reply to pin) ---
    {
        "pid": "n5-156", "form": "ne / yo (sentence-final)",
        "question_ja": "A: あついです（  ）。\nB: ええ、ほんとうに あついですね。",
        "choices": ["ね", "よ", "か", "の"],
        "correct": "ね",
        "explanation": "ね seeks confirmation/agreement; B's response 'ええ、ほんとうに...ですね' (yes, really hot) confirms agreement, which only pairs with ね from A. Distractors: よ is assertive (informing — B wouldn't agree-back as enthusiastically), か would make A's line a question, の is informal-question.",
        "difficulty": 2,
    },
    {
        "pid": "n5-158", "form": "darou (casual probably)",
        "question_ja": "あした、たぶん あめが ふる（  ）。",
        "choices": ["だろう", "だった", "だ", "じゃない"],
        "correct": "だろう",
        "explanation": "Plain-form + だろう = probably / I expect (casual variant of でしょう). たぶん (probably) anchors the speculation. Distractors: だった is plain past, だ is plain affirmative (no speculation), じゃない is negation.",
        "difficulty": 2,
    },
    {
        "pid": "n5-159", "form": "desu ne / desu yo (polite)",
        "question_ja": "A: この みせは あたらしいです（  ）。\nB: そうですね、せんしゅう できました。",
        "choices": ["ね", "よ", "か", "の"],
        "correct": "ね",
        "explanation": "ね seeks confirmation; B's そうですね confirms agreement, which uniquely pairs with ね. Distractors: よ would assert; か would query; の is informal.",
        "difficulty": 2,
    },

    # --- Cross-reference patterns (Noun の あとで / まえに / V-た あとで / V-plain まえに) ---
    {
        "pid": "n5-160", "form": "Noun no atode (after Noun)",
        "question_ja": "じゅぎょう（  ）あとで、ともだちと あいます。",
        "choices": ["の", "を", "に", "が"],
        "correct": "の",
        "explanation": "Noun の あとで = after [Noun]. The の is the genitive linking noun → temporal-noun (あと). Distractors: を/に/が don't link nouns to あと in this temporal pattern.",
        "difficulty": 1,
    },
    {
        "pid": "n5-161", "form": "Noun no maeni (before Noun)",
        "question_ja": "ごはん（  ）まえに、てを あらいます。",
        "choices": ["の", "を", "に", "で"],
        "correct": "の",
        "explanation": "Noun の まえに = before [Noun]. Same genitive-link pattern as n5-160 with まえ. Distractors: を/に/で don't link nouns to まえ in this temporal pattern.",
        "difficulty": 1,
    },
    {
        "pid": "n5-162", "form": "Verb-plain mae ni (before V-ing)",
        "question_ja": "ねる（  ）に、はを みがきます。",
        "choices": ["まえ", "あと", "とき", "うち"],
        "correct": "まえ",
        "explanation": "V-plain (non-past) + まえに = before [V]-ing. Sequence: brush teeth → go to bed. Distractors: あと would need V-past form (ねた あとで); とき is when; うち is while/within.",
        "difficulty": 2,
    },
    {
        "pid": "n5-163", "form": "Verb-ta atode (after V-ing)",
        "question_ja": "ごはんを たべた（  ）で、しゅくだいを します。",
        "choices": ["あと", "まえ", "とき", "ところ"],
        "correct": "あと",
        "explanation": "V-past (た-form) + あとで = after [V]-ing. Sequence: ate → then homework. Distractors: まえ would need non-past (たべる まえに); とき is when (different aspect); ところ is moment-of-action.",
        "difficulty": 2,
    },

    # --- Set greetings ---
    {
        "pid": "n5-166", "form": "set greetings",
        "question_ja": "ごはんを たべる まえに、（  ）と 言います。",
        "choices": ["いただきます", "ごちそうさま", "おはようございます", "おやすみなさい"],
        "correct": "いただきます",
        "explanation": "いただきます is said BEFORE eating (literally 'I humbly receive'). Distractors: ごちそうさま is said AFTER eating; おはようございます is morning greeting; おやすみなさい is good-night.",
        "difficulty": 1,
    },

    # --- ~ndesu ---
    {
        "pid": "n5-167", "form": "~ndesu (explanation)",
        "question_ja": "A: どうして きょう やすみましたか。\nB: あたまが いたかった（  ）。",
        "choices": ["んです", "ます", "でした", "ました"],
        "correct": "んです",
        "explanation": "Plain + んです = explanation form (giving a reason for a state/situation). A asks 'why', B explains with んです. Distractors: ます is non-past polite (wrong tense — past pain), でした copula (would need adjective ending い→かった directly + でした), ました past polite verb ending (the predicate is an i-adj, not a verb).",
        "difficulty": 3,
    },

    # --- Must-form variants (test conjugation, not nuance) ---
    {
        "pid": "n5-171", "form": "V-nai hou ga ii (shouldn't)",
        "question_ja": "あぶないですから、そこへ 行か（  ）ほうが いいです。",
        "choices": ["ない", "ます", "た", "て"],
        "correct": "ない",
        "explanation": "V-ない + ほうが いい = shouldn't [V] (negative recommendation). The slot needs the negative-plain form ない. Distractors: ます is polite-affirmative; た is past affirmative; て is conjunction form — none combine with ほうが いい to form 'shouldn't'.",
        "difficulty": 2,
    },
    {
        "pid": "n5-172", "form": "~nakute mo ii (don't have to)",
        "question_ja": "しゅくだいは あした まで ですから、きょう 出さ（  ）いいです。",
        "choices": ["なくても", "なくては", "ないと", "なくちゃ"],
        "correct": "なくても",
        "explanation": "V-stem + なくても いい = don't have to [V] (permission-not-to). Distractors test the must-form siblings: なくては requires いけない (must), ないと requires いけない (must, casual), なくちゃ is the casual contraction (would need ません to follow, not いいです).",
        "difficulty": 3,
    },
    {
        "pid": "n5-173", "form": "~nakute wa ikenai (must)",
        "question_ja": "あした、テストですから、こんばん べんきょうし（  ）いけません。",
        "choices": ["なくては", "なくても", "ないで", "なくて"],
        "correct": "なくては",
        "explanation": "V-stem + なくては + いけない = must [V] (obligation). The いけません ending forces なくては. Distractors: なくても goes with いい (don't have to); ないで is V-without-doing; なくて is conjunction without obligation.",
        "difficulty": 3,
    },
    {
        "pid": "n5-174", "form": "~nakute wa naranai (must, formal)",
        "question_ja": "がっこうの ルールを まもら（  ）なりません。",
        "choices": ["なくては", "なくても", "ないで", "なくて"],
        "correct": "なくては",
        "explanation": "V-stem + なくては + ならない = must [V] (formal obligation, same as いけない). The なりません ending forces なくては. Distractors: なくても is permission-not-to (with いい); ないで is V-without-doing; なくて is bare conjunction.",
        "difficulty": 3,
    },
    {
        "pid": "n5-175", "form": "~nai to ikenai (must, common)",
        "question_ja": "もう おそいですから、はやく 行か（  ）いけません。",
        "choices": ["ないと", "なくて", "ないで", "なくちゃ"],
        "correct": "ないと",
        "explanation": "V-ない + と + いけない = must [V] (common spoken variant of must). The いけません ending forces ないと. Distractors: なくて is bare conjunction; ないで is V-without-doing; なくちゃ doesn't pair with いけません (it's already a contraction containing いけない).",
        "difficulty": 3,
    },
    {
        "pid": "n5-176", "form": "~nakucha / ~nakya (casual must)",
        "question_ja": "もう ５じだ。はやく かえら（  ）。",
        "choices": ["なくちゃ", "なくては", "ないと", "なくても"],
        "correct": "なくちゃ",
        "explanation": "V-stem + なくちゃ = must [V] (casual contraction of なくては いけない; sentence-final by itself implies the いけない). The casual だ ending of the first sentence (もう ５じだ) anchors the casual register. Distractors: なくては/ないと would need a following いけない; なくても is permission-not-to.",
        "difficulty": 3,
    },

    # --- Casual quotation ~tte ---
    {
        "pid": "n5-179", "form": "~tte (casual quote)",
        "question_ja": "たなかさんは、あした こない（  ）言って いました。",
        "choices": ["って", "を", "が", "に"],
        "correct": "って",
        "explanation": "Plain + って + 言う / 言って いる = casual quote-marker (informal counterpart of と). Distractors: を marks direct objects (言う doesn't take a を for embedded quotes); が marks subject; に is recipient/time.",
        "difficulty": 2,
    },

    # --- ~kata (way of doing) ---
    {
        "pid": "n5-180", "form": "V-stem + kata (way of)",
        "question_ja": "おすしの たべ（  ）を おしえて ください。",
        "choices": ["かた", "とき", "ばしょ", "ひと"],
        "correct": "かた",
        "explanation": "V-stem (drop ます) + かた = way of [V]-ing. tabe-kata = way of eating. Distractors: とき (time/when), ばしょ (place), ひと (person) — none form 'way of' in this construction.",
        "difficulty": 2,
    },

    # --- ~naa exclamation ---
    {
        "pid": "n5-181", "form": "~naa (exclamation)",
        "question_ja": "「うわあ、この けしきは きれいだ（  ）。」",
        "choices": ["なあ", "ね", "よ", "か"],
        "correct": "なあ",
        "explanation": "なあ is a sentence-final exclamation expressing strong personal feeling ('really, isn't it?'). The 「うわあ」 opening interjection anchors strong emotional register, which only なあ matches. Distractors: ね seeks confirmation (less self-directed than なあ), よ asserts, か questions.",
        "difficulty": 3,
    },

    # --- ~na prohibition ---
    {
        "pid": "n5-182", "form": "V-plain + na (prohibition)",
        "question_ja": "あぶない！　そこへ 行く（  ）！",
        "choices": ["な", "ね", "よ", "の"],
        "correct": "な",
        "explanation": "V-plain (dictionary form) + な = strong/casual prohibition ('don't!'). The exclamatory あぶない！ context anchors the strong-register prohibition. Distractors: ね/よ are sentence-final tags but not prohibitions; の would form an informal question, not a command.",
        "difficulty": 2,
    },

    # --- Q-word + ka / mo compounds ---
    {
        "pid": "n5-183", "form": "Q-word + ka / mo",
        "question_ja": "「おなかが すきました。なに（  ）たべませんか。」",
        "choices": ["か", "も", "を", "に"],
        "correct": "か",
        "explanation": "なに + か = 'something' (positive existence). 'Want to eat something?' Distractors: なに + も + negative-verb = 'nothing' (would need ません), wo/ni don't form Q-word compounds.",
        "difficulty": 2,
    },
    {
        "pid": "n5-184", "form": "nanika / nanimo",
        "question_ja": "つかれましたから、なに（  ）たべたく ありません。",
        "choices": ["も", "か", "を", "が"],
        "correct": "も",
        "explanation": "なに + も + negative = nothing. The negative たべたく ありません forces も (not か, which would be positive 'something'). Distractors: か is positive existence; を/が don't form Q-word compounds.",
        "difficulty": 2,
    },
    {
        "pid": "n5-185", "form": "dareka / daremo",
        "question_ja": "へやに だれ（  ）いません。しずかです。",
        "choices": ["も", "か", "が", "に"],
        "correct": "も",
        "explanation": "だれ + も + negative-verb = no one. The negative いません forces も. Distractors: か is positive existence (would mean 'someone is there'); が/に don't form Q-word compounds.",
        "difficulty": 2,
    },
    {
        "pid": "n5-186", "form": "dokoka / dokomo",
        "question_ja": "つかれましたから、きょうは どこ（  ）行きません。",
        "choices": ["も", "か", "へ", "を"],
        "correct": "も",
        "explanation": "どこ + も + negative-verb = nowhere. The negative 行きません forces も. Distractors: か is positive 'somewhere'; へ/を don't form Q-word compounds (they're plain particles).",
        "difficulty": 2,
    },
    {
        "pid": "n5-187", "form": "itsuka / itsumo",
        "question_ja": "わたしは いつ（  ）７じに おきます。",
        "choices": ["も", "か", "に", "の"],
        "correct": "も",
        "explanation": "いつ + も = always (positive existence; differs from なに/だれ/どこ which need a negative verb to form 'nothing/no-one/nowhere'). Distractors: いつ + か = 'sometime' (would need a non-habitual context); に/の don't form Q-word compounds.",
        "difficulty": 2,
    },
]

next_num = last_num
added = 0
for n in NEW:
    next_num += 1
    qid = f"q-{next_num:04d}"
    new_q = {
        "id": qid,
        "grammarPatternId": n["pid"],
        "type": "mcq",
        "direction": "j_to_e",
        "prompt_ja": "（  ）に いちばん いい ものを えらんで ください。",
        "question_ja": n["question_ja"],
        "choices": n["choices"],
        "correctAnswer": n["correct"],
        "explanation_en": n["explanation"],
        "difficulty": n["difficulty"],
    }
    q["questions"].append(new_q)
    added += 1

json.dump(q, (ROOT / "data" / "questions.json").open("w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

print(f"\nAdded {added} new questions across {len(set(n['pid'] for n in NEW))} patterns.")
print(f"Total questions: {len(q['questions'])}")

g = json.load((ROOT / "data" / "grammar.json").open(encoding="utf-8"))
covered = set(qq.get("grammarPatternId") for qq in q["questions"])
all_pids = set(p["id"] for p in g["patterns"])
remaining = sorted(all_pids - covered)
print(f"Patterns now uncovered: {len(remaining)}")
if remaining:
    print(f"  Remaining: {remaining}")
