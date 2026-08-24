#!/usr/bin/env python3
"""Set-aware duel-recommendation engine for the CRL dashboard.

Given the combined duel log (every tracked player's Practice + Official CRL games, each row
carrying game_num = position within its Bo3 duel set), this produces, per opponent:
  1. per_set_usage: which win conditions the opponent plays in game 1 / 2 / 3 of their sets,
     as a share of that set's decks (top few covering ~75% of the win-con mass).
  2. set_decks: a set-ordered, duel-legal recommendation drawn from OUR own played decks --
     deck for set 1 is chosen to beat set 1's win-con pool, set 2's deck beats set 2's pool,
     set 3's deck beats set 3's pool -- scored by real matchup win rate (win-con, refined by
     the deck's spell where the data supports it), not by our raw win rate in a slice.

Pure functions; no I/O. build_dashboard.py imports build_all(); a __main__ test harness at the
bottom exercises it from post_rows_0.jsonl with reconstructed game positions.
"""
from collections import Counter, defaultdict

POST_PATCH = "20260804"


# ---- row accessors (work on build_dashboard dict rows) ----
def _won(r):
    cf, ca = r.get("crowns_for"), r.get("crowns_against")
    if cf is None or ca is None:
        w = r.get("won")
        return w
    return cf > ca


def _eligible(r):
    # dashboard marks incomplete post-cutoff practice sets stats_eligible=False; skip them
    # (defaults True so container test rows without the field still count).
    return r.get("stats_eligible", True)


def _date8(bt):
    # battle_time comes in three shapes: a datetime object (dashboard's combined_duel_log),
    # compact "20260804T112650.000Z" (post_rows), or human "2026-08-04 11:26:50" (xlsx).
    # str() normalizes all of them; keep the leading YYYYMMDD digits for the cutoff compare.
    if not bt:
        return ""
    ds = "".join(ch for ch in str(bt) if ch.isdigit())
    return ds[:8]


# ---- matchup matrix from the whole pool ----
def build_matchup(rows, classify_deck, SPELLS, min1=5, min2=5):
    """win-con vs win-con (m1) and win-con+spell vs win-con (m2) win-rate cells."""
    M1 = defaultdict(lambda: [0, 0])   # (a,b) -> [games, wins]
    M2 = defaultdict(lambda: [0, 0])   # (a,s,b) -> [games, wins]
    for r in rows:
        if not r.get("deck") or not r.get("opponent_deck") or not _eligible(r):
            continue
        if _date8(r.get("battle_time")) < POST_PATCH:
            continue
        w = _won(r)
        if w is None:
            continue
        A = classify_deck(r["deck"]) or []
        B = classify_deck(r["opponent_deck"]) or []
        if not A or not B:
            continue
        S = [c for c in r["deck"] if c in SPELLS]
        wv = 1 if w else 0
        for a in A:
            for b in B:
                c = M1[(a, b)]; c[0] += 1; c[1] += wv
                for s in S:
                    c2 = M2[(a, s, b)]; c2[0] += 1; c2[1] += wv
    m1 = defaultdict(dict); m2 = defaultdict(lambda: defaultdict(dict))
    for (a, b), v in M1.items():
        if v[0] >= min1:
            m1[a][b] = [v[0], 100.0 * v[1] / v[0]]
    for (a, s, b), v in M2.items():
        if v[0] >= min2:
            m2[a][s][b] = [v[0], 100.0 * v[1] / v[0]]
    return {k: dict(v) for k, v in m1.items()}, {k: {s: dict(bb) for s, bb in v.items()} for k, v in m2.items()}


