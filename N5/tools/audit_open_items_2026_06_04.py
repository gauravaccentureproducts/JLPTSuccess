"""Generate a findings report for the remaining OPEN items
(OPEN-003 / 004 / 005 / 013) from the 2026-06-04 consolidated review.

The report is honest: it surfaces candidates a human native reviewer
should look at, but does NOT decide for them. Writes to
docs/vocab-review/N5-vocab-open-items-findings-2026-06-04.md.

Heuristics used (all conservative — recall-first, precision-second
because we'd rather flag too many for native review than too few):

  OPEN-003/004: particle_examples scan
    - patterns: 「を しる」, 「を する」, 「に いく」, 「と あう」, 「を ならう」
    - flag any particle_examples list where 3+ items share an identical
      shape suffix (suggests template generation)

  OPEN-005: gloss audit
    - gloss < 4 chars (suspiciously brief)
    - gloss contains 'and' or '/' or ',' AND no usage caveat in
      pragmatic_functions (multi-sense entry that may need
      disambiguation)
    - gloss longer than 90 chars (typically over-expanded)
    - gloss with unmarked English copula 'is/am/are' (likely
      mis-categorized as a sentence not a definition)

  OPEN-013: example_sentences audit
    - sentence > 35 chars (long for N5)
    - sentence contains kanji NOT in the N5 whitelist
    - sentence contains 4+ kanji in a row (likely off-N5 vocab block)
"""
from __future__ import annotations
import sys, io, json, re
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "vocab.json"
KANJI = ROOT / "data" / "kanji.json"
OUT = ROOT / "docs" / "vocab-review" / "N5-vocab-open-items-findings-2026-06-04.md"

PARTICLE_TEMPLATES = ["を しる", "を する", "に いく", "と あう", "を ならう"]


