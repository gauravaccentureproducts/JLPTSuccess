"""Apply native-reviewer batches A-D from the 2026-06-04 review report.

Batches:
  A. Sense de-contamination — fix the polite-person かた entry's
     particle_examples (currently shared with way-of-doing kata).
  B. Homonym false_friends sweep — populate the false_friends array
     on every entry that shares a kana reading with another entry,
     cross-referencing the sibling form + gloss.
  C. Counter cleanup — drop counter field from collective / abstract
     entries where the headword isn't naturally individually counted.
  D. Family pragmatic notes — add pragmatic_functions entries to 16
     family/relative terms documenting uchi/soto usage.

Read backup at data/vocab.json.bak_2026_06_04_native_review_batches.
Run from N5/:
    python tools/apply_native_review_batches_2026_06_04.py --dry-run
    python tools/apply_native_review_batches_2026_06_04.py
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from collections import defaultdict
from pathlib import Path

# Force UTF-8 stdout — script contains em-dashes + Japanese in log lines,
# and Windows default cp932 console encoding crashes on —.
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "vocab.json"


def _find(entries, form, contains_id=None):
    """Find an entry by form; if multiple, optionally narrow by id substring."""
    matches = [e for e in entries if e.get("form") == form]
    if contains_id:
        matches = [e for e in matches if contains_id in (e.get("id") or "")]
    return matches


# ---------------------------------------------------------------------------
# BATCH A — sense de-contamination
# ---------------------------------------------------------------------------
# Reviewer-flagged: the polite-person かた entry has the SAME particle_examples
# as the way-of-doing かた entry. Both currently carry
#   ['読みかたは', '書きかたを', '読みかたを', '行きかたが']
# which all belong to the way-of-doing sense (Vstem + かた). The polite-person
# sense needs particle_examples that use kata-as-person (あの方, どの方,
# あの方が, あの方は).

BATCH_A_FIXES = {
    # (form, id_substring) -> new particle_examples
    ("かた", "1-people-pronouns-and-se"): [
        "あの方は",
        "あの方が",
        "どの方も",
        "あの方に",
    ],
}


def apply_batch_a(entries, log):
    count = 0
    for (form, id_sub), new_pe in BATCH_A_FIXES.items():
        matches = _find(entries, form, contains_id=id_sub)
        for e in matches:
            old_pe = e.get("particle_examples") or []
            e["particle_examples"] = list(new_pe)
            # Mark provenance so the audit trail is honest.
            e["particle_examples_provenance"] = (
                "native_review_2026_06_04 (batch A: sense de-contamination — "
                "earlier particle_examples were shared with the way-of-doing "
                "「〜かた」 entry and belonged to that sense; replaced with "
                "polite-person 「方」 collocations)"
            )
            log.append(f"  A. {e['id']}: particle_examples = {old_pe} → {new_pe}")
            count += 1
    return count


# ---------------------------------------------------------------------------
# BATCH B — homonym false_friends sweep
# ---------------------------------------------------------------------------
# For each kana reading that has ≥2 entries in the corpus, populate the
# false_friends array on each entry, cross-referencing the OTHER entries
# sharing that reading. The renderer already shows .false-friend-grid
# under a "Don't confuse with" heading; we just need to populate the field.
#
# The schema (per js/learn-vocab.js line 574) is: array of strings, each a
# vocab form to link to via /learn/vocab/<form>. Our scheme: include the
# sibling entry's form. The SPA renders each as a card linking to the
# other entry.
#
# IMPORTANT: we skip 4 reading-pair classes that aren't really homonyms:
#   - particles (が, と, から, に, は) that share readings with content
#     words — the particle entry already lives in section 35 with a
#     pos='particle' marker, the contrast is grammatically obvious.
#   - simple counter / number duplicates (ばん=番, ふく=服, ほん=本) where
#     entries with the same form differ only in metadata.
#   - kana/kanji duplicates of the SAME word (e.g., 'いくつ' twice — looks
#     like a corpus dedup leftover, not a homonym).
# The 13 pedagogically-risky pairs the reviewer named are all in the kept set.

# Skip-list rationale documented per entry.
B_SKIP_FORMS = {
    # particles — context disambiguates, schema marks pos='particle'
    "が", "と", "に", "は", "から", "も",
    # number / counter / number-word duplicates not homonyms
    "ふく", "ほん", "ばん", "に",  # 二 vs に (particle)
    # genuine-duplicate corpus rows (same word twice)
    "あの", "いくつ", "おく", "かい", "はい", "はる", "いれる",
    # cross-kanji same-meaning (e.g. ひ=日/火 are both "day" and "fire" -
    # genuinely distinct, but kept as separate kanji-headed entries; the
    # gloss already names the difference)
}


def apply_batch_b(entries, log):
    """For each reading with ≥2 entries, populate cross-references:

      - Cross-form pairs (different form, same reading): use the
        `false_friends` field with sibling forms. The SPA renderer
        already shows these as "Don't confuse with" cards that link
        to /learn/vocab/<form>. Works perfectly because each form
        has its own URL.

      - Same-form homonyms (identical form, different gloss): the SPA
        routes by form, so all senses share one URL — false_friends
        can't disambiguate. Route through `pragmatic_functions`
        instead — the renderer already shows it as a multi-sense
        block on the same page. Add ONE entry per same-form group
        listing all senses inline so the learner sees the
        disambiguation regardless of which sense the SPA happens to
        render.
    """
    by_reading = defaultdict(list)
    for e in entries:
        r = e.get("reading") or e.get("form") or ""
        if r:
            by_reading[r].append(e)

    count = 0
    for r, group in by_reading.items():
        if len(group) < 2:
            continue
        if r in B_SKIP_FORMS:
            continue
        forms = {e.get("form") for e in group}

        if len(forms) >= 2:
            # ---- Cross-form pair: use false_friends ----
            for e in group:
                this_form = e.get("form")
                others = [other.get("form") for other in group
                          if other.get("form") != this_form]
                seen = []
                for o in others:
                    if o and o not in seen:
                        seen.append(o)
                if not seen:
                    continue
                existing = e.get("false_friends") or []
                merged = list(existing)
                for f in seen:
                    if f not in merged:
                        merged.append(f)
                if merged != existing:
                    e["false_friends"] = merged
                    e["false_friends_provenance"] = (
                        "native_review_2026_06_04 (batch B: same-reading "
                        "cross-form homonym; reviewer recommended "
                        "explicit 'Don't confuse with' cross-links)"
                    )
                    log.append(
                        f"  B-x. {e['id']}: reading={r}  false_friends += {seen}"
                    )
                    count += 1
        else:
            # ---- Same-form homonym: use pragmatic_functions ----
            # All entries share the same form — the SPA serves them all
            # at the same URL and only renders one. Add a pragmatic_functions
            # block to EVERY entry in the group so whichever the SPA
            # happens to render, the learner sees the disambiguation.
            # Build a single combined block describing all senses.
            senses_summary = []
            for other in group:
                g = other.get("gloss") or ""
                senses_summary.append(f"{r} — {g}")
            summary_text = "  /  ".join(senses_summary)
            note = {
                "function": f"Same-kana homonym (multiple N5 senses)",
                "gloss": (
                    f"The kana 「{r}」 covers {len(group)} distinct N5 meanings: "
                    + summary_text
                ),
                "context": (
                    "Context (preceding particle, surrounding nouns, "
                    "kanji where written) disambiguates which sense is "
                    "intended. When writing, prefer the kanji form to "
                    "remove ambiguity."
                ),
            }
            for e in group:
                existing = e.get("pragmatic_functions") or []
                # Don't clobber existing native-curated pragmatic_functions;
                # only add when absent.
                if any(p.get("function", "").startswith("Same-kana homonym")
                       for p in existing):
                    continue
                merged = list(existing) + [note]
                e["pragmatic_functions"] = merged
                # Tag provenance distinctly from the cross-form case.
                existing_prov = e.get("pragmatic_functions_provenance") or ""
                e["pragmatic_functions_provenance"] = (
                    (existing_prov + " | " if existing_prov else "")
                    + "native_review_2026_06_04 (batch B: same-form "
                    "homonym disambiguation; SPA routes by form so "
                    "false_friends cannot disambiguate — multi-sense "
                    "summary surfaced here instead)"
                )
                log.append(
                    f"  B-s. {e['id']}: reading={r} form={e.get('form')!r}  "
                    f"+pragmatic_functions homonym-summary ({len(group)} senses)"
                )
                count += 1
    return count


# ---------------------------------------------------------------------------
# BATCH C — counter cleanup
# ---------------------------------------------------------------------------
# The reviewer specifically named 家族 and 両親 as having counter metadata
# that doesn't apply (collective nouns). Sweep the corpus for entries where
# the counter field is present but the headword is a known collective /
# abstract / functional non-count noun.

# Forms where counter must be dropped. Conservative list — only the reviewer-
# named pair plus same-class siblings I'm confident about.
BATCH_C_DROP_COUNTER_FORMS = {
    # Both 家族 and 両親 are stored kana-headed in the corpus.
    "かぞく",    # 家族 — collective noun; a household / group
    "りょうしん",  # 両親 — already refers to two parents as a set
    "家族",       # kanji form, if present
    "両親",       # kanji form, if present
    "みんな",     # 'everyone' — pronoun-like, not counted
    "ご家族",    # polite form of 家族 (if present)
}


def apply_batch_c(entries, log):
    count = 0
    for e in entries:
        if e.get("form") in BATCH_C_DROP_COUNTER_FORMS:
            if e.get("counter"):
                old = e["counter"]
                del e["counter"]
                if "counter_register" in e:
                    del e["counter_register"]
                if "counter_provenance" in e:
                    del e["counter_provenance"]
                if "counter_audit_wave" in e:
                    del e["counter_audit_wave"]
                log.append(
                    f"  C. {e['id']}: counter removed (was {old}) — "
                    f"{e.get('form')} is a collective/non-count noun"
                )
                count += 1
    return count


# ---------------------------------------------------------------------------
# BATCH D — family pragmatic notes (uchi / soto)
# ---------------------------------------------------------------------------
# Reviewer wants the practical use-when-speaking-to-outsiders / use-for-
# other-family / use-as-address distinction surfaced on every family entry.
# The pragmatic_functions field is the right home — the renderer already
# shows it in a 'Multiple uses (pragmatic)' section.

# Each note follows the schema: {function, gloss, context}.
BATCH_D_PRAGMATIC = {
    "母": [
        {"function": "Own mother (talking to outsiders)",
         "gloss": "Use 母 when referring to YOUR own mother in conversation with people outside your family.",
         "context": "Example: 「私の母は元気です」 — 'My mother is well.' Don't use お母さん in that position; that form is for someone else's mother or as a direct address."},
    ],
    "父": [
        {"function": "Own father (talking to outsiders)",
         "gloss": "Use 父 when referring to YOUR own father in conversation with people outside your family.",
         "context": "Example: 「父は会社員です」 — 'My father is a company employee.' For someone else's father, use お父さん."},
    ],
    "あに": [
        {"function": "Own older brother (talking to outsiders)",
         "gloss": "Use あに / 兄 when referring to YOUR own older brother in conversation with people outside your family.",
         "context": "For someone else's older brother, or as a direct address form within the family, use お兄さん."},
    ],
    "あね": [
        {"function": "Own older sister (talking to outsiders)",
         "gloss": "Use あね / 姉 when referring to YOUR own older sister in conversation with people outside your family.",
         "context": "For someone else's older sister, or as a direct address form within the family, use お姉さん."},
    ],
    "お母さん": [
        {"function": "Someone else's mother / address form",
         "gloss": "Use お母さん to refer politely to SOMEONE ELSE'S mother, or to address YOUR OWN mother directly.",
         "context": "When talking ABOUT your own mother to outsiders, switch to 母. The お…さん pattern marks respect for the referent, which is why it doesn't fit your own family in outward-facing reference."},
    ],
    "お父さん": [
        {"function": "Someone else's father / address form",
         "gloss": "Use お父さん to refer politely to SOMEONE ELSE'S father, or to address YOUR OWN father directly.",
         "context": "When talking ABOUT your own father to outsiders, switch to 父."},
    ],
    "おにいさん": [
        {"function": "Someone else's older brother / address form",
         "gloss": "Use お兄さん (おにいさん) for SOMEONE ELSE'S older brother, or to address your own older brother directly.",
         "context": "When talking about your own older brother to outsiders, use あに / 兄 instead."},
    ],
    "おねえさん": [
        {"function": "Someone else's older sister / address form",
         "gloss": "Use お姉さん (おねえさん) for SOMEONE ELSE'S older sister, or to address your own older sister directly.",
         "context": "When talking about your own older sister to outsiders, use あね / 姉 instead."},
    ],
    "そふ": [
        {"function": "Own grandfather (talking to outsiders)",
         "gloss": "Use 祖父 (そふ) when referring to YOUR own grandfather in conversation with people outside your family. More formal/literary than おじいさん.",
         "context": "Within the family or for someone else's grandfather, おじいさん is more common in spoken Japanese."},
    ],
    "そぼ": [
        {"function": "Own grandmother (talking to outsiders)",
         "gloss": "Use 祖母 (そぼ) when referring to YOUR own grandmother in conversation with people outside your family. More formal/literary than おばあさん.",
         "context": "Within the family or for someone else's grandmother, おばあさん is more common in spoken Japanese."},
    ],
    "おじいさん": [
        {"function": "Kinship / general elderly man / address",
         "gloss": "Used both for grandfathers (own or someone else's) and as a friendly term for an elderly man.",
         "context": "Pragmatic caution: using おじいさん to address an unrelated elderly man you don't know can sound presumptuous about their age — many Japanese speakers avoid it in cold-call situations and switch to 「すみません」 + a job/role title where possible."},
    ],
    "おばあさん": [
        {"function": "Kinship / general elderly woman / address",
         "gloss": "Used both for grandmothers (own or someone else's) and as a friendly term for an elderly woman.",
         "context": "Pragmatic caution: using おばあさん to address an unrelated elderly woman can sound presumptuous about their age. See おじいさん for the same caveat."},
    ],
    "おじさん": [
        {"function": "Uncle / middle-aged man / address",
         "gloss": "Used both for one's uncle (own or someone else's) and as a friendly term for a middle-aged man.",
         "context": "Pragmatic caution: using おじさん to address a man who isn't actually your uncle can sound like you're calling him 'old' — children often use it freely; adults usually avoid it for strangers."},
    ],
    "おばさん": [
        {"function": "Aunt / middle-aged woman / address",
         "gloss": "Used both for one's aunt (own or someone else's) and as a friendly term for a middle-aged woman.",
         "context": "Pragmatic caution: using おばさん to address an unrelated woman can sound rude — many Japanese women dislike being called おばさん because of the age implication. See おじさん for the same caveat."},
    ],
    "おくさん": [
        {"function": "Someone else's wife",
         "gloss": "Use おくさん (奥さん) to refer to SOMEONE ELSE'S wife or to address a married woman politely.",
         "context": "Don't use おくさん for your own wife when speaking to outsiders — say 妻 (つま) or 家内 (かない) instead. Using おくさん for one's own wife is a common learner mistake."},
    ],
    # ご主人 not currently in corpus — flagged for follow-up corpus expansion.
}


def apply_batch_d(entries, log):
    count = 0
    for form, notes in BATCH_D_PRAGMATIC.items():
        matches = _find(entries, form)
        if not matches:
            log.append(f"  D. SKIP: form {form!r} not found in corpus")
            continue
        for e in matches:
            existing = e.get("pragmatic_functions") or []
            # If already populated (from a prior native pass), don't clobber.
            if existing:
                log.append(f"  D. {e['id']}: pragmatic_functions already populated — left intact")
                continue
            e["pragmatic_functions"] = list(notes)
            e["pragmatic_functions_provenance"] = (
                "native_review_2026_06_04 (batch D: uchi/soto + address-form "
                "guidance per reviewer recommendation on family terms)"
            )
            log.append(f"  D. {e['id']}: added {len(notes)} pragmatic_functions entry")
            count += 1
    return count


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    v = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = v.get("entries", [])
    log: list[str] = []

    print(f"Loaded {len(entries)} vocab entries.")
    print()

    print("Batch A — sense de-contamination")
    n_a = apply_batch_a(entries, log)
    print(f"  entries touched: {n_a}")
    print()

    print("Batch B — homonym false_friends sweep")
    n_b = apply_batch_b(entries, log)
    print(f"  entries touched: {n_b}")
    print()

    print("Batch C — counter cleanup")
    n_c = apply_batch_c(entries, log)
    print(f"  entries touched: {n_c}")
    print()

    print("Batch D — family pragmatic notes")
    n_d = apply_batch_d(entries, log)
    print(f"  entries touched: {n_d}")
    print()

    print("=" * 60)
    print(f"Total entries touched: {n_a + n_b + n_c + n_d}")
    if args.dry_run:
        print("(DRY RUN — no file written)")
    else:
        # Bump _meta to record the review pass
        meta = v.get("_meta") or {}
        meta["native_review_pass_2026_06_04"] = (
            "Batches A-D applied from the consolidated native-reviewer "
            "report dated 2026-06-04: A) かた sense de-contamination "
            f"({n_a} entry), B) homonym false_friends sweep "
            f"({n_b} entries), C) counter cleanup ({n_c} entries), "
            f"D) family pragmatic notes ({n_d} entries). Batch E "
            "(particle-example native re-audit, ~50-300 entries) "
            "deferred to a follow-up cycle and tracked in xlsx bug tracker."
        )
        v["_meta"] = meta
        VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
        print(f"Wrote {VOCAB}")
    print()
    print("Per-entry log (first 50):")
    for line in log[:50]:
        try:
            print(line)
        except UnicodeEncodeError:
            sys.stdout.buffer.write(line.encode("utf-8") + b"\n")
    if len(log) > 50:
        print(f"  ... (+ {len(log) - 50} more lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
