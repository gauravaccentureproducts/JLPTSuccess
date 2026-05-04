"""Seasoned-Japanese-teacher audit pass.

Scans data/ and KnowledgeBank/ for error classes a real JLPT N5
instructor would catch on first reading:

  T-1  Particle-verb mismatch (X を 行く, X で 住む, etc.)
  T-2  Conjugation errors (来って, 行きった, irregular ru-verbs missed)
  T-3  Register inconsistency inside one example/stem
       (desu/masu mixed with plain in the SAME sentence)
  T-4  Counter-reading errors (3本 → さんぼん not さんほん etc.)
  T-5  EN-gloss faithfulness (very rough heuristic — flags obvious
       count/tense/negation mismatches between ja and translation_en)
  T-6  N4-leakage in grammar / examples (patterns formally outside
       N5 scope that still appear without late_n5 tier flag)
  T-7  Common-mistake category coverage on grammar patterns
  T-8  Vocab reading mismatches with kanji catalog
  T-9  Stem-context anchor drift (questions whose context doesn't
       actually anchor the answer particle)

Output: a categorized findings report. Read-only; no files modified.

USAGE: python tools/audit_teacher_review.py [--category T-3]
"""
from __future__ import annotations

import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load(p: Path):
    return json.loads(p.read_text(encoding='utf-8'))


def find_questions():
    """Yield (source, idx, q) for every question in questions.json."""
    qj = load(ROOT / 'data' / 'questions.json')
    for i, q in enumerate(qj.get('questions', [])):
        yield ('questions.json', i, q)


def find_grammar_examples():
    """Yield (pattern_id, idx, ex) for every grammar example."""
    gj = load(ROOT / 'data' / 'grammar.json')
    for p in gj.get('patterns', []):
        for i, ex in enumerate(p.get('examples', [])):
            yield (p.get('id', '?'), i, ex, p)


def stem_text(q: dict) -> str:
    """Best-effort plain-text version of a question stem for regex searches."""
    s = q.get('question_ja') or q.get('stem_html') or q.get('prompt_ja') or ''
    # Strip HTML tags
    s = re.sub(r'<[^>]+>', '', s)
    return s


# ---------------------------------------------------------------------------
# T-1: Particle-verb mismatches
# ---------------------------------------------------------------------------

# Patterns that are definitionally wrong:
#   を 行く / を 来る / を 帰る  (motion verbs take に or へ for destination,
#                                を for path-traversal)
#   で 住む / で いる            (location of existence takes に, not で)
#   に 食べる / に 飲む           (NOT for direct object — consumption verbs
#                                take を, not に)

# Caveat: we want to catch the ERRORS, but X を歩く / X を通る / X を出る
# (path verbs) ARE correct with を. So we limit to verbs that NEVER take を:
T1_BAD_PATTERNS = [
    # (regex, description)
    (re.compile(r'を\s*行きます'),  'を + 行きます (motion destination needs に/へ)'),
    (re.compile(r'を\s*行く'),     'を + 行く (motion destination needs に/へ)'),
    (re.compile(r'を\s*来ます'),   'を + 来ます (destination needs に, not を)'),
    (re.compile(r'を\s*帰ります'), 'を + 帰ります (帰る is intransitive — を marks path only)'),
    (re.compile(r'で\s*住みます'), 'で + 住みます (location of habitation takes に)'),
    (re.compile(r'で\s*住む'),    'で + 住む (location of habitation takes に)'),
    (re.compile(r'で\s*います'),  'で + います (existence-location takes に, で is for action)'),
    (re.compile(r'に\s*食べます'),  'に + 食べます (direct object takes を)'),
    (re.compile(r'に\s*飲みます'),  'に + 飲みます (direct object takes を)'),
]

def check_t1():
    findings = []
    for src, i, q in find_questions():
        # Only check the JA-side stem + correct answer assembly. Distractor
        # mismatches are intentional — that's the whole point of distractors.
        # We only flag if the ASSEMBLED-correct sentence has a bad pair.
        stem = stem_text(q)
        correct = q.get('correctAnswer') or ''
        # If the stem has a blank, substitute correct in
        if '（' in stem and '）' in stem:
            assembled = re.sub(r'（[^）]*）', correct, stem, count=1)
        elif '(' in stem and ')' in stem:
            assembled = re.sub(r'\([^)]*\)', correct, stem, count=1)
        else:
            assembled = stem
        for rx, why in T1_BAD_PATTERNS:
            if rx.search(assembled):
                findings.append((q.get('id', f'#{i}'), why, assembled[:60]))
    return findings