# ---- per-set win-con usage for one opponent ----
def per_set_usage(rows, opp_tag, classify_deck, cover=0.75, maxk=4, min_pos_games=6):
    """For each game position 1/2/3, share of that position's decks running each win-con.
    Returns {pos: {"n": nsets_at_pos, "top": [(wincon, pct_of_decks, weight_norm), ...]}}"""
    pos_counts = {1: Counter(), 2: Counter(), 3: Counter()}
    pos_n = {1: 0, 2: 0, 3: 0}
    for r in rows:
        if r.get("player_tag") != opp_tag:
            continue
        if _date8(r.get("battle_time")) < POST_PATCH or not _eligible(r):
            continue
        gnum = r.get("game_num")
        if gnum not in (1, 2, 3):
            continue
        A = classify_deck(r.get("deck") or []) or []
        if not A:
            continue
        pos_n[gnum] += 1
        for a in A:
            pos_counts[gnum][a] += 1
    out = {}
    for pos in (1, 2, 3):
        n = pos_n[pos]
        if n < min_pos_games:
            out[pos] = {"n": n, "top": []}
            continue
        items = pos_counts[pos].most_common()
        total = sum(c for _, c in items) or 1
        top = []
        cum = 0.0
        for wc, c in items:
            share = c / total          # share of win-con mass at this position
            top.append([wc, round(100.0 * c / n, 1), share])   # pct = % of decks running it
            cum += share
            if cum >= cover or len(top) >= maxk:
                break
        # normalize weights over the chosen top
        wsum = sum(t[2] for t in top) or 1
        for t in top:
            t[2] = t[2] / wsum
        out[pos] = {"n": n, "top": top}
    return out


# ---- our own candidate decks ----
def my_deck_pool(rows, my_tag, classify_deck, SPELLS, min_games=2):
    """Distinct 8-card decks we've actually played (post-patch), with win-cons, spells, games."""
    seen = {}
    for r in rows:
        if r.get("player_tag") != my_tag:
            continue
        if _date8(r.get("battle_time")) < POST_PATCH or not _eligible(r):
            continue
        d = r.get("deck") or []
        if len(d) != 8:
            continue
        key = frozenset(d)
        wcs = classify_deck(d) or []
        if not wcs:
            continue
        if key not in seen:
            seen[key] = {"cards": sorted(d), "wcs": sorted(wcs),
                         "spells": sorted(c for c in d if c in SPELLS), "games": 0}
        seen[key]["games"] += 1
    return [v for v in seen.values() if v["games"] >= min_games]


# ---- score a deck vs a set's weighted win-con pool ----
def _deck_rate_vs(deck, target, m1, m2, min2=6):
    """Best rate this deck gets vs one opponent win-con: best of its win-con(+spell) cells."""
    best = None
    for a in deck["wcs"]:
        for s in deck["spells"]:
            c = m2.get(a, {}).get(s, {}).get(target)
            if c and c[0] >= min2:
                best = c[1] if best is None else max(best, c[1])
        c = m1.get(a, {}).get(target)
        if c:
            best = c[1] if best is None else max(best, c[1])
    return best


def score_deck(deck, pool_top, m1, m2):
    """Weighted coverage of a deck vs a set's win-con pool. Returns (coverage%, covered_frac)."""
    sw = sm = 0.0
    covered = 0.0
    for wc, _pct, w in pool_top:
        r = _deck_rate_vs(deck, wc, m1, m2)
        if r is not None:
            sm += w * r; sw += w; covered += w
    if sw == 0:
        return None, 0.0
    return sm / sw, covered


def recommend_set_decks(usage, my_decks, m1, m2, max_overlap=2):
    """Pick a deck per set (1,2,3) to beat that set's pool, minimizing card reuse across the
    three. Greedy by coverage, then a local pass to reduce overlap. Returns list of dicts."""
    # best-scored deck list per set
    per_set_ranked = {}
    for pos in (1, 2, 3):
        pool = usage.get(pos, {}).get("top", [])
        if not pool:
            per_set_ranked[pos] = []
            continue
        scored = []
        for d in my_decks:
            cov, frac = score_deck(d, pool, m1, m2)
            if cov is None:
                continue
            scored.append({"deck": d, "coverage": cov, "covered": frac})
        # coverage is primary (bucketed to whole % so near-ties fall to more-played decks),
        # then games played, then how much of the pool it covers.
        scored.sort(key=lambda x: (-round(x["coverage"]), -x["deck"]["games"], -x["covered"]))
        per_set_ranked[pos] = scored

    # assemble a duel-legal triple: reuse NO cards across the three decks if possible.
    # order sets by how few candidates they have (constrain the hardest set first).
    chosen = {}
    used_cards = set()
    order = sorted((p for p in (1, 2, 3) if per_set_ranked[p]), key=lambda p: len(per_set_ranked[p]))
    for pos in order:
        pick = None; pick_overlap = None
        for thr in (0, 1, 2, 99):     # escalate allowed overlap only as needed
            for cand in per_set_ranked[pos]:
                ov = len(set(cand["deck"]["cards"]) & used_cards)
                if ov <= thr:
                    pick = cand; pick_overlap = ov; break
            if pick is not None:
                break
        chosen[pos] = {**pick, "overlap": pick_overlap,
                       "shared": sorted(set(pick["deck"]["cards"]) & used_cards)}
        used_cards |= set(pick["deck"]["cards"])
    return [{"set": p, **chosen[p]} for p in (1, 2, 3) if p in chosen]


