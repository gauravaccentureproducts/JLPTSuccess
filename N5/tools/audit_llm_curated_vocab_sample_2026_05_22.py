"""Close review §4 item 7 — spot-check 5-10% of llm_curated vocab
examples for OTHER regressions beyond the kanji-whitelist breach
(NTR-001).

Dimensions audited:
  D1 — over-formal register (でございます / おります / sonkeigo)
  D2 — unidiomatic / literary phrasing (のである, であろう, etc.)
  D3 — headword absent from example
  D5 — cross-entry template duplication (same 8-char prefix N+ times)

Sample: deterministic stratified ~100/970, seeded by SHA256 for
reproducibility.
"""
import sys, io, json, os, re, hashlib
from collections import defaultdict, Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OVERFORMAL = [
    re.compile(r"でございます"),
    re.compile(r"〜?ております"),
    re.compile(r"(?:存じます|致します|頂きます|申し上げ)"),
    re.compile(r"いらっしゃいま"),
    re.compile(r"くださいませ"),
    re.compile(r"おっしゃ"),
]
STIFF = [
    re.compile(r"〜のである"),
    re.compile(r"〜であろう"),
    re.compile(r"恐れ入りま"),
    re.compile(r"〜なければなりません"),  # N4+ obligation, not core N5
    re.compile(r"〜ねばならない"),  # literary obligation
]


def main():
    v = json.load(open(os.path.join(REPO_N5, "data", "vocab.json"), encoding="utf-8"))
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))
    llm = []
    for entry in vl:
        if not isinstance(entry, dict): continue
        eid = entry.get("id") or entry.get("form")
        form = entry.get("form") or ""
        reading = entry.get("reading") or ""
        section = entry.get("section") or ""
        for idx, ex in enumerate(entry.get("examples") or []):
            if not isinstance(ex, dict): continue
            if (ex.get("provenance") or ex.get("_provenance") or "") == "llm_curated":
                llm.append({"vocab_id": eid, "form": form, "reading": reading,
                            "section": section, "ex_idx": idx,
                            "ja": ex.get("ja", "") or "",
                            "en": ex.get("en", "") or ""})
    print(f"Total llm_curated examples: {len(llm)}")
    target = 100
    by_section = defaultdict(list)
    for e in llm:
        by_section[e["section"]].append(e)
    sample = []
    for section, items in by_section.items():
        take_n = max(1, round(len(items) * target / max(1, len(llm))))
        items_sorted = sorted(items, key=lambda x: hashlib.sha256(
            f"{x['vocab_id']}|{x['ex_idx']}".encode()).hexdigest())
        sample.extend(items_sorted[:take_n])
    sample = sample[:target + 10]
    print(f"Sampled {len(sample)} examples for audit")
    print()

    d1 = []; d2 = []; d3 = []
    for s in sample:
        ja = s["ja"]
        if any(p.search(ja) for p in OVERFORMAL):
            d1.append(s)
        if any(p.search(ja) for p in STIFF):
            d2.append(s)
        form, reading = s["form"], s["reading"]
        stems = {w for w in (form, reading, form[:-1] if len(form)>=2 else "", reading[:-1] if len(reading)>=2 else "") if w}
        if not any(st in ja for st in stems):
            d3.append(s)

    # D5: scan ALL llm examples (not just sample) for cross-entry template duplication
    prefix_counter = Counter()
    prefix_to_items = defaultdict(list)
    for e in llm:
        ja = e["ja"]
        if len(ja) >= 10:
            p = ja[:10]
            prefix_counter[p] += 1
            prefix_to_items[p].append(e)
    duplicates_global = [(p, c) for p, c in prefix_counter.most_common() if c >= 5]

    print("--- D1 Over-formal register ---")
    for s in d1: print(f"  {s['vocab_id']}[{s['ex_idx']}]: {s['ja']!r}")
    if not d1: print("  (none)")
    print()
    print("--- D2 Unidiomatic / literary forms ---")
    for s in d2: print(f"  {s['vocab_id']}[{s['ex_idx']}]: {s['ja']!r}")
    if not d2: print("  (none)")
    print()
    print("--- D3 Headword absent (heuristic) ---")
    for s in d3[:10]: print(f"  {s['vocab_id']}[{s['ex_idx']}]: form={s['form']!r} ja={s['ja']!r}")
    if len(d3) > 10: print(f"  ... and {len(d3)-10} more")
    if not d3: print("  (none)")
    print()
    print(f"--- D5 Template clusters (10-char prefix, 5+ occurrences across ALL {len(llm)} llm examples) ---")
    for p, c in duplicates_global[:8]:
        print(f"  prefix {p!r}: {c} occurrences")
        for m in prefix_to_items[p][:3]:
            print(f"    {m['vocab_id']}[{m['ex_idx']}]: {m['ja']!r}")
    if not duplicates_global: print("  (no 5+ clusters)")
    print()
    print("=== Summary ===")
    print(f"  Sample size: {len(sample)} / {len(llm)} llm_curated examples")
    print(f"  D1 over-formal:   {len(d1)} hits")
    print(f"  D2 unidiomatic:   {len(d2)} hits")
    print(f"  D3 headword-absent: {len(d3)} hits")
    print(f"  D5 template-clusters (global ≥5): {len(duplicates_global)} groups")


if __name__ == "__main__":
    main()
