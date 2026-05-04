// Particle minimal-pair drills (Brief §2.7)
// Both choices grammatical; meaning differs. Show BOTH translations after
// the answer so the learner internalizes the meaning difference.
import { renderJa } from './furigana.js';

const PAIRS = [
  // に / で - location
  {
    set: 'に vs で (location)',
    a: { sentence: 'へやに ねこが います。', particle: 'に', en_with: 'There is a cat in the room (existence - location of being).' },
    b: { sentence: 'へやで しゅくだいを します。', particle: 'で', en_with: 'I do homework in the room (action - location of doing).' },
  },
  {
    set: 'に vs で (location)',
    a: { sentence: 'こうえんに 木が あります。', particle: 'に', en_with: 'There are trees in the park.' },
    b: { sentence: 'こうえんで あそびます。', particle: 'で', en_with: 'I play in the park.' },
  },
  // に / へ - direction
  {
    set: 'に vs へ (direction)',
    a: { sentence: '日本に 行きます。', particle: 'に', en_with: 'I go TO Japan (focus on arrival/destination).' },
    b: { sentence: '日本へ 行きます。', particle: 'へ', en_with: 'I go TOWARD Japan (focus on direction; slightly more formal).' },
  },
  // を / が - with stative predicates
  {
    set: 'を vs が (with stative)',
    a: { sentence: 'ねこが すきです。', particle: 'が', en_with: 'I like cats (stative - must take が).' },
    b: { sentence: 'りんごを 食べます。', particle: 'を', en_with: 'I eat apples (action verb - direct object takes を).' },
  },
  // と / に - with people
  {
    set: 'と vs に (people / interaction)',
    a: { sentence: 'ともだちと 行きます。', particle: 'と', en_with: 'I go WITH a friend (companion).' },
    b: { sentence: 'ともだちに 会います。', particle: 'に', en_with: 'I meet a friend (会う takes に for the person met).' },
  },
  // か / や - listing
  {
    set: 'か vs や (listing / alternative)',
    a: { sentence: 'コーヒーか おちゃが いいです。', particle: 'か', en_with: 'Coffee OR tea is good (alternatives - pick one).' },
    b: { sentence: 'コーヒーや おちゃが すきです。', particle: 'や', en_with: 'I like coffee, tea, etc. (non-exhaustive listing).' },
  },
  // wa / ga - topic vs subject
  {
    set: 'は vs が (topic / new info)',
    a: { sentence: 'わたしは がくせいです。', particle: 'は', en_with: 'I am a student (topical statement; わたし is the topic).' },
    b: { sentence: 'だれが がくせいですか。', particle: 'が', en_with: 'Who is the student? (question word + が - asking for new info).' },
  },
];

let session = null;

export async function renderParticlePairs(container) {
  if (!session) return renderSetup(container);
  return renderRound(container);
}

function renderSetup(container) {
  container.innerHTML = `
    <h2>Particle minimal-pair drill</h2>
    <p>Each round shows two sentences differing by one particle. Both are grammatical - the <strong>meaning</strong> changes. After your pick, both translations appear so you can train the meaning difference, not just the "correct" particle.</p>
    <p class="muted small">Pairs covered: ${[...new Set(PAIRS.map(p => p.set))].join(' · ')}</p>
    <button id="pp-start" class="btn-primary">Start (10 rounds)</button>
  `;
  document.getElementById('pp-start').addEventListener('click', () => {
    session = { idx: 0, total: 10, queue: pickRounds(10), score: 0, history: [] };
    renderRound(container);
  });
}

function pickRounds(n) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const pair = PAIRS[Math.floor(Math.random() * PAIRS.length)];
    // Randomize which side we ask
    const side = Math.random() < 0.5 ? 'a' : 'b';
    const target = pair[side];
    const other = pair[side === 'a' ? 'b' : 'a'];
    out.push({ set: pair.set, target, other });
  }
  return out;
}

