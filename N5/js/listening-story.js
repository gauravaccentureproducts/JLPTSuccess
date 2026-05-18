// IMP-WAVE-P4-27 (UI audit fix, 2026-05-12): story-mode listening.
//
// JapanesePod101-parity feature. Groups the 50 listening items by
// ambient_context (station / cafe / shop / home / office / clinic /
// classroom / restaurant) into thematic "stories" the learner can
// auto-play in sequence — like a single immersive listening
// session, not 50 disconnected drills.
//
// Route: #/listeningstory[/<context>]
//   no context:  picker page (pick a story)
//   <context>:   chained player (auto-play next on each completion)
//
// Implementation re-uses the existing audio_slow + audio render
// from listening.json; the rendering is a leaner, narrative-focused
// view (no MC-question scoring; the prompt + script are
// auto-revealed at the end of each clip).

import { renderJa } from './furigana.js';
import { t } from './i18n.js';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c]));

let _itemsCache = null;
async function loadItems() {
  if (_itemsCache) return _itemsCache;
  const r = await fetch('data/listening.json');
  if (!r.ok) return [];
  const data = await r.json();
  _itemsCache = data.items || [];
  return _itemsCache;
}

const CONTEXT_LABEL = {
  station:    { en: 'Station / Transit',  ja: 'えき / 電車' },
  cafe:       { en: 'Cafe',               ja: 'カフェ' },
  restaurant: { en: 'Restaurant',         ja: 'レストラン' },
  shop:       { en: 'Shop',               ja: 'みせ' },
  home:       { en: 'Home',               ja: 'うち' },
  office:     { en: 'Office',             ja: 'かいしゃ' },
  clinic:     { en: 'Clinic',             ja: 'クリニック' },
  classroom:  { en: 'Classroom',          ja: 'きょうしつ' },
  general:    { en: 'Other',              ja: 'その他' },
};

const CONTEXT_ORDER = ['station', 'cafe', 'restaurant', 'shop', 'home', 'office', 'clinic', 'classroom', 'general'];

export async function renderListeningStory(container, params) {
  const items = await loadItems();
  const ctx = (params || '').split('/').filter(Boolean)[0] || '';

  if (!ctx) {
    return renderPicker(container, items);
  }
  return renderChain(container, items, ctx);
}

function renderPicker(container, items) {
  // Group by ambient_context
  const groups = new Map();
  for (const it of items) {
    const c = it.ambient_context || 'general';
    if (!groups.has(c)) groups.set(c, []);
    groups.get(c).push(it);
  }
  const sections = CONTEXT_ORDER
    .filter(c => groups.has(c))
    .map(c => {
      const list = groups.get(c) || [];
      const label = CONTEXT_LABEL[c] || { en: c, ja: c };
      return `
        <a class="listening-story-card" href="#/listeningstory/${esc(c)}">
          <h3>
            <span lang="ja">${esc(label.ja)}</span>
            <span class="muted small"> · ${esc(label.en)}</span>
          </h3>
          <p class="muted small">${list.length} clip(s) — auto-plays in sequence</p>
        </a>
      `;
    })
    .join('');

  container.innerHTML = `
    <article class="listening-story-root">
      <a class="back-link" href="#/listening">← Back to Listening</a>
      <h2>Story-mode listening</h2>
      <p class="page-lede">
        Pick a setting — clips auto-play one after another, like a single immersive listening session. Per-clip prompt + script reveal at the end of each.
      </p>
      <div class="listening-story-grid">${sections}</div>
    </article>
  `;
}

function renderChain(container, items, ctx) {
  const list = items.filter(it => (it.ambient_context || 'general') === ctx);
  if (!list.length) {
    container.innerHTML = `<p>No clips for "${esc(ctx)}". <a href="#/listeningstory">Pick another.</a></p>`;
    return;
  }
  const label = CONTEXT_LABEL[ctx] || { en: ctx, ja: ctx };

  // Build the chained-player markup. Each clip is a collapsible
  // <details> block with the audio player; on `ended` event we
  // advance to the next clip's <audio> and play it.
  const blocks = list.map((it, i) => `
    <details class="listening-story-clip" id="clip-${esc(it.id)}" ${i === 0 ? 'open' : ''} data-clip-index="${i}">
      <summary>
        <strong>${i + 1}.</strong>
        <span lang="ja">${esc(it.title_ja || it.id)}</span>
        <span class="muted small">${esc(it.format_type || '')}</span>
      </summary>
      ${it.audio ? `
        <audio class="listening-story-audio" controls preload="metadata"
               src="${esc(it.audio)}" data-next-index="${i + 1}"></audio>
      ` : ''}
      <details class="listening-story-script muted small">
        <summary>Show script + prompt</summary>
        ${it.prompt_ja ? `<p lang="ja"><strong>Prompt:</strong> ${esc(it.prompt_ja)}</p>` : ''}
        ${it.script_ja ? `<p lang="ja">${esc(it.script_ja).replace(/\n/g, '<br>')}</p>` : ''}
        ${it.correctAnswer ? `<p lang="ja"><strong>Answer:</strong> ${esc(it.correctAnswer)}</p>` : ''}
      </details>
    </details>
  `).join('');

  container.innerHTML = `
    <article class="listening-story-chain">
      <a class="back-link" href="#/listeningstory">← Pick another story</a>
      <h2>
        <span lang="ja">${esc(label.ja)}</span>
        <span class="muted small"> · ${esc(label.en)}</span>
      </h2>
      <p class="page-lede muted small">
        ${list.length} clips. Each auto-plays the next when finished. Expand the script after listening to check your comprehension.
      </p>
      <div class="listening-story-chain-list">${blocks}</div>
    </article>
  `;

  // Wire auto-advance: on `ended`, open the next clip and play.
  const audios = Array.from(container.querySelectorAll('audio.listening-story-audio'));
  audios.forEach((a, i) => {
    a.addEventListener('ended', () => {
      const nextIdx = parseInt(a.dataset.nextIndex || '-1', 10);
      if (nextIdx >= 0 && nextIdx < audios.length) {
        const nextAudio = audios[nextIdx];
        const nextDetails = container.querySelector(`details[data-clip-index="${nextIdx}"]`);
        if (nextDetails) nextDetails.open = true;
        if (nextAudio) {
          // Tiny pause before play to let DOM expand
          setTimeout(() => {
            nextAudio.play().catch(() => { /* autoplay-policy: user gesture required after page load */ });
            nextAudio.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }, 200);
        }
      }
    });
  });
}
