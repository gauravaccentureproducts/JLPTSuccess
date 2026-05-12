"""
ISSUE-112 quality follow-up phase 1 — Upgrade generic-fallback template
mistakes on the 16 patterns whose categories weren't in the original
family-template dict.

Categories addressed:
  - Te-form and Related Patterns        (9 patterns: n5-069..077)
  - Desiderative and Volitional         (3 patterns: n5-104, 105, 107)
  - Giving and Receiving (basic)        (3 patterns: n5-130, 131, 132)
  - Asking/Stating with から/ので (cause) (1 pattern:  n5-134)

For each of the 16 patterns, REPLACES the auto_generated_template
entries with family-specific pedagogical content covering all 4
error categories {particle, verb_class, conjugation, register}.
Pre-existing heuristic_categorized entries (the original common_mistakes
content) are PRESERVED.

Provenance after upgrade: 'llm_curated' (upgraded from
'auto_generated_template').
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
GRAMMAR = REPO / "data" / "grammar.json"


# Family-specific upgraded templates keyed by category-name substring.
UPGRADED_TEMPLATES = {
    "Te-form and Related Patterns": [
        ("conjugation",
         "食む + て = 食みて",
         "食む → 食んで (Group 1 む-ending uses ん + で)",
         "Te-form derivation by ending (Group 1 / godan): く→いて (書く→書いて), ぐ→いで (泳ぐ→泳いで), す→して (話す→話して), つ・る・う→って (待つ→待って, 帰る→帰って, 買う→買って), ぶ・む・ぬ→んで (遊ぶ→遊んで, 飲む→飲んで, 死ぬ→死んで). Memorize all 5 sub-rules — they're the #1 te-form mistake source."),
        ("verb_class",
         "食べる + て → 食べって (treating Group 2 as Group 1)",
         "食べる + て → 食べて (drop る, add て)",
         "Group 2 (ichidan / る-verbs) te-form: drop る, add て. Group 3 (irregular): する → して, くる → きて. Don't apply Group 1 sub-rules to Group 2 / 3 verbs."),
        ("particle",
         "食べての本",
         "食べる本 OR 食べてから本を読む",
         "Te-form on its own doesn't take a particle. To connect two clauses, use te-form + next verb directly (食べて、行く = eat and go). For sequence emphasis use てから (食べてから = after eating)."),
        ("register",
         "casual てる instead of polite ています",
         "polite ています / casual てる — match register throughout",
         "ています is the polite progressive (今、食べています = I'm eating now). The casual contraction is てる (今、食べてる). Don't mix polite and casual in the same sentence."),
    ],
    "Desiderative and Volitional": [
        ("particle",
         "水を飲みたい (using を with 〜たい)",
         "水が飲みたい (using が with 〜たい in standard speech)",
         "〜たい marks the desired object with が in standard speech: 水が飲みたい (I want to drink water). Modern colloquial allows を, but が is the textbook-correct form. Native teachers will mark を wrong on exams."),
        ("verb_class",
         "Trying to attach 〜たい to dictionary form: 飲むたい",
         "Attaching 〜たい to verb-stem: 飲みたい",
         "〜たい attaches to the verb STEM (the ます-form minus ます). Drop ます from 飲みます → 飲み, then append たい → 飲みたい. Don't attach to dictionary form."),
        ("conjugation",
         "飲みたいでした (incorrect past)",
         "飲みたかったです (correct past)",
         "〜たい conjugates like an い-adjective: present 〜たい, past 〜たかった, negative 〜たくない, past negative 〜たくなかった. Add です for polite form; do NOT use でした."),
        ("register",
         "Speaker's desire 〜たい about another person: 田中さんが飲みたい",
         "Use 〜たがる about another person: 田中さんが飲みたがっている",
         "〜たい is reserved for the SPEAKER'S OWN desire (or asking the listener). For third-person desire, switch to 〜たがる (田中さんは水を飲みたがる = Tanaka-san wants to drink water). The distinction is mandatory in formal writing."),
    ],
    "Giving and Receiving (basic)": [
        ("particle",
         "友達をプレゼントをあげる (double を)",
         "友達にプレゼントをあげる (に for recipient, を for object)",
         "Giving verbs (あげる / さしあげる / やる) take に for the RECIPIENT and を for the OBJECT given. Receiving verbs (もらう / いただく) take から or に for the GIVER and を for the object."),
        ("verb_class",
         "Treating くれる / もらう / あげる as Group 1",
         "All three are Group 2 (ichidan, る-verbs)",
         "あげる, もらう, くれる are all Group 2. Past tense: あげた, もらった, くれた. Polite: あげます, もらいます, くれます. Don't apply Group 1 sub-rules (which would yield wrong forms like あげって)."),
        ("conjugation",
         "Using くれた when giving to an outgroup person",
         "Use あげた when giving outward; くれた is for inward direction (ingroup)",
         "Directional rule: あげる = I/we give to someone (outward); もらう = I/we receive from someone (inward); くれる = someone gives to me/us (inward). Mixing the direction is the #1 give/receive mistake."),
        ("register",
         "あげる to a superior (rude)",
         "さしあげる to a superior (humble)",
         "あげる is for ingroup peers; for SUPERIORS / customers, use 差し上げる (さしあげる) as the humble form. Conversely, やる is for inferiors / pets / plants — using it with peers is rude/childish."),
    ],
    "Asking and Stating with から": [
        ("particle",
         "雨だ。だから行きません (using だから as conjunction)",
         "雨だから行きません (clause-final から; no comma break)",
         "から attaches to the END of clause A to mark it as a REASON for clause B. Don't start a new sentence with だから unless it's deliberately emphatic. Standard form: A から B (A reason → B result)."),
        ("conjugation",
         "明日雨ですからから行きません (double から)",
         "明日雨ですから行きません",
         "から attaches once at the clause boundary. Don't double the particle. Note that AFTER copula です/だ + から, the clause break is automatic."),
        ("verb_class",
         "Forgetting that な-adjective + ので requires な",
         "静かなので (correct な before ので) vs 静かので (incorrect)",
         "ので attaches to the PLAIN-FORM (連体形 / attributive form). For な-adjectives that means stem + な + ので (静かなので). For nouns + copula, use な (学生なので). Don't drop the な."),
        ("register",
         "から in a customer-facing complaint context",
         "ので / 〜まして for softer / more polite reasoning",
         "から is direct / blunt; sounds confrontational in customer-service contexts. Use ので (softer) or 〜まして (formal speech) when explaining a reason to a customer or boss. The pragmatic register matters as much as the grammatical form."),
    ],
}


def main() -> int:
    data = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    upgraded_patterns = 0
    upgraded_entries = 0

    for p in data["patterns"]:
        category = p.get("category") or ""
        # Find matching family
        family = None
        for fam_key, fam_templates in UPGRADED_TEMPLATES.items():
            if fam_key.lower() in category.lower():
                family = fam_templates
                break
        if not family:
            continue

        cms = p.get("common_mistakes") or []
        if not isinstance(cms, list):
            continue

        # Build pool by category: keep heuristic_categorized + native_reviewed,
        # replace auto_generated_template entries with the family-specific.
        keep = []
        replaced_categories = set()
        for cm in cms:
            if not isinstance(cm, dict):
                keep.append(cm)
                continue
            prov = cm.get("provenance")
            if prov != "auto_generated_template":
                keep.append(cm)
                replaced_categories.add(cm.get("category"))

        # Now add family-specific templates for missing categories
        added_for_this_pattern = 0
        pattern_label = p.get("pattern") or p["id"]
        for cat, wrong, right, why in family:
            if cat in replaced_categories:
                continue
            keep.append({
                "wrong":     wrong.format(pattern=pattern_label),
                "right":     right.format(pattern=pattern_label),
                "why":       why.format(pattern=pattern_label),
                "category":  cat,
                "provenance": "llm_curated",
                "audit_wave": "issue-112-quality-phase1-2026-05-12",
            })
            replaced_categories.add(cat)
            added_for_this_pattern += 1

        # Ensure at least 3 categorized
        cat_count = sum(1 for cm in keep if isinstance(cm, dict) and cm.get("category"))
        if cat_count < 3:
            # Pad with remaining family templates
            for cat, wrong, right, why in family:
                if cat_count >= 3:
                    break
                if cat in replaced_categories:
                    continue
                keep.append({
                    "wrong":     wrong.format(pattern=pattern_label),
                    "right":     right.format(pattern=pattern_label),
                    "why":       why.format(pattern=pattern_label),
                    "category":  cat,
                    "provenance": "llm_curated",
                    "audit_wave": "issue-112-quality-phase1-2026-05-12",
                })
                replaced_categories.add(cat)
                cat_count += 1

        p["common_mistakes"] = keep
        if added_for_this_pattern > 0:
            upgraded_patterns += 1
            upgraded_entries += added_for_this_pattern

    GRAMMAR.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Upgraded {upgraded_entries} template entries across {upgraded_patterns} patterns")

    # Re-census categorization coverage
    at3 = sum(
        1 for p in data["patterns"]
        if sum(1 for cm in (p.get("common_mistakes") or [])
               if isinstance(cm, dict) and cm.get("category")) >= 3
    )
    print(f"Patterns at >=3 categorized: {at3}/{len(data['patterns'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
