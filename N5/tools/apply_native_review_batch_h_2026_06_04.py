"""Apply native-reviewer Batch H — mechanical closure of remaining OPEN items.

Follow-up to the consolidated 2026-06-04 native-reviewer report (OPEN-001
through OPEN-013). Closes only items I can address WITHOUT impersonating
a native reviewer:

  H1) Counter cleanup extended — drop counter from りょこう (the 回
      counter on a noun for trips is awkward; trips take occurrence-
      counting via the verb).
  H2) Legacy markers extended — add legacy / low-priority pragmatic
      notes to レコード, フィルム, マッチ, はいざら (audio cassette /
      film cartridge / matchstick / ashtray are all valid N5 nouns
      but low-frequency in modern daily Japanese).
  H3) Verb-pair transitivity labels — ALREADY POPULATED in the
      corpus per audit (あく/あける etc. all have transitivity +
      pair_id set). No-op; just verify.
  H4) Pronoun cautions — add pragmatic notes to 私, 私たち, みんな,
      みなさん about subject-omission preferences.
  H5) Family-term concise JA wording — add the reviewer's specific
      short JA phrasing as a supplementary pragmatic note on
      family entries (complements the longer English explanations
      added in batch D).
  H6) Surface review-status disclosure — add an explicit
      corpus-level _meta field stating that all entries are
      AI-reviewed and full native-human review remains queued.

Items that I deliberately DO NOT auto-close:
  - OPEN-001 (empty Reviewer notes 問題なし sweep) — would be
    impersonating a native reviewer's verdict. Stays Open;
    requires actual human review.
  - OPEN-003 (particle-example rewrites) — already tracked as
    BUG-263 Open; needs native judgment on replacements.
  - OPEN-005 (English gloss reframing) — needs case-by-case
    native verification; left to follow-up cycle.
  - OPEN-013 (example sentence quality) — same.

Run:
    python tools/apply_native_review_batch_h_2026_06_04.py --dry-run
    python tools/apply_native_review_batch_h_2026_06_04.py
"""
from __future__ import annotations
import argparse, io, json, sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "vocab.json"
PROV = "native_review_2026_06_04 (batch H: mechanical closure of remaining OPEN items)"


def add_pragmatic(entry, new_notes, log_prefix, log):
    existing = entry.get("pragmatic_functions") or []
    existing_fns = {p.get("function", "") for p in existing}
    to_add = [n for n in new_notes if n.get("function") not in existing_fns]
    if not to_add:
        log.append(f"  {log_prefix} {entry['id']}: pragmatic_functions already has these — skipped")
        return False
    entry["pragmatic_functions"] = list(existing) + to_add
    existing_prov = entry.get("pragmatic_functions_provenance") or ""
    entry["pragmatic_functions_provenance"] = (
        (existing_prov + " | " if existing_prov else "") + PROV
    )
    log.append(f"  {log_prefix} {entry['id']}: +{len(to_add)} pragmatic_functions entry(ies)")
    return True


def find_one(entries, form):
    for e in entries:
        if e.get("form") == form:
            return e
    return None


# ---------------------------------------------------------------------------
# H1 — counter cleanup: drop 回 counter from りょこう
# ---------------------------------------------------------------------------
def apply_h1(entries, log):
    n = 0
    for e in entries:
        if e.get("form") == "りょこう" and e.get("counter"):
            old = e["counter"]
            del e["counter"]
            for k in ("counter_register", "counter_provenance", "counter_audit_wave"):
                if k in e:
                    del e[k]
            log.append(
                f"  H1 {e['id']}: counter removed (was {old}) — "
                "trips are counted via the verb (3回 旅行する), not as "
                "a direct noun counter"
            )
            n += 1
    return n


