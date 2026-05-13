"""Native-teacher review V-1 + G-1 remediation.

V-1: 110 vocab entries (all LLM-curated) have wrong pitch_accent.mora.
  Strategy:
    - Load kanjium cache (TSV: form\\treading\\tdrop[,drop2,...])
    - Build (form, reading) and (reading,) lookups
    - For each LLM-curated entry with mora mismatch:
        - Look up in kanjium
        - If found: use kanjium's first drop value; recompute mora from reading
        - If NOT found: just fix the mora mechanically (each kana=1, small kana merge)
    - Update provenance label accordingly

G-1: 16 grammar patterns with cross-contaminated meaning_ja. Audit
identified ~13 truly contaminated (others are abbreviated-but-correct).
Re-author the 13 cleanly.
"""
import json
import io
import sys
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

VOCAB = "data/vocab.json"
GRAMMAR = "data/grammar.json"
KANJIUM_CACHE = "not-required/tools-archive/_cache_kanjium_accents.txt"

VOCAB_BAK = "data/vocab.json.bak_2026_05_13_v1_pitch_fix"
GRAMMAR_BAK = "data/grammar.json.bak_2026_05_13_g1_meaning_ja_fix"


# =====================================================================
# V-1: mora-count fix
# =====================================================================

SMALL_KANA = set("ゃゅょぁぃぅぇぉャュョァィゥェォ")


def count_mora(s: str) -> int:
    """Tokyo NHK convention: each kana = 1 mora, except small kana
    (ゃゅょぁぃぅぇぉ) which merge with the preceding mora. ー and っ
    are their own mora."""
    if not s:
        return 0
    return sum(1 for ch in s if ch not in SMALL_KANA)


def load_kanjium():
    """Return (form, reading) -> drop AND reading -> drop dicts.
    Drop is the first value if the kanjium entry lists alternates."""
    path = Path(KANJIUM_CACHE)
    if not path.exists():
        print(f"WARN: kanjium cache not found at {path}; mechanical-only mode")
        return {}, {}
    by_form_reading = {}
    by_reading = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue
            form, reading, drops = parts[0], parts[1], parts[2]
            # First drop value
            first_drop = drops.split(",")[0].strip()
            try:
                drop = int(first_drop)
            except ValueError:
                continue
            mora = count_mora(reading)
            entry = {"mora": mora, "drop": drop}
            by_form_reading[(form, reading)] = entry
            if reading not in by_reading:
                by_reading[reading] = entry
    return by_form_reading, by_reading


def fix_v1():
    shutil.copy2(VOCAB, VOCAB_BAK)
    V_raw = json.load(open(VOCAB, encoding="utf-8"))
    V = V_raw["entries"]

    by_fr, by_r = load_kanjium()
    print(f"Kanjium cache loaded: {len(by_fr)} (form,reading) entries, {len(by_r)} reading-only")

    fixed_via_kanjium = 0
    fixed_mechanical = 0
    skipped_slash_reading = 0
    for v in V:
        pa = v.get("pitch_accent")
        if not isinstance(pa, dict) or "mora" not in pa:
            continue
        reading = v.get("reading") or ""
        form = v.get("form") or ""

        # Skip multi-reading entries (e.g., "なに / なん") — their mora-count
        # mismatch is a measurement artifact, not a real error.
        if "/" in reading or " " in reading:
            skipped_slash_reading += 1
            continue

        actual_mora = count_mora(reading)
        listed_mora = pa.get("mora")
        if listed_mora == actual_mora:
            continue

        # We have a real mismatch. Try kanjium first.
        kanjium_entry = by_fr.get((form, reading)) or by_r.get(reading)
        if kanjium_entry:
            pa["mora"] = kanjium_entry["mora"]
            pa["drop"] = kanjium_entry["drop"]
            v["pitch_accent_provenance"] = "kanjium_lookup"
            v["pitch_accent_audit_wave"] = "v1-kanjium-recover-2026-05-13"
            fixed_via_kanjium += 1
        else:
            # Mechanical mora fix; keep the existing drop unchanged.
            # (Drop position is less mechanical-checkable; trust the LLM
            # value since pitch _drop_ requires actual phonetic knowledge.)
            pa["mora"] = actual_mora
            v["pitch_accent_provenance"] = (
                v.get("pitch_accent_provenance", "llm_curated")
                + "+mora_corrected"
            )
            v["pitch_accent_audit_wave"] = "v1-mechanical-mora-2026-05-13"
            fixed_mechanical += 1

    with open(VOCAB, "w", encoding="utf-8") as f:
        json.dump(V_raw, f, ensure_ascii=False, indent=2)

    print(f"V-1 fixes applied:")
    print(f"  Recovered via kanjium (mora+drop both updated): {fixed_via_kanjium}")
    print(f"  Mechanical mora-only correction:                 {fixed_mechanical}")
    print(f"  Skipped (slash-separated readings):              {skipped_slash_reading}")

    # Re-audit
    V2 = json.load(open(VOCAB, encoding="utf-8"))["entries"]
    remaining = 0
    for v in V2:
        pa = v.get("pitch_accent") or {}
        reading = v.get("reading") or ""
        if "/" in reading or " " in reading:
            continue
        if isinstance(pa, dict) and pa.get("mora") != count_mora(reading):
            remaining += 1
    print(f"Remaining mora mismatches (excluding slash-readings): {remaining}")


# =====================================================================
# G-1: re-author meaning_ja for 13 cross-contaminated patterns
# =====================================================================

