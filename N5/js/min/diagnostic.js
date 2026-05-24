import{renderJa as h}from"./furigana.js";import*as v from"./storage.js";import{t as y}from"./i18n.js";import{navigateTo as w}from"./router.js";let p=null,d=null,n=null,g="setup";const b=10;async function S(){return p||(p=(await(await fetch("data/questions.json")).json()).questions||[],p)}async function x(){if(d)return d;const e=await(await fetch("data/grammar.json")).json();return d=new Map((e.patterns||[]).map(s=>[s.id,s])),d}async function N(t){return await Promise.all([S(),x()]),g==="attempting"&&n?l(t):g==="results"&&n?I(t):A(t)}function A(t){g="setup";const e=v.getSettings(),s=e.diagnosticCompleted;t.innerHTML=`
    <h2>${y("page.diagnostic")}</h2>
    <div class="diagnostic-setup">
      <p><strong>${b} questions</strong> sampled across the highest-frequency N5 categories. The diagnostic gives you a quick map of which patterns to practice - without affecting your test score history.</p>
      <ul>
        <li>Results don't count toward "Tests taken".</li>
        <li>Missed patterns enter the Drill queue immediately.</li>
        <li>Skippable any time - you can re-take it later from the Summary tab.</li>
      </ul>
      ${s?`<p class="muted">You already took the diagnostic on ${B(e.lastDiagnosticDate)}. Re-taking it will replace any current SRS state for sampled patterns.</p>`:""}
      <div class="diagnostic-actions">
        <button id="start-diagnostic" class="btn-primary">${s?"Re-take Diagnostic":"Start Diagnostic"}</button>
        <button id="skip-diagnostic">Skip for now</button>
      </div>
    </div>
  `,document.getElementById("start-diagnostic").addEventListener("click",()=>D(t)),document.getElementById("skip-diagnostic").addEventListener("click",()=>{v.setSettings({diagnosticCompleted:!0}),w("learn")})}function D(t){const e=E(p,b);if(e.length===0){t.innerHTML=`
      <h2>${y("page.diagnostic")}</h2>
      <div class="placeholder"><p>No questions available. Add to <code>data/questions.json</code> first.</p></div>
    `;return}n={questions:e,answers:{},currentIdx:0,startedAt:new Date().toISOString()},g="attempting",l(t)}function E(t,e){const s=new Map;for(const r of t){const o=d.get(r.grammarPatternId)?.category||"?";s.has(o)||s.set(o,[]),s.get(o).push(r)}for(const r of s.values())$(r);const i=[...s.entries()];$(i);const c=[];let a=0;for(;c.length<e&&i.some(([,r])=>r.length>0);){const[,r]=i[a%i.length];if(r.length>0&&c.push(r.shift()),a++,a>e*50)break}return c}function $(t){for(let e=t.length-1;e>0;e--){const s=Math.floor(Math.random()*(e+1));[t[e],t[s]]=[t[s],t[e]]}return t}function l(t){const e=n.questions.length,s=n.questions[n.currentIdx],i=n.questions.filter(r=>!L(r)).length,c=i===0;let a="";s.type==="mcq"||s.type==="dropdown"?a=T(s):s.type==="sentence_order"&&(a=q(s)),t.innerHTML=`
    <div class="test-attempting">
      <div class="diagnostic-banner">Diagnostic - results seed your weak list but don't count toward score history</div>
      <div class="test-progress">
        <div class="progress-meta">
          <span>Question <strong>${n.currentIdx+1}</strong> of <strong>${e}</strong></span>
          <span class="answered-count">${e-i} / ${e} answered</span>
        </div>
        <div class="progress-bar"><div style="width:${(n.currentIdx+1)/e*100}%"></div></div>
      </div>

      <article class="question-card">
        <p class="prompt">${m(s.prompt_ja||"")}</p>
        ${s.question_ja?`<p class="question">${h(s.question_ja)}</p>`:""}
        ${a}
      </article>

      <div class="test-nav">
        <button id="prev-q" ${n.currentIdx===0?"disabled":""}>\u2190 Previous</button>
        <button id="next-q" ${n.currentIdx===e-1?"disabled":""}>Next \u2192</button>
        <button id="finish-diagnostic" class="btn-primary"
          ${c?"":"disabled"}
          title="${c?"Finish diagnostic":`${i} unanswered`}">
          ${c?"Finish Diagnostic":`Finish (${i} remaining)`}
        </button>
      </div>
    </div>
  `,document.getElementById("prev-q")?.addEventListener("click",()=>k(n.currentIdx-1,t)),document.getElementById("next-q")?.addEventListener("click",()=>k(n.currentIdx+1,t)),document.getElementById("finish-diagnostic")?.addEventListener("click",()=>R(t)),t.querySelectorAll("[data-choice]").forEach(r=>{r.addEventListener("click",()=>{n.answers[s.id]=r.dataset.choice,l(t)})}),t.querySelectorAll("[data-tile-add]").forEach(r=>{r.addEventListener("click",()=>j(s,r.dataset.tileAdd,t))}),t.querySelectorAll("[data-tile-remove]").forEach(r=>{r.addEventListener("click",()=>C(s,parseInt(r.dataset.tileRemove,10),t))})}function T(t){const e=n.answers[t.id];return`<div class="choice-grid">${(t.choices||[]).map(s=>`<button type="button" data-choice="${m(s)}" class="choice-button ${e===s?"selected":""}">${h(s)}</button>`).join("")}</div>`}function q(t){const e=n.answers[t.id]||[],s=(t.tiles||[]).filter(a=>!e.includes(a)),i=e.length?e.map((a,r)=>`<button type="button" data-tile-remove="${r}" class="tile ordered">${h(a)}</button>`).join(""):'<span class="tile-placeholder">Click tiles below to build the sentence</span>',c=s.map(a=>`<button type="button" data-tile-add="${m(a)}" class="tile">${h(a)}</button>`).join("");return`<div class="sentence-order"><div class="ordered-tray">${i}</div><div class="tile-pool">${c}</div></div>`}function L(t){const e=n.answers[t.id];return t.type==="sentence_order"?Array.isArray(e)&&e.length===(t.tiles?.length||0):e!=null&&e!==""}function k(t,e){t<0||t>=n.questions.length||(n.currentIdx=t,l(e))}function j(t,e,s){n.answers[t.id]||(n.answers[t.id]=[]),!n.answers[t.id].includes(e)&&(n.answers[t.id].push(e),l(s))}function C(t,e,s){Array.isArray(n.answers[t.id])&&(n.answers[t.id].splice(e,1),n.answers[t.id].length===0&&delete n.answers[t.id],l(s))}function M(t,e){if(t.type==="sentence_order"){if(!Array.isArray(e))return!1;const s=t.correctOrder||[];return e.length===s.length&&e.every((i,c)=>i===s[c])}return e===t.correctAnswer}function R(t){const e=n.questions.map(s=>{const i=n.answers[s.id];return{questionId:s.id,grammarPatternId:s.grammarPatternId,type:s.type,userAnswer:i,correctAnswer:s.correctAnswer??s.correctOrder,isCorrect:M(s,i)}});v.recordTestResponses(e),v.setSettings({diagnosticCompleted:!0,lastDiagnosticDate:new Date().toISOString()}),n.responses=e,g="results",I(t)}function I(t){const e=n.responses,s=e.length,i=e.filter(o=>o.isCorrect).length,c=s-i,a=[...new Set(e.filter(o=>!o.isCorrect).map(o=>o.grammarPatternId))],r=a.map(o=>{const u=d.get(o);return`<li><a href="#/learn/${encodeURIComponent(o)}">${m(u?.pattern||o)}</a> - ${m(u?.meaning_en||"")}</li>`}).join(""),f=new Set;for(const o of n.questions){const u=d.get(o.grammarPatternId);u?.category&&f.add(u.category)}t.innerHTML=`
    <h2>Diagnostic - Results</h2>
    <div class="diagnostic-banner">These results don't count toward "Tests taken". Missed patterns are queued in Drill.</div>

    <section class="score-summary">
      <div class="score-headline"><span class="score-big">${i}/${s}</span></div>
      <div class="score-meta">
        <span class="score-correct">${i} correct</span>
        <span class="score-incorrect">${c} incorrect</span>
      </div>
      <p class="muted">Sampled ${f.size} categor${f.size===1?"y":"ies"} across the N5 catalog.</p>
    </section>

    ${a.length>0?`
      <section class="gap-list">
        <h3>Patterns to review (${a.length})</h3>
        <p>These patterns missed at least once. They've entered your Drill queue at the 1-day box.</p>
        <ul>${r}</ul>
        <div class="test-nav" style="justify-content:flex-start; margin-top:12px">
          <a href="#/drill" class="btn-primary" style="text-decoration:none; padding:10px 20px">Drill them now</a>
          <a href="#/review" style="padding:10px 16px">Review the lessons</a>
        </div>
      </section>
    `:`
      <section class="gap-list"><p>No misses - strong baseline. Take the full Test in Chapter 2 to dig deeper.</p></section>
    `}

    <div class="test-nav">
      <button id="diag-back" class="btn-primary">Back to Learn</button>
    </div>
  `,document.getElementById("diag-back")?.addEventListener("click",()=>{w("learn")})}function B(t){if(!t)return"";try{return new Date(t).toLocaleDateString()}catch{return t}}function m(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{N as renderDiagnostic};
