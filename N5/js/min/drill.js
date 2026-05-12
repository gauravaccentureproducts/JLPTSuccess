import{renderJa as b}from"./furigana.js";import*as $ from"./storage.js";import{t as _}from"./i18n.js";import{attachRomajiKanaAll as E}from"./romaji-kana.js";let w=null,h=null,d=null,g="setup";async function P(){if(w)return w;const e=await fetch("data/questions.json");if(!e.ok)throw new Error(`Failed to load questions.json: ${e.status}`);return w=(await e.json()).questions||[],w}async function S(){if(h)return h;const t=await(await fetch("data/grammar.json")).json();return h=new Map((t.patterns||[]).map(n=>[n.id,n])),h}async function N(e){return g==="finished"&&(g="setup",d=null),g==="drilling"&&d?m(e):g==="finished"&&d?j(e):A(e)}async function A(e){g="setup",await Promise.all([P(),S()]);const t=$.getDuePatternIds(),n=Object.entries($.getHistory()),r=n.filter(([,a])=>a.srsBox&&a.srsBox!=="graduated").length,s=n.filter(([,a])=>a.srsBox==="graduated").length;if(t.length===0){e.innerHTML=`
      <h2>${_("page.drill")}</h2>
      <div class="placeholder">
        <p><strong>No patterns due right now.</strong></p>
        <p>Patterns enter Drill the moment you miss them in a Test or Diagnostic. Once in Drill, they reappear at <strong>1d / 3d / 7d / 14d</strong> intervals - graduate after 4 consecutive correct answers.</p>
        <p class="muted">Queue: <strong>${r}</strong> pending \xB7 <strong>${s}</strong> graduated</p>
        <p style="margin-top:24px"><a href="#/test" class="btn-primary" style="text-decoration:none">Take a Test \u2192</a></p>
      </div>
    `;return}const o=L(t,w,10);if(o.length===0){e.innerHTML=`
      <h2>${_("page.drill")}</h2>
      <div class="placeholder">
        <p><strong>${t.length}</strong> pattern(s) due, but no questions exist for them yet.</p>
        <p class="muted">Add questions for these patterns to <code>data/questions.json</code>.</p>
      </div>
    `;return}e.innerHTML=`
    <h2>${_("page.drill")}</h2>
    <div class="drill-setup">
      <div class="drill-stats">
        <div class="stat-card weak"><div class="stat-num">${t.length}</div><div class="stat-label">Due today</div></div>
        <div class="stat-card neutral"><div class="stat-num">${r}</div><div class="stat-label">In queue</div></div>
        <div class="stat-card mastered"><div class="stat-num">${s}</div><div class="stat-label">Graduated</div></div>
      </div>
      <p>Drill session: <strong>${o.length}</strong> question(s) from due patterns. You'll get feedback after each question. Correct answers advance the SRS box (1d \u2192 3d \u2192 7d \u2192 14d \u2192 graduated). A wrong answer resets the pattern to the 1-day box.</p>
      <button id="start-drill" class="btn-primary">Start Drill</button>
    </div>
  `,document.getElementById("start-drill").addEventListener("click",()=>{d={questions:o,currentIdx:0,answers:{},startedAt:new Date().toISOString()},g="drilling",m(e)})}function L(e,t,n){const r=new Set(e),s=t.filter(i=>r.has(i.grammarPatternId));B(s);const o=new Set,a=[];for(const i of s)o.has(i.grammarPatternId)||(a.push(i),o.add(i.grammarPatternId));const l=s.filter(i=>!a.includes(i));return[...a,...l].slice(0,n)}function B(e){for(let t=e.length-1;t>0;t--){const n=Math.floor(Math.random()*(t+1));[e[t],e[n]]=[e[n],e[t]]}return e}function m(e){const t=d.questions.length,n=d.currentIdx,r=d.questions[n],s=d.answers[r.id],o=!!s,a=h.get(r.grammarPatternId),l=a?a.pattern:r.grammarPatternId;let i="";r.type==="mcq"||r.type==="dropdown"?i=T(r,s):r.type==="sentence_order"?i=D(r,s):(r.type==="text_input"||r.type==="cloze"||r.type==="production")&&(i=M(r,s));const c=o?z(r,s):"",u=x(r,s),v=!o&&!u?`<p class="check-answer-hint">${r.type==="sentence_order"?"Tap the tiles in order to build the sentence, then click Check Answer.":r.type==="text_input"?"Type your answer in the box, then click Check Answer.":"Pick a choice, then click Check Answer."}</p>`:"",k=o?`<button id="next-drill" class="btn-primary">${n===t-1?"Finish Drill":"Next Question \u2192"}</button>`:`${v}<button id="check-answer" class="btn-primary" ${u?"":"disabled"} title="${u?"Check your answer":"Answer the question first"}">Check Answer</button>`;if(e.innerHTML=`
    <div class="drill-session">
      <div class="drill-header">
        <span>Drill \xB7 Question <strong>${n+1}</strong> of <strong>${t}</strong></span>
        <span class="pattern-tag">Pattern: ${f(l)}</span>
      </div>
      <div class="progress-bar"><div style="width:${(n+(o?1:.5))/t*100}%"></div></div>

      <article class="question-card">
        <p class="prompt">${f(r.prompt_ja||"")}</p>
        ${r.question_ja?`<p class="question">${b(r.question_ja)}</p>`:""}
        ${i}
        ${c}
      </article>

      <div class="test-nav">${k}</div>
    </div>
  `,o)document.getElementById("next-drill")?.addEventListener("click",()=>K(e));else{e.querySelectorAll("[data-choice]").forEach(p=>{p.addEventListener("click",()=>{d.answers[r.id]||(d.draftAnswer=p.dataset.choice,d.questions[n]._draft=p.dataset.choice,m(e))})}),e.querySelectorAll("[data-tile-add]").forEach(p=>{p.addEventListener("click",()=>H(r,p.dataset.tileAdd,e))}),e.querySelectorAll("[data-tile-remove]").forEach(p=>{p.addEventListener("click",()=>R(r,parseInt(p.dataset.tileRemove,10),e))}),E(e);const y=e.querySelector("[data-drill-text-input]");y&&(y.addEventListener("input",()=>{r._draft=y.value;const p=document.getElementById("check-answer");p&&(p.disabled=!x(r,null))}),y.addEventListener("keydown",p=>{p.key==="Enter"&&x(r,null)&&(p.preventDefault(),I(r,e))}),d.answers[r.id]||Promise.resolve().then(()=>y.focus())),document.getElementById("check-answer")?.addEventListener("click",()=>I(r,e))}}function T(e,t){const n=t?t.answer:e._draft;return`<div class="choice-grid">${(e.choices||[]).map(s=>{let o="choice-button";return t?(s===e.correctAnswer&&(o+=" correct-choice"),t.answer===s&&s!==e.correctAnswer&&(o+=" wrong-choice")):n===s&&(o+=" selected"),`<button type="button" data-choice="${f(s)}" class="${o}" ${t?"disabled":""}>${b(s)}</button>`}).join("")}</div>`}function D(e,t){const n=t?t.answer:e._draft||[],r=(e.tiles||[]).filter(a=>!n.includes(a)),s=n.length?n.map((a,l)=>{let i="tile ordered";return t&&(i=`tile ordered ${e.correctOrder?.[l]===a?"correct-tile":"wrong-tile"}`),`<button type="button" ${t?"disabled":`data-tile-remove="${l}"`} class="${i}">${b(a)}</button>`}).join(""):'<span class="tile-placeholder">Click tiles below to build the sentence</span>',o=r.map(a=>`<button type="button" ${t?"disabled":`data-tile-add="${f(a)}"`} class="tile">${b(a)}</button>`).join("");return`
    <div class="sentence-order">
      <div class="ordered-tray">${s}</div>
      <div class="tile-pool">${o}</div>
    </div>
  `}function x(e,t){return t?!0:e.type==="sentence_order"?Array.isArray(e._draft)&&e._draft.length===(e.tiles?.length||0):e.type==="text_input"||e.type==="cloze"||e.type==="production"?typeof e._draft=="string"&&e._draft.trim().length>0:e._draft!==void 0&&e._draft!==null&&e._draft!==""}function M(e,t){const n=t?t.answer:e._draft||"",r=!!t,s=f(n),o=e.question_ja||"",a=/[\(（][\s　]*[\)）]/,l=a.test(o);let i="drill-text-input";r&&(i+=t.isCorrect?" drill-text-input-correct":" drill-text-input-wrong");const c=`
    <input type="text" data-drill-text-input data-jp-input
           class="${i}"
           ${r?"disabled":""}
           autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"
           value="${s}"
           placeholder="${e.type==="production"?"Type the Japanese sentence (romaji auto-converts)":"Type your answer (romaji auto-converts)"}"
           lang="ja">
  `;return l&&e.type!=="production"?`
      <div class="drill-text-input-block">
        <p class="drill-cloze-sentence" lang="ja">${o.split(a).map(f).join(`<span class="drill-cloze-blank">${c}</span>`)}</p>
      </div>
    `:`
    <div class="drill-text-input-block">
      ${c}
    </div>
  `}function H(e,t,n){e._draft||(e._draft=[]),!e._draft.includes(t)&&(e._draft.push(t),m(n))}function R(e,t,n){Array.isArray(e._draft)&&(e._draft.splice(t,1),m(n))}function W(e,t){return C(e,t).isCorrect}function C(e,t){if(e.type==="sentence_order"){if(!Array.isArray(t))return{isCorrect:!1,score:0,reason:"wrong_form"};const n=e.correctOrder||[];return t.length!==n.length?{isCorrect:!1,score:0,reason:"wrong_length"}:t.every((s,o)=>s===n[o])?{isCorrect:!0,score:1,reason:null}:{isCorrect:!1,score:0,reason:"wrong_order"}}if(e.type==="text_input"||e.type==="cloze"||e.type==="production"){if(typeof t!="string")return{isCorrect:!1,score:0,reason:"empty"};const n=c=>String(c||"").normalize("NFKC").replace(/[\s　]+/g,"").replace(/[。．.!?！？]+$/g,"").toLowerCase().trim(),r=n(t);if(!r)return{isCorrect:!1,score:0,reason:"empty"};if(n(e.correctAnswer)===r)return{isCorrect:!0,score:1,reason:null};const s=Array.isArray(e.acceptedAnswers)?e.acceptedAnswers:[];if(s.some(c=>n(c)===r))return{isCorrect:!0,score:1,reason:null};const o=c=>String(c||"").replace(/[぀-ゟ゠-ヿ]/g,""),a=c=>String(c||"").replace(/[^぀-ゟ゠-ヿ]/g,""),l=a(t),i=o(t);for(const c of[e.correctAnswer,...s]){if(!c)continue;const u=a(c),v=o(c);if(l&&u&&l===u)return{isCorrect:!1,score:.5,reason:"kana_form_correct"};if(i&&v&&i===v)return{isCorrect:!1,score:.5,reason:"kanji_form_correct"}}for(const c of[e.correctAnswer,...s])if(c&&O(r,n(c)))return{isCorrect:!1,score:.5,reason:"one_char_typo"};return{isCorrect:!1,score:0,reason:"wrong"}}return t===e.correctAnswer?{isCorrect:!0,score:1,reason:null}:{isCorrect:!1,score:0,reason:"wrong"}}function O(e,t){if(e===t)return!0;const n=e.length,r=t.length;if(Math.abs(n-r)>1)return!1;if(n===r){let c=0;for(let u=0;u<n;u++)if(e[u]!==t[u]&&(c++,c>1))return!1;return c===1}const s=n>r?e:t,o=n>r?t:e;let a=0,l=0,i=0;for(;a<s.length&&l<o.length;)if(s[a]===o[l])a++,l++;else{if(i++,i>1)return!1;a++}return!0}function I(e,t){const n=e._draft,r=C(e,n),s=r.isCorrect;d.answers[e.id]={answer:n,isCorrect:s,score:r.score,partial_reason:r.reason,recorded:!1},$.recordDrillResponse(e.grammarPatternId,s),d.answers[e.id].recorded=!0,m(t)}function z(e,t){const n=t.isCorrect,r=h.get(e.grammarPatternId),s=!n&&e.distractor_explanations&&typeof t.answer=="string"?e.distractor_explanations[t.answer]:null,o=$.getPatternEntry(e.grammarPatternId),a=o?.srsBox||"?",l=o?.consecutiveCorrect??0;let i="";n?a==="graduated"?i='<strong class="graduated">Graduated.</strong> Pattern mastered.':i=`Advanced to <strong>${a}</strong> box. ${l}/4 consecutive correct.`:i="Reset to the <strong>1d</strong> box. This pattern returns tomorrow.";const c=t.score,u=t.partial_reason,k=c===.5&&u?`<p class="feedback-partial-credit"><strong>Half-credit</strong> (50%): ${f({kana_form_correct:"Reading is right \u2014 the canonical answer uses the kanji form.",kanji_form_correct:"Kanji is right \u2014 the canonical answer uses the kana form.",one_char_typo:"One character off from the expected answer."}[u]||u)}</p>`:"";return`
    <div class="drill-feedback ${n?"correct":c===.5?"partial":"incorrect"}">
      <div class="feedback-headline">${n?"Correct":c===.5?"Close \u2014 half-credit":"Wrong"}</div>
      ${k}
      ${e.explanation_en?`<p class="feedback-explanation">${f(e.explanation_en)}</p>`:""}
      ${s?`<p class="feedback-distractor"><em>Why your choice was off:</em> ${f(s)}</p>`:""}
      <p class="feedback-srs">${i}</p>
      ${r?`<p class="feedback-pattern">Pattern: <a href="#/learn/${encodeURIComponent(r.id)}">${f(r.pattern)}</a></p>`:""}
    </div>
  `}function K(e){if(d.currentIdx===d.questions.length-1){g="finished",j(e);return}d.currentIdx+=1,m(e)}function j(e){const t=d.questions.length,n=Object.values(d.answers).filter(a=>a.isCorrect).length,r=t-n,s=new Map;for(const a of d.questions){const l=d.answers[a.id];s.has(a.grammarPatternId)||s.set(a.grammarPatternId,{right:0,wrong:0});const i=s.get(a.grammarPatternId);l?.isCorrect?i.right++:i.wrong++}const o=[...s.entries()].map(([a,l])=>{const i=h.get(a),c=$.getPatternEntry(a),u=c?.srsBox==="graduated"?"\u2605 graduated":c?.srsBox||"-";return`
      <li>
        <span class="pat-name">${f(i?.pattern||a)}</span>
        <span class="pat-stats">${l.right} right \xB7 ${l.wrong} wrong</span>
        <span class="pat-box">${f(u)}</span>
      </li>
    `}).join("");e.innerHTML=`
    <div class="drill-finished">
      <h2>Drill complete</h2>
      <div class="score-summary">
        <div class="score-headline">
          <span class="score-big">${n}/${t}</span>
        </div>
        <div class="score-meta">
          <span class="score-correct">${n} correct</span>
          <span class="score-incorrect">${r} incorrect</span>
        </div>
      </div>

      <h3>Pattern updates</h3>
      <ul class="pattern-summary-list">${o}</ul>

      <div class="test-nav">
        <button id="drill-again" class="btn-primary">Drill again</button>
        <button id="drill-back">Back to Learn</button>
      </div>
    </div>
  `,document.getElementById("drill-again")?.addEventListener("click",()=>{d=null,g="setup",A(e)}),document.getElementById("drill-back")?.addEventListener("click",()=>{location.hash="#/learn"})}function f(e){return String(e??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{N as renderDrill};
