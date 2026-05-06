import"./storage.js";const h=[["mojigoi","Moji + Goi","\u6587\u5B57\u30FB\u8A9E\u5F59",["moji","goi"],25],["bunpoudok","Bunpou + Dokkai","\u6587\u6CD5\u30FB\u8AAD\u89E3",["bunpou","dokkai"],50],["choukai","Listening","\u8074\u89E3",["listening"],30]],S=60;let l=null,p=null,b=null;function u(n){return String(n??"").replace(/[&<>"']/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[s])}async function v(n,s){const a=await fetch(`data/papers/${n}/paper-${s}.json`);return a.ok?a.json():null}async function y(){const n=await fetch("data/listening.json");return n.ok?n.json():{items:[]}}function k(n){const s=Math.floor(n/60),a=String(n%60).padStart(2,"0");return`${String(s).padStart(2,"0")}:${a}`}function T(n,s,a){b=Date.now()+n*1e3,p&&clearInterval(p),p=setInterval(()=>{const i=Math.max(0,Math.ceil((b-Date.now())/1e3));s(i),i<=0&&(clearInterval(p),p=null,a())},1e3),s(n)}async function P(n,s){const a=(s||"").split("/").filter(Boolean);if(a.length===0)return w(n);const i=parseInt(a[0],10);if(!Number.isFinite(i)||i<1||i>7){n.innerHTML='<p>Bad paper number. <a href="#/sitting">Pick again.</a></p>';return}if(a[1]==="result")return I(n,i);const r=a[1]?parseInt(a[1],10):0;if(!Number.isFinite(r)||r<0||r>=h.length){n.innerHTML='<p>Bad section. <a href="#/sitting">Restart.</a></p>';return}return L(n,i,r)}function w(n){n.innerHTML=`
    <article class="sitting-picker">
      <a class="back-link" href="#/test">\u2190 Back to Test</a>
      <h2>Full mock-test sitting</h2>
      <p class="page-lede">
        Take the entire JLPT N5 in one sitting: <strong>Moji + Goi (25 min)</strong>
        \u2192 break \u2192 <strong>Bunpou + Dokkai (50 min)</strong> \u2192 break \u2192
        <strong>Listening (30 min)</strong>. Total ~110 minutes
        including breaks. Each section runs at the official time budget;
        unanswered questions auto-submit at zero.
      </p>
      <p class="muted">Pick a paper number. All 4 sections from that paper number combine into one sitting.</p>
      <div class="sitting-paper-grid">
        ${[1,2,3,4,5,6,7].map(s=>`
          <a class="sitting-paper-card" href="#/sitting/${s}/0">
            <span class="card-index" aria-hidden="true">${String(s).padStart(2,"0")}</span>
            <h3>Paper ${s}</h3>
            <p class="muted small">moji-${s} \xB7 goi-${s} \xB7 bunpou-${s} \xB7 dokkai-${s} \xB7 listening</p>
          </a>
        `).join("")}
      </div>
    </article>
  `}async function L(n,s,a){const[,i,r,c,m]=h[a];(!l||l.paperNumber!==s)&&(l={paperNumber:s,currentSection:a,startedAt:new Date().toISOString(),sectionResults:[],answers:{}});let d=[];if(c[0]==="listening")d=((await y()).items||[]).slice(0,12).map(e=>({id:e.id,stem_html:e.title_ja||e.id,audio:e.audio,script_ja:e.script_ja,prompt_ja:e.prompt_ja,choices:e.choices||[],correctIndex:(e.choices||[]).findIndex(o=>o===e.correctAnswer),kind:"listening"}));else for(const t of c){const e=await v(t,s);e&&d.push(...e.questions.map(o=>({...o,kind:t})))}if(d.length===0){n.innerHTML=`<p>No questions for section ${a}. <a href="#/sitting">Restart.</a></p>`;return}const g=()=>{let t=0;for(const e of d){const o=l.answers[e.id];typeof o=="number"&&o===e.correctIndex&&(t+=1)}l.sectionResults[a]={label:i,jaLabel:r,total:d.length,correct:t,durationSec:m*60},a+1<h.length?M(n,s,a+1):location.hash=`#/sitting/${s}/result`},f=d.length;n.innerHTML=`
    <article class="sitting-section">
      <header class="sitting-section-header">
        <span class="sitting-section-label" lang="ja">${u(r)}</span>
        <h2>${u(i)} <span class="muted small">(Paper ${s}, ${f} questions)</span></h2>
        <p class="sitting-timer-chip" id="sitting-timer" aria-live="polite">${k(m*60)}</p>
      </header>
      <form id="sitting-form" class="sitting-form">
        ${d.map((t,e)=>`
          <fieldset class="sitting-question" id="sq-${u(t.id)}">
            <legend>Q${e+1}</legend>
            ${t.audio?`<audio class="example-audio" controls preload="metadata" src="${u(t.audio)}"></audio>`:""}
            ${t.stem_html?`<p class="sitting-stem" lang="ja">${t.stem_html}</p>`:""}
            ${t.prompt_ja?`<p class="sitting-prompt" lang="ja">${u(t.prompt_ja)}</p>`:""}
            ${t.script_ja&&!t.audio?`<p class="sitting-script" lang="ja">${u(t.script_ja)}</p>`:""}
            <div class="sitting-choices">
              ${(t.choices||[]).map((o,$)=>`
                <label>
                  <input type="radio" name="${u(t.id)}" value="${$}">
                  <span lang="ja">${u(o)}</span>
                </label>
              `).join("")}
            </div>
          </fieldset>
        `).join("")}
        <div class="sitting-actions">
          <button type="submit" class="btn-primary">Submit section ${a+1} of ${h.length}</button>
        </div>
      </form>
    </article>
  `,document.getElementById("sitting-form").addEventListener("submit",t=>{t.preventDefault(),p&&clearInterval(p),p=null;for(const e of d){const o=document.querySelector(`input[name="${e.id}"]:checked`);o&&(l.answers[e.id]=parseInt(o.value,10))}g()}),document.getElementById("sitting-form").addEventListener("change",t=>{if(t.target.tagName==="INPUT"){const e=d.find(o=>o.id===t.target.name);e&&(l.answers[e.id]=parseInt(t.target.value,10))}}),T(m*60,t=>{const e=document.getElementById("sitting-timer");e&&(e.textContent=k(t)),t<=60&&e&&e.classList.add("danger")},()=>{for(const t of d){const e=document.querySelector(`input[name="${t.id}"]:checked`);e&&(l.answers[t.id]=parseInt(e.value,10))}g()})}function M(n,s,a){const[,i,r]=h[a];let c=S;n.innerHTML=`
    <article class="sitting-break">
      <h2>Break</h2>
      <p class="page-lede">Stretch. Get water. Section <strong>${a+1}</strong> (${u(i)} / <span lang="ja">${u(r)}</span>) starts in <strong id="break-countdown">${c}</strong>s.</p>
      <div class="sitting-break-actions">
        <a class="btn-primary" href="#/sitting/${s}/${a}" id="skip-break">Skip break, start now</a>
      </div>
    </article>
  `,p&&clearInterval(p),p=setInterval(()=>{c-=1;const m=document.getElementById("break-countdown");m&&(m.textContent=String(c)),c<=0&&(clearInterval(p),p=null,location.hash=`#/sitting/${s}/${a}`)},1e3)}function I(n,s){if(!l||!l.sectionResults||l.sectionResults.length<h.length){n.innerHTML='<p>No completed sitting in memory. <a href="#/sitting">Start again.</a></p>';return}let a=0,i=0;for(const t of l.sectionResults)a+=t.correct,i+=t.total;const r=i>0?Math.round(100*a/i):0,c=60,m=[63,61,79],d="~19 / section",g=l.sectionResults.map((t,e)=>(t.total?100*t.correct/t.total:0)>=m[e]),f=g.every(Boolean);n.innerHTML=`
    <article class="sitting-result">
      <h2>JLPT N5 Mock - Paper ${s} - Result</h2>
      <p class="page-lede">
        Total: <strong>${a} / ${i}</strong> (${r}%) \xB7
        ${r>=c&&f?'<span class="pass-badge pass">Pass \xB7 all section minimums met</span>':r>=c?`<span class="pass-badge fail">Overall ${r}% (\u2265${c}%) but a section is below its minimum</span>`:`<span class="pass-badge fail">Below ${c}% study-target</span>`}
      </p>
      <p class="muted small" style="margin-top:-4px;">
        Real JLPT N5 official pass mark = 80 / 180 (44.4%) with section minimums of 19 / 60 (~32% per section after scoring scale). Study target \u2265 ${c}% is the conservative bar matching Bunpro / Try! N5 guidance.
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
          ${l.sectionResults.map((t,e)=>{const o=t.total?Math.round(100*t.correct/t.total):0,$=g[e]?"pass":"fail",j=g[e]?"\u2713 met":`\u2717 ${m[e]}%`;return`<tr class="${$}"><td>${u(t.label)} <span class="muted small" lang="ja">(${u(t.jaLabel)})</span></td><td>${t.correct} / ${t.total}</td><td>${o}%</td><td class="muted small">${j}</td></tr>`}).join("")}
        </tbody>
        <tfoot>
          <tr><th>Total</th><th>${a} / ${i}</th><th>${r}%</th><th class="muted small">\u2265 ${c}% target</th></tr>
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
  `,l=null}export{P as renderSitting};
