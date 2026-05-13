"""Thorough accuracy-audit run-2 sweep — zero-tolerance pass.

Samples 12 high-risk areas for Japanese-language correctness issues
that CI invariants don't cover. Read-only.
"""
import json
import io
import sys
import re
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

g = json.load(open("data/grammar.json", encoding="utf-8"))["patterns"]
V = json.load(open("data/vocab.json", encoding="utf-8"))["entries"]
K = json.load(open("data/kanji.json", encoding="utf-8"))["entries"]
R = json.load(open("data/reading.json", encoding="utf-8"))["passages"]
L = json.load(open("data/listening.json", encoding="utf-8"))["items"]


# 1. Group-1 exception verbs
print("=== 1. Group-1 exception verbs (look ichidan, are godan) ===")
exceptions = {
    "はいる": "godan_group1_exception",
    "かえる": "godan_group1_exception",
    "はしる": "godan_group1_exception",
    "しる": "godan_group1_exception",
    "きる": "godan_group1_exception",
    "いる": "godan_group1_exception",
}
for v in V:
    if v.get("reading") in exceptions:
        vc = v.get("verb_class")
        ok = "OK" if "godan" in str(vc) else "FAIL"
        print(f"  [{ok}] {v.get('form')} ({v['reading']}) verb_class={vc!r}")

# 2. 行く te-form correctness (must be 行って not 行いて)
print("\n=== 2. 行く te-form correctness ===")
bad = []
for p in g:
    for ex in p.get("examples") or []:
        ja = ex.get("ja") or ""
        if "行いて" in ja or "行いた" in ja:
            bad.append((p["id"], ja[:80]))
print(f"Wrong 行いて/行いた found: {len(bad)}")
for pid, ja in bad[:5]:
    print(f"  {pid}: {ja}")

# 3. Counter sound-changes verification
print("\n=== 3. Counter sound-changes (本 with 1/3/6/8/10 → ぽん/ぼん) ===")
for k in K:
    if k["glyph"] == "本":
        compounds = k.get("n5_compounds") or []
        for c in compounds:
            if isinstance(c, dict):
                f = c.get("form", "")
                r = c.get("reading", "")
                if any(n in f for n in ["一本", "二本", "三本", "四本", "五本",
                                          "六本", "七本", "八本", "九本", "十本"]):
                    print(f"  {f} -> {r}")
        break

# 4. Sokuon allophones as separate kun entries (anti-A4)
print("\n=== 4. Sokuon allophones in kanji.kun ===")
sokuon_violations = []
for k in K:
    kun = k.get("kun") or []
    if isinstance(kun, list):
        for item in kun:
            kun_text = item if isinstance(item, str) else item.get("reading", "")
            if "っ" in kun_text:
                sokuon_violations.append((k["glyph"], kun_text))
print(f"Sokuon allophones found in kun arrays: {len(sokuon_violations)}")
for g_, kun in sokuon_violations[:5]:
    print(f"  {g_}: {kun!r}")

# 5. Half-applied ウ音便 keigo in politeness_ladder
print("\n=== 5. Half-applied ウ音便 keigo (anti-A9) ===")
bad_wo_onbin = []
for p in g:
    pl = p.get("politeness_ladder") or []
    if isinstance(pl, list):
        for entry in pl:
            if not isinstance(entry, dict):
                continue
            ja = (entry.get("ja") or entry.get("form") or "") or ""
            # Bad pattern: i-adj stem + う + ござ (didn't contract)
            for bad_pat in ["かう ござ", "なう ござ", "いう ござ", "たう ござ", "はやう"]:
                if bad_pat in ja:
                    bad_wo_onbin.append((p["id"], ja[:60]))
                    break
print(f"Half-applied ウ音便 found: {len(bad_wo_onbin)}")

# 6. Pitch minimal pairs verify
print("\n=== 6. Pitch minimal-pair coverage ===")
mp = [v for v in V if v.get("pitch_minimal_pair")]
print(f"Vocab with pitch_minimal_pair: {len(mp)}")

