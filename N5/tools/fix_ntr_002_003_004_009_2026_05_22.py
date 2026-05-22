"""Close S1 remaining bugs:
  NTR-002 (BUG-162): n5-045 duplicate of n5-017 → mark deprecated
  NTR-003 (BUG-163): かれ/かのじょ glosses inverted → flip primary
  NTR-004 (BUG-164): あなた needs usage warning → add note + new example
  NTR-009 (BUG-169): Hindi gloss sync for boyfriend/girlfriend → mirror EN fix

All four bundled because NTR-003 and NTR-009 are paired (same field
edit), and NTR-002/004 are independent but small data-edits in the
same vocab/grammar files."""
import sys, io, os, shutil, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_22"


def backup(fp, tag):
    bak = fp + f".bak_{TODAY}_{tag}"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)


def main():
    # --- NTR-002: deprecate n5-045 (alias of n5-017) ---
    gfp = os.path.join(REPO_N5, "data", "grammar.json")
    backup(gfp, "ntr_002")
    with open(gfp, "r", encoding="utf-8") as f:
        g = json.load(f)
    gl = g.get("patterns", g)
    n5_045_idx = None
    n5_017_idx = None
    for i, e in enumerate(gl):
        if e.get("id") == "n5-045":
            n5_045_idx = i
        elif e.get("id") == "n5-017":
            n5_017_idx = i
    if n5_045_idx is not None:
        e = gl[n5_045_idx]
        e["deprecated"] = True
        e["deprecated_reason"] = "Duplicate of n5-017 (canonical 何 pattern). Marked deprecated 2026-05-22 per NTR-002. UI grammar TOC filters this entry out; external references (questions.json, audio_manifest, etc.) still resolve to this ID for backward compatibility."
        # Keep _alias_of pointing to n5-017
        e["_alias_of"] = "n5-017"
        print(f"  n5-045: marked deprecated=True, _alias_of=n5-017")
    if n5_017_idx is not None:
        e = gl[n5_017_idx]
        # Clear the reverse alias — canonical entry shouldn't point back at deprecated alias
        if e.get("_alias_of") == "n5-045":
            del e["_alias_of"]
            print(f"  n5-017: removed reverse _alias_of (was pointing to deprecated n5-045)")
    with open(gfp, "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=2)

    # --- NTR-003 + NTR-009: flip かれ/かのじょ glosses, sync Hindi ---
    vfp = os.path.join(REPO_N5, "data", "vocab.json")
    backup(vfp, "ntr_003_004_009")
    with open(vfp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))

    REGLOSSES = {
        "かれ": {
            "gloss": "boyfriend (primary); he, him (third-person pronoun, more formal/literary)",
            "gloss_hi": "बॉयफ्रेंड (प्राथमिक अर्थ); वह (पुरुष, औपचारिक/साहित्यिक सर्वनाम के रूप में)",
        },
        "かのじょ": {
            "gloss": "girlfriend (primary); she, her (third-person pronoun, more formal/literary)",
            "gloss_hi": "गर्लफ्रेंड (प्राथमिक अर्थ); वह (महिला, औपचारिक/साहित्यिक सर्वनाम के रूप में)",
        },
    }

    for entry in vl:
        if not isinstance(entry, dict): continue
        form = entry.get("form")
        if form in REGLOSSES:
            old_g = entry.get("gloss")
            old_h = entry.get("gloss_hi")
            entry["gloss"] = REGLOSSES[form]["gloss"]
            entry["gloss_hi"] = REGLOSSES[form]["gloss_hi"]
            entry["gloss_provenance"] = "native_reviewed_2026_05_22"
            entry["gloss_hi_provenance"] = "native_reviewed_2026_05_22"
            print(f"  {form}: gloss {old_g[:40]!r} -> {REGLOSSES[form]['gloss'][:40]!r}")
            print(f"  {form}: gloss_hi {old_h!r} -> {REGLOSSES[form]['gloss_hi'][:60]!r}")

    # --- NTR-004: あなた usage warning + replace example [0] ---
    for entry in vl:
        if not isinstance(entry, dict): continue
        if entry.get("form") == "あなた":
            # Add usage_note + revise gloss to include caveat
            entry["gloss"] = "you (use with caution — Japanese typically uses the person's name + さん or drops the subject entirely)"
            entry["gloss_hi"] = "आप (सावधानी से प्रयोग करें — जापानी में आमतौर पर व्यक्ति का नाम + さん का प्रयोग किया जाता है, या विषय छोड़ दिया जाता है)"
            entry["usage_note"] = "あなた is distant or formal, or (from a wife to a husband) intimate. It is NOT the normal way to address someone you know — use their name + さん, or drop the subject. Appropriate contexts: form-filling, wedding vows, lyrics, addressing strangers respectfully."
            entry["usage_note_hi"] = "あなた का प्रयोग दूरी या औपचारिकता दर्शाता है, या (पत्नी से पति को) आत्मीयता। यह किसी परिचित को संबोधित करने का सामान्य तरीका नहीं है — उनके नाम + さん का प्रयोग करें, या विषय छोड़ दें। उपयुक्त संदर्भ: फ़ॉर्म भरना, विवाह की शपथ, गीत, अजनबियों को सम्मानपूर्वक संबोधित करना।"
            entry["gloss_provenance"] = "native_reviewed_2026_05_22"
            entry["gloss_hi_provenance"] = "native_reviewed_2026_05_22"
            entry["usage_note_provenance"] = "native_reviewed_2026_05_22"
            # Replace example [0] from "あなたは どなたですか。" (survey-form register)
            # with name-based address showing the typical alternative
            examples = entry.get("examples") or []
            if examples and isinstance(examples[0], dict):
                old_ja = examples[0].get("ja")
                examples[0]["ja"] = "田中さんは どこから 来ましたか。"
                examples[0]["en"] = "Tanaka-san, where are you from? (Note: Japanese uses name+さん rather than あなた when addressing someone you know.)"
                examples[0]["provenance"] = "native_reviewed_2026_05_22"
                examples[0]["usage_demo"] = "name_based_address_alternative"
                print(f"  あなた: example[0] {old_ja!r} -> {examples[0]['ja']!r} (name-based address alternative)")
            # Keep examples [1] and [2] (form-filling-appropriate uses of あなた); but bump provenance
            for i in (1, 2):
                if i < len(examples) and isinstance(examples[i], dict):
                    examples[i]["usage_context"] = "anata_appropriate_register"  # form-filling/written
            entry["examples"] = examples
            print(f"  あなた: gloss + usage_note + example[0] updated")
            break

    with open(vfp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)

    print()
    print("=== Done ===")
    print("  NTR-002: n5-045 deprecated; n5-017 reverse alias cleared")
    print("  NTR-003: かれ/かのじょ glosses re-ordered (boyfriend/girlfriend primary)")
    print("  NTR-009: Hindi glosses for かれ/かのじょ synced (same commit as NTR-003)")
    print("  NTR-004: あなた gloss + usage_note added; example[0] re-pointed to name-based address")


if __name__ == "__main__":
    main()
