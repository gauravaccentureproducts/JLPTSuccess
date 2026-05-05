import{renderJa as s}from"./furigana.js";import*as f from"./storage.js";let l=null,c=null;const g={task:"\u304B\u3060\u3044\u308A\u304B\u3044 (\u30BF\u30B9\u30AF\u308A\u304B\u3044)",point:"\u30DD\u30A4\u30F3\u30C8\u308A\u304B\u3044",utterance:"\u306F\u3064\u308F\u3072\u3087\u3046\u3052\u3093"};async function $(){if(l)return l;try{const i=await fetch("data/listening.json");if(!i.ok)return l={items:[]},l;l=await i.json()}catch{l={items:[]}}return l}async function v(i){return await $(),c?m(i):u(i)}function u(i){const e=l.items||[];if(e.length===0){i.innerHTML=`
      <h2>${s("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
      <div class="placeholder">
        <p><strong>No listening items shipped yet.</strong></p>
        <p>The listening module is wired and will activate as soon as audio assets ship.</p>
        <p class="muted small">For developers: run <code>python tools/build_audio.py</code> to generate MP3 files for every reading passage and listening script. Audio files land in <code>audio/listening/*.mp3</code> and <code>audio/reading/*.mp3</code>; the service worker will cache them on first online visit.</p>
        <p class="muted small">Listening scripts and questions live in <code>data/listening.json</code> (created by the same build).</p>
      </div>
    `;return}const o=e.reduce((t,n)=>((t[n.format]=t[n.format]||[]).push(n),t),{});i.innerHTML=`
    <h2>${s("\u3061\u3087\u3046\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${s("JLPT N5 \u3061\u3087\u3046\u304B\u3044\u306E \u4E09\u3064\u306E \u3051\u3044\u3057\u304D\u3002\u304A\u3093\u305B\u3044\u3092 \u805E\u3044\u3066\u3001\u305F\u3060\u3057\u3044 \u3053\u305F\u3048\u3092 \u3048\u3089\u3093\u3067 \u304F\u3060\u3055\u3044\u3002")}</p>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">${s("\u305C\u3093\u3076 \u3072\u3089\u304F")}</button>
      <button type="button" class="btn-secondary toc-collapse-all">${s("\u305C\u3093\u3076 \u3068\u3058\u308B")}</button>
    </div>
    ${Object.entries(o).map(([t,n])=>`
      <details class="listening-section">
        <summary><h3>${s(g[t]||t)} <span class="muted small">(${n.length})</span></h3></summary>
        <ul class="listening-list">
          ${n.map(d=>`<li><button class="listening-pick" data-id="${r(d.id)}">${d.title_ja?s(d.title_ja):r(d.id)}</button></li>`).join("")}
        </ul>
      </details>
    `).join("")}
  `;const a=i.querySelector(".toc-expand-all"),p=i.querySelector(".toc-collapse-all");a&&a.addEventListener("click",()=>{i.querySelectorAll("details.listening-section").forEach(t=>t.open=!0)}),p&&p.addEventListener("click",()=>{i.querySelectorAll("details.listening-section").forEach(t=>t.open=!1)}),i.querySelectorAll("[data-id]").forEach(t=>{t.addEventListener("click",()=>{c={item:e.find(d=>d.id===t.dataset.id),picked:null},m(i)})})}function m(i){const e=c.item,o=c.picked,a=o!=null,p=o===e.correctAnswer;a&&f.setListeningCompleted(e.id),i.innerHTML=`
    <article class="listening-item">
      <div class="srs-progress">
        <span><a id="listening-back" href="#/listening">\u2190 ${s("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</a></span>
      </div>
      <h2>${e.title_ja?s(e.title_ja):r(e.id)}</h2>
      <p class="muted small">${s("\u3051\u3044\u3057\u304D")}: ${s(g[e.format]||e.format)}</p>
      <div class="listening-audio">
        ${e.audio?`<audio controls preload="none" src="${r(e.audio)}">Audio</audio>`:`<p class="muted small">${s("\u304A\u3093\u305B\u3044\u30D5\u30A1\u30A4\u30EB\u306F \u307E\u3060 \u3042\u308A\u307E\u305B\u3093\u3002")}</p>`}
      </div>
      ${e.prompt_ja?`<p>${s(e.prompt_ja)}</p>`:""}
      ${e.choices?`
        <div class="choice-grid">
          ${e.choices.map(t=>{let n="choice-button";return a?t===e.correctAnswer?n+=" correct-choice":t===o&&(n+=" wrong-choice"):o===t&&(n+=" selected"),`<button data-pick="${r(t)}" class="${n}" ${a?"disabled":""}>${s(t)}</button>`}).join("")}
        </div>
      `:""}
      ${a?`
        <div class="drill-feedback ${p?"correct":"incorrect"}">
          <div class="feedback-headline">${p?s("\u305B\u3044\u304B\u3044"):s("\u3056\u3093\u306D\u3093")}</div>
          ${e.script_ja?`<details><summary>${s("\u30B9\u30AF\u30EA\u30D7\u30C8\u3092 \u898B\u308B")}</summary><div>${s(e.script_ja)}</div></details>`:""}
          ${e.explanation_en?`<p class="muted small">${r(e.explanation_en)}</p>`:""}
          <button id="listening-back-list" class="btn-primary">${s("\u30EA\u30B9\u30C8\u306B \u3082\u3069\u308B")}</button>
        </div>
      `:""}
    </article>
  `,i.querySelectorAll("[data-pick]").forEach(t=>{t.addEventListener("click",()=>{c.picked=t.dataset.pick,m(i)})}),document.getElementById("listening-back")?.addEventListener("click",t=>{t.preventDefault(),c=null,u(i)}),document.getElementById("listening-back-list")?.addEventListener("click",()=>{c=null,u(i)})}function r(i){return String(i??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{v as renderListening};
