import{renderJa as x}from"./furigana.js";import*as w from"./storage.js";import{esc as t,wireExpandCollapseControls as E}from"./learn.js";import{currentLocale as y}from"./i18n.js";function b(a){const o=y();if(o&&o!=="en"){const r=a[`gloss_${o}`];if(typeof r=="string"&&r.trim())return r}return a.gloss||""}const h=[["People and Body",["1. People - Pronouns and Self","2. People - Family","3. People - Roles","4. Body Parts"]],["Demonstratives, Questions, Numbers, Time",["5. Demonstratives","6. Question Words","7. Numbers","8. Native Counters (\u3064-series)","9. Counters (Common)","10. Time - General","11. Time - Days, Weeks, Months, Years","12. Time - Frequency / Sequence"]],["Places and Things",["13. Locations and Places (general)","14. Nature and Weather","15. Animals","16. Food and Drink - General","17. Food - Items","18. Drinks","19. Tableware and Cooking","20. Colors","21. Clothing and Accessories","22. Money and Shopping","23. Transport","24. School and Study","25. Languages and Countries","26. House and Furniture"]],["Verbs",["27. Verbs - Group 1 (\u3046-verbs)","28. Verbs - Group 2 (\u308B-verbs)","29. Verbs - Irregular and \u3059\u308B-verbs","30. Verbs - Existence and Possession"]],["Adjectives and Function Words",["31. \u3044-Adjectives","32. \u306A-Adjectives","33. Adverbs","34. Conjunctions","35. Particles (functional vocabulary)","36. Greetings and Set Phrases"]],["Misc",["37. Common Nouns - Miscellaneous","38. Sounds and Voice","39. Function / Filler Expressions","40. Misc Useful Items"]]];function C(a){for(const[o,r]of h)if(r.includes(a))return o;return"Misc"}function S(a){const o=new Map;for(const[l]of h)o.set(l,[]);for(const l of a){const g=C(l.section||"Other");o.get(g).push(l)}const r=[];for(const[,l]of o.entries())l.sort((g,e)=>{const p=parseInt(g.section||"",10),c=parseInt(e.section||"",10);return!isNaN(p)&&!isNaN(c)&&p!==c?p-c:(g.form||"").localeCompare(e.form||"")}),r.push(...l);return r}let j="";function M(a,o){return o?[a.form||"",a.reading||"",a.gloss||"",a.section||""].join(" ").toLowerCase().includes(o):!0}function T(a,o){const r=o.entries||[],l=j.trim().toLowerCase(),e=S(r).filter(n=>M(n,l)),p=new Map;for(const[n]of h)p.set(n,[]);for(const n of e){const i=C(n.section||"Other");p.get(i).push(n)}const c=n=>n.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),f=l.length>0,m=[...p.entries()].filter(([,n])=>n.length>0).map(([n,i])=>{const v=i.map(s=>`
        <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(s.form||"")}">
          <span class="vocab-form" lang="ja">${t(s.form||"")}</span>
          ${s.reading?`<span class="vocab-reading" lang="ja">${t(s.reading)}</span>`:""}
          <span class="vocab-gloss">${t(b(s))}</span>
        </a>
      `).join("");return`
        <details class="vocab-section" id="vocab-${c(n)}"${f?" open":""}>
          <summary><strong>${t(n)}</strong> <span class="muted small">(${i.length})</span></summary>
          <div class="vocab-grid">${v}</div>
        </details>
      `}).join("");a.innerHTML=`
    <article class="vocab-toc">
      <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
      <h2>Vocabulary</h2>
      <p class="page-lede">${r.length} N5 words in ${h.length} sections.</p>
      <div class="kanji-filters" role="search" aria-label="Filter vocabulary">
        <input type="search" id="vocab-filter-q" class="kanji-filter-input"
          placeholder="Search form, reading, or English (e.g. \u305F\u3079\u308B / eat / \u98F2\u3080)"
          value="${t(j)}" autocomplete="off" lang="ja"
          aria-label="Search vocabulary">
        <p class="kanji-filter-count muted small" aria-live="polite">
          Showing <strong>${e.length}</strong> of ${r.length}.
        </p>
      </div>
      <div class="toc-controls">
        <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
        <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      </div>
      ${m||'<div class="placeholder"><p>No words match the current filter.</p></div>'}
    </article>
  `,E(a,"details.vocab-section");const u=document.getElementById("vocab-filter-q");u&&u.addEventListener("input",()=>{j=u.value,T(a,o);const n=document.getElementById("vocab-filter-q");if(n){n.focus();const i=n.value;n.setSelectionRange(i.length,i.length)}})}function I(a,o,r,l){const g=o.entries||[],e=g.find(s=>s.form===l);if(!e){a.innerHTML=`
      <article class="vocab-detail">
        <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
        <h2>Word not found</h2>
        <p>No vocab entry matches <strong lang="ja">${t(l)}</strong>. The word may live under a different form.</p>
      </article>
    `;return}const p=new Set,c=[];for(const s of r.patterns||[]){for(const d of s.examples||[]){if(!d.ja||d.ja.includes("(see ")||p.has(d.ja))continue;let $=!1;if(Array.isArray(d.vocab_ids))$=d.vocab_ids.includes(e.id);else{const k=[l];e.reading&&e.reading!==l&&k.push(e.reading),$=k.some(V=>d.ja.includes(V))}if($&&(p.add(d.ja),c.push({ja:d.ja,en:d.translation_en,source:s.pattern}),c.length>=24))break}if(c.length>=24)break}c.sort((s,d)=>(s.ja?.length||0)-(d.ja?.length||0));const f=c.slice(0,5),m=S(g),u=m.findIndex(s=>s.id===e.id),n=u>0?m[u-1]:null,i=u>=0&&u<m.length-1?m[u+1]:null,v=w.isVocabKnown(e.form);a.innerHTML=`
    <article class="vocab-detail">
      <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
      <header class="vocab-header pattern-header">
        <div>
          <p class="muted small">${t(e.section||"")}</p>
          <h2 class="vocab-form-big" lang="ja">${t(e.form)}</h2>
          ${e.reading?`<p class="vocab-reading-big" lang="ja">${t(e.reading)}</p>`:""}
          <p class="vocab-gloss-big">${t(b(e))}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${v?"checked":""}>
          <span>Mark as known</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">Meaning</h3>
        <p><strong>${y()==="en"?"English":"Meaning"}:</strong> ${t(b(e)||"-")}</p>
        ${y()!=="en"&&e.gloss&&b(e)!==e.gloss?`<p><strong>English:</strong> ${t(e.gloss)}</p>`:""}
        ${e.reading?`<p><strong>Japanese reading:</strong> <span lang="ja">${t(e.reading)}</span></p>`:""}
      </section>

      <section>
        <h3 class="section-title">Example sentences ${f.length?`(${f.length})`:""}</h3>
        ${f.length?`
          <ol class="example-list">
            ${f.map(s=>`
              <li>
                <p lang="ja" class="example-ja">${x(s.ja)}</p>
                ${s.en?`<p class="translation">${t(s.en)}</p>`:""}
                ${s.source?`<p class="muted small">From pattern: <span lang="ja">${t(s.source)}</span></p>`:""}
              </li>
            `).join("")}
          </ol>
        `:`
          <p class="muted">No example sentences in the corpus yet for this word. Try the search bar to find phrases that include it.</p>
        `}
      </section>

      <nav class="vocab-nav">
        ${n?`<a href="#/learn/vocab/${encodeURIComponent(n.form)}">\u2190 <span lang="ja">${t(n.form)}</span></a>`:"<span></span>"}
        ${i?`<a href="#/learn/vocab/${encodeURIComponent(i.form)}"><span lang="ja">${t(i.form)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-vocab")?.addEventListener("change",s=>{w.setVocabKnown(e.form,s.target.checked)})}export{I as renderVocabularyDetail,T as renderVocabularyList};
