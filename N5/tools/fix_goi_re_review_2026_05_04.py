"""Apply 5 follow-up fixes from the goi re-review (2026-05-04).

The re-review (after v1.12.13) identified:
  - Q51: tautological keyed answer (cf-of-fix from previous list NOT touched).
         Reviewer suggested stem rewrite to test real vocab.
  - Q5:  noeisedeso (-noeite) introduced N4 grammar. Revert to から.
  - Q99: weak entailment (Spain-から → Spain人). Add pragmatic-substitution
         caveat to rationale, mirroring the existing pattern for similar items.
  - Q98: わたす is borderline N5/N4 ([Ext] in vocabulary_n5.md). Strict
         adherence: flip stem ↔ keyed so わたす sits in the recognition
         position (acceptable per project [Ext] policy) and strict-N5 出す
         is the keyed answer.
  - Q94: rationale labels あまくない (plain neg) but stem is あまくないです
         (already polite via i-adj+です). Tighten labeling.

Idempotent. Lock-step MD ↔ paper-JSON updates so JA-32 stays green.
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


# ---------------------------------------------------------------------------
# JSON-side updates (paper-{1,4,7}.json)
# ---------------------------------------------------------------------------

JSON_FIXES = {
    # Q5 / goi-1.5: revert -node -> -kara (N5-canonical reason conjunction)
    (1, 'goi-1.5'): {
        'stem_html': 'つかれましたから、いえで （　　）。',
        'rationale': 'つかれた + やすむ. つかれましたから (polite past + から) is the N5-canonical reason -> action chain (replaces ので which leans N4 in major textbooks).',
    },

    # Q51 / goi-4.6: full rewrite — stem now tests vocab triangle
    # 病院/はたらく/医者 instead of the prior tautology
    # 「父は医者 = 父の仕事は医者」.
    (4, 'goi-4.6'): {
        'stem_html': 'A: わたしの ちちは びょういんで はたらいて います。',
        'choices': [
            'わたしの ちちは ははと はたらいて います。',
            'わたしの ちちは いしゃです。',
            'わたしの ちちは びょうきです。',
            'わたしの ちちは 学校の 先生です。',
        ],
        'correctIndex': 1,
        'rationale': '「病院で はたらく」 ≈ 「いしゃです」. N5 pragmatic substitution (working at a hospital is the standard textbook paraphrase of "is a doctor", though strictly someone could work at a hospital without being a doctor — nurse, admin). Tests the N5 vocab triangle 病院 / はたらく / いしゃ; replaces the prior tautological 「父は医者 = 父の仕事は医者」 which tested no vocabulary.',
    },

    # Q94 / goi-7.4: tighten rationale labelling
    (7, 'goi-7.4'): {
        'rationale': 'あまくないです (i-adj + です polite neg) = あまく ありません (formal polite neg). Two equivalent polite negative forms of i-adjectives — a true synonymy item rather than a graded approximation. Same meaning, different polite form.',
    },

    # Q98 / goi-7.8: remove わたす [Ext] entirely. New keyed verb is
    # 持って いく (strict N5: 持つ + 行く), pragmatically substituting
    # for 出す in the homework-submission context.
    (7, 'goi-7.8'): {
        'stem_html': 'A: わたしは あした しゅくだいを 出します。',
        'choices': [
            'あした しゅくだいを はじめます。',
            'あした、 わたしは しゅくだいを 先生に もって いきます。',
            'あした しゅくだいを かいます。',
            'あした しゅくだいを かえします。',
        ],
        'correctIndex': 1,
        'rationale': '「(教師に) しゅくだいを 出す」 ≈ 「先生に しゅくだいを もって いく」. Submitting homework to a teacher is paraphrased as physically taking it to them. Strict-N5: replaces the previous keyed verb わたす (vocabulary_n5.md [Ext] borderline N5/N4) with もって いく - both もつ and いく are core N5; わたす no longer appears in the goi corpus. Note: kept in kana since 持 is not in the kanji whitelist.',
    },

    # Q99 / goi-7.9: add pragmatic-substitution caveat, mirroring the
    # existing acknowledgement pattern for soft-entailment items.
    (7, 'goi-7.9'): {
        'rationale': 'X から きた ≈ X 人. N5 pragmatic substitution: at this level "came from X" is the standard textbook paraphrase of nationality, even though strictly someone could come from X without being X-jin (tourist, long-term resident, expat returning home). Closest among the four offered options.',
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


# ---------------------------------------------------------------------------
# MD-side updates (KnowledgeBank/goi_questions_n5.md)
# ---------------------------------------------------------------------------

MD_REPLACEMENTS = {
    'Q5': '''### Q5

つかれましたから、いえで （　　）。

1. はたらきます
2. やすみます
3. はしります
4. およぎます

**Answer: 2** - つかれた + やすむ. つかれましたから (polite past + から) is the N5-canonical reason -> action chain (replaces ので which leans N4 in major textbooks).''',

    'Q51': '''### Q51

A: わたしの ちちは びょういんで はたらいて います。

_My father works at a hospital._

1. わたしの ちちは ははと はたらいて います。
2. わたしの ちちは いしゃです。
3. わたしの ちちは びょうきです。
4. わたしの ちちは 学校の 先生です。

**Answer: 2** - 「病院で はたらく」 ≈ 「いしゃです」. N5 pragmatic substitution (working at a hospital is the standard textbook paraphrase of "is a doctor", though strictly someone could work at a hospital without being a doctor - nurse, admin). Tests the N5 vocab triangle 病院 / はたらく / いしゃ; replaces the prior tautological 「父は医者 = 父の仕事は医者」 which tested no vocabulary.''',

    'Q94': '''### Q94

A: この みせの ケーキは あまくないです。

_The cake at this shop is not sweet._

1. この みせの ケーキは あまいです。
2. この みせの ケーキは からい です。
3. この みせの ケーキは あまく ありません。
4. この みせの ケーキは おいしくないです。

**Answer: 3** - あまくないです (i-adj + です polite neg) = あまく ありません (formal polite neg). Two equivalent polite negative forms of i-adjectives - a true synonymy item rather than a graded approximation. Same meaning, different polite form.''',

    'Q98': '''### Q98

A: わたしは あした しゅくだいを 出します。

_I will submit my homework tomorrow._

1. あした しゅくだいを はじめます。
2. あした、 わたしは しゅくだいを 先生に もって いきます。
3. あした しゅくだいを かいます。
4. あした しゅくだいを かえします。

**Answer: 2** - 「(教師に) しゅくだいを 出す」 ≈ 「先生に しゅくだいを もって いく」. Submitting homework to a teacher is paraphrased as physically taking it to them. Strict-N5: replaces the previous keyed verb わたす (vocabulary_n5.md [Ext] borderline N5/N4) with もって いく - both もつ and いく are core N5; わたす no longer appears in the goi corpus. Note: kept in kana since 持 is not in the kanji whitelist.''',

    'Q99': '''### Q99

A: わたしは スペインから きました。

_I came from Spain._

1. わたしは スペインへ いきます。
2. わたしは スペイン人です。
3. わたしは スペインの 人と ともだちです。
4. わたしは スペインごを 話します。

**Answer: 2** - X から きた ≈ X 人. N5 pragmatic substitution: at this level "came from X" is the standard textbook paraphrase of nationality, even though strictly someone could come from X without being X-jin (tourist, long-term resident, expat returning home). Closest among the four offered options.''',
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
        changes.append(f'goi_questions_n5.md {qnum}: replaced block (re-review fix)')
    if text != original_text:
        KB.write_text(text, encoding='utf-8')


def main() -> int:
    update_md_source()
    update_paper_jsons()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
