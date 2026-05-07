import"./furigana.js";import*as I from"./storage.js";let $=null;const v=new Map;let m=null,u="setup",g=null;const P={moji:11,goi:11,bunpou:23,dokkai:23};let o=null,f=null;async function y(){if($)return $;const t=await fetch("data/papers/manifest.json");if(!t.ok)throw new Error(`Failed to load papers manifest: ${t.status}`);return $=await t.json(),$}async function M(t,e){const s=`${t}-${e}`;if(v.has(s))return v.get(s);const a=await fetch(`data/papers/${t}/paper-${e}.json`);if(!a.ok)throw new Error(`Failed to load paper ${s}: ${a.status}`);const n=await a.json();return v.set(s,n),n}function S(t){return`jlpt-n5-tutor.paper.${t}`}function b(t){try{const e=localStorage.getItem(S(t));return e?JSON.parse(e):{attempts:0,bestScore:null,lastScore:null}}catch{return{attempts:0,bestScore:null,lastScore:null}}}function q(t,e,s){const a=b(t),n={attempts:(a.attempts||0)+1,bestScore:a.bestScore==null?{correct:e,total:s}:e>a.bestScore.correct?{correct:e,total:s}:a.bestScore,lastScore:{correct:e,total:s,dateIso:new Date().toISOString()}};return localStorage.setItem(S(t),JSON.stringify(n)),n}async function A(t,e){const s=(e||"").split("/").filter(Boolean);if(s.length<2&&(u==="attempting"||u==="results")&&(u="setup",m=null,g=null),u==="attempting"&&m)return h(t);if(u==="results"&&g)return j(t);if(s.length===0)return x(t);if(s.length===1)return L(t,s[0]);if(s.length===2){const[a,n]=s;return _(t,a,parseInt(n,10))}return x(t)}async function x(t){const e=await y(),s=e.categories.map(a=>{const n=a.papers.filter(r=>(b(r.id).attempts||0)>0).length;return`
      <a class="paper-cat-card" href="#/papers/${c(a.id)}">
        <div class="paper-cat-icon" aria-hidden="true">${E(a.id)}</div>
        <div class="paper-cat-meta">
          <h3>${c(a.label)} <span class="paper-cat-ja" lang="ja">${c(a.label_ja)}</span></h3>
          <p class="paper-cat-desc">${c(a.description)}</p>
          <p class="paper-cat-stats">
            <span class="paper-stat">${a.paperCount} papers</span>
            <span class="paper-stat-sep">\xB7</span>
            <span class="paper-stat">${a.questionCount} questions</span>
            <span class="paper-stat-sep">\xB7</span>
            <span class="paper-stat">${n} of ${a.paperCount} attempted</span>
          </p>
        </div>
      </a>
    `}).join("");t.innerHTML=`
    <article class="papers-index">
      <a class="back-link" href="#/test">\u2190 Back to Test</a>
      <h2>Mock-test Papers</h2>
      <p class="page-lede">${e.totalQuestions} audited JLPT N5 questions across ${e.totalPapers} papers in 4 sections. Each paper is sized to a study-session (15 questions, ~10 minutes). Scores persist locally so you can track which papers you've completed.</p>
      <div class="paper-cat-grid">${s}</div>
      <p class="papers-foot-note">Source: <code>KnowledgeBank/{moji,goi,bunpou,dokkai}_questions_n5.md</code> - curated and native-teacher-reviewed across Pass-9 through Pass-19.</p>
    </article>
  `}function E(t){return`<span class="paper-cat-letter" lang="ja">${{moji:"\u5B57",goi:"\u8A9E",bunpou:"\u6CD5",dokkai:"\u8AAD"}[t]||"?"}</span>`}async function L(t,e){const a=(await y()).categories.find(r=>r.id===e);if(!a){t.innerHTML=`
      <article class="papers-index">
        <a class="back-link" href="#/papers">\u2190 Back to Mock-test Papers</a>
        <h2>Unknown category</h2>
        <p>The category <code>${c(e)}</code> doesn't exist. <a href="#/papers">Return to the index.</a></p>
      </article>
    `;return}const n=a.papers.map(r=>{const i=b(r.id),d=(i.attempts||0)>0,p=i.bestScore,l=d?`<span class="paper-badge paper-badge-done">${p?`${p.correct}/${p.total}`:"Done"}</span>`:'<span class="paper-badge paper-badge-new">New</span>';return`
      <div class="paper-card-row">
        <a class="paper-card" href="#/papers/${c(a.id)}/${r.paperNumber}">
          <div class="paper-card-num">Paper ${r.paperNumber}</div>
          <div class="paper-card-meta">
            <span class="paper-q-count">${r.questionCount} questions</span>
            <span class="paper-source-range muted">${c(r.source_question_range)}</span>
          </div>
          ${l}
        </a>
        <a class="paper-card-print" href="#/print/${c(r.id)}" title="Open print-friendly view (Save as PDF or print to paper)" aria-label="Print Paper ${r.paperNumber}">
          <span aria-hidden="true">\u{1F5A8}</span>
          <span class="paper-card-print-label">Print</span>
        </a>
      </div>
    `}).join("");t.innerHTML=`
    <article class="papers-index">
      <a class="back-link" href="#/papers">\u2190 All sections</a>
      <h2>${c(a.label)} <span class="paper-cat-ja" lang="ja">${c(a.label_ja)}</span></h2>
      <p class="page-lede">${c(a.description)} \xB7 ${a.paperCount} papers \xB7 ${a.questionCount} questions total. <a class="muted small" href="#/print">Print any paper \u2192</a></p>
      <div class="paper-list-grid">${n}</div>
    </article>
  `}async function _(t,e,s){if(!Number.isInteger(s)||s<1){t.innerHTML="<p>Invalid paper number.</p>";return}const a=await M(e,s),n=!!I.getSettings().examMode,r=P[e]||15;return m={paper:a,paperId:a.id,categoryId:e,paperNumber:s,questions:a.questions,answers:new Array(a.questions.length).fill(null),currentIdx:0,submitted:!1,examMode:n,durationSec:n?r*60:null},n?(f=Date.now()+r*60*1e3,o&&clearInterval(o),o=setInterval(()=>T(t),1e3)):(f=null,o&&(clearInterval(o),o=null)),u="attempting",h(t)}function T(t){if(!m||!f)return;const e=f-Date.now(),s=document.getElementById("paper-timer");if(!s)return;if(e<=0){o&&clearInterval(o),o=null,s.textContent="00:00",s.classList.add("timer-expired"),k(t);return}const a=Math.floor(e/6e4),n=Math.floor(e%6e4/1e3);s.textContent=`${String(a).padStart(2,"0")}:${String(n).padStart(2,"0")}`,e<6e4&&s.classList.add("timer-low")}function h(t){const e=m;if(!e){t.innerHTML='<p>No active session. <a href="#/papers">Pick a paper.</a></p>';return}const s=e.questions[e.currentIdx],a=e.questions.length,n=e.answers.filter(p=>p!==null).length,r=s.passage_text?`<div class="paper-passage" lang="ja">${w(s.passage_text)}</div>`:"",i=s.choices.map((p,l)=>`
    <label class="paper-choice ${e.answers[e.currentIdx]===l?"selected":""}">
      <input type="radio" name="choice" value="${l}" ${e.answers[e.currentIdx]===l?"checked":""}>
      <span class="paper-choice-letter">${l+1}</span>
      <span class="paper-choice-text" lang="ja">${w(p)}</span>
    </label>
  `).join("");t.innerHTML=`
    <article class="paper-attempting">
      <header class="paper-progress-bar">
        <a class="paper-quit" href="#/papers/${c(e.categoryId)}" title="Quit and return to paper list">\u2715 Quit</a>
        <div class="paper-progress-info">
          <span class="paper-progress-current">Q${e.currentIdx+1}</span>
          <span class="paper-progress-of">of ${a}</span>
          <span class="paper-progress-answered">\xB7 ${n} answered</span>
          ${e.examMode?`<span class="paper-timer-wrap">\xB7 <span id="paper-timer" class="paper-timer">${B(e.durationSec*1e3)}</span></span>`:""}
        </div>
      </header>
      ${r}
      <div class="paper-question-stem" lang="ja">${w(s.stem_html)}</div>
      <form class="paper-choices" id="paper-choices-form">${i}</form>
      <footer class="paper-controls">
        <button type="button" class="btn-secondary" id="paper-prev" ${e.currentIdx===0?"disabled":""}>\u2190 Previous</button>
        ${e.currentIdx===a-1?(()=>{const p=a-n,l=p===0;return`
                <div class="paper-submit-cluster">
                  ${l?"":`<p class="paper-submit-hint">Answer all ${a} questions to submit \xB7 <strong>${p}</strong> ${p===1?"question":"questions"} unanswered</p>`}
                  <button type="button" class="btn-primary" id="paper-submit" ${l?"":"disabled"} title="${l?"Submit your paper":`Answer all questions to submit (${p} remaining)`}">${l?"Submit paper":`Submit paper (${p} remaining)`}</button>
                </div>`})():'<button type="button" class="btn-primary" id="paper-next">Next \u2192</button>'}
      </footer>
    </article>
  `,document.getElementById("paper-choices-form").addEventListener("change",p=>{p.target&&p.target.name==="choice"&&(e.answers[e.currentIdx]=parseInt(p.target.value,10),h(t))}),document.getElementById("paper-prev")?.addEventListener("click",()=>{e.currentIdx>0&&(e.currentIdx-=1,h(t))}),document.getElementById("paper-next")?.addEventListener("click",()=>{e.currentIdx<a-1&&(e.currentIdx+=1,h(t))}),document.getElementById("paper-submit")?.addEventListener("click",()=>{k(t)})}function B(t){t<0&&(t=0);const e=Math.floor(t/6e4),s=Math.floor(t%6e4/1e3);return`${String(e).padStart(2,"0")}:${String(s).padStart(2,"0")}`}function w(t){return t?`<span class="ja-text" lang="ja">${t}</span>`:""}function k(t){const e=m;o&&(clearInterval(o),o=null),f=null;let s=0;const a=e.questions.map((r,i)=>{const d=e.answers[i],p=d===r.correctIndex;return p&&(s+=1),{idx:i,kbSourceId:r.kbSourceId,stem_html:r.stem_html,choices:r.choices,correctIndex:r.correctIndex,chosen:d,isRight:p,rationale:r.rationale||""}}),n=e.questions.length;q(e.paperId,s,n);try{e.questions.forEach((r,i)=>{const d=e.answers[i]===r.correctIndex;I.recordAttempt?.(`paper:${e.categoryId}:${r.kbSourceId}`,d,"paper")})}catch{}return g={paperId:e.paperId,paperName:e.paper.name,categoryId:e.categoryId,correct:s,total:n,detail:a},u="results",m=null,j(t)}function j(t){const e=g;if(!e){t.innerHTML='<p>No results to display. <a href="#/papers">Pick a paper.</a></p>';return}const s=Math.round(e.correct/e.total*100),a=s>=80?"Great work":s>=60?"Solid":s>=40?"Keep going":"Review and retry",n=e.detail.map(r=>`
    <li class="paper-review-item ${r.isRight?"review-right":"review-wrong"}">
      <div class="paper-review-head">
        <span class="paper-review-num">Q${r.idx+1}</span>
        <span class="paper-review-status">${r.isRight?"\u2713":"\u2717"}</span>
        <span class="paper-review-source muted">${c(r.kbSourceId)}</span>
      </div>
      <div class="paper-review-stem ja-text" lang="ja">${r.stem_html}</div>
      <ol class="paper-review-choices">
        ${r.choices.map((i,d)=>`<li class="${d===r.correctIndex?"choice-correct":d===r.chosen?"choice-chosen-wrong":""}" lang="ja">${c(i)}</li>`).join("")}
      </ol>
      ${r.rationale?`<p class="paper-review-rationale">${c(r.rationale)}</p>`:""}
    </li>
  `).join("");t.innerHTML=`
    <article class="paper-results">
      <header class="paper-results-summary">
        <h2>${c(e.paperName)} \xB7 Results</h2>
        <div class="paper-score-display">
          <div class="paper-score-big">${e.correct}<span class="paper-score-of">/${e.total}</span></div>
          <div class="paper-score-pct">${s}%</div>
          <div class="paper-score-verdict">${a}</div>
        </div>
      </header>
      <nav class="paper-results-actions">
        <a class="btn-primary" href="#/papers/${c(e.categoryId)}">Back to ${c(e.categoryId)} papers</a>
        <a class="btn-secondary" href="#/papers/${c(e.categoryId)}/${parseInt(e.paperId.split("-")[1],10)}" id="paper-retry">Retry this paper</a>
      </nav>
      <section class="paper-review">
        <h3>Question review</h3>
        <ol class="paper-review-list">${n}</ol>
      </section>
    </article>
  `,document.getElementById("paper-retry")?.addEventListener("click",()=>{u="setup",g=null})}function c(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{A as renderPapers};
