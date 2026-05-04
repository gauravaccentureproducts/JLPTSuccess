"""Close all 11 items from feedback/jlpt-n5-reference-markdowns-audit-2026-05-04.md.

Items:
  §1.1 HIGH    kanji_n5.md - apply [N4+] flag to ~19 entries with out-of-scope readings
  §1.2 HIGH    kanji_n5.md - reorder 入 kun (い → はい first)
  §1.3 HIGH    vocab POS mistags in §1 (Pronouns) + §12 (Time-Frequency).
               BOTH vocabulary_n5.md AND data/vocab.json need updates so JA-31 stays green.
  §1.4 HIGH    grammar_n5.md - add Verb + ことができる pattern
  §2.1 MED     grammar_n5.md - add から particle option to もらう
  §2.2 MED     grammar_n5.md - replace combined もの+んだ example with cleaner one
  §2.3 MED     grammar_n5.md - drop ごはん from bika-go example list (lexicalized)
  §2.4 MED     grammar_n5.md - Genki citation L8/L10 → L8 / L9
  §2.5 MED     sources.md - add JLPT.jp N5 sample-paper PDFs reference
  §3.1 LOW     sources.md - add NHK NEWS WEB EASY reference
  §3.2 LOW     grammar_n5.md - register caveat on prohibitive な

Idempotent. JA-13 / JA-31 invariants run via check_content_integrity.py
after.
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

changes: list[str] = []


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8')


def write(p: Path, s: str) -> None:
    p.write_text(s, encoding='utf-8')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    """Substring replace; record a change only if the substring was found."""
    if old in text and new not in text:
        text = text.replace(old, new, 1)
        changes.append(label)
    return text


# =====================================================================
# §1.1 + §1.2: kanji_n5.md scope flags + 入 kun reorder
# =====================================================================
def fix_kanji_md() -> None:
    p = KB / 'kanji_n5.md'
    text = read(p)

    # §1.2: 入 kun reorder + add note explaining the stem split.
    text = replace_once(
        text,
        '- **入**\n  - On: ニュウ\n  - Kun: い(る), はい(る), い(れる)\n  - Meaning: enter, put in',
        ('- **入**\n  - On: ニュウ\n  - Kun: はい(る), い(る), い(れる)\n'
         '  - Meaning: enter, put in (Note: はい-stem is the standalone verb '
         '入る = はいる; い-stem appears in 入れる いれる, 入り いり.)'),
        '§1.2 入 kun reorder + stem-split note',
    )

    # §1.1: flag out-of-scope readings on ~19 entries with [N4+ ...] notes.
    # Each substring is unique enough to safely substring-replace once.
    KANJI_FIXES = [
        # 半: なか(ば) is N3+
        ('- **半**\n  - On: ハン\n  - Kun: なか(ば)\n  - Meaning: half',
         '- **半**\n  - On: ハン\n  - Kun: なか(ば) [N3+ noun reading; recognition only]\n  - Meaning: half',
         '§1.1 半: flag なか(ば) [N3+]'),
        # 何: カ on-yomi is N3+
        ('- **何**\n  - On: カ\n  - Kun: なに, なん\n  - Meaning: what',
         '- **何**\n  - On: カ [N3+ on-reading; recognition only]\n  - Kun: なに, なん\n  - Meaning: what',
         '§1.1 何: flag カ [N3+]'),
        # 語: かた(る) is N3
        ('- **語**\n  - On: ゴ\n  - Kun: かた(る)\n  - Meaning: language, word',
         '- **語**\n  - On: ゴ\n  - Kun: かた(る) [N3 verb reading; recognition only]\n  - Meaning: language, word',
         '§1.1 語: flag かた(る) [N3]'),
        # 木: こ- prefix is N4+
        ('- **木**\n  - On: モク, ボク\n  - Kun: き, こ-\n  - Meaning: tree, wood, Thursday',
         '- **木**\n  - On: モク, ボク\n  - Kun: き, こ- [N4+ prefix; recognition only]\n  - Meaning: tree, wood, Thursday',
         '§1.1 木: flag こ- [N4+]'),
        # 金: かな- prefix is N4+
        ('- **金**\n  - On: キン, コン\n  - Kun: かね, かな-\n  - Meaning: gold, money, Friday',
         '- **金**\n  - On: キン, コン\n  - Kun: かね, かな- [N4+ prefix; recognition only]\n  - Meaning: gold, money, Friday',
         '§1.1 金: flag かな- [N4+]'),
        # 生: clarify the misleading "primary N5 use: in compounds" note;
        # both 生きる and 生まれる ARE N5 verbs.
        ('- **生**\n  - On: セイ\n  - Kun: い(きる), う(まれる)\n  - Meaning: life, birth (primary N5 use: in compounds like 学生 / 先生)',
         '- **生**\n  - On: セイ\n  - Kun: い(きる), う(まれる)\n  - Meaning: life, birth (N5 contexts: standalone verbs 生きる いきる, 生まれる うまれる; on-reading セイ in compounds 学生 がくせい, 先生 せんせい.)',
         '§1.1 生: clarify N5-use note'),
        # 小: こ- and お- prefixes are N4+
        ('- **小**\n  - On: ショウ\n  - Kun: ちい(さい), こ-, お-\n  - Meaning: small, little',
         '- **小**\n  - On: ショウ\n  - Kun: ちい(さい), こ- [N4+ prefix], お- [N4+ prefix]\n  - Meaning: small, little',
         '§1.1 小: flag こ- and お- [N4+]'),
        # 後: のち is literary/N4+; reorder common readings first
        ('- **後**\n  - On: ゴ, コウ\n  - Kun: のち, うし(ろ), あと\n  - Meaning: after, behind',
         '- **後**\n  - On: ゴ, コウ\n  - Kun: うし(ろ), あと, のち [N4+ literary reading]\n  - Meaning: after, behind',
         '§1.1 後: reorder + flag のち [N4+]'),
        # 空: あ(く) is N4
        ('- **空**\n  - On: クウ\n  - Kun: そら, あ(く), から\n  - Meaning: sky, empty',
         '- **空**\n  - On: クウ\n  - Kun: そら, あ(く) [N4 verb reading], から\n  - Meaning: sky, empty',
         '§1.1 空: flag あ(く) [N4]'),
        # 見: み(える) and み(せる) are N4 borderline
        ('- **見**\n  - On: ケン\n  - Kun: み(る), み(える), み(せる)\n  - Meaning: see, look',
         '- **見**\n  - On: ケン\n  - Kun: み(る), み(える) [N4 verb reading; recognition only], み(せる) [N4-N5 borderline; 見せる "to show" is borderline N5]\n  - Meaning: see, look',
         '§1.1 見: flag み(える)/み(せる)'),
        # 聞: き(こえる) is N4
        ('- **聞**\n  - On: ブン, モン\n  - Kun: き(く), き(こえる)\n  - Meaning: hear, listen, ask',
         '- **聞**\n  - On: ブン, モン\n  - Kun: き(く), き(こえる) [N4 verb reading; recognition only]\n  - Meaning: hear, listen, ask',
         '§1.1 聞: flag き(こえる) [N4]'),
        # 来: きた(る) is literary/N3+
        ('- **来**\n  - On: ライ\n  - Kun: く(る), きた(る)\n  - Meaning: come',
         '- **来**\n  - On: ライ\n  - Kun: く(る), きた(る) [N3+ literary reading]\n  - Meaning: come',
         '§1.1 来: flag きた(る) [N3+]'),
        # 行: ゆ(く) poetic alt; おこな(う) is N3
        ('- **行**\n  - On: コウ, ギョウ, アン\n  - Kun: い(く), ゆ(く), おこな(う)\n  - Meaning: go, conduct',
         '- **行**\n  - On: コウ, ギョウ, アン\n  - Kun: い(く), ゆ(く) [N4+ poetic alt of い(く)], おこな(う) [N3 verb reading]\n  - Meaning: go, conduct',
         '§1.1 行: flag ゆ(く)/おこな(う)'),
        # 立: た(てる) is N4 transitive
        ('- **立**\n  - On: リツ, リュウ\n  - Kun: た(つ), た(てる)\n  - Meaning: stand',
         '- **立**\n  - On: リツ, リュウ\n  - Kun: た(つ), た(てる) [N4 transitive verb reading]\n  - Meaning: stand',
         '§1.1 立: flag た(てる) [N4]'),
        # 休: やす(まる) is N4 intransitive
        ('- **休**\n  - On: キュウ\n  - Kun: やす(む), やす(まる)\n  - Meaning: rest, holiday',
         '- **休**\n  - On: キュウ\n  - Kun: やす(む), やす(まる) [N4 intransitive verb reading]\n  - Meaning: rest, holiday',
         '§1.1 休: flag やす(まる) [N4]'),
        # 言: こと is jukujikun-only (in 言葉)
        ('- **言**\n  - On: ゲン, ゴン\n  - Kun: い(う), こと\n  - Meaning: say, word',
         '- **言**\n  - On: ゲン, ゴン\n  - Kun: い(う), こと [jukujikun in 言葉 ことば only; not a standalone N5 reading]\n  - Meaning: say, word',
         '§1.1 言: flag こと [jukujikun]'),
        # 新: あら(た) is N3; にい- is N4+
        ('- **新**\n  - On: シン\n  - Kun: あたら(しい), あら(た), にい-\n  - Meaning: new',
         '- **新**\n  - On: シン\n  - Kun: あたら(しい), あら(た) [N3 stem reading], にい- [N4+ prefix; recognition only]\n  - Meaning: new',
         '§1.1 新: flag あら(た)/にい-'),
        # 白: しら- prefix is N3+
        ('- **白**\n  - On: ハク, ビャク\n  - Kun: しろ, しろ(い), しら-\n  - Meaning: white',
         '- **白**\n  - On: ハク, ビャク\n  - Kun: しろ, しろ(い), しら- [N3+ prefix; recognition only]\n  - Meaning: white',
         '§1.1 白: flag しら- [N3+]'),
    ]
    for old, new, label in KANJI_FIXES:
        text = replace_once(text, old, new, label)

    write(p, text)


# =====================================================================
# §1.3: vocab POS mistags — fix BOTH vocab.json AND vocabulary_n5.md
# =====================================================================
def fix_vocab_pos() -> None:
    # Pairs: (vocab.json id-substring filter or form, expected POS in JSON, MD-line-search-needle, MD-tag).
    # JSON updates first; MD updates second.
    JSON_FIXES = [
        # (form, reading, section_substring, new_pos)
        ('人',       'ひと',     '1. People - Pronouns and Self', 'noun'),
        ('かた',     'かた',     '1. People - Pronouns and Self', 'noun'),
        ('だれ',     'だれ',     '1. People - Pronouns and Self', 'question-word'),
        ('どなた',   'どなた',   '1. People - Pronouns and Self', 'question-word'),
        ('みなさん', 'みなさん', '1. People - Pronouns and Self', 'noun'),
        ('もうすぐ', 'もうすぐ', '12. Time - Frequency / Sequence', 'adverb'),
    ]
    vp = ROOT / 'data' / 'vocab.json'
    vocab = json.loads(vp.read_text(encoding='utf-8'))
    entries = vocab['entries']
    for form, reading, sect, new_pos in JSON_FIXES:
        for e in entries:
            if (e.get('form') == form
                    and e.get('reading') == reading
                    and sect in (e.get('section') or '')
                    and e.get('pos') != new_pos):
                e['pos'] = new_pos
                changes.append(f'§1.3 vocab.json {form} ({sect[:18]}...): pos → {new_pos}')
    vp.write_text(json.dumps(vocab, ensure_ascii=False, indent=2), encoding='utf-8')

    # MD: fix the same 6 entries (single-form lines) AND the multi-form
    # みんな / みな entry (kept in MD only).
    md = KB / 'vocabulary_n5.md'
    text = read(md)
    MD_FIXES = [
        ('- 人 (ひと) - [pron.] person',                '- 人 (ひと) - [n.] person'),
        ('- かた - [pron.] person (polite)',              '- かた - [n.] person (polite)'),
        ('- だれ - [pron.] who',                          '- だれ - [Q-word] who'),
        ('- どなた - [pron.] who (polite)',               '- どなた - [Q-word] who (polite)'),
        ('- みなさん - [pron.] everyone (polite)',         '- みなさん - [n.] everyone (polite)'),
        ('- みんな / みな - [pron.] everyone',             '- みんな / みな - [n.] everyone'),
        ('- もうすぐ - [n.] soon, before long',           '- もうすぐ - [adv.] soon, before long'),
    ]
    for old, new in MD_FIXES:
        if old in text:
            text = text.replace(old, new, 1)
            changes.append(f'§1.3 vocabulary_n5.md: {old[:30]}... → {new.split("- ")[2][:30]}...')
    write(md, text)


# =====================================================================
# §1.4: grammar_n5.md - add Verb + ことができる pattern
# =====================================================================
def fix_grammar_kotogadekiru() -> None:
    p = KB / 'grammar_n5.md'
    text = read(p)
    # Insert into Section 17 (Nominalization) since the こと construction
    # nominalizes a verb. Find the section header.
    if 'Verb (plain dictionary) + ことができる' in text:
        return  # Already added.

    # The most natural insertion point: after the "～ができます" entry in
    # Section 10. Find that line.
    needle = '～ができます'
    idx = text.find(needle)
    if idx == -1:
        return
    # Append a new bullet directly after this line. Find end-of-line.
    line_end = text.find('\n', idx)
    if line_end == -1:
        return
    insertion = (
        '\n- Verb (plain dictionary) + ことができる / ことができます '
        '(can do - productive form)\n'
        '  - Example: 日本語を 話す ことが できます。 (I can speak Japanese.)\n'
        '  - Pairs with noun + ができる above; uses the こと nominalizer '
        '(Section 17) to convert any plain-form verb into the "can do" frame.'
    )
    text = text[:line_end] + insertion + text[line_end:]
    changes.append('§1.4: added "Verb + ことができる" pattern to Section 10')
    write(p, text)


# =====================================================================
# §2.1: もらう - add から particle option
# =====================================================================
def fix_morau_kara() -> None:
    p = KB / 'grammar_n5.md'
    text = read(p)
    text = replace_once(
        text,
        '- ～に～をもらいます',
        ('- ～に / から ～をもらいます (either particle is acceptable at N5; '
         '～に is more typical for personal givers, ～から for institutional '
         'sources)'),
        '§2.1: もらう に / から particle option',
    )
    write(p, text)


# =====================================================================
# §2.2: もの example - replace combined もの+んだ example
# =====================================================================
def fix_mono_example() -> None:
    p = KB / 'grammar_n5.md'
    text = read(p)
    text = replace_once(
        text,
        'E.g., だって、いそがしいんだもの。 - "But, you know, I\'m busy."',
        'E.g., 行きたくないもん。 - "I don\'t wanna go." Or: だって、雨だもの。 - "Because, you know, it\'s raining."',
        '§2.2: cleaner もの example (no overlapping んだ pattern)',
    )
    write(p, text)


# =====================================================================
# §2.3: bika-go example - drop ごはん (lexicalized), use cleaner cases
# =====================================================================
def fix_bikago_example() -> None:
    p = KB / 'grammar_n5.md'
    text = read(p)
    text = replace_once(
        text,
        'お～ / ご～ (beautifying prefixes - limited to common cases like お茶, お金, ごはん)',
        ('お～ / ご～ (beautifying prefixes - limited to productive cases like '
         'お茶, お金, おさけ, おみず, おはな. Note: ごはん is a single '
         'lexicalized word now, not a productive ご-prefix; it\'s included '
         'in N5 vocab as one item rather than as an example of generative '
         '美化語.)'),
        '§2.3: bika-go example list - drop ごはん from "productive" set',
    )
    write(p, text)


# =====================================================================
# §2.4: Genki citation - L8 / L10 → L8 / L9 for も compounds
# =====================================================================
def fix_genki_citation() -> None:
    p = KB / 'grammar_n5.md'
    text = read(p)
    text = replace_once(
        text,
        'Question word + か / も compounds (Genki I L8 / L10):',
        'Question word + か / も compounds (Genki I L8 for か-compounds; L9 for も-compounds with negative; いつも at L11):',
        '§2.4: Genki citation L8/L10 → L8 / L9 (も compounds at L9)',
    )
    write(p, text)


# =====================================================================
# §2.5 + §3.1: sources.md additions
# =====================================================================
def fix_sources() -> None:
    p = KB / 'sources.md'
    text = read(p)
    # §2.5: add JLPT.jp N5 sample paper PDFs reference. Append into existing
    # JEES section if possible; otherwise to bottom.
    if 'N5 Sample Questions' not in text and 'サンプル問題' not in text:
        # Find the JLPT.jp / JEES area; insert a sub-bullet there.
        idx = text.find('jlpt.jp')
        if idx == -1:
            idx = text.find('JEES')
        if idx == -1:
            idx = len(text) - 1
        # Find end-of-line then end-of-paragraph.
        line_end = text.find('\n', idx)
        if line_end == -1:
            line_end = len(text)
        insertion = (
            '\n  - **N5 Sample Questions** (free PDFs hosted by JEES) - the '
            'closest authoritative reference for what an actual N5 paper '
            'looks like. Includes sample 文字 (moji), 語彙 (goi), 文法 '
            '(bunpou), 読解 (dokkai), 聴解 (chōkai) sections. Cited as '
            '「JLPT N5 サンプル問題」 in this project for format-fidelity '
            'checks on mock paper authoring.'
        )
        text = text[:line_end] + insertion + text[line_end:]
        changes.append('§2.5: sources.md - added JLPT.jp N5 sample-papers reference')

    # §3.1: add NHK NEWS WEB EASY reference.
    if 'NHK' not in text or ('Easy' not in text and 'easy' not in text and 'やさしい' not in text):
        # Append under "Established Learner References" if present, else
        # bottom.
        anchor = 'Established Learner References'
        idx = text.find(anchor)
        if idx == -1:
            anchor = 'Learner References'
            idx = text.find(anchor)
        # Find the next blank line to anchor near the section's content.
        if idx != -1:
            sect_end = text.find('\n## ', idx + 1)
            if sect_end == -1:
                sect_end = len(text)
        else:
            sect_end = len(text)
        insertion = (
            '\n- **NHK NEWS WEB EASY** - https://www3.nhk.or.jp/news/easy/ '
            '- daily news rewritten for N5/N4 learners (やさしい日本語の'
            'ニュース). Largest open-web source of authentic-feeling N5 '
            'reading material; widely cited in N5 prep guides. Useful as '
            'an extension to the in-corpus reading.json passages.'
        )
        text = text[:sect_end] + insertion + text[sect_end:]
        changes.append('§3.1: sources.md - added NHK NEWS WEB EASY reference')

    write(p, text)


# =====================================================================
# §3.2: prohibitive な register caveat
# =====================================================================
def fix_prohibitive_na() -> None:
    p = KB / 'grammar_n5.md'
    text = read(p)
    needle = '- Verb-plain + な (don\'t do! - strong / casual prohibition)\n  - Example: ここで たばこを すうな! (Don\'t smoke here!)'
    if needle in text and 'rough / commanding' not in text:
        replacement = needle + (
            '\n  - Register: **rough / commanding**. Use only with clear '
            'authority differential (parent → child, sergeant → soldier) '
            'or in writing (signs / labels). For polite prohibition use '
            '～ないでください (Section 7).'
        )
        text = text.replace(needle, replacement, 1)
        changes.append('§3.2: prohibitive な register caveat added')
    write(p, text)


def main() -> int:
    fix_kanji_md()
    fix_vocab_pos()
    fix_grammar_kotogadekiru()
    fix_morau_kara()
    fix_mono_example()
    fix_bikago_example()
    fix_genki_citation()
    fix_sources()
    fix_prohibitive_na()

    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
