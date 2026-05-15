"""Reconcile vocab.json pitch_accent.drop against
data/n5_pitch_accent_reference.json (kanjium).

For each of the 1,009 vocab entries:
  - LOOKUP — find the reference entry by vocab_id
  - CLASSIFY current drop:
      * MATCH: current drop ∈ reference drops → confidence='high'
      * DISAGREE: not in reference drops → fix to reference[0],
        confidence='high', log the diff
      * NOT_FOUND: no reference entry → confidence='unverified',
        keep current value

Adds two new fields to each vocab pitch_accent object:
  - confidence: 'high' | 'medium' | 'unverified'
  - source: 'kanjium-<commit>-<match_kind>' | None

Writes a diff report to docs/PITCH-ACCENT-RECONCILIATION-2026-05-15.md.
"""
from __future__ import annotations
import json
from collections import OrderedDict, Counter
from pathlib import Path

VOCAB = Path("data/vocab.json")
REF = Path("data/n5_pitch_accent_reference.json")
REPORT = Path("docs/PITCH-ACCENT-RECONCILIATION-2026-05-15.md")


def main():
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    ref = json.loads(REF.read_text(encoding="utf-8"))
    ref_meta = ref["_meta"]
    ref_idx = {r["vocab_id"]: r for r in ref["entries"]}
    pin = ref_meta.get("source_pinned_commit", "?")[:8]

    stats = Counter()
    diffs = []  # for the report
    unverified_samples = []

    for e in vocab["entries"]:
        vid = e["id"]
        pa = e.get("pitch_accent")
        if not isinstance(pa, dict):
            # Skip entries without pitch_accent dict (shouldn't happen)
            continue
        current_drop = pa.get("drop")
        if current_drop is None:
            stats["NO_DROP_IN_VOCAB"] += 1
            continue
        ref_entry = ref_idx.get(vid)
        if ref_entry is None:
            # NOT_FOUND
            pa["confidence"] = "unverified"
            pa.pop("source", None)
            stats["NOT_FOUND"] += 1
            unverified_samples.append((vid, e.get("form"), e.get("reading"), current_drop))
            continue
        ref_drops = ref_entry["drops"]
        match_kind = ref_entry.get("match_kind", "exact")
        if current_drop in ref_drops:
            pa["confidence"] = "high"
            pa["source"] = f"kanjium-{pin}-{match_kind}"
            stats["MATCH"] += 1
        else:
            # DISAGREE — fix to reference[0]
            new_drop = ref_drops[0]
            diffs.append({
                "vocab_id": vid,
                "form": e.get("form"),
                "reading": e.get("reading"),
                "old_drop": current_drop,
                "new_drop": new_drop,
                "ref_drops": ref_drops,
                "match_kind": match_kind,
            })
            pa["drop"] = new_drop
            pa["confidence"] = "high"
            pa["source"] = f"kanjium-{pin}-{match_kind}"
            stats["DISAGREE_FIXED"] += 1

    VOCAB.write_text(json.dumps(vocab, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")

    # Write report
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Pitch-Accent Reconciliation — 2026-05-15",
        "",
        "## Methodology",
        "",
        "Cross-referenced every vocab.json `pitch_accent.drop` value against",
        f"the kanjium pitch-accent dataset (commit `{ref_meta.get('source_pinned_commit')}`,",
        "CC-BY-SA 4.0). For each vocab entry:",
        "",
        "- **MATCH:** current drop ∈ reference drops → `confidence: high`",
        "- **DISAGREE:** current drop not in reference → fix to reference[0] →",
        "  `confidence: high`, source pinned",
        "- **NOT_FOUND:** not in reference (gairaigo, function words, compounds",
        "  kanjium doesn't enumerate) → `confidence: unverified`, value kept as-is",
        "",
        "## Statistics",
        "",
        f"- **MATCH (no change):** {stats['MATCH']}",
        f"- **DISAGREE → fixed:** {stats['DISAGREE_FIXED']}",
        f"- **NOT_FOUND (unverified):** {stats['NOT_FOUND']}",
        f"- **Total processed:** {sum(stats.values())}",
        "",
        f"Reference coverage: {(stats['MATCH'] + stats['DISAGREE_FIXED'])*100 // sum(stats.values())}% of vocab entries",
        "have a kanjium-derived high-confidence value. Remaining",
        f"{stats['NOT_FOUND']*100 // sum(stats.values())}% are mostly loanwords (gairaigo) and function-word",
        "phrases not in the kanjium upstream.",
        "",
        "## Diff list — DISAGREE entries fixed to reference",
        "",
    ]
    if diffs:
        lines.append("| Vocab ID | Form | Reading | Old | New | All reference drops | Match kind |")
        lines.append("|----------|------|---------|-----|-----|---------------------|------------|")
        for d in sorted(diffs, key=lambda x: (x["form"] or "", x["reading"] or "")):
            ref_drops_str = ",".join(str(x) for x in d["ref_drops"])
            lines.append(
                f"| `{d['vocab_id']}` | {d['form']} | {d['reading']} | "
                f"{d['old_drop']} | **{d['new_drop']}** | {ref_drops_str} | "
                f"{d['match_kind']} |"
            )
    else:
        lines.append("(none)")
    lines.extend([
        "",
        "## Sample of NOT_FOUND (`confidence: unverified`) entries",
        "",
        "These are predominantly gairaigo (loanwords), compound expressions,",
        "and function-word entries not in the kanjium upstream. Their",
        "`pitch_accent.drop` values are kept as-is from LLM authoring and",
        "should be flagged for future native-human review.",
        "",
    ])
    lines.append("| Vocab ID | Form | Reading | Drop (kept) |")
    lines.append("|----------|------|---------|-------------|")
    for vid, form, reading, drop in unverified_samples[:30]:
        lines.append(f"| `{vid}` | {form} | {reading} | {drop} |")
    if len(unverified_samples) > 30:
        lines.append(f"| ... | ... | ... | (+{len(unverified_samples)-30} more) |")
    lines.extend([
        "",
        "## Caveats",
        "",
        "- **Source authority:** kanjium aggregates from EDICT/EDRDG and NHK",
        "  日本語発音アクセント新辞典. Some words have multiple attested drops",
        "  (e.g., 0 OR 2); the reference's `drops` array lists all and we",
        "  accept any as MATCH.",
        "- **Tokyo dialect bias:** kanjium reflects standard Tokyo pronunciation;",
        "  Kansai/Kyushu accent patterns differ entirely.",
        "- **Reading-only matches (`match_kind: by-reading`):** these used the",
        "  reading-only fallback because our vocab uses kana-only forms for",
        "  many words where kanjium has the kanji form. The drop set is the",
        "  UNION of all kanjium entries with that reading — wider but less",
        "  precise. JA-90 treats both `exact` and `by-reading` as valid",
        "  high-confidence sources.",
        "- **NOT_FOUND entries:** ~18% of vocab — kept as `unverified`. Future",
        "  native-human review pass should prioritize these.",
        "",
        "## Locked by",
        "",
        "CI invariant **JA-90** validates that every vocab `pitch_accent.drop`",
        "agrees with the reference (or has `confidence: unverified` set).",
        "",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"MATCH:           {stats['MATCH']}")
    print(f"DISAGREE_FIXED:  {stats['DISAGREE_FIXED']}")
    print(f"NOT_FOUND:       {stats['NOT_FOUND']}")
    print(f"Total:           {sum(stats.values())}")
    print(f"\nReport written: {REPORT}")
    print(f"Top 10 diffs:")
    for d in diffs[:10]:
        print(f"  {d['form']:8s} ({d['reading']:10s}): {d['old_drop']} -> {d['new_drop']} (ref: {d['ref_drops']})")


if __name__ == "__main__":
    main()
