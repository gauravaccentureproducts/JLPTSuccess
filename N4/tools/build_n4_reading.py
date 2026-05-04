"""Build N4 reading corpus seed (~10 passages with comprehension questions).

Each passage is hand-authored to use only N5+N4 in-scope kanji and to
demonstrate one of the N4 grammar patterns naturally. Questions follow the
JLPT N4 dokkai format: short passage + 2-3 multi-choice questions.

Quality: SEED-grade. Native-teacher review (Pass-4) recommended before
exam-grade use, but each passage is grammatical and topical.
"""
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

PASSAGES = [
    {
        'id': 'n4.read.001',
        'level': 'easy',
        'topic': 'daily-routine',
        'title_ja': 'わたしの 一日',
        'ja': 'わたしは 毎日 七時に 起きます。朝ごはんを 食べてから、学校に 行きます。学校では 日本語と すうがくを 勉強します。午後 三時に うちに 帰って、しゅくだいを します。夜は テレビを 見ながら、ご飯を 食べます。十時ごろ ねます。',
        'questions': [
            {
                'q': 'この人は 何時に おきますか。',
                'choices': ['六時', '七時', '八時', '九時'],
                'correct': '七時',
                'explanation_en': '"わたしは 毎日 七時に 起きます" - I get up at seven every day.',
            },
            {
                'q': 'この人は 学校で 何を 勉強しますか。',
                'choices': ['えいごと すうがく', '日本語と すうがく', '日本語と えいご', 'おんがくと すうがく'],
                'correct': '日本語と すうがく',
                'explanation_en': '"日本語と すうがくを 勉強します"',
            },
        ],
    },
    {
        'id': 'n4.read.002',
        'level': 'easy',
        'topic': 'weather',
        'title_ja': '今日の てんき',
        'ja': '今日は あさから 雨が ふっています。さむい日なので、あつい コーヒーを 飲みました。午後は 雨が やむかも しれませんが、あたたかい 服を 着て でかけたいです。明日は はれると 思います。',
        'questions': [
            {
                'q': '今日の てんきは どうですか。',
                'choices': ['はれ', 'くもり', '雨', 'ゆき'],
                'correct': '雨',
                'explanation_en': '"今日は あさから 雨が ふっています"',
            },
            {
                'q': 'この人は 午後 何を したいですか。',
                'choices': ['うちに いる', 'コーヒーを 飲む', 'あたたかい服を 着て でかける', 'ねる'],
                'correct': 'あたたかい服を 着て でかける',
                'explanation_en': '"あたたかい 服を 着て でかけたいです"',
            },
        ],
    },
    {
        'id': 'n4.read.003',
        'level': 'easy',
        'topic': 'family',
        'title_ja': 'わたしの 家族',
        'ja': 'わたしの 家族は 五人です。父と 母と 兄が 一人、妹が 一人 います。父は 会社員で、母は 先生です。兄は 大学生で、東京に 住んでいます。妹は 高校生です。わたしたちは 毎週 日曜日に いっしょに 食事を します。',
        'questions': [
            {
                'q': 'この人の 家族は 何人ですか。',
                'choices': ['三人', '四人', '五人', '六人'],
                'correct': '五人',
                'explanation_en': '"わたしの 家族は 五人です"',
            },
            {
                'q': '兄は どこに すんでいますか。',
                'choices': ['おおさか', 'きょうと', '東京', '北海道'],
                'correct': '東京',
                'explanation_en': '"兄は 大学生で、東京に 住んでいます"',
            },
            {
                'q': '家族は いつ いっしょに 食事を しますか。',
                'choices': ['毎日', '毎週 土曜日', '毎週 日曜日', '毎月'],
                'correct': '毎週 日曜日',
                'explanation_en': '"毎週 日曜日に いっしょに 食事を します"',
            },
        ],
    },
    {
        'id': 'n4.read.004',
        'level': 'medium',
        'topic': 'travel',
        'title_ja': 'きょうと旅行',
        'ja': '先月、わたしは 友だちと きょうとに 行きました。新かんせんで 東京から きょうとまで 二時間半 かかりました。きょうとでは 古い おてらを いくつか 見ました。おてらの 中は しずかで、きれいでした。お昼は きょうとの 有名な 料理を 食べました。とても おいしかったです。また 行きたいと 思います。',
        'questions': [
            {
                'q': 'いつ きょうとに 行きましたか。',
                'choices': ['今日', 'きのう', '先月', '去年'],
                'correct': '先月',
                'explanation_en': '"先月、わたしは 友だちと きょうとに 行きました"',
            },
            {
                'q': '東京から きょうとまで どのくらい かかりましたか。',
                'choices': ['一時間', '二時間半', '三時間', '四時間'],
                'correct': '二時間半',
                'explanation_en': '"二時間半 かかりました"',
            },
            {
                'q': 'きょうとで 何を 食べましたか。',
                'choices': ['アメリカの 料理', 'きょうとの 有名な 料理', '中国の 料理', '何も 食べなかった'],
                'correct': 'きょうとの 有名な 料理',
                'explanation_en': '"きょうとの 有名な 料理を 食べました"',
            },
        ],
    },
    {
        'id': 'n4.read.005',
        'level': 'medium',
        'topic': 'shopping',
        'title_ja': 'デパートでの かいもの',
        'ja': 'きのう、わたしは デパートに 行きました。妹の たんじょうびの プレゼントを かいたかったです。一かいで かわいい かばんを 見ましたが、たかかったので、かいませんでした。三かいで 安くて きれいな ぼうしを 見つけました。それを かいました。妹は きっと よろこぶと 思います。',
        'questions': [
            {
                'q': 'なぜ デパートに 行きましたか。',
                'choices': ['自分の たんじょうびの プレゼントを かうため', '妹の たんじょうびの プレゼントを かうため', '友だちと あうため', 'りょこうの じゅんびのため'],
                'correct': '妹の たんじょうびの プレゼントを かうため',
                'explanation_en': '"妹の たんじょうびの プレゼントを かいたかったです"',
            },
            {
                'q': 'なぜ 一かいの かばんを かいませんでしたか。',
                'choices': ['きれいじゃ なかったから', 'たかかったから', 'いろが よくなかったから', 'ちいさかったから'],
                'correct': 'たかかったから',
                'explanation_en': '"たかかったので、かいませんでした"',
            },
        ],
    },
    {
        'id': 'n4.read.006',
        'level': 'medium',
        'topic': 'study',
        'title_ja': '日本語の 勉強',
        'ja': 'わたしは 日本語を 勉強しはじめて 一年に なります。さいしょは ひらがなも わからなかったですが、今は かんじも すこし よめます。先生は とても しんせつで、わたしが わからない時は ゆっくり せつめいして くれます。週に 三かい クラスに 行って、毎日 三十分 ふくしゅうします。日本人の 友だちと 話すことが、いちばん 楽しいです。',
        'questions': [
            {
                'q': 'いつから 日本語を 勉強していますか。',
                'choices': ['一か月前', '半年前', '一年前', '二年前'],
                'correct': '一年前',
                'explanation_en': '"日本語を 勉強しはじめて 一年に なります"',
            },
            {
                'q': '一週間に 何かい クラスに 行きますか。',
                'choices': ['一かい', '二かい', '三かい', '毎日'],
                'correct': '三かい',
                'explanation_en': '"週に 三かい クラスに 行って"',
            },
            {
                'q': 'いちばん 楽しいことは 何ですか。',
                'choices': ['先生と 話すこと', '日本人の 友だちと 話すこと', 'かんじを よむこと', 'ふくしゅうすること'],
                'correct': '日本人の 友だちと 話すこと',
                'explanation_en': '"日本人の 友だちと 話すことが、いちばん 楽しいです"',
            },
        ],
    },
    {
        'id': 'n4.read.007',
        'level': 'medium',
        'topic': 'food',
        'title_ja': '日本の 食べ物',
        'ja': '日本には おいしい 食べ物が たくさん あります。わたしの すきな 食べ物は すしと ラーメンです。すしは あまり たかくない店で 食べることが できます。ラーメンは みせによって あじが ちがいます。今度の 週まつ、新しい ラーメン店に 行ってみたいです。',
        'questions': [
            {
                'q': 'この人の すきな 食べ物は 何ですか。',
                'choices': ['てんぷらと そば', 'すしと ラーメン', 'うどんと カレー', 'おこのみやきと たこやき'],
                'correct': 'すしと ラーメン',
                'explanation_en': '"わたしの すきな 食べ物は すしと ラーメンです"',
            },
            {
                'q': 'ラーメンに ついて 何と 言っていますか。',
                'choices': ['いつも おなじ あじ', 'みせに よって あじが ちがう', 'たかい', 'からい'],
                'correct': 'みせに よって あじが ちがう',
                'explanation_en': '"ラーメンは みせによって あじが ちがいます"',
            },
        ],
    },
    {
        'id': 'n4.read.008',
        'level': 'hard',
        'topic': 'work',
        'title_ja': '新しい 仕事',
        'ja': 'わたしは 来月から 新しい 会社で はたらく ことに なりました。今までの 会社では 五年間 はたらきましたが、もっと 大きい 会社に いきたかったので、てんしょく しました。新しい 会社は 駅から 近くて、たてものも きれいです。どうりょうの 人たちは みんな しんせつそうです。きんちょうしますが、楽しみにしています。',
        'questions': [
            {
                'q': 'いつから 新しい 仕事を 始めますか。',
                'choices': ['今日', '来週', '来月', '来年'],
                'correct': '来月',
                'explanation_en': '"来月から 新しい 会社で はたらく ことに なりました"',
            },
            {
                'q': 'なぜ てんしょく しましたか。',
                'choices': ['前の 会社が きらいだったから', 'もっと 大きい 会社に いきたかったから', 'お金が ほしかったから', '家から 近かったから'],
                'correct': 'もっと 大きい 会社に いきたかったから',
                'explanation_en': '"もっと 大きい 会社に いきたかったので、てんしょく しました"',
            },
            {
                'q': '新しい 会社の ばしょは どうですか。',
                'choices': ['駅から とおい', '駅から 近い', 'いなかに ある', '海の そばに ある'],
                'correct': '駅から 近い',
                'explanation_en': '"駅から 近くて"',
            },
        ],
    },
    {
        'id': 'n4.read.009',
        'level': 'medium',
        'topic': 'health',
        'title_ja': 'びょういん',
        'ja': '今朝、おなかが いたかったので、びょういんに 行きました。お医者さんは わたしを みてから、「だいじょうぶです。たくさん 休んで ください」と 言いました。くすりも もらいました。三日間、しごとを 休まなければ なりません。一日 三かい くすりを 飲んで、はやく よく なりたいです。',
        'questions': [
            {
                'q': 'なぜ びょういんに 行きましたか。',
                'choices': ['あたまが いたかったから', 'おなかが いたかったから', 'けがを したから', 'かぜを ひいたから'],
                'correct': 'おなかが いたかったから',
                'explanation_en': '"おなかが いたかったので、びょういんに 行きました"',
            },
            {
                'q': '何日 しごとを 休みますか。',
                'choices': ['一日', '二日', '三日', '一週間'],
                'correct': '三日',
                'explanation_en': '"三日間、しごとを 休まなければ なりません"',
            },
            {
                'q': '一日に 何かい くすりを 飲みますか。',
                'choices': ['一かい', '二かい', '三かい', '四かい'],
                'correct': '三かい',
                'explanation_en': '"一日 三かい くすりを 飲んで"',
            },
        ],
    },
    {
        'id': 'n4.read.010',
        'level': 'hard',
        'topic': 'opinion',
        'title_ja': 'うんどうの たいせつさ',
        'ja': '今の 時代、たくさんの 人は あまり うんどうしません。コンピューターや スマートフォンの まえに ずっと すわっていることが 多いです。しかし、けんこうのために うんどうは とても たいせつだと 思います。毎日 三十分でも 歩けば、からだが 元気になります。わたしは 朝、駅まで 歩いて 行くように しています。みなさんも 何か 始めて みませんか。',
        'questions': [
            {
                'q': 'なぜ 今の 人は あまり うんどうしませんか。',
                'choices': ['いそがしいから', 'コンピューターや スマートフォンの まえに ずっと すわっているから', 'うんどうが きらいだから', 'お金が かかるから'],
                'correct': 'コンピューターや スマートフォンの まえに ずっと すわっているから',
                'explanation_en': '"コンピューターや スマートフォンの まえに ずっと すわっていることが 多いです"',
            },
            {
                'q': 'この人は 朝 何を しますか。',
                'choices': ['ジョギング', '駅まで 歩いて 行く', 'たいそう', 'なにも しない'],
                'correct': '駅まで 歩いて 行く',
                'explanation_en': '"わたしは 朝、駅まで 歩いて 行くように しています"',
            },
            {
                'q': 'この人の 意見は 何ですか。',
                'choices': ['うんどうは ひつようない', 'コンピューターは よくない', 'けんこうのために うんどうは たいせつ', '駅まで 歩くのが しんどい'],
                'correct': 'けんこうのために うんどうは たいせつ',
                'explanation_en': '"けんこうのために うんどうは とても たいせつだと 思います"',
            },
        ],
    },
]

