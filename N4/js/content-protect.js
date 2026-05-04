// Content-protection layer (2026-05-02).
//
// IMPORTANT — what this is and isn't:
//   - This module raises FRICTION against casual copying / sharing of
//     question content. It is NOT security. The site is a static PWA;
//     anyone with browser devtools can extract `data/*.json` directly.
//     A motivated user with screen-recording software, a phone camera,
//     or a screen reader can capture content regardless of these
//     handlers. There is no W3C API to truly block screenshots.
//
//   - What it stops cleanly:
//       * accidental Ctrl+C / Ctrl+A / Ctrl+S / Ctrl+P
//       * right-click context menu
//       * text selection on body content
//       * F12 / Ctrl+Shift+I / Ctrl+U opening devtools (best effort)
//       * dragging images / kanji glyphs out of the page
//       * print to PDF (CSS print rule blanks the page)
//
//   - What it deters but cannot prevent:
//       * Win+Shift+S / Cmd+Shift+4 region screenshots (we blur on
//         window blur, but the OS often takes the screenshot before
//         the blur event fires)
//       * Browser menu → Save / Print
//       * view-source: prefix on the URL
//       * Mobile screenshot (no API exists)
//
// Usage: imported and initialized once from js/app.js.
//
// FEATURE FLAG (2026-05-02): the content-protection layer is currently
// MASKED — initContentProtection() is a no-op and the CSS rules below
// are scoped to `html[data-protect="on"]` (which is never set when the
// flag is off). Reason: the user needs to take screenshots / copy text
// to file bug reports against the site, and the layer was blocking that.
// To re-enable the full layer (right-click block, copy/cut block,
// devtools-shortcut block, screenshot blur, print-page blank, body
// user-select:none, etc.) flip CONTENT_PROTECT_ENABLED back to true.
// No other change required — JS init re-attaches handlers AND sets the
// `data-protect="on"` attribute on <html>, which activates the gated
// CSS rules at css/main.css §3478.
const CONTENT_PROTECT_ENABLED = false;

const ALLOW_SELECT_TAGS = new Set(['INPUT', 'TEXTAREA']);
const ALLOW_SELECT_CLASS = 'allow-select';

function isAllowedTarget(el) {
  if (!el) return false;
  if (ALLOW_SELECT_TAGS.has(el.tagName)) return true;
  if (el.isContentEditable) return true;
  // Allow if the element or any ancestor opts in via class
  if (el.closest && el.closest('.' + ALLOW_SELECT_CLASS)) return true;
  return false;
}

function blockEvent(e) {
  if (isAllowedTarget(e.target)) return;
  e.preventDefault();
  e.stopPropagation();
  return false;
}

export function initContentProtection() {
  if (!CONTENT_PROTECT_ENABLED) {
    // Masked. Make doubly sure the CSS rules don't apply by clearing
    // the gate attribute (no-op if it was never set, but defensive).
    document.documentElement.removeAttribute('data-protect');
    return;
  }
  // Activate the gated CSS rules.
  document.documentElement.setAttribute('data-protect', 'on');

  // 1. Right-click context menu
  document.addEventListener('contextmenu', blockEvent, { capture: true });

  // 2. Copy / cut / paste (paste is fine on inputs but we redirect)
  document.addEventListener('copy', blockEvent, { capture: true });
  document.addEventListener('cut', blockEvent, { capture: true });

  // 3. Drag start (block image/text drag)
  document.addEventListener('dragstart', blockEvent, { capture: true });
  document.addEventListener('drop', blockEvent, { capture: true });

  // 4. Selection start
  document.addEventListener('selectstart', (e) => {
    if (isAllowedTarget(e.target)) return;
    e.preventDefault();
  }, { capture: true });

  // 5. Keyboard shortcuts. Note: modern browsers ignore preventDefault
  // on Ctrl+S, Ctrl+P, F12 in most cases. We try anyway; the menu-bar
  // alternative still exists.
  document.addEventListener('keydown', (e) => {
    const k = (e.key || '').toLowerCase();
    const ctrl = e.ctrlKey || e.metaKey;
    if (isAllowedTarget(e.target)) {
      // Allow normal typing in inputs; only block global shortcuts
      if (ctrl && (k === 's' || k === 'p')) {
        e.preventDefault();
      }
      return;
    }
    // Block Ctrl+A/C/X/S/P globally on non-input targets
    if (ctrl && (k === 'a' || k === 'c' || k === 'x' || k === 's' || k === 'p' || k === 'u')) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
    // F12 / Ctrl+Shift+I / Ctrl+Shift+J / Ctrl+Shift+C — devtools
    if (e.key === 'F12') {
      e.preventDefault();
      return false;
    }
    if (ctrl && e.shiftKey && (k === 'i' || k === 'j' || k === 'c' || k === 'k')) {
      e.preventDefault();
      return false;
    }
    // PrtScn — most OSes don't deliver this to the browser, but try.
    if (k === 'printscreen') {
      e.preventDefault();
      blurPage();
      setTimeout(unblurPage, 500);
    }
  }, { capture: true });

  // 6. Screenshot deterrent via window blur. When focus leaves the
  // tab/window — which happens for Cmd+Shift+4 / Win+Shift+S region
  // selectors and OS-level screenshot tools — obscure the body via
  // CSS [data-blur] toggle on <html>.
  window.addEventListener('blur', blurPage);
  window.addEventListener('focus', unblurPage);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) blurPage();
    else unblurPage();
  });

  // 7. Catch programmatic clipboard writes (drag-to-OS, etc.).
  // We can't truly block navigator.clipboard.writeText, but on most
  // pages the content is read via getSelection() — we override that.
  try {
    const origGetSelection = window.getSelection;
    window.getSelection = function () {
      const sel = origGetSelection.call(this);
      // If the active focus is on an input/textarea, return the real
      // selection (user is typing); otherwise return an empty-string
      // wrapper so any read attempt yields nothing.
      const active = document.activeElement;
      if (active && isAllowedTarget(active)) return sel;
      return {
        toString: () => '',
        rangeCount: 0,
        anchorNode: null,
        focusNode: null,
        removeAllRanges: () => {},
      };
    };
  } catch { /* getSelection not overridable; not fatal */ }
}

function blurPage() {
  document.documentElement.setAttribute('data-blur', 'true');
}
function unblurPage() {
  document.documentElement.removeAttribute('data-blur');
}
