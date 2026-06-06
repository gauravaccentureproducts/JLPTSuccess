#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a Word (.docx) of N5 vocabulary entries for native-speaker review.

Mirrors what the SPA vocab page (renderVocabDetail in js/learn-vocab.js)
shows in the DEFAULT (English) locale, one entry per page, EXCEPT:
  - audio players / controls are dropped (sentence text is kept)
  - furigana ruby is rendered as plain Japanese text
  - chrome (nav, back-link, mark-known toggle) is dropped
  - keigo-chain visualiser is omitted (its data lives in JS, not the corpus)

Companion to tools/build_grammar_review_docx.py — same visual language,
same reviewer-notes box per entry, same TOC bookmark-link scheme.

Usage:
  python tools/build_vocab_review_docx.py 私              # one entry by form (sample)
  python tools/build_vocab_review_docx.py all             # all 995 entries
Output: docs/vocab-review/<name>.docx
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
VOCAB = os.path.join(ROOT, "data", "vocab.json")
EN_LOCALE = os.path.join(ROOT, "locales", "en.json")
OUT_DIR = os.path.join(ROOT, "docs", "vocab-review")

CJK = "Yu Gothic"
LATIN = "Calibri"
WRONG_RED = RGBColor(0xB3, 0x1B, 0x1B)
RIGHT_GREEN = RGBColor(0x1A, 0x5C, 0x38)
MUTED = RGBColor(0x66, 0x66, 0x66)
HEAD_DARK = RGBColor(0x14, 0x45, 0x2A)

# --- vocab super-categories for the front TOC (each maps to several
# numbered section labels seen in data/vocab.json). The 41 N5 vocab
# sections collapse to 8 cleaner groupings the reviewer can navigate
# without scrolling a 41-row TOC stub. ---
VOCAB_SUPERCATS = [
    ('People & Self', [
        '1. People - Pronouns and Self', '2. People - Family',
        '3. People - Roles', '4. Body Parts',
    ]),
    ('Demonstratives, Questions & Numbers', [
        '5. Demonstratives', '6. Question Words', '7. Numbers',
        '8. Native Counters (つ-series)', '9. Counters (Common)',
    ]),
    ('Time', [
        '10. Time - General', '11. Time - Days, Weeks, Months, Years',
        '12. Time - Frequency / Sequence',
    ]),
    ('Place & Nature', [
        '13. Locations and Places (general)', '14. Nature and Weather',
        '15. Animals',
    ]),
    ('Food, Daily Life, Money', [
        '16. Food and Drink - General', '17. Food - Items',
        '18. Drinks', '19. Tableware and Cooking', '20. Colors',
        '21. Clothing and Accessories', '22. Money and Shopping',
        '23. Transport', '26. House and Furniture',
    ]),
    ('School, Languages, Countries', [
        '24. School and Study', '25. Languages and Countries',
    ]),
    ('Verbs', [
        '27. Verbs - Group 1 (う-verbs)', '28. Verbs - Group 2 (る-verbs)',
        '29. Verbs - Irregular and する-verbs',
        '30. Verbs - Existence and Possession',
    ]),
    ('Adjectives, Adverbs, Function Words', [
        '31. い-Adjectives', '32. な-Adjectives', '33. Adverbs',
        '34. Conjunctions', '35. Particles (functional vocabulary)',
        '36. Greetings and Set Phrases',
        '37. Common Nouns - Miscellaneous', '37. Common nouns - miscellaneous',
        '38. Sounds and Voice', '39. Function / Filler Expressions',
        '40. Misc Useful Items',
    ]),
]


def supercat_for(entry):
    sec = entry.get('section', '') or ''
    for sc, members in VOCAB_SUPERCATS:
        if sec in members:
            return sc
    return 'Adjectives, Adverbs, Function Words'  # catch-all


def _section_sort_key(sec):
    """Sort sections by their leading number (e.g. '1.', '10.', '37.')."""
    head = (sec or '').split('.', 1)[0].strip()
    try:
        return (int(head), sec)
    except ValueError:
        return (10_000, sec)


