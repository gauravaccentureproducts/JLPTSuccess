"""Build mock-test "papers" from KB question files.

Closes the major KB-utilization gap: ~400 audited questions in
KnowledgeBank/{moji,goi,bunpou,dokkai}_questions_n5.md were not flowing
to the runtime. This script parses them, slices into 15-question papers
per category, and emits paper JSON files plus a manifest the runtime
loads.

Output:
  data/papers/manifest.json          — index of all papers
  data/papers/moji/paper-N.json      — moji papers (50 + 50 = 100 Qs → 7)
  data/papers/goi/paper-N.json       — goi papers (~7)
  data/papers/bunpou/paper-N.json    — bunpou papers (~7)
  data/papers/dokkai/paper-N.json    — dokkai papers (~6, passage-grouped)

Format per paper:
  {
    "id": "moji-1",
    "category": "moji",
    "paperNumber": 1,
    "name": "Moji Paper 1",
    "source_file": "KnowledgeBank/moji_questions_n5.md",
    "source_question_range": "Q1-Q15",
    "questionCount": 15,
    "questions": [
      {
        "id": "moji-1.1",            # paper-id . index
        "kbSourceId": "Q1",
        "type": "mcq",
        "stem_html": "あの 人は <u>学生</u> です。",
        "choices": ["がくせ", "がくせい", "かくせい", "かくせ"],
        "correctIndex": 1,            # 0-based; the source uses 1-based "Answer: 2"
        "rationale_en": "学 (ガク) + 生 (セイ)."
      }, ...
    ]
  }

Skipped files:
  externally_sourced_n5.md — provenance disclosed in its header (third-
    party scraped, NOT JEES official). Excluded from v1 to avoid sourcing
    issues; can be added later under its own category if desired.
    (Renamed from authentic_extracted_n5.md on 2026-05-04 to match its
    H1 title; see CHANGELOG v1.12.5.)
  grammar_n5.md / kanji_n5.md / vocabulary_n5.md — catalogs, not question
    banks; already built by tools/build_data.py.

Run:
  python tools/build_papers.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "KnowledgeBank"
OUT = ROOT / "data" / "papers"

# Per-paper question count. The user requested 15.
PAPER_SIZE = 15

# Categories sourced from KB files.
SOURCES = {
    "moji":   "moji_questions_n5.md",
    "goi":    "goi_questions_n5.md",
    "bunpou": "bunpou_questions_n5.md",
    "dokkai": "dokkai_questions_n5.md",
    # externally_sourced_n5.md skipped per docstring rationale.
}

CATEGORY_META = {
    "moji":   {"label": "Moji",    "label_ja": "文字",     "description": "Kanji reading + orthography"},
    "goi":    {"label": "Goi",     "label_ja": "語彙",     "description": "Vocabulary in context"},
    "bunpou": {"label": "Bunpou",  "label_ja": "文法",     "description": "Grammar (choose form / arrange / passage)"},
    "dokkai": {"label": "Dokkai",  "label_ja": "読解",     "description": "Reading comprehension"},
}


# -----------------------------------------------------------------------
# Parsing helpers
# -----------------------------------------------------------------------

def split_questions(md: str) -> list[tuple[str, str]]:
    """Split an MD body into question blocks.

    Returns list of (question_label, body) tuples. Each body is the text
    AFTER the `### Q<n>` header up to (but not including) the next
    `### Q<n>` or `## ` heading.
    """
    # Q-headers can be `### Q<N>` or `#### Q<N>` (dokkai uses both, with
    # passage headers at `### Passage <N>` and Qs at `#### Q<N>`).
    Q_HEADER = re.compile(r'(?m)^(#{3,4})\s+Q(\d+)\b[^\n]*$')
    matches = list(Q_HEADER.finditer(md))
    if not matches:
        return []
    blocks: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = md[m.end():end].strip()
        # Stop body at the next ## or ### heading (but NOT #### Q...).
        # Without this, a Mondai-3 Q's body slurps the next `### Passage`
        # header and the answer-rationale regex (DOTALL) treats the whole
        # passage as rationale text. The negative lookahead skips Q-headers
        # at any level so we don't break the Q-to-Q boundary.
        section_break = re.search(r'(?m)^#{2,3}\s+(?!Q\d)', body)
        if section_break:
            body = body[:section_break.start()].strip()
        label = f"Q{m.group(2)}"
        blocks.append((label, body))
    return blocks


def parse_mcq_question(body: str) -> dict | None:
    """Parse a standard MCQ body: stem, 4 numbered choices, answer line.

    Returns None if the body doesn't look like an MCQ (e.g., it's a
    Mondai-2 sentence-arrangement Q which has 4 options but the format
    is similar enough to parse).
    """
    # Strip leading prose / stems. Find the first numbered choice.
    choice_re = re.compile(r'(?m)^\s*(\d)\.\s*(.+?)\s*$')
    answer_re = re.compile(r'\*\*Answer:\s*(\d)\*\*(?:\s*[-—]\s*(.+))?', re.S)

    choices_iter = list(choice_re.finditer(body))
    if len(choices_iter) < 4:
        return None
    # Use first 4 numbered choices
    choices_iter = choices_iter[:4]
    first_choice_pos = choices_iter[0].start()

    stem = body[:first_choice_pos].strip()
    # Drop trailing prose-italic prefixes like `_Translation:_`
    stem_lines = [ln for ln in stem.split('\n') if not ln.strip().startswith('_')]
    stem = '\n'.join(stem_lines).strip()

    choices = [m.group(2).strip() for m in choices_iter]

    # Find answer line (after the choices)
    after_choices = body[choices_iter[-1].end():]
    am = answer_re.search(after_choices)
    if not am:
        return None
    correct_idx_1based = int(am.group(1))
    if not (1 <= correct_idx_1based <= 4):
        return None
    correct_idx_0based = correct_idx_1based - 1
    rationale = (am.group(2) or '').strip().replace('\n', ' ')
    # Strip trailing markdown/inline-html artifacts in rationale
    rationale = re.sub(r'\s+', ' ', rationale)

    return {
        "type": "mcq",
        "stem_html": stem,
        "choices": choices,
        "correctIndex": correct_idx_0based,
        "rationale": rationale,
    }


# -----------------------------------------------------------------------
# Per-category builders
# -----------------------------------------------------------------------

def parse_mondai3_passages(md: str) -> dict[str, dict]:
    """Bunpou Mondai 3 has passage-grouped questions: each passage carries
    inline `[ 1 ]`..`[ 5 ]` blanks, and each question (Q91..Q100) supplies
    choices for the corresponding numbered blank.

    Returns a map: { question_label: {passage_text, blank_number} } so
    the simple-category parser can stamp those fields onto questions
    that fall inside a Mondai-3 region.

    Returns empty dict if the file has no Mondai 3 section.
    """
    out: dict[str, dict] = {}
    # Find the Mondai 3 section
    m3 = re.search(r'(?ms)^## Mondai 3.*?(?=^## |\Z)', md)
    if not m3:
        return out
    m3_text = m3.group(0)
    # Split into passage blocks: `### Passage <name> (Q<a>-Q<b>)`
    p_re = re.compile(r'(?m)^### (Passage \S+)\s*\(Q(\d+)-Q(\d+)\)\s*$')
    p_matches = list(p_re.finditer(m3_text))
    for i, pm in enumerate(p_matches):
        passage_label = pm.group(1)
        q_start = int(pm.group(2))
        q_end = int(pm.group(3))
        end = p_matches[i + 1].start() if i + 1 < len(p_matches) else len(m3_text)
        body = m3_text[pm.end():end]
        # The passage is in `> ...` blockquotes BEFORE the first `#### Q`
        first_q = re.search(r'(?m)^#### Q\d', body)
        before_qs = body[:first_q.start()] if first_q else body
        # Pull blockquote lines
        passage_lines = []
        for line in before_qs.split('\n'):
            line = line.strip()
            if line.startswith('>'):
                passage_lines.append(line.lstrip('>').strip())
        passage_text = '\n'.join(p for p in passage_lines if p).strip()
        # Map each Q in this passage to its blank number (1-based, inside
        # the passage; blank N corresponds to the Nth Q in the range)
        for offset, q_num in enumerate(range(q_start, q_end + 1), 1):
            label = f'Q{q_num}'
            out[label] = {
                'passage_text': passage_text,
                'passage_label': passage_label,
                'blank_number': offset,
            }
    return out


def build_simple_category(category: str, md_path: Path) -> list[dict]:
    """For moji/goi/bunpou: parse all questions, slice into 15-question
    sequential papers. Returns list of paper dicts.

    For bunpou specifically, also detects Mondai 3 (passage-grouped
    grammar) and stamps passage_text + blank_number on those questions
    so the runtime can render the passage context."""
    md = md_path.read_text(encoding='utf-8')
    blocks = split_questions(md)
    # Mondai-3 metadata (only relevant for bunpou)
    mondai3_map = parse_mondai3_passages(md)
    parsed: list[dict] = []
    for label, body in blocks:
        q = parse_mcq_question(body)
        if q is None:
            print(f"  WARN: {md_path.name} {label} unparseable; skipping",
                  file=sys.stderr)
            continue
        q["kbSourceId"] = label
        # If this Q is part of a Mondai-3 passage, attach passage context
        if label in mondai3_map:
            m3 = mondai3_map[label]
            q['passage_text'] = m3['passage_text']
            q['passage_label'] = m3['passage_label']
            q['blank_number'] = m3['blank_number']
            # The original `body` already had the stem set to a "(blank N)"
            # subtitle. Set stem_html to that so the UI shows which blank
            # the question is for.
            q['stem_html'] = f'→ blank [{m3["blank_number"]}]'
        parsed.append(q)

    papers: list[dict] = []
    for i in range(0, len(parsed), PAPER_SIZE):
        chunk = parsed[i:i + PAPER_SIZE]
        paper_num = (i // PAPER_SIZE) + 1
        paper_id = f"{category}-{paper_num}"
        # ID-stamp questions inside the paper
        for k, q in enumerate(chunk, 1):
            q["id"] = f"{paper_id}.{k}"
        first_label = chunk[0]["kbSourceId"]
        last_label = chunk[-1]["kbSourceId"]
        papers.append({
            "id": paper_id,
            "category": category,
            "paperNumber": paper_num,
            "name": f"{CATEGORY_META[category]['label']} Paper {paper_num}",
            "source_file": f"KnowledgeBank/{md_path.name}",
            "source_question_range": f"{first_label}-{last_label}",
            "questionCount": len(chunk),
            "questions": chunk,
        })
    return papers


def build_dokkai(md_path: Path) -> list[dict]:
    """Dokkai questions are passage-based; preserve passage groupings.

    Strategy: split by `### Passage <N>` headers, collect each passage's
    questions, then group passages until each paper has ~15 questions.
    """
    md = md_path.read_text(encoding='utf-8')
    # Split into passage sections
    passage_re = re.compile(r'(?m)^### (Passage \d+(?:\s+\([^)]*\))?)\s*$')
    pmatches = list(passage_re.finditer(md))
    if not pmatches:
        return []
    passages: list[dict] = []
    for i, m in enumerate(pmatches):
        end = pmatches[i + 1].start() if i + 1 < len(pmatches) else len(md)
        body = md[m.end():end].strip()
        # Stop at next `## ` (mondai break)
        section_break = re.search(r'(?m)^## ', body)
        if section_break:
            body = body[:section_break.start()].strip()
        # Pull passage prose: everything before the first `#### Q`
        first_q = re.search(r'(?m)^#### Q\d', body)
        passage_text = body[:first_q.start()].strip() if first_q else body
        # Pull questions
        q_blocks = split_questions(body)
        parsed_qs = []
        for label, qbody in q_blocks:
            q = parse_mcq_question(qbody)
            if q is None:
                continue
            q["kbSourceId"] = label
            parsed_qs.append(q)
        if not parsed_qs:
            continue
        passages.append({
            "passage_label": m.group(1),
            "passage_text": passage_text,
            "questions": parsed_qs,
        })

    # Group passages so each paper has ~15 questions (whole-passage units)
    papers: list[dict] = []
    current: list[dict] = []
    current_q_count = 0
    paper_num = 1

    def flush_paper():
        nonlocal current, current_q_count, paper_num
        if not current:
            return
        # Flatten passage Qs into the paper's questions array; embed
        # passage_text on each question's group_passage_text field.
        flat_questions: list[dict] = []
        for p in current:
            for q in p["questions"]:
                q["passage_text"] = p["passage_text"]
                q["passage_label"] = p["passage_label"]
                flat_questions.append(q)
        # ID-stamp
        paper_id = f"dokkai-{paper_num}"
        for k, q in enumerate(flat_questions, 1):
            q["id"] = f"{paper_id}.{k}"
        first_label = flat_questions[0]["kbSourceId"]
        last_label = flat_questions[-1]["kbSourceId"]
        papers.append({
            "id": paper_id,
            "category": "dokkai",
            "paperNumber": paper_num,
            "name": f"Dokkai Paper {paper_num}",
            "source_file": f"KnowledgeBank/{md_path.name}",
            "source_question_range": f"{first_label}-{last_label}",
            "questionCount": len(flat_questions),
            "passages": [{
                "label": p["passage_label"],
                "text": p["passage_text"],
                "question_ids": [q["id"] for q in p["questions"]],
            } for p in current],
            "questions": flat_questions,
        })
        current = []
        current_q_count = 0
        paper_num += 1

    for p in passages:
        # If adding this passage would exceed PAPER_SIZE+5 (some
        # tolerance), flush first
        if current_q_count > 0 and current_q_count + len(p["questions"]) > PAPER_SIZE + 3:
            flush_paper()
        current.append(p)
        current_q_count += len(p["questions"])
        if current_q_count >= PAPER_SIZE:
            flush_paper()
    flush_paper()
    return papers


# -----------------------------------------------------------------------
# Manifest
# -----------------------------------------------------------------------

def build_manifest(papers_by_cat: dict[str, list[dict]]) -> dict:
    cats = []
    total_papers = 0
    total_questions = 0
    for cat, papers in papers_by_cat.items():
        cat_q = sum(p["questionCount"] for p in papers)
        cats.append({
            **CATEGORY_META[cat],
            "id": cat,
            "paperCount": len(papers),
            "questionCount": cat_q,
            "papers": [{
                "id": p["id"],
                "paperNumber": p["paperNumber"],
                "name": p["name"],
                "questionCount": p["questionCount"],
                "source_question_range": p["source_question_range"],
            } for p in papers],
        })
        total_papers += len(papers)
        total_questions += cat_q
    return {
        "schema_version": "1.0",
        "totalPapers": total_papers,
        "totalQuestions": total_questions,
        "categories": cats,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    papers_by_cat: dict[str, list[dict]] = {}
    for cat, fname in SOURCES.items():
        path = KB / fname
        if not path.exists():
            print(f"ERROR: {path} missing", file=sys.stderr)
            continue
        if cat == "dokkai":
            papers = build_dokkai(path)
        else:
            papers = build_simple_category(cat, path)
        papers_by_cat[cat] = papers
        # Write per-paper files
        cat_dir = OUT / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        for p in papers:
            (cat_dir / f"paper-{p['paperNumber']}.json").write_text(
                json.dumps(p, ensure_ascii=False, indent=2),
                encoding='utf-8',
            )
        total_q = sum(p["questionCount"] for p in papers)
        print(f"  {cat}: {len(papers)} papers, {total_q} questions")

    manifest = build_manifest(papers_by_cat)
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(f"  manifest.json: {manifest['totalPapers']} papers, "
          f"{manifest['totalQuestions']} questions across "
          f"{len(manifest['categories'])} categories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
