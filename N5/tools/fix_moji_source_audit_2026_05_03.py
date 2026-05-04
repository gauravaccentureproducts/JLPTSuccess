"""Close all 12 items from feedback/jlpt-n5-moji-and-source-audit-2026-05-03.md.

Pre-state findings (verified before writing this script):
  §2.3 already closed — bunpou source has 0 occurrences of all 9 flagged
       kanji (朝, 思, 京, 阪, 牛, 乳, 公, 園, 楽). Earlier session work
       cleaned them up. Nothing to do.
  §4.2 already closed — goi source has 0 occurrences of 去.

Items requiring fixes:
  §1.1 CRITICAL: re-extract 24 moji-4/5/6/7 empty stems from KB MD
  §2.1 HIGH:    moji source Q35 町→まち, Q95 八百屋→みせ (in MD + JSON)
  §2.2 HIGH:    add 向/央/付 to dokkai_kanji_exception.json + JA-28
  §2.4 HIGH:    drop __lemma__ - prefix on moji-7 Q97-Q99 (source + JSON)
  §3.1 MEDIUM:  correction of record. Revert prior JSON over-strict
                fixes on goi-5.5/6.11/7.10 (distractors are policy-OK
                with non-N5 kanji); update source MD goi Q58 (correct-
                answer position) to match JSON's kana form.
  §4.1 LOW:     replace 熱 with ねつ in bunpou rationale.

Auto-closed:
  §3.2  bunpou-7 ぎんこう  — clarification only; existing fix stands.
  §3.3  Q92 起ちます       — distractor, policy-allowed; no fix.
  §3.4  manifest totals    — positive finding; no fix.
  §3.5  Q62 rationale      — positive finding; no fix.

Idempotent. JA-13 / JA-28 invariants run via check_content_integrity.py
after this script.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / 'KnowledgeBank'
PAPERS = ROOT / 'data' / 'papers'

changes: list[str] = []


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding='utf-8'))


def save_json(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


# =====================================================================
# §1.1 + §2.4: Re-extract 24 moji empty stems from KB markdown
# (§2.4 handled inline by stripping the lemma-prefix on Q97-Q99)
# =====================================================================
# kbSourceId → (stem, rationale_seed)
# Rationales mirror the source's "**Answer: N** - <note>." format,
# stripped of the answer-revealing prefix.
MOJI_STEMS = {
    # moji-4 (Q46-Q60)
    'Q52': ('__せんせい__ に しつもんを しました。',                  '先生 (teacher).'),
    'Q53': ('__がっこう__ で にほんごを べんきょうします。',          '学校 (school).'),
    'Q57': ('__はは__ は 学校の 先生です。',                          '母 (mother).'),
    'Q59': ('__ひと__ が おおぜい います。',                          '人 (person).'),
    'Q60': ('__おとこ__ の こが あそんで います。',                  '男 (man / male).'),
    # moji-5 (Q61-Q75)
    'Q61': ('__おんな__ の 学生が きました。',                        '女 (woman / female).'),
    'Q63': ('__にほん__ に すんで います。',                          '日本 (Japan).'),
    'Q64': ('__にほんご__ で 話します。',                              '日本語 (Japanese language).'),
    'Q65': ('__がいこく__ で しごとを して います。',                '外 + 国.'),
    'Q68': ('__もくようび__ に テストが あります。',                  '木 (Thursday).'),
    'Q69': ('__きょう__ は とても いい てんきです。',                '今日.'),
    'Q70': ('__らいねん__ に だいがくに いきます。',                  '来年.'),
    'Q71': ('__せんしゅう__ えいがを 見ました。',                      '先週.'),
    'Q72': ('__まいにち__ にほんごを 話します。',                      '毎日.'),
    'Q73': ('__ごぜん__ じゅうじに あいましょう。',                    '午前.'),
    'Q74': ('__ごご__ に 友だちが きます。',                            '午後.'),
    'Q75': ('__でんしゃ__ の なかで 本を 読みます。',                  '電車.'),
    # moji-6 (Q76-Q90)
    'Q76': ('__でんわ__ で 友だちと 話します。',                        '電話.'),
    'Q79': ('__えき__ で 友だちと あいました。',                        '駅.'),
    'Q80': ('__みせ__ は えきの まえに あります。',                    '店.'),
    # moji-7 (Q91-Q100). §2.4 lemma-prefix dropped on Q97-Q99.
    'Q97': ('この レストランは __やすい__ です。',                      '安い.'),
    'Q98': ('この かわは とても __ながい__ です。',                    '長い.'),
    'Q99': ('__しろい__ ねこが います。',                                '白い.'),
    'Q100': ('__なまえ__ を ここに かいて ください。',                  '名前.'),
}


def fix_moji_stems() -> None:
    for paper_n in (4, 5, 6, 7):
        p_path = PAPERS / 'moji' / f'paper-{paper_n}.json'
        paper = load_json(p_path)
        modified = False
        for q in paper.get('questions', []):
            kb = q.get('kbSourceId')
            if kb not in MOJI_STEMS:
                continue
            stem, rat = MOJI_STEMS[kb]
            if (q.get('stem_html') or '') != stem:
                q['stem_html'] = stem
                modified = True
                changes.append(f'§1.1 moji-{paper_n}.{kb}: stem populated')
            if not (q.get('rationale') or '').strip():
                q['rationale'] = rat
                modified = True
                changes.append(f'§1.1 moji-{paper_n}.{kb}: rationale set')
        if modified:
            save_json(p_path, paper)


# =====================================================================
# §2.4: drop __lemma__ - prefix on moji source Q97-Q99
# =====================================================================
def fix_moji_source_lemma_prefix() -> None:
    md_path = KB / 'moji_questions_n5.md'
    text = md_path.read_text(encoding='utf-8')
    # Three textual replacements. Each one targets the exact lemma-prefix
    # form documented in the audit; safe substring replace.
    REPLACEMENTS = [
        ('__やすい__ - この レストランは __やすい__ です。',
         'この レストランは __やすい__ です。'),
        ('__ながい__ - この かわは とても __ながい__ です。',
         'この かわは とても __ながい__ です。'),
        ('__しろい__ - __しろい__ ねこが います。',
         '__しろい__ ねこが います。'),
    ]
    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
            changes.append(f'§2.4 moji_questions_n5.md: dropped lemma-prefix → {new[:30]}...')
    md_path.write_text(text, encoding='utf-8')


# =====================================================================
# §2.1: moji source Q35 町→まち, Q95 八百屋→みせ (MD + JSON)
# =====================================================================
def fix_moji_source_2_1() -> None:
    md_path = KB / 'moji_questions_n5.md'
    text = md_path.read_text(encoding='utf-8')
    # Q35: 私の いえは 町の <u>北</u> に あります。
    #   → 私の いえは まちの <u>北</u> に あります。
    old_q35 = '私の いえは 町の <u>北</u> に あります。'
    new_q35 = '私の いえは まちの <u>北</u> に あります。'
    if old_q35 in text:
        text = text.replace(old_q35, new_q35)
        changes.append('§2.1 moji_questions_n5.md Q35: 町→まち')
    # Q95: 八百屋で やさいを __かいます__。
    #   → みせで やさいを __かいます__。
    old_q95 = '八百屋で やさいを __かいます__。'
    new_q95 = 'みせで やさいを __かいます__。'
    if old_q95 in text:
        text = text.replace(old_q95, new_q95)
        changes.append('§2.1 moji_questions_n5.md Q95: 八百屋→みせ')
    md_path.write_text(text, encoding='utf-8')

    # Propagate to JSON: Q35 lives in moji-3 (paper-3.json, Q31-Q45 range)
    # and Q95 lives in moji-7 (paper-7.json, Q91-Q100). Find by kbSourceId.
    for paper_n, kb_q, find, replace in [
        (3, 'Q35', '町の', 'まちの'),
        (7, 'Q95', '八百屋で', 'みせで'),
    ]:
        p_path = PAPERS / 'moji' / f'paper-{paper_n}.json'
        paper = load_json(p_path)
        modified = False
        for q in paper.get('questions', []):
            if q.get('kbSourceId') != kb_q:
                continue
            stem = q.get('stem_html') or ''
            if find in stem:
                q['stem_html'] = stem.replace(find, replace)
                modified = True
                changes.append(f'§2.1 moji-{paper_n}.{kb_q} JSON: {find}→{replace}')
        if modified:
            save_json(p_path, paper)


# =====================================================================
# §2.2: add 向/央/付 to dokkai_kanji_exception.json
# =====================================================================
def fix_dokkai_exception_register() -> None:
    p = ROOT / 'data' / 'dokkai_kanji_exception.json'
    data = load_json(p)
    existing = data.get('exception_kanji', [])
    NEW = [
        ('向', 'needed for 子ども向け / 〜向け (target-audience compound, common in N5 dokkai)'),
        ('央', 'needed for 中央 in proper nouns (中央こうえん, 中央えき)'),
        ('付', 'needed for 〜付き (menu/list "included" convention)'),
    ]
    added: list[str] = []
    for kanji, _why in NEW:
        if kanji not in existing:
            existing.append(kanji)
            added.append(kanji)
            changes.append(f'§2.2 dokkai_kanji_exception.json: + {kanji}')
    if added:
        data['exception_kanji'] = existing
        # Append a justification block to _doc so the WHY is on-record.
        doc = data.get('_doc') or []
        if isinstance(doc, list):
            note = (
                f'2026-05-03 (moji-and-source audit §2.2): added {", ".join(added)} '
                f'with justifications — 向 for 〜向け target-audience compounds, '
                f'央 for 中央 proper nouns (parks/stations), 付 for 〜付き menu '
                f'convention. All three appear in dokkai passage content multiple '
                f'times; kana-substitution would reduce passage authenticity.'
            )
            if not any('moji-and-source audit §2.2' in (line or '') for line in doc):
                doc.append(note)
                data['_doc'] = doc
        save_json(p, data)
    # Also update KnowledgeBank/dokkai_questions_n5.md header per the
    # exception register's own instruction ("update KnowledgeBank/
    # dokkai_questions_n5.md header"). Append to the exception list there.
    md = KB / 'dokkai_questions_n5.md'
    if md.exists() and added:
        text = md.read_text(encoding='utf-8')
        # Look for the exception-list region. Add a marker comment if
        # it doesn't already exist; otherwise leave the file alone (the
        # canonical register lives in the JSON).
        if '2026-05-03 audit §2.2' not in text:
            note = (
                '\n\n<!-- 2026-05-03 audit §2.2: '
                f'dokkai_kanji_exception.json extended with {", ".join(added)} '
                '(see WHY notes in that file). -->\n'
            )
            text = text + note
            md.write_text(text, encoding='utf-8')
            changes.append('§2.2 dokkai_questions_n5.md: header note appended')


# =====================================================================
# §3.1: revert over-strict goi distractor fixes; update goi Q58 source MD
# =====================================================================
GOI_REVERTS = [
    # (paper_n, qid, find, replace_with_kanji_form, choice_pos_for_log)
    (5, 'goi-5.5',  'もう すこし', 'もう少し',   'distractor [0]'),
    (6, 'goi-6.11', 'てがみ',       '手紙',       'distractor [3]'),
    (7, 'goi-7.10', 'うって',       '売って',     'distractor [1]'),
]


def fix_goi_3_1_reverts() -> None:
    for paper_n, qid, find, replace, where in GOI_REVERTS:
        p_path = PAPERS / 'goi' / f'paper-{paper_n}.json'
        paper = load_json(p_path)
        modified = False
        for q in paper.get('questions', []):
            if q.get('id') != qid:
                continue
            new_choices = []
            for ch in q.get('choices', []):
                if isinstance(ch, str) and find in ch and replace not in ch:
                    new_choices.append(ch.replace(find, replace))
                    modified = True
                else:
                    new_choices.append(ch)
            if modified:
                q['choices'] = new_choices
                # Restore rationale references to the kanji form too if needed.
                rat = q.get('rationale') or ''
                if find in rat and replace not in rat:
                    q['rationale'] = rat.replace(find, replace)
                changes.append(f'§3.1 {qid} {where}: {find}→{replace} (revert prior over-strict fix)')
        if modified:
            save_json(p_path, paper)

    # Q58 source MD update: 「きのう 早く ねました。」 → 「きのう はやく ねました。」
    # Real policy violation (correct-answer position with non-N5 kanji 早).
    md_path = KB / 'goi_questions_n5.md'
    text = md_path.read_text(encoding='utf-8')
    old_q58 = 'きのう 早く ねました。'
    new_q58 = 'きのう はやく ねました。'
    if old_q58 in text:
        text = text.replace(old_q58, new_q58)
        md_path.write_text(text, encoding='utf-8')
        changes.append('§3.1 goi_questions_n5.md Q58: 早く→はやく (real correct-answer violation)')


# =====================================================================
# §4.1: replace 熱 with ねつ in bunpou rationale
# =====================================================================
def fix_bunpou_4_1() -> None:
    md_path = KB / 'bunpou_questions_n5.md'
    text = md_path.read_text(encoding='utf-8')
    # The audit cites Q19's rationale: "熱がある (have a fever)."
    if '熱がある' in text:
        text = text.replace('熱がある', 'ねつが ある')
        md_path.write_text(text, encoding='utf-8')
        changes.append('§4.1 bunpou_questions_n5.md: 熱がある→ねつが ある')
    elif '熱' in text:
        # Catch-all: any other 熱 occurrence in rationale-like context
        # is rare; flag for manual review rather than blind-replace.
        changes.append('§4.1 bunpou: 熱 still present (manual review needed)')


def main() -> int:
    fix_moji_stems()
    fix_moji_source_lemma_prefix()
    fix_moji_source_2_1()
    fix_dokkai_exception_register()
    fix_goi_3_1_reverts()
    fix_bunpou_4_1()

    if not changes:
        print('No changes (everything already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
