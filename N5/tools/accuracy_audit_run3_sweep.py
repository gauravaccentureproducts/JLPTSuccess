"""Accuracy-audit run-3 sweep — surfaces not deep-sampled in run-2.

Looks at:
  - Vocab.examples — naturalness of stems
  - Reading passages — internal grammar (particles, verbs, register)
  - Listening script_ja — natural conversation phrasing
  - Cultural-context blocks — accuracy of cultural claims
  - Essay sub-fields (intro/why/pitfalls/contrasts/practice)
  - Authentic citations text
  - Kanji etymology stories
  - Stale field values + dead-link audio refs
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


# 1. Vocab examples — sample 10 random + check for double-particle / dangling
print("=== 1. Vocab examples — random naturalness sample ===")
import random
random.seed(424242)
all_v_exs = [(v["id"], ex) for v in V for ex in (v.get("examples") or [])
             if isinstance(ex, dict) and ex.get("ja")]
print(f"Total vocab examples: {len(all_v_exs)}")

# Look for double-particle issues
problems = []
for vid, ex in all_v_exs:
    ja = ex.get("ja") or ""
    for bad in ["をを", "がが", "にに", "でで", "とと", "もも", "へへ", "ですです", "ますます", "ははは", "がが、"]:
        if bad in ja:
            problems.append((vid, bad, ja[:60]))
print(f"Double-particle / triple-kana issues in vocab examples: {len(problems)}")
for vid, bad, ja in problems[:5]:
    print(f"  {vid}: '{bad}' in {ja!r}")

# Random 6 sample for eyeball
print("Random 6 vocab examples (naturalness eyeball):")
for vid, ex in random.sample(all_v_exs, 6):
    print(f"  {vid}: ja={ex.get('ja')!r}")


# 2. Reading passages — internal grammar check
print("\n\n=== 2. Reading passages — internal text scan ===")
# Look for 3+ consecutive same kana (same as JA-78 but for reading paragraphs)
REPEAT_RE = re.compile(r"([぀-ゟ])\1{2,}")
r_issues = []
for r in R:
    for pi, para in enumerate(r.get("paragraphs") or []):
        text = para.get("text_ja") or ""
        m = REPEAT_RE.search(text)
        if m:
            r_issues.append((r["id"], pi, m.group(0), text[:60]))
print(f"Reading paragraphs with 3+ same kana: {len(r_issues)}")
for rid, pi, rep, text in r_issues[:5]:
    print(f"  {rid} para[{pi}]: '{rep}' in {text!r}")

# Reading passage double-particle issues
r_double = []
for r in R:
    for pi, para in enumerate(r.get("paragraphs") or []):
        text = para.get("text_ja") or ""
        for bad in ["をを", "がが", "にに", "でで", "とと", "ですです", "ますます"]:
            if bad in text:
                r_double.append((r["id"], pi, bad, text[:60]))
                break
print(f"Reading paragraphs with double-particle: {len(r_double)}")
for rid, pi, bad, text in r_double[:5]:
    print(f"  {rid} para[{pi}]: '{bad}' in {text!r}")


# 3. Listening scripts — same scans on script_ja + lines
print("\n\n=== 3. Listening scripts — text-quality scan ===")
l_issues = []
for li in L:
    script = li.get("script_ja") or ""
    for bad in ["をを", "がが", "にに", "でで", "とと", "ですです", "ますます"]:
        if bad in script:
            l_issues.append((li["id"], bad, script[:80]))
            break
    m = REPEAT_RE.search(script)
    if m:
        l_issues.append((li["id"], f"3+x'{m.group(1)}'", script[:80]))
print(f"Listening script issues: {len(l_issues)}")
for lid, kind, script in l_issues[:5]:
    print(f"  {lid}: {kind} in {script!r}")


# 4. Cultural-context blocks — sample 8 grammar patterns
print("\n\n=== 4. Cultural-context naturalness sample ===")
with_cc = [p for p in g if p.get("cultural_callout")]
print(f"Patterns with cultural_callout: {len(with_cc)}")
for p in random.sample(with_cc, 6):
    cc = p.get("cultural_callout")
    if isinstance(cc, dict):
        text = cc.get("text") or cc.get("ja") or cc.get("en") or str(cc)
    else:
        text = str(cc)
    print(f"  {p['id']}: {text[:120]}")


# 5. Essay sub-fields sample
print("\n\n=== 5. Essay sub-fields — sample (intro/why/pitfalls/practice) ===")
patterns_with_essay = [p for p in g if p.get("essay")]
for p in random.sample(patterns_with_essay, 4):
    e = p.get("essay") or {}
    for sub in ["intro", "why", "pitfalls", "practice"]:
        text = e.get(sub) or ""
        if text:
            # Quick scan for placeholder leakage in essays
            for bad in ["TODO", "TBD", "(temp)", "placeholder", "fallback"]:
                if bad.lower() in text.lower():
                    print(f"  ! {p['id']}.essay.{sub}: contains '{bad}'")


# 6. Authentic citations sample
print("\n\n=== 6. Authentic_citations sample ===")
with_ac = [p for p in g if p.get("authentic_citations")]
print(f"Patterns with authentic_citations: {len(with_ac)}")
# Sample 3
for p in random.sample(with_ac, 3):
    ac = p.get("authentic_citations") or []
    if isinstance(ac, list) and ac:
        first = ac[0]
        print(f"  {p['id']}: source={first.get('source')!r}, context={first.get('context','')[:60]!r}")


# 7. Kanji etymology naturalness
print("\n\n=== 7. Kanji etymology sample ===")
random.seed(8765)
for k in random.sample([k for k in K if k.get("etymology")], 5):
    ety = k.get("etymology")
    if isinstance(ety, dict):
        text = ety.get("text") or ety.get("en") or str(ety)
    else:
        text = str(ety)
    print(f"  {k['glyph']}: {text[:100]}")


# 8. Audio refs dead-link check
print("\n\n=== 8. Audio reference integrity (sample) ===")
# Sample 20 audio refs from grammar examples, listening, etc. and verify file exists
audio_refs = []
for p in g:
    for ex in p.get("examples") or []:
        if ex.get("audio"):
            audio_refs.append(ex["audio"])
for li in L:
    if li.get("audio"):
        audio_refs.append(li["audio"])
    if li.get("audio_slow"):
        audio_refs.append(li["audio_slow"])

random.seed(13)
sample = random.sample(audio_refs, min(15, len(audio_refs)))
missing = [a for a in sample if not os.path.exists(a)]
print(f"Audio refs sampled: {len(sample)}; missing on disk: {len(missing)}")
for m in missing[:5]:
    print(f"  missing: {m}")


# 9. Number-vs-counter mismatch sample — verify counter-words in vocab examples
print("\n\n=== 9. Counter-word vocab spotcheck ===")
counter_words = [v for v in V if v.get("pos") == "counter"]
print(f"Vocab counter entries: {len(counter_words)}")
# Verify each has a counter-appropriate example
for v in random.sample(counter_words, 5):
    exs = v.get("examples") or []
    if exs:
        ex0 = exs[0]
        print(f"  {v['form']} ({v['reading']}): ex={ex0.get('ja','?')[:60]}")


# 10. Cross-locale: meaning_hi presence + reasonableness (just count, not validate)
print("\n\n=== 10. Hindi locale coverage spot-check ===")
no_hi = sum(1 for p in g if not p.get("meaning_hi"))
no_hi_v = sum(1 for v in V if not v.get("gloss_hi"))
no_hi_k = sum(1 for k in K if not (k.get("meanings_hi") or k.get("meaning_hi")))
print(f"Grammar patterns missing meaning_hi: {no_hi}")
print(f"Vocab entries missing gloss_hi: {no_hi_v}")
print(f"Kanji entries missing meaning_hi: {no_hi_k}")


# 11. Verb form-field consistency in examples (anti-§3.2.34)
print("\n\n=== 11. Grammar example form-field consistency ===")
inconsistent = []
for p in g:
    exs = p.get("examples") or []
    if not exs:
        continue
    has_form = sum(1 for ex in exs if ex.get("form"))
    if 0 < has_form < len(exs):
        inconsistent.append((p["id"], has_form, len(exs)))
print(f"Patterns with mixed form-field presence on examples: {len(inconsistent)}")
for pid, has, total in inconsistent[:5]:
    print(f"  {pid}: {has}/{total} examples have `form`")


# 12. Verify all listening choices include the correctAnswer (anti-bug)
print("\n\n=== 12. Listening correctAnswer in choices ===")
mismatch = []
for li in L:
    ca = li.get("correctAnswer")
    choices = li.get("choices") or []
    if ca and ca not in choices:
        mismatch.append((li["id"], ca, choices))
print(f"Listening items where correctAnswer NOT in choices: {len(mismatch)}")
for lid, ca, ch in mismatch[:5]:
    print(f"  {lid}: correctAnswer={ca!r}, choices={ch}")
