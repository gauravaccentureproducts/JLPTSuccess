import{renderJa as w}from"./furigana.js";import*as u from"./storage.js";const $=10,S=50;let r=null,l="setup",p=null,g=null;async function D(){if(p&&g)return;const[s,t]=await Promise.all([fetch("data/grammar.json").then(a=>a.json()),fetch("data/questions.json").then(a=>a.json())]);p=new Map((s.patterns||[]).map(a=>[a.id,a])),g=new Map;for(const a of t.questions||[])g.has(a.grammarPatternId)||g.set(a.grammarPatternId,[]),g.get(a.grammarPatternId).push(a)}function L(s){const t=u.getHistory(),a=new Date,d=[];for(const[e,n]of Object.entries(t))n.isMastered||n.nextDue&&new Date(n.nextDue)<=a&&d.push({pid:e,entry:n,isNew:!1});return d.sort((e,n)=>new Date(e.entry.nextDue)-new Date(n.entry.nextDue)),d.slice(0,s)}function I(s,t){const a=u.getHistory(),d=new Set([...t.map(n=>n.pid),...Object.keys(a)]),e=[];for(const[n]of p)if(!d.has(n)){if(e.length>=s)break;e.push({pid:n,entry:null,isNew:!0})}return e}async function T(s){return await D(),l==="finished"&&(l="setup",r=null),l==="session"&&r?h(s):l==="finished"&&r?v(s):E(s)}function E(s){l="setup";const t=u.getSettings(),a=t.dailyNewLimit??$,d=t.dailyReviewCap??S,e=L(d),n=I(a,e);s.innerHTML=`
    <h2>Chapter 3 - Review (SRS)</h2>
    <p>Spaced-repetition session using the SM-2 algorithm. Items reappear at intervals that grow as you grade them correctly and shrink when you miss.</p>

    <section class="srs-stats">
      <div class="stat-card weak">
        <div class="stat-num">${e.length}</div>
        <div class="stat-label">Due today</div>
        <div class="stat-hint">SRS scheduled</div>
      </div>
      <div class="stat-card neutral">
        <div class="stat-num">${n.length}</div>
        <div class="stat-label">New</div>
        <div class="stat-hint">never reviewed</div>
      </div>
      <div class="stat-card mastered">
        <div class="stat-num">${e.length+n.length}</div>
        <div class="stat-label">Session size</div>
      </div>
    </section>

    <p class="muted small">Configure daily new-card limit and review cap in Settings.</p>

    ${e.length+n.length>0?`
      <button id="srs-start" class="btn-primary">Start review session</button>
    `:Object.keys(u.getHistory()).length===0?`
      <div class="empty-state">
        <p><strong>Reviews appear here after you finish your first lesson.</strong></p>
        <p class="muted small">SM-2 spaced repetition starts as soon as you've grade-rated a few patterns.</p>
        <p><a href="#/learn" class="btn-primary" style="text-decoration:none">Go to Learn</a></p>
      </div>
    `:`
      <div class="empty-state">
        <p><strong>No reviews due right now.</strong> Come back later, or start a new lesson.</p>
        <p><a href="#/learn" class="btn-primary" style="text-decoration:none">Go to Learn</a></p>
      </div>
    `}
  `,document.getElementById("srs-start")?.addEventListener("click",()=>{r={queue:[...e,...n],idx:0,grades:[],startedAt:new Date().toISOString()},l="session",h(s)})}function h(s){const t=r.queue[r.idx];if(!t)return v(s);const a=p.get(t.pid);if(!a){x(s,3);return}const e=(a.examples||[]).filter(o=>o.ja&&!o.ja.includes("(see "))[0],n=a.meaning_en||"",m=r.queue.length;s.innerHTML=`
    <div class="srs-card">
      <div class="srs-progress">
        <span>Review \xB7 Card <strong>${r.idx+1}</strong> of <strong>${m}</strong></span>
        ${t.isNew?'<span class="srs-tag new">NEW</span>':""}
      </div>
      <article class="srs-content">
        <h3 class="pattern-name">${w(a.pattern)}</h3>
        <p class="meaning-en">${f(n)}</p>
        ${e?`
          <div class="srs-example">
            <p>${w(e.ja,e.furigana||[])}</p>
            ${e.translation_en?`<p class="muted small">${f(e.translation_en)}</p>`:""}
          </div>
        `:""}
        ${a.explanation_en?`<p class="srs-explanation">${f(a.explanation_en)}</p>`:""}
      </article>

      <div class="srs-grade-row">
        <p class="muted small">Grade your recall:</p>
        <div class="srs-grade-buttons">
          <button class="grade-btn grade-again" data-grade="1">
            <span class="grade-label">Again</span>
            <span class="grade-hint">Forgot it</span>
          </button>
          <button class="grade-btn grade-hard" data-grade="3">
            <span class="grade-label">Hard</span>
            <span class="grade-hint">Correct but difficult</span>
          </button>
          <button class="grade-btn grade-good" data-grade="4">
            <span class="grade-label">Good</span>
            <span class="grade-hint">Correct, normal</span>
          </button>
          <button class="grade-btn grade-easy" data-grade="5">
            <span class="grade-label">Easy</span>
            <span class="grade-hint">Trivially correct</span>
          </button>
        </div>
      </div>

      <div class="test-nav">
        <button id="srs-end">End session</button>
        <a href="#/learn/${encodeURIComponent(t.pid)}" class="srs-link">View full lesson \u2192</a>
      </div>
    </div>
  `,s.querySelectorAll("[data-grade]").forEach(o=>{o.addEventListener("click",()=>{const c=parseInt(o.dataset.grade,10),y=u.recordSrsResponse(t.pid,c);r.grades.push({pid:t.pid,grade:c,snapshot:y}),x(s,c,{lastGraded:{pid:t.pid,grade:c,snapshot:y}})})}),document.getElementById("srs-end")?.addEventListener("click",()=>{l="finished",v(s)})}function x(s,t,a={}){r.idx+=1,r.idx>=r.queue.length?(l="finished",v(s)):(h(s),a.lastGraded&&k(s,a.lastGraded))}let i=null;function k(s,t){const a=document.getElementById("undo-grade-toast");a&&a.remove(),i&&(clearTimeout(i),i=null);const e={1:"Again",3:"Hard",4:"Good",5:"Easy"}[t.grade]||`Grade ${t.grade}`,n=document.createElement("div");n.id="undo-grade-toast",n.className="undo-toast",n.setAttribute("role","status"),n.setAttribute("aria-live","polite"),n.innerHTML=`
    <span class="undo-toast-text">Recorded: <strong>${e}</strong></span>
    <button type="button" class="undo-toast-btn" id="undo-grade-btn">\u21B6 Undo</button>
  `,document.body.appendChild(n),document.getElementById("undo-grade-btn").addEventListener("click",()=>{if(u.undoSrsResponse(t.pid,t.snapshot)){const o=r.grades.findIndex(c=>c.pid===t.pid&&c.grade===t.grade);o>=0&&r.grades.splice(o,1)}b()}),n.addEventListener("mouseenter",()=>{i&&(clearTimeout(i),i=null)}),n.addEventListener("mouseleave",()=>{i||(i=setTimeout(b,2e3))}),i=setTimeout(b,2e3)}function b(){i&&(clearTimeout(i),i=null);const s=document.getElementById("undo-grade-toast");s&&s.remove()}function v(s){const t={1:0,3:0,4:0,5:0};for(const e of r.grades)t[e.grade]=(t[e.grade]||0)+1;const a=r.grades.length,d=r.grades.map(({pid:e,grade:n})=>{const m=p.get(e),o=u.getSrsState(e);return{label:m?.pattern||e,grade:n,nextDue:o?.nextDue,interval:o?.interval}});s.innerHTML=`
    <div class="srs-finished">
      <h2>Review complete</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${a}</div><div class="stat-label">Total cards</div></div>
        <div class="stat-card weak"><div class="stat-num">${t[1]}</div><div class="stat-label">Again</div></div>
        <div class="stat-card neutral"><div class="stat-num">${t[3]+t[4]}</div><div class="stat-label">Hard / Good</div></div>
        <div class="stat-card mastered"><div class="stat-num">${t[5]}</div><div class="stat-label">Easy</div></div>
      </section>

      <h3>Schedule</h3>
      <ul class="srs-schedule">
        ${d.map(e=>`
          <li>
            <span lang="ja"><strong>${f(e.label)}</strong></span>
            <span class="muted small">grade ${e.grade}, next in ${e.interval}d (${e.nextDue?new Date(e.nextDue).toLocaleDateString():"-"})</span>
          </li>
        `).join("")}
      </ul>

      <div class="test-nav">
        <button id="srs-restart" class="btn-primary">Start new session</button>
        <button id="srs-back">Back to Learn</button>
      </div>
    </div>
  `,document.getElementById("srs-restart")?.addEventListener("click",()=>{r=null,l="setup",E(s)}),document.getElementById("srs-back")?.addEventListener("click",()=>{location.hash="#/learn"})}function f(s){return String(s??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{T as renderReview};
