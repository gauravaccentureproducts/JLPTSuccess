"""Brutal-honesty re-audit — find issues that 30-sample passes missed.

Run from N5/:
    python tools/brutal_honesty_audit_2026_05_17.py
"""
from __future__ import annotations

import glob
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))

findings: list[tuple[str, str, str]] = []


def add(scenario_id: str, severity: str, msg: str) -> None:
    findings.append((scenario_id, severity, msg))
    print(f"  [{severity}] {scenario_id}: {msg}")


def section(name: str) -> None:
    print(f"\n=== {name} ===")


# ===== A. Japanese language — deep samples =====
def deep_japanese():
    section("A. Japanese language — DEEP audit")
    G = json.load(open("data/grammar.json", encoding="utf-8"))
    V = json.load(open("data/vocab.json", encoding="utf-8"))
    L = json.load(open("data/listening.json", encoding="utf-8"))
    R = json.load(open("data/reading.json", encoding="utf-8"))

    # A-001/002: scan ALL 1782 grammar examples for wh+は anti-patterns (not just sample)
    wh_words = ("だれ", "なに", "なん", "いつ", "どこ", "どれ", "どの", "どう", "どんな")
    wh_ha_issues = []
    for p in G.get("patterns") or []:
        pid = p.get("id")
        for i, ex in enumerate(p.get("examples") or []):
            if not isinstance(ex, dict):
                continue
            ja = ex.get("ja", "") or ""
            for wh in wh_words:
                if f"{wh}は" in ja and not any(c in ja for c in ("、", "ですが")):
                    # Allow contrastive context
                    wh_ha_issues.append((pid, i, ja, wh))
    print(f"  A-005 FULL scan: {len(wh_ha_issues)} wh+は anti-patterns")
    for pid, i, ja, wh in wh_ha_issues[:5]:
        print(f"    {pid} ex[{i}]: {ja[:70]!r}")

    # A-014: full counter rendaku scan ON GRAMMAR + VOCAB + LISTENING + READING + QUESTIONS
    wrong_rendaku = [
        "いちふん", "じゅうふん", "いちほん", "さんほん", "ろくほん",
        "はちほん", "じゅうほん", "じゅういちほん", "にじゅうほん",
        "いちひき", "さんひき", "ろくひき", "はちひき", "じゅうひき",
        "いちこ", "ろくこ", "はちこ", "じゅうこ",
    ]
    rendaku_hits = []
    for path in ("data/grammar.json", "data/vocab.json", "data/listening.json",
                 "data/reading.json", "data/questions.json"):
        d = json.load(open(path, encoding="utf-8"))

        def walk(o, p=""):
            if isinstance(o, dict):
                for k, v in o.items():
                    yield from walk(v, f"{p}.{k}")
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    yield from walk(v, f"{p}[{i}]")
            elif isinstance(o, str):
                yield (p, o)

        for path_in, s in walk(d):
            for w in wrong_rendaku:
                if w in s:
                    # Filter pedagogical-wrong-example fields
                    if "wrong" in path_in.lower() or ".wrong" in path_in:
                        continue
                    rendaku_hits.append((path, path_in, w, s[:60]))
    print(f"  A-014 FULL scan: {len(rendaku_hits)} wrong-rendaku hits "
          "(excluding pedagogical wrong_corrected_pair[].wrong fields)")
    for fp, p, w, s in rendaku_hits[:10]:
        print(f"    {fp.split('/')[-1]} {p}: {w!r} in {s!r}")
    if rendaku_hits:
        add("A-014", "Major", f"FULL scan found {len(rendaku_hits)} additional wrong-rendaku hits beyond the 13 already fixed")

    # A-010: i-adj vs na-adj — verify every adjective declared one or the other,
    # and check examples agree
    n_adj_mistag = 0
    for e in V["entries"]:
        if not isinstance(e, dict):
            continue
        pos = e.get("pos", "")
        form = e.get("form", "")
        reading = e.get("reading", "")
        if "い-adj" in pos or "i-adj" in pos.lower():
            # i-adj should end in い (kana)
            if reading and not reading.endswith("い"):
                add("A-010", "Major", f"i-adj {form!r} reading={reading!r} doesn't end in い")
                n_adj_mistag += 1
        elif "な-adj" in pos or "na-adj" in pos.lower():
            # na-adj typically does NOT end in い (but some do: e.g. きらい, ゆうめい — these are na-adj despite い ending)
            # No strict check — just look for obvious mis-tag
            pass
    print(f"  A-010 i-adj/na-adj mistag scan: {n_adj_mistag} findings")

    # A-009: verb-class consistency on every verb entry
    for e in V["entries"]:
        if not isinstance(e, dict):
            continue
        pos = (e.get("pos", "") or "").lower()
        form = e.get("form", "")
        reading = e.get("reading", "")
        if "verb-3" in pos or "irregular" in pos:
            # Check known irregulars
            if not (form.endswith("する") or form.endswith("くる") or form == "来る"
                    or reading.endswith("する") or reading.endswith("くる")):
                # Some compound irregulars (べんきょうする, etc.) are fine
                continue

    # Cross-file duplicate-form check on vocab.json
    form_to_idx = defaultdict(list)
    for i, e in enumerate(V["entries"]):
        if isinstance(e, dict) and e.get("form"):
            form_to_idx[e["form"]].append(i)
    dups = {f: idxs for f, idxs in form_to_idx.items() if len(idxs) > 1}
    print(f"  Vocab same-form distinct entries: {len(dups)}")
    for f, idxs in list(dups.items())[:5]:
        readings = [V["entries"][i].get("reading") for i in idxs]
        print(f"    {f!r}: idx={idxs}, readings={readings}")

    # A-024..026: deeper translation aspect check
    n_pairs = 0
    issues_trans = []
    for p in G.get("patterns") or []:
        for i, ex in enumerate(p.get("examples") or []):
            if not isinstance(ex, dict):
                continue
            ja = ex.get("ja", "") or ""
            en = ex.get("translation_en", "") or ""
            if not ja or not en:
                continue
            n_pairs += 1
            # Check past-marker mismatch
            ja_past = any(m in ja for m in ("ました", "た。", "でした", "かった"))
            en_lower = en.lower()
            past_verbs = (" was ", " were ", "went ", "came ", "did ", "made ",
                          "ate ", "bought ", "saw ", "wrote ", "studied ",
                          "lived ", "took ", "drank ", "read ", "spoke ",
                          "met ", "gave ", "called ")
            past_ed = re.search(r"\b\w+ed\b", en_lower)
            en_past = any(v in en_lower for v in past_verbs) or past_ed
            if ja_past and not en_past:
                issues_trans.append((p.get("id"), i, ja, en))
    print(f"  A-025 deep aspect check: {n_pairs} pairs scanned, {len(issues_trans)} JA-past / EN-not-past potential issues")
    for pid, i, ja, en in issues_trans[:5]:
        print(f"    {pid} ex[{i}]: ja={ja[:50]!r}  en={en[:50]!r}")

    # Romaji leakage in user-facing fields (excluding _meta + provenance)
    romaji_in_jp = []
    for p in G.get("patterns") or []:
        for i, ex in enumerate(p.get("examples") or []):
            if isinstance(ex, dict):
                ja = ex.get("ja", "") or ""
                # ASCII alpha letters present in JA field
                if re.search(r"[a-zA-Z]{3,}", ja):
                    romaji_in_jp.append((p.get("id"), i, ja))
    print(f"  Romaji in grammar ja fields: {len(romaji_in_jp)}")
    for pid, i, ja in romaji_in_jp[:5]:
        print(f"    {pid} ex[{i}]: {ja!r}")


