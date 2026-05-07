# Native-speaker recording brief (IMP-094)

> **Author:** the project's resident 日本語教師 persona (round-9 close-out, 2026-05-07).
> **Audience:** the voice actor and recording engineer for a future JLPTSuccess listening-audio swap session.
> **Purpose:** ship a fully-prepared studio packet so a recording session can run without on-the-fly pedagogical decisions.

This brief is the **pre-production deliverable** for IMP-094 (replace
synthetic listening audio with native-speaker recordings). It does not
itself produce audio — it produces the artifact that unblocks a studio
session whenever budget or volunteer talent becomes available.

The Japanese-language version of this brief, intended for the actor
to read directly, is at [`RECORDING-BRIEF.ja.md`](RECORDING-BRIEF.ja.md).

> **2026-05-08 — synthetic-render gotcha now documented.** A user-
> reported "audio breaks every two words" bug on the round-9 VOICEVOX
> render traced to two pipeline issues: (a) JLPT-style bunsetsu
> spaces in `text_ja` were being sent verbatim to VOICEVOX, which
> treats every space as a prosodic boundary and inserts a micro-pause;
> (b) the inter-line silence was 500ms (twice the JLPT-real-exam pace).
> Fixed in `tools/build_listening_audio_multivoice_2026_05_07.py` +
> `tools/build_audio.py` (commit forthcoming). All 47 listening items
> re-rendered. **For human voice actors this gotcha doesn't apply** —
> a native speaker reads JLPT-spaced text with natural prosody. But
> for any future synthetic re-render, the build script must strip
> bunsetsu spaces before calling the engine. See § 9 below.

---

## 1. Voice profile (announcer-neutral, JLPT-fidelity)

The official JLPT listening-section voice is **announcer-neutral
standard Japanese (NHK 標準語 announcer style)**. Specifically:

| Trait | Spec | Notes |
|---|---|---|
| Dialect | Tokyo standard (標準語 / 共通語) | No regional accent (Kansai 関西弁, Tohoku 東北弁, etc.) — those would invalidate the item as a JLPT listening drill. |
| Register | Polite-neutral (です・ます) by default; casual (だ・る) only where the script marks it | Match the register of the script line by line. |
| Tone | Calm, neutral, **no emotional colour**. The exam isn't drama. | Avoid prosody that telegraphs the answer ("happy" tone on a 〜たい sentence, "stressed" tone on a 〜なければなりません, etc.). |
| Speech rate | **180–240 morae/min** (JLPT N5 target band) | Slower than natural conversational Japanese (~300+). Roughly = 1 mora every 250–333 ms. The synthetic VOICEVOX baseline runs `speed_scale=1.30` on Shikoku Metan to land in this band. |
| Pause discipline | Exactly the pauses written in the script. **Do not improvise commas or breath pauses**, especially mid-clause. | Mid-sentence pauses change comprehensibility for N5. The clipped-audio bug we hit on the synthetic baseline was specifically a TTS engine inserting a hard stop at sentence-internal `、`. |
| Mic distance | Consistent — the listener should not be able to tell which speaker is closer to the mic. | At N5 the listener uses speaker-role text cues (男:/女:/先生:/学生:) more than acoustic ones, but inconsistent levels confuse the comprehension task. |

### Pacing reference

A JLPT N5 listening item is typically **120–250 morae** long. At the
target rate that equals **30 seconds to 1 minute 20 seconds** of
audio per item.

| Item type | Typical length | Target audio duration |
|---|---|---|
| Mondai 1 (task-understanding dialogue) | 100–180 morae | 35–60 sec |
| Mondai 2 (point-comprehension dialogue) | 120–200 morae | 40–70 sec |
| Mondai 3 (utterance-expression, single line) | 8–15 morae | 5–10 sec |
| Mondai 4 (immediate-response, single line) | 5–10 morae | 3–6 sec |

If your take is consistently >10 % outside the target band, slow down
or speed up — but **never edit pauses** to fit the target. Use the
sentence-level take, not splice-level edits.

---

## 2. Per-mondai direction

The four JLPT N5 listening formats each have a distinct sound profile.
Match it.

### Mondai 1 — 課題理解 (task understanding)

A short dialogue, typically two speakers, where the listener has to
identify what the speaker should do next, where to meet, what to buy,
etc.

- **Two voices required.** One male, one female unless the script
  explicitly assigns same-gender roles (兄/弟, 母/娘, etc.).
- **Turn-taking pause:** ~250 ms between turns (slightly longer than
  natural — the exam favours clarity over flow).
