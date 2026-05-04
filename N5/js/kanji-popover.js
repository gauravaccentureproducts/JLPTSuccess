// Per-kanji "I know this" popover (Brief 2 §4.2).
// Click any kanji glyph rendered through renderJa() to open a popover with
// readings, meanings, and a "I know this kanji" toggle.
// The "known" flag persists in localStorage and feeds into furigana mode
// 'hide-known', so toggling a kanji to known immediately hides its ruby.
import * as storage from './storage.js';

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
    el.innerHTML = `
      <button class="kanji-popover-close" aria-label="Close">×</button>
      <div class="kanji-popover-glyph" lang="ja">${esc(entry.glyph)}</div>
      <dl class="kanji-popover-readings">
        ${entry.on?.length ? `<dt>On</dt><dd lang="ja">${entry.on.map(esc).join(' / ')}</dd>` : ''}
        ${entry.kun?.length ? `<dt>Kun</dt><dd lang="ja">${entry.kun.map(esc).join(' / ')}</dd>` : ''}
        ${entry.meanings?.length ? `<dt>Meaning</dt><dd>${entry.meanings.map(esc).join(', ')}</dd>` : ''}
      </dl>
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