def build_for_opponent(rows, opp_tag, classify_deck, SPELLS, m1, m2, my_decks):
    usage = per_set_usage(rows, opp_tag, classify_deck)
    set_decks = recommend_set_decks(usage, my_decks, m1, m2)
    return {"per_set_usage": usage, "set_decks": set_decks}


def build_all(rows, my_tag, opp_tags, classify_deck, SPELLS):
    m1, m2 = build_matchup(rows, classify_deck, SPELLS)
    my_decks = my_deck_pool(rows, my_tag, classify_deck, SPELLS)
    out = {}
    for tag in opp_tags:
        out[tag] = build_for_opponent(rows, tag, classify_deck, SPELLS, m1, m2, my_decks)
    return out, {"n_my_decks": len(my_decks), "n_m1": len(m1), "n_m2": len(m2)}


# --------------------------------------------------------------------------
# standalone test harness (container): reconstruct game_num from post_rows_0.jsonl
# --------------------------------------------------------------------------
if __name__ == "__main__":
    import json, sys
    D = "/mnt/user-data/uploads/CRL"
    proto = json.load(open(f"{D}/proto_decks.json"))
    WC = set(proto["wincons"]); SPELLS = set(proto["spells"])
    def classify_deck(d): return [c for c in d if c in WC]
    raw = [json.loads(l) for l in open(f"{D}/post_rows_0.jsonl")]

    # reconstruct rows with game_num by grouping each player's games per opponent into sets
    def sig(d): return tuple(sorted(classify_deck(d)))
    rows = []
    bykey = defaultdict(list)
    for r in raw:
        bykey[(r[0], r[1])].append(r)
    for (pt, ot), gs in bykey.items():
        gs.sort(key=lambda r: r[6])
        cur = []; seen = set()
        def flush(cur):
            for i, r in enumerate(cur[:3]):
                rows.append({"player_tag": r[0], "opponent_tag": r[1], "deck": r[2],
                             "opponent_deck": r[3], "crowns_for": r[4], "crowns_against": r[5],
                             "battle_time": r[6], "match_category": r[7], "game_num": i + 1})
        for r in gs:
            s = sig(r[2])
            if len(cur) >= 3 or s in seen:
                flush(cur); cur = []; seen = set()
            cur.append(r); seen.add(s)
        flush(cur)

    FIN = {"#G9YV9GR8R": "Mohamed Light", "#2LJ0ULYCC": "Guriko", "#RUQ0JU2P": "Asaf",
           "#2CLV2RP0": "Mugi", "#9CPCC890": "Adriel"}
    YOU = "#9RQ8YRYQL"
    m1, m2 = build_matchup(rows, classify_deck, SPELLS)
    my_decks = my_deck_pool(rows, YOU, classify_deck, SPELLS)
    print(f"matrix m1={len(m1)} m2={len(m2)} | my candidate decks={len(my_decks)}")
    for tag, name in FIN.items():
        rec = build_for_opponent(rows, tag, classify_deck, SPELLS, m1, m2, my_decks)
        print(f"\n===== {name} =====")
        for pos in (1, 2, 3):
            u = rec["per_set_usage"][pos]
            tops = ", ".join(f"{wc} {pct}%" for wc, pct, w in u["top"])
            print(f"  Set {pos} (n={u['n']}): {tops}")
        for sd in rec["set_decks"]:
            d = sd["deck"]
            print(f"  -> Set {sd['set']} counter: [{'/'.join(d['wcs'])}] +{','.join(d['spells']) or '-'} "
                  f"cov {sd['coverage']:.0f}% (covers {sd['covered']*100:.0f}% of pool, overlap {sd['overlap']}, {d['games']}g)")
            print(f"       deck: {', '.join(d['cards'])}")
