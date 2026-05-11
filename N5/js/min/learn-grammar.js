import{renderJa as _}from"./furigana.js";import*as V from"./storage.js";import{esc as n,wireExpandCollapseControls as Q}from"./learn.js";import{currentLocale as A,t as r}from"./i18n.js";let $=null,k=null;async function K(){return $||k||(k=fetch("data/audio_manifest.json").then(a=>a.ok?a.json():null).then(a=>(a&&Array.isArray(a.items)?$=new Set(a.items.map(e=>e.path)):$=new Set,$)).catch(()=>($=new Set,$)),k)}function J(a){return $?$.has(a):!1}function X(a){const e=A();if(e&&e!=="en"){const s=a[`explanation_${e}`];if(typeof s=="string"&&s.trim())return s}return a.explanation_en||""}function Y(a){const e=A();if(e&&e!=="en"){const s=a[`meaning_${e}`];if(typeof s=="string"&&s.trim())return s}return a.meaning_en||""}function Z(a){const e=A();if(e&&e!=="en"&&a.l1_notes&&typeof a.l1_notes=="object"){const s=a.l1_notes[e];if(typeof s=="string"&&s.trim())return s}return null}const S=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],B={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function I(a){if(typeof a=="object"&&a&&a.id in B)return B[a.id];const e=typeof a=="string"?a:a?.category||"";for(const[s,d]of S)if(d.includes(e))return s;return"Set Phrases and Discourse"}function ee(a){const e=new Map;for(const[d]of S)e.set(d,[]);for(const d of a){const m=I(d);e.has(m)&&e.get(m).push(d)}const s=[];for(const[,d]of e)d.sort((m,b)=>(m.patternOrder??0)-(b.patternOrder??0)),s.push(...d);return s}let C="";function te(a,e){return e?[a.pattern,a.meaning_en,a.meaning_ja||"",a.notes||"",(a.examples||[]).map(d=>d.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function U(a,e){const s=new Map;for(const[o]of S)s.set(o,[]);const d=C.trim().toLowerCase(),m=e.patterns.filter(o=>te(o,d));for(const o of m){const l=I(o);s.get(l).push(o)}const b=o=>o.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");let c=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${s.size} sections.</p>
  `;for(const[o,l]of s){if(l.length===0)continue;l.sort((i,g)=>(i.patternOrder??0)-(g.patternOrder??0));const p=!!d;c+=`<details class="toc-category" id="cat-${b(o)}"${p?" open":""}>`,c+=`<summary><h3>${n(o)} <span class="cat-count muted small">(${l.length})</span></h3></summary>`,c+='<div class="grammar-grid">';for(const i of l){const g=(()=>{const y=(i.examples||[]).filter(w=>w&&w.ja);return y[0]?y[0].ja:""})(),v=i.genki_lesson?`G${i.genki_lesson.book}\xB7L${i.genki_lesson.lesson}`:"",P=(()=>{const y=A&&A();if(y&&y!=="en"){const w=i[`meaning_${y}`];if(typeof w=="string"&&w.trim())return w}return i.meaning_en||""})();c+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(i.id)}">
          <span class="grammar-pattern" lang="ja">${n(i.pattern)}</span>
          <span class="grammar-card-print-meaning">${n(P)}</span>
          <span class="grammar-card-print-example" lang="ja">${n(g)}</span>
          ${v?`<span class="grammar-card-print-lesson">${n(v)}</span>`:""}
        </a>
      `}c+="</div></details>"}m.length===0?c+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(c+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),c+=`
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. \u3066-form / wants to / \u3067\u3059)"
        value="${n(C)}" autocomplete="off"
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
  `,a.innerHTML=c,Q(a,"details.toc-category"),a.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const o=Array.from(a.querySelectorAll("details.toc-category")),l=o.map(i=>i.open);o.forEach(i=>{i.open=!0}),document.body.classList.add("is-printing-cheatsheet");const p=()=>{o.forEach((i,g)=>{i.open=l[g]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",p)};window.addEventListener("afterprint",p),window.print()});const h=document.getElementById("grammar-filter-q");if(h){let o=!1;h.addEventListener("compositionstart",()=>{o=!0}),h.addEventListener("compositionend",()=>{o=!1,C=h.value,U(a,e);const l=document.getElementById("grammar-filter-q");if(l){l.focus();const p=l.value;l.setSelectionRange(p.length,p.length)}}),h.addEventListener("input",()=>{if(o)return;C=h.value,U(a,e);const l=document.getElementById("grammar-filter-q");if(l){l.focus();const p=l.value;l.setSelectionRange(p.length,p.length)}})}}const M={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function ae(a){return M[a]?M[a]:String(a).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function ne(a){const e=a.form_rules?.attaches_to??[],s=a.form_rules?.conjugations??[];if(!e.length&&!s.length)return"";const d=`
    <div class="pattern-usage-header">
      <h3 class="section-title">${n(r("grammar_detail.how_to_use"))}</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,m=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${n(a.pattern)}">
      <tbody>
        ${e.map((c,h)=>`
          <tr>
            <td class="pattern-usage-pos">${n(ae(c))}</td>
            ${h===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${_(a.pattern)}</td>`:""}
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
            <td>${n(c.label||c.form)}</td>
            <td lang="ja">${_(c.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${d}${m}${b}</section>`}async function se(a,e,s){await K();const d=e.form_rules?.conjugations??[],m=e.examples??[],b=e.common_mistakes??[],c=V.getPatternEntry(e.id),h=!!c?.isManuallyKnown,o=!!c?.isMastered,l=!!c?.isWeak&&!o,p=Array.isArray(s)?ee(s):[],i=p.findIndex(t=>t.id===e.id),g=i>0?p[i-1]:null,v=i>=0&&i<p.length-1?p[i+1]:null,P=g||v?`
    <div class="pattern-nav">
      ${g?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(g.id)}" title="Previous: ${n(g.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${n(g.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${v?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(v.id)}" title="Next: ${n(v.pattern)}"><span class="pattern-nav-name" lang="ja">${n(v.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",y=m.map((t,u)=>{const j=!t.ja||t.ja.includes("(see ")?null:`audio/grammar/${e.id}.${u}.mp3`,x=j&&J(j)?j:null;return`
    <li>
      <span class="form-tag">${n(t.form||"")}</span>
      ${_(t.ja,t.furigana)}
      ${t.translation_en?`<span class="translation">${n(t.translation_en)}</span>`:""}
      ${x?`<audio class="example-audio" controls preload="none" src="${n(x)}"></audio>`:""}
    </li>
  `}).join(""),w=b.map(t=>`
    <li>
      <div><span class="wrong">${_(t.wrong)}</span></div>
      <div><span class="right">${_(t.right)}</span></div>
      <span class="why">${n(t.why)}</span>
    </li>
  `).join(""),E=Array.isArray(e.wrong_corrected_pair)?e.wrong_corrected_pair:[],R=t=>{if(!t)return"";const u=`grammar_detail.cat_${t}`,f=r(u)!==u?r(u):t;return`<span class="error-category-badge cat-${n(t)}">${n(f)}</span>`},q=r("grammar_detail.wcp_wrong"),D=r("grammar_detail.wcp_correct"),F=E.map(t=>`
    <li>
      <div class="wcp-header">${R(t.error_category)}</div>
      <div class="wcp-row wcp-row-wrong">
        <span class="wcp-mark" aria-hidden="true">\u2717</span>
        <span class="wcp-label">${n(q)}</span>
        <span class="wrong">${_(t.wrong)}</span>
      </div>
      <div class="wcp-row wcp-row-correct">
        <span class="wcp-mark" aria-hidden="true">\u2713</span>
        <span class="wcp-label">${n(D)}</span>
        <span class="right">${_(t.correct)}</span>
      </div>
      <span class="why">${n(t.why)}</span>
    </li>
  `).join(""),L=e.politeness_ladder&&typeof e.politeness_ladder=="object"?e.politeness_ladder:null,O=L?`
    <section class="politeness-ladder">
      <h3 class="section-title">${n(r("grammar_detail.ladder_section"))}</h3>
      <table class="ladder-table">
        <tbody>
          ${["casual","polite","humble","respectful"].map(t=>{const u=L[t];if(!u)return"";const f=r(`grammar_detail.ladder_${t}`);return`
              <tr class="ladder-row ladder-${t}">
                <th scope="row">${n(f)}</th>
                <td lang="ja">${_(u)}</td>
              </tr>
            `}).join("")}
        </tbody>
      </table>
    </section>
  `:"",N=Array.isArray(e.authentic_citations)?e.authentic_citations:[],G=N.length?`
    <section class="authentic-citations">
      <h3 class="section-title">${n(r("grammar_detail.citations_section"))}</h3>
      <ul class="citations-list">
        ${N.map(t=>`
          <li>
            <strong class="citation-source">${n(t.source||"")}</strong>
            ${t.context?` \u2014 <span class="citation-context">${_(t.context)}</span>`:""}
          </li>
        `).join("")}
      </ul>
    </section>
  `:"",H=o?'<span class="status-badge mastered">\u2605 Mastered</span>':l?'<span class="status-badge weak">Needs practice</span>':"",z=(()=>{const t=e.genki_lesson;return t?`<span class="pattern-lesson-tag" title="Genki ${t.book} Lesson ${t.lesson}">G${t.book}\xB7L${t.lesson}</span>`:""})(),W=`
    <article class="pattern-detail">
      ${P}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 ${n(r("grammar_detail.back_to_list"))}</a>
      ${e._alias_of?`<p class="pattern-alias-badge muted small">\u2194 <a href="#/learn/${encodeURIComponent(e._alias_of)}">Also see ${n(e._alias_of)}</a> <span class="muted">(dual-coverage of the same concept; different examples)</span></p>`:""}
      ${e._homonym_of?`<p class="pattern-homonym-badge muted small">\u26A0 <a href="#/learn/${encodeURIComponent(e._homonym_of)}">Same kana, different meaning: ${n(e._homonym_of)}</a></p>`:""}
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${n(e.pattern)} ${z}</h2>
          <p class="meaning-en">${n(Y(e))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${h?"checked":""}>
          <span>${n(r("grammar_detail.mark_as_known"))}</span>
          ${H}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} ${n(r("grammar_detail.print_pdf"))}
        </button>
      </div>

      ${ne(e)}

      <section>
        <h3 class="section-title">${n(r("grammar_detail.explanation"))}</h3>
        <p>${n(X(e))}</p>
      </section>

      ${(()=>{const t=e.essay;if(!t||typeof t!="object")return"";const u=t.provenance==="needs_native_review",f=(j,x,T)=>!x&&!T?"":x?`<p><strong>${n(j)}:</strong> ${n(x)}</p>`:`<p><strong>${n(j)}:</strong> <span class="muted small">${n(T)}</span></p>`;return`
          <section class="pattern-essay">
            <h3 class="section-title">${n(r("grammar_detail.deep_dive"))} ${u?'<span class="essay-stub-badge muted small">stub</span>':""}</h3>
            ${f(r("grammar_detail.deep_dive_at_a_glance"),t.intro)}
            ${f(r("grammar_detail.deep_dive_why"),t.why_it_matters,u?"Pending native author.":"")}
            ${f(r("grammar_detail.deep_dive_pitfalls"),t.common_pitfalls)}
            ${f(r("grammar_detail.deep_dive_contrasts"),t.contrasts)}
            ${f(r("grammar_detail.deep_dive_practice"),t.closing_practice_tip,u?"Pending native author.":"")}
          </section>
        `})()}

      ${(()=>{const t=Z(e);return t?`
          <section class="l1-note">
            <h3 class="section-title">${n(r("grammar_detail.l1_note"))}</h3>
            <p>${n(t)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">${n(r("grammar_detail.examples"))} (${m.length})</h3>
        <ul class="example-list">${y}</ul>
      </section>

      ${b.length?`
        <section>
          <h3 class="section-title">${n(r("grammar_detail.common_mistakes"))}</h3>
          <ul class="mistakes-list">${w}</ul>
        </section>
      `:""}

      ${E.length?`
        <section class="wrong-corrected-pair">
          <h3 class="section-title">${n(r("grammar_detail.wcp_section"))} (${E.length})</h3>
          <ul class="wcp-list">${F}</ul>
        </section>
      `:""}

      ${O}

      ${G}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${_(e.meaning_ja)}</p>
      </section>

      ${e.notes?`<section><h3 class="section-title">${n(r("grammar_detail.notes"))}</h3><p>${n(e.notes)}</p></section>`:""}

      ${e.cultural_callout?`
        <!-- IMP-WAVE-P2-12 (UI audit fix, 2026-05-11): usage-culture
             callout \u2014 when/why a learner picks this pattern in real
             Japanese situations (business / classroom / casual / etc.). -->
        <section class="grammar-cultural-callout">
          <h3 class="section-title">Cultural usage note</h3>
          <p>${n(e.cultural_callout.note||"")}</p>
          ${Array.isArray(e.cultural_callout.contexts)&&e.cultural_callout.contexts.length?`
            <p class="muted small">
              Contexts: ${e.cultural_callout.contexts.map(t=>`<span class="cultural-context-chip">${n(t)}</span>`).join(" ")}
            </p>
          `:""}
        </section>
      `:""}

      ${e.authentic_refs?.length?`
        <!-- IMP-WAVE-AUTHENTIC-XLINK (2026-05-11): authentic-content
             cross-link. Real-world cards where this grammar pattern
             appears (signs, menus, transit announcements, etc.). -->
        <section class="grammar-authentic-refs">
          <h3 class="section-title">Seen in the real world</h3>
          <p class="muted small">
            This pattern shows up on these authentic Japanese cards. Click to see real-world usage in context.
          </p>
          <ul class="authentic-ref-list">
            ${e.authentic_refs.map(t=>{const u=t.split(".")[1]||"authentic";return`<li><a href="#/authentic">${n(t)}</a> <span class="muted small">(${n(u)})</span></li>`}).join("")}
          </ul>
        </section>
      `:""}
    </article>
  `;a.innerHTML=W,document.getElementById("mark-known")?.addEventListener("change",t=>{V.setManuallyKnown(e.id,t.target.checked),se(a,e,s)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{ee as buildOrderedPatternList,se as renderGrammarPatternDetail,U as renderGrammarTOC};
