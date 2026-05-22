"""Advisory tool — surface TASKS.md '[ ]' items that may already be shipped.

Closes the gap surfaced 2026-05-22 when SVA-1.1 (footer privacy badge)
and SVA-1.4 (Export Progress button) were discovered to already exist
in the codebase, despite TASKS.md showing them as '[ ]' (pending).
Doc-state drifts from code-state when humans add features without
sweeping TASKS.md.

This tool is INTENTIONALLY HEURISTIC, not a strict CI invariant.
False positives are expected — surface candidates for human review,
do NOT fail CI on suspected duplication.

For each '- [ ]' line in TASKS.md:
  1. Extract noun-phrase keywords (CSS classes mentioned, function/
     handler names, locale keys, file paths, distinctive English
     phrases).
  2. Grep the codebase (js/, css/, locales/, index.html, prompts/)
     for those keywords.
  3. Score the match strength:
       - HIGH: explicit symbol match (e.g., backticked file path or
         CSS class found verbatim in code)
       - MEDIUM: keyword phrase appears verbatim in implementation
         file
       - LOW: only weak/partial matches
       - NONE: keyword doesn't appear at all
  4. Output advisory: HIGH/MEDIUM candidates for human verification.

NOT a CI gate. Run on demand:
  python tools/audit_tasks_md_against_codebase_2026_05_22.py
  python tools/audit_tasks_md_against_codebase_2026_05_22.py --all
    (include LOW matches too)
"""
import sys, io, os, re, subprocess, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_keywords(line: str) -> list[str]:
    """Pull distinctive keywords from a TASKS.md `[ ]` line.

    Priority extraction order:
      1. Backticked tokens: `like-this` → very high signal
      2. CSS-class-shaped tokens: .foo-bar
      3. Quoted phrases: "Export your data"
      4. File-extension tokens: PRIVACY.md, branding.json
      5. Distinctive 3+ word phrases from the bullet text
    """
    keywords: list[str] = []

    # Backticked tokens
    for m in re.finditer(r"`([^`]{2,60})`", line):
        kw = m.group(1).strip()
        if kw and kw not in keywords:
            keywords.append(kw)

    # File-extension tokens (e.g., PRIVACY.md, branding.json, SELF-HOST.md)
    for m in re.finditer(r"\b([A-Za-z0-9_\-/]+\.(md|json|css|js|html|txt|tsv|yaml|yml))\b", line):
        kw = m.group(1)
        if kw not in keywords:
            keywords.append(kw)

    # Quoted phrases
    for m in re.finditer(r'"([^"]{6,80})"', line):
        kw = m.group(1).strip()
        if kw and kw not in keywords:
            keywords.append(kw)

    return keywords


def grep_codebase(keyword: str, root: str) -> list[tuple[str, int, str]]:
    """Search the codebase for occurrences of `keyword`. Returns list of
    (file, line_number, line_content) tuples. Limits to interesting
    surfaces: js/, css/, locales/, index.html, PRIVACY.md, README.md.
    """
    if len(keyword) < 3:
        return []
    paths = ["js", "css", "locales", "index.html", "PRIVACY.md", "README.md", "prompts"]
    cmd = [
        "git", "grep", "-n", "-F", "--", keyword,
    ] + paths
    try:
        result = subprocess.run(
            cmd, cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=10
        )
    except Exception:
        return []
    hits: list[tuple[str, int, str]] = []
    for line in result.stdout.strip().splitlines():
        m = re.match(r"^([^:]+):(\d+):(.*)$", line)
        if m:
            hits.append((m.group(1), int(m.group(2)), m.group(3).strip()[:120]))
    return hits


def score_item(line: str, hits_per_kw: dict[str, list]) -> tuple[str, str]:
    """Score the match strength + return a one-line explanation."""
    total = sum(len(v) for v in hits_per_kw.values())
    distinct_files = set()
    for hits in hits_per_kw.values():
        for fp, _, _ in hits:
            distinct_files.add(fp)
    if total == 0:
        return ("NONE", "no keyword hits")
    # If any backticked token matched in an implementation file
    code_files = [f for f in distinct_files if f.startswith(("js/", "css/", "locales/")) or f == "index.html"]
    if total >= 5 and len(code_files) >= 2:
        return ("HIGH", f"{total} hits across {len(distinct_files)} files, {len(code_files)} in code")
    if total >= 2 and len(code_files) >= 1:
        return ("MEDIUM", f"{total} hits across {len(distinct_files)} files, {len(code_files)} in code")
    return ("LOW", f"{total} hits across {len(distinct_files)} files")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Include LOW-confidence matches in output (default: HIGH + MEDIUM only)")
    args = parser.parse_args()

    tasks_path = os.path.join(REPO_N5, "TASKS.md")
    if not os.path.exists(tasks_path):
        print("TASKS.md not found")
        return 1

    with open(tasks_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    open_items: list[tuple[int, str]] = []
    for i, line in enumerate(lines, start=1):
        m = re.match(r"^-\s*\[\s*\]\s+(.+)$", line.rstrip("\n"))
        if m:
            open_items.append((i, m.group(1)))

    print(f"Scanning {len(open_items)} '[ ]' items in TASKS.md against js/ + css/ + locales/ + index.html + PRIVACY.md + README.md + prompts/")
    print()

    high_or_medium = 0
    show_levels = {"HIGH", "MEDIUM"}
    if args.all:
        show_levels.add("LOW")

    for line_no, text in open_items:
        kws = extract_keywords(text)
        if not kws:
            continue  # no distinctive keywords; can't audit
        hits_per_kw: dict[str, list] = {}
        for kw in kws:
            h = grep_codebase(kw, REPO_N5)
            if h:
                hits_per_kw[kw] = h
        if not hits_per_kw:
            continue
        level, summary = score_item(text, hits_per_kw)
        if level not in show_levels:
            continue
        if level in ("HIGH", "MEDIUM"):
            high_or_medium += 1
        snippet = text[:90] + ("..." if len(text) > 90 else "")
        print(f"  [{level}] TASKS.md:L{line_no}: {snippet}")
        print(f"    keywords matched: {sorted(hits_per_kw.keys())}")
        print(f"    {summary}")
        # Show up to 3 sample hits
        sample = []
        for kw, hits in hits_per_kw.items():
            for fp, ln, content in hits[:1]:
                sample.append(f"      {fp}:{ln}: {content[:80]}")
                if len(sample) >= 3:
                    break
            if len(sample) >= 3:
                break
        for s in sample:
            print(s)
        print()

    print(f"=== Summary ===")
    print(f"  total '[ ]' items: {len(open_items)}")
    print(f"  flagged HIGH or MEDIUM (suspect already-shipped): {high_or_medium}")
    if high_or_medium == 0:
        print("  Nothing suspect — all '[ ]' items appear genuinely unimplemented.")
    else:
        print(f"  Review each flag and either flip to '[x]' (if shipped) or document why it's still open.")
    print(f"  Bounded-coverage: false positives expected. This is an advisory heuristic, not a CI gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
