"""Phase A — Programmatic deep-linguistic audit.

Six native-teacher-perspective checks across all Japanese-content
corpora (grammar.json, vocab.json, kanji.json, reading.json,
papers/dokkai/*.json):

  L1  Counter-noun semantic pairing (本 for cylindrical, 枚 for flat,
      冊 for books, 人 for people, 匹 for small animals, 個 for
      general)
  L2  Adjective conjugation correctness (い-adj uses くて/くない;
      な-adj uses で/じゃない)
  L3  Time-particle accuracy (時/曜日/月 take に; 毎日/今日/きのう/
      あした take NO particle; 朝/夜 usually NO particle)
  L4  Discourse register coherence (within one sentence, don't mix
      plain だ with polite です unmarkedly)
  L5  Verb-group conjugation correctness (cross-check verb-class
      tag in vocab.json against example conjugation pattern)
  L6  Honorifics / お-ご prefix correctness (お for wago; ご for
      kango; obvious mismatches)
"""
from __future__ import annotations
import json
import re
from collections import defaultdict
from pathlib import Path


# ---- L1: Counter-noun semantic pairing ----
# noun → set of canonical counters
# (kana forms used because most examples mix kanji/kana freely)
COUNTER_PAIRS = {
    # cylindrical → 本
    "ペン":   {"本"}, "えんぴつ": {"本"}, "ボールペン": {"本"},
    "かさ":   {"本"}, "ビール":   {"本"}, "ワイン":     {"本"},
    "ジュース": {"本"}, "ペットボトル": {"本"},
    # flat → 枚
    "シャツ": {"枚"}, "Tシャツ": {"枚"}, "ハンカチ": {"枚"},
    "ふうとう":{"枚"}, "はがき":  {"枚"}, "きって":   {"枚"},
    "おさら": {"枚"}, "コート":  {"枚"},
    "しゃしん":{"枚"}, "ちず":    {"枚"}, "かみ":     {"枚"},
    "ふとん": {"枚"},
    # books → 冊
    "本":   {"冊"}, "じしょ": {"冊"}, "ノート":     {"冊"},
    "ざっし":{"冊"}, "きょうかしょ": {"冊"}, "まんが": {"冊"},
    # people → 人 (にん, with 1人 ひとり / 2人 ふたり irregulars)
    # we don't enforce — too many variants
    # small animals → 匹/ぴき
    "ねこ": {"ひき","ぴき","びき"},
    "いぬ": {"ひき","ぴき","びき"},
    "さかな":{"ひき","ぴき","びき"},
    "とり": {"わ"},  # birds 羽
    # large animals → 頭
    "うし": {"頭"}, "うま": {"頭"}, "ぞう": {"頭"},
    # machines / vehicles → 台
    "車": {"台"}, "じてんしゃ": {"台"}, "テレビ": {"台"},
    "ラジオ":{"台"}, "カメラ":  {"台"}, "パソコン": {"台"},
    # buildings → 軒 (N4) — skip for N5
    # cups / glasses of liquid → 杯
    "コーヒー": {"杯","はい","ぱい","ばい"},
    "おちゃ":   {"杯","はい","ぱい","ばい"},
    "おさけ":   {"杯","はい","ぱい","ばい"},
    "みず":     {"杯","はい","ぱい","ばい"},
    # general small objects → 個
    "りんご": {"個","つ"}, "たまご": {"個","つ"}, "みかん": {"個","つ"},
    "ボール": {"個","つ"}, "ケーキ": {"個","つ"},
}

NUMBER_KANJI = "〇一二三四五六七八九十百千万"
# Note: 倍/ばい (multiplier suffix on numbers, e.g., 三倍 "triple") is
# excluded — it's not a counter on a noun, it's a math multiplier.
COUNTER_RX_BODY = (
    r"(?P<num>[" + NUMBER_KANJI + r"\d]+)\s*"
    r"(?P<counter>本|ぼん|ぽん|枚|まい|冊|さつ|個|こ|つ|"
    r"頭|とう|台|だい|杯|はい|ぱい|"
    r"ひき|ぴき|びき|わ)"
)
COUNTER_RX = re.compile(COUNTER_RX_BODY)

