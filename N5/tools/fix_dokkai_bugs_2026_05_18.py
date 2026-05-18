"""
fix_dokkai_bugs_2026_05_18.py
=============================

Closes DOKKAI-001..003 (BUG-107..109).

DOKKAI-001 — passage_text duplicated across passages[] and questions[];
            12 of 102 have "> " blockquote prefix drift.
DOKKAI-002 — dokkai-1.1 rationale_hi contains untranslated "ago".
DOKKAI-003 — grammarPatternId schema-shape inconsistency (78/102 have,
            24 missing).

Plus horizontal sweep across bunpou/goi/moji paper files for any
similar passage_text duplication or schema-shape inconsistency.

Non-destructive: writes .bak files before mutating.
"""
import sys, io, json, os, shutil, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_18"

# DOKKAI-002 specific fix
DOKKAI_002_FIX = {
    "dokkai-1.1": {
        "rationale_hi": "भूत-सकारात्मक: एक महीना पहले आया (अब यहाँ रह रहा है)।",
        "rationale_hi_provenance": "native_reviewed_2026_05_18",
    },
}

def backup(fp):
    bak = fp + f".bak_{TODAY}_dokkai_close"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)

def fix_dokkai_paper(fp):
    """Apply all 3 DOKKAI fixes to a single dokkai paper file."""
    backup(fp)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)

    stats = {
        "passage_text_dropped": 0,
        "passages_text_normalized": 0,  # leading "> " stripped from passages[].text
        "rationale_hi_rewritten": 0,
        "grammar_pattern_id_filled_null": 0,
    }

    # DOKKAI-001 fix part B: normalize passages[].text — strip leading "> " if present.
    for passage in d.get("passages", []):
        text = passage.get("text", "") or ""
        if text.startswith("> "):
            passage["text"] = text[2:]
            stats["passages_text_normalized"] += 1
        elif text.lstrip().startswith("> "):
            # Conservative: only strip when the file uses "> " as a true prefix
            pass

    for q in d.get("questions", []):
        qid = q.get("id", "")

        # DOKKAI-001 fix part A: drop redundant passage_text from questions
        if "passage_text" in q:
            del q["passage_text"]
            stats["passage_text_dropped"] += 1

        # DOKKAI-002 fix: rewrite specific rationale_hi
        if qid in DOKKAI_002_FIX:
            spec = DOKKAI_002_FIX[qid]
            for k, v in spec.items():
                q[k] = v
            stats["rationale_hi_rewritten"] += 1

        # DOKKAI-003 fix: add grammarPatternId=null + provenance="not_applicable_comprehension"
        # where missing. This matches option (a) recommended by the bug spec.
        if "grammarPatternId" not in q:
            q["grammarPatternId"] = None
            q["grammarPatternId_provenance"] = "not_applicable_comprehension"
            stats["grammar_pattern_id_filled_null"] += 1

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

    return stats

def horizontal_scan_other_papers():
    """Look for the same drift classes in bunpou/goi/moji papers."""
    findings = {
        "passage_text_in_non_dokkai": 0,
        "missing_grammarPatternId_in_non_dokkai": [],
        "english_fragments_in_rationale_hi": [],
    }
    STOP_LIST = [" ago", " ago.", " ago,", " ago)", " yet ", " yet.", " yet,", " yet)",
                 " lot ", " lot.", " lot,", " ago "]
    # Also extend trigger set to include other English temporal/quantity markers
    # but keep narrow to avoid false positives on legitimate kanji like "ago" (none in N5).
    for fp in sorted(glob.glob(os.path.join(REPO_N5, "data", "papers", "*", "*.json"))):
        if "manifest" in os.path.basename(fp) or ".bak" in os.path.basename(fp):
            continue
        category = os.path.basename(os.path.dirname(fp))
        d = json.load(open(fp, encoding="utf-8"))
        for q in d.get("questions", []):
            qid = q.get("id", "")
            # Non-dokkai shouldn't have passage_text
            if category != "dokkai" and "passage_text" in q:
                findings["passage_text_in_non_dokkai"] += 1
            # Schema-shape: bunpou/goi/moji should all have grammarPatternId after PAPER-001/002 close-out
            if category != "dokkai" and "grammarPatternId" not in q:
                findings["missing_grammarPatternId_in_non_dokkai"].append((qid, category))
            # English-fragment scan extension
            rh = q.get("rationale_hi", "") or ""
            for trig in STOP_LIST:
                if trig in rh:
                    findings["english_fragments_in_rationale_hi"].append((qid, trig, rh[:120]))
                    break
    return findings

def main():
    dokkai_files = sorted(glob.glob(os.path.join(REPO_N5, "data", "papers", "dokkai", "paper-*.json")))
    total_stats = {
        "passage_text_dropped": 0,
        "passages_text_normalized": 0,
        "rationale_hi_rewritten": 0,
        "grammar_pattern_id_filled_null": 0,
    }
    for fp in dokkai_files:
        s = fix_dokkai_paper(fp)
        print(f"  {os.path.basename(fp)}: {s}")
        for k in total_stats:
            total_stats[k] += s[k]
    print()
    print("=== Totals ===")
    for k, v in total_stats.items():
        print(f"  {k}: {v}")

    print()
    print("=== Horizontal scan results ===")
    findings = horizontal_scan_other_papers()
    print(f"  passage_text in non-dokkai papers (should be 0): {findings['passage_text_in_non_dokkai']}")
    print(f"  missing grammarPatternId in non-dokkai papers: {len(findings['missing_grammarPatternId_in_non_dokkai'])}")
    if findings['missing_grammarPatternId_in_non_dokkai']:
        for qid, cat in findings['missing_grammarPatternId_in_non_dokkai'][:5]:
            print(f"    {cat}/{qid}")
    print(f"  English fragments in rationale_hi (stop-list): {len(findings['english_fragments_in_rationale_hi'])}")
    for qid, trig, rh in findings['english_fragments_in_rationale_hi'][:5]:
        print(f"    {qid} ({trig!r}): {rh}")

if __name__ == "__main__":
    main()
