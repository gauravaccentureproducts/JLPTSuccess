import*as a from"./storage.js";import{t as h,currentLocale as M}from"./i18n.js";import{gatherSignal as A,recommend as G}from"./pedagogy-recommender.js";import"./branding.js";let w=null,x=null;async function B(){if(w)return w;const t=["grammar","vocab","kanji","reading","listening"].map(n=>fetch(`data/${n}.json`).then(l=>l.ok?l.json():null).catch(()=>null)),[i,c,d,m,p]=await Promise.all(t),r=(n,...l)=>{if(!n)return 0;for(const y of l)if(Array.isArray(n[y]))return n[y].length;return 0};if(w={grammar:r(i,"patterns"),vocab:r(c,"entries"),kanji:r(d,"entries"),reading:r(m,"passages"),listening:r(p,"items")},i&&Array.isArray(i.patterns)){x={};for(const n of i.patterns){if(!n?.id)continue;const l=n.pattern||n.name||n.meaning_en||"";x[n.id]=l?`${n.id} - ${l}`:n.id}}return w}const b=e=>{const t=M()==="hi"?"hi-IN":"en-US";return Intl.NumberFormat(t).format(e||0)};function I(e){const t=a.getHistory(),i=a.getKnownKanji?a.getKnownKanji():{},c=a.getKnownVocab?a.getKnownVocab():{},d=a.getResults(),m=Object.values(t).filter(f=>f&&(f.isMastered||f.isManuallyKnown)).length,p=Object.keys(c).length,r=Object.keys(i).length,n=a.getCompletedReading?a.getCompletedReading():{},l=a.getCompletedListening?a.getCompletedListening():{},y=Object.keys(n).length,k=Object.keys(l).length,g=d.length?d[d.length-1]:null;return{grammar:{done:m,total:e.grammar},vocab:{done:p,total:e.vocab},kanji:{done:r,total:e.kanji},reading:{done:y,total:e.reading},listening:{done:k,total:e.listening},mockTest:g?{done:g.correct,total:g.total,percent:g.percent}:{done:0,total:0,percent:null,notAttempted:!0}}}function N(e){return[{idx:"01",id:"grammar",title:"Grammar",count:`${b(e.grammar)} patterns`,desc:"Basic sentence structure, particles, verb forms, adjectives, comparison, requests, and common N5 expressions.",href:"#/learn/grammar",action:"Open Grammar Syllabus"},{idx:"02",id:"vocab",title:"Vocabulary",count:`${b(e.vocab)} words`,desc:"Daily life words, time expressions, family, food, school, travel, verbs, adjectives, and common expressions.",href:"#/learn/vocab",action:"Open Vocabulary List"},{idx:"03",id:"kanji",title:"Kanji",count:`${b(e.kanji)} characters`,desc:"Numbers, time, people, school, directions, nature, common verbs, and basic recognition kanji.",href:"#/kanji",action:"Open Kanji List"},{idx:"04",id:"reading",title:"Reading",count:`${b(e.reading)} passages`,desc:"Short notices, simple messages, daily-life paragraphs, and basic comprehension practice.",href:"#/reading",action:"Start Reading Practice"},{idx:"05",id:"listening",title:"Listening",count:`${b(e.listening)} drills`,desc:"Greetings, classroom phrases, daily conversations, time, shopping, directions, and simple Q&A.",href:"#/listening",action:"Start Listening Practice"},{idx:"06",id:"test",title:"Mock Test",count:"15 questions",desc:"Auto-scored mock test with correct answers, explanations, and weak-area review.",href:"#/test",action:"Take Mock Test"}]}const V=[{text:"Learn basic sentence structure and particles",href:"#/learn/grammar"},{text:"Study core vocabulary",href:"#/learn/vocab"},{text:"Learn basic kanji recognition",href:"#/kanji"},{text:"Practice grammar questions",href:"#/drill"},{text:"Practice short reading passages",href:"#/reading"},{text:"Practice listening drills",href:"#/listening"},{text:"Take the mock test",href:"#/test"},{text:"Mixed drill: grammar + vocab + kanji SRS",href:"#/review"},{text:"Real-world Japanese (signs, menus, transit)",href:"#/authentic"}];function q(e){return`
    <a class="syllabus-card" href="${e.href}" data-section="${e.id}">
      <p class="syllabus-card-index" aria-hidden="true">${e.idx}</p>
      <h3 class="syllabus-card-title">${e.title}</h3>
      <p class="syllabus-card-count">${o(e.count)}</p>
      <p class="syllabus-card-desc">${o(e.desc)}</p>
      <span class="syllabus-card-action">${o(e.action)} <span aria-hidden="true">\u2192</span></span>
    </a>
  `}function v(e,t){if(t.notAttempted)return`
      <li class="progress-row">
        <span class="progress-label">${o(e)}</span>
        <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:0%"></span></span>
        <span class="progress-value">Not attempted</span>
      </li>
    `;const i=t.total>0?Math.min(100,Math.round(t.done/t.total*100)):0,c=e==="Mock Test"?`${t.done} / ${t.total} (${t.percent??i}%)`:`${b(t.done)} / ${b(t.total)}`;return`
    <li class="progress-row">
      <span class="progress-label">${o(e)}</span>
      <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:${i}%"></span></span>
      <span class="progress-value">${c}</span>
    </li>
  `}async function W(e){const t=a.getHistory(),i=a.getResults(),c=Object.keys(t).length>0||i.length>0,d=a.getSettings(),m=d.lastLearnId||null,p=await B(),r=I(p),n=N(p),l=a.getStreak?a.getStreak():null,y=(()=>{const s=new Date;return`${s.getFullYear()}-${String(s.getMonth()+1).padStart(2,"0")}-${String(s.getDate()).padStart(2,"0")}`})(),k=c&&l&&l.lastStudyDate===y,g=a.getReviewsToday?a.getReviewsToday():0,f=a.getDailyGoal?a.getDailyGoal():20,C=Math.min(100,Math.round(100*g/f)),u=a.getDueCountsBySkill?a.getDueCountsBySkill():{grammar:a.getDueCount?a.getDueCount():0,vocab:0,kanji:0},S=u.grammar+u.vocab+u.kanji,L=u.vocab>0||u.kanji>0?`<span class="muted small" style="margin-left:6px;">(${u.grammar} grammar \xB7 ${u.vocab} vocab \xB7 ${u.kanji} kanji)</span>`:"",j=a.getReviewForecast?a.getReviewForecast(7):[],T=Math.max(1,...j.map(s=>s.count)),_=x&&x[m]||m,D=c&&m?`<a class="resume-strip" href="#/learn/${encodeURIComponent(m)}">Last session: ${o(_)}.</a>`:"",K=d.showRecommender!==!1;let R="";try{if(c&&K){const s=G(A({corpusCounts:p}));if(s){const $=M(),P=$==="hi"?s.label_hi:s.label_en,O=$==="hi"?s.why_hi:s.why_en;R=`
          <aside class="home-recommend" aria-labelledby="home-recommend-h">
            <h3 id="home-recommend-h" class="home-recommend-title">${o(h("home.recommend_title")||"Recommended next")}</h3>
            <a class="home-recommend-action" href="${o(s.href)}">
              <span class="home-recommend-label"><strong>${o(P)}</strong></span>
              <span class="home-recommend-meta muted small">${o(s.duration)} \xB7 ${o(s.rule_id)}</span>
            </a>
            <p class="home-recommend-why muted small">${o(O)}</p>
          </aside>
        `}}}catch(s){typeof console<"u"&&console.warn("[recommender] suppressed:",s)}e.innerHTML=`
    <section class="home-syllabus">
      <p class="home-up-link">
        <a href="#/levels">\u2190 All JLPT levels</a>
      </p>
      ${D}

      ${c?`
        <div class="syllabus-daily-status">
          <span class="syllabus-daily-streak">Streak: ${l?.current??0} ${(l?.current??0)===1?"day":"days"}</span>
          <a class="syllabus-daily-progress" href="#/review" title="Open today's mixed-skill review queue (grammar + vocab + kanji SRS)">
            <span class="syllabus-daily-progress-label">${h("home.today_label")}: <strong>${g}</strong> / ${f}</span>
            <span class="syllabus-daily-progress-bar" aria-hidden="true">
              <span class="syllabus-daily-progress-fill" style="width:${C}%"></span>
            </span>
          </a>
          ${S>0?`
            <a class="syllabus-daily-due" href="#/review">
              ${h("home.reviews_due",{n:`<strong>${S}</strong>`})}${L}
            </a>
          `:`
            <span class="syllabus-daily-due is-empty">${h("home.no_reviews_due")}</span>
          `}
          <span class="syllabus-daily-today ${k?"is-met":"is-pending"}">
            <span class="syllabus-daily-mark" aria-hidden="true">${k?"\u2713":"\u25CB"}</span>
            <span class="syllabus-daily-text">${k?h("home.practiced_today"):h("home.not_yet_practiced")}</span>
          </span>
        </div>
      `:""}

      ${R}

      <section class="syllabus-overview" aria-label="Syllabus overview">
        <header class="section-label">
          <span class="section-label-text">Syllabus</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <div class="syllabus-grid">
          ${n.map(q).join("")}
        </div>
      </section>

      <section class="syllabus-study-order" aria-label="Recommended study order">
        <header class="section-label">
          <span class="section-label-text">Recommended Study Order</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ol class="study-order-list">
          ${V.map((s,$)=>`
            <li class="study-order-item">
              <a class="study-order-link" href="${s.href}">
                <span class="study-order-num" aria-hidden="true">${String($+1).padStart(2,"0")}</span>
                <span class="study-order-text">${o(s.text)}</span>
              </a>
            </li>
          `).join("")}
        </ol>
      </section>

      <section class="syllabus-progress" aria-label="Progress overview">
        <header class="section-label">
          <span class="section-label-text">Progress</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ul class="progress-list">
          ${v("Grammar",r.grammar)}
          ${v("Vocabulary",r.vocab)}
          ${v("Kanji",r.kanji)}
          ${v("Reading",r.reading)}
          ${v("Listening",r.listening)}
          ${v("Mock Test",r.mockTest)}
        </ul>
      </section>

      ${c&&j.length?`
        <!-- IMP-036 (audit round-3): 7-day review forecast.
             Aggregates FSRS-4 nextDue dates from grammar + vocab + kanji
             histories so the learner sees "tomorrow I'll have 8 reviews;
             Wednesday I'll have 25 - better stay on top of it". -->
        <section class="syllabus-forecast" aria-label="Review forecast">
          <header class="section-label">
            <span class="section-label-text">${h("home.forecast_label")}</span>
            <span class="section-label-rule" aria-hidden="true"></span>
          </header>
          <ol class="forecast-bar-chart">
            ${j.map(s=>{const $=s.count===0?4:Math.max(8,Math.round(56*s.count/T));return`
                <li class="forecast-bar">
                  <span class="forecast-bar-count">${s.count}</span>
                  <span class="forecast-bar-track" aria-hidden="true">
                    <span class="forecast-bar-fill" style="height:${$}px"></span>
                  </span>
                  <span class="forecast-bar-label muted small">${o(s.label)}</span>
                </li>
              `}).join("")}
          </ol>
          <p class="muted small" style="margin-top:6px;">
            <a href="#/missed">Browse wrong-answer history \u2192</a>
          </p>
        </section>
      `:""}

      <section class="syllabus-action" aria-label="Where to start">
        <p class="syllabus-action-prompt">Not sure where to start?</p>
        <div class="syllabus-action-buttons">
          <a class="btn-action btn-action-primary" href="#/diagnostic">Take Placement Check</a>
          <a class="btn-action btn-action-secondary" href="#/learn/grammar">Start with Grammar</a>
        </div>
      </section>
    </section>
  `}function o(e){return String(e??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{W as renderHome};
