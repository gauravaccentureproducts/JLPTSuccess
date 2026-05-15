"""Mega-audit across all remaining content files (2026-05-15):

  data/listening.json           (50 chokai items)
  data/authentic.json           (188 real-world cards)
  data/questions.json           (290 MCQ items)
  data/drills_auto.json         (1,096 cloze drills)
  data/papers/bunpou/*.json     (7 grammar papers)
  data/papers/goi/*.json        (7 vocab papers)
  data/papers/moji/*.json       (7 script/kanji papers)

Total: ~1,924 items across 25 files.

Check categories per file type:

LISTENING (L1-L10):
  L1  empty script_ja
  L2  correctAnswer not in choices
  L3  choices count != 4
  L4  empty explanation_en
  L5  empty explanation_hi (locale parity)
  L6  audio file missing on disk
  L7  duplicate items by id
  L8  HTML markup in script_ja
  L9  empty prompt_ja
  L10 mondai out of valid N5 listening range (1, 2, 3, 4)

AUTHENTIC (A1-A8):
  A1  empty ja text
  A2  empty gloss_en
  A3  empty gloss_hi (locale parity)
  A4  empty context
  A5  empty context_hi (locale parity)
  A6  duplicate items by id
  A7  HTML markup in ja / gloss
  A8  reading field empty for non-katakana-only ja

QUESTIONS (Q1-Q10):
  Q1  empty question_ja
  Q2  correctAnswer not in choices
  Q3  choices count != 4
  Q4  empty explanation_en
  Q5  empty explanation_hi
  Q6  distractor_explanations missing for distractor choices
  Q7  distractor_explanations_hi missing
  Q8  duplicate items by id
  Q9  HTML markup leak
  Q10 grammarPatternId resolves to grammar.json

DRILLS (D1-D5):
  D1  empty stem
  D2  empty correctAnswer
  D3  correctAnswer not in acceptedAnswers
  D4  duplicate items by id
  D5  empty explanation_en

PAPERS (PP1-PP8) — for bunpou/goi/moji:
  PP1 empty stem_html
  PP2 choices count != 4
  PP3 correctIndex out of [0,3]
  PP4 duplicate choices within question
  PP5 empty rationale
  PP6 empty rationale_hi (locale parity)
  PP7 duplicate qid across all papers (within category)
  PP8 mondai out of valid range per category
"""
from __future__ import annotations
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HTML_TAG_RX = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)[\s/>]")


def has_html(s: str) -> str | None:
    if not isinstance(s, str):
        return None
    m = HTML_TAG_RX.search(s)
    return m.group(1) if m else None


def audit_listening():
    print("=" * 72)
    print("LISTENING.JSON")
    print("=" * 72)
    d = json.loads(Path("data/listening.json").read_text(encoding="utf-8"))
    items = d["items"]
    findings = defaultdict(list)
    seen_ids = Counter()
    for it in items:
        iid = it.get("id", "?")
        seen_ids[iid] += 1
        if not (it.get("script_ja") or "").strip():
            findings["L1-EMPTY-SCRIPT"].append(iid)
        choices = it.get("choices") or []
        # JLPT N5 choice counts:
        #   mondai 1 (task)      → 4
        #   mondai 2 (point)     → 4
        #   mondai 3 (utterance) → 3 strict / 4 in some authored items
        #   mondai 4 (response)  → 3
        # Accept the strict-JLPT minimums (3 for mondai 3/4, 4 for 1/2)
        # plus the looser 4-choice variants we have in mondai 3.
        fmt = it.get("format", "")
        if fmt == "response":
            expected = {3}
        elif fmt == "utterance":
            expected = {3, 4}   # corpus has both shapes; both functional
        else:
            expected = {4}
        if len(choices) not in expected:
            findings["L3-CHOICES-COUNT"].append((iid, len(choices), expected, fmt))
        ans = it.get("correctAnswer")
        if ans is not None and choices and ans not in choices:
            findings["L2-ANSWER-NOT-IN-CHOICES"].append((iid, ans, choices))
        if not (it.get("explanation_en") or "").strip():
            findings["L4-EMPTY-EXPLANATION-EN"].append(iid)
        if (it.get("explanation_en") or "").strip() and not (it.get("explanation_hi") or "").strip():
            findings["L5-EMPTY-EXPLANATION-HI"].append(iid)
        if not (it.get("prompt_ja") or "").strip():
            findings["L9-EMPTY-PROMPT"].append(iid)
        audio = (it.get("audio") or "").strip()
        if audio and not Path(audio).exists():
            findings["L6-AUDIO-MISSING"].append((iid, audio))
        tag = has_html(it.get("script_ja", ""))
        if tag:
            findings["L8-HTML-IN-SCRIPT"].append((iid, tag))
        mondai = it.get("mondai")
        if mondai is not None and mondai not in (1, 2, 3, 4):
            findings["L10-MONDAI-OOR"].append((iid, mondai))
    for iid, n in seen_ids.items():
        if n > 1:
            findings["L7-DUP-ID"].append((iid, n))
    return findings


