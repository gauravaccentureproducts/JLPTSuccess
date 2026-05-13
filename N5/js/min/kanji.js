import*as _ from"./storage.js";import{currentLocale as y,t}from"./i18n.js";import{renderItemBadge as b}from"./provenance-badge.js";function w(s){const n=y();if(n&&n!=="en"){const l=s[`meanings_${n}`];if(Array.isArray(l)&&l.length)return l}return s.meanings||[]}let h=null;async function x(){return h||(h=await(await fetch("data/kanji.json")).json(),h)}async function K(s,n){await x();const l=h.entries||[],r=n?decodeURIComponent(n):"";if(!r)return $(s,l);const d=l.find(o=>o.glyph===r);if(!d){s.innerHTML=`
      <div class="placeholder">
        <h2>Kanji not found</h2>
        <p>No N5 entry for <strong lang="ja">${a(r)}</strong>.</p>
        <p><a href="#/kanji" class="btn-primary" style="text-decoration:none">Back to kanji list</a></p>
      </div>
    `;return}return L(s,d,l)}let f="",k="all",m="all",j="lesson";function S(s){return s==null?"":s<=5?"1-5":s<=10?"6-10":s<=15?"11-15":"16+"}function I(s){return s==null?"":s<=30?"1-30":s<=60?"31-60":s<=90?"61-90":"91-106"}function C(s,n,l,r){if(n){const d=s.additional_readings||{};if(![s.glyph||"",...s.on||[],...s.kun||[],...d.on||[],...d.kun||[],...s.meanings||[]].join(" ").toLowerCase().includes(n))return!1}return!(l!=="all"&&S(s.stroke_count)!==l||r!=="all"&&I(s.lesson_order)!==r)}function v(s){switch(j){case"frequency":return s.frequency_rank??999;case"strokes":return s.stroke_count??999;case"glyph":return s.glyph||"";default:return s.lesson_order??999}}function $(s,n){const l=f.trim().toLowerCase(),r=n.filter(i=>C(i,l,k,m)).slice().sort((i,c)=>{const p=v(i),g=v(c);return typeof p=="string"?p.localeCompare(g):p-g}),d=r.map(i=>`
    <a class="kanji-card" href="#/kanji/${encodeURIComponent(i.glyph)}">
      <span class="kanji-card-glyph" lang="ja">${a(i.glyph)}</span>
    </a>
  `).join(""),o=(i,c,p,g)=>`<button type="button" class="kanji-chip ${g?"active":""}"
       data-filter-group="${i}" data-filter-value="${c}">${a(p)}</button>`;s.innerHTML=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Kanji</h2>
    <p>${n.length} kanji at JLPT N5 level. Tap any card for readings, meanings, and stroke order.</p>

    <div class="kanji-filters" role="search" aria-label="Filter kanji">
      <input type="search" id="kanji-filter-q" class="kanji-filter-input"
        placeholder="Search reading, meaning, or glyph (e.g. \u307F\u305A / water / \u6C34)"
        value="${a(f)}" autocomplete="off" lang="ja"
        aria-label="Search kanji by reading, meaning, or glyph">

      <div class="kanji-filter-row" aria-label="Stroke count filter">
        <span class="kanji-filter-label">Strokes:</span>
        ${o("stroke","all","All",k==="all")}
        ${o("stroke","1-5","1-5",k==="1-5")}
        ${o("stroke","6-10","6-10",k==="6-10")}
        ${o("stroke","11-15","11-15",k==="11-15")}
        ${o("stroke","16+","16+",k==="16+")}
      </div>

      <div class="kanji-filter-row" aria-label="Lesson order filter">
        <span class="kanji-filter-label">Lesson:</span>
        ${o("lesson","all","All",m==="all")}
        ${o("lesson","1-30","1-30",m==="1-30")}
        ${o("lesson","31-60","31-60",m==="31-60")}
        ${o("lesson","61-90","61-90",m==="61-90")}
        ${o("lesson","91-106","91-106",m==="91-106")}
      </div>

      <div class="kanji-filter-row kanji-sort-row" aria-label="Sort kanji">
        <span class="kanji-filter-label">Sort:</span>
        <select id="kanji-sort" class="kanji-sort-select" aria-label="Sort kanji by">
          <option value="lesson"    ${j==="lesson"?"selected":""}>Lesson order (default)</option>
          <option value="frequency" ${j==="frequency"?"selected":""}>Frequency rank</option>
          <option value="strokes"   ${j==="strokes"?"selected":""}>Stroke count</option>
          <option value="glyph"     ${j==="glyph"?"selected":""}>Glyph (Unicode order)</option>
        </select>
      </div>

      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${r.length}</strong> of ${n.length}.
      </p>
    </div>

    <div class="kanji-card-grid">${d||'<p class="muted">No kanji match the current filters.</p>'}</div>
  `;const u=document.getElementById("kanji-filter-q");if(u){let i=!1;const c=()=>{f=u.value,$(s,n);const p=document.getElementById("kanji-filter-q");if(p){p.focus();const g=p.value;p.setSelectionRange(g.length,g.length)}};u.addEventListener("compositionstart",()=>{i=!0}),u.addEventListener("compositionend",()=>{i=!1,c()}),u.addEventListener("input",()=>{i||c()})}s.querySelectorAll("[data-filter-group]").forEach(i=>{i.addEventListener("click",()=>{const c=i.dataset.filterGroup,p=i.dataset.filterValue;c==="stroke"?k=p:c==="lesson"&&(m=p),$(s,n)})});const e=document.getElementById("kanji-sort");e&&e.addEventListener("change",()=>{j=e.value,$(s,n)})}function L(s,n,l){const r=l.findIndex(e=>e.glyph===n.glyph),d=r>0?l[r-1]:null,o=r<l.length-1?l[r+1]:null,u=_.isKanjiKnown(n.glyph);s.innerHTML=`
    <article class="kanji-detail">
      <div class="srs-progress">
        <a href="#/kanji">\u2190 ${a(t("kanji_detail.all_kanji"))}</a>
        <span class="muted small">${r+1} ${a(t("kanji_detail.of_total"))} ${l.length}</span>
      </div>
      <div class="kanji-glyph-row pattern-header">
        <div class="kanji-glyph-cluster">
          <div class="kanji-glyph-big" lang="ja">${a(n.glyph)}</div>
          <div class="kanji-readings">
            ${n.on?.length?`<p><strong>${a(t("kanji_detail.on"))}:</strong> <span lang="ja">${n.on.map(a).join(" / ")}</span></p>`:Array.isArray(n.on)?`<p><strong>${a(t("kanji_detail.on"))}:</strong> <span class="muted small">${a(t("kanji_detail.none_at_n5"))}</span></p>`:""}
            ${n.kun?.length?`<p><strong>${a(t("kanji_detail.kun"))}:</strong> <span lang="ja">${n.kun.map(a).join(" / ")}</span></p>`:Array.isArray(n.kun)?`<p><strong>${a(t("kanji_detail.kun"))}:</strong> <span class="muted small">${a(t("kanji_detail.none_at_n5"))}</span></p>`:""}
            ${(()=>{const e=w(n);return e.length?`<p><strong>${a(t("kanji_detail.meaning"))}:</strong> ${e.map(a).join(", ")} ${b(n,!0)}</p>`:""})()}
          </div>
        </div>
        <label class="known-toggle" title="Manually mark this kanji as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-kanji" ${u?"checked":""}>
          <span>${a(t("kanji_detail.mark_as_known"))}</span>
        </label>
      </div>
      ${n.radical||n.radical_decomposition||n.mnemonic?`
        <section class="kanji-mnemonic-block">
          <h3>${a(t("kanji_detail.radical_and_mnemonic"))}</h3>
          ${n.radical?`
            <p><strong>${a(t("kanji_detail.radical"))}:</strong>
              <span class="kanji-radical-glyph" lang="ja">${a(n.radical.glyph||"")}</span>
              <span class="muted small">${a(n.radical.name||"")}</span>
            </p>
          `:""}
          ${n.radical_decomposition?.length?`
            <p><strong>${a(t("kanji_detail.components"))}:</strong>
              <span class="kanji-decomposition" lang="ja">${n.radical_decomposition.map(a).join(" + ")}</span>
            </p>
          `:""}
          ${A(n.mnemonic)}
          ${n.etymology?`
            <!-- IMP-WAVE-P2-13 (UI audit fix, 2026-05-11): historical /
                 pictographic origin of the kanji. Schema:
                 {origin_type, story, related_modern}. -->
            <div class="kanji-etymology">
              <p><strong>Etymology:</strong>
                <span class="kanji-etymology-type muted small">(${a(n.etymology.origin_type||"origin")})</span>
                ${a(n.etymology.story||"")}
              </p>
              ${n.etymology.related_modern?`
                <p class="muted small">${a(n.etymology.related_modern)}</p>
              `:""}
            </div>
          `:""}
        </section>
      `:""}
      ${n.confusable_with?.length?`
        <section class="kanji-confusable-block">
          <h3>${a(t("kanji_detail.dont_confuse"))}</h3>
          <div class="kanji-confusable-grid">
            ${n.confusable_with.map(e=>`
              <a class="kanji-confusable-card" href="#/kanji/${encodeURIComponent(e)}">
                <span lang="ja">${a(e)}</span>
              </a>
            `).join("")}
          </div>
        </section>
      `:""}
      ${n.examples?.length?`
        <section class="kanji-examples">
          <h3>${a(t("kanji_detail.example_usage"))}</h3>
          <table class="kanji-examples-table">
            <tbody>
              ${n.examples.map(e=>`
                <tr>
                  <td class="ex-form" lang="ja">${a(e.form)}</td>
                  <td class="ex-reading" lang="ja">${a(e.reading||"")}</td>
                  <td class="ex-gloss">${a(e.gloss||"")}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </section>
      `:""}
      ${n.n5_compounds?.length?`
        <!-- IMP-176 (2026-05-13): Jisho-style "words containing this kanji"
             with click-through to the vocab detail page. n5_compounds is
             the same schema as examples but with vocab_id linking. -->
        <section class="kanji-n5-compounds">
          <h3>Words containing this kanji</h3>
          <p class="muted small">
            N5-scope vocabulary that uses this kanji. Click any row to jump to its vocab entry.
          </p>
          <table class="kanji-examples-table">
            <tbody>
              ${n.n5_compounds.map(e=>{const i=e.form?`#/learn/vocab/${encodeURIComponent(e.form)}`:null;return`
                  <tr>
                    <td class="ex-form">${i?`<a href="${a(i)}" lang="ja">${a(e.form)}</a>`:`<span lang="ja">${a(e.form)}</span>`}</td>
                    <td class="ex-reading" lang="ja">${a(e.reading||"")}</td>
                    <td class="ex-gloss">${a(e.gloss||"")}</td>
                  </tr>
                `}).join("")}
            </tbody>
          </table>
        </section>
      `:""}
      ${n.sentences?.length?`
        <section class="kanji-sentences">
          <h3>${a(t("kanji_detail.in_a_sentence"))}</h3>
          <ul class="kanji-sentences-list">
            ${n.sentences.map(e=>`
              <li>
                <p class="kanji-sentence-ja" lang="ja">${a(e.ja)}</p>
                ${e.translation_en?`<p class="kanji-sentence-en muted small">${a(e.translation_en)}</p>`:""}
              </li>
            `).join("")}
          </ul>
        </section>
      `:""}
      ${n.authentic_refs?.length?`
        <!-- IMP-WAVE-AUTHENTIC-XLINK (2026-05-11): real-world
             cards where this kanji appears on actual JP signs,
             menus, transit boards, etc. The /authentic page
             hosts the source cards. -->
        <section class="kanji-authentic-refs">
          <h3>Seen in the real world</h3>
          <p class="muted small">
            This kanji appears on these authentic Japanese cards. Click to see the original sign / menu / notice in context.
          </p>
          <ul class="authentic-ref-list">
            ${n.authentic_refs.map(e=>{const i=e.split(".")[1]||"authentic";return`<li><a href="#/authentic">${a(e)}</a> <span class="muted small">(${a(i)})</span></li>`}).join("")}
          </ul>
        </section>
      `:""}
      ${n.stroke_order_svg?`
        <section class="kanji-stroke">
          <h3>${a(t("kanji_detail.stroke_order"))}</h3>
          <object class="stroke-svg" data="${a(n.stroke_order_svg)}" type="image/svg+xml" aria-label="Stroke order for ${a(n.glyph)}">
            <p class="muted small">${a(t("kanji_detail.stroke_diagram_fail"))}</p>
          </object>
          <p class="muted small kanji-stroke-credit">${a(t("kanji_detail.stroke_order_credit"))}: <a href="https://kanjivg.tagaini.net/" rel="noopener noreferrer" target="_blank">KanjiVG</a> (CC BY-SA 3.0).</p>
        </section>
      `:""}
      ${n.stroke_order_mistakes?`
        <!-- JCE-7 (round-9 follow-up, 2026-05-08): classroom-trap notes
             on stroke order, authored by the resident JA-teacher
             persona. Surfaces below the SVG so a learner reading the
             diagram has the trap context inline. -->
        <section class="kanji-stroke-mistakes">
          <h3>${a(t("kanji_detail.stroke_order_traps"))}</h3>
          <p class="kanji-stroke-mistake-note" lang="ja">${a(n.stroke_order_mistakes)}</p>
        </section>
      `:""}
      ${(()=>{const e=n.stroke_order_trap;return!e||typeof e!="object"?"":`
          <section class="kanji-stroke-trap">
            <h3>${a(t("kanji_detail.stroke_order_trap_section"))}</h3>
            ${e.trap?`<p><strong>${a(t("kanji_detail.what_learners_get_wrong"))}:</strong> ${a(e.trap)}</p>`:""}
            ${e.correct_order_summary?`<p><strong>${a(t("kanji_detail.correct_order"))}:</strong> ${a(e.correct_order_summary)}</p>`:""}
            ${e.why_it_matters?`<p><strong>${a(t("kanji_detail.why_it_matters"))}:</strong> ${a(e.why_it_matters)}</p>`:""}
          </section>
        `})()}
      ${(()=>{const e=n.on_kun_pair_drill;if(!e||typeof e!="object")return"";const i=e.standalone||{},c=e.compound||{};return`
          <section class="kanji-on-kun-drill">
            <h3>${a(t("kanji_detail.on_kun_pair_drill"))}</h3>
            <table class="on-kun-drill-table">
              <thead>
                <tr><th>${a(t("kanji_detail.standalone_typically_kun"))}</th><th>${a(t("kanji_detail.compound_typically_on"))}</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <span class="form" lang="ja">${a(i.form||"")}</span>
                    <span class="reading muted small" lang="ja">${a(i.reading||"")}</span>
                    <span class="gloss">${a(i.gloss||"")}</span>
                  </td>
                  <td>
                    <span class="form" lang="ja">${a(c.form||"")}</span>
                    <span class="reading muted small" lang="ja">${a(c.reading||"")}</span>
                    <span class="gloss">${a(c.gloss||"")}</span>
                  </td>
                </tr>
              </tbody>
            </table>
            ${e.contrast_note?`<p class="contrast-note">${a(e.contrast_note)}</p>`:""}
          </section>
        `})()}
      ${n.reading_rule?`
        <section class="kanji-reading-rule">
          <h3>${a(t("kanji_detail.reading_rule_of_thumb"))}</h3>
          <p class="muted small">${a(n.reading_rule)}</p>
        </section>
      `:""}
      ${(()=>{const e=Array.isArray(n.okurigana_cuts)?n.okurigana_cuts:[];return e.length?`
          <section class="kanji-okurigana-cuts">
            <h3>${a(t("kanji_detail.okurigana_boundary"))}</h3>
            <p class="muted small">${a(t("kanji_detail.okurigana_intro"))}</p>
            <ul class="okurigana-cuts-list">
              ${e.map(i=>{const c=String(i).split(":");return c.length!==2?`<li><span lang="ja">${a(i)}</span></li>`:`<li>
                  <span class="okurigana-kanji" lang="ja">${a(c[0])}</span><span class="okurigana-cut" aria-hidden="true">\uFE31</span><span class="okurigana-suffix" lang="ja">${a(c[1])}</span>
                </li>`}).join("")}
            </ul>
          </section>
        `:""})()}
      <nav class="kanji-nav">
        ${d?`<a href="#/kanji/${encodeURIComponent(d.glyph)}">\u2190 <span lang="ja">${a(d.glyph)}</span></a>`:"<span></span>"}
        ${o?`<a href="#/kanji/${encodeURIComponent(o.glyph)}"><span lang="ja">${a(o.glyph)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-kanji")?.addEventListener("change",e=>{_.setKanjiKnown(n.glyph,e.target.checked)})}function a(s){return String(s??"").replace(/[&<>"']/g,n=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[n])}function A(s){if(!s)return"";if(typeof s=="string")return`<p class="kanji-mnemonic">${a(s)}</p>`;if(typeof s!="object")return"";const n=s.summary||s.meaning||"",l=s.visual||"",r=s.reading||"",d=s.provenance||{},o=e=>d[e]==="auto_derived"?' <span class="kanji-mnemonic-prov muted small" title="Auto-derived stub; pending native review.">auto</span>':"",u=[];return n&&u.push(`<p class="kanji-mnemonic kanji-mnemonic-summary"><strong>Meaning:</strong> ${a(n)}${o("summary")}</p>`),l&&l!==n&&u.push(`<p class="kanji-mnemonic kanji-mnemonic-visual"><strong>Visual:</strong> ${a(l)}${o("visual")}</p>`),r&&u.push(`<p class="kanji-mnemonic kanji-mnemonic-reading"><strong>Reading:</strong> ${a(r)}${o("reading")}</p>`),u.join(`
          `)}export{K as renderKanji};
