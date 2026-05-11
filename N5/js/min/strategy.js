const e=s=>String(s??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t]);let i=null;async function c(){if(i)return i;try{const s=await fetch("data/test_strategy.json");if(!s.ok)throw new Error(`HTTP ${s.status}`);return i=await s.json(),i}catch(s){return console.error("[strategy] load failed:",s),null}}function d(s){return s?`
    <section class="strategy-block">
      <h3>T1 \xB7 Section &amp; mondai timing</h3>
      ${["moji_goi","bunpou_dokkai","chokai"].map(l=>{const a=s[l];if(!a)return"";const n=(a.mondai_breakdown||[]).map(o=>`
      <tr>
        <td>${e(o.number)}</td>
        <td>${e(o.type)} ${o.label_ja?`<span class="muted small" lang="ja">${e(o.label_ja)}</span>`:""}</td>
        <td>${e(o.n_questions)}</td>
        <td>${e(o.seconds_per_q)}s</td>
        <td class="muted small">${e(o.strategy||"")}</td>
      </tr>
    `).join("");return`
      <section class="timing-section">
        <h4>${e(a.section_part||l)} \u2014 ${e(a.module||"")}</h4>
        <p class="muted small">${e(a.total_minutes)} min \xB7 ${e(a.total_questions)} questions \xB7 avg ${e(a.average_seconds_per_question)}s/q</p>
        <table class="timing-table">
          <thead><tr><th>Mondai</th><th>Type</th><th>Q</th><th>Time/Q</th><th>Strategy</th></tr></thead>
          <tbody>${n}</tbody>
        </table>
        ${a.time_budget_warning?`<p class="muted small warning">\u26A0 ${e(a.time_budget_warning)}</p>`:""}
        ${a.rest_break?`<p class="muted small">${e(a.rest_break)}</p>`:""}
        ${a.format_note?`<p class="muted small">${e(a.format_note)}</p>`:""}
      </section>
    `}).join("")}
    </section>
  `:""}function m(s){if(!Array.isArray(s)||!s.length)return"";const t={};s.forEach(l=>{var a;(t[a=l.module||"other"]||(t[a]=[])).push(l)});const r=Object.entries(t).map(([l,a])=>`
    <details class="trap-group">
      <summary><strong>${e(l)}</strong> (${a.length})</summary>
      <ul class="trap-list">
        ${a.map(n=>`
          <li>
            <p><strong>${e(n.name||"")}</strong> \u2014 ${e(n.description||"")}</p>
            ${n.wrong_example?`<p class="wrong" lang="ja">\u2717 ${e(n.wrong_example)}</p>`:""}
            ${n.correct_example?`<p class="right" lang="ja">\u2713 ${e(n.correct_example)}</p>`:""}
            ${n.defense?`<p class="muted small"><em>Defense:</em> ${e(n.defense)}</p>`:""}
          </li>
        `).join("")}
      </ul>
    </details>
  `).join("");return`
    <section class="strategy-block">
      <h3>T2 \xB7 Trap-pattern catalog (${s.length} traps)</h3>
      ${r}
    </section>
  `}function p(s){return!Array.isArray(s)||!s.length?"":`
    <section class="strategy-block">
      <h3>T3 \xB7 Test-taking techniques (${s.length})</h3>
      <ul class="techniques-list">
        ${s.map(t=>`
          <li>
            <p><strong>${e(t.title_en||t.name||"")}</strong>${t.title_ja?` <span class="muted small" lang="ja">${e(t.title_ja)}</span>`:""}</p>
            <p>${e(t.description||"")}</p>
            ${t.applies_to?.length?`<p class="muted small">Applies to: ${t.applies_to.map(e).join(", ")}</p>`:""}
            ${t.rationale?`<p class="muted small"><em>Why:</em> ${e(t.rationale)}</p>`:""}
            ${t.warning?`<p class="warning"><em>\u26A0 Warning:</em> ${e(t.warning)}</p>`:""}
          </li>
        `).join("")}
      </ul>
    </section>
  `}function g(s){if(!s||typeof s!="object")return"";const t=s.sections||{},r=s.total_score||{},l=s.diagnostic_band||{};return`
    <section class="strategy-block">
      <h3>T4 \xB7 Score breakdown</h3>
      <p class="muted small">${e(s.scoring_system||"")}</p>
      <table class="score-table">
        <thead><tr><th>Section</th><th>Max</th><th>Pass min</th></tr></thead>
        <tbody>
          ${Object.entries(t).map(([a,n])=>`
            <tr>
              <td>${e(n.label||a)}</td>
              <td>${e(n.max_score)}</td>
              <td>${e(n.pass_min)}</td>
            </tr>
          `).join("")}
          <tr><td><strong>Total</strong></td><td><strong>${e(r.max_score)}</strong></td><td><strong>${e(r.pass_min)}</strong></td></tr>
        </tbody>
      </table>
      ${r.rule?`<p class="muted small"><strong>Rule:</strong> ${e(r.rule)}</p>`:""}
      ${s.scaling_explanation?`<p class="muted small"><strong>Scaling:</strong> ${e(s.scaling_explanation)}</p>`:""}
      <h4>Diagnostic bands</h4>
      <ul class="diag-bands">
        ${Object.entries(l).map(([a,n])=>`
          <li><strong>${e(a)}:</strong> ${e(n)}</li>
        `).join("")}
      </ul>
    </section>
  `}function u(s){return!s||!Array.isArray(s.diagnostic_areas)?"":`
    <section class="strategy-block">
      <h3>T5 \xB7 Diagnostic + drill recommendations</h3>
      <ul class="diagnostic-list">
        ${s.diagnostic_areas.map(t=>`
          <li>
            <p><strong>${e(t.area)}</strong></p>
            ${t.diagnostic_questions?.length?`<p class="muted small">Diagnostic: ${t.diagnostic_questions.map(e).join("; ")}</p>`:""}
            ${t.drill_recommendation?`<p>${e(t.drill_recommendation)}</p>`:""}
            ${t.module_pointers?.length?`<p class="muted small">References: ${t.module_pointers.map(e).join(", ")}</p>`:""}
          </li>
        `).join("")}
      </ul>
      ${s.drill_methodology?.length?`
        <h4>Drill methodology</h4>
        <ol>${s.drill_methodology.map(t=>`<li>${e(t)}</li>`).join("")}</ol>
      `:""}
    </section>
  `}function $(s){return!s||typeof s!="object"?"":`
    <section class="strategy-block">
      <h3>T6 \xB7 Meta-strategy</h3>
      ${s.five_minute_summary?.length?`
        <h4>Five-minute summary</h4>
        <ol>${s.five_minute_summary.map(t=>`<li>${e(t)}</li>`).join("")}</ol>
      `:""}
      ${s.study_distribution_recommendation?`
        <h4>Study distribution</h4>
        <ul>${Object.entries(s.study_distribution_recommendation).map(([t,r])=>`<li><strong>${e(t)}:</strong> ${e(r)}</li>`).join("")}</ul>
      `:""}
      ${s.two_week_drill_schedule?.length?`
        <details>
          <summary><strong>Fourteen-day drill schedule</strong></summary>
          <ol>${s.two_week_drill_schedule.map(t=>`<li><strong>Day ${e(t.day)}:</strong> ${e(t.focus)} <span class="muted small">(${e(t.minutes)} min)</span></li>`).join("")}</ol>
        </details>
      `:""}
      ${s.exam_day_checklist?.length?`
        <h4>Exam-day checklist</h4>
        <ul>${s.exam_day_checklist.map(t=>`<li>${e(t)}</li>`).join("")}</ul>
      `:""}
    </section>
  `}async function h(s){s.innerHTML='<p class="muted small">Loading test strategy\u2026</p>';const t=await c();if(!t){s.innerHTML='<article class="strategy-page"><p>Could not load test-strategy data. Please try again.</p></article>';return}s.innerHTML=`
    <article class="strategy-page">
      <a class="back-link" href="#/home">\u2190 Back home</a>
      <h2>JLPT N5 \xB7 Test-taking strategy</h2>
      <p class="muted small">${e(t.source_notes||"")}</p>
      <!-- IMP-WAVE-P4-T6 (2026-05-11): focused entry-point into the
           printable exam-day prep page (extracts meta_strategy into
           an actionable checklist). -->
      <p>
        <a href="#/examday" class="btn-secondary" style="text-decoration:none">\u{1F4CB} Open exam-day prep checklist \u2192</a>
        \xB7
        <a href="#/weakareas" style="margin-left:8px">Weak-area diagnostic \u2192</a>
      </p>
      ${d(t.section_timing)}
      ${m(t.trap_patterns)}
      ${p(t.techniques)}
      ${g(t.score_breakdown)}
      ${u(t.diagnostic_drills)}
      ${$(t.meta_strategy)}
      <p class="muted small">Schema version ${e(t.schema_version)} \xB7 last updated ${e(t.last_updated)}</p>
    </article>
  `}export{h as renderStrategy};
