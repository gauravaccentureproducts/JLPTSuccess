import{renderJa as i}from"./furigana.js";import*as p from"./storage.js";import{t as g}from"./i18n.js";const v={easy:"\u3084\u3055\u3057\u3044",medium:"\u3075\u3064\u3046","info-search":"\u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F"},y={"self-introduction":"\u3058\u3053\u3057\u3087\u3046\u304B\u3044","daily routine":"\u307E\u3044\u306B\u3061\u306E \u305B\u3044\u304B\u3064","weekend plan":"\u3057\u3085\u3046\u307E\u3064\u306E \u3088\u3066\u3044",weekend:"\u3057\u3085\u3046\u307E\u3064",shopping:"\u304B\u3044\u3082\u306E",family:"\u304B\u305E\u304F",weather:"\u3066\u3093\u304D",schedule:"\u3088\u3066\u3044",transport:"\u3053\u3046\u3064\u3046",hobby:"\u3057\u3085\u307F",school:"\u5B66\u6821",food:"\u305F\u3079\u3082\u306E",travel:"\u308A\u3087\u3053\u3046",health:"\u3051\u3093\u3053\u3046",study:"\u3079\u3093\u304D\u3087\u3046",people:"\u3072\u3068",request:"\u304A\u306D\u304C\u3044",room:"\u3078\u3084",directions:"\u307F\u3061\u3042\u3093\u306A\u3044"};let $=null,d=null;async function b(){return $||($=await(await fetch("data/reading.json")).json(),$)}function j(n){d={passage:!!(typeof p<"u"&&p.getSettings?p.getSettings():{}).readingMockTestMode?{...n,questions:(n.questions||[]).filter(r=>r.format_role==="primary"||!r.format_role)}:n,phase:"read",answers:{},idx:0}}async function q(n,e){await b();const l=e?decodeURIComponent(e):"";if(l){const r=($.passages||[]).find(a=>a.id===l);if(r)return(!d||d.passage?.id!==r.id)&&j(r),_(n)}return d?_(n):f(n)}function f(n){const e=$.passages||[],o=!!(typeof p<"u"&&p.getSettings?p.getSettings():{}).readingMockTestMode,r=e.map(a=>`
      <li>
        <button class="reading-pick" data-id="${t(a.id)}">
          <span class="reading-title"><strong>${i(a.title_ja)}</strong></span>
        </button>
      </li>
    `).join("");n.innerHTML=`
    <h2>${i("\u3069\u3063\u304B\u3044 \u308C\u3093\u3057\u3085\u3046")}</h2>
    <p>${i("\u307F\u3058\u304B\u3044 JLPT \u3051\u3044\u3057\u304D\u306E \u3076\u3093\u3057\u3087\u3046\u3068 \u3057\u3064\u3082\u3093\u3067\u3059\u3002")} ${e.length} ${i("\u3076\u3093\u3057\u3087\u3046\u304C \u3042\u308A\u307E\u3059\u3002\u3084\u3055\u3057\u3044 \u2192 \u3075\u3064\u3046 \u2192 \u3058\u3087\u3046\u307B\u3046\u3051\u3093\u3055\u304F \u306E \u3058\u3085\u3093\u306B \u306A\u3089\u3093\u3067 \u3044\u307E\u3059\u3002")}</p>
    <label class="reading-mode-toggle">
      <input type="checkbox" id="reading-mock-mode" ${o?"checked":""}>
      <span>${i("\u3082\u304E\u30C6\u30B9\u30C8\u30E2\u30FC\u30C9")} (primary questions only - matches official JLPT N5 distribution)</span>
    </label>
    <ul class="reading-list">${r}</ul>
  `,document.getElementById("reading-mock-mode").addEventListener("change",a=>{p.setSettings({readingMockTestMode:a.target.checked}),f(n)}),n.querySelectorAll("[data-id]").forEach(a=>{a.addEventListener("click",()=>{location.hash=`#/reading/${encodeURIComponent(a.dataset.id)}`})})}function _(n){const e=d.passage;return d.phase==="read"?w(n,e):d.phase==="questions"?h(n,e):k(n,e)}function w(n,e){const l=$?.passages||[],o=l.findIndex(s=>s.id===e.id),r=o>0?l[o-1]:null,a=o>=0&&o<l.length-1?l[o+1]:null,u=`
    <nav class="reading-nav" aria-label="Passage navigation">
      ${r?`<a href="#/reading/${encodeURIComponent(r.id)}" title="${t(r.title_ja||r.id)}">\u2190 <span lang="ja">${i(r.title_ja||r.id)}</span></a>`:"<span></span>"}
      ${a?`<a href="#/reading/${encodeURIComponent(a.id)}" title="${t(a.title_ja||a.id)}"><span lang="ja">${i(a.title_ja||a.id)}</span> \u2192</a>`:"<span></span>"}
    </nav>
  `;n.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span><a href="#/reading" id="reading-back">\u2190 ${i("\u3082\u3069\u308B")}</a> \u30FB ${i("\u3076\u3093\u3057\u3087\u3046\u3092 \u8AAD\u3093\u3067\u3001\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u3066 \u304F\u3060\u3055\u3044\u3002")}</span>
      </div>
      <h2>${i(e.title_ja)}</h2>
      <p class="muted small">\u30EC\u30D9\u30EB: ${i(v[e.level]||e.level)} \u30FB \u30C8\u30D4\u30C3\u30AF: ${i(y[e.topic]||e.topic)}</p>
      <div class="passage-text">${i(e.ja)}</div>
      ${e.cultural_context?`
        <aside class="reading-cultural-context">
          <p class="muted small"><strong>${t(g("dokkai_detail.cultural_context"))}:</strong> ${t(e.cultural_context)}</p>
        </aside>
      `:""}
      ${e.authentic_categories?.length?`
        <!-- IMP-WAVE-AUTHENTIC-XLINK (2026-05-11): thematic
             cross-link to /authentic content. Passage topic
             maps to authentic categories; renderer surfaces
             a "Related real-world content" chip. -->
        <aside class="reading-authentic-link muted small">
          <strong>Related real-world content:</strong>
          ${e.authentic_categories.map(s=>`<a href="#/authentic" class="authentic-cat-chip">${t(s)}</a>`).join(" ")}
        </aside>
      `:""}
      ${x(e)}
      ${(()=>{const s=e.time_target_seconds;return!s||typeof s!="object"?"":`
          <aside class="reading-time-target muted small">
            <strong>${t(g("dokkai_detail.target_time"))}:</strong> ${t(s.total_seconds||"?")}s ${t(g("dokkai_detail.total"))}
            ${s.reading_seconds?` (${t(g("dokkai_detail.read"))}: ${t(s.reading_seconds)}s`:""}${s.comprehension_seconds?` + ${t(g("dokkai_detail.comprehend"))}: ${t(s.comprehension_seconds)}s)`:s.reading_seconds?")":""}
            ${s.note?`<br><span class="muted small">${t(s.note)}</span>`:""}
          </aside>
        `})()}
      ${(()=>{const s=Array.isArray(e.comprehension_strategy_hints)?e.comprehension_strategy_hints:[];return s.length?`
          <aside class="reading-strategy-hints">
            <details>
              <summary><strong>${t(g("dokkai_detail.strategy_hints"))} (${s.length})</strong></summary>
              <ul>
                ${s.map(c=>`<li class="muted small">${t(c)}</li>`).join("")}
              </ul>
            </details>
          </aside>
        `:""})()}
      ${(()=>{const s=e.register_signal;return!s||typeof s!="object"||!s.register?"":`
          <p class="muted small reading-register-signal">
            <strong>${t(g("dokkai_detail.register"))}:</strong> ${t(s.register)}${s.confidence?` <span class="muted">(${t(s.confidence)} ${t(g("dokkai_detail.confidence"))})</span>`:""}
            ${Array.isArray(s.signals)&&s.signals.length?`<br><span class="muted small">${t(g("dokkai_detail.signals"))}: ${s.signals.map(t).join("; ")}</span>`:""}
          </p>
        `})()}
      ${(()=>{const s=e.target_reading_age;return!s||typeof s!="object"?"":`
          <p class="muted small reading-target-age">
            <strong>${t(g("dokkai_detail.native_reading_level"))}:</strong> ${t(g("dokkai_detail.age"))} ${t(s.native_equivalent_age_years||"?")}
            ${s.kanji_ratio!=null?` <span class="muted">(${(s.kanji_ratio*100).toFixed(1)}% ${t(g("dokkai_detail.kanji"))}, ${t(s.char_count||"?")} ${t(g("dokkai_detail.chars"))})</span>`:""}
          </p>
        `})()}
      ${(()=>{const s=Array.isArray(e.discourse_markers_used)?e.discourse_markers_used:[];return s.length?`
          <p class="muted small reading-discourse-markers">
            <strong>${t(g("dokkai_detail.discourse_markers"))}:</strong>
            ${s.map(c=>`<span class="discourse-marker-chip" lang="ja">${t(c)}</span>`).join(" ")}
          </p>
        `:""})()}
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
                <p class="reading-translation-text">${t(e.translation_literal)}</p>
              </section>
            `:""}
            ${e.translation_natural?`
              <section class="reading-translation-block">
                <h4 class="reading-translation-label">Natural</h4>
                <p class="reading-translation-text">${t(e.translation_natural)}</p>
              </section>
            `:""}
            <p class="muted small">Translations are study aids, not the default render. Try the Japanese first; reveal English only when stuck.</p>
          </div>
        </details>
      `:""}
      ${e.audio?`
        <div class="reading-audio">
          <p class="muted small">${i("\u304A\u3093\u305B\u3044 (\u3042\u308B \u3068\u304D):")}</p>
          <audio controls preload="none" src="${t(e.audio)}">Your browser does not support audio.</audio>
        </div>
      `:""}
      <button id="reading-start-q" class="btn-primary">${i("\u3057\u3064\u3082\u3093\u3092 \u306F\u3058\u3081\u308B")} (${e.questions.length})</button>
      ${u}
    </article>
  `,document.getElementById("reading-back").addEventListener("click",s=>{s.preventDefault(),d=null,location.hash="#/reading"}),document.getElementById("reading-start-q").addEventListener("click",()=>{d.phase="questions",h(n,e)})}function h(n,e){const l=e.questions.length,o=d.idx,r=e.questions[o],a=d.answers[r.id],u=a!=null,s=a===r.correctAnswer;n.innerHTML=`
    <article class="reading-passage">
      <div class="srs-progress">
        <span>${i(e.title_ja)} \u30FB ${i("\u3082\u3093\u3060\u3044")} ${o+1} / ${l}</span>
      </div>
      <details class="passage-recap">
        <summary>${i("\u3076\u3093\u3057\u3087\u3046\u3092 \u898B\u308B")}</summary>
        <div class="passage-text">${i(e.ja)}</div>
      </details>
      <div class="question-card">
        <p class="question">${i(r.prompt_ja)}</p>
        <div class="choice-grid">
          ${r.choices.map(c=>{let m="choice-button";return u?c===r.correctAnswer?m+=" correct-choice":c===a&&(m+=" wrong-choice"):a===c&&(m+=" selected"),`<button data-pick="${t(c)}" class="${m}" ${u?"disabled":""}>${i(c)}</button>`}).join("")}
        </div>
        ${u?`
          <div class="drill-feedback ${s?"correct":"incorrect"}">
            <div class="feedback-headline">${s?i("\u305B\u3044\u304B\u3044"):i("\u3056\u3093\u306D\u3093")}</div>
            ${r.explanation_en?`<p class="muted small">${t(r.explanation_en)}</p>`:""}
            <button id="reading-next" class="btn-primary">${o===l-1?i("\u304A\u308F\u308A"):i("\u3064\u304E\u306E \u3057\u3064\u3082\u3093")}</button>
          </div>
        `:""}
      </div>
    </article>
  `,n.querySelectorAll("[data-pick]").forEach(c=>{c.addEventListener("click",()=>{d.answers[r.id]=c.dataset.pick,h(n,e)})}),document.getElementById("reading-next")?.addEventListener("click",()=>{o===l-1?(d.phase="results",k(n,e)):(d.idx+=1,h(n,e))})}function k(n,e){const l=e.questions.length,o=e.questions.filter(a=>d.answers[a.id]===a.correctAnswer).length,r=Math.round(o/l*100);o>0&&p.setReadingCompleted(e.id),n.innerHTML=`
    <div class="reading-results">
      <h2>${i(e.title_ja)} \u30FB ${i("\u3051\u3063\u304B")}</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${o}/${l}</div><div class="stat-label">${i("\u30B9\u30B3\u30A2")}</div></div>
        <div class="stat-card ${r>=70?"mastered":"weak"}"><div class="stat-num">${r}%</div><div class="stat-label">${i("\u305B\u3044\u304B\u3044\u308A\u3064")}</div></div>
      </section>
      <div class="test-nav">
        <button id="reading-back-list" class="btn-primary">${i("\u307B\u304B\u306E \u3076\u3093\u3057\u3087\u3046\u3092 \u3048\u3089\u3076")}</button>
      </div>
    </div>
  `,document.getElementById("reading-back-list").addEventListener("click",()=>{d=null,f(n)})}function t(n){return String(n??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}function x(n){const e=Array.isArray(n.grammar_footnotes)?n.grammar_footnotes:[];if(e.length===0)return"";const l=(n.ja||"").split("\u3002").filter(a=>a.trim()).map(a=>a.trim()),o=new Map;for(const a of e){const u=a.sentence_index??0;o.has(u)||o.set(u,[]),o.get(u).push(a)}const r=[...o.entries()].sort((a,u)=>a[0]-u[0]).map(([a,u])=>{const s=(l[a]||"").slice(0,50)+(l[a]&&l[a].length>50?"\u2026":"\u3002"),c=u.map(m=>`
      <li class="reading-footnote-item">
        <a class="reading-footnote-pid" href="#/learn/${t(m.pattern_id)}" title="Open ${t(m.pattern_id)} in Learn">${t(m.pattern_id)}</a>
        <span class="reading-footnote-note">${t(m.note||"")}</span>
      </li>
    `).join("");return`
      <li class="reading-footnote-group">
        <p class="reading-footnote-sentence" lang="ja">
          <span class="muted small">Sentence ${a+1}:</span> ${t(s)}
        </p>
        <ul class="reading-footnote-list">${c}</ul>
      </li>
    `}).join("");return`
    <details class="reading-grammar-footnotes">
      <summary><strong>Grammar footnotes</strong> <span class="muted small">\u2014 ${e.length} note${e.length===1?"":"s"} across ${o.size} sentence${o.size===1?"":"s"}</span></summary>
      <ol class="reading-footnote-groups">${r}</ol>
    </details>
  `}export{q as renderReading};