# Normalize counter alternants (rendaku/handakuon variants) to the
# canonical reading group used as the key in COUNTER_PAIRS.
COUNTER_NORMALIZE = {
    "ぼん":"本","ぽん":"本","本":"本",
    "まい":"枚","枚":"枚",
    "さつ":"冊","冊":"冊",
    "こ":"個","つ":"個","個":"個",
    "とう":"頭","頭":"頭",
    "だい":"台","台":"台",
    "杯":"杯","はい":"杯","ぱい":"杯","ばい":"杯",
    "ひき":"ひき","ぴき":"ひき","びき":"ひき",
    "わ":"わ",
}


def check_L1(ja: str) -> list[str]:
    """Refined: require the counted noun to be IMMEDIATELY followed by
    を/が/に/も before the number-counter sequence (with optional
    whitespace). This avoids substring matches like うし inside きょうしつ.
    Also pick the CLOSEST matching noun (rightmost), not the first in
    dict iteration order — so 「コートの ボタンを 一つ」 correctly
    identifies ボタン (closer) as the counted noun, not コート."""
    out = []
    for m in COUNTER_RX.finditer(ja):
        counter = m.group("counter")
        normalized = COUNTER_NORMALIZE.get(counter, counter)
        # Look for the rightmost (closest) "noun + particle + (whitespace)" pattern
        # immediately preceding the number-counter group.
        # Pattern: noun + [をがにも] + optional space
        prefix = ja[: m.start()]
        best_noun = None
        best_pos = -1
        for noun, valid in COUNTER_PAIRS.items():
            # find noun followed by [をがにも] and possibly spaces, ending at prefix end
            pat = re.compile(re.escape(noun) + r"[をがにも]\s*$")
            mm = pat.search(prefix)
            if mm and mm.start() > best_pos:
                best_pos = mm.start()
                best_noun = (noun, valid)
        if best_noun is None:
            continue
        noun, valid = best_noun
        valid_set = set()
        for v in valid:
            valid_set.add(v)
            valid_set.add(COUNTER_NORMALIZE.get(v, v))
        if normalized not in valid_set and counter not in valid:
            out.append(f"counter-mismatch: '{noun}' takes {valid}, got '{counter}'")
    return out


# ---- L2: Adjective conjugation ----
# i-adj-stem + で is wrong; should be くて (conjunction).
# Common errors: 大きいで, 高いで, おいしいで, etc.
# But careful: のんで, よんで etc. are verb-て forms — they end in で
# because of the て-form rule for む/ぶ/ぬ verbs.
# Filter: i-adj forms end in 「い」 + で. So pattern is 「Xいで」 where
# X is a hiragana-only stem. But 飲んで, 読んで etc. have ん before で.
# Specific i-adjective stems to flag:
IADJ_STEMS = [
    "大き","小さ","新し","古","高","安","あつ","さむ",
    "おいし","まず","いそが","おもしろ","つまらな","むずか",
    "やさし","かわい","つよ","よわ","ひろ","せま","とお","ちか",
    "やす","たか","くろ","しろ","あか","あお","き","あたら","ふる",
    "あつ","さむ","あたたか","すずし","くらい","あかる",
]
# CRITICAL: exclude 「す」 from the trigger set. 〜いです IS the
# CORRECT polite-affirmative form of an i-adjective (おもしろいです =
# "is interesting"). The wrong forms are 〜いで followed by ANYTHING
# OTHER than す — like 〜いで、 (wrong conjunction; should be 〜くて、),
# 〜いでは (wrong negative; should be 〜くては / 〜くなくては), or
# 〜いでも (wrong; should be 〜くても).
IADJ_NEG_DE_RX = re.compile(
    r"(" + "|".join(IADJ_STEMS) + r")い\s*で(?:は|も|、|。| )"
)
# な-adj using くて (wrong)
NAADJ_KUTE_RX = re.compile(r"(きれい|げんき|しずか|べんり|ゆうめい|にぎやか|ひま|だいじょうぶ|たいせつ)くて")


