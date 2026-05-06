import"./storage.js";const m=[["mojigoi","Moji + Goi","\u6587\u5B57\u30FB\u8A9E\u5F59",["moji","goi"],25],["bunpoudok","Bunpou + Dokkai","\u6587\u6CD5\u30FB\u8AAD\u89E3",["bunpou","dokkai"],50],["choukai","Listening","\u8074\u89E3",["listening"],30]],j=60;let o=null,p=null,h=null;function g(n){return String(n??"").replace(/[&<>"']/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[s])}async function S(n,s){const a=await fetch(`data/papers/${n}/paper-${s}.json`);return a.ok?a.json():null}async function v(){const n=await fetch("data/listening.json");return n.ok?n.json():{items:[]}}function $(n){const s=Math.floor(n/60),a=String(n%60).padStart(2,"0");return`${String(s).padStart(2,"0")}:${a}`}function y(n,s,a){h=Date.now()+n*1e3,p&&clearInterval(p),p=setInterval(()=>{const i=Math.max(0,Math.ceil((h-Date.now())/1e3));s(i),i<=0&&(clearInterval(p),p=null,a())},1e3),s(n)}async function I(n,s){const a=(s||"").split("/").filter(Boolean);if(a.length===0)return w(n);const i=parseInt(a[0],10);if(!Number.isFinite(i)||i<1||i>7){n.innerHTML='<p>Bad paper number. <a href="#/sitting">Pick again.</a></p>';return}if(a[1]==="result")return T(n,i);const d=a[1]?parseInt(a[1],10):0;if(!Number.isFinite(d)||d<0||d>=m.length){n.innerHTML='<p>Bad section. <a href="#/sitting">Restart.</a></p>';return}return L(n,i,d)}function w(n){n.innerHTML=`
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
  `}async function L(n,s,a){const[,i,d,u,r]=m[a];(!o||o.paperNumber!==s)&&(o={paperNumber:s,currentSection:a,startedAt:new Date().toISOString(),sectionResults:[],answers:{}});let l=[];if(u[0]==="listening")l=((await v()).items||[]).slice(0,12).map(e=>({id:e.id,stem_html:e.title_ja||e.id,audio:e.audio,script_ja:e.script_ja,prompt_ja:e.prompt_ja,choices:e.choices||[],correctIndex:(e.choices||[]).findIndex(c=>c===e.correctAnswer),kind:"listening"}));else for(const t of u){const e=await S(t,s);e&&l.push(...e.questions.map(c=>({...c,kind:t})))}if(l.length===0){n.innerHTML=`<p>No questions for section ${a}. <a href="#/sitting">Restart.</a></p>`;return}const f=()=>{let t=0;for(const e of l){const c=o.answers[e.id];typeof c=="number"&&c===e.correctIndex&&(t+=1)}o.sectionResults[a]={label:i,jaLabel:d,total:l.length,correct:t,durationSec:r*60},a+1<m.length?M(n,s,a+1):location.hash=`#/sitting/${s}/result`},b=l.length;n.innerHTML=`
    <article class="sitting-section">
      <header class="sitting-section-header">
        <span class="sitting-section-label" lang="ja">${g(d)}</span>
        <h2>${g(i)} <span class="muted small">(Paper ${s}, ${b} questions)</span></h2>
        <p class="sitting-timer-chip" id="sitting-timer" aria-live="polite">${$(r*60)}</p>
      </header>
      <form id="sitting-form" class="sitting-form">
        ${l.map((t,e)=>`
          <fieldset class="sitting-question" id="sq-${g(t.id)}">
            <legend>Q${e+1}</legend>
            ${t.audio?`<audio class="example-audio" controls preload="metadata" src="${g(t.audio)}"></audio>`:""}
            ${t.stem_html?`<p class="sitting-stem" lang="ja">${t.stem_html}</p>`:""}
            ${t.prompt_ja?`<p class="sitting-prompt" lang="ja">${g(t.prompt_ja)}</p>`:""}
            ${t.script_ja&&!t.audio?`<p class="sitting-script" lang="ja">${g(t.script_ja)}</p>`:""}
            <div class="sitting-choices">
              ${(t.choices||[]).map((c,k)=>`
                <label>
                  <input type="radio" name="${g(t.id)}" value="${k}">
                  <span lang="ja">${g(c)}</span>
                </label>
              `).join("")}
            </div>
          </fieldset>
        `).join("")}
        <div class="sitting-actions">
          <button type="submit" class="btn-primary">Submit section ${a+1} of ${m.length}</button>
        </div>
      </form>
    </article>
  `,document.getElementById("sitting-form").addEventListener("submit",t=>{t.preventDefault(),p&&clearInterval(p),p=null;for(const e of l){const c=document.querySelector(`input[name="${e.id}"]:checked`);c&&(o.answers[e.id]=parseInt(c.value,10))}f()}),document.getElementById("sitting-form").addEventListener("change",t=>{if(t.target.tagName==="INPUT"){const e=l.find(c=>c.id===t.target.name);e&&(o.answers[e.id]=parseInt(t.target.value,10))}}),y(r*60,t=>{const e=document.getElementById("sitting-timer");e&&(e.textContent=$(t)),t<=60&&e&&e.classList.add("danger")},()=>{for(const t of l){const e=document.querySelector(`input[name="${t.id}"]:checked`);e&&(o.answers[t.id]=parseInt(e.value,10))}f()})}function M(n,s,a){const[,i,d]=m[a];let u=j;n.innerHTML=`
    <article class="sitting-break">
      <h2>Break</h2>
      <p class="page-lede">Stretch. Get water. Section <strong>${a+1}</strong> (${g(i)} / <span lang="ja">${g(d)}</span>) starts in <strong id="break-countdown">${u}</strong>s.</p>
      <div class="sitting-break-actions">
        <a class="btn-primary" href="#/sitting/${s}/${a}" id="skip-break">Skip break, start now</a>
      </div>
    </article>
  `,p&&clearInterval(p),p=setInterval(()=>{u-=1;const r=document.getElementById("break-countdown");r&&(r.textContent=String(u)),u<=0&&(clearInterval(p),p=null,location.hash=`#/sitting/${s}/${a}`)},1e3)}function T(n,s){if(!o||!o.sectionResults||o.sectionResults.length<m.length){n.innerHTML='<p>No completed sitting in memory. <a href="#/sitting">Start again.</a></p>';return}let a=0,i=0;for(const r of o.sectionResults)a+=r.correct,i+=r.total;const d=i>0?Math.round(100*a/i):0,u=60;n.innerHTML=`
    <article class="sitting-result">
      <h2>Sitting complete - Paper ${s}</h2>
      <p class="page-lede">
        Score: <strong>${a} / ${i}</strong> (${d}%) \xB7
        ${d>=u?`<span class="pass-badge pass">Pass \xB7 \u2265 ${u}%</span>`:`<span class="pass-badge fail">Below pass \xB7 target ${u}%</span>`}
      </p>
      <table class="category-table">
        <thead><tr><th>Section</th><th>Score</th><th>%</th></tr></thead>
        <tbody>
          ${o.sectionResults.map(r=>{const l=r.total?Math.round(100*r.correct/r.total):0;return`<tr class="${l>=u?"pass":"fail"}"><td>${g(r.label)} <span class="muted small" lang="ja">(${g(r.jaLabel)})</span></td><td>${r.correct} / ${r.total}</td><td>${l}%</td></tr>`}).join("")}
        </tbody>
      </table>
      <div class="test-nav">
        <a class="btn-primary" href="#/sitting">Try another paper</a>
        <a class="btn-secondary" href="#/home">Home</a>
      </div>
    </article>
  `,o=null}export{I as renderSitting};
