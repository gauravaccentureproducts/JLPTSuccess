"""Tighten the 5 inference-paraphrase cluster items from the goi audit.

Audit (2026-05-04) flagged Q70, Q76, Q86, Q97, Q100 as relying on
real-world inference rather than strict semantic equivalence:

  Q70   好き           ↔  よくする
  Q76   X より Y すき  ↔  Y を よく 飲む
  Q86   電話を かける  ↔  電話で 話す
  Q97   じょうず       ↔  よく 話せる   (also: 話せる is N4 potential)
  Q100  ならって いる  ↔  れんしゅう

Audit recommended "tighten at least two of them so that the pattern
doesn't dominate." Per "fix all fixables", tightening all five.

Approach: add explicit context to each stem so the keyed answer
becomes a direct (rather than inferred) paraphrase.

Q97 also drops the N4 potential form 話せます as bonus.

Idempotent. JA-32 honored.
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


JSON_FIXES = {
    # Q70/goi-5.10: add frequency 「まいにち します」 to stem
    (5, 'goi-5.10'): {
        'stem_html': 'A: たろうさんは スポーツが すきで、 まいにち します。',
        'rationale': '「すき + まいにち する」 = 「よく する」. The frequency context makes this a direct paraphrase rather than an inference from liking alone.',
    },
    # Q76/goi-6.1: add frequency 「まいにち 飲みます」
    (6, 'goi-6.1'): {
        'stem_html': 'A: わたしは おちゃより コーヒーの ほうが すきで、 まいにち 飲みます。',
        'rationale': '「コーヒーの ほうが すき + まいにち 飲む」 = 「コーヒーを よく 飲む」. The frequency clause makes the preference paraphrase direct.',
    },
    # Q86/goi-6.11: add successful-conversation context 「一時間 話しました」
    (6, 'goi-6.11'): {
        'stem_html': 'A: 友だちに でんわを かけて、 一時間 話しました。',
        'rationale': '「電話を かけて + 一時間 話した」 = 「電話で 話した」. The "talked for one hour" context confirms a successful conversation, removing the inference gap.',
    },
    # Q97/goi-7.7: scope じょうず to speaking + drop potential 話せます
    (7, 'goi-7.7'): {
        'stem_html': 'A: たろうさんは 日本ごを 話すのが じょうずです。',
        'choices': [
            'たろうさんは 日本ごを 上手に 話します。',
            'たろうさんは 日本ごが ぜんぜん わかりません。',
            'たろうさんは 日本ごが すきじゃ ありません。',
            'たろうさんは 日本ごを ならって います。',
        ],
        'rationale': '「話すのが じょうず」 = 「上手に 話す」. Same skill, different syntactic frame (nominalized adjective vs. adverbial). Strict-N5: also drops the potential form 話せます (N4) used in a previous version.',
    },
    # Q100/goi-7.10: add practice context 「まいにち れんしゅうします」
    (7, 'goi-7.10'): {
        'stem_html': 'A: わたしは ピアノを ならって、 まいにち れんしゅうします。',
        'rationale': '「ならって + まいにち れんしゅうする」 = 「れんしゅうを して いる」. Lessons + daily practice is a direct paraphrase of "doing practice", not an inference from "is taking lessons".',
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


MD_REPLACEMENTS = {
    'Q70': '''### Q70

A: たろうさんは スポーツが すきで、 まいにち します。

_Taro likes sports and does them every day._

1. たろうさんは スポーツを よく します。
2. たろうさんは スポーツを 見ません。
3. たろうさんは スポーツを ぜんぜん しません。
4. たろうさんは スポーツが きらいです。

**Answer: 1** - 「すき + まいにち する」 = 「よく する」. The frequency context makes this a direct paraphrase rather than an inference from liking alone.''',

    'Q76': '''### Q76

A: わたしは おちゃより コーヒーの ほうが すきで、 まいにち 飲みます。

_I prefer coffee to tea, and drink it every day._

1. わたしは コーヒーより おちゃの ほうが すきです。
2. わたしは おちゃと コーヒーが すきです。
3. わたしは おちゃが きらいで、コーヒーが すきです。
4. わたしは コーヒーを よく のみます。

**Answer: 4** - 「コーヒーの ほうが すき + まいにち 飲む」 = 「コーヒーを よく 飲む」. The frequency clause makes the preference paraphrase direct.''',

    'Q86': '''### Q86

A: 友だちに でんわを かけて、 一時間 話しました。

_I called my friend and we talked for an hour._

1. 友だちが でんわを くれました。
2. 友だちと でんわで 話しました。
3. でんわを 買いました。
4. 友だちに 手紙を 書きました。

**Answer: 2** - 「電話を かけて + 一時間 話した」 = 「電話で 話した」. The "talked for one hour" context confirms a successful conversation, removing the inference gap.''',

    'Q97': '''### Q97

A: たろうさんは 日本ごを 話すのが じょうずです。

_Taro is good at speaking Japanese._

1. たろうさんは 日本ごを 上手に 話します。
2. たろうさんは 日本ごが ぜんぜん わかりません。
3. たろうさんは 日本ごが すきじゃ ありません。
4. たろうさんは 日本ごを ならって います。

**Answer: 1** - 「話すのが じょうず」 = 「上手に 話す」. Same skill, different syntactic frame (nominalized adjective vs. adverbial). Strict-N5: also drops the potential form 話せます (N4) used in a previous version.''',

    'Q100': '''### Q100

A: わたしは ピアノを ならって、 まいにち れんしゅうします。

_I'm taking piano lessons and practice every day._

1. わたしは ピアノが よく わかります。
2. わたしは ピアノを 売って います。
3. わたしは ピアノを 買いました。
4. わたしは ピアノの れんしゅうを して います。

**Answer: 4** - 「ならって + まいにち れんしゅうする」 = 「れんしゅうを して いる」. Lessons + daily practice is a direct paraphrase of "doing practice", not an inference from "is taking lessons".''',
}


def update_md_source() -> None:
    text = KB.read_text(encoding='utf-8')
    original_text = text
    for qnum, replacement in MD_REPLACEMENTS.items():
        block_re = re.compile(
            rf'### {re.escape(qnum)}\b[\s\S]+?(?=\n### Q\d|\n## )'
        )
        m = block_re.search(text)
        if m is None:
            changes.append(f'goi_questions_n5.md {qnum}: NOT FOUND (skipped)')
            continue
        if m.group(0).strip() == replacement.strip():
            continue
        text = text[:m.start()] + replacement + '\n' + text[m.end():]
        changes.append(f'goi_questions_n5.md {qnum}: replaced block (tightened)')
    if text != original_text:
        KB.write_text(text, encoding='utf-8')


def revise_inference_policy_header() -> None:
    """The v1.12.12 header documented Q70/Q76/Q86/Q97/Q100 as deliberate
    inference convention. After tightening, that framing is no longer
    accurate — the items are now direct paraphrases. Revise the section
    to record what happened."""
    text = KB.read_text(encoding='utf-8')
    OLD = '''### Inference-style paraphrases (Mondai 4 / 言い換え類義)

A small cluster of paraphrase items in Papers 6-7 (Q70 好き/よくする,
Q76 おちゃより/コーヒーよく飲む, Q86 でんわをかける/でんわで話す, Q97
じょうず/よくはなせる, Q100 ならっている/れんしゅう) treats real-world
inference as paraphrase rather than strict semantic equivalence. The
project accepts this as a deliberate N5-level pedagogical convention:
likes/skill/lessons commonly entail the related action at the
introductory level, even though strict logic admits exceptions
(fans who don\'t play, listeners who don\'t speak, etc.). Each
rationale notes the specific gap; the items are graded by closeness
among the four offered options, not by exact synonymy.'''

    NEW = '''### Paraphrase-tightening pass (2026-05-04, v1.12.13)

Five paraphrase items in Papers 5-7 originally relied on real-world
inference rather than strict semantic equivalence:

  Q70   好き              ->  よく する
  Q76   X より Y すき      ->  Y を よく 飲む
  Q86   電話を かける      ->  電話で 話した
  Q97   じょうず           ->  よく 話せる    (also dropped N4 potential 話せます)
  Q100  ならって いる      ->  れんしゅう

Each stem was tightened in v1.12.13 by adding explicit context that
makes the keyed answer a direct paraphrase rather than an inference:
  - Q70/Q76/Q100 add a frequency clause (「まいにち する」 etc.)
  - Q86 adds the duration of conversation (「一時間 話しました」)
  - Q97 scopes じょうず to "speaking" specifically (「話すのが じょうず」)
    and replaces 話せます (N4 potential) with 上手に 話します (N5 plain).

The rationales no longer carry "by elimination" or "closest among the
four" hedges - these are now true paraphrases.'''

    if OLD in text:
        text = text.replace(OLD, NEW)
        KB.write_text(text, encoding='utf-8')
        changes.append('goi_questions_n5.md: revised inference-paraphrase policy section to reflect tightening')


def main() -> int:
    update_md_source()
    update_paper_jsons()
    revise_inference_policy_header()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
