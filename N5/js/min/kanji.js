import*as $ from"./storage.js";import{currentLocale as y}from"./i18n.js";import{renderItemBadge as b}from"./provenance-badge.js";function _(a){const n=y();if(n&&n!=="en"){const t=a[`meanings_${n}`];if(Array.isArray(t)&&t.length)return t}return a.meanings||[]}let f=null;async function w(){return f||(f=await(await fetch("data/kanji.json")).json(),f)}async function B(a,n){await w();const t=f.entries||[],l=n?decodeURIComponent(n):"";if(!l)return j(a,t);const r=t.find(o=>o.glyph===l);if(!r){a.innerHTML=`
      <div class="placeholder">
        <h2>Kanji not found</h2>
        <p>No N5 entry for <strong lang="ja">${e(l)}</strong>.</p>
        <p><a href="#/kanji" class="btn-primary" style="text-decoration:none">Back to kanji list</a></p>
      </div>
    `;return}return C(a,r,t)}let h="",g="all",k="all",m="lesson";function S(a){return a==null?"":a<=5?"1-5":a<=10?"6-10":a<=15?"11-15":"16+"}function L(a){return a==null?"":a<=30?"1-30":a<=60?"31-60":a<=90?"61-90":"91-106"}function x(a,n,t,l){if(n){const r=a.additional_readings||{};if(![a.glyph||"",...a.on||[],...a.kun||[],...r.on||[],...r.kun||[],...a.meanings||[]].join(" ").toLowerCase().includes(n))return!1}return!(t!=="all"&&S(a.stroke_count)!==t||l!=="all"&&L(a.lesson_order)!==l)}function v(a){switch(m){case"frequency":return a.frequency_rank??999;case"strokes":return a.stroke_count??999;case"glyph":return a.glyph||"";default:return a.lesson_order??999}}function j(a,n){const t=h.trim().toLowerCase(),l=n.filter(i=>x(i,t,g,k)).slice().sort((i,d)=>{const c=v(i),u=v(d);return typeof c=="string"?c.localeCompare(u):c-u}),r=l.map(i=>`
    <a class="kanji-card" href="#/kanji/${encodeURIComponent(i.glyph)}">
      <span class="kanji-card-glyph" lang="ja">${e(i.glyph)}</span>
    </a>
  `).join(""),o=(i,d,c,u)=>`<button type="button" class="kanji-chip ${u?"active":""}"
       data-filter-group="${i}" data-filter-value="${d}">${e(c)}</button>`;a.innerHTML=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Kanji</h2>
    <p>${n.length} kanji at JLPT N5 level. Tap any card for readings, meanings, and stroke order.</p>

    <div class="kanji-filters" role="search" aria-label="Filter kanji">
      <input type="search" id="kanji-filter-q" class="kanji-filter-input"
        placeholder="Search reading, meaning, or glyph (e.g. \u307F\u305A / water / \u6C34)"
        value="${e(h)}" autocomplete="off" lang="ja"
        aria-label="Search kanji by reading, meaning, or glyph">

      <div class="kanji-filter-row" aria-label="Stroke count filter">
        <span class="kanji-filter-label">Strokes:</span>
        ${o("stroke","all","All",g==="all")}
        ${o("stroke","1-5","1-5",g==="1-5")}
        ${o("stroke","6-10","6-10",g==="6-10")}
        ${o("stroke","11-15","11-15",g==="11-15")}
        ${o("stroke","16+","16+",g==="16+")}
      </div>

      <div class="kanji-filter-row" aria-label="Lesson order filter">
        <span class="kanji-filter-label">Lesson:</span>
        ${o("lesson","all","All",k==="all")}
        ${o("lesson","1-30","1-30",k==="1-30")}
        ${o("lesson","31-60","31-60",k==="31-60")}
        ${o("lesson","61-90","61-90",k==="61-90")}
        ${o("lesson","91-106","91-106",k==="91-106")}
      </div>

      <div class="kanji-filter-row kanji-sort-row" aria-label="Sort kanji">
        <span class="kanji-filter-label">Sort:</span>
        <select id="kanji-sort" class="kanji-sort-select" aria-label="Sort kanji by">
          <option value="lesson"    ${m==="lesson"?"selected":""}>Lesson order (default)</option>
          <option value="frequency" ${m==="frequency"?"selected":""}>Frequency rank</option>
          <option value="strokes"   ${m==="strokes"?"selected":""}>Stroke count</option>
          <option value="glyph"     ${m==="glyph"?"selected":""}>Glyph (Unicode order)</option>
        </select>
      </div>

      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${l.length}</strong> of ${n.length}.
      </p>
    </div>

    <div class="kanji-card-grid">${r||'<p class="muted">No kanji match the current filters.</p>'}</div>
  `;const p=document.getElementById("kanji-filter-q");if(p){let i=!1;const d=()=>{h=p.value,j(a,n);const c=document.getElementById("kanji-filter-q");if(c){c.focus();const u=c.value;c.setSelectionRange(u.length,u.length)}};p.addEventListener("compositionstart",()=>{i=!0}),p.addEventListener("compositionend",()=>{i=!1,d()}),p.addEventListener("input",()=>{i||d()})}a.querySelectorAll("[data-filter-group]").forEach(i=>{i.addEventListener("click",()=>{const d=i.dataset.filterGroup,c=i.dataset.filterValue;d==="stroke"?g=c:d==="lesson"&&(k=c),j(a,n)})});const s=document.getElementById("kanji-sort");s&&s.addEventListener("change",()=>{m=s.value,j(a,n)})}function C(a,n,t){const l=t.findIndex(s=>s.glyph===n.glyph),r=l>0?t[l-1]:null,o=l<t.length-1?t[l+1]:null,p=$.isKanjiKnown(n.glyph);a.innerHTML=`
    <article class="kanji-detail">
      <div class="srs-progress">
        <a href="#/kanji">\u2190 All kanji</a>
        <span class="muted small">${l+1} of ${t.length}</span>
      </div>
      <div class="kanji-glyph-row pattern-header">
        <div class="kanji-glyph-cluster">
          <div class="kanji-glyph-big" lang="ja">${e(n.glyph)}</div>
          <div class="kanji-readings">
            ${n.on?.length?`<p><strong>On:</strong> <span lang="ja">${n.on.map(e).join(" / ")}</span></p>`:Array.isArray(n.on)?'<p><strong>On:</strong> <span class="muted small">(none at N5)</span></p>':""}
            ${n.kun?.length?`<p><strong>Kun:</strong> <span lang="ja">${n.kun.map(e).join(" / ")}</span></p>`:Array.isArray(n.kun)?'<p><strong>Kun:</strong> <span class="muted small">(none at N5)</span></p>':""}
            ${(()=>{const s=_(n);return s.length?`<p><strong>Meaning:</strong> ${s.map(e).join(", ")} ${b(n,!0)}</p>`:""})()}
          </div>
        </div>
        <label class="known-toggle" title="Manually mark this kanji as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-kanji" ${p?"checked":""}>
          <span>Mark as known</span>
        </label>
      </div>
      ${n.radical||n.radical_decomposition||n.mnemonic?`
        <section class="kanji-mnemonic-block">
          <h3>Radical &amp; mnemonic</h3>
          ${n.radical?`
            <p><strong>Radical:</strong>
              <span class="kanji-radical-glyph" lang="ja">${e(n.radical.glyph||"")}</span>
              <span class="muted small">${e(n.radical.name||"")}</span>
            </p>
          `:""}
          ${n.radical_decomposition?.length?`
            <p><strong>Components:</strong>
              <span class="kanji-decomposition" lang="ja">${n.radical_decomposition.map(e).join(" + ")}</span>
            </p>
          `:""}
          ${I(n.mnemonic)}
        </section>
      `:""}
      ${n.confusable_with?.length?`
        <section class="kanji-confusable-block">
          <h3>Don't confuse with</h3>
          <div class="kanji-confusable-grid">
            ${n.confusable_with.map(s=>`
              <a class="kanji-confusable-card" href="#/kanji/${encodeURIComponent(s)}">
                <span lang="ja">${e(s)}</span>
              </a>
            `).join("")}
          </div>
        </section>
      `:""}
      ${n.examples?.length?`
        <section class="kanji-examples">
          <h3>Example usage (N5)</h3>
          <table class="kanji-examples-table">
            <tbody>
              ${n.examples.map(s=>`
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
      ${n.sentences?.length?`
        <section class="kanji-sentences">
          <h3>In a sentence</h3>
          <ul class="kanji-sentences-list">
            ${n.sentences.map(s=>`
              <li>
                <p class="kanji-sentence-ja" lang="ja">${e(s.ja)}</p>
                ${s.translation_en?`<p class="kanji-sentence-en muted small">${e(s.translation_en)}</p>`:""}
              </li>
            `).join("")}
          </ul>
        </section>
      `:""}
      ${n.stroke_order_svg?`
        <section class="kanji-stroke">
          <h3>Stroke order</h3>
          <object class="stroke-svg" data="${e(n.stroke_order_svg)}" type="image/svg+xml" aria-label="Stroke order for ${e(n.glyph)}">
            <p class="muted small">Stroke-order diagram could not load.</p>
          </object>
          <p class="muted small kanji-stroke-credit">Stroke data: <a href="https://kanjivg.tagaini.net/" rel="noopener noreferrer" target="_blank">KanjiVG</a> (CC BY-SA 3.0).</p>
        </section>
      `:""}
      ${n.stroke_order_mistakes?`
        <!-- JCE-7 (round-9 follow-up, 2026-05-08): classroom-trap notes
             on stroke order, authored by the resident JA-teacher
             persona. Surfaces below the SVG so a learner reading the
             diagram has the trap context inline. -->
        <section class="kanji-stroke-mistakes">
          <h3>Common stroke-order traps</h3>
          <p class="kanji-stroke-mistake-note" lang="ja">${e(n.stroke_order_mistakes)}</p>
        </section>
      `:""}
      <nav class="kanji-nav">
        ${r?`<a href="#/kanji/${encodeURIComponent(r.glyph)}">\u2190 <span lang="ja">${e(r.glyph)}</span></a>`:"<span></span>"}
        ${o?`<a href="#/kanji/${encodeURIComponent(o.glyph)}"><span lang="ja">${e(o.glyph)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-kanji")?.addEventListener("change",s=>{$.setKanjiKnown(n.glyph,s.target.checked)})}function e(a){return String(a??"").replace(/[&<>"']/g,n=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[n])}function I(a){if(!a)return"";if(typeof a=="string")return`<p class="kanji-mnemonic">${e(a)}</p>`;if(typeof a!="object")return"";const n=a.summary||a.meaning||"",t=a.visual||"",l=a.reading||"",r=a.provenance||{},o=s=>r[s]==="auto_derived"?' <span class="kanji-mnemonic-prov muted small" title="Auto-derived stub; pending native review.">auto</span>':"",p=[];return n&&p.push(`<p class="kanji-mnemonic kanji-mnemonic-summary"><strong>Meaning:</strong> ${e(n)}${o("summary")}</p>`),t&&t!==n&&p.push(`<p class="kanji-mnemonic kanji-mnemonic-visual"><strong>Visual:</strong> ${e(t)}${o("visual")}</p>`),l&&p.push(`<p class="kanji-mnemonic kanji-mnemonic-reading"><strong>Reading:</strong> ${e(l)}${o("reading")}</p>`),p.join(`
          `)}export{B as renderKanji};
