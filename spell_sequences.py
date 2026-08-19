"""
spell_sequences.py -- what spell package follows what, across a duel set.

THE IDEA (Alexander, 2026-08-18)
--------------------------------
Spells are a far smaller space than win conditions -- roughly 18 cards, and most decks run
exactly two. So sequencing signal that is invisible at the deck level may be readable at the
spell level: if they opened Lightning + Barb Barrel, is Snowball + Poison the common
follow-up? And does their game-1 WIN CONDITION change the answer -- e.g. having already
spent Royal Hogs, does the biggest spell-bait threat being gone push them toward Poison/Log?

THE TRAP THIS SCRIPT AVOIDS
---------------------------
Cards cannot repeat inside a duel set. So a game-1 Lightning + Barb Barrel MECHANICALLY
guarantees game 2 has neither. Naively comparing "P(game-2 spells | game-1 spells)" against
the overall popularity of spell packages would rediscover that rule and dress it up as a
behavioural finding.

So the baseline here is **the constraint-aware one**: the marginal distribution of game-2
spell packages RENORMALISED over only those packages that are actually still legal given
what game 1 burned. Lift above that baseline is genuine preference; lift above the naive
baseline is mostly just arithmetic.

    reports/spell_sequences.md
"""
import os
import sys
import collections
import datetime
import json
import numpy as np

