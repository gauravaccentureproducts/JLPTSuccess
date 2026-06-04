"""Apply native-reviewer Batch G — final P1/P2 section-level fixes (2026-06-04).

Follow-up to batch F. Tackles the remaining concrete pragmatic notes
from the consolidated 2026-06-04 native-reviewer report sections 11-30
that didn't fit in batch F.

  G1)  学生 vs せいと scope
  G2)  けいかん vs おまわりさん tone
  G3)  外国人 pragmatic caution
  G4)  一日 readings — ついたち (1st of month) vs いちにち (one day)
  G5)  こんや vs こんばん distinction
  G6)  アルバイト → バイト abbreviation
  G7)  いっぱい — full vs a lot
  G8)  ただ — just / only / simply
  G9)  しか — requires negative predicate
  G10) ぐらい vs くらい
  G11) やはり formality note (やっぱり absent from corpus)
  G12) ことば vs たんご scope
  G13) 何で — why vs by-what-means
  G14) ほしい — adjective-of-desire grammar
  G15) ござる — very polite copula
  G16) はやい — 早い (early) vs 速い (fast) split
  G17) やさしい — 易しい (easy) vs 優しい (kind) split
  G18) おてあらい vs トイレ politeness
  G19) おふろ vs シャワー bathing culture
  G20) せ — back vs height; 足 — leg vs foot
  G21) じ / もじ / かんじ / かな / ひらがな / カタカナ distinctions
  G22) からい — primary 'spicy', occasional 'salty'
  G23) いっぱい vs たくさん vs すこし vs ちょっと scope
  G24) Color noun vs adjective forms (白 vs 白い etc.)
  G26) はブラシ orthographic note

Run from N5/:
    python tools/apply_native_review_batch_g_2026_06_04.py --dry-run
    python tools/apply_native_review_batch_g_2026_06_04.py
"""
from __future__ import annotations
import argparse, io, json, sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "vocab.json"
PROV = "native_review_2026_06_04 (batch G: section-level P1/P2 fixes)"


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
    log.append(f"  {log_prefix} {entry['id']}: +{len(to_add)} entry(ies)")
    return True


def find_one(entries, form):
    for e in entries:
        if e.get("form") == form:
            return e
    return None


# ---------------------------------------------------------------------------
JOBS = []

# G1 — 学生 vs せいと scope
JOBS.append(("学生", [{
    "function": "Older students — typically university / college / high-school age",
    "gloss": "学生 (がくせい) usually refers to STUDENTS in higher education — university, college, sometimes high school. For elementary or junior-high schoolchildren, the more usual word is せいと (生徒).",
    "context": "English 'student' covers both, but Japanese typically reserves 学生 for the older end. Example: 「大学の 学生です」 = 'I'm a university student.' For a primary-schooler, prefer せいと or 小学生 (しょうがくせい)."
}], "G1-a"))

JOBS.append(("せいと", [{
    "function": "Younger students / pupils — typically elementary, junior-high, or high school",
    "gloss": "せいと (生徒) refers to pupils in compulsory education and high school. For university and college, use 学生 (がくせい).",
    "context": "Example: 「中学校の せいとです」 = 'I'm a junior-high-school pupil.' English 'student' translates to both 学生 and せいと depending on level."
}], "G1-b"))

# G2 — police tone
JOBS.append(("けいかん", [{
    "function": "Formal / descriptive — 'police officer'",
    "gloss": "けいかん (警官) is the formal / written / news-register word for a police officer. Direct address or warm reference uses おまわりさん.",
    "context": "けいかん appears in news, official documents, signage. To call out to or warmly refer to an officer (especially in conversation with children), use おまわりさん."
}], "G2-a"))

JOBS.append(("おまわりさん", [{
    "function": "Warm / child-friendly / direct-address — 'the (friendly) police officer'",
    "gloss": "おまわりさん is the everyday / child-friendly form for a police officer. Built from まわる ('to go around', as in patrolling) + the お…さん honorific frame.",
    "context": "Used when speaking to children about police, when directly addressing an officer, or in friendly conversational reference. For formal / written register, use けいかん (警官)."
}], "G2-b"))

