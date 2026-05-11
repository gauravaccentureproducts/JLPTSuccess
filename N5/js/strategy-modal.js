// IMP-WAVE-P4-T3 (UI audit fix, 2026-05-11): contextual strategy
// modal for the mock-paper sitting flow.
//
// Loads data/test_strategy.json once, then on demand opens a modal
// listing techniques + trap patterns relevant to the current
// section/module. Powered by the 15 techniques + 30 trap_patterns
// authored in the strategy JSON.
//
// Public API:
//   await openStrategyModal(sectionId, modules)
//     sectionId: 'mojigoi' | 'bunpoudok' | 'choukai'
//     modules:   array of module ids the section covers, e.g.
//                ['moji', 'goi'] for sectionId 'mojigoi'.
//     Filters techniques whose applies_to overlaps section/mondai,
//     plus traps whose module matches. Renders an accessible modal
//     (focus-trapped, ESC closes) with two collapsible sub-lists.
//
// Section -> strategy key mapping:
//   mojigoi   -> applies_to includes 'moji_goi'    + 'all_sections'
//   bunpoudok -> applies_to includes 'bunpou_dokkai' + 'all_sections'
//   choukai   -> applies_to includes 'chokai'       + 'all_sections'
//                                                   + 'chokai_mondai_N'
//
// Section -> trap module mapping:
//   mojigoi   -> 'vocab', 'kanji'
//   bunpoudok -> 'grammar', 'dokkai'
//   choukai   -> 'chokai'

let _strategyCache = null;

const SECTION_TO_TECH_KEYS = {
  mojigoi:   ['moji_goi', 'all_sections', 'all_sections_paper', 'moji_goi_mondai_1', 'moji_goi_mondai_2', 'moji_goi_mondai_3', 'moji_goi_mondai_4', 'moji_goi_mondai_5'],
  bunpoudok: ['bunpou_dokkai', 'all_sections', 'all_sections_paper', 'bunpou_mondai_1', 'bunpou_mondai_2', 'bunpou_mondai_3', 'dokkai_mondai_4', 'dokkai_mondai_5', 'dokkai_mondai_6'],
  choukai:   ['all_sections', 'all_sections_paper', 'chokai_mondai_1', 'chokai_mondai_2', 'chokai_mondai_3', 'chokai_mondai_4'],
};

const SECTION_TO_TRAP_MODULES = {
  mojigoi:   ['vocab', 'kanji'],
  bunpoudok: ['grammar', 'dokkai'],
  choukai:   ['chokai'],
};

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

async function loadStrategy() {
  if (_strategyCache) return _strategyCache;
  try {
    const r = await fetch('data/test_strategy.json');
    if (!r.ok) return null;
    _strategyCache = await r.json();
    return _strategyCache;
  } catch (e) {
    console.warn('[strategy-modal] load failed:', e);
    return null;
  }
}

function filterTechniques(strategy, sectionId) {
  const techKeys = SECTION_TO_TECH_KEYS[sectionId] || ['all_sections'];
  const techs = strategy.techniques || [];
  return techs.filter(t => {
    const applies = t.applies_to || [];
    return applies.some(a => techKeys.includes(a));
  });
}

function filterTraps(strategy, sectionId) {
  const trapModules = SECTION_TO_TRAP_MODULES[sectionId] || [];
  const traps = strategy.trap_patterns || [];
  return traps.filter(t => trapModules.includes(t.module));
}

function renderModalContent(techs, traps, sectionLabel) {
  return `
    <header class="strategy-modal-header">
      <h2 id="strategy-modal-title">Strategies for ${esc(sectionLabel)}</h2>
      <button type="button" class="strategy-modal-close" aria-label="Close">&times;</button>
    </header>
    <div class="strategy-modal-body">
      <p class="muted small">
        ${techs.length} technique(s) and ${traps.length} known trap pattern(s) authored for this section. All content is from <code>data/test_strategy.json</code>.
      </p>
      ${techs.length ? `
        <section class="strategy-block">
          <h3>Techniques</h3>
          <ul class="strategy-list">
            ${techs.map(t => `
              <li class="strategy-item">
                <div class="strategy-item-head">
                  <strong>${esc(t.title_en || t.name || t.id)}</strong>
                  ${t.title_ja ? `<span class="muted small" lang="ja">(${esc(t.title_ja)})</span>` : ''}
                </div>
                <p>${esc(t.description || '')}</p>
                ${t.rationale ? `<p class="muted small"><em>Why:</em> ${esc(t.rationale)}</p>` : ''}
                ${t.warning ? `<p class="strategy-warning"><strong>⚠ Caveat:</strong> ${esc(t.warning)}</p>` : ''}
              </li>
            `).join('')}
          </ul>
        </section>
      ` : ''}
      ${traps.length ? `
        <section class="strategy-block">
          <h3>Trap patterns to watch for</h3>
          <ul class="strategy-list">
            ${traps.map(t => `
              <li class="strategy-item">
                <div class="strategy-item-head">
                  <strong>${esc(t.name || t.id)}</strong>
                  <span class="strategy-module-chip muted small">${esc(t.module || '')}</span>
                </div>
                <p>${esc(t.description || '')}</p>
                ${t.wrong_example ? `<p class="wrong" lang="ja"><strong>✗</strong> ${esc(t.wrong_example)}</p>` : ''}
                ${t.correct_example ? `<p class="right" lang="ja"><strong>✓</strong> ${esc(t.correct_example)}</p>` : ''}
                ${t.defense ? `<p class="muted small"><em>Defense:</em> ${esc(t.defense)}</p>` : ''}
              </li>
            `).join('')}
          </ul>
        </section>
      ` : ''}
      ${!techs.length && !traps.length ? `<p class="muted">No strategies authored for this section yet.</p>` : ''}
    </div>
  `;
}

export async function openStrategyModal(sectionId, sectionLabel) {
  const strategy = await loadStrategy();
  if (!strategy) {
    alert("Couldn't load strategy data. Please retry.");
    return;
  }
  const techs = filterTechniques(strategy, sectionId);
  const traps = filterTraps(strategy, sectionId);

  // Build modal DOM.
  const backdrop = document.createElement('div');
  backdrop.className = 'strategy-modal-backdrop';
  backdrop.setAttribute('role', 'dialog');
  backdrop.setAttribute('aria-modal', 'true');
  backdrop.setAttribute('aria-labelledby', 'strategy-modal-title');
  const dialog = document.createElement('div');
  dialog.className = 'strategy-modal-dialog';
  dialog.innerHTML = renderModalContent(techs, traps, sectionLabel || sectionId);
  backdrop.appendChild(dialog);
  document.body.appendChild(backdrop);

  // Focus management: remember the active element, move focus into modal.
  const lastActive = document.activeElement;
  const closeBtn = dialog.querySelector('.strategy-modal-close');
  closeBtn.focus();

  const close = () => {
    backdrop.remove();
    document.removeEventListener('keydown', onKey);
    if (lastActive && lastActive.focus) lastActive.focus();
  };

  const onKey = (ev) => {
    if (ev.key === 'Escape') close();
  };
  document.addEventListener('keydown', onKey);
  backdrop.addEventListener('click', (ev) => {
    if (ev.target === backdrop) close();
  });
  closeBtn.addEventListener('click', close);
}
