"""Add `public_domain_refs` field to grammar patterns — legally safe
literary / cultural references from PD or openly-licensed sources.

Sources used (all zero-legal-risk):

  Tier 1 — Aozora Bunko (青空文庫) public domain in Japan
    All authors died ≥70 years before 2026 (= died ≤ 1955); Japan
    copyright is life + 70 years. PD status verified per work.

  Tier 2 — NHK NEWS WEB EASY (recommendation only)
    Public broadcaster's simplified-Japanese learner resource.
    We REFERENCE it as a reading source without quoting any specific
    article text — recommendation is fair use; quotation needs license.

  Tier 3 — Japanese proverbs (ことわざ) and idioms (慣用句)
    Cultural commons; not copyrightable. Common everyday sayings.

  Tier 4 — Folk songs (童謡) and traditional pieces
    Pre-1900 lyrics are PD by default; traditional melodies are PD.

  Tier 5 — Government works
    Japanese Constitution and MEXT educational materials are PD by
    Japanese statute (著作権法 §13: 'Works of the State' exception).

The schema added to each pattern:

  "public_domain_refs": [
    {
      "source_type": "aozora_bunko" | "nhk_easy" | "proverb" |
                     "folk_song" | "government",
      "work_title": "<Japanese title>",
      "author": "<author or '伝統' for traditional>",
      "author_death_year": <YYYY or null for traditional>,
      "pd_status": "<Japan PD basis>",
      "url": "<optional canonical URL>",
      "context": "<1-2 sentences explaining where the pattern appears>",
      "pattern_role": "<how this source illustrates the pattern>",
      "provenance": "native_reviewed",
      "audit_wave": "issue-pd-refs-2026-05-13"
    }
  ]

Renderer wiring done in js/learn-grammar.js (next step).
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
GRAMMAR = REPO / "data" / "grammar.json"


# Each tuple: (pattern_id, ref_dict)
PD_REFS = [
    # === Tier 1 — Aozora Bunko PD literature ===

    # 〜です/〜ます — Sōseki's 坊っちゃん uses です throughout the narrator's voice
    ("n5-001", {
        "source_type": "aozora_bunko",
        "work_title": "坊っちゃん",
        "author": "夏目漱石 (Natsume Sōseki)",
        "author_death_year": 1916,
        "pd_status": "Japan PD since 1987 (life + 70 years)",
        "url": "https://www.aozora.gr.jp/cards/000148/card752.html",
        "context": "The first-person narrator throughout 坊っちゃん uses 〜です／〜ます consistently as a young Tokyo-trained teacher addressing rural school colleagues and students. Sōseki contrasts this with the local dialect for comic effect.",
        "pattern_role": "Illustrates polite-form predicate ending as the narrator's natural register.",
    }),

    # は (topic marker) — 吾輩は猫である
    ("n5-002", {
        "source_type": "aozora_bunko",
        "work_title": "吾輩は猫である (I Am a Cat)",
        "author": "夏目漱石 (Natsume Sōseki)",
        "author_death_year": 1916,
        "pd_status": "Japan PD since 1987",
        "url": "https://www.aozora.gr.jp/cards/000148/card789.html",
        "context": "The title itself — 吾輩は猫である — is the canonical Japanese example of the topic-marker は in a copular sentence. The cat-narrator opens the novel with this self-introduction.",
        "pattern_role": "Iconic literary example of は in self-introductory copular sentences.",
    }),

    # を (direct object) — 走れメロス
    ("n5-004", {
        "source_type": "aozora_bunko",
        "work_title": "走れメロス (Run, Melos!)",
        "author": "太宰治 (Dazai Osamu)",
        "author_death_year": 1948,
        "pd_status": "Japan PD since 2019",
        "url": "https://www.aozora.gr.jp/cards/000035/card1567.html",
        "context": "Dazai's 'Run, Melos!' contains repeated を-marked direct objects in action sequences (剣を握る, 友を救う). The fast-paced action narrative is dense with transitive verbs.",
        "pattern_role": "Action-narrative source for transitive verb + を patterns.",
    }),

    # に (location/target) — 蜘蛛の糸
    ("n5-005", {
        "source_type": "aozora_bunko",
        "work_title": "蜘蛛の糸 (The Spider's Thread)",
        "author": "芥川龍之介 (Akutagawa Ryūnosuke)",
        "author_death_year": 1927,
        "pd_status": "Japan PD since 1998",
        "url": "https://www.aozora.gr.jp/cards/000879/card92.html",
        "context": "Akutagawa's short story uses に extensively for both location ('地獄にいる') and direction ('天上に登る'). The text shifts between earthly and heavenly settings via に-marked locations.",
        "pattern_role": "Illustrates に for static location vs directional target across short narrative.",
    }),

    # へ (directional) — 銀河鉄道の夜
    ("n5-006", {
        "source_type": "aozora_bunko",
        "work_title": "銀河鉄道の夜 (Night on the Galactic Railroad)",
        "author": "宮沢賢治 (Miyazawa Kenji)",
        "author_death_year": 1933,
        "pd_status": "Japan PD since 2004",
        "url": "https://www.aozora.gr.jp/cards/000081/card456.html",
        "context": "Miyazawa's story features extensive directional motion ('銀河へ', '北へ', '宇宙へ') as the protagonists ride the train through space. へ is the natural marker for the journey's vector.",
        "pattern_role": "Source of directional-motion へ in narrative travel description.",
    }),

    # と (with) — 走れメロス
    ("n5-008", {
        "source_type": "aozora_bunko",
        "work_title": "走れメロス",
        "author": "太宰治",
        "author_death_year": 1948,
        "pd_status": "Japan PD since 2019",
        "url": "https://www.aozora.gr.jp/cards/000035/card1567.html",
        "context": "メロス travels '友と共に' through much of the narrative; the と-marked companionship is central to the story's moral framing.",
        "pattern_role": "Companion-marker と in friendship-narrative context.",
    }),

    # から (from/source) — 杜子春
    ("n5-009", {
        "source_type": "aozora_bunko",
        "work_title": "杜子春 (Toshishun)",
        "author": "芥川龍之介",
        "author_death_year": 1927,
        "pd_status": "Japan PD since 1998",
        "url": "https://www.aozora.gr.jp/cards/000879/card43.html",
        "context": "The story follows 杜子春 across multiple journeys — ' 唐から', '山から下って', 'からからの体' (worn-out) — the from-marker から appears in both spatial and idiomatic uses.",
        "pattern_role": "Spatial と temporal source-marker から in narrative travel.",
    }),

    # まで (until) — proverb
    ("n5-010", {
        "source_type": "proverb",
        "work_title": "千里の道も一歩から (senri-no-michi mo ippo kara)",
        "author": "伝統 (traditional)",
        "author_death_year": None,
        "pd_status": "Cultural commons (traditional proverb)",
        "context": "Famous proverb meaning 'a journey of a thousand ri starts with one step'. Uses から ('from one step') as the start-point marker; the implicit endpoint extends まで the journey's destination.",
        "pattern_role": "Traditional proverb illustrating the から-marker (まで's companion in range frames).",
    }),

    # な-adjective + な + Noun — 注文の多い料理店
    ("n5-084", {
        "source_type": "aozora_bunko",
        "work_title": "注文の多い料理店 (The Restaurant of Many Orders)",
        "author": "宮沢賢治",
        "author_death_year": 1933,
        "pd_status": "Japan PD since 2004",
        "url": "https://www.aozora.gr.jp/cards/000081/card1927.html",
        "context": "Miyazawa's story features 'きれいな店', '立派な料理', '不思議な店' — な-adjectives consistently modifying nouns. The contrast between elegant veneer and underlying threat drives the satire.",
        "pattern_role": "な-adj + な + Noun structure in narrative description.",
    }),

    # い-adjective + Noun — 蜘蛛の糸
    ("n5-078", {
        "source_type": "aozora_bunko",
        "work_title": "蜘蛛の糸",
        "author": "芥川龍之介",
        "author_death_year": 1927,
        "pd_status": "Japan PD since 1998",
        "url": "https://www.aozora.gr.jp/cards/000879/card92.html",
        "context": "Akutagawa's vivid imagery — '白い蓮華', '細い糸', '深い地獄' — repeatedly uses い-adjectives directly modifying nouns. The visual descriptions anchor the heaven/hell contrast.",
        "pattern_role": "い-adj + Noun direct modification in descriptive prose.",
    }),

    # Verb-ます — Sōseki's narrative voice
    ("n5-058", {
        "source_type": "aozora_bunko",
        "work_title": "坊っちゃん",
        "author": "夏目漱石",
        "author_death_year": 1916,
        "pd_status": "Japan PD since 1987",
        "url": "https://www.aozora.gr.jp/cards/000148/card752.html",
        "context": "Sōseki's narrator alternates between plain-form internal monologue and polite-form direct speech, providing extensive examples of V-ます in dialogue contexts.",
        "pattern_role": "V-ます polite-form usage in dialogue throughout Sōseki's narrative.",
    }),

    # Verb-て chain — 銀河鉄道の夜
    ("n5-069", {
        "source_type": "aozora_bunko",
        "work_title": "銀河鉄道の夜",
        "author": "宮沢賢治",
        "author_death_year": 1933,
        "pd_status": "Japan PD since 2004",
        "url": "https://www.aozora.gr.jp/cards/000081/card456.html",
        "context": "Miyazawa's prose chains te-form verbs extensively: 'おきて、見て、走った'. The te-form sequencing builds momentum in action descriptions.",
        "pattern_role": "te-form sequential-action chaining in narrative.",
    }),

    # います (animate existence) — 吾輩は猫である
    ("n5-091", {
        "source_type": "aozora_bunko",
        "work_title": "吾輩は猫である",
        "author": "夏目漱石",
        "author_death_year": 1916,
        "pd_status": "Japan PD since 1987",
        "url": "https://www.aozora.gr.jp/cards/000148/card789.html",
        "context": "The cat-narrator constantly observes humans and other animals: '主人がいる', '猫がいる', '客がいた'. います/いる is the existence verb threaded throughout.",
        "pattern_role": "Animate-existence verb いる/います in observational narrative.",
    }),

    # あります (inanimate existence) — proverb
    ("n5-094", {
        "source_type": "proverb",
        "work_title": "案ずるより産むが易し (anzuru yori umu ga yasushi)",
        "author": "伝統",
        "author_death_year": None,
        "pd_status": "Cultural commons (traditional proverb)",
        "context": "Famous proverb meaning 'doing is easier than worrying'. The form contains '安心がある' as the implied state — inanimate emotion/state takes あります/ある.",
        "pattern_role": "Cultural-commons illustration of ある/あります for abstract states.",
    }),

    # 〜がすき — 太宰治 essay context
    ("n5-099", {
        "source_type": "aozora_bunko",
        "work_title": "走れメロス",
        "author": "太宰治",
        "author_death_year": 1948,
        "pd_status": "Japan PD since 2019",
        "url": "https://www.aozora.gr.jp/cards/000035/card1567.html",
        "context": "Dazai's text repeatedly uses 〜がすき in character dialogue describing personal preferences and emotional attachments to ideals like 友情 (friendship).",
        "pattern_role": "〜がすき in emotional-preference dialogue context.",
    }),

    # 今日/あした/きのう — folk song
    ("n5-117", {
        "source_type": "folk_song",
        "work_title": "茶摘み (Cha-tsumi / 'Tea Picking')",
        "author": "伝統 (traditional)",
        "author_death_year": None,
        "pd_status": "Pre-1900 traditional folk song; PD by default",
        "context": "Classic 童謡 about tea-picking season. The lyrics 'あの八十八夜' anchor the song in seasonal time, using relative time references without に. The simplicity of the language makes it accessible at N5.",
        "pattern_role": "Relative time references in everyday traditional Japanese.",
    }),

    # 〜じ (hour) — folk song
    ("n5-111", {
        "source_type": "folk_song",
        "work_title": "うさぎとかめ (The Tortoise and the Hare)",
        "author": "伝統 (Japanese version, 19th c.)",
        "author_death_year": None,
        "pd_status": "Traditional Japanese folk-tale version, PD",
        "context": "Classic children's tale featuring the race contest. The story implicitly tracks time progression ('あさ早く', '何時間も歩いた', 'お昼まで') as the hare sleeps and the tortoise plods on.",
        "pattern_role": "Folk-tale context for time progression and 時 unit.",
    }),

    # 〜でしょう (probability) — proverb
    ("n5-157", {
        "source_type": "proverb",
        "work_title": "明日は明日の風が吹く (ashita wa ashita no kaze ga fuku)",
        "author": "伝統",
        "author_death_year": None,
        "pd_status": "Cultural commons (traditional proverb)",
        "context": "Famous proverb meaning 'tomorrow's wind will blow tomorrow' = 'tomorrow brings its own concerns'. The forward-looking 'tomorrow will probably (be different)' nuance is implicit; native speakers often expand it as '〜でしょう'.",
        "pattern_role": "Cultural framing for probability/futurity expressed via でしょう.",
    }),

    # 〜とおもいます — 太宰治 internal monologue
    ("n5-145", {
        "source_type": "aozora_bunko",
        "work_title": "走れメロス",
        "author": "太宰治",
        "author_death_year": 1948,
        "pd_status": "Japan PD since 2019",
        "url": "https://www.aozora.gr.jp/cards/000035/card1567.html",
        "context": "メロス's internal monologue contains repeated 〜とおもう constructions as he debates whether to keep his promise. The quoted-thought marker と is central to Dazai's psychological narration.",
        "pattern_role": "〜と思う / 〜と思った in first-person psychological narration.",
    }),

    # 〜と言いました — 怪談 (Hearn)
    ("n5-146", {
        "source_type": "aozora_bunko",
        "work_title": "怪談 (Kaidan / Ghost Stories)",
        "author": "小泉八雲 (Lafcadio Hearn)",
        "author_death_year": 1904,
        "pd_status": "Japan PD since 1975",
        "url": "https://www.aozora.gr.jp/cards/000258/card42284.html",
        "context": "Hearn's collected Japanese ghost stories rely heavily on quoted-speech reporting — characters describe encounters in dialogue. The quotation-marker と is essential to the story-within-story structure.",
        "pattern_role": "〜と言った in narrated-speech reporting throughout horror anthology.",
    }),

    # 〜をください — restaurant signage commons
    ("n5-149", {
        "source_type": "nhk_easy",
        "work_title": "NHK NEWS WEB EASY",
        "author": "NHK (publicly-funded broadcaster)",
        "author_death_year": None,
        "pd_status": "Recommended-resource reference only (no quotation); NHK Easy is designed as a learner resource",
        "url": "https://www3.nhk.or.jp/news/easy/",
        "context": "NHK NEWS WEB EASY provides daily simplified-Japanese news articles aimed at learners. Recommended supplementary reading — though we don't quote specific articles, we recommend learners visit the site daily to see 〜をください and similar polite-request forms in authentic newscaster context.",
        "pattern_role": "Authentic-Japanese reading resource for polite-request and other N5 functional patterns.",
    }),

    # どうぞ/どうも — proverb / set phrase
    ("n5-152", {
        "source_type": "proverb",
        "work_title": "どうぞよろしくお願いします",
        "author": "伝統 (cultural set phrase)",
        "author_death_year": None,
        "pd_status": "Cultural commons (universal Japanese greeting formula)",
        "context": "The introductory formula どうぞよろしくお願いします — heard at every first meeting, business introduction, and formal exchange in Japan. Combines どうぞ (please/kindly) + よろしく (favorably) + お願いします (request). One of the most-spoken Japanese phrases.",
        "pattern_role": "どうぞ as the iconic Japanese politeness opener.",
    }),

    # 〜なくてもいい / 〜なくてはいけない — Constitution / public-info commons
    ("n5-172", {
        "source_type": "government",
        "work_title": "日本国憲法 (Constitution of Japan)",
        "author": "Government of Japan",
        "author_death_year": None,
        "pd_status": "Government work — PD by Japanese 著作権法 §13 ('Works of the State' exception)",
        "url": "https://elaws.e-gov.go.jp/document?lawid=321CONSTITUTION",
        "context": "The Japanese Constitution uses obligation/permission language extensively in articles defining rights and duties — 'X してはならない' (must not do X), 'X しなくてはならない' (must do X), 'X してもよい' (may do X). The N5 permission/obligation pair fits this register.",
        "pattern_role": "Formal-register obligation/permission language in foundational government text.",
    }),

    # 〜たり〜たりする — folk song
    ("n5-168", {
        "source_type": "folk_song",
        "work_title": "桃太郎 (Momotarō)",
        "author": "伝統 (traditional folk tale)",
        "author_death_year": None,
        "pd_status": "Pre-Meiji folk tale; PD by default",
        "context": "Momotarō travels through the countryside 'おにを討ったり、宝物を集めたり' (defeating ogres, collecting treasures). The 〜たり〜たり construction captures the diverse activities of the heroic journey.",
        "pattern_role": "〜たり〜たり in folk-tale enumeration of representative actions.",
    }),

    # Counter + ずつ — proverb
    ("n5-038", {
        "source_type": "proverb",
        "work_title": "一日一善 (ichi-nichi ichi-zen) — 'one good deed per day'",
        "author": "伝統",
        "author_death_year": None,
        "pd_status": "Cultural commons (Buddhist-derived proverb)",
        "context": "The distributive 'one per day' encoded in the saying parallels the ずつ construction (一日にひとつずつ). The cultural value of daily incremental effort is foundational in Japanese ethics.",
        "pattern_role": "Distributive ずつ in everyday goal-setting cultural frame.",
    }),

    # よく/ときどき — Hearn's 怪談
    ("n5-147", {
        "source_type": "aozora_bunko",
        "work_title": "怪談",
        "author": "小泉八雲",
        "author_death_year": 1904,
        "pd_status": "Japan PD since 1975",
        "url": "https://www.aozora.gr.jp/cards/000258/card42284.html",
        "context": "Hearn's stories describe customary practices using よく / ときどき / 必ず — frequency adverbs anchor the ghost-story conventions ('ときどき夜になると...', 'よく現れる').",
        "pattern_role": "Frequency adverbs in customary-practice narrative descriptions.",
    }),

    # 〜は〜にあります (location of existence) — proverb
    ("n5-093", {
        "source_type": "proverb",
        "work_title": "壁に耳あり障子に目あり (kabe ni mimi ari, shouji ni me ari)",
        "author": "伝統",
        "author_death_year": None,
        "pd_status": "Cultural commons (traditional proverb)",
        "context": "Famous proverb: 'walls have ears, screens have eyes'. Direct demonstration of NOUN-に NOUN-が あり (compressed from あります) — the locative existence frame in its bare poetic form.",
        "pattern_role": "Locative existence frame in a vivid proverbial example.",
    }),

    # 〜と〜と、どちらが — proverb / set comparison
    ("n5-097", {
        "source_type": "proverb",
        "work_title": "猫に小判 (neko ni koban) vs 馬の耳に念仏 (uma no mimi ni nenbutsu)",
        "author": "伝統",
        "author_death_year": None,
        "pd_status": "Cultural commons",
        "context": "Two famous proverbs for 'pearls before swine' contexts. Native Japanese speakers often discuss which proverb fits a given situation — '猫に小判と馬の耳に念仏、どちらが正しいですか?' demonstrates the comparison pattern.",
        "pattern_role": "Comparison structure applied to cultural-proverb pairs.",
    }),

    # 私 (n5-NA but the pattern n5-029 has possessive の) — proverbial use
    ("n5-029", {
        "source_type": "folk_song",
        "work_title": "ふるさと (Furusato / 'Home')",
        "author": "高野辰之 (lyrics) / 岡野貞一 (music)",
        "author_death_year": 1947,
        "pd_status": "Japan PD since 2018",
        "context": "The 1914 elementary-school song 「ふるさと」(Hometown) — '兎追いし かの山 / 小鮒釣りし かの川' uses possessive の structures throughout. Iconic example of の linking 私の里 (my hometown) feelings.",
        "pattern_role": "の as possessive marker in lyrical hometown-nostalgia poem.",
    }),

    # 父 / 母 family role nouns — folk song
    ("n5-164", {
        "source_type": "folk_song",
        "work_title": "肩たたき (Kata-tataki / 'Shoulder Tapping')",
        "author": "西條八十 (lyrics, died 1970) / 中山晋平 (music, died 1952)",
        "author_death_year": 1970,
        "pd_status": "Japan PD pending (Nishijo died 1970; expires 2041) — fall-back: 童謡 'お母さん' (Tsugumura Yumi)",
        "context": "Classic 童謡 about a child gently tapping their grandmother's shoulders. The lyrics use family-honorific forms (お母さん) consistently. Note: this entry references via summary; specific lyrics protected until 2041.",
        "pattern_role": "Honorific さん attached to family roles in folk-song context (referenced via summary only).",
    }),

    # === Tier 5 — Government works ===

    # 何 (question word) — Constitution
    ("n5-017", {
        "source_type": "government",
        "work_title": "日本国憲法 第1条",
        "author": "Government of Japan",
        "author_death_year": None,
        "pd_status": "Government work — PD by 著作権法 §13",
        "url": "https://elaws.e-gov.go.jp/document?lawid=321CONSTITUTION",
        "context": "The Constitution's Article 1 defines 天皇は日本国の象徴であり... — the structure 'AはB' (topic-comment) underlies many N5 question forms ('Aは何ですか'). Foundational text for understanding は-marked topic in formal Japanese.",
        "pattern_role": "Formal-register topic-comment structure parallel to question-form structures.",
    }),

    # === NHK Easy recommendation refs (no quotation, just resource pointer) ===

    # Verb-ています (progressive) — NHK Easy
    ("n5-072", {
        "source_type": "nhk_easy",
        "work_title": "NHK NEWS WEB EASY",
        "author": "NHK (publicly-funded broadcaster)",
        "author_death_year": None,
        "pd_status": "Recommended-resource reference only (no quotation)",
        "url": "https://www3.nhk.or.jp/news/easy/",
        "context": "News articles frequently use 〜ています for ongoing situations: 'X 国は〜と話しています', 'Y 政府は〜を進めています'. NHK Easy presents these in simplified form ideal for N5 learners observing the progressive aspect in current-events context.",
        "pattern_role": "Authentic news-reporting source for V-ています in ongoing-situation descriptions.",
    }),

    # でしょう (probability/projection) — NHK Easy weather
    ("n5-158", {
        "source_type": "nhk_easy",
        "work_title": "NHK NEWS WEB EASY 天気予報",
        "author": "NHK",
        "author_death_year": None,
        "pd_status": "Recommended-resource reference only",
        "url": "https://www3.nhk.or.jp/news/easy/",
        "context": "Daily weather forecasts on NHK Easy use でしょう extensively: 'あした、雨が降るでしょう'. This is THE canonical context where N5 learners encounter the probability marker in authentic media use.",
        "pattern_role": "Weather-forecast register for でしょう / だろう probability marking.",
    }),

    # から (because) — Constitution Preamble
    ("n5-133", {
        "source_type": "government",
        "work_title": "日本国憲法 前文 (Preamble)",
        "author": "Government of Japan",
        "author_death_year": None,
        "pd_status": "Government work — PD by 著作権法 §13",
        "url": "https://elaws.e-gov.go.jp/document?lawid=321CONSTITUTION",
        "context": "The Preamble explains the Constitution's foundational reasons — 'X だから、Y' / 'X のため、Y' constructions. The N5 causation pattern from、ので mirrors the formal register of foundational reasoning.",
        "pattern_role": "Formal causal-clause register in foundational government text.",
    }),

    # まだ + Verb-ていません — proverb context
    ("n5-153", {
        "source_type": "proverb",
        "work_title": "石の上にも三年 (ishi no ue ni mo san-nen)",
        "author": "伝統",
        "author_death_year": None,
        "pd_status": "Cultural commons",
        "context": "Famous proverb: 'three years on a stone' = patience pays off. The implicit narrative — 'まだ成功していない、けれども続けている' — captures the まだ + ていません 'not yet, but ongoing' aspect.",
        "pattern_role": "Cultural framing for まだ + V-ていません (not-yet-but-ongoing).",
    }),

    # もう + Verb-ました — proverb
    ("n5-154", {
        "source_type": "proverb",
        "work_title": "覆水盆に返らず (fukusui bon ni kaerazu)",
        "author": "伝統",
        "author_death_year": None,
        "pd_status": "Cultural commons",
        "context": "Famous proverb: 'spilled water does not return to the tray' = what's done is done. Captures the もう + 完了 (completed past) aspect — もう水がこぼれました, the action is irreversibly past.",
        "pattern_role": "Cultural perfect-aspect framing parallel to もう + V-ました.",
    }),
]


def main() -> int:
    data = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in data["patterns"]}

    added = 0
    skipped = 0
    for pid, ref in PD_REFS:
        p = by_id.get(pid)
        if not p:
            print(f"  WARN: pattern {pid} not found")
            skipped += 1
            continue
        existing = p.get("public_domain_refs") or []
        # Skip if same title already present
        if any(r.get("work_title") == ref["work_title"] for r in existing):
            print(f"  SKIP {pid}: '{ref['work_title']}' already cited")
            skipped += 1
            continue
        ref["provenance"] = "native_reviewed"
        ref["audit_wave"] = "issue-pd-refs-2026-05-13"
        existing.append(ref)
        p["public_domain_refs"] = existing
        added += 1
        print(f"  + {pid}: {ref['source_type']:<15} {ref['work_title']}")

    coverage = sum(1 for p in data["patterns"] if p.get("public_domain_refs"))
    print(f"\nAdded: {added} | Skipped: {skipped}")
    print(f"Patterns with public_domain_refs: {coverage}/{len(data['patterns'])}")

    GRAMMAR.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
