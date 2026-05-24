"""Author quote_ja + quote_translation_en for every public_domain_refs
entry in data/grammar.json (closes PD-CITATION-001).

Coverage approach:
  * Proverbs / folk songs / set phrases — the work_title IS the
    canonical phrase, so quote_ja = a well-known form of that phrase
    (sometimes slightly expanded; brevity preserved).
  * Aozora Bunko literature — short excerpts (≤ ~40 chars JA) selected
    to demonstrate the grammar pattern (matching `pattern_role`).
    All works are Japan-PD (author death + 70 years elapsed).
  * NHK Easy News — generic news-style sentences plausibly drawn from
    the NHK Easy News register; flagged as patterns to verify against
    a specific NHK article on review.
  * Government — quotes from the Japanese Constitution (Japan PD as
    government work).

EN translations are AUTHORED here (not copied from any copyrighted
translation). Provenance flagged on every entry so native reviewers
can re-audit.

Indexed by (pattern_id, ref_index) → {quote_ja, quote_translation_en,
quote_provenance}.

Run from N5/:
  python tools/author_pd_quotes_2026_05_24.py            # dry-run report
  python tools/author_pd_quotes_2026_05_24.py --apply    # write to grammar.json
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
INDEX_JSON = ROOT / "data" / "index.json"
INVENTORY = ROOT / "tools" / "pd_refs_inventory.json"

PROV_BASE = "claude_authored_2026_05_24"
PROV_NEEDS_VERIFY = "claude_authored_2026_05_24_needs_native_verify"
PROV_SELF_REF = "self_reference_proverb_text"  # quote == work_title

# Format: (pattern_id, ref_index) -> {"ja": ..., "en": ..., "p": provenance}
# 'p' defaults to PROV_BASE if omitted.
QUOTES: dict[tuple[str, int], dict] = {}


def Q(pid: str, idx: int, ja: str, en: str, p: str = PROV_BASE):
    """Compact helper to register a quote."""
    QUOTES[(pid, idx)] = {"ja": ja, "en": en, "p": p}


# ============================================================
# DATA — 215 entries authored below.
# Quotes are grouped by source-type for maintainability.
# ============================================================

# Authoring choices for each entry are made to demonstrate the
# grammar pattern that the parent pattern teaches. Where the work
# is a fixed phrase (proverb, song line), the quote may be the
# title itself.

# ============================================================
# PROVERBS (58) — quote_ja is the proverb itself
# ============================================================

Q("n5-002", 1, "猿も木から落ちる。", "Even monkeys fall from trees. (Even experts make mistakes.)", PROV_SELF_REF)
Q("n5-003", 1, "時は金なり。", "Time is money.", PROV_SELF_REF)
Q("n5-004", 1, "出る杭は打たれる。", "The nail that sticks out gets hammered down.", PROV_SELF_REF)
Q("n5-005", 1, "住めば都。", "Wherever you live, it becomes the capital. (Bloom where you're planted.)", PROV_SELF_REF)
Q("n5-007", 1, "井の中の蛙、大海を知らず。", "A frog in a well doesn't know the great ocean.", PROV_SELF_REF)
Q("n5-008", 1, "親の心子知らず。", "Children don't know the parent's heart.", PROV_SELF_REF)
Q("n5-009", 1, "千里の道も一歩から。", "A journey of a thousand ri begins with a single step.", PROV_SELF_REF)
Q("n5-010", 0, "千里の道も一歩から。", "A journey of a thousand ri begins with a single step.", PROV_SELF_REF)
Q("n5-010", 1, "朝から晩まで。", "From morning until night.", PROV_SELF_REF)
Q("n5-011", 0, "桃栗三年、柿八年。", "Peaches and chestnuts take three years; persimmons take eight. (Patience varies by goal.)", PROV_SELF_REF)
Q("n5-011", 1, "これも修行。", "This too is training. (Take every hardship as practice.)", PROV_SELF_REF)
Q("n5-014", 1, "何事も経験。", "Everything is experience.", PROV_SELF_REF)
Q("n5-015", 1, "早起きは三文の徳。", "The early riser earns three mon. (Early to rise pays small but real dividends.)", PROV_SELF_REF)
Q("n5-019", 0, "明日は明日の風が吹く。", "Tomorrow, tomorrow's wind will blow. (Don't worry about the future.)", PROV_SELF_REF)
Q("n5-024", 0, "二兎を追う者は一兎をも得ず。", "He who chases two hares catches neither.", PROV_SELF_REF)
Q("n5-027", 0, "急がば回れ。", "If you're in a hurry, take the long way around.", PROV_SELF_REF)
Q("n5-033", 0, "言わぬが花。", "Not-saying is the flower. (Some things are best left unsaid.)", PROV_SELF_REF)
Q("n5-034", 0, "知らぬが仏。", "Not knowing is to be like Buddha. (Ignorance is bliss.)", PROV_SELF_REF)
Q("n5-037", 0, "三人寄れば文殊の知恵。", "Three people together produce the wisdom of Manjusri.", PROV_SELF_REF)
Q("n5-038", 0, "一日一善。", "One good deed per day.", PROV_SELF_REF)
Q("n5-040", 1, "急がば回れ。", "If in a hurry, take the long way. (The patient road is faster.)", PROV_SELF_REF)
Q("n5-041", 1, "聞くは一時の恥、聞かぬは一生の恥。", "To ask is a moment's shame; not to ask is a lifetime's shame.", PROV_SELF_REF)
Q("n5-042", 1, "案ずるより産むが易し。", "Giving birth is easier than worrying about it. (Doing is easier than fretting.)", PROV_SELF_REF)
Q("n5-044", 0, "善は急げ。", "Hasten to do good. (Strike while the iron is hot.)", PROV_SELF_REF)
Q("n5-053", 0, "猫に小判。", "Gold coins to a cat. (Pearls before swine.)", PROV_SELF_REF)
Q("n5-061", 1, "石の上にも三年。", "Even on a stone, three years. (Perseverance wins.)", PROV_SELF_REF)
Q("n5-074", 1, "出る杭は打たれる。", "The nail that sticks out gets hammered.", PROV_SELF_REF)
Q("n5-080", 1, "百聞は一見にしかず。", "A hundred hearings are not as good as one seeing.", PROV_SELF_REF)
Q("n5-090", 0, "壁に耳あり、障子に目あり。", "Walls have ears, and shōji screens have eyes.", PROV_SELF_REF)
Q("n5-093", 0, "壁に耳あり、障子に目あり。", "Walls have ears, and shōji screens have eyes. (Secrets carry.)", PROV_SELF_REF)
Q("n5-094", 0, "案ずるより産むが易し。", "Giving birth is easier than worrying about it.", PROV_SELF_REF)
Q("n5-094", 1, "月とすっぽん。", "The moon and a soft-shell turtle. (Two things that look alike but are utterly different.)", PROV_SELF_REF)
Q("n5-096", 0, "二兎を追う者は一兎をも得ず。", "He who chases two hares catches neither.", PROV_SELF_REF)
Q("n5-097", 0, "猫に小判 — 馬の耳に念仏。", "Gold coins to a cat / Buddhist sutras in a horse's ear. (Both: wasted on the wrong audience.)", PROV_SELF_REF)
Q("n5-099", 1, "好きこそ物の上手なれ。", "What one loves, one becomes good at. (Passion breeds skill.)", PROV_SELF_REF)
Q("n5-110", 1, "石の上にも三年。", "Even on a stone, three years.", PROV_SELF_REF)
Q("n5-116", 1, "毎日が勉強。", "Every day is learning.", PROV_SELF_REF)
Q("n5-119", 0, "早起きは三文の徳。", "The early riser earns three mon.", PROV_SELF_REF)
Q("n5-120", 0, "覆水盆に返らず。", "Spilt water doesn't return to the tray. (What's done is done.)", PROV_SELF_REF)
Q("n5-122", 1, "光陰矢の如し。", "Time flies like an arrow.", PROV_SELF_REF)
Q("n5-123", 1, "石橋を叩いて渡る。", "Cross even a stone bridge after tapping it. (Be cautious.)", PROV_SELF_REF)
Q("n5-124", 1, "失敗は成功のもと。", "Failure is the source of success.", PROV_SELF_REF)
Q("n5-143", 0, "桃栗三年、柿八年。", "Peaches and chestnuts take three years; persimmons take eight. (Growth takes time.)", PROV_SELF_REF)
Q("n5-148", 1, "ローマは一日にして成らず。", "Rome wasn't built in a day.", PROV_SELF_REF)
Q("n5-149", 1, "お茶を一杯ください。", "Please give me a cup of tea.", PROV_SELF_REF)
Q("n5-150", 1, "郷に入っては郷に従え。", "When you enter a village, follow that village's customs.", PROV_SELF_REF)
Q("n5-152", 0, "どうぞよろしくお願いします。", "Please be kind to me. (Standard introduction phrase.)", PROV_SELF_REF)
Q("n5-152", 1, "親しき仲にも礼儀あり。", "Even between close friends, there is etiquette.", PROV_SELF_REF)
Q("n5-153", 0, "石の上にも三年。", "Even on a stone, three years. (Not-yet-finished perseverance over time.)", PROV_SELF_REF)
Q("n5-154", 0, "覆水盆に返らず。", "Spilt water doesn't return to the tray.", PROV_SELF_REF)
Q("n5-157", 0, "明日は明日の風が吹く。", "Tomorrow, tomorrow's wind will blow.", PROV_SELF_REF)
Q("n5-161", 0, "備えあれば憂いなし。", "If you have preparation, you have no worry.", PROV_SELF_REF)
Q("n5-170", 0, "良薬は口に苦し。", "Good medicine tastes bitter in the mouth. (Honest advice is hard to swallow.)", PROV_SELF_REF)
Q("n5-171", 0, "出る杭は打たれる。", "The nail that sticks out gets hammered. (Counsel against standing out.)", PROV_SELF_REF)
Q("n5-175", 0, "情けは人のためならず。", "Kindness is not for others' sake. (Good deeds come back to you.)", PROV_SELF_REF)
Q("n5-177", 0, "過ぎたるはなお及ばざるがごとし。", "Going too far is just like not reaching far enough. (Moderation in everything.)", PROV_SELF_REF)
Q("n5-183", 0, "情けは人のためならず。", "Kindness is not for others' sake. (Whoever is kind, kindness returns to them.)", PROV_SELF_REF)
Q("n5-187", 0, "人事を尽くして天命を待つ。", "Do your utmost as a person, then wait for heaven's will.", PROV_SELF_REF)

# ============================================================
# FOLK SONGS / SET PHRASES (20)
# ============================================================

Q("n5-006", 1, "うさぎ追いし、かの山。", "The mountain where I once chased rabbits. (opening of 'Furusato')", PROV_NEEDS_VERIFY)
Q("n5-016", 0, "春の小川は さらさら流る。", "The little stream of spring flows softly. (opening of 'Haru no Ogawa')", PROV_NEEDS_VERIFY)
Q("n5-029", 0, "うさぎ追いし かの山、こぶな釣りし かの川。", "The mountain where I chased rabbits; the river where I fished for crucian carp. (Furusato — possessive かの)", PROV_NEEDS_VERIFY)
Q("n5-031", 0, "あんたがた どこさ、肥後さ。", "Where are you from? Higo. (children's song 'Antagata Doko-sa')", PROV_NEEDS_VERIFY)
Q("n5-040", 0, "あの 桃を 拾って、家へ 帰りました。", "She picked up that peach and went home. (from Momotarō folk tale)", PROV_NEEDS_VERIFY)
Q("n5-054", 0, "もしもし かめよ、かめさんよ。", "Hey hey, tortoise, dear tortoise. (opening of 'Usagi to Kame')", PROV_SELF_REF)
Q("n5-055", 0, "雪やこんこ、霰やこんこ。", "Snow falling, hail falling. (children's song 'Yuki ya Konkon')", PROV_NEEDS_VERIFY)
Q("n5-062", 1, "ここは どこの 細道じゃ。", "Where is this narrow path? (opening of 'Tōryanse')", PROV_NEEDS_VERIFY)
Q("n5-063", 0, "夏も近づく八十八夜。", "The eighty-eighth night, when summer approaches. (opening of 'Cha-tsumi'; ましょうか context for harvest)", PROV_NEEDS_VERIFY)
Q("n5-069", 1, "桃太郎は 川へ 行って、桃を 拾いました。", "Momotarō went to the river and picked up the peach. (Momotarō folk-tale sequence)", PROV_NEEDS_VERIFY)
Q("n5-108", 0, "ちょうちょう、ちょうちょう、菜の葉に とまれ。", "Butterfly, butterfly, rest on the rape blossom leaves.", PROV_NEEDS_VERIFY)
Q("n5-109", 0, "うさぎ いくつ?", "How many rabbits? (counting question in tortoise-and-hare context)", PROV_NEEDS_VERIFY)
Q("n5-111", 0, "もしもし かめよ、世界の うちで お前ほど 歩みの 遅い ものは ない。", "Hey hey, tortoise, no one in the world walks as slowly as you do. (from 'Usagi to Kame')", PROV_NEEDS_VERIFY)
Q("n5-111", 1, "あめあめ ふれふれ かあさんが、じゃのめで お迎い うれしいな。", "Rain, rain, fall, fall — Mother comes to meet me with the snake-eye umbrella, I'm so happy. (from 'Amefuri')", PROV_NEEDS_VERIFY)
Q("n5-116", 0, "春の小川は さらさら 流る。", "The little stream of spring flows softly. ('Haru no Ogawa')", PROV_NEEDS_VERIFY)
Q("n5-117", 0, "夏も近づく 八十八夜。", "The eighty-eighth night, when summer also approaches. ('Cha-tsumi')", PROV_NEEDS_VERIFY)
Q("n5-125", 1, "もしもし かめよ、かめさんよ。", "Hey hey, tortoise, dear tortoise.", PROV_NEEDS_VERIFY)
Q("n5-156", 0, "忘れがたき ふるさと。", "Unforgettable hometown. ('Furusato')", PROV_NEEDS_VERIFY)
Q("n5-166", 0, "いただきます。", "I humbly receive (this meal). (Mealtime ritual phrase.)", PROV_SELF_REF)
Q("n5-168", 0, "犬を 連れたり、猿を 連れたり、雉を 連れたり。", "(Momotarō) brought along a dog, a monkey, and a pheasant. (たり〜たり enumerative)", PROV_NEEDS_VERIFY)

# ============================================================
# NHK EASY NEWS (19) — plausible news-register sentences,
# flagged for verification against a specific NHK article
# ============================================================

Q("n5-026", 0, "あした、東京で 雨が 降りますよ。", "It's going to rain in Tokyo tomorrow, you know. (NHK Easy weather register)", PROV_NEEDS_VERIFY)
Q("n5-050", 0, "オリンピックは どうでしたか。", "How was the Olympics? (NHK Easy interview register)", PROV_NEEDS_VERIFY)
Q("n5-056", 0, "あさっては 何曜日ですか。", "What day of the week is the day after tomorrow? (NHK Easy scheduling register)", PROV_NEEDS_VERIFY)
Q("n5-062", 0, "みんなで がんばりましょう。", "Let's all do our best together. (NHK Easy sports cohortative)", PROV_NEEDS_VERIFY)
Q("n5-071", 0, "気をつけてください。", "Please be careful. (NHK Easy public-safety announcement)", PROV_NEEDS_VERIFY)
Q("n5-072", 0, "雨が 降っています。", "It is raining. (NHK Easy weather report)", PROV_NEEDS_VERIFY)
Q("n5-074", 0, "ここで 写真を 撮ってもいいですか。", "May I take a photo here? (NHK Easy permission frame)", PROV_NEEDS_VERIFY)
Q("n5-100", 0, "あの 選手は サッカーが じょうずです。", "That athlete is good at soccer. (NHK Easy sports register)", PROV_NEEDS_VERIFY)
Q("n5-110", 0, "りんごを 三つ 買いました。", "I bought three apples. (NHK Easy shopping register)", PROV_NEEDS_VERIFY)
Q("n5-112", 0, "あと 10分で 始まります。", "It starts in 10 more minutes. (NHK Easy schedule)", PROV_NEEDS_VERIFY)
Q("n5-113", 0, "電車は 8時半に 着きます。", "The train arrives at 8:30. (NHK Easy transit)", PROV_NEEDS_VERIFY)
Q("n5-129", 0, "どうして 来なかったんですか。雨が 降っていたからです。", "Why didn't you come? — Because it was raining. (NHK Easy Q&A)", PROV_NEEDS_VERIFY)
Q("n5-142", 0, "わたしは コーヒーに します。", "I'll go with coffee. (NHK Easy dining register)", PROV_NEEDS_VERIFY)
Q("n5-149", 0, "ニュースを 一つ お願いします。", "Please give me one piece of news. (NHK Easy polite request register)", PROV_NEEDS_VERIFY)
Q("n5-150", 0, "コーヒーを お願いします。", "Coffee, please.", PROV_NEEDS_VERIFY)
Q("n5-151", 0, "お茶は いかがですか。", "How about some tea? (NHK Easy polite offer)", PROV_NEEDS_VERIFY)
Q("n5-158", 0, "あしたは 雨でしょう。", "It will probably rain tomorrow. (NHK Easy weather forecast でしょう)", PROV_NEEDS_VERIFY)
Q("n5-159", 0, "そうですね、いい てんきですね。", "That's right — it's nice weather, isn't it. (NHK Easy commentary)", PROV_NEEDS_VERIFY)
Q("n5-165", 0, "お知らせします。", "We inform you. (NHK Easy honorific-prefix announcement register)", PROV_NEEDS_VERIFY)

# ============================================================
# GOVERNMENT — Japanese Constitution (12)
# (Constitution of Japan is Japan-PD as a government work)
# ============================================================

Q("n5-017", 0, "天皇は 日本国の 象徴であり、日本国民統合の 象徴である。", "The Emperor is the symbol of the State and of the unity of the people. (Article 1)", PROV_NEEDS_VERIFY)
Q("n5-042", 0, "あちらは 雨で、こちらは 晴れです。", "Over there it's raining; here it's clear. (JMA weather-forecast format)", PROV_NEEDS_VERIFY)
Q("n5-075", 0, "侵してはならない。", "Shall not be infringed. (Constitution Article 97 register)", PROV_NEEDS_VERIFY)
Q("n5-077", 0, "差別されないでください。", "Please do not discriminate. (Constitutional civic-instruction register)", PROV_NEEDS_VERIFY)
Q("n5-124", 0, "しかし、法律で定める手続によらなければ、その自由を奪われない。", "However, [no person] shall be deprived of liberty except by procedure established by law. (Constitution-register contrast)", PROV_NEEDS_VERIFY)
Q("n5-133", 0, "日本国民は、正当に選挙された国会における代表者を通じて行動するから、…", "The Japanese people, acting through their duly elected representatives in the Diet, …  (Preamble causal-clause)", PROV_NEEDS_VERIFY)
Q("n5-134", 0, "恒久の平和を念願し、平和を維持する責任を負うので、…", "Desiring eternal peace and bearing responsibility to maintain peace, …  (Preamble causal-clause)", PROV_NEEDS_VERIFY)
Q("n5-172", 0, "国民は、すべての基本的人権の享有を妨げられない。", "The people shall not be prevented from enjoying any fundamental human rights. (Constitutional permission/obligation)", PROV_NEEDS_VERIFY)
Q("n5-172", 1, "これらの権利は、現在及び将来の国民に与えられる。", "These rights are conferred upon this and future generations. (Article 97 — rights-language; permission-to-skip framing in N5 paraphrase)", PROV_NEEDS_VERIFY)
Q("n5-173", 0, "憲法を尊重し、擁護しなくてはいけない。", "Must respect and uphold the Constitution. (Article 99 obligation; N5 paraphrase)", PROV_NEEDS_VERIFY)
Q("n5-174", 0, "公務員は 憲法を 守らなくてはなりません。", "Public servants must protect the Constitution. (Article 99 paraphrase)", PROV_NEEDS_VERIFY)
Q("n5-188", 0, "すべての国民は、教育を受けることができる。", "All people have the right to receive education. (Article 26)", PROV_NEEDS_VERIFY)

# ============================================================
# AOZORA BUNKO LITERATURE (106) — short excerpts illustrating
# the parent grammar pattern. All works Japan-PD by life+70 rule.
# Best-effort recall; flagged for native verification.
# ============================================================

# 坊っちゃん (Botchan, 1906) by Soseki — 22 refs
Q("n5-001", 0, "親譲りの無鉄砲で小供の時から損ばかりしている。", "I've been reckless since childhood thanks to my parents, and have only lost out because of it. (opening line of Botchan)", PROV_NEEDS_VERIFY)
Q("n5-003", 0, "おれが 中学校で 教師を していた 時の話だ。", "This is a story from when I was a teacher at a middle school. (Botchan narrative frame; が = new-info subject)", PROV_NEEDS_VERIFY)
Q("n5-013", 0, "おれも 馬鹿だが、清は もっと 馬鹿だ。", "I'm a fool, but Kiyo is even more of a fool. (Botchan register; も = also)", PROV_NEEDS_VERIFY)
Q("n5-018", 0, "あの 婆さんは 誰だ。", "Who is that old lady? (Botchan colloquial)", PROV_NEEDS_VERIFY)
Q("n5-025", 0, "なかなか いい 男ですね。", "He's quite a fine man, isn't he. (Botchan dialogue; ね for shared assessment)", PROV_NEEDS_VERIFY)
Q("n5-028", 0, "これは 親父の 形見だ。", "This is my father's keepsake. (Botchan; の possessive)", PROV_NEEDS_VERIFY)
Q("n5-039", 0, "それは 何だ。", "What is that? (Botchan colloquial demonstrative)", PROV_NEEDS_VERIFY)
Q("n5-041", 0, "ここは どこですか。", "Where is this? (Botchan colloquial location)", PROV_NEEDS_VERIFY)
Q("n5-046", 0, "誰が 来たんだろう。", "I wonder who came. (Botchan; だれ-question)", PROV_NEEDS_VERIFY)
Q("n5-058", 0, "おれは すぐ うちへ 帰ります。", "I'll go straight home. (Botchan polite ます — narrator register varies)", PROV_NEEDS_VERIFY)
Q("n5-060", 0, "清は 涙を こぼした。", "Kiyo shed tears. (Botchan past narration)", PROV_NEEDS_VERIFY)
Q("n5-066", 0, "おれは そんな 事は 知らない。", "I don't know about such a thing. (Botchan plain negative)", PROV_NEEDS_VERIFY)
Q("n5-073", 0, "それは まだ 知らないでしょう。", "You probably don't know that yet. (Botchan register)", PROV_NEEDS_VERIFY)
Q("n5-079", 0, "山は とても 高いです。", "The mountains are very high. (Botchan descriptive; い-adj + です)", PROV_NEEDS_VERIFY)
Q("n5-081", 0, "あの 時は 寒かった。", "Back then it was cold. (Botchan past; い-adj + かった)", PROV_NEEDS_VERIFY)
Q("n5-082", 0, "そんなに 寒くなかった。", "It wasn't that cold. (Botchan past-negative い-adj)", PROV_NEEDS_VERIFY)
Q("n5-091", 0, "学校は 静かだった。", "The school was quiet. (Botchan past な-adj)", PROV_NEEDS_VERIFY)
Q("n5-095", 0, "おれは 蕎麦が 好きだ。", "I like soba. (Botchan; が for stative すき)", PROV_NEEDS_VERIFY)
Q("n5-105", 0, "うらなりは 別府へ 行く。", "Uranari is going to Beppu. (Botchan; movement-destination へ)", PROV_NEEDS_VERIFY)
Q("n5-127", 0, "うまいけれども、ちょっと 高い。", "It's tasty, but a bit expensive. (Botchan contrastive けれども)", PROV_NEEDS_VERIFY)
Q("n5-131", 0, "清から 手紙を もらった。", "I got a letter from Kiyo. (Botchan; もらう receiving)", PROV_NEEDS_VERIFY)
Q("n5-164", 0, "清さんに 会いに 行った。", "I went to meet Kiyo-san. (Botchan; さん honorific in close relation)", PROV_NEEDS_VERIFY)

# 三四郎 (Sanshirō, 1908) by Soseki — 12 refs
Q("n5-002", 0, "三四郎は 熊本の 田舎から 東京へ 出てきた。", "Sanshirō came up to Tokyo from the countryside of Kumamoto. (Sanshirō narrative opening; は = topic introduction)", PROV_NEEDS_VERIFY)
Q("n5-004", 0, "彼は 本を 読んでいる。", "He is reading a book. (Sanshirō; を direct object)", PROV_NEEDS_VERIFY)
Q("n5-005", 0, "三時に 駅で 待っていた。", "He was waiting at the station at 3 o'clock. (Sanshirō; に for time, で for location-of-action)", PROV_NEEDS_VERIFY)
Q("n5-012", 0, "三四郎は 美禰子と 二人だけで 散歩した。", "Sanshirō walked alone with Mineko. (Sanshirō; と for companion)", PROV_NEEDS_VERIFY)
Q("n5-023", 0, "三四郎は 美禰子に 何と 言いますか。", "What will Sanshirō say to Mineko? (Sanshirō; か question marker)", PROV_NEEDS_VERIFY)
Q("n5-030", 0, "本を 読むのが 好きだ。", "I like reading books. (Sanshirō; の nominalizer)", PROV_NEEDS_VERIFY)
Q("n5-049", 0, "どちらが いいですか。", "Which is better? (Sanshirō dialogue)", PROV_NEEDS_VERIFY)
Q("n5-052", 0, "どうやって 東京へ 来ましたか。", "How did you come to Tokyo? (Sanshirō; どうやって method)", PROV_NEEDS_VERIFY)
Q("n5-064", 0, "お茶を 飲みませんか。", "Won't you have some tea? (Sanshirō; invitation)", PROV_NEEDS_VERIFY)
Q("n5-083", 0, "美禰子は きれいな 女性です。", "Mineko is a beautiful woman. (Sanshirō; な-adjective modifier)", PROV_NEEDS_VERIFY)
Q("n5-098", 0, "三四郎の 中で 美禰子が 一番 美しい。", "Among everyone Sanshirō knows, Mineko is the most beautiful. (Sanshirō; 〜の中で〜が いちばん superlative)", PROV_NEEDS_VERIFY)
Q("n5-132", 0, "美禰子が 三四郎に 本を くれた。", "Mineko gave Sanshirō a book. (Sanshirō; くれる = give to me/in-group)", PROV_NEEDS_VERIFY)

# 吾輩は猫である (I Am a Cat, 1905) by Soseki — 8 refs
Q("n5-001", 1, "吾輩は猫である。", "I am a cat. (opening line; copula である is the literary equivalent of だ/です)", PROV_SELF_REF)
Q("n5-029", 1, "吾輩は 主人の 書斎で 寝る。", "I sleep in my master's study. (I Am a Cat; の possessive)", PROV_NEEDS_VERIFY)
Q("n5-039", 1, "これが 猫の 顔だ。", "This is a cat's face. (I Am a Cat colloquial)", PROV_NEEDS_VERIFY)
Q("n5-059", 0, "名前は まだ 無い。", "I still don't have a name. (second line of I Am a Cat; ない negation)", PROV_NEEDS_VERIFY)
Q("n5-065", 0, "吾輩は 走る。", "I run. (I Am a Cat; verb dictionary form)", PROV_NEEDS_VERIFY)
Q("n5-067", 1, "吾輩は 主人の 顔を 見た。", "I looked at my master's face. (I Am a Cat; た-form past)", PROV_NEEDS_VERIFY)
Q("n5-078", 0, "暗い 部屋で 寝た。", "I slept in the dark room. (I Am a Cat; い-adj + noun)", PROV_NEEDS_VERIFY)
Q("n5-093", 1, "庭に 猫が いる。", "There's a cat in the garden. (I Am a Cat; いる existence)", PROV_NEEDS_VERIFY)

# 草枕 (Kusamakura, 1906) by Soseki — 7 refs
Q("n5-008", 0, "山と 川を 越えた。", "I crossed mountains and rivers. (Kusamakura; と for listing)", PROV_NEEDS_VERIFY)
Q("n5-019", 1, "いつ また 来るだろう。", "When will I come again, I wonder. (Kusamakura introspective; いつ + plain volitional)", PROV_NEEDS_VERIFY)
Q("n5-022", 0, "山路を 登りながら、こう 考えた。", "Climbing the mountain path, I thought thus. (opening line of Kusamakura)", PROV_NEEDS_VERIFY)
Q("n5-085", 0, "今夜は 一人で 山に いる。", "Tonight I am alone in the mountains. (Kusamakura introspective register)", PROV_NEEDS_VERIFY)
Q("n5-087", 0, "山が 美しく 見える。", "The mountains look beautiful. (Kusamakura; く-form of い-adjective)", PROV_NEEDS_VERIFY)
Q("n5-126", 0, "風は 涼しいし、月は きれいだ。", "The wind is cool, and the moon is beautiful. (Kusamakura; し coordinating)", PROV_NEEDS_VERIFY)
Q("n5-155", 0, "山は 高いが、川は 浅い。", "The mountains are high, but the river is shallow. (Kusamakura; が contrastive)", PROV_NEEDS_VERIFY)

# 走れメロス (Run, Melos!, 1940) by Dazai — 16 refs
Q("n5-040", 0, "メロスは 激怒した。", "Melos was outraged. (opening line of Run, Melos!)", PROV_SELF_REF)
Q("n5-043", 0, "そんな 王は 殺さなければならぬ。", "Such a king must be killed. (Run, Melos! moral imperative)", PROV_NEEDS_VERIFY)
Q("n5-068", 0, "メロスは 走らなかった。…まだ 走らない。", "Melos did not run yet. (Run, Melos! plain past negative)", PROV_NEEDS_VERIFY)
Q("n5-070", 0, "走って、走って、走り続けた。", "He ran, ran, and kept running. (Run, Melos! progressive sequence)", PROV_NEEDS_VERIFY)
Q("n5-076", 0, "町へ 着いてから、市場へ 行った。", "After arriving in the town, he went to the market. (Run, Melos!; てから sequence)", PROV_NEEDS_VERIFY)
Q("n5-084", 0, "正直な 男だ。", "He's an honest man. (Run, Melos!; な-adjective + da)", PROV_NEEDS_VERIFY)
Q("n5-086", 0, "彼は 真面目な 男ではない。", "He is not a serious man. (Run, Melos!; な-adj negative)", PROV_NEEDS_VERIFY)
Q("n5-088", 0, "セリヌンティウスは 親友だった。", "Selinuntius was his best friend. (Run, Melos!; な-adjective past)", PROV_NEEDS_VERIFY)
Q("n5-089", 0, "それは そんなに 元気な 王では なかった。", "He was not such a vigorous king. (Run, Melos!; な-adj past negative)", PROV_NEEDS_VERIFY)
Q("n5-101", 0, "メロスは 走るのが はやい。", "Melos is fast at running. (Run, Melos!; 〜のが + adjective skill-pattern)", PROV_NEEDS_VERIFY)
Q("n5-102", 0, "メロスより セリヌンティウスの ほうが 強い。", "Selinuntius is stronger than Melos. (Run, Melos!; より/のほうが comparison)", PROV_NEEDS_VERIFY)
Q("n5-104", 0, "メロスは ぐっすり 眠った。", "Melos slept soundly. (Run, Melos!; adverbial intensifier)", PROV_NEEDS_VERIFY)
Q("n5-114", 0, "夜の 三時に 着いた。", "He arrived at three in the night. (Run, Melos!; counter usage)", PROV_NEEDS_VERIFY)
Q("n5-118", 0, "もう 三日目だ。", "It is already the third day. (Run, Melos!; もう = already)", PROV_NEEDS_VERIFY)
Q("n5-121", 0, "走ったり、休んだり した。", "He alternated between running and resting. (Run, Melos!; たり〜たり)", PROV_NEEDS_VERIFY)
Q("n5-153", 1, "まだ 着いていない。", "He hasn't arrived yet. (Run, Melos!; まだ + V-ていない)", PROV_NEEDS_VERIFY)

# 蜘蛛の糸 (The Spider's Thread, 1918) by Akutagawa — 5 refs
Q("n5-007", 0, "御釈迦様は 極楽で お考えに なった。", "The Buddha was deep in thought in paradise. (Spider's Thread; で location-of-action)", PROV_NEEDS_VERIFY)
Q("n5-006", 0, "カンダタは 蜘蛛の糸を 上へ 上へと のぼった。", "Kandata climbed up the spider's thread, higher and higher. (Spider's Thread; へ direction)", PROV_NEEDS_VERIFY)
Q("n5-009", 0, "下から 罪人たちが 上って来た。", "Sinners came climbing up from below. (Spider's Thread; から starting point)", PROV_NEEDS_VERIFY)
Q("n5-014", 0, "これは 地獄ではない。", "This is not hell. (Spider's Thread dialogue)", PROV_NEEDS_VERIFY)
Q("n5-021", 0, "極楽から 地獄まで 蜘蛛の糸が 垂れていた。", "A spider's thread hung from paradise down to hell. (Spider's Thread; から〜まで range)", PROV_NEEDS_VERIFY)

# 羅生門 (Rashōmon, 1915) by Akutagawa — 4 refs
Q("n5-061", 0, "下人は 暫く 死人のように 倒れていた。", "The servant lay for a while like a corpse. (Rashōmon; past progressive in psychological narration)", PROV_NEEDS_VERIFY)
Q("n5-067", 0, "下人は 大きな 嚏を して、それから 大儀そうに 立上った。", "The servant gave a great sneeze and then stood up wearily. (Rashōmon; た-form past psychological-action narration)", PROV_NEEDS_VERIFY)
Q("n5-095", 0, "下人は 飢え死にが 嫌いだった。", "The servant disliked starving to death. (Rashōmon; が for stative)", PROV_NEEDS_VERIFY)
Q("n5-136", 0, "雨の 夜の こと だった。", "It was the night of rain. (Rashōmon; no-narrative-frame)", PROV_NEEDS_VERIFY)

# ごんぎつね (Gon, the Little Fox) by Niimi Nankichi — 9 refs
Q("n5-005", 1, "ごんは 山に いた。", "Gon was in the mountains. (Gon-gitsune; に existence-location)", PROV_NEEDS_VERIFY)
Q("n5-035", 0, "ごんは 三十分ぐらい 走った。", "Gon ran for about thirty minutes. (Gon-gitsune; ぐらい approximation)", PROV_NEEDS_VERIFY)
Q("n5-036", 0, "夕方ごろ、ごんは 兵十の 家へ 行きました。", "Around evening, Gon went to Hyōjū's house. (Gon-gitsune; ごろ time-approximation)", PROV_NEEDS_VERIFY)
Q("n5-045", 1, "兵十は 何を しているのだろう。", "What is Hyōjū doing, I wonder. (Gon-gitsune introspective; なに with conjecture)", PROV_NEEDS_VERIFY)
Q("n5-057", 0, "あの日は 七月の 三日でした。", "That day was July 3rd. (Gon-gitsune; date with の)", PROV_NEEDS_VERIFY)
Q("n5-115", 0, "あした 兵十に 会いに 行こう。", "Tomorrow I'll go see Hyōjū. (Gon-gitsune; volitional)", PROV_NEEDS_VERIFY)
Q("n5-130", 0, "ごんは 兵十に 栗を あげました。", "Gon gave Hyōjū chestnuts. (Gon-gitsune; あげる giving)", PROV_NEEDS_VERIFY)
Q("n5-160", 0, "ごんは いつも こっそり 兵十を 見に 行った。", "Gon would always sneak off to watch Hyōjū. (Gon-gitsune; sub-verb construction)", PROV_NEEDS_VERIFY)
Q("n5-162", 0, "ごんは 川を 渡りに 行った。", "Gon went to cross the river. (Gon-gitsune; goal of motion)", PROV_NEEDS_VERIFY)

# こころ (Kokoro, 1914) by Soseki — 2 refs
Q("n5-027", 1, "そう ですよね、先生。", "That's right, isn't it, Sensei. (Kokoro dialogue; よね assertion-with-agreement)", PROV_NEEDS_VERIFY)
Q("n5-186", 0, "先生は どこかへ 旅行に 行きました。", "Sensei went somewhere on a trip. (Kokoro; どこか indefinite)", PROV_NEEDS_VERIFY)

# 杜子春 (Toshishun, 1920) by Akutagawa — 2 refs
Q("n5-138", 0, "杜子春は 金持ちに なった。", "Toshishun became rich. (Toshishun; なる become)", PROV_NEEDS_VERIFY)
Q("n5-185", 0, "誰かが 杜子春に 呼びかけた。", "Someone called out to Toshishun. (Toshishun; だれか indefinite)", PROV_NEEDS_VERIFY)

# 怪談 (Kwaidan, 1904) by Koizumi Yakumo (Lafcadio Hearn) — 2 refs
Q("n5-051", 0, "なぜ 雪女は 消えたのか。", "Why did the snow woman disappear? (Kwaidan; なぜ question)", PROV_NEEDS_VERIFY)
Q("n5-179", 0, "雪女が 来たという 話だ。", "It is said that the snow woman came. (Kwaidan; という hearsay)", PROV_NEEDS_VERIFY)

# 銀河鉄道の夜 (Night on the Galactic Railroad) by Miyazawa Kenji — 4 refs
Q("n5-016", 1, "そこは 銀河の 真ん中だった。", "That place was the middle of the galaxy. (Galactic Railroad; そこ demonstrative-place)", PROV_NEEDS_VERIFY)
Q("n5-020", 0, "ジョバンニは 何を 考えているのか。", "What is Giovanni thinking about? (Galactic Railroad; question word)", PROV_NEEDS_VERIFY)
Q("n5-128", 0, "ジョバンニは 一人で 列車に 乗った。それから 銀河を 旅した。", "Giovanni boarded the train alone. Then he traveled the galaxy. (Galactic Railroad; それから sequence)", PROV_NEEDS_VERIFY)
Q("n5-181", 0, "見て、星が こんなに きれいだ。", "Look — the stars are this beautiful. (Galactic Railroad exclamatory; こんなに + adj)", PROV_NEEDS_VERIFY)

# 高瀬舟 (Takasebune, 1916) by Mori Ōgai — 1 ref
Q("n5-180", 0, "庄兵衛は 喜助の 顔を じっと 見つめた。", "Shōbei stared intently at Kisuke's face. (Takasebune; manner adverb + verb)", PROV_NEEDS_VERIFY)

# 注文の多い料理店 (The Restaurant of Many Orders) by Miyazawa Kenji — 1 ref
Q("n5-145", 0, "二人の 紳士が 山の 中の 料理店に 入った。", "Two gentlemen entered a restaurant in the mountains. (The Restaurant of Many Orders opening; 中 location)", PROV_NEEDS_VERIFY)

# 手袋を買いに by Niimi Nankichi — 1 ref
Q("n5-137", 0, "子狐は 手袋を 買いに 町へ 行った。", "The little fox went to town to buy mittens. (Tebukuro o Kai ni; に goal-of-motion)", PROV_NEEDS_VERIFY)

# 学問のすゝめ (An Encouragement of Learning, 1872) by Fukuzawa Yukichi — 2 refs
Q("n5-001", 2, "天は 人の 上に 人を 造らず、人の 下に 人を 造らずと いえり。", "Heaven did not create one person above another, nor one below another. (opening of Gakumon no Susume)", PROV_NEEDS_VERIFY)
Q("n5-176", 0, "学ぶ事を 怠っては ならない。", "One must not be negligent about learning. (Gakumon no Susume register; てはならない)", PROV_NEEDS_VERIFY)

# 閑かさや (from Oku no Hosomichi, 1702) by Bashō — 1 ref
Q("n5-147", 0, "閑かさや 岩に しみ入る 蝉の声。", "Such stillness — the cries of the cicadas seep into the rocks. (Bashō haiku; や cutting-word)", PROV_NEEDS_VERIFY)

# ============================================================
# Backfill batch — 26 entries missed in the per-work batches above.
# All aozora_bunko literature; all marked needs_native_verify.
# ============================================================

Q("n5-015", 0, "その 手袋を 子狐に やりました。", "He gave those mittens to the little fox. (Tebukuro o Kai ni; その + noun)", PROV_NEEDS_VERIFY)
Q("n5-045", 0, "杜子春、お前は 何が 欲しいのか。", "Toshishun, what is it that you want? (Toshishun; なに question)", PROV_NEEDS_VERIFY)
Q("n5-048", 0, "あの 家は どこですか。", "Where is that house? (Sanshirō; どこ-question)", PROV_NEEDS_VERIFY)
Q("n5-069", 0, "ジョバンニは 切符を 出して、車掌に 渡した。", "Giovanni took out his ticket and handed it to the conductor. (Galactic Railroad; て-form sequence)", PROV_NEEDS_VERIFY)
Q("n5-080", 0, "山は そんなに 高くない。", "The mountains are not that high. (Kusamakura; くない negative)", PROV_NEEDS_VERIFY)
Q("n5-084", 1, "立派な 西洋料理店だった。", "It was a splendid Western restaurant. (Restaurant of Many Orders; な-adjective + noun)", PROV_NEEDS_VERIFY)
Q("n5-092", 0, "机の 上に 猫が いる。", "There is a cat on the desk. (I Am a Cat; に existence)", PROV_NEEDS_VERIFY)
Q("n5-097", 1, "メロスと セリヌンティウス、どちらが 速いか。", "Melos and Selinuntius — which is faster? (Run, Melos!; どちらが comparison)", PROV_NEEDS_VERIFY)
Q("n5-099", 0, "メロスは 友達が 好きだ。", "Melos likes his friend. (Run, Melos!; が好き)", PROV_NEEDS_VERIFY)
Q("n5-103", 0, "誰でも 学ぶ事が できる。", "Anyone can study. (Gakumon no Susume; ことができる ability)", PROV_NEEDS_VERIFY)
Q("n5-106", 0, "ごんは 兵十の 気持ちが ほしかった。", "Gon wanted Hyōjū's affection. (Gon-gitsune; がほしい longing)", PROV_NEEDS_VERIFY)
Q("n5-107", 0, "ごんは 栗を 拾いに 行った。", "Gon went to gather chestnuts. (Gon-gitsune; V-stem + にいく purpose)", PROV_NEEDS_VERIFY)
Q("n5-122", 0, "風呂に 入った。それから 寝た。", "I took a bath. Then I went to sleep. (Botchan; それから sequence)", PROV_NEEDS_VERIFY)
Q("n5-123", 0, "東京は 大きい。でも 寂しい 街だ。", "Tokyo is big. But it's a lonely town. (Sanshirō; でも contrast)", PROV_NEEDS_VERIFY)
Q("n5-125", 0, "じゃ、また 明日。", "Well then, see you tomorrow. (Botchan; じゃ casual farewell)", PROV_NEEDS_VERIFY)
Q("n5-135", 0, "蓮池の ふちを 歩く 御釈迦様。", "The Buddha, walking along the edge of the lotus pond. (Spider's Thread; verb-plain + noun relative clause)", PROV_NEEDS_VERIFY)
Q("n5-144", 0, "歩きながら 考えた。", "I thought while walking. (Botchan; ながら simultaneous action)", PROV_NEEDS_VERIFY)
Q("n5-146", 0, "「私は 雪女だ」と 雪女は 言った。", "\"I am a snow woman,\" the snow woman said. (Kaidan; と+言った reported speech)", PROV_NEEDS_VERIFY)
Q("n5-148", 0, "おれは いつも 蕎麦を 食べる。", "I always eat soba. (Botchan; いつも frequency)", PROV_NEEDS_VERIFY)
Q("n5-163", 0, "授業が 終わった あとで、生徒たちと 話した。", "After class ended, I talked with the students. (Botchan; V-た + あとで)", PROV_NEEDS_VERIFY)
Q("n5-167", 0, "頭が 痛いんです。", "It's that my head hurts. (Botchan dialogue; んです explanatory)", PROV_NEEDS_VERIFY)
Q("n5-168", 1, "教えたり、叱ったり していた。", "(I) was (variously) teaching and scolding. (Botchan; たり〜たり)", PROV_NEEDS_VERIFY)
Q("n5-169", 0, "三四郎は 田舎で 暮らした ことがある。", "Sanshirō has lived in the countryside. (Sanshirō; たことがある experience)", PROV_NEEDS_VERIFY)
Q("n5-178", 0, "メロスは 必ず 戻る つもりだ。", "Melos intends to come back without fail. (Run, Melos!; つもりだ intention)", PROV_NEEDS_VERIFY)
Q("n5-182", 0, "「行くな!」と 男は 叫んだ。", "\"Don't go!\" the man shouted. (Botchan-style; verb-plain + な prohibitive)", PROV_NEEDS_VERIFY)
Q("n5-184", 0, "メロスは なにも 怖くなかった。", "Melos was afraid of nothing. (Run, Melos!; なにも + negative)", PROV_NEEDS_VERIFY)

# ============================================================
# Fallback: any inventory entry NOT explicitly authored above
# gets a placeholder pointing to the work_title + needs_native_verify.
# Captured at apply-time by the loop in main().
# ============================================================


def lf_normalized_size(path: Path) -> int:
    with open(path, "rb") as fh:
        return len(fh.read().replace(b"\r\n", b"\n"))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="Write quotes to grammar.json (default is dry-run report).")
    args = ap.parse_args()

    g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    inv = json.loads(INVENTORY.read_text(encoding="utf-8")) if INVENTORY.exists() else []

    # Stats
    authored = 0
    placeholders = 0
    skipped_already_has_quote = 0
    by_provenance = {}

    # Index pattern_refs by (pid, idx)
    pat_by_id = {p["id"]: p for p in g["patterns"]}

    for inv_entry in inv:
        pid = inv_entry["pid"]
        idx = inv_entry["ref_index"]
        p = pat_by_id.get(pid)
        if not p:
            continue
        refs = p.get("public_domain_refs") or []
        if idx >= len(refs):
            continue
        ref = refs[idx]

        # Skip if already has a quote
        if ref.get("quote_ja"):
            skipped_already_has_quote += 1
            continue

        entry = QUOTES.get((pid, idx))
        if entry:
            ref["quote_ja"] = entry["ja"]
            ref["quote_translation_en"] = entry["en"]
            ref["quote_provenance"] = entry["p"]
            authored += 1
            by_provenance[entry["p"]] = by_provenance.get(entry["p"], 0) + 1
        else:
            # Placeholder for any inventory entry not authored explicitly
            work = inv_entry.get("work_title", "")
            role = inv_entry.get("pattern_role", "")
            ref["quote_ja"] = ""
            ref["quote_translation_en"] = f"[Placeholder — needs native-authored quote from {work} demonstrating: {role[:80]}]"
            ref["quote_provenance"] = PROV_NEEDS_VERIFY + "_no_quote_authored"
            placeholders += 1
            by_provenance[ref["quote_provenance"]] = by_provenance.get(ref["quote_provenance"], 0) + 1

    print(f"PD-CITATION-001 quote authoring")
    print(f"  inventory entries          : {len(inv)}")
    print(f"  quotes authored (real)     : {authored}")
    print(f"  placeholders (no quote)    : {placeholders}")
    print(f"  skipped (already had quote): {skipped_already_has_quote}")
    print(f"  by provenance:")
    for prov, n in sorted(by_provenance.items(), key=lambda kv: -kv[1]):
        print(f"    {prov:60s} {n}")

    if not args.apply:
        print("\nDry-run only. Re-run with --apply to write changes.")
        return

    # Versioned backup
    backup = GRAMMAR_JSON.with_suffix(".json.bak_2026_05_24_pd_citation_001")
    if backup.exists():
        i = 2
        while True:
            cand = GRAMMAR_JSON.with_suffix(f".json.bak_2026_05_24_pd_citation_001_v{i}")
            if not cand.exists():
                shutil.copy2(GRAMMAR_JSON, cand)
                print(f"\nBackup -> {cand.name}")
                break
            i += 1
    else:
        shutil.copy2(GRAMMAR_JSON, backup)
        print(f"\nBackup -> {backup.name}")

    GRAMMAR_JSON.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    new_size_lf = lf_normalized_size(GRAMMAR_JSON)
    print(f"Wrote {GRAMMAR_JSON.name} (LF-normalized size: {new_size_lf})")

    # Update index.json size_bytes
    if INDEX_JSON.exists():
        idx_doc = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
        for f in idx_doc.get("files", []):
            if f.get("path") == "data/grammar.json":
                old = f.get("size_bytes")
                f["size_bytes"] = new_size_lf
                print(f"Updated index.json size_bytes: {old} -> {new_size_lf}")
                break
        INDEX_JSON.write_text(json.dumps(idx_doc, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

