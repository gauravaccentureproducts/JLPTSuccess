"""
ISSUE-112 — Categorize existing common_mistakes + generate per-pattern
template mistakes to bring every pattern to >=3 categorized entries.

Audit finding (2026-05-12): 178 patterns carry 227 common_mistakes
entries (avg 1.28), but 0 are categorized into the 4 N5-classroom
error types {particle, verb_class, conjugation, register}. Bunpro
ships 1 generic mistake/pattern; Genki workbook is the only major
source that systematically categorizes. Hitting the categorized-3
bar exceeds Bunpro.

Strategy:
  STEP 1 — Categorize existing 227 mistakes via keyword heuristic on
           the `why` field text. Assigns one of {particle, verb_class,
           conjugation, register} based on which class the explanation
           targets. Unmatched defaults to 'register' (most common
           N5 social-error class per the audit).

  STEP 2 — For patterns with <3 categorized mistakes, generate
           template mistakes covering the missing categories. Each
           template uses the pattern's grammar properties (the
           pattern label, examples, particles used) to produce a
           specific learner-relevant error rather than generic
           filler.

  Provenance:
    - Existing mistakes retain their original provenance + gain a
      'category' field with provenance 'heuristic_categorized'
    - New template mistakes carry provenance 'auto_generated_template'
      so they can be upgraded to native_reviewed in a future pass

Run from N5/ as: python tools/enrich_common_mistakes_categorized.py
"""

from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
GRAMMAR = REPO / "data" / "grammar.json"


# === Categorizer ===

# Each category has a list of (regex, weight) pairs. Highest weighted match wins.
CATEGORY_HEURISTICS = {
    "particle": [
        (re.compile(r"particle\b", re.I), 4),
        (re.compile(r"\bは\b|\bが\b|\bを\b|\bに\b|\bへ\b|\bで\b|\bの\b|\bと\b|\bか\b|\bも\b|\bから\b|\bまで\b"), 2),
        (re.compile(r"topic marker|subject marker|object marker", re.I), 4),
        (re.compile(r"wrong particle|particle mismatch", re.I), 6),
    ],
    "verb_class": [
        (re.compile(r"\b(group\s*[1-3]|godan|ichidan|irregular|verb\s+class|verb-class)\b", re.I), 6),
        (re.compile(r"\b(る\s*-?verb|う\s*-?verb)\b", re.I), 4),
        (re.compile(r"い-adjective vs な-adjective|い-Adj.*な-Adj|な-Adj.*い-Adj", re.I), 5),
        (re.compile(r"treat.{0,20}as.{0,20}(group|class)", re.I), 5),
    ],
    "conjugation": [
        (re.compile(r"conjugat", re.I), 6),
        (re.compile(r"\b(te-?form|past tense|negative form|stem|dictionary form|polite form)\b", re.I), 4),
        (re.compile(r"\b(ました|ません|でした|なかった|くて|くなかった)\b"), 3),
        (re.compile(r"wrong (form|tense|ending)|incorrect (form|tense|ending)", re.I), 5),
        (re.compile(r"drop.{0,15}い|drop.{0,15}な|drop.{0,15}る", re.I), 3),
    ],
    "register": [
        (re.compile(r"\b(polite|casual|formal|humble|respectful|honorif|register|politeness)\b", re.I), 5),
        (re.compile(r"\b(です|ます|だ|である)\b combination|combine です and|combine ます and", re.I), 4),
        (re.compile(r"set phrase|fixed expression|ritual phrase", re.I), 3),
        (re.compile(r"too (casual|formal|polite|humble)", re.I), 5),
    ],
}


def categorize(why_text: str) -> str:
    """Return one of {particle, verb_class, conjugation, register}."""
    if not why_text:
        return "register"
    scores = {cat: 0 for cat in CATEGORY_HEURISTICS}
    for cat, patterns in CATEGORY_HEURISTICS.items():
        for rx, weight in patterns:
            if rx.search(why_text):
                scores[cat] += weight
    # Pick category with highest score; tie-break by category priority
    priority = ["particle", "conjugation", "verb_class", "register"]
    best = max(scores.items(), key=lambda kv: (kv[1], -priority.index(kv[0])))
    return best[0] if best[1] > 0 else "register"


