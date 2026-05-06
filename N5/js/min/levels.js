const n=[{id:"n5",code:"N5",label:"Beginner",desc:"Basic Japanese - 177 grammar patterns, 1003 vocab, 106 kanji, 60 dokkai/listening drills.",href:"#/home",available:!0},{id:"n4",code:"N4",label:"Elementary",desc:"Builds on N5 with everyday topics, basic written passages, and lower-frequency kanji.",href:"../N4/",available:!1},{id:"n3",code:"N3",label:"Intermediate",desc:"Bridge between elementary and upper-intermediate Japanese - natural-speed listening.",href:"#/n3",available:!1},{id:"n2",code:"N2",label:"Upper-intermediate",desc:"Newspapers, business contexts, and abstract grammar; expected for university entry.",href:"#/n2",available:!1},{id:"n1",code:"N1",label:"Advanced",desc:"Logical reasoning, formal/literary registers, all major grammar at native speed.",href:"#/n1",available:!1}];function c(l){l.innerHTML=`
    <section class="levels-page">
      <header class="levels-header">
        <h1 class="levels-title">JLPT</h1>
        <p class="levels-subtitle">Choose a level to start. Each level has its own grammar, vocabulary, kanji, reading, and listening study material.</p>
      </header>
      <div class="levels-grid">
        ${n.map(e=>{if(e.available){const a=e.external?' rel="noopener" data-external="true"':"";return`
              <a class="level-card is-available" href="${e.href}" data-level="${e.id}"${a}>
                <span class="level-card-code">${e.code}</span>
                <h2 class="level-card-label">${e.label}</h2>
                <p class="level-card-desc">${e.desc}</p>
                <span class="level-card-arrow" aria-hidden="true">\u2192</span>
              </a>
            `}return`
            <div class="level-card is-disabled" data-level="${e.id}"
                 aria-disabled="true"
                 title="Content not yet available">
              <span class="level-card-code">${e.code}</span>
              <h2 class="level-card-label">${e.label}</h2>
              <p class="level-card-desc">${e.desc}</p>
            </div>
          `}).join("")}
      </div>
      <p class="levels-foot">
        N5 is currently the active level. N4 - N1 will fill in over time.
      </p>
    </section>
  `}function i(l){const e=(location.hash||"").match(/^#\/(n[1-4])(?:$|\/)/i),a=(e?e[1]:"N?").toUpperCase(),r=n.find(t=>t.id===a.toLowerCase())||{code:a,label:"Level",desc:""};l.innerHTML=`
    <section class="level-placeholder">
      <p class="level-placeholder-back">
        <a href="../">\u2190 All JLPT levels</a>
      </p>
      <h1 class="level-placeholder-title">JLPT ${s(a)}</h1>
      <p class="level-placeholder-label">${s(r.label)}</p>
      <div class="level-placeholder-card">
        <p class="level-placeholder-headline">Content not yet available.</p>
        <p>${s(r.desc)}</p>
        <p>This site currently ships the JLPT N5 corpus only. ${s(a)} content is on the roadmap.</p>
      </div>
      <p class="level-placeholder-foot">
        <a href="#/home" class="btn-action btn-action-secondary">Open JLPT N5 instead</a>
      </p>
    </section>
  `}function s(l){return String(l??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}export{i as renderLevelPlaceholder,c as renderLevels};
