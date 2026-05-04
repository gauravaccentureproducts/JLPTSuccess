"""Auto-link every example in data/grammar.json to the vocab entries it
demonstrates. Closes the homograph mismatch class flagged 2026-05-01
(かた "person" vocab page was showing 読みかた "way of doing" examples
because the renderer matched by substring with no disambiguation).

Architecture:
- Each example in grammar.json gains a `vocab_ids: [...]` array listing
  the canonical vocab.json IDs the example demonstrates.
- The renderer (js/learn.js renderVocabDetail) filters by `vocab_ids`
  instead of substring-matching the form. With explicit links, homograph
  pages can never show another homograph's examples.

Disambiguation strategy:
- For NON-homograph forms (1 vocab entry per form): straightforward link.
- For homograph forms (>=2 entries):
  (a) If glosses are equivalent (e.g., 魚 in both Animals and Food
      sections, both glossed "fish"), link to ALL — they're alternative
      thematic placements, not different senses.
  (b) If glosses are different, apply disambiguation rules from
      HOMOGRAPH_RULES below. These rules are deterministic regex/POS
      checks against the JA text.
  (c) When rules can't decide (truly ambiguous example), OVER-LINK
      to all candidate entries. Per user direction 2026-05-01: showing
      one example on two detail pages is mildly redundant but never
      pedagogically wrong, whereas under-linking would show no examples
      on either page.

Run:
    python tools/link_grammar_examples_to_vocab.py
Idempotent: re-running overwrites the vocab_ids field with the latest
auto-tagger output.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / "data" / "grammar.json"
VOCAB = ROOT / "data" / "vocab.json"

# Homograph disambiguation rules. Each rule is keyed by the surface form
# and returns a function: (vocab_entries, example_ja, example_form) ->
# list of vocab_ids to link.
#
# The function should return a SUBSET of the candidate entries' ids.
# Returning all candidates means "over-link" (safe fallback when the
# example genuinely demonstrates multiple senses or the rule is unsure).


def _ids(entries):
    return [e["id"] for e in entries]


def _filter(entries, predicate):
    """Keep entries where predicate(entry) is True. If empty, return all
    (over-link fallback)."""
    keep = [e for e in entries if predicate(e)]
    return keep if keep else entries


def _is_pos(entry, *pos_values):
    return entry.get("pos") in pos_values


def _gloss_matches(entry, *substrs):
    g = (entry.get("gloss") or "").lower()
    return any(s.lower() in g for s in substrs)


def rule_kata(entries, ja, form):
    """かた: 'person (polite)' (pronoun) vs 'way of doing' (noun).
    'Way' sense: preceded by Verb-stem form (the pattern is
    Verb-stem + 〜かた, e.g., 読みかた). Otherwise person sense."""
    # Match 〜みかた / 〜きかた / 〜しかた / 〜ちかた / etc. (Verb-stem ending in i + かた)
    way_signal = re.search(r"[いきしちにひみり]かた", ja) or re.search(r"[え-お]かた", ja)
    # Also match: 食べ方 etc. — but our data uses kana 〜かた
    if way_signal:
        return _ids(_filter(entries, lambda e: _gloss_matches(e, "way of doing")))
    # Person sense: preceded by demonstrative or possessive
    person_signal = re.search(r"(この|その|あの|どの|あなたの|わたしの)\s*かた", ja) or "方は" in ja or "方が" in ja
    if person_signal:
        return _ids(_filter(entries, lambda e: _gloss_matches(e, "person")))
    return _ids(entries)  # ambiguous → over-link


def rule_ha(entries, ja, form):
    """は: 'tooth' (noun) vs 'leaf' (noun) vs 'topic marker' (particle).
    Particle signal: typed as standalone は after a noun. Other senses:
    not common in N5 examples, fall back to particle if context unclear."""
    # If the は is followed by another noun + verb (typical sentence frame),
    # it's the particle. The standalone noun senses (tooth/leaf) are rare
    # in N5 examples.
    if re.search(r"は\s+\S", ja) or "は、" in ja or "は。" in ja:
        return _ids(_filter(entries, lambda e: _is_pos(e, "particle")))
    # Tooth/leaf require explicit context — over-link to noun senses
    return _ids(_filter(entries, lambda e: _is_pos(e, "noun")))


def rule_hito(entries, ja, form):
    """人: 'person' (pronoun) vs counter for people.
    Counter signal: preceded by a number — 一人, 二人, 三人, etc."""
    if re.search(r"[一二三四五六七八九十百0-9０-９]\s*人", ja):
        return _ids(_filter(entries, lambda e: _is_pos(e, "counter")))
    return _ids(_filter(entries, lambda e: _is_pos(e, "pronoun")))


def rule_iru(entries, ja, form):
    """いる: 'to exist (animate)' (verb-2 in §28, also verb-1 in §30) vs
    'to need' (verb-1 in §27, godan exception). All three are likely to
    co-occur in N5 examples; default to over-link unless 'need' context."""
    if "いります" in ja or "いりません" in ja or "いりました" in ja or "いる必要" in ja:
        return _ids(_filter(entries, lambda e: _gloss_matches(e, "need")))
    return _ids(_filter(entries, lambda e: _gloss_matches(e, "exist")))


def rule_oku(entries, ja, form):
    """おく: numeral '100 million' vs verb 'to place'. Numeral context:
    surrounded by digits or 万/千 etc. Verb context: ます/た/て suffix."""
    if re.search(r"おく(ます|た|て|ない|か|に|を|が|は)", ja):
        return _ids(_filter(entries, lambda e: _is_pos(e, "verb-1")))
    return _ids(_filter(entries, lambda e: _is_pos(e, "numeral")))


def rule_hon(entries, ja, form):
    """本: counter for long thin objects vs noun 'book'. Counter signal:
    preceded by a number."""
    if re.search(r"[一二三四五六七八九十0-9０-９]\s*本", ja):
        return _ids(_filter(entries, lambda e: _is_pos(e, "counter")))
    return _ids(_filter(entries, lambda e: _is_pos(e, "noun")))


def rule_hai(entries, ja, form):
    """はい: 'yes' (expression) vs counter for cups. Counter signal:
    preceded by a number."""
    if re.search(r"[一二三四五六七八九十0-9０-９]\s*はい", ja):
        return _ids(_filter(entries, lambda e: _is_pos(e, "counter")))
    return _ids(_filter(entries, lambda e: _is_pos(e, "expression")))


def rule_kai(entries, ja, form):
    """かい: floor vs times. Floor: 〜階. Times: 〜回. Surface form かい
    in kana is rarely disambiguated alone — over-link."""
    return _ids(entries)


def rule_kiru(entries, ja, form):
    """きる: 'to cut' (verb-1 godan exception) vs 'to wear (upper body)'
    (verb-2). Hard to disambiguate by form alone since both conjugate
    differently but examples may show base form. Use POS heuristics on
    surrounding context.
    'Cut': common collocations with 紙, ハサミ, etc.
    'Wear': シャツ, セーター, etc.
    Over-link if ambiguous."""
    if any(s in ja for s in ["シャツ", "セーター", "コート", "服"]):
        return _ids(_filter(entries, lambda e: _gloss_matches(e, "wear")))
    if any(s in ja for s in ["紙", "はさみ", "切って"]):
        return _ids(_filter(entries, lambda e: _gloss_matches(e, "cut")))
    return _ids(entries)


def rule_kara(entries, ja, form):
    """から: conjunction 'because' vs particle 'from'. Conjunction:
    after a clause-ending form (です/ます/た). Particle: after a noun
    or time."""
    # Conjunction: ですから, ましたから, etc.
    if re.search(r"(です|ます|でした|ました|だ|た|い)から", ja):
        return _ids(_filter(entries, lambda e: _is_pos(e, "conjunction")))
    return _ids(_filter(entries, lambda e: _is_pos(e, "particle")))


def rule_ga(entries, ja, form):
    """が: conjunction 'but' vs particle 'subject marker'. Conjunction:
    after a clause-ending form. Particle: after a noun."""
    if re.search(r"(です|ます|でした|ました|だ|た|い)が", ja):
        # Clause + が — could be conjunction or formal-soft particle. Default conj.
        return _ids(_filter(entries, lambda e: _is_pos(e, "conjunction")))
    return _ids(_filter(entries, lambda e: _is_pos(e, "particle")))


def rule_to(entries, ja, form):
    """と: noun 'door' vs particle 'and/with/quote'. The particle is
    by far the more common N5 use; over-link to particle unless context
    clearly invokes door (e.g., 戸 kanji)."""
    if "戸" in ja:
        return _ids(_filter(entries, lambda e: _is_pos(e, "noun")))
    return _ids(_filter(entries, lambda e: _is_pos(e, "particle")))


def rule_doumo(entries, ja, form):
    """どうも: adverb 'thanks/indeed' vs expression 'thanks'. These are
    effectively the same word with two thematic placements. Over-link."""
    return _ids(entries)


# Map: form → disambiguation function
HOMOGRAPH_RULES: dict = {
    "かた": rule_kata,
    "は":   rule_ha,
    "人":   rule_hito,
    "いる": rule_iru,
    "おく": rule_oku,
    "本":   rule_hon,
    "はい": rule_hai,
    "かい": rule_kai,
    "きる": rule_kiru,
    "から": rule_kara,
    "が":   rule_ga,
    "と":   rule_to,
    "どうも": rule_doumo,
    # Other homograph clusters fall through to default behaviour
    # (over-link all entries) since they're either same-meaning
    # duplicates or the disambiguation isn't worth a custom rule.
}


_BOUNDARY = set(" 　、。！？「」（）()\n\t" + "　")


def matches_in_example(form: str, ja: str, pos: str = "") -> bool:
    """POS-aware substring check.

    Long forms (≥3 chars) are matched directly — the substring is
    distinctive enough that false positives are unlikely.

    Short forms (1-2 chars) need word-boundary signals to avoid the
    で-in-です / は-in-はな / こ-in-この class of false matches:

    - **Particles** (`pos == "particle"`): boundary AFTER. Particles
      attach to the preceding word so the BEFORE side is typically a
      kana/kanji, but the AFTER side must be a word boundary
      (space/punctuation/end). E.g., は in 「がっこうは べんきょう」.

    - **All other POS**: standalone token, requires boundary on BOTH
      sides. Catches counter こ matching at start of この (before is
      string-start which is a boundary, but after is の — fails). Same
      for で-in-です (no boundary after で), は-in-はな (no boundary
      after は), etc.

    Conjugated verbs aren't handled — only the dictionary form matches
    literally. This is an accepted under-linking; a proper Japanese
    morphological analyser would be needed for full coverage.
    """
    if not form:
        return False
    if form not in ja:
        return False
    # 2+-char forms: substring match is sufficient. Compounds like
    # 読みかた (verb-stem + かた) attach without space, so requiring a
    # boundary would miss the legitimate compound match. False-positive
    # risk at 2 chars is low — vocab forms aren't typically substrings
    # of other vocab forms at this length.
    if len(form) >= 2:
        # Counter-specific boundary: a 2-char counter (かい / ほん /
        # はい) must be preceded by a numeral so that かい inside かい
        # ました (the verb 買う) doesn't false-match. Numeral context =
        # ASCII digit, full-width digit, or kanji numeral.
        if pos == "counter":
            _NUMERAL = set("0123456789０１２３４５６７８９"
                           "一二三四五六七八九十百千万")
            idx = 0
            flen = len(form)
            while True:
                i = ja.find(form, idx)
                if i < 0:
                    return False
                if i > 0 and ja[i-1] in _NUMERAL:
                    return True
                idx = i + 1
        # Short-standalone-word boundary: 2-char standalone words
        # (noun / expression / interjection / adjective / adverb) need
        # word-boundary checks on BOTH sides so that:
        #   - はい (yes) doesn't false-match inside すってはいけません
        #     (left boundary catch)
        #   - あし (foot) doesn't false-match inside あした / あさって
        #     (right boundary catch)
        #
        # _PARTICLE_END catches the typical "previous word ended on a
        # particle" left context. _RIGHT_OK extends _BOUNDARY with the
        # particles and copula/modifier starts that legitimately attach
        # to the END of a noun/adj (e.g., 「あしを」 — を attaches and
        # IS a valid right context).
        #
        # Best-effort: Japanese has no real word boundaries, but the
        # common false-positive pattern is "verb-stem or longer-noun
        # substring contains short-noun".
        if pos in ("noun", "expression", "interjection",
                   "na-adjective", "i-adjective", "adverb") and len(form) <= 2:
            _PARTICLE_END = set("はがをにでとも")
            _RIGHT_OK = _BOUNDARY | _PARTICLE_END | set("のなだへやかねよ")
            idx = 0
            flen = len(form)
            while True:
                i = ja.find(form, idx)
                if i < 0:
                    return False
                left_ok = (i == 0
                           or ja[i-1] in _BOUNDARY
                           or ja[i-1] in _PARTICLE_END)
                right_pos = i + flen
                right_ok = (right_pos >= len(ja)
                            or ja[right_pos] in _RIGHT_OK)
                if left_ok and right_ok:
                    return True
                idx = i + 1
        return True
    # 1-char forms: high false-positive risk (で in です, は in はな,
    # こ in この). Enforce per-POS boundary rules.
    flen = len(form)
    idx = 0
    while True:
        i = ja.find(form, idx)
        if i < 0:
            return False
        before_b = (i == 0) or (ja[i-1] in _BOUNDARY)
        after_b = (i+flen >= len(ja)) or (ja[i+flen] in _BOUNDARY)
        if pos == "particle":
            if after_b:
                return True
        else:
            if before_b and after_b:
                return True
        idx = i + 1


def _has_left_boundary(ja: str, candidate: str) -> bool:
    """True iff `candidate` appears in `ja` at a position whose
    preceding character is a word-boundary (start-of-string, space,
    or Japanese punctuation).

    Used by conjugation_matches to avoid false positives where one
    verb's conjugated form happens to be a substring of another verb's
    conjugated form. E.g., かります (かりる polite) is a substring of
    わかります (わかる polite). Without this check, わかります examples
    would link to BOTH わかる AND かりる. With it, the match for
    かります requires "boundary then か"; in わかります the か is
    preceded by わ (not a boundary), so the false link is rejected.
    """
    idx = 0
    while True:
        i = ja.find(candidate, idx)
        if i < 0:
            return False
        if i == 0 or ja[i-1] in _BOUNDARY:
            return True
        idx = i + 1


def conjugation_matches(dict_form: str, pos: str, ja: str) -> bool:
    """Check whether a verb's or i-adjective's dictionary form appears in
    the example as one of its common conjugated forms (ます / ました /
    ません / て / た / ない / なかった / よう, plus potential
    -える/-られる, plus i-adj -くて/-く/-くない/-かった).

    Best-effort heuristic: handles regular Group-1 (う-verb), Group-2
    (る-verb), the two common irregulars (する, 来る), the verb potential
    form (which itself conjugates as verb-2), and i-adjectives.

    The dict_form must already not appear literally in `ja`.
    Each candidate must occur at a left word-boundary to avoid the
    かります-substring-of-わかります class of false positives.
    """
    if not dict_form or len(dict_form) < 2:
        return False
    last = dict_form[-1]
    stem = dict_form[:-1]
    candidates: list[str] = []

    if pos == "verb-2":
        # Ichidan: drop る, add ます/ました/ません/て/た/ない/なかった
        if last == "る":
            for suf in ("ます", "ました", "ません", "ませんでした",
                        "て", "た", "ない", "なかった",
                        "ています", "ていません",
                        "たい", "たくない", "ましょう"):
                candidates.append(stem + suf)
            # Potential / passive: 食べる → 食べられる, conjugates as verb-2
            for suf in ("られる", "られます", "られました", "られません",
                        "られない", "られなかった"):
                candidates.append(stem + suf)
    elif pos == "verb-1":
        # Godan: stem mutation depending on the dictionary-form ending.
        # ます-form: change う-row to い-row
        u_to_i = {"う":"い","く":"き","ぐ":"ぎ","す":"し",
                  "つ":"ち","ぬ":"に","ぶ":"び","む":"み","る":"り"}
        i_stem = stem + u_to_i.get(last, "")
        if u_to_i.get(last):
            for suf in ("ます", "ました", "ません", "ませんでした",
                        "たい", "たくない", "ましょう"):
                candidates.append(i_stem + suf)
        # て / た forms have their own euphonic rules:
        te_form = {
            "う": stem + "って", "つ": stem + "って", "る": stem + "って",
            "ぶ": stem + "んで", "ぬ": stem + "んで", "む": stem + "んで",
            "く": stem + "いて", "ぐ": stem + "いで",
            "す": stem + "して",
        }.get(last)
        if te_form:
            candidates.extend([te_form, te_form[:-1] + "た",
                               te_form + "います", te_form + "いません"])
        # 行く is the famous exception: te=行って, ta=行った (already covered above)
        # ない-form: change う-row to あ-row
        u_to_a = {"う":"わ","く":"か","ぐ":"が","す":"さ",
                  "つ":"た","ぬ":"な","ぶ":"ば","む":"ま","る":"ら"}
        a_stem = stem + u_to_a.get(last, "")
        if u_to_a.get(last):
            for suf in ("ない", "なかった", "なくて", "なければ"):
                candidates.append(a_stem + suf)
        # Potential form: change う-row to え-row + る → behaves as verb-2.
        # 行く → 行ける → 行けます/行けません/行けない/行けて...
        u_to_e = {"う":"え","く":"け","ぐ":"げ","す":"せ",
                  "つ":"て","ぬ":"ね","ぶ":"べ","む":"め","る":"れ"}
        e_stem = stem + u_to_e.get(last, "")
        if u_to_e.get(last):
            # The potential dict form itself (e_stem + る), then the
            # full verb-2 conjugation set on that potential stem:
            potential_dict = e_stem + "る"
            candidates.append(potential_dict)
            for suf in ("ます", "ました", "ません", "ませんでした",
                        "て", "た", "ない", "なかった",
                        "ています", "ていません"):
                candidates.append(e_stem + suf)
    elif pos == "verb-3":
        # Irregular: する / 来る (くる) — handle by exact-form lookup
        if dict_form == "する":
            candidates.extend(["します","しました","しません","しませんでした",
                                "して","した","しない","しなかった","しよう","しましょう",
                                "できる","できます","できました","できません",
                                "できない","できなかった","できて"])
        elif dict_form in ("くる", "来る"):
            candidates.extend(["きます","きました","きません","きませんでした",
                                "きて","きた","こない","こなかった",
                                "来ます","来ました","来ません","来て","来た",
                                "来ない","来なかった",
                                "こられる","こられます","来られる","来られます"])
    elif pos == "i-adj":
        # i-adjective: drop い, add くて/く/くない/くなかった/かった/ければ
        if last == "い":
            for suf in ("くて", "く", "くない", "くなかった",
                        "かった", "ければ", "くありません"):
                candidates.append(stem + suf)

    return any(_has_left_boundary(ja, c) for c in candidates if c)


def disambiguate(form: str, candidates: list, example_ja: str) -> list:
    """Given a list of vocab entry candidates that share `form`, return
    the subset of ids that this example actually demonstrates."""
    if len(candidates) == 1:
        return [candidates[0]["id"]]
    rule = HOMOGRAPH_RULES.get(form)
    if rule:
        return rule(candidates, example_ja, form)
    # Default: over-link all candidates (safe fallback per user direction
    # 2026-05-01: over-link is preferred to under-link). Same-meaning
    # duplicates land here naturally.
    return [c["id"] for c in candidates]


def main() -> int:
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))

    # Build form → [entries] index
    by_form: dict[str, list] = defaultdict(list)
    for e in vocab["entries"]:
        f = e.get("form", "")
        if f:
            by_form[f].append(e)

    homograph_forms = {f for f, es in by_form.items() if len(es) >= 2}
    print(f"vocab forms: {len(by_form)}, homographs: {len(homograph_forms)}",
          file=sys.stderr)

    examples_total = 0
    examples_linked = 0
    examples_with_homograph = 0
    homograph_decisions: dict[str, int] = defaultdict(int)

    for p in grammar["patterns"]:
        for ex in p.get("examples", []):
            examples_total += 1
            ja = ex.get("ja", "")
            if not ja:
                ex["vocab_ids"] = []
                continue
            linked: list[str] = []
            seen_forms: set[str] = set()
            # Walk longer forms first so "じかん" matches before "かん" etc.
            for form in sorted(by_form.keys(), key=len, reverse=True):
                if form in seen_forms:
                    continue
                # POS-aware matching: only candidates whose own POS-rule
                # is satisfied count as matched. For homographs that
                # share form but differ in POS (e.g., 人 = pronoun + counter),
                # this also acts as a per-POS pre-filter before the
                # higher-level disambiguation rule.
                candidates = by_form[form]
                matched = [c for c in candidates
                           if matches_in_example(form, ja, c.get("pos", ""))]
                # Conjugation fallback for verbs and i-adjectives: try
                # common conjugated forms when the dictionary form doesn't
                # appear literally. Catches わかります / わかりません /
                # 行きました / 食べて / 行けません / いそがしくて / etc.
                # Only fires for POS verb-1/2/3 and i-adj where applicable.
                # Try both the kanji form AND the kana reading so that
                # 分かる ↔ わかります (kana-only example) is caught.
                if not matched and len(form) >= 2 and any(
                    c.get("pos","").startswith("verb")
                    or c.get("pos","") == "i-adj"
                    for c in candidates
                ):
                    def _conj_any(c):
                        pos = c.get("pos","")
                        if not (pos.startswith("verb") or pos == "i-adj"):
                            return False
                        if conjugation_matches(form, pos, ja):
                            return True
                        reading = c.get("reading","")
                        if reading and reading != form:
                            return conjugation_matches(reading, pos, ja)
                        return False
                    matched = [c for c in candidates if _conj_any(c)]
                if not matched:
                    continue
                seen_forms.add(form)
                ids = disambiguate(form, matched, ja)
                for vid in ids:
                    if vid not in linked:
                        linked.append(vid)
                if len(candidates) > 1:
                    examples_with_homograph += 1
                    homograph_decisions[form] += 1
            # Post-filter: kana-conjugation collisions between irregular
            # 来る (verb-3, ます-stem き) and きる (verb-2 "to wear",
            # ms-stem also き) — surface forms きました / きます /
            # きませんでした / きて / きた are ambiguous between the
            # two. When 来る is linked AND the example has no clothing
            # context (シャツ / セーター / 服 / きもの / ようふく),
            # drop きる verb-1/verb-2 from the link set. Same for the
            # verb-1 "to cut" きる: drop unless cutting context
            # (紙 / はさみ).
            kuru_id = "n5.vocab.29-verbs-irregular-and-v.来る"
            kiru_wear_id = "n5.vocab.28-verbs-group-2-verbs.きる"
            kiru_cut_id = "n5.vocab.27-verbs-group-1-verbs.きる"
            if kuru_id in linked:
                if kiru_wear_id in linked and not any(
                    s in ja for s in ("シャツ", "セーター", "コート",
                                       "服", "きもの", "ようふく",
                                       "ジャケット")):
                    linked = [v for v in linked if v != kiru_wear_id]
                if kiru_cut_id in linked and not any(
                    s in ja for s in ("紙", "はさみ", "ハサミ", "切")):
                    linked = [v for v in linked if v != kiru_cut_id]
            # 入る (はいる "to enter") collides with はい (yes /
            # counter for cupfuls) at kana-substring level. When 入る
            # is in the link set, drop はい unless the example has a
            # standalone はい greeting (== "はい、" at start).
            hairu_id = "n5.vocab.27-verbs-group-1-verbs.入る"
            hai_yes_id = "n5.vocab.39-function-filler-expre.はい"
            hai_counter_id = "n5.vocab.9-counters-common.はい"
            if hairu_id in linked:
                if hai_yes_id in linked and not ja.startswith("はい"):
                    linked = [v for v in linked if v != hai_yes_id]
                if hai_counter_id in linked:
                    linked = [v for v in linked if v != hai_counter_id]
            # Also: いけません (cannot go / must not) is the negative
            # potential of 行く and contains the substring いけ which
            # collides with いけ (pond / lake). Drop いけ noun when
            # 行く is linked AND no nature/water context.
            iku_id = "n5.vocab.27-verbs-group-1-verbs.行く"
            ike_lake_id = "n5.vocab.14-nature-and-weather.いけ"
            if iku_id in linked and ike_lake_id in linked:
                if not any(s in ja for s in ("水", "魚", "公園", "庭")):
                    linked = [v for v in linked if v != ike_lake_id]
            # Also: 行く's negative-potential いけません contains いけ
            # which can also surface even when 行く isn't directly
            # linked (e.g., the idiomatic "Verb-て + は + いけません"
            # = "must not Verb"). Catch the bare いけません idiom.
            if "いけません" in ja and ike_lake_id in linked:
                linked = [v for v in linked if v != ike_lake_id]
            ex["vocab_ids"] = linked
            if linked:
                examples_linked += 1

    GRAMMAR.write_text(
        json.dumps(grammar, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"examples: {examples_total}, linked: {examples_linked} "
          f"({100*examples_linked/max(1,examples_total):.0f}%)",
          file=sys.stderr)
    print(f"homograph decisions made: {examples_with_homograph}",
          file=sys.stderr)
    if homograph_decisions:
        print("top homograph forms by example count:", file=sys.stderr)
        for f, n in sorted(homograph_decisions.items(),
                           key=lambda kv: -kv[1])[:15]:
            rule = "custom rule" if f in HOMOGRAPH_RULES else "over-link"
            print(f"  {f}: {n}  ({rule})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
