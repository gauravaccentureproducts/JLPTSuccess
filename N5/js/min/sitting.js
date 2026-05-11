import"./storage.js";import{t as h}from"./i18n.js";import{loadPacing as _,renderPacingChip as j}from"./mondai-pacing.js";import{estimate as w}from"./score-estimator.js";import{openStrategyModal as T}from"./strategy-modal.js";const f=[["mojigoi","Moji + Goi","\u6587\u5B57\u30FB\u8A9E\u5F59",["moji","goi"],25],["bunpoudok","Bunpou + Dokkai","\u6587\u6CD5\u30FB\u8AAD\u89E3",["bunpou","dokkai"],50],["choukai","Listening","\u8074\u89E3",["listening"],30]],v=60;let l=null,m=null,S=null;function o(a){return String(a??"").replace(/[&<>"']/g,i=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[i])}async function L(a,i){const n=await fetch(`data/papers/${a}/paper-${i}.json`);return n.ok?n.json():null}async function M(){const a=await fetch("data/listening.json");return a.ok?a.json():{items:[]}}function k(a){const i=Math.floor(a/60),n=String(a%60).padStart(2,"0");return`${String(i).padStart(2,"0")}:${n}`}function I(a,i,n){S=Date.now()+a*1e3,m&&clearInterval(m),m=setInterval(()=>{const t=Math.max(0,Math.ceil((S-Date.now())/1e3));i(t),t<=0&&(clearInterval(m),m=null,n())},1e3),i(a)}async function D(a,i){const n=(i||"").split("/").filter(Boolean);if(n.length===0)return E(a);const t=parseInt(n[0],10);if(!Number.isFinite(t)||t<1||t>7){a.innerHTML=`<p>${o(h("meta.bad_paper"))} <a href="#/sitting">${o(h("meta.pick_again"))}</a></p>`;return}if(n[1]==="result")return N(a,t);const c=n[1]?parseInt(n[1],10):0;if(!Number.isFinite(c)||c<0||c>=f.length){a.innerHTML=`<p>${o(h("meta.bad_section"))} <a href="#/sitting">${o(h("meta.pick_again"))}</a></p>`;return}return P(a,t,c)}function E(a){a.innerHTML=`
    <article class="sitting-picker">
      <a class="back-link" href="#/test">\u2190 ${o(h("meta.back_to_test"))}</a>
      <h2>${o(h("meta.sitting_title"))}</h2>
      <p class="page-lede">${o(h("meta.sitting_intro"))}</p>
      <p class="muted">${o(h("meta.pick_paper_intro"))}</p>
      <div class="sitting-paper-grid">
        ${[1,2,3,4,5,6,7].map(i=>`
          <a class="sitting-paper-card" href="#/sitting/${i}/0">
            <span class="card-index" aria-hidden="true">${String(i).padStart(2,"0")}</span>
            <h3>${o(h("meta.paper_n").replace("${n}",i))}</h3>
            <p class="muted small">moji-${i} \xB7 goi-${i} \xB7 bunpou-${i} \xB7 dokkai-${i} \xB7 listening</p>
          </a>
        `).join("")}
      </div>
    </article>
  `}async function P(a,i,n){const[,t,c,p,g]=f[n];(!l||l.paperNumber!==i)&&(l={paperNumber:i,currentSection:n,startedAt:new Date().toISOString(),sectionResults:[],answers:{}});let u=[];if(p[0]==="listening")u=((await M()).items||[]).slice(0,12).map(s=>({id:s.id,stem_html:s.title_ja||s.id,audio:s.audio,script_ja:s.script_ja,prompt_ja:s.prompt_ja,choices:s.choices||[],correctIndex:(s.choices||[]).findIndex(d=>d===s.correctAnswer),kind:"listening",mondai:s.mondai}));else for(const e of p){const s=await L(e,i);s&&u.push(...s.questions.map(d=>({...d,kind:e})))}if(u.length===0){a.innerHTML=`<p>No questions for section ${n}. <a href="#/sitting">Restart.</a></p>`;return}await _();const $=()=>{let e=0;for(const s of u){const d=l.answers[s.id];typeof d=="number"&&d===s.correctIndex&&(e+=1)}l.sectionResults[n]={label:t,jaLabel:c,total:u.length,correct:e,durationSec:g*60},n+1<f.length?B(a,i,n+1):location.hash=`#/sitting/${i}/result`},b=u.length;a.innerHTML=`
    <article class="sitting-section">
      <header class="sitting-section-header">
        <span class="sitting-section-label" lang="ja">${o(c)}</span>
        <h2>${o(t)} <span class="muted small">(Paper ${i}, ${b} questions)</span></h2>
        <p class="sitting-timer-chip" id="sitting-timer" aria-live="polite">${k(g*60)}</p>
        <!-- IMP-WAVE-P4-T3 (UI audit fix, 2026-05-11): per-section
             strategy button. Opens a modal listing techniques + trap
             patterns scoped to this section. data-section is the
             internal id; data-label is the human-readable label
             passed to openStrategyModal as the modal title. -->
        <button type="button" class="sitting-strategy-btn" id="sitting-strategy-btn"
                data-section="${o(f[n][0])}" data-label="${o(t)}"
                aria-label="View strategies for this section">
          \u{1F4CB} Strategies
        </button>
      </header>
      <form id="sitting-form" class="sitting-form">
        ${u.map((e,s)=>`
          <fieldset class="sitting-question" id="sq-${o(e.id)}">
            <legend>Q${s+1} ${j(e.kind,e.mondai)}</legend>
            ${e.audio?`<audio class="example-audio" controls preload="metadata" src="${o(e.audio)}"></audio>`:""}
            ${e.stem_html?`<p class="sitting-stem" lang="ja">${e.stem_html}</p>`:""}
            ${e.prompt_ja?`<p class="sitting-prompt" lang="ja">${o(e.prompt_ja)}</p>`:""}
            ${e.script_ja&&!e.audio?`<p class="sitting-script" lang="ja">${o(e.script_ja)}</p>`:""}
            <div class="sitting-choices">
              ${(e.choices||[]).map((d,y)=>`
                <label>
                  <input type="radio" name="${o(e.id)}" value="${y}">
                  <span lang="ja">${o(d)}</span>
                </label>
              `).join("")}
            </div>
          </fieldset>
        `).join("")}
        <div class="sitting-actions">
          <button type="submit" class="btn-primary">Submit section ${n+1} of ${f.length}</button>
        </div>
      </form>
    </article>
  `;const r=document.getElementById("sitting-strategy-btn");r&&r.addEventListener("click",()=>{const e=r.dataset.section,s=r.dataset.label;T(e,s)}),document.getElementById("sitting-form").addEventListener("submit",e=>{e.preventDefault(),m&&clearInterval(m),m=null;for(const s of u){const d=document.querySelector(`input[name="${s.id}"]:checked`);d&&(l.answers[s.id]=parseInt(d.value,10))}$()}),document.getElementById("sitting-form").addEventListener("change",e=>{if(e.target.tagName==="INPUT"){const s=u.find(d=>d.id===e.target.name);s&&(l.answers[s.id]=parseInt(e.target.value,10))}}),I(g*60,e=>{const s=document.getElementById("sitting-timer");s&&(s.textContent=k(e)),e<=60&&s&&s.classList.add("danger")},()=>{for(const e of u){const s=document.querySelector(`input[name="${e.id}"]:checked`);s&&(l.answers[e.id]=parseInt(s.value,10))}$()})}function B(a,i,n){const[,t,c]=f[n];let p=v;a.innerHTML=`
    <article class="sitting-break">
      <h2>Break</h2>
      <p class="page-lede">Stretch. Get water. Section <strong>${n+1}</strong> (${o(t)} / <span lang="ja">${o(c)}</span>) starts in <strong id="break-countdown">${p}</strong>s.</p>
      <div class="sitting-break-actions">
        <a class="btn-primary" href="#/sitting/${i}/${n}" id="skip-break">Skip break, start now</a>
      </div>
    </article>
  `,m&&clearInterval(m),m=setInterval(()=>{p-=1;const g=document.getElementById("break-countdown");g&&(g.textContent=String(p)),p<=0&&(clearInterval(m),m=null,location.hash=`#/sitting/${i}/${n}`)},1e3)}function N(a,i){if(!l||!l.sectionResults||l.sectionResults.length<f.length){a.innerHTML='<p>No completed sitting in memory. <a href="#/sitting">Start again.</a></p>';return}let n=0,t=0;for(const r of l.sectionResults)n+=r.correct,t+=r.total;const c=t>0?Math.round(100*n/t):0,p=60,g=[63,61,79],u="~19 / section",$=l.sectionResults.map((r,e)=>(r.total?100*r.correct/r.total:0)>=g[e]),b=$.every(Boolean);a.innerHTML=`
    <article class="sitting-result">
      <h2>JLPT N5 Mock - Paper ${i} - Result</h2>
      <p class="page-lede">
        Total: <strong>${n} / ${t}</strong> (${c}%) \xB7
        ${c>=p&&b?'<span class="pass-badge pass">Pass \xB7 all section minimums met</span>':c>=p?`<span class="pass-badge fail">Overall ${c}% (\u2265${p}%) but a section is below its minimum</span>`:`<span class="pass-badge fail">Below ${p}% study-target</span>`}
      </p>
      <p class="muted small" style="margin-top:-4px;">
        Real JLPT N5 official pass mark = 80 / 180 (44.4%) with section minimums of 19 / 60 (~32% per section after scoring scale). Study target \u2265 ${p}% is the conservative bar matching Bunpro / Try! N5 guidance.
      </p>
      <table class="category-table">
        <thead>
          <tr>
            <th>Section</th>
            <th>Score</th>
            <th>%</th>
            <th>Section minimum</th>
          </tr>
        </thead>
        <tbody>
          ${l.sectionResults.map((r,e)=>{const s=r.total?Math.round(100*r.correct/r.total):0,d=$[e]?"pass":"fail",y=$[e]?"\u2713 met":`\u2717 ${g[e]}%`;return`<tr class="${d}"><td>${o(r.label)} <span class="muted small" lang="ja">(${o(r.jaLabel)})</span></td><td>${r.correct} / ${r.total}</td><td>${s}%</td><td class="muted small">${y}</td></tr>`}).join("")}
        </tbody>
        <tfoot>
          <tr><th>Total</th><th>${n} / ${t}</th><th>${c}%</th><th class="muted small">\u2265 ${p}% target</th></tr>
        </tfoot>
      </table>
      <p class="muted small">
        \u203B The app ships 85Q across the 3 sections (close to the official 91Q). Per-section minimums above are raw-question approximations. The official JLPT N5 score report uses a scaled-equating method that this app does not replicate \u2014 only raw-correct percentages are shown.
      </p>

      <!-- IMP-WAVE-P4-T4 (UI audit fix, 2026-05-11): scaled-score
           estimator. Maps app's 3 sections onto official 2 (mojigoi+
           bunpoudok = section 1 lang+reading; choukai = section 2
           listening), projects raw% linearly onto the 120/60 caps,
           and surfaces a diagnostic band. APPROXIMATION \u2014 labelled
           as such so users don't read it as JEES-official. -->
      ${A(l.sectionResults)}

      <div class="test-nav">
        <a class="btn-primary" href="#/sitting">Try another paper</a>
        <a class="btn-secondary" href="#/home">Home</a>
      </div>
    </article>
  `,l=null}function A(a){if(!a||a.length<3)return"";const i={correct:(a[0]?.correct||0)+(a[1]?.correct||0),total:(a[0]?.total||0)+(a[1]?.total||0)},n={correct:a[2]?.correct||0,total:a[2]?.total||0},t=w(i,n);return`
    <section class="score-estimate" aria-labelledby="score-estimate-heading">
      <h3 id="score-estimate-heading">Scaled-score estimate <span class="muted small">(approximation)</span></h3>
      <p class="muted small">
        The official JLPT N5 uses an equipercentile scale that this app does NOT replicate. The numbers below are a linear-projection approximation onto the official 120 + 60 = 180 cap, intended as a directional indicator only.
      </p>
      <table class="category-table">
        <thead>
          <tr>
            <th>Section</th>
            <th>Raw %</th>
            <th>Estimated scaled</th>
            <th>Section minimum</th>
          </tr>
        </thead>
        <tbody>
          <tr class="${t.section1.meets_min?"pass":"fail"}">
            <td>Section 1 \u2014 Lang Knowledge + Reading</td>
            <td>${t.section1.raw_pct}%</td>
            <td>${t.section1.scaled} / ${t.section1.max}</td>
            <td class="muted small">${t.section1.meets_min?`\u2713 \u2265 ${t.section1.min}`:`\u2717 &lt; ${t.section1.min}`}</td>
          </tr>
          <tr class="${t.section2.meets_min?"pass":"fail"}">
            <td>Section 2 \u2014 Listening</td>
            <td>${t.section2.raw_pct}%</td>
            <td>${t.section2.scaled} / ${t.section2.max}</td>
            <td class="muted small">${t.section2.meets_min?`\u2713 \u2265 ${t.section2.min}`:`\u2717 &lt; ${t.section2.min}`}</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <th>Total</th>
            <th></th>
            <th>${t.total.scaled} / ${t.total.max}</th>
            <th class="muted small">${t.total.meets_min?`\u2713 \u2265 ${t.total.min}`:`\u2717 &lt; ${t.total.min}`}</th>
          </tr>
        </tfoot>
      </table>
      <p class="score-band-callout score-band-${o(t.band.tone)}">
        <strong>Estimated band:</strong> ${o(t.band.label)}
        <span class="muted small" style="display:block; margin-top:4px">${o(t.band.hint)}</span>
      </p>
    </section>
  `}export{D as renderSitting};
