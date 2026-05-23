"""Batch B — content fixes for deferred items 1 / 2 / 5 / 9.

  - Item 1 (RP-006): swap 7 N1+ distractors for N3-level alternatives
    in moji-6.9 / 6.11 / 6.12 / 7.4
  - Item 2 (RP-007): enrich 36 thin moji mondai-2 rationales using a
    template that names which visually-similar candidate trips the
    learner
  - Item 5 (RP-008): rebalance moji correctIndex distribution
    (28/26/25/21 → closer to 25/25/25/25)
  - Item 9 (RP-009): rebalance goi correctIndex distribution
    (27/27/25/21 → closer to 25/25/25/25)
"""
import sys, io, os, json, shutil, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"


# Item 1: off-level distractor replacements.
# Pick visually-similar kanji in N5 whitelist OR dokkai_kanji_exception
# (so JA-150 / JA-13 don't trip), preferring N3-level when available.
# Visual similarity = shares a radical with the correct kanji.
DISTRACTOR_REPLACEMENTS = {
    # moji-6.9: correct 聞 (k-radical 門). 訊 (N1) → 問 (門-radical, N3, in dokkai exception).
    "moji-6.9": [("訊きます", "問きます")],
    # moji-6.11: correct 読 (言-radical). 詠 (N1) → 話 (言-radical, N5 whitelist).
    # 諳 (non-JLPT) → 語 (言-radical, in whitelist).
    "moji-6.11": [("詠みます", "話みます"), ("諳みます", "語みます")],
    # moji-6.12: correct 書 (日 + 又). 掻 (N1) → 画 (similar 田-radical, in exception).
    # Keep 描 (N3-ish, reviewer accepted as borderline).
    "moji-6.12": [("掻きます", "画きます")],
    # moji-7.4: correct 言 (言-radical). 謂 (N1) → 試 (言-radical-similar, in exception).
    # Keep 議 (N3, reviewer accepted).
    "moji-7.4": [("謂います", "試います")],
}


def fix_item_1():
    """Swap 7 off-level distractors. Verify the replacements aren't
    accidentally the correct answer + keep correctIndex unchanged."""
    fixed = 0
    for qid, swaps in DISTRACTOR_REPLACEMENTS.items():
        paper_num = qid.split("-")[1].split(".")[0]
        fp = os.path.join(REPO_N5, "data", "papers", "moji", f"paper-{paper_num}.json")
        bak = fp + f".bak_{TODAY}_rp_006"
        if not os.path.exists(bak): shutil.copy2(fp, bak)
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        for q in d.get("questions") or []:
            if q.get("id") != qid: continue
            choices = q.get("choices") or []
            correct_idx = q.get("correctIndex")
            correct_text = choices[correct_idx] if correct_idx is not None else None
            for old_text, new_text in swaps:
                if new_text == correct_text:
                    print(f"  RP-006 ({qid}): SKIP swap {old_text!r}→{new_text!r} (collides with correct)")
                    continue
                # Replace in-place
                for i, c in enumerate(choices):
                    if c == old_text:
                        choices[i] = new_text
                        fixed += 1
                        print(f"  RP-006 ({qid}): choice [{i}] {old_text!r} → {new_text!r}")
                        break
            q["rp_006_fix_2026_05_23"] = "off-level distractors swapped for in-scope visually-similar alternatives"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  RP-006 total: {fixed} distractor swaps")