def ordered_entries(allp):
    """Order: super-category bucket → section number → frequency_rank → form."""
    buckets = {sc: [] for sc, _ in VOCAB_SUPERCATS}
    for e in allp:
        buckets[supercat_for(e)].append(e)
    out = []
    for sc, _ in VOCAB_SUPERCATS:
        group = buckets[sc]
        group.sort(key=lambda e: (
            _section_sort_key(e.get('section', '')),
            e.get('frequency_rank') or 9_999_999,
            e.get('form', ''),
        ))
        out.extend(group)
    return out


# --- pitch-accent renderer (mirror of _pitchPattern in learn-vocab.js) ---
def _pitch_pattern(pa, reading):
    """Render the HL contour for {mora, drop} on the kana reading.
    drop=0 → 平板 (heiban); pitch rises after mora 1 and never falls.
    drop=N (N>=1) → pitch rises after mora 1, falls after mora N.
    The renderer prefixes each kana with H or L; we keep it ASCII for
    the docx (HL letters next to kana mora, separated by spaces).
    """
    if not pa or not reading:
        return ''
    drop = pa.get('drop')
    if drop is None:
        return ''
    moras = list(reading)  # crude; ya-on like ki+ya forms one mora but
                           # this is reviewer-readable enough as docx text.
    pieces = []
    for i, k in enumerate(moras, start=1):
        if i == 1:
            tag = 'L' if (drop != 1) else 'H'
        elif drop == 0:
            tag = 'H'
        elif i <= drop:
            tag = 'H'
        else:
            tag = 'L'
        pieces.append(f"{tag}{k}")
    return ' '.join(pieces) + (' (heiban)' if drop == 0 else f' (drop after mora {drop})')


def _counter_kana(counter):
    """Render counter.kana or fallback for a counter dict."""
    if not isinstance(counter, dict):
        return ''
    return counter.get('reading') or counter.get('kana') or counter.get('kanji') or ''


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
    """Reviewer notes table — pre-populated with a visible '未確認 /
    not yet reviewed' placeholder so unreviewed entries flag themselves
    rather than being silently empty (addresses OPEN-001 mechanically:
    the human native reviewer DELETES the placeholder when filling in
    「問題なし。」 or 「要修正: ...」, so the queue of unreviewed entries
    is visually obvious throughout the document until each one is
    addressed). 2026-06-04, batch I."""
    p = para(doc, space_before=10, space_after=2)
    run(p, "Reviewer notes", bold=True, size=11, color=MUTED)
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)

    # Placeholder line 1: status marker in red so empty entries stand out
    cp1 = cell.paragraphs[0]
    cp1.paragraph_format.space_after = Pt(2)
    run(cp1, "☐ 未確認 / not yet reviewed",
        italic=True, color=WRONG_RED, size=10)

    # Placeholder line 2: instruction (small muted)
    cp2 = cell.add_paragraph()
    cp2.paragraph_format.space_after = Pt(6)
    run(cp2,
        "[Native reviewer: delete the line above and write 「問題なし。」 "
        "if the entry is correct, OR 「要修正: <issue>」 with a specific "
        "issue. Empty boxes are treated as 'not yet reviewed'.]",
        italic=True, color=MUTED, size=9)

    # Two empty paragraphs for actual reviewer text
    for _ in range(2):
        cp = cell.add_paragraph()
        cp.paragraph_format.space_after = Pt(6)


# --- clickable Table of Contents: bookmarks + internal hyperlinks ---
_BM_ID = [1000]


def _bookmark(paragraph, name):
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


def _entry_anchor(e):
    """Bookmark name safe for Word — bookmarks must be alnum-ish."""
    # Use the form, with non-alnum replaced. Append index to guarantee uniqueness.
    form = e.get('form', '') or e.get('id', '')
    safe = ''.join(c if c.isalnum() else '_' for c in form)
    # Bookmark names must start with a letter
    if not safe or not safe[0].isalpha():
        safe = 'v_' + safe
    # Cap length (Word's 40-char practical limit on bookmark names)
    safe = safe[:38]
    return safe


