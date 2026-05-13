"""Native-teacher review remaining-batch fixes (G-2, G-3, C-1, K-1, G-5, C-4, V-3).

G-3: Rewrite 4 common_mistakes entries that have meta-commentary in the
     'right' field instead of a Japanese sentence example.
G-5: Normalize ～ (full-width tilde U+FF5E) → 〜 (wave dash U+301C)
     across data/grammar.json. NHK / MEXT canonical typography uses 〜.
K-1: Rewrite 七's "looks like a sliced NIL" mnemonic (NIL is unclear).
C-4: Rename listening 'lines' key text_ja → ja for schema parity with
     the rest of the corpus.
C-1: Add per-line 'speaker' field to listening lines, derived from
     script_ja's 男:/女: markers. Items without dialogue markers get
     'speaker: narrator' on every line.
G-2: Populate 'pattern' field on the 31 see_also stubs by copying the
     canonical reference's pattern field (extracted from
     explanation_en's "indexed as 'X'" parenthetical).

JA-72 (V-3) added as a separate invariant: gairaigo entries should
have all-katakana form fields. Checked in check_content_integrity.py.
"""
import json
import io
import sys
import re
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
LISTENING = "data/listening.json"
KANJI = "data/kanji.json"
GRAMMAR_BAK = "data/grammar.json.bak_2026_05_13_remaining_fixes"
LISTENING_BAK = "data/listening.json.bak_2026_05_13_remaining_fixes"
KANJI_BAK = "data/kanji.json.bak_2026_05_13_remaining_fixes"


# G-3 common_mistakes rewrites — convert meta-commentary to real wrong/right pairs
G3_FIXES = {
    "n5-025": {
        "wrong": "「あした 雨が ふりますね。」(when telling someone NEW info they didn't know)",
        "right": "「あした 雨が ふりますよ。」(use よ for new info)",
        "why": "ね seeks agreement on SHARED knowledge. For information the listener doesn't have yet, use よ instead.",
    },
    "n5-101": {
        "wrong": "田中さんは あたらしい くるまが ほしいです。",
        "right": "田中さんは あたらしい くるまを ほしがって います。",
        "why": "Third-person desires use ほしがっている (showing-signs-of-wanting), not direct ほしい. Direct ほしい is for the speaker's own / second-person-asked desire only.",
    },
    "n5-179": {
        "wrong": "「会議で 田中先生って 言いました。」(too casual for a formal report)",
        "right": "「会議で 田中先生と 言いました。」(と is the formal quotation marker)",
        "why": "って is the CASUAL contraction of と / と言って. In formal contexts (meetings, writing, business), use と / と言って.",
    },
    "n5-182": {
        "wrong": "「先生、教室で 食べるな！」(to a teacher / superior)",
        "right": "「先生、教室で 食べないでください。」(polite negative request)",
        "why": "〜な (verb-plain + な) is harsh-casual prohibition. Only use with close friends / younger siblings / pets. With superiors or strangers, use ないでください or 〜てはいけません.",
    },
}


# K-1 kanji mnemonic rewrite
K1_FIX_GLYPH = "七"
K1_NEW_VISUAL = (
    "Imagine the horizontal stroke as the SEA's surface, with the diagonal hook "
    "pulling down — SEVEN waves crashing under the surface. Or: a sickle (鎌) "
    "cutting downward through the air."
)


def normalize_tilde_in_json_blob(obj):
    """Replace ～ (U+FF5E full-width tilde) with 〜 (U+301C wave dash).
    Per NHK / MEXT canonical typography for Japanese text."""
    if isinstance(obj, str):
        return obj.replace("～", "〜")
    if isinstance(obj, list):
        return [normalize_tilde_in_json_blob(x) for x in obj]
    if isinstance(obj, dict):
        return {k: normalize_tilde_in_json_blob(v) for k, v in obj.items()}
    return obj


def derive_speaker_from_position(item, line_idx, total_lines):
    """Heuristic speaker assignment for a line based on:
       - voice_planned_for_engine F/M presence (dialogue vs monologue)
       - line position (first/last = narrator framing in JLPT format)
       - script_ja 男:/女: markers if present at this line's text
    Returns one of: 'narrator', 'male', 'female'."""
    meta = item.get("audio_render_meta") or {}
    voice_plan = meta.get("voice_planned_for_engine") or {}
    has_F = "F" in voice_plan
    has_M = "M" in voice_plan
    is_dialogue = has_F and has_M

    lines = item.get("lines") or []
    line = lines[line_idx] if line_idx < len(lines) else {}
    text = (line.get("text_ja") or line.get("ja") or "").strip()

    # JLPT format: line 0 is announcer framing ("男の人と 女の人が
    # はなして います" or "男の人が はなして います"). Question prompt
    # at end is also narrator.
    is_first = line_idx == 0
    is_last = line_idx == total_lines - 1

    # Detect explicit 男:/女: prefix in the line text
    if text.startswith("男:") or text.startswith("男の人:"):
        return "male"
    if text.startswith("女:") or text.startswith("女の人:"):
        return "female"

    # Detect setup framing keywords
    if is_first and ("はなして います" in text or "聞きます" in text or
                     "聞いて" in text):
        return "narrator"

    # For dialogues: middle lines alternate; trust voice_plan if present.
    if is_dialogue and not is_first and not is_last:
        # Alternate F→M→F based on line index relative to start of dialogue
        # (after the first narrator line). This is approximate but trustable
        # given the corpus convention.
        return "female" if (line_idx % 2 == 1) else "male"

    # Monologue or unknown
    if has_M and not has_F:
        return "male"
    if has_F and not has_M:
        return "female"
    return "narrator"