- **Narrator opening:** the first line is typically the narrator
  setting the scene (`男の人と女の人が話しています…`). Read this in
  third-person announcer voice — flatter than the dialogue lines, no
  character.
- **Question line:** the narrator's closing line (`二人はどこで会いますか`)
  is the comprehension target. Read it **clearly and one-tier slower**
  than the dialogue, with the wh-word (どこ / 何 / いつ / だれ /
  どうして) given a slight prosodic peak.

### Mondai 2 — ポイント理解 (point comprehension)

Same format as Mondai 1 but the question targets a specific reason or
detail (why something happened, what was bought, etc.).

- Same two-voice rule.
- The same narrator opening + question-line discipline applies.
- **Distractor lines** in the dialogue (information that's true but
  not the answer) must not be given prosodic emphasis — emphasis is
  the listener's tell that this is the answer. Keep all factual lines
  in the same neutral register.

### Mondai 3 — 発話表現 (utterance expression)

A one-line situational scene-setter (`～のとき、何と言いますか`)
followed by three short candidate utterances. The listener picks the
most natural utterance for the situation.

- **Narrator only** for the scene-setter — neutral, slightly slower,
  no character.
- **Three candidate utterances** are read by **one** speaker each, in
  the voice and register that matches the scenario (formal stranger
  → polite male / female adult; casual same-age friend → casual; child
  → younger-sounding voice if available).
- **No emotional cue** that telegraphs the right answer. The wrong
  candidates should sound just as plausible in delivery as the right
  one — the test is on the **words**, not the tone.

### Mondai 4 — 即時応答 (immediate response)

A one-line stimulus (a question, greeting, or remark) followed by
three short response candidates.

- **Stimulus line** read by one speaker; **response candidates**
  ideally by a different speaker to make the speaker turn obvious
  even before content. (At N5 the listener may rely on this acoustic
  cue.)
- Response candidates must all sound **equally socially appropriate**
  — again, no emotional tell.
- These items are very short (often 3–5 seconds total). One clean
  take, no splice.

---

## 3. Pronunciation rulings (standardisation)

The N5 corpus contains a number of words with **multiple legitimate
readings**. The actor should follow the rulings in this section so
audio matches the on-screen ruby exactly. Disagreements with the
actor's intuition should be flagged to the project before recording,
not silently overridden.

### 3.1 Numerals + counters (high-frequency)

| Form | Reading | Notes |
|---|---|---|
| 一時 | いちじ | Time. NOT ひととき. |
| 二時 | にじ | |
| 三時 | さんじ | |
| 四時 | **よじ** | NOT しじ. The し reading is avoided for "four" in time. |
| 七時 | **しちじ** | しちじ is canonical; ななじ is heard but JLPT favours しちじ. |
| 九時 | **くじ** | NOT きゅうじ. |
| 一分 | **いっぷん** | Sokuon + handakuten on ふん. |
| 三分 | **さんぷん** | NOT さんふん. |
| 四分 | **よんぷん** | NOT しふん. |
| 六分 | **ろっぷん** | Sokuon. |
| 八分 | **はっぷん** | Sokuon. NOT はちふん. |
| 十分 | **じっぷん** *or* じゅっぷん | じっぷん is NHK standard; じゅっぷん is acceptable. **Pick one and stay consistent across the whole corpus.** Project preference: じゅっぷん (more common in modern speech). |
| 何分 | **なんぷん** | NOT なんふん. |
| 一人 | **ひとり** | NOT いちにん. |
| 二人 | **ふたり** | NOT ににん. |
| 一日 | **ついたち** (date) / **いちにち** (duration) | Context-dependent; the script will mark it. |
| 二日 | **ふつか** (date) / にちにち (rare) | |
| 二十日 | **はつか** | |
| 一本 | **いっぽん** | |
| 三本 | **さんぼん** | |
| 六本 | **ろっぽん** | |
| 一個 | **いっこ** | |
| 一冊 | **いっさつ** | |
| 一枚 | いちまい | No sokuon. |
| 一台 | いちだい | No sokuon. |

### 3.2 Days of the week

| Form | Reading |
|---|---|
| 日曜日 | にちようび |
| 月曜日 | げつようび |
| 火曜日 | かようび |
| 水曜日 | すいようび |
| 木曜日 | もくようび |
| 金曜日 | きんようび |
| 土曜日 | どようび |

### 3.3 Common N5 ambiguous compounds