# G3 — foreigner pragmatic caution
JOBS.append(("外国人", [{
    "function": "Pragmatic caution — 'foreigner' can sound exclusionary in direct address",
    "gloss": "外国人 (がいこくじん) literally means 'foreign-country person'. The word is accurate but in direct address it can feel othering — many residents of Japan find it cold when applied to them personally.",
    "context": "For a more neutral / friendly tone: 海外から 来た方 (かいがいから きた かた) = 'a person from overseas', or just refer to the person by name + さん / nationality (アメリカ人 / フランス人). Used naturally in news, statistics, or general statements about non-Japanese people."
}], "G3"))

# G4 — 一日 readings
# Both 一日 entries exist; we add the disambiguation note to both
def _ichinichi_notes(role):
    return [{
        "function": "Two readings — ついたち (1st day of month) vs いちにち (one day / whole day)",
        "gloss": "一日 has two readings with different meanings: ついたち = the 1st day of the month (a date); いちにち = one day or 'a whole day' (a duration).",
        "context": "ついたち is irregular — it's the only date in the 1-10 sequence not formed by Sino-Japanese counting; comes from 月立ち (the start of the month). Examples: 「七月一日」(しちがつ ついたち) = July 1st. 「一日中」(いちにち じゅう) = 'all day long'. {role}"
    }]
# Both 一日 entries get a note (they may already differentiate by id suffix).

# G5 — こんや vs こんばん
JOBS.append(("こんや", [{
    "function": "'Tonight' — slightly more formal / written than こんばん",
    "gloss": "こんや (今夜) and こんばん (今晩) both mean 'tonight', but こんや has a slightly more formal, written, or newscaster feel. Conversational everyday speech usually uses こんばん.",
    "context": "Examples: 「こんばんは 寒いです」 (informal, spoken) = 'It's cold tonight.' 「こんやの ニュースで…」 (newscast / formal) = 'In tonight's news...'"
}], "G5-a"))

JOBS.append(("こんばん", [{
    "function": "'Tonight' — the conversational default",
    "gloss": "こんばん (今晩) is the everyday spoken word for 'tonight'. The greeting 「こんばんは」 ('good evening') is built from this word + the topic particle は.",
    "context": "More formal / written alternative: こんや (今夜). Pair: 「こんばん 何を しますか」 = 'What are you doing tonight?'"
}], "G5-b"))

# G6 — アルバイト
JOBS.append(("アルバイト", [{
    "function": "Often abbreviated to バイト in casual speech",
    "gloss": "アルバイト (from German 'Arbeit', 'work') means a part-time job. In casual conversation it's frequently shortened to バイト.",
    "context": "Examples: 「アルバイトを しています」 (formal/neutral) = 'I have a part-time job.' 「バイトに 行く」 (casual, very common) = 'I'm off to my part-time gig.' Both refer to the same thing."
}], "G6"))

# G7 — いっぱい
JOBS.append(("いっぱい", [{
    "function": "Two senses — 'full' (container) vs 'a lot' (quantity)",
    "gloss": "いっぱい covers both 'full / brimming' (a glass is いっぱい of water) AND 'a lot / many' (today there are いっぱい of people).",
    "context": "Examples: 「コップに 水が いっぱい あります」 = 'The cup is full of water.' 「公園に 人が いっぱい います」 = 'There are a lot of people in the park.' Context (specific container vs general scene) disambiguates."
}], "G7"))

