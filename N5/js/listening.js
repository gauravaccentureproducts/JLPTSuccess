// Listening module shell (Brief §3.1)
// Three JLPT N5 listening formats: 課題理解 / ポイント理解 / 発話表現.
// Audio assets ship via the build-time TTS pipeline (tools/build_audio.py).
// When MP3s are absent, the module degrades gracefully: shows the script
// text + plays nothing, with a clear "audio not yet generated" notice.
import { renderJa } from './furigana.js';
import * as storage from './storage.js';
import { hasAlignedTranscript, renderTranscriptHTML, wireTranscriptSync } from './listening-transcript.js';
import { t } from './i18n.js';

let bank = null;
let session = null;

// 課題理解 / ポイント理解 / 発話表現 are official JLPT format names; the
// kanji 課 解 達 表 現 are not in the N5 catalog, but these labels are
// authentic JLPT taxonomy and the kana gloss is shown alongside.
const FORMATS = {
  task:      'かだいりかい (タスクりかい)',
  point:     'ポイントりかい',
  utterance: 'はつわひょうげん',
  // ISSUE-057 (audit round-7): mondai-4 即時応答 (immediate response).
  // Distinct from utterance/発話表現 (mondai-3). Three short replies,
  // pick the most natural rejoinder.
  response:  'そくじおうとう',
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

export async function renderListening(container, params) {
  await loadBank();
  // 2026-05-08: URL-based routing for listening detail. User reported
  // refresh on a detail page bouncing back to the index — that was a
  // symptom of the detail view being purely in-memory (`session`)
  // with no URL representation. Now `#/listening/<id>` deep-links to
  // a specific item; refresh preserves it; sharing the URL works.
  const id = (params || '').trim();
  if (id) {
    const item = (bank.items || []).find(it => it.id === id);
    if (!item) {
      // Unknown id — redirect to index. The hashchange triggered by
      // the assignment causes the router to re-fire renderListening
      // with empty params, which falls into the index path below.
      session = null;
      location.hash = '#/listening';
      return;
    }
    // Preserve `picked` only if we're already on the same item (e.g.
    // a re-render after a click). Otherwise start fresh.
    if (!session || session.item?.id !== item.id) {
      session = { item, picked: null };
    }
    return renderItem(container);
  }
  // No params: index view. Drop any prior session so going back to
  // an item via the index lands on a fresh question.
  session = null;
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
      // Navigate via hashchange so the detail view has its own URL
      // (refresh-survives, share-link-able). The router's hashchange
      // listener in app.js calls renderListening(container, id),
      // which loads the item and shows renderItem.
      location.hash = `#/listening/${encodeURIComponent(btn.dataset.id)}`;
    });
  });
}

