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
- **Copyright:** © 2009–2011 Ulrich Apel
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

*Last updated: 2026-05-02*
