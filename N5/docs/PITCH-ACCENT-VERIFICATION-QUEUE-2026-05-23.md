# Pitch-accent native-speaker verification queue

**Built:** 2026-05-23 (commit pending) via
`tools/build_pitch_accent_by_reading_queue_2026_05_23.py`.

**Purpose:** ordered backlog for the broader native-speaker
verification pass when a real human native speaker / certified
Japanese-language teacher is engaged. The 2026-05-23 reviewer
task scaffolded the audit-block schema on 3 canary entries
(あなた / みなさん / きのう); the remaining `by-reading` entries
below form the broader pass.

**Ranking proxy:** vocab.json `section` field leading number
(lower = more foundational; section 1 = Pronouns/Self, the
first thing N5 learners encounter). Inside-section: alphabetical
kana order for determinism.

**Discipline (per F.44.7 / F.44.15 Shape 2 / NATIVE-SPEAKER-
RE-VERIFICATION.md):** This file is a QUEUE, not a verification.
LLM-authored values in `drops` come from kanjium-by-reading
lookup — defensible but not authoritative against NHK 2016.
Each entry needs a real human native-speaker pass before
`match_kind` can be promoted to `exact`.

**Queue size:** 587 entries (excluding the 3 canary
entries already scaffolded in
`n5_pitch_accent_reference.json` `_meta.audit_waves`).

## Top-50 priority entries (section 1-10 vocabulary)

