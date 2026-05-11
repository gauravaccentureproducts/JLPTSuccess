import{renderJa as n}from"./furigana.js";import*as A from"./storage.js";import{hasAlignedTranscript as x,renderTranscriptHTML as T,wireTranscriptSync as E}from"./listening-transcript.js";import{t as d}from"./i18n.js";let m=null,$=null;const k={task:"\u304B\u3060\u3044\u308A\u304B\u3044 (\u30BF\u30B9\u30AF\u308A\u304B\u3044)",point:"\u30DD\u30A4\u30F3\u30C8\u308A\u304B\u3044",utterance:"\u306F\u3064\u308F\u3072\u3087\u3046\u3052\u3093",response:"\u305D\u304F\u3058\u304A\u3046\u3068\u3046"};async function L(){if(m)return m;try{const a=await fetch("data/listening.json");if(!a.ok)return m={items:[]},m;m=await a.json()}catch{m={items:[]}}return m}async function P(a,t){await L();const u=(t||"").trim();if(u){const p=(m.items||[]).find(h=>h.id===u);if(!p){$=null,location.hash="#/listening";return}return(!$||$.item?.id!==p.id)&&($={item:p,picked:null}),j(a)}return $=null,S(a)}function S(a){const t=m.items||[];if(t.length===0){a.innerHTML=`
      <h2>${n("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
      <div class="placeholder">
        <p><strong>No listening items shipped yet.</strong></p>
        <p>The listening module is wired and will activate as soon as audio assets ship.</p>
        <p class="muted small">For developers: run <code>python tools/build_audio.py</code> to generate MP3 files for every reading passage and listening script. Audio files land in <code>audio/listening/*.mp3</code> and <code>audio/reading/*.mp3</code>; the service worker will cache them on first online visit.</p>
        <p class="muted small">Listening scripts and questions live in <code>data/listening.json</code> (created by the same build).</p>
      </div>
    `;return}const u=t.reduce((i,c)=>((i[c.format]=i[c.format]||[]).push(c),i),{});a.innerHTML=`
    <h2>${n("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${n("JLPT N5 \u3061\u3087\u3046\u304B\u3044\u306E \u4E09\u3064\u306E \u3051\u3044\u3057\u304D\u3002\u304A\u3093\u305B\u3044\u3092 \u805E\u3044\u3066\u3001\u305F\u3060\u3057\u3044 \u3053\u305F\u3048\u3092 \u3048\u3089\u3093\u3067 \u304F\u3060\u3055\u3044\u3002")}</p>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">${n("\u305C\u3093\u3076 \u3072\u3089\u304F")}</button>
      <button type="button" class="btn-secondary toc-collapse-all">${n("\u305C\u3093\u3076 \u3068\u3058\u308B")}</button>
    </div>
    ${Object.entries(u).map(([i,c])=>`
      <details class="listening-section">
        <summary><h3>${n(k[i]||i)} <span class="muted small">(${c.length})</span></h3></summary>
        <ul class="listening-list">
          ${c.map(r=>`<li><button class="listening-pick" data-id="${s(r.id)}">${r.title_ja?n(r.title_ja):s(r.id)}</button></li>`).join("")}
        </ul>
      </details>
    `).join("")}
  `;const p=a.querySelector(".toc-expand-all"),h=a.querySelector(".toc-collapse-all");p&&p.addEventListener("click",()=>{a.querySelectorAll("details.listening-section").forEach(i=>i.open=!0)}),h&&h.addEventListener("click",()=>{a.querySelectorAll("details.listening-section").forEach(i=>i.open=!1)}),a.querySelectorAll("[data-id]").forEach(i=>{i.addEventListener("click",()=>{location.hash=`#/listening/${encodeURIComponent(i.dataset.id)}`})})}function j(a){const t=$.item,u=$.picked,p=u!=null,h=u===t.correctAnswer;p&&A.setListeningCompleted(t.id);const i=m?.items||[],c=i.findIndex(e=>e.id===t.id),r=c>0?i[c-1]:null,g=c>=0&&c<i.length-1?i[c+1]:null,w=r||g?`
    <nav class="listening-nav" aria-label="Listening item navigation">
      ${r?`<button type="button" class="listening-nav-btn listening-nav-prev" data-nav="prev" title="${s(r.title_ja||r.id)}">
             <span class="listening-nav-arrow" aria-hidden="true">&larr;</span>
             <span class="listening-nav-meta">
               <span class="listening-nav-label muted small">${n("\u307E\u3048")}</span>
               <span class="listening-nav-name" lang="ja">${r.title_ja?n(r.title_ja):s(r.id)}</span>
             </span>
           </button>`:'<span class="listening-nav-btn listening-nav-empty" aria-hidden="true"></span>'}
      ${g?`<button type="button" class="listening-nav-btn listening-nav-next" data-nav="next" title="${s(g.title_ja||g.id)}">
             <span class="listening-nav-meta">
               <span class="listening-nav-label muted small">${n("\u3064\u304E")}</span>
               <span class="listening-nav-name" lang="ja">${g.title_ja?n(g.title_ja):s(g.id)}</span>
             </span>
             <span class="listening-nav-arrow" aria-hidden="true">&rarr;</span>
           </button>`:'<span class="listening-nav-btn listening-nav-empty" aria-hidden="true"></span>'}
    </nav>
  `:"";a.innerHTML=`
    <article class="listening-item">
      <div class="srs-progress">
        <span><a id="listening-back" href="#/listening">\u2190 ${n("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</a></span>
      </div>
      <h2>${t.title_ja?n(t.title_ja):s(t.id)}</h2>
      <p class="muted small">${n("\u3051\u3044\u3057\u304D")}: ${n(k[t.format]||t.format)}</p>
      <div class="listening-audio">
        ${t.audio?`
          <audio id="listening-audio-${s(t.id)}" controls preload="none" src="${s(t.audio)}">Audio</audio>
          ${t.audio_slow?`
            <!-- IMP-141 (richness audit, 2026-05-09): slow-version
                 0.7x render. Toggle swaps the <audio> src + label
                 so users can replay at beginner-friendly tempo
                 without losing the original-speed reference. -->
            <div class="listening-speed-toggle" role="group" aria-label="${s(n("\u3055\u3044\u305B\u3044 \u305D\u304F\u3069"))}">
              <button type="button" class="listening-speed-btn is-active" data-listening-speed="normal"
                      data-audio-target="listening-audio-${s(t.id)}"
                      data-audio-normal="${s(t.audio)}"
                      data-audio-slow="${s(t.audio_slow)}">
                ${n("\u3075\u3064\u3046")} (1.0\xD7)
              </button>
              <button type="button" class="listening-speed-btn" data-listening-speed="slow"
                      data-audio-target="listening-audio-${s(t.id)}"
                      data-audio-normal="${s(t.audio)}"
                      data-audio-slow="${s(t.audio_slow)}">
                ${n("\u3086\u3063\u304F\u308A")} (0.7\xD7)
              </button>
            </div>
          `:""}
        `:`<p class="muted small">${n("\u304A\u3093\u305B\u3044\u30D5\u30A1\u30A4\u30EB\u306F \u307E\u3060 \u3042\u308A\u307E\u305B\u3093\u3002")}</p>`}
      </div>
      ${t.voice_planned?(()=>{const e=_=>_?String(_).replace(/^ja-JP-/,"").replace(/Neural$/,""):"",l=e(t.voice_planned.primary),y=e(t.voice_planned.secondary),o=t.voice_planned.engine||"TTS",f=[l,y].filter(Boolean).join(" \xB7 "),v=(typeof d=="function"?d("listening.voices_label"):"Voices")||"Voices";return`<p class="muted xs listening-voice-attribution">
          ${s(v)}: ${s(f)} (${s(o)})
        </p>`})():""}
      ${t.prompt_ja?`<p>${n(t.prompt_ja)}</p>`:""}
      ${(()=>{const e=Array.isArray(t.listening_strategy_hints)?t.listening_strategy_hints:[];return e.length?`
          <aside class="listening-strategy-hints">
            <details>
              <summary><strong>${s(d("chokai_detail.strategy_hints"))} (${e.length})</strong></summary>
              <ul>
                ${e.map(l=>`<li class="muted small">${s(l)}</li>`).join("")}
              </ul>
            </details>
          </aside>
        `:""})()}
      ${(()=>{const e=t.speech_rate_classification;return!e||typeof e!="object"||!e.category?"":`
          <p class="muted small listening-speech-rate">
            <strong>${s(d("chokai_detail.speech_rate"))}:</strong> ${s(e.category)}
            ${e.morae_per_min?` <span class="muted">(${s(e.morae_per_min)} mora/min)</span>`:""}
            ${e.note?`<br><span class="muted small">${s(e.note)}</span>`:""}
          </p>
        `})()}
      ${(()=>{const e=t.register_signal_l;return!e||typeof e!="object"||!e.register?"":`
          <p class="muted small listening-register-signal">
            <strong>${s(d("chokai_detail.register"))}:</strong> ${s(e.register)}${e.confidence?` <span class="muted">(${s(e.confidence)} ${s(d("chokai_detail.confidence"))})</span>`:""}
            ${Array.isArray(e.signals)&&e.signals.length?`<br><span class="muted small">${s(d("chokai_detail.signals"))}: ${e.signals.map(s).join("; ")}</span>`:""}
          </p>
        `})()}
      ${(()=>{const e=t.speaker_demographics;return!e||typeof e!="object"||!Array.isArray(e.roles_detected)||!e.roles_detected.length?"":`
          <p class="muted small listening-speakers">
            <strong>${s(d("chokai_detail.speakers_detected"))} (${e.n_speakers_inferred||e.roles_detected.length}):</strong>
            ${e.roles_detected.map(l=>`<span class="speaker-role-chip" lang="ja">${s(l.tag||l.role||"?")}</span>`).join(" ")}
          </p>
        `})()}
      ${(()=>{const e=Array.isArray(t.prosody_hints)?t.prosody_hints:[];return e.length?`
          <aside class="listening-prosody">
            <details>
              <summary class="muted small"><strong>${s(d("chokai_detail.prosody_intonation_cues"))}</strong></summary>
              <ul>
                ${e.map(l=>`<li class="muted small">${s(l)}</li>`).join("")}
              </ul>
            </details>
          </aside>
        `:""})()}
      ${(()=>{const e=t.time_target_seconds;return!e||typeof e!="object"?"":`
          <p class="muted small listening-time-target">
            <strong>${s(d("chokai_detail.target_time"))}:</strong> ~${s(e.estimated_total_seconds||e.jlpt_target_seconds_per_question||"?")}s
            ${e.audio_seconds_estimated?`<span class="muted"> (${s(d("chokai_detail.audio_approx"))}${s(e.audio_seconds_estimated)}s)</span>`:""}
          </p>
        `})()}
      ${(()=>{const e=t.distractor_pattern_hint;return!e||typeof e!="object"||!e.pattern?"":`
          <aside class="listening-distractor-pattern">
            <details>
              <summary class="muted small"><strong>${s(d("chokai_detail.distractor_pattern"))}:</strong> ${s(e.pattern)}</summary>
              ${e.note?`<p class="muted small">${s(e.note)}</p>`:""}
              ${e.mentioned_count!=null?`<p class="muted small">${s(d("chokai_detail.mentioned_rejected_count"))}: ${s(e.mentioned_count)}</p>`:""}
            </details>
          </aside>
        `})()}
      ${t.authentic_categories?.length?`
        <!-- IMP-WAVE-AUTHENTIC-XLINK (2026-05-11): thematic
             cross-link from listening setting (ambient_context)
             to matching authentic-content categories. -->
        <aside class="listening-authentic-link muted small">
          <strong>Related real-world content:</strong>
          ${t.authentic_categories.map(e=>`<a href="#/authentic" class="authentic-cat-chip">${s(e)}</a>`).join(" ")}
        </aside>
      `:""}
      ${t.timestamped_transcript&&Array.isArray(t.timestamped_transcript.lines)&&t.timestamped_transcript.lines.length?`
        <!-- IMP-WAVE-P3-17 (UI audit fix, 2026-05-11): estimated
             line-level timestamps from mora-proportional
             distribution. The estimated:true flag signals these
             aren't from waveform alignment. -->
        <aside class="listening-timestamps">
          <details>
            <summary class="muted small">
              <strong>Timestamped transcript</strong>
              ${t.timestamped_transcript.estimated?'<span class="muted small">(estimated, ~'+t.timestamped_transcript.total_seconds+"s)</span>":""}
            </summary>
            <table class="listening-timestamp-table">
              <thead><tr><th>Time</th><th>Speaker</th><th lang="ja">\u30BB\u30EA\u30D5</th></tr></thead>
              <tbody>
                ${t.timestamped_transcript.lines.map(e=>`
                  <tr>
                    <td class="muted small">${s(e.start_s.toFixed(1))}\u2013${s(e.end_s.toFixed(1))}s</td>
                    <td class="muted small">${s(e.speaker||"-")}</td>
                    <td lang="ja">${s(e.text||"")}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </details>
        </aside>
      `:""}
      ${t.inference_question_expansion&&Array.isArray(t.inference_question_expansion.prompts)&&t.inference_question_expansion.prompts.length?`
        <!-- IMP-WAVE-P2-14 (UI audit fix, 2026-05-11): post-item
             inference questions that go beyond literal comprehension.
             Types: next_utterance / speaker_intent / implication /
             relationship. -->
        <aside class="listening-inference-prompts">
          <details>
            <summary class="muted small"><strong>Going deeper</strong> \u2014 inference questions</summary>
            <ul>
              ${t.inference_question_expansion.prompts.map(e=>`
                <li>
                  <span class="inference-type-chip muted small">${s(e.type||"inference")}</span>
                  <span lang="ja">${s(e.prompt_ja||"")}</span>
                  ${e.prompt_en?`<br><span class="muted small">${s(e.prompt_en)}</span>`:""}
                  ${e.hint?`<br><em class="muted small">Hint: ${s(e.hint)}</em>`:""}
                </li>
              `).join("")}
            </ul>
          </details>
        </aside>
      `:""}
      ${t.choices?`
        <div class="choice-grid">
          ${t.choices.map(e=>{let l="choice-button";return p?e===t.correctAnswer?l+=" correct-choice":e===u&&(l+=" wrong-choice"):u===e&&(l+=" selected"),`<button data-pick="${s(e)}" class="${l}" ${p?"disabled":""}>${n(e)}</button>`}).join("")}
        </div>
      `:""}
      ${p?`
        <div class="drill-feedback ${h?"correct":"incorrect"}">
          <div class="feedback-headline">${h?n("\u305B\u3044\u304B\u3044"):n("\u3056\u3093\u306D\u3093")}</div>
          ${x(t)?`<details open><summary>${n("\u30B9\u30AF\u30EA\u30D7\u30C8")}</summary>${T(t)}</details>`:t.script_ja?`<details><summary>${n("\u30B9\u30AF\u30EA\u30D7\u30C8\u3092 \u898B\u308B")}</summary><div>${n(t.script_ja)}</div></details>`:""}
          ${t.explanation_en?`<p class="muted small">${s(t.explanation_en)}</p>`:""}
          <button id="listening-back-list" class="btn-primary">${n("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</button>
        </div>
      `:""}
      ${w}
    </article>
  `,a.querySelector('[data-nav="prev"]')?.addEventListener("click",()=>{r&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(r.id)}`)}),a.querySelector('[data-nav="next"]')?.addEventListener("click",()=>{g&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(g.id)}`)}),a.querySelectorAll("[data-pick]").forEach(e=>{e.addEventListener("click",()=>{$.picked=e.dataset.pick,j(a)})}),document.getElementById("listening-back-list")?.addEventListener("click",()=>{location.hash="#/listening"}),E(a,t),a.querySelectorAll("[data-listening-speed]").forEach(e=>{e.addEventListener("click",()=>{const l=e.dataset.listeningSpeed,y=e.dataset.audioTarget,o=document.getElementById(y);if(!o)return;const f=l==="slow"?e.dataset.audioSlow:e.dataset.audioNormal,v=!o.paused,_=o.duration?o.currentTime/o.duration:0;o.pause(),o.src=f,o.addEventListener("loadedmetadata",()=>{o.duration&&_>0&&(o.currentTime=o.duration*_),v&&o.play().catch(()=>{})},{once:!0}),e.parentElement?.querySelectorAll("[data-listening-speed]").forEach(b=>{b.classList.toggle("is-active",b===e)})})})}function s(a){return String(a??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{P as renderListening};
