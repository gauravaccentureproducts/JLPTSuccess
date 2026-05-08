"""
Vocab.json structural dedup — closes the 164-case grammar.json double-tag
root cause flagged in the 2026-05-08 native-teacher audit.

Strategy (SAFE SUBSET):
- Only dedup pairs where one entry explicitly says "(also in §X)" OR
  both entries have the same normalized gloss.
- Skip 3+ entry groups (e.g., あつい with weather/touch/thick variants);
  those need case-by-case review.
- Skip true polysemes (different glosses, e.g., は = tooth/leaf/particle).
- Pick canonical = the entry NOT marked "(also in)"; if both unmarked,
  prefer the lower-numbered section (§13 preferred over §26).
- Merge unique data from removed entry into canonical: examples,
  pitch_accent, notes — preserve before deletion.
- Migrate all references in grammar.json from removed IDs to canonical.

Out of scope:
- Polysemes (legitimate same-form-different-meaning; preserved).
- 3+ entry groups (need manual review).
- Mid-build vocab section restructuring (e.g., えいが → "Entertainment"
  section creation).

Run: python not-required/tools-archive/dedup_vocab_2026_05_08.py
"""
import json
import re
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def normalize_gloss(g):
    g = re.sub(r"\s*\(also in.*?\)", "", g)
    g = re.sub(r"\(.*?\)", "", g)
    return g.lower().strip().rstrip(",.")


def section_num(s):
    m = re.match(r"^(\d+)\.", s)
    return int(m.group(1)) if m else 999


def build_dedup_mapping(vocab_data):
    """Return (mapping, canonical_entries_to_merge_data_into).

    mapping: {removed_id: canonical_id}
    merge_pairs: [(canonical_entry, removed_entry), ...]
    """
    groups = defaultdict(list)
    for e in vocab_data["entries"]:
        key = (e.get("form", ""), e.get("reading", ""))
        groups[key].append(e)

    mapping = {}
    merge_pairs = []
    for (form, reading), entries in groups.items():
        if len(entries) != 2:
            continue
        e1, e2 = entries
        g1, g2 = e1.get("gloss", "").lower(), e2.get("gloss", "").lower()
        cross1 = "(also in" in g1
        cross2 = "(also in" in g2
        if not (cross1 or cross2 or normalize_gloss(g1) == normalize_gloss(g2)):
            continue
        if cross1 and not cross2:
            canonical, removed = e2, e1
        elif cross2 and not cross1:
            canonical, removed = e1, e2
        elif section_num(e1["section"]) <= section_num(e2["section"]):
            canonical, removed = e1, e2
        else:
            canonical, removed = e2, e1
        mapping[removed["id"]] = canonical["id"]
        merge_pairs.append((canonical, removed))
    return mapping, merge_pairs


def merge_data(canonical, removed):
    """Merge unique examples + fill missing optional fields from removed
    into canonical. Idempotent — modifies canonical in place."""
    # Merge examples (unique by ja+translation_en pair)
    canon_examples = canonical.get("examples", [])
    canon_keys = {(ex.get("ja", ""), ex.get("translation_en", "")) for ex in canon_examples}
    for ex in removed.get("examples", []):
        key = (ex.get("ja", ""), ex.get("translation_en", ""))
        if key not in canon_keys:
            canon_examples.append(ex)
            canon_keys.add(key)
    canonical["examples"] = canon_examples

    # Take pitch_accent if canonical lacks one
    if "pitch_accent" not in canonical and "pitch_accent" in removed:
        canonical["pitch_accent"] = removed["pitch_accent"]
        if "pitch_accent_provenance" in removed:
            canonical["pitch_accent_provenance"] = removed["pitch_accent_provenance"]

    # Take notes if canonical lacks them
    if not canonical.get("notes") and removed.get("notes"):
        canonical["notes"] = removed["notes"]


def update_vocab_id_refs(obj, mapping):
    """Walk a JSON tree and replace any string equal to a removed ID
    with its canonical. Returns count of replacements."""
    if isinstance(obj, str):
        return 0  # strings can't be modified in-place; handled at parent level
    if isinstance(obj, dict):
        count = 0
        for k, v in obj.items():
            if isinstance(v, str) and v in mapping:
                obj[k] = mapping[v]
                count += 1
            elif isinstance(v, list):
                # check each list element
                for i, item in enumerate(v):
                    if isinstance(item, str) and item in mapping:
                        v[i] = mapping[item]
                        count += 1
                    else:
                        count += update_vocab_id_refs(item, mapping)
            else:
                count += update_vocab_id_refs(v, mapping)
        return count
    if isinstance(obj, list):
        count = 0
        for i, item in enumerate(obj):
            if isinstance(item, str) and item in mapping:
                obj[i] = mapping[item]
                count += 1
            else:
                count += update_vocab_id_refs(item, mapping)
        return count
    return 0


def dedup_vocab_id_arrays(obj):
    """After mapping, vocab_ids arrays may have duplicate IDs (since
    removed and canonical both occurred in some lists). Dedupe while
    preserving order."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "vocab_ids" and isinstance(v, list):
                seen = set()
                deduped = []
                for vid in v:
                    if vid not in seen:
                        seen.add(vid)
                        deduped.append(vid)
                obj[k] = deduped
            else:
                dedup_vocab_id_arrays(v)
    elif isinstance(obj, list):
        for item in obj:
            dedup_vocab_id_arrays(item)


def main():
    vocab_path = DATA_DIR / "vocab.json"
    grammar_path = DATA_DIR / "grammar.json"

    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab_data = json.load(f)
    with open(grammar_path, "r", encoding="utf-8") as f:
        grammar_data = json.load(f)

    mapping, merge_pairs = build_dedup_mapping(vocab_data)
    print(f"Identified {len(mapping)} safe-dedup pairs")

    # Step 1: merge data from removed into canonical
    for canonical, removed in merge_pairs:
        merge_data(canonical, removed)

    # Step 2: migrate references in grammar.json
    ref_count = update_vocab_id_refs(grammar_data, mapping)
    print(f"Migrated {ref_count} references in grammar.json")

    # Step 3: dedup any vocab_ids arrays that now have dupes
    dedup_vocab_id_arrays(grammar_data)

    # Step 4: remove duplicate entries from vocab.json
    removed_ids = set(mapping.keys())
    before = len(vocab_data["entries"])
    vocab_data["entries"] = [e for e in vocab_data["entries"] if e["id"] not in removed_ids]
    after = len(vocab_data["entries"])
    print(f"Removed {before - after} duplicate entries from vocab.json ({before} -> {after})")

    # Write back
    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(vocab_data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(grammar_path, "w", encoding="utf-8") as f:
        json.dump(grammar_data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("Done.")


if __name__ == "__main__":
    main()
