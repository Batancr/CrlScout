"""
scout_player_spells.py -- one player's SPELL profile across the four scouting framings.

Companion to spell_sequences.py (roster-wide) and scout_player_sequences.py (one player's
win conditions). Same four framings: post-patch / all-time x CRL+practice / CRL-only.

WHY THIS IS DESCRIPTIVE AND NOT SIGNIFICANCE-TESTED
---------------------------------------------------
A single player has at most a few dozen duels. Split four ways, spell-package transition
cells land at n = 1-4. No honest test survives that, so this script does NOT print p-values
for transitions -- printing them would invite reading noise as a tell.

What IS statistically usable at this sample size is CONCENTRATION: what share of their games
run their top spell packages, and how that ranks against every other rostered player in the
same framing. A percentile is stable where a per-cell rate is not. Same logic as the
win-condition scout.

    reports/spell_scout_<player>.md
"""
import os
import sys
import json
import collections
import datetime

REPO = os.environ.get("CRL_REPO", os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
os.environ.setdefault("CRL_HOME", REPO)
import build_duel_workbook as B  # noqa: E402
from spell_sequences import SPELLS, fmt, PATCH  # noqa: E402

MIN_DUELS_FOR_PEER = 12

FRAMINGS = [
    ("Post-patch (Aug 5+) — CRL + practice", True, None),
    ("Post-patch (Aug 5+) — Official CRL only", True, "Official CRL"),
    ("All time — CRL + practice", False, None),
    ("All time — Official CRL only", False, "Official CRL"),
]


def load_by_player():
    duel_log, _, _ = B.build_dataset()
    byd = collections.defaultdict(list)
    for r in duel_log:
        byd[r["duel_id"]].append(r)
    out = collections.defaultdict(list)
    for did, rows in byd.items():
        rows = [r for r in rows if not r["is_rematch"] and r["deck"]]
        if len(rows) < 2:
            continue
        rows.sort(key=lambda r: (r["game_num"], r["battle_time"]))
        seen, games = set(), []
        for r in rows:
            if r["game_num"] in seen:
                continue
            seen.add(r["game_num"])
            games.append({
                "spells": frozenset(c for c in r["deck"] if c in SPELLS),
                "wc": frozenset(B.classify_deck(r["deck"])),
            })
        out[rows[0]["player_name"]].append({
            "category": rows[0].get("match_category") or "Practice",
            "time": rows[0]["battle_time"],
            "opponent": rows[0]["opponent_name"],
            "games": games[:B.MAX_GAMES_PER_DUEL],
        })
    return out


def subset(duels, post, cat):
    return [d for d in duels
            if not (post and d["time"] < PATCH) and not (cat and d["category"] != cat)]


def profile(duels):
    pkg = collections.Counter()
    card = collections.Counter()
    g1 = collections.Counter()
    trans = collections.defaultdict(collections.Counter)
    g3 = collections.defaultdict(collections.Counter)
    wc_ctx = collections.defaultdict(collections.Counter)
    n_games = 0
    for d in duels:
        gs = d["games"]
        for g in gs:
            pkg[g["spells"]] += 1
            for c in g["spells"]:
                card[c] += 1
            n_games += 1
        if gs:
            g1[gs[0]["spells"]] += 1
        if len(gs) >= 2:
            trans[gs[0]["spells"]][gs[1]["spells"]] += 1
            for w in gs[0]["wc"]:
                wc_ctx[(w, gs[0]["spells"])][gs[1]["spells"]] += 1
        if len(gs) >= 3:
            g3[gs[0]["spells"] | gs[1]["spells"]][gs[2]["spells"]] += 1
    top3 = sum(c for _, c in pkg.most_common(3))
    return {"n_duels": len(duels), "n_games": n_games, "pkg": pkg, "card": card,
            "g1": g1, "trans": trans, "g3": g3, "wc_ctx": wc_ctx,
            "conc": top3 / n_games if n_games else 0.0,
            "n_pkgs": len(pkg)}


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "Asaf"
    allp = load_by_player()
    if target not in allp:
        print("not found; close:", [n for n in allp if target.lower() in (n or "").lower()][:8])
        return

    L = [f"# Spell profile — {target}\n",
         f"\n_Generated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC_\n",
         "\n> **No p-values on transitions here, deliberately.** Split four ways, this player's "
         "spell-package transition cells land at n = 1–4. No honest test survives that, and "
         "printing one would invite reading noise as a tell. The **concentration percentile** "
         "is the statistically usable number — it ranks him against every rostered player with "
         f"at least {MIN_DUELS_FOR_PEER} duels in the same framing.\n"]

    payload = []
    for label, post, cat in FRAMINGS:
        me = profile(subset(allp[target], post, cat))
        peers = []
        for name, duels in allp.items():
            if name == target:
                continue
            p = profile(subset(duels, post, cat))
            if p["n_duels"] >= MIN_DUELS_FOR_PEER:
                peers.append(p["conc"])
        pct = (100.0 * sum(1 for x in peers if x < me["conc"]) / len(peers)) if peers else None

        L.append(f"\n## {label}\n")
        L.append(f"\n**{me['n_duels']} duels · {me['n_games']} games · "
                 f"{me['n_pkgs']} distinct spell packages**\n")
        if me["n_duels"] < 20:
            L.append(f"\n⚠️ **Only {me['n_duels']} duels — indicative, not established.**\n")
        L.append(f"\n- Top-3 spell-package concentration: **{me['conc']:.0%}** of games"
                 + (f" — more concentrated than **{pct:.0f}%** of the roster "
                    f"({len(peers)} peers)\n" if pct is not None else "\n"))

        tot = me["n_games"] or 1
        L.append("\n**Spell packages he brings:**\n\n| package | games | share |\n|---|---|---|\n")
        for p, c in me["pkg"].most_common(8):
            L.append(f"| {fmt(p)} | {c} | {c/tot:.0%} |\n")

        L.append("\n**Individual spell usage:**\n\n| spell | decks | share of his decks |\n|---|---|---|\n")
        for c, n in me["card"].most_common(10):
            L.append(f"| {c} | {n} | {n/tot:.0%} |\n")

        rows = []
        for a, tc in me["trans"].items():
            for b, c in tc.items():
                rows.append((c, fmt(a), fmt(b)))
        rows.sort(reverse=True)
        L.append("\n**Game 1 spells → game 2 spells** (raw counts; no significance claimed)\n\n"
                 "| he opened | he followed with | times |\n|---|---|---|\n")
        if rows:
            for c, a, b in rows[:10]:
                L.append(f"| {a} | {b} | {c} |\n")
        else:
            L.append("| _no duels with two games_ | | |\n")
        rep = [r for r in rows if r[0] > 1]
        L.append(f"\n_{len(rep)} of {len(rows)} game-1→game-2 spell transitions occurred more "
                 f"than once._\n")

        g3rows = []
        for a, tc in me["g3"].items():
            for b, c in tc.items():
                g3rows.append((c, fmt(a), fmt(b)))
        g3rows.sort(reverse=True)
        if g3rows:
            L.append("\n**Spells used in games 1+2 → game 3** (raw counts)\n\n"
                     "| already spent | game 3 | times |\n|---|---|---|\n")
            for c, a, b in g3rows[:8]:
                L.append(f"| {a} | {b} | {c} |\n")

        payload.append({"label": label, "n_duels": me["n_duels"], "n_games": me["n_games"],
                        "n_pkgs": me["n_pkgs"], "conc": me["conc"], "pct": pct,
                        "pkg": [[fmt(k), v] for k, v in me["pkg"].most_common(8)],
                        "card": me["card"].most_common(10),
                        "trans": [[a, b, c] for c, a, b in rows[:10]],
                        "g3": [[a, b, c] for c, a, b in g3rows[:8]]})
        print(f"{label:42} n={me['n_duels']:3} games={me['n_games']:4} "
              f"pkgs={me['n_pkgs']:3} conc={me['conc']:.0%} pct={None if pct is None else round(pct)}")

    os.makedirs(os.path.join(REPO, "reports"), exist_ok=True)
    p = os.path.join(REPO, "reports", f"spell_scout_{target.lower()}.md")
    with open(p, "w") as f:
        f.write("".join(L))
    with open(os.path.join(REPO, "reports", f"spell_scout_{target.lower()}.json"), "w") as f:
        json.dump(payload, f, indent=1)
    print("wrote", p)


if __name__ == "__main__":
    main()
