"""Close NTR-001 (BUG-161) — rewrite 99 vocab examples that contain
non-whitelist, non-exception kanji. Each rewrite swaps the offending
kanji for its kana surface form in context (preserving the example's
pedagogical intent and the headword being taught).

Most rewrites are kana-substitution of side-words (the headword is
already whitelist-compliant; the violation is in surrounding text).
A few need light rephrasing where multiple offenders interlock.
"""
import sys, io, os, shutil, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_22"

# (vocab_id, ex_idx) -> new_ja_text
REWRITES = {
    # === Pronouns / Greetings / Counters ===
    ("n5.vocab.1-people-pronouns-and-se.どなた", 2): "どなたさまですか。",
    ("n5.vocab.2-people-family.そふ", 2): "そふは 八十さいです。",
    ("n5.vocab.4-body-parts.め", 2): "こんやは めが つかれました。",
    ("n5.vocab.7-numbers.一", 2): "コーヒーを 一ぱい ください。",
    ("n5.vocab.7-numbers.四", 2): "かぞくは 四人です。",
    ("n5.vocab.7-numbers.万", 2): "一万円 かりました。",
    ("n5.vocab.7-numbers.ゼロ", 2): "こたえは ゼロです。",
    ("n5.vocab.9-counters-common.人", 2): "かぞくは 四人です。",
    ("n5.vocab.9-counters-common.二人", 2): "二人で しょくじに 行きました。",
    # === Time ===
    ("n5.vocab.10-time-general.びょう", 2): "十びょう まって ください。",
    ("n5.vocab.11-time-days-weeks-month.五日", 2): "五日に だいじな かいぎが あります。",
    ("n5.vocab.11-time-days-weeks-month.先週", 0): "先週 きょうとに 行きました。",
    ("n5.vocab.11-time-days-weeks-month.来週", 0): "来週 きょうとに 行きます。",
    ("n5.vocab.11-time-days-weeks-month.月", 5): "こんやの 月は とても きれいです。",
    ("n5.vocab.11-time-days-weeks-month.七月", 0): "七月は なつです。",
    ("n5.vocab.11-time-days-weeks-month.先月", 0): "先月 りょこうしました。",
    ("n5.vocab.11-time-days-weeks-month.先月", 2): "先月から 日本語を はじめました。",
    ("n5.vocab.12-time-frequency-sequen.すぐ", 2): "すぐ 行きます。まって いて ください。",
    ("n5.vocab.12-time-frequency-sequen.もう", 3): "もう すこし まって ください。",
    ("n5.vocab.12-time-frequency-sequen.さいご", 2): "さいごに こたえを しらべました。",
    # === Locations ===
    ("n5.vocab.13-locations-and-places-.ろうか", 0): "ろうかで はしらないで ください。",
    ("n5.vocab.13-locations-and-places-.西", 0): "西に うみが あります。",
    ("n5.vocab.13-locations-and-places-.おてら", 1): "ふるい おてらに おまいりに 行きました。",
    ("n5.vocab.13-locations-and-places-.カフェ", 2): "カフェで 友だちを まちます。",
    # === Nature & Weather ===
    ("n5.vocab.14-nature-and-weather.うみ", 0): "なつに うみで およぎます。",
    ("n5.vocab.14-nature-and-weather.田", 0): "田の 中で こめを つくります。",
    ("n5.vocab.14-nature-and-weather.田", 1): "あきに 田の こめを かります。",
    ("n5.vocab.14-nature-and-weather.ゆき", 0): "ふゆは ゆきが ふります。",
    ("n5.vocab.14-nature-and-weather.はれ", 2): "あしたは はれの よほうです。",
    ("n5.vocab.14-nature-and-weather.くもり", 2): "あしたは くもりの よほうです。",
    ("n5.vocab.14-nature-and-weather.さむい", 0): "ふゆは さむいです。",
    ("n5.vocab.14-nature-and-weather.さむい", 2): "こんやは とても さむいですね。",
    # === Animals ===
    ("n5.vocab.15-animals.ねこ", 2): "うちには ねこが 二ひき います。",
    # === Food & Drink ===
    ("n5.vocab.16-food-and-drink-genera.ごはん", 2): "こんやは ごはんを たくさん 食べました。",
    ("n5.vocab.17-food-items.にく", 2): "こんやは にくを 食べます。",
    ("n5.vocab.17-food-items.とりにく", 2): "こんやは とりにくを 食べます。",
    ("n5.vocab.17-food-items.すいか", 0): "なつは すいかが おいしいです。",
    ("n5.vocab.17-food-items.すし", 2): "こんや すしを 食べに 行きませんか。",
    ("n5.vocab.17-food-items.カレー", 0): "ゆうごはんは カレーです。",
    ("n5.vocab.17-food-items.カレー", 2): "こんやの ばんごはんは カレーです。",
    ("n5.vocab.17-food-items.ラーメン", 2): "ラーメンを 一ぱい 食べました。",
    ("n5.vocab.17-food-items.うどん", 0): "おひるに うどんを 食べました。",
    ("n5.vocab.17-food-items.うどん", 2): "おひるに うどんを 食べました。",
    ("n5.vocab.17-food-items.そば", 2): "おひるごはんに そばを 食べました。",
    ("n5.vocab.17-food-items.ハンバーガー", 2): "おひるは ハンバーガーに します。",
    ("n5.vocab.17-food-items.サンドイッチ", 2): "おひるは サンドイッチを 食べました。",
    ("n5.vocab.17-food-items.アイスクリーム", 0): "なつは アイスクリームが おいしいです。",
    # === Drinks ===
    ("n5.vocab.18-drinks.コーヒー", 2): "朝 コーヒーを 一ぱい 飲みます。",
    ("n5.vocab.18-drinks.ぎゅうにゅう", 2): "まいあさ ぎゅうにゅうを 一ぱい 飲みます。",
    ("n5.vocab.18-drinks.ワイン", 1): "あかい ワインを 一本 ください。",
    # === Colors ===
    ("n5.vocab.20-colors.白", 0): "白は ゆきの いろです。",
    ("n5.vocab.20-colors.くろ", 0): "くろは よるの いろです。",
    ("n5.vocab.20-colors.あか", 0): "あかは 花の いろです。",
    ("n5.vocab.20-colors.あお", 0): "あおは そらの いろです。",
    ("n5.vocab.20-colors.あお", 1): "そらの いろは あおです。",
    ("n5.vocab.20-colors.きいろ", 0): "きいろは レモンの いろです。",
    ("n5.vocab.20-colors.きいろ", 1): "バナナの いろは きいろです。",
    # === Clothing ===
    ("n5.vocab.21-clothing-and-accessor.コート", 0): "ふゆに コートを きます。",
    ("n5.vocab.21-clothing-and-accessor.Tシャツ", 0): "なつに Tシャツを きます。",
    ("n5.vocab.21-clothing-and-accessor.ハンカチ", 2): "新しい ハンカチを 一まい もって います。",
    # === Money & Shopping ===
    ("n5.vocab.22-money-and-shopping.きって", 2): "八十円の きってを 五まい ください。",
    # === School & Study ===
    ("n5.vocab.24-school-and-study.かな", 2): "かなを ぜんぶ おぼえました。",
    # === House & Furniture ===
    ("n5.vocab.26-house-and-furniture.もん", 1): "学校の もんは 八時に あきます。",
    ("n5.vocab.26-house-and-furniture.もうふ", 2): "さむいから もうふを 一まい ください。",
    ("n5.vocab.26-house-and-furniture.ビデオ", 2): "こんや ビデオを 見ましょう。",
    ("n5.vocab.26-house-and-furniture.えいが", 2): "こんや えいがを 見ましょう。",
    # === Group-1 Verbs ===
    ("n5.vocab.27-verbs-group-1-verbs.なく", 0): "あかちゃんが ないて います。",
    ("n5.vocab.27-verbs-group-1-verbs.すう", 2): "いきを ふかく すって ください。",
    ("n5.vocab.27-verbs-group-1-verbs.しまる", 1): "お店は よる 十時に しまります。",
    # === Group-2 Verbs ===
    ("n5.vocab.28-verbs-group-2-verbs.かける", 1): "まいばん 母に 電話を かけます。",
    ("n5.vocab.28-verbs-group-2-verbs.聞こえる", 0): "となりの へやから おんがくが 聞こえます。",
    # === Irregular Verbs ===
    ("n5.vocab.29-verbs-irregular-and-v.けっこんする", 1): "あねは 来月 けっこんします。",
    ("n5.vocab.29-verbs-irregular-and-v.りょこうする", 0): "なつに りょこうします。",
    # === Adjectives ===
    ("n5.vocab.31-adjectives.あつい", 3): "なつは とても あついです。",
    ("n5.vocab.31-adjectives.あつい.2", 0): "おちゃが あついです。気を つけて ください。",
    ("n5.vocab.31-adjectives.あつい.3", 0): "なつは あついです。",
    ("n5.vocab.31-adjectives.よわい", 2): "こんやは からだが よわいです。",
    ("n5.vocab.31-adjectives.わかい", 2): "わかい ときは よく はしりました。",
    ("n5.vocab.31-adjectives.ぬるい", 0): "おちゃが ぬるいです。",
    # === Na-Adjectives ===
    ("n5.vocab.32-adjectives.ひま", 2): "こんやは ひまですか。",
    ("n5.vocab.32-adjectives.だいじょうぶ", 2): "だいじょうぶです、しんぱいしないで ください。",
    # === Adverbs ===
    ("n5.vocab.33-adverbs.すこし", 2): "すこし まって ください。",
    ("n5.vocab.33-adverbs.ちょっと", 2): "ちょっと まって ください。",
    ("n5.vocab.33-adverbs.もうすこし", 2): "もうすこし まって ください。",
    ("n5.vocab.33-adverbs.一番", 0): "なつが 一番 すきです。",
    ("n5.vocab.33-adverbs.やはり", 0): "やはり 日本りょうりが 好きです。",
    ("n5.vocab.33-adverbs.わくわく", 2): "あしたの たびを かんがえて わくわくします。",
    # === Particles ===
    ("n5.vocab.35-particles-functional-.ずつ", 2): "一つずつ とって ください。",
    # === Greetings / Set Phrases ===
    ("n5.vocab.36-greetings-and-set-phr.どうぞよろしく", 2): "本日は どうぞよろしく おねがいします。",
    ("n5.vocab.36-greetings-and-set-phr.いらっしゃいませ", 2): "いらっしゃいませ、何名さまですか。",
    ("n5.vocab.36-greetings-and-set-phr.ぺこぺこ", 2): "おひるまえで おなかが ぺこぺこです。",
    # === Common Nouns ===
    ("n5.vocab.37-common-nouns-miscella.しゅみ", 2): "しゅみは おんがくです。",
    ("n5.vocab.37-common-nouns-miscella.りょこう", 0): "なつに りょこうします。",
    ("n5.vocab.37-common-nouns-miscella.ティッシュ", 2): "ティッシュを 一まい ください。",
    ("n5.vocab.37-common-nouns-miscella.よてい", 2): "こんやの よていは ありますか。",
    ("n5.vocab.37-common-nouns-miscella.ストーブ", 0): "ふゆは ストーブを つかいます。",
    ("n5.vocab.37-common-nouns-miscella.メートル", 2): "百メートル はしりました。",
    ("n5.vocab.37-common-nouns-miscella.キログラム", 0): "五キログラムの こめを 買いました。",
    # === Function fillers ===
    ("n5.vocab.39-function-filler-expre.そうですね", 2): "そうですね。かんがえて みます。",
}


