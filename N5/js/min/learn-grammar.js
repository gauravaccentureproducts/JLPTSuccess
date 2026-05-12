import{renderJa as _}from"./furigana.js";import*as L from"./storage.js";import{esc as a,wireExpandCollapseControls as G}from"./learn.js";import{currentLocale as C,t as o}from"./i18n.js";let b=null,A=null;async function W(){return b||A||(A=fetch("data/audio_manifest.json").then(t=>t.ok?t.json():null).then(t=>(t&&Array.isArray(t.items)?b=new Set(t.items.map(e=>e.path)):b=new Set,b)).catch(()=>(b=new Set,b)),A)}function Q(t){return b?b.has(t):!1}function K(t){const e=C();if(e&&e!=="en"){const s=t[`explanation_${e}`];if(typeof s=="string"&&s.trim())return s}return t.explanation_en||""}function J(t){const e=C();if(e&&e!=="en"){const s=t[`meaning_${e}`];if(typeof s=="string"&&s.trim())return s}return t.meaning_en||""}function X(t){const e=C();if(e&&e!=="en"&&t.l1_notes&&typeof t.l1_notes=="object"){const s=t.l1_notes[e];if(typeof s=="string"&&s.trim())return s}return null}const k=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],V={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function T(t){if(typeof t=="object"&&t&&t.id in V)return V[t.id];const e=typeof t=="string"?t:t?.category||"";for(const[s,d]of k)if(d.includes(e))return s;return"Set Phrases and Discourse"}function Y(t){const e=new Map;for(const[d]of k)e.set(d,[]);for(const d of t){const m=T(d);e.has(m)&&e.get(m).push(d)}const s=[];for(const[,d]of e)d.sort((m,$)=>(m.patternOrder??0)-($.patternOrder??0)),s.push(...d);return s}let P="";function Z(t,e){return e?[t.pattern,t.meaning_en,t.meaning_ja||"",t.notes||"",(t.examples||[]).map(d=>d.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function B(t,e){const s=new Map;for(const[r]of k)s.set(r,[]);const d=P.trim().toLowerCase(),m=e.patterns.filter(r=>Z(r,d));for(const r of m){const i=T(r);s.get(i).push(r)}const $=r=>r.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");let l=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${s.size} sections.</p>
  `;for(const[r,i]of s){if(i.length===0)continue;i.sort((c,g)=>(c.patternOrder??0)-(g.patternOrder??0));const p=!!d;l+=`<details class="toc-category" id="cat-${$(r)}"${p?" open":""}>`,l+=`<summary><h3>${a(r)} <span class="cat-count muted small">(${i.length})</span></h3></summary>`,l+='<div class="grammar-grid">';for(const c of i){const g=(()=>{const v=(c.examples||[]).filter(y=>y&&y.ja);return v[0]?v[0].ja:""})(),w=(()=>{const v=C&&C();if(v&&v!=="en"){const y=c[`meaning_${v}`];if(typeof y=="string"&&y.trim())return y}return c.meaning_en||""})();l+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(c.id)}">
          <span class="grammar-pattern" lang="ja">${a(c.pattern)}</span>
          <span class="grammar-card-print-meaning">${a(w)}</span>
          <span class="grammar-card-print-example" lang="ja">${a(g)}</span>
        </a>
      `}l+="</div></details>"}m.length===0?l+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(l+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),l+=`
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
  `,t.innerHTML=l,G(t,"details.toc-category"),t.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const r=Array.from(t.querySelectorAll("details.toc-category")),i=r.map(c=>c.open);r.forEach(c=>{c.open=!0}),document.body.classList.add("is-printing-cheatsheet");const p=()=>{r.forEach((c,g)=>{c.open=i[g]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",p)};window.addEventListener("afterprint",p),window.print()});const f=document.getElementById("grammar-filter-q");if(f){let r=!1;f.addEventListener("compositionstart",()=>{r=!0}),f.addEventListener("compositionend",()=>{r=!1,P=f.value,B(t,e);const i=document.getElementById("grammar-filter-q");if(i){i.focus();const p=i.value;i.setSelectionRange(p.length,p.length)}}),f.addEventListener("input",()=>{if(r)return;P=f.value,B(t,e);const i=document.getElementById("grammar-filter-q");if(i){i.focus();const p=i.value;i.setSelectionRange(p.length,p.length)}})}}const I={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function ee(t){return I[t]?I[t]:String(t).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function te(t){const e=t.form_rules?.attaches_to??[],s=t.form_rules?.conjugations??[];if(!e.length&&!s.length)return"";const d=`
    <div class="pattern-usage-header">
      <h3 class="section-title">${a(o("grammar_detail.how_to_use"))}</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,m=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${a(t.pattern)}">
      <tbody>
        ${e.map((l,f)=>`
          <tr>
            <td class="pattern-usage-pos">${a(ee(l))}</td>
            ${f===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${_(t.pattern)}</td>`:""}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"",$=s.length>=2?`
    <table class="pattern-conjugation-table" aria-label="Conjugation forms">
      <thead>
        <tr><th scope="col">Form</th><th scope="col">Example</th></tr>
      </thead>
      <tbody>
        ${s.map(l=>`
          <tr>
            <td>${a(l.label||l.form)}</td>
            <td lang="ja">${_(l.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${d}${m}${$}</section>`}async function ae(t,e,s){await W();const d=e.form_rules?.conjugations??[],m=e.examples??[],$=e.common_mistakes??[],l=L.getPatternEntry(e.id),f=!!l?.isManuallyKnown,r=!!l?.isMastered,i=!!l?.isWeak&&!r,p=Array.isArray(s)?Y(s):[],c=p.findIndex(n=>n.id===e.id),g=c>0?p[c-1]:null,w=c>=0&&c<p.length-1?p[c+1]:null,v=g||w?`
    <div class="pattern-nav">
      ${g?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(g.id)}" title="Previous: ${a(g.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${a(g.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${w?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(w.id)}" title="Next: ${a(w.pattern)}"><span class="pattern-nav-name" lang="ja">${a(w.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",y=m.map((n,u)=>{const j=!n.ja||n.ja.includes("(see ")?null:`audio/grammar/${e.id}.${u}.mp3`,x=j&&Q(j)?j:null;return`
    <li>
      <span class="form-tag">${a(n.form||"")}</span>
      ${_(n.ja,n.furigana)}
      ${n.translation_en?`<span class="translation">${a(n.translation_en)}</span>`:""}
      ${x?`<audio class="example-audio" controls preload="none" src="${a(x)}"></audio>`:""}
    </li>
  `}).join(""),U=$.map(n=>`
    <li>
      <div><span class="wrong">${_(n.wrong)}</span></div>
      <div><span class="right">${_(n.right)}</span></div>
      <span class="why">${a(n.why)}</span>
    </li>
  `).join(""),E=Array.isArray(e.wrong_corrected_pair)?e.wrong_corrected_pair:[],M=n=>{if(!n)return"";const u=`grammar_detail.cat_${n}`,h=o(u)!==u?o(u):n;return`<span class="error-category-badge cat-${a(n)}">${a(h)}</span>`},R=o("grammar_detail.wcp_wrong"),q=o("grammar_detail.wcp_correct"),D=E.map(n=>`
    <li>
      <div class="wcp-header">${M(n.error_category)}</div>
      <div class="wcp-row wcp-row-wrong">
        <span class="wcp-mark" aria-hidden="true">\u2717</span>
        <span class="wcp-label">${a(R)}</span>
        <span class="wrong">${_(n.wrong)}</span>
      </div>
      <div class="wcp-row wcp-row-correct">
        <span class="wcp-mark" aria-hidden="true">\u2713</span>
        <span class="wcp-label">${a(q)}</span>
        <span class="right">${_(n.correct)}</span>
      </div>
      <span class="why">${a(n.why)}</span>
    </li>
  `).join(""),S=e.politeness_ladder&&typeof e.politeness_ladder=="object"?e.politeness_ladder:null,F=S?`
    <section class="politeness-ladder">
      <h3 class="section-title">${a(o("grammar_detail.ladder_section"))}</h3>
      <table class="ladder-table">
        <tbody>
          ${["casual","polite","humble","respectful"].map(n=>{const u=S[n];if(!u)return"";const h=o(`grammar_detail.ladder_${n}`);return`
              <tr class="ladder-row ladder-${n}">
                <th scope="row">${a(h)}</th>
                <td lang="ja">${_(u)}</td>
              </tr>
            `}).join("")}
        </tbody>
      </table>
    </section>
  `:"",O="",H=r?'<span class="status-badge mastered">\u2605 Mastered</span>':i?'<span class="status-badge weak">Needs practice</span>':"",z=`
    <article class="pattern-detail">
      ${v}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 ${a(o("grammar_detail.back_to_list"))}</a>
      ${e._alias_of?`<p class="pattern-alias-badge muted small">\u2194 <a href="#/learn/${encodeURIComponent(e._alias_of)}">Also see ${a(e._alias_of)}</a> <span class="muted">(dual-coverage of the same concept; different examples)</span></p>`:""}
      ${e._homonym_of?`<p class="pattern-homonym-badge muted small">\u26A0 <a href="#/learn/${encodeURIComponent(e._homonym_of)}">Same kana, different meaning: ${a(e._homonym_of)}</a></p>`:""}
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${a(e.pattern)}</h2>
          <p class="meaning-en">${a(J(e))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${f?"checked":""}>
          <span>${a(o("grammar_detail.mark_as_known"))}</span>
          ${H}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} ${a(o("grammar_detail.print_pdf"))}
        </button>
      </div>

      ${te(e)}

      <section>
        <h3 class="section-title">${a(o("grammar_detail.explanation"))}</h3>
        <p>${a(K(e))}</p>
      </section>

      ${(()=>{const n=e.essay;if(!n||typeof n!="object")return"";const u=n.provenance==="needs_native_review",h=(j,x,N)=>!x&&!N?"":x?`<p><strong>${a(j)}:</strong> ${a(x)}</p>`:`<p><strong>${a(j)}:</strong> <span class="muted small">${a(N)}</span></p>`;return`
          <section class="pattern-essay">
            <h3 class="section-title">${a(o("grammar_detail.deep_dive"))} ${u?'<span class="essay-stub-badge muted small">stub</span>':""}</h3>
            ${h(o("grammar_detail.deep_dive_at_a_glance"),n.intro)}
            ${h(o("grammar_detail.deep_dive_why"),n.why_it_matters,u?"Pending native author.":"")}
            ${h(o("grammar_detail.deep_dive_pitfalls"),n.common_pitfalls)}
            ${h(o("grammar_detail.deep_dive_contrasts"),n.contrasts)}
            ${h(o("grammar_detail.deep_dive_practice"),n.closing_practice_tip,u?"Pending native author.":"")}
            ${h("Cultural / usage context",n.cultural_context)}
          </section>
        `})()}

      ${(()=>{const n=X(e);return n?`
          <section class="l1-note">
            <h3 class="section-title">${a(o("grammar_detail.l1_note"))}</h3>
            <p>${a(n)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">${a(o("grammar_detail.examples"))} (${m.length})</h3>
        <ul class="example-list">${y}</ul>
      </section>

      ${$.length?`
        <section>
          <h3 class="section-title">${a(o("grammar_detail.common_mistakes"))}</h3>
          <ul class="mistakes-list">${U}</ul>
        </section>
      `:""}

      ${E.length?`
        <section class="wrong-corrected-pair">
          <h3 class="section-title">${a(o("grammar_detail.wcp_section"))} (${E.length})</h3>
          <ul class="wcp-list">${D}</ul>
        </section>
      `:""}

      ${F}

      ${O}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${_(e.meaning_ja)}</p>
      </section>

      ${e.notes?`<section><h3 class="section-title">${a(o("grammar_detail.notes"))}</h3><p>${a(e.notes)}</p></section>`:""}

      ${e.cultural_callout?`
        <!-- IMP-WAVE-P2-12 (UI audit fix, 2026-05-11): usage-culture
             callout \u2014 when/why a learner picks this pattern in real
             Japanese situations (business / classroom / casual / etc.). -->
        <section class="grammar-cultural-callout">
          <h3 class="section-title">Cultural usage note</h3>
          <p>${a(e.cultural_callout.note||"")}</p>
          ${Array.isArray(e.cultural_callout.contexts)&&e.cultural_callout.contexts.length?`
            <p class="muted small">
              Contexts: ${e.cultural_callout.contexts.map(n=>`<span class="cultural-context-chip">${a(n)}</span>`).join(" ")}
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
            ${e.authentic_refs.map(n=>{const u=n.split(".")[1]||"authentic";return`<li><a href="#/authentic">${a(n)}</a> <span class="muted small">(${a(u)})</span></li>`}).join("")}
          </ul>
        </section>
      `:""}
    </article>
  `;t.innerHTML=z,document.getElementById("mark-known")?.addEventListener("change",n=>{L.setManuallyKnown(e.id,n.target.checked),ae(t,e,s)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{Y as buildOrderedPatternList,ae as renderGrammarPatternDetail,B as renderGrammarTOC};
