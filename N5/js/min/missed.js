import*as c from"./storage.js";import{t as a}from"./i18n.js";let m=null;async function w(){if(m)return;const e=await fetch("data/grammar.json");if(!e.ok)return;const s=await e.json();m=new Map((s.patterns||[]).map(n=>[n.id,n]))}function f(e){if(!e)return"";const s=new Date(e);if(isNaN(s.getTime()))return"";const n=new Date;if(s.toDateString()===n.toDateString())return s.toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"});const r=new Date;return r.setDate(r.getDate()-1),s.toDateString()===r.toDateString()?a("meta.yesterday")+" "+s.toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"}):s.toLocaleDateString()}function g(e){return e==null?'<em class="muted">(no answer)</em>':Array.isArray(e)?t(e.join(" / ")):t(String(e))}function t(e){return String(e??"").replace(/[&<>"']/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[s])}async function h(e){await w();const s=c.getWrongHistory?c.getWrongHistory():[];if(!s.length){e.innerHTML=`
      <article class="missed-page">
        <a class="back-link" href="#/review">\u2190 ${t(a("meta.back_to_review"))}</a>
        <h2>${t(a("meta.wrong_answer_history"))}</h2>
        <div class="placeholder">
          <p>${t(a("meta.no_misses"))}</p>
        </div>
      </article>
    `;return}const n=new Map;for(const r of s){const o=new Date(r.ts).toDateString();n.has(o)||n.set(o,[]),n.get(o).push(r)}let l="";for(const[r,o]of n){const p=o.map(i=>{const d=m?.get(i.patternId),u=d?d.pattern:i.patternId||"(unknown pattern)";return`
        <li class="missed-row">
          <div class="missed-row-meta">
            <span class="missed-row-time muted small">${t(f(i.ts))}</span>
            <span class="missed-row-source muted small">${t(i.source||"test")}</span>
          </div>
          <div class="missed-row-pattern">
            <a href="#/learn/${encodeURIComponent(i.patternId||"")}" lang="ja">${t(u)}</a>
          </div>
          <div class="missed-row-answers">
            <p><strong class="muted small">${t(a("meta.you_label"))}:</strong> <span class="missed-wrong" lang="ja">${g(i.wrongAnswer)}</span></p>
            <p><strong class="muted small">${t(a("meta.correct_label"))}:</strong> <span class="missed-right" lang="ja">${g(i.correctAnswer)}</span></p>
          </div>
        </li>
      `}).join("");l+=`
      <section class="missed-day-group">
        <header class="section-label">
          <span class="section-label-text">${t(r)}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ul class="missed-list">${p}</ul>
      </section>
    `}e.innerHTML=`
    <article class="missed-page">
      <a class="back-link" href="#/review">\u2190 ${t(a("meta.back_to_review"))}</a>
      <h2>${t(a("meta.wrong_answer_history"))}</h2>
      <p class="page-lede">
        ${t(a("meta.most_recent_misses").replace("${n}",s.length))}
      </p>
      ${l}
      <div class="missed-actions">
        <button id="missed-clear" class="btn-danger">${t(a("meta.clear_history"))}</button>
      </div>
    </article>
  `,document.getElementById("missed-clear")?.addEventListener("click",()=>{confirm(a("meta.clear_confirm"))&&(c.clearWrongHistory(),h(e))})}export{h as renderMissed};
