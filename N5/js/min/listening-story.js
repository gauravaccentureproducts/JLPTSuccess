import"./furigana.js";import"./i18n.js";import{assetUrl as h}from"./router.js";const t=n=>String(n??"").replace(/[&<>"']/g,i=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[i]);let d=null;async function f(){if(d)return d;const n=await fetch("data/listening.json");return n.ok?(d=(await n.json()).items||[],d):[]}const u={station:{en:"Station / Transit",ja:"\u3048\u304D / \u96FB\u8ECA"},cafe:{en:"Cafe",ja:"\u30AB\u30D5\u30A7"},restaurant:{en:"Restaurant",ja:"\u30EC\u30B9\u30C8\u30E9\u30F3"},shop:{en:"Shop",ja:"\u307F\u305B"},home:{en:"Home",ja:"\u3046\u3061"},office:{en:"Office",ja:"\u304B\u3044\u3057\u3083"},clinic:{en:"Clinic",ja:"\u30AF\u30EA\u30CB\u30C3\u30AF"},classroom:{en:"Classroom",ja:"\u304D\u3087\u3046\u3057\u3064"},general:{en:"Other",ja:"\u305D\u306E\u4ED6"}},y=["station","cafe","restaurant","shop","home","office","clinic","classroom","general"];async function T(n,i){const s=await f(),r=(i||"").split("/").filter(Boolean)[0]||"";return r?$(n,s,r):j(n,s)}function j(n,i){const s=new Map;for(const a of i){const o=a.ambient_context||"general";s.has(o)||s.set(o,[]),s.get(o).push(a)}const r=y.filter(a=>s.has(a)).map(a=>{const o=s.get(a)||[],l=u[a]||{en:a,ja:a};return`
        <a class="listening-story-card" href="#/listeningstory/${t(a)}">
          <h3>
            <span lang="ja">${t(l.ja)}</span>
            <span class="muted small"> \xB7 ${t(l.en)}</span>
          </h3>
          <p class="muted small">${o.length} clip(s), auto-plays in sequence</p>
        </a>
      `}).join("");n.innerHTML=`
    <article class="listening-story-root">
      <a class="back-link" href="#/listening">\u2190 Back to Listening</a>
      <h2>Story-mode listening</h2>
      <p class="page-lede">
        Pick a setting, clips auto-play one after another, like a single immersive listening session. Per-clip prompt + script reveal at the end of each.
      </p>
      <div class="listening-story-grid">${r}</div>
    </article>
  `}function $(n,i,s){const r=i.filter(e=>(e.ambient_context||"general")===s);if(!r.length){n.innerHTML=`<p>No clips for "${t(s)}". <a href="#/listeningstory">Pick another.</a></p>`;return}const a=u[s]||{en:s,ja:s},o=r.map((e,c)=>`
    <details class="listening-story-clip" id="clip-${t(e.id)}" ${c===0?"open":""} data-clip-index="${c}">
      <summary>
        <strong>${c+1}.</strong>
        <span lang="ja">${t(e.title_ja||e.id)}</span>
        <span class="muted small">${t(e.format_type||"")}</span>
      </summary>
      ${e.audio?`
        <audio class="listening-story-audio" controls preload="metadata"
               src="${t(h(e.audio))}" data-next-index="${c+1}"></audio>
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
        <span lang="ja">${t(a.ja)}</span>
        <span class="muted small"> \xB7 ${t(a.en)}</span>
      </h2>
      <p class="page-lede muted small">
        ${r.length} clips. Each auto-plays the next when finished. Expand the script after listening to check your comprehension.
      </p>
      <div class="listening-story-chain-list">${o}</div>
    </article>
  `;const l=Array.from(n.querySelectorAll("audio.listening-story-audio"));l.forEach((e,c)=>{e.addEventListener("ended",()=>{const p=parseInt(e.dataset.nextIndex||"-1",10);if(p>=0&&p<l.length){const m=l[p],g=n.querySelector(`details[data-clip-index="${p}"]`);g&&(g.open=!0),m&&setTimeout(()=>{m.play().catch(()=>{}),m.scrollIntoView({behavior:"smooth",block:"center"})},200)}})})}export{T as renderListeningStory};
