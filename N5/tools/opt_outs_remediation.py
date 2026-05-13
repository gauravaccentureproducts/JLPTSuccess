"""Close the 3 opt-outs from the native-teacher review cycle:

T-2 (Low, run-2): Improved listening speaker heuristic for the 3 items
  where the script uses announcer+content format. Detects:
    - Explicit prefix markers (男:/女:/学生:/先生:/etc.)
    - "X人が はなしています" framing to determine main-content gender
    - Position-based fallback (line 0 = framing narrator; subsequent
      = main-content gender; last = question prompt = narrator)

V-2 (Low, run-1): Slash-separated reading migration. 17 vocab entries
  have `reading` like "なに / なん". Split into `readings: ["なに", "なん"]`
  list field. Keep `reading` field set to the FIRST reading for
  backward compatibility with any code that reads it directly.

G-2 (Medium, run-1): Remove "(This pattern is also indexed as 'X' in
  another category)" parentheticals from explanation_en. The 31
  affected entries have FULL content — they're not stubs. The
  parenthetical was an artifact of a category-restructure. Replace with
  a clean `see_also: ["target_id"]` structured field.
"""
import json
import io
import sys
import re
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
LISTENING = "data/listening.json"
VOCAB = "data/vocab.json"
GRAMMAR_BAK = "data/grammar.json.bak_2026_05_13_opt_outs"
LISTENING_BAK = "data/listening.json.bak_2026_05_13_opt_outs"
VOCAB_BAK = "data/vocab.json.bak_2026_05_13_opt_outs"


# =====================================================================
# T-2: improved listening speaker heuristic
# =====================================================================

# Extended marker set: 男:/女:/学生:/先生:/客:/etc.
SPEAKER_PREFIXES = {
    "男:": "male", "男の人:": "male", "男１:": "male", "男2:": "male",
    "女:": "female", "女の人:": "female", "女１:": "female", "女2:": "female",
    "学生:": "student", "先生:": "teacher",
    "客:": "customer", "店員:": "clerk", "店員さん:": "clerk",
}


def detect_main_speaker_from_framing(script: str) -> str | None:
    """Inspect the script's first line for "X人が はなしています" framing.
    Returns 'male' / 'female' / None."""
    first_line = (script or "").split("\n", 1)[0]
    if "男の人" in first_line and ("はなして" in first_line or "聞きます" in first_line or "話して" in first_line):
        return "male"
    if "女の人" in first_line and ("はなして" in first_line or "聞きます" in first_line or "話して" in first_line):
        return "female"
    return None


def fix_t2():
    shutil.copy2(LISTENING, LISTENING_BAK)
    l_raw = json.load(open(LISTENING, encoding="utf-8"))
    updates = 0
    items_updated = 0
    for item in l_raw["items"]:
        lines = item.get("lines") or []
        if not lines:
            continue

        # Determine if this item has an actual speaker pattern beyond
        # what's already tagged.
        any_explicit = False
        for ln in lines:
            text = (ln.get("ja") or "").strip()
            for prefix in SPEAKER_PREFIXES:
                if text.startswith(prefix):
                    any_explicit = True
                    break

        # Detect main speaker from framing (announcer+content format)
        main_speaker = detect_main_speaker_from_framing(item.get("script_ja") or "")

        if not any_explicit and not main_speaker:
            continue  # nothing to refine

        # Reassign speakers
        item_changed = False
        for i, ln in enumerate(lines):
            if not isinstance(ln, dict):
                continue
            text = (ln.get("ja") or "").strip()
            new_speaker = None

            # Priority 1: explicit prefix
            for prefix, role in SPEAKER_PREFIXES.items():
                if text.startswith(prefix):
                    new_speaker = role
                    break

            # Priority 2: announcer+content framing (per-line by position)
            if new_speaker is None and main_speaker:
                is_first = i == 0
                # Question prompt typically appears at the end of a JLPT
                # listening item; detect by question marker.
                is_question = (text.endswith("ですか。") or text.endswith("か？") or
                               text.endswith("ですか") or
                               ("どんな" in text or "どこ" in text or "なに" in text
                                or "いつ" in text or "だれ" in text) and "ですか" in text)
                if is_first:
                    new_speaker = "narrator"  # announcer framing
                elif is_question and i == len(lines) - 1:
                    new_speaker = "narrator"  # question prompt
                else:
                    new_speaker = main_speaker

            if new_speaker and ln.get("speaker") != new_speaker:
                ln["speaker"] = new_speaker
                updates += 1
                item_changed = True

        if item_changed:
            items_updated += 1

    with open(LISTENING, "w", encoding="utf-8") as f:
        json.dump(l_raw, f, ensure_ascii=False, indent=2)
    print(f"T-2: {updates} speaker tags refined across {items_updated} items")


# =====================================================================
# V-2: slash-separated readings → readings[] list
# =====================================================================

def fix_v2():
    shutil.copy2(VOCAB, VOCAB_BAK)
    v_raw = json.load(open(VOCAB, encoding="utf-8"))
    migrated = 0
    for v in v_raw["entries"]:
        reading = v.get("reading") or ""
        if "/" not in reading:
            continue
        # Split on "/"; normalize whitespace
        parts = [p.strip() for p in reading.split("/") if p.strip()]
        if len(parts) >= 2:
            v["readings"] = parts
            v["reading"] = parts[0]  # keep primary for backward compat
            v["readings_provenance"] = "v2_migration_2026_05_13"
            migrated += 1
    with open(VOCAB, "w", encoding="utf-8") as f:
        json.dump(v_raw, f, ensure_ascii=False, indent=2)
    print(f"V-2: {migrated} vocab entries migrated to readings[] list")


# =====================================================================
# G-2: remove "(This pattern is also indexed as 'X')" parentheticals
# =====================================================================

PAREN_RE = re.compile(
    r"\s*\(This pattern is also indexed as '[^']+' in another category\.[^)]*\)\s*",
    flags=re.IGNORECASE,
)


def fix_g2():
    shutil.copy2(GRAMMAR, GRAMMAR_BAK)
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))
    cleaned = 0
    for p in g_raw["patterns"]:
        expl = p.get("explanation_en") or ""
        if "also indexed" not in expl:
            continue
        # Extract the see_also target ID before stripping
        m = re.search(r"also indexed as '([^']+)' in another category", expl)
        target = m.group(1) if m else None
        new_expl = PAREN_RE.sub("", expl).strip()
        if new_expl != expl:
            p["explanation_en"] = new_expl
            # Add structured see_also if a target was extracted
            if target:
                p.setdefault("see_also", []).append(target)
                # Deduplicate
                p["see_also"] = sorted(set(p["see_also"]))
            cleaned += 1
    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)
    print(f"G-2: {cleaned} explanation_en parentheticals removed; see_also fields populated")


def main():
    print("=" * 60)
    print("T-2: listening speaker heuristic refinement")
    print("=" * 60)
    fix_t2()
    print()
    print("=" * 60)
    print("V-2: slash-separated readings → readings[] list")
    print("=" * 60)
    fix_v2()
    print()
    print("=" * 60)
    print("G-2: clean explanation_en forwarding parentheticals")
    print("=" * 60)
    fix_g2()


if __name__ == "__main__":
    main()
