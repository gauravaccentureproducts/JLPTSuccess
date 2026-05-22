"""Apply NTR-FU-004 / 005 / 006 / 007 in one combined script.

NTR-FU-004: move n5-045 from core_n5 to new `deprecated` bucket in
            n5_core_pattern_ids.json; update n5-045.contrasts[0].note.
NTR-FU-005: rewrite あなた examples [1] and [2] to align with usage_note.
NTR-FU-006: add applies_to='noun_of_reference' to じぶん counter.
NTR-FU-007: add `legacy_section_in_id: true` flag to おはし + えいが.

All provenance-stamped native_reviewed_2026_05_23.
"""
import sys, io, os, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"


def fix_ntr_fu_004():
    """n5-045 deprecated → move to `deprecated` bucket + update contrasts.note."""
    # 1) n5_core_pattern_ids.json: move n5-045 from core_n5 → deprecated bucket
    fp = os.path.join(REPO_N5, "data", "n5_core_pattern_ids.json")
    bak = fp + f".bak_{TODAY}_ntr_fu_004"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        c = json.load(f)
    if "n5-045" in c.get("core_n5", []):
        c["core_n5"].remove("n5-045")
    c["coreCount"] = len(c["core_n5"])
    # New deprecated bucket
    if "deprecated" not in c:
        c["deprecated"] = []
    if not any(isinstance(e, dict) and e.get("id") == "n5-045" for e in c["deprecated"]):
        c["deprecated"].append({
            "id": "n5-045",
            "canonical_id": "n5-017",
            "pattern": "何（なに／なん）",
            "rationale": (
                "Duplicate of n5-017 (canonical 何 pattern). Marked "
                "deprecated 2026-05-22 per NTR-002; moved out of "
                "core_n5 list 2026-05-23 per NTR-FU-004 follow-up. "
                "External references in questions.json / audio_manifest / "
                "pattern_markers / native-teacher-review docs still "
                "resolve to this ID for backward compatibility; UI "
                "renders an alias-link from the deprecated entry to "
                "the canonical."
            ),
        })
    c["deprecatedCount"] = len(c["deprecated"])
    # Update _meta.lastUpdated
    if isinstance(c.get("_meta"), dict):
        c["_meta"]["lastUpdated"] = "2026-05-23"
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print(f"  NTR-FU-004 A: n5-045 moved from core_n5 → deprecated; coreCount={c['coreCount']}, deprecatedCount={c['deprecatedCount']}")

    # 2) grammar.json: update n5-045.contrasts[0].note to point at deprecation lattice
    fp2 = os.path.join(REPO_N5, "data", "grammar.json")
    bak2 = fp2 + f".bak_{TODAY}_ntr_fu_004"
    if not os.path.exists(bak2):
        shutil.copy2(fp2, bak2)
    with open(fp2, "r", encoding="utf-8") as f:
        g = json.load(f)
    for p in g["patterns"]:
        if isinstance(p, dict) and p.get("id") == "n5-045":
            c = p.get("contrasts")
            if isinstance(c, list) and c and isinstance(c[0], dict):
                old_note = c[0].get("note", "")
                if "duplicate entry" in old_note.lower():
                    c[0]["note"] = (
                        "[Deprecated entry.] This pattern is the deprecated "
                        "alias of n5-017 (canonical 何 pattern). See "
                        "`deprecated: true` + `_alias_of: 'n5-017'` + "
                        "`deprecated_reason` on this entry. UI may filter "
                        "this from grammar TOC listings; external "
                        "references resolve here for backward "
                        "compatibility."
                    )
                    c[0]["note_provenance"] = "native_reviewed_2026_05_23"
                    print(f"  NTR-FU-004 B: n5-045.contrasts[0].note updated to point at deprecation lattice")
            break
    with open(fp2, "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=2)


def fix_ntr_fu_005():
    """あなた examples [1] and [2] aligned with usage_note."""
    fp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = fp + f".bak_{TODAY}_ntr_fu_005"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))
    for e in vl:
        if isinstance(e, dict) and e.get("form") == "あなた":
            exs = e.get("examples") or []
            if len(exs) >= 3:
                # Example [1]: 'あなたは がくせいですか。' → name+さん pattern
                exs[1]["ja"] = "木村さんは がくせいですか。"
                exs[1]["en"] = (
                    "Kimura-san, are you a student? (Note: Japanese uses name+さん "
                    "rather than あなた when addressing someone known. The bare "
                    "'are YOU a student?' phrasing with あなた sounds confrontational.)"
                )
                exs[1]["provenance"] = "native_reviewed_2026_05_23"
                # Example [2]: 'あなたは 何さいですか。' → form-filling context
                # where あなた IS appropriate per the usage_note
                exs[2]["ja"] = "あなたの 名前を ここに 書いて ください。"
                exs[2]["en"] = (
                    "Please write your name here. (Form-filling / generic-instruction "
                    "context — one of the few places where あなた is the natural choice "
                    "because the addressee is unspecified and the register is impersonal.)"
                )
                exs[2]["provenance"] = "native_reviewed_2026_05_23"
                print(f"  NTR-FU-005: あなた examples [1] + [2] rewritten")
            break
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)


def fix_ntr_fu_006():
    """じぶん counter applies_to='noun_of_reference' (reflexive doesn't count itself)."""
    fp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = fp + f".bak_{TODAY}_ntr_fu_006"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))
    for e in vl:
        if isinstance(e, dict) and e.get("form") == "じぶん" and (e.get("section") or "").startswith("1."):
            c = e.get("counter")
            if isinstance(c, dict) and "applies_to" not in c:
                c["applies_to"] = "noun_of_reference"
                c["note"] = (
                    "Counter 人/にん is shown here for cohort consistency but じぶん "
                    "is reflexive (oneself) and doesn't count itself. UI may choose "
                    "to suppress counter display for reflexive pronouns."
                )
                e["counter_provenance"] = "native_reviewed_2026_05_23"
                print(f"  NTR-FU-006: じぶん counter annotated applies_to='noun_of_reference'")
            break
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)


def fix_ntr_fu_007():
    """おはし + えいが: legacy_section_in_id flag (slug-immutable + section-field-authoritative)."""
    fp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = fp + f".bak_{TODAY}_ntr_fu_007"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))
    annotated = 0
    for e in vl:
        if not isinstance(e, dict): continue
        f_ = e.get("form")
        if f_ in ("おはし", "えいが"):
            e["legacy_section_in_id"] = True
            e["legacy_section_in_id_note"] = (
                "Entry ID embeds the original section slug; section field is "
                "authoritative for current classification. ID kept immutable to "
                "preserve external references (audio_manifest, questions.json, "
                "user localStorage, etc.). Section retag landed in NTR-005/006 "
                "(2026-05-22); slug-section-vs-field-section divergence flagged "
                "in NTR-FU-007 (2026-05-23)."
            )
            e["legacy_section_in_id_provenance"] = "native_reviewed_2026_05_23"
            annotated += 1
            print(f"  NTR-FU-007: {f_!r} flagged legacy_section_in_id=true")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print(f"  NTR-FU-007: {annotated} entries flagged")


def main():
    fix_ntr_fu_004()
    fix_ntr_fu_005()
    fix_ntr_fu_006()
    fix_ntr_fu_007()
    print()
    print(f"=== NTR-FU-004/005/006/007 batch applied ===")


if __name__ == "__main__":
    main()
