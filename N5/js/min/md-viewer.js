const w={privacy:{path:"PRIVACY.md",title:"Privacy"},notices:{path:"NOTICES.md",title:"Notices"}};function u(s){return String(s??"").replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e])}function L(s){const e=s.split(/\r?\n/),n=[];let t=0,o=!1,i=[],p="",l=null,h=!1;const a=()=>{l&&(n.push(`</${l}>`),l=null)},d=()=>{h&&(n.push("</blockquote>"),h=!1)};for(;t<e.length;){const c=e[t];if(c.startsWith("```")){o?(n.push(`<pre><code${p?` class="language-${u(p)}"`:""}>${u(i.join(`
`))}</code></pre>`),i=[],p="",o=!1):(a(),d(),p=c.slice(3).trim(),o=!0),t++;continue}if(o){i.push(c),t++;continue}if(/^---+$/.test(c.trim())){a(),d(),n.push("<hr>"),t++;continue}const m=c.match(/^(#{1,6})\s+(.*)$/);if(m){a(),d();const r=m[1].length;n.push(`<h${r}>${f(m[2])}</h${r}>`),t++;continue}if(c.startsWith("> ")){a(),h||(n.push("<blockquote>"),h=!0),n.push(`<p>${f(c.slice(2))}</p>`),t++;continue}else h&&d();const g=c.match(/^(\s*)[-*]\s+(.*)$/),$=c.match(/^(\s*)\d+\.\s+(.*)$/);if(g||$){const r=$?"ol":"ul",v=g||$;l&&l!==r&&a(),l||(n.push(`<${r}>`),l=r),n.push(`<li>${f(v[2])}</li>`),t++;continue}else l&&a();if(!c.trim()){t++;continue}const k=[c];for(;t+1<e.length;){const r=e[t+1];if(!r.trim()||/^(#{1,6}|\s*[-*]\s|\s*\d+\.\s|>\s|---|```)/.test(r))break;k.push(r),t++}n.push(`<p>${f(k.join(" "))}</p>`),t++}return a(),d(),o&&n.push(`<pre><code>${u(i.join(`
`))}</code></pre>`),n.join(`
`)}function f(s){let e=u(s);return e=e.replace(/`([^`]+)`/g,"<code>$1</code>"),e=e.replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>"),e=e.replace(/(^|[^*])\*([^*]+)\*(?!\*)/g,"$1<em>$2</em>"),e=e.replace(/\[([^\]]+)\]\(([^)]+)\)/g,(n,t,o)=>{if(/^(javascript|data|vbscript):/i.test(o))return t;const p=/^https?:/i.test(o)?' target="_blank" rel="noopener noreferrer"':"";return`<a href="${o}"${p}>${t}</a>`}),e}async function y(s,e){const n=w[e];if(!n){s.innerHTML=`<p>Unknown document: ${u(e)}</p>`;return}s.innerHTML=`
    <article class="md-doc-page">
      <p class="muted small"><a href="#/home">\u2190 Back home</a></p>
      <h1>${u(n.title)}</h1>
      <p class="muted small">Loading\u2026</p>
    </article>
  `;let t;try{const i=await fetch(n.path);if(!i.ok)throw new Error(`HTTP ${i.status}`);t=await i.text()}catch{s.querySelector(".md-doc-page p.muted").textContent="Could not load. Try refreshing \u2014 the file is precached and works offline once you have visited the app online.";return}const o=L(t);s.innerHTML=`
    <article class="md-doc-page">
      <p class="muted small"><a href="#/home">\u2190 Back home</a></p>
      ${o}
      <p class="muted small md-doc-source">Source: <code>${u(n.path)}</code> on GitHub.</p>
    </article>
  `}async function b(s){return y(s,"privacy")}async function T(s){return y(s,"notices")}export{T as renderNotices,b as renderPrivacy};
