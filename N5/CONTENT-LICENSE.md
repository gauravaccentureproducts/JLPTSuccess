# Content provenance + license

> **Plain-English summary:** every grammar pattern, vocabulary entry,
> kanji record, mock-test question, reading passage, and listening
> drill in this repo is **original content** authored by the project
> contributors. None of it is copied from JLPT past papers. The JLPT
> *format* (number-of-questions / Mondai structure / difficulty
> distribution) is referenced as factual context, which is not
> copyrightable. The actual question text is ours.

This file documents the policy formally so the project stays
defensible if ever questioned. Last updated: 2026-05-11
(legal-vetting F-3 close-out — counts refreshed from live data).

---

## 1. What is original

Every byte of the following is original work (counts current as of 2026-05-11):

| File / directory | Item count | Authored by |
|---|---|---|
| `data/grammar.json` (178 patterns) | 178 patterns × ≥4 examples each, all with `meaning_hi` + `explanation_hi` + `l1_notes.hi` | Project authors, with a per-pattern `examples` array hand-written to illustrate the pattern in N5-scope vocabulary |
| `data/questions.json` (290 MCQ + variants) | 290 stems + distractor sets | Project authors, with `tools/add_uncovered_questions*.py` documenting the conventions for adding more |
| `data/papers/*/paper-*.json` (29 papers × 426 paper questions across moji / goi / bunpou / dokkai + chokai virtual paper + full-mock 85-Q × 105-min papers) | 29 papers · 426 questions | Project authors, sourced from internal `KnowledgeBank/*_questions_n5.md` mock files (also authored by project - see provenance audit, §3) |
| `data/reading.json` (54 passages) | 54 short passages + comprehension Qs, all with `summary_hi` + `cultural_context` where Japan-specific | Project authors, with stems written to N5 kanji whitelist + format alignment with JEES sample papers |
| `data/listening.json` (50 drills) | 50 dialogue/monologue scripts + 50 questions, all with `explanation_hi` and multi-voice 男:/女: role tagging for VOICEVOX synthesis | Project authors |
| `data/vocab.json` (1009 entries) | 1009 form/reading/gloss/section/pos rows, all with `gloss_hi`; 134 verbs with `verb_class` + 6 X-6.6 group-1 exception flags; 87 nouns with `counter`; pitch-accent + collocations on high-frequency entries (count reflects post-2026-05-08 structural-dedup pass, was 1041 pre-dedup) | Compiled by project authors from public N5-syllabus references (see §4) |
| `data/kanji.json` (106 entries) | 106 glyphs × on/kun/meanings_hi/radical-breakdown/mnemonics/look-alike clusters/≥3 examples | Compiled from public N5-syllabus + JOYO references; example sentences are original |

## 2. What is third-party (and properly licensed)

Bundled third-party content is documented in [`NOTICES.md`](./NOTICES.md):

- **KanjiVG** stroke-order SVGs (`svg/kanji/<glyph>.svg`, 106 files) —
  CC BY-SA 3.0, attributed.
- **VOICEVOX** synthesized audio (3 surfaces, 2141 files total):
  - Grammar: `audio/grammar/n5-NNN.M.mp3` (1782 files) — speaker 8
    (春日部つむぎ).
  - Listening: `audio/listening/n5.listen.NNN.mp3` + `.slow.mp3`
    (50 + 50 = 100 files) — 6 distinct speakers (8 / 11 / 2 / 3 / 10 / 13:
    春日部つむぎ / 玄野武宏 / 四国めたん / ずんだもん / 雨晴はう / 青山龍星)
    cycled across items for age × gender variety.
  - Kanji per-yomi: `audio/kanji/<glyph>-{on|kun}-<reading>.mp3`
    (259 files: 136 on + 123 kun) — speaker 8 (春日部つむぎ).
  VOICEVOX engine LGPL-3.0; each character permits commercial +
  non-commercial use with attribution per https://voicevox.hiroshiba.jp/term/
  and the canonical per-character term sheets (see NOTICES.md).
- **Microsoft Edge TTS** — no longer shipped. Listening audio was
  edge-TTS rendered between v1.13.x and v1.14.0; flipped to VOICEVOX
  in v1.14.1. Historical edge-TTS renders preserved in
  `audio/_backup_edge_tts_listening_2026_05_12/` (untracked / gitignored).
- **gTTS** synthesized audio (`audio/reading/*.mp3`, 54 files) —
  Google Translate TTS via the open-source `gtts` Python library;
  no per-file crediting required by its licence.

That's the entire third-party surface. Everything else under `data/`
and `KnowledgeBank/` is original.

## 3. Provenance audit (automated)

`tools/audit_provenance.py` scans every text field in every data file
for past-paper signatures: JEES citations, year-numbered question
markers (`2018年7月本試験` etc.), past-paper terminology (`過去問` /
`真題` / `本試験第N回`), and full-name JEES references. Last run
2026-05-07 (round-9 close-out): **0 hits across 716 audited questions**
(290 question-bank + 426 paper-bound).

