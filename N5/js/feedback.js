// Feedback page (#/feedback) — added 2026-05-02 per user direction.
//
// Why this design:
//   - The site is a static PWA, no backend, no third-party form services
//     (would conflict with the no-tracker stance documented in
//     PRIVACY.md). So feedback flows through the user's own email
//     client via a mailto: URL with subject + body pre-filled.
//   - The recipient address is built from a char-code array at submit
//     time, never serialized as a literal string in source. This means:
//       * The address doesn't appear in HTML, view-source, or any DOM
//         attribute the user can read with right-click → inspect.
//       * Naive scrapers (regex `[a-z0-9]+@[a-z0-9]+`) won't find it.
//       * It still ends up in the user's email client's To: field
//         when they click Submit, because that's the whole point.
//   - The form itself collects: Category, Title, Sender email, Message.
//     The sender email is included in the body (not the From header,
//     which is set by the user's mail client) so the recipient knows
//     where to reply.
//
// Subject format: "JLPT-Tutor Feedback - <Title> [<Category>]"

import { renderJa } from './furigana.js';

// Closed taxonomy — must agree with the labels surfaced in the form.
// To add a new category later: add to this list AND add an <option> in
// renderFeedback's HTML. The "value" goes into the email subject.
const CATEGORIES = [
  { value: 'General feedback',     label: 'General feedback' },
  { value: 'Bug report',           label: 'Bug report' },
  { value: 'Feature request',      label: 'Feature request' },
  { value: 'Content correction',   label: 'Content correction (wrong reading / translation / etc.)' },
  { value: 'Other',                label: 'Other' },
];

/**
 * Build the recipient email address from a char-code array.
 * Deliberately a function (not a module-scope const) so the literal
 * string is constructed only when the user actually clicks Submit, not
 * at module-load time. Char codes:
 *   g g a a u r r a a v v @ g m a i l . c o m
 * No emoji or fancy encoding — base-10 ASCII codepoints.
 */
function buildRecipient() {
  const c = [
    103, 103, 97, 97, 117, 114, 114, 97, 97, 118, 118,
    64,
    103, 109, 97, 105, 108, 46, 99, 111, 109,
  ];
  return String.fromCharCode.apply(null, c);
}

/**
 * Read the live version label from the footer (e.g. "v1.10.2" → "1.10.2").
 * Falls back to the major-minor placeholder if the footer hasn't rendered.
 */
function getVersion() {
  const txt = document.querySelector('.footer-meta')?.textContent || '';
  const m = txt.match(/v?(\d+\.\d+(?:\.\d+)?)/);
  return m ? m[1] : '1.10';
}

// Lightweight email-shape check for the user-supplied "from" field.
// Doesn't try to validate every RFC-5322 corner case — just catches
// obvious typos so the recipient gets a usable Reply-To.
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function renderFeedback(container) {
  container.innerHTML = `
    <article class="feedback-page">
      <header class="feedback-header">
        <h2>Feedback</h2>
        <p class="feedback-intro">
          Found a bug, a wrong reading, or an idea for the site? Send a
          note. Submitting opens your email client with the message
          pre-filled — nothing is sent through a third-party server,
          no account or tracker involved.
        </p>
      </header>

      <form id="feedback-form" class="feedback-form" novalidate>
        <label class="feedback-field">
          <span class="feedback-label">Category</span>
          <select id="fb-category" required>
            ${CATEGORIES.map(c => `<option value="${esc(c.value)}">${esc(c.label)}</option>`).join('')}
          </select>
        </label>

        <label class="feedback-field">
          <span class="feedback-label">Title <span class="feedback-required" aria-hidden="true">*</span></span>
          <input id="fb-title" type="text" required maxlength="100"
                 placeholder="Brief summary (e.g., 'Wrong kun reading on 高')"
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
                    placeholder="What happened? If it's a content issue, please cite the entry ID (e.g., n5-001, n5.kanji.私, n5.read.012)."></textarea>
          <span class="feedback-help">For bugs: include the steps to reproduce + your browser. For content corrections: cite the entry ID.</span>
        </label>

        <div class="feedback-error" id="fb-error" role="alert" aria-live="polite" hidden></div>

        <div class="feedback-actions">
          <button type="submit" class="btn-action btn-action-primary">Open email to send</button>
          <a class="btn-action btn-action-secondary" href="#/home">Cancel</a>
        </div>

        <p class="feedback-privacy">
          <strong>What gets sent:</strong> only what you typed above, plus the
          version label (v${esc(getVersion())}) so we know which
          build you're on. The page URL, your IP, and any localStorage
          contents are <strong>not</strong> included. You'll see the
          full message in your email client before sending.
        </p>
      </form>

      <div id="fb-confirmation" class="feedback-confirmation" hidden>
        <p>Your email client should have opened with the message pre-filled.
           If it didn't, your browser may not have a default mail handler set —
           in that case, copy the message above and send manually.</p>
        <a class="btn-action btn-action-secondary" href="#/home">Back to home</a>
      </div>
    </article>
  `;

  // Wire the form
  const form = document.getElementById('feedback-form');
  const errorBox = document.getElementById('fb-error');

  form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    errorBox.hidden = true;
    errorBox.textContent = '';

    const category = document.getElementById('fb-category').value.trim();
    const title    = document.getElementById('fb-title').value.trim();
    const fromAddr = document.getElementById('fb-from').value.trim();
    const body     = document.getElementById('fb-body').value.trim();

    // Validation: required + email shape
    const errors = [];
    if (!category) errors.push('Pick a category.');
    if (!title)    errors.push('Title is required.');
    if (!fromAddr) errors.push('Your email is required.');
    else if (!EMAIL_RE.test(fromAddr)) errors.push('Your email looks malformed (need name@domain.tld).');
    if (!body)     errors.push('Message is required.');

    if (errors.length) {
      errorBox.textContent = errors.join(' ');
      errorBox.hidden = false;
      // Focus the first invalid field
      if (!title)    document.getElementById('fb-title').focus();
      else if (!fromAddr || !EMAIL_RE.test(fromAddr)) document.getElementById('fb-from').focus();
      else if (!body) document.getElementById('fb-body').focus();
      return;
    }

    // Build subject + body. The recipient is constructed from char codes
    // ONLY now (at click time), so the literal address never appears in
    // the source / DOM tree before the user has explicitly initiated send.
    const subject = `JLPT-Tutor Feedback - ${title} [${category}]`;
    const fullBody = [
      `Category: ${category}`,
      `From:     ${fromAddr}`,
      `Version:  ${getVersion()}`,
      ``,
      `---`,
      ``,
      body,
      ``,
      `---`,
      `Sent from the JLPT N5 Tutor feedback form.`,
    ].join('\n');

    const mailto = (
      'mailto:' + buildRecipient()
      + '?subject=' + encodeURIComponent(subject)
      + '&body='    + encodeURIComponent(fullBody)
    );

    // Hand off to the user's mail client.
    window.location.href = mailto;

    // Show the confirmation panel immediately. If the mail client failed
    // to open, the message is still on screen and the user can copy it.
    document.getElementById('fb-confirmation').hidden = false;
  });
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
