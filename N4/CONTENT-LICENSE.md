# Content License + Source Authorities

## Code license

MIT.

## Content license

All grammar examples, vocabulary entries, kanji example words, reading passages, listening scripts, and mock-test questions in this repo are **original content** authored by the project maintainers. They are CC-BY 4.0 licensed: you may reuse with attribution.

## Source authorities (used for triangulation, NOT verbatim copy)

| Source | URL | Use |
|---|---|---|
| JLPT Sensei N4 | https://jlptsensei.com/jlpt-n4-{kanji,vocab,grammar}-list/ | Inventory list |
| Tanos N4 | https://www.tanos.co.uk/jlpt/jlpt4/{kanji,vocab,grammar}/ | Cross-reference frequency |
| Bunpro N4 | https://bunpro.jp/jlpt/n4 | Pattern catalogue + register notes |
| JLPT.jp samples | https://www.jlpt.jp/e/samples/n4/index.html | Format / topic reference |
| Genki II / Minna no Nihongo II | (textbooks) | Pedagogy + chapter ordering |

## Past-paper policy

- We do **not** copy past-paper questions verbatim. Past-paper formats and difficulty distributions inform our authoring, but every question text is original.
- `tools/audit_provenance.py` runs at CI time and fails the build if known JEES sample phrasings are detected.
- If a future use case requires licensed past-paper material (e.g., a "compare your score against actual JLPT past papers" feature), see `<JLPT-root>/jees-inquiry-template.md` for the formal-permission email template.

## Kanji stroke order SVGs

Stroke-order SVGs in `svg/kanji/` are derived from the [KanjiVG](https://kanjivg.tagaini.net) project (Creative Commons BY-SA 3.0, by Ulrich Apel). KanjiVG attribution preserved in `NOTICES.md`.

## Fonts

- **Inter** (Google Fonts, OFL): `fonts/inter-{300,400,500}.woff2`.
- **Noto Sans JP** (Google Fonts, OFL): `fonts/noto-sans-jp-400.woff2`. Subset to N5 ∪ N4 = 280 kanji.

## Audio

- v1: synthetic TTS via [gTTS](https://gtts.readthedocs.io) (Apache 2.0). Each item flagged `voice: "synthetic"`.
- v2 (planned): native-recorded audio. Each item flagged `voice: "native"`.

## Reuse

Free for any educational, commercial, or derivative use under the terms above. Attribution: `JLPT N4 Tutor` + link to the project repo.
