"""Apply reviewer's 2026-05-23 v1.16.7 review findings.

Findings 1-4 + 6 are REAL (defects); Finding 5 + 7 acknowledged.

  RV-001 (Finding 1): あなた ex[0].translation_en mismatch
  RV-002 (Finding 2): あなた ex[2].translation_en mismatch
  RV-003 (Finding 3): listening glossary entries not in script_ja
    (reviewer found 1, horizontal sweep found 3 total)
  RV-004 (Finding 4): listening line speaker tag mismatches
    (reviewer found 1; horizontal sweep found 18)
  RV-005 (Finding 5): かれ gloss — accepted reviewer's secondary
    suggestion: add explicit "modern conversational" marker
  RV-006 (Finding 6): q-0005 distractor_explanations_hi.で polish

Also drops the redundant `en` field on 3 あなた examples (only 3
entries had it from RP-002; canonical field is `translation_en`).
"""
import sys, io, os, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"


def fix_anata_translations():
    """RV-001 + RV-002 + drop redundant `en` field."""
    fp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = fp + f".bak_{TODAY}_rv_001_002"
    if not os.path.exists(bak): shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    entries = d if isinstance(d, list) else d.get("entries", [])
    for e in entries:
        if not isinstance(e, dict) or e.get("form") != "あなた": continue
        for i, ex in enumerate(e.get("examples") or []):
            if not isinstance(ex, dict): continue
            ja = ex.get("ja", "")
            # Update translation_en + drop the redundant `en` field (move
            # to translation_en if it had richer content)
            rich_en = ex.pop("en", None)
            if i == 0:
                # ja = "田中さんは どこから 来ましたか。"
                ex["translation_en"] = (
                    "Tanaka-san, where are you from? "
                    "(Note: Japanese uses name+さん rather than あなた when "
                    "addressing someone known. The bare 'where are YOU "
                    "from?' phrasing with あなた sounds confrontational.)"
                )
                ex["translation_en_provenance"] = "native_reviewed_2026_05_23"
                print(f"  RV-001: あなた ex[0] translation_en corrected")
            elif i == 1:
                # ja = "山田さんは がくせいですか。" — translation was already correct
                ex["translation_en"] = (
                    "Yamada-san, are you a student? "
                    "(Note: Japanese uses name+さん rather than あなた when "
                    "addressing someone known.)"
                )
                ex["translation_en_provenance"] = "native_reviewed_2026_05_23"
                print(f"  RV-001: あなた ex[1] translation_en enriched")
            elif i == 2:
                # ja = "あなたの 名前を ここに 書いて ください。"
                ex["translation_en"] = (
                    "Please write your name here. "
                    "(Form-filling / generic-instruction context — one of "
                    "the few places where あなた is the natural choice "
                    "because the addressee is unspecified and the register "
                    "is impersonal.)"
                )
                ex["translation_en_provenance"] = "native_reviewed_2026_05_23"
                print(f"  RV-002: あなた ex[2] translation_en corrected")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def fix_listening_glossary():
    """RV-003: drop irrelevant glossary entries (3 cases — horizontal sweep)."""
    fp = os.path.join(REPO_N5, "data", "listening.json")
    bak = fp + f".bak_{TODAY}_rv_003"
    if not os.path.exists(bak): shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    items = d.get("items") if isinstance(d, dict) else d
    # Per the horizontal scan: n5.listen.001 has あし, n5.listen.028 has いえ, n5.listen.049 has まがる
    to_remove = {
        "n5.listen.001": "あし",
        "n5.listen.028": "いえ",
        "n5.listen.049": "まがる",
    }
    removed = 0
    for it in items:
        if not isinstance(it, dict): continue
        iid = it.get("id")
        if iid not in to_remove: continue
        target_form = to_remove[iid]
        gloss = it.get("vocab_glossary") or []
        new_gloss = [g for g in gloss if not (isinstance(g, dict) and g.get("form") == target_form)]
        if len(new_gloss) < len(gloss):
            it["vocab_glossary"] = new_gloss
            it.setdefault("rv_003_fix_2026_05_23", []).append(
                f"removed irrelevant glossary entry {target_form!r} not present in script_ja"
            )
            removed += 1
            print(f"  RV-003: {iid} removed glossary entry {target_form!r}")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  RV-003 total: {removed} glossary entries removed")