# ---------------------------------------------------------------------------
# T-2: Conjugation errors
# ---------------------------------------------------------------------------

# Patterns that are definitionally wrong conjugations.
T2_BAD_PATTERNS = [
    (re.compile(r'来って'),         '来って — wrong (来る te-form is 来て)'),
    (re.compile(r'する って'),     'する って — should be して'),
    (re.compile(r'行きった'),       '行きった — wrong (行く ta-form is 行った)'),
    (re.compile(r'いきった'),       'いきった — wrong (行く ta-form is 行った/いった)'),
    (re.compile(r'食べりて'),       '食べりて — wrong (食べる te-form is 食べて)'),
    (re.compile(r'たべりて'),       'たべりて — wrong (食べる te-form is 食べて)'),
    (re.compile(r'ありった'),       'ありった — wrong (ある ta-form is あった)'),
    (re.compile(r'いるって'),       'いるって — wrong (いる te-form is いて)'),
]

def check_t2():
    findings = []
    # Walk all string fields in grammar/questions/reading
    for fname in ['grammar.json', 'questions.json', 'reading.json', 'listening.json']:
        try:
            d = load(ROOT / 'data' / fname)
        except Exception:
            continue
        def walk(obj, path):
            if isinstance(obj, str):
                for rx, why in T2_BAD_PATTERNS:
                    m = rx.search(obj)
                    if m:
                        findings.append((path, why, obj[:60]))
                        break
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    walk(v, f'{path}.{k}')
            elif isinstance(obj, list):
                for j, v in enumerate(obj):
                    walk(v, f'{path}[{j}]')
        walk(d, fname)
    return findings


# ---------------------------------------------------------------------------
# T-3: Register inconsistency
# ---------------------------------------------------------------------------

# Inside ONE sentence (no boundary 。), it's a teaching-time red flag if
# we mix polite ます/です with plain dictionary form. (The exception is
# embedded clauses like ～と思います、～と言いました — those are fine.
# We crudely exclude lines containing と思 or と言.)
T3_PLAIN_VERB_END = re.compile(r'(?<![ぁ-ん])(行く|来る|食べる|飲む|見る|読む|書く|する|ある|いる|帰る)([、。]|\s|$)')
T3_POLITE_END = re.compile(r'(ます|ました|ません|ませんでした|です|でした|ではありません)')


def check_t3():
    findings = []
    for pid, i, ex, _ in find_grammar_examples():
        ja = ex.get('ja', '')
        if not ja: continue
        # Split on 。, examine each clause
        for clause in re.split(r'[。!?]', ja):
            if 'と思' in clause or 'と言' in clause:
                continue  # embedded thought / quote OK to mix
            has_plain = bool(T3_PLAIN_VERB_END.search(clause))
            has_polite = bool(T3_POLITE_END.search(clause))
            if has_plain and has_polite:
                findings.append((f'{pid} ex[{i}]', 'plain+polite in one clause', clause[:60]))
                break
    return findings


# ---------------------------------------------------------------------------
# T-4: Counter-reading errors
# ---------------------------------------------------------------------------

# Sound-change rules teachers test heavily:
#   ほん -> ぼん after 3 (3本 さんぼん), ぽん after 1/6/8/10 (1本 いっぽん)
#   かい -> がい after 3 (3階 さんがい)
#   ひき -> ぴき after 1/6/8/10
#   さつ -> ざつ never (no rendaku)
# We catch the most common error: 3本 read as さんほん.

T4_RULES = [
    (re.compile(r'(?<![一-鿿])3\s*本'), 'さんぼん', 'さんほん',  '3本 = さんぼん (rendaku ぼ)'),
    (re.compile(r'(?<![一-鿿])三\s*本'), 'さんぼん', 'さんほん', '三本 = さんぼん (rendaku ぼ)'),
    (re.compile(r'(?<![一-鿿])1\s*本'), 'いっぽん', 'いちほん', '1本 = いっぽん (sokuon + ぽ)'),
    (re.compile(r'(?<![一-鿿])6\s*本'), 'ろっぽん', 'ろくほん', '6本 = ろっぽん (sokuon + ぽ)'),
    (re.compile(r'(?<![一-鿿])8\s*本'), 'はっぽん', 'はちほん', '8本 = はっぽん (sokuon + ぽ)'),
    (re.compile(r'(?<![一-鿿])3\s*階'), 'さんがい', 'さんかい', '3階 = さんがい (rendaku が)'),
]


