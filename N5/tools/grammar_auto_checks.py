"""Run automated objective checks across all 178 patterns. Outputs a
findings JSON keyed by pattern_id -> {ts_id -> [issue, issue, ...]}.
These findings layer under the human reviewer's content judgments."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IN_FILE = ROOT / "tools" / "grammar_review_input.json"
OUT_FILE = ROOT / "tools" / "grammar_auto_findings.json"

# Patterns that legitimately don't have a clear single string-pattern
# present in JA examples (they're sentence-final particles, multi-form
# patterns, etc.) — skip the "pattern-in-example" check for these.
SKIP_PATTERN_PRESENCE = set()


def normalize(s: str) -> str:
    return re.sub(r"\s+", "", s or "")


def main():
    patterns = json.loads(IN_FILE.read_text(encoding="utf-8"))
    findings = {}
    counts = {"TS-02": 0, "TS-03": 0, "TS-05": 0, "TS-08": 0, "TS-09": 0}

    for p in patterns:
        pid = p["id"]
        pat_text = normalize(p.get("pattern", ""))
        f = {"TS-02": [], "TS-03": [], "TS-05": [], "TS-08": [], "TS-09": []}

        # TS-02 + TS-03 + TS-09: empty / missing data.
        # BUG-011: register-variant entries are a separate schema (kind=register_variant,
        # carries form_a/form_b instead of wrong/right). They are NOT empty —
        # both forms are valid, no wrong/right contrast. Skip them.
        for i, m in enumerate(p.get("common_mistakes") or []):
            if m.get("kind") == "register_variant":
                continue
            if not (m.get("wrong") or "").strip() or not (m.get("right") or "").strip():
                f["TS-03"].append(f"common_mistakes[{i}]: empty wrong or right field")
            if not (m.get("why") or "").strip():
                f["TS-09"].append(f"common_mistakes[{i}]: empty 'why' commentary")
        for i, w in enumerate(p.get("wrong_corrected_pair") or []):
            if w.get("kind") == "register_variant":
                continue
            if not (w.get("wrong") or "").strip() or not (w.get("correct") or "").strip():
                f["TS-03"].append(f"wrong_corrected_pair[{i}]: empty wrong or correct field")
            if not (w.get("why") or "").strip():
                f["TS-09"].append(f"wrong_corrected_pair[{i}]: empty 'why' commentary")

        # TS-08: example with EN translation missing
        for i, ex in enumerate(p.get("examples") or []):
            if not (ex.get("en") or "").strip():
                f["TS-08"].append(f"examples[{i}]: empty EN translation")
            if not (ex.get("ja") or "").strip():
                f["TS-02"].append(f"examples[{i}]: empty JA field")

        # TS-05: pattern-presence sanity. Strip kana brackets / kanji
        # variants; we just want SOMETHING from the pattern label to
        # appear in each example.
        if pat_text and pid not in SKIP_PATTERN_PRESENCE:
            # Strip wave dash and parentheses for matching
            tokens = re.split(r"[／/〜～()]+", p.get("pattern", ""))
            tokens = [normalize(t) for t in tokens if normalize(t)]
            if tokens:
                misses = 0
                for ex in (p.get("examples") or []):
                    ja_norm = normalize(ex.get("ja", ""))
                    if not any(t in ja_norm for t in tokens):
                        misses += 1
                if misses and (p.get("examples") or []):
                    pct = misses / len(p["examples"]) * 100
                    if pct > 40:  # only flag if MORE THAN 40% of examples don't visibly contain the pattern
                        f["TS-05"].append(f"{misses}/{len(p['examples'])} examples don't visibly contain any of: {tokens}")

        # Compact: only keep ts_ids with at least one finding
        f = {k: v for k, v in f.items() if v}
        if f:
            findings[pid] = f
            for k in f:
                counts[k] = counts.get(k, 0) + 1

    OUT_FILE.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK wrote {OUT_FILE}  ({len(findings)} patterns with auto-findings)")
    print(f"  by TS: {counts}")


if __name__ == "__main__":
    main()
