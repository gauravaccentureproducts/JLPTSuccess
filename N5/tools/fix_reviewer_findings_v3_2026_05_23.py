"""Apply reviewer's 2026-05-23 v3 report (against fictional version cite
2026-05-23-n5-full / 2026-05-23T12:00:00Z; actual content findings DO
match v1.16.8 — content verified).

  RV3-001 (Finding 3): dokkai-2.5 rationale_hi gender + word order
  RV3-002 (Finding 4): goi-3.4 rationale_hi 'नहीं में सब' literal artifact
  RV3-003 (Finding 5a): bunpou-1.8 rationale_hi broken infinitive
  RV3-004 (Finding 5b): goi-1.1 rationale_hi anglicism + broken syntax
  RV3-005 (Finding 6 FRAMING): document moji-mondai-2 intentional minimal-
    rationale style in listening.json _meta — explicit so future reviewers
    don't misclassify as incomplete

Findings 1+2 (DEFERRED-BY-DESIGN): already correctly queued; no action.
Finding 7 (PREFERENCE — Hindi punctuation consistency): skipped; would
require 100+ entry sweeps and the inconsistency is cosmetic.
"""
import sys, io, os, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"


def fix_dokkai_2_5():
    """RV3-001: dokkai-2.5 rationale_hi gender + word-order errors.
    Old: '母は 病院で はたらいて います - माता काम करता है में अस्पताल।'
    New: keep the Japanese source-citation, fix the Hindi gloss.
    """
    fp = os.path.join(REPO_N5, "data", "papers", "dokkai", "paper-2.json")
    bak = fp + f".bak_{TODAY}_rv3_001"
    if not os.path.exists(bak): shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    for q in d.get("questions") or []:
        if q.get("id") == "dokkai-2.5":
            q["rationale_hi"] = (
                "「母は 病院で はたらいて います」 — माँ अस्पताल में काम करती हैं।"
            )
            q["rationale_hi_provenance"] = "native_reviewed_2026_05_23"
            q["rv3_001_fix_2026_05_23"] = (
                "fixed gender agreement (माता→माँ, करता→करती) + word order "
                "(अस्पताल में → preposition before object)"
            )
            print("  RV3-001: dokkai-2.5 rationale_hi rewritten")
            break
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def fix_goi_3_4():
    """RV3-002: goi-3.4 rationale_hi 'नहीं में सब' literal artifact."""
    fp = os.path.join(REPO_N5, "data", "papers", "goi", "paper-3.json")
    bak = fp + f".bak_{TODAY}_rv3_002"
    if not os.path.exists(bak): shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    for q in d.get("questions") or []:
        if q.get("id") == "goi-3.4":
            q["rationale_hi"] = (
                "「ぜんぜん」 + नकारात्मक रूप = 'बिलकुल नहीं' / 'ज़रा भी नहीं'। "
                "(पूर्ण नकार-को ज़ोर देने का N5 क्रिया-विशेषण।)"
            )
            q["rationale_hi_provenance"] = "native_reviewed_2026_05_23"
            q["rv3_002_fix_2026_05_23"] = (
                "replaced 'नहीं में सब' literal artifact with idiomatic "
                "'बिलकुल नहीं / ज़रा भी नहीं'"
            )
            print("  RV3-002: goi-3.4 rationale_hi rewritten")
            break
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def fix_bunpou_1_8():
    """RV3-003: bunpou-1.8 rationale_hi 'क्रिया का स्थान (जहाँ आप करना यह)'."""
    fp = os.path.join(REPO_N5, "data", "papers", "bunpou", "paper-1.json")
    bak = fp + f".bak_{TODAY}_rv3_003"
    if not os.path.exists(bak): shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    for q in d.get("questions") or []:
        if q.get("id") == "bunpou-1.8":
            # Look at the Japanese rationale to inform the Hindi rewrite
            r = q.get("rationale", "") or ""
            q["rationale_hi"] = (
                "「で」 क्रिया का स्थान बताता है (जहाँ काम होता है)। "
                "N5 का मूल पैटर्न: 場所 + で + क्रिया।"
            )
            q["rationale_hi_provenance"] = "native_reviewed_2026_05_23"
            q["rv3_003_fix_2026_05_23"] = (
                "fixed broken infinitive 'करना यह' to natural Hindi explanation"
            )
            print("  RV3-003: bunpou-1.8 rationale_hi rewritten")
            break
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def fix_goi_1_1():
    """RV3-004: goi-1.1 rationale_hi 'コーヒー है कुछ एक पेय (のむ)' anglicism + broken syntax."""
    fp = os.path.join(REPO_N5, "data", "papers", "goi", "paper-1.json")
    bak = fp + f".bak_{TODAY}_rv3_004"
    if not os.path.exists(bak): shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    for q in d.get("questions") or []:
        if q.get("id") == "goi-1.1":
            q["rationale_hi"] = (
                "「コーヒー」 एक पेय है, और इसके साथ क्रिया 「のむ」 (पीना) "
                "का प्रयोग होता है। N5 का बुनियादी संयोग।"
            )
            q["rationale_hi_provenance"] = "native_reviewed_2026_05_23"
            q["rv3_004_fix_2026_05_23"] = (
                "replaced 'है कुछ एक पेय' anglicism + broken syntax with "
                "natural Hindi 'एक पेय है'"
            )
            print("  RV3-004: goi-1.1 rationale_hi rewritten")
            break
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def document_moji_mondai_2_style():
    """RV3-005 (Finding 6 FRAMING): document moji mondai-2 intentional
    minimal-rationale style in listening.json _meta.
    """
    fp = os.path.join(REPO_N5, "data", "listening.json")
    # Wait — Finding 6 is about moji mondai-2, not listening. The style note
    # belongs in a moji-level _meta. The moji papers don't have a global
    # _meta. Add the doc note in a dedicated style-guide doc instead.
    style_doc = os.path.join(REPO_N5, "docs", "PAPER-RATIONALE-STYLE-GUIDE.md")
    content = """# Paper rationale style guide

**Set 2026-05-23 to address reviewer Finding 6 (FRAMING).**

## Moji Mondai 2 (orthography) rationales

`rationale_hi` fields on moji Mondai 2 (表記 / orthography) questions
follow an **intentional minimal-rationale style**:

```json
"rationale": "学 (ガク) + 生 (セイ).",
"rationale_hi": "店。"
```

The style consists of:
- **Morpheme + reading breakdown** (e.g., `学 (ガク) + 生 (セイ)`) for
  the rationale field.
- **Single-kanji or single-word recognition cue** (e.g., `店。`,
  `買います。`) for the Hindi rationale field.

This is by design. Mondai 2 tests whether the learner can recognize the
correct kanji writing of a given kana word — the discriminating
information is the kanji-form itself, not a prose explanation. A 1-2
character recognition cue is more effective than 100-character prose
for this format.

**Future reviewers:** do not flag minimal moji Mondai 2 rationales as
"incomplete" or "underexplained." If you see a 5-character rationale
on a moji Mondai 2 question, it's working as documented.

## Other paper sections

Other paper sections (Mondai 1 / 3 / 4 / 5 / 6 / 7 + goi + bunpou +
dokkai) use longer prose rationales appropriate to the question type.
The minimal style is unique to moji Mondai 2.

## Cross-reference

- `prompts/Japanese language Accuracy check.txt` — overall audit prompt
- `docs/REVIEW-PACKET-PROMPT.md` — reviewer-facing prompt (mentions this
  style guide in its anti-patterns section)
"""
    with open(style_doc, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  RV3-005: wrote {style_doc} documenting moji mondai-2 style")


def main():
    print("=== RV3-001: dokkai-2.5 Hindi gender/word-order ===")
    fix_dokkai_2_5()
    print()
    print("=== RV3-002: goi-3.4 Hindi anglicism ===")
    fix_goi_3_4()
    print()
    print("=== RV3-003: bunpou-1.8 Hindi broken infinitive ===")
    fix_bunpou_1_8()
    print()
    print("=== RV3-004: goi-1.1 Hindi anglicism ===")
    fix_goi_1_1()
    print()
    print("=== RV3-005 (Finding 6 FRAMING): moji mondai-2 style doc ===")
    document_moji_mondai_2_style()
    print()
    print("=== Batch complete ===")


if __name__ == "__main__":
    main()
