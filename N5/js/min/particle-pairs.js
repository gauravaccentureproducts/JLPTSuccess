import{renderJa as o}from"./furigana.js";const u=[{set:"\u306B vs \u3067 (location)",a:{sentence:"\u3078\u3084\u306B \u306D\u3053\u304C \u3044\u307E\u3059\u3002",particle:"\u306B",en_with:"There is a cat in the room (existence - location of being)."},b:{sentence:"\u3078\u3084\u3067 \u3057\u3085\u304F\u3060\u3044\u3092 \u3057\u307E\u3059\u3002",particle:"\u3067",en_with:"I do homework in the room (action - location of doing)."}},{set:"\u306B vs \u3067 (location)",a:{sentence:"\u3053\u3046\u3048\u3093\u306B \u6728\u304C \u3042\u308A\u307E\u3059\u3002",particle:"\u306B",en_with:"There are trees in the park."},b:{sentence:"\u3053\u3046\u3048\u3093\u3067 \u3042\u305D\u3073\u307E\u3059\u3002",particle:"\u3067",en_with:"I play in the park."}},{set:"\u306B vs \u3078 (direction)",a:{sentence:"\u65E5\u672C\u306B \u884C\u304D\u307E\u3059\u3002",particle:"\u306B",en_with:"I go TO Japan (focus on arrival/destination)."},b:{sentence:"\u65E5\u672C\u3078 \u884C\u304D\u307E\u3059\u3002",particle:"\u3078",en_with:"I go TOWARD Japan (focus on direction; slightly more formal)."}},{set:"\u3092 vs \u304C (with stative)",a:{sentence:"\u306D\u3053\u304C \u3059\u304D\u3067\u3059\u3002",particle:"\u304C",en_with:"I like cats (stative - must take \u304C)."},b:{sentence:"\u308A\u3093\u3054\u3092 \u98DF\u3079\u307E\u3059\u3002",particle:"\u3092",en_with:"I eat apples (action verb - direct object takes \u3092)."}},{set:"\u3068 vs \u306B (people / interaction)",a:{sentence:"\u3068\u3082\u3060\u3061\u3068 \u884C\u304D\u307E\u3059\u3002",particle:"\u3068",en_with:"I go WITH a friend (companion)."},b:{sentence:"\u3068\u3082\u3060\u3061\u306B \u4F1A\u3044\u307E\u3059\u3002",particle:"\u306B",en_with:"I meet a friend (\u4F1A\u3046 takes \u306B for the person met)."}},{set:"\u304B vs \u3084 (listing / alternative)",a:{sentence:"\u30B3\u30FC\u30D2\u30FC\u304B \u304A\u3061\u3083\u304C \u3044\u3044\u3067\u3059\u3002",particle:"\u304B",en_with:"Coffee OR tea is good (alternatives - pick one)."},b:{sentence:"\u30B3\u30FC\u30D2\u30FC\u3084 \u304A\u3061\u3083\u304C \u3059\u304D\u3067\u3059\u3002",particle:"\u3084",en_with:"I like coffee, tea, etc. (non-exhaustive listing)."}},{set:"\u306F vs \u304C (topic / new info)",a:{sentence:"\u308F\u305F\u3057\u306F \u304C\u304F\u305B\u3044\u3067\u3059\u3002",particle:"\u306F",en_with:"I am a student (topical statement; \u308F\u305F\u3057 is the topic)."},b:{sentence:"\u3060\u308C\u304C \u304C\u304F\u305B\u3044\u3067\u3059\u304B\u3002",particle:"\u304C",en_with:"Who is the student? (question word + \u304C - asking for new info)."}}];let n=null;async function k(t){return n?l(t):g(t)}function g(t){t.innerHTML=`
    <h2>Particle minimal-pair drill</h2>
    <p>Each round shows two sentences differing by one particle. Both are grammatical - the <strong>meaning</strong> changes. After your pick, both translations appear so you can train the meaning difference, not just the "correct" particle.</p>
    <p class="muted small">Pairs covered: ${[...new Set(u.map(e=>e.set))].join(" \xB7 ")}</p>
    <button id="pp-start" class="btn-primary">Start (10 rounds)</button>
  `,document.getElementById("pp-start").addEventListener("click",()=>{n={idx:0,total:10,queue:m(10),score:0,history:[]},l(t)})}function m(t){const e=[];for(let a=0;a<t;a++){const r=u[Math.floor(Math.random()*u.length)],i=Math.random()<.5?"a":"b",c=r[i],s=r[i==="a"?"b":"a"];e.push({set:r.set,target:c,other:s})}return e}function l(t){const e=n.queue[n.idx],a=n.feedback,r=e.target.sentence.replace(e.target.particle,"\uFF08\u3000\uFF09"),i=Array.from(new Set([e.target.particle,e.other.particle])).sort(),c=["\u306F","\u304C","\u3092","\u306B","\u3067","\u3078","\u3068","\u304B\u3089","\u307E\u3067","\u3084","\u304B","\u3082"].filter(s=>!i.includes(s));for(;i.length<4&&c.length;){const s=Math.floor(Math.random()*c.length);i.push(c.splice(s,1)[0])}v(i),t.innerHTML=`
    <div class="pp-round">
      <div class="srs-progress">
        <span>Round <strong>${n.idx+1}</strong> / <strong>${n.total}</strong></span>
        <span class="muted small">Set: ${d(e.set)} \xB7 Score: ${n.score}</span>
      </div>
      <article class="pp-card">
        <p class="pp-sentence" lang="ja">${o(r)}</p>
        <div class="choice-grid">
          ${i.map(s=>`<button class="choice-button${a?s===e.target.particle?" correct-choice":s===a.picked&&s!==e.target.particle?" wrong-choice":"":""}" data-pick="${d(s)}" ${a?"disabled":""}>${o(s)}</button>`).join("")}
        </div>
        ${a?`
          <div class="drill-feedback ${a.correct?"correct":"incorrect"}">
            <div class="feedback-headline">${a.correct?"Correct":"Wrong"}</div>
            <p>The intended sentence: <strong lang="ja">${o(e.target.sentence)}</strong></p>
            <p class="muted small">${d(e.target.en_with)}</p>
            <hr style="border: none; border-top: 1px solid var(--c-border); margin: 8px 0;">
            <p>The other particle would mean:</p>
            <p><strong lang="ja">${o(e.other.sentence)}</strong></p>
            <p class="muted small">${d(e.other.en_with)}</p>
            <button id="pp-next" class="btn-primary">${n.idx===n.total-1?"Finish":"Next"}</button>
          </div>
        `:""}
      </article>
    </div>
  `,t.querySelectorAll("[data-pick]").forEach(s=>{s.addEventListener("click",()=>{const p=s.dataset.pick,h=p===e.target.particle;n.feedback={picked:p,correct:h},h&&(n.score+=1),n.history.push({set:e.set,picked:p,correct:h,target:e.target.particle}),l(t)})}),document.getElementById("pp-next")?.addEventListener("click",()=>{n.feedback=null,n.idx+=1,n.idx>=n.total?f(t):l(t)})}function f(t){const e=n.total,a=Math.round(n.score/e*100);t.innerHTML=`
    <h2>Particle pairs - done</h2>
    <section class="srs-summary-stats">
      <div class="stat-card mastered"><div class="stat-num">${n.score}/${e}</div><div class="stat-label">Score</div></div>
      <div class="stat-card ${a>=70?"mastered":"weak"}"><div class="stat-num">${a}%</div><div class="stat-label">Accuracy</div></div>
    </section>
    <div class="test-nav">
      <button id="pp-restart" class="btn-primary">Try again</button>
      <button id="pp-back">Back</button>
    </div>
  `,document.getElementById("pp-restart").addEventListener("click",()=>{n=null,g(t)}),document.getElementById("pp-back").addEventListener("click",()=>{location.hash="#/learn"})}function v(t){for(let e=t.length-1;e>0;e--){const a=Math.floor(Math.random()*(e+1));[t[e],t[a]]=[t[a],t[e]]}return t}function d(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{k as renderParticlePairs};
