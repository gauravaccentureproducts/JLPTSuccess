import{renderJa as $}from"./furigana.js";import*as v from"./storage.js";let b=null,f=null,d=null,p="setup";async function I(){if(b)return b;const t=await fetch("data/questions.json");if(!t.ok)throw new Error(`Failed to load questions.json: ${t.status}`);return b=(await t.json()).questions||[],b}async function A(){if(f)return f;const e=await(await fetch("data/grammar.json")).json();return f=new Map((e.patterns||[]).map(r=>[r.id,r])),f}async function O(t){return p==="finished"&&(p="setup",d=null),p==="drilling"&&d?g(t):p==="finished"&&d?w(t):y(t)}async function y(t){p="setup",await Promise.all([I(),A()]);const e=v.getDuePatternIds(),r=Object.entries(v.getHistory()),s=r.filter(([,n])=>n.srsBox&&n.srsBox!=="graduated").length,a=r.filter(([,n])=>n.srsBox==="graduated").length;if(e.length===0){t.innerHTML=`
      <h2>Drill</h2>
      <div class="placeholder">
        <p><strong>No patterns due right now.</strong></p>
        <p>Patterns enter Drill the moment you miss them in a Test or Diagnostic. Once in Drill, they reappear at <strong>1d / 3d / 7d / 14d</strong> intervals - graduate after 4 consecutive correct answers.</p>
        <p class="muted">Queue: <strong>${s}</strong> pending \xB7 <strong>${a}</strong> graduated</p>
        <p style="margin-top:24px"><a href="#/test" class="btn-primary" style="text-decoration:none">Take a Test \u2192</a></p>
      </div>
    `;return}const i=_(e,b,10);if(i.length===0){t.innerHTML=`
      <h2>Drill</h2>
      <div class="placeholder">
        <p><strong>${e.length}</strong> pattern(s) due, but no questions exist for them yet.</p>
        <p class="muted">Add questions for these patterns to <code>data/questions.json</code>.</p>
      </div>
    `;return}t.innerHTML=`
    <h2>Drill</h2>
    <div class="drill-setup">
      <div class="drill-stats">
        <div class="stat-card weak"><div class="stat-num">${e.length}</div><div class="stat-label">Due today</div></div>
        <div class="stat-card neutral"><div class="stat-num">${s}</div><div class="stat-label">In queue</div></div>
        <div class="stat-card mastered"><div class="stat-num">${a}</div><div class="stat-label">Graduated</div></div>
      </div>
      <p>Drill session: <strong>${i.length}</strong> question(s) from due patterns. You'll get feedback after each question. Correct answers advance the SRS box (1d \u2192 3d \u2192 7d \u2192 14d \u2192 graduated). A wrong answer resets the pattern to the 1-day box.</p>
      <button id="start-drill" class="btn-primary">Start Drill</button>
    </div>
  `,document.getElementById("start-drill").addEventListener("click",()=>{d={questions:i,currentIdx:0,answers:{},startedAt:new Date().toISOString()},p="drilling",g(t)})}function _(t,e,r){const s=new Set(t),a=e.filter(o=>s.has(o.grammarPatternId));P(a);const i=new Set,n=[];for(const o of a)i.has(o.grammarPatternId)||(n.push(o),i.add(o.grammarPatternId));const c=a.filter(o=>!n.includes(o));return[...n,...c].slice(0,r)}function P(t){for(let e=t.length-1;e>0;e--){const r=Math.floor(Math.random()*(e+1));[t[e],t[r]]=[t[r],t[e]]}return t}function g(t){const e=d.questions.length,r=d.currentIdx,s=d.questions[r],a=d.answers[s.id],i=!!a,n=f.get(s.grammarPatternId),c=n?n.pattern:s.grammarPatternId;let o="";s.type==="mcq"||s.type==="dropdown"?o=E(s,a):s.type==="sentence_order"&&(o=D(s,a));const h=i?T(s,a):"",m=C(s,a),k=!i&&!m?`<p class="check-answer-hint">${s.type==="sentence_order"?"Tap the tiles in order to build the sentence, then click Check Answer.":s.type==="text_input"?"Type your answer in the box, then click Check Answer.":"Pick a choice, then click Check Answer."}</p>`:"",x=i?`<button id="next-drill" class="btn-primary">${r===e-1?"Finish Drill":"Next Question \u2192"}</button>`:`${k}<button id="check-answer" class="btn-primary" ${m?"":"disabled"} title="${m?"Check your answer":"Answer the question first"}">Check Answer</button>`;t.innerHTML=`
    <div class="drill-session">
      <div class="drill-header">
        <span>Drill \xB7 Question <strong>${r+1}</strong> of <strong>${e}</strong></span>
        <span class="pattern-tag">Pattern: ${u(c)}</span>
      </div>
      <div class="progress-bar"><div style="width:${(r+(i?1:.5))/e*100}%"></div></div>

      <article class="question-card">
        <p class="prompt">${u(s.prompt_ja||"")}</p>
        ${s.question_ja?`<p class="question">${$(s.question_ja)}</p>`:""}
        ${o}
        ${h}
      </article>

      <div class="test-nav">${x}</div>
    </div>
  `,i?document.getElementById("next-drill")?.addEventListener("click",()=>H(t)):(t.querySelectorAll("[data-choice]").forEach(l=>{l.addEventListener("click",()=>{d.answers[s.id]||(d.draftAnswer=l.dataset.choice,d.questions[r]._draft=l.dataset.choice,g(t))})}),t.querySelectorAll("[data-tile-add]").forEach(l=>{l.addEventListener("click",()=>j(s,l.dataset.tileAdd,t))}),t.querySelectorAll("[data-tile-remove]").forEach(l=>{l.addEventListener("click",()=>B(s,parseInt(l.dataset.tileRemove,10),t))}),document.getElementById("check-answer")?.addEventListener("click",()=>S(s,t)))}function E(t,e){const r=e?e.answer:t._draft;return`<div class="choice-grid">${(t.choices||[]).map(a=>{let i="choice-button";return e?(a===t.correctAnswer&&(i+=" correct-choice"),e.answer===a&&a!==t.correctAnswer&&(i+=" wrong-choice")):r===a&&(i+=" selected"),`<button type="button" data-choice="${u(a)}" class="${i}" ${e?"disabled":""}>${$(a)}</button>`}).join("")}</div>`}function D(t,e){const r=e?e.answer:t._draft||[],s=(t.tiles||[]).filter(n=>!r.includes(n)),a=r.length?r.map((n,c)=>{let o="tile ordered";return e&&(o=`tile ordered ${t.correctOrder?.[c]===n?"correct-tile":"wrong-tile"}`),`<button type="button" ${e?"disabled":`data-tile-remove="${c}"`} class="${o}">${$(n)}</button>`}).join(""):'<span class="tile-placeholder">Click tiles below to build the sentence</span>',i=s.map(n=>`<button type="button" ${e?"disabled":`data-tile-add="${u(n)}"`} class="tile">${$(n)}</button>`).join("");return`
    <div class="sentence-order">
      <div class="ordered-tray">${a}</div>
      <div class="tile-pool">${i}</div>
    </div>
  `}function C(t,e){return e?!0:t.type==="sentence_order"?Array.isArray(t._draft)&&t._draft.length===(t.tiles?.length||0):t._draft!==void 0&&t._draft!==null&&t._draft!==""}function j(t,e,r){t._draft||(t._draft=[]),!t._draft.includes(e)&&(t._draft.push(e),g(r))}function B(t,e,r){Array.isArray(t._draft)&&(t._draft.splice(e,1),g(r))}function L(t,e){if(t.type==="sentence_order"){if(!Array.isArray(e))return!1;const r=t.correctOrder||[];return e.length!==r.length?!1:e.every((s,a)=>s===r[a])}return e===t.correctAnswer}function S(t,e){const r=t._draft,s=L(t,r);d.answers[t.id]={answer:r,isCorrect:s,recorded:!1},v.recordDrillResponse(t.grammarPatternId,s),d.answers[t.id].recorded=!0,g(e)}function T(t,e){const r=e.isCorrect,s=f.get(t.grammarPatternId),a=!r&&t.distractor_explanations&&typeof e.answer=="string"?t.distractor_explanations[e.answer]:null,i=v.getPatternEntry(t.grammarPatternId),n=i?.srsBox||"?",c=i?.consecutiveCorrect??0;let o="";return r?n==="graduated"?o='<strong class="graduated">Graduated.</strong> Pattern mastered.':o=`Advanced to <strong>${n}</strong> box. ${c}/4 consecutive correct.`:o="Reset to the <strong>1d</strong> box. This pattern returns tomorrow.",`
    <div class="drill-feedback ${r?"correct":"incorrect"}">
      <div class="feedback-headline">${r?"Correct":"Wrong"}</div>
      ${t.explanation_en?`<p class="feedback-explanation">${u(t.explanation_en)}</p>`:""}
      ${a?`<p class="feedback-distractor"><em>Why your choice was off:</em> ${u(a)}</p>`:""}
      <p class="feedback-srs">${o}</p>
      ${s?`<p class="feedback-pattern">Pattern: <a href="#/learn/${encodeURIComponent(s.id)}">${u(s.pattern)}</a></p>`:""}
    </div>
  `}function H(t){if(d.currentIdx===d.questions.length-1){p="finished",w(t);return}d.currentIdx+=1,g(t)}function w(t){const e=d.questions.length,r=Object.values(d.answers).filter(n=>n.isCorrect).length,s=e-r,a=new Map;for(const n of d.questions){const c=d.answers[n.id];a.has(n.grammarPatternId)||a.set(n.grammarPatternId,{right:0,wrong:0});const o=a.get(n.grammarPatternId);c?.isCorrect?o.right++:o.wrong++}const i=[...a.entries()].map(([n,c])=>{const o=f.get(n),h=v.getPatternEntry(n),m=h?.srsBox==="graduated"?"\u2605 graduated":h?.srsBox||"-";return`
      <li>
        <span class="pat-name">${u(o?.pattern||n)}</span>
        <span class="pat-stats">${c.right} right \xB7 ${c.wrong} wrong</span>
        <span class="pat-box">${u(m)}</span>
      </li>
    `}).join("");t.innerHTML=`
    <div class="drill-finished">
      <h2>Drill complete</h2>
      <div class="score-summary">
        <div class="score-headline">
          <span class="score-big">${r}/${e}</span>
        </div>
        <div class="score-meta">
          <span class="score-correct">${r} correct</span>
          <span class="score-incorrect">${s} incorrect</span>
        </div>
      </div>

      <h3>Pattern updates</h3>
      <ul class="pattern-summary-list">${i}</ul>

      <div class="test-nav">
        <button id="drill-again" class="btn-primary">Drill again</button>
        <button id="drill-back">Back to Learn</button>
      </div>
    </div>
  `,document.getElementById("drill-again")?.addEventListener("click",()=>{d=null,p="setup",y(t)}),document.getElementById("drill-back")?.addEventListener("click",()=>{location.hash="#/learn"})}function u(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{O as renderDrill};
