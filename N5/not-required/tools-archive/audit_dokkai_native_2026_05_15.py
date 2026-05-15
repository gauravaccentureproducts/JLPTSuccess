"""Native-teacher accuracy audit of dokkai content:
 - data/reading.json (54 standalone passages with questions)
 - data/papers/dokkai/paper-{1..7}.json (7 mock-exam papers)

Targets content-quality gaps not covered by existing CI invariants
(JA-3, JA-5, JA-6, JA-18, JA-19, JA-20, JA-23, JA-27, JA-28, JA-73).

Check categories:

reading.json passages:
  R1  empty ja text
  R2  question with empty prompt_ja
  R3  choices count != 4
  R4  correctAnswer not in choices  [CRITICAL]
  R5  duplicate choices within question
  R6  empty explanation_en
  R7  empty translation_literal / translation_natural
  R8  empty summary
  R12 HTML markup leak in ja / questions / translations
  R13 empty title_ja
  R15 mondai out of range (must be 1..4)

papers/dokkai/*.json questions:
  P1  empty stem_html
  P2  choices count != 4
  P3  correctIndex out of range (must be 0..3)
  P4  duplicate choices within question
  P5  empty rationale
  P6  empty passage_text
  P7  duplicate question ids across all papers
  P8  HTML markup other than expected <u>/<br> in stem_html

Cross-checks:
  X1  reading.json passage audio referenced but missing on disk
"""
from __future__ import annotations
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

READING = Path("data/reading.json")
PAPERS_DIR = Path("data/papers/dokkai")

HIRA = re.compile(r"[぀-ゟ]")
KATA = re.compile(r"[゠-ヿ]")
HAN = re.compile(r"[一-鿿]")


def has_japanese(s: str) -> bool:
    return bool(HIRA.search(s) or KATA.search(s) or HAN.search(s))


def has_html_markup(s: str) -> str | None:
    """Return the first HTML tag found, or None."""
    m = re.search(r"<([a-zA-Z][a-zA-Z0-9]*)[\s/>]", s)
    return m.group(1) if m else None


