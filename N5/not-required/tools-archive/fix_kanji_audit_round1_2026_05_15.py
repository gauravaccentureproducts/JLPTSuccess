"""Kanji audit Round 1 fixes.

- K1: 58 sentence translations added (sentences with empty translation_en)
- K2: 5 within-entry duplicate sentences — replace [1] with a fresh
  sentence + translation
- K8: 2 stroke-count text mismatches in stroke_order_trap.why_it_matters
  (east 9→8, drink 13→12 — the stroke_count int field is correct)
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

KANJI = Path("data/kanji.json")

# Format: (glyph, idx) -> (new_ja, new_en)
# If new_ja is None, only translation_en is updated (K1 case).
# If new_ja is provided, both ja and translation_en are replaced
# (K2 dup-replacement case).

K1_TRANSLATIONS: dict[tuple[str, int], str] = {
    # numbers + counters
    ("五", 0): "Shiro is five years old.",
    ("五", 1): "Hours are from five to nine.",
    ("六", 0): "Father also comes at six.",
    ("八", 0): "But the train was late, so I arrived at school at 8:10.",
    ("八", 1): "Dates: August 1st to August 7th. Time: 10 a.m. to 8 p.m. All books are half-price.",
    ("九", 0): "Hours are from five to nine.",
    ("百", 0): "B: It was 1,500 yen.",
    ("百", 1): "This book is 1,500 yen.",
    ("千", 0): "That big book is 2,000 yen.",
    # time / dates
    ("月", 0): "It is now April.",
    ("月", 1): "Open hours: Monday to Friday, 9 a.m. to 5 p.m.",
    ("火", 0): "Woman: Tuesday and Thursday.",
    ("水", 0): "On Mondays, Wednesdays, and Fridays I work part-time at a cafe.",
    ("土", 0): "On Saturday I play soccer with friends.",
    ("土", 1): "On Saturday I'll go with my mother to see the cherry blossoms.",
    ("年", 0): "I have been studying Japanese for one year.",
    ("年", 1): "I want to go to Japan next year.",
    ("半", 0): "Dates: August 1st to August 7th. Time: 10 a.m. to 8 p.m. All books are half-price.",
    ("毎", 0): "I get up at 6 every day.",
    ("毎", 1): "Every morning I run in the park.",
    ("週", 0): "These days I go to piano class twice a week.",
    ("午", 0): "I go to school at 9 a.m.",
    ("午", 1): "Let's meet at 3 p.m.",
    # people / family / roles
    ("男", 0): "A man and a woman are talking.",
    ("男", 1): "The woman is phoning the man.",
    ("口", 0): "Go out the station exit and walk straight.",
    ("会", 0): "Dear Yamada-san — let's meet tomorrow at 1 in front of the station.",
    ("社", 0): "My father is a company employee.",
    ("員", 0): "The shop clerk is talking.",
    # direction / position
    ("下", 0): "Isn't it underneath?",
    ("左", 0): "There is a post office on the left.",
    ("右", 0): "Turn right at the first traffic light.",
    ("後", 0): "Why was the hike rescheduled to a later day?",
    ("後", 1): "What will this person do after graduating?",
    ("外", 0): "Today it is raining, so going outside ( ).",
    ("外", 1): "It's cold today, so I won't go outside.",
    ("東", 0): "I'm going back from Osaka to Tokyo the night after next.",
    ("北", 0): "Man: The north exit.",
    # nature
    ("川", 0): "I saw fish in the river.",
    ("気", 0): "The weather was very good.",
    ("電", 0): "But the train was late, so I arrived at school at 8:10.",
    ("車", 0): "But the train was late, so I arrived at school at 8:10.",
    ("道", 0): "But the road is crowded.",
    ("道", 1): "I don't know the way.",
    # commerce / school
    ("店", 0): "Mother: What will you buy at the shop?",
    ("店", 1): "I want to buy coffee at the shop.",
    ("立", 0): "That is why my father is always standing.",
    ("安", 0): "The coffee is delicious, and the price is also cheap.",
    ("古", 0): "Kyoto is an old town.",
    ("長", 0): "This road is long.",
    ("白", 0): "There is a big white dog at my house.",
    ("名", 0): "His name is Shiro.",
    ("番", 0): "It is the biggest book.",
    # pronoun (mock-test fragments)
    ("私", 0): "I am ( ) a student.",
    ("私", 1): "I have ( ) been to China.",
}

# K2: 5 within-entry duplicate sentences. Replace [1] with a fresh
# sentence using the same kanji + a translation.
K2_REPLACEMENTS: dict[tuple[str, int], tuple[str, str]] = {
    ("東", 1): ("東の 空に 月が 見えます。",
              "The moon is visible in the eastern sky."),
    ("山", 1): ("ふじ山は 日本で 一番 高い 山です。",
              "Mt. Fuji is the tallest mountain in Japan."),
    ("読", 1): ("まいばん ねる 前に しんぶんを 読みます。",
              "I read the newspaper every night before sleeping."),
    ("立", 1): ("バスの 中で 立って いる 人が います。",
              "There are people standing on the bus."),
    ("安", 1): ("この みせは やさいが 安くて 新しいです。",
              "This shop's vegetables are cheap and fresh."),
}

# K8: stroke-count text mismatches in stroke_order_trap.why_it_matters
# The stroke_count integer is correct; the text is what's wrong.
K8_TRAP_TEXT_FIXES: dict[str, tuple[str, str]] = {
    "東": ("9 strokes. The horizontal+vertical at top precedes the box.",
          "8 strokes. The horizontal+vertical at top precedes the box."),
    "飲": ("13 strokes. Left-radical-first; 食 used in many food/drink verbs.",
          "12 strokes. Left-radical-first; 食 used in many food/drink verbs."),
}


def main() -> None:
    d = json.loads(KANJI.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    entries = d["entries"]
    n_k1 = n_k2 = n_k8 = 0
    missing = []

    by_glyph = {e["glyph"]: e for e in entries}

    # K1: add translations
    for (glyph, idx), new_en in K1_TRANSLATIONS.items():
        e = by_glyph.get(glyph)
        if not e:
            missing.append((glyph, idx, "entry-missing"))
            continue
        sents = e.get("sentences", [])
        if idx >= len(sents):
            missing.append((glyph, idx, f"idx-out-of-range ({len(sents)})"))
            continue
        sents[idx]["translation_en"] = new_en
        n_k1 += 1

    # K2: replace duplicate-[1] with fresh sentence + translation
    for (glyph, idx), (new_ja, new_en) in K2_REPLACEMENTS.items():
        e = by_glyph.get(glyph)
        if not e or idx >= len(e.get("sentences", [])):
            missing.append((glyph, idx, "k2 entry/idx missing"))
            continue
        e["sentences"][idx]["ja"] = new_ja
        e["sentences"][idx]["translation_en"] = new_en
        n_k2 += 1

    # K8: fix stroke_order_trap.why_it_matters text
    for glyph, (old_text, new_text) in K8_TRAP_TEXT_FIXES.items():
        e = by_glyph.get(glyph)
        if not e:
            missing.append((glyph, None, "k8 entry-missing"))
            continue
        sot = e.get("stroke_order_trap")
        if not isinstance(sot, dict):
            missing.append((glyph, None, "k8 no stroke_order_trap"))
            continue
        current = sot.get("why_it_matters", "")
        if current != old_text:
            missing.append((glyph, None, f"k8 text mismatch: {current!r}"))
            continue
        sot["why_it_matters"] = new_text
        n_k8 += 1

    KANJI.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"K1 translations added:    {n_k1}/{len(K1_TRANSLATIONS)}")
    print(f"K2 dup-sentence replaced: {n_k2}/{len(K2_REPLACEMENTS)}")
    print(f"K8 trap-text fixed:       {n_k8}/{len(K8_TRAP_TEXT_FIXES)}")
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  {m}")


if __name__ == "__main__":
    main()
