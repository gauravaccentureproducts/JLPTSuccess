"""Phase D fixes — 2 new template-leak classes + 1 wrong-headword.

Caught during native-teacher review of verb-entry examples:

  Template 1 (28 entries): 「毎日 VERB-dictionary ことが できます。」
      "I can VERB every day" — pedagogically templated and often
      semantically nonsensical (毎日 こまる ことが できます = "I can be
      troubled every day"; 毎日 くもる ことが できます = "I can become
      cloudy every day").

  Template 2 (30 entries): 「あした VERB-dictionary つもりです。」
      "I plan to VERB tomorrow" — templated, with several genuinely
      wrong cases (あした 立つ つもりです = "I plan to stand tomorrow";
      あした はじまる つもりです / しまる つもりです — these are
      intransitive verbs that don't take volitional つもり).

  Wrong-headword: n5.vocab.27-verbs-group-1-verbs.すう [1] had
      'バスで 学校へ 行きます。' (about bus/school, nothing about
      smoking). Replaced with natural usage of すう.

All replacements use the entry's verb in a natural N5 context.
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")

FIXES = {
    # === Template 1: 毎日 X ことが できます (28 entries) ===
    ("n5.vocab.27-verbs-group-1-verbs.聞く", 1):
        ("先生の 話を よく 聞きます。", "I listen carefully to the teacher."),
    ("n5.vocab.27-verbs-group-1-verbs.しる", 1):
        ("田中さんの じゅうしょを しって いますか。",
         "Do you know Tanaka-san's address?"),
    ("n5.vocab.27-verbs-group-1-verbs.はく", 1):
        ("げんかんで くつを はきます。",
         "I put on shoes at the entrance."),
    ("n5.vocab.27-verbs-group-1-verbs.ひく.2", 1):
        ("妹は 毎日 ピアノを ひきます。",
         "My younger sister plays piano every day."),
    ("n5.vocab.27-verbs-group-1-verbs.こまる", 1):
        ("お金が なくて こまって います。",
         "I'm troubled because I have no money."),
    ("n5.vocab.27-verbs-group-1-verbs.わたす", 1):
        ("先生に レポートを わたしました。",
         "I handed the report to the teacher."),
    ("n5.vocab.27-verbs-group-1-verbs.はる", 1):
        ("ふうとうに きってを はりました。",
         "I put a stamp on the envelope."),
    ("n5.vocab.27-verbs-group-1-verbs.おとす", 1):
        ("さいふを 道で おとして しまいました。",
         "I dropped my wallet on the road."),
    ("n5.vocab.27-verbs-group-1-verbs.ふく", 1):
        ("タオルで てを ふきます。",
         "I wipe my hands with a towel."),
    ("n5.vocab.27-verbs-group-1-verbs.くもる", 1):
        ("あさから 空が くもって います。",
         "The sky has been cloudy since morning."),
    ("n5.vocab.27-verbs-group-1-verbs.たのむ", 1):
        ("友だちに しごとを たのみました。",
         "I asked a friend to do a job."),
    ("n5.vocab.27-verbs-group-1-verbs.とまる", 1):
        ("バスは えきの 前に とまります。",
         "The bus stops in front of the station."),
    ("n5.vocab.28-verbs-group-2-verbs.しめる", 1):
        ("出る 前に まどを しめて ください。",
         "Please close the window before leaving."),
    ("n5.vocab.28-verbs-group-2-verbs.かりる", 1):
        ("としょかんで 本を 三さつ かりました。",
         "I borrowed three books from the library."),
    ("n5.vocab.28-verbs-group-2-verbs.こたえる", 1):
        ("先生の しつもんに こたえます。",
         "I answer the teacher's question."),
    ("n5.vocab.28-verbs-group-2-verbs.かける", 1):
        ("毎晩 母に 電話を かけます。",
         "I call my mother every evening."),
    ("n5.vocab.28-verbs-group-2-verbs.ならべる", 1):
        ("おさらを テーブルに ならべます。",
         "I arrange plates on the table."),
    ("n5.vocab.28-verbs-group-2-verbs.あつめる", 1):
        ("古い きってを あつめて います。",
         "I am collecting old stamps."),
    ("n5.vocab.28-verbs-group-2-verbs.おちる", 1):
        ("木の はが 道に おちて います。",
         "Tree leaves have fallen on the road."),
    ("n5.vocab.29-verbs-irregular-and-v.さんぽする", 1):
        ("毎朝 こうえんで さんぽします。",
         "I take a walk in the park every morning."),
    ("n5.vocab.29-verbs-irregular-and-v.れんしゅうする", 1):
        ("ピアノを 一時間 れんしゅうしました。",
         "I practiced piano for one hour."),
    ("n5.vocab.29-verbs-irregular-and-v.しごとする", 1):
        ("父は ぎんこうで しごとして います。",
         "My father works at a bank."),
    ("n5.vocab.29-verbs-irregular-and-v.コピーする", 1):
        ("この 紙を 三まい コピーして ください。",
         "Please make three copies of this paper."),
    ("n5.vocab.29-verbs-irregular-and-v.そうじする", 1):
        ("土曜日に へやを そうじしました。",
         "I cleaned my room on Saturday."),
    ("n5.vocab.29-verbs-irregular-and-v.かいものする", 1):
        ("コンビニで かいものしました。",
         "I shopped at the convenience store."),
    ("n5.vocab.30-verbs-existence-and-p.あげる", 1):
        ("ともだちに たんじょうびの プレゼントを あげました。",
         "I gave a birthday present to my friend."),
    ("n5.vocab.30-verbs-existence-and-p.かえす", 1):
        ("としょかんに 本を かえしました。",
         "I returned the book to the library."),
    ("n5.vocab.27-verbs-group-1-verbs.はらう", 1):
        ("レジで お金を はらいます。",
         "I pay money at the cashier."),

    # === Template 2: あした X つもりです (30 entries) ===
    ("n5.vocab.27-verbs-group-1-verbs.うたう", 1):
        ("みんなで しあわせの うたを うたいました。",
         "We all sang a happy song together."),
    ("n5.vocab.27-verbs-group-1-verbs.立つ", 1):
        ("先生が きょうしつの 前に 立って います。",
         "The teacher is standing in front of the classroom."),
    ("n5.vocab.27-verbs-group-1-verbs.はしる", 1):
        ("毎朝 こうえんで はしります。",
         "I run in the park every morning."),
    ("n5.vocab.27-verbs-group-1-verbs.もつ", 1):
        ("にもつを 一つ もって 行きます。",
         "I'll go carrying one piece of luggage."),
    ("n5.vocab.27-verbs-group-1-verbs.はじまる", 1):
        ("じゅぎょうは 九時に はじまります。",
         "Class begins at 9."),
    ("n5.vocab.27-verbs-group-1-verbs.うる", 1):
        ("やおやで やさいを うって います。",
         "Vegetables are sold at the greengrocer."),
    ("n5.vocab.27-verbs-group-1-verbs.よぶ", 1):
        ("先生を 大きい こえで よびました。",
         "I called the teacher in a loud voice."),
    ("n5.vocab.27-verbs-group-1-verbs.ならぶ", 1):
        ("ラーメンやの 前に 人が ならんで います。",
         "People are lined up in front of the ramen shop."),
    ("n5.vocab.27-verbs-group-1-verbs.のぼる", 1):
        ("ふじ山に のぼる 人が 多いです。",
         "Many people climb Mt. Fuji."),
    ("n5.vocab.27-verbs-group-1-verbs.ぬぐ", 1):
        ("家の 中では くつを ぬぎます。",
         "We take off our shoes inside the house."),
    ("n5.vocab.27-verbs-group-1-verbs.いそぐ", 1):
        ("おくれそうなので いそぎましょう。",
         "We might be late, so let's hurry."),
    ("n5.vocab.27-verbs-group-1-verbs.ならう", 1):
        ("ピアノを 五さいから ならって います。",
         "I have been learning piano since age five."),
    ("n5.vocab.27-verbs-group-1-verbs.もってくる", 1):
        ("あした 本を もって きて ください。",
         "Please bring a book tomorrow."),
    ("n5.vocab.27-verbs-group-1-verbs.しまる", 1):
        ("お店は 夜 十時に しまります。",
         "The shop closes at 10 pm."),
    ("n5.vocab.27-verbs-group-1-verbs.だす", 1):
        ("ふうとうに きってを はって だしました。",
         "I put a stamp on the envelope and sent it."),
    ("n5.vocab.27-verbs-group-1-verbs.なくす", 1):
        ("えきで かさを なくしました。",
         "I lost my umbrella at the station."),
    ("n5.vocab.27-verbs-group-1-verbs.けす", 1):
        ("出る とき 電気を けして ください。",
         "Please turn off the light when you leave."),
    ("n5.vocab.28-verbs-group-2-verbs.出る", 1):
        ("七時に いえを 出ます。",
         "I leave home at 7."),
    ("n5.vocab.28-verbs-group-2-verbs.入れる", 1):
        ("コーヒーに さとうを 入れて ください。",
         "Please put sugar in the coffee."),
    ("n5.vocab.28-verbs-group-2-verbs.おしえる", 1):
        ("私の 電話番号を おしえます。",
         "I'll give you my phone number."),
    ("n5.vocab.28-verbs-group-2-verbs.つける", 1):
        ("くらいので 電気を つけます。",
         "It's dark, so I'll turn on the light."),
    ("n5.vocab.28-verbs-group-2-verbs.見せる", 1):
        ("私の しゃしんを 友だちに 見せます。",
         "I show my photo to my friend."),
    ("n5.vocab.28-verbs-group-2-verbs.いれる", 1):
        ("ふうとうに てがみを いれました。",
         "I put the letter into the envelope."),
    ("n5.vocab.29-verbs-irregular-and-v.けっこんする", 1):
        ("姉は 来月 けっこんします。",
         "My older sister is getting married next month."),
    ("n5.vocab.29-verbs-irregular-and-v.りょこうする", 1):
        ("なつ休みに かぞくと りょこうします。",
         "I'll travel with my family during summer vacation."),
    ("n5.vocab.29-verbs-irregular-and-v.しつもんする", 1):
        ("わからない とき 先生に しつもんします。",
         "When I don't understand, I ask the teacher."),
    ("n5.vocab.29-verbs-irregular-and-v.電話する", 1):
        ("おそく なって ごめんね。あとで 電話する。",
         "Sorry I'm late. I'll call you later."),
    ("n5.vocab.29-verbs-irregular-and-v.せんたくする", 1):
        ("日曜日に せんたくします。",
         "I do the laundry on Sunday."),
    ("n5.vocab.30-verbs-existence-and-p.やる", 1):
        ("ねこに ごはんを やります。",
         "I feed the cat."),
    ("n5.vocab.28-verbs-group-2-verbs.おくれる", 1):
        ("バスが おくれて、しごとに おくれました。",
         "The bus was late, so I was late for work."),

    # === Wrong-headword: すう ===
    ("n5.vocab.27-verbs-group-1-verbs.すう", 1):
        ("ここで たばこを すっても いいですか。",
         "May I smoke a cigarette here?"),
}


def main():
    d = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    n = missing = 0
    for (vid, idx), (new_ja, new_en) in FIXES.items():
        for e in d["entries"]:
            if e["id"] == vid:
                if idx < len(e.get("examples", [])):
                    e["examples"][idx]["ja"] = new_ja
                    e["examples"][idx]["translation_en"] = new_en
                    n += 1
                else:
                    missing += 1
                break
        else:
            missing += 1
            print(f"  MISSING: {vid}")
    VOCAB.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Applied {n}/{len(FIXES)} fixes (missing: {missing})")


if __name__ == "__main__":
    main()
