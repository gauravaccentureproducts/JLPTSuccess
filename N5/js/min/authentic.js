import{renderJa as p}from"./furigana.js";import"./i18n.js";let r=null;async function g(){return r||(r=await(await fetch("data/authentic.json")).json(),r)}const m={signs:{en:"Signs",ja:"\u304B\u3093\u3070\u3093"},menu:{en:"Menu / dining",ja:"\u30E1\u30CB\u30E5\u30FC"},transit:{en:"Transit / station",ja:"\u3048\u304D"},shop:{en:"Shop / business hours",ja:"\u307F\u305B"},notice:{en:"Notices / warnings",ja:"\u304A\u3057\u3089\u305B"},weather:{en:"Weather forecast",ja:"\u3066\u3093\u304D"},hospital:{en:"Hospital / health",ja:"\u3073\u3087\u3046\u3044\u3093"},post:{en:"Post office / parcels",ja:"\u3086\u3046\u3073\u3093\u304D\u3087\u304F"},time:{en:"Time / business hours",ja:"\u3058\u304B\u3093"}},u=["signs","menu","transit","shop","notice","weather","hospital","post","time"];async function v(e){const c=(await g()).items||[],t=new Map;for(const a of u)t.set(a,[]);for(const a of c)t.has(a.category)&&t.get(a.category).push(a);const d=u.map(a=>{const o=t.get(a)||[];if(!o.length)return"";const i=m[a]||{en:a,ja:a},h=o.map(f).join("");return`
      <section class="authentic-section" id="auth-${a}">
        <h3 class="authentic-cat-title">
          <span lang="ja">${n(i.ja)}</span>
          <span class="muted small"> \xB7 ${n(i.en)}</span>
        </h3>
        <div class="authentic-grid">${h}</div>
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
      ${d}
    </article>
  `,e.querySelectorAll("[data-auth-speak]").forEach(a=>{a.addEventListener("click",()=>{const o=a.dataset.authSpeak||"";if(!("speechSynthesis"in window)||!o)return;const i=new SpeechSynthesisUtterance(o);i.lang="ja-JP",i.rate=.9,window.speechSynthesis.cancel(),window.speechSynthesis.speak(i)})})}function f(e){const s=e.ja||"",c=e.reading||"";return`
    <div class="authentic-card" data-category="${n(e.category)}">
      <div class="authentic-card-ja" lang="ja">${p(s)}</div>
      ${c&&c!==s?`
        <div class="authentic-card-reading muted small" lang="ja">${n(c)}</div>
      `:""}
      <div class="authentic-card-gloss"><strong>${n(e.gloss_en||"")}</strong></div>
      ${e.gloss_hi?`<div class="authentic-card-gloss-hi muted small" lang="hi">${n(e.gloss_hi)}</div>`:""}
      ${e.context?`<p class="authentic-card-context muted small">${n(e.context)}</p>`:""}
      ${e.vocab_refs?.length?`
        <p class="authentic-card-vocab-refs muted small">
          Study vocab: ${e.vocab_refs.map(t=>`<a href="#/learn/${encodeURIComponent(t)}">${n(l(t))}</a>`).join(", ")}
        </p>
      `:""}
      ${e.kanji_refs?.length?`
        <p class="authentic-card-kanji-refs muted small">
          Study kanji: ${e.kanji_refs.map(t=>`<a href="#/kanji/${encodeURIComponent(l(t))}" lang="ja">${n(l(t))}</a>`).join(" ")}
        </p>
      `:""}
      <div class="authentic-card-actions">
        <button type="button" class="btn-secondary btn-tiny" data-auth-speak="${n(s)}"
                title="Read aloud (uses your device's voice \u2014 no network call)">
          \u{1F50A} Pronounce
        </button>
      </div>
    </div>
  `}function n(e){return String(e??"").replace(/[&<>"']/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[s])}function l(e){if(typeof e!="string")return String(e);const s=e.lastIndexOf(".");return s>=0?e.slice(s+1):e}export{v as renderAuthentic};
