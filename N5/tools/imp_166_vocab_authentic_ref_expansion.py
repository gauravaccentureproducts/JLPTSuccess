"""IMP-166: expand vocab `authentic_refs` from 37/1009 to ≥100/1009.

The `authentic_refs` field on vocab entries lists authentic.json item IDs
that demonstrate the word in a real-world context (sign, menu, transit
notice, etc.).

Two-phase fill:

PHASE 1 — Reverse-map existing authentic.json vocab_refs:
  authentic.json has 39 items with vocab_refs (pointing to vocab IDs).
  vocab.json has 37 with authentic_refs. Slight mismatch — invert
  authentic.json → vocab.json union to make the bidirectional graph
  consistent.

PHASE 2 — Match additional authentic items to vocab by form/reading:
  Walk all 188 authentic.json items; for each, look up its `ja` (form)
  and `reading` against vocab. If a clean match exists and the vocab
  entry doesn't yet have an authentic_refs entry, add it.

Provenance: auto_derived (mechanical inversion + form/reading match).
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

VOCAB = "data/vocab.json"
AUTHENTIC = "data/authentic.json"
VOCAB_BAK = "data/vocab.json.bak_2026_05_13_imp_166_authentic_refs"


def main():
    shutil.copy2(VOCAB, VOCAB_BAK)

    V_raw = json.load(open(VOCAB, encoding="utf-8"))
    V = V_raw["entries"]
    A_raw = json.load(open(AUTHENTIC, encoding="utf-8"))
    A_items = A_raw.get("items") or A_raw.get("entries") or []

    # Build vocab indexes
    vocab_by_id = {v["id"]: v for v in V}
    vocab_by_form = {}
    vocab_by_reading = {}
    for v in V:
        f = v.get("form")
        r = v.get("reading")
        if f:
            vocab_by_form.setdefault(f, []).append(v)
        if r:
            vocab_by_reading.setdefault(r, []).append(v)

    # === PHASE 1: reverse-map vocab_refs -> authentic_refs ===
    phase1_added = 0
    for auth in A_items:
        auth_id = auth.get("id")
        if not auth_id:
            continue
        vrefs = auth.get("vocab_refs") or []
        for vid in vrefs:
            v = vocab_by_id.get(vid)
            if not v:
                continue
            existing_refs = v.get("authentic_refs") or []
            if auth_id not in existing_refs:
                v["authentic_refs"] = sorted(set(existing_refs) | {auth_id})
                if not v.get("authentic_refs_provenance"):
                    v["authentic_refs_provenance"] = "auto_derived"
                phase1_added += 1

    # === PHASE 2: form/reading match for unlinked authentic items ===
    phase2_added = 0
    for auth in A_items:
        auth_id = auth.get("id")
        if not auth_id:
            continue
        # Skip if this authentic item already has vocab_refs (Phase 1 handled it)
        if auth.get("vocab_refs"):
            continue
        ja_form = (auth.get("ja") or "").strip()
        ja_reading = (auth.get("reading") or "").strip()
        if not ja_form and not ja_reading:
            continue
        # Try form match first, then reading
        matches = vocab_by_form.get(ja_form, [])
        if not matches and ja_reading:
            matches = vocab_by_reading.get(ja_reading, [])
        for v in matches:
            existing_refs = v.get("authentic_refs") or []
            if auth_id not in existing_refs:
                v["authentic_refs"] = sorted(set(existing_refs) | {auth_id})
                if not v.get("authentic_refs_provenance"):
                    v["authentic_refs_provenance"] = "auto_derived"
                phase2_added += 1

    with open(VOCAB, "w", encoding="utf-8") as f:
        json.dump(V_raw, f, ensure_ascii=False, indent=2)

    print(f"Phase 1 (reverse-map): {phase1_added} authentic_refs entries added")
    print(f"Phase 2 (form/reading match): {phase2_added} authentic_refs entries added")

    # Final coverage
    V2 = json.load(open(VOCAB, encoding="utf-8"))["entries"]
    with_refs = sum(1 for v in V2 if v.get("authentic_refs"))
    total_ref_entries = sum(len(v.get("authentic_refs") or []) for v in V2)
    print(f"\nFinal: {with_refs}/1009 vocab entries with authentic_refs")
    print(f"Total authentic_refs link count: {total_ref_entries}")


if __name__ == "__main__":
    main()