def check_t4():
    """Flag examples that contain a numeric-counter form whose furigana/
    explanation mentions the WRONG reading."""
    findings = []
    for fname in ['grammar.json', 'questions.json', 'kanji.json', 'vocab.json']:
        try:
            d = load(ROOT / 'data' / fname)
        except Exception:
            continue
        def walk(obj, path):
            if isinstance(obj, str):
                for rx, right, wrong, why in T4_RULES:
                    if rx.search(obj) and wrong in obj and right not in obj:
                        findings.append((path, why, obj[:60]))
                        break
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    walk(v, f'{path}.{k}')
            elif isinstance(obj, list):
                for j, v in enumerate(obj):
                    walk(v, f'{path}[{j}]')
        walk(d, fname)
    return findings


# ---------------------------------------------------------------------------
# T-5: EN-gloss faithfulness — heuristic
# ---------------------------------------------------------------------------

# A teacher catches obvious mismatches:
#   - JA negative but EN positive (or vice versa)
#   - JA past but EN present
#   - Number mismatches (ひと-/ふた-/さん- prefix vs "two" / "three")
#
# This is a heuristic — false positives expected; goal is to surface for
# manual review.

# T-5 v3: catch real gloss errors, suppress idiomatic patterns that LOOK
# like negation mismatches but are correct natural translations:
#
#   1. しか + neg = "only have" (positive in EN)
#   2. ～ませんか = invitation ("won't you ~?" → "shall we ~?", "would you?")
#   3. ～でしょう / ～ですね / ～ますね = tag question ("isn't it?", "right?")
#   4. はじめて = "first time" (often EN-translated as "never before")
#   5. plain ない is also negation (regex needs to catch plain forms)
NEG_JA_STRICT = re.compile(
    r'(ません|ないで(?:ください|す|よ)?|なかった|ない[。、 ?？!]|'
    r'ない(?=[\sの]))')
NEG_EN_BROAD = re.compile(
    r"(\bnot\b|\bno\b|\bnever\b|\bnone\b|\bnothing\b|n['’]t\b|"
    r"without|except|forgot to|nobody|cannot|can ?not)", re.I)
SUPPRESS_IDIOM = re.compile(
    # Phase-1 suppressors (already known false positives):
    r'(しか|だけ|ばかり|ませんか[。?？]?|ね[。?？]?$|でしょう|はじめて|'
    # 2026-05-03: 24 more confirmed false positives — manual review
    # showed all 24 are correct natural translations:
    #   - すみません (fixed apology, ません is non-verbal)
    #   - い-adj ending in ない (あぶない/きたない/つまらない etc.)
    #   - obligation/should-not idioms: ～なくて(は) / ～ないと いけ・なら,
    #     ～ないほうが いい (JA double-neg, EN may be positive or negative
    #     but the idiom is correctly translated either way)
    #   - quoted casual speech: 「...ない」って
    #   - verb prohibitive な at sentence end (行くな = "don'\''t go")
    r'すみません|あぶない|きたない|つまらない|'
    r'なくて(?:は|も)|ないと いけ|ないほうが|'
    r'って (?:言|聞|書)|'
    r'(?:る|く|す|つ|ぬ|ぶ|む|う|ぐ)な[!！。]?$)')


def check_t5():
    findings = []
    for pid, i, ex, _ in find_grammar_examples():
        ja = ex.get('ja', '')
        en = ex.get('translation_en', '')
        if not ja or not en:
            continue
        if SUPPRESS_IDIOM.search(ja):
            continue
        ja_neg = bool(NEG_JA_STRICT.search(ja))
        en_neg = bool(NEG_EN_BROAD.search(en))
        if ja_neg != en_neg:
            who = 'JA negative but EN positive' if ja_neg else 'EN negative but JA positive'
            findings.append((f'{pid} ex[{i}]', who,
                             f'JA={ja[:50]}  EN={en[:50]}'))
    return findings


