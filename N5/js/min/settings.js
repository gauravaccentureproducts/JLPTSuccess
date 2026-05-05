import*as n from"./storage.js";import{setLocale as p,currentLocale as m,supportedLocales as g}from"./i18n.js";import"./furigana.js";const y={en:"English",vi:"Ti\u1EBFng Vi\u1EC7t",id:"Bahasa Indonesia",ne:"\u0928\u0947\u092A\u093E\u0932\u0940",zh:"\u4E2D\u6587"};async function k(a){const t=n.getSettings();a.innerHTML=`
    <h2>Settings</h2>
    <p class="muted">All settings live on this device. Nothing leaves your browser.</p>

    <section class="settings-section">
      <h3>Display</h3>
      <label class="settings-row">
        <span>UI language</span>
        <select id="set-locale">
          ${g.map(e=>`<option value="${e}" ${m()===e?"selected":""}>${y[e]||e}</option>`).join("")}
        </select>
      </label>
      <label class="settings-row">
        <span>Theme</span>
        <select id="set-theme">
          <option value="system" ${(t.theme||"system")==="system"?"selected":""}>System</option>
          <option value="light"  ${t.theme==="light"?"selected":""}>Light</option>
          <option value="dark"   ${t.theme==="dark"?"selected":""}>Dark</option>
        </select>
      </label>
      <label class="settings-row">
        <span>Font size</span>
        <select id="set-font">
          <option value="s"  ${t.fontSize==="s"?"selected":""}>S</option>
          <option value="m"  ${(t.fontSize||"m")==="m"?"selected":""}>M (default)</option>
          <option value="l"  ${t.fontSize==="l"?"selected":""}>L</option>
          <option value="xl" ${t.fontSize==="xl"?"selected":""}>XL</option>
        </select>
      </label>
    </section>

    <section class="settings-section">
      <h3>Keyboard</h3>
      <p class="settings-row" style="display:block;">
        <span>Press <kbd>?</kbd> on any page to open the keyboard-shortcuts cheatsheet.</span>
      </p>
    </section>

    <section class="settings-section">
      <h3>Practice</h3>
      <label class="settings-row">
        <span>Default test length</span>
        <select id="set-test-length">
          ${[20,30,50].map(e=>`<option value="${e}" ${t.lastTestLength===e?"selected":""}>${e} questions</option>`).join("")}
        </select>
      </label>
      <label class="settings-row">
        <span>Daily new-card limit</span>
        <input type="number" id="set-daily-new" min="1" max="50" value="${t.dailyNewLimit||10}">
      </label>
      <label class="settings-row">
        <span>Daily review cap</span>
        <input type="number" id="set-daily-review" min="5" max="200" value="${t.dailyReviewCap||50}">
      </label>
      <label class="settings-row">
        <span>Daily review goal</span>
        <input type="number" id="set-daily-goal" min="1" max="200" value="${t.dailyGoalReviews||20}">
      </label>
      <label class="settings-row">
        <span>Audio playback speed</span>
        <select id="set-audio-rate">
          <option value="0.75" ${t.audioPlaybackRate===.75?"selected":""}>0.75x</option>
          <option value="1.0"  ${(t.audioPlaybackRate||1)===1?"selected":""}>1.0x (default)</option>
          <option value="1.25" ${t.audioPlaybackRate===1.25?"selected":""}>1.25x</option>
        </select>
      </label>
      <label class="settings-row">
        <span>Reduce motion</span>
        <select id="set-reduce-motion">
          <option value="auto" ${t.reduceMotion===null||t.reduceMotion===void 0?"selected":""}>Follow system</option>
          <option value="on"   ${t.reduceMotion===!0?"selected":""}>Always reduce</option>
          <option value="off"  ${t.reduceMotion===!1?"selected":""}>Never reduce</option>
        </select>
      </label>
      <label class="settings-row">
        <span>
          Auto-furigana (experimental)
          <span class="setting-help muted small" style="display:block; margin-top:2px;">
            Adds ruby readings on a small whitelist of single-reading kanji
            (counters, days, fixed compounds). Off by default \u2014 Pass-13
            review found broader auto-ruby produced wrong context-dependent
            readings. Risk-accepted as opt-in.
          </span>
        </span>
        <input type="checkbox" id="set-auto-furigana" ${t.autoFurigana?"checked":""}>
      </label>
    </section>

    <section class="settings-section">
      <h3>Data</h3>
      <p class="muted small">Use export to back up your progress (no cloud sync). Import re-applies a saved file.</p>
      <div class="settings-actions">
        <button id="set-export">Export progress</button>
        <button id="set-import-trigger">Import progress\u2026</button>
        <input type="file" id="set-import-file" accept="application/json,.json" hidden>
      </div>
      <p id="set-import-msg" class="muted small" role="status" aria-live="polite"></p>
    </section>

    <section class="settings-danger-zone" aria-labelledby="danger-zone-label">
      <p class="danger-label" id="danger-zone-label">Danger zone</p>
      <div class="settings-row">
        <div>
          <span>Reset all progress</span>
          <p class="setting-help">Clears study history, FSRS schedule, test results, streak, known-kanji flags, and settings. Cannot be undone.</p>
        </div>
        <button id="set-reset" class="btn-danger">Reset\u2026</button>
      </div>
      <div id="reset-confirm" hidden class="reset-confirm-box">
        <p><strong>Type <code>RESET</code> to confirm.</strong> This wipes every byte of your progress on this device.</p>
        <input id="reset-phrase" type="text" autocomplete="off" placeholder="Type RESET">
        <div class="settings-actions">
          <button id="reset-confirm-btn" class="btn-danger" disabled>Confirm reset</button>
          <button id="reset-cancel-btn" class="btn-secondary">Cancel</button>
        </div>
      </div>
    </section>
  `;let r=null;const l=e=>{let s=document.getElementById("settings-saved-toast");s||(s=document.createElement("div"),s.id="settings-saved-toast",s.className="settings-saved-toast",s.setAttribute("role","status"),s.setAttribute("aria-live","polite"),document.body.appendChild(s)),s.textContent=e?`Saved: ${e}`:"Saved",s.classList.add("is-visible"),r&&clearTimeout(r),r=setTimeout(()=>{s.classList.remove("is-visible")},1800)};document.getElementById("set-locale").addEventListener("change",async e=>{await p(e.target.value),document.dispatchEvent(new CustomEvent("locale-changed")),location.reload()}),document.getElementById("set-theme").addEventListener("change",e=>{n.setSettings({theme:e.target.value}),v()}),document.getElementById("set-font").addEventListener("change",e=>{n.setSettings({fontSize:e.target.value}),b()}),document.getElementById("set-test-length").addEventListener("change",e=>{n.setSettings({lastTestLength:parseInt(e.target.value,10)}),l(`Default test length = ${e.target.value} questions`)}),document.getElementById("set-daily-new").addEventListener("change",e=>{n.setSettings({dailyNewLimit:parseInt(e.target.value,10)}),l(`Daily new-card limit = ${e.target.value}`)}),document.getElementById("set-daily-review").addEventListener("change",e=>{n.setSettings({dailyReviewCap:parseInt(e.target.value,10)}),l(`Daily review cap = ${e.target.value}`)}),document.getElementById("set-daily-goal").addEventListener("change",e=>{n.setSettings({dailyGoalReviews:parseInt(e.target.value,10)}),l(`Daily review goal = ${e.target.value}`)}),document.getElementById("set-auto-furigana").addEventListener("change",e=>{n.setSettings({autoFurigana:!!e.target.checked}),l(`Auto-furigana = ${e.target.checked?"on":"off"}`),document.dispatchEvent(new CustomEvent("furigana-rerender"))}),document.getElementById("set-audio-rate").addEventListener("change",e=>{n.setSettings({audioPlaybackRate:parseFloat(e.target.value)}),h(),l(`Audio playback speed = ${e.target.value}\xD7`)}),document.getElementById("set-reduce-motion").addEventListener("change",e=>{const s=e.target.value,o=s==="auto"?null:s==="on";n.setSettings({reduceMotion:o}),f(),l(`Reduce motion = ${s==="auto"?"Follow system":s==="on"?"Always reduce":"Never reduce"}`)}),document.getElementById("set-export").addEventListener("click",()=>{const e=n.exportProgress(),s=new Blob([JSON.stringify(e,null,2)],{type:"application/json"}),o=URL.createObjectURL(s),d=`jlpt-n5-progress-${new Date().toISOString().slice(0,10)}.json`,c=document.createElement("a");c.href=o,c.download=d,document.body.appendChild(c),c.click(),document.body.removeChild(c),URL.revokeObjectURL(o);const i=document.getElementById("set-import-msg");i&&(i.textContent=`Exported to ${d} (check your downloads folder).`,i.style.color="var(--c-success)",setTimeout(()=>{i.textContent.startsWith("Exported")&&(i.textContent="")},4e3))});const u=document.getElementById("set-import-file");document.getElementById("set-import-trigger").addEventListener("click",()=>u.click()),u.addEventListener("change",async e=>{const s=e.target.files?.[0],o=document.getElementById("set-import-msg");if(s)try{const d=await s.text(),c=JSON.parse(d),i=n.importProgress(c);o.textContent=i.message,o.style.color=i.ok?"var(--c-success)":"var(--c-error)",i.ok&&setTimeout(()=>location.reload(),800)}catch(d){o.textContent=`Import failed: ${d.message}`,o.style.color="var(--c-error)"}}),document.getElementById("set-reset").addEventListener("click",()=>{document.getElementById("reset-confirm").hidden=!1,document.getElementById("reset-phrase").focus()}),document.getElementById("reset-cancel-btn").addEventListener("click",()=>{document.getElementById("reset-confirm").hidden=!0,document.getElementById("reset-phrase").value="",document.getElementById("reset-confirm-btn").disabled=!0}),document.getElementById("reset-phrase").addEventListener("input",e=>{document.getElementById("reset-confirm-btn").disabled=e.target.value.trim()!=="RESET"}),document.getElementById("reset-confirm-btn").addEventListener("click",()=>{n.reset(),location.hash="#/learn",location.reload()})}function v(){const t=n.getSettings().theme||"system";document.documentElement.setAttribute("data-theme",t)}function b(){const a=n.getSettings();document.documentElement.setAttribute("data-font",a.fontSize||"m")}function h(){const a=n.getSettings().audioPlaybackRate||1;document.querySelectorAll("audio").forEach(t=>{try{t.playbackRate=a}catch{}})}function f(){const a=n.getSettings().reduceMotion;a===!0?document.documentElement.setAttribute("data-reduce-motion","on"):a===!1?document.documentElement.setAttribute("data-reduce-motion","off"):document.documentElement.removeAttribute("data-reduce-motion")}export{h as applyAudioRate,b as applyFontSize,f as applyReduceMotion,v as applyTheme,k as renderSettings};