# JA-20 compliance: every kanji in a choice must appear in the passage.
# When a choice's kanji isn't in the passage, render the choice in kana.
# (Loses some kanji-recognition pedagogy but ensures the test format stays
# valid — distractors can't be eliminated by mismatched kanji alone.)
import re
KANJI_RE_LOCAL = re.compile(r'[一-鿿]')

def kana_fold_for_passage(choice, passage_text):
    """Replace each kanji char in `choice` not present in `passage_text` with
    a hiragana approximation. Heuristic table for common numeric / counter
    kanji; otherwise returns the choice as-is and JA-20 will flag (caller
    must hand-fix)."""
    KANA_MAP = {
        '一': 'いち', '二': 'に', '三': 'さん', '四': 'よん', '五': 'ご',
        '六': 'ろく', '七': 'なな', '八': 'はち', '九': 'きゅう', '十': 'じゅう',
        '今': 'いま', '日': 'にち', '前': 'まえ', '半': 'はん', '月': 'げつ',
        '北': 'きた', '海': 'うみ', '道': 'みち', '土': 'ど', '週': 'しゅう',
        '中': 'ちゅう', '国': 'こく', '何': 'なに',
        '自': 'じ', '分': 'ぶん', '友': 'とも', '年': 'ねん',
        '金': 'きん', '家': 'いえ', '時': 'じ', '間': 'かん',
        '人': 'にん',
    }
    out = []
    for c in choice:
        if KANJI_RE_LOCAL.match(c) and c not in passage_text:
            out.append(KANA_MAP.get(c, c))
        else:
            out.append(c)
    return ''.join(out)

