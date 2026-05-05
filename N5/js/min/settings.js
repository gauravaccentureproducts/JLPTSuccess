import*as a from"./storage.js";import{setLocale as m,currentLocale as p,supportedLocales as v,t}from"./i18n.js";import"./furigana.js";const y={en:"English",vi:"Ti\u1EBFng Vi\u1EC7t",id:"Bahasa Indonesia",ne:"\u0928\u0947\u092A\u093E\u0932\u0940",zh:"\u4E2D\u6587"};async function L(o){const s=a.getSettings();o.innerHTML=`
    <h2>${t("settings.title")}</h2>
    <p class="muted">${t("settings.subtitle")}</p>

    <section class="settings-section">
      <h3>${t("settings.display")}</h3>
      <label class="settings-row">
        <span>${t("settings.language")}</span>
        <select id="set-locale">
          ${v.map(e=>`<option value="${e}" ${p()===e?"selected":""}>${y[e]||e}</option>`).join("")}
        </select>
      </label>
      <label class="settings-row">
        <span>${t("settings.theme")}</span>
        <select id="set-theme">
          <option value="system" ${(s.theme||"system")==="system"?"selected":""}>${t("settings.theme_system")}</option>
          <option value="light"  ${s.theme==="light"?"selected":""}>${t("settings.theme_light")}</option>
          <option value="dark"   ${s.theme==="dark"?"selected":""}>${t("settings.theme_dark")}</option>
        </select>
      </label>
      <label class="settings-row">
        <span>${t("settings.font_size")}</span>
        <select id="set-font">
          <option value="s"  ${s.fontSize==="s"?"selected":""}>${t("settings.font_s")}</option>
          <option value="m"  ${(s.fontSize||"m")==="m"?"selected":""}>${t("settings.font_m")}</option>
          <option value="l"  ${s.fontSize==="l"?"selected":""}>${t("settings.font_l")}</option>
          <option value="xl" ${s.fontSize==="xl"?"selected":""}>${t("settings.font_xl")}</option>
        </select>
      </label>
    </section>

    <section class="settings-section">
      <h3>${t("settings.keyboard")}</h3>
      <p class="settings-row" style="display:block;">
        <span>${t("settings.keyboard_hint")}</span>
      </p>
    </section>

    <section class="settings-section">
      <h3>${t("settings.practice")}</h3>
      <label class="settings-row">
        <span>${t("settings.test_length")}</span>
        <select id="set-test-length">
          ${[20,30,50].map(e=>`<option value="${e}" ${s.lastTestLength===e?"selected":""}>${e} ${t("settings.test_unit")}</option>`).join("")}
        </select>
      </label>
      <label class="settings-row">
        <span>${t("settings.daily_new_limit")}</span>
        <input type="number" id="set-daily-new" min="1" max="50" value="${s.dailyNewLimit||10}">
      </label>
      <label class="settings-row">
        <span>${t("settings.daily_review_cap")}</span>
        <input type="number" id="set-daily-review" min="5" max="200" value="${s.dailyReviewCap||50}">
      </label>
      <label class="settings-row">
        <span>${t("settings.daily_goal")}</span>
        <input type="number" id="set-daily-goal" min="1" max="200" value="${s.dailyGoalReviews||20}">
      </label>
      <label class="settings-row">
        <span>${t("settings.audio_speed")}</span>
        <select id="set-audio-rate">
          <option value="0.75" ${s.audioPlaybackRate===.75?"selected":""}>0.75x</option>
          <option value="1.0"  ${(s.audioPlaybackRate||1)===1?"selected":""}>1.0x</option>
          <option value="1.25" ${s.audioPlaybackRate===1.25?"selected":""}>1.25x</option>
        </select>
      </label>
      <label class="settings-row">
        <span>${t("settings.reduce_motion")}</span>
        <select id="set-reduce-motion">
          <option value="auto" ${s.reduceMotion===null||s.reduceMotion===void 0?"selected":""}>${t("settings.reduce_auto")}</option>
          <option value="on"   ${s.reduceMotion===!0?"selected":""}>${t("settings.reduce_on")}</option>
          <option value="off"  ${s.reduceMotion===!1?"selected":""}>${t("settings.reduce_off")}</option>
        </select>
      </label>
      <label class="settings-row">
        <span>
          ${t("settings.auto_furigana")}
          <span class="setting-help muted small" style="display:block; margin-top:2px;">
            ${t("settings.auto_furigana_help")}
          </span>
        </span>
        <input type="checkbox" id="set-auto-furigana" ${s.autoFurigana?"checked":""}>
      </label>
    </section>

    <section class="settings-section">
      <h3>${t("settings.data")}</h3>
      <p class="muted small">${t("settings.data_help")}</p>
      <div class="settings-actions">
        <button id="set-export">${t("settings.export")}</button>
        <button id="set-import-trigger">${t("settings.import")}</button>
        <input type="file" id="set-import-file" accept="application/json,.json" hidden>
      </div>
      <p id="set-import-msg" class="muted small" role="status" aria-live="polite"></p>
    </section>

    <section class="settings-danger-zone" aria-labelledby="danger-zone-label">
      <p class="danger-label" id="danger-zone-label">${t("settings.danger_zone")}</p>
      <div class="settings-row">
        <div>
          <span>${t("settings.reset_label")}</span>
          <p class="setting-help">${t("settings.reset_help")}</p>
        </div>
        <button id="set-reset" class="btn-danger">${t("settings.reset_btn")}</button>
      </div>
      <div id="reset-confirm" hidden class="reset-confirm-box">
        <p><strong>${t("settings.reset_confirm")}</strong></p>
        <input id="reset-phrase" type="text" autocomplete="off" placeholder="RESET">
        <div class="settings-actions">
          <button id="reset-confirm-btn" class="btn-danger" disabled>${t("settings.reset_confirm_btn")}</button>
          <button id="reset-cancel-btn" class="btn-secondary">${t("settings.cancel")}</button>
        </div>
      </div>
    </section>
  `;let u=null;const d=e=>{let n=document.getElementById("settings-saved-toast");n||(n=document.createElement("div"),n.id="settings-saved-toast",n.className="settings-saved-toast",n.setAttribute("role","status"),n.setAttribute("aria-live","polite"),document.body.appendChild(n)),n.textContent=e?`Saved: ${e}`:"Saved",n.classList.add("is-visible"),u&&clearTimeout(u),u=setTimeout(()=>{n.classList.remove("is-visible")},1800)};document.getElementById("set-locale").addEventListener("change",async e=>{await m(e.target.value),document.dispatchEvent(new CustomEvent("locale-changed")),location.reload()}),document.getElementById("set-theme").addEventListener("change",e=>{a.setSettings({theme:e.target.value}),b()}),document.getElementById("set-font").addEventListener("change",e=>{a.setSettings({fontSize:e.target.value}),h()}),document.getElementById("set-test-length").addEventListener("change",e=>{a.setSettings({lastTestLength:parseInt(e.target.value,10)}),d(`Default test length = ${e.target.value} questions`)}),document.getElementById("set-daily-new").addEventListener("change",e=>{a.setSettings({dailyNewLimit:parseInt(e.target.value,10)}),d(`Daily new-card limit = ${e.target.value}`)}),document.getElementById("set-daily-review").addEventListener("change",e=>{a.setSettings({dailyReviewCap:parseInt(e.target.value,10)}),d(`Daily review cap = ${e.target.value}`)}),document.getElementById("set-daily-goal").addEventListener("change",e=>{a.setSettings({dailyGoalReviews:parseInt(e.target.value,10)}),d(`Daily review goal = ${e.target.value}`)}),document.getElementById("set-auto-furigana").addEventListener("change",e=>{a.setSettings({autoFurigana:!!e.target.checked}),d(`Auto-furigana = ${e.target.checked?"on":"off"}`),document.dispatchEvent(new CustomEvent("furigana-rerender"))}),document.getElementById("set-audio-rate").addEventListener("change",e=>{a.setSettings({audioPlaybackRate:parseFloat(e.target.value)}),$(),d(`Audio playback speed = ${e.target.value}\xD7`)}),document.getElementById("set-reduce-motion").addEventListener("change",e=>{const n=e.target.value,i=n==="auto"?null:n==="on";a.setSettings({reduceMotion:i}),f(),d(`Reduce motion = ${n==="auto"?"Follow system":n==="on"?"Always reduce":"Never reduce"}`)}),document.getElementById("set-export").addEventListener("click",()=>{const e=a.exportProgress(),n=new Blob([JSON.stringify(e,null,2)],{type:"application/json"}),i=URL.createObjectURL(n),c=`jlpt-n5-progress-${new Date().toISOString().slice(0,10)}.json`,r=document.createElement("a");r.href=i,r.download=c,document.body.appendChild(r),r.click(),document.body.removeChild(r),URL.revokeObjectURL(i);const l=document.getElementById("set-import-msg");l&&(l.textContent=`Exported to ${c} (check your downloads folder).`,l.style.color="var(--c-success)",setTimeout(()=>{l.textContent.startsWith("Exported")&&(l.textContent="")},4e3))});const g=document.getElementById("set-import-file");document.getElementById("set-import-trigger").addEventListener("click",()=>g.click()),g.addEventListener("change",async e=>{const n=e.target.files?.[0],i=document.getElementById("set-import-msg");if(n)try{const c=await n.text(),r=JSON.parse(c),l=a.importProgress(r);i.textContent=l.message,i.style.color=l.ok?"var(--c-success)":"var(--c-error)",l.ok&&setTimeout(()=>location.reload(),800)}catch(c){i.textContent=`Import failed: ${c.message}`,i.style.color="var(--c-error)"}}),document.getElementById("set-reset").addEventListener("click",()=>{document.getElementById("reset-confirm").hidden=!1,document.getElementById("reset-phrase").focus()}),document.getElementById("reset-cancel-btn").addEventListener("click",()=>{document.getElementById("reset-confirm").hidden=!0,document.getElementById("reset-phrase").value="",document.getElementById("reset-confirm-btn").disabled=!0}),document.getElementById("reset-phrase").addEventListener("input",e=>{document.getElementById("reset-confirm-btn").disabled=e.target.value.trim()!=="RESET"}),document.getElementById("reset-confirm-btn").addEventListener("click",()=>{a.reset(),location.hash="#/learn",location.reload()})}function b(){const s=a.getSettings().theme||"system";document.documentElement.setAttribute("data-theme",s)}function h(){const o=a.getSettings();document.documentElement.setAttribute("data-font",o.fontSize||"m")}function $(){const o=a.getSettings().audioPlaybackRate||1;document.querySelectorAll("audio").forEach(s=>{try{s.playbackRate=o}catch{}})}function f(){const o=a.getSettings().reduceMotion;o===!0?document.documentElement.setAttribute("data-reduce-motion","on"):o===!1?document.documentElement.setAttribute("data-reduce-motion","off"):document.documentElement.removeAttribute("data-reduce-motion")}export{$ as applyAudioRate,h as applyFontSize,f as applyReduceMotion,b as applyTheme,L as renderSettings};
