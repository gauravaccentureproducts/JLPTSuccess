import{renderJa as n}from"./furigana.js";import*as L from"./storage.js";import{hasAlignedTranscript as E,renderTranscriptHTML as S,wireTranscriptSync as T}from"./listening-transcript.js";let p=null,v=null;const k={task:"\u304B\u3060\u3044\u308A\u304B\u3044 (\u30BF\u30B9\u30AF\u308A\u304B\u3044)",point:"\u30DD\u30A4\u30F3\u30C8\u308A\u304B\u3044",utterance:"\u306F\u3064\u308F\u3072\u3087\u3046\u3052\u3093",response:"\u305D\u304F\u3058\u304A\u3046\u3068\u3046"};async function x(){if(p)return p;try{const i=await fetch("data/listening.json");if(!i.ok)return p={items:[]},p;p=await i.json()}catch{p={items:[]}}return p}async function M(i,e){await x();const u=(e||"").trim();if(u){const c=(p.items||[]).find($=>$.id===u);if(!c){v=null,location.hash="#/listening";return}return(!v||v.item?.id!==c.id)&&(v={item:c,picked:null}),j(i)}return v=null,q(i)}function q(i){const e=p.items||[];if(e.length===0){i.innerHTML=`
      <h2>${n("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
      <div class="placeholder">
        <p><strong>No listening items shipped yet.</strong></p>
        <p>The listening module is wired and will activate as soon as audio assets ship.</p>
        <p class="muted small">For developers: run <code>python tools/build_audio.py</code> to generate MP3 files for every reading passage and listening script. Audio files land in <code>audio/listening/*.mp3</code> and <code>audio/reading/*.mp3</code>; the service worker will cache them on first online visit.</p>
        <p class="muted small">Listening scripts and questions live in <code>data/listening.json</code> (created by the same build).</p>
      </div>
    `;return}const u=e.reduce((l,r)=>((l[r.format]=l[r.format]||[]).push(r),l),{});i.innerHTML=`
    <h2>${n("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${n("JLPT N5 \u3061\u3087\u3046\u304B\u3044\u306E \u4E09\u3064\u306E \u3051\u3044\u3057\u304D\u3002\u304A\u3093\u305B\u3044\u3092 \u805E\u3044\u3066\u3001\u305F\u3060\u3057\u3044 \u3053\u305F\u3048\u3092 \u3048\u3089\u3093\u3067 \u304F\u3060\u3055\u3044\u3002")}</p>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">${n("\u305C\u3093\u3076 \u3072\u3089\u304F")}</button>
      <button type="button" class="btn-secondary toc-collapse-all">${n("\u305C\u3093\u3076 \u3068\u3058\u308B")}</button>
    </div>
    ${Object.entries(u).map(([l,r])=>`
      <details class="listening-section">
        <summary><h3>${n(k[l]||l)} <span class="muted small">(${r.length})</span></h3></summary>
        <ul class="listening-list">
          ${r.map(o=>`<li><button class="listening-pick" data-id="${s(o.id)}">${o.title_ja?n(o.title_ja):s(o.id)}</button></li>`).join("")}
        </ul>
      </details>
    `).join("")}
  `;const c=i.querySelector(".toc-expand-all"),$=i.querySelector(".toc-collapse-all");c&&c.addEventListener("click",()=>{i.querySelectorAll("details.listening-section").forEach(l=>l.open=!0)}),$&&$.addEventListener("click",()=>{i.querySelectorAll("details.listening-section").forEach(l=>l.open=!1)}),i.querySelectorAll("[data-id]").forEach(l=>{l.addEventListener("click",()=>{location.hash=`#/listening/${encodeURIComponent(l.dataset.id)}`})})}function j(i){const e=v.item,u=v.picked,c=u!=null,$=u===e.correctAnswer;c&&L.setListeningCompleted(e.id);const l=p?.items||[],r=l.findIndex(a=>a.id===e.id),o=r>0?l[r-1]:null,g=r>=0&&r<l.length-1?l[r+1]:null,_=o||g?`
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
  `:"";i.innerHTML=`
    <article class="listening-item">
      <div class="srs-progress">
        <span><a id="listening-back" href="#/listening">\u2190 ${n("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</a></span>
      </div>
      <h2>${e.title_ja?n(e.title_ja):s(e.id)}</h2>
      <p class="muted small">${n("\u3051\u3044\u3057\u304D")}: ${n(k[e.format]||e.format)}</p>
      <div class="listening-audio">
        ${e.audio?`
          <audio id="listening-audio-${s(e.id)}" controls preload="none" src="${s(e.audio)}">Audio</audio>
          ${e.audio_slow?`
            <!-- IMP-141 (richness audit, 2026-05-09): slow-version
                 0.7x render. Toggle swaps the <audio> src + label
                 so users can replay at beginner-friendly tempo
                 without losing the original-speed reference. -->
            <div class="listening-speed-toggle" role="group" aria-label="${s(n("\u3055\u3044\u305B\u3044 \u305D\u304F\u3069"))}">
              <button type="button" class="listening-speed-btn is-active" data-listening-speed="normal"
                      data-audio-target="listening-audio-${s(e.id)}"
                      data-audio-normal="${s(e.audio)}"
                      data-audio-slow="${s(e.audio_slow)}">
                ${n("\u3075\u3064\u3046")} (1.0\xD7)
              </button>
              <button type="button" class="listening-speed-btn" data-listening-speed="slow"
                      data-audio-target="listening-audio-${s(e.id)}"
                      data-audio-normal="${s(e.audio)}"
                      data-audio-slow="${s(e.audio_slow)}">
                ${n("\u3086\u3063\u304F\u308A")} (0.7\xD7)
              </button>
            </div>
          `:""}
        `:`<p class="muted small">${n("\u304A\u3093\u305B\u3044\u30D5\u30A1\u30A4\u30EB\u306F \u307E\u3060 \u3042\u308A\u307E\u305B\u3093\u3002")}</p>`}
      </div>
      ${e.voice_planned?(()=>{const a=h=>h?String(h).replace(/^ja-JP-/,"").replace(/Neural$/,""):"",m=a(e.voice_planned.primary),f=a(e.voice_planned.secondary),d=e.voice_planned.engine||"TTS",b=[m,f].filter(Boolean).join(" \xB7 "),y=(typeof t=="function"?t("listening.voices_label"):"Voices")||"Voices";return`<p class="muted xs listening-voice-attribution">
          ${s(y)}: ${s(b)} (${s(d)})
        </p>`})():""}
      ${e.prompt_ja?`<p>${n(e.prompt_ja)}</p>`:""}
      ${e.choices?`
        <div class="choice-grid">
          ${e.choices.map(a=>{let m="choice-button";return c?a===e.correctAnswer?m+=" correct-choice":a===u&&(m+=" wrong-choice"):u===a&&(m+=" selected"),`<button data-pick="${s(a)}" class="${m}" ${c?"disabled":""}>${n(a)}</button>`}).join("")}
        </div>
      `:""}
      ${c?`
        <div class="drill-feedback ${$?"correct":"incorrect"}">
          <div class="feedback-headline">${$?n("\u305B\u3044\u304B\u3044"):n("\u3056\u3093\u306D\u3093")}</div>
          ${E(e)?`<details open><summary>${n("\u30B9\u30AF\u30EA\u30D7\u30C8")}</summary>${S(e)}</details>`:e.script_ja?`<details><summary>${n("\u30B9\u30AF\u30EA\u30D7\u30C8\u3092 \u898B\u308B")}</summary><div>${n(e.script_ja)}</div></details>`:""}
          ${e.explanation_en?`<p class="muted small">${s(e.explanation_en)}</p>`:""}
          <button id="listening-back-list" class="btn-primary">${n("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</button>
        </div>
      `:""}
      ${_}
    </article>
  `,i.querySelector('[data-nav="prev"]')?.addEventListener("click",()=>{o&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(o.id)}`)}),i.querySelector('[data-nav="next"]')?.addEventListener("click",()=>{g&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(g.id)}`)}),i.querySelectorAll("[data-pick]").forEach(a=>{a.addEventListener("click",()=>{v.picked=a.dataset.pick,j(i)})}),document.getElementById("listening-back-list")?.addEventListener("click",()=>{location.hash="#/listening"}),T(i,e),i.querySelectorAll("[data-listening-speed]").forEach(a=>{a.addEventListener("click",()=>{const m=a.dataset.listeningSpeed,f=a.dataset.audioTarget,d=document.getElementById(f);if(!d)return;const b=m==="slow"?a.dataset.audioSlow:a.dataset.audioNormal,y=!d.paused,h=d.duration?d.currentTime/d.duration:0;d.pause(),d.src=b,d.addEventListener("loadedmetadata",()=>{d.duration&&h>0&&(d.currentTime=d.duration*h),y&&d.play().catch(()=>{})},{once:!0}),a.parentElement?.querySelectorAll("[data-listening-speed]").forEach(w=>{w.classList.toggle("is-active",w===a)})})})}function s(i){return String(i??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{M as renderListening};
