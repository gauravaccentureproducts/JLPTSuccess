import*as _ from"./storage.js";import{currentLocale as b,t}from"./i18n.js";import{renderItemBadge as y}from"./provenance-badge.js";function w(e){const n=b();if(n&&n!=="en"){const l=e[`meanings_${n}`];if(Array.isArray(l)&&l.length)return l}return e.meanings||[]}let m=null;async function S(){return m||(m=await(await fetch("data/kanji.json")).json(),m)}async function K(e,n){await S();const l=m.entries||[],o=n?decodeURIComponent(n):"";if(!o)return f(e,l);const p=l.find(r=>r.glyph===o);if(!p){e.innerHTML=`
      <div class="placeholder">
        <h2>Kanji not found</h2>
        <p>No N5 entry for <strong lang="ja">${a(o)}</strong>.</p>
        <p><a href="#/kanji" class="btn-primary" style="text-decoration:none">Back to kanji list</a></p>
      </div>
    `;return}return I(e,p,l)}let $="",g="all",j="all",h="lesson";function x(e){return e==null?"":e<=5?"1-5":e<=10?"6-10":e<=15?"11-15":"16+"}function L(e){return e==null?"":e<=30?"1-30":e<=60?"31-60":e<=90?"61-90":"91-106"}function A(e,n,l,o){if(n){const p=e.additional_readings||{};if(![e.glyph||"",...e.on||[],...e.kun||[],...p.on||[],...p.kun||[],...e.meanings||[]].join(" ").toLowerCase().includes(n))return!1}return!(l!=="all"&&x(e.stroke_count)!==l||o!=="all"&&L(e.lesson_order)!==o)}function v(e){switch(h){case"frequency":return e.frequency_rank??999;case"strokes":return e.stroke_count??999;case"glyph":return e.glyph||"";default:return e.lesson_order??999}}function f(e,n){const l=$.trim().toLowerCase(),o=n.filter(i=>A(i,l,g,j)).slice().sort((i,c)=>{const d=v(i),k=v(c);return typeof d=="string"?d.localeCompare(k):d-k}),p=o.map(i=>`
    <a class="kanji-card" href="#/kanji/${encodeURIComponent(i.glyph)}">
      <span class="kanji-card-glyph" lang="ja">${a(i.glyph)}</span>
    </a>
  `).join(""),r=(i,c,d,k)=>`<button type="button" class="kanji-chip ${k?"active":""}"
       data-filter-group="${i}" data-filter-value="${c}">${a(d)}</button>`;e.innerHTML=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Kanji</h2>
    <p>${n.length} kanji at JLPT N5 level. Tap any card for readings, meanings, and stroke order.</p>

    <div class="kanji-filters" role="search" aria-label="Filter kanji">
      <input type="search" id="kanji-filter-q" class="kanji-filter-input"
        placeholder="Search reading, meaning, or glyph (e.g. \u307F\u305A / water / \u6C34)"
        value="${a($)}" autocomplete="off" lang="ja"
        aria-label="Search kanji by reading, meaning, or glyph">

      <div class="kanji-filter-row" aria-label="Stroke count filter">
        <span class="kanji-filter-label">Strokes:</span>
        ${r("stroke","all","All",g==="all")}
        ${r("stroke","1-5","1-5",g==="1-5")}
        ${r("stroke","6-10","6-10",g==="6-10")}
        ${r("stroke","11-15","11-15",g==="11-15")}
        ${r("stroke","16+","16+",g==="16+")}
      </div>

      <div class="kanji-filter-row" aria-label="Lesson order filter">
        <span class="kanji-filter-label">Lesson:</span>
        ${r("lesson","all","All",j==="all")}
        ${r("lesson","1-30","1-30",j==="1-30")}
        ${r("lesson","31-60","31-60",j==="31-60")}
        ${r("lesson","61-90","61-90",j==="61-90")}
        ${r("lesson","91-106","91-106",j==="91-106")}
      </div>

      <div class="kanji-filter-row kanji-sort-row" aria-label="Sort kanji">
        <span class="kanji-filter-label">Sort:</span>
        <select id="kanji-sort" class="kanji-sort-select" aria-label="Sort kanji by">
          <option value="lesson"    ${h==="lesson"?"selected":""}>Lesson order (default)</option>
          <option value="frequency" ${h==="frequency"?"selected":""}>Frequency rank</option>
          <option value="strokes"   ${h==="strokes"?"selected":""}>Stroke count</option>
          <option value="glyph"     ${h==="glyph"?"selected":""}>Glyph (Unicode order)</option>
        </select>
      </div>

      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${o.length}</strong> of ${n.length}.
      </p>
    </div>

    <div class="kanji-card-grid">${p||'<p class="muted">No kanji match the current filters.</p>'}</div>
  `;const u=document.getElementById("kanji-filter-q");if(u){let i=!1;const c=()=>{$=u.value,f(e,n);const d=document.getElementById("kanji-filter-q");if(d){d.focus();const k=d.value;d.setSelectionRange(k.length,k.length)}};u.addEventListener("compositionstart",()=>{i=!0}),u.addEventListener("compositionend",()=>{i=!1,c()}),u.addEventListener("input",()=>{i||c()})}e.querySelectorAll("[data-filter-group]").forEach(i=>{i.addEventListener("click",()=>{const c=i.dataset.filterGroup,d=i.dataset.filterValue;c==="stroke"?g=d:c==="lesson"&&(j=d),f(e,n)})});const s=document.getElementById("kanji-sort");s&&s.addEventListener("change",()=>{h=s.value,f(e,n)})}function I(e,n,l){const o=l.findIndex(s=>s.glyph===n.glyph),p=o>0?l[o-1]:null,r=o<l.length-1?l[o+1]:null,u=_.isKanjiKnown(n.glyph);e.innerHTML=`
    <article class="kanji-detail">
      <div class="srs-progress">
        <a href="#/kanji">\u2190 ${a(t("kanji_detail.all_kanji"))}</a>
        <span class="muted small">${o+1} ${a(t("kanji_detail.of_total"))} ${l.length}</span>
      </div>
      <div class="kanji-glyph-row pattern-header">
        <div class="kanji-glyph-cluster">
          <div class="kanji-glyph-big" lang="ja">${a(n.glyph)}</div>
          <div class="kanji-readings">
            ${n.on?.length?`<p><strong>${a(t("kanji_detail.on"))}:</strong> <span lang="ja">${n.on.map(a).join(" / ")}</span></p>`:Array.isArray(n.on)?`<p><strong>${a(t("kanji_detail.on"))}:</strong> <span class="muted small">${a(t("kanji_detail.none_at_n5"))}</span></p>`:""}
            ${n.kun?.length?`<p><strong>${a(t("kanji_detail.kun"))}:</strong> <span lang="ja">${n.kun.map(a).join(" / ")}</span></p>`:Array.isArray(n.kun)?`<p><strong>${a(t("kanji_detail.kun"))}:</strong> <span class="muted small">${a(t("kanji_detail.none_at_n5"))}</span></p>`:""}
            ${(()=>{const s=w(n);return s.length?`<p><strong>${a(t("kanji_detail.meaning"))}:</strong> ${s.map(a).join(", ")} ${y(n,!0)}</p>`:""})()}
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
          ${C(n.mnemonic)}
        </section>
      `:""}
      ${n.confusable_with?.length?`
        <section class="kanji-confusable-block">
          <h3>${a(t("kanji_detail.dont_confuse"))}</h3>
          <div class="kanji-confusable-grid">
            ${n.confusable_with.map(s=>`
              <a class="kanji-confusable-card" href="#/kanji/${encodeURIComponent(s)}">
                <span lang="ja">${a(s)}</span>
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
              ${n.examples.map(s=>`
                <tr>
                  <td class="ex-form" lang="ja">${a(s.form)}</td>
                  <td class="ex-reading" lang="ja">${a(s.reading||"")}</td>
                  <td class="ex-gloss">${a(s.gloss||"")}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </section>
      `:""}
      ${n.sentences?.length?`
        <section class="kanji-sentences">
          <h3>${a(t("kanji_detail.in_a_sentence"))}</h3>
          <ul class="kanji-sentences-list">
            ${n.sentences.map(s=>`
              <li>
                <p class="kanji-sentence-ja" lang="ja">${a(s.ja)}</p>
                ${s.translation_en?`<p class="kanji-sentence-en muted small">${a(s.translation_en)}</p>`:""}
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
            ${n.authentic_refs.map(s=>{const i=s.split(".")[1]||"authentic";return`<li><a href="#/authentic">${a(s)}</a> <span class="muted small">(${a(i)})</span></li>`}).join("")}
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
      ${(()=>{const s=n.stroke_order_trap;return!s||typeof s!="object"?"":`
          <section class="kanji-stroke-trap">
            <h3>${a(t("kanji_detail.stroke_order_trap_section"))}</h3>
            ${s.trap?`<p><strong>${a(t("kanji_detail.what_learners_get_wrong"))}:</strong> ${a(s.trap)}</p>`:""}
            ${s.correct_order_summary?`<p><strong>${a(t("kanji_detail.correct_order"))}:</strong> ${a(s.correct_order_summary)}</p>`:""}
            ${s.why_it_matters?`<p><strong>${a(t("kanji_detail.why_it_matters"))}:</strong> ${a(s.why_it_matters)}</p>`:""}
          </section>
        `})()}
      ${(()=>{const s=n.on_kun_pair_drill;if(!s||typeof s!="object")return"";const i=s.standalone||{},c=s.compound||{};return`
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
            ${s.contrast_note?`<p class="contrast-note">${a(s.contrast_note)}</p>`:""}
          </section>
        `})()}
      ${n.reading_rule?`
        <section class="kanji-reading-rule">
          <h3>${a(t("kanji_detail.reading_rule_of_thumb"))}</h3>
          <p class="muted small">${a(n.reading_rule)}</p>
        </section>
      `:""}
      ${(()=>{const s=Array.isArray(n.okurigana_cuts)?n.okurigana_cuts:[];return s.length?`
          <section class="kanji-okurigana-cuts">
            <h3>${a(t("kanji_detail.okurigana_boundary"))}</h3>
            <p class="muted small">${a(t("kanji_detail.okurigana_intro"))}</p>
            <ul class="okurigana-cuts-list">
              ${s.map(i=>{const c=String(i).split(":");return c.length!==2?`<li><span lang="ja">${a(i)}</span></li>`:`<li>
                  <span class="okurigana-kanji" lang="ja">${a(c[0])}</span><span class="okurigana-cut" aria-hidden="true">\uFE31</span><span class="okurigana-suffix" lang="ja">${a(c[1])}</span>
                </li>`}).join("")}
            </ul>
          </section>
        `:""})()}
      <nav class="kanji-nav">
        ${p?`<a href="#/kanji/${encodeURIComponent(p.glyph)}">\u2190 <span lang="ja">${a(p.glyph)}</span></a>`:"<span></span>"}
        ${r?`<a href="#/kanji/${encodeURIComponent(r.glyph)}"><span lang="ja">${a(r.glyph)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-kanji")?.addEventListener("change",s=>{_.setKanjiKnown(n.glyph,s.target.checked)})}function a(e){return String(e??"").replace(/[&<>"']/g,n=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[n])}function C(e){if(!e)return"";if(typeof e=="string")return`<p class="kanji-mnemonic">${a(e)}</p>`;if(typeof e!="object")return"";const n=e.summary||e.meaning||"",l=e.visual||"",o=e.reading||"",p=e.provenance||{},r=s=>p[s]==="auto_derived"?' <span class="kanji-mnemonic-prov muted small" title="Auto-derived stub; pending native review.">auto</span>':"",u=[];return n&&u.push(`<p class="kanji-mnemonic kanji-mnemonic-summary"><strong>Meaning:</strong> ${a(n)}${r("summary")}</p>`),l&&l!==n&&u.push(`<p class="kanji-mnemonic kanji-mnemonic-visual"><strong>Visual:</strong> ${a(l)}${r("visual")}</p>`),o&&u.push(`<p class="kanji-mnemonic kanji-mnemonic-reading"><strong>Reading:</strong> ${a(o)}${r("reading")}</p>`),u.join(`
          `)}export{K as renderKanji};
