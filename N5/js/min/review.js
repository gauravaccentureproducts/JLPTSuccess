import{renderJa as D}from"./furigana.js";import*as m from"./storage.js";import{t as U}from"./i18n.js";const R=10,_=50;let l=null,f="setup",y=null,$=null,w=null,k=null,x=null;async function T(){if(y&&$&&w&&x)return;const[t,a,i,r]=await Promise.all([fetch("data/grammar.json").then(e=>e.json()),fetch("data/questions.json").then(e=>e.json()),fetch("data/vocab.json").then(e=>e.json()),fetch("data/kanji.json").then(e=>e.json())]);y=new Map((t.patterns||[]).map(e=>[e.id,e])),$=new Map;for(const e of a.questions||[])$.has(e.grammarPatternId)||$.set(e.grammarPatternId,[]),$.get(e.grammarPatternId).push(e);w=new Map,k=new Map;for(const e of i.entries||[])e.form&&w.set(e.form,e),e.id&&k.set(e.id,e);x=new Map((r.entries||[]).map(e=>[e.glyph,e]))}function A(t){const a=m.getHistory(),i=new Date,r=[];for(const[e,n]of Object.entries(a))n.isMastered||n.nextDue&&new Date(n.nextDue)<=i&&r.push({pid:e,entry:n,isNew:!1});return r.sort((e,n)=>new Date(e.entry.nextDue)-new Date(n.entry.nextDue)),r.slice(0,t)}function M(t,a){const i=m.getHistory(),r=new Set([...a.map(n=>n.pid),...Object.keys(i)]),e=[];for(const[n]of y)if(!r.has(n)){if(e.length>=t)break;e.push({pid:n,entry:null,isNew:!0})}return e}async function N(t){return await T(),f==="finished"&&(f="setup",l=null),f==="session"&&l?E(t):f==="finished"&&l?I(t):L(t)}function L(t){f="setup";const a=m.getSettings(),i=a.dailyNewLimit??R,r=a.dailyReviewCap??_,e=A(r),n=M(i,e),g=m.getDueCountsBySkill(),d=g.grammar+g.vocab+g.kanji;t.innerHTML=`
    <h2>${U("page.review")} <span class="srs-mode-badge" aria-label="Mixed skill drill">Mixed drill</span></h2>
    <p>Spaced-repetition session using the SM-2 algorithm. Items reappear at intervals that grow as you grade them correctly and shrink when you miss. <strong>Grammar, vocab and kanji items are interleaved round-robin in the same session</strong> so you get a single mixed 15-min drill instead of three separate loops (IMP-144).</p>

    ${d>0?`
      <!-- IMP-092 Phase 2A + IMP-144 (2026-05-09): mixed-skill summary -->
      <section class="srs-unified-summary" aria-label="Today's reviews across all skills">
        <h3 style="margin:0 0 8px; font-weight:500;">Today: <strong>${d}</strong> review${d===1?"":"s"} due across all skills</h3>
        <p class="muted small" style="margin:0 0 12px;">
          ${g.grammar} grammar \xB7 ${g.vocab} vocab \xB7 ${g.kanji} kanji
          <span style="margin-left:8px;">(see <a href="#/summary">Progress dashboard</a> for forecast)</span>
        </p>
      </section>
    `:""}

    <section class="srs-stats">
      <div class="stat-card weak">
        <div class="stat-num">${e.length}</div>
        <div class="stat-label">Grammar due</div>
        <div class="stat-hint">SRS scheduled</div>
      </div>
      <div class="stat-card neutral">
        <div class="stat-num">${n.length}</div>
        <div class="stat-label">New grammar</div>
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
    `:Object.keys(m.getHistory()).length===0?`
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
  `,document.getElementById("srs-start")?.addEventListener("click",()=>{const h=[...e,...n].map(p=>({skill:"grammar",id:p.pid,entry:p.entry,isNew:p.isNew})),c=(m.getUnifiedDueQueue?m.getUnifiedDueQueue():[]).filter(p=>p.skill!=="grammar"),v=[],b=[h,c];for(;b.some(p=>p.length>0);)for(const p of b)p.length>0&&v.push(p.shift());l={queue:v,idx:0,grades:[],startedAt:new Date().toISOString()},f="session",E(t)})}function E(t){const a=l.queue[l.idx];if(!a)return I(t);const i=a.skill||"grammar",r=a.id||a.pid,e=l.queue.length,n={grammar:{label:"\u6587",cls:"srs-skill-grammar",name:"Grammar"},vocab:{label:"\u8A9E",cls:"srs-skill-vocab",name:"Vocab"},kanji:{label:"\u6F22",cls:"srs-skill-kanji",name:"Kanji"}},g=n[i]||n.grammar;let d="",h=`#/learn/${encodeURIComponent(r)}`;if(i==="grammar"){const s=y.get(r);if(!s){j(t,3);return}const v=(s.examples||[]).filter(p=>p.ja&&!p.ja.includes("(see "))[0],b=s.meaning_en||"";d=`
      <h3 class="pattern-name">${D(s.pattern)}</h3>
      <p class="meaning-en">${o(b)}</p>
      ${v?`
        <div class="srs-example">
          <p>${D(v.ja,v.furigana||[])}</p>
          ${v.translation_en?`<p class="muted small">${o(v.translation_en)}</p>`:""}
        </div>
      `:""}
      ${s.explanation_en?`<p class="srs-explanation">${o(s.explanation_en)}</p>`:""}
    `}else if(i==="vocab"){const s=k&&k.get(r)||w&&w.get(r);if(!s){j(t,3);return}const c=s.examples&&s.examples[0]||null;d=`
      <h3 class="pattern-name" lang="ja">${o(s.form||"")}</h3>
      <p class="meaning-en"><span lang="ja" class="vocab-reading">${o(s.reading||"")}</span>
        ${s.pos?`<span class="muted small" style="margin-left:8px;">${o(s.pos)}</span>`:""}</p>
      <p class="meaning-en"><strong>${o(s.gloss||"")}</strong></p>
      ${s.gloss_hi?`<p class="muted small" lang="hi">${o(s.gloss_hi)}</p>`:""}
      ${c?`
        <div class="srs-example">
          <p lang="ja">${o(c.ja||c)}</p>
          ${c.translation_en?`<p class="muted small">${o(c.translation_en)}</p>`:""}
        </div>
      `:""}
      ${s.collocations&&s.collocations.length?`
        <p class="muted small">Collocations: <span lang="ja">${s.collocations.slice(0,3).map(o).join(" \xB7 ")}</span></p>
      `:""}
    `,h=s.form?`#/learn/vocab/${encodeURIComponent(s.form)}`:"#/learn/vocab"}else if(i==="kanji"){const s=x&&x.get(r);if(!s){j(t,3);return}d=`
      <h3 class="pattern-name kanji-glyph-big" lang="ja" style="font-size:5em; line-height:1;">${o(s.glyph)}</h3>
      ${s.on?.length?`<p class="meaning-en"><strong>On:</strong> <span lang="ja">${s.on.map(o).join(" / ")}</span></p>`:""}
      ${s.kun?.length?`<p class="meaning-en"><strong>Kun:</strong> <span lang="ja">${s.kun.map(o).join(" / ")}</span></p>`:""}
      ${s.meanings?.length?`<p class="meaning-en"><strong>Meaning:</strong> ${s.meanings.map(o).join(", ")}</p>`:""}
      ${s.meanings_hi?.length?`<p class="muted small" lang="hi">${s.meanings_hi.map(o).join(", ")}</p>`:""}
      ${s.mnemonic?`<p class="srs-explanation">${o(s.mnemonic)}</p>`:""}
    `,h=`#/kanji/${encodeURIComponent(s.glyph)}`}t.innerHTML=`
    <div class="srs-card">
      <div class="srs-progress">
        <span>Review \xB7 Card <strong>${l.idx+1}</strong> of <strong>${e}</strong></span>
        <span class="srs-skill-badge ${g.cls}" title="${g.name}" lang="ja">${g.label}</span>
        ${a.isNew?'<span class="srs-tag new">NEW</span>':""}
      </div>
      <article class="srs-content">
        ${d}
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
        <a href="${h}" class="srs-link">View full lesson \u2192</a>
      </div>
    </div>
  `,t.querySelectorAll("[data-grade]").forEach(s=>{s.addEventListener("click",()=>{const c=parseInt(s.dataset.grade,10),v=a.skill&&m.recordUnifiedSrsResponse,b=v?m.recordUnifiedSrsResponse(i,r,c):m.recordSrsResponse(r,c);l.grades.push({skill:i,pid:r,grade:c,snapshot:b}),j(t,c,{lastGraded:{skill:i,pid:r,grade:c,snapshot:b,isUnified:v}})})}),document.getElementById("srs-end")?.addEventListener("click",()=>{f="finished",I(t)})}function j(t,a,i={}){l.idx+=1,l.idx>=l.queue.length?(f="finished",I(t)):(E(t),i.lastGraded&&B(t,i.lastGraded))}let u=null;function B(t,a){const i=document.getElementById("undo-grade-toast");i&&i.remove(),u&&(clearTimeout(u),u=null);const e={1:"Again",3:"Hard",4:"Good",5:"Easy"}[a.grade]||`Grade ${a.grade}`,n=document.createElement("div");n.id="undo-grade-toast",n.className="undo-toast",n.setAttribute("role","status"),n.setAttribute("aria-live","polite"),n.innerHTML=`
    <span class="undo-toast-text">Recorded: <strong>${e}</strong></span>
    <button type="button" class="undo-toast-btn" id="undo-grade-btn">\u21B6 Undo</button>
  `,document.body.appendChild(n),document.getElementById("undo-grade-btn").addEventListener("click",()=>{if(a.isUnified&&m.undoUnifiedSrsResponse?m.undoUnifiedSrsResponse(a.skill,a.pid,a.snapshot):m.undoSrsResponse(a.pid,a.snapshot)){const d=l.grades.findIndex(h=>h.pid===a.pid&&h.grade===a.grade);d>=0&&l.grades.splice(d,1)}S()}),n.addEventListener("mouseenter",()=>{u&&(clearTimeout(u),u=null)}),n.addEventListener("mouseleave",()=>{u||(u=setTimeout(S,2e3))}),u=setTimeout(S,2e3)}function S(){u&&(clearTimeout(u),u=null);const t=document.getElementById("undo-grade-toast");t&&t.remove()}function I(t){const a={1:0,3:0,4:0,5:0};for(const e of l.grades)a[e.grade]=(a[e.grade]||0)+1;const i=l.grades.length,r=l.grades.map(({pid:e,grade:n})=>{const g=y.get(e),d=m.getSrsState(e);return{label:g?.pattern||e,grade:n,nextDue:d?.nextDue,interval:d?.interval}});t.innerHTML=`
    <div class="srs-finished">
      <h2>Review complete</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${i}</div><div class="stat-label">Total cards</div></div>
        <div class="stat-card weak"><div class="stat-num">${a[1]}</div><div class="stat-label">Again</div></div>
        <div class="stat-card neutral"><div class="stat-num">${a[3]+a[4]}</div><div class="stat-label">Hard / Good</div></div>
        <div class="stat-card mastered"><div class="stat-num">${a[5]}</div><div class="stat-label">Easy</div></div>
      </section>

      <h3>Schedule</h3>
      <ul class="srs-schedule">
        ${r.map(e=>`
          <li>
            <span lang="ja"><strong>${o(e.label)}</strong></span>
            <span class="muted small">grade ${e.grade}, next in ${e.interval}d (${e.nextDue?new Date(e.nextDue).toLocaleDateString():"-"})</span>
          </li>
        `).join("")}
      </ul>

      <div class="test-nav">
        <button id="srs-restart" class="btn-primary">Start new session</button>
        <button id="srs-back">Back to Learn</button>
      </div>
    </div>
  `,document.getElementById("srs-restart")?.addEventListener("click",()=>{l=null,f="setup",L(t)}),document.getElementById("srs-back")?.addEventListener("click",()=>{location.hash="#/learn"})}function o(t){return String(t??"").replace(/[&<>"']/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[a])}export{N as renderReview};
