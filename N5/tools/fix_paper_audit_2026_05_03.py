"""Fix all 7 outstanding items from feedback/new/jlpt-n5-paper-files-audit-2026-05-03.md.

Items already passing on baseline verifier (don't re-fix):
  §2.3 dokkai-4 Q58 prompt    — already cleaned
  §3.3 goi-6 Q87 二十さい      — already cleaned
  §3.4 dokkai-4 Q60 後の 日    — already cleaned
  §4.1 goi-1 Q11 distractors  — re-tightened by this script anyway

Items addressed here:
  §1.1 + §3.1  bunpou-5/6 — re-extract 19 missing stems + write rationales
                            (covers §3.1 since we author rationales as we go)
  §2.1         goi-4/5/6/7 — replace 4 non-N5 kanji (早/少/紙/売) with kana
  §2.2         bunpou-7 + KB markdown — ぎんこうから かえって → 学校から かえって
  §2.4         strip trailing '---' residue from 5 rationales
  §3.2         merge explanation_en into rationale (bunpou-4.11, goi-2.6)
  §3.5         strip leading '> ' markdown blockquote from dokkai-4 passages
  §4.1         anchor goi-1 Q11 stem to disambiguate おいしい from たかい

Idempotent. JA-13 N5-kanji-scope guard runs at end (via
check_content_integrity.py — caller's responsibility).
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / 'data' / 'papers'

changes: list[str] = []


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding='utf-8'))


def save(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def all_questions(paper: dict) -> list[dict]:
    if 'questions' in paper:
        return paper['questions']
    out: list[dict] = []
    for sec in paper.get('sections', []) or []:
        if 'questions' in sec:
            out.extend(sec['questions'])
    return out


# =====================================================================
# §1.1 + §3.1: bunpou-5/6 — re-extract stems + rationales from KB markdown
# =====================================================================
# Hand-curated mapping. The KB markdown stems use the
#   "leading-text ___ ___ ★ ___ trailing-text" pattern. Where the
# JSON had an empty stem_html, the leading-text was missing in the
# extractor's pattern. The full stem from KB is reproduced verbatim.
#
# Rationales include the reconstructed sentence + which numbered tile
# lands on the ★ position, mirroring the pattern from KB's
# "**Answer: N** (TILE goes in ★). Order: ..." comment.
BUNPOU_STEMS_AND_RATIONALES = {
    # bunpou-5 (Q61-Q75)
    'bunpou-5.1':  ('きのう ___ ___ ★ ___ 見ました。',
                    'Order: きのう ともだちと(2) いっしょに(4) えいが(3=★) を(1) 見ました = '
                    '"Yesterday I watched a movie together with my friend." えいが(3) goes on the ★.'),
    'bunpou-5.2':  ('わたしは ___ ___ ★ ___ あります。',
                    'Order: わたしは 中国(4) に(3) 行った(2=★) ことが(1) あります = '
                    '"I have been to China." 行った(2) goes on the ★.'),
    'bunpou-5.3':  ('あした ___ ___ ★ ___ 行きます。',
                    'Order: あした ともだち(3) の(2) うち(4=★) に(1) 行きます = '
                    '"Tomorrow I will go to my friend\'s house." うち(4) goes on the ★.'),
    'bunpou-5.4':  ('___ ___ ★ ___ ですか。',
                    'Order: あの 店(2) の(3) 名前は(4=★) 何(1) ですか = '
                    '"What is the name of that shop?" 名前は(4) goes on the ★.'),
    'bunpou-5.5':  ('わたしの ___ ___ ★ ___ あります。',
                    'Order: わたしの つくえの(4) うえ(2) に(1=★) 本が(3) あります = '
                    '"There is a book on top of my desk." に(1) goes on the ★.'),
    'bunpou-5.6':  ('きょうは ___ ___ ★ ___ 食べました。',
                    'Order: きょうは ホテルで(3) あさごはんに(4) パン(2=★) を(1) 食べました = '
                    '"Today I had bread for breakfast at the hotel." パン(2) goes on the ★.'),
    'bunpou-5.7':  ('___ ___ ★ ___ ありませんか。',
                    'Order: しゅくだいは(2) あした(3) まで(4=★) に(1) ありませんか = '
                    '"Isn\'t the homework due by tomorrow?" まで(4) goes on the ★.'),
    'bunpou-5.8':  ('___ ___ ★ ___ かりました。',
                    'Order: 友だちに(2) 本(4) 三さつ(3) を(1=★) かりました = '
                    '"I borrowed three books from my friend." を(1) goes on the ★.'),
    'bunpou-5.9':  ('___ ___ ★ ___ あいました。',
                    'Order: 学校(2) の(1) 友だちに(3) まえで(4=★) あいました = '
                    '"I met a school friend in front (of the school)." まえで(4) goes on the ★.'),
    'bunpou-5.10': ('___ ___ ★ ___ よみたいです。',
                    'Order: としょかんに(3) ある(1) 本を(2=★) 三さつ(4) よみたいです = '
                    '"I want to read three books that are in the library." 本を(2) goes on the ★.'),
    'bunpou-5.11': ('___ ___ ★ ___ きました。',
                    'Order: 雨(3) が(2) たくさん(4=★) ふって(1) きました = '
                    '"It started to rain heavily." たくさん(4) goes on the ★.'),
    'bunpou-5.12': ('れいぞうこの ___ ___ ★ ___ ありますか。',
                    'Order: れいぞうこの 中(3) に(1) のみもの(2=★) が(4) ありますか = '
                    '"Are there drinks in the refrigerator?" のみもの(2) goes on the ★.'),
    'bunpou-5.13': ('わたしは ___ ___ ★ ___ ません。',
                    'Order: わたしは あまり(2) ぎんこう(3) に(1=★) 行き(4) ません = '
                    '"I don\'t go to the bank often." に(1) goes on the ★.'),
    'bunpou-5.14': ('___ ___ ★ ___ ですか。',
                    'Order: これは(4) だれ(3) の(1=★) かばん(2) ですか = '
                    '"Whose bag is this?" の(1) goes on the ★.'),
    'bunpou-5.15': ('あした ___ ___ ★ ___ 来ません。',
                    'Order: あした しごとが あります(4) ので(3) パーティーに(2=★) は(1) 来ません = '
                    '"Tomorrow I have work, so I\'m not coming to the party." パーティーに(2) goes on the ★.'),
    # bunpou-6 (Q76-Q90)
    'bunpou-6.1':  ('___ ___ ★ ___ じょうずです。',
                    'Order: たなかさんは(3) 日本語(2) が(1=★) とても(4) じょうずです = '
                    '"Mr. Tanaka is very good at Japanese." が(1) goes on the ★.'),
    'bunpou-6.2':  ('___ ___ ★ ___ ましょう。',
                    'Order: いっしょに(2) こうえん(4) へ(1=★) 行き(3) ましょう = '
                    '"Let\'s go to the park together." へ(1) goes on the ★.'),
    'bunpou-6.3':  ('___ ___ ★ ___ きてください。',
                    'Order: その本(3) を(2) ここに(4) もって(1=★) きてください = '
                    '"Please bring that book here." もって(1) goes on the ★.'),
    'bunpou-6.4':  ('___ ___ ★ ___ 食べました。',
                    'Order: その(4) ケーキ(2) を(3=★) ぜんぶ(1) 食べました = '
                    '"I ate all of that cake." を(3) goes on the ★.'),
    'bunpou-6.5':  ('___ ___ ★ ___ ありますか。',
                    'Order: あした(3) しゅくだい(2=★) は(4) が(1) ありますか = '
                    '"Is there homework for tomorrow?" しゅくだい(2) goes on the ★.'),
    'bunpou-6.6':  ('___ ___ ★ ___ 行きました。',
                    'Order: 友だち(4) と(1) えいがかん(3=★) に(2) 行きました = '
                    '"I went to the cinema with my friend." えいがかん(3) goes on the ★.'),
    'bunpou-6.7':  ('___ ___ ★ ___ ですか。',
                    'Order: これ(2) は だれ(4) の(1=★) 本(3) ですか = '
                    '"Whose book is this?" の(1) goes on the ★.'),
    'bunpou-6.8':  ('しゅくだいを ___ ___ ★ ___ 食べました。',
                    'Order: しゅくだいを してから(1) いえで(3) みんなで(4=★) ばんごはんを(2) 食べました = '
                    '"After homework, everyone ate dinner together at home." みんなで(4) goes on the ★.'),
    'bunpou-6.9':  ('___ ___ ★ ___ あります。',
                    'Order: やま(2) の うえに(1) ゆきが(3) たくさん(4=★) あります = '
                    '"There is a lot of snow on top of the mountain." たくさん(4) goes on the ★.'),
    'bunpou-6.10': ('私は ___ ___ ★ ___ おもいます。',
                    'Order: 私は 新しい(2) かばん(4) が(1=★) ほしいと(3) おもいます = '
                    '"I think I want a new bag." が(1) goes on the ★.'),
    'bunpou-6.11': ('___ ___ ★ ___ できます。',
                    'Order: たなかさんは(4) ピアノを(2) すこし(1=★) ひくことが(3) できます = '
                    '"Mr. Tanaka can play the piano a little." すこし(1) goes on the ★.'),
    'bunpou-6.12': ('___ ___ ★ ___ おきます。',
                    'Order: まいにち(4) あさ(2) 七時(3=★) に(1) おきます = '
                    '"Every day I get up at seven o\'clock in the morning." 七時(3) goes on the ★.'),
    'bunpou-6.13': ('___ ___ ★ ___ いませんから、たべません。',
                    'Order: おなか(2) が(1) すいて(3) まだ(4=★) いませんから、たべません = '
                    '"I\'m not hungry yet, so I won\'t eat." まだ(4) goes on the ★.'),
    'bunpou-6.14': ('___ ___ ★ ___ いません。',
                    'Order: しゅくだい(1) が(2) まだ(3=★) おわって(4) いません = '
                    '"The homework isn\'t finished yet." まだ(3) goes on the ★.'),
    'bunpou-6.15': ('わたしは ___ ___ ★ ___ つもりです。',
                    'Order: わたしは らいねん(2) 大学(3) に(1=★) 行く(4) つもりです = '
                    '"Next year I plan to go to college." に(1) goes on the ★.'),
}


def fix_bunpou_5_6() -> None:
    for n in (5, 6):
        path = PAPERS / 'bunpou' / f'paper-{n}.json'
        paper = load(path)
        modified = False
        for q in all_questions(paper):
            qid = q.get('id')
            if qid not in BUNPOU_STEMS_AND_RATIONALES:
                continue
            stem, rationale = BUNPOU_STEMS_AND_RATIONALES[qid]
            if not (q.get('stem_html') or '').strip() or q.get('stem_html') != stem:
                if q.get('stem_html') != stem:
                    q['stem_html'] = stem
                    modified = True
                    changes.append(f'§1.1: set stem_html on {qid}')
            if not (q.get('rationale') or '').strip():
                q['rationale'] = rationale
                modified = True
                changes.append(f'§3.1: set rationale on {qid}')
        if modified:
            save(path, paper)


# =====================================================================
# §2.1: goi non-N5 kanji in choices — replace with kana
# =====================================================================
GOI_KANJI_REPLACEMENTS = [
    # (paper_n, qid, find, replace, note)
    (4, 'goi-4.13', '早く', 'はやく', '早 not in N5 whitelist'),
    (5, 'goi-5.5',  'もう少し', 'もう すこし', '少 not in N5 whitelist'),
    (6, 'goi-6.11', '手紙', 'てがみ', '紙 not in N5 whitelist (手 IS, but compound 手紙 is broken)'),
    (7, 'goi-7.10', '売って', 'うって', '売 not in N5 whitelist'),
]


def fix_goi_kanji() -> None:
    for n, qid, find, replace, note in GOI_KANJI_REPLACEMENTS:
        path = PAPERS / 'goi' / f'paper-{n}.json'
        paper = load(path)
        modified = False
        for q in all_questions(paper):
            if q.get('id') != qid:
                continue
            new_choices = []
            for ch in (q.get('choices') or []):
                if isinstance(ch, str):
                    if find in ch:
                        new = ch.replace(find, replace)
                        new_choices.append(new)
                        if new != ch:
                            modified = True
                    else:
                        new_choices.append(ch)
                else:
                    # dict-shaped choice
                    txt = ch.get('text') or ch.get('html') or ''
                    if find in txt:
                        ch = dict(ch)
                        for k in ('text', 'html'):
                            if k in ch:
                                ch[k] = ch[k].replace(find, replace)
                        modified = True
                    new_choices.append(ch)
            if modified:
                q['choices'] = new_choices
                # Also patch the rationale if it cites the kanji form.
                rat = q.get('rationale') or ''
                if find in rat:
                    q['rationale'] = rat.replace(find, replace)
                changes.append(f'§2.1: {qid} {find} → {replace} ({note})')
        if modified:
            save(path, paper)


# =====================================================================
# §2.2: bunpou-7 ぎんこう → 学校 in Passage B (KB markdown + paper JSON)
# =====================================================================
def fix_bunpou_7_school() -> None:
    # 1. Patch KnowledgeBank markdown source.
    kb = ROOT / 'KnowledgeBank' / 'bunpou_questions_n5.md'
    text = kb.read_text(encoding='utf-8')
    # Only the Passage B sentence is wrong; Q6 ("ぎんこうは 駅(...)まえに あります")
    # and Q73 (ぎんこう as a tile choice) stay because there ぎんこう
    # is the meant referent. Limit the substitution to the exact
    # passage-B phrase to avoid collateral damage.
    needle = 'まいにち、 ぎんこうから かえってから'
    replacement = 'まいにち、 学校から かえってから'
    if needle in text:
        text = text.replace(needle, replacement)
        kb.write_text(text, encoding='utf-8')
        changes.append('§2.2: KB bunpou_questions_n5.md ぎんこうから → 学校から (Passage B only)')

    # 2. Patch the bunpou-7 paper JSON. The string lives in passage text;
    # find it and replace.
    path = PAPERS / 'bunpou' / 'paper-7.json'
    paper = load(path)
    js_text = json.dumps(paper, ensure_ascii=False)
    if 'ぎんこうから かえって' in js_text:
        new_js = js_text.replace('ぎんこうから かえって', '学校から かえって')
        save(path, json.loads(new_js))
        changes.append('§2.2: bunpou-7 paper.json ぎんこうから → 学校から')


# =====================================================================
# §2.4: strip trailing '---' residue from rationales (any paper)
# =====================================================================
def fix_trailing_dashes() -> None:
    for category in ('bunpou', 'goi', 'dokkai', 'moji'):
        cdir = PAPERS / category
        if not cdir.exists():
            continue
        for f in sorted(cdir.glob('paper-*.json')):
            paper = load(f)
            modified = False
            for q in all_questions(paper):
                rat = q.get('rationale')
                if not isinstance(rat, str):
                    continue
                # Remove trailing pattern: optional space + 1+ dashes + optional whitespace
                cleaned = re.sub(r'\s*-{2,}\s*$', '', rat).rstrip()
                if cleaned != rat:
                    q['rationale'] = cleaned
                    modified = True
                    changes.append(f"§2.4: stripped trailing --- from {q.get('id', '?')}")
            if modified:
                save(f, paper)


# =====================================================================
# §3.2: merge explanation_en → rationale on bunpou-4.11 and goi-2.6
# =====================================================================
def fix_explanation_merge() -> None:
    targets = [
        (PAPERS / 'bunpou' / 'paper-4.json', 'bunpou-4.11'),
        (PAPERS / 'goi' / 'paper-2.json', 'goi-2.6'),
    ]
    for path, qid in targets:
        paper = load(path)
        modified = False
        for q in all_questions(paper):
            if q.get('id') != qid:
                continue
            ex = q.get('explanation_en')
            if not ex:
                # Already merged; nothing to do.
                continue
            existing_rat = (q.get('rationale') or '').rstrip('.')
            sep = '. ' if existing_rat else ''
            q['rationale'] = f"{existing_rat}{sep}{ex}".strip()
            del q['explanation_en']
            modified = True
            changes.append(f'§3.2: merged explanation_en into rationale on {qid}')
        if modified:
            save(path, paper)


# =====================================================================
# §3.5: strip leading '> ' from dokkai-4 passage texts
# =====================================================================
def fix_dokkai_4_blockquote() -> None:
    path = PAPERS / 'dokkai' / 'paper-4.json'
    paper = load(path)
    modified = False

    def strip_leading_quote(s: str) -> str:
        # Remove a single leading '> ' (markdown blockquote) and any
        # immediate whitespace; preserve all other content verbatim.
        return re.sub(r'^>\s+', '', s)

    for psg in paper.get('passages', []) or []:
        txt = psg.get('text') or ''
        new = strip_leading_quote(txt)
        if new != txt:
            psg['text'] = new
            modified = True
            changes.append(f"§3.5: stripped leading > from passage {psg.get('label', '?')}")
    for sec in paper.get('sections', []) or []:
        for psg in sec.get('passages', []) or []:
            txt = psg.get('text') or ''
            new = strip_leading_quote(txt)
            if new != txt:
                psg['text'] = new
                modified = True
                changes.append(f"§3.5: stripped leading > from section passage")
    if modified:
        save(path, paper)


# =====================================================================
# §4.1: anchor goi-1 Q11 stem to disambiguate おいしい from たかい
# =====================================================================
def fix_goi_1_q11_anchor() -> None:
    path = PAPERS / 'goi' / 'paper-1.json'
    paper = load(path)
    modified = False
    for q in all_questions(paper):
        if q.get('id') != 'goi-1.11':
            continue
        stem = q.get('stem_html') or ''
        if 'あまい' in stem:
            # Already anchored — nothing to do.
            return
        # Anchor stem with sweetness so おいしい is the unique natural
        # completion. Choices stay as ?+です strings.
        new_stem = 'この りんごは あまいですから、（　　）。'
        new_rat = (
            'Sweet apples → delicious. The "あまいですから" anchor forces '
            'おいしい as the only natural completion: たかい (expensive) and '
            'あおい (green/unripe) don\'t follow from sweetness, and '
            'おもしろい (interesting) is unidiomatic for food.'
        )
        if stem != new_stem:
            q['stem_html'] = new_stem
            q['rationale'] = new_rat
            modified = True
            changes.append('§4.1: anchored goi-1 Q11 stem with あまいですから')
    if modified:
        save(path, paper)


# =====================================================================
# main
# =====================================================================
def main() -> int:
    fix_bunpou_5_6()
    fix_goi_kanji()
    fix_bunpou_7_school()
    fix_trailing_dashes()
    fix_explanation_merge()
    fix_dokkai_4_blockquote()
    fix_goi_1_q11_anchor()

    if not changes:
        print('No changes. (All items already in fixed state.)')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