# 7. Placeholder leakage scan
print("\n=== 7. Placeholder text leakage ===")
files_to_scan = [
    "data/grammar.json", "data/vocab.json", "data/kanji.json",
    "data/reading.json", "data/listening.json",
]
leak_terms = ["TODO", "FIXME", "XXX", "placeholder",
              "lorem ipsum", "TBD", "(temp)", "INSERT_",
              "Sample text", "test test"]
any_leaks = False
for f in files_to_scan:
    content = open(f, encoding="utf-8").read()
    for term in leak_terms:
        if term in content:
            n = content.count(term)
            idx = content.find(term)
            ctx = content[max(0, idx - 40):idx + 40].replace("\n", " ")
            print(f"  {f}: '{term}' x{n}, sample: ...{ctx}...")
            any_leaks = True
if not any_leaks:
    print("  (none found)")

# 8. Cross-surface completeness
print("\n=== 8. Cross-surface completeness ===")
empty_prompt_L = sum(1 for li in L if not li.get("prompt_ja"))
empty_text_R = sum(
    1 for r in R for p in (r.get("paragraphs") or []) if not (p.get("text_ja") or "")
)
empty_choices_L = sum(1 for li in L if not li.get("choices"))
print(f"Listening items with empty prompt_ja: {empty_prompt_L}")
print(f"Reading paragraphs with empty text_ja: {empty_text_R}")
print(f"Listening items with empty choices: {empty_choices_L}")

# 9. Grammar example sanity (double-copula, double-particle)
print("\n=== 9. Grammar example sanity ===")
double_issues = []
for p in g:
    for ex in p.get("examples") or []:
        ja = ex.get("ja") or ""
        for bad in ["ですです", "ますます", "だだ", "ははは", "がが", "をを"]:
            if bad in ja:
                double_issues.append((p["id"], bad, ja[:60]))
print(f"Double-particle / double-copula: {len(double_issues)}")
for pid, bad, ja in double_issues:
    print(f"  {pid}: '{bad}' in {ja!r}")

# 10. Romaji leakage in JA user-facing fields
print("\n=== 10. Romaji in JA fields ===")
romaji_re = re.compile(r"\b[A-Za-z]{4,}\b")
romaji_leaks = []
allowlist = {"true", "false", "null", "JLPT", "VOICEVOX", "TTS"}
for p in g:
    for ex in p.get("examples") or []:
        ja = ex.get("ja") or ""
        for m in romaji_re.findall(ja):
            if m.lower() not in {x.lower() for x in allowlist} and m not in allowlist:
                romaji_leaks.append((p["id"], m, ja[:60]))
print(f"Suspicious romaji in grammar examples: {len(romaji_leaks)}")
for pid, term, ja in romaji_leaks[:5]:
    print(f"  {pid}: '{term}' in {ja!r}")

# 11. Cultural-context register check on listening items
print("\n=== 11. Listening cultural_context coverage ===")
no_ctx = [li["id"] for li in L if not li.get("cultural_context")]
print(f"Listening items missing cultural_context: {len(no_ctx)}")

# 12. Quick sanity on the kanji on-yomi conversion completeness
print("\n=== 12. Kanji on-yomi katakana-conversion completeness ===")
hira_re = re.compile(r"[぀-ゟ]")
hira_in_on = []
for k in K:
    for o in (k.get("on") or []):
        if isinstance(o, str) and hira_re.search(o):
            hira_in_on.append((k["glyph"], o))
print(f"On-yomi entries still containing hiragana: {len(hira_in_on)}")
for g_, o in hira_in_on[:5]:
    print(f"  {g_}: {o!r}")

# 13. Random sample 6 grammar examples — naturalness eyeball
print("\n=== 13. Random sample of grammar examples (naturalness eyeball) ===")
import random
random.seed(777)
samples = []
all_examples = [(p["id"], ex) for p in g for ex in (p.get("examples") or [])]
for pid, ex in random.sample(all_examples, 8):
    print(f"  {pid}: ja={ex.get('ja')!r}, en={ex.get('translation_en')[:60]!r}")
