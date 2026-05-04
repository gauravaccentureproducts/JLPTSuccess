// Changelog viewer — renders CHANGELOG.md inside the app shell so the
// "What's new" link in the footer points at #/changelog instead of a raw
// .md file on GitHub. Per spec §5.11 (homepage update 2026-05-02): users
// see the changelog with the app's own typography, dark-mode tokens, etc.
//
// Markdown rendering is intentionally minimal — the changelog uses a small
// subset (headings, lists, paragraphs, inline `code` and **bold**) and we
// avoid pulling in a parser library to honour the no-third-party CSP.
//
// If we ever need full Markdown features here, swap to a vetted parser
// hosted under our own static-asset path (CSP self-only).

let cachedHtml = null;

export async function renderChangelog(container) {
  container.innerHTML = `<p class="muted">Loading…</p>`;
  if (!cachedHtml) {
    try {
      const res = await fetch('CHANGELOG.md');
      const md = await res.text();
      cachedHtml = mdToHtml(md);
    } catch (err) {
      container.innerHTML = `
        <article class="changelog">
          <h2>What's new</h2>
          <p class="muted">Could not load CHANGELOG.md (${esc(String(err))}).</p>
        </article>
      `;
      return;
    }
  }
  container.innerHTML = `
    <article class="changelog">
      ${cachedHtml}
    </article>
  `;
}

// Subset Markdown → HTML. Handles: # / ## / ### / #### headings,
// `- ` and `* ` unordered lists, blank-line paragraph breaks, `code`,
// **bold**, *italic*, [text](url) links, --- horizontal rules.
function mdToHtml(md) {
  // Normalise line endings.
  md = md.replace(/\r\n/g, '\n');

  // Process line by line, then join.
  const lines = md.split('\n');
  const out = [];
  let inList = false;
  let inCode = false;
  let inPara = false;
  const closeList = () => { if (inList) { out.push('</ul>'); inList = false; } };
  const closePara = () => { if (inPara) { out.push('</p>'); inPara = false; } };

  for (let raw of lines) {
    // Code fence
    if (/^```/.test(raw)) {
      closeList(); closePara();
      if (inCode) { out.push('</code></pre>'); inCode = false; }
      else { out.push('<pre><code>'); inCode = true; }
      continue;
    }
    if (inCode) { out.push(esc(raw)); continue; }

    // Horizontal rule
    if (/^---+\s*$/.test(raw)) {
      closeList(); closePara();
      out.push('<hr>');
      continue;
    }

    // Headings
    const h = raw.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      closeList(); closePara();
      const level = h[1].length;
      out.push(`<h${level}>${inline(h[2])}</h${level}>`);
      continue;
    }

    // Unordered list
    const li = raw.match(/^[-*]\s+(.*)$/);
    if (li) {
      closePara();
      if (!inList) { out.push('<ul>'); inList = true; }
      out.push(`<li>${inline(li[1])}</li>`);
      continue;
    }

    // Blank line — close any open block
    if (/^\s*$/.test(raw)) {
      closeList(); closePara();
      continue;
    }

    // Paragraph text
    closeList();
    if (!inPara) { out.push('<p>'); inPara = true; }
    out.push(inline(raw));
  }
  closeList(); closePara();
  if (inCode) out.push('</code></pre>');
  return out.join('\n');
}

function inline(s) {
  // Order matters: escape first, then re-introduce inline markdown features.
  s = esc(s);
  // Inline code (do this BEFORE bold/italic so backtick-wrapped chars don't conflict)
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  // Bold + italic
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');
  // Links [text](url) — only allow same-origin or full URLs we can vet
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, text, url) => {
    const safeUrl = /^(https?:|#|\/|\.\/|mailto:)/.test(url) ? url : '#';
    const ext = /^https?:/.test(safeUrl) ? ' rel="noopener noreferrer" target="_blank"' : '';
    return `<a href="${safeUrl}"${ext}>${text}</a>`;
  });
  return s;
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