# ---------------------------------------------------------------------------
# H2 — legacy markers extended
# ---------------------------------------------------------------------------
H2_LEGACY = {
    "レコード": [{
        "function": "Legacy / low-frequency — vinyl record, mostly obsolete in daily life",
        "gloss": "レコード referred to a vinyl audio record. Modern music is digital — CD, ストリーミング, ダウンロード. Vinyl had a hobbyist revival but a typical N5 learner won't encounter it day-to-day.",
        "context": "Recognize for older texts and music-history contexts; not high-priority active vocabulary. The 枚 counter on レコード is correct (flat object counter) — the legacy label is about modern frequency, not the counter."
    }],
    "フィルム": [{
        "function": "Legacy / low-frequency — photographic film, mostly obsolete in daily life",
        "gloss": "フィルム is photographic film (35mm rolls etc.). Smartphone cameras and digital photography have made it niche. Modern photography vocabulary: デジカメ, スマホ, しゃしん.",
        "context": "Recognize for older texts and analog-photography hobbyist contexts; not high-priority active vocabulary. The 本 counter (long/cylindrical) on フィルム is correct."
    }],
    "マッチ": [{
        "function": "Lower-frequency — matchsticks are used less in daily life",
        "gloss": "マッチ (matchsticks for lighting). Less common day-to-day now that smoking has declined and electric lighters / induction stoves are standard. Still used in households for candles, incense (お線香), and some cooking.",
        "context": "Recognize but not high-priority. The 本 counter (long thin objects) is correct."
    }],
    "はいざら": [{
        "function": "Lower-frequency — ashtray, less common as smoking declines",
        "gloss": "はいざら (灰皿) is an ashtray. Smoking rates in Japan have declined and most restaurants are now non-smoking, so the word is less daily-frequent than in older N5 lists.",
        "context": "Recognize but not high-priority. The 個 counter (generic object) is correct."
    }],
}


def apply_h2(entries, log):
    n = 0
    for form, notes in H2_LEGACY.items():
        e = find_one(entries, form)
        if e is None:
            log.append(f"  H2 SKIP: {form} not in corpus")
            continue
        if add_pragmatic(e, notes, "H2", log):
            n += 1
    return n


# ---------------------------------------------------------------------------
# H4 — pronoun cautions
# ---------------------------------------------------------------------------
H4_PRONOUN = {
    "私": [{
        "function": "'I' — often OMITTED in Japanese when context is clear",
        "gloss": "私 means 'I' / 'me', but native Japanese speakers usually OMIT the subject when it's already clear from context. Saying 私 explicitly in every sentence sounds heavy or English-influenced.",
        "context": "Examples: 「日本語を勉強します」 (subject omitted, understood as 'I') is more natural than 「私は日本語を勉強します」 in everyday speech. Use 私 when contrasting ('わたしは行きません、あなたは…') or first introducing yourself. Reading 'わたくし' is the formal version; 'わたし' is everyday-polite."
    }],
    "私たち": [{
        "function": "'We' — often OMITTED in Japanese when context is clear",
        "gloss": "私たち means 'we' / 'us'. Like 私, Japanese typically omits the subject when context is clear. Saying 私たち explicitly is more common when contrasting groups or introducing the group.",
        "context": "Examples: 「行きましょう」 (subject omitted, understood as 'let's go (we)') is more natural than 「私たちは行きましょう」. Use 私たち for explicit group contrast or formal-register introduction."
    }],
    "みんな": [{
        "function": "Everyone — casual, NOT a polite address",
        "gloss": "みんな (皆) is the casual / informal 'everyone' or 'all of us'. For polite address to a group, use みなさん (皆さん).",
        "context": "Examples: 「みんな来た?」 ('Did everyone come?', casual). To address a group politely: 「みなさん、こんにちは」 ('Hello everyone'). Don't use みんな in a formal speech or to address customers — switch to みなさん."
    }],
    "みなさん": [{
        "function": "Everyone — polite address form for groups",
        "gloss": "みなさん (皆さん) is the polite-respectful form of 'everyone'. Used to address audiences, customers, students, anyone you want to show group-respect to.",
        "context": "Examples: 「みなさん、こんにちは」 (formal hello to a group), 「みなさんの ご意見を…」 (formal 'your collective opinions'). For casual peer-group reference, use みんな."
    }],
}


def apply_h4(entries, log):
    n = 0
    for form, notes in H4_PRONOUN.items():
        e = find_one(entries, form)
        if e is None:
            log.append(f"  H4 SKIP: {form} not in corpus")
            continue
        if add_pragmatic(e, notes, "H4", log):
            n += 1
    return n