# ===== C. Hindi locale =====
def deep_hindi():
    section("C. Hindi locale — DEEP audit")
    files = ["data/grammar.json", "data/vocab.json", "data/reading.json",
             "data/listening.json", "data/questions.json"]
    # Scan ALL Hindi fields for: English-intrusion, English-possessive 's,
    # mixed-script issues
    all_hi = []
    for path in files:
        d = json.load(open(path, encoding="utf-8"))

        def walk(o, p=""):
            if isinstance(o, dict):
                for k, v in o.items():
                    if isinstance(k, str) and (k.endswith("_hi") or k == "l1_notes"):
                        if isinstance(v, str) and v.strip():
                            yield (path, f"{p}.{k}", v)
                        elif isinstance(v, dict):
                            for kk, vv in v.items():
                                if kk == "hi" and isinstance(vv, str) and vv.strip():
                                    yield (path, f"{p}.{k}.{kk}", vv)
                    yield from walk(v, f"{p}.{k}")
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    yield from walk(v, f"{p}[{i}]")

        for hit in walk(d):
            all_hi.append(hit)
    print(f"  Total Hindi strings scanned: {len(all_hi)}")

    # English-possessive 's after Devanagari noun
    poss_issues = []
    for path, p, s in all_hi:
        for m in re.finditer(r"[ऀ-ॿ]'s\b", s):
            poss_issues.append((path, p, s[:80], m.group(0)))
    print(f"  HI English-possessive 's intrusions: {len(poss_issues)}")
    for path, p, s, match in poss_issues:
        print(f"    {path.split('/')[-1]} {p}: match={match!r}  ctx={s!r}")
    if len(poss_issues) > 0:
        add("C-002", "Major", f"FULL scan found {len(poss_issues)} HI+'s intrusions beyond the 1 already fixed")

    # Untranslated technical terms — flag mid-text English of length >= 5
    untrans = []
    for path, p, s in all_hi:
        if len(s) < 30:
            continue
        # Look for ASCII words of 5+ letters mid-text
        ascii_words = re.findall(r"\b[A-Za-z]{5,}\b", s)
        # Filter known acceptable (Japanese-romanized terms, common borrowings)
        whitelist = {"please", "plain", "past", "form", "base", "Verb",
                     "Group", "type", "kanji", "kana", "verb", "noun",
                     "adjective", "particle", "nominalizer", "potential",
                     "stative", "stem", "Group 1", "Group 2", "hiragana",
                     "katakana", "yesterday", "today", "week", "month", "year",
                     "tomorrow", "weekend", "weekday", "morning", "evening",
                     "spring", "summer", "autumn", "winter", "Tokyo", "Japan",
                     "Hindi", "Japanese", "English", "school", "library",
                     "office", "Sunday", "Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "father", "mother",
                     "parents", "drop", "handakuten", "dakuten", "clause",
                     "potential", "transitive", "intransitive", "lends",
                     "borrows", "permission", "obligation"}
        suspicious = [w for w in ascii_words if w not in whitelist]
        if suspicious:
            untrans.append((path, p, suspicious[:3], s[:100]))
    print(f"  HI suspicious-English-intrusion entries (post-filter): {len(untrans)}")
    for path, p, words, s in untrans[:8]:
        print(f"    {path.split('/')[-1]} {p}: words={words!r}  ctx={s!r}")


