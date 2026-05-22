"""Verify every claim in the 2026-05-22 native-teacher review against
current data BEFORE filing bugs (per procedure-manual F.41.4)."""
import sys, io, json, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load corpora
vocab = json.load(open(f"{REPO_N5}/data/vocab.json", encoding="utf-8"))
grammar = json.load(open(f"{REPO_N5}/data/grammar.json", encoding="utf-8"))
kanji_data = json.load(open(f"{REPO_N5}/data/kanji.json", encoding="utf-8"))
whitelist_kanji = json.load(open(f"{REPO_N5}/data/n5_kanji_whitelist.json", encoding="utf-8"))
dokkai_exception = json.load(open(f"{REPO_N5}/data/dokkai_kanji_exception.json", encoding="utf-8"))

# Normalize whitelist + exception sets
WL = set(whitelist_kanji if isinstance(whitelist_kanji, list) else whitelist_kanji.get("kanji", []))
EX = set(e["kanji"] for e in dokkai_exception["exception_kanji"] if isinstance(e, dict) and "kanji" in e)
ALLOWED = WL | EX
print(f"=== Setup: {len(WL)} whitelist kanji + {len(EX)} dokkai-exception = {len(ALLOWED)} allowed ===")
print()

# CJK kanji range U+4E00..U+9FFF (covers all common kanji)
KANJI_RE = re.compile(r"[一-鿿]")

# === S1.1: 99 vocab examples leak non-whitelist kanji ===
print("=== S1.1: Vocab example kanji whitelist violations ===")
vocab_entries = vocab if isinstance(vocab, list) else vocab.get("vocab", vocab.get("entries", []))
print(f"  vocab.json entries: {len(vocab_entries)}")
total_examples = 0
violations = []
by_provenance = {}
for entry in vocab_entries:
    if not isinstance(entry, dict): continue
    eid = entry.get("id") or entry.get("form")
    examples = entry.get("examples") or []
    for ex_idx, ex in enumerate(examples):
        if not isinstance(ex, dict): continue
        total_examples += 1
        ja = ex.get("ja") or ex.get("japanese") or ""
        prov = ex.get("provenance") or ex.get("_provenance") or "<untagged>"
        kanji_in_ex = set(KANJI_RE.findall(ja))
        offending = kanji_in_ex - ALLOWED
        if offending:
            violations.append((eid, ex_idx, ja, sorted(offending), prov))
            by_provenance.setdefault(prov, {"viol": 0, "total": 0})["viol"] += 1
        if prov:
            by_provenance.setdefault(prov, {"viol": 0, "total": 0})["total"] = by_provenance.get(prov, {}).get("total", 0) + 1
# rebuild total counts per provenance
prov_totals = {}
for entry in vocab_entries:
    if not isinstance(entry, dict): continue
    for ex in entry.get("examples") or []:
        if not isinstance(ex, dict): continue
        prov = ex.get("provenance") or ex.get("_provenance") or "<untagged>"
        prov_totals[prov] = prov_totals.get(prov, 0) + 1

print(f"  total examples scanned: {total_examples}")
print(f"  violations (examples with offending kanji): {len(violations)}")
print(f"  by provenance:")
for prov, total in sorted(prov_totals.items()):
    v = by_provenance.get(prov, {}).get("viol", 0)
    print(f"    {prov}: {v} / {total} ({100*v/total:.1f}%)")

# Top offending kanji
from collections import Counter
offending_counter = Counter()
for _, _, _, off, _ in violations:
    for k in off:
        offending_counter[k] += 1
print(f"  top 20 offending kanji: {offending_counter.most_common(20)}")

