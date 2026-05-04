// Global keyboard shortcuts (Brief 2 §7.2).
//
//   1 / 2 / 3 / 4   - select Nth multiple-choice answer (when visible)
//   space           - flip flashcard / reveal answer
//   enter           - submit / continue (clicks the visible primary button)
//   ?               - open cheatsheet overlay
//   Esc             - close overlay (handled inside the overlay)
//
// Handlers are no-ops when focus is in an input/textarea so typing is unaffected.

let overlay = null;

function isTypingTarget(t) {
  if (!t) return false;
  const tag = t.tagName;
  if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return true;
  if (t.isContentEditable) return true;
  return false;
}

function pickChoice(n) {
  const btns = [...document.querySelectorAll('.choice-button:not([disabled])')];
  const target = btns[n - 1];
  if (target) {
    target.click();
    return true;
  }
  return false;
}

function pressPrimary() {
  // Order of preference: focused button, visible primary, visible Submit/Continue/Next.
  const explicit = document.activeElement?.matches?.('button:not([disabled])') ? document.activeElement : null;
  const candidate = explicit
    || document.querySelector('button.btn-primary:not([disabled])')
    || [...document.querySelectorAll('button:not([disabled])')]
        .find(b => /^(submit|continue|next|start|finish|confirm)/i.test(b.textContent.trim()));
  if (candidate) {
    candidate.click();
    return true;
  }
  return false;
}

function flipOrReveal() {
  // Click any visible "Reveal" / "Show answer" / "Flip" button if present.
  const btn = [...document.querySelectorAll('button:not([disabled])')]
    .find(b => /^(reveal|show answer|flip)/i.test(b.textContent.trim()));
  if (btn) {
    btn.click();
    return true;
  }
  return false;
}

function showCheatsheet() {
  if (overlay) { overlay.hidden = false; return; }
  overlay = document.createElement('div');
  overlay.className = 'shortcuts-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Keyboard shortcuts');
  overlay.innerHTML = `
    <div class="shortcuts-card">
      <button class="shortcuts-close" aria-label="Close">×</button>
      <h3>Keyboard shortcuts</h3>
      <dl class="shortcuts-list">
        <dt><kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd> <kbd>4</kbd></dt>
        <dd>Pick multiple-choice answer</dd>
        <dt><kbd>Space</kbd></dt>
        <dd>Reveal / flip answer (where available)</dd>
        <dt><kbd>Enter</kbd></dt>
        <dd>Submit / Continue / Next</dd>
        <dt><kbd>?</kbd></dt>
        <dd>Open this cheatsheet</dd>
        <dt><kbd>Esc</kbd></dt>
        <dd>Close this overlay</dd>
        <dt><kbd>/</kbd></dt>
        <dd>Focus search (when available)</dd>
      </dl>
    </div>
  `;
  document.body.appendChild(overlay);
  overlay.querySelector('.shortcuts-close').addEventListener('click', hideCheatsheet);
  overlay.addEventListener('click', (e) => { if (e.target === overlay) hideCheatsheet(); });
}

function hideCheatsheet() {
  if (overlay) overlay.hidden = true;
}

export function initShortcuts() {
  document.addEventListener('keydown', (ev) => {
    if (isTypingTarget(ev.target)) return;
    if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
    if (ev.key === '?') {
      ev.preventDefault();
      showCheatsheet();
      return;
    }
    if (ev.key === 'Escape') {
      if (overlay && !overlay.hidden) {
        ev.preventDefault();
        hideCheatsheet();
      }
      return;
    }
    if (overlay && !overlay.hidden) return; // pause other shortcuts while cheatsheet open
    if (['1','2','3','4'].includes(ev.key)) {
      if (pickChoice(parseInt(ev.key, 10))) ev.preventDefault();
      return;
    }
    if (ev.key === ' ') {
      if (flipOrReveal()) ev.preventDefault();
      return;
    }
    if (ev.key === 'Enter') {
      if (pressPrimary()) ev.preventDefault();
      return;
    }
  });
}
