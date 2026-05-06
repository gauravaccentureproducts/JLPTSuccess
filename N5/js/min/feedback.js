import"./furigana.js";const p=[{value:"General feedback",label:"General feedback"},{value:"Bug report",label:"Bug report"},{value:"Feature request",label:"Feature request"},{value:"Content correction",label:"Content correction (wrong reading / translation / etc.)"},{value:"Other",label:"Other"}];function h(){const t=[103,103,97,97,117,114,114,97,97,118,118,64,103,109,97,105,108,46,99,111,109];return String.fromCharCode.apply(null,t)}function c(){const a=(document.querySelector(".footer-meta")?.textContent||"").match(/v?(\d+\.\d+(?:\.\d+)?)/);return a?a[1]:"1.10"}const u=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;function k(t){t.innerHTML=`
    <article class="feedback-page">
      <header class="feedback-header">
        <h2>Feedback</h2>
        <p class="feedback-intro">
          Found a bug, a wrong reading, or an idea for the site? Send a
          note. Submitting opens your email client with the message
          pre-filled - nothing is sent through a third-party server,
          no account or tracker involved.
        </p>
      </header>

      <form id="feedback-form" class="feedback-form" novalidate>
        <label class="feedback-field">
          <span class="feedback-label">Category</span>
          <select id="fb-category" required>
            ${p.map(r=>`<option value="${d(r.value)}">${d(r.label)}</option>`).join("")}
          </select>
        </label>

        <label class="feedback-field">
          <span class="feedback-label">Title <span class="feedback-required" aria-hidden="true">*</span></span>
          <input id="fb-title" type="text" required maxlength="100"
                 placeholder="Brief summary (e.g., 'Wrong kun reading on \u9AD8')"
                 autocomplete="off">
          <span class="feedback-help">A one-line summary; appears in the email subject.</span>
        </label>

        <label class="feedback-field">
          <span class="feedback-label">Your email <span class="feedback-required" aria-hidden="true">*</span></span>
          <input id="fb-from" type="email" required maxlength="120"
                 placeholder="you@example.com"
                 autocomplete="email">
          <span class="feedback-help">So we can reply if needed. Not stored anywhere on this device.</span>
        </label>

        <label class="feedback-field">
          <span class="feedback-label">Message <span class="feedback-required" aria-hidden="true">*</span></span>
          <textarea id="fb-body" required rows="8" maxlength="4000"
                    placeholder="What happened? If it's a content issue, please cite the entry ID (e.g., n5-001, n5.kanji.\u79C1, n5.read.012)."></textarea>
          <span class="feedback-help">For bugs: include the steps to reproduce + your browser. For content corrections: cite the entry ID.</span>
        </label>

        <div class="feedback-error" id="fb-error" role="alert" aria-live="polite" hidden></div>

        <div class="feedback-actions">
          <button type="submit" class="btn-action btn-action-primary">Open email to send</button>
          <a class="btn-action btn-action-secondary" href="#/home">Cancel</a>
        </div>

        <p class="feedback-privacy">
          <strong>What gets sent:</strong> only what you typed above, plus the
          version label (v${d(c())}) so we know which
          build you're on. The page URL, your IP, and any localStorage
          contents are <strong>not</strong> included. You'll see the
          full message in your email client before sending.
        </p>
      </form>

      <div id="fb-confirmation" class="feedback-confirmation" hidden>
        <p>Your email client should have opened with the message pre-filled.
           If it didn't, your browser may not have a default mail handler set -
           in that case, copy the message above and send manually.</p>
        <a class="btn-action btn-action-secondary" href="#/home">Back to home</a>
      </div>
    </article>
  `;const a=document.getElementById("feedback-form"),o=document.getElementById("fb-error");a.addEventListener("submit",r=>{r.preventDefault(),o.hidden=!0,o.textContent="";const l=document.getElementById("fb-category").value.trim(),s=document.getElementById("fb-title").value.trim(),n=document.getElementById("fb-from").value.trim(),i=document.getElementById("fb-body").value.trim(),e=[];if(l||e.push("Pick a category."),s||e.push("Title is required."),n?u.test(n)||e.push("Your email looks malformed (need name@domain.tld)."):e.push("Your email is required."),i||e.push("Message is required."),e.length){o.textContent=e.join(" "),o.hidden=!1,s?!n||!u.test(n)?document.getElementById("fb-from").focus():i||document.getElementById("fb-body").focus():document.getElementById("fb-title").focus();return}const f=`JLPT-Tutor Feedback - ${s} [${l}]`,b=[`Category: ${l}`,`From:     ${n}`,`Version:  ${c()}`,"","---","",i,"","---","Sent from the JLPT N5 Tutor feedback form."].join(`
`),m="mailto:"+h()+"?subject="+encodeURIComponent(f)+"&body="+encodeURIComponent(b);window.location.href=m,document.getElementById("fb-confirmation").hidden=!1})}function d(t){return String(t??"").replace(/[&<>"']/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[a])}export{k as renderFeedback};
