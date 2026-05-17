"""Fix BUG-047 through BUG-053 — listening.json data-quality bugs.

All 7 bugs are manifestations of the same meta-class as BUG-041..046
(reading.json batch-drift): a round-9 VOICEVOX migration completed in
some fields but never propagated to others. Per-bug summary:

  BUG-047 (Medium/P2): voice_planned.engine="edge-tts" vs
          audio_render_meta.voice_provider="voicevox" on all 50.
          Fix: drop voice_planned (audio_render_meta is canonical
          per option (b) of the bug; UI updated to read from
          audio_render_meta in the same commit).

  BUG-048 (Medium/P2): pacing_status / voice_variety_status stale
          for items 41-50.
          Fix: items 041-047 pacing_status "no_audio" → "unmeasured"
          (audio IS rendered; just not measured for pacing).
          Items 048-050 voice_variety_status None → "rendered".

  BUG-049 (Major/P2): 26/50 items pacing too slow (mean 160 mpm vs
          target 200-220 mpm).
          Fix: SURFACE-ONLY in this batch — needs audio re-render
          (VOICEVOX install required, ~30 min budget). The bug
          stays Open with a "pacing_fix_status" stamp in _meta
          documenting the queued action.

  BUG-050 (Medium/P2): version.json.counts.listening=47 vs actual 50.
          ALREADY FIXED in cdef185 (Rule-5 install bumped version
          .json simultaneously). JA-107 now locks. Mark Fixed.

  BUG-051 (Medium/P3): format and format_type fields are 1:1
          redundant. Fix: drop format (format_type is more
          descriptive); JS consumers updated to use format_type.

  BUG-052 (Low/P4): _meta.voice_variety_plan describes VOICEVOX as
          future work even though it has already been used.
          Fix: rewrite the block as a past-tense completion record
          (status=completed_2026_05_12).

  BUG-053 (Low/P4): voicevox_speaker_catalog has wrong character-
          name → speaker-ID mappings (e.g. "hau-tsumugi" listed for
          ID 8 but VOICEVOX ID 8 is 春日部つむぎ; ID 10 is 雨晴はう).
          Plus voice-variety target of 8 only met at 6.
          Fix: rewrite catalog with correct mappings (bundled into
          BUG-052's voice_variety_plan rewrite).
"""
from __future__ import annotations

import io
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / "data" / "listening.json"


def fix_bug_047_drop_voice_planned(items: list[dict]) -> int:
    """Drop voice_planned (audio_render_meta is the canonical source).

    Per option (b) of the BUG-047 description. The UI's F-10 voice-
    attribution surface (listening.js) is being updated in the same
    commit to read voice_provider + voice_planned_for_engine from
    audio_render_meta. Pre-fix every item had voice_planned.engine=
    "edge-tts" while audio_render_meta.voice_provider="voicevox".
    """
    n = 0
    for item in items:
        if "voice_planned" in item:
            del item["voice_planned"]
            item["bug_047_fix_2026_05_17"] = True
            n += 1
    return n


def fix_bug_048_refresh_stale_audit(items: list[dict]) -> tuple[int, int]:
    """Refresh stale pacing_status / voice_variety_status on rendered items.

    Items 041-047: pacing_status was "no_audio" but audio_render_meta.
    rendered_at is set — audio HAS been rendered, pacing just hasn't
    been measured. Correct status is "unmeasured".

    Items 048-050: voice_variety_status was None but audio_render_meta.
    rendered_at is set — render happened. Correct status is "rendered".
    """
    n_pacing = 0
    n_voice_variety = 0
    for item in items:
        arm = item.get("audio_render_meta", {})
        if not arm.get("rendered_at"):
            continue  # No render → leave statuses as-is
        # pacing_status: "no_audio" is wrong when render exists
        if item.get("pacing_status") == "no_audio":
            item["pacing_status"] = "unmeasured"
            item["bug_048_fix_2026_05_17"] = True
            n_pacing += 1
        # voice_variety_status: None is wrong when render exists
        if item.get("voice_variety_status") is None:
            item["voice_variety_status"] = "rendered"
            item["bug_048_fix_2026_05_17"] = True
            n_voice_variety += 1
    return n_pacing, n_voice_variety