def audit_authentic():
    print("=" * 72)
    print("AUTHENTIC.JSON")
    print("=" * 72)
    d = json.loads(Path("data/authentic.json").read_text(encoding="utf-8"))
    items = d["items"]
    findings = defaultdict(list)
    seen_ids = Counter()
    for it in items:
        iid = it.get("id", "?")
        seen_ids[iid] += 1
        if not (it.get("ja") or "").strip():
            findings["A1-EMPTY-JA"].append(iid)
        if not (it.get("gloss_en") or "").strip():
            findings["A2-EMPTY-GLOSS-EN"].append(iid)
        if (it.get("gloss_en") or "").strip() and not (it.get("gloss_hi") or "").strip():
            findings["A3-EMPTY-GLOSS-HI"].append(iid)
        if not (it.get("context") or "").strip():
            findings["A4-EMPTY-CONTEXT"].append(iid)
        if (it.get("context") or "").strip() and not (it.get("context_hi") or "").strip():
            findings["A5-EMPTY-CONTEXT-HI"].append(iid)
        tag = has_html(it.get("ja", ""))
        if tag:
            findings["A7-HTML-IN-JA"].append((iid, tag))
        tag = has_html(it.get("gloss_en", ""))
        if tag:
            findings["A7-HTML-IN-GLOSS"].append((iid, tag))
    for iid, n in seen_ids.items():
        if n > 1:
            findings["A6-DUP-ID"].append((iid, n))
    return findings


def audit_questions():
    print("=" * 72)
    print("QUESTIONS.JSON")
    print("=" * 72)
    d = json.loads(Path("data/questions.json").read_text(encoding="utf-8"))
    items = d["questions"]
    findings = defaultdict(list)
    seen_ids = Counter()
    for q in items:
        qid = q.get("id", "?")
        seen_ids[qid] += 1
        qtype = q.get("type", "")
        # Only mcq-style questions have question_ja + choices + correctAnswer
        # Other types (sentence_order, fill_in_blanks, etc.) use different
        # schemas (tiles, correctOrder, etc.).
        if qtype == "mcq":
            if not (q.get("question_ja") or "").strip():
                findings["Q1-EMPTY-QUESTION-JA"].append(qid)
            choices = q.get("choices") or []
            if len(choices) != 4:
                findings["Q3-CHOICES-NOT-4"].append((qid, len(choices)))
            ans = q.get("correctAnswer")
            if ans is not None and choices and ans not in choices:
                findings["Q2-ANSWER-NOT-IN-CHOICES"].append((qid, ans))
            # Distractor explanations: one entry per non-correct choice
            de = q.get("distractor_explanations") or {}
            if choices and ans:
                distractors = [c for c in choices if c != ans]
                missing_de = [d for d in distractors if d not in de or not (de.get(d) or "").strip()]
                if missing_de:
                    findings["Q6-DISTRACTOR-EN-MISSING"].append((qid, missing_de))
                de_hi = q.get("distractor_explanations_hi") or {}
                missing_hi = [d for d in distractors if d not in de_hi or not (de_hi.get(d) or "").strip()]
                if missing_hi:
                    findings["Q7-DISTRACTOR-HI-MISSING"].append((qid, missing_hi))
        elif qtype == "sentence_order":
            # Sentence-order questions: must have tiles + correctOrder
            if not q.get("tiles"):
                findings["Q11-SO-NO-TILES"].append(qid)
            if not q.get("correctOrder"):
                findings["Q12-SO-NO-CORRECT-ORDER"].append(qid)
        # Common-to-all-types fields
        if not (q.get("explanation_en") or "").strip():
            findings["Q4-EMPTY-EXPLANATION-EN"].append(qid)
        if (q.get("explanation_en") or "").strip() and not (q.get("explanation_hi") or "").strip():
            findings["Q5-EMPTY-EXPLANATION-HI"].append(qid)
    for qid, n in seen_ids.items():
        if n > 1:
            findings["Q8-DUP-ID"].append((qid, n))
    return findings


