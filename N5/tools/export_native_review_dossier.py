"""Native-review dossier exporter — closes INFRA-4 / INFRA-5 prep.

The Pass-11 native-teacher review still has empty P1-P14 sections in
TASKS.md because the reviewer needs a single self-contained pack: the
content to review, formatted for tracking, with stable IDs to cite back.

This script generates that pack from the live data files. Output:

  feedback/native-review-dossier/
    01_grammar_patterns.md      — all 177 grammar patterns, one per
                                   section, with examples + stem +
                                   meaning_en + notes; ID-cited so
                                   reviewer can write `n5-001: …`
    02_vocab_borderline.md      — vocab entries where the pos field
                                   indicates a borderline category
                                   (verb-3, adverb, expression — high
                                   register/usage variability)
    03_kanji_readings.md        — 106 kanji with on / kun / meanings
                                   for primary-reading verification
    04_reading_passages.md      — all 30 dokkai passages + their
                                   comprehension Qs (Pass-15 rewrites
                                   especially flagged for native eyes)
    05_listening_scripts.md     — 30 listening dialogues with speakers
                                   tagged; verifies natural turn-taking
    cover.md                    — review process, severity rubric,
                                   issue-tracking format
    review_log.csv              — empty template the reviewer fills in
                                   (id, severity, finding, suggested fix)

Run: python tools/export_native_review_dossier.py
Then ship feedback/native-review-dossier/ to the reviewer (.zip preferred).

Idempotent: regenerates everything from current data each run.
"""
from __future__ import annotations

import json
import sys
import io
import csv
from pathlib import Path
from datetime import date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "feedback" / "native-review-dossier"


def _load(name: str) -> dict:
    p = ROOT / "data" / f"{name}.json"
    return json.loads(p.read_text(encoding="utf-8"))


def write_cover():
    today = date.today().isoformat()
    content = f"""# JLPT N5 Tutor — Native-Reviewer Dossier

Generated: {today}
Source revision: see git log on `data/` directory at this commit
Review channel: file findings into `review_log.csv` (template included)

## Purpose

This pack is the single bundle a native-Japanese teacher needs to
audit the live JLPT N5 corpus end-to-end. Every entry has a stable ID
(e.g. `n5-001`, `n5.kanji.人`, `n5.read.001`) — the reviewer cites
that ID in the log; we map the citation back to the source file
without ambiguity.

## Files in this dossier

| File | Scope | Reviewer attention |
|---|---|---|
| `01_grammar_patterns.md` | 177 grammar patterns | Confirm each pattern's *meaning_en* + *notes* match standard N5 textbook framing. Flag any example that sounds unnatural to a native ear. |
| `02_vocab_borderline.md` | ~100 vocab entries with high register / usage variability | Flag entries where the gloss obscures a register split (e.g. casual vs polite vs formal). |
| `03_kanji_readings.md` | 106 kanji | Confirm primary reading (see precedence rule below). Flag any entry where the listed primary is not the most common N5-context reading. |
| `04_reading_passages.md` | 30 dokkai passages + comprehension Qs | Especially Pass-15 rewrites (flagged inline). Naturalness > textbook-strictness for these. |
| `05_listening_scripts.md` | 30 listening dialogues | Speaker-turn naturalness; pacing of greetings; correctness of context (e.g. shop vs office vs school register). |

## Severity rubric (use in `review_log.csv`)

| Severity | Definition |
|---|---|
| CRITICAL | Factually wrong (false claim about Japanese grammar / wrong reading / etc). Must fix before next release. |
| HIGH | Unnatural-but-not-wrong (a native speaker would phrase it differently). Should fix. |
| MEDIUM | Polish / register / nuance. Fix when convenient. |
| LOW | Style preference — e.g. "I'd use 〜じゃ instead of 〜では here." Optional. |

## Issue format

In `review_log.csv`, one row per finding. Required fields:

- `id` — the cited pattern/word/passage/script ID
- `field` — which field has the issue (e.g. `meaning_en`, `examples[2].ja`, `notes`)
- `severity` — CRITICAL / HIGH / MEDIUM / LOW
- `finding` — what's wrong, in 1-2 sentences
- `suggested_fix` — concrete replacement text (ideal) or "discuss" (if it needs a chat)

Optional:

- `reviewer_initials` — for multi-reviewer setups
- `confidence` — 1-5 (5 = certain; 1 = "I'd want to check with a colleague")

## Kanji primary-reading precedence (file 03)

Each kanji record lists `on:` and `kun:` reading lists, and may also
carry an explicit `primary_reading:` field. The runtime surfaces the
primary in this order:

1. If `primary_reading:` is set explicitly, that's the primary
   regardless of which list it came from.
2. Otherwise: if the kanji has any kun readings, the **first kun**
   is primary (the standalone i-adjective / verb-stem form is what
   N5 learners encounter first — see `高い`, `長い`, `安い`, `白い`).
3. Otherwise: the **first on** is primary.

Some kanji are genuinely tied (e.g. `新` — 新聞 しんぶん and 新しい
あたらしい are both N5 contexts). For those, either reading is
acceptable as primary; the listed one is fine unless you have a
strong textbook-aligned reason to swap.

## Empty meaning_ja in file 01

Some grammar patterns have a `meaning_ja:` field that contains only
the pattern itself in 「」 brackets (e.g., `「いつ・どこ まで」` for
`まで`). This is intentional — those patterns are particles or
function words whose meaning is best explained in English at N5
level; a Japanese gloss would be circular. **Skip these as
"deliberately blank"** unless you can supply a learner-friendly
Japanese explanation that adds information beyond the pattern itself.

## Turnaround

Recommended cadence: 2-3 hours per file (5 files = 10-15h total). The
reviewer can return finished `review_log.csv` in batches; the dev
side processes by severity tier.
"""
    (OUT / "cover.md").write_text(content, encoding="utf-8")
    print(f"  wrote cover.md")