# ===== B. JLPT format — re-check mondai distribution against JEES ranges =====
def deep_jlpt():
    section("B. JLPT format — DEEP audit")
    # Per JEES official N5 sample paper (2010):
    # 文字・語彙 section: M1 (kanji→reading) = 12; M2 (reading→kanji) = 8;
    #                    M3 (orthography) = 10; M4 (paraphrase) = 5
    # 文法・読解 section: M1 (grammar fill-blank) = 16; M2 (sentence construction) = 5;
    #                    M3 (passage coherence blank) = 5; M4 (short reading) = 3;
    #                    M5 (medium reading) = 2; M6 (info-search) = 1
    # 聴解 section: M1 (task understanding) = 7; M2 (point understanding) = 6;
    #             M3 (utterance expression) = 5; M4 (immediate response) = 6
    # Total: ~92 questions per single JEES paper

    # Our project ships 28 papers — total ~402 questions across multiple papers.
    expected_per_paper = {
        1: 12 + 16 + 7,  # Goi M1 + Bunpou M1 + Chokai M1 = 35
        2: 8 + 5 + 6,
        3: 10 + 5 + 5,
        4: 5 + 3 + 6,
        5: 2,
        6: 1,
    }
    print(f"  JEES canonical per-paper mondai count: {expected_per_paper}")

    # Count actual mondai per category
    cat_mondai_counts = defaultdict(lambda: defaultdict(int))
    for p in sorted(glob.glob("data/papers/**/*.json", recursive=True)):
        d = json.load(open(p, encoding="utf-8"))
        cat = d.get("category", "?")
        for q in d.get("questions", []):
            m = q.get("mondai")
            if m:
                cat_mondai_counts[cat][m] += 1
    print(f"  Per-category mondai distribution:")
    for cat, mondai in cat_mondai_counts.items():
        print(f"    {cat}: {dict(mondai)}")

    # B-004: deeper distractor plausibility — scan ALL mondai-1 (50 items)
    # for ANY distractor that doesn't pass phonetic-near or kun/on-confusion test
    # The canonical pattern is "wrong-reading distractors". Look for obviously
    # implausible distractors (random kana strings).
    poor_distractors = []
    for p in sorted(glob.glob("data/papers/goi/*.json") + glob.glob("data/papers/moji/*.json")):
        d = json.load(open(p, encoding="utf-8"))
        for q in d.get("questions", []):
            if q.get("mondai") != 1:
                continue
            choices = q.get("choices", []) or []
            ci = q.get("correctIndex", -1)
            if ci < 0 or ci >= len(choices):
                continue
            correct = choices[ci]
            for i, ch in enumerate(choices):
                if i == ci:
                    continue
                # Phonetic distance: if Levenshtein > len(correct), implausible
                # (excessive distance)
                if len(set(correct) & set(ch)) == 0:
                    poor_distractors.append((q.get("id"), correct, ch))
    print(f"  B-004 distractor zero-char-overlap (definitely-implausible): {len(poor_distractors)}")
    for qid, correct, ch in poor_distractors[:5]:
        print(f"    {qid}: correct={correct!r} distractor={ch!r}")

    # B-008: check passage length distribution more rigorously
    R = json.load(open("data/reading.json", encoding="utf-8"))
    too_short = 0
    too_long = 0
    for p in R.get("passages", []):
        # Combine all text content
        text = ""
        for k in ("text", "passage", "body", "content_ja", "content"):
            v = p.get(k)
            if isinstance(v, str):
                text = v
                break
        if text:
            text = re.sub(r"<[^>]+>", "", text)
            n = len(text)
            diff = p.get("difficulty", "")
            if diff == "easy" and n > 200:
                too_long += 1
                add("B-008", "Minor", f"easy passage {p.get('id')} is {n} chars (typical JEES easy: 60-150)")
            elif diff == "hard" and n < 200:
                too_short += 1
    print(f"  B-008 length-vs-difficulty mismatch: too_long={too_long}, too_short={too_short}")


