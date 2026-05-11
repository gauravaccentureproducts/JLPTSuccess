import*as g from"./storage.js";import{t as h}from"./i18n.js";let $=null;async function k(){return $||($=await(await fetch("data/grammar.json")).json(),$)}async function T(c){const r=await k(),i=(r.patterns||[]).map(p=>p.id),a=new Map((r.patterns||[]).map(p=>[p.id,p])),o=g.getMasteredPatternIds(),e=g.getWeakPatternIds(),t=g.getSeenPatternIds(),s=i.filter(p=>!t.includes(p)),n=g.getResults(),l=n.length,m=n[n.length-1];if(l===0&&t.length===0){c.innerHTML=`
      <h2>${h("page.summary")}</h2>
      <div class="empty-state">
        <p><strong>${h("meta.progress_empty")}</strong></p>
        <p class="muted">${h("meta.progress_empty_help")}</p>
        <p><a href="#/learn" class="btn-primary" style="text-decoration:none">${h("meta.start_lesson")}</a></p>
      </div>
    `;return}c.innerHTML=`
    <h2>${h("page.summary")}</h2>

    <section class="summary-stats">
      <div class="stat-card mastered">
        <div class="stat-num">${o.length}</div>
        <div class="stat-label">${h("meta.mastered")}</div>
        <div class="stat-hint">\u2265 4 consecutive correct</div>
      </div>
      <div class="stat-card weak">
        <div class="stat-num">${e.length}</div>
        <div class="stat-label">${h("meta.need_practice")}</div>
        <div class="stat-hint">\u2265 50% error, \u2265 2 attempts</div>
      </div>
      <div class="stat-card untested">
        <div class="stat-num">${s.length}</div>
        <div class="stat-label">Untested</div>
        <div class="stat-hint">${h("meta.untested")}</div>
      </div>
      <div class="stat-card neutral">
        <div class="stat-num">${l}</div>
        <div class="stat-label">${h("meta.tests_taken")}</div>
        ${m?`<div class="stat-hint">Last: ${M(m.timestamp)}</div>`:'<div class="stat-hint">None yet</div>'}
      </div>
    </section>

    ${S(r.patterns||[],new Set(o),new Set(e),new Set(t))}

    ${I(n,a)}

    ${x(o,e,s,a)}

    ${C(n)}

    ${y("Mastered",o,a,"No mastered patterns yet. 4 consecutive correct in tests/drill graduates a pattern.")}
    ${y("Need practice",e,a,"No weak patterns. Either you have not tested yet, or you are doing well.")}
    ${y("Untested",s,a,"All authored patterns have been tested at least once.")}

    <section class="next-steps">
      <h3>Suggested next step</h3>
      ${R(o,e,s,l)}
    </section>

    <!-- IMP-WAVE-P4-T5/T6 (UI audit, 2026-05-11): cross-history
         weak-area diagnostic + exam-day prep page. Both surface
         test_strategy.json data in actionable form. -->
    <section class="weak-areas-cta" style="margin:24px 0; padding:16px; border:1px solid var(--surface-border); border-radius:var(--radius-md); background:var(--surface-soft, transparent);">
      <h3 style="margin-top:0">Weak-area diagnostic + exam-day prep</h3>
      <p class="muted small">See which of the 9 N5 diagnostic areas you're weakest on, with drill recommendations for each gap. Print the exam-day checklist before test morning.</p>
      <p>
        <a href="#/weakareas" class="btn-secondary" style="text-decoration:none">Open weak-area diagnostic \u2192</a>
        \xB7
        <a href="#/examday" style="margin-left:8px">\u{1F4CB} Exam-day prep \u2192</a>
      </p>
    </section>

    <section class="reset">
      <button id="retake-diagnostic">Re-take Diagnostic</button>
      <button id="reset-progress" class="btn-danger">Reset all progress</button>
      <p class="muted small">Reset clears history, results, weak patterns, and settings. Cannot be undone.</p>
    </section>
  `,document.getElementById("reset-progress")?.addEventListener("click",()=>{confirm("Reset all progress? This clears every test result, the rolling history, and weak-pattern flags.")&&confirm("Are you sure? This cannot be undone.")&&(g.reset(),location.hash="#/learn",location.reload())}),document.getElementById("retake-diagnostic")?.addEventListener("click",()=>{location.hash="#/diagnostic"})}function I(c,r){const i=new Map;for(const e of c)for(const t of e.responses||[]){if(!t.grammarPatternId)continue;const s=i.get(t.grammarPatternId)||{attempts:0,correct:0};s.attempts+=1,t.isCorrect&&(s.correct+=1),i.set(t.grammarPatternId,s)}if(i.size===0)return"";const a=[...i.entries()].map(([e,t])=>({pid:e,attempts:t.attempts,correct:t.correct,accuracy:t.correct/t.attempts,pattern:r.get(e)})).filter(e=>e.attempts>=2).sort((e,t)=>e.accuracy-t.accuracy).slice(0,6);return a.length===0?"":`
    <section class="error-patterns">
      <h3>Error patterns</h3>
      <p class="muted small">Patterns with \u2265 2 attempts, sorted by lowest accuracy. Click to revisit the lesson.</p>
      <ol class="error-list">${a.map(e=>{const t=Math.round(e.accuracy*100),s=e.pattern?.pattern||e.pid,n=e.pattern?.meaning_en||"";return`
      <li class="error-row">
        <div class="error-row-head">
          <a href="#/learn/${encodeURIComponent(e.pid)}"><strong>${d(s)}</strong></a>
          <span class="error-acc">${t}%</span>
        </div>
        <div class="error-row-meta">${e.correct}/${e.attempts} correct \xB7 ${d(n)}</div>
        <div class="error-bar"><div style="width:${t}%; background: ${t<50?"var(--c-error)":t<70?"var(--c-warning)":"var(--c-success)"}"></div></div>
      </li>
    `}).join("")}</ol>
    </section>
  `}function x(c,r,i,a){const o=[];for(const t of r.slice(0,5)){const s=a.get(t);s&&o.push({pid:t,label:s.pattern,why:"Needs practice (\u2265 50% errors)"})}if(o.length<5){const t=5-o.length,s=i.filter(n=>/^n5-0(0[1-9]|1[0-9])$/.test(n)).slice(0,t);for(const n of s){const l=a.get(n);l&&o.push({pid:n,label:l.pattern,why:"Foundational - not yet practiced"})}}return o.length===0?"":`
    <section class="recommendation">
      <h3>Recommended next session</h3>
      <ul class="rec-list">${o.map(t=>`
    <li><a href="#/learn/${encodeURIComponent(t.pid)}"><strong>${d(t.label)}</strong></a> <span class="muted small">- ${d(t.why)}</span></li>
  `).join("")}</ul>
    </section>
  `}function C(c){if(!c||c.length===0)return"";const r=c.slice(-10).reverse(),i=r.map(a=>{const o=a.total>0?Math.round(a.correct/a.total*100):0,e=new Date(a.timestamp).toLocaleString();return`<tr><td>${d(e)}</td><td>${a.total}</td><td>${a.correct}</td><td>${o}%</td></tr>`}).join("");return`
    <section class="session-log">
      <h3>Session log <span class="muted small">(last ${r.length})</span></h3>
      <table class="session-table">
        <thead><tr><th>When</th><th>Length</th><th>Correct</th><th>%</th></tr></thead>
        <tbody>${i}</tbody>
      </table>
    </section>
  `}function S(c,r,i,a){const o=new Map;for(const s of c){const n=s.category||"Other";o.has(n)||o.set(n,{order:s.categoryOrder??99,patterns:[]}),o.get(n).patterns.push(s)}const e=[...o.entries()].sort((s,n)=>s[1].order-n[1].order),t=e.map(([s,{patterns:n}])=>{const l=n.length,m=n.filter(u=>r.has(u.id)).length,p=n.filter(u=>i.has(u.id)).length,w=n.filter(u=>a.has(u.id)).length;let v="untested",f=`${l} pattern${l===1?"":"s"} - none seen yet`;p>0?(v="weak",f=`${p} weak / ${l} total. Review needed.`):m===l&&l>0?(v="mastered",f=`All ${l} mastered.`):w>0&&(v="in-progress",f=`${m} mastered / ${w} seen / ${l} total.`);const b=l>0?Math.round(m/l*100):0;return`
      <div class="heat-cell heat-${v}" title="${d(f)}" data-cat="${d(s)}">
        <div class="heat-cat">${d(s)}</div>
        <div class="heat-meta">
          <span class="heat-count">${m}/${l}</span>
          ${p>0?`<span class="heat-warn">${p} weak</span>`:""}
        </div>
        <div class="heat-bar"><div style="width:${b}%"></div></div>
      </div>
    `}).join("");return`
    <section class="heatmap-section">
      <h3>Category heatmap</h3>
      <p class="muted small">Each cell shows mastered / total for one of the ${e.length} categories. Hover for details.</p>
      <div class="heatmap-grid">${t}</div>
      <div class="heatmap-legend">
        <span><span class="legend-swatch heat-mastered"></span>All mastered</span>
        <span><span class="legend-swatch heat-in-progress"></span>In progress</span>
        <span><span class="legend-swatch heat-weak"></span>Has weak items</span>
        <span><span class="legend-swatch heat-untested"></span>Untested</span>
      </div>
    </section>
  `}function y(c,r,i,a){if(r.length===0)return`<section class="pattern-section"><h3>${d(c)} (0)</h3><p class="muted">${d(a)}</p></section>`;const o=r.map(e=>{const t=i.get(e),s=t?`${t.pattern} - ${t.meaning_en}`:e;return`<li><a href="#/learn/${encodeURIComponent(e)}">${d(s)}</a></li>`}).join("");return`<section class="pattern-section"><h3>${d(c)} (${r.length})</h3><ul>${o}</ul></section>`}function R(c,r,i,a){return a===0?'<p>Take your first test in <a href="#/test">Chapter 2</a>. The system will identify weak patterns automatically and queue them for re-teaching.</p>':r.length>0?`<p><strong>${r.length}</strong> pattern(s) need practice. Open <a href="#/review">Chapter 3 - Review</a> to study them with form rules, common mistakes, and per-distractor explanations.</p>`:i.length>0?`<p>You haven't seen <strong>${i.length}</strong> pattern(s) in any test. Take another test in <a href="#/test">Chapter 2</a> for broader coverage.</p>`:"<p>Strong work - you've covered every authored pattern with no current weaknesses. Keep practicing to graduate them all to mastered.</p>"}function M(c){try{return new Date(c).toLocaleDateString()}catch{return c}}function d(c){return String(c??"").replace(/[&<>"']/g,r=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[r])}export{T as renderSummary};
