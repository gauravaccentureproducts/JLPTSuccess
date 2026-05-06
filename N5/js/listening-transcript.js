// IMP-070 (audit round-6): listening transcript-aligned playback renderer.
//
// Optional schema extension on listening.json items:
//   lines: [
//     { text_ja: "あの、すみません。", startMs?: 0    },
//     { text_ja: "はい?",              startMs?: 1800 },
//     { text_ja: "トイレは どこですか?", startMs?: 2900 },
//     ...
//   ]
//
// When `lines` is present, the rendered transcript shows each line as a
// separate row. If `startMs` is also present on a line, the row is
// click-to-seek and is auto-highlighted in sync with the audio's current
// time. If `startMs` is absent, the row stays a static text row (no
// seek, no highlight).
//
// When `lines` is absent (current 40/40 items), the caller falls back
// to the single-block `script_ja` rendering. This module is purely
// additive - pre-existing behavior is preserved bit-for-bit.
//
// Authoring of `lines` arrays is out of scope for this PR. The build
// pipeline (tools/build_audio.py) can add an `--align` step in a future
// pass that reads the TTS output's word-timing manifest and emits
// per-sentence startMs offsets. Until then, the field stays absent.

import { renderJa } from './furigana.js';

/** Returns true when the item has a usable transcript-line array. */
export function hasAlignedTranscript(item) {
  return Array.isArray(item?.lines) && item.lines.length > 0;
}

/** Render the transcript-line block. Caller is responsible for placing
 *  the returned HTML inside the listening item's feedback area (the
 *  block where the existing <details><summary>script</summary>...</details>
 *  used to live). */
export function renderTranscriptHTML(item) {
  if (!hasAlignedTranscript(item)) return '';
  const rows = item.lines.map((ln, idx) => {
    const hasSeek = Number.isFinite(ln.startMs);
    const cls = hasSeek
      ? 'transcript-line transcript-line-seekable'
      : 'transcript-line';
    const dataAttr = hasSeek ? `data-start-ms="${ln.startMs}" data-line-idx="${idx}"` : '';
    const txt = ln.text_ja ? renderJa(ln.text_ja) : '';
    return `<div class="${cls}" ${dataAttr}>${txt}</div>`;
  }).join('');
  return `<div class="listening-transcript" data-transcript="1">${rows}</div>`;
}

/** Wire up click-to-seek + synchronised highlighting between the
 *  transcript block and an <audio> element on the page.
 *  No-op if either side is missing. */
export function wireTranscriptSync(container, item) {
  if (!hasAlignedTranscript(item)) return;
  const transcript = container.querySelector('.listening-transcript');
  const audio = container.querySelector('audio');
  if (!transcript || !audio) return;

  // Click on a seekable line => seek the audio to that line's start.
  transcript.addEventListener('click', (e) => {
    const el = e.target.closest('.transcript-line-seekable');
    if (!el) return;
    const ms = Number(el.dataset.startMs);
    if (!Number.isFinite(ms)) return;
    audio.currentTime = ms / 1000;
    if (audio.paused) audio.play().catch(() => { /* autoplay blocked, ignore */ });
  });

  // Build a sorted lookup of [startMs, lineEl] for fast highlight.
  const lineEls = Array.from(
    transcript.querySelectorAll('.transcript-line-seekable')
  );
  const stops = lineEls
    .map(el => ({ ms: Number(el.dataset.startMs), el }))
    .filter(s => Number.isFinite(s.ms))
    .sort((a, b) => a.ms - b.ms);
  if (stops.length === 0) return;

  let activeIdx = -1;
  audio.addEventListener('timeupdate', () => {
    const tMs = audio.currentTime * 1000;
    // Largest stop with ms <= tMs is the active line.
    let idx = -1;
    for (let i = 0; i < stops.length; i++) {
      if (stops[i].ms <= tMs) idx = i; else break;
    }
    if (idx === activeIdx) return;
    if (activeIdx >= 0) stops[activeIdx].el.classList.remove('transcript-line-active');
    if (idx >= 0) stops[idx].el.classList.add('transcript-line-active');
    activeIdx = idx;
  });

  audio.addEventListener('ended', () => {
    if (activeIdx >= 0) stops[activeIdx].el.classList.remove('transcript-line-active');
    activeIdx = -1;
  });
}
