import*as $ from"./storage.js";import{currentLocale as y}from"./i18n.js";function b(n){const a=y();if(a&&a!=="en"){const t=n[`meanings_${a}`];if(Array.isArray(t)&&t.length)return t}return n.meanings||[]}let f=null;async function w(){return f||(f=await(await fetch("data/kanji.json")).json(),f)}async function K(n,a){await w();const t=f.entries||[],o=a?decodeURIComponent(a):"";if(!o)return h(n,t);const i=t.find(r=>r.glyph===o);if(!i){n.innerHTML=`
      <div class="placeholder">
        <h2>Kanji not found</h2>
        <p>No N5 entry for <strong lang="ja">${s(o)}</strong>.</p>
        <p><a href="#/kanji" class="btn-primary" style="text-decoration:none">Back to kanji list</a></p>
      </div>
    `;return}return L(n,i,t)}let m="",d="all",g="all",u="lesson";function _(n){return n==null?"":n<=5?"1-5":n<=10?"6-10":n<=15?"11-15":"16+"}function S(n){return n==null?"":n<=30?"1-30":n<=60?"31-60":n<=90?"61-90":"91-106"}function x(n,a,t,o){if(a){const i=n.additional_readings||{};if(![n.glyph||"",...n.on||[],...n.kun||[],...i.on||[],...i.kun||[],...n.meanings||[]].join(" ").toLowerCase().includes(a))return!1}return!(t!=="all"&&_(n.stroke_count)!==t||o!=="all"&&S(n.lesson_order)!==o)}function v(n){switch(u){case"frequency":return n.frequency_rank??999;case"strokes":return n.stroke_count??999;case"glyph":return n.glyph||"";default:return n.lesson_order??999}}function h(n,a){const t=m.trim().toLowerCase(),o=a.filter(e=>x(e,t,d,g)).slice().sort((e,c)=>{const p=v(e),j=v(c);return typeof p=="string"?p.localeCompare(j):p-j}),i=o.map(e=>`
    <a class="kanji-card" href="#/kanji/${encodeURIComponent(e.glyph)}">
      <span class="kanji-card-glyph" lang="ja">${s(e.glyph)}</span>
      ${e.meanings?.length?`<span class="kanji-card-meaning">${s(e.meanings.slice(0,2).join(", "))}</span>`:""}
      <span class="kanji-card-readings" lang="ja">
        ${e.kun?.[0]?s(e.kun[0]):""}${e.on?.[0]?`<br>${s(e.on[0])}`:""}
      </span>
    </a>
  `).join(""),r=(e,c,p,j)=>`<button type="button" class="kanji-chip ${j?"active":""}"
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
        ${r("stroke","all","All",d==="all")}
        ${r("stroke","1-5","1-5",d==="1-5")}
        ${r("stroke","6-10","6-10",d==="6-10")}
        ${r("stroke","11-15","11-15",d==="11-15")}
        ${r("stroke","16+","16+",d==="16+")}
      </div>

      <div class="kanji-filter-row" aria-label="Lesson order filter">
        <span class="kanji-filter-label">Lesson:</span>
        ${r("lesson","all","All",g==="all")}
        ${r("lesson","1-30","1-30",g==="1-30")}
        ${r("lesson","31-60","31-60",g==="31-60")}
        ${r("lesson","61-90","61-90",g==="61-90")}
        ${r("lesson","91-106","91-106",g==="91-106")}
      </div>

      <div class="kanji-filter-row kanji-sort-row" aria-label="Sort kanji">
        <span class="kanji-filter-label">Sort:</span>
        <select id="kanji-sort" class="kanji-sort-select" aria-label="Sort kanji by">
          <option value="lesson"    ${u==="lesson"?"selected":""}>Lesson order (default)</option>
          <option value="frequency" ${u==="frequency"?"selected":""}>Frequency rank</option>
          <option value="strokes"   ${u==="strokes"?"selected":""}>Stroke count</option>
          <option value="glyph"     ${u==="glyph"?"selected":""}>Glyph (Unicode order)</option>
        </select>
      </div>

      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${o.length}</strong> of ${a.length}.
      </p>
    </div>

    <div class="kanji-card-grid">${i||'<p class="muted">No kanji match the current filters.</p>'}</div>
  `;const k=document.getElementById("kanji-filter-q");k&&k.addEventListener("input",()=>{m=k.value,h(n,a);const e=document.getElementById("kanji-filter-q");if(e){e.focus();const c=e.value;e.setSelectionRange(c.length,c.length)}}),n.querySelectorAll("[data-filter-group]").forEach(e=>{e.addEventListener("click",()=>{const c=e.dataset.filterGroup,p=e.dataset.filterValue;c==="stroke"?d=p:c==="lesson"&&(g=p),h(n,a)})});const l=document.getElementById("kanji-sort");l&&l.addEventListener("change",()=>{u=l.value,h(n,a)})}function L(n,a,t){const o=t.findIndex(l=>l.glyph===a.glyph),i=o>0?t[o-1]:null,r=o<t.length-1?t[o+1]:null,k=$.isKanjiKnown(a.glyph);n.innerHTML=`
    <article class="kanji-detail">
      <div class="srs-progress">
        <a href="#/kanji">\u2190 All kanji</a>
        <span class="muted small">${o+1} of ${t.length}</span>
      </div>
      <div class="kanji-glyph-row pattern-header">
        <div class="kanji-glyph-cluster">
          <div class="kanji-glyph-big" lang="ja">${s(a.glyph)}</div>
          <div class="kanji-readings">
            ${a.on?.length?`<p><strong>On:</strong> <span lang="ja">${a.on.map(s).join(" / ")}</span></p>`:Array.isArray(a.on)?'<p><strong>On:</strong> <span class="muted small">(none at N5)</span></p>':""}
            ${a.kun?.length?`<p><strong>Kun:</strong> <span lang="ja">${a.kun.map(s).join(" / ")}</span></p>`:Array.isArray(a.kun)?'<p><strong>Kun:</strong> <span class="muted small">(none at N5)</span></p>':""}
            ${(()=>{const l=b(a);return l.length?`<p><strong>Meaning:</strong> ${l.map(s).join(", ")}</p>`:""})()}
          </div>
        </div>
        <label class="known-toggle" title="Manually mark this kanji as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-kanji" ${k?"checked":""}>
          <span>Mark as known</span>
        </label>
      </div>
      ${a.examples?.length?`
        <section class="kanji-examples">
          <h3>Example usage (N5)</h3>
          <table class="kanji-examples-table">
            <tbody>
              ${a.examples.map(l=>`
                <tr>
                  <td class="ex-form" lang="ja">${s(l.form)}</td>
                  <td class="ex-reading" lang="ja">${s(l.reading||"")}</td>
                  <td class="ex-gloss">${s(l.gloss||"")}</td>
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
            ${a.sentences.map(l=>`
              <li>
                <p class="kanji-sentence-ja" lang="ja">${s(l.ja)}</p>
                ${l.translation_en?`<p class="kanji-sentence-en muted small">${s(l.translation_en)}</p>`:""}
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
        ${r?`<a href="#/kanji/${encodeURIComponent(r.glyph)}"><span lang="ja">${s(r.glyph)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-kanji")?.addEventListener("change",l=>{$.setKanjiKnown(a.glyph,l.target.checked)})}function s(n){return String(n??"").replace(/[&<>"']/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[a])}export{K as renderKanji};
