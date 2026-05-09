import{renderJa as b}from"./furigana.js";import*as x from"./storage.js";import{esc as r,wireExpandCollapseControls as M}from"./learn.js";import{currentLocale as w}from"./i18n.js";function F(t){const e=w();if(e&&e!=="en"){const a=t[`explanation_${e}`];if(typeof a=="string"&&a.trim())return a}return t.explanation_en||""}function D(t){const e=w();if(e&&e!=="en"){const a=t[`meaning_${e}`];if(typeof a=="string"&&a.trim())return a}return t.meaning_en||""}function I(t){const e=w();if(e&&e!=="en"&&t.l1_notes&&typeof t.l1_notes=="object"){const a=t.l1_notes[e];if(typeof a=="string"&&a.trim())return a}return null}const C=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],N={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function S(t){if(typeof t=="object"&&t&&t.id in N)return N[t.id];const e=typeof t=="string"?t:t?.category||"";for(const[a,l]of C)if(l.includes(e))return a;return"Set Phrases and Discourse"}function R(t){const e=new Map;for(const[l]of C)e.set(l,[]);for(const l of t){const c=S(l);e.has(c)&&e.get(c).push(l)}const a=[];for(const[,l]of e)l.sort((c,g)=>(c.patternOrder??0)-(g.patternOrder??0)),a.push(...l);return a}let E="",v="all";function q(t,e,a){return a!=="all"&&(t.tier||"core_n5")!==a?!1:e?[t.pattern,t.meaning_en,t.meaning_ja||"",t.notes||"",(t.examples||[]).map(c=>c.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function L(t,e){const a=new Map;for(const[s]of C)a.set(s,[]);const l=E.trim().toLowerCase(),c=e.patterns.filter(s=>q(s,l,v));for(const s of c){const i=S(s);a.get(i).push(s)}const g=s=>s.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),d=(s,i,p,o)=>`<button type="button" class="kanji-chip ${o?"active":""}"
       data-grammar-filter-group="${s}" data-grammar-filter-value="${i}">${r(p)}</button>`;let u=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${a.size} sections.</p>
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. \u3066-form / wants to / \u3067\u3059)"
        value="${r(E)}" autocomplete="off"
        aria-label="Search grammar patterns">
      <div class="kanji-filter-row" aria-label="Tier filter">
        <span class="kanji-filter-label">Tier:</span>
        ${d("tier","all","All",v==="all")}
        ${d("tier","core_n5","Core N5",v==="core_n5")}
        ${d("tier","late_n5","Late N5",v==="late_n5")}
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
  `;for(const[s,i]of a){if(i.length===0)continue;i.sort((o,m)=>(o.patternOrder??0)-(m.patternOrder??0));const p=l||v!=="all";u+=`<details class="toc-category" id="cat-${g(s)}"${p?" open":""}>`,u+=`<summary><h3>${r(s)} <span class="cat-count muted small">(${i.length})</span></h3></summary>`,u+='<div class="grammar-grid">';for(const o of i){const m=(()=>{const j=(o.examples||[]).filter(k=>k&&k.ja);return j[0]?j[0].ja:""})(),y=o.genki_lesson?`G${o.genki_lesson.book}\xB7L${o.genki_lesson.lesson}`:"";u+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(o.id)}">
          <span class="grammar-pattern" lang="ja">${r(o.pattern)}</span>
          <span class="grammar-card-print-meaning">${r(o.meaning_en||"")}</span>
          <span class="grammar-card-print-example" lang="ja">${r(m)}</span>
          ${y?`<span class="grammar-card-print-lesson">${r(y)}</span>`:""}
        </a>
      `}u+="</div></details>"}c.length===0?u+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(u+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),t.innerHTML=u,M(t,"details.toc-category"),t.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const s=Array.from(t.querySelectorAll("details.toc-category")),i=s.map(o=>o.open);s.forEach(o=>{o.open=!0}),document.body.classList.add("is-printing-cheatsheet");const p=()=>{s.forEach((o,m)=>{o.open=i[m]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",p)};window.addEventListener("afterprint",p),window.print()});const f=document.getElementById("grammar-filter-q");f&&f.addEventListener("input",()=>{E=f.value,L(t,e);const s=document.getElementById("grammar-filter-q");if(s){s.focus();const i=s.value;s.setSelectionRange(i.length,i.length)}}),t.querySelectorAll("[data-grammar-filter-group]").forEach(s=>{s.addEventListener("click",()=>{const i=s.dataset.grammarFilterGroup,p=s.dataset.grammarFilterValue;i==="tier"&&(v=p),L(t,e)})})}const T={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function G(t){return T[t]?T[t]:String(t).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function O(t){const e=t.form_rules?.attaches_to??[],a=t.form_rules?.conjugations??[];if(!e.length&&!a.length)return"";const l=`
    <div class="pattern-usage-header">
      <h3 class="section-title">How to use</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,c=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${r(t.pattern)}">
      <tbody>
        ${e.map((d,u)=>`
          <tr>
            <td class="pattern-usage-pos">${r(G(d))}</td>
            ${u===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${b(t.pattern)}</td>`:""}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"",g=a.length>=2?`
    <table class="pattern-conjugation-table" aria-label="Conjugation forms">
      <thead>
        <tr><th scope="col">Form</th><th scope="col">Example</th></tr>
      </thead>
      <tbody>
        ${a.map(d=>`
          <tr>
            <td>${r(d.label||d.form)}</td>
            <td lang="ja">${b(d.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${l}${c}${g}</section>`}function z(t,e,a){const l=e.form_rules?.conjugations??[],c=e.examples??[],g=e.common_mistakes??[],d=x.getPatternEntry(e.id),u=!!d?.isManuallyKnown,f=!!d?.isMastered,s=!!d?.isWeak&&!f,i=Array.isArray(a)?R(a):[],p=i.findIndex(n=>n.id===e.id),o=p>0?i[p-1]:null,m=p>=0&&p<i.length-1?i[p+1]:null,y=o||m?`
    <div class="pattern-nav">
      ${o?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(o.id)}" title="Previous: ${r(o.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${r(o.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${m?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(m.id)}" title="Next: ${r(m.pattern)}"><span class="pattern-nav-name" lang="ja">${r(m.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",j=c.map((n,$)=>{const _=!n.ja||n.ja.includes("(see ")?null:`audio/grammar/${e.id}.${$}.mp3`;return`
    <li>
      <span class="form-tag">${r(n.form||"")}</span>
      ${b(n.ja,n.furigana)}
      ${n.translation_en?`<span class="translation">${r(n.translation_en)}</span>`:""}
      ${_?`<audio class="example-audio" controls preload="none" src="${r(_)}">Audio not available.</audio>`:""}
    </li>
  `}).join(""),k=g.map(n=>`
    <li>
      <div><span class="wrong">${b(n.wrong)}</span></div>
      <div><span class="right">${b(n.right)}</span></div>
      <span class="why">${r(n.why)}</span>
    </li>
  `).join(""),V=f?'<span class="status-badge mastered">\u2605 Mastered</span>':s?'<span class="status-badge weak">Needs practice</span>':"",B=(()=>{const n=e.genki_lesson;return n?`<span class="pattern-lesson-tag" title="Genki ${n.book} Lesson ${n.lesson}">G${n.book}\xB7L${n.lesson}</span>`:""})(),U=`
    <article class="pattern-detail">
      ${y}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 Back to grammar list</a>
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${r(e.pattern)} ${B}</h2>
          <p class="meaning-en">${r(D(e))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${u?"checked":""}>
          <span>Mark as known</span>
          ${V}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} Print / Save as PDF
        </button>
      </div>

      ${O(e)}

      <section>
        <h3 class="section-title">Explanation</h3>
        <p>${r(F(e))}</p>
      </section>

      ${(()=>{const n=e.essay;if(!n||typeof n!="object")return"";const $=n.provenance==="needs_native_review",h=(_,P,A)=>!P&&!A?"":P?`<p><strong>${r(_)}:</strong> ${r(P)}</p>`:`<p><strong>${r(_)}:</strong> <span class="muted small">${r(A)}</span></p>`;return`
          <section class="pattern-essay">
            <h3 class="section-title">Deep dive ${$?'<span class="essay-stub-badge muted small">stub</span>':""}</h3>
            ${h("At a glance",n.intro)}
            ${h("Why it matters",n.why_it_matters,$?"Pending native author.":"")}
            ${h("Common pitfalls",n.common_pitfalls)}
            ${h("Contrasts",n.contrasts)}
            ${h("Practice tip",n.closing_practice_tip,$?"Pending native author.":"")}
          </section>
        `})()}

      ${(()=>{const n=I(e);return n?`
          <section class="l1-note">
            <h3 class="section-title">L1 note</h3>
            <p>${r(n)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">Examples (${c.length})</h3>
        <ul class="example-list">${j}</ul>
      </section>

      ${g.length?`
        <section>
          <h3 class="section-title">Common Mistakes / Contrasts</h3>
          <ul class="mistakes-list">${k}</ul>
        </section>
      `:""}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${b(e.meaning_ja)}</p>
      </section>

      ${e.notes?`<section><h3 class="section-title">Notes</h3><p>${r(e.notes)}</p></section>`:""}
    </article>
  `;t.innerHTML=U,document.getElementById("mark-known")?.addEventListener("change",n=>{x.setManuallyKnown(e.id,n.target.checked),z(t,e,a)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{R as buildOrderedPatternList,z as renderGrammarPatternDetail,L as renderGrammarTOC};