# Spot-check the specific cases the review listed
print()
print("  Spot-checks against review-listed cases:")
spot_targets = [
    ("びょう", "待"), ("一", "杯"), ("万", "借"), ("先週", "都"),
    ("はれ", "予"), ("ねこ", "匹"), ("どなた", "様"), ("め", "夜"),
]
for form_kana, expected_kanji in spot_targets:
    found = False
    for vid, idx, ja, off, prov in violations:
        # vid might be like "n5.vocab.10-time-general.びょう"
        if vid and form_kana in str(vid):
            if expected_kanji in off:
                print(f"    {form_kana}/{expected_kanji}: ✓ verified in violations (id={vid}, idx={idx}, prov={prov})")
                found = True
                break
    if not found:
        # broader search across all examples
        for entry in vocab_entries:
            if not isinstance(entry, dict): continue
            form = entry.get("form") or ""
            reading = entry.get("reading") or ""
            if form_kana in (form, reading):
                for idx, ex in enumerate(entry.get("examples") or []):
                    if isinstance(ex, dict) and expected_kanji in (ex.get("ja") or ""):
                        print(f"    {form_kana}/{expected_kanji}: ✓ found in entry form={form} (idx={idx})")
                        found = True
                        break
                if found: break
    if not found:
        print(f"    {form_kana}/{expected_kanji}: ✗ NOT found in violations")

# === S1.2: n5-017 / n5-045 duplicate ===
print()
print("=== S1.2: n5-017 / n5-045 duplicate check ===")
grammar_list = grammar if isinstance(grammar, list) else grammar.get("patterns", grammar.get("grammar", []))
for gid in ["n5-017", "n5-045"]:
    m = [e for e in grammar_list if isinstance(e, dict) and e.get("id") == gid]
    if m:
        e = m[0]
        print(f"  {gid}: pattern={e.get('pattern')!r} meaning_en={(e.get('meaning_en') or '')[:60]!r}")
        contrasts = e.get("contrasts") or e.get("common_mistakes") or []
        # Look for self-identification as duplicate
        text = json.dumps(e, ensure_ascii=False)
        if "duplicate" in text.lower() or "canonical" in text.lower():
            print(f"    *** Contains 'duplicate' or 'canonical' in entry: TRUE ***")
            for c in contrasts if isinstance(contrasts, list) else []:
                if isinstance(c, dict) and ("duplicate" in str(c).lower() or "canonical" in str(c).lower()):
                    print(f"      contrast/note: {str(c)[:120]}")
        else:
            print(f"    No 'duplicate'/'canonical' self-reference text found")

# === S1.3: かれ / かのじょ glosses ===
print()
print("=== S1.3: かれ/かのじょ gloss check ===")
for target in ["かれ", "かのじょ"]:
    for entry in vocab_entries:
        if not isinstance(entry, dict): continue
        form = entry.get("form") or ""
        reading = entry.get("reading") or ""
        if target in (form, reading):
            gloss = entry.get("gloss") or entry.get("meaning") or entry.get("meaning_en") or ""
            gloss_hi = entry.get("gloss_hi") or entry.get("meaning_hi") or ""
            print(f"  {target} (form={form}): gloss={gloss!r}")
            print(f"    gloss_hi={gloss_hi!r}")
            break

# === S1.4: あなた gloss + caveat ===
print()
print("=== S1.4: あなた gloss check ===")
for entry in vocab_entries:
    if not isinstance(entry, dict): continue
    form = entry.get("form") or ""
    reading = entry.get("reading") or ""
    if "あなた" in (form, reading):
        gloss = entry.get("gloss") or entry.get("meaning") or entry.get("meaning_en") or ""
        usage = entry.get("usage_note") or entry.get("note") or ""
        examples = entry.get("examples") or []
        print(f"  あなた (form={form}): gloss={gloss!r}")
        print(f"    usage_note={usage!r}")
        if examples:
            print(f"    first example: {examples[0].get('ja', '') if isinstance(examples[0], dict) else examples[0]}")
        break

# === S2.1: おはし section ===
print()
print("=== S2.1: おはし / はし section check ===")
for entry in vocab_entries:
    if not isinstance(entry, dict): continue
    form = entry.get("form") or ""
    if form in ("はし", "おはし") or "tableware" in (entry.get("section") or "").lower():
        section = entry.get("section") or ""
        if form in ("はし", "おはし") or "20. Tableware" in section:
            print(f"  form={form!r} reading={entry.get('reading')!r} section={section!r}")

