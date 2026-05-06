import{t as A}from"./i18n.js";import{renderJa as b}from"./furigana.js";import{matchesAnswer as z}from"./normalize.js";import*as $ from"./storage.js";let a=null,y="setup",T=null,_=null,x=null,v=null,f=null;const H=60,k=60;async function E(){if(_)return _;const t=await fetch("data/questions.json");if(!t.ok)throw new Error(`Failed to load questions.json: ${t.status}`);return _=(await t.json()).questions||[],_}async function J(){if(x)return x;const e=await(await fetch("data/grammar.json")).json();return x=new Map((e.patterns||[]).map(s=>[s.id,s])),x}async function rt(t,e){if(!e&&y==="results"&&(y="setup",a=null,T=null),y==="attempting"&&a)return I(t);if(y==="results"&&T)return q(t);if(e){const s=parseInt(decodeURIComponent(e),10);if([20,30,50].includes(s)){await E(),$.setSettings({lastTestLength:s}),j(s,t);return}}return L(t)}async function L(t){y="setup";const e=await E(),s=$.getSettings(),r=s.lastTestLength||20,c=($.getResults()||[]).length===0,i=!!s.examMode;let u="Mock-test papers",o=null;try{const n=await fetch("data/papers/manifest.json").then(m=>m.ok?m.json():null);n&&n.totalPapers&&n.totalQuestions&&(u=`${n.totalPapers} papers (${n.totalQuestions} questions)`),n&&Array.isArray(n.full_mock_papers)&&n.full_mock_papers.length&&(o=n.full_mock_papers)}catch{}t.innerHTML=`
    <h2>${A("page.test")}</h2>
    ${c?`
      <div class="empty-state-banner">
        <p><strong>Take your first mock test when you've covered at least lessons 1-10.</strong> If you're new, study a few patterns first - missed items will flow into Review and Daily Drill automatically.</p>
        <p><a href="#/learn">Continue learning \u2192</a></p>
      </div>
    `:""}
    <!-- Promotional trust callout (round-9 follow-up 2026-05-07): the
         "your scores stay on this device" message is the strongest
         niche-N2 reassurance precisely at the moment a learner is
         about to submit results. Bunpro / Renshuu push results to
         their server; the callout makes the privacy claim concrete
         right where it matters most. -->
    <aside class="trust-callout" aria-label="Privacy reassurance">
      <strong>${A("trust.no_login")} \xB7 ${A("trust.no_tracking")} \xB7 ${A("trust.on_device")}</strong>
      <p>${A("trust.test_callout")}</p>
    </aside>
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
      <h3 style="margin:0 0 8px; font-weight:400;">Full Mock Test (real JLPT N5 shape)</h3>
      <p style="margin:0 0 12px; color:var(--c-muted);">Take the entire JLPT N5 in one sitting: <strong>\u8A00\u8A9E\u77E5\u8B58\uFF08\u6587\u5B57\u30FB\u8A9E\u5F59\uFF09 30Q / 25 min</strong> \u2192 <strong>\u8A00\u8A9E\u77E5\u8B58\uFF08\u6587\u6CD5\uFF09\u30FB\u8AAD\u89E3 31Q / 50 min</strong> \u2192 <strong>\u8074\u89E3 24Q / 30 min</strong>. Total <strong>85Q / 105 min</strong> (close to the official 91Q / 105min). Each section runs at the official time budget and auto-submits at zero.${o?` ${o.length} papers available.`:""}</p>
      <a class="btn-secondary" href="#/sitting" style="text-decoration:none; padding:10px 18px; display:inline-block; min-height:44px; line-height:24px;">Start full mock test \u2192</a>
    </div>
  `,document.getElementById("start-test").addEventListener("click",()=>{const n=parseInt(document.getElementById("test-length").value,10),m=!!document.getElementById("exam-mode")?.checked;$.setSettings({lastTestLength:n,examMode:m}),j(n,t,{examMode:m})})}function G(t,e){const s=e>=8?Math.ceil(e/5):1/0,r=new Map;for(const o of t)r.has(o.grammarPatternId)||r.set(o.grammarPatternId,[]),r.get(o.grammarPatternId).push(o);for(const o of r.values())C(o);const c=[],i=[...r.values()];C(i);let u=0;for(;c.length<e&&i.some(o=>o.length>0);){const o=i[u%i.length];if(o.length>0&&o.filter(n=>c.includes(n)).length<s){const n=o.shift();n&&c.push(n)}if(u++,u>e*50)break}return c.slice(0,Math.min(e,t.length))}function C(t){for(let e=t.length-1;e>0;e--){const s=Math.floor(Math.random()*(e+1));[t[e],t[s]]=[t[s],t[e]]}return t}async function j(t,e,s={}){const r=await E(),c=G(r,t),i=!!s.examMode;a={questions:c,answers:{},tileOrders:{},currentIdx:0,startedAt:new Date().toISOString(),examMode:i,durationSec:i?t*H:null},i?(f=Date.now()+a.durationSec*1e3,v&&clearInterval(v),v=setInterval(()=>U(e),1e3)):f=null,y="attempting",window.__testInProgress=!0,I(e)}function U(t){if(!f||y!=="attempting")return;const e=f-Date.now(),s=document.getElementById("test-timer");if(s){const r=Math.max(0,Math.ceil(e/1e3)),c=String(Math.floor(r/60)).padStart(2,"0"),i=String(r%60).padStart(2,"0");s.textContent=`${c}:${i}`,s.classList.toggle("danger",r<=60),s.classList.toggle("warning",r>60&&r<=300)}e<=0&&(clearInterval(v),v=null,f=null,D(t))}function I(t){const e=a.questions.length,s=a.questions[a.currentIdx],r=a.questions.filter(n=>!B(n)).length,c=r===0;let i="";s.type==="mcq"||s.type==="dropdown"?i=F(s):s.type==="sentence_order"?i=W(s):s.type==="text_input"?i=K(s):i=`<p class="placeholder-inline">Unsupported question type: ${g(s.type)}</p>`;let u="";if(a.examMode&&f){const n=Math.max(0,Math.ceil((f-Date.now())/1e3)),m=String(Math.floor(n/60)).padStart(2,"0"),w=String(n%60).padStart(2,"0");u=`<span id="test-timer" class="test-timer-chip${n<=60?" danger":n<=300?" warning":""}" aria-live="polite" title="Time remaining">${m}:${w}</span>`}t.innerHTML=`
    <div class="test-attempting">
      <div class="test-progress">
        <div class="progress-meta">
          <span>Question <strong>${a.currentIdx+1}</strong> of <strong>${e}</strong></span>
          ${u}
          <span class="answered-count">${e-r} / ${e} answered</span>
        </div>
        <div class="progress-bar"><div style="width:${(a.currentIdx+1)/e*100}%"></div></div>
      </div>

      <article class="question-card">
        <p class="prompt">${g(s.prompt_ja||"")}</p>
        ${s.question_ja?`<p class="question">${b(s.question_ja)}</p>`:""}
        ${i}
      </article>

      <div class="test-nav">
        <button id="prev-q" ${a.currentIdx===0?"disabled":""}>\u2190 Previous</button>
        <button id="next-q" ${a.currentIdx===e-1?"disabled":""}>Next \u2192</button>
        <button id="submit-test" class="btn-primary"
          ${c?"":"disabled"}
          title="${c?"Submit your test":`Answer all questions to submit (${r} remaining)`}">
          ${c?"Submit":`Submit (${r} remaining)`}
        </button>
      </div>
    </div>
  `,document.getElementById("prev-q")?.addEventListener("click",()=>R(a.currentIdx-1,t)),document.getElementById("next-q")?.addEventListener("click",()=>R(a.currentIdx+1,t)),document.getElementById("submit-test")?.addEventListener("click",()=>D(t)),t.querySelectorAll("[data-choice]").forEach(n=>{n.addEventListener("click",()=>{a.answers[s.id]=n.dataset.choice,I(t)})}),t.querySelectorAll("[data-tile-add]").forEach(n=>{n.addEventListener("click",()=>Y(s,n.dataset.tileAdd,t))}),t.querySelectorAll("[data-tile-remove]").forEach(n=>{n.addEventListener("click",()=>X(s,parseInt(n.dataset.tileRemove,10),t))});const o=t.querySelector("[data-text-input]");o&&(o.addEventListener("input",()=>{a.answers[s.id]=o.value;const n=a.questions.filter(M=>!B(M)).length,m=n===0,w=document.getElementById("submit-test");w&&(w.disabled=!m,w.textContent=m?"Submit":`Submit (${n} remaining)`,w.title=m?"Submit your test":`Answer all questions to submit (${n} remaining)`)}),typeof a.answers[s.id]=="string"&&(o.value=a.answers[s.id]))}function B(t){const e=a.answers[t.id];return t.type==="sentence_order"?Array.isArray(e)&&e.length===(t.tiles?.length||0):t.type==="text_input"?typeof e=="string"&&e.trim()!=="":e!=null&&e!==""}function R(t,e){t<0||t>=a.questions.length||(a.currentIdx=t,I(e))}function F(t){const e=a.answers[t.id];return`<div class="choice-grid">${(t.choices||[]).map(r=>`
    <button type="button" data-choice="${g(r)}" class="choice-button ${e===r?"selected":""}">
      ${b(r)}
    </button>
  `).join("")}</div>`}function K(t){const e=typeof a.answers[t.id]=="string"?a.answers[t.id]:"";return`
    <div class="text-input-wrap">
      <label for="text-input-${g(t.id)}" class="visually-hidden">Type your answer</label>
      <input
        id="text-input-${g(t.id)}"
        type="text"
        data-text-input
        class="text-input"
        autocomplete="off"
        autocapitalize="off"
        autocorrect="off"
        spellcheck="false"
        lang="ja"
        placeholder="Type kana or romaji..."
        value="${g(e)}">
      <p class="muted small">Accepts hiragana, katakana, or Hepburn romaji. Punctuation/whitespace ignored.</p>
    </div>
  `}function W(t){const e=a.answers[t.id]||[],s=(t.tiles||[]).filter(i=>!e.includes(i)),r=e.length?e.map((i,u)=>`
        <button type="button" data-tile-remove="${u}" class="tile ordered">${b(i)}</button>
      `).join(""):'<span class="tile-placeholder">Click tiles below to build the sentence</span>',c=s.map(i=>`
    <button type="button" data-tile-add="${g(i)}" class="tile">${b(i)}</button>
  `).join("");return`
    <div class="sentence-order">
      <div class="ordered-tray">${r}</div>
      <div class="tile-pool">${c}</div>
    </div>
  `}function Y(t,e,s){a.answers[t.id]||(a.answers[t.id]=[]),!a.answers[t.id].includes(e)&&(a.answers[t.id].push(e),I(s))}function X(t,e,s){Array.isArray(a.answers[t.id])&&(a.answers[t.id].splice(e,1),a.answers[t.id].length===0&&delete a.answers[t.id],I(s))}function V(t,e){if(t.type==="sentence_order"){if(!Array.isArray(e))return!1;const s=t.correctOrder||[];return e.length!==s.length?!1:e.every((r,c)=>r===s[c])}if(t.type==="text_input"){const s=t.acceptedAnswers||[t.correctAnswer];return z(e,s)}return e===t.correctAnswer}function D(t){v&&(clearInterval(v),v=null);const e=a.startedAt?Math.round((Date.now()-new Date(a.startedAt).getTime())/1e3):null,s=!!(a.examMode&&f&&Date.now()>=f);f=null;const r=a.questions.map(o=>{const n=a.answers[o.id];return{questionId:o.id,grammarPatternId:o.grammarPatternId,type:o.type,userAnswer:n,correctAnswer:o.correctAnswer??o.correctOrder,isCorrect:V(o,n)}}),c=r.filter(o=>o.isCorrect).length,i=r.length,u={timestamp:new Date().toISOString(),type:"test",total:i,correct:c,incorrect:i-c,percent:i>0?Math.round(c/i*100):0,examMode:a.examMode||!1,elapsedSec:e,timedOut:s,responses:r};$.recordTestResponses(r),$.recordTestResult(u),T={result:u,questions:a.questions},y="results",window.__testInProgress=!1,q(t)}async function q(t){const{result:e,questions:s}=T;await J();const r=e.responses.map(d=>{const l=s.find(p=>p.id===d.questionId);return Z(l,d)}).join(""),i=tt(e.responses).map(d=>{const l=x.get(d),p=l?l.pattern:d;return`<li><a href="#/review">${g(p)}</a></li>`}).join(""),u=e.percent>=k,o=`
    <div class="pass-badge ${u?"pass":"fail"}" role="status">
      ${u?`<strong>Pass</strong> \xB7 \u2265 ${k}% study target`:`<strong>Below pass</strong> \xB7 target ${k}% (you got ${e.percent}%)`}
    </div>
  `;let n="";if(typeof e.elapsedSec=="number"){const d=Math.floor(e.elapsedSec/60),l=String(e.elapsedSec%60).padStart(2,"0"),p=e.timedOut?" (auto-submitted at zero)":"";n=`<span class="score-time muted small">Time: ${d}m ${l}s${p}</span>`}const m=new Map;for(const d of e.responses){const l=x.get(d.grammarPatternId),p=l&&l.category||"Other";m.has(p)||m.set(p,{correct:0,total:0});const h=m.get(p);h.total+=1,d.isCorrect&&(h.correct+=1)}const w=[...m.entries()].sort((d,l)=>d[1].correct/d[1].total-l[1].correct/l[1].total).map(([d,{correct:l,total:p}])=>{const h=p>0?Math.round(l/p*100):0;return`
        <tr class="${h>=k?"pass":"fail"}">
          <td class="cat-name">${g(d)}</td>
          <td class="cat-score">${l} / ${p}</td>
          <td class="cat-pct">${h}%</td>
          <td class="cat-bar"><div class="cat-bar-track"><div class="cat-bar-fill" style="width:${h}%"></div></div></td>
        </tr>
      `}).join(""),M={mcq:"Multiple choice",sentence_order:"Sentence ordering",text_input:"Text input",dropdown:"Dropdown"},S=new Map;for(const d of e.responses){const l=d.type||"mcq";S.has(l)||S.set(l,{correct:0,total:0});const p=S.get(l);p.total+=1,d.isCorrect&&(p.correct+=1)}const N=[...S.entries()].sort((d,l)=>d[1].correct/d[1].total-l[1].correct/l[1].total).map(([d,{correct:l,total:p}])=>{const h=p>0?Math.round(l/p*100):0,P=h>=k?"pass":"fail",O=M[d]||d;return`
        <tr class="${P}">
          <td class="cat-name">${g(O)}</td>
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
          ${n}
        </div>
        ${o}
      </section>

      <section class="category-breakdown">
        <h3>By grammar category</h3>
        ${m.size>0?`
          <table class="category-table">
            <thead>
              <tr><th>Category</th><th>Score</th><th>%</th><th>Distribution</th></tr>
            </thead>
            <tbody>${w}</tbody>
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
            <tbody>${N}</tbody>
          </table>
          <p class="muted small">Types sorted by accuracy (weakest first). Useful for picking your next drill mode.</p>
        `:'<p class="muted small">All questions in this test were the same type - type breakdown is only meaningful when the test mixes question formats.</p>'}
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
  `,document.getElementById("new-test")?.addEventListener("click",()=>{a=null,T=null,y="setup",L(t)}),document.getElementById("back-to-learn")?.addEventListener("click",()=>{location.hash="#/learn"})}function Z(t,e){const s=e.isCorrect?"\u2713":"\u2717",r=e.isCorrect?"correct":"incorrect",c=Q(t,e.userAnswer),i=Q(t,e.correctAnswer),u=!e.isCorrect&&t.distractor_explanations&&typeof e.userAnswer=="string"?t.distractor_explanations[e.userAnswer]:null,o=x?.get(t.grammarPatternId),n=o?o.pattern:t.grammarPatternId;return`
    <li class="review-item ${r}">
      <div class="review-marker" aria-label="${e.isCorrect?"correct":"incorrect"}">${s}</div>
      <div class="review-body">
        <div class="review-question">
          ${t.question_ja?b(t.question_ja):g(t.prompt_ja||"")}
        </div>
        <div class="review-answers">
          <span class="answer-label">Your answer:</span>
          <span class="user-answer ${r}">${c}</span>
          ${e.isCorrect?"":`<span class="answer-label">Correct:</span><span class="correct-answer">${i}</span>`}
        </div>
        ${t.explanation_en?`<p class="review-explanation">${g(t.explanation_en)}</p>`:""}
        ${u?`<p class="distractor-explanation"><em>Why your choice was wrong:</em> ${g(u)}</p>`:""}
        <p class="review-pattern">Pattern: <a href="#/learn/${encodeURIComponent(t.grammarPatternId)}">${g(n)}</a></p>
      </div>
    </li>
  `}function Q(t,e){return t.type==="sentence_order"&&Array.isArray(e)?b(e.join(" ")):b(String(e??"-"))}function tt(t){return[...new Set($.getWeakPatternIds())]}function g(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{rt as renderTest};
