import{renderJa as p}from"./furigana.js";const c=[{key:"this",label_en:"this (near speaker)",kana:"\u3053-"},{key:"that_l",label_en:"that (near listener)",kana:"\u305D-"},{key:"that_far",label_en:"that (far from both)",kana:"\u3042-"},{key:"which",label_en:"which / what",kana:"\u3069-"}],a=[{key:"pronoun",label_en:"Pronoun (object)",cell_en:"this one",forms:["\u3053\u308C","\u305D\u308C","\u3042\u308C","\u3069\u308C"]},{key:"adjective",label_en:"Adjective + Noun",cell_en:"this + N",forms:["\u3053\u306E","\u305D\u306E","\u3042\u306E","\u3069\u306E"]},{key:"place",label_en:"Location",cell_en:"here / there / where",forms:["\u3053\u3053","\u305D\u3053","\u3042\u305D\u3053","\u3069\u3053"]},{key:"polite",label_en:"Polite (direction / option)",cell_en:"this way / which way",forms:["\u3053\u3061\u3089","\u305D\u3061\u3089","\u3042\u3061\u3089","\u3069\u3061\u3089"]}];let o=null;async function k(e){e.innerHTML=`
    <h2>Demonstratives (this / that / which)</h2>
    <p>Japanese demonstratives form a regular 4\xD74 grid. The first column lists pronouns (standalone), the second adjectives (always followed by a noun), the third locations, and the fourth the polite directions/options.</p>

    ${b()}
    ${f()}
    ${d()}
  `,u(e)}function b(){return`
    <section class="kosoado-proximity">
      <h3>Proximity</h3>
      <div class="proximity-diagram">
        <div class="prox-row">
          <div class="prox-bubble speaker">SPEAKER<br><small>\u3053-</small></div>
          <div class="prox-arrow">\u2194</div>
          <div class="prox-bubble listener">LISTENER<br><small>\u305D-</small></div>
          <div class="prox-arrow long">\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500</div>
          <div class="prox-bubble far">FAR FROM BOTH<br><small>\u3042-</small></div>
        </div>
        <div class="prox-question">QUESTION (anywhere) <strong>\u3069-</strong></div>
      </div>
      <p class="muted small">\u3053- = near speaker, \u305D- = near listener, \u3042- = far from both, \u3069- = question.</p>
    </section>
  `}function f(){let e=`
    <section class="kosoado-grid-section">
      <h3>Grid</h3>
      <table class="kosoado-grid">
        <thead>
          <tr>
            <th>Row \u2192<br>\u2193 Column</th>
            ${a.map(t=>`<th>${r(t.label_en)}<br><small>${r(t.cell_en)}</small></th>`).join("")}
          </tr>
        </thead>
        <tbody>
  `;return c.forEach((t,n)=>{e+=`<tr><th>${r(t.label_en)}<br><small>${r(t.kana)}</small></th>`,a.forEach(s=>{e+=`<td>${p(s.forms[n])}</td>`}),e+="</tr>"}),e+="</tbody></table></section>",e}function d(){if(!o)return`
      <section class="kosoado-drill">
        <h3>Quick drill</h3>
        <p>Click "Start" to be asked random row+column combinations. Type the form (kana).</p>
        <button id="kosoado-start" class="btn-primary">Start drill</button>
      </section>
    `;const{question:e,userAnswer:t,feedback:n,score:s,total:l}=o;return`
    <section class="kosoado-drill">
      <h3>Quick drill <span class="muted small">(${s} / ${l})</span></h3>
      <div class="drill-question">
        <p>Give the form for <strong>${r(e.row.label_en)}</strong> \xD7 <strong>${r(e.col.label_en)}</strong>:</p>
        <input type="text" id="kosoado-input" class="text-input" lang="ja"
               autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"
               placeholder="Type kana or romaji..." value="${r(t||"")}"
               ${n?"disabled":""}>
      </div>
      ${n?`
        <div class="drill-feedback ${n.correct?"correct":"incorrect"}">
          <div class="feedback-headline">${n.correct?"Correct":"Wrong"}</div>
          <p>Answer: <strong lang="ja">${r(e.expected)}</strong></p>
        </div>
        <button id="kosoado-next" class="btn-primary">Next</button>
      `:`
        <button id="kosoado-check" class="btn-primary">Check</button>
      `}
      <button id="kosoado-stop" style="margin-left: 8px">End drill</button>
    </section>
  `}function u(e){const t=document.getElementById("kosoado-start");if(t){t.addEventListener("click",()=>{o={score:0,total:0},h(),i(e)});return}const n=document.getElementById("kosoado-stop");n&&n.addEventListener("click",()=>{o=null,i(e)});const s=document.getElementById("kosoado-check");s&&(s.addEventListener("click",()=>{const m=document.getElementById("kosoado-input");y(m.value),i(e)}),document.getElementById("kosoado-input")?.focus());const l=document.getElementById("kosoado-next");l&&l.addEventListener("click",()=>{h(),o.feedback=null,o.userAnswer="",i(e)})}function i(e){const t=e.querySelector(".kosoado-drill");if(!t){e.innerHTML="",k(e);return}t.outerHTML=d(),u(e)}function h(){const e=Math.floor(Math.random()*c.length),t=Math.floor(Math.random()*a.length);o.question={row:c[e],col:a[t],expected:a[t].forms[e]},o.feedback=null,o.userAnswer=""}async function y(e){const{matchesAnswer:t}=await import("./normalize.js"),n=t(e,[o.question.expected]);o.feedback={correct:n},o.total+=1,n&&(o.score+=1),o.userAnswer=e}function r(e){return String(e??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{k as renderKosoado};