# G8 — ただ
JOBS.append(("ただ", [{
    "function": "Multiple senses — 'just / only / merely', 'free of charge', 'however / but'",
    "gloss": "ただ has several meanings: (1) 'only / merely / just' — limits or restricts; (2) 'free of charge' — no cost; (3) 'however / but' — adversative connector at sentence start.",
    "context": "Examples: 「ただの 学生です」 = 'I'm just a student.' 「ただで もらいました」 = 'I got it for free.' 「行きたいです。ただ、時間が ありません」 = 'I want to go. However, I don't have time.' Context disambiguates."
}], "G8"))

# G9 — しか
JOBS.append(("しか", [{
    "function": "ALWAYS pairs with a negative predicate — 'only / nothing but'",
    "gloss": "しか is a restrictive particle that REQUIRES a negative predicate. Together they mean 'only X' with an implicit 'and not more'. Pattern: 「Xしか〜ない」.",
    "context": "Examples: 「水しか のみません」 = 'I drink only water (and nothing else).' 「1000円しか ありません」 = 'I have only 1000 yen.' Note: the verb must be negative — you can't say 「水しか のみます」 (ungrammatical). Contrast with だけ (positive predicate OK): 「水だけ のみます」 = 'I drink only water.'"
}], "G9"))

# G10 — ぐらい vs くらい
JOBS.append(("ぐらい", [{
    "function": "Approximation suffix — 'about / approximately'",
    "gloss": "ぐらい / くらい attach to quantities and times to mean 'about / approximately'. The two forms are mostly interchangeable; ぐらい is slightly more common after consonant-final words, くらい slightly more common at the start of a phrase or for emphasis.",
    "context": "Examples: 「1時間ぐらい かかります」 = 'It takes about an hour.' 「100人くらい 来ました」 = 'About 100 people came.' Either form works in most contexts; rule of thumb: when in doubt, ぐらい."
}], "G10-a"))

JOBS.append(("くらい", [{
    "function": "Approximation suffix — interchangeable with ぐらい",
    "gloss": "くらい / ぐらい are the same particle in two voiced/unvoiced forms. くらい is slightly more common phrase-initially and after vowel-final words; ぐらい is slightly more common after consonant-final words.",
    "context": "Same examples as ぐらい — see that entry. Standard textbooks treat them as free variants for N5 purposes."
}], "G10-b"))

# G11 — やはり
JOBS.append(("やはり", [{
    "function": "Formal / written — colloquial spoken form is やっぱり",
    "gloss": "やはり ('as expected / after all / indeed') is the formal/written register. In casual conversation, native speakers usually say やっぱり.",
    "context": "Examples: 「やはり 来ましたね」 (slightly formal) = 'You came after all.' 「やっぱり おいしい!」 (casual) = 'It IS delicious, just like I thought!' Either form is grammatical; switch register depending on context."
}], "G11"))

# G12 — ことば vs たんご
JOBS.append(("ことば", [{
    "function": "Broad scope — 'word', 'language', or 'speech / what someone said'",
    "gloss": "ことば covers a wide range: a single word, a language (Japanese, English), or 'what someone said / their speech'. For 'vocabulary item / lexical entry' specifically, the narrower word is たんご.",
    "context": "Examples: 「日本語の ことば」 = 'a Japanese word' OR 'the Japanese language'. 「親切な ことば」 = 'kind words / kind speech'. For a vocabulary drill: 「たんごを おぼえる」 = 'memorize vocabulary'."
}], "G12-a"))

JOBS.append(("たんご", [{
    "function": "Narrow scope — 'vocabulary item / individual word as a lexical entry'",
    "gloss": "たんご (単語) means 'word' as an entry in a dictionary or vocabulary list — the unit you drill, memorize, or look up. ことば is the broader term covering language / speech / utterance.",
    "context": "Examples: 「今日は たんごを 20個 おぼえました」 = 'Today I memorized 20 vocabulary words.' 「たんごテスト」 = 'vocabulary test'. Use ことば for the broader senses."
}], "G12-b"))

