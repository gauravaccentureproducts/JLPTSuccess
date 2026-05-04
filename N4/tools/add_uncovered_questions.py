"""One-shot script: author 15 new questions for previously-uncovered grammar patterns.

Triggered by DEFER-1 (multi-session content authoring) — chips at the
65 uncovered patterns. Run once 2026-05-02. Each question is single-correct,
uses N5-only kanji, has 4 distinct distractors that are clearly wrong (no
multi-correct grey zones — verified after run by tools/audit_multi_correct.py).
"""
import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

q = json.load((ROOT / "data" / "questions.json").open(encoding="utf-8"))

existing_ids = sorted([qq["id"] for qq in q["questions"] if qq.get("id", "").startswith("q-")])
last_num = int(existing_ids[-1].split("-")[1]) if existing_ids else 0
print(f"Last q-id: {existing_ids[-1] if existing_ids else 'none'}, next: q-{last_num+1:04d}")

NEW = [
    {
        "pid": "n5-031", "pattern_form": "sentence-final no",
        "question_ja": "A: あした、しごとに 行く（  ）。\nB: ううん、行かない。",
        "choices": ["の", "よ", "ね", "と"],
        "correct": "の",
        "explanation": "Sentence-final no (rising intonation) marks an informal yes/no question. B-plain-negative reply confirms A asked a question. Distractors: yo (assertive), ne (confirmation-seeking), to (quote-marker, ungrammatical sentence-finally).",
        "difficulty": 1,
    },
    {
        "pid": "n5-094", "pattern_form": "ga arimasu (events/skills/possessions)",
        "question_ja": "らいしゅう しけん（  ）あります。",
        "choices": ["が", "を", "に", "で"],
        "correct": "が",
        "explanation": "X ga arimasu is the canonical pattern for there is/have an event. Subject is marked by ga. Distractors: wo marks direct objects (arimasu is intransitive); ni marks location/time; de marks place of action.",
        "difficulty": 1,
    },
    {
        "pid": "n5-106", "pattern_form": "Noun + ga hoshii desu",
        "question_ja": "わたしは あたらしい くつ（  ）ほしいです。",
        "choices": ["が", "を", "に", "と"],
        "correct": "が",
        "explanation": "hoshii takes ga to mark the object of desire (not wo). watashi wa X ga hoshii desu = I want X. Distractors: wo ungrammatical with hoshii; ni/to wrong category.",
        "difficulty": 1,
    },
    {
        "pid": "n5-111", "pattern_form": "ji (oclock counter)",
        "question_ja": "いま なん（  ）ですか。",
        "choices": ["じ", "ふん", "にち", "がつ"],
        "correct": "じ",
        "explanation": "ima nan-ji = what time/oclock now? — ji is the oclock counter. Distractors: fun (minutes), nichi (day), gatsu (month).",
        "difficulty": 1,
    },
    {
        "pid": "n5-113", "pattern_form": "ji-han (half past)",
        "question_ja": "がっこうは ８じ（  ）に はじまります。",
        "choices": ["はん", "ばん", "まえ", "あと"],
        "correct": "はん",
        "explanation": "ji-han = half past. 8-ji-han = 8:30. Distractors: ban (evening), mae (before), ato (after).",
        "difficulty": 1,
    },
    {
        "pid": "n5-116", "pattern_form": "mainichi / maishuu / etc.",
        "question_ja": "（  ）あさ ７じに おきます。",
        "choices": ["まいにち", "きのう", "こんばん", "あした"],
        "correct": "まいにち",
        "explanation": "mainichi = every day. Pairs with habitual present. Distractors: kinou (yesterday), konban (tonight), ashita (tomorrow) — all single-day temporals, not recurrence.",
        "difficulty": 1,
    },
    {
        "pid": "n5-118", "pattern_form": "ima / sugu / mou / mada",
        "question_ja": "「ごはんは（  ）たべましたか。」「はい、もう たべました。」",
        "choices": ["もう", "まだ", "いま", "すぐ"],
        "correct": "もう",
        "explanation": "mou (already) pairs with the affirmative answer yes I already ate. Distractors: mada (yet/still — would pair with negative answer), ima (now — wrong tense), sugu (right away — wrong nuance).",
        "difficulty": 2,
    },
    {
        "pid": "n5-119", "pattern_form": "mae (before)",
        "question_ja": "ごはんを たべる（  ）に てを あらいます。",
        "choices": ["まえ", "あと", "うしろ", "うえ"],
        "correct": "まえ",
        "explanation": "Verb-dictionary-form + mae-ni = before doing. taberu mae ni te wo arau = wash hands before eating (canonical sequence). Distractors: ato needs past-form (tabeta ato de); ushiro/ue are spatial.",
        "difficulty": 1,
    },
    {
        "pid": "n5-120", "pattern_form": "ato (after)",
        "question_ja": "べんきょうした（  ）で、ともだちと あいます。",
        "choices": ["あと", "まえ", "とき", "うち"],
        "correct": "あと",
        "explanation": "Verb-past-form + ato-de = after doing. benkyou-shita ato de = after studying. Distractors: mae needs non-past-form (benkyou-suru mae ni); toki/uchi wrong nuance.",
        "difficulty": 1,
    },
    {
        "pid": "n5-125", "pattern_form": "dewa / ja",
        "question_ja": "「もう おそいですから、（  ）かえります。」",
        "choices": ["では", "でも", "けれど", "だから"],
        "correct": "では",
        "explanation": "dewa (formal) / ja (casual) = well then — transitions from a stated reason to a follow-up action. Distractors: demo (but/however) introduces contrast, not transition; keredo (but) similar contrast; dakara (therefore) is causal explanation, not transition.",
        "difficulty": 2,
    },
    {
        "pid": "n5-127", "pattern_form": "keredo / kedo (but)",
        "question_ja": "にほんごは むずかしい（  ）、おもしろいです。",
        "choices": ["けれど", "から", "まで", "ので"],
        "correct": "けれど",
        "explanation": "keredo (or kedo informal) = but / although — connects contrasting clauses. Distractors: kara/node are causal (because), made is endpoint.",
        "difficulty": 1,
    },
    {
        "pid": "n5-129", "pattern_form": "doushite ka. ... kara.",
        "question_ja": "「（  ）にほんへ きましたか。」「にほんごを べんきょうしたいですから。」",
        "choices": ["どうして", "いつ", "どこ", "だれ"],
        "correct": "どうして",
        "explanation": "doushite = why — pairs with kara (because) in the answer. The B response gives a reason, so A asked why. Distractors: itsu (when), doko (where), dare (who) all expect different answer types.",
        "difficulty": 1,
    },
    {
        "pid": "n5-132", "pattern_form": "ga kuremasu (give to me)",
        "question_ja": "たんじょうびに、ともだち（  ）プレゼントを くれました。",
        "choices": ["が", "を", "に", "で"],
        "correct": "が",
        "explanation": "X ga (watashi ni) Y wo kureru = X gives Y (to me / in-group). The giver is marked with ga. Distractors: wo marks the gift, ni marks recipient, de is means/place.",
        "difficulty": 2,
    },
    {
        "pid": "n5-135", "pattern_form": "Verb-plain + Noun (relative clause)",
        "question_ja": "きのう（  ）ひとは たなかさんです。",
        "choices": ["きた", "きます", "きました", "こない"],
        "correct": "きた",
        "explanation": "Plain-form verb modifies a following noun (relative clause). kita hito = the person who came. Distractors: kimasu/kimashita are polite-form (cannot modify a noun directly in N5); konai would mean the person who doesnt come — wrong sense for past event.",
        "difficulty": 2,
    },
    {
        "pid": "n5-136", "pattern_form": "Adjective + Noun",
        "question_ja": "これは とても（  ）ほんです。",
        "choices": ["おもしろい", "おもしろく", "おもしろくて", "おもしろくない"],
        "correct": "おもしろい",
        "explanation": "i-adjective in dictionary form modifies a following noun directly: omoshiroi hon = interesting book. Distractors: omoshiroku (adverb form), omoshirokute (te-form, conjunction), omoshirokunai (negative) — none modify a noun in this slot.",
        "difficulty": 1,
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
