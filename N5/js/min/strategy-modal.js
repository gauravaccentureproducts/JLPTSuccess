let r=null;const p={mojigoi:["moji_goi","all_sections","all_sections_paper","moji_goi_mondai_1","moji_goi_mondai_2","moji_goi_mondai_3","moji_goi_mondai_4","moji_goi_mondai_5"],bunpoudok:["bunpou_dokkai","all_sections","all_sections_paper","bunpou_mondai_1","bunpou_mondai_2","bunpou_mondai_3","dokkai_mondai_4","dokkai_mondai_5","dokkai_mondai_6"],choukai:["all_sections","all_sections_paper","chokai_mondai_1","chokai_mondai_2","chokai_mondai_3","chokai_mondai_4"]},_={mojigoi:["vocab","kanji"],bunpoudok:["grammar","dokkai"],choukai:["chokai"]};function o(t){return String(t??"").replace(/[&<>"']/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[a])}async function h(){if(r)return r;try{const t=await fetch("data/test_strategy.json");return t.ok?(r=await t.json(),r):null}catch(t){return console.warn("[strategy-modal] load failed:",t),null}}function y(t,a){const n=p[a]||["all_sections"];return(t.techniques||[]).filter(l=>(l.applies_to||[]).some(i=>n.includes(i)))}function k(t,a){const n=_[a]||[];return(t.trap_patterns||[]).filter(l=>n.includes(l.module))}function f(t,a,n){return`
    <header class="strategy-modal-header">
      <h2 id="strategy-modal-title">Strategies for ${o(n)}</h2>
      <button type="button" class="strategy-modal-close" aria-label="Close">&times;</button>
    </header>
    <div class="strategy-modal-body">
      <p class="muted small">
        ${t.length} technique(s) and ${a.length} known trap pattern(s) authored for this section. All content is from <code>data/test_strategy.json</code>.
      </p>
      ${t.length?`
        <section class="strategy-block">
          <h3>Techniques</h3>
          <ul class="strategy-list">
            ${t.map(e=>`
              <li class="strategy-item">
                <div class="strategy-item-head">
                  <strong>${o(e.title_en||e.name||e.id)}</strong>
                  ${e.title_ja?`<span class="muted small" lang="ja">(${o(e.title_ja)})</span>`:""}
                </div>
                <p>${o(e.description||"")}</p>
                ${e.rationale?`<p class="muted small"><em>Why:</em> ${o(e.rationale)}</p>`:""}
                ${e.warning?`<p class="strategy-warning"><strong>\u26A0 Caveat:</strong> ${o(e.warning)}</p>`:""}
              </li>
            `).join("")}
          </ul>
        </section>
      `:""}
      ${a.length?`
        <section class="strategy-block">
          <h3>Trap patterns to watch for</h3>
          <ul class="strategy-list">
            ${a.map(e=>`
              <li class="strategy-item">
                <div class="strategy-item-head">
                  <strong>${o(e.name||e.id)}</strong>
                  <span class="strategy-module-chip muted small">${o(e.module||"")}</span>
                </div>
                <p>${o(e.description||"")}</p>
                ${e.wrong_example?`<p class="wrong" lang="ja"><strong>\u2717</strong> ${o(e.wrong_example)}</p>`:""}
                ${e.correct_example?`<p class="right" lang="ja"><strong>\u2713</strong> ${o(e.correct_example)}</p>`:""}
                ${e.defense?`<p class="muted small"><em>Defense:</em> ${o(e.defense)}</p>`:""}
              </li>
            `).join("")}
          </ul>
        </section>
      `:""}
      ${!t.length&&!a.length?'<p class="muted">No strategies authored for this section yet.</p>':""}
    </div>
  `}async function $(t,a){const n=await h();if(!n){alert("Couldn't load strategy data. Please retry.");return}const e=y(n,t),l=k(n,t),s=document.createElement("div");s.className="strategy-modal-backdrop",s.setAttribute("role","dialog"),s.setAttribute("aria-modal","true"),s.setAttribute("aria-labelledby","strategy-modal-title");const i=document.createElement("div");i.className="strategy-modal-dialog",i.innerHTML=f(e,l,a||t),s.appendChild(i),document.body.appendChild(s);const c=document.activeElement,u=i.querySelector(".strategy-modal-close");u.focus();const d=()=>{s.remove(),document.removeEventListener("keydown",g),c&&c.focus&&c.focus()},g=m=>{m.key==="Escape"&&d()};document.addEventListener("keydown",g),s.addEventListener("click",m=>{m.target===s&&d()}),u.addEventListener("click",d)}export{$ as openStrategyModal};
