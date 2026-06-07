import*as j from"./storage.js";import{currentLocale as $,t}from"./i18n.js";import{renderItemBadge as f}from"./provenance-badge.js";function y(s){const n=$();if(n&&n!=="en"){const i=s[`meanings_${n}`];if(Array.isArray(i)&&i.length)return i}return s.meanings||[]}let m=null;async function v(){return m||(m=await(await fetch("data/kanji.json")).json(),m)}async function K(s,n){await v();const i=m.entries||[],o=n?decodeURIComponent(n):"";if(!o)return C(s,i);const l=i.find(c=>c.glyph===o);if(!l){s.innerHTML=`
      <div class="placeholder">
        <h2>Kanji not found</h2>
        <p>No N5 entry for <strong lang="ja">${a(o)}</strong>.</p>
        <p><a href="#/kanji" class="btn-primary" style="text-decoration:none">Back to kanji list</a></p>
      </div>
    `;return}return I(s,l,i)}let L="",S="all",B="all",b="lesson";function w(s){return s==null?"":s<=5?"1-5":s<=10?"6-10":s<=15?"11-15":"16+"}function x(s){return s==null?"":s<=30?"1-30":s<=60?"31-60":s<=90?"61-90":"91-106"}function U(s,n,i,o){if(n){const l=s.additional_readings||{};if(![s.glyph||"",...s.on||[],...s.kun||[],...l.on||[],...l.kun||[],...s.meanings||[]].join(" ").toLowerCase().includes(n))return!1}return!(i!=="all"&&w(s.stroke_count)!==i||o!=="all"&&x(s.lesson_order)!==o)}function E(s){switch(b){case"frequency":return s.frequency_rank??999;case"strokes":return s.stroke_count??999;case"glyph":return s.glyph||"";default:return s.lesson_order??999}}function C(s,n){const o=n.slice().sort((l,c)=>(l.lesson_order??999)-(c.lesson_order??999)).map(l=>`
    <a class="kanji-card" href="#/kanji/${encodeURIComponent(l.glyph)}">
      <span class="kanji-card-glyph" lang="ja">${a(l.glyph)}</span>
    </a>
  `).join("");s.innerHTML=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Kanji</h2>
    <p>${n.length} kanji at JLPT N5 level. Tap any card for readings, meanings, and stroke order.</p>
    <div class="kanji-card-grid">${o}</div>
  `}function I(s,n,i){const o=i.findIndex(e=>e.glyph===n.glyph),l=o>0?i[o-1]:null,c=o<i.length-1?i[o+1]:null,u=j.isKanjiKnown(n.glyph);s.innerHTML=`
    <article class="kanji-detail">
      <div class="srs-progress">
        <a href="#/kanji">\u2190 ${a(t("kanji_detail.all_kanji"))}</a>
        <span class="muted small">${o+1} ${a(t("kanji_detail.of_total"))} ${i.length}</span>
      </div>
      <div class="kanji-glyph-row pattern-header">
        <div class="kanji-glyph-cluster">
          <div class="kanji-glyph-big" lang="ja">${a(n.glyph)}</div>
          <div class="kanji-readings">
            ${n.on?.length?`<p><strong>${a(t("kanji_detail.on"))}:</strong> <span lang="ja">${n.on.map(a).join(" / ")}</span></p>`:Array.isArray(n.on)?`<p><strong>${a(t("kanji_detail.on"))}:</strong> <span class="muted small">${a(t("kanji_detail.none_at_n5"))}</span></p>`:""}
            ${n.kun?.length?`<p><strong>${a(t("kanji_detail.kun"))}:</strong> <span lang="ja">${n.kun.map(a).join(" / ")}</span></p>`:Array.isArray(n.kun)?`<p><strong>${a(t("kanji_detail.kun"))}:</strong> <span class="muted small">${a(t("kanji_detail.none_at_n5"))}</span></p>`:""}
            ${(()=>{const e=y(n);return e.length?`<p><strong>${a(t("kanji_detail.meaning"))}:</strong> ${e.map(a).join(", ")} ${f(n,!0)}</p>`:""})()}
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
          ${n.mnemonic_image?`
            <!-- Mnemonic illustration (decorative memory-aid card). The
                 authoritative readings/meaning stay as the live HTML above;
                 the image is supplementary. alt text + lazy-load required. -->
            <figure class="kanji-mnemonic-figure">
              <img class="kanji-mnemonic-img" src="${a(n.mnemonic_image)}"
                   loading="lazy" decoding="async"
                   alt="${a(n.mnemonic_image_alt||"Memory-aid illustration for the kanji "+(n.glyph||""))}">
            </figure>
          `:""}
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
      ${(()=>{const e=n.glyph||"",d=n.n5_compounds||[],p=new Set(d.filter(r=>r.form).map(r=>r.form)),h=new Set,k=[];for(const r of[...n.examples||[],...d]){const g=r.form||"";!g||!g.includes(e)||h.has(g)||(h.add(g),k.push({form:g,reading:r.reading||"",gloss:r.gloss||"",link:p.has(g)}))}if(!k.length)return"";const _=k.map(r=>`
                <tr>
                  <td class="ex-form">${r.link?`<a href="#/learn/vocab/${encodeURIComponent(r.form)}" lang="ja">${a(r.form)}</a>`:`<span lang="ja">${a(r.form)}</span>`}</td>
                  <td class="ex-reading" lang="ja">${a(r.reading)}</td>
                  <td class="ex-gloss">${a(r.gloss)}</td>
                </tr>`).join("");return`
        <section class="kanji-examples">
          <h3>${a(t("kanji_detail.example_usage"))}</h3>
          <p class="muted small">N5 words that use this kanji. Click a linked row to open its vocab entry.</p>
          <table class="kanji-examples-table">
            <tbody>${_}</tbody>
          </table>
        </section>`})()}
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
            ${n.authentic_refs.map(e=>{const d=e.split(".")[1]||"authentic";return`<li><a href="#/authentic">${a(e)}</a> <span class="muted small">(${a(d)})</span></li>`}).join("")}
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
      ${(()=>{const e=n.on_kun_pair_drill;if(!e||typeof e!="object")return"";const d=e.standalone||{},p=e.compound||{};return`
          <section class="kanji-on-kun-drill">
            <h3>${a(t("kanji_detail.on_kun_pair_drill"))}</h3>
            <table class="on-kun-drill-table">
              <thead>
                <tr><th>${a(t("kanji_detail.standalone_typically_kun"))}</th><th>${a(t("kanji_detail.compound_typically_on"))}</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <span class="form" lang="ja">${a(d.form||"")}</span>
                    <span class="reading muted small" lang="ja">${a(d.reading||"")}</span>
                    <span class="gloss">${a(d.gloss||"")}</span>
                  </td>
                  <td>
                    <span class="form" lang="ja">${a(p.form||"")}</span>
                    <span class="reading muted small" lang="ja">${a(p.reading||"")}</span>
                    <span class="gloss">${a(p.gloss||"")}</span>
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
              ${e.map(d=>{const p=String(d).split(":");return p.length!==2?`<li><span lang="ja">${a(d)}</span></li>`:`<li>
                  <span class="okurigana-kanji" lang="ja">${a(p[0])}</span><span class="okurigana-cut" aria-hidden="true">\uFE31</span><span class="okurigana-suffix" lang="ja">${a(p[1])}</span>
                </li>`}).join("")}
            </ul>
          </section>
        `:""})()}
      <nav class="kanji-nav">
        ${l?`<a href="#/kanji/${encodeURIComponent(l.glyph)}">\u2190 <span lang="ja">${a(l.glyph)}</span></a>`:"<span></span>"}
        ${c?`<a href="#/kanji/${encodeURIComponent(c.glyph)}"><span lang="ja">${a(c.glyph)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-kanji")?.addEventListener("change",e=>{j.setKanjiKnown(n.glyph,e.target.checked)})}function a(s){return String(s??"").replace(/[&<>"']/g,n=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[n])}function A(s){if(!s)return"";if(typeof s=="string")return`<p class="kanji-mnemonic">${a(s)}</p>`;if(typeof s!="object")return"";const n=s.summary||s.meaning||"",i=s.visual||"",o=s.reading||"",l=s.provenance||{},c=e=>"",u=[];return n&&u.push(`<p class="kanji-mnemonic kanji-mnemonic-summary"><strong>Meaning:</strong> ${a(n)}${c("summary")}</p>`),i&&i!==n&&u.push(`<p class="kanji-mnemonic kanji-mnemonic-visual"><strong>Visual:</strong> ${a(i)}${c("visual")}</p>`),o&&u.push(`<p class="kanji-mnemonic kanji-mnemonic-reading"><strong>Reading:</strong> ${a(o)}${c("reading")}</p>`),u.join(`
          `)}export{K as renderKanji};
