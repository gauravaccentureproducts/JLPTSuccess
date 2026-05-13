"""Accuracy-audit run-1 fixes — F-1 + F-2 + F-3.

F-1 CRITICAL: n5.listen.028 had correctAnswer=しつれいします for a
  友だち (friend) context, but おじゃまします is canonical for a
  friend's house. The item's own cultural_context contradicted its
  correctAnswer. Rewrite the prompt to a formal context (entering
  a teacher's room) where しつれいします IS canonical.

F-2 MINOR: All 106 kanji entries store on-yomi in hiragana. Standard
  pedagogical convention is katakana for on-yomi, hiragana for kun-
  yomi (Genki I / Minna no Nihongo / dictionaries). Convert the
  display field; keep audio file paths (which include hiragana
  filenames) intact via the audio_yomi schema's separate `reading`
  and `audio` keys.

F-3 MINOR: n5.read.017 has topic='schedule' but content is a café
  menu. Update to topic='food'.
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

LISTENING = "data/listening.json"
READING = "data/reading.json"
KANJI = "data/kanji.json"
LISTENING_BAK = "data/listening.json.bak_2026_05_13_accuracy_audit"
READING_BAK = "data/reading.json.bak_2026_05_13_accuracy_audit"
KANJI_BAK = "data/kanji.json.bak_2026_05_13_accuracy_audit"


# Hiragana → Katakana conversion table for on-yomi display.
# Range U+3041..U+3096 (hiragana) maps to U+30A1..U+30F6 (katakana).
def kana_to_katakana(s: str) -> str:
    if not s:
        return s
    out = []
    for ch in s:
        code = ord(ch)
        if 0x3041 <= code <= 0x3096:
            out.append(chr(code + 0x60))
        else:
            out.append(ch)
    return "".join(out)


def fix_f1():
    """Rewrite n5.listen.028 to a formal teacher's-room context."""
    shutil.copy2(LISTENING, LISTENING_BAK)
    l_raw = json.load(open(LISTENING, encoding="utf-8"))
    for li in l_raw["items"]:
        if li.get("id") != "n5.listen.028":
            continue
        # Update prompt + title + script to teacher's-room context
        li["title_ja"] = "先生の へやに 入る"
        li["prompt_ja"] = "先生の へやに 入ります。何と 言いますか。"
        li["script_ja"] = "先生の へやに 入ります。何と 言いますか。"
        # Choices stay; correctAnswer しつれいします is correct here
        li["explanation_en"] = (
            "しつれいします is the canonical phrase when entering a "
            "teacher's, superior's, or formal context room. ただいま is "
            "for returning to YOUR own home. For a friend's casual home, "
            "おじゃまします is used (see n5.listen.038)."
        )
        li["cultural_context"] = (
            "Entering a teacher's room or superior's office: しつれいします "
            "('I beg your pardon' / 'excuse me for intruding') — said when "
            "entering and again when leaving. For casual contexts (friend's "
            "home), おじゃまします is the equivalent. Distinguishing the two "
            "registers is a core N5 pragmatics skill."
        )
        li["audit_wave"] = "accuracy-audit-f1-fix-2026-05-13"
        print(f"  F-1: rewrote n5.listen.028 to teacher's-room context")
        break
    with open(LISTENING, "w", encoding="utf-8") as f:
        json.dump(l_raw, f, ensure_ascii=False, indent=2)


def fix_f2():
    """Convert all kanji on-yomi entries from hiragana to katakana."""
    shutil.copy2(KANJI, KANJI_BAK)
    k_raw = json.load(open(KANJI, encoding="utf-8"))
    converted_entries = 0
    converted_readings = 0
    for k in k_raw["entries"]:
        # 1. Top-level `on` array
        on = k.get("on") or []
        if on and any(0x3041 <= ord(c) <= 0x3096 for o in on for c in o):
            new_on = [kana_to_katakana(o) for o in on]
            k["on"] = new_on
            converted_readings += len(on)
            converted_entries += 1
        # 2. audio_yomi.on[*].reading (display field; keep audio path intact)
        ay = k.get("audio_yomi") or {}
        if isinstance(ay, dict):
            on_audio_list = ay.get("on") or []
            for entry in on_audio_list:
                if isinstance(entry, dict) and "reading" in entry:
                    entry["reading"] = kana_to_katakana(entry["reading"])
    with open(KANJI, "w", encoding="utf-8") as f:
        json.dump(k_raw, f, ensure_ascii=False, indent=2)
    print(f"  F-2: converted on-yomi to katakana on {converted_entries} kanji entries ({converted_readings} readings)")


def fix_f3():
    """Fix n5.read.017 topic tag from schedule to food."""
    shutil.copy2(READING, READING_BAK)
    r_raw = json.load(open(READING, encoding="utf-8"))
    for r in r_raw["passages"]:
        if r.get("id") == "n5.read.017":
            old = r.get("topic")
            r["topic"] = "food"
            r["topic_audit_wave"] = "accuracy-audit-f3-fix-2026-05-13"
            print(f"  F-3: n5.read.017 topic: {old!r} -> 'food'")
            break
    with open(READING, "w", encoding="utf-8") as f:
        json.dump(r_raw, f, ensure_ascii=False, indent=2)


def main():
    print("=" * 60)
    print("F-3: n5.read.017 topic tag")
    print("=" * 60)
    fix_f3()
    print()
    print("=" * 60)
    print("F-1: n5.listen.028 register rewrite")
    print("=" * 60)
    fix_f1()
    print()
    print("=" * 60)
    print("F-2: kanji on-yomi hiragana -> katakana")
    print("=" * 60)
    fix_f2()


if __name__ == "__main__":
    main()
