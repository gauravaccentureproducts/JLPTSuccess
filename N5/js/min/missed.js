import*as l from"./storage.js";let c=null;async function p(){if(c)return;const e=await fetch("data/grammar.json");if(!e.ok)return;const t=await e.json();c=new Map((t.patterns||[]).map(s=>[s.id,s]))}function w(e){if(!e)return"";const t=new Date(e);if(isNaN(t.getTime()))return"";const s=new Date;if(t.toDateString()===s.toDateString())return t.toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"});const a=new Date;return a.setDate(a.getDate()-1),t.toDateString()===a.toDateString()?"Yesterday "+t.toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"}):t.toLocaleDateString()}function m(e){return e==null?'<em class="muted">(no answer)</em>':Array.isArray(e)?r(e.join(" / ")):r(String(e))}function r(e){return String(e??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}async function f(e){await p();const t=l.getWrongHistory?l.getWrongHistory():[];if(!t.length){e.innerHTML=`
      <article class="missed-page">
        <a class="back-link" href="#/review">\u2190 Back to Review</a>
        <h2>Wrong-answer history</h2>
        <div class="placeholder">
          <p>You haven't missed anything recently - keep practising. Wrong answers from Test and Drill flow into this list automatically (most recent 200).</p>
        </div>
      </article>
    `;return}const s=new Map;for(const a of t){const i=new Date(a.ts).toDateString();s.has(i)||s.set(i,[]),s.get(i).push(a)}let o="";for(const[a,i]of s){const g=i.map(n=>{const d=c?.get(n.patternId),u=d?d.pattern:n.patternId||"(unknown pattern)";return`
        <li class="missed-row">
          <div class="missed-row-meta">
            <span class="missed-row-time muted small">${r(w(n.ts))}</span>
            <span class="missed-row-source muted small">${r(n.source||"test")}</span>
          </div>
          <div class="missed-row-pattern">
            <a href="#/learn/${encodeURIComponent(n.patternId||"")}" lang="ja">${r(u)}</a>
          </div>
          <div class="missed-row-answers">
            <p><strong class="muted small">You:</strong> <span class="missed-wrong" lang="ja">${m(n.wrongAnswer)}</span></p>
            <p><strong class="muted small">Correct:</strong> <span class="missed-right" lang="ja">${m(n.correctAnswer)}</span></p>
          </div>
        </li>
      `}).join("");o+=`
      <section class="missed-day-group">
        <header class="section-label">
          <span class="section-label-text">${r(a)}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ul class="missed-list">${g}</ul>
      </section>
    `}e.innerHTML=`
    <article class="missed-page">
      <a class="back-link" href="#/review">\u2190 Back to Review</a>
      <h2>Wrong-answer history</h2>
      <p class="page-lede">
        Most recent ${t.length} miss${t.length===1?"":"es"}
        from Test and Drill (capped at 200). Newest first.
      </p>
      ${o}
      <div class="missed-actions">
        <button id="missed-clear" class="btn-danger">Clear history</button>
      </div>
    </article>
  `,document.getElementById("missed-clear")?.addEventListener("click",()=>{confirm("Clear the wrong-answer history? FSRS schedule and test results stay intact.")&&(l.clearWrongHistory(),f(e))})}export{f as renderMissed};
