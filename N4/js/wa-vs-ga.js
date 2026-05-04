// は vs が module (Brief §2.6)
// Dedicated lesson + minimal-pair drill covering all five core uses.
import { renderJa } from './furigana.js';
import { matchesAnswer } from './normalize.js';

const PAIRS = [
  {
    use: 'Topic vs new info',
    explanation_en: 'は marks a TOPIC the listener already knows. が marks NEW info - often as the answer to a question.',
    a: { sentence: 'わたし___ がくせいです。', particle: 'は', context: 'Self-introduction; the listener doesn\'t already know who you are, but in self-intro context the speaker is implicitly the topic.' },
    b: { sentence: 'だれ___ がくせいですか。', particle: 'が', context: 'Who is the student? - question word + が.' },
  },
  {
    use: 'Stative predicate',
    explanation_en: 'すき, きらい, わかる, できる, ある, いる, ほしい, 上手, 下手 ALL take が, never を.',
    a: { sentence: 'ねこ___ すきです。', particle: 'が', context: 'すき (like) is stative → が, never を.' },
    b: { sentence: '日本語___ わかりますか。', particle: 'が', context: 'わかる takes が.' },
  },
  {
    use: 'Existence',
    explanation_en: 'There-is sentences put the EXISTING THING with が and the location with に.',
    a: { sentence: 'へやに ねこ___ います。', particle: 'が', context: 'The cat (new info) is in the room.' },
    b: { sentence: 'ねこ___ どこに いますか。', particle: 'は', context: 'As for the cat (already-known topic), where is it? Different framing - topic-first.' },
  },
  {
    use: 'Neutral description',
    explanation_en: 'Pure description of what one observes uses が. (雨が ふっている = "It\'s raining" - no topic implied.)',
    a: { sentence: 'あめ___ ふっています。', particle: 'が', context: 'Neutral description - there\'s rain falling.' },
    b: { sentence: 'きょう___ あついです。', particle: 'は', context: '"As for today, it\'s hot" - topical comment about a known frame (today).' },
  },
  {
    use: 'XはYが (X has Y)',
    explanation_en: 'The "X has Y" / "X is Y-ish" pattern combines both: X (topic) は + Y (what) が + adjective.',
    a: { sentence: 'ぞう___ はな___ ながいです。', particle: ['は', 'が'], context: 'As for the elephant, the nose is long. (= elephants have long noses)' },
    b: { sentence: 'わたし___ かのじょ___ います。', particle: ['は', 'が'], context: 'I have a girlfriend. (Topic: I; what exists: a girlfriend.)' },
  },
];

let drillState = null;

export async function renderWaGa(container) {
  container.innerHTML = `
    <h2>は vs が - five uses</h2>
    <p>The は / が distinction is the single most-tested grammar point at N5. Five core uses are below, each with a minimal pair.</p>

    ${renderUses()}
    ${renderDrillSection()}
  `;
  wireDrill(container);
}

function renderUses() {
  return PAIRS.map((pair, idx) => `
    <section class="waga-use">
      <h3>${idx + 1}. ${esc(pair.use)}</h3>
      <p>${esc(pair.explanation_en)}</p>
      <div class="waga-pair">
        <div class="waga-side">
          <p class="waga-sentence">${renderJa(fillBlank(pair.a.sentence, pair.a.particle))}</p>
          <p class="waga-context muted small">${esc(pair.a.context)}</p>
        </div>
        <div class="waga-side">
          <p class="waga-sentence">${renderJa(fillBlank(pair.b.sentence, pair.b.particle))}</p>
          <p class="waga-context muted small">${esc(pair.b.context)}</p>
        </div>
      </div>
    </section>
  `).join('');
}

function fillBlank(sentence, particle) {
  if (Array.isArray(particle)) {
    let i = 0;
    return sentence.replace(/___/g, () => particle[i++] ?? '___');
  }
  return sentence.split('___').join(particle);
}

function renderDrillSection() {
  if (!drillState) {
    return `
      <section class="waga-drill">
        <h3>Minimal-pair drill</h3>
        <p>Type the missing particle (は or が) for each blank, then click Check. Both translations are shown after - focus on the meaning difference.</p>
        <button id="waga-start" class="btn-primary">Start drill</button>
      </section>
    `;
  }
  const { current, feedback, score, total } = drillState;
  const blanks = Array.isArray(current.particle) ? current.particle.length : 1;
  const inputs = Array.from({length: blanks}, (_, i) => `
    <input type="text" data-waga-input data-idx="${i}"
           class="text-input waga-input" lang="ja"
           autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"
           placeholder="は or が" maxlength="2" value="${esc((drillState.userValues || [])[i] || '')}"
           ${feedback ? 'disabled' : ''}>
  `).join(' ');
  return `
    <section class="waga-drill">
      <h3>Minimal-pair drill <span class="muted small">(${score} / ${total})</span></h3>
      <p class="muted">Use: <strong>${esc(current.useLabel)}</strong></p>
      <p class="waga-sentence">${renderJa(current.sentenceWithBlanks).replace(/___/g, () => `__BLANK__${inputs}`)}</p>
      <p class="waga-sentence">${renderJa(current.sentenceWithBlanks).replace(/___/g, '＿')}</p>
      <div class="waga-blank-row">${inputs}</div>
      ${feedback ? `
        <div class="drill-feedback ${feedback.correct ? 'correct' : 'incorrect'}">
          <div class="feedback-headline">${feedback.correct ? 'Correct' : 'Wrong'}</div>
          <p>Expected: <strong lang="ja">${esc(Array.isArray(current.particle) ? current.particle.join(' / ') : current.particle)}</strong></p>
          <p class="muted small">${esc(current.context)}</p>
        </div>
        <button id="waga-next" class="btn-primary">Next</button>
      ` : `
        <button id="waga-check" class="btn-primary">Check</button>
      `}
      <button id="waga-stop" style="margin-left: 8px">End drill</button>
    </section>
  `;
}

function wireDrill(container) {
  document.getElementById('waga-start')?.addEventListener('click', () => {
    drillState = { score: 0, total: 0 };
    pickQuestion();
    renderInPlace(container);
  });
  document.getElementById('waga-stop')?.addEventListener('click', () => {
    drillState = null;
    renderInPlace(container);
  });
  document.getElementById('waga-check')?.addEventListener('click', () => {
    const inputs = Array.from(document.querySelectorAll('[data-waga-input]'));
    drillState.userValues = inputs.map(i => i.value);
    const expected = Array.isArray(drillState.current.particle) ? drillState.current.particle : [drillState.current.particle];
    const correct = expected.every((p, i) => matchesAnswer(drillState.userValues[i] || '', [p]));
    drillState.feedback = { correct };
    drillState.total += 1;
    if (correct) drillState.score += 1;
    renderInPlace(container);
  });
  document.getElementById('waga-next')?.addEventListener('click', () => {
    pickQuestion();
    renderInPlace(container);
  });
}

function pickQuestion() {
  const pair = PAIRS[Math.floor(Math.random() * PAIRS.length)];
  const side = Math.random() < 0.5 ? 'a' : 'b';
  drillState.current = {
    useLabel: pair.use,
    sentenceWithBlanks: pair[side].sentence,
    particle: pair[side].particle,
    context: pair[side].context,
  };
  drillState.feedback = null;
  drillState.userValues = [];
}

function renderInPlace(container) {
  const section = container.querySelector('.waga-drill');
  if (!section) {
    container.innerHTML = '';
    renderWaGa(container);
    return;
  }
  section.outerHTML = renderDrillSection();
  wireDrill(container);
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