def audit_reading():
    print("=" * 72)
    print("READING.JSON AUDIT")
    print("=" * 72)
    d = json.loads(READING.read_text(encoding="utf-8"))
    passages = d["passages"]
    findings = defaultdict(list)

    for p in passages:
        pid = p.get("id", "?")
        ja = (p.get("ja") or "").strip()
        if not ja:
            findings["R1-EMPTY-JA"].append(pid)
        title = (p.get("title_ja") or "").strip()
        if not title:
            findings["R13-EMPTY-TITLE"].append(pid)
        if not (p.get("translation_literal") or "").strip():
            findings["R7-EMPTY-LITERAL"].append(pid)
        if not (p.get("translation_natural") or "").strip():
            findings["R7-EMPTY-NATURAL"].append(pid)
        if not (p.get("summary") or "").strip():
            findings["R8-EMPTY-SUMMARY"].append(pid)
        # R15: mondai — for N5 dokkai, valid mondai numbers are 4, 5, 6
        #   問題4: short passages with single comprehension question
        #   問題5: mid-length passages with multiple questions
        #   問題6: information-retrieval (signs, menus, brochures)
        mondai = p.get("mondai")
        if mondai is not None and mondai not in (4, 5, 6):
            findings["R15-MONDAI-OUT-OF-RANGE"].append((pid, mondai))
        # R12: HTML markup in ja
        tag = has_html_markup(ja)
        if tag:
            findings["R12-HTML-IN-JA"].append((pid, tag, ja[:60]))

        # Questions
        for j, q in enumerate(p.get("questions", [])):
            qid = q.get("id", f"{pid}.q{j}")
            stem = (q.get("prompt_ja") or "").strip()
            if not stem:
                findings["R2-EMPTY-PROMPT"].append(qid)
            choices = q.get("choices", []) or []
            if len(choices) != 4:
                findings["R3-CHOICES-NOT-4"].append((qid, len(choices)))
            # R4: correctAnswer must be one of choices
            ans = q.get("correctAnswer")
            if ans is not None and choices and ans not in choices:
                findings["R4-ANSWER-NOT-IN-CHOICES"].append(
                    (qid, ans, choices)
                )
            # R5: duplicate choices
            if len(choices) != len(set(choices)):
                dup = [c for c, n in Counter(choices).items() if n > 1]
                findings["R5-DUP-CHOICES"].append((qid, dup))
            # R6: empty explanation
            if not (q.get("explanation_en") or "").strip():
                findings["R6-EMPTY-EXPLANATION-EN"].append(qid)
            # R12: HTML in question fields
            for fld in ("prompt_ja", "explanation_en", "explanation_hi"):
                v = q.get(fld, "")
                t = has_html_markup(v) if isinstance(v, str) else None
                if t:
                    findings["R12-HTML-IN-QUESTION"].append(
                        (qid, fld, t, v[:60])
                    )
            # R16: empty correctAnswer
            if q.get("correctAnswer") is None or (
                isinstance(q.get("correctAnswer"), str) and not q["correctAnswer"].strip()
            ):
                findings["R16-EMPTY-CORRECT-ANSWER"].append(qid)
            # R17: Hindi explanation missing when EN is present
            if (q.get("explanation_en") or "").strip() and not (q.get("explanation_hi") or "").strip():
                findings["R17-EMPTY-EXPLANATION-HI"].append(qid)
            # R18: format_role missing (renderer needs this for question
            # layout differentiation)
            if not (q.get("format_role") or "").strip():
                findings["R18-EMPTY-FORMAT-ROLE"].append(qid)

        # R19: audio file referenced but not on disk
        audio_path = (p.get("audio") or "").strip()
        if audio_path:
            disk_path = Path(audio_path)
            if not disk_path.exists():
                findings["R19-AUDIO-MISSING"].append((pid, audio_path))

        # R20: kanji_used / vocab_used populated when ja is non-empty
        if ja and not p.get("kanji_used"):
            findings["R20-KANJI-USED-EMPTY"].append(pid)
        if ja and not p.get("vocab_used"):
            findings["R20-VOCAB-USED-EMPTY"].append(pid)

        # R21: summary_hi present (locale parity)
        if (p.get("summary") or "").strip() and not (p.get("summary_hi") or "").strip():
            findings["R21-SUMMARY-HI-MISSING"].append(pid)

        # R22: paragraphs structure (when present, paragraphs[i].ja
        # should reconstruct the full ja text approximately)
        paragraphs = p.get("paragraphs") or []
        if paragraphs:
            paragraph_text = "".join(
                (par.get("ja") or "") for par in paragraphs
            ).strip()
            # Lose-comparison: stripped both should match
            pure_ja = re.sub(r"\s+", "", ja)
            pure_par = re.sub(r"\s+", "", paragraph_text)
            if pure_ja and pure_par and pure_par != pure_ja:
                # Allow small differences (newline / punctuation)
                if abs(len(pure_par) - len(pure_ja)) > 5:
                    findings["R22-PARAGRAPHS-DESYNC"].append(
                        (pid, len(pure_par), len(pure_ja))
                    )

    print()
    for cat in sorted(findings):
        rows = findings[cat]
        print(f"  {cat:35s} {len(rows)}")
        for r in rows[:5]:
            print(f"    {r}")
        if len(rows) > 5:
            print(f"    ... +{len(rows)-5} more")
    print()
    return findings


