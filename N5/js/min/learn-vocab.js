import{renderJa as A}from"./furigana.js";import*as C from"./storage.js";import{esc as a,wireExpandCollapseControls as N}from"./learn.js";import{currentLocale as _,t as o}from"./i18n.js";import{renderItemBadge as T}from"./provenance-badge.js";function P(t,r){if(!t||!Number.isFinite(t.mora))return"";const i=t.mora,l=t.drop;let c="";for(let s=1;s<=i;s++)l===0?c+=s===1?"L":"H":l===1?c+=s===1?"H":"L":c+=s===1?"L":s<=l?"H":"L";return c}function V(t){return{satsu:"\u3055\u3064",dai:"\u3060\u3044",hiki:"\u3072\u304D",wa:"\u308F",mai:"\u307E\u3044",ken:"\u3051\u3093",hon:"\u307B\u3093",soku:"\u305D\u304F",ko:"\u3053",nin:"\u306B\u3093",tsu:"\u3064",kai:"\u304B\u3044",do:"\u3069",fun:"\u3075\u3093",ji:"\u3058"}[t]||t}const L={be:{humble:{ja:"\u304A\u308B",reading:"\u304A\u308B",gloss:"to exist (humble; said about self / in-group)"},respectful:{ja:"\u3044\u3089\u3063\u3057\u3083\u308B",reading:"\u3044\u3089\u3063\u3057\u3083\u308B",gloss:"to exist (respectful; said about social superiors)"},note_en:'\u3044\u308B has both humble (\u8B19\u8B72\u8A9E: \u304A\u308B) and respectful (\u5C0A\u656C\u8A9E: \u3044\u3089\u3063\u3057\u3083\u308B) keigo forms. The respectful \u3044\u3089\u3063\u3057\u3083\u308B also covers "go" and "come" (see chains go / come).'},go:{humble:{ja:"\u53C2\u308B",reading:"\u307E\u3044\u308B",gloss:"to go / come (humble)"},respectful:{ja:"\u3044\u3089\u3063\u3057\u3083\u308B",reading:"\u3044\u3089\u3063\u3057\u3083\u308B",gloss:"to go / come / be (respectful)"},note_en:'\u884C\u304F maps to humble \u53C2\u308B and respectful \u3044\u3089\u3063\u3057\u3083\u308B. The respectful \u3044\u3089\u3063\u3057\u3083\u308B is shared with "come" and "be" (one form, three meanings).'},eat:{humble:{ja:"\u3044\u305F\u3060\u304F",reading:"\u3044\u305F\u3060\u304F",gloss:"to eat / receive (humble; also said before meals as \u3044\u305F\u3060\u304D\u307E\u3059)"},respectful:{ja:"\u53EC\u3057\u4E0A\u304C\u308B",reading:"\u3081\u3057\u3042\u304C\u308B",gloss:"to eat (respectful; offered to the listener)"},note_en:'\u98DF\u3079\u308B has the humble form \u3044\u305F\u3060\u304F (also a courtesy expression before meals) and the respectful \u53EC\u3057\u4E0A\u304C\u308B (used when offering food: \u304A\u53EC\u3057\u4E0A\u304C\u308A\u304F\u3060\u3055\u3044 = "please eat").'},see:{humble:{ja:"\u62DD\u898B\u3059\u308B",reading:"\u306F\u3044\u3051\u3093\u3059\u308B",gloss:"to see / look at (humble)"},respectful:{ja:"\u3054\u89A7\u306B\u306A\u308B",reading:"\u3054\u3089\u3093\u306B\u306A\u308B",gloss:"to see / look at (respectful)"},note_en:"\u898B\u308B's humble \u62DD\u898B\u3059\u308B is used when viewing something a superior gave/showed you (e.g. \u5199\u771F\u3092\u62DD\u898B\u3057\u307E\u3057\u305F). \u5FA1\u89A7\u306B\u306A\u308B is offered to a superior (\u304A\u5199\u771F\u3092\u5FA1\u89A7\u306B\u306A\u308A\u307E\u3059\u304B)."},say:{humble:{ja:"\u7533\u3059",reading:"\u3082\u3046\u3059",gloss:"to say (humble; common in self-introductions)"},respectful:{ja:"\u304A\u3063\u3057\u3083\u308B",reading:"\u304A\u3063\u3057\u3083\u308B",gloss:"to say (respectful)"},note_en:`\u8A00\u3046's humble \u7533\u3059 appears in self-intros (\u9234\u6728\u3068\u7533\u3057\u307E\u3059 = "I am called Suzuki"). Respectful \u304A\u3063\u3057\u3083\u308B is used when quoting a superior's words (\u5148\u751F\u304C\u304A\u3063\u3057\u3083\u3063\u305F).`},do:{humble:{ja:"\u3044\u305F\u3059",reading:"\u3044\u305F\u3059",gloss:"to do (humble)"},respectful:{ja:"\u306A\u3055\u308B",reading:"\u306A\u3055\u308B",gloss:"to do (respectful)"},note_en:"\u3059\u308B maps to humble \u3044\u305F\u3059 and respectful \u306A\u3055\u308B. Common in customer-service speech: \u304A\u96FB\u8A71\u3044\u305F\u3057\u307E\u3059 (I will call) / \u4F55\u306B\u306A\u3055\u3044\u307E\u3059\u304B (what would you like)."}};function E(t){const r=L[t.register_chain_id];if(!r)return"";const i=t.form,l=t.reading||"",c=t.gloss||"",s=u=>String(u??"").replace(/[&<>"']/g,d=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[d]);return`
    <div class="keigo-chain">
      <p><strong>Keigo chain (${s(t.register_chain_id)}):</strong> this verb has humble (\u8B19\u8B72\u8A9E) and respectful (\u5C0A\u656C\u8A9E) forms used in formal Japanese.</p>
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
              <span lang="ja" class="keigo-form">${s(r.humble.ja)}</span>
              <span lang="ja" class="keigo-reading muted small">${s(r.humble.reading)}</span>
              <span class="keigo-gloss">${s(r.humble.gloss)}</span>
            </td>
            <td data-label="Plain (you are here)" class="keigo-cell-current">
              <span lang="ja" class="keigo-form">${s(i)}</span>
              <span lang="ja" class="keigo-reading muted small">${s(l)}</span>
              <span class="keigo-gloss">${s(c)}</span>
            </td>
            <td data-label="Respectful (\u5C0A\u656C\u8A9E)">
              <span lang="ja" class="keigo-form">${s(r.respectful.ja)}</span>
              <span lang="ja" class="keigo-reading muted small">${s(r.respectful.reading)}</span>
              <span class="keigo-gloss">${s(r.respectful.gloss)}</span>
            </td>
          </tr>
        </tbody>
      </table>
      <p class="muted small">${s(r.note_en)}</p>
      <p class="muted small">Humble + respectful forms are N3+ scope; shown here for awareness only \u2014 they are not yet drilled at N5.</p>
    </div>
  `}function y(t){const r=_();if(r&&r!=="en"){const i=t[`gloss_${r}`];if(typeof i=="string"&&i.trim())return i}return t.gloss||""}const j=[["People and Body",["1. People - Pronouns and Self","2. People - Family","3. People - Roles","4. Body Parts"]],["Demonstratives, Questions, Numbers, Time",["5. Demonstratives","6. Question Words","7. Numbers","8. Native Counters (\u3064-series)","9. Counters (Common)","10. Time - General","11. Time - Days, Weeks, Months, Years","12. Time - Frequency / Sequence"]],["Places and Things",["13. Locations and Places (general)","14. Nature and Weather","15. Animals","16. Food and Drink - General","17. Food - Items","18. Drinks","19. Tableware and Cooking","20. Colors","21. Clothing and Accessories","22. Money and Shopping","23. Transport","24. School and Study","25. Languages and Countries","26. House and Furniture"]],["Verbs",["27. Verbs - Group 1 (\u3046-verbs)","28. Verbs - Group 2 (\u308B-verbs)","29. Verbs - Irregular and \u3059\u308B-verbs","30. Verbs - Existence and Possession"]],["Adjectives and Function Words",["31. \u3044-Adjectives","32. \u306A-Adjectives","33. Adverbs","34. Conjunctions","35. Particles (functional vocabulary)","36. Greetings and Set Phrases"]],["Misc",["37. Common Nouns - Miscellaneous","38. Sounds and Voice","39. Function / Filler Expressions","40. Misc Useful Items"]]];function S(t){for(const[r,i]of j)if(i.includes(t))return r;return"Misc"}function I(t){const r=new Map;for(const[l]of j)r.set(l,[]);for(const l of t){const c=S(l.section||"Other");r.get(c).push(l)}const i=[];for(const[,l]of r.entries())l.sort((c,s)=>{const u=parseInt(c.section||"",10),d=parseInt(s.section||"",10);return!isNaN(u)&&!isNaN(d)&&u!==d?u-d:(c.form||"").localeCompare(s.form||"")}),i.push(...l);return i}let k="";function G(t,r){return r?[t.form||"",t.reading||"",t.gloss||"",t.section||""].join(" ").toLowerCase().includes(r):!0}function F(t,r){const i=r.entries||[],l=k.trim().toLowerCase(),s=I(i).filter(e=>G(e,l)),u=new Map;for(const[e]of j)u.set(e,[]);for(const e of s){const n=S(e.section||"Other");u.get(n).push(e)}const d=e=>e.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),b=l.length>0,m=_(),f=m&&m!=="en",v=e=>{if(!f)return"";const n=e.length;if(n===0)return"";const p=e.filter(x=>typeof x[`gloss_${m}`]=="string"&&x[`gloss_${m}`].trim()).length,g=Math.round(100*p/n);return`<span class="vocab-coverage-badge tone-${g>=50?"good":g>0?"partial":"none"}" title="${p}/${n} translated">${g}%</span>`},$=[...u.entries()].filter(([,e])=>e.length>0).map(([e,n])=>{const p=n.map(g=>`
        <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(g.form||"")}">
          <span class="vocab-form" lang="ja">${a(g.form||"")}</span>
        </a>
      `).join("");return`
        <details class="vocab-section" id="vocab-${d(e)}"${b?" open":""}>
          <summary><strong>${a(e)}</strong> <span class="muted small">(${n.length})</span> ${v(n)}</summary>
          <div class="vocab-grid">${p}</div>
        </details>
      `}).join("");t.innerHTML=`
    <article class="vocab-toc">
      <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
      <h2>Vocabulary</h2>
      <p class="page-lede">${i.length} N5 words in ${j.length} sections.</p>
      <div class="kanji-filters" role="search" aria-label="Filter vocabulary">
        <input type="search" id="vocab-filter-q" class="kanji-filter-input"
          placeholder="Search form, reading, or English (e.g. \u305F\u3079\u308B / eat / \u98F2\u3080)"
          value="${a(k)}" autocomplete="off" lang="ja"
          aria-label="Search vocabulary">
        <p class="kanji-filter-count muted small" aria-live="polite">
          Showing <strong>${s.length}</strong> of ${i.length}.
        </p>
      </div>
      <div class="toc-controls">
        <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
        <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      </div>
      ${$||'<div class="placeholder"><p>No words match the current filter.</p></div>'}
    </article>
  `,N(t,"details.vocab-section");const h=document.getElementById("vocab-filter-q");if(h){let e=!1;const n=()=>{k=h.value,F(t,r);const p=document.getElementById("vocab-filter-q");if(p){p.focus();const g=p.value;p.setSelectionRange(g.length,g.length)}};h.addEventListener("compositionstart",()=>{e=!0}),h.addEventListener("compositionend",()=>{e=!1,n()}),h.addEventListener("input",()=>{e||n()})}}function q(t,r,i,l){const c=r.entries||[];let s=c.find(e=>e.form===l);if(s||(s=c.find(e=>e.id===l)),!s&&l&&l.includes(".")){const e=l.split(".").pop();s=c.find(n=>n.form===e)}if(!s){t.innerHTML=`
      <article class="vocab-detail">
        <a class="back-link" href="#/learn/vocab">\u2190 ${a(o("vocab_detail.back_to_vocabulary"))}</a>
        <h2>Word not found</h2>
        <p>No vocab entry matches <strong lang="ja">${a(l)}</strong>. The word may live under a different form.</p>
      </article>
    `;return}const u=new Set,d=[];for(const e of i.patterns||[]){for(const n of e.examples||[]){if(!n.ja||n.ja.includes("(see ")||u.has(n.ja))continue;let p=!1;if(Array.isArray(n.vocab_ids))p=n.vocab_ids.includes(s.id);else{const g=[l];s.reading&&s.reading!==l&&g.push(s.reading),p=g.some(w=>n.ja.includes(w))}if(p&&(u.add(n.ja),d.push({ja:n.ja,en:n.translation_en,source:e.pattern}),d.length>=24))break}if(d.length>=24)break}for(const e of s.examples||[])if(e.ja&&!u.has(e.ja)&&(u.add(e.ja),d.push({ja:e.ja,en:e.translation_en,source:"Vocab catalog"}),d.length>=24))break;d.sort((e,n)=>(e.ja?.length||0)-(n.ja?.length||0));const b=d.slice(0,5),m=I(c),f=m.findIndex(e=>e.id===s.id),v=f>0?m[f-1]:null,$=f>=0&&f<m.length-1?m[f+1]:null,h=C.isVocabKnown(s.form);t.innerHTML=`
    <article class="vocab-detail">
      <a class="back-link" href="#/learn/vocab">\u2190 ${a(o("vocab_detail.back_to_vocabulary"))}</a>
      <header class="vocab-header pattern-header">
        <div>
          <p class="muted small">${a(s.section||"")}</p>
          <h2 class="vocab-form-big" lang="ja">${a(s.form)}</h2>
          ${s.reading?`<p class="vocab-reading-big" lang="ja">${a(s.reading)}</p>`:""}
          <p class="vocab-gloss-big">${a(y(s))} ${T(s,!0)}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${h?"checked":""}>
          <span>${a(o("vocab_detail.mark_as_known"))}</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">${a(o("vocab_detail.meaning"))}</h3>
        <p><strong>${_()==="en"?a(o("vocab_detail.english")):a(o("vocab_detail.meaning"))}:</strong> ${a(y(s)||"-")}</p>
        ${_()!=="en"&&s.gloss&&y(s)!==s.gloss?`<p><strong>${a(o("vocab_detail.english"))}:</strong> ${a(s.gloss)}</p>`:""}
        ${s.reading?`<p><strong>${a(o("vocab_detail.japanese_reading"))}:</strong> <span lang="ja">${a(s.reading)}</span></p>`:""}
        ${(()=>{const e=[];if(s.pitch_accent&&Number.isFinite(s.pitch_accent.mora)&&e.push(`<p><strong>${a(o("vocab_detail.pitch_accent"))}:</strong> <span class="vocab-pitch" lang="ja">${a(P(s.pitch_accent,s.reading))}</span> <span class="muted small">(drop: ${s.pitch_accent.drop})</span></p>`),s.counter&&e.push(`<p><strong>${a(o("vocab_detail.counter"))}:</strong> <span lang="ja">\u301C${a(V(s.counter))}</span></p>`),s.register&&e.push(`<p><strong>${a(o("vocab_detail.register"))}:</strong> <span class="vocab-register-tag">${a(s.register)}</span></p>`),s.transitivity&&e.push(`<p><strong>${a(o("vocab_detail.transitivity"))}:</strong> ${a(s.transitivity)}${s.pair_id?` <span class="muted small">(${a(o("vocab_detail.pair"))}: ${a(s.pair_id)})</span>`:""}</p>`),s.verb_class){const p={godan:"Godan (Group 1, u-verb)",ichidan:"Ichidan (Group 2, ru-verb)",irregular:"Irregular (Group 3 \u2014 \u3059\u308B / \u6765\u308B)"}[s.verb_class]||s.verb_class,g=s.group1_exception?' <span class="vocab-g1-exception" title="Looks like Group 2 but conjugates as Group 1 (X-6.6)">Group-1 exception</span>':"";e.push(`<p><strong>${a(o("vocab_detail.verb_class"))}:</strong> ${a(p)}${g}</p>`)}return s.register_chain_id&&L[s.register_chain_id]&&e.push(E(s)),e.join("")})()}
      </section>

      <section>
        <h3 class="section-title">${a(o("vocab_detail.example_sentences"))} ${b.length?`(${b.length})`:""}</h3>
        ${b.length?`
          <ol class="example-list">
            ${b.map(e=>`
              <li>
                <p lang="ja" class="example-ja">${A(e.ja)}</p>
                ${e.en?`<p class="translation">${a(e.en)}</p>`:""}
                ${e.source?`<p class="muted small">${a(o("vocab_detail.from_pattern"))}: <span lang="ja">${a(e.source)}</span></p>`:""}
              </li>
            `).join("")}
          </ol>
        `:`
          <p class="muted">${a(o("vocab_detail.no_examples"))}</p>
        `}
      </section>

      ${(()=>{const e=Array.isArray(s.collocations)?s.collocations.filter(n=>typeof n=="string"&&n.trim()):[];return e.length?`
          <section class="vocab-collocations">
            <h3 class="section-title">${a(o("vocab_detail.collocations"))} (${e.length})</h3>
            <ul class="collocation-list">
              ${e.map(n=>`<li class="collocation-chip" lang="ja">${a(n)}</li>`).join("")}
            </ul>
          </section>
        `:""})()}

      ${(()=>{const e=Array.isArray(s.authentic_refs)?s.authentic_refs:[];return e.length?`
          <section class="vocab-authentic-refs">
            <h3 class="section-title">Seen in the real world</h3>
            <p class="muted small">
              This word appears on these authentic Japanese cards. Click to see the original sign / menu / notice in context.
            </p>
            <ul class="authentic-ref-list">
              ${e.map(n=>{const p=n.split(".")[1]||"authentic";return`<li><a href="#/authentic" data-auth-jump="${a(n)}">${a(n)}</a> <span class="muted small">(${a(p)})</span></li>`}).join("")}
            </ul>
          </section>
        `:""})()}

      ${(()=>{const e=Array.isArray(s.false_friends)?s.false_friends:[];return e.length?`
          <section class="vocab-false-friends">
            <h3 class="section-title">${a(o("vocab_detail.false_friends"))}</h3>
            <div class="false-friend-grid">
              ${e.map(n=>`
                <a class="false-friend-card" href="#/learn/vocab/${encodeURIComponent(n)}">
                  <span lang="ja">${a(n)}</span>
                </a>
              `).join("")}
            </div>
          </section>
        `:""})()}

      ${(()=>{const e=Array.isArray(s.pragmatic_functions)?s.pragmatic_functions:[];return e.length?`
          <section class="vocab-pragmatic">
            <h3 class="section-title">${a(o("vocab_detail.pragmatic"))}</h3>
            <ul class="pragmatic-list">
              ${e.map(n=>`
                <li>
                  <strong class="pragmatic-function">${a(n.function||"")}</strong>
                  ${n.gloss?` \u2014 <span class="pragmatic-gloss">${a(n.gloss)}</span>`:""}
                  ${n.context?`<p class="muted small pragmatic-context">${a(n.context)}</p>`:""}
                </li>
              `).join("")}
            </ul>
          </section>
        `:""})()}

      ${(()=>{const e=s.devoiced_vowels;return!e||typeof e!="object"?"":`
          <section class="vocab-devoicing">
            <h3 class="section-title">${a(o("vocab_detail.devoiced_vowels"))}</h3>
            ${Array.isArray(e.positions)&&e.positions.length?`<p><strong>${a(o("vocab_detail.devoiced_position"))}:</strong> mora ${e.positions.join(", ")} (0-indexed)</p>`:`<p class="muted small">${a(o("vocab_detail.devoiced_no_dev"))}</p>`}
            ${e.note?`<p class="muted small">${a(e.note)}</p>`:""}
            ${e.rule?`<p class="muted small"><em>${a(o("vocab_detail.devoiced_rule"))}:</em> ${a(e.rule)}</p>`:""}
          </section>
        `})()}

      ${(()=>{const e=s.counter_register;return!e||typeof e!="object"?"":`
          <section class="vocab-counter-register">
            <h3 class="section-title">${a(o("vocab_detail.counter_register"))}</h3>
            ${e.counter?`<p><strong>${a(o("vocab_detail.counter_root"))}:</strong> <span lang="ja">\u301C${a(e.counter)}</span> ${e.irregular?`<span class="vocab-g1-exception" title="Irregular kun-yomi form">${a(o("vocab_detail.irregular"))}</span>`:""}</p>`:""}
            ${e.note?`<p>${a(e.note)}</p>`:""}
            ${e.register_pair?`
              <div class="register-pair-grid">
                ${e.register_pair.casual_alt?`<div><span class="muted small">${a(o("vocab_detail.casual"))}:</span> <span lang="ja">${a(e.register_pair.casual_alt)}</span></div>`:""}
                ${e.register_pair.formal_same?`<div><span class="muted small">${a(o("vocab_detail.formal"))}:</span> <span lang="ja">${a(e.register_pair.formal_same)}</span></div>`:""}
              </div>
            `:""}
          </section>
        `})()}

      <nav class="vocab-nav">
        ${v?`<a href="#/learn/vocab/${encodeURIComponent(v.form)}">\u2190 <span lang="ja">${a(v.form)}</span></a>`:"<span></span>"}
        ${$?`<a href="#/learn/vocab/${encodeURIComponent($.form)}"><span lang="ja">${a($.form)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-vocab")?.addEventListener("change",e=>{C.setVocabKnown(s.form,e.target.checked)})}export{q as renderVocabularyDetail,F as renderVocabularyList};
