import{renderJa as h}from"./furigana.js";import*as P from"./storage.js";import{esc as o,wireExpandCollapseControls as V}from"./learn.js";import{currentLocale as y}from"./i18n.js";function B(t){const e=y();if(e&&e!=="en"){const n=t[`explanation_${e}`];if(typeof n=="string"&&n.trim())return n}return t.explanation_en||""}function U(t){const e=y();if(e&&e!=="en"){const n=t[`meaning_${e}`];if(typeof n=="string"&&n.trim())return n}return t.meaning_en||""}function M(t){const e=y();if(e&&e!=="en"&&t.l1_notes&&typeof t.l1_notes=="object"){const n=t.l1_notes[e];if(typeof n=="string"&&n.trim())return n}return null}const j=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],x={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function C(t){if(typeof t=="object"&&t&&t.id in x)return x[t.id];const e=typeof t=="string"?t:t?.category||"";for(const[n,l]of j)if(l.includes(e))return n;return"Set Phrases and Discourse"}function F(t){const e=new Map;for(const[l]of j)e.set(l,[]);for(const l of t){const c=C(l);e.has(c)&&e.get(c).push(l)}const n=[];for(const[,l]of e)l.sort((c,g)=>(c.patternOrder??0)-(g.patternOrder??0)),n.push(...l);return n}let k="",b="all";function D(t,e,n){return n!=="all"&&(t.tier||"core_n5")!==n?!1:e?[t.pattern,t.meaning_en,t.meaning_ja||"",t.notes||"",(t.examples||[]).map(c=>c.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function E(t,e){const n=new Map;for(const[a]of j)n.set(a,[]);const l=k.trim().toLowerCase(),c=e.patterns.filter(a=>D(a,l,b));for(const a of c){const i=C(a);n.get(i).push(a)}const g=a=>a.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),p=(a,i,d,r)=>`<button type="button" class="kanji-chip ${r?"active":""}"
       data-grammar-filter-group="${a}" data-grammar-filter-value="${i}">${o(d)}</button>`;let u=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${n.size} sections.</p>
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. \u3066-form / wants to / \u3067\u3059)"
        value="${o(k)}" autocomplete="off"
        aria-label="Search grammar patterns">
      <div class="kanji-filter-row" aria-label="Tier filter">
        <span class="kanji-filter-label">Tier:</span>
        ${p("tier","all","All",b==="all")}
        ${p("tier","core_n5","Core N5",b==="core_n5")}
        ${p("tier","late_n5","Late N5",b==="late_n5")}
      </div>
      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${c.length}</strong> of ${e.patterns.length}.
      </p>
    </div>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
      <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
      <!-- IMP-143 (richness audit, 2026-05-09): print-as-PDF cheat
           sheet for the entire grammar list. Auto-expands all sections,
           triggers window.print(), then restores prior state. The print
           stylesheet reveals .grammar-card-print-* spans for a dense
           one-row-per-pattern reference layout. -->
      <button type="button" class="btn-secondary toc-print-cheatsheet">
        \u{1F5A8} Print cheat sheet
      </button>
    </div>
  `;for(const[a,i]of n){if(i.length===0)continue;i.sort((r,m)=>(r.patternOrder??0)-(m.patternOrder??0));const d=l||b!=="all";u+=`<details class="toc-category" id="cat-${g(a)}"${d?" open":""}>`,u+=`<summary><h3>${o(a)} <span class="cat-count muted small">(${i.length})</span></h3></summary>`,u+='<div class="grammar-grid">';for(const r of i){const m=(()=>{const $=(r.examples||[]).filter(_=>_&&_.ja);return $[0]?$[0].ja:""})(),v=r.genki_lesson?`G${r.genki_lesson.book}\xB7L${r.genki_lesson.lesson}`:"";u+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(r.id)}">
          <span class="grammar-pattern" lang="ja">${o(r.pattern)}</span>
          <span class="grammar-card-print-meaning">${o(r.meaning_en||"")}</span>
          <span class="grammar-card-print-example" lang="ja">${o(m)}</span>
          ${v?`<span class="grammar-card-print-lesson">${o(v)}</span>`:""}
        </a>
      `}u+="</div></details>"}c.length===0?u+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(u+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),t.innerHTML=u,V(t,"details.toc-category"),t.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const a=Array.from(t.querySelectorAll("details.toc-category")),i=a.map(r=>r.open);a.forEach(r=>{r.open=!0}),document.body.classList.add("is-printing-cheatsheet");const d=()=>{a.forEach((r,m)=>{r.open=i[m]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",d)};window.addEventListener("afterprint",d),window.print()});const f=document.getElementById("grammar-filter-q");f&&f.addEventListener("input",()=>{k=f.value,E(t,e);const a=document.getElementById("grammar-filter-q");if(a){a.focus();const i=a.value;a.setSelectionRange(i.length,i.length)}}),t.querySelectorAll("[data-grammar-filter-group]").forEach(a=>{a.addEventListener("click",()=>{const i=a.dataset.grammarFilterGroup,d=a.dataset.grammarFilterValue;i==="tier"&&(b=d),E(t,e)})})}const A={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function I(t){return A[t]?A[t]:String(t).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function R(t){const e=t.form_rules?.attaches_to??[],n=t.form_rules?.conjugations??[];if(!e.length&&!n.length)return"";const l=`
    <div class="pattern-usage-header">
      <h3 class="section-title">How to use</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,c=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${o(t.pattern)}">
      <tbody>
        ${e.map((p,u)=>`
          <tr>
            <td class="pattern-usage-pos">${o(I(p))}</td>
            ${u===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${h(t.pattern)}</td>`:""}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"",g=n.length>=2?`
    <table class="pattern-conjugation-table" aria-label="Conjugation forms">
      <thead>
        <tr><th scope="col">Form</th><th scope="col">Example</th></tr>
      </thead>
      <tbody>
        ${n.map(p=>`
          <tr>
            <td>${o(p.label||p.form)}</td>
            <td lang="ja">${h(p.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${l}${c}${g}</section>`}function q(t,e,n){const l=e.form_rules?.conjugations??[],c=e.examples??[],g=e.common_mistakes??[],p=P.getPatternEntry(e.id),u=!!p?.isManuallyKnown,f=!!p?.isMastered,a=!!p?.isWeak&&!f,i=Array.isArray(n)?F(n):[],d=i.findIndex(s=>s.id===e.id),r=d>0?i[d-1]:null,m=d>=0&&d<i.length-1?i[d+1]:null,v=r||m?`
    <div class="pattern-nav">
      ${r?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(r.id)}" title="Previous: ${o(r.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${o(r.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${m?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(m.id)}" title="Next: ${o(m.pattern)}"><span class="pattern-nav-name" lang="ja">${o(m.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",$=c.map((s,T)=>{const w=!s.ja||s.ja.includes("(see ")?null:`audio/grammar/${e.id}.${T}.mp3`;return`
    <li>
      <span class="form-tag">${o(s.form||"")}</span>
      ${h(s.ja,s.furigana)}
      ${s.translation_en?`<span class="translation">${o(s.translation_en)}</span>`:""}
      ${w?`<audio class="example-audio" controls preload="none" src="${o(w)}">Audio not available.</audio>`:""}
    </li>
  `}).join(""),_=g.map(s=>`
    <li>
      <div><span class="wrong">${h(s.wrong)}</span></div>
      <div><span class="right">${h(s.right)}</span></div>
      <span class="why">${o(s.why)}</span>
    </li>
  `).join(""),N=f?'<span class="status-badge mastered">\u2605 Mastered</span>':a?'<span class="status-badge weak">Needs practice</span>':"",S=(()=>{const s=e.genki_lesson;return s?`<span class="pattern-lesson-tag" title="Genki ${s.book} Lesson ${s.lesson}">G${s.book}\xB7L${s.lesson}</span>`:""})(),L=`
    <article class="pattern-detail">
      ${v}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 Back to grammar list</a>
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${o(e.pattern)} ${S}</h2>
          <p class="meaning-en">${o(U(e))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${u?"checked":""}>
          <span>Mark as known</span>
          ${N}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} Print / Save as PDF
        </button>
      </div>

      ${R(e)}

      <section>
        <h3 class="section-title">Explanation</h3>
        <p>${o(B(e))}</p>
      </section>

      ${(()=>{const s=M(e);return s?`
          <section class="l1-note">
            <h3 class="section-title">L1 note</h3>
            <p>${o(s)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">Examples (${c.length})</h3>
        <ul class="example-list">${$}</ul>
      </section>

      ${g.length?`
        <section>
          <h3 class="section-title">Common Mistakes / Contrasts</h3>
          <ul class="mistakes-list">${_}</ul>
        </section>
      `:""}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${h(e.meaning_ja)}</p>
      </section>

      ${e.notes?`<section><h3 class="section-title">Notes</h3><p>${o(e.notes)}</p></section>`:""}
    </article>
  `;t.innerHTML=L,document.getElementById("mark-known")?.addEventListener("change",s=>{P.setManuallyKnown(e.id,s.target.checked),q(t,e,n)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{F as buildOrderedPatternList,q as renderGrammarPatternDetail,E as renderGrammarTOC};