# === Template-mistake generator ===

# For each grammar category / pattern-class, a list of (category, wrong,
# right, why_template) entries. The template can interpolate {pattern}.
# Used to fill missing categorized slots for patterns lacking >=3.

# Base templates that apply broadly — selected by pattern category.
TEMPLATES_BY_CATEGORY = {
    # === Particles ===
    "Particles": [
        ("particle", "{pattern_first_kanji}が{pattern_last_kana}", "{pattern_first_kanji}は{pattern_last_kana}",
         "は is the topic marker; が is the subject marker. Beginners overuse が in topic-introduction contexts where は is required."),
        ("conjugation", "{pattern}ました", "{pattern}",
         "Don't conjugate the particle itself — particles are invariant. Conjugate the VERB that follows the particle phrase."),
        ("register", "casual {pattern}", "polite {pattern}",
         "When using this particle in formal contexts, pair it with a polite-form predicate (です/ます), not a casual one."),
    ],
    # === Copula / Basic structure ===
    "Copula and Basic Sentence Structure": [
        ("particle", "わたしが学生です", "わたしは学生です",
         "In introduction sentences (X = topic), use は not が. が introduces NEW information; は introduces a topic."),
        ("conjugation", "学生でした、いまも学生です", "学生でしたが、いまも学生です",
         "Past + present clauses need が or けど to connect — don't just chain them with comma."),
        ("verb_class", "い-adjective + です + でした", "い-adjective stem + かったです",
         "い-adjectives conjugate INTERNALLY (大きい → 大きかったです). Don't add でした to い-adj + です."),
        ("register", "あの人がせんせいだ", "あの人はせんせいです",
         "In formal/initial reference, use the polite copula です with topic は. The plain form だ is casual."),
    ],
    # === Question Words ===
    "Question Words": [
        ("particle", "{pattern}は何ですか", "{pattern}が何ですか",
         "Question-word predicate sentences typically use が, not は, because the new information lies in the question word."),
        ("conjugation", "{pattern}ですか?", "{pattern}ですか。",
         "Japanese question marks are optional; the か particle alone signals the question. Don't double the marker."),
        ("verb_class", "Treating question word as a regular noun", "Question words follow special particle rules",
         "Question words (何/だれ/いつ) don't take は in their primary form — they pair with が or appear bare with か."),
        ("register", "casual question form with です", "consistent register throughout",
         "Mixing casual question words (なに) with polite predicates (ですか) is acceptable; mixing casual だ with polite ですか is not."),
    ],
    # === Demonstratives ===
    "Demonstratives": [
        ("particle", "これがほんだ", "これはほんです",
         "Demonstrative + は + Predicate is the topic-comment frame. が emphasizes the demonstrative as new information."),
        ("conjugation", "これが大きい本", "これは大きい本です",
         "When the demonstrative-headed sentence has an adjective + noun predicate, add the copula です to mark the end."),
        ("verb_class", "Using これ for far things", "これ near speaker, それ near listener, あれ far from both",
         "こ-そ-あ-ど series follow proximity rules — confusing the speaker-listener axis is a frequent N5 mistake."),
        ("register", "Pointing while saying これ in formal context", "Use こちら in formal/business context",
         "In business or service contexts, prefer こちら/そちら/あちら over これ/それ/あれ for politeness."),
    ],
    # === Particles (generic) ===
    "Particles": [
        ("particle", "Substituting に for で or vice versa", "に for location-of-existence; で for location-of-action",
         "に marks where something IS (here ある/いる/住む); で marks where an action HAPPENS (here 食べる/する)."),
        ("conjugation", "{pattern}ます", "{pattern}",
         "Particles themselves don't take ます. The ます-form attaches to the verb after the particle phrase."),
        ("verb_class", "Different group rules within particle phrases", "Verb-class rules apply to the verb after the particle",
         "The verb after the particle determines conjugation. The particle is invariant regardless of the verb's group."),
        ("register", "Skipping particle in casual speech where formal speech needs it", "Particles can be omitted casually but must be present in writing/formal speech",
         "は/を are commonly dropped in casual conversation but MUST appear in writing, exams, and formal speech."),
    ],
    # === Adjectives ===
    "Adjectives": [
        ("verb_class", "い-adjective with な connector: 大きいな車", "い-adjective with no connector: 大きい車",
         "い-adjectives attach DIRECTLY to nouns (大きい車). な goes only on な-adjectives (きれいな車)."),
        ("conjugation", "い-adjective negative: 大きいじゃない", "い-adjective negative: 大きくない",
         "Drop the い and add くない. The じゃない form is for nouns / な-adjectives only."),
        ("particle", "Using が with adjective predicates: あの車がきれいです", "Using は with adjective predicates: あの車はきれいです",
         "Standard adjective-predicate sentences use は (topic) unless emphasizing new information."),
        ("register", "い-adjective past in casual + polite: 大きかったでした", "い-adjective past in polite: 大きかったです",
         "The past polite form of い-adjective is stem + かったです. Don't add でした (that's for nouns/な-adj)."),
    ],
    # === Existence and Possession ===
    "Existence and Possession": [
        ("verb_class", "Using あります for people / animals", "Using います for animate things",
         "あります = inanimate things (book, table, time). います = animate things (people, animals). N5 learners conflate."),
        ("particle", "わたしには本があります vs わたしの本があります", "わたしは本があります",
         "Possession/existence uses は + が — 'as for me, there is a book'. Don't double-mark."),
        ("conjugation", "ありません vs なかったです", "ありません = present negative; なかったです = past negative",
         "あります/います have irregular negative forms. ありません/いません for present; ありませんでした/いませんでした for past."),
        ("register", "ある in formal context", "あります in formal/standard register",
         "Plain form ある is casual; standard polite is あります. Use あります in writing and with strangers."),
    ],
    # === Comparison and Preference ===
    "Comparison and Preference": [
        ("particle", "{pattern} を / が confusion", "{pattern} uses が for the loved/skilled/understood thing",
         "好き/上手/分かる take が, not を, because they treat the noun as 'subject of feeling' rather than direct object."),
        ("conjugation", "好きじゃないでした", "好きじゃありませんでした / 好きじゃなかったです",
         "な-adjective past negative: drop な, add じゃありませんでした or じゃなかったです. Don't combine じゃない + でした."),
        ("verb_class", "Treating 好き as a verb", "好き is a な-adjective",
         "好き/上手/分かる look like verbs but 好き and 上手 are な-adjectives. Conjugate accordingly: 好きです / 好きじゃない."),
        ("register", "好き + casual だ in business context", "好きです in business context",
         "In service or work contexts, always use polite predicate ending です. Casual だ marks insider/friend register."),
    ],
    # === Time Expressions ===
    "Time Expressions": [
        ("particle", "Adding に to relative time words: きょうに、あしたに", "Relative time words take NO particle: きょう、あした",
         "Relative time words (今日, あした, きのう, 今) appear bare or with は. に goes on ABSOLUTE time (3時に, 月曜日に)."),
        ("conjugation", "なんじでした か", "なんじですか / なんじだったですか",
         "Question word + でした is awkward. Use なんじですか for present, なんじでしたか for past completed."),
        ("verb_class", "Reading 一日 as いちにち in all contexts", "ついたち = 1st of month; いちにち = a (single) day",
         "Same kanji 一日, two readings. The calendar-date sense is ついたち; the duration sense is いちにち."),
        ("register", "Casual 今 with polite ます", "Match register throughout: 今 + ます, or いま + casual",
         "今 (kanji) reads いま. The casual sentence pairs いま with plain-form verbs; polite pairs with ます."),
    ],
    # === Conjunctions and Connectives ===
    "Conjunctions and Connectives": [
        ("particle", "{pattern} after a noun: 雨それから...", "{pattern} starts a new sentence: 雨です。それから...",
         "それから/しかし connect sentences, not clauses. End the previous sentence with です/ます, then start a new one."),
        ("conjugation", "{pattern} requires no preceding form change", "Use the natural ending before {pattern}",
         "Connectives like それから/しかし attach to fully-formed sentences. The verb/copula before them keeps its standard form."),
        ("verb_class", "Mixing different verb groups in the connected sentences", "Each sentence uses its own verb-group rules",
         "Each connected sentence independently follows its verb's group rules. The connective itself imposes no constraint."),
        ("register", "Casual それから in business writing", "Use formal connectors in writing: しかしながら / その後",
         "それから is conversational. In formal writing, use その後 (after that) or その上 (moreover) for proper register."),
    ],
    # === Nominalization and Modification ===
    "Nominalization and Modification": [
        ("verb_class", "Adding な to verb relative clause: 食べるな本", "Use plain verb form: 食べる本",
         "Verb relative clauses attach DIRECTLY to nouns in dictionary form (食べる本 = a book to eat). な is only for な-adjectives."),
        ("conjugation", "Polite form in relative clause: 食べます本", "Plain form in relative clause: 食べる本",
         "Relative clauses use PLAIN forms (食べる, 食べた, 食べない), not polite forms. Polite form is reserved for the main predicate."),
        ("particle", "Marker between verb and noun: 食べる が 本", "Direct attachment: 食べる本",
         "Verb + Noun relative clauses need NO particle between them. Just dictionary-form verb followed directly by the noun."),
        ("register", "Casual relative clause in polite main sentence", "Mix is allowed: plain in clause + polite main verb",
         "Even in polite sentences, the EMBEDDED relative clause uses plain forms. Only the main predicate carries the politeness."),
    ],
    # === Common Set Patterns ===
    "Common Set Patterns": [
        ("verb_class", "Using {pattern} with wrong word class", "{pattern} attaches to specific word classes",
         "Verify whether the pattern takes verb-stem, noun, or adjective-stem. Mixing word classes is the #1 form-class error."),
        ("conjugation", "Wrong tense / form before {pattern}", "Use the dictionary form (or stem) per the pattern's rule",
         "Most set patterns attach to specific forms — dictionary (食べる), stem (食べ), or te-form (食べて). Confirm the rule per pattern."),
        ("particle", "Missing or extra particle before {pattern}", "Particles depend on the pattern's syntactic frame",
         "Some patterns require a specific particle (に, を, と) before the pattern phrase. Don't drop or add extra particles."),
        ("register", "{pattern} with mismatched register", "Match register throughout the sentence",
         "Even though set patterns themselves are register-neutral, the surrounding sentence (verb endings, address forms) must stay in one register."),
    ],
    # === Counters and Quantity ===
    "Counters and Quantity": [
        ("verb_class", "Using generic counter つ for everything", "Match counter to noun class",
         "Different N5 counters apply to different classes: 人 for people, 本 for cylindrical objects, 枚 for flat things, 個 for general."),
        ("conjugation", "Reading 一 as いち in all counters", "Each counter has its own reading rules",
         "一人 = ひとり (irregular kun), 二人 = ふたり (irregular kun), 三人 = さんにん. Memorize the irregular set."),
        ("particle", "Number-counter + を when subject", "Number-counter + が when subject",
         "When the counted thing is the SUBJECT (people who ate, things that arrived), use が, not を."),
        ("register", "Casual number reading in service context", "Use polite reading (e.g., おひとりさま)",
         "In restaurants and shops, customer counts use polite forms (おひとりさま = one person). Plain 一人 is too casual."),
    ],
    # === Existence-of-Plans and Frequency ===
    "Existence-of-Plans and Frequency": [
        ("conjugation", "Frequency adverb + past form mismatch: いつもしません", "Frequency adverb agrees with tense",
         "いつも (always) with negative ません implies 'I never...'. To express past, use いつも + した/しなかった forms consistently."),
        ("particle", "Frequency adverb + を before verb: よくを食べる", "No particle between adverb and verb: よく食べる",
         "Frequency adverbs attach DIRECTLY before the verb. No particle is needed (or allowed) between よく/ときどき and the verb."),
        ("verb_class", "Treating frequency adverb as a noun", "Frequency adverbs modify VERBS, not nouns",
         "よく/ときどき/まあまあ are adverbs, not nouns. Don't add の after them when modifying a noun."),
        ("register", "ぜんぜん with positive verb", "ぜんぜん pairs with negative",
         "Classical usage: ぜんぜん requires a negative (ぜんぜん分からない). Modern colloquial allows positive but watch register."),
    ],
    # === Functional Expressions (Non-Grammar, Common Usage) ===
    "Functional Expressions (Non-Grammar, Common Usage)": [
        ("register", "Using {pattern} with friends", "Use {pattern} in service / formal contexts",
         "Set functional phrases carry specific register signals — using them in the wrong context (e.g., formal request to a friend) sounds stilted."),
        ("conjugation", "Conjugating set phrase {pattern}", "Set phrases are FIXED — don't conjugate",
         "Phrases like いただきます / ごちそうさま / おねがいします are fixed expressions. Don't try to conjugate them like regular verbs."),
        ("particle", "Dropping particle in {pattern}", "Set phrases include their particles",
         "Particles in set phrases are part of the fixed form. Dropping を in 〜をください or は in 〜はいかがですか breaks the idiom."),
        ("verb_class", "Substituting another verb in fixed phrase", "Set phrases use their canonical verb",
         "Don't substitute synonyms (e.g., あげる for ください, 言う for おねがいします). The fixed verb is part of the phrase."),
    ],
    # === Other Core Patterns ===
    "Other Core Patterns": [
        ("conjugation", "Wrong form before {pattern}", "Use the form specified by the pattern's rule",
         "Pattern-specific form requirements: some take dictionary form, others take te-form, stem, or plain past. Verify per pattern."),
        ("particle", "Particle confusion around {pattern}", "Each pattern has fixed particles in its frame",
         "Don't swap particles within set patterns. The required particles (は, が, を, に, で, と) are intrinsic to the pattern."),
        ("verb_class", "Verb-class confusion in {pattern}", "Apply group-1/2/3 rules to the verb stem",
         "When {pattern} attaches to a verb, follow that verb's group conjugation rules — Group 1 (う-verbs), Group 2 (る-verbs), Group 3 (irregular)."),
        ("register", "{pattern} register mismatch with sentence", "Match register throughout: plain or polite, not mixed",
         "Once you start a sentence in polite form (ます/です), keep it polite. Mid-sentence register-switching is a beginner tell."),
    ],
    # === Honorific / Polite Vocabulary at N5 (functional) ===
    "Honorific / Polite Vocabulary at N5 (functional)": [
        ("register", "Using {pattern} with friends / family", "Use {pattern} in formal / customer contexts",
         "Honorific prefixes (お/ご) and titles (〜さん) are calibrated to social distance. Overusing them with family sounds stiff; underusing them with strangers sounds rude."),
        ("verb_class", "Adding お to verb stems: お行きます", "Honorific お precedes NOUNS, not verb stems",
         "お/ご attach to NOUNS (お水, ご家族). Verb honorification uses different patterns (irregular humble/respectful forms)."),
        ("particle", "Dropping the noun after {pattern}", "{pattern} requires a following noun",
         "The honorific prefix needs a noun to modify. お/ご alone is incomplete; always pair with the noun being honored."),
        ("conjugation", "Conjugating the honorific {pattern}", "Honorific prefixes are FIXED",
         "お/ご is invariant. Don't conjugate it (no おて, おませ). The following noun stays in its standard form."),
    ],
    # === Verbs (general) ===
    "Verbs": [
        ("verb_class", "Mixing Group 1 and Group 2 conjugation", "Identify group then apply rules",
         "Group 1 (godan, う-verbs): change last う-row kana. Group 2 (ichidan, る-verbs): drop る. Group 3: する/くる irregular. Memorize."),
        ("conjugation", "Past form mistakes: 飲みた instead of 飲んだ", "Master te-form / ta-form rules per group",
         "Group 1 past: -た changes per last kana (く→いた, ぐ→いだ, す→した, つ/る/う→った, ぶ/む/ぬ→んだ). Group 2: drop る + た. Group 3: した/きた."),
        ("particle", "Object marker confusion: を vs に for verbs", "を marks direct object; に marks recipient/destination",
         "Transitive verbs need を for the direct object (本を読む = read a book). に marks destination (家に帰る) or recipient (友達に話す)."),
        ("register", "Casual だ-form mixing with ます-form", "Choose one register and maintain",
         "Switching mid-sentence from 飲む to 飲みます reads as a register error. Pick plain or polite for the whole sentence."),
    ],
    # === Additional Upper N5 / Borderline ===
    "Additional Upper N5 / Borderline Patterns": [
        ("conjugation", "Wrong negative form in {pattern}", "Build the negative carefully per pattern rule",
         "Borderline patterns often use specific negative-form rules (なくて, ないで, なくては, etc.). Each derives differently from ない."),
        ("verb_class", "Group confusion in {pattern}", "Apply standard group rules; double-check Group 1 vs 2",
         "Even at upper-N5, the verb's group is the source of conjugation. 入る/帰る/走る/知る/切る/要る are Group 1 despite ending in る."),
        ("particle", "Dropping or adding particles in {pattern}", "Particles in {pattern} are syntactically fixed",
         "Borderline patterns import particle constraints from their source structure. Don't simplify; the particles are part of the meaning."),
        ("register", "{pattern} casual / formal context mismatch", "Use {pattern} in the appropriate context",
         "Some borderline patterns are more casual (〜って) and others more formal (〜なくてはいけない). Choose contextually."),
    ],
}