# Also enumerate all section-20 entries
print()
print("  Entries currently in any '20.' section:")
sec20 = [e for e in vocab_entries if isinstance(e, dict) and (e.get("section") or "").startswith("20.")]
sec19 = [e for e in vocab_entries if isinstance(e, dict) and (e.get("section") or "").startswith("19.")]
for e in sec20[:5]:
    print(f"    section='{e.get('section')}' form={e.get('form')!r}")
print(f"  total section 20: {len(sec20)}, total section 19: {len(sec19)}")

# === S2.2: えいが section ===
print()
print("=== S2.2: えいが section check ===")
for entry in vocab_entries:
    if not isinstance(entry, dict): continue
    if (entry.get("form") or "") in ("えいが", "映画") or (entry.get("reading") or "") == "えいが":
        print(f"  form={entry.get('form')!r} reading={entry.get('reading')!r} section={entry.get('section')!r}")

# === S2.3: 三 mnemonic ===
print()
print("=== S2.3: 三 kanji mnemonic check ===")
kanji_list = kanji_data if isinstance(kanji_data, list) else kanji_data.get("entries", kanji_data.get("kanji", []))
for entry in kanji_list:
    if not isinstance(entry, dict): continue
    if entry.get("kanji") == "三" or entry.get("form") == "三" or entry.get("character") == "三":
        mn = entry.get("mnemonic") or entry.get("mnemonic_en") or ""
        print(f"  三 mnemonic: {mn[:200]!r}")
        break

# === S2.4: pitch accent values ===
print()
print("=== S2.4: pitch accent check (これ, みなさん, きのう, あなた) ===")
for target in ["これ", "みなさん", "きのう", "あなた"]:
    for entry in vocab_entries:
        if not isinstance(entry, dict): continue
        form = entry.get("form") or ""
        reading = entry.get("reading") or ""
        if target in (form, reading):
            pa = entry.get("pitch_accent") or entry.get("pitch_marks") or {}
            print(f"  {target}: form={form} reading={reading} pitch_accent={pa}")
            break

# === S3.2: Q-0226 ===
print()
print("=== S3.2: Q-0226 check ===")
qs = json.load(open(f"{REPO_N5}/data/questions.json", encoding="utf-8"))
qlist = qs if isinstance(qs, list) else qs.get("questions", [])
for q in qlist:
    if isinstance(q, dict) and q.get("id") in ("q-0226", "Q-0226", "q-226", "Q0226"):
        print(f"  id={q.get('id')}")
        print(f"  question_ja={q.get('question_ja') or q.get('question') or ''}")
        print(f"  correctAnswer={q.get('correctAnswer')}")
        print(f"  explanation_en={(q.get('explanation_en') or '')[:120]}")
        break

# === S3.4: 七 primary + reading_rule ===
print()
print("=== S3.4: 七 primary + reading_rule ===")
for entry in kanji_list:
    if not isinstance(entry, dict): continue
    if entry.get("kanji") == "七" or entry.get("form") == "七" or entry.get("character") == "七":
        print(f"  primary_reading={entry.get('primary_reading')!r}")
        print(f"  on={entry.get('on')!r} kun={entry.get('kun')!r}")
        print(f"  reading_rule={(entry.get('reading_rule') or '')[:200]!r}")
        break

# === S3.5: pronoun counter ===
print()
print("=== S3.5: pronoun counter check ===")
pronoun_entries = []
for entry in vocab_entries:
    if not isinstance(entry, dict): continue
    form = entry.get("form") or ""
    pos = entry.get("pos") or ""
    section = entry.get("section") or ""
    if "pronoun" in pos.lower() or "1. People" in section or form in ("わたし", "あなた", "かれ", "かのじょ", "わたしたち"):
        counter = entry.get("counter")
        if counter:
            pronoun_entries.append((form, counter))
print(f"  Pronoun entries with counter field: {len(pronoun_entries)}")
for f, c in pronoun_entries[:8]:
    print(f"    {f}: counter={c}")
