import*as k from"./storage.js";import{currentLocale as w}from"./i18n.js";function j(n){const a=w();if(a&&a!=="en"){const t=n[`meanings_${a}`];if(Array.isArray(t)&&t.length)return t}return n.meanings||[]}let d=null,o=null;async function v(){if(d)return d;try{const a=await(await fetch("data/kanji.json")).json(),t=new Map;for(const e of a.entries||[])t.set(e.glyph,e);d=t}catch{d=new Map}return d}function y(){return o||(o=document.createElement("div"),o.className="kanji-popover",o.setAttribute("role","dialog"),o.setAttribute("aria-modal","false"),o.hidden=!0,document.body.appendChild(o),document.addEventListener("click",n=>{o.hidden||o.contains(n.target)||n.target.closest("[data-glyph]")||c()}),document.addEventListener("keydown",n=>{n.key==="Escape"&&!o.hidden&&(c(),n.preventDefault())}),o)}function c(){o&&(o.hidden=!0)}async function $(n,a){await v();const t=y(),e=d.get(n),h=k.isKanjiKnown(n);if(!e)t.innerHTML=`
      <button class="kanji-popover-close" aria-label="Close">\xD7</button>
      <p><strong lang="ja">${i(n)}</strong> is not in the N5 set yet.</p>
    `;else{const s=e.additional_readings?.on||[],l=e.additional_readings?.kun||[],m=e.stroke_count?`<span class="kanji-popover-strokes" title="${e.stroke_count} strokes">${e.stroke_count}\u753B</span>`:"";t.innerHTML=`
      <button class="kanji-popover-close" aria-label="Close">\xD7</button>
      <div class="kanji-popover-header">
        <div class="kanji-popover-glyph" lang="ja">${i(e.glyph)}</div>
        ${m}
      </div>
      <dl class="kanji-popover-readings">
        ${e.on?.length?`<dt>On</dt><dd lang="ja">${e.on.map(i).join(" / ")}</dd>`:Array.isArray(e.on)?'<dt>On</dt><dd class="muted small">(none at N5)</dd>':""}
        ${e.kun?.length?`<dt>Kun</dt><dd lang="ja">${e.kun.map(i).join(" / ")}</dd>`:Array.isArray(e.kun)?'<dt>Kun</dt><dd class="muted small">(none at N5)</dd>':""}
        ${(()=>{const g=j(e);return g.length?`<dt>Meaning</dt><dd>${g.map(i).join(", ")}</dd>`:""})()}
      </dl>
      ${s.length||l.length?`
        <details class="kanji-popover-additional">
          <summary>Other readings (not taught at N5)</summary>
          <dl>
            ${s.length?`<dt>On</dt><dd lang="ja">${s.map(i).join(" / ")}</dd>`:""}
            ${l.length?`<dt>Kun</dt><dd lang="ja">${l.map(i).join(" / ")}</dd>`:""}
          </dl>
        </details>
      `:""}
      <label class="kanji-popover-known">
        <input type="checkbox" data-known-toggle ${h?"checked":""}>
        <span>I know this kanji</span>
      </label>
      <a class="kanji-popover-link" href="#/kanji/${encodeURIComponent(e.glyph)}">Open full kanji page \u2192</a>
    `}const p=a.getBoundingClientRect();t.hidden=!1;const u=t.getBoundingClientRect();let f=p.bottom+6+window.scrollY,r=p.left+window.scrollX;r+u.width>window.scrollX+window.innerWidth-8&&(r=window.scrollX+window.innerWidth-u.width-8),r<window.scrollX+8&&(r=window.scrollX+8),t.style.top=`${f}px`,t.style.left=`${r}px`,t.querySelector(".kanji-popover-close")?.addEventListener("click",c),t.querySelector("[data-known-toggle]")?.addEventListener("change",s=>{k.setKanjiKnown(n,s.target.checked),document.dispatchEvent(new CustomEvent("furigana-rerender"))})}function A(){document.addEventListener("click",n=>{const a=n.target.closest("[data-glyph]");if(!a||a.tagName==="A")return;const t=a.getAttribute("data-glyph");t&&(n.preventDefault(),$(t,a))})}function i(n){return String(n??"").replace(/[&<>"']/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[a])}export{A as initKanjiPopover};
