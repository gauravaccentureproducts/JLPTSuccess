import"./furigana.js";import*as I from"./storage.js";let $=null;const b=new Map;let m=null,u="setup",g=null;const P={moji:11,goi:11,bunpou:23,dokkai:23};let l=null,f=null;async function y(){if($)return $;const a=await fetch("data/papers/manifest.json");if(!a.ok)throw new Error(`Failed to load papers manifest: ${a.status}`);return $=await a.json(),$}async function M(a,e){const t=`${a}-${e}`;if(b.has(t))return b.get(t);const s=await fetch(`data/papers/${a}/paper-${e}.json`);if(!s.ok)throw new Error(`Failed to load paper ${t}: ${s.status}`);const n=await s.json();return b.set(t,n),n}function S(a){return`jlpt-n5-tutor.paper.${a}`}function w(a){try{const e=localStorage.getItem(S(a));return e?JSON.parse(e):{attempts:0,bestScore:null,lastScore:null}}catch{return{attempts:0,bestScore:null,lastScore:null}}}function q(a,e,t){const s=w(a),n={attempts:(s.attempts||0)+1,bestScore:s.bestScore==null?{correct:e,total:t}:e>s.bestScore.correct?{correct:e,total:t}:s.bestScore,lastScore:{correct:e,total:t,dateIso:new Date().toISOString()}};return localStorage.setItem(S(a),JSON.stringify(n)),n}async function R(a,e){const t=(e||"").split("/").filter(Boolean);if(t.length<2&&(u==="attempting"||u==="results")&&(u="setup",m=null,g=null),u==="attempting"&&m)return h(a);if(u==="results"&&g)return j(a);if(t.length===0)return x(a);if(t.length===1)return E(a,t[0]);if(t.length===2){const[s,n]=t;return L(a,s,parseInt(n,10))}return x(a)}async function x(a){const e=await y(),t=e.categories.map(s=>{const n=s.papers.filter(r=>(w(r.id).attempts||0)>0).length;return`
      <a class="paper-cat-card" href="#/papers/${c(s.id)}">
        <div class="paper-cat-icon" aria-hidden="true">${_(s.id)}</div>
        <div class="paper-cat-meta">
          <h3>${c(s.label)} <span class="paper-cat-ja" lang="ja">${c(s.label_ja)}</span></h3>
          <p class="paper-cat-desc">${c(s.description)}</p>
          <p class="paper-cat-stats">
            <span class="paper-stat">${s.paperCount} papers</span>
            <span class="paper-stat-sep">\xB7</span>
            <span class="paper-stat">${s.questionCount} questions</span>
            <span class="paper-stat-sep">\xB7</span>
            <span class="paper-stat">${n} of ${s.paperCount} attempted</span>
          </p>
        </div>
      </a>
    `}).join("");a.innerHTML=`
    <article class="papers-index">
      <a class="back-link" href="#/test">\u2190 Back to Test</a>
      <h2>Mock-test Papers</h2>
      <p class="page-lede">${e.totalQuestions} audited JLPT N5 questions across ${e.totalPapers} papers in 4 sections. Each paper is sized to a study-session (15 questions, ~10 minutes). Scores persist locally so you can track which papers you've completed.</p>
      <div class="paper-cat-grid">${t}</div>
      <p class="papers-foot-note">Source: <code>KnowledgeBank/{moji,goi,bunpou,dokkai}_questions_n5.md</code> - curated and native-teacher-reviewed across Pass-9 through Pass-19.</p>
    </article>
  `}function _(a){return`<span class="paper-cat-letter" lang="ja">${{moji:"\u5B57",goi:"\u8A9E",bunpou:"\u6CD5",dokkai:"\u8AAD"}[a]||"?"}</span>`}async function E(a,e){const s=(await y()).categories.find(r=>r.id===e);if(!s){a.innerHTML=`
      <article class="papers-index">
        <a class="back-link" href="#/papers">\u2190 Back to Mock-test Papers</a>
        <h2>Unknown category</h2>
        <p>The category <code>${c(e)}</code> doesn't exist. <a href="#/papers">Return to the index.</a></p>
      </article>
    `;return}const n=s.papers.map(r=>{const o=w(r.id),d=(o.attempts||0)>0,p=o.bestScore,i=d?`<span class="paper-badge paper-badge-done">${p?`${p.correct}/${p.total}`:"Done"}</span>`:'<span class="paper-badge paper-badge-new">New</span>';return`
      <div class="paper-card-row">
        <a class="paper-card" href="#/papers/${c(s.id)}/${r.paperNumber}">
          <div class="paper-card-num">Paper ${r.paperNumber}</div>
          <div class="paper-card-meta">
            <span class="paper-q-count">${r.questionCount} questions</span>
            <span class="paper-source-range muted">${c(r.source_question_range)}</span>
          </div>
          ${i}
        </a>
        <a class="paper-card-print" href="#/print/${c(r.id)}" title="Open print-friendly view (Save as PDF or print to paper)" aria-label="Print Paper ${r.paperNumber}">
          <span aria-hidden="true">\u{1F5A8}</span>
          <span class="paper-card-print-label">Print</span>
        </a>
      </div>
    `}).join("");a.innerHTML=`
    <article class="papers-index">
      <a class="back-link" href="#/papers">\u2190 All sections</a>
      <h2>${c(s.label)} <span class="paper-cat-ja" lang="ja">${c(s.label_ja)}</span></h2>
      <p class="page-lede">${c(s.description)} \xB7 ${s.paperCount} papers \xB7 ${s.questionCount} questions total. <a class="muted small" href="#/print">Print any paper \u2192</a></p>
      <div class="paper-list-grid">${n}</div>
    </article>
  `}async function L(a,e,t){if(!Number.isInteger(t)||t<1){a.innerHTML="<p>Invalid paper number.</p>";return}const s=await M(e,t),n=!!I.getSettings().examMode,r=P[e]||15;return m={paper:s,paperId:s.id,categoryId:e,paperNumber:t,questions:s.questions,answers:new Array(s.questions.length).fill(null),currentIdx:0,submitted:!1,examMode:n,durationSec:n?r*60:null},n?(f=Date.now()+r*60*1e3,l&&clearInterval(l),l=setInterval(()=>T(a),1e3)):(f=null,l&&(clearInterval(l),l=null)),u="attempting",h(a)}function T(a){if(!m||!f)return;const e=f-Date.now(),t=document.getElementById("paper-timer");if(!t)return;if(e<=0){l&&clearInterval(l),l=null,t.textContent="00:00",t.classList.add("timer-expired"),k(a);return}const s=Math.floor(e/6e4),n=Math.floor(e%6e4/1e3);t.textContent=`${String(s).padStart(2,"0")}:${String(n).padStart(2,"0")}`,e<6e4&&t.classList.add("timer-low")}function h(a){const e=m;if(!e){a.innerHTML='<p>No active session. <a href="#/papers">Pick a paper.</a></p>';return}const t=e.questions[e.currentIdx],s=e.questions.length,n=e.answers.filter(p=>p!==null).length;let r="";if(t.passage_label&&Array.isArray(e.paper?.passages)){const p=e.paper.passages.find(i=>i&&i.label===t.passage_label);p&&p.text&&(r=`<div class="paper-passage" lang="ja">${v(p.text)}</div>`)}else t.passage_text&&(r=`<div class="paper-passage" lang="ja">${v(t.passage_text)}</div>`);const o=t.choices.map((p,i)=>`
    <label class="paper-choice ${e.answers[e.currentIdx]===i?"selected":""}">
      <input type="radio" name="choice" value="${i}" ${e.answers[e.currentIdx]===i?"checked":""}>
      <span class="paper-choice-letter">${i+1}</span>
      <span class="paper-choice-text" lang="ja">${v(p)}</span>
    </label>
  `).join("");a.innerHTML=`
    <article class="paper-attempting">
      <header class="paper-progress-bar">
        <a class="paper-quit" href="#/papers/${c(e.categoryId)}" title="Quit and return to paper list">\u2715 Quit</a>
        <div class="paper-progress-info">
          <span class="paper-progress-current">Q${e.currentIdx+1}</span>
          <span class="paper-progress-of">of ${s}</span>
          <span class="paper-progress-answered">\xB7 ${n} answered</span>
          ${e.examMode?`<span class="paper-timer-wrap">\xB7 <span id="paper-timer" class="paper-timer">${A(e.durationSec*1e3)}</span></span>`:""}
        </div>
      </header>
      ${r}
      <div class="paper-question-stem" lang="ja">${v(t.stem_html)}</div>
      <form class="paper-choices" id="paper-choices-form">${o}</form>
      <footer class="paper-controls">
        <button type="button" class="btn-secondary" id="paper-prev" ${e.currentIdx===0?"disabled":""}>\u2190 Previous</button>
        ${e.currentIdx===s-1?(()=>{const p=s-n,i=p===0;return`
                <div class="paper-submit-cluster">
                  ${i?"":`<p class="paper-submit-hint">Answer all ${s} questions to submit \xB7 <strong>${p}</strong> ${p===1?"question":"questions"} unanswered</p>`}
                  <button type="button" class="btn-primary" id="paper-submit" ${i?"":"disabled"} title="${i?"Submit your paper":`Answer all questions to submit (${p} remaining)`}">${i?"Submit paper":`Submit paper (${p} remaining)`}</button>
                </div>`})():'<button type="button" class="btn-primary" id="paper-next">Next \u2192</button>'}
      </footer>
    </article>
  `,document.getElementById("paper-choices-form").addEventListener("change",p=>{p.target&&p.target.name==="choice"&&(e.answers[e.currentIdx]=parseInt(p.target.value,10),h(a))}),document.getElementById("paper-prev")?.addEventListener("click",()=>{e.currentIdx>0&&(e.currentIdx-=1,h(a))}),document.getElementById("paper-next")?.addEventListener("click",()=>{e.currentIdx<s-1&&(e.currentIdx+=1,h(a))}),document.getElementById("paper-submit")?.addEventListener("click",()=>{k(a)})}function A(a){a<0&&(a=0);const e=Math.floor(a/6e4),t=Math.floor(a%6e4/1e3);return`${String(e).padStart(2,"0")}:${String(t).padStart(2,"0")}`}function v(a){return a?`<span class="ja-text" lang="ja">${a}</span>`:""}function k(a){const e=m;l&&(clearInterval(l),l=null),f=null;let t=0;const s=e.questions.map((r,o)=>{const d=e.answers[o],p=d===r.correctIndex;return p&&(t+=1),{idx:o,kbSourceId:r.kbSourceId,stem_html:r.stem_html,choices:r.choices,correctIndex:r.correctIndex,chosen:d,isRight:p,rationale:r.rationale||""}}),n=e.questions.length;q(e.paperId,t,n);try{e.questions.forEach((r,o)=>{const d=e.answers[o]===r.correctIndex;I.recordAttempt?.(`paper:${e.categoryId}:${r.kbSourceId}`,d,"paper")})}catch{}return g={paperId:e.paperId,paperName:e.paper.name,categoryId:e.categoryId,correct:t,total:n,detail:s},u="results",m=null,j(a)}function j(a){const e=g;if(!e){a.innerHTML='<p>No results to display. <a href="#/papers">Pick a paper.</a></p>';return}const t=Math.round(e.correct/e.total*100),s=t>=80?"Great work":t>=60?"Solid":t>=40?"Keep going":"Review and retry",n=e.detail.map(r=>`
    <li class="paper-review-item ${r.isRight?"review-right":"review-wrong"}">
      <div class="paper-review-head">
        <span class="paper-review-num">Q${r.idx+1}</span>
        <span class="paper-review-status">${r.isRight?"\u2713":"\u2717"}</span>
        <span class="paper-review-source muted">${c(r.kbSourceId)}</span>
      </div>
      <div class="paper-review-stem ja-text" lang="ja">${r.stem_html}</div>
      <ol class="paper-review-choices">
        ${r.choices.map((o,d)=>`<li class="${d===r.correctIndex?"choice-correct":d===r.chosen?"choice-chosen-wrong":""}" lang="ja">${c(o)}</li>`).join("")}
      </ol>
      ${r.rationale?`<p class="paper-review-rationale">${c(r.rationale)}</p>`:""}
    </li>
  `).join("");a.innerHTML=`
    <article class="paper-results">
      <header class="paper-results-summary">
        <h2>${c(e.paperName)} \xB7 Results</h2>
        <div class="paper-score-display">
          <div class="paper-score-big">${e.correct}<span class="paper-score-of">/${e.total}</span></div>
          <div class="paper-score-pct">${t}%</div>
          <div class="paper-score-verdict">${s}</div>
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
  `,document.getElementById("paper-retry")?.addEventListener("click",()=>{u="setup",g=null})}function c(a){return String(a??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{R as renderPapers};
