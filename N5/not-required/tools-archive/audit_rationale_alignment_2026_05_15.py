"""Wave 3 sub-audit — rationale-answer alignment.

For each MCQ question in papers/*/paper-*.json, check that the rationale
mentions or correlates with the correct answer text. Catches the
dokkai-2.3 class of bug where the rationale describes a different part
of the passage than the answer it's supposed to justify.

Heuristic:
  - For each (correct_answer, rationale) pair, compute character
    overlap. If <2 characters of the answer appear in the rationale,
    flag for review.
  - Allow numeric / short answers (e.g., '土曜日', '七時') to be matched
    fuzzily.
"""
from __future__ import annotations
import json
import re
from collections import defaultdict
from pathlib import Path


HIRA_KATA_HAN = re.compile(r"[ぁ-ゟ゠-ヿ一-鿿]")


def japanese_chars(s: str) -> set[str]:
    return set(c for c in s if HIRA_KATA_HAN.match(c))


def main():
    findings = defaultdict(list)
    n_questions = 0
    for cat in ("dokkai", "bunpou", "goi", "moji"):
        pdir = Path(f"data/papers/{cat}")
        if not pdir.exists():
            continue
        for pf in sorted(pdir.glob("paper-*.json")):
            paper = json.loads(pf.read_text(encoding="utf-8"))
            for q in paper.get("questions") or []:
                n_questions += 1
                qid = q.get("id", f"{pf.stem}.q?")
                choices = q.get("choices") or []
                ci = q.get("correctIndex")
                if not isinstance(ci, int) or ci < 0 or ci >= len(choices):
                    continue
                correct = choices[ci]
                rationale = (q.get("rationale") or "").strip()
                if not rationale:
                    continue
                # Skip very-short correct answers (single char common across MCQs)
                if len(correct) <= 1:
                    continue
                # Compute character overlap
                correct_chars = japanese_chars(correct)
                rationale_chars = japanese_chars(rationale)
                if not correct_chars:
                    continue
                overlap = correct_chars & rationale_chars
                # Require at least 2 chars of overlap OR substring match
                if correct in rationale:
                    continue
                if len(overlap) >= max(2, len(correct_chars) // 3):
                    continue
                # Otherwise: rationale doesn't reference the answer
                findings["R-RATIONALE-ANSWER-MISALIGNED"].append(
                    (cat, qid, correct, overlap, rationale[:80])
                )
    print(f"Total questions scanned: {n_questions}")
    print()
    for cat in sorted(findings):
        rows = findings[cat]
        print(f"{cat}: {len(rows)}")
        for r in rows[:15]:
            print(f"  {r}")
        if len(rows) > 15:
            print(f"  ... +{len(rows)-15} more")


if __name__ == "__main__":
    main()
