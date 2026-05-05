import*as a from"./storage.js";import{t as r}from"./i18n.js";let v=null,w=null;async function T(){if(v)return v;const e=["grammar","vocab","kanji","reading","listening"].map(t=>fetch(`data/${t}.json`).then(l=>l.ok?l.json():null).catch(()=>null)),[c,p,m,u,d]=await Promise.all(e),n=(t,...l)=>{if(!t)return 0;for(const h of l)if(Array.isArray(t[h]))return t[h].length;return 0};if(v={grammar:n(c,"patterns"),vocab:n(p,"entries"),kanji:n(m,"entries"),reading:n(u,"passages"),listening:n(d,"items")},c&&Array.isArray(c.patterns)){w={};for(const t of c.patterns){if(!t?.id)continue;const l=t.pattern||t.name||t.meaning_en||"";w[t.id]=l?`${t.id} \u2014 ${l}`:t.id}}return v}const o=s=>Intl.NumberFormat("en-US").format(s||0);function C(s){const e=a.getHistory(),c=a.getKnownKanji?a.getKnownKanji():{},p=a.getKnownVocab?a.getKnownVocab():{},m=a.getResults(),u=Object.values(e).filter(y=>y&&(y.isMastered||y.isManuallyKnown)).length,d=Object.keys(p).length,n=Object.keys(c).length,t=a.getCompletedReading?a.getCompletedReading():{},l=a.getCompletedListening?a.getCompletedListening():{},h=Object.keys(t).length,$=Object.keys(l).length,b=m.length?m[m.length-1]:null;return{grammar:{done:u,total:s.grammar},vocab:{done:d,total:s.vocab},kanji:{done:n,total:s.kanji},reading:{done:h,total:s.reading},listening:{done:$,total:s.listening},mockTest:b?{done:b.correct,total:b.total,percent:b.percent}:{done:0,total:0,percent:null,notAttempted:!0}}}function L(s){return[{idx:"01",id:"grammar",title:"Grammar",count:`${o(s.grammar)} patterns`,desc:"Basic sentence structure, particles, verb forms, adjectives, comparison, requests, and common N5 expressions.",href:"#/learn/grammar",action:"Open Grammar Syllabus"},{idx:"02",id:"vocab",title:"Vocabulary",count:`${o(s.vocab)} words`,desc:"Daily life words, time expressions, family, food, school, travel, verbs, adjectives, and common expressions.",href:"#/learn/vocab",action:"Open Vocabulary List"},{idx:"03",id:"kanji",title:"Kanji",count:`${o(s.kanji)} characters`,desc:"Numbers, time, people, school, directions, nature, common verbs, and basic recognition kanji.",href:"#/kanji",action:"Open Kanji List"},{idx:"04",id:"reading",title:"Reading",count:`${o(s.reading)} passages`,desc:"Short notices, simple messages, daily-life paragraphs, and basic comprehension practice.",href:"#/reading",action:"Start Reading Practice"},{idx:"05",id:"listening",title:"Listening",count:`${o(s.listening)} drills`,desc:"Greetings, classroom phrases, daily conversations, time, shopping, directions, and simple Q&A.",href:"#/listening",action:"Start Listening Practice"},{idx:"06",id:"test",title:"Mock Test",count:"15 questions",desc:"Auto-scored mock test with correct answers, explanations, and weak-area review.",href:"#/test",action:"Take Mock Test"}]}const P=[{text:"Learn basic sentence structure and particles",href:"#/learn/grammar"},{text:"Study core vocabulary",href:"#/learn/vocab"},{text:"Learn basic kanji recognition",href:"#/kanji"},{text:"Practice grammar questions",href:"#/drill"},{text:"Practice short reading passages",href:"#/reading"},{text:"Practice listening drills",href:"#/listening"},{text:"Take the mock test",href:"#/test"},{text:"Review weak areas",href:"#/review"}];function K(s){return`
    <a class="syllabus-card" href="${s.href}" data-section="${s.id}">
      <p class="syllabus-card-index" aria-hidden="true">${s.idx}</p>
      <h3 class="syllabus-card-title">${s.title}</h3>
      <p class="syllabus-card-count">${g(s.count)}</p>
      <p class="syllabus-card-desc">${g(s.desc)}</p>
      <span class="syllabus-card-action">${g(s.action)} <span aria-hidden="true">\u2192</span></span>
    </a>
  `}function f(s,e){if(e.notAttempted)return`
      <li class="progress-row">
        <span class="progress-label">${g(s)}</span>
        <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:0%"></span></span>
        <span class="progress-value">Not attempted</span>
      </li>
    `;const c=e.total>0?Math.min(100,Math.round(e.done/e.total*100)):0,p=s==="Mock Test"?`${e.done} / ${e.total} (${e.percent??c}%)`:`${o(e.done)} / ${o(e.total)}`;return`
    <li class="progress-row">
      <span class="progress-label">${g(s)}</span>
      <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:${c}%"></span></span>
      <span class="progress-value">${p}</span>
    </li>
  `}async function I(s){const e=a.getHistory(),c=a.getResults(),p=Object.keys(e).length>0||c.length>0,u=a.getSettings().lastLearnId||null,d=await T(),n=C(d),t=L(d),l=a.getStreak?a.getStreak():null,h=(()=>{const i=new Date;return`${i.getFullYear()}-${String(i.getMonth()+1).padStart(2,"0")}-${String(i.getDate()).padStart(2,"0")}`})(),$=p&&l&&l.lastStudyDate===h,b=a.getReviewsToday?a.getReviewsToday():0,y=a.getDailyGoal?a.getDailyGoal():20,S=Math.min(100,Math.round(100*b/y)),x=a.getDueCount?a.getDueCount():0,k=a.getReviewForecast?a.getReviewForecast(7):[],R=Math.max(1,...k.map(i=>i.count)),_=w&&w[u]||u,M=p&&u?`<a class="resume-strip" href="#/learn/${encodeURIComponent(u)}">Last session: ${g(_)}.</a>`:"";s.innerHTML=`
    <section class="home-syllabus">
      <p class="home-up-link">
        <a href="#/levels">\u2190 All JLPT levels</a>
      </p>
      ${M}

      <header class="syllabus-header">
        <span class="syllabus-watermark" aria-hidden="true">\u4E94</span>
        <h1 class="syllabus-title">${r("home.syllabus_title")}</h1>
        <p class="syllabus-subtitle">${r("home.syllabus_subtitle")}</p>
        <!-- ISSUE-027 / IMP-048 (audit round-4): privacy / niche-N2
             trust band. Surfaces the most-defensible competitive claim
             on first paint. 2026-05-05: trust pills now use t() so
             they translate when the locale chip switches. -->
        <p class="syllabus-trust-band" aria-label="Trust signals">
          <span class="trust-pill"><span aria-hidden="true">\u25CF</span> ${r("trust.no_login")}</span>
          <span class="trust-pill"><span aria-hidden="true">\u25CF</span> ${r("trust.no_tracking")}</span>
          <a class="trust-pill" href="./" data-trust-install title="Install for offline use"><span aria-hidden="true">\u25CF</span> ${r("trust.works_offline")}</a>
          <a class="trust-pill" href="https://github.com/gauravaccentureproducts/JLPTSuccess/blob/master/LICENSE" target="_blank" rel="noopener" title="MIT licensed source \xB7 CC BY-SA content"><span aria-hidden="true">\u25CF</span> ${r("trust.open_source")}</a>
          <a class="trust-pill" href="PRIVACY.md" target="_blank" rel="noopener" title="No data leaves your device"><span aria-hidden="true">\u25CF</span> ${r("trust.on_device")}</a>
          <span class="trust-pill" title="Free, forever. No ads, no paywall, no upsell."><span aria-hidden="true">\u25CF</span> ${r("trust.free_no_paywall")}</span>
        </p>
        <ul class="syllabus-stat-pills" aria-label="Corpus size">
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(d.grammar)}</span><span class="syllabus-stat-lbl">grammar patterns</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(d.vocab)}</span><span class="syllabus-stat-lbl">vocab words</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(d.kanji)}</span><span class="syllabus-stat-lbl">kanji</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(d.reading)}</span><span class="syllabus-stat-lbl">reading passages</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(d.listening)}</span><span class="syllabus-stat-lbl">listening drills</span></li>
        </ul>
        ${p?`
          <div class="syllabus-daily-status">
            <span class="syllabus-daily-streak">Streak: ${l?.current??0} ${(l?.current??0)===1?"day":"days"}</span>
            <a class="syllabus-daily-progress" href="#/review" title="Open today's review queue">
              <span class="syllabus-daily-progress-label">${r("home.today_label")}: <strong>${b}</strong> / ${y}</span>
              <span class="syllabus-daily-progress-bar" aria-hidden="true">
                <span class="syllabus-daily-progress-fill" style="width:${S}%"></span>
              </span>
            </a>
            ${x>0?`
              <a class="syllabus-daily-due" href="#/review">
                ${r("home.reviews_due",{n:`<strong>${x}</strong>`})}
              </a>
            `:`
              <span class="syllabus-daily-due is-empty">${r("home.no_reviews_due")}</span>
            `}
            <span class="syllabus-daily-today ${$?"is-met":"is-pending"}">
              <span class="syllabus-daily-mark" aria-hidden="true">${$?"\u2713":"\u25CB"}</span>
              <span class="syllabus-daily-text">${$?r("home.practiced_today"):r("home.not_yet_practiced")}</span>
            </span>
          </div>
        `:""}
      </header>

      <section class="syllabus-overview" aria-label="Syllabus overview">
        <header class="section-label">
          <span class="section-label-text">Syllabus</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <div class="syllabus-grid">
          ${t.map(K).join("")}
        </div>
      </section>

      <section class="syllabus-study-order" aria-label="Recommended study order">
        <header class="section-label">
          <span class="section-label-text">Recommended Study Order</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ol class="study-order-list">
          ${P.map((i,j)=>`
            <li class="study-order-item">
              <a class="study-order-link" href="${i.href}">
                <span class="study-order-num" aria-hidden="true">${String(j+1).padStart(2,"0")}</span>
                <span class="study-order-text">${g(i.text)}</span>
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
          ${f("Grammar",n.grammar)}
          ${f("Vocabulary",n.vocab)}
          ${f("Kanji",n.kanji)}
          ${f("Reading",n.reading)}
          ${f("Listening",n.listening)}
          ${f("Mock Test",n.mockTest)}
        </ul>
      </section>

      ${p&&k.length?`
        <!-- IMP-036 (audit round-3): 7-day review forecast.
             Aggregates FSRS-4 nextDue dates from grammar + vocab + kanji
             histories so the learner sees "tomorrow I'll have 8 reviews;
             Wednesday I'll have 25 \u2014 better stay on top of it". -->
        <section class="syllabus-forecast" aria-label="Review forecast">
          <header class="section-label">
            <span class="section-label-text">${r("home.forecast_label")}</span>
            <span class="section-label-rule" aria-hidden="true"></span>
          </header>
          <ol class="forecast-bar-chart">
            ${k.map(i=>{const j=i.count===0?4:Math.max(8,Math.round(56*i.count/R));return`
                <li class="forecast-bar">
                  <span class="forecast-bar-count">${i.count}</span>
                  <span class="forecast-bar-track" aria-hidden="true">
                    <span class="forecast-bar-fill" style="height:${j}px"></span>
                  </span>
                  <span class="forecast-bar-label muted small">${g(i.label)}</span>
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
  `}function g(s){return String(s??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{I as renderHome};
