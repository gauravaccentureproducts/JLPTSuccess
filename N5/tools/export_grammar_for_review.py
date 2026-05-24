"""Export every pattern's reviewable content to a single compact JSON
file the reviewer (acting as a native JA / JLPT expert) reads through
end-to-end. One pattern per top-level entry; only the fields the 10 test
scenarios actually need."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
OUT_FILE = ROOT / "tools" / "grammar_review_input.json"


def main():
    with GRAMMAR_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)
    patterns = sorted(data["patterns"], key=lambda p: (p.get("categoryOrder", 999), p.get("patternOrder", 999), p.get("id", "")))

    out = []
    for p in patterns:
        compact = {
            "id": p["id"],
            "category": p.get("category", ""),
            "pattern": p.get("pattern", ""),
            "meaning_ja": p.get("meaning_ja", ""),
            "meaning_en": p.get("meaning_en", ""),
            "explanation_en": (p.get("explanation_en", "") or "").strip(),
            "attaches_to": (p.get("form_rules") or {}).get("attaches_to") or [],
            "examples": [
                {"ja": ex.get("ja", ""), "en": ex.get("translation_en", ""), "form": ex.get("form", "")}
                for ex in (p.get("examples") or [])
            ],
            "common_mistakes": [
                # Preserve `kind` so consumers can distinguish register_variant
                # entries (which carry form_a/form_b instead of wrong/right).
                {"wrong": m.get("wrong", ""), "right": m.get("right", ""), "why": m.get("why", ""), "kind": m.get("kind", "")}
                for m in (p.get("common_mistakes") or [])
            ],
            "wrong_corrected_pair": [
                {"wrong": w.get("wrong", ""), "correct": w.get("correct", ""), "why": w.get("why", ""), "kind": w.get("kind", "")}
                for w in (p.get("wrong_corrected_pair") or [])
            ],
        }
        out.append(compact)

    OUT_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK wrote {OUT_FILE}  ({len(out)} patterns)")


if __name__ == "__main__":
    main()
