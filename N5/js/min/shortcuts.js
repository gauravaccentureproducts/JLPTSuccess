let e=null;function i(t){if(!t)return!1;const n=t.tagName;return!!(n==="INPUT"||n==="TEXTAREA"||n==="SELECT"||t.isContentEditable)}function l(t){const r=[...document.querySelectorAll(".choice-button:not([disabled])")][t-1];return r?(r.click(),!0):!1}function a(){const n=(document.activeElement?.matches?.("button:not([disabled])")?document.activeElement:null)||document.querySelector("button.btn-primary:not([disabled])")||[...document.querySelectorAll("button:not([disabled])")].find(r=>/^(submit|continue|next|start|finish|confirm)/i.test(r.textContent.trim()));return n?(n.click(),!0):!1}function s(){const t=[...document.querySelectorAll("button:not([disabled])")].find(n=>/^(reveal|show answer|flip)/i.test(n.textContent.trim()));return t?(t.click(),!0):!1}function u(){if(e){e.hidden=!1;return}e=document.createElement("div"),e.className="shortcuts-overlay",e.setAttribute("role","dialog"),e.setAttribute("aria-modal","true"),e.setAttribute("aria-label","Keyboard shortcuts"),e.innerHTML=`
    <div class="shortcuts-card">
      <button class="shortcuts-close" aria-label="Close">\xD7</button>
      <h3>Keyboard shortcuts</h3>
      <dl class="shortcuts-list">
        <dt><kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd> <kbd>4</kbd></dt>
        <dd>Pick multiple-choice answer</dd>
        <dt><kbd>Space</kbd></dt>
        <dd>Reveal / flip answer (where available)</dd>
        <dt><kbd>Enter</kbd></dt>
        <dd>Submit / Continue / Next</dd>
        <dt><kbd>?</kbd></dt>
        <dd>Open this cheatsheet</dd>
        <dt><kbd>Esc</kbd></dt>
        <dd>Close this overlay</dd>
        <dt><kbd>/</kbd></dt>
        <dd>Focus search (when available)</dd>
      </dl>
    </div>
  `,document.body.appendChild(e),e.querySelector(".shortcuts-close").addEventListener("click",d),e.addEventListener("click",t=>{t.target===e&&d()})}function d(){e&&(e.hidden=!0)}function c(){document.addEventListener("keydown",t=>{if(!i(t.target)&&!(t.metaKey||t.ctrlKey||t.altKey)){if(t.key==="?"){t.preventDefault(),u();return}if(t.key==="Escape"){e&&!e.hidden&&(t.preventDefault(),d());return}if(!(e&&!e.hidden)){if(["1","2","3","4"].includes(t.key)){l(parseInt(t.key,10))&&t.preventDefault();return}if(t.key===" "){s()&&t.preventDefault();return}if(t.key==="Enter"){a()&&t.preventDefault();return}}}})}export{c as initShortcuts};
