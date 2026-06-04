"""Apply native-reviewer Batch F — section-level fixes (2026-06-04).

The reviewer's consolidated report flagged dozens of specific entries in
the section-level feedback sections (11-30). Batch F applies the changes
that don't need a second-round native pass on replacements:

  F1) Legacy markers for きしゃ / じびき / せびろ.
  F2) なく — disambiguate 鳴く (animals) vs 泣く (human crying).
  F3) Pronoun pragmatic notes — かのじょ, かれ, じぶん, あなた.
  F4) 先生 — title-word usage note (teacher / doctor / honorific).
  F5) Greetings context notes — しつれいします, しつれいしました,
      さようなら, おかえりなさい, おかげさまで, ごちそうさまでした.
  F6) Key contrast notes — うみ/みずうみ, ごはん/こめ, おさけ,
      カップ/コップ.
  F7) な-adj predicate note — すき, だいすき, きらい, だいきらい.
  F8) きれい — dual meaning (pretty/beautiful AND clean).

Read backup: data/vocab.json.bak_2026_06_04_batch_f
Run from N5/:
    python tools/apply_native_review_batch_f_2026_06_04.py --dry-run
    python tools/apply_native_review_batch_f_2026_06_04.py
"""
from __future__ import annotations
import argparse, io, json, sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "vocab.json"

PROV = "native_review_2026_06_04 (batch F: section-level fixes)"


def add_pragmatic(entry, new_notes, log_prefix, log):
    """Append pragmatic_functions entries; preserve any prior ones; tag provenance."""
    existing = entry.get("pragmatic_functions") or []
    # Avoid duplicating if a same-function note already exists.
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
    """Find a single entry by form. Returns first match (form, not reading)."""
    for e in entries:
        if e.get("form") == form:
            return e
    return None


# ---------------------------------------------------------------------------
# F1) Legacy markers
# ---------------------------------------------------------------------------
F1_LEGACY_NOTES = {
    "きしゃ": [{
        "function": "Legacy / archaic — use 電車 instead in modern Japanese",
        "gloss": "きしゃ originally meant a steam-powered train. Today, ordinary trains are called 電車 (でんしゃ).",
        "context": "きしゃ still appears in older N5 wordlists and historical texts, but a modern speaker would say 電車. Recognize it for reading; prefer 電車 for speaking and writing."
    }],
    "じびき": [{
        "function": "Legacy / archaic — use じしょ instead in modern Japanese",
        "gloss": "じびき is the older word for 'dictionary'; modern Japanese uses じしょ (辞書).",
        "context": "じびき still appears in some older N5 lists and pre-war literature; recognize it for reading but prefer じしょ in active vocabulary."
    }],
    "せびろ": [{
        "function": "Legacy / older term — use スーツ instead in modern Japanese",
        "gloss": "せびろ is the older Japanese word for 'business suit'; modern Japanese uses the loanword スーツ.",
        "context": "せびろ appears in older texts and some N5 wordlists; a 20th-century salaryman novel might use it. Today's speaker says スーツ."
    }],
}


# ---------------------------------------------------------------------------
# F2) なく — disambiguate 鳴く (animals / non-human) vs 泣く (humans)
# ---------------------------------------------------------------------------
F2_NAKU = [{
    "function": "Animal/non-human sound vs human crying — different kanji",
    "gloss": "Same kana なく, two different kanji: 鳴く is for animal sounds (a dog barks, a cat meows, a bird sings, an insect chirps); 泣く is for a human crying tears.",
    "context": "This entry covers the 鳴く sense (animals). For a person crying, use 泣く. Common N5 examples: 「いぬが なく」=  the dog barks (鳴く). 「あかちゃんが なく」 = the baby cries (泣く)."
}]


# ---------------------------------------------------------------------------
# F3) Pronoun pragmatic notes
# ---------------------------------------------------------------------------
F3_KANOJO = [{
    "function": "Primary modern sense = girlfriend, not generic 'she'",
    "gloss": "In everyday modern Japanese, かのじょ usually means 'girlfriend'. Used as a generic pronoun for 'she/her' it sounds formal or literary — and can imply romantic relationship if mis-applied.",
    "context": "For a non-romantic 'she', native speakers usually use the person's name + さん, the job title, or just omit the subject entirely. Example: 「田中さんは 先生です」 'Tanaka-san is a teacher' — not 「かのじょは 先生です」."
}]

F3_KARE = [{
    "function": "Primary modern sense = boyfriend, not generic 'he'",
    "gloss": "In everyday modern Japanese, かれ usually means 'boyfriend'. Used as a generic pronoun for 'he/him' it sounds formal or literary — and can imply romantic relationship if mis-applied.",
    "context": "For a non-romantic 'he', native speakers usually use the person's name + さん, the job title, or just omit the subject entirely. Example: 「田中さんは 学生です」 'Tanaka-san is a student' — not 「かれは 学生です」."
}]