def main():
    v = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = v.get("entries", [])
    print(f"Loaded {len(entries)} vocab entries.")

    # Load N5 kanji whitelist
    n5_kanji = set()
    if KANJI.exists():
        kdata = json.loads(KANJI.read_text(encoding="utf-8"))
        kentries = kdata if isinstance(kdata, list) else (kdata.get("entries") or [])
        for k in kentries:
            g = k.get("glyph") or k.get("kanji") or ""
            if g:
                n5_kanji.add(g)
    print(f"N5 kanji whitelist: {len(n5_kanji)} characters")

    findings_o3 = []  # particle templates
    findings_o5 = []  # glosses
    findings_o13 = []  # examples

    for e in entries:
        eid = e.get("id", "")
        form = e.get("form", "")
        reading = e.get("reading", "")
        gloss = e.get("gloss", "") or ""

        # --- OPEN-003 / OPEN-004: particle_examples scan ---
        pe = e.get("particle_examples") or e.get("collocations") or []
        if isinstance(pe, list) and pe:
            template_hits = []
            for shape in PARTICLE_TEMPLATES:
                for p in pe:
                    if isinstance(p, str) and shape in p:
                        template_hits.append((shape, p))
            # also flag if 3+ examples share the same trailing 2-3 chars
            tails = defaultdict(list)
            for p in pe:
                if isinstance(p, str) and len(p) >= 3:
                    tails[p[-3:]].append(p)
            shared_tail = {t: ps for t, ps in tails.items() if len(ps) >= 3}

            if template_hits or shared_tail:
                findings_o3.append({
                    "id": eid, "form": form, "reading": reading,
                    "particle_examples": pe,
                    "template_hits": template_hits,
                    "shared_tail": shared_tail,
                })

        # --- OPEN-005: gloss audit ---
        gflags = []
        if gloss:
            if len(gloss) < 4:
                gflags.append("very-short")
            if len(gloss) > 90:
                gflags.append("very-long")
            has_disambig = bool(e.get("pragmatic_functions"))
            if any(sep in gloss for sep in (" and ", " / ", ", ")) and not has_disambig:
                gflags.append("multi-sense-no-disambig")
            # Unmarked sentence-shaped gloss
            if re.search(r"\bis\s|\bare\s|\bam\s", gloss.lower()):
                gflags.append("sentence-shaped")
        if gflags:
            findings_o5.append({
                "id": eid, "form": form, "reading": reading,
                "gloss": gloss, "flags": gflags,
            })

        # --- OPEN-013: example_sentences audit ---
        examples = e.get("examples") or []
        ex_flags = []
        for i, ex in enumerate(examples):
            ja = ex.get("ja", "") or ""
            f = []
            if len(ja) > 35:
                f.append(f"long-{len(ja)}c")
            # Find kanji (CJK Unified Ideographs U+4E00-U+9FFF)
            kanji_in_sent = [c for c in ja if "一" <= c <= "鿿"]
            off_n5 = [c for c in kanji_in_sent if c not in n5_kanji]
            if off_n5:
                f.append(f"off-N5-kanji({''.join(off_n5)})")
            # 4+ kanji in a row
            run_match = re.search(r"[一-鿿]{4,}", ja)
            if run_match:
                f.append(f"kanji-run({run_match.group()})")
            if f:
                ex_flags.append({"i": i, "ja": ja, "flags": f})
        if ex_flags:
            findings_o13.append({
                "id": eid, "form": form, "reading": reading,
                "issues": ex_flags,
            })

    # Write report
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        f.write("# N5 Vocabulary — Native-Review Open-Items Findings Report\n\n")
        f.write("Generated: 2026-06-04 (batch I).  \n")
        f.write("Purpose: surface mechanical-heuristic candidates for the 6 OPEN items the human native reviewer needs to close.\n\n")
        f.write("This file is **not** a list of confirmed bugs. It is a list of "
                "entries the heuristics flagged for human attention. A native reviewer "
                "should look at each, decide KEEP / REWRITE / DELETE, and apply the change "
                "directly to the corpus.\n\n")

        f.write("---\n\n")

        # OPEN-003 / OPEN-004
        f.write(f"## OPEN-003 / OPEN-004 — particle_examples candidates ({len(findings_o3)} entries)\n\n")
        f.write("Heuristic: entries whose `particle_examples` contain the reviewer's "
                "named template shapes (`を しる`, `を する`, `に いく`, `と あう`, "
                "`を ならう`) OR have 3+ examples sharing the same 3-character tail "
                "(template-generation signal).\n\n")
        if not findings_o3:
            f.write("_No candidates flagged. Either the patterns truly aren't there, or our heuristics are too narrow — a recall-pass by a native reviewer remains advised._\n\n")
        else:
            for fnd in findings_o3:
                f.write(f"### {fnd['form']} (`{fnd['id']}`)\n")
                if fnd["reading"] and fnd["reading"] != fnd["form"]:
                    f.write(f"reading: `{fnd['reading']}`  \n")
                f.write(f"current particle_examples: `{fnd['particle_examples']}`\n\n")
                if fnd["template_hits"]:
                    f.write("- template-shape hits:\n")
                    for shape, p in fnd["template_hits"]:
                        f.write(f"  - shape `{shape}` in `{p}`\n")
                if fnd["shared_tail"]:
                    f.write("- shared-tail signal (template-generation):\n")
                    for tail, ps in fnd["shared_tail"].items():
                        f.write(f"  - tail `{tail}`: `{ps}`\n")
                f.write("\n")

        # OPEN-005
        f.write(f"---\n\n## OPEN-005 — gloss audit ({len(findings_o5)} entries)\n\n")
        f.write("Heuristic: glosses that are very short (< 4 chars), very long (> 90 chars), "
                "multi-sense without disambiguation in `pragmatic_functions`, or "
                "sentence-shaped (containing 'is/am/are' — usually a sign that the gloss "
                "is a usage example, not a definition).\n\n")
        if not findings_o5:
            f.write("_No candidates flagged._\n\n")
        else:
            # Group by flag for easier review
            by_flag = defaultdict(list)
            for fnd in findings_o5:
                for fl in fnd["flags"]:
                    by_flag[fl].append(fnd)
            for fl in sorted(by_flag.keys()):
                f.write(f"### Flag: `{fl}` ({len(by_flag[fl])} entries)\n\n")
                for fnd in by_flag[fl][:30]:  # cap list length per flag for readability
                    f.write(f"- **{fnd['form']}** (`{fnd['id']}`): {fnd['gloss']!r}\n")
                if len(by_flag[fl]) > 30:
                    f.write(f"  - …and {len(by_flag[fl]) - 30} more (see raw data)\n")
                f.write("\n")

        # OPEN-013
        f.write(f"---\n\n## OPEN-013 — example sentences audit ({len(findings_o13)} entries)\n\n")
        f.write("Heuristic: example sentences that are longer than 35 characters, contain "
                "kanji not in the N5 whitelist, or have a run of 4+ consecutive kanji "
                "(likely off-N5 vocabulary block).\n\n")
        if not findings_o13:
            f.write("_No candidates flagged._\n\n")
        else:
            sample = findings_o13[:50]
            for fnd in sample:
                f.write(f"### {fnd['form']} (`{fnd['id']}`)\n")
                for iss in fnd["issues"]:
                    f.write(f"- example[{iss['i']}]: `{iss['ja']}` → flags: {iss['flags']}\n")
                f.write("\n")
            if len(findings_o13) > 50:
                f.write(f"_…and {len(findings_o13) - 50} more entries with flagged examples (see raw data)._\n\n")

        # Summary
        f.write("---\n\n## Summary\n\n")
        f.write(f"- OPEN-003 / OPEN-004 particle-examples candidates: **{len(findings_o3)} entries**\n")
        f.write(f"- OPEN-005 gloss-audit candidates: **{len(findings_o5)} entries**\n")
        f.write(f"- OPEN-013 example-sentence candidates: **{len(findings_o13)} entries**\n\n")
        f.write("All numbers are heuristic flags, not confirmed bugs. The human native "
                "reviewer should walk each list and decide per entry.\n")

    print(f"\nWrote {OUT}")
    print(f"  OPEN-003/004 candidates: {len(findings_o3)}")
    print(f"  OPEN-005 candidates: {len(findings_o5)}")
    print(f"  OPEN-013 candidates: {len(findings_o13)}")


if __name__ == "__main__":
    main()
