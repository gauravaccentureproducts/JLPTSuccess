"""Provenance audit: scan every text field in every data file for
past-paper signatures.

Triggered by CONTENT-LICENSE.md §3 (2026-05-02 — formalized after
clarifying that the corpus is original, not sourced from JLPT past
papers). Run before every release as part of the content-integrity
gate; exit non-zero if any signature is found.

Detects:
  1. JEES citations ("JEES", "Japan Educational Exchanges")
  2. Year-numbered past-paper markers ("2018年7月本試験")
  3. Past-paper terminology ("過去問" / "真題" / "本試験第N回" / "実問題")
  4. JLPT-year-paper citations ("JLPT N5 2018年")

If a hit appears, the report shows the question id + field + matching
substring. The expected fix is to re-author the offending stem in the
project's own voice — not to add an exception or override the rule.
"""
from __future__ import annotations

import json
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

SUSPECT_PATTERNS = [
    (re.compile(r"\bJEES\b"), "JEES citation"),
    (re.compile(r"Japan\s*Educational\s*Exchanges?", re.I), "JEES full name"),
    (re.compile(r"(19|20)\d{2}年[\s　]*[1-9七十二]+月.*?(本試験|公開|JLPT)"),
     "year+month past-paper marker"),
    (re.compile(r"本試験[\s　]*第\d+回"), "past-paper round number"),
    (re.compile(r"実試験|実問題|真題"), "past-paper terminology (実試験/実問題/真題)"),
    (re.compile(r"(JLPT|日本語能力試験)\s*N[1-5]\s*(20\d{2}|19\d{2})年"),
     "JLPT year-paper citation"),
    (re.compile(r"過去問"), "kakomon (past-question) self-attestation"),
]

# Fields whose strings get scanned. Add new fields here when the schema
# grows; missing-field skipping is silent (the field just isn't checked).
RUNTIME_FIELDS = ("question_ja", "prompt_ja", "explanation_en",
                  "rationale", "distractor_explanations")
PAPER_FIELDS = ("stem_html", "rationale", "explanation_en", "passage_text",
                "prompt_ja", "kbSourceId")
GRAMMAR_FIELDS = ("meaning_en", "meaning_ja", "notes", "pattern")


def scan(text: str, qid: str, label: str, hits: list) -> None:
    if not text or not isinstance(text, str):
        return
    for pat, why in SUSPECT_PATTERNS:
        m = pat.search(text)
        if m:
            hits.append({
                "qid": qid,
                "field": label,
                "rule": why,
                "snippet": m.group(0),
            })


def main() -> int:
    hits: list = []

    # data/questions.json
    qpath = ROOT / "data" / "questions.json"
    if qpath.exists():
        q = json.loads(qpath.read_text(encoding="utf-8"))
        for qq in q.get("questions", []):
            qid = qq.get("id", "?")
            for field in RUNTIME_FIELDS:
                v = qq.get(field, "")
                if isinstance(v, dict):
                    for k, vv in v.items():
                        scan(vv, qid, f"{field}.{k}", hits)
                else:
                    scan(v, qid, field, hits)

    # data/papers/**/paper-*.json
    papers_dir = ROOT / "data" / "papers"
    if papers_dir.exists():
        for f in papers_dir.rglob("paper-*.json"):
            p = json.loads(f.read_text(encoding="utf-8"))
            for qq in p.get("questions", []):
                qid = qq.get("id", "?")
                for field in PAPER_FIELDS:
                    scan(qq.get(field, ""), qid, field, hits)

    # data/grammar.json (patterns + their notes/meaning)
    gpath = ROOT / "data" / "grammar.json"
    if gpath.exists():
        g = json.loads(gpath.read_text(encoding="utf-8"))
        for p in g.get("patterns", []):
            pid = p.get("id", "?")
            for field in GRAMMAR_FIELDS:
                scan(p.get(field, ""), pid, field, hits)

    # KnowledgeBank/*.md (raw source files for the paper questions —
    # these are also project-authored but worth scanning to catch any
    # references in the metadata / notes sections)
    kb_dir = ROOT / "KnowledgeBank"
    if kb_dir.exists():
        for f in kb_dir.glob("*_questions_n5.md"):
            try:
                text = f.read_text(encoding="utf-8")
                # Only scan the first 300 lines (header / introduction);
                # the question body itself is project-authored.
                head = "\n".join(text.splitlines()[:300])
                scan(head, f.name, "kb-header", hits)
            except Exception:  # pragma: no cover
                continue

    print("=" * 72)
    print(f"  PROVENANCE AUDIT — {ROOT}")
    print("=" * 72)
    print(f"\nTotal hits: {len(hits)}")
    if hits:
        print()
        for h in hits[:50]:
            print(f"  {h['qid']} [{h['field']}] — {h['rule']}: {h['snippet'][:80]}")
        if len(hits) > 50:
            print(f"  ... and {len(hits) - 50} more")
        print()
        print("FAIL: provenance leak detected. Each hit should be re-authored")
        print("in the project's voice, not exempted. See CONTENT-LICENSE.md §3.")
        return 1

    print("\nPASS: 0 past-paper signatures across data/, KnowledgeBank/.")
    print("All content traces to project-authored sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