def build_readme(doc, entries, version_meta):
    """Front README page: orient the reviewer to the site, level, and task.

    Lives on its own page, before the clickable Contents page. Tells the
    reviewer what JLPTSuccess is, what N5 covers, what this packet is for,
    what they should check for each entry, and exactly where (the
    Reviewer-notes table at the bottom of every entry page) to write
    their comments.
    """
    # Title
    h = para(doc, space_before=0, space_after=4)
    run(h, "N5 Vocabulary — Native-Speaker Review Packet",
        bold=True, size=22, color=HEAD_DARK)

    # Doc metadata (count + site version + build date) right under the title.
    # vocab.json doesn't carry a corpus-version field, so we anchor to the
    # site release tag + the packet build date — that's the pair an
    # institutional reviewer needs to identify "which release did I review".
    from datetime import date
    site_v = version_meta.get('site_version') or '(unknown)'
    meta = para(doc, space_after=14)
    run(meta,
        "%d entries  ·  built %s  ·  JLPTSuccess release %s" % (
            len(entries),
            date.today().isoformat(),
            site_v),
        italic=True, size=10, color=MUTED)

    # 1. About JLPTSuccess
    h1 = para(doc, space_before=4, space_after=2)
    run(h1, "About JLPTSuccess", bold=True, size=14, color=HEAD_DARK)
    p1 = para(doc, space_after=4)
    run(p1,
        "JLPTSuccess is a free, learner-focused study site for the "
        "Japanese-Language Proficiency Test (JLPT). It runs in any modern "
        "browser at ")
    run(p1, "https://gauravaccentureproducts.github.io/JLPTSuccess/",
        color=RGBColor(0x05, 0x63, 0xC1))
    run(p1,
        ", works offline as a Progressive Web App, and ships with the "
        "full corpus (grammar patterns, vocabulary entries, kanji, reading "
        "passages, listening items, and mock exam questions) plus drills, "
        "tests, an SRS-style review queue, and bilingual UI (English + "
        "Hindi).")

    # 2. About the N5 level
    h2 = para(doc, space_before=10, space_after=2)
    run(h2, "About the N5 level", bold=True, size=14, color=HEAD_DARK)
    p2 = para(doc, space_after=4)
    run(p2,
        "JLPT has five levels: N5 (entry-level) → N4 → N3 → N2 → N1 "
        "(near-native). N5 is the first certification, aimed at learners "
        "who understand basic everyday Japanese: roughly 100 kanji, ~800 "
        "vocabulary items, basic verb conjugations and particles, simple "
        "polite-form sentences, and survival-level listening / reading.")
    p2b = para(doc, space_after=4)
    run(p2b, "This N5 corpus currently contains: ")
    run(p2b, "%d grammar patterns" % version_meta.get('counts', {}).get('grammar', 178), bold=True)
    run(p2b, " · ")
    run(p2b, "%d vocabulary entries" % len(entries), bold=True)
    run(p2b, " · ")
    run(p2b, "%d kanji" % version_meta.get('counts', {}).get('kanji', 106), bold=True)
    run(p2b, " · ")
    run(p2b, "%d reading passages" % version_meta.get('counts', {}).get('reading', 54), bold=True)
    run(p2b, " · ")
    run(p2b, "%d listening items" % version_meta.get('counts', {}).get('listening', 50), bold=True)
    run(p2b, " · ")
    run(p2b, "%d mock-test questions" % version_meta.get('counts', {}).get('paperQuestions', 402), bold=True)
    run(p2b, ". This packet covers ONLY the vocabulary corpus.")

    # 3. Purpose of this document
    h3 = para(doc, space_before=10, space_after=2)
    run(h3, "Purpose of this document", bold=True, size=14, color=HEAD_DARK)
    p3 = para(doc, space_after=4)
    run(p3,
        "Many of the 995 vocabulary entries were AI-generated, "
        "machine-translated, or auto-derived from corpus heuristics. "
        "Before the next public release we want a native Japanese speaker "
        "(ideally a JLPT instructor or native teacher) to verify each "
        "entry's accuracy. This packet renders the same content the "
        "live site shows on each vocab detail page — in printable form — "
        "so you can read and annotate offline.")

    # 4. What the reviewer should check
    h4 = para(doc, space_before=10, space_after=2)
    run(h4, "What you (the reviewer) are asked to check",
        bold=True, size=14, color=HEAD_DARK)
    p4 = para(doc, space_after=2)
    run(p4,
        "For each entry, please verify the following. Flag anything that "
        "is wrong, awkward, or off-level for N5:")
    checklist = [
        ('Form / Reading',
         'Does the kanji + kana headword spell the intended word correctly? '
         'Is the reading kana accurate?'),
        ('English gloss',
         'Does it convey the Japanese meaning at N5 level? Too narrow, '
         'too broad, idiomatic-only, or just wrong?'),
        ('Hindi gloss (when shown)',
         'Translation accuracy — does the Hindi term match the Japanese '
         'sense at N5 level?'),
        ('Example sentences',
         'Natural, grammatical, level-appropriate. Catch unnatural word '
         'order, wrong particles, kanji a beginner won\'t know, or '
         'sentences that don\'t illustrate the headword.'),
        ('Particle examples',
         'Are these the collocations a native speaker would actually use? '
         'Anything obviously template-generated rather than real usage?'),
        ('Counter (if shown)',
         'Is the counter shown the one a Japanese speaker would use for '
         'this object/concept?'),
        ('Verb class (for verbs)',
         'Group 1 (う-verb) / Group 2 (る-verb) / Irregular — correct? '
         'Group-1 exception flag accurate?'),
        ('False friends, pragmatic, devoiced vowels',
         'When shown, do these notes match how the word actually behaves '
         'in modern standard Japanese?'),
    ]
    for label, body in checklist:
        cp = para(doc, space_before=2, space_after=2)
        run(cp, "• " + label + ": ", bold=True)
        run(cp, body)

    # 5. Where to write your notes
    h5 = para(doc, space_before=10, space_after=2)
    run(h5, "Where to write your review comments",
        bold=True, size=14, color=HEAD_DARK)
    p5a = para(doc, space_after=4)
    run(p5a,
        "Each entry page has a gray-bordered ")
    run(p5a, "Reviewer notes", bold=True)
    run(p5a,
        " table box at the bottom (after the entry's last section). "
        "Click into that table and type your comments directly there. "
        "You can write in Japanese, English, or Hindi — whichever is "
        "natural. There is no required format: bullet points, prose, "
        "or short verdicts (\"OK\" / \"reading wrong: should be \") all "
        "work.")
    p5b = para(doc, space_after=4)
    run(p5b,
        "Please write your feedback in ", bold=False)
    run(p5b, "every entry's", bold=True)
    run(p5b,
        " Reviewer-notes box individually — do not skip entries. "
        "Per-entry feedback (one box at a time) is much easier for "
        "us to act on than a single end-of-document summary, and "
        "ensures every entry has been considered. Even a brief ",
        bold=False)
    run(p5b, "OK", bold=True)
    run(p5b, " / ", bold=False)
    run(p5b, "問題なし", bold=True)
    run(p5b,
        " counts as a reviewed entry — that signals \"I looked at "
        "this one, no changes needed.\"", bold=False)
    p5c = para(doc, space_after=4)
    run(p5c,
        "Heavy-rewrite suggestions (whole replacement examples, full new "
        "particle-example lists) are welcome — put them directly into the "
        "notes box; we'll port them back to the corpus on our end.")

    # 6. How to read the page layout
    h6 = para(doc, space_before=10, space_after=2)
    run(h6, "Quick guide to each entry page",
        bold=True, size=14, color=HEAD_DARK)
    guide = [
        ('Small gray header line',
         'The numbered section the entry belongs to (e.g. "1. People - '
         'Pronouns and Self"). 41 sections total, grouped on the '
         'Contents page into 8 super-categories.'),
        ('Large dark-green word',
         'The entry headword (form): kanji if used at N5, otherwise kana.'),
        ('Gray kana line below',
         'The reading (only shown when it differs from the form, e.g. '
         'kanji headwords).'),
        ('Italic gray subtitle',
         'The English gloss — short translation of the meaning.'),
        ('MEANING section',
         'Structured detail: English, Hindi gloss (when present), '
         'reading, counter, and verb-class (for verbs).'),
        ('Example sentences',
         'Real Japanese sentences using the entry, with English '
         'translation. Each line shows a "From pattern" or '
         '"Provenance" tag indicating where the example came from.'),
        ('Particle examples',
         'Short particle-collocation templates (e.g. "わたしの ともだち"). '
         'Historically called "collocations" — renamed because they are '
         'particle templates, not real corpus collocations.'),
        ('Provenance & review status',
         'A small footer showing which fields are AI-generated vs '
         'native-reviewed. Helpful context for prioritising your '
         'attention.'),
        ('Reviewer notes',
         'The gray-bordered box where you write your feedback. (See '
         'previous section.)'),
    ]
    for label, body in guide:
        gp = para(doc, space_before=1, space_after=1)
        run(gp, "• " + label + ": ", bold=True)
        run(gp, body)

    # 7. Logistics + thank-you
    h7 = para(doc, space_before=10, space_after=2)
    run(h7, "Logistics", bold=True, size=14, color=HEAD_DARK)
    p7 = para(doc, space_after=4)
    run(p7,
        "When you are done, simply ", bold=False)
    run(p7, "save the document", bold=True)
    run(p7,
        " with all your edits. You do ", bold=False)
    run(p7, "not", bold=True)
    run(p7,
        " need to send it anywhere — keep the file locally; our team "
        "will follow up to collect it (or you can hand it back via "
        "whatever channel we used to share it). Thank you for the "
        "time and care; native review is the single highest-impact "
        "step in our quality pipeline.", bold=False)

    doc.add_page_break()


