let i=null,c=null,l=null;async function p(){if(i)return i;const a=await fetch("data/grammar.json");if(!a.ok)throw new Error(`Failed to load grammar.json: ${a.status}`);return i=await a.json(),i}async function u(){if(c)return c;const a=await fetch("data/vocab.json");if(!a.ok)throw new Error(`Failed to load vocab.json: ${a.status}`);return c=await a.json(),c}async function g(){if(l)return l;const a=await fetch("data/kanji.json");if(!a.ok)throw new Error(`Failed to load kanji.json: ${a.status}`);return l=await a.json(),l}async function w(a,r){const e=r?decodeURIComponent(r):"";if(!e)return await Promise.all([p(),u(),g()]),m(a);if(e==="grammar"){const[{renderGrammarTOC:t},o]=await Promise.all([import("./learn-grammar.js"),p()]);return t(a,o)}if(e==="vocab"||e==="vocabulary"){const[{renderVocabularyList:t},o]=await Promise.all([import("./learn-vocab.js"),u()]);return t(a,o)}if(e.startsWith("vocab/")){const[{renderVocabularyDetail:t},o,b]=await Promise.all([import("./learn-vocab.js"),u(),p()]),f=decodeURIComponent(e.slice(6));return t(a,o,b,f)}const n=e.startsWith("grammar/")?e.slice(8):e,[{renderGrammarPatternDetail:s},d]=await Promise.all([import("./learn-grammar.js"),p()]),h=d.patterns.find(t=>t.id===n);return h?s(a,h,d.patterns):m(a)}function m(a){const r=(i?.patterns||[]).length||178,e=(c?.entries||[]).length||995,n=(l?.entries||[]).length||106,s=54,d=50;a.innerHTML=`
    <h2>Learn</h2>

    <div class="section-label">
      <span class="section-label-text">Reference</span>
      <span class="section-label-rule" aria-hidden="true"></span>
    </div>
    <div class="learn-hub learn-hub-3">
      <a class="hub-card" href="#/learn/grammar">
        <p class="card-index" aria-hidden="true">01</p>
        <h3>Grammar</h3>
        <p>${r} patterns across 5 sections. Form, examples, common mistakes.</p>
        <span class="hub-cta">Browse</span>
      </a>
      <a class="hub-card" href="#/learn/vocab">
        <p class="card-index" aria-hidden="true">02</p>
        <h3>Vocabulary</h3>
        <p>${e} words grouped by topic - people, time, places, verbs, adjectives.</p>
        <span class="hub-cta">Browse</span>
      </a>
      <a class="hub-card" href="#/kanji">
        <p class="card-index" aria-hidden="true">03</p>
        <h3>Kanji</h3>
        <p>${n} kanji with on / kun-yomi, meanings, stroke order. Tap any glyph.</p>
        <span class="hub-cta">Browse</span>
      </a>
    </div>

    <div class="section-label">
      <span class="section-label-text">Practice</span>
      <span class="section-label-rule" aria-hidden="true"></span>
    </div>
    <div class="learn-hub learn-hub-2">
      <a class="hub-card" href="#/reading">
        <p class="card-index" aria-hidden="true">04</p>
        <h3>Dokkai (Reading)</h3>
        <p>${s} graded passages with comprehension questions. Audio for every passage.</p>
        <span class="hub-cta">Practice</span>
      </a>
      <a class="hub-card" href="#/listening">
        <p class="card-index" aria-hidden="true">05</p>
        <h3>Listening</h3>
        <p>${d} items across the three JLPT N5 listening formats. Audio for every script.</p>
        <span class="hub-cta">Practice</span>
      </a>
    </div>
  `}function v(a){return String(a??"").replace(/[&<>"']/g,r=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[r])}function j(a,r){const e=a.querySelector(".toc-expand-all"),n=a.querySelector(".toc-collapse-all");!e||!n||(e.addEventListener("click",()=>{a.querySelectorAll(r).forEach(s=>s.open=!0)}),n.addEventListener("click",()=>{a.querySelectorAll(r).forEach(s=>s.open=!1)}))}export{v as esc,w as renderLearn,j as wireExpandCollapseControls};