F3_JIBUN = [{
    "function": "'Oneself' — most natural in 自分で / 自分の patterns",
    "gloss": "じぶん means 'oneself'. The most common N5 usage is in 自分で (by oneself) and 自分の (one's own / my own).",
    "context": "Example: 「じぶんで します」 = 'I'll do it myself.' 「じぶんの ほん」 = 'my own book.' Note: 「じぶんは…」 as a generic subject can sound odd in conversation — Japanese typically drops the subject or uses わたし."
}]

F3_ANATA = [{
    "function": "'You' — use with caution; sounds blunt or intimate",
    "gloss": "あなた is grammatically 'you', but native speakers rarely use it. Defaults to direct/blunt with strangers, or intimate/married-couple between partners.",
    "context": "Safer alternatives: the person's name + さん, their job title (先生 / 店員さん / お客さん), a kinship term (お母さん / おじいさん), or simply omit the subject. Example: 「田中さんは どこから ですか」, not 「あなたは どこから ですか」."
}]


# ---------------------------------------------------------------------------
# F4) 先生 — title-word usage note
# ---------------------------------------------------------------------------
F4_SENSEI = [{
    "function": "Honorific title for teachers, doctors, masters, and certain professionals",
    "gloss": "先生 isn't only 'teacher' — it's the respectful title used for any expert authority: teachers, doctors, lawyers, dentists, traditional-arts masters, novelists, politicians, etc.",
    "context": "Used as a title attached to a name: 田中先生 = 'Dr./Prof./Sensei Tanaka'. Used standalone, 先生! is how a student calls a teacher in class, or a patient addresses their doctor. Don't translate it as just 'teacher' — the role is wider."
}]


# ---------------------------------------------------------------------------
# F5) Greetings context notes
# ---------------------------------------------------------------------------
F5_SHITSUREI_SHIMASU = [{
    "function": "Polite 'excuse me' — said BEFORE doing something potentially intrusive",
    "gloss": "Used when entering a room, hanging up the phone, leaving someone's presence, or interrupting — to acknowledge that you're about to inconvenience or disturb someone.",
    "context": "Example contexts: knocking and entering a teacher's office (しつれいします); ending a phone call politely (それでは、しつれいします); leaving work before colleagues (おさきに しつれいします). The pair しつれいしました is said AFTER the inconvenience."
}]

F5_SHITSUREI_SHIMASHITA = [{
    "function": "Polite 'excuse me (for what I did)' — said AFTER the inconvenience",
    "gloss": "Past-form pair to しつれいします. Said after the action that may have inconvenienced someone: after leaving a room, after taking up someone's time, after a small mistake.",
    "context": "Example: leaving the teacher's office after a meeting: しつれいしました. Bumping into someone: あ、しつれいしました. Don't confuse with しつれいします (BEFORE) and ごめんなさい (for fault/apology)."
}]

F5_SAYOUNARA = [{
    "function": "'Goodbye' — surprisingly formal in modern usage; often NOT used among friends",
    "gloss": "Native speakers reserve さようなら for relatively formal goodbyes, school dismissals, or longer separations. Everyday casual 'bye' is じゃあね / じゃあ / バイバイ.",
    "context": "Saying さようなら to your roommate as you leave for the day sounds odd or even final (like 'farewell forever'). Use じゃあね or またね for casual. Use さようなら when leaving a job, parting at a station, formal ceremonies."
}]

F5_OKAERINASAI = [{
    "function": "'Welcome back' — said TO someone arriving home, in response to ただいま",
    "gloss": "Used by people inside the home (family, host) to greet someone who has just come back. Forms a fixed pair: 「ただいま」 → 「おかえりなさい」.",
    "context": "Casual: おかえり (no なさい). Said in the home, not in shops (shops use いらっしゃいませ). Workplace return-from-trip equivalent: お疲れさま (おつかれさま)."
}]

F5_OKAGESAMA = [{
    "function": "Polite acknowledgement when someone asks how you are",
    "gloss": "Often a polite reply to 「お元気ですか」 or to 'How is your business / family / health?' — meaning roughly 'thanks to you / thanks to your kindness'.",
    "context": "Example: 「お元気ですか」 → 「はい、おかげさまで。」 ('Yes, doing well thanks to you/kind support.') Implies humility — credits the asker or general circumstance for the speaker's good situation. Don't use it as a literal 'thank you for X'."
}]

F5_GOCHISOUSAMA = [{
    "function": "Said AFTER eating — closes the meal politely",
    "gloss": "Fixed-pair partner to いただきます (said BEFORE eating). Acknowledges the meal and the labour that produced it. Said even when eating alone, in restaurants, or after being treated.",
    "context": "Casual form: ごちそうさま (no でした). When someone treated you to a meal, said directly to them as thanks. Don't drop the verb past-form ending in formal situations: ごちそうさまでした is the polite version."
}]