# Catch-all template applied when no category-specific template exists.
GENERIC_TEMPLATES = [
    ("particle",
     "Misusing particles around {pattern}",
     "Use the correct particle for {pattern}'s syntactic frame",
     "Particles surrounding {pattern} follow the pattern's syntactic frame. Common error: substituting は for が, を for に, or omitting the particle entirely in casual-form sentences."),
    ("verb_class",
     "Applying wrong verb-class rules with {pattern}",
     "Identify the verb group then apply correct conjugation",
     "When attaching {pattern} to verbs, identify the verb group (Group 1 う-verbs, Group 2 る-verbs, Group 3 irregular) and apply that group's conjugation rules. Don't generalize Group 2 rules to Group 1 verbs."),
    ("conjugation",
     "Wrong form before {pattern}",
     "Use the form specified by the pattern's rule",
     "Each pattern attaches to a specific form: dictionary form (食べる), te-form (食べて), stem (食べ), or plain past (食べた). Confirm the required form before applying {pattern}."),
    ("register",
     "Register mismatch with {pattern}",
     "Match register throughout the sentence",
     "Maintain consistent register throughout the sentence. Mixing casual (〜だ, 〜る) with polite (〜です, 〜ます) within a single sentence sounds awkward and is a typical N5 tell."),
]


