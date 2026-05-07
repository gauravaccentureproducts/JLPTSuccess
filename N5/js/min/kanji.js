import*as $ from"./storage.js";import{currentLocale as b}from"./i18n.js";import{renderItemBadge as y}from"./provenance-badge.js";function _(n){const a=b();if(a&&a!=="en"){const t=n[`meanings_${a}`];if(Array.isArray(t)&&t.length)return t}return n.meanings||[]}let f=null;async function w(){return f||(f=await(await fetch("data/kanji.json")).json(),f)}async function K(n,a){await w();const t=f.entries||[],i=a?decodeURIComponent(a):"";if(!i)return m(n,t);const r=t.find(l=>l.glyph===i);if(!r){n.innerHTML=`
      <div class="placeholder">
        <h2>Kanji not found</h2>
        <p>No N5 entry for <strong lang="ja">${e(i)}</strong>.</p>
        <p><a href="#/kanji" class="btn-primary" style="text-decoration:none">Back to kanji list</a></p>
      </div>
    `;return}return C(n,r,t)}let j="",d="all",k="all",g="lesson";function S(n){return n==null?"":n<=5?"1-5":n<=10?"6-10":n<=15?"11-15":"16+"}function x(n){return n==null?"":n<=30?"1-30":n<=60?"31-60":n<=90?"61-90":"91-106"}function L(n,a,t,i){if(a){const r=n.additional_readings||{};if(![n.glyph||"",...n.on||[],...n.kun||[],...r.on||[],...r.kun||[],...n.meanings||[]].join(" ").toLowerCase().includes(a))return!1}return!(t!=="all"&&S(n.stroke_count)!==t||i!=="all"&&x(n.lesson_order)!==i)}function v(n){switch(g){case"frequency":return n.frequency_rank??999;case"strokes":return n.stroke_count??999;case"glyph":return n.glyph||"";default:return n.lesson_order??999}}function m(n,a){const t=j.trim().toLowerCase(),i=a.filter(o=>L(o,t,d,k)).slice().sort((o,c)=>{const p=v(o),h=v(c);return typeof p=="string"?p.localeCompare(h):p-h}),r=i.map(o=>`
    <a class="kanji-card" href="#/kanji/${encodeURIComponent(o.glyph)}">
      <span class="kanji-card-glyph" lang="ja">${e(o.glyph)}</span>
    </a>
  `).join(""),l=(o,c,p,h)=>`<button type="button" class="kanji-chip ${h?"active":""}"
       data-filter-group="${o}" data-filter-value="${c}">${e(p)}</button>`;n.innerHTML=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Kanji</h2>
    <p>${a.length} kanji at JLPT N5 level. Tap any card for readings, meanings, and stroke order.</p>

    <div class="kanji-filters" role="search" aria-label="Filter kanji">
      <input type="search" id="kanji-filter-q" class="kanji-filter-input"
        placeholder="Search reading, meaning, or glyph (e.g. \u307F\u305A / water / \u6C34)"
        value="${e(j)}" autocomplete="off" lang="ja"
        aria-label="Search kanji by reading, meaning, or glyph">

      <div class="kanji-filter-row" aria-label="Stroke count filter">
        <span class="kanji-filter-label">Strokes:</span>
        ${l("stroke","all","All",d==="all")}
        ${l("stroke","1-5","1-5",d==="1-5")}
        ${l("stroke","6-10","6-10",d==="6-10")}
        ${l("stroke","11-15","11-15",d==="11-15")}
        ${l("stroke","16+","16+",d==="16+")}
      </div>

      <div class="kanji-filter-row" aria-label="Lesson order filter">
        <span class="kanji-filter-label">Lesson:</span>
        ${l("lesson","all","All",k==="all")}
        ${l("lesson","1-30","1-30",k==="1-30")}
        ${l("lesson","31-60","31-60",k==="31-60")}
        ${l("lesson","61-90","61-90",k==="61-90")}
        ${l("lesson","91-106","91-106",k==="91-106")}
      </div>

      <div class="kanji-filter-row kanji-sort-row" aria-label="Sort kanji">
        <span class="kanji-filter-label">Sort:</span>
        <select id="kanji-sort" class="kanji-sort-select" aria-label="Sort kanji by">
          <option value="lesson"    ${g==="lesson"?"selected":""}>Lesson order (default)</option>
          <option value="frequency" ${g==="frequency"?"selected":""}>Frequency rank</option>
          <option value="strokes"   ${g==="strokes"?"selected":""}>Stroke count</option>
          <option value="glyph"     ${g==="glyph"?"selected":""}>Glyph (Unicode order)</option>
        </select>
      </div>

      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${i.length}</strong> of ${a.length}.
      </p>
    </div>

    <div class="kanji-card-grid">${r||'<p class="muted">No kanji match the current filters.</p>'}</div>
  `;const u=document.getElementById("kanji-filter-q");u&&u.addEventListener("input",()=>{j=u.value,m(n,a);const o=document.getElementById("kanji-filter-q");if(o){o.focus();const c=o.value;o.setSelectionRange(c.length,c.length)}}),n.querySelectorAll("[data-filter-group]").forEach(o=>{o.addEventListener("click",()=>{const c=o.dataset.filterGroup,p=o.dataset.filterValue;c==="stroke"?d=p:c==="lesson"&&(k=p),m(n,a)})});const s=document.getElementById("kanji-sort");s&&s.addEventListener("change",()=>{g=s.value,m(n,a)})}function C(n,a,t){const i=t.findIndex(s=>s.glyph===a.glyph),r=i>0?t[i-1]:null,l=i<t.length-1?t[i+1]:null,u=$.isKanjiKnown(a.glyph);n.innerHTML=`
    <article class="kanji-detail">
      <div class="srs-progress">
        <a href="#/kanji">\u2190 All kanji</a>
        <span class="muted small">${i+1} of ${t.length}</span>
      </div>
      <div class="kanji-glyph-row pattern-header">
        <div class="kanji-glyph-cluster">
          <div class="kanji-glyph-big" lang="ja">${e(a.glyph)}</div>
          <div class="kanji-readings">
            ${a.on?.length?`<p><strong>On:</strong> <span lang="ja">${a.on.map(e).join(" / ")}</span></p>`:Array.isArray(a.on)?'<p><strong>On:</strong> <span class="muted small">(none at N5)</span></p>':""}
            ${a.kun?.length?`<p><strong>Kun:</strong> <span lang="ja">${a.kun.map(e).join(" / ")}</span></p>`:Array.isArray(a.kun)?'<p><strong>Kun:</strong> <span class="muted small">(none at N5)</span></p>':""}
            ${(()=>{const s=_(a);return s.length?`<p><strong>Meaning:</strong> ${s.map(e).join(", ")} ${y(a,!0)}</p>`:""})()}
          </div>
        </div>
        <label class="known-toggle" title="Manually mark this kanji as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-kanji" ${u?"checked":""}>
          <span>Mark as known</span>
        </label>
      </div>
      ${a.radical||a.radical_decomposition||a.mnemonic?`
        <section class="kanji-mnemonic-block">
          <h3>Radical &amp; mnemonic</h3>
          ${a.radical?`
            <p><strong>Radical:</strong>
              <span class="kanji-radical-glyph" lang="ja">${e(a.radical.glyph||"")}</span>
              <span class="muted small">${e(a.radical.name||"")}</span>
            </p>
          `:""}
          ${a.radical_decomposition?.length?`
            <p><strong>Components:</strong>
              <span class="kanji-decomposition" lang="ja">${a.radical_decomposition.map(e).join(" + ")}</span>
            </p>
          `:""}
          ${a.mnemonic?`<p class="kanji-mnemonic">${e(a.mnemonic)}</p>`:""}
        </section>
      `:""}
      ${a.confusable_with?.length?`
        <section class="kanji-confusable-block">
          <h3>Don't confuse with</h3>
          <div class="kanji-confusable-grid">
            ${a.confusable_with.map(s=>`
              <a class="kanji-confusable-card" href="#/kanji/${encodeURIComponent(s)}">
                <span lang="ja">${e(s)}</span>
              </a>
            `).join("")}
          </div>
        </section>
      `:""}
      ${a.examples?.length?`
        <section class="kanji-examples">
          <h3>Example usage (N5)</h3>
          <table class="kanji-examples-table">
            <tbody>
              ${a.examples.map(s=>`
                <tr>
                  <td class="ex-form" lang="ja">${e(s.form)}</td>
                  <td class="ex-reading" lang="ja">${e(s.reading||"")}</td>
                  <td class="ex-gloss">${e(s.gloss||"")}</td>
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
            ${a.sentences.map(s=>`
              <li>
                <p class="kanji-sentence-ja" lang="ja">${e(s.ja)}</p>
                ${s.translation_en?`<p class="kanji-sentence-en muted small">${e(s.translation_en)}</p>`:""}
              </li>
            `).join("")}
          </ul>
        </section>
      `:""}
      ${a.stroke_order_svg?`
        <section class="kanji-stroke">
          <h3>Stroke order</h3>
          <object class="stroke-svg" data="${e(a.stroke_order_svg)}" type="image/svg+xml" aria-label="Stroke order for ${e(a.glyph)}">
            <p class="muted small">Stroke-order diagram could not load.</p>
          </object>
          <p class="muted small kanji-stroke-credit">Stroke data: <a href="https://kanjivg.tagaini.net/" rel="noopener noreferrer" target="_blank">KanjiVG</a> (CC BY-SA 3.0).</p>
        </section>
      `:""}
      ${a.stroke_order_mistakes?`
        <!-- JCE-7 (round-9 follow-up, 2026-05-08): classroom-trap notes
             on stroke order, authored by the resident JA-teacher
             persona. Surfaces below the SVG so a learner reading the
             diagram has the trap context inline. -->
        <section class="kanji-stroke-mistakes">
          <h3>Common stroke-order traps</h3>
          <p class="kanji-stroke-mistake-note" lang="ja">${e(a.stroke_order_mistakes)}</p>
        </section>
      `:""}
      <nav class="kanji-nav">
        ${r?`<a href="#/kanji/${encodeURIComponent(r.glyph)}">\u2190 <span lang="ja">${e(r.glyph)}</span></a>`:"<span></span>"}
        ${l?`<a href="#/kanji/${encodeURIComponent(l.glyph)}"><span lang="ja">${e(l.glyph)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-kanji")?.addEventListener("change",s=>{$.setKanjiKnown(a.glyph,s.target.checked)})}function e(n){return String(n??"").replace(/[&<>"']/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[a])}export{K as renderKanji};
