"""Check that every pattern listed in KnowledgeBank/grammar_n5.md has an entry in data/grammar.json.

Run from the repo root:
    python tools/check_coverage.py

Exits with 0 if coverage is complete, 1 otherwise.
This is a count-based check; deep substring matching across notation variants
(〜 vs ～, etc.) is a Phase 2 enhancement.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def extract_md_pattern_lines(md_path: Path) -> list[str]:
    """Return non-empty bullet lines that look like grammar patterns.

    Skips the ## Legend section (its bullets describe tagging conventions,
    not grammar patterns). Also skips example sub-bullets ("- Example: ...")
    which are pedagogical illustrations under their parent pattern.
    """
    text = md_path.read_text(encoding="utf-8")
    out = []
    in_legend = False
    for line in text.splitlines():
        h2 = re.match(r"^##\s+(.+?)\s*$", line)
        if h2:
            in_legend = h2.group(1).strip().lower() == "legend"
            continue
        if in_legend:
            continue
        m = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if not m:
            continue
        body = m.group(1).strip()
        if not body or body.startswith("**"):
            continue
        # Example sub-bullets (e.g., "- Example: ...") are not patterns
        if body.startswith("Example:") or body.startswith("Example "):
            continue
        out.append(body)
    return out


def main() -> int:
    grammar_md = ROOT / "KnowledgeBank" / "grammar_n5.md"
    grammar_json = ROOT / "data" / "grammar.json"

    if not grammar_md.exists():
        print(f"ERROR: missing {grammar_md}", file=sys.stderr)
        return 1
    if not grammar_json.exists():
        print(f"ERROR: missing {grammar_json}", file=sys.stderr)
        return 1

    md_patterns = extract_md_pattern_lines(grammar_md)
    grammar = json.loads(grammar_json.read_text(encoding="utf-8"))
    json_patterns = [p["pattern"] for p in grammar.get("patterns", [])]

    print(f"KnowledgeBank/grammar_n5.md : {len(md_patterns):>4} pattern entries")
    print(f"data/grammar.json: {len(json_patterns):>4} pattern entries")

    if len(json_patterns) < len(md_patterns):
        missing = len(md_patterns) - len(json_patterns)
        print(
            f"INCOMPLETE: {missing} pattern(s) in KnowledgeBank/grammar_n5.md not yet authored "
            "in data/grammar.json"
        )
        return 1

    print("OK: pattern count meets coverage")
    return 0


if __name__ == "__main__":
    sys.exit(main())
