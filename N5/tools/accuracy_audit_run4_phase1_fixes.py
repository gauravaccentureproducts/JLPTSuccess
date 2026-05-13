"""Accuracy-audit run-4 Phase-1 follow-up fixes.

Phase-0 was all-clean post-n5-166 fix. Phase-1 random sampling +
content-listing semantic check surfaced these additional findings
not covered by any CI invariant:

F-3 CRITICAL: n5-058 Verb-ます meaning_ja contains terminology error
   "ていねいな ふつうけい" (polite plain-form) — internally contradictory.
   ふつうけい = 普通形 = plain form. Verb-ます IS the polite form, not
   plain. Other patterns use ふつうけい correctly (n5-135, n5-162 for
   relative clauses + before-clauses); only n5-058 has the contradiction.

F-4 CRITICAL: n5-098 '〜の中で〜が いちばん' (superlative) — body swap.
   Pattern field is superlative ("Among X, Y is the most...") but ALL
   meaning fields, 5 of 6 examples, and all common_mistakes are about
   すき/きらい (like/dislike). That's pattern n5-099's content leaked in.
   ex[5] is also a literal duplicate of ex[4].

F-5 MAJOR: n5-175 '〜ないといけない' — meaning_ja is just '「〜なくては
   いけない」' (an alternative form), not an explanation.

F-6 MAJOR: n5-014/n5-043/n5-078 meaning_ja too thin to convey the
   pedagogical point (proximity system / direct attachment rule).

F-7 MINOR: n5-161/n5-184 cultural_callout is a pointer ("See n5-119")
   rather than inline content.

All fixes preserve provenance tags and re-derive _meaning_ja_markers
where applicable.
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
GRAMMAR_BAK = "data/grammar.json.bak_2026_05_13_phase1_fixes"

# Backup
shutil.copy2(GRAMMAR, GRAMMAR_BAK)
print(f"Backed up grammar.json to {GRAMMAR_BAK}")

g = json.load(open(GRAMMAR, encoding="utf-8"))

# Build id index
by_id = {p["id"]: p for p in g["patterns"]}

# -------------------------------------------------------------------
# F-3: n5-058 Verb-ます meaning_ja terminology fix
# -------------------------------------------------------------------
p = by_id["n5-058"]
print(f"\n[F-3] n5-058 Verb-ます")
print(f"  OLD meaning_ja: {p['meaning_ja']!r}")
p["meaning_ja"] = (
    "ていねいな いいかた。"
    "「Verb-ます」で げんざい・みらいの ことを ていねいに いいます。"
    "「ごはんを たべます」「学校に いきます」。"
)
print(f"  NEW meaning_ja: {p['meaning_ja']!r}")
p["_meaning_ja_markers"] = [
    "ていねいな いいかた",
    "ていねい",
    "Verb-ます",
    "げんざい",
    "みらい",
    "たべます",
    "いきます",
]
p["meaning_ja_provenance"] = "phase1_terminology_fix_2026_05_13_run4"

# -------------------------------------------------------------------
# F-4: n5-098 superlative pattern body rewrite
# -------------------------------------------------------------------
p = by_id["n5-098"]
print(f"\n[F-4] n5-098 〜の中で〜が いちばん (superlative)")
print(f"  OLD meaning_en: {p['meaning_en']!r}")
p["meaning_en"] = (
    "Among X (group), Y is the most [adj] — N5 superlative pattern. "
    "Uses が-particle on the superlative item; 'いちばん' (number one) "
    "before the adjective."
)
print(f"  NEW meaning_en: {p['meaning_en']!r}")

print(f"  OLD meaning_ja: {p['meaning_ja']!r}")
p["meaning_ja"] = (
    "「〜の中で〜が いちばん [けいようし]」で、"
    "グループ(なかま)の 中で 何が いちばん [けいようし]か を いいます。"
    "「くだものの 中で りんごが いちばん すきです」"
    "「クラスの 中で たなかさんが いちばん せが たかいです」。"
)
print(f"  NEW meaning_ja: {p['meaning_ja']!r}")

print(f"  OLD meaning_hi: {p.get('meaning_hi','')[:60]!r}")
p["meaning_hi"] = (
    "उच्चतम तुलना: '〜の中で〜が いちばん [विशेषण]' = "
    "'X (समूह) में Y सबसे [विशेषण] है'। "
    "जैसे: 'फलों में सेब सबसे पसंदीदा है'।"
)
print(f"  NEW meaning_hi: {p['meaning_hi'][:60]!r}")

# Replace examples with proper superlative examples
new_examples = []
# Preserve existing example structure (keep first audio metadata)
old_ex0_keys = set(p["examples"][0].keys()) if p.get("examples") else set()
def make_ex(ja, vocab_ids):
    base = {"ja": ja, "en": "", "vocab_ids": vocab_ids}
    # preserve form field if other examples have it
    return base

new_examples.append({
    "ja": "くだものの 中で りんごが いちばん すきです。",
    "en": "Among fruits, I like apples the best.",
    "vocab_ids": [
        "n5.vocab.17-food-items.くだもの",
        "n5.vocab.17-food-items.りんご",
        "n5.vocab.32-adjectives.すき",
    ],
})
new_examples.append({
    "ja": "クラスの 中で たなかさんが いちばん せが たかいです。",
    "en": "In the class, Tanaka is the tallest.",
    "vocab_ids": [
        "n5.vocab.37-common-nouns-miscella.クラス",
        "n5.vocab.31-adjectives.高い",
    ],
})
new_examples.append({
    "ja": "日本の 中で ふじさんが いちばん たかい 山です。",
    "en": "In Japan, Mt. Fuji is the tallest mountain.",
    "vocab_ids": [
        "n5.vocab.25-languages-and-countri.日本",
        "n5.vocab.14-nature-and-weather.山",
        "n5.vocab.31-adjectives.高い",
    ],
})
new_examples.append({
    "ja": "スポーツの 中で サッカーが いちばん おもしろいです。",
    "en": "Among sports, soccer is the most interesting.",
    "vocab_ids": [
        "n5.vocab.37-common-nouns-miscella.スポーツ",
        "n5.vocab.31-adjectives.おもしろい",
    ],
})
new_examples.append({
    "ja": "1ねんの 中で はるが いちばん いい きせつです。",
    "en": "In a year, spring is the best season.",
    "vocab_ids": [
        "n5.vocab.11-time-days-weeks-month.年",
        "n5.vocab.14-nature-and-weather.はる",
    ],
})
new_examples.append({
    "ja": "かぞくの 中で おとうとが いちばん せが ひくいです。",
    "en": "In my family, my younger brother is the shortest.",
    "vocab_ids": [
        "n5.vocab.2-people-family.かぞく",
        "n5.vocab.2-people-family.おとうと",
        "n5.vocab.31-adjectives.ひくい",
    ],
})
# Preserve more example slots up to old length so form-consistency is kept
# Match original length of 6 examples
print(f"  OLD examples count: {len(p['examples'])}")
# Carry over any other keys from existing ex[0] (form, audio, etc.) to new ones
template_keys = {k: p['examples'][0].get(k) for k in p['examples'][0].keys()
                 if k not in ('ja', 'en', 'vocab_ids')}
for i, ex in enumerate(new_examples):
    for k, v in template_keys.items():
        if k not in ex:
            ex[k] = v
# But strip audio refs since those would point to old example files
for ex in new_examples:
    if "audio" in ex:
        del ex["audio"]
p["examples"] = new_examples
print(f"  NEW examples count: {len(p['examples'])}")

# Replace common_mistakes with superlative-specific ones
old_cm = p.get("common_mistakes") or []
old_cm_keys = set(old_cm[0].keys()) if old_cm else set()
new_cm = []
def make_cm(wrong, right, why):
    base = {"wrong": wrong, "right": right, "why": why}
    return base
new_cm.append(make_cm(
    wrong="くだものの 中で りんごは いちばん すきです。",
    right="くだものの 中で りんごが いちばん すきです。",
    why="いちばん の しゅご には「が」を つかいます。「は」では ありません。",
))
new_cm.append(make_cm(
    wrong="クラスの 中に たなかさんが いちばん せが たかいです。",
    right="クラスの 中で たなかさんが いちばん せが たかいです。",
    why="グループ(なかま)を しめす ときは「〜の 中で」。「〜の 中に」(ばしょ) では ありません。",
))
new_cm.append(make_cm(
    wrong="りんごが くだものの 中で いちばん すきです。",
    right="くだものの 中で りんごが いちばん すきです。",
    why="「〜の 中で」(グループ)を 先に いう ほうが ふつうです。",
))
p["common_mistakes"] = new_cm

# Update markers
p["_meaning_ja_markers"] = [
    "〜の中で",
    "〜の 中で",
    "いちばん",
    "けいようし",
    "グループ",
    "なかま",
    "くだものの",
    "りんごが",
    "せが たかい",
    "たなかさん",
]
p["meaning_ja_provenance"] = "phase1_body_swap_fix_2026_05_13_run4"
print(f"  Markers re-derived: {len(p['_meaning_ja_markers'])} tokens")

# -------------------------------------------------------------------
# F-5: n5-175 〜ないといけない expand meaning_ja
# -------------------------------------------------------------------
p = by_id["n5-175"]
print(f"\n[F-5] n5-175 〜ないといけない")
print(f"  OLD meaning_ja: {p['meaning_ja']!r}")
p["meaning_ja"] = (
    "「〜ないと いけない」は ぎむを いいます。"
    "「〜なくては いけない」の カジュアルな かたちです。"
    "「もう ねないと いけない」「べんきょうを しないと いけない」。"
)
print(f"  NEW meaning_ja: {p['meaning_ja']!r}")
p["_meaning_ja_markers"] = [
    "〜ないと いけない",
    "ぎむ",
    "なくては いけない",
    "カジュアル",
    "ねないと いけない",
    "べんきょう",
]
p["meaning_ja_provenance"] = "phase1_thin_expand_2026_05_13_run4"

# -------------------------------------------------------------------
# F-6: n5-014/n5-043/n5-078 meaning_ja expansion
# -------------------------------------------------------------------
p = by_id["n5-014"]
print(f"\n[F-6a] n5-014 これ／それ／あれ／どれ")
print(f"  OLD meaning_ja: {p['meaning_ja']!r}")
p["meaning_ja"] = (
    "「これ・それ・あれ・どれ」は もの や こと を しめす ことばです。"
    "「これ」(はなす人の ちかく)、"
    "「それ」(きく人の ちかく)、"
    "「あれ」(どちらも とおい)、"
    "「どれ」(しつもん)。"
)
print(f"  NEW meaning_ja: {p['meaning_ja']!r}")
p["_meaning_ja_markers"] = [
    "「これ・それ・あれ・どれ」",
    "もの や こと",
    "はなす人",
    "きく人",
    "ちかく",
    "とおい",
    "しつもん",
]
p["meaning_ja_provenance"] = "phase1_thin_expand_2026_05_13_run4"

p = by_id["n5-043"]
print(f"\n[F-6b] n5-043 こんな / そんな / あんな / どんな + Noun")
print(f"  OLD meaning_ja: {p['meaning_ja']!r}")
p["meaning_ja"] = (
    "「こんな・そんな・あんな・どんな + めいし」で"
    " めいしの しゅるいや ようすを しめします。"
    "「こんな本」(この ような 本)、"
    "「どんな たべものが すきですか」(しつもん)。"
)
print(f"  NEW meaning_ja: {p['meaning_ja']!r}")
p["_meaning_ja_markers"] = [
    "こんな",
    "そんな",
    "あんな",
    "どんな",
    "めいし",
    "しゅるい",
    "ようす",
    "この ような",
    "しつもん",
    "たべもの",
]
p["meaning_ja_provenance"] = "phase1_thin_expand_2026_05_13_run4"

p = by_id["n5-078"]
print(f"\n[F-6c] n5-078 い-Adjective + Noun")
print(f"  OLD meaning_ja: {p['meaning_ja']!r}")
p["meaning_ja"] = (
    "「い-けいようし + めいし」で めいしを しゅうしょくします。"
    "「い-けいようし」は そのまま めいしに つけます("
    "「な」は いりません)。"
    "「たかい 山」「あつい 日」「あたらしい 本」。"
)
print(f"  NEW meaning_ja: {p['meaning_ja']!r}")
p["_meaning_ja_markers"] = [
    "い-けいようし",
    "めいし",
    "しゅうしょく",
    "そのまま",
    "「な」は いりません",
    "たかい 山",
    "あつい 日",
    "あたらしい 本",
]
p["meaning_ja_provenance"] = "phase1_thin_expand_2026_05_13_run4"

# -------------------------------------------------------------------
# F-7: n5-161/n5-184 cultural_callout inline (was pointer-only)
# -------------------------------------------------------------------
p = by_id["n5-161"]
print(f"\n[F-7a] n5-161 cultural_callout")
old_cc = p.get("cultural_callout")
print(f"  OLD: {str(old_cc)[:120]}")
if isinstance(old_cc, dict):
    p["cultural_callout"]["note"] = (
        "Noun + の + まえに — combine a noun with まえに to mean "
        "'before [noun]'. The の linker is mandatory: '食事のまえに' "
        "(before the meal), 'しゅっぱつのまえに' (before departure). "
        "Differs from verb + まえに (which uses dictionary form, no の: "
        "'食べるまえに'). See n5-119 for the broader 〜まえ pattern."
    )
else:
    p["cultural_callout"] = {
        "note": (
            "Noun + の + まえに — combine a noun with まえに to mean "
            "'before [noun]'. The の linker is mandatory."
        )
    }
print(f"  NEW: {str(p['cultural_callout'])[:120]}")

p = by_id["n5-184"]
print(f"\n[F-7b] n5-184 cultural_callout")
old_cc = p.get("cultural_callout")
print(f"  OLD: {str(old_cc)[:120]}")
if isinstance(old_cc, dict):
    p["cultural_callout"]["note"] = (
        "なにか / なにも — question-word + か/も compounds for "
        "'something' vs 'nothing'. なにか (something — affirmative "
        "sentences: '何か 食べますか' = 'will you eat something?'), "
        "なにも (nothing — REQUIRES negative verb: '何も 食べません' "
        "= 'I will not eat anything'). Mismatching the affirmative/"
        "negative polarity is the most common N5 error. See n5-183 "
        "for the full Question-word + か/も system."
    )
else:
    p["cultural_callout"] = {
        "note": (
            "なにか (something) takes affirmative verb; なにも (nothing) "
            "REQUIRES negative verb. Mismatching polarity is the most "
            "common N5 error."
        )
    }
print(f"  NEW: {str(p['cultural_callout'])[:120]}")

# Write back
with open(GRAMMAR, "w", encoding="utf-8") as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"\nWritten {GRAMMAR} — Phase-1 fixes applied")
print("Backup: " + GRAMMAR_BAK)
