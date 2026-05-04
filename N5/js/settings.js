// Settings panel - per spec §3.6 of the developer brief + Brief 2 §5.
// On-device only. Reads/writes via storage adapter.
import * as storage from './storage.js';
import { setLocale, currentLocale, supportedLocales } from './i18n.js';
import { renderJa } from './furigana.js';

const LOCALE_NAMES = {
  en: 'English',
  vi: 'Tiếng Việt',
  id: 'Bahasa Indonesia',
  ne: 'नेपाली',
  zh: '中文',
};

export async function renderSettings(container) {
  const s = storage.getSettings();

  container.innerHTML = `
    <h2>Settings</h2>
    <p class="muted">All settings live on this device. Nothing leaves your browser.</p>

    <section class="settings-section">
      <h3>Display</h3>
      <label class="settings-row">
        <span>UI language</span>
        <select id="set-locale">
          ${supportedLocales.map(lc => `<option value="${lc}" ${currentLocale()===lc?'selected':''}>${LOCALE_NAMES[lc] || lc}</option>`).join('')}
        </select>
      </label>
      <label class="settings-row">
        <span>Theme</span>
        <select id="set-theme">
          <option value="system" ${(s.theme||'system')==='system'?'selected':''}>System</option>
          <option value="light"  ${s.theme==='light'?'selected':''}>Light</option>
          <option value="dark"   ${s.theme==='dark'?'selected':''}>Dark</option>
        </select>
      </label>
      <label class="settings-row">
        <span>Font size</span>
        <select id="set-font">
          <option value="s"  ${s.fontSize==='s'?'selected':''}>S</option>
          <option value="m"  ${(s.fontSize||'m')==='m'?'selected':''}>M (default)</option>
          <option value="l"  ${s.fontSize==='l'?'selected':''}>L</option>
          <option value="xl" ${s.fontSize==='xl'?'selected':''}>XL</option>
        </select>
      </label>
    </section>

    <section class="settings-section">
      <h3>Practice</h3>
      <label class="settings-row">
        <span>Default test length</span>
        <select id="set-test-length">
          ${[20,30,50].map(n => `<option value="${n}" ${s.lastTestLength===n?'selected':''}>${n} questions</option>`).join('')}
        </select>
      </label>
      <label class="settings-row">
        <span>Daily new-card limit</span>
        <input type="number" id="set-daily-new" min="1" max="50" value="${s.dailyNewLimit||10}">
      </label>
      <label class="settings-row">
        <span>Daily review cap</span>
        <input type="number" id="set-daily-review" min="5" max="200" value="${s.dailyReviewCap||50}">
      </label>
      <label class="settings-row">
        <span>Audio playback speed</span>
        <select id="set-audio-rate">
          <option value="0.75" ${s.audioPlaybackRate===0.75?'selected':''}>0.75x</option>
          <option value="1.0"  ${(s.audioPlaybackRate||1.0)===1.0?'selected':''}>1.0x (default)</option>
          <option value="1.25" ${s.audioPlaybackRate===1.25?'selected':''}>1.25x</option>
        </select>
      </label>
      <label class="settings-row">
        <span>Reduce motion</span>
        <select id="set-reduce-motion">
          <option value="auto" ${s.reduceMotion===null||s.reduceMotion===undefined?'selected':''}>Follow system</option>
          <option value="on"   ${s.reduceMotion===true?'selected':''}>Always reduce</option>
          <option value="off"  ${s.reduceMotion===false?'selected':''}>Never reduce</option>
        </select>
      </label>
    </section>

    <section class="settings-section">
      <h3>Data</h3>
      <p class="muted small">Use export to back up your progress (no cloud sync). Import re-applies a saved file.</p>
      <div class="settings-actions">
        <button id="set-export">Export progress</button>
        <button id="set-import-trigger">Import progress…</button>
        <input type="file" id="set-import-file" accept="application/json,.json" hidden>
      </div>
      <p id="set-import-msg" class="muted small" role="status" aria-live="polite"></p>
    </section>

    <section class="settings-danger-zone" aria-labelledby="danger-zone-label">
      <p class="danger-label" id="danger-zone-label">Danger zone</p>
      <div class="settings-row">
        <div>
          <span>Reset all progress</span>
          <p class="setting-help">Clears study history, FSRS schedule, test results, streak, known-kanji flags, and settings. Cannot be undone.</p>
        </div>
        <button id="set-reset" class="btn-danger">Reset…</button>
      </div>
      <div id="reset-confirm" hidden class="reset-confirm-box">
        <p><strong>Type <code>RESET</code> to confirm.</strong> This wipes every byte of your progress on this device.</p>
        <input id="reset-phrase" type="text" autocomplete="off" placeholder="Type RESET">
        <div class="settings-actions">
          <button id="reset-confirm-btn" class="btn-danger" disabled>Confirm reset</button>
          <button id="reset-cancel-btn" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </section>
  `;

  // Saved-toast helper: brief on-screen confirmation that a setting
  // change actually persisted. Settings that have a visible side-effect
  // (theme, font) don't need it because the page literally changes —
  // but settings like "Daily new-card limit" or "Default test length"
  // have no visual feedback otherwise, so a returning user can't tell
  // if their click was accepted. Single shared toast, debounced so
  // rapid changes don't pile up. */
  let savedToastTimer = null;
  const showSavedToast = (label) => {
    let toast = document.getElementById('settings-saved-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'settings-saved-toast';
      toast.className = 'settings-saved-toast';
      toast.setAttribute('role', 'status');
      toast.setAttribute('aria-live', 'polite');
      document.body.appendChild(toast);
    }
    toast.textContent = label ? `Saved: ${label}` : 'Saved';
    toast.classList.add('is-visible');
    if (savedToastTimer) clearTimeout(savedToastTimer);
    savedToastTimer = setTimeout(() => {
      toast.classList.remove('is-visible');
    }, 1800);
  };

  // Wire change handlers
  document.getElementById('set-locale').addEventListener('change', async (e) => {
    await setLocale(e.target.value);
    location.reload();
  });
  // Pass-13: 3-mode furigana radios removed. Auto-furigana feature was
  // producing wrong context-dependent readings (e.g., 大学 = だいがく vs
  // 大[おお]+学[がく]). Native-speaker review concluded the feature should
  // be dropped entirely; in-scope kanji render plain, out-of-scope words
  // are authored in kana. See verification.md Pass 13.
  document.getElementById('set-theme').addEventListener('change', (e) => {
    storage.setSettings({ theme: e.target.value });
    applyTheme();
    // (theme change is instantly visible; no toast needed)
  });
  document.getElementById('set-font').addEventListener('change', (e) => {
    storage.setSettings({ fontSize: e.target.value });
    applyFontSize();
    // (font change is instantly visible; no toast needed)
  });
  document.getElementById('set-test-length').addEventListener('change', (e) => {
    storage.setSettings({ lastTestLength: parseInt(e.target.value, 10) });
    showSavedToast(`Default test length = ${e.target.value} questions`);
  });
  document.getElementById('set-daily-new').addEventListener('change', (e) => {
    storage.setSettings({ dailyNewLimit: parseInt(e.target.value, 10) });
    showSavedToast(`Daily new-card limit = ${e.target.value}`);
  });
  document.getElementById('set-daily-review').addEventListener('change', (e) => {
    storage.setSettings({ dailyReviewCap: parseInt(e.target.value, 10) });
    showSavedToast(`Daily review cap = ${e.target.value}`);
  });
  document.getElementById('set-audio-rate').addEventListener('change', (e) => {
    storage.setSettings({ audioPlaybackRate: parseFloat(e.target.value) });
    applyAudioRate();
    showSavedToast(`Audio playback speed = ${e.target.value}×`);
  });
  document.getElementById('set-reduce-motion').addEventListener('change', (e) => {
    const v = e.target.value;
    const stored = v === 'auto' ? null : v === 'on';
    storage.setSettings({ reduceMotion: stored });
    applyReduceMotion();
    const label = v === 'auto' ? 'Follow system' : v === 'on' ? 'Always reduce' : 'Never reduce';
    showSavedToast(`Reduce motion = ${label}`);
  });

  document.getElementById('set-export').addEventListener('click', () => {
    const payload = storage.exportProgress();
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const filename = `jlpt-n5-progress-${new Date().toISOString().slice(0,10)}.json`;
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    // Visible confirmation: the browser starts a download somewhere out
    // of the user's eye-line. A short status note keeps the user oriented.
    const msg = document.getElementById('set-import-msg');
    if (msg) {
      msg.textContent = `Exported to ${filename} (check your downloads folder).`;
      msg.style.color = 'var(--c-success)';
      setTimeout(() => { if (msg.textContent.startsWith('Exported')) msg.textContent = ''; }, 4000);
    }
  });

  const fileInput = document.getElementById('set-import-file');
  document.getElementById('set-import-trigger').addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', async (e) => {
    const file = e.target.files?.[0];
    const msg = document.getElementById('set-import-msg');
    if (!file) return;
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      const result = storage.importProgress(data);
      msg.textContent = result.message;
      msg.style.color = result.ok ? 'var(--c-success)' : 'var(--c-error)';
      if (result.ok) setTimeout(() => location.reload(), 800);
    } catch (err) {
      msg.textContent = `Import failed: ${err.message}`;
      msg.style.color = 'var(--c-error)';
    }
  });

  // Typed-phrase reset confirm (Brief 2 §5).
  document.getElementById('set-reset').addEventListener('click', () => {
    document.getElementById('reset-confirm').hidden = false;
    document.getElementById('reset-phrase').focus();
  });
  document.getElementById('reset-cancel-btn').addEventListener('click', () => {
    document.getElementById('reset-confirm').hidden = true;
    document.getElementById('reset-phrase').value = '';
    document.getElementById('reset-confirm-btn').disabled = true;
  });
  document.getElementById('reset-phrase').addEventListener('input', (e) => {
    document.getElementById('reset-confirm-btn').disabled = e.target.value.trim() !== 'RESET';
  });
  document.getElementById('reset-confirm-btn').addEventListener('click', () => {
    storage.reset();
    location.hash = '#/learn';
    location.reload();
  });
}

// Theme + font are global side-effects; expose so app.js can apply on boot.
export function applyTheme() {
  const s = storage.getSettings();
  const theme = s.theme || 'system';
  document.documentElement.setAttribute('data-theme', theme);
}
export function applyFontSize() {
  const s = storage.getSettings();
  document.documentElement.setAttribute('data-font', s.fontSize || 'm');
}
// Apply user audio-rate setting to every <audio> on the page (Brief 2 §5).
export function applyAudioRate() {
  const rate = storage.getSettings().audioPlaybackRate || 1.0;
  document.querySelectorAll('audio').forEach(a => { try { a.playbackRate = rate; } catch {} });
}
// Apply reduce-motion override on top of prefers-reduced-motion (Brief 2 §5).
export function applyReduceMotion() {
  const v = storage.getSettings().reduceMotion;
  if (v === true) document.documentElement.setAttribute('data-reduce-motion', 'on');
  else if (v === false) document.documentElement.setAttribute('data-reduce-motion', 'off');
  else document.documentElement.removeAttribute('data-reduce-motion');
}
