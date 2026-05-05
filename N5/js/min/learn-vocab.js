import{renderJa as S}from"./furigana.js";import*as j from"./storage.js";import{esc as s,wireExpandCollapseControls as V}from"./learn.js";const b=[["People and Body",["1. People - Pronouns and Self","2. People - Family","3. People - Roles","4. Body Parts"]],["Demonstratives, Questions, Numbers, Time",["5. Demonstratives","6. Question Words","7. Numbers","8. Native Counters (\u3064-series)","9. Counters (Common)","10. Time - General","11. Time - Days, Weeks, Months, Years","12. Time - Frequency / Sequence"]],["Places and Things",["13. Locations and Places (general)","14. Nature and Weather","15. Animals","16. Food and Drink - General","17. Food - Items","18. Drinks","19. Tableware and Cooking","20. Colors","21. Clothing and Accessories","22. Money and Shopping","23. Transport","24. School and Study","25. Languages and Countries","26. House and Furniture"]],["Verbs",["27. Verbs - Group 1 (\u3046-verbs)","28. Verbs - Group 2 (\u308B-verbs)","29. Verbs - Irregular and \u3059\u308B-verbs","30. Verbs - Existence and Possession"]],["Adjectives and Function Words",["31. \u3044-Adjectives","32. \u306A-Adjectives","33. Adverbs","34. Conjunctions","35. Particles (functional vocabulary)","36. Greetings and Set Phrases"]],["Misc",["37. Common Nouns - Miscellaneous","38. Sounds and Voice","39. Function / Filler Expressions","40. Misc Useful Items"]]];function k(o){for(const[r,l]of b)if(l.includes(o))return r;return"Misc"}function w(o){const r=new Map;for(const[t]of b)r.set(t,[]);for(const t of o){const g=k(t.section||"Other");r.get(g).push(t)}const l=[];for(const[,t]of r.entries())t.sort((g,e)=>{const p=parseInt(g.section||"",10),c=parseInt(e.section||"",10);return!isNaN(p)&&!isNaN(c)&&p!==c?p-c:(g.form||"").localeCompare(e.form||"")}),l.push(...t);return l}let $="";function x(o,r){return r?[o.form||"",o.reading||"",o.gloss||"",o.section||""].join(" ").toLowerCase().includes(r):!0}function T(o,r){const l=r.entries||[],t=$.trim().toLowerCase(),e=w(l).filter(n=>x(n,t)),p=new Map;for(const[n]of b)p.set(n,[]);for(const n of e){const i=k(n.section||"Other");p.get(i).push(n)}const c=n=>n.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),f=t.length>0,m=[...p.entries()].filter(([,n])=>n.length>0).map(([n,i])=>{const h=i.map(a=>`
        <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(a.form||"")}">
          <span class="vocab-form" lang="ja">${s(a.form||"")}</span>
          ${a.reading?`<span class="vocab-reading" lang="ja">${s(a.reading)}</span>`:""}
          <span class="vocab-gloss">${s(a.gloss||"")}</span>
        </a>
      `).join("");return`
        <details class="vocab-section" id="vocab-${c(n)}"${f?" open":""}>
          <summary><strong>${s(n)}</strong> <span class="muted small">(${i.length})</span></summary>
          <div class="vocab-grid">${h}</div>
        </details>
      `}).join("");o.innerHTML=`
    <article class="vocab-toc">
      <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
      <h2>Vocabulary</h2>
      <p class="page-lede">${l.length} N5 words in ${b.length} sections.</p>
      <div class="kanji-filters" role="search" aria-label="Filter vocabulary">
        <input type="search" id="vocab-filter-q" class="kanji-filter-input"
          placeholder="Search form, reading, or English (e.g. \u305F\u3079\u308B / eat / \u98F2\u3080)"
          value="${s($)}" autocomplete="off" lang="ja"
          aria-label="Search vocabulary">
        <p class="kanji-filter-count muted small" aria-live="polite">
          Showing <strong>${e.length}</strong> of ${l.length}.
        </p>
      </div>
      <div class="toc-controls">
        <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
        <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      </div>
      ${m||'<div class="placeholder"><p>No words match the current filter.</p></div>'}
    </article>
  `,V(o,"details.vocab-section");const u=document.getElementById("vocab-filter-q");u&&u.addEventListener("input",()=>{$=u.value,T(o,r);const n=document.getElementById("vocab-filter-q");if(n){n.focus();const i=n.value;n.setSelectionRange(i.length,i.length)}})}function F(o,r,l,t){const g=r.entries||[],e=g.find(a=>a.form===t);if(!e){o.innerHTML=`
      <article class="vocab-detail">
        <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
        <h2>Word not found</h2>
        <p>No vocab entry matches <strong lang="ja">${s(t)}</strong>. The word may live under a different form.</p>
      </article>
    `;return}const p=new Set,c=[];for(const a of l.patterns||[]){for(const d of a.examples||[]){if(!d.ja||d.ja.includes("(see ")||p.has(d.ja))continue;let v=!1;if(Array.isArray(d.vocab_ids))v=d.vocab_ids.includes(e.id);else{const y=[t];e.reading&&e.reading!==t&&y.push(e.reading),v=y.some(C=>d.ja.includes(C))}if(v&&(p.add(d.ja),c.push({ja:d.ja,en:d.translation_en,source:a.pattern}),c.length>=24))break}if(c.length>=24)break}c.sort((a,d)=>(a.ja?.length||0)-(d.ja?.length||0));const f=c.slice(0,5),m=w(g),u=m.findIndex(a=>a.id===e.id),n=u>0?m[u-1]:null,i=u>=0&&u<m.length-1?m[u+1]:null,h=j.isVocabKnown(e.form);o.innerHTML=`
    <article class="vocab-detail">
      <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
      <header class="vocab-header pattern-header">
        <div>
          <p class="muted small">${s(e.section||"")}</p>
          <h2 class="vocab-form-big" lang="ja">${s(e.form)}</h2>
          ${e.reading?`<p class="vocab-reading-big" lang="ja">${s(e.reading)}</p>`:""}
          <p class="vocab-gloss-big">${s(e.gloss||"")}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${h?"checked":""}>
          <span>Mark as known</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">Meaning</h3>
        <p><strong>English:</strong> ${s(e.gloss||"-")}</p>
        ${e.reading?`<p><strong>Japanese reading:</strong> <span lang="ja">${s(e.reading)}</span></p>`:""}
      </section>

      <section>
        <h3 class="section-title">Example sentences ${f.length?`(${f.length})`:""}</h3>
        ${f.length?`
          <ol class="example-list">
            ${f.map(a=>`
              <li>
                <p lang="ja" class="example-ja">${S(a.ja)}</p>
                ${a.en?`<p class="translation">${s(a.en)}</p>`:""}
                ${a.source?`<p class="muted small">From pattern: <span lang="ja">${s(a.source)}</span></p>`:""}
              </li>
            `).join("")}
          </ol>
        `:`
          <p class="muted">No example sentences in the corpus yet for this word. Try the search bar to find phrases that include it.</p>
        `}
      </section>

      <nav class="vocab-nav">
        ${n?`<a href="#/learn/vocab/${encodeURIComponent(n.form)}">\u2190 <span lang="ja">${s(n.form)}</span></a>`:"<span></span>"}
        ${i?`<a href="#/learn/vocab/${encodeURIComponent(i.form)}"><span lang="ja">${s(i.form)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-vocab")?.addEventListener("change",a=>{j.setVocabKnown(e.form,a.target.checked)})}export{F as renderVocabularyDetail,T as renderVocabularyList};