def audit_papers():
    print("=" * 72)
    print("PAPERS/DOKKAI AUDIT")
    print("=" * 72)
    findings = defaultdict(list)
    all_qids: Counter[str] = Counter()
    paper_files = sorted(PAPERS_DIR.glob("paper-*.json"))
    total_questions = 0
    for pf in paper_files:
        p = json.loads(pf.read_text(encoding="utf-8"))
        for j, q in enumerate(p.get("questions", [])):
            total_questions += 1
            qid = q.get("id", f"{pf.stem}.q{j}")
            all_qids[qid] += 1
            stem = (q.get("stem_html") or "").strip()
            if not stem:
                findings["P1-EMPTY-STEM"].append(qid)
            choices = q.get("choices", []) or []
            if len(choices) != 4:
                findings["P2-CHOICES-NOT-4"].append((qid, len(choices)))
            ci = q.get("correctIndex")
            if ci is None or not isinstance(ci, int) or ci < 0 or ci > 3:
                findings["P3-CORRECTINDEX-OOR"].append((qid, ci))
            if len(choices) != len(set(choices)):
                dup = [c for c, n in Counter(choices).items() if n > 1]
                findings["P4-DUP-CHOICES"].append((qid, dup))
            if not (q.get("rationale") or "").strip():
                findings["P5-EMPTY-RATIONALE"].append(qid)
            if not (q.get("passage_text") or "").strip():
                findings["P6-EMPTY-PASSAGE"].append(qid)
            # P8: HTML markup beyond expected <u>/<br>
            for fld in ("stem_html", "rationale", "passage_text"):
                v = q.get(fld, "")
                if isinstance(v, str):
                    # Find all tags
                    for m in re.finditer(r"<([a-zA-Z][a-zA-Z0-9]*)[\s/>]", v):
                        tag = m.group(1).lower()
                        if tag not in ("u", "br", "b", "i", "em", "strong"):
                            findings["P8-UNEXPECTED-HTML"].append(
                                (qid, fld, tag, v[:60])
                            )

    # P7: duplicate question ids across all papers
    for qid, n in all_qids.items():
        if n > 1:
            findings["P7-DUP-QID"].append((qid, n))

    # Extra deep checks across papers
    for pf in paper_files:
        p = json.loads(pf.read_text(encoding="utf-8"))
        for q in p.get("questions", []):
            qid = q.get("id", "?")
            # P9: empty Hindi rationale (locale parity)
            if (q.get("rationale") or "").strip() and not (q.get("rationale_hi") or "").strip():
                findings["P9-EMPTY-RATIONALE-HI"].append(qid)
            # P10: mondai out of valid N5 dokkai range (4, 5, 6)
            mondai = q.get("mondai")
            if mondai is not None and mondai not in (4, 5, 6):
                findings["P10-MONDAI-OOR"].append((qid, mondai))
            # P11: kbSourceId missing (provenance)
            if not (q.get("kbSourceId") or "").strip():
                findings["P11-KB-SOURCE-MISSING"].append(qid)
            # P12: passage_label missing
            if not (q.get("passage_label") or "").strip():
                findings["P12-PASSAGE-LABEL-MISSING"].append(qid)
            # P13: correctIndex points to a choice that exists
            ci = q.get("correctIndex")
            choices = q.get("choices", [])
            if isinstance(ci, int) and choices and (ci >= len(choices)):
                findings["P13-CORRECT-INDEX-OUT-OF-CHOICES"].append(
                    (qid, ci, len(choices))
                )

    print(f"\nTotal questions across all papers: {total_questions}\n")
    for cat in sorted(findings):
        rows = findings[cat]
        print(f"  {cat:35s} {len(rows)}")
        for r in rows[:5]:
            print(f"    {r}")
        if len(rows) > 5:
            print(f"    ... +{len(rows)-5} more")
    print()
    return findings


def main():
    print(f"\n{'#'*72}\n# DOKKAI AUDIT — reading.json + papers/dokkai\n{'#'*72}\n")
    r_findings = audit_reading()
    p_findings = audit_papers()
    print()
    print("=" * 72)
    print("OVERALL SUMMARY")
    print("=" * 72)
    print("\nreading.json:")
    for cat in sorted(r_findings):
        print(f"  {cat:35s} {len(r_findings[cat])}")
    print("\npapers/dokkai:")
    for cat in sorted(p_findings):
        print(f"  {cat:35s} {len(p_findings[cat])}")


if __name__ == "__main__":
    main()
