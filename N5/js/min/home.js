import*as s from"./storage.js";import{t as e,currentLocale as S}from"./i18n.js";import{gatherSignal as O,recommend as I}from"./pedagogy-recommender.js";import"./branding.js";let v=null,$=null;async function P(){if(v)return v;const t=["grammar","vocab","kanji","reading","listening"].map(r=>fetch(`data/${r}.json`).then(l=>l.ok?l.json():null).catch(()=>null)),[i,c,d,m,h]=await Promise.all(t),u=(r,...l)=>{if(!r)return 0;for(const y of l)if(Array.isArray(r[y]))return r[y].length;return 0};if(v={grammar:u(i,"patterns"),vocab:u(c,"entries"),kanji:u(d,"entries"),reading:u(m,"passages"),listening:u(h,"items")},i&&Array.isArray(i.patterns)){$={};for(const r of i.patterns){if(!r?.id)continue;const l=r.pattern||r.name||r.meaning_en||"";$[r.id]=l?`${r.id} - ${l}`:r.id}}return v}const w=a=>{const t=S()==="hi"?"hi-IN":"en-US";return Intl.NumberFormat(t).format(a||0)};function B(a){const t=s.getHistory(),i=s.getKnownKanji?s.getKnownKanji():{},c=s.getKnownVocab?s.getKnownVocab():{},d=s.getResults(),m=Object.values(t).filter(_=>_&&(_.isMastered||_.isManuallyKnown)).length,h=Object.keys(c).length,u=Object.keys(i).length,r=s.getCompletedReading?s.getCompletedReading():{},l=s.getCompletedListening?s.getCompletedListening():{},y=Object.keys(r).length,b=Object.keys(l).length,g=d.length?d[d.length-1]:null;return{grammar:{done:m,total:a.grammar},vocab:{done:h,total:a.vocab},kanji:{done:u,total:a.kanji},reading:{done:y,total:a.reading},listening:{done:b,total:a.listening},mockTest:g?{done:g.correct,total:g.total,percent:g.percent}:{done:0,total:0,percent:null,notAttempted:!0}}}function q(a){const t=(i,c)=>{const d=e(`home.${i}`);return typeof d=="string"&&d.includes("${n}")?d.replace("${n}",w(c)):d};return[{idx:"01",id:"grammar",title:e("home.card_grammar_title"),count:t("card_grammar_count",a.grammar),desc:e("home.card_grammar_desc"),href:"learn/grammar/",action:e("home.card_grammar_action")},{idx:"02",id:"vocab",title:e("home.card_vocab_title"),count:t("card_vocab_count",a.vocab),desc:e("home.card_vocab_desc"),href:"learn/vocab/",action:e("home.card_vocab_action")},{idx:"03",id:"kanji",title:e("home.card_kanji_title"),count:t("card_kanji_count",a.kanji),desc:e("home.card_kanji_desc"),href:"kanji/",action:e("home.card_kanji_action")},{idx:"04",id:"reading",title:e("home.card_reading_title"),count:t("card_reading_count",a.reading),desc:e("home.card_reading_desc"),href:"reading/",action:e("home.card_reading_action")},{idx:"05",id:"listening",title:e("home.card_listening_title"),count:t("card_listening_count",a.listening),desc:e("home.card_listening_desc"),href:"listening/",action:e("home.card_listening_action")},{idx:"06",id:"test",title:e("home.card_test_title"),count:e("home.card_test_count"),desc:e("home.card_test_desc"),href:"test/",action:e("home.card_test_action")}]}function J(){return[{text:e("home.study_step_grammar"),href:"learn/grammar/"},{text:e("home.study_step_vocab"),href:"learn/vocab/"},{text:e("home.study_step_kanji"),href:"kanji/"},{text:e("home.study_step_drill"),href:"drill/"},{text:e("home.study_step_reading"),href:"reading/"},{text:e("home.study_step_listening"),href:"listening/"},{text:e("home.study_step_test"),href:"test/"},{text:e("home.study_step_review"),href:"review/"},{text:e("home.study_step_authentic"),href:"authentic/"}]}function F(a){return`
    <a class="syllabus-card" href="${a.href}" data-section="${a.id}">
      <p class="syllabus-card-index" aria-hidden="true">${a.idx}</p>
      <h3 class="syllabus-card-title">${a.title}</h3>
      <p class="syllabus-card-count">${o(a.count)}</p>
      <p class="syllabus-card-desc">${o(a.desc)}</p>
      <span class="syllabus-card-action">${o(a.action)} <span aria-hidden="true">\u2192</span></span>
    </a>
  `}function U(a,t){if(t.notAttempted)return`
      <li class="progress-row">
        <span class="progress-label">${o(a)}</span>
        <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:0%"></span></span>
        <span class="progress-value">${o(e("home.progress_not_attempted"))}</span>
      </li>
    `;const i=t.total>0?Math.min(100,Math.round(t.done/t.total*100)):0,c=a===e("home.progress_label_test")||a==="Mock Test"?`${t.done} / ${t.total} (${t.percent??i}%)`:`${w(t.done)} / ${w(t.total)}`;return`
    <li class="progress-row">
      <span class="progress-label">${o(a)}</span>
      <span class="progress-bar" aria-hidden="true"><span class="progress-fill" style="width:${i}%"></span></span>
      <span class="progress-value">${c}</span>
    </li>
  `}async function W(a){const t=s.getHistory(),i=s.getResults(),c=Object.keys(t).length>0||i.length>0,d=s.getSettings(),m=d.lastLearnId||null,h=await P(),u=B(h),r=q(h),l=s.getStreak?s.getStreak():null,y=(()=>{const n=new Date;return`${n.getFullYear()}-${String(n.getMonth()+1).padStart(2,"0")}-${String(n.getDate()).padStart(2,"0")}`})(),b=c&&l&&l.lastStudyDate===y,g=s.getReviewsToday?s.getReviewsToday():0,_=s.getDailyGoal?s.getDailyGoal():20,R=Math.min(100,Math.round(100*g/_)),p=s.getDueCountsBySkill?s.getDueCountsBySkill():{grammar:s.getDueCount?s.getDueCount():0,vocab:0,kanji:0},j=p.grammar+p.vocab+p.kanji,C=p.vocab>0||p.kanji>0?`<span class="muted small" style="margin-left:6px;">(${p.grammar} grammar \xB7 ${p.vocab} vocab \xB7 ${p.kanji} kanji)</span>`:"",k=s.getReviewForecast?s.getReviewForecast(7):[],M=Math.max(1,...k.map(n=>n.count)),A=$&&$[m]||m,D=c&&m?`<a class="resume-strip" href="learn/${encodeURIComponent(m)}/">Last session: ${o(A)}.</a>`:"",K=d.showRecommender!==!1;let x="";try{if(c&&K){const n=I(O({corpusCounts:h}));if(n){const f=S(),T=f==="hi"?n.label_hi:n.label_en,L=f==="hi"?n.why_hi:n.why_en;x=`
          <aside class="home-recommend" aria-labelledby="home-recommend-h">
            <h3 id="home-recommend-h" class="home-recommend-title">${o(e("home.recommend_title")||"Recommended next")}</h3>
            <a class="home-recommend-action" href="${o(n.href)}">
              <span class="home-recommend-label"><strong>${o(T)}</strong></span>
              <span class="home-recommend-meta muted small">${o(n.duration)} \xB7 ${o(n.rule_id)}</span>
            </a>
            <p class="home-recommend-why muted small">${o(L)}</p>
          </aside>
        `}}}catch(n){typeof console<"u"&&console.warn("[recommender] suppressed:",n)}a.innerHTML=`
    <section class="home-syllabus">
      <p class="home-up-link">
        <a href="../">\u2190 ${e("nav.all_levels")}</a>
      </p>
      ${D}

      ${c?`
        <div class="syllabus-daily-status">
          <span class="syllabus-daily-streak">Streak: ${l?.current??0} ${(l?.current??0)===1?"day":"days"}</span>
          <a class="syllabus-daily-progress" href="review/" title="Open today's mixed-skill review queue (grammar + vocab + kanji SRS)">
            <span class="syllabus-daily-progress-label">${e("home.today_label")}: <strong>${g}</strong> / ${_}</span>
            <span class="syllabus-daily-progress-bar" aria-hidden="true">
              <span class="syllabus-daily-progress-fill" style="width:${R}%"></span>
            </span>
          </a>
          ${j>0?`
            <a class="syllabus-daily-due" href="review/">
              ${e("home.reviews_due",{n:`<strong>${j}</strong>`})}${C}
            </a>
          `:`
            <span class="syllabus-daily-due is-empty">${e("home.no_reviews_due")}</span>
          `}
          <span class="syllabus-daily-today ${b?"is-met":"is-pending"}">
            <span class="syllabus-daily-mark" aria-hidden="true">${b?"\u2713":"\u25CB"}</span>
            <span class="syllabus-daily-text">${b?e("home.practiced_today"):e("home.not_yet_practiced")}</span>
          </span>
        </div>
      `:""}

      ${x}

      <!-- SVA-1.3 (2026-05-22) home-privacy-hero removed 2026-05-26 per
           user request (visual clutter; trust signals communicated via
           /privacy and /notices pages instead). i18n key home.privacy_hero
           retained in locales/*.json so JA-108 key-set parity stays
           clean and any future revert is a single template-block
           addition. -->

      <section class="syllabus-overview" aria-label="Syllabus overview">
        <header class="section-label">
          <span class="section-label-text">${o(e("home.syllabus_section_label"))}</span>
          <span class="section-label-rule" aria-hidden="true"></span>
        </header>
        <div class="syllabus-grid">
          ${r.map(F).join("")}
        </div>
      </section>

      <!-- Recommended-study-order + progress-overview sections removed
           2026-05-27 per user request (visual clutter on home page). The
           studyOrder() helper, computeProgress(), and renderProgressRow()
           remain defined above so a future revert is a single template-
           block addition. i18n keys home.study_order_*, home.progress_*
           retained in locales/*.json so JA-108 key-set parity stays
           clean. Matches the v1.17.8 home-privacy-hero removal pattern. -->

      ${c&&k.length?`
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
            ${k.map(n=>{const f=n.count===0?4:Math.max(8,Math.round(56*n.count/M));return`
                <li class="forecast-bar">
                  <span class="forecast-bar-count">${n.count}</span>
                  <span class="forecast-bar-track" aria-hidden="true">
                    <span class="forecast-bar-fill" style="height:${f}px"></span>
                  </span>
                  <span class="forecast-bar-label muted small">${o(n.label)}</span>
                </li>
              `}).join("")}
          </ol>
          <p class="muted small" style="margin-top:6px;">
            <a href="missed/">Browse wrong-answer history \u2192</a>
          </p>
        </section>
      `:""}

      <!-- "Not sure where to start?" action CTA section removed
           2026-05-27 per user request (visual clutter; placement check
           is still reachable from the diagnostic route directly, and
           grammar is reachable from the primary nav). i18n keys
           home.action_prompt / home.action_placement / home.action_start_grammar
           retained in locales/*.json so JA-108 key-set parity stays
           clean and a future revert is a single template-block addition. -->
    </section>
  `}function o(a){return String(a??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}export{W as renderHome};
