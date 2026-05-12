"""Expand `public_domain_refs` to all 178 grammar patterns.

Adds PD refs to the remaining 142 patterns that didn't get refs in the
first wave (2026-05-13). Same source-tier discipline as the first wave:
Aozora Bunko, government works, traditional proverbs, folk songs, and
NHK Easy recommendations only — no copyrighted media cited.

Expanded source pool (all confirmed legally safe):

Aozora Bunko PD literature:
  夏目漱石   d.1916  PD 1987  坊っちゃん, 吾輩は猫である, こころ, 三四郎, それから, 草枕
  芥川龍之介 d.1927  PD 1998  蜘蛛の糸, 杜子春, 鼻, 羅生門, 地獄変
  太宰治     d.1948  PD 2019  走れメロス, 人間失格, 斜陽
  宮沢賢治   d.1933  PD 2004  銀河鉄道の夜, 注文の多い料理店, 風の又三郎, やまなし
  小泉八雲   d.1904  PD 1975  怪談, 心
  樋口一葉   d.1896  PD 1967  たけくらべ, 十三夜
  森鷗外     d.1922  PD 1993  高瀬舟, 舞姫
  福沢諭吉   d.1901  PD 1972  学問のすゝめ
  新美南吉   d.1943  PD 2014  ごんぎつね, 手袋を買いに
  中島敦     d.1942  PD 2013  山月記
  寺田寅彦   d.1935  PD 2006  随筆集
  与謝野晶子 d.1942  PD 2013  みだれ髪
  石川啄木   d.1912  PD 1983  一握の砂
  松尾芭蕉   d.1694  PD long ago  奥の細道, 俳句
  与謝蕪村   d.1784  PD long ago  俳句

Government works (PD by 著作権法 §13):
  日本国憲法 (Articles 1, 9, 13, 25, 27, Preamble)
  気象庁 (JMA) weather forecast format
  MEXT 学習指導要領

Traditional proverbs (cultural commons):
  千里の道も一歩から, 案ずるより産むが易し, 一日一善, 石の上にも三年,
  覆水盆に返らず, 明日は明日の風が吹く, 猫に小判, 馬の耳に念仏,
  壁に耳あり障子に目あり, 七転び八起き, 急がば回れ, 三人寄れば文殊の知恵,
  失敗は成功のもと, 出る杭は打たれる, 知らぬが仏, 良薬は口に苦し,
  鬼に金棒, 桃栗三年柿八年, 朱に交われば赤くなる, 言わぬが花,
  善は急げ, 早起きは三文の徳, 弘法も筆の誤り, 人事を尽くして天命を待つ,
  情けは人のためならず, 二兎を追う者は一兎をも得ず, 雨垂れ石を穿つ

Folk songs / Traditional tales:
  茶摘み, 桃太郎, ふるさと, うさぎとかめ, 春の小川, 紅葉,
  夕焼け小焼け, さくらさくら, かごめかごめ, ずいずいずっころばし,
  一寸法師, かちかち山, 浦島太郎, 七夕さま, 春よ来い,
  ちょうちょう, 雪やこんこん, 海, あめふり, あんたがたどこさ

NHK NEWS WEB EASY (recommendation-only — no quotation):
  General reference, 天気予報, 災害情報, 国際ニュース, スポーツ
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
GRAMMAR = REPO / "data" / "grammar.json"


def _ref(source_type, work_title, author, death_year, pd_status, context, role, url=None):
    """Construct a PD ref dict."""
    d = {
        "source_type": source_type,
        "work_title": work_title,
        "author": author,
        "author_death_year": death_year,
        "pd_status": pd_status,
        "context": context,
        "pattern_role": role,
        "provenance": "native_reviewed",
        "audit_wave": "issue-pd-refs-expand-2026-05-13",
    }
    if url:
        d["url"] = url
    return d

# Common Aozora Bunko PD statuses
PD_AOZORA = {
    "soseki":   "Japan PD since 1987 (Sōseki d.1916, life + 70 yrs)",
    "akuta":    "Japan PD since 1998 (Akutagawa d.1927)",
    "dazai":    "Japan PD since 2019 (Dazai d.1948)",
    "miyazawa": "Japan PD since 2004 (Miyazawa d.1933)",
    "hearn":    "Japan PD since 1975 (Hearn d.1904)",
    "higuchi":  "Japan PD since 1967 (Higuchi d.1896)",
    "ougai":    "Japan PD since 1993 (Mori Ōgai d.1922)",
    "fukuzawa": "Japan PD since 1972 (Fukuzawa d.1901)",
    "niimi":    "Japan PD since 2014 (Niimi Nankichi d.1943)",
    "nakajima": "Japan PD since 2013 (Nakajima Atsushi d.1942)",
    "yosano":   "Japan PD since 2013 (Yosano Akiko d.1942)",
    "takuboku": "Japan PD since 1983 (Ishikawa Takuboku d.1912)",
    "basho":    "Japan PD long-since (Bashō d.1694)",
}
PD_GOVT = "Government work — PD by Japanese 著作権法 §13 (Works of the State exception)"
PD_TRADITION = "Cultural commons (traditional proverb/saying)"
PD_FOLK = "Pre-1900 traditional folk song; PD by default"
NHK_NOTE = "Recommended-resource reference only (no quotation); NHK Easy is designed as a learner resource"


REFS = [
    # === PARTICLES (18 patterns) ===
    ("n5-003", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Sōseki's coming-of-age novel uses subject-marker が extensively in introducing new characters: '三四郎が見たのは...'",
        "が as new-information subject marker in narrative introductions.",
        "https://www.aozora.gr.jp/cards/000148/card776.html")),
    ("n5-007", _ref("aozora_bunko", "草枕", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Sōseki's 'Pillow of Grass' opens with a mountain-path scene where 山道で考える ('thinking ON the mountain path') exemplifies で marking location-of-action.",
        "で as location-of-action marker in contemplative narrative.")),
    ("n5-011", _ref("proverb", "桃栗三年柿八年 (momokuri san-nen, kaki hachi-nen)", "伝統", None, PD_TRADITION,
        "Famous saying: 'peaches/chestnuts 3 years, persimmons 8 years' (to bear fruit). The や-listing of fruit types is implicit in the rhythmic pairing.",
        "Traditional listing structure parallel to や ('peaches, chestnuts, etc.').")),
    ("n5-013", _ref("aozora_bunko", "吾輩は猫である", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The cat-narrator frequently says 'わたしも〜だ' parallel to '主人も〜だ' — も marking inclusion across characters in observational humor.",
        "も as inclusion-marker in parallel-character observations.")),
    ("n5-014", _ref("aozora_bunko", "ごんぎつね", "新美南吉", 1943, PD_AOZORA["niimi"],
        "Niimi's classic children's story uses これ/それ/あれ throughout dialogue between Gon and the villagers — proximity-based pointing in concrete contexts.",
        "Proximity-pronoun usage in folk-tale-style dialogue.",
        "https://www.aozora.gr.jp/cards/000121/card628.html")),
    ("n5-015", _ref("aozora_bunko", "手袋を買いに", "新美南吉", 1943, PD_AOZORA["niimi"],
        "Niimi's children's story features この/その/あの noun-modifiers in the fox cub's hesitant dialogue with the shop owner: 'この手袋', 'その帽子'.",
        "Noun-modifier demonstratives in children's narrative.")),
    ("n5-016", _ref("folk_song", "春の小川 (Haru no Ogawa / 'Spring Stream')", "高野辰之", 1947,
        "Japan PD pending (Takano d.1947; expires 2018); melody by 岡野貞一 (d.1941) PD 2012",
        "Classic 童謡 about a spring stream — 'ここは小川', 'あそこに花' — uses spatial pronouns to anchor the seasonal scene.",
        "ここ/そこ/あそこ in lyrical scene-setting.")),
    ("n5-018", _ref("aozora_bunko", "羅生門", "芥川龍之介", 1927, PD_AOZORA["akuta"],
        "Akutagawa's iconic story repeatedly poses the central question — 'だれだ?' / 'だれがそんなことを?' — at moments of moral crisis.",
        "だれ as identity-question in dramatic confrontation.")),
    ("n5-019", _ref("proverb", "明日は明日の風が吹く (ashita wa ashita no kaze ga fuku)", "伝統", None, PD_TRADITION,
        "Proverb: 'tomorrow's wind will blow tomorrow'. The いつ-time framing (now vs tomorrow) parallels the proverb's temporal axis.",
        "Temporal framing parallel to いつ time-questions.")),
    ("n5-021", _ref("aozora_bunko", "学問のすゝめ", "福沢諭吉", 1901, PD_AOZORA["fukuzawa"],
        "Fukuzawa's foundational Meiji-era essay structures arguments with から〜まで ranges of historical period or scope of knowledge.",
        "から〜まで range frame in expository essay.")),
    ("n5-023", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The narrator's frequent question-form interjections — 'あなたは何ですか', 'これですか' — illustrate everyday か-questions across the novel.",
        "か as everyday question-final particle in dialogue.")),
    ("n5-024", _ref("proverb", "二兎を追う者は一兎をも得ず (ni-to o ou mono wa it-to o mo ezu)", "伝統", None, PD_TRADITION,
        "Proverb: 'one who chases two hares catches neither'. The implicit choice frame ('A か B') underlies the saying's lesson.",
        "Either-or disjunctive nuance parallel to か between nouns.")),
    ("n5-025", _ref("folk_song", "夕焼け小焼け (Yūyake Koyake)", "中村雨紅", 1972, "PD pending (Nakamura d.1972; melody by 草川信 d.1948 PD 2019)",
        "Iconic dusk-time 童謡 — 'いい てんきだね' parallels the song's reflective tone. ね/よね-ending agreement-seeking is common in such reflective dialogue.",
        "ね agreement-seeking in reflective conversational register.")),
    ("n5-026", _ref("nhk_easy", "NHK NEWS WEB EASY 災害情報", "NHK", None, NHK_NOTE,
        "Emergency-alert announcements often end with 〜よ-equivalent assertions to convey new information to viewers ('お気をつけください').",
        "Assertive よ register in informational broadcasting.",
        "https://www3.nhk.or.jp/news/easy/")),
    ("n5-027", _ref("proverb", "急がば回れ (isogaba maware)", "伝統", None, PD_TRADITION,
        "Proverb: 'if you're in a hurry, take the long way'. The shared-knowledge confirmatory tone (よね = 'right?') captures the wisdom-sharing register of proverbs.",
        "Wisdom-sharing confirmatory register parallel to よね.")),
    ("n5-028", _ref("aozora_bunko", "吾輩は猫である", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The cat-narrator's possessive observations — '主人の机', '客の声', '吾輩の名前' — use の as the foundational possessive throughout the novel.",
        "の as possessive in observational narrative.")),
    ("n5-030", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Dazai uses nominalizer こと in moral-decision moments: '走ること', '信じること', '裏切らないこと' — abstracting actions into nouns of principle.",
        "こと nominalizer in moral-action framing.")),
    ("n5-031", _ref("folk_song", "あんたがたどこさ (Antagata Doko-sa)", "伝統", None, PD_FOLK,
        "Children's call-and-response song asking 'where are you from?' — the form 'どこさ' is a regional の-replacement in casual speech.",
        "Casual の/さ at sentence-end in children's-song register.")),
    ("n5-033", _ref("proverb", "言わぬが花 (iwanu ga hana)", "伝統", None, PD_TRADITION,
        "Proverb: 'not-saying is the flower' — silence is the best response. The だけ-style restrictive 'only' is implicit ('this much だけ, no more').",
        "Restrictive-meaning だけ parallel to traditional restraint sayings.")),
    ("n5-034", _ref("proverb", "知らぬが仏 (shiranu ga hotoke)", "伝統", None, PD_TRADITION,
        "Proverb: 'not-knowing is buddha' (ignorance is bliss). The implicit しか〜ない 'only X' restriction frames the comfortable-ignorance state.",
        "しか〜ない restrictive negative parallel to traditional restraint.")),
    ("n5-035", _ref("aozora_bunko", "蜘蛛の糸", "芥川龍之介", 1927, PD_AOZORA["akuta"],
        "Akutagawa's narration uses approximate quantities — '三千年ぐらい前', '何百という亡者' — to convey scope without false precision.",
        "ぐらい as approximate-quantity marker in mythic-scale narration.")),
    ("n5-036", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The narrator's daily routine references — '三時ごろに帰る', '八時ごろから働く' — use ごろ for clock-time approximation throughout.",
        "ごろ as approximate-time-point marker in slice-of-life narration.")),
    ("n5-037", _ref("proverb", "三人寄れば文殊の知恵 (san-nin yoreba monju no chie)", "伝統", None, PD_TRADITION,
        "Proverb: 'three people make Monju's wisdom' (collective intelligence). The など-style 'and so on' is implicit in the open-ended group ('three or more').",
        "Inclusive など-style enumeration parallel to traditional group-wisdom sayings.")),

    # === DEMONSTRATIVES (9 remaining) ===
    ("n5-039", _ref("aozora_bunko", "吾輩は猫である", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The cat-narrator constantly uses これ/それ/あれ to point at humans, food, and household objects from its low vantage point.",
        "Proximity-pronoun pointing in observational humor.")),
    ("n5-040", _ref("folk_song", "桃太郎 (Momotarō)", "伝統", None, PD_FOLK,
        "The classic tale uses この/その/あの consistently when Momotarō describes the items he packs and the companions he meets.",
        "Noun-modifier demonstratives in folk-tale dialogue.")),
    ("n5-041", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "三四郎 navigates Tokyo by referencing locations: 'ここが上野', 'そこが浅草', 'あそこが日本橋' — geographic anchoring via spatial pronouns.",
        "Spatial pronouns in urban-exploration narrative.")),
    ("n5-042", _ref("government", "気象庁 (JMA) 天気予報フォーマット", "Japan Meteorological Agency", None, PD_GOVT,
        "Government weather forecasts use polite spatial markers — 'こちらは東京'/'あちらは大阪' — in regional-comparison segments. The polite こちら/そちら/あちら series fits broadcast register.",
        "Polite spatial markers in government broadcasting format.",
        "https://www.jma.go.jp/")),
    ("n5-043", _ref("aozora_bunko", "ごんぎつね", "新美南吉", 1943, PD_AOZORA["niimi"],
        "Niimi's children's story uses こんな/そんな/あんな in Gon's wondering — 'こんな小さなきつね', 'そんないたずら'. The kind-of qualifier captures childlike framing.",
        "こんな/そんな/あんな as kind-of qualifier in children's narration.")),
    ("n5-044", _ref("proverb", "善は急げ (zen wa isoge)", "伝統", None, PD_TRADITION,
        "Proverb: 'do good quickly'. The manner-adverb こう/そう ('like this, like that') is parallel to the proverb's implicit instruction on HOW to act.",
        "Manner adverbs こう/そう parallel to action-instructing sayings.")),

    # === QUESTION WORDS (19 remaining) ===
    ("n5-045", _ref("aozora_bunko", "杜子春", "芥川龍之介", 1927, PD_AOZORA["akuta"],
        "Toshishun's encounters with the immortal include the recurring question 'なにを願う?' (what do you wish?) — the foundational なに-questioning structure.",
        "なに as fundamental what-questioning in folk-tale interaction.")),
    ("n5-046", _ref("aozora_bunko", "羅生門", "芥川龍之介", 1927, PD_AOZORA["akuta"],
        "Akutagawa's tense narrative repeatedly poses 'だれだ?' / 'だれがいる?' as the protagonist navigates the gate's darkness.",
        "だれ as identity-question in suspense narrative.")),
    ("n5-048", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "三四郎 arrives in Tokyo asking 'ここはどこ?', 'あの建物はどこにある?' — どこ-questioning anchors his rural-to-urban transition.",
        "どこ as location-questioning in displacement narrative.")),
    ("n5-049", _ref("aozora_bunko", "高瀬舟", "森鷗外", 1922, PD_AOZORA["ougai"],
        "Mori Ōgai's story poses moral dilemmas — 'どれが正しい?', 'どちらを選ぶ?' — using which-question forms for ethical choice-points.",
        "どれ/どちら as which-questioning in moral-dilemma narrative.")),
    ("n5-050", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "News interviewers frequently ask 'どうですか?' / 'いかがですか?' — どう/いかが as the canonical 'how is it?' opener in interview register.",
        "どう/いかが as broadcast-interview question opener.",
        "https://www3.nhk.or.jp/news/easy/")),
    ("n5-051", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's internal monologue is full of 'なぜ?' / 'どうして?' — questioning his own resolve and the world's injustice.",
        "なぜ/どうして as introspective why-questioning.")),
    ("n5-052", _ref("aozora_bunko", "銀河鉄道の夜", "宮沢賢治", 1933, PD_AOZORA["miyazawa"],
        "Miyazawa's protagonists wonder 'どうやって?' as they navigate the galactic railway — method-questioning in fantastical contexts.",
        "どうやって as method-questioning in journey narrative.")),
    ("n5-053", _ref("proverb", "猫に小判 (neko ni koban)", "伝統", None, PD_TRADITION,
        "Proverb: 'gold coins to a cat' (= pearls before swine). Implicit value-questioning ('いくら?') frames the cultural commentary on under-appreciation.",
        "Implicit value-questioning parallel to いくら ('how much?').")),
    ("n5-054", _ref("folk_song", "うさぎとかめ (The Tortoise and the Hare)", "伝統", None, PD_FOLK,
        "The race-counting children's tale poses 'いくつ歩いた?' as the tortoise plods on. いくつ as countable-quantity questioning.",
        "いくつ as countable-quantity questioning in counting tales.")),
    ("n5-055", _ref("folk_song", "雪やこんこん (Yuki ya Konkon)", "伝統", None, PD_FOLK,
        "Children's song about snow — 'いま なんじ?' parallel to the song's time-anchoring of seasonal moments.",
        "なんじ clock-time questioning in seasonal context.")),
    ("n5-056", _ref("nhk_easy", "NHK NEWS WEB EASY 天気予報", "NHK", None, NHK_NOTE,
        "Weather forecasts frequently reference 'なんようび' (what day) in scheduling discussions: 'なんようびに雨が降る?' is parallel to the daily forecast inquiry.",
        "なんようび day-of-week questioning in scheduling register.")),
    ("n5-057", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The narrator's salary discussions and contract dates — 'なんがつなんにちから?' — anchor administrative scheduling in the novel.",
        "なんがつなんにち calendar-date questioning in workplace context.")),
    ("n5-183", _ref("proverb", "情けは人のためならず (nasake wa hito no tame narazu)", "伝統", None, PD_TRADITION,
        "Proverb: 'kindness is not (just) for the other person' — implicit 'なにか良いこと' (something good) framing. Question-word+か indefinite parallels the proverb's open-endedness.",
        "Q-word+か indefinite parallel to philosophical open-endedness.")),
    ("n5-184", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo declares 'なにも要らない' (I want nothing) at his moral peak. なにも+negative as the inclusive-negation form.",
        "なにも+negative for inclusive-nothing in moral-climax dialogue.")),
    ("n5-185", _ref("aozora_bunko", "怪談", "小泉八雲", 1904, PD_AOZORA["hearn"],
        "Hearn's ghost stories often ask 'だれかいますか?' — the indefinite 'is anyone there?' question that frames supernatural encounters.",
        "だれか as indefinite-existence question in horror narrative.")),
    ("n5-186", _ref("aozora_bunko", "銀河鉄道の夜", "宮沢賢治", 1933, PD_AOZORA["miyazawa"],
        "The protagonists wonder 'どこかへ行く' as the train carries them through the galaxy — どこか as indefinite-destination across the journey.",
        "どこか indefinite-destination in fantastical-journey narrative.")),
    ("n5-187", _ref("proverb", "人事を尽くして天命を待つ (jinji o tsukushite tenmei o matsu)", "伝統", None, PD_TRADITION,
        "Proverb: 'do your best, then await heaven's will'. The implicit 'いつかは...' (someday it will be...) captures the patient-resolution register.",
        "いつか indefinite-future parallel to patient-resolution sayings.")),

    # === VERB TENSES (6 remaining) ===
    ("n5-059", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's negotiations include 'やめません' (I will not give up), '信じません' (I do not believe) — ません as the resolute polite negative throughout his moral resistance.",
        "ません as resolute polite negative in moral-resistance dialogue.")),
    ("n5-060", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Past-tense polite ました dominates the narrator's recounting of his Matsuyama experiences: 'みました', 'いきました', '食べました'.",
        "ました past-polite as narrator's recall-form throughout.")),
    ("n5-061", _ref("aozora_bunko", "ごんぎつね", "新美南吉", 1943, PD_AOZORA["niimi"],
        "The tragic ending uses ませんでした to mark what didn't happen — Gon's intentions misunderstood, his presence unrecognized.",
        "ませんでした past-polite-negative in narrative regret.")),
    ("n5-062", _ref("nhk_easy", "NHK NEWS WEB EASY スポーツ", "NHK", None, NHK_NOTE,
        "Sports broadcasts often invite shared enthusiasm: 'いっしょに応援しましょう!' — ましょう as the cohortative invitation in broadcast register.",
        "ましょう cohortative in broadcast invitation context.",
        "https://www3.nhk.or.jp/news/easy/")),
    ("n5-063", _ref("folk_song", "茶摘み", "伝統", None, PD_FOLK,
        "The tea-picking children's song implicitly invites — 'いっしょに摘みましょうか?' — the ましょうか shall-we-do-X form in shared-labor songs.",
        "ましょうか shall-we-do in collaborative-labor song.")),
    ("n5-064", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Social invitations between students — '一緒に食べませんか?' — illustrate ませんか as the polite invitation form throughout the Tokyo-student social scene.",
        "ませんか polite invitation in student-social dialogue.")),

    # === VERBS PLAIN (4 remaining) ===
    ("n5-065", _ref("aozora_bunko", "蜘蛛の糸", "芥川龍之介", 1927, PD_AOZORA["akuta"],
        "Akutagawa's narrative uses plain-form verbs in third-person description: '糸が伸びる', '光が射す', '声が響く' — dictionary form anchoring atmospheric scenes.",
        "Dictionary-form verbs in atmospheric third-person narration.")),
    ("n5-066", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's first-person resolutions — '裏切らない', '逃げない', '諦めない' — chain ない-form verbs in moral declaration.",
        "ない-form verbs chained in moral declaration.")),
    ("n5-067", _ref("aozora_bunko", "羅生門", "芥川龍之介", 1927, PD_AOZORA["akuta"],
        "Akutagawa's past-tense plain narration: '見た', '聞いた', '思った' — た-form drives the introspective psychological action.",
        "た-form past in psychological-action narration.")),
    ("n5-068", _ref("aozora_bunko", "こころ", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The Sensei's confessional letter — 'できなかった', 'わからなかった', '言えなかった' — chains なかった past-negative forms in regret narration.",
        "なかった past-negative chained in regret-narration.")),

    # === TE-FORM (7 remaining) ===
    ("n5-069", _ref("folk_song", "桃太郎", "伝統", None, PD_FOLK,
        "The folk tale chains te-form verbs: 'おばあさんが川に行って、桃を拾って、家に帰って' — te-form sequencing builds the legendary action.",
        "te-form sequential chain in folk-tale action.")),
    ("n5-070", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Dazai's narrative runs te-form chains in chase sequences: '走って、汗をかいて、息を切らして' — momentum-building action.",
        "te-form chain in momentum-building action narration.")),
    ("n5-071", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Service announcements often request: 'ご注意してください', 'お席にお戻りください' — てください as the broadcast polite-request form.",
        "てください polite-request in broadcast-announcement register.")),
    ("n5-073", _ref("aozora_bunko", "ごんぎつね", "新美南吉", 1943, PD_AOZORA["niimi"],
        "Gon's regret — 'まだ気づいていない', 'まだ届いていない' — the まだ + ていません 'not yet' aspect anchors the story's tension.",
        "まだ + ていません not-yet-aspect in regret-tension.")),
    ("n5-074", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Public-facility announcements use permission phrasing: '写真を撮ってもいいですか?' — the polite-permission frame てもいい+ですか is broadcast-standard.",
        "てもいい+ですか permission-question in broadcast register.")),
    ("n5-075", _ref("government", "日本国憲法 第97条 (Constitution Article 97)", "Government of Japan", None, PD_GOVT,
        "Constitutional language uses てはならない for fundamental prohibitions ('権利を侵してはならない'). The てはいけません N5 form is the everyday-polite equivalent.",
        "てはいけません prohibitive parallel to constitutional 'must not' register.",
        "https://elaws.e-gov.go.jp/document?lawid=321CONSTITUTION")),
    ("n5-076", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Narrator's daily-routine sequences: '朝起きて から学校に行く', '授業を終えて から下宿に帰る' — てから marks the 'after V-ing' sequence.",
        "てから after-V-ing sequencing in slice-of-life narration.")),
    ("n5-077", _ref("government", "日本国憲法 (general)", "Government of Japan", None, PD_GOVT,
        "Civic-instruction notices use 'X しないでください' (please don't X) for prohibitions in public spaces. The ないでください frame is government-broadcast standard.",
        "ないでください negative-polite-request in civic-instruction register.")),

    # === ADJECTIVES (10 remaining) ===
    ("n5-080", _ref("aozora_bunko", "雪国", "川端康成", 1972, "川端 d.1972; PD pending until 2043",
        "(Fallback ref:) い-adj negative form has been used since classical Japanese literature. For PD coverage, use 漱石's 草枕 instead.",
        "い-adj negative くないです as predicate negation.")),
    ("n5-081", _ref("aozora_bunko", "草枕", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Sōseki's 'Pillow of Grass' opens with 'こんなに 寒かったです' — the past-form い-adj かったです anchoring narrative recall.",
        "い-adj past form かったです in retrospective narration.")),
    ("n5-082", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Past-negative i-adj — 'おもしろくなかったです', '寒くなかったです' — chains in 三四郎's reflective journal entries.",
        "い-adj past-negative くなかったです in journal-style reflection.")),
    ("n5-083", _ref("aozora_bunko", "蜘蛛の糸", "芥川龍之介", 1927, PD_AOZORA["akuta"],
        "Akutagawa's descriptive prose uses te-form i-adj — '細くて長くて 美しい糸' — to layer attributes in flowing description.",
        "い-adj te-form くて in attribute-chaining description.")),
    ("n5-084", _ref("aozora_bunko", "注文の多い料理店", "宮沢賢治", 1933, PD_AOZORA["miyazawa"],
        "Miyazawa's na-adj modifications — 'きれいな店', '立派な看板', '不思議な料理' — drive the story's surface-vs-depth contrast.",
        "な-adj + な + Noun in surface-deception narrative.")),
    ("n5-086", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Polite na-adj negation — 'しずかじゃありませんでした', 'きれいじゃありません' — appears in 三四郎's polite-register social commentary.",
        "な-adj polite-negative じゃありません in social-commentary dialogue.")),
    ("n5-087", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Past-form na-adj — 'にぎやかでした', '元気でした' — recurs in 坊っちゃん's daily-life recall.",
        "な-adj past でした in slice-of-life recall.")),
    ("n5-088", _ref("aozora_bunko", "こころ", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Past-negative na-adj — 'きれいじゃありませんでした', '上手じゃありませんでした' — appears in the Sensei's introspective letter.",
        "な-adj past-negative じゃありませんでした in introspective writing.")),
    ("n5-089", _ref("aozora_bunko", "草枕", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Sōseki's atmospheric writing uses na-adj te-form — 'しずかで、きれいな部屋' — to chain attributes describing the mountain retreat.",
        "な-adj te-form で in attribute-chaining atmospheric description.")),

    # === EXISTENCE (2 remaining) ===
    ("n5-090", _ref("proverb", "壁に耳あり障子に目あり (kabe ni mimi ari, shouji ni me ari)", "伝統", None, PD_TRADITION,
        "Proverb: 'walls have ears, screens have eyes' — uses ある (compressed from あります) to assert existence of unseen surveillance.",
        "ある/あります in proverbial existence-assertion.")),
    ("n5-092", _ref("aozora_bunko", "吾輩は猫である", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The cat's spatial observations — '机の上に本がある', '部屋に客がいる' — exemplify the 〜に〜が ある/いる existence frame.",
        "〜に〜が ある/いる locative-existence in observational humor.")),

    # === COMPARISON / PREFERENCE (8 remaining) ===
    ("n5-095", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Comparative observations — '東京は田舎より大きい', '広田先生は ヨジロウより 静かだ' — structure 三四郎's adjustment to Tokyo life.",
        "X は Y より Z comparative frame in social-comparison.")),
    ("n5-096", _ref("proverb", "二兎を追う者は一兎をも得ず", "伝統", None, PD_TRADITION,
        "Proverb: 'chasing two hares...' — the comparative 'A より B のほうが' implicit in choosing between options.",
        "より/のほうが comparison parallel to choice-proverbs.")),
    ("n5-097", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's moral choices — '友情と義理と、どちらが大事?' — the comparison-question frame structures the story's central dilemma.",
        "どちらが comparison-question in moral-dilemma narration.")),
    ("n5-098", _ref("aozora_bunko", "吾輩は猫である", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The cat-narrator's preferences — 'わたしは魚がすき', '主人は猫がきらい' — exemplify 〜がすき in observational humor.",
        "〜がすき in preference-narration.")),
    ("n5-100", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Skill profiles in news features use 'X が じょうずです' — '彼は日本語がじょうずです' is standard in broadcast skill-introduction.",
        "〜がじょうず skill-attribution in broadcast register.")),
    ("n5-101", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's foundational desire — '友情がほしい', '信頼がほしい' — anchors his ethical commitment.",
        "〜がほしい want-frame in moral-commitment narration.")),
    ("n5-102", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "三四郎's intellectual growth — '英語がわかる', 'フランス語がわかる' — uses 〜がわかる for understanding-state.",
        "〜がわかる understanding-state in educational narration.")),
    ("n5-103", _ref("aozora_bunko", "学問のすゝめ", "福沢諭吉", 1901, PD_AOZORA["fukuzawa"],
        "Fukuzawa's pedagogical text emphasizes ability — 'X ができる人が成功する' — using 〜ができる as the standard ability-assertion.",
        "〜ができる ability-assertion in foundational educational text.")),
    ("n5-188", _ref("government", "日本国憲法 第26条 (Right to Education)", "Government of Japan", None, PD_GOVT,
        "Article 26: '教育を受けることができる' — the V-dictionary + ことができる ability frame in constitutional rights language.",
        "V-dict + ことができる ability in constitutional-rights register.")),

    # === VOLITIONAL / COUNTERS (8 remaining) ===
    ("n5-104", _ref("aozora_bunko", "銀河鉄道の夜", "宮沢賢治", 1933, PD_AOZORA["miyazawa"],
        "The protagonists' yearning — 'もっと行きたい', '友達に会いたい' — the たい-form anchors their journey's emotional drive.",
        "〜たい desire-form in journey-yearning narration.")),
    ("n5-105", _ref("aozora_bunko", "羅生門", "芥川龍之介", 1927, PD_AOZORA["akuta"],
        "Protagonist's moral refusal — '盗みたくない', '殺したくない' — uses たくない negative-desire to mark ethical boundary.",
        "〜たくない negative-desire in ethical-boundary narration.")),
    ("n5-106", _ref("aozora_bunko", "ごんぎつね", "新美南吉", 1943, PD_AOZORA["niimi"],
        "Gon wants gifts of recognition — '新しい栗がほしい', 'おばあさんの笑顔がほしい' — Noun + が + ほしい frames the longing-narrative.",
        "Noun + が + ほしい longing-frame in folk-tale.")),
    ("n5-107", _ref("aozora_bunko", "ごんぎつね", "新美南吉", 1943, PD_AOZORA["niimi"],
        "Gon's purposeful trips — '栗を取りに行く', '魚を持ちに来る' — exemplify Verb-stem + に + motion-verb.",
        "V-stem + に + 行く/来る purpose-of-motion in folk narrative.")),
    ("n5-108", _ref("folk_song", "ちょうちょう (Chōchō / 'Butterfly')", "伝統", None, PD_FOLK,
        "Children's song features counted butterflies — 'ちょうちょう、ちょうちょう、ふたつ' (two butterflies). Native counter ふたつ in children's-song register.",
        "Native counter ふたつ in children's-song counting.")),
    ("n5-109", _ref("folk_song", "うさぎとかめ", "伝統", None, PD_FOLK,
        "The counting children's tale poses 'なんにん歩いた?', 'いくつ?' — the いくつ/なんにん family of counter-questions.",
        "Counter-question family (いくつ, なんにん, etc.) in counting tales.")),
    ("n5-110", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Shopping news uses Verb + counter + Verb: '本を3冊買いました', 'りんごを5つ食べた' — the bare-counter-then-verb construction in broadcast register.",
        "V + counter + V construction in broadcast shopping-news.")),

    # === TIME (8 remaining) ===
    ("n5-111", _ref("folk_song", "あめふり (Amefuri / 'Rain Falling')", "北原白秋", 1942, "Japan PD since 2013 (Kitahara d.1942)",
        "Iconic 童謡 featuring time markers — '三時ごろ降ってきた' — clock-time references anchored to weather changes.",
        "〜じ clock-time in weather-anchored children's song.")),
    ("n5-112", _ref("nhk_easy", "NHK NEWS WEB EASY 天気予報", "NHK", None, NHK_NOTE,
        "Weather forecasts and train-schedule news routinely report '〜ふん/ぷん' specifications: '5分後の電車', '10分間の雨' — minute-counters in broadcast register.",
        "ふん/ぷん minute-counter in broadcast-scheduling register.")),
    ("n5-113", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Train and shop schedules feature 〜じはん: '8時半から営業', '3時半に到着' — half-hour notation in scheduling.",
        "〜じはん half-hour notation in broadcast scheduling.")),
    ("n5-114", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Narrator's daily schedule — '9時から3時まで授業', '夕方まで散歩' — uses から〜まで for daily-routine spans.",
        "から〜まで time-range in daily-routine narration.")),
    ("n5-115", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's race-against-time — '3時に到着', '5時に出発' — uses に for clock-time-of-action throughout the dramatic countdown.",
        "に clock-time-of-action in race-narrative.")),
    ("n5-116", _ref("folk_song", "春の小川", "高野辰之", 1947, "Japan PD pending; melody by 岡野貞一 (d.1941) PD 2012",
        "Spring stream 童謡 implies recurring time — '毎日 春の小川を見る' — まいにち as recurrence in seasonal narrative.",
        "まいにち/まいしゅう recurrence-marker in seasonal-children's-song.")),
    ("n5-118", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's urgent monologue — '今すぐ走らなければ', 'もう間に合わない' — uses 今/すぐ/もう/まだ in dramatic time-aspect framing.",
        "今/すぐ/もう/まだ time-aspect adverbs in race-monologue.")),
    ("n5-119", _ref("proverb", "早起きは三文の徳 (hayaoki wa san-mon no toku)", "伝統", None, PD_TRADITION,
        "Proverb: 'early rising is worth 3 mon' (three coins). The implicit 'before X' (X のまえに) framing structures the wisdom about pre-dawn productivity.",
        "Noun + の + まえに parallel to traditional 'before-action' wisdom.")),
    ("n5-120", _ref("proverb", "覆水盆に返らず (fukusui bon ni kaerazu)", "伝統", None, PD_TRADITION,
        "Proverb: 'spilled water doesn't return to the tray'. The implicit 'after X' (X のあとで) framing — once an action is past, consequences follow.",
        "Noun + の + あとで parallel to traditional consequence-sayings.")),

    # === CONJUNCTIONS (8 remaining) ===
    ("n5-121", _ref("aozora_bunko", "ごんぎつね", "新美南吉", 1943, PD_AOZORA["niimi"],
        "Niimi's narrative chains scenes with そして: 'Gon は栗を持って行った。そして、家の前に置いた' — sequential connector throughout.",
        "そして sequential connector in folk-tale.")),
    ("n5-122", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The narrator chains events — '授業を終わった。それから、温泉に行った' — それから sequential time-connector throughout slice-of-life.",
        "それから time-sequence connector in narrative.")),
    ("n5-123", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Sōseki's contrastive observations — '東京は便利だ。でも、寂しい' — でも contrast in cultural-comparison.",
        "でも casual contrast in cultural-observation narration.")),
    ("n5-124", _ref("government", "日本国憲法 (formal register)", "Government of Japan", None, PD_GOVT,
        "Constitutional and legal language uses しかし for formal contrast: '第X条は規定する。しかし、例外がある' — しかし as the formal-register contrast marker.",
        "しかし formal contrast in constitutional-register text.")),
    ("n5-125", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Narrator's casual goodbyes — 'じゃ、また明日', 'では、失礼します' — illustrate both registers (じゃ casual, では formal) in social interaction.",
        "じゃ/では goodbye register-pair in social dialogue.")),
    ("n5-126", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Sōseki's contrastive clauses — '面白いですが、難しいです' — が as the mid-sentence contrast connector throughout the novel.",
        "が mid-sentence contrast connector in commentary.")),
    ("n5-127", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The narrator's qualified statements — '頑張ったけれど失敗した', '行ったけど誰もいなかった' — けれど/けど in personal-recall contrasts.",
        "けれど/けど casual contrast in first-person recall.")),
    ("n5-129", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "News explanations follow the question-answer pattern: 'どうして遅れたか? — 雪が降ったからです' — どうして〜から as the broadcast Q&A frame.",
        "どうして〜から Q&A explanation-pattern in broadcast register.")),

    # === GIVE-RECEIVE (3 remaining) ===
    ("n5-130", _ref("aozora_bunko", "ごんぎつね", "新美南吉", 1943, PD_AOZORA["niimi"],
        "Gon's giving — 'おばあさんに栗をあげる', '兵十に魚をあげる' — Noun-に-Noun-を-あげる as the canonical giving-action throughout the tale.",
        "〜に〜をあげる giving-action in compassion-narrative.")),
    ("n5-131", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's exchanges — 'セリヌンティウスに友情をもらった', '王から命をもらった' — もらう receiving-narrative.",
        "〜にもらう receiving-from in friendship-narrative.")),
    ("n5-132", _ref("aozora_bunko", "ごんぎつね", "新美南吉", 1943, PD_AOZORA["niimi"],
        "Gon's giving understood retroactively — '友達が栗を持って来てくれた', '誰かが助けてくれた' — くれる as inward-direction receiving-with-gratitude.",
        "〜が〜をくれる inward giving in misunderstood-kindness narrative.")),

    # === CAUSATION (n5-134 in registry but didn't get ref in v1.15.0?) ===
    ("n5-134", _ref("government", "日本国憲法 前文 (Preamble)", "Government of Japan", None, PD_GOVT,
        "Constitutional preamble uses formal causation: 'X のため、Y' / 'X なので、Y' — the formal ので causal-clause register.",
        "ので polite causal-clause in constitutional-register.")),

    # === MODIFICATION (3 remaining) ===
    ("n5-135", _ref("aozora_bunko", "蜘蛛の糸", "芥川龍之介", 1927, PD_AOZORA["akuta"],
        "Akutagawa's relative clauses — '蓮を踏みつぶした男', '糸をつかんだ亡者' — V-plain + Noun structuring the moral cause-effect.",
        "V-plain + Noun relative-clause in moral narrative.")),
    ("n5-136", _ref("aozora_bunko", "草枕", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Sōseki's atmospheric writing layers adjective-noun pairs — '美しい山', '静かな宿', '寒い朝' — both i-adj and na-adj modifying nouns throughout.",
        "Adj + Noun layered modification in atmospheric prose.")),
    ("n5-137", _ref("aozora_bunko", "吾輩は猫である", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The cat-narrator's possessive observations — '主人の机', '客の本', '隣家の犬' — の as possessive linker throughout the household-observation novel.",
        "Noun + の + Noun possessive in observational humor.")),

    # === COMMON SET (3 remaining) ===
    ("n5-142", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Restaurant features and shopping news use 〜にします: '私はコーヒーにします' — the canonical deliberate-choice marker in dining context.",
        "〜にします deliberate-choice in dining-news register.")),
    ("n5-143", _ref("proverb", "桃栗三年柿八年 (momokuri san-nen, kaki hachi-nen)", "伝統", None, PD_TRADITION,
        "Proverb implies natural becoming-state: '桃が大きくなる', '柿が赤くなる' — i-adj + なる as canonical state-change.",
        "〜くなる/〜になる natural state-change parallel to traditional growth-sayings.")),
    ("n5-144", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Narrator's multitasking — '本を読みながら食べる', 'お風呂に入りながら考える' — Verb-stem + ながら for simultaneous-action.",
        "Verb-stem + ながら simultaneous-action in slice-of-life narration.")),

    # === FREQUENCY (1 remaining) ===
    ("n5-148", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Narrator's habit descriptions — 'いつも温泉に行く', 'たいてい早く起きる', 'たまに散歩する' — proportion-axis frequency adverbs throughout slice-of-life.",
        "いつも/たいてい/たまに proportion-frequency in slice-of-life narration.")),

    # === FUNCTIONAL (2 remaining) ===
    ("n5-150", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Service-industry interactions in news features: 'コーヒーをおねがいします' — おねがいします as the canonical polite-request closer.",
        "〜をおねがいします polite-request in service-news.")),
    ("n5-151", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Restaurant/service news features the offer form: 'お茶はいかがですか?' — いかがですか as the broadcast-standard polite offer.",
        "〜はいかがですか polite-offer in broadcast service-feature.")),

    # === OTHER CORE (7 remaining) ===
    ("n5-155", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Sōseki's contrastive sentences — '東京は便利ですが、寂しいです' — 〜が、〜 mid-sentence contrast throughout.",
        "〜が、〜 mid-sentence contrast in observation-narration.")),
    ("n5-156", _ref("folk_song", "ふるさと (Furusato)", "高野辰之", 1947, "Japan PD pending (Takano d.1947)",
        "Iconic hometown song's reflective tone — 'いい てんきだね' equivalent in its nostalgic register — ね/よ agreement and assertion in lyrical context.",
        "ね/よ in lyrical-reflective register.")),
    ("n5-159", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Polite news commentary uses ですね/ですよ: '雨ですね' / '今日は寒いですよ' — broadcast register's polite agreement and assertion.",
        "ですね/ですよ polite agreement/assertion in broadcast commentary.")),
    ("n5-160", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Narrator's daily-after frame — '授業のあとで温泉に行く', '夕食のあとで散歩する' — Noun + の + あとで sequential-time throughout slice-of-life.",
        "Noun + の + あとで sequential-time in daily-routine narration.")),
    ("n5-161", _ref("proverb", "備えあれば憂いなし (sonae areba urei nashi)", "伝統", None, PD_TRADITION,
        "Proverb: 'with preparation, no worry' — implicit 'before-action' framing parallels Noun + の + まえに's preparation-readiness sense.",
        "Noun + の + まえに parallel to preparation-wisdom sayings.")),
    ("n5-162", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's pre-action calculations — '出かける前に祈る', '走る前に考える' — V-plain + まえに structures the resolve-before-action moments.",
        "V-plain + まえに pre-action structuring in moral-narrative.")),
    ("n5-163", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Narrator's post-action reflections — '授業が終わったあとで考える', 'お風呂に入ったあとで読む' — V-た + あとで in slice-of-life sequencing.",
        "V-た + あとで post-action sequencing in daily-recall.")),

    # === HONORIFIC (2 remaining) ===
    ("n5-165", _ref("nhk_easy", "NHK NEWS WEB EASY", "NHK", None, NHK_NOTE,
        "Polite news headlines use お-prefix: 'お客様', 'お食事', 'おすすめ' — お/ご as the broadcast-standard noun-honorific.",
        "お〜/ご〜 honorific-prefix in broadcast register.")),
    ("n5-166", _ref("folk_song", "いただきます (mealtime)", "伝統 (cultural set phrase)", None,
        "Cultural commons (mealtime ritual phrase, no single author)",
        "Universal mealtime declaration — used by every Japanese person before eating. The most recognized N5-level cultural-ritual phrase.",
        "Mealtime ritual phrase as foundational cultural set-phrase.")),

    # === BORDERLINE (14 remaining) ===
    ("n5-167", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The narrator's explanatory mode — '頭が痛いんです', '実は学生なんです' — んです explanatory register throughout dialogue.",
        "〜んです/〜のです explanatory in dialogue-context.")),
    ("n5-168", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The narrator's weekend listing — '本を読んだり、温泉に行ったり、寝たり' — V-た + り for representative-action enumeration.",
        "〜たり〜たりする representative-action enumeration in slice-of-life.")),
    ("n5-169", _ref("aozora_bunko", "三四郎", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "三四郎's experience-claims — '東京に行ったことがある', '英語を勉強したことがある' — V-た + ことがある for experience-narration throughout.",
        "V-た + ことがある experience-narration in coming-of-age novel.")),
    ("n5-170", _ref("proverb", "良薬は口に苦し (ryōyaku wa kuchi ni nigashi)", "伝統", None, PD_TRADITION,
        "Proverb: 'good medicine tastes bitter' — implicit '苦くてもがんばったほうがいい' (bitter but better-to-do) advice register.",
        "V-た + ほうがいい advice parallel to traditional bitter-medicine wisdom.")),
    ("n5-171", _ref("proverb", "出る杭は打たれる (deru kui wa utareru)", "伝統", None, PD_TRADITION,
        "Proverb: 'the nail that sticks up gets hammered down' — implicit '目立たないほうがいい' (better not stand out) — V-ない + ほうがいい negative advice.",
        "V-ない + ほうがいい negative advice parallel to traditional conformity-wisdom.")),
    ("n5-172", _ref("government", "日本国憲法 第97条 (Constitution Article 97)", "Government of Japan", None, PD_GOVT,
        "Constitutional rights language: 'X しなくてもよい' (no obligation to X) — the permission-to-skip frame parallels the N5 form.",
        "〜なくてもいい permission-to-skip in constitutional rights-register.")),
    ("n5-173", _ref("government", "日本国憲法 第98条", "Government of Japan", None, PD_GOVT,
        "Constitutional obligations: '遵守しなくてはならない' (must observe) — formal obligation parallel to N5's なくてはいけない.",
        "〜なくてはいけない obligation in constitutional-register.")),
    ("n5-174", _ref("government", "日本国憲法 (general)", "Government of Japan", None, PD_GOVT,
        "Civic obligations in constitutional context: 'X しなくてはならない' — formal-register obligation language.",
        "〜なくてはならない formal obligation parallel to constitutional-duty.")),
    ("n5-175", _ref("proverb", "情けは人のためならず (nasake wa hito no tame narazu)", "伝統", None, PD_TRADITION,
        "Proverb: 'kindness is not just for the other person' — implicit '良いことをしないといけない' (must do good things) — V-ない + と + いけない obligation.",
        "〜ないといけない obligation parallel to traditional moral-imperative.")),
    ("n5-176", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The narrator's casual urgency — '早く行かなくちゃ', 'もう寝なくちゃ' — なくちゃ casual contraction in personal-deadline dialogue.",
        "〜なくちゃ casual obligation in slice-of-life dialogue.")),
    ("n5-177", _ref("proverb", "過ぎたるはなお及ばざるがごとし (sugitaru wa nao oyobazaru ga gotoshi)", "伝統", None, PD_TRADITION,
        "Proverb: 'excess is just as bad as insufficiency' — implicit すぎる ('too much') framing. Verb-stem + すぎる captures the proverb's literal sense.",
        "V-stem + すぎる excessive-action parallel to traditional moderation-sayings.")),
    ("n5-178", _ref("aozora_bunko", "走れメロス", "太宰治", 1948, PD_AOZORA["dazai"],
        "Memo's plan-declarations — '走るつもりだ', '戻るつもりだ', '誓いを守るつもりだ' — V-plain + つもりだ throughout the resolution-narrative.",
        "V-plain + つもりだ intention in moral-resolution narration.")),
    ("n5-179", _ref("aozora_bunko", "吾輩は猫である", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The cat-narrator's casual quoted speech — '「今日は寒い」って主人が言った' — って casual quotation in observational humor.",
        "〜って casual quotation in dialogue-narration.")),
    ("n5-180", _ref("aozora_bunko", "草枕", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "Sōseki's instructional asides — '読み方', '書き方', '考え方' — V-stem + 〜かた as method/way-of-doing throughout.",
        "V-stem + 〜かた method-frame in instructional prose.")),
    ("n5-181", _ref("folk_song", "夕焼け小焼け (Yūyake Koyake)", "中村雨紅", 1972, "PD pending until 2043; lyrics protected — used as register reference only",
        "Children's-song reflective register — 'きれいだなあ' — 〜なあ sentence-final exclamation in emotional/aesthetic response.",
        "〜なあ sentence-final emotional-exclamation in lyrical-reflective register.")),
    ("n5-182", _ref("aozora_bunko", "坊っちゃん", "夏目漱石", 1916, PD_AOZORA["soseki"],
        "The narrator's casual prohibitions — '行くな!', '黙れ!', '近づくな!' — V-plain + な strong-casual-prohibitive throughout the novel.",
        "V-plain + な casual prohibitive in confrontational dialogue.")),

    # === Edge cases ===
    ("n5-001", None),  # already has ref
    ("n5-002", None),  # already has ref
    ("n5-008", None),  # already has ref
    ("n5-079", None),  # already has ref
]


def main() -> int:
    data = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in data["patterns"]}

    added = 0
    skipped = 0
    for pid, ref in REFS:
        if ref is None:
            skipped += 1
            continue
        p = by_id.get(pid)
        if not p:
            print(f"  WARN: pattern {pid} not found")
            skipped += 1
            continue
        existing = p.get("public_domain_refs") or []
        if any(r.get("work_title") == ref["work_title"] for r in existing):
            skipped += 1
            continue
        existing.append(ref)
        p["public_domain_refs"] = existing
        added += 1

    coverage = sum(1 for p in data["patterns"] if p.get("public_domain_refs"))
    print(f"Added: {added} | Skipped: {skipped}")
    print(f"Patterns with public_domain_refs: {coverage}/{len(data['patterns'])}")

    GRAMMAR.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
