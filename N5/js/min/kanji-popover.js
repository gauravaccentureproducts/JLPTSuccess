import*as g from"./storage.js";let i=null,a=null;async function w(){if(i)return i;try{const o=await(await fetch("data/kanji.json")).json(),e=new Map;for(const n of o.entries||[])e.set(n.glyph,n);i=e}catch{i=new Map}return i}function m(){return a||(a=document.createElement("div"),a.className="kanji-popover",a.setAttribute("role","dialog"),a.setAttribute("aria-modal","false"),a.hidden=!0,document.body.appendChild(a),document.addEventListener("click",t=>{a.hidden||a.contains(t.target)||t.target.closest("[data-glyph]")||c()}),document.addEventListener("keydown",t=>{t.key==="Escape"&&!a.hidden&&(c(),t.preventDefault())}),a)}function c(){a&&(a.hidden=!0)}async function j(t,o){await w();const e=m(),n=i.get(t),k=g.isKanjiKnown(t);if(!n)e.innerHTML=`
      <button class="kanji-popover-close" aria-label="Close">\xD7</button>
      <p><strong lang="ja">${d(t)}</strong> is not in the N5 set yet.</p>
    `;else{const s=n.additional_readings?.on||[],l=n.additional_readings?.kun||[],f=n.stroke_count?`<span class="kanji-popover-strokes" title="${n.stroke_count} strokes">${n.stroke_count}\u753B</span>`:"";e.innerHTML=`
      <button class="kanji-popover-close" aria-label="Close">\xD7</button>
      <div class="kanji-popover-header">
        <div class="kanji-popover-glyph" lang="ja">${d(n.glyph)}</div>
        ${f}
      </div>
      <dl class="kanji-popover-readings">
        ${n.on?.length?`<dt>On</dt><dd lang="ja">${n.on.map(d).join(" / ")}</dd>`:Array.isArray(n.on)?'<dt>On</dt><dd class="muted small">(none at N5)</dd>':""}
        ${n.kun?.length?`<dt>Kun</dt><dd lang="ja">${n.kun.map(d).join(" / ")}</dd>`:Array.isArray(n.kun)?'<dt>Kun</dt><dd class="muted small">(none at N5)</dd>':""}
        ${n.meanings?.length?`<dt>Meaning</dt><dd>${n.meanings.map(d).join(", ")}</dd>`:""}
      </dl>
      ${s.length||l.length?`
        <details class="kanji-popover-additional">
          <summary>Other readings (not taught at N5)</summary>
          <dl>
            ${s.length?`<dt>On</dt><dd lang="ja">${s.map(d).join(" / ")}</dd>`:""}
            ${l.length?`<dt>Kun</dt><dd lang="ja">${l.map(d).join(" / ")}</dd>`:""}
          </dl>
        </details>
      `:""}
      <label class="kanji-popover-known">
        <input type="checkbox" data-known-toggle ${k?"checked":""}>
        <span>I know this kanji</span>
      </label>
      <a class="kanji-popover-link" href="#/kanji/${encodeURIComponent(n.glyph)}">Open full kanji page \u2192</a>
    `}const p=o.getBoundingClientRect();e.hidden=!1;const u=e.getBoundingClientRect();let h=p.bottom+6+window.scrollY,r=p.left+window.scrollX;r+u.width>window.scrollX+window.innerWidth-8&&(r=window.scrollX+window.innerWidth-u.width-8),r<window.scrollX+8&&(r=window.scrollX+8),e.style.top=`${h}px`,e.style.left=`${r}px`,e.querySelector(".kanji-popover-close")?.addEventListener("click",c),e.querySelector("[data-known-toggle]")?.addEventListener("change",s=>{g.setKanjiKnown(t,s.target.checked),document.dispatchEvent(new CustomEvent("furigana-rerender"))})}function v(){document.addEventListener("click",t=>{const o=t.target.closest("[data-glyph]");if(!o||o.tagName==="A")return;const e=o.getAttribute("data-glyph");e&&(t.preventDefault(),j(e,o))})}function d(t){return String(t??"").replace(/[&<>"']/g,o=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[o])}export{v as initKanjiPopover};
