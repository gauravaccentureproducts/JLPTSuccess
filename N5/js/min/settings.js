import*as a from"./storage.js";import{setLocale as h,currentLocale as y,supportedLocales as v,t}from"./i18n.js";import"./furigana.js";import{exportVocabTSV as b,exportGrammarTSV as f,exportKanjiTSV as $}from"./corpus-export.js";const E={en:"English",hi:"\u0939\u093F\u0928\u094D\u0926\u0940"};async function T(o){const s=a.getSettings();o.innerHTML=`
    <h2>${t("settings.title")}</h2>
    <p class="muted">${t("settings.subtitle")}</p>

    <section class="settings-section">
      <h3>${t("settings.display")}</h3>
      <label class="settings-row">
        <span>${t("settings.language")}</span>
        <select id="set-locale">
          ${v.map(e=>`<option value="${e}" ${y()===e?"selected":""}>${E[e]||e}</option>`).join("")}
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
      <!-- IMP-NEXT-1 (round-9 follow-up, 2026-05-08): Settings toggle
           for the EB-4 pedagogy recommender. Defaults ON; when off, the
           "Recommended next" card on the home page is suppressed. The
           setting is read by home.js at render time. The recommender
           code itself stays loaded (it's a small module) so toggling
           on/off is instant \u2014 no fetch, no re-init. -->
      <label class="settings-row">
        <span>
          ${t("settings.show_recommender")}
          <span class="setting-help muted small" style="display:block; margin-top:2px;">
            ${t("settings.show_recommender_help")}
          </span>
        </span>
        <input type="checkbox" id="set-show-recommender" ${s.showRecommender!==!1?"checked":""}>
      </label>
      <!-- IMP-145 (richness audit, 2026-05-09): WaniKani-style SRS gating.
           When ON, vocab cards are hidden from the unified review queue
           until ALL their prerequisite kanji are marked-known. Default
           OFF so existing learners aren't surprised. -->
      <label class="settings-row" style="margin-top:12px;">
        <span>
          WaniKani-style SRS gating
          <span class="setting-help muted small" style="display:block; margin-top:2px;">
            Hide vocab from review until every kanji in the word is marked-known.
            Forces a kanji-first study order. Off by default.
          </span>
        </span>
        <input type="checkbox" id="set-srs-gating" ${s.srsGatingEnabled?"checked":""}>
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

      <!-- IMP-174 (2026-05-13): Anki-importable corpus CSV/TSV export.
           Per-surface buttons (vocab / grammar / kanji); each generates
           a 3-column TSV (Front, Back, Notes). Anki imports natively.
           Privacy preserved: pure client-side; no network. -->
      <h4 style="margin-top:1.5rem;">Anki / CSV export</h4>
      <p class="muted small">Download corpus as tab-separated values for import into Anki or any flashcard tool. Three columns: Front, Back, Notes. Plain text only, no HTML.</p>
      <div class="settings-actions">
        <button id="set-export-vocab">Vocab TSV</button>
        <button id="set-export-grammar">Grammar TSV</button>
        <button id="set-export-kanji">Kanji TSV</button>
      </div>
      <p id="set-corpus-export-msg" class="muted small" role="status" aria-live="polite"></p>
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
  `;let g=null;const i=e=>{let n=document.getElementById("settings-saved-toast");n||(n=document.createElement("div"),n.id="settings-saved-toast",n.className="settings-saved-toast",n.setAttribute("role","status"),n.setAttribute("aria-live","polite"),document.body.appendChild(n)),n.textContent=e?`Saved: ${e}`:"Saved",n.classList.add("is-visible"),g&&clearTimeout(g),g=setTimeout(()=>{n.classList.remove("is-visible")},1800)};document.getElementById("set-locale").addEventListener("change",async e=>{await h(e.target.value),document.dispatchEvent(new CustomEvent("locale-changed")),location.reload()}),document.getElementById("set-theme").addEventListener("change",e=>{a.setSettings({theme:e.target.value}),k()}),document.getElementById("set-font").addEventListener("change",e=>{a.setSettings({fontSize:e.target.value}),w()}),document.getElementById("set-test-length").addEventListener("change",e=>{a.setSettings({lastTestLength:parseInt(e.target.value,10)}),i(`Default test length = ${e.target.value} questions`)}),document.getElementById("set-daily-new").addEventListener("change",e=>{a.setSettings({dailyNewLimit:parseInt(e.target.value,10)}),i(`Daily new-card limit = ${e.target.value}`)}),document.getElementById("set-daily-review").addEventListener("change",e=>{a.setSettings({dailyReviewCap:parseInt(e.target.value,10)}),i(`Daily review cap = ${e.target.value}`)}),document.getElementById("set-daily-goal").addEventListener("change",e=>{a.setSettings({dailyGoalReviews:parseInt(e.target.value,10)}),i(`Daily review goal = ${e.target.value}`)}),document.getElementById("set-auto-furigana").addEventListener("change",e=>{a.setSettings({autoFurigana:!!e.target.checked}),i(`Auto-furigana = ${e.target.checked?"on":"off"}`),document.dispatchEvent(new CustomEvent("furigana-rerender"))}),document.getElementById("set-show-recommender").addEventListener("change",e=>{a.setSettings({showRecommender:!!e.target.checked}),i(`Recommended-next = ${e.target.checked?"on":"off"}`)}),document.getElementById("set-srs-gating")?.addEventListener("change",e=>{a.setSettings({srsGatingEnabled:!!e.target.checked}),i(`SRS gating = ${e.target.checked?"on":"off"}`)}),document.getElementById("set-audio-rate").addEventListener("change",e=>{a.setSettings({audioPlaybackRate:parseFloat(e.target.value)}),x(),i(`Audio playback speed = ${e.target.value}\xD7`)}),document.getElementById("set-reduce-motion").addEventListener("change",e=>{const n=e.target.value,l=n==="auto"?null:n==="on";a.setSettings({reduceMotion:l}),S(),i(`Reduce motion = ${n==="auto"?"Follow system":n==="on"?"Always reduce":"Never reduce"}`)});const m=document.getElementById("set-corpus-export-msg");function u(e){m&&(m.textContent=e,m.style.color="var(--c-success)",setTimeout(()=>{m.textContent===e&&(m.textContent="")},4e3))}document.getElementById("set-export-vocab").addEventListener("click",async()=>{const e=await b();u(`Exported ${e} vocab entries to TSV. Check downloads.`)}),document.getElementById("set-export-grammar").addEventListener("click",async()=>{const e=await f();u(`Exported ${e} grammar patterns to TSV. Check downloads.`)}),document.getElementById("set-export-kanji").addEventListener("click",async()=>{const e=await $();u(`Exported ${e} kanji entries to TSV. Check downloads.`)}),document.getElementById("set-export").addEventListener("click",()=>{const e=a.exportProgress(),n=new Blob([JSON.stringify(e,null,2)],{type:"application/json"}),l=URL.createObjectURL(n),d=`jlpt-n5-progress-${new Date().toISOString().slice(0,10)}.json`,c=document.createElement("a");c.href=l,c.download=d,document.body.appendChild(c),c.click(),document.body.removeChild(c),URL.revokeObjectURL(l);const r=document.getElementById("set-import-msg");r&&(r.textContent=`Exported to ${d} (check your downloads folder).`,r.style.color="var(--c-success)",setTimeout(()=>{r.textContent.startsWith("Exported")&&(r.textContent="")},4e3))});const p=document.getElementById("set-import-file");document.getElementById("set-import-trigger").addEventListener("click",()=>p.click()),p.addEventListener("change",async e=>{const n=e.target.files?.[0],l=document.getElementById("set-import-msg");if(n)try{const d=await n.text(),c=JSON.parse(d),r=a.importProgress(c);l.textContent=r.message,l.style.color=r.ok?"var(--c-success)":"var(--c-error)",r.ok&&setTimeout(()=>location.reload(),800)}catch(d){l.textContent=`Import failed: ${d.message}`,l.style.color="var(--c-error)"}}),document.getElementById("set-reset").addEventListener("click",()=>{document.getElementById("reset-confirm").hidden=!1,document.getElementById("reset-phrase").focus()}),document.getElementById("reset-cancel-btn").addEventListener("click",()=>{document.getElementById("reset-confirm").hidden=!0,document.getElementById("reset-phrase").value="",document.getElementById("reset-confirm-btn").disabled=!0}),document.getElementById("reset-phrase").addEventListener("input",e=>{document.getElementById("reset-confirm-btn").disabled=e.target.value.trim()!=="RESET"}),document.getElementById("reset-confirm-btn").addEventListener("click",()=>{a.reset(),location.hash="#/learn",location.reload()})}function k(){const s=a.getSettings().theme||"system";document.documentElement.setAttribute("data-theme",s)}function w(){const o=a.getSettings();document.documentElement.setAttribute("data-font",o.fontSize||"m")}function x(){const o=a.getSettings().audioPlaybackRate||1;document.querySelectorAll("audio").forEach(s=>{try{s.playbackRate=o}catch{}})}function S(){const o=a.getSettings().reduceMotion;o===!0?document.documentElement.setAttribute("data-reduce-motion","on"):o===!1?document.documentElement.setAttribute("data-reduce-motion","off"):document.documentElement.removeAttribute("data-reduce-motion")}export{x as applyAudioRate,w as applyFontSize,S as applyReduceMotion,k as applyTheme,T as renderSettings};
