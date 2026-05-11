import*as f from"./storage.js";import"./i18n.js";const u=a=>String(a??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t]);let d=null;async function g(){if(d)return d;try{const a=await fetch("data/test_strategy.json");if(!a.ok)throw new Error(`HTTP ${a.status}`);return d=await a.json(),d}catch(a){return console.error("[weak-areas] load failed:",a),null}}let m=null;async function h(){if(m)return m;try{const a=await fetch("data/grammar.json");return a.ok?(m=(await a.json()).patterns||[],m):null}catch{return null}}function y(a){if(typeof a!="string")return null;const t=a.match(/grammar\.json:(n5-\d+)(?:\.\.(n5-)?(\d+))?/);if(t){const l=t[1],i=t[3],o=parseInt(l.split("-")[1],10),r=i?parseInt(i,10):o;return{kind:"grammar",matches:n=>{if(typeof n!="string"||!n.startsWith("n5-"))return!1;const e=parseInt(n.split("-")[1],10);return Number.isFinite(e)&&e>=o&&e<=r}}}return a.includes("kanji.json")?{kind:"kanji",matches:()=>!1}:a.includes("vocab.json")?{kind:"vocab",matches:()=>!1}:a.includes("listening.json")?{kind:"listening",matches:()=>!1}:a.includes("reading.json")?{kind:"reading",matches:()=>!1}:null}function k(a,t,l){const i=(a.module_pointers||[]).map(y).filter(Boolean);if(!i.length)return null;const o=new Set;for(const s of l)for(const c of i)if(c.kind==="grammar"&&c.matches(s.id)){o.add(s.id);break}let r=0,n=0;for(const s of o){const c=t[s];if(!c)continue;const p=(c.correct||0)+(c.wrong||0);p&&(r+=p,n+=c.correct||0)}const e=r>0?Math.round(100*n/r):null;return{area_name:a.area,n_in_scope:o.size,attempts:r,correct:n,accuracy:e,drill_recommendation:a.drill_recommendation||"",module_pointers:a.module_pointers||[],diagnostic_questions:a.diagnostic_questions||[]}}function w(a){return a==null?'<span class="weak-area-badge weak-area-untested">Not tested</span>':a<60?`<span class="weak-area-badge weak-area-low">${a}% \u2014 needs review</span>`:a<80?`<span class="weak-area-badge weak-area-mid">${a}% \u2014 improving</span>`:`<span class="weak-area-badge weak-area-high">${a}% \u2014 solid</span>`}async function j(a){a.innerHTML='<p class="muted small">Computing your weak areas\u2026</p>';const[t,l]=await Promise.all([g(),h()]);if(!t||!l){a.innerHTML=`<article class="weak-areas-page"><p>Couldn't load required data. Please try again.</p></article>`;return}const i=f.getHistory()||{},r=(t.diagnostic_drills&&t.diagnostic_drills.diagnostic_areas||[]).map(e=>k(e,i,l)).filter(Boolean);r.sort((e,s)=>e.accuracy==null&&s.accuracy==null?0:e.accuracy==null?1:s.accuracy==null?-1:e.accuracy-s.accuracy);const n=r.some(e=>e.attempts>0);a.innerHTML=`
    <article class="weak-areas-page">
      <a class="back-link" href="#/summary">\u2190 Back to Progress</a>
      <h2>Weak-area diagnostic</h2>
      <p class="muted">
        Cross-references your actual test &amp; drill history against the
        9 diagnostic areas in <code>test_strategy.json</code>. Areas with
        accuracy &lt; 60% are flagged for review; each links to the
        specific drill resources for that gap.
      </p>
      ${n?"":`
        <div class="empty-state">
          <p>No test history yet. Take a few tests or drill some questions, then come back to see your diagnostic.</p>
          <p><a href="#/test" class="btn-primary" style="text-decoration:none">Start a test</a></p>
        </div>
      `}
      <section class="weak-areas-list">
        ${r.map(e=>`
          <article class="weak-area-card">
            <header class="weak-area-header">
              <h3>${u(e.area_name)}</h3>
              ${w(e.accuracy)}
            </header>
            <p class="muted small">
              ${e.n_in_scope} pattern(s) in scope \xB7
              ${e.attempts} attempt(s)${e.accuracy!=null?` \xB7 ${e.correct}/${e.attempts} correct`:""}
            </p>
            ${e.drill_recommendation?`<p class="weak-area-recommendation">${u(e.drill_recommendation)}</p>`:""}
            ${e.diagnostic_questions?.length?`
              <details class="weak-area-diagnostic">
                <summary class="muted small">Diagnostic questions</summary>
                <ul>${e.diagnostic_questions.map(s=>`<li class="muted small">${u(s)}</li>`).join("")}</ul>
              </details>
            `:""}
            ${e.module_pointers?.length?`
              <p class="muted small">References: ${e.module_pointers.map(u).join(", ")}</p>
            `:""}
          </article>
        `).join("")}
      </section>
      <p class="muted small" style="margin-top:24px">
        <a href="#/strategy">See full test-strategy bank \u2192</a>
      </p>
    </article>
  `}export{j as renderWeakAreas};
