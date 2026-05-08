// IMP-007 / IMP-010 / IMP-038 (audit round-3): custom audio-player
// helper that wraps any <audio> element on the page with skip-back-5s
// + skip-forward-5s + per-clip playback-rate (0.75x / 1.0x / 1.25x)
// controls. Replaces the bare <audio controls> on listening / reading
// surfaces.
//
// Design constraints:
// - Native <audio controls> stays inside the wrapper as a fallback,
//   but is visually hidden so the custom controls own the surface.
//   This keeps keyboard accessibility (space to play) intact via the
//   underlying element.
// - Each instance is independent - pressing 1.25× on one clip doesn't
//   affect another. The global Settings audio-rate still applies as
//   the *initial* rate; per-clip overrides stick until the page is
//   navigated away.
// - The wrapper is idempotent: calling enhanceAudioPlayers() multiple
//   times on the same DOM is a no-op for already-enhanced nodes
//   (detected via a data-enhanced attribute).

const SKIP_SECONDS = 5;
const SPEEDS = [0.75, 1.0, 1.25];

function controlsHTML(rate) {
  return `
    <div class="audio-skin-controls">
      <button type="button" class="audio-skin-btn audio-skin-back" title="Back 5s" aria-label="Skip back 5 seconds">−5s</button>
      <button type="button" class="audio-skin-btn audio-skin-play" title="Play/pause" aria-label="Play or pause">▶</button>
      <button type="button" class="audio-skin-btn audio-skin-fwd" title="Forward 5s" aria-label="Skip forward 5 seconds">+5s</button>
      <span class="audio-skin-time" aria-live="off">0:00 / 0:00</span>
      <span class="audio-skin-rates" role="group" aria-label="Playback speed">
        ${SPEEDS.map(s => `
          <button type="button" class="audio-skin-rate ${s === rate ? 'active' : ''}" data-rate="${s}" aria-pressed="${s === rate}">${s}×</button>
        `).join('')}
      </span>
    </div>
  `;
}

function fmt(seconds) {
  if (!Number.isFinite(seconds)) return '0:00';
  const m = Math.floor(seconds / 60);
  const s = String(Math.floor(seconds % 60)).padStart(2, '0');
  return `${m}:${s}`;
}

function enhanceOne(audio) {
  if (audio.dataset.enhanced === '1') return;
  audio.dataset.enhanced = '1';

  // Read the current global default rate (Settings).
  let rate = 1.0;
  try {
    const s = JSON.parse(localStorage.getItem('jlpt-n5-tutor:settings') || '{}');
    if (typeof s.audioPlaybackRate === 'number') rate = s.audioPlaybackRate;
  } catch { /* fall through */ }
  audio.playbackRate = rate;

  // Wrap.
  const wrap = document.createElement('div');
  wrap.className = 'audio-skin';
  audio.parentNode.insertBefore(wrap, audio);
  wrap.appendChild(audio);
  audio.classList.add('audio-skin-native');  // CSS hides this
  audio.removeAttribute('controls');         // we're providing our own

  const ctrl = document.createElement('div');
  ctrl.innerHTML = controlsHTML(rate);
  wrap.appendChild(ctrl.firstElementChild);

  const playBtn = wrap.querySelector('.audio-skin-play');
  const backBtn = wrap.querySelector('.audio-skin-back');
  const fwdBtn  = wrap.querySelector('.audio-skin-fwd');
  const timeEl  = wrap.querySelector('.audio-skin-time');
  const rateBtns = wrap.querySelectorAll('.audio-skin-rate');

  // Render time as "0:08 / 0:18 (0.75×)" — the rate suffix lets the
  // learner SEE the rate is applied (some users were unsure whether
  // clicking the rate button actually slowed playback). Suffix is
  // omitted when rate is exactly 1.0 to keep the display compact in
  // the common case.
  const updateTime = () => {
    const r = audio.playbackRate;
    const rateSuffix = Math.abs(r - 1.0) > 0.001 ? ` (${r}×)` : '';
    timeEl.textContent = `${fmt(audio.currentTime)} / ${fmt(audio.duration)}${rateSuffix}`;
  };
  audio.addEventListener('timeupdate', updateTime);
  audio.addEventListener('loadedmetadata', updateTime);
  // Also update on ratechange so the suffix appears immediately after
  // a rate-button click — even if playback hasn't started yet.
  audio.addEventListener('ratechange', updateTime);
  audio.addEventListener('ended', () => { playBtn.textContent = '▶'; });
  audio.addEventListener('play',  () => { playBtn.textContent = '❚❚'; });
  audio.addEventListener('pause', () => { playBtn.textContent = '▶'; });

  playBtn.addEventListener('click', () => {
    if (audio.paused) audio.play(); else audio.pause();
  });
  backBtn.addEventListener('click', () => {
    audio.currentTime = Math.max(0, audio.currentTime - SKIP_SECONDS);
  });
  fwdBtn.addEventListener('click', () => {
    audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + SKIP_SECONDS);
  });
  rateBtns.forEach(b => {
    b.addEventListener('click', () => {
      const r = parseFloat(b.dataset.rate);
      if (!Number.isFinite(r)) return;
      audio.playbackRate = r;
      rateBtns.forEach(x => {
        const isActive = parseFloat(x.dataset.rate) === r;
        x.classList.toggle('active', isActive);
        x.setAttribute('aria-pressed', isActive ? 'true' : 'false');
      });
    });
  });
}

export function enhanceAudioPlayers(root = document) {
  root.querySelectorAll('audio:not([data-enhanced="1"])').forEach(enhanceOne);
}