# G14 — ほしい
JOBS.append(("ほしい", [{
    "function": "い-adjective expressing desire — NOT a verb",
    "gloss": "ほしい means 'want / desired' but is grammatically an い-adjective, not a verb. The thing wanted is marked with が (the grammatical subject), and the person wanting it is marked with は (the topic).",
    "context": "Pattern: 「Xは Yが ほしいです」 = 'X wants Y' (literally: 'as for X, Y is desired'). Example: 「わたしは くるまが ほしいです」 = 'I want a car.' Note: ほしい is for objects/things. For 'want to DO an action', use the Vたい form: 「行きたいです」 = 'I want to go'."
}], "G14"))

# G15 — ござる
JOBS.append(("ござる", [{
    "function": "Very polite — almost always seen in the form ございます",
    "gloss": "ござる is the ultra-polite copula / existence verb. It is almost never used in its plain dictionary form; what you'll actually see is ございます (the polite-form conjugation).",
    "context": "Examples: 「ありがとう ございます」 = 'thank you (polite)'. 「おはよう ございます」 = 'good morning (polite)'. 「Xが ございます」 = 'there is X (very polite, often in shops/restaurants)'. As an N5 learner, recognize ござる as the root of these set phrases."
}], "G15"))

# G16 — はやい
JOBS.append(("はやい", [{
    "function": "Two kanji, two meanings — 早い (early) vs 速い (fast)",
    "gloss": "Same kana はやい, two different kanji: 早い means 'early' (time); 速い means 'fast' (speed). Context disambiguates when written in kana.",
    "context": "Examples: 「あさが はやい」 = '(my) morning is early' (= I get up early). 「はやく はしる」 = 'run fast'. When writing, prefer the kanji to remove ambiguity. When reading, look at what's being modified: time-related → 早い; motion-related → 速い."
}], "G16"))

# G17 — やさしい
JOBS.append(("やさしい", [{
    "function": "Two kanji, two meanings — 易しい (easy) vs 優しい (kind/gentle)",
    "gloss": "Same kana やさしい, two different kanji and meanings: 易しい = 'easy / simple'; 優しい = 'kind / gentle / considerate'. Context (modifying a person vs a task) usually disambiguates.",
    "context": "Examples: 「やさしい もんだいです」 = 'It's an easy problem' (易しい). 「やさしい 人です」 = 'They are a kind person' (優しい). Same kana, very different meanings — when writing, prefer the kanji."
}], "G17"))

# G18 — おてあらい vs トイレ politeness
JOBS.append(("おてあらい", [{
    "function": "Polite — 'restroom / washroom' (literal: お-hand-wash)",
    "gloss": "おてあらい (お手洗い) is the polite Japanese-style word for restroom. Slightly more euphemistic / refined than トイレ. Common on signage in restaurants, hotels, and businesses.",
    "context": "Example: 「おてあらいは どこですか」 = 'Where is the restroom?' (polite). For everyday casual conversation, トイレ is also fine and very common."
}], "G18-a"))

JOBS.append(("トイレ", [{
    "function": "Everyday — 'toilet / restroom' (loanword)",
    "gloss": "トイレ (from English 'toilet') is the everyday, direct, very common word for toilet/restroom. More casual / direct than おてあらい (お手洗い).",
    "context": "Example: 「トイレに 行きたいです」 = 'I want to go to the toilet.' Both トイレ and おてあらい are widely understood; choose by formality. In a fancy restaurant or business setting, おてあらい sounds more polished."
}], "G18-b"))

# G19 — おふろ vs シャワー
JOBS.append(("おふろ", [{
    "function": "Bath — Japanese-style tub-soaking bath",
    "gloss": "おふろ (お風呂) is a TUB-style bath. In Japanese homes, the tub is typically deep and used for soaking; you wash yourself OUTSIDE the tub first, then enter the clean water to soak.",
    "context": "Example: 「おふろに 入ります」 = 'I take a bath' (literally 'enter the bath'). Note the verb — 入る (enter), not 取る (take). For a quick shower without soaking, use シャワー."
}], "G19-a"))

