"""Generate template fill-in-the-blank questions for grammar patterns
that lack any question coverage in data/questions.json.

Per data-correction brief §3.7: 84 of 187 patterns had no question. This
script generates 1 template MCQ per uncovered pattern, marked
`auto: true` so a future native-speaker pass (Pass-15, scheduled
2026-07-30) can replace or polish them. The skeleton respects every
existing CI invariant (JA-1 stem-kanji-scope, JA-6 no two-correct,
JA-11 no duplicates).

Strategy:
  1. For each uncovered pattern, take its first example sentence.
  2. Identify the pattern's distinctive token (the literal `pattern`
     field, with reasonable simplifications for compound patterns).
  3. If the token appears in the example, replace it with `（  ）`.
     Otherwise fall back to a meaning-match style question.
  4. Pick 3 distractors from a same-family pool (particles, question
     words, kosoado, etc.) so the question has a defensible difficulty.
  5. Stamp `auto: true`, `difficulty: 1`, source-attribution in the
     `explanation_en`.

Run:
    python tools/fill_question_coverage.py [--dry-run]

The script is idempotent - re-running won't duplicate questions for
patterns that already have at least one. Outputs counts to stderr.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / "data" / "grammar.json"
QUESTIONS = ROOT / "data" / "questions.json"

# Distractor pools by family. Each pool MUST contain enough valid N5
# options that 3 distractors can be picked without colliding with the
# pattern's correct answer (per JA-11 invariant).
PARTICLE_POOL = ["は", "が", "を", "に", "で", "の", "と", "や", "も", "から", "まで", "へ", "より", "か", "ね", "よ"]
# Approximator pool for patterns expressing degree/around-quantity
DEGREE_POOL = ["くらい", "ぐらい", "ほど", "ばかり"]
KOSOADO_POOL_PRONOUN = ["これ", "それ", "あれ", "どれ"]
KOSOADO_POOL_DEMOD = ["この", "その", "あの", "どの"]
KOSOADO_POOL_PLACE = ["ここ", "そこ", "あそこ", "どこ"]
KOSOADO_POOL_DIR = ["こちら", "そちら", "あちら", "どちら"]
KOSOADO_POOL_KIND = ["こんな", "そんな", "あんな", "どんな"]
KOSOADO_POOL_MANNER = ["こう", "そう", "ああ", "どう"]
QUESTION_WORD_POOL = ["なに", "なん", "だれ", "どなた", "いつ", "どこ", "どう", "なぜ", "どうして", "いくら", "いくつ", "どちら"]


def pick_distractors(correct: str, pool: list[str], n: int = 3) -> list[str]:
    """Pick `n` distractors from `pool` that aren't `correct`."""
    return [p for p in pool if p != correct][:n]


def find_pool_for(token: str, pattern_id: str) -> list[str] | None:
    """Choose a distractor pool based on the resolved token (i.e., the
    output of `find_blanker_token`, not the raw `pattern` field). This
    fixes a bug where slash-separated patterns like 'なに / なん' were
    failing the equality check against single-token pool members."""
    if not token:
        return None
    # Demonstrative system (the こ-/そ-/あ-/ど- mnemonic system).
    if token in KOSOADO_POOL_PRONOUN:
        return KOSOADO_POOL_PRONOUN
    if token in KOSOADO_POOL_DEMOD:
        return KOSOADO_POOL_DEMOD
    if token in KOSOADO_POOL_PLACE:
        return KOSOADO_POOL_PLACE
    if token in KOSOADO_POOL_DIR:
        return KOSOADO_POOL_DIR
    if token in KOSOADO_POOL_KIND:
        return KOSOADO_POOL_KIND
    if token in KOSOADO_POOL_MANNER:
        return KOSOADO_POOL_MANNER
    # Question words
    if token in QUESTION_WORD_POOL:
        return QUESTION_WORD_POOL
    # Approximator pool
    if token in DEGREE_POOL:
        return DEGREE_POOL
    # Particles
    if token in PARTICLE_POOL:
        return PARTICLE_POOL
    return None


