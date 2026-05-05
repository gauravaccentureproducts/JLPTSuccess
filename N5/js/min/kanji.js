import*as $ from"./storage.js";let f=null;async function y(){return f||(f=await(await fetch("data/kanji.json")).json(),f)}async function x(n,a){await y();const o=f.entries||[],l=a?decodeURIComponent(a):"";if(!l)return h(n,o);const i=o.find(t=>t.glyph===l);if(!i){n.innerHTML=`
      <div class="placeholder">
        <h2>Kanji not found</h2>
        <p>No N5 entry for <strong lang="ja">${s(l)}</strong>.</p>
        <p><a href="#/kanji" class="btn-primary" style="text-decoration:none">Back to kanji list</a></p>
      </div>
    `;return}return S(n,i,o)}let m="",d="all",g="all",k="lesson";function b(n){return n==null?"":n<=5?"1-5":n<=10?"6-10":n<=15?"11-15":"16+"}function w(n){return n==null?"":n<=30?"1-30":n<=60?"31-60":n<=90?"61-90":"91-106"}function _(n,a,o,l){if(a){const i=n.additional_readings||{};if(![n.glyph||"",...n.on||[],...n.kun||[],...i.on||[],...i.kun||[],...n.meanings||[]].join(" ").toLowerCase().includes(a))return!1}return!(o!=="all"&&b(n.stroke_count)!==o||l!=="all"&&w(n.lesson_order)!==l)}function v(n){switch(k){case"frequency":return n.frequency_rank??999;case"strokes":return n.stroke_count??999;case"glyph":return n.glyph||"";default:return n.lesson_order??999}}function h(n,a){const o=m.trim().toLowerCase(),l=a.filter(e=>_(e,o,d,g)).slice().sort((e,c)=>{const p=v(e),j=v(c);return typeof p=="string"?p.localeCompare(j):p-j}),i=l.map(e=>`
    <a class="kanji-card" href="#/kanji/${encodeURIComponent(e.glyph)}">
      <span class="kanji-card-glyph" lang="ja">${s(e.glyph)}</span>
      ${e.meanings?.length?`<span class="kanji-card-meaning">${s(e.meanings.slice(0,2).join(", "))}</span>`:""}
      <span class="kanji-card-readings" lang="ja">
        ${e.kun?.[0]?s(e.kun[0]):""}${e.on?.[0]?`<br>${s(e.on[0])}`:""}
      </span>
    </a>
  `).join(""),t=(e,c,p,j)=>`<button type="button" class="kanji-chip ${j?"active":""}"
       data-filter-group="${e}" data-filter-value="${c}">${s(p)}</button>`;n.innerHTML=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Kanji</h2>
    <p>${a.length} kanji at JLPT N5 level. Tap any card for readings, meanings, and stroke order.</p>

    <div class="kanji-filters" role="search" aria-label="Filter kanji">
      <input type="search" id="kanji-filter-q" class="kanji-filter-input"
        placeholder="Search reading, meaning, or glyph (e.g. \u307F\u305A / water / \u6C34)"
        value="${s(m)}" autocomplete="off" lang="ja"
        aria-label="Search kanji by reading, meaning, or glyph">

      <div class="kanji-filter-row" aria-label="Stroke count filter">
        <span class="kanji-filter-label">Strokes:</span>
        ${t("stroke","all","All",d==="all")}
        ${t("stroke","1-5","1-5",d==="1-5")}
        ${t("stroke","6-10","6-10",d==="6-10")}
        ${t("stroke","11-15","11-15",d==="11-15")}
        ${t("stroke","16+","16+",d==="16+")}
      </div>

      <div class="kanji-filter-row" aria-label="Lesson order filter">
        <span class="kanji-filter-label">Lesson:</span>
        ${t("lesson","all","All",g==="all")}
        ${t("lesson","1-30","1-30",g==="1-30")}
        ${t("lesson","31-60","31-60",g==="31-60")}
        ${t("lesson","61-90","61-90",g==="61-90")}
        ${t("lesson","91-106","91-106",g==="91-106")}
      </div>

      <div class="kanji-filter-row kanji-sort-row" aria-label="Sort kanji">
        <span class="kanji-filter-label">Sort:</span>
        <select id="kanji-sort" class="kanji-sort-select" aria-label="Sort kanji by">
          <option value="lesson"    ${k==="lesson"?"selected":""}>Lesson order (default)</option>
          <option value="frequency" ${k==="frequency"?"selected":""}>Frequency rank</option>
          <option value="strokes"   ${k==="strokes"?"selected":""}>Stroke count</option>
          <option value="glyph"     ${k==="glyph"?"selected":""}>Glyph (Unicode order)</option>
        </select>
      </div>

      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${l.length}</strong> of ${a.length}.
      </p>
    </div>

    <div class="kanji-card-grid">${i||'<p class="muted">No kanji match the current filters.</p>'}</div>
  `;const u=document.getElementById("kanji-filter-q");u&&u.addEventListener("input",()=>{m=u.value,h(n,a);const e=document.getElementById("kanji-filter-q");if(e){e.focus();const c=e.value;e.setSelectionRange(c.length,c.length)}}),n.querySelectorAll("[data-filter-group]").forEach(e=>{e.addEventListener("click",()=>{const c=e.dataset.filterGroup,p=e.dataset.filterValue;c==="stroke"?d=p:c==="lesson"&&(g=p),h(n,a)})});const r=document.getElementById("kanji-sort");r&&r.addEventListener("change",()=>{k=r.value,h(n,a)})}function S(n,a,o){const l=o.findIndex(r=>r.glyph===a.glyph),i=l>0?o[l-1]:null,t=l<o.length-1?o[l+1]:null,u=$.isKanjiKnown(a.glyph);n.innerHTML=`
    <article class="kanji-detail">
      <div class="srs-progress">
        <a href="#/kanji">\u2190 All kanji</a>
        <span class="muted small">${l+1} of ${o.length}</span>
      </div>
      <div class="kanji-glyph-row pattern-header">
        <div class="kanji-glyph-cluster">
          <div class="kanji-glyph-big" lang="ja">${s(a.glyph)}</div>
          <div class="kanji-readings">
            ${a.on?.length?`<p><strong>On:</strong> <span lang="ja">${a.on.map(s).join(" / ")}</span></p>`:Array.isArray(a.on)?'<p><strong>On:</strong> <span class="muted small">(none at N5)</span></p>':""}
            ${a.kun?.length?`<p><strong>Kun:</strong> <span lang="ja">${a.kun.map(s).join(" / ")}</span></p>`:Array.isArray(a.kun)?'<p><strong>Kun:</strong> <span class="muted small">(none at N5)</span></p>':""}
            ${a.meanings?.length?`<p><strong>Meaning:</strong> ${a.meanings.map(s).join(", ")}</p>`:""}
          </div>
        </div>
        <label class="known-toggle" title="Manually mark this kanji as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-kanji" ${u?"checked":""}>
          <span>Mark as known</span>
        </label>
      </div>
      ${a.examples?.length?`
        <section class="kanji-examples">
          <h3>Example usage (N5)</h3>
          <table class="kanji-examples-table">
            <tbody>
              ${a.examples.map(r=>`
                <tr>
                  <td class="ex-form" lang="ja">${s(r.form)}</td>
                  <td class="ex-reading" lang="ja">${s(r.reading||"")}</td>
                  <td class="ex-gloss">${s(r.gloss||"")}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </section>
      `:""}
      ${a.sentences?.length?`
        <section class="kanji-sentences">
          <h3>In a sentence</h3>
          <ul class="kanji-sentences-list">
            ${a.sentences.map(r=>`
              <li>
                <p class="kanji-sentence-ja" lang="ja">${s(r.ja)}</p>
                ${r.translation_en?`<p class="kanji-sentence-en muted small">${s(r.translation_en)}</p>`:""}
              </li>
            `).join("")}
          </ul>
        </section>
      `:""}
      ${a.stroke_order_svg?`
        <section class="kanji-stroke">
          <h3>Stroke order</h3>
          <object class="stroke-svg" data="${s(a.stroke_order_svg)}" type="image/svg+xml" aria-label="Stroke order for ${s(a.glyph)}">
            <p class="muted small">Stroke-order diagram could not load.</p>
          </object>
          <p class="muted small kanji-stroke-credit">Stroke data: <a href="https://kanjivg.tagaini.net/" rel="noopener noreferrer" target="_blank">KanjiVG</a> (CC BY-SA 3.0).</p>
        </section>
      `:""}
      <nav class="kanji-nav">
        ${i?`<a href="#/kanji/${encodeURIComponent(i.glyph)}">\u2190 <span lang="ja">${s(i.glyph)}</span></a>`:"<span></span>"}
        ${t?`<a href="#/kanji/${encodeURIComponent(t.glyph)}"><span lang="ja">${s(t.glyph)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-kanji")?.addEventListener("change",r=>{$.setKanjiKnown(a.glyph,r.target.checked)})}function s(n){return String(n??"").replace(/[&<>"']/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[a])}export{x as renderKanji};
