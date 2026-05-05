import*as a from"./storage.js";let v=null,$=null;async function L(){if(v)return v;const e=["grammar","vocab","kanji","reading","listening"].map(t=>fetch(`data/${t}.json`).then(l=>l.ok?l.json():null).catch(()=>null)),[o,d,b,p,c]=await Promise.all(e),n=(t,...l)=>{if(!t)return 0;for(const y of l)if(Array.isArray(t[y]))return t[y].length;return 0};if(v={grammar:n(o,"patterns"),vocab:n(d,"entries"),kanji:n(b,"entries"),reading:n(p,"passages"),listening:n(c,"items")},o&&Array.isArray(o.patterns)){$={};for(const t of o.patterns){if(!t?.id)continue;const l=t.pattern||t.name||t.meaning_en||"";$[t.id]=l?`${t.id} \u2014 ${l}`:t.id}}return v}const i=s=>Intl.NumberFormat("en-US").format(s||0);function P(s){const e=a.getHistory(),o=a.getKnownKanji?a.getKnownKanji():{},d=a.getKnownVocab?a.getKnownVocab():{},b=a.getResults(),p=Object.values(e).filter(m=>m&&(m.isMastered||m.isManuallyKnown)).length,c=Object.keys(d).length,n=Object.keys(o).length,t=a.getCompletedReading?a.getCompletedReading():{},l=a.getCompletedListening?a.getCompletedListening():{},y=Object.keys(t).length,f=Object.keys(l).length,g=b.length?b[b.length-1]:null;return{grammar:{done:p,total:s.grammar},vocab:{done:c,total:s.vocab},kanji:{done:n,total:s.kanji},reading:{done:y,total:s.reading},listening:{done:f,total:s.listening},mockTest:g?{done:g.correct,total:g.total,percent:g.percent}:{done:0,total:0,percent:null,notAttempted:!0}}}function C(s){return[{idx:"01",id:"grammar",title:"Grammar",count:`${i(s.grammar)} patterns`,desc:"Basic sentence structure, particles, verb forms, adjectives, comparison, requests, and common N5 expressions.",href:"#/learn/grammar",action:"Open Grammar Syllabus"},{idx:"02",id:"vocab",title:"Vocabulary",count:`${i(s.vocab)} words`,desc:"Daily life words, time expressions, family, food, school, travel, verbs, adjectives, and common expressions.",href:"#/learn/vocab",action:"Open Vocabulary List"},{idx:"03",id:"kanji",title:"Kanji",count:`${i(s.kanji)} characters`,desc:"Numbers, time, people, school, directions, nature, common verbs, and basic recognition kanji.",href:"#/kanji",action:"Open Kanji List"},{idx:"04",id:"reading",title:"Reading",count:`${i(s.reading)} passages`,desc:"Short notices, simple messages, daily-life paragraphs, and basic comprehension practice.",href:"#/reading",action:"Start Reading Practice"},{idx:"05",id:"listening",title:"Listening",count:`${i(s.listening)} drills`,desc:"Greetings, classroom phrases, daily conversations, time, shopping, directions, and simple Q&A.",href:"#/listening",action:"Start Listening Practice"},{idx:"06",id:"test",title:"Mock Test",count:"15 questions",desc:"Auto-scored mock test with correct answers, explanations, and weak-area review.",href:"#/test",action:"Take Mock Test"}]}const M=[{text:"Learn basic sentence structure and particles",href:"#/learn/grammar"},{text:"Study core vocabulary",href:"#/learn/vocab"},{text:"Learn basic kanji recognition",href:"#/kanji"},{text:"Practice grammar questions",href:"#/drill"},{text:"Practice short reading passages",href:"#/reading"},{text:"Practice listening drills",href:"#/listening"},{text:"Take the mock test",href:"#/test"},{text:"Review weak areas",href:"#/review"}];function N(s){return`
    <a class="syllabus-card" href="${s.href}" data-section="${s.id}">
      <p class="syllabus-card-index" aria-hidden="true">${s.idx}</p>
      <h3 class="syllabus-card-title">${s.title}</h3>
      <p class="syllabus-card-count">${u(s.count)}</p>
      <p class="syllabus-card-desc">${u(s.desc)}</p>
      <span class="syllabus-card-action">${u(s.action)} <span aria-hidden="true">\u2192</span></span>
    </a>
  `}function h(s,e){if(e.notAttempted)return`
      <li class="progress-row">
        <span class="progress-label">${u(s)}</span>
        <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:0%"></span></span>
        <span class="progress-value">Not attempted</span>
      </li>
    `;const o=e.total>0?Math.min(100,Math.round(e.done/e.total*100)):0,d=s==="Mock Test"?`${e.done} / ${e.total} (${e.percent??o}%)`:`${i(e.done)} / ${i(e.total)}`;return`
    <li class="progress-row">
      <span class="progress-label">${u(s)}</span>
      <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:${o}%"></span></span>
      <span class="progress-value">${d}</span>
    </li>
  `}async function I(s){const e=a.getHistory(),o=a.getResults(),d=Object.keys(e).length>0||o.length>0,p=a.getSettings().lastLearnId||null,c=await L(),n=P(c),t=C(c),l=a.getStreak?a.getStreak():null,y=(()=>{const r=new Date;return`${r.getFullYear()}-${String(r.getMonth()+1).padStart(2,"0")}-${String(r.getDate()).padStart(2,"0")}`})(),f=d&&l&&l.lastStudyDate===y,g=a.getReviewsToday?a.getReviewsToday():0,m=a.getDailyGoal?a.getDailyGoal():20,j=Math.min(100,Math.round(100*g/m)),k=a.getDueCount?a.getDueCount():0,w=a.getReviewForecast?a.getReviewForecast(7):[],x=Math.max(1,...w.map(r=>r.count)),R=$&&$[p]||p,T=d&&p?`<a class="resume-strip" href="#/learn/${encodeURIComponent(p)}">Last session: ${u(R)}.</a>`:"";s.innerHTML=`
    <section class="home-syllabus">
      <p class="home-up-link">
        <a href="#/levels">\u2190 All JLPT levels</a>
      </p>
      ${T}

      <header class="syllabus-header">
        <span class="syllabus-watermark" aria-hidden="true">\u4E94</span>
        <h1 class="syllabus-title">JLPT N5 Syllabus</h1>
        <p class="syllabus-subtitle">Study grammar, vocabulary, kanji, reading, and listening in a structured order.</p>
        <!-- ISSUE-027 / IMP-048 (audit round-4): privacy / niche-N2
             trust band. Surfaces the most-defensible competitive claim
             on first paint. Each item links to its proof:
               "Open source" -> /LICENSE
               "Works offline" -> install banner / docs
               "Privacy" -> PRIVACY.md -->
        <p class="syllabus-trust-band" aria-label="Trust signals">
          <span class="trust-pill"><span aria-hidden="true">\u25CF</span> No login</span>
          <span class="trust-pill"><span aria-hidden="true">\u25CF</span> No tracking</span>
          <a class="trust-pill" href="./" data-trust-install title="Install for offline use"><span aria-hidden="true">\u25CF</span> Works offline</a>
          <!-- ISSUE-040 (audit round-5): the GitHub blob URL stays correct
               on every deploy (canonical / fork / localhost) because the
               source-of-truth always lives in the upstream repo. The
               relative ../../LICENSE only resolved correctly on the
               canonical /JLPTSuccess/N5/ deploy. -->
          <a class="trust-pill" href="https://github.com/gauravaccentureproducts/JLPTSuccess/blob/master/LICENSE" target="_blank" rel="noopener" title="MIT licensed source \xB7 CC BY-SA content"><span aria-hidden="true">\u25CF</span> Open source</a>
          <a class="trust-pill" href="PRIVACY.md" target="_blank" rel="noopener" title="No data leaves your device"><span aria-hidden="true">\u25CF</span> 100% on-device</a>
          <!-- ISSUE-037 + IMP-058 (audit round-5): price differentiator pill.
               Bunpro / WaniKani / Renshuu all charge; this pill makes the
               niche-N2 claim complete. -->
          <span class="trust-pill" title="Free, forever. No ads, no paywall, no upsell."><span aria-hidden="true">\u25CF</span> Free \xB7 No ads \xB7 No paywall</span>
        </p>
        <ul class="syllabus-stat-pills" aria-label="Corpus size">
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${i(c.grammar)}</span><span class="syllabus-stat-lbl">grammar patterns</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${i(c.vocab)}</span><span class="syllabus-stat-lbl">vocab words</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${i(c.kanji)}</span><span class="syllabus-stat-lbl">kanji</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${i(c.reading)}</span><span class="syllabus-stat-lbl">reading passages</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${i(c.listening)}</span><span class="syllabus-stat-lbl">listening drills</span></li>
        </ul>
        ${d?`
          <div class="syllabus-daily-status">
            <span class="syllabus-daily-streak">Streak: ${l?.current??0} ${(l?.current??0)===1?"day":"days"}</span>
            <a class="syllabus-daily-progress" href="#/review" title="Open today's review queue">
              <span class="syllabus-daily-progress-label">Today: <strong>${g}</strong> / ${m}</span>
              <span class="syllabus-daily-progress-bar" aria-hidden="true">
                <span class="syllabus-daily-progress-fill" style="width:${j}%"></span>
              </span>
            </a>
            ${k>0?`
              <a class="syllabus-daily-due" href="#/review">
                <strong>${k}</strong> review${k===1?"":"s"} due
              </a>
            `:`
              <span class="syllabus-daily-due is-empty">No reviews due</span>
            `}
            <span class="syllabus-daily-today ${f?"is-met":"is-pending"}">
              <span class="syllabus-daily-mark" aria-hidden="true">${f?"\u2713":"\u25CB"}</span>
              <span class="syllabus-daily-text">${f?"Practiced today":"Not yet practiced today"}</span>
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
          ${t.map(N).join("")}
        </div>
      </section>

      <section class="syllabus-study-order" aria-label="Recommended study order">
        <header class="section-label">
          <span class="section-label-text">Recommended Study Order</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ol class="study-order-list">
          ${M.map((r,S)=>`
            <li class="study-order-item">
              <a class="study-order-link" href="${r.href}">
                <span class="study-order-num" aria-hidden="true">${String(S+1).padStart(2,"0")}</span>
                <span class="study-order-text">${u(r.text)}</span>
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
          ${h("Grammar",n.grammar)}
          ${h("Vocabulary",n.vocab)}
          ${h("Kanji",n.kanji)}
          ${h("Reading",n.reading)}
          ${h("Listening",n.listening)}
          ${h("Mock Test",n.mockTest)}
        </ul>
      </section>

      ${d&&w.length?`
        <!-- IMP-036 (audit round-3): 7-day review forecast.
             Aggregates FSRS-4 nextDue dates from grammar + vocab + kanji
             histories so the learner sees "tomorrow I'll have 8 reviews;
             Wednesday I'll have 25 \u2014 better stay on top of it". -->
        <section class="syllabus-forecast" aria-label="Review forecast">
          <header class="section-label">
            <span class="section-label-text">Review forecast (7 days)</span>
            <span class="section-label-rule" aria-hidden="true"></span>
          </header>
          <ol class="forecast-bar-chart">
            ${w.map(r=>{const S=r.count===0?4:Math.max(8,Math.round(56*r.count/x));return`
                <li class="forecast-bar">
                  <span class="forecast-bar-count">${r.count}</span>
                  <span class="forecast-bar-track" aria-hidden="true">
                    <span class="forecast-bar-fill" style="height:${S}px"></span>
                  </span>
                  <span class="forecast-bar-label muted small">${u(r.label)}</span>
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
  `}function u(s){return String(s??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{I as renderHome};
