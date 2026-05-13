"""Accuracy-audit run-4 Phase-1 manual-sampling pass.

Phase-1 = naturalness, register, semantic alignment — things CI can't
catch but a native teacher would. Run after Phase-0 produces all-clean
(corpus state: post-n5-166 fix, all 83 CI invariants + all 29 Phase-0
checks PASS).

Specific Phase-1 checks here:

  P1-A (CHECK-31 narrow): Find content-listing patterns (pattern field
       lists 2+ Japanese tokens like 'X / Y / Z') where meaning_ja
       contains NONE of the pattern's tokens. Catches the n5-166 class
       systematically. Narrower than the reverted JA-80 attempt — only
       fires for "listing" patterns, not "Verb-X" templated patterns.

  P1-B (random meaning_ja semantic sample): Pick 12 patterns at random
       and print pattern + meaning_en + meaning_ja side-by-side for
       eyeball comparison. Find any obvious semantic misalignment.

  P1-C (common_mistakes register stack sample): Pick 8 patterns at
       random with non-empty common_mistakes; check each for register-
       stacking issues (mixing 普通体 + 丁寧体 within one example).

  P1-D (cultural_callout claim sample): Pick 6 patterns at random
       with cultural_callout; check the cultural CLAIM is accurate.

  P1-E (example naturalness sample): Pick 10 grammar examples at
       random across the corpus; check for textbook-laboratory phrasing
       or unnatural collocations.
"""
import json
import io
import sys
import re
import random
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

G = json.load(open("data/grammar.json", encoding="utf-8"))["patterns"]
V = json.load(open("data/vocab.json", encoding="utf-8"))["entries"]

JA_TOKEN_RE = re.compile(r"[ぁ-んァ-ヿ一-鿿]{3,}")
TEMPLATE_PREFIX_RE = re.compile(r"\b(Verb|Adj|N|V|Noun|i-Adj|na-Adj|Verb-stem|Verb-て|Verb-た|Verb-ない)\b")

# --------------------------------------------------------------------
# P1-A: CHECK-31 narrow — content-listing pattern check
# --------------------------------------------------------------------
print("=" * 60)
print("P1-A: CHECK-31 narrow — content-listing semantic alignment")
print("=" * 60)
hits = []
for p in G:
    pf = (p.get("pattern") or "").strip()
    mja = (p.get("meaning_ja") or "").strip()
    men = (p.get("meaning_en") or "").strip()
    if not (pf and mja and men):
        continue
    # Skip patterns with grammar-template prefixes
    if TEMPLATE_PREFIX_RE.search(pf):
        continue
    # Find Japanese tokens (≥3-char runs) shared between pattern and meaning_en
    pf_tokens = set(JA_TOKEN_RE.findall(pf))
    men_tokens = set(JA_TOKEN_RE.findall(men))
    shared = pf_tokens & men_tokens
    # Only fire if pattern has ≥2 distinct Japanese tokens (a LIST pattern)
    if len(shared) < 2:
        continue
    # Check: at least one shared token must appear in meaning_ja
    if not any(tok in mja for tok in shared):
        hits.append((p["id"], pf, shared, mja[:100]))

print(f"Patterns checked (content-listing): {sum(1 for p in G if not TEMPLATE_PREFIX_RE.search((p.get('pattern') or '').strip()) and len(set(JA_TOKEN_RE.findall((p.get('pattern') or '').strip())) & set(JA_TOKEN_RE.findall((p.get('meaning_en') or '').strip()))) >= 2)}")
print(f"Firings: {len(hits)}")
for pid, pf, shared, mja_excerpt in hits[:10]:
    print(f"  {pid}:")
    print(f"    pattern: {pf!r}")
    print(f"    shared tokens: {sorted(shared)}")
    print(f"    meaning_ja[:100]: {mja_excerpt!r}")

# --------------------------------------------------------------------
# P1-B: 12 random patterns — meaning_ja eyeball
# --------------------------------------------------------------------
print("\n" + "=" * 60)
print("P1-B: Random 12 patterns — meaning_ja semantic eyeball")
print("=" * 60)
random.seed(2026513)
sample = random.sample(G, 12)
for p in sample:
    print(f"\n{p['id']}: pattern={p.get('pattern')!r}")
    print(f"  EN: {(p.get('meaning_en') or '')[:120]}")
    print(f"  JA: {(p.get('meaning_ja') or '')[:120]}")

# --------------------------------------------------------------------
# P1-C: 8 random patterns — common_mistakes register check
# --------------------------------------------------------------------
print("\n" + "=" * 60)
print("P1-C: Random 8 patterns — common_mistakes register stack sample")
print("=" * 60)
with_cm = [p for p in G if p.get("common_mistakes")]
sample_c = random.sample(with_cm, 8) if len(with_cm) >= 8 else with_cm
for p in sample_c:
    cm = (p.get("common_mistakes") or [])[0]
    if isinstance(cm, dict):
        wrong = cm.get("wrong") or ""
        right = cm.get("right") or ""
        print(f"\n{p['id']}: pattern={p.get('pattern')!r}")
        print(f"  wrong: {wrong[:80]!r}")
        print(f"  right: {right[:80]!r}")

# --------------------------------------------------------------------
# P1-D: 6 random cultural_callouts
# --------------------------------------------------------------------
print("\n" + "=" * 60)
print("P1-D: Random 6 cultural_callouts — accuracy sample")
print("=" * 60)
with_cc = [p for p in G if p.get("cultural_callout")]
sample_cc = random.sample(with_cc, 6) if len(with_cc) >= 6 else with_cc
for p in sample_cc:
    cc = p.get("cultural_callout")
    if isinstance(cc, dict):
        note = cc.get("note") or cc.get("text") or str(cc)
    else:
        note = str(cc)
    print(f"\n{p['id']}: pattern={p.get('pattern')!r}")
    print(f"  callout: {note[:200]}")

# --------------------------------------------------------------------
# P1-E: 10 random grammar examples — naturalness
# --------------------------------------------------------------------
print("\n" + "=" * 60)
print("P1-E: Random 10 grammar examples — naturalness eyeball")
print("=" * 60)
all_exs = [(p["id"], ex) for p in G for ex in (p.get("examples") or []) if isinstance(ex, dict) and ex.get("ja")]
sample_e = random.sample(all_exs, 10)
for pid, ex in sample_e:
    print(f"  {pid}: ja={ex.get('ja')!r}; en={(ex.get('en') or '')[:60]}")
