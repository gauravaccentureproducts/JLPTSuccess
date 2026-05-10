import{renderJa as b}from"./furigana.js";import*as x from"./storage.js";import{esc as s,wireExpandCollapseControls as B}from"./learn.js";import{currentLocale as P}from"./i18n.js";function U(t){const e=P();if(e&&e!=="en"){const a=t[`explanation_${e}`];if(typeof a=="string"&&a.trim())return a}return t.explanation_en||""}function M(t){const e=P();if(e&&e!=="en"){const a=t[`meaning_${e}`];if(typeof a=="string"&&a.trim())return a}return t.meaning_en||""}function D(t){const e=P();if(e&&e!=="en"&&t.l1_notes&&typeof t.l1_notes=="object"){const a=t.l1_notes[e];if(typeof a=="string"&&a.trim())return a}return null}const w=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],E={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function A(t){if(typeof t=="object"&&t&&t.id in E)return E[t.id];const e=typeof t=="string"?t:t?.category||"";for(const[a,l]of w)if(l.includes(e))return a;return"Set Phrases and Discourse"}function F(t){const e=new Map;for(const[l]of w)e.set(l,[]);for(const l of t){const p=A(l);e.has(p)&&e.get(p).push(l)}const a=[];for(const[,l]of e)l.sort((p,m)=>(p.patternOrder??0)-(m.patternOrder??0)),a.push(...l);return a}let C="";function I(t,e){return e?[t.pattern,t.meaning_en,t.meaning_ja||"",t.notes||"",(t.examples||[]).map(l=>l.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function R(t,e){const a=new Map;for(const[r]of w)a.set(r,[]);const l=C.trim().toLowerCase(),p=e.patterns.filter(r=>I(r,l));for(const r of p){const c=A(r);a.get(c).push(r)}const m=r=>r.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");let i=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${a.size} sections.</p>
  `;for(const[r,c]of a){if(c.length===0)continue;c.sort((o,d)=>(o.patternOrder??0)-(d.patternOrder??0));const u=!!l;i+=`<details class="toc-category" id="cat-${m(r)}"${u?" open":""}>`,i+=`<summary><h3>${s(r)} <span class="cat-count muted small">(${c.length})</span></h3></summary>`,i+='<div class="grammar-grid">';for(const o of c){const d=(()=>{const y=(o.examples||[]).filter(_=>_&&_.ja);return y[0]?y[0].ja:""})(),g=o.genki_lesson?`G${o.genki_lesson.book}\xB7L${o.genki_lesson.lesson}`:"";i+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(o.id)}">
          <span class="grammar-pattern" lang="ja">${s(o.pattern)}</span>
          <span class="grammar-card-print-meaning">${s(o.meaning_en||"")}</span>
          <span class="grammar-card-print-example" lang="ja">${s(d)}</span>
          ${g?`<span class="grammar-card-print-lesson">${s(g)}</span>`:""}
        </a>
      `}i+="</div></details>"}p.length===0?i+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(i+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),i+=`
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. \u3066-form / wants to / \u3067\u3059)"
        value="${s(C)}" autocomplete="off"
        aria-label="Search grammar patterns">
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
  `,t.innerHTML=i,B(t,"details.toc-category"),t.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const r=Array.from(t.querySelectorAll("details.toc-category")),c=r.map(o=>o.open);r.forEach(o=>{o.open=!0}),document.body.classList.add("is-printing-cheatsheet");const u=()=>{r.forEach((o,d)=>{o.open=c[d]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",u)};window.addEventListener("afterprint",u),window.print()});const f=document.getElementById("grammar-filter-q");f&&f.addEventListener("input",()=>{C=f.value,R(t,e);const r=document.getElementById("grammar-filter-q");if(r){r.focus();const c=r.value;r.setSelectionRange(c.length,c.length)}})}const N={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function q(t){return N[t]?N[t]:String(t).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function O(t){const e=t.form_rules?.attaches_to??[],a=t.form_rules?.conjugations??[];if(!e.length&&!a.length)return"";const l=`
    <div class="pattern-usage-header">
      <h3 class="section-title">How to use</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,p=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${s(t.pattern)}">
      <tbody>
        ${e.map((i,f)=>`
          <tr>
            <td class="pattern-usage-pos">${s(q(i))}</td>
            ${f===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${b(t.pattern)}</td>`:""}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"",m=a.length>=2?`
    <table class="pattern-conjugation-table" aria-label="Conjugation forms">
      <thead>
        <tr><th scope="col">Form</th><th scope="col">Example</th></tr>
      </thead>
      <tbody>
        ${a.map(i=>`
          <tr>
            <td>${s(i.label||i.form)}</td>
            <td lang="ja">${b(i.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${l}${p}${m}</section>`}function G(t,e,a){const l=e.form_rules?.conjugations??[],p=e.examples??[],m=e.common_mistakes??[],i=x.getPatternEntry(e.id),f=!!i?.isManuallyKnown,r=!!i?.isMastered,c=!!i?.isWeak&&!r,u=Array.isArray(a)?F(a):[],o=u.findIndex(n=>n.id===e.id),d=o>0?u[o-1]:null,g=o>=0&&o<u.length-1?u[o+1]:null,y=d||g?`
    <div class="pattern-nav">
      ${d?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(d.id)}" title="Previous: ${s(d.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${s(d.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${g?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(g.id)}" title="Next: ${s(g.pattern)}"><span class="pattern-nav-name" lang="ja">${s(g.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",_=p.map((n,v)=>{const $=!n.ja||n.ja.includes("(see ")?null:`audio/grammar/${e.id}.${v}.mp3`;return`
    <li>
      <span class="form-tag">${s(n.form||"")}</span>
      ${b(n.ja,n.furigana)}
      ${n.translation_en?`<span class="translation">${s(n.translation_en)}</span>`:""}
      ${$?`<audio class="example-audio" controls preload="none" src="${s($)}">Audio not available.</audio>`:""}
    </li>
  `}).join(""),S=m.map(n=>`
    <li>
      <div><span class="wrong">${b(n.wrong)}</span></div>
      <div><span class="right">${b(n.right)}</span></div>
      <span class="why">${s(n.why)}</span>
    </li>
  `).join(""),L=r?'<span class="status-badge mastered">\u2605 Mastered</span>':c?'<span class="status-badge weak">Needs practice</span>':"",V=(()=>{const n=e.genki_lesson;return n?`<span class="pattern-lesson-tag" title="Genki ${n.book} Lesson ${n.lesson}">G${n.book}\xB7L${n.lesson}</span>`:""})(),T=`
    <article class="pattern-detail">
      ${y}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 Back to grammar list</a>
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${s(e.pattern)} ${V}</h2>
          <p class="meaning-en">${s(M(e))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${f?"checked":""}>
          <span>Mark as known</span>
          ${L}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} Print / Save as PDF
        </button>
      </div>

      ${O(e)}

      <section>
        <h3 class="section-title">Explanation</h3>
        <p>${s(U(e))}</p>
      </section>

      ${(()=>{const n=e.essay;if(!n||typeof n!="object")return"";const v=n.provenance==="needs_native_review",h=($,j,k)=>!j&&!k?"":j?`<p><strong>${s($)}:</strong> ${s(j)}</p>`:`<p><strong>${s($)}:</strong> <span class="muted small">${s(k)}</span></p>`;return`
          <section class="pattern-essay">
            <h3 class="section-title">Deep dive ${v?'<span class="essay-stub-badge muted small">stub</span>':""}</h3>
            ${h("At a glance",n.intro)}
            ${h("Why it matters",n.why_it_matters,v?"Pending native author.":"")}
            ${h("Common pitfalls",n.common_pitfalls)}
            ${h("Contrasts",n.contrasts)}
            ${h("Practice tip",n.closing_practice_tip,v?"Pending native author.":"")}
          </section>
        `})()}

      ${(()=>{const n=D(e);return n?`
          <section class="l1-note">
            <h3 class="section-title">L1 note</h3>
            <p>${s(n)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">Examples (${p.length})</h3>
        <ul class="example-list">${_}</ul>
      </section>

      ${m.length?`
        <section>
          <h3 class="section-title">Common Mistakes / Contrasts</h3>
          <ul class="mistakes-list">${S}</ul>
        </section>
      `:""}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${b(e.meaning_ja)}</p>
      </section>

      ${e.notes?`<section><h3 class="section-title">Notes</h3><p>${s(e.notes)}</p></section>`:""}
    </article>
  `;t.innerHTML=T,document.getElementById("mark-known")?.addEventListener("change",n=>{x.setManuallyKnown(e.id,n.target.checked),G(t,e,a)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{F as buildOrderedPatternList,G as renderGrammarPatternDetail,R as renderGrammarTOC};