# ---------------------------------------------------------------------------
# F6) Key contrast notes
# ---------------------------------------------------------------------------
F6A_UMI = [{
    "function": "Sea / ocean — NOT lake (use みずうみ for lake)",
    "gloss": "うみ = salt-water sea or ocean. For an inland fresh-water body of water, use みずうみ (湖).",
    "context": "Examples: 海に いきます = 'go to the sea/ocean'. 湖の そばに すみます = 'live near a lake'. Don't translate English 'lake' as うみ."
}]

F6A_MIZUUMI = [{
    "function": "Lake (fresh-water, inland) — NOT sea (use うみ for sea/ocean)",
    "gloss": "みずうみ = inland fresh-water body. For salt-water ocean or sea, use うみ (海).",
    "context": "Examples: びわ湖は 日本で 一番 大きい みずうみです = 'Lake Biwa is the largest lake in Japan.'"
}]

F6C_GOHAN = [{
    "function": "Cooked rice — AND 'meal' more generally",
    "gloss": "ごはん covers both 'cooked rice' (the white grain on your plate) AND 'a meal' (breakfast/lunch/dinner generally — even without rice).",
    "context": "Examples: 「ごはんを たべます」 can mean 'I'll eat (a meal)' OR 'I'll eat (cooked) rice', depending context. 朝ごはん = breakfast; 夕ごはん = dinner. For uncooked rice grain, use 米 (こめ)."
}]

F6C_KOME = [{
    "function": "Uncooked rice grain — NOT a meal, NOT cooked rice",
    "gloss": "こめ is rice as a commodity / raw grain (e.g., what farmers grow, what you buy at a shop). Cooked rice on your plate is ごはん.",
    "context": "Example: 日本人は 米を たくさん たべます (literal: 'Japanese people eat a lot of rice' — fine because it speaks generically about rice as food). But at the table: ごはんを ください, not 米を ください."
}]

F6D_OSAKE = [{
    "function": "Alcohol generally — not only Japanese sake",
    "gloss": "おさけ (お酒) is the generic Japanese word for alcoholic beverages: beer, wine, whisky, sake (Japanese rice wine), all included.",
    "context": "If you specifically mean Japanese rice wine, you can say にほんしゅ (日本酒). 'Drinking alcohol' generally: おさけを のむ. English speakers often think おさけ = 'sake' but it's much broader."
}]

F6E_KAPPU = [{
    "function": "Loanword 'cup' — typically for warm drinks (tea, coffee) and with a handle",
    "gloss": "カップ (from English 'cup') is the type with a handle, often used for hot drinks: a coffee cup, a teacup. Also: trophy cup, measuring cup.",
    "context": "Contrast with コップ (from Dutch 'kop'): a tumbler-shaped glass without a handle, typically for cold drinks like water or juice. ジュースを コップで のみます = 'drink juice from a glass'."
}]

F6E_KOPPU = [{
    "function": "Loanword 'cup/glass' — tumbler-shaped, typically for cold drinks",
    "gloss": "コップ (from Dutch 'kop') is a tumbler-style drinking vessel, usually no handle, often glass. Used for water, juice, beer, etc.",
    "context": "Contrast with カップ (from English): handled, often porcelain, typically for hot drinks like coffee or tea. コーヒーは カップで のみます = 'drink coffee from a (handled) cup'."
}]


# ---------------------------------------------------------------------------
# F7) Adjective-predicate notes (すき / だいすき / きらい / だいきらい)
# ---------------------------------------------------------------------------
F7_SUKI = [{
    "function": "な-adjective, not a verb — 'liked' or 'pleasing'",
    "gloss": "English 'like' is a verb, but すき is a な-adjective in Japanese. The thing liked is the GRAMMATICAL SUBJECT marked with が; the person doing the liking is the topic marked with は.",
    "context": "Pattern: 「Xは Yが すきです」 = 'X likes Y' (literally: 'as for X, Y is pleasing'). Example: 「わたしは すしが すきです」 = 'I like sushi.' Note the が — NOT を like an English 'like' verb."
}]

F7_DAISUKI = [{
    "function": "な-adjective intensifier of すき — 'love' or 'really like'",
    "gloss": "Built from だい (大, 'big') + すき. Same grammar as すき: thing-liked is marked with が, person-doing-the-liking with は. Translates loosely as 'love' but is more like 'really like / am very fond of'.",
    "context": "Example: 「いぬが だいすきです」 = 'I love dogs.' For romantic love use 愛している (あいしている) — N3 vocabulary; だいすき in romance contexts is closer to 'I really like you' / 'I'm crazy about you'."
}]

