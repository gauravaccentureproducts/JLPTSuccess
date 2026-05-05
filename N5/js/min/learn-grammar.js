import{renderJa as h}from"./furigana.js";import*as y from"./storage.js";import{esc as s,wireExpandCollapseControls as V}from"./learn.js";const v=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],j={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function C(a){if(typeof a=="object"&&a&&a.id in j)return j[a.id];const e=typeof a=="string"?a:a?.category||"";for(const[n,o]of v)if(o.includes(e))return n;return"Set Phrases and Discourse"}function T(a){const e=new Map;for(const[o]of v)e.set(o,[]);for(const o of a){const i=C(o);e.has(i)&&e.get(i).push(o)}const n=[];for(const[,o]of e)o.sort((i,m)=>(i.patternOrder??0)-(m.patternOrder??0)),n.push(...o);return n}let $="",b="all";function B(a,e,n){return n!=="all"&&(a.tier||"core_n5")!==n?!1:e?[a.pattern,a.meaning_en,a.meaning_ja||"",a.notes||"",(a.examples||[]).map(i=>i.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function k(a,e){const n=new Map;for(const[t]of v)n.set(t,[]);const o=$.trim().toLowerCase(),i=e.patterns.filter(t=>B(t,o,b));for(const t of i){const r=C(t);n.get(r).push(t)}const m=t=>t.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),c=(t,r,u,d)=>`<button type="button" class="kanji-chip ${d?"active":""}"
       data-grammar-filter-group="${t}" data-grammar-filter-value="${r}">${s(u)}</button>`;let p=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${n.size} sections.</p>
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. \u3066-form / wants to / \u3067\u3059)"
        value="${s($)}" autocomplete="off"
        aria-label="Search grammar patterns">
      <div class="kanji-filter-row" aria-label="Tier filter">
        <span class="kanji-filter-label">Tier:</span>
        ${c("tier","all","All",b==="all")}
        ${c("tier","core_n5","Core N5",b==="core_n5")}
        ${c("tier","late_n5","Late N5",b==="late_n5")}
      </div>
      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${i.length}</strong> of ${e.patterns.length}.
      </p>
    </div>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
      <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
    </div>
  `;for(const[t,r]of n){if(r.length===0)continue;r.sort((d,g)=>(d.patternOrder??0)-(g.patternOrder??0));const u=o||b!=="all";p+=`<details class="toc-category" id="cat-${m(t)}"${u?" open":""}>`,p+=`<summary><h3>${s(t)} <span class="cat-count muted small">(${r.length})</span></h3></summary>`,p+='<div class="grammar-grid">';for(const d of r)p+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(d.id)}">
          <span class="grammar-pattern" lang="ja">${s(d.pattern)}</span>
          <span class="grammar-gloss">${s(d.meaning_en)}</span>
        </a>
      `;p+="</div></details>"}i.length===0?p+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(p+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),a.innerHTML=p,V(a,"details.toc-category");const f=document.getElementById("grammar-filter-q");f&&f.addEventListener("input",()=>{$=f.value,k(a,e);const t=document.getElementById("grammar-filter-q");if(t){t.focus();const r=t.value;t.setSelectionRange(r.length,r.length)}}),a.querySelectorAll("[data-grammar-filter-group]").forEach(t=>{t.addEventListener("click",()=>{const r=t.dataset.grammarFilterGroup,u=t.dataset.grammarFilterValue;r==="tier"&&(b=u),k(a,e)})})}const A={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function U(a){return A[a]?A[a]:String(a).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function L(a){const e=a.form_rules?.attaches_to??[],n=a.form_rules?.conjugations??[];if(!e.length&&!n.length)return"";const o=`
    <div class="pattern-usage-header">
      <h3 class="section-title">How to use</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,i=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${s(a.pattern)}">
      <tbody>
        ${e.map((c,p)=>`
          <tr>
            <td class="pattern-usage-pos">${s(U(c))}</td>
            ${p===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${h(a.pattern)}</td>`:""}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"",m=n.length>=2?`
    <table class="pattern-conjugation-table" aria-label="Conjugation forms">
      <thead>
        <tr><th scope="col">Form</th><th scope="col">Example</th></tr>
      </thead>
      <tbody>
        ${n.map(c=>`
          <tr>
            <td>${s(c.label||c.form)}</td>
            <td lang="ja">${h(c.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${o}${i}${m}</section>`}function M(a,e,n){const o=e.form_rules?.conjugations??[],i=e.examples??[],m=e.common_mistakes??[],c=y.getPatternEntry(e.id),p=!!c?.isManuallyKnown,f=!!c?.isMastered,t=!!c?.isWeak&&!f,r=Array.isArray(n)?T(n):[],u=r.findIndex(l=>l.id===e.id),d=u>0?r[u-1]:null,g=u>=0&&u<r.length-1?r[u+1]:null,P=d||g?`
    <div class="pattern-nav">
      ${d?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(d.id)}" title="Previous: ${s(d.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${s(d.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${g?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(g.id)}" title="Next: ${s(g.pattern)}"><span class="pattern-nav-name" lang="ja">${s(g.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",x=i.map((l,S)=>{const _=!l.ja||l.ja.includes("(see ")?null:`audio/grammar/${e.id}.${S}.mp3`;return`
    <li>
      <span class="form-tag">${s(l.form||"")}</span>
      ${h(l.ja,l.furigana)}
      ${l.translation_en?`<span class="translation">${s(l.translation_en)}</span>`:""}
      ${_?`<audio class="example-audio" controls preload="none" src="${s(_)}">Audio not available.</audio>`:""}
    </li>
  `}).join(""),E=m.map(l=>`
    <li>
      <div><span class="wrong">${h(l.wrong)}</span></div>
      <div><span class="right">${h(l.right)}</span></div>
      <span class="why">${s(l.why)}</span>
    </li>
  `).join(""),w=f?'<span class="status-badge mastered">\u2605 Mastered</span>':t?'<span class="status-badge weak">Needs practice</span>':"",N=`
    <article class="pattern-detail">
      ${P}
      <a class="back-link" href="#/learn/grammar">\u2190 Back to grammar list</a>
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${s(e.pattern)}</h2>
          <p class="meaning-en">${s(e.meaning_en)}</p>
        </div>
        <label class="known-toggle" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${p?"checked":""}>
          <span>Mark as known</span>
          ${w}
        </label>
      </div>

      ${L(e)}

      <section>
        <h3 class="section-title">Explanation</h3>
        <p>${s(e.explanation_en)}</p>
      </section>

      <section>
        <h3 class="section-title">Examples (${i.length})</h3>
        <ul class="example-list">${x}</ul>
      </section>

      ${m.length?`
        <section>
          <h3 class="section-title">Common Mistakes / Contrasts</h3>
          <ul class="mistakes-list">${E}</ul>
        </section>
      `:""}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${h(e.meaning_ja)}</p>
      </section>

      ${e.notes?`<section><h3 class="section-title">Notes</h3><p>${s(e.notes)}</p></section>`:""}
    </article>
  `;a.innerHTML=N,document.getElementById("mark-known")?.addEventListener("change",l=>{y.setManuallyKnown(e.id,l.target.checked),M(a,e,n)})}export{T as buildOrderedPatternList,M as renderGrammarPatternDetail,k as renderGrammarTOC};
