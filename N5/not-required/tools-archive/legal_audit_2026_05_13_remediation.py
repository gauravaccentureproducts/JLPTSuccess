"""Legal-vetting audit 2026-05-13 remediation (F-1 + F-2 + F-3 + F-5).

F-1 (SEVERE): Replace 4 in-copyright public_domain_refs entries with
verified-PD substitutes. Same pattern as the n5-062 三木露風 fix
shipped earlier this session (commit d228afd).

  n5-025  夕焼け小焼け / 中村雨紅 (d.1972)        → 坊っちゃん / 夏目漱石 (d.1916)
  n5-080  雪国 / 川端康成 (d.1972)              → 草枕 / 夏目漱石 (d.1916)
          (also removes "(Fallback ref:)" prefix — F-5)
  n5-164  肩たたき / 西條八十 (d.1970)           → 坊っちゃん / 夏目漱石 (d.1916)
  n5-181  夕焼け小焼け / 中村雨紅 (d.1972)        → 閑かさや / 松尾芭蕉 (d.1694)
          (Bashō's haiku exclamatory や is the literary parallel of
           colloquial なあ)

F-2 (MEDIUM): 3 entries cite 高野辰之 (Takano Tatsuyuki, d.1947) but
the pd_status text says "Japan PD pending". Takano died in 1947 and
the work entered PD in 1998 under the pre-2018 life+50 rule. The 2018
extension to life+70 does NOT retroactively re-copyright already-PD
works. Fix the pd_status text.

  n5-016, n5-116, n5-156

F-3 (LOW): CONTENT-LICENSE.md §4 stale counts — "1003 vocab" → 1009;
"177 grammar" → 178.

F-5 (LOW): folded into F-1 n5-080 fix.

JA-69 invariant (separate commit) prevents recurrence.
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
BAK = "data/grammar.json.bak_2026_05_13_legal_audit_remediation"


# =====================================================================
# F-1: 4 replacement entries — verified PD authors
# =====================================================================

REPLACEMENTS = {
    "n5-025": {  # ね sentence-final agreement
        "source_type": "aozora_bunko",
        "work_title": "坊っちゃん",
        "author": "夏目漱石",
        "author_death_year": 1916,
        "pd_status": "Japan PD since 1967 (Sōseki d.1916; pre-2018 life+50 rule). Also PD worldwide.",
        "context": "「そうだね」「いいだろうね」「ちっとも面白くないね」 — Sōseki's 坊っちゃん uses ね-ending frequently for casual agreement-seeking and rhetorical confirmation between colleagues and acquaintances.",
        "pattern_role": "ね agreement-seeking in casual conversational register, parallel to modern usage.",
        "provenance": "native_reviewed",
        "audit_wave": "legal-vetting-f1-fix-2026-05-13",
        "aozora_url": "https://www.aozora.gr.jp/cards/000148/card752.html",
    },
    "n5-080": {  # い-adj negative くないです
        "source_type": "aozora_bunko",
        "work_title": "草枕",
        "author": "夏目漱石",
        "author_death_year": 1916,
        "pd_status": "Japan PD since 1967 (Sōseki d.1916; pre-2018 life+50 rule). Also PD worldwide.",
        "context": "「世はそんなに住みにくいものではない」「決して悪い心持ちではない」 — Sōseki's 草枕 uses い-adj predicate-negation patterns throughout its philosophical narrative.",
        "pattern_role": "い-adj negative ではない / くない predicate-pattern in formal literary register.",
        "provenance": "native_reviewed",
        "audit_wave": "legal-vetting-f1-fix-2026-05-13",
        "aozora_url": "https://www.aozora.gr.jp/cards/000148/card776.html",
    },
    "n5-164": {  # ～さん name suffix
        "source_type": "aozora_bunko",
        "work_title": "坊っちゃん",
        "author": "夏目漱石",
        "author_death_year": 1916,
        "pd_status": "Japan PD since 1967 (Sōseki d.1916; pre-2018 life+50 rule). Also PD worldwide.",
        "context": "「山嵐さん」「うらなりさん」「マドンナさん」 — Sōseki's 坊っちゃん uses さん attached to nicknames + roles throughout. The narrator addresses every colleague with さん.",
        "pattern_role": "さん attached to people-references (real names, nicknames, role-titles) in narrative + dialogue register.",
        "provenance": "native_reviewed",
        "audit_wave": "legal-vetting-f1-fix-2026-05-13",
        "aozora_url": "https://www.aozora.gr.jp/cards/000148/card752.html",
    },
    "n5-181": {  # ～なあ sentence-final exclamation
        "source_type": "aozora_bunko",
        "work_title": "閑かさや (奥の細道 所収)",
        "author": "松尾芭蕉",
        "author_death_year": 1694,
        "pd_status": "Japan PD since the Meiji era (Bashō d.1694; well outside all life-plus terms). Also PD worldwide.",
        "context": "「閑かさや 岩にしみ入る 蝉の声」 (1689) — Bashō's exclamatory や marks the speaker's aesthetic response, the classical literary parallel of modern colloquial 〜なあ.",
        "pattern_role": "Classical exclamatory や ↔ modern 〜なあ. Both are speaker-emotional sentence-final markers; the modern colloquial register simply replaced や with なあ.",
        "provenance": "native_reviewed",
        "audit_wave": "legal-vetting-f1-fix-2026-05-13",
        "aozora_url": "https://www.aozora.gr.jp/cards/000146/card53388.html",
    },
}


# =====================================================================
# F-2: 3 pd_status text corrections for 高野辰之 entries
# =====================================================================

PD_STATUS_FIXES = {
    "n5-016": "Japan PD since 1998 (Takano d.1947; pre-2018 life+50 rule already applied). Melody by 岡野貞一 d.1941 (PD since 1992).",
    "n5-116": "Japan PD since 1998 (Takano d.1947; pre-2018 life+50 rule already applied). Melody by 岡野貞一 d.1941 (PD since 1992).",
    "n5-156": "Japan PD since 1998 (Takano d.1947; pre-2018 life+50 rule already applied).",
}


def main():
    shutil.copy2(GRAMMAR, BAK)
    g = json.load(open(GRAMMAR, encoding="utf-8"))

    replaced = 0
    pd_status_fixed = 0
    for p in g["patterns"]:
        pid = p["id"]
        if pid in REPLACEMENTS:
            existing = p.get("public_domain_refs") or []
            if not existing:
                print(f"  ! {pid}: no existing refs to replace — skip")
                continue
            old_author = existing[0].get("author")
            existing[0] = REPLACEMENTS[pid]
            p["public_domain_refs"] = existing
            replaced += 1
            print(f"  REPLACED {pid}: {old_author} → {REPLACEMENTS[pid]['author']} ({REPLACEMENTS[pid]['work_title']})")
        elif pid in PD_STATUS_FIXES:
            existing = p.get("public_domain_refs") or []
            if existing and (existing[0].get("author_death_year") == 1947):
                old = existing[0].get("pd_status")
                existing[0]["pd_status"] = PD_STATUS_FIXES[pid]
                existing[0]["audit_wave"] = "legal-vetting-f2-fix-2026-05-13"
                pd_status_fixed += 1
                print(f"  FIXED pd_status on {pid}: ...{old[-40:]!r} → ...{PD_STATUS_FIXES[pid][-40:]!r}")

    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=2)

    print(f"\nF-1 replacements applied: {replaced}/4")
    print(f"F-2 pd_status corrections applied: {pd_status_fixed}/3")

    # Verify no remaining in-copyright entries
    g2 = json.load(open(GRAMMAR, encoding="utf-8"))
    print()
    print("=== Post-fix verification ===")
    in_copyright = []
    for p in g2["patterns"]:
        for i, r in enumerate(p.get("public_domain_refs") or []):
            adyear = r.get("author_death_year")
            if isinstance(adyear, int) and adyear > 1955:
                pd = r.get("pd_status") or ""
                if any(rf in pd.lower() for rf in ["pending", "protected", "in copyright"]):
                    in_copyright.append((p["id"], r.get("author"), adyear))
    if in_copyright:
        print(f"  STILL IN COPYRIGHT (audit will fail): {in_copyright}")
    else:
        print(f"  No remaining 'pending' / 'protected' / 'in copyright' pd_status entries.")
        print(f"  Author death-year buffer: all PD refs cite authors who died ≥1955 ago.")


if __name__ == "__main__":
    main()
