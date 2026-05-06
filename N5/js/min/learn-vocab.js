import{renderJa as I}from"./furigana.js";import*as C from"./storage.js";import{esc as r,wireExpandCollapseControls as V}from"./learn.js";import{currentLocale as $}from"./i18n.js";import{renderItemBadge as N}from"./provenance-badge.js";function T(a,n){if(!a||!Number.isFinite(a.mora))return"";const l=a.mora,t=a.drop;let i="";for(let e=1;e<=l;e++)t===0?i+=e===1?"L":"H":t===1?i+=e===1?"H":"L":i+=e===1?"L":e<=t?"H":"L";return i}function P(a){return{satsu:"\u3055\u3064",dai:"\u3060\u3044",hiki:"\u3072\u304D",wa:"\u308F",mai:"\u307E\u3044",ken:"\u3051\u3093",hon:"\u307B\u3093",soku:"\u305D\u304F",ko:"\u3053",nin:"\u306B\u3093",tsu:"\u3064",kai:"\u304B\u3044",do:"\u3069",fun:"\u3075\u3093",ji:"\u3058"}[a]||a}const x={be:{humble:{ja:"\u304A\u308B",reading:"\u304A\u308B",gloss:"to exist (humble; said about self / in-group)"},respectful:{ja:"\u3044\u3089\u3063\u3057\u3083\u308B",reading:"\u3044\u3089\u3063\u3057\u3083\u308B",gloss:"to exist (respectful; said about social superiors)"},note_en:'\u3044\u308B has both humble (\u8B19\u8B72\u8A9E: \u304A\u308B) and respectful (\u5C0A\u656C\u8A9E: \u3044\u3089\u3063\u3057\u3083\u308B) keigo forms. The respectful \u3044\u3089\u3063\u3057\u3083\u308B also covers "go" and "come" (see chains go / come).'},go:{humble:{ja:"\u53C2\u308B",reading:"\u307E\u3044\u308B",gloss:"to go / come (humble)"},respectful:{ja:"\u3044\u3089\u3063\u3057\u3083\u308B",reading:"\u3044\u3089\u3063\u3057\u3083\u308B",gloss:"to go / come / be (respectful)"},note_en:'\u884C\u304F maps to humble \u53C2\u308B and respectful \u3044\u3089\u3063\u3057\u3083\u308B. The respectful \u3044\u3089\u3063\u3057\u3083\u308B is shared with "come" and "be" (one form, three meanings).'},eat:{humble:{ja:"\u3044\u305F\u3060\u304F",reading:"\u3044\u305F\u3060\u304F",gloss:"to eat / receive (humble; also said before meals as \u3044\u305F\u3060\u304D\u307E\u3059)"},respectful:{ja:"\u53EC\u3057\u4E0A\u304C\u308B",reading:"\u3081\u3057\u3042\u304C\u308B",gloss:"to eat (respectful; offered to the listener)"},note_en:'\u98DF\u3079\u308B has the humble form \u3044\u305F\u3060\u304F (also a courtesy expression before meals) and the respectful \u53EC\u3057\u4E0A\u304C\u308B (used when offering food: \u304A\u53EC\u3057\u4E0A\u304C\u308A\u304F\u3060\u3055\u3044 = "please eat").'},see:{humble:{ja:"\u62DD\u898B\u3059\u308B",reading:"\u306F\u3044\u3051\u3093\u3059\u308B",gloss:"to see / look at (humble)"},respectful:{ja:"\u3054\u89A7\u306B\u306A\u308B",reading:"\u3054\u3089\u3093\u306B\u306A\u308B",gloss:"to see / look at (respectful)"},note_en:"\u898B\u308B's humble \u62DD\u898B\u3059\u308B is used when viewing something a superior gave/showed you (e.g. \u5199\u771F\u3092\u62DD\u898B\u3057\u307E\u3057\u305F). \u5FA1\u89A7\u306B\u306A\u308B is offered to a superior (\u304A\u5199\u771F\u3092\u5FA1\u89A7\u306B\u306A\u308A\u307E\u3059\u304B)."},say:{humble:{ja:"\u7533\u3059",reading:"\u3082\u3046\u3059",gloss:"to say (humble; common in self-introductions)"},respectful:{ja:"\u304A\u3063\u3057\u3083\u308B",reading:"\u304A\u3063\u3057\u3083\u308B",gloss:"to say (respectful)"},note_en:`\u8A00\u3046's humble \u7533\u3059 appears in self-intros (\u9234\u6728\u3068\u7533\u3057\u307E\u3059 = "I am called Suzuki"). Respectful \u304A\u3063\u3057\u3083\u308B is used when quoting a superior's words (\u5148\u751F\u304C\u304A\u3063\u3057\u3083\u3063\u305F).`},do:{humble:{ja:"\u3044\u305F\u3059",reading:"\u3044\u305F\u3059",gloss:"to do (humble)"},respectful:{ja:"\u306A\u3055\u308B",reading:"\u306A\u3055\u308B",gloss:"to do (respectful)"},note_en:"\u3059\u308B maps to humble \u3044\u305F\u3059 and respectful \u306A\u3055\u308B. Common in customer-service speech: \u304A\u96FB\u8A71\u3044\u305F\u3057\u307E\u3059 (I will call) / \u4F55\u306B\u306A\u3055\u3044\u307E\u3059\u304B (what would you like)."}};function E(a){const n=x[a.register_chain_id];if(!n)return"";const l=a.form,t=a.reading||"",i=a.gloss||"",e=p=>String(p??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);return`
    <div class="keigo-chain">
      <p><strong>Keigo chain (${e(a.register_chain_id)}):</strong> this verb has humble (\u8B19\u8B72\u8A9E) and respectful (\u5C0A\u656C\u8A9E) forms used in formal Japanese.</p>
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
              <span lang="ja" class="keigo-form">${e(n.humble.ja)}</span>
              <span lang="ja" class="keigo-reading muted small">${e(n.humble.reading)}</span>
              <span class="keigo-gloss">${e(n.humble.gloss)}</span>
            </td>
            <td data-label="Plain (you are here)" class="keigo-cell-current">
              <span lang="ja" class="keigo-form">${e(l)}</span>
              <span lang="ja" class="keigo-reading muted small">${e(t)}</span>
              <span class="keigo-gloss">${e(i)}</span>
            </td>
            <td data-label="Respectful (\u5C0A\u656C\u8A9E)">
              <span lang="ja" class="keigo-form">${e(n.respectful.ja)}</span>
              <span lang="ja" class="keigo-reading muted small">${e(n.respectful.reading)}</span>
              <span class="keigo-gloss">${e(n.respectful.gloss)}</span>
            </td>
          </tr>
        </tbody>
      </table>
      <p class="muted small">${e(n.note_en)}</p>
      <p class="muted small">Humble + respectful forms are N3+ scope; shown here for awareness only \u2014 they are not yet drilled at N5.</p>
    </div>
  `}function k(a){const n=$();if(n&&n!=="en"){const l=a[`gloss_${n}`];if(typeof l=="string"&&l.trim())return l}return a.gloss||""}const j=[["People and Body",["1. People - Pronouns and Self","2. People - Family","3. People - Roles","4. Body Parts"]],["Demonstratives, Questions, Numbers, Time",["5. Demonstratives","6. Question Words","7. Numbers","8. Native Counters (\u3064-series)","9. Counters (Common)","10. Time - General","11. Time - Days, Weeks, Months, Years","12. Time - Frequency / Sequence"]],["Places and Things",["13. Locations and Places (general)","14. Nature and Weather","15. Animals","16. Food and Drink - General","17. Food - Items","18. Drinks","19. Tableware and Cooking","20. Colors","21. Clothing and Accessories","22. Money and Shopping","23. Transport","24. School and Study","25. Languages and Countries","26. House and Furniture"]],["Verbs",["27. Verbs - Group 1 (\u3046-verbs)","28. Verbs - Group 2 (\u308B-verbs)","29. Verbs - Irregular and \u3059\u308B-verbs","30. Verbs - Existence and Possession"]],["Adjectives and Function Words",["31. \u3044-Adjectives","32. \u306A-Adjectives","33. Adverbs","34. Conjunctions","35. Particles (functional vocabulary)","36. Greetings and Set Phrases"]],["Misc",["37. Common Nouns - Miscellaneous","38. Sounds and Voice","39. Function / Filler Expressions","40. Misc Useful Items"]]];function S(a){for(const[n,l]of j)if(l.includes(a))return n;return"Misc"}function L(a){const n=new Map;for(const[t]of j)n.set(t,[]);for(const t of a){const i=S(t.section||"Other");n.get(i).push(t)}const l=[];for(const[,t]of n.entries())t.sort((i,e)=>{const p=parseInt(i.section||"",10),c=parseInt(e.section||"",10);return!isNaN(p)&&!isNaN(c)&&p!==c?p-c:(i.form||"").localeCompare(e.form||"")}),l.push(...t);return l}let y="";function M(a,n){return n?[a.form||"",a.reading||"",a.gloss||"",a.section||""].join(" ").toLowerCase().includes(n):!0}function F(a,n){const l=n.entries||[],t=y.trim().toLowerCase(),e=L(l).filter(s=>M(s,t)),p=new Map;for(const[s]of j)p.set(s,[]);for(const s of e){const o=S(s.section||"Other");p.get(o).push(s)}const c=s=>s.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),m=t.length>0,g=$(),h=g&&g!=="en",f=s=>{if(!h)return"";const o=s.length;if(o===0)return"";const d=s.filter(w=>typeof w[`gloss_${g}`]=="string"&&w[`gloss_${g}`].trim()).length,u=Math.round(100*d/o);return`<span class="vocab-coverage-badge tone-${u>=50?"good":u>0?"partial":"none"}" title="${d}/${o} translated">${u}%</span>`},b=[...p.entries()].filter(([,s])=>s.length>0).map(([s,o])=>{const d=o.map(u=>`
        <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(u.form||"")}">
          <span class="vocab-form" lang="ja">${r(u.form||"")}</span>
        </a>
      `).join("");return`
        <details class="vocab-section" id="vocab-${c(s)}"${m?" open":""}>
          <summary><strong>${r(s)}</strong> <span class="muted small">(${o.length})</span> ${f(o)}</summary>
          <div class="vocab-grid">${d}</div>
        </details>
      `}).join("");a.innerHTML=`
    <article class="vocab-toc">
      <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
      <h2>Vocabulary</h2>
      <p class="page-lede">${l.length} N5 words in ${j.length} sections.</p>
      <div class="kanji-filters" role="search" aria-label="Filter vocabulary">
        <input type="search" id="vocab-filter-q" class="kanji-filter-input"
          placeholder="Search form, reading, or English (e.g. \u305F\u3079\u308B / eat / \u98F2\u3080)"
          value="${r(y)}" autocomplete="off" lang="ja"
          aria-label="Search vocabulary">
        <p class="kanji-filter-count muted small" aria-live="polite">
          Showing <strong>${e.length}</strong> of ${l.length}.
        </p>
      </div>
      <div class="toc-controls">
        <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
        <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      </div>
      ${b||'<div class="placeholder"><p>No words match the current filter.</p></div>'}
    </article>
  `,V(a,"details.vocab-section");const v=document.getElementById("vocab-filter-q");v&&v.addEventListener("input",()=>{y=v.value,F(a,n);const s=document.getElementById("vocab-filter-q");if(s){s.focus();const o=s.value;s.setSelectionRange(o.length,o.length)}})}function B(a,n,l,t){const i=n.entries||[],e=i.find(s=>s.form===t);if(!e){a.innerHTML=`
      <article class="vocab-detail">
        <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
        <h2>Word not found</h2>
        <p>No vocab entry matches <strong lang="ja">${r(t)}</strong>. The word may live under a different form.</p>
      </article>
    `;return}const p=new Set,c=[];for(const s of l.patterns||[]){for(const o of s.examples||[]){if(!o.ja||o.ja.includes("(see ")||p.has(o.ja))continue;let d=!1;if(Array.isArray(o.vocab_ids))d=o.vocab_ids.includes(e.id);else{const u=[t];e.reading&&e.reading!==t&&u.push(e.reading),d=u.some(_=>o.ja.includes(_))}if(d&&(p.add(o.ja),c.push({ja:o.ja,en:o.translation_en,source:s.pattern}),c.length>=24))break}if(c.length>=24)break}for(const s of e.examples||[])if(s.ja&&!p.has(s.ja)&&(p.add(s.ja),c.push({ja:s.ja,en:s.translation_en,source:"Vocab catalog"}),c.length>=24))break;c.sort((s,o)=>(s.ja?.length||0)-(o.ja?.length||0));const m=c.slice(0,5),g=L(i),h=g.findIndex(s=>s.id===e.id),f=h>0?g[h-1]:null,b=h>=0&&h<g.length-1?g[h+1]:null,v=C.isVocabKnown(e.form);a.innerHTML=`
    <article class="vocab-detail">
      <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
      <header class="vocab-header pattern-header">
        <div>
          <p class="muted small">${r(e.section||"")}</p>
          <h2 class="vocab-form-big" lang="ja">${r(e.form)}</h2>
          ${e.reading?`<p class="vocab-reading-big" lang="ja">${r(e.reading)}</p>`:""}
          <p class="vocab-gloss-big">${r(k(e))} ${N(e,!0)}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${v?"checked":""}>
          <span>Mark as known</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">Meaning</h3>
        <p><strong>${$()==="en"?"English":"Meaning"}:</strong> ${r(k(e)||"-")}</p>
        ${$()!=="en"&&e.gloss&&k(e)!==e.gloss?`<p><strong>English:</strong> ${r(e.gloss)}</p>`:""}
        ${e.reading?`<p><strong>Japanese reading:</strong> <span lang="ja">${r(e.reading)}</span></p>`:""}
        ${(()=>{const s=[];if(e.pitch_accent&&Number.isFinite(e.pitch_accent.mora)&&s.push(`<p><strong>Pitch accent:</strong> <span class="vocab-pitch" lang="ja">${r(T(e.pitch_accent,e.reading))}</span> <span class="muted small">(drop: ${e.pitch_accent.drop})</span></p>`),e.counter&&s.push(`<p><strong>Counter:</strong> <span lang="ja">\u301C${r(P(e.counter))}</span></p>`),e.register&&s.push(`<p><strong>Register:</strong> <span class="vocab-register-tag">${r(e.register)}</span></p>`),e.transitivity&&s.push(`<p><strong>Transitivity:</strong> ${r(e.transitivity)}${e.pair_id?` <span class="muted small">(pair: ${r(e.pair_id)})</span>`:""}</p>`),e.verb_class){const d={godan:"Godan (Group 1, u-verb)",ichidan:"Ichidan (Group 2, ru-verb)",irregular:"Irregular (Group 3 \u2014 \u3059\u308B / \u6765\u308B)"}[e.verb_class]||e.verb_class,u=e.group1_exception?' <span class="vocab-g1-exception" title="Looks like Group 2 but conjugates as Group 1 (X-6.6)">Group-1 exception</span>':"";s.push(`<p><strong>Verb class:</strong> ${r(d)}${u}</p>`)}return e.register_chain_id&&x[e.register_chain_id]&&s.push(E(e)),s.join("")})()}
      </section>

      <section>
        <h3 class="section-title">Example sentences ${m.length?`(${m.length})`:""}</h3>
        ${m.length?`
          <ol class="example-list">
            ${m.map(s=>`
              <li>
                <p lang="ja" class="example-ja">${I(s.ja)}</p>
                ${s.en?`<p class="translation">${r(s.en)}</p>`:""}
                ${s.source?`<p class="muted small">From pattern: <span lang="ja">${r(s.source)}</span></p>`:""}
              </li>
            `).join("")}
          </ol>
        `:`
          <p class="muted">No example sentences in the corpus yet for this word. Try the search bar to find phrases that include it.</p>
        `}
      </section>

      <nav class="vocab-nav">
        ${f?`<a href="#/learn/vocab/${encodeURIComponent(f.form)}">\u2190 <span lang="ja">${r(f.form)}</span></a>`:"<span></span>"}
        ${b?`<a href="#/learn/vocab/${encodeURIComponent(b.form)}"><span lang="ja">${r(b.form)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-vocab")?.addEventListener("change",s=>{C.setVocabKnown(e.form,s.target.checked)})}export{B as renderVocabularyDetail,F as renderVocabularyList};
