import{renderJa as a}from"./furigana.js";import*as p from"./storage.js";const y={easy:"\u3084\u3055\u3057\u3044",medium:"\u3075\u3064\u3046","info-search":"\u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F"},k={"self-introduction":"\u3058\u3053\u3057\u3087\u3046\u304B\u3044","daily routine":"\u307E\u3044\u306B\u3061\u306E \u305B\u3044\u304B\u3064","weekend plan":"\u3057\u3085\u3046\u307E\u3064\u306E \u3088\u3066\u3044",weekend:"\u3057\u3085\u3046\u307E\u3064",shopping:"\u304B\u3044\u3082\u306E",family:"\u304B\u305E\u304F",weather:"\u3066\u3093\u304D",schedule:"\u3088\u3066\u3044",transport:"\u3053\u3046\u3064\u3046",hobby:"\u3057\u3085\u307F",school:"\u5B66\u6821",food:"\u305F\u3079\u3082\u306E",travel:"\u308A\u3087\u3053\u3046",health:"\u3051\u3093\u3053\u3046",study:"\u3079\u3093\u304D\u3087\u3046",people:"\u3072\u3068",request:"\u304A\u306D\u304C\u3044",room:"\u3078\u3084",directions:"\u307F\u3061\u3042\u3093\u306A\u3044"};let m=null,o=null;async function b(){return m||(m=await(await fetch("data/reading.json")).json(),m)}function _(t){o={passage:!!(typeof p<"u"&&p.getSettings?p.getSettings():{}).readingMockTestMode?{...t,questions:(t.questions||[]).filter(n=>n.format_role==="primary"||!n.format_role)}:t,phase:"read",answers:{},idx:0}}async function E(t,e){await b();const r=e?decodeURIComponent(e):"";if(r){const n=(m.passages||[]).find(s=>s.id===r);if(n)return(!o||o.passage?.id!==n.id)&&_(n),h(t)}return o?h(t):$(t)}function $(t){const e=m.passages||[],i=!!(typeof p<"u"&&p.getSettings?p.getSettings():{}).readingMockTestMode,n=e.map(s=>`
      <li>
        <button class="reading-pick" data-id="${l(s.id)}">
          <span class="reading-title"><strong>${a(s.title_ja)}</strong></span>
        </button>
      </li>
    `).join("");t.innerHTML=`
    <h2>${a("\u3069\u3063\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${a("\u307F\u3058\u304B\u3044 JLPT \u3051\u3044\u3057\u304D\u306E \u3076\u3093\u3057\u3087\u3046\u3068 \u3057\u3064\u3082\u3093\u3067\u3059\u3002")} ${e.length} ${a("\u3076\u3093\u3057\u3087\u3046\u304C \u3042\u308A\u307E\u3059\u3002\u3084\u3055\u3057\u3044 \u2192 \u3075\u3064\u3046 \u2192 \u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F \u306E \u3058\u3085\u3093\u306B \u306A\u3089\u3093\u3067 \u3044\u307E\u3059\u3002")}</p>
    <label class="reading-mode-toggle">
      <input type="checkbox" id="reading-mock-mode" ${i?"checked":""}>
      <span>${a("\u3082\u304E\u30C6\u30B9\u30C8\u30E2\u30FC\u30C9")} (primary questions only - matches official JLPT N5 distribution)</span>
    </label>
    <ul class="reading-list">${n}</ul>
  `,document.getElementById("reading-mock-mode").addEventListener("change",s=>{p.setSettings({readingMockTestMode:s.target.checked}),$(t)}),t.querySelectorAll("[data-id]").forEach(s=>{s.addEventListener("click",()=>{location.hash=`#/reading/${encodeURIComponent(s.dataset.id)}`})})}function h(t){const e=o.passage;return o.phase==="read"?j(t,e):o.phase==="questions"?f(t,e):v(t,e)}function j(t,e){const r=m?.passages||[],i=r.findIndex(g=>g.id===e.id),n=i>0?r[i-1]:null,s=i>=0&&i<r.length-1?r[i+1]:null,d=`
    <nav class="reading-nav" aria-label="Passage navigation">
      ${n?`<a href="#/reading/${encodeURIComponent(n.id)}" title="${l(n.title_ja||n.id)}">\u2190 <span lang="ja">${a(n.title_ja||n.id)}</span></a>`:"<span></span>"}
      ${s?`<a href="#/reading/${encodeURIComponent(s.id)}" title="${l(s.title_ja||s.id)}"><span lang="ja">${a(s.title_ja||s.id)}</span> \u2192</a>`:"<span></span>"}
    </nav>
  `;t.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span><a href="#/reading" id="reading-back">\u2190 ${a("\u3082\u3069\u308B")}</a> \u30FB ${a("\u3076\u3093\u3057\u3087\u3046\u3092 \u8AAD\u3093\u3067\u3001\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u3066 \u304F\u3060\u3055\u3044\u3002")}</span>
      </div>
      <h2>${a(e.title_ja)}</h2>
      <p class="muted small">\u30EC\u30D9\u30EB: ${a(y[e.level]||e.level)} \u30FB \u30C8\u30D4\u30C3\u30AF: ${a(k[e.topic]||e.topic)}</p>
      <div class="passage-text">${a(e.ja)}</div>
      ${e.cultural_context?`
        <aside class="reading-cultural-context">
          <p class="muted small"><strong>Cultural context:</strong> ${l(e.cultural_context)}</p>
        </aside>
      `:""}
      ${w(e)}
      ${e.translation_literal||e.translation_natural?`
        <!-- IMP-140 (richness audit, 2026-05-10): opt-in literal vs
             natural translation toggle. The Japanese passage stays the
             default render (preserving JA-27 "Japanese-first"). The
             translations are collapsed by default; click to reveal as
             a study aid. -->
        <details class="reading-translations">
          <summary class="muted small">Show English translation (study aid)</summary>
          <div class="reading-translation-pair">
            ${e.translation_literal?`
              <section class="reading-translation-block">
                <h4 class="reading-translation-label">Literal</h4>
                <p class="reading-translation-text">${l(e.translation_literal)}</p>
              </section>
            `:""}
            ${e.translation_natural?`
              <section class="reading-translation-block">
                <h4 class="reading-translation-label">Natural</h4>
                <p class="reading-translation-text">${l(e.translation_natural)}</p>
              </section>
            `:""}
            <p class="muted small">Translations are study aids, not the default render. Try the Japanese first; reveal English only when stuck.</p>
          </div>
        </details>
      `:""}
      ${e.audio?`
        <div class="reading-audio">
          <p class="muted small">${a("\u304A\u3093\u305B\u3044 (\u3042\u308B \u3068\u304D):")}</p>
          <audio controls preload="none" src="${l(e.audio)}">Your browser does not support audio.</audio>
        </div>
      `:""}
      <button id="reading-start-q" class="btn-primary">${a("\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u308B")} (${e.questions.length})</button>
      ${d}
    </article>
  `,document.getElementById("reading-back").addEventListener("click",g=>{g.preventDefault(),o=null,location.hash="#/reading"}),document.getElementById("reading-start-q").addEventListener("click",()=>{o.phase="questions",f(t,e)})}function f(t,e){const r=e.questions.length,i=o.idx,n=e.questions[i],s=o.answers[n.id],d=s!=null,g=s===n.correctAnswer;t.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span>${a(e.title_ja)} \u30FB ${a("\u3082\u3093\u3060\u3044")} ${i+1} / ${r}</span>
      </div>
      <details class="passage-recap">
        <summary>${a("\u3076\u3093\u3057\u3087\u3046\u3092 \u898B\u308B")}</summary>
        <div class="passage-text">${a(e.ja)}</div>
      </details>
      <div class="question-card">
        <p class="question">${a(n.prompt_ja)}</p>
        <div class="choice-grid">
          ${n.choices.map(c=>{let u="choice-button";return d?c===n.correctAnswer?u+=" correct-choice":c===s&&(u+=" wrong-choice"):s===c&&(u+=" selected"),`<button data-pick="${l(c)}" class="${u}" ${d?"disabled":""}>${a(c)}</button>`}).join("")}
        </div>
        ${d?`
          <div class="drill-feedback ${g?"correct":"incorrect"}">
            <div class="feedback-headline">${g?a("\u305B\u3044\u304B\u3044"):a("\u3056\u3093\u306D\u3093")}</div>
            ${n.explanation_en?`<p class="muted small">${l(n.explanation_en)}</p>`:""}
            <button id="reading-next" class="btn-primary">${i===r-1?a("\u304A\u308F\u308A"):a("\u3064\u304E\u306E \u3057\u3064\u3082\u3093")}</button>
          </div>
        `:""}
      </div>
    </article>
  `,t.querySelectorAll("[data-pick]").forEach(c=>{c.addEventListener("click",()=>{o.answers[n.id]=c.dataset.pick,f(t,e)})}),document.getElementById("reading-next")?.addEventListener("click",()=>{i===r-1?(o.phase="results",v(t,e)):(o.idx+=1,f(t,e))})}function v(t,e){const r=e.questions.length,i=e.questions.filter(s=>o.answers[s.id]===s.correctAnswer).length,n=Math.round(i/r*100);i>0&&p.setReadingCompleted(e.id),t.innerHTML=`
    <div class="reading-results">
      <h2>${a(e.title_ja)} \u30FB ${a("\u3051\u3063\u304B")}</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${i}/${r}</div><div class="stat-label">${a("\u30B9\u30B3\u30A2")}</div></div>
        <div class="stat-card ${n>=70?"mastered":"weak"}"><div class="stat-num">${n}%</div><div class="stat-label">${a("\u305B\u3044\u304B\u3044\u308A\u3064")}</div></div>
      </section>
      <div class="test-nav">
        <button id="reading-back-list" class="btn-primary">${a("\u307B\u304B\u306E \u3076\u3093\u3057\u3087\u3046\u3092 \u3048\u3089\u3076")}</button>
      </div>
    </div>
  `,document.getElementById("reading-back-list").addEventListener("click",()=>{o=null,$(t)})}function l(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}function w(t){const e=Array.isArray(t.grammar_footnotes)?t.grammar_footnotes:[];if(e.length===0)return"";const r=(t.ja||"").split("\u3002").filter(s=>s.trim()).map(s=>s.trim()),i=new Map;for(const s of e){const d=s.sentence_index??0;i.has(d)||i.set(d,[]),i.get(d).push(s)}const n=[...i.entries()].sort((s,d)=>s[0]-d[0]).map(([s,d])=>{const g=(r[s]||"").slice(0,50)+(r[s]&&r[s].length>50?"\u2026":"\u3002"),c=d.map(u=>`
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
      <ol class="reading-footnote-groups">${n}</ol>
    </details>
  `}export{E as renderReading};
