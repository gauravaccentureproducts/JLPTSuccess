"""Extract round-4 targets (DOKO/KORE/GREET templates) with full context."""
import json, re
from pathlib import Path

d = json.load(open("data/vocab.json", encoding="utf-8"))
pat_doko = re.compile(r"^あの\s+(.{1,10})は\s*どこですか。?$")
pat_kore = re.compile(r"^(これ|あれ|それ)は\s*(.{1,10})です。?$")
pat_quote = re.compile(r"^「(.{1,10})」と\s*(いいました|言いました|あいさつしました)。?$")
GREETINGS = {"おはよう","こんにちは","こんばんは","ありがとう","さようなら",
             "おやすみ","ただいま","おかえり","もしもし","いってきます",
             "いってらっしゃい","おかげさまで"}

out = {"doko": [], "kore": [], "greet_wrong_verb": []}
for e in d["entries"]:
    eid = e.get("id","")
    form = e.get("form","")
    gloss = e.get("gloss","")
    section = e.get("section","")
    is_loc = "13-locations" in section or "26-house" in section
    exs = e.get("examples", [])
    for i, ex in enumerate(exs):
        ja = ex.get("ja","").strip()
        m = pat_doko.fullmatch(ja)
        if m and not is_loc and m.group(1).strip() == form.strip():
            out["doko"].append({
                "id": eid, "idx": i, "form": form, "gloss": gloss,
                "ja": ja, "en": ex.get("translation_en",""),
                "all_ja": [x.get("ja") for x in exs],
            })
        m = pat_kore.fullmatch(ja)
        if m and len(exs) >= 3:
            out["kore"].append({
                "id": eid, "idx": i, "form": form, "gloss": gloss,
                "ja": ja, "en": ex.get("translation_en",""),
                "all_ja": [x.get("ja") for x in exs],
            })
        m = pat_quote.fullmatch(ja)
        if m and m.group(2) == "あいさつしました" and m.group(1) not in GREETINGS:
            out["greet_wrong_verb"].append({
                "id": eid, "idx": i, "form": form, "gloss": gloss,
                "ja": ja, "en": ex.get("translation_en",""),
                "all_ja": [x.get("ja") for x in exs],
            })

Path("not-required/tools-archive/_round4_targets.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"DOKO: {len(out['doko'])}, KORE: {len(out['kore'])}, GREET-WRONG-VERB: {len(out['greet_wrong_verb'])}")
