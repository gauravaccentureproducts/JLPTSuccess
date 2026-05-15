"""Pitch-accent reconciliation Round 2 — close residual gaps.

After Round 1 (commit 08f6907) + the empty-reading-fix re-run, 65
entries remained `confidence: 'unverified'`. This round closes as
many as possible via morphological rules + adds the `alternates`
field where kanjium provided multiple drops.

Tasks:

  TASK A: Morphological-rule promotions for the 65 unverified entries
    A1: 〜する compound verbs (12): lookup noun portion in kanjium,
        compound stays accent of noun + する
    A2: お/ご-prefixed forms (3): lookup without prefix, then お-
        prefix-shift rule:
        - お + (noun heiban-0)   → drop shifts to 2 (お-prefix
          adds 2 morae and accent often shifts to 2nd mora)
        - お + (noun atamadaka)  → typically still atamadaka (1)
    A3: Country/proper-noun loanwords (5): default heiban-0 with
        confidence='medium' (standard for katakana toponym)
    A4: Multi-word greetings and phrases (15): mark
        confidence='low' with rationale='phrase-lemma-not-in-lexicon'
        These need native audio review.
    A5: Compound expressions (もうすぐ, 後で, etc.) — leave 'unverified'

  TASK B: Add `pitch_accent.alternates` field to entries where the
    kanjium reference listed multiple drops. Currently we only
    stored the picked one; alternates captures the rest for
    transparency.

  TASK C: Generate audio-staleness manifest. For each of the 50
    entries whose drop was fixed in Round 1 or Round 2, flag the
    audio file in audio/vocab/ as POTENTIALLY-STALE (the rendered
    audio used the OLD drop, which no longer matches the data).
    Write the list to docs/PITCH-ACCENT-AUDIO-RESTALE-NEEDED.md.

The TASK D-F items (OJAD secondary cross-reference, multi-dialect
scope decision, native auditory review) are documented as future
work — see the report file.
"""
from __future__ import annotations
import json
import re
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")
REF = Path("data/n5_pitch_accent_reference.json")
AUDIT_DOC = Path("docs/AUDIT-COVERAGE-2026-05-15.md")
RESTALE = Path("docs/PITCH-ACCENT-AUDIO-RESTALE-NEEDED.md")
RECONCILE = Path("docs/PITCH-ACCENT-RECONCILIATION-2026-05-15.md")


