"""
scout_player_sequences.py -- single-player deck/win-condition sequencing profile.

Built for finals prep: given one player, show what they actually open with, what they follow
it with, and -- the question that matters -- HOW PREDICTABLE they are compared with everyone
else on the roster.

WHY A PERCENTILE AND NOT JUST COUNTS
------------------------------------
"Asaf sticks to the win-condition sequences he knows best" is a claim about him RELATIVE to
other players. A raw repeat rate can't test it: every player repeats somewhat. So the same
concentration metrics are computed for all rostered players with a comparable number of
duels, and the subject is placed as a percentile within that distribution. At n=16-74 the
per-transition counts are far too thin for significance, but a concentration percentile is
stable and honest.

Two metrics:
  * pool concentration -- share of their games played with their top 3 decks. High = small
    rehearsed pool.
  * transition entropy  -- normalised Shannon entropy of (game-1 win con -> game-2 win con).
    0.0 = perfectly scripted follow-up, 1.0 = uniformly unpredictable.

USAGE
    python scout_player_sequences.py "Asaf"
"""
import os
import sys
import json
import math
import collections
import datetime

REPO = os.environ.get("CRL_REPO", os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
os.environ.setdefault("CRL_HOME", REPO)
import build_duel_workbook as B  # noqa: E402

PATCH = datetime.datetime(2026, 8, 5, tzinfo=datetime.timezone.utc)
MIN_DUELS_FOR_PEER = 12

FRAMINGS = [
    ("post-patch, CRL + practice", True,  None),
    ("post-patch, Official CRL only", True,  "Official CRL"),
    ("all time, CRL + practice", False, None),
    ("all time, Official CRL only", False, "Official CRL"),
]


def load_player_duels():
    """player_name -> list of duels, each a list of (wincons, deck, category, time)."""
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
        games = []
        seen = set()
        for r in rows:
            if r["game_num"] in seen:
                continue
            seen.add(r["game_num"])
            games.append({
                "wc": frozenset(B.classify_deck(r["deck"])),
                "deck": frozenset(r["deck"]),
                "opp_wc": frozenset(B.classify_deck(r["opponent_deck"] or [])),
            })
        out[rows[0]["player_name"]].append({
            "category": rows[0].get("match_category") or "Practice",
            "time": rows[0]["battle_time"],
            "opponent": rows[0]["opponent_name"],
            "games": games[:B.MAX_GAMES_PER_DUEL],
        })
    return out


def subset(duels, post_patch, category):
    out = []
    for d in duels:
        if post_patch and d["time"] < PATCH:
            continue
        if category and d["category"] != category:
            continue
        out.append(d)
    return out


def norm_entropy(counter):
    tot = sum(counter.values())
    if tot <= 1 or len(counter) <= 1:
        return 0.0
    h = -sum((c / tot) * math.log(c / tot, 2) for c in counter.values() if c)
    return h / math.log(len(counter), 2)


def profile(duels):
    """Concentration + transition stats for one player under one framing."""
    deck_ct = collections.Counter()
    g1 = collections.Counter()
    trans = collections.defaultdict(collections.Counter)
    seqs = collections.Counter()
    n_games = 0
    for d in duels:
        gs = d["games"]
        for g in gs:
            deck_ct[tuple(sorted(g["deck"]))] += 1
            n_games += 1
        if gs:
            for w in gs[0]["wc"]:
                g1[w] += 1
        if len(gs) >= 2:
            for a in gs[0]["wc"]:
                for b in gs[1]["wc"]:
                    trans[a][b] += 1
        if len(gs) >= 3:
            key = (" / ".join(sorted(gs[0]["wc"])) or "?",
                   " / ".join(sorted(gs[1]["wc"])) or "?",
                   " / ".join(sorted(gs[2]["wc"])) or "?")
            seqs[key] += 1

    top3 = sum(c for _, c in deck_ct.most_common(3))
    conc = top3 / n_games if n_games else 0.0
    ent = [norm_entropy(c) for c in trans.values() if sum(c.values()) >= 3]
    return {
        "n_duels": len(duels), "n_games": n_games,
        "pool_size": len(deck_ct), "concentration": conc,
        "entropy": (sum(ent) / len(ent)) if ent else None,
        "deck_ct": deck_ct, "g1": g1, "trans": trans, "seqs": seqs,
    }


def percentile(value, peers, lower_is_more_predictable=False):
    if not peers or value is None:
        return None
    if lower_is_more_predictable:
        below = sum(1 for p in peers if p > value)
    else:
        below = sum(1 for p in peers if p < value)
    return 100.0 * below / len(peers)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "Asaf"
    allp = load_player_duels()
    if target not in allp:
        cand = [n for n in allp if target.lower() in (n or "").lower()]
        print(f"'{target}' not found. Close matches: {cand[:10]}")
        return

    report = {"player": target, "framings": []}
    lines = [f"# Scouting profile — {target}\n",
             f"_Generated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC_\n",
             "\nPredictability is reported as a **percentile against the roster** — the "
             "claim \"sticks to sequences he knows\" is comparative, so a raw repeat rate "
             "can't test it. Peers are all players with at least "
             f"{MIN_DUELS_FOR_PEER} duels in the same framing.\n"]

    for label, post, cat in FRAMINGS:
        me = profile(subset(allp[target], post, cat))
        peers_c, peers_e = [], []
        for name, duels in allp.items():
            if name == target:
                continue
            p = profile(subset(duels, post, cat))
            if p["n_duels"] >= MIN_DUELS_FOR_PEER:
                peers_c.append(p["concentration"])
                if p["entropy"] is not None:
                    peers_e.append(p["entropy"])

        pc = percentile(me["concentration"], peers_c)
        pe = percentile(me["entropy"], peers_e, lower_is_more_predictable=True)

        lines.append(f"\n## {label}\n")
        lines.append(f"- **{me['n_duels']} duels · {me['n_games']} games · "
                     f"{me['pool_size']} distinct decks**\n")
        if me["n_duels"] < 10:
            lines.append(f"- ⚠️ **Only {me['n_duels']} duels — treat everything below as "
                         "indicative, not established.**\n")
        lines.append(f"- Top-3 deck concentration: **{me['concentration']:.0%}** of games"
                     + (f" — more concentrated than **{pc:.0f}%** of the roster "
                        f"({len(peers_c)} peers)\n" if pc is not None else "\n"))
        if me["entropy"] is not None:
            lines.append(f"- Follow-up entropy: **{me['entropy']:.2f}** (0 = scripted, "
                         f"1 = unpredictable)"
                         + (f" — more predictable than **{pe:.0f}%** of the roster\n"
                            if pe is not None else "\n"))

        lines.append("\n**Opens game 1 with:**\n\n| win condition | games |\n|---|---|\n")
        for w, c in me["g1"].most_common(8):
            lines.append(f"| {w} | {c} |\n")

        rows = []
        for a, tc in me["trans"].items():
            tot = sum(tc.values())
            for b, c in tc.most_common(3):
                rows.append((c, a, b, tot))
        if rows:
            lines.append("\n**Game 1 → game 2 win condition:**\n\n"
                         "| after opening | follows with | n | share |\n|---|---|---|---|\n")
            for c, a, b, tot in sorted(rows, reverse=True)[:14]:
                lines.append(f"| {a} | **{b}** | {c} | {c/tot:.0%} |\n")

        if me["seqs"]:
            lines.append("\n**Full 3-game sequences seen more than once:**\n\n"
                         "| game 1 | game 2 | game 3 | times |\n|---|---|---|---|\n")
            any_rep = False
            for (x, y, z), c in me["seqs"].most_common(10):
                if c > 1:
                    any_rep = True
                    lines.append(f"| {x} | {y} | {z} | {c} |\n")
            if not any_rep:
                lines.append("| _no exact 3-game sequence repeated_ | | | |\n")

        report["framings"].append({
            "label": label, "n_duels": me["n_duels"], "n_games": me["n_games"],
            "pool_size": me["pool_size"], "concentration": me["concentration"],
            "entropy": me["entropy"], "conc_pctile": pc, "entropy_pctile": pe,
            "g1": me["g1"].most_common(8),
            "trans": sorted(((a, b, c, sum(tc.values()))
                             for a, tc in me["trans"].items() for b, c in tc.most_common(3)),
                            key=lambda r: -r[2])[:14],
            "seqs": [[list(k), v] for k, v in me["seqs"].most_common(10) if v > 1],
        })
        print(f"{label:34} n={me['n_duels']:3}  conc={me['concentration']:.0%}"
              f"  pctile={pc if pc is None else round(pc)}"
              f"  entropy={me['entropy']}")

    os.makedirs(os.path.join(REPO, "reports"), exist_ok=True)
    md = os.path.join(REPO, "reports", f"scout_{target.lower()}.md")
    with open(md, "w") as f:
        f.write("".join(lines))
    js = os.path.join(REPO, "reports", f"scout_{target.lower()}.json")
    with open(js, "w") as f:
        json.dump(report, f, indent=1, default=str)
    print(f"\nwrote {md}\nwrote {js}")


if __name__ == "__main__":
    main()