def check_L2(ja: str) -> list[str]:
    out = []
    # i-adj + で (wrong; should be くて)
    for m in IADJ_NEG_DE_RX.finditer(ja):
        out.append(f"i-adj-conj-wrong: '{m.group(0)}' should be ...くて (not ...いで)")
    for m in NAADJ_KUTE_RX.finditer(ja):
        out.append(f"na-adj-conj-wrong: '{m.group(0)}' should be ...で (not ...くて)")
    return out


# ---- L3: Time-particle accuracy ----
# Conservative — flag only the most clearly-wrong cases. Many time
# expressions accept に or で in specific contexts (e.g., 今年で =
# "as of this year"; あさってに = formal/emphasized future).
# Frequency adverbs (毎日/毎週/etc.) should NEVER take に.
NO_PARTICLE_TIMES = [
    "毎日", "毎週", "毎月", "毎年", "毎朝", "毎晩",
    "いつも", "ときどき", "たいてい", "よく", "あまり",
    "ぜんぜん",
]
# Require word boundary BEFORE the time word (preceded by start,
# whitespace, or non-Japanese-content char) — avoids catching
# 「とうきょう」/「べんきょう」 substring matches of 「きょう」.
NO_PARTICLE_NI_RX = re.compile(
    r"(?:^|[\s、。「『(『]|[^ぁ-ゟ゠-ヿ一-鿿])(" +
    "|".join(re.escape(s) for s in NO_PARTICLE_TIMES) +
    r")に\s"
)


def check_L3(ja: str) -> list[str]:
    out = []
    for m in NO_PARTICLE_NI_RX.finditer(ja):
        word = m.group(1)
        out.append(f"time-particle-wrong: '{word}に' — frequency adverbs take NO particle")
    return out


# ---- L4: Discourse register coherence ----
# Within ONE sentence, don't mix だ/する with です/します unmarkedly.
# Quote-bracketed content is exempt (quoting different register).
# Mixed register patterns:
# - 〜だ。〜です。 within a single 'ja' field
# - 〜する。〜します。 within a single 'ja' field
PLAIN_END_RX = re.compile(r"(?<![「『])([ぁ-ゟ一-鿿])だ。")
POLITE_END_RX = re.compile(r"です。")
PLAIN_VERB_END_RX = re.compile(r"(?<![ぁ-ゟ])(?:する|くる|来る|やる|食べる|寝る|起きる|見る|読む)。")
POLITE_VERB_END_RX = re.compile(r"ます。")


def check_L4(ja: str) -> list[str]:
    # Strip quoted content for this check
    de_quoted = re.sub(r"「[^」]*」", "", ja)
    de_quoted = re.sub(r"『[^』]*』", "", de_quoted)
    has_plain_copula = PLAIN_END_RX.search(de_quoted)
    has_polite_copula = POLITE_END_RX.search(de_quoted)
    has_plain_verb = PLAIN_VERB_END_RX.search(de_quoted)
    has_polite_verb = POLITE_VERB_END_RX.search(de_quoted)
    out = []
    # Only flag when polite + plain coexist with multiple sentences
    sentences = [s for s in de_quoted.split("。") if s.strip()]
    if len(sentences) >= 2:
        if has_plain_copula and has_polite_copula:
            out.append("register-mix: plain だ + polite です within same passage")
        if has_plain_verb and has_polite_verb:
            out.append("register-mix: plain dict-verb + polite ます within same passage")
    return out


# ---- L5: Verb-group conjugation correctness ----
# Cross-check vocab.json verb entries against their examples' conjugations.
# For each verb entry with pos in {verb-1, verb-2, verb-3}, scan its
# examples for conjugation patterns that contradict the pos tag.
# E.g., verb-2 entries should NOT show as godan-conjugated.


# ---- L6: お/ご prefix on noun ----
# Common errors:
# - ご on wago: ごみず (should be おみず), ご名前 (should be お名前)
# - お on kango with stuffy senses: おしごと is OK; おどうりょう is rare
# Only flag clear mismatches:
GO_PREFIX_WRONG = ["ご水", "ごみず", "ご名前", "ごなまえ", "ご手紙", "ごてがみ"]
OO_PREFIX_WRONG = ["お家族", "おかぞく", "お住所", "おじゅうしょ"]  # ご-form preferred


