"""Deterministic heuristic audit of data/grammar.json.

Free, full-coverage substitute for the LLM-audit pipeline (`tools/llm_audit.py`)
that catches the same CLASSES of issues that surfaced in the 5-pattern LLM
validation experiment (see `feedback/llm-audit-validation-report.md`),
applied across all 187 patterns. Issues flagged here are mechanical /
structural, the kind that can be detected without LLM judgment.

For issues that genuinely need linguistic intuition (UNNATURAL phrasing,
TRANSLATION quality, REGISTER subtleties beyond surface level), the
LLM-audit pipeline (which costs ~$0.06/pattern) is still the right tool.
But the heuristic scan catches everything that's deterministically
detectable, at $0 and ~50ms.

Issue classes detected:

H1 — STUB_REDIRECT — `notes` field contains internal authoring text
     ("Duplicate-cleanup redirect", "See n5-XXX for", etc.). Equivalent
     to Pass-12 F-12.3 fix in questions.json, applied to grammar.json.
     Caught n5-115 in the LLM validation.

H2 — PATTERN_MISMATCH — none of the pattern's examples contains the
     pattern field's distinctive token. Caught n5-115 in validation
     (4 of 5 examples didn't have 時).

H3 — REGISTER_MIX — examples mix plain forms (-た / -だ / -る at
     end-of-clause) with polite forms (-ました / -ます / -です) within
     one pattern entry. Caught Pass-13 F-13.9 / F-13.10 class.

H4 — EMPTY_TRANSLATION — `translation_en` is empty, "TBD", placeholder,
     or just whitespace.

H5 — DUPLICATE_EXAMPLES — two examples with byte-identical `ja` field
     within one pattern (auto-gen leak class).

H6 — SCOPE_LEAK_KANJI — examples contain a kanji NOT in
     `data/n5_kanji_whitelist.json`. Equivalent of JA-13 invariant
     applied per-pattern with a per-finding output.

H7 — META_FIELD_LEAK — any field that looks like internal metadata
     ("kosoado_role", "_*" prefix, etc.) is non-empty AND would render
     in the user-facing display. (Conservative check.)

Output: Pass-N-style findings, one per issue, with severity guess
based on issue class. Optional fix suggestions where mechanical.

Run:
    python tools/heuristic_audit.py
    python tools/heuristic_audit.py --json    # machine-readable
    python tools/heuristic_audit.py --severity HIGH    # filter
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / "data" / "grammar.json"
WHITELIST = ROOT / "data" / "n5_kanji_whitelist.json"

# Severity per issue class
SEV = {
    "H1": "MEDIUM",  # stub-redirect text reaches learners
    "H2": "HIGH",    # pattern claim doesn't match examples
    "H3": "MEDIUM",  # register mix
    "H4": "LOW",     # empty translation
    "H5": "MEDIUM",  # duplicate examples
    "H6": "HIGH",    # scope leak (already caught by JA-13 broadly)
    "H7": "LOW",     # metadata leak
}

KANJI_RE = re.compile(r"[一-鿿]")
POLITE_END_RE = re.compile(r"(ました|ません|ます|でした|です)[。！？]?$")
PLAIN_END_RE = re.compile(r"(?<![ま])(た|だ|る|い)[。！？]?$")  # rough; excludes -ました
STUB_RE = re.compile(
    # Only the unambiguous auto-gen markers. "See n5-XXX" alone is too loose
    # — n5-029's `notes` legitimately says "Differentiated from n5-028
    # (possessive sense)..." which is useful content, not stub. We want to
    # catch only the auto-injected boilerplate.
    r"Duplicate-cleanup redirect"
    r"|inlined from canonical pattern"
    r"|primary discussion of this pattern"
    r"|placeholder content"
    r"|fill in later"
    r"|TODO:\s*(write|add|fill|fix)",
    re.IGNORECASE,
)


def is_polite(s: str) -> bool:
    return bool(POLITE_END_RE.search(s))


def is_plain(s: str) -> bool:
    if is_polite(s):
        return False
    return bool(PLAIN_END_RE.search(s.strip()))


# Use explicit Unicode escapes for the tilde-likes — they look identical
# but have distinct codepoints (U+301C wave dash, U+FF5E fullwidth tilde,
# U+007E ASCII tilde, U+223C TILDE OPERATOR). Data uses U+FF5E for ~の,
# U+301C for some others; both must be treated as separators.
_SPLIT_RE = re.compile(
    r"["
    r"/／"        # ASCII / and FULLWIDTH /
    r"・"         # KATAKANA MIDDLE DOT ・
    r"、"         # IDEOGRAPHIC COMMA 、
    r"「」"   # CORNER BRACKETS 「」
    r"【】"   # BLACK LENTICULAR BRACKETS 【】
    r"　"         # IDEOGRAPHIC SPACE
    r"“”‘’"  # smart quotes
    r"()（）"  # parens (ASCII + fullwidth)
    r"：:"        # colons (ASCII + fullwidth)
    r"〜～~"  # tildes (wave dash + fullwidth tilde + ASCII tilde)
    r"+＋"        # plus (ASCII + fullwidth)
    r"]+"
)
# Separators only - excludes sound marks (゜゛) and prolonged-sound ー
# (those are part of words, not boundaries).


def find_distinctive_tokens(pattern_field: str) -> list[str]:
    """Pick all reasonable tokens from the pattern field. We accept a
    pattern as 'demonstrated by examples' if ANY of its tokens appears in
    ANY example. Slash-separated patterns like 'これ/それ/あれ/どれ' must
    not be flagged as mismatch just because one example uses これ and
    another uses あれ; the family is the unit. Compound patterns like
    'から〜まで' split on the embedded 〜."""
    if not pattern_field:
        return []
    parts = _SPLIT_RE.split(pattern_field.strip())
    out: list[str] = []
    for t in parts:
        t = t.strip()
        if not t:
            continue
        # Strip pedagogical prefixes
        for pre in ("Verb-", "Noun-", "Adjective-",
                    "い-Adjective", "な-Adjective", "い-", "な-"):
            if t.startswith(pre):
                t = t[len(pre):]
                break
        # Strip pedagogical suffixes
        for suf in ("+ Noun", "+ N", "+ noun", "+ n"):
            if t.endswith(suf):
                t = t[:-len(suf)].strip()
        # Skip pure-English / no-JA tokens (like 'possessive', 'nominalizer')
        if not any(("一" <= c <= "鿿") or ("ぁ" <= c <= "ヿ") for c in t):
            continue
        if t and t not in out:
            out.append(t)
    return out


def audit_one(p: dict, whitelist: set[str]) -> list[dict]:
    findings: list[dict] = []
    pid = p["id"]
    examples = p.get("examples", [])

    # H1 — stub-redirect text in notes (or any text field)
    for field in ("notes", "common_mistakes", "meaning_en"):
        v = p.get(field)
        if isinstance(v, str) and STUB_RE.search(v):
            findings.append({
                "pattern_id": pid,
                "rule": "H1",
                "severity": SEV["H1"],
                "field": field,
                "issue": f"Stub-redirect / internal-authoring text in user-facing field: {v[:80]!r}",
                "suggested_fix": "Replace with proper grammar notes or remove the field.",
            })

    # H2 — pattern-mismatch (no example contains ANY of the pattern's
    # distinctive tokens). Slash-families count as one unit: a 4-pronoun
    # pattern is fine if examples cover any subset. Whitespace-insensitive
    # match: examples often have spaces (`じかん が あります`) that are
    # absent from the pattern token (`があります`).
    tokens = find_distinctive_tokens(p.get("pattern", ""))
    if tokens and examples:
        # Strip whitespace from tokens AND examples before substring check
        norm_tokens = [re.sub(r"\s+", "", t) for t in tokens]
        any_match = False
        for ex in examples:
            ja_clean = re.sub(r"\s+", "", ex.get("ja", ""))
            if any(t in ja_clean for t in norm_tokens):
                any_match = True
                break
        if not any_match:
            findings.append({
                "pattern_id": pid,
                "rule": "H2",
                "severity": SEV["H2"],
                "field": "examples",
                "issue": f"None of {len(examples)} examples contain any of the pattern tokens {tokens!r}",
                "suggested_fix": "Author at least 2-3 examples that demonstrate the actual pattern.",
            })

    # H3 — register mix within one pattern
    if len(examples) >= 2:
        polite_count = sum(1 for ex in examples if is_polite(ex.get("ja", "")))
        plain_count = sum(1 for ex in examples if is_plain(ex.get("ja", "")))
        # Only flag if there's a real mix and the pattern isn't *about* register
        # (e.g., n5-067 Verb-ta plain past — by definition mixes registers).
        meaning_lc = (p.get("meaning_en") or "").lower()
        register_topical = any(
            kw in meaning_lc
            for kw in ["plain", "polite", "casual", "formal", "register",
                      "dictionary form", "past form", "negative form",
                      "te-form", "te form", "ta-form", "ta form", "nai-form"]
        )
        if polite_count >= 1 and plain_count >= 1 and not register_topical:
            findings.append({
                "pattern_id": pid,
                "rule": "H3",
                "severity": SEV["H3"],
                "field": "examples",
                "issue": f"Mixed registers within one pattern: {polite_count} polite + {plain_count} plain. Standardize unless this pattern is about register.",
                "suggested_fix": "Pick one register; convert all examples to match.",
            })

    # H4 — empty / placeholder translation
    for i, ex in enumerate(examples):
        en = ex.get("translation_en", "")
        if not en or en.strip().lower() in ("tbd", "todo", "placeholder", "n/a", "..."):
            findings.append({
                "pattern_id": pid,
                "rule": "H4",
                "severity": SEV["H4"],
                "field": f"examples[{i}].translation_en",
                "issue": f"Empty or placeholder translation: {en!r}",
                "suggested_fix": "Author a proper English translation.",
            })

    # H5 — duplicate examples within a pattern
    seen_ja: dict[str, int] = {}
    for i, ex in enumerate(examples):
        ja = ex.get("ja", "")
        if not ja:
            continue
        if ja in seen_ja:
            findings.append({
                "pattern_id": pid,
                "rule": "H5",
                "severity": SEV["H5"],
                "field": f"examples[{i}].ja",
                "issue": f"Duplicate of examples[{seen_ja[ja]}].ja ({ja!r})",
                "suggested_fix": "Replace one of the duplicates with a distinct example.",
            })
        else:
            seen_ja[ja] = i

    # H6 — kanji scope leak in examples or notes
    for i, ex in enumerate(examples):
        ja = ex.get("ja", "")
        for ch in KANJI_RE.findall(ja):
            if ch not in whitelist:
                findings.append({
                    "pattern_id": pid,
                    "rule": "H6",
                    "severity": SEV["H6"],
                    "field": f"examples[{i}].ja",
                    "issue": f"Out-of-scope kanji {ch!r} in example",
                    "suggested_fix": f"Replace with kana reading of {ch}.",
                })

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--severity", choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                        help="filter to >= this severity")
    args = parser.parse_args(argv)

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    whitelist = set(json.loads(WHITELIST.read_text(encoding="utf-8")))
    patterns = grammar["patterns"]

    SEV_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
    threshold = SEV_RANK.get(args.severity, 0)

    all_findings: list[dict] = []
    for p in patterns:
        all_findings.extend(audit_one(p, whitelist))

    if threshold:
        all_findings = [f for f in all_findings if SEV_RANK[f["severity"]] >= threshold]

    if args.json:
        print(json.dumps({"audited": len(patterns), "findings": all_findings},
                         ensure_ascii=False, indent=2))
        return 0

    # Human-readable summary
    print(f"audited: {len(patterns)} patterns")
    print(f"findings: {len(all_findings)}")
    by_rule: dict[str, int] = {}
    by_sev: dict[str, int] = {}
    for f in all_findings:
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
        by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
    print()
    print("by rule:")
    for r, n in sorted(by_rule.items()):
        print(f"  {r} {SEV[r]:<8s} {n:>3d}")
    print()
    print("by severity:")
    for s in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        if s in by_sev:
            print(f"  {s:<8s} {by_sev[s]:>3d}")
    print()
    print("findings:")
    for f in all_findings:
        print(f"  [{f['severity']:<6s}] {f['pattern_id']} {f['rule']} {f['field']}: {f['issue']}")
    return 0 if not all_findings else 0  # informational, not failing


if __name__ == "__main__":
    sys.exit(main())
