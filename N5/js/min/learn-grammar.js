import{renderJa as b}from"./furigana.js";import*as B from"./storage.js";import{esc as a,wireExpandCollapseControls as te}from"./learn.js";import{currentLocale as A,t as r}from"./i18n.js";import{assetUrl as ae}from"./router.js";let v=null,C=null;async function ne(){return v||C||(C=fetch("data/audio_manifest.json").then(n=>n.ok?n.json():null).then(n=>(n&&Array.isArray(n.items)?v=new Set(n.items.map(t=>t.path)):v=new Set,v)).catch(()=>(v=new Set,v)),C)}function se(n){return v?v.has(n):!1}function re(n){const t=A();if(t&&t!=="en"){const s=n[`explanation_${t}`];if(typeof s=="string"&&s.trim())return s}return n.explanation_en||""}function T(n){const t=A();if(t&&t!=="en"){const s=n[`meaning_${t}`];if(typeof s=="string"&&s.trim())return s}return n.meaning_en||""}function oe(n){const t=A();if(t&&t!=="en"&&n.l1_notes&&typeof n.l1_notes=="object"){const s=n.l1_notes[t];if(typeof s=="string"&&s.trim())return s}return null}const S=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],U={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function q(n){if(typeof n=="object"&&n&&n.id in U)return U[n.id];const t=typeof n=="string"?n:n?.category||"";for(const[s,u]of S)if(u.includes(t))return s;return"Set Phrases and Discourse"}function ie(n){const t=new Map;for(const[u]of S)t.set(u,[]);for(const u of n){const g=q(u);t.has(g)&&t.get(g).push(u)}const s=[];for(const[,u]of t)u.sort((g,y)=>(g.patternOrder??0)-(y.patternOrder??0)),s.push(...u);return s}let P="";function le(n,t){return t?[n.pattern,n.meaning_en,n.meaning_ja||"",n.notes||"",(n.examples||[]).map(u=>u.ja).join(" ")].join(" ").toLowerCase().includes(t):!0}function I(n,t){const s=new Map;for(const[o]of S)s.set(o,[]);const u=P.trim().toLowerCase(),g=t.patterns.filter(o=>le(o,u));for(const o of g){const l=q(o);s.get(l).push(o)}const y=o=>o.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");let c=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${t.patterns.length} patterns in ${s.size} sections.</p>
  `;for(const[o,l]of s){if(l.length===0)continue;l.sort((d,h)=>(d.patternOrder??0)-(h.patternOrder??0));const m=!!u;c+=`<details class="toc-category" id="cat-${y(o)}"${m?" open":""}>`,c+=`<summary><h3>${a(o)} <span class="cat-count muted small">(${l.length})</span></h3></summary>`,c+='<div class="grammar-grid">';for(const d of l){const h=(()=>{const w=(d.examples||[]).filter(j=>j&&j.ja);return w[0]?w[0].ja:""})(),x=(()=>{const w=A&&A();if(w&&w!=="en"){const j=d[`meaning_${w}`];if(typeof j=="string"&&j.trim())return j}return d.meaning_en||""})();c+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(d.id)}">
          <span class="grammar-pattern" lang="ja">${a(d.pattern)}</span>
          <span class="grammar-card-print-meaning">${a(x)}</span>
          <span class="grammar-card-print-example" lang="ja">${a(h)}</span>
        </a>
      `}c+="</div></details>"}g.length===0?c+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':t.patterns.length===1&&(c+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),c+=`
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
  `,n.innerHTML=c,te(n,"details.toc-category"),n.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const o=Array.from(n.querySelectorAll("details.toc-category")),l=o.map(d=>d.open);o.forEach(d=>{d.open=!0}),document.body.classList.add("is-printing-cheatsheet");const m=()=>{o.forEach((d,h)=>{d.open=l[h]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",m)};window.addEventListener("afterprint",m),window.print()});const _=document.getElementById("grammar-filter-q");if(_){let o=!1;_.addEventListener("compositionstart",()=>{o=!0}),_.addEventListener("compositionend",()=>{o=!1,P=_.value,I(n,t);const l=document.getElementById("grammar-filter-q");if(l){l.focus();const m=l.value;l.setSelectionRange(m.length,m.length)}}),_.addEventListener("input",()=>{if(o)return;P=_.value,I(n,t);const l=document.getElementById("grammar-filter-q");if(l){l.focus();const m=l.value;l.setSelectionRange(m.length,m.length)}})}}const M={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function ce(n){return M[n]?M[n]:String(n).replace(/_/g," ").replace(/^./,t=>t.toUpperCase())}function de(n){const t=n.form_rules?.attaches_to??[],s=n.form_rules?.conjugations??[];if(!t.length&&!s.length)return"";const u=`
    <div class="pattern-usage-header">
      <h3 class="section-title">${a(r("grammar_detail.how_to_use"))}</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,g=t.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${a(n.pattern)}">
      <tbody>
        ${t.map((c,_)=>`
          <tr>
            <td class="pattern-usage-pos">${a(ce(c))}</td>
            ${_===0?`<td class="pattern-usage-form" rowspan="${t.length}" lang="ja">${b(n.pattern)}</td>`:""}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"",y=s.length>=2?`
    <table class="pattern-conjugation-table" aria-label="Conjugation forms">
      <thead>
        <tr><th scope="col">Form</th><th scope="col">Example</th></tr>
      </thead>
      <tbody>
        ${s.map(c=>`
          <tr>
            <td>${a(c.label||c.form)}</td>
            <td lang="ja">${b(c.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${u}${g}${y}</section>`}async function pe(n,t,s){await ne();const u=t.form_rules?.conjugations??[],g=t.examples??[],y=t.common_mistakes??[],c=B.getPatternEntry(t.id),_=!!c?.isManuallyKnown,o=!!c?.isMastered,l=!!c?.isWeak&&!o,m=Array.isArray(s)?ie(s):[],d=m.findIndex(e=>e.id===t.id),h=d>0?m[d-1]:null,x=d>=0&&d<m.length-1?m[d+1]:null,w=h||x?`
    <div class="pattern-nav">
      ${h?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(h.id)}" title="Previous: ${a(h.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${a(h.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${x?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(x.id)}" title="Next: ${a(x.pattern)}"><span class="pattern-nav-name" lang="ja">${a(x.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",j=g.map((e,i)=>{const f=!e.ja||e.ja.includes("(see ")?null:`audio/grammar/${t.id}.${i}.mp3`,$=f&&se(f)?f:null;return`
    <li>
      <span class="form-tag">${a(e.form||"")}</span>
      ${b(e.ja,e.furigana)}
      ${e.translation_en?`<span class="translation">${a(e.translation_en)}</span>`:""}
      ${$?`<audio class="example-audio" controls preload="none" src="${a(ae($))}"></audio>`:""}
    </li>
  `}).join(""),R=y.map(e=>{if(e.kind==="register_variant"){const i=e.label_a?`<span class="variant-label">${a(e.label_a)}</span>`:"",p=e.label_b?`<span class="variant-label">${a(e.label_b)}</span>`:"",f=e.form_a??e.wrong??"",$=e.form_b??e.right??"";return`
        <li class="variant-pair">
          <div class="variant-row">${i}<span class="variant-form">${b(f)}</span></div>
          <div class="variant-row">${p}<span class="variant-form">${b($)}</span></div>
          <span class="why">${a(e.why)}</span>
        </li>
      `}return`
      <li>
        <div><span class="wrong">${b(e.wrong)}</span></div>
        <div><span class="right">${b(e.right)}</span></div>
        <span class="why">${a(e.why)}</span>
      </li>
    `}).join(""),E=Array.isArray(t.wrong_corrected_pair)?t.wrong_corrected_pair:[],D=e=>{if(!e)return"";const i=`grammar_detail.cat_${e}`,p=r(i)!==i?r(i):e;return`<span class="error-category-badge cat-${a(e)}">${a(p)}</span>`},F=r("grammar_detail.wcp_wrong"),H=r("grammar_detail.wcp_correct"),O=E.map(e=>`
    <li>
      <div class="wcp-header">${D(e.error_category)}</div>
      <div class="wcp-row wcp-row-wrong">
        <span class="wcp-mark" aria-hidden="true">\u2717</span>
        <span class="wcp-label">${a(F)}</span>
        <span class="wrong">${b(e.wrong)}</span>
      </div>
      <div class="wcp-row wcp-row-correct">
        <span class="wcp-mark" aria-hidden="true">\u2713</span>
        <span class="wcp-label">${a(H)}</span>
        <span class="right">${b(e.correct)}</span>
      </div>
      <span class="why">${a(e.why)}</span>
    </li>
  `).join(""),L=t.politeness_ladder&&typeof t.politeness_ladder=="object"?t.politeness_ladder:null,z=L?`
    <section class="politeness-ladder">
      <h3 class="section-title">${a(r("grammar_detail.ladder_section"))}</h3>
      <table class="ladder-table">
        <tbody>
          ${["casual","polite","humble","respectful"].map(e=>{const i=L[e];if(!i)return"";const p=r(`grammar_detail.ladder_${e}`);return`
              <tr class="ladder-row ladder-${e}">
                <th scope="row">${a(p)}</th>
                <td lang="ja">${b(i)}</td>
              </tr>
            `}).join("")}
        </tbody>
      </table>
    </section>
  `:"",G="",N=Array.isArray(t.public_domain_refs)?t.public_domain_refs:[],W=N.length?`
    <section class="pd-refs">
      <h3 class="section-title">Public-domain references</h3>
      <ul class="pd-refs-list">
        ${N.map(e=>{const i=a(e.source_type||"?"),p=a(e.work_title||""),f=a(e.author||""),$=e.author_death_year?` (died ${e.author_death_year})`:"",k=e.pd_status?`<span class="pd-status muted small">${a(e.pd_status)}</span>`:"",K=e.context?`<p class="pd-context muted small">${a(e.context)}</p>`:"",X=e.pattern_role?`<p class="pd-role muted small"><em>${a(e.pattern_role)}</em></p>`:"",Y=e.url?` <a href="${a(e.url)}" target="_blank" rel="noopener" class="pd-link">\u2197 source</a>`:"",Z=e.quote_ja?`<blockquote class="pd-quote-ja" lang="ja">${a(e.quote_ja)}</blockquote>`:"",ee=e.quote_translation_en?`<p class="pd-quote-en muted small">${a(e.quote_translation_en)}</p>`:"";return`
            <li class="pd-ref pd-ref-${i}">
              <div class="pd-ref-header">
                <strong class="pd-work-title" lang="ja">${p}</strong>${Y}
                ${f?`<span class="pd-author muted small">\u2014 ${f}${$}</span>`:""}
              </div>
              ${k}
              ${Z}
              ${ee}
              ${K}
              ${X}
            </li>`}).join("")}
      </ul>
    </section>
  `:"",Q=o?'<span class="status-badge mastered">\u2605 Mastered</span>':l?'<span class="status-badge weak">Needs practice</span>':"",V=e=>{const i=Array.isArray(s)?s.find(p=>p&&p.id===e):null;return a(i&&i.pattern?i.pattern:e)},J=`
    <article class="pattern-detail">
      ${w}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 ${a(r("grammar_detail.back_to_list"))}</a>
      ${t._alias_of?`<p class="pattern-alias-badge muted small">\u2194 <a href="#/learn/${encodeURIComponent(t._alias_of)}">Also see ${V(t._alias_of)}</a> <span class="muted">(dual-coverage of the same concept; different examples)</span></p>`:""}
      ${t._homonym_of?`<p class="pattern-homonym-badge muted small">\u26A0 <a href="#/learn/${encodeURIComponent(t._homonym_of)}">Same kana, different meaning: ${V(t._homonym_of)}</a></p>`:""}
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${a(t.pattern)}</h2>
          <p class="meaning-en">${a(T(t))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${_?"checked":""}>
          <span>${a(r("grammar_detail.mark_as_known"))}</span>
          ${Q}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} ${a(r("grammar_detail.print_pdf"))}
        </button>
      </div>

      ${de(t)}

      <section>
        <h3 class="section-title">${a(r("grammar_detail.meaning"))}</h3>
        <p>${a(T(t))}</p>
      </section>

      <section>
        <h3 class="section-title">${a(r("grammar_detail.explanation"))}</h3>
        <p>${a(re(t))}</p>
      </section>

      ${(()=>{const e=t.essay;if(!e||typeof e!="object")return"";const i=e.provenance==="needs_native_review",p=(f,$,k)=>!$&&!k?"":$?`<p><strong>${a(f)}:</strong> ${a($)}</p>`:`<p><strong>${a(f)}:</strong> <span class="muted small">${a(k)}</span></p>`;return`
          <section class="pattern-essay">
            <h3 class="section-title">${a(r("grammar_detail.deep_dive"))} ${i?'<span class="essay-stub-badge muted small">stub</span>':""}</h3>
            ${p(r("grammar_detail.deep_dive_at_a_glance"),e.intro)}
            ${p(r("grammar_detail.deep_dive_why"),e.why_it_matters,i?"Pending native author.":"")}
            ${p(r("grammar_detail.deep_dive_pitfalls"),e.common_pitfalls)}
            ${p(r("grammar_detail.deep_dive_contrasts"),e.contrasts)}
            ${p(r("grammar_detail.deep_dive_practice"),e.closing_practice_tip,i?"Pending native author.":"")}
            ${p("Cultural / usage context",e.cultural_context)}
          </section>
        `})()}

      ${(()=>{const e=oe(t);return e?`
          <section class="l1-note">
            <h3 class="section-title">${a(r("grammar_detail.l1_note"))}</h3>
            <p>${a(e)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">${a(r("grammar_detail.examples"))} (${g.length})</h3>
        <ul class="example-list">${j}</ul>
      </section>

      ${y.length?`
        <section>
          <h3 class="section-title">${a(r("grammar_detail.common_mistakes"))}</h3>
          <ul class="mistakes-list">${R}</ul>
        </section>
      `:""}

      ${E.length?`
        <section class="wrong-corrected-pair">
          <h3 class="section-title">${a(r("grammar_detail.wcp_section"))} (${E.length})</h3>
          <ul class="wcp-list">${O}</ul>
        </section>
      `:""}

      ${z}

      ${G}

      ${W}

      ${t.notes?`<section><h3 class="section-title">${a(r("grammar_detail.notes"))}</h3><p>${a(t.notes)}</p></section>`:""}

      ${t.cultural_callout?`
        <!-- IMP-WAVE-P2-12 (UI audit fix, 2026-05-11): usage-culture
             callout \u2014 when/why a learner picks this pattern in real
             Japanese situations (business / classroom / casual / etc.). -->
        <section class="grammar-cultural-callout">
          <h3 class="section-title">Cultural usage note</h3>
          <p>${a(t.cultural_callout.note||"")}</p>
          ${Array.isArray(t.cultural_callout.contexts)&&t.cultural_callout.contexts.length?`
            <p class="muted small">
              Contexts: ${t.cultural_callout.contexts.map(e=>`<span class="cultural-context-chip">${a(e)}</span>`).join(" ")}
            </p>
          `:""}
        </section>
      `:""}

      ${t.authentic_refs?.length?`
        <!-- IMP-WAVE-AUTHENTIC-XLINK (2026-05-11): authentic-content
             cross-link. Real-world cards where this grammar pattern
             appears (signs, menus, transit announcements, etc.). -->
        <section class="grammar-authentic-refs">
          <h3 class="section-title">Seen in the real world</h3>
          <p class="muted small">
            This pattern shows up on these authentic Japanese cards. Click to see real-world usage in context.
          </p>
          <ul class="authentic-ref-list">
            ${t.authentic_refs.map(e=>{const i=e.split(".")[1]||"authentic";return`<li><a href="#/authentic">${a(e)}</a> <span class="muted small">(${a(i)})</span></li>`}).join("")}
          </ul>
        </section>
      `:""}
    </article>
  `;n.innerHTML=J,document.getElementById("mark-known")?.addEventListener("change",e=>{B.setManuallyKnown(t.id,e.target.checked),pe(n,t,s)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{ie as buildOrderedPatternList,pe as renderGrammarPatternDetail,I as renderGrammarTOC};