| Form | Reading | Notes |
|---|---|---|
| 今日 | **きょう** | NOT こんにち. |
| 昨日 | **きのう** | NOT さくじつ. |
| 明日 | **あした** | NOT あす, NOT みょうにち. JLPT N5 standardises on あした. |
| 今朝 | **けさ** | NOT こんちょう. |
| 今晩 | **こんばん** | |
| 一人で | **ひとりで** | |
| 大人 | **おとな** | NOT だいにん. |
| 子供 | **こども** | NOT しきょう. |
| 上手 | **じょうず** | NOT うわて. |
| 下手 | **へた** | NOT したて. |
| 仕事 | **しごと** | |
| 会社 | **かいしゃ** | |
| 私 | **わたし** | NOT わたくし at N5 (too formal). わたくし is N3+. |
| 何 | **なん** before だ/の/と/で counter; **なに** elsewhere | The script ruby will mark it. Trust the ruby. |
| 何人 | **なんにん** | |
| 何時 | **なんじ** | |
| 何曜日 | **なんようび** | |
| 出口 | **でぐち** | NOT しゅっこう. |
| 入口 | **いりぐち** | NOT にゅうこう. |
| 大阪 | **おおさか** | Long お — おおさか, not おさか. |
| 東京 | **とうきょう** | Long お — とうきょう, not ときょう. |
| 京都 | **きょうと** | |
| 北海道 | **ほっかいどう** | Sokuon + long お. |

### 3.4 Pitch-accent rulings (where it disambiguates)

JLPT N5 does **not** test pitch accent directly, but a few high-frequency
homographs disambiguate by pitch. Use the NHK accent dictionary
canonical reading:

| Form | Meaning | Pitch (Tokyo) | Pattern |
|---|---|---|---|
| 雨 | rain | あ↓め | 頭高 (atamadaka) |
| 飴 | candy | あめ↑ | 平板 (heiban) |
| 橋 | bridge | は↑し↓ | 尾高 (odaka) |
| 箸 | chopsticks | は↓し | 頭高 |
| 端 | edge | は↑し | 平板 |
| 紙 | paper | か↑み | 平板 |
| 髪 | hair | か↑み | 平板 (same — context disambiguates) |
| 神 | god | か↓み | 頭高 |
| 今 | now | い↓ま | 頭高 |
| 居間 | living room | い↑ま | 平板 |
| 一 | one | い↓ち | 頭高 |
| 市 | city | し↓ | 頭高 |

The N5 corpus avoids these homographs in confusable contexts, but if
the script puts e.g. 雨 at the start of a sentence, render it
頭高 — drop on the second mora.

### 3.5 Foreign-loan words (katakana)

Loanwords from English have **Japanese** pitch accent + mora pattern,
not English. Do not over-anglicise. Examples in the N5 corpus:

| Form | Reading | Pitch hint |
|---|---|---|
| コーヒー | こ↓ーひー | 頭高 (drop on the long ー) |
| テレビ | て↑れび | 平板 |
| ラジオ | ら↑じお | 平板 |
| カメラ | か↓めら | 頭高 |
| パン | パ↓ン | 頭高 |
| ノート | の↑ーと | 平板 |
| ペン | ペ↑ン | 平板 |
| デパート | で↑ぱーと↓ | 中高 |
| アパート | ア↑ぱーと↓ | 中高 |
| エレベーター | え↑れべーたー↓ | 中高 |
| バス | バ↑ス | 平板 |
| タクシー | タ↑くしー | 平板 |

**Critical:** the long vowel `ー` is a full mora. Honour it. `コーヒー`
is **four** morae (こ・ー・ひ・ー), not two.

---

## 4. Recording session protocol

### Equipment

- **Mic:** large-diaphragm condenser, cardioid pattern. Treated room.
  Pop filter required — sokuon + p/t/k initial bursts on Japanese
  consonants are noticeable.
- **Sample rate:** 44.1 kHz / 16-bit minimum. 48 kHz / 24-bit
  preferred.
- **Format delivered:** mono WAV (raw takes) → studio normalises and
  delivers per-item MP3.

### Per-item delivery format

For each `n5.listen.NNN` ID:

1. **One mono MP3** at 128 kbps CBR, normalised to **−16 LUFS
   integrated**, peaks ≤ −1 dBTP.
2. **Filename** matches the on-disk path the project already uses:
   `audio/listening/n5.listen.NNN.mp3`. This keeps the manifest +
   `<audio src>` references unchanged.
3. **Length-on-disk metadata:** the project's
   `tools/audit_audio_coverage.py` and
   `tools/fix_truncated_audio_2026_05_07.py` audit duration vs script
   morae. A sane delivered take is in the JLPT-N5 target band 180–240
   morae/min. If your take falls outside, the truncation guard will
   flag it.

### Take discipline

- **Read the entire item in one continuous take.** Do not splice line
  by line. The natural rhythm + breath of one take is part of the
  pedagogical signal.