def fix_listening_speakers():
    """RV-004: correct speaker tags based on 男：/女： prefix (18 cases)."""
    fp = os.path.join(REPO_N5, "data", "listening.json")
    bak = fp + f".bak_{TODAY}_rv_004"
    if not os.path.exists(bak): shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    items = d.get("items") if isinstance(d, dict) else d
    fixed = 0
    for it in items:
        if not isinstance(it, dict): continue
        lines = it.get("lines") or []
        item_fixed = []
        for i, ln in enumerate(lines):
            if not isinstance(ln, dict): continue
            ja = ln.get("ja", "")
            current = ln.get("speaker", "")
            new_speaker = None
            if ja.startswith("男："):
                new_speaker = "male"
            elif ja.startswith("女："):
                new_speaker = "female"
            # Don't touch narrator lines (no 男/女 prefix)
            if new_speaker and current != new_speaker:
                ln["speaker"] = new_speaker
                item_fixed.append((i, current, new_speaker))
                fixed += 1
        if item_fixed:
            it["rv_004_fix_2026_05_23"] = [
                f"line[{i}]: speaker {old!r} → {new!r} (matched prefix)"
                for i, old, new in item_fixed
            ]
            print(f"  RV-004: {it.get('id')} corrected {len(item_fixed)} speaker tags")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  RV-004 total: {fixed} speaker corrections")


def fix_kare_gloss():
    """RV-005: PREFERENCE — add 'modern conversational' marker to かれ + かのじょ
    gloss per reviewer's secondary suggestion."""
    fp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = fp + f".bak_{TODAY}_rv_005"
    if not os.path.exists(bak): shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    entries = d if isinstance(d, list) else d.get("entries", [])
    for e in entries:
        if not isinstance(e, dict): continue
        if e.get("form") == "かれ":
            e["gloss"] = (
                "boyfriend (primary in modern conversational Japanese); "
                "he, him (third-person pronoun, more formal/literary)"
            )
            e["gloss_provenance"] = "native_reviewed_2026_05_23"
            e["rv_005_fix_2026_05_23"] = "added 'modern conversational' marker per reviewer suggestion"
            print(f"  RV-005: かれ gloss enriched with 'modern conversational' marker")
        elif e.get("form") == "かのじょ":
            e["gloss"] = (
                "girlfriend (primary in modern conversational Japanese); "
                "she, her (third-person pronoun, more formal/literary)"
            )
            e["gloss_provenance"] = "native_reviewed_2026_05_23"
            e["rv_005_fix_2026_05_23"] = "added 'modern conversational' marker per reviewer suggestion"
            print(f"  RV-005: かのじょ gloss enriched with 'modern conversational' marker")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def fix_q0005_hindi():
    """RV-006: polish q-0005 distractor_explanations_hi.で
    ('फ़िट होता है' English-loanword → natural Hindi 'उपयुक्त नहीं है')."""
    fp = os.path.join(REPO_N5, "data", "questions.json")
    bak = fp + f".bak_{TODAY}_rv_006"
    if not os.path.exists(bak): shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    entries = d if isinstance(d, list) else d.get("questions", d.get("entries", []))
    for e in entries:
        if not isinstance(e, dict) or e.get("id") != "q-0005": continue
        de = e.get("distractor_explanations_hi") or {}
        if "で" in de:
            de["で"] = (
                "で क्रिया का स्थान या साधन सूचित करता है — यह वाक्य के "
                "विषय-सूचक के रूप में उपयुक्त नहीं है।"
            )
            e["rv_006_fix_2026_05_23"] = (
                "distractor_explanations_hi.で polished: 'फ़िट होता है' "
                "English-loanword → natural Hindi 'उपयुक्त नहीं है'"
            )
            print(f"  RV-006: q-0005 distractor_explanations_hi.で polished")
        break
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def main():
    print("=== RV-001 + RV-002: あなた translation_en fixes ===")
    fix_anata_translations()
    print()
    print("=== RV-003: listening glossary contamination ===")
    fix_listening_glossary()
    print()
    print("=== RV-004: listening speaker label corrections ===")
    fix_listening_speakers()
    print()
    print("=== RV-005: かれ + かのじょ gloss enrichment ===")
    fix_kare_gloss()
    print()
    print("=== RV-006: q-0005 Hindi polish ===")
    fix_q0005_hindi()
    print()
    print("=== Batch complete ===")


if __name__ == "__main__":
    main()