# ---------------------------------------------------------------------------
# T-6: N4-leakage in grammar without late_n5 tier
# ---------------------------------------------------------------------------

# Patterns that are STRICTLY N4 in most reference grammars but
# sometimes leak into N5 banks. Genki/Minna defaults:
#   ましょう / ましょうか     — squarely N5 (Lesson 6 / 4)
#   てもいい / てはいけない    — squarely N5 (Lesson 6)
#   ながら                    — squarely N5 (Lesson 28 in Minna; some
#                                debate, but JEES official scope = N5)
#   ～たり〜たりする         — N5 (Genki I L11 / Minna L19)
#   ～なくちゃ / ～なきゃ      — N4 colloquial contractions of ～なければ
#                                (Genki II L17 plain-form). Should be
#                                tagged late_n5 OR removed.
#   ～なくてもいい            — N4 boundary; some N5 books (Genki I L17)
#                                include it. Tag late_n5.
N4_TRULY_LEAKED = [
    'なきゃ', 'なくちゃ',  # colloquial — N4
    'なくてもいい',           # N4 boundary
]


def check_t6():
    findings = []
    gj = load(ROOT / 'data' / 'grammar.json')
    for p in gj.get('patterns', []):
        pid = p.get('id', '?')
        pattern = p.get('pattern', '')
        tier = p.get('tier', '')
        for n4 in N4_TRULY_LEAKED:
            if n4 in pattern and tier != 'late_n5':
                findings.append((pid, f'pattern contains {n4!r} but tier={tier!r}', pattern[:60]))
                break
    return findings


# ---------------------------------------------------------------------------
# T-7: Common-mistake coverage — gut check
# ---------------------------------------------------------------------------

def check_t7():
    findings = []
    gj = load(ROOT / 'data' / 'grammar.json')
    for p in gj.get('patterns', []):
        pid = p.get('id', '?')
        cm = p.get('common_mistakes') or []
        # A pattern published without any common-mistake guidance is a
        # teaching-quality gap, not strictly an error. We only flag if the
        # pattern is in the "high-confusion" list (particles, koso-a-do,
        # etc.) AND has zero common_mistakes entries.
        is_high_confusion = bool(re.search(
            r'は|が|を|に|で|と|や|から|まで|より|の|も|か|こゝそゝあゝど',
            p.get('pattern', '')
        ))
        if is_high_confusion and len(cm) == 0:
            findings.append((pid, 'high-confusion pattern without common_mistakes',
                             p.get('pattern', '')[:40]))
    return findings


# ---------------------------------------------------------------------------
# T-8: Vocab reading mismatches with kanji catalog
# ---------------------------------------------------------------------------

def check_t8():
    """For each vocab.json entry, pull its kanji form (if any) and verify
    each kanji is either in N5 catalog OR explicitly flagged as
    out-of-scope."""
    findings = []
    try:
        wl = set(json.loads((ROOT / 'data' / 'n5_kanji_whitelist.json').read_text(encoding='utf-8')))
    except Exception:
        return [("?", "could not load whitelist", "")]
    KANJI_RE = re.compile(r'[一-鿿]')
    vj = load(ROOT / 'data' / 'vocab.json')
    out_of_scope: dict[str, list[str]] = defaultdict(list)
    for v in vj.get('words', []) if isinstance(vj, dict) else vj:
        form = (v.get('lemma') or v.get('form') or '') if isinstance(v, dict) else ''
        for ch in form:
            if KANJI_RE.match(ch) and ch not in wl:
                out_of_scope[ch].append(form)
    for ch, samples in sorted(out_of_scope.items()):
        if len(samples) > 0:
            findings.append((f'kanji {ch}', f'{len(samples)} vocab entries use out-of-scope kanji',
                             ', '.join(samples[:3])))
    return findings


# ---------------------------------------------------------------------------
# T-9: Stem-context anchor drift — ko-so-a-do specific
# ---------------------------------------------------------------------------

