import{renderJa as b}from"./furigana.js";import*as k from"./storage.js";import{esc as s,wireExpandCollapseControls as U}from"./learn.js";import{currentLocale as C}from"./i18n.js";function M(t){const e=C();if(e&&e!=="en"){const a=t[`explanation_${e}`];if(typeof a=="string"&&a.trim())return a}return t.explanation_en||""}function D(t){const e=C();if(e&&e!=="en"){const a=t[`meaning_${e}`];if(typeof a=="string"&&a.trim())return a}return t.meaning_en||""}function I(t){const e=C();if(e&&e!=="en"&&t.l1_notes&&typeof t.l1_notes=="object"){const a=t.l1_notes[e];if(typeof a=="string"&&a.trim())return a}return null}const w=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],x={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function A(t){if(typeof t=="object"&&t&&t.id in x)return x[t.id];const e=typeof t=="string"?t:t?.category||"";for(const[a,c]of w)if(c.includes(e))return a;return"Set Phrases and Discourse"}function R(t){const e=new Map;for(const[c]of w)e.set(c,[]);for(const c of t){const d=A(c);e.has(d)&&e.get(d).push(c)}const a=[];for(const[,c]of e)c.sort((d,g)=>(d.patternOrder??0)-(g.patternOrder??0)),a.push(...c);return a}let j="";function F(t,e){return e?[t.pattern,t.meaning_en,t.meaning_ja||"",t.notes||"",(t.examples||[]).map(c=>c.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function S(t,e){const a=new Map;for(const[r]of w)a.set(r,[]);const c=j.trim().toLowerCase(),d=e.patterns.filter(r=>F(r,c));for(const r of d){const i=A(r);a.get(i).push(r)}const g=r=>r.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");let l=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${a.size} sections.</p>
  `;for(const[r,i]of a){if(i.length===0)continue;i.sort((o,u)=>(o.patternOrder??0)-(u.patternOrder??0));const p=!!c;l+=`<details class="toc-category" id="cat-${g(r)}"${p?" open":""}>`,l+=`<summary><h3>${s(r)} <span class="cat-count muted small">(${i.length})</span></h3></summary>`,l+='<div class="grammar-grid">';for(const o of i){const u=(()=>{const y=(o.examples||[]).filter(_=>_&&_.ja);return y[0]?y[0].ja:""})(),f=o.genki_lesson?`G${o.genki_lesson.book}\xB7L${o.genki_lesson.lesson}`:"";l+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(o.id)}">
          <span class="grammar-pattern" lang="ja">${s(o.pattern)}</span>
          <span class="grammar-card-print-meaning">${s(o.meaning_en||"")}</span>
          <span class="grammar-card-print-example" lang="ja">${s(u)}</span>
          ${f?`<span class="grammar-card-print-lesson">${s(f)}</span>`:""}
        </a>
      `}l+="</div></details>"}d.length===0?l+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(l+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),l+=`
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. \u3066-form / wants to / \u3067\u3059)"
        value="${s(j)}" autocomplete="off"
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
  `,t.innerHTML=l,U(t,"details.toc-category"),t.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const r=Array.from(t.querySelectorAll("details.toc-category")),i=r.map(o=>o.open);r.forEach(o=>{o.open=!0}),document.body.classList.add("is-printing-cheatsheet");const p=()=>{r.forEach((o,u)=>{o.open=i[u]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",p)};window.addEventListener("afterprint",p),window.print()});const m=document.getElementById("grammar-filter-q");if(m){let r=!1;m.addEventListener("compositionstart",()=>{r=!0}),m.addEventListener("compositionend",()=>{r=!1,j=m.value,S(t,e);const i=document.getElementById("grammar-filter-q");if(i){i.focus();const p=i.value;i.setSelectionRange(p.length,p.length)}}),m.addEventListener("input",()=>{if(r)return;j=m.value,S(t,e);const i=document.getElementById("grammar-filter-q");if(i){i.focus();const p=i.value;i.setSelectionRange(p.length,p.length)}})}}const L={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function q(t){return L[t]?L[t]:String(t).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function O(t){const e=t.form_rules?.attaches_to??[],a=t.form_rules?.conjugations??[];if(!e.length&&!a.length)return"";const c=`
    <div class="pattern-usage-header">
      <h3 class="section-title">How to use</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,d=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${s(t.pattern)}">
      <tbody>
        ${e.map((l,m)=>`
          <tr>
            <td class="pattern-usage-pos">${s(q(l))}</td>
            ${m===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${b(t.pattern)}</td>`:""}
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
        ${a.map(l=>`
          <tr>
            <td>${s(l.label||l.form)}</td>
            <td lang="ja">${b(l.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${c}${d}${g}</section>`}function G(t,e,a){const c=e.form_rules?.conjugations??[],d=e.examples??[],g=e.common_mistakes??[],l=k.getPatternEntry(e.id),m=!!l?.isManuallyKnown,r=!!l?.isMastered,i=!!l?.isWeak&&!r,p=Array.isArray(a)?R(a):[],o=p.findIndex(n=>n.id===e.id),u=o>0?p[o-1]:null,f=o>=0&&o<p.length-1?p[o+1]:null,y=u||f?`
    <div class="pattern-nav">
      ${u?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(u.id)}" title="Previous: ${s(u.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${s(u.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${f?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(f.id)}" title="Next: ${s(f.pattern)}"><span class="pattern-nav-name" lang="ja">${s(f.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",_=d.map((n,v)=>{const $=!n.ja||n.ja.includes("(see ")?null:`audio/grammar/${e.id}.${v}.mp3`;return`
    <li>
      <span class="form-tag">${s(n.form||"")}</span>
      ${b(n.ja,n.furigana)}
      ${n.translation_en?`<span class="translation">${s(n.translation_en)}</span>`:""}
      ${$?`<audio class="example-audio" controls preload="none" src="${s($)}">Audio not available.</audio>`:""}
    </li>
  `}).join(""),N=g.map(n=>`
    <li>
      <div><span class="wrong">${b(n.wrong)}</span></div>
      <div><span class="right">${b(n.right)}</span></div>
      <span class="why">${s(n.why)}</span>
    </li>
  `).join(""),V=r?'<span class="status-badge mastered">\u2605 Mastered</span>':i?'<span class="status-badge weak">Needs practice</span>':"",T=(()=>{const n=e.genki_lesson;return n?`<span class="pattern-lesson-tag" title="Genki ${n.book} Lesson ${n.lesson}">G${n.book}\xB7L${n.lesson}</span>`:""})(),B=`
    <article class="pattern-detail">
      ${y}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 Back to grammar list</a>
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${s(e.pattern)} ${T}</h2>
          <p class="meaning-en">${s(D(e))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${m?"checked":""}>
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
        <p>${s(M(e))}</p>
      </section>

      ${(()=>{const n=e.essay;if(!n||typeof n!="object")return"";const v=n.provenance==="needs_native_review",h=($,P,E)=>!P&&!E?"":P?`<p><strong>${s($)}:</strong> ${s(P)}</p>`:`<p><strong>${s($)}:</strong> <span class="muted small">${s(E)}</span></p>`;return`
          <section class="pattern-essay">
            <h3 class="section-title">Deep dive ${v?'<span class="essay-stub-badge muted small">stub</span>':""}</h3>
            ${h("At a glance",n.intro)}
            ${h("Why it matters",n.why_it_matters,v?"Pending native author.":"")}
            ${h("Common pitfalls",n.common_pitfalls)}
            ${h("Contrasts",n.contrasts)}
            ${h("Practice tip",n.closing_practice_tip,v?"Pending native author.":"")}
          </section>
        `})()}

      ${(()=>{const n=I(e);return n?`
          <section class="l1-note">
            <h3 class="section-title">L1 note</h3>
            <p>${s(n)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">Examples (${d.length})</h3>
        <ul class="example-list">${_}</ul>
      </section>

      ${g.length?`
        <section>
          <h3 class="section-title">Common Mistakes / Contrasts</h3>
          <ul class="mistakes-list">${N}</ul>
        </section>
      `:""}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${b(e.meaning_ja)}</p>
      </section>

      ${e.notes?`<section><h3 class="section-title">Notes</h3><p>${s(e.notes)}</p></section>`:""}
    </article>
  `;t.innerHTML=B,document.getElementById("mark-known")?.addEventListener("change",n=>{k.setManuallyKnown(e.id,n.target.checked),G(t,e,a)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{R as buildOrderedPatternList,G as renderGrammarPatternDetail,S as renderGrammarTOC};
