// IMP-174 (2026-05-13): Anki-importable CSV export for vocab / grammar
// / kanji corpora. Pure client-side; no network. Each export is a
// 3-column TSV (tab-separated, since vocab/grammar may contain commas
// in gloss) that Anki accepts directly via File -> Import.
//
// Column layout:
//   Front  -> the prompt side (Japanese form / pattern / kanji)
//   Back   -> the answer side (reading + gloss)
//   Notes  -> supplementary context (examples / form rules / compounds)
//
// Anki import settings to use:
//   Field separator: Tab
//   First field is sorting field
//   Allow HTML in fields: NO (we emit plain text only)
//
// Privacy: nothing leaves the device. The Blob+download pattern is the
// same one used by Settings' progress-export.

// (esc not needed — output is plain-text TSV; HTML escaping is the
// importer's responsibility.)

function tsvEscape(s) {
  if (s == null) return '';
  // Strip tabs (would break the TSV format) and collapse newlines into
  // <br>-equivalent (literal `<br>` Anki imports as line break when
  // "Allow HTML" is ON; otherwise it renders as plain "<br>"). We use a
  // space + dash instead for the conservative no-HTML case.
  return String(s).replace(/\t/g, ' ').replace(/\r?\n/g, ' / ');
}

function downloadTSV(rows, filename) {
  const tsv = rows.map(r => r.map(tsvEscape).join('\t')).join('\n');
  const blob = new Blob(['﻿' + tsv], { type: 'text/tab-separated-values;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

export async function exportVocabTSV() {
  const res = await fetch('data/vocab.json');
  const data = await res.json();
  const rows = [['Front', 'Back', 'Notes']];
  for (const v of (data.entries || [])) {
    const front = v.form || v.reading || '';
    const reading = v.reading || '';
    const gloss = v.gloss || '';
    const back = front && reading && front !== reading
      ? `${reading} - ${gloss}`
      : gloss;
    const examples = (v.examples || []).slice(0, 2)
      .map(ex => `${ex.ja || ''}${ex.translation_en ? ' = ' + ex.translation_en : ''}`)
      .join(' || ');
    rows.push([front, back, examples]);
  }
  downloadTSV(rows, `jlpt-n5-vocab-${new Date().toISOString().slice(0, 10)}.tsv`);
  return rows.length - 1;
}

export async function exportGrammarTSV() {
  const res = await fetch('data/grammar.json');
  const data = await res.json();
  const rows = [['Front', 'Back', 'Notes']];
  for (const p of (data.patterns || [])) {
    const front = p.pattern || p.title || '';
    const meaning = p.meaning_en || '';
    const form = p.form_rules?.summary || p.form_rules?.attaches_to?.join('; ') || '';
    const back = form ? `${meaning} (${form})` : meaning;
    const ex = (p.examples || []).slice(0, 2)
      .map(e => `${e.ja || ''}${e.translation_en ? ' = ' + e.translation_en : ''}`)
      .join(' || ');
    rows.push([front, back, ex]);
  }
  downloadTSV(rows, `jlpt-n5-grammar-${new Date().toISOString().slice(0, 10)}.tsv`);
  return rows.length - 1;
}

export async function exportKanjiTSV() {
  const res = await fetch('data/kanji.json');
  const data = await res.json();
  const rows = [['Front', 'Back', 'Notes']];
  for (const k of (data.entries || [])) {
    const front = k.glyph || '';
    const on = (k.on || []).map(o => typeof o === 'string' ? o : (o.reading || '')).filter(Boolean).join(', ');
    const kun = (k.kun || []).map(o => typeof o === 'string' ? o : (o.reading || '')).filter(Boolean).join(', ');
    const meanings = (k.meanings || []).join(', ');
    const back = `${meanings} | on: ${on} | kun: ${kun}`;
    const compounds = (k.n5_compounds || []).slice(0, 5)
      .map(c => `${c.form || ''} (${c.reading || ''}): ${c.gloss || ''}`)
      .join(' || ');
    rows.push([front, back, compounds]);
  }
  downloadTSV(rows, `jlpt-n5-kanji-${new Date().toISOString().slice(0, 10)}.tsv`);
  return rows.length - 1;
}

export async function exportAllCorpora() {
  const v = await exportVocabTSV();
  const g = await exportGrammarTSV();
  const k = await exportKanjiTSV();
  return { vocab: v, grammar: g, kanji: k };
}
