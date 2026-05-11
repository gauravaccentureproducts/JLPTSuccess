import{renderJa as _}from"./furigana.js";import*as T from"./storage.js";import{esc as a,wireExpandCollapseControls as W}from"./learn.js";import{currentLocale as x,t as r}from"./i18n.js";let $=null,A=null;async function K(){return $||A||(A=fetch("data/audio_manifest.json").then(t=>t.ok?t.json():null).then(t=>(t&&Array.isArray(t.items)?$=new Set(t.items.map(e=>e.path)):$=new Set,$)).catch(()=>($=new Set,$)),A)}function J(t){return $?$.has(t):!1}function X(t){const e=x();if(e&&e!=="en"){const s=t[`explanation_${e}`];if(typeof s=="string"&&s.trim())return s}return t.explanation_en||""}function Y(t){const e=x();if(e&&e!=="en"){const s=t[`meaning_${e}`];if(typeof s=="string"&&s.trim())return s}return t.meaning_en||""}function Z(t){const e=x();if(e&&e!=="en"&&t.l1_notes&&typeof t.l1_notes=="object"){const s=t.l1_notes[e];if(typeof s=="string"&&s.trim())return s}return null}const S=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],B={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function U(t){if(typeof t=="object"&&t&&t.id in B)return B[t.id];const e=typeof t=="string"?t:t?.category||"";for(const[s,d]of S)if(d.includes(e))return s;return"Set Phrases and Discourse"}function ee(t){const e=new Map;for(const[d]of S)e.set(d,[]);for(const d of t){const m=U(d);e.has(m)&&e.get(m).push(d)}const s=[];for(const[,d]of e)d.sort((m,b)=>(m.patternOrder??0)-(b.patternOrder??0)),s.push(...d);return s}let P="";function te(t,e){return e?[t.pattern,t.meaning_en,t.meaning_ja||"",t.notes||"",(t.examples||[]).map(d=>d.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function M(t,e){const s=new Map;for(const[o]of S)s.set(o,[]);const d=P.trim().toLowerCase(),m=e.patterns.filter(o=>te(o,d));for(const o of m){const l=U(o);s.get(l).push(o)}const b=o=>o.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");let c=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${s.size} sections.</p>
  `;for(const[o,l]of s){if(l.length===0)continue;l.sort((i,g)=>(i.patternOrder??0)-(g.patternOrder??0));const p=!!d;c+=`<details class="toc-category" id="cat-${b(o)}"${p?" open":""}>`,c+=`<summary><h3>${a(o)} <span class="cat-count muted small">(${l.length})</span></h3></summary>`,c+='<div class="grammar-grid">';for(const i of l){const g=(()=>{const y=(i.examples||[]).filter(w=>w&&w.ja);return y[0]?y[0].ja:""})(),v=i.genki_lesson?`G${i.genki_lesson.book}\xB7L${i.genki_lesson.lesson}`:"",C=(()=>{const y=x&&x();if(y&&y!=="en"){const w=i[`meaning_${y}`];if(typeof w=="string"&&w.trim())return w}return i.meaning_en||""})();c+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(i.id)}">
          <span class="grammar-pattern" lang="ja">${a(i.pattern)}</span>
          <span class="grammar-card-print-meaning">${a(C)}</span>
          <span class="grammar-card-print-example" lang="ja">${a(g)}</span>
          ${v?`<span class="grammar-card-print-lesson">${a(v)}</span>`:""}
        </a>
      `}c+="</div></details>"}m.length===0?c+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(c+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),c+=`
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. \u3066-form / wants to / \u3067\u3059)"
        value="${a(P)}" autocomplete="off"
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
  `,t.innerHTML=c,W(t,"details.toc-category"),t.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const o=Array.from(t.querySelectorAll("details.toc-category")),l=o.map(i=>i.open);o.forEach(i=>{i.open=!0}),document.body.classList.add("is-printing-cheatsheet");const p=()=>{o.forEach((i,g)=>{i.open=l[g]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",p)};window.addEventListener("afterprint",p),window.print()});const f=document.getElementById("grammar-filter-q");if(f){let o=!1;f.addEventListener("compositionstart",()=>{o=!0}),f.addEventListener("compositionend",()=>{o=!1,P=f.value,M(t,e);const l=document.getElementById("grammar-filter-q");if(l){l.focus();const p=l.value;l.setSelectionRange(p.length,p.length)}}),f.addEventListener("input",()=>{if(o)return;P=f.value,M(t,e);const l=document.getElementById("grammar-filter-q");if(l){l.focus();const p=l.value;l.setSelectionRange(p.length,p.length)}})}}const I={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function ne(t){return I[t]?I[t]:String(t).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function ae(t){const e=t.form_rules?.attaches_to??[],s=t.form_rules?.conjugations??[];if(!e.length&&!s.length)return"";const d=`
    <div class="pattern-usage-header">
      <h3 class="section-title">${a(r("grammar_detail.how_to_use"))}</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,m=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${a(t.pattern)}">
      <tbody>
        ${e.map((c,f)=>`
          <tr>
            <td class="pattern-usage-pos">${a(ne(c))}</td>
            ${f===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${_(t.pattern)}</td>`:""}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"",b=s.length>=2?`
    <table class="pattern-conjugation-table" aria-label="Conjugation forms">
      <thead>
        <tr><th scope="col">Form</th><th scope="col">Example</th></tr>
      </thead>
      <tbody>
        ${s.map(c=>`
          <tr>
            <td>${a(c.label||c.form)}</td>
            <td lang="ja">${_(c.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${d}${m}${b}</section>`}async function se(t,e,s){await K();const d=e.form_rules?.conjugations??[],m=e.examples??[],b=e.common_mistakes??[],c=T.getPatternEntry(e.id),f=!!c?.isManuallyKnown,o=!!c?.isMastered,l=!!c?.isWeak&&!o,p=Array.isArray(s)?ee(s):[],i=p.findIndex(n=>n.id===e.id),g=i>0?p[i-1]:null,v=i>=0&&i<p.length-1?p[i+1]:null,C=g||v?`
    <div class="pattern-nav">
      ${g?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(g.id)}" title="Previous: ${a(g.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${a(g.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${v?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(v.id)}" title="Next: ${a(v.pattern)}"><span class="pattern-nav-name" lang="ja">${a(v.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",y=m.map((n,u)=>{const j=!n.ja||n.ja.includes("(see ")?null:`audio/grammar/${e.id}.${u}.mp3`,k=j&&J(j)?j:null;return`
    <li>
      <span class="form-tag">${a(n.form||"")}</span>
      ${_(n.ja,n.furigana)}
      ${n.translation_en?`<span class="translation">${a(n.translation_en)}</span>`:""}
      ${k?`<audio class="example-audio" controls preload="none" src="${a(k)}"></audio>`:""}
    </li>
  `}).join(""),w=b.map(n=>`
    <li>
      <div><span class="wrong">${_(n.wrong)}</span></div>
      <div><span class="right">${_(n.right)}</span></div>
      <span class="why">${a(n.why)}</span>
    </li>
  `).join(""),E=Array.isArray(e.wrong_corrected_pair)?e.wrong_corrected_pair:[],R=n=>{if(!n)return"";const u=`grammar_detail.cat_${n}`,h=r(u)!==u?r(u):n;return`<span class="error-category-badge cat-${a(n)}">${a(h)}</span>`},q=r("grammar_detail.wcp_wrong"),D=r("grammar_detail.wcp_correct"),F=E.map(n=>`
    <li>
      <div class="wcp-header">${R(n.error_category)}</div>
      <div class="wcp-row wcp-row-wrong">
        <span class="wcp-mark" aria-hidden="true">\u2717</span>
        <span class="wcp-label">${a(q)}</span>
        <span class="wrong">${_(n.wrong)}</span>
      </div>
      <div class="wcp-row wcp-row-correct">
        <span class="wcp-mark" aria-hidden="true">\u2713</span>
        <span class="wcp-label">${a(D)}</span>
        <span class="right">${_(n.correct)}</span>
      </div>
      <span class="why">${a(n.why)}</span>
    </li>
  `).join(""),L=e.politeness_ladder&&typeof e.politeness_ladder=="object"?e.politeness_ladder:null,O=L?`
    <section class="politeness-ladder">
      <h3 class="section-title">${a(r("grammar_detail.ladder_section"))}</h3>
      <table class="ladder-table">
        <tbody>
          ${["casual","polite","humble","respectful"].map(n=>{const u=L[n];if(!u)return"";const h=r(`grammar_detail.ladder_${n}`);return`
              <tr class="ladder-row ladder-${n}">
                <th scope="row">${a(h)}</th>
                <td lang="ja">${_(u)}</td>
              </tr>
            `}).join("")}
        </tbody>
      </table>
    </section>
  `:"",N=Array.isArray(e.authentic_citations)?e.authentic_citations:[],G=N.length?`
    <section class="authentic-citations">
      <h3 class="section-title">${a(r("grammar_detail.citations_section"))}</h3>
      <ul class="citations-list">
        ${N.map(n=>`
          <li>
            <strong class="citation-source">${a(n.source||"")}</strong>
            ${n.context?` \u2014 <span class="citation-context">${_(n.context)}</span>`:""}
          </li>
        `).join("")}
      </ul>
    </section>
  `:"",H=o?'<span class="status-badge mastered">\u2605 Mastered</span>':l?'<span class="status-badge weak">Needs practice</span>':"",z=(()=>{const n=e.genki_lesson;return n?`<span class="pattern-lesson-tag" title="Genki ${n.book} Lesson ${n.lesson}">G${n.book}\xB7L${n.lesson}</span>`:""})(),Q=`
    <article class="pattern-detail">
      ${C}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 ${a(r("grammar_detail.back_to_list"))}</a>
      ${e._alias_of?`<p class="pattern-alias-badge muted small">\u2194 <a href="#/learn/${encodeURIComponent(e._alias_of)}">Also see ${a(e._alias_of)}</a> <span class="muted">(dual-coverage of the same concept; different examples)</span></p>`:""}
      ${e._homonym_of?`<p class="pattern-homonym-badge muted small">\u26A0 <a href="#/learn/${encodeURIComponent(e._homonym_of)}">Same kana, different meaning: ${a(e._homonym_of)}</a></p>`:""}
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${a(e.pattern)} ${z}</h2>
          <p class="meaning-en">${a(Y(e))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${f?"checked":""}>
          <span>${a(r("grammar_detail.mark_as_known"))}</span>
          ${H}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} ${a(r("grammar_detail.print_pdf"))}
        </button>
      </div>

      ${ae(e)}

      <section>
        <h3 class="section-title">${a(r("grammar_detail.explanation"))}</h3>
        <p>${a(X(e))}</p>
      </section>

      ${(()=>{const n=e.essay;if(!n||typeof n!="object")return"";const u=n.provenance==="needs_native_review",h=(j,k,V)=>!k&&!V?"":k?`<p><strong>${a(j)}:</strong> ${a(k)}</p>`:`<p><strong>${a(j)}:</strong> <span class="muted small">${a(V)}</span></p>`;return`
          <section class="pattern-essay">
            <h3 class="section-title">${a(r("grammar_detail.deep_dive"))} ${u?'<span class="essay-stub-badge muted small">stub</span>':""}</h3>
            ${h(r("grammar_detail.deep_dive_at_a_glance"),n.intro)}
            ${h(r("grammar_detail.deep_dive_why"),n.why_it_matters,u?"Pending native author.":"")}
            ${h(r("grammar_detail.deep_dive_pitfalls"),n.common_pitfalls)}
            ${h(r("grammar_detail.deep_dive_contrasts"),n.contrasts)}
            ${h(r("grammar_detail.deep_dive_practice"),n.closing_practice_tip,u?"Pending native author.":"")}
          </section>
        `})()}

      ${(()=>{const n=Z(e);return n?`
          <section class="l1-note">
            <h3 class="section-title">${a(r("grammar_detail.l1_note"))}</h3>
            <p>${a(n)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">${a(r("grammar_detail.examples"))} (${m.length})</h3>
        <ul class="example-list">${y}</ul>
      </section>

      ${b.length?`
        <section>
          <h3 class="section-title">${a(r("grammar_detail.common_mistakes"))}</h3>
          <ul class="mistakes-list">${w}</ul>
        </section>
      `:""}

      ${E.length?`
        <section class="wrong-corrected-pair">
          <h3 class="section-title">${a(r("grammar_detail.wcp_section"))} (${E.length})</h3>
          <ul class="wcp-list">${F}</ul>
        </section>
      `:""}

      ${O}

      ${G}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${_(e.meaning_ja)}</p>
      </section>

      ${e.notes?`<section><h3 class="section-title">${a(r("grammar_detail.notes"))}</h3><p>${a(e.notes)}</p></section>`:""}
    </article>
  `;t.innerHTML=Q,document.getElementById("mark-known")?.addEventListener("change",n=>{T.setManuallyKnown(e.id,n.target.checked),se(t,e,s)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{ee as buildOrderedPatternList,se as renderGrammarPatternDetail,M as renderGrammarTOC};
