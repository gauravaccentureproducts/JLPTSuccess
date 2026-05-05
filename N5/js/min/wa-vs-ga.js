import{renderJa as l}from"./furigana.js";import{matchesAnswer as f}from"./normalize.js";const p=[{use:"Topic vs new info",explanation_en:"\u306F marks a TOPIC the listener already knows. \u304C marks NEW info - often as the answer to a question.",a:{sentence:"\u308F\u305F\u3057___ \u304C\u304F\u305B\u3044\u3067\u3059\u3002",particle:"\u306F",context:"Self-introduction; the listener doesn't already know who you are, but in self-intro context the speaker is implicitly the topic."},b:{sentence:"\u3060\u308C___ \u304C\u304F\u305B\u3044\u3067\u3059\u304B\u3002",particle:"\u304C",context:"Who is the student? - question word + \u304C."}},{use:"Stative predicate",explanation_en:"\u3059\u304D, \u304D\u3089\u3044, \u308F\u304B\u308B, \u3067\u304D\u308B, \u3042\u308B, \u3044\u308B, \u307B\u3057\u3044, \u4E0A\u624B, \u4E0B\u624B ALL take \u304C, never \u3092.",a:{sentence:"\u306D\u3053___ \u3059\u304D\u3067\u3059\u3002",particle:"\u304C",context:"\u3059\u304D (like) is stative \u2192 \u304C, never \u3092."},b:{sentence:"\u65E5\u672C\u8A9E___ \u308F\u304B\u308A\u307E\u3059\u304B\u3002",particle:"\u304C",context:"\u308F\u304B\u308B takes \u304C."}},{use:"Existence",explanation_en:"There-is sentences put the EXISTING THING with \u304C and the location with \u306B.",a:{sentence:"\u3078\u3084\u306B \u306D\u3053___ \u3044\u307E\u3059\u3002",particle:"\u304C",context:"The cat (new info) is in the room."},b:{sentence:"\u306D\u3053___ \u3069\u3053\u306B \u3044\u307E\u3059\u304B\u3002",particle:"\u306F",context:"As for the cat (already-known topic), where is it? Different framing - topic-first."}},{use:"Neutral description",explanation_en:`Pure description of what one observes uses \u304C. (\u96E8\u304C \u3075\u3063\u3066\u3044\u308B = "It's raining" - no topic implied.)`,a:{sentence:"\u3042\u3081___ \u3075\u3063\u3066\u3044\u307E\u3059\u3002",particle:"\u304C",context:"Neutral description - there's rain falling."},b:{sentence:"\u304D\u3087\u3046___ \u3042\u3064\u3044\u3067\u3059\u3002",particle:"\u306F",context:`"As for today, it's hot" - topical comment about a known frame (today).`}},{use:"X\u306FY\u304C (X has Y)",explanation_en:'The "X has Y" / "X is Y-ish" pattern combines both: X (topic) \u306F + Y (what) \u304C + adjective.',a:{sentence:"\u305E\u3046___ \u306F\u306A___ \u306A\u304C\u3044\u3067\u3059\u3002",particle:["\u306F","\u304C"],context:"As for the elephant, the nose is long. (= elephants have long noses)"},b:{sentence:"\u308F\u305F\u3057___ \u304B\u306E\u3058\u3087___ \u3044\u307E\u3059\u3002",particle:["\u306F","\u304C"],context:"I have a girlfriend. (Topic: I; what exists: a girlfriend.)"}}];let n=null;async function m(e){e.innerHTML=`
    <h2>\u306F vs \u304C - five uses</h2>
    <p>The \u306F / \u304C distinction is the single most-tested grammar point at N5. Five core uses are below, each with a minimal pair.</p>

    ${w()}
    ${h()}
  `,_(e)}function w(){return p.map((e,t)=>`
    <section class="waga-use">
      <h3>${t+1}. ${a(e.use)}</h3>
      <p>${a(e.explanation_en)}</p>
      <div class="waga-pair">
        <div class="waga-side">
          <p class="waga-sentence">${l(u(e.a.sentence,e.a.particle))}</p>
          <p class="waga-context muted small">${a(e.a.context)}</p>
        </div>
        <div class="waga-side">
          <p class="waga-sentence">${l(u(e.b.sentence,e.b.particle))}</p>
          <p class="waga-context muted small">${a(e.b.context)}</p>
        </div>
      </div>
    </section>
  `).join("")}function u(e,t){if(Array.isArray(t)){let i=0;return e.replace(/___/g,()=>t[i++]??"___")}return e.split("___").join(t)}function h(){if(!n)return`
      <section class="waga-drill">
        <h3>Minimal-pair drill</h3>
        <p>Type the missing particle (\u306F or \u304C) for each blank, then click Check. Both translations are shown after - focus on the meaning difference.</p>
        <button id="waga-start" class="btn-primary">Start drill</button>
      </section>
    `;const{current:e,feedback:t,score:i,total:r}=n,s=Array.isArray(e.particle)?e.particle.length:1,c=Array.from({length:s},(x,d)=>`
    <input type="text" data-waga-input data-idx="${d}"
           class="text-input waga-input" lang="ja"
           autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"
           placeholder="\u306F or \u304C" maxlength="2" value="${a((n.userValues||[])[d]||"")}"
           ${t?"disabled":""}>
  `).join(" ");return`
    <section class="waga-drill">
      <h3>Minimal-pair drill <span class="muted small">(${i} / ${r})</span></h3>
      <p class="muted">Use: <strong>${a(e.useLabel)}</strong></p>
      <p class="waga-sentence">${l(e.sentenceWithBlanks).replace(/___/g,()=>`__BLANK__${c}`)}</p>
      <p class="waga-sentence">${l(e.sentenceWithBlanks).replace(/___/g,"\uFF3F")}</p>
      <div class="waga-blank-row">${c}</div>
      ${t?`
        <div class="drill-feedback ${t.correct?"correct":"incorrect"}">
          <div class="feedback-headline">${t.correct?"Correct":"Wrong"}</div>
          <p>Expected: <strong lang="ja">${a(Array.isArray(e.particle)?e.particle.join(" / "):e.particle)}</strong></p>
          <p class="muted small">${a(e.context)}</p>
        </div>
        <button id="waga-next" class="btn-primary">Next</button>
      `:`
        <button id="waga-check" class="btn-primary">Check</button>
      `}
      <button id="waga-stop" style="margin-left: 8px">End drill</button>
    </section>
  `}function _(e){document.getElementById("waga-start")?.addEventListener("click",()=>{n={score:0,total:0},g(),o(e)}),document.getElementById("waga-stop")?.addEventListener("click",()=>{n=null,o(e)}),document.getElementById("waga-check")?.addEventListener("click",()=>{const t=Array.from(document.querySelectorAll("[data-waga-input]"));n.userValues=t.map(s=>s.value);const r=(Array.isArray(n.current.particle)?n.current.particle:[n.current.particle]).every((s,c)=>f(n.userValues[c]||"",[s]));n.feedback={correct:r},n.total+=1,r&&(n.score+=1),o(e)}),document.getElementById("waga-next")?.addEventListener("click",()=>{g(),o(e)})}function g(){const e=p[Math.floor(Math.random()*p.length)],t=Math.random()<.5?"a":"b";n.current={useLabel:e.use,sentenceWithBlanks:e[t].sentence,particle:e[t].particle,context:e[t].context},n.feedback=null,n.userValues=[]}function o(e){const t=e.querySelector(".waga-drill");if(!t){e.innerHTML="",m(e);return}t.outerHTML=h(),_(e)}function a(e){return String(e??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{m as renderWaGa};
