"""Batch 2 of DEFER-1: 20 more single-correct questions for previously-
uncovered grammar patterns. Run-once 2026-05-02 after batch 1 (q-0514..q-0528).

Target: drop the uncovered count from 50 -> 30.

Each question is single-correct, uses N5-only kanji, has 4 distinct
distractors that are clearly wrong. Patterns from grey-zone-prone
categories (frequency adverbs, sentence-final particles, kosoado
quartets without scene context) are deliberately skipped this round
and will need extra care to author cleanly later.
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

NEW = [
    {
        "pid": "n5-114", "form": "kara ~ made (from X to Y)",
        "question_ja": "じゅぎょうは ９じ（  ）１２じまでです。",
        "choices": ["から", "まで", "に", "へ"],
        "correct": "から",
        "explanation": "X kara Y made = from X to Y. The blank pairs with まで in the second half, so から (start) is the only fit. Distractors: まで is already used; に is recipient/time-point (not range); へ is direction.",
        "difficulty": 1,
    },
    {
        "pid": "n5-137", "form": "Noun no Noun",
        "question_ja": "これは わたし（  ）ほんです。",
        "choices": ["の", "は", "が", "を"],
        "correct": "の",
        "explanation": "Noun の Noun = possessive/attributive linking. watashi no hon = my book. Distractors: は marks topic (would change meaning to topic-comment); が marks subject; を marks object.",
        "difficulty": 1,
    },
    {
        "pid": "n5-142", "form": "ni shimasu (decide on)",
        "question_ja": "わたしは コーヒー（  ）します。",
        "choices": ["に", "を", "が", "で"],
        "correct": "に",
        "explanation": "X に します = decide on / choose X (e.g., when ordering at a restaurant). The choice marker is に. Distractors: を + する is generic 'do X'; が marks subject; で is means/place.",
        "difficulty": 1,
    },
    {
        "pid": "n5-143", "form": "ni narimasu / ku narimasu (becomes)",
        "question_ja": "そらが あおく（  ）。",
        "choices": ["なりました", "しました", "あります", "います"],
        "correct": "なりました",
        "explanation": "i-adj-stem + ku + narimasu = becomes [adj]. aoku narimashita = became blue. Distractors: shimashita is 'did' (transitive change); arimasu / imasu are 'exist'.",
        "difficulty": 2,
    },
    {
        "pid": "n5-145", "form": "to omoimasu (I think that)",
        "question_ja": "あした、あめが ふる（  ）おもいます。",
        "choices": ["と", "を", "に", "で"],
        "correct": "と",
        "explanation": "Plain-form sentence + と + omoimasu = I think that ~. と is the quote-marker linking the embedded clause to omoimasu. Distractors: を marks direct object (omou doesn't take a を for embedded thoughts); に/で wrong category.",
        "difficulty": 1,
    },
    {
        "pid": "n5-146", "form": "to iimashita (said that)",
        "question_ja": "せんせいは「あした テストです」（  ）言いました。",
        "choices": ["と", "を", "に", "で"],
        "correct": "と",
        "explanation": "Direct-quote + と + iimashita = said that ~. The brackets「」around the quoted speech force と as the quote-marker. Distractors: を/に/で don't function as quote-markers.",
        "difficulty": 1,
    },
    {
        "pid": "n5-149", "form": "wo kudasai (please give me)",
        "question_ja": "すみません、コーヒー（  ）ください。",
        "choices": ["を", "に", "が", "の"],
        "correct": "を",
        "explanation": "Noun + を + kudasai = please give me [noun]. The thing requested takes the object marker を. Distractors: に is recipient/time; が marks subject; の is possessive.",
        "difficulty": 1,
    },
    {
        "pid": "n5-150", "form": "wo onegaishimasu (I'd like ~)",
        "question_ja": "すみません、お茶（  ）おねがいします。",
        "choices": ["を", "に", "で", "と"],
        "correct": "を",
        "explanation": "Noun + を + onegaishimasu = I'd like [noun] please (more polite than wo kudasai). Same を-marks-the-thing pattern. Distractors: に/で/と don't fit this request frame.",
        "difficulty": 1,
    },
    {
        "pid": "n5-151", "form": "wa ikaga desu ka (how about)",
        "question_ja": "コーヒー（  ）いかがですか。",
        "choices": ["は", "を", "に", "が"],
        "correct": "は",
        "explanation": "Noun は ikaga desu ka = how about [noun]? (polite offer). は marks the noun as topic of the offer. Distractors: を/に/が don't fit the offer-introduction pattern.",
        "difficulty": 1,
    },
    {
        "pid": "n5-153", "form": "mada + V-te imasen (not yet)",
        "question_ja": "「ごはんを たべましたか。」「いいえ、（  ）たべて いません。」",
        "choices": ["まだ", "もう", "いま", "すぐ"],
        "correct": "まだ",
        "explanation": "mada + V-te imasen = not yet (action still pending). The negative answer 'no, I have not eaten yet' pins まだ. Distractors: もう would pair with the affirmative 'already ate'; いま (now) and すぐ (right away) don't fit the not-yet frame.",
        "difficulty": 2,
    },
    {
        "pid": "n5-154", "form": "mou + V-mashita (already)",
        "question_ja": "「しゅくだいを しましたか。」「はい、（  ）しました。」",
        "choices": ["もう", "まだ", "いま", "あとで"],
        "correct": "もう",
        "explanation": "mou + V-mashita = already (action completed). The affirmative answer 'yes, already did' pins もう. Distractors: まだ would pair with negative; いま (now) doesn't match completed-past; あとで (later) is future.",
        "difficulty": 1,
    },
    {
        "pid": "n5-155", "form": "ga (mid-sentence but)",
        "question_ja": "この りょうりは おいしいです（  ）、すこし からいです。",
        "choices": ["が", "から", "ので", "まで"],
        "correct": "が",
        "explanation": "Mid-sentence が = but (contrast connector). 'Tasty BUT a bit spicy.' Distractors: から/ので are causal (because); まで is endpoint.",
        "difficulty": 1,
    },
    {
        "pid": "n5-157", "form": "deshou (probably / right?)",
        "question_ja": "あした、たぶん あめが ふる（  ）。",
        "choices": ["でしょう", "でした", "ですか", "でして"],
        "correct": "でしょう",
        "explanation": "deshou = probably / I expect (paired with tabun 'probably' in the stem for emphasis). Distractors: deshita (past copula), desu ka (question ending — would change meaning), deshite (te-form, ungrammatical sentence-finally).",
        "difficulty": 2,
    },
    {
        "pid": "n5-164", "form": "san (name suffix)",
        "question_ja": "あの ひとは たなか（  ）です。",
        "choices": ["さん", "ちゃん", "くん", "さま"],
        "correct": "さん",
        "explanation": "san is the standard polite name suffix (Mr./Ms.) for adults in neutral contexts. Distractors: chan (young children / very close friends), kun (young men / juniors), sama (extremely formal — overkill for everyday use).",
        "difficulty": 1,
    },
    {
        "pid": "n5-165", "form": "o~ / go~ (beautifying prefix)",
        "question_ja": "（  ）ちゃを のみますか。",
        "choices": ["お", "ご", "の", "を"],
        "correct": "お",
        "explanation": "o-cha = (honorific) tea. Native-Japanese-origin words usually take お (o-); Sino-Japanese words take ご (go-). Distractors: ご is for Sino-Japanese stems (gohan, gokazoku); の is possessive; を is object marker.",
        "difficulty": 2,
    },
    {
        "pid": "n5-168", "form": "tari ~ tari suru",
        "question_ja": "にちようびは ほんを よんだり、おんがくを きいたり（  ）。",
        "choices": ["します", "あります", "います", "なります"],
        "correct": "します",
        "explanation": "V-tari V-tari + suru = do A and B (among other things). The pattern needs the suru helper at the end to bind the listed activities. Distractors: arimasu/imasu are existence verbs; narimasu is 'become' — none bind tari-listings.",
        "difficulty": 2,
    },
    {
        "pid": "n5-169", "form": "V-ta koto ga aru (have done before)",
        "question_ja": "わたしは にほんへ 行った（  ）が あります。",
        "choices": ["こと", "もの", "ところ", "とき"],
        "correct": "こと",
        "explanation": "V-ta + koto + ga arimasu = have done [V] before (experiential). Only こと forms this experience-pattern. Distractors: もの is a physical thing; ところ is a place; とき is a time/occasion.",
        "difficulty": 2,
    },
    {
        "pid": "n5-170", "form": "V-ta hou ga ii (should do)",
        "question_ja": "つかれた ときは、はやく ねた（  ）が いいです。",
        "choices": ["ほう", "もの", "こと", "ところ"],
        "correct": "ほう",
        "explanation": "V-ta + hou + ga + ii = should do [V] (recommendation). Only ほう forms this recommendation pattern. Distractors: もの/こと/ところ don't fit this comparative-recommendation frame.",
        "difficulty": 2,
    },
    {
        "pid": "n5-177", "form": "V-stem / Adj-stem + sugiru",
        "question_ja": "この りょうりは からい（  ）。",
        "choices": ["すぎます", "すぎる", "すぎて", "すぎない"],
        "correct": "すぎます",
        "explanation": "i-adj-stem (drop い) + sugimasu = too [adj]. karai → kara + sugimasu = 'too spicy'. Wait — actually karai stem is kara-, but the construction is karasugiru. Distractors: sugiru (plain form mid-sentence inappropriate), sugite (te-form), suginai (negative). The polite-finished-sentence form sugimasu fits the deshou-style ending.",
        "difficulty": 3,
    },
    {
        "pid": "n5-178", "form": "V-plain + tsumori da (intend to)",
        "question_ja": "らいねん、にほんへ 行く（  ）です。",
        "choices": ["つもり", "もの", "こと", "とき"],
        "correct": "つもり",
        "explanation": "V-plain + tsumori desu = intend to do [V]. Only つもり forms this intention pattern. Distractors: もの (physical thing), こと (matter/fact), とき (time/occasion) don't carry the future-intention sense.",
        "difficulty": 2,
    },
]

# Fix n5-177 — the stem I wrote uses karai (i-adj) and the answer slot
# attaches the suffix to the stem. Re-checking: 'kono ryouri wa karai
# (sugimasu)' — putting すぎます after the い-form would require dropping
# the い: 'kono ryouri wa kara-sugimasu'. So my stem is malformed.
# Fix: change stem to something cleaner.
for n in NEW:
    if n["pid"] == "n5-177":
        n["question_ja"] = "この にもつは おも（  ）。"
        n["choices"] = ["すぎます", "すぎる", "すぎて", "すぎない"]
        n["correct"] = "すぎます"
        n["explanation"] = (
            "i-adj-stem (drop い) + sugimasu = too [adj]. omoi → omo + "
            "sugimasu = 'too heavy'. Distractors: sugiru (plain form, "
            "would need different polite-level context), sugite (te-form, "
            "conjunction not a sentence ender), suginai (negative — would "
            "mean 'not too heavy' which contradicts the implied complaint)."
        )

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
print(f"Sample remaining: {remaining[:10]}")
