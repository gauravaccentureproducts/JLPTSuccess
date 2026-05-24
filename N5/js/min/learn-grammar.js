import{renderJa as _}from"./furigana.js";import*as V from"./storage.js";import{esc as a,wireExpandCollapseControls as Z}from"./learn.js";import{currentLocale as A,t as o}from"./i18n.js";import{assetUrl as ee}from"./router.js";let v=null,C=null;async function te(){return v||C||(C=fetch("data/audio_manifest.json").then(n=>n.ok?n.json():null).then(n=>(n&&Array.isArray(n.items)?v=new Set(n.items.map(t=>t.path)):v=new Set,v)).catch(()=>(v=new Set,v)),C)}function ae(n){return v?v.has(n):!1}function ne(n){const t=A();if(t&&t!=="en"){const s=n[`explanation_${t}`];if(typeof s=="string"&&s.trim())return s}return n.explanation_en||""}function se(n){const t=A();if(t&&t!=="en"){const s=n[`meaning_${t}`];if(typeof s=="string"&&s.trim())return s}return n.meaning_en||""}function re(n){const t=A();if(t&&t!=="en"&&n.l1_notes&&typeof n.l1_notes=="object"){const s=n.l1_notes[t];if(typeof s=="string"&&s.trim())return s}return null}const S=[["Sentence Basics",["Copula and Basic Sentence Structure","Particles","Demonstratives","Question Words"]],["Verbs",["Verbs - Tense and Politeness (\u307E\u3059-form)","Verbs - Plain (Dictionary) Form and Negation","Te-form and Related Patterns","Existence and Possession","Desiderative and Volitional","Giving and Receiving (basic)","Additional Upper N5 / Borderline Patterns - Permission and Obligation","Additional Upper N5 / Borderline Patterns - Experience and Advice","Additional Upper N5 / Borderline Patterns - Compound and Listed Actions","Additional Upper N5 / Borderline Patterns - Excess","Additional Upper N5 / Borderline Patterns - Intention","Additional Upper N5 / Borderline Patterns - Way of Doing","Additional Upper N5 / Borderline Patterns - Prohibitive (Casual)"]],["Adjectives and Comparison",["Adjectives","Comparison and Preference"]],["Time, Counters, Connectives",["Counters and Quantity","Time Expressions","Conjunctions and Connectives","Asking and Stating with \u304B\u3089 / \u306E\u3067 (basic causation)","Existence-of-Plans and Frequency"]],["Set Phrases and Discourse",["Nominalization and Modification","Common Set Patterns","Functional Expressions (Non-Grammar, Common Usage)","Other Core Patterns","Honorific / Polite Vocabulary at N5 (functional)","Additional Upper N5 / Borderline Patterns - Explanation and Emphasis","Additional Upper N5 / Borderline Patterns - Quotation (Casual)","Additional Upper N5 / Borderline Patterns - Sentence-Final Exclamation"]]],B={"n5-135":"Verbs","n5-144":"Verbs","n5-153":"Verbs","n5-154":"Verbs","n5-162":"Verbs","n5-163":"Verbs"};function T(n){if(typeof n=="object"&&n&&n.id in B)return B[n.id];const t=typeof n=="string"?n:n?.category||"";for(const[s,p]of S)if(p.includes(t))return s;return"Set Phrases and Discourse"}function oe(n){const t=new Map;for(const[p]of S)t.set(p,[]);for(const p of n){const g=T(p);t.has(g)&&t.get(g).push(p)}const s=[];for(const[,p]of t)p.sort((g,y)=>(g.patternOrder??0)-(y.patternOrder??0)),s.push(...p);return s}let P="";function ie(n,t){return t?[n.pattern,n.meaning_en,n.meaning_ja||"",n.notes||"",(n.examples||[]).map(p=>p.ja).join(" ")].join(" ").toLowerCase().includes(t):!0}function U(n,t){const s=new Map;for(const[r]of S)s.set(r,[]);const p=P.trim().toLowerCase(),g=t.patterns.filter(r=>ie(r,p));for(const r of g){const i=T(r);s.get(i).push(r)}const y=r=>r.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");let l=`
    <a class="back-link" href="#/learn">\u2190 Back to Learn</a>
    <h2>Grammar</h2>
    <p class="page-lede">${t.patterns.length} patterns in ${s.size} sections.</p>
  `;for(const[r,i]of s){if(i.length===0)continue;i.sort((c,h)=>(c.patternOrder??0)-(h.patternOrder??0));const u=!!p;l+=`<details class="toc-category" id="cat-${y(r)}"${u?" open":""}>`,l+=`<summary><h3>${a(r)} <span class="cat-count muted small">(${i.length})</span></h3></summary>`,l+='<div class="grammar-grid">';for(const c of i){const h=(()=>{const w=(c.examples||[]).filter(j=>j&&j.ja);return w[0]?w[0].ja:""})(),x=(()=>{const w=A&&A();if(w&&w!=="en"){const j=c[`meaning_${w}`];if(typeof j=="string"&&j.trim())return j}return c.meaning_en||""})();l+=`
        <a class="grammar-card" href="#/learn/${encodeURIComponent(c.id)}">
          <span class="grammar-pattern" lang="ja">${a(c.pattern)}</span>
          <span class="grammar-card-print-meaning">${a(x)}</span>
          <span class="grammar-card-print-example" lang="ja">${a(h)}</span>
        </a>
      `}l+="</div></details>"}g.length===0?l+='<div class="placeholder"><p>No patterns match the current filter.</p></div>':t.patterns.length===1&&(l+='<div class="placeholder" style="margin-top:24px"><p>Scaffold currently has 1 example pattern. Add more to <code>data/grammar.json</code> as you author content.</p></div>'),l+=`
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
  `,n.innerHTML=l,Z(n,"details.toc-category"),n.querySelector(".toc-print-cheatsheet")?.addEventListener("click",()=>{const r=Array.from(n.querySelectorAll("details.toc-category")),i=r.map(c=>c.open);r.forEach(c=>{c.open=!0}),document.body.classList.add("is-printing-cheatsheet");const u=()=>{r.forEach((c,h)=>{c.open=i[h]}),document.body.classList.remove("is-printing-cheatsheet"),window.removeEventListener("afterprint",u)};window.addEventListener("afterprint",u),window.print()});const $=document.getElementById("grammar-filter-q");if($){let r=!1;$.addEventListener("compositionstart",()=>{r=!0}),$.addEventListener("compositionend",()=>{r=!1,P=$.value,U(n,t);const i=document.getElementById("grammar-filter-q");if(i){i.focus();const u=i.value;i.setSelectionRange(u.length,u.length)}}),$.addEventListener("input",()=>{if(r)return;P=$.value,U(n,t);const i=document.getElementById("grammar-filter-q");if(i){i.focus();const u=i.value;i.setSelectionRange(u.length,u.length)}})}}const q={noun:"Noun",noun_subject:"Noun (subject)",noun_location:"Noun (location)",noun_time:"Noun (time)",noun_quantity:"Noun (quantity)",noun_or_adj:"Noun or adjective",na_adjective:"\u306A-adjective",i_adjective:"\u3044-adjective",verb:"Verb",verb_stem:"Verb stem (\u307E\u3059-base)",verb_stem_i:"Verb i-stem",verb_root:"Verb root",verb_dictionary:"Verb (dictionary form)",verb_plain:"Verb (plain form)",verb_te:"Verb (\u3066-form)",verb_ta:"Verb (\u305F-form)",verb_nai:"Verb (\u306A\u3044-form)",verb_mashita:"Verb (\u307E\u3057\u305F form)",verb_te_imasu_neg:"Verb (\u3066-\u3044\u307E\u305B\u3093)",verb_or_adj_stem:"Verb or adjective stem",pronoun:"Pronoun",question_word:"Question word",before_noun:"Before a noun",adverbial:"Adverbial position",sentence_end:"Sentence end",sentence_pattern:"Full sentence",clause:"Clause",clause_start:"Clause-initial",clause_end:"Clause-final",plain_clause:"Plain-form clause",plain_or_polite_clause:"Plain or polite clause",quoted_clause:"Quoted clause",quantity:"Quantity expression",number:"Number",set_phrase:"Set phrase",standalone:"Standalone",dialogue:"Dialogue line",after_name:"After a name"};function le(n){return q[n]?q[n]:String(n).replace(/_/g," ").replace(/^./,t=>t.toUpperCase())}function ce(n){const t=n.form_rules?.attaches_to??[],s=n.form_rules?.conjugations??[];if(!t.length&&!s.length)return"";const p=`
    <div class="pattern-usage-header">
      <h3 class="section-title">${a(o("grammar_detail.how_to_use"))}</h3>
      <span class="pattern-usage-chip" lang="ja">\u4F7F\u3044\u65B9</span>
    </div>
  `,g=t.length?`
    <table class="pattern-usage-table" aria-label="Attach points for ${a(n.pattern)}">
      <tbody>
        ${t.map((l,$)=>`
          <tr>
            <td class="pattern-usage-pos">${a(le(l))}</td>
            ${$===0?`<td class="pattern-usage-form" rowspan="${t.length}" lang="ja">${_(n.pattern)}</td>`:""}
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
        ${s.map(l=>`
          <tr>
            <td>${a(l.label||l.form)}</td>
            <td lang="ja">${_(l.example)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `:"";return`<section class="pattern-usage">${p}${g}${y}</section>`}async function de(n,t,s){await te();const p=t.form_rules?.conjugations??[],g=t.examples??[],y=t.common_mistakes??[],l=V.getPatternEntry(t.id),$=!!l?.isManuallyKnown,r=!!l?.isMastered,i=!!l?.isWeak&&!r,u=Array.isArray(s)?oe(s):[],c=u.findIndex(e=>e.id===t.id),h=c>0?u[c-1]:null,x=c>=0&&c<u.length-1?u[c+1]:null,w=h||x?`
    <div class="pattern-nav">
      ${h?`<a class="pattern-nav-prev" href="#/learn/${encodeURIComponent(h.id)}" title="Previous: ${a(h.pattern)}">&larr; <span class="pattern-nav-name" lang="ja">${a(h.pattern)}</span></a>`:'<span class="pattern-nav-prev pattern-nav-empty" aria-hidden="true"></span>'}
      ${x?`<a class="pattern-nav-next" href="#/learn/${encodeURIComponent(x.id)}" title="Next: ${a(x.pattern)}"><span class="pattern-nav-name" lang="ja">${a(x.pattern)}</span> &rarr;</a>`:'<span class="pattern-nav-next pattern-nav-empty" aria-hidden="true"></span>'}
    </div>
  `:"",j=g.map((e,d)=>{const f=!e.ja||e.ja.includes("(see ")?null:`audio/grammar/${t.id}.${d}.mp3`,b=f&&ae(f)?f:null;return`
    <li>
      <span class="form-tag">${a(e.form||"")}</span>
      ${_(e.ja,e.furigana)}
      ${e.translation_en?`<span class="translation">${a(e.translation_en)}</span>`:""}
      ${b?`<audio class="example-audio" controls preload="none" src="${a(ee(b))}"></audio>`:""}
    </li>
  `}).join(""),I=y.map(e=>{if(e.kind==="register_variant"){const d=e.label_a?`<span class="variant-label">${a(e.label_a)}</span>`:"",m=e.label_b?`<span class="variant-label">${a(e.label_b)}</span>`:"",f=e.form_a??e.wrong??"",b=e.form_b??e.right??"";return`
        <li class="variant-pair">
          <div class="variant-row">${d}<span class="variant-form">${_(f)}</span></div>
          <div class="variant-row">${m}<span class="variant-form">${_(b)}</span></div>
          <span class="why">${a(e.why)}</span>
        </li>
      `}return`
      <li>
        <div><span class="wrong">${_(e.wrong)}</span></div>
        <div><span class="right">${_(e.right)}</span></div>
        <span class="why">${a(e.why)}</span>
      </li>
    `}).join(""),E=Array.isArray(t.wrong_corrected_pair)?t.wrong_corrected_pair:[],M=e=>{if(!e)return"";const d=`grammar_detail.cat_${e}`,m=o(d)!==d?o(d):e;return`<span class="error-category-badge cat-${a(e)}">${a(m)}</span>`},R=o("grammar_detail.wcp_wrong"),D=o("grammar_detail.wcp_correct"),F=E.map(e=>`
    <li>
      <div class="wcp-header">${M(e.error_category)}</div>
      <div class="wcp-row wcp-row-wrong">
        <span class="wcp-mark" aria-hidden="true">\u2717</span>
        <span class="wcp-label">${a(R)}</span>
        <span class="wrong">${_(e.wrong)}</span>
      </div>
      <div class="wcp-row wcp-row-correct">
        <span class="wcp-mark" aria-hidden="true">\u2713</span>
        <span class="wcp-label">${a(D)}</span>
        <span class="right">${_(e.correct)}</span>
      </div>
      <span class="why">${a(e.why)}</span>
    </li>
  `).join(""),N=t.politeness_ladder&&typeof t.politeness_ladder=="object"?t.politeness_ladder:null,H=N?`
    <section class="politeness-ladder">
      <h3 class="section-title">${a(o("grammar_detail.ladder_section"))}</h3>
      <table class="ladder-table">
        <tbody>
          ${["casual","polite","humble","respectful"].map(e=>{const d=N[e];if(!d)return"";const m=o(`grammar_detail.ladder_${e}`);return`
              <tr class="ladder-row ladder-${e}">
                <th scope="row">${a(m)}</th>
                <td lang="ja">${_(d)}</td>
              </tr>
            `}).join("")}
        </tbody>
      </table>
    </section>
  `:"",O="",L=Array.isArray(t.public_domain_refs)?t.public_domain_refs:[],z=L.length?`
    <section class="pd-refs">
      <h3 class="section-title">Public-domain references</h3>
      <ul class="pd-refs-list">
        ${L.map(e=>{const d=a(e.source_type||"?"),m=a(e.work_title||""),f=a(e.author||""),b=e.author_death_year?` (died ${e.author_death_year})`:"",k=e.pd_status?`<span class="pd-status muted small">${a(e.pd_status)}</span>`:"",Q=e.context?`<p class="pd-context muted small">${a(e.context)}</p>`:"",J=e.pattern_role?`<p class="pd-role muted small"><em>${a(e.pattern_role)}</em></p>`:"",K=e.url?` <a href="${a(e.url)}" target="_blank" rel="noopener" class="pd-link">\u2197 source</a>`:"",X=e.quote_ja?`<blockquote class="pd-quote-ja" lang="ja">${a(e.quote_ja)}</blockquote>`:"",Y=e.quote_translation_en?`<p class="pd-quote-en muted small">${a(e.quote_translation_en)}</p>`:"";return`
            <li class="pd-ref pd-ref-${d}">
              <div class="pd-ref-header">
                <strong class="pd-work-title" lang="ja">${m}</strong>${K}
                ${f?`<span class="pd-author muted small">\u2014 ${f}${b}</span>`:""}
              </div>
              ${k}
              ${X}
              ${Y}
              ${Q}
              ${J}
            </li>`}).join("")}
      </ul>
    </section>
  `:"",G=r?'<span class="status-badge mastered">\u2605 Mastered</span>':i?'<span class="status-badge weak">Needs practice</span>':"",W=`
    <article class="pattern-detail">
      ${w}
      <a class="back-link no-print" href="#/learn/grammar">\u2190 ${a(o("grammar_detail.back_to_list"))}</a>
      ${t._alias_of?`<p class="pattern-alias-badge muted small">\u2194 <a href="#/learn/${encodeURIComponent(t._alias_of)}">Also see ${a(t._alias_of)}</a> <span class="muted">(dual-coverage of the same concept; different examples)</span></p>`:""}
      ${t._homonym_of?`<p class="pattern-homonym-badge muted small">\u26A0 <a href="#/learn/${encodeURIComponent(t._homonym_of)}">Same kana, different meaning: ${a(t._homonym_of)}</a></p>`:""}
      <div class="pattern-header">
        <div>
          <h2 class="pattern-name">${a(t.pattern)}</h2>
          <p class="meaning-en">${a(se(t))}</p>
        </div>
        <label class="known-toggle no-print" title="Manually mark as known. Cleared on the next miss in Test or Drill.">
          <input type="checkbox" id="mark-known" ${$?"checked":""}>
          <span>${a(o("grammar_detail.mark_as_known"))}</span>
          ${G}
        </label>
        <button type="button" id="pattern-print-btn" class="btn-secondary no-print pattern-print-btn"
                title="Print this lesson note (use 'Save as PDF' in your browser's print dialog).">
          \u{1F5A8} ${a(o("grammar_detail.print_pdf"))}
        </button>
      </div>

      ${ce(t)}

      <section>
        <h3 class="section-title">${a(o("grammar_detail.explanation"))}</h3>
        <p>${a(ne(t))}</p>
      </section>

      ${(()=>{const e=t.essay;if(!e||typeof e!="object")return"";const d=e.provenance==="needs_native_review",m=(f,b,k)=>!b&&!k?"":b?`<p><strong>${a(f)}:</strong> ${a(b)}</p>`:`<p><strong>${a(f)}:</strong> <span class="muted small">${a(k)}</span></p>`;return`
          <section class="pattern-essay">
            <h3 class="section-title">${a(o("grammar_detail.deep_dive"))} ${d?'<span class="essay-stub-badge muted small">stub</span>':""}</h3>
            ${m(o("grammar_detail.deep_dive_at_a_glance"),e.intro)}
            ${m(o("grammar_detail.deep_dive_why"),e.why_it_matters,d?"Pending native author.":"")}
            ${m(o("grammar_detail.deep_dive_pitfalls"),e.common_pitfalls)}
            ${m(o("grammar_detail.deep_dive_contrasts"),e.contrasts)}
            ${m(o("grammar_detail.deep_dive_practice"),e.closing_practice_tip,d?"Pending native author.":"")}
            ${m("Cultural / usage context",e.cultural_context)}
          </section>
        `})()}

      ${(()=>{const e=re(t);return e?`
          <section class="l1-note">
            <h3 class="section-title">${a(o("grammar_detail.l1_note"))}</h3>
            <p>${a(e)}</p>
          </section>
        `:""})()}

      <section>
        <h3 class="section-title">${a(o("grammar_detail.examples"))} (${g.length})</h3>
        <ul class="example-list">${j}</ul>
      </section>

      ${y.length?`
        <section>
          <h3 class="section-title">${a(o("grammar_detail.common_mistakes"))}</h3>
          <ul class="mistakes-list">${I}</ul>
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
        <p>${_(t.meaning_ja)}</p>
      </section>

      ${t.notes?`<section><h3 class="section-title">${a(o("grammar_detail.notes"))}</h3><p>${a(t.notes)}</p></section>`:""}

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
            ${t.authentic_refs.map(e=>{const d=e.split(".")[1]||"authentic";return`<li><a href="#/authentic">${a(e)}</a> <span class="muted small">(${a(d)})</span></li>`}).join("")}
          </ul>
        </section>
      `:""}
    </article>
  `;n.innerHTML=W,document.getElementById("mark-known")?.addEventListener("change",e=>{V.setManuallyKnown(t.id,e.target.checked),de(n,t,s)}),document.getElementById("pattern-print-btn")?.addEventListener("click",()=>{window.print()})}export{oe as buildOrderedPatternList,de as renderGrammarPatternDetail,U as renderGrammarTOC};
