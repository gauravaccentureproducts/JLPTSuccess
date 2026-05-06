const k={privacy:{path:"PRIVACY.md",title:"Privacy"},notices:{path:"NOTICES.md",title:"Notices"}};function p(s){return String(s??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}function w(s){const e=s.split(/\r?\n/),n=[];let t=0,o=!1,l=[],r="",a=null,h=!1;const u=()=>{a&&(n.push(`</${a}>`),a=null)},d=()=>{h&&(n.push("</blockquote>"),h=!1)};for(;t<e.length;){const c=e[t];if(c.startsWith("```")){o?(n.push(`<pre><code${r?` class="language-${p(r)}"`:""}>${p(l.join(`
`))}</code></pre>`),l=[],r="",o=!1):(u(),d(),r=c.slice(3).trim(),o=!0),t++;continue}if(o){l.push(c),t++;continue}if(/^---+$/.test(c.trim())){u(),d(),n.push("<hr>"),t++;continue}const m=c.match(/^(#{1,6})\s+(.*)$/);if(m){u(),d();const i=m[1].length;n.push(`<h${i}>${f(m[2])}</h${i}>`),t++;continue}if(c.startsWith("> ")){u(),h||(n.push("<blockquote>"),h=!0),n.push(`<p>${f(c.slice(2))}</p>`),t++;continue}else h&&d();const g=c.match(/^(\s*)[-*]\s+(.*)$/),$=c.match(/^(\s*)\d+\.\s+(.*)$/);if(g||$){const i=$?"ol":"ul",b=g||$;a&&a!==i&&u(),a||(n.push(`<${i}>`),a=i),n.push(`<li>${f(b[2])}</li>`),t++;continue}else a&&u();if(!c.trim()){t++;continue}const v=[c];for(;t+1<e.length;){const i=e[t+1];if(!i.trim()||/^(#{1,6}|\s*[-*]\s|\s*\d+\.\s|>\s|---|```)/.test(i))break;v.push(i),t++}n.push(`<p>${f(v.join(" "))}</p>`),t++}return u(),d(),o&&n.push(`<pre><code>${p(l.join(`
`))}</code></pre>`),n.join(`
`)}function f(s){let e=p(s);return e=e.replace(/`([^`]+)`/g,"<code>$1</code>"),e=e.replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>"),e=e.replace(/(^|[^*])\*([^*]+)\*(?!\*)/g,"$1<em>$2</em>"),e=e.replace(/\[([^\]]+)\]\(([^)]+)\)/g,(n,t,o)=>{if(/^(javascript|data|vbscript):/i.test(o))return t;const r=/^https?:/i.test(o)?' target="_blank" rel="noopener noreferrer"':"";return`<a href="${o}"${r}>${t}</a>`}),e}async function y(s,e){const n=k[e];if(!n){s.innerHTML=`<p>Unknown document: ${p(e)}</p>`;return}s.innerHTML=`
    <article class="md-doc-page">
      <p class="muted small"><a href="#/home">\u2190 Back home</a></p>
      <h1>${p(n.title)}</h1>
      <p class="muted small">Loading\u2026</p>
    </article>
  `;let t;try{const r=await fetch(n.path);if(!r.ok)throw new Error(`HTTP ${r.status}`);t=await r.text()}catch{s.querySelector(".md-doc-page p.muted").textContent="Could not load. Try refreshing \u2014 the file is precached and works offline once you have visited the app online.";return}const o=w(t),l=e==="privacy"?`
    <aside class="trust-callout" aria-label="Privacy commitment">
      <strong>No login \xB7 No tracking \xB7 100% on-device \xB7 Open source</strong>
      <p>This app does NOT collect, transmit, or store any personal data on a remote server. Verifiable in the open-source code on GitHub.</p>
    </aside>
  `:"";s.innerHTML=`
    <article class="md-doc-page">
      <p class="muted small"><a href="#/home">\u2190 Back home</a></p>
      ${l}
      ${o}
      <p class="muted small md-doc-source">Source: <code>${p(n.path)}</code> on GitHub.</p>
    </article>
  `}async function L(s){return y(s,"privacy")}async function T(s){return y(s,"notices")}export{T as renderNotices,L as renderPrivacy};