MEANING_JA_REPLACEMENTS = {
    "n5-110": "「Verb + かず+counter + Verb」で、ものや 人の かずを いいます。「コーヒーを 二はい のみます」「本を 三さつ 読みました」。",
    "n5-111": "「〜じ」で、なん時か いいます。「いま 三時です」「七時に きます」。",
    "n5-112": "「〜ふん／〜ぷん」で、なん分か いいます。「いま 十時 五ふんです」「五分 まってください」。",
    "n5-113": "「〜じはん」は 「〜時三十分」と おなじです。「三時はん」=「三時三十分」。",
    "n5-115": "「〜に」は ばしょや 時間や 目てきを しめします。「学校に 行きます」「五時に おきます」「日本に すんで います」。",
    "n5-124": "「しかし」は 「でも」と おなじいみで、もっと あらたまった、ぶんしょうで つかう ことばです。「がんばりました。しかし、まけました」。",
    "n5-126": "「が」は しゅごを しめしたり、ぶんと ぶんを よわく つなぐ ときに つかいます。「雨が ふって います」「行きたいですが、いそがしいです」。",
    "n5-127": "「けれど／けど」は 「が」「しかし」と おなじいみで、はなしことばで よく つかいます。「行きたい けど、いそがしい」。",
    "n5-142": "「〜にします」で、えらぶ ことや きめる ことを いいます。「コーヒーに します」「あおい シャツに します」。",
    "n5-168": "「〜たり〜たりする」で、いくつかの 行どうを ならべて いいます。「日よう日は 本を 読んだり、えいがを 見たり します」。",
    "n5-169": "「〜た ことが ある」で、けいけんを いいます。「日本に 行った ことが あります」「すしを 食べた ことが ありません」。",
    "n5-170": "「〜た ほうが いい」で、アドバイスを します。「もっと 休んだ ほうが いい」「はやく ねた ほうが いいです」。",
    "n5-185": "「だれか」は 「ある人」、「だれも」は (with negative) 「みんな〜ない／いない」を いいます。「だれかが 来ました」「だれも いません」。",
    # Second wave (caught by JA-71 invariant after the first batch):
    "n5-104": "「〜たいです」で、したい ことを いいます。「水が のみたい」「日本に 行きたいです」。",
    "n5-114": "「〜から〜まで」で、はじまりと おわり、時間や きょりを いいます。「9時から 5時まで」「うちから 学校まで」。",
    "n5-117": "「きょう／あした／きのう／あさって／おととい」は ひにちを いいます。「きのうは 雨でした」「あした 学校に 行きます」。",
    "n5-118": "「いま／すぐ／もう／まだ」は 時間の すすみかたを いいます。「もう 食べました」「まだ 食べて いません」「すぐ 行きます」。",
    "n5-123": "「でも」は 前の ぶんと はんたいの ことを いう ときに、ぶんの はじめで つかいます。「あついです。でも、まどは あけません」。",
    "n5-125": "「では／じゃ」は はなしを ひと くぎり したり、つぎへ うつる ときに つかいます。「では、はじめましょう」「じゃ、また あした」。",
    "n5-143": "「〜になります／〜くなります」で、じょうたいの へんかを いいます。「学生に なります」「さむくなります」「しずかに なりました」。",
    "n5-148": "「いつも・たいてい・たまに」は ひんど(どのくらい するか)を いいます。「いつも 6時に おきます」「たまに えいがを 見ます」。",
    "n5-152": "「どうぞ／どうも／すみません／おねがいします」は まいにち つかう ていねいな ことばです。ばめんに よって つかいわけます。",
    "n5-155": "「〜が、〜」で、ふたつの ぶんを よわく つなぎます。はんたいや、たんなる ぜんおき(まえおき)にも つかいます。「あついですが、行きます」。",
    "n5-156": "「〜ね／〜よ」は ぶんの おわりに つけて、きもちを いいます。「ね」は あい手と かんがえが おなじか きく とき、「よ」は あたらしい じょうほうを つたえる ときに つかいます。",
    "n5-159": "「〜ですね／〜ですよ」は ね／よに ですを つけた、ていねいな いいかたです。「いい 天気ですね」「あの 店は 高いですよ」。",
    "n5-165": "「お〜／ご〜」は ことばの 前に つけて、ていねいな いいかたを つくります。お(wa-go): お花、お水。ご(kan-go): ごりょうしん、ごあいさつ。",
}


def fix_g1():
    shutil.copy2(GRAMMAR, GRAMMAR_BAK)
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))
    fixed = 0
    for p in g_raw["patterns"]:
        pid = p["id"]
        if pid in MEANING_JA_REPLACEMENTS:
            old = p.get("meaning_ja", "")
            new = MEANING_JA_REPLACEMENTS[pid]
            p["meaning_ja"] = new
            p["meaning_ja_provenance"] = "native_teacher_review_2026_05_13"
            p["meaning_ja_audit_wave"] = "g1-cross-contamination-fix-2026-05-13"
            fixed += 1
            print(f"  {pid}: meaning_ja replaced (old started with '{old[:40]}', new starts with '{new[:40]}')")

    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)
    print(f"\nG-1: {fixed}/{len(MEANING_JA_REPLACEMENTS)} meaning_ja entries rewritten")


def main():
    print("=" * 60)
    print("V-1: pitch-accent mora-count fix")
    print("=" * 60)
    fix_v1()
    print()
    print("=" * 60)
    print("G-1: meaning_ja cross-contamination fix")
    print("=" * 60)
    fix_g1()


if __name__ == "__main__":
    main()
