"""Iteration 2: choice-length asymmetry fixes (16 items).

Best-in-class JLPT prep books keep distractor lengths roughly balanced
with the keyed answer to avoid a length-signal cue. This iteration
reshapes distractors in 16 dokkai items to bring max/min length ratio
under 2.5x.

Strategy per item:
- Keep correctIndex and keyed answer text exactly as-is.
- Reshape ONLY the distractors that are length-asymmetric.
- New distractors must:
  * Stay within strict-N5 (or dokkai-exception) kanji bounds
  * Be plausible given the passage (not absurd)
  * Match the keyed answer's length within ~50%

bunpou-5.15 (Q75) skipped: Mondai 2 sentence-rearrangement, fragments
have semantic positions that cannot be permuted. Length asymmetry is
inherent to the format.

Idempotent.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KB_DOKKAI = ROOT / 'KnowledgeBank/dokkai_questions_n5.md'

changes: list[str] = []


# Each entry: (paper_n, qid, full new choice list, correctIndex must match keyed)
# Note: correctIndex stays at the position the keyed answer ends up in.
DOKKAI_FIXES = [
    # Q5 / dokkai-1.5: keyed=コート, distractor "何も もって 来なくて いい" (14ch) → "おみやげ" (4ch).
    # All distractors now 3-4 char, matching keyed.
    (1, 'dokkai-1.5', {
        'choices': ['のみもの', 'コート', 'おかし', 'おみやげ'],
        'correctIndex': 1,
        'rationale': '\'コートを もって 来て ください\' - explicitly asks for a coat. (Distractors all single-noun for length parity.)',
    }),

    # Q22 / dokkai-2.6: keyed='家で 子どもと あそぶ' (11). Reshape distractors to ~10ch.
    (2, 'dokkai-2.6', {
        'choices': ['まいにち しごとを する', '山に のぼりに 行く', '家で 子どもと あそぶ', '家で ゆっくり ねる'],
        'correctIndex': 2,
        'rationale': '\'日曜日は いつも 家に いて 子どもと あそびます\' - parents play with the kids at home on Sundays.',
    }),

    # Q24 / dokkai-2.8: keyed='こうえんで お弁当を 食べる' (14). Reshape short distractors.
    (2, 'dokkai-2.8', {
        'choices': ['こうえんで お弁当を 食べる', '学校に いって しごとを する', '家で 一日 ねて すごす', '雨の 中を さんぽする'],
        'correctIndex': 0,
        'rationale': '\'こうえんで お弁当を 食べる つもり\' - planning to eat bento at the park.',
    }),

    # Q28 / dokkai-2.12: keyed='かいしゃの ちかくの レストラン' (16). Reshape '家'(1) etc.
    (2, 'dokkai-2.12', {
        'choices': ['駅の ちかくの きっさてん', 'かいしゃの しょくどう', 'かいしゃの ちかくの レストラン', '家の ちかくの レストラン'],
        'correctIndex': 2,
        'rationale': '\'ばんごはんは いつも かいしゃの ちかくの レストランで\' - dinner is always at a restaurant near the company.',
    }),

    # Q37 / dokkai-3.5: keyed='一しゅうかんに 三回' (10). 毎日(2) too short.
    (3, 'dokkai-3.5', {
        'choices': ['一しゅうかんに 一回', '一しゅうかんに 二回', '一しゅうかんに 三回', '一しゅうかんに 四回'],
        'correctIndex': 2,
        'rationale': '\'月曜日と 水曜日と 金曜日に\' - Mon/Wed/Fri = 3 times per week.',
    }),

    # Q58 / dokkai-4.10: keyed='コーヒーが おいしくて、ねだんも 安いから' (21). All ~15-20.
    (4, 'dokkai-4.10', {
        'choices': ['友だちが はたらいて いるから', 'コーヒーが おいしくて、ねだんも 安いから', 'みせが えきから ちかいから', 'こんで いて にぎやかだから'],
        'correctIndex': 1,
        'rationale': '\'コーヒーが おいしくて、 ねだんも 安いです\' - the coffee is good and the price is cheap.',
    }),

    # Q63 / dokkai-5.3: keyed='日本に すんで しごとを する' (15). '母と すむ'(5) too short.
    (5, 'dokkai-5.3', {
        'choices': ['日本に すんで しごとを する', '大学いんに 入って べんきょうする', '父と いっしょに 先生に なる', '母と いっしょに 国へ かえる'],
        'correctIndex': 0,
        'rationale': '\'大学を そつぎょうしてから、日本に すんで しごとを するつもり\' - plans to live and work in Japan after graduation.',
    }),

    # Q65 / dokkai-5.5: keyed='こわかったが、いい けいけんだった' (17). Distractors 6-7.
    (5, 'dokkai-5.5', {
        'choices': ['こわかったが、いい けいけんだった', 'たのしくて すぐ なれた', 'むずかしくて つまらなかった', 'とても じょうずに ひけた'],
        'correctIndex': 0,
        'rationale': '\'こわかったですが、とても いい けいけんでした\' - was scary but a good experience.',
    }),

    # Q68 / dokkai-5.8: keyed='やさいが たくさん、にくは すこし' (17). 高い(2), ピリ辛い(4).
    (5, 'dokkai-5.8', {
        'choices': ['ねだんが とても 高い', 'ピリ辛くて 食べられない', 'ふつうの カレーと 同じ', 'やさいが たくさん、にくは すこし'],
        'correctIndex': 3,
        'rationale': '\'中に やさいが たくさん 入って います。にくは すこし だけです\' - lots of vegetables, only a little meat.',
    }),

    # Q69 / dokkai-5.9: keyed='カレーの 作りかたを ならって、友だちに 作って あげる' (28). Distractors ~10-15.
    (5, 'dokkai-5.9', {
        'choices': ['母から カレーを 作って もらう', '友だちと レストランで カレーを 食べる', 'カレーやで アルバイトを はじめる', 'カレーの 作りかたを ならって、友だちに 作って あげる'],
        'correctIndex': 3,
        'rationale': '\'母から カレーの 作りかたを 教わって、友だちに 作って あげたいです\' - learn the recipe and make it for friends.',
    }),

    # Q73 / dokkai-5.13: keyed='友だちの 家 (たなかさんの 家)' (17 incl. paren). Reshape.
    # The paren is unusual; clean to just '友だちの たなかさんの 家'.
    (5, 'dokkai-5.13', {
        'choices': ['私の 家で ひらかれる', '友だちの たなかさんの 家', 'みんなで レストランへ 行く', 'こうえんで パーティーする'],
        'correctIndex': 1,
        'rationale': '\'ばしょは たなかさんの 家です\' - the venue is Tanaka-san\'s house.',
    }),

    # Q81 / dokkai-6.6: keyed='うみの ちかくの レストラン' (14). 家(1) too short.
    (6, 'dokkai-6.6', {
        'choices': ['うみの ちかくの レストラン', 'うみで お弁当を 食べる', '駅の ちかくの きっさてん', 'でんしゃの 中で 食べる'],
        'correctIndex': 0,
        'rationale': '\'ひるごはんは うみの ちかくの レストランで\' - lunch at a restaurant near the sea.',
    }),

    # Q90 / dokkai-6.15: keyed='子ども向けの 本を 書きはじめる' (16). Distractors 6-10.
    (6, 'dokkai-6.15', {
        'choices': ['子ども向けの 本やで はたらく', '子ども向けの 本を 書きはじめる', '本を 読んで しゅくだいを する', '学校で 子どもに 本を 読む'],
        'correctIndex': 1,
        'rationale': '\'来月、妹は 子ども向けの 本を 書きはじめる つもりです\' - plans to start writing children\'s books next month.',
    }),

    # Q93 / dokkai-7.3: keyed='月よう日 と 水よう日' (11). 毎日(2) too short.
    (7, 'dokkai-7.3', {
        'choices': ['月よう日 と 水よう日', '月よう日 と 火よう日', '火よう日 と 木よう日', '土よう日 と 日よう日'],
        'correctIndex': 0,
        'rationale': '\'時間: 月よう日 と 水よう日 の 7:00pm-9:00pm\' - the poster lists Mon and Wed.',
    }),

    # Q94 / dokkai-7.4: distractor '(housewife)' English gloss is the length cue.
    # Drop the English; the Japanese しゅふ stands alone.
    (7, 'dokkai-7.4', {
        'choices': ['かいしゃいん', 'しゅふ', '大学生', 'こうこうせい'],
        'correctIndex': 3,
        'rationale': '\'大人だけの きょうしつです。こうこうせいは 入れません\' - adult-only class; high schoolers cannot enter.',
    }),

    # Q102 / dokkai-7.12: keyed='先生に 言う' (6). Distractors 8-15.
    (7, 'dokkai-7.12', {
        'choices': ['学校に 来て 図書館を つかう', 'まず 先生に 言う', '土ようびに かりに 行く', '日よう日は 図書館は つかえない'],
        'correctIndex': 1,
        'rationale': '\'やすみの 日に 図書館を つかいたい 人は、先生に 言って ください\' - first ask the teacher.',
    }),
]


def apply_dokkai_fixes() -> None:
    md_text = KB_DOKKAI.read_text(encoding='utf-8')
    md_modified = False

    for paper_n, qid, fix in DOKKAI_FIXES:
        p_path = ROOT / f'data/papers/dokkai/paper-{paper_n}.json'
        paper = json.loads(p_path.read_text(encoding='utf-8'))
        modified = False
        kbid = None
        for q in paper['questions']:
            if q['id'] != qid:
                continue
            kbid = q['kbSourceId']
            for k, v in fix.items():
                if q.get(k) != v:
                    q[k] = v
                    modified = True
                    changes.append(f'paper-{paper_n}.json {qid} ({kbid}): {k} updated')
        if modified:
            p_path.write_text(json.dumps(paper, ensure_ascii=False, indent=2), encoding='utf-8')

        # Mirror to MD: rebuild the Q-block
        if kbid:
            new_md_block = f'''#### {kbid}

{paper["questions"][[i for i,q in enumerate(paper["questions"]) if q["id"]==qid][0]]["stem_html"].split("|")[0]}

{chr(10).join(f"{i+1}. {c}" for i, c in enumerate(fix["choices"]))}

**Answer: {fix["correctIndex"]+1}** - {fix["rationale"]}'''
            # We need stem_html without the leading "A: " prefix etc
            q_obj = next((q for q in paper['questions'] if q['id'] == qid), None)
            if q_obj:
                stem = q_obj['stem_html']
                new_md_block = (
                    f'#### {kbid}\n\n'
                    f'{stem}\n\n'
                    f'{chr(10).join(f"{i+1}. {c}" for i, c in enumerate(fix["choices"]))}\n\n'
                    f'**Answer: {fix["correctIndex"]+1}** - {fix["rationale"]}'
                )
            # Replace the block in MD
            block_re = re.compile(rf'#### {re.escape(kbid)}\b[\s\S]+?(?=\n####|\n###|\n## )')
            m = block_re.search(md_text)
            if m and m.group(0).strip() != new_md_block.strip():
                md_text = md_text[:m.start()] + new_md_block + '\n' + md_text[m.end():]
                md_modified = True
                changes.append(f'dokkai_questions_n5.md {kbid}: replaced block')

    if md_modified:
        KB_DOKKAI.write_text(md_text, encoding='utf-8')


def main() -> int:
    apply_dokkai_fixes()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes[:50]:
        print(f'  - {c}')
    if len(changes) > 50:
        print(f'  ... +{len(changes)-50} more')
    return 0


if __name__ == '__main__':
    sys.exit(main())
