let u=null;async function d(e){if(e.innerHTML='<p class="muted">Loading\u2026</p>',!u)try{const t=await(await fetch("CHANGELOG.md")).text();u=$(t)}catch(r){e.innerHTML=`
        <article class="changelog">
          <h2>What's new</h2>
          <p class="muted">Could not load CHANGELOG.md (${h(String(r))}).</p>
        </article>
      `;return}e.innerHTML=`
    <article class="changelog">
      ${u}
    </article>
  `}function $(e){e=e.replace(/\r\n/g,`
`);const r=e.split(`
`),t=[];let s=!1,n=!1,c=!1;const i=()=>{s&&(t.push("</ul>"),s=!1)},o=()=>{c&&(t.push("</p>"),c=!1)};for(let l of r){if(/^```/.test(l)){i(),o(),n?(t.push("</code></pre>"),n=!1):(t.push("<pre><code>"),n=!0);continue}if(n){t.push(h(l));continue}if(/^---+\s*$/.test(l)){i(),o(),t.push("<hr>");continue}const a=l.match(/^(#{1,4})\s+(.*)$/);if(a){i(),o();const g=a[1].length;t.push(`<h${g}>${p(a[2])}</h${g}>`);continue}const f=l.match(/^[-*]\s+(.*)$/);if(f){o(),s||(t.push("<ul>"),s=!0),t.push(`<li>${p(f[1])}</li>`);continue}if(/^\s*$/.test(l)){i(),o();continue}i(),c||(t.push("<p>"),c=!0),t.push(p(l))}return i(),o(),n&&t.push("</code></pre>"),t.join(`
`)}function p(e){return e=h(e),e=e.replace(/`([^`]+)`/g,"<code>$1</code>"),e=e.replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>"),e=e.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g,"<em>$1</em>"),e=e.replace(/\[([^\]]+)\]\(([^)]+)\)/g,(r,t,s)=>{const n=/^(https?:|#|\/|\.\/|mailto:)/.test(s)?s:"#",c=/^https?:/.test(n)?' rel="noopener noreferrer" target="_blank"':"";return`<a href="${n}"${c}>${t}</a>`}),e}function h(e){return String(e??"").replace(/[&<>"']/g,r=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[r])}export{d as renderChangelog};
