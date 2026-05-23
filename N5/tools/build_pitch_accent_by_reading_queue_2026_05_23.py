"""Build the worklist for the broader pitch-accent native-speaker
verification pass.

Output: docs/PITCH-ACCENT-VERIFICATION-QUEUE-2026-05-23.md

Ranking:
  1. Sort by N5 vocab frequency proxy = vocab.json section number
     (lower section number = more foundational vocab = higher
     review priority). Section 1 (Pronouns/Self) ranks highest.
  2. Within section, sort by alphabetical kana order for
     determinism.

Filters:
  - match_kind == "by-reading" only (these are the ones with
    weakest provenance — kanjium-by-reading lookup, not exact
    headword match).
  - Skip entries already in the 2026-05-23 audit wave (3 entries
    already scaffolded).
"""
import sys, io, os, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALREADY_SCAFFOLDED = {"あなた", "みなさん", "きのう"}


def main():
    pa = json.load(open(os.path.join(REPO_N5, "data", "n5_pitch_accent_reference.json"), encoding="utf-8"))
    v = json.load(open(os.path.join(REPO_N5, "data", "vocab.json"), encoding="utf-8"))
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))

    section_by_form = {}
    for e in vl:
        if not isinstance(e, dict): continue
        f = e.get("form")
        s = e.get("section") or ""
        if f: section_by_form[f] = s

    SEC_RE = re.compile(r"^(\d+)\.")
    queue = []
    for e in pa["entries"]:
        if not isinstance(e, dict): continue
        if e.get("match_kind") != "by-reading": continue
        f = e.get("form")
        if not f: continue
        if f in ALREADY_SCAFFOLDED: continue
        sec = section_by_form.get(f, "")
        m = SEC_RE.match(sec)
        sec_num = int(m.group(1)) if m else 999
        queue.append({
            "form": f,
            "reading": e.get("reading"),
            "drops": e.get("drops"),
            "vocab_id": e.get("vocab_id"),
            "section": sec,
            "section_num": sec_num,
        })

    queue.sort(key=lambda x: (x["section_num"], x["form"]))

    out_path = os.path.join(REPO_N5, "docs", "PITCH-ACCENT-VERIFICATION-QUEUE-2026-05-23.md")
    lines = []
    lines.append("# Pitch-accent native-speaker verification queue")
    lines.append("")
    lines.append("**Built:** 2026-05-23 (commit pending) via")
    lines.append("`tools/build_pitch_accent_by_reading_queue_2026_05_23.py`.")
    lines.append("")
    lines.append("**Purpose:** ordered backlog for the broader native-speaker")
    lines.append("verification pass when a real human native speaker / certified")
    lines.append("Japanese-language teacher is engaged. The 2026-05-23 reviewer")
    lines.append("task scaffolded the audit-block schema on 3 canary entries")
    lines.append("(あなた / みなさん / きのう); the remaining `by-reading` entries")
    lines.append("below form the broader pass.")
    lines.append("")
    lines.append("**Ranking proxy:** vocab.json `section` field leading number")
    lines.append("(lower = more foundational; section 1 = Pronouns/Self, the")
    lines.append("first thing N5 learners encounter). Inside-section: alphabetical")
    lines.append("kana order for determinism.")
    lines.append("")
    lines.append("**Discipline (per F.44.7 / F.44.15 Shape 2 / NATIVE-SPEAKER-")
    lines.append("RE-VERIFICATION.md):** This file is a QUEUE, not a verification.")
    lines.append("LLM-authored values in `drops` come from kanjium-by-reading")
    lines.append("lookup — defensible but not authoritative against NHK 2016.")
    lines.append("Each entry needs a real human native-speaker pass before")
    lines.append("`match_kind` can be promoted to `exact`.")
    lines.append("")
    lines.append(f"**Queue size:** {len(queue)} entries (excluding the 3 canary")
    lines.append("entries already scaffolded in")
    lines.append("`n5_pitch_accent_reference.json` `_meta.audit_waves`).")
    lines.append("")
    lines.append("## Top-50 priority entries (section 1-10 vocabulary)")
    lines.append("")
    lines.append("| Rank | Form | Reading | Section | Drops | vocab_id |")
    lines.append("|---|---|---|---|---|---|")
    for i, q in enumerate(queue[:50], start=1):
        lines.append(f"| {i} | {q['form']} | {q['reading']} | {q['section']} | {q['drops']} | `{q['vocab_id']}` |")
    lines.append("")
    if len(queue) > 50:
        lines.append(f"## Remaining {len(queue)-50} entries (section 11+)")
        lines.append("")
        lines.append("Omitted from this view; see the full machine-readable")
        lines.append("output at `docs/PITCH-ACCENT-VERIFICATION-QUEUE-2026-05-23.json`")
        lines.append("for the complete sorted queue.")
        lines.append("")
    lines.append("## Verification protocol")
    lines.append("")
    lines.append("Per entry, the human verifier:")
    lines.append("")
    lines.append("1. Looks up the form in NHK 日本語発音アクセント新辞典 (2016).")
    lines.append("   Cites page number + drop notation (Maru notation: ⓪ ① ② ③).")
    lines.append("2. Locates the form in a listening passage where it occurs")
    lines.append("   (search `data/listening.json` `script_ja` for the form")
    lines.append("   string). Notes passage_id + approximate timestamp.")
    lines.append("3. Confirms whether the audio pitch matches the dictionary")
    lines.append("   value. If audio and dictionary disagree:")
    lines.append("   - Default to the audio (that's what the learner hears).")
    lines.append("   - Note the disagreement explicitly in `decision_note`.")
    lines.append("   - Keep the dictionary value as a non-primary alternate in")
    lines.append("     `verified_drops`.")
    lines.append("4. Fills in the audit block's `result_schema` fields on the")
    lines.append("   entry in `n5_pitch_accent_reference.json`.")
    lines.append("5. Flips `verifier_pending: false`.")
    lines.append("6. If verification is solid, promotes `match_kind` from")
    lines.append("   `by-reading` to `exact`.")
    lines.append("")
    lines.append("**Discipline guard rail:** JA-155 catches any entry where")
    lines.append("`match_kind: 'exact'` exists without a complete `audit` block")
    lines.append("(verifier_pending: false + result_schema populated). This")
    lines.append("prevents un-verified promotions from leaking back in.")
    lines.append("")
    out = "\n".join(lines)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote {out_path}")

    # Also dump machine-readable JSON
    json_path = os.path.join(REPO_N5, "docs", "PITCH-ACCENT-VERIFICATION-QUEUE-2026-05-23.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "built_at": "2026-05-23",
            "scope": "all match_kind=by-reading entries in n5_pitch_accent_reference.json, excluding 3 canary entries already scaffolded",
            "ranking_proxy": "vocab.json section leading number; inside-section alphabetical",
            "queue_size": len(queue),
            "queue": queue,
        }, f, ensure_ascii=False, indent=2)
    print(f"Wrote {json_path}")
    print()
    print(f"=== Queue size: {len(queue)} entries ===")
    print(f"Top section coverage:")
    from collections import Counter
    sc = Counter(q["section_num"] for q in queue)
    for s, n in sorted(sc.items())[:8]:
        print(f"  section {s}: {n} entries")


if __name__ == "__main__":
    main()