REPO = os.environ.get("CRL_REPO", os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
os.environ.setdefault("CRL_HOME", REPO)
import build_duel_workbook as B  # noqa: E402

PATCH = datetime.datetime(2026, 8, 5, tzinfo=datetime.timezone.utc)

# The damage/utility spell slots. Deliberately EXCLUDES Graveyard and Goblin Barrel: both are
# spells in-game but function as win conditions and are already handled by classify_deck().
SPELLS = {
    "Arrows", "Barbarian Barrel", "Earthquake", "Fireball", "Freeze", "Giant Snowball",
    "Goblin Curse", "Lightning", "Poison", "Rage", "Rocket", "Royal Delivery", "The Log",
    "Tornado", "Void", "Zap", "Clone", "Mirror",
}

MIN_CTX = 20
MIN_CELL = 5
N_PERM = 2000
FDR_Q = 0.10


def fmt(s):
    return " + ".join(sorted(s)) if s else "(no spells)"


def binom_sf(c, n, p):
    """P(X >= c) for X ~ Binomial(n, p). Exact; n here is at most a few hundred."""
    from math import comb
    if p <= 0:
        return 1.0
    if p >= 1:
        return 1.0
    return min(1.0, sum(comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(c, n + 1)))


def add_significance(rows, q=FDR_Q):
    """Exact binomial p per row vs its constraint-aware baseline, then Benjamini-Hochberg.

    Every row is a 'this happened more than the legal-pool baseline predicts' claim, and we
    are scanning hundreds of them, so an uncorrected p<0.05 means nothing here.
    """
    for r in rows:
        r["p"] = binom_sf(r["c"], r["n"], r["base"])
    ps = sorted(r["p"] for r in rows)
    thresh = 0.0
    for i, p in enumerate(ps, 1):
        if p <= q * i / len(ps):
            thresh = p
    for r in rows:
        r["sig"] = r["p"] <= thresh
    return thresh, sum(1 for r in rows if r["sig"])


def load(post_patch=True, category=None, since=None):
    """Duels as ordered lists of {spells, wc, opp_wc, cards}.

    `since` overrides the patch cutoff -- used for the FINALS WINDOW (Day-2 CRL onward),
    where the population is the top-16 field plus their finals prep rather than the whole
    tracked roster.
    """
    duel_log, _, _ = B.build_dataset()
    byd = collections.defaultdict(list)
    for r in duel_log:
        byd[r["duel_id"]].append(r)

    out = []
    for did, rows in byd.items():
        rows = [r for r in rows if not r["is_rematch"] and r["deck"]]
        if len(rows) < 2:
            continue
        rows.sort(key=lambda r: (r["game_num"], r["battle_time"]))
        if post_patch and rows[0]["battle_time"] < PATCH:
            continue
        cat = rows[0].get("match_category") or "Practice"
        if category and cat != category:
            continue
        seen, games = set(), []
        for r in rows:
            if r["game_num"] in seen:
                continue
            seen.add(r["game_num"])
            games.append({
                "spells": frozenset(c for c in r["deck"] if c in SPELLS),
                "cards": frozenset(r["deck"]),
                "wc": frozenset(B.classify_deck(r["deck"])),
                "opp_wc": frozenset(B.classify_deck(r["opponent_deck"] or [])),
            })
        if len(games) >= 2:
            out.append({"games": games[:B.MAX_GAMES_PER_DUEL], "category": cat,
                        "player": rows[0]["player_name"]})
    return out


def feasible_baseline(pool_counts, burned):
    """Marginal over game-2 spell packages, renormalised to those still legal.

    `burned` is the set of cards already spent in this set, so any package sharing a card
    with it is impossible and is dropped before renormalising.
    """
    tot, keep = 0, {}
    for pkg, c in pool_counts.items():
        if pkg & burned:
            continue
        keep[pkg] = c
        tot += c
    if tot == 0:
        return {}, 0
    return {k: v / tot for k, v in keep.items()}, tot


def analyse(duels, label, out_lines, min_ctx=MIN_CTX):
    g2_pool = collections.Counter()
    for d in duels:
        if len(d["games"]) >= 2:
            g2_pool[d["games"][1]["spells"]] += 1

    # ---------------------------------------------------- A: g1 spells -> g2 spells
    ctx = collections.defaultdict(collections.Counter)
    ctxn = collections.Counter()
    for d in duels:
        g = d["games"]
        if len(g) < 2:
            continue
        ctx[g[0]["spells"]][g[1]["spells"]] += 1
        ctxn[g[0]["spells"]] += 1

    rows = []
    for c1, tc in ctx.items():
        n = ctxn[c1]
        if n < min_ctx:
            continue
        base, _ = feasible_baseline(g2_pool, c1)
        for pkg, cnt in tc.items():
            if cnt < MIN_CELL:
                continue
            b = base.get(pkg, 0.0)
            if b <= 0:
                continue
            rows.append({"ctx": fmt(c1), "tgt": fmt(pkg), "n": n, "c": cnt,
                         "rate": cnt / n, "base": b, "lift": (cnt / n) / b})
    thr1, ns1 = add_significance(rows) if rows else (0.0, 0)
    rows.sort(key=lambda r: (-r["sig"], -r["lift"]))

    out_lines.append(f"\n## {label}\n")
    out_lines.append(f"\nDuels: **{len(duels)}** · distinct game-2 spell packages: "
                     f"**{len(g2_pool)}**\n")
    out_lines.append("\n### Game 1 spells → game 2 spells\n\n")
    out_lines.append("Baseline is constraint-aware: the game-2 package distribution "
                     "renormalised over only packages still legal after game 1 burned its "
                     "cards. Lift is therefore preference, not the no-repeat rule.\n\n")
    if rows:
        out_lines.append(f"\n**{ns1} of {len(rows)} rows survive FDR correction "
                         f"(q={FDR_Q}, threshold p<={thr1:.5f}). Only ticked rows are "
                         f"trustworthy.**\n\n")
        out_lines.append("| ✓ | they opened with | they follow with | rate | legal-base | lift | n | p |\n")
        out_lines.append("|---|---|---|---|---|---|---|---|\n")
        for r in rows[:20]:
            out_lines.append(f"| {'**✓**' if r['sig'] else ''} | {r['ctx']} | **{r['tgt']}** | {r['rate']:.0%} | "
                             f"{r['base']:.0%} | {r['lift']:.2f}x | {r['n']} | {r['p']:.4f} |\n")
    else:
        out_lines.append(f"_No game-1 spell package reached {min_ctx} observations._\n")

    # ------------------------------------- B: (their g1 win con + g1 spells) -> g2 spells
    ctx2 = collections.defaultdict(collections.Counter)
    ctx2n = collections.Counter()
    for d in duels:
        g = d["games"]
        if len(g) < 2:
            continue
        for w in g[0]["wc"]:
            ctx2[(w, g[0]["spells"])][g[1]["spells"]] += 1
            ctx2n[(w, g[0]["spells"])] += 1

    rows2 = []
    for (w, c1), tc in ctx2.items():
        n = ctx2n[(w, c1)]
        if n < max(12, min_ctx // 2):
            continue
        base, _ = feasible_baseline(g2_pool, c1)
        for pkg, cnt in tc.items():
            if cnt < MIN_CELL:
                continue
            b = base.get(pkg, 0.0)
            if b <= 0:
                continue
            rows2.append({"wc": w, "ctx": fmt(c1), "tgt": fmt(pkg), "n": n, "c": cnt,
                          "rate": cnt / n, "base": b, "lift": (cnt / n) / b})
    thr2, ns2 = add_significance(rows2) if rows2 else (0.0, 0)
    rows2.sort(key=lambda r: (-r["sig"], -r["lift"]))
    out_lines.append("\n### Their game-1 win condition + spells → their game-2 spells\n\n")
    out_lines.append("Your hypothesis: having already spent (say) Royal Hogs, the biggest "
                     "spell-bait threat is gone, which should move their next spell choice.\n\n")
    if rows2:
        out_lines.append(f"\n**{ns2} of {len(rows2)} rows survive FDR (q={FDR_Q}, "
                         f"p<={thr2:.5f}).**\n\n")
        out_lines.append("| ✓ | g1 win con | g1 spells | g2 spells | rate | legal-base | lift | n | p |\n")
        out_lines.append("|---|---|---|---|---|---|---|---|---|\n")
        for r in rows2[:20]:
            out_lines.append(f"| {'**✓**' if r['sig'] else ''} | {r['wc']} | {r['ctx']} | **{r['tgt']}** | {r['rate']:.0%} | "
                             f"{r['base']:.0%} | {r['lift']:.2f}x | {r['n']} | {r['p']:.4f} |\n")
    else:
        out_lines.append("_No (win condition, spell package) context reached the minimum "
                         "sample._\n")

    # ---------------------------------------------------- C: g1+g2 spells -> g3 spells
    g3_pool = collections.Counter()
    for d in duels:
        if len(d["games"]) >= 3:
            g3_pool[d["games"][2]["spells"]] += 1
    ctx3 = collections.defaultdict(collections.Counter)
    ctx3n = collections.Counter()
    for d in duels:
        g = d["games"]
        if len(g) < 3:
            continue
        key = (g[0]["spells"] | g[1]["spells"])
        ctx3[key][g[2]["spells"]] += 1
        ctx3n[key] += 1
    rows3 = []
    for k, tc in ctx3.items():
        n = ctx3n[k]
        if n < max(12, min_ctx // 2):
            continue
        base, _ = feasible_baseline(g3_pool, k)
        for pkg, cnt in tc.items():
            if cnt < MIN_CELL:
                continue
            b = base.get(pkg, 0.0)
            if b <= 0:
                continue
            rows3.append({"ctx": fmt(k), "tgt": fmt(pkg), "n": n, "c": cnt,
                          "rate": cnt / n, "base": b, "lift": (cnt / n) / b})
    thr3, ns3 = add_significance(rows3) if rows3 else (0.0, 0)
    rows3.sort(key=lambda r: (-r["sig"], -r["lift"]))
    out_lines.append("\n### Games 1+2 spells → game 3 spells\n\n")
    out_lines.append(f"Duels reaching game 3: **{sum(g3_pool.values())}**. By game 3 up to "
                     "four spells are burned, so the legal pool is small — which is exactly "
                     "why this is the most predictable slot.\n\n")
    if rows3:
        out_lines.append(f"\n**{ns3} of {len(rows3)} rows survive FDR (q={FDR_Q}, "
                         f"p<={thr3:.5f}).**\n\n")
        out_lines.append("| ✓ | spells already used (g1+g2) | game 3 spells | rate | legal-base | lift | n | p |\n")
        out_lines.append("|---|---|---|---|---|---|---|---|\n")
        for r in rows3[:20]:
            out_lines.append(f"| {'**✓**' if r['sig'] else ''} | {r['ctx']} | **{r['tgt']}** | {r['rate']:.0%} | "
                             f"{r['base']:.0%} | {r['lift']:.2f}x | {r['n']} | {r['p']:.4f} |\n")
    else:
        out_lines.append("_No game-1+2 spell combination reached the minimum sample._\n")

    # ---------------------------------------------------- how concentrated is the space?
    tot = sum(g2_pool.values())
    out_lines.append("\n### Most common game-2 spell packages overall\n\n")
    out_lines.append("| package | share |\n|---|---|\n")
    for pkg, c in g2_pool.most_common(10):
        out_lines.append(f"| {fmt(pkg)} | {c/tot:.0%} |\n")

    return {"rows": rows[:18], "rows2": rows2[:18], "rows3": rows3[:18],
            "pool": [[fmt(k), v / tot] for k, v in g2_pool.most_common(10)],
            "n_duels": len(duels)}


def main():
    lines = ["# Spell sequencing across a duel set\n",
             f"\n_Generated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC_\n",
             "\nSpells are a ~18-card space and most decks run two, so sequence signal that "
             "is invisible at deck level may be readable here.\n",
             "\n> **Method note.** Cards cannot repeat inside a duel set, so game-1 spells are "
             "mechanically absent from game 2. Every baseline below is renormalised over only "
             "the packages still legal, so the lift column measures preference rather than "
             "re-deriving the no-repeat rule.\n"]

    payload = {}
    for label, cat in [("Post-patch (Aug 5+) — CRL + practice", None),
                       ("Post-patch (Aug 5+) — Official CRL only", "Official CRL")]:
        duels = load(post_patch=True, category=cat)
        print(f"{label}: {len(duels)} duels")
        payload[label] = analyse(duels, label, lines,
                                 min_ctx=MIN_CTX if cat is None else 12)

    os.makedirs(os.path.join(REPO, "reports"), exist_ok=True)
    p = os.path.join(REPO, "reports", "spell_sequences.md")
    with open(p, "w") as f:
        f.write("".join(lines))
    with open(os.path.join(REPO, "reports", "spell_sequences.json"), "w") as f:
        json.dump(payload, f, indent=1)
    print("wrote", p)


if __name__ == "__main__":
    main()