def build_toc(doc, entries, L):
    """Front Contents page: clickable links per entry, grouped by super-cat then numbered section."""
    h = para(doc, space_before=0, space_after=4)
    run(h, "Contents", bold=True, size=20, color=HEAD_DARK)
    intro = para(doc, space_after=10)
    run(intro,
        "%d N5 vocabulary entries — click any entry to jump to its detail page." % len(entries),
        italic=True, size=10, color=MUTED)

    buckets = {sc: [] for sc, _ in VOCAB_SUPERCATS}
    for e in entries:
        buckets[supercat_for(e)].append(e)

    n = 0
    # Per-entry anchor index — we need globally unique bookmarks even when
    # two entries share a form spelling (rare but possible across sections).
    used_anchors = {}
    for sc, _ in VOCAB_SUPERCATS:
        group = buckets.get(sc) or []
        if not group:
            continue
        sc_head = para(doc, space_before=8, space_after=2)
        run(sc_head, sc, bold=True, size=13, color=HEAD_DARK)

        # Sub-group by section number so the TOC reads "1. People - Pronouns ... → 私, あなた, ..."
        by_sec = {}
        for e in group:
            by_sec.setdefault(e.get('section', '(none)'), []).append(e)
        for sec in sorted(by_sec.keys(), key=_section_sort_key):
            sec_head = para(doc, space_before=4, space_after=1)
            run(sec_head, sec, bold=False, size=11, color=MUTED)
            for e in by_sec[sec]:
                n += 1
                anchor = _entry_anchor(e)
                # Disambiguate collisions
                if anchor in used_anchors:
                    used_anchors[anchor] += 1
                    anchor = f"{anchor[:34]}_{used_anchors[anchor]}"
                else:
                    used_anchors[anchor] = 1
                e['_anchor'] = anchor
                line = para(doc, space_before=0, space_after=1)
                form = e.get('form', '')
                reading = e.get('reading', '')
                label = f"{n}.  {form}"
                if reading and reading != form:
                    label += f"  ({reading})"
                _toc_link(line, anchor, label)
                if e.get('gloss'):
                    run(line, "  —  " + e['gloss'], size=9, color=MUTED)
    doc.add_page_break()


