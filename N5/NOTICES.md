# Third-party content notices

This project bundles content from the following third-party sources. Each is
attributed below per its license.

## KanjiVG

- **What it is:** stroke-order SVG diagrams for the 106 N5-syllabus kanji.
- **Source:** <https://kanjivg.tagaini.net/>
- **Repository:** <https://github.com/KanjiVG/kanjivg>
- **Files:** `svg/kanji/<glyph>.svg` (106 files, one per N5 kanji)
- **License:** Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
- **License text:** <https://creativecommons.org/licenses/by-sa/3.0/>
- **Copyright:** © 2009 - 2011 Ulrich Apel
- **Modifications:** the SVG content is unmodified from upstream; only the file
  names are changed (codepoint-hex `<NNNNN>.svg` → literal-glyph `<漢>.svg`)
  to keep the on-disk filenames learner-readable. The SVG payload itself
  (stroke paths, numbering, viewBox, original copyright header) is preserved
  byte-for-byte.

Per CC BY-SA 3.0:
- You are free to share and adapt this content provided you give appropriate
  credit (which this file does), and any derivative work is distributed under
  the same or a compatible license.
- The KanjiVG SVG files in `svg/kanji/` retain their original CC BY-SA 3.0
  license. The rest of the project is governed by its own LICENSE.

## VOICEVOX (synthesized listening audio)

- **What it is:** Japanese TTS engine + trained voice models used to
  render the 47 listening-drill MP3s under `audio/listening/`.
- **Source:** <https://voicevox.hiroshiba.jp/>
- **Repository:** <https://github.com/VOICEVOX/voicevox_engine>
- **Engine version used at v1.12.50 render:** 0.25.2
- **Speakers used (4):**
  - 四国めたん ノーマル (Shikoku Metan, normal style) — VOICEVOX speaker ID 2
  - 春日部つむぎ ノーマル (Hau Tsumugi, normal style) — VOICEVOX speaker ID 8
  - 白上虎太郎 ふつう (Shirakami Kotaro, futsu style) — VOICEVOX speaker ID 11
  - 青山龍星 ノーマル (Aoyama Ryusei, normal style) — VOICEVOX speaker ID 13
- **License (engine):** LGPL-3.0
- **License (voice models):** each speaker model has its own
  permissive licence — full terms at
  <https://voicevox.hiroshiba.jp/term/>. Summary of the relevant
  clauses for our use:
  - **Free for commercial and non-commercial use** including in this
    open-source app.
  - **Per-speaker credit required.** Each speaker requires that you
    credit the character name when distributing audio output (e.g.,
    "Voice: 四国めたん"). This file satisfies that requirement; the
    in-app `#/notices` viewer also surfaces it for end-users who play
    listening audio.
  - **No defamatory / R-rated / political-misuse contexts.** Every
    listening item in `data/listening.json` is a plain JLPT-N5
    practice prompt — none of those exclusions apply.
  - **Output redistribution permitted** under the same conditions
    (credit + non-misuse).
- **Files:** `audio/listening/*.mp3` (47 files), each rendered with
  one of the 4 speakers above; per-item speaker mapping captured in
  `data/audio_manifest_voice.json` and the per-item
  `audio_render_meta.voices_used` array in `data/listening.json`.
- **Build pipeline:** [`AUDIO.md`](AUDIO.md) +
  `tools/build_listening_audio_multivoice_2026_05_07.py`.

The grammar (631 files) and reading (40 files) MP3s under
`audio/grammar/` and `audio/reading/` are rendered with **gTTS**
(Google Translate TTS, single voice). gTTS attribution is implicit in
its open-source library; no per-file crediting is required by its
licence.

## University of Leeds Japanese Internet Corpus (frequency_rank)

- **What it is:** word-frequency ranks for ~700 of the 1000 vocab
  entries, surfaced as `frequency_rank` + `frequency_rank_source:
  "leeds_corpus_internet_jp"` in `data/vocab.json`.
- **Source:** <http://corpus.leeds.ac.uk/frqc/internet-jp.num>
  (mirrored / cleaned via <https://github.com/hingston/japanese>,
  file `44492-japanese-words-latin-lines-removed.txt`).
- **License:** Creative Commons Attribution 2.5 (CC BY 2.5).
- **License text:** <https://creativecommons.org/licenses/by/2.5/>
- **Attribution:** University of Leeds Centre for Translation
  Studies (Serge Sharoff and contributors); cleanup by William
  Hingston.
- **Modifications:** the rank values are reused as-is. Only words
  matching a vocab `form` or `reading` field were imported; no
  text from the corpus is redistributed.
- **Why a proxy:** the IMP-139 audit asked for BCCWJ ranks; this
  internet-corpus rank is a freely-redistributable proxy. Each
  imported entry is tagged with `frequency_rank_provenance:
  "auto_extracted"` so a future BCCWJ swap can re-tag without
  data migration.

## Question content / corpus

The grammar patterns, vocabulary entries, kanji records, mock-test
questions, reading passages, and listening drills in this repo are
**original content** authored by the project. None of it is copied
from JLPT past papers.

The full provenance policy + reference-source list is in
[`CONTENT-LICENSE.md`](./CONTENT-LICENSE.md). An automated audit
(`tools/audit_provenance.py`, also wired into the JA-30 invariant)
scans every text field on every release and fails the build if any
past-paper signature is found.

The JLPT trademark is owned by the Japan Foundation + JEES; this
project is a learner-built study tool and is not affiliated with
either organization.

---

*Last updated: 2026-05-09 (richness-audit Tier-1 batch 3 — added
University of Leeds JP Internet Corpus attribution for IMP-139
frequency_rank import).*
