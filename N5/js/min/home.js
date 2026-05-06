import*as a from"./storage.js";import{t as i,currentLocale as M}from"./i18n.js";let w=null,j=null;async function A(){if(w)return w;const e=["grammar","vocab","kanji","reading","listening"].map(t=>fetch(`data/${t}.json`).then(r=>r.ok?r.json():null).catch(()=>null)),[c,d,h,g,p]=await Promise.all(e),l=(t,...r)=>{if(!t)return 0;for(const y of r)if(Array.isArray(t[y]))return t[y].length;return 0};if(w={grammar:l(c,"patterns"),vocab:l(d,"entries"),kanji:l(h,"entries"),reading:l(g,"passages"),listening:l(p,"items")},c&&Array.isArray(c.patterns)){j={};for(const t of c.patterns){if(!t?.id)continue;const r=t.pattern||t.name||t.meaning_en||"";j[t.id]=r?`${t.id} - ${r}`:t.id}}return w}const o=s=>{const e=M()==="hi"?"hi-IN":"en-US";return Intl.NumberFormat(e).format(s||0)};function D(s){const e=a.getHistory(),c=a.getKnownKanji?a.getKnownKanji():{},d=a.getKnownVocab?a.getKnownVocab():{},h=a.getResults(),g=Object.values(e).filter(f=>f&&(f.isMastered||f.isManuallyKnown)).length,p=Object.keys(d).length,l=Object.keys(c).length,t=a.getCompletedReading?a.getCompletedReading():{},r=a.getCompletedListening?a.getCompletedListening():{},y=Object.keys(t).length,k=Object.keys(r).length,b=h.length?h[h.length-1]:null;return{grammar:{done:g,total:s.grammar},vocab:{done:p,total:s.vocab},kanji:{done:l,total:s.kanji},reading:{done:y,total:s.reading},listening:{done:k,total:s.listening},mockTest:b?{done:b.correct,total:b.total,percent:b.percent}:{done:0,total:0,percent:null,notAttempted:!0}}}function N(s){return[{idx:"01",id:"grammar",title:"Grammar",count:`${o(s.grammar)} patterns`,desc:"Basic sentence structure, particles, verb forms, adjectives, comparison, requests, and common N5 expressions.",href:"#/learn/grammar",action:"Open Grammar Syllabus"},{idx:"02",id:"vocab",title:"Vocabulary",count:`${o(s.vocab)} words`,desc:"Daily life words, time expressions, family, food, school, travel, verbs, adjectives, and common expressions.",href:"#/learn/vocab",action:"Open Vocabulary List"},{idx:"03",id:"kanji",title:"Kanji",count:`${o(s.kanji)} characters`,desc:"Numbers, time, people, school, directions, nature, common verbs, and basic recognition kanji.",href:"#/kanji",action:"Open Kanji List"},{idx:"04",id:"reading",title:"Reading",count:`${o(s.reading)} passages`,desc:"Short notices, simple messages, daily-life paragraphs, and basic comprehension practice.",href:"#/reading",action:"Start Reading Practice"},{idx:"05",id:"listening",title:"Listening",count:`${o(s.listening)} drills`,desc:"Greetings, classroom phrases, daily conversations, time, shopping, directions, and simple Q&A.",href:"#/listening",action:"Start Listening Practice"},{idx:"06",id:"test",title:"Mock Test",count:"15 questions",desc:"Auto-scored mock test with correct answers, explanations, and weak-area review.",href:"#/test",action:"Take Mock Test"}]}const I=[{text:"Learn basic sentence structure and particles",href:"#/learn/grammar"},{text:"Study core vocabulary",href:"#/learn/vocab"},{text:"Learn basic kanji recognition",href:"#/kanji"},{text:"Practice grammar questions",href:"#/drill"},{text:"Practice short reading passages",href:"#/reading"},{text:"Practice listening drills",href:"#/listening"},{text:"Take the mock test",href:"#/test"},{text:"Review weak areas",href:"#/review"}];function K(s){return`
    <a class="syllabus-card" href="${s.href}" data-section="${s.id}">
      <p class="syllabus-card-index" aria-hidden="true">${s.idx}</p>
      <h3 class="syllabus-card-title">${s.title}</h3>
      <p class="syllabus-card-count">${u(s.count)}</p>
      <p class="syllabus-card-desc">${u(s.desc)}</p>
      <span class="syllabus-card-action">${u(s.action)} <span aria-hidden="true">\u2192</span></span>
    </a>
  `}function $(s,e){if(e.notAttempted)return`
      <li class="progress-row">
        <span class="progress-label">${u(s)}</span>
        <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:0%"></span></span>
        <span class="progress-value">Not attempted</span>
      </li>
    `;const c=e.total>0?Math.min(100,Math.round(e.done/e.total*100)):0,d=s==="Mock Test"?`${e.done} / ${e.total} (${e.percent??c}%)`:`${o(e.done)} / ${o(e.total)}`;return`
    <li class="progress-row">
      <span class="progress-label">${u(s)}</span>
      <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:${c}%"></span></span>
      <span class="progress-value">${d}</span>
    </li>
  `}async function V(s){const e=a.getHistory(),c=a.getResults(),d=Object.keys(e).length>0||c.length>0,g=a.getSettings().lastLearnId||null,p=await A(),l=D(p),t=N(p),r=a.getStreak?a.getStreak():null,y=(()=>{const n=new Date;return`${n.getFullYear()}-${String(n.getMonth()+1).padStart(2,"0")}-${String(n.getDate()).padStart(2,"0")}`})(),k=d&&r&&r.lastStudyDate===y,b=a.getReviewsToday?a.getReviewsToday():0,f=a.getDailyGoal?a.getDailyGoal():20,T=Math.min(100,Math.round(100*b/f)),m=a.getDueCountsBySkill?a.getDueCountsBySkill():{grammar:a.getDueCount?a.getDueCount():0,vocab:0,kanji:0},x=m.grammar+m.vocab+m.kanji,R=m.vocab>0||m.kanji>0?`<span class="muted small" style="margin-left:6px;">(${m.grammar} grammar \xB7 ${m.vocab} vocab \xB7 ${m.kanji} kanji)</span>`:"",S=a.getReviewForecast?a.getReviewForecast(7):[],_=Math.max(1,...S.map(n=>n.count)),C=j&&j[g]||g,P=d&&g?`<a class="resume-strip" href="#/learn/${encodeURIComponent(g)}">Last session: ${u(C)}.</a>`:"",L=d?"":`
    <aside class="starter-pack" aria-labelledby="starter-pack-h">
      <h3 id="starter-pack-h" class="starter-pack-title">New to JLPT N5? Start here.</h3>
      <p class="starter-pack-lede muted small">These 5 patterns are the foundation \u2014 every other N5 grammar pattern builds on these. Tap any one to read the explanation, examples, and common mistakes. Roughly <strong>5 minutes per pattern</strong>.</p>
      <ol class="starter-pack-list">
        ${[{id:"n5-001",label:"\u3067\u3059\uFF0F\u301C\u307E\u3059",why:"How sentences end politely"},{id:"n5-002",label:"\u306F",why:"The topic marker"},{id:"n5-058",label:"Verb-\u307E\u3059",why:"Polite verb form"},{id:"n5-077",label:"\u3044-Adjectives",why:"Describing things"},{id:"n5-024",label:"\u304B",why:"Asking questions"}].map((n,v)=>`
          <li>
            <a href="#/learn/${encodeURIComponent(n.id)}" class="starter-pack-card">
              <span class="starter-pack-num">${v+1}</span>
              <span class="starter-pack-meta">
                <strong lang="ja">${u(n.label)}</strong>
                <small>${u(n.why)}</small>
              </span>
            </a>
          </li>
        `).join("")}
      </ol>
      <p class="starter-pack-foot muted small">Or take the <a href="#/diagnostic">10-question diagnostic</a> to see what you already know.</p>
    </aside>
  `;s.innerHTML=`
    <section class="home-syllabus">
      <p class="home-up-link">
        <a href="#/levels">\u2190 All JLPT levels</a>
      </p>
      ${P}
      ${L}

      <header class="syllabus-header">
        <span class="syllabus-watermark" aria-hidden="true">\u4E94</span>
        <h1 class="syllabus-title">${i("home.syllabus_title")}</h1>
        <p class="syllabus-subtitle">${i("home.syllabus_subtitle")}</p>
        <!-- ISSUE-027 / IMP-048 (audit round-4): privacy / niche-N2
             trust band. Surfaces the most-defensible competitive claim
             on first paint. 2026-05-05: trust pills now use t() so
             they translate when the locale chip switches. -->
        <p class="syllabus-trust-band" aria-label="Trust signals">
          <span class="trust-pill"><span aria-hidden="true">\u25CF</span> ${i("trust.no_login")}</span>
          <span class="trust-pill"><span aria-hidden="true">\u25CF</span> ${i("trust.no_tracking")}</span>
          <a class="trust-pill" href="./" data-trust-install title="Install for offline use"><span aria-hidden="true">\u25CF</span> ${i("trust.works_offline")}</a>
          <a class="trust-pill" href="https://github.com/gauravaccentureproducts/JLPTSuccess/blob/master/LICENSE" target="_blank" rel="noopener" title="MIT licensed source \xB7 CC BY-SA content"><span aria-hidden="true">\u25CF</span> ${i("trust.open_source")}</a>
          <a class="trust-pill" href="PRIVACY.md" target="_blank" rel="noopener" title="No data leaves your device"><span aria-hidden="true">\u25CF</span> ${i("trust.on_device")}</a>
          <span class="trust-pill" title="Free, forever. No ads, no paywall, no upsell."><span aria-hidden="true">\u25CF</span> ${i("trust.free_no_paywall")}</span>
        </p>
        <ul class="syllabus-stat-pills" aria-label="Corpus size">
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(p.grammar)}</span><span class="syllabus-stat-lbl">grammar patterns</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(p.vocab)}</span><span class="syllabus-stat-lbl">vocab words</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(p.kanji)}</span><span class="syllabus-stat-lbl">kanji</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(p.reading)}</span><span class="syllabus-stat-lbl">reading passages</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${o(p.listening)}</span><span class="syllabus-stat-lbl">listening drills</span></li>
        </ul>
        ${d?`
          <div class="syllabus-daily-status">
            <span class="syllabus-daily-streak">Streak: ${r?.current??0} ${(r?.current??0)===1?"day":"days"}</span>
            <a class="syllabus-daily-progress" href="#/review" title="Open today's review queue">
              <span class="syllabus-daily-progress-label">${i("home.today_label")}: <strong>${b}</strong> / ${f}</span>
              <span class="syllabus-daily-progress-bar" aria-hidden="true">
                <span class="syllabus-daily-progress-fill" style="width:${T}%"></span>
              </span>
            </a>
            ${x>0?`
              <a class="syllabus-daily-due" href="#/review">
                ${i("home.reviews_due",{n:`<strong>${x}</strong>`})}${R}
              </a>
            `:`
              <span class="syllabus-daily-due is-empty">${i("home.no_reviews_due")}</span>
            `}
            <span class="syllabus-daily-today ${k?"is-met":"is-pending"}">
              <span class="syllabus-daily-mark" aria-hidden="true">${k?"\u2713":"\u25CB"}</span>
              <span class="syllabus-daily-text">${k?i("home.practiced_today"):i("home.not_yet_practiced")}</span>
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
          ${I.map((n,v)=>`
            <li class="study-order-item">
              <a class="study-order-link" href="${n.href}">
                <span class="study-order-num" aria-hidden="true">${String(v+1).padStart(2,"0")}</span>
                <span class="study-order-text">${u(n.text)}</span>
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
          ${$("Grammar",l.grammar)}
          ${$("Vocabulary",l.vocab)}
          ${$("Kanji",l.kanji)}
          ${$("Reading",l.reading)}
          ${$("Listening",l.listening)}
          ${$("Mock Test",l.mockTest)}
        </ul>
      </section>

      ${d&&S.length?`
        <!-- IMP-036 (audit round-3): 7-day review forecast.
             Aggregates FSRS-4 nextDue dates from grammar + vocab + kanji
             histories so the learner sees "tomorrow I'll have 8 reviews;
             Wednesday I'll have 25 - better stay on top of it". -->
        <section class="syllabus-forecast" aria-label="Review forecast">
          <header class="section-label">
            <span class="section-label-text">${i("home.forecast_label")}</span>
            <span class="section-label-rule" aria-hidden="true"></span>
          </header>
          <ol class="forecast-bar-chart">
            ${S.map(n=>{const v=n.count===0?4:Math.max(8,Math.round(56*n.count/_));return`
                <li class="forecast-bar">
                  <span class="forecast-bar-count">${n.count}</span>
                  <span class="forecast-bar-track" aria-hidden="true">
                    <span class="forecast-bar-fill" style="height:${v}px"></span>
                  </span>
                  <span class="forecast-bar-label muted small">${u(n.label)}</span>
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
  `}function u(s){return String(s??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{V as renderHome};
