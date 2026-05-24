"""
Build JLPT_N5_Grammar_Patterns.docx — complete N5 grammar syllabus.

Source : data/grammar.json (178 patterns) + data/audio_manifest.json
Output : data/complete course syllabus/JLPT_N5_Grammar_Patterns.docx
Layout : 1 pattern per page, grouped by category (categoryOrder), then patternOrder.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor, Cm


# ---------- paths ----------

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
OUT_DIR = ROOT / "data" / "complete course syllabus"
OUT_FILE = OUT_DIR / "JLPT_N5_Grammar_Patterns.docx"

SPA_URL_TEMPLATE = "https://gauravaccentureproducts.github.io/JLPTSuccess/N5/#/learn/{id}"
AUDIO_URL_TEMPLATE = "https://gauravaccentureproducts.github.io/JLPTSuccess/N5/{path}"

GREEN = RGBColor(0x14, 0x45, 0x2A)
GREEN_SOFT = RGBColor(0x1A, 0x5C, 0x38)
MUTED = RGBColor(0x55, 0x55, 0x55)
WRONG = RGBColor(0xAA, 0x33, 0x33)
RIGHT = RGBColor(0x1A, 0x5C, 0x38)


# ---------- low-level helpers ----------

def add_page_break(doc):
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


def add_para(doc, text, *, bold=False, italic=False, size=11, color=None, align=None, lang=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    if lang is not None:
        _set_run_lang(run, lang)
    return p


def _set_run_lang(run, lang):
    rPr = run._element.get_or_add_rPr()
    langel = rPr.find(qn("w:lang"))
    if langel is None:
        langel = OxmlElement("w:lang")
        rPr.append(langel)
    if lang == "ja":
        langel.set(qn("w:val"), "ja-JP")
        langel.set(qn("w:eastAsia"), "ja-JP")
        langel.set(qn("w:bidi"), "ja-JP")
    else:
        langel.set(qn("w:val"), "en-US")
        langel.set(qn("w:eastAsia"), "ja-JP")
        langel.set(qn("w:bidi"), "en-US")


def add_heading(doc, text, level=1, *, color=GREEN):
    h = doc.add_heading("", level=level)
    run = h.add_run(text)
    run.font.color.rgb = color
    run.font.size = Pt({1: 18, 2: 14, 3: 12}.get(level, 12))
    return h


def add_kv(doc, label, value, *, value_lang=None):
    """Bold 'Label: ' followed by value, single paragraph."""
    if value is None or value == "":
        return
    p = doc.add_paragraph()
    r1 = p.add_run(f"{label}: ")
    r1.bold = True
    r1.font.size = Pt(10)
    r2 = p.add_run(str(value))
    r2.font.size = Pt(10)
    if value_lang is not None:
        _set_run_lang(r2, value_lang)
    return p


def add_bilingual_block(doc, ja_text, en_text, *, audio_filename=None, audio_url=None):
    """Render a JA/EN sentence pair indented like an .ex block."""
    if ja_text:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.4)
        r_tag = p.add_run("[JA]  ")
        r_tag.bold = True
        r_tag.font.size = Pt(9)
        r_tag.font.color.rgb = MUTED
        r_ja = p.add_run(ja_text)
        r_ja.font.size = Pt(11)
        _set_run_lang(r_ja, "ja")
    if en_text:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.4)
        r_tag = p.add_run("[EN]  ")
        r_tag.bold = True
        r_tag.font.size = Pt(9)
        r_tag.font.color.rgb = MUTED
        r_en = p.add_run(en_text)
        r_en.font.size = Pt(11)
        r_en.font.color.rgb = MUTED
    if audio_filename:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.4)
        r_tag = p.add_run("[Audio] ")
        r_tag.bold = True
        r_tag.font.size = Pt(9)
        r_tag.font.color.rgb = MUTED
        r_fn = p.add_run(audio_filename + "   ")
        r_fn.font.size = Pt(9)
        r_fn.font.color.rgb = MUTED
        if audio_url:
            _add_hyperlink(p, audio_url, audio_url, size_pt=8, color=GREEN_SOFT)


def _add_hyperlink(paragraph, url, text, *, size_pt=10, color=GREEN):
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    color_el = OxmlElement("w:color")
    color_el.set(qn("w:val"), f"{color[0]:02x}{color[1]:02x}{color[2]:02x}")
    rPr.append(color_el)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rPr.append(underline)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(size_pt * 2))
    rPr.append(sz)
    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


def add_wr_pair(doc, wrong_text, right_text, explanation):
    if wrong_text:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.4)
        r1 = p.add_run("✗ ")
        r1.font.color.rgb = WRONG
        r1.bold = True
        r2 = p.add_run(wrong_text)
        r2.font.color.rgb = WRONG
        _set_run_lang(r2, "ja")
    if right_text:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.4)
        r1 = p.add_run("✓ ")
        r1.font.color.rgb = RIGHT
        r1.bold = True
        r2 = p.add_run(right_text)
        r2.font.color.rgb = RIGHT
        _set_run_lang(r2, "ja")
    if explanation:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.4)
        r = p.add_run(explanation)
        r.font.size = Pt(10)
        r.font.color.rgb = MUTED
        r.italic = True


# ---------- main builders ----------

def build_cover(doc, n_patterns, n_categories):
    add_heading(doc, "JLPT N5", level=1, color=GREEN)
    add_heading(doc, "Complete Grammar Syllabus", level=2, color=GREEN_SOFT)
    add_para(doc, "")
    add_para(doc, f"{n_patterns} grammar patterns across {n_categories} categories", size=12, italic=True, color=MUTED)
    add_para(doc, f"Generated: {date.today().isoformat()}", size=10, color=MUTED)
    add_para(doc, "Source: JLPTSuccess N5 — data/grammar.json", size=10, color=MUTED)
    add_para(doc, "")
    add_para(doc, "Page layout per pattern", size=11, bold=True, color=GREEN_SOFT)
    bullets = [
        "Pattern name (Japanese + ID)",
        "Meaning (Japanese + English)",
        "Japanese explanation [Phase 2: to be authored by native reviewer]",
        "English explanation",
        "Pattern usage — attaches-to + conjugation table",
        "Example sentences (Japanese + English + audio reference)",
        "Common mistakes",
        "Wrong / corrected pairs",
        "Cultural callout / register / notes (where authored)",
        "Footer metadata: Pattern ID, Tier, Category, Genki & Minna no Nihongo cross-refs",
    ]
    for b in bullets:
        p = doc.add_paragraph(style="List Bullet")
        r = p.add_run(b)
        r.font.size = Pt(10)
    add_page_break(doc)


def build_toc(doc, patterns_by_category):
    add_heading(doc, "Table of Contents", level=1)
    for cat_name, lst in patterns_by_category:
        add_para(doc, f"{cat_name}  ({len(lst)} patterns)", size=11, bold=True, color=GREEN_SOFT)
        for p in lst:
            line = doc.add_paragraph()
            line.paragraph_format.left_indent = Cm(0.6)
            r1 = line.add_run(f"  {p['id']}  —  ")
            r1.font.size = Pt(10)
            r1.font.color.rgb = MUTED
            r2 = line.add_run(p["pattern"])
            r2.font.size = Pt(10)
            _set_run_lang(r2, "ja")
            r3 = line.add_run(f"   ({p.get('meaning_en','')})")
            r3.font.size = Pt(9)
            r3.font.color.rgb = MUTED
        add_para(doc, "", size=4)
    add_page_break(doc)


def build_category_divider(doc, cat_name, n_in_cat, cat_no):
    add_heading(doc, f"Category {cat_no}: {cat_name}", level=1)
    add_para(doc, f"{n_in_cat} grammar patterns in this category.", size=10, italic=True, color=MUTED)
    add_page_break(doc)


def build_pattern(doc, p):
    # 4.1 Pattern name - matches TOC format: "<id> — <pattern>"
    pname_h = doc.add_heading("", level=1)
    r_id = pname_h.add_run(f"{p['id']} ")
    r_id.font.color.rgb = MUTED
    r_id.font.size = Pt(20)
    r_dash = pname_h.add_run("— ")
    r_dash.font.color.rgb = GREEN
    r_dash.font.size = Pt(20)
    pname_run = pname_h.add_run(p["pattern"])
    pname_run.font.color.rgb = GREEN
    pname_run.font.size = Pt(20)
    _set_run_lang(pname_run, "ja")

    # subtitle: meaning_en
    sub = doc.add_paragraph()
    r_sub = sub.add_run(p.get("meaning_en", ""))
    r_sub.italic = True
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = GREEN_SOFT

    # SPA link
    link_p = doc.add_paragraph()
    link_p.add_run("Open interactive page: ").font.size = Pt(9)
    _add_hyperlink(link_p, SPA_URL_TEMPLATE.format(id=p["id"]), SPA_URL_TEMPLATE.format(id=p["id"]), size_pt=9, color=GREEN_SOFT)

    # 4.7 Meaning JP + EN
    add_heading(doc, "Meaning", level=2)
    add_kv(doc, "Japanese", p.get("meaning_ja", ""), value_lang="ja")
    add_kv(doc, "English", p.get("meaning_en", ""))

    # 4.2 JA description (placeholder per user decision option d)
    add_heading(doc, "説明 (Japanese description)", level=2)
    ph = doc.add_paragraph()
    r_ph = ph.add_run("[Phase 2: Japanese explanation to be authored by native reviewer]")
    r_ph.italic = True
    r_ph.font.color.rgb = MUTED
    r_ph.font.size = Pt(10)

    # 4.3 EN description
    add_heading(doc, "Explanation (English)", level=2)
    add_para(doc, p.get("explanation_en", "").strip(), size=11)

    # 4.4 Usage — attaches_to + conjugations
    form_rules = p.get("form_rules") or {}
    if form_rules:
        add_heading(doc, "Pattern usage", level=2)
        attaches = form_rules.get("attaches_to") or []
        if attaches:
            add_kv(doc, "Attaches to", ", ".join(attaches))
        conjugations = form_rules.get("conjugations") or []
        if conjugations:
            add_para(doc, "Conjugations / forms:", size=10, bold=True)
            tbl = doc.add_table(rows=1, cols=3)
            tbl.style = "Light Grid Accent 1"
            hdr = tbl.rows[0].cells
            hdr[0].text = "Form"
            hdr[1].text = "Label"
            hdr[2].text = "Example (JA)"
            for c in conjugations:
                row = tbl.add_row().cells
                row[0].text = c.get("form", "")
                row[1].text = c.get("label", "")
                row[2].text = c.get("example", "")
                _set_run_lang(row[2].paragraphs[0].runs[0], "ja") if row[2].paragraphs[0].runs else None

    # 4.5 + 4.6 Examples + audio
    examples = p.get("examples") or []
    if examples:
        add_heading(doc, "Example sentences", level=2)
        for i, ex in enumerate(examples, start=1):
            ja = ex.get("ja", "")
            en = ex.get("translation_en", "")
            audio_path = ex.get("audio", "")
            audio_url = AUDIO_URL_TEMPLATE.format(path=audio_path) if audio_path else None
            num_p = doc.add_paragraph()
            rn = num_p.add_run(f"Example {i}" + (f"  ({ex.get('form','')})" if ex.get("form") else ""))
            rn.bold = True
            rn.font.size = Pt(10)
            rn.font.color.rgb = GREEN_SOFT
            add_bilingual_block(doc, ja, en, audio_filename=audio_path, audio_url=audio_url)

    # Common mistakes (extra) — data fields: wrong, right, why
    cm = p.get("common_mistakes") or []
    if cm:
        add_heading(doc, "Common mistakes", level=2)
        for m in cm:
            add_wr_pair(doc, m.get("wrong", ""), m.get("right", ""), m.get("why", ""))

    # Wrong/corrected pairs (extra) — data fields: wrong, correct, why
    wcp = p.get("wrong_corrected_pair") or []
    if wcp:
        add_heading(doc, "Wrong / corrected pairs", level=2)
        for w in wcp:
            add_wr_pair(doc, w.get("wrong", ""), w.get("correct", ""), w.get("why", ""))

    # Contrasts (extra)
    contrasts = p.get("contrasts") or []
    if contrasts:
        add_heading(doc, "Contrasts with similar patterns", level=2)
        for c in contrasts:
            if isinstance(c, dict):
                target = c.get("with") or c.get("pattern") or ""
                expl = c.get("explanation_en") or c.get("explanation") or ""
                if target or expl:
                    add_kv(doc, f"vs. {target}", expl)
            elif isinstance(c, str):
                add_para(doc, c, size=10)

    # Notes / cultural / register / essay
    notes = p.get("notes")
    if isinstance(notes, str) and notes.strip():
        add_heading(doc, "Notes", level=2)
        add_para(doc, notes, size=10, italic=True, color=MUTED)
    cc = p.get("cultural_callout")
    if isinstance(cc, str) and cc.strip():
        add_heading(doc, "Cultural callout", level=2)
        add_para(doc, cc, size=10)
    elif isinstance(cc, dict):
        text = cc.get("text") or cc.get("body") or ""
        if text:
            add_heading(doc, "Cultural callout", level=2)
            add_para(doc, text, size=10)
    essay = p.get("essay")
    if isinstance(essay, dict):
        intro = essay.get("intro")
        why = essay.get("why_it_matters")
        if intro or why:
            add_heading(doc, "Pedagogical essay", level=2)
            if intro:
                add_kv(doc, "Intro", intro)
            if why:
                add_kv(doc, "Why it matters", why)
            cp = essay.get("common_pitfalls")
            if cp:
                add_kv(doc, "Common pitfalls", cp)
            ctip = essay.get("closing_practice_tip")
            if ctip:
                add_kv(doc, "Practice tip", ctip)

    # Cross-reference metadata
    add_heading(doc, "Cross-references", level=2)
    add_kv(doc, "Register", p.get("register", ""))
    gl = p.get("genki_lesson")
    if gl:
        add_kv(doc, "Genki lesson", gl)
    mc = p.get("minna_chapter")
    if mc:
        add_kv(doc, "Minna no Nihongo chapter", mc)
    # public_domain_refs head if available
    pdr = p.get("public_domain_refs")
    if isinstance(pdr, list) and pdr:
        refs = [r if isinstance(r, str) else (r.get("title") or r.get("source") or "") for r in pdr]
        refs = [r for r in refs if r]
        if refs:
            add_kv(doc, "Public-domain refs", "; ".join(refs[:5]) + (" ..." if len(refs) > 5 else ""))

    add_page_break(doc)


def main():
    with GRAMMAR_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)
    patterns = data["patterns"]
    # sort
    patterns_sorted = sorted(patterns, key=lambda p: (p.get("categoryOrder", 999), p.get("patternOrder", 999), p.get("id", "")))

    # group by category
    from collections import OrderedDict
    by_cat = OrderedDict()
    for p in patterns_sorted:
        by_cat.setdefault(p.get("category", "Uncategorised"), []).append(p)

    doc = Document()
    # Default to 11pt Calibri-equivalent with East Asian fallback
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    rpr = style.element.rPr
    rFonts = rpr.find(qn("w:rFonts")) if rpr is not None else None
    if rFonts is not None:
        rFonts.set(qn("w:eastAsia"), "Yu Gothic")

    build_cover(doc, len(patterns_sorted), len(by_cat))
    build_toc(doc, list(by_cat.items()))

    for cat_no, (cat_name, lst) in enumerate(by_cat.items(), start=1):
        build_category_divider(doc, cat_name, len(lst), cat_no)
        for p in lst:
            build_pattern(doc, p)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc.save(OUT_FILE)
    print(f"OK wrote {OUT_FILE}")
    print(f"   patterns: {len(patterns_sorted)}   categories: {len(by_cat)}")


if __name__ == "__main__":
    main()
