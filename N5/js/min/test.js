import{t as g}from"./i18n.js";import{renderJa as b}from"./furigana.js";import{matchesAnswer as z}from"./normalize.js";import*as k from"./storage.js";import{navigateTo as H}from"./router.js";let r=null,y="setup",A=null,M=null,x=null,$=null,w=null;const J=60,I=60;async function E(){if(M)return M;const t=await fetch("data/questions.json");if(!t.ok)throw new Error(`Failed to load questions.json: ${t.status}`);return M=(await t.json()).questions||[],M}async function G(){if(x)return x;const e=await(await fetch("data/grammar.json")).json();return x=new Map((e.patterns||[]).map(s=>[s.id,s])),x}async function it(t,e){if(!e&&y==="results"&&(y="setup",r=null,A=null),y==="attempting"&&r)return _(t);if(y==="results"&&A)return D(t);if(e){const s=parseInt(decodeURIComponent(e),10);if([20,30,50].includes(s)){await E(),k.setSettings({lastTestLength:s}),C(s,t);return}}return j(t)}async function j(t){y="setup";const e=await E(),s=k.getSettings(),a=s.lastTestLength||20,l=(k.getResults()||[]).length===0,i=!!s.examMode;let u=g("meta.mock_papers"),o=null;try{const n=await fetch("data/papers/manifest.json").then(h=>h.ok?h.json():null);n&&n.totalPapers&&n.totalQuestions&&(u=`${n.totalPapers} papers (${n.totalQuestions} questions)`),n&&Array.isArray(n.full_mock_papers)&&n.full_mock_papers.length&&(o=n.full_mock_papers)}catch{}t.innerHTML=`
    <h2>${g("page.test")}</h2>
    ${l?`
      <div class="empty-state-banner">
        <p><strong>${c(g("meta.first_mock_hint"))}</strong></p>
        <p><a href="#/learn">${c(g("meta.continue_learning"))} \u2192</a></p>
      </div>
    `:""}
    <!-- Promotional trust callout (round-9 follow-up 2026-05-07): the
         "your scores stay on this device" message is the strongest
         niche-N2 reassurance precisely at the moment a learner is
         about to submit results. Bunpro / Renshuu push results to
         their server; the callout makes the privacy claim concrete
         right where it matters most. -->
    <aside class="trust-callout" aria-label="Privacy reassurance">
      <strong>${g("trust.no_login")} \xB7 ${g("trust.no_tracking")} \xB7 ${g("trust.on_device")}</strong>
      <p>${g("trust.test_callout")}</p>
    </aside>
    <p>${c(g("meta.test_setup_intro"))}</p>
    <div class="test-setup">
      <label class="length-picker">
        <span>${c(g("meta.test_length"))}</span>
        <select id="test-length">
          <option value="20" ${a===20?"selected":""}>20 ${c(g("meta.questions_unit"))}</option>
          <option value="30" ${a===30?"selected":""}>30 ${c(g("meta.questions_unit"))}</option>
          <option value="50" ${a===50?"selected":""}>50 ${c(g("meta.questions_unit"))}</option>
        </select>
      </label>
      <label class="exam-mode-toggle" title="Adds a countdown timer at JLPT pace (~60 seconds per question). Auto-submits at zero.">
        <input type="checkbox" id="exam-mode" ${i?"checked":""}>
        <span>${c(g("test.exam_mode"))}</span>
      </label>
      <button id="start-test" class="btn-primary">${c(g("meta.start_test"))}</button>
      <p class="bank-note">Question bank: <strong>${e.length}</strong> available. Test length is capped at the bank size.</p>
      <p class="bank-note muted small">${c(g("test.pass_mark"))}: <strong>${I}%</strong> (JLPT N5 study target).</p>
    </div>
    <hr style="border:0; border-top:1px solid var(--c-border); margin:32px 0 24px;">
    <div class="test-papers-cta">
      <h3 style="margin:0 0 8px; font-weight:400;">${c(g("meta.mock_papers"))}</h3>
      <p style="margin:0 0 12px; color:var(--c-muted);">Take a focused paper from a specific JLPT section (Moji / Goi / Bunpou / Dokkai). ${u} across 4 sections, drawn from the audited <code>KnowledgeBank</code> question files.</p>
      <a class="btn-secondary" href="#/papers" style="text-decoration:none; padding:10px 18px; display:inline-block; min-height:44px; line-height:24px;">Browse papers \u2192</a>
    </div>
    <hr style="border:0; border-top:1px solid var(--c-border); margin:32px 0 24px;">
    <div class="test-sitting-cta">
      <h3 style="margin:0 0 8px; font-weight:400;">Full Mock Test (real JLPT N5 shape)</h3>
      <p style="margin:0 0 12px; color:var(--c-muted);">Take the entire JLPT N5 in one sitting: <strong>\u8A00\u8A9E\u77E5\u8B58\uFF08\u6587\u5B57\u30FB\u8A9E\u5F59\uFF09 30Q / 25 min</strong> \u2192 <strong>\u8A00\u8A9E\u77E5\u8B58\uFF08\u6587\u6CD5\uFF09\u30FB\u8AAD\u89E3 31Q / 50 min</strong> \u2192 <strong>\u8074\u89E3 24Q / 30 min</strong>. Total <strong>85Q / 105 min</strong> (close to the official 91Q / 105min). Each section runs at the official time budget and auto-submits at zero.${o?` ${o.length} papers available.`:""}</p>
      <!-- v1.17.18 (2026-05-27): stronger Test/Mock merge per user.
           Replaced the single "Start full mock test \u2192" CTA with the
           inline paper picker (was previously rendered as the landing
           screen of /#/sitting). Saves a click + makes the mock entry
           visible alongside the quick-test setup. Each card still
           routes into the existing /#/sitting/<n>/0 flow so the
           sitting renderer (js/sitting.js) is untouched. The
           /#/sitting bare landing also still works (it renders the
           same picker via sitting.js renderPicker()) for any inbound
           bookmark or external link. -->
      <div class="sitting-paper-grid">
        ${[1,2,3,4,5,6,7].map(n=>`
          <a class="sitting-paper-card" href="#/sitting/${n}/0">
            <span class="card-index" aria-hidden="true">${String(n).padStart(2,"0")}</span>
            <h3>${c(g("meta.paper_n").replace("${n}",n))}</h3>
            <p class="muted small">moji-${n} \xB7 goi-${n} \xB7 bunpou-${n} \xB7 dokkai-${n} \xB7 listening</p>
          </a>
        `).join("")}
      </div>
    </div>
  `,document.getElementById("start-test").addEventListener("click",()=>{const n=parseInt(document.getElementById("test-length").value,10),h=!!document.getElementById("exam-mode")?.checked;k.setSettings({lastTestLength:n,examMode:h}),C(n,t,{examMode:h})})}function U(t,e){const s=e>=8?Math.ceil(e/5):1/0,a=new Map;for(const o of t)a.has(o.grammarPatternId)||a.set(o.grammarPatternId,[]),a.get(o.grammarPatternId).push(o);for(const o of a.values())L(o);const l=[],i=[...a.values()];L(i);let u=0;for(;l.length<e&&i.some(o=>o.length>0);){const o=i[u%i.length];if(o.length>0&&o.filter(n=>l.includes(n)).length<s){const n=o.shift();n&&l.push(n)}if(u++,u>e*50)break}return l.slice(0,Math.min(e,t.length))}function L(t){for(let e=t.length-1;e>0;e--){const s=Math.floor(Math.random()*(e+1));[t[e],t[s]]=[t[s],t[e]]}return t}async function C(t,e,s={}){const a=await E(),l=U(a,t),i=!!s.examMode;r={questions:l,answers:{},tileOrders:{},currentIdx:0,startedAt:new Date().toISOString(),examMode:i,durationSec:i?t*J:null},i?(w=Date.now()+r.durationSec*1e3,$&&clearInterval($),$=setInterval(()=>F(e),1e3)):w=null,y="attempting",window.__testInProgress=!0,_(e)}function F(t){if(!w||y!=="attempting")return;const e=w-Date.now(),s=document.getElementById("test-timer");if(s){const a=Math.max(0,Math.ceil(e/1e3)),l=String(Math.floor(a/60)).padStart(2,"0"),i=String(a%60).padStart(2,"0");s.textContent=`${l}:${i}`,s.classList.toggle("danger",a<=60),s.classList.toggle("warning",a>60&&a<=300)}e<=0&&(clearInterval($),$=null,w=null,q(t))}function _(t){const e=r.questions.length,s=r.questions[r.currentIdx],a=r.questions.filter(n=>!B(n)).length,l=a===0;let i="";s.type==="mcq"||s.type==="dropdown"?i=K(s):s.type==="sentence_order"?i=Y(s):s.type==="text_input"?i=W(s):i=`<p class="placeholder-inline">Unsupported question type: ${c(s.type)}</p>`;let u="";if(r.examMode&&w){const n=Math.max(0,Math.ceil((w-Date.now())/1e3)),h=String(Math.floor(n/60)).padStart(2,"0"),v=String(n%60).padStart(2,"0");u=`<span id="test-timer" class="test-timer-chip${n<=60?" danger":n<=300?" warning":""}" aria-live="polite" title="Time remaining">${h}:${v}</span>`}t.innerHTML=`
    <div class="test-attempting">
      <div class="test-progress">
        <div class="progress-meta">
          <span>Question <strong>${r.currentIdx+1}</strong> of <strong>${e}</strong></span>
          ${u}
          <span class="answered-count">${e-a} / ${e} answered</span>
        </div>
        <div class="progress-bar"><div style="width:${(r.currentIdx+1)/e*100}%"></div></div>
      </div>

      <article class="question-card">
        <p class="prompt">${c(s.prompt_ja||"")}</p>
        ${s.question_ja?`<p class="question">${b(s.question_ja)}</p>`:""}
        ${i}
      </article>

      <div class="test-nav">
        <button id="prev-q" ${r.currentIdx===0?"disabled":""}>\u2190 Previous</button>
        <button id="next-q" ${r.currentIdx===e-1?"disabled":""}>Next \u2192</button>
        <button id="submit-test" class="btn-primary"
          ${l?"":"disabled"}
          title="${l?"Submit your test":`Answer all questions to submit (${a} remaining)`}">
          ${l?"Submit":`Submit (${a} remaining)`}
        </button>
      </div>
    </div>
  `,document.getElementById("prev-q")?.addEventListener("click",()=>R(r.currentIdx-1,t)),document.getElementById("next-q")?.addEventListener("click",()=>R(r.currentIdx+1,t)),document.getElementById("submit-test")?.addEventListener("click",()=>q(t)),t.querySelectorAll("[data-choice]").forEach(n=>{n.addEventListener("click",()=>{r.answers[s.id]=n.dataset.choice,_(t)})}),t.querySelectorAll("[data-tile-add]").forEach(n=>{n.addEventListener("click",()=>X(s,n.dataset.tileAdd,t))}),t.querySelectorAll("[data-tile-remove]").forEach(n=>{n.addEventListener("click",()=>V(s,parseInt(n.dataset.tileRemove,10),t))});const o=t.querySelector("[data-text-input]");o&&(o.addEventListener("input",()=>{r.answers[s.id]=o.value;const n=r.questions.filter(T=>!B(T)).length,h=n===0,v=document.getElementById("submit-test");v&&(v.disabled=!h,v.textContent=h?"Submit":`Submit (${n} remaining)`,v.title=h?"Submit your test":`Answer all questions to submit (${n} remaining)`)}),typeof r.answers[s.id]=="string"&&(o.value=r.answers[s.id]))}function B(t){const e=r.answers[t.id];return t.type==="sentence_order"?Array.isArray(e)&&e.length===(t.tiles?.length||0):t.type==="text_input"?typeof e=="string"&&e.trim()!=="":e!=null&&e!==""}function R(t,e){t<0||t>=r.questions.length||(r.currentIdx=t,_(e))}function K(t){const e=r.answers[t.id];return`<div class="choice-grid">${(t.choices||[]).map(a=>`
    <button type="button" data-choice="${c(a)}" class="choice-button ${e===a?"selected":""}">
      ${b(a)}
    </button>
  `).join("")}</div>`}function W(t){const e=typeof r.answers[t.id]=="string"?r.answers[t.id]:"";return`
    <div class="text-input-wrap">
      <label for="text-input-${c(t.id)}" class="visually-hidden">Type your answer</label>
      <input
        id="text-input-${c(t.id)}"
        type="text"
        data-text-input
        class="text-input"
        autocomplete="off"
        autocapitalize="off"
        autocorrect="off"
        spellcheck="false"
        lang="ja"
        placeholder="Type kana or romaji..."
        value="${c(e)}">
      <p class="muted small">Accepts hiragana, katakana, or Hepburn romaji. Punctuation/whitespace ignored.</p>
    </div>
  `}function Y(t){const e=r.answers[t.id]||[],s=(t.tiles||[]).filter(i=>!e.includes(i)),a=e.length?e.map((i,u)=>`
        <button type="button" data-tile-remove="${u}" class="tile ordered">${b(i)}</button>
      `).join(""):'<span class="tile-placeholder">Click tiles below to build the sentence</span>',l=s.map(i=>`
    <button type="button" data-tile-add="${c(i)}" class="tile">${b(i)}</button>
  `).join("");return`
    <div class="sentence-order">
      <div class="ordered-tray">${a}</div>
      <div class="tile-pool">${l}</div>
    </div>
  `}function X(t,e,s){r.answers[t.id]||(r.answers[t.id]=[]),!r.answers[t.id].includes(e)&&(r.answers[t.id].push(e),_(s))}function V(t,e,s){Array.isArray(r.answers[t.id])&&(r.answers[t.id].splice(e,1),r.answers[t.id].length===0&&delete r.answers[t.id],_(s))}function Z(t,e){if(t.type==="sentence_order"){if(!Array.isArray(e))return!1;const s=t.correctOrder||[];return e.length!==s.length?!1:e.every((a,l)=>a===s[l])}if(t.type==="text_input"){const s=t.acceptedAnswers||[t.correctAnswer];return z(e,s)}return e===t.correctAnswer}function q(t){$&&(clearInterval($),$=null);const e=r.startedAt?Math.round((Date.now()-new Date(r.startedAt).getTime())/1e3):null,s=!!(r.examMode&&w&&Date.now()>=w);w=null;const a=r.questions.map(o=>{const n=r.answers[o.id];return{questionId:o.id,grammarPatternId:o.grammarPatternId,type:o.type,userAnswer:n,correctAnswer:o.correctAnswer??o.correctOrder,isCorrect:Z(o,n)}}),l=a.filter(o=>o.isCorrect).length,i=a.length,u={timestamp:new Date().toISOString(),type:"test",total:i,correct:l,incorrect:i-l,percent:i>0?Math.round(l/i*100):0,examMode:r.examMode||!1,elapsedSec:e,timedOut:s,responses:a};k.recordTestResponses(a),k.recordTestResult(u),A={result:u,questions:r.questions},y="results",window.__testInProgress=!1,D(t)}async function D(t){const{result:e,questions:s}=A;await G();const a=e.responses.map(p=>{const d=s.find(m=>m.id===p.questionId);return tt(d,p)}).join(""),i=et(e.responses).map(p=>{const d=x.get(p),m=d?d.pattern:p;return`<li><a href="#/review">${c(m)}</a></li>`}).join(""),u=e.percent>=I,o=`
    <div class="pass-badge ${u?"pass":"fail"}" role="status">
      ${u?`<strong>Pass</strong> \xB7 \u2265 ${I}% study target`:`<strong>Below pass</strong> \xB7 target ${I}% (you got ${e.percent}%)`}
    </div>
  `;let n="";if(typeof e.elapsedSec=="number"){const p=Math.floor(e.elapsedSec/60),d=String(e.elapsedSec%60).padStart(2,"0"),m=e.timedOut?" (auto-submitted at zero)":"";n=`<span class="score-time muted small">Time: ${p}m ${d}s${m}</span>`}const h=new Map;for(const p of e.responses){const d=x.get(p.grammarPatternId),m=d&&d.category||"Other";h.has(m)||h.set(m,{correct:0,total:0});const f=h.get(m);f.total+=1,p.isCorrect&&(f.correct+=1)}const v=[...h.entries()].sort((p,d)=>p[1].correct/p[1].total-d[1].correct/d[1].total).map(([p,{correct:d,total:m}])=>{const f=m>0?Math.round(d/m*100):0;return`
        <tr class="${f>=I?"pass":"fail"}">
          <td class="cat-name">${c(p)}</td>
          <td class="cat-score">${d} / ${m}</td>
          <td class="cat-pct">${f}%</td>
          <td class="cat-bar"><div class="cat-bar-track"><div class="cat-bar-fill" style="width:${f}%"></div></div></td>
        </tr>
      `}).join(""),T={mcq:"Multiple choice",sentence_order:"Sentence ordering",text_input:"Text input",dropdown:"Dropdown"},S=new Map;for(const p of e.responses){const d=p.type||"mcq";S.has(d)||S.set(d,{correct:0,total:0});const m=S.get(d);m.total+=1,p.isCorrect&&(m.correct+=1)}const N=[...S.entries()].sort((p,d)=>p[1].correct/p[1].total-d[1].correct/d[1].total).map(([p,{correct:d,total:m}])=>{const f=m>0?Math.round(d/m*100):0,P=f>=I?"pass":"fail",O=T[p]||p;return`
        <tr class="${P}">
          <td class="cat-name">${c(O)}</td>
          <td class="cat-score">${d} / ${m}</td>
          <td class="cat-pct">${f}%</td>
          <td class="cat-bar"><div class="cat-bar-track"><div class="cat-bar-fill" style="width:${f}%"></div></div></td>
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
        ${h.size>0?`
          <table class="category-table">
            <thead>
              <tr><th>Category</th><th>Score</th><th>%</th><th>Distribution</th></tr>
            </thead>
            <tbody>${v}</tbody>
          </table>
          <p class="muted small">Categories sorted by accuracy (weakest first). Pass target ${I}%.</p>
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
        <ol class="review-list">${a}</ol>
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
  `,document.getElementById("new-test")?.addEventListener("click",()=>{r=null,A=null,y="setup",j(t)}),document.getElementById("back-to-learn")?.addEventListener("click",()=>{H("learn")})}function tt(t,e){const s=e.isCorrect?"\u2713":"\u2717",a=e.isCorrect?"correct":"incorrect",l=Q(t,e.userAnswer),i=Q(t,e.correctAnswer),u=!e.isCorrect&&t.distractor_explanations&&typeof e.userAnswer=="string"?t.distractor_explanations[e.userAnswer]:null,o=x?.get(t.grammarPatternId),n=o?o.pattern:t.grammarPatternId;return`
    <li class="review-item ${a}">
      <div class="review-marker" aria-label="${e.isCorrect?"correct":"incorrect"}">${s}</div>
      <div class="review-body">
        <div class="review-question">
          ${t.question_ja?b(t.question_ja):c(t.prompt_ja||"")}
        </div>
        <div class="review-answers">
          <span class="answer-label">Your answer:</span>
          <span class="user-answer ${a}">${l}</span>
          ${e.isCorrect?"":`<span class="answer-label">Correct:</span><span class="correct-answer">${i}</span>`}
        </div>
        ${t.explanation_en?`<p class="review-explanation">${c(t.explanation_en)}</p>`:""}
        ${u?`<p class="distractor-explanation"><em>Why your choice was wrong:</em> ${c(u)}</p>`:""}
        <p class="review-pattern">Pattern: <a href="#/learn/${encodeURIComponent(t.grammarPatternId)}">${c(n)}</a></p>
      </div>
    </li>
  `}function Q(t,e){return t.type==="sentence_order"&&Array.isArray(e)?b(e.join(" ")):b(String(e??"-"))}function et(t){return[...new Set(k.getWeakPatternIds())]}function c(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{it as renderTest};