def write_grammar():
    g = _load("grammar")
    lines = ["# 01 — Grammar patterns (n5-001 .. n5-187)\n",
             "",
             "Cite as `n5-NNN` in `review_log.csv`. For per-example issues,",
             "use `n5-NNN.examples[K]` where K is the 0-based index.",
             "",
             "---",
             ""]
    for p in g["patterns"]:
        lines.append(f"## {p['id']} — `{p.get('pattern','')}`")
        lines.append("")
        lines.append(f"- **tier:** {p.get('tier','core_n5')}")
        lines.append(f"- **meaning_en:** {p.get('meaning_en','')}")
        if p.get("meaning_ja"):
            lines.append(f"- **meaning_ja:** {p['meaning_ja']}")
        if p.get("notes"):
            lines.append(f"- **notes:** {p['notes']}")
        examples = p.get("examples") or []
        if examples:
            lines.append("- **examples:**")
            for i, ex in enumerate(examples):
                lines.append(f"  - `[{i}]` {ex.get('ja','')}")
                if ex.get("translation_en"):
                    lines.append(f"    > {ex['translation_en']}")
        lines.append("")
    (OUT / "01_grammar_patterns.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote 01_grammar_patterns.md ({len(g['patterns'])} patterns)")


def write_vocab():
    v = _load("vocab")
    BORDERLINE_POS = {"verb-3", "adverb", "expression", "interjection",
                      "conjunction", "particle"}
    items = [e for e in v["entries"] if e.get("pos") in BORDERLINE_POS]
    lines = [
        "# 02 — Vocab (borderline / register-sensitive)",
        "",
        f"Filtered to {len(items)} entries where the part-of-speech tag "
        "(`verb-3` / `adverb` / `expression` / `interjection` / `conjunction` "
        "/ `particle`) suggests register or usage subtlety. Cite as the `id` "
        "field in `review_log.csv`.",
        "",
        "---", ""]
    for e in items:
        lines.append(f"- **`{e['id']}`** — `{e.get('form','')}` ({e.get('reading','')}) "
                     f"[{e.get('pos','')}] — {e.get('gloss','')}")
    (OUT / "02_vocab_borderline.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote 02_vocab_borderline.md ({len(items)} entries)")