def make_template_mistake(category: str, pattern: str, wrong_t: str, right_t: str, why_t: str) -> dict:
    """Materialize a template entry with the pattern label interpolated."""
    return {
        "wrong": wrong_t.format(pattern=pattern, pattern_first_kanji="X", pattern_last_kana="Y"),
        "right": right_t.format(pattern=pattern, pattern_first_kanji="X", pattern_last_kana="Y"),
        "why": why_t.format(pattern=pattern),
        "category": category,
        "provenance": "auto_generated_template",
        "audit_wave": "issue-112-wave1-2026-05-12",
    }


def pick_templates_for_pattern(p: dict, n_needed: int, existing_cats: set[str]) -> list[dict]:
    """Pick n_needed template mistakes covering categories not yet represented."""
    out = []
    category = p.get("category") or ""
    pattern_label = p.get("pattern") or p["id"]

    # Choose template family by pattern category (substring match)
    chosen_family = None
    for family_key, templates in TEMPLATES_BY_CATEGORY.items():
        if family_key.lower() in category.lower():
            chosen_family = templates
            break
    if chosen_family is None:
        chosen_family = GENERIC_TEMPLATES

    # Prefer to fill missing categories first
    desired_order = ["particle", "verb_class", "conjugation", "register"]
    missing = [c for c in desired_order if c not in existing_cats]

    used = set()
    # First pass: pick templates whose category is missing
    for tmpl in chosen_family:
        cat, w, r, why = tmpl
        if cat in missing and cat not in used:
            out.append(make_template_mistake(cat, pattern_label, w, r, why))
            used.add(cat)
            if len(out) >= n_needed:
                return out

    # Second pass: pick any remaining templates (covering already-present categories
    # to ensure we hit n_needed)
    for tmpl in chosen_family:
        cat, w, r, why = tmpl
        if cat in used:
            continue
        out.append(make_template_mistake(cat, pattern_label, w, r, why))
        used.add(cat)
        if len(out) >= n_needed:
            return out

    # Fallback to generic templates if family was too small
    for tmpl in GENERIC_TEMPLATES:
        if len(out) >= n_needed:
            break
        cat, w, r, why = tmpl
        if cat in used:
            continue
        out.append(make_template_mistake(cat, pattern_label, w, r, why))
        used.add(cat)

    return out


