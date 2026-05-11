import"./storage.js";import{t as g}from"./i18n.js";import{loadPacing as _,renderPacingChip as j}from"./mondai-pacing.js";import{estimate as w}from"./score-estimator.js";const f=[["mojigoi","Moji + Goi","\u6587\u5B57\u30FB\u8A9E\u5F59",["moji","goi"],25],["bunpoudok","Bunpou + Dokkai","\u6587\u6CD5\u30FB\u8AAD\u89E3",["bunpou","dokkai"],50],["choukai","Listening","\u8074\u89E3",["listening"],30]],T=60;let l=null,p=null,S=null;function o(a){return String(a??"").replace(/[&<>"']/g,n=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[n])}async function v(a,n){const i=await fetch(`data/papers/${a}/paper-${n}.json`);return i.ok?i.json():null}async function L(){const a=await fetch("data/listening.json");return a.ok?a.json():{items:[]}}function k(a){const n=Math.floor(a/60),i=String(a%60).padStart(2,"0");return`${String(n).padStart(2,"0")}:${i}`}function M(a,n,i){S=Date.now()+a*1e3,p&&clearInterval(p),p=setInterval(()=>{const e=Math.max(0,Math.ceil((S-Date.now())/1e3));n(e),e<=0&&(clearInterval(p),p=null,i())},1e3),n(a)}async function R(a,n){const i=(n||"").split("/").filter(Boolean);if(i.length===0)return I(a);const e=parseInt(i[0],10);if(!Number.isFinite(e)||e<1||e>7){a.innerHTML=`<p>${o(g("meta.bad_paper"))} <a href="#/sitting">${o(g("meta.pick_again"))}</a></p>`;return}if(i[1]==="result")return N(a,e);const c=i[1]?parseInt(i[1],10):0;if(!Number.isFinite(c)||c<0||c>=f.length){a.innerHTML=`<p>${o(g("meta.bad_section"))} <a href="#/sitting">${o(g("meta.pick_again"))}</a></p>`;return}return P(a,e,c)}function I(a){a.innerHTML=`
    <article class="sitting-picker">
      <a class="back-link" href="#/test">\u2190 ${o(g("meta.back_to_test"))}</a>
      <h2>${o(g("meta.sitting_title"))}</h2>
      <p class="page-lede">${o(g("meta.sitting_intro"))}</p>
      <p class="muted">${o(g("meta.pick_paper_intro"))}</p>
      <div class="sitting-paper-grid">
        ${[1,2,3,4,5,6,7].map(n=>`
          <a class="sitting-paper-card" href="#/sitting/${n}/0">
            <span class="card-index" aria-hidden="true">${String(n).padStart(2,"0")}</span>
            <h3>${o(g("meta.paper_n").replace("${n}",n))}</h3>
            <p class="muted small">moji-${n} \xB7 goi-${n} \xB7 bunpou-${n} \xB7 dokkai-${n} \xB7 listening</p>
          </a>
        `).join("")}
      </div>
    </article>
  `}async function P(a,n,i){const[,e,c,d,u]=f[i];(!l||l.paperNumber!==n)&&(l={paperNumber:n,currentSection:i,startedAt:new Date().toISOString(),sectionResults:[],answers:{}});let m=[];if(d[0]==="listening")m=((await L()).items||[]).slice(0,12).map(s=>({id:s.id,stem_html:s.title_ja||s.id,audio:s.audio,script_ja:s.script_ja,prompt_ja:s.prompt_ja,choices:s.choices||[],correctIndex:(s.choices||[]).findIndex(r=>r===s.correctAnswer),kind:"listening",mondai:s.mondai}));else for(const t of d){const s=await v(t,n);s&&m.push(...s.questions.map(r=>({...r,kind:t})))}if(m.length===0){a.innerHTML=`<p>No questions for section ${i}. <a href="#/sitting">Restart.</a></p>`;return}await _();const h=()=>{let t=0;for(const s of m){const r=l.answers[s.id];typeof r=="number"&&r===s.correctIndex&&(t+=1)}l.sectionResults[i]={label:e,jaLabel:c,total:m.length,correct:t,durationSec:u*60},i+1<f.length?E(a,n,i+1):location.hash=`#/sitting/${n}/result`},$=m.length;a.innerHTML=`
    <article class="sitting-section">
      <header class="sitting-section-header">
        <span class="sitting-section-label" lang="ja">${o(c)}</span>
        <h2>${o(e)} <span class="muted small">(Paper ${n}, ${$} questions)</span></h2>
        <p class="sitting-timer-chip" id="sitting-timer" aria-live="polite">${k(u*60)}</p>
      </header>
      <form id="sitting-form" class="sitting-form">
        ${m.map((t,s)=>`
          <fieldset class="sitting-question" id="sq-${o(t.id)}">
            <legend>Q${s+1} ${j(t.kind,t.mondai)}</legend>
            ${t.audio?`<audio class="example-audio" controls preload="metadata" src="${o(t.audio)}"></audio>`:""}
            ${t.stem_html?`<p class="sitting-stem" lang="ja">${t.stem_html}</p>`:""}
            ${t.prompt_ja?`<p class="sitting-prompt" lang="ja">${o(t.prompt_ja)}</p>`:""}
            ${t.script_ja&&!t.audio?`<p class="sitting-script" lang="ja">${o(t.script_ja)}</p>`:""}
            <div class="sitting-choices">
              ${(t.choices||[]).map((r,b)=>`
                <label>
                  <input type="radio" name="${o(t.id)}" value="${b}">
                  <span lang="ja">${o(r)}</span>
                </label>
              `).join("")}
            </div>
          </fieldset>
        `).join("")}
        <div class="sitting-actions">
          <button type="submit" class="btn-primary">Submit section ${i+1} of ${f.length}</button>
        </div>
      </form>
    </article>
  `,document.getElementById("sitting-form").addEventListener("submit",t=>{t.preventDefault(),p&&clearInterval(p),p=null;for(const s of m){const r=document.querySelector(`input[name="${s.id}"]:checked`);r&&(l.answers[s.id]=parseInt(r.value,10))}h()}),document.getElementById("sitting-form").addEventListener("change",t=>{if(t.target.tagName==="INPUT"){const s=m.find(r=>r.id===t.target.name);s&&(l.answers[s.id]=parseInt(t.target.value,10))}}),M(u*60,t=>{const s=document.getElementById("sitting-timer");s&&(s.textContent=k(t)),t<=60&&s&&s.classList.add("danger")},()=>{for(const t of m){const s=document.querySelector(`input[name="${t.id}"]:checked`);s&&(l.answers[t.id]=parseInt(s.value,10))}h()})}function E(a,n,i){const[,e,c]=f[i];let d=T;a.innerHTML=`
    <article class="sitting-break">
      <h2>Break</h2>
      <p class="page-lede">Stretch. Get water. Section <strong>${i+1}</strong> (${o(e)} / <span lang="ja">${o(c)}</span>) starts in <strong id="break-countdown">${d}</strong>s.</p>
      <div class="sitting-break-actions">
        <a class="btn-primary" href="#/sitting/${n}/${i}" id="skip-break">Skip break, start now</a>
      </div>
    </article>
  `,p&&clearInterval(p),p=setInterval(()=>{d-=1;const u=document.getElementById("break-countdown");u&&(u.textContent=String(d)),d<=0&&(clearInterval(p),p=null,location.hash=`#/sitting/${n}/${i}`)},1e3)}function N(a,n){if(!l||!l.sectionResults||l.sectionResults.length<f.length){a.innerHTML='<p>No completed sitting in memory. <a href="#/sitting">Start again.</a></p>';return}let i=0,e=0;for(const t of l.sectionResults)i+=t.correct,e+=t.total;const c=e>0?Math.round(100*i/e):0,d=60,u=[63,61,79],m="~19 / section",h=l.sectionResults.map((t,s)=>(t.total?100*t.correct/t.total:0)>=u[s]),$=h.every(Boolean);a.innerHTML=`
    <article class="sitting-result">
      <h2>JLPT N5 Mock - Paper ${n} - Result</h2>
      <p class="page-lede">
        Total: <strong>${i} / ${e}</strong> (${c}%) \xB7
        ${c>=d&&$?'<span class="pass-badge pass">Pass \xB7 all section minimums met</span>':c>=d?`<span class="pass-badge fail">Overall ${c}% (\u2265${d}%) but a section is below its minimum</span>`:`<span class="pass-badge fail">Below ${d}% study-target</span>`}
      </p>
      <p class="muted small" style="margin-top:-4px;">
        Real JLPT N5 official pass mark = 80 / 180 (44.4%) with section minimums of 19 / 60 (~32% per section after scoring scale). Study target \u2265 ${d}% is the conservative bar matching Bunpro / Try! N5 guidance.
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
          ${l.sectionResults.map((t,s)=>{const r=t.total?Math.round(100*t.correct/t.total):0,b=h[s]?"pass":"fail",y=h[s]?"\u2713 met":`\u2717 ${u[s]}%`;return`<tr class="${b}"><td>${o(t.label)} <span class="muted small" lang="ja">(${o(t.jaLabel)})</span></td><td>${t.correct} / ${t.total}</td><td>${r}%</td><td class="muted small">${y}</td></tr>`}).join("")}
        </tbody>
        <tfoot>
          <tr><th>Total</th><th>${i} / ${e}</th><th>${c}%</th><th class="muted small">\u2265 ${d}% target</th></tr>
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
      ${B(l.sectionResults)}

      <div class="test-nav">
        <a class="btn-primary" href="#/sitting">Try another paper</a>
        <a class="btn-secondary" href="#/home">Home</a>
      </div>
    </article>
  `,l=null}function B(a){if(!a||a.length<3)return"";const n={correct:(a[0]?.correct||0)+(a[1]?.correct||0),total:(a[0]?.total||0)+(a[1]?.total||0)},i={correct:a[2]?.correct||0,total:a[2]?.total||0},e=w(n,i);return`
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
          <tr class="${e.section1.meets_min?"pass":"fail"}">
            <td>Section 1 \u2014 Lang Knowledge + Reading</td>
            <td>${e.section1.raw_pct}%</td>
            <td>${e.section1.scaled} / ${e.section1.max}</td>
            <td class="muted small">${e.section1.meets_min?`\u2713 \u2265 ${e.section1.min}`:`\u2717 &lt; ${e.section1.min}`}</td>
          </tr>
          <tr class="${e.section2.meets_min?"pass":"fail"}">
            <td>Section 2 \u2014 Listening</td>
            <td>${e.section2.raw_pct}%</td>
            <td>${e.section2.scaled} / ${e.section2.max}</td>
            <td class="muted small">${e.section2.meets_min?`\u2713 \u2265 ${e.section2.min}`:`\u2717 &lt; ${e.section2.min}`}</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <th>Total</th>
            <th></th>
            <th>${e.total.scaled} / ${e.total.max}</th>
            <th class="muted small">${e.total.meets_min?`\u2713 \u2265 ${e.total.min}`:`\u2717 &lt; ${e.total.min}`}</th>
          </tr>
        </tfoot>
      </table>
      <p class="score-band-callout score-band-${o(e.band.tone)}">
        <strong>Estimated band:</strong> ${o(e.band.label)}
        <span class="muted small" style="display:block; margin-top:4px">${o(e.band.hint)}</span>
      </p>
    </section>
  `}export{R as renderSitting};