function renderRound(container) {
  const r = session.queue[session.idx];
  const feedback = session.feedback;
  const sentenceWithBlank = r.target.sentence.replace(r.target.particle, '（　）');
  const choices = Array.from(new Set([r.target.particle, r.other.particle])).sort();
  // Add 2 random distractors so we have 4 choices
  const pool = ['は', 'が', 'を', 'に', 'で', 'へ', 'と', 'から', 'まで', 'や', 'か', 'も'].filter(p => !choices.includes(p));
  while (choices.length < 4 && pool.length) {
    const i = Math.floor(Math.random() * pool.length);
    choices.push(pool.splice(i, 1)[0]);
  }
  shuffle(choices);

  container.innerHTML = `
    <div class="pp-round">
      <div class="srs-progress">
        <span>Round <strong>${session.idx + 1}</strong> / <strong>${session.total}</strong></span>
        <span class="muted small">Set: ${esc(r.set)} · Score: ${session.score}</span>
      </div>
      <article class="pp-card">
        <p class="pp-sentence" lang="ja">${renderJa(sentenceWithBlank)}</p>
        <div class="choice-grid">
          ${choices.map(c => `<button class="choice-button${feedback ? (c === r.target.particle ? ' correct-choice' : (c === feedback.picked && c !== r.target.particle ? ' wrong-choice' : '')) : ''}" data-pick="${esc(c)}" ${feedback ? 'disabled' : ''}>${renderJa(c)}</button>`).join('')}
        </div>
        ${feedback ? `
          <div class="drill-feedback ${feedback.correct ? 'correct' : 'incorrect'}">
            <div class="feedback-headline">${feedback.correct ? 'Correct' : 'Wrong'}</div>
            <p>The intended sentence: <strong lang="ja">${renderJa(r.target.sentence)}</strong></p>
            <p class="muted small">${esc(r.target.en_with)}</p>
            <hr style="border: none; border-top: 1px solid var(--c-border); margin: 8px 0;">
            <p>The other particle would mean:</p>
            <p><strong lang="ja">${renderJa(r.other.sentence)}</strong></p>
            <p class="muted small">${esc(r.other.en_with)}</p>
            <button id="pp-next" class="btn-primary">${session.idx === session.total - 1 ? 'Finish' : 'Next'}</button>
          </div>
        ` : ''}
      </article>
    </div>
  `;

  container.querySelectorAll('[data-pick]').forEach(btn => {
    btn.addEventListener('click', () => {
      const picked = btn.dataset.pick;
      const correct = picked === r.target.particle;
      session.feedback = { picked, correct };
      if (correct) session.score += 1;
      session.history.push({ set: r.set, picked, correct, target: r.target.particle });
      renderRound(container);
    });
  });
  document.getElementById('pp-next')?.addEventListener('click', () => {
    session.feedback = null;
    session.idx += 1;
    if (session.idx >= session.total) renderFinished(container);
    else renderRound(container);
  });
}

function renderFinished(container) {
  const total = session.total;
  const pct = Math.round((session.score / total) * 100);
  container.innerHTML = `
    <h2>Particle pairs - done</h2>
    <section class="srs-summary-stats">
      <div class="stat-card mastered"><div class="stat-num">${session.score}/${total}</div><div class="stat-label">Score</div></div>
      <div class="stat-card ${pct >= 70 ? 'mastered' : 'weak'}"><div class="stat-num">${pct}%</div><div class="stat-label">Accuracy</div></div>
    </section>
    <div class="test-nav">
      <button id="pp-restart" class="btn-primary">Try again</button>
      <button id="pp-back">Back</button>
    </div>
  `;
  document.getElementById('pp-restart').addEventListener('click', () => {
    session = null;
    renderSetup(container);
  });
  document.getElementById('pp-back').addEventListener('click', () => {
    location.hash = '#/learn';
  });
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}
