import*as t from"./storage.js";import{t as e,currentLocale as R}from"./i18n.js";import{gatherSignal as I,recommend as P}from"./pedagogy-recommender.js";import"./branding.js";let v=null,k=null;async function B(){if(v)return v;const s=["grammar","vocab","kanji","reading","listening"].map(o=>fetch(`data/${o}.json`).then(i=>i.ok?i.json():null).catch(()=>null)),[c,d,m,u,g]=await Promise.all(s),l=(o,...i)=>{if(!o)return 0;for(const b of i)if(Array.isArray(o[b]))return o[b].length;return 0};if(v={grammar:l(c,"patterns"),vocab:l(d,"entries"),kanji:l(m,"entries"),reading:l(u,"passages"),listening:l(g,"items")},c&&Array.isArray(c.patterns)){k={};for(const o of c.patterns){if(!o?.id)continue;const i=o.pattern||o.name||o.meaning_en||"";k[o.id]=i?`${o.id} - ${i}`:o.id}}return v}const j=a=>{const s=R()==="hi"?"hi-IN":"en-US";return Intl.NumberFormat(s).format(a||0)};function F(a){const s=t.getHistory(),c=t.getKnownKanji?t.getKnownKanji():{},d=t.getKnownVocab?t.getKnownVocab():{},m=t.getResults(),u=Object.values(s).filter(y=>y&&(y.isMastered||y.isManuallyKnown)).length,g=Object.keys(d).length,l=Object.keys(c).length,o=t.getCompletedReading?t.getCompletedReading():{},i=t.getCompletedListening?t.getCompletedListening():{},b=Object.keys(o).length,$=Object.keys(i).length,h=m.length?m[m.length-1]:null;return{grammar:{done:u,total:a.grammar},vocab:{done:g,total:a.vocab},kanji:{done:l,total:a.kanji},reading:{done:b,total:a.reading},listening:{done:$,total:a.listening},mockTest:h?{done:h.correct,total:h.total,percent:h.percent}:{done:0,total:0,percent:null,notAttempted:!0}}}function G(a){const s=(c,d)=>{const m=e(`home.${c}`);return typeof m=="string"&&m.includes("${n}")?m.replace("${n}",j(d)):m};return[{idx:"01",id:"grammar",title:e("home.card_grammar_title"),count:s("card_grammar_count",a.grammar),desc:e("home.card_grammar_desc"),href:"#/learn/grammar",action:e("home.card_grammar_action")},{idx:"02",id:"vocab",title:e("home.card_vocab_title"),count:s("card_vocab_count",a.vocab),desc:e("home.card_vocab_desc"),href:"#/learn/vocab",action:e("home.card_vocab_action")},{idx:"03",id:"kanji",title:e("home.card_kanji_title"),count:s("card_kanji_count",a.kanji),desc:e("home.card_kanji_desc"),href:"#/kanji",action:e("home.card_kanji_action")},{idx:"04",id:"reading",title:e("home.card_reading_title"),count:s("card_reading_count",a.reading),desc:e("home.card_reading_desc"),href:"#/reading",action:e("home.card_reading_action")},{idx:"05",id:"listening",title:e("home.card_listening_title"),count:s("card_listening_count",a.listening),desc:e("home.card_listening_desc"),href:"#/listening",action:e("home.card_listening_action")},{idx:"06",id:"test",title:e("home.card_test_title"),count:e("home.card_test_count"),desc:e("home.card_test_desc"),href:"#/test",action:e("home.card_test_action")}]}function H(){return[{text:e("home.study_step_grammar"),href:"#/learn/grammar"},{text:e("home.study_step_vocab"),href:"#/learn/vocab"},{text:e("home.study_step_kanji"),href:"#/kanji"},{text:e("home.study_step_drill"),href:"#/drill"},{text:e("home.study_step_reading"),href:"#/reading"},{text:e("home.study_step_listening"),href:"#/listening"},{text:e("home.study_step_test"),href:"#/test"},{text:e("home.study_step_review"),href:"#/review"},{text:e("home.study_step_authentic"),href:"#/authentic"}]}function V(a){return`
    <a class="syllabus-card" href="${a.href}" data-section="${a.id}">
      <p class="syllabus-card-index" aria-hidden="true">${a.idx}</p>
      <h3 class="syllabus-card-title">${a.title}</h3>
      <p class="syllabus-card-count">${r(a.count)}</p>
      <p class="syllabus-card-desc">${r(a.desc)}</p>
      <span class="syllabus-card-action">${r(a.action)} <span aria-hidden="true">\u2192</span></span>
    </a>
  `}function f(a,s){if(s.notAttempted)return`
      <li class="progress-row">
        <span class="progress-label">${r(a)}</span>
        <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:0%"></span></span>
        <span class="progress-value">${r(e("home.progress_not_attempted"))}</span>
      </li>
    `;const c=s.total>0?Math.min(100,Math.round(s.done/s.total*100)):0,d=a===e("home.progress_label_test")||a==="Mock Test"?`${s.done} / ${s.total} (${s.percent??c}%)`:`${j(s.done)} / ${j(s.total)}`;return`
    <li class="progress-row">
      <span class="progress-label">${r(a)}</span>
      <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:${c}%"></span></span>
      <span class="progress-value">${d}</span>
    </li>
  `}async function J(a){const s=t.getHistory(),c=t.getResults(),d=Object.keys(s).length>0||c.length>0,m=t.getSettings(),u=m.lastLearnId||null,g=await B(),l=F(g),o=G(g),i=t.getStreak?t.getStreak():null,b=(()=>{const n=new Date;return`${n.getFullYear()}-${String(n.getMonth()+1).padStart(2,"0")}-${String(n.getDate()).padStart(2,"0")}`})(),$=d&&i&&i.lastStudyDate===b,h=t.getReviewsToday?t.getReviewsToday():0,y=t.getDailyGoal?t.getDailyGoal():20,C=Math.min(100,Math.round(100*h/y)),p=t.getDueCountsBySkill?t.getDueCountsBySkill():{grammar:t.getDueCount?t.getDueCount():0,vocab:0,kanji:0},x=p.grammar+p.vocab+p.kanji,M=p.vocab>0||p.kanji>0?`<span class="muted small" style="margin-left:6px;">(${p.grammar} grammar \xB7 ${p.vocab} vocab \xB7 ${p.kanji} kanji)</span>`:"",w=t.getReviewForecast?t.getReviewForecast(7):[],D=Math.max(1,...w.map(n=>n.count)),K=k&&k[u]||u,L=d&&u?`<a class="resume-strip" href="#/learn/${encodeURIComponent(u)}">Last session: ${r(K)}.</a>`:"",T=m.showRecommender!==!1;let S="";try{if(d&&T){const n=P(I({corpusCounts:g}));if(n){const _=R(),A=_==="hi"?n.label_hi:n.label_en,O=_==="hi"?n.why_hi:n.why_en;S=`
          <aside class="home-recommend" aria-labelledby="home-recommend-h">
            <h3 id="home-recommend-h" class="home-recommend-title">${r(e("home.recommend_title")||"Recommended next")}</h3>
            <a class="home-recommend-action" href="${r(n.href)}">
              <span class="home-recommend-label"><strong>${r(A)}</strong></span>
              <span class="home-recommend-meta muted small">${r(n.duration)} \xB7 ${r(n.rule_id)}</span>
            </a>
            <p class="home-recommend-why muted small">${r(O)}</p>
          </aside>
        `}}}catch(n){typeof console<"u"&&console.warn("[recommender] suppressed:",n)}a.innerHTML=`
    <section class="home-syllabus">
      <p class="home-up-link">
        <a href="#/levels">\u2190 All JLPT levels</a>
      </p>
      ${L}

      ${d?`
        <div class="syllabus-daily-status">
          <span class="syllabus-daily-streak">Streak: ${i?.current??0} ${(i?.current??0)===1?"day":"days"}</span>
          <a class="syllabus-daily-progress" href="#/review" title="Open today's mixed-skill review queue (grammar + vocab + kanji SRS)">
            <span class="syllabus-daily-progress-label">${e("home.today_label")}: <strong>${h}</strong> / ${y}</span>
            <span class="syllabus-daily-progress-bar" aria-hidden="true">
              <span class="syllabus-daily-progress-fill" style="width:${C}%"></span>
            </span>
          </a>
          ${x>0?`
            <a class="syllabus-daily-due" href="#/review">
              ${e("home.reviews_due",{n:`<strong>${x}</strong>`})}${M}
            </a>
          `:`
            <span class="syllabus-daily-due is-empty">${e("home.no_reviews_due")}</span>
          `}
          <span class="syllabus-daily-today ${$?"is-met":"is-pending"}">
            <span class="syllabus-daily-mark" aria-hidden="true">${$?"\u2713":"\u25CB"}</span>
            <span class="syllabus-daily-text">${$?e("home.practiced_today"):e("home.not_yet_practiced")}</span>
          </span>
        </div>
      `:""}

      ${S}

      <section class="syllabus-overview" aria-label="Syllabus overview">
        <header class="section-label">
          <span class="section-label-text">${r(e("home.syllabus_section_label"))}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <div class="syllabus-grid">
          ${o.map(V).join("")}
        </div>
      </section>

      <section class="syllabus-study-order" aria-label="Recommended study order">
        <header class="section-label">
          <span class="section-label-text">${r(e("home.study_order_section_label"))}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ol class="study-order-list">
          ${H().map((n,_)=>`
            <li class="study-order-item">
              <a class="study-order-link" href="${n.href}">
                <span class="study-order-num" aria-hidden="true">${String(_+1).padStart(2,"0")}</span>
                <span class="study-order-text">${r(n.text)}</span>
              </a>
            </li>
          `).join("")}
        </ol>
      </section>

      <section class="syllabus-progress" aria-label="Progress overview">
        <header class="section-label">
          <span class="section-label-text">${r(e("home.progress_section_label"))}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ul class="progress-list">
          ${f(e("home.progress_label_grammar"),l.grammar)}
          ${f(e("home.progress_label_vocab"),l.vocab)}
          ${f(e("home.progress_label_kanji"),l.kanji)}
          ${f(e("home.progress_label_reading"),l.reading)}
          ${f(e("home.progress_label_listening"),l.listening)}
          ${f(e("home.progress_label_test"),l.mockTest)}
        </ul>
      </section>

      ${d&&w.length?`
        <!-- IMP-036 (audit round-3): 7-day review forecast.
             Aggregates FSRS-4 nextDue dates from grammar + vocab + kanji
             histories so the learner sees "tomorrow I'll have 8 reviews;
             Wednesday I'll have 25 - better stay on top of it". -->
        <section class="syllabus-forecast" aria-label="Review forecast">
          <header class="section-label">
            <span class="section-label-text">${e("home.forecast_label")}</span>
            <span class="section-label-rule" aria-hidden="true"></span>
          </header>
          <ol class="forecast-bar-chart">
            ${w.map(n=>{const _=n.count===0?4:Math.max(8,Math.round(56*n.count/D));return`
                <li class="forecast-bar">
                  <span class="forecast-bar-count">${n.count}</span>
                  <span class="forecast-bar-track" aria-hidden="true">
                    <span class="forecast-bar-fill" style="height:${_}px"></span>
                  </span>
                  <span class="forecast-bar-label muted small">${r(n.label)}</span>
                </li>
              `}).join("")}
          </ol>
          <p class="muted small" style="margin-top:6px;">
            <a href="#/missed">Browse wrong-answer history \u2192</a>
          </p>
        </section>
      `:""}

      <section class="syllabus-action" aria-label="Where to start">
        <p class="syllabus-action-prompt">${r(e("home.action_prompt"))}</p>
        <div class="syllabus-action-buttons">
          <a class="btn-action btn-action-primary" href="#/diagnostic">${r(e("home.action_placement"))}</a>
          <a class="btn-action btn-action-secondary" href="#/learn/grammar">${r(e("home.action_start_grammar"))}</a>
        </div>
      </section>
    </section>
  `}function r(a){return String(a??"").replace(/[&<>"']/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[s])}export{J as renderHome};