function renderItem(container) {
  const it = session.item;
  const picked = session.picked;
  const feedback = picked != null;
  const correct = picked === it.correctAnswer;
  // Mark as completed the first time the user submits any answer (right
  // or wrong - listening counts toward syllabus progress on engagement,
  // not just correctness, since the audio comprehension is the practice).
  if (feedback) {
    storage.setListeningCompleted(it.id);
  }

  // 2026-05-08: prev/next item nav, matching the grammar/kanji detail
  // pages. Order is the natural file order (n5.listen.001 → .047),
  // grouped roughly by mondai. Clicking a button replaces `session.item`
  // and re-renders. The "list" back-link at the top of the article still
  // works for jumping out of sequential nav.
  const items = (bank?.items) || [];
  const idx = items.findIndex(x => x.id === it.id);
  const prev = idx > 0 ? items[idx - 1] : null;
  const next = idx >= 0 && idx < items.length - 1 ? items[idx + 1] : null;
  const navHtml = (prev || next) ? `
    <nav class="listening-nav" aria-label="Listening item navigation">
      ${prev
        ? `<button type="button" class="listening-nav-btn listening-nav-prev" data-nav="prev" title="${esc(prev.title_ja || prev.id)}">
             <span class="listening-nav-arrow" aria-hidden="true">&larr;</span>
             <span class="listening-nav-meta">
               <span class="listening-nav-label muted small">${renderJa('まえ')}</span>
               <span class="listening-nav-name" lang="ja">${prev.title_ja ? renderJa(prev.title_ja) : esc(prev.id)}</span>
             </span>
           </button>`
        : `<span class="listening-nav-btn listening-nav-empty" aria-hidden="true"></span>`}
      ${next
        ? `<button type="button" class="listening-nav-btn listening-nav-next" data-nav="next" title="${esc(next.title_ja || next.id)}">
             <span class="listening-nav-meta">
               <span class="listening-nav-label muted small">${renderJa('つぎ')}</span>
               <span class="listening-nav-name" lang="ja">${next.title_ja ? renderJa(next.title_ja) : esc(next.id)}</span>
             </span>
             <span class="listening-nav-arrow" aria-hidden="true">&rarr;</span>
           </button>`
        : `<span class="listening-nav-btn listening-nav-empty" aria-hidden="true"></span>`}
    </nav>
  ` : '';

  container.innerHTML = `
    <article class="listening-item">
      <div class="srs-progress">
        <span><a id="listening-back" href="#/listening">← ${renderJa('リストに もどる')}</a></span>
      </div>
      <h2>${it.title_ja ? renderJa(it.title_ja) : esc(it.id)}</h2>
      <p class="muted small">${renderJa('けいしき')}: ${renderJa(FORMATS[it.format] || it.format)}</p>
      <div class="listening-audio">
        ${it.audio ? `
          <audio id="listening-audio-${esc(it.id)}" controls preload="none" src="${esc(it.audio)}">Audio</audio>
          ${it.audio_slow ? `
            <!-- IMP-141 (richness audit, 2026-05-09): slow-version
                 0.7x render. Toggle swaps the <audio> src + label
                 so users can replay at beginner-friendly tempo
                 without losing the original-speed reference. -->
            <div class="listening-speed-toggle" role="group" aria-label="${esc(renderJa('さいせい そくど'))}">
              <button type="button" class="listening-speed-btn is-active" data-listening-speed="normal"
                      data-audio-target="listening-audio-${esc(it.id)}"
                      data-audio-normal="${esc(it.audio)}"
                      data-audio-slow="${esc(it.audio_slow)}">
                ${renderJa('ふつう')} (1.0×)
              </button>
              <button type="button" class="listening-speed-btn" data-listening-speed="slow"
                      data-audio-target="listening-audio-${esc(it.id)}"
                      data-audio-normal="${esc(it.audio)}"
                      data-audio-slow="${esc(it.audio_slow)}">
                ${renderJa('ゆっくり')} (0.7×)
              </button>
            </div>
          ` : ''}
        ` : `<p class="muted small">${renderJa('おんせいファイルは まだ ありません。')}</p>`}
      </div>
      ${it.voice_planned ? (() => {
        // F-10 (legal-vetting 2026-05-11): surface synthetic-voice provenance
        // on the playback UI per audit recommendation (was only in NOTICES.md
        // + audio_render_meta). Strip the ja-JP-...Neural wrapper for a
        // friendly speaker label; engine identifier stays as-is.
        const friendly = v => v ? String(v).replace(/^ja-JP-/, '').replace(/Neural$/, '') : '';
        const p = friendly(it.voice_planned.primary);
        const s = friendly(it.voice_planned.secondary);
        const engine = it.voice_planned.engine || 'TTS';
        const names = [p, s].filter(Boolean).join(' · ');
        const label = (typeof t === 'function' ? t('listening.voices_label') : 'Voices') || 'Voices';
        return `<p class="muted xs listening-voice-attribution">
          ${esc(label)}: ${esc(names)} (${esc(engine)})
        </p>`;
      })() : ''}
      ${it.prompt_ja ? `<p>${renderJa(it.prompt_ja)}</p>` : ''}
      ${(() => {
        // IMP-WAVE4 (UI audit fix, 2026-05-11): listening_strategy_hints —
        // mondai-format-keyed strategic guidance (4 hints per item).
        const hints = Array.isArray(it.listening_strategy_hints) ? it.listening_strategy_hints : [];
        if (!hints.length) return '';
        return `
          <aside class="listening-strategy-hints">
            <details>
              <summary><strong>${esc(t('chokai_detail.strategy_hints'))} (${hints.length})</strong></summary>
              <ul>
                ${hints.map(h => `<li class="muted small">${esc(h)}</li>`).join('')}
              </ul>
            </details>
          </aside>
        `;
      })()}
      ${(() => {
        // IMP-WAVE4: speech_rate_classification — pacing vs N5 standard.
        const sr = it.speech_rate_classification;
        if (!sr || typeof sr !== 'object' || !sr.category) return '';
        return `
          <p class="muted small listening-speech-rate">
            <strong>${esc(t('chokai_detail.speech_rate'))}:</strong> ${esc(sr.category)}
            ${sr.morae_per_min ? ` <span class="muted">(${esc(sr.morae_per_min)} mora/min)</span>` : ''}
            ${sr.note ? `<br><span class="muted small">${esc(sr.note)}</span>` : ''}
          </p>
        `;
      })()}
      ${(() => {
        // IMP-WAVE4: register_signal_l — auto-detected register for listening.
        const rs = it.register_signal_l;
        if (!rs || typeof rs !== 'object' || !rs.register) return '';
        return `
          <p class="muted small listening-register-signal">
            <strong>${esc(t('chokai_detail.register'))}:</strong> ${esc(rs.register)}${rs.confidence ? ` <span class="muted">(${esc(rs.confidence)} ${esc(t('chokai_detail.confidence'))})</span>` : ''}
            ${Array.isArray(rs.signals) && rs.signals.length ? `<br><span class="muted small">${esc(t('chokai_detail.signals'))}: ${rs.signals.map(esc).join('; ')}</span>` : ''}
          </p>
        `;
      })()}
      ${(() => {
        // IMP-WAVE4: speaker_demographics — auto-extracted speaker roles.
        const sd = it.speaker_demographics;
        if (!sd || typeof sd !== 'object' || !Array.isArray(sd.roles_detected) || !sd.roles_detected.length) return '';
        return `
          <p class="muted small listening-speakers">
            <strong>${esc(t('chokai_detail.speakers_detected'))} (${sd.n_speakers_inferred || sd.roles_detected.length}):</strong>
            ${sd.roles_detected.map(r => `<span class="speaker-role-chip" lang="ja">${esc(r.tag || r.role || '?')}</span>`).join(' ')}
          </p>
        `;
      })()}
      ${(() => {
        // IMP-WAVE4: prosody_hints — intonation cues from punctuation.
        const ph = Array.isArray(it.prosody_hints) ? it.prosody_hints : [];
        if (!ph.length) return '';
        return `
          <aside class="listening-prosody">
            <details>
              <summary class="muted small"><strong>${esc(t('chokai_detail.prosody_intonation_cues'))}</strong></summary>
              <ul>
                ${ph.map(h => `<li class="muted small">${esc(h)}</li>`).join('')}
              </ul>
            </details>
          </aside>
        `;
      })()}
      ${(() => {
        // IMP-WAVE4: time_target_seconds — JLPT N5 per-item time budget.
        const tt = it.time_target_seconds;
        if (!tt || typeof tt !== 'object') return '';
        return `
          <p class="muted small listening-time-target">
            <strong>${esc(t('chokai_detail.target_time'))}:</strong> ~${esc(tt.estimated_total_seconds || tt.jlpt_target_seconds_per_question || '?')}s
            ${tt.audio_seconds_estimated ? `<span class="muted"> (${esc(t('chokai_detail.audio_approx'))}${esc(tt.audio_seconds_estimated)}s)</span>` : ''}
          </p>
        `;
      })()}
      ${(() => {
        // IMP-WAVE4: distractor_pattern_hint — what trap the wrong answers represent.
        const dp = it.distractor_pattern_hint;
        if (!dp || typeof dp !== 'object' || !dp.pattern) return '';
        return `
          <aside class="listening-distractor-pattern">
            <details>
              <summary class="muted small"><strong>${esc(t('chokai_detail.distractor_pattern'))}:</strong> ${esc(dp.pattern)}</summary>
              ${dp.note ? `<p class="muted small">${esc(dp.note)}</p>` : ''}
              ${dp.mentioned_count != null ? `<p class="muted small">${esc(t('chokai_detail.mentioned_rejected_count'))}: ${esc(dp.mentioned_count)}</p>` : ''}
            </details>
          </aside>
        `;
      })()}
      ${it.authentic_categories?.length ? `
        <!-- IMP-WAVE-AUTHENTIC-XLINK (2026-05-11): thematic
             cross-link from listening setting (ambient_context)
             to matching authentic-content categories. -->
        <aside class="listening-authentic-link muted small">
          <strong>Related real-world content:</strong>
          ${it.authentic_categories.map(c => `<a href="#/authentic" class="authentic-cat-chip">${esc(c)}</a>`).join(' ')}
        </aside>
      ` : ''}
      ${it.timestamped_transcript && Array.isArray(it.timestamped_transcript.lines) && it.timestamped_transcript.lines.length ? `
        <!-- IMP-WAVE-P3-17 (UI audit fix, 2026-05-11): estimated
             line-level timestamps from mora-proportional
             distribution. The estimated:true flag signals these
             aren't from waveform alignment. -->
        <aside class="listening-timestamps">
          <details>
            <summary class="muted small">
              <strong>Timestamped transcript</strong>
              ${it.timestamped_transcript.estimated ? '<span class="muted small">(estimated, ~' + it.timestamped_transcript.total_seconds + 's)</span>' : ''}
            </summary>
            <table class="listening-timestamp-table">
              <thead><tr><th>Time</th><th>Speaker</th><th lang="ja">セリフ</th></tr></thead>
              <tbody>
                ${it.timestamped_transcript.lines.map(ln => `
                  <tr>
                    <td class="muted small">${esc(ln.start_s.toFixed(1))}–${esc(ln.end_s.toFixed(1))}s</td>
                    <td class="muted small">${esc(ln.speaker || '-')}</td>
                    <td lang="ja">${esc(ln.text || '')}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </details>
        </aside>
      ` : ''}
      ${it.inference_question_expansion && Array.isArray(it.inference_question_expansion.prompts) && it.inference_question_expansion.prompts.length ? `
        <!-- IMP-WAVE-P2-14 (UI audit fix, 2026-05-11): post-item
             inference questions that go beyond literal comprehension.
             Types: next_utterance / speaker_intent / implication /
             relationship. -->
        <aside class="listening-inference-prompts">
          <details>
            <summary class="muted small"><strong>Going deeper</strong> — inference questions</summary>
            <ul>
              ${it.inference_question_expansion.prompts.map(q => `
                <li>
                  <span class="inference-type-chip muted small">${esc(q.type || 'inference')}</span>
                  <span lang="ja">${esc(q.prompt_ja || '')}</span>
                  ${q.prompt_en ? `<br><span class="muted small">${esc(q.prompt_en)}</span>` : ''}
                  ${q.hint ? `<br><em class="muted small">Hint: ${esc(q.hint)}</em>` : ''}
                </li>
              `).join('')}
            </ul>
          </details>
        </aside>
      ` : ''}
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
          ${hasAlignedTranscript(it)
            ? `<details open><summary>${renderJa('スクリプト')}</summary>${renderTranscriptHTML(it)}</details>`
            : (it.script_ja ? `<details><summary>${renderJa('スクリプトを 見る')}</summary><div>${renderJa(it.script_ja)}</div></details>` : '')}
          ${it.explanation_en ? `<p class="muted small">${esc(it.explanation_en)}</p>` : ''}
          <button id="listening-back-list" class="btn-primary">${renderJa('リストに もどる')}</button>
        </div>
      ` : ''}
      ${navHtml}
    </article>
  `;
  // Wire prev/next nav buttons. Navigate via hashchange so the URL
  // captures the active item — refresh-survives, share-link-able.
  // Router's hashchange listener picks up the new id and re-renders.
  container.querySelector('[data-nav="prev"]')?.addEventListener('click', () => {
    if (prev) { window.scrollTo(0, 0); location.hash = `#/listening/${encodeURIComponent(prev.id)}`; }
  });
  container.querySelector('[data-nav="next"]')?.addEventListener('click', () => {
    if (next) { window.scrollTo(0, 0); location.hash = `#/listening/${encodeURIComponent(next.id)}`; }
  });
  container.querySelectorAll('[data-pick]').forEach(btn => {
    btn.addEventListener('click', () => {
      // `picked` is in-memory only — refresh resets it. The URL still
      // points at the same item, so refresh keeps the user on this
      // page (no answer pre-selected after refresh; that's OK).
      session.picked = btn.dataset.pick;
      renderItem(container);
    });
  });
  // "← リストに もどる" link at the top: keep its href="#/listening",
  // remove the preventDefault so the browser actually navigates and
  // the URL changes (was previously rendering index without updating
  // the URL — a refresh would then jump back to the detail page).
  // No JS handler needed — the anchor's href does the work.
  document.getElementById('listening-back-list')?.addEventListener('click', () => {
    location.hash = '#/listening';
  });
  // IMP-070: wire transcript-line click-to-seek + auto-highlight when
  // the item ships with a `lines` array. No-op when absent.
  wireTranscriptSync(container, it);
  // IMP-141 (richness audit, 2026-05-09): slow-audio toggle.
  // Swap the <audio> src to the slow render and resume playback at
  // the same relative position. No-op when audio_slow is absent.
  container.querySelectorAll('[data-listening-speed]').forEach(btn => {
    btn.addEventListener('click', () => {
      const speed = btn.dataset.listeningSpeed;
      const audioId = btn.dataset.audioTarget;
      const audio = document.getElementById(audioId);
      if (!audio) return;
      const newSrc = speed === 'slow' ? btn.dataset.audioSlow : btn.dataset.audioNormal;
      // Preserve relative position so the toggle feels seamless.
      const wasPlaying = !audio.paused;
      const ratio = audio.duration ? audio.currentTime / audio.duration : 0;
      audio.pause();
      audio.src = newSrc;
      audio.addEventListener('loadedmetadata', () => {
        if (audio.duration && ratio > 0) audio.currentTime = audio.duration * ratio;
        if (wasPlaying) audio.play().catch(() => {});
      }, { once: true });
      // Visual state on the toggle group
      btn.parentElement?.querySelectorAll('[data-listening-speed]').forEach(b => {
        b.classList.toggle('is-active', b === btn);
      });
    });
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