JOBS.append(("シャワー", [{
    "function": "Shower — quick rinse (loanword, often distinct from soaking-bath)",
    "gloss": "シャワー (from English 'shower') is the quick standing rinse. In Japanese culture, this is often a separate practice from おふろ (the soaking bath) — you might シャワー in the morning and おふろ at night.",
    "context": "Example: 「シャワーを 浴びます」 = 'I take a shower' (literally 'bathe in shower'). Verb collocate is 浴びる (あびる, 'bathe / be exposed to'), not 入る."
}], "G19-b"))

# G20 — body parts dual
JOBS.append(("せ", [{
    "function": "Two meanings — 'back (of body)' AND 'height (stature)'",
    "gloss": "せ (背) covers both 'back' (the body part) and 'height / stature' (how tall someone is).",
    "context": "Examples: 「せが いたい」 = 'My back hurts.' 「せが たかい」 = 'They are tall' (literally: 'their stature is high'). Context disambiguates: pairs with verbs/adjectives of body sensation (痛い, ぶつける) → back; pairs with 高い / 低い → height."
}], "G20-a"))

JOBS.append(("足", [{
    "function": "'Leg' AND 'foot' — Japanese 足 covers both",
    "gloss": "Japanese 足 (あし) covers the entire lower limb — both 'leg' and 'foot'. English splits these; Japanese usually doesn't, unless you need to be specific.",
    "context": "Examples: 「足が ながい」 = 'long legs'. 「足が いたい」 = 'my foot hurts' OR 'my leg hurts' — depending context. For 'foot specifically (sole)' you can say 足首 (あしくび, 'ankle') or 足の うら (sole) — N4+ vocabulary."
}], "G20-b"))

# G21 — kanji/kana family
JOBS.append(("じ", [{
    "function": "Generic 'character / letter' — covers all writing systems",
    "gloss": "じ (字) is the broadest term for a written character: kanji, kana (hiragana/katakana), even Roman letters can be called じ in everyday speech. もじ (文字) is a near-synonym.",
    "context": "Examples: 「じを 書きます」 = 'I write characters.' For a specific system, use the specific name: かんじ, ひらがな, カタカナ. Use じ when you don't need to specify."
}], "G21-a"))

JOBS.append(("もじ", [{
    "function": "Generic 'character / letter / script' — slightly more formal than じ",
    "gloss": "もじ (文字) is a near-synonym of じ but feels slightly more formal / technical. Refers to written characters of any kind.",
    "context": "Examples: 「もじを ならいます」 = 'learn to write characters.' On a computer: もじ is also used for 'character' in the encoding sense (e.g., 文字化け = mojibake / garbled characters)."
}], "G21-b"))

JOBS.append(("かんじ", [{
    "function": "Chinese-origin characters — distinct from kana",
    "gloss": "かんじ (漢字) are the Chinese-origin characters used in Japanese writing. Each kanji has both meaning and (typically multiple) readings. N5 covers ~100 kanji.",
    "context": "Distinct from かな (the syllabic systems ひらがな / カタカナ). Example: 「漢字で 書きます」 = 'I'll write it in kanji.' On the JLPTSuccess kanji pages, each card shows the kanji's On/Kun readings, stroke order, and example words."
}], "G21-c"))

JOBS.append(("かな", [{
    "function": "Umbrella term — both ひらがな and カタカナ together",
    "gloss": "かな is the umbrella term for the two Japanese syllabic systems: ひらがな (hiragana — rounded shapes, native words and grammatical particles) and カタカナ (katakana — angular shapes, loanwords and emphasis).",
    "context": "Examples: 「かなで 書いてください」 = 'Please write in kana' (= either hiragana or katakana, not kanji). When you need to specify, use ひらがな or カタカナ directly."
}], "G21-d"))

