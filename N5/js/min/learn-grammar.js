import{renderJa as f}from"./furigana.js";import*as V from"./storage.js";import{esc as a,wireExpandCollapseControls as X}from"./learn.js";import{currentLocale as A,t as o}from"./i18n.js";let b=null,P=null;async function Y(){return b||P||(P=fetch("data/audio_manifest.json").then(n=>n.ok?n.json():null).then(n=>(n&&Array.isArray(n.items)?b=new Set(n.items.map(e=>e.path)):b=new Set,b)).catch(()=>(b=new Set,b)),P)}function Z(n){return b?b.has(n):!1}function ee(n){const e=A();if(e&&e!=="en"){const s=n[`explanation_${e}`];if(typeof s=="string"&&s.trim())return s}return n.explanation_en||""}function te(n){const e=A();if(e&&e!=="en"){const s=n[`meaning_${e}`];if(typeof s=="string"&&s.trim())return s}return n.meaning_en||""}function ae(n){const e=A();if(e&&e!=="en"&&n.l1_notes&&typeof n.l1_notes=="object"){const s=n.l1_notes[e];if(typeof s=="string"&&s.trim())return s}return null}const S=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],T={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function B(n){if(typeof n=="object"&&n&&n.id in T)return T[n.id];const e=typeof n=="string"?n:n?.category||"";for(const[s,p]of S)if(p.includes(e))return s;return"Set Phrases and Discourse"}function ne(n){const e=new Map;for(const[p]of S)e.set(p,[]);for(const p of n){const g=B(p);e.has(g)&&e.get(g).push(p)}const s=[];for(const[,p]of e)p.sort((g,v)=>(g.patternOrder??0)-(v.patternOrder??0)),s.push(...p);return s}let k="";function se(n,e){return e?[n.pattern,n.meaning_en,n.meaning_ja||"",n.notes||"",(n.examples||[]).map(p=>p.ja).join(" ")].join(" ").toLowerCase().includes(e):!0}function I(n,e){const s=new Map;for(const[r]of S)s.set(r,[]);const p=k.trim().toLowerCase(),g=e.patterns.filter(r=>se(r,p));for(const r of g){const i=B(r);s.get(i).push(r)}const v=r=>r.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");let l=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${e.patterns.length} patterns in ${s.size} sections.</p>
  `;for(const[r,i]of s){if(i.length===0)continue;i.sort((c,h)=>(c.patternOrder??0)-(h.patternOrder??0));const u=!!p;l+=`<details class="toc-category" id="cat-${v(r)}"${u?" open":""}>`,l+=`<summary><h3>${a(r)} <span class="cat-count muted small">(${i.length})</span></h3></summary>`,l+='<div class="grammar-grid">';for(const c of i){const h=(()=>{const y=(c.examples||[]).filter(w=>w&&w.ja);return y[0]?y[0].ja:""})(),x=(()=>{const y=A&&A();if(y&&y!=="en"){const w=c[`meaning_${y}`];if(typeof w=="string"&&w.trim())return w}return c.meaning_en||""})();l+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(c.id)}">
          <span class="grammar-pattern" lang="ja">${a(c.pattern)}</span>
          <span class="grammar-card-print-meaning">${a(x)}</span>
          <span class="grammar-card-print-example" lang="ja">${a(h)}</span>
        </a>
      `}l+="</div></details>"}g.length===0?l+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':e.patterns.length===1&&(l+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),l+=`
    <div class="kanji-filters" role="search" aria-label="Filter grammar patterns">
      <input type="search" id="grammar-filter-q" class="kanji-filter-input"
        placeholder="Search pattern, meaning, or example (e.g. \u3066-form / wants to / \u3067\u3059)"
        value="${a(k)}" autocomplete="off"
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
  `,n.innerHTML=l,X(n,"details.toc-category"),n.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const r=Array.from(n.querySelectorAll("details.toc-category")),i=r.map(c=>c.open);r.forEach(c=>{c.open=!0}),document.body.classList.add("is-printing-cheatsheet");const u=()=>{r.forEach((c,h)=>{c.open=i[h]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",u)};window.addEventListener("afterprint",u),window.print()});const _=document.getElementById("grammar-filter-q");if(_){let r=!1;_.addEventListener("compositionstart",()=>{r=!0}),_.addEventListener("compositionend",()=>{r=!1,k=_.value,I(n,e);const i=document.getElementById("grammar-filter-q");if(i){i.focus();const u=i.value;i.setSelectionRange(u.length,u.length)}}),_.addEventListener("input",()=>{if(r)return;k=_.value,I(n,e);const i=document.getElementById("grammar-filter-q");if(i){i.focus();const u=i.value;i.setSelectionRange(u.length,u.length)}})}}const U={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function re(n){return U[n]?U[n]:String(n).replace(/_/g," ").replace(/^./,e=>e.toUpperCase())}function oe(n){const e=n.form_rules?.attaches_to??[],s=n.form_rules?.conjugations??[];if(!e.length&&!s.length)return"";const p=`
    <div class="pattern-usage-header">
      <h3 class="section-title">${a(o("grammar_detail.how_to_use"))}</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,g=e.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${a(n.pattern)}">
      <tbody>
        ${e.map((l,_)=>`
          <tr>
            <td class="pattern-usage-pos">${a(re(l))}</td>
            ${_===0?`<td class="pattern-usage-form" rowspan="${e.length}" lang="ja">${f(n.pattern)}</td>`:""}
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"",v=s.length>=2?`
    <table class="pattern-conjugation-table" aria-label="Conjugation forms">
      <thead>
        <tr><th scope="col">Form</th><th scope="col">Example</th></tr>
      </thead>
      <tbody>
        ${s.map(l=>`
          <tr>
            <td>${a(l.label||l.form)}</td>
            <td lang="ja">${f(l.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${p}${g}${v}</section>`}async function ie(n,e,s){await Y();const p=e.form_rules?.conjugations??[],g=e.examples??[],v=e.common_mistakes??[],l=V.getPatternEntry(e.id),_=!!l?.isManuallyKnown,r=!!l?.isMastered,i=!!l?.isWeak&&!r,u=Array.isArray(s)?ne(s):[],c=u.findIndex(t=>t.id===e.id),h=c>0?u[c-1]:null,x=c>=0&&c<u.length-1?u[c+1]:null,y=h||x?`
    <div class="pattern-nav">
      ${h?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(h.id)}" title="Previous: ${a(h.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${a(h.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${x?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(x.id)}" title="Next: ${a(x.pattern)}"><span class="pattern-nav-name" lang="ja">${a(x.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",w=g.map((t,d)=>{const $=!t.ja||t.ja.includes("(see ")?null:`audio/grammar/${e.id}.${d}.mp3`,j=$&&Z($)?$:null;return`
    <li>
      <span class="form-tag">${a(t.form||"")}</span>
      ${f(t.ja,t.furigana)}
      ${t.translation_en?`<span class="translation">${a(t.translation_en)}</span>`:""}
      ${j?`<audio class="example-audio" controls preload="none" src="${a(j)}"></audio>`:""}
    </li>
  `}).join(""),M=v.map(t=>{if(t.kind==="register_variant"){const d=t.label_a?`<span class="variant-label">${a(t.label_a)}</span>`:"",m=t.label_b?`<span class="variant-label">${a(t.label_b)}</span>`:"";return`
        <li class="variant-pair">
          <div class="variant-row">${d}<span class="variant-form">${f(t.wrong)}</span></div>
          <div class="variant-row">${m}<span class="variant-form">${f(t.right)}</span></div>
          <span class="why">${a(t.why)}</span>
        </li>
      `}return`
      <li>
        <div><span class="wrong">${f(t.wrong)}</span></div>
        <div><span class="right">${f(t.right)}</span></div>
        <span class="why">${a(t.why)}</span>
      </li>
    `}).join(""),E=Array.isArray(e.wrong_corrected_pair)?e.wrong_corrected_pair:[],R=t=>{if(!t)return"";const d=`grammar_detail.cat_${t}`,m=o(d)!==d?o(d):t;return`<span class="error-category-badge cat-${a(t)}">${a(m)}</span>`},q=o("grammar_detail.wcp_wrong"),D=o("grammar_detail.wcp_correct"),F=E.map(t=>`
    <li>
      <div class="wcp-header">${R(t.error_category)}</div>
      <div class="wcp-row wcp-row-wrong">
        <span class="wcp-mark" aria-hidden="true">\u2717</span>
        <span class="wcp-label">${a(q)}</span>
        <span class="wrong">${f(t.wrong)}</span>
      </div>
      <div class="wcp-row wcp-row-correct">
        <span class="wcp-mark" aria-hidden="true">\u2713</span>
        <span class="wcp-label">${a(D)}</span>
        <span class="right">${f(t.correct)}</span>
      </div>
      <span class="why">${a(t.why)}</span>
    </li>
  `).join(""),N=e.politeness_ladder&&typeof e.politeness_ladder=="object"?e.politeness_ladder:null,H=N?`
    <section class="politeness-ladder">
      <h3 class="section-title">${a(o("grammar_detail.ladder_section"))}</h3>
      <table class="ladder-table">
        <tbody>
          ${["casual","polite","humble","respectful"].map(t=>{const d=N[t];if(!d)return"";const m=o(`grammar_detail.ladder_${t}`);return`
              <tr class="ladder-row ladder-${t}">
                <th scope="row">${a(m)}</th>
                <td lang="ja">${f(d)}</td>
              </tr>
            `}).join("")}
        </tbody>
      </table>
    </section>
  `:"",O="",L=Array.isArray(e.public_domain_refs)?e.public_domain_refs:[],z=L.length?`
    <section class="pd-refs">
      <h3 class="section-title">Public-domain references</h3>
      <ul class="pd-refs-list">
        ${L.map(t=>{const d=a(t.source_type||"?"),m=a(t.work_title||""),$=a(t.author||""),j=t.author_death_year?` (died ${t.author_death_year})`:"",C=t.pd_status?`<span class="pd-status muted small">${a(t.pd_status)}</span>`:"",Q=t.context?`<p class="pd-context muted small">${a(t.context)}</p>`:"",K=t.pattern_role?`<p class="pd-role muted small"><em>${a(t.pattern_role)}</em></p>`:"",J=t.url?` <a href="${a(t.url)}" target="_blank" rel="noopener" class="pd-link">\u2197 source</a>`:"";return`
            <li class="pd-ref pd-ref-${d}">
              <div class="pd-ref-header">
                <strong class="pd-work-title" lang="ja">${m}</strong>${J}
                ${$?`<span class="pd-author muted small">\u2014 ${$}${j}</span>`:""}
              </div>
              ${C}
              ${Q}
              ${K}
            </li>`}).join("")}
      </ul>
    </section>
  `:"",G=r?'<span class="status-badge mastered">\u2605 Mastered</span>':i?'<span class="status-badge weak">Needs practice</span>':"",W=`
    <article class="pattern-detail">
      ${y}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 ${a(o("grammar_detail.back_to_list"))}</a>
      ${e._alias_of?`<p class="pattern-alias-badge muted small">\u2194 <a href="#/learn/${encodeURIComponent(e._alias_of)}">Also see ${a(e._alias_of)}</a> <span class="muted">(dual-coverage of the same concept; different examples)</span></p>`:""}
      ${e._homonym_of?`<p class="pattern-homonym-badge muted small">\u26A0 <a href="#/learn/${encodeURIComponent(e._homonym_of)}">Same kana, different meaning: ${a(e._homonym_of)}</a></p>`:""}
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${a(e.pattern)}</h2>
          <p class="meaning-en">${a(te(e))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${_?"checked":""}>
          <span>${a(o("grammar_detail.mark_as_known"))}</span>
          ${G}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} ${a(o("grammar_detail.print_pdf"))}
        </button>
      </div>

      ${oe(e)}

      <section>
        <h3 class="section-title">${a(o("grammar_detail.explanation"))}</h3>
        <p>${a(ee(e))}</p>
      </section>

      ${(()=>{const t=e.essay;if(!t||typeof t!="object")return"";const d=t.provenance==="needs_native_review",m=($,j,C)=>!j&&!C?"":j?`<p><strong>${a($)}:</strong> ${a(j)}</p>`:`<p><strong>${a($)}:</strong> <span class="muted small">${a(C)}</span></p>`;return`
          <section class="pattern-essay">
            <h3 class="section-title">${a(o("grammar_detail.deep_dive"))} ${d?'<span class="essay-stub-badge muted small">stub</span>':""}</h3>
            ${m(o("grammar_detail.deep_dive_at_a_glance"),t.intro)}
            ${m(o("grammar_detail.deep_dive_why"),t.why_it_matters,d?"Pending native author.":"")}
            ${m(o("grammar_detail.deep_dive_pitfalls"),t.common_pitfalls)}
            ${m(o("grammar_detail.deep_dive_contrasts"),t.contrasts)}
            ${m(o("grammar_detail.deep_dive_practice"),t.closing_practice_tip,d?"Pending native author.":"")}
            ${m("Cultural / usage context",t.cultural_context)}
          </section>
        `})()}

      ${(()=>{const t=ae(e);return t?`
          <section class="l1-note">
            <h3 class="section-title">${a(o("grammar_detail.l1_note"))}</h3>
            <p>${a(t)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">${a(o("grammar_detail.examples"))} (${g.length})</h3>
        <ul class="example-list">${w}</ul>
      </section>

      ${v.length?`
        <section>
          <h3 class="section-title">${a(o("grammar_detail.common_mistakes"))}</h3>
          <ul class="mistakes-list">${M}</ul>
        </section>
      `:""}

      ${E.length?`
        <section class="wrong-corrected-pair">
          <h3 class="section-title">${a(o("grammar_detail.wcp_section"))} (${E.length})</h3>
          <ul class="wcp-list">${F}</ul>
        </section>
      `:""}

      ${H}

      ${O}

      ${z}

      <section>
        <h3 class="section-title">\u610F\u5473\uFF08\u3084\u3055\u3057\u3044 \u306B\u307B\u3093\u3054\uFF09</h3>
        <p>${f(e.meaning_ja)}</p>
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
              Contexts: ${e.cultural_callout.contexts.map(t=>`<span class="cultural-context-chip">${a(t)}</span>`).join(" ")}
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
            ${e.authentic_refs.map(t=>{const d=t.split(".")[1]||"authentic";return`<li><a href="#/authentic">${a(t)}</a> <span class="muted small">(${a(d)})</span></li>`}).join("")}
          </ul>
        </section>
      `:""}
    </article>
  `;n.innerHTML=W,document.getElementById("mark-known")?.addEventListener("change",t=>{V.setManuallyKnown(e.id,t.target.checked),ie(n,e,s)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{ne as buildOrderedPatternList,ie as renderGrammarPatternDetail,I as renderGrammarTOC};