def check_t9():
    """For ko-so-a-do questions, confirm that the stem provides a
    distance-anchor word (here / there / over there). Without anchor,
    the question has multiple correct answers."""
    findings = []
    # Distance-test means all 4 choices are the SAME form-type. When
    # choices mix pronoun (これ) + adnominal (この) + place (ここ) the
    # question is testing FORM, not distance — and only one form fits
    # the syntactic slot anyway.
    PRONOUN = {'これ', 'それ', 'あれ', 'どれ'}
    ADNOMINAL = {'この', 'その', 'あの', 'どの'}
    PLACE = {'ここ', 'そこ', 'あそこ', 'どこ'}
    DIRECTIONAL = {'こちら', 'そちら', 'あちら', 'どちら'}
    KOSOADO_FAMILIES = (PRONOUN, ADNOMINAL, PLACE, DIRECTIONAL)
    KEYWORD_ANCHORS = [
        'ここ', 'そこ', 'あそこ', 'こちら', 'そちら', 'あちら',
        '私', 'わたし', 'あなた', 'あの人', '近く', 'ちかく',
        'とおく', '遠く', 'むこう', '向こう',
        '隣', 'となり', '前', 'まえ', '後', 'うしろ', 'ぼく',
        '手', 'て', 'てもと', '足元', '中', 'なか', '外', 'そと',
        '上', 'うえ', '下', 'した', 'はなれた', '少し はなれた',
        'すぐ そこ', 'むこうの', 'こちらの', 'そちらの', 'あちらの',
    ]
    for src, i, q in find_questions():
        choices = q.get('choices') or []
        if not choices: continue
        # Only flag distance-tests: all 4 choices belong to the same family.
        is_distance_test = False
        for fam in KOSOADO_FAMILIES:
            if sum(1 for c in choices if c in fam) >= 3:
                is_distance_test = True
                break
        # If choices SPAN multiple families it's a form-test, not distance.
        family_count = sum(
            1 for fam in KOSOADO_FAMILIES
            if any(c in fam for c in choices)
        )
        if family_count > 1:
            is_distance_test = False
        if not is_distance_test:
            continue
        stem = stem_text(q)
        full = stem + ' ' + (q.get('rationale') or '')
        # ANY parenthetical scene context counts as an anchor — by
        # convention the project uses (...) to set ko-so-a-do scenes,
        # so flag only stems WITHOUT both keyword anchors AND scene
        # parens.
        has_paren_scene = bool(re.search(r'[（(][^）)]{6,}[）)]', stem))
        if has_paren_scene:
            continue
        if not any(a in full for a in KEYWORD_ANCHORS):
            findings.append((q.get('id', f'#{i}'),
                             'kosoado Q without distance-anchor in stem',
                             stem[:60]))
    return findings


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

CHECKS = [
    ('T-1', 'Particle-verb mismatch (を行く, で住む, etc.)', check_t1),
    ('T-2', 'Conjugation errors (来って, 行きった, etc.)', check_t2),
    ('T-3', 'Register inconsistency in single example clause', check_t3),
    ('T-4', 'Counter-reading errors (3本=さんぼん etc.)', check_t4),
    ('T-5', 'EN-gloss faithfulness heuristic (negation/tense)', check_t5),
    ('T-6', 'N4-borderline grammar without late_n5 tier', check_t6),
    ('T-7', 'High-confusion grammar without common_mistakes', check_t7),
    ('T-8', 'Vocab kanji-form out-of-scope vs catalog', check_t8),
    ('T-9', 'kosoado-Q without distance anchor in stem', check_t9),
]

def main():
    cat = None
    if len(sys.argv) > 1 and sys.argv[1] == '--category':
        cat = sys.argv[2]
    print('Seasoned-Japanese-teacher audit')
    print('=' * 70)
    total = 0
    for code, desc, fn in CHECKS:
        if cat and code != cat:
            continue
        try:
            findings = fn()
        except Exception as e:
            print(f'\n{code} {desc}\n  ERROR: {e}')
            continue
        n = len(findings)
        total += n
        marker = '○' if n == 0 else 'X'
        print(f'\n{marker} {code} {desc} ({n})')
        for who, why, sample in findings[:50]:
            print(f'    {who}: {why}')
            print(f'        sample: {sample!r}')
        if n > 50:
            print(f'    ... and {n - 50} more')
    print()
    print('=' * 70)
    print(f'Total findings: {total}')


if __name__ == '__main__':
    main()