# ===== F. Security — deep =====
def deep_security():
    section("F. SECURITY — DEEP audit")
    # Scan ALL JS files for: eval, innerHTML, dangerouslySetInnerHTML,
    # document.write, on{event}= attrs, src= with http(s)://
    js_findings = defaultdict(int)
    for path in glob.glob("js/*.js"):
        c = Path(path).read_text(encoding="utf-8", errors="ignore")
        if re.search(r"\beval\s*\(", c):
            js_findings["eval()"] += c.count("eval(")
            add("F-001", "Major", f"eval() in {path}")
        # innerHTML assignment is a real XSS vector if user-supplied
        if re.search(r"\.innerHTML\s*=", c):
            js_findings[".innerHTML="] += 1
        if re.search(r"document\.write\s*\(", c):
            js_findings["document.write"] += 1
            add("F-001", "Major", f"document.write in {path}")
        if re.search(r"\bonerror\s*=", c):
            js_findings["onerror="] += 1
    print(f"  JS hazard tallies: {dict(js_findings)}")

    # Check that innerHTML uses are safe (template literal with no user input)
    innerhtml_total = 0
    innerhtml_likely_safe = 0
    for path in glob.glob("js/*.js"):
        c = Path(path).read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"(\w+)\.innerHTML\s*=\s*([^;\n]+)", c):
            innerhtml_total += 1
            rhs = m.group(2).strip()
            # Safe-ish: backtick template literal with no user-input variables
            if rhs.startswith("`"):
                # Look for variables that aren't ESC- prefixed
                if not re.search(r"\$\{[^}]+\}", rhs):
                    innerhtml_likely_safe += 1
    print(f"  innerHTML uses: {innerhtml_total} total; likely-safe: {innerhtml_likely_safe}")

    # Check for external script src
    html = Path("index.html").read_text(encoding="utf-8")
    ext_scripts = re.findall(r"<script[^>]*src=[\"']https?://[^\"']+", html)
    print(f"  External <script src> in index.html: {len(ext_scripts)}")
    for s in ext_scripts:
        add("F-013", "Major", f"External script: {s[:80]}")


# ===== G. Privacy — deep =====
def deep_privacy():
    section("G. PRIVACY — DEEP audit")
    # Re-verify analytics-zero with stricter check (script tags + import + fetch)
    n_real = 0
    for path in glob.glob("**/*.js", recursive=True) + glob.glob("**/*.html", recursive=True):
        if "node_modules" in path or ".min." in path:
            continue
        try:
            c = Path(path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Look for actual integration code
        for pat in (r"<script[^>]*src=[\"'][^\"']*(?:analytics|tag-manager|amplitude|mixpanel|plausible\.io|segment\.io)",
                    r"fetch\([\"'][^\"']*(?:analytics|telemetry|tracking)",
                    r"navigator\.sendBeacon\s*\(",):
            if re.search(pat, c):
                n_real += 1
                add("G-001", "Critical", f"Possible analytics integration in {path}")
    print(f"  G-001 actual integration hits: {n_real}")

    # localStorage usage — verify namespace is jlpt-n5-tutor:*
    ls_uses = []
    for path in glob.glob("js/*.js"):
        c = Path(path).read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"localStorage\.(setItem|getItem|removeItem)\s*\(\s*[\"']([^\"']+)", c):
            ls_uses.append((path, m.group(2)))
    bad_ls = [u for u in ls_uses if not u[1].startswith("jlpt-n5-tutor")]
    print(f"  localStorage uses: {len(ls_uses)} total; non-namespaced: {len(bad_ls)}")
    for path, key in bad_ls[:5]:
        add("G-003", "Major", f"localStorage non-namespaced key {key!r} in {path}")

    # PII patterns in JS source / data
    pii_patterns = [
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "email"),
        (r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "phone-like"),
    ]
    for pat, name in pii_patterns:
        hits = 0
        for path in glob.glob("js/*.js"):
            c = Path(path).read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(pat, c):
                # Filter doc-comment / example mentions
                start = max(0, m.start() - 30)
                ctx = c[start: m.end() + 30]
                if "//" in ctx or "/*" in ctx or "example" in ctx.lower():
                    continue
                hits += 1
        print(f"  PII-{name} in js/*.js: {hits}")


