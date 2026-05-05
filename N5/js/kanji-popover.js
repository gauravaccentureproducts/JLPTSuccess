// Per-kanji "I know this" popover (Brief 2 §4.2).
// Click any kanji glyph rendered through renderJa() to open a popover with
// readings, meanings, and a "I know this kanji" toggle.
// The "known" flag persists in localStorage and feeds into furigana mode
// 'hide-known', so toggling a kanji to known immediately hides its ruby.
import * as storage from './storage.js';
import { currentLocale } from './i18n.js';

// IMP-047 (audit round-5): same locale-aware fallback as kanji.js.
function localizedMeanings(entry) {
  const lc = currentLocale();
  if (lc && lc !== 'en') {
    const localized = entry[`meanings_${lc}`];
    if (Array.isArray(localized) && localized.length) return localized;
  }
  return entry.meanings || [];
}

let bank = null;
let popoverEl = null;

async function loadBank() {
  if (bank) return bank;
  try {
    const res = await fetch('data/kanji.json');
    const data = await res.json();
    const map = new Map();
    for (const e of data.entries || []) map.set(e.glyph, e);
    bank = map;
  } catch {
    bank = new Map();
  }
  return bank;
}

function ensurePopover() {
  if (popoverEl) return popoverEl;
  popoverEl = document.createElement('div');
  popoverEl.className = 'kanji-popover';
  popoverEl.setAttribute('role', 'dialog');
  popoverEl.setAttribute('aria-modal', 'false');
  popoverEl.hidden = true;
  document.body.appendChild(popoverEl);
  // Dismiss on outside click or Escape
  document.addEventListener('click', (ev) => {
    if (popoverEl.hidden) return;
    if (popoverEl.contains(ev.target)) return;
    if (ev.target.closest('[data-glyph]')) return;
    hidePopover();
  });
  document.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape' && !popoverEl.hidden) {
      hidePopover();
      ev.preventDefault();
    }
  });
  return popoverEl;
}

function hidePopover() {
  if (popoverEl) popoverEl.hidden = true;
}

async function showPopover(glyph, anchor) {
  await loadBank();
  const el = ensurePopover();
  const entry = bank.get(glyph);
  const known = storage.isKanjiKnown(glyph);
  if (!entry) {
    el.innerHTML = `
      <button class="kanji-popover-close" aria-label="Close">×</button>
      <p><strong lang="ja">${esc(glyph)}</strong> is not in the N5 set yet.</p>
    `;
  } else {
    // ISSUE-008 (2026-05-04 audit round 2): surface stroke_count next to
    // the glyph and additional_readings (populated-but-pedagogically-pruned
    // ON/KUN forms — N5 teaches one of them, this entry shows the other
    // for cross-reference). Both fields shipped in v1.12.28's IMP-015.
    const addOn  = entry.additional_readings?.on  || [];
    const addKun = entry.additional_readings?.kun || [];
    const strokeChip = entry.stroke_count
      ? `<span class="kanji-popover-strokes" title="${entry.stroke_count} strokes">${entry.stroke_count}画</span>`
      : '';
    el.innerHTML = `
      <button class="kanji-popover-close" aria-label="Close">×</button>
      <div class="kanji-popover-header">
        <div class="kanji-popover-glyph" lang="ja">${esc(entry.glyph)}</div>
        ${strokeChip}
      </div>
      <dl class="kanji-popover-readings">
        ${entry.on?.length
            ? `<dt>On</dt><dd lang="ja">${entry.on.map(esc).join(' / ')}</dd>`
            : (Array.isArray(entry.on) ? `<dt>On</dt><dd class="muted small">(none at N5)</dd>` : '')}
        ${entry.kun?.length
            ? `<dt>Kun</dt><dd lang="ja">${entry.kun.map(esc).join(' / ')}</dd>`
            : (Array.isArray(entry.kun) ? `<dt>Kun</dt><dd class="muted small">(none at N5)</dd>` : '')}
        ${(() => { const m = localizedMeanings(entry); return m.length ? `<dt>Meaning</dt><dd>${m.map(esc).join(', ')}</dd>` : ''; })()}
      </dl>
      ${(addOn.length || addKun.length) ? `
        <details class="kanji-popover-additional">
          <summary>Other readings (not taught at N5)</summary>
          <dl>
            ${addOn.length  ? `<dt>On</dt><dd lang="ja">${addOn.map(esc).join(' / ')}</dd>`  : ''}
            ${addKun.length ? `<dt>Kun</dt><dd lang="ja">${addKun.map(esc).join(' / ')}</dd>` : ''}
          </dl>
        </details>
      ` : ''}
      <label class="kanji-popover-known">
        <input type="checkbox" data-known-toggle ${known ? 'checked' : ''}>
        <span>I know this kanji</span>
      </label>
      <a class="kanji-popover-link" href="#/kanji/${encodeURIComponent(entry.glyph)}">Open full kanji page →</a>
    `;
  }
  // Position next to anchor, clamped to viewport
  const rect = anchor.getBoundingClientRect();
  el.hidden = false;
  const elRect = el.getBoundingClientRect();
  let top = rect.bottom + 6 + window.scrollY;
  let left = rect.left + window.scrollX;
  if (left + elRect.width > window.scrollX + window.innerWidth - 8) {
    left = window.scrollX + window.innerWidth - elRect.width - 8;
  }
  if (left < window.scrollX + 8) left = window.scrollX + 8;
  el.style.top = `${top}px`;
  el.style.left = `${left}px`;
  el.querySelector('.kanji-popover-close')?.addEventListener('click', hidePopover);
  el.querySelector('[data-known-toggle]')?.addEventListener('change', (e) => {
    storage.setKanjiKnown(glyph, e.target.checked);
    document.dispatchEvent(new CustomEvent('furigana-rerender'));
  });
}

// Click delegation: any [data-glyph] inside the document opens the popover.
export function initKanjiPopover() {
  document.addEventListener('click', (ev) => {
    const target = ev.target.closest('[data-glyph]');
    if (!target) return;
    // Avoid hijacking links inside ruby (e.g. the kanji index)
    if (target.tagName === 'A') return;
    const glyph = target.getAttribute('data-glyph');
    if (!glyph) return;
    ev.preventDefault();
    showPopover(glyph, target);
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
