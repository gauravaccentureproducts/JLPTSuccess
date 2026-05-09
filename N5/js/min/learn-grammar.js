import{renderJa as h}from"./furigana.js";import*as j from"./storage.js";import{esc as r,wireExpandCollapseControls as B}from"./learn.js";import{currentLocale as v}from"./i18n.js";function L(t){const e=v();if(e&&e!=="en"){const n=t[`explanation_${e}`];if(typeof n=="string"&&n.trim())return n}return t.explanation_en||""}function U(t){const e=v();if(e&&e!=="en"){const n=t[`meaning_${e}`];if(typeof n=="string"&&n.trim())return n}return t.meaning_en||""}function M(t){const e=v();if(e&&e!=="en"&&t.l1_notes&&typeof t.l1_notes=="object"){const n=t.l1_notes[e];if(typeof n=="string"&&n.trim())return n}return null}const $=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],k={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function C(t){if(typeof t=="object"&&t&&t.id in k)return k[t.id];const e=typeof t=="string"?t:t?.category||"";for(const[n,i]of $)if(i.includes(e))return n;return"Set Phrases and Discourse"}function F(t){const e=new Map;for(const[i]of $)e.set(i,[]);for(const i of t){const l=C(i);e.has(l)&&e.get(l).push(i)}const n=[];for(const[,i]of e)i.sort((l,m)=>(l.patternOrder??0)-(m.patternOrder??0)),n.push(...i);return n}let _="",b="all";function R(t,e,n){return n!=="all"&&(t.tier||"core_n5")!==n?!1:e?[t.pattern,t.meaning_en,t.meaning_ja||"",t.notes||"",(t.examples||[]).map(l=>l.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function P(t,e){const n=new Map;for(const[a]of $)n.set(a,[]);const i=_.trim().toLowerCase(),l=e.patterns.filter(a=>R(a,i,b));for(const a of l){const o=C(a);n.get(o).push(a)}const m=a=>a.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),c=(a,o,u,p)=>`<button type="button" class="kanji-chip ${p?"active":""}"
       data-grammar-filter-group="${a}" data-grammar-filter-value="${o}">${r(u)}</button>`;let d=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${n.size} sections.</p>
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. \u3066-form / wants to / \u3067\u3059)"
        value="${r(_)}" autocomplete="off"
        aria-label="Search grammar patterns">
      <div class="kanji-filter-row" aria-label="Tier filter">
        <span class="kanji-filter-label">Tier:</span>
        ${c("tier","all","All",b==="all")}
        ${c("tier","core_n5","Core N5",b==="core_n5")}
        ${c("tier","late_n5","Late N5",b==="late_n5")}
      </div>
      <p class="kanji-filter-count muted small" aria-live="polite">
        Showing <strong>${l.length}</strong> of ${e.patterns.length}.
      </p>
    </div>
    <div class="toc-controls">
      <button type="button" class="btn-secondary toc-expand-all">Expand all</button>
      <button type="button" class="btn-secondary toc-collapse-all">Collapse all</button>
    </div>
  `;for(const[a,o]of n){if(o.length===0)continue;o.sort((p,g)=>(p.patternOrder??0)-(g.patternOrder??0));const u=i||b!=="all";d+=`<details class="toc-category" id="cat-${m(a)}"${u?" open":""}>`,d+=`<summary><h3>${r(a)} <span class="cat-count muted small">(${o.length})</span></h3></summary>`,d+='<div class="grammar-grid">';for(const p of o)d+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(p.id)}">
          <span class="grammar-pattern" lang="ja">${r(p.pattern)}</span>
        </a>
      `;d+="</div></details>"}l.length===0?d+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(d+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),t.innerHTML=d,B(t,"details.toc-category");const f=document.getElementById("grammar-filter-q");f&&f.addEventListener("input",()=>{_=f.value,P(t,e);const a=document.getElementById("grammar-filter-q");if(a){a.focus();const o=a.value;a.setSelectionRange(o.length,o.length)}}),t.querySelectorAll("[data-grammar-filter-group]").forEach(a=>{a.addEventListener("click",()=>{const o=a.dataset.grammarFilterGroup,u=a.dataset.grammarFilterValue;o==="tier"&&(b=u),P(t,e)})})}const x={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function D(t){return x[t]?x[t]:String(t).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function I(t){const e=t.form_rules?.attaches_to??[],n=t.form_rules?.conjugations??[];if(!e.length&&!n.length)return"";const i=`
    <div class="pattern-usage-header">
      <h3 class="section-title">How to use</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,l=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${r(t.pattern)}">
      <tbody>
        ${e.map((c,d)=>`
          <tr>
            <td class="pattern-usage-pos">${r(D(c))}</td>
            ${d===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${h(t.pattern)}</td>`:""}
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
            <td>${r(c.label||c.form)}</td>
            <td lang="ja">${h(c.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${i}${l}${m}</section>`}function q(t,e,n){const i=e.form_rules?.conjugations??[],l=e.examples??[],m=e.common_mistakes??[],c=j.getPatternEntry(e.id),d=!!c?.isManuallyKnown,f=!!c?.isMastered,a=!!c?.isWeak&&!f,o=Array.isArray(n)?F(n):[],u=o.findIndex(s=>s.id===e.id),p=u>0?o[u-1]:null,g=u>=0&&u<o.length-1?o[u+1]:null,A=p||g?`
    <div class="pattern-nav">
      ${p?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(p.id)}" title="Previous: ${r(p.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${r(p.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${g?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(g.id)}" title="Next: ${r(g.pattern)}"><span class="pattern-nav-name" lang="ja">${r(g.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",E=l.map((s,T)=>{const y=!s.ja||s.ja.includes("(see ")?null:`audio/grammar/${e.id}.${T}.mp3`;return`
    <li>
      <span class="form-tag">${r(s.form||"")}</span>
      ${h(s.ja,s.furigana)}
      ${s.translation_en?`<span class="translation">${r(s.translation_en)}</span>`:""}
      ${y?`<audio class="example-audio" controls preload="none" src="${r(y)}">Audio not available.</audio>`:""}
    </li>
  `}).join(""),w=m.map(s=>`
    <li>
      <div><span class="wrong">${h(s.wrong)}</span></div>
      <div><span class="right">${h(s.right)}</span></div>
      <span class="why">${r(s.why)}</span>
    </li>
  `).join(""),N=f?'<span class="status-badge mastered">\u2605 Mastered</span>':a?'<span class="status-badge weak">Needs practice</span>':"",S=(()=>{const s=e.genki_lesson;return s?`<span class="pattern-lesson-tag" title="Genki ${s.book} Lesson ${s.lesson}">G${s.book}\xB7L${s.lesson}</span>`:""})(),V=`
    <article class="pattern-detail">
      ${A}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 Back to grammar list</a>
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${r(e.pattern)} ${S}</h2>
          <p class="meaning-en">${r(U(e))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${d?"checked":""}>
          <span>Mark as known</span>
          ${N}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} Print / Save as PDF
        </button>
      </div>

      ${I(e)}

      <section>
        <h3 class="section-title">Explanation</h3>
        <p>${r(L(e))}</p>
      </section>

      ${(()=>{const s=M(e);return s?`
          <section class="l1-note">
            <h3 class="section-title">L1 note</h3>
            <p>${r(s)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">Examples (${l.length})</h3>
        <ul class="example-list">${E}</ul>
      </section>

      ${m.length?`
        <section>
          <h3 class="section-title">Common Mistakes / Contrasts</h3>
          <ul class="mistakes-list">${w}</ul>
        </section>
      `:""}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${h(e.meaning_ja)}</p>
      </section>

      ${e.notes?`<section><h3 class="section-title">Notes</h3><p>${r(e.notes)}</p></section>`:""}
    </article>
  `;t.innerHTML=V,document.getElementById("mark-known")?.addEventListener("change",s=>{j.setManuallyKnown(e.id,s.target.checked),q(t,e,n)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{F as buildOrderedPatternList,q as renderGrammarPatternDetail,P as renderGrammarTOC};
