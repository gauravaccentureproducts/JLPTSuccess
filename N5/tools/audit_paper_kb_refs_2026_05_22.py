"""Inspect all paper-file fields for any KnowledgeBank/ residue beyond source_file.

Also check static mirrors (N5/papers/**/index.html) for rendered KB references
and check whether source_file is rendered to a user-visible surface.
"""
import sys, io, json, glob, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=== source_question_range values ===")
seen_sqr = {}
for fp in sorted(glob.glob("data/papers/*/paper-*.json")):
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    sqr = d.get("source_question_range", "<MISSING>")
    seen_sqr.setdefault(sqr, []).append(fp.replace("\\", "/"))
for k, files in seen_sqr.items():
    print(f"  {k!r}: {len(files)} files")
    if len(files) <= 3:
        for fp in files:
            print(f"      {fp}")

print()
print("=== Top-level fields with KnowledgeBank/ string (excluding 'questions' nested array) ===")
hits = []
for fp in sorted(glob.glob("data/papers/*/paper-*.json")):
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    for k, v in d.items():
        if k == "questions":
            continue
        if isinstance(v, str) and "KnowledgeBank" in v:
            hits.append((fp, k))
for h in hits[:20]:
    print(f"  {h[0]}: field {h[1]!r}")
total_files = len(set(h[0] for h in hits))
print(f"  TOTAL: {len(hits)} top-level field hits across {total_files} files")

print()
print("=== Static-mirror HTML files rendering source_file? ===")
mirror_hits = []
for mfp in sorted(glob.glob("papers/*/index.html")):
    with open(mfp, "r", encoding="utf-8") as f:
        html = f.read()
    if "KnowledgeBank" in html or "source_file" in html or "authored in-place" in html:
        mirror_hits.append(mfp)
print(f"  mirrors mentioning KnowledgeBank / source_file / authored in-place: {len(mirror_hits)}")
for m in mirror_hits[:5]:
    print(f"    {m}")

print()
print("=== Other repo files with 'KnowledgeBank/' substring (excluding .git, not-required, archives) ===")
import subprocess
try:
    out = subprocess.check_output(
        ["git", "grep", "-l", "KnowledgeBank/", "--"],
        encoding="utf-8", errors="replace"
    ).strip().splitlines()
except Exception as e:
    out = [f"<git grep failed: {e}>"]
for p in out[:30]:
    print(f"  {p}")
print(f"  TOTAL files with 'KnowledgeBank/' substring: {len(out)}")
