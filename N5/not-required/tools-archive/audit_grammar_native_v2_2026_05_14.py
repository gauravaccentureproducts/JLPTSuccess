"""Second-pass native-Japanese-teacher accuracy audit on data/grammar.json.

Adds 4 new check classes beyond the first pass:
  CHECK 1 - form-tag vs content (refined: accept よね/の/かな as Q markers)
  CHECK 2 - within-pattern duplicate examples
  CHECK 3 - cross-pattern boilerplate (top frequencies)
  CHECK 4 - politeness_ladder.humble half-applied ウ音便 (expanded)
  CHECK 5 - particle gotchas (好き/嫌い+を, copula stacking)
  CHECK 6 - missing translation_en
  CHECK 7 - illegal sentence-final particle stacking
  CHECK 8 - mixed kanji/kana orthography within same pattern
"""
import json
import re
from collections import defaultdict

g = json.load(open("data/grammar.json", encoding="utf-8"))
patterns = g["patterns"]
print(f"Re-audit: {len(patterns)} patterns, "
      f"{sum(len(p.get('examples', [])) for p in patterns)} examples")
print()

# CHECK 1
print("=" * 72)
print("CHECK 1 - form-tag vs content (refined)")
print("=" * 72)
form_mismatches = []
for p in patterns:
    for i, ex in enumerate(p.get("examples", [])):
        ja = ex.get("ja", "").rstrip("。、！？!?")
        form = ex.get("form", "")
        if form == "past":
            if not (ja.endswith("た") or "ました" in ja or "でした" in ja
                    or "かった" in ja or "だった" in ja or "んだ" in ja):
                form_mismatches.append((p["id"], i, form, ja, "no past marker"))
        elif form == "negative":
            if not ("ない" in ja or "ません" in ja or "じゃ" in ja
                    or "では" in ja or "なかった" in ja or "なくて" in ja):
                form_mismatches.append((p["id"], i, form, ja, "no negative marker"))
        elif form == "question":
            ends_q = (ja.endswith("か") or ja.endswith("？") or ja.endswith("?")
                      or ja.endswith("の") or ja.endswith("よね") or ja.endswith("かな")
                      or ja.endswith("だろう") or ja.endswith("でしょう"))
            if not ends_q:
                form_mismatches.append((p["id"], i, form, ja, "no question marker"))
print(f"  Found {len(form_mismatches)} form-tag mismatches")
for m in form_mismatches[:15]:
    pid, idx, form, ja, msg = m
    print(f"  {pid}[{idx}] form={form!r:12s} ja={ja[:55]} - {msg}")

# CHECK 2
print()
print("=" * 72)
print("CHECK 2 - within-pattern duplicate examples")
print("=" * 72)
dups = []
for p in patterns:
    seen = {}
    for i, ex in enumerate(p.get("examples", [])):
        ja = (ex.get("ja") or "").strip()
        if ja in seen:
            dups.append((p["id"], seen[ja], i, ja))
        else:
            seen[ja] = i
print(f"  Found {len(dups)} within-pattern duplicates")
for d in dups[:10]:
    print(f"  {d[0]}[{d[1]}] and [{d[2]}]: {d[3][:55]}")

# CHECK 3
print()
print("=" * 72)
print("CHECK 3 - cross-pattern boilerplate (top 15 frequencies)")
print("=" * 72)
ex_to_pids = defaultdict(list)
for p in patterns:
    for ex in p.get("examples", []):
        ja = (ex.get("ja") or "").strip()
        if ja:
            ex_to_pids[ja].append(p["id"])
top = sorted(ex_to_pids.items(), key=lambda x: -len(x[1]))[:15]
for ja, pids in top:
    if len(pids) >= 2:
        print(f"  x{len(pids):2d}  {ja[:50]:50s}  in: {','.join(pids[:6])}")

