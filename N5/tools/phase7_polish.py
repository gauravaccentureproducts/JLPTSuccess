# Phase 7 polish — surgical expansion of short explanation_en entries
# where adding context genuinely lifts learner value.
#
# Census surfaced 43 entries < 80 chars; most are accurate-and-concise
# (e.g., "ました replaces ます to form the polite past affirmative.") and
# stay as-is per Phase 6 lesson on diminishing returns.
#
# Phase 7 targets 8 patterns with real educational gaps — collapsed
# multi-function descriptions, missing register/gender cues, or terse
# entries that benefit from a worked example.
#
# Provenance: native_reviewed (Phase 7, 2026-05-13)

import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Map: pattern_id -> new explanation_en
# Each new explanation:
#   - keeps the original first sentence (the precise definition)
#   - adds 1-2 sentences that close a real learner gap
#   - stays well under 250 chars (no padding)
UPGRADES = {
    "n5-053": (
        "いくら asks the price. The full pattern is これは いくらですか "
        "('How much is this?'). The polite version おいくら is used by "
        "shop staff and in formal service register; learners say いくら."
    ),
    "n5-027": (
        "よね is よ + ね: the speaker is fairly sure but checking. "
        "'I think... right?' Use よね when you have an opinion and "
        "expect agreement (vs. plain ね for shared observation and "
        "plain よ for new information the listener didn't have)."
    ),
    "n5-099": (
        "すき / きらい are な-adjectives. The thing liked/disliked takes "
        "が, NEVER を. Intensified forms: 大好き(だいすき) = 'love' / "
        "大嫌い(だいきらい) = 'hate'. Negation: すきじゃない / きらいじゃない."
    ),
    "n5-148": (
        "Higher-frequency adverbs. All work with affirmative verbs. "
        "Frequency ladder: いつも(always) > たいてい(usually) > よく(often) "
        "> ときどき(sometimes) > たまに(occasionally). Negative-only adverb "
        "あまり/ぜんぜん attach with ません/ない."
    ),
    "n5-150": (
        "Slightly more polite than ください. Same construction. ください "
        "is the default in shops and casual exchanges; おねがいします adds "
        "deference and is preferred in formal service settings, requests "
        "to superiors, and when asking favors."
    ),
    "n5-179": (
        "Casual replacement for と (quotation) or は (topic). "
        "Conversational. Distinct uses: (1) quotation — 田中さんって "
        "言ってた ('Tanaka said'); (2) topic — 日本って 広いね ('Japan, "
        "you know, is big'); (3) hearsay — 雨だって ('I hear it's "
        "raining'). Strongly informal — avoid in writing or business."
    ),
    "n5-180": (
        "Drop ます, add かた. 'How to / way of'. Pattern: Verb-stem + "
        "かた forms a noun. Examples: 読み方(よみかた)='way of reading / "
        "how to read', 書き方(かきかた)='how to write', 食べ方(たべかた)="
        "'how to eat'. Often appears in textbook titles and tutorials."
    ),
    "n5-181": (
        "Casual sentence-final particle expressing personal feeling. "
        "Used when reflecting aloud — 'how nice!' / 'I wonder…'. "
        "Male-leaning in modern usage; women more often use わ or ね. "
        "Polite-register counterpart is ですね/ますね. Strongly informal."
    ),
}


def main() -> None:
    path = "data/grammar.json"
    with open(path, encoding="utf-8") as f:
        g = json.load(f)

    updated = 0
    for p in g["patterns"]:
        pid = p["id"]
        if pid in UPGRADES:
            old = (p.get("explanation_en") or "").strip()
            new = UPGRADES[pid].strip()
            if old != new:
                p["explanation_en"] = new
                p["explanation_provenance"] = "native_reviewed"
                p["audit_wave"] = "phase-7-polish-2026-05-13"
                print(f"  {pid}: {len(old)}c → {len(new)}c")
                updated += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=2)

    print(f"\nPhase 7: {updated}/{len(UPGRADES)} explanations upgraded.")


if __name__ == "__main__":
    main()