The intent: if a contributor ever paraphrases too closely from a real
past paper, the audit catches it before commit.

## 4. References used (and not copied from)

The following public-information sources were used **as references for
distribution / topic / vocabulary scope** - never for question text:

| Source | What we took | What we did NOT take |
|---|---|---|
| **JEES official sample papers** (jlpt.jp) | The Mondai structure (1 - 7), the rough question-count distribution per Mondai, the difficulty range | Any specific question text, distractor set, or passage |
| **JLPT N5 official syllabus** (published by JEES) | The kanji list (106 chars), the vocabulary scope (~800 core entries; we expanded to 1009 with related N5 vocabulary), the grammar inventory (~150 patterns; we cover 178 with related forms) | Anything that would constitute the "exam itself" |
| **Tofugu / WaniKani / Imabi / Bunpro / JLPTsensei / Tae Kim** | Pattern explanations, common-mistake lists, register notes - used as cross-references when authoring our own `meaning_en` / `notes` fields | Any verbatim text |
| **KANJIDIC2 + JMdict** | On / kun reading lists per kanji, frequency rank | We re-derived our own primary-reading flags + example sentences |
| **JLPT past-paper *analysis* (third-party books, learner blogs)** | Question-distribution facts, common topics in dokkai (school / shopping / family / weather), characteristic phrasings of Mondai instructions | The actual past-paper questions themselves |

**The principle:** facts about the JLPT exam (how many questions of
what type) are not copyrighted. The specific *expressions* of those
questions are. We keep the former and write the latter ourselves.

## 5. The mock-test format

The MCQ paper structure (Mondai 1 文の文法1 60-question section,
Mondai 2 並べ替え 30-question section, Mondai 3 passage-based
10-question section, etc.) follows the **standard JLPT N5 format**.
This is a fact about the test, documented in dozens of learner books
and on jlpt.jp. The format itself is not copyrightable - only specific
question text is. Our paper structure mirrors the official one
deliberately so the student's practice transfers to the real exam.

## 6. What this project does NOT do

- **No verbatim past-paper text.** Not in any data file, KnowledgeBank
  source file, or example.
- **No translated past-paper text.** Translation is a derivative
  work; even an English version of a Japanese past-paper question
  would be infringement.
- **No "JLPT 真題" / "JLPT 過去問" content** under those labels or
  any other.
- **No claim of authority.** This is a learner-built study tool,
  not an official JLPT preparation product. The JLPT trademark is
  owned by the Japan Foundation + JEES.

## 7. If JEES ever wants to talk to us

We're open to it. If you represent JEES or the Japan Foundation and
have a concern about anything in this repo, please contact the
project owner (see `README.md`) - we'll respond within 7 days. The
provenance audit should support any specific question; if there's a
specific stem that closely resembles a past paper despite §3 above,
we'll rewrite it.

The reverse is also true: if you'd like to **license** specific past-
paper material to us under an explicit grant (e.g. for a future
"compare your score against actual past papers" feature), we'd be
happy to discuss.

## 8. License of original content

The repository's overall license is in `LICENSE`. The content (data
files, question text, examples, explanations) is governed by that
license. Any reuse - including by AI training pipelines, commercial
JLPT-prep products, or other open-source projects - is subject to
the same terms.

## 9. Provenance honesty

The `review_status: native_reviewed` flag that appears on individual
fields in `data/grammar.json`, `data/vocab.json`, `data/kanji.json`,
`data/listening.json`, `data/reading.json`, and `data/papers/*.json`
reflects a review pass conducted on 2026-05-07 by Claude (Anthropic's
LLM) acting in a native-reviewer persona, per explicit user directive.
The user authorized this reviewer-role assignment in lieu of recruiting
a native Hindi-speaking Japanese teacher. The same disclosure is
carried verbatim in each of those files at
`_meta.native_review_pass_2026_05_07`, and in the papers manifest at
`data/papers/manifest.json#_meta.native_review_pass_2026_05_07`.

For institutional adopters or users who require strict
native-human-reviewed content, a future native-human-reviewer pass
remains queued. That pass would reopen the project's IMP-101 item and
re-stamp the `review_status` field on each reviewed entry; until then,
treat `native_reviewed` as "AI-reviewed by Claude in native-reviewer
persona."

This section discloses what the field means today; it does not
deprecate the flag. Removing or weakening the flag without this
disclosure would itself be a misrepresentation - so the two are
coupled and travel together.

---

*This file is reviewed at every release. The audit
(`tools/audit_provenance.py`) runs as part of the content-integrity
gate (CI). If you spot a provenance issue, file an issue with the
specific question ID and we'll fix it within the next release.*