def fix_bug_049_pacing_surface_only(listening_data: dict) -> int:
    """Surface BUG-049 (pacing too slow) in _meta — needs audio re-render.

    Adds a _meta.pacing_fix_status block documenting the deferred fix
    so the next audit cycle can pick it up. Does not modify item-level
    data — that requires VOICEVOX re-render at speed_scale ~1.3x.
    """
    meta = listening_data.setdefault("_meta", {})
    if meta.get("pacing_fix_status"):
        return 0  # idempotency
    # Compute current pacing distribution from the items themselves
    items = listening_data.get("items", [])
    ps = Counter()
    mpms = []
    for it in items:
        ps[it.get("pacing_status")] += 1
        v = it.get("pacing_morae_per_min")
        if isinstance(v, (int, float)):
            mpms.append(v)
    mean_mpm = round(sum(mpms) / len(mpms), 1) if mpms else None
    meta["pacing_fix_status"] = {
        "bug": "BUG-049",
        "status": "open_awaiting_re_render",
        "filed": "2026-05-17",
        "issue": (
            "Pacing systematically too slow: 26/50 items below the "
            "JLPT N5 target band of 180-240 mora/min. Mean observed "
            f"= {mean_mpm} mpm; some items (e.g. n5.listen.012) "
            "around 38 mpm — roughly 5× slower than exam pace."
        ),
        "fix_action_required": (
            "Re-render the 26 too-slow items at audio_render_meta."
            "speed_scale ~1.3 (currently 1.0 by default). VOICEVOX "
            "must be running locally; ~30 min budget."
        ),
        "current_distribution": dict(ps),
        "mean_mpm_observed": mean_mpm,
        "target_mpm_band": [180, 240],
    }
    return 1


def fix_bug_051_drop_format(items: list[dict]) -> int:
    """Drop the redundant `format` field (format_type is canonical).

    The two fields had perfect 1:1 mapping:
        format="task"       ↔ format_type="task_understanding"
        format="point"      ↔ format_type="point_understanding"
        format="utterance"  ↔ format_type="utterance_expression"
        format="response"   ↔ format_type="immediate_response"

    JS consumers (listening.js, search.js) updated in the same commit
    to use format_type.
    """
    n = 0
    for item in items:
        if "format" in item:
            del item["format"]
            item["bug_051_fix_2026_05_17"] = True
            n += 1
    return n


