import{renderJa as M}from"./furigana.js";import*as S from"./storage.js";import{esc as t,wireExpandCollapseControls as E}from"./learn.js";import{currentLocale as $}from"./i18n.js";function y(a){const o=$();if(o&&o!=="en"){const r=a[`gloss_${o}`];if(typeof r=="string"&&r.trim())return r}return a.gloss||""}const j=[["People and Body",["1. People - Pronouns and Self","2. People - Family","3. People - Roles","4. Body Parts"]],["Demonstratives, Questions, Numbers, Time",["5. Demonstratives","6. Question Words","7. Numbers","8. Native Counters (\u3064-series)","9. Counters (Common)","10. Time - General","11. Time - Days, Weeks, Months, Years","12. Time - Frequency / Sequence"]],["Places and Things",["13. Locations and Places (general)","14. Nature and Weather","15. Animals","16. Food and Drink - General","17. Food - Items","18. Drinks","19. Tableware and Cooking","20. Colors","21. Clothing and Accessories","22. Money and Shopping","23. Transport","24. School and Study","25. Languages and Countries","26. House and Furniture"]],["Verbs",["27. Verbs - Group 1 (\u3046-verbs)","28. Verbs - Group 2 (\u308B-verbs)","29. Verbs - Irregular and \u3059\u308B-verbs","30. Verbs - Existence and Possession"]],["Adjectives and Function Words",["31. \u3044-Adjectives","32. \u306A-Adjectives","33. Adverbs","34. Conjunctions","35. Particles (functional vocabulary)","36. Greetings and Set Phrases"]],["Misc",["37. Common Nouns - Miscellaneous","38. Sounds and Voice","39. Function / Filler Expressions","40. Misc Useful Items"]]];function V(a){for(const[o,r]of j)if(r.includes(a))return o;return"Misc"}function x(a){const o=new Map;for(const[l]of j)o.set(l,[]);for(const l of a){const u=V(l.section||"Other");o.get(u).push(l)}const r=[];for(const[,l]of o.entries())l.sort((u,n)=>{const d=parseInt(u.section||"",10),i=parseInt(n.section||"",10);return!isNaN(d)&&!isNaN(i)&&d!==i?d-i:(u.form||"").localeCompare(n.form||"")}),r.push(...l);return r}let k="";function T(a,o){return o?[a.form||"",a.reading||"",a.gloss||"",a.section||""].join(" ").toLowerCase().includes(o):!0}function L(a,o){const r=o.entries||[],l=k.trim().toLowerCase(),n=x(r).filter(e=>T(e,l)),d=new Map;for(const[e]of j)d.set(e,[]);for(const e of n){const s=V(e.section||"Other");d.get(s).push(e)}const i=e=>e.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),h=l.length>0,p=$(),f=p&&p!=="en",m=e=>{if(!f)return"";const s=e.length;if(s===0)return"";const g=e.filter(C=>typeof C[`gloss_${p}`]=="string"&&C[`gloss_${p}`].trim()).length,c=Math.round(100*g/s);return`<span class="vocab-coverage-badge tone-${c>=50?"good":c>0?"partial":"none"}" title="${g}/${s} translated">${c}%</span>`},b=[...d.entries()].filter(([,e])=>e.length>0).map(([e,s])=>{const g=s.map(c=>`
        <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(c.form||"")}">
          <span class="vocab-form" lang="ja">${t(c.form||"")}</span>
          ${c.reading?`<span class="vocab-reading" lang="ja">${t(c.reading)}</span>`:""}
          <span class="vocab-gloss">${t(y(c))}</span>
        </a>
      `).join("");return`
        <details class="vocab-section" id="vocab-${i(e)}"${h?" open":""}>
          <summary><strong>${t(e)}</strong> <span class="muted small">(${s.length})</span> ${m(s)}</summary>
          <div class="vocab-grid">${g}</div>
        </details>
      `}).join("");a.innerHTML=`
    <article class="vocab-toc">
      <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
      <h2>Vocabulary</h2>
      <p class="page-lede">${r.length} N5 words in ${j.length} sections.</p>
      <div class="kanji-filters" role="search" aria-label="Filter vocabulary">
        <input type="search" id="vocab-filter-q" class="kanji-filter-input"
          placeholder="Search form, reading, or English (e.g. \u305F\u3079\u308B / eat / \u98F2\u3080)"
          value="${t(k)}" autocomplete="off" lang="ja"
          aria-label="Search vocabulary">
        <p class="kanji-filter-count muted small" aria-live="polite">
          Showing <strong>${n.length}</strong> of ${r.length}.
        </p>
      </div>
      <div class="toc-controls">
        <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
        <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      </div>
      ${b||'<div class="placeholder"><p>No words match the current filter.</p></div>'}
    </article>
  `,E(a,"details.vocab-section");const v=document.getElementById("vocab-filter-q");v&&v.addEventListener("input",()=>{k=v.value,L(a,o);const e=document.getElementById("vocab-filter-q");if(e){e.focus();const s=e.value;e.setSelectionRange(s.length,s.length)}})}function P(a,o,r,l){const u=o.entries||[],n=u.find(e=>e.form===l);if(!n){a.innerHTML=`
      <article class="vocab-detail">
        <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
        <h2>Word not found</h2>
        <p>No vocab entry matches <strong lang="ja">${t(l)}</strong>. The word may live under a different form.</p>
      </article>
    `;return}const d=new Set,i=[];for(const e of r.patterns||[]){for(const s of e.examples||[]){if(!s.ja||s.ja.includes("(see ")||d.has(s.ja))continue;let g=!1;if(Array.isArray(s.vocab_ids))g=s.vocab_ids.includes(n.id);else{const c=[l];n.reading&&n.reading!==l&&c.push(n.reading),g=c.some(w=>s.ja.includes(w))}if(g&&(d.add(s.ja),i.push({ja:s.ja,en:s.translation_en,source:e.pattern}),i.length>=24))break}if(i.length>=24)break}i.sort((e,s)=>(e.ja?.length||0)-(s.ja?.length||0));const h=i.slice(0,5),p=x(u),f=p.findIndex(e=>e.id===n.id),m=f>0?p[f-1]:null,b=f>=0&&f<p.length-1?p[f+1]:null,v=S.isVocabKnown(n.form);a.innerHTML=`
    <article class="vocab-detail">
      <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
      <header class="vocab-header pattern-header">
        <div>
          <p class="muted small">${t(n.section||"")}</p>
          <h2 class="vocab-form-big" lang="ja">${t(n.form)}</h2>
          ${n.reading?`<p class="vocab-reading-big" lang="ja">${t(n.reading)}</p>`:""}
          <p class="vocab-gloss-big">${t(y(n))}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${v?"checked":""}>
          <span>Mark as known</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">Meaning</h3>
        <p><strong>${$()==="en"?"English":"Meaning"}:</strong> ${t(y(n)||"-")}</p>
        ${$()!=="en"&&n.gloss&&y(n)!==n.gloss?`<p><strong>English:</strong> ${t(n.gloss)}</p>`:""}
        ${n.reading?`<p><strong>Japanese reading:</strong> <span lang="ja">${t(n.reading)}</span></p>`:""}
      </section>

      <section>
        <h3 class="section-title">Example sentences ${h.length?`(${h.length})`:""}</h3>
        ${h.length?`
          <ol class="example-list">
            ${h.map(e=>`
              <li>
                <p lang="ja" class="example-ja">${M(e.ja)}</p>
                ${e.en?`<p class="translation">${t(e.en)}</p>`:""}
                ${e.source?`<p class="muted small">From pattern: <span lang="ja">${t(e.source)}</span></p>`:""}
              </li>
            `).join("")}
          </ol>
        `:`
          <p class="muted">No example sentences in the corpus yet for this word. Try the search bar to find phrases that include it.</p>
        `}
      </section>

      <nav class="vocab-nav">
        ${m?`<a href="#/learn/vocab/${encodeURIComponent(m.form)}">\u2190 <span lang="ja">${t(m.form)}</span></a>`:"<span></span>"}
        ${b?`<a href="#/learn/vocab/${encodeURIComponent(b.form)}"><span lang="ja">${t(b.form)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-vocab")?.addEventListener("change",e=>{S.setVocabKnown(n.form,e.target.checked)})}export{P as renderVocabularyDetail,L as renderVocabularyList};
