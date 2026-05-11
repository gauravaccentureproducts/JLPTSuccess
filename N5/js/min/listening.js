import{renderJa as n}from"./furigana.js";import*as A from"./storage.js";import{hasAlignedTranscript as E,renderTranscriptHTML as L,wireTranscriptSync as T}from"./listening-transcript.js";import{t as d}from"./i18n.js";let u=null,$=null;const k={task:"\u304B\u3060\u3044\u308A\u304B\u3044 (\u30BF\u30B9\u30AF\u308A\u304B\u3044)",point:"\u30DD\u30A4\u30F3\u30C8\u308A\u304B\u3044",utterance:"\u306F\u3064\u308F\u3072\u3087\u3046\u3052\u3093",response:"\u305D\u304F\u3058\u304A\u3046\u3068\u3046"};async function S(){if(u)return u;try{const a=await fetch("data/listening.json");if(!a.ok)return u={items:[]},u;u=await a.json()}catch{u={items:[]}}return u}async function B(a,t){await S();const m=(t||"").trim();if(m){const p=(u.items||[]).find(h=>h.id===m);if(!p){$=null,location.hash="#/listening";return}return(!$||$.item?.id!==p.id)&&($={item:p,picked:null}),j(a)}return $=null,x(a)}function x(a){const t=u.items||[];if(t.length===0){a.innerHTML=`
      <h2>${n("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
      <div class="placeholder">
        <p><strong>No listening items shipped yet.</strong></p>
        <p>The listening module is wired and will activate as soon as audio assets ship.</p>
        <p class="muted small">For developers: run <code>python tools/build_audio.py</code> to generate MP3 files for every reading passage and listening script. Audio files land in <code>audio/listening/*.mp3</code> and <code>audio/reading/*.mp3</code>; the service worker will cache them on first online visit.</p>
        <p class="muted small">Listening scripts and questions live in <code>data/listening.json</code> (created by the same build).</p>
      </div>
    `;return}const m=t.reduce((i,c)=>((i[c.format]=i[c.format]||[]).push(c),i),{});a.innerHTML=`
    <h2>${n("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${n("JLPT N5 \u3061\u3087\u3046\u304B\u3044\u306E \u4E09\u3064\u306E \u3051\u3044\u3057\u304D\u3002\u304A\u3093\u305B\u3044\u3092 \u805E\u3044\u3066\u3001\u305F\u3060\u3057\u3044 \u3053\u305F\u3048\u3092 \u3048\u3089\u3093\u3067 \u304F\u3060\u3055\u3044\u3002")}</p>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">${n("\u305C\u3093\u3076 \u3072\u3089\u304F")}</button>
      <button type="button" class="btn-secondary toc-collapse-all">${n("\u305C\u3093\u3076 \u3068\u3058\u308B")}</button>
    </div>
    ${Object.entries(m).map(([i,c])=>`
      <details class="listening-section">
        <summary><h3>${n(k[i]||i)} <span class="muted small">(${c.length})</span></h3></summary>
        <ul class="listening-list">
          ${c.map(o=>`<li><button class="listening-pick" data-id="${s(o.id)}">${o.title_ja?n(o.title_ja):s(o.id)}</button></li>`).join("")}
        </ul>
      </details>
    `).join("")}
  `;const p=a.querySelector(".toc-expand-all"),h=a.querySelector(".toc-collapse-all");p&&p.addEventListener("click",()=>{a.querySelectorAll("details.listening-section").forEach(i=>i.open=!0)}),h&&h.addEventListener("click",()=>{a.querySelectorAll("details.listening-section").forEach(i=>i.open=!1)}),a.querySelectorAll("[data-id]").forEach(i=>{i.addEventListener("click",()=>{location.hash=`#/listening/${encodeURIComponent(i.dataset.id)}`})})}function j(a){const t=$.item,m=$.picked,p=m!=null,h=m===t.correctAnswer;p&&A.setListeningCompleted(t.id);const i=u?.items||[],c=i.findIndex(e=>e.id===t.id),o=c>0?i[c-1]:null,g=c>=0&&c<i.length-1?i[c+1]:null,w=o||g?`
    <nav class="listening-nav" aria-label="Listening item navigation">
      ${o?`<button type="button" class="listening-nav-btn listening-nav-prev" data-nav="prev" title="${s(o.title_ja||o.id)}">
             <span class="listening-nav-arrow" aria-hidden="true">&larr;</span>
             <span class="listening-nav-meta">
               <span class="listening-nav-label muted small">${n("\u307E\u3048")}</span>
               <span class="listening-nav-name" lang="ja">${o.title_ja?n(o.title_ja):s(o.id)}</span>
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
      ${t.voice_planned?(()=>{const e=_=>_?String(_).replace(/^ja-JP-/,"").replace(/Neural$/,""):"",l=e(t.voice_planned.primary),y=e(t.voice_planned.secondary),r=t.voice_planned.engine||"TTS",f=[l,y].filter(Boolean).join(" \xB7 "),v=(typeof d=="function"?d("listening.voices_label"):"Voices")||"Voices";return`<p class="muted xs listening-voice-attribution">
          ${s(v)}: ${s(f)} (${s(r)})
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
      ${t.choices?`
        <div class="choice-grid">
          ${t.choices.map(e=>{let l="choice-button";return p?e===t.correctAnswer?l+=" correct-choice":e===m&&(l+=" wrong-choice"):m===e&&(l+=" selected"),`<button data-pick="${s(e)}" class="${l}" ${p?"disabled":""}>${n(e)}</button>`}).join("")}
        </div>
      `:""}
      ${p?`
        <div class="drill-feedback ${h?"correct":"incorrect"}">
          <div class="feedback-headline">${h?n("\u305B\u3044\u304B\u3044"):n("\u3056\u3093\u306D\u3093")}</div>
          ${E(t)?`<details open><summary>${n("\u30B9\u30AF\u30EA\u30D7\u30C8")}</summary>${L(t)}</details>`:t.script_ja?`<details><summary>${n("\u30B9\u30AF\u30EA\u30D7\u30C8\u3092 \u898B\u308B")}</summary><div>${n(t.script_ja)}</div></details>`:""}
          ${t.explanation_en?`<p class="muted small">${s(t.explanation_en)}</p>`:""}
          <button id="listening-back-list" class="btn-primary">${n("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</button>
        </div>
      `:""}
      ${w}
    </article>
  `,a.querySelector('[data-nav="prev"]')?.addEventListener("click",()=>{o&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(o.id)}`)}),a.querySelector('[data-nav="next"]')?.addEventListener("click",()=>{g&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(g.id)}`)}),a.querySelectorAll("[data-pick]").forEach(e=>{e.addEventListener("click",()=>{$.picked=e.dataset.pick,j(a)})}),document.getElementById("listening-back-list")?.addEventListener("click",()=>{location.hash="#/listening"}),T(a,t),a.querySelectorAll("[data-listening-speed]").forEach(e=>{e.addEventListener("click",()=>{const l=e.dataset.listeningSpeed,y=e.dataset.audioTarget,r=document.getElementById(y);if(!r)return;const f=l==="slow"?e.dataset.audioSlow:e.dataset.audioNormal,v=!r.paused,_=r.duration?r.currentTime/r.duration:0;r.pause(),r.src=f,r.addEventListener("loadedmetadata",()=>{r.duration&&_>0&&(r.currentTime=r.duration*_),v&&r.play().catch(()=>{})},{once:!0}),e.parentElement?.querySelectorAll("[data-listening-speed]").forEach(b=>{b.classList.toggle("is-active",b===e)})})})}function s(a){return String(a??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{B as renderListening};