F7_KIRAI = [{
    "function": "な-adjective, not a verb — 'disliked' or 'unpleasant'",
    "gloss": "Mirror of すき. The thing disliked is the grammatical subject marked with が; the person doing the disliking is the topic marked with は.",
    "context": "Pattern: 「Xは Yが きらいです」 = 'X dislikes Y' (literally: 'as for X, Y is unpleasant'). Example: 「わたしは なっとうが きらいです」 = 'I don't like natto.'"
}]

F7_DAIKIRAI = [{
    "function": "な-adjective intensifier of きらい — 'hate' or 'really dislike'",
    "gloss": "Built from だい (大, 'big') + きらい. Same grammar as きらい. Stronger than 'don't like' — closer to 'hate' or 'really can't stand'.",
    "context": "Example: 「むしが だいきらいです」 = 'I hate insects.' Use sparingly — it's a strong word, especially toward people."
}]


# ---------------------------------------------------------------------------
# F8) きれい — dual meaning (pretty AND clean)
# ---------------------------------------------------------------------------
F8_KIREI = [{
    "function": "Two distinct senses in one word: 'pretty/beautiful' AND 'clean/tidy'",
    "gloss": "きれい covers both 'visually attractive' (pretty/beautiful) AND 'free from dirt' (clean/tidy). Context disambiguates.",
    "context": "Examples: 「きれいな 花」 = 'pretty flowers' (visual beauty). 「へやが きれいです」 = 'the room is clean / tidy' (cleanliness). Same word, just two senses. Also note: きれい LOOKS like an い-adjective but is actually a な-adjective (きれいな + noun; きれいです at sentence end)."
}]


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
JOBS = [
    # (form, notes, log_prefix)
    ("きしゃ",       F1_LEGACY_NOTES["きしゃ"],  "F1-a"),
    ("じびき",       F1_LEGACY_NOTES["じびき"],  "F1-b"),
    ("せびろ",       F1_LEGACY_NOTES["せびろ"],  "F1-c"),
    ("なく",         F2_NAKU,                    "F2  "),
    ("かのじょ",     F3_KANOJO,                  "F3-a"),
    ("かれ",         F3_KARE,                    "F3-b"),
    ("じぶん",       F3_JIBUN,                   "F3-c"),
    ("あなた",       F3_ANATA,                   "F3-d"),
    ("先生",         F4_SENSEI,                  "F4  "),
    ("しつれいします",   F5_SHITSUREI_SHIMASU,   "F5-a"),
    ("しつれいしました", F5_SHITSUREI_SHIMASHITA, "F5-b"),
    ("さようなら",   F5_SAYOUNARA,               "F5-c"),
    ("おかえりなさい", F5_OKAERINASAI,            "F5-d"),
    ("おかげさまで", F5_OKAGESAMA,               "F5-e"),
    ("ごちそうさまでした", F5_GOCHISOUSAMA,       "F5-f"),
    ("うみ",         F6A_UMI,                    "F6a-1"),
    ("みずうみ",     F6A_MIZUUMI,                "F6a-2"),
    ("ごはん",       F6C_GOHAN,                  "F6c-1"),
    ("こめ",         F6C_KOME,                   "F6c-2"),
    ("おさけ",       F6D_OSAKE,                  "F6d"),
    ("カップ",       F6E_KAPPU,                  "F6e-1"),
    ("コップ",       F6E_KOPPU,                  "F6e-2"),
    ("すき",         F7_SUKI,                    "F7-a"),
    ("だいすき",     F7_DAISUKI,                 "F7-b"),
    ("きらい",       F7_KIRAI,                   "F7-c"),
    ("だいきらい",   F7_DAIKIRAI,                "F7-d"),
    ("きれい",       F8_KIREI,                   "F8  "),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    v = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = v.get("entries", [])
    log = []
    n = 0
    for form, notes, prefix in JOBS:
        e = find_one(entries, form)
        if e is None:
            log.append(f"  {prefix} SKIP: form {form!r} not in corpus")
            continue
        if add_pragmatic(e, notes, prefix, log):
            n += 1

    print(f"Batch F — section-level fixes")
    print(f"  jobs: {len(JOBS)}")
    print(f"  entries touched: {n}")
    print()
    if args.dry_run:
        print("(DRY RUN — no file written)")
    else:
        meta = v.get("_meta") or {}
        meta["native_review_pass_2026_06_04_batch_f"] = (
            f"Batch F applied: {n} of {len(JOBS)} target entries received "
            "pragmatic_functions additions covering legacy markers (F1), "
            "なく animal/human kanji split (F2), pronoun usage cautions (F3), "
            "先生 honorific scope (F4), greeting context (F5), key "
            "lexical contrasts (F6), な-adj predicate grammar (F7), and "
            "きれい dual-meaning (F8). Driver: "
            "tools/apply_native_review_batch_f_2026_06_04.py."
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
