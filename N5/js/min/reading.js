import{renderJa as s}from"./furigana.js";import*as c from"./storage.js";const v={easy:"\u3084\u3055\u3057\u3044",medium:"\u3075\u3064\u3046","info-search":"\u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F"},h={"self-introduction":"\u3058\u3053\u3057\u3087\u3046\u304B\u3044","daily routine":"\u307E\u3044\u306B\u3061\u306E \u305B\u3044\u304B\u3064","weekend plan":"\u3057\u3085\u3046\u307E\u3064\u306E \u3088\u3066\u3044",weekend:"\u3057\u3085\u3046\u307E\u3064",shopping:"\u304B\u3044\u3082\u306E",family:"\u304B\u305E\u304F",weather:"\u3066\u3093\u304D",schedule:"\u3088\u3066\u3044",transport:"\u3053\u3046\u3064\u3046",hobby:"\u3057\u3085\u307F",school:"\u5B66\u6821",food:"\u305F\u3079\u3082\u306E",travel:"\u308A\u3087\u3053\u3046",health:"\u3051\u3093\u3053\u3046",study:"\u3079\u3093\u304D\u3087\u3046",people:"\u3072\u3068",request:"\u304A\u306D\u304C\u3044",room:"\u3078\u3084",directions:"\u307F\u3061\u3042\u3093\u306A\u3044"};let p=null,o=null;async function y(){return p||(p=await(await fetch("data/reading.json")).json(),p)}function q(t){o={passage:!!(typeof c<"u"&&c.getSettings?c.getSettings():{}).readingMockTestMode?{...t,questions:(t.questions||[]).filter(n=>n.format_role==="primary"||!n.format_role)}:t,phase:"read",answers:{},idx:0}}async function w(t,e){await y();const d=e?decodeURIComponent(e):"";if(d){const n=(p.passages||[]).find(a=>a.id===d);if(n)return(!o||o.passage?.id!==n.id)&&q(n),k(t)}return o?k(t):f(t)}function f(t){const e=p.passages||[],i=!!(typeof c<"u"&&c.getSettings?c.getSettings():{}).readingMockTestMode,n=e.map(a=>{const u=(a.questions||[]).length,l=(a.questions||[]).filter(g=>g.format_role==="primary"||!g.format_role).length,r=i?l:u;return`
      <li>
        <button class="reading-pick" data-id="${m(a.id)}">
          <span class="reading-title"><strong>${s(a.title_ja)}</strong> <span class="muted small">(${s(v[a.level]||a.level)})</span></span>
          <span class="muted small">${s(h[a.topic]||a.topic)} \u30FB ${r} ${s("\u3082\u3093")}</span>
        </button>
      </li>
    `}).join("");t.innerHTML=`
    <h2>${s("\u3069\u3063\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${s("\u307F\u3058\u304B\u3044 JLPT \u3051\u3044\u3057\u304D\u306E \u3076\u3093\u3057\u3087\u3046\u3068 \u3057\u3064\u3082\u3093\u3067\u3059\u3002")} ${e.length} ${s("\u3076\u3093\u3057\u3087\u3046\u304C \u3042\u308A\u307E\u3059\u3002\u3084\u3055\u3057\u3044 \u2192 \u3075\u3064\u3046 \u2192 \u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F \u306E \u3058\u3085\u3093\u306B \u306A\u3089\u3093\u3067 \u3044\u307E\u3059\u3002")}</p>
    <label class="reading-mode-toggle">
      <input type="checkbox" id="reading-mock-mode" ${i?"checked":""}>
      <span>${s("\u3082\u304E\u30C6\u30B9\u30C8\u30E2\u30FC\u30C9")} (primary questions only \u2014 matches official JLPT N5 distribution)</span>
    </label>
    <ul class="reading-list">${n}</ul>
  `,document.getElementById("reading-mock-mode").addEventListener("change",a=>{c.setSettings({readingMockTestMode:a.target.checked}),f(t)}),t.querySelectorAll("[data-id]").forEach(a=>{a.addEventListener("click",()=>{location.hash=`#/reading/${encodeURIComponent(a.dataset.id)}`})})}function k(t){const e=o.passage;return o.phase==="read"?_(t,e):o.phase==="questions"?$(t,e):b(t,e)}function _(t,e){const d=p?.passages||[],i=d.findIndex(l=>l.id===e.id),n=i>0?d[i-1]:null,a=i>=0&&i<d.length-1?d[i+1]:null,u=`
    <nav class="reading-nav" aria-label="Passage navigation">
      ${n?`<a href="#/reading/${encodeURIComponent(n.id)}" title="${m(n.title_ja||n.id)}">\u2190 <span lang="ja">${s(n.title_ja||n.id)}</span></a>`:"<span></span>"}
      ${a?`<a href="#/reading/${encodeURIComponent(a.id)}" title="${m(a.title_ja||a.id)}"><span lang="ja">${s(a.title_ja||a.id)}</span> \u2192</a>`:"<span></span>"}
    </nav>
  `;t.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span><a href="#/reading" id="reading-back">\u2190 ${s("\u3082\u3069\u308B")}</a> \u30FB ${s("\u3076\u3093\u3057\u3087\u3046\u3092 \u8AAD\u3093\u3067\u3001\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u3066 \u304F\u3060\u3055\u3044\u3002")}</span>
      </div>
      <h2>${s(e.title_ja)}</h2>
      <p class="muted small">\u30EC\u30D9\u30EB: ${s(v[e.level]||e.level)} \u30FB \u30C8\u30D4\u30C3\u30AF: ${s(h[e.topic]||e.topic)}</p>
      <div class="passage-text">${s(e.ja)}</div>
      ${e.audio?`
        <div class="reading-audio">
          <p class="muted small">${s("\u304A\u3093\u305B\u3044 (\u3042\u308B \u3068\u304D):")}</p>
          <audio controls preload="none" src="${m(e.audio)}">Your browser does not support audio.</audio>
        </div>
      `:""}
      <button id="reading-start-q" class="btn-primary">${s("\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u308B")} (${e.questions.length})</button>
      ${u}
    </article>
  `,document.getElementById("reading-back").addEventListener("click",l=>{l.preventDefault(),o=null,location.hash="#/reading"}),document.getElementById("reading-start-q").addEventListener("click",()=>{o.phase="questions",$(t,e)})}function $(t,e){const d=e.questions.length,i=o.idx,n=e.questions[i],a=o.answers[n.id],u=a!=null,l=a===n.correctAnswer;t.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span>${s(e.title_ja)} \u30FB ${s("\u3082\u3093\u3060\u3044")} ${i+1} / ${d}</span>
      </div>
      <details class="passage-recap">
        <summary>${s("\u3076\u3093\u3057\u3087\u3046\u3092 \u898B\u308B")}</summary>
        <div class="passage-text">${s(e.ja)}</div>
      </details>
      <div class="question-card">
        <p class="question">${s(n.prompt_ja)}</p>
        <div class="choice-grid">
          ${n.choices.map(r=>{let g="choice-button";return u?r===n.correctAnswer?g+=" correct-choice":r===a&&(g+=" wrong-choice"):a===r&&(g+=" selected"),`<button data-pick="${m(r)}" class="${g}" ${u?"disabled":""}>${s(r)}</button>`}).join("")}
        </div>
        ${u?`
          <div class="drill-feedback ${l?"correct":"incorrect"}">
            <div class="feedback-headline">${l?s("\u305B\u3044\u304B\u3044"):s("\u3056\u3093\u306D\u3093")}</div>
            ${n.explanation_en?`<p class="muted small">${m(n.explanation_en)}</p>`:""}
            <button id="reading-next" class="btn-primary">${i===d-1?s("\u304A\u308F\u308A"):s("\u3064\u304E\u306E \u3057\u3064\u3082\u3093")}</button>
          </div>
        `:""}
      </div>
    </article>
  `,t.querySelectorAll("[data-pick]").forEach(r=>{r.addEventListener("click",()=>{o.answers[n.id]=r.dataset.pick,$(t,e)})}),document.getElementById("reading-next")?.addEventListener("click",()=>{i===d-1?(o.phase="results",b(t,e)):(o.idx+=1,$(t,e))})}function b(t,e){const d=e.questions.length,i=e.questions.filter(a=>o.answers[a.id]===a.correctAnswer).length,n=Math.round(i/d*100);i>0&&c.setReadingCompleted(e.id),t.innerHTML=`
    <div class="reading-results">
      <h2>${s(e.title_ja)} \u30FB ${s("\u3051\u3063\u304B")}</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${i}/${d}</div><div class="stat-label">${s("\u30B9\u30B3\u30A2")}</div></div>
        <div class="stat-card ${n>=70?"mastered":"weak"}"><div class="stat-num">${n}%</div><div class="stat-label">${s("\u305B\u3044\u304B\u3044\u308A\u3064")}</div></div>
      </section>
      <div class="test-nav">
        <button id="reading-back-list" class="btn-primary">${s("\u307B\u304B\u306E \u3076\u3093\u3057\u3087\u3046\u3092 \u3048\u3089\u3076")}</button>
      </div>
    </div>
  `,document.getElementById("reading-back-list").addEventListener("click",()=>{o=null,f(t)})}function m(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{w as renderReading};