def fix_bug_052_053_voice_variety_plan_rewrite(listening_data: dict) -> int:
    """Rewrite _meta.voice_variety_plan as past-tense completion record.

    Fixes BUG-052 (plan still describes VOICEVOX as future work even
    though render is done) AND BUG-053 (catalog has wrong character-
    name → speaker-ID mappings; observed 6 distinct speakers vs target
    of 8).
    """
    meta = listening_data.setdefault("_meta", {})

    # Compute actual speakers used from items
    items = listening_data.get("items", [])
    speakers_used = Counter()
    for it in items:
        arm = it.get("audio_render_meta", {})
        vu = arm.get("voices_used") or []
        if isinstance(vu, list):
            for v in vu:
                speakers_used[v] += 1

    new_plan = {
        "status": "completed_2026_05_12",
        "note": (
            "BUG-052/053 fix 2026-05-17 — VOICEVOX migration "
            "COMPLETED on 2026-05-12 (per audio_render_meta."
            "rendered_at on all 50 items). 6 distinct VOICEVOX "
            "speakers observed in production vs the 8 target; see "
            "voicevox_speaker_catalog below for the *corrected* "
            "speaker_id → character mappings (the prior catalog "
            "had wrong character names: ID 8 was labeled "
            "'hau-tsumugi' but is actually 春日部つむぎ; ID 11 "
            "was 'shirakami-kotaro' but is actually 玄野武宏; "
            "ID 13 was filed under '12' as 'aoyama-ryusei' but "
            "the correct ID is 13)."
        ),
        "target_voices": 8,
        "observed_distinct_voices": len(speakers_used),
        "target_dialogue_voices_per_item": 2,
        # CORRECTED VOICEVOX speaker catalog. Source of truth: the
        # VOICEVOX speaker enumeration (localhost:50021/speakers
        # returns speaker.styles[].id). Kanji names are the canonical
        # character names; romaji is the latin gloss for export.
        "voicevox_speaker_catalog": {
            "2": {"character": "四国めたん", "romaji": "shikoku-metan", "style": "ノーマル"},
            "3": {"character": "ずんだもん", "romaji": "zundamon", "style": "ノーマル"},
            "8": {"character": "春日部つむぎ", "romaji": "kasukabe-tsumugi", "style": "ノーマル"},
            "10": {"character": "雨晴はう", "romaji": "amehare-hau", "style": "ノーマル"},
            "11": {"character": "玄野武宏", "romaji": "kurono-takehiro", "style": "ノーマル"},
            "13": {"character": "青山龍星", "romaji": "aoyama-ryusei", "style": "ノーマル"},
            # Below: 2 speakers from the original plan that did NOT
            # appear in the actual render. Kept here for the unmet-
            # target diversity note.
            "14": {"character": "冥鳴ひまり", "romaji": "meimei-himari", "style": "ノーマル", "render_status": "not_used"},
            "53": {"character": "ナースロボ＿タイプＴ", "romaji": "nurse-robo-type-T", "style": "ノーマル", "render_status": "not_used"},
        },
        "observed_speaker_distribution": dict(speakers_used.most_common()),
        "speaker_label_classification": {
            "male_hints": ["お父さん", "かれ", "先生男", "父", "男"],
            "female_hints": ["お母さん", "かのじょ", "先生女", "女", "母"],
            "other_staff_teacher_etc": "rotates across voicevox 11 / 13 / 10",
        },
        "unmet_target_note": (
            "Target was 8 distinct VOICEVOX speakers; the 2026-05-12 "
            "render used 6 (the 14 冥鳴ひまり and 53 ナースロボ＿タイプＴ "
            "slots from the original plan were dropped during the "
            "render pass; the cause is unrecorded). Future iteration: "
            "re-render a subset of items using the 2 missing speakers "
            "to hit the diversity target. Tracked under the BUG-053 "
            "follow-up."
        ),
        "supersedes": "voice_variety_plan_2026_05_07",
        "render_command_historical": (
            "Render was completed via tools/build_audio_voicevox.py "
            "on 2026-05-12 against VOICEVOX engine running at "
            "localhost:50021. The audio_render_meta.voicevox_engine_"
            "version field on each item records the exact engine "
            "build used."
        ),
        "bug_052_053_fix_2026_05_17": True,
    }

    if meta.get("voice_variety_plan") != new_plan:
        meta["voice_variety_plan"] = new_plan
        # Also mark the legacy 2026-05-07 plan as superseded
        legacy = meta.get("voice_variety_plan_2026_05_07")
        if legacy and "superseded_by" not in legacy:
            legacy["superseded_by"] = "voice_variety_plan (2026-05-12 VOICEVOX render)"
            legacy["superseded_at"] = "2026-05-17"
        return 1
    return 0


def main() -> int:
    L = json.loads(LISTENING.read_text(encoding="utf-8"))
    items = L.get("items", [])
    print(f"Loaded listening.json — {len(items)} items")

    print("\n--- BUG-047: drop voice_planned (audio_render_meta canonical) ---")
    n = fix_bug_047_drop_voice_planned(items)
    print(f"  Dropped voice_planned on {n} items")

    print("\n--- BUG-048: refresh stale audit status fields ---")
    n_p, n_v = fix_bug_048_refresh_stale_audit(items)
    print(f"  pacing_status no_audio→unmeasured: {n_p} items")
    print(f"  voice_variety_status None→rendered: {n_v} items")

    print("\n--- BUG-049: surface as deferred (audio re-render required) ---")
    n = fix_bug_049_pacing_surface_only(L)
    print(f"  _meta.pacing_fix_status block added: {n}")

    print("\n--- BUG-051: drop format (format_type canonical) ---")
    n = fix_bug_051_drop_format(items)
    print(f"  Dropped format on {n} items")

    print("\n--- BUG-052+BUG-053: rewrite _meta.voice_variety_plan ---")
    n = fix_bug_052_053_voice_variety_plan_rewrite(L)
    print(f"  _meta.voice_variety_plan rewritten: {n}")

    LISTENING.write_text(
        json.dumps(L, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nSaved {LISTENING}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
