import"./storage.js";import{t as g}from"./i18n.js";const f=[["mojigoi","Moji + Goi","\u6587\u5B57\u30FB\u8A9E\u5F59",["moji","goi"],25],["bunpoudok","Bunpou + Dokkai","\u6587\u6CD5\u30FB\u8AAD\u89E3",["bunpou","dokkai"],50],["choukai","Listening","\u8074\u89E3",["listening"],30]],v=60;let c=null,d=null,k=null;function i(n){return String(n??"").replace(/[&<>"']/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[s])}async function y(n,s){const a=await fetch(`data/papers/${n}/paper-${s}.json`);return a.ok?a.json():null}async function _(){const n=await fetch("data/listening.json");return n.ok?n.json():{items:[]}}function S(n){const s=Math.floor(n/60),a=String(n%60).padStart(2,"0");return`${String(s).padStart(2,"0")}:${a}`}function w(n,s,a){k=Date.now()+n*1e3,d&&clearInterval(d),d=setInterval(()=>{const r=Math.max(0,Math.ceil((k-Date.now())/1e3));s(r),r<=0&&(clearInterval(d),d=null,a())},1e3),s(n)}async function P(n,s){const a=(s||"").split("/").filter(Boolean);if(a.length===0)return T(n);const r=parseInt(a[0],10);if(!Number.isFinite(r)||r<1||r>7){n.innerHTML=`<p>${i(g("meta.bad_paper"))} <a href="#/sitting">${i(g("meta.pick_again"))}</a></p>`;return}if(a[1]==="result")return I(n,r);const l=a[1]?parseInt(a[1],10):0;if(!Number.isFinite(l)||l<0||l>=f.length){n.innerHTML=`<p>${i(g("meta.bad_section"))} <a href="#/sitting">${i(g("meta.pick_again"))}</a></p>`;return}return L(n,r,l)}function T(n){n.innerHTML=`
    <article class="sitting-picker">
      <a class="back-link" href="#/test">\u2190 ${i(g("meta.back_to_test"))}</a>
      <h2>${i(g("meta.sitting_title"))}</h2>
      <p class="page-lede">${i(g("meta.sitting_intro"))}</p>
      <p class="muted">${i(g("meta.pick_paper_intro"))}</p>
      <div class="sitting-paper-grid">
        ${[1,2,3,4,5,6,7].map(s=>`
          <a class="sitting-paper-card" href="#/sitting/${s}/0">
            <span class="card-index" aria-hidden="true">${String(s).padStart(2,"0")}</span>
            <h3>${i(g("meta.paper_n").replace("${n}",s))}</h3>
            <p class="muted small">moji-${s} \xB7 goi-${s} \xB7 bunpou-${s} \xB7 dokkai-${s} \xB7 listening</p>
          </a>
        `).join("")}
      </div>
    </article>
  `}async function L(n,s,a){const[,r,l,p,u]=f[a];(!c||c.paperNumber!==s)&&(c={paperNumber:s,currentSection:a,startedAt:new Date().toISOString(),sectionResults:[],answers:{}});let m=[];if(p[0]==="listening")m=((await _()).items||[]).slice(0,12).map(e=>({id:e.id,stem_html:e.title_ja||e.id,audio:e.audio,script_ja:e.script_ja,prompt_ja:e.prompt_ja,choices:e.choices||[],correctIndex:(e.choices||[]).findIndex(o=>o===e.correctAnswer),kind:"listening"}));else for(const t of p){const e=await y(t,s);e&&m.push(...e.questions.map(o=>({...o,kind:t})))}if(m.length===0){n.innerHTML=`<p>No questions for section ${a}. <a href="#/sitting">Restart.</a></p>`;return}const h=()=>{let t=0;for(const e of m){const o=c.answers[e.id];typeof o=="number"&&o===e.correctIndex&&(t+=1)}c.sectionResults[a]={label:r,jaLabel:l,total:m.length,correct:t,durationSec:u*60},a+1<f.length?M(n,s,a+1):location.hash=`#/sitting/${s}/result`},$=m.length;n.innerHTML=`
    <article class="sitting-section">
      <header class="sitting-section-header">
        <span class="sitting-section-label" lang="ja">${i(l)}</span>
        <h2>${i(r)} <span class="muted small">(Paper ${s}, ${$} questions)</span></h2>
        <p class="sitting-timer-chip" id="sitting-timer" aria-live="polite">${S(u*60)}</p>
      </header>
      <form id="sitting-form" class="sitting-form">
        ${m.map((t,e)=>`
          <fieldset class="sitting-question" id="sq-${i(t.id)}">
            <legend>Q${e+1}</legend>
            ${t.audio?`<audio class="example-audio" controls preload="metadata" src="${i(t.audio)}"></audio>`:""}
            ${t.stem_html?`<p class="sitting-stem" lang="ja">${t.stem_html}</p>`:""}
            ${t.prompt_ja?`<p class="sitting-prompt" lang="ja">${i(t.prompt_ja)}</p>`:""}
            ${t.script_ja&&!t.audio?`<p class="sitting-script" lang="ja">${i(t.script_ja)}</p>`:""}
            <div class="sitting-choices">
              ${(t.choices||[]).map((o,b)=>`
                <label>
                  <input type="radio" name="${i(t.id)}" value="${b}">
                  <span lang="ja">${i(o)}</span>
                </label>
              `).join("")}
            </div>
          </fieldset>
        `).join("")}
        <div class="sitting-actions">
          <button type="submit" class="btn-primary">Submit section ${a+1} of ${f.length}</button>
        </div>
      </form>
    </article>
  `,document.getElementById("sitting-form").addEventListener("submit",t=>{t.preventDefault(),d&&clearInterval(d),d=null;for(const e of m){const o=document.querySelector(`input[name="${e.id}"]:checked`);o&&(c.answers[e.id]=parseInt(o.value,10))}h()}),document.getElementById("sitting-form").addEventListener("change",t=>{if(t.target.tagName==="INPUT"){const e=m.find(o=>o.id===t.target.name);e&&(c.answers[e.id]=parseInt(t.target.value,10))}}),w(u*60,t=>{const e=document.getElementById("sitting-timer");e&&(e.textContent=S(t)),t<=60&&e&&e.classList.add("danger")},()=>{for(const t of m){const e=document.querySelector(`input[name="${t.id}"]:checked`);e&&(c.answers[t.id]=parseInt(e.value,10))}h()})}function M(n,s,a){const[,r,l]=f[a];let p=v;n.innerHTML=`
    <article class="sitting-break">
      <h2>Break</h2>
      <p class="page-lede">Stretch. Get water. Section <strong>${a+1}</strong> (${i(r)} / <span lang="ja">${i(l)}</span>) starts in <strong id="break-countdown">${p}</strong>s.</p>
      <div class="sitting-break-actions">
        <a class="btn-primary" href="#/sitting/${s}/${a}" id="skip-break">Skip break, start now</a>
      </div>
    </article>
  `,d&&clearInterval(d),d=setInterval(()=>{p-=1;const u=document.getElementById("break-countdown");u&&(u.textContent=String(p)),p<=0&&(clearInterval(d),d=null,location.hash=`#/sitting/${s}/${a}`)},1e3)}function I(n,s){if(!c||!c.sectionResults||c.sectionResults.length<f.length){n.innerHTML='<p>No completed sitting in memory. <a href="#/sitting">Start again.</a></p>';return}let a=0,r=0;for(const t of c.sectionResults)a+=t.correct,r+=t.total;const l=r>0?Math.round(100*a/r):0,p=60,u=[63,61,79],m="~19 / section",h=c.sectionResults.map((t,e)=>(t.total?100*t.correct/t.total:0)>=u[e]),$=h.every(Boolean);n.innerHTML=`
    <article class="sitting-result">
      <h2>JLPT N5 Mock - Paper ${s} - Result</h2>
      <p class="page-lede">
        Total: <strong>${a} / ${r}</strong> (${l}%) \xB7
        ${l>=p&&$?'<span class="pass-badge pass">Pass \xB7 all section minimums met</span>':l>=p?`<span class="pass-badge fail">Overall ${l}% (\u2265${p}%) but a section is below its minimum</span>`:`<span class="pass-badge fail">Below ${p}% study-target</span>`}
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
          ${c.sectionResults.map((t,e)=>{const o=t.total?Math.round(100*t.correct/t.total):0,b=h[e]?"pass":"fail",j=h[e]?"\u2713 met":`\u2717 ${u[e]}%`;return`<tr class="${b}"><td>${i(t.label)} <span class="muted small" lang="ja">(${i(t.jaLabel)})</span></td><td>${t.correct} / ${t.total}</td><td>${o}%</td><td class="muted small">${j}</td></tr>`}).join("")}
        </tbody>
        <tfoot>
          <tr><th>Total</th><th>${a} / ${r}</th><th>${l}%</th><th class="muted small">\u2265 ${p}% target</th></tr>
        </tfoot>
      </table>
      <p class="muted small">
        \u203B The app ships 85Q across the 3 sections (close to the official 91Q). Per-section minimums above are raw-question approximations. The official JLPT N5 score report uses a scaled-equating method that this app does not replicate \u2014 only raw-correct percentages are shown.
      </p>
      <div class="test-nav">
        <a class="btn-primary" href="#/sitting">Try another paper</a>
        <a class="btn-secondary" href="#/home">Home</a>
      </div>
    </article>
  `,c=null}export{P as renderSitting};
