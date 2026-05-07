import{renderJa as n}from"./furigana.js";import*as p from"./storage.js";const k={easy:"\u3084\u3055\u3057\u3044",medium:"\u3075\u3064\u3046","info-search":"\u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F"},b={"self-introduction":"\u3058\u3053\u3057\u3087\u3046\u304B\u3044","daily routine":"\u307E\u3044\u306B\u3061\u306E \u305B\u3044\u304B\u3064","weekend plan":"\u3057\u3085\u3046\u307E\u3064\u306E \u3088\u3066\u3044",weekend:"\u3057\u3085\u3046\u307E\u3064",shopping:"\u304B\u3044\u3082\u306E",family:"\u304B\u305E\u304F",weather:"\u3066\u3093\u304D",schedule:"\u3088\u3066\u3044",transport:"\u3053\u3046\u3064\u3046",hobby:"\u3057\u3085\u307F",school:"\u5B66\u6821",food:"\u305F\u3079\u3082\u306E",travel:"\u308A\u3087\u3053\u3046",health:"\u3051\u3093\u3053\u3046",study:"\u3079\u3093\u304D\u3087\u3046",people:"\u3072\u3068",request:"\u304A\u306D\u304C\u3044",room:"\u3078\u3084",directions:"\u307F\u3061\u3042\u3093\u306A\u3044"};let m=null,r=null;async function y(){return m||(m=await(await fetch("data/reading.json")).json(),m)}function _(t){r={passage:!!(typeof p<"u"&&p.getSettings?p.getSettings():{}).readingMockTestMode?{...t,questions:(t.questions||[]).filter(a=>a.format_role==="primary"||!a.format_role)}:t,phase:"read",answers:{},idx:0}}async function q(t,e){await y();const o=e?decodeURIComponent(e):"";if(o){const a=(m.passages||[]).find(s=>s.id===o);if(a)return(!r||r.passage?.id!==a.id)&&_(a),h(t)}return r?h(t):$(t)}function $(t){const e=m.passages||[],i=!!(typeof p<"u"&&p.getSettings?p.getSettings():{}).readingMockTestMode,a=e.map(s=>`
      <li>
        <button class="reading-pick" data-id="${l(s.id)}">
          <span class="reading-title"><strong>${n(s.title_ja)}</strong></span>
        </button>
      </li>
    `).join("");t.innerHTML=`
    <h2>${n("\u3069\u3063\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${n("\u307F\u3058\u304B\u3044 JLPT \u3051\u3044\u3057\u304D\u306E \u3076\u3093\u3057\u3087\u3046\u3068 \u3057\u3064\u3082\u3093\u3067\u3059\u3002")} ${e.length} ${n("\u3076\u3093\u3057\u3087\u3046\u304C \u3042\u308A\u307E\u3059\u3002\u3084\u3055\u3057\u3044 \u2192 \u3075\u3064\u3046 \u2192 \u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F \u306E \u3058\u3085\u3093\u306B \u306A\u3089\u3093\u3067 \u3044\u307E\u3059\u3002")}</p>
    <label class="reading-mode-toggle">
      <input type="checkbox" id="reading-mock-mode" ${i?"checked":""}>
      <span>${n("\u3082\u304E\u30C6\u30B9\u30C8\u30E2\u30FC\u30C9")} (primary questions only - matches official JLPT N5 distribution)</span>
    </label>
    <ul class="reading-list">${a}</ul>
  `,document.getElementById("reading-mock-mode").addEventListener("change",s=>{p.setSettings({readingMockTestMode:s.target.checked}),$(t)}),t.querySelectorAll("[data-id]").forEach(s=>{s.addEventListener("click",()=>{location.hash=`#/reading/${encodeURIComponent(s.dataset.id)}`})})}function h(t){const e=r.passage;return r.phase==="read"?j(t,e):r.phase==="questions"?f(t,e):v(t,e)}function j(t,e){const o=m?.passages||[],i=o.findIndex(g=>g.id===e.id),a=i>0?o[i-1]:null,s=i>=0&&i<o.length-1?o[i+1]:null,d=`
    <nav class="reading-nav" aria-label="Passage navigation">
      ${a?`<a href="#/reading/${encodeURIComponent(a.id)}" title="${l(a.title_ja||a.id)}">\u2190 <span lang="ja">${n(a.title_ja||a.id)}</span></a>`:"<span></span>"}
      ${s?`<a href="#/reading/${encodeURIComponent(s.id)}" title="${l(s.title_ja||s.id)}"><span lang="ja">${n(s.title_ja||s.id)}</span> \u2192</a>`:"<span></span>"}
    </nav>
  `;t.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span><a href="#/reading" id="reading-back">\u2190 ${n("\u3082\u3069\u308B")}</a> \u30FB ${n("\u3076\u3093\u3057\u3087\u3046\u3092 \u8AAD\u3093\u3067\u3001\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u3066 \u304F\u3060\u3055\u3044\u3002")}</span>
      </div>
      <h2>${n(e.title_ja)}</h2>
      <p class="muted small">\u30EC\u30D9\u30EB: ${n(k[e.level]||e.level)} \u30FB \u30C8\u30D4\u30C3\u30AF: ${n(b[e.topic]||e.topic)}</p>
      <div class="passage-text">${n(e.ja)}</div>
      ${e.cultural_context?`
        <aside class="reading-cultural-context">
          <p class="muted small"><strong>Cultural context:</strong> ${l(e.cultural_context)}</p>
        </aside>
      `:""}
      ${w(e)}
      ${e.audio?`
        <div class="reading-audio">
          <p class="muted small">${n("\u304A\u3093\u305B\u3044 (\u3042\u308B \u3068\u304D):")}</p>
          <audio controls preload="none" src="${l(e.audio)}">Your browser does not support audio.</audio>
        </div>
      `:""}
      <button id="reading-start-q" class="btn-primary">${n("\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u308B")} (${e.questions.length})</button>
      ${d}
    </article>
  `,document.getElementById("reading-back").addEventListener("click",g=>{g.preventDefault(),r=null,location.hash="#/reading"}),document.getElementById("reading-start-q").addEventListener("click",()=>{r.phase="questions",f(t,e)})}function f(t,e){const o=e.questions.length,i=r.idx,a=e.questions[i],s=r.answers[a.id],d=s!=null,g=s===a.correctAnswer;t.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span>${n(e.title_ja)} \u30FB ${n("\u3082\u3093\u3060\u3044")} ${i+1} / ${o}</span>
      </div>
      <details class="passage-recap">
        <summary>${n("\u3076\u3093\u3057\u3087\u3046\u3092 \u898B\u308B")}</summary>
        <div class="passage-text">${n(e.ja)}</div>
      </details>
      <div class="question-card">
        <p class="question">${n(a.prompt_ja)}</p>
        <div class="choice-grid">
          ${a.choices.map(c=>{let u="choice-button";return d?c===a.correctAnswer?u+=" correct-choice":c===s&&(u+=" wrong-choice"):s===c&&(u+=" selected"),`<button data-pick="${l(c)}" class="${u}" ${d?"disabled":""}>${n(c)}</button>`}).join("")}
        </div>
        ${d?`
          <div class="drill-feedback ${g?"correct":"incorrect"}">
            <div class="feedback-headline">${g?n("\u305B\u3044\u304B\u3044"):n("\u3056\u3093\u306D\u3093")}</div>
            ${a.explanation_en?`<p class="muted small">${l(a.explanation_en)}</p>`:""}
            <button id="reading-next" class="btn-primary">${i===o-1?n("\u304A\u308F\u308A"):n("\u3064\u304E\u306E \u3057\u3064\u3082\u3093")}</button>
          </div>
        `:""}
      </div>
    </article>
  `,t.querySelectorAll("[data-pick]").forEach(c=>{c.addEventListener("click",()=>{r.answers[a.id]=c.dataset.pick,f(t,e)})}),document.getElementById("reading-next")?.addEventListener("click",()=>{i===o-1?(r.phase="results",v(t,e)):(r.idx+=1,f(t,e))})}function v(t,e){const o=e.questions.length,i=e.questions.filter(s=>r.answers[s.id]===s.correctAnswer).length,a=Math.round(i/o*100);i>0&&p.setReadingCompleted(e.id),t.innerHTML=`
    <div class="reading-results">
      <h2>${n(e.title_ja)} \u30FB ${n("\u3051\u3063\u304B")}</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${i}/${o}</div><div class="stat-label">${n("\u30B9\u30B3\u30A2")}</div></div>
        <div class="stat-card ${a>=70?"mastered":"weak"}"><div class="stat-num">${a}%</div><div class="stat-label">${n("\u305B\u3044\u304B\u3044\u308A\u3064")}</div></div>
      </section>
      <div class="test-nav">
        <button id="reading-back-list" class="btn-primary">${n("\u307B\u304B\u306E \u3076\u3093\u3057\u3087\u3046\u3092 \u3048\u3089\u3076")}</button>
      </div>
    </div>
  `,document.getElementById("reading-back-list").addEventListener("click",()=>{r=null,$(t)})}function l(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}function w(t){const e=Array.isArray(t.grammar_footnotes)?t.grammar_footnotes:[];if(e.length===0)return"";const o=(t.ja||"").split("\u3002").filter(s=>s.trim()).map(s=>s.trim()),i=new Map;for(const s of e){const d=s.sentence_index??0;i.has(d)||i.set(d,[]),i.get(d).push(s)}const a=[...i.entries()].sort((s,d)=>s[0]-d[0]).map(([s,d])=>{const g=(o[s]||"").slice(0,50)+(o[s]&&o[s].length>50?"\u2026":"\u3002"),c=d.map(u=>`
      <li class="reading-footnote-item">
        <a class="reading-footnote-pid" href="#/learn/${l(u.pattern_id)}" title="Open ${l(u.pattern_id)} in Learn">${l(u.pattern_id)}</a>
        <span class="reading-footnote-note">${l(u.note||"")}</span>
      </li>
    `).join("");return`
      <li class="reading-footnote-group">
        <p class="reading-footnote-sentence" lang="ja">
          <span class="muted small">Sentence ${s+1}:</span> ${l(g)}
        </p>
        <ul class="reading-footnote-list">${c}</ul>
      </li>
    `}).join("");return`
    <details class="reading-grammar-footnotes">
      <summary><strong>Grammar footnotes</strong> <span class="muted small">\u2014 ${e.length} note${e.length===1?"":"s"} across ${i.size} sentence${i.size===1?"":"s"}</span></summary>
      <ol class="reading-footnote-groups">${a}</ol>
    </details>
  `}export{q as renderReading};
