import{renderJa as h}from"./furigana.js";import"./i18n.js";let r=null;async function p(){return r||(r=await(await fetch("data/authentic.json")).json(),r)}const g={signs:{en:"Signs",ja:"\u304B\u3093\u3070\u3093"},menu:{en:"Menu / dining",ja:"\u30E1\u30CB\u30E5\u30FC"},transit:{en:"Transit / station",ja:"\u3048\u304D"},shop:{en:"Shop / business hours",ja:"\u307F\u305B"},notice:{en:"Notices / warnings",ja:"\u304A\u3057\u3089\u305B"},weather:{en:"Weather forecast",ja:"\u3066\u3093\u304D"},hospital:{en:"Hospital / health",ja:"\u3073\u3087\u3046\u3044\u3093"},post:{en:"Post office / parcels",ja:"\u3086\u3046\u3073\u3093\u304D\u3087\u304F"},time:{en:"Time / business hours",ja:"\u3058\u304B\u3093"}},l=["signs","menu","transit","shop","notice","weather","hospital","post","time"];async function $(e){const c=(await p()).items||[],n=new Map;for(const a of l)n.set(a,[]);for(const a of c)n.has(a.category)&&n.get(a.category).push(a);const u=l.map(a=>{const o=n.get(a)||[];if(!o.length)return"";const i=g[a]||{en:a,ja:a},d=o.map(m).join("");return`
      <section class="authentic-section" id="auth-${a}">
        <h3 class="authentic-cat-title">
          <span lang="ja">${s(i.ja)}</span>
          <span class="muted small"> \xB7 ${s(i.en)}</span>
        </h3>
        <div class="authentic-grid">${d}</div>
      </section>
    `}).join("");e.innerHTML=`
    <article class="authentic-root">
      <a class="back-link" href="#/home">\u2190 Home</a>
      <h2>Authentic Japanese (real-world signs &amp; phrases)</h2>
      <p class="page-lede">
        ${c.length} starter entries you'd actually see in Japan \u2014 station signs,
        menu prices, shop hours, public-space notices. Every entry sticks to the
        N5 kanji whitelist (or kana when the kanji is N4+); the goal is real-world
        usage, not vocabulary expansion beyond N5.
      </p>
      <p class="muted small">
        Tap a card to study; click <em>Pronounce</em> to use your device's
        speech engine if available (no audio is bundled \u2014 privacy-preserving).
      </p>
      ${u}
    </article>
  `,e.querySelectorAll("[data-auth-speak]").forEach(a=>{a.addEventListener("click",()=>{const o=a.dataset.authSpeak||"";if(!("speechSynthesis"in window)||!o)return;const i=new SpeechSynthesisUtterance(o);i.lang="ja-JP",i.rate=.9,window.speechSynthesis.cancel(),window.speechSynthesis.speak(i)})})}function m(e){const t=e.ja||"",c=e.reading||"";return`
    <div class="authentic-card" data-category="${s(e.category)}">
      <div class="authentic-card-ja" lang="ja">${h(t)}</div>
      ${c&&c!==t?`
        <div class="authentic-card-reading muted small" lang="ja">${s(c)}</div>
      `:""}
      <div class="authentic-card-gloss"><strong>${s(e.gloss_en||"")}</strong></div>
      ${e.gloss_hi?`<div class="authentic-card-gloss-hi muted small" lang="hi">${s(e.gloss_hi)}</div>`:""}
      ${e.context?`<p class="authentic-card-context muted small">${s(e.context)}</p>`:""}
      ${e.vocab_refs?.length?`
        <p class="authentic-card-vocab-refs muted small">
          Study: ${e.vocab_refs.map(n=>`<a href="#/learn/${encodeURIComponent(n)}">${s(f(n))}</a>`).join(", ")}
        </p>
      `:""}
      <div class="authentic-card-actions">
        <button type="button" class="btn-secondary btn-tiny" data-auth-speak="${s(t)}"
                title="Read aloud (uses your device's voice \u2014 no network call)">
          \u{1F50A} Pronounce
        </button>
      </div>
    </div>
  `}function s(e){return String(e??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}function f(e){if(typeof e!="string")return String(e);const t=e.lastIndexOf(".");return t>=0?e.slice(t+1):e}export{$ as renderAuthentic};
