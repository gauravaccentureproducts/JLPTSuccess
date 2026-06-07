#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a Word (.docx) of N5 grammar pattern pages for native-speaker review.

Mirrors what the SPA pattern page (renderGrammarPatternDetail in
js/learn-grammar.js) shows in the DEFAULT (English) locale, one pattern per
page, EXCEPT:
  - audio players / controls are dropped (sentence text is kept)
  - furigana ruby is rendered as plain Japanese text
  - chrome (nav, back-link, mark-known toggle, print button) is dropped
  - the L1-note section is omitted (it only renders in non-English locales)

Incorrect forms (common_mistakes.wrong, wrong_corrected_pair.wrong) are shown
struck through, exactly as the website renders them. A blank "Reviewer notes"
box is appended after each pattern.

Usage:
  python tools/build_grammar_review_docx.py n5-121      # one pattern (sample)
  python tools/build_grammar_review_docx.py all         # all patterns
Output: docs/grammar-review/<name>.docx
"""
import json
import sys
import os

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAMMAR = os.path.join(ROOT, "data", "grammar.json")
EN_LOCALE = os.path.join(ROOT, "locales", "en.json")
OUT_DIR = os.path.join(ROOT, "docs", "grammar-review")

CJK = "Yu Gothic"
LATIN = "Calibri"
WRONG_RED = RGBColor(0xB3, 0x1B, 0x1B)
RIGHT_GREEN = RGBColor(0x1A, 0x5C, 0x38)
MUTED = RGBColor(0x66, 0x66, 0x66)
HEAD_DARK = RGBColor(0x14, 0x45, 0x2A)

# --- render-contract constants mirrored from js/learn-grammar.js ---
ATTACHES_TO_LABEL = {
    'noun': 'Noun', 'noun_subject': 'Noun (subject)', 'noun_location': 'Noun (location)',
    'noun_time': 'Noun (time)', 'noun_quantity': 'Noun (quantity)', 'noun_or_adj': 'Noun or adjective',
    'na_adjective': 'な-adjective', 'i_adjective': 'い-adjective', 'verb': 'Verb',
    'verb_stem': 'Verb stem (ます-base)', 'verb_stem_i': 'Verb i-stem', 'verb_root': 'Verb root',
    'verb_dictionary': 'Verb (dictionary form)', 'verb_plain': 'Verb (plain form)',
    'verb_te': 'Verb (て-form)', 'verb_ta': 'Verb (た-form)', 'verb_nai': 'Verb (ない-form)',
    'verb_mashita': 'Verb (ました form)', 'verb_te_imasu_neg': 'Verb (て-いません)',
    'verb_or_adj_stem': 'Verb or adjective stem', 'pronoun': 'Pronoun', 'question_word': 'Question word',
    'before_noun': 'Before a noun', 'adverbial': 'Adverbial position', 'sentence_end': 'Sentence end',
    'sentence_pattern': 'Full sentence', 'clause': 'Clause', 'clause_start': 'Clause-initial',
    'clause_end': 'Clause-final', 'plain_clause': 'Plain-form clause',
    'plain_or_polite_clause': 'Plain or polite clause', 'quoted_clause': 'Quoted clause',
    'quantity': 'Quantity expression', 'number': 'Number', 'set_phrase': 'Set phrase',
    'standalone': 'Standalone', 'dialogue': 'Dialogue line', 'after_name': 'After a name',
}
GRAMMAR_SUPERCATS = [
    ('Sentence Basics', ['Copula and Basic Sentence Structure', 'Particles', 'Demonstratives', 'Question Words']),
    ('Verbs', ['Verbs - Tense and Politeness (ます-form)', 'Verbs - Plain (Dictionary) Form and Negation',
        'Te-form and Related Patterns', 'Existence and Possession', 'Desiderative and Volitional',
        'Giving and Receiving (basic)', 'Additional Upper N5 / Borderline Patterns - Permission and Obligation',
        'Additional Upper N5 / Borderline Patterns - Experience and Advice',
        'Additional Upper N5 / Borderline Patterns - Compound and Listed Actions',
        'Additional Upper N5 / Borderline Patterns - Excess', 'Additional Upper N5 / Borderline Patterns - Intention',
        'Additional Upper N5 / Borderline Patterns - Way of Doing',
        'Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)']),
    ('Adjectives and Comparison', ['Adjectives', 'Comparison and Preference']),
    ('Time, Counters, Connectives', ['Counters and Quantity', 'Time Expressions',
        'Conjunctions and Connectives', 'Asking and Stating with から / ので (basic causation)',
        'Existence-of-Plans and Frequency']),
    ('Set Phrases and Discourse', ['Nominalization and Modification', 'Common Set Patterns',
        'Functional Expressions (Non-Grammar, Common Usage)', 'Other Core Patterns',
        'Honorific / Polite Vocabulary at N5 (functional)',
        'Additional Upper N5 / Borderline Patterns - Explanation and Emphasis',
        'Additional Upper N5 / Borderline Patterns - Quotation (Casual)',
        'Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation']),
]
PATTERN_SUPERCAT_OVERRIDES = {
    'n5-135': 'Verbs', 'n5-144': 'Verbs', 'n5-153': 'Verbs',
    'n5-154': 'Verbs', 'n5-162': 'Verbs', 'n5-163': 'Verbs',
}


def attaches_label(key):
    return ATTACHES_TO_LABEL.get(key) or str(key).replace('_', ' ').capitalize()


def supercat_for(p):
    if p.get('id') in PATTERN_SUPERCAT_OVERRIDES:
        return PATTERN_SUPERCAT_OVERRIDES[p['id']]
    cat = p.get('category', '')
    for sc, members in GRAMMAR_SUPERCATS:
        if cat in members:
            return sc
    return 'Set Phrases and Discourse'


def ordered_patterns(allp):
    buckets = {sc: [] for sc, _ in GRAMMAR_SUPERCATS}
    for p in allp:
        buckets[supercat_for(p)].append(p)
    out = []
    for sc, _ in GRAMMAR_SUPERCATS:
        out.extend(sorted(buckets[sc], key=lambda x: (x.get('patternOrder', 0), x.get('id', ''))))
    return out


# --- docx helpers ---
def _set_fonts(run, cjk=CJK, latin=LATIN):
    run.font.name = latin
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set(qn('w:ascii'), latin)
    rfonts.set(qn('w:hAnsi'), latin)
    rfonts.set(qn('w:eastAsia'), cjk)


def run(par, text, *, bold=False, italic=False, strike=False, color=None, size=None):
    r = par.add_run(text if text is not None else '')
    r.bold = bold
    r.italic = italic
    if strike:
        r.font.strike = True
    if color is not None:
        r.font.color.rgb = color
    if size is not None:
        r.font.size = Pt(size)
    _set_fonts(r)
    return r


def para(doc, *, space_before=2, space_after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def title(doc, text):
    p = para(doc, space_before=0, space_after=2)
    run(p, text, bold=True, size=22, color=HEAD_DARK)
    return p


def subtitle(doc, text):
    p = para(doc, space_after=8)
    run(p, text, italic=True, size=12, color=MUTED)


def section_header(doc, en_label, ja_chip):
    p = para(doc, space_before=10, space_after=3)
    run(p, en_label, bold=True, size=13, color=HEAD_DARK)
    if ja_chip:
        run(p, "  " + ja_chip, bold=False, size=10, color=MUTED)
    # bottom rule
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1'); bottom.set(qn('w:color'), 'CCCCCC')
    pbdr.append(bottom); pPr.append(pbdr)


def labeled(doc, label, text):
    if not text:
        return
    p = para(doc)
    run(p, label + ": ", bold=True)
    run(p, text)


def reviewer_box(doc):
    """Reviewer notes table - pre-populated with a visible '未確認 / not yet
    reviewed' placeholder so unreviewed patterns flag themselves rather than
    being silently empty. The native reviewer DELETES the placeholder when
    writing 「問題なし。」 or 「要修正: ...」 so the unreviewed queue stays visually
    obvious. (Same convention as the vocab/kanji review packets.)"""
    p = para(doc, space_before=10, space_after=2)
    run(p, "Reviewer notes", bold=True, size=11, color=MUTED)
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)
    cp1 = cell.paragraphs[0]
    cp1.paragraph_format.space_after = Pt(2)
    run(cp1, "☐ 未確認 / not yet reviewed", italic=True, color=WRONG_RED, size=10)
    cp2 = cell.add_paragraph()
    cp2.paragraph_format.space_after = Pt(6)
    run(cp2,
        "[Native reviewer: delete the line above and write 「問題なし。」 if the "
        "pattern is correct, OR 「要修正: <issue>」 with a specific issue. Empty "
        "boxes are treated as 'not yet reviewed'.]",
        italic=True, color=MUTED, size=9)
    for _ in range(2):
        cp = cell.add_paragraph()
        cp.paragraph_format.space_after = Pt(6)


# --- clickable Table of Contents: bookmarks + internal hyperlinks ---
_BM_ID = [1000]

def _bookmark(paragraph, name):
    """Wrap a paragraph in a Word bookmark so TOC links can jump to it."""
    bid = str(_BM_ID[0]); _BM_ID[0] += 1
    start = OxmlElement('w:bookmarkStart'); start.set(qn('w:id'), bid); start.set(qn('w:name'), name)
    end = OxmlElement('w:bookmarkEnd'); end.set(qn('w:id'), bid)
    pPr = paragraph._p.find(qn('w:pPr'))
    if pPr is not None:
        pPr.addnext(start)
    else:
        paragraph._p.insert(0, start)
    paragraph._p.append(end)


def _toc_link(paragraph, anchor, text):
    """Append a clickable internal hyperlink that jumps to bookmark `anchor`."""
    h = OxmlElement('w:hyperlink'); h.set(qn('w:anchor'), anchor)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), LATIN); rf.set(qn('w:hAnsi'), LATIN); rf.set(qn('w:eastAsia'), CJK)
    rPr.append(rf)
    col = OxmlElement('w:color'); col.set(qn('w:val'), '0563C1'); rPr.append(col)
    u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rPr.append(u)
    r.append(rPr)
    t = OxmlElement('w:t'); t.set(qn('xml:space'), 'preserve'); t.text = text
    r.append(t); h.append(r)
    paragraph._p.append(h)


def build_toc(doc, pats, L):
    """Front Contents page: a clickable link to every pattern, grouped by category."""
    h = para(doc, space_before=0, space_after=4)
    run(h, "Contents", bold=True, size=20, color=HEAD_DARK)
    intro = para(doc, space_after=10)
    run(intro, "%d N5 grammar patterns - click any entry to jump to that pattern." % len(pats),
        italic=True, size=10, color=MUTED)
    buckets = {sc: [] for sc, _ in GRAMMAR_SUPERCATS}
    for p in pats:
        buckets[supercat_for(p)].append(p)
    n = 0
    for sc, _ in GRAMMAR_SUPERCATS:
        group = buckets.get(sc) or []
        if not group:
            continue
        ch = para(doc, space_before=8, space_after=2)
        run(ch, sc, bold=True, size=12, color=HEAD_DARK)
        for p in group:
            n += 1
            line = para(doc, space_before=0, space_after=1)
            _toc_link(line, 'pat_' + p.get('id', '').replace('-', '_'),
                      "%d.  %s" % (n, p.get('pattern', '')))
            if p.get('meaning_en'):
                run(line, "  -  " + p['meaning_en'], size=9, color=MUTED)
    doc.add_page_break()


# --- per-pattern render (mirror of renderGrammarPatternDetail, EN locale) ---
def render_pattern(doc, p, L, first):
    if not first:
        doc.add_page_break()

    tp = title(doc, p.get('pattern', ''))
    _bookmark(tp, 'pat_' + p.get('id', '').replace('-', '_'))
    subtitle(doc, p.get('meaning_en', ''))

    # HOW TO USE — only if >=2 attach points OR >=2 conjugations (renderer gate)
    fr = p.get('form_rules') or {}
    attaches = fr.get('attaches_to') or []
    conjs = fr.get('conjugations') or []
    show_top = len(attaches) >= 2
    show_conj = len(conjs) >= 2
    if show_top or show_conj:
        section_header(doc, L['how_to_use'], '使い方')
        if show_top:
            t = doc.add_table(rows=0, cols=2); t.style = 'Table Grid'
            for a in attaches:
                cells = t.add_row().cells
                run(cells[0].paragraphs[0], attaches_label(a))
                run(cells[1].paragraphs[0], p.get('pattern', ''))
        if show_conj:
            t = doc.add_table(rows=1, cols=2); t.style = 'Table Grid'
            run(t.rows[0].cells[0].paragraphs[0], 'Form', bold=True)
            run(t.rows[0].cells[1].paragraphs[0], 'Example', bold=True)
            for c in conjs:
                cells = t.add_row().cells
                run(cells[0].paragraphs[0], c.get('label') or c.get('form') or '')
                run(cells[1].paragraphs[0], c.get('example') or '')

    # EXPLANATION
    if p.get('explanation_en'):
        section_header(doc, L['explanation'], '説明')
        run(para(doc), p['explanation_en'])

    # DEEP DIVE (essay)
    essay = p.get('essay')
    if isinstance(essay, dict):
        stub = essay.get('provenance') == 'needs_native_review'
        hdr = L['deep_dive'] + (' [stub]' if stub else '')
        section_header(doc, hdr, '詳細')
        labeled(doc, L['deep_dive_at_a_glance'], essay.get('intro'))
        labeled(doc, L['deep_dive_why'], essay.get('why_it_matters') or ('Pending native author.' if stub else None))
        labeled(doc, L['deep_dive_pitfalls'], essay.get('common_pitfalls'))
        labeled(doc, L['deep_dive_contrasts'], essay.get('contrasts'))
        labeled(doc, L['deep_dive_practice'], essay.get('closing_practice_tip') or ('Pending native author.' if stub else None))
        # C9 (2026-05-31): essay.cultural_context is NOT rendered here - it
        # duplicates the dedicated 'Cultural usage note' section below
        # (render-level de-dup; the note appears once per pattern).

    # EXAMPLES (audio dropped)
    examples = p.get('examples') or []
    if examples:
        section_header(doc, "%s (%d)" % (L['examples'], len(examples)), '例文')
        for ex in examples:
            pp = para(doc)
            if ex.get('form'):
                run(pp, "[%s] " % ex['form'], size=9, color=MUTED)
            run(pp, ex.get('ja', ''))
            if ex.get('translation_en'):
                run(pp, "  —  " + ex['translation_en'], italic=True, color=MUTED)

    # COMMON MISTAKES / Contrasts
    mistakes = p.get('common_mistakes') or []
    if mistakes:
        section_header(doc, L['common_mistakes'], '注意点')
        for m in mistakes:
            if m.get('kind') == 'register_variant':
                pp = para(doc)
                if m.get('label_a'):
                    run(pp, m['label_a'] + ": ", bold=True, color=MUTED)
                run(pp, m.get('form_a') or m.get('wrong') or '')
                pp2 = para(doc, space_before=0)
                if m.get('label_b'):
                    run(pp2, m['label_b'] + ": ", bold=True, color=MUTED)
                run(pp2, m.get('form_b') or m.get('right') or '')
            else:
                pp = para(doc)
                run(pp, "✗ ", bold=True, color=WRONG_RED)
                run(pp, m.get('wrong', ''), strike=True, color=WRONG_RED)
                pp2 = para(doc, space_before=0)
                run(pp2, "✓ ", bold=True, color=RIGHT_GREEN)
                run(pp2, m.get('right', ''), bold=True, color=RIGHT_GREEN)
            if m.get('why'):
                run(para(doc, space_before=0, space_after=6), m['why'], size=10, color=MUTED)

    # Categorized common-learner errors (wrong_corrected_pair)
    wcp = p.get('wrong_corrected_pair') or []
    if wcp:
        section_header(doc, "%s (%d)" % (L['wcp_section'], len(wcp)), '誤用')
        for m in wcp:
            cat = m.get('error_category')
            if cat:
                run(para(doc, space_after=0), "[%s]" % (L.get('cat_' + cat, cat)), size=9, bold=True, color=MUTED)
            pp = para(doc, space_before=0)
            run(pp, "✗ " + L['wcp_wrong'] + " ", bold=True, color=WRONG_RED)
            run(pp, m.get('wrong', ''), strike=True, color=WRONG_RED)
            pp2 = para(doc, space_before=0)
            run(pp2, "✓ " + L['wcp_correct'] + " ", bold=True, color=RIGHT_GREEN)
            run(pp2, m.get('correct', ''), bold=True, color=RIGHT_GREEN)
            if m.get('why'):
                run(para(doc, space_before=0, space_after=6), m['why'], size=10, color=MUTED)

    # Politeness ladder
    ladder = p.get('politeness_ladder')
    if isinstance(ladder, dict):
        section_header(doc, L['ladder_section'], '丁寧さ')
        t = doc.add_table(rows=0, cols=2); t.style = 'Table Grid'
        for tier in ['casual', 'polite', 'humble', 'respectful']:
            if ladder.get(tier):
                cells = t.add_row().cells
                run(cells[0].paragraphs[0], L['ladder_' + tier], bold=True)
                run(cells[1].paragraphs[0], ladder[tier])

    # Public-domain references
    pd = p.get('public_domain_refs') or []
    if pd:
        section_header(doc, 'Public-domain references', '出典')
        for r in pd:
            pp = para(doc)
            run(pp, r.get('work_title', ''), bold=True)
            if r.get('author'):
                death = " (died %s)" % r['author_death_year'] if r.get('author_death_year') else ''
                run(pp, "  — " + r['author'] + death, size=10, color=MUTED)
            if r.get('pd_status'):
                run(para(doc, space_before=0), r['pd_status'], size=9, color=MUTED)
            if r.get('quote_ja'):
                run(para(doc, space_before=0), r['quote_ja'])
            if r.get('quote_translation_en'):
                run(para(doc, space_before=0), r['quote_translation_en'], size=10, italic=True, color=MUTED)
            if r.get('context'):
                run(para(doc, space_before=0), r['context'], size=10, color=MUTED)
            if r.get('pattern_role'):
                run(para(doc, space_before=0, space_after=4), r['pattern_role'], size=10, italic=True, color=MUTED)

    # Notes
    if p.get('notes'):
        section_header(doc, L['notes'], '')
        run(para(doc), p['notes'])

    # Cultural usage note
    cc = p.get('cultural_callout')
    if isinstance(cc, dict) and (cc.get('note') or cc.get('contexts')):
        section_header(doc, 'Cultural usage note', '文化')
        if cc.get('note'):
            run(para(doc), cc['note'])
        if cc.get('contexts'):
            run(para(doc, space_before=0), "Contexts: " + ", ".join(cc['contexts']), size=10, color=MUTED)

    # Seen in the real world (authentic_refs — distinct from internal authentic_citations)
    ar = p.get('authentic_refs') or []
    if ar:
        section_header(doc, 'Seen in the real world', '')
        for cid in ar:
            run(para(doc, space_before=0), "• " + str(cid), size=10)

    reviewer_box(doc)


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else 'n5-121'
    g = json.load(open(GRAMMAR, encoding='utf-8'))
    allp = g if isinstance(g, list) else (g.get('patterns') or list(g.values())[0])
    L = json.load(open(EN_LOCALE, encoding='utf-8')).get('grammar_detail', {})

    if arg == 'all':
        pats = ordered_patterns(allp)
        out_name = "N5-grammar-178-patterns-for-native-review.docx"
    else:
        pats = [p for p in allp if p.get('id') == arg]
        if not pats:
            print("pattern not found:", arg); return 1
        out_name = "N5-grammar-review-SAMPLE-%s.docx" % arg

    doc = Document()
    # Set the Normal style to use a JA-capable east-Asian font so table cells
    # and any default paragraphs render kana/kanji correctly.
    st = doc.styles['Normal']
    st.font.name = LATIN
    st.font.size = Pt(11)
    _rpr = st.element.get_or_add_rPr()
    _rfonts = _rpr.find(qn('w:rFonts'))
    if _rfonts is None:
        _rfonts = OxmlElement('w:rFonts')
        _rpr.append(_rfonts)
    _rfonts.set(qn('w:ascii'), LATIN)
    _rfonts.set(qn('w:hAnsi'), LATIN)
    _rfonts.set(qn('w:eastAsia'), CJK)

    if arg == 'all':
        build_toc(doc, pats, L)

    for i, p in enumerate(pats):
        render_pattern(doc, p, L, first=(i == 0))

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, out_name)
    doc.save(out_path)
    print("wrote", out_path, "(%d pattern(s))" % len(pats))

    # Full review packet only: keep exactly ONE date-stamped copy in the folder.
    # Remove older stamped copies first, then emit a fresh one, so a reviewer is
    # never handed a stale upload. (Procedure manual Appendix F.53.)
    if arg == 'all':
        import glob, shutil, datetime
        stem = os.path.splitext(out_path)[0]
        for prev in glob.glob(stem + "_*.docx"):
            os.remove(prev)
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        dated = "%s_%s.docx" % (stem, stamp)
        shutil.copy2(out_path, dated)
        print("wrote dated copy", os.path.basename(dated), "(older dated copies removed)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
