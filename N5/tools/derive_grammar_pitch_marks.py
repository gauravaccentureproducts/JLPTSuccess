"""IMP-154 remaining work: derive `pitch_marks` for the 559 grammar
example sentences that lack it.

Method:
  For each example sentence missing pitch_marks, walk the `ja` text and
  find all content words (by matching against vocab entry `form` /
  `reading` longest-prefix-first). For each match that has a
  pitch_accent {mora, drop} entry in vocab.json, emit a pitch_marks
  entry {form, mora, drop}.

  pitch_marks schema (matches existing entries):
    [{form: str, mora: int, drop: int}, ...]

Provenance: auto_derived_from_vocab_pitch (clear that the derivation
is mechanical from the vocab pitch dictionary, not native review).
"""
import json
import io
import sys
import shutil
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def main():
    VOCAB = "data/vocab.json"
    GRAMMAR = "data/grammar.json"
    BACKUP = "data/grammar.json.bak_2026_05_13_imp_154_pitch_marks"

    shutil.copy2(GRAMMAR, BACKUP)

    V = json.load(open(VOCAB, encoding="utf-8"))["entries"]
    G = json.load(open(GRAMMAR, encoding="utf-8"))

    # Build lookup: form -> pitch_accent, reading -> pitch_accent
    pitch_by_form = {}
    pitch_by_reading = {}
    for v in V:
        pa = v.get("pitch_accent")
        if not pa or not isinstance(pa, dict) or "mora" not in pa or "drop" not in pa:
            continue
        form = v.get("form") or ""
        reading = v.get("reading") or ""
        if form:
            pitch_by_form[form] = (pa["mora"], pa["drop"])
        if reading:
            pitch_by_reading[reading] = (pa["mora"], pa["drop"])

    print(f"Pitch lookup loaded: {len(pitch_by_form)} forms, "
          f"{len(pitch_by_reading)} readings")

    # All candidate strings — sorted by length descending for greedy match
    all_keys = list(set(pitch_by_form.keys()) | set(pitch_by_reading.keys()))
    all_keys = [k for k in all_keys if len(k) >= 2]  # skip single-char to avoid spurious
    all_keys.sort(key=len, reverse=True)

    # Conjugation-aware fallback: for each vocab form ending in る/く/ぐ/す/つ/
    # ぬ/ぶ/む/う (godan / ichidan), generate the stem + common conjugation
    # endings (ます, ない, た, て). Add those as alternate lookup keys.
    conjugated_lookup = {}
    for form, pitch in list(pitch_by_form.items()) + list(pitch_by_reading.items()):
        # Verbs only — last char must be a "u-row" kana
        if not form or form[-1] not in "うくぐすつぬぶむるい":
            continue
        # ichidan: ending る + preceding い/え row kana  -> stem = form[:-1]
        # godan: ending u-row -> stem = form[:-1] + i-row replacement (complex)
        # Simple approach: strip last char, try common suffixes
        stem = form[:-1]
        last = form[-1]
        # ichidan: ます = stem + ます
        if last == "る":
            for suffix in ("ます", "ない", "た", "て", "ました", "ません"):
                conjugated_lookup[stem + suffix] = pitch
        # godan -u, godan -ku, -gu, -su, -tsu, -nu, -bu, -mu — irregular masu
        # Use a small map: あ-i-pair
        u_to_i = {"う": "い", "く": "き", "ぐ": "ぎ", "す": "し", "つ": "ち",
                  "ぬ": "に", "ぶ": "び", "む": "み"}
        if last in u_to_i:
            i_form = stem + u_to_i[last]
            for suffix in ("ます", "ました", "ません"):
                conjugated_lookup[i_form + suffix] = pitch
        # i-adjective: い → かった / くて / くない
        if last == "い":
            for suffix in ("かった", "くて", "くない"):
                conjugated_lookup[stem + suffix] = pitch

    print(f"Conjugated fallback: {len(conjugated_lookup)} additional keys")

    # Merge into the keys list (sorted by length desc)
    merged_keys = list(set(all_keys) | set(conjugated_lookup.keys()))
    merged_keys = [k for k in merged_keys if len(k) >= 2]
    merged_keys.sort(key=len, reverse=True)

    def derive_pitch_marks(ja_text: str) -> list:
        """Greedy left-to-right match against vocab forms/readings/conjugations."""
        seen = {}  # form -> (mora, drop) — dedupe within sentence
        text = re.sub(r"[、。「」『』！？・…]", " ", ja_text)
        i = 0
        text_chars = list(text)
        while i < len(text_chars):
            matched = False
            for key in merged_keys:
                if text_chars[i:i+len(key)] == list(key):
                    if key in pitch_by_form:
                        seen.setdefault(key, pitch_by_form[key])
                    elif key in pitch_by_reading:
                        seen.setdefault(key, pitch_by_reading[key])
                    elif key in conjugated_lookup:
                        seen.setdefault(key, conjugated_lookup[key])
                    i += len(key)
                    matched = True
                    break
            if not matched:
                i += 1
        return [{"form": k, "mora": m, "drop": d} for k, (m, d) in seen.items()]

    updated = 0
    skipped_no_match = 0
    for p in G["patterns"]:
        for ex in (p.get("examples") or []):
            if ex.get("pitch_marks"):
                continue
            ja = ex.get("ja") or ""
            if not ja:
                continue
            marks = derive_pitch_marks(ja)
            if marks:
                ex["pitch_marks"] = marks
                ex["pitch_marks_provenance"] = "auto_derived_from_vocab_pitch"
                ex["pitch_marks_audit_wave"] = "imp-154-drift-fill-2026-05-13"
                updated += 1
            else:
                skipped_no_match += 1

    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(G, f, ensure_ascii=False, indent=2)

    print(f"\nFilled pitch_marks on {updated} examples")
    print(f"Skipped (no vocab match): {skipped_no_match}")

    # Final coverage
    total = 0; with_marks = 0
    for p in G["patterns"]:
        for ex in (p.get("examples") or []):
            total += 1
            if ex.get("pitch_marks"):
                with_marks += 1
    print(f"\nFinal coverage: {with_marks}/{total} ({with_marks*100//total}%)")


if __name__ == "__main__":
    main()