| Rank | Form | Reading | Section | Drops | vocab_id |
|---|---|---|---|---|---|
| 1 | かのじょ | かのじょ | 1. People - Pronouns and Self | [1] | `n5.vocab.1-people-pronouns-and-se.かのじょ` |
| 2 | かれ | かれ | 1. People - Pronouns and Self | [1] | `n5.vocab.1-people-pronouns-and-se.かれ` |
| 3 | じぶん | じぶん | 1. People - Pronouns and Self | [1, 0] | `n5.vocab.1-people-pronouns-and-se.じぶん` |
| 4 | どなた | どなた | 1. People - Pronouns and Self | [1] | `n5.vocab.1-people-pronouns-and-se.どなた` |
| 5 | みんな | みんな | 1. People - Pronouns and Self | [3] | `n5.vocab.1-people-pronouns-and-se.みんな` |
| 6 | あに | あに | 2. People - Family | [1] | `n5.vocab.2-people-family.あに` |
| 7 | あね | あね | 2. People - Family | [0] | `n5.vocab.2-people-family.あね` |
| 8 | いもうと | いもうと | 2. People - Family | [4] | `n5.vocab.2-people-family.いもうと` |
| 9 | おじいさん | おじいさん | 2. People - Family | [2] | `n5.vocab.2-people-family.おじいさん` |
| 10 | おじさん | おじさん | 2. People - Family | [0] | `n5.vocab.2-people-family.おじさん` |
| 11 | おとうと | おとうと | 2. People - Family | [4] | `n5.vocab.2-people-family.おとうと` |
| 12 | おにいさん | おにいさん | 2. People - Family | [2] | `n5.vocab.2-people-family.おにいさん` |
| 13 | おねえさん | おねえさん | 2. People - Family | [2] | `n5.vocab.2-people-family.おねえさん` |
| 14 | おばあさん | おばあさん | 2. People - Family | [2] | `n5.vocab.2-people-family.おばあさん` |
| 15 | おばさん | おばさん | 2. People - Family | [0] | `n5.vocab.2-people-family.おばさん` |
| 16 | かぞく | かぞく | 2. People - Family | [1] | `n5.vocab.2-people-family.かぞく` |
| 17 | きょうだい | きょうだい | 2. People - Family | [0, 1] | `n5.vocab.2-people-family.きょうだい` |
| 18 | そふ | そふ | 2. People - Family | [1] | `n5.vocab.2-people-family.そふ` |
| 19 | そぼ | そぼ | 2. People - Family | [1] | `n5.vocab.2-people-family.そぼ` |
| 20 | りょうしん | りょうしん | 2. People - Family | [1] | `n5.vocab.2-people-family.りょうしん` |
| 21 | いしゃ | いしゃ | 3. People - Roles | [1, 0] | `n5.vocab.3-people-roles.いしゃ` |
| 22 | おまわりさん | おまわりさん | 3. People - Roles | [2] | `n5.vocab.3-people-roles.おまわりさん` |
| 23 | けいかん | けいかん | 3. People - Roles | [0] | `n5.vocab.3-people-roles.けいかん` |
| 24 | せいと | せいと | 3. People - Roles | [1] | `n5.vocab.3-people-roles.せいと` |
| 25 | りゅうがくせい | りゅうがくせい | 3. People - Roles | [3, 4] | `n5.vocab.3-people-roles.りゅうがくせい` |
| 26 | あたま | あたま | 4. Body Parts | [3, 2] | `n5.vocab.4-body-parts.あたま` |
| 27 | おなか | おなか | 4. Body Parts | [0] | `n5.vocab.4-body-parts.おなか` |
| 28 | かお | かお | 4. Body Parts | [0] | `n5.vocab.4-body-parts.かお` |
| 29 | からだ | からだ | 4. Body Parts | [0] | `n5.vocab.4-body-parts.からだ` |
| 30 | くち | くち | 4. Body Parts | [0] | `n5.vocab.4-body-parts.くち` |
| 31 | せ | せ | 4. Body Parts | [0, 1] | `n5.vocab.4-body-parts.せ` |
| 32 | はな | はな | 4. Body Parts | [2, 1, 0] | `n5.vocab.4-body-parts.はな` |
| 33 | みみ | みみ | 4. Body Parts | [2] | `n5.vocab.4-body-parts.みみ` |
| 34 | あそこ | あそこ | 5. Demonstratives | [0] | `n5.vocab.5-demonstratives.あそこ` |
| 35 | あちら | あちら | 5. Demonstratives | [0] | `n5.vocab.5-demonstratives.あちら` |
| 36 | あっち | あっち | 5. Demonstratives | [3] | `n5.vocab.5-demonstratives.あっち` |
| 37 | あれ | あれ | 5. Demonstratives | [0] | `n5.vocab.5-demonstratives.あれ` |
| 38 | こう | こう | 5. Demonstratives | [1, 0] | `n5.vocab.5-demonstratives.こう` |
| 39 | ここ | ここ | 5. Demonstratives | [1, 0] | `n5.vocab.5-demonstratives.ここ` |
| 40 | こちら | こちら | 5. Demonstratives | [0] | `n5.vocab.5-demonstratives.こちら` |
| 41 | こっち | こっち | 5. Demonstratives | [3] | `n5.vocab.5-demonstratives.こっち` |
| 42 | この | この | 5. Demonstratives | [0, 1] | `n5.vocab.5-demonstratives.この` |
| 43 | そう | そう | 5. Demonstratives | [0, 1] | `n5.vocab.5-demonstratives.そう` |
| 44 | そこ | そこ | 5. Demonstratives | [0] | `n5.vocab.5-demonstratives.そこ` |
| 45 | そちら | そちら | 5. Demonstratives | [0] | `n5.vocab.5-demonstratives.そちら` |
| 46 | そっち | そっち | 5. Demonstratives | [3] | `n5.vocab.5-demonstratives.そっち` |
| 47 | その | その | 5. Demonstratives | [1, 0] | `n5.vocab.5-demonstratives.その` |
| 48 | どこ | どこ | 5. Demonstratives | [1] | `n5.vocab.5-demonstratives.どこ` |
| 49 | どちら | どちら | 5. Demonstratives | [1] | `n5.vocab.5-demonstratives.どちら` |
| 50 | どっち | どっち | 5. Demonstratives | [1] | `n5.vocab.5-demonstratives.どっち` |

## Remaining 537 entries (section 11+)

Omitted from this view; see the full machine-readable
output at `docs/PITCH-ACCENT-VERIFICATION-QUEUE-2026-05-23.json`
for the complete sorted queue.

## Verification protocol

Per entry, the human verifier:

1. Looks up the form in NHK 日本語発音アクセント新辞典 (2016).
   Cites page number + drop notation (Maru notation: ⓪ ① ② ③).
2. Locates the form in a listening passage where it occurs
   (search `data/listening.json` `script_ja` for the form
   string). Notes passage_id + approximate timestamp.
3. Confirms whether the audio pitch matches the dictionary
   value. If audio and dictionary disagree:
   - Default to the audio (that's what the learner hears).
   - Note the disagreement explicitly in `decision_note`.
   - Keep the dictionary value as a non-primary alternate in
     `verified_drops`.
4. Fills in the audit block's `result_schema` fields on the
   entry in `n5_pitch_accent_reference.json`.
5. Flips `verifier_pending: false`.
6. If verification is solid, promotes `match_kind` from
   `by-reading` to `exact`.

**Discipline guard rail:** JA-155 catches any entry where
`match_kind: 'exact'` exists without a complete `audit` block
(verifier_pending: false + result_schema populated). This
prevents un-verified promotions from leaking back in.
