import"./furigana.js";import{t as $}from"./i18n.js";const t=e=>String(e??"").replace(/[&<>"']/g,i=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[i]);let h=null;async function _(){if(h)return h;const[e,i,l,n]=await Promise.all([fetch("data/authentic.json"),fetch("data/vocab.json"),fetch("data/kanji.json"),fetch("data/grammar.json")]),[o,u,m,f]=await Promise.all([e.json(),i.json(),l.json(),n.json()]),b=o&&o.items||[],d=new Map;for(const a of b)d.set(a.id,a);const k=u&&u.entries||[],g=m&&m.entries||(Array.isArray(m)?m:[]),y=f&&f.patterns||[];return h={authItems:b,cardById:d,vocabEntries:k,kanjiEntries:g,grammarPatterns:y},h}function w(e){const i=[];for(const l of e.vocabEntries){const n=l.authentic_refs||[];n.length&&i.push({skill:"vocab",id:l.id,display_label:l.form||l.reading||l.id,display_sub:l.gloss_en||l.gloss||"",reading:l.reading||"",refs:n,href:`#/learn/vocab/${encodeURIComponent(l.id)}`})}for(const l of e.kanjiEntries){const n=l.authentic_refs||[];n.length&&i.push({skill:"kanji",id:l.id,display_label:l.glyph||l.id,display_sub:(l.meanings||[]).join(", "),reading:(l.kun||[]).concat(l.on||[]).join(" / "),refs:n,href:`#/kanji/${encodeURIComponent(l.id)}`})}for(const l of e.grammarPatterns){const n=l.authentic_refs||[];n.length&&i.push({skill:"grammar",id:l.id,display_label:l.pattern||l.id,display_sub:l.meaning_en||"",reading:"",refs:n,href:`#/learn/${encodeURIComponent(l.id)}`})}return i}const j={vocab:{en:"Vocab",ja:"\u8A9E\u5F59"},kanji:{en:"Kanji",ja:"\u6F22\u5B57"},grammar:{en:"Grammar",ja:"\u6587\u6CD5"}},E={hospital:"#d6604d",menu:"#f4a582",notice:"#92c5de",post:"#fddbc7",shop:"#5aae61",signs:"#4393c3",time:"#b2182b",transit:"#2166ac",weather:"#9970ab"};async function x(e){e.innerHTML='<div class="placeholder"><p>Loading mining index\u2026</p></div>';const i=await _(),l=w(i);let n="all",o="skill";const u=a=>{const s=i.cardById.get(a);if(!s)return`<span class="mining-card-chip mining-card-missing" title="Missing card: ${t(a)}">?</span>`;const c=E[s.category]||"#888",r=s.ja||a,p=s.gloss_en||"",v=`${r} \u2014 ${p} (${s.category||"?"})`;return`<a class="mining-card-chip" href="#/authentic" data-card-id="${t(a)}" title="${t(v)}" style="border-left:3px solid ${c}">
      <span class="mining-card-ja" lang="ja">${t(r)}</span>
      ${p?`<span class="mining-card-en muted small">${t(p)}</span>`:""}
    </a>`},m=a=>`
    <li class="mining-row" data-skill="${t(a.skill)}">
      <a class="mining-entry" href="${a.href}">
        <span class="mining-skill-badge mining-skill-${t(a.skill)}" aria-label="${t(j[a.skill]?.en||a.skill)}">${t(j[a.skill]?.en?.[0]||"?")}</span>
        <span class="mining-entry-label" lang="ja">${t(a.display_label)}</span>
        ${a.reading?`<span class="mining-entry-reading muted small" lang="ja">${t(a.reading)}</span>`:""}
        ${a.display_sub?`<span class="mining-entry-sub muted small">${t(a.display_sub)}</span>`:""}
      </a>
      <div class="mining-cards">
        ${a.refs.map(u).join("")}
      </div>
      <span class="mining-count muted small" aria-label="linked cards">\xD7${a.refs.length}</span>
    </li>
  `,f=a=>{const s=[...a];if(o==="count")s.sort((c,r)=>r.refs.length-c.refs.length||c.display_label.localeCompare(r.display_label));else if(o==="label")s.sort((c,r)=>c.display_label.localeCompare(r.display_label,"ja"));else{const c={vocab:0,kanji:1,grammar:2};s.sort((r,p)=>c[r.skill]-c[p.skill]||r.display_label.localeCompare(p.display_label,"ja"))}return s},b=()=>{const a=f(l);return n==="all"?a:a.filter(s=>s.skill===n)},d={all:l.length,vocab:l.filter(a=>a.skill==="vocab").length,kanji:l.filter(a=>a.skill==="kanji").length,grammar:l.filter(a=>a.skill==="grammar").length},k=l.reduce((a,s)=>a+s.refs.length,0),g=()=>{const a=b().map(m).join("");e.innerHTML=`
      <article class="mining-page">
        <header class="mining-header">
          <h2>${t($("mining.title")||"Real-world cross-links")}</h2>
          <p class="muted small">${t($("mining.tagline")||"Every vocab / kanji / grammar entry that links to one or more authentic real-Japan cards. Click an entry to jump to its detail page; click a card chip to browse the full authentic library.")}</p>
          <p class="muted small">${d.all} entries linked across ${i.authItems.length} authentic cards (${k} cross-links total).</p>
        </header>

        <div class="mining-toolbar" role="toolbar" aria-label="Filters and sort">
          <div class="mining-filters" role="group" aria-label="Filter by skill">
            <button type="button" class="mining-filter ${n==="all"?"active":""}"     data-filter="all">All <span class="muted small">(${d.all})</span></button>
            <button type="button" class="mining-filter ${n==="vocab"?"active":""}"   data-filter="vocab">Vocab <span class="muted small">(${d.vocab})</span></button>
            <button type="button" class="mining-filter ${n==="kanji"?"active":""}"   data-filter="kanji">Kanji <span class="muted small">(${d.kanji})</span></button>
            <button type="button" class="mining-filter ${n==="grammar"?"active":""}" data-filter="grammar">Grammar <span class="muted small">(${d.grammar})</span></button>
          </div>
          <div class="mining-sort" role="group" aria-label="Sort order">
            <label for="mining-sort-select" class="muted small">Sort:</label>
            <select id="mining-sort-select" class="mining-sort-select">
              <option value="skill" ${o==="skill"?"selected":""}>By skill, then label</option>
              <option value="label" ${o==="label"?"selected":""}>Alphabetical (label)</option>
              <option value="count" ${o==="count"?"selected":""}>By cross-link count (desc)</option>
            </select>
          </div>
        </div>

        <ol class="mining-list">
          ${a||'<li class="placeholder">No cross-links match the current filter.</li>'}
        </ol>

        <p class="muted small" style="margin-top:24px;">
          <a href="#/authentic">\u2190 Browse the full authentic card library</a>
        </p>
      </article>
    `,y()},y=()=>{e.querySelectorAll(".mining-filter").forEach(s=>{s.addEventListener("click",()=>{n=s.dataset.filter,g()})});const a=e.querySelector("#mining-sort-select");a&&a.addEventListener("change",()=>{o=a.value,g()})};g()}export{x as renderMining};
