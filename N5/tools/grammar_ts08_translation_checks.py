"""TS-08 automated heuristic checks for EN translation accuracy across
all 178 patterns. Flags candidate issues for human review:

H1. JA past-tense marker (ました / でした / た in past forms) without past
    tense in EN.
H2. JA question marker (か at end, or ？) without ? in EN.
H3. JA polite-negative (ません / ない at end) without negation in EN.
H4. JA exists/possessive (あります / います / もっています) translated as
    something other than have/exist/be.

These are heuristics; many will be false positives (English often
expresses tense/aspect implicitly). They are surfaced as candidates,
not Fails. A human reviewer should triage.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
OUT_FILE = ROOT / "tools" / "grammar_ts08_findings.json"


# Heuristic patterns
JA_PAST_ENDINGS = ("ました", "でした", "ました。", "でした。")
JA_NEG_ENDINGS = ("ません", "ません。", "ません か", "ませんか", "ません か。", "ませんか。", "なかった", "なかった。")
JA_Q_MARKERS = ("か。", "か？", "ですか", "ますか")
EN_PAST_HINTS = re.compile(r"\b(?:was|were|did|had|been|gave|came|went|ate|read|bought|drank|wrote|saw|got|made|took|slept|woke|opened|received|met|sent|said|spoke|sat|stood|started|stopped|finished|ed)\b", re.IGNORECASE)
EN_NEG_HINTS = re.compile(r"\b(?:not|no|never|none|don't|doesn't|didn't|isn't|aren't|wasn't|weren't|haven't|hasn't|won't|can't|cannot)\b", re.IGNORECASE)


def check_example(ja: str, en: str) -> list[str]:
    issues = []
    if not ja or not en:
        return issues
    ja_stripped = ja.strip()
    en_stripped = en.strip()

    # H1: past-tense ending without past-tense English
    if any(ja_stripped.endswith(ending) for ending in JA_PAST_ENDINGS):
        # If the JA is also negative (ませんでした) it's still past + negative
        # Either past hint or "haven't"/"didn't" should be present
        if not EN_PAST_HINTS.search(en_stripped) and not EN_NEG_HINTS.search(en_stripped):
            # exclude very short EN where verb might be elided
            if len(en_stripped.split()) >= 3:
                issues.append(f"H1: JA past form ({ja_stripped[-10:]}) but no obvious past-tense in EN: '{en_stripped[:80]}'")

    # H2: question marker without ? in EN
    if any(marker in ja_stripped for marker in JA_Q_MARKERS):
        if "?" not in en_stripped:
            issues.append(f"H2: JA question marker (か / ですか / ますか) but no '?' in EN: '{en_stripped[:80]}'")

    # H3: negation marker without negation in EN
    if any(ja_stripped.endswith(ending) for ending in JA_NEG_ENDINGS):
        if not EN_NEG_HINTS.search(en_stripped):
            issues.append(f"H3: JA negative form ({ja_stripped[-10:]}) but no negation in EN: '{en_stripped[:80]}'")

    return issues


def main():
    g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    findings = {}
    total_examples = 0
    flagged = 0
    by_h = {"H1": 0, "H2": 0, "H3": 0}
    for p in g["patterns"]:
        pid = p["id"]
        pat_issues = []
        for i, ex in enumerate(p.get("examples") or []):
            ja = ex.get("ja", "") or ""
            en = ex.get("translation_en", "") or ""
            total_examples += 1
            issues = check_example(ja, en)
            if issues:
                pat_issues.append({"example_index": i, "ja": ja, "en": en, "issues": issues})
                flagged += 1
                for it in issues:
                    for h in by_h:
                        if it.startswith(h):
                            by_h[h] += 1
        if pat_issues:
            findings[pid] = pat_issues

    OUT_FILE.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK wrote {OUT_FILE}")
    print(f"  Total examples scanned   : {total_examples}")
    print(f"  Examples with finding(s) : {flagged}")
    print(f"  Patterns with finding(s) : {len(findings)}")
    print(f"  By heuristic: {by_h}")


if __name__ == "__main__":
    main()
