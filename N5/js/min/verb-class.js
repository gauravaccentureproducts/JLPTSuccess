import"./normalize.js";import*as g from"./storage.js";const h=[{v:"\u306E\u3080",g:1,en:"drink"},{v:"\u304B\u3046",g:1,en:"buy"},{v:"\u3044\u304F",g:1,en:"go (irregular \u305F-form)"},{v:"\u3088\u3080",g:1,en:"read"},{v:"\u306F\u306A\u3059",g:1,en:"speak"},{v:"\u304B\u304F",g:1,en:"write"},{v:"\u3042\u3046",g:1,en:"meet"},{v:"\u307E\u3064",g:1,en:"wait"},{v:"\u3068\u308B",g:1,en:"take"},{v:"\u306E\u308B",g:1,en:"ride"},{v:"\u3046\u308B",g:1,en:"sell"},{v:"\u304A\u308F\u308B",g:1,en:"finish (intransitive)"},{v:"\u3059\u308F\u308B",g:1,en:"sit"},{v:"\u3042\u308B",g:1,en:"exist (inanimate)"},{v:"\u308F\u304B\u308B",g:1,en:"understand"},{v:"\u3042\u3089\u3046",g:1,en:"wash"},{v:"\u304A\u3088\u3050",g:1,en:"swim"},{v:"\u3044\u305D\u3050",g:1,en:"hurry"},{v:"\u305F\u3079\u308B",g:2,en:"eat"},{v:"\u307F\u308B",g:2,en:"see"},{v:"\u304A\u304D\u308B",g:2,en:"wake up / get up"},{v:"\u306D\u308B",g:2,en:"sleep"},{v:"\u304A\u3057\u3048\u308B",g:2,en:"teach"},{v:"\u3042\u3051\u308B",g:2,en:"open (transitive)"},{v:"\u3057\u3081\u308B",g:2,en:"close (transitive)"},{v:"\u304A\u308A\u308B",g:2,en:"get off"},{v:"\u3067\u304D\u308B",g:2,en:"can do"},{v:"\u308F\u3059\u308C\u308B",g:2,en:"forget"},{v:"\u304A\u307C\u3048\u308B",g:2,en:"remember"},{v:"\u304B\u308A\u308B",g:2,en:"borrow"},{v:"\u304B\u3048\u308B",g:1,en:"return / go home",except:!0},{v:"\u306F\u3044\u308B",g:1,en:"enter",except:!0},{v:"\u306F\u3057\u308B",g:1,en:"run",except:!0},{v:"\u3057\u308B",g:1,en:"know",except:!0},{v:"\u304D\u308B",g:1,en:"cut",except:!0},{v:"\u3044\u308B",g:1,en:"need (\u8981\u308B)",except:!0},{v:"\u3057\u3083\u3079\u308B",g:1,en:"chatter / speak",except:!0},{v:"\u3059\u3079\u308B",g:1,en:"slip / slide",except:!0},{v:"\u3059\u308B",g:3,en:"do"},{v:"\u304F\u308B",g:3,en:"come"},{v:"\u3079\u3093\u304D\u3087\u3046\u3059\u308B",g:3,en:"study"},{v:"\u308A\u3087\u3053\u3046\u3059\u308B",g:3,en:"travel"}];let s=null,i="teach";const u=.9,p=25;async function y(t){return i==="drill"&&s?d(t):i==="finished"&&s?b(t):m(t)}function m(t){i="teach";const e=g.get("verb-class-last-attempt",null);t.innerHTML=`
    <h2>Verb groups - classification</h2>
    <p>Japanese verbs split into three groups. Knowing which group a verb belongs to is the prerequisite for every conjugation (\u307E\u3059-form, \u3066-form, plain-past, \u306A\u3044-form, etc.). Classification first, conjugation second.</p>

    <section class="verb-group-section">
      <h3>Group 1 - \u4E94\u6BB5 (u-verbs)</h3>
      <p>Dictionary form ends in any of <code>-\u3046 -\u3064 -\u308B -\u304F -\u3050 -\u3059 -\u306C -\u3076 -\u3080</code>. Conjugation shifts the final vowel: \u306E\u3080 \u2192 \u306E\u307F\u307E\u3059 \u2192 \u306E\u3093\u3067 \u2192 \u306E\u3093\u3060.</p>
      <p class="verb-list" lang="ja">\u306E\u3080\u30FB\u304B\u3046\u30FB\u3044\u304F\u30FB\u3088\u3080\u30FB\u306F\u306A\u3059\u30FB\u304B\u304F\u30FB\u3042\u3046\u30FB\u307E\u3064\u30FB\u3068\u308B\u30FB\u306E\u308B</p>
    </section>

    <section class="verb-group-section">
      <h3>Group 2 - \u4E00\u6BB5 (ru-verbs)</h3>
      <p>Dictionary form ends in <code>-i\u308B</code> or <code>-e\u308B</code>. Conjugation simply drops \u308B: \u305F\u3079\u308B \u2192 \u305F\u3079\u307E\u3059 \u2192 \u305F\u3079\u3066 \u2192 \u305F\u3079\u305F.</p>
      <p class="verb-list" lang="ja">\u305F\u3079\u308B\u30FB\u307F\u308B\u30FB\u304A\u304D\u308B\u30FB\u306D\u308B\u30FB\u304A\u3057\u3048\u308B\u30FB\u3042\u3051\u308B\u30FB\u3057\u3081\u308B\u30FB\u3067\u304D\u308B\u30FB\u308F\u3059\u308C\u308B</p>
    </section>

    <section class="verb-group-section">
      <h3>Group 3 - Irregulars</h3>
      <p>Just two: \u3059\u308B (do) and \u304F\u308B (come). Anything ending in <code>\uFF5E\u3059\u308B</code> like \u3079\u3093\u304D\u3087\u3046\u3059\u308B conjugates like \u3059\u308B.</p>
      <p class="verb-list" lang="ja">\u3059\u308B\u30FB\u304F\u308B\u30FB\u3079\u3093\u304D\u3087\u3046\u3059\u308B\u30FB\u308A\u3087\u3053\u3046\u3059\u308B</p>
    </section>

    <section class="verb-group-section warning-section">
      <h3>The famous Group-1 exceptions</h3>
      <p>These verbs end in <code>-i\u308B</code> or <code>-e\u308B</code> and LOOK like Group 2, but they are actually <strong>Group 1</strong>. Memorize them - the drill below over-samples them deliberately.</p>
      <p class="verb-list" lang="ja">\u304B\u3048\u308B (return)\u30FB\u306F\u3044\u308B (enter)\u30FB\u306F\u3057\u308B (run)\u30FB\u3057\u308B (know)\u30FB\u304D\u308B (cut)\u30FB\u3044\u308B (need)\u30FB\u3057\u3083\u3079\u308B (chatter)\u30FB\u3059\u3079\u308B (slip)</p>
    </section>

    <section class="drill-cta">
      <h3>Drill: classify on sight</h3>
      <p>${p} verbs, mixed groups, with deliberate over-sampling of the exceptions. Pass threshold: ${Math.round(u*100)}%.</p>
      ${e?`<p class="muted small">Last attempt: ${e.score}/${e.total} (${Math.round(e.score/e.total*100)}%) on ${new Date(e.ts).toLocaleDateString()}.</p>`:""}
      <button id="vc-start" class="btn-primary">Start drill</button>
    </section>
  `,document.getElementById("vc-start").addEventListener("click",()=>{s={queue:f(),idx:0,score:0,misses:[]},i="drill",d(t)})}function f(){const t=h.filter(o=>o.except),e=h.filter(o=>!o.except);v(t),v(e);const r=Math.floor(p*.4),n=[];for(;n.length<p;)n.filter(l=>l.except).length<r&&t.length?n.push({...t[Math.floor(Math.random()*t.length)]}):n.push({...e[Math.floor(Math.random()*e.length)]});return v(n),n}function v(t){for(let e=t.length-1;e>0;e--){const r=Math.floor(Math.random()*(e+1));[t[e],t[r]]=[t[r],t[e]]}return t}function d(t){const e=s.queue[s.idx],r=s.queue.length,n=s.feedback;t.innerHTML=`
    <div class="vc-drill">
      <div class="srs-progress">
        <span>Verb classification \xB7 <strong>${s.idx+1}</strong> / <strong>${r}</strong></span>
        <span class="muted small">Score: ${s.score}/${s.idx+0}</span>
      </div>
      <article class="vc-card">
        <p class="vc-prompt">Which group is this verb?</p>
        <p class="vc-verb" lang="ja">${c(e.v)}</p>
        <p class="muted small">${c(e.en)}</p>
        <div class="vc-buttons">
          <button class="vc-btn" data-grp="1" ${n?"disabled":""}>Group 1<br><small>\u4E94\u6BB5 (u-verbs)</small></button>
          <button class="vc-btn" data-grp="2" ${n?"disabled":""}>Group 2<br><small>\u4E00\u6BB5 (ru-verbs)</small></button>
          <button class="vc-btn" data-grp="3" ${n?"disabled":""}>Group 3<br><small>Irregular</small></button>
        </div>
        ${n?`
          <div class="drill-feedback ${n.correct?"correct":"incorrect"}">
            <div class="feedback-headline">${n.correct?"Correct":"Wrong"}</div>
            <p>${c(e.v)} is <strong>Group ${e.g}</strong>${e.except?" (a famous Group-1 exception - looks like Group 2 but isn't)":""}.</p>
            <button id="vc-next" class="btn-primary">${s.idx===r-1?"Finish":"Next"}</button>
          </div>
        `:""}
      </article>
    </div>
  `,t.querySelectorAll(".vc-btn").forEach(o=>{o.addEventListener("click",()=>{const a=parseInt(o.dataset.grp,10)===e.g;a?s.score+=1:s.misses.push(e),s.feedback={correct:a},d(t)})}),document.getElementById("vc-next")?.addEventListener("click",()=>{s.feedback=null,s.idx+=1,s.idx>=r?(i="finished",b(t)):d(t)})}function b(t){const e=s.queue.length,r=s.score,n=Math.round(r/e*100),o=n>=Math.round(u*100);g.set("verb-class-last-attempt",{score:r,total:e,ts:new Date().toISOString(),passed:o});const l={1:[],2:[],3:[]};for(const a of s.misses)l[a.g].push(a);t.innerHTML=`
    <div class="vc-finished">
      <h2>Drill complete</h2>
      <section class="srs-summary-stats">
        <div class="stat-card mastered"><div class="stat-num">${r}/${e}</div><div class="stat-label">Score</div></div>
        <div class="stat-card ${o?"mastered":"weak"}"><div class="stat-num">${n}%</div><div class="stat-label">${o?"PASSED":"Try again"}</div></div>
      </section>
      ${o?"<p>You can confidently classify N5 verbs. Time to drill conjugation (te-form, \u307E\u3059-form, etc.).</p>":`<p>Aim for ${Math.round(u*100)}%. The Group-1 exceptions are usually the trip-up - re-read the warning section above.</p>`}
      ${s.misses.length>0?`
        <h3>Missed</h3>
        <ul class="vc-misses">
          ${s.misses.map(a=>`<li><span lang="ja">${c(a.v)}</span> <span class="muted small">(${c(a.en)}) - Group ${a.g}${a.except?" [exception]":""}</span></li>`).join("")}
        </ul>
      `:""}
      <div class="test-nav">
        <button id="vc-restart" class="btn-primary">Try again</button>
        <button id="vc-back">Back</button>
      </div>
    </div>
  `,document.getElementById("vc-restart").addEventListener("click",()=>{s=null,i="teach",m(t)}),document.getElementById("vc-back").addEventListener("click",()=>{location.hash="#/learn"})}function c(t){return String(t??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{y as renderVerbClass};
