import{renderJa as t}from"./furigana.js";import*as _ from"./storage.js";import{hasAlignedTranscript as L,renderTranscriptHTML as E,wireTranscriptSync as S}from"./listening-transcript.js";let c=null,g=null;const f={task:"\u304B\u3060\u3044\u308A\u304B\u3044 (\u30BF\u30B9\u30AF\u308A\u304B\u3044)",point:"\u30DD\u30A4\u30F3\u30C8\u308A\u304B\u3044",utterance:"\u306F\u3064\u308F\u3072\u3087\u3046\u3052\u3093",response:"\u305D\u304F\u3058\u304A\u3046\u3068\u3046"};async function T(){if(c)return c;try{const n=await fetch("data/listening.json");if(!n.ok)return c={items:[]},c;c=await n.json()}catch{c={items:[]}}return c}async function I(n,e){await T();const u=(e||"").trim();if(u){const r=(c.items||[]).find(m=>m.id===u);if(!r){g=null,location.hash="#/listening";return}return(!g||g.item?.id!==r.id)&&(g={item:r,picked:null}),b(n)}return g=null,q(n)}function q(n){const e=c.items||[];if(e.length===0){n.innerHTML=`
      <h2>${t("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
      <div class="placeholder">
        <p><strong>No listening items shipped yet.</strong></p>
        <p>The listening module is wired and will activate as soon as audio assets ship.</p>
        <p class="muted small">For developers: run <code>python tools/build_audio.py</code> to generate MP3 files for every reading passage and listening script. Audio files land in <code>audio/listening/*.mp3</code> and <code>audio/reading/*.mp3</code>; the service worker will cache them on first online visit.</p>
        <p class="muted small">Listening scripts and questions live in <code>data/listening.json</code> (created by the same build).</p>
      </div>
    `;return}const u=e.reduce((i,o)=>((i[o.format]=i[o.format]||[]).push(o),i),{});n.innerHTML=`
    <h2>${t("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${t("JLPT N5 \u3061\u3087\u3046\u304B\u3044\u306E \u4E09\u3064\u306E \u3051\u3044\u3057\u304D\u3002\u304A\u3093\u305B\u3044\u3092 \u805E\u3044\u3066\u3001\u305F\u3060\u3057\u3044 \u3053\u305F\u3048\u3092 \u3048\u3089\u3093\u3067 \u304F\u3060\u3055\u3044\u3002")}</p>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">${t("\u305C\u3093\u3076 \u3072\u3089\u304F")}</button>
      <button type="button" class="btn-secondary toc-collapse-all">${t("\u305C\u3093\u3076 \u3068\u3058\u308B")}</button>
    </div>
    ${Object.entries(u).map(([i,o])=>`
      <details class="listening-section">
        <summary><h3>${t(f[i]||i)} <span class="muted small">(${o.length})</span></h3></summary>
        <ul class="listening-list">
          ${o.map(l=>`<li><button class="listening-pick" data-id="${s(l.id)}">${l.title_ja?t(l.title_ja):s(l.id)}</button></li>`).join("")}
        </ul>
      </details>
    `).join("")}
  `;const r=n.querySelector(".toc-expand-all"),m=n.querySelector(".toc-collapse-all");r&&r.addEventListener("click",()=>{n.querySelectorAll("details.listening-section").forEach(i=>i.open=!0)}),m&&m.addEventListener("click",()=>{n.querySelectorAll("details.listening-section").forEach(i=>i.open=!1)}),n.querySelectorAll("[data-id]").forEach(i=>{i.addEventListener("click",()=>{location.hash=`#/listening/${encodeURIComponent(i.dataset.id)}`})})}function b(n){const e=g.item,u=g.picked,r=u!=null,m=u===e.correctAnswer;r&&_.setListeningCompleted(e.id);const i=c?.items||[],o=i.findIndex(a=>a.id===e.id),l=o>0?i[o-1]:null,p=o>=0&&o<i.length-1?i[o+1]:null,y=l||p?`
    <nav class="listening-nav" aria-label="Listening item navigation">
      ${l?`<button type="button" class="listening-nav-btn listening-nav-prev" data-nav="prev" title="${s(l.title_ja||l.id)}">
             <span class="listening-nav-arrow" aria-hidden="true">&larr;</span>
             <span class="listening-nav-meta">
               <span class="listening-nav-label muted small">${t("\u307E\u3048")}</span>
               <span class="listening-nav-name" lang="ja">${l.title_ja?t(l.title_ja):s(l.id)}</span>
             </span>
           </button>`:'<span class="listening-nav-btn listening-nav-empty" aria-hidden="true"></span>'}
      ${p?`<button type="button" class="listening-nav-btn listening-nav-next" data-nav="next" title="${s(p.title_ja||p.id)}">
             <span class="listening-nav-meta">
               <span class="listening-nav-label muted small">${t("\u3064\u304E")}</span>
               <span class="listening-nav-name" lang="ja">${p.title_ja?t(p.title_ja):s(p.id)}</span>
             </span>
             <span class="listening-nav-arrow" aria-hidden="true">&rarr;</span>
           </button>`:'<span class="listening-nav-btn listening-nav-empty" aria-hidden="true"></span>'}
    </nav>
  `:"";n.innerHTML=`
    <article class="listening-item">
      <div class="srs-progress">
        <span><a id="listening-back" href="#/listening">\u2190 ${t("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</a></span>
      </div>
      <h2>${e.title_ja?t(e.title_ja):s(e.id)}</h2>
      <p class="muted small">${t("\u3051\u3044\u3057\u304D")}: ${t(f[e.format]||e.format)}</p>
      <div class="listening-audio">
        ${e.audio?`
          <audio id="listening-audio-${s(e.id)}" controls preload="none" src="${s(e.audio)}">Audio</audio>
          ${e.audio_slow?`
            <!-- IMP-141 (richness audit, 2026-05-09): slow-version
                 0.7x render. Toggle swaps the <audio> src + label
                 so users can replay at beginner-friendly tempo
                 without losing the original-speed reference. -->
            <div class="listening-speed-toggle" role="group" aria-label="${s(t("\u3055\u3044\u305B\u3044 \u305D\u304F\u3069"))}">
              <button type="button" class="listening-speed-btn is-active" data-listening-speed="normal"
                      data-audio-target="listening-audio-${s(e.id)}"
                      data-audio-normal="${s(e.audio)}"
                      data-audio-slow="${s(e.audio_slow)}">
                ${t("\u3075\u3064\u3046")} (1.0\xD7)
              </button>
              <button type="button" class="listening-speed-btn" data-listening-speed="slow"
                      data-audio-target="listening-audio-${s(e.id)}"
                      data-audio-normal="${s(e.audio)}"
                      data-audio-slow="${s(e.audio_slow)}">
                ${t("\u3086\u3063\u304F\u308A")} (0.7\xD7)
              </button>
            </div>
          `:""}
        `:`<p class="muted small">${t("\u304A\u3093\u305B\u3044\u30D5\u30A1\u30A4\u30EB\u306F \u307E\u3060 \u3042\u308A\u307E\u305B\u3093\u3002")}</p>`}
      </div>
      ${e.prompt_ja?`<p>${t(e.prompt_ja)}</p>`:""}
      ${e.choices?`
        <div class="choice-grid">
          ${e.choices.map(a=>{let v="choice-button";return r?a===e.correctAnswer?v+=" correct-choice":a===u&&(v+=" wrong-choice"):u===a&&(v+=" selected"),`<button data-pick="${s(a)}" class="${v}" ${r?"disabled":""}>${t(a)}</button>`}).join("")}
        </div>
      `:""}
      ${r?`
        <div class="drill-feedback ${m?"correct":"incorrect"}">
          <div class="feedback-headline">${m?t("\u305B\u3044\u304B\u3044"):t("\u3056\u3093\u306D\u3093")}</div>
          ${L(e)?`<details open><summary>${t("\u30B9\u30AF\u30EA\u30D7\u30C8")}</summary>${E(e)}</details>`:e.script_ja?`<details><summary>${t("\u30B9\u30AF\u30EA\u30D7\u30C8\u3092 \u898B\u308B")}</summary><div>${t(e.script_ja)}</div></details>`:""}
          ${e.explanation_en?`<p class="muted small">${s(e.explanation_en)}</p>`:""}
          <button id="listening-back-list" class="btn-primary">${t("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</button>
        </div>
      `:""}
      ${y}
    </article>
  `,n.querySelector('[data-nav="prev"]')?.addEventListener("click",()=>{l&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(l.id)}`)}),n.querySelector('[data-nav="next"]')?.addEventListener("click",()=>{p&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(p.id)}`)}),n.querySelectorAll("[data-pick]").forEach(a=>{a.addEventListener("click",()=>{g.picked=a.dataset.pick,b(n)})}),document.getElementById("listening-back-list")?.addEventListener("click",()=>{location.hash="#/listening"}),S(n,e),n.querySelectorAll("[data-listening-speed]").forEach(a=>{a.addEventListener("click",()=>{const v=a.dataset.listeningSpeed,w=a.dataset.audioTarget,d=document.getElementById(w);if(!d)return;const k=v==="slow"?a.dataset.audioSlow:a.dataset.audioNormal,j=!d.paused,$=d.duration?d.currentTime/d.duration:0;d.pause(),d.src=k,d.addEventListener("loadedmetadata",()=>{d.duration&&$>0&&(d.currentTime=d.duration*$),j&&d.play().catch(()=>{})},{once:!0}),a.parentElement?.querySelectorAll("[data-listening-speed]").forEach(h=>{h.classList.toggle("is-active",h===a)})})})}function s(n){return String(n??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{I as renderListening};
