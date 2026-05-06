import{renderJa as _}from"./furigana.js";import*as S from"./storage.js";import{esc as t,wireExpandCollapseControls as x}from"./learn.js";import{currentLocale as $}from"./i18n.js";import{renderItemBadge as M}from"./provenance-badge.js";function T(s,o){if(!s||!Number.isFinite(s.mora))return"";const c=s.mora,r=s.drop;let i="";for(let e=1;e<=c;e++)r===0?i+=e===1?"L":"H":r===1?i+=e===1?"H":"L":i+=e===1?"L":e<=r?"H":"L";return i}function E(s){return{satsu:"\u3055\u3064",dai:"\u3060\u3044",hiki:"\u3072\u304D",wa:"\u308F",mai:"\u307E\u3044",ken:"\u3051\u3093",hon:"\u307B\u3093",soku:"\u305D\u304F",ko:"\u3053",nin:"\u306B\u3093",tsu:"\u3064",kai:"\u304B\u3044",do:"\u3069",fun:"\u3075\u3093",ji:"\u3058"}[s]||s}function j(s){const o=$();if(o&&o!=="en"){const c=s[`gloss_${o}`];if(typeof c=="string"&&c.trim())return c}return s.gloss||""}const y=[["People and Body",["1. People - Pronouns and Self","2. People - Family","3. People - Roles","4. Body Parts"]],["Demonstratives, Questions, Numbers, Time",["5. Demonstratives","6. Question Words","7. Numbers","8. Native Counters (\u3064-series)","9. Counters (Common)","10. Time - General","11. Time - Days, Weeks, Months, Years","12. Time - Frequency / Sequence"]],["Places and Things",["13. Locations and Places (general)","14. Nature and Weather","15. Animals","16. Food and Drink - General","17. Food - Items","18. Drinks","19. Tableware and Cooking","20. Colors","21. Clothing and Accessories","22. Money and Shopping","23. Transport","24. School and Study","25. Languages and Countries","26. House and Furniture"]],["Verbs",["27. Verbs - Group 1 (\u3046-verbs)","28. Verbs - Group 2 (\u308B-verbs)","29. Verbs - Irregular and \u3059\u308B-verbs","30. Verbs - Existence and Possession"]],["Adjectives and Function Words",["31. \u3044-Adjectives","32. \u306A-Adjectives","33. Adverbs","34. Conjunctions","35. Particles (functional vocabulary)","36. Greetings and Set Phrases"]],["Misc",["37. Common Nouns - Miscellaneous","38. Sounds and Voice","39. Function / Filler Expressions","40. Misc Useful Items"]]];function L(s){for(const[o,c]of y)if(c.includes(s))return o;return"Misc"}function V(s){const o=new Map;for(const[r]of y)o.set(r,[]);for(const r of s){const i=L(r.section||"Other");o.get(i).push(r)}const c=[];for(const[,r]of o.entries())r.sort((i,e)=>{const p=parseInt(i.section||"",10),l=parseInt(e.section||"",10);return!isNaN(p)&&!isNaN(l)&&p!==l?p-l:(i.form||"").localeCompare(e.form||"")}),c.push(...r);return c}let k="";function F(s,o){return o?[s.form||"",s.reading||"",s.gloss||"",s.section||""].join(" ").toLowerCase().includes(o):!0}function N(s,o){const c=o.entries||[],r=k.trim().toLowerCase(),e=V(c).filter(n=>F(n,r)),p=new Map;for(const[n]of y)p.set(n,[]);for(const n of e){const a=L(n.section||"Other");p.get(a).push(n)}const l=n=>n.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),m=r.length>0,d=$(),f=d&&d!=="en",h=n=>{if(!f)return"";const a=n.length;if(a===0)return"";const g=n.filter(C=>typeof C[`gloss_${d}`]=="string"&&C[`gloss_${d}`].trim()).length,u=Math.round(100*g/a);return`<span class="vocab-coverage-badge tone-${u>=50?"good":u>0?"partial":"none"}" title="${g}/${a} translated">${u}%</span>`},b=[...p.entries()].filter(([,n])=>n.length>0).map(([n,a])=>{const g=a.map(u=>`
        <a class="vocab-card" href="#/learn/vocab/${encodeURIComponent(u.form||"")}">
          <span class="vocab-form" lang="ja">${t(u.form||"")}</span>
        </a>
      `).join("");return`
        <details class="vocab-section" id="vocab-${l(n)}"${m?" open":""}>
          <summary><strong>${t(n)}</strong> <span class="muted small">(${a.length})</span> ${h(a)}</summary>
          <div class="vocab-grid">${g}</div>
        </details>
      `}).join("");s.innerHTML=`
    <article class="vocab-toc">
      <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
      <h2>Vocabulary</h2>
      <p class="page-lede">${c.length} N5 words in ${y.length} sections.</p>
      <div class="kanji-filters" role="search" aria-label="Filter vocabulary">
        <input type="search" id="vocab-filter-q" class="kanji-filter-input"
          placeholder="Search form, reading, or English (e.g. \u305F\u3079\u308B / eat / \u98F2\u3080)"
          value="${t(k)}" autocomplete="off" lang="ja"
          aria-label="Search vocabulary">
        <p class="kanji-filter-count muted small" aria-live="polite">
          Showing <strong>${e.length}</strong> of ${c.length}.
        </p>
      </div>
      <div class="toc-controls">
        <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
        <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      </div>
      ${b||'<div class="placeholder"><p>No words match the current filter.</p></div>'}
    </article>
  `,x(s,"details.vocab-section");const v=document.getElementById("vocab-filter-q");v&&v.addEventListener("input",()=>{k=v.value,N(s,o);const n=document.getElementById("vocab-filter-q");if(n){n.focus();const a=n.value;n.setSelectionRange(a.length,a.length)}})}function D(s,o,c,r){const i=o.entries||[],e=i.find(n=>n.form===r);if(!e){s.innerHTML=`
      <article class="vocab-detail">
        <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
        <h2>Word not found</h2>
        <p>No vocab entry matches <strong lang="ja">${t(r)}</strong>. The word may live under a different form.</p>
      </article>
    `;return}const p=new Set,l=[];for(const n of c.patterns||[]){for(const a of n.examples||[]){if(!a.ja||a.ja.includes("(see ")||p.has(a.ja))continue;let g=!1;if(Array.isArray(a.vocab_ids))g=a.vocab_ids.includes(e.id);else{const u=[r];e.reading&&e.reading!==r&&u.push(e.reading),g=u.some(w=>a.ja.includes(w))}if(g&&(p.add(a.ja),l.push({ja:a.ja,en:a.translation_en,source:n.pattern}),l.length>=24))break}if(l.length>=24)break}l.sort((n,a)=>(n.ja?.length||0)-(a.ja?.length||0));const m=l.slice(0,5),d=V(i),f=d.findIndex(n=>n.id===e.id),h=f>0?d[f-1]:null,b=f>=0&&f<d.length-1?d[f+1]:null,v=S.isVocabKnown(e.form);s.innerHTML=`
    <article class="vocab-detail">
      <a class="back-link" href="#/learn/vocab">\u2190 Back to Vocabulary</a>
      <header class="vocab-header pattern-header">
        <div>
          <p class="muted small">${t(e.section||"")}</p>
          <h2 class="vocab-form-big" lang="ja">${t(e.form)}</h2>
          ${e.reading?`<p class="vocab-reading-big" lang="ja">${t(e.reading)}</p>`:""}
          <p class="vocab-gloss-big">${t(j(e))} ${M(e,!0)}</p>
        </div>
        <label class="known-toggle" title="Manually mark this word as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known-vocab" ${v?"checked":""}>
          <span>Mark as known</span>
        </label>
      </header>

      <section>
        <h3 class="section-title">Meaning</h3>
        <p><strong>${$()==="en"?"English":"Meaning"}:</strong> ${t(j(e)||"-")}</p>
        ${$()!=="en"&&e.gloss&&j(e)!==e.gloss?`<p><strong>English:</strong> ${t(e.gloss)}</p>`:""}
        ${e.reading?`<p><strong>Japanese reading:</strong> <span lang="ja">${t(e.reading)}</span></p>`:""}
        ${(()=>{const n=[];return e.pitch_accent&&Number.isFinite(e.pitch_accent.mora)&&n.push(`<p><strong>Pitch accent:</strong> <span class="vocab-pitch" lang="ja">${t(T(e.pitch_accent,e.reading))}</span> <span class="muted small">(drop: ${e.pitch_accent.drop})</span></p>`),e.counter&&n.push(`<p><strong>Counter:</strong> <span lang="ja">\u301C${t(E(e.counter))}</span></p>`),e.register&&n.push(`<p><strong>Register:</strong> <span class="vocab-register-tag">${t(e.register)}</span></p>`),e.transitivity&&n.push(`<p><strong>Transitivity:</strong> ${t(e.transitivity)}${e.pair_id?` <span class="muted small">(pair: ${t(e.pair_id)})</span>`:""}</p>`),n.join("")})()}
      </section>

      <section>
        <h3 class="section-title">Example sentences ${m.length?`(${m.length})`:""}</h3>
        ${m.length?`
          <ol class="example-list">
            ${m.map(n=>`
              <li>
                <p lang="ja" class="example-ja">${_(n.ja)}</p>
                ${n.en?`<p class="translation">${t(n.en)}</p>`:""}
                ${n.source?`<p class="muted small">From pattern: <span lang="ja">${t(n.source)}</span></p>`:""}
              </li>
            `).join("")}
          </ol>
        `:`
          <p class="muted">No example sentences in the corpus yet for this word. Try the search bar to find phrases that include it.</p>
        `}
      </section>

      <nav class="vocab-nav">
        ${h?`<a href="#/learn/vocab/${encodeURIComponent(h.form)}">\u2190 <span lang="ja">${t(h.form)}</span></a>`:"<span></span>"}
        ${b?`<a href="#/learn/vocab/${encodeURIComponent(b.form)}"><span lang="ja">${t(b.form)}</span> \u2192</a>`:"<span></span>"}
      </nav>
    </article>
  `,document.getElementById("mark-known-vocab")?.addEventListener("change",n=>{S.setVocabKnown(e.form,n.target.checked)})}export{D as renderVocabularyDetail,N as renderVocabularyList};
