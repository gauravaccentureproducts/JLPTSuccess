"""Refresh-state script for the N5Improvement audit prompt.

Produces live counts for every scorecard row across all five content
surfaces (Grammar / Vocab / Kanji / Reading / Listening), plus the
interconnection-density numbers and competitor-parity flags.

Output goes to stdout. Audit consumer reads, populates Section 2-4
tables, and produces Sections 5-10 findings.

Read-only: opens JSON files, walks structures, computes counts.
No mutations.
"""
import json
import os
import re
import sys
import io
import glob
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def truthy(v):
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return bool(v)


def main():
    G = load("data/grammar.json")["patterns"]
    V = load("data/vocab.json")["entries"]
    K = load("data/kanji.json")["entries"]
    R = load("data/reading.json")["passages"]
    L = load("data/listening.json")["items"]

    print("=" * 70)
    print("CORPUS WIDTHS (live)")
    print("=" * 70)
    print(f"  Grammar patterns:   {len(G)}")
    print(f"  Vocabulary entries: {len(V)}")
    print(f"  Kanji glyphs:       {len(K)}")
    print(f"  Reading passages:   {len(R)}")
    print(f"  Listening items:    {len(L)}")

    # ---------------- GRAMMAR SCORECARD ----------------
    print("\n" + "=" * 70)
    print("GRAMMAR SCORECARD (178 patterns)")
    print("=" * 70)

    examples_ge_7 = sum(1 for p in G if len(p.get("examples") or []) >= 7)
    examples_ge_10 = sum(1 for p in G if len(p.get("examples") or []) >= 10)
    cm_ge_3 = sum(1 for p in G if len(p.get("common_mistakes") or []) >= 3)
    wrong_corrected_present = sum(1 for p in G if (p.get("wrong_corrected_pair") or []))
    contrasts_ge_1 = sum(1 for p in G if len(p.get("contrasts") or []) >= 1)
    register_present = sum(1 for p in G if truthy(p.get("register")))
    sources_ge_2 = sum(1 for p in G if len(p.get("sources") or []) >= 2)
    audio_per_example = sum(
        1 for p in G
        if (p.get("examples") or [])
        and all(e.get("audio") for e in (p.get("examples") or []))
    )
    # ISSUE-128 fix (2026-05-13): grammar example field is `pitch_marks`, not `pitch_accent`.
    pitch_marked = sum(
        1 for p in G
        if (p.get("examples") or [])
        and all(e.get("pitch_marks") for e in (p.get("examples") or []))
    )
    cultural_callout_present = sum(1 for p in G if truthy(p.get("cultural_callout")))
    authentic_refs_ge_2 = sum(1 for p in G if len(p.get("authentic_refs") or p.get("public_domain_refs") or []) >= 2)
    authentic_refs_ge_1 = sum(1 for p in G if len(p.get("authentic_refs") or p.get("public_domain_refs") or []) >= 1)
    politeness_ladder_present = sum(1 for p in G if (p.get("politeness_ladder") or []))
    pragmatic_multi_function = sum(1 for p in G if p.get("pragmatic_functions"))
    essay_present = sum(1 for p in G if (p.get("essay") or {}).get("intro"))

    n = len(G)
    print(f"  examples >= 7:                 {examples_ge_7}/{n} ({examples_ge_7*100//n}%)")
    print(f"  examples >= 10:                {examples_ge_10}/{n} ({examples_ge_10*100//n}%)")
    print(f"  common_mistakes >= 3:          {cm_ge_3}/{n} ({cm_ge_3*100//n}%)")
    print(f"  wrong_corrected_pair >= 1:     {wrong_corrected_present}/{n} ({wrong_corrected_present*100//n}%)")
    print(f"  contrasts >= 1:                {contrasts_ge_1}/{n} ({contrasts_ge_1*100//n}%)")
    print(f"  register tag present:          {register_present}/{n} ({register_present*100//n}%)")
    print(f"  sources >= 2:                  {sources_ge_2}/{n} ({sources_ge_2*100//n}%)")
    print(f"  audio per example (all):       {audio_per_example}/{n} ({audio_per_example*100//n}%)")
    print(f"  pitch on every example:        {pitch_marked}/{n} ({pitch_marked*100//n}%)")
    print(f"  cultural_callout present:      {cultural_callout_present}/{n} ({cultural_callout_present*100//n}%)")
    print(f"  authentic_refs/pd_refs >= 1:   {authentic_refs_ge_1}/{n} ({authentic_refs_ge_1*100//n}%)")
    print(f"  authentic_refs/pd_refs >= 2:   {authentic_refs_ge_2}/{n} ({authentic_refs_ge_2*100//n}%)")
    print(f"  politeness_ladder present:     {politeness_ladder_present}/{n} ({politeness_ladder_present*100//n}%)")
    print(f"  essay (Tofugu-bar) present:    {essay_present}/{n} ({essay_present*100//n}%)")

    # ---------------- VOCAB SCORECARD ----------------
    print("\n" + "=" * 70)
    print("VOCAB SCORECARD (1009 entries)")
    print("=" * 70)

    examples_ge_3 = sum(1 for v in V if len(v.get("examples") or []) >= 3)
    # ISSUE-128 fix (2026-05-13): vocab field is `pitch_accent`, not `pitch`.
    pitch_with_drop = sum(1 for v in V if isinstance(v.get("pitch_accent"), dict) and "drop" in v.get("pitch_accent", {}))
    collocations_ge_5 = sum(1 for v in V if len(v.get("collocations") or []) >= 5)
    collocations_ge_2 = sum(1 for v in V if len(v.get("collocations") or []) >= 2)
    transitivity_pair = sum(1 for v in V if v.get("transitivity_pair") or v.get("intrans_pair") or v.get("trans_pair"))
    verb_class = sum(1 for v in V if v.get("verb_class") or v.get("group"))
    counter_pairing = sum(1 for v in V if v.get("counter") or v.get("counters"))
    register_present_v = sum(1 for v in V if truthy(v.get("register")))
    register_origin = sum(1 for v in V if v.get("register_origin"))
    # ISSUE-128: fields are `onomatopoeia` (bool) and `mimetic_class` (string).
    onomatopoeia = sum(1 for v in V if v.get("onomatopoeia") is True or v.get("mimetic_class"))
    pragma_functions = sum(1 for v in V if v.get("pragmatic_functions"))
    devoiced_vowel = sum(1 for v in V if v.get("devoiced_vowel"))
    minimal_pair_pitch = sum(1 for v in V if v.get("pitch_minimal_pair"))
    minimal_pair_long = sum(1 for v in V if v.get("long_vowel_pair") or v.get("minimal_pair_long"))
    # ISSUE-128: field is `frequent_patterns`.
    word_to_pattern = sum(1 for v in V if v.get("frequent_patterns"))
    authentic_ref_v = sum(1 for v in V if v.get("authentic_ref") or v.get("authentic_refs"))

    n = len(V)
    print(f"  examples >= 3:                 {examples_ge_3}/{n} ({examples_ge_3*100//n}%)")
    print(f"  pitch with mora+drop:          {pitch_with_drop}/{n} ({pitch_with_drop*100//n}%)")
    print(f"  collocations >= 5:             {collocations_ge_5}/{n} ({collocations_ge_5*100//n}%)")
    print(f"  collocations >= 2:             {collocations_ge_2}/{n} ({collocations_ge_2*100//n}%)")
    print(f"  transitivity_pair (verbs):     {transitivity_pair}/{n} ({transitivity_pair*100//n}%)")
    print(f"  verb_class flag:               {verb_class}/{n} ({verb_class*100//n}%)")
    print(f"  counter pairing (nouns):       {counter_pairing}/{n} ({counter_pairing*100//n}%)")
    print(f"  register tag present:          {register_present_v}/{n} ({register_present_v*100//n}%)")
    print(f"  register_origin (wago/kango):  {register_origin}/{n} ({register_origin*100//n}%)")
    print(f"  onomatopoeia/mimetic flag:     {onomatopoeia}/{n} ({onomatopoeia*100//n}%)")
    print(f"  pragmatic_functions:           {pragma_functions}/{n} ({pragma_functions*100//n}%)")
    print(f"  devoiced_vowel marker:         {devoiced_vowel}/{n} ({devoiced_vowel*100//n}%)")
    print(f"  pitch minimal-pair link:       {minimal_pair_pitch}/{n} ({minimal_pair_pitch*100//n}%)")
    print(f"  long-vowel minimal-pair:       {minimal_pair_long}/{n} ({minimal_pair_long*100//n}%)")
    print(f"  word->pattern reverse map:     {word_to_pattern}/{n} ({word_to_pattern*100//n}%)")
    print(f"  authentic_ref present:         {authentic_ref_v}/{n} ({authentic_ref_v*100//n}%)")

    # ---------------- KANJI SCORECARD ----------------
    print("\n" + "=" * 70)
    print("KANJI SCORECARD (106 entries)")
    print("=" * 70)

    mnemonic_radical = sum(1 for k in K if k.get("mnemonic") or k.get("radical_story"))
    # ISSUE-128: kanji `mnemonic` is a dict with `visual`/`reading` sub-fields.
    mnemonic_visual = sum(1 for k in K if isinstance(k.get("mnemonic"), dict) and k["mnemonic"].get("visual"))
    mnemonic_reading = sum(1 for k in K if isinstance(k.get("mnemonic"), dict) and k["mnemonic"].get("reading"))
    radical_decomp = sum(1 for k in K if k.get("radical_decomposition"))
    stroke_svg = sum(1 for k in K if k.get("stroke_order_svg"))
    stroke_trap = sum(1 for k in K if k.get("stroke_order_trap"))
    lookalikes = sum(1 for k in K if k.get("lookalikes"))
    vocab_links_inbound = defaultdict(int)
    for v in V:
        form = v.get("form") or ""
        for ch in form:
            for ke in K:
                if ke.get("glyph") == ch:
                    vocab_links_inbound[ch] += 1
                    break
    kanji_with_ge_5_vocab = sum(1 for ke in K if vocab_links_inbound.get(ke["glyph"], 0) >= 5)
    audio_yomi = sum(1 for k in K if k.get("audio_yomi"))
    etymology = sum(1 for k in K if k.get("etymology"))
    real_signage = sum(1 for k in K if k.get("real_signage") or k.get("authentic_refs"))
    n5_compounds = sum(1 for k in K if k.get("n5_compounds"))
    on_kun_rule = sum(1 for k in K if k.get("reading_rule") or k.get("on_kun_pair_drill"))
    okurigana_cuts = sum(1 for k in K if k.get("okurigana_cuts"))
    pitch_minimal_pair_k = sum(1 for k in K if k.get("pitch_minimal_pair"))

    n = len(K)
    print(f"  mnemonic (radical_story):      {mnemonic_radical}/{n} ({mnemonic_radical*100//n}%)")
    print(f"  mnemonic_visual:               {mnemonic_visual}/{n} ({mnemonic_visual*100//n}%)")
    print(f"  mnemonic_reading:              {mnemonic_reading}/{n} ({mnemonic_reading*100//n}%)")
    print(f"  radical_decomposition:         {radical_decomp}/{n} ({radical_decomp*100//n}%)")
    print(f"  stroke_order_svg:              {stroke_svg}/{n} ({stroke_svg*100//n}%)")
    print(f"  stroke_order_trap:             {stroke_trap}/{n} ({stroke_trap*100//n}%)")
    print(f"  lookalikes:                    {lookalikes}/{n} ({lookalikes*100//n}%)")
    print(f"  inbound vocab links >= 5:      {kanji_with_ge_5_vocab}/{n} ({kanji_with_ge_5_vocab*100//n}%)")
    print(f"  audio_yomi (per-yomi audio):   {audio_yomi}/{n} ({audio_yomi*100//n}%)")
    print(f"  etymology:                     {etymology}/{n} ({etymology*100//n}%)")
    print(f"  real-world signage ref:        {real_signage}/{n} ({real_signage*100//n}%)")
    print(f"  n5_compounds:                  {n5_compounds}/{n} ({n5_compounds*100//n}%)")
    print(f"  on/kun rule note:              {on_kun_rule}/{n} ({on_kun_rule*100//n}%)")
    print(f"  okurigana_cuts:                {okurigana_cuts}/{n} ({okurigana_cuts*100//n}%)")
    print(f"  pitch_minimal_pair link:       {pitch_minimal_pair_k}/{n} ({pitch_minimal_pair_k*100//n}%)")

    # ---------------- READING SCORECARD ----------------
    print("\n" + "=" * 70)
    print(f"READING SCORECARD ({len(R)} passages)")
    print("=" * 70)
    n = len(R)
    grammar_footnote = sum(1 for r in R if r.get("grammar_footnotes") or r.get("sentence_footnotes"))
    vocab_preview = sum(1 for r in R if r.get("vocab_preview") or r.get("vocab_glossary"))
    native_audio = sum(1 for r in R if r.get("audio"))
    # ISSUE-128: per-paragraph summary tracked via `paragraph_summary_provenance`.
    paragraph_summary = sum(1 for r in R if r.get("paragraph_summary_provenance"))
    natural_translation = sum(1 for r in R if r.get("translation_natural") or r.get("translation_literal"))
    cultural_callout_r = sum(1 for r in R if r.get("cultural_callout") or r.get("cultural_note"))
    reflection_prompts = sum(1 for r in R if r.get("reflection_prompts"))
    topic_tag = sum(1 for r in R if r.get("topic") or r.get("topic_cluster"))

    print(f"  grammar_footnotes per sent:    {grammar_footnote}/{n} ({grammar_footnote*100//n}%)")
    print(f"  vocab_preview present:         {vocab_preview}/{n} ({vocab_preview*100//n}%)")
    print(f"  native audio rendered:         {native_audio}/{n} ({native_audio*100//n}%)")
    print(f"  paragraph_summary:             {paragraph_summary}/{n} ({paragraph_summary*100//n}%)")
    print(f"  literal/natural translation:   {natural_translation}/{n} ({natural_translation*100//n}%)")
    print(f"  cultural_callout:              {cultural_callout_r}/{n} ({cultural_callout_r*100//n}%)")
    print(f"  reflection_prompts:            {reflection_prompts}/{n} ({reflection_prompts*100//n}%)")
    print(f"  topic tag:                     {topic_tag}/{n} ({topic_tag*100//n}%)")

    # ---------------- LISTENING SCORECARD ----------------
    print("\n" + "=" * 70)
    print(f"LISTENING SCORECARD ({len(L)} items)")
    print("=" * 70)
    n = len(L)
    # ISSUE-128: listening field names corrected to live schema.
    timestamped = sum(1 for li in L if li.get("timestamped_transcript"))
    glossary_inline = sum(1 for li in L if li.get("vocab_glossary"))
    slow_variant = sum(1 for li in L if li.get("audio_slow") or li.get("audio_variants"))
    discourse_markers = sum(1 for li in L if li.get("discourse_markers_used"))
    aizuchi = sum(1 for li in L if li.get("aizuchi_tokens"))  # tokens = actual content, not just flag
    pitch_pair_listen = sum(1 for li in L if li.get("pitch_minimal_pair"))
    devoiced_vowel_listen = sum(1 for li in L if li.get("devoiced_vowel_marks"))
    sokuon_pair = sum(1 for li in L if li.get("sokuon_pair") or li.get("long_vowel_pair"))
    ambient_layer = sum(1 for li in L if li.get("ambient_context") or li.get("audio_render_meta"))
    # ISSUE-128: field is `inference_question_expansion`.
    inference_q = sum(1 for li in L if li.get("inference_question_expansion"))
    prompt_ja_pre = sum(1 for li in L if li.get("prompt_ja"))

    # ISSUE-128: parse audio_render_meta.voices_used list (the live schema).
    voices = set()
    for li in L:
        meta = li.get("audio_render_meta") or {}
        used = meta.get("voices_used") or []
        if isinstance(used, list):
            for v in used:
                voices.add(str(v))

    print(f"  timestamped transcript:        {timestamped}/{n} ({timestamped*100//n}%)")
    print(f"  vocab_glossary inline:         {glossary_inline}/{n} ({glossary_inline*100//n}%)")
    print(f"  slow-version variant:          {slow_variant}/{n} ({slow_variant*100//n}%)")
    print(f"  discourse_markers:             {discourse_markers}/{n} ({discourse_markers*100//n}%)")
    print(f"  aizuchi present:               {aizuchi}/{n} ({aizuchi*100//n}%)")
    print(f"  pitch minimal-pair listen:     {pitch_pair_listen}/{n} ({pitch_pair_listen*100//n}%)")
    print(f"  devoiced_vowel marks:          {devoiced_vowel_listen}/{n} ({devoiced_vowel_listen*100//n}%)")
    print(f"  sokuon/long-vowel pair:        {sokuon_pair}/{n} ({sokuon_pair*100//n}%)")
    print(f"  ambient_context/render_meta:   {ambient_layer}/{n} ({ambient_layer*100//n}%)")
    print(f"  inference question:            {inference_q}/{n} ({inference_q*100//n}%)")
    print(f"  prompt_ja pre-audio:           {prompt_ja_pre}/{n} ({prompt_ja_pre*100//n}%)")
    print(f"  Distinct voices across corpus: {len(voices)} ({sorted(voices)})")

    # ---------------- DENSITY ----------------
    print("\n" + "=" * 70)
    print("INTERCONNECTION DENSITY")
    print("=" * 70)

    # Density 1: pattern -> how many vocab link in via vocab_ids
    density1_counts = []
    for p in G:
        seen = set()
        for ex in (p.get("examples") or []):
            for vid in (ex.get("vocab_ids") or []):
                seen.add(vid)
        density1_counts.append(len(seen))
    d1_avg = sum(density1_counts) / max(1, len(density1_counts))
    d1_below_floor = sum(1 for c in density1_counts if c < 3)
    print(f"  Density-1 (pattern->vocab):    avg={d1_avg:.1f}, below floor (<3): {d1_below_floor}/{len(G)}")

    # Density 2: vocab -> how many grammar patterns reference it (via vocab_ids reverse)
    vocab_id_to_patterns = defaultdict(set)
    for p in G:
        for ex in (p.get("examples") or []):
            for vid in (ex.get("vocab_ids") or []):
                vocab_id_to_patterns[vid].add(p["id"])
    density2_counts = [len(vocab_id_to_patterns.get(v.get("id"), set())) for v in V]
    d2_avg = sum(density2_counts) / max(1, len(density2_counts))
    d2_below_floor = sum(1 for c in density2_counts if c < 1)
    print(f"  Density-2 (vocab->pattern):    avg={d2_avg:.1f}, below floor (<1): {d2_below_floor}/{len(V)}")

    # Density 3: kanji -> how many vocab use it
    density3_counts = []
    for ke in K:
        glyph = ke["glyph"]
        c = sum(1 for v in V if glyph in (v.get("form") or ""))
        density3_counts.append(c)
    d3_avg = sum(density3_counts) / max(1, len(density3_counts))
    d3_below_floor = sum(1 for c in density3_counts if c < 2)
    print(f"  Density-3 (kanji->vocab):      avg={d3_avg:.1f}, below floor (<2): {d3_below_floor}/{len(K)}")

    # Density 4: kanji -> how many reading passages contain it
    density4_counts = []
    for ke in K:
        glyph = ke["glyph"]
        c = sum(1 for r in R if glyph in (r.get("ja") or r.get("text") or ""))
        density4_counts.append(c)
    d4_avg = sum(density4_counts) / max(1, len(density4_counts))
    d4_below_floor = sum(1 for c in density4_counts if c < 1)
    print(f"  Density-4 (kanji->reading):    avg={d4_avg:.1f}, below floor (<1): {d4_below_floor}/{len(K)}")

    # Aggregate metric
    import math
    total_xrefs = sum(density1_counts) + sum(density2_counts) + sum(density3_counts) + sum(density4_counts)
    corpus_size = len(G) + len(V) + len(K) + len(R) + len(L)
    aggregate = total_xrefs / math.sqrt(corpus_size)
    print(f"\n  Aggregate (total_xrefs/sqrt(corpus_size)): {aggregate:.1f}")
    print(f"    (total_xrefs={total_xrefs}, corpus_size={corpus_size})")

    # ---------------- PROVENANCE ----------------
    print("\n" + "=" * 70)
    print("PROVENANCE TIER DISTRIBUTION")
    print("=" * 70)
    for name, items, key in [
        ("Grammar.explanation_en", G, "explanation_provenance"),
        ("Grammar.common_mistakes", G, "_common_mistakes_provenance"),
        ("Grammar.cultural_callout", G, "cultural_callout_provenance"),
        ("Vocab.gloss", V, "gloss_provenance"),
    ]:
        if key.startswith("_"):
            continue  # nested, skip for now
        c = Counter()
        for it in items:
            c[it.get(key) or "(none)"] += 1
        print(f"\n  {name}:")
        for k, v in c.most_common():
            print(f"    {k:35s} {v}")

    # ---------------- ANTI-ITEM SANITY ----------------
    print("\n" + "=" * 70)
    print("ANTI-ITEM SANITY (corpus widths still frozen)")
    print("=" * 70)
    expected = {"grammar": 178, "vocab": 1009, "kanji": 106, "reading": 54, "listening": 50}
    actual = {"grammar": len(G), "vocab": len(V), "kanji": len(K), "reading": len(R), "listening": len(L)}
    for k, exp in expected.items():
        flag = "OK" if actual[k] == exp else "DRIFT"
        print(f"  {k}: live={actual[k]}, expected={exp} [{flag}]")


if __name__ == "__main__":
    main()