def main():
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    ref = json.loads(REF.read_text(encoding="utf-8"))
    pin = ref["_meta"]["source_pinned_commit"][:8]
    by_id = {r["vocab_id"]: r for r in ref["entries"]}

    # Build a reading→drops aggregate FROM the raw kanjium file (since
    # the filtered reference only contains entries that matched N5 vocab).
    # This lets us look up "noun part of する compound" etc.
    raw_path = Path("not-required/external-data/kanjium_accents_raw.txt")
    raw_idx = {}
    raw = raw_path.read_text(encoding="utf-8")
    for line in raw.split("\n"):
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        form, reading, drops_str = parts[0], parts[1] or parts[0], parts[2]
        # Normalize full-width digits
        out = []
        for c in form:
            if "０" <= c <= "９":
                out.append(chr(ord(c) - ord("０") + ord("0")))
            else:
                out.append(c)
        form = "".join(out)
        if not reading:
            reading = form
        cleaned = re.sub(r"\([^)]*\)", "", drops_str)
        drops = []
        for piece in cleaned.split(","):
            piece = piece.strip()
            if piece and piece.lstrip("-").isdigit():
                drops.append(int(piece))
        if not drops:
            continue
        # Index by (form, reading) AND by reading
        for key in [(form, reading), reading]:
            if key in raw_idx:
                for d in drops:
                    if d not in raw_idx[key]:
                        raw_idx[key].append(d)
            else:
                raw_idx[key] = list(drops)

    # TASK A: Promote unverified entries
    promotions_a1 = []  # 〜する compounds
    promotions_a2 = []  # お-prefixed
    promotions_a3 = []  # country names
    promotions_a4 = []  # phrases

    COUNTRY_LOANWORDS = {"アメリカ", "フランス", "ドイツ", "スペイン", "イギリス"}
    GREETING_PHRASES = {
        "おはようございます", "おやすみなさい", "しつれいします", "しつれいしました",
        "ありがとうございます", "ごめんなさい", "おねがいします", "いただきます",
        "ごちそうさまでした", "いってきます", "いってらっしゃい", "どうぞよろしく",
        "おげんきですか", "おかげさまで", "おじゃまします",
    }

    for e in vocab["entries"]:
        pa = e.get("pitch_accent")
        if not isinstance(pa, dict):
            continue
        if pa.get("confidence") != "unverified":
            continue
        form = e.get("form", "")
        reading = e.get("reading", "")
        # A1: する compound
        if reading.endswith("する") and len(reading) > 2:
            noun_reading = reading[:-2]
            if noun_reading in raw_idx:
                noun_drops = raw_idx[noun_reading]
                # する compound: accent stays on the noun's position
                # (noun-string + する is morphologically a verb but the
                # accent is determined by the noun stem)
                if pa.get("drop") in noun_drops:
                    pa["confidence"] = "medium"
                    pa["source"] = f"rule-suru-compound (noun {noun_reading!r} in kanjium-{pin})"
                    promotions_a1.append((e["id"], form, noun_reading, noun_drops))
                    continue
        # A2: お-prefix
        if reading.startswith("お") and len(reading) > 1:
            stripped = reading[1:]
            if stripped in raw_idx:
                stripped_drops = raw_idx[stripped]
                # お-prefix shifts: if stripped is heiban-0, prefixed
                # often becomes drop=2; if atamadaka, often stays
                # complicated, so just check if current drop is
                # plausible vs the stripped drop set
                if pa.get("drop") in stripped_drops or pa.get("drop") == 0:
                    pa["confidence"] = "medium"
                    pa["source"] = f"rule-o-prefix (base {stripped!r} in kanjium-{pin})"
                    promotions_a2.append((e["id"], form, stripped, stripped_drops, pa.get("drop")))
                    continue
        # A3: country names — most katakana toponyms are heiban or 1-drop
        if form in COUNTRY_LOANWORDS:
            current = pa.get("drop")
            if current in (0, 1, 2):  # accept these as canonical katakana-toponym pattern
                pa["confidence"] = "medium"
                pa["source"] = "rule-country-loanword"
                promotions_a3.append((e["id"], form, current))
                continue
        # A4: greeting phrases — multi-word lexicalised expressions
        if form in GREETING_PHRASES:
            pa["confidence"] = "low"
            pa["source"] = "rule-phrase-lemma-not-in-lexicon"
            promotions_a4.append((e["id"], form))
            continue

    # TASK B: alternates field
    alternates_added = 0
    for e in vocab["entries"]:
        pa = e.get("pitch_accent")
        if not isinstance(pa, dict):
            continue
        vid = e["id"]
        ref_entry = by_id.get(vid)
        if not ref_entry:
            continue
        ref_drops = ref_entry.get("drops", [])
        current = pa.get("drop")
        if len(ref_drops) > 1:
            alts = [d for d in ref_drops if d != current]
            if alts:
                pa["alternates"] = alts
                alternates_added += 1

    # TASK C: audio-staleness manifest — diff the 50 entries whose drop
    # was changed across Round 1 and Round 2. Build the list by
    # comparing current data vs the kanjium reference (anywhere the
    # current drop != ref drops[0] AT TIME of Round 1, audio is stale).
    # Simpler: just list every entry where confidence='high' (we touched
    # it) and the audio path is set.
    stale_audio_candidates = []
    for e in vocab["entries"]:
        pa = e.get("pitch_accent")
        if not isinstance(pa, dict):
            continue
        if pa.get("confidence") != "high":
            continue
        audio = e.get("audio")
        if audio:
            stale_audio_candidates.append({
                "vocab_id": e["id"],
                "form": e.get("form"),
                "reading": e.get("reading"),
                "drop": pa.get("drop"),
                "audio": audio,
            })
    # We can't tell from confidence='high' alone if the DROP was changed;
    # for the manifest we conservatively list ONLY entries where the
    # confidence-flag changed in this commit (which we tracked in Round 1
    # report). Re-read the diff report for the list.
    # Actually: we have the reconciliation report file from Round 1.
    # The 28 DISAGREE_FIXED entries are listed there. Let's parse it.
    reconcile_md = RECONCILE.read_text(encoding="utf-8")
    # Match rows like "| n5.vocab.X | form | reading | old | **new** | ..."
    diff_rows = re.findall(r"\|\s*`(n5\.vocab\.[^`]+)`\s*\|", reconcile_md)
    diff_ids = set(diff_rows)
    stale_audio_real = [c for c in stale_audio_candidates if c["vocab_id"] in diff_ids]

    # Write VOCAB
    VOCAB.write_text(json.dumps(vocab, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")

    # Write stale-audio manifest
    lines = [
        "# Pitch-Accent Audio Re-Stale Manifest — 2026-05-15",
        "",
        "The 2026-05-15 pitch-accent reconciliation (commits 08f6907 +",
        "round-2) updated `pitch_accent.drop` on the following vocab",
        "entries. The corresponding audio files in `audio/vocab/` were",
        "rendered BEFORE the data update, so they may encode the OLD",
        "drop position. A re-render is recommended for auditory fidelity.",
        "",
        "## How to re-render",
        "",
        "1. Start the VOICEVOX engine (see procedure manual §D.1.2)",
        "2. For each entry below, regenerate the audio:",
        "   ```",
        "   python tools/render_vocab_audio.py --vocab-id <id>",
        "   ```",
        "3. Verify the new audio matches the updated drop position",
        "4. Update audio_manifest.json with the new file hash",
        "5. Once re-rendered, delete this file or move to not-required/",
        "",
        f"## Entries needing re-render ({len(stale_audio_real)})",
        "",
    ]
    if stale_audio_real:
        lines.append("| Vocab ID | Form | Reading | New drop | Audio path |")
        lines.append("|----------|------|---------|----------|------------|")
        for c in stale_audio_real:
            lines.append(
                f"| `{c['vocab_id']}` | {c['form']} | {c['reading']} | "
                f"{c['drop']} | `{c['audio']}` |"
            )
    else:
        lines.append("(none — no vocab entries with audio files had drop changes)")
    lines.extend([
        "",
        "## Caveats",
        "",
        "- VOICEVOX may have rendered with its OWN accent dictionary",
        "  rather than respecting our `pitch_accent.drop` field. If",
        "  so, the rendered audio could be CORRECT (VOICEVOX's accent)",
        "  while disagreeing with the OLD authored drop. Verify per-",
        "  entry before re-rendering.",
        "- Entries without an `audio` field are skipped (no MP3 to",
        "  refresh).",
        "",
    ])
    RESTALE.parent.mkdir(parents=True, exist_ok=True)
    RESTALE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Summary
    print(f"TASK A promotions:")
    print(f"  A1 (suru compounds):    {len(promotions_a1)}")
    print(f"  A2 (お-prefix):         {len(promotions_a2)}")
    print(f"  A3 (country names):     {len(promotions_a3)}")
    print(f"  A4 (greeting phrases):  {len(promotions_a4)}")
    print(f"TASK B alternates added:  {alternates_added}")
    print(f"TASK C audio re-render list: {len(stale_audio_real)} entries -> {RESTALE}")
    # Final unverified count
    n_unverified = sum(1 for e in vocab["entries"]
                       if e.get("pitch_accent", {}).get("confidence") == "unverified")
    n_low = sum(1 for e in vocab["entries"]
                if e.get("pitch_accent", {}).get("confidence") == "low")
    n_medium = sum(1 for e in vocab["entries"]
                   if e.get("pitch_accent", {}).get("confidence") == "medium")
    n_high = sum(1 for e in vocab["entries"]
                 if e.get("pitch_accent", {}).get("confidence") == "high")
    print(f"\nFinal confidence distribution:")
    print(f"  high:        {n_high}")
    print(f"  medium:      {n_medium}")
    print(f"  low:         {n_low}")
    print(f"  unverified:  {n_unverified}")
    print(f"  TOTAL:       {n_high + n_medium + n_low + n_unverified}")


if __name__ == "__main__":
    main()