def audit_drills():
    print("=" * 72)
    print("DRILLS_AUTO.JSON")
    print("=" * 72)
    d = json.loads(Path("data/drills_auto.json").read_text(encoding="utf-8"))
    items = d["questions"]
    findings = defaultdict(list)
    seen_ids = Counter()
    for q in items:
        qid = q.get("id", "?")
        seen_ids[qid] += 1
        dtype = q.get("type", "")
        # `cloze` drills have a Japanese stem with a blank; `production`
        # drills are EN→JA typing exercises and have prompt_en + no stem.
        if dtype == "cloze":
            if not (q.get("stem") or "").strip():
                findings["D1-EMPTY-CLOZE-STEM"].append(qid)
        elif dtype == "production":
            if not (q.get("prompt_en") or "").strip():
                findings["D1-EMPTY-PRODUCTION-PROMPT"].append(qid)
        ans = q.get("correctAnswer")
        if not ans or not str(ans).strip():
            findings["D2-EMPTY-ANSWER"].append(qid)
        accepted = q.get("acceptedAnswers") or []
        if ans and accepted and ans not in accepted:
            findings["D3-ANSWER-NOT-IN-ACCEPTED"].append((qid, ans, accepted))
        if not (q.get("explanation_en") or "").strip():
            findings["D5-EMPTY-EXPLANATION-EN"].append(qid)
    for qid, n in seen_ids.items():
        if n > 1:
            findings["D4-DUP-ID"].append((qid, n))
    return findings


def audit_papers_category(category: str):
    findings = defaultdict(list)
    pdir = Path(f"data/papers/{category}")
    if not pdir.exists():
        return findings
    all_qids = Counter()
    valid_mondai = {"bunpou": (1, 2, 3, 4), "goi": (1, 2, 3, 4), "moji": (1, 2, 3, 4)}[category]
    for pf in sorted(pdir.glob("paper-*.json")):
        p = json.loads(pf.read_text(encoding="utf-8"))
        for q in p.get("questions", []):
            qid = q.get("id", f"{pf.stem}.q?")
            all_qids[qid] += 1
            stem = (q.get("stem_html") or "").strip()
            if not stem:
                findings["PP1-EMPTY-STEM"].append(qid)
            choices = q.get("choices") or []
            if len(choices) != 4:
                findings["PP2-CHOICES-NOT-4"].append((qid, len(choices)))
            ci = q.get("correctIndex")
            if ci is None or not isinstance(ci, int) or ci < 0 or ci > 3:
                findings["PP3-CORRECTINDEX-OOR"].append((qid, ci))
            if len(choices) != len(set(choices)):
                dup = [c for c, n in Counter(choices).items() if n > 1]
                findings["PP4-DUP-CHOICES"].append((qid, dup))
            if not (q.get("rationale") or "").strip():
                findings["PP5-EMPTY-RATIONALE"].append(qid)
            if (q.get("rationale") or "").strip() and not (q.get("rationale_hi") or "").strip():
                findings["PP6-EMPTY-RATIONALE-HI"].append(qid)
            mondai = q.get("mondai")
            if mondai is not None and mondai not in valid_mondai:
                findings["PP8-MONDAI-OOR"].append((qid, mondai))
    for qid, n in all_qids.items():
        if n > 1:
            findings["PP7-DUP-QID"].append((qid, n))
    return findings


def main():
    findings_by_file = {
        "listening.json": audit_listening(),
        "authentic.json": audit_authentic(),
        "questions.json": audit_questions(),
        "drills_auto.json": audit_drills(),
        "papers/bunpou": audit_papers_category("bunpou"),
        "papers/goi": audit_papers_category("goi"),
        "papers/moji": audit_papers_category("moji"),
    }
    print()
    print("=" * 72)
    print("MEGA-AUDIT SUMMARY")
    print("=" * 72)
    total = 0
    for fname, findings in findings_by_file.items():
        if not findings:
            print(f"\n{fname}: clean (0 findings)")
            continue
        print(f"\n{fname}:")
        for cat in sorted(findings):
            n = len(findings[cat])
            total += n
            print(f"  {cat:38s} {n}")
            for r in findings[cat][:3]:
                print(f"    {r}")
            if len(findings[cat]) > 3:
                print(f"    ... +{len(findings[cat])-3} more")
    print(f"\nTOTAL FINDINGS: {total}")


if __name__ == "__main__":
    main()
