// Listening module shell (Brief §3.1)
// Three JLPT N5 listening formats: 課題理解 / ポイント理解 / 発話表現.
// Audio assets ship via the build-time TTS pipeline (tools/build_audio.py).
// When MP3s are absent, the module degrades gracefully: shows the script
// text + plays nothing, with a clear "audio not yet generated" notice.
import { renderJa } from './furigana.js';
import * as storage from './storage.js';

let bank = null;
let session = null;

// 課題理解 / ポイント理解 / 発話表現 are official JLPT format names; the
// kanji 課 解 達 表 現 are not in the N5 catalog, but these labels are
// authentic JLPT taxonomy and the kana gloss is shown alongside.
const FORMATS = {
  task:      'かだいりかい (タスクりかい)',
  point:     'ポイントりかい',
  utterance: 'はつわひょうげん',
};

async function loadBank() {
  if (bank) return bank;
  try {
    const res = await fetch('data/listening.json');
    if (!res.ok) {
      bank = { items: [] };
      return bank;
    }
    bank = await res.json();
  } catch {
    bank = { items: [] };
  }
  return bank;
}

export async function renderListening(container) {
  await loadBank();
  if (session) return renderItem(container);
  return renderIndex(container);
}

function renderIndex(container) {
  const items = bank.items || [];
  if (items.length === 0) {
    container.innerHTML = `
      <h2>${renderJa('ちょうかい れんしゅう')}</h2>
      <div class="placeholder">
        <p><strong>No listening items shipped yet.</strong></p>
        <p>The listening module is wired and will activate as soon as audio assets ship.</p>
        <p class="muted small">For developers: run <code>python tools/build_audio.py</code> to generate MP3 files for every reading passage and listening script. Audio files land in <code>audio/listening/*.mp3</code> and <code>audio/reading/*.mp3</code>; the service worker will cache them on first online visit.</p>
        <p class="muted small">Listening scripts and questions live in <code>data/listening.json</code> (created by the same build).</p>
      </div>
    `;
    return;
  }
  const byFormat = items.reduce((acc, x) => {
    (acc[x.format] = acc[x.format] || []).push(x);
    return acc;
  }, {});
  container.innerHTML = `
    <h2>${renderJa('ちょうかい れんしゅう')}</h2>
    <p>${renderJa('JLPT N5 ちょうかいの 三つの けいしき。おんせいを 聞いて、ただしい こたえを えらんで ください。')}</p>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">${renderJa('ぜんぶ ひらく')}</button>
      <button type="button" class="btn-secondary toc-collapse-all">${renderJa('ぜんぶ とじる')}</button>
    </div>
    ${Object.entries(byFormat).map(([fmt, list]) => `
      <details class="listening-section">
        <summary><h3>${renderJa(FORMATS[fmt] || fmt)} <span class="muted small">(${list.length})</span></h3></summary>
        <ul class="listening-list">
          ${list.map(it => `<li><button class="listening-pick" data-id="${esc(it.id)}">${it.title_ja ? renderJa(it.title_ja) : esc(it.id)}</button></li>`).join('')}
        </ul>
      </details>
    `).join('')}
  `;
  // Wire Expand-all / Collapse-all
  const expandBtn = container.querySelector('.toc-expand-all');
  const collapseBtn = container.querySelector('.toc-collapse-all');
  if (expandBtn) expandBtn.addEventListener('click', () => {
    container.querySelectorAll('details.listening-section').forEach(d => d.open = true);
  });
  if (collapseBtn) collapseBtn.addEventListener('click', () => {
    container.querySelectorAll('details.listening-section').forEach(d => d.open = false);
  });
  container.querySelectorAll('[data-id]').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = items.find(x => x.id === btn.dataset.id);
      session = { item, picked: null };
      renderItem(container);
    });
  });
}

function renderItem(container) {
  const it = session.item;
  const picked = session.picked;
  const feedback = picked != null;
  const correct = picked === it.correctAnswer;
  // Mark as completed the first time the user submits any answer (right
  // or wrong — listening counts toward syllabus progress on engagement,
  // not just correctness, since the audio comprehension is the practice).
  if (feedback) {
    storage.setListeningCompleted(it.id);
  }

  container.innerHTML = `
    <article class="listening-item">
      <div class="srs-progress">
        <span><a id="listening-back" href="#/listening">← ${renderJa('リストに もどる')}</a></span>
      </div>
      <h2>${it.title_ja ? renderJa(it.title_ja) : esc(it.id)}</h2>
      <p class="muted small">${renderJa('けいしき')}: ${renderJa(FORMATS[it.format] || it.format)}</p>
      <div class="listening-audio">
        ${it.audio ? `<audio controls preload="none" src="${esc(it.audio)}">Audio</audio>` : `<p class="muted small">${renderJa('おんせいファイルは まだ ありません。')}</p>`}
      </div>
      ${it.prompt_ja ? `<p>${renderJa(it.prompt_ja)}</p>` : ''}
      ${it.choices ? `
        <div class="choice-grid">
          ${it.choices.map(c => {
            let cls = 'choice-button';
            if (feedback) {
              if (c === it.correctAnswer) cls += ' correct-choice';
              else if (c === picked) cls += ' wrong-choice';
            } else if (picked === c) {
              cls += ' selected';
            }
            return `<button data-pick="${esc(c)}" class="${cls}" ${feedback ? 'disabled' : ''}>${renderJa(c)}</button>`;
          }).join('')}
        </div>
      ` : ''}
      ${feedback ? `
        <div class="drill-feedback ${correct ? 'correct' : 'incorrect'}">
          <div class="feedback-headline">${correct ? renderJa('せいかい') : renderJa('ざんねん')}</div>
          ${it.script_ja ? `<details><summary>${renderJa('スクリプトを 見る')}</summary><div>${renderJa(it.script_ja)}</div></details>` : ''}
          ${it.explanation_en ? `<p class="muted small">${esc(it.explanation_en)}</p>` : ''}
          <button id="listening-back-list" class="btn-primary">${renderJa('リストに もどる')}</button>
        </div>
      ` : ''}
    </article>
  `;
  container.querySelectorAll('[data-pick]').forEach(btn => {
    btn.addEventListener('click', () => {
      session.picked = btn.dataset.pick;
      renderItem(container);
    });
  });
  document.getElementById('listening-back')?.addEventListener('click', (e) => {
    e.preventDefault();
    session = null;
    renderIndex(container);
  });
  document.getElementById('listening-back-list')?.addEventListener('click', () => {
    session = null;
    renderIndex(container);
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
