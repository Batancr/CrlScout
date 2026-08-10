"""
analyze_chaos.py -- turn the chaos/battles archive into draft analytics.

THE DRAFT DECODE (confirmed by Alexander against his in-game log, 2026-08-09)
----------------------------------------------------------------------------
Both players draft from ONE shared 16-card pool. Each player makes 4 choices between 2
cards; whichever card they take goes to their deck and the other goes to the opponent.
The API's card array preserves this:

    my[i]  is paired with  opp[9-i]      (1-based, for all i = 1..8)

      i = 1..4  ->  MY four choices, in draft order. I took my[i], they got opp[9-i].
      i = 5..8  ->  THEIR four choices, in reverse order. They took opp[9-i], I got my[i].

So positions 1-4 of a deck are that player's picks, and 5-8 are what the opponent passed
on. Verified two ways: it matches Alexander's in-game log exactly, and for the handful of
battles captured from BOTH players' logs it produces identical decisions from either side.

WHY THIS MATTERS: every battle records not just what was played but what was REJECTED.
That's a revealed preference, and it's a far better measure of perceived card value than
a usage count -- a card can only be "used a lot" if it's offered a lot.

WHAT COMES OUT (all into chaos/reports/)
    card_pick_and_win.csv     pick rate + win rate per card, tracked-top-players vs field
    draft_pairs.csv           every A-vs-B choice and which side won it
    picked_vs_passed.csv      win rate when chosen vs when handed to you
    card_strength_model.csv   ridge logistic regression: a card's effect on winning with
                              the other 15 cards held fixed (needs numpy; skipped if absent)
    summary.md                the headline numbers

Run: python analyze_chaos.py
"""
import csv
import json
import math
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BATTLE_DIR = os.path.join(HERE, "battles")
ROSTER_PATH = os.path.join(HERE, "roster.json")
OUT_DIR = os.path.join(HERE, "reports")

# Batan is a top Chaos Draft player and is analysed as one of the tracked group, not
# separately (changed 2026-08-09 at Alexander's direction). Kept as a named set only so
# his two accounts can be labelled in the per-player table.
BATAN = {"#9RQ8YRYQL", "#9RG0VPUVY"}
MIN_OFFERS = 25          # don't rank a card until it's been offered this often
MIN_SIDE_GAMES = 40      # for the picked-vs-passed split, per side


def canon(t):
    t = (t or "").strip().upper()
    return t if t.startswith("#") else f"#{t}"


def load_battles():
    """Dedupe across sources: the same battle appears in both players' logs when we track
    both, keyed by (battleTime, unordered tag pair).

    Two sources are read. baseline_backfill.json is a FROZEN snapshot of every Chaos Draft
    battle already visible in the CRL archive when this tracker was created -- it is never
    fetched or mutated, it just means the analysis has history from day one instead of
    starting at an empty API window. battles/ is the live, growing archive."""
    out = {}
    baseline = os.path.join(HERE, "baseline_backfill.json")
    if os.path.exists(baseline):
        try:
            with open(baseline) as f:
                for b in json.load(f):
                    t = (b.get("team") or [{}])[0]
                    o = (b.get("opponent") or [{}])[0]
                    tc = [c.get("name") for c in (t.get("cards") or [])]
                    oc = [c.get("name") for c in (o.get("cards") or [])]
                    if len(tc) == 8 and len(oc) == 8:
                        key = (b.get("battleTime"),
                               frozenset((canon(t.get("tag")), canon(o.get("tag")))))
                        out.setdefault(key, (t, o, tc, oc))
        except (json.JSONDecodeError, OSError):
            pass
    if not os.path.isdir(BATTLE_DIR):
        return out
    for fn in sorted(os.listdir(BATTLE_DIR)):
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(BATTLE_DIR, fn)) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        for b in data:
            t = (b.get("team") or [{}])[0]
            o = (b.get("opponent") or [{}])[0]
            tc = [c.get("name") for c in (t.get("cards") or [])]
            oc = [c.get("name") for c in (o.get("cards") or [])]
            if len(tc) != 8 or len(oc) != 8:
                continue
            key = (b.get("battleTime"), frozenset((canon(t.get("tag")), canon(o.get("tag")))))
            out.setdefault(key, (t, o, tc, oc))
    return out