# ===== I. Data engineering — duplicate IDs, cross-refs =====
def deep_data():
    section("I. DATA ENGINEERING — DEEP audit")
    # Vocab: duplicate IDs
    V = json.load(open("data/vocab.json", encoding="utf-8"))
    ids = [e.get("id") for e in V["entries"] if isinstance(e, dict)]
    id_counts = Counter(ids)
    dup_ids = {k: v for k, v in id_counts.items() if v > 1}
    print(f"  Vocab duplicate IDs: {len(dup_ids)}")
    for k, v in list(dup_ids.items())[:5]:
        add("I-010", "Major", f"vocab.json duplicate id {k!r} ({v} occurrences)")

    # Grammar: duplicate IDs
    G = json.load(open("data/grammar.json", encoding="utf-8"))
    g_ids = [p.get("id") for p in G["patterns"]]
    g_dup = {k: v for k, v in Counter(g_ids).items() if v > 1}
    print(f"  Grammar duplicate IDs: {len(g_dup)}")

    # Cross-corpus refs: verify every frequent_patterns entry resolves
    valid_pids = set(g_ids)
    unresolved = 0
    for e in V["entries"]:
        if not isinstance(e, dict):
            continue
        for fp in e.get("frequent_patterns", []) or []:
            if fp not in valid_pids:
                unresolved += 1
                add("I-017", "Major", f"vocab.json {e.get('id')!r} frequent_patterns contains unresolved {fp!r}")
    print(f"  Vocab frequent_patterns unresolved: {unresolved}")

    # Questions: grammarPatternId references resolve
    Q = json.load(open("data/questions.json", encoding="utf-8"))
    q_unresolved = 0
    for q in Q.get("questions", []):
        gpid = q.get("grammarPatternId")
        if gpid and gpid not in valid_pids:
            q_unresolved += 1
            if q_unresolved <= 5:
                add("I-017", "Major", f"questions.json {q.get('id')!r} grammarPatternId={gpid!r} unresolved")
    print(f"  Questions grammarPatternId unresolved: {q_unresolved}")


# ===== L. Cultural — character-name diversity =====
def deep_cultural():
    section("L. CULTURAL — DEEP audit")
    # Extract names from listening scripts + reading passages
    L = json.load(open("data/listening.json", encoding="utf-8"))
    R = json.load(open("data/reading.json", encoding="utf-8"))
    name_pat = re.compile(r"([A-Za-zぁ-ゖァ-ヿ一-鿿]{2,5}さん)")
    names = Counter()
    for it in L.get("items", []):
        s = it.get("script_ja", "") or ""
        for m in name_pat.finditer(s):
            names[m.group(1)] += 1
    for p in R.get("passages", []):
        for k in ("text", "passage", "body", "content_ja", "content"):
            v = p.get(k)
            if isinstance(v, str):
                for m in name_pat.finditer(v):
                    names[m.group(1)] += 1
                break
    print(f"  Distinct character-names: {len(names)}")
    print(f"  Top 10: {names.most_common(10)}")
    if len(names) > 0:
        top = names.most_common(1)[0]
        total = sum(names.values())
        ratio = top[1] / total
        print(f"  Most-common name ratio: {ratio:.2f} ({top})")
        if ratio > 0.4:
            add("L-010", "Medium", f"Name concentration too high: {top[0]} appears {top[1]}/{total} = {ratio:.0%}")


def main() -> int:
    deep_japanese()
    deep_hindi()
    deep_jlpt()
    deep_security()
    deep_privacy()
    deep_data()
    deep_cultural()

    print(f"\n=== TOTAL FINDINGS: {len(findings)} ===")
    by_sev = Counter(f[1] for f in findings)
    print(f"  By severity: {dict(by_sev)}")
    return 0 if len(findings) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