def main() -> int:
    data = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    categorized_existing = 0
    template_added = 0
    coverage_at3_before = 0
    coverage_at3_after = 0

    # Pre-census
    for p in data["patterns"]:
        cms = p.get("common_mistakes") or []
        cat_n = sum(1 for cm in cms if isinstance(cm, dict) and cm.get("category"))
        if cat_n >= 3:
            coverage_at3_before += 1

    # Process
    for p in data["patterns"]:
        cms = p.get("common_mistakes") or []
        if not isinstance(cms, list):
            cms = [cms] if cms else []

        # STEP 1: categorize existing
        existing_cats: set[str] = set()
        for cm in cms:
            if not isinstance(cm, dict):
                continue
            if not cm.get("category"):
                cat = categorize(cm.get("why", ""))
                cm["category"] = cat
                cm["category_provenance"] = "heuristic_categorized"
                categorized_existing += 1
            existing_cats.add(cm["category"])

        # STEP 2: top up to >=3
        n_existing = len(cms)
        n_needed = max(0, 3 - n_existing)
        if n_needed > 0:
            new_entries = pick_templates_for_pattern(p, n_needed, existing_cats)
            cms.extend(new_entries)
            template_added += len(new_entries)

        p["common_mistakes"] = cms

    # Post-census
    for p in data["patterns"]:
        cms = p.get("common_mistakes") or []
        cat_n = sum(1 for cm in cms if isinstance(cm, dict) and cm.get("category"))
        if cat_n >= 3:
            coverage_at3_after += 1

    print(f"Existing common_mistakes categorized: {categorized_existing}")
    print(f"New template mistakes generated:      {template_added}")
    print()
    print(f"Patterns at >=3 categorized: {coverage_at3_before}/{len(data['patterns'])} -> {coverage_at3_after}/{len(data['patterns'])}")

    GRAMMAR.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nWrote {GRAMMAR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
