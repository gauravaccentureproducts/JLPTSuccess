import{renderJa as v}from"./furigana.js";let f=null;const y=new Map;async function P(){if(f)return f;const n=await fetch("data/papers/manifest.json");if(!n.ok)throw new Error(`Failed to load papers manifest: ${n.status}`);return f=await n.json(),f}async function w(n,t){const a=`${n}-${t}`;if(y.has(a))return y.get(a);const i=await fetch(`data/papers/${n}/paper-${t}.json`);if(!i.ok)throw new Error(`Failed to load paper ${a}: ${i.status}`);const e=await i.json();return y.set(a,e),e}function j(n){const t=String(n).match(/^([a-z]+)-(\d+)$/);return t?{category:t[1],number:parseInt(t[2],10)}:null}function C(n,t){return(n.combined_sections||[]).find(a=>a.id===t)}function T(n,t){return(n.full_mock_papers||[]).find(a=>a.id===t)}function S(n,t){return(n.virtual_papers||[]).find(a=>a.id===t)}async function z(n,t){const a=(t||"").trim();if(!a)return h(n);const[i,e]=a.split("?"),r=decodeURIComponent(i),l=e&&/(?:^|&)key=1\b/.test(e)||!1;let o;try{o=await P()}catch(c){n.innerHTML=`<article class="print-paper-error"><p>Could not load papers manifest: ${s(String(c))}</p></article>`;return}if(/^full-mock-\d+$/.test(r))return I(n,o,r,l);if(/^genngo-chishiki-(moji-goi|bunpou-dokkai)-\d+$/.test(r))return E(n,o,r,l);if(/^chokai-\d+(?:-virtual)?$/.test(r))return H(n,o,r,l);const p=j(r);return p&&["moji","goi","bunpou","dokkai"].includes(p.category)?D(n,o,p,l):h(n,r)}async function h(n,t){const a=await P(),i=[];(a.categories||[]).forEach(e=>{e.papers.forEach(r=>{i.push(g(r.id,r.name,`${r.questionCount} Q \xB7 ${e.label_ja}`))})}),(a.combined_sections||[]).forEach(e=>{i.push(g(e.id,e.name_en,`${e.questionCount} Q \xB7 ${s(e.sectionLabel)}`))}),(a.full_mock_papers||[]).forEach(e=>{i.push(g(e.id,e.name_en,`${e.totalQuestions} Q \xB7 ${e.totalDurationMin} min \xB7 full mock`))}),(a.virtual_papers||[]).forEach(e=>{i.push(g(e.id,e.name,`${e.questionCount} Q \xB7 ${e.expectedDurationMin} min \xB7 listening`))}),n.innerHTML=`
    <article class="print-paper-index">
      <a class="back-link" href="#/papers">\u2190 Mock-test papers</a>
      <h2>Print a paper</h2>
      <p class="page-lede">Pick a paper to render in print-ready layout. Use your browser's <strong>Print \u2192 Save as PDF</strong> to keep an offline copy, or print to paper for a real-pencil mock-test ritual. The on-screen layout includes a cover page, mondai-grouped questions, and an optional answer-key page.</p>
      ${t?`<p class="print-paper-bad-id">Unknown paper id: <code>${s(t)}</code>. Pick from the list below.</p>`:""}
      <ul class="print-paper-list">${i.join("")}</ul>
      <p class="print-paper-foot muted small">For the on-screen mock-test flow with auto-grading, use <a href="#/papers">Mock-test papers</a> or <a href="#/test">Test</a>.</p>
    </article>
  `}function g(n,t,a){return`
    <li class="print-paper-card">
      <a class="print-paper-link" href="#/print/${s(n)}">
        <strong>${s(t)}</strong>
        <span class="muted small">${s(a)}</span>
      </a>
      <span class="print-paper-actions">
        <a href="#/print/${s(n)}" title="Open print view">View</a>
        <span aria-hidden="true">\xB7</span>
        <a href="#/print/${s(n)}?key=1" title="Open with answer key">+ Key</a>
      </span>
    </li>
  `}async function D(n,t,a,i){const{category:e,number:r}=a;let l;try{l=await w(e,r)}catch(u){n.innerHTML=`<article class="print-paper-error"><p>Could not load <code>${s(e)}-${r}</code>: ${s(String(u))}</p><p><a href="#/print">Back to print index.</a></p></article>`;return}const o=(t.categories||[]).find(u=>u.id===e)||{label:e,label_ja:""},p=(o.papers||[]).find(u=>u.id===l.id)||{},c=[{label_ja:o.label_ja||o.label||e,label_en:o.label||e,questions:l.questions,duration_min:p.expectedDurationMin||null}],_={name_en:l.name||`${o.label} Paper ${r}`,name_ja:`${o.label_ja||""} Paper ${r}`,total_q:l.questions.length,duration_min:p.expectedDurationMin||null,instructions:k(e)};return $(n,l.id,_,c,i)}async function E(n,t,a,i){const e=C(t,a);if(!e)return h(n,a);const l=(await Promise.all(e.componentPapers.map(async p=>{const c=j(p);if(!c)return null;const _=await w(c.category,c.number),u=(t.categories||[]).find(d=>d.id===c.category)||{label:c.category,label_ja:""},m=(u.papers||[]).find(d=>d.id===p)||{};return{label_ja:u.label_ja,label_en:u.label,questions:_.questions,duration_min:m.expectedDurationMin||null}}))).filter(Boolean),o={name_en:e.name_en,name_ja:e.name_ja,total_q:e.questionCount,duration_min:e.expectedDurationMin,instructions:k("combined")};return $(n,e.id,o,l,i)}async function I(n,t,a,i){const e=T(t,a);if(!e)return h(n,a);const r=[];for(const o of e.sections)if(/^genngo-chishiki/.test(o)){const p=C(t,o);if(!p)continue;for(const c of p.componentPapers){const _=j(c);if(!_)continue;const u=await w(_.category,_.number),m=(t.categories||[]).find(d=>d.id===_.category)||{label:_.category,label_ja:""};r.push({label_ja:m.label_ja,label_en:m.label,questions:u.questions,duration_min:null})}}else if(/^chokai-\d+/.test(o)){const p=S(t,o.replace(/-virtual$/,""));p&&r.push({label_ja:"\u8074\u89E3",label_en:"Listening",questions:q(p),duration_min:p.expectedDurationMin||null,is_chokai:!0,source_listening_ids:p.source_listening_ids||[]})}const l={name_en:e.name_en,name_ja:e.name_ja,total_q:e.totalQuestions,duration_min:e.totalDurationMin,instructions:k("full-mock")};return $(n,e.id,l,r,i)}async function H(n,t,a,i){const e=a.replace(/-virtual$/,""),r=S(t,e);if(!r)return h(n,a);const l={name_en:`${r.name} (script)`,name_ja:r.label_ja,total_q:r.questionCount,duration_min:r.expectedDurationMin||null,instructions:k("chokai")},o=[{label_ja:"\u8074\u89E3",label_en:"Listening",questions:q(r),duration_min:r.expectedDurationMin||null,is_chokai:!0,source_listening_ids:r.source_listening_ids||[]}];return $(n,r.id,l,o,i)}let b=null;async function J(){if(b)return b;const n=await fetch("data/listening.json");return b=n.ok?await n.json():{items:[]},b}function q(n){return n.source_listening_ids.map((t,a)=>({_chokai_listen_id:t,id:`${n.id}-${a+1}`,mondai:null,type:"mcq",stem_html:"",choices:[],correctIndex:0,rationale:""}))}async function $(n,t,a,i,e){if(i.some(c=>c.is_chokai)){const c=await J(),_=new Map((c.items||[]).map(u=>[u.id,u]));i.forEach(u=>{u.is_chokai&&(u.questions=u.questions.map(m=>{const d=_.get(m._chokai_listen_id);if(!d)return{...m,stem_html:"(listening item not found: "+s(m._chokai_listen_id)+")"};const x=(d.choices||[]).findIndex(L=>L===d.correctAnswer);return{...m,mondai:d.mondai||null,stem_html:O(d),choices:d.choices||[],correctIndex:x>=0?x:0,rationale:d.explanation_ja||d.explanation_en||""}}))})}const l=i.map(c=>{const u=U(c.questions).map(m=>`
      <section class="print-mondai">
        <header class="print-mondai-header">
          <h3>${A(c,m.mondai)}</h3>
          ${B(c,m.mondai)}
        </header>
        <ol class="print-q-list">
          ${m.questions.map(d=>N(d,c.is_chokai)).join("")}
        </ol>
      </section>
    `).join("");return`
      <section class="print-section">
        <header class="print-section-header">
          <h2 lang="ja">${s(c.label_ja||"")}</h2>
          <p class="print-section-meta">${s(c.label_en||"")}${c.duration_min?` \xB7 ${c.duration_min} min`:""} \xB7 ${c.questions.length} questions</p>
        </header>
        ${u}
      </section>
    `}).join(""),o=e?R(i):"";n.innerHTML=`
    <article class="print-paper-screen">
      <header class="print-paper-toolbar">
        <a class="back-link" href="#/print">\u2190 Print index</a>
        <span class="print-paper-toolbar-actions">
          <a class="btn-secondary" href="#/print/${s(t)}${e?"":"?key=1"}">${e?"Hide answer key":"+ Answer key"}</a>
          <button class="btn-primary" id="print-paper-now-btn" type="button">Print / Save PDF</button>
        </span>
      </header>

      <article class="print-paper-root" lang="ja">
        ${Q()}
        ${F(a)}
        ${l}
        ${o}
        <footer class="print-paper-footer">
          <p class="print-paper-source">${s(a.name_en)} \xB7 JLPTSuccess \xB7 gauravaccentureproducts.github.io/JLPTSuccess</p>
        </footer>
      </article>

      <p class="muted small print-paper-hint">Tip: Browser <strong>Print</strong> dialog has a "Save as PDF" destination. Use that to keep an offline copy without using paper. Each printed page carries a faint <strong>JLPTSUCCESS.COM</strong> watermark \u2014 readability of the questions is unaffected; the watermark deters resale of printed copies.</p>
    </article>
  `;try{typeof v=="function"&&v(n)}catch{}const p=n.querySelector("#print-paper-now-btn");p&&p.addEventListener("click",()=>window.print())}function Q(){return`
    <div class="print-paper-watermark" aria-hidden="true">
      <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
        <defs>
          <pattern id="jlpts-watermark" x="0" y="0" width="280" height="160" patternUnits="userSpaceOnUse">
            <text x="140" y="86"
                  font-family="Helvetica, Arial, sans-serif"
                  font-size="16"
                  font-weight="700"
                  fill="#000"
                  fill-opacity="0.06"
                  letter-spacing="2"
                  text-anchor="middle"
                  transform="rotate(-28 140 86)">JLPTSUCCESS.COM</text>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#jlpts-watermark)" />
      </svg>
    </div>
  `}function F(n){return`
    <header class="print-paper-cover">
      <p class="print-paper-brand">JLPTSuccess \xB7 JLPT N5</p>
      <h1 class="print-paper-title" lang="ja">${s(n.name_ja||n.name_en||"")}</h1>
      ${n.name_en&&n.name_en!==n.name_ja?`<p class="print-paper-title-en">${s(n.name_en)}</p>`:""}
      <dl class="print-paper-cover-meta">
        <dt>Questions</dt><dd>${n.total_q}</dd>
        ${n.duration_min?`<dt>Time allowed</dt><dd>${n.duration_min} min</dd>`:""}
        <dt>Date</dt><dd class="print-paper-fillable">________________</dd>
        <dt>Name</dt><dd class="print-paper-fillable">________________________________</dd>
      </dl>
      <section class="print-paper-instructions">
        <h2>Instructions</h2>
        ${n.instructions}
      </section>
    </header>
  `}function k(n){const t=`
    <ol>
      <li>Write your name and the date in the spaces above.</li>
      <li>Read each question carefully and circle <strong>one</strong> answer per question.</li>
      <li>Do not write outside the answer area; erasers are permitted.</li>
      <li>If you change your mind, cross out the wrong answer cleanly and circle your new choice.</li>
    </ol>
  `;switch(n){case"full-mock":return`
        <p>This is a 105-minute, three-section mock paper modelled on the real JLPT N5 sitting.</p>
        ${t}
        <p><strong>Section timing:</strong> 25 min for \u8A00\u8A9E\u77E5\u8B58\uFF08\u6587\u5B57\u30FB\u8A9E\u5F59\uFF09, 50 min for \u8A00\u8A9E\u77E5\u8B58\uFF08\u6587\u6CD5\uFF09\u30FB\u8AAD\u89E3, 30 min for \u8074\u89E3. Take a brief stretch between sections; do <strong>not</strong> exceed total 105 min.</p>
      `;case"chokai":return`
        <p>This is a printed transcript of a listening section. The audio is not on paper \u2014 play it from your phone or computer while marking answers here.</p>
        ${t}
        <p><strong>Audio source:</strong> on the JLPTSuccess web app, open the Listening tab and play the items in order. Each item is read once at JLPT-N5 pace.</p>
      `;case"combined":return`
        <p>This is a combined-section paper. Time yourself for the full section; do <strong>not</strong> pause between sub-sections.</p>
        ${t}
      `;default:return t}}function U(n){const t=new Map;return n.forEach(a=>{const i=a.mondai==null?0:a.mondai;t.has(i)||t.set(i,[]),t.get(i).push(a)}),[...t.entries()].sort((a,i)=>a[0]-i[0]).map(([a,i])=>({mondai:a,questions:i}))}function A(n,t){if(!t)return n.label_ja||n.label_en||"Questions";const a=(n.label_en||"").toLowerCase(),i={moji:["","\u554F\u984C1 \u6F22\u5B57\u8AAD\u307F","\u554F\u984C2 \u8868\u8A18","\u554F\u984C3 \u6587\u8108\u898F\u5B9A","\u554F\u984C4 \u8A00\u3044\u63DB\u3048","\u554F\u984C5 \u7528\u6CD5"],goi:["","\u554F\u984C1 \u6587\u8108\u898F\u5B9A","\u554F\u984C2 \u8A00\u3044\u63DB\u3048\u985E\u7FA9","\u554F\u984C3 \u7528\u6CD5","\u554F\u984C4","\u554F\u984C5"],bunpou:["","\u554F\u984C1 \u6587\u306E\u6587\u6CD5 (1)","\u554F\u984C2 \u6587\u306E\u6587\u6CD5 (2) (\u4E26\u3079\u66FF\u3048)","\u554F\u984C3 \u6587\u7AE0\u306E\u6587\u6CD5"],dokkai:["","\u554F\u984C4 \u5185\u5BB9\u7406\u89E3 (\u77ED\u6587)","\u554F\u984C5 \u5185\u5BB9\u7406\u89E3 (\u4E2D\u6587)","\u554F\u984C6 \u60C5\u5831\u691C\u7D22"],listening:["","\u554F\u984C1 \u8AB2\u984C\u7406\u89E3","\u554F\u984C2 \u30DD\u30A4\u30F3\u30C8\u7406\u89E3","\u554F\u984C3 \u767A\u8A71\u8868\u73FE","\u554F\u984C4 \u5373\u6642\u5FDC\u7B54"]},e=i[a]||i[n.label_en&&n.label_en.toLowerCase()]||null;return e&&e[t]?`<span lang="ja">${s(e[t])}</span>`:`<span lang="ja">\u554F\u984C${t}</span>`}function B(n,t){const a=(n.label_en||"").toLowerCase();return{"moji-1":'<p class="print-mondai-instr" lang="ja">_____ \u306E\u3053\u3068\u3070\u306E \u3088\u307F\u304B\u305F\u3092 \u3048\u3089\u3093\u3067\u304F\u3060\u3055\u3044\u3002</p>',"moji-2":'<p class="print-mondai-instr" lang="ja">_____ \u306E\u3053\u3068\u3070\u3092 \u304B\u3093\u3058\u3067 \u304B\u3044\u3066\u3042\u308B\u306E\u306F \u3069\u308C\u3067\u3059\u304B\u3002</p>',"goi-1":'<p class="print-mondai-instr" lang="ja">(  ) \u306B \u306A\u306B\u3092 \u3044\u308C\u307E\u3059\u304B\u3002\u3044\u3061\u3070\u3093 \u3044\u3044\u3082\u306E\u3092 \u3048\u3089\u3093\u3067\u304F\u3060\u3055\u3044\u3002</p>',"bunpou-1":'<p class="print-mondai-instr" lang="ja">(  ) \u306B \u306A\u306B\u3092 \u3044\u308C\u307E\u3059\u304B\u3002\u3044\u3061\u3070\u3093 \u3044\u3044\u3082\u306E\u3092 \u3048\u3089\u3093\u3067\u304F\u3060\u3055\u3044\u3002</p>',"bunpou-2":'<p class="print-mondai-instr" lang="ja">_\u2605_ \u306B \u306F\u3044\u308B \u3082\u306E\u306F \u3069\u308C\u3067\u3059\u304B\u30021\u30FB2\u30FB3\u30FB4 \u304B\u3089 \u3044\u3061\u3070\u3093 \u3044\u3044 \u3082\u306E\u3092 \u3048\u3089\u3093\u3067\u304F\u3060\u3055\u3044\u3002</p>',"dokkai-4":'<p class="print-mondai-instr" lang="ja">\u3064\u304E\u306E \u6587\u3092 \u3088\u3093\u3067\u3001\u3057\u3064\u3082\u3093\u306B \u3053\u305F\u3048\u3066\u304F\u3060\u3055\u3044\u3002</p>',"dokkai-6":'<p class="print-mondai-instr" lang="ja">\u3064\u304E\u306E \u30DA\u30FC\u30B8\u3092 \u898B\u3066\u3001\u3057\u3064\u3082\u3093\u306B \u3053\u305F\u3048\u3066\u304F\u3060\u3055\u3044\u3002</p>',"listening-1":'<p class="print-mondai-instr" lang="ja">\u554F\u984C1: \u4E8C\u4EBA\u306E\u8A71\u3092\u805E\u3044\u3066\u3001\u7537\u306E\u4EBA (\u5973\u306E\u4EBA) \u306F\u6B21\u306B\u4F55\u3092\u3057\u307E\u3059\u304B\u30021\u30FB2\u30FB3\u30FB4 \u304B\u3089\u3001\u3044\u3061\u3070\u3093 \u3044\u3044\u3082\u306E\u3092 \u3048\u3089\u3093\u3067\u304F\u3060\u3055\u3044\u3002</p>',"listening-3":'<p class="print-mondai-instr" lang="ja">\u554F\u984C3: \u5834\u9762\u3092\u898B\u306A\u304C\u3089\u77E2\u5370 (\u2192) \u306E\u4EBA\u306F\u4F55\u3068\u8A00\u3044\u307E\u3059\u304B\u30021\u30FB2\u30FB3 \u304B\u3089\u3001\u3044\u3061\u3070\u3093 \u3044\u3044\u3082\u306E\u3092 \u3048\u3089\u3093\u3067\u304F\u3060\u3055\u3044\u3002</p>',"listening-4":'<p class="print-mondai-instr" lang="ja">\u554F\u984C4: \u6587\u3092\u805E\u3044\u3066\u3001\u305D\u308C\u306B\u5BFE\u3059\u308B\u7B54\u3048\u3068\u3057\u3066\u3001\u3044\u3061\u3070\u3093 \u3044\u3044\u3082\u306E\u3092 \u3048\u3089\u3093\u3067\u304F\u3060\u3055\u3044\u3002</p>'}[`${a}-${t}`]||""}function N(n,t){const a=String(n.stem_html||n.prompt_html||n.prompt_ja||"").trim(),e=(n.choices||[]).map((r,l)=>`
    <li class="print-choice">
      <span class="print-choice-num">${M(l+1)}</span>
      <span class="print-choice-text" lang="ja">${s(r)}</span>
    </li>
  `).join("");return`
    <li class="print-q" id="print-q-${s(n.id||"")}">
      <header class="print-q-header">
        <span class="print-q-id muted small">${s(n.id||"")}</span>
        ${t?'<span class="print-q-audio-hint muted small">(audio plays once)</span>':""}
      </header>
      <div class="print-q-stem" lang="ja">${a}</div>
      <ol class="print-q-choices">${e}</ol>
    </li>
  `}function O(n){const t=n.prompt_ja||"",a=n.script_ja||"";return`
    <p class="print-chokai-prompt"><strong>${s(n.title_ja||n.id||"")}</strong> &nbsp; ${s(t)}</p>
    <pre class="print-chokai-script">${s(a)}</pre>
  `}function R(n){return`
    <section class="print-key" aria-labelledby="print-key-h">
      <h2 id="print-key-h">Answer key</h2>
      <p class="muted small">Cut along this line before handing the paper to a learner; or print without the answer key by removing <code>?key=1</code> from the URL.</p>
      ${n.map(a=>{const i=a.questions.map(e=>{const r=M((e.correctIndex||0)+1),l=(e.choices||[])[e.correctIndex||0]||"",o=(e.rationale||"").trim();return`
        <li>
          <span class="print-key-id">${s(e.id||"")}</span>
          <span class="print-key-correct">${r}</span>
          <span class="print-key-text" lang="ja">${s(l)}</span>
          ${o?`<p class="print-key-why muted small" lang="ja">${s(o)}</p>`:""}
        </li>
      `}).join("");return`
      <section class="print-key-section">
        <h3>${s(a.label_en||a.label_ja||"Section")}</h3>
        <ol class="print-key-list">${i}</ol>
      </section>
    `}).join("")}
    </section>
  `}function M(n){return["","\u2460","\u2461","\u2462","\u2463","\u2464","\u2465","\u2466","\u2467","\u2468"][n]||String(n)}function s(n){return String(n??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{z as renderPrint};