# --- per-entry render (mirror of renderVocabDetail, EN locale) ---
def render_entry(doc, e, L, first):
    if not first:
        doc.add_page_break()

    # Section chip (small muted line above the title)
    if e.get('section'):
        sec_p = para(doc, space_before=0, space_after=0)
        run(sec_p, e['section'], size=9, color=MUTED)

    # Title: the form (kanji or kana headword)
    tp = title(doc, e.get('form', ''))
    _bookmark(tp, e.get('_anchor') or _entry_anchor(e))

    # Reading (kana under the title)
    if e.get('reading') and e['reading'] != e.get('form'):
        rp = para(doc, space_before=0, space_after=2)
        run(rp, e['reading'], size=13, color=MUTED)

    # Gloss as the subtitle (italic muted)
    subtitle(doc, e.get('gloss', ''))

    # MEANING (mirrors the SPA's structured detail block)
    section_header(doc, L.get('meaning', 'Meaning'), '意味')
    labeled(doc, L.get('english', 'English'), e.get('gloss') or '-')
    # Hindi gloss appears only when the locale isn't EN in the SPA. The
    # reviewer is bilingual; surface it as supplementary if present so they
    # can sanity-check both glosses.
    if e.get('gloss_hi'):
        labeled(doc, 'Hindi (gloss_hi)', e['gloss_hi'])
    if e.get('reading'):
        labeled(doc, L.get('japanese_reading', 'Japanese reading'), e['reading'])

    if e.get('counter'):
        labeled(doc, L.get('counter', 'Counter'), '〜' + _counter_kana(e['counter']))

    if e.get('verb_class'):
        class_labels = {
            'godan': 'Godan (Group 1, う-verb)',
            'ichidan': 'Ichidan (Group 2, る-verb)',
            'irregular': 'Irregular (Group 3 — する / 来る)',
        }
        label = class_labels.get(e['verb_class'], e['verb_class'])
        if e.get('group1_exception'):
            label += "  [Group-1 exception]"
        labeled(doc, L.get('verb_class', 'Verb class'), label)

    if e.get('transitivity'):
        t_text = e['transitivity']
        if e.get('pair_id'):
            t_text += f"  ({L.get('pair', 'pair')}: {e['pair_id']})"
        labeled(doc, L.get('transitivity', 'Transitivity'), t_text)

    # EXAMPLES (audio dropped)
    examples = e.get('examples') or []
    if examples:
        section_header(doc, f"{L.get('example_sentences', 'Example sentences')} ({len(examples)})", '例文')
        for ex in examples:
            pp = para(doc)
            run(pp, ex.get('ja', ''))
            if ex.get('translation_en'):
                run(pp, "  —  " + ex['translation_en'], italic=True, color=MUTED)
            if ex.get('source'):
                run(para(doc, space_before=0), L.get('from_pattern', 'From pattern') + ': ' + ex['source'], size=9, color=MUTED)
            elif ex.get('provenance'):
                run(para(doc, space_before=0), 'Provenance: ' + ex['provenance'], size=9, color=MUTED)

    # PARTICLE EXAMPLES (formerly "collocations")
    pe = e.get('particle_examples') or e.get('collocations') or []
    pe = [c for c in pe if isinstance(c, str) and c.strip()]
    if pe:
        section_header(doc, f"{L.get('particle_examples', 'Particle examples')} ({len(pe)})", '助詞例')
        for c in pe:
            p_ = para(doc, space_before=0, space_after=1)
            run(p_, '• ' + c)

    # FALSE FRIENDS
    ff = e.get('false_friends') or []
    if ff:
        section_header(doc, L.get('false_friends', "Don't confuse with"), '紛らわしい語')
        run(para(doc), ', '.join(ff))

    # PRAGMATIC FUNCTIONS
    pf = e.get('pragmatic_functions') or []
    if pf:
        section_header(doc, L.get('pragmatic', 'Multiple uses (pragmatic)'), '用法')
        for f in pf:
            pp = para(doc)
            run(pp, f.get('function', '') or '', bold=True)
            if f.get('gloss'):
                run(pp, '  —  ' + f['gloss'])
            if f.get('context'):
                run(para(doc, space_before=0), f['context'], size=10, color=MUTED)

    # DEVOICED VOWELS
    dv = e.get('devoiced_vowels')
    if isinstance(dv, dict):
        section_header(doc, L.get('devoiced_vowels', 'Pronunciation: devoiced vowels'), '無声化')
        if dv.get('positions'):
            labeled(doc, L.get('devoiced_position', 'Position(s)'),
                    ', '.join(str(p) for p in dv['positions']) + ' (0-indexed)')
        else:
            run(para(doc), L.get('devoiced_no_dev', 'No devoicing in standard Tokyo speech for this form.'),
                color=MUTED, size=10)
        if dv.get('note'):
            run(para(doc, space_before=0), dv['note'], size=10, color=MUTED)
        if dv.get('rule'):
            run(para(doc, space_before=0), L.get('devoiced_rule', 'Rule') + ': ' + dv['rule'], size=10, italic=True, color=MUTED)

    # COUNTER REGISTER (advanced counter detail)
    cr = e.get('counter_register')
    if isinstance(cr, dict):
        section_header(doc, L.get('counter_register', 'Counter register'), '助数詞・場面')
        if cr.get('counter'):
            label_text = '〜' + cr['counter']
            if cr.get('irregular'):
                label_text += '  [' + L.get('irregular', 'irregular') + ']'
            labeled(doc, L.get('counter_root', 'Counter root'), label_text)
        if cr.get('note'):
            run(para(doc), cr['note'])
        rp = cr.get('register_pair')
        if isinstance(rp, dict):
            if rp.get('casual_alt'):
                labeled(doc, L.get('casual', 'casual'), rp['casual_alt'])
            if rp.get('formal_same'):
                labeled(doc, L.get('formal', 'formal'), rp['formal_same'])

    # "Seen in the real world" (authentic_refs) intentionally NOT shown: the
    # refs are auto-derived placeholder ids (e.g. "auth.signs.ni-getsu") that
    # don't resolve to real example text, so they were noise for the reviewer.

    # PROVENANCE / REVIEW STATUS (audit-trail surface for the reviewer)
    if e.get('review_status') or e.get('gloss_provenance'):
        section_header(doc, 'Provenance & review status', '出処')
        if e.get('review_status'):
            labeled(doc, 'review_status', e['review_status'])
        if isinstance(e.get('gloss_provenance'), dict):
            for k, v in e['gloss_provenance'].items():
                labeled(doc, f"gloss_provenance.{k}", v)
        elif e.get('gloss_provenance'):
            labeled(doc, 'gloss_provenance', e['gloss_provenance'])

    reviewer_box(doc)


