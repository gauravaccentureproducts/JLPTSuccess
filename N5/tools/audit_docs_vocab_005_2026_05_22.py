"""Verify DOCS-VOCAB-005 claim:
 - all 28 paper files carry source_file pointing to KnowledgeBank/
 - methodology doc heading structure
 - n5_vocab_whitelist_README.md existence
"""
import sys, io, json, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=== source_file values across all paper files ===")
seen = {}
all_paper_files = sorted(glob.glob("data/papers/*/paper-*.json"))
print(f"  total paper files found: {len(all_paper_files)}")
for fp in all_paper_files:
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    sf = d.get("source_file", "<MISSING>")
    norm = fp.replace("\\", "/")
    seen.setdefault(sf, []).append(norm)
for sf, files in seen.items():
    print(f"  {sf!r}: {len(files)} files")
    for fpath in files[:3]:
        print(f"      {fpath}")
    if len(files) > 3:
        print(f"      ... ({len(files)-3} more)")

print()
print("=== docs/N5-syllabus-methodology.md headings ===")
methodology_path = "docs/N5-syllabus-methodology.md"
if os.path.exists(methodology_path):
    with open(methodology_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if line.startswith("#"):
                print(f"  L{i}: {line.rstrip()}")
else:
    print("  FILE NOT FOUND")

print()
print("=== vocab_whitelist file existence ===")
matches = list(glob.glob("**/*vocab_whitelist*", recursive=True))
if matches:
    for p in matches:
        print(f"  found: {p}")
else:
    print("  no files matching *vocab_whitelist* found")

# Also look for any *whitelist* file
print()
matches = list(glob.glob("**/n5_vocab*", recursive=True))
if matches:
    for p in matches:
        print(f"  found n5_vocab*: {p}")
else:
    print("  no n5_vocab* files found")
