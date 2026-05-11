import"./i18n.js";const t=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);let i=null;async function y(){if(i)return i;try{const s=await fetch("data/test_strategy.json");return s.ok?(i=await s.json(),i):null}catch(s){return console.warn("[exam-day] load failed:",s),null}}async function p(s){s.innerHTML='<p class="muted small">Loading exam-day prep\u2026</p>';const c=await y();if(!c||!c.meta_strategy){s.innerHTML=`<article class="exam-day-page"><p>Couldn't load exam-day data. Please retry.</p></article>`;return}const l=c.meta_strategy,h=l.five_minute_summary||[],u=l.exam_day_checklist||[],r=l.two_week_drill_schedule||[],d=l.study_distribution_recommendation||{},e=c.section_timing&&c.section_timing.exam_structure||{};s.innerHTML=`
    <article class="exam-day-page">
      <a class="back-link" href="#/strategy">\u2190 Back to Strategy</a>
      <h2>JLPT N5 \u2014 Exam-Day Prep</h2>
      <p class="page-lede">
        Print this page, or pull it up on your phone the morning of the test.
        Compact, actionable, sourced from <code>data/test_strategy.json</code>.
      </p>

      <section class="exam-day-callout">
        <h3>5-minute pre-exam summary</h3>
        <ul class="exam-day-list">
          ${h.map(a=>`<li>${t(a)}</li>`).join("")}
        </ul>
      </section>

      <section class="exam-day-callout exam-day-checklist-section">
        <h3>\u{1F4CB} Day-of-exam checklist</h3>
        <ul class="exam-day-checklist">
          ${u.map(a=>`<li><label><input type="checkbox" class="exam-check"> ${t(a)}</label></li>`).join("")}
        </ul>
        <p class="muted small">Your checks are saved locally so they survive page reloads.</p>
      </section>

      ${e.section_1?`
        <section class="exam-day-callout">
          <h3>Exam structure at a glance</h3>
          <table class="category-table">
            <thead>
              <tr><th>Section</th><th>Duration</th><th>Questions</th><th>Score min</th><th>Score max</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>${t(e.section_1.name||"Section 1")}</td>
                <td>${t(String(e.section_1.total_minutes||""))} min</td>
                <td>${t(String(e.section_1.total_questions||""))}</td>
                <td>${t(String(e.section_1.score_min_required||""))}</td>
                <td>${t(String(e.section_1.score_max||""))}</td>
              </tr>
              <tr>
                <td>${t(e.section_2?.name||"Section 2")}</td>
                <td>${t(String(e.section_2?.total_minutes||""))} min</td>
                <td>${t(String(e.section_2?.total_questions||""))}</td>
                <td>${t(String(e.section_2?.score_min_required||""))}</td>
                <td>${t(String(e.section_2?.score_max||""))}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr><th>Total to pass</th><th colspan="3"></th><th>\u2265 ${t(String(e.pass_threshold_total||80))} / ${t(String(e.pass_threshold_total_max||180))}</th></tr>
            </tfoot>
          </table>
          ${e.section_minimums_rule?`<p class="muted small">${t(e.section_minimums_rule)}</p>`:""}
        </section>
      `:""}

      ${Object.keys(d).length?`
        <section class="exam-day-callout">
          <h3>Recommended study-time distribution</h3>
          <ul class="exam-day-list">
            ${Object.entries(d).map(([a,n])=>`<li><strong>${t(a)}</strong>: ${t(n)}</li>`).join("")}
          </ul>
        </section>
      `:""}

      ${r.length?`
        <section class="exam-day-callout">
          <h3>14-day drill schedule</h3>
          <p class="muted small">Use the 14 days before exam day to cycle through these focused sessions:</p>
          <table class="category-table">
            <thead>
              <tr><th>Day</th><th>Focus</th><th>Minutes</th></tr>
            </thead>
            <tbody>
              ${r.map(a=>`<tr><td>Day ${t(String(a.day))}</td><td>${t(a.focus)}</td><td>${t(String(a.minutes||""))}</td></tr>`).join("")}
            </tbody>
          </table>
        </section>
      `:""}

      <p class="muted small" style="margin-top:24px">
        <a href="#/strategy">See full strategy bank \u2192</a>
        \xB7
        <a href="#/weakareas">View your weak-area diagnostic \u2192</a>
      </p>
    </article>
  `;const m="jlpt-n5-tutor:examDayChecks";let o={};try{o=JSON.parse(localStorage.getItem(m)||"{}")}catch{o={}}s.querySelectorAll(".exam-check").forEach((a,n)=>{a.checked=!!o[n],a.addEventListener("change",()=>{o[n]=a.checked;try{localStorage.setItem(m,JSON.stringify(o))}catch{}})})}export{p as renderExamDay};