def _load_version_meta():
    """Pull vocab _meta.version + site version.json into a single dict so
    the README can stamp itself with the exact build state. Falls back
    gracefully if either file is missing."""
    out = {}
    try:
        with open(VOCAB, encoding='utf-8') as f:
            v = json.load(f)
        out['vocab_version'] = (v.get('_meta') or {}).get('version', '')
    except Exception:
        out['vocab_version'] = ''
    try:
        ver_fp = os.path.join(ROOT, 'data', 'version.json')
        with open(ver_fp, encoding='utf-8') as f:
            ver = json.load(f)
        out['site_version'] = ver.get('version', '')
        out['counts'] = ver.get('counts', {})
    except Exception:
        out['site_version'] = ''
        out['counts'] = {}
    return out


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else '私'
    with open(VOCAB, encoding='utf-8') as f:
        v = json.load(f)
    entries = v.get('entries') if isinstance(v, dict) else v
    if not isinstance(entries, list):
        print("could not read vocab entries"); return 1
    with open(EN_LOCALE, encoding='utf-8') as f:
        L = json.load(f).get('vocab_detail', {})

    version_meta = _load_version_meta()

    if arg == 'all':
        ents = ordered_entries(entries)
        out_name = "N5-vocab-995-entries-for-native-review.docx"
    else:
        # Match by form (kanji/kana headword)
        ents = [e for e in entries if e.get('form') == arg]
        if not ents:
            print("vocab not found:", arg); return 1
        out_name = "N5-vocab-review-SAMPLE-%s.docx" % arg.replace('/', '_').replace(' ', '_')

    doc = Document()
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

    # README always renders first — both for the full 995-entry packet
    # AND single-entry samples (so the reviewer who receives the sample
    # also gets the orientation context).
    build_readme(doc, ents, version_meta)

    if arg == 'all':
        build_toc(doc, ents, L)

    for i, e in enumerate(ents):
        render_entry(doc, e, L, first=(i == 0))

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, out_name)
    doc.save(out_path)
    print("wrote", out_path, "(%d entry/entries)" % len(ents))
    return 0


if __name__ == '__main__':
    sys.exit(main())
