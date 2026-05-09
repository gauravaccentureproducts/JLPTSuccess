import{renderJa as b}from"./furigana.js";import*as y from"./storage.js";import{t as w}from"./i18n.js";let $=null,g=null,c=null,f="setup";async function C(){if($)return $;const t=await fetch("data/questions.json");if(!t.ok)throw new Error(`Failed to load questions.json: ${t.status}`);return $=(await t.json()).questions||[],$}async function P(){if(g)return g;const e=await(await fetch("data/grammar.json")).json();return g=new Map((e.patterns||[]).map(n=>[n.id,n])),g}async function Q(t){return f==="finished"&&(f="setup",c=null),f==="drilling"&&c?h(t):f==="finished"&&c?I(t):_(t)}async function _(t){f="setup",await Promise.all([C(),P()]);const e=y.getDuePatternIds(),n=Object.entries(y.getHistory()),r=n.filter(([,s])=>s.srsBox&&s.srsBox!=="graduated").length,a=n.filter(([,s])=>s.srsBox==="graduated").length;if(e.length===0){t.innerHTML=`
      <h2>${w("page.drill")}</h2>
      <div class="placeholder">
        <p><strong>No patterns due right now.</strong></p>
        <p>Patterns enter Drill the moment you miss them in a Test or Diagnostic. Once in Drill, they reappear at <strong>1d / 3d / 7d / 14d</strong> intervals - graduate after 4 consecutive correct answers.</p>
        <p class="muted">Queue: <strong>${r}</strong> pending \xB7 <strong>${a}</strong> graduated</p>
        <p style="margin-top:24px"><a href="#/test" class="btn-primary" style="text-decoration:none">Take a Test \u2192</a></p>
      </div>
    `;return}const i=j(e,$,10);if(i.length===0){t.innerHTML=`
      <h2>${w("page.drill")}</h2>
      <div class="placeholder">
        <p><strong>${e.length}</strong> pattern(s) due, but no questions exist for them yet.</p>
        <p class="muted">Add questions for these patterns to <code>data/questions.json</code>.</p>
      </div>
    `;return}t.innerHTML=`
    <h2>${w("page.drill")}</h2>
    <div class="drill-setup">
      <div class="drill-stats">
        <div class="stat-card weak"><div class="stat-num">${e.length}</div><div class="stat-label">Due today</div></div>
        <div class="stat-card neutral"><div class="stat-num">${r}</div><div class="stat-label">In queue</div></div>
        <div class="stat-card mastered"><div class="stat-num">${a}</div><div class="stat-label">Graduated</div></div>
      </div>
      <p>Drill session: <strong>${i.length}</strong> question(s) from due patterns. You'll get feedback after each question. Correct answers advance the SRS box (1d \u2192 3d \u2192 7d \u2192 14d \u2192 graduated). A wrong answer resets the pattern to the 1-day box.</p>
      <button id="start-drill" class="btn-primary">Start Drill</button>
    </div>
  `,document.getElementById("start-drill").addEventListener("click",()=>{c={questions:i,currentIdx:0,answers:{},startedAt:new Date().toISOString()},f="drilling",h(t)})}function j(t,e,n){const r=new Set(t),a=e.filter(o=>r.has(o.grammarPatternId));L(a);const i=new Set,s=[];for(const o of a)i.has(o.grammarPatternId)||(s.push(o),i.add(o.grammarPatternId));const d=a.filter(o=>!s.includes(o));return[...s,...d].slice(0,n)}function L(t){for(let e=t.length-1;e>0;e--){const n=Math.floor(Math.random()*(e+1));[t[e],t[n]]=[t[n],t[e]]}return t}function h(t){const e=c.questions.length,n=c.currentIdx,r=c.questions[n],a=c.answers[r.id],i=!!a,s=g.get(r.grammarPatternId),d=s?s.pattern:r.grammarPatternId;let o="";r.type==="mcq"||r.type==="dropdown"?o=B(r,a):r.type==="sentence_order"?o=D(r,a):(r.type==="text_input"||r.type==="cloze"||r.type==="production")&&(o=S(r,a));const p=i?M(r,a):"",m=k(r,a),x=!i&&!m?`<p class="check-answer-hint">${r.type==="sentence_order"?"Tap the tiles in order to build the sentence, then click Check Answer.":r.type==="text_input"?"Type your answer in the box, then click Check Answer.":"Pick a choice, then click Check Answer."}</p>`:"",E=i?`<button id="next-drill" class="btn-primary">${n===e-1?"Finish Drill":"Next Question \u2192"}</button>`:`${x}<button id="check-answer" class="btn-primary" ${m?"":"disabled"} title="${m?"Check your answer":"Answer the question first"}">Check Answer</button>`;if(t.innerHTML=`
    <div class="drill-session">
      <div class="drill-header">
        <span>Drill \xB7 Question <strong>${n+1}</strong> of <strong>${e}</strong></span>
        <span class="pattern-tag">Pattern: ${u(d)}</span>
      </div>
      <div class="progress-bar"><div style="width:${(n+(i?1:.5))/e*100}%"></div></div>

      <article class="question-card">
        <p class="prompt">${u(r.prompt_ja||"")}</p>
        ${r.question_ja?`<p class="question">${b(r.question_ja)}</p>`:""}
        ${o}
        ${p}
      </article>

      <div class="test-nav">${E}</div>
    </div>
  `,i)document.getElementById("next-drill")?.addEventListener("click",()=>O(t));else{t.querySelectorAll("[data-choice]").forEach(l=>{l.addEventListener("click",()=>{c.answers[r.id]||(c.draftAnswer=l.dataset.choice,c.questions[n]._draft=l.dataset.choice,h(t))})}),t.querySelectorAll("[data-tile-add]").forEach(l=>{l.addEventListener("click",()=>T(r,l.dataset.tileAdd,t))}),t.querySelectorAll("[data-tile-remove]").forEach(l=>{l.addEventListener("click",()=>H(r,parseInt(l.dataset.tileRemove,10),t))});const v=t.querySelector("[data-drill-text-input]");v&&(v.addEventListener("input",()=>{r._draft=v.value;const l=document.getElementById("check-answer");l&&(l.disabled=!k(r,null))}),v.addEventListener("keydown",l=>{l.key==="Enter"&&k(r,null)&&(l.preventDefault(),A(r,t))}),c.answers[r.id]||Promise.resolve().then(()=>v.focus())),document.getElementById("check-answer")?.addEventListener("click",()=>A(r,t))}}function B(t,e){const n=e?e.answer:t._draft;return`<div class="choice-grid">${(t.choices||[]).map(a=>{let i="choice-button";return e?(a===t.correctAnswer&&(i+=" correct-choice"),e.answer===a&&a!==t.correctAnswer&&(i+=" wrong-choice")):n===a&&(i+=" selected"),`<button type="button" data-choice="${u(a)}" class="${i}" ${e?"disabled":""}>${b(a)}</button>`}).join("")}</div>`}function D(t,e){const n=e?e.answer:t._draft||[],r=(t.tiles||[]).filter(s=>!n.includes(s)),a=n.length?n.map((s,d)=>{let o="tile ordered";return e&&(o=`tile ordered ${t.correctOrder?.[d]===s?"correct-tile":"wrong-tile"}`),`<button type="button" ${e?"disabled":`data-tile-remove="${d}"`} class="${o}">${b(s)}</button>`}).join(""):'<span class="tile-placeholder">Click tiles below to build the sentence</span>',i=r.map(s=>`<button type="button" ${e?"disabled":`data-tile-add="${u(s)}"`} class="tile">${b(s)}</button>`).join("");return`
    <div class="sentence-order">
      <div class="ordered-tray">${a}</div>
      <div class="tile-pool">${i}</div>
    </div>
  `}function k(t,e){return e?!0:t.type==="sentence_order"?Array.isArray(t._draft)&&t._draft.length===(t.tiles?.length||0):t.type==="text_input"||t.type==="cloze"||t.type==="production"?typeof t._draft=="string"&&t._draft.trim().length>0:t._draft!==void 0&&t._draft!==null&&t._draft!==""}function S(t,e){const n=e?e.answer:t._draft||"",r=!!e,a=u(n),i=t.question_ja||"",s=/[\(（][\s　]*[\)）]/,d=s.test(i);let o="drill-text-input";r&&(o+=e.isCorrect?" drill-text-input-correct":" drill-text-input-wrong");const p=`
    <input type="text" data-drill-text-input
           class="${o}"
           ${r?"disabled":""}
           autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"
           value="${a}"
           placeholder="${t.type==="production"?"Type the Japanese sentence":"Type your answer"}"
           lang="ja">
  `;return d&&t.type!=="production"?`
      <div class="drill-text-input-block">
        <p class="drill-cloze-sentence" lang="ja">${i.split(s).map(u).join(`<span class="drill-cloze-blank">${p}</span>`)}</p>
      </div>
    `:`
    <div class="drill-text-input-block">
      ${p}
    </div>
  `}function T(t,e,n){t._draft||(t._draft=[]),!t._draft.includes(e)&&(t._draft.push(e),h(n))}function H(t,e,n){Array.isArray(t._draft)&&(t._draft.splice(e,1),h(n))}function z(t,e){if(t.type==="sentence_order"){if(!Array.isArray(e))return!1;const n=t.correctOrder||[];return e.length!==n.length?!1:e.every((r,a)=>r===n[a])}if(t.type==="text_input"||t.type==="cloze"||t.type==="production"){if(typeof e!="string")return!1;const n=i=>String(i||"").normalize("NFKC").replace(/[\s　]+/g,"").replace(/[。．.!?！？]+$/g,"").toLowerCase().trim(),r=n(e);return r?n(t.correctAnswer)===r?!0:(Array.isArray(t.acceptedAnswers)?t.acceptedAnswers:[]).some(i=>n(i)===r):!1}return e===t.correctAnswer}function A(t,e){const n=t._draft,r=z(t,n);c.answers[t.id]={answer:n,isCorrect:r,recorded:!1},y.recordDrillResponse(t.grammarPatternId,r),c.answers[t.id].recorded=!0,h(e)}function M(t,e){const n=e.isCorrect,r=g.get(t.grammarPatternId),a=!n&&t.distractor_explanations&&typeof e.answer=="string"?t.distractor_explanations[e.answer]:null,i=y.getPatternEntry(t.grammarPatternId),s=i?.srsBox||"?",d=i?.consecutiveCorrect??0;let o="";return n?s==="graduated"?o='<strong class="graduated">Graduated.</strong> Pattern mastered.':o=`Advanced to <strong>${s}</strong> box. ${d}/4 consecutive correct.`:o="Reset to the <strong>1d</strong> box. This pattern returns tomorrow.",`
    <div class="drill-feedback ${n?"correct":"incorrect"}">
      <div class="feedback-headline">${n?"Correct":"Wrong"}</div>
      ${t.explanation_en?`<p class="feedback-explanation">${u(t.explanation_en)}</p>`:""}
      ${a?`<p class="feedback-distractor"><em>Why your choice was off:</em> ${u(a)}</p>`:""}
      <p class="feedback-srs">${o}</p>
      ${r?`<p class="feedback-pattern">Pattern: <a href="#/learn/${encodeURIComponent(r.id)}">${u(r.pattern)}</a></p>`:""}
    </div>
  `}function O(t){if(c.currentIdx===c.questions.length-1){f="finished",I(t);return}c.currentIdx+=1,h(t)}function I(t){const e=c.questions.length,n=Object.values(c.answers).filter(s=>s.isCorrect).length,r=e-n,a=new Map;for(const s of c.questions){const d=c.answers[s.id];a.has(s.grammarPatternId)||a.set(s.grammarPatternId,{right:0,wrong:0});const o=a.get(s.grammarPatternId);d?.isCorrect?o.right++:o.wrong++}const i=[...a.entries()].map(([s,d])=>{const o=g.get(s),p=y.getPatternEntry(s),m=p?.srsBox==="graduated"?"\u2605 graduated":p?.srsBox||"-";return`
      <li>
        <span class="pat-name">${u(o?.pattern||s)}</span>
        <span class="pat-stats">${d.right} right \xB7 ${d.wrong} wrong</span>
        <span class="pat-box">${u(m)}</span>
      </li>
    `}).join("");t.innerHTML=`
    <div class="drill-finished">
      <h2>Drill complete</h2>
      <div class="score-summary">
        <div class="score-headline">
          <span class="score-big">${n}/${e}</span>
        </div>
        <div class="score-meta">
          <span class="score-correct">${n} correct</span>
          <span class="score-incorrect">${r} incorrect</span>
        </div>
      </div>

      <h3>Pattern updates</h3>
      <ul class="pattern-summary-list">${i}</ul>

      <div class="test-nav">
        <button id="drill-again" class="btn-primary">Drill again</button>
        <button id="drill-back">Back to Learn</button>
      </div>
    </div>
  `,document.getElementById("drill-again")?.addEventListener("click",()=>{c=null,f="setup",_(t)}),document.getElementById("drill-back")?.addEventListener("click",()=>{location.hash="#/learn"})}function u(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{Q as renderDrill};
