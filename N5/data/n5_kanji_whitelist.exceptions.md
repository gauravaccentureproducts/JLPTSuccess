# N5 kanji whitelist - exception register

Each line below documents a kanji that is in the project whitelist
(`n5_kanji_whitelist.json`) but not in the official JLPT N5 kanji scope
(canonically 103 kanji per JLPT.jp). Required for any exception:

- The kanji glyph
- WHY: a one-sentence reason
- REVIEW_DATE: optional date for re-evaluation

The integrity check `JA-25` (Pass-22 F-22.4) enforces this contract:
every kanji in the project whitelist that is not in
`data/n5_official_kanji_scope.json` must have a corresponding line below
with a `WHY:` justification.

This file may be empty during bootstrapping. Once
`data/n5_official_kanji_scope.json` is populated with the canonical 103
kanji, JA-25 begins enforcing accountability for the deltas.

## Exceptions

(none currently documented - JA-25 is in bootstrapping mode until the
official-scope reference file is added at `data/n5_official_kanji_scope.json`)

## Notes

- Spec: `specifications/procedure-manual-appendix-c-pass22-polish.md` §C.4.
- Per-level files: when an N4 / N3 / N2 / N1 build adds its own whitelist,
  it gets its own `n<L>_kanji_whitelist.exceptions.md` following the
  same format.
- Do NOT silence violations by adding kanji here without a WHY. The
  whole point of the WHY-comment is accountability; an undocumented
  addition defeats the invariant.