def write_kanji():
    k = _load("kanji")
    lines = ["# 03 — Kanji readings (106 entries)",
             "",
             "Cite as the `id` field. The FIRST reading in each `on` / `kun` "
             "list is the runtime primary — flag if a different reading "
             "is more representative for N5 contexts.",
             "",
             "---", ""]
    for e in k["entries"]:
        on = " / ".join(e.get("on") or []) or "—"
        kun = " / ".join(e.get("kun") or []) or "—"
        meanings = ", ".join(e.get("meanings") or [])
        # Primary-reading surface: prefer the explicit `primary_reading`
        # field when set; else fall back to the first-kun rule then
        # first-on (matches the precedence documented in cover.md).
        primary = e.get("primary_reading")
        primary_kind = e.get("primary_kind")
        if not primary:
            if e.get("kun"):
                primary, primary_kind = e["kun"][0], "kun"
            elif e.get("on"):
                primary, primary_kind = e["on"][0], "on"
        lines.append(f"## `{e['id']}` — {e['glyph']}")
        lines.append("")
        lines.append(f"- **on:** {on}")
        lines.append(f"- **kun:** {kun}")
        if primary:
            lines.append(f"- **primary reading:** {primary} ({primary_kind})")
        lines.append(f"- **meanings:** {meanings}")
        if e.get("frequency_rank"):
            lines.append(f"- **freq rank (within N5):** {e['frequency_rank']}")
        lines.append("")
    (OUT / "03_kanji_readings.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote 03_kanji_readings.md ({len(k['entries'])} kanji)")


def write_reading():
    r = _load("reading")
    passages = r.get("passages") or []
    lines = ["# 04 — Reading passages (30 dokkai)",
             "",
             "Cite as `n5.read.NNN`. Per-question issues: `n5.read.NNN.questions[K]`. "
             "Pass-15 rewrites (esp. §1.4, §1.5, §2.1) need fresh native eyes.",
             "",
             "---", ""]
    for p in passages:
        lines.append(f"## `{p['id']}` — {p.get('title_ja','')}")
        lines.append("")
        lines.append(f"- **level:** {p.get('level','')}")
        lines.append(f"- **topic:** {p.get('topic','')}")
        lines.append("")
        lines.append("```")
        lines.append(p.get("ja", ""))
        lines.append("```")
        lines.append("")
        for i, q in enumerate(p.get("questions") or []):
            lines.append(f"- **Q[{i}] (`{q.get('id','?')}`):** {q.get('prompt_ja','')}")
            for c in q.get("choices") or []:
                marker = "✓" if c == q.get("correctAnswer") else " "
                lines.append(f"  - [{marker}] {c}")
        lines.append("")
    (OUT / "04_reading_passages.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote 04_reading_passages.md ({len(passages)} passages)")


def write_listening():
    li = _load("listening")
    items = li.get("items") or []
    lines = ["# 05 — Listening dialogues (30 items)",
             "",
             "Cite as `n5.listen.NNN`. Speaker-turn naturalness, pacing, ",
             "and register fit (e.g. shop / school / office) are the main ",
             "concerns. Per-item: format / setup + dialogue script / ",
             "comprehension question / choices.",
             "",
             "---", ""]
    for it in items:
        lines.append(f"## `{it['id']}` — {it.get('title_ja') or ''}")
        lines.append("")
        lines.append(f"- **format:** {it.get('format','')}")
        # The setup line is the first line of script_ja (the speakers-and-
        # situation context, e.g. "男の人と 女の人が 話しています。…");
        # everything after that is the dialogue itself. We keep them
        # together in one fenced block so the reviewer sees the same
        # rendering the runtime audio is built from.
        script = it.get("script_ja") or it.get("script") or ""
        if script:
            lines.append("- **script (setup + dialogue):**")
            lines.append("")
            lines.append("```")
            lines.append(script)
            lines.append("```")
            lines.append("")
        # The comprehension question is the prompt_ja field.
        prompt = it.get("prompt_ja") or it.get("question_ja") or ""
        if prompt:
            lines.append(f"- **question:** {prompt}")
        for c in it.get("choices") or []:
            marker = "✓" if c == it.get("correctAnswer") else " "
            lines.append(f"  - [{marker}] {c}")
        lines.append("")
    (OUT / "05_listening_scripts.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote 05_listening_scripts.md ({len(items)} items)")


def write_review_log_template():
    log_path = OUT / "review_log.csv"
    with log_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "field", "severity", "finding",
                    "suggested_fix", "reviewer_initials", "confidence"])
        # One example row so the reviewer sees the format
        w.writerow([
            "n5-001",
            "examples[1].ja",
            "MEDIUM",
            "Slight register mismatch — sentence is plain-form but the "
            "context (formal greeting) calls for です/ます.",
            "Replace with: わたしは リーです。",
            "RT",
            "5",
        ])
    print(f"  wrote review_log.csv (1 example row)")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Writing dossier to {OUT}")
    write_cover()
    write_grammar()
    write_vocab()
    write_kanji()
    write_reading()
    write_listening()
    write_review_log_template()
    print("\nDossier complete. Ship the directory (zip preferred) to the reviewer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
