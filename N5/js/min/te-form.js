import{matchesAnswer as k}from"./normalize.js";import*as u from"./storage.js";const v={"\u3046/\u3064/\u308B \u2192 \u3063\u3066":[{v:"\u304B\u3046",te:"\u304B\u3063\u3066",en:"buy"},{v:"\u307E\u3064",te:"\u307E\u3063\u3066",en:"wait"},{v:"\u3068\u308B",te:"\u3068\u3063\u3066",en:"take"},{v:"\u306E\u308B",te:"\u306E\u3063\u3066",en:"ride"},{v:"\u3042\u3046",te:"\u3042\u3063\u3066",en:"meet"},{v:"\u3059\u308F\u308B",te:"\u3059\u308F\u3063\u3066",en:"sit"},{v:"\u306F\u3057\u308B",te:"\u306F\u3057\u3063\u3066",en:"run (Group 1 exception)"},{v:"\u304D\u308B",te:"\u304D\u3063\u3066",en:"cut (Group 1 exception)"}],"\u306C/\u3076/\u3080 \u2192 \u3093\u3067":[{v:"\u306E\u3080",te:"\u306E\u3093\u3067",en:"drink"},{v:"\u3088\u3080",te:"\u3088\u3093\u3067",en:"read"},{v:"\u3042\u305D\u3076",te:"\u3042\u305D\u3093\u3067",en:"play"},{v:"\u3088\u3076",te:"\u3088\u3093\u3067",en:"call"},{v:"\u3057\u306C",te:"\u3057\u3093\u3067",en:"die"}],"\u304F \u2192 \u3044\u3066 (exception: \u3044\u304F \u2192 \u3044\u3063\u3066)":[{v:"\u304B\u304F",te:"\u304B\u3044\u3066",en:"write"},{v:"\u304D\u304F",te:"\u304D\u3044\u3066",en:"listen / ask"},{v:"\u306F\u305F\u3089\u304F",te:"\u306F\u305F\u3089\u3044\u3066",en:"work"},{v:"\u3044\u304F",te:"\u3044\u3063\u3066",en:"go (the famous exception!)"}],"\u3050 \u2192 \u3044\u3067":[{v:"\u304A\u3088\u3050",te:"\u304A\u3088\u3044\u3067",en:"swim"},{v:"\u3044\u305D\u3050",te:"\u3044\u305D\u3044\u3067",en:"hurry"}],"\u3059 \u2192 \u3057\u3066":[{v:"\u306F\u306A\u3059",te:"\u306F\u306A\u3057\u3066",en:"speak"},{v:"\u3051\u3059",te:"\u3051\u3057\u3066",en:"turn off"},{v:"\u304A\u3059",te:"\u304A\u3057\u3066",en:"push"}],"Group 2 (drop \u308B + \u3066)":[{v:"\u305F\u3079\u308B",te:"\u305F\u3079\u3066",en:"eat"},{v:"\u307F\u308B",te:"\u307F\u3066",en:"see"},{v:"\u304A\u304D\u308B",te:"\u304A\u304D\u3066",en:"wake up"},{v:"\u306D\u308B",te:"\u306D\u3066",en:"sleep"},{v:"\u304A\u3057\u3048\u308B",te:"\u304A\u3057\u3048\u3066",en:"teach"}],"Irregular (\u3059\u308B \u2192 \u3057\u3066, \u6765\u308B \u2192 \u304D\u3066)":[{v:"\u3059\u308B",te:"\u3057\u3066",en:"do"},{v:"\u304F\u308B",te:"\u304D\u3066",en:"come"},{v:"\u3079\u3093\u304D\u3087\u3046\u3059\u308B",te:"\u3079\u3093\u304D\u3087\u3046\u3057\u3066",en:"study"}]};let d="teach",r=null;async function w(s){return d==="drill"&&r?m(s):d==="finished"&&r?f(s):h(s)}function h(s){d="teach";const o=u.get("te-form-accuracy",{});s.innerHTML=`
    <h2>\u3066-form gym</h2>
    <p>The \u3066-form is the gateway to almost every later N5 grammar pattern (\u3066\u304F\u3060\u3055\u3044, \u3066\u3044\u307E\u3059, \u3066\u3082\u3044\u3044\u3067\u3059, etc.). Master the seven transformation rules first; the rest follows.</p>

    <section class="te-rules">
      <h3>Transformation rules</h3>
      <table class="te-rules-table">
        <thead><tr><th>Rule</th><th>Example</th><th>Your accuracy</th></tr></thead>
        <tbody>
          ${Object.entries(v).map(([t,n])=>{const a=o[t],e=a?`${a.correct}/${a.attempts} (${Math.round(a.correct/a.attempts*100)}%)`:"-",c=n[0];return`<tr><td>${l(t)}</td><td lang="ja">${l(c.v)} \u2192 ${l(c.te)}</td><td>${e}</td></tr>`}).join("")}
        </tbody>
      </table>
    </section>

    <section class="drill-cta">
      <h3>Drill</h3>
      <p>Type the \u3066-form for each dictionary-form verb. Kana or romaji is fine. After a miss, the rule you violated is shown.</p>
      <button id="te-start" class="btn-primary">Start drill (20 verbs)</button>
    </section>
  `,document.getElementById("te-start").addEventListener("click",()=>{r={queue:$(20),idx:0,score:0,grades:[]},d="drill",m(s)})}function $(s){const o=u.get("te-form-accuracy",{}),t=[];for(const[e,c]of Object.entries(v)){const i=o[e],g=i&&i.attempts>0?1-i.correct/i.attempts:.5,y=Math.max(1,Math.round(g*10));for(const b of c)for(let p=0;p<y;p++)t.push({...b,rule:e})}for(let e=t.length-1;e>0;e--){const c=Math.floor(Math.random()*(e+1));[t[e],t[c]]=[t[c],t[e]]}const n=new Set,a=[];for(const e of t)if(!n.has(e.v)&&(n.add(e.v),a.push(e),a.length>=s))break;return a}function m(s){const o=r.queue.length,t=r.queue[r.idx],n=r.feedback;s.innerHTML=`
    <div class="te-drill">
      <div class="srs-progress">
        <span>\u3066-form drill \xB7 <strong>${r.idx+1}</strong> / <strong>${o}</strong></span>
        <span class="muted small">${r.score}/${r.idx+0}</span>
      </div>
      <article class="vc-card">
        <p class="vc-prompt">Type the \u3066-form for:</p>
        <p class="vc-verb" lang="ja">${l(t.v)}</p>
        <p class="muted small">${l(t.en)}</p>
        <div style="margin: 16px 0">
          <input id="te-input" type="text" class="text-input" lang="ja"
                 autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"
                 placeholder="Type kana or romaji..." ${n?"disabled":""}>
        </div>
        ${n?`
          <div class="drill-feedback ${n.correct?"correct":"incorrect"}">
            <div class="feedback-headline">${n.correct?"Correct":"Wrong"}</div>
            <p>Answer: <strong lang="ja">${l(t.te)}</strong></p>
            <p class="muted small">Rule: <strong>${l(t.rule)}</strong></p>
            <button id="te-next" class="btn-primary">${r.idx===o-1?"Finish":"Next"}</button>
          </div>
        `:'<button id="te-check" class="btn-primary">Check</button>'}
      </article>
    </div>
  `,document.getElementById("te-check")?.addEventListener("click",()=>{const a=document.getElementById("te-input").value,e=k(a,[t.te]);r.feedback={correct:e,value:a},e&&(r.score+=1),r.grades.push({rule:t.rule,correct:e});const c=u.get("te-form-accuracy",{});c[t.rule]||(c[t.rule]={attempts:0,correct:0}),c[t.rule].attempts+=1,e&&(c[t.rule].correct+=1),u.set("te-form-accuracy",c),m(s)}),document.getElementById("te-input")?.addEventListener("keydown",a=>{a.key==="Enter"&&document.getElementById("te-check")?.click()}),document.getElementById("te-input")?.focus(),document.getElementById("te-next")?.addEventListener("click",()=>{r.feedback=null,r.idx+=1,r.idx>=o?(d="finished",f(s)):m(s)})}function f(s){const o=r.queue.length,t=Math.round(r.score/o*100),n={};for(const e of r.grades)n[e.rule]||(n[e.rule]={attempts:0,correct:0}),n[e.rule].attempts+=1,e.correct&&(n[e.rule].correct+=1);const a=Object.entries(n).map(([e,c])=>{const i=Math.round(c.correct/c.attempts*100);return`<li><span>${l(e)}</span> <span class="muted">${c.correct}/${c.attempts} (${i}%)</span></li>`}).join("");s.innerHTML=`
    <div class="te-finished">
      <h2>\u3066-form drill complete</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${r.score}/${o}</div><div class="stat-label">Score</div></div>
        <div class="stat-card ${t>=80?"mastered":"weak"}"><div class="stat-num">${t}%</div><div class="stat-label">Accuracy</div></div>
      </section>
      <h3>Per-rule accuracy</h3>
      <ul class="te-rule-list">${a}</ul>
      <p class="muted small">All-time per-rule accuracy is also shown in the rule table at the top of this page. Lower-accuracy rules are over-sampled in the next drill.</p>
      <div class="test-nav">
        <button id="te-restart" class="btn-primary">Drill again</button>
        <button id="te-back">Back</button>
      </div>
    </div>
  `,document.getElementById("te-restart").addEventListener("click",()=>{r=null,d="teach",h(s)}),document.getElementById("te-back").addEventListener("click",()=>{location.hash="#/learn"})}function l(s){return String(s??"").replace(/[&<>"']/g,o=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[o])}export{w as renderTeForm};