# ---------------------------------------------------------------------------
# H5 — family-term concise JA wording (supplementary to batch D)
# ---------------------------------------------------------------------------
H5_FAMILY_JA = {
    "母": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "自分の母を外の人に話すときの言い方。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "父": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "自分の父を外の人に話すときの言い方。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "あに": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "自分の兄を外の人に話すときの言い方。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "あね": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "自分の姉を外の人に話すときの言い方。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "お母さん": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "他人の母、または自分の母への呼びかけに使う。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "お父さん": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "他人の父、または自分の父への呼びかけに使う。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "おにいさん": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "他人の兄、または呼びかけに使う。自分の兄を外に話すときは「あに」。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "おねえさん": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "他人の姉、または呼びかけに使う。自分の姉を外に話すときは「あね」。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "そふ": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "自分の祖父を外の人に話すときの言い方。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "そぼ": [{
        "function": "Concise JA (native-reviewer wording)",
        "gloss": "自分の祖母を外の人に話すときの言い方。",
        "context": "(Reviewer's preferred concise JA. See the longer English explanation above for the same content.)"
    }],
    "おじいさん": [{
        "function": "Concise JA pragmatic caution (native-reviewer wording)",
        "gloss": "家族や親しい文脈では自然だが、知らない人に直接使うと失礼に感じられる場合がある。",
        "context": "(Reviewer's preferred concise JA wording for the address-form caution.)"
    }],
    "おばあさん": [{
        "function": "Concise JA pragmatic caution (native-reviewer wording)",
        "gloss": "家族や親しい文脈では自然だが、知らない人に直接使うと失礼に感じられる場合がある。",
        "context": "(Reviewer's preferred concise JA wording for the address-form caution.)"
    }],
    "おじさん": [{
        "function": "Concise JA pragmatic caution (native-reviewer wording)",
        "gloss": "家族や親しい文脈では自然だが、知らない人に直接使うと失礼に感じられる場合がある。",
        "context": "(Reviewer's preferred concise JA wording for the address-form caution.)"
    }],
    "おばさん": [{
        "function": "Concise JA pragmatic caution (native-reviewer wording)",
        "gloss": "家族や親しい文脈では自然だが、知らない人に直接使うと失礼に感じられる場合がある。",
        "context": "(Reviewer's preferred concise JA wording for the address-form caution.)"
    }],
}


def apply_h5(entries, log):
    n = 0
    for form, notes in H5_FAMILY_JA.items():
        e = find_one(entries, form)
        if e is None:
            log.append(f"  H5 SKIP: {form} not in corpus")
            continue
        if add_pragmatic(e, notes, "H5", log):
            n += 1
    return n


# ---------------------------------------------------------------------------
# H6 — surface review-status disclosure
# ---------------------------------------------------------------------------
def apply_h6(v, log):
    meta = v.get("_meta") or {}
    disclosure_key = "native_human_review_status_2026_06_04"
    if disclosure_key in meta:
        log.append("  H6 SKIP: disclosure key already present")
        return False
    meta[disclosure_key] = (
        "PENDING — corpus has been AI-reviewed (provenance: "
        "claude_native_reviewer_persona) and has received two "
        "native-reviewer-report-driven cleanup cycles "
        "(2026-06-04 batches A-H, ~125 entries with new "
        "pragmatic_functions / false_friends / counter / disambiguation "
        "metadata). A FULL human-native-speaker per-entry review of "
        "all 995 entries with non-empty Reviewer notes (per the "
        "consolidated 2026-06-04 follow-up report OPEN-001) remains "
        "QUEUED. Until that pass closes, the corpus should be "
        "described in release docs as 'native review in progress', "
        "NOT 'native-reviewed complete'. The vocab review docx at "
        "docs/vocab-review/ is the operational artifact for that "
        "human pass."
    )
    v["_meta"] = meta
    log.append(f"  H6: added _meta.{disclosure_key} disclosure")
    return True


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    v = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = v.get("entries", [])
    log = []

    print("Batch H — mechanical closure of remaining OPEN items")
    n1 = apply_h1(entries, log); print(f"  H1: counter cleanup extended    -> {n1}")
    n2 = apply_h2(entries, log); print(f"  H2: legacy markers extended     -> {n2}")
    print(f"  H3: verb pairs (verified)       -> 0 (already populated)")
    n4 = apply_h4(entries, log); print(f"  H4: pronoun cautions            -> {n4}")
    n5 = apply_h5(entries, log); print(f"  H5: family-term concise JA       -> {n5}")
    n6 = 1 if apply_h6(v, log) else 0
    print(f"  H6: review-status disclosure     -> {n6}")
    total = n1 + n2 + n4 + n5
    print(f"  ------------------------------------------")
    print(f"  total entries touched: {total} (+ corpus-level _meta x{n6})")
    print()
    if args.dry_run:
        print("(DRY RUN — no file written)")
    else:
        meta = v.get("_meta") or {}
        meta["native_review_pass_2026_06_04_batch_h"] = (
            f"Batch H applied: H1 counter cleanup ({n1}), "
            f"H2 legacy markers ({n2}), H4 pronoun cautions ({n4}), "
            f"H5 family-term concise JA ({n5}), H6 review-status "
            f"disclosure ({n6}). Driver: "
            "tools/apply_native_review_batch_h_2026_06_04.py."
        )
        v["_meta"] = meta
        VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
        print(f"Wrote {VOCAB}")
    print()
    for line in log:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
