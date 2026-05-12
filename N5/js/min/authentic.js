import{renderJa as p}from"./furigana.js";import"./i18n.js";let i=null;async function m(){return i||(i=await(await fetch("data/authentic.json")).json(),i)}const g={signs:{en:"Signs",ja:"\u304B\u3093\u3070\u3093"},menu:{en:"Menu / dining",ja:"\u30E1\u30CB\u30E5\u30FC"},transit:{en:"Transit / station",ja:"\u3048\u304D"},shop:{en:"Shop / business hours",ja:"\u307F\u305B"},notice:{en:"Notices / warnings",ja:"\u304A\u3057\u3089\u305B"},weather:{en:"Weather forecast",ja:"\u3066\u3093\u304D"},hospital:{en:"Hospital / health",ja:"\u3073\u3087\u3046\u3044\u3093"},post:{en:"Post office / parcels",ja:"\u3086\u3046\u3073\u3093\u304D\u3087\u304F"},time:{en:"Time / business hours",ja:"\u3058\u304B\u3093"}},u=["signs","menu","transit","shop","notice","weather","hospital","post","time"];async function v(e){const o=(await m()).items||[],n=new Map;for(const a of u)n.set(a,[]);for(const a of o)n.has(a.category)&&n.get(a.category).push(a);const d=u.map(a=>{const r=n.get(a)||[];if(!r.length)return"";const c=g[a]||{en:a,ja:a},h=r.map(f).join("");return`
      <section class="authentic-section" id="auth-${a}">
        <h3 class="authentic-cat-title">
          <span lang="ja">${t(c.ja)}</span>
          <span class="muted small"> \xB7 ${t(c.en)}</span>
        </h3>
        <div class="authentic-grid">${h}</div>
      </section>
    `}).join("");e.innerHTML=`
    <article class="authentic-root">
      <a class="back-link" href="#/home">\u2190 Home</a>
      <h2>Authentic Japanese (real-world signs &amp; phrases)</h2>
      <p class="page-lede">
        ${o.length} starter entries you'd actually see in Japan \u2014 station signs,
        menu prices, shop hours, public-space notices. Every entry sticks to the
        N5 kanji whitelist (or kana when the kanji is N4+); the goal is real-world
        usage, not vocabulary expansion beyond N5.
      </p>
      <p class="muted small">
        Tap a card to study; click <em>Pronounce</em> to use your device's
        speech engine if available (no audio is bundled \u2014 privacy-preserving).
      </p>
      <p class="muted small">
        <a href="#/mining">\u2192 Sentence-mining index: every vocab / kanji / grammar entry linked to one or more of these cards</a>
      </p>
      ${d}
    </article>
  `,e.querySelectorAll("[data-auth-speak]").forEach(a=>{a.addEventListener("click",()=>{const r=a.dataset.authSpeak||"";if(!("speechSynthesis"in window)||!r)return;const c=new SpeechSynthesisUtterance(r);c.lang="ja-JP",c.rate=.9,window.speechSynthesis.cancel(),window.speechSynthesis.speak(c)})})}function f(e){const s=e.ja||"",o=e.reading||"";return`
    <div class="authentic-card" data-category="${t(e.category)}">
      <div class="authentic-card-ja" lang="ja">${p(s)}</div>
      ${o&&o!==s?`
        <div class="authentic-card-reading muted small" lang="ja">${t(o)}</div>
      `:""}
      <div class="authentic-card-gloss"><strong>${t(e.gloss_en||"")}</strong></div>
      ${e.gloss_hi?`<div class="authentic-card-gloss-hi muted small" lang="hi">${t(e.gloss_hi)}</div>`:""}
      ${e.context?`<p class="authentic-card-context muted small">${t(e.context)}</p>`:""}
      ${e.vocab_refs?.length?`
        <p class="authentic-card-vocab-refs muted small">
          Study vocab: ${e.vocab_refs.map(n=>`<a href="#/learn/${encodeURIComponent(n)}">${t(l(n))}</a>`).join(", ")}
        </p>
      `:""}
      ${e.kanji_refs?.length?`
        <p class="authentic-card-kanji-refs muted small">
          Study kanji: ${e.kanji_refs.map(n=>`<a href="#/kanji/${encodeURIComponent(l(n))}" lang="ja">${t(l(n))}</a>`).join(" ")}
        </p>
      `:""}
      ${e.grammar_refs?.length?`
        <p class="authentic-card-grammar-refs muted small">
          Study grammar: ${e.grammar_refs.map(n=>`<a href="#/learn/${encodeURIComponent(n)}">${t(n)}</a>`).join(", ")}
        </p>
      `:""}
      <div class="authentic-card-actions">
        <button type="button" class="btn-secondary btn-tiny" data-auth-speak="${t(s)}"
                title="Read aloud (uses your device's voice \u2014 no network call)">
          \u{1F50A} Pronounce
        </button>
      </div>
    </div>
  `}function t(e){return String(e??"").replace(/[&<>"']/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[s])}function l(e){if(typeof e!="string")return String(e);const s=e.lastIndexOf(".");return s>=0?e.slice(s+1):e}export{v as renderAuthentic};
