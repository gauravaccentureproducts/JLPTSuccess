import{renderJa as I}from"./furigana.js";import*as C from"./storage.js";import{esc as s,wireExpandCollapseControls as N}from"./learn.js";import{currentLocale as _,t as o}from"./i18n.js";import{renderItemBadge as T}from"./provenance-badge.js";function P(n,r){if(!n||!Number.isFinite(n.mora))return"";const c=n.mora,l=n.drop;let p="";for(let a=1;a<=c;a++)l===0?p+=a===1?"L":"H":l===1?p+=a===1?"H":"L":p+=a===1?"L":a<=l?"H":"L";return p}function V(n){return{satsu:"\u3055\u3064",dai:"\u3060\u3044",hiki:"\u3072\u304D",wa:"\u308F",mai:"\u307E\u3044",ken:"\u3051\u3093",hon:"\u307B\u3093",soku:"\u305D\u304F",ko:"\u3053",nin:"\u306B\u3093",tsu:"\u3064",kai:"\u304B\u3044",do:"\u3069",fun:"\u3075\u3093",ji:"\u3058"}[n]||n}const S={be:{humble:{ja:"\u304A\u308B",reading:"\u304A\u308B",gloss:"to exist (humble; said about self / in-group)"},respectful:{ja:"\u3044\u3089\u3063\u3057\u3083\u308B",reading:"\u3044\u3089\u3063\u3057\u3083\u308B",gloss:"to exist (respectful; said about social superiors)"},note_en:'\u3044\u308B has both humble (\u8B19\u8B72\u8A9E: \u304A\u308B) and respectful (\u5C0A\u656C\u8A9E: \u3044\u3089\u3063\u3057\u3083\u308B) keigo forms. The respectful \u3044\u3089\u3063\u3057\u3083\u308B also covers "go" and "come" (see chains go / come).'},go:{humble:{ja:"\u53C2\u308B",reading:"\u307E\u3044\u308B",gloss:"to go / come (humble)"},respectful:{ja:"\u3044\u3089\u3063\u3057\u3083\u308B",reading:"\u3044\u3089\u3063\u3057\u3083\u308B",gloss:"to go / come / be (respectful)"},note_en:'\u884C\u304F maps to humble \u53C2\u308B and respectful \u3044\u3089\u3063\u3057\u3083\u308B. The respectful \u3044\u3089\u3063\u3057\u3083\u308B is shared with "come" and "be" (one form, three meanings).'},eat:{humble:{ja:"\u3044\u305F\u3060\u304F",reading:"\u3044\u305F\u3060\u304F",gloss:"to eat / receive (humble; also said before meals as \u3044\u305F\u3060\u304D\u307E\u3059)"},respectful:{ja:"\u53EC\u3057\u4E0A\u304C\u308B",reading:"\u3081\u3057\u3042\u304C\u308B",gloss:"to eat (respectful; offered to the listener)"},note_en:'\u98DF\u3079\u308B has the humble form \u3044\u305F\u3060\u304F (also a courtesy expression before meals) and the respectful \u53EC\u3057\u4E0A\u304C\u308B (used when offering food: \u304A\u53EC\u3057\u4E0A\u304C\u308A\u304F\u3060\u3055\u3044 = "please eat").'},see:{humble:{ja:"\u62DD\u898B\u3059\u308B",reading:"\u306F\u3044\u3051\u3093\u3059\u308B",gloss:"to see / look at (humble)"},respectful:{ja:"\u3054\u89A7\u306B\u306A\u308B",reading:"\u3054\u3089\u3093\u306B\u306A\u308B",gloss:"to see / look at (respectful)"},note_en:"\u898B\u308B's humble \u62DD\u898B\u3059\u308B is used when viewing something a superior gave/showed you (e.g. \u5199\u771F\u3092\u62DD\u898B\u3057\u307E\u3057\u305F). \u5FA1\u89A7\u306B\u306A\u308B is offered to a superior (\u304A\u5199\u771F\u3092\u5FA1\u89A7\u306B\u306A\u308A\u307E\u3059\u304B)."},say:{humble:{ja:"\u7533\u3059",reading:"\u3082\u3046\u3059",gloss:"to say (humble; common in self-introductions)"},respectful:{ja:"\u304A\u3063\u3057\u3083\u308B",reading:"\u304A\u3063\u3057\u3083\u308B",gloss:"to say (respectful)"},note_en:`\u8A00\u3046's humble \u7533\u3059 appears in self-intros (\u9234\u6728\u3068\u7533\u3057\u307E\u3059 = "I am called Suzuki"). Respectful \u304A\u3063\u3057\u3083\u308B is used when quoting a superior's words (\u5148\u751F\u304C\u304A\u3063\u3057\u3083\u3063\u305F).`},do:{humble:{ja:"\u3044\u305F\u3059",reading:"\u3044\u305F\u3059",gloss:"to do (humble)"},respectful:{ja:"\u306A\u3055\u308B",reading:"\u306A\u3055\u308B",gloss:"to do (respectful)"},note_en:"\u3059\u308B maps to humble \u3044\u305F\u3059 and respectful \u306A\u3055\u308B. Common in customer-service speech: \u304A\u96FB\u8A71\u3044\u305F\u3057\u307E\u3059 (I will call) / \u4F55\u306B\u306A\u3055\u3044\u307E\u3059\u304B (what would you like)."}};function E(n){const r=S[n.register_chain_id];if(!r)return"";const c=n.form,l=n.reading||"",p=n.gloss||"",a=u=>String(u??"").replace(/[&<>"']/g,d=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[d]);return`
    <div class="keigo-chain">
      <p><strong>Keigo chain (${a(n.register_chain_id)}):</strong> this verb has humble (\u8B19\u8B72\u8A9E) and respectful (\u5C0A\u656C\u8A9E) forms used in formal Japanese.</p>
      <table class="keigo-chain-table" aria-label="Politeness register trio">
        <thead>
          <tr>
            <th>Humble (\u8B19\u8B72\u8A9E)</th>
            <th>Plain (you are here)</th>
            <th>Respectful (\u5C0A\u656C\u8A9E)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td data-label="Humble (\u8B19\u8B72\u8A9E)">
              <span lang="ja" class="keigo-form">${a(r.humble.ja)}</span>
              <span lang="ja" class="keigo-reading muted small">${a(r.humble.reading)}</span>
              <span class="keigo-gloss">${a(r.humble.gloss)}</span>
            </td>
            <td data-label="Plain (you are here)" class="keigo-cell-current">
              <span lang="ja" class="keigo-form">${a(c)}</span>
              <span lang="ja" class="keigo-reading muted small">${a(l)}</span>
              <span class="keigo-gloss">${a(p)}</span>
            </td>
            <td data-label="Respectful (\u5C0A\u656C\u8A9E)">
              <span lang="ja" class="keigo-form">${a(r.respectful.ja)}</span>
              <span lang="ja" class="keigo-reading muted small">${a(r.respectful.reading)}</span>
              <span class="keigo-gloss">${a(r.respectful.gloss)}</span>
            </td>
          </tr>
        </tbody>
      </table>
      <p class="muted small">${a(r.note_en)}</p>
      <p class="muted small">Humble + respectful forms are N3+ scope; shown here for awareness only \u2014 they are not yet drilled at N5.</p>
    </div>
  `}function y(n){const r=_();if(r&&r!=="en"){const c=n[`gloss_${r}`];if(typeof c=="string"&&c.trim())return c}return n.gloss||""}const j=[["People and Body",["1. People - Pronouns and Self","2. People - Family","3. People - Roles","4. Body Parts"]],["Demonstratives, Questions, Numbers, Time",["5. Demonstratives","6. Question Words","7. Numbers","8. Native Counters (\u3064-series)","9. Counters (Common)","10. Time - General","11. Time - Days, Weeks, Months, Years","12. Time - Frequency / Sequence"]],["Places and Things",["13. Locations and Places (general)","14. Nature and Weather","15. Animals","16. Food and Drink - General","17. Food - Items","18. Drinks","19. Tableware and Cooking","20. Colors","21. Clothing and Accessories","22. Money and Shopping","23. Transport","24. School and Study","25. Languages and Countries","26. House and Furniture"]],["Verbs",["27. Verbs - Group 1 (\u3046-verbs)","28. Verbs - Group 2 (\u308B-verbs)","29. Verbs - Irregular and \u3059\u308B-verbs","30. Verbs - Existence and Possession"]],["Adjectives and Function Words",["31. \u3044-Adjectives","32. \u306A-Adjectives","33. Adverbs","34. Conjunctions","35. Particles (functional vocabulary)","36. Greetings and Set Phrases"]],["Misc",["37. Common Nouns - Miscellaneous","38. Sounds and Voice","39. Function / Filler Expressions","40. Misc Useful Items"]]];function L(n){for(const[r,c]of j)if(c.includes(n))return r;return"Misc"}function A(n){const r=new Map;for(const[l]of j)r.set(l,[]);for(const l of n){const p=L(l.section||"Other");r.get(p).push(l)}const c=[];for(const[,l]of r.entries())l.sort((p,a)=>{const u=parseInt(p.section||"",10),d=parseInt(a.section||"",10);return!isNaN(u)&&!isNaN(d)&&u!==d?u-d:(p.form||"").localeCompare(a.form||"")}),c.push(...l);return c}let k="";function G(n,r){return r?[n.form||"",n.reading||"",n.gloss||"",n.section||""].join(" ").toLowerCase().includes(r):!0}function F(n,r){const c=r.entries||[],l=k.trim().toLowerCase(),a=A(c).filter(e=>G(e,l)),u=new Map;for(const[e]of j)u.set(e,[]);for(const e of a){const t=L(e.section||"Other");u.get(t).push(e)}const d=e=>e.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),b=l.length>0,m=_(),f=m&&m!=="en",v=e=>{if(!f)return"";const t=e.length;if(t===0)return"";const i=e.filter(x=>typeof x[`gloss_${m}`]=="string"&&x[`gloss_${m}`].trim()).length,g=Math.round(100*i/t);return`<span class="vocab-coverage-badge tone-${g>=50?"good":g>0?"partial":"none"}" title="${i}/${t} translated">${g}%</span>`},$=[...u.entries()].filter(([,e])=>e.length>0).map(([e,t])=>{const i=t.map(g=>`
        <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(g.form||"")}">
          <span class="vocab-form" lang="ja">${s(g.form||"")}</span>
        </a>
      `).join("");return`
        <details class="vocab-section" id="vocab-${d(e)}"${b?" open":""}>
          <summary><strong>${s(e)}</strong> <span class="muted small">(${t.length})</span> ${v(t)}</summary>
          <div class="vocab-grid">${i}</div>
        </details>
      `}).join("");n.innerHTML=`
    <article class="vocab-toc">
      <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
      <h2>Vocabulary</h2>
      <p class="page-lede">${c.length} N5 words in ${j.length} sections.</p>
      <div class="kanji-filters" role="search" aria-label="Filter vocabulary">
        <input type="search" id="vocab-filter-q" class="kanji-filter-input"
          placeholder="Search form, reading, or English (e.g. \u305F\u3079\u308B / eat / \u98F2\u3080)"
          value="${s(k)}" autocomplete="off" lang="ja"
          aria-label="Search vocabulary">
        <p class="kanji-filter-count muted small" aria-live="polite">
          Showing <strong>${a.length}</strong> of ${c.length}.
        </p>
      </div>
      <div class="toc-controls">
        <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
        <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      </div>
      ${$||'<div class="placeholder"><p>No words match the current filter.</p></div>'}
    </article>
  `,N(n,"details.vocab-section");const h=document.getElementById("vocab-filter-q");if(h){let e=!1;const t=()=>{k=h.value,F(n,r);const i=document.getElementById("vocab-filter-q");if(i){i.focus();const g=i.value;i.setSelectionRange(g.length,g.length)}};h.addEventListener("compositionstart",()=>{e=!0}),h.addEventListener("compositionend",()=>{e=!1,t()}),h.addEventListener("input",()=>{e||t()})}}function q(n,r,c,l){const p=r.entries||[];let a=p.find(e=>e.form===l);if(a||(a=p.find(e=>e.id===l)),!a&&l&&l.includes(".")){const e=l.split(".").pop();a=p.find(t=>t.form===e)}if(!a){n.innerHTML=`
      <article class="vocab-detail">
        <a class="back-link" href="#/learn/vocab">\u2190 ${s(o("vocab_detail.back_to_vocabulary"))}</a>
        <h2>Word not found</h2>
        <p>No vocab entry matches <strong lang="ja">${s(l)}</strong>. The word may live under a different form.</p>
      </article>
    `;return}const u=new Set,d=[];for(const e of c.patterns||[]){for(const t of e.examples||[]){if(!t.ja||t.ja.includes("(see ")||u.has(t.ja))continue;let i=!1;if(Array.isArray(t.vocab_ids))i=t.vocab_ids.includes(a.id);else{const g=[l];a.reading&&a.reading!==l&&g.push(a.reading),i=g.some(w=>t.ja.includes(w))}if(i&&(u.add(t.ja),d.push({ja:t.ja,en:t.translation_en,source:e.pattern}),d.length>=24))break}if(d.length>=24)break}for(const e of a.examples||[])if(e.ja&&!u.has(e.ja)&&(u.add(e.ja),d.push({ja:e.ja,en:e.translation_en,source:"Vocab catalog"}),d.length>=24))break;d.sort((e,t)=>(e.ja?.length||0)-(t.ja?.length||0));const b=d.slice(0,5),m=A(p),f=m.findIndex(e=>e.id===a.id),v=f>0?m[f-1]:null,$=f>=0&&f<m.length-1?m[f+1]:null,h=C.isVocabKnown(a.form);n.innerHTML=`
    <article class="vocab-detail">
      <a class="back-link" href="#/learn/vocab">\u2190 ${s(o("vocab_detail.back_to_vocabulary"))}</a>
      <header class="vocab-header pattern-header">
        <div>
          <p class="muted small">${s(a.section||"")}</p>
          <h2 class="vocab-form-big" lang="ja">${s(a.form)}</h2>
          ${a.reading?`<p class="vocab-reading-big" lang="ja">${s(a.reading)}</p>`:""}
          <p class="vocab-gloss-big">${s(y(a))} ${T(a,!0)}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${h?"checked":""}>
          <span>${s(o("vocab_detail.mark_as_known"))}</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">${s(o("vocab_detail.meaning"))}</h3>
        <p><strong>${_()==="en"?s(o("vocab_detail.english")):s(o("vocab_detail.meaning"))}:</strong> ${s(y(a)||"-")}</p>
        ${_()!=="en"&&a.gloss&&y(a)!==a.gloss?`<p><strong>${s(o("vocab_detail.english"))}:</strong> ${s(a.gloss)}</p>`:""}
        ${a.reading?`<p><strong>${s(o("vocab_detail.japanese_reading"))}:</strong> <span lang="ja">${s(a.reading)}</span></p>`:""}
        ${(()=>{const e=[];if(a.pitch_accent&&Number.isFinite(a.pitch_accent.mora)&&e.push(`<p><strong>${s(o("vocab_detail.pitch_accent"))}:</strong> <span class="vocab-pitch" lang="ja">${s(P(a.pitch_accent,a.reading))}</span> <span class="muted small">(drop: ${a.pitch_accent.drop})</span></p>`),a.counter&&e.push(`<p><strong>${s(o("vocab_detail.counter"))}:</strong> <span lang="ja">\u301C${s(V(a.counter))}</span></p>`),a.register&&e.push(`<p><strong>${s(o("vocab_detail.register"))}:</strong> <span class="vocab-register-tag">${s(a.register)}</span></p>`),a.transitivity&&e.push(`<p><strong>${s(o("vocab_detail.transitivity"))}:</strong> ${s(a.transitivity)}${a.pair_id?` <span class="muted small">(${s(o("vocab_detail.pair"))}: ${s(a.pair_id)})</span>`:""}</p>`),a.verb_class){const i={godan:"Godan (Group 1, u-verb)",ichidan:"Ichidan (Group 2, ru-verb)",irregular:"Irregular (Group 3 \u2014 \u3059\u308B / \u6765\u308B)"}[a.verb_class]||a.verb_class,g=a.group1_exception?' <span class="vocab-g1-exception" title="Looks like Group 2 but conjugates as Group 1 (X-6.6)">Group-1 exception</span>':"";e.push(`<p><strong>${s(o("vocab_detail.verb_class"))}:</strong> ${s(i)}${g}</p>`)}return a.register_chain_id&&S[a.register_chain_id]&&e.push(E(a)),e.join("")})()}
      </section>

      <section>
        <h3 class="section-title">${s(o("vocab_detail.example_sentences"))} ${b.length?`(${b.length})`:""}</h3>
        ${b.length?`
          <ol class="example-list">
            ${b.map(e=>`
              <li>
                <p lang="ja" class="example-ja">${I(e.ja)}</p>
                ${e.en?`<p class="translation">${s(e.en)}</p>`:""}
                ${e.source?`<p class="muted small">${s(o("vocab_detail.from_pattern"))}: <span lang="ja">${s(e.source)}</span></p>`:""}
              </li>
            `).join("")}
          </ol>
        `:`
          <p class="muted">${s(o("vocab_detail.no_examples"))}</p>
        `}
      </section>

      ${(()=>{const t=(Array.isArray(a.particle_examples)?a.particle_examples:Array.isArray(a.collocations)?a.collocations:[]).filter(i=>typeof i=="string"&&i.trim());return t.length?`
          <section class="vocab-particle-examples">
            <h3 class="section-title">${s(o("vocab_detail.particle_examples"))} (${t.length})</h3>
            <ul class="particle-example-list">
              ${t.map(i=>`<li class="particle-example-chip" lang="ja">${s(i)}</li>`).join("")}
            </ul>
          </section>
        `:""})()}

      ${(()=>{const e=Array.isArray(a.authentic_refs)?a.authentic_refs:[];return e.length?`
          <section class="vocab-authentic-refs">
            <h3 class="section-title">Seen in the real world</h3>
            <p class="muted small">
              This word appears on these authentic Japanese cards. Click to see the original sign / menu / notice in context.
            </p>
            <ul class="authentic-ref-list">
              ${e.map(t=>{const i=t.split(".")[1]||"authentic";return`<li><a href="#/authentic" data-auth-jump="${s(t)}">${s(t)}</a> <span class="muted small">(${s(i)})</span></li>`}).join("")}
            </ul>
          </section>
        `:""})()}

      ${(()=>{const e=Array.isArray(a.false_friends)?a.false_friends:[];return e.length?`
          <section class="vocab-false-friends">
            <h3 class="section-title">${s(o("vocab_detail.false_friends"))}</h3>
            <div class="false-friend-grid">
              ${e.map(t=>`
                <a class="false-friend-card" href="#/learn/vocab/${encodeURIComponent(t)}">
                  <span lang="ja">${s(t)}</span>
                </a>
              `).join("")}
            </div>
          </section>
        `:""})()}

      ${(()=>{const e=Array.isArray(a.pragmatic_functions)?a.pragmatic_functions:[];return e.length?`
          <section class="vocab-pragmatic">
            <h3 class="section-title">${s(o("vocab_detail.pragmatic"))}</h3>
            <ul class="pragmatic-list">
              ${e.map(t=>`
                <li>
                  <strong class="pragmatic-function">${s(t.function||"")}</strong>
                  ${t.gloss?` \u2014 <span class="pragmatic-gloss">${s(t.gloss)}</span>`:""}
                  ${t.context?`<p class="muted small pragmatic-context">${s(t.context)}</p>`:""}
                </li>
              `).join("")}
            </ul>
          </section>
        `:""})()}

      ${(()=>{const e=a.devoiced_vowels;return!e||typeof e!="object"?"":`
          <section class="vocab-devoicing">
            <h3 class="section-title">${s(o("vocab_detail.devoiced_vowels"))}</h3>
            ${Array.isArray(e.positions)&&e.positions.length?`<p><strong>${s(o("vocab_detail.devoiced_position"))}:</strong> mora ${e.positions.join(", ")} (0-indexed)</p>`:`<p class="muted small">${s(o("vocab_detail.devoiced_no_dev"))}</p>`}
            ${e.note?`<p class="muted small">${s(e.note)}</p>`:""}
            ${e.rule?`<p class="muted small"><em>${s(o("vocab_detail.devoiced_rule"))}:</em> ${s(e.rule)}</p>`:""}
          </section>
        `})()}

      ${(()=>{const e=a.counter_register;return!e||typeof e!="object"?"":`
          <section class="vocab-counter-register">
            <h3 class="section-title">${s(o("vocab_detail.counter_register"))}</h3>
            ${e.counter?`<p><strong>${s(o("vocab_detail.counter_root"))}:</strong> <span lang="ja">\u301C${s(e.counter)}</span> ${e.irregular?`<span class="vocab-g1-exception" title="Irregular kun-yomi form">${s(o("vocab_detail.irregular"))}</span>`:""}</p>`:""}
            ${e.note?`<p>${s(e.note)}</p>`:""}
            ${e.register_pair?`
              <div class="register-pair-grid">
                ${e.register_pair.casual_alt?`<div><span class="muted small">${s(o("vocab_detail.casual"))}:</span> <span lang="ja">${s(e.register_pair.casual_alt)}</span></div>`:""}
                ${e.register_pair.formal_same?`<div><span class="muted small">${s(o("vocab_detail.formal"))}:</span> <span lang="ja">${s(e.register_pair.formal_same)}</span></div>`:""}
              </div>
            `:""}
          </section>
        `})()}

      <nav class="vocab-nav">
        ${v?`<a href="#/learn/vocab/${encodeURIComponent(v.form)}">\u2190 <span lang="ja">${s(v.form)}</span></a>`:"<span></span>"}
        ${$?`<a href="#/learn/vocab/${encodeURIComponent($.form)}"><span lang="ja">${s($.form)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-vocab")?.addEventListener("change",e=>{C.setVocabKnown(a.form,e.target.checked)})}export{q as renderVocabularyDetail,F as renderVocabularyList};
