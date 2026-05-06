// ISSUE-055 (round-7 deferred → fixed 2026-05-06): in-app markdown
// viewer for PRIVACY.md + NOTICES.md.
//
// Background: footer links previously served PRIVACY.md / NOTICES.md
// as raw text/markdown. Modern Chrome / Firefox render them as plain
// text (acceptable but ugly); mobile Safari downloads them. Result:
// trust-surface friction on the niche-N2 (privacy posture credibility)
// and niche-N3 (institutional adoption) flows.
//
// Fix: render the markdown inline via a minimal, dependency-free
// markdown subset that covers what PRIVACY.md / NOTICES.md actually
// use (h1-h3, paragraphs, lists, links, code blocks, blockquotes,
// emphasis). No third-party library — niche-N2 privacy contract
// forbids new third-party scripts.
//
// API:
//   renderPrivacy(container)  → fetches PRIVACY.md + renders into container
//   renderNotices(container)  → fetches NOTICES.md + renders into container

const MD_FILES = {
  privacy: { path: 'PRIVACY.md', title: 'Privacy' },
  notices: { path: 'NOTICES.md', title: 'Notices' },
};

function _esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

/**
 * Minimal markdown → HTML renderer. Handles the subset that PRIVACY.md
 * + NOTICES.md actually use:
 *   # / ## / ###   headings
 *   - / *          unordered lists
 *   1.             ordered lists
 *   ```            fenced code blocks
 *   `code`         inline code
 *   > quote        blockquote
 *   **bold**       bold
 *   *italic*       italic
 *   [text](url)    links
 *   horizontal rule (---)
 *   plain paragraph (any other line)
 *
 * Output is HTML-escaped at the leaf level. No raw HTML passthrough.
 */
function renderMarkdown(md) {
  const lines = md.split(/\r?\n/);
  const out = [];
  let i = 0;
  let inCode = false;
  let codeBuf = [];
  let codeLang = '';
  let inList = null;  // 'ul' | 'ol' | null
  let inQuote = false;

  const closeList = () => {
    if (inList) { out.push(`</${inList}>`); inList = null; }
  };
  const closeQuote = () => {
    if (inQuote) { out.push('</blockquote>'); inQuote = false; }
  };

  while (i < lines.length) {
    const line = lines[i];

    // Fenced code blocks
    if (line.startsWith('```')) {
      if (inCode) {
        out.push(`<pre><code${codeLang ? ` class="language-${_esc(codeLang)}"` : ''}>${_esc(codeBuf.join('\n'))}</code></pre>`);
        codeBuf = []; codeLang = ''; inCode = false;
      } else {
        closeList(); closeQuote();
        codeLang = line.slice(3).trim();
        inCode = true;
      }
      i++; continue;
    }
    if (inCode) { codeBuf.push(line); i++; continue; }

    // Horizontal rule
    if (/^---+$/.test(line.trim())) {
      closeList(); closeQuote();
      out.push('<hr>'); i++; continue;
    }

    // Headings
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      closeList(); closeQuote();
      const level = h[1].length;
      out.push(`<h${level}>${_renderInline(h[2])}</h${level}>`);
      i++; continue;
    }

    // Blockquote
    if (line.startsWith('> ')) {
      closeList();
      if (!inQuote) { out.push('<blockquote>'); inQuote = true; }
      out.push(`<p>${_renderInline(line.slice(2))}</p>`);
      i++; continue;
    } else if (inQuote) {
      closeQuote();
    }

    // Lists
    const ul = line.match(/^(\s*)[-*]\s+(.*)$/);
    const ol = line.match(/^(\s*)\d+\.\s+(.*)$/);
    if (ul || ol) {
      const tag = ol ? 'ol' : 'ul';
      const m = ul || ol;
      if (inList && inList !== tag) closeList();
      if (!inList) { out.push(`<${tag}>`); inList = tag; }
      out.push(`<li>${_renderInline(m[2])}</li>`);
      i++; continue;
    } else if (inList) {
      closeList();
    }

    // Empty line
    if (!line.trim()) { i++; continue; }

    // Plain paragraph (collect consecutive non-empty / non-block lines)
    const paraLines = [line];
    while (i + 1 < lines.length) {
      const next = lines[i + 1];
      if (!next.trim()) break;
      if (/^(#{1,6}|\s*[-*]\s|\s*\d+\.\s|>\s|---|```)/.test(next)) break;
      paraLines.push(next);
      i++;
    }
    out.push(`<p>${_renderInline(paraLines.join(' '))}</p>`);
    i++;
  }
  closeList(); closeQuote();
  if (inCode) {
    // Unclosed code fence — best effort
    out.push(`<pre><code>${_esc(codeBuf.join('\n'))}</code></pre>`);
  }
  return out.join('\n');
}

function _renderInline(s) {
  // Order matters: handle code spans first to avoid double-formatting.
  let out = _esc(s);
  // Inline code: `code`
  out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
  // Bold: **text**
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  // Italic: *text* (but not part of **)
  out = out.replace(/(^|[^*])\*([^*]+)\*(?!\*)/g, '$1<em>$2</em>');
  // Links: [text](url) — only allow http/https/relative paths (no javascript:)
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (m, text, url) => {
    if (/^(javascript|data|vbscript):/i.test(url)) return text;  // strip dangerous
    const ext = /^https?:/i.test(url);
    const attrs = ext ? ' target="_blank" rel="noopener noreferrer"' : '';
    return `<a href="${url}"${attrs}>${text}</a>`;
  });
  return out;
}

async function _renderInto(container, key) {
  const cfg = MD_FILES[key];
  if (!cfg) {
    container.innerHTML = `<p>Unknown document: ${_esc(key)}</p>`;
    return;
  }
  container.innerHTML = `
    <article class="md-doc-page">
      <p class="muted small"><a href="#/home">← Back home</a></p>
      <h1>${_esc(cfg.title)}</h1>
      <p class="muted small">Loading…</p>
    </article>
  `;
  let md;
  try {
    const res = await fetch(cfg.path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    md = await res.text();
  } catch (err) {
    container.querySelector('.md-doc-page p.muted').textContent =
      'Could not load. Try refreshing — the file is precached and works offline once you have visited the app online.';
    return;
  }
  const html = renderMarkdown(md);
  container.innerHTML = `
    <article class="md-doc-page">
      <p class="muted small"><a href="#/home">← Back home</a></p>
      ${html}
      <p class="muted small md-doc-source">Source: <code>${_esc(cfg.path)}</code> on GitHub.</p>
    </article>
  `;
}

export async function renderPrivacy(container) {
  return _renderInto(container, 'privacy');
}

export async function renderNotices(container) {
  return _renderInto(container, 'notices');
}