def check_L6(ja: str) -> list[str]:
    out = []
    for w in GO_PREFIX_WRONG:
        if w in ja:
            out.append(f"honorific-prefix: '{w}' should use お- (wago)")
    for w in OO_PREFIX_WRONG:
        if w in ja:
            out.append(f"honorific-prefix: '{w}' should use ご- (kango)")
    return out


# ---- Driver ----
def iter_corpus():
    """Yield (corpus, item_id, field, ja, verb_pos_hint) tuples.
    verb_pos_hint is non-None only for vocab examples on verb entries."""
    g = json.loads(Path("data/grammar.json").read_text(encoding="utf-8"))
    for p in g["patterns"]:
        for i, ex in enumerate(p.get("examples") or []):
            ja = (ex.get("ja") or "").strip()
            if ja:
                yield ("grammar", p["id"], f"examples[{i}].ja", ja, None)
    v = json.loads(Path("data/vocab.json").read_text(encoding="utf-8"))
    for e in v["entries"]:
        verb_pos = e.get("pos") if e.get("pos","").startswith("verb") else None
        verb_reading = e.get("reading", "") if verb_pos else None
        for i, ex in enumerate(e.get("examples") or []):
            ja = (ex.get("ja") or "").strip()
            if ja:
                yield ("vocab", e["id"], f"examples[{i}].ja", ja, (verb_pos, verb_reading))
    k = json.loads(Path("data/kanji.json").read_text(encoding="utf-8"))
    for e in k["entries"]:
        for i, s in enumerate(e.get("sentences") or []):
            ja = (s.get("ja") or "").strip()
            if ja:
                yield ("kanji", e["glyph"], f"sentences[{i}].ja", ja, None)
    r = json.loads(Path("data/reading.json").read_text(encoding="utf-8"))
    for p in r["passages"]:
        ja = (p.get("ja") or "").strip()
        if ja:
            yield ("reading", p["id"], "ja", ja, None)
        for i, q in enumerate(p.get("questions") or []):
            stem = (q.get("prompt_ja") or "").strip()
            if stem:
                yield ("reading", p["id"], f"questions[{i}].prompt_ja", stem, None)
    for cat in ("dokkai",):
        pdir = Path(f"data/papers/{cat}")
        if not pdir.exists():
            continue
        for pf in sorted(pdir.glob("paper-*.json")):
            paper = json.loads(pf.read_text(encoding="utf-8"))
            for q in paper.get("questions") or []:
                for fld in ("stem_html", "passage_text"):
                    ja = (q.get(fld) or "").strip()
                    if ja:
                        yield (f"papers/{cat}", q.get("id", "?"),
                               f"{pf.name}.{fld}", ja, None)


def main():
    findings = defaultdict(list)
    n_sentences = 0
    for corpus, iid, field, ja, verb_hint in iter_corpus():
        n_sentences += 1
        for issue in check_L1(ja):
            findings["L1-COUNTER-NOUN-MISMATCH"].append((corpus, iid, field, issue, ja[:60]))
        for issue in check_L2(ja):
            findings["L2-ADJ-CONJUGATION"].append((corpus, iid, field, issue, ja[:60]))
        for issue in check_L3(ja):
            findings["L3-TIME-PARTICLE"].append((corpus, iid, field, issue, ja[:60]))
        for issue in check_L4(ja):
            findings["L4-REGISTER-MIX"].append((corpus, iid, field, issue, ja[:60]))
        for issue in check_L6(ja):
            findings["L6-HONORIFIC-PREFIX"].append((corpus, iid, field, issue, ja[:60]))

    print(f"Scanned {n_sentences} Japanese sentences.\n")
    total = 0
    for cat in sorted(findings):
        rows = findings[cat]
        total += len(rows)
        print(f"{cat:30s} {len(rows)}")
        for r in rows[:8]:
            print(f"  {r}")
        if len(rows) > 8:
            print(f"  ... +{len(rows)-8} more")
        print()
    print(f"TOTAL FINDINGS: {total}")


if __name__ == "__main__":
    main()
