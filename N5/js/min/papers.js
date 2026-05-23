import"./furigana.js";import*as x from"./storage.js";let b=null;const y=new Map;let f=null,m="setup",h=null;const _={moji:11,goi:11,bunpou:23,dokkai:23};let d=null,$=null;async function S(){if(b)return b;const t=await fetch("data/papers/manifest.json");if(!t.ok)throw new Error(`Failed to load papers manifest: ${t.status}`);return b=await t.json(),b}async function E(t,e){const a=`${t}-${e}`;if(y.has(a))return y.get(a);const s=await fetch(`data/papers/${t}/paper-${e}.json`);if(!s.ok)throw new Error(`Failed to load paper ${a}: ${s.status}`);const p=await s.json();return y.set(a,p),p}function j(t){return`jlpt-n5-tutor.paper.${t}`}function k(t){try{const e=localStorage.getItem(j(t));return e?JSON.parse(e):{attempts:0,bestScore:null,lastScore:null}}catch{return{attempts:0,bestScore:null,lastScore:null}}}function L(t,e,a){const s=k(t),p={attempts:(s.attempts||0)+1,bestScore:s.bestScore==null?{correct:e,total:a}:e>s.bestScore.correct?{correct:e,total:a}:s.bestScore,lastScore:{correct:e,total:a,dateIso:new Date().toISOString()}};return localStorage.setItem(j(t),JSON.stringify(p)),p}async function D(t,e){const a=(e||"").split("/").filter(Boolean);if(a.length<2&&(m==="attempting"||m==="results")&&(m="setup",f=null,h=null),m==="attempting"&&f)return v(t);if(m==="results"&&h)return P(t);if(a.length===0)return M(t);if(a.length===1)return B(t,a[0]);if(a.length===2){const[s,p]=a;return A(t,s,parseInt(p,10))}return M(t)}async function M(t){const e=await S(),a=e.categories.map(s=>{const p=s.papers.filter(r=>(k(r.id).attempts||0)>0).length;return`
      <a class="paper-cat-card" href="#/papers/${c(s.id)}">
        <div class="paper-cat-icon" aria-hidden="true">${T(s.id)}</div>
        <div class="paper-cat-meta">
          <h3>${c(s.label)} <span class="paper-cat-ja" lang="ja">${c(s.label_ja)}</span></h3>
          <p class="paper-cat-desc">${c(s.description)}</p>
          <p class="paper-cat-stats">
            <span class="paper-stat">${s.paperCount} papers</span>
            <span class="paper-stat-sep">\xB7</span>
            <span class="paper-stat">${s.questionCount} questions</span>
            <span class="paper-stat-sep">\xB7</span>
            <span class="paper-stat">${p} of ${s.paperCount} attempted</span>
          </p>
        </div>
      </a>
    `}).join("");t.innerHTML=`
    <article class="papers-index">
      <a class="back-link" href="#/test">\u2190 Back to Test</a>
      <h2>Mock-test Papers</h2>
      <p class="page-lede">${e.totalQuestions} audited JLPT N5 questions across ${e.totalPapers} papers in 4 sections. Each paper is sized to a study-session (15 questions, ~10 minutes). Scores persist locally so you can track which papers you've completed.</p>
      <div class="paper-cat-grid">${a}</div>
      <p class="papers-foot-note">Source: <code>KnowledgeBank/{moji,goi,bunpou,dokkai}_questions_n5.md</code> - curated and native-teacher-reviewed across Pass-9 through Pass-19.</p>
    </article>
  `}function T(t){return`<span class="paper-cat-letter" lang="ja">${{moji:"\u5B57",goi:"\u8A9E",bunpou:"\u6CD5",dokkai:"\u8AAD"}[t]||"?"}</span>`}async function B(t,e){const s=(await S()).categories.find(r=>r.id===e);if(!s){t.innerHTML=`
      <article class="papers-index">
        <a class="back-link" href="#/papers">\u2190 Back to Mock-test Papers</a>
        <h2>Unknown category</h2>
        <p>The category <code>${c(e)}</code> doesn't exist. <a href="#/papers">Return to the index.</a></p>
      </article>
    `;return}const p=s.papers.map(r=>{const o=k(r.id),l=(o.attempts||0)>0,n=o.bestScore,i=l?`<span class="paper-badge paper-badge-done">${n?`${n.correct}/${n.total}`:"Done"}</span>`:'<span class="paper-badge paper-badge-new">New</span>';return`
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
    `}).join("");t.innerHTML=`
    <article class="papers-index">
      <a class="back-link" href="#/papers">\u2190 All sections</a>
      <h2>${c(s.label)} <span class="paper-cat-ja" lang="ja">${c(s.label_ja)}</span></h2>
      <p class="page-lede">${c(s.description)} \xB7 ${s.paperCount} papers \xB7 ${s.questionCount} questions total. <a class="muted small" href="#/print">Print any paper \u2192</a></p>
      <div class="paper-list-grid">${p}</div>
    </article>
  `}async function A(t,e,a){if(!Number.isInteger(a)||a<1){t.innerHTML="<p>Invalid paper number.</p>";return}const s=await E(e,a),p=!!x.getSettings().examMode,r=_[e]||15;return f={paper:s,paperId:s.id,categoryId:e,paperNumber:a,questions:s.questions,answers:new Array(s.questions.length).fill(null),currentIdx:0,submitted:!1,examMode:p,durationSec:p?r*60:null},p?($=Date.now()+r*60*1e3,d&&clearInterval(d),d=setInterval(()=>N(t),1e3)):($=null,d&&(clearInterval(d),d=null)),m="attempting",v(t)}function N(t){if(!f||!$)return;const e=$-Date.now(),a=document.getElementById("paper-timer");if(!a)return;if(e<=0){d&&clearInterval(d),d=null,a.textContent="00:00",a.classList.add("timer-expired"),q(t);return}const s=Math.floor(e/6e4),p=Math.floor(e%6e4/1e3);a.textContent=`${String(s).padStart(2,"0")}:${String(p).padStart(2,"0")}`,e<6e4&&a.classList.add("timer-low")}function v(t){const e=f;if(!e){t.innerHTML='<p>No active session. <a href="#/papers">Pick a paper.</a></p>';return}const a=e.questions[e.currentIdx],s=e.questions.length,p=e.answers.filter(n=>n!==null).length;let r="";if(a.passage_label&&Array.isArray(e.paper?.passages)){const n=e.paper.passages.find(i=>i&&i.label===a.passage_label);n&&n.text&&(r=n.text.includes("> ")||n.text.includes("|---|")?`<div class="paper-passage" lang="ja">${C(n.text)}</div>`:`<div class="paper-passage" lang="ja">${w(n.text)}</div>`)}else a.passage_text&&(r=`<div class="paper-passage" lang="ja">${w(a.passage_text)}</div>`);const o=a.choices.map((n,i)=>`
    <label class="paper-choice ${e.answers[e.currentIdx]===i?"selected":""}">
      <input type="radio" name="choice" value="${i}" ${e.answers[e.currentIdx]===i?"checked":""}>
      <span class="paper-choice-letter">${i+1}</span>
      <span class="paper-choice-text" lang="ja">${w(n)}</span>
    </label>
  `).join("");t.innerHTML=`
    <article class="paper-attempting">
      <header class="paper-progress-bar">
        <a class="paper-quit" href="#/papers/${c(e.categoryId)}" title="Quit and return to paper list">\u2715 Quit</a>
        <div class="paper-progress-info">
          <span class="paper-progress-current">Q${e.currentIdx+1}</span>
          <span class="paper-progress-of">of ${s}</span>
          <span class="paper-progress-answered">\xB7 ${p} answered</span>
          ${e.examMode?`<span class="paper-timer-wrap">\xB7 <span id="paper-timer" class="paper-timer">${R(e.durationSec*1e3)}</span></span>`:""}
        </div>
      </header>
      ${r}
      <div class="paper-question-stem" lang="ja">${w(a.stem_html)}</div>
      <form class="paper-choices" id="paper-choices-form">${o}</form>
      <footer class="paper-controls">
        <button type="button" class="btn-secondary" id="paper-prev" ${e.currentIdx===0?"disabled":""}>\u2190 Previous</button>
        ${e.currentIdx===s-1?(()=>{const n=s-p,i=n===0;return`
                <div class="paper-submit-cluster">
                  ${i?"":`<p class="paper-submit-hint">Answer all ${s} questions to submit \xB7 <strong>${n}</strong> ${n===1?"question":"questions"} unanswered</p>`}
                  <button type="button" class="btn-primary" id="paper-submit" ${i?"":"disabled"} title="${i?"Submit your paper":`Answer all questions to submit (${n} remaining)`}">${i?"Submit paper":`Submit paper (${n} remaining)`}</button>
                </div>`})():'<button type="button" class="btn-primary" id="paper-next">Next \u2192</button>'}
      </footer>
    </article>
  `,document.getElementById("paper-choices-form").addEventListener("change",n=>{n.target&&n.target.name==="choice"&&(e.answers[e.currentIdx]=parseInt(n.target.value,10),v(t))}),document.getElementById("paper-prev")?.addEventListener("click",()=>{e.currentIdx>0&&(e.currentIdx-=1,v(t))}),document.getElementById("paper-next")?.addEventListener("click",()=>{e.currentIdx<s-1&&(e.currentIdx+=1,v(t))}),document.getElementById("paper-submit")?.addEventListener("click",()=>{q(t)})}function R(t){t<0&&(t=0);const e=Math.floor(t/6e4),a=Math.floor(t%6e4/1e3);return`${String(e).padStart(2,"0")}:${String(a).padStart(2,"0")}`}function w(t){return t?`<span class="ja-text" lang="ja">${t}</span>`:""}function C(t){if(!t)return"";const e=t.split(`
`),a=[];let s=!1,p=!1,r=[];function o(){if(r.length===0)return;const n=r[0],i=r.slice(2);let u='<table class="paper-passage-table"><thead><tr>';for(const g of n)u+=`<th lang="ja">${g}</th>`;u+="</tr></thead><tbody>";for(const g of i){u+="<tr>";for(const I of g)u+=`<td lang="ja">${I}</td>`;u+="</tr>"}u+="</tbody></table>",a.push(u),r=[],s=!1}for(let n of e){let i=n;if(i.startsWith("> ")||i===">")p=!0,i=i.replace(/^> ?/,"");else if(i.trim()===""){s&&o(),a.length&&!a[a.length-1].endsWith("<br>")&&a.push("<br>");continue}const u=i.match(/^\|(.*)\|$/);if(u){const g=u[1].split("|").map(I=>I.trim());s=!0,r.push(g);continue}s&&o(),i.trim()&&a.push(`<div class="paper-passage-line" lang="ja">${i}</div>`)}s&&o();const l=a.join(`
`);return p?`<blockquote class="paper-passage-blockquote">${l}</blockquote>`:l}function q(t){const e=f;d&&(clearInterval(d),d=null),$=null;let a=0;const s=e.questions.map((r,o)=>{const l=e.answers[o],n=l===r.correctIndex;return n&&(a+=1),{idx:o,kbSourceId:r.kbSourceId,stem_html:r.stem_html,choices:r.choices,correctIndex:r.correctIndex,chosen:l,isRight:n,rationale:r.rationale||""}}),p=e.questions.length;L(e.paperId,a,p);try{e.questions.forEach((r,o)=>{const l=e.answers[o]===r.correctIndex;x.recordAttempt?.(`paper:${e.categoryId}:${r.kbSourceId}`,l,"paper")})}catch{}return h={paperId:e.paperId,paperName:e.paper.name,categoryId:e.categoryId,correct:a,total:p,detail:s},m="results",f=null,P(t)}function P(t){const e=h;if(!e){t.innerHTML='<p>No results to display. <a href="#/papers">Pick a paper.</a></p>';return}const a=Math.round(e.correct/e.total*100),s=a>=80?"Great work":a>=60?"Solid":a>=40?"Keep going":"Review and retry",p=e.detail.map(r=>`
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
  `).join("");t.innerHTML=`
    <article class="paper-results">
      <header class="paper-results-summary">
        <h2>${c(e.paperName)} \xB7 Results</h2>
        <div class="paper-score-display">
          <div class="paper-score-big">${e.correct}<span class="paper-score-of">/${e.total}</span></div>
          <div class="paper-score-pct">${a}%</div>
          <div class="paper-score-verdict">${s}</div>
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
  `,document.getElementById("paper-retry")?.addEventListener("click",()=>{m="setup",h=null})}function c(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{D as renderPapers};
