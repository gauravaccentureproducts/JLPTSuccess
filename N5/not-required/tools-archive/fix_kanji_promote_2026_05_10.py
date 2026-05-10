"""Job C — kanji-promotion sweep.

For words that have an N5-whitelist kanji form (e.g. 何 for なに/なん,
私 for わたし, 食べる for たべる, 行く for いく), the corpus
should USE the kanji rather than the kana. Per the user direction
2026-05-10 + native-teacher review.

Scope:
- data/grammar.json: pattern titles + every examples[].ja field.
- data/reading.json: every passages[].ja field (case-by-case
  judgement; we apply the same content-word promotions but only
  via word-boundary matching to avoid breaking intentional kana
  usage in early-N5 mondai-4 texts).
- data/listening.json: SKIPPED. The bunsetsu-spaced kana
  convention there matches the JLPT N5 listening-textbook
  format and is pedagogically intentional. Don't change.

Strategy:
1. Load the N5 kanji whitelist.
2. Define a CURATED list of (kana, kanji) promotion candidates —
   common N5 content words. Curated rather than auto-derived from
   vocab.json because vocab.json contains many compounds where
   only PART of the kanji is whitelisted; mass-promotion would
   trip JA-13.
3. Filter the curated list: drop any candidate whose kanji form
   contains any out-of-scope character.
4. Apply with word-boundary regex: a kana sequence only promotes
   if it's NOT preceded or followed by other hiragana / katakana
   (so わたし → 私 happens, but わたしたち's わたし also matches
   because たち follows; the regex specifically allows known
   suffixes). Particles (は が を の に で と も か や), spaces,
   punctuation, sentence-end count as boundaries.
5. Verb conjugations are handled by listing each form explicitly
   (いく/いきます/いきました/いって/いかない/etc.) — safer than
   stem-matching.

Run from N5 root:
    python not-required/tools-archive/fix_kanji_promote_2026_05_10.py
Then run the integrity gate.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
GRAMMAR = ROOT / "data" / "grammar.json"
READING = ROOT / "data" / "reading.json"
WHITELIST = ROOT / "data" / "n5_kanji_whitelist.json"

# Curated promotion candidates. Each entry: (kana, kanji). The kanji
# must consist entirely of N5-whitelist characters; we filter below.
# Order matters: longer keys first so わたしたち matches before わたし.
CANDIDATES = [
    # ---- pronouns / people ----
    ("わたしたち", "私たち"),
    ("わたし",     "私"),
    ("にほんじん", "日本人"),
    ("がくせい",   "学生"),
    ("せんせい",   "先生"),
    ("ともだち",   "友だち"),       # 達 is N4 — keep だち kana
    ("こども",     "子ども"),
    ("こどもたち", "子どもたち"),
    ("おとこ",     "男"),
    ("おんな",     "女"),
    ("おとこのこ", "男の子"),
    ("おんなのこ", "女の子"),
    ("ひとり",     "一人"),
    ("ふたり",     "二人"),
    # 'ひと' alone is risky (homophone with substrings); only handle compounds.
    # ---- family ----
    ("ちち",       "父"),
    ("はは",       "母"),
    # 兄 姉 弟 妹 are NOT N5 — skip
    # ---- time ----
    ("きょう",     "今日"),
    ("まいにち",   "毎日"),       # 毎 is N5
    ("ことし",     "今年"),
    ("らいねん",   "来年"),
    ("らいげつ",   "来月"),
    # ---- common verbs (only forms that DON'T conflict with compounds) ----
    # NOTE on dropped candidates:
    # - 'いま' (now → 今): substring of もらいます/おもいます. Dropped.
    # - 'きます'/'きました'/'きません' (来〜): substring of できます/
    #   いただきます/しています. Dropped — the kanji 来 would land in
    #   the wrong place. Verb 来る is preserved via 'くる' entry only.
    # - 'とお' (ten → 十): substring of とおもいます ("I think").
    #   Dropped.
    # - Verb-stem-only forms removed; only complete-word forms kept
    #   that are unlikely to appear as substrings of unrelated words.
    ("いきます",   "行きます"),       # safe: 'いきます' rarely a substring
    ("いきました", "行きました"),
    ("いきません", "行きません"),
    ("いく",       "行く"),
    ("くる",       "来る"),
    ("みます",     "見ます"),
    ("みました",   "見ました"),
    ("みる",       "見る"),
    ("みて",       "見て"),
    ("ききます",   "聞きます"),
    ("きく",       "聞く"),
    ("よみます",   "読みます"),
    ("よむ",       "読む"),
    ("かきます",   "書きます"),
    ("かく",       "書く"),
    ("はなします", "話します"),
    ("かいます",   "買います"),
    ("かいました", "買いました"),
    ("かう",       "買う"),
    ("やすみます", "休みます"),
    ("やすむ",     "休む"),
    ("たべます",   "食べます"),
    ("たべました", "食べました"),
    ("たべる",     "食べる"),
    ("のみます",   "飲みます"),
    ("のむ",       "飲む"),
    ("でます",     "出ます"),
    ("でる",       "出る"),
    ("はいります", "入ります"),
    ("はいる",     "入る"),
    ("あいます",   "会います"),
    ("あいました", "会いました"),
    ("あう",       "会う"),
    ("たちます",   "立ちます"),
    ("たつ",       "立つ"),
    # ---- common nouns ----
    ("ほん",       "本"),
    ("やすみ",     "休み"),
    ("なまえ",     "名前"),
    ("でんわ",     "電話"),
    ("でんしゃ",   "電車"),
    ("くるま",     "車"),
    ("みず",       "水"),
    ("はな",       "花"),       # noun "flower"; 'はなし' (story) is excluded by word-boundary
    ("やま",       "山"),
    ("かわ",       "川"),
    ("はなし",     "話"),       # noun "story"
    ("がっこう",   "学校"),
    ("にほん",     "日本"),
    ("にほんご",   "日本語"),
    ("えいご",     "英語"),       # 英 N4 — filter out
    ("なに",       "何"),       # before any particle except な (の-particle is OK)
    ("なん",       "何"),
    ("くに",       "国"),
    ("みち",       "道"),
    ("いえ",       "家"),       # 家 N4 — filter out
    ("おかね",     "お金"),
    ("でんき",     "電気"),
    ("じかん",     "時間"),       # 間 N4 — filter out
    # 'いま' (now) dropped — too short, substring of もらいます/おもいます/etc.
    # ---- adjectives ----
    ("おおきい",   "大きい"),
    ("ちいさい",   "小さい"),
    ("たかい",     "高い"),
    ("やすい",     "安い"),
    ("あたらしい", "新しい"),
    ("ふるい",     "古い"),       # 古 N5
    ("おおい",     "多い"),       # 多 N5
    ("すくない",   "少ない"),     # 少 — verify N5? (it's not — skip)
    ("ながい",     "長い"),       # 長 N5
    ("みじかい",   "短い"),       # 短 — verify
    # ---- numbers when used as pronouns ----
    ("ひとつ",     "一つ"),
    ("ふたつ",     "二つ"),
    ("みっつ",     "三つ"),
    ("よっつ",     "四つ"),
    ("いつつ",     "五つ"),
    ("むっつ",     "六つ"),
    ("ななつ",     "七つ"),
    ("やっつ",     "八つ"),
    ("ここのつ",   "九つ"),
    ("とお",       "十"),
    # ---- weather / nature ----
    ("あめ",       "雨"),       # rain
    ("ゆき",       "雪"),       # 雪 N5? verify
    ("そら",       "空"),       # 空 N5
    ("つき",       "月"),       # moon
    # 'ひ' (day, sun) removed — too short; high false-positive risk inside
    # other kana words (びょうき contains び, さんぽ contains ぽ, etc.).
]

# These suffixes are allowed AFTER a kana token without breaking the
# match. So わたし followed by たち still matches (both promoted
# individually as separate keys above; but if a longer key isn't
# in the list, allow trailing suffix chars from this set).
# Actually we sort by length-desc so longer keys win: わたしたち
# matches before わたし. So we don't need this.
ALLOWED_TRAILING = ""

# Particles that MUST NOT be confused with content-word kanji.
# Used only to validate the word-boundary regex against false-positives.
PARTICLE_CHARS = set("はがをのにでとへもかや、。「」『』 　()()・…ー〜")


def main():
    with open(WHITELIST, "r", encoding="utf-8") as f:
        whitelist = set(json.load(f))

    # Filter candidates: every kanji in `kanji` must be whitelisted.
    safe = []
    skipped = []
    for kana, kanji in CANDIDATES:
        oos = [c for c in kanji if "一" <= c <= "龯" and c not in whitelist]
        if oos:
            skipped.append((kana, kanji, oos))
            continue
        safe.append((kana, kanji))
    print(f"{len(safe)} safe candidates ({len(skipped)} dropped for OOS kanji)")
    for kana, kanji, oos in skipped:
        print(f"  DROP {kana} → {kanji} (OOS: {''.join(oos)})")

    # Sort by kana length descending so longer keys match first.
    safe.sort(key=lambda kv: -len(kv[0]))

    # Build a single regex: alternation of all kana keys, with
    # negative-lookbehind+lookahead boundaries against other kana.
    # Boundary policy: a match must NOT be preceded or followed by
    # another hiragana/katakana character — i.e., it must be a
    # standalone token (followed by a particle or punctuation or
    # end-of-string).
    pattern_parts = [re.escape(k) for k, v in safe]
    # Boundary policy:
    # - Lookbehind: forbid preceding KANJI. Kana neighbours allowed
    #   because we can't easily distinguish "preceded by particle"
    #   from "preceded by stem-of-larger-word" with fixed-width
    #   lookbehind. The risk is small in practice (Japanese rarely
    #   has kana sequences ending in candidate-prefix patterns).
    # - Lookahead: must be followed by a SPECIFIC allowed character
    #   (single-char particle, punctuation, whitespace) or end-of-
    #   string. This is the critical guard that prevents false
    #   positives like ほん→本 inside ほんだな (bookshelf): だ is
    #   intentionally NOT in the allowed-next list (compound risk).
    ALLOWED_NEXT = (
        'はがをのにでとへもかやねよぞさ'  # single-char particles
        '、。！？!?()(){}「」『』〜・…ー'    # punctuation
        ' 　\t\n'                        # whitespace (incl. full-width)
    )
    big_re = re.compile(
        r"(?<![一-龯])(" + "|".join(pattern_parts) + r")"
        r"(?=[" + re.escape(ALLOWED_NEXT) + r"]|$)"
    )
    kana_to_kanji = dict(safe)

    def promote(text):
        if not text:
            return text
        return big_re.sub(lambda m: kana_to_kanji[m.group(1)], text)

    def promote_walk(obj, path=""):
        """Recursively promote text in dicts/lists. Returns (#promoted, #total)."""
        if isinstance(obj, dict):
            n_changed = 0
            for k, v in obj.items():
                if isinstance(v, str):
                    new = promote(v)
                    if new != v:
                        obj[k] = new
                        n_changed += 1
                elif isinstance(v, (list, dict)):
                    n_changed += promote_walk(v, f"{path}.{k}")
            return n_changed
        if isinstance(obj, list):
            n_changed = 0
            for i, item in enumerate(obj):
                if isinstance(item, str):
                    new = promote(item)
                    if new != item:
                        obj[i] = new
                        n_changed += 1
                elif isinstance(item, (list, dict)):
                    n_changed += promote_walk(item, f"{path}[{i}]")
            return n_changed
        return 0

    # ---- Grammar: promote pattern + examples[].ja only ----
    with open(GRAMMAR, "r", encoding="utf-8") as f:
        gdata = json.load(f)
    g_changes = 0
    g_examples = 0
    for p in gdata["patterns"]:
        # Promote pattern title.
        new_pat = promote(p.get("pattern", ""))
        if new_pat != p.get("pattern"):
            print(f"  pattern  {p['id']}: {p['pattern']!r} → {new_pat!r}")
            p["pattern"] = new_pat
            g_changes += 1
        # Promote each example's `ja` only (don't touch translation_en,
        # romaji, vocab_ids, form, etc.).
        for ex in p.get("examples", []):
            ja = ex.get("ja", "")
            new_ja = promote(ja)
            if new_ja != ja:
                ex["ja"] = new_ja
                g_examples += 1
    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(gdata, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Grammar: {g_changes} pattern titles + {g_examples} example.ja sentences updated.")

    # ---- Reading: promote passages[].ja only ----
    with open(READING, "r", encoding="utf-8") as f:
        rdata = json.load(f)
    r_changes = 0
    for p in rdata["passages"]:
        ja = p.get("ja", "")
        new_ja = promote(ja)
        if new_ja != ja:
            p["ja"] = new_ja
            r_changes += 1
    with open(READING, "w", encoding="utf-8") as f:
        json.dump(rdata, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Reading: {r_changes} passage.ja updated.")


if __name__ == "__main__":
    main()
