import{renderJa as v}from"./furigana.js";import{matchesAnswer as H}from"./normalize.js";import*as $ from"./storage.js";let n=null,w="setup",A=null,M=null,x=null,b=null,f=null;const N=60,k=60;async function E(){if(M)return M;const t=await fetch("data/questions.json");if(!t.ok)throw new Error(`Failed to load questions.json: ${t.status}`);return M=(await t.json()).questions||[],M}async function G(){if(x)return x;const e=await(await fetch("data/grammar.json")).json();return x=new Map((e.patterns||[]).map(s=>[s.id,s])),x}async function nt(t,e){if(!e&&w==="results"&&(w="setup",n=null,A=null),w==="attempting"&&n)return I(t);if(w==="results"&&A)return R(t);if(e){const s=parseInt(decodeURIComponent(e),10);if([20,30,50].includes(s)){await E(),$.setSettings({lastTestLength:s}),C(s,t);return}}return L(t)}async function L(t){w="setup";const e=await E(),s=$.getSettings(),r=s.lastTestLength||20,c=($.getResults()||[]).length===0,i=!!s.examMode;let u="Mock-test papers";try{const a=await fetch("data/papers/manifest.json").then(o=>o.ok?o.json():null);a&&a.totalPapers&&a.totalQuestions&&(u=`${a.totalPapers} papers (${a.totalQuestions} questions)`)}catch{}t.innerHTML=`
    <h2>Chapter 2 - Test</h2>
    ${c?`
      <div class="empty-state-banner">
        <p><strong>Take your first mock test when you've covered at least lessons 1-10.</strong> If you're new, study a few patterns first - missed items will flow into Review and Daily Drill automatically.</p>
        <p><a href="#/learn">Continue learning \u2192</a></p>
      </div>
    `:""}
    <p>Configure and start a new auto-graded test. The Submit button stays disabled until every question has an answer.</p>
    <div class="test-setup">
      <label class="length-picker">
        <span>Test length</span>
        <select id="test-length">
          <option value="20" ${r===20?"selected":""}>20 questions</option>
          <option value="30" ${r===30?"selected":""}>30 questions</option>
          <option value="50" ${r===50?"selected":""}>50 questions</option>
        </select>
      </label>
      <label class="exam-mode-toggle" title="Adds a countdown timer at JLPT pace (~60 seconds per question). Auto-submits at zero.">
        <input type="checkbox" id="exam-mode" ${i?"checked":""}>
        <span>Exam mode (timer)</span>
      </label>
      <button id="start-test" class="btn-primary">Start Test</button>
      <p class="bank-note">Question bank: <strong>${e.length}</strong> available. Test length is capped at the bank size.</p>
      <p class="bank-note muted small">Pass mark: <strong>${k}%</strong> (JLPT N5 study target).</p>
    </div>
    <hr style="border:0; border-top:1px solid var(--c-border); margin:32px 0 24px;">
    <div class="test-papers-cta">
      <h3 style="margin:0 0 8px; font-weight:400;">Mock-test papers</h3>
      <p style="margin:0 0 12px; color:var(--c-muted);">Take a focused paper from a specific JLPT section (Moji / Goi / Bunpou / Dokkai). ${u} across 4 sections, drawn from the audited <code>KnowledgeBank</code> question files.</p>
      <a class="btn-secondary" href="#/papers" style="text-decoration:none; padding:10px 18px; display:inline-block; min-height:44px; line-height:24px;">Browse papers \u2192</a>
    </div>
    <hr style="border:0; border-top:1px solid var(--c-border); margin:32px 0 24px;">
    <div class="test-sitting-cta">
      <h3 style="margin:0 0 8px; font-weight:400;">Full mock-test sitting</h3>
      <p style="margin:0 0 12px; color:var(--c-muted);">Take the entire JLPT N5 in one sitting: Moji + Goi (25 min) \u2192 Bunpou + Dokkai (50 min) \u2192 Listening (30 min). Each section runs at the official time budget; auto-submits at zero. ~110 min total including breaks.</p>
      <a class="btn-secondary" href="#/sitting" style="text-decoration:none; padding:10px 18px; display:inline-block; min-height:44px; line-height:24px;">Start sitting \u2192</a>
    </div>
  `,document.getElementById("start-test").addEventListener("click",()=>{const a=parseInt(document.getElementById("test-length").value,10),o=!!document.getElementById("exam-mode")?.checked;$.setSettings({lastTestLength:a,examMode:o}),C(a,t,{examMode:o})})}function Q(t,e){const s=e>=8?Math.ceil(e/5):1/0,r=new Map;for(const a of t)r.has(a.grammarPatternId)||r.set(a.grammarPatternId,[]),r.get(a.grammarPatternId).push(a);for(const a of r.values())_(a);const c=[],i=[...r.values()];_(i);let u=0;for(;c.length<e&&i.some(a=>a.length>0);){const a=i[u%i.length];if(a.length>0&&a.filter(o=>c.includes(o)).length<s){const o=a.shift();o&&c.push(o)}if(u++,u>e*50)break}return c.slice(0,Math.min(e,t.length))}function _(t){for(let e=t.length-1;e>0;e--){const s=Math.floor(Math.random()*(e+1));[t[e],t[s]]=[t[s],t[e]]}return t}async function C(t,e,s={}){const r=await E(),c=Q(r,t),i=!!s.examMode;n={questions:c,answers:{},tileOrders:{},currentIdx:0,startedAt:new Date().toISOString(),examMode:i,durationSec:i?t*N:null},i?(f=Date.now()+n.durationSec*1e3,b&&clearInterval(b),b=setInterval(()=>J(e),1e3)):f=null,w="attempting",window.__testInProgress=!0,I(e)}function J(t){if(!f||w!=="attempting")return;const e=f-Date.now(),s=document.getElementById("test-timer");if(s){const r=Math.max(0,Math.ceil(e/1e3)),c=String(Math.floor(r/60)).padStart(2,"0"),i=String(r%60).padStart(2,"0");s.textContent=`${c}:${i}`,s.classList.toggle("danger",r<=60),s.classList.toggle("warning",r>60&&r<=300)}e<=0&&(clearInterval(b),b=null,f=null,D(t))}function I(t){const e=n.questions.length,s=n.questions[n.currentIdx],r=n.questions.filter(o=>!j(o)).length,c=r===0;let i="";s.type==="mcq"||s.type==="dropdown"?i=U(s):s.type==="sentence_order"?i=K(s):s.type==="text_input"?i=F(s):i=`<p class="placeholder-inline">Unsupported question type: ${m(s.type)}</p>`;let u="";if(n.examMode&&f){const o=Math.max(0,Math.ceil((f-Date.now())/1e3)),g=String(Math.floor(o/60)).padStart(2,"0"),y=String(o%60).padStart(2,"0");u=`<span id="test-timer" class="test-timer-chip${o<=60?" danger":o<=300?" warning":""}" aria-live="polite" title="Time remaining">${g}:${y}</span>`}t.innerHTML=`
    <div class="test-attempting">
      <div class="test-progress">
        <div class="progress-meta">
          <span>Question <strong>${n.currentIdx+1}</strong> of <strong>${e}</strong></span>
          ${u}
          <span class="answered-count">${e-r} / ${e} answered</span>
        </div>
        <div class="progress-bar"><div style="width:${(n.currentIdx+1)/e*100}%"></div></div>
      </div>

      <article class="question-card">
        <p class="prompt">${m(s.prompt_ja||"")}</p>
        ${s.question_ja?`<p class="question">${v(s.question_ja)}</p>`:""}
        ${i}
      </article>

      <div class="test-nav">
        <button id="prev-q" ${n.currentIdx===0?"disabled":""}>\u2190 Previous</button>
        <button id="next-q" ${n.currentIdx===e-1?"disabled":""}>Next \u2192</button>
        <button id="submit-test" class="btn-primary"
          ${c?"":"disabled"}
          title="${c?"Submit your test":`Answer all questions to submit (${r} remaining)`}">
          ${c?"Submit":`Submit (${r} remaining)`}
        </button>
      </div>
    </div>
  `,document.getElementById("prev-q")?.addEventListener("click",()=>B(n.currentIdx-1,t)),document.getElementById("next-q")?.addEventListener("click",()=>B(n.currentIdx+1,t)),document.getElementById("submit-test")?.addEventListener("click",()=>D(t)),t.querySelectorAll("[data-choice]").forEach(o=>{o.addEventListener("click",()=>{n.answers[s.id]=o.dataset.choice,I(t)})}),t.querySelectorAll("[data-tile-add]").forEach(o=>{o.addEventListener("click",()=>W(s,o.dataset.tileAdd,t))}),t.querySelectorAll("[data-tile-remove]").forEach(o=>{o.addEventListener("click",()=>Y(s,parseInt(o.dataset.tileRemove,10),t))});const a=t.querySelector("[data-text-input]");a&&(a.addEventListener("input",()=>{n.answers[s.id]=a.value;const o=n.questions.filter(T=>!j(T)).length,g=o===0,y=document.getElementById("submit-test");y&&(y.disabled=!g,y.textContent=g?"Submit":`Submit (${o} remaining)`,y.title=g?"Submit your test":`Answer all questions to submit (${o} remaining)`)}),typeof n.answers[s.id]=="string"&&(a.value=n.answers[s.id]))}function j(t){const e=n.answers[t.id];return t.type==="sentence_order"?Array.isArray(e)&&e.length===(t.tiles?.length||0):t.type==="text_input"?typeof e=="string"&&e.trim()!=="":e!=null&&e!==""}function B(t,e){t<0||t>=n.questions.length||(n.currentIdx=t,I(e))}function U(t){const e=n.answers[t.id];return`<div class="choice-grid">${(t.choices||[]).map(r=>`
    <button type="button" data-choice="${m(r)}" class="choice-button ${e===r?"selected":""}">
      ${v(r)}
    </button>
  `).join("")}</div>`}function F(t){const e=typeof n.answers[t.id]=="string"?n.answers[t.id]:"";return`
    <div class="text-input-wrap">
      <label for="text-input-${m(t.id)}" class="visually-hidden">Type your answer</label>
      <input
        id="text-input-${m(t.id)}"
        type="text"
        data-text-input
        class="text-input"
        autocomplete="off"
        autocapitalize="off"
        autocorrect="off"
        spellcheck="false"
        lang="ja"
        placeholder="Type kana or romaji..."
        value="${m(e)}">
      <p class="muted small">Accepts hiragana, katakana, or Hepburn romaji. Punctuation/whitespace ignored.</p>
    </div>
  `}function K(t){const e=n.answers[t.id]||[],s=(t.tiles||[]).filter(i=>!e.includes(i)),r=e.length?e.map((i,u)=>`
        <button type="button" data-tile-remove="${u}" class="tile ordered">${v(i)}</button>
      `).join(""):'<span class="tile-placeholder">Click tiles below to build the sentence</span>',c=s.map(i=>`
    <button type="button" data-tile-add="${m(i)}" class="tile">${v(i)}</button>
  `).join("");return`
    <div class="sentence-order">
      <div class="ordered-tray">${r}</div>
      <div class="tile-pool">${c}</div>
    </div>
  `}function W(t,e,s){n.answers[t.id]||(n.answers[t.id]=[]),!n.answers[t.id].includes(e)&&(n.answers[t.id].push(e),I(s))}function Y(t,e,s){Array.isArray(n.answers[t.id])&&(n.answers[t.id].splice(e,1),n.answers[t.id].length===0&&delete n.answers[t.id],I(s))}function X(t,e){if(t.type==="sentence_order"){if(!Array.isArray(e))return!1;const s=t.correctOrder||[];return e.length!==s.length?!1:e.every((r,c)=>r===s[c])}if(t.type==="text_input"){const s=t.acceptedAnswers||[t.correctAnswer];return H(e,s)}return e===t.correctAnswer}function D(t){b&&(clearInterval(b),b=null);const e=n.startedAt?Math.round((Date.now()-new Date(n.startedAt).getTime())/1e3):null,s=!!(n.examMode&&f&&Date.now()>=f);f=null;const r=n.questions.map(a=>{const o=n.answers[a.id];return{questionId:a.id,grammarPatternId:a.grammarPatternId,type:a.type,userAnswer:o,correctAnswer:a.correctAnswer??a.correctOrder,isCorrect:X(a,o)}}),c=r.filter(a=>a.isCorrect).length,i=r.length,u={timestamp:new Date().toISOString(),type:"test",total:i,correct:c,incorrect:i-c,percent:i>0?Math.round(c/i*100):0,examMode:n.examMode||!1,elapsedSec:e,timedOut:s,responses:r};$.recordTestResponses(r),$.recordTestResult(u),A={result:u,questions:n.questions},w="results",window.__testInProgress=!1,R(t)}async function R(t){const{result:e,questions:s}=A;await G();const r=e.responses.map(d=>{const l=s.find(p=>p.id===d.questionId);return V(l,d)}).join(""),i=Z(e.responses).map(d=>{const l=x.get(d),p=l?l.pattern:d;return`<li><a href="#/review">${m(p)}</a></li>`}).join(""),u=e.percent>=k,a=`
    <div class="pass-badge ${u?"pass":"fail"}" role="status">
      ${u?`<strong>Pass</strong> \xB7 \u2265 ${k}% study target`:`<strong>Below pass</strong> \xB7 target ${k}% (you got ${e.percent}%)`}
    </div>
  `;let o="";if(typeof e.elapsedSec=="number"){const d=Math.floor(e.elapsedSec/60),l=String(e.elapsedSec%60).padStart(2,"0"),p=e.timedOut?" (auto-submitted at zero)":"";o=`<span class="score-time muted small">Time: ${d}m ${l}s${p}</span>`}const g=new Map;for(const d of e.responses){const l=x.get(d.grammarPatternId),p=l&&l.category||"Other";g.has(p)||g.set(p,{correct:0,total:0});const h=g.get(p);h.total+=1,d.isCorrect&&(h.correct+=1)}const y=[...g.entries()].sort((d,l)=>d[1].correct/d[1].total-l[1].correct/l[1].total).map(([d,{correct:l,total:p}])=>{const h=p>0?Math.round(l/p*100):0;return`
        <tr class="${h>=k?"pass":"fail"}">
          <td class="cat-name">${m(d)}</td>
          <td class="cat-score">${l} / ${p}</td>
          <td class="cat-pct">${h}%</td>
          <td class="cat-bar"><div class="cat-bar-track"><div class="cat-bar-fill" style="width:${h}%"></div></div></td>
        </tr>
      `}).join(""),T={mcq:"Multiple choice",sentence_order:"Sentence ordering",text_input:"Text input",dropdown:"Dropdown"},S=new Map;for(const d of e.responses){const l=d.type||"mcq";S.has(l)||S.set(l,{correct:0,total:0});const p=S.get(l);p.total+=1,d.isCorrect&&(p.correct+=1)}const O=[...S.entries()].sort((d,l)=>d[1].correct/d[1].total-l[1].correct/l[1].total).map(([d,{correct:l,total:p}])=>{const h=p>0?Math.round(l/p*100):0,P=h>=k?"pass":"fail",z=T[d]||d;return`
        <tr class="${P}">
          <td class="cat-name">${m(z)}</td>
          <td class="cat-score">${l} / ${p}</td>
          <td class="cat-pct">${h}%</td>
          <td class="cat-bar"><div class="cat-bar-track"><div class="cat-bar-fill" style="width:${h}%"></div></div></td>
        </tr>
      `}).join("");t.innerHTML=`
    <div class="test-results">
      <h2>Results</h2>

      <section class="score-summary">
        <div class="score-headline">
          <span class="score-big">${e.correct}/${e.total}</span>
          <span class="score-pct">${e.percent}%</span>
        </div>
        <div class="score-meta">
          <span class="score-correct">${e.correct} correct</span>
          <span class="score-incorrect">${e.incorrect} incorrect</span>
          ${o}
        </div>
        ${a}
      </section>

      <section class="category-breakdown">
        <h3>By grammar category</h3>
        ${g.size>0?`
          <table class="category-table">
            <thead>
              <tr><th>Category</th><th>Score</th><th>%</th><th>Distribution</th></tr>
            </thead>
            <tbody>${y}</tbody>
          </table>
          <p class="muted small">Categories sorted by accuracy (weakest first). Pass target ${k}%.</p>
        `:'<p class="muted">No category metadata available for this test.</p>'}
      </section>

      <section class="category-breakdown">
        <h3>By question type</h3>
        ${S.size>1?`
          <table class="category-table">
            <thead>
              <tr><th>Type</th><th>Score</th><th>%</th><th>Distribution</th></tr>
            </thead>
            <tbody>${O}</tbody>
          </table>
          <p class="muted small">Types sorted by accuracy (weakest first). Useful for picking your next drill mode.</p>
        `:'<p class="muted small">All questions in this test were the same type \u2014 type breakdown is only meaningful when the test mixes question formats.</p>'}
      </section>

      <section class="answer-review">
        <h3>Answer Review</h3>
        <ol class="review-list">${r}</ol>
      </section>

      <section class="gap-list">
        <h3>Grammar Gap List</h3>
        ${i?`<p>Patterns flagged as weak by your rolling history (\u2265 50% error AND \u2265 2 attempts):</p><ul>${i}</ul>`:"<p>No weak patterns yet. Keep practicing - patterns are flagged after 2+ attempts with \u2265 50% error.</p>"}
      </section>

      <div class="test-nav">
        <button id="new-test" class="btn-primary">New Test</button>
        <button id="back-to-learn">Back to Learn</button>
      </div>
    </div>
  `,document.getElementById("new-test")?.addEventListener("click",()=>{n=null,A=null,w="setup",L(t)}),document.getElementById("back-to-learn")?.addEventListener("click",()=>{location.hash="#/learn"})}function V(t,e){const s=e.isCorrect?"\u2713":"\u2717",r=e.isCorrect?"correct":"incorrect",c=q(t,e.userAnswer),i=q(t,e.correctAnswer),u=!e.isCorrect&&t.distractor_explanations&&typeof e.userAnswer=="string"?t.distractor_explanations[e.userAnswer]:null,a=x?.get(t.grammarPatternId),o=a?a.pattern:t.grammarPatternId;return`
    <li class="review-item ${r}">
      <div class="review-marker" aria-label="${e.isCorrect?"correct":"incorrect"}">${s}</div>
      <div class="review-body">
        <div class="review-question">
          ${t.question_ja?v(t.question_ja):m(t.prompt_ja||"")}
        </div>
        <div class="review-answers">
          <span class="answer-label">Your answer:</span>
          <span class="user-answer ${r}">${c}</span>
          ${e.isCorrect?"":`<span class="answer-label">Correct:</span><span class="correct-answer">${i}</span>`}
        </div>
        ${t.explanation_en?`<p class="review-explanation">${m(t.explanation_en)}</p>`:""}
        ${u?`<p class="distractor-explanation"><em>Why your choice was wrong:</em> ${m(u)}</p>`:""}
        <p class="review-pattern">Pattern: <a href="#/learn/${encodeURIComponent(t.grammarPatternId)}">${m(o)}</a></p>
      </div>
    </li>
  `}function q(t,e){return t.type==="sentence_order"&&Array.isArray(e)?v(e.join(" ")):v(String(e??"-"))}function Z(t){return[...new Set($.getWeakPatternIds())]}function m(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{nt as renderTest};