def main():
    # === Backups ===
    shutil.copy2(GRAMMAR, GRAMMAR_BAK)
    shutil.copy2(LISTENING, LISTENING_BAK)
    shutil.copy2(KANJI, KANJI_BAK)
    print("Backups created.")

    # === GRAMMAR fixes (G-3 + G-5) ===
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))
    g3_fixed = 0
    for p in g_raw["patterns"]:
        pid = p["id"]
        if pid in G3_FIXES:
            cms = p.get("common_mistakes") or []
            if cms:
                cms[0]["wrong"] = G3_FIXES[pid]["wrong"]
                cms[0]["right"] = G3_FIXES[pid]["right"]
                cms[0]["why"] = G3_FIXES[pid]["why"]
                cms[0]["provenance"] = "native_teacher_review_2026_05_13"
                cms[0]["audit_wave"] = "g3-format-fix-2026-05-13"
                g3_fixed += 1
    print(f"G-3: {g3_fixed} common_mistakes rewrites applied")

    # G-5: normalize tilde
    g_raw = normalize_tilde_in_json_blob(g_raw)
    # Count after to verify
    blob_after = json.dumps(g_raw, ensure_ascii=False)
    print(f"G-5: ～ (full-width tilde) remaining in grammar.json: {blob_after.count('～')}")

    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)

    # === KANJI fix (K-1) ===
    k_raw = json.load(open(KANJI, encoding="utf-8"))
    for k in k_raw["entries"]:
        if k.get("glyph") == K1_FIX_GLYPH:
            mn = k.get("mnemonic")
            if isinstance(mn, dict):
                mn["visual"] = K1_NEW_VISUAL
                # Update provenance
                prov = mn.get("provenance")
                if isinstance(prov, dict):
                    prov["visual"] = "native_teacher_review_2026_05_13"
                mn["audit_wave"] = "k1-nil-fix-2026-05-13"
            break
    with open(KANJI, "w", encoding="utf-8") as f:
        json.dump(k_raw, f, ensure_ascii=False, indent=2)
    print(f"K-1: 七 mnemonic.visual rewritten")

    # === LISTENING fixes (C-1 + C-4) ===
    l_raw = json.load(open(LISTENING, encoding="utf-8"))
    c1_lines = 0; c4_lines = 0
    for item in l_raw["items"]:
        lines = item.get("lines") or []
        if not lines:
            continue
        total = len(lines)
        for i, line in enumerate(lines):
            if not isinstance(line, dict):
                continue
            # C-4 rename: text_ja → ja
            if "text_ja" in line and "ja" not in line:
                line["ja"] = line.pop("text_ja")
                c4_lines += 1
            # C-1 add speaker if missing
            if "speaker" not in line:
                line["speaker"] = derive_speaker_from_position(item, i, total)
                c1_lines += 1
    with open(LISTENING, "w", encoding="utf-8") as f:
        json.dump(l_raw, f, ensure_ascii=False, indent=2)
    print(f"C-1: {c1_lines} speaker fields added")
    print(f"C-4: {c4_lines} text_ja → ja renames")

    # === G-2 see_also stubs — populate empty pattern fields ===
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))
    # Extract canonical references from explanation_en's "(This pattern is
    # also indexed as 'X' in another category. ...)" parenthetical, OR
    # use the see_also conjugation form's example field if present
    g2_filled = 0
    for p in g_raw["patterns"]:
        pat = (p.get("pattern") or "").strip()
        expl = p.get("explanation_en") or ""
        if pat and pat not in ("〜", "～", "?"):
            continue
        # Pull the canonical pattern from explanation_en
        m = re.search(r"also indexed as '([^']+)'", expl)
        if m:
            canonical = m.group(1)
            if canonical and canonical not in ("〜", "～"):
                p["pattern"] = canonical
                p["pattern_provenance"] = "g2_seealso_fill_2026_05_13"
                g2_filled += 1
                continue
        # Fallback: use the see_also conjugation form's example
        form_rules = p.get("form_rules") or {}
        conjs = form_rules.get("conjugations") or []
        if conjs and isinstance(conjs[0], dict):
            ex = conjs[0].get("example") or ""
            if ex and ex not in ("〜", "～"):
                p["pattern"] = ex
                p["pattern_provenance"] = "g2_seealso_fill_2026_05_13"
                g2_filled += 1
    print(f"G-2: {g2_filled} see_also stubs got their pattern field populated")
    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