def fix_item_2():
    """Enrich rationales under 15 chars in moji mondai 2.

    Template: <correct kanji> (<reading>). 視覚的に 似ている 候補に
    注意 (e.g., <distractor>) — 意味が 違う.

    For each thin rationale, parse the current text + choices, build
    a template-augmented rationale that's informative but mechanical.
    """
    enriched = 0
    for fp in sorted(glob.glob("data/papers/moji/paper-*.json")):
        if ".bak" in fp: continue
        full_fp = os.path.join(REPO_N5, fp.replace("/", os.sep))
        if not os.path.exists(full_fp): full_fp = os.path.abspath(fp)
        bak = full_fp + f".bak_{TODAY}_rp_007"
        if not os.path.exists(bak): shutil.copy2(full_fp, bak)
        with open(full_fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        modified = False
        for q in d.get("questions") or []:
            if not isinstance(q, dict): continue
            if q.get("mondai") != 2: continue
            rat = q.get("rationale", "") or ""
            if len(rat) >= 15: continue
            # Enrich
            choices = q.get("choices") or []
            ci = q.get("correctIndex")
            if ci is None or not choices: continue
            correct = choices[ci] if ci < len(choices) else ""
            distractors = [c for i, c in enumerate(choices) if i != ci]
            new_rat = (
                f"正解: {correct}. 元の解説: 「{rat}」. 視覚的に 似ているが 意味が 違う候補: "
                f"{', '.join(distractors)} — それぞれ別の意味を持つ漢字。"
            )
            q["rationale"] = new_rat
            q["rationale_provenance"] = "template_enriched_2026_05_23"
            q["rp_007_fix_2026_05_23"] = "thin rationale template-enriched"
            enriched += 1
            modified = True
        if modified:
            with open(full_fp, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  RP-007 total: {enriched} rationales template-enriched")


def fix_item_5_and_9(category, target_paper_dir, expected_initial_dist):
    """Rebalance correctIndex distribution by rotating ~7 questions
    from over-represented positions to under-represented ones.

    For moji (28/26/25/21): move 3-4 A-positions to D-position.
    For goi (27/27/25/21):  move 2-3 from A/B to D.

    Mechanism: select questions where current correctIndex is over-rep,
    rotate their choices so the correct text moves to under-rep position,
    update correctIndex to match. Provenance-stamp the rebalance.
    """
    from collections import Counter
    # First pass: collect candidates
    candidates_to_rotate = []  # list of (fp, qid, current_ci, target_ci)
    counter = Counter()
    all_questions = []
    for fp in sorted(glob.glob(f"data/papers/{category}/paper-*.json")):
        if ".bak" in fp: continue
        full_fp = os.path.join(REPO_N5, fp.replace("/", os.sep))
        if not os.path.exists(full_fp): full_fp = os.path.abspath(fp)
        with open(full_fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        for q in d.get("questions") or []:
            if isinstance(q, dict) and q.get("correctIndex") is not None:
                counter[q["correctIndex"]] += 1
                all_questions.append((full_fp, q))
    over = [(pos, n) for pos, n in counter.items() if n > 26]
    under = [(pos, n) for pos, n in counter.items() if n < 24]
    print(f"  {category} initial: {dict(counter)} (over: {over}, under: {under})")
    if not over or not under: return
    # Plan rotations
    rotations = []  # (qid, from_pos, to_pos)
    over_remaining = {pos: n - 25 for pos, n in over}
    under_needed = {pos: 25 - n for pos, n in under}
    for full_fp, q in all_questions:
        if not over_remaining or not under_needed: break
        cur = q["correctIndex"]
        if cur in over_remaining and over_remaining[cur] > 0:
            target = next(iter(under_needed))
            rotations.append((full_fp, q, cur, target))
            over_remaining[cur] -= 1
            under_needed[target] -= 1
            if under_needed[target] <= 0: del under_needed[target]
            if over_remaining[cur] <= 0: del over_remaining[cur]
    # Apply rotations
    files_touched = {}
    for full_fp, q, from_pos, to_pos in rotations:
        choices = q["choices"] or []
        if from_pos >= len(choices) or to_pos >= len(choices): continue
        # Swap the choice at from_pos with the one at to_pos
        choices[from_pos], choices[to_pos] = choices[to_pos], choices[from_pos]
        q["correctIndex"] = to_pos
        q["rp_008_or_009_fix_2026_05_23"] = f"correctIndex rebalanced {from_pos}→{to_pos}"
        files_touched[full_fp] = files_touched.get(full_fp, [])
        files_touched[full_fp].append(q.get("id"))
    # Write back affected files
    for fp_path, qids in files_touched.items():
        with open(fp_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
        # The mutation already happened in-memory on the same dict refs
        # because we passed q (a reference to the actual entry). But we
        # loaded from disk into a fresh dict; need to re-read & re-apply.
        pass  # the in-memory q is part of the cached load — needs careful rewrite below
    # Simpler: per-file pass that does in-memory mutate then write
    counter2 = Counter()
    for full_fp in sorted(set(fp for fp, _, _, _ in rotations)):
        bak = full_fp + f".bak_{TODAY}_rp_008_009"
        if not os.path.exists(bak): shutil.copy2(full_fp, bak)
        with open(full_fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        for q in d.get("questions") or []:
            if not isinstance(q, dict): continue
            for _fp, _q, from_pos, to_pos in rotations:
                if _fp == full_fp and _q.get("id") == q.get("id"):
                    choices = q.get("choices") or []
                    if from_pos < len(choices) and to_pos < len(choices):
                        choices[from_pos], choices[to_pos] = choices[to_pos], choices[from_pos]
                        q["correctIndex"] = to_pos
                        q["rp_008_or_009_fix_2026_05_23"] = f"correctIndex rebalanced {from_pos}→{to_pos}"
        with open(full_fp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    # Recount
    for fp in sorted(glob.glob(f"data/papers/{category}/paper-*.json")):
        if ".bak" in fp: continue
        full_fp = os.path.join(REPO_N5, fp.replace("/", os.sep))
        if not os.path.exists(full_fp): full_fp = os.path.abspath(fp)
        with open(full_fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        for q in d.get("questions") or []:
            if isinstance(q, dict) and q.get("correctIndex") is not None:
                counter2[q["correctIndex"]] += 1
    print(f"  {category} after rebalance: {dict(counter2)}  ({len(rotations)} rotations applied)")


def main():
    print("=== Item 1 (RP-006): off-level distractor swaps ===")
    fix_item_1()
    print()
    print("=== Item 2 (RP-007): thin rationale enrichment ===")
    fix_item_2()
    print()
    print("=== Item 5 (RP-008): moji correctIndex rebalance ===")
    fix_item_5_and_9("moji", "moji", (28, 26, 25, 21))
    print()
    print("=== Item 9 (RP-009): goi correctIndex rebalance ===")
    fix_item_5_and_9("goi", "goi", (27, 27, 25, 21))
    print()
    print("=== Batch B complete ===")


if __name__ == "__main__":
    main()
