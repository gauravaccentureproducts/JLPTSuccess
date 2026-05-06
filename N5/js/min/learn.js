let i=null,c=null,l=null;async function d(){if(i)return i;const a=await fetch("data/grammar.json");if(!a.ok)throw new Error(`Failed to load grammar.json: ${a.status}`);return i=await a.json(),i}async function p(){if(c)return c;const a=await fetch("data/vocab.json");if(!a.ok)throw new Error(`Failed to load vocab.json: ${a.status}`);return c=await a.json(),c}async function f(){if(l)return l;const a=await fetch("data/kanji.json");if(!a.ok)throw new Error(`Failed to load kanji.json: ${a.status}`);return l=await a.json(),l}async function g(a,r){const e=r?decodeURIComponent(r):"";if(!e)return await Promise.all([d(),p(),f()]),h(a);if(e==="grammar"){const[{renderGrammarTOC:s},o]=await Promise.all([import("./learn-grammar.js"),d()]);return s(a,o)}if(e==="vocab"||e==="vocabulary"){const[{renderVocabularyList:s},o]=await Promise.all([import("./learn-vocab.js"),p()]);return s(a,o)}if(e.startsWith("vocab/")){const[{renderVocabularyDetail:s},o,m]=await Promise.all([import("./learn-vocab.js"),p(),d()]),b=decodeURIComponent(e.slice(6));return s(a,o,m,b)}const[{renderGrammarPatternDetail:n},t]=await Promise.all([import("./learn-grammar.js"),d()]),u=t.patterns.find(s=>s.id===e);return u?n(a,u,t.patterns):h(a)}function h(a){const r=(i?.patterns||[]).length||187,e=(c?.entries||[]).length||1003,n=(l?.entries||[]).length||106;a.innerHTML=`
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
        <p>30 graded passages with comprehension questions. Audio for every passage.</p>
        <span class="hub-cta">Practice</span>
      </a>
      <a class="hub-card" href="#/listening">
        <p class="card-index" aria-hidden="true">05</p>
        <h3>Listening</h3>
        <p>12 items across the three JLPT N5 listening formats. Audio for every script.</p>
        <span class="hub-cta">Practice</span>
      </a>
    </div>
  `}function w(a){return String(a??"").replace(/[&<>"']/g,r=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[r])}function v(a,r){const e=a.querySelector(".toc-expand-all"),n=a.querySelector(".toc-collapse-all");!e||!n||(e.addEventListener("click",()=>{a.querySelectorAll(r).forEach(t=>t.open=!0)}),n.addEventListener("click",()=>{a.querySelectorAll(r).forEach(t=>t.open=!1)}))}export{w as esc,g as renderLearn,v as wireExpandCollapseControls};
