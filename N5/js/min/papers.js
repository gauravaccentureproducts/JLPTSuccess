import"./furigana.js";import*as x from"./storage.js";let h=null;const $=new Map;let d=null,u="setup",m=null;async function b(){if(h)return h;const s=await fetch("data/papers/manifest.json");if(!s.ok)throw new Error(`Failed to load papers manifest: ${s.status}`);return h=await s.json(),h}async function k(s,e){const t=`${s}-${e}`;if($.has(t))return $.get(t);const a=await fetch(`data/papers/${s}/paper-${e}.json`);if(!a.ok)throw new Error(`Failed to load paper ${t}: ${a.status}`);const p=await a.json();return $.set(t,p),p}function w(s){return`jlpt-n5-tutor.paper.${s}`}function f(s){try{const e=localStorage.getItem(w(s));return e?JSON.parse(e):{attempts:0,bestScore:null,lastScore:null}}catch{return{attempts:0,bestScore:null,lastScore:null}}}function S(s,e,t){const a=f(s),p={attempts:(a.attempts||0)+1,bestScore:a.bestScore==null?{correct:e,total:t}:e>a.bestScore.correct?{correct:e,total:t}:a.bestScore,lastScore:{correct:e,total:t,dateIso:new Date().toISOString()}};return localStorage.setItem(w(s),JSON.stringify(p)),p}async function _(s,e){const t=(e||"").split("/").filter(Boolean);if(t.length<2&&(u==="attempting"||u==="results")&&(u="setup",d=null,m=null),u==="attempting"&&d)return g(s);if(u==="results"&&m)return I(s);if(t.length===0)return y(s);if(t.length===1)return q(s,t[0]);if(t.length===2){const[a,p]=t;return P(s,a,parseInt(p,10))}return y(s)}async function y(s){const e=await b(),t=e.categories.map(a=>{const p=a.papers.filter(r=>(f(r.id).attempts||0)>0).length;return`
      <a class="paper-cat-card" href="#/papers/${c(a.id)}">
        <div class="paper-cat-icon" aria-hidden="true">${j(a.id)}</div>
        <div class="paper-cat-meta">
          <h3>${c(a.label)} <span class="paper-cat-ja" lang="ja">${c(a.label_ja)}</span></h3>
          <p class="paper-cat-desc">${c(a.description)}</p>
          <p class="paper-cat-stats">
            <span class="paper-stat">${a.paperCount} papers</span>
            <span class="paper-stat-sep">\xB7</span>
            <span class="paper-stat">${a.questionCount} questions</span>
            <span class="paper-stat-sep">\xB7</span>
            <span class="paper-stat">${p} of ${a.paperCount} attempted</span>
          </p>
        </div>
      </a>
    `}).join("");s.innerHTML=`
    <article class="papers-index">
      <a class="back-link" href="#/test">\u2190 Back to Test</a>
      <h2>Mock-test Papers</h2>
      <p class="page-lede">${e.totalQuestions} audited JLPT N5 questions across ${e.totalPapers} papers in 4 sections. Each paper is sized to a study-session (15 questions, ~10 minutes). Scores persist locally so you can track which papers you've completed.</p>
      <div class="paper-cat-grid">${t}</div>
      <p class="papers-foot-note">Source: <code>KnowledgeBank/{moji,goi,bunpou,dokkai}_questions_n5.md</code> - curated and native-teacher-reviewed across Pass-9 through Pass-19.</p>
    </article>
  `}function j(s){return`<span class="paper-cat-letter" lang="ja">${{moji:"\u5B57",goi:"\u8A9E",bunpou:"\u6CD5",dokkai:"\u8AAD"}[s]||"?"}</span>`}async function q(s,e){const a=(await b()).categories.find(r=>r.id===e);if(!a){s.innerHTML=`
      <article class="papers-index">
        <a class="back-link" href="#/papers">\u2190 Back to Mock-test Papers</a>
        <h2>Unknown category</h2>
        <p>The category <code>${c(e)}</code> doesn't exist. <a href="#/papers">Return to the index.</a></p>
      </article>
    `;return}const p=a.papers.map(r=>{const o=f(r.id),l=(o.attempts||0)>0,n=o.bestScore,i=l?`<span class="paper-badge paper-badge-done">${n?`${n.correct}/${n.total}`:"Done"}</span>`:'<span class="paper-badge paper-badge-new">New</span>';return`
      <a class="paper-card" href="#/papers/${c(a.id)}/${r.paperNumber}">
        <div class="paper-card-num">Paper ${r.paperNumber}</div>
        <div class="paper-card-meta">
          <span class="paper-q-count">${r.questionCount} questions</span>
          <span class="paper-source-range muted">${c(r.source_question_range)}</span>
        </div>
        ${i}
      </a>
    `}).join("");s.innerHTML=`
    <article class="papers-index">
      <a class="back-link" href="#/papers">\u2190 All sections</a>
      <h2>${c(a.label)} <span class="paper-cat-ja" lang="ja">${c(a.label_ja)}</span></h2>
      <p class="page-lede">${c(a.description)} \xB7 ${a.paperCount} papers \xB7 ${a.questionCount} questions total.</p>
      <div class="paper-list-grid">${p}</div>
    </article>
  `}async function P(s,e,t){if(!Number.isInteger(t)||t<1){s.innerHTML="<p>Invalid paper number.</p>";return}const a=await k(e,t);return d={paper:a,paperId:a.id,categoryId:e,paperNumber:t,questions:a.questions,answers:new Array(a.questions.length).fill(null),currentIdx:0,submitted:!1},u="attempting",g(s)}function g(s){const e=d;if(!e){s.innerHTML='<p>No active session. <a href="#/papers">Pick a paper.</a></p>';return}const t=e.questions[e.currentIdx],a=e.questions.length,p=e.answers.filter(n=>n!==null).length,r=t.passage_text?`<div class="paper-passage" lang="ja">${v(t.passage_text)}</div>`:"",o=t.choices.map((n,i)=>`
    <label class="paper-choice ${e.answers[e.currentIdx]===i?"selected":""}">
      <input type="radio" name="choice" value="${i}" ${e.answers[e.currentIdx]===i?"checked":""}>
      <span class="paper-choice-letter">${i+1}</span>
      <span class="paper-choice-text" lang="ja">${v(n)}</span>
    </label>
  `).join("");s.innerHTML=`
    <article class="paper-attempting">
      <header class="paper-progress-bar">
        <a class="paper-quit" href="#/papers/${c(e.categoryId)}" title="Quit and return to paper list">\u2715 Quit</a>
        <div class="paper-progress-info">
          <span class="paper-progress-current">Q${e.currentIdx+1}</span>
          <span class="paper-progress-of">of ${a}</span>
          <span class="paper-progress-answered">\xB7 ${p} answered</span>
        </div>
      </header>
      ${r}
      <div class="paper-question-stem" lang="ja">${v(t.stem_html)}</div>
      <form class="paper-choices" id="paper-choices-form">${o}</form>
      <footer class="paper-controls">
        <button type="button" class="btn-secondary" id="paper-prev" ${e.currentIdx===0?"disabled":""}>\u2190 Previous</button>
        ${e.currentIdx===a-1?(()=>{const n=a-p,i=n===0;return`
                <div class="paper-submit-cluster">
                  ${i?"":`<p class="paper-submit-hint">Answer all ${a} questions to submit \xB7 <strong>${n}</strong> ${n===1?"question":"questions"} unanswered</p>`}
                  <button type="button" class="btn-primary" id="paper-submit" ${i?"":"disabled"} title="${i?"Submit your paper":`Answer all questions to submit (${n} remaining)`}">${i?"Submit paper":`Submit paper (${n} remaining)`}</button>
                </div>`})():'<button type="button" class="btn-primary" id="paper-next">Next \u2192</button>'}
      </footer>
    </article>
  `,document.getElementById("paper-choices-form").addEventListener("change",n=>{n.target&&n.target.name==="choice"&&(e.answers[e.currentIdx]=parseInt(n.target.value,10),g(s))}),document.getElementById("paper-prev")?.addEventListener("click",()=>{e.currentIdx>0&&(e.currentIdx-=1,g(s))}),document.getElementById("paper-next")?.addEventListener("click",()=>{e.currentIdx<a-1&&(e.currentIdx+=1,g(s))}),document.getElementById("paper-submit")?.addEventListener("click",()=>{L(s)})}function v(s){return s?`<span class="ja-text" lang="ja">${s}</span>`:""}function L(s){const e=d;let t=0;const a=e.questions.map((r,o)=>{const l=e.answers[o],n=l===r.correctIndex;return n&&(t+=1),{idx:o,kbSourceId:r.kbSourceId,stem_html:r.stem_html,choices:r.choices,correctIndex:r.correctIndex,chosen:l,isRight:n,rationale:r.rationale||""}}),p=e.questions.length;S(e.paperId,t,p);try{e.questions.forEach((r,o)=>{const l=e.answers[o]===r.correctIndex;x.recordAttempt?.(`paper:${e.categoryId}:${r.kbSourceId}`,l,"paper")})}catch{}return m={paperId:e.paperId,paperName:e.paper.name,categoryId:e.categoryId,correct:t,total:p,detail:a},u="results",d=null,I(s)}function I(s){const e=m;if(!e){s.innerHTML='<p>No results to display. <a href="#/papers">Pick a paper.</a></p>';return}const t=Math.round(e.correct/e.total*100),a=t>=80?"Great work":t>=60?"Solid":t>=40?"Keep going":"Review and retry",p=e.detail.map(r=>`
    <li class="paper-review-item ${r.isRight?"review-right":"review-wrong"}">
      <div class="paper-review-head">
        <span class="paper-review-num">Q${r.idx+1}</span>
        <span class="paper-review-status">${r.isRight?"\u2713":"\u2717"}</span>
        <span class="paper-review-source muted">${c(r.kbSourceId)}</span>
      </div>
      <div class="paper-review-stem ja-text" lang="ja">${r.stem_html}</div>
      <ol class="paper-review-choices">
        ${r.choices.map((o,l)=>`<li class="${l===r.correctIndex?"choice-correct":l===r.chosen?"choice-chosen-wrong":""}" lang="ja">${c(o)}</li>`).join("")}
      </ol>
      ${r.rationale?`<p class="paper-review-rationale">${c(r.rationale)}</p>`:""}
    </li>
  `).join("");s.innerHTML=`
    <article class="paper-results">
      <header class="paper-results-summary">
        <h2>${c(e.paperName)} \xB7 Results</h2>
        <div class="paper-score-display">
          <div class="paper-score-big">${e.correct}<span class="paper-score-of">/${e.total}</span></div>
          <div class="paper-score-pct">${t}%</div>
          <div class="paper-score-verdict">${a}</div>
        </div>
      </header>
      <nav class="paper-results-actions">
        <a class="btn-primary" href="#/papers/${c(e.categoryId)}">Back to ${c(e.categoryId)} papers</a>
        <a class="btn-secondary" href="#/papers/${c(e.categoryId)}/${parseInt(e.paperId.split("-")[1],10)}" id="paper-retry">Retry this paper</a>
      </nav>
      <section class="paper-review">
        <h3>Question review</h3>
        <ol class="paper-review-list">${p}</ol>
      </section>
    </article>
  `,document.getElementById("paper-retry")?.addEventListener("click",()=>{u="setup",m=null})}function c(s){return String(s??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{_ as renderPapers};
