import{renderJa as t}from"./furigana.js";import*as l from"./storage.js";const k={easy:"\u3084\u3055\u3057\u3044",medium:"\u3075\u3064\u3046","info-search":"\u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F"},b={"self-introduction":"\u3058\u3053\u3057\u3087\u3046\u304B\u3044","daily routine":"\u307E\u3044\u306B\u3061\u306E \u305B\u3044\u304B\u3064","weekend plan":"\u3057\u3085\u3046\u307E\u3064\u306E \u3088\u3066\u3044",weekend:"\u3057\u3085\u3046\u307E\u3064",shopping:"\u304B\u3044\u3082\u306E",family:"\u304B\u305E\u304F",weather:"\u3066\u3093\u304D",schedule:"\u3088\u3066\u3044",transport:"\u3053\u3046\u3064\u3046",hobby:"\u3057\u3085\u307F",school:"\u5B66\u6821",food:"\u305F\u3079\u3082\u306E",travel:"\u308A\u3087\u3053\u3046",health:"\u3051\u3093\u3053\u3046",study:"\u3079\u3093\u304D\u3087\u3046",people:"\u3072\u3068",request:"\u304A\u306D\u304C\u3044",room:"\u3078\u3084",directions:"\u307F\u3061\u3042\u3093\u306A\u3044"};let c=null,o=null;async function y(){return c||(c=await(await fetch("data/reading.json")).json(),c)}function x(s){o={passage:!!(typeof l<"u"&&l.getSettings?l.getSettings():{}).readingMockTestMode?{...s,questions:(s.questions||[]).filter(a=>a.format_role==="primary"||!a.format_role)}:s,phase:"read",answers:{},idx:0}}async function q(s,e){await y();const d=e?decodeURIComponent(e):"";if(d){const a=(c.passages||[]).find(n=>n.id===d);if(a)return(!o||o.passage?.id!==a.id)&&x(a),v(s)}return o?v(s):f(s)}function f(s){const e=c.passages||[],i=!!(typeof l<"u"&&l.getSettings?l.getSettings():{}).readingMockTestMode,a=e.map(n=>`
      <li>
        <button class="reading-pick" data-id="${u(n.id)}">
          <span class="reading-title"><strong>${t(n.title_ja)}</strong></span>
        </button>
      </li>
    `).join("");s.innerHTML=`
    <h2>${t("\u3069\u3063\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${t("\u307F\u3058\u304B\u3044 JLPT \u3051\u3044\u3057\u304D\u306E \u3076\u3093\u3057\u3087\u3046\u3068 \u3057\u3064\u3082\u3093\u3067\u3059\u3002")} ${e.length} ${t("\u3076\u3093\u3057\u3087\u3046\u304C \u3042\u308A\u307E\u3059\u3002\u3084\u3055\u3057\u3044 \u2192 \u3075\u3064\u3046 \u2192 \u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F \u306E \u3058\u3085\u3093\u306B \u306A\u3089\u3093\u3067 \u3044\u307E\u3059\u3002")}</p>
    <label class="reading-mode-toggle">
      <input type="checkbox" id="reading-mock-mode" ${i?"checked":""}>
      <span>${t("\u3082\u304E\u30C6\u30B9\u30C8\u30E2\u30FC\u30C9")} (primary questions only - matches official JLPT N5 distribution)</span>
    </label>
    <ul class="reading-list">${a}</ul>
  `,document.getElementById("reading-mock-mode").addEventListener("change",n=>{l.setSettings({readingMockTestMode:n.target.checked}),f(s)}),s.querySelectorAll("[data-id]").forEach(n=>{n.addEventListener("click",()=>{location.hash=`#/reading/${encodeURIComponent(n.dataset.id)}`})})}function v(s){const e=o.passage;return o.phase==="read"?_(s,e):o.phase==="questions"?$(s,e):h(s,e)}function _(s,e){const d=c?.passages||[],i=d.findIndex(g=>g.id===e.id),a=i>0?d[i-1]:null,n=i>=0&&i<d.length-1?d[i+1]:null,p=`
    <nav class="reading-nav" aria-label="Passage navigation">
      ${a?`<a href="#/reading/${encodeURIComponent(a.id)}" title="${u(a.title_ja||a.id)}">\u2190 <span lang="ja">${t(a.title_ja||a.id)}</span></a>`:"<span></span>"}
      ${n?`<a href="#/reading/${encodeURIComponent(n.id)}" title="${u(n.title_ja||n.id)}"><span lang="ja">${t(n.title_ja||n.id)}</span> \u2192</a>`:"<span></span>"}
    </nav>
  `;s.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span><a href="#/reading" id="reading-back">\u2190 ${t("\u3082\u3069\u308B")}</a> \u30FB ${t("\u3076\u3093\u3057\u3087\u3046\u3092 \u8AAD\u3093\u3067\u3001\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u3066 \u304F\u3060\u3055\u3044\u3002")}</span>
      </div>
      <h2>${t(e.title_ja)}</h2>
      <p class="muted small">\u30EC\u30D9\u30EB: ${t(k[e.level]||e.level)} \u30FB \u30C8\u30D4\u30C3\u30AF: ${t(b[e.topic]||e.topic)}</p>
      <div class="passage-text">${t(e.ja)}</div>
      ${e.cultural_context?`
        <aside class="reading-cultural-context">
          <p class="muted small"><strong>Cultural context:</strong> ${u(e.cultural_context)}</p>
        </aside>
      `:""}
      ${e.audio?`
        <div class="reading-audio">
          <p class="muted small">${t("\u304A\u3093\u305B\u3044 (\u3042\u308B \u3068\u304D):")}</p>
          <audio controls preload="none" src="${u(e.audio)}">Your browser does not support audio.</audio>
        </div>
      `:""}
      <button id="reading-start-q" class="btn-primary">${t("\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u308B")} (${e.questions.length})</button>
      ${p}
    </article>
  `,document.getElementById("reading-back").addEventListener("click",g=>{g.preventDefault(),o=null,location.hash="#/reading"}),document.getElementById("reading-start-q").addEventListener("click",()=>{o.phase="questions",$(s,e)})}function $(s,e){const d=e.questions.length,i=o.idx,a=e.questions[i],n=o.answers[a.id],p=n!=null,g=n===a.correctAnswer;s.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span>${t(e.title_ja)} \u30FB ${t("\u3082\u3093\u3060\u3044")} ${i+1} / ${d}</span>
      </div>
      <details class="passage-recap">
        <summary>${t("\u3076\u3093\u3057\u3087\u3046\u3092 \u898B\u308B")}</summary>
        <div class="passage-text">${t(e.ja)}</div>
      </details>
      <div class="question-card">
        <p class="question">${t(a.prompt_ja)}</p>
        <div class="choice-grid">
          ${a.choices.map(r=>{let m="choice-button";return p?r===a.correctAnswer?m+=" correct-choice":r===n&&(m+=" wrong-choice"):n===r&&(m+=" selected"),`<button data-pick="${u(r)}" class="${m}" ${p?"disabled":""}>${t(r)}</button>`}).join("")}
        </div>
        ${p?`
          <div class="drill-feedback ${g?"correct":"incorrect"}">
            <div class="feedback-headline">${g?t("\u305B\u3044\u304B\u3044"):t("\u3056\u3093\u306D\u3093")}</div>
            ${a.explanation_en?`<p class="muted small">${u(a.explanation_en)}</p>`:""}
            <button id="reading-next" class="btn-primary">${i===d-1?t("\u304A\u308F\u308A"):t("\u3064\u304E\u306E \u3057\u3064\u3082\u3093")}</button>
          </div>
        `:""}
      </div>
    </article>
  `,s.querySelectorAll("[data-pick]").forEach(r=>{r.addEventListener("click",()=>{o.answers[a.id]=r.dataset.pick,$(s,e)})}),document.getElementById("reading-next")?.addEventListener("click",()=>{i===d-1?(o.phase="results",h(s,e)):(o.idx+=1,$(s,e))})}function h(s,e){const d=e.questions.length,i=e.questions.filter(n=>o.answers[n.id]===n.correctAnswer).length,a=Math.round(i/d*100);i>0&&l.setReadingCompleted(e.id),s.innerHTML=`
    <div class="reading-results">
      <h2>${t(e.title_ja)} \u30FB ${t("\u3051\u3063\u304B")}</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${i}/${d}</div><div class="stat-label">${t("\u30B9\u30B3\u30A2")}</div></div>
        <div class="stat-card ${a>=70?"mastered":"weak"}"><div class="stat-num">${a}%</div><div class="stat-label">${t("\u305B\u3044\u304B\u3044\u308A\u3064")}</div></div>
      </section>
      <div class="test-nav">
        <button id="reading-back-list" class="btn-primary">${t("\u307B\u304B\u306E \u3076\u3093\u3057\u3087\u3046\u3092 \u3048\u3089\u3076")}</button>
      </div>
    </div>
  `,document.getElementById("reading-back-list").addEventListener("click",()=>{o=null,f(s)})}function u(s){return String(s??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{q as renderReading};
