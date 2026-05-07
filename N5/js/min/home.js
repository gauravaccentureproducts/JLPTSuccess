import*as e from"./storage.js";import{t as r,currentLocale as _}from"./i18n.js";import{gatherSignal as O,recommend as G}from"./pedagogy-recommender.js";import{getBranding as V}from"./branding.js";let v=null,j=null;async function B(){if(v)return v;const t=["grammar","vocab","kanji","reading","listening"].map(n=>fetch(`data/${n}.json`).then(o=>o.ok?o.json():null).catch(()=>null)),[u,c,m,h,d]=await Promise.all(t),i=(n,...o)=>{if(!n)return 0;for(const f of o)if(Array.isArray(n[f]))return n[f].length;return 0};if(v={grammar:i(u,"patterns"),vocab:i(c,"entries"),kanji:i(m,"entries"),reading:i(h,"passages"),listening:i(d,"items")},u&&Array.isArray(u.patterns)){j={};for(const n of u.patterns){if(!n?.id)continue;const o=n.pattern||n.name||n.meaning_en||"";j[n.id]=o?`${n.id} - ${o}`:n.id}}return v}const p=s=>{const t=_()==="hi"?"hi-IN":"en-US";return Intl.NumberFormat(t).format(s||0)};function q(s){const t=e.getHistory(),u=e.getKnownKanji?e.getKnownKanji():{},c=e.getKnownVocab?e.getKnownVocab():{},m=e.getResults(),h=Object.values(t).filter($=>$&&($.isMastered||$.isManuallyKnown)).length,d=Object.keys(c).length,i=Object.keys(u).length,n=e.getCompletedReading?e.getCompletedReading():{},o=e.getCompletedListening?e.getCompletedListening():{},f=Object.keys(n).length,w=Object.keys(o).length,y=m.length?m[m.length-1]:null;return{grammar:{done:h,total:s.grammar},vocab:{done:d,total:s.vocab},kanji:{done:i,total:s.kanji},reading:{done:f,total:s.reading},listening:{done:w,total:s.listening},mockTest:y?{done:y.correct,total:y.total,percent:y.percent}:{done:0,total:0,percent:null,notAttempted:!0}}}function E(s){return[{idx:"01",id:"grammar",title:"Grammar",count:`${p(s.grammar)} patterns`,desc:"Basic sentence structure, particles, verb forms, adjectives, comparison, requests, and common N5 expressions.",href:"#/learn/grammar",action:"Open Grammar Syllabus"},{idx:"02",id:"vocab",title:"Vocabulary",count:`${p(s.vocab)} words`,desc:"Daily life words, time expressions, family, food, school, travel, verbs, adjectives, and common expressions.",href:"#/learn/vocab",action:"Open Vocabulary List"},{idx:"03",id:"kanji",title:"Kanji",count:`${p(s.kanji)} characters`,desc:"Numbers, time, people, school, directions, nature, common verbs, and basic recognition kanji.",href:"#/kanji",action:"Open Kanji List"},{idx:"04",id:"reading",title:"Reading",count:`${p(s.reading)} passages`,desc:"Short notices, simple messages, daily-life paragraphs, and basic comprehension practice.",href:"#/reading",action:"Start Reading Practice"},{idx:"05",id:"listening",title:"Listening",count:`${p(s.listening)} drills`,desc:"Greetings, classroom phrases, daily conversations, time, shopping, directions, and simple Q&A.",href:"#/listening",action:"Start Listening Practice"},{idx:"06",id:"test",title:"Mock Test",count:"15 questions",desc:"Auto-scored mock test with correct answers, explanations, and weak-area review.",href:"#/test",action:"Take Mock Test"}]}const F=[{text:"Learn basic sentence structure and particles",href:"#/learn/grammar"},{text:"Study core vocabulary",href:"#/learn/vocab"},{text:"Learn basic kanji recognition",href:"#/kanji"},{text:"Practice grammar questions",href:"#/drill"},{text:"Practice short reading passages",href:"#/reading"},{text:"Practice listening drills",href:"#/listening"},{text:"Take the mock test",href:"#/test"},{text:"Review weak areas",href:"#/review"}];function H(s){return`
    <a class="syllabus-card" href="${s.href}" data-section="${s.id}">
      <p class="syllabus-card-index" aria-hidden="true">${s.idx}</p>
      <h3 class="syllabus-card-title">${s.title}</h3>
      <p class="syllabus-card-count">${l(s.count)}</p>
      <p class="syllabus-card-desc">${l(s.desc)}</p>
      <span class="syllabus-card-action">${l(s.action)} <span aria-hidden="true">\u2192</span></span>
    </a>
  `}function k(s,t){if(t.notAttempted)return`
      <li class="progress-row">
        <span class="progress-label">${l(s)}</span>
        <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:0%"></span></span>
        <span class="progress-value">Not attempted</span>
      </li>
    `;const u=t.total>0?Math.min(100,Math.round(t.done/t.total*100)):0,c=s==="Mock Test"?`${t.done} / ${t.total} (${t.percent??u}%)`:`${p(t.done)} / ${p(t.total)}`;return`
    <li class="progress-row">
      <span class="progress-label">${l(s)}</span>
      <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:${u}%"></span></span>
      <span class="progress-value">${c}</span>
    </li>
  `}async function W(s){const t=e.getHistory(),u=e.getResults(),c=Object.keys(t).length>0||u.length>0,m=e.getSettings(),h=m.lastLearnId||null,d=await B(),i=q(d),n=E(d),o=e.getStreak?e.getStreak():null,f=(()=>{const a=new Date;return`${a.getFullYear()}-${String(a.getMonth()+1).padStart(2,"0")}-${String(a.getDate()).padStart(2,"0")}`})(),w=c&&o&&o.lastStudyDate===f,y=e.getReviewsToday?e.getReviewsToday():0,$=e.getDailyGoal?e.getDailyGoal():20,T=Math.min(100,Math.round(100*y/$)),g=e.getDueCountsBySkill?e.getDueCountsBySkill():{grammar:e.getDueCount?e.getDueCount():0,vocab:0,kanji:0},x=g.grammar+g.vocab+g.kanji,C=g.vocab>0||g.kanji>0?`<span class="muted small" style="margin-left:6px;">(${g.grammar} grammar \xB7 ${g.vocab} vocab \xB7 ${g.kanji} kanji)</span>`:"",S=e.getReviewForecast?e.getReviewForecast(7):[],L=Math.max(1,...S.map(a=>a.count)),M=j&&j[h]||h,P=c&&h?`<a class="resume-strip" href="#/learn/${encodeURIComponent(h)}">Last session: ${l(M)}.</a>`:"",A=[{id:"n5-001",label:"\u3067\u3059\uFF0F\u301C\u307E\u3059",why:"How sentences end politely"},{id:"n5-002",label:"\u306F",why:"The topic marker"},{id:"n5-058",label:"Verb-\u307E\u3059",why:"Polite verb form"},{id:"n5-077",label:"\u3044-Adjectives",why:"Describing things"},{id:"n5-024",label:"\u304B",why:"Asking questions"}],D=m.showRecommender!==!1;let R="";try{if(c&&D){const a=G(O({corpusCounts:d}));if(a){const b=_(),I=b==="hi"?a.label_hi:a.label_en,K=b==="hi"?a.why_hi:a.why_en;R=`
          <aside class="home-recommend" aria-labelledby="home-recommend-h">
            <h3 id="home-recommend-h" class="home-recommend-title">${l(r("home.recommend_title")||"Recommended next")}</h3>
            <a class="home-recommend-action" href="${l(a.href)}">
              <span class="home-recommend-label"><strong>${l(I)}</strong></span>
              <span class="home-recommend-meta muted small">${l(a.duration)} \xB7 ${l(a.rule_id)}</span>
            </a>
            <p class="home-recommend-why muted small">${l(K)}</p>
          </aside>
        `}}}catch(a){typeof console<"u"&&console.warn("[recommender] suppressed:",a)}const N=c?"":`
    <aside class="starter-pack" aria-labelledby="starter-pack-h">
      <h3 id="starter-pack-h" class="starter-pack-title">New to JLPT N5? Start here.</h3>
      <p class="starter-pack-lede muted small">These 5 patterns are the foundation \u2014 every other N5 grammar pattern builds on these. Tap any one to read the explanation, examples, and common mistakes. Roughly <strong>5 minutes per pattern</strong>.</p>
      <ol class="starter-pack-list">
        ${A.map((a,b)=>`
          <li>
            <a href="#/learn/${encodeURIComponent(a.id)}" class="starter-pack-card">
              <span class="starter-pack-num">${b+1}</span>
              <span class="starter-pack-meta">
                <strong lang="ja">${l(a.label)}</strong>
                <small>${l(a.why)}</small>
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
      ${N}

      <header class="syllabus-header">
        <span class="syllabus-watermark" aria-hidden="true">${l(V()?.brand?.home_glyph||"\u4E94")}</span>
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
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${p(d.grammar)}</span><span class="syllabus-stat-lbl">grammar patterns</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${p(d.vocab)}</span><span class="syllabus-stat-lbl">vocab words</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${p(d.kanji)}</span><span class="syllabus-stat-lbl">kanji</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${p(d.reading)}</span><span class="syllabus-stat-lbl">reading passages</span></li>
          <li class="syllabus-stat-pill"><span class="syllabus-stat-num">${p(d.listening)}</span><span class="syllabus-stat-lbl">listening drills</span></li>
        </ul>
        ${c?`
          <div class="syllabus-daily-status">
            <span class="syllabus-daily-streak">Streak: ${o?.current??0} ${(o?.current??0)===1?"day":"days"}</span>
            <a class="syllabus-daily-progress" href="#/review" title="Open today's review queue">
              <span class="syllabus-daily-progress-label">${r("home.today_label")}: <strong>${y}</strong> / ${$}</span>
              <span class="syllabus-daily-progress-bar" aria-hidden="true">
                <span class="syllabus-daily-progress-fill" style="width:${T}%"></span>
              </span>
            </a>
            ${x>0?`
              <a class="syllabus-daily-due" href="#/review">
                ${r("home.reviews_due",{n:`<strong>${x}</strong>`})}${C}
              </a>
            `:`
              <span class="syllabus-daily-due is-empty">${r("home.no_reviews_due")}</span>
            `}
            <span class="syllabus-daily-today ${w?"is-met":"is-pending"}">
              <span class="syllabus-daily-mark" aria-hidden="true">${w?"\u2713":"\u25CB"}</span>
              <span class="syllabus-daily-text">${w?r("home.practiced_today"):r("home.not_yet_practiced")}</span>
            </span>
          </div>
        `:""}
      </header>

      ${R}

      <section class="syllabus-overview" aria-label="Syllabus overview">
        <header class="section-label">
          <span class="section-label-text">Syllabus</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <div class="syllabus-grid">
          ${n.map(H).join("")}
        </div>
      </section>

      <section class="syllabus-study-order" aria-label="Recommended study order">
        <header class="section-label">
          <span class="section-label-text">Recommended Study Order</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <ol class="study-order-list">
          ${F.map((a,b)=>`
            <li class="study-order-item">
              <a class="study-order-link" href="${a.href}">
                <span class="study-order-num" aria-hidden="true">${String(b+1).padStart(2,"0")}</span>
                <span class="study-order-text">${l(a.text)}</span>
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
          ${k("Grammar",i.grammar)}
          ${k("Vocabulary",i.vocab)}
          ${k("Kanji",i.kanji)}
          ${k("Reading",i.reading)}
          ${k("Listening",i.listening)}
          ${k("Mock Test",i.mockTest)}
        </ul>
      </section>

      ${c&&S.length?`
        <!-- IMP-036 (audit round-3): 7-day review forecast.
             Aggregates FSRS-4 nextDue dates from grammar + vocab + kanji
             histories so the learner sees "tomorrow I'll have 8 reviews;
             Wednesday I'll have 25 - better stay on top of it". -->
        <section class="syllabus-forecast" aria-label="Review forecast">
          <header class="section-label">
            <span class="section-label-text">${r("home.forecast_label")}</span>
            <span class="section-label-rule" aria-hidden="true"></span>
          </header>
          <ol class="forecast-bar-chart">
            ${S.map(a=>{const b=a.count===0?4:Math.max(8,Math.round(56*a.count/L));return`
                <li class="forecast-bar">
                  <span class="forecast-bar-count">${a.count}</span>
                  <span class="forecast-bar-track" aria-hidden="true">
                    <span class="forecast-bar-fill" style="height:${b}px"></span>
                  </span>
                  <span class="forecast-bar-label muted small">${l(a.label)}</span>
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
  `}function l(s){return String(s??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{W as renderHome};