# CHECK 4
print()
print("=" * 72)
print("CHECK 4 - politeness_ladder.humble half-applied uon'bin (expanded)")
print("=" * 72)
SUSPICIOUS_PRE_GOZA = [
    "たかう", "おもう", "おおう", "はやう", "ふかう", "ちかう",
    "おいしう", "うれしう", "やさしう", "たのしう", "むずかしう",
    "あおう", "あかう", "おもしろう",
    "ありがたう", "おはやう", "おしう", "ねむう", "うまう",
]
found = 0
for p in patterns:
    pl = p.get("politeness_ladder", {})
    if not isinstance(pl, dict):
        continue
    humble = pl.get("humble", "")
    if not isinstance(humble, str):
        continue
    for pre in SUSPICIOUS_PRE_GOZA:
        if pre in humble and "ござ" in humble:
            print(f"  {p['id']} {p.get('pattern')!r}")
            print(f"    humble: {humble}")
            print(f"    suspicious token: {pre}")
            found += 1
            break
if not found:
    print("  No half-applied uon'bin detected.")

# CHECK 5
print()
print("=" * 72)
print("CHECK 5 - particle gotchas")
print("=" * 72)
SUSPICIOUS = [
    (r"を\s*すきです", "suki takes ga not o"),
    (r"を\s*きらいです", "kirai takes ga not o"),
    (r"を\s*じょうずです", "jouzu takes ga not o"),
    (r"を\s*へたです", "heta takes ga not o"),
    (r"を\s*ほしいです", "hoshii takes ga not o"),
    (r"きれいだです", "double copula"),
    (r"しずかだです", "double copula"),
    (r"きれいなです", "wrong adnominal na+desu"),
    (r"です\s*か\s*か", "double ka question marker"),
]
hits = 0
for p in patterns:
    for i, ex in enumerate(p.get("examples", [])):
        ja = ex.get("ja", "")
        for pat, msg in SUSPICIOUS:
            if re.search(pat, ja):
                print(f"  {p['id']}[{i}] {ja} - {msg}")
                hits += 1
                break
if hits == 0:
    print("  No particle gotchas found.")

# CHECK 6
print()
print("=" * 72)
print("CHECK 6 - examples missing translation_en")
print("=" * 72)
missing_trans = []
for p in patterns:
    for i, ex in enumerate(p.get("examples", [])):
        if not ex.get("translation_en"):
            missing_trans.append((p["id"], i, ex.get("ja", "")))
print(f"  Found {len(missing_trans)} missing translations")
for m in missing_trans[:15]:
    print(f"  {m[0]}[{m[1]}] ja={m[2][:50]}")

# CHECK 7
print()
print("=" * 72)
print("CHECK 7 - sentence-final particle stacking")
print("=" * 72)
STACKS = ["なあですね", "なあですよ", "ですなあね", "よねか", "ねね",
          "よよ", "だですね", "だですよ", "なな", "なあな"]
hits = 0
for p in patterns:
    for i, ex in enumerate(p.get("examples", [])):
        ja = ex.get("ja", "")
        for s in STACKS:
            if s in ja:
                print(f"  {p['id']}[{i}] {ja} - illegal stack {s!r}")
                hits += 1
                break
if hits == 0:
    print("  No illegal particle stacks found.")

# CHECK 8 - kanji/kana orthography mixing within one pattern
print()
print("=" * 72)
print("CHECK 8 - mixed kanji/kana orthography within same pattern")
print("=" * 72)
MIXED_PAIRS = [
    ("行く", "いく"), ("来る", "くる"), ("見る", "みる"),
    ("食べる", "たべる"), ("飲む", "のむ"), ("読む", "よむ"),
    ("書く", "かく"), ("学校", "がっこう"), ("先生", "せんせい"),
    ("今日", "きょう"), ("明日", "あした"), ("昨日", "きのう"),
]
mixed_findings = 0
for p in patterns:
    examples = p.get("examples", [])
    for kanji, kana in MIXED_PAIRS:
        k_idx = [i for i, ex in enumerate(examples) if kanji in ex.get("ja", "")]
        n_idx = [i for i, ex in enumerate(examples)
                 if kana in ex.get("ja", "") and kanji not in ex.get("ja", "")]
        if k_idx and n_idx:
            mixed_findings += 1
            if mixed_findings <= 15:
                print(f"  {p['id']} {p.get('pattern')!r}: BOTH {kanji}[{k_idx[0]}] AND {kana}[{n_idx[0]}]")
print(f"  (total: {mixed_findings} pattern-pair mismatches)")