- **Two clean takes per item minimum.** Pick the better one in
  post; keep the alternate.
- **No outtakes / breath edits.** Pre-roll silence ≤ 200 ms. Trail
  silence ≤ 300 ms. Anything beyond that confuses the in-app
  auto-advance logic.
- **Same actor across the entire corpus where possible.** If two
  actors are used (one M, one F), keep the same two for all 47 items.
  Mid-corpus actor changes break the listener's "is this the same
  speaker as last time?" cue.

### Pronunciation flagging

If you read a word and have any doubt about the canonical reading:

1. **Flag it in the take log.** Don't override silently.
2. The JA-teacher reviewer (this brief's author) will rule before
   master delivery.

### Numbering / line-count consistency

For multi-line dialogue items (mondai 1 + 2), the project's
`data/listening.json` ships a `lines[]` array with `startMs`
timestamps for each line. Your delivered audio's actual line
boundaries should match within ±300 ms of those timestamps so the
in-app **transcript-aligned playback** works correctly.

The project will re-run `tools/listening_align_2026_05_07.py` (TBD)
on delivery to re-stamp `startMs` from the actual audio. So mild
drift is fine; gross drift (>1 sec) suggests a missed line or splice.

---

## 5. Sample fully-directed items

The eight items at IDs `n5.listen.001`, `005`, `009`, `041` (one
per mondai) plus `004`, `008`, `028`, `045` (a second per mondai)
have item-specific direction sheets at
**`data/recording_directions.json`**. Use those eight as the
**pilot batch** to calibrate; once all parties agree on those, the
remaining 39 items can use the same conventions without per-item
directions.

> **Why a separate file?** The directions reference Japanese
> technical vocabulary (韻律, 中立, etc.) that is out of N5 scope
> for *learners* but legitimate for *recording engineers*. Keeping
> the directions out of `data/listening.json` means the JA-13
> N5-scope-kanji invariant doesn't reject them, while the
> production-side schema stays clean.

`data/recording_directions.json` structure:

```json
{
  "_meta": { "authored_by": "...", "authored_at": "2026-05-07", ... },
  "directions": {
    "n5.listen.001": {
      "speakers": [
        {"role": "narrator", "voice": "F", "register": "announcer-neutral"},
        {"role": "男",       "voice": "M", "register": "polite-adult"},
        {"role": "女",       "voice": "F", "register": "polite-adult"}
      ],
      "pacing": "180-240 morae/min; ~250ms between turns",
      "prosody_hints": [
        {"line_index": 0, "note": "Narrator scene-set: flatter than dialogue. No character."},
        {"line_index": 4, "note": "Question target. Slight prosodic peak on どこ."}
      ],
      "pronunciation_callouts": [
        {"form": "三時", "reading": "さんじ"},
        {"form": "明日", "reading": "あした"}
      ],
      "do_not": [
        "Do not emphasise えきの前 — that's the distractor; emphasis would telegraph the wrong answer."
      ]
    },
    "n5.listen.004": { ... },
    "n5.listen.005": { ... },
    "n5.listen.008": { ... },
    "n5.listen.009": { ... },
    "n5.listen.028": { ... },
    "n5.listen.041": { ... },
    "n5.listen.045": { ... }
  }
}
```

Direction blocks are **optional**. Items without an entry follow the
brief defaults.

---

## 6. Acceptance criteria

A delivered batch passes acceptance when:

- [ ] Every item's audio length sits within the per-mondai target
      band (§ 1 table).
- [ ] `tools/audit_audio_coverage.py` reports 100 % coverage.
- [ ] `tools/fix_truncated_audio_2026_05_07.py` flags 0 truncations.
- [ ] A native-speaker spot-check (10 % random sample) confirms:
      pronunciation rulings followed, no regional accent slipped in,
      no emotional tells on distractors.
- [ ] `tools/check_content_integrity.py` exits 0 (no JA-15 missing-
      file invariant violations).
- [ ] Each replaced item has `voice: "native"` set in
      `data/audio_manifest.json` and `data/audio_manifest_voice.json`,
      so subsequent re-renders by the synthetic pipeline don't
      clobber the native take.
- [ ] `CACHE_VERSION` bumped in `sw.js` so returning users pull the
      new audio bytes.

---

## 7. Estimated cost (revised, post round-9)

Round-9 closed at synthetic-VOICEVOX-multi-voice baseline. The
priority order in [`NATIVE-AUDIO-WORKFLOW.md`](NATIVE-AUDIO-WORKFLOW.md)
puts **reading passages first, then grammar examples, listening last**.

| Surface | Items | Studio time | Voice talent | Edit | Total estimate |
|---|---|---|---|---|---|
| Reading (40 passages) | 40 × ~30 s | ~1.5–3 hr | USD$150–600 | USD$120–240 | **USD$270–840** |
| Grammar (631 examples) | 631 × ~3 s | ~2–4 hr | USD$200–800 | USD$200–400 | **USD$400–1200** |
| Listening (47 drills) | 47 × ~30 s | ~2–4 hr | USD$200–800 | USD$160–320 | **USD$360–1120** |

**Recommend reading-only as the first batch** — biggest marginal
quality lift relative to current synthetic baseline, smallest budget.

---

## 8. Out of scope for this brief

- Recording vocab (`data/vocab.json`) entries individually. Forvo-
  style word audio is a separate, deferred surface.
- Recording grammar example sentences via the same actor as
  listening. Different domain (read-aloud sentences vs dialogues);
  re-cast if budget permits two actors.
- Re-recording the existing synthetic VOICEVOX listening unless the
  reading batch reveals a comprehension gap that listening shares.

---

## 9. Synthetic-render-only gotcha (engineering note, NOT for actors)

> **This section does NOT apply to human voice actors.** A native
> speaker reads JLPT-spaced text with natural prosody. The notes
> below are for the build pipeline that does synthetic VOICEVOX /
> gTTS / edge-tts rendering — i.e. the audio that ships *until* a
> native-recording session lands.

### The bug

User-reported 2026-05-08: the round-9 synthetic render had audible
"breaks every two words." Two pipeline issues, both fixed in commits
referenced below:

1. **Bunsetsu spaces sent to TTS unmodified.** The `text_ja` /
   `script_ja` / `ja` fields use JLPT-textbook style spacing for
   learner readability:
   ```
   あした、二人は どこで 会いますか。
   ```
   Every Japanese TTS engine — VOICEVOX, gTTS, edge-tts, Azure JA —
   tokenizes on space and inserts a micro-pause at each. Natural
   Japanese has no inter-bunsetsu spaces; the result was choppy
   audio. **Fix:** strip ASCII space + full-width space (U+3000) +
   tab + newline before sending to the engine. Keep `、` / `。` —
   those produce *correct* prosodic pauses.

2. **Inter-line silence was 500ms.** Real JLPT N5 listening tape is
   ~200ms between turns. **Fix:** drop to 200ms; remove trailing
   silence after the very last segment.

### Where the fixes live

- `tools/build_listening_audio_multivoice_2026_05_07.py` →
  `clean_text_for_tts()` helper applied before every render call;
  silence reduced to 200ms.
- `tools/build_audio.py` → `normalize_for_tts()` extended to also
  strip spaces (was digit-conversion only). Affects grammar +
  reading audio render paths.

### What synthesizers handle vs what they don't

| Character | Treatment | Send to TTS? |
|---|---|---|
| `、` (ideographic comma) | Soft prosodic pause — correct for Japanese | YES |
| `。` (ideographic period) | Strong prosodic pause + falling tone — correct | YES |
| ` ` (ASCII space) | Hard pause — WRONG for natural JA | **STRIP** |
| `　` (full-width space U+3000) | Hard pause — WRONG | **STRIP** |
| `\t` / `\n` | Engine-dependent; usually pause | **STRIP** |
| `「`/`」` (quotes) | Some engines pause; OK to leave | (case-by-case) |

### How to verify a re-render is good

```bash
# Re-render listening (requires VOICEVOX engine on :50021):
python tools/build_listening_audio_multivoice_2026_05_07.py --force-rerender

# Re-render grammar + reading (requires gTTS network egress):
python tools/build_audio.py --force

# Both:
python tools/audit_audio_coverage.py        # 100 % coverage
python tools/fix_truncated_audio_2026_05_07.py  # 0 truncations
```

If you change the TTS pipeline in any way, re-render at least one
multi-line listening item (`n5.listen.001` is canonical) and confirm
the audio flows naturally end-to-end before merging. A spaced-text
regression sounds like "robot reading every word separately."

### Why the original brief (sections 1–8) didn't catch this

This brief was written for a future *human* voice-actor session.
Section 1 says "do NOT improvise commas or breath pauses, especially
mid-clause" — that warns the actor. The synthetic engine was never
going to read that document, so the warning didn't apply to it. The
build-pipeline fix in `tools/` is the equivalent guardrail for the
non-human path.

---

*Brief author: project's resident 日本語教師 persona. Reviewed
2026-05-07. § 9 added 2026-05-08 after user-reported choppy-audio
bug fix.*
