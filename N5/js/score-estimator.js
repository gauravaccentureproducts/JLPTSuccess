// IMP-WAVE-P4-T4 (UI audit fix, 2026-05-11): JLPT N5 scaled-score
// estimator.
//
// Real JLPT scoring is equipercentile-scaled, NOT a raw-percent
// linear map. We can't replicate the official 0-180 conversion
// (JEES doesn't publish the scale), but we can give the user a
// rough projection using the section caps + diagnostic-band table
// authored in data/test_strategy.json (score_breakdown).
//
// Approach (kept simple + documented as approximation):
//   - Section 1 (Lang Knowledge + Reading): raw%  ->  raw% * 1.2
//     up to a cap of 120. This is a linear projection, NOT the
//     official equipercentile scale.
//   - Section 2 (Listening): raw%  ->  raw% * 0.6 up to a cap of 60.
//   - Total = section1_scaled + section2_scaled (max 180).
//   - Band lookup: diagnostic_band buckets from test_strategy.json.
//
// We are explicit with the user that this is an APPROXIMATION:
// the result UI calls it an "estimate" and links to the
// scaling_explanation note.
//
// Public API:
//   await loadScoreBands()
//      Returns the diagnostic_band table from test_strategy.json
//      or a sensible default if the fetch fails.
//
//   estimate(sec1, sec2)
//      sec1 = {correct, total}, sec2 = {correct, total}
//      Returns {section1: {raw_pct, scaled, max, min, meets_min},
//               section2: {raw_pct, scaled, max, min, meets_min},
//               total:    {scaled, max, min, meets_min, all_sections_pass},
//               band:     {key, label, hint}}.

let _bandsCache = null;

const DEFAULT_BANDS = {
  below_38_or_19: 'fail (any section below minimum = fail regardless of total)',
  '38_57':  'weak — needs focused review of section topics',
  '57_80':  'borderline — strengthen weak section',
  '80_120': 'pass — solid',
  '120_180': 'strong pass — N4-ready',
};

export async function loadScoreBands() {
  if (_bandsCache) return _bandsCache;
  try {
    const r = await fetch('data/test_strategy.json');
    if (!r.ok) {
      _bandsCache = DEFAULT_BANDS;
      return _bandsCache;
    }
    const d = await r.json();
    _bandsCache = (d.score_breakdown && d.score_breakdown.diagnostic_band) || DEFAULT_BANDS;
    return _bandsCache;
  } catch {
    _bandsCache = DEFAULT_BANDS;
    return _bandsCache;
  }
}

function pctOf(c, t) { return t > 0 ? (100 * c / t) : 0; }

export function estimate(sec1, sec2) {
  const s1pct = pctOf(sec1.correct, sec1.total);
  const s2pct = pctOf(sec2.correct, sec2.total);
  // Linear projection of raw% onto the section cap.
  const s1scaled = Math.round(Math.min(120, s1pct * 1.2));
  const s2scaled = Math.round(Math.min(60,  s2pct * 0.6));
  const total = s1scaled + s2scaled;

  const SEC1_MIN = 38;
  const SEC2_MIN = 19;
  const TOTAL_MIN = 80;

  const s1ok = s1scaled >= SEC1_MIN;
  const s2ok = s2scaled >= SEC2_MIN;
  const totalOk = total >= TOTAL_MIN;
  const allPass = s1ok && s2ok && totalOk;

  return {
    section1: {
      raw_pct: Math.round(s1pct),
      scaled:  s1scaled,
      max:     120,
      min:     SEC1_MIN,
      meets_min: s1ok,
    },
    section2: {
      raw_pct: Math.round(s2pct),
      scaled:  s2scaled,
      max:     60,
      min:     SEC2_MIN,
      meets_min: s2ok,
    },
    total: {
      scaled:  total,
      max:     180,
      min:     TOTAL_MIN,
      meets_min: totalOk,
      all_sections_pass: allPass,
    },
    band: getBand(total, s1ok && s2ok),
  };
}

// Returns one of: fail / weak / borderline / pass / strong_pass.
// `sectionMinsMet` qualifies the band — if a section min is missed,
// the band auto-degrades to "fail" no matter what the total is.
export function getBand(total, sectionMinsMet) {
  if (!sectionMinsMet) {
    return {
      key:   'fail_section_min',
      label: 'Fail (section minimum missed)',
      hint:  'Even if the total cleared 80, a section below its minimum (38 or 19) is a fail. Strengthen the weakest section.',
      tone:  'fail',
    };
  }
  if (total < 38) {
    return {
      key:   'fail_overall',
      label: 'Fail',
      hint:  'Below 38 in Section 1, OR below 19 in Section 2. Cannot pass at this level.',
      tone:  'fail',
    };
  }
  if (total < 57) {
    return {
      key:   'weak',
      label: 'Weak',
      hint:  'Needs focused review of the weakest section topics. Use #/weakareas to identify gaps.',
      tone:  'weak',
    };
  }
  if (total < 80) {
    return {
      key:   'borderline',
      label: 'Borderline',
      hint:  'Just below the pass line. Strengthen the weaker section to lock in a pass.',
      tone:  'borderline',
    };
  }
  if (total < 120) {
    return {
      key:   'pass',
      label: 'Pass — solid',
      hint:  'Comfortable pass. Maintain accuracy and move on to N4-prep.',
      tone:  'pass',
    };
  }
  return {
    key:   'strong_pass',
    label: 'Strong pass — N4-ready',
    hint:  'Excellent. Consider stepping up to N4 study material.',
    tone:  'strong_pass',
  };
}
