"""Close 14 fixable items from the 2026-05-04 goi audit.

Out of 19 reported issues:
  - 4 Critical: all rewritten (Q21, Q94, Q98, Q99)
  - 5 Moderate (item-level): Q39, Q68, Q79 (caveat), Q89, Q45
  - 5 Minor polish: Q1, Q5, Q10, Q19 (skipping Q33, Q12, Q27 per audit notes)
  - Q70/Q76/Q86/Q97/Q100 inference-paraphrase cluster: documented at
    header level rather than per-item rewrite (per audit's
    recommendation #2: "Decide a policy on the inference-style
    paraphrases. ... document that decision and stop apologizing for
    it in the rationale field").
  - Q47/Q48/Q62/Q64/Q91/Q97 N4 leakage: documented at header level
    as a "late N5 stretch" policy.
  - Q82 weather: audit says acceptable; no fix.

Updates BOTH:
  - KnowledgeBank/goi_questions_n5.md (source MD)
  - data/papers/goi/paper-{N}.json (extracted paper JSONs)

Idempotent. JA-32 (paper rationale ↔ MD parity) honored: every kanji
in new content also lives in MD Q-blocks.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / 'KnowledgeBank' / 'goi_questions_n5.md'
PAPERS = ROOT / 'data' / 'papers' / 'goi'

changes: list[str] = []


# (paper_n, qid) -> dict of fields to update
# 'stem_html', 'choices', 'correctIndex', 'rationale' — any subset
JSON_FIXES = {
    # =========== Critical ===========
    # Q21/goi-2.6: rewrite stem to anchor うえ via 「から おちました」 verb
    (2, 'goi-2.6'): {
        'stem_html': 'ほんが つくえの （　　）から おちました。',
        'rationale': 'things fall from above; おちる anchors うえ uniquely (a book cannot fall from under, in front of, or behind a desk — only from on top of it).',
    },
    # Q94/goi-7.4: replace choice #3 with true polite-form paraphrase
    (7, 'goi-7.4'): {
        'choices': [
            'この みせの ケーキは あまいです。',
            'この みせの ケーキは からい です。',
            'この みせの ケーキは あまく ありません。',
            'この みせの ケーキは おいしくないです。',
        ],
        'rationale': 'あまくない (plain neg) = あまく ありません (polite neg). Same meaning, different politeness register; a true paraphrase rather than a graded approximation.',
    },
    # Q98/goi-7.8: replace whole item with cleaner 出す ↔ わたす paraphrase
    (7, 'goi-7.8'): {
        'stem_html': 'A: わたしは あした しゅくだいを 出します。',
        'choices': [
            'あした しゅくだいを はじめます。',
            'あした、 わたしは 先生に しゅくだいを わたします。',
            'あした しゅくだいを かいます。',
            'あした しゅくだいを かえします。',
        ],
        'correctIndex': 1,
        'rationale': '(homework + 先生に) 出す ≈ わたす. Submitting homework to a teacher is paraphrased as handing it over.',
    },
    # Q99/goi-7.9: replace with origin → nationality paraphrase
    (7, 'goi-7.9'): {
        'stem_html': 'A: わたしは スペインから きました。',
        'choices': [
            'わたしは スペインへ いきます。',
            'わたしは スペイン人です。',
            'わたしは スペインの 人と ともだちです。',
            'わたしは スペインごを 話します。',
        ],
        'correctIndex': 1,
        'rationale': 'X から きた (came from X) = X 人 (X-jin / from X). Origin-of-coming = nationality.',
    },

    # =========== Moderate ===========
    # Q39/goi-3.9: swap noun 机 → ボール (because 〜つ takes generic objects, not furniture)
    (3, 'goi-3.9'): {
        'stem_html': 'きょうしつには ボールが 五（　　） あります。',
        'rationale': '〜つ is the generic native counter for small objects (1-9). ボール (ball) takes 〜つ at N5 level. (Furniture like つくえ takes 〜台 (だい) idiomatically — N4-level distinction.)',
    },
    # Q68/goi-5.8: 学生 → 人 (broader scope, matches だれも)
    (5, 'goi-5.8'): {
        'choices': [
            'きょうしつに 人が いません。',
            'きょうしつに 一人 います。',
            'きょうしつに 二人 います。',
            'きょうしつに 学生が おおぜい います。',
        ],
        'rationale': 'だれも (no one — universal over people) ↔ 人が いません (no people). Both negate the existence of any person, so the scope matches exactly.',
    },
    # Q79/goi-6.4: add caveat to align with Q80's style
    (6, 'goi-6.4'): {
        'rationale': 'by elimination among the four options. Strictly, 大きくない (not big) is broader than ちいさい (small) — 中ぐらい (medium-sized) also fits 大きくない. Among the four options, ちいさい is the closest single-word match.',
    },
    # Q89/goi-6.14: rewrite keyed; 「高い お金」 is unnatural
    (6, 'goi-6.14'): {
        'choices': [
            'その くつは とても やすいです。',
            'その くつに とても たくさん お金を はらいました。',
            'その くつは ながかったです。',
            'その くつは よかったです。',
        ],
        'rationale': '高かった (was expensive) ↔ たくさん お金を 払った (paid a lot of money). Note: 「高い お金」 is unnatural — money is not 高い/安い; ねだん (price) is. Hence the rewording from a prior version.',
    },
    # Q45/goi-3.15: シャツ → パジャマ (clearly indoor, not cold-weather garment)
    (3, 'goi-3.15'): {
        'choices': ['ぼうし', 'かばん', 'コート', 'パジャマ'],
        'rationale': 'cold + コート (coat). パジャマ (pajamas) replaces the previous シャツ distractor — a shirt is also wearable in cold weather, while pajamas are clearly an indoor / sleep garment.',
    },

    # =========== Minor polish ===========
    # Q1/goi-1.1: 毎あさ → まいあさ (consistency: avoid kanji-kana split on a single word)
    (1, 'goi-1.1'): {
        'stem_html': 'まいあさ コーヒーを （　　）。',
    },
    # Q5/goi-1.5: ますから → たので (tense consistency)
    (1, 'goi-1.5'): {
        'stem_html': 'つかれたので、いえで （　　）。',
    },
    # Q10/goi-1.10: replace あついです distractor (homophone 暑い/厚い trap) with はやいです
    (1, 'goi-1.10'): {
        'choices': ['おいしいです', 'うるさいです', 'おもしろいです', 'はやいです'],
        'rationale': '本 + おもしろい (interesting). はやい distractor replaces the prior あつい — あつい is a homophone trap (厚い "thick" is plausible for a book), so it weakens distractor quality.',
    },
    # Q19/goi-2.4: stem light on context — add topic anchor
    (2, 'goi-2.4'): {
        'stem_html': 'きのうは しごとが とても （　　）。',
        'rationale': 'past i-adj + です. しごとが いそがしい (work was busy) is the canonical N5 stem-and-answer pairing for this grammar pattern. The topic word しごと anchors いそがしい uniquely.',
    },
}


def update_paper_jsons() -> None:
    for (paper_n, qid), updates in JSON_FIXES.items():
        p_path = PAPERS / f'paper-{paper_n}.json'
        paper = json.loads(p_path.read_text(encoding='utf-8'))
        modified = False
        for q in paper.get('questions', []):
            if q.get('id') != qid:
                continue
            for k, v in updates.items():
                if q.get(k) != v:
                    q[k] = v
                    modified = True
                    changes.append(f'paper-{paper_n}.json {qid}: updated {k}')
        if modified:
            p_path.write_text(json.dumps(paper, ensure_ascii=False, indent=2),
                              encoding='utf-8')


# =====================================================================
# MD source updates — by Q-number, full block replacement
# =====================================================================
# Each entry: (kb_qnum, full_replacement_text). The replacement starts
# with `### Q<N>` and ends just before the blank line before the next
# question.
MD_REPLACEMENTS: dict[str, str] = {
    'Q1': '''### Q1

まいあさ コーヒーを （　　）。

1. たべます
2. のみます
3. ききます
4. みます

**Answer: 2** - コーヒー is something one drinks (のむ).''',

    'Q5': '''### Q5

つかれたので、いえで （　　）。

1. はたらきます
2. やすみます
3. はしります
4. およぎます

**Answer: 2** - つかれた + やすむ.''',

    'Q10': '''### Q10

その 本は とても （　　）。

1. おいしいです
2. うるさいです
3. おもしろいです
4. はやいです

**Answer: 3** - 本 + おもしろい (interesting). はやい distractor replaces the prior あつい - あつい is a homophone trap (厚い "thick" is plausible for a book).''',

    'Q19': '''### Q19

きのうは しごとが とても （　　）。

1. つよいでした
2. つかれます
3. はやいです
4. いそがしかったです

**Answer: 4** - past i-adj + です. しごとが いそがしい (work was busy) is the canonical N5 stem-and-answer pairing for this grammar pattern.''',

    'Q21': '''### Q21

ほんが つくえの （　　）から おちました。

1. うえ
2. した
3. まえ
4. うしろ

**Answer: 1** - things fall from above; おちる anchors うえ uniquely (a book cannot fall from under, in front of, or behind a desk - only from on top of it).''',

    'Q39': '''### Q39

きょうしつには ボールが 五（　　） あります。

1. にん
2. つ
3. まい
4. ほん

**Answer: 2** - 〜つ is the generic native counter for small objects (1-9). ボール (ball) takes 〜つ at N5 level. (Furniture like つくえ takes 〜台 (だい) idiomatically - N4-level distinction.)''',

    'Q45': '''### Q45

さむいですから、（　　） を きて ください。

1. ぼうし
2. かばん
3. コート
4. パジャマ

**Answer: 3** - cold + コート (coat). パジャマ replaces the prior シャツ distractor - a shirt is also wearable in cold weather, while pajamas are clearly an indoor / sleep garment.''',

    'Q68': '''### Q68

A: だれも きょうしつに いません。

_There is no one in the classroom._

1. きょうしつに 人が いません。
2. きょうしつに 一人 います。
3. きょうしつに 二人 います。
4. きょうしつに 学生が おおぜい います。

**Answer: 1** - だれも (no one - universal over people) = 人が いません (no people). Both negate the existence of any person, so the scope matches exactly.''',

    'Q79': '''### Q79

A: たなかさんの いえは 大きくないです。

_Tanaka-san\'s house is not big._

1. たなかさんの いえは 大きいです。
2. たなかさんの いえは ちいさいです。
3. たなかさんの いえは あたらしいです。
4. たなかさんの いえは ふるいです。

**Answer: 2** - by elimination among the four options. Strictly, 大きくない (not big) is broader than ちいさい (small) - 中ぐらい (medium-sized) also fits 大きくない. Among the four options, ちいさい is the closest single-word match.''',

    'Q89': '''### Q89

A: その くつは 高かったです。

_Those shoes were expensive._

1. その くつは とても やすいです。
2. その くつに とても たくさん お金を はらいました。
3. その くつは ながかったです。
4. その くつは よかったです。

**Answer: 2** - 高かった (was expensive) = たくさん お金を 払った (paid a lot of money). Note: 「高い お金」 is unnatural Japanese - money is not 高い/安い; ねだん (price) is. Hence the rewording from a prior version.''',

    'Q94': '''### Q94

A: この みせの ケーキは あまくないです。

_The cake at this shop is not sweet._

1. この みせの ケーキは あまいです。
2. この みせの ケーキは からい です。
3. この みせの ケーキは あまく ありません。
4. この みせの ケーキは おいしくないです。

**Answer: 3** - あまくない (plain neg) = あまく ありません (polite neg). Same meaning, different politeness register; a true paraphrase rather than a graded approximation.''',

    'Q98': '''### Q98

A: わたしは あした しゅくだいを 出します。

_I will submit my homework tomorrow._

1. あした しゅくだいを はじめます。
2. あした、 わたしは 先生に しゅくだいを わたします。
3. あした しゅくだいを かいます。
4. あした しゅくだいを かえします。

**Answer: 2** - (homework + 先生に) 出す = わたす. Submitting homework to a teacher is paraphrased as handing it over.''',

    'Q99': '''### Q99

A: わたしは スペインから きました。

_I came from Spain._

1. わたしは スペインへ いきます。
2. わたしは スペイン人です。
3. わたしは スペインの 人と ともだちです。
4. わたしは スペインごを 話します。

**Answer: 2** - X から きた (came from X) = X 人 (X-jin / from X). Origin-of-coming = nationality.''',
}


def update_md_source() -> None:
    text = KB.read_text(encoding='utf-8')
    original_text = text
    for qnum, replacement in MD_REPLACEMENTS.items():
        # Find the existing block: from "### Q<N>\n" through end of last
        # blank line before the next "### Q" header.
        block_re = re.compile(
            rf'### {re.escape(qnum)}\b[\s\S]+?(?=\n### Q\d|\n## )'
        )
        m = block_re.search(text)
        if m is None:
            changes.append(f'goi_questions_n5.md {qnum}: NOT FOUND (skipped)')
            continue
        if m.group(0).strip() == replacement.strip():
            continue  # idempotent — already in fixed state
        text = text[:m.start()] + replacement + '\n' + text[m.end():]
        changes.append(f'goi_questions_n5.md {qnum}: replaced block')
    if text != original_text:
        KB.write_text(text, encoding='utf-8')


# =====================================================================
# Header policy notes (inference paraphrase + N4 stretch)
# =====================================================================
HEADER_POLICY = '''## Audit policies (formalized 2026-05-04)

### Inference-style paraphrases (Mondai 4 / 言い換え類義)

A small cluster of paraphrase items in Papers 6-7 (Q70 好き/よくする,
Q76 おちゃより/コーヒーよく飲む, Q86 でんわをかける/でんわで話す, Q97
じょうず/よくはなせる, Q100 ならっている/れんしゅう) treats real-world
inference as paraphrase rather than strict semantic equivalence. The
project accepts this as a deliberate N5-level pedagogical convention:
likes/skill/lessons commonly entail the related action at the
introductory level, even though strict logic admits exceptions
(fans who don\'t play, listeners who don\'t speak, etc.). Each
rationale notes the specific gap; the items are graded by closeness
among the four offered options, not by exact synonymy.

### Borderline N5 / late-N5 stretch items

Six items in this corpus rely on grammar that is canonically tested
at N4 rather than N5:

  Q47  ～たことがあります  (experience past)
  Q48  ～つもりです        (intent)
  Q62  ～あいだに          (during which)
  Q64  potential form ひけます
  Q91  ～て、N に なります (duration)
  Q97  potential form 話せます

Each is included because the structure is encountered at the strict
N5/N4 boundary and the keyed answer remains correct under the
construction. Per the project\'s "late_n5" tier convention (also
applied in grammar.json with 25 patterns flagged tier=late_n5), these
items are positioned as **stretch content** for learners on the cusp
of N4. Strict-N5 deployments may filter to questions outside this
list.

'''


def update_header_policy() -> None:
    text = KB.read_text(encoding='utf-8')
    if 'Audit policies (formalized 2026-05-04)' in text:
        return  # idempotent
    # Insert just before the first `### Q1` header.
    m = re.search(r'\n### Q1\b', text)
    if m is None:
        return
    text = text[:m.start()] + '\n' + HEADER_POLICY + text[m.start():]
    KB.write_text(text, encoding='utf-8')
    changes.append('goi_questions_n5.md: header policy notes inserted')


def main() -> int:
    update_md_source()
    update_paper_jsons()
    update_header_policy()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
