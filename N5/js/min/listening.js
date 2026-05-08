import{renderJa as n}from"./furigana.js";import*as f from"./storage.js";import{hasAlignedTranscript as b,renderTranscriptHTML as y,wireTranscriptSync as k}from"./listening-transcript.js";let c=null,u=null;const v={task:"\u304B\u3060\u3044\u308A\u304B\u3044 (\u30BF\u30B9\u30AF\u308A\u304B\u3044)",point:"\u30DD\u30A4\u30F3\u30C8\u308A\u304B\u3044",utterance:"\u306F\u3064\u308F\u3072\u3087\u3046\u3052\u3093",response:"\u305D\u304F\u3058\u304A\u3046\u3068\u3046"};async function j(){if(c)return c;try{const t=await fetch("data/listening.json");if(!t.ok)return c={items:[]},c;c=await t.json()}catch{c={items:[]}}return c}async function E(t,e){await j();const d=(e||"").trim();if(d){const l=(c.items||[]).find(m=>m.id===d);if(!l){u=null,location.hash="#/listening";return}return(!u||u.item?.id!==l.id)&&(u={item:l,picked:null}),h(t)}return u=null,w(t)}function w(t){const e=c.items||[];if(e.length===0){t.innerHTML=`
      <h2>${n("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
      <div class="placeholder">
        <p><strong>No listening items shipped yet.</strong></p>
        <p>The listening module is wired and will activate as soon as audio assets ship.</p>
        <p class="muted small">For developers: run <code>python tools/build_audio.py</code> to generate MP3 files for every reading passage and listening script. Audio files land in <code>audio/listening/*.mp3</code> and <code>audio/reading/*.mp3</code>; the service worker will cache them on first online visit.</p>
        <p class="muted small">Listening scripts and questions live in <code>data/listening.json</code> (created by the same build).</p>
      </div>
    `;return}const d=e.reduce((i,a)=>((i[a.format]=i[a.format]||[]).push(a),i),{});t.innerHTML=`
    <h2>${n("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${n("JLPT N5 \u3061\u3087\u3046\u304B\u3044\u306E \u4E09\u3064\u306E \u3051\u3044\u3057\u304D\u3002\u304A\u3093\u305B\u3044\u3092 \u805E\u3044\u3066\u3001\u305F\u3060\u3057\u3044 \u3053\u305F\u3048\u3092 \u3048\u3089\u3093\u3067 \u304F\u3060\u3055\u3044\u3002")}</p>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">${n("\u305C\u3093\u3076 \u3072\u3089\u304F")}</button>
      <button type="button" class="btn-secondary toc-collapse-all">${n("\u305C\u3093\u3076 \u3068\u3058\u308B")}</button>
    </div>
    ${Object.entries(d).map(([i,a])=>`
      <details class="listening-section">
        <summary><h3>${n(v[i]||i)} <span class="muted small">(${a.length})</span></h3></summary>
        <ul class="listening-list">
          ${a.map(s=>`<li><button class="listening-pick" data-id="${r(s.id)}">${s.title_ja?n(s.title_ja):r(s.id)}</button></li>`).join("")}
        </ul>
      </details>
    `).join("")}
  `;const l=t.querySelector(".toc-expand-all"),m=t.querySelector(".toc-collapse-all");l&&l.addEventListener("click",()=>{t.querySelectorAll("details.listening-section").forEach(i=>i.open=!0)}),m&&m.addEventListener("click",()=>{t.querySelectorAll("details.listening-section").forEach(i=>i.open=!1)}),t.querySelectorAll("[data-id]").forEach(i=>{i.addEventListener("click",()=>{location.hash=`#/listening/${encodeURIComponent(i.dataset.id)}`})})}function h(t){const e=u.item,d=u.picked,l=d!=null,m=d===e.correctAnswer;l&&f.setListeningCompleted(e.id);const i=c?.items||[],a=i.findIndex(o=>o.id===e.id),s=a>0?i[a-1]:null,p=a>=0&&a<i.length-1?i[a+1]:null,$=s||p?`
    <nav class="listening-nav" aria-label="Listening item navigation">
      ${s?`<button type="button" class="listening-nav-btn listening-nav-prev" data-nav="prev" title="${r(s.title_ja||s.id)}">
             <span class="listening-nav-arrow" aria-hidden="true">&larr;</span>
             <span class="listening-nav-meta">
               <span class="listening-nav-label muted small">${n("\u307E\u3048")}</span>
               <span class="listening-nav-name" lang="ja">${s.title_ja?n(s.title_ja):r(s.id)}</span>
             </span>
           </button>`:'<span class="listening-nav-btn listening-nav-empty" aria-hidden="true"></span>'}
      ${p?`<button type="button" class="listening-nav-btn listening-nav-next" data-nav="next" title="${r(p.title_ja||p.id)}">
             <span class="listening-nav-meta">
               <span class="listening-nav-label muted small">${n("\u3064\u304E")}</span>
               <span class="listening-nav-name" lang="ja">${p.title_ja?n(p.title_ja):r(p.id)}</span>
             </span>
             <span class="listening-nav-arrow" aria-hidden="true">&rarr;</span>
           </button>`:'<span class="listening-nav-btn listening-nav-empty" aria-hidden="true"></span>'}
    </nav>
  `:"";t.innerHTML=`
    <article class="listening-item">
      <div class="srs-progress">
        <span><a id="listening-back" href="#/listening">\u2190 ${n("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</a></span>
      </div>
      <h2>${e.title_ja?n(e.title_ja):r(e.id)}</h2>
      <p class="muted small">${n("\u3051\u3044\u3057\u304D")}: ${n(v[e.format]||e.format)}</p>
      <div class="listening-audio">
        ${e.audio?`<audio controls preload="none" src="${r(e.audio)}">Audio</audio>`:`<p class="muted small">${n("\u304A\u3093\u305B\u3044\u30D5\u30A1\u30A4\u30EB\u306F \u307E\u3060 \u3042\u308A\u307E\u305B\u3093\u3002")}</p>`}
      </div>
      ${e.prompt_ja?`<p>${n(e.prompt_ja)}</p>`:""}
      ${e.choices?`
        <div class="choice-grid">
          ${e.choices.map(o=>{let g="choice-button";return l?o===e.correctAnswer?g+=" correct-choice":o===d&&(g+=" wrong-choice"):d===o&&(g+=" selected"),`<button data-pick="${r(o)}" class="${g}" ${l?"disabled":""}>${n(o)}</button>`}).join("")}
        </div>
      `:""}
      ${l?`
        <div class="drill-feedback ${m?"correct":"incorrect"}">
          <div class="feedback-headline">${m?n("\u305B\u3044\u304B\u3044"):n("\u3056\u3093\u306D\u3093")}</div>
          ${b(e)?`<details open><summary>${n("\u30B9\u30AF\u30EA\u30D7\u30C8")}</summary>${y(e)}</details>`:e.script_ja?`<details><summary>${n("\u30B9\u30AF\u30EA\u30D7\u30C8\u3092 \u898B\u308B")}</summary><div>${n(e.script_ja)}</div></details>`:""}
          ${e.explanation_en?`<p class="muted small">${r(e.explanation_en)}</p>`:""}
          <button id="listening-back-list" class="btn-primary">${n("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</button>
        </div>
      `:""}
      ${$}
    </article>
  `,t.querySelector('[data-nav="prev"]')?.addEventListener("click",()=>{s&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(s.id)}`)}),t.querySelector('[data-nav="next"]')?.addEventListener("click",()=>{p&&(window.scrollTo(0,0),location.hash=`#/listening/${encodeURIComponent(p.id)}`)}),t.querySelectorAll("[data-pick]").forEach(o=>{o.addEventListener("click",()=>{u.picked=o.dataset.pick,h(t)})}),document.getElementById("listening-back-list")?.addEventListener("click",()=>{location.hash="#/listening"}),k(t,e)}function r(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{E as renderListening};
