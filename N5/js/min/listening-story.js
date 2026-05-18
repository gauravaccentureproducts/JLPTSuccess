import"./furigana.js";import"./i18n.js";const t=n=>String(n??"").replace(/[&<>"']/g,i=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[i]);let d=null;async function h(){if(d)return d;const n=await fetch("data/listening.json");return n.ok?(d=(await n.json()).items||[],d):[]}const u={station:{en:"Station / Transit",ja:"\u3048\u304D / \u96FB\u8ECA"},cafe:{en:"Cafe",ja:"\u30AB\u30D5\u30A7"},restaurant:{en:"Restaurant",ja:"\u30EC\u30B9\u30C8\u30E9\u30F3"},shop:{en:"Shop",ja:"\u307F\u305B"},home:{en:"Home",ja:"\u3046\u3061"},office:{en:"Office",ja:"\u304B\u3044\u3057\u3083"},clinic:{en:"Clinic",ja:"\u30AF\u30EA\u30CB\u30C3\u30AF"},classroom:{en:"Classroom",ja:"\u304D\u3087\u3046\u3057\u3064"},general:{en:"Other",ja:"\u305D\u306E\u4ED6"}},f=["station","cafe","restaurant","shop","home","office","clinic","classroom","general"];async function b(n,i){const a=await h(),r=(i||"").split("/").filter(Boolean)[0]||"";return r?j(n,a,r):y(n,a)}function y(n,i){const a=new Map;for(const s of i){const o=s.ambient_context||"general";a.has(o)||a.set(o,[]),a.get(o).push(s)}const r=f.filter(s=>a.has(s)).map(s=>{const o=a.get(s)||[],l=u[s]||{en:s,ja:s};return`
        <a class="listening-story-card" href="#/listeningstory/${t(s)}">
          <h3>
            <span lang="ja">${t(l.ja)}</span>
            <span class="muted small"> \xB7 ${t(l.en)}</span>
          </h3>
          <p class="muted small">${o.length} clip(s) \u2014 auto-plays in sequence</p>
        </a>
      `}).join("");n.innerHTML=`
    <article class="listening-story-root">
      <a class="back-link" href="#/listening">\u2190 Back to Listening</a>
      <h2>Story-mode listening</h2>
      <p class="page-lede">
        Pick a setting \u2014 clips auto-play one after another, like a single immersive listening session. Per-clip prompt + script reveal at the end of each.
      </p>
      <div class="listening-story-grid">${r}</div>
    </article>
  `}function j(n,i,a){const r=i.filter(e=>(e.ambient_context||"general")===a);if(!r.length){n.innerHTML=`<p>No clips for "${t(a)}". <a href="#/listeningstory">Pick another.</a></p>`;return}const s=u[a]||{en:a,ja:a},o=r.map((e,c)=>`
    <details class="listening-story-clip" id="clip-${t(e.id)}" ${c===0?"open":""} data-clip-index="${c}">
      <summary>
        <strong>${c+1}.</strong>
        <span lang="ja">${t(e.title_ja||e.id)}</span>
        <span class="muted small">${t(e.format_type||"")}</span>
      </summary>
      ${e.audio?`
        <audio class="listening-story-audio" controls preload="metadata"
               src="${t(e.audio)}" data-next-index="${c+1}"></audio>
      `:""}
      <details class="listening-story-script muted small">
        <summary>Show script + prompt</summary>
        ${e.prompt_ja?`<p lang="ja"><strong>Prompt:</strong> ${t(e.prompt_ja)}</p>`:""}
        ${e.script_ja?`<p lang="ja">${t(e.script_ja).replace(/\n/g,"<br>")}</p>`:""}
        ${e.correctAnswer?`<p lang="ja"><strong>Answer:</strong> ${t(e.correctAnswer)}</p>`:""}
      </details>
    </details>
  `).join("");n.innerHTML=`
    <article class="listening-story-chain">
      <a class="back-link" href="#/listeningstory">\u2190 Pick another story</a>
      <h2>
        <span lang="ja">${t(s.ja)}</span>
        <span class="muted small"> \xB7 ${t(s.en)}</span>
      </h2>
      <p class="page-lede muted small">
        ${r.length} clips. Each auto-plays the next when finished. Expand the script after listening to check your comprehension.
      </p>
      <div class="listening-story-chain-list">${o}</div>
    </article>
  `;const l=Array.from(n.querySelectorAll("audio.listening-story-audio"));l.forEach((e,c)=>{e.addEventListener("ended",()=>{const p=parseInt(e.dataset.nextIndex||"-1",10);if(p>=0&&p<l.length){const m=l[p],g=n.querySelector(`details[data-clip-index="${p}"]`);g&&(g.open=!0),m&&setTimeout(()=>{m.play().catch(()=>{}),m.scrollIntoView({behavior:"smooth",block:"center"})},200)}})})}export{b as renderListeningStory};