def decode_draft(tc, oc):
    """-> list of (chooser_is_team, chosen, rejected, round_number). See the module docstring."""
    d = []
    for i in range(4):
        d.append((True, tc[i], oc[7 - i], i + 1))
    for i in range(4, 8):
        d.append((False, oc[7 - i], tc[i], 8 - i))
    return d


def pct(x):
    return f"{x:.1%}"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    battles = load_battles()
    if not battles:
        print("No battles archived yet -- run fetch_chaos.py first.")
        return 0
    roster = {}
    if os.path.exists(ROSTER_PATH):
        with open(ROSTER_PATH) as f:
            roster = json.load(f)
    tracked = {canon(t) for t in roster}

    stats = defaultdict(lambda: {"off": Counter(), "pick": Counter(),
                                 "ind": Counter(), "win": Counter()})
    pairs, pairwin = Counter(), Counter()
    pw, pn, rw, rn = Counter(), Counter(), Counter(), Counter()
    per_player = defaultdict(lambda: {"g": 0, "w": 0})

    for (t, o, tc, oc) in battles.values():
        tt, ot = canon(t.get("tag")), canon(o.get("tag"))
        tcr, ocr = t.get("crowns") or 0, o.get("crowns") or 0
        if tcr == ocr:
            continue
        twin = tcr > ocr
        for tag, won in ((tt, twin), (ot, not twin)):
            if tag in tracked:
                per_player[tag]["g"] += 1
                per_player[tag]["w"] += 1 if won else 0

        for chooser_is_team, chosen, rejected, _rnd in decode_draft(tc, oc):
            tag = tt if chooser_is_team else ot
            groups = ["field"]
            if tag in tracked:
                groups.append("top")
            for g in groups:
                stats[g]["off"][chosen] += 1
                stats[g]["off"][rejected] += 1
                stats[g]["pick"][chosen] += 1
            k = tuple(sorted((chosen, rejected)))
            pairs[k] += 1
            pairwin[(k, chosen)] += 1

        for tag, cards, won in ((tt, tc, twin), (ot, oc, not twin)):
            g = "top" if tag in tracked else "field"
            for i, c in enumerate(cards):
                for grp in ({g} | ({"field"} if g == "top" else set())):
                    stats[grp]["ind"][c] += 1
                    if won:
                        stats[grp]["win"][c] += 1
                if i < 4:
                    pn[c] += 1
                    pw[c] += 1 if won else 0
                else:
                    rn[c] += 1
                    rw[c] += 1 if won else 0

    # ---- card_strength_model.csv (optional; needs numpy) ----
    model_note = "numpy not installed -- strength model skipped."
    strength = {}
    try:
        import numpy as np
        cards = sorted({c for _, _, tc, oc in battles.values() for c in tc + oc})
        idx = {c: i for i, c in enumerate(cards)}
        X, y = [], []
        for (t, o, tc, oc) in battles.values():
            tcr, ocr = t.get("crowns") or 0, o.get("crowns") or 0
            if tcr == ocr:
                continue
            v = np.zeros(len(cards))
            for c in tc:
                v[idx[c]] += 1
            for c in oc:
                v[idx[c]] -= 1
            X.append(v)
            y.append(1.0 if tcr > ocr else 0.0)
        X, y = np.array(X), np.array(y)
        if len(y) >= 200:
            wgt = np.zeros(len(cards))
            lam, lr = 2.0, 0.5
            for _ in range(4000):
                p = 1 / (1 + np.exp(-X @ wgt))
                wgt -= lr * (X.T @ (p - y) / len(y) + lam * wgt / len(y))
            acc = (((1 / (1 + np.exp(-X @ wgt))) > 0.5) == (y > 0.5)).mean()
            with open(os.path.join(OUT_DIR, "card_strength_model.csv"), "w", newline="",
                      encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Card", "Strength", "Top Pick Rate", "Times Offered (all)"])
                for c, s in sorted(zip(cards, wgt), key=lambda kv: -kv[1]):
                    off = stats["field"]["off"][c]
                    w.writerow([c, f"{s:+.3f}",
                                pct(stats["top"]["pick"][c] / stats["top"]["off"][c])
                                if stats["top"]["off"][c] else "", off])
            strength = dict(zip(cards, (float(x) for x in wgt)))
            model_note = f"strength model fitted on {len(y)} battles, in-sample accuracy {acc:.1%}."
        else:
            model_note = f"only {len(y)} battles -- need 200+ for the strength model."
    except ImportError:
        pass

    # ---- card_pick_and_win.csv ----
    all_cards = sorted(set(stats["field"]["off"]) | set(stats["top"]["off"]))
    with open(os.path.join(OUT_DIR, "card_pick_and_win.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Card",
                    "Top Offered", "Top Picked", "Top Pick Rate", "Top Games", "Top Win Rate",
                    "Field Offered", "Field Pick Rate", "Field Games", "Field Win Rate"])
        for c in all_cards:
            tp, fl = stats["top"], stats["field"]
            w.writerow([c,
                        tp["off"][c], tp["pick"][c],
                        pct(tp["pick"][c] / tp["off"][c]) if tp["off"][c] else "",
                        tp["ind"][c], pct(tp["win"][c] / tp["ind"][c]) if tp["ind"][c] else "",
                        fl["off"][c], pct(fl["pick"][c] / fl["off"][c]) if fl["off"][c] else "",
                        fl["ind"][c], pct(fl["win"][c] / fl["ind"][c]) if fl["ind"][c] else ""])

    # ---- draft_pairs.csv ----
    with open(os.path.join(OUT_DIR, "draft_pairs.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Card A", "Card B", "Offered Together", "A Picked", "B Picked", "A Pick Rate"])
        for (a, b), n in pairs.most_common():
            aw = pairwin[((a, b), a)]
            w.writerow([a, b, n, aw, n - aw, pct(aw / n)])

    # ---- picked_vs_passed.csv ----
    with open(os.path.join(OUT_DIR, "picked_vs_passed.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Card", "Win Rate When Picked", "Games Picked",
                    "Win Rate When Passed To You", "Games Passed", "Difference", "Z"])
        rows = []
        for c in set(pn) | set(rn):
            if pn[c] < MIN_SIDE_GAMES or rn[c] < MIN_SIDE_GAMES:
                continue
            p, r = pw[c] / pn[c], rw[c] / rn[c]
            se = math.sqrt(p * (1 - p) / pn[c] + r * (1 - r) / rn[c])
            rows.append((c, p, pn[c], r, rn[c], p - r, (p - r) / se if se else 0.0))
        for c, p, a, r, b, d, z in sorted(rows, key=lambda x: -x[5]):
            w.writerow([c, pct(p), a, pct(r), b, f"{d:+.1%}", f"{z:.2f}"])

    # ---- player_profiles.csv : how each tracked player DRAFTS ----
    #
    # The headline stat here is DRAFT EDGE: using the fitted card strengths, the average of
    # strength(card they took) - strength(card they passed on), across all their choices.
    # Because the offered pairs are random (verified: elixir, rarity and spell-vs-spell
    # rates all match a shuffled null), every player faces a comparable distribution of
    # decisions -- so this isolates decision quality from luck of the draw in a way raw win
    # rate cannot. Positive = they consistently take the better card of the two.
    #
    # It's only meaningful once a player has a few dozen decisions; the CSV carries the
    # count so thin rows can be filtered rather than silently trusted.
    prof = defaultdict(lambda: {"g": 0, "w": 0, "dec": 0, "edge": 0.0,
                                "pick": Counter(), "off": Counter()})
    for (t, o, tc, oc) in battles.values():
        tt, ot = canon(t.get("tag")), canon(o.get("tag"))
        tcr, ocr = t.get("crowns") or 0, o.get("crowns") or 0
        if tcr == ocr:
            continue
        for chooser_is_team, chosen, rejected, _r in decode_draft(tc, oc):
            tag = tt if chooser_is_team else ot
            if tag not in tracked:
                continue
            p = prof[tag]
            p["dec"] += 1
            p["pick"][chosen] += 1
            p["off"][chosen] += 1
            p["off"][rejected] += 1
            if strength:
                p["edge"] += strength.get(chosen, 0.0) - strength.get(rejected, 0.0)
    for tag, d in per_player.items():
        prof[tag]["g"], prof[tag]["w"] = d["g"], d["w"]

    field_rate = {c: (stats["field"]["pick"][c] / stats["field"]["off"][c])
                  for c in stats["field"]["off"] if stats["field"]["off"][c]}
    with open(os.path.join(OUT_DIR, "player_profiles.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Player", "Tag", "Games", "Wins", "Win Rate", "Draft Decisions",
                    "Draft Edge (avg strength gained per pick)",
                    "Most Picked #1", "Most Picked #2", "Most Picked #3",
                    "Most Contrarian Pick (vs field)", "Most Avoided (vs field)"])
        for tag, p in sorted(prof.items(), key=lambda kv: -kv[1]["g"]):
            if not p["dec"]:
                continue
            nm = (roster.get(tag, {}) or {}).get("name") or tag
            top = [c for c, _ in p["pick"].most_common(3)]
            # divergence vs the field, only on cards this player saw enough times
            div = []
            for c, n in p["off"].items():
                if n < 4 or c not in field_rate:
                    continue
                div.append((c, p["pick"][c] / n - field_rate[c], n))
            div.sort(key=lambda x: -x[1])
            hi = f"{div[0][0]} (+{div[0][1]:.0%})" if div else ""
            lo = f"{div[-1][0]} ({div[-1][1]:.0%})" if div else ""
            w.writerow([nm, tag, p["g"], p["w"],
                        pct(p["w"] / p["g"]) if p["g"] else "",
                        p["dec"], f"{p['edge']/p['dec']:+.3f}" if p["dec"] and strength else "",
                        *(top + [""] * 3)[:3], hi, lo])

    # ---- summary.md ----
    def top_by(group, key, n=10, reverse=True):
        s = stats[group]
        rows = [(c, s["pick"][c] / s["off"][c], s["off"][c],
                 (s["win"][c] / s["ind"][c]) if s["ind"][c] else 0.0, s["ind"][c])
                for c in s["off"] if s["off"][c] >= MIN_OFFERS]
        return sorted(rows, key=lambda r: -r[key] if reverse else r[key])[:n]

    lines = ["# Chaos Draft tracker", "",
             f"- Unique battles archived: **{len(battles)}**",
             f"- Tracked top players: **{len(tracked)}**",
             f"- Draft decisions decoded: **{sum(stats['field']['pick'].values())}**",
             f"- {model_note}", "",
             "## Most picked when offered — tracked top players", "",
             "| Card | Pick rate | Offers | Win rate |", "|---|---|---|---|"]
    for c, pr, off, wr, ind in top_by("top", 1):
        lines.append(f"| {c} | {pr:.0%} | {off} | {wr:.0%} |")
    lines += ["", "## Least picked — tracked top players", "",
              "| Card | Pick rate | Offers | Win rate |", "|---|---|---|---|"]
    for c, pr, off, wr, ind in top_by("top", 1, reverse=False):
        lines.append(f"| {c} | {pr:.0%} | {off} | {wr:.0%} |")
    # ---- automatic findings ----
    # Recomputed every run so the interesting questions answer themselves as data arrives,
    # instead of needing a fresh manual pass each time.
    lines += ["", "## What separates the top players from the field", "",
              "Pick-rate gap on cards both groups saw enough of. A positive gap means the",
              "tracked top players take it more often than the field does.", "",
              "| Card | Top | Field | Gap | Model strength |", "|---|---|---|---|---|"]
    gaps = []
    for c, n in stats["top"]["off"].items():
        fn = stats["field"]["off"][c]
        if n < 40 or fn < 200:
            continue
        gaps.append((c, stats["top"]["pick"][c] / n, stats["field"]["pick"][c] / fn,
                     strength.get(c)))
    gaps.sort(key=lambda r: -(r[1] - r[2]))
    for c, tr, fr, st in gaps[:6]:
        lines.append(f"| {c} | {tr:.0%} | {fr:.0%} | **+{tr-fr:.0%}** | "
                     f"{st:+.2f} |" if st is not None else
                     f"| {c} | {tr:.0%} | {fr:.0%} | **+{tr-fr:.0%}** | — |")
    lines += ["", "Cards the top players avoid *more* than the field:", "",
              "| Card | Top | Field | Gap | Model strength |", "|---|---|---|---|---|"]
    for c, tr, fr, st in gaps[-6:]:
        lines.append(f"| {c} | {tr:.0%} | {fr:.0%} | **{tr-fr:.0%}** | "
                     f"{st:+.2f} |" if st is not None else
                     f"| {c} | {tr:.0%} | {fr:.0%} | **{tr-fr:.0%}** | — |")

    # Who drafts unlike the rest of the tracked group? Mean absolute deviation of a
    # player's pick rates from the group's, over cards they've each seen enough times.
    lines += ["", "## Draft-style outliers among the tracked players", "",
              "How far each player's pick rates sit from the tracked-group consensus.",
              "Higher = more idiosyncratic. Needs 100+ decisions to mean much.", "",
              "| Player | Decisions | Deviation from consensus | Draft edge | Win rate |",
              "|---|---|---|---|---|"]
    top_rate = {c: stats["top"]["pick"][c] / n for c, n in stats["top"]["off"].items() if n}
    devs = []
    for tag, p in prof.items():
        if p["dec"] < 100:
            continue
        ds = [abs(p["pick"][c] / n - top_rate[c])
              for c, n in p["off"].items() if n >= 5 and c in top_rate]
        if len(ds) < 15:
            continue
        devs.append((tag, sum(ds) / len(ds), p))
    for tag, d, p in sorted(devs, key=lambda r: -r[1]):
        nm = (roster.get(tag, {}) or {}).get("name") or tag
        edge = f"{p['edge']/p['dec']:+.3f}" if p["dec"] and strength else "—"
        wr = f"{p['w']/p['g']:.0%}" if p["g"] else "—"
        lines.append(f"| {nm} | {p['dec']} | {d:.3f} | {edge} | {wr} |")
    if not devs:
        lines.append("| *(no player has 100+ decisions yet)* | | | | |")

    lines += ["", "## Tracked players", "", "| Player | Games | Win rate |", "|---|---|---|"]
    for tag, d in sorted(per_player.items(), key=lambda kv: -kv[1]["g"]):
        nm = (roster.get(tag, {}) or {}).get("name") or tag
        flag = " *(your account)*" if tag in BATAN else ""
        lines.append(f"| {nm}{flag} | {d['g']} | {d['w']/d['g']:.0%} |" if d["g"] else "")
    with open(os.path.join(OUT_DIR, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"{len(battles)} battles | {len(tracked)} tracked top players | "
          f"{sum(stats['field']['pick'].values())} decisions decoded")
    print(model_note)
    print(f"reports written to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
