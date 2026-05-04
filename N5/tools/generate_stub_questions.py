"""Generate stub MCQ questions for any patterns in data/grammar.json that don't
yet have a question in data/questions.json.

Each stub is a recognition-style question: given the English meaning, choose
the matching Japanese pattern from 4 options (1 correct + 3 random distractors).

Run from the repo root:
    python tools/generate_stub_questions.py

Idempotent: only adds stubs for uncovered patterns. Existing questions are
preserved unchanged.
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Deterministic seed so re-runs produce the same stub set.
random.seed(42)


def main() -> int:
    grammar_path = ROOT / "data" / "grammar.json"
    questions_path = ROOT / "data" / "questions.json"

    grammar = json.loads(grammar_path.read_text(encoding="utf-8"))
    qbank = json.loads(questions_path.read_text(encoding="utf-8"))

    patterns = grammar.get("patterns", [])
    questions = qbank.get("questions", [])
    covered = {q["grammarPatternId"] for q in questions}

    to_stub = [p for p in patterns if p["id"] not in covered]
    if not to_stub:
        print("No uncovered patterns. Nothing to do.")
        return 0

    # Index patterns by their .pattern label for distractor selection.
    by_label = {}
    for p in patterns:
        by_label.setdefault(p["pattern"], []).append(p)

    all_labels = list(by_label.keys())

    # Determine starting question id.
    used_ids = []
    for q in questions:
        try:
            used_ids.append(int(q["id"].split("-")[1]))
        except (ValueError, IndexError):
            continue
    next_id = (max(used_ids) + 1) if used_ids else 1

    new_count = 0
    for p in to_stub:
        meaning = p.get("meaning_en") or "TBD"
        if meaning == "TBD":
            meaning = (
                "(stub) - pattern needs authoring. See "
                f"KnowledgeBank/grammar_n5.md for source"
            )

        # Pick 3 random distractors with labels different from this pattern.
        candidate_labels = [lbl for lbl in all_labels if lbl != p["pattern"]]
        random.shuffle(candidate_labels)
        distractors = candidate_labels[:3]

        choices = [p["pattern"]] + distractors
        random.shuffle(choices)

        new_q = {
            "id": f"q-{next_id:04d}",
            "grammarPatternId": p["id"],
            "type": "mcq",
            "direction": "e_to_j",
            "prompt_ja": "つぎの いみに あう パターンを えらんでください。",
            "question_ja": meaning,
            "choices": choices,
            "correctAnswer": p["pattern"],
            "explanation_en": (
                f"Stub question for {p['id']} ({p['pattern']}). "
                "Replace with a real fill-in-blank or sentence-order question "
                "once the pattern's examples are authored."
            ),
            "high_confusion": False,
            "difficulty": 1,
            "is_stub": True,
        }
        questions.append(new_q)
        next_id += 1
        new_count += 1

    qbank["questions"] = questions
    questions_path.write_text(
        json.dumps(qbank, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Added {new_count} stub questions. Total questions: {len(questions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