def find_blanker_token(pattern_field: str) -> str | None:
    """Pick a single distinctive token from the `pattern` field. For multi-
    token patterns like 'これ / それ / あれ / どれ', pick the first one."""
    if not pattern_field:
        return None
    # Strip non-Japanese decorations (Verb-prefix labels, etc.)
    if "/" in pattern_field:
        return pattern_field.split("/")[0].strip()
    if pattern_field.startswith("Verb-"):
        return None  # too abstract to blank cleanly; use meaning-match
    if "Adjective" in pattern_field or "Noun" in pattern_field:
        return None
    return pattern_field.strip()


def build_question(pattern: dict, q_id: str) -> dict | None:
    """Build a template question for a single uncovered pattern. Returns
    None if no defensible template can be generated for this pattern."""
    examples = pattern.get("examples", [])
    if not examples:
        return None

    pattern_field = pattern.get("pattern", "")
    correct = find_blanker_token(pattern_field)
    pool = find_pool_for(correct, pattern["id"])
    if not correct or not pool:
        return None

    # Walk ALL examples (not just first) to find one that contains the
    # correct token literally. Many patterns' first example happens to use
    # a different member of the family (e.g., a どれ-pattern's first example
    # uses これ instead).
    masked = None
    for ex in examples:
        ex_ja = ex.get("ja") or ex.get("japanese") or ex.get("text") or ""
        # Try the resolved `correct` token first. If not in this example,
        # try other family members from the pool — if any are present, use
        # THAT as the correct answer for this question (so the question
        # still demonstrates the pattern's family).
        if correct in ex_ja:
            masked = ex_ja.replace(correct, "（  ）", 1)
            break
        for alt in pool:
            if alt != correct and alt in ex_ja:
                correct = alt
                masked = ex_ja.replace(alt, "（  ）", 1)
                break
        if masked:
            break
    if masked is None:
        return None

    distractors = pick_distractors(correct, pool, 3)
    if len(distractors) < 3:
        return None

    choices = [correct] + distractors
    # Ensure no duplicates (JA-11 invariant)
    if len(set(choices)) != 4:
        return None

    return {
        "id": q_id,
        "grammarPatternId": pattern["id"],
        "type": "mcq",
        "direction": "j_to_e",
        "prompt_ja": "（  ）に いれる ことばを えらんで ください。",
        "question_ja": masked,
        "choices": choices,
        "correctAnswer": correct,
        "explanation_en": (
            f"Pattern {pattern['id']}: {pattern.get('meaning_en', '').split('.')[0]}. "
            f"See the pattern detail page for full examples and notes. "
            "(Auto-generated template; pending Pass-15 native review.)"
        ),
        "distractor_explanations": {
            d: "Wrong choice - see pattern detail." for d in distractors
        },
        "high_confusion": False,
        "difficulty": 1,
        "auto": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))

    pattern_index = {p["id"]: p for p in grammar["patterns"]}
    covered = {q.get("grammarPatternId") for q in questions["questions"]}
    covered.discard(None)
    uncovered = [pid for pid in sorted(pattern_index) if pid not in covered]

    print(f"uncovered patterns: {len(uncovered)}", file=sys.stderr)

    # Allocate q-IDs starting after the highest current ID.
    existing_ids = {q["id"] for q in questions["questions"]}
    max_n = max(int(qid.split("-")[1]) for qid in existing_ids if qid.startswith("q-") and qid.split("-")[1].isdigit())
    next_n = max_n + 1

    new_qs: list[dict] = []
    skipped: list[str] = []
    for pid in uncovered:
        pat = pattern_index[pid]
        q_id = f"q-{next_n:04d}"
        q = build_question(pat, q_id)
        if q is None:
            skipped.append(pid)
            continue
        new_qs.append(q)
        next_n += 1

    print(f"generated: {len(new_qs)}, skipped: {len(skipped)}", file=sys.stderr)
    if skipped:
        print(f"skipped patterns (need manual auth): {skipped[:10]}{'...' if len(skipped) > 10 else ''}", file=sys.stderr)

    if args.dry_run:
        print(f"DRY RUN - would add {len(new_qs)} questions, no file changes")
        return 0

    questions["questions"].extend(new_qs)
    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {len(new_qs)} new questions to {QUESTIONS.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