# Build entries
entries = []
for p in PASSAGES:
    passage_text = p['ja']
    questions = []
    for i, q in enumerate(p['questions'], 1):
        # JA-20: kana-fold any choice whose kanji aren't in the passage
        folded_choices = [kana_fold_for_passage(c, passage_text) for c in q['choices']]
        folded_correct = kana_fold_for_passage(q['correct'], passage_text)
        questions.append({
            'id': f'{p["id"]}.q{i}',
            'prompt_ja': q['q'],
            'choices': folded_choices,
            'correctAnswer': folded_correct,
            'explanation_en': q['explanation_en'],
            'format_role': 'primary' if i == 1 else 'extra',
        })
    entries.append({
        'id': p['id'],
        'level': p['level'],
        'topic': p['topic'],
        'title_ja': p['title_ja'],
        'ja': p['ja'],
        'audio': f'audio/reading/{p["id"]}.mp3',
        'questions': questions,
        'tier': 'core_n4',
        'voice': 'synthetic',
        'review_status': 'llm_authored_curated',
    })

print(f'Generated {len(entries)} reading passages')

payload = {
    '_meta': {
        'schema_version': 1,
        'entity_count': len(entries),
        'id_range': 'n4.read.001..',
        'id_gap_policy': 'Numeric IDs reserved per passage; never re-used.',
        'history': [
            {'date': '2026-05-04',
             'delta': f'+{len(entries)} N4 reading passages (curated seed; native review pending)'},
        ],
    },
    'passages': entries,
}
(ROOT / 'data' / 'reading.json').write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'data/reading.json written')