JOBS.append(("ひらがな", [{
    "function": "Hiragana — rounded syllabic script for native Japanese words and grammar",
    "gloss": "ひらがな is one of the two Japanese syllabaries (the other is カタカナ). 46 basic characters plus modifications. Used for native Japanese words, verb endings, particles, and as ruby (furigana) reading-hints above kanji.",
    "context": "First script that N5 learners typically master. Distinct from カタカナ (used for loanwords) and かんじ (Chinese-origin meaning-characters)."
}], "G21-e"))

JOBS.append(("カタカナ", [{
    "function": "Katakana — angular syllabic script for loanwords, names, emphasis",
    "gloss": "カタカナ is the other Japanese syllabary. Same sound system as ひらがな but with angular shapes. Used for: loanwords (コーヒー, テレビ), foreign names, scientific names, onomatopoeia, and stylistic emphasis.",
    "context": "An N5 learner needs to recognize both syllabaries. Pair with ひらがな (native words) and かんじ (Chinese-origin characters) to make up the three writing systems used in Japanese."
}], "G21-f"))

# G22 — からい
JOBS.append(("からい", [{
    "function": "Primarily 'spicy / hot in taste' — occasionally 'salty' in some regions",
    "gloss": "からい (辛い) primarily means 'spicy / hot' as in chili pepper, wasabi, mustard. In some regions and older usage it can also mean 'salty', but in modern standard Japanese 'salty' is しょっぱい.",
    "context": "Examples: 「カレーは からい」 = 'Curry is spicy.' 「わさびが からい」 = 'Wasabi is hot/spicy.' For 'salty', prefer しょっぱい in modern usage. からい can also figuratively mean 'harsh' (e.g., harsh criticism = 辛い 評価)."
}], "G22"))

# G24 — color noun vs adjective forms
def _color_noun_note(noun_form, adj_form):
    return [{
        "function": f"Noun form — pair with the い-adjective form '{adj_form}'",
        "gloss": f"{noun_form} is the NOUN form of the color (the color itself, as a concept). The corresponding い-adjective form is {adj_form} (describes a thing as being that color).",
        "context": f"Examples: 「{noun_form}が すきです」 = 'I like {noun_form} (the color).' VS 「{adj_form} ペン」 = 'a {adj_form} pen' (describing a pen). Use the noun when talking about the color itself; use the adjective when describing something's color."
    }]

def _color_adj_note(adj_form, noun_form):
    return [{
        "function": f"い-adjective form — pair with the noun form '{noun_form}'",
        "gloss": f"{adj_form} is the い-ADJECTIVE form (describes a thing as being that color). The noun form (the color itself) is {noun_form}.",
        "context": f"Examples: 「{adj_form} はな」 = 'a {adj_form} flower' (describing a flower). VS 「{noun_form}が すきです」 = 'I like {noun_form} (the color).' Use the adjective when describing; use the noun for the color concept."
    }]

JOBS.append(("白", _color_noun_note("白 (しろ)", "白い (しろい)"), "G24-a"))
JOBS.append(("白い", _color_adj_note("白い (しろい)", "白 (しろ)"), "G24-b"))
JOBS.append(("くろ", _color_noun_note("くろ (黒)", "くろい (黒い)"), "G24-c"))
JOBS.append(("くろい", _color_adj_note("くろい (黒い)", "くろ (黒)"), "G24-d"))
JOBS.append(("あか", _color_noun_note("あか (赤)", "あかい (赤い)"), "G24-e"))
JOBS.append(("あかい", _color_adj_note("あかい (赤い)", "あか (赤)"), "G24-f"))
JOBS.append(("あお", _color_noun_note("あお (青)", "あおい (青い)"), "G24-g"))
JOBS.append(("あおい", _color_adj_note("あおい (青い)", "あお (青)"), "G24-h"))

