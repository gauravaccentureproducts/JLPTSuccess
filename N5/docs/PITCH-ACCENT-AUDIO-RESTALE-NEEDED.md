# Pitch-Accent Audio Re-Stale Manifest — 2026-05-15

The 2026-05-15 pitch-accent reconciliation (commits 08f6907 +
round-2) updated `pitch_accent.drop` on the following vocab
entries. The corresponding audio files in `audio/vocab/` were
rendered BEFORE the data update, so they may encode the OLD
drop position. A re-render is recommended for auditory fidelity.

## How to re-render

1. Start the VOICEVOX engine (see procedure manual §D.1.2)
2. For each entry below, regenerate the audio:
   ```
   python tools/render_vocab_audio.py --vocab-id <id>
   ```
3. Verify the new audio matches the updated drop position
4. Update audio_manifest.json with the new file hash
5. Once re-rendered, delete this file or move to not-required/

## Entries needing re-render (0)

**No vocab entries have per-entry audio files in this project.** The
audio pipeline at N5 currently renders only grammar examples, listening
scripts, reading passages, and kanji yomi — NOT individual vocab
entries. So the 50 pitch-accent drop fixes have **no rendered-audio
counterpart** that could go stale.

If a future vocab-level audio renderer is added (e.g., per-entry TTS
for pronunciation drill mode), the `confidence: 'high'` + `source:
'kanjium-...'` entries can be queued for fresh rendering using the
updated drop positions.

## Caveats

- VOICEVOX may have rendered with its OWN accent dictionary
  rather than respecting our `pitch_accent.drop` field. If
  so, the rendered audio could be CORRECT (VOICEVOX's accent)
  while disagreeing with the OLD authored drop. Verify per-
  entry before re-rendering.
- Entries without an `audio` field are skipped (no MP3 to
  refresh).

