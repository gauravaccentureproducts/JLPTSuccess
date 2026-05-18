"""
fix_dokkai_bugs_horizontal_2026_05_18.py
========================================

Horizontal deployment of DOKKAI-001..003 fixes per Rule 6 — applies the
same fixes to non-dokkai paper files where the same drift classes exist.

Horizontal-scan findings (after initial fix_dokkai_bugs_2026_05_18.py):

  - 10 bunpou/paper-7.json Mondai 3 questions have stray passage_text
    (same DOKKAI-001 drift class — but no passages[] block exists yet
    in bunpou/paper-7.json; need to CREATE it from the unique passages
    extracted from question.passage_text + question.passage_label, then
    drop passage_text from questions)
  - 1 goi-7.1 question has " ago" in rationale_hi (same DOKKAI-002
    class — extend the fix)
  - 83 non-dokkai questions missing grammarPatternId (11 goi + 72 moji)
    — extend DOKKAI-003 explicit-null pattern to all paper categories
    with category-appropriate provenance ("not_applicable_vocab",
    "not_applicable_orthography")
"""
import sys, io, json, os, shutil, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_18"

# Map category → provenance value for grammarPatternId=null entries
NULL_PROVENANCE_BY_CATEGORY = {
    "dokkai": "not_applicable_comprehension",
    "goi": "not_applicable_vocab",
    "moji": "not_applicable_orthography",
    "bunpou": "not_applicable_comprehension",  # bunpou Mondai-4 dokkai-style sub-questions if any
}

# goi-7.1 fix (carry-over of DOKKAI-002 "ago" class)
GOI_002_FIX = {
    "goi-7.1": {
        "rationale_hi": "यहाँ एक साल से = एक साल पहले आया।",
        "rationale_hi_provenance": "native_reviewed_2026_05_18",
    },
}


def backup(fp):
    bak = fp + f".bak_{TODAY}_dokkai_horizontal"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)


def fix_bunpou_paper_7():
    """bunpou/paper-7.json has 10 Mondai 3 questions referencing 2 paragraph passages
    via passage_label, but the passages are stored only as passage_text on each
    question — no passages[] block. Create the passages[] block from the unique
    passage_text values, then drop passage_text from questions.
    """
    fp = os.path.join(REPO_N5, "data", "papers", "bunpou", "paper-7.json")
    backup(fp)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)

    # Build unique passages map: label → text (taking first occurrence per label)
    # Also normalize: strip leading "> " if present
    passages_by_label = {}
    label_to_question_ids = {}
    for q in d.get("questions", []):
        label = q.get("passage_label")
        if not label:
            continue
        text = q.get("passage_text", "") or ""
        text_norm = text.lstrip().removeprefix("> ").rstrip()
        if label not in passages_by_label:
            passages_by_label[label] = text_norm
            label_to_question_ids[label] = []
        label_to_question_ids[label].append(q.get("id"))

    # Insert passages[] block (preserve key ordering by mutating the dict)
    if passages_by_label:
        d["passages"] = [
            {
                "label": label,
                "text": passages_by_label[label],
                "question_ids": label_to_question_ids[label],
            }
            for label in sorted(passages_by_label.keys())
        ]

    # Drop passage_text from questions
    dropped = 0
    for q in d.get("questions", []):
        if "passage_text" in q:
            del q["passage_text"]
            dropped += 1

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  bunpou/paper-7.json: created passages[] with {len(passages_by_label)} entries; dropped {dropped} stray passage_text fields")


def fix_remaining_grammar_pattern_id_nulls():
    """Add grammarPatternId=null + category-appropriate provenance to every
    paper question that's missing the field."""
    filled = 0
    for fp in sorted(glob.glob(os.path.join(REPO_N5, "data", "papers", "*", "*.json"))):
        if "manifest" in os.path.basename(fp) or ".bak" in os.path.basename(fp):
            continue
        category = os.path.basename(os.path.dirname(fp))
        backup(fp)
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        modified = False
        for q in d.get("questions", []):
            if "grammarPatternId" not in q:
                q["grammarPatternId"] = None
                q["grammarPatternId_provenance"] = NULL_PROVENANCE_BY_CATEGORY.get(category, "not_applicable")
                modified = True
                filled += 1
        if modified:
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  grammarPatternId nulls filled across non-dokkai papers: {filled}")


def fix_goi_7_1_ago():
    """goi-7.1 has the same untranslated 'ago' as dokkai-1.1. Apply same fix shape."""
    fp = os.path.join(REPO_N5, "data", "papers", "goi", "paper-7.json")
    backup(fp)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    fixed = 0
    for q in d.get("questions", []):
        qid = q.get("id", "")
        if qid in GOI_002_FIX:
            spec = GOI_002_FIX[qid]
            for k, v in spec.items():
                q[k] = v
            fixed += 1
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  goi-7.1 'ago' fragment: fixed {fixed} entries")


def main():
    print("=== Horizontal deployment of DOKKAI-001..003 fixes ===")
    print()
    print("Stage 1: bunpou/paper-7.json passages[] + passage_text drop (DOKKAI-001 horizontal)")
    fix_bunpou_paper_7()
    print()
    print("Stage 2: goi-7.1 'ago' fragment (DOKKAI-002 horizontal)")
    fix_goi_7_1_ago()
    print()
    print("Stage 3: 83 non-dokkai grammarPatternId nulls (DOKKAI-003 horizontal)")
    fix_remaining_grammar_pattern_id_nulls()


if __name__ == "__main__":
    main()