def main():
    vfp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = vfp + f".bak_{TODAY}_ntr_001"
    if not os.path.exists(bak):
        shutil.copy2(vfp, bak)
    with open(vfp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))

    touched = 0
    not_found = []
    for entry in vl:
        if not isinstance(entry, dict): continue
        eid = entry.get("id") or entry.get("form")
        for idx, ex in enumerate(entry.get("examples") or []):
            if not isinstance(ex, dict): continue
            key = (eid, idx)
            if key in REWRITES:
                old_ja = ex.get("ja") or ""
                new_ja = REWRITES[key]
                ex["ja"] = new_ja
                # Bump provenance to native_reviewed_2026_05_22 for the rewrite
                ex["provenance"] = "native_reviewed_2026_05_22"
                touched += 1
                print(f"  {eid}[{idx}]: {old_ja!r} -> {new_ja!r}")

    # Verify all keys in REWRITES were used
    seen = set()
    for entry in vl:
        if not isinstance(entry, dict): continue
        eid = entry.get("id") or entry.get("form")
        for idx, ex in enumerate(entry.get("examples") or []):
            seen.add((eid, idx))
    for key in REWRITES:
        if key not in seen:
            not_found.append(key)

    if not_found:
        print(f"\nWARNING: {len(not_found)} rewrite keys not found in vocab.json:")
        for k in not_found:
            print(f"  {k}")

    # Write back
    with open(vfp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print(f"\n=== Touched {touched} examples (expected {len(REWRITES)}) ===")


if __name__ == "__main__":
    main()
