import{renderJa as U}from"./furigana.js";import*as c from"./storage.js";import{t as _}from"./i18n.js";const T=10,A=50;let o=null,v="setup",k=null,w=null,y=null,$=null,x=null;async function C(){if(k&&w&&y&&x)return;const[t,a,i,r]=await Promise.all([fetch("data/grammar.json").then(e=>e.json()),fetch("data/questions.json").then(e=>e.json()),fetch("data/vocab.json").then(e=>e.json()),fetch("data/kanji.json").then(e=>e.json())]);k=new Map((t.patterns||[]).map(e=>[e.id,e])),w=new Map;for(const e of a.questions||[])w.has(e.grammarPatternId)||w.set(e.grammarPatternId,[]),w.get(e.grammarPatternId).push(e);y=new Map,$=new Map;for(const e of i.entries||[])e.form&&y.set(e.form,e),e.id&&$.set(e.id,e);x=new Map((r.entries||[]).map(e=>[e.glyph,e]))}function B(t){const a=c.getHistory(),i=new Date,r=[];for(const[e,n]of Object.entries(a))n.isMastered||n.nextDue&&new Date(n.nextDue)<=i&&r.push({pid:e,entry:n,isNew:!1});return r.sort((e,n)=>new Date(e.entry.nextDue)-new Date(n.entry.nextDue)),r.slice(0,t)}function q(t,a){const i=c.getHistory(),r=new Set([...a.map(n=>n.pid),...Object.keys(i)]),e=[];for(const[n]of k)if(!r.has(n)){if(e.length>=t)break;e.push({pid:n,entry:null,isNew:!0})}return e}async function G(t){return await C(),v==="finished"&&(v="setup",o=null),v==="session"&&o?I(t):v==="finished"&&o?S(t):M(t)}function M(t){v="setup";const a=c.getSettings(),i=a.dailyNewLimit??T,r=a.dailyReviewCap??A,e=B(r),n=q(i,e),u=c.getDueCountsBySkill(),m=u.grammar+u.vocab+u.kanji;t.innerHTML=`
    <h2>${_("page.review")} <span class="srs-mode-badge" aria-label="Mixed skill drill">Mixed drill</span></h2>
    <p>Spaced-repetition session using the SM-2 algorithm. Items reappear at intervals that grow as you grade them correctly and shrink when you miss. <strong>Grammar, vocab and kanji items are interleaved round-robin in the same session</strong> so you get a single mixed 15-min drill instead of three separate loops (IMP-144).</p>

    ${m>0?`
      <!-- IMP-092 Phase 2A + IMP-144 (2026-05-09): mixed-skill summary -->
      <section class="srs-unified-summary" aria-label="Today's reviews across all skills">
        <h3 style="margin:0 0 8px; font-weight:500;">Today: <strong>${m}</strong> review${m===1?"":"s"} due across all skills</h3>
        <p class="muted small" style="margin:0 0 12px;">
          ${u.grammar} grammar \xB7 ${u.vocab} vocab \xB7 ${u.kanji} kanji
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
    `:Object.keys(c.getHistory()).length===0?`
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
  `,document.getElementById("srs-start")?.addEventListener("click",()=>{const h=[...e,...n].map(g=>({skill:"grammar",id:g.pid,entry:g.entry,isNew:g.isNew}));let l=(c.getUnifiedDueQueue?c.getUnifiedDueQueue():[]).filter(g=>g.skill!=="grammar");if(c.isSrsGatingEnabled&&c.isSrsGatingEnabled()){const g=l.length;l=l.filter(E=>{if(E.skill!=="vocab")return!0;const R=$&&$.get(E.id)||y&&y.get(E.id);return R?c.vocabKanjiPrerequisitesMet(R.form||""):!0});const L=l.length;g!==L&&console.info(`[IMP-145] SRS gating filtered ${g-L} kanji-locked vocab item(s) from queue.`)}const f=[],b=[h,l];for(;b.some(g=>g.length>0);)for(const g of b)g.length>0&&f.push(g.shift());o={queue:f,idx:0,grades:[],startedAt:new Date().toISOString()},v="session",I(t)})}function I(t){const a=o.queue[o.idx];if(!a)return S(t);const i=a.skill||"grammar",r=a.id||a.pid,e=o.queue.length,n={grammar:{label:"\u6587",cls:"srs-skill-grammar",name:"Grammar"},vocab:{label:"\u8A9E",cls:"srs-skill-vocab",name:"Vocab"},kanji:{label:"\u6F22",cls:"srs-skill-kanji",name:"Kanji"}},u=n[i]||n.grammar;let m="",h=`#/learn/${encodeURIComponent(r)}`;if(i==="grammar"){const s=k.get(r);if(!s){j(t,3);return}const f=(s.examples||[]).filter(g=>g.ja&&!g.ja.includes("(see "))[0],b=s.meaning_en||"";m=`
      <h3 class="pattern-name">${U(s.pattern)}</h3>
      <p class="meaning-en">${d(b)}</p>
      ${f?`
        <div class="srs-example">
          <p>${U(f.ja,f.furigana||[])}</p>
          ${f.translation_en?`<p class="muted small">${d(f.translation_en)}</p>`:""}
        </div>
      `:""}
      ${s.explanation_en?`<p class="srs-explanation">${d(s.explanation_en)}</p>`:""}
    `}else if(i==="vocab"){const s=$&&$.get(r)||y&&y.get(r);if(!s){j(t,3);return}const l=s.examples&&s.examples[0]||null;m=`
      <h3 class="pattern-name" lang="ja">${d(s.form||"")}</h3>
      <p class="meaning-en"><span lang="ja" class="vocab-reading">${d(s.reading||"")}</span>
        ${s.pos?`<span class="muted small" style="margin-left:8px;">${d(s.pos)}</span>`:""}</p>
      <p class="meaning-en"><strong>${d(s.gloss||"")}</strong></p>
      ${s.gloss_hi?`<p class="muted small" lang="hi">${d(s.gloss_hi)}</p>`:""}
      ${l?`
        <div class="srs-example">
          <p lang="ja">${d(l.ja||l)}</p>
          ${l.translation_en?`<p class="muted small">${d(l.translation_en)}</p>`:""}
        </div>
      `:""}
      ${s.collocations&&s.collocations.length?`
        <p class="muted small">Collocations: <span lang="ja">${s.collocations.slice(0,3).map(d).join(" \xB7 ")}</span></p>
      `:""}
    `,h=s.form?`#/learn/vocab/${encodeURIComponent(s.form)}`:"#/learn/vocab"}else if(i==="kanji"){const s=x&&x.get(r);if(!s){j(t,3);return}m=`
      <h3 class="pattern-name kanji-glyph-big" lang="ja" style="font-size:5em; line-height:1;">${d(s.glyph)}</h3>
      ${s.on?.length?`<p class="meaning-en"><strong>On:</strong> <span lang="ja">${s.on.map(d).join(" / ")}</span></p>`:""}
      ${s.kun?.length?`<p class="meaning-en"><strong>Kun:</strong> <span lang="ja">${s.kun.map(d).join(" / ")}</span></p>`:""}
      ${s.meanings?.length?`<p class="meaning-en"><strong>Meaning:</strong> ${s.meanings.map(d).join(", ")}</p>`:""}
      ${s.meanings_hi?.length?`<p class="muted small" lang="hi">${s.meanings_hi.map(d).join(", ")}</p>`:""}
      ${s.mnemonic?`<p class="srs-explanation">${d(s.mnemonic)}</p>`:""}
    `,h=`#/kanji/${encodeURIComponent(s.glyph)}`}t.innerHTML=`
    <div class="srs-card">
      <div class="srs-progress">
        <span>Review \xB7 Card <strong>${o.idx+1}</strong> of <strong>${e}</strong></span>
        <span class="srs-skill-badge ${u.cls}" title="${u.name}" lang="ja">${u.label}</span>
        ${a.isNew?'<span class="srs-tag new">NEW</span>':""}
      </div>
      <article class="srs-content">
        ${m}
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
  `,t.querySelectorAll("[data-grade]").forEach(s=>{s.addEventListener("click",()=>{const l=parseInt(s.dataset.grade,10),f=a.skill&&c.recordUnifiedSrsResponse,b=f?c.recordUnifiedSrsResponse(i,r,l):c.recordSrsResponse(r,l);o.grades.push({skill:i,pid:r,grade:l,snapshot:b}),j(t,l,{lastGraded:{skill:i,pid:r,grade:l,snapshot:b,isUnified:f}})})}),document.getElementById("srs-end")?.addEventListener("click",()=>{v="finished",S(t)})}function j(t,a,i={}){o.idx+=1,o.idx>=o.queue.length?(v="finished",S(t)):(I(t),i.lastGraded&&P(t,i.lastGraded))}let p=null;function P(t,a){const i=document.getElementById("undo-grade-toast");i&&i.remove(),p&&(clearTimeout(p),p=null);const e={1:"Again",3:"Hard",4:"Good",5:"Easy"}[a.grade]||`Grade ${a.grade}`,n=document.createElement("div");n.id="undo-grade-toast",n.className="undo-toast",n.setAttribute("role","status"),n.setAttribute("aria-live","polite"),n.innerHTML=`
    <span class="undo-toast-text">Recorded: <strong>${e}</strong></span>
    <button type="button" class="undo-toast-btn" id="undo-grade-btn">\u21B6 Undo</button>
  `,document.body.appendChild(n),document.getElementById("undo-grade-btn").addEventListener("click",()=>{if(a.isUnified&&c.undoUnifiedSrsResponse?c.undoUnifiedSrsResponse(a.skill,a.pid,a.snapshot):c.undoSrsResponse(a.pid,a.snapshot)){const m=o.grades.findIndex(h=>h.pid===a.pid&&h.grade===a.grade);m>=0&&o.grades.splice(m,1)}D()}),n.addEventListener("mouseenter",()=>{p&&(clearTimeout(p),p=null)}),n.addEventListener("mouseleave",()=>{p||(p=setTimeout(D,2e3))}),p=setTimeout(D,2e3)}function D(){p&&(clearTimeout(p),p=null);const t=document.getElementById("undo-grade-toast");t&&t.remove()}function S(t){const a={1:0,3:0,4:0,5:0};for(const e of o.grades)a[e.grade]=(a[e.grade]||0)+1;const i=o.grades.length,r=o.grades.map(({pid:e,grade:n})=>{const u=k.get(e),m=c.getSrsState(e);return{label:u?.pattern||e,grade:n,nextDue:m?.nextDue,interval:m?.interval}});t.innerHTML=`
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
            <span lang="ja"><strong>${d(e.label)}</strong></span>
            <span class="muted small">grade ${e.grade}, next in ${e.interval}d (${e.nextDue?new Date(e.nextDue).toLocaleDateString():"-"})</span>
          </li>
        `).join("")}
      </ul>

      <div class="test-nav">
        <button id="srs-restart" class="btn-primary">Start new session</button>
        <button id="srs-back">Back to Learn</button>
      </div>
    </div>
  `,document.getElementById("srs-restart")?.addEventListener("click",()=>{o=null,v="setup",M(t)}),document.getElementById("srs-back")?.addEventListener("click",()=>{location.hash="#/learn"})}function d(t){return String(t??"").replace(/[&<>"']/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[a])}export{G as renderReview};