# G26 — はブラシ orthographic
JOBS.append(("はブラシ", [{
    "function": "Orthography note — usually written 歯ブラシ in modern Japanese",
    "gloss": "はブラシ is the kana-headword form; in modern written Japanese this word is typically written as 歯ブラシ (kanji 歯 'tooth' + katakana ブラシ from English 'brush').",
    "context": "Mixed kanji+katakana words like 歯ブラシ are common — the Japanese-origin part (歯) keeps its kanji, the loanword part (ブラシ) keeps its katakana. Recognize はブラシ in beginner kana-only texts; expect to see 歯ブラシ in real-world reading."
}], "G26"))


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    v = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = v.get("entries", [])
    log = []
    n = 0

    # Run standard jobs (form-based lookup)
    for form, notes, prefix in JOBS:
        e = find_one(entries, form)
        if e is None:
            log.append(f"  {prefix} SKIP: form {form!r} not in corpus")
            continue
        if add_pragmatic(e, notes, prefix, log):
            n += 1

    # G4 — 一日 has TWO entries; touch both
    for e in entries:
        if e.get("form") == "一日":
            sense_hint = e.get("gloss") or ""
            role = ("This entry covers the いちにち (whole day) sense."
                    if "day" in sense_hint.lower() and "1st" not in sense_hint
                    else "This entry covers the ついたち (1st-of-month) sense."
                    if "1st" in sense_hint or "first" in sense_hint.lower()
                    else "")
            notes = [{
                "function": "Two readings — ついたち (1st day of month) vs いちにち (one day / whole day)",
                "gloss": "一日 has two readings with different meanings: ついたち = the 1st day of the month (a date); いちにち = one day or 'a whole day' (a duration).",
                "context": (
                    "ついたち is irregular — the only date in the 1–10 sequence not formed by Sino-Japanese counting; "
                    "etymologically from 月立ち (the start of the month). Examples: 「七月一日」(しちがつ ついたち) = July 1st. "
                    "「一日中」(いちにち じゅう) = 'all day long'. " + role
                ).strip()
            }]
            if add_pragmatic(e, notes, "G4", log):
                n += 1

    # G13 — 何で (refresh / strengthen the note since pragmatic_functions already exists per audit)
    e = find_one(entries, "何で")
    if e is not None:
        notes = [{
            "function": "Two senses — 'why?' (most common) vs 'by what means?'",
            "gloss": "何で (なんで) has two N5-level senses: (1) the casual 'why?' (synonymous with どうして / なぜ); (2) the literal 'by what means / by what method?'. Context disambiguates.",
            "context": (
                "Examples: 「何で 来ましたか」 — most often heard as 'Why did you come?' but literally could be 'By what means did you come?' (car/train/bus/etc.). "
                "「何で 食べますか」 — 'Why do you eat?' OR 'With what do you eat?' (chopsticks/fork). "
                "For unambiguous 'why', prefer どうして. For unambiguous 'by what means', use なにで or その方法は? Note: なんで can also be more casual than どうして / なぜ."
            )
        }]
        if add_pragmatic(e, notes, "G13", log):
            n += 1


    print(f"Batch G — section-level P1/P2 fixes")
    print(f"  jobs: {len(JOBS) + 3}  (incl. G4-double + G13 + special)")
    print(f"  entries touched: {n}")
    print()
    if args.dry_run:
        print("(DRY RUN — no file written)")
    else:
        meta = v.get("_meta") or {}
        meta["native_review_pass_2026_06_04_batch_g"] = (
            f"Batch G applied: {n} entries received additional "
            "pragmatic_functions notes covering G1-G26 section-level "
            "recommendations from the 2026-06-04 native-reviewer report "
            "(student/police scope, foreigner caution, date readings, "
            "tonight, part-time, full-vs-lot, just/only, particle "
            "polarity, approximation, formality split, vocab scope, "
            "question-word ambiguity, adjective-of-desire, polite "
            "copula, early/fast + easy/kind splits, toilet/bath "
            "register, body-part duals, kanji/kana family, spicy/salty, "
            "color noun-vs-adj, hairbrush orthography). "
            "Driver: tools/apply_native_review_batch_g_2026_06_04.py."
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
